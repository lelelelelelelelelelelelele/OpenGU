"""Modern influence-maximization selector and score benchmark primitives.

This package is intentionally isolated from the production AttackManager.  It
provides auditable RR-set primitives, typed score/selection outputs, and local
exact fixtures before any formal dataset matrix is authorized.
"""

from .contracts import ApproximationCertificate, ScoreArtifact, SelectionArtifact
from .rr_core import DirectedGraph, RRBundle, sample_rr_bundle
from .score_reducers import build_score_bundle, rr_k_semivalue, rr_shapley, rr_sni
from .selectors import (
    SampleBudgetExceeded,
    corrected_imm_select,
    maximum_coverage_greedy,
    opimc_select,
    select_top_k_score,
)

__all__ = [
    "ApproximationCertificate",
    "DirectedGraph",
    "RRBundle",
    "SampleBudgetExceeded",
    "ScoreArtifact",
    "SelectionArtifact",
    "build_score_bundle",
    "corrected_imm_select",
    "maximum_coverage_greedy",
    "opimc_select",
    "rr_k_semivalue",
    "rr_shapley",
    "rr_sni",
    "sample_rr_bundle",
    "select_top_k_score",
]
