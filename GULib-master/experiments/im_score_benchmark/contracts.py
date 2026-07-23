"""Typed, JSON-serializable outputs for the IM score benchmark."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence

import numpy as np


def _readonly_vector(values: Sequence[Any], dtype: np.dtype) -> np.ndarray:
    array = np.asarray(values, dtype=dtype).reshape(-1).copy()
    array.setflags(write=False)
    return array


def _json_value(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


@dataclass(frozen=True)
class ApproximationCertificate:
    """A machine-readable quality statement with an explicit proof scope."""

    kind: str
    lower_bound: float
    upper_bound: float
    ratio_lower_bound: float
    target_ratio: float
    failure_probability: float
    met_target: bool
    paper_equivalent: bool
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        values = (
            self.lower_bound,
            self.upper_bound,
            self.ratio_lower_bound,
            self.target_ratio,
            self.failure_probability,
        )
        if not all(np.isfinite(value) for value in values):
            raise ValueError("certificate values must be finite")
        if self.lower_bound < 0.0:
            raise ValueError("certificate lower_bound must be non-negative")
        if self.upper_bound < self.lower_bound:
            raise ValueError("certificate upper_bound must cover lower_bound")
        if not 0.0 <= self.ratio_lower_bound <= 1.0:
            raise ValueError("certificate ratio_lower_bound must be in [0, 1]")
        if not 0.0 <= self.target_ratio <= 1.0:
            raise ValueError("certificate target_ratio must be in [0, 1]")
        if not 0.0 < self.failure_probability < 1.0:
            raise ValueError("certificate failure_probability must be in (0, 1)")
        object.__setattr__(self, "details", dict(self.details))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "lower_bound": float(self.lower_bound),
            "upper_bound": float(self.upper_bound),
            "ratio_lower_bound": float(self.ratio_lower_bound),
            "target_ratio": float(self.target_ratio),
            "failure_probability": float(self.failure_probability),
            "met_target": bool(self.met_target),
            "paper_equivalent": bool(self.paper_equivalent),
            "details": _json_value(self.details),
        }


@dataclass(frozen=True)
class ScoreArtifact:
    """A complete static score vector over one ordered candidate domain."""

    semantics: str
    candidate_nodes: np.ndarray
    scores: np.ndarray
    ranking: np.ndarray
    source_rr_count: int
    budget: Optional[int] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        candidates = _readonly_vector(self.candidate_nodes, np.int64)
        scores = _readonly_vector(self.scores, np.float64)
        ranking = _readonly_vector(self.ranking, np.int64)
        if not self.semantics:
            raise ValueError("score semantics must be non-empty")
        if candidates.size == 0:
            raise ValueError("score artifact candidate domain must be non-empty")
        if candidates.size != np.unique(candidates).size:
            raise ValueError("score artifact candidates must be unique")
        if scores.shape != candidates.shape:
            raise ValueError("score vector must cover every candidate")
        if not np.isfinite(scores).all():
            raise ValueError("score vector must be finite")
        if ranking.shape != candidates.shape:
            raise ValueError("ranking must contain every candidate")
        if set(ranking.tolist()) != set(candidates.tolist()):
            raise ValueError("ranking must be a permutation of candidate nodes")
        if int(self.source_rr_count) < 0:
            raise ValueError("source_rr_count must be non-negative")
        if self.budget is not None and int(self.budget) <= 0:
            raise ValueError("budget must be positive when present")
        object.__setattr__(self, "candidate_nodes", candidates)
        object.__setattr__(self, "scores", scores)
        object.__setattr__(self, "ranking", ranking)
        object.__setattr__(self, "source_rr_count", int(self.source_rr_count))
        object.__setattr__(
            self,
            "budget",
            None if self.budget is None else int(self.budget),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def score_for(self, node_id: int) -> float:
        matches = np.flatnonzero(self.candidate_nodes == int(node_id))
        if matches.size != 1:
            raise KeyError("node is outside the score candidate domain")
        return float(self.scores[int(matches[0])])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "semantics": self.semantics,
            "candidate_nodes": self.candidate_nodes.tolist(),
            "scores": self.scores.tolist(),
            "ranking": self.ranking.tolist(),
            "source_rr_count": int(self.source_rr_count),
            "budget": self.budget,
            "metadata": _json_value(self.metadata),
        }


@dataclass(frozen=True)
class SelectionArtifact:
    """An ordered seed selection and the context needed to interpret it."""

    algorithm: str
    selected_nodes: np.ndarray
    accepted_gains: np.ndarray
    budget: int
    source_rr_count: int
    certificate: Optional[ApproximationCertificate] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        selected = _readonly_vector(self.selected_nodes, np.int64)
        gains = _readonly_vector(self.accepted_gains, np.float64)
        if not self.algorithm:
            raise ValueError("selection algorithm must be non-empty")
        if int(self.budget) <= 0:
            raise ValueError("selection budget must be positive")
        if selected.size != int(self.budget):
            raise ValueError("selected node count must equal budget")
        if selected.size != np.unique(selected).size:
            raise ValueError("selected nodes must be unique")
        if gains.shape != selected.shape:
            raise ValueError("accepted gains must align with selected nodes")
        if not np.isfinite(gains).all() or np.any(gains < 0.0):
            raise ValueError("accepted gains must be finite and non-negative")
        if int(self.source_rr_count) < 0:
            raise ValueError("source_rr_count must be non-negative")
        object.__setattr__(self, "selected_nodes", selected)
        object.__setattr__(self, "accepted_gains", gains)
        object.__setattr__(self, "budget", int(self.budget))
        object.__setattr__(self, "source_rr_count", int(self.source_rr_count))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "selected_nodes": self.selected_nodes.tolist(),
            "accepted_gains": self.accepted_gains.tolist(),
            "budget": int(self.budget),
            "source_rr_count": int(self.source_rr_count),
            "certificate": (
                None if self.certificate is None else self.certificate.to_dict()
            ),
            "metadata": _json_value(self.metadata),
        }
