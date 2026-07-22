"""Dataset-agnostic selector benchmark engine."""

from __future__ import annotations

import platform
import sys
from typing import Any, Dict, Iterable, Mapping, Sequence

import numpy as np

from .baselines import degree_score, random_selection
from .evaluate_spread import evaluate_selections
from .legacy_adapters import legacy_celf_selection
from .rr_core import DirectedGraph, sample_rr_bundle
from .score_reducers import build_score_bundle
from .selectors import (
    corrected_imm_select,
    opimc_select,
    select_top_k_score,
)
from .telemetry import measure_call


SUPPORTED_METHODS = (
    "degree",
    "random",
    "im_batch_celf_current",
    "im_celf_strict",
    "rr_sni",
    "rr_shapley",
    "rr_ksemivalue",
    "corrected_imm",
    "opimc",
)


def _compose_telemetry(
    online: Mapping[str, Any],
    *shared: Mapping[str, Any],
    setup: Mapping[str, Any] = None,
) -> Dict[str, Any]:
    """Expose online, shared-precompute, and conservative end-to-end cost."""

    shared_items = [dict(item) for item in shared]
    rss_values = [
        value
        for value in [online.get("peak_rss_bytes")]
        + [item.get("peak_rss_bytes") for item in shared_items]
        if value is not None
    ]
    python_peak_values = [
        int(online.get("python_tracemalloc_peak_bytes", 0))
    ] + [
        int(item.get("python_tracemalloc_peak_bytes", 0))
        for item in shared_items
    ]
    online_seconds = float(online["wall_seconds"])
    shared_seconds = sum(float(item["wall_seconds"]) for item in shared_items)
    return {
        **dict(online),
        "wall_seconds": online_seconds + shared_seconds,
        "peak_rss_bytes": None if not rss_values else int(max(rss_values)),
        "python_tracemalloc_peak_bytes": int(max(python_peak_values)),
        "time_semantics": "end_to_end_including_shared_precompute",
        "online_wall_seconds": online_seconds,
        "shared_precompute_wall_seconds": shared_seconds,
        "shared_precompute_components": shared_items,
        "excluded_one_time_setup_wall_seconds": (
            0.0 if setup is None else float(setup["wall_seconds"])
        ),
    }


def _seed(base_seed: int, *parts: int) -> int:
    return int(
        np.random.SeedSequence(
            [int(base_seed)] + [int(value) for value in parts]
        ).generate_state(1, dtype=np.uint32)[0]
    )


def run_selector_benchmark(
    graph: DirectedGraph,
    *,
    dataset_name: str,
    candidate_nodes: Sequence[int],
    budgets: Iterable[int],
    selector_seed: int,
    propagation_probability: float,
    methods: Sequence[str] = SUPPORTED_METHODS,
    score_rr_count: int = 4096,
    legacy_mc_rounds: int = 100,
    current_celf_batch_size: int = 5,
    epsilon: float = 0.1,
    delta: float = 0.01,
    imm_max_rr_sets: int = 2_000_000,
    opim_initial_rr_count: int = 4096,
    opim_max_rr_sets: int = 2_000_000,
    evaluator_seed: int = 99_999,
    evaluator_min_rr_sets: int = 4096,
    evaluator_batch_rr_sets: int = 4096,
    evaluator_max_rr_sets: int = 2_000_000,
    evaluator_half_width: float = 0.005,
    source_manifest: Mapping[str, Any] = None,
) -> Dict[str, Any]:
    """Run requested selectors and independent degree-relative evaluation."""

    candidates = np.asarray(candidate_nodes, dtype=np.int64).reshape(-1)
    if candidates.size == 0 or candidates.size != np.unique(candidates).size:
        raise ValueError("candidate_nodes must be non-empty and unique")
    requested_methods = tuple(dict.fromkeys(str(value) for value in methods))
    if not requested_methods:
        raise ValueError("methods must be non-empty")
    unknown = sorted(set(requested_methods).difference(SUPPORTED_METHODS))
    if unknown:
        raise ValueError("unsupported methods: {0}".format(unknown))
    if "degree" not in requested_methods:
        raise ValueError("degree baseline is mandatory")
    if len(requested_methods) < 2:
        raise ValueError("at least degree and one competitor are required")
    budget_values = sorted({int(value) for value in budgets})
    if not budget_values:
        raise ValueError("budgets must be non-empty")
    if budget_values[0] <= 0 or budget_values[-1] > candidates.size:
        raise ValueError("budgets are outside candidate domain")

    timings: Dict[str, Any] = {}
    degree_artifact, timings["degree_score"] = measure_call(
        degree_score,
        graph,
        candidates,
    )
    needs_rr_scores = any(
        method in requested_methods
        for method in ("rr_sni", "rr_shapley", "rr_ksemivalue")
    )
    score_artifacts = {}
    rr_summary = None
    if needs_rr_scores:
        rr_bundle, timings["shared_score_rr_bundle"] = measure_call(
            sample_rr_bundle,
            graph,
            candidate_nodes=candidates,
            rr_count=int(score_rr_count),
            propagation_probability=propagation_probability,
            rr_seed=_seed(selector_seed, 100),
            metadata={"phase": "shared_full_score"},
        )
        rr_summary = rr_bundle.summary()
        score_artifacts, timings["score_reducers"] = measure_call(
            build_score_bundle,
            rr_bundle,
            budget_values,
        )
    needs_legacy = any(
        method in requested_methods
        for method in ("im_batch_celf_current", "im_celf_strict")
    )
    if needs_legacy:
        warmup_graph = DirectedGraph.from_edges(2, [(0, 1)])
        _, timings["legacy_runtime_warmup"] = measure_call(
            legacy_celf_selection,
            warmup_graph,
            candidate_nodes=[0, 1],
            budget=1,
            propagation_probability=0.5,
            selector_seed=1,
            mc_rounds=1,
            batch_size=1,
            algorithm="legacy_runtime_warmup_not_a_result",
        )

    per_budget: Dict[str, Any] = {}
    for budget in budget_values:
        selections = {}
        method_payloads: Dict[str, Any] = {}

        degree_selection, method_time = measure_call(
            select_top_k_score,
            degree_artifact,
            budget,
            algorithm="degree",
        )
        selections["degree"] = degree_selection.selected_nodes.tolist()
        method_payloads["degree"] = {
            "selection": degree_selection.to_dict(),
            "telemetry": _compose_telemetry(
                method_time,
                timings["degree_score"],
            ),
        }

        if "random" in requested_methods:
            selection, method_time = measure_call(
                random_selection,
                candidates,
                budget,
                _seed(selector_seed, budget, 200),
            )
            selections["random"] = selection.selected_nodes.tolist()
            method_payloads["random"] = {
                "selection": selection.to_dict(),
                "telemetry": _compose_telemetry(method_time),
            }

        legacy_specs = (
            (
                "im_batch_celf_current",
                int(current_celf_batch_size),
            ),
            ("im_celf_strict", 1),
        )
        for method, batch_size in legacy_specs:
            if method not in requested_methods:
                continue
            selection, method_time = measure_call(
                legacy_celf_selection,
                graph,
                candidate_nodes=candidates,
                budget=budget,
                propagation_probability=propagation_probability,
                selector_seed=_seed(selector_seed, budget, 250, batch_size),
                mc_rounds=int(legacy_mc_rounds),
                batch_size=batch_size,
                algorithm=method,
            )
            selections[method] = selection.selected_nodes.tolist()
            method_payloads[method] = {
                "selection": selection.to_dict(),
                "telemetry": _compose_telemetry(
                    method_time,
                    setup=timings["legacy_runtime_warmup"],
                ),
            }

        static_keys = {
            "rr_sni": "rr_sni",
            "rr_shapley": "rr_shapley",
            "rr_ksemivalue": "rr_ksemivalue_k{0}".format(budget),
        }
        for method, artifact_key in static_keys.items():
            if method not in requested_methods:
                continue
            selection, method_time = measure_call(
                select_top_k_score,
                score_artifacts[artifact_key],
                budget,
                algorithm=method,
            )
            selections[method] = selection.selected_nodes.tolist()
            method_payloads[method] = {
                "selection": selection.to_dict(),
                "score": score_artifacts[artifact_key].to_dict(),
                "telemetry": _compose_telemetry(
                    method_time,
                    timings["shared_score_rr_bundle"],
                    timings["score_reducers"],
                ),
            }

        if "corrected_imm" in requested_methods:
            selection, method_time = measure_call(
                corrected_imm_select,
                graph,
                candidate_nodes=candidates,
                budget=budget,
                propagation_probability=propagation_probability,
                selector_seed=_seed(selector_seed, budget, 300),
                epsilon=epsilon,
                delta=delta,
                max_rr_sets=int(imm_max_rr_sets),
            )
            selections["corrected_imm"] = selection.selected_nodes.tolist()
            method_payloads["corrected_imm"] = {
                "selection": selection.to_dict(),
                "telemetry": _compose_telemetry(method_time),
            }

        if "opimc" in requested_methods:
            selection, method_time = measure_call(
                opimc_select,
                graph,
                candidate_nodes=candidates,
                budget=budget,
                propagation_probability=propagation_probability,
                selector_seed=_seed(selector_seed, budget, 400),
                epsilon=epsilon,
                delta=delta,
                initial_rr_count=int(opim_initial_rr_count),
                max_rr_sets=int(opim_max_rr_sets),
            )
            selections["opimc"] = selection.selected_nodes.tolist()
            method_payloads["opimc"] = {
                "selection": selection.to_dict(),
                "telemetry": _compose_telemetry(method_time),
            }

        evaluation, evaluation_time = measure_call(
            evaluate_selections,
            graph,
            selections=selections,
            degree_key="degree",
            propagation_probability=propagation_probability,
            evaluator_seed=_seed(evaluator_seed, budget),
            min_rr_sets=int(evaluator_min_rr_sets),
            batch_rr_sets=int(evaluator_batch_rr_sets),
            max_rr_sets=int(evaluator_max_rr_sets),
            target_half_width_probability=float(evaluator_half_width),
        )
        per_budget[str(budget)] = {
            "budget": budget,
            "methods": method_payloads,
            "independent_evaluation": evaluation,
            "evaluation_telemetry": evaluation_time,
        }

    return {
        "schema": "im_score_benchmark.selector_benchmark",
        "version": 1,
        "run_kind": "selector_only",
        "dataset": str(dataset_name),
        "graph": {
            "num_nodes": graph.num_nodes,
            "edge_count": graph.edge_count,
            "candidate_count": int(candidates.size),
        },
        "config": {
            "budgets": budget_values,
            "methods": list(requested_methods),
            "selector_seed": int(selector_seed),
            "propagation_probability": float(propagation_probability),
            "candidate_fraction": 1.0,
            "score_rr_count": int(score_rr_count),
            "legacy_mc_rounds": int(legacy_mc_rounds),
            "current_celf_batch_size": int(current_celf_batch_size),
            "epsilon": float(epsilon),
            "delta": float(delta),
            "evaluator_seed": int(evaluator_seed),
        },
        "source_manifest": (
            {} if source_manifest is None else dict(source_manifest)
        ),
        "shared_rr_bundle": rr_summary,
        "shared_timings": timings,
        "budgets": per_budget,
        "environment": {
            "python": platform.python_version(),
            "executable": sys.executable,
            "platform": platform.platform(),
        },
    }
