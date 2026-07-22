"""Full-candidate score reducers derived from one RR bundle."""

from __future__ import annotations

import math
from typing import Dict, Iterable

import numpy as np

from .contracts import ScoreArtifact
from .rr_core import RRBundle


def _stable_ranking(candidate_nodes: np.ndarray, scores: np.ndarray) -> np.ndarray:
    order = np.lexsort((candidate_nodes, -scores))
    return candidate_nodes[order].astype(np.int64, copy=False)


def _artifact(
    bundle: RRBundle,
    *,
    semantics: str,
    scores: np.ndarray,
    budget: int = None,
    metadata: Dict[str, object] = None,
) -> ScoreArtifact:
    return ScoreArtifact(
        semantics=semantics,
        candidate_nodes=bundle.candidate_nodes,
        scores=scores,
        ranking=_stable_ranking(bundle.candidate_nodes, scores),
        source_rr_count=bundle.rr_count,
        budget=budget,
        metadata={
            "estimator": "reverse_reachable",
            "root_domain_size": bundle.root_domain_size,
            "total_incidences": bundle.total_incidences,
            **({} if metadata is None else metadata),
        },
    )


def rr_sni(bundle: RRBundle) -> ScoreArtifact:
    """Estimate singleton influence for every candidate.

    The estimate is n/theta times the number of sampled RR sets containing the
    candidate.
    """

    scale = float(bundle.num_nodes) / float(bundle.rr_count)
    scores = bundle.incidence_counts().astype(np.float64) * scale
    return _artifact(
        bundle,
        semantics="rr_singleton_influence",
        scores=scores,
        metadata={
            "budget_dependent": False,
            "top_k_im_guarantee": False,
        },
    )


def rr_shapley(bundle: RRBundle) -> ScoreArtifact:
    """Estimate candidate-restricted influence Shapley values."""

    scores = np.zeros(bundle.candidate_count, dtype=np.float64)
    for rr_index in range(bundle.rr_count):
        row = bundle.local_row(rr_index)
        if row.size:
            scores[row] += 1.0 / float(row.size)
    scores *= float(bundle.num_nodes) / float(bundle.rr_count)
    return _artifact(
        bundle,
        semantics="rr_candidate_restricted_shapley",
        scores=scores,
        metadata={
            "budget_dependent": False,
            "top_k_im_guarantee": False,
            "empty_candidate_rr_sets_contribute": 0.0,
        },
    )


def _coalition_avoidance_probability(
    candidate_count: int,
    rr_candidate_count: int,
    budget: int,
) -> float:
    """Probability that k-1 sampled co-players avoid the RR candidate set."""

    choose = int(budget) - 1
    if choose == 0:
        return 1.0
    outside = int(candidate_count) - int(rr_candidate_count)
    available = int(candidate_count) - 1
    if choose < 0 or choose > available or choose > outside:
        return 0.0
    log_probability = (
        math.lgamma(outside + 1)
        - math.lgamma(choose + 1)
        - math.lgamma(outside - choose + 1)
        - math.lgamma(available + 1)
        + math.lgamma(choose + 1)
        + math.lgamma(available - choose + 1)
    )
    return float(math.exp(min(0.0, log_probability)))


def rr_k_semivalue(bundle: RRBundle, budget: int) -> ScoreArtifact:
    """Estimate expected marginal contribution at coalition size k-1."""

    budget = int(budget)
    if not 1 <= budget <= bundle.candidate_count:
        raise ValueError("budget must be in [1, candidate_count]")
    scores = np.zeros(bundle.candidate_count, dtype=np.float64)
    weight_by_row_size: Dict[int, float] = {}
    for rr_index in range(bundle.rr_count):
        row = bundle.local_row(rr_index)
        row_size = int(row.size)
        if row_size == 0:
            continue
        if row_size not in weight_by_row_size:
            weight_by_row_size[row_size] = _coalition_avoidance_probability(
                bundle.candidate_count,
                row_size,
                budget,
            )
        scores[row] += weight_by_row_size[row_size]
    scores *= float(bundle.num_nodes) / float(bundle.rr_count)
    return _artifact(
        bundle,
        semantics="rr_budget_conditioned_semivalue",
        scores=scores,
        budget=budget,
        metadata={
            "budget_dependent": True,
            "coalition_size": budget - 1,
            "top_k_im_guarantee": False,
            "formula_status": "project_derived_exact_tiny_required",
        },
    )


def build_score_bundle(
    bundle: RRBundle,
    budgets: Iterable[int],
) -> Dict[str, ScoreArtifact]:
    """Build SNI, Shapley, and one k-semivalue artifact per budget."""

    result = {
        "rr_sni": rr_sni(bundle),
        "rr_shapley": rr_shapley(bundle),
    }
    for budget in sorted({int(value) for value in budgets}):
        result["rr_ksemivalue_k{0}".format(budget)] = rr_k_semivalue(
            bundle,
            budget,
        )
    return result
