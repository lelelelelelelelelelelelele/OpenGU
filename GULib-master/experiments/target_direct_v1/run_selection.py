"""Produce 17 white-box selections from the exact OpenGU GNNDelete target."""

from __future__ import annotations

import argparse
import itertools
import json
import os
import platform
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np
import torch
import torch_geometric

from cache_v2 import ProducerVersion
from cache_v2.index import CacheIndex
from experiments.bc_target_v2.core import (
    checkpoint_view_indices,
    degree_scores,
    deterministic_random_scores,
    hutchinson_parameter_change_scores,
    inverse_hessian_vectors,
    weighted_checkpoint_scores,
)
from experiments.bc_target_v2.run_selection import _checkpoint_graph_scores
from experiments.c_target_v1.core import (
    checkpoint_point_gradients,
    deployed_cross_gradient_scores,
    ids_hash,
    inverse_hessian_target,
    pair_metrics,
    parameter_schema_hash,
    source_fingerprint,
    stable_ranking,
    tensor_hash,
)
from experiments.c_target_v1.score_store import (
    ScoreBundlePayload,
    ScoreBundleStore,
)
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1 import PROFILE
from experiments.target_direct_v1.recipe import (
    ALGORITHM_VERSION,
    APPROVED_BUDGET_RATIOS,
    SCORE_BUDGET_SEMANTICS,
    SCORE_FAMILY,
    SCORE_NAMES,
    build_recipe,
)
from experiments.target_direct_v1.split_profile import verify_profile
from utils.target_checkpoint import (
    capture_state,
    data_identity,
    load_target_checkpoint,
    save_target_checkpoint,
    state_hash,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SELECTION_PRODUCER_VERSION = "target-direct-selection-prefix-v2"
SELECTION_ALGORITHM_VERSION = "target-direct-score-desc-prefix-v2"


def _int_list(value: str) -> Tuple[int, ...]:
    result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset", choices=("Cora", "CiteSeer", "PubMed"), required=True
    )
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--selection-cache-root", type=Path, required=True)
    parser.add_argument("--checkpoint-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--ratio", type=float, required=True)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num-threads", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument(
        "--checkpoint-epochs",
        type=_int_list,
        default=(1, 10, 25, 50, 75, 100),
    )
    parser.add_argument("--gcn-num-layers", type=int, default=2)
    parser.add_argument("--gcn-hidden", type=int, default=64)
    parser.add_argument(
        "--parameter-scope",
        choices=("last_layer", "all_trainable"),
        default="last_layer",
    )
    parser.add_argument("--affected-hops", type=int, default=2)
    parser.add_argument("--lissa-iterations", type=int, default=20)
    parser.add_argument("--lissa-scale", type=float, default=25.0)
    parser.add_argument("--lissa-damp", type=float, default=0.01)
    parser.add_argument("--hutch-probes", type=int, default=32)
    parser.add_argument("--hutch-seed", type=int, default=1729)
    parser.add_argument("--reuse-checkpoint", action="store_true")
    parser.add_argument("--fail-if-score-producer-called", action="store_true")
    parser.add_argument("--fail-if-producer-called", action="store_true")
    parser.add_argument("--overwrite-output", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--experiment-git-sha", default=None)
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.seed < 0 or args.num_threads <= 0 or args.epochs <= 0:
        raise ValueError("seed, thread count, and epochs must be positive")
    if not any(
        abs(float(args.ratio) - approved) < 1e-12
        for approved in APPROVED_BUDGET_RATIOS
    ):
        raise ValueError(
            "formal ratio must be one of {0}".format(
                list(APPROVED_BUDGET_RATIOS)
            )
        )
    if args.checkpoint_epochs[-1] != args.epochs:
        raise ValueError("final checkpoint epoch must equal epochs")
    if len(args.checkpoint_epochs) < 3:
        raise ValueError("at least three checkpoints are required")
    if tuple(sorted(set(args.checkpoint_epochs))) != tuple(args.checkpoint_epochs):
        raise ValueError("checkpoint epochs must be unique and increasing")
    if args.gcn_num_layers != 2:
        raise ValueError("target_direct_v1 currently freezes a two-layer OpenGU GCN")
    if args.gcn_hidden <= 0:
        raise ValueError("gcn_hidden must be positive")
    for path, label in (
        (args.processed_root, "processed_root"),
        (args.runtime_root, "runtime_root"),
        (args.cache_root, "cache_root"),
        (args.selection_cache_root, "selection_cache_root"),
    ):
        if not Path(path).expanduser().is_absolute():
            raise ValueError("{0} must be absolute".format(label))
    cache_root = Path(args.cache_root).expanduser().resolve()
    selection_cache_root = Path(args.selection_cache_root).expanduser().resolve()
    if cache_root != selection_cache_root:
        raise ValueError(
            "cache_root and selection_cache_root must resolve to the same canonical Cache V2 root"
        )


def _git_provenance(expected_sha: str | None, allow_dirty: bool) -> Dict[str, Any]:
    def run(*arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout.strip()

    head = run("rev-parse", "HEAD").lower()
    status = run("status", "--short")
    if expected_sha is not None and head != str(expected_sha).lower():
        raise RuntimeError(
            "experiment Git HEAD mismatch: observed {0}, expected {1}".format(
                head, expected_sha
            )
        )
    if status and not allow_dirty:
        raise RuntimeError("formal target-direct selection requires a clean worktree")
    return {
        "head": head,
        "expected_head": expected_sha,
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "worktree_dirty": bool(status),
        "status_short": status.splitlines() if status else [],
    }


def _seed_everything(seed: int, num_threads: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(num_threads)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _synchronize(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def _gpu_peaks(device: torch.device) -> Dict[str, Any]:
    if device.type != "cuda":
        return {
            "available": False,
            "device": str(device),
            "peak_allocated_bytes": None,
            "peak_reserved_bytes": None,
        }
    _synchronize(device)
    return {
        "available": True,
        "device": str(device),
        "device_name": torch.cuda.get_device_name(device),
        "peak_allocated_bytes": int(torch.cuda.max_memory_allocated(device)),
        "peak_reserved_bytes": int(torch.cuda.max_memory_reserved(device)),
    }


def _atomic_json(path: Path, value: Mapping[str, Any], overwrite: bool) -> None:
    target = Path(path).expanduser().resolve()
    if target.exists() and not overwrite:
        raise FileExistsError("output already exists: {0}".format(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp-{0}".format(os.getpid()))
    try:
        temporary.write_text(
            json.dumps(
                value,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()


def _parameter_argv(args: argparse.Namespace, expected_k: int) -> Sequence[str]:
    return [
        str(Path(__file__).resolve()),
        "--root_path",
        str(REPO_ROOT),
        "--runtime_root",
        str(args.runtime_root.expanduser().resolve()),
        "--processed_root",
        str(args.processed_root.expanduser().resolve()),
        "--processed_profile",
        PROFILE,
        "--dataset_name",
        args.dataset.lower(),
        "--base_model",
        "GCN",
        "--unlearning_methods",
        "GNNDelete",
        "--train_ratio",
        "0.7",
        "--val_ratio",
        "0.1",
        "--test_ratio",
        "0.2",
        "--unlearn_ratio",
        str(args.ratio),
        "--proportion_unlearned_nodes",
        str(args.ratio),
        "--formal_expected_k",
        str(expected_k),
        "--formal_fail_closed",
        "--num_epochs",
        str(args.epochs),
        "--num_threads",
        str(args.num_threads),
        "--random_seed",
        str(args.seed),
        "--cuda",
        str(args.cuda),
        "--gcn_num_layers",
        str(args.gcn_num_layers),
        "--gcn_hidden",
        str(args.gcn_hidden),
    ]


def _prepare_target(
    args: argparse.Namespace,
    *,
    candidate_count: int,
    expected_k: int,
    expected_data_identity: Mapping[str, Any],
) -> Tuple[Any, Any, Sequence[Mapping[str, Any]], Dict[str, Any], Dict[str, Any]]:
    sys.argv = list(_parameter_argv(args, expected_k))
    from parameter_parser import parameter_parser
    from attack.pipeline_adapter import AttackPipeline

    runtime_args = parameter_parser()
    runtime_args["seed"] = int(args.seed)
    runtime_args["target_direct_checkpoint_epochs"] = tuple(
        int(value) for value in args.checkpoint_epochs
    )
    pipeline = AttackPipeline(runtime_args)
    observed_identity = data_identity(pipeline.data)
    if observed_identity != dict(expected_data_identity):
        raise RuntimeError(
            "OpenGU runtime data differs from verified target-direct profile"
        )

    checkpoint_path = args.checkpoint_path.expanduser().resolve()
    training_started = time.perf_counter()
    if args.reuse_checkpoint:
        checkpoint = load_target_checkpoint(
            checkpoint_path,
            expected_metadata={
                "dataset_name": args.dataset.lower(),
                "base_model": "GCN",
                "seed": int(args.seed),
                "processed_profile": PROFILE,
                "num_epochs": int(args.epochs),
                "gcn_num_layers": int(args.gcn_num_layers),
                "gcn_hidden": int(args.gcn_hidden),
            },
            map_location="cpu",
        )
        if checkpoint["metadata"].get("data_identity") != observed_identity:
            raise RuntimeError("reused target checkpoint data identity mismatch")
        pipeline.method.determine_target_model()
        model = pipeline.method.target_model.model
        model.load_state_dict(checkpoint["state_dict"], strict=True)
        checkpoints = checkpoint["checkpoints"]
        training_observation = {
            "mode": "reused_checkpoint",
            "seconds": time.perf_counter() - training_started,
        }
        checkpoint_manifest = {
            "path": checkpoint["path"],
            "file_sha256": checkpoint["file_sha256"],
            "state_hash": checkpoint["state_hash"],
            "checkpoint_count": len(checkpoints),
            "metadata": dict(checkpoint["metadata"]),
        }
    else:
        pipeline.args["train_only"] = True
        pipeline.args["num_runs"] = 1
        pipeline.method.run_exp()
        model = pipeline._get_trained_model()
        checkpoints = tuple(
            getattr(pipeline.method.target_model, "target_direct_checkpoints", ())
        )
        final_state = capture_state(model)
        metadata = {
            "dataset_name": args.dataset.lower(),
            "base_model": "GCN",
            "seed": int(args.seed),
            "processed_profile": PROFILE,
            "num_epochs": int(args.epochs),
            "gcn_num_layers": int(args.gcn_num_layers),
            "gcn_hidden": int(args.gcn_hidden),
            "data_identity": observed_identity,
            "candidate_identity": {
                "denominator": "train_candidate_count",
                "candidate_count": int(candidate_count),
                "deletion_budget_conditioned": False,
            },
        }
        checkpoint_manifest = save_target_checkpoint(
            checkpoint_path,
            state_dict=final_state,
            metadata=metadata,
            checkpoints=checkpoints,
            overwrite=args.overwrite_output,
        )
        training_observation = {
            "mode": "cold_training",
            "seconds": time.perf_counter() - training_started,
            "test_f1_observed_after_training": float(
                pipeline.method.poison_f1[0]
            ),
        }
    model = model.to(pipeline.device)
    model.load_state_dict(checkpoints[-1]["state"], strict=True)
    if state_hash(model.state_dict()) != checkpoint_manifest["state_hash"]:
        raise RuntimeError("prepared model differs from target checkpoint")
    return (
        pipeline,
        model,
        checkpoints,
        checkpoint_manifest,
        training_observation,
    )


def _pair_metrics(
    payload: ScoreBundlePayload, budget: int
) -> Dict[str, Mapping[str, Any]]:
    result = {}
    for left, right in itertools.combinations(sorted(payload.scores), 2):
        result["{0}__{1}".format(left, right)] = pair_metrics(
            payload.scores[left],
            payload.scores[right],
            payload.rankings[left],
            payload.rankings[right],
            int(budget),
        )
    return result


def selection_recipe_parameters(
    *,
    name: str,
    ratio: float,
    expected_k: int,
    target_checkpoint_state_hash: str,
) -> Dict[str, Any]:
    if name not in SCORE_NAMES:
        raise ValueError("unknown target-direct score name")
    if not any(
        abs(float(ratio) - approved) < 1e-12
        for approved in APPROVED_BUDGET_RATIOS
    ):
        raise ValueError("unapproved target-direct budget ratio")
    if int(expected_k) <= 0:
        raise ValueError("expected_k must be positive")
    return {
        "prefix_stable": True,
        "requested_ratio": float(ratio),
        "budget_denominator": "train_candidate_count",
        "budget_rounding": "floor_with_minimum_one",
        "expected_k": int(expected_k),
        "score_name": name,
        "score_family": SCORE_FAMILY,
        "target_checkpoint_state_hash": target_checkpoint_state_hash,
        "orientation": "score_desc_more_influential_or_harmful_if_removed",
    }


def run(args: argparse.Namespace) -> Dict[str, Any]:
    _validate_args(args)
    run_started = time.perf_counter()
    git_provenance = _git_provenance(
        args.experiment_git_sha, args.allow_dirty
    )
    profile = verify_profile(
        repository_root=REPO_ROOT,
        processed_root=args.processed_root,
        dataset=args.dataset,
    )
    candidate_count = int(profile["inputs"].candidate_count)
    expected_k = max(1, int(candidate_count * float(args.ratio)))
    _seed_everything(args.seed, args.num_threads)
    if not torch.cuda.is_available():
        raise RuntimeError("target-direct formal selection requires CUDA")
    torch.cuda.set_device(args.cuda)
    device = torch.device("cuda", args.cuda)
    torch.cuda.reset_peak_memory_stats(device)

    pipeline, model, checkpoints, target_checkpoint, training_observation = (
        _prepare_target(
            args,
            candidate_count=candidate_count,
            expected_k=expected_k,
            expected_data_identity=data_identity(profile["data"]),
        )
    )
    data = pipeline.data.to(device)
    candidate_ids = torch.where(data.train_mask)[0].sort().values
    target_ids = torch.where(data.val_mask)[0].sort().values
    if int(candidate_ids.numel()) != candidate_count:
        raise RuntimeError("candidate count changed after target preparation")
    if int(target_ids.numel()) <= 0:
        raise RuntimeError("validation target set is empty")
    views = checkpoint_view_indices(len(checkpoints))
    final_state = checkpoints[-1]["state"]
    checkpoint_manifest = [
        {
            "global_step": int(item["global_step"]),
            "state_hash": str(item["state_hash"]),
            "weight": float(item["update_lr"]),
        }
        for item in checkpoints
    ]
    source_paths = (
        Path(__file__).resolve(),
        Path(__file__).with_name("recipe.py"),
        Path(__file__).with_name("split_profile.py"),
        REPO_ROOT / "utils" / "node_split.py",
        REPO_ROOT / "experiments" / "bc_target_v2" / "run_selection.py",
        REPO_ROOT / "experiments" / "bc_target_v2" / "core.py",
        REPO_ROOT / "experiments" / "c_target_v1" / "core.py",
        REPO_ROOT / "experiments" / "c_target_v1" / "score_store.py",
        REPO_ROOT / "utils" / "target_checkpoint.py",
    )
    code_fingerprint = source_fingerprint(source_paths)
    split_tensor = torch.stack(
        [
            data.train_mask.to(torch.uint8),
            data.val_mask.to(torch.uint8),
            data.test_mask.to(torch.uint8),
        ]
    )
    model_config = getattr(model, "config", None)
    model_lr = float(getattr(model_config, "lr", 0.01))
    model_decay = float(getattr(model_config, "decay", 5e-4))
    random_seed = int(args.seed) + 100003
    recipe = build_recipe(
        source_fingerprint=code_fingerprint,
        data_identity={
            "dataset": args.dataset,
            "dataset_family": "Planetoid",
            "dataset_adapter": "OpenGU persisted processed pair",
            "split_policy": PROFILE,
            "dataset_source_fingerprint": profile["manifest"][
                "dataset_source"
            ]["source_fingerprint"],
            "processed_data_sha256": profile["manifest"]["data_sha256"],
            "edge_index_hash": tensor_hash(data.edge_index),
            "features_hash": tensor_hash(data.x),
            "labels_hash": tensor_hash(data.y),
            "split_hash": tensor_hash(split_tensor),
            "num_nodes": int(data.num_nodes),
            "num_edges_directed": int(data.edge_index.shape[1]),
        },
        candidate_ids_hash=ids_hash(candidate_ids),
        target_ids_hash=ids_hash(target_ids),
        selector_model={
            "architecture": "OpenGU.GCNNet",
            "layers": int(args.gcn_num_layers),
            "hidden_channels": int(args.gcn_hidden),
            "dropout": 0.5,
            "final_state_hash": target_checkpoint["state_hash"],
            "parameter_schema_hash": parameter_schema_hash(
                model, args.parameter_scope
            ),
        },
        training={
            "epochs": int(args.epochs),
            "optimizer": "Adam",
            "lr": model_lr,
            "weight_decay": model_decay,
            "scheduler": "none",
            "train_loss_reduction": "mean",
        },
        checkpoints=checkpoint_manifest,
        checkpoint_views=views,
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "affected_set": "candidate_plus_undirected_k_hop_neighbors",
            "affected_hops": int(args.affected_hops),
            "per_candidate_exact_retrain": False,
        },
        hessian={
            "method": "LiSSA_full_train_mean_ce",
            "iterations": int(args.lissa_iterations),
            "scale": float(args.lissa_scale),
            "damp": float(args.lissa_damp),
            "hutch_probes": int(args.hutch_probes),
            "hutch_seed": int(args.hutch_seed),
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
            "random_ranking": random_seed,
            "hutchinson": int(args.hutch_seed),
        },
        numerics={
            "torch_dtype": str(data.x.dtype),
            "compute_device": str(device),
            "cuda_version": torch.version.cuda,
        },
        target_checkpoint={
            "file_sha256": target_checkpoint["file_sha256"],
            "state_hash": target_checkpoint["state_hash"],
            "checkpoint_count": target_checkpoint["checkpoint_count"],
        },
    )

    def produce() -> ScoreBundlePayload:
        _synchronize(device)
        scoring_started = time.perf_counter()
        candidate_gradients = []
        target_gradients = []
        point_vectors = []
        checkpoint_gradient_seconds = []
        for item in checkpoints:
            _synchronize(device)
            started = time.perf_counter()
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
            point_vectors.append(matrix.mv(target).to(torch.float64))
            _synchronize(device)
            checkpoint_gradient_seconds.append(time.perf_counter() - started)

        final_candidate_gradient = candidate_gradients[-1]
        target_gradient, inverse_target, ihvp_observation = inverse_hessian_target(
            model,
            data,
            state=final_state,
            hessian_train_ids=candidate_ids,
            target_ids=target_ids,
            parameter_scope=args.parameter_scope,
            iterations=args.lissa_iterations,
            scale=args.lissa_scale,
            damp=args.lissa_damp,
        )
        max_target_diff = float(
            (target_gradient - target_gradients[-1]).abs().max().item()
        )
        if max_target_diff > 1e-6:
            raise RuntimeError("final target gradient mismatch")
        graph = _checkpoint_graph_scores(
            model,
            data,
            checkpoints=checkpoints,
            candidate_ids=candidate_ids,
            target_gradients=target_gradients,
            parameter_scope=args.parameter_scope,
            affected_hops=args.affected_hops,
            final_inverse_target=inverse_target,
        )
        generator = torch.Generator(device="cpu")
        generator.manual_seed(int(args.hutch_seed))
        probes = torch.randint(
            0,
            2,
            (int(args.hutch_probes), final_candidate_gradient.shape[1]),
            generator=generator,
            dtype=torch.int64,
        ).to(dtype=final_candidate_gradient.dtype)
        probes = probes.mul(2).sub(1)
        inverse_probes, hutch_observation = inverse_hessian_vectors(
            model,
            data,
            state=final_state,
            hessian_train_ids=candidate_ids,
            parameter_scope=args.parameter_scope,
            vectors=probes,
            iterations=args.lissa_iterations,
            scale=args.lissa_scale,
            damp=args.lissa_damp,
        )
        weights = [float(item["update_lr"]) for item in checkpoints]
        final_graph = graph["final_scores"]
        _synchronize(device)
        shared_prerequisite_seconds = time.perf_counter() - scoring_started
        method_score_seconds: Dict[str, float] = {}

        def timed_score(name: str, factory) -> torch.Tensor:
            _synchronize(device)
            started = time.perf_counter()
            value = factory()
            _synchronize(device)
            method_score_seconds[name] = time.perf_counter() - started
            return value

        scores = {
            "a_grad_norm": timed_score(
                "a_grad_norm",
                lambda: final_candidate_gradient.norm(dim=1).to(torch.float64),
            ),
            "b_param_hutch": timed_score(
                "b_param_hutch",
                lambda: hutchinson_parameter_change_scores(
                    final_candidate_gradient,
                    inverse_probes.to(final_candidate_gradient.device),
                ).to(torch.float64),
            ),
            "degree": timed_score(
                "degree",
                lambda: degree_scores(
                    data.edge_index, candidate_ids, int(data.num_nodes)
                ),
            ),
            "random": timed_score(
                "random",
                lambda: deterministic_random_scores(candidate_count, random_seed),
            ),
            "r_point": timed_score(
                "r_point",
                lambda: final_candidate_gradient.mv(inverse_target).to(torch.float64),
            ),
            "gt_simple": timed_score(
                "gt_simple", lambda: final_graph["gt_simple"].to(torch.float64)
            ),
            "gt_full": timed_score(
                "gt_full", lambda: final_graph["gt_full"].to(torch.float64)
            ),
            "p_point": timed_score("p_point", lambda: point_vectors[-1]),
            "p_simple": timed_score(
                "p_simple", lambda: final_graph["p_simple"].to(torch.float64)
            ),
            "p_graph": timed_score(
                "p_graph", lambda: final_graph["p_graph"].to(torch.float64)
            ),
            "tracin_cp_point_3": timed_score(
                "tracin_cp_point_3",
                lambda: weighted_checkpoint_scores(
                    point_vectors, weights, views["cp3"]
                ),
            ),
            "tracin_cp_point_6": timed_score(
                "tracin_cp_point_6",
                lambda: weighted_checkpoint_scores(
                    point_vectors, weights, views["cp_all"]
                ),
            ),
            "tracin_cp_simple_3": timed_score(
                "tracin_cp_simple_3",
                lambda: weighted_checkpoint_scores(
                    graph["simple_vectors"], weights, views["cp3"]
                ),
            ),
            "tracin_cp_simple_6": timed_score(
                "tracin_cp_simple_6",
                lambda: weighted_checkpoint_scores(
                    graph["simple_vectors"], weights, views["cp_all"]
                ),
            ),
            "tracin_cp_graph_3": timed_score(
                "tracin_cp_graph_3",
                lambda: weighted_checkpoint_scores(
                    graph["graph_vectors"], weights, views["cp3"]
                ),
            ),
            "tracin_cp_graph_6": timed_score(
                "tracin_cp_graph_6",
                lambda: weighted_checkpoint_scores(
                    graph["graph_vectors"], weights, views["cp_all"]
                ),
            ),
            "legacy": timed_score(
                "legacy",
                lambda: deployed_cross_gradient_scores(
                    final_candidate_gradient
                ).to(torch.float64),
            ),
        }
        if set(scores) != set(SCORE_NAMES):
            raise RuntimeError("score set does not match target-direct recipe")
        if any(not torch.isfinite(score).all() for score in scores.values()):
            raise RuntimeError("target-direct scores contain non-finite values")
        candidate_list = [int(value) for value in candidate_ids.tolist()]
        score_lists = {
            name: [float(value) for value in scores[name].tolist()]
            for name in sorted(scores)
        }
        rankings = {}
        method_ranking_seconds = {}
        for name in sorted(scores):
            _synchronize(device)
            started = time.perf_counter()
            rankings[name] = list(stable_ranking(candidate_list, scores[name]))
            _synchronize(device)
            method_ranking_seconds[name] = time.perf_counter() - started
        _synchronize(device)
        return ScoreBundlePayload.build(
            candidate_list,
            score_lists,
            rankings,
            {
                "experiment": "target_direct_v1",
                "score_family": SCORE_FAMILY,
                "dataset": args.dataset,
                "model": "OpenGU.GCNNet",
                "seed": int(args.seed),
                "candidate_count": candidate_count,
                "target_count": int(target_ids.numel()),
                "budget_projection": {
                    "semantics": SCORE_BUDGET_SEMANTICS,
                    "supported_ratios": list(APPROVED_BUDGET_RATIOS),
                    "denominator": "train_candidate_count",
                    "rounding": "floor_with_minimum_one",
                    "budget_conditioned_strategies": [],
                },
                "checkpoint_steps": [
                    int(item["global_step"]) for item in checkpoints
                ],
                "checkpoint_gradient_seconds": checkpoint_gradient_seconds,
                "checkpoint_graph": graph["checkpoint_observations"],
                "target_gradient_max_abs_diff": max_target_diff,
                "c_ihvp": ihvp_observation,
                "b_param_hutch": hutch_observation,
                "score_compute_seconds": time.perf_counter() - scoring_started,
                "shared_prerequisite_seconds": shared_prerequisite_seconds,
                "method_score_seconds": method_score_seconds,
                "method_ranking_seconds": method_ranking_seconds,
                "formal_score_count": len(SCORE_NAMES),
                "parameter_scope": args.parameter_scope,
                "target_checkpoint_state_hash": target_checkpoint["state_hash"],
            },
        )

    training_gpu_peaks = _gpu_peaks(device)
    torch.cuda.reset_peak_memory_stats(device)
    score_store = ScoreBundleStore(
        args.cache_root.expanduser().resolve(),
        producer_version=ProducerVersion(
            semantic_version=ALGORITHM_VERSION,
            source_fingerprint=code_fingerprint,
        ),
        index=CacheIndex(
            args.cache_root.expanduser().resolve() / "index.sqlite"
        ),
    )
    _synchronize(device)
    score_started = time.perf_counter()
    score_result = score_store.get_or_compute(
        recipe,
        produce,
        fail_if_called=(
            args.fail_if_score_producer_called
            or args.fail_if_producer_called
        ),
    )
    _synchronize(device)
    score_access_seconds = time.perf_counter() - score_started
    score_gpu_peaks = _gpu_peaks(device)
    payload = score_result.payload
    selection_dataset = make_dataset_selection_inputs(
        pipeline.data,
        dataset_name=args.dataset.lower(),
        source_path=Path(profile["data_path"]),
    )
    if tuple(payload.candidate_nodes_ordered) != selection_dataset.candidate_nodes:
        raise RuntimeError("ScoreBundle candidates differ from OpenGU candidates")
    selection_source_fingerprint = source_fingerprint(
        (
            REPO_ROOT / "experiments" / "selection_budget_planner.py",
            REPO_ROOT / "cache_v2" / "selection_materializer.py",
            Path(__file__).resolve(),
        )
    )
    selection_producer = ProducerVersion(
        semantic_version=SELECTION_PRODUCER_VERSION,
        source_fingerprint=selection_source_fingerprint,
    )
    selections = {}
    selection_timings = {}
    payload_score_seconds = {
        str(name): float(value)
        for name, value in dict(
            payload.metadata.get("method_score_seconds", {})
        ).items()
    }
    payload_ranking_seconds = {
        str(name): float(value)
        for name, value in dict(
            payload.metadata.get("method_ranking_seconds", {})
        ).items()
    }
    measured_method_seconds = sum(payload_score_seconds.values()) + sum(
        payload_ranking_seconds.values()
    )
    cold_shared_overhead_seconds = (
        max(0.0, score_access_seconds - measured_method_seconds)
        if not score_result.hit
        else None
    )
    for name in sorted(payload.rankings):
        ranking = tuple(int(node) for node in payload.rankings[name])
        started = time.perf_counter()
        materialized = materialize_budget_selection(
            store_root=args.selection_cache_root.expanduser().resolve(),
            dataset=selection_dataset,
            strategy=name,
            selector_seed=int(args.seed),
            budgets=(expected_k,),
            producer_version=selection_producer,
            algorithm_version=SELECTION_ALGORITHM_VERSION,
            parameters=selection_recipe_parameters(
                name=name,
                ratio=float(args.ratio),
                expected_k=expected_k,
                target_checkpoint_state_hash=target_checkpoint["state_hash"],
            ),
            source_score_artifact_id=score_result.artifact_id,
            producer=lambda max_k, ordered=ranking: ordered[:max_k],
            fail_if_producer_called=args.fail_if_producer_called,
        )
        materialization_seconds = time.perf_counter() - started
        incremental_seconds = (
            payload_score_seconds.get(name, 0.0)
            + payload_ranking_seconds.get(name, 0.0)
            + materialization_seconds
        )
        selection_projection_cache_hit = bool(materialized.cache_hit)
        selection_timings[name] = {
            "formula_seconds": payload_score_seconds.get(name),
            "ranking_seconds": payload_ranking_seconds.get(name),
            "materialization_seconds": materialization_seconds,
            "score_measurement_source": (
                "current_cold_compute"
                if not score_result.hit
                else "shared_score_bundle_metadata"
            ),
            "selection_projection_cache_hit": selection_projection_cache_hit,
            "cold_selection_projection_seconds": (
                materialization_seconds
                if not selection_projection_cache_hit
                else None
            ),
            "cold_incremental_seconds": (
                incremental_seconds if not score_result.hit else None
            ),
            "cold_standalone_equivalent_seconds": (
                cold_shared_overhead_seconds + incremental_seconds
                if cold_shared_overhead_seconds is not None
                else None
            ),
            "cold_amortized_17way_seconds": (
                cold_shared_overhead_seconds / len(payload.rankings)
                + incremental_seconds
                if cold_shared_overhead_seconds is not None
                else None
            ),
            "cache_hit": bool(materialized.cache_hit),
            "producer_called": bool(materialized.producer_called),
            "status": "success",
        }
        selections[name] = materialized.to_manifest(
            args.selection_cache_root.expanduser().resolve()
        )

    return {
        "schema": "target_direct_v1.selection_summary",
        "version": 2,
        "status": {"state": "success", "failure": None},
        "algorithm_version": ALGORITHM_VERSION,
        "dataset": args.dataset,
        "model": "OpenGU.GCNNet",
        "seed": int(args.seed),
        "processed_profile": PROFILE,
        "candidate_count": candidate_count,
        "target_count": int(target_ids.numel()),
        "budget": {
            "requested_ratio": float(args.ratio),
            "denominator": "train_candidate_count",
            "denominator_count": candidate_count,
            "rounding": "floor_with_minimum_one",
            "expected_k": expected_k,
        },
        "budget_projection": {
            "score_semantics": SCORE_BUDGET_SEMANTICS,
            "supported_ratios": list(APPROVED_BUDGET_RATIOS),
            "budget_conditioned_strategies": [],
            "score_bundle_shared_across_ratios": True,
            "selection_artifact_ratio_conditioned": True,
        },
        "target_objective": "validation_mask_mean_cross_entropy",
        "parameter_scope": args.parameter_scope,
        "dataset_profile": profile["manifest"],
        "git_provenance": git_provenance,
        "target_checkpoint": target_checkpoint,
        "training_observation": training_observation,
        "score_bundle": {
            "root": str(score_store.root),
            "hit": bool(score_result.hit),
            "outcome": score_result.outcome,
            "producer_called": bool(score_result.producer_called),
            "artifact_id": score_result.artifact_id,
            "recipe_hash": recipe.recipe_hash,
            "content_hash": score_result.content_hash,
            "payload_path": str(
                score_store.root.joinpath(*score_result.semantic_path.split("/"))
            ),
            "access_seconds": score_access_seconds,
            "cold_total_seconds": (
                score_access_seconds if not score_result.hit else None
            ),
            "warm_read_seconds": score_access_seconds if score_result.hit else None,
            "cold_shared_overhead_seconds": cold_shared_overhead_seconds,
            "timing_definition": {
                "cold_incremental_seconds": "formula + ranking + Selection Artifact materialization; excludes shared prerequisites",
                "cold_standalone_equivalent_seconds": "shared ScoreBundle overhead + this method's measured incremental work",
                "cold_amortized_17way_seconds": "one seventeenth of shared ScoreBundle overhead + this method's measured incremental work",
            },
        },
        "selection_cache": {
            "root": str(args.selection_cache_root.expanduser().resolve()),
            "method_count": len(selections),
            "hit_count": sum(
                1 for item in selection_timings.values() if item["cache_hit"]
            ),
            "method_timings": selection_timings,
        },
        "selection_artifacts": selections,
        "pairwise_metrics_at_k": _pair_metrics(payload, expected_k),
        "persisted_metadata": dict(payload.metadata),
        "gpu_memory": {
            "training_and_checkpoint": training_gpu_peaks,
            "score_bundle": score_gpu_peaks,
            "process_peak_allocated_bytes": max(
                int(training_gpu_peaks["peak_allocated_bytes"] or 0),
                int(score_gpu_peaks["peak_allocated_bytes"] or 0),
            ),
            "process_peak_reserved_bytes": max(
                int(training_gpu_peaks["peak_reserved_bytes"] or 0),
                int(score_gpu_peaks["peak_reserved_bytes"] or 0),
            ),
        },
        "runtime": {"total_seconds": time.perf_counter() - run_started},
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_geometric": torch_geometric.__version__,
            "cuda": torch.version.cuda,
            "device": str(device),
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parsed = build_parser().parse_args(argv)
    started = time.perf_counter()
    try:
        summary = run(parsed)
    except Exception as exc:
        failure_gpu = {
            "available": bool(torch.cuda.is_available()),
            "device": None,
            "peak_allocated_bytes": None,
            "peak_reserved_bytes": None,
        }
        if torch.cuda.is_available():
            try:
                failure_device = torch.device("cuda", parsed.cuda)
                failure_gpu = _gpu_peaks(failure_device)
            except Exception:
                pass
        failure = {
            "schema": "target_direct_v1.selection_summary",
            "version": 2,
            "status": {
                "state": "failed",
                "failure": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            },
            "dataset": parsed.dataset,
            "seed": int(parsed.seed),
            "processed_profile": PROFILE,
            "parameter_scope": parsed.parameter_scope,
            "budget": {
                "requested_ratio": float(parsed.ratio),
                "denominator": "train_candidate_count",
                "rounding": "floor_with_minimum_one",
            },
            "gpu_memory": failure_gpu,
            "runtime": {"total_seconds": time.perf_counter() - started},
        }
        _atomic_json(parsed.output, failure, parsed.overwrite_output)
        raise
    _atomic_json(parsed.output, summary, parsed.overwrite_output)
    print(
        json.dumps(
            {
                "output": str(parsed.output.expanduser().resolve()),
                "status": "success",
                "score_bundle_hit": summary["score_bundle"]["hit"],
                "expected_k": summary["budget"]["expected_k"],
                "target_checkpoint_state_hash": summary["target_checkpoint"][
                    "state_hash"
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
