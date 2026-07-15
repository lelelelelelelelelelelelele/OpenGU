"""Dataset-free immutable Selection Artifact storage for Cache V2.

The store accepts only Recipe identity and already-produced selected nodes.
It never owns or invokes a Selection producer.  Exact resolution, payload and
sidecar integrity, immutable writes, conflict quarantine, and index updates
remain Cache responsibilities.
"""

from __future__ import annotations

import json
import operator
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

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
    utc_now_iso,
    validate_artifact_id,
    validate_sha256,
)
from .errors import (
    ArtifactStoreError,
    CacheResolutionError,
    ContractValidationError,
    PathValidationError,
)
from .index import CacheIndex
from .paths import normalize_relative_path, normalize_semantic_path
from .resolver import ArtifactResolver
from .conflict_resolution import ConflictResolutionLedger


SELECTION_PAYLOAD_VERSION = 1
SELECTION_PAYLOAD_SCHEMA = "cache_v2.selection"
CONFLICT_MARKER_VERSION = 1


class ArtifactIntegrityError(ArtifactStoreError):
    """An indexed payload or sidecar failed closed verification."""


class ArtifactConflictError(ArtifactStoreError):
    """A recomputation observed different content for the same Recipe."""

    def __init__(self, conflict_id: str, quarantine_path: str):
        self.conflict_id = conflict_id
        self.quarantine_path = quarantine_path
        super().__init__(
            "Recipe conflict recorded as {0}; observation quarantined at {1}".format(
                conflict_id, quarantine_path
            )
        )


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
        raise ContractValidationError("payload is not canonical JSON: {0}".format(exc))
    return text.encode("utf-8")


def _reject_constant(value: str) -> None:
    raise ValueError("non-finite JSON number {0} is forbidden".format(value))


def _unique_object(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {0}".format(key))
        result[key] = value
    return result


def _parse_canonical_plain_json(payload: bytes, label: str) -> Any:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ArtifactIntegrityError("{0} is not UTF-8: {1}".format(label, exc))
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (TypeError, ValueError) as exc:
        raise ArtifactIntegrityError("{0} is invalid JSON: {1}".format(label, exc))
    if _plain_json_bytes(value) != payload:
        raise ArtifactIntegrityError("{0} is not canonical JSON".format(label))
    return value


def _node_sequence(value: Any) -> Tuple[int, ...]:
    if hasattr(value, "tolist") and not isinstance(value, (str, bytes, bytearray)):
        value = value.tolist()
    if isinstance(value, (str, bytes, bytearray)):
        raise ContractValidationError("selected_nodes_ordered must be an integer sequence")
    try:
        items = list(value)
    except TypeError:
        raise ContractValidationError("selected_nodes_ordered must be an integer sequence")

    nodes = []
    for position, item in enumerate(items):
        if isinstance(item, bool):
            raise ContractValidationError(
                "selected node at position {0} must be an integer, not bool".format(
                    position
                )
            )
        try:
            integer = operator.index(item)
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "selected node at position {0} is not an integer".format(position)
            )
        nodes.append(integer)
    if len(set(nodes)) != len(nodes):
        raise ContractValidationError("selected_nodes_ordered contains duplicates")
    return tuple(nodes)


def _nodes_hash(nodes: Sequence[int]) -> str:
    return sha256_bytes(_plain_json_bytes(list(nodes)))


def _required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ContractValidationError("{0} must be a non-empty string".format(label))
    return value.strip()


def _recipe_graph_fingerprint(fields: Mapping[str, Any]) -> str:
    names = (
        "graph_fingerprint",
        "topology_fingerprint",
        "training_graph_fingerprint",
    )
    values = [fields[name] for name in names if name in fields]
    if not values:
        raise ContractValidationError(
            "Selection Recipe requires graph_fingerprint, topology_fingerprint, "
            "or training_graph_fingerprint"
        )
    if any(value != values[0] for value in values[1:]):
        raise ContractValidationError("Selection Recipe graph fingerprints disagree")
    return validate_sha256(values[0], "Recipe graph fingerprint")


def _validate_candidate_input(
    recipe: ArtifactRecipe,
    num_nodes: int,
    candidate_nodes: Optional[Sequence[int]],
) -> Optional[Tuple[int, ...]]:
    """Validate caller-supplied candidates before resolution or production."""

    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
        raise ContractValidationError("num_nodes must be a non-negative integer")
    expected_hash = validate_sha256(
        recipe.fields.get("candidate_set_hash"), "Recipe candidate_set_hash"
    )
    if candidate_nodes is None:
        return None
    candidates = _node_sequence(candidate_nodes)
    for node in candidates:
        if node < 0 or node >= num_nodes:
            raise ContractValidationError(
                "candidate node {0} is outside [0, {1})".format(node, num_nodes)
            )
    observed_hash = _nodes_hash(sorted(candidates))
    if observed_hash != expected_hash:
        raise ContractValidationError(
            "candidate_nodes do not match Recipe candidate_set_hash"
        )
    return candidates


@dataclass(frozen=True)
class SelectionPayload:
    """Versioned, canonical JSON payload for one ordered node Selection."""

    payload_version: int
    selected_nodes_ordered: Tuple[int, ...]
    ordered_nodes_hash: str
    node_set_hash: str
    graph_fingerprint: str
    candidate_set_hash: str
    node_id_space: str
    source_score_artifact_id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.payload_version != SELECTION_PAYLOAD_VERSION:
            raise ContractValidationError(
                "unsupported Selection payload version {0}; expected {1}".format(
                    self.payload_version, SELECTION_PAYLOAD_VERSION
                )
            )
        nodes = _node_sequence(self.selected_nodes_ordered)
        ordered_hash = validate_sha256(self.ordered_nodes_hash, "ordered_nodes_hash")
        set_hash = validate_sha256(self.node_set_hash, "node_set_hash")
        graph_hash = validate_sha256(self.graph_fingerprint, "graph_fingerprint")
        candidate_hash = validate_sha256(
            self.candidate_set_hash, "candidate_set_hash"
        )
        node_space = _required_text(self.node_id_space, "node_id_space")
        source_id = self.source_score_artifact_id
        if source_id is not None:
            source_id = validate_artifact_id(source_id, "source_score_artifact_id")
            if not source_id.startswith("score_"):
                raise ContractValidationError(
                    "source_score_artifact_id must identify a Score Artifact"
                )
        expected_ordered = _nodes_hash(nodes)
        expected_set = _nodes_hash(sorted(nodes))
        if ordered_hash != expected_ordered:
            raise ContractValidationError(
                "ordered_nodes_hash does not match selected_nodes_ordered"
            )
        if set_hash != expected_set:
            raise ContractValidationError(
                "node_set_hash does not match selected_nodes_ordered"
            )
        object.__setattr__(self, "selected_nodes_ordered", nodes)
        object.__setattr__(self, "ordered_nodes_hash", ordered_hash)
        object.__setattr__(self, "node_set_hash", set_hash)
        object.__setattr__(self, "graph_fingerprint", graph_hash)
        object.__setattr__(self, "candidate_set_hash", candidate_hash)
        object.__setattr__(self, "node_id_space", node_space)
        object.__setattr__(self, "source_score_artifact_id", source_id)

    @classmethod
    def build(
        cls,
        selected_nodes: Any,
        graph_fingerprint: str,
        candidate_set_hash: str,
        node_id_space: str = "global",
        source_score_artifact_id: Optional[str] = None,
    ) -> "SelectionPayload":
        nodes = _node_sequence(selected_nodes)
        return cls(
            payload_version=SELECTION_PAYLOAD_VERSION,
            selected_nodes_ordered=nodes,
            ordered_nodes_hash=_nodes_hash(nodes),
            node_set_hash=_nodes_hash(sorted(nodes)),
            graph_fingerprint=graph_fingerprint,
            candidate_set_hash=candidate_set_hash,
            node_id_space=node_id_space,
            source_score_artifact_id=source_score_artifact_id,
        )

    @classmethod
    def from_bytes(cls, payload: bytes) -> "SelectionPayload":
        value = _parse_canonical_plain_json(payload, "Selection payload")
        if not isinstance(value, dict):
            raise ArtifactIntegrityError("Selection payload must be a JSON object")
        expected = {
            "payload_version",
            "selected_nodes_ordered",
            "ordered_nodes_hash",
            "node_set_hash",
            "graph_fingerprint",
            "candidate_set_hash",
            "node_id_space",
            "source_score_artifact_id",
        }
        if set(value) != expected:
            missing = sorted(expected.difference(value))
            extra = sorted(set(value).difference(expected))
            raise ArtifactIntegrityError(
                "Selection payload schema mismatch; missing={0}, extra={1}".format(
                    missing, extra
                )
            )
        try:
            return cls(**value)
        except (CacheV2Error, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError(
                "Selection payload contract is invalid: {0}".format(exc)
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_version": self.payload_version,
            "selected_nodes_ordered": list(self.selected_nodes_ordered),
            "ordered_nodes_hash": self.ordered_nodes_hash,
            "node_set_hash": self.node_set_hash,
            "graph_fingerprint": self.graph_fingerprint,
            "candidate_set_hash": self.candidate_set_hash,
            "node_id_space": self.node_id_space,
            "source_score_artifact_id": self.source_score_artifact_id,
        }

    @property
    def canonical_bytes(self) -> bytes:
        return _plain_json_bytes(self.to_dict())

    @property
    def content_hash(self) -> str:
        return sha256_bytes(self.canonical_bytes)

    def validate_against(
        self,
        recipe: ArtifactRecipe,
        num_nodes: int,
        candidate_nodes: Optional[Sequence[int]] = None,
    ) -> None:
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
            raise ContractValidationError("num_nodes must be a non-negative integer")
        fields = recipe.fields
        graph_hash = _recipe_graph_fingerprint(fields)
        candidate_hash = validate_sha256(
            fields.get("candidate_set_hash"), "Recipe candidate_set_hash"
        )
        node_space = _required_text(fields.get("node_id_space"), "Recipe node_id_space")
        k = fields.get("k")
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ContractValidationError("Selection Recipe k must be a non-negative integer")
        if graph_hash != self.graph_fingerprint:
            raise ArtifactIntegrityError("payload graph fingerprint does not match Recipe")
        if candidate_hash != self.candidate_set_hash:
            raise ArtifactIntegrityError("payload candidate-set hash does not match Recipe")
        if node_space != self.node_id_space:
            raise ArtifactIntegrityError("payload node-id space does not match Recipe")
        if k != len(self.selected_nodes_ordered):
            raise ArtifactIntegrityError("payload node count does not match Recipe k")
        expected_source = fields.get("source_score_artifact_id")
        if expected_source != self.source_score_artifact_id:
            raise ArtifactIntegrityError(
                "payload source Score Artifact does not match Recipe"
            )
        for node in self.selected_nodes_ordered:
            if node < 0 or node >= num_nodes:
                raise ArtifactIntegrityError(
                    "selected node {0} is outside [0, {1})".format(node, num_nodes)
                )
        if candidate_nodes is not None:
            candidates = _node_sequence(candidate_nodes)
            for node in candidates:
                if node < 0 or node >= num_nodes:
                    raise ArtifactIntegrityError(
                        "candidate node {0} is outside [0, {1})".format(
                            node, num_nodes
                        )
                    )
            observed_candidate_hash = _nodes_hash(sorted(candidates))
            if observed_candidate_hash != candidate_hash:
                raise ArtifactIntegrityError(
                    "candidate_nodes do not match Recipe candidate_set_hash"
                )
            candidate_set = set(candidates)
            missing = [
                node
                for node in self.selected_nodes_ordered
                if node not in candidate_set
            ]
            if missing:
                raise ArtifactIntegrityError(
                    "selected nodes are not members of candidate_nodes: {0}".format(
                        missing
                    )
                )


@dataclass(frozen=True)
class StoreResult:
    hit: bool
    outcome: str
    artifact_id: str
    content_hash: str
    semantic_path: str
    payload: SelectionPayload
    producer_called: bool
    miss_reasons: Tuple[str, ...] = ()


@dataclass(frozen=True)
class _CreatedFile:
    """Filesystem identity for a file created by the current operation."""

    path: Path
    device: int
    inode: int


class ArtifactStore:
    """Absolute-root, exact-only Selection ArtifactStore.

    Normal resolution never scans payload directories and never falls back to
    Legacy caches.  Canary and materializer CLIs share this same store API.
    """

    def __init__(
        self,
        root: Union[str, Path],
        producer_version: ProducerVersion,
        index: Optional[CacheIndex] = None,
        trace_path: Optional[Union[str, Path]] = None,
    ) -> None:
        supplied = Path(root).expanduser()
        if not supplied.is_absolute():
            raise PathValidationError(
                "ArtifactStore root must be explicitly absolute: {0!r}".format(str(root))
            )
        if ".." in supplied.parts:
            raise PathValidationError("ArtifactStore root must not contain '..'")
        if not isinstance(producer_version, ProducerVersion):
            raise ContractValidationError("producer_version must be ProducerVersion")
        if not producer_version.is_identified:
            raise ContractValidationError("producer_version must identify its producer")
        self.root = supplied.resolve(strict=False)
        self.index = index or CacheIndex(self.root / "index.sqlite")
        if not isinstance(self.index, CacheIndex):
            raise ContractValidationError("index must be CacheIndex")
        if ".." in self.index.database_path.parts:
            raise PathValidationError("CacheIndex database must not contain '..'")
        self._require_below_root(self.index.database_path, "CacheIndex database")
        self.producer_version = producer_version
        self.trace_path = self._store_path(trace_path, "trace.jsonl")

    def _store_path(
        self, supplied: Optional[Union[str, Path]], default_name: str
    ) -> Path:
        if supplied is None:
            path = self.root / default_name
        else:
            value = Path(supplied)
            if value.is_absolute():
                if ".." in value.parts:
                    raise PathValidationError(
                        "{0} must not contain '..'".format(default_name)
                    )
                path = value
            else:
                relative = normalize_relative_path(str(value), label=default_name)
                path = self.root.joinpath(*PurePosixPath(relative).parts)
        return self._require_below_root(path, default_name)

    def _require_below_root(self, path: Path, label: str) -> Path:
        resolved = Path(path).resolve(strict=False)
        try:
            relative = resolved.relative_to(self.root)
        except ValueError:
            raise PathValidationError("{0} must stay below ArtifactStore root".format(label))
        if not relative.parts:
            raise PathValidationError(
                "{0} must be a file or directory below ArtifactStore root".format(
                    label
                )
            )
        return resolved

    def _safe_output_path(self, path: Path, label: str) -> Path:
        """Resolve an output immediately before I/O and reject symlink escape."""

        if ".." in Path(path).parts:
            raise PathValidationError("{0} must not contain '..'".format(label))
        return self._require_below_root(Path(path), label)

    def initialize(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self._safe_output_path(self.index.database_path, "CacheIndex database")
        self.index.initialize()

    def _ensure_initialized(self) -> None:
        if not self.root.is_dir() or not self.index.database_path.is_file():
            raise ArtifactStoreError("ArtifactStore is not initialized")
        self.index.check_schema()

    def _trace(self, event: str, **fields: Any) -> None:
        entry = {"event": event, "timestamp": utc_now_iso()}
        entry.update(fields)
        payload = _plain_json_bytes(entry) + b"\n"
        trace_path = self._safe_output_path(self.trace_path, "trace")
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path = self._safe_output_path(trace_path, "trace")
        descriptor = os.open(
            str(trace_path), os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600
        )
        try:
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _atomic_write_once(
        self, path: Path, payload: bytes
    ) -> Optional[_CreatedFile]:
        """Publish complete bytes without an overwrite race.

        A same-directory temporary is hard-linked into place.  Linking fails
        atomically when any destination already exists; identical content is
        idempotent, while different content fails closed.
        """

        path = self._safe_output_path(path, "write-once target")
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.parent / (".{0}.{1}.tmp".format(path.name, uuid.uuid4().hex))
        temporary = self._safe_output_path(temporary, "temporary output")
        try:
            with temporary.open("xb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            path = self._safe_output_path(path, "write-once target")
            try:
                os.link(str(temporary), str(path))
            except FileExistsError:
                path = self._safe_output_path(path, "existing write-once target")
                if not path.is_file() or path.read_bytes() != payload:
                    raise ArtifactIntegrityError(
                        "refusing to overwrite existing store file: {0}".format(path)
                    )
                return None
            created = path.stat()
            return _CreatedFile(path, created.st_dev, created.st_ino)
        finally:
            if temporary.exists():
                temporary.unlink()

    def _cleanup_created_file(self, created: Optional[_CreatedFile]) -> None:
        """Remove only the exact filesystem object created by this call."""

        if created is None:
            return
        try:
            observed = created.path.lstat()
        except FileNotFoundError:
            return
        if observed.st_dev == created.device and observed.st_ino == created.inode:
            created.path.unlink()

    @contextmanager
    def _exclusive_lock(
        self, lock_name: str, timeout_seconds: float = 30.0
    ) -> Iterator[None]:
        """Cross-process fail-closed lock whose cleanup is ownership checked."""

        lock_path = self._safe_output_path(
            self.root / ".locks" / (lock_name + ".lock"), "coordination lock"
        )
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self._safe_output_path(lock_path, "coordination lock")
        token = _plain_json_bytes(
            {"pid": os.getpid(), "token": uuid.uuid4().hex, "version": 1}
        )
        deadline = time.monotonic() + timeout_seconds
        identity: Optional[Tuple[int, int]] = None
        while identity is None:
            try:
                descriptor = os.open(
                    str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600
                )
            except FileExistsError:
                self._safe_output_path(lock_path, "coordination lock")
                if time.monotonic() >= deadline:
                    raise CacheResolutionError(
                        "timed out waiting for coordination lock {0}".format(
                            lock_name
                        )
                    )
                time.sleep(0.05)
                continue
            try:
                os.write(descriptor, token)
                os.fsync(descriptor)
                observed = os.fstat(descriptor)
                identity = (observed.st_dev, observed.st_ino)
            finally:
                os.close(descriptor)
        try:
            yield
        finally:
            try:
                observed = lock_path.lstat()
                if (
                    identity is not None
                    and observed.st_dev == identity[0]
                    and observed.st_ino == identity[1]
                    and lock_path.read_bytes() == token
                ):
                    lock_path.unlink()
            except FileNotFoundError:
                pass

    def _recipe_lock(self, recipe: ArtifactRecipe) -> Any:
        return self._exclusive_lock("selection-" + recipe.recipe_hash)

    def _conflict_marker_paths(
        self, recipe: ArtifactRecipe
    ) -> Tuple[str, Path]:
        semantic = normalize_semantic_path(
            "conflict_markers/selection/{0}/marker.json".format(
                recipe.recipe_hash
            )
        )
        marker_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts),
            "conflict marker",
        )
        return semantic, marker_path

    def _inspect_conflict_marker(
        self, recipe: ArtifactRecipe
    ) -> Optional[Dict[str, Any]]:
        """Return a valid marker, or fail closed on any partial/corrupt state."""

        raw_directories = (
            self.root / "conflict_markers",
            self.root / "conflict_markers" / "selection",
            self.root
            / "conflict_markers"
            / "selection"
            / recipe.recipe_hash,
        )
        for position, raw_directory in enumerate(raw_directories):
            if raw_directory.is_symlink():
                raise CacheResolutionError(
                    "conflict marker directory is a symlink: {0}".format(
                        raw_directory
                    )
                )
            try:
                directory = self._safe_output_path(
                    raw_directory, "conflict marker directory"
                )
            except PathValidationError as exc:
                raise CacheResolutionError(
                    "conflict marker directory escapes ArtifactStore root: {0}".format(
                        exc
                    )
                )
            if not directory.exists():
                # A missing ancestor means no marker has ever been committed.
                return None
            if not directory.is_dir():
                raise CacheResolutionError(
                    "conflict marker directory is not a directory: {0}".format(
                        directory
                    )
                )
            if position < 2:
                continue

            entries = list(directory.iterdir())
            if len(entries) != 1 or entries[0].name != "marker.json":
                raise CacheResolutionError(
                    "conflict marker recipe directory is incomplete or unexpected"
                )
            if entries[0].is_symlink():
                raise CacheResolutionError(
                    "conflict marker must not be a symlink"
                )

        try:
            semantic, marker_path = self._conflict_marker_paths(recipe)
        except PathValidationError as exc:
            raise CacheResolutionError(
                "conflict marker escapes ArtifactStore root: {0}".format(exc)
            )
        if marker_path.is_symlink() or not marker_path.is_file():
            raise CacheResolutionError(
                "conflict marker is not a regular file: {0}".format(semantic)
            )
        try:
            value = _parse_canonical_plain_json(
                marker_path.read_bytes(), "conflict marker"
            )
        except ArtifactIntegrityError as exc:
            raise CacheResolutionError(
                "conflict marker is corrupt: {0}".format(exc)
            )
        expected_keys = {
            "artifact_type",
            "existing_artifact_id",
            "existing_content_hash",
            "marker_version",
            "observed_content_hash",
            "reason",
            "recipe_hash",
        }
        if not isinstance(value, dict) or set(value) != expected_keys:
            raise CacheResolutionError("conflict marker schema is invalid")
        try:
            existing_id = validate_artifact_id(
                value["existing_artifact_id"], "existing_artifact_id"
            )
            existing_hash = validate_sha256(
                value["existing_content_hash"], "existing_content_hash"
            )
            observed_hash = validate_sha256(
                value["observed_content_hash"], "observed_content_hash"
            )
        except CacheV2Error as exc:
            raise CacheResolutionError(
                "conflict marker contract is invalid: {0}".format(exc)
            )
        if (
            value["marker_version"] != CONFLICT_MARKER_VERSION
            or value["artifact_type"] != ArtifactType.SELECTION.value
            or value["recipe_hash"] != recipe.recipe_hash
            or value["reason"] != "content_conflict"
            or not existing_id.startswith("sel_")
            or existing_hash == observed_hash
        ):
            raise CacheResolutionError("conflict marker identity is invalid")
        return value

    def _sync_directory(self, directory: Path) -> None:
        """Persist a new directory entry where the platform exposes fsync."""

        if os.name == "nt":
            return
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        descriptor = os.open(str(directory), flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _write_conflict_marker(
        self,
        recipe: ArtifactRecipe,
        existing_artifact_id: str,
        existing_content_hash: str,
        observed_content_hash: str,
    ) -> str:
        """Permanently remember the first differing-content observation."""

        existing = self._inspect_conflict_marker(recipe)
        semantic, marker_path = self._conflict_marker_paths(recipe)
        if existing is not None:
            return semantic
        marker = {
            "artifact_type": ArtifactType.SELECTION.value,
            "existing_artifact_id": validate_artifact_id(
                existing_artifact_id, "existing_artifact_id"
            ),
            "existing_content_hash": validate_sha256(
                existing_content_hash, "existing_content_hash"
            ),
            "marker_version": CONFLICT_MARKER_VERSION,
            "observed_content_hash": validate_sha256(
                observed_content_hash, "observed_content_hash"
            ),
            "reason": "content_conflict",
            "recipe_hash": recipe.recipe_hash,
        }
        if marker["existing_content_hash"] == marker["observed_content_hash"]:
            raise ContractValidationError(
                "identical content must not create a conflict marker"
            )
        marker_path.parent.mkdir(parents=True, exist_ok=False)
        marker_path = self._safe_output_path(marker_path, "conflict marker")
        created = self._atomic_write_once(marker_path, _plain_json_bytes(marker))
        if created is not None:
            # The marker is permanent: a later quarantine or SQLite failure
            # must never invoke cleanup for this filesystem identity.
            self._sync_directory(marker_path.parent)
        validated = self._inspect_conflict_marker(recipe)
        if validated is None:
            raise CacheResolutionError("conflict marker was not durably published")
        return semantic

    def _assert_no_conflict_marker(self, recipe: ArtifactRecipe) -> None:
        marker = self._inspect_conflict_marker(recipe)
        if marker is None:
            return
        conflicts = self.index.conflicts(
            artifact_type=ArtifactType.SELECTION, recipe_hash=recipe.recipe_hash
        )
        if not conflicts:
            raise CacheResolutionError(
                "durable conflict marker has no indexed conflict and blocks exact Selection hit"
            )
        resolved, unresolved = ConflictResolutionLedger(self.index).classify(conflicts)
        marker_match = any(
            item["conflict"].get("existing_artifact_id")
            == marker["existing_artifact_id"]
            and item["conflict"].get("existing_content_hash")
            == marker["existing_content_hash"]
            and item["conflict"].get("observed_content_hash")
            == marker["observed_content_hash"]
            for item in resolved
        )
        if unresolved or not marker_match:
            raise CacheResolutionError(
                "durable conflict marker blocks exact Selection hit for Recipe {0}".format(
                    recipe.recipe_hash
                )
            )

    def _formal_paths(self, recipe: ArtifactRecipe, artifact_id: str) -> Tuple[str, Path, Path]:
        semantic = normalize_semantic_path(
            "artifacts/selection/{0}/payload.json".format(artifact_id)
        )
        payload_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts), "formal payload"
        )
        return semantic, payload_path, payload_path.with_name("header.json")

    def _sidecar_bytes(self, header: ArtifactHeader, payload_size: int) -> bytes:
        return _plain_json_bytes(
            {
                "artifact_header": header.to_dict(),
                "payload_contract": {
                    "schema": SELECTION_PAYLOAD_SCHEMA,
                    "version": SELECTION_PAYLOAD_VERSION,
                    "size_bytes": payload_size,
                },
            }
        )

    def _header_for_payload(
        self,
        recipe: ArtifactRecipe,
        payload: SelectionPayload,
        semantic_path: str,
        compute_seconds: float,
        status: ArtifactStatus = ArtifactStatus.VALID,
    ) -> ArtifactHeader:
        payload_bytes = payload.canonical_bytes
        return ArtifactHeader(
            artifact_type=ArtifactType.SELECTION,
            recipe=recipe,
            content_hash=sha256_bytes(payload_bytes),
            producer_version=self.producer_version,
            status=status,
            verification_status=VerificationStatus.VERIFIED,
            semantic_path=semantic_path,
            compute_seconds=compute_seconds,
            metadata={
                "payload_schema": SELECTION_PAYLOAD_SCHEMA,
                "payload_version": SELECTION_PAYLOAD_VERSION,
                "payload_size_bytes": len(payload_bytes),
            },
        )

    def _write_formal(
        self,
        recipe: ArtifactRecipe,
        payload: SelectionPayload,
        compute_seconds: float,
        miss_reasons: Tuple[str, ...],
        num_nodes: int,
        candidate_nodes: Optional[Sequence[int]],
    ) -> StoreResult:
        artifact_id = build_artifact_id(
            ArtifactType.SELECTION, recipe.recipe_hash, payload.content_hash
        )
        semantic, payload_path, header_path = self._formal_paths(
            recipe, artifact_id
        )
        header = self._header_for_payload(
            recipe, payload, semantic, compute_seconds
        )
        payload_bytes = payload.canonical_bytes
        created_payload: Optional[_CreatedFile] = None
        created_header: Optional[_CreatedFile] = None
        identical_artifact_id: Optional[str] = None
        conflict_error: Optional[ArtifactConflictError] = None
        try:
            # BEGIN IMMEDIATE closes the last DB race even for writers that do
            # not cooperate with the filesystem recipe lock.
            with self.index.transaction() as writer:
                existing = writer.connection.execute(
                    """
                    SELECT artifact_id, content_hash FROM artifacts
                    WHERE artifact_type = ? AND recipe_hash = ?
                    """,
                    (ArtifactType.SELECTION.value, recipe.recipe_hash),
                ).fetchone()
                if existing is not None:
                    existing_id = str(existing["artifact_id"])
                    existing_hash = str(existing["content_hash"])
                    if existing_hash == header.content_hash:
                        identical_artifact_id = existing_id
                    else:
                        self._write_conflict_marker(
                            recipe,
                            existing_id,
                            existing_hash,
                            header.content_hash,
                        )
                        quarantine_path, observed_header = (
                            self._quarantine_observation(
                                recipe, payload, compute_seconds
                            )
                        )
                        conflict = ArtifactConflictRecord(
                            artifact_type=ArtifactType.SELECTION,
                            recipe_hash=recipe.recipe_hash,
                            existing_artifact_id=existing_id,
                            existing_content_hash=existing_hash,
                            observed_content_hash=observed_header.content_hash,
                            quarantine_path=quarantine_path,
                            metadata={
                                "observed_artifact_id": observed_header.artifact_id
                            },
                        )
                        writer.record_conflict(conflict)
                        conflict_error = ArtifactConflictError(
                            conflict.conflict_id, quarantine_path
                        )
                else:
                    created_payload = self._atomic_write_once(
                        payload_path, payload_bytes
                    )
                    created_header = self._atomic_write_once(
                        header_path,
                        self._sidecar_bytes(header, len(payload_bytes)),
                    )
                    registration = writer.register_artifact(header)
                    if registration.outcome != RegisterOutcome.CREATED:
                        raise ArtifactStoreError(
                            "unexpected registration outcome under write lock: {0}".format(
                                registration.outcome.value
                            )
                        )
        except Exception:
            self._cleanup_created_file(created_header)
            self._cleanup_created_file(created_payload)
            raise

        if conflict_error is not None:
            self._trace(
                "artifact_conflict",
                recipe_hash=recipe.recipe_hash,
                conflict_id=conflict_error.conflict_id,
                quarantine_path=conflict_error.quarantine_path,
            )
            raise conflict_error

        if identical_artifact_id is not None:
            candidate = self.index.get_artifact(identical_artifact_id)
            loaded = self._load_candidate(
                candidate,
                recipe,
                num_nodes,
                candidate_nodes=candidate_nodes,
                miss_reasons=miss_reasons,
            )
            return StoreResult(
                hit=True,
                outcome=RegisterOutcome.IDENTICAL.value,
                artifact_id=loaded.artifact_id,
                content_hash=loaded.content_hash,
                semantic_path=loaded.semantic_path,
                payload=payload,
                producer_called=False,
                miss_reasons=miss_reasons,
            )

        self._trace(
            "artifact_registered",
            recipe_hash=recipe.recipe_hash,
            artifact_id=header.artifact_id,
            outcome=RegisterOutcome.CREATED.value,
            semantic_path=semantic,
        )
        return StoreResult(
            hit=False,
            outcome=RegisterOutcome.CREATED.value,
            artifact_id=header.artifact_id,
            content_hash=header.content_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def _quarantine_observation(
        self,
        recipe: ArtifactRecipe,
        payload: SelectionPayload,
        compute_seconds: float,
    ) -> Tuple[str, ArtifactHeader]:
        content_hash = payload.content_hash
        semantic = normalize_semantic_path(
            "quarantine/selection/{0}/{1}-{2}/payload.json".format(
                recipe.recipe_hash[:16], content_hash[:16], uuid.uuid4().hex
            )
        )
        payload_path = self._safe_output_path(
            self.root.joinpath(*PurePosixPath(semantic).parts),
            "quarantine payload",
        )
        header = self._header_for_payload(
            recipe,
            payload,
            semantic,
            compute_seconds,
            status=ArtifactStatus.CONFLICT,
        )
        created_payload: Optional[_CreatedFile] = None
        created_header: Optional[_CreatedFile] = None
        try:
            created_payload = self._atomic_write_once(
                payload_path, payload.canonical_bytes
            )
            created_header = self._atomic_write_once(
                payload_path.with_name("header.json"),
                self._sidecar_bytes(header, len(payload.canonical_bytes)),
            )
        except Exception:
            self._cleanup_created_file(created_header)
            self._cleanup_created_file(created_payload)
            raise
        return semantic, header

    def _load_candidate(
        self,
        candidate: Mapping[str, Any],
        recipe: ArtifactRecipe,
        num_nodes: int,
        candidate_nodes: Optional[Sequence[int]],
        miss_reasons: Tuple[str, ...] = (),
    ) -> StoreResult:
        if candidate.get("artifact_type") != ArtifactType.SELECTION.value:
            raise ArtifactIntegrityError("indexed candidate is not a Selection Artifact")
        if candidate.get("recipe_hash") != recipe.recipe_hash:
            raise ArtifactIntegrityError("indexed candidate Recipe hash changed")
        if candidate.get("status") != ArtifactStatus.VALID.value:
            raise ArtifactIntegrityError("indexed candidate is not valid")
        if candidate.get("verification_status") != VerificationStatus.VERIFIED.value:
            raise ArtifactIntegrityError("indexed candidate is not verified")
        semantic = candidate.get("semantic_path")
        if not isinstance(semantic, str):
            raise ArtifactIntegrityError("indexed candidate has no semantic_path")
        semantic = normalize_semantic_path(semantic)
        try:
            payload_path = self._safe_output_path(
                self.root.joinpath(*PurePosixPath(semantic).parts),
                "indexed Selection payload",
            )
            header_path = self._safe_output_path(
                payload_path.with_name("header.json"),
                "indexed Artifact header",
            )
        except PathValidationError as exc:
            raise ArtifactIntegrityError(
                "indexed Selection path escapes ArtifactStore root: {0}".format(exc)
            )
        if not payload_path.is_file() or not header_path.is_file():
            raise ArtifactIntegrityError("indexed Selection payload or header is missing")

        header_value = _parse_canonical_plain_json(
            header_path.read_bytes(), "Artifact header sidecar"
        )
        if not isinstance(header_value, dict) or set(header_value) != {
            "artifact_header",
            "payload_contract",
        }:
            raise ArtifactIntegrityError("Artifact header sidecar schema is invalid")
        artifact_header = header_value["artifact_header"]
        payload_contract = header_value["payload_contract"]
        if not isinstance(artifact_header, dict) or not isinstance(payload_contract, dict):
            raise ArtifactIntegrityError("Artifact header sidecar sections are invalid")
        if (
            set(payload_contract) != {"schema", "version", "size_bytes"}
            or payload_contract.get("schema") != SELECTION_PAYLOAD_SCHEMA
            or payload_contract.get("version") != SELECTION_PAYLOAD_VERSION
            or isinstance(payload_contract.get("size_bytes"), bool)
            or not isinstance(payload_contract.get("size_bytes"), int)
            or payload_contract["size_bytes"] < 0
        ):
            raise ArtifactIntegrityError("payload size/schema contract is invalid")

        producer_value = artifact_header.get("producer_version")
        if not isinstance(producer_value, dict) or set(producer_value) != {
            "semantic_version",
            "source_fingerprint",
        }:
            raise ArtifactIntegrityError(
                "Artifact header producer_version contract is invalid"
            )
        expected_metadata = {
            "payload_schema": SELECTION_PAYLOAD_SCHEMA,
            "payload_version": SELECTION_PAYLOAD_VERSION,
            "payload_size_bytes": payload_contract["size_bytes"],
        }
        if artifact_header.get("metadata") != canonicalize(expected_metadata):
            raise ArtifactIntegrityError(
                "payload size does not match Artifact header metadata"
            )
        try:
            producer_version = ProducerVersion(**producer_value)
            versioned_header = ArtifactHeader(
                header_version=artifact_header["header_version"],
                artifact_id=artifact_header["artifact_id"],
                artifact_type=artifact_header["artifact_type"],
                recipe=recipe,
                content_hash=artifact_header["content_hash"],
                producer_version=producer_version,
                status=artifact_header["status"],
                verification_status=artifact_header["verification_status"],
                semantic_path=artifact_header["semantic_path"],
                compute_seconds=artifact_header["compute_seconds"],
                created_at=artifact_header["created_at"],
                metadata=expected_metadata,
            )
        except (CacheV2Error, KeyError, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError(
                "Artifact header sidecar violates versioned contract: {0}".format(
                    exc
                )
            )
        if versioned_header.to_dict() != artifact_header:
            raise ArtifactIntegrityError(
                "Artifact header sidecar fields are not self-consistent"
            )

        index_expectations = {
            "artifact_id": versioned_header.artifact_id,
            "artifact_type": versioned_header.artifact_type.value,
            "recipe_hash": versioned_header.recipe_hash,
            "content_hash": versioned_header.content_hash,
            "semantic_path": versioned_header.semantic_path,
            "status": versioned_header.status.value,
            "verification_status": versioned_header.verification_status.value,
            "compute_seconds": versioned_header.compute_seconds,
            "created_at": versioned_header.created_at,
            "header_version": versioned_header.header_version,
        }
        for key, expected in index_expectations.items():
            if candidate.get(key) != expected:
                raise ArtifactIntegrityError(
                    "Artifact header sidecar {0} does not match index".format(key)
                )
        if candidate.get("recipe") != recipe.canonical_form:
            raise ArtifactIntegrityError(
                "Artifact header Recipe does not match indexed recipe_json"
            )
        if candidate.get("producer_version") != canonicalize(
            producer_version.to_dict()
        ):
            raise ArtifactIntegrityError(
                "Artifact header producer_version does not match index"
            )
        if candidate.get("metadata") != canonicalize(expected_metadata):
            raise ArtifactIntegrityError(
                "Artifact header metadata does not match index"
            )

        before = payload_path.stat()
        payload_bytes = payload_path.read_bytes()
        after = payload_path.stat()
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            raise ArtifactIntegrityError("Selection payload changed while being read")
        if len(payload_bytes) != after.st_size:
            raise ArtifactIntegrityError("Selection payload size changed while being read")
        if len(payload_bytes) != payload_contract["size_bytes"]:
            raise ArtifactIntegrityError("Selection payload size does not match header")
        observed_hash = sha256_bytes(payload_bytes)
        if observed_hash != candidate.get("content_hash"):
            raise ArtifactIntegrityError("Selection payload content hash mismatch")
        payload = SelectionPayload.from_bytes(payload_bytes)
        payload.validate_against(
            recipe, num_nodes, candidate_nodes=candidate_nodes
        )
        return StoreResult(
            hit=True,
            outcome="hit",
            artifact_id=candidate["artifact_id"],
            content_hash=observed_hash,
            semantic_path=semantic,
            payload=payload,
            producer_called=False,
            miss_reasons=miss_reasons,
        )

    def load(
        self,
        recipe: ArtifactRecipe,
        num_nodes: int,
        *,
        candidate_nodes: Sequence[int],
    ) -> StoreResult:
        self._ensure_initialized()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        candidates = _validate_candidate_input(recipe, num_nodes, candidate_nodes)
        with self._recipe_lock(recipe):
            self._assert_no_conflict_marker(recipe)
            explanation = ArtifactResolver(self.index).explain_exact(
                ArtifactType.SELECTION, recipe
            )
            if not explanation.hit or explanation.exact_candidate is None:
                raise CacheResolutionError(
                    "exact Selection Artifact is not resolvable: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            return self._load_candidate(
                explanation.exact_candidate,
                recipe,
                num_nodes,
                candidate_nodes=candidates,
                miss_reasons=explanation.miss_reasons,
            )

    def load_read_only(
        self,
        recipe: ArtifactRecipe,
        num_nodes: int,
        *,
        candidate_nodes: Optional[Sequence[int]] = None,
        artifact_id: Optional[str] = None,
    ) -> StoreResult:
        """Verify an immutable exact hit without creating a coordination lock.

        Runtime consumers already know the formal Artifact ID.  They do not
        compute, register, quarantine, or mutate payloads, so an on-disk writer
        lock would add an unnecessary cache write.  A second exact resolution
        after the payload read closes the conflict/status race fail-closed.
        """

        self._ensure_initialized()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        candidates = _validate_candidate_input(recipe, num_nodes, candidate_nodes)
        self._assert_no_conflict_marker(recipe)
        before = ArtifactResolver(self.index).explain_exact(
            ArtifactType.SELECTION, recipe
        )
        if not before.hit or before.exact_candidate is None:
            raise CacheResolutionError(
                "exact Selection Artifact is not resolvable: {0}".format(
                    ",".join(before.miss_reasons)
                )
            )
        if artifact_id is not None and before.exact_candidate.get("artifact_id") != artifact_id:
            raise CacheResolutionError(
                "exact Selection Artifact ID does not match requested Artifact"
            )
        result = self._load_candidate(
            before.exact_candidate,
            recipe,
            num_nodes,
            candidate_nodes=candidates,
            miss_reasons=before.miss_reasons,
        )
        self._assert_no_conflict_marker(recipe)
        after = ArtifactResolver(self.index).explain_exact(
            ArtifactType.SELECTION, recipe
        )
        if (
            not after.hit
            or after.exact_candidate is None
            or after.exact_candidate.get("artifact_id") != result.artifact_id
        ):
            raise CacheResolutionError(
                "exact Selection resolution changed during read"
            )
        return result

    def store_selection(
        self,
        recipe: ArtifactRecipe,
        selected_nodes: Sequence[int],
        *,
        num_nodes: int,
        candidate_nodes: Optional[Sequence[int]] = None,
        compute_seconds: float = 0.0,
    ) -> StoreResult:
        """Persist nodes already produced and validated by the experiment layer.

        No producer callback is accepted here.  Optional ``candidate_nodes`` is
        retained for callers that want Cache to repeat membership validation;
        the dataset-free boundary validates Recipe/payload hashes, node bounds,
        and immutable-store conflict semantics without it.
        """

        self._ensure_initialized()
        if not isinstance(recipe, ArtifactRecipe):
            raise ContractValidationError("recipe must be ArtifactRecipe")
        candidates = _validate_candidate_input(recipe, num_nodes, candidate_nodes)
        fields = recipe.fields
        payload = SelectionPayload.build(
            selected_nodes,
            graph_fingerprint=_recipe_graph_fingerprint(fields),
            candidate_set_hash=fields.get("candidate_set_hash"),
            node_id_space=fields.get("node_id_space"),
            source_score_artifact_id=fields.get("source_score_artifact_id"),
        )
        payload.validate_against(recipe, num_nodes, candidate_nodes=candidates)
        with self._recipe_lock(recipe):
            self._assert_no_conflict_marker(recipe)
            explanation = ArtifactResolver(self.index).explain_exact(
                ArtifactType.SELECTION, recipe
            )
            if (
                not explanation.hit
                and (
                    explanation.exact_candidate is not None
                    or explanation.miss_reasons != ("no_exact_candidate",)
                )
            ):
                raise CacheResolutionError(
                    "exact Selection lookup failed closed: {0}".format(
                        ",".join(explanation.miss_reasons)
                    )
                )
            result = self._write_formal(
                recipe,
                payload,
                compute_seconds,
                explanation.miss_reasons,
                num_nodes,
                candidate_nodes=candidates,
            )
            self._trace(
                "upstream_selection_stored",
                recipe_hash=recipe.recipe_hash,
                artifact_id=result.artifact_id,
                content_hash=result.content_hash,
                outcome=result.outcome,
            )
            return result

__all__ = [
    "SELECTION_PAYLOAD_SCHEMA",
    "SELECTION_PAYLOAD_VERSION",
    "ArtifactConflictError",
    "ArtifactIntegrityError",
    "ArtifactStore",
    "ArtifactStoreError",
    "CacheResolutionError",
    "SelectionPayload",
    "StoreResult",
]
