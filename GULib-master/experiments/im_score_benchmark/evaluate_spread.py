"""Independent common-random RR evaluation against the degree baseline."""

from __future__ import annotations

import math
from typing import Any, Dict, Mapping, Sequence

import numpy as np

from .rr_core import DirectedGraph, RRBundle, sample_rr_bundle


def _coverage_flags(bundle: RRBundle, selected_nodes: Sequence[int]) -> np.ndarray:
    selected = {int(node) for node in selected_nodes}
    local_selected = {
        index
        for index, node in enumerate(bundle.candidate_nodes.tolist())
        if int(node) in selected
    }
    flags = np.zeros(bundle.rr_count, dtype=np.float64)
    if not local_selected:
        return flags
    for rr_index in range(bundle.rr_count):
        if any(
            int(local_id) in local_selected
            for local_id in bundle.local_row(rr_index)
        ):
            flags[rr_index] = 1.0
    return flags


def _paired_summary(
    method_hits: np.ndarray,
    degree_hits: np.ndarray,
    num_nodes: int,
) -> Dict[str, Any]:
    differences = method_hits - degree_hits
    count = int(differences.size)
    mean_difference = float(differences.mean())
    if count <= 1:
        half_width = math.inf
    else:
        half_width = float(
            1.959963984540054
            * differences.std(ddof=1)
            / math.sqrt(float(count))
        )
    method_probability = float(method_hits.mean())
    degree_probability = float(degree_hits.mean())
    return {
        "sample_count": count,
        "coverage_probability": method_probability,
        "spread_estimate": float(num_nodes) * method_probability,
        "degree_coverage_probability": degree_probability,
        "degree_spread_estimate": float(num_nodes) * degree_probability,
        "spread_ratio_vs_degree": (
            None
            if degree_probability <= 0.0
            else method_probability / degree_probability
        ),
        "paired_difference_probability": mean_difference,
        "paired_difference_spread": float(num_nodes) * mean_difference,
        "paired_ci95_probability": [
            mean_difference - half_width,
            mean_difference + half_width,
        ],
        "paired_ci95_half_width_probability": half_width,
    }


def evaluate_selections(
    graph: DirectedGraph,
    *,
    selections: Mapping[str, Sequence[int]],
    degree_key: str,
    propagation_probability: float,
    evaluator_seed: int,
    min_rr_sets: int = 4096,
    batch_rr_sets: int = 4096,
    max_rr_sets: int = 2_000_000,
    target_half_width_probability: float = 0.005,
    root_nodes: Sequence[int] = None,
) -> Dict[str, Any]:
    """Sequential paired evaluation using samples independent of selectors."""

    if degree_key not in selections:
        raise ValueError("degree_key is missing from selections")
    if len(selections) < 2:
        raise ValueError("at least degree and one competitor are required")
    min_rr_sets = int(min_rr_sets)
    batch_rr_sets = int(batch_rr_sets)
    max_rr_sets = int(max_rr_sets)
    if not 1 <= min_rr_sets <= max_rr_sets or batch_rr_sets <= 0:
        raise ValueError("invalid evaluator RR schedule")
    union_nodes = sorted(
        {
            int(node)
            for selected in selections.values()
            for node in selected
        }
    )
    if not union_nodes:
        raise ValueError("selection union must be non-empty")
    observations = {
        name: [] for name in sorted(selections)
    }
    total = 0
    batch_index = 0
    summaries: Dict[str, Any] = {}
    while total < max_rr_sets:
        current = min(batch_rr_sets, max_rr_sets - total)
        seed = int(
            np.random.SeedSequence(
                [int(evaluator_seed), int(batch_index)]
            ).generate_state(1, dtype=np.uint64)[0]
        )
        bundle = sample_rr_bundle(
            graph,
            candidate_nodes=union_nodes,
            rr_count=current,
            propagation_probability=propagation_probability,
            rr_seed=seed,
            root_nodes=root_nodes,
            metadata={"phase": "independent_evaluator", "batch": batch_index},
        )
        for name, selected in selections.items():
            observations[name].append(_coverage_flags(bundle, selected))
        total += current
        batch_index += 1
        if total < min_rr_sets:
            continue
        degree_hits = np.concatenate(observations[degree_key])
        summaries = {
            name: _paired_summary(
                np.concatenate(parts),
                degree_hits,
                graph.num_nodes,
            )
            for name, parts in observations.items()
        }
        competitor_widths = [
            value["paired_ci95_half_width_probability"]
            for name, value in summaries.items()
            if name != degree_key
        ]
        if competitor_widths and max(competitor_widths) <= float(
            target_half_width_probability
        ):
            break
    return {
        "schema": "im_score_benchmark.independent_spread_evaluation",
        "version": 1,
        "degree_key": degree_key,
        "propagation_probability": float(propagation_probability),
        "evaluator_seed": int(evaluator_seed),
        "sample_count": int(total),
        "batch_count": int(batch_index),
        "target_half_width_probability": float(
            target_half_width_probability
        ),
        "max_rr_sets": int(max_rr_sets),
        "stopped_for_precision": (
            total < max_rr_sets
            and all(
                value["paired_ci95_half_width_probability"]
                <= float(target_half_width_probability)
                for name, value in summaries.items()
                if name != degree_key
            )
        ),
        "methods": summaries,
    }
