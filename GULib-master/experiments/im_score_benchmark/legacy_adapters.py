"""Adapters for the repository's current Batch-CELF and strict CELF controls."""

from __future__ import annotations

import sys
import threading
from typing import Any, Sequence

import numpy as np
import torch

from .contracts import SelectionArtifact
from .rr_core import DirectedGraph


_IMPORT_LOCK = threading.Lock()


def _load_im_strategy() -> Any:
    """Load the legacy package without letting config.py consume runner args."""

    with _IMPORT_LOCK:
        original_argv = sys.argv
        try:
            sys.argv = [original_argv[0]]
            from attack.attack_strategies.im_strategy import IMStrategy
        finally:
            sys.argv = original_argv
    return IMStrategy


def legacy_celf_selection(
    graph: DirectedGraph,
    *,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
    selector_seed: int,
    mc_rounds: int,
    batch_size: int,
    algorithm: str,
) -> SelectionArtifact:
    """Call the accepted repository IM implementation without cache writes."""

    candidates = [int(node) for node in candidate_nodes]
    budget = int(budget)
    if len(candidates) != len(set(candidates)):
        raise ValueError("candidate_nodes must be unique")
    if not 1 <= budget <= len(candidates):
        raise ValueError("budget must be in [1, candidate_count]")
    edge_index = torch.tensor(
        [
            [src for src, _ in graph.edges],
            [dst for _, dst in graph.edges],
        ],
        dtype=torch.long,
    )
    strategy_class = _load_im_strategy()
    strategy = strategy_class(
        {
            "propagation_prob": float(propagation_probability),
            "mc_rounds": int(mc_rounds),
            "candidate_fraction": 1.0,
            "im_selector_seed": int(selector_seed),
            "im_batch_size": int(batch_size),
            "enable_score_cache": False,
            "im_parallel_mc": False,
        }
    )
    selected, gains = strategy.compute_im_celf(
        edge_index,
        graph.num_nodes,
        budget,
        candidates,
    )
    return SelectionArtifact(
        algorithm=algorithm,
        selected_nodes=np.asarray(selected, dtype=np.int64),
        accepted_gains=gains.detach().cpu().numpy().astype(np.float64),
        budget=budget,
        source_rr_count=0,
        metadata={
            "selection_semantics": (
                "strict_celf" if int(batch_size) == 1 else "batch_celf"
            ),
            "mc_rounds": int(mc_rounds),
            "batch_size": int(batch_size),
            "candidate_fraction": 1.0,
            "theory_status": (
                "exact_oracle_greedy_if_mc_exact"
                if int(batch_size) == 1
                else "batch_approximation_no_classic_greedy_guarantee"
            ),
        },
    )
