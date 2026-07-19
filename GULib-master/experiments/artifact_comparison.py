"""Read-only Gate 3 semantic comparison for Legacy/reference and V2 payloads.

Reference normalization and equivalence policy belong to the experiment and
migration layer.  Cache V2 remains exact-only and does not import this module.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence, Tuple

import numpy as np

from cache_v2.contracts import validate_artifact_id, validate_sha256
from cache_v2.errors import ContractValidationError
from cache_v2.formal_artifacts import EvaluationPayload, PredictionPayload, ScorePayload
from cache_v2.store import SelectionPayload


COMPARISON_CONTRACT = "opengu-cache-v2-gate3-comparison-v1"


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ContractValidationError("{0} must be a non-empty string".format(label))
    return value.strip()


def _optional_text(value: Any, label: str) -> Optional[str]:
    if value is None:
        return None
    return _required_text(value, label)


def _optional_hash(value: Any, label: str) -> Optional[str]:
    if value is None:
        return None
    return validate_sha256(value, label)


def _freeze_array(value: Any, dtype: np.dtype, label: str) -> np.ndarray:
    try:
        array = np.ascontiguousarray(np.asarray(value), dtype=dtype).copy()
    except (TypeError, ValueError, OverflowError) as exc:
        raise ContractValidationError("{0} cannot be normalized: {1}".format(label, exc))
    array.setflags(write=False)
    return array


def _int_vector(value: Any, label: str) -> np.ndarray:
    raw = np.asarray(value)
    if raw.ndim != 1 or raw.dtype.kind not in "iu":
        raise ContractValidationError(
            "{0} must be a one-dimensional integer array".format(label)
        )
    if raw.dtype.kind == "u" and raw.size and int(raw.max()) > np.iinfo(np.int64).max:
        raise ContractValidationError("{0} contains an integer outside int64".format(label))
    return _freeze_array(raw, np.dtype("<i8"), label)


def _float_array(value: Any, label: str, ndim: int) -> np.ndarray:
    raw = np.asarray(value)
    if raw.ndim != ndim or raw.dtype.kind not in "fiu":
        raise ContractValidationError(
            "{0} must be a {1}-dimensional numeric array".format(label, ndim)
        )
    array = _freeze_array(raw, np.dtype("<f8"), label)
    if not np.isfinite(array).all():
        raise ContractValidationError("{0} must contain only finite values".format(label))
    return array


def _bool_vector(value: Any, label: str) -> np.ndarray:
    raw = np.asarray(value)
    if raw.ndim != 1 or raw.dtype.kind != "b":
        raise ContractValidationError(
            "{0} must be a one-dimensional boolean array".format(label)
        )
    return _freeze_array(raw, np.dtype("|b1"), label)


def _unique_nodes(array: np.ndarray, label: str) -> None:
    if len(set(int(item) for item in array)) != len(array):
        raise ContractValidationError("{0} contains duplicate nodes".format(label))


def _flat_metrics(value: Any, label: str) -> Dict[str, float]:
    if not isinstance(value, Mapping) or not value:
        raise ContractValidationError("{0} must be a non-empty mapping".format(label))
    result: Dict[str, float] = {}
    for raw_key, raw_value in value.items():
        key = _required_text(raw_key, "{0} key".format(label))
        if key in result:
            raise ContractValidationError("{0} has duplicate metric keys".format(label))
        if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
            raise ContractValidationError(
                "{0}.{1} must be a numeric scalar".format(label, key)
            )
        number = float(raw_value)
        if not math.isfinite(number):
            raise ContractValidationError(
                "{0}.{1} must be finite".format(label, key)
            )
        result[key] = number
    return {key: result[key] for key in sorted(result)}


@dataclass(frozen=True)
class FloatTolerance:
    atol: float = 1e-6
    rtol: float = 0.0

    def __post_init__(self) -> None:
        for name in ("atol", "rtol"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ContractValidationError("float tolerance must be numeric")
            normalized = float(value)
            if not math.isfinite(normalized) or normalized < 0:
                raise ContractValidationError(
                    "float tolerance must be finite and non-negative"
                )
            object.__setattr__(self, name, normalized)

    def to_dict(self) -> Dict[str, float]:
        return {"atol": self.atol, "rtol": self.rtol}


@dataclass(frozen=True)
class ComparisonPolicy:
    score: FloatTolerance
    prediction: FloatTolerance
    evaluation: FloatTolerance

    def __post_init__(self) -> None:
        for name in ("score", "prediction", "evaluation"):
            if not isinstance(getattr(self, name), FloatTolerance):
                raise ContractValidationError(
                    "{0} policy must be FloatTolerance".format(name)
                )

    @classmethod
    def from_atol(
        cls,
        score_atol: float,
        prediction_atol: float,
        evaluation_atol: float,
    ) -> "ComparisonPolicy":
        return cls(
            score=FloatTolerance(score_atol, 0.0),
            prediction=FloatTolerance(prediction_atol, 0.0),
            evaluation=FloatTolerance(evaluation_atol, 0.0),
        )

    def to_dict(self) -> Dict[str, Dict[str, float]]:
        return {
            "score": self.score.to_dict(),
            "prediction": self.prediction.to_dict(),
            "evaluation": self.evaluation.to_dict(),
        }


@dataclass(frozen=True)
class ReferenceScore:
    reference_id: str
    ordered_node_ids: Sequence[int]
    scores: Optional[Any]
    graph_fingerprint: Optional[str]
    candidate_set_hash: Optional[str]
    node_id_space: Optional[str]

    def __post_init__(self) -> None:
        nodes = _int_vector(self.ordered_node_ids, "reference Score ordered_node_ids")
        _unique_nodes(nodes, "reference Score ordered_node_ids")
        scores = self.scores
        if scores is not None:
            scores = _float_array(scores, "reference Score scores", 1)
            if scores.shape != nodes.shape:
                raise ContractValidationError(
                    "reference Score scores must match ordered_node_ids"
                )
        object.__setattr__(self, "reference_id", _required_text(self.reference_id, "reference_id"))
        object.__setattr__(self, "ordered_node_ids", nodes)
        object.__setattr__(self, "scores", scores)
        object.__setattr__(self, "graph_fingerprint", _optional_hash(self.graph_fingerprint, "reference graph_fingerprint"))
        object.__setattr__(self, "candidate_set_hash", _optional_hash(self.candidate_set_hash, "reference candidate_set_hash"))
        object.__setattr__(self, "node_id_space", _optional_text(self.node_id_space, "reference node_id_space"))


@dataclass(frozen=True)
class ReferenceSelection:
    reference_id: str
    selected_nodes_ordered: Sequence[int]
    graph_fingerprint: Optional[str]
    candidate_set_hash: Optional[str]
    node_id_space: Optional[str]

    def __post_init__(self) -> None:
        nodes = _int_vector(
            self.selected_nodes_ordered, "reference Selection selected_nodes_ordered"
        )
        _unique_nodes(nodes, "reference Selection selected_nodes_ordered")
        object.__setattr__(self, "reference_id", _required_text(self.reference_id, "reference_id"))
        object.__setattr__(self, "selected_nodes_ordered", nodes)
        object.__setattr__(self, "graph_fingerprint", _optional_hash(self.graph_fingerprint, "reference graph_fingerprint"))
        object.__setattr__(self, "candidate_set_hash", _optional_hash(self.candidate_set_hash, "reference candidate_set_hash"))
        object.__setattr__(self, "node_id_space", _optional_text(self.node_id_space, "reference node_id_space"))


@dataclass(frozen=True)
class ReferencePrediction:
    reference_id: str
    logits_before: Any
    logits_unlearned: Any
    logits_retrained: Any
    y: Any
    train_mask: Any
    test_mask: Any
    retain_mask: Any
    selected_nodes: Any
    class_order: Any
    graph_fingerprint: Optional[str]
    split_fingerprint: Optional[str]
    node_id_space: Optional[str]

    def __post_init__(self) -> None:
        before = _float_array(self.logits_before, "reference logits_before", 2)
        unlearned = _float_array(self.logits_unlearned, "reference logits_unlearned", 2)
        retrained = _float_array(self.logits_retrained, "reference logits_retrained", 2)
        if before.shape != unlearned.shape or before.shape != retrained.shape:
            raise ContractValidationError("reference Prediction logits shapes must match")
        labels = _int_vector(self.y, "reference y")
        train = _bool_vector(self.train_mask, "reference train_mask")
        test = _bool_vector(self.test_mask, "reference test_mask")
        retain = _bool_vector(self.retain_mask, "reference retain_mask")
        selected = _int_vector(self.selected_nodes, "reference selected_nodes")
        classes = _int_vector(self.class_order, "reference class_order")
        num_nodes, num_classes = before.shape
        if any(array.shape != (num_nodes,) for array in (labels, train, test, retain)):
            raise ContractValidationError(
                "reference labels and masks must match logits rows"
            )
        if classes.shape != (num_classes,):
            raise ContractValidationError(
                "reference class_order must match logits columns"
            )
        _unique_nodes(selected, "reference selected_nodes")
        _unique_nodes(classes, "reference class_order")
        if any(int(node) < 0 or int(node) >= num_nodes for node in selected):
            raise ContractValidationError("reference selected_nodes is out of range")
        if not set(int(item) for item in labels).issubset(
            set(int(item) for item in classes)
        ):
            raise ContractValidationError("reference y is outside class_order")
        expected_retain = np.array(train, copy=True)
        expected_retain[selected] = False
        if not np.array_equal(retain, expected_retain):
            raise ContractValidationError(
                "reference retain_mask must equal train_mask minus selected_nodes"
            )
        for name, value in (
            ("logits_before", before),
            ("logits_unlearned", unlearned),
            ("logits_retrained", retrained),
            ("y", labels),
            ("train_mask", train),
            ("test_mask", test),
            ("retain_mask", retain),
            ("selected_nodes", selected),
            ("class_order", classes),
        ):
            object.__setattr__(self, name, value)
        object.__setattr__(self, "reference_id", _required_text(self.reference_id, "reference_id"))
        object.__setattr__(self, "graph_fingerprint", _optional_hash(self.graph_fingerprint, "reference graph_fingerprint"))
        object.__setattr__(self, "split_fingerprint", _optional_hash(self.split_fingerprint, "reference split_fingerprint"))
        object.__setattr__(self, "node_id_space", _optional_text(self.node_id_space, "reference node_id_space"))


@dataclass(frozen=True)
class ReferenceEvaluation:
    reference_id: str
    metrics: Mapping[str, Any]
    graph_fingerprint: Optional[str]
    metric_name: Optional[str]
    metric_version: Optional[str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "reference_id", _required_text(self.reference_id, "reference_id"))
        object.__setattr__(self, "metrics", _flat_metrics(self.metrics, "reference metrics"))
        object.__setattr__(self, "graph_fingerprint", _optional_hash(self.graph_fingerprint, "reference graph_fingerprint"))
        object.__setattr__(self, "metric_name", _optional_text(self.metric_name, "reference metric_name"))
        object.__setattr__(self, "metric_version", _optional_text(self.metric_version, "reference metric_version"))


@dataclass(frozen=True)
class ReferenceArtifactBundle:
    score: ReferenceScore
    selection: ReferenceSelection
    prediction: ReferencePrediction
    evaluation: ReferenceEvaluation

    def __post_init__(self) -> None:
        expected = (
            (self.score, ReferenceScore),
            (self.selection, ReferenceSelection),
            (self.prediction, ReferencePrediction),
            (self.evaluation, ReferenceEvaluation),
        )
        if any(not isinstance(value, kind) for value, kind in expected):
            raise ContractValidationError("reference bundle has a wrong component type")


@dataclass(frozen=True)
class FormalArtifactBundle:
    score: ScorePayload
    selection: SelectionPayload
    prediction: PredictionPayload
    evaluation: EvaluationPayload

    def __post_init__(self) -> None:
        expected = (
            (self.score, ScorePayload),
            (self.selection, SelectionPayload),
            (self.prediction, PredictionPayload),
            (self.evaluation, EvaluationPayload),
        )
        if any(not isinstance(value, kind) for value, kind in expected):
            raise ContractValidationError("formal bundle has a wrong payload type")


@dataclass(frozen=True)
class FormalArtifactIds:
    score: str
    selection: str
    prediction: str
    evaluation: str

    def __post_init__(self) -> None:
        prefixes = {
            "score": "score_",
            "selection": "sel_",
            "prediction": "pred_",
            "evaluation": "eval_",
        }
        for name, prefix in prefixes.items():
            value = validate_artifact_id(getattr(self, name), name)
            if not value.startswith(prefix):
                raise ContractValidationError(
                    "{0} does not identify the expected Artifact type".format(name)
                )
            object.__setattr__(self, name, value)

    def to_dict(self) -> Dict[str, str]:
        return {
            "score": self.score,
            "selection": self.selection,
            "prediction": self.prediction,
            "evaluation": self.evaluation,
        }


@dataclass(frozen=True)
class ArtifactComparisonResult:
    artifact_type: str
    passed: bool
    reasons: Tuple[str, ...]
    details: Mapping[str, Any]

    def __post_init__(self) -> None:
        artifact_type = _required_text(self.artifact_type, "artifact_type")
        if artifact_type not in ("score", "selection", "prediction", "evaluation"):
            raise ContractValidationError("unsupported comparison Artifact type")
        reasons = tuple(_required_text(item, "comparison reason") for item in self.reasons)
        if len(set(reasons)) != len(reasons):
            raise ContractValidationError("comparison reasons contain duplicates")
        if bool(self.passed) != (len(reasons) == 0):
            raise ContractValidationError("comparison passed flag disagrees with reasons")
        details = copy.deepcopy(dict(self.details))
        try:
            json.dumps(details, allow_nan=False, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ContractValidationError("comparison details are not JSON-safe: {0}".format(exc))
        object.__setattr__(self, "artifact_type", artifact_type)
        object.__setattr__(self, "passed", bool(self.passed))
        object.__setattr__(self, "reasons", reasons)
        object.__setattr__(self, "details", details)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "passed": self.passed,
            "reasons": list(self.reasons),
            "details": copy.deepcopy(dict(self.details)),
        }


@dataclass(frozen=True)
class Gate3ComparisonReport:
    reference_ids: Mapping[str, str]
    formal_artifact_ids: FormalArtifactIds
    policy: ComparisonPolicy
    results: Tuple[ArtifactComparisonResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.formal_artifact_ids, FormalArtifactIds):
            raise ContractValidationError("formal_artifact_ids must be FormalArtifactIds")
        if not isinstance(self.policy, ComparisonPolicy):
            raise ContractValidationError("policy must be ComparisonPolicy")
        reference_ids = dict(self.reference_ids)
        if set(reference_ids) != {"score", "selection", "prediction", "evaluation"}:
            raise ContractValidationError("reference_ids must cover all four Artifacts")
        reference_ids = {
            key: _required_text(reference_ids[key], "reference_id")
            for key in ("score", "selection", "prediction", "evaluation")
        }
        results = tuple(self.results)
        if [item.artifact_type for item in results] != [
            "score",
            "selection",
            "prediction",
            "evaluation",
        ]:
            raise ContractValidationError("results must cover all four Artifacts in order")
        object.__setattr__(self, "reference_ids", reference_ids)
        object.__setattr__(self, "results", results)

    @property
    def passed(self) -> bool:
        return all(item.passed for item in self.results)

    @property
    def status(self) -> str:
        return "passed" if self.passed else "failed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "comparison_contract": COMPARISON_CONTRACT,
            "status": self.status,
            "passed": self.passed,
            "policy": self.policy.to_dict(),
            "reference_ids": dict(self.reference_ids),
            "formal_artifact_ids": self.formal_artifact_ids.to_dict(),
            "results": [item.to_dict() for item in self.results],
        }

    @property
    def canonical_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @property
    def report_hash(self) -> str:
        return hashlib.sha256(self.canonical_json.encode("utf-8")).hexdigest()


def _add_identity_comparison(
    reasons: list,
    details: Dict[str, Any],
    name: str,
    reference: Optional[str],
    formal: str,
) -> None:
    if reference is None:
        details[name] = {
            "exact": False,
            "reference": None,
            "formal": formal,
        }
        reasons.append("reference_{0}_missing".format(name))
    else:
        exact = reference == formal
        details[name] = {
            "exact": exact,
            "reference": reference,
            "formal": formal,
        }
        if not exact:
            reasons.append("{0}_mismatch".format(name))


def _set_overlap(reference: np.ndarray, formal: np.ndarray) -> Dict[str, Any]:
    reference_set = set(int(item) for item in reference)
    formal_set = set(int(item) for item in formal)
    intersection = len(reference_set.intersection(formal_set))
    union = len(reference_set.union(formal_set))
    reference_bytes = json.dumps(
        [int(item) for item in reference], separators=(",", ":")
    ).encode("utf-8")
    formal_bytes = json.dumps(
        [int(item) for item in formal], separators=(",", ":")
    ).encode("utf-8")
    return {
        "ordered_exact": bool(np.array_equal(reference, formal)),
        "set_exact": reference_set == formal_set,
        "reference_ordered_hash": hashlib.sha256(reference_bytes).hexdigest(),
        "formal_ordered_hash": hashlib.sha256(formal_bytes).hexdigest(),
        "reference_count": len(reference),
        "formal_count": len(formal),
        "intersection_count": intersection,
        "reference_only_count": len(reference_set.difference(formal_set)),
        "formal_only_count": len(formal_set.difference(reference_set)),
        "jaccard": 1.0 if union == 0 else float(intersection / union),
    }


def _float_comparison(
    reference: np.ndarray, formal: np.ndarray, tolerance: FloatTolerance
) -> Dict[str, Any]:
    if reference.shape != formal.shape:
        return {
            "shape_exact": False,
            "reference_shape": list(reference.shape),
            "formal_shape": list(formal.shape),
            "mismatch_count": None,
            "max_abs_diff": None,
            "within_tolerance": False,
        }
    reference64 = np.asarray(reference, dtype=np.float64)
    formal64 = np.asarray(formal, dtype=np.float64)
    absolute = np.abs(reference64 - formal64)
    close = np.isclose(
        reference64,
        formal64,
        atol=tolerance.atol,
        rtol=tolerance.rtol,
        equal_nan=False,
    )
    return {
        "shape_exact": True,
        "reference_shape": list(reference.shape),
        "formal_shape": list(formal.shape),
        "mismatch_count": int(np.size(close) - np.count_nonzero(close)),
        "max_abs_diff": 0.0 if absolute.size == 0 else float(absolute.max()),
        "within_tolerance": bool(close.all()),
    }


def compare_score(
    reference: ReferenceScore,
    formal: ScorePayload,
    tolerance: FloatTolerance,
) -> ArtifactComparisonResult:
    if not isinstance(reference, ReferenceScore) or not isinstance(formal, ScorePayload):
        raise ContractValidationError("compare_score requires normalized Score values")
    if not isinstance(tolerance, FloatTolerance):
        raise ContractValidationError("score tolerance must be FloatTolerance")
    reasons = []
    details: Dict[str, Any] = {}
    _add_identity_comparison(reasons, details, "graph_fingerprint", reference.graph_fingerprint, formal.graph_fingerprint)
    _add_identity_comparison(reasons, details, "candidate_set_hash", reference.candidate_set_hash, formal.candidate_set_hash)
    _add_identity_comparison(reasons, details, "node_id_space", reference.node_id_space, formal.node_id_space)
    overlap = _set_overlap(reference.ordered_node_ids, formal.ordered_node_ids)
    details.update(overlap)
    if not overlap["ordered_exact"]:
        reasons.append("ordered_nodes_mismatch")
    presence_exact = (reference.scores is None) == (formal.scores is None)
    details["score_presence_exact"] = presence_exact
    if not presence_exact:
        reasons.append("score_presence_mismatch")
    elif reference.scores is not None and formal.scores is not None:
        score_details = _float_comparison(reference.scores, formal.scores, tolerance)
        details["scores"] = score_details
        if not score_details["within_tolerance"]:
            reasons.append("score_values_float_mismatch")
    return ArtifactComparisonResult("score", not reasons, tuple(reasons), details)


def compare_selection(
    reference: ReferenceSelection, formal: SelectionPayload
) -> ArtifactComparisonResult:
    if not isinstance(reference, ReferenceSelection) or not isinstance(
        formal, SelectionPayload
    ):
        raise ContractValidationError(
            "compare_selection requires normalized Selection values"
        )
    reasons = []
    details: Dict[str, Any] = {}
    _add_identity_comparison(reasons, details, "graph_fingerprint", reference.graph_fingerprint, formal.graph_fingerprint)
    _add_identity_comparison(reasons, details, "candidate_set_hash", reference.candidate_set_hash, formal.candidate_set_hash)
    _add_identity_comparison(reasons, details, "node_id_space", reference.node_id_space, formal.node_id_space)
    overlap = _set_overlap(
        reference.selected_nodes_ordered,
        np.asarray(formal.selected_nodes_ordered, dtype=np.int64),
    )
    details.update(overlap)
    if not overlap["ordered_exact"]:
        reasons.append("ordered_nodes_mismatch")
    return ArtifactComparisonResult("selection", not reasons, tuple(reasons), details)


def _exact_array(
    reasons: list,
    details: Dict[str, Any],
    name: str,
    reference: np.ndarray,
    formal: np.ndarray,
) -> None:
    exact = bool(np.array_equal(reference, formal))
    details[name] = {
        "exact": exact,
        "reference_shape": list(reference.shape),
        "formal_shape": list(formal.shape),
    }
    if not exact:
        reasons.append("{0}_mismatch".format(name))


def compare_prediction(
    reference: ReferencePrediction,
    formal: PredictionPayload,
    tolerance: FloatTolerance,
) -> ArtifactComparisonResult:
    if not isinstance(reference, ReferencePrediction) or not isinstance(
        formal, PredictionPayload
    ):
        raise ContractValidationError(
            "compare_prediction requires normalized Prediction values"
        )
    if not isinstance(tolerance, FloatTolerance):
        raise ContractValidationError("prediction tolerance must be FloatTolerance")
    reasons = []
    details: Dict[str, Any] = {}
    _add_identity_comparison(reasons, details, "graph_fingerprint", reference.graph_fingerprint, formal.graph_fingerprint)
    _add_identity_comparison(reasons, details, "split_fingerprint", reference.split_fingerprint, formal.split_fingerprint)
    _add_identity_comparison(reasons, details, "node_id_space", reference.node_id_space, formal.node_id_space)
    for name in ("y", "train_mask", "test_mask", "retain_mask", "selected_nodes", "class_order"):
        _exact_array(reasons, details, name, getattr(reference, name), getattr(formal, name))
    for name in ("logits_before", "logits_unlearned", "logits_retrained"):
        float_details = _float_comparison(
            getattr(reference, name), getattr(formal, name), tolerance
        )
        details[name] = float_details
        if not float_details["within_tolerance"]:
            reasons.append("{0}_float_mismatch".format(name))
    return ArtifactComparisonResult("prediction", not reasons, tuple(reasons), details)


def compare_evaluation(
    reference: ReferenceEvaluation,
    formal: EvaluationPayload,
    tolerance: FloatTolerance,
) -> ArtifactComparisonResult:
    if not isinstance(reference, ReferenceEvaluation) or not isinstance(
        formal, EvaluationPayload
    ):
        raise ContractValidationError(
            "compare_evaluation requires normalized Evaluation values"
        )
    if not isinstance(tolerance, FloatTolerance):
        raise ContractValidationError("evaluation tolerance must be FloatTolerance")
    reasons = []
    details: Dict[str, Any] = {}
    _add_identity_comparison(reasons, details, "graph_fingerprint", reference.graph_fingerprint, formal.graph_fingerprint)
    _add_identity_comparison(reasons, details, "metric_name", reference.metric_name, formal.metric_name)
    _add_identity_comparison(reasons, details, "metric_version", reference.metric_version, formal.metric_version)
    try:
        formal_metrics = _flat_metrics(formal.metrics, "formal metrics")
    except ContractValidationError as exc:
        raise ContractValidationError(
            "formal Evaluation metrics are not Gate 3 scalar metrics: {0}".format(exc)
        )
    reference_keys = sorted(reference.metrics)
    formal_keys = sorted(formal_metrics)
    keys_exact = reference_keys == formal_keys
    details["metric_keys_exact"] = keys_exact
    details["reference_metric_keys"] = reference_keys
    details["formal_metric_keys"] = formal_keys
    if not keys_exact:
        reasons.append("metric_keys_mismatch")
    metric_details: Dict[str, Any] = {}
    any_mismatch = False
    for key in sorted(set(reference_keys).intersection(formal_keys)):
        compared = _float_comparison(
            np.asarray([reference.metrics[key]], dtype=np.float64),
            np.asarray([formal_metrics[key]], dtype=np.float64),
            tolerance,
        )
        compared["reference_value"] = reference.metrics[key]
        compared["formal_value"] = formal_metrics[key]
        metric_details[key] = compared
        any_mismatch = any_mismatch or not compared["within_tolerance"]
    details["metrics"] = metric_details
    if any_mismatch:
        reasons.append("metric_value_mismatch")
    return ArtifactComparisonResult("evaluation", not reasons, tuple(reasons), details)


def _validate_formal_bundle_identity(
    bundle: FormalArtifactBundle, ids: FormalArtifactIds
) -> None:
    if bundle.selection.source_score_artifact_id != ids.score:
        raise ContractValidationError(
            "formal Selection does not identify the compared Score Artifact"
        )
    if bundle.prediction.selection_artifact_id != ids.selection:
        raise ContractValidationError(
            "formal Prediction does not identify the compared Selection Artifact"
        )
    if bundle.evaluation.prediction_artifact_id != ids.prediction:
        raise ContractValidationError(
            "formal Evaluation does not identify the compared Prediction Artifact"
        )
    graph_values = {
        bundle.score.graph_fingerprint,
        bundle.selection.graph_fingerprint,
        bundle.prediction.graph_fingerprint,
        bundle.evaluation.graph_fingerprint,
    }
    if len(graph_values) != 1:
        raise ContractValidationError("formal bundle graph identities disagree")
    if bundle.score.candidate_set_hash != bundle.selection.candidate_set_hash:
        raise ContractValidationError("formal Score/Selection candidate identities disagree")
    if tuple(int(item) for item in bundle.prediction.selected_nodes) != tuple(
        int(item) for item in bundle.selection.selected_nodes_ordered
    ):
        raise ContractValidationError(
            "formal Prediction selected_nodes do not match Selection payload"
        )


def compare_artifact_bundle(
    reference: ReferenceArtifactBundle,
    formal: FormalArtifactBundle,
    formal_artifact_ids: FormalArtifactIds,
    policy: ComparisonPolicy,
) -> Gate3ComparisonReport:
    if not isinstance(reference, ReferenceArtifactBundle):
        raise ContractValidationError("reference must be ReferenceArtifactBundle")
    if not isinstance(formal, FormalArtifactBundle):
        raise ContractValidationError("formal must be FormalArtifactBundle")
    if not isinstance(formal_artifact_ids, FormalArtifactIds):
        raise ContractValidationError("formal_artifact_ids must be FormalArtifactIds")
    if not isinstance(policy, ComparisonPolicy):
        raise ContractValidationError("policy must be ComparisonPolicy")
    _validate_formal_bundle_identity(formal, formal_artifact_ids)
    results = (
        compare_score(reference.score, formal.score, policy.score),
        compare_selection(reference.selection, formal.selection),
        compare_prediction(reference.prediction, formal.prediction, policy.prediction),
        compare_evaluation(reference.evaluation, formal.evaluation, policy.evaluation),
    )
    reference_ids = {
        "score": reference.score.reference_id,
        "selection": reference.selection.reference_id,
        "prediction": reference.prediction.reference_id,
        "evaluation": reference.evaluation.reference_id,
    }
    return Gate3ComparisonReport(
        reference_ids=reference_ids,
        formal_artifact_ids=formal_artifact_ids,
        policy=policy,
        results=results,
    )


__all__ = [
    "COMPARISON_CONTRACT",
    "ArtifactComparisonResult",
    "ComparisonPolicy",
    "FloatTolerance",
    "FormalArtifactBundle",
    "FormalArtifactIds",
    "Gate3ComparisonReport",
    "ReferenceArtifactBundle",
    "ReferenceEvaluation",
    "ReferencePrediction",
    "ReferenceScore",
    "ReferenceSelection",
    "compare_artifact_bundle",
    "compare_evaluation",
    "compare_prediction",
    "compare_score",
    "compare_selection",
]
