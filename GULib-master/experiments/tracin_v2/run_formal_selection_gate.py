"""Run a formal ``proper-tracin-v1`` Score -> max-k Selection gate on CPU.

This remains an isolated selection-only lane.  It does not register the
strategy in AttackManager or the default GU runner, and it never reads or
writes Legacy Result/Selection/Score caches.
"""

from __future__ import annotations

import argparse
import json
import platform
import socket
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np
import torch
import torch_geometric
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

from cache_v2 import (
    ProducerVersion,
    ScoreArtifactStore,
    ScorePayload,
    ordered_ids_hash,
    sha256_bytes,
)
from cache_v2.legacy_freeze import snapshot_legacy_caches
from experiments.bc_target_v2.dataset_source import (
    canonical_data_root,
    resolve_planetoid_public_source,
    validate_public_split,
)
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import make_dataset_selection_inputs

from .core import tracin_cp_eval_scores
from .formal_recipe import ALGORITHM_VERSION, SCORE_NAME, build_formal_recipe
from .run_planetoid_gate import (
    accuracy,
    atomic_write_json,
    build_model,
    canonical_dataset_name,
    checkpoint_gradients,
    parameter_schema_hash,
    parse_ints,
    reject_legacy_output_path,
    seed_everything,
    source_fingerprint,
    state_hash,
    tensor_hash,
    train_trajectory,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = canonical_data_root(REPO_ROOT)
SELECTION_ALGORITHM_VERSION = "proper-tracin-v1-topk"
SELECTION_PRODUCER_VERSION = "proper-tracin-selection-v1"


def parse_budgets(value: str) -> Tuple[int, ...]:
    budgets = parse_ints(value)
    if not budgets or any(item <= 0 for item in budgets):
        raise argparse.ArgumentTypeError(
            "budgets must be positive comma-separated integers"
        )
    return tuple(sorted(set(int(item) for item in budgets), reverse=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--score-store-root", type=Path, required=True)
    parser.add_argument("--selection-store-root", type=Path, required=True)
    parser.add_argument("--legacy-results-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--fail-if-producer-called", action="store_true")
    parser.add_argument("--dataset", type=canonical_dataset_name, default="Cora")
    parser.add_argument("--model", choices=("gcn", "gat"), default="gcn")
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--checkpoint-epochs", default="1,5,10,20,30")
    parser.add_argument("--hidden-channels", type=int, default=16)
    parser.add_argument("--gat-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--optimizer", choices=("sgd", "adam"), default="adam")
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--lr-milestones", default="50,80")
    parser.add_argument("--lr-gamma", type=float, default=0.5)
    parser.add_argument(
        "--parameter-scope",
        choices=("all_trainable", "last_layer"),
        default="all_trainable",
    )
    parser.add_argument("--budgets", type=parse_budgets, default=(14, 7, 3))
    parser.add_argument("--num-threads", type=int, default=1)
    return parser


def checkpoint_weight_schedule(
    checkpoint_steps: Sequence[int],
    *,
    initial_lr: float,
    milestones: Sequence[int],
    gamma: float,
) -> Tuple[Mapping[str, Any], ...]:
    """Return the update LR used before each end-of-epoch scheduler step."""

    result = []
    for step in checkpoint_steps:
        decays = sum(1 for milestone in milestones if int(milestone) < int(step))
        result.append(
            {
                "global_step": int(step),
                "weight": float(initial_lr) * (float(gamma) ** decays),
            }
        )
    return tuple(result)


def _split_hash(data: Any) -> str:
    return sha256_bytes(
        bytes.fromhex(tensor_hash(data.train_mask))
        + bytes.fromhex(tensor_hash(data.val_mask))
        + bytes.fromhex(tensor_hash(data.test_mask))
    )


def _numerics_profile(num_threads: int) -> Mapping[str, Any]:
    return {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_geometric": torch_geometric.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "byteorder": sys.byteorder,
        "torch_build_hash": sha256_bytes(
            torch.__config__.show().encode("utf-8")
        ),
        "execution_backend": "cpu",
        "dtype": "float32",
        "num_threads": int(num_threads),
        "deterministic_algorithms": True,
    }


def _require_absolute(path: Path, label: str) -> Path:
    supplied = path.expanduser()
    if not supplied.is_absolute() or ".." in supplied.parts:
        raise ValueError("{0} must be an explicit absolute path".format(label))
    return supplied.resolve(strict=False)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    checkpoint_epochs = parse_ints(args.checkpoint_epochs)
    milestones = parse_ints(args.lr_milestones)
    if (
        not checkpoint_epochs
        or tuple(sorted(set(checkpoint_epochs))) != checkpoint_epochs
        or checkpoint_epochs[0] <= 0
        or checkpoint_epochs[-1] != args.epochs
    ):
        raise ValueError(
            "checkpoint epochs must be unique, ascending, positive, and end at --epochs"
        )
    if args.epochs <= 0 or args.hidden_channels <= 0 or args.gat_heads <= 0:
        raise ValueError("epochs and model dimensions must be positive")
    if args.num_threads <= 0:
        raise ValueError("num_threads must be positive")
    if not 0 < args.lr_gamma <= 1:
        raise ValueError("lr_gamma must be in (0, 1]")

    repo = REPO_ROOT
    output = _require_absolute(args.output, "output")
    score_root = _require_absolute(args.score_store_root, "score-store-root")
    selection_root = _require_absolute(
        args.selection_store_root, "selection-store-root"
    )
    legacy_results_root = _require_absolute(
        args.legacy_results_root, "legacy-results-root"
    )
    dataset_source = resolve_planetoid_public_source(
        args.data_root,
        repository_root=repo,
        dataset=args.dataset,
    )
    reject_legacy_output_path(output, repo)
    for label, root in (
        ("score-store-root", score_root),
        ("selection-store-root", selection_root),
    ):
        for legacy_name in ("cache", "selection_cache", "score_cache"):
            legacy_root = (legacy_results_root / legacy_name).resolve(strict=False)
            try:
                root.relative_to(legacy_root)
            except ValueError:
                pass
            else:
                raise ValueError(
                    "{0} must not be inside Legacy {1}".format(label, legacy_name)
                )

    seed_everything(args.seed, args.num_threads)
    dataset = Planetoid(
        root=str(dataset_source.resolved_root),
        name=dataset_source.storage_name,
        transform=NormalizeFeatures(),
    )
    data = dataset[0].to(torch.device("cpu"))
    split_observation = validate_public_split(data, args.dataset)
    candidate_ids = data.train_mask.nonzero(as_tuple=False).view(-1)
    target_ids = data.val_mask.nonzero(as_tuple=False).view(-1)
    if set(candidate_ids.tolist()) & set(target_ids.tolist()):
        raise RuntimeError("candidate T and target E must be disjoint")
    if max(args.budgets) > int(candidate_ids.numel()):
        raise ValueError("largest budget exceeds candidate count")

    lr = args.lr if args.lr is not None else (
        0.1 if args.optimizer == "sgd" else 0.01
    )
    model = build_model(
        args.model,
        dataset.num_features,
        args.hidden_channels,
        dataset.num_classes,
        args.dropout,
        args.gat_heads,
    ).to(torch.device("cpu"))
    initial_state_hash = state_hash(
        {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}
    )
    schedule = checkpoint_weight_schedule(
        checkpoint_epochs,
        initial_lr=lr,
        milestones=milestones,
        gamma=args.lr_gamma,
    )
    numerics = _numerics_profile(args.num_threads)
    numerics_hash = sha256_bytes(
        json.dumps(numerics, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    source_hash = source_fingerprint(
        [
            Path(__file__).resolve(),
            Path(__file__).with_name("core.py"),
            Path(__file__).with_name("formal_recipe.py"),
            Path(__file__).with_name("run_planetoid_gate.py"),
            repo / "cache_v2" / "score_store.py",
            repo / "cache_v2" / "selection_materializer.py",
            repo / "experiments" / "selection_budget_planner.py",
            repo / "experiments" / "bc_target_v2" / "dataset_source.py",
        ]
    )
    recipe = build_formal_recipe(
        source_fingerprint=source_hash,
        data_identity={
            "dataset_adapter": "torch_geometric.datasets.Planetoid",
            "dataset_name": args.dataset,
            "split_policy": "public",
            "dataset_source_fingerprint": dataset_source.source_fingerprint,
            "transform_policy": "NormalizeFeatures",
            "edge_index_hash": tensor_hash(data.edge_index),
            "features_hash": tensor_hash(data.x),
            "labels_hash": tensor_hash(data.y),
            "split_hash": _split_hash(data),
        },
        candidate_ids_hash=ordered_ids_hash(candidate_ids.tolist()),
        target_ids_hash=ordered_ids_hash(target_ids.tolist()),
        target_profile="attack_safe_holdout",
        label_source="validation_true_labels",
        selector_model_input={
            "architecture": "two_layer_{0}".format(args.model),
            "hidden_channels": int(args.hidden_channels),
            "gat_heads": int(args.gat_heads) if args.model == "gat" else None,
            "dropout": float(args.dropout),
            "initial_state_hash": initial_state_hash,
            "parameter_schema_hash": parameter_schema_hash(
                model, args.parameter_scope
            ),
            "gradient_model_mode": "eval",
        },
        checkpoint_schedule=schedule,
        training={
            "epochs": int(args.epochs),
            "batch_policy": "full_batch_one_optimizer_step_per_epoch",
        },
        optimizer={
            "family": args.optimizer,
            "initial_lr": float(lr),
            "weight_decay": float(args.weight_decay),
            "lr_milestones": list(milestones),
            "lr_gamma": float(args.lr_gamma),
            "weight_policy": (
                "paper_lr"
                if args.optimizer == "sgd"
                else "adam_lr_weighted_gradient_heuristic"
            ),
        },
        loss={
            "family": "cross_entropy",
            "candidate_reduction": "single",
            "target_reduction": "mean",
            "training_reduction": "mean",
            "class_weights": None,
            "ignore_index": -100,
        },
        parameter_scope=args.parameter_scope,
        seed_bundle={
            "train": int(args.seed),
            "data": int(args.seed),
            "query": int(args.seed),
        },
        numerics_profile_hash=numerics_hash,
    )
    producer_version = ProducerVersion(
        semantic_version=ALGORITHM_VERSION,
        source_fingerprint=source_hash,
    )
    store = ScoreArtifactStore(
        score_root, producer_version=producer_version
    )

    legacy_before = snapshot_legacy_caches(legacy_results_root)

    def produce_score() -> ScorePayload:
        checkpoints, train_summary = train_trajectory(
            model,
            data,
            checkpoint_epochs,
            args.epochs,
            args.optimizer,
            lr,
            args.weight_decay,
            milestones,
            args.lr_gamma,
        )
        observed_schedule = tuple(
            {
                "global_step": int(item["global_step"]),
                "weight": float(item["update_lr"]),
            }
            for item in checkpoints
        )
        if observed_schedule != schedule:
            raise RuntimeError(
                "observed checkpoint weights do not match pre-compute Recipe"
            )
        candidate_trajectory = []
        target_trajectory = []
        for item in checkpoints:
            candidate_gradient, target_gradient = checkpoint_gradients(
                model,
                data,
                item["state"],
                candidate_ids,
                target_ids,
                args.parameter_scope,
            )
            candidate_trajectory.append(candidate_gradient)
            target_trajectory.append(target_gradient)
        score_values = tracin_cp_eval_scores(
            candidate_trajectory,
            target_trajectory,
            [float(item["weight"]) for item in schedule],
        )
        model.load_state_dict(checkpoints[-1]["state"])
        return ScorePayload.build(
            score_name=SCORE_NAME,
            candidate_nodes=candidate_ids.tolist(),
            scores=score_values.tolist(),
            output_provenance={
                "checkpoint_manifest": [
                    {
                        "global_step": int(item["global_step"]),
                        "state_hash": str(item["state_hash"]),
                        "weight": float(item["update_lr"]),
                    }
                    for item in checkpoints
                ],
                "final_state_hash": str(checkpoints[-1]["state_hash"]),
                "final_train_loss": float(train_summary["final_train_loss"]),
                "test_accuracy": accuracy(model, data, data.test_mask),
                "hostname": socket.gethostname(),
                "numerics": dict(numerics),
            },
        )

    score_result = store.get_or_compute(
        recipe,
        produce_score,
        fail_if_producer_called=args.fail_if_producer_called,
    )
    selection_dataset = make_dataset_selection_inputs(
        data,
        dataset_name=args.dataset,
        source_path=dataset_source.processed_data_path,
    )
    if (
        tuple(selection_dataset.candidate_nodes)
        != score_result.payload.candidate_nodes_ordered
    ):
        raise RuntimeError(
            "Score candidates do not match persisted Selection candidate set"
        )
    selection_source_hash = source_fingerprint(
        [
            Path(__file__).resolve(),
            repo / "experiments" / "selection_budget_planner.py",
            repo / "cache_v2" / "selection_materializer.py",
        ]
    )
    selection_result = materialize_budget_selection(
        store_root=selection_root,
        dataset=selection_dataset,
        strategy="proper_tracin",
        selector_seed=int(args.seed),
        budgets=args.budgets,
        producer_version=ProducerVersion(
            semantic_version=SELECTION_PRODUCER_VERSION,
            source_fingerprint=selection_source_hash,
        ),
        algorithm_version=SELECTION_ALGORITHM_VERSION,
        parameters={
            "prefix_stable": True,
            "score_name": SCORE_NAME,
            "ranking": "score_desc_node_id_asc",
            "score_algorithm_version": ALGORITHM_VERSION,
        },
        source_score_artifact_id=score_result.artifact_id,
        producer=lambda max_k: score_result.payload.ranking[:max_k],
        fail_if_producer_called=args.fail_if_producer_called,
    )

    legacy_after = snapshot_legacy_caches(legacy_results_root)
    legacy_unchanged = legacy_before == legacy_after
    if not legacy_unchanged:
        raise RuntimeError("Legacy cache snapshot changed during formal gate")

    result: Dict[str, Any] = {
        "schema": "proper-tracin-v1.formal-selection-gate",
        "version": 1,
        "status": "passed-selection-only",
        "formal_score_artifact": True,
        "default_runner_registered": False,
        "gu_canary_run": False,
        "hybrid_gate_run": False,
        "algorithm_version": ALGORITHM_VERSION,
        "recipe_hash": recipe.recipe_hash,
        "recipe": recipe.to_dict(),
        "dataset": {
            "name": args.dataset,
            "num_nodes": int(data.num_nodes),
            "num_candidates": int(candidate_ids.numel()),
            "num_targets": int(target_ids.numel()),
            "split_policy": "public",
            "source": dataset_source.to_manifest(),
            "split_observation": split_observation,
        },
        "score_artifact": {
            "store_root": str(score_root),
            "hit": bool(score_result.hit),
            "outcome": score_result.outcome,
            "producer_called": bool(score_result.producer_called),
            "artifact_id": score_result.artifact_id,
            "recipe_hash": recipe.recipe_hash,
            "content_hash": score_result.content_hash,
            "semantic_path": score_result.semantic_path,
            "output_provenance": dict(score_result.payload.output_provenance),
        },
        "selection": selection_result.to_manifest(selection_root),
        "legacy_cache": {
            "unchanged": legacy_unchanged,
            "before": legacy_before,
            "after": legacy_after,
        },
        "provenance": {
            "hostname": socket.gethostname(),
            "source_fingerprint": source_hash,
            "numerics": dict(numerics),
        },
    }
    atomic_write_json(output, result, args.overwrite)
    print(
        json.dumps(
            {
                "output": str(output),
                "status": result["status"],
                "score_artifact_id": score_result.artifact_id,
                "score_hit": score_result.hit,
                "score_producer_called": score_result.producer_called,
                "selection_artifact_id": selection_result.result.artifact_id,
                "selection_hit": selection_result.cache_hit,
                "selection_producer_called": selection_result.producer_called,
                "budgets": list(selection_result.budgets_descending),
                "legacy_unchanged": legacy_unchanged,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
