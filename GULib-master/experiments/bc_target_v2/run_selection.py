"""Run one cached Planetoid/GCN B+C selection cell with runtime telemetry."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

import torch
import torch_geometric
from torch import Tensor
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

from cache_v2 import ProducerVersion
from experiments.c_target_v1.core import (
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
    train_trajectory,
)
from experiments.c_target_v1.score_store import (
    ScoreBundlePayload,
    ScoreBundleStore,
)
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import make_dataset_selection_inputs

from .core import (
    checkpoint_view_indices,
    degree_scores,
    deterministic_random_scores,
    hutchinson_parameter_change_scores,
    inverse_hessian_vectors,
    weighted_checkpoint_scores,
)
from .recipe import ALGORITHM_VERSION, SCORE_NAMES, build_recipe


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = Path(
    "E:/project/OpenGU/GULib-master/data/raw/Planetoid"
)
DEFAULT_CACHE_ROOT = REPO_ROOT / "results" / "cache_v2" / "bc_target_v2"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "results" / "bc_target_v2" / "selection"
SELECTION_ALGORITHM_VERSION = "bc-target-score-ranking-prefix-v2"
SELECTION_PRODUCER_VERSION = "bc-target-maxk-selection-v2"


def _int_list(value: str) -> Sequence[int]:
    try:
        result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected comma-separated positive integers")
    if tuple(sorted(set(result))) != result:
        raise argparse.ArgumentTypeError("values must be unique and increasing")
    return result


def _budget_list(value: str) -> Sequence[int]:
    try:
        result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected comma-separated positive integers")
    return tuple(sorted(set(result), reverse=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument(
        "--dataset",
        choices=("Cora", "CiteSeer", "PubMed"),
        default="Cora",
    )
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument(
        "--selection-cache-root",
        type=Path,
        default=None,
        help="formal Cache V2 Selection store (default: <cache-root>/selection_artifacts)",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--budgets", type=_budget_list, default=(14, 7, 3))
    parser.add_argument("--num-threads", type=int, default=1)
    parser.add_argument(
        "--device",
        choices=("auto", "cpu", "cuda"),
        default="auto",
        help="compute device; auto uses CUDA when available",
    )
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
    parser.add_argument(
        "--parameter-scope",
        choices=("all_trainable", "last_layer"),
        default="all_trainable",
    )
    parser.add_argument("--affected-hops", type=int, default=2)
    parser.add_argument("--lissa-iterations", type=int, default=20)
    parser.add_argument("--lissa-scale", type=float, default=25.0)
    parser.add_argument("--lissa-damp", type=float, default=0.01)
    parser.add_argument("--hutch-probes", type=int, default=32)
    parser.add_argument("--hutch-seed", type=int, default=1729)
    parser.add_argument("--fail-if-producer-called", action="store_true")
    parser.add_argument("--overwrite-output", action="store_true")
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.seed < 0 or args.num_threads <= 0 or args.epochs <= 0:
        raise ValueError("seed, thread count, and epochs are invalid")
    if args.checkpoint_epochs[-1] != args.epochs:
        raise ValueError("final checkpoint epoch must equal --epochs")
    if len(args.checkpoint_epochs) < 3:
        raise ValueError("at least three checkpoints are required")
    if args.hidden_channels <= 0 or not 0 <= args.dropout < 1:
        raise ValueError("hidden channels or dropout is invalid")
    if args.lr <= 0 or args.weight_decay < 0 or not 0 < args.gamma <= 1:
        raise ValueError("optimizer settings are invalid")
    if args.affected_hops < 0 or args.hutch_probes <= 0:
        raise ValueError("affected hops and Hutchinson probes are invalid")


def _resolve_device(value: str) -> torch.device:
    normalized = str(value).strip().lower()
    if normalized == "auto":
        normalized = "cuda" if torch.cuda.is_available() else "cpu"
    if normalized == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    if normalized == "cuda":
        return torch.device("cuda", torch.cuda.current_device())
    return torch.device(normalized)


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


def _write_json_atomic(
    path: Path, value: Mapping[str, Any], overwrite: bool
) -> None:
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


def _all_pair_metrics(
    payload: ScoreBundlePayload, budgets: Sequence[int]
) -> Dict[str, Dict[str, Mapping[str, Any]]]:
    result: Dict[str, Dict[str, Mapping[str, Any]]] = {}
    names = sorted(payload.scores)
    for left, right in itertools.combinations(names, 2):
        key = "{0}__{1}".format(left, right)
        result[key] = {}
        for budget in budgets:
            result[key][str(budget)] = pair_metrics(
                payload.scores[left],
                payload.scores[right],
                payload.rankings[left],
                payload.rankings[right],
                int(budget),
            )
    return result


def _checkpoint_graph_scores(
    model: GateGCN,
    data,
    *,
    checkpoints,
    candidate_ids: Tensor,
    target_gradients,
    parameter_scope: str,
    affected_hops: int,
    final_inverse_target: Tensor,
) -> Dict[str, Any]:
    simple_vectors = []
    graph_vectors = []
    observations = []
    final_index = len(checkpoints) - 1
    final_scores = None
    for index, item in enumerate(checkpoints):
        target = target_gradients[index]
        inverse = final_inverse_target if index == final_index else target
        scores, observation = graph_source_scores(
            model,
            data,
            state=item["state"],
            candidate_ids=candidate_ids,
            parameter_scope=parameter_scope,
            affected_hops=affected_hops,
            target_gradient=target,
            inverse_target=inverse,
        )
        simple_vectors.append(scores["p_simple"].to(torch.float64))
        graph_vectors.append(scores["p_graph"].to(torch.float64))
        observations.append(
            {
                "global_step": int(item["global_step"]),
                "seconds": float(observation["graph_source_seconds"]),
                "affected_size_min": int(observation["affected_size_min"]),
                "affected_size_mean": float(observation["affected_size_mean"]),
                "affected_size_max": int(observation["affected_size_max"]),
            }
        )
        if index == final_index:
            final_scores = scores
            final_observation = observation
    if final_scores is None:
        raise RuntimeError("final graph source scores were not produced")
    return {
        "simple_vectors": simple_vectors,
        "graph_vectors": graph_vectors,
        "final_scores": final_scores,
        "final_observation": final_observation,
        "checkpoint_observations": observations,
    }


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    _validate_args(args)
    run_started = time.perf_counter()
    device = _resolve_device(args.device)
    if device.type == "cuda":
        torch.cuda.set_device(device)
        torch.cuda.reset_peak_memory_stats(device)
    seed_everything(args.seed, args.num_threads)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.seed)

    dataset = Planetoid(
        root=str(args.data_root.expanduser().resolve()),
        name=args.dataset,
        transform=NormalizeFeatures(),
    )
    data = dataset[0].to(device)
    candidate_ids = torch.where(data.train_mask)[0].sort().values
    target_ids = torch.where(data.val_mask)[0].sort().values
    hessian_train_ids = candidate_ids
    if not bool(data.val_mask.any().item()):
        raise ValueError("validation target set is empty")
    if max(args.budgets) > candidate_ids.numel():
        raise ValueError("a requested budget exceeds the candidate count")

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
    views = checkpoint_view_indices(len(checkpoints))

    source_paths = (
        Path(__file__).resolve(),
        Path(__file__).with_name("__init__.py"),
        Path(__file__).with_name("core.py"),
        Path(__file__).with_name("recipe.py"),
        REPO_ROOT / "experiments" / "c_target_v1" / "core.py",
        REPO_ROOT / "experiments" / "c_target_v1" / "score_store.py",
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
    random_seed = int(args.seed) + 100003
    recipe = build_recipe(
        source_fingerprint=code_fingerprint,
        data_identity={
            "dataset": args.dataset,
            "dataset_family": "Planetoid",
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
            "parameter_schema_hash": parameter_schema_hash(
                model, args.parameter_scope
            ),
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
        checkpoint_views=views,
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "affected_set": "candidate_plus_undirected_k_hop_neighbors",
            "affected_hops": int(args.affected_hops),
            "grad1": "sum_ce_original_graph_affected_set",
            "grad2": "sum_ce_deleted_graph_affected_neighbors_excluding_candidate",
            "per_candidate_exact_retrain": False,
        },
        hessian={
            "method": "LiSSA_full_train_mean_ce",
            "iterations": int(args.lissa_iterations),
            "scale": float(args.lissa_scale),
            "damp": float(args.lissa_damp),
            "shared_c_target_solve": "H^-1_g_E_once",
            "b_reference": "per_candidate_LiSSA_norm",
            "b_proxy": "shared_Rademacher_Hutchinson",
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
            "deterministic_algorithms": True,
        },
        numerics={
            "torch_dtype": str(data.x.dtype),
            "deterministic_algorithms": True,
            "compute_device": str(device),
            "cuda_version": torch.version.cuda if device.type == "cuda" else None,
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
        max_target_diff = float(
            (target_gradient - final_checkpoint_target).abs().max().item()
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
        inverse_probes, b_hutch_observation = inverse_hessian_vectors(
            model,
            data,
            state=final_state,
            hessian_train_ids=hessian_train_ids,
            parameter_scope=args.parameter_scope,
            vectors=probes,
            iterations=args.lissa_iterations,
            scale=args.lissa_scale,
            damp=args.lissa_damp,
        )

        weights = [float(item["update_lr"]) for item in checkpoints]
        final_graph_scores = graph["final_scores"]
        scores = {
            "a_grad_norm": final_candidate_gradient.norm(dim=1).to(torch.float64),
            "b_param_hutch": hutchinson_parameter_change_scores(
                final_candidate_gradient,
                inverse_probes.to(final_candidate_gradient.device),
            ).to(torch.float64),
            "degree": degree_scores(
                data.edge_index, candidate_ids, int(data.num_nodes)
            ),
            "random": deterministic_random_scores(
                int(candidate_ids.numel()), random_seed
            ),
            "r_point": final_candidate_gradient.mv(inverse_target).to(
                torch.float64
            ),
            "gt_simple": final_graph_scores["gt_simple"].to(torch.float64),
            "gt_full": final_graph_scores["gt_full"].to(torch.float64),
            "p_point": point_vectors[-1],
            "p_simple": final_graph_scores["p_simple"].to(torch.float64),
            "p_graph": final_graph_scores["p_graph"].to(torch.float64),
            "tracin_cp_point_3": weighted_checkpoint_scores(
                point_vectors, weights, views["cp3"]
            ),
            "tracin_cp_point_6": weighted_checkpoint_scores(
                point_vectors, weights, views["cp_all"]
            ),
            "tracin_cp_simple_3": weighted_checkpoint_scores(
                graph["simple_vectors"], weights, views["cp3"]
            ),
            "tracin_cp_simple_6": weighted_checkpoint_scores(
                graph["simple_vectors"], weights, views["cp_all"]
            ),
            "tracin_cp_graph_3": weighted_checkpoint_scores(
                graph["graph_vectors"], weights, views["cp3"]
            ),
            "tracin_cp_graph_6": weighted_checkpoint_scores(
                graph["graph_vectors"], weights, views["cp_all"]
            ),
            "legacy": deployed_cross_gradient_scores(
                final_candidate_gradient
            ).to(torch.float64),
        }
        if set(scores) != set(SCORE_NAMES):
            raise RuntimeError("score set does not match the frozen recipe")
        if any(not torch.isfinite(value).all() for value in scores.values()):
            raise ValueError("selection scores contain non-finite values")

        candidate_list = [int(value) for value in candidate_ids.tolist()]
        score_lists = {
            name: [float(value) for value in scores[name].tolist()]
            for name in sorted(scores)
        }
        rankings = {
            name: list(stable_ranking(candidate_list, scores[name]))
            for name in sorted(scores)
        }
        _synchronize(device)
        metadata = {
            "experiment": "bc_target_v2",
            "dataset": args.dataset,
            "model": "GCN",
            "seed": int(args.seed),
            "candidate_count": len(candidate_list),
            "target_count": int(target_ids.numel()),
            "budgets_supported": list(args.budgets),
            "checkpoint_steps": [
                int(item["global_step"]) for item in checkpoints
            ],
            "checkpoint_weights": weights,
            "checkpoint_views": {
                name: list(indices) for name, indices in views.items()
            },
            "checkpoint_gradient_seconds": checkpoint_gradient_seconds,
            "checkpoint_graph": graph["checkpoint_observations"],
            "target_gradient_max_abs_diff": max_target_diff,
            "c_ihvp": ihvp_observation,
            "b_param_hutch": b_hutch_observation,
            "final_graph_source": graph["final_observation"],
            "score_compute_seconds": time.perf_counter() - scoring_started,
            "formal_score_count": len(SCORE_NAMES),
            "validation_only_scores_excluded": ["b_param_lissa"],
            "per_candidate_exact_retrain_performed": False,
        }
        return ScoreBundlePayload.build(
            candidate_list, score_lists, rankings, metadata
        )

    store = ScoreBundleStore(
        args.cache_root.expanduser().resolve(),
        producer_version=ProducerVersion(
            semantic_version=ALGORITHM_VERSION,
            source_fingerprint=code_fingerprint,
        ),
    )
    training_gpu_peaks = _gpu_peaks(device)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    _synchronize(device)
    score_bundle_started = time.perf_counter()
    store_result = store.get_or_compute(
        recipe,
        produce,
        fail_if_called=args.fail_if_producer_called,
    )
    _synchronize(device)
    score_bundle_access_seconds = time.perf_counter() - score_bundle_started
    score_bundle_gpu_peaks = _gpu_peaks(device)
    payload = store_result.payload
    selection_cache_root = (
        args.cache_root.expanduser().resolve() / "selection_artifacts"
        if args.selection_cache_root is None
        else args.selection_cache_root.expanduser().resolve()
    )
    selection_dataset = make_dataset_selection_inputs(
        data,
        dataset_name=args.dataset,
    )
    if tuple(payload.candidate_nodes_ordered) != selection_dataset.candidate_nodes:
        raise RuntimeError("ScoreBundle candidates do not match Selection inputs")
    selection_source_fingerprint = source_fingerprint(
        (
            REPO_ROOT / "experiments" / "selection_budget_planner.py",
            REPO_ROOT / "cache_v2" / "selection_materializer.py",
        )
    )
    selection_producer = ProducerVersion(
        semantic_version=SELECTION_PRODUCER_VERSION,
        source_fingerprint=selection_source_fingerprint,
    )
    selection_artifacts = {}
    selection_timings = {}
    for name in sorted(payload.rankings):
        ranking = tuple(int(node) for node in payload.rankings[name])
        selection_started = time.perf_counter()
        materialized = materialize_budget_selection(
            store_root=selection_cache_root,
            dataset=selection_dataset,
            strategy=name,
            selector_seed=int(args.seed),
            budgets=args.budgets,
            producer_version=selection_producer,
            algorithm_version=SELECTION_ALGORITHM_VERSION,
            parameters={
                "prefix_stable": True,
                "score_name": name,
                "score_family": "bc_target_selection_score_bundle",
                "orientation": "score_desc_more_influential_or_harmful_if_removed",
                "ranking": "score_desc_node_id_asc",
            },
            source_score_artifact_id=store_result.artifact_id,
            producer=lambda max_k, ordered=ranking: ordered[:max_k],
            fail_if_producer_called=args.fail_if_producer_called,
        )
        selection_seconds = time.perf_counter() - selection_started
        selection_artifacts[name] = materialized.to_manifest(selection_cache_root)
        selection_timings[name] = {
            "seconds": selection_seconds,
            "cache_hit": bool(materialized.cache_hit),
            "outcome": "hit" if materialized.cache_hit else "miss_saved",
            "producer_called": bool(materialized.producer_called),
            "status": "success",
        }
    output_path = args.output
    if output_path is None:
        output_path = DEFAULT_OUTPUT_ROOT / (
            "{0}_gcn_seed{1}_selection.json".format(
                args.dataset.lower(), args.seed
            )
        )
    summary = {
        "schema": "bc_target_v2.selection_summary",
        "version": 2,
        "algorithm_version": ALGORITHM_VERSION,
        "dataset": args.dataset,
        "model": "GCN",
        "seed": int(args.seed),
        "candidate_count": len(payload.candidate_nodes_ordered),
        "target_count": int(target_ids.numel()),
        "budgets": list(args.budgets),
        "target_set": "validation_mask_mean_ce",
        "per_candidate_exact_retrain_performed": False,
        "status": {"state": "success", "failure": None},
        "cache": {
            "root": str(store.root),
            "hit": bool(store_result.hit),
            "outcome": store_result.outcome,
            "producer_called": bool(store_result.producer_called),
            "artifact_id": store_result.artifact_id,
            "recipe_hash": recipe.recipe_hash,
            "content_hash": store_result.content_hash,
            "semantic_path": store_result.semantic_path,
            "payload_path": str(
                store.root.joinpath(*store_result.semantic_path.split("/"))
            ),
        },
        "selection_cache": {
            "root": str(selection_cache_root),
            "lookup_policy": "exact_then_smallest_covering_k",
            "request_max_k": max(int(value) for value in args.budgets),
            "method_count": len(selection_artifacts),
            "hit_count": sum(
                1 for item in selection_artifacts.values() if item["cache"]["hit"]
            ),
            "miss_saved_count": sum(
                1 for item in selection_artifacts.values() if not item["cache"]["hit"]
            ),
            "producer_call_count": sum(
                1
                for item in selection_artifacts.values()
                if item["cache"]["producer_called"]
            ),
            "method_timings": selection_timings,
        },
        "selection_artifacts": selection_artifacts,
        "selector_model_final_state_hash": state_hash(final_state),
        "pairwise_metrics": _all_pair_metrics(payload, args.budgets),
        "scores": {
            name: list(payload.scores[name]) for name in sorted(payload.scores)
        },
        "rankings": {
            name: list(payload.rankings[name])
            for name in sorted(payload.rankings)
        },
        "persisted_metadata": dict(payload.metadata),
        "training_observation": training_observation,
        "runtime": {
            "total_seconds": None,
            "score_bundle_access_seconds": score_bundle_access_seconds,
            "score_bundle_cold_total_seconds": (
                score_bundle_access_seconds if not store_result.hit else None
            ),
            "score_bundle_warm_read_seconds": (
                score_bundle_access_seconds if store_result.hit else None
            ),
            "persisted_score_compute_seconds": payload.metadata.get(
                "score_compute_seconds"
            ),
        },
        "gpu_memory": {
            "training_and_recipe": training_gpu_peaks,
            "score_bundle": score_bundle_gpu_peaks,
            "process_peak_allocated_bytes": (
                max(
                    int(training_gpu_peaks["peak_allocated_bytes"] or 0),
                    int(score_bundle_gpu_peaks["peak_allocated_bytes"] or 0),
                )
                if device.type == "cuda"
                else None
            ),
            "process_peak_reserved_bytes": (
                max(
                    int(training_gpu_peaks["peak_reserved_bytes"] or 0),
                    int(score_bundle_gpu_peaks["peak_reserved_bytes"] or 0),
                )
                if device.type == "cuda"
                else None
            ),
        },
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_geometric": torch_geometric.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
            "device": str(device),
            "cuda": torch.version.cuda,
        },
        "config": {
            "data_root": str(args.data_root.expanduser().resolve()),
            "cache_root": str(store.root),
            "selection_cache_root": str(selection_cache_root),
            "dataset": args.dataset,
            "seed": int(args.seed),
            "budgets": list(args.budgets),
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
            "lissa_iterations": int(args.lissa_iterations),
            "lissa_scale": float(args.lissa_scale),
            "lissa_damp": float(args.lissa_damp),
            "hutch_probes": int(args.hutch_probes),
            "hutch_seed": int(args.hutch_seed),
            "num_threads": int(args.num_threads),
            "device": str(device),
        },
    }
    _synchronize(device)
    summary["runtime"]["total_seconds"] = time.perf_counter() - run_started
    _write_json_atomic(
        output_path, summary, overwrite=args.overwrite_output
    )
    print(
        json.dumps(
            {
                "output": str(output_path.expanduser().resolve()),
                "dataset": args.dataset,
                "seed": int(args.seed),
                "cache_hit": bool(store_result.hit),
                "artifact_id": store_result.artifact_id,
                "selection_cache_hit_count": summary["selection_cache"]["hit_count"],
                "selection_cache_miss_saved_count": summary["selection_cache"]["miss_saved_count"],
                "candidate_count": len(payload.candidate_nodes_ordered),
                "score_count": len(payload.scores),
                "budgets": list(args.budgets),
                "seconds": summary["runtime"]["total_seconds"],
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
