"""Append-only, schema-v1-compatible conflict resolution records.

Conflict observations remain in SQLite and durable conflict markers remain on
disk.  A resolution is a separate canonical, write-once authorization record;
ordinary reads never create or modify one.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from .canonical import canonical_sha256
from .contracts import (
    ArtifactStatus,
    VerificationStatus,
    utc_now_iso,
    validate_artifact_id,
    validate_sha256,
)
from .errors import CacheResolutionError, ContractValidationError
from .index import CacheIndex


RESOLUTION_VERSION = 1
RESOLUTION_ACTION_KEEP_EXISTING = "keep_existing"
_CONFLICT_ID = re.compile(r"^conf_[0-9a-f]{24}$")
_RESOLUTION_ID = re.compile(r"^res_[0-9a-f]{24}$")
_EXPECTED_KEYS = {
    "action",
    "actor",
    "artifact_type",
    "authorized_at",
    "conflict_fingerprint",
    "conflict_id",
    "existing_artifact_id",
    "existing_content_hash",
    "observed_content_hash",
    "reason",
    "recipe_hash",
    "resolution_id",
    "resolution_version",
}


def _canonical_plain_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _required_text(value: Any, label: str, *, max_length: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError("{0} must be non-empty text".format(label))
    text = value.strip()
    if len(text) > max_length:
        raise ContractValidationError("{0} is too long".format(label))
    return text


def _validate_timestamp(value: Any) -> str:
    text = _required_text(value, "authorized_at", max_length=64)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractValidationError("authorized_at is not ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ContractValidationError("authorized_at must include a timezone")
    return text


def _conflict_identity(conflict: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "artifact_type": conflict.get("artifact_type"),
        "conflict_id": conflict.get("conflict_id"),
        "detected_at": conflict.get("detected_at"),
        "existing_artifact_id": conflict.get("existing_artifact_id"),
        "existing_content_hash": conflict.get("existing_content_hash"),
        "legacy_source_id": conflict.get("legacy_source_id"),
        "observed_content_hash": conflict.get("observed_content_hash"),
        "quarantine_path": conflict.get("quarantine_path"),
        "recipe_hash": conflict.get("recipe_hash"),
    }


def conflict_fingerprint(conflict: Mapping[str, Any]) -> str:
    return canonical_sha256(_conflict_identity(conflict))


@dataclass(frozen=True)
class ConflictResolutionRecord:
    conflict_id: str
    conflict_fingerprint: str
    artifact_type: str
    recipe_hash: str
    existing_artifact_id: str
    existing_content_hash: str
    observed_content_hash: str
    actor: str
    reason: str
    authorized_at: str
    action: str = RESOLUTION_ACTION_KEEP_EXISTING
    resolution_version: int = RESOLUTION_VERSION
    resolution_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.conflict_id, str) or not _CONFLICT_ID.fullmatch(
            self.conflict_id
        ):
            raise ContractValidationError("conflict_id is invalid")
        fingerprint = validate_sha256(
            self.conflict_fingerprint, "conflict_fingerprint"
        )
        artifact_type = _required_text(
            self.artifact_type, "artifact_type", max_length=32
        )
        recipe_hash = validate_sha256(self.recipe_hash, "recipe_hash")
        artifact_id = validate_artifact_id(
            self.existing_artifact_id, "existing_artifact_id"
        )
        existing_hash = validate_sha256(
            self.existing_content_hash, "existing_content_hash"
        )
        observed_hash = validate_sha256(
            self.observed_content_hash, "observed_content_hash"
        )
        if existing_hash == observed_hash:
            raise ContractValidationError(
                "resolution requires a differing observed content hash"
            )
        actor = _required_text(self.actor, "actor", max_length=256)
        reason = _required_text(self.reason, "reason", max_length=4096)
        authorized_at = _validate_timestamp(self.authorized_at)
        if self.action != RESOLUTION_ACTION_KEEP_EXISTING:
            raise ContractValidationError("unsupported conflict resolution action")
        if self.resolution_version != RESOLUTION_VERSION:
            raise ContractValidationError("unsupported conflict resolution version")
        identity = {
            "action": self.action,
            "actor": actor,
            "authorized_at": authorized_at,
            "conflict_fingerprint": fingerprint,
            "conflict_id": self.conflict_id,
            "reason": reason,
            "resolution_version": self.resolution_version,
        }
        expected_id = "res_{0}".format(canonical_sha256(identity)[:24])
        resolution_id = self.resolution_id or expected_id
        if not isinstance(resolution_id, str) or not _RESOLUTION_ID.fullmatch(
            resolution_id
        ):
            raise ContractValidationError("resolution_id is invalid")
        if resolution_id != expected_id:
            raise ContractValidationError("resolution_id does not match resolution identity")
        object.__setattr__(self, "conflict_fingerprint", fingerprint)
        object.__setattr__(self, "artifact_type", artifact_type)
        object.__setattr__(self, "recipe_hash", recipe_hash)
        object.__setattr__(self, "existing_artifact_id", artifact_id)
        object.__setattr__(self, "existing_content_hash", existing_hash)
        object.__setattr__(self, "observed_content_hash", observed_hash)
        object.__setattr__(self, "actor", actor)
        object.__setattr__(self, "reason", reason)
        object.__setattr__(self, "authorized_at", authorized_at)
        object.__setattr__(self, "resolution_id", resolution_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "actor": self.actor,
            "artifact_type": self.artifact_type,
            "authorized_at": self.authorized_at,
            "conflict_fingerprint": self.conflict_fingerprint,
            "conflict_id": self.conflict_id,
            "existing_artifact_id": self.existing_artifact_id,
            "existing_content_hash": self.existing_content_hash,
            "observed_content_hash": self.observed_content_hash,
            "reason": self.reason,
            "recipe_hash": self.recipe_hash,
            "resolution_id": self.resolution_id,
            "resolution_version": self.resolution_version,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ConflictResolutionRecord":
        if not isinstance(value, Mapping) or set(value) != _EXPECTED_KEYS:
            raise ContractValidationError("conflict resolution record schema is invalid")
        return cls(**dict(value))


class ConflictResolutionLedger:
    """Read exact resolution paths and explicitly publish write-once decisions."""

    def __init__(self, index: CacheIndex):
        if not isinstance(index, CacheIndex):
            raise TypeError("ConflictResolutionLedger requires CacheIndex")
        self.index = index
        self.root = index.database_path.parent.absolute()

    @staticmethod
    def _validate_conflict_id(conflict_id: Any) -> str:
        if not isinstance(conflict_id, str) or not _CONFLICT_ID.fullmatch(conflict_id):
            raise ContractValidationError("conflict_id is invalid")
        return conflict_id

    def resolution_path(self, conflict_id: str) -> str:
        value = self._validate_conflict_id(conflict_id)
        return str(self.root / "conflict_resolutions" / value / "resolution.json")

    def _load_path(self, path: Path) -> Optional[ConflictResolutionRecord]:
        if not path.exists():
            return None
        if path.is_symlink() or not path.is_file():
            raise CacheResolutionError("conflict resolution record is not a regular file")
        try:
            raw = path.read_bytes()
            value = json.loads(raw.decode("utf-8"))
            if _canonical_plain_json(value).encode("utf-8") != raw:
                raise ContractValidationError(
                    "conflict resolution record is not canonical JSON"
                )
            return ConflictResolutionRecord.from_mapping(value)
        except (OSError, UnicodeError, ValueError, ContractValidationError) as exc:
            raise CacheResolutionError(
                "conflict resolution record is invalid: {0}".format(exc)
            ) from exc

    def load(self, conflict: Mapping[str, Any]) -> Optional[ConflictResolutionRecord]:
        conflict_id = self._validate_conflict_id(conflict.get("conflict_id"))
        record = self._load_path(Path(self.resolution_path(conflict_id)))
        if record is None:
            return None
        if (
            record.conflict_fingerprint != conflict_fingerprint(conflict)
            or record.artifact_type != conflict.get("artifact_type")
            or record.recipe_hash != conflict.get("recipe_hash")
            or record.existing_artifact_id != conflict.get("existing_artifact_id")
            or record.existing_content_hash != conflict.get("existing_content_hash")
            or record.observed_content_hash != conflict.get("observed_content_hash")
        ):
            raise CacheResolutionError(
                "conflict resolution record does not match indexed conflict"
            )
        try:
            artifact = self.index.get_artifact(record.existing_artifact_id)
        except Exception as exc:
            raise CacheResolutionError(
                "resolved conflict formal Artifact is unavailable: {0}".format(exc)
            ) from exc
        if (
            artifact.get("artifact_type") != record.artifact_type
            or artifact.get("recipe_hash") != record.recipe_hash
            or artifact.get("content_hash") != record.existing_content_hash
            or artifact.get("status") != ArtifactStatus.VALID.value
            or artifact.get("verification_status")
            != VerificationStatus.VERIFIED.value
        ):
            raise CacheResolutionError(
                "resolved conflict formal Artifact no longer matches authorization"
            )
        return record

    def classify(
        self, conflicts: Iterable[Mapping[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        resolved: List[Dict[str, Any]] = []
        unresolved: List[Dict[str, Any]] = []
        for conflict in conflicts:
            value = dict(conflict)
            record = self.load(value)
            if record is None:
                unresolved.append(value)
            else:
                resolved.append(
                    {"conflict": value, "resolution": record.to_dict()}
                )
        return resolved, unresolved

    def _formal_conflict(self, conflict_id: str) -> Dict[str, Any]:
        conflict = self.index.get_conflict(conflict_id)
        if conflict.get("existing_artifact_id") is None:
            raise ContractValidationError(
                "keep_existing requires a formal existing Artifact"
            )
        artifact = self.index.get_artifact(conflict["existing_artifact_id"])
        if (
            artifact.get("artifact_type") != conflict.get("artifact_type")
            or artifact.get("recipe_hash") != conflict.get("recipe_hash")
            or artifact.get("content_hash") != conflict.get("existing_content_hash")
            or artifact.get("status") != ArtifactStatus.VALID.value
            or artifact.get("verification_status")
            != VerificationStatus.VERIFIED.value
        ):
            raise ContractValidationError(
                "formal existing Artifact is not a valid verified baseline"
            )
        return conflict

    def keep_existing(
        self,
        conflict_id: str,
        *,
        actor: str,
        reason: str,
        apply: bool = False,
    ) -> Dict[str, Any]:
        conflict = self._formal_conflict(self._validate_conflict_id(conflict_id))
        actor_value = _required_text(actor, "actor", max_length=256)
        reason_value = _required_text(reason, "reason", max_length=4096)
        path = Path(self.resolution_path(conflict_id))
        existing = self._load_path(path)
        if existing is not None:
            validated = self.load(conflict)
            if (
                validated is None
                or validated.actor != actor_value
                or validated.reason != reason_value
            ):
                raise ContractValidationError(
                    "conflict resolution record is write-once and already differs"
                )
            return {
                "mode": "apply" if apply else "dry-run",
                "outcome": "identical",
                "conflict": conflict,
                "resolution": validated.to_dict(),
                "resolution_path": str(path),
                "writes": [],
            }

        record = ConflictResolutionRecord(
            conflict_id=conflict["conflict_id"],
            conflict_fingerprint=conflict_fingerprint(conflict),
            artifact_type=conflict["artifact_type"],
            recipe_hash=conflict["recipe_hash"],
            existing_artifact_id=conflict["existing_artifact_id"],
            existing_content_hash=conflict["existing_content_hash"],
            observed_content_hash=conflict["observed_content_hash"],
            actor=actor_value,
            reason=reason_value,
            authorized_at=utc_now_iso(),
        )
        if not apply:
            return {
                "mode": "dry-run",
                "outcome": "planned",
                "conflict": conflict,
                "resolution": record.to_dict(),
                "resolution_path": str(path),
                "writes": [],
            }

        path.parent.mkdir(parents=True, exist_ok=True)
        payload = _canonical_plain_json(record.to_dict()).encode("utf-8")
        descriptor: Optional[int] = None
        try:
            descriptor = os.open(
                str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644
            )
            os.write(descriptor, payload)
            os.fsync(descriptor)
        except FileExistsError:
            repeated = self._load_path(path)
            if repeated is None or repeated.to_dict() != record.to_dict():
                raise ContractValidationError(
                    "conflict resolution record is write-once and already differs"
                )
            return {
                "mode": "apply",
                "outcome": "identical",
                "conflict": conflict,
                "resolution": repeated.to_dict(),
                "resolution_path": str(path),
                "writes": [],
            }
        finally:
            if descriptor is not None:
                os.close(descriptor)
        validated = self.load(conflict)
        if validated is None:
            raise CacheResolutionError("published conflict resolution could not be read")
        return {
            "mode": "apply",
            "outcome": "created",
            "conflict": conflict,
            "resolution": validated.to_dict(),
            "resolution_path": str(path),
            "writes": [str(path)],
        }


__all__ = [
    "ConflictResolutionLedger",
    "ConflictResolutionRecord",
    "RESOLUTION_ACTION_KEEP_EXISTING",
    "RESOLUTION_VERSION",
    "conflict_fingerprint",
]
