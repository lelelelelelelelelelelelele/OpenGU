"""Gate 3 read-only old/new comparison policy contracts."""

from __future__ import annotations

import hashlib

import numpy as np
import pytest

from cache_v2.errors import ContractValidationError
from cache_v2.formal_artifacts import EvaluationPayload, PredictionPayload, ScorePayload
from cache_v2.store import SelectionPayload
from experiments.artifact_comparison import (
    ComparisonPolicy,
    FormalArtifactBundle,
    FormalArtifactIds,
    ReferenceArtifactBundle,
    ReferenceEvaluation,
    ReferencePrediction,
    ReferenceScore,
    ReferenceSelection,
    compare_artifact_bundle,
    compare_selection,
)


GRAPH_HASH = "a" * 64
CANDIDATE_HASH = "b" * 64
SPLIT_HASH = "c" * 64
SCORE_ID = "score_11111111_22222222"
SELECTION_ID = "sel_33333333_44444444"
PREDICTION_ID = "pred_55555555_66666666"
EVALUATION_ID = "eval_77777777_88888888"


def _formal_bundle(logit_delta=0.0, metric_delta=0.0):
    score = ScorePayload.build(
        ordered_node_ids=[4, 1, 3],
        scores=[0.9, 0.8, 0.2],
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
        score_kind="scores",
    )
    selection = SelectionPayload.build(
        [4, 1],
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
        source_score_artifact_id=SCORE_ID,
    )
    logits = np.array(
        [[2.0, 0.1], [1.5, 0.5], [0.2, 1.4], [0.3, 1.2], [1.1, 0.7], [0.4, 1.0]],
        dtype=np.float32,
    )
    train_mask = np.array([1, 1, 1, 1, 1, 0], dtype=bool)
    retain_mask = train_mask.copy()
    retain_mask[[4, 1]] = False
    prediction = PredictionPayload.build(
        logits_before=logits + np.float32(logit_delta),
        logits_unlearned=logits + np.float32(0.05 + logit_delta),
        logits_retrained=logits - np.float32(0.02 - logit_delta),
        y=np.array([0, 0, 1, 1, 0, 1], dtype=np.int64),
        train_mask=train_mask,
        test_mask=np.array([0, 0, 0, 0, 0, 1], dtype=bool),
        retain_mask=retain_mask,
        selected_nodes=np.array([4, 1], dtype=np.int64),
        class_order=np.array([0, 1], dtype=np.int64),
        graph_fingerprint=GRAPH_HASH,
        split_fingerprint=SPLIT_HASH,
        selection_artifact_id=SELECTION_ID,
        node_id_space="global",
    )
    evaluation = EvaluationPayload.build(
        prediction_artifact_id=PREDICTION_ID,
        graph_fingerprint=GRAPH_HASH,
        metric_name="collateral-core",
        metric_version="v1",
        metrics={"gap": 0.02 + metric_delta, "mean_pred_shift": 0.05},
    )
    return FormalArtifactBundle(score, selection, prediction, evaluation)


def _reference_bundle(score_delta=0.0, logit_delta=0.0, metric_delta=0.0):
    formal = _formal_bundle()
    return ReferenceArtifactBundle(
        score=ReferenceScore(
            reference_id="legacy-score-fixture",
            ordered_node_ids=[4, 1, 3],
            scores=np.array([0.9 + score_delta, 0.8, 0.2]),
            graph_fingerprint=GRAPH_HASH,
            candidate_set_hash=CANDIDATE_HASH,
            node_id_space="global",
        ),
        selection=ReferenceSelection(
            reference_id="legacy-selection-fixture",
            selected_nodes_ordered=[4, 1],
            graph_fingerprint=GRAPH_HASH,
            candidate_set_hash=CANDIDATE_HASH,
            node_id_space="global",
        ),
        prediction=ReferencePrediction(
            reference_id="legacy-prediction-fixture",
            logits_before=formal.prediction.logits_before + logit_delta,
            logits_unlearned=formal.prediction.logits_unlearned + logit_delta,
            logits_retrained=formal.prediction.logits_retrained + logit_delta,
            y=formal.prediction.y,
            train_mask=formal.prediction.train_mask,
            test_mask=formal.prediction.test_mask,
            retain_mask=formal.prediction.retain_mask,
            selected_nodes=formal.prediction.selected_nodes,
            class_order=formal.prediction.class_order,
            graph_fingerprint=GRAPH_HASH,
            split_fingerprint=SPLIT_HASH,
            node_id_space="global",
        ),
        evaluation=ReferenceEvaluation(
            reference_id="legacy-evaluation-fixture",
            metrics={"gap": 0.02 + metric_delta, "mean_pred_shift": 0.05},
            graph_fingerprint=GRAPH_HASH,
            metric_name="collateral-core",
            metric_version="v1",
        ),
    )


def _ids():
    return FormalArtifactIds(
        score=SCORE_ID,
        selection=SELECTION_ID,
        prediction=PREDICTION_ID,
        evaluation=EVALUATION_ID,
    )


def test_four_artifact_bundle_passes_only_with_declared_float_tolerances():
    policy = ComparisonPolicy.from_atol(
        score_atol=1e-6,
        prediction_atol=1e-6,
        evaluation_atol=1e-6,
    )
    report = compare_artifact_bundle(
        _reference_bundle(score_delta=5e-7, logit_delta=5e-7, metric_delta=5e-7),
        _formal_bundle(),
        _ids(),
        policy,
    )

    assert report.passed is True
    assert report.status == "passed"
    assert [item.artifact_type for item in report.results] == [
        "score",
        "selection",
        "prediction",
        "evaluation",
    ]
    assert report.to_dict()["policy"]["prediction"] == {"atol": 1e-6, "rtol": 0.0}
    assert report.canonical_json == report.canonical_json
    assert report.report_hash == hashlib.sha256(
        report.canonical_json.encode("utf-8")
    ).hexdigest()


def test_selection_requires_ordered_exact_match_not_set_or_jaccard_similarity():
    reference = ReferenceSelection(
        reference_id="legacy-selection",
        selected_nodes_ordered=[1, 4],
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
    )
    result = compare_selection(reference, _formal_bundle().selection)

    assert result.passed is False
    assert result.details["ordered_exact"] is False
    assert result.details["set_exact"] is True
    assert result.details["jaccard"] == 1.0
    assert "ordered_nodes_mismatch" in result.reasons


def test_known_im_overlap_shape_remains_a_gate3_failure():
    legacy_nodes = list(range(1354))
    v2_nodes = list(range(1252)) + list(range(2000, 2102))
    reference = ReferenceSelection(
        reference_id="legacy-ogbn-arxiv-im-known-mismatch",
        selected_nodes_ordered=legacy_nodes,
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
    )
    formal = SelectionPayload.build(
        v2_nodes,
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
    )
    result = compare_selection(reference, formal)

    assert result.passed is False
    assert result.details["intersection_count"] == 1252
    assert result.details["reference_only_count"] == 102
    assert result.details["formal_only_count"] == 102
    assert result.details["jaccard"] == pytest.approx(1252 / 1456)


def test_prediction_and_evaluation_above_tolerance_fail_closed():
    report = compare_artifact_bundle(
        _reference_bundle(logit_delta=2e-6, metric_delta=2e-6),
        _formal_bundle(),
        _ids(),
        ComparisonPolicy.from_atol(1e-6, 1e-6, 1e-6),
    )

    assert report.passed is False
    by_type = {item.artifact_type: item for item in report.results}
    assert "logits_before_float_mismatch" in by_type["prediction"].reasons
    assert "metric_value_mismatch" in by_type["evaluation"].reasons
    assert by_type["prediction"].details["logits_before"]["max_abs_diff"] > 1e-6


def test_missing_provenance_and_metric_key_mismatch_fail_closed():
    reference = _reference_bundle()
    degraded = ReferenceArtifactBundle(
        score=ReferenceScore(
            reference_id=reference.score.reference_id,
            ordered_node_ids=reference.score.ordered_node_ids,
            scores=reference.score.scores,
            graph_fingerprint=None,
            candidate_set_hash=CANDIDATE_HASH,
            node_id_space="global",
        ),
        selection=reference.selection,
        prediction=reference.prediction,
        evaluation=ReferenceEvaluation(
            reference_id=reference.evaluation.reference_id,
            metrics={"gap": 0.02},
            graph_fingerprint=GRAPH_HASH,
            metric_name="collateral-core",
            metric_version=None,
        ),
    )
    report = compare_artifact_bundle(
        degraded,
        _formal_bundle(),
        _ids(),
        ComparisonPolicy.from_atol(1e-6, 1e-6, 1e-6),
    )

    assert report.passed is False
    by_type = {item.artifact_type: item for item in report.results}
    assert "reference_graph_fingerprint_missing" in by_type["score"].reasons
    assert "reference_metric_version_missing" in by_type["evaluation"].reasons
    assert "metric_keys_mismatch" in by_type["evaluation"].reasons


def test_non_finite_reference_or_invalid_tolerance_is_rejected():
    with pytest.raises(ContractValidationError, match="finite"):
        ReferenceScore(
            reference_id="bad-score",
            ordered_node_ids=[1],
            scores=[float("nan")],
            graph_fingerprint=GRAPH_HASH,
            candidate_set_hash=CANDIDATE_HASH,
            node_id_space="global",
        )
    with pytest.raises(ContractValidationError, match="tolerance"):
        ComparisonPolicy.from_atol(-1.0, 1e-6, 1e-6)


def test_comparison_harness_does_not_mutate_reference_arrays():
    reference = _reference_bundle()
    arrays = (
        reference.score.scores,
        reference.prediction.logits_before,
        reference.prediction.train_mask,
    )
    before = tuple(hashlib.sha256(value.tobytes()).hexdigest() for value in arrays)
    compare_artifact_bundle(
        reference,
        _formal_bundle(),
        _ids(),
        ComparisonPolicy.from_atol(1e-6, 1e-6, 1e-6),
    )
    after = tuple(hashlib.sha256(value.tobytes()).hexdigest() for value in arrays)

    assert before == after
    assert all(value.flags.writeable is False for value in arrays)


def test_cache_v2_does_not_import_gate3_legacy_comparison_policy():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    for path in (root / "cache_v2").glob("*.py"):
        source = path.read_text(encoding="utf-8").lower()
        assert "artifact_comparison" not in source, path.name
