"""Run the cache-backed Planetoid/GCN C-target GIF/TracIn experiment on CPU.

The experiment intentionally does not perform exact retraining.  Its operational
reference is the graph-aware first-order GIF source term evaluated against one
shared LiSSA approximation of ``H^-1 g_E``.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

import numpy as np
import torch
import torch_geometric
from torch import Tensor
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

from cache_v2 import ProducerVersion
from experiments.bc_target_v2.dataset_source import (
    canonical_data_root,
    resolve_planetoid_public_source,
    validate_public_split,
)

from .core import (
    GateGCN,
    checkpoint_point_gradients,
    deployed_cross_gradient_scores,
    graph_source_scores,
    ids_hash,
    inverse_hessian_target,
    pair_metrics,
    parameter_schema_hash,
    seed_everything,
    source_fingerprint,
    stable_ranking,
    state_hash,
    tensor_hash,
    tracin_cp_eval_scores,
    train_trajectory,
)
from .recipe import ALGORITHM_VERSION, SCORE_NAMES, build_recipe
from .score_store import ScoreBundlePayload, ScoreBundleStore


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = canonical_data_root(REPO_ROOT)
DEFAULT_CACHE_ROOT = REPO_ROOT / "results" / "cache_v2" / "c_target_v1"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "results" / "c_target_v1"


def _int_list(value: str) -> Sequence[int]:
    try:
        result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected comma-separated positive integers")
    if tuple(sorted(set(result))) != result:
        raise argparse.ArgumentTypeError("values must be unique and strictly increasing")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument(
        "--dataset",
        choices=("Cora", "CiteSeer", "PubMed"),
        default="Cora",
        help="Planetoid dataset; the accepted v1 run uses Cora",
    )
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--num-threads", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument(
        "--checkpoint-epochs",
        type=_int_list,
        default=(1, 10, 25, 50, 100, 200),
    )
    parser.add_argument("--hidden-channels", type=int, default=16)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--optimizer", choices=("sgd", "adam"), default="adam")
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--milestones", type=_int_list, default=(100, 150))
    parser.add_argument("--gamma", type=float, default=0.5)
    parser.add_argument("--parameter-scope", choices=("all_trainable", "last_layer"), default="all_trainable")
    parser.add_argument("--affected-hops", type=int, default=2)
    parser.add_argument("--candidate-limit", type=int, default=0)
    parser.add_argument("--topk-ratio", type=float, default=0.05)
    parser.add_argument("--lissa-iterations", type=int, default=20)
    parser.add_argument("--lissa-scale", type=float, default=25.0)
    parser.add_argument("--lissa-damp", type=float, default=0.01)
    parser.add_argument("--fail-if-producer-called", action="store_true")
    parser.add_argument("--overwrite-output", action="store_true")
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.seed < 0 or args.num_threads <= 0 or args.epochs <= 0:
        raise ValueError("seed, thread count, and epochs are invalid")
    if args.checkpoint_epochs[-1] != args.epochs:
        raise ValueError("the final checkpoint epoch must equal --epochs")
    if args.hidden_channels <= 0 or not 0 <= args.dropout < 1:
        raise ValueError("hidden channels or dropout is invalid")
    if args.lr <= 0 or args.weight_decay < 0 or not 0 < args.gamma <= 1:
        raise ValueError("optimizer settings are invalid")
    if args.affected_hops < 0 or args.candidate_limit < 0:
        raise ValueError("affected hops and candidate limit must be non-negative")
    if not 0 < args.topk_ratio <= 1:
        raise ValueError("top-k ratio must be in (0, 1]")


def _accuracy(model: GateGCN, data, mask: Tensor) -> float:
    model.eval()
    with torch.no_grad():
        prediction = model(data.x, data.edge_index).argmax(dim=-1)
    return float((prediction[mask] == data.y[mask]).float().mean().item())


def _score_stats(values: Sequence[float]) -> Dict[str, float]:
    array = np.asarray(values, dtype=np.float64)
    return {
        "min": float(array.min()),
        "max": float(array.max()),
        "mean": float(array.mean()),
        "std": float(array.std()),
        "l2_norm": float(np.linalg.norm(array)),
    }


def _write_json_atomic(path: Path, value: Mapping[str, Any], overwrite: bool) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError("output already exists: {0}".format(path))
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8")
    temporary = path.with_name(path.name + ".tmp-{0}".format(os.getpid()))
    temporary.write_bytes(payload)
    os.replace(str(temporary), str(path))


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    _validate_args(args)
    run_started = time.perf_counter()
    dataset_source = resolve_planetoid_public_source(
        args.data_root,
        repository_root=REPO_ROOT,
        dataset=args.dataset,
    )
    seed_everything(args.seed, args.num_threads)
    device = torch.device("cpu")

    load_started = time.perf_counter()
    dataset = Planetoid(
        root=str(dataset_source.resolved_root),
        name=dataset_source.storage_name,
        transform=NormalizeFeatures(),
    )
    data = dataset[0].to(device)
    split_observation = validate_public_split(data, args.dataset)
    load_seconds = time.perf_counter() - load_started

    candidate_ids = torch.where(data.train_mask)[0].sort().values
    if args.candidate_limit:
        candidate_ids = candidate_ids[: args.candidate_limit]
    if candidate_ids.numel() == 0:
        raise ValueError("candidate set is empty")
    target_ids = torch.where(data.val_mask)[0].sort().values
    hessian_train_ids = torch.where(data.train_mask)[0].sort().values

    model = GateGCN(
        int(dataset.num_features),
        int(args.hidden_channels),
        int(dataset.num_classes),
        float(args.dropout),
    ).to(device)
    checkpoints, training_observation = train_trajectory(
        model,
        data,
        checkpoint_epochs=args.checkpoint_epochs,
        epochs=args.epochs,
        lr=args.lr,
        weight_decay=args.weight_decay,
        milestones=args.milestones,
        gamma=args.gamma,
        optimizer_name=args.optimizer,
    )
    final_state = checkpoints[-1]["state"]
    model.load_state_dict(final_state)

    source_paths = (
        Path(__file__).resolve(),
        Path(__file__).with_name("__init__.py"),
        Path(__file__).with_name("core.py"),
        Path(__file__).with_name("recipe.py"),
        Path(__file__).with_name("score_store.py"),
        REPO_ROOT / "experiments" / "bc_target_v2" / "dataset_source.py",
    )
    code_fingerprint = source_fingerprint(source_paths)
    split_tensor = torch.stack(
        [
            data.train_mask.to(torch.uint8),
            data.val_mask.to(torch.uint8),
            data.test_mask.to(torch.uint8),
        ]
    )
    checkpoint_manifest = [
        {
            "global_step": int(item["global_step"]),
            "state_hash": str(item["state_hash"]),
            "weight": float(item["update_lr"]),
        }
        for item in checkpoints
    ]
    recipe = build_recipe(
        source_fingerprint=code_fingerprint,
        data_identity={
            "dataset": args.dataset,
            "dataset_family": "Planetoid",
            "dataset_source_fingerprint": dataset_source.source_fingerprint,
            "edge_index_hash": tensor_hash(data.edge_index),
            "features_hash": tensor_hash(data.x),
            "labels_hash": tensor_hash(data.y),
            "split_hash": tensor_hash(split_tensor),
            "num_nodes": int(data.num_nodes),
            "num_edges_directed": int(data.edge_index.shape[1]),
            "feature_transform": "torch_geometric.transforms.NormalizeFeatures",
        },
        candidate_ids_hash=ids_hash(candidate_ids),
        target_ids_hash=ids_hash(target_ids),
        selector_model={
            "architecture": "GateGCN",
            "layers": 2,
            "hidden_channels": int(args.hidden_channels),
            "dropout": float(args.dropout),
            "final_state_hash": state_hash(final_state),
            "parameter_schema_hash": parameter_schema_hash(model, args.parameter_scope),
        },
        training={
            "epochs": int(args.epochs),
            "optimizer": str(args.optimizer).upper(),
            "lr": float(args.lr),
            "weight_decay": float(args.weight_decay),
            "scheduler": "MultiStepLR",
            "milestones": list(args.milestones),
            "gamma": float(args.gamma),
            "train_loss_reduction": "mean",
        },
        checkpoints=checkpoint_manifest,
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "affected_set": "candidate_plus_undirected_k_hop_neighbors",
            "affected_hops": int(args.affected_hops),
            "grad1": "sum_ce_original_graph_affected_set",
            "grad2": "sum_ce_deleted_graph_affected_neighbors_excluding_candidate",
            "exact_retrain": False,
        },
        hessian={
            "method": "LiSSA_full_train_mean_ce",
            "iterations": int(args.lissa_iterations),
            "scale": float(args.lissa_scale),
            "damp": float(args.lissa_damp),
            "shared_solve": "H^-1_g_E_once",
        },
        loss={
            "type": "cross_entropy",
            "target_set": "validation_mask",
            "target_reduction": "mean",
            "graph_source_reduction": "sum",
        },
        parameter_scope=args.parameter_scope,
        seed_bundle={
            "python_numpy_torch": int(args.seed),
            "deterministic_algorithms": True,
        },
        numerics={
            "torch_dtype": str(data.x.dtype),
            "deterministic_algorithms": True,
        },
    )

    def produce() -> ScoreBundlePayload:
        scoring_started = time.perf_counter()
        candidate_gradients = []
        target_gradients = []
        checkpoint_gradient_seconds = []
        for item in checkpoints:
            checkpoint_started = time.perf_counter()
            matrix, target = checkpoint_point_gradients(
                model,
                data,
                state=item["state"],
                candidate_ids=candidate_ids,
                target_ids=target_ids,
                parameter_scope=args.parameter_scope,
            )
            candidate_gradients.append(matrix)
            target_gradients.append(target)
            checkpoint_gradient_seconds.append(
                time.perf_counter() - checkpoint_started
            )

        final_candidate_gradient = candidate_gradients[-1]
        final_checkpoint_target = target_gradients[-1]
        target_gradient, inverse_target, ihvp_observation = inverse_hessian_target(
            model,
            data,
            state=final_state,
            hessian_train_ids=hessian_train_ids,
            target_ids=target_ids,
            parameter_scope=args.parameter_scope,
            iterations=args.lissa_iterations,
            scale=args.lissa_scale,
            damp=args.lissa_damp,
        )
        target_gradient_max_abs_diff = float(
            (target_gradient - final_checkpoint_target).abs().max().item()
        )
        if target_gradient_max_abs_diff > 1e-6:
            raise RuntimeError("final target gradient mismatch across shared computations")

        graph_scores, graph_observation = graph_source_scores(
            model,
            data,
            state=final_state,
            candidate_ids=candidate_ids,
            parameter_scope=args.parameter_scope,
            affected_hops=args.affected_hops,
            target_gradient=target_gradient,
            inverse_target=inverse_target,
        )
        scores = dict(graph_scores)
        scores.update(
            {
                "r_point": final_candidate_gradient.mv(inverse_target).to(torch.float64),
                "p_point": final_candidate_gradient.mv(target_gradient).to(torch.float64),
                "tracin_cp_point": tracin_cp_eval_scores(
                    candidate_gradients,
                    target_gradients,
                    [float(item["update_lr"]) for item in checkpoints],
                ).to(torch.float64),
                "legacy": deployed_cross_gradient_scores(
                    final_candidate_gradient
                ).to(torch.float64),
            }
        )
        if set(scores) != set(SCORE_NAMES):
            raise RuntimeError("runner score set does not match the frozen Recipe")

        candidate_list = [int(value) for value in candidate_ids.tolist()]
        score_lists = {
            name: [float(value) for value in scores[name].tolist()]
            for name in sorted(scores)
        }
        rankings = {
            name: list(stable_ranking(candidate_list, scores[name]))
            for name in sorted(scores)
        }
        metadata = {
            "experiment": "c_target_v1",
            "dataset": args.dataset,
            "model": "GCN",
            "seed": int(args.seed),
            "candidate_count": len(candidate_list),
            "target_count": int(target_ids.numel()),
            "train_count_for_hessian": int(hessian_train_ids.numel()),
            "checkpoint_gradient_seconds": checkpoint_gradient_seconds,
            "checkpoint_steps": [int(item["global_step"]) for item in checkpoints],
            "checkpoint_weights": [float(item["update_lr"]) for item in checkpoints],
            "target_gradient_max_abs_diff": target_gradient_max_abs_diff,
            "ihvp": ihvp_observation,
            "graph_source": graph_observation,
            "final_accuracy": {
                "train": _accuracy(model, data, data.train_mask),
                "validation": _accuracy(model, data, data.val_mask),
                "test_diagnostic_only": _accuracy(model, data, data.test_mask),
            },
            "score_compute_seconds": time.perf_counter() - scoring_started,
            "exact_retrain_performed": False,
        }
        return ScoreBundlePayload.build(
            candidate_list,
            score_lists,
            rankings,
            metadata,
        )

    store = ScoreBundleStore(
        args.cache_root.expanduser().resolve(),
        producer_version=ProducerVersion(
            semantic_version=ALGORITHM_VERSION,
            source_fingerprint=code_fingerprint,
        ),
    )
    result = store.get_or_compute(
        recipe,
        produce,
        fail_if_called=args.fail_if_producer_called,
    )
    payload = result.payload
    candidate_count = len(payload.candidate_nodes_ordered)
    k = max(1, int(math.floor(candidate_count * args.topk_ratio)))
    metrics: Dict[str, Dict[str, Mapping[str, Any]]] = {}
    for reference in ("gt_full", "gt_simple", "r_point"):
        metrics[reference] = {}
        for name in sorted(payload.scores):
            if name == reference:
                continue
            metrics[reference][name] = pair_metrics(
                payload.scores[reference],
                payload.scores[name],
                payload.rankings[reference],
                payload.rankings[name],
                k,
            )

    output_path = args.output
    if output_path is None:
        output_path = DEFAULT_OUTPUT_ROOT / (
            "{0}_gcn_seed{1}_n{2}.json".format(
                args.dataset.lower(), args.seed, candidate_count
            )
        )
    output_path = output_path.expanduser().resolve()
    summary = {
        "schema": "c_target_v1.run_summary",
        "version": 1,
        "algorithm_version": ALGORITHM_VERSION,
        "dataset": args.dataset,
        "dataset_source": dataset_source.to_manifest(),
        "split_observation": split_observation,
        "model": "GCN",
        "device": "cpu",
        "seed": int(args.seed),
        "candidate_count": candidate_count,
        "target_set": "validation_mask_mean_ce",
        "target_count": int(target_ids.numel()),
        "topk_ratio": float(args.topk_ratio),
        "topk": k,
        "exact_retrain_performed": False,
        "cache": {
            "root": str(store.root),
            "hit": bool(result.hit),
            "outcome": result.outcome,
            "producer_called": bool(result.producer_called),
            "producer_call_count": int(store.producer_call_count),
            "miss_reasons": list(result.miss_reasons),
            "artifact_id": result.artifact_id,
            "recipe_hash": recipe.recipe_hash,
            "content_hash": result.content_hash,
            "semantic_path": result.semantic_path,
            "payload_path": str(store.root.joinpath(*result.semantic_path.split("/"))),
        },
        "metrics": metrics,
        "score_stats": {
            name: _score_stats(payload.scores[name])
            for name in sorted(payload.scores)
        },
        "scores": {
            name: list(payload.scores[name]) for name in sorted(payload.scores)
        },
        "rankings": {
            name: list(payload.rankings[name]) for name in sorted(payload.rankings)
        },
        "persisted_metadata": dict(payload.metadata),
        "training_observation": training_observation,
        "runtime": {
            "data_load_seconds": load_seconds,
            "total_seconds": time.perf_counter() - run_started,
        },
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_geometric": torch_geometric.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "config": {
            "data_root_requested": str(args.data_root),
            "data_root": str(dataset_source.resolved_root),
            "dataset": args.dataset,
            "cache_root": str(store.root),
            "epochs": int(args.epochs),
            "checkpoint_epochs": list(args.checkpoint_epochs),
            "hidden_channels": int(args.hidden_channels),
            "dropout": float(args.dropout),
            "optimizer": args.optimizer,
            "lr": float(args.lr),
            "weight_decay": float(args.weight_decay),
            "milestones": list(args.milestones),
            "gamma": float(args.gamma),
            "parameter_scope": args.parameter_scope,
            "affected_hops": int(args.affected_hops),
            "candidate_limit": int(args.candidate_limit),
            "lissa_iterations": int(args.lissa_iterations),
            "lissa_scale": float(args.lissa_scale),
            "lissa_damp": float(args.lissa_damp),
            "num_threads": int(args.num_threads),
        },
    }
    _write_json_atomic(output_path, summary, args.overwrite_output)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "cache_hit": result.hit,
                "artifact_id": result.artifact_id,
                "recipe_hash": recipe.recipe_hash,
                "candidate_count": candidate_count,
                "topk": k,
                "gt_full_vs_p_graph": metrics["gt_full"]["p_graph"],
                "gt_full_vs_tracin_cp_point": metrics["gt_full"]["tracin_cp_point"],
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
