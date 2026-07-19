"""Experiment-owned Gate 3 adapter for a completed Degree run leaf.

The adapter reads OpenGU's canonical processed pickle plus one checksummed
reference run leaf.  It computes Degree Score/Selection in the experiment
layer, normalizes Prediction/Evaluation into formal V2 payloads, stores them
under an isolated ArtifactStore, and invokes the read-only comparison harness.
Cache V2 never loads these sources or calls the producers.
"""

from __future__ import annotations

import hashlib
import json
import math
import pickle
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Dict, Sequence, Tuple, Union

import numpy as np
import torch
from torch_geometric.utils import degree

from cache_v2 import ArtifactType, ProducerVersion
from cache_v2.errors import ContractValidationError, PathValidationError
from cache_v2.formal_artifacts import (
    EvaluationPayload,
    PredictionPayload,
    ScorePayload,
    build_evaluation_recipe,
    build_prediction_recipe,
    build_score_recipe,
)
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
)
from experiments.artifact_producer import (
    FormalArtifactRequest,
    materialize_formal_artifact,
)
from experiments.selection_inputs import (
    make_dataset_selection_inputs,
    processed_data_path,
)
from experiments.selection_producer import (
    DEGREE_ALGORITHM_VERSION,
    DEGREE_PRODUCER_SEMANTIC_VERSION,
    SelectionInputs,
    build_degree_producer,
    build_selection_job,
    load_simple_strategy,
    producer_source_fingerprint,
    resolve_or_produce_selection,
)


GATE3_DEGREE_ADAPTER_CONTRACT = "opengu-cache-v2-gate3-degree-adapter-v1"
EVALUATION_METRIC_NAME = "collateral-core"
EVALUATION_METRIC_VERSION = "opengu-collateral-core-v1"
CORE_EVALUATION_KEYS = (
    "perf_before",
    "perf_retrain",
    "perf_unlearn",
    "drop_retrain",
    "gap",
    "gap_pct",
    "mean_pred_shift",
    "max_pred_shift",
    "fraction_flipped",
)


def _absolute_path(value: Union[str, Path], label: str) -> Path:
    supplied = Path(value).expanduser()
    if not supplied.is_absolute():
        raise PathValidationError("{0} must be explicitly absolute".format(label))
    if ".." in supplied.parts:
        raise PathValidationError("{0} must not contain '..'".format(label))
    return supplied.resolve(strict=False)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_state(paths: Sequence[Path]) -> Dict[str, Dict[str, Any]]:
    state = {}
    for path in paths:
        stat = path.stat()
        state[path.name] = {
            "sha256": _sha256_file(path),
            "size_bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
    return state


def _load_json(path: Path, label: str) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractValidationError(
            "{0} is not valid JSON: {1}".format(label, exc)
        )
    if not isinstance(value, dict):
        raise ContractValidationError("{0} must be a JSON object".format(label))
    return value


def _required_mapping(value: Any, label: str) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractValidationError("{0} must be a mapping".format(label))
    return dict(value)


def _required_integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ContractValidationError(
            "{0} must be an integer >= {1}".format(label, minimum)
        )
    return int(value)


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ContractValidationError("{0} must be a non-empty string".format(label))
    return value.strip()


def _integer_nodes(value: Any, label: str) -> Tuple[int, ...]:
    raw = np.asarray(value)
    if raw.ndim != 1 or raw.dtype.kind not in "iu":
        raise ContractValidationError(
            "{0} must be a one-dimensional integer array".format(label)
        )
    nodes = tuple(int(item) for item in raw.tolist())
    if len(nodes) != len(set(nodes)):
        raise ContractValidationError("{0} contains duplicate nodes".format(label))
    return nodes


def _adapter_source_fingerprint() -> str:
    root = Path(__file__).resolve().parents[1]
    paths = (
        Path(__file__).resolve(),
        root / "experiments" / "artifact_comparison.py",
        root / "experiments" / "artifact_producer.py",
        root / "attack" / "attack_eval.py",
    )
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8") + b"\x00")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def prediction_split_fingerprint(
    y: Any, train_mask: Any, test_mask: Any
) -> str:
    arrays = (
        ("y", np.ascontiguousarray(np.asarray(y), dtype="<i8")),
        ("train_mask", np.ascontiguousarray(np.asarray(train_mask), dtype="|b1")),
        ("test_mask", np.ascontiguousarray(np.asarray(test_mask), dtype="|b1")),
    )
    if any(array.ndim != 1 for _, array in arrays):
        raise ContractValidationError("split fingerprint inputs must be vectors")
    if len({array.shape for _, array in arrays}) != 1:
        raise ContractValidationError("split fingerprint inputs must have equal shapes")
    digest = hashlib.sha256(b"opengu-prediction-split-v1\x00")
    for name, array in arrays:
        digest.update(name.encode("ascii") + b"\x00")
        digest.update(str(array.dtype).encode("ascii") + b"\x00")
        digest.update(json.dumps(list(array.shape)).encode("ascii") + b"\x00")
        digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def _scalar_metrics_from_prediction(payload: PredictionPayload) -> Dict[str, float]:
    test_mask = np.asarray(payload.test_mask, dtype=bool)
    if not bool(test_mask.any()):
        raise ContractValidationError("Prediction test_mask is empty")
    y = np.asarray(payload.y, dtype=np.int64)
    before_pred = np.asarray(payload.logits_before).argmax(axis=1)
    retrained_pred = np.asarray(payload.logits_retrained).argmax(axis=1)
    unlearned_pred = np.asarray(payload.logits_unlearned).argmax(axis=1)
    perf_before = float(np.mean(before_pred[test_mask] == y[test_mask]))
    perf_retrain = float(np.mean(retrained_pred[test_mask] == y[test_mask]))
    perf_unlearn = float(np.mean(unlearned_pred[test_mask] == y[test_mask]))
    drop_retrain = perf_before - perf_retrain
    gap = perf_retrain - perf_unlearn
    gap_pct = gap / perf_retrain * 100.0 if perf_retrain > 0 else 0.0

    retrained = torch.from_numpy(
        np.ascontiguousarray(payload.logits_retrained, dtype=np.float32).copy()
    )
    unlearned = torch.from_numpy(
        np.ascontiguousarray(payload.logits_unlearned, dtype=np.float32).copy()
    )
    retrained_prob = torch.softmax(retrained, dim=1)
    unlearned_prob = torch.softmax(unlearned, dim=1)
    retain = torch.from_numpy(
        np.ascontiguousarray(payload.retain_mask, dtype=np.bool_).copy()
    )
    node_shift = (unlearned_prob - retrained_prob).abs()[retain].max(dim=1).values
    flipped = (
        unlearned.argmax(dim=1)[retain] != retrained.argmax(dim=1)[retain]
    ).float()
    metrics = {
        "perf_before": perf_before,
        "perf_retrain": perf_retrain,
        "perf_unlearn": perf_unlearn,
        "drop_retrain": drop_retrain,
        "gap": gap,
        "gap_pct": gap_pct,
        "mean_pred_shift": float(node_shift.mean()) if node_shift.numel() else 0.0,
        "max_pred_shift": float(node_shift.max()) if node_shift.numel() else 0.0,
        "fraction_flipped": float(flipped.mean()) if flipped.numel() else 0.0,
    }
    if any(not math.isfinite(value) for value in metrics.values()):
        raise ContractValidationError("recomputed Evaluation metric is non-finite")
    return metrics


def _collateral_metrics(collateral: Mapping[str, Any]) -> Dict[str, float]:
    rows = collateral.get("results")
    if not isinstance(rows, list):
        raise ContractValidationError("collateral.results must be a list")
    matches = [
        row
        for row in rows
        if isinstance(row, Mapping) and row.get("strategy") == "degree"
    ]
    if len(matches) != 1:
        raise ContractValidationError(
            "collateral must contain exactly one degree result"
        )
    row = matches[0]
    metrics = {}
    for key in CORE_EVALUATION_KEYS:
        value = row.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ContractValidationError(
                "collateral degree metric {0} must be numeric".format(key)
            )
        number = float(value)
        if not math.isfinite(number):
            raise ContractValidationError(
                "collateral degree metric {0} must be finite".format(key)
            )
        metrics[key] = number
    return metrics


def _formal_document(materialized: Any, recipe_hash: str) -> Dict[str, Any]:
    return {
        "artifact_id": materialized.artifact_id,
        "recipe_hash": recipe_hash,
        "content_hash": materialized.content_hash,
        "semantic_path": materialized.result.semantic_path,
        "outcome": materialized.result.outcome,
        "hit": materialized.result.hit,
        "producer_called": materialized.producer_called,
    }


def materialize_degree_gate3_bundle(
    *,
    source_leaf: Union[str, Path],
    processed_root: Union[str, Path],
    store_root: Union[str, Path],
    policy: ComparisonPolicy | None = None,
) -> Dict[str, Any]:
    """Materialize and compare one provenance-complete Degree reference leaf."""

    source = _absolute_path(source_leaf, "source_leaf")
    processed = _absolute_path(processed_root, "processed_root")
    store = _absolute_path(store_root, "store_root")
    if not source.is_dir():
        raise FileNotFoundError("reference source leaf is missing: {0}".format(source))
    if _is_within(store, source) or _is_within(source, store):
        raise PathValidationError("store_root must not overlap source_leaf")
    if _is_within(store, processed) or _is_within(processed, store):
        raise PathValidationError("store_root must not overlap processed_root")

    source_paths = tuple(
        source / name
        for name in ("attack.json", "collateral.json", "predictions.npz", "_meta.json")
    )
    missing = [str(path) for path in source_paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "reference run leaf is incomplete: {0}".format(", ".join(missing))
        )
    source_before = _source_state(source_paths)
    attack = _load_json(source / "attack.json", "attack.json")
    collateral = _load_json(source / "collateral.json", "collateral.json")
    meta = _load_json(source / "_meta.json", "_meta.json")

    attack_config = _required_mapping(attack.get("config"), "attack.config")
    dataset_name = _required_text(
        attack_config.get("dataset_name"), "attack.config.dataset_name"
    )
    if dataset_name != "cora":
        raise ContractValidationError("Gate 3 Degree adapter currently requires cora")
    train_ratio = float(attack_config.get("train_ratio"))
    val_ratio = float(attack_config.get("val_ratio"))
    test_ratio = float(attack_config.get("test_ratio"))
    is_transductive = bool(attack_config.get("is_transductive"))
    is_balanced = bool(attack_config.get("is_balanced"))
    run_seed = _required_integer(
        attack_config.get("random_seed"), "attack.config.random_seed"
    )

    processed_path = processed_data_path(
        processed,
        dataset_name=dataset_name,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        is_transductive=is_transductive,
        is_balanced=is_balanced,
    )
    if not processed_path.is_file():
        raise FileNotFoundError(
            "canonical OpenGU processed graph is missing: {0}".format(processed_path)
        )
    with processed_path.open("rb") as handle:
        data = pickle.load(handle)
    dataset = make_dataset_selection_inputs(
        data,
        dataset_name=dataset_name,
        source_path=processed_path,
    )

    results = _required_mapping(attack.get("results"), "attack.results")
    degree_result = _required_mapping(results.get("degree"), "attack.results.degree")
    if degree_result.get("failed") is True:
        raise ContractValidationError("reference degree attack is marked failed")
    reference_selected = _integer_nodes(
        degree_result.get("selected_nodes"),
        "attack degree selected_nodes",
    )
    degree_config = _required_mapping(
        degree_result.get("config"), "attack degree config"
    )
    k = _required_integer(degree_config.get("k"), "attack degree config.k", minimum=1)
    if len(reference_selected) != k:
        raise ContractValidationError("reference selected-node count does not match k")
    if set(reference_selected).difference(dataset.candidate_nodes):
        raise ContractValidationError(
            "reference selected nodes are outside canonical candidate set"
        )

    with np.load(source / "predictions.npz", allow_pickle=False) as archive:
        required_arrays = {
            "_meta__y",
            "_meta__train_mask",
            "_meta__test_mask",
            "_meta__num_nodes",
            "degree__logits_before",
            "degree__logits_unlearned",
            "degree__logits_retrained",
            "degree__retain_mask",
            "degree__selected_nodes",
        }
        missing_arrays = sorted(required_arrays.difference(archive.files))
        if missing_arrays:
            raise ContractValidationError(
                "predictions.npz is missing arrays: {0}".format(
                    ",".join(missing_arrays)
                )
            )
        arrays = {name: np.array(archive[name], copy=True) for name in required_arrays}

    prediction_selected = _integer_nodes(
        arrays["degree__selected_nodes"],
        "Prediction selected_nodes",
    )
    if prediction_selected != reference_selected:
        raise ContractValidationError(
            "attack and Prediction selected_nodes are not ordered-identical"
        )
    if int(np.asarray(arrays["_meta__num_nodes"]).item()) != dataset.num_nodes:
        raise ContractValidationError("Prediction num_nodes disagrees with dataset")
    y = np.asarray(arrays["_meta__y"], dtype=np.int64)
    train_mask = np.asarray(arrays["_meta__train_mask"], dtype=bool)
    test_mask = np.asarray(arrays["_meta__test_mask"], dtype=bool)
    if not np.array_equal(y, np.asarray(data.y.detach().cpu(), dtype=np.int64)):
        raise ContractValidationError("Prediction labels disagree with processed dataset")
    if not np.array_equal(
        train_mask, np.asarray(data.train_mask.detach().cpu(), dtype=bool)
    ):
        raise ContractValidationError(
            "Prediction train_mask disagrees with processed dataset"
        )
    if not np.array_equal(
        test_mask, np.asarray(data.test_mask.detach().cpu(), dtype=bool)
    ):
        raise ContractValidationError(
            "Prediction test_mask disagrees with processed dataset"
        )

    degree_class, degree_source = load_simple_strategy("degree")
    degree_version = ProducerVersion(
        semantic_version=DEGREE_PRODUCER_SEMANTIC_VERSION,
        source_fingerprint=producer_source_fingerprint(degree_source, "degree"),
    )
    selection_inputs = SelectionInputs(
        dataset=dataset,
        strategy="degree",
        seed=0,
        k=k,
        producer_version=degree_version,
        algorithm_version=DEGREE_ALGORITHM_VERSION,
        parameters={},
    )
    degrees = degree(
        dataset.edge_index[0],
        num_nodes=dataset.num_nodes,
    ).detach().cpu()

    adapter_fingerprint = _adapter_source_fingerprint()
    score_version = ProducerVersion(
        semantic_version="opengu-degree-score-v1",
        source_fingerprint=adapter_fingerprint,
    )
    score_recipe = build_score_recipe(
        graph_fingerprint=dataset.graph_fingerprint,
        candidate_set_hash=dataset.candidate_set_hash,
        num_nodes=dataset.num_nodes,
        node_id_space=dataset.node_id_space,
        selector_identity={
            "strategy": "degree",
            "selector_seed": 0,
            "selection_k": k,
        },
        score_algorithm={
            "name": "degree-selected-topk",
            "version": DEGREE_ALGORITHM_VERSION,
        },
        parameters={},
        producer_version=score_version,
        score_kind="scores",
    )

    def produce_score() -> ScorePayload:
        selected = tuple(
            int(node)
            for node in build_degree_producer(
                dataset, k, degree_class
            )()
        )
        return ScorePayload.build(
            ordered_node_ids=selected,
            scores=[float(degrees[node]) for node in selected],
            graph_fingerprint=dataset.graph_fingerprint,
            candidate_set_hash=dataset.candidate_set_hash,
            node_id_space=dataset.node_id_space,
            score_kind="scores",
        )

    score = materialize_formal_artifact(
        store,
        FormalArtifactRequest(ArtifactType.SCORE, score_recipe, score_version),
        produce_score,
    )
    formal_selected = tuple(
        int(item) for item in score.result.payload.ordered_node_ids.tolist()
    )
    selection_job = build_selection_job(
        selection_inputs,
        producer=lambda: formal_selected,
        source_score_artifact_id=score.artifact_id,
        execution_backend="torch-cpu",
    )
    selection = resolve_or_produce_selection(selection_job, store)
    if tuple(selection.result.payload.selected_nodes_ordered) != reference_selected:
        raise ContractValidationError(
            "ordered Selection mismatch between canonical producer and reference"
        )

    logits_before = np.asarray(arrays["degree__logits_before"], dtype=np.float32)
    logits_unlearned = np.asarray(
        arrays["degree__logits_unlearned"], dtype=np.float32
    )
    logits_retrained = np.asarray(
        arrays["degree__logits_retrained"], dtype=np.float32
    )
    if logits_before.ndim != 2:
        raise ContractValidationError("Prediction logits must be matrices")
    num_classes = int(logits_before.shape[1])
    class_order = np.arange(num_classes, dtype=np.int64)
    split_fingerprint = prediction_split_fingerprint(y, train_mask, test_mask)
    prediction_version = ProducerVersion(
        semantic_version="opengu-run-prediction-import-v1",
        source_fingerprint=adapter_fingerprint,
    )
    prediction_recipe = build_prediction_recipe(
        graph_fingerprint=dataset.graph_fingerprint,
        split_fingerprint=split_fingerprint,
        selection_artifact_id=selection.artifact_id,
        selected_nodes_hash=selection.result.payload.ordered_nodes_hash,
        num_nodes=dataset.num_nodes,
        num_classes=num_classes,
        class_order=class_order,
        node_id_space=dataset.node_id_space,
        target_model_recipe={
            "dataset": dataset_name,
            "base_model": _required_text(
                attack_config.get("base_model"), "attack.config.base_model"
            ),
            "method": _required_text(
                attack_config.get("unlearning_methods"),
                "attack.config.unlearning_methods",
            ),
            "unlearn_ratio": float(attack_config.get("unlearn_ratio")),
            "source_git_sha": _required_text(
                meta.get("git_sha"), "_meta.git_sha"
            ),
            "source_predictions_sha256": source_before["predictions.npz"]["sha256"],
        },
        run_seed=run_seed,
        producer_version=prediction_version,
    )

    def produce_prediction() -> PredictionPayload:
        return PredictionPayload.build(
            logits_before=logits_before,
            logits_unlearned=logits_unlearned,
            logits_retrained=logits_retrained,
            y=y,
            train_mask=train_mask,
            test_mask=test_mask,
            retain_mask=np.asarray(arrays["degree__retain_mask"], dtype=bool),
            selected_nodes=np.asarray(formal_selected, dtype=np.int64),
            class_order=class_order,
            graph_fingerprint=dataset.graph_fingerprint,
            split_fingerprint=split_fingerprint,
            selection_artifact_id=selection.artifact_id,
            node_id_space=dataset.node_id_space,
        )

    prediction = materialize_formal_artifact(
        store,
        FormalArtifactRequest(
            ArtifactType.PREDICTION,
            prediction_recipe,
            prediction_version,
        ),
        produce_prediction,
    )
    reference_metrics = _collateral_metrics(collateral)
    evaluation_version = ProducerVersion(
        semantic_version="opengu-collateral-evaluation-v1",
        source_fingerprint=adapter_fingerprint,
    )
    evaluation_recipe = build_evaluation_recipe(
        prediction_artifact_id=prediction.artifact_id,
        graph_fingerprint=dataset.graph_fingerprint,
        metric_name=EVALUATION_METRIC_NAME,
        metric_version=EVALUATION_METRIC_VERSION,
        metric_parameters={
            "f1_average": "micro",
            "shift_norm": "linf",
            "source_collateral_sha256": source_before["collateral.json"]["sha256"],
        },
        producer_version=evaluation_version,
    )

    def produce_evaluation() -> EvaluationPayload:
        return EvaluationPayload.build(
            prediction_artifact_id=prediction.artifact_id,
            graph_fingerprint=dataset.graph_fingerprint,
            metric_name=EVALUATION_METRIC_NAME,
            metric_version=EVALUATION_METRIC_VERSION,
            metrics=_scalar_metrics_from_prediction(prediction.result.payload),
        )

    evaluation = materialize_formal_artifact(
        store,
        FormalArtifactRequest(
            ArtifactType.EVALUATION,
            evaluation_recipe,
            evaluation_version,
        ),
        produce_evaluation,
    )

    reference_bundle = ReferenceArtifactBundle(
        score=ReferenceScore(
            reference_id="degree-score:{0}".format(
                source_before["attack.json"]["sha256"]
            ),
            ordered_node_ids=reference_selected,
            scores=[float(degrees[node]) for node in reference_selected],
            graph_fingerprint=dataset.graph_fingerprint,
            candidate_set_hash=dataset.candidate_set_hash,
            node_id_space=dataset.node_id_space,
        ),
        selection=ReferenceSelection(
            reference_id="degree-selection:{0}".format(
                source_before["attack.json"]["sha256"]
            ),
            selected_nodes_ordered=reference_selected,
            graph_fingerprint=dataset.graph_fingerprint,
            candidate_set_hash=dataset.candidate_set_hash,
            node_id_space=dataset.node_id_space,
        ),
        prediction=ReferencePrediction(
            reference_id="prediction:{0}".format(
                source_before["predictions.npz"]["sha256"]
            ),
            logits_before=logits_before,
            logits_unlearned=logits_unlearned,
            logits_retrained=logits_retrained,
            y=y,
            train_mask=train_mask,
            test_mask=test_mask,
            retain_mask=np.asarray(arrays["degree__retain_mask"], dtype=bool),
            selected_nodes=np.asarray(reference_selected, dtype=np.int64),
            class_order=class_order,
            graph_fingerprint=dataset.graph_fingerprint,
            split_fingerprint=split_fingerprint,
            node_id_space=dataset.node_id_space,
        ),
        evaluation=ReferenceEvaluation(
            reference_id="evaluation:{0}".format(
                source_before["collateral.json"]["sha256"]
            ),
            metrics=reference_metrics,
            graph_fingerprint=dataset.graph_fingerprint,
            metric_name=EVALUATION_METRIC_NAME,
            metric_version=EVALUATION_METRIC_VERSION,
        ),
    )
    formal_bundle = FormalArtifactBundle(
        score=score.result.payload,
        selection=selection.result.payload,
        prediction=prediction.result.payload,
        evaluation=evaluation.result.payload,
    )
    artifact_ids = FormalArtifactIds(
        score=score.artifact_id,
        selection=selection.artifact_id,
        prediction=prediction.artifact_id,
        evaluation=evaluation.artifact_id,
    )
    effective_policy = policy or ComparisonPolicy.from_atol(
        score_atol=0.0,
        prediction_atol=0.0,
        evaluation_atol=1e-6,
    )
    comparison = compare_artifact_bundle(
        reference_bundle,
        formal_bundle,
        artifact_ids,
        effective_policy,
    )
    source_after = _source_state(source_paths)
    if source_after != source_before:
        raise ContractValidationError("Gate 3 adapter modified its reference source")

    score_doc = _formal_document(score, score_recipe.recipe_hash)
    selection_doc = {
        "artifact_id": selection.artifact_id,
        "recipe_hash": selection_job.recipe.recipe_hash,
        "content_hash": selection.content_hash,
        "semantic_path": selection.result.semantic_path,
        "outcome": selection.result.outcome,
        "hit": selection.hit,
        "producer_called": selection.producer_called,
        "source_score_artifact_id": (
            selection.result.payload.source_score_artifact_id
        ),
    }
    prediction_doc = _formal_document(
        prediction, prediction_recipe.recipe_hash
    )
    evaluation_doc = _formal_document(
        evaluation, evaluation_recipe.recipe_hash
    )
    return {
        "adapter_contract": GATE3_DEGREE_ADAPTER_CONTRACT,
        "passed": comparison.passed,
        "status": comparison.status,
        "source_leaf": str(source),
        "source_files": source_before,
        "source_unchanged": True,
        "store_root": str(store),
        "canonical_dataset": {
            "processed_path": str(processed_path),
            "processed_sha256": _sha256_file(processed_path),
            "dataset_fingerprint": dataset.dataset_fingerprint,
            "graph_fingerprint": dataset.graph_fingerprint,
            "candidate_set_hash": dataset.candidate_set_hash,
            "num_nodes": dataset.num_nodes,
            "edge_count": int(dataset.edge_index.shape[1]),
            "candidate_count": dataset.candidate_count,
            "node_id_space": dataset.node_id_space,
        },
        "selection": {
            "strategy": "degree",
            "k": k,
            "algorithm_version": DEGREE_ALGORITHM_VERSION,
            "producer_version": degree_version.to_dict(),
            "ordered_exact": formal_selected == reference_selected,
        },
        "artifact_ids": artifact_ids.to_dict(),
        "artifacts": {
            "score": score_doc,
            "selection": selection_doc,
            "prediction": prediction_doc,
            "evaluation": evaluation_doc,
        },
        "comparison": comparison.to_dict(),
        "comparison_report_hash": comparison.report_hash,
    }


__all__ = [
    "CORE_EVALUATION_KEYS",
    "EVALUATION_METRIC_NAME",
    "EVALUATION_METRIC_VERSION",
    "GATE3_DEGREE_ADAPTER_CONTRACT",
    "materialize_degree_gate3_bundle",
    "prediction_split_fingerprint",
]
