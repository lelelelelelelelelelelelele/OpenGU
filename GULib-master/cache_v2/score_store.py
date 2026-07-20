"""Immutable exact-only Score Artifact payloads and store.

The store owns serialization, integrity checks, exact resolution, and conflict
quarantine.  It never trains a model or computes scores; producers remain in
the experiment layer.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

from .canonical import canonicalize, sha256_bytes
from .contracts import (
    ArtifactConflictRecord,
    ArtifactHeader,
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    ProducerVersion,
    RegisterOutcome,
    VerificationStatus,
    build_artifact_id,
)
from .errors import CacheV2Error, ContractValidationError, PathValidationError
from .index import CacheIndex
from .paths import normalize_semantic_path
from .resolver import ArtifactResolver
from .store import ArtifactStoreError, CacheResolutionError


SCORE_PAYLOAD_SCHEMA = "cache_v2.score_vector"
SCORE_PAYLOAD_VERSION = 1
CONFLICT_MARKER_VERSION = 1


class ScoreArtifactIntegrityError(ArtifactStoreError):
    """A Score payload, header, or index projection failed verification."""


class ScoreArtifactConflictError(ArtifactStoreError):
    """One Recipe produced a second, different Score payload."""

    def __init__(self, conflict_id: str, quarantine_path: str) -> None:
        super().__init__(
            "Score Artifact content conflict {0}; quarantined at {1}".format(
                conflict_id, quarantine_path
            )
        )
        self.conflict_id = str(conflict_id)
        self.quarantine_path = str(quarantine_path)


class ScoreProducerCalledError(ArtifactStoreError):
    """A fail-if-called warm assertion reached the experiment producer."""


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
        raise ContractValidationError(
            "Score payload is not canonical JSON: {0}".format(exc)
        )


def _unique_object(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {0}".format(key))
        result[key] = value
    return result


def _parse_canonical_json(payload: bytes, label: str) -> Any:
    try:
        value = json.loads(
            payload.decode("utf-8"), object_pairs_hook=_unique_object
        )
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
        raise ScoreArtifactIntegrityError(
            "{0} is invalid JSON: {1}".format(label, exc)
        )
    if _plain_json_bytes(value) != payload:
        raise ScoreArtifactIntegrityError("{0} is not canonical JSON".format(label))
    return value


def _integer_nodes(values: Sequence[int]) -> Tuple[int, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise ContractValidationError("candidate nodes must be an integer sequence")
    try:
        raw = tuple(values)
    except TypeError:
        raise ContractValidationError("candidate nodes must be an integer sequence")
    nodes = []
    for position, value in enumerate(raw):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ContractValidationError(
                "candidate node at position {0} must be an integer".format(position)
            )
        nodes.append(int(value))
    if not nodes:
        raise ContractValidationError("candidate nodes must not be empty")
    if len(set(nodes)) != len(nodes):
        raise ContractValidationError("candidate nodes contain duplicates")
    return tuple(nodes)


def ordered_ids_hash(values: Sequence[int]) -> str:
    """Canonical hash for an ordered integer ID sequence."""

    return sha256_bytes(_plain_json_bytes(list(_integer_nodes(values))))


def _stable_ranking(
    candidate_nodes: Tuple[int, ...], scores: Tuple[float, ...]
) -> Tuple[int, ...]:
    order = sorted(
        range(len(candidate_nodes)),
        key=lambda index: (-scores[index], candidate_nodes[index]),
    )
    return tuple(candidate_nodes[index] for index in order)


@dataclass(frozen=True)
class ScorePayload:
    """One candidate-aligned score vector plus deterministic full ranking."""

    payload_version: int
    score_name: str
    candidate_nodes_ordered: Tuple[int, ...]
    candidate_ids_hash: str
    scores: Tuple[float, ...]
    ranking: Tuple[int, ...]
    output_provenance: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.payload_version != SCORE_PAYLOAD_VERSION:
            raise ContractValidationError(
                "unsupported Score payload version {0}; expected {1}".format(
                    self.payload_version, SCORE_PAYLOAD_VERSION
                )
            )
        if not isinstance(self.score_name, str) or not self.score_name.strip():
            raise ContractValidationError("score_name must be non-empty")
        candidates = _integer_nodes(self.candidate_nodes_ordered)
        observed_ids_hash = ordered_ids_hash(candidates)
        if self.candidate_ids_hash != observed_ids_hash:
            raise ContractValidationError(
                "candidate_ids_hash does not match candidate_nodes_ordered"
            )
        try:
            scores = tuple(float(value) for value in self.scores)
        except (TypeError, ValueError):
            raise ContractValidationError("scores must be a numeric sequence")
        if len(scores) != len(candidates) or any(
            not math.isfinite(value) for value in scores
        ):
            raise ContractValidationError(
                "scores must be finite and aligned with candidate nodes"
            )
        ranking = _integer_nodes(self.ranking)
        if len(ranking) != len(candidates) or set(ranking) != set(candidates):
            raise ContractValidationError(
                "ranking must contain every candidate exactly once"
            )
        if ranking != _stable_ranking(candidates, scores):
            raise ContractValidationError(
                "ranking must use score-descending, node-id-ascending order"
            )
        if not isinstance(self.output_provenance, Mapping):
            raise ContractValidationError("output_provenance must be a mapping")
        try:
            provenance = json.loads(
                _plain_json_bytes(dict(self.output_provenance)).decode("utf-8")
            )
        except (TypeError, ValueError) as exc:
            raise ContractValidationError(
                "output_provenance is not canonical JSON: {0}".format(exc)
            )
        object.__setattr__(self, "score_name", self.score_name.strip())
        object.__setattr__(self, "candidate_nodes_ordered", candidates)
        object.__setattr__(self, "candidate_ids_hash", observed_ids_hash)
        object.__setattr__(self, "scores", scores)
        object.__setattr__(self, "ranking", ranking)
        object.__setattr__(self, "output_provenance", provenance)

    @classmethod
    def build(
        cls,
        *,
        score_name: str,
        candidate_nodes: Sequence[int],
        scores: Sequence[float],
        output_provenance: Optional[Mapping[str, Any]] = None,
    ) -> "ScorePayload":
        candidates = _integer_nodes(candidate_nodes)
        score_values = tuple(float(value) for value in scores)
        return cls(
            payload_version=SCORE_PAYLOAD_VERSION,
            score_name=str(score_name),
            candidate_nodes_ordered=candidates,
            candidate_ids_hash=ordered_ids_hash(candidates),
            scores=score_values,
            ranking=_stable_ranking(candidates, score_values),
            output_provenance=(
                {} if output_provenance is None else dict(output_provenance)
            ),
        )

    @classmethod
    def from_bytes(cls, payload: bytes) -> "ScorePayload":
        value = _parse_canonical_json(payload, "Score payload")
        expected = {
            "payload_version",
            "score_name",
            "candidate_nodes_ordered",
            "candidate_ids_hash",
            "scores",
            "ranking",
            "output_provenance",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ScoreArtifactIntegrityError("Score payload schema mismatch")
        try:
            return cls(
                payload_version=value["payload_version"],
                score_name=value["score_name"],
                candidate_nodes_ordered=tuple(value["candidate_nodes_ordered"]),
                candidate_ids_hash=value["candidate_ids_hash"],
                scores=tuple(value["scores"]),
                ranking=tuple(value["ranking"]),
                output_provenance=value["output_provenance"],
            )
        except (ContractValidationError, KeyError, TypeError, ValueError) as exc:
            raise ScoreArtifactIntegrityError(
                "Score payload contract is invalid: {0}".format(exc)
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "score_name": self.score_name,
            "candidate_nodes_ordered": list(self.candidate_nodes_ordered),
            "candidate_ids_hash": self.candidate_ids_hash,
            "scores": list(self.scores),
            "ranking": list(self.ranking),
            "output_provenance": dict(self.output_provenance),
        }

    @property
    def canonical_bytes(self) -> bytes:
        return _plain_json_bytes(self.to_dict())

    @property
    def content_hash(self) -> str:
        return sha256_bytes(self.canonical_bytes)

    def validate_against(self, recipe: ArtifactRecipe) -> None:
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        fields = recipe.fields
        candidate_set = fields.get("candidate_set")
        if not isinstance(candidate_set, Mapping):
            raise ScoreArtifactIntegrityError("Recipe candidate_set is missing")
        if candidate_set.get("ordered_ids_hash") != self.candidate_ids_hash:
            raise ScoreArtifactIntegrityError(
                "Score payload candidates do not match Recipe"
            )
        if fields.get("score_name") != self.score_name:
            raise ScoreArtifactIntegrityError(
                "Score payload name does not match Recipe"
            )


@dataclass(frozen=True)
class ScoreStoreResult:
    hit: bool
    outcome: str
    artifact_id: str
    content_hash: str
    semantic_path: str
    payload: ScorePayload
    producer_called: bool
    miss_reasons: Tuple[str, ...] = ()


class ScoreArtifactStore:
    """Exact-only immutable store for formal Score Artifacts."""

    def __init__(
        self,
        root: Union[str, Path],
        *,
        producer_version: ProducerVersion,
        lock_timeout_seconds: float = 30.0,
    ) -> None:
        supplied = Path(root).expanduser()
        if not supplied.is_absolute():
            raise PathValidationError(
                "ScoreArtifactStore root must be explicitly absolute"
            )
        if ".." in supplied.parts:
            raise PathValidationError("ScoreArtifactStore root must not contain '..'")
        if not isinstance(producer_version, ProducerVersion):
            raise ContractValidationError(
                "producer_version must be ProducerVersion"
            )
        if not producer_version.is_identified:
            raise ContractValidationError(
                "producer_version must identify its producer"
            )
        if (
            isinstance(lock_timeout_seconds, bool)
            or not isinstance(lock_timeout_seconds, (int, float))
            or not math.isfinite(float(lock_timeout_seconds))
            or float(lock_timeout_seconds) <= 0
        ):
            raise ContractValidationError(
                "lock_timeout_seconds must be finite and positive"
            )
        self.root = supplied.resolve(strict=False)
        self.producer_version = producer_version
        self.lock_timeout_seconds = float(lock_timeout_seconds)
        self.index = CacheIndex(self.root / "index.sqlite")
        self.producer_call_count = 0

    def _safe_path(self, path: Path, label: str) -> Path:
        if ".." in Path(path).parts:
            raise PathValidationError("{0} must not contain '..'".format(label))
        resolved = Path(path).resolve(strict=False)
        try:
            relative = resolved.relative_to(self.root)
        except ValueError:
            raise PathValidationError(
                "{0} must stay below ScoreArtifactStore root".format(label)
            )
        if not relative.parts:
            raise PathValidationError(
                "{0} must be below ScoreArtifactStore root".format(label)
            )
        return resolved

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self._safe_path(self.index.database_path, "CacheIndex database")
        self.index.initialize()

    def _ensure_initialized(self) -> None:
        if not self.root.is_dir() or not self.index.database_path.is_file():
            raise ArtifactStoreError("ScoreArtifactStore is not initialized")
        self.index.check_schema()

    @contextmanager
    def _recipe_lock(self, recipe: ArtifactRecipe) -> Iterator[None]:
        lock_dir = self._safe_path(self.root / ".locks", "lock directory")
        lock_dir.mkdir(parents=True, exist_ok=True)
        lock_path = self._safe_path(
            lock_dir / ("score-{0}.lock".format(recipe.recipe_hash)),
            "recipe lock",
        )
        deadline = time.monotonic() + self.lock_timeout_seconds
        descriptor: Optional[int] = None
        while descriptor is None:
            try:
                descriptor = os.open(
                    str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600
                )
                os.write(descriptor, str(os.getpid()).encode("ascii"))
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise CacheResolutionError(
                        "timed out waiting for Score Artifact recipe lock"
                    )
                time.sleep(0.05)
        try:
            yield
        finally:
            if descriptor is not None:
                os.close(descriptor)
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass

    def _artifact_paths(
        self, recipe: ArtifactRecipe, artifact_id: str
    ) -> Tuple[str, Path, Path]:
        semantic = normalize_semantic_path(
            "artifacts/score/{0}/{1}/payload.json".format(
                recipe.recipe_hash[:2], artifact_id
            )
        )
        payload_path = self._safe_path(
            self.root.joinpath(*PurePosixPath(semantic).parts), "Score payload"
        )
        return semantic, payload_path, payload_path.with_name("header.json")

    def _header(
        self,
        recipe: ArtifactRecipe,
        payload: ScorePayload,
        semantic_path: str,
        compute_seconds: float,
    ) -> ArtifactHeader:
        return ArtifactHeader(
            artifact_type=ArtifactType.SCORE,
            recipe=recipe,
            content_hash=payload.content_hash,
            producer_version=self.producer_version,
            status=ArtifactStatus.VALID,
            verification_status=VerificationStatus.VERIFIED,
            semantic_path=semantic_path,
            compute_seconds=float(compute_seconds),
            metadata={
                "payload_schema": SCORE_PAYLOAD_SCHEMA,
                "payload_version": SCORE_PAYLOAD_VERSION,
                "payload_size_bytes": len(payload.canonical_bytes),
                "score_name": payload.score_name,
            },
        )

    def _sidecar_bytes(self, header: ArtifactHeader, payload_size: int) -> bytes:
        return _plain_json_bytes(
            {
                "artifact_header": header.to_dict(),
                "payload_contract": {
                    "schema": SCORE_PAYLOAD_SCHEMA,
                    "version": SCORE_PAYLOAD_VERSION,
                    "size_bytes": int(payload_size),
                },
            }
        )

    def _publish_directory(
        self, directory: Path, files: Mapping[str, bytes]
    ) -> None:
        directory = self._safe_path(directory, "published Artifact directory")
        parent = self._safe_path(directory.parent, "Artifact parent")
        parent.mkdir(parents=True, exist_ok=True)
        if directory.exists():
            raise CacheResolutionError(
                "unindexed Score Artifact directory already exists"
            )
        temporary = Path(tempfile.mkdtemp(prefix=".tmp-score-", dir=str(parent)))
        try:
            for name, payload in files.items():
                (temporary / name).write_bytes(payload)
            os.replace(str(temporary), str(directory))
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)

    def _marker_path(self, recipe: ArtifactRecipe) -> Tuple[str, Path]:
        semantic = normalize_semantic_path(
            "conflict_markers/score/{0}/marker.json".format(
                recipe.recipe_hash[:24]
            )
        )
        return semantic, self._safe_path(
            self.root.joinpath(*PurePosixPath(semantic).parts),
            "Score conflict marker",
        )

    def _assert_no_conflict_marker(self, recipe: ArtifactRecipe) -> None:
        semantic, marker_path = self._marker_path(recipe)
        if not marker_path.exists():
            return
        if marker_path.is_symlink() or not marker_path.is_file():
            raise CacheResolutionError(
                "Score conflict marker is not a regular file: {0}".format(semantic)
            )
        value = _parse_canonical_json(
            marker_path.read_bytes(), "Score conflict marker"
        )
        expected = {
            "artifact_type",
            "existing_artifact_id",
            "existing_content_hash",
            "marker_version",
            "observed_content_hash",
            "reason",
            "recipe_hash",
        }
        if (
            not isinstance(value, dict)
            or set(value) != expected
            or value.get("artifact_type") != ArtifactType.SCORE.value
            or value.get("marker_version") != CONFLICT_MARKER_VERSION
            or value.get("reason") != "content_conflict"
            or value.get("recipe_hash") != recipe.recipe_hash
        ):
            raise CacheResolutionError("Score conflict marker is invalid")
        raise CacheResolutionError(
            "durable Score conflict marker blocks exact hit for Recipe {0}".format(
                recipe.recipe_hash
            )
        )

    def _write_marker(
        self,
        recipe: ArtifactRecipe,
        *,
        existing_artifact_id: str,
        existing_content_hash: str,
        observed_content_hash: str,
    ) -> str:
        semantic, marker_path = self._marker_path(recipe)
        marker = {
            "artifact_type": ArtifactType.SCORE.value,
            "existing_artifact_id": str(existing_artifact_id),
            "existing_content_hash": str(existing_content_hash),
            "marker_version": CONFLICT_MARKER_VERSION,
            "observed_content_hash": str(observed_content_hash),
            "reason": "content_conflict",
            "recipe_hash": recipe.recipe_hash,
        }
        if marker_path.exists():
            return semantic
        marker_path.parent.mkdir(parents=True, exist_ok=False)
        temporary = marker_path.with_name(".marker-{0}.tmp".format(os.getpid()))
        temporary.write_bytes(_plain_json_bytes(marker))
        try:
            os.replace(str(temporary), str(marker_path))
        finally:
            if temporary.exists():
                temporary.unlink()
        return semantic

    def _quarantine(
        self,
        recipe: ArtifactRecipe,
        payload: ScorePayload,
        header: ArtifactHeader,
    ) -> str:
        semantic = normalize_semantic_path(
            "quarantine/score/{0}/{1}/payload.json".format(
                recipe.recipe_hash[:24], payload.content_hash[:24]
            )
        )
        payload_path = self._safe_path(
            self.root.joinpath(*PurePosixPath(semantic).parts),
            "Score quarantine payload",
        )
        directory = payload_path.parent
        if directory.exists():
            existing = payload_path.read_bytes() if payload_path.is_file() else None
            if existing != payload.canonical_bytes:
                raise CacheResolutionError(
                    "Score quarantine path already contains different content"
                )
            return semantic
        self._publish_directory(
            directory,
            {
                "payload.json": payload.canonical_bytes,
                "header.json": self._sidecar_bytes(
                    header, len(payload.canonical_bytes)
                ),
            },
        )
        return semantic

    def _load_candidate(
        self,
        candidate: Mapping[str, Any],
        recipe: ArtifactRecipe,
        miss_reasons: Tuple[str, ...],
    ) -> ScoreStoreResult:
        semantic = candidate.get("semantic_path")
        if not isinstance(semantic, str):
            raise ScoreArtifactIntegrityError(
                "indexed Score Artifact has no semantic path"
            )
        try:
            normalized = normalize_semantic_path(semantic)
            payload_path = self._safe_path(
                self.root.joinpath(*PurePosixPath(normalized).parts),
                "indexed Score payload",
            )
        except PathValidationError as exc:
            raise ScoreArtifactIntegrityError(
                "indexed Score path escapes store root: {0}".format(exc)
            )
        header_path = payload_path.with_name("header.json")
        if not payload_path.is_file() or not header_path.is_file():
            raise ScoreArtifactIntegrityError(
                "indexed Score payload or header is missing"
            )
        payload_bytes = payload_path.read_bytes()
        observed_hash = sha256_bytes(payload_bytes)
        if observed_hash != candidate.get("content_hash"):
            raise ScoreArtifactIntegrityError("Score payload content hash mismatch")
        header_value = _parse_canonical_json(
            header_path.read_bytes(), "Score header"
        )
        if not isinstance(header_value, dict) or set(header_value) != {
            "artifact_header",
            "payload_contract",
        }:
            raise ScoreArtifactIntegrityError("Score header schema mismatch")
        artifact_header = header_value["artifact_header"]
        contract = header_value["payload_contract"]
        if not isinstance(artifact_header, dict) or contract != {
            "schema": SCORE_PAYLOAD_SCHEMA,
            "version": SCORE_PAYLOAD_VERSION,
            "size_bytes": len(payload_bytes),
        }:
            raise ScoreArtifactIntegrityError("Score payload contract mismatch")
        producer_value = artifact_header.get("producer_version")
        expected_metadata = {
            "payload_schema": SCORE_PAYLOAD_SCHEMA,
            "payload_version": SCORE_PAYLOAD_VERSION,
            "payload_size_bytes": len(payload_bytes),
            "score_name": recipe.fields.get("score_name"),
        }
        try:
            versioned = ArtifactHeader(
                header_version=artifact_header["header_version"],
                artifact_id=artifact_header["artifact_id"],
                artifact_type=artifact_header["artifact_type"],
                recipe=recipe,
                content_hash=artifact_header["content_hash"],
                producer_version=ProducerVersion(**producer_value),
                status=artifact_header["status"],
                verification_status=artifact_header["verification_status"],
                semantic_path=artifact_header["semantic_path"],
                compute_seconds=artifact_header["compute_seconds"],
                created_at=artifact_header["created_at"],
                metadata=expected_metadata,
            )
        except (CacheV2Error, KeyError, TypeError, ValueError) as exc:
            raise ScoreArtifactIntegrityError(
                "Score header violates the versioned contract: {0}".format(exc)
            )
        if versioned.to_dict() != artifact_header:
            raise ScoreArtifactIntegrityError(
                "Score header fields are not self-consistent"
            )
        expectations = {
            "artifact_id": versioned.artifact_id,
            "artifact_type": ArtifactType.SCORE.value,
            "recipe_hash": recipe.recipe_hash,
            "content_hash": observed_hash,
            "semantic_path": normalized,
            "status": ArtifactStatus.VALID.value,
            "verification_status": VerificationStatus.VERIFIED.value,
            "producer_version": canonicalize(self.producer_version.to_dict()),
            "metadata": canonicalize(expected_metadata),
        }
        for key, expected in expectations.items():
            if candidate.get(key) != expected:
                raise ScoreArtifactIntegrityError(
                    "Score index/header mismatch for {0}".format(key)
                )
        payload = ScorePayload.from_bytes(payload_bytes)
        payload.validate_against(recipe)
        return ScoreStoreResult(
            hit=True,
            outcome="hit",
            artifact_id=str(candidate["artifact_id"]),
            content_hash=observed_hash,
            semantic_path=normalized,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def _store_under_lock(
        self,
        recipe: ArtifactRecipe,
        payload: ScorePayload,
        *,
        compute_seconds: float,
        miss_reasons: Tuple[str, ...],
        producer_called: bool,
    ) -> ScoreStoreResult:
        explanation = ArtifactResolver(self.index).explain_exact(
            ArtifactType.SCORE, recipe
        )
        if explanation.exact_candidate is not None:
            if not explanation.hit:
                raise CacheResolutionError(
                    "indexed Score Artifact is not safely resolvable: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            existing = self._load_candidate(
                explanation.exact_candidate, recipe, explanation.miss_reasons
            )
            if existing.content_hash == payload.content_hash:
                return ScoreStoreResult(
                    hit=True,
                    outcome="hit",
                    artifact_id=existing.artifact_id,
                    content_hash=existing.content_hash,
                    semantic_path=existing.semantic_path,
                    payload=existing.payload,
                    producer_called=producer_called,
                    miss_reasons=explanation.miss_reasons,
                )
            observed_id = build_artifact_id(
                ArtifactType.SCORE, recipe.recipe_hash, payload.content_hash
            )
            quarantine_semantic = normalize_semantic_path(
                "quarantine/score/{0}/{1}/payload.json".format(
                    recipe.recipe_hash[:24], payload.content_hash[:24]
                )
            )
            observed_header = self._header(
                recipe, payload, quarantine_semantic, compute_seconds
            )
            quarantine_path = self._quarantine(
                recipe, payload, observed_header
            )
            self._write_marker(
                recipe,
                existing_artifact_id=existing.artifact_id,
                existing_content_hash=existing.content_hash,
                observed_content_hash=payload.content_hash,
            )
            conflict = ArtifactConflictRecord(
                artifact_type=ArtifactType.SCORE,
                recipe_hash=recipe.recipe_hash,
                existing_artifact_id=existing.artifact_id,
                existing_content_hash=existing.content_hash,
                observed_content_hash=payload.content_hash,
                quarantine_path=quarantine_path,
                metadata={"observed_artifact_id": observed_id},
            )
            self.index.record_conflict(conflict)
            raise ScoreArtifactConflictError(
                conflict.conflict_id, quarantine_path
            )
        if explanation.miss_reasons != ("no_exact_candidate",):
            raise CacheResolutionError(
                "Score Artifact lookup failed closed: {0}".format(
                    ",".join(explanation.miss_reasons)
                )
            )

        payload.validate_against(recipe)
        artifact_id = build_artifact_id(
            ArtifactType.SCORE, recipe.recipe_hash, payload.content_hash
        )
        semantic, payload_path, _ = self._artifact_paths(recipe, artifact_id)
        header = self._header(recipe, payload, semantic, compute_seconds)
        self._publish_directory(
            payload_path.parent,
            {
                "payload.json": payload.canonical_bytes,
                "header.json": self._sidecar_bytes(
                    header, len(payload.canonical_bytes)
                ),
            },
        )
        registration = self.index.register_artifact(header)
        if registration.outcome != RegisterOutcome.CREATED:
            raise CacheResolutionError(
                "unexpected Score registration outcome {0}".format(
                    registration.outcome.value
                )
            )
        return ScoreStoreResult(
            hit=False,
            outcome=registration.outcome.value,
            artifact_id=header.artifact_id,
            content_hash=payload.content_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=producer_called,
            miss_reasons=miss_reasons,
        )

    def load(self, recipe: ArtifactRecipe) -> ScoreStoreResult:
        self._ensure_initialized()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        with self._recipe_lock(recipe):
            self._assert_no_conflict_marker(recipe)
            explanation = ArtifactResolver(self.index).explain_exact(
                ArtifactType.SCORE, recipe
            )
            if not explanation.hit or explanation.exact_candidate is None:
                raise CacheResolutionError(
                    "exact Score Artifact is not resolvable: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            return self._load_candidate(
                explanation.exact_candidate, recipe, explanation.miss_reasons
            )

    def store_score(
        self,
        recipe: ArtifactRecipe,
        payload: ScorePayload,
        *,
        compute_seconds: float = 0.0,
    ) -> ScoreStoreResult:
        self.initialize()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        if not isinstance(payload, ScorePayload):
            raise ContractValidationError("payload must be ScorePayload")
        if (
            isinstance(compute_seconds, bool)
            or not isinstance(compute_seconds, (int, float))
            or not math.isfinite(float(compute_seconds))
            or float(compute_seconds) < 0
        ):
            raise ContractValidationError(
                "compute_seconds must be finite and non-negative"
            )
        payload.validate_against(recipe)
        with self._recipe_lock(recipe):
            self._assert_no_conflict_marker(recipe)
            return self._store_under_lock(
                recipe,
                payload,
                compute_seconds=float(compute_seconds),
                miss_reasons=("no_exact_candidate",),
                producer_called=False,
            )

    def get_or_compute(
        self,
        recipe: ArtifactRecipe,
        producer: Callable[[], ScorePayload],
        *,
        fail_if_producer_called: bool = False,
    ) -> ScoreStoreResult:
        self.initialize()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        if not callable(producer):
            raise ContractValidationError("producer must be callable")
        with self._recipe_lock(recipe):
            self._assert_no_conflict_marker(recipe)
            explanation = ArtifactResolver(self.index).explain_exact(
                ArtifactType.SCORE, recipe
            )
            if explanation.hit and explanation.exact_candidate is not None:
                return self._load_candidate(
                    explanation.exact_candidate,
                    recipe,
                    explanation.miss_reasons,
                )
            if explanation.miss_reasons != ("no_exact_candidate",):
                raise CacheResolutionError(
                    "Score Artifact lookup failed closed: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            if fail_if_producer_called:
                raise ScoreProducerCalledError(
                    "Score producer was called on an asserted warm hit"
                )
            started = time.perf_counter()
            self.producer_call_count += 1
            payload = producer()
            compute_seconds = time.perf_counter() - started
            if not isinstance(payload, ScorePayload):
                raise ContractValidationError(
                    "Score producer must return ScorePayload"
                )
            return self._store_under_lock(
                recipe,
                payload,
                compute_seconds=compute_seconds,
                miss_reasons=explanation.miss_reasons,
                producer_called=True,
            )


__all__ = [
    "SCORE_PAYLOAD_SCHEMA",
    "SCORE_PAYLOAD_VERSION",
    "ScoreArtifactConflictError",
    "ScoreArtifactIntegrityError",
    "ScoreArtifactStore",
    "ScorePayload",
    "ScoreProducerCalledError",
    "ScoreStoreResult",
    "ordered_ids_hash",
]
