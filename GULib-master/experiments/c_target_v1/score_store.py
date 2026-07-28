"""Typed Cache V2 ScoreBundle payload and exact-only store."""

from __future__ import annotations

import json
import math
import os
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterator, Mapping, Optional, Sequence, Tuple

from cache_v2 import (
    ArtifactHeader,
    ArtifactRecipe,
    ArtifactStatus,
    ArtifactType,
    ProducerVersion,
    RegisterOutcome,
    VerificationStatus,
    build_artifact_id,
    sha256_bytes,
)
from cache_v2.errors import ContractValidationError, PathValidationError
from cache_v2.index import CacheIndex
from cache_v2.resolver import ArtifactResolver
from cache_v2.store import ArtifactStoreError, CacheResolutionError

from .core import ids_hash


PAYLOAD_SCHEMA = "cache_v2.score_bundle.c_target"
PAYLOAD_VERSION = 1


class ScoreBundleIntegrityError(ArtifactStoreError):
    """A formal score payload failed verification."""


class ProducerCalledError(ArtifactStoreError):
    """A warm-hit assertion reached the producer."""


def _plain_json_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(
            "ScoreBundle is not canonical JSON: {0}".format(exc)
        )
    return text.encode("utf-8")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {0}".format(key))
        result[key] = value
    return result


def _parse_bytes(payload: bytes, label: str) -> Any:
    try:
        text = payload.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
        raise ScoreBundleIntegrityError(
            "{0} is invalid canonical JSON: {1}".format(label, exc)
        )
    if _plain_json_bytes(value) != payload:
        raise ScoreBundleIntegrityError(
            "{0} is not canonical JSON".format(label)
        )
    return value


def _candidate_ids(value: Sequence[int]) -> Tuple[int, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise ContractValidationError("candidate ids must be an integer sequence")
    try:
        raw = list(value)
    except TypeError:
        raise ContractValidationError("candidate ids must be an integer sequence")
    result = []
    for position, item in enumerate(raw):
        if isinstance(item, bool) or not isinstance(item, int):
            raise ContractValidationError(
                "candidate id at position {0} must be an integer".format(
                    position
                )
            )
        result.append(int(item))
    if len(set(result)) != len(result):
        raise ContractValidationError("candidate ids contain duplicates")
    return tuple(result)


def _stable_ranking(ids: Tuple[int, ...], scores: Tuple[float, ...]) -> Tuple[int, ...]:
    order = sorted(
        range(len(ids)), key=lambda index: (-scores[index], ids[index])
    )
    return tuple(ids[index] for index in order)


@dataclass(frozen=True)
class ScoreBundlePayload:
    payload_version: int
    candidate_nodes_ordered: Tuple[int, ...]
    candidate_ids_hash: str
    scores: Mapping[str, Tuple[float, ...]]
    rankings: Mapping[str, Tuple[int, ...]]
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        if self.payload_version != PAYLOAD_VERSION:
            raise ContractValidationError(
                "unsupported score payload version {0}".format(
                    self.payload_version
                )
            )
        candidates = _candidate_ids(self.candidate_nodes_ordered)
        observed_hash = ids_hash(candidates)
        if self.candidate_ids_hash != observed_hash:
            raise ContractValidationError(
                "candidate_ids_hash does not match candidate_nodes_ordered"
            )
        if not isinstance(self.scores, Mapping) or not self.scores:
            raise ContractValidationError("scores must be a non-empty mapping")
        if set(self.scores) != set(self.rankings):
            raise ContractValidationError("score and ranking names must match")

        clean_scores: Dict[str, Tuple[float, ...]] = {}
        clean_rankings: Dict[str, Tuple[int, ...]] = {}
        for name in sorted(self.scores):
            if not isinstance(name, str) or not name.strip():
                raise ContractValidationError("score names must be non-empty")
            raw_scores = tuple(float(value) for value in self.scores[name])
            if len(raw_scores) != len(candidates) or any(
                not math.isfinite(value) for value in raw_scores
            ):
                raise ContractValidationError(
                    "score {0} must be finite and candidate-aligned".format(name)
                )
            ranking = _candidate_ids(self.rankings[name])
            if len(ranking) != len(candidates) or set(ranking) != set(candidates):
                raise ContractValidationError(
                    "ranking {0} must contain every candidate once".format(name)
                )
            expected = _stable_ranking(candidates, raw_scores)
            if ranking != expected:
                raise ContractValidationError(
                    "ranking {0} is inconsistent with scores".format(name)
                )
            clean_scores[name] = raw_scores
            clean_rankings[name] = ranking

        try:
            clean_metadata = json.loads(
                _plain_json_bytes(dict(self.metadata)).decode("utf-8")
            )
        except (TypeError, ValueError) as exc:
            raise ContractValidationError(
                "metadata is not canonical JSON: {0}".format(exc)
            )
        object.__setattr__(self, "candidate_nodes_ordered", candidates)
        object.__setattr__(self, "candidate_ids_hash", observed_hash)
        object.__setattr__(self, "scores", clean_scores)
        object.__setattr__(self, "rankings", clean_rankings)
        object.__setattr__(self, "metadata", clean_metadata)

    @classmethod
    def build(
        cls,
        candidate_nodes: Sequence[int],
        scores: Mapping[str, Sequence[float]],
        rankings: Mapping[str, Sequence[int]],
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "ScoreBundlePayload":
        candidates = _candidate_ids(candidate_nodes)
        return cls(
            payload_version=PAYLOAD_VERSION,
            candidate_nodes_ordered=candidates,
            candidate_ids_hash=ids_hash(candidates),
            scores={
                str(name): tuple(float(value) for value in values)
                for name, values in scores.items()
            },
            rankings={
                str(name): tuple(int(value) for value in values)
                for name, values in rankings.items()
            },
            metadata={} if metadata is None else dict(metadata),
        )

    @classmethod
    def from_bytes(cls, payload: bytes) -> "ScoreBundlePayload":
        value = _parse_bytes(payload, "ScoreBundle payload")
        expected = {
            "payload_version",
            "candidate_nodes_ordered",
            "candidate_ids_hash",
            "scores",
            "rankings",
            "metadata",
        }
        if not isinstance(value, dict) or set(value) != expected:
            raise ScoreBundleIntegrityError(
                "ScoreBundle payload schema mismatch"
            )
        try:
            return cls(
                payload_version=value["payload_version"],
                candidate_nodes_ordered=tuple(value["candidate_nodes_ordered"]),
                candidate_ids_hash=value["candidate_ids_hash"],
                scores={
                    name: tuple(values)
                    for name, values in value["scores"].items()
                },
                rankings={
                    name: tuple(values)
                    for name, values in value["rankings"].items()
                },
                metadata=value["metadata"],
            )
        except (ContractValidationError, KeyError, TypeError, ValueError) as exc:
            raise ScoreBundleIntegrityError(
                "ScoreBundle contract is invalid: {0}".format(exc)
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "candidate_nodes_ordered": list(self.candidate_nodes_ordered),
            "candidate_ids_hash": self.candidate_ids_hash,
            "scores": {
                name: list(self.scores[name]) for name in sorted(self.scores)
            },
            "rankings": {
                name: list(self.rankings[name])
                for name in sorted(self.rankings)
            },
            "metadata": dict(self.metadata),
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
        candidate_fields = fields.get("candidate_set", {})
        expected_candidate_hash = candidate_fields.get("ordered_ids_hash")
        if expected_candidate_hash != self.candidate_ids_hash:
            raise ScoreBundleIntegrityError(
                "payload candidates do not match Recipe"
            )
        expected_names = tuple(fields.get("score_names", ()))
        if set(expected_names) != set(self.scores):
            raise ScoreBundleIntegrityError(
                "payload score names do not match Recipe"
            )


@dataclass(frozen=True)
class ScoreStoreResult:
    hit: bool
    outcome: str
    artifact_id: str
    content_hash: str
    semantic_path: str
    payload: ScoreBundlePayload
    producer_called: bool
    miss_reasons: Tuple[str, ...] = ()


class ScoreBundleStore:
    """Small exact-only ScoreArtifact store using Cache V2 contracts/index."""

    def __init__(
        self,
        root: Path,
        *,
        producer_version: ProducerVersion,
        index: Optional[CacheIndex] = None,
        lock_timeout_seconds: float = 30.0,
    ) -> None:
        supplied = Path(root).expanduser()
        if not supplied.is_absolute():
            raise PathValidationError(
                "ScoreBundleStore root must be explicitly absolute"
            )
        if not isinstance(producer_version, ProducerVersion):
            raise ContractValidationError(
                "producer_version must be ProducerVersion"
            )
        self.root = supplied.resolve(strict=False)
        self.producer_version = producer_version
        self.lock_timeout_seconds = float(lock_timeout_seconds)
        self._injected_index = index is not None
        if index is None:
            self.index = CacheIndex((self.root / "index.sqlite3").absolute())
        else:
            if not isinstance(index, CacheIndex):
                raise ContractValidationError("index must be CacheIndex")
            index_path = index.database_path.resolve(strict=False)
            try:
                index_path.relative_to(self.root)
            except ValueError as exc:
                raise PathValidationError(
                    "injected CacheIndex must resolve below the ScoreBundleStore root"
                ) from exc
            self.index = index
        self.producer_call_count = 0

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / ".locks").mkdir(parents=True, exist_ok=True)
        self.index.initialize()
        if self._injected_index:
            self.index.check_schema()

    @contextmanager
    def _recipe_lock(self, recipe: ArtifactRecipe) -> Iterator[None]:
        lock_path = self.root / ".locks" / (
            "score-{0}.lock".format(recipe.recipe_hash)
        )
        deadline = time.monotonic() + self.lock_timeout_seconds
        descriptor = None
        while descriptor is None:
            try:
                descriptor = os.open(
                    str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
                os.write(
                    descriptor,
                    str(os.getpid()).encode("ascii", errors="strict"),
                )
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise CacheResolutionError(
                        "timed out waiting for ScoreBundle recipe lock"
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

    def _paths(
        self, recipe: ArtifactRecipe, artifact_id: str
    ) -> Tuple[str, Path, Path]:
        semantic = (
            "artifacts/score/{0}/{1}/payload.json".format(
                recipe.recipe_hash[:2], artifact_id
            )
        )
        payload_path = self.root.joinpath(*PurePosixPath(semantic).parts)
        return semantic, payload_path, payload_path.with_name("header.json")

    def _load_candidate(
        self,
        candidate: Mapping[str, Any],
        recipe: ArtifactRecipe,
        miss_reasons: Tuple[str, ...],
    ) -> ScoreStoreResult:
        semantic = candidate.get("semantic_path")
        if not isinstance(semantic, str):
            raise ScoreBundleIntegrityError(
                "indexed ScoreArtifact has no semantic path"
            )
        payload_path = self.root.joinpath(*PurePosixPath(semantic).parts)
        header_path = payload_path.with_name("header.json")
        if not payload_path.is_file() or not header_path.is_file():
            raise ScoreBundleIntegrityError(
                "indexed ScoreBundle payload or header is missing"
            )
        payload_bytes = payload_path.read_bytes()
        observed_hash = sha256_bytes(payload_bytes)
        if observed_hash != candidate.get("content_hash"):
            raise ScoreBundleIntegrityError(
                "ScoreBundle payload content hash mismatch"
            )
        header_value = _parse_bytes(
            header_path.read_bytes(), "ScoreBundle header"
        )
        if (
            not isinstance(header_value, dict)
            or set(header_value)
            != {"artifact_header", "payload_contract"}
        ):
            raise ScoreBundleIntegrityError(
                "ScoreBundle header schema mismatch"
            )
        artifact_header = header_value["artifact_header"]
        contract = header_value["payload_contract"]
        expected_contract = {
            "schema": PAYLOAD_SCHEMA,
            "version": PAYLOAD_VERSION,
            "size_bytes": len(payload_bytes),
        }
        if contract != expected_contract:
            raise ScoreBundleIntegrityError(
                "ScoreBundle payload contract mismatch"
            )
        for name, expected in (
            ("artifact_id", candidate.get("artifact_id")),
            ("artifact_type", ArtifactType.SCORE.value),
            ("recipe_hash", recipe.recipe_hash),
            ("content_hash", observed_hash),
            ("semantic_path", semantic),
            ("status", ArtifactStatus.VALID.value),
            ("verification_status", VerificationStatus.VERIFIED.value),
        ):
            if artifact_header.get(name) != expected:
                raise ScoreBundleIntegrityError(
                    "ScoreBundle header {0} mismatch".format(name)
                )
        payload = ScoreBundlePayload.from_bytes(payload_bytes)
        payload.validate_against(recipe)
        return ScoreStoreResult(
            hit=True,
            outcome="hit",
            artifact_id=str(candidate["artifact_id"]),
            content_hash=observed_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def get_or_compute(
        self,
        recipe: ArtifactRecipe,
        producer: Callable[[], ScoreBundlePayload],
        *,
        fail_if_called: bool = False,
    ) -> ScoreStoreResult:
        self.initialize()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        with self._recipe_lock(recipe):
            explanation = ArtifactResolver(self.index).explain_exact(
                ArtifactType.SCORE, recipe
            )
            if explanation.hit and explanation.exact_candidate is not None:
                return self._load_candidate(
                    explanation.exact_candidate,
                    recipe,
                    explanation.miss_reasons,
                )
            if (
                explanation.exact_candidate is not None
                or explanation.miss_reasons != ("no_exact_candidate",)
            ):
                raise CacheResolutionError(
                    "ScoreBundle lookup failed closed: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            if fail_if_called:
                raise ProducerCalledError(
                    "ScoreBundle producer was called on an asserted warm hit"
                )

            started = time.perf_counter()
            self.producer_call_count += 1
            payload = producer()
            compute_seconds = time.perf_counter() - started
            if not isinstance(payload, ScoreBundlePayload):
                raise ContractValidationError(
                    "producer must return ScoreBundlePayload"
                )
            payload.validate_against(recipe)
            content_hash = payload.content_hash
            artifact_id = build_artifact_id(
                ArtifactType.SCORE, recipe.recipe_hash, content_hash
            )
            semantic, payload_path, header_path = self._paths(
                recipe, artifact_id
            )
            metadata = {
                "payload_schema": PAYLOAD_SCHEMA,
                "payload_version": PAYLOAD_VERSION,
                "payload_size_bytes": len(payload.canonical_bytes),
                "score_names": sorted(payload.scores),
            }
            header = ArtifactHeader(
                artifact_type=ArtifactType.SCORE,
                recipe=recipe,
                content_hash=content_hash,
                producer_version=self.producer_version,
                status=ArtifactStatus.VALID,
                verification_status=VerificationStatus.VERIFIED,
                semantic_path=semantic,
                compute_seconds=compute_seconds,
                metadata=metadata,
            )
            header_bytes = _plain_json_bytes(
                {
                    "artifact_header": header.to_dict(),
                    "payload_contract": {
                        "schema": PAYLOAD_SCHEMA,
                        "version": PAYLOAD_VERSION,
                        "size_bytes": len(payload.canonical_bytes),
                    },
                }
            )
            artifact_dir = payload_path.parent
            artifact_parent = artifact_dir.parent
            artifact_parent.mkdir(parents=True, exist_ok=True)
            if artifact_dir.exists():
                raise CacheResolutionError(
                    "unindexed ScoreBundle artifact directory already exists"
                )
            temporary_dir = Path(
                tempfile.mkdtemp(prefix=".tmp-score-", dir=str(artifact_parent))
            )
            try:
                (temporary_dir / "payload.json").write_bytes(
                    payload.canonical_bytes
                )
                (temporary_dir / "header.json").write_bytes(header_bytes)
                os.rename(str(temporary_dir), str(artifact_dir))
            finally:
                if temporary_dir.exists():
                    try:
                        temporary_dir.rmdir()
                    except OSError:
                        pass

            registration = self.index.register_artifact(header)
            if registration.outcome != RegisterOutcome.CREATED:
                raise CacheResolutionError(
                    "unexpected ScoreBundle registration outcome {0}".format(
                        registration.outcome.value
                    )
                )
            return ScoreStoreResult(
                hit=False,
                outcome=registration.outcome.value,
                artifact_id=header.artifact_id,
                content_hash=content_hash,
                semantic_path=semantic,
                payload=payload,
                producer_called=True,
                miss_reasons=explanation.miss_reasons,
            )
