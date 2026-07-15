"""Explicit write-once freeze for the three Legacy cache roots."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

from .errors import CacheV2Error, ContractValidationError


FREEZE_SCHEMA = "opengu.legacy_cache_freeze"
FREEZE_VERSION = 1
LEGACY_CACHE_ROOTS: Tuple[str, ...] = ("cache", "selection_cache", "score_cache")


class LegacyCacheFrozenError(CacheV2Error):
    """A caller attempted to mutate a frozen Legacy cache."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _required_text(value: Any, label: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError("{0} must be non-empty text".format(label))
    text = value.strip()
    if len(text) > limit:
        raise ContractValidationError("{0} is too long".format(label))
    return text


def snapshot_legacy_caches(results_root: Union[str, Path]) -> Dict[str, Any]:
    root = Path(results_root).expanduser().resolve(strict=False)
    caches: Dict[str, Any] = {}
    combined = hashlib.sha256()
    total_files = 0
    total_bytes = 0
    for name in LEGACY_CACHE_ROOTS:
        cache_root = root / name
        records = []
        if cache_root.is_dir():
            for path in sorted(item for item in cache_root.rglob("*") if item.is_file()):
                stat = path.stat()
                record = {
                    "path": path.relative_to(cache_root).as_posix(),
                    "size_bytes": stat.st_size,
                    "sha256": _sha256_file(path),
                }
                records.append(record)
        aggregate = hashlib.sha256(_canonical_json(records).encode("utf-8")).hexdigest()
        size_bytes = sum(item["size_bytes"] for item in records)
        caches[name] = {
            "exists": cache_root.is_dir(),
            "file_count": len(records),
            "size_bytes": size_bytes,
            "aggregate_sha256": aggregate,
        }
        total_files += len(records)
        total_bytes += size_bytes
        combined.update(name.encode("utf-8"))
        combined.update(aggregate.encode("ascii"))
    return {
        "cache_roots": caches,
        "total_files": total_files,
        "total_bytes": total_bytes,
        "aggregate_sha256": combined.hexdigest(),
    }


def freeze_marker_path(results_root: Union[str, Path]) -> Path:
    return Path(results_root).expanduser().resolve(strict=False) / "cache_v2" / "legacy_freeze.json"


def _validate_marker(value: Any) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractValidationError("Legacy freeze marker root is invalid")
    required = {
        "authorized_at",
        "authorized_by",
        "reason",
        "results_root",
        "schema",
        "scope",
        "snapshot",
        "state",
        "version",
    }
    if set(value) != required:
        raise ContractValidationError("Legacy freeze marker schema is invalid")
    if value.get("schema") != FREEZE_SCHEMA or value.get("version") != FREEZE_VERSION:
        raise ContractValidationError("Legacy freeze marker version is invalid")
    if value.get("state") != "frozen" or tuple(value.get("scope") or ()) != LEGACY_CACHE_ROOTS:
        raise ContractValidationError("Legacy freeze marker scope is invalid")
    _required_text(value.get("authorized_by"), "authorized_by", 256)
    _required_text(value.get("reason"), "reason", 4096)
    timestamp = _required_text(value.get("authorized_at"), "authorized_at", 64)
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractValidationError("Legacy freeze authorized_at is invalid") from exc
    if parsed.tzinfo is None:
        raise ContractValidationError("Legacy freeze authorized_at has no timezone")
    root = Path(str(value.get("results_root"))).expanduser()
    if not root.is_absolute():
        raise ContractValidationError("Legacy freeze results_root is not absolute")
    if not isinstance(value.get("snapshot"), Mapping):
        raise ContractValidationError("Legacy freeze snapshot is invalid")
    return dict(value)


def read_freeze_marker(results_root: Union[str, Path]) -> Optional[Dict[str, Any]]:
    path = freeze_marker_path(results_root)
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise LegacyCacheFrozenError("Legacy freeze marker is not a regular file")
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
        if _canonical_json(value).encode("utf-8") != raw:
            raise ContractValidationError("Legacy freeze marker is not canonical JSON")
        marker = _validate_marker(value)
    except (OSError, UnicodeError, ValueError, ContractValidationError) as exc:
        raise LegacyCacheFrozenError(
            "Legacy freeze marker is invalid and writes fail closed: {0}".format(exc)
        ) from exc
    expected_root = str(Path(results_root).expanduser().resolve(strict=False))
    if marker["results_root"] != expected_root:
        raise LegacyCacheFrozenError("Legacy freeze marker results_root mismatch")
    return marker


def plan_or_freeze_legacy_caches(
    results_root: Union[str, Path],
    *,
    actor: str,
    reason: str,
    apply: bool = False,
) -> Dict[str, Any]:
    root = Path(results_root).expanduser().resolve(strict=False)
    actor_value = _required_text(actor, "actor", 256)
    reason_value = _required_text(reason, "reason", 4096)
    path = freeze_marker_path(root)
    existing = read_freeze_marker(root)
    if existing is not None:
        if existing["authorized_by"] != actor_value or existing["reason"] != reason_value:
            raise ContractValidationError("Legacy freeze marker is write-once and differs")
        return {
            "ok": True,
            "mode": "apply" if apply else "dry-run",
            "outcome": "already_frozen",
            "marker_path": str(path),
            "marker": existing,
            "writes": [],
        }
    marker = {
        "authorized_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "authorized_by": actor_value,
        "reason": reason_value,
        "results_root": str(root),
        "schema": FREEZE_SCHEMA,
        "scope": list(LEGACY_CACHE_ROOTS),
        "snapshot": snapshot_legacy_caches(root),
        "state": "frozen",
        "version": FREEZE_VERSION,
    }
    if not apply:
        return {
            "ok": True,
            "mode": "dry-run",
            "outcome": "planned",
            "marker_path": str(path),
            "marker": marker,
            "writes": [],
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_json(marker).encode("utf-8")
    descriptor = None
    try:
        descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    except FileExistsError:
        observed = read_freeze_marker(root)
        if observed != marker:
            raise ContractValidationError("Legacy freeze marker is write-once and differs")
        return {
            "ok": True,
            "mode": "apply",
            "outcome": "already_frozen",
            "marker_path": str(path),
            "marker": observed,
            "writes": [],
        }
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return {
        "ok": True,
        "mode": "apply",
        "outcome": "frozen",
        "marker_path": str(path),
        "marker": read_freeze_marker(root),
        "writes": [str(path)],
    }


def legacy_results_root_for_cache(cache_path: Union[str, Path]) -> Optional[Path]:
    resolved = Path(cache_path).expanduser().resolve(strict=False)
    for candidate in (resolved, *resolved.parents):
        if candidate.name in LEGACY_CACHE_ROOTS:
            return candidate.parent
    return None


def assert_legacy_cache_writable(cache_path: Union[str, Path]) -> None:
    results_root = legacy_results_root_for_cache(cache_path)
    if results_root is None:
        return
    marker = read_freeze_marker(results_root)
    if marker is not None:
        raise LegacyCacheFrozenError(
            "Legacy cache writes are frozen by {0}".format(
                freeze_marker_path(results_root)
            )
        )


__all__ = [
    "FREEZE_SCHEMA",
    "FREEZE_VERSION",
    "LEGACY_CACHE_ROOTS",
    "LegacyCacheFrozenError",
    "assert_legacy_cache_writable",
    "freeze_marker_path",
    "plan_or_freeze_legacy_caches",
    "read_freeze_marker",
    "snapshot_legacy_caches",
]
