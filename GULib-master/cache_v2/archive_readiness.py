"""Read-only Legacy archive inventory and explicit manifest publication."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from .conflict_resolution import ConflictResolutionLedger
from .errors import CacheV2Error, ContractValidationError
from .index import CacheIndex
from .legacy_freeze import (
    LEGACY_CACHE_ROOTS,
    freeze_marker_path,
    read_freeze_marker,
)


MANIFEST_SCHEMA = "opengu.legacy_archive_readiness"
MANIFEST_VERSION = 1
SOURCE_SUFFIXES = frozenset({".py", ".yaml", ".yml", ".sh", ".ps1"})
CONSUMER_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    ("result_cache_class", re.compile(r"\bResultCache\s*\(")),
    ("selection_cache_class", re.compile(r"\bSelectionCache\s*\(")),
    ("score_cache_class", re.compile(r"\bScoreCache\s*\(")),
    ("result_cache_path", re.compile(r"results[/\\]cache(?:[/\\]|[\"'])")),
    ("selection_cache_path", re.compile(r"results[/\\]selection_cache(?:[/\\]|[\"'])")),
    ("score_cache_path", re.compile(r"results[/\\]score_cache(?:[/\\]|[\"'])")),
)


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


def _inventory_tree(root: Path) -> Dict[str, Any]:
    files = []
    if root.is_dir():
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            stat = path.stat()
            files.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "size_bytes": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                    "sha256": _sha256_file(path),
                }
            )
    return {
        "exists": root.is_dir(),
        "file_count": len(files),
        "size_bytes": sum(item["size_bytes"] for item in files),
        "aggregate_sha256": hashlib.sha256(
            _canonical_json(files).encode("utf-8")
        ).hexdigest(),
        "files": files,
    }


def _source_consumers(source_root: Path) -> List[Dict[str, Any]]:
    ignored_parts = {".git", ".planning", "results", "report", "reports", "docs"}
    findings: List[Dict[str, Any]] = []
    for path in sorted(source_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        relative = path.relative_to(source_root)
        if any(part in ignored_parts for part in relative.parts[:-1]):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, 1):
            kinds = sorted(name for name, pattern in CONSUMER_PATTERNS if pattern.search(line))
            if kinds:
                findings.append(
                    {
                        "path": relative.as_posix(),
                        "line": number,
                        "kinds": kinds,
                        "text": line.strip()[:500],
                    }
                )
    return findings


def _v2_index_state(index_path: Path) -> Dict[str, Any]:
    if not index_path.is_file():
        return {
            "exists": False,
            "schema_ok": False,
            "counts": {},
            "artifact_types": {},
            "formal_conflicts": 0,
            "legacy_diagnostic_conflicts": 0,
            "resolved_formal_conflicts": 0,
            "unresolved_formal_conflicts": 0,
        }
    index = CacheIndex(index_path)
    index.check_schema()
    uri = "file:{0}?mode=ro".format(index_path.as_posix())
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        counts = {}
        for table in (
            "legacy_sources",
            "artifacts",
            "artifact_conflicts",
            "dependencies",
            "consumer_refs",
        ):
            counts[table] = int(
                connection.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
            )
        artifact_types = {
            str(row[0]): int(row[1])
            for row in connection.execute(
                "SELECT artifact_type, COUNT(*) FROM artifacts GROUP BY artifact_type"
            ).fetchall()
        }
    finally:
        connection.close()
    conflicts = index.conflicts()
    formal = [item for item in conflicts if item.get("existing_artifact_id")]
    diagnostic = [item for item in conflicts if not item.get("existing_artifact_id")]
    resolved, unresolved = ConflictResolutionLedger(index).classify(formal)
    return {
        "exists": True,
        "schema_ok": True,
        "index_path": str(index_path),
        "index_sha256": _sha256_file(index_path),
        "counts": counts,
        "artifact_types": artifact_types,
        "formal_conflicts": len(formal),
        "legacy_diagnostic_conflicts": len(diagnostic),
        "resolved_formal_conflicts": len(resolved),
        "unresolved_formal_conflicts": len(unresolved),
    }


def build_archive_readiness_manifest(
    results_root: Union[str, Path],
    source_root: Union[str, Path],
) -> Dict[str, Any]:
    results = Path(results_root).expanduser().resolve(strict=False)
    source = Path(source_root).expanduser().resolve(strict=False)
    inventories = {
        name: _inventory_tree(results / name) for name in LEGACY_CACHE_ROOTS
    }
    total_files = sum(item["file_count"] for item in inventories.values())
    total_bytes = sum(item["size_bytes"] for item in inventories.values())
    combined = hashlib.sha256()
    for name in LEGACY_CACHE_ROOTS:
        combined.update(name.encode("utf-8"))
        combined.update(inventories[name]["aggregate_sha256"].encode("ascii"))
    marker = read_freeze_marker(results)
    marker_path = freeze_marker_path(results)
    marker_hash = _sha256_file(marker_path) if marker is not None else None
    consumers = _source_consumers(source)
    v2 = _v2_index_state(results / "cache_v2" / "index.sqlite")
    archive_ready = bool(
        marker is not None
        and v2["schema_ok"]
        and v2["unresolved_formal_conflicts"] == 0
    )
    delete_ready = bool(archive_ready and not consumers and total_files == 0)
    return {
        "schema": MANIFEST_SCHEMA,
        "version": MANIFEST_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "results_root": str(results),
        "source_root": str(source),
        "legacy": {
            "roots": inventories,
            "total_files": total_files,
            "total_bytes": total_bytes,
            "aggregate_sha256": combined.hexdigest(),
        },
        "freeze": {
            "state": "frozen" if marker is not None else "unfrozen",
            "marker_path": str(marker_path),
            "marker_sha256": marker_hash,
            "marker": marker,
        },
        "cache_v2": v2,
        "consumer_refs": {
            "count": len(consumers),
            "items": consumers,
        },
        "rollback": {
            "mode": "in_place_read_only",
            "legacy_payloads_moved": False,
            "legacy_payloads_deleted": False,
            "restore_source": str(results),
            "integrity_anchor": combined.hexdigest(),
        },
        "verdict": {
            "archive_preparation_complete": archive_ready,
            "physical_archive_authorized": False,
            "legacy_delete_ready": delete_ready,
            "legacy_exact_replay_policy": "migration_diagnostic",
            "reasons": [
                item
                for item, include in (
                    ("Legacy caches are not frozen", marker is None),
                    ("Cache V2 index is unavailable or invalid", not v2["schema_ok"]),
                    ("formal V2 conflicts remain unresolved", v2["unresolved_formal_conflicts"] > 0),
                    ("executable/config consumers still reference Legacy cache APIs or paths", bool(consumers)),
                    ("Legacy payloads remain as rollback inputs", total_files > 0),
                )
                if include
            ],
        },
    }


def publish_archive_readiness_manifest(
    results_root: Union[str, Path],
    source_root: Union[str, Path],
    output_path: Union[str, Path],
    *,
    apply: bool = False,
) -> Dict[str, Any]:
    manifest = build_archive_readiness_manifest(results_root, source_root)
    output = Path(output_path).expanduser()
    if not output.is_absolute():
        output = Path(source_root).expanduser().resolve(strict=False) / output
    output = output.resolve(strict=False)
    if not apply:
        return {
            "ok": True,
            "mode": "dry-run",
            "manifest": manifest,
            "output_path": str(output),
            "writes": [],
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_json(manifest).encode("utf-8")
    descriptor: Optional[int] = None
    try:
        descriptor = os.open(str(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    except FileExistsError as exc:
        raise ContractValidationError(
            "archive readiness manifest is write-once; choose a new output path"
        ) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return {
        "ok": True,
        "mode": "apply",
        "manifest": manifest,
        "output_path": str(output),
        "output_sha256": _sha256_file(output),
        "writes": [str(output)],
    }


__all__ = [
    "MANIFEST_SCHEMA",
    "MANIFEST_VERSION",
    "build_archive_readiness_manifest",
    "publish_archive_readiness_manifest",
]
