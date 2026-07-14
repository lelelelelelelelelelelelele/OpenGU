"""Read-only discovery and inspection of OpenGU legacy cache sources.

The legacy indexer deliberately does not import or instantiate the legacy
``ResultCache``, ``SelectionCache`` or ``ScoreCache`` implementations.  Their
constructors create directories, which would violate the V2.1 dry-run
contract.  This module keeps discovery and inspection pure; applying a scan
plan is an explicit, separate operation performed through :class:`CacheIndex`.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple

from .errors import LegacySourceChangedError
from .paths import normalize_relative_path


_RUN_COMPONENTS = frozenset(
    ("attack.json", "collateral.json", "predictions.npz", "_meta.json")
)
_SCORE_SUFFIXES = frozenset((".json", ".npz"))
_HEX32 = re.compile(r"^[0-9a-f]{32}$")
_CHUNK_SIZE = 1024 * 1024


def _reject_non_standard_json_constant(value: str) -> None:
    raise ValueError("non-standard JSON numeric constant: {0}".format(value))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return asdict(value)
    raise TypeError("not JSON serializable: {0!r}".format(type(value).__name__))


def _canonical_json(value: Any) -> str:
    """Return a strict, deterministic JSON representation."""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=_json_default,
    )


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _semantic_json_hash(value: Any) -> str:
    return _sha256_bytes(_canonical_json(value).encode("utf-8"))


def _recipe_hash(fields: Mapping[str, Any]) -> str:
    """Use the machine contract when available, with a no-write fallback."""

    try:
        from .contracts import ArtifactRecipe
    except ImportError:
        return _semantic_json_hash(dict(fields))
    return ArtifactRecipe(fields=dict(fields)).recipe_hash


def _enum_value(value: Any) -> Any:
    return value.value if isinstance(value, Enum) else value


def _safe_int(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _is_excluded_dir_name(name: str) -> bool:
    lowered = name.casefold()
    if lowered == "cache_v2":
        return True
    if lowered.startswith("_archive"):
        return True
    normalized = lowered.lstrip("_")
    if re.search(
        r"(?:^|[-_.])(?:archive|deprecated|backup|backups|bak|old)(?:$|[-_.0-9])",
        normalized,
    ):
        return True
    return False


@dataclass(frozen=True)
class Anomaly:
    """One stable, machine-readable scan anomaly."""

    code: str
    severity: str
    path: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class SourceFileState:
    """Immutable observation of one physical legacy source file."""

    path: str
    size_bytes: int
    mtime_ns: int
    source_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScannedLegacySource:
    """A logical legacy source prepared for optional index insertion.

    ``artifact_type`` and ``recipe_hash`` are candidate hints only.  No record
    emitted by this V2.1 indexer is a formal V2 Artifact: legacy producer
    version and provenance are incomplete by construction.
    """

    record_id: str
    legacy_kind: str
    source_path: str
    source_paths: Tuple[str, ...]
    source_sha256: str
    size_bytes: int
    mtime_ns: int
    artifact_type: Optional[str]
    recipe: Optional[Dict[str, Any]]
    recipe_hash: Optional[str]
    identity_complete: bool
    content_hash: Optional[str]
    status: str
    verification_status: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "legacy_kind": self.legacy_kind,
            "source_path": self.source_path,
            "source_paths": list(self.source_paths),
            "source_sha256": self.source_sha256,
            "size_bytes": self.size_bytes,
            "mtime_ns": self.mtime_ns,
            "artifact_type": self.artifact_type,
            "recipe": self.recipe,
            "recipe_hash": self.recipe_hash,
            "identity_complete": self.identity_complete,
            "content_hash": self.content_hash,
            "status": self.status,
            "verification_status": self.verification_status,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ScannedConflict:
    artifact_type: str
    recipe_hash: str
    content_hashes: Tuple[str, ...]
    source_paths: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "recipe_hash": self.recipe_hash,
            "content_hashes": list(self.content_hashes),
            "source_paths": list(self.source_paths),
        }


@dataclass
class ScanReport:
    """Complete in-memory scan plan plus a bounded JSON summary view."""

    root: str
    scanned_at: str
    source_state_hash: str
    file_states: List[SourceFileState]
    records: List[ScannedLegacySource]
    anomalies: List[Anomaly]
    conflicts: List[ScannedConflict]
    duplicate_groups: List[Dict[str, Any]]
    excluded_paths: List[str]
    missing_roots: List[str]

    def anomaly_counts(self) -> Dict[str, int]:
        return dict(sorted(Counter(item.code for item in self.anomalies).items()))

    def summary(self) -> Dict[str, Any]:
        by_kind = Counter(item.legacy_kind for item in self.records)
        by_status = Counter(item.status for item in self.records)
        by_verification = Counter(item.verification_status for item in self.records)
        by_artifact_type = Counter(
            item.artifact_type or "none" for item in self.records
        )
        return {
            "discovered_files": len(self.file_states),
            "logical_sources": len(self.records),
            "by_legacy_kind": dict(sorted(by_kind.items())),
            "by_candidate_artifact_type": dict(sorted(by_artifact_type.items())),
            "by_status": dict(sorted(by_status.items())),
            "by_verification_status": dict(sorted(by_verification.items())),
            "anomalies": self.anomaly_counts(),
            "conflict_groups": len(self.conflicts),
            "duplicate_same_content_groups": len(self.duplicate_groups),
            "excluded_paths": len(self.excluded_paths),
            "missing_roots": len(self.missing_roots),
        }

    def to_dict(
        self,
        include_records: bool = False,
        sample_limit: int = 5,
    ) -> Dict[str, Any]:
        sample_limit = max(0, int(sample_limit))
        grouped: Dict[str, List[Anomaly]] = defaultdict(list)
        for item in self.anomalies:
            grouped[item.code].append(item)
        anomaly_samples = {
            code: [entry.to_dict() for entry in entries[:sample_limit]]
            for code, entries in sorted(grouped.items())
        }
        payload: Dict[str, Any] = {
            "root": self.root,
            "scanned_at": self.scanned_at,
            "source_state_hash": self.source_state_hash,
            "summary": self.summary(),
            "anomaly_samples": anomaly_samples,
            "conflicts": [item.to_dict() for item in self.conflicts[:sample_limit]],
            "duplicate_same_content": self.duplicate_groups[:sample_limit],
            "excluded_path_samples": self.excluded_paths[:sample_limit],
            "missing_roots": list(self.missing_roots),
            "record_samples": [
                item.to_dict() for item in self.records[:sample_limit]
            ],
        }
        if include_records:
            payload["records"] = [item.to_dict() for item in self.records]
            payload["file_states"] = [item.to_dict() for item in self.file_states]
            payload["all_anomalies"] = [item.to_dict() for item in self.anomalies]
        return payload


@dataclass
class _Discovery:
    result_cache: List[Path] = field(default_factory=list)
    selection_cache: List[Path] = field(default_factory=list)
    score_groups: Dict[str, Dict[str, Path]] = field(default_factory=dict)
    run_groups: Dict[Path, Dict[str, Path]] = field(default_factory=dict)
    files: List[Path] = field(default_factory=list)
    excluded_paths: List[str] = field(default_factory=list)
    missing_roots: List[str] = field(default_factory=list)


class LegacyIndexer:
    """Discover and inspect legacy cache/result sources without writing."""

    def __init__(self, root: Any, sample_limit: int = 5):
        requested_root = Path(root).expanduser()
        if not requested_root.is_absolute():
            raise ValueError(
                "LegacyIndexer requires an explicit absolute root; callers must "
                "resolve relative input against the repository root"
            )
        self.root = requested_root.resolve()
        self.sample_limit = max(0, int(sample_limit))
        self._anomalies: List[Anomaly] = []
        self._states: Dict[str, SourceFileState] = {}
        self._selection_records_by_legacy_key: Dict[str, ScannedLegacySource] = {}

    @property
    def index_path(self) -> Path:
        return self.root / "cache_v2" / "index.sqlite"

    def scan(self) -> ScanReport:
        """Return a complete read-only plan.  No directory is created."""

        self._anomalies = []
        self._states = {}
        self._selection_records_by_legacy_key = {}
        if not self.root.is_dir():
            raise FileNotFoundError("legacy root not found: {0}".format(self.root))

        discovery = self._discover()
        for path in sorted(set(discovery.files), key=self._relative):
            self._observe_file(path)

        records: List[ScannedLegacySource] = []
        for path in sorted(discovery.result_cache, key=self._relative):
            try:
                record = self._inspect_result_cache(path)
                if record is not None:
                    records.append(record)
            except Exception as exc:
                self._anomaly(
                    "source_inspection_error",
                    "error",
                    path,
                    "unexpected ResultCache inspection failure",
                    error_type=type(exc).__name__,
                    error=str(exc),
                )
        for path in sorted(discovery.selection_cache, key=self._relative):
            try:
                record = self._inspect_selection_cache(path)
                if record is not None:
                    records.append(record)
                    key = str(record.metadata.get("legacy_cache_key") or "")
                    if key:
                        self._selection_records_by_legacy_key[key] = record
            except Exception as exc:
                self._anomaly(
                    "source_inspection_error",
                    "error",
                    path,
                    "unexpected SelectionCache inspection failure",
                    error_type=type(exc).__name__,
                    error=str(exc),
                )
        for group_key in sorted(discovery.score_groups):
            group_files = discovery.score_groups[group_key]
            try:
                record = self._inspect_score_group(group_key, group_files)
                if record is not None:
                    records.append(record)
            except Exception as exc:
                path = next(iter(group_files.values()), None)
                self._anomaly(
                    "source_inspection_error",
                    "error",
                    path,
                    "unexpected ScoreCache inspection failure",
                    error_type=type(exc).__name__,
                    error=str(exc),
                )
        for leaf in sorted(discovery.run_groups, key=self._relative):
            try:
                records.extend(self._inspect_run_group(leaf, discovery.run_groups[leaf]))
            except Exception as exc:
                self._anomaly(
                    "source_inspection_error",
                    "error",
                    leaf,
                    "unexpected run-leaf inspection failure",
                    error_type=type(exc).__name__,
                    error=str(exc),
                )

        records.sort(key=lambda item: (item.legacy_kind, item.source_path))
        conflicts, duplicates = self._detect_recipe_collisions(records)
        file_states = sorted(self._states.values(), key=lambda item: item.path)
        source_state_hash = _semantic_json_hash(
            [item.to_dict() for item in file_states]
        )
        return ScanReport(
            root=str(self.root),
            scanned_at=_utc_now(),
            source_state_hash=source_state_hash,
            file_states=file_states,
            records=records,
            anomalies=sorted(
                self._anomalies,
                key=lambda item: (item.code, item.path or "", item.message),
            ),
            conflicts=conflicts,
            duplicate_groups=duplicates,
            excluded_paths=sorted(set(discovery.excluded_paths)),
            missing_roots=sorted(set(discovery.missing_roots)),
        )

    def verify_report_sources(self, report: ScanReport) -> None:
        """Fail closed if any scanned source changed before index apply."""

        if not isinstance(report, ScanReport):
            raise TypeError("verify_report_sources requires ScanReport")
        if Path(report.root).resolve() != self.root:
            raise LegacySourceChangedError(
                "scan report root does not match this LegacyIndexer"
            )
        expected_state_hash = _semantic_json_hash(
            [item.to_dict() for item in sorted(report.file_states, key=lambda item: item.path)]
        )
        if expected_state_hash != report.source_state_hash:
            raise LegacySourceChangedError("scan report source_state_hash is inconsistent")

        discovery = self._discover()
        current_paths = {self._relative(path) for path in discovery.files}
        expected_paths = {item.path for item in report.file_states}
        if current_paths != expected_paths:
            added = sorted(current_paths - expected_paths)
            removed = sorted(expected_paths - current_paths)
            raise LegacySourceChangedError(
                "Legacy source set changed after scan; added={0}, removed={1}".format(
                    added[:5], removed[:5]
                )
            )

        for state in report.file_states:
            relative = normalize_relative_path(state.path, label="scan source path")
            path = self.root.joinpath(*relative.split("/"))
            try:
                before = path.stat()
                digest = hashlib.sha256()
                with path.open("rb") as handle:
                    while True:
                        chunk = handle.read(_CHUNK_SIZE)
                        if not chunk:
                            break
                        digest.update(chunk)
                after = path.stat()
            except OSError as exc:
                raise LegacySourceChangedError(
                    "Legacy source became unreadable after scan: {0}: {1}".format(
                        relative, exc
                    )
                )
            observed = (int(after.st_size), int(after.st_mtime_ns), digest.hexdigest())
            expected = (state.size_bytes, state.mtime_ns, state.source_sha256)
            if (
                before.st_size != after.st_size
                or before.st_mtime_ns != after.st_mtime_ns
                or observed != expected
            ):
                raise LegacySourceChangedError(
                    "Legacy source changed after scan: {0}".format(relative)
                )

    def _relative(self, path: Path) -> str:
        resolved = path.resolve()
        try:
            return resolved.relative_to(self.root).as_posix()
        except ValueError:
            return str(resolved)

    def _anomaly(
        self,
        code: str,
        severity: str,
        path: Optional[Path],
        message: str,
        **details: Any
    ) -> None:
        self._anomalies.append(
            Anomaly(
                code=code,
                severity=severity,
                path=self._relative(path) if path is not None else None,
                message=message,
                details=details,
            )
        )

    def _walk_files(self, base: Path) -> Iterator[Path]:
        if not base.is_dir():
            return
        for current, dirs, files in os.walk(str(base), topdown=True, followlinks=False):
            current_path = Path(current)
            kept: List[str] = []
            for name in sorted(dirs):
                child = current_path / name
                if child.is_symlink():
                    self._anomaly(
                        "symlink_skipped", "info", child, "symlink directory skipped"
                    )
                    continue
                if _is_excluded_dir_name(name):
                    continue
                kept.append(name)
            dirs[:] = kept
            for name in sorted(files):
                path = current_path / name
                if path.is_symlink():
                    self._anomaly(
                        "symlink_skipped", "info", path, "symlink file skipped"
                    )
                    continue
                yield path

    def _discover(self) -> _Discovery:
        found = _Discovery()
        for child in sorted(self.root.iterdir(), key=lambda item: item.name.casefold()):
            if child.is_dir() and _is_excluded_dir_name(child.name):
                found.excluded_paths.append(self._relative(child))

        cache_dir = self.root / "cache"
        if cache_dir.is_dir():
            for path in sorted(cache_dir.iterdir(), key=lambda item: item.name):
                if path.is_file() and not path.is_symlink() and path.suffix.casefold() == ".json":
                    found.result_cache.append(path)
                    found.files.append(path)
        else:
            found.missing_roots.append(self._relative(cache_dir))

        selection_dir = self.root / "selection_cache"
        if selection_dir.is_dir():
            for path in sorted(selection_dir.iterdir(), key=lambda item: item.name):
                if path.is_file() and not path.is_symlink() and path.suffix.casefold() == ".json":
                    found.selection_cache.append(path)
                    found.files.append(path)
        else:
            found.missing_roots.append(self._relative(selection_dir))

        score_dir = self.root / "score_cache"
        if score_dir.is_dir():
            groups: Dict[str, Dict[str, Path]] = defaultdict(dict)
            for path in self._walk_files(score_dir):
                suffix = path.suffix.casefold()
                if suffix not in _SCORE_SUFFIXES:
                    continue
                stem_key = self._relative(path.with_suffix(""))
                groups[stem_key][suffix] = path
                found.files.append(path)
            found.score_groups = dict(groups)
        else:
            found.missing_roots.append(self._relative(score_dir))

        runs_dir = self.root / "runs"
        if runs_dir.is_dir():
            run_groups: Dict[Path, Dict[str, Path]] = defaultdict(dict)
            for path in self._walk_files(runs_dir):
                if path.name not in _RUN_COMPONENTS:
                    continue
                run_groups[path.parent][path.name] = path
                found.files.append(path)
            found.run_groups = dict(run_groups)
        else:
            found.missing_roots.append(self._relative(runs_dir))
        return found

    def _observe_file(self, path: Path) -> Optional[SourceFileState]:
        rel = self._relative(path)
        if rel in self._states:
            return self._states[rel]
        try:
            before = path.stat()
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                while True:
                    chunk = handle.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    digest.update(chunk)
            after = path.stat()
        except OSError as exc:
            self._anomaly(
                "source_read_error",
                "error",
                path,
                "failed to read legacy source",
                error_type=type(exc).__name__,
                error=str(exc),
            )
            return None
        if before.st_size != after.st_size or before.st_mtime_ns != after.st_mtime_ns:
            self._anomaly(
                "source_changed_during_scan",
                "error",
                path,
                "source changed while it was being hashed",
            )
        state = SourceFileState(
            path=rel,
            size_bytes=int(after.st_size),
            mtime_ns=int(after.st_mtime_ns),
            source_sha256=digest.hexdigest(),
        )
        self._states[rel] = state
        return state

    def _read_json(self, path: Path) -> Optional[Any]:
        try:
            return json.loads(
                path.read_text(encoding="utf-8"),
                parse_constant=_reject_non_standard_json_constant,
            )
        except Exception as exc:
            self._anomaly(
                "json_decode_error",
                "error",
                path,
                "legacy JSON could not be decoded",
                error_type=type(exc).__name__,
                error=str(exc),
            )
            return None

    def _hash_json(self, value: Any, path: Path) -> Optional[str]:
        try:
            return _semantic_json_hash(value)
        except (TypeError, ValueError, OverflowError) as exc:
            self._anomaly(
                "json_semantic_hash_error",
                "error",
                path,
                "JSON value cannot be canonically hashed",
                error_type=type(exc).__name__,
                error=str(exc),
            )
            return None

    def _combined_state(self, paths: Sequence[Path]) -> Optional[Tuple[str, int, int]]:
        states = [self._states.get(self._relative(path)) for path in paths]
        states = [item for item in states if item is not None]
        if not states:
            return None
        digest = _semantic_json_hash(
            [{"path": item.path, "sha256": item.source_sha256} for item in states]
        )
        return (
            digest,
            sum(item.size_bytes for item in states),
            max(item.mtime_ns for item in states),
        )

    def _make_record(
        self,
        legacy_kind: str,
        paths: Sequence[Path],
        artifact_type: Optional[str],
        recipe: Optional[Dict[str, Any]],
        identity_complete: bool,
        content_hash: Optional[str],
        status: str,
        verification_status: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[ScannedLegacySource]:
        ordered_paths = tuple(sorted(paths, key=self._relative))
        combined = self._combined_state(ordered_paths)
        if not ordered_paths or combined is None:
            return None
        source_paths = tuple(self._relative(path) for path in ordered_paths)
        recipe_digest = (
            _recipe_hash(recipe) if recipe is not None else None
        )
        record_id = _semantic_json_hash(
            {"legacy_kind": legacy_kind, "source_paths": list(source_paths)}
        )
        return ScannedLegacySource(
            record_id=record_id,
            legacy_kind=legacy_kind,
            source_path=source_paths[0],
            source_paths=source_paths,
            source_sha256=combined[0],
            size_bytes=combined[1],
            mtime_ns=combined[2],
            artifact_type=artifact_type,
            recipe=dict(recipe) if recipe is not None else None,
            recipe_hash=recipe_digest,
            identity_complete=bool(identity_complete),
            content_hash=content_hash,
            status=status,
            verification_status=verification_status,
            metadata=dict(metadata or {}),
        )

    def _validate_selected_nodes(
        self,
        nodes: Any,
        path: Path,
        expected_k: Any = None,
    ) -> Optional[List[int]]:
        if not isinstance(nodes, list) or any(
            not isinstance(item, int) or isinstance(item, bool) for item in nodes
        ):
            self._anomaly(
                "selected_nodes_invalid",
                "error",
                path,
                "selected_nodes must be a list of integer node IDs",
            )
            return None
        normalized = [int(item) for item in nodes]
        if len(set(normalized)) != len(normalized):
            self._anomaly(
                "selected_nodes_invalid",
                "error",
                path,
                "selected_nodes contains duplicate node IDs",
                count=len(normalized),
                unique_count=len(set(normalized)),
            )
        k_value = _safe_int(expected_k)
        if k_value is not None and len(normalized) != k_value:
            self._anomaly(
                "selected_nodes_k_mismatch",
                "error",
                path,
                "selected_nodes length does not match k",
                expected_k=k_value,
                observed_count=len(normalized),
            )
        return normalized

    def _inspect_result_cache(self, path: Path) -> Optional[ScannedLegacySource]:
        payload = self._read_json(path)
        if payload is None:
            return self._make_record(
                "result_cache",
                (path,),
                None,
                None,
                False,
                None,
                "corrupt",
                "corrupt",
                {"reason": "json_decode_error"},
            )
        if not isinstance(payload, dict):
            self._anomaly(
                "json_schema_error", "error", path, "ResultCache root must be an object"
            )
            return self._make_record(
                "result_cache", (path,), None, None, False, None, "corrupt", "corrupt"
            )
        embedded_key = payload.get("cache_key")
        if embedded_key != path.stem:
            self._anomaly(
                "embedded_key_mismatch",
                "error",
                path,
                "ResultCache filename does not match embedded cache_key",
                filename_key=path.stem,
                embedded_key=embedded_key,
            )
        config = payload.get("config")
        result = payload.get("result")
        if not isinstance(config, dict) or not isinstance(result, dict):
            self._anomaly(
                "json_schema_error",
                "error",
                path,
                "ResultCache requires object config and result fields",
            )
            result = result if isinstance(result, dict) else {}
            config = config if isinstance(config, dict) else {}
        nodes = self._validate_selected_nodes(
            result.get("selected_nodes", []), path, config.get("k")
        )
        content_hash = self._hash_json(result, path)
        config_allowlist = (
            "dataset_name",
            "base_model",
            "unlearning_methods",
            "unlearn_ratio",
            "k",
            "random_seed",
            "seed",
            "strategy_name",
            "unlearn_task",
            "downstream_task",
            "is_transductive",
            "is_balanced",
            "gcn_num_layers",
            "gcn_hidden",
            "alpha",
            "hybrid_alpha",
            "fusion_method",
            "candidate_fraction",
            "mc_rounds",
            "im_batch_size",
            "im_selector_seed",
        )
        metadata: Dict[str, Any] = {
            "legacy_cache_key": embedded_key,
            "cached_at": payload.get("cached_at"),
            "config_projection": {
                key: config.get(key) for key in config_allowlist if key in config
            },
            "result_strategy": result.get("strategy_name"),
            "selection_cache_key": result.get("selection_cache_key"),
            "selection_cache_hit": result.get("selection_cache_hit"),
        }
        if nodes is not None:
            metadata["selected_nodes_count"] = len(nodes)
            metadata["ordered_nodes_hash"] = _semantic_json_hash(nodes)
            metadata["node_set_hash"] = _semantic_json_hash(sorted(set(nodes)))
        # A ResultCache remains a legacy source only.  It is never projected
        # into a fifth V2 Result artifact or silently promoted to Selection.
        return self._make_record(
            "result_cache",
            (path,),
            None,
            None,
            False,
            content_hash,
            "unknown",
            "degraded" if content_hash is not None else "corrupt",
            metadata,
        )

    def _selection_recipe(
        self, config: Mapping[str, Any], path: Path
    ) -> Tuple[Optional[Dict[str, Any]], bool]:
        strategy = config.get("strategy_name")
        k_value = _safe_int(config.get("k"))
        graph_fingerprint = config.get("graph_fingerprint")
        params_fingerprint = config.get("strategy_params_fingerprint")
        supported = strategy in (
            "random",
            "degree",
            "pagerank",
            "im",
            "tracin",
            "hybrid",
        )
        if not supported:
            self._anomaly(
                "recipe_incomplete",
                "warning",
                path,
                "unknown selection strategy",
                strategy=strategy,
            )
            return None, False

        split_fields = (
            "is_transductive",
            "is_balanced",
            "train_ratio",
            "val_ratio",
            "test_ratio",
        )
        missing: List[str] = []
        if not isinstance(graph_fingerprint, str) or not _HEX32.match(graph_fingerprint):
            missing.append("graph_fingerprint")
            self._anomaly(
                "graph_fingerprint_missing",
                "warning",
                path,
                "selection recipe lacks a valid graph fingerprint",
            )
        if k_value is None or k_value < 0:
            missing.append("k")
        if not isinstance(params_fingerprint, str) or not _HEX32.match(params_fingerprint):
            missing.append("strategy_params_fingerprint")
        for key in split_fields:
            if key not in config:
                missing.append(key)

        recipe: Dict[str, Any] = {
            "kind": "selection",
            "graph_fingerprint": graph_fingerprint,
            "candidate_policy": {
                key: config.get(key) for key in split_fields
            },
            "selector": {
                "name": strategy,
                "params_fingerprint": params_fingerprint,
                "producer_contract": "legacy-selection-unknown-version",
            },
            "selection_rule": {"kind": "ordered_top_k", "k": k_value},
        }
        if strategy in ("random", "im", "tracin", "hybrid"):
            seed = _safe_int(config.get("seed"))
            recipe["selector"]["seed"] = seed
            if seed is None:
                missing.append("seed")
        if strategy in ("tracin", "hybrid"):
            base_model = config.get("base_model")
            recipe["selector"]["legacy_model_proxy"] = {
                "base_model": base_model,
                "seed": _safe_int(config.get("seed")),
            }
            if not isinstance(base_model, str) or not base_model:
                missing.append("selector_base_model")
                self._anomaly(
                    "selector_identity_missing",
                    "warning",
                    path,
                    "model-dependent selector lacks a base-model identity proxy",
                )
        if missing:
            self._anomaly(
                "recipe_incomplete",
                "warning",
                path,
                "selection recipe is incomplete",
                missing_fields=sorted(set(missing)),
            )
        return recipe, not missing

    def _inspect_selection_cache(self, path: Path) -> Optional[ScannedLegacySource]:
        payload = self._read_json(path)
        if payload is None or not isinstance(payload, dict):
            if payload is not None:
                self._anomaly(
                    "json_schema_error",
                    "error",
                    path,
                    "SelectionCache root must be an object",
                )
            return self._make_record(
                "selection_cache",
                (path,),
                "selection",
                None,
                False,
                None,
                "corrupt",
                "corrupt",
            )
        embedded_key = payload.get("cache_key")
        if embedded_key != path.stem:
            self._anomaly(
                "embedded_key_mismatch",
                "error",
                path,
                "SelectionCache filename does not match embedded cache_key",
                filename_key=path.stem,
                embedded_key=embedded_key,
            )
        config = payload.get("config")
        result = payload.get("selection_result")
        if not isinstance(config, dict) or not isinstance(result, dict):
            self._anomaly(
                "json_schema_error",
                "error",
                path,
                "SelectionCache requires object config and selection_result fields",
            )
            return self._make_record(
                "selection_cache",
                (path,),
                "selection",
                None,
                False,
                None,
                "corrupt",
                "corrupt",
                {"legacy_cache_key": embedded_key},
            )
        if result.get("selection_key") != path.stem:
            self._anomaly(
                "embedded_key_mismatch",
                "error",
                path,
                "selection_result.selection_key does not match filename",
                selection_key=result.get("selection_key"),
                filename_key=path.stem,
            )
        if result.get("strategy_name") != config.get("strategy_name"):
            self._anomaly(
                "identity_mismatch",
                "error",
                path,
                "selection strategy differs between config and payload",
            )
        nodes = self._validate_selected_nodes(
            result.get("selected_nodes"), path, config.get("k")
        )
        content_hash = (
            _semantic_json_hash({"selected_nodes": nodes}) if nodes is not None else None
        )
        recipe, identity_complete = self._selection_recipe(config, path)
        self._anomaly(
            "producer_version_missing",
            "warning",
            path,
            "legacy SelectionCache has no explicit producer version or source fingerprint",
        )
        metadata: Dict[str, Any] = {
            "legacy_cache_key": embedded_key,
            "cached_at": payload.get("cached_at"),
            "dataset_name": config.get("dataset_name"),
            "base_model": config.get("base_model"),
            "unlearn_ratio": config.get("unlearn_ratio"),
            "producer_version": {
                "semantic_version": None,
                "source_fingerprint": None,
            },
        }
        if nodes is not None:
            metadata.update(
                {
                    "selected_nodes_count": len(nodes),
                    "ordered_nodes_hash": _semantic_json_hash(nodes),
                    "node_set_hash": _semantic_json_hash(sorted(set(nodes))),
                }
            )
        status = "degraded" if content_hash is not None else "corrupt"
        verification = "degraded" if content_hash is not None else "corrupt"
        return self._make_record(
            "selection_cache",
            (path,),
            "selection",
            recipe,
            identity_complete,
            content_hash,
            status,
            verification,
            metadata,
        )

    def _hash_npz(
        self, path: Path
    ) -> Tuple[Optional[str], Dict[str, Dict[str, Any]], Optional[Dict[str, Any]]]:
        try:
            import numpy as np
        except ImportError as exc:
            self._anomaly(
                "npz_read_error",
                "error",
                path,
                "numpy is required to inspect legacy NPZ sources",
                error=str(exc),
            )
            return None, {}, None

        digest = hashlib.sha256()
        array_meta: Dict[str, Dict[str, Any]] = {}
        loaded: Dict[str, Any] = {}
        try:
            with np.load(str(path), allow_pickle=False) as bundle:
                for name in sorted(bundle.files):
                    array = np.asarray(bundle[name])
                    if array.dtype.hasobject:
                        raise ValueError("object arrays are forbidden")
                    contiguous = np.ascontiguousarray(array)
                    header = {
                        "name": name,
                        "dtype": contiguous.dtype.str,
                        "shape": list(contiguous.shape),
                    }
                    digest.update(_canonical_json(header).encode("utf-8"))
                    digest.update(b"\x00")
                    byte_view = contiguous.view(np.uint8).reshape(-1)
                    for offset in range(0, int(byte_view.size), _CHUNK_SIZE):
                        digest.update(
                            memoryview(byte_view[offset : offset + _CHUNK_SIZE])
                        )
                    digest.update(b"\x00")
                    array_meta[name] = {
                        "dtype": str(contiguous.dtype),
                        "shape": list(contiguous.shape),
                    }
                    # Retain only schema metadata after hashing.  Prediction
                    # bundles can be large; keeping every decompressed array
                    # alive would turn a read-only inventory into an OOM risk.
                    loaded[name] = dict(array_meta[name])
        except Exception as exc:
            self._anomaly(
                "npz_read_error",
                "error",
                path,
                "legacy NPZ could not be decoded",
                error_type=type(exc).__name__,
                error=str(exc),
            )
            return None, {}, None
        return digest.hexdigest(), array_meta, loaded

    def _score_recipe(
        self, config: Mapping[str, Any], namespace: Any, path: Path
    ) -> Tuple[Optional[Dict[str, Any]], bool]:
        namespace = str(namespace or config.get("namespace") or "")
        graph_fingerprint = config.get("graph_fingerprint")
        if namespace not in ("if", "im", "im_celf"):
            self._anomaly(
                "recipe_incomplete",
                "warning",
                path,
                "unknown score namespace",
                namespace=namespace,
            )
            return None, False
        missing: List[str] = []
        if not isinstance(graph_fingerprint, str) or not _HEX32.match(graph_fingerprint):
            missing.append("graph_fingerprint")
            self._anomaly(
                "graph_fingerprint_missing",
                "warning",
                path,
                "score recipe lacks a valid graph fingerprint",
            )
        recipe: Dict[str, Any] = {
            "kind": "score",
            "score_family": namespace,
            "graph_fingerprint": graph_fingerprint,
            "producer_contract": "legacy-score-unknown-version",
        }
        if namespace == "if":
            allowed = (
                "base_model",
                "seed",
                "loss_type",
                "is_transductive",
                "is_balanced",
                "unlearn_ratio",
                "unlearning_methods",
            )
            recipe["selector_model_proxy"] = {
                key: config.get(key) for key in allowed
            }
            for key in ("base_model", "seed", "loss_type"):
                if config.get(key) is None:
                    missing.append(key)
            if config.get("base_model") is None:
                self._anomaly(
                    "selector_identity_missing",
                    "warning",
                    path,
                    "IF score lacks a selector-model identity proxy",
                )
        else:
            allowed = (
                "propagation_prob",
                "mc_rounds",
                "candidate_fraction",
                "im_selector_seed",
            )
            recipe["algorithm_parameters"] = {
                key: config.get(key) for key in allowed
            }
            for key in allowed:
                if config.get(key) is None:
                    missing.append(key)
            if namespace == "im_celf":
                for key in ("im_batch_size", "k"):
                    recipe["algorithm_parameters"][key] = config.get(key)
                    if config.get(key) is None:
                        missing.append(key)
        if missing:
            self._anomaly(
                "recipe_incomplete",
                "warning",
                path,
                "score recipe is incomplete",
                missing_fields=sorted(set(missing)),
            )
        return recipe, not missing

    def _inspect_score_group(
        self, group_key: str, files: Mapping[str, Path]
    ) -> Optional[ScannedLegacySource]:
        sidecar = files.get(".json")
        npz_path = files.get(".npz")
        paths = [path for path in (sidecar, npz_path) if path is not None]
        if npz_path is None:
            assert sidecar is not None
            self._anomaly(
                "sidecar_npz_missing",
                "error",
                sidecar,
                "ScoreCache sidecar has no matching NPZ payload",
            )
        if sidecar is None:
            assert npz_path is not None
            self._anomaly(
                "npz_sidecar_missing",
                "warning",
                npz_path,
                "ScoreCache NPZ has no matching JSON sidecar",
            )

        payload = self._read_json(sidecar) if sidecar is not None else None
        config: Mapping[str, Any] = {}
        namespace: Any = None
        if payload is not None:
            if not isinstance(payload, dict) or not isinstance(payload.get("config"), dict):
                self._anomaly(
                    "json_schema_error",
                    "error",
                    sidecar,
                    "ScoreCache sidecar requires an object config",
                )
                payload = None
            else:
                config = payload["config"]
                namespace = payload.get("namespace")
                if payload.get("key") != Path(group_key).name:
                    self._anomaly(
                        "embedded_key_mismatch",
                        "error",
                        sidecar,
                        "ScoreCache sidecar key does not match filename",
                        embedded_key=payload.get("key"),
                        filename_key=Path(group_key).name,
                    )
                dir_namespace = sidecar.parent.name
                if (
                    namespace != dir_namespace
                    or config.get("namespace") != dir_namespace
                ):
                    self._anomaly(
                        "identity_mismatch",
                        "error",
                        sidecar,
                        "ScoreCache namespace disagrees with directory/config",
                        directory_namespace=dir_namespace,
                        sidecar_namespace=namespace,
                        config_namespace=config.get("namespace"),
                    )

        content_hash: Optional[str] = None
        arrays: Dict[str, Dict[str, Any]] = {}
        loaded: Optional[Dict[str, Any]] = None
        structurally_valid = npz_path is not None
        if npz_path is not None:
            content_hash, arrays, loaded = self._hash_npz(npz_path)
            if content_hash is None:
                structurally_valid = False
            elif loaded is not None:
                required = {"candidates", "scores"}
                if set(loaded) != required:
                    self._anomaly(
                        "npz_required_array_missing",
                        "error",
                        npz_path,
                        "ScoreCache NPZ must contain exactly candidates and scores",
                        observed_arrays=sorted(loaded),
                    )
                    structurally_valid = False
                else:
                    candidates = loaded["candidates"]
                    scores = loaded["scores"]
                    candidates_shape = tuple(candidates["shape"])
                    scores_shape = tuple(scores["shape"])
                    if (
                        len(candidates_shape) != 1
                        or len(scores_shape) != 1
                        or candidates_shape != scores_shape
                    ):
                        self._anomaly(
                            "npz_shape_mismatch",
                            "error",
                            npz_path,
                            "ScoreCache candidate and score arrays must be equal 1-D shapes",
                            candidates_shape=list(candidates_shape),
                            scores_shape=list(scores_shape),
                        )
                        structurally_valid = False
                    if candidates["dtype"] != "int64" or scores["dtype"] != "float32":
                        self._anomaly(
                            "npz_dtype_mismatch",
                            "error",
                            npz_path,
                            "ScoreCache arrays have unexpected dtypes",
                            candidates_dtype=candidates["dtype"],
                            scores_dtype=scores["dtype"],
                        )
                        structurally_valid = False
                    if payload is not None and _safe_int(payload.get("n_candidates")) != int(
                        candidates_shape[0]
                    ):
                        self._anomaly(
                            "n_candidates_mismatch",
                            "error",
                            sidecar,
                            "sidecar n_candidates disagrees with NPZ",
                            sidecar_count=payload.get("n_candidates"),
                            npz_count=int(candidates_shape[0]),
                        )
                        structurally_valid = False

        recipe: Optional[Dict[str, Any]] = None
        identity_complete = False
        if payload is not None:
            recipe, identity_complete = self._score_recipe(
                config, namespace, sidecar  # type: ignore[arg-type]
            )
            self._anomaly(
                "producer_version_missing",
                "warning",
                sidecar,
                "legacy ScoreCache has no explicit producer version or source fingerprint",
            )
        status = "degraded" if structurally_valid and payload is not None else "unknown"
        verification = "degraded" if structurally_valid else "corrupt"
        if npz_path is not None and content_hash is None:
            status = "corrupt"
        metadata = {
            "legacy_key": Path(group_key).name,
            "namespace": namespace or (npz_path.parent.name if npz_path else None),
            "saved_at": payload.get("saved_at") if isinstance(payload, dict) else None,
            "arrays": arrays,
            "producer_version": {
                "semantic_version": None,
                "source_fingerprint": None,
            },
        }
        return self._make_record(
            "score_cache",
            paths,
            "score",
            recipe,
            identity_complete,
            content_hash,
            status,
            verification,
            metadata,
        )

    def _run_selection_recipe(
        self, config: Mapping[str, Any], path: Path
    ) -> Tuple[Optional[Dict[str, Any]], bool]:
        """Project only selection-relevant run fields; never full config."""

        strategy = config.get("strategy_name")
        if strategy not in ("random", "degree", "pagerank", "im", "tracin", "hybrid"):
            return None, False
        graph_fingerprint = config.get("graph_fingerprint")
        k_value = _safe_int(config.get("k"))
        split_keys = (
            "is_transductive",
            "is_balanced",
            "train_ratio",
            "val_ratio",
            "test_ratio",
        )
        missing: List[str] = []
        if not isinstance(graph_fingerprint, str) or not _HEX32.match(graph_fingerprint):
            missing.append("graph_fingerprint")
            self._anomaly(
                "graph_fingerprint_missing",
                "warning",
                path,
                "run selection has no graph fingerprint",
            )
        if k_value is None:
            missing.append("k")
        for key in split_keys:
            if key not in config:
                missing.append(key)

        def required_value(field: str, *aliases: str) -> Any:
            for key in (field,) + aliases:
                if key in config and config.get(key) is not None:
                    return config.get(key)
            missing.append(field)
            return None

        def required_int(field: str, *aliases: str) -> Optional[int]:
            value = required_value(field, *aliases)
            normalized = _safe_int(value)
            if value is not None and normalized is None:
                missing.append(field)
            return normalized

        selector: Dict[str, Any] = {
            "name": strategy,
            "producer_contract": "legacy-run-selector-unknown-version",
        }
        if strategy == "random":
            selector["seed"] = required_int("random_seed", "seed")
            selector["parameters"] = {}
        elif strategy == "degree":
            selector["parameters"] = {}
        elif strategy == "pagerank":
            selector["parameters"] = {
                "pagerank_alpha": required_value("pagerank_alpha")
            }
        elif strategy == "im":
            selector["seed"] = required_int("im_selector_seed", "seed")
            selector["parameters"] = {
                "propagation_prob": required_value("propagation_prob"),
                "mc_rounds": required_value("mc_rounds"),
                "candidate_fraction": required_value("candidate_fraction"),
                "im_batch_size": required_value("im_batch_size", "im_v4_batch_size"),
            }
        elif strategy == "tracin":
            selector["seed"] = required_int("random_seed", "seed")
            selector["parameters"] = {
                "loss_type": required_value("loss")
            }
            selector["legacy_model_proxy"] = {
                "base_model": config.get("base_model"),
                "seed": selector["seed"],
            }
            if not config.get("base_model"):
                missing.append("selector_base_model")
        else:
            hybrid_alpha = required_value("hybrid_alpha", "alpha")
            selector["seed"] = required_int("random_seed", "seed")
            selector["parameters"] = {
                "fusion_method": required_value("fusion_method"),
                "hybrid_alpha": hybrid_alpha,
                "loss_type": required_value("loss"),
                "propagation_prob": required_value("propagation_prob"),
                "mc_rounds": required_value("mc_rounds"),
                "candidate_fraction": required_value("candidate_fraction"),
                "im_batch_size": required_value("im_batch_size", "im_v4_batch_size"),
                "im_selector_seed": required_int("im_selector_seed"),
            }
            selector["legacy_model_proxy"] = {
                "base_model": config.get("base_model"),
                "seed": selector["seed"],
            }
            if not config.get("base_model"):
                missing.append("selector_base_model")
        recipe = {
            "kind": "selection",
            "graph_fingerprint": graph_fingerprint,
            "candidate_policy": {
                key: config.get(key) for key in split_keys
            },
            "selector": selector,
            "selection_rule": {"kind": "ordered_top_k", "k": k_value},
        }
        if missing:
            self._anomaly(
                "recipe_incomplete",
                "warning",
                path,
                "run selection recipe is incomplete",
                missing_fields=sorted(set(missing)),
            )
        return recipe, not missing

    def _run_meta_identity(
        self, meta: Any, fallback_result: Optional[Mapping[str, Any]] = None
    ) -> Tuple[Optional[str], Optional[str], Optional[int]]:
        method: Optional[str] = None
        strategy: Optional[str] = None
        seed: Optional[int] = None
        if isinstance(meta, dict):
            method_value = meta.get("method")
            strategy_value = meta.get("strategy")
            method = str(method_value) if method_value is not None else None
            strategy = str(strategy_value) if strategy_value is not None else None
            seed = _safe_int(meta.get("seed"))
        if fallback_result:
            config = fallback_result.get("config")
            if isinstance(config, dict):
                if method is None and config.get("unlearning_methods") is not None:
                    method = str(config.get("unlearning_methods"))
                if strategy is None and config.get("strategy_name") is not None:
                    strategy = str(config.get("strategy_name"))
                if seed is None:
                    seed = _safe_int(config.get("random_seed", config.get("seed")))
        return method, strategy, seed

    def _inspect_run_group(
        self, leaf: Path, files: Mapping[str, Path]
    ) -> List[ScannedLegacySource]:
        records: List[ScannedLegacySource] = []
        missing = sorted(_RUN_COMPONENTS - set(files))
        if missing:
            self._anomaly(
                "run_component_missing",
                "warning",
                leaf,
                "run leaf is missing one or more canonical components",
                missing_components=missing,
            )

        parsed: Dict[str, Any] = {}
        for name in ("_meta.json", "attack.json", "collateral.json"):
            path = files.get(name)
            if path is not None:
                parsed[name] = self._read_json(path)
        meta = parsed.get("_meta.json")
        if meta is not None and not isinstance(meta, dict):
            self._anomaly(
                "json_schema_error", "error", files.get("_meta.json"), "_meta.json must be an object"
            )
            meta = None

        attack = parsed.get("attack.json")
        attack_result: Optional[Mapping[str, Any]] = None
        strategy_hint: Optional[str] = None
        if isinstance(meta, dict) and meta.get("strategy") is not None:
            strategy_hint = str(meta.get("strategy"))
        if isinstance(attack, dict):
            results = attack.get("results")
            if isinstance(results, dict):
                candidate = results.get(strategy_hint) if strategy_hint else None
                if not isinstance(candidate, dict) and len(results) == 1:
                    only_value = next(iter(results.values()))
                    candidate = only_value if isinstance(only_value, dict) else None
                if isinstance(candidate, dict):
                    attack_result = candidate
        method, strategy, seed = self._run_meta_identity(meta, attack_result)

        meta_path = files.get("_meta.json")
        if meta_path is not None:
            if isinstance(meta, dict):
                meta_projection = {
                    key: meta.get(key)
                    for key in (
                        "fingerprint_version",
                        "git_sha",
                        "hostname",
                        "python",
                        "method",
                        "strategy",
                        "seed",
                        "timestamp",
                    )
                }
                meta_content_hash = self._hash_json(meta_projection, meta_path)
                meta_metadata = {
                    "legacy_config_name": meta.get("config_name"),
                    "legacy_config_fingerprint": meta.get("config_fingerprint"),
                    "method": method,
                    "strategy": strategy,
                    "seed": seed,
                    "git_sha": meta.get("git_sha"),
                }
                meta_status = "unknown"
                meta_verification = "unknown"
            else:
                meta_content_hash = None
                meta_metadata = {"reason": "json_decode_or_schema_error"}
                meta_status = "corrupt"
                meta_verification = "corrupt"
            record = self._make_record(
                "run_meta",
                (meta_path,),
                None,
                None,
                False,
                meta_content_hash,
                meta_status,
                meta_verification,
                meta_metadata,
            )
            if record is not None:
                records.append(record)

        attack_path = files.get("attack.json")
        if attack_path is not None:
            if not isinstance(attack, dict) or attack_result is None:
                if isinstance(attack, dict):
                    self._anomaly(
                        "json_schema_error",
                        "error",
                        attack_path,
                        "attack.json lacks a result matching the run strategy",
                        strategy=strategy_hint,
                    )
                record = self._make_record(
                    "run_attack",
                    (attack_path,),
                    "selection",
                    None,
                    False,
                    None,
                    "corrupt",
                    "corrupt",
                    {"method": method, "strategy": strategy, "seed": seed},
                )
                if record is not None:
                    records.append(record)
            else:
                config = attack_result.get("config")
                if not isinstance(config, dict):
                    outer = attack.get("config")
                    config = outer if isinstance(outer, dict) else {}
                if method is not None and config.get("unlearning_methods") not in (None, method):
                    self._anomaly(
                        "identity_mismatch",
                        "error",
                        attack_path,
                        "run method differs between _meta and attack result",
                        meta_method=method,
                        attack_method=config.get("unlearning_methods"),
                    )
                if strategy is not None and attack_result.get("strategy_name") not in (None, strategy):
                    self._anomaly(
                        "identity_mismatch",
                        "error",
                        attack_path,
                        "run strategy differs between _meta and attack result",
                        meta_strategy=strategy,
                        attack_strategy=attack_result.get("strategy_name"),
                    )
                nodes = self._validate_selected_nodes(
                    attack_result.get("selected_nodes"), attack_path, config.get("k")
                )
                content_hash = (
                    _semantic_json_hash({"selected_nodes": nodes})
                    if nodes is not None
                    else None
                )
                legacy_selection_key = attack_result.get("selection_cache_key")
                joined = self._selection_records_by_legacy_key.get(
                    str(legacy_selection_key)
                ) if legacy_selection_key else None
                if legacy_selection_key and joined is None:
                    self._anomaly(
                        "dangling_selection_ref",
                        "warning",
                        attack_path,
                        "run references a SelectionCache key absent from the active cache",
                        selection_cache_key=legacy_selection_key,
                    )
                if joined is not None:
                    recipe = joined.recipe
                    identity_complete = joined.identity_complete
                    if (
                        content_hash is not None
                        and joined.content_hash is not None
                        and content_hash != joined.content_hash
                    ):
                        self._anomaly(
                            "identity_mismatch",
                            "error",
                            attack_path,
                            "run selected_nodes differ from the referenced active SelectionCache",
                            selection_cache_key=legacy_selection_key,
                        )
                else:
                    recipe, identity_complete = self._run_selection_recipe(
                        config, attack_path
                    )
                failed = attack_result.get("failed") is True
                if failed:
                    self._anomaly(
                        "producer_reported_failure",
                        "error",
                        attack_path,
                        "attack producer recorded a failure",
                        failure_reason=attack_result.get("failure_reason"),
                    )
                git_sha = meta.get("git_sha") if isinstance(meta, dict) else None
                if not git_sha:
                    self._anomaly(
                        "producer_version_missing",
                        "warning",
                        attack_path,
                        "run attack has no producer source fingerprint",
                    )
                metadata: Dict[str, Any] = {
                    "method": method,
                    "strategy": strategy,
                    "seed": seed,
                    "legacy_config_name": meta.get("config_name") if isinstance(meta, dict) else None,
                    "git_sha": git_sha,
                    "selection_cache_key": legacy_selection_key,
                    "selection_cache_hit": attack_result.get("selection_cache_hit"),
                    "selection_recipe_joined": joined is not None,
                    "producer_version": {
                        "semantic_version": None,
                        "source_fingerprint": git_sha,
                    },
                }
                if nodes is not None:
                    metadata.update(
                        {
                            "selected_nodes_count": len(nodes),
                            "ordered_nodes_hash": _semantic_json_hash(nodes),
                            "node_set_hash": _semantic_json_hash(sorted(set(nodes))),
                        }
                    )
                record = self._make_record(
                    "run_attack",
                    (attack_path,),
                    "selection",
                    recipe,
                    identity_complete,
                    content_hash,
                    "invalid" if failed else "degraded",
                    "invalid" if failed else "degraded",
                    metadata,
                )
                if record is not None:
                    records.append(record)

        collateral_path = files.get("collateral.json")
        collateral = parsed.get("collateral.json")
        if collateral_path is not None:
            if isinstance(collateral, dict):
                collateral_config = collateral.get("config")
                collateral_results = collateral.get("results")
                if not isinstance(collateral_config, dict) or not isinstance(
                    collateral_results, list
                ):
                    self._anomaly(
                        "json_schema_error",
                        "error",
                        collateral_path,
                        "collateral.json requires object config and list results",
                    )
                allowed = (
                    "dataset_name",
                    "base_model",
                    "unlearning_methods",
                    "unlearn_ratio",
                    "random_seed",
                    "strategies_requested",
                )
                recipe = {
                    "kind": "evaluation",
                    "prediction_artifact_id": None,
                    "legacy_metric_bundle": "collateral-v1-unknown-version",
                    "legacy_execution_hint": {
                        key: collateral_config.get(key)
                        for key in allowed
                        if isinstance(collateral_config, dict) and key in collateral_config
                    },
                }
                self._anomaly(
                    "recipe_incomplete",
                    "warning",
                    collateral_path,
                    "legacy collateral metrics have no PredictionArtifact dependency",
                    missing_fields=["prediction_artifact_id", "metric_version"],
                )
                content_hash = self._hash_json(collateral_results, collateral_path)
                status = "degraded" if content_hash is not None else "corrupt"
                verification = "degraded" if content_hash is not None else "corrupt"
                metadata = {
                    "method": method,
                    "strategy": strategy,
                    "seed": seed,
                    "legacy_config_name": meta.get("config_name") if isinstance(meta, dict) else None,
                    "git_sha": meta.get("git_sha") if isinstance(meta, dict) else None,
                }
            else:
                recipe = None
                content_hash = None
                status = "corrupt"
                verification = "corrupt"
                metadata = {"method": method, "strategy": strategy, "seed": seed}
            record = self._make_record(
                "run_collateral",
                (collateral_path,),
                "evaluation",
                recipe,
                False,
                content_hash,
                status,
                verification,
                metadata,
            )
            if record is not None:
                records.append(record)

        prediction_path = files.get("predictions.npz")
        if prediction_path is not None:
            content_hash, arrays, loaded = self._hash_npz(prediction_path)
            structurally_valid = loaded is not None
            strategy_name = strategy
            if strategy_name is None and loaded:
                prefixes = {
                    name.split("__", 1)[0]
                    for name in loaded
                    if "__" in name and not name.startswith("_meta__")
                }
                if len(prefixes) == 1:
                    strategy_name = next(iter(prefixes))
            required_global = {
                "_meta__y",
                "_meta__train_mask",
                "_meta__test_mask",
                "_meta__num_nodes",
            }
            required_strategy: Set[str] = set()
            if strategy_name:
                required_strategy = {
                    "{0}__logits_before".format(strategy_name),
                    "{0}__logits_unlearned".format(strategy_name),
                    "{0}__logits_retrained".format(strategy_name),
                    "{0}__retain_mask".format(strategy_name),
                    "{0}__selected_nodes".format(strategy_name),
                }
            missing_arrays = sorted(
                (required_global | required_strategy) - set(loaded or {})
            )
            if not strategy_name or missing_arrays:
                self._anomaly(
                    "prediction_schema_error",
                    "error",
                    prediction_path,
                    "prediction NPZ lacks required strategy/global arrays",
                    strategy=strategy_name,
                    missing_arrays=missing_arrays,
                )
                structurally_valid = False
            if structurally_valid and loaded is not None and strategy_name:
                logits_names = (
                    "{0}__logits_before".format(strategy_name),
                    "{0}__logits_unlearned".format(strategy_name),
                    "{0}__logits_retrained".format(strategy_name),
                )
                shapes = [tuple(loaded[name]["shape"]) for name in logits_names]
                if len(set(shapes)) != 1 or len(shapes[0]) != 2:
                    self._anomaly(
                        "prediction_schema_error",
                        "error",
                        prediction_path,
                        "prediction logits must share one [N,C] shape",
                        logits_shapes=[list(shape) for shape in shapes],
                    )
                    structurally_valid = False
            config_hint: Dict[str, Any] = {}
            if isinstance(collateral, dict) and isinstance(collateral.get("config"), dict):
                config_hint = {
                    key: collateral["config"].get(key)
                    for key in (
                        "dataset_name",
                        "base_model",
                        "unlearning_methods",
                        "unlearn_ratio",
                        "random_seed",
                    )
                }
            recipe = {
                "kind": "prediction",
                "graph_fingerprint": None,
                "selection_artifact_id": None,
                "strategy": strategy_name,
                "target_execution_hint": config_hint,
                "producer_contract": "legacy-prediction-unknown-version",
            }
            self._anomaly(
                "recipe_incomplete",
                "warning",
                prediction_path,
                "legacy prediction lacks graph and SelectionArtifact identities",
                missing_fields=["graph_fingerprint", "selection_artifact_id"],
            )
            git_sha = meta.get("git_sha") if isinstance(meta, dict) else None
            metadata = {
                "method": method,
                "strategy": strategy_name,
                "seed": seed,
                "arrays": arrays,
                "git_sha": git_sha,
                "producer_version": {
                    "semantic_version": None,
                    "source_fingerprint": git_sha,
                },
            }
            record = self._make_record(
                "run_prediction",
                (prediction_path,),
                "prediction",
                recipe,
                False,
                content_hash,
                "degraded" if structurally_valid else "corrupt",
                "degraded" if structurally_valid else "corrupt",
                metadata,
            )
            if record is not None:
                records.append(record)
        return records

    def _detect_recipe_collisions(
        self, records: Sequence[ScannedLegacySource]
    ) -> Tuple[List[ScannedConflict], List[Dict[str, Any]]]:
        groups: Dict[Tuple[str, str], List[ScannedLegacySource]] = defaultdict(list)
        for record in records:
            if (
                record.artifact_type is not None
                and record.recipe_hash is not None
                and record.content_hash is not None
                and record.identity_complete
                and record.status not in ("invalid", "corrupt", "missing", "retired")
            ):
                groups[(record.artifact_type, record.recipe_hash)].append(record)

        conflicts: List[ScannedConflict] = []
        duplicates: List[Dict[str, Any]] = []
        for (artifact_type, recipe_digest), members in sorted(groups.items()):
            if len(members) < 2:
                continue
            by_content: Dict[str, List[ScannedLegacySource]] = defaultdict(list)
            for member in members:
                assert member.content_hash is not None
                by_content[member.content_hash].append(member)
            source_paths = tuple(sorted(member.source_path for member in members))
            if len(by_content) == 1:
                content_hash = next(iter(by_content))
                duplicate = {
                    "artifact_type": artifact_type,
                    "recipe_hash": recipe_digest,
                    "content_hash": content_hash,
                    "source_paths": list(source_paths),
                }
                duplicates.append(duplicate)
                self._anomaly(
                    "duplicate_same_content",
                    "info",
                    self.root / source_paths[0],
                    "multiple legacy sources have the same recipe and content",
                    artifact_type=artifact_type,
                    recipe_hash=recipe_digest,
                    source_paths=list(source_paths),
                )
                continue
            conflict = ScannedConflict(
                artifact_type=artifact_type,
                recipe_hash=recipe_digest,
                content_hashes=tuple(sorted(by_content)),
                source_paths=source_paths,
            )
            conflicts.append(conflict)
            self._anomaly(
                "recipe_content_conflict",
                "error",
                self.root / source_paths[0],
                "same legacy recipe produced different semantic content",
                artifact_type=artifact_type,
                recipe_hash=recipe_digest,
                content_hashes=sorted(by_content),
                source_paths=list(source_paths),
            )
        return conflicts, duplicates

    def to_contract_plan(
        self, report: ScanReport
    ) -> Tuple[List[Any], List[Any]]:
        """Convert an in-memory report to validated machine-contract records.

        Legacy records retain ``artifact_id=None``.  ``observed_artifact_type``
        and ``observed_recipe_hash`` are audit hints, never formal Artifact
        registration.
        """

        from .contracts import (
            ArtifactConflictRecord,
            ArtifactType,
            LegacySourceRecord,
            PathKind,
            VerificationStatus,
        )

        source_records: List[Any] = []
        source_by_scan_id: Dict[str, Any] = {}
        source_by_path: Dict[str, Any] = {}
        for scanned in report.records:
            observed_type = (
                ArtifactType(scanned.artifact_type)
                if scanned.artifact_type is not None
                else None
            )
            verification = VerificationStatus(scanned.verification_status)
            metadata = dict(scanned.metadata)
            metadata.update(
                {
                    "scan_record_id": scanned.record_id,
                    "source_paths": list(scanned.source_paths),
                    "observed_status": scanned.status,
                    "identity_complete": scanned.identity_complete,
                    "recipe": scanned.recipe,
                }
            )
            contract_record = LegacySourceRecord(
                legacy_kind=scanned.legacy_kind,
                legacy_path=scanned.source_path,
                path_kind=PathKind.RELATIVE,
                source_root=str(self.root),
                verification_status=verification,
                raw_content_hash=scanned.source_sha256,
                semantic_content_hash=scanned.content_hash,
                artifact_id=None,
                size_bytes=scanned.size_bytes,
                mtime_ns=scanned.mtime_ns,
                observed_artifact_type=observed_type,
                observed_recipe_hash=scanned.recipe_hash,
                metadata=metadata,
            )
            source_records.append(contract_record)
            source_by_scan_id[scanned.record_id] = contract_record
            source_by_path[scanned.source_path] = contract_record

        conflict_records: List[Any] = []
        grouped: Dict[Tuple[str, str], List[ScannedLegacySource]] = defaultdict(list)
        for scanned in report.records:
            if scanned.artifact_type and scanned.recipe_hash and scanned.content_hash:
                grouped[(scanned.artifact_type, scanned.recipe_hash)].append(scanned)
        for conflict in report.conflicts:
            members = sorted(
                grouped.get((conflict.artifact_type, conflict.recipe_hash), []),
                key=lambda item: (item.content_hash or "", item.source_path),
            )
            if not members:
                continue
            baseline = members[0]
            assert baseline.content_hash is not None
            emitted_hashes: Set[str] = set()
            for observed in members[1:]:
                if (
                    observed.content_hash is None
                    or observed.content_hash == baseline.content_hash
                    or observed.content_hash in emitted_hashes
                ):
                    continue
                emitted_hashes.add(observed.content_hash)
                legacy_source = source_by_scan_id.get(observed.record_id)
                conflict_records.append(
                    ArtifactConflictRecord(
                        artifact_type=ArtifactType(conflict.artifact_type),
                        recipe_hash=conflict.recipe_hash,
                        existing_artifact_id=None,
                        existing_content_hash=baseline.content_hash,
                        observed_content_hash=observed.content_hash,
                        legacy_source_id=(
                            legacy_source.legacy_source_id
                            if legacy_source is not None
                            else None
                        ),
                        quarantine_path=None,
                        metadata={
                            "legacy_only": True,
                            "fail_closed": True,
                            "baseline_source_path": baseline.source_path,
                            "observed_source_path": observed.source_path,
                            "all_source_paths": list(conflict.source_paths),
                        },
                    )
                )
        return source_records, conflict_records

    @staticmethod
    def _index_path(index: Any) -> Optional[Path]:
        for name in ("path", "db_path", "index_path", "database_path"):
            value = getattr(index, name, None)
            if value is not None and not callable(value):
                return Path(value).expanduser().resolve()
        return None

    @staticmethod
    def _find_index_method(index: Any, names: Sequence[str]) -> Any:
        for name in names:
            method = getattr(index, name, None)
            if callable(method):
                return method
        raise TypeError(
            "CacheIndex lacks required method; expected one of {0}".format(
                ", ".join(names)
            )
        )

    @staticmethod
    def _call_index_writer(method: Any, record: Any, connection: Any) -> Any:
        """Call the expected CacheIndex writer without falling back to SQL."""

        import inspect

        parameters = inspect.signature(method).parameters
        if "connection" in parameters:
            return method(record, connection=connection)
        if "conn" in parameters:
            return method(record, conn=connection)
        if "transaction" in parameters:
            return method(record, transaction=connection)
        # Some CacheIndex implementations bind a transaction to the instance
        # while inside ``transaction()`` and expose a one-argument writer.
        return method(record)

    def apply(self, index: Any, report: Optional[ScanReport] = None) -> Dict[str, Any]:
        """Insert a previously scanned plan through CacheIndex in one transaction.

        The caller must explicitly initialize the index first.  This method
        refuses any database path except ``<root>/cache_v2/index.sqlite`` and
        never creates an Artifact or copies a legacy payload.
        """

        report = report or self.scan()
        self.verify_report_sources(report)
        actual_path = self._index_path(index)
        expected_path = self.index_path.resolve()
        if actual_path is None:
            raise TypeError("CacheIndex does not expose its database path")
        if actual_path != expected_path:
            raise ValueError(
                "legacy apply may write only {0}; got {1}".format(
                    expected_path, actual_path
                )
            )
        source_records, conflict_records = self.to_contract_plan(report)
        transaction_factory = self._find_index_method(
            index, ("batch", "transaction", "write_transaction")
        )
        inserted_sources = 0
        inserted_conflicts = 0
        with transaction_factory() as writer:
            self.verify_report_sources(report)
            source_writer = self._find_index_method(
                writer,
                (
                    "register_legacy_source",
                    "add_legacy_source",
                    "upsert_legacy_source",
                ),
            )
            for record in source_records:
                self._call_index_writer(source_writer, record, writer)
                inserted_sources += 1
            if conflict_records:
                conflict_writer = self._find_index_method(
                    writer,
                    (
                        "record_conflict",
                        "add_artifact_conflict",
                        "record_artifact_conflict",
                        "register_artifact_conflict",
                        "add_conflict",
                    ),
                )
                for record in conflict_records:
                    self._call_index_writer(conflict_writer, record, writer)
                    inserted_conflicts += 1
            self.verify_report_sources(report)
        return {
            "index_path": str(expected_path),
            "source_state_hash": report.source_state_hash,
            "legacy_sources_written": inserted_sources,
            "conflicts_written": inserted_conflicts,
            "formal_artifacts_written": 0,
        }
