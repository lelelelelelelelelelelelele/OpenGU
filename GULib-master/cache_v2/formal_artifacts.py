"""Strict Gate 2 payload and Recipe contracts for formal Cache V2 Artifacts.

This module owns serialization and identity validation only.  It never loads a
dataset, invokes a producer, opens a CacheIndex, or writes a payload.
"""

from __future__ import annotations

import copy
import json
import math
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, Optional, Sequence, Tuple, Type

import numpy as np

from .canonical import canonicalize, sha256_bytes
from .contracts import (
    ArtifactRecipe,
    ArtifactType,
    ProducerVersion,
    validate_artifact_id,
    validate_sha256,
)
from .errors import CacheV2Error, ContractValidationError
from .store import ArtifactIntegrityError


SCORE_PAYLOAD_SCHEMA = "cache_v2.score"
SCORE_PAYLOAD_VERSION = 1
SCORE_RECIPE_CONTRACT = "opengu-score-artifact-v1"

PREDICTION_PAYLOAD_SCHEMA = "cache_v2.prediction"
PREDICTION_PAYLOAD_VERSION = 1
PREDICTION_RECIPE_CONTRACT = "opengu-prediction-artifact-v1"

EVALUATION_PAYLOAD_SCHEMA = "cache_v2.evaluation"
EVALUATION_PAYLOAD_VERSION = 1
EVALUATION_RECIPE_CONTRACT = "opengu-evaluation-artifact-v1"

_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def _plain_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractValidationError("payload is not canonical JSON: {0}".format(exc))


def _reject_constant(value: str) -> None:
    raise ValueError("non-finite JSON number {0} is forbidden".format(value))


def _unique_object(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {0}".format(key))
        result[key] = value
    return result


def _parse_plain_json(payload: bytes, label: str) -> Any:
    try:
        text = payload.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
        raise ArtifactIntegrityError("{0} is invalid canonical JSON: {1}".format(label, exc))
    try:
        canonical = _plain_json_bytes(value)
    except CacheV2Error as exc:
        raise ArtifactIntegrityError("{0} is invalid: {1}".format(label, exc))
    if canonical != payload:
        raise ArtifactIntegrityError("{0} is not canonical JSON".format(label))
    return value


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ContractValidationError("{0} must be a non-empty string".format(label))
    return value.strip()


def _required_integer(value: Any, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ContractValidationError(
            "{0} must be an integer >= {1}".format(label, minimum)
        )
    return value


def _required_mapping(value: Any, label: str, allow_empty: bool = False) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractValidationError("{0} must be a mapping".format(label))
    copied = copy.deepcopy(dict(value))
    if not allow_empty and not copied:
        raise ContractValidationError("{0} must not be empty".format(label))
    canonicalize(copied)
    return copied


def _producer_mapping(value: ProducerVersion) -> Dict[str, Optional[str]]:
    if not isinstance(value, ProducerVersion) or not value.is_identified:
        raise ContractValidationError("producer_version must identify its producer")
    return value.to_dict()


def ordered_int_hash(values: Sequence[int]) -> str:
    array = _int_vector(values, "integer sequence")
    return sha256_bytes(_plain_json_bytes([int(item) for item in array]))


def _freeze_array(array: np.ndarray, dtype: np.dtype) -> np.ndarray:
    contiguous = np.ascontiguousarray(array, dtype=dtype)
    frozen = np.frombuffer(contiguous.tobytes(order="C"), dtype=dtype).reshape(
        contiguous.shape
    )
    frozen.setflags(write=False)
    return frozen


def _int_vector(value: Any, label: str) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1 or array.dtype.kind not in "iu":
        raise ContractValidationError("{0} must be a one-dimensional integer array".format(label))
    if array.dtype.kind == "u" and array.size and int(array.max()) > np.iinfo(np.int64).max:
        raise ContractValidationError("{0} contains an integer outside int64".format(label))
    return _freeze_array(array, np.dtype("<i8"))


def _float_vector(value: Any, label: str, dtype: str = "<f8") -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1 or array.dtype.kind not in "fiu":
        raise ContractValidationError("{0} must be a one-dimensional numeric array".format(label))
    frozen = _freeze_array(array, np.dtype(dtype))
    if not np.isfinite(frozen).all():
        raise ArtifactIntegrityError("{0} must contain only finite values".format(label))
    return frozen


def _float_matrix(value: Any, label: str) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 2 or array.dtype.kind != "f":
        raise ContractValidationError("{0} must be a two-dimensional floating array".format(label))
    frozen = _freeze_array(array, np.dtype("<f4"))
    if not np.isfinite(frozen).all():
        raise ArtifactIntegrityError("{0} must contain only finite values".format(label))
    return frozen


def _bool_vector(value: Any, label: str) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim != 1 or array.dtype.kind != "b":
        raise ContractValidationError("{0} must be a one-dimensional boolean array".format(label))
    return _freeze_array(array, np.dtype("|b1"))


def _npy_bytes(array: np.ndarray) -> bytes:
    output = BytesIO()
    np.lib.format.write_array(output, array, version=(2, 0), allow_pickle=False)
    return output.getvalue()


def _read_npy(payload: bytes, label: str) -> np.ndarray:
    source = BytesIO(payload)
    try:
        array = np.lib.format.read_array(source, allow_pickle=False)
    except (TypeError, ValueError) as exc:
        raise ArtifactIntegrityError("{0} is not a safe NPY array: {1}".format(label, exc))
    if source.read(1):
        raise ArtifactIntegrityError("{0} has trailing bytes".format(label))
    return array


def _zip_member(name: str, payload: bytes) -> Tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(filename=name, date_time=_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o600 << 16
    info.extra = b""
    info.comment = b""
    return info, payload


def _archive_bytes(entries: Sequence[Tuple[str, bytes]]) -> bytes:
    output = BytesIO()
    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for name, payload in entries:
            info, content = _zip_member(name, payload)
            archive.writestr(info, content)
    return output.getvalue()


def _read_archive(payload: bytes, expected_names: Sequence[str], label: str) -> Dict[str, bytes]:
    try:
        with zipfile.ZipFile(BytesIO(payload), mode="r") as archive:
            infos = archive.infolist()
            names = [item.filename for item in infos]
            if names != list(expected_names):
                raise ArtifactIntegrityError(
                    "{0} member schema mismatch: {1}".format(label, names)
                )
            for item in infos:
                if (
                    item.date_time != _ZIP_TIMESTAMP
                    or item.compress_type != zipfile.ZIP_STORED
                    or item.flag_bits & 0x1
                    or item.file_size != item.compress_size
                    or "/" in item.filename
                    or "\\" in item.filename
                ):
                    raise ArtifactIntegrityError(
                        "{0} member metadata is not canonical".format(label)
                    )
            return {item.filename: archive.read(item) for item in infos}
    except ArtifactIntegrityError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise ArtifactIntegrityError("{0} is not a valid deterministic archive: {1}".format(label, exc))


def _recipe_contract(recipe: ArtifactRecipe, expected: str, label: str) -> Dict[str, Any]:
    if not isinstance(recipe, ArtifactRecipe):
        raise ContractValidationError("recipe must be ArtifactRecipe")
    fields = recipe.fields
    if fields.get("artifact_contract") != expected:
        raise ArtifactIntegrityError("{0} Recipe contract mismatch".format(label))
    return fields


@dataclass(frozen=True, eq=False)
class ScorePayload:
    payload_version: int
    ordered_node_ids: np.ndarray
    scores: Optional[np.ndarray]
    graph_fingerprint: str
    candidate_set_hash: str
    node_id_space: str
    score_kind: str

    artifact_type = ArtifactType.SCORE
    payload_schema = SCORE_PAYLOAD_SCHEMA
    contract_version = SCORE_PAYLOAD_VERSION
    file_extension = "npz"

    def __post_init__(self) -> None:
        if self.payload_version != SCORE_PAYLOAD_VERSION:
            raise ContractValidationError("unsupported Score payload version")
        nodes = _int_vector(self.ordered_node_ids, "ordered_node_ids")
        if len(set(int(item) for item in nodes)) != len(nodes):
            raise ContractValidationError("ordered_node_ids contains duplicates")
        scores = self.scores
        if scores is not None:
            scores = _float_vector(scores, "scores")
            if scores.shape != nodes.shape:
                raise ContractValidationError("scores must match ordered_node_ids length")
        graph = validate_sha256(self.graph_fingerprint, "graph_fingerprint")
        candidate = validate_sha256(self.candidate_set_hash, "candidate_set_hash")
        node_space = _required_text(self.node_id_space, "node_id_space")
        kind = _required_text(self.score_kind, "score_kind")
        if kind not in ("ranking", "scores"):
            raise ContractValidationError("score_kind must be ranking or scores")
        if (kind == "scores") != (scores is not None):
            raise ContractValidationError("score_kind and scores presence disagree")
        object.__setattr__(self, "ordered_node_ids", nodes)
        object.__setattr__(self, "scores", scores)
        object.__setattr__(self, "graph_fingerprint", graph)
        object.__setattr__(self, "candidate_set_hash", candidate)
        object.__setattr__(self, "node_id_space", node_space)
        object.__setattr__(self, "score_kind", kind)

    @classmethod
    def build(
        cls,
        ordered_node_ids: Any,
        scores: Optional[Any],
        graph_fingerprint: str,
        candidate_set_hash: str,
        node_id_space: str,
        score_kind: str,
    ) -> "ScorePayload":
        return cls(
            SCORE_PAYLOAD_VERSION,
            ordered_node_ids,
            scores,
            graph_fingerprint,
            candidate_set_hash,
            node_id_space,
            score_kind,
        )

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "graph_fingerprint": self.graph_fingerprint,
            "candidate_set_hash": self.candidate_set_hash,
            "node_id_space": self.node_id_space,
            "score_kind": self.score_kind,
            "ordered_nodes_hash": ordered_int_hash(self.ordered_node_ids),
            "score_values_hash": None
            if self.scores is None
            else sha256_bytes(self.scores.tobytes(order="C")),
        }

    @property
    def canonical_bytes(self) -> bytes:
        entries = [
            ("metadata.json", _plain_json_bytes(self.metadata)),
            ("ordered_node_ids.npy", _npy_bytes(self.ordered_node_ids)),
        ]
        if self.scores is not None:
            entries.append(("scores.npy", _npy_bytes(self.scores)))
        return _archive_bytes(entries)

    @property
    def content_hash(self) -> str:
        return sha256_bytes(self.canonical_bytes)

    @property
    def dependencies(self) -> Tuple[Tuple[str, str], ...]:
        return ()

    @classmethod
    def from_bytes(cls, payload: bytes) -> "ScorePayload":
        try:
            with zipfile.ZipFile(BytesIO(payload), "r") as probe:
                names = probe.namelist()
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            raise ArtifactIntegrityError("Score payload is not a valid archive: {0}".format(exc))
        expected = (
            ["metadata.json", "ordered_node_ids.npy", "scores.npy"]
            if "scores.npy" in names
            else ["metadata.json", "ordered_node_ids.npy"]
        )
        members = _read_archive(payload, expected, "Score payload")
        metadata = _parse_plain_json(members["metadata.json"], "Score metadata")
        required = {
            "payload_version",
            "graph_fingerprint",
            "candidate_set_hash",
            "node_id_space",
            "score_kind",
            "ordered_nodes_hash",
            "score_values_hash",
        }
        if not isinstance(metadata, dict) or set(metadata) != required:
            raise ArtifactIntegrityError("Score metadata schema mismatch")
        try:
            value = cls(
                payload_version=metadata["payload_version"],
                ordered_node_ids=_read_npy(members["ordered_node_ids.npy"], "ordered_node_ids"),
                scores=None
                if "scores.npy" not in members
                else _read_npy(members["scores.npy"], "scores"),
                graph_fingerprint=metadata["graph_fingerprint"],
                candidate_set_hash=metadata["candidate_set_hash"],
                node_id_space=metadata["node_id_space"],
                score_kind=metadata["score_kind"],
            )
        except (CacheV2Error, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError("Score payload contract is invalid: {0}".format(exc))
        if value.metadata != metadata or value.canonical_bytes != payload:
            raise ArtifactIntegrityError("Score payload bytes are not canonical")
        return value

    def validate_against(self, recipe: ArtifactRecipe) -> None:
        fields = _recipe_contract(recipe, SCORE_RECIPE_CONTRACT, "Score")
        if validate_sha256(fields.get("graph_fingerprint"), "Recipe graph_fingerprint") != self.graph_fingerprint:
            raise ArtifactIntegrityError("Score payload graph fingerprint does not match Recipe")
        if validate_sha256(fields.get("candidate_set_hash"), "Recipe candidate_set_hash") != self.candidate_set_hash:
            raise ArtifactIntegrityError("Score payload candidate hash does not match Recipe")
        if _required_text(fields.get("node_id_space"), "Recipe node_id_space") != self.node_id_space:
            raise ArtifactIntegrityError("Score payload node-id space does not match Recipe")
        if _required_text(fields.get("score_kind"), "Recipe score_kind") != self.score_kind:
            raise ArtifactIntegrityError("Score payload kind does not match Recipe")
        num_nodes = _required_integer(fields.get("num_nodes"), "Recipe num_nodes")
        if any(int(node) < 0 or int(node) >= num_nodes for node in self.ordered_node_ids):
            raise ArtifactIntegrityError("Score payload node is outside Recipe num_nodes")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ScorePayload) and self.metadata == other.metadata and np.array_equal(
            self.ordered_node_ids, other.ordered_node_ids
        ) and (
            (self.scores is None and other.scores is None)
            or (
                self.scores is not None
                and other.scores is not None
                and np.array_equal(self.scores, other.scores)
            )
        )


@dataclass(frozen=True, eq=False)
class PredictionPayload:
    payload_version: int
    logits_before: np.ndarray
    logits_unlearned: np.ndarray
    logits_retrained: np.ndarray
    y: np.ndarray
    train_mask: np.ndarray
    test_mask: np.ndarray
    retain_mask: np.ndarray
    selected_nodes: np.ndarray
    class_order: np.ndarray
    graph_fingerprint: str
    split_fingerprint: str
    selection_artifact_id: str
    node_id_space: str

    artifact_type = ArtifactType.PREDICTION
    payload_schema = PREDICTION_PAYLOAD_SCHEMA
    contract_version = PREDICTION_PAYLOAD_VERSION
    file_extension = "npz"

    def __post_init__(self) -> None:
        if self.payload_version != PREDICTION_PAYLOAD_VERSION:
            raise ContractValidationError("unsupported Prediction payload version")
        before = _float_matrix(self.logits_before, "logits_before")
        unlearned = _float_matrix(self.logits_unlearned, "logits_unlearned")
        retrained = _float_matrix(self.logits_retrained, "logits_retrained")
        if before.shape != unlearned.shape or before.shape != retrained.shape:
            raise ArtifactIntegrityError("Prediction logits shapes must match")
        labels = _int_vector(self.y, "y")
        train = _bool_vector(self.train_mask, "train_mask")
        test = _bool_vector(self.test_mask, "test_mask")
        retain = _bool_vector(self.retain_mask, "retain_mask")
        selected = _int_vector(self.selected_nodes, "selected_nodes")
        classes = _int_vector(self.class_order, "class_order")
        num_nodes, num_classes = before.shape
        if any(array.shape != (num_nodes,) for array in (labels, train, test, retain)):
            raise ArtifactIntegrityError("Prediction labels and masks must match logits rows")
        if classes.shape != (num_classes,) or len(set(int(item) for item in classes)) != num_classes:
            raise ArtifactIntegrityError("class_order must be unique and match logits columns")
        if len(set(int(item) for item in selected)) != len(selected):
            raise ArtifactIntegrityError("selected_nodes contains duplicates")
        if any(int(node) < 0 or int(node) >= num_nodes for node in selected):
            raise ArtifactIntegrityError("selected_nodes contains an out-of-range node")
        if not set(int(item) for item in labels).issubset(set(int(item) for item in classes)):
            raise ArtifactIntegrityError("y contains labels outside class_order")
        expected_retain = np.array(train, copy=True)
        expected_retain[selected] = False
        if not np.array_equal(retain, expected_retain):
            raise ArtifactIntegrityError("retain_mask must equal train_mask minus selected_nodes")
        graph = validate_sha256(self.graph_fingerprint, "graph_fingerprint")
        split = validate_sha256(self.split_fingerprint, "split_fingerprint")
        selection = validate_artifact_id(self.selection_artifact_id, "selection_artifact_id")
        if not selection.startswith("sel_"):
            raise ContractValidationError("selection_artifact_id must identify Selection")
        node_space = _required_text(self.node_id_space, "node_id_space")
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
        object.__setattr__(self, "graph_fingerprint", graph)
        object.__setattr__(self, "split_fingerprint", split)
        object.__setattr__(self, "selection_artifact_id", selection)
        object.__setattr__(self, "node_id_space", node_space)

    @classmethod
    def build(cls, **fields: Any) -> "PredictionPayload":
        return cls(payload_version=PREDICTION_PAYLOAD_VERSION, **fields)

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "graph_fingerprint": self.graph_fingerprint,
            "split_fingerprint": self.split_fingerprint,
            "selection_artifact_id": self.selection_artifact_id,
            "node_id_space": self.node_id_space,
            "num_nodes": int(self.logits_before.shape[0]),
            "num_classes": int(self.logits_before.shape[1]),
            "selected_nodes_hash": ordered_int_hash(self.selected_nodes),
            "class_order_hash": ordered_int_hash(self.class_order),
        }

    @property
    def canonical_bytes(self) -> bytes:
        arrays = {
            "class_order.npy": self.class_order,
            "logits_before.npy": self.logits_before,
            "logits_retrained.npy": self.logits_retrained,
            "logits_unlearned.npy": self.logits_unlearned,
            "retain_mask.npy": self.retain_mask,
            "selected_nodes.npy": self.selected_nodes,
            "test_mask.npy": self.test_mask,
            "train_mask.npy": self.train_mask,
            "y.npy": self.y,
        }
        entries = [("metadata.json", _plain_json_bytes(self.metadata))]
        entries.extend((name, _npy_bytes(arrays[name])) for name in sorted(arrays))
        return _archive_bytes(entries)

    @property
    def content_hash(self) -> str:
        return sha256_bytes(self.canonical_bytes)

    @property
    def dependencies(self) -> Tuple[Tuple[str, str], ...]:
        return (("selection_input", self.selection_artifact_id),)

    @classmethod
    def from_bytes(cls, payload: bytes) -> "PredictionPayload":
        array_names = [
            "class_order.npy",
            "logits_before.npy",
            "logits_retrained.npy",
            "logits_unlearned.npy",
            "retain_mask.npy",
            "selected_nodes.npy",
            "test_mask.npy",
            "train_mask.npy",
            "y.npy",
        ]
        expected = ["metadata.json"] + array_names
        members = _read_archive(payload, expected, "Prediction payload")
        metadata = _parse_plain_json(members["metadata.json"], "Prediction metadata")
        required = {
            "payload_version",
            "graph_fingerprint",
            "split_fingerprint",
            "selection_artifact_id",
            "node_id_space",
            "num_nodes",
            "num_classes",
            "selected_nodes_hash",
            "class_order_hash",
        }
        if not isinstance(metadata, dict) or set(metadata) != required:
            raise ArtifactIntegrityError("Prediction metadata schema mismatch")
        arrays = {name[:-4]: _read_npy(members[name], name) for name in array_names}
        try:
            value = cls(
                payload_version=metadata["payload_version"],
                graph_fingerprint=metadata["graph_fingerprint"],
                split_fingerprint=metadata["split_fingerprint"],
                selection_artifact_id=metadata["selection_artifact_id"],
                node_id_space=metadata["node_id_space"],
                **arrays,
            )
        except (CacheV2Error, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError("Prediction payload contract is invalid: {0}".format(exc))
        if value.metadata != metadata or value.canonical_bytes != payload:
            raise ArtifactIntegrityError("Prediction payload bytes are not canonical")
        return value

    def validate_against(self, recipe: ArtifactRecipe) -> None:
        fields = _recipe_contract(recipe, PREDICTION_RECIPE_CONTRACT, "Prediction")
        expected = {
            "graph_fingerprint": self.graph_fingerprint,
            "split_fingerprint": self.split_fingerprint,
            "selection_artifact_id": self.selection_artifact_id,
            "selected_nodes_hash": self.metadata["selected_nodes_hash"],
            "num_nodes": self.metadata["num_nodes"],
            "num_classes": self.metadata["num_classes"],
            "class_order_hash": self.metadata["class_order_hash"],
            "node_id_space": self.node_id_space,
        }
        for name, observed in expected.items():
            if fields.get(name) != observed:
                raise ArtifactIntegrityError(
                    "Prediction payload {0} does not match Recipe".format(name)
                )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PredictionPayload) or self.metadata != other.metadata:
            return False
        names = (
            "logits_before",
            "logits_unlearned",
            "logits_retrained",
            "y",
            "train_mask",
            "test_mask",
            "retain_mask",
            "selected_nodes",
            "class_order",
        )
        return all(np.array_equal(getattr(self, name), getattr(other, name)) for name in names)


@dataclass(frozen=True, eq=False)
class EvaluationPayload:
    payload_version: int
    prediction_artifact_id: str
    graph_fingerprint: str
    metric_name: str
    metric_version: str
    metrics: Mapping[str, Any]

    artifact_type = ArtifactType.EVALUATION
    payload_schema = EVALUATION_PAYLOAD_SCHEMA
    contract_version = EVALUATION_PAYLOAD_VERSION
    file_extension = "json"

    def __post_init__(self) -> None:
        if self.payload_version != EVALUATION_PAYLOAD_VERSION:
            raise ContractValidationError("unsupported Evaluation payload version")
        prediction = validate_artifact_id(self.prediction_artifact_id, "prediction_artifact_id")
        if not prediction.startswith("pred_"):
            raise ContractValidationError("prediction_artifact_id must identify Prediction")
        graph = validate_sha256(self.graph_fingerprint, "graph_fingerprint")
        metric_name = _required_text(self.metric_name, "metric_name")
        metric_version = _required_text(self.metric_version, "metric_version")
        metrics = _required_mapping(self.metrics, "metrics")
        encoded = _plain_json_bytes(metrics)
        metrics = _parse_plain_json(encoded, "Evaluation metrics")
        object.__setattr__(self, "prediction_artifact_id", prediction)
        object.__setattr__(self, "graph_fingerprint", graph)
        object.__setattr__(self, "metric_name", metric_name)
        object.__setattr__(self, "metric_version", metric_version)
        object.__setattr__(self, "metrics", metrics)

    @classmethod
    def build(cls, **fields: Any) -> "EvaluationPayload":
        return cls(payload_version=EVALUATION_PAYLOAD_VERSION, **fields)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "prediction_artifact_id": self.prediction_artifact_id,
            "graph_fingerprint": self.graph_fingerprint,
            "metric_name": self.metric_name,
            "metric_version": self.metric_version,
            "metrics": copy.deepcopy(dict(self.metrics)),
        }

    @property
    def canonical_bytes(self) -> bytes:
        return _plain_json_bytes(self.to_dict())

    @property
    def content_hash(self) -> str:
        return sha256_bytes(self.canonical_bytes)

    @property
    def dependencies(self) -> Tuple[Tuple[str, str], ...]:
        return (("prediction_input", self.prediction_artifact_id),)

    @classmethod
    def from_bytes(cls, payload: bytes) -> "EvaluationPayload":
        value = _parse_plain_json(payload, "Evaluation payload")
        expected = {
            "payload_version",
            "prediction_artifact_id",
            "graph_fingerprint",
            "metric_name",
            "metric_version",
            "metrics",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ArtifactIntegrityError("Evaluation payload schema mismatch")
        try:
            result = cls(**value)
        except (CacheV2Error, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError("Evaluation payload contract is invalid: {0}".format(exc))
        if result.canonical_bytes != payload:
            raise ArtifactIntegrityError("Evaluation payload bytes are not canonical")
        return result

    def validate_against(self, recipe: ArtifactRecipe) -> None:
        fields = _recipe_contract(recipe, EVALUATION_RECIPE_CONTRACT, "Evaluation")
        expected = {
            "prediction_artifact_id": self.prediction_artifact_id,
            "graph_fingerprint": self.graph_fingerprint,
            "metric_name": self.metric_name,
            "metric_version": self.metric_version,
        }
        for name, observed in expected.items():
            if fields.get(name) != observed:
                raise ArtifactIntegrityError(
                    "Evaluation payload {0} does not match Recipe".format(name)
                )

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EvaluationPayload) and self.to_dict() == other.to_dict()


FORMAL_PAYLOAD_TYPES: Dict[ArtifactType, Type[Any]] = {
    ArtifactType.SCORE: ScorePayload,
    ArtifactType.PREDICTION: PredictionPayload,
    ArtifactType.EVALUATION: EvaluationPayload,
}


def payload_type_for(artifact_type: ArtifactType) -> Type[Any]:
    try:
        type_value = ArtifactType(artifact_type)
        return FORMAL_PAYLOAD_TYPES[type_value]
    except (KeyError, TypeError, ValueError):
        raise ContractValidationError(
            "formal payload type must be score, prediction, or evaluation"
        )


def build_score_recipe(
    *,
    graph_fingerprint: str,
    candidate_set_hash: str,
    num_nodes: int,
    node_id_space: str,
    selector_identity: Mapping[str, Any],
    score_algorithm: Mapping[str, Any],
    parameters: Mapping[str, Any],
    producer_version: ProducerVersion,
    score_kind: str = "scores",
) -> ArtifactRecipe:
    return ArtifactRecipe(
        {
            "artifact_contract": SCORE_RECIPE_CONTRACT,
            "graph_fingerprint": validate_sha256(graph_fingerprint, "graph_fingerprint"),
            "candidate_set_hash": validate_sha256(candidate_set_hash, "candidate_set_hash"),
            "num_nodes": _required_integer(num_nodes, "num_nodes"),
            "node_id_space": _required_text(node_id_space, "node_id_space"),
            "selector_identity": _required_mapping(selector_identity, "selector_identity"),
            "score_algorithm": _required_mapping(score_algorithm, "score_algorithm"),
            "score_kind": _required_text(score_kind, "score_kind"),
            "parameters": _required_mapping(parameters, "parameters", allow_empty=True),
            "producer_version": _producer_mapping(producer_version),
        }
    )


def build_prediction_recipe(
    *,
    graph_fingerprint: str,
    split_fingerprint: str,
    selection_artifact_id: str,
    selected_nodes_hash: str,
    num_nodes: int,
    num_classes: int,
    class_order: Sequence[int],
    node_id_space: str,
    target_model_recipe: Mapping[str, Any],
    run_seed: int,
    producer_version: ProducerVersion,
) -> ArtifactRecipe:
    target = _required_mapping(target_model_recipe, "Prediction Artifact target_model_recipe")
    selection = validate_artifact_id(selection_artifact_id, "selection_artifact_id")
    if not selection.startswith("sel_"):
        raise ContractValidationError("Prediction Artifact requires a Selection Artifact ID")
    return ArtifactRecipe(
        {
            "artifact_contract": PREDICTION_RECIPE_CONTRACT,
            "graph_fingerprint": validate_sha256(graph_fingerprint, "graph_fingerprint"),
            "split_fingerprint": validate_sha256(split_fingerprint, "split_fingerprint"),
            "selection_artifact_id": selection,
            "selected_nodes_hash": validate_sha256(selected_nodes_hash, "selected_nodes_hash"),
            "num_nodes": _required_integer(num_nodes, "num_nodes"),
            "num_classes": _required_integer(num_classes, "num_classes", minimum=1),
            "class_order_hash": ordered_int_hash(class_order),
            "node_id_space": _required_text(node_id_space, "node_id_space"),
            "target_model_recipe": target,
            "run_seed": _required_integer(run_seed, "run_seed", minimum=0),
            "producer_version": _producer_mapping(producer_version),
        }
    )


def build_evaluation_recipe(
    *,
    prediction_artifact_id: str,
    graph_fingerprint: str,
    metric_name: str,
    metric_version: str,
    metric_parameters: Mapping[str, Any],
    producer_version: ProducerVersion,
) -> ArtifactRecipe:
    prediction = validate_artifact_id(prediction_artifact_id, "prediction_artifact_id")
    if not prediction.startswith("pred_"):
        raise ContractValidationError("Evaluation Artifact requires a Prediction Artifact ID")
    return ArtifactRecipe(
        {
            "artifact_contract": EVALUATION_RECIPE_CONTRACT,
            "prediction_artifact_id": prediction,
            "graph_fingerprint": validate_sha256(graph_fingerprint, "graph_fingerprint"),
            "metric_name": _required_text(metric_name, "metric_name"),
            "metric_version": _required_text(metric_version, "metric_version"),
            "metric_parameters": _required_mapping(
                metric_parameters, "metric_parameters", allow_empty=True
            ),
            "producer_version": _producer_mapping(producer_version),
        }
    )


__all__ = [
    "EVALUATION_PAYLOAD_SCHEMA",
    "EVALUATION_PAYLOAD_VERSION",
    "EVALUATION_RECIPE_CONTRACT",
    "PREDICTION_PAYLOAD_SCHEMA",
    "PREDICTION_PAYLOAD_VERSION",
    "PREDICTION_RECIPE_CONTRACT",
    "SCORE_PAYLOAD_SCHEMA",
    "SCORE_PAYLOAD_VERSION",
    "SCORE_RECIPE_CONTRACT",
    "EvaluationPayload",
    "PredictionPayload",
    "ScorePayload",
    "build_evaluation_recipe",
    "build_prediction_recipe",
    "build_score_recipe",
    "ordered_int_hash",
    "payload_type_for",
]
