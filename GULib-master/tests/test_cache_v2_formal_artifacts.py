"""Gate 2 contracts for formal Score, Prediction, and Evaluation Artifacts."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import zipfile
from io import BytesIO
from pathlib import Path

import numpy as np
import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion
from cache_v2.formal_artifacts import (
    EvaluationPayload,
    PredictionPayload,
    ScorePayload,
    build_evaluation_recipe,
    build_prediction_recipe,
    build_score_recipe,
)
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.store import (
    ArtifactConflictError,
    ArtifactIntegrityError,
    ArtifactStore,
)
from cache_v2.errors import CacheResolutionError, ContractValidationError
from experiments.artifact_producer import (
    FormalArtifactRequest,
    materialize_formal_artifact,
)


GRAPH_HASH = "a" * 64
SPLIT_HASH = "b" * 64
CANDIDATE_HASH = "c" * 64
SCORE_VERSION = ProducerVersion("pagerank-score-v1", "score-source-v1")
PREDICTION_VERSION = ProducerVersion("gu-prediction-v1", "prediction-source-v1")
EVALUATION_VERSION = ProducerVersion("collateral-eval-v1", "evaluation-source-v1")
SELECTION_VERSION = ProducerVersion("selection-fixture-v1", "selection-source-v1")


def _candidate_hash(nodes):
    payload = json.dumps(
        sorted(nodes),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _tree_state(root):
    return {
        path.relative_to(root).as_posix(): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            path.stat().st_mtime_ns,
            path.stat().st_size,
        )
        for path in root.rglob("*")
        if path.is_file()
    }


def _selection_recipe(candidate_nodes=(0, 1, 2, 3, 4, 5)):
    return ArtifactRecipe(
        {
            "artifact_kind": "selection",
            "topology_fingerprint": GRAPH_HASH,
            "candidate_set_hash": _candidate_hash(candidate_nodes),
            "node_id_space": "global",
            "selector": "degree",
            "selector_algorithm_version": "fixture-v1",
            "selection_rule": "topk_desc",
            "k": 2,
        }
    )


def _selection(store_root):
    candidates = (0, 1, 2, 3, 4, 5)
    store = ArtifactStore(store_root, producer_version=SELECTION_VERSION)
    store.initialize()
    return store.store_selection(
        _selection_recipe(candidates),
        [4, 1],
        num_nodes=6,
        candidate_nodes=candidates,
        compute_seconds=0.1,
    )


def _canonical_cora_shape_selection(store_root):
    candidates = tuple(range(2166))
    recipe = ArtifactRecipe(
        {
            "artifact_kind": "selection",
            "topology_fingerprint": GRAPH_HASH,
            "candidate_set_hash": _candidate_hash(candidates),
            "node_id_space": "global",
            "selector": "degree",
            "selector_algorithm_version": "canonical-shape-fixture-v1",
            "selection_rule": "topk_desc",
            "k": 108,
        }
    )
    store = ArtifactStore(store_root, producer_version=SELECTION_VERSION)
    store.initialize()
    return store.store_selection(
        recipe,
        list(range(108)),
        num_nodes=2708,
        candidate_nodes=candidates,
        compute_seconds=0.1,
    )


def _score_recipe():
    return build_score_recipe(
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        num_nodes=6,
        node_id_space="global",
        selector_identity={"strategy": "pagerank", "model": None},
        score_algorithm={"name": "pagerank", "version": "v1"},
        parameters={"damping": 0.85},
        producer_version=SCORE_VERSION,
    )


def _score_payload(values=(0.9, 0.8, 0.2)):
    return ScorePayload.build(
        ordered_node_ids=[4, 1, 3],
        scores=values,
        graph_fingerprint=GRAPH_HASH,
        candidate_set_hash=CANDIDATE_HASH,
        node_id_space="global",
        score_kind="scores",
    )


def _prediction_recipe(selection):
    return build_prediction_recipe(
        graph_fingerprint=GRAPH_HASH,
        split_fingerprint=SPLIT_HASH,
        selection_artifact_id=selection.artifact_id,
        selected_nodes_hash=selection.payload.ordered_nodes_hash,
        num_nodes=6,
        num_classes=2,
        class_order=[0, 1],
        node_id_space="global",
        target_model_recipe={
            "method": "GNNDelete",
            "architecture": "GCN",
            "training_seed": 42,
        },
        run_seed=42,
        producer_version=PREDICTION_VERSION,
    )


def _prediction_payload(selection):
    logits_before = np.array(
        [[2.0, 0.1], [1.5, 0.5], [0.2, 1.4], [0.3, 1.2], [1.1, 0.7], [0.4, 1.0]],
        dtype=np.float32,
    )
    logits_unlearned = logits_before + np.float32(0.05)
    logits_retrained = logits_before - np.float32(0.02)
    train_mask = np.array([1, 1, 1, 1, 1, 0], dtype=bool)
    retain_mask = train_mask.copy()
    retain_mask[[4, 1]] = False
    return PredictionPayload.build(
        logits_before=logits_before,
        logits_unlearned=logits_unlearned,
        logits_retrained=logits_retrained,
        y=np.array([0, 0, 1, 1, 0, 1], dtype=np.int64),
        train_mask=train_mask,
        test_mask=np.array([0, 0, 0, 0, 0, 1], dtype=bool),
        retain_mask=retain_mask,
        selected_nodes=np.array([4, 1], dtype=np.int64),
        class_order=np.array([0, 1], dtype=np.int64),
        graph_fingerprint=GRAPH_HASH,
        split_fingerprint=SPLIT_HASH,
        selection_artifact_id=selection.artifact_id,
        node_id_space="global",
    )


def _evaluation_recipe(prediction_artifact_id):
    return build_evaluation_recipe(
        prediction_artifact_id=prediction_artifact_id,
        graph_fingerprint=GRAPH_HASH,
        metric_name="collateral-core",
        metric_version="v1",
        metric_parameters={"f1_average": "micro", "shift_norm": "linf"},
        producer_version=EVALUATION_VERSION,
    )


def _evaluation_payload(prediction_artifact_id, gap=0.02):
    return EvaluationPayload.build(
        prediction_artifact_id=prediction_artifact_id,
        graph_fingerprint=GRAPH_HASH,
        metric_name="collateral-core",
        metric_version="v1",
        metrics={
            "perf_before": 0.60,
            "perf_unlearn": 0.58,
            "perf_retrain": 0.59,
            "gap": gap,
            "mean_pred_shift": 0.05,
            "fraction_flipped": 0.10,
        },
    )


def test_recipe_builders_bind_minimal_identity_and_producer_versions():
    score = _score_recipe()
    assert score.fields["artifact_contract"] == "opengu-score-artifact-v1"
    assert score.fields["producer_version"] == SCORE_VERSION.to_dict()
    assert "k" not in score.fields

    with pytest.raises(ContractValidationError, match="Prediction Artifact"):
        build_prediction_recipe(
            graph_fingerprint=GRAPH_HASH,
            split_fingerprint=SPLIT_HASH,
            selection_artifact_id="sel_00000000_00000000",
            selected_nodes_hash="d" * 64,
            num_nodes=6,
            num_classes=2,
            class_order=[0, 1],
            node_id_space="global",
            target_model_recipe={},
            run_seed=42,
            producer_version=PREDICTION_VERSION,
        )


def test_score_payload_is_deterministic_versioned_and_recipe_checked():
    recipe = _score_recipe()
    first = _score_payload()
    second = ScorePayload.from_bytes(first.canonical_bytes)

    assert first == second
    assert first.canonical_bytes == second.canonical_bytes
    first.validate_against(recipe)
    with zipfile.ZipFile(BytesIO(first.canonical_bytes), "r") as archive:
        assert archive.namelist() == ["metadata.json", "ordered_node_ids.npy", "scores.npy"]
        assert {item.date_time for item in archive.infolist()} == {(1980, 1, 1, 0, 0, 0)}
        assert {item.compress_type for item in archive.infolist()} == {zipfile.ZIP_STORED}

    with pytest.raises(ArtifactIntegrityError, match="finite"):
        _score_payload(values=(0.9, float("nan"), 0.2))


def test_prediction_payload_is_deterministic_and_validates_shapes_and_retain_mask(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    recipe = _prediction_recipe(selection)
    payload = _prediction_payload(selection)
    roundtrip = PredictionPayload.from_bytes(payload.canonical_bytes)

    assert payload == roundtrip
    assert payload.canonical_bytes == roundtrip.canonical_bytes
    payload.validate_against(recipe)
    assert payload.logits_before.dtype == np.dtype("<f4")
    assert payload.y.dtype == np.dtype("<i8")

    bad_retain = payload.retain_mask.copy()
    bad_retain[4] = True
    with pytest.raises(ArtifactIntegrityError, match="retain_mask"):
        PredictionPayload.build(
            logits_before=payload.logits_before,
            logits_unlearned=payload.logits_unlearned,
            logits_retrained=payload.logits_retrained,
            y=payload.y,
            train_mask=payload.train_mask,
            test_mask=payload.test_mask,
            retain_mask=bad_retain,
            selected_nodes=payload.selected_nodes,
            class_order=payload.class_order,
            graph_fingerprint=GRAPH_HASH,
            split_fingerprint=SPLIT_HASH,
            selection_artifact_id=selection.artifact_id,
            node_id_space="global",
        )


def test_formal_store_cold_warm_chain_is_exact_zero_write_and_dependency_bound(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)

    score_store = FormalArtifactStore(root, producer_version=SCORE_VERSION)
    score = score_store.store_payload(_score_recipe(), _score_payload(), compute_seconds=0.2)
    assert score.hit is False
    assert score.artifact_id.startswith("score_")

    prediction_store = FormalArtifactStore(root, producer_version=PREDICTION_VERSION)
    prediction_recipe = _prediction_recipe(selection)
    prediction = prediction_store.store_payload(
        prediction_recipe, _prediction_payload(selection), compute_seconds=1.5
    )
    assert prediction.artifact_id.startswith("pred_")
    assert prediction_store.index.parents(prediction.artifact_id) == [selection.artifact_id]

    evaluation_store = FormalArtifactStore(root, producer_version=EVALUATION_VERSION)
    evaluation_recipe = _evaluation_recipe(prediction.artifact_id)
    evaluation = evaluation_store.store_payload(
        evaluation_recipe,
        _evaluation_payload(prediction.artifact_id),
        compute_seconds=0.01,
    )
    assert evaluation.artifact_id.startswith("eval_")
    assert evaluation_store.index.parents(evaluation.artifact_id) == [prediction.artifact_id]

    before = _tree_state(root)
    warm = FormalArtifactStore(root, producer_version=EVALUATION_VERSION).load_payload_read_only(
        ArtifactType.EVALUATION,
        evaluation_recipe,
        artifact_id=evaluation.artifact_id,
    )
    assert warm.hit is True
    assert warm.payload == evaluation.payload
    assert _tree_state(root) == before


def test_canonical_cora_shape_prediction_evaluation_roundtrip_is_cpu_only(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    selection = _canonical_cora_shape_selection(root)
    num_nodes = 2708
    num_classes = 7
    class_order = np.arange(num_classes, dtype=np.int64)
    train_mask = np.zeros(num_nodes, dtype=bool)
    train_mask[:2166] = True
    test_mask = ~train_mask
    retain_mask = train_mask.copy()
    retain_mask[:108] = False
    base = np.arange(num_nodes * num_classes, dtype=np.float32).reshape(
        num_nodes, num_classes
    )
    base /= np.float32(num_nodes * num_classes)
    payload = PredictionPayload.build(
        logits_before=base,
        logits_unlearned=base + np.float32(0.01),
        logits_retrained=base - np.float32(0.01),
        y=np.arange(num_nodes, dtype=np.int64) % num_classes,
        train_mask=train_mask,
        test_mask=test_mask,
        retain_mask=retain_mask,
        selected_nodes=np.arange(108, dtype=np.int64),
        class_order=class_order,
        graph_fingerprint=GRAPH_HASH,
        split_fingerprint=SPLIT_HASH,
        selection_artifact_id=selection.artifact_id,
        node_id_space="global",
    )
    recipe = build_prediction_recipe(
        graph_fingerprint=GRAPH_HASH,
        split_fingerprint=SPLIT_HASH,
        selection_artifact_id=selection.artifact_id,
        selected_nodes_hash=selection.payload.ordered_nodes_hash,
        num_nodes=num_nodes,
        num_classes=num_classes,
        class_order=class_order,
        node_id_space="global",
        target_model_recipe={"method": "fixture", "architecture": "GCN"},
        run_seed=42,
        producer_version=PREDICTION_VERSION,
    )
    prediction_store = FormalArtifactStore(
        root, producer_version=PREDICTION_VERSION
    )
    prediction = prediction_store.store_payload(recipe, payload)
    assert prediction.payload.logits_before.shape == (2708, 7)

    evaluation_recipe = _evaluation_recipe(prediction.artifact_id)
    evaluation_store = FormalArtifactStore(
        root, producer_version=EVALUATION_VERSION
    )
    evaluation = evaluation_store.store_payload(
        evaluation_recipe,
        _evaluation_payload(prediction.artifact_id),
    )
    warm = evaluation_store.load_payload_read_only(
        ArtifactType.EVALUATION,
        evaluation_recipe,
        artifact_id=evaluation.artifact_id,
    )
    assert warm.hit is True


def test_formal_store_rejects_missing_or_unhealthy_dependencies(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    prediction_store = FormalArtifactStore(root, producer_version=PREDICTION_VERSION)
    recipe = _prediction_recipe(selection)
    payload = _prediction_payload(selection)
    prediction = prediction_store.store_payload(recipe, payload)

    with sqlite3.connect(str(prediction_store.index.database_path)) as connection:
        connection.execute(
            "UPDATE artifacts SET status = 'invalid' WHERE artifact_id = ?",
            (selection.artifact_id,),
        )
        connection.commit()
    with pytest.raises(CacheResolutionError, match="dependency"):
        prediction_store.load_payload_read_only(
            ArtifactType.PREDICTION, recipe, artifact_id=prediction.artifact_id
        )

    fake_recipe = build_evaluation_recipe(
        prediction_artifact_id="pred_00000000_00000000",
        graph_fingerprint=GRAPH_HASH,
        metric_name="collateral-core",
        metric_version="v1",
        metric_parameters={},
        producer_version=EVALUATION_VERSION,
    )
    with pytest.raises(CacheResolutionError, match="dependency"):
        FormalArtifactStore(root, producer_version=EVALUATION_VERSION).store_payload(
            fake_recipe,
            _evaluation_payload("pred_00000000_00000000"),
        )


def test_evaluation_hit_recursively_rejects_corrupt_selection_dependency(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    prediction = FormalArtifactStore(
        root, producer_version=PREDICTION_VERSION
    ).store_payload(_prediction_recipe(selection), _prediction_payload(selection))
    evaluation_store = FormalArtifactStore(
        root, producer_version=EVALUATION_VERSION
    )
    recipe = _evaluation_recipe(prediction.artifact_id)
    evaluation = evaluation_store.store_payload(
        recipe, _evaluation_payload(prediction.artifact_id)
    )

    selection_path = root.joinpath(*Path(selection.semantic_path).parts)
    selection_path.write_bytes(selection_path.read_bytes() + b"\n")
    with pytest.raises(ArtifactIntegrityError, match="dependency payload"):
        evaluation_store.load_payload_read_only(
            ArtifactType.EVALUATION,
            recipe,
            artifact_id=evaluation.artifact_id,
        )


@pytest.mark.parametrize(
    "artifact_type",
    [ArtifactType.SCORE, ArtifactType.PREDICTION, ArtifactType.EVALUATION],
)
def test_all_formal_types_reject_corrupt_payload_bytes(tmp_path, artifact_type):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    if artifact_type is ArtifactType.SCORE:
        store = FormalArtifactStore(root, producer_version=SCORE_VERSION)
        recipe = _score_recipe()
        result = store.store_payload(recipe, _score_payload())
    elif artifact_type is ArtifactType.PREDICTION:
        store = FormalArtifactStore(root, producer_version=PREDICTION_VERSION)
        recipe = _prediction_recipe(selection)
        result = store.store_payload(recipe, _prediction_payload(selection))
    else:
        prediction = FormalArtifactStore(
            root, producer_version=PREDICTION_VERSION
        ).store_payload(_prediction_recipe(selection), _prediction_payload(selection))
        store = FormalArtifactStore(root, producer_version=EVALUATION_VERSION)
        recipe = _evaluation_recipe(prediction.artifact_id)
        result = store.store_payload(
            recipe, _evaluation_payload(prediction.artifact_id)
        )

    payload_path = root.joinpath(*Path(result.semantic_path).parts)
    payload_path.write_bytes(payload_path.read_bytes() + b"\n")
    with pytest.raises(ArtifactIntegrityError, match="payload"):
        store.load_payload_read_only(
            artifact_type, recipe, artifact_id=result.artifact_id
        )


@pytest.mark.parametrize(
    "artifact_type",
    [ArtifactType.SCORE, ArtifactType.PREDICTION, ArtifactType.EVALUATION],
)
def test_all_formal_types_reject_corrupt_header_bytes(tmp_path, artifact_type):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    if artifact_type is ArtifactType.SCORE:
        store = FormalArtifactStore(root, producer_version=SCORE_VERSION)
        recipe = _score_recipe()
        result = store.store_payload(recipe, _score_payload())
    elif artifact_type is ArtifactType.PREDICTION:
        store = FormalArtifactStore(root, producer_version=PREDICTION_VERSION)
        recipe = _prediction_recipe(selection)
        result = store.store_payload(recipe, _prediction_payload(selection))
    else:
        prediction = FormalArtifactStore(
            root, producer_version=PREDICTION_VERSION
        ).store_payload(_prediction_recipe(selection), _prediction_payload(selection))
        store = FormalArtifactStore(root, producer_version=EVALUATION_VERSION)
        recipe = _evaluation_recipe(prediction.artifact_id)
        result = store.store_payload(
            recipe, _evaluation_payload(prediction.artifact_id)
        )

    payload_path = root.joinpath(*Path(result.semantic_path).parts)
    payload_path.with_name("header.json").write_bytes(b"{}")
    with pytest.raises(ArtifactIntegrityError, match="header sidecar"):
        store.load_payload_read_only(
            artifact_type, recipe, artifact_id=result.artifact_id
        )


@pytest.mark.parametrize("artifact_type", [ArtifactType.SCORE, ArtifactType.PREDICTION, ArtifactType.EVALUATION])
def test_all_formal_types_conflict_quarantine_and_corruption_fail_closed(tmp_path, artifact_type):
    root = (tmp_path / "cache-v2").absolute()
    selection = _selection(root)
    if artifact_type is ArtifactType.SCORE:
        store = FormalArtifactStore(root, producer_version=SCORE_VERSION)
        recipe = _score_recipe()
        first = _score_payload()
        different = _score_payload(values=(0.91, 0.8, 0.2))
    elif artifact_type is ArtifactType.PREDICTION:
        store = FormalArtifactStore(root, producer_version=PREDICTION_VERSION)
        recipe = _prediction_recipe(selection)
        first = _prediction_payload(selection)
        changed = first.logits_unlearned.copy()
        changed[0, 0] += np.float32(0.1)
        different = PredictionPayload.build(
            logits_before=first.logits_before,
            logits_unlearned=changed,
            logits_retrained=first.logits_retrained,
            y=first.y,
            train_mask=first.train_mask,
            test_mask=first.test_mask,
            retain_mask=first.retain_mask,
            selected_nodes=first.selected_nodes,
            class_order=first.class_order,
            graph_fingerprint=GRAPH_HASH,
            split_fingerprint=SPLIT_HASH,
            selection_artifact_id=selection.artifact_id,
            node_id_space="global",
        )
    else:
        prediction = FormalArtifactStore(
            root, producer_version=PREDICTION_VERSION
        ).store_payload(_prediction_recipe(selection), _prediction_payload(selection))
        store = FormalArtifactStore(root, producer_version=EVALUATION_VERSION)
        recipe = _evaluation_recipe(prediction.artifact_id)
        first = _evaluation_payload(prediction.artifact_id, gap=0.02)
        different = _evaluation_payload(prediction.artifact_id, gap=0.03)

    original = store.store_payload(recipe, first)
    with pytest.raises(ArtifactConflictError) as caught:
        store.store_payload(recipe, different)
    quarantine = root.joinpath(*Path(caught.value.quarantine_path).parts)
    assert quarantine.is_file()
    with pytest.raises(CacheResolutionError, match="conflict"):
        store.load_payload_read_only(artifact_type, recipe, artifact_id=original.artifact_id)


def test_experiment_layer_calls_upstream_producer_only_on_miss_and_never_writes_legacy(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    legacy = tmp_path / "results"
    for name in ("cache", "selection_cache", "score_cache"):
        path = legacy / name
        path.mkdir(parents=True, exist_ok=True)
        (path / "sentinel.txt").write_text(name, encoding="utf-8")
    before_legacy = _tree_state(legacy)
    request = FormalArtifactRequest(
        artifact_type=ArtifactType.SCORE,
        recipe=_score_recipe(),
        producer_version=SCORE_VERSION,
    )
    calls = {"count": 0}

    def producer():
        calls["count"] += 1
        return _score_payload()

    cold = materialize_formal_artifact(root, request, producer)

    def forbidden_producer():
        raise AssertionError("producer called on exact hit")

    before_v2 = _tree_state(root)
    warm = materialize_formal_artifact(root, request, forbidden_producer)
    assert calls["count"] == 1
    assert cold.producer_called is True
    assert warm.producer_called is False
    assert warm.result.artifact_id == cold.result.artifact_id
    assert _tree_state(root) == before_v2
    assert _tree_state(legacy) == before_legacy


def test_experiment_layer_does_not_recompute_a_corrupt_exact_candidate(tmp_path):
    root = (tmp_path / "cache-v2").absolute()
    request = FormalArtifactRequest(
        artifact_type=ArtifactType.SCORE,
        recipe=_score_recipe(),
        producer_version=SCORE_VERSION,
    )
    cold = materialize_formal_artifact(root, request, _score_payload)
    payload_path = root.joinpath(*Path(cold.result.semantic_path).parts)
    damaged = bytearray(payload_path.read_bytes())
    damaged[0] ^= 0x01
    payload_path.write_bytes(bytes(damaged))
    calls = {"count": 0}

    def forbidden_recompute():
        calls["count"] += 1
        return _score_payload()

    with pytest.raises(ArtifactIntegrityError, match="content hash"):
        materialize_formal_artifact(root, request, forbidden_recompute)
    assert calls["count"] == 0


def test_cache_v2_formal_modules_have_no_upstream_producer_or_dataset_imports():
    root = Path(__file__).resolve().parents[1]
    for relative in (
        "cache_v2/formal_artifacts.py",
        "cache_v2/formal_store.py",
    ):
        source = (root / relative).read_text(encoding="utf-8")
        lowered = source.lower()
        for forbidden in (
            "from experiments",
            "import experiments",
            "from dataset",
            "import dataset",
            "planetoid",
            "ogb",
            "torch_geometric",
            "allow_download",
            "dataset_root",
            "get_or_compute",
        ):
            assert forbidden not in lowered, (relative, forbidden)
