"""Versioned, payload-free Cache V2 machine contracts.

The dataclasses in this module validate metadata only.  They never create a
directory, open a database, or write an Artifact payload.
"""

from __future__ import unicode_literals

import copy
import json
import math
import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from .canonical import (
    canonical_json,
    canonical_sha256,
    canonicalize,
    reject_forbidden_recipe_fields,
)
from .errors import ContractValidationError, HashValidationError
from .paths import normalize_semantic_path, normalize_source_path


HEADER_VERSION = 1
RECIPE_VERSION = 1
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ARTIFACT_ID_RE = re.compile(r"^(?:score|sel|pred|eval)_[0-9a-f]{8}_[0-9a-f]{8}$")


class _ValueEnum(str, Enum):
    def __str__(self):
        return self.value


class ArtifactType(_ValueEnum):
    SCORE = "score"
    SELECTION = "selection"
    PREDICTION = "prediction"
    EVALUATION = "evaluation"


class ArtifactStatus(_ValueEnum):
    VALID = "valid"
    DEGRADED = "degraded"
    INVALID = "invalid"
    CORRUPT = "corrupt"
    MISSING = "missing"
    RETIRED = "retired"
    UNKNOWN = "unknown"
    CONFLICT = "conflict"


class VerificationStatus(_ValueEnum):
    VERIFIED = "verified"
    DEGRADED = "degraded"
    INVALID = "invalid"
    CORRUPT = "corrupt"
    MISSING = "missing"
    UNKNOWN = "unknown"


class PathKind(_ValueEnum):
    RELATIVE = "relative"
    ABSOLUTE = "absolute"


class RegisterOutcome(_ValueEnum):
    CREATED = "created"
    IDENTICAL = "identical"
    CONFLICT = "conflict"


ARTIFACT_ID_PREFIXES = {
    ArtifactType.SCORE: "score",
    ArtifactType.SELECTION: "sel",
    ArtifactType.PREDICTION: "pred",
    ArtifactType.EVALUATION: "eval",
}


def utc_now_iso():
    """Return a stable UTC RFC 3339 timestamp."""

    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _normalize_text(value, label):
    if not isinstance(value, str):
        raise ContractValidationError("{0} must be a string".format(label))
    value = unicodedata.normalize("NFC", value).strip()
    if not value:
        raise ContractValidationError("{0} must not be empty".format(label))
    if "\x00" in value:
        raise ContractValidationError("{0} contains a NUL byte".format(label))
    return value


def _coerce_enum(enum_type, value, label):
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(value)
    except (TypeError, ValueError):
        allowed = ", ".join(item.value for item in enum_type)
        raise ContractValidationError(
            "{0} must be one of [{1}], got {2!r}".format(label, allowed, value)
        )


def validate_sha256(value, label="SHA-256"):
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise HashValidationError(
            "{0} must be exactly 64 lowercase hexadecimal characters".format(label)
        )
    return value


def validate_artifact_id(value, label="artifact_id"):
    value = _normalize_text(value, label)
    if ARTIFACT_ID_RE.fullmatch(value) is None:
        raise ContractValidationError(
            "{0} must match <type-prefix>_<recipe8>_<content8>".format(label)
        )
    return value


def _normalize_utc_timestamp(value, label):
    value = _normalize_text(value, label)
    parse_value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(parse_value)
    except ValueError:
        raise ContractValidationError("{0} must be an ISO-8601 timestamp".format(label))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractValidationError("{0} must include a UTC offset".format(label))
    if parsed.utcoffset().total_seconds() != 0:
        raise ContractValidationError("{0} must be normalized to UTC".format(label))
    return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _copy_mapping(value, label):
    if not isinstance(value, Mapping):
        raise ContractValidationError("{0} must be a mapping".format(label))
    copied = copy.deepcopy(dict(value))
    canonicalize(copied)  # validate supported, deterministic value types
    return copied


class ArtifactRecipe(object):
    """A minimal Artifact identity recipe, never a full experiment config."""

    __slots__ = ("_fields", "recipe_version", "_canonical_json", "_recipe_hash")

    def __init__(self, fields, recipe_version=RECIPE_VERSION):
        if not isinstance(fields, Mapping):
            raise ContractValidationError("ArtifactRecipe.fields must be a mapping")
        if isinstance(recipe_version, bool) or not isinstance(recipe_version, int):
            raise ContractValidationError("recipe_version must be an integer")
        if recipe_version != RECIPE_VERSION:
            raise ContractValidationError(
                "unsupported Recipe version {0}; expected {1}".format(
                    recipe_version, RECIPE_VERSION
                )
            )

        reject_forbidden_recipe_fields(fields)
        copied_fields = copy.deepcopy(dict(fields))
        payload = {"recipe_version": recipe_version, "fields": copied_fields}
        serialized = canonical_json(payload)

        self._fields = copied_fields
        self.recipe_version = recipe_version
        self._canonical_json = serialized
        self._recipe_hash = canonical_sha256(payload)

    @classmethod
    def from_mapping(cls, fields, recipe_version=RECIPE_VERSION):
        return cls(fields=fields, recipe_version=recipe_version)

    @property
    def fields(self):
        return copy.deepcopy(self._fields)

    @property
    def canonical_json(self):
        return self._canonical_json

    @property
    def canonical_bytes(self):
        return self._canonical_json.encode("utf-8")

    @property
    def canonical_form(self):
        return json.loads(self._canonical_json)

    @property
    def recipe_hash(self):
        return self._recipe_hash

    def to_dict(self):
        return {"recipe_version": self.recipe_version, "fields": self.fields}

    def __eq__(self, other):
        if not isinstance(other, ArtifactRecipe):
            return NotImplemented
        return self._canonical_json == other._canonical_json

    def __hash__(self):
        return hash(self._canonical_json)

    def __repr__(self):
        return "ArtifactRecipe(recipe_version={0}, recipe_hash={1!r})".format(
            self.recipe_version, self.recipe_hash
        )


@dataclass(frozen=True)
class ProducerVersion:
    """Producer identity supporting semantic and source versions together."""

    semantic_version: Optional[str] = None
    source_fingerprint: Optional[str] = None

    def __post_init__(self):
        for field_name in ("semantic_version", "source_fingerprint"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _normalize_text(value, field_name))

    @property
    def is_identified(self):
        return self.semantic_version is not None or self.source_fingerprint is not None

    def to_dict(self):
        return {
            "semantic_version": self.semantic_version,
            "source_fingerprint": self.source_fingerprint,
        }


def build_artifact_id(artifact_type, recipe_hash, content_hash):
    artifact_type = _coerce_enum(ArtifactType, artifact_type, "artifact_type")
    recipe_hash = validate_sha256(recipe_hash, "recipe_hash")
    content_hash = validate_sha256(content_hash, "content_hash")
    return "{0}_{1}_{2}".format(
        ARTIFACT_ID_PREFIXES[artifact_type], recipe_hash[:8], content_hash[:8]
    )


@dataclass(frozen=True)
class ArtifactHeader:
    """Unified V2.1 metadata/header model; contains no payload bytes."""

    artifact_type: ArtifactType
    recipe: ArtifactRecipe
    content_hash: str
    producer_version: ProducerVersion
    status: ArtifactStatus
    verification_status: VerificationStatus = VerificationStatus.VERIFIED
    artifact_id: Optional[str] = None
    semantic_path: Optional[str] = None
    compute_seconds: Optional[float] = None
    created_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping = field(default_factory=dict)
    header_version: int = HEADER_VERSION

    def __post_init__(self):
        artifact_type = _coerce_enum(ArtifactType, self.artifact_type, "artifact_type")
        status = _coerce_enum(ArtifactStatus, self.status, "status")
        verification_status = _coerce_enum(
            VerificationStatus, self.verification_status, "verification_status"
        )
        if not isinstance(self.recipe, ArtifactRecipe):
            raise ContractValidationError(
                "ArtifactHeader.recipe must be an explicitly projected ArtifactRecipe"
            )
        if not isinstance(self.producer_version, ProducerVersion):
            raise ContractValidationError("producer_version must be ProducerVersion")
        if self.header_version != HEADER_VERSION:
            raise ContractValidationError(
                "unsupported Artifact header version {0}; expected {1}".format(
                    self.header_version, HEADER_VERSION
                )
            )

        content_hash = validate_sha256(self.content_hash, "content_hash")
        if status == ArtifactStatus.VALID:
            if verification_status != VerificationStatus.VERIFIED:
                raise ContractValidationError(
                    "valid Artifacts require verification_status=verified"
                )
            if not self.producer_version.is_identified:
                raise ContractValidationError(
                    "valid Artifacts require producer semantic_version or source_fingerprint"
                )

        expected_id = build_artifact_id(artifact_type, self.recipe.recipe_hash, content_hash)
        if self.artifact_id is None:
            artifact_id = expected_id
        else:
            artifact_id = validate_artifact_id(self.artifact_id)
            if artifact_id != expected_id:
                raise ContractValidationError(
                    "artifact_id does not match its type, Recipe hash, and content hash"
                )

        semantic_path = self.semantic_path
        if semantic_path is not None:
            semantic_path = normalize_semantic_path(semantic_path)

        compute_seconds = self.compute_seconds
        if compute_seconds is not None:
            if isinstance(compute_seconds, bool) or not isinstance(compute_seconds, (int, float)):
                raise ContractValidationError("compute_seconds must be a finite number")
            compute_seconds = float(compute_seconds)
            if not math.isfinite(compute_seconds) or compute_seconds < 0:
                raise ContractValidationError("compute_seconds must be finite and >= 0")

        object.__setattr__(self, "artifact_type", artifact_type)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "verification_status", verification_status)
        object.__setattr__(self, "content_hash", content_hash)
        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "semantic_path", semantic_path)
        object.__setattr__(self, "compute_seconds", compute_seconds)
        object.__setattr__(self, "created_at", _normalize_utc_timestamp(self.created_at, "created_at"))
        object.__setattr__(self, "metadata", _copy_mapping(self.metadata, "metadata"))

    @property
    def recipe_hash(self):
        return self.recipe.recipe_hash

    @property
    def metadata_json(self):
        return canonical_json(self.metadata)

    @property
    def producer_version_json(self):
        return canonical_json(self.producer_version.to_dict())

    def to_dict(self):
        return {
            "header_version": self.header_version,
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type.value,
            "recipe": self.recipe.canonical_form,
            "recipe_hash": self.recipe_hash,
            "content_hash": self.content_hash,
            "producer_version": self.producer_version.to_dict(),
            "status": self.status.value,
            "verification_status": self.verification_status.value,
            "semantic_path": self.semantic_path,
            "compute_seconds": self.compute_seconds,
            "created_at": self.created_at,
            "metadata": canonicalize(self.metadata),
        }


@dataclass(frozen=True)
class LegacySourceRecord:
    legacy_kind: str
    legacy_path: str
    path_kind: PathKind
    verification_status: VerificationStatus
    raw_content_hash: Optional[str] = None
    semantic_content_hash: Optional[str] = None
    source_root: Optional[str] = None
    artifact_id: Optional[str] = None
    size_bytes: Optional[int] = None
    mtime_ns: Optional[int] = None
    observed_artifact_type: Optional[ArtifactType] = None
    observed_recipe_hash: Optional[str] = None
    imported_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping = field(default_factory=dict)
    legacy_source_id: Optional[str] = None

    def __post_init__(self):
        legacy_kind = _normalize_text(self.legacy_kind, "legacy_kind").lower()
        path_kind = _coerce_enum(PathKind, self.path_kind, "path_kind")
        verification = _coerce_enum(
            VerificationStatus, self.verification_status, "verification_status"
        )
        legacy_path, source_root = normalize_source_path(
            self.legacy_path, path_kind, source_root=self.source_root
        )

        raw_hash = self.raw_content_hash
        if raw_hash is not None:
            raw_hash = validate_sha256(raw_hash, "raw_content_hash")
        semantic_hash = self.semantic_content_hash
        if semantic_hash is not None:
            semantic_hash = validate_sha256(semantic_hash, "semantic_content_hash")
        artifact_id = self.artifact_id
        if artifact_id is not None:
            artifact_id = validate_artifact_id(artifact_id)

        observed_type = self.observed_artifact_type
        if observed_type is not None:
            observed_type = _coerce_enum(
                ArtifactType, observed_type, "observed_artifact_type"
            )
        observed_recipe_hash = self.observed_recipe_hash
        if observed_recipe_hash is not None:
            observed_recipe_hash = validate_sha256(
                observed_recipe_hash, "observed_recipe_hash"
            )

        for field_name in ("size_bytes", "mtime_ns"):
            value = getattr(self, field_name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                raise ContractValidationError("{0} must be a non-negative integer".format(field_name))

        identity = {
            "legacy_kind": legacy_kind,
            "path_kind": path_kind.value,
            "source_root": source_root,
            "legacy_path": legacy_path,
        }
        expected_source_id = "legacy_{0}".format(canonical_sha256(identity)[:24])
        source_id = self.legacy_source_id
        if source_id is None:
            source_id = expected_source_id
        else:
            source_id = _normalize_text(source_id, "legacy_source_id")
            if source_id != expected_source_id:
                raise ContractValidationError("legacy_source_id does not match source identity")

        object.__setattr__(self, "legacy_kind", legacy_kind)
        object.__setattr__(self, "path_kind", path_kind)
        object.__setattr__(self, "verification_status", verification)
        object.__setattr__(self, "legacy_path", legacy_path)
        object.__setattr__(self, "source_root", source_root)
        object.__setattr__(self, "raw_content_hash", raw_hash)
        object.__setattr__(self, "semantic_content_hash", semantic_hash)
        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "observed_artifact_type", observed_type)
        object.__setattr__(self, "observed_recipe_hash", observed_recipe_hash)
        object.__setattr__(self, "imported_at", _normalize_utc_timestamp(self.imported_at, "imported_at"))
        object.__setattr__(self, "metadata", _copy_mapping(self.metadata, "metadata"))
        object.__setattr__(self, "legacy_source_id", source_id)


@dataclass(frozen=True)
class ArtifactConflictRecord:
    artifact_type: ArtifactType
    recipe_hash: str
    observed_content_hash: str
    existing_artifact_id: Optional[str] = None
    existing_content_hash: Optional[str] = None
    legacy_source_id: Optional[str] = None
    quarantine_path: Optional[str] = None
    detected_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping = field(default_factory=dict)
    conflict_id: Optional[str] = None

    def __post_init__(self):
        artifact_type = _coerce_enum(ArtifactType, self.artifact_type, "artifact_type")
        recipe_hash = validate_sha256(self.recipe_hash, "recipe_hash")
        observed_hash = validate_sha256(self.observed_content_hash, "observed_content_hash")
        existing_id = self.existing_artifact_id
        if existing_id is not None:
            existing_id = validate_artifact_id(existing_id, "existing_artifact_id")
        existing_content_hash = self.existing_content_hash
        if existing_content_hash is None:
            raise ContractValidationError(
                "a conflict requires an existing_content_hash baseline"
            )
        existing_content_hash = validate_sha256(
            existing_content_hash, "existing_content_hash"
        )
        if existing_content_hash == observed_hash:
            raise ContractValidationError(
                "identical content is idempotent and must not be recorded as a conflict"
            )
        legacy_source_id = self.legacy_source_id
        if legacy_source_id is not None:
            legacy_source_id = _normalize_text(legacy_source_id, "legacy_source_id")
        quarantine_path = self.quarantine_path
        if quarantine_path is not None:
            quarantine_path = normalize_semantic_path(quarantine_path)

        identity = {
            "artifact_type": artifact_type,
            "recipe_hash": recipe_hash,
            "existing_artifact_id": existing_id,
            "existing_content_hash": existing_content_hash,
            "observed_content_hash": observed_hash,
            "legacy_source_id": legacy_source_id,
            "quarantine_path": quarantine_path,
        }
        expected_conflict_id = "conf_{0}".format(canonical_sha256(identity)[:24])
        conflict_id = self.conflict_id
        if conflict_id is None:
            conflict_id = expected_conflict_id
        else:
            conflict_id = _normalize_text(conflict_id, "conflict_id")
            if conflict_id != expected_conflict_id:
                raise ContractValidationError("conflict_id does not match conflict identity")

        object.__setattr__(self, "artifact_type", artifact_type)
        object.__setattr__(self, "recipe_hash", recipe_hash)
        object.__setattr__(self, "existing_artifact_id", existing_id)
        object.__setattr__(self, "existing_content_hash", existing_content_hash)
        object.__setattr__(self, "observed_content_hash", observed_hash)
        object.__setattr__(self, "legacy_source_id", legacy_source_id)
        object.__setattr__(self, "quarantine_path", quarantine_path)
        object.__setattr__(self, "detected_at", _normalize_utc_timestamp(self.detected_at, "detected_at"))
        object.__setattr__(self, "metadata", _copy_mapping(self.metadata, "metadata"))
        object.__setattr__(self, "conflict_id", conflict_id)


@dataclass(frozen=True)
class RegistrationResult:
    outcome: RegisterOutcome
    artifact_id: str
    existing_artifact_id: Optional[str] = None
    conflict_id: Optional[str] = None

    def __post_init__(self):
        outcome = _coerce_enum(RegisterOutcome, self.outcome, "outcome")
        artifact_id = validate_artifact_id(self.artifact_id)
        existing_id = self.existing_artifact_id
        if existing_id is not None:
            existing_id = validate_artifact_id(existing_id, "existing_artifact_id")
        conflict_id = self.conflict_id
        if conflict_id is not None:
            conflict_id = _normalize_text(conflict_id, "conflict_id")
        if outcome == RegisterOutcome.CONFLICT and conflict_id is None:
            raise ContractValidationError("conflict registration requires conflict_id")
        if outcome != RegisterOutcome.CONFLICT and conflict_id is not None:
            raise ContractValidationError("non-conflict registration must not carry conflict_id")
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "existing_artifact_id", existing_id)
        object.__setattr__(self, "conflict_id", conflict_id)


@dataclass(frozen=True)
class ConsumerRef:
    consumer_type: str
    consumer_id: str
    artifact_id: str
    created_at: str = field(default_factory=utc_now_iso)
    metadata: Mapping = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "consumer_type", _normalize_text(self.consumer_type, "consumer_type"))
        object.__setattr__(self, "consumer_id", _normalize_text(self.consumer_id, "consumer_id"))
        object.__setattr__(self, "artifact_id", validate_artifact_id(self.artifact_id))
        object.__setattr__(self, "created_at", _normalize_utc_timestamp(self.created_at, "created_at"))
        object.__setattr__(self, "metadata", _copy_mapping(self.metadata, "metadata"))

    @property
    def metadata_json(self):
        return canonical_json(self.metadata)


@dataclass(frozen=True)
class DependencyRecord:
    parent_artifact_id: str
    child_artifact_id: str
    relation: str = "input"

    def __post_init__(self):
        parent = validate_artifact_id(self.parent_artifact_id, "parent_artifact_id")
        child = validate_artifact_id(self.child_artifact_id, "child_artifact_id")
        if parent == child:
            raise ContractValidationError("an Artifact cannot depend on itself")
        object.__setattr__(self, "parent_artifact_id", parent)
        object.__setattr__(self, "child_artifact_id", child)
        object.__setattr__(self, "relation", _normalize_text(self.relation, "relation"))
