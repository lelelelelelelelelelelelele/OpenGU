"""Degree and random baselines under the shared candidate contract."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .contracts import ScoreArtifact, SelectionArtifact
from .rr_core import DirectedGraph


def _stable_ranking(candidate_nodes: np.ndarray, scores: np.ndarray) -> np.ndarray:
    order = np.lexsort((candidate_nodes, -scores))
    return candidate_nodes[order].astype(np.int64, copy=False)


def degree_score(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
) -> ScoreArtifact:
    """Match OpenGU DegreeStrategy by using directed source/out degree."""

    candidates = np.asarray(candidate_nodes, dtype=np.int64).reshape(-1)
    scores = np.asarray(
        [len(graph.out_neighbors[int(node)]) for node in candidates.tolist()],
        dtype=np.float64,
    )
    return ScoreArtifact(
        semantics="degree_out",
        candidate_nodes=candidates,
        scores=scores,
        ranking=_stable_ranking(candidates, scores),
        source_rr_count=0,
        metadata={
            "source": "directed_graph",
            "matches_opengu_degree_axis": "edge_index_source_count",
            "budget_dependent": False,
            "top_k_im_guarantee": False,
        },
    )


def random_selection(
    candidate_nodes: Sequence[int],
    budget: int,
    seed: int,
) -> SelectionArtifact:
    candidates = np.asarray(candidate_nodes, dtype=np.int64).reshape(-1)
    budget = int(budget)
    if candidates.size != np.unique(candidates).size:
        raise ValueError("candidate_nodes must be unique")
    if not 1 <= budget <= candidates.size:
        raise ValueError("budget must be in [1, candidate_count]")
    rng = np.random.default_rng(int(seed))
    selected = rng.choice(candidates, size=budget, replace=False)
    return SelectionArtifact(
        algorithm="random",
        selected_nodes=selected,
        accepted_gains=np.zeros(budget, dtype=np.float64),
        budget=budget,
        source_rr_count=0,
        metadata={
            "selection_semantics": "uniform_without_replacement",
            "random_seed": int(seed),
        },
    )
