"""Append-only AutoReport V3 machine events.

V1/v2 Markdown is frozen under ``results/_journal/archive``. V3 uses a JSONL
audit stream while the live ``auto_report.md`` / ``auto_report.html`` pair is a
bounded projection that can be rebuilt at any time.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EVENT_PATH = REPO_ROOT / "results" / "_journal" / "auto_report.events.jsonl"
DEFAULT_STATUS_MD_PATH = REPO_ROOT / "results" / "_journal" / "auto_report.md"
DEFAULT_STATUS_HTML_PATH = REPO_ROOT / "results" / "_journal" / "auto_report.html"

EVENT_SCHEMA = "opengu.autoreport.event"
EVENT_SCHEMA_VERSION = 3
STAGES = {"selection", "attack", "collateral", "run"}
STATES = {"started", "completed", "failed", "skipped", "retrying"}
TERMINAL_STATES = {"completed", "failed", "skipped"}
CACHE_TYPES = {"selection", "result", "score", "artifact", "run_artifact"}
CACHE_OUTCOMES = {"hit", "miss", "bypass", "unknown"}
WRITE_OUTCOMES = {"saved", "reused", "not_written", "unknown"}

ENV_EVENT_PATH = "OPENGU_AUTOREPORT_EVENT_PATH"
ENV_STATUS_MD_PATH = "OPENGU_AUTOREPORT_STATUS_MD_PATH"
ENV_STATUS_HTML_PATH = "OPENGU_AUTOREPORT_STATUS_HTML_PATH"
ENV_CELL_ID = "OPENGU_AUTOREPORT_CELL_ID"
ENV_RUN_ID = "OPENGU_AUTOREPORT_RUN_ID"
ENV_ATTEMPT = "OPENGU_AUTOREPORT_ATTEMPT"
ENV_CONFIG_FINGERPRINT = "OPENGU_AUTOREPORT_CONFIG_FINGERPRINT"
ENV_GIT_SHA = "OPENGU_AUTOREPORT_GIT_SHA"
ENV_IDENTITY_JSON = "OPENGU_AUTOREPORT_IDENTITY_JSON"


class EventValidationError(ValueError):
    """Raised when an AutoReport event violates the V3 contract."""


class EventStreamCorruptionError(RuntimeError):
    """Raised when an existing audit stream cannot be trusted for append."""


@dataclass(frozen=True)
class AppendResult:
    event_id: str
    dedup_key: str
    written: bool
    path: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _digest(value: Any, length: int = 24) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()[:length]


def _normalize_scalar(value: Any) -> Any:
    if isinstance(value, float):
        return format(value, ".12g")
    if value is None or isinstance(value, (str, int, bool)):
        return value
    return str(value)


def normalize_identity(identity: Mapping[str, Any]) -> Dict[str, Any]:
    required = ("dataset", "model", "method", "ratio")
    missing = [key for key in required if identity.get(key) in (None, "")]
    if missing:
        raise EventValidationError("identity missing required fields: {0}".format(", ".join(missing)))
    normalized = {key: _normalize_scalar(value) for key, value in identity.items()}
    for optional in ("strategy", "seed", "k"):
        normalized.setdefault(optional, None)
    return dict(sorted(normalized.items()))


def make_cell_id(identity: Mapping[str, Any]) -> str:
    """Return a stable ID for matrix coordinates, independent of attempts/git."""
    return "cell_" + _digest(normalize_identity(identity), length=20)


def make_config_fingerprint(config: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(config).encode("utf-8")).hexdigest()[:16]


def new_run_id(cell_id: str) -> str:
    if not str(cell_id).startswith("cell_"):
        raise EventValidationError("run_id requires a valid cell_id")
    nonce = "{0}:{1}:{2}:{3}".format(cell_id, _utc_now(), os.getpid(), uuid.uuid4().hex)
    return "run_" + hashlib.sha256(nonce.encode("utf-8")).hexdigest()[:24]


def current_git_sha() -> str:
    env_sha = os.environ.get(ENV_GIT_SHA)
    if env_sha:
        return env_sha
    try:
        output = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return output.decode("utf-8", errors="replace").strip() or "unknown"
    except Exception:
        return "unknown"


def event_path_from_env(event_path: Optional[os.PathLike] = None) -> Path:
    return Path(event_path or os.environ.get(ENV_EVENT_PATH) or DEFAULT_EVENT_PATH).resolve()


def status_paths_from_env(
    status_md_path: Optional[os.PathLike] = None,
    status_html_path: Optional[os.PathLike] = None,
) -> Tuple[Path, Path]:
    md_path = Path(
        status_md_path or os.environ.get(ENV_STATUS_MD_PATH) or DEFAULT_STATUS_MD_PATH
    ).resolve()
    html_path = Path(
        status_html_path or os.environ.get(ENV_STATUS_HTML_PATH) or DEFAULT_STATUS_HTML_PATH
    ).resolve()
    return md_path, html_path


def artifact_ref(
    *,
    path: Optional[os.PathLike] = None,
    artifact_id: Optional[str] = None,
    artifact_type: Optional[str] = None,
    recipe_hash: Optional[str] = None,
    content_hash: Optional[str] = None,
    size_bytes: Optional[int] = None,
    mtime_ns: Optional[int] = None,
) -> Dict[str, Any]:
    if path is None and artifact_id is None:
        raise EventValidationError("artifact requires path or artifact_id")
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "recipe_hash": recipe_hash,
        "content_hash": content_hash,
        "size_bytes": size_bytes,
        "mtime_ns": mtime_ns,
        "path": None if path is None else str(path),
    }


def cache_observation(
    *,
    cache_type: str,
    outcome: str,
    recipe: Optional[Mapping[str, Any]] = None,
    recipe_hash: Optional[str] = None,
    artifact: Optional[Mapping[str, Any]] = None,
    hit_source: Optional[str] = None,
    lookup_policy: Optional[str] = None,
    authoritative: Optional[bool] = None,
    write_outcome: str = "unknown",
    miss_reason: Optional[str] = None,
) -> Dict[str, Any]:
    if cache_type not in CACHE_TYPES:
        raise EventValidationError("unknown cache type: {0}".format(cache_type))
    if outcome not in CACHE_OUTCOMES:
        raise EventValidationError("unknown cache outcome: {0}".format(outcome))
    if write_outcome not in WRITE_OUTCOMES:
        raise EventValidationError("unknown cache write outcome: {0}".format(write_outcome))
    if outcome == "hit" and not hit_source:
        raise EventValidationError("cache hit requires hit_source")
    if outcome == "hit" and not lookup_policy:
        raise EventValidationError("cache hit requires lookup_policy")
    if outcome == "hit" and not isinstance(authoritative, bool):
        raise EventValidationError("cache hit requires explicit authoritative=true/false")
    if outcome == "hit" and recipe is None and not recipe_hash:
        raise EventValidationError("cache hit requires recipe or recipe_hash")
    return {
        "type": cache_type,
        "outcome": outcome,
        "recipe": None if recipe is None else dict(recipe),
        "recipe_hash": recipe_hash,
        "artifact": None if artifact is None else dict(artifact),
        "hit_source": hit_source,
        "lookup_policy": lookup_policy,
        "authoritative": authoritative,
        "write_outcome": write_outcome,
        "miss_reason": miss_reason,
    }


def read_event_stream(event_path: Optional[os.PathLike] = None) -> Tuple[List[Dict[str, Any]], List[str]]:
    path = event_path_from_env(event_path)
    events: List[Dict[str, Any]] = []
    warnings: List[str] = []
    if not path.exists():
        return events, warnings
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return events, ["could not read {0}: {1}".format(path, exc)]
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            warnings.append("line {0}: invalid JSON ({1})".format(line_number, exc.msg))
            continue
        if not isinstance(event, dict):
            warnings.append("line {0}: event is not an object".format(line_number))
            continue
        if event.get("schema") != EVENT_SCHEMA or event.get("schema_version") != EVENT_SCHEMA_VERSION:
            warnings.append("line {0}: unsupported schema".format(line_number))
            continue
        events.append(event)
    return events, warnings


def _dedup_payload(event: Mapping[str, Any]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "cell_id": event["cell_id"],
        "stage": event["stage"],
        "state": event["state"],
        "config_fingerprint": event["config_fingerprint"],
    }
    semantic_cache_reuse = (
        (event.get("metadata") or {}).get("dedup_scope") == "semantic_cache_reuse"
    )
    if event["state"] == "skipped" or semantic_cache_reuse:
        # Repeated complete-cell/cache skips stay quiet until the cache/artifact
        # identity changes. Standalone producers may opt cache-only terminal
        # stages into the same semantic compression without hiding real runner
        # attempts, which retain their per-run transition history.
        payload["cache"] = event.get("cache") or []
        payload["artifacts"] = event.get("artifacts") or []
        payload["reason"] = (event.get("metadata") or {}).get("reason")
        payload["dedup_scope"] = (event.get("metadata") or {}).get("dedup_scope")
    else:
        payload["run_id"] = event["run_id"]
        payload["attempt"] = event["attempt"]
    return payload


def _validate_event(event: Mapping[str, Any]) -> None:
    if event.get("schema") != EVENT_SCHEMA or event.get("schema_version") != EVENT_SCHEMA_VERSION:
        raise EventValidationError("invalid AutoReport schema")
    if event.get("stage") not in STAGES:
        raise EventValidationError("invalid stage: {0}".format(event.get("stage")))
    if event.get("state") not in STATES:
        raise EventValidationError("invalid state: {0}".format(event.get("state")))
    if event.get("event_type") != "{0}.{1}".format(event.get("stage"), event.get("state")):
        raise EventValidationError("event_type does not match stage/state")
    if not isinstance(event.get("attempt"), int) or int(event["attempt"]) < 1:
        raise EventValidationError("attempt must be a positive integer")
    if event.get("state") == "failed":
        error = event.get("error")
        if not isinstance(error, Mapping) or not error.get("type") or not error.get("message"):
            raise EventValidationError("failed event requires error.type and error.message")
    if event.get("state") == "retrying":
        retry = event.get("retry")
        if (
            not isinstance(retry, Mapping)
            or event["attempt"] < 2
            or retry.get("attempt") != event.get("attempt")
            or not str(retry.get("retry_of") or "").startswith("run_")
        ):
            raise EventValidationError(
                "retrying event requires attempt>=2 and a matching retry.retry_of run_id"
            )
    if not str(event.get("cell_id", "")).startswith("cell_"):
        raise EventValidationError("invalid cell_id")
    if not str(event.get("run_id", "")).startswith("run_"):
        raise EventValidationError("invalid run_id")
    identity = normalize_identity(event.get("identity") or {})
    if event.get("cell_id") != make_cell_id(identity):
        raise EventValidationError("cell_id does not match normalized identity")
    if not event.get("config_fingerprint"):
        raise EventValidationError("config_fingerprint is required")
    if not event.get("git_sha"):
        raise EventValidationError("git_sha is required")
    producer = event.get("producer")
    if not isinstance(producer, Mapping) or not producer.get("script"):
        raise EventValidationError("producer.script is required")
    for observation in event.get("cache") or []:
        cache_observation(
            cache_type=observation.get("type"),
            outcome=observation.get("outcome"),
            recipe=observation.get("recipe"),
            recipe_hash=observation.get("recipe_hash"),
            artifact=observation.get("artifact"),
            hit_source=observation.get("hit_source"),
            lookup_policy=observation.get("lookup_policy"),
            authoritative=observation.get("authoritative"),
            write_outcome=observation.get("write_outcome", "unknown"),
            miss_reason=observation.get("miss_reason"),
        )
    expected_dedup_key = "dedup_" + _digest(_dedup_payload(event), length=32)
    if event.get("dedup_key") != expected_dedup_key:
        raise EventValidationError("dedup_key does not match event content")
    expected_event_id = "evt_" + _digest({"dedup_key": expected_dedup_key}, length=24)
    if event.get("event_id") != expected_event_id:
        raise EventValidationError("event_id does not match dedup_key")


def build_event(
    *,
    identity: Mapping[str, Any],
    stage: str,
    state: str,
    producer: str,
    config_fingerprint: str,
    git_sha: Optional[str] = None,
    cell_id: Optional[str] = None,
    run_id: Optional[str] = None,
    attempt: int = 1,
    cache: Optional[Sequence[Mapping[str, Any]]] = None,
    artifacts: Optional[Sequence[Mapping[str, Any]]] = None,
    metrics: Optional[Mapping[str, Any]] = None,
    error: Optional[Mapping[str, Any]] = None,
    retry: Optional[Mapping[str, Any]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    identity_value = normalize_identity(identity)
    cell_id_value = cell_id or make_cell_id(identity_value)
    run_id_value = run_id or new_run_id(cell_id_value)
    event: Dict[str, Any] = {
        "schema": EVENT_SCHEMA,
        "schema_version": EVENT_SCHEMA_VERSION,
        "event_id": None,
        "dedup_key": None,
        "event_type": "{0}.{1}".format(stage, state),
        "timestamp": timestamp or _utc_now(),
        "producer": {"script": producer, "host": socket.gethostname()},
        "cell_id": cell_id_value,
        "run_id": run_id_value,
        "attempt": int(attempt),
        "stage": stage,
        "state": state,
        "identity": identity_value,
        "git_sha": git_sha or current_git_sha(),
        "config_fingerprint": str(config_fingerprint),
        "cache": [dict(item) for item in (cache or [])],
        "artifacts": [dict(item) for item in (artifacts or [])],
        "metrics": dict(metrics or {}),
        "error": None if error is None else dict(error),
        "retry": None if retry is None else dict(retry),
        "metadata": dict(metadata or {}),
    }
    dedup_key = "dedup_" + _digest(_dedup_payload(event), length=32)
    event["dedup_key"] = dedup_key
    event["event_id"] = "evt_" + _digest({"dedup_key": dedup_key}, length=24)
    _validate_event(event)
    return event


@contextmanager
def _exclusive_lock(path: Path, timeout_s: float = 10.0, stale_after_s: float = 120.0):
    lock_path = path.with_name(path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_s
    fd: Optional[int] = None
    while fd is None:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, "{0} {1}\n".format(os.getpid(), _utc_now()).encode("utf-8"))
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > stale_after_s:
                    lock_path.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise TimeoutError("timed out waiting for AutoReport lock: {0}".format(lock_path))
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def _check_transition_conflict(events: Iterable[Mapping[str, Any]], event: Mapping[str, Any]) -> None:
    if event["state"] not in TERMINAL_STATES:
        return
    for existing in events:
        if (
            existing.get("cell_id") == event["cell_id"]
            and existing.get("run_id") == event["run_id"]
            and existing.get("stage") == event["stage"]
            and existing.get("state") in TERMINAL_STATES
            and existing.get("state") != event["state"]
        ):
            raise EventValidationError(
                "conflicting terminal transition for {0}/{1}: {2} -> {3}".format(
                    event["run_id"], event["stage"], existing.get("state"), event["state"]
                )
            )


def append_event(
    event: Mapping[str, Any],
    *,
    event_path: Optional[os.PathLike] = None,
    refresh: bool = True,
    status_md_path: Optional[os.PathLike] = None,
    status_html_path: Optional[os.PathLike] = None,
) -> AppendResult:
    event_value = dict(event)
    _validate_event(event_value)
    path = event_path_from_env(event_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    written = False
    with _exclusive_lock(path):
        existing, stream_warnings = read_event_stream(path)
        integrity_errors = []
        for index, existing_event in enumerate(existing, 1):
            try:
                _validate_event(existing_event)
            except EventValidationError as exc:
                integrity_errors.append("event {0}: {1}".format(index, exc))
        if stream_warnings or integrity_errors:
            details = "; ".join((stream_warnings + integrity_errors)[:5])
            raise EventStreamCorruptionError(
                "refusing to append to an untrusted AutoReport stream: {0}".format(details)
            )
        if not any(item.get("dedup_key") == event_value["dedup_key"] for item in existing):
            _check_transition_conflict(existing, event_value)
            prefix = ""
            if path.exists() and path.stat().st_size:
                with path.open("rb") as existing_file:
                    existing_file.seek(-1, os.SEEK_END)
                    if existing_file.read(1) not in (b"\n", b"\r"):
                        prefix = "\n"
            line = prefix + _canonical_json(event_value) + "\n"
            with path.open("a", encoding="utf-8", newline="\n") as file_obj:
                file_obj.write(line)
                file_obj.flush()
                os.fsync(file_obj.fileno())
            written = True
        if refresh:
            refresh_status_views(
                event_path=path,
                status_md_path=status_md_path,
                status_html_path=status_html_path,
                acquire_lock=False,
            )
    return AppendResult(
        event_id=str(event_value["event_id"]),
        dedup_key=str(event_value["dedup_key"]),
        written=written,
        path=str(path),
    )


def record_event(
    *,
    identity: Mapping[str, Any],
    stage: str,
    state: str,
    producer: str,
    config_fingerprint: str,
    git_sha: Optional[str] = None,
    cell_id: Optional[str] = None,
    run_id: Optional[str] = None,
    attempt: int = 1,
    cache: Optional[Sequence[Mapping[str, Any]]] = None,
    artifacts: Optional[Sequence[Mapping[str, Any]]] = None,
    metrics: Optional[Mapping[str, Any]] = None,
    error: Optional[Mapping[str, Any]] = None,
    retry: Optional[Mapping[str, Any]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    event_path: Optional[os.PathLike] = None,
    refresh: bool = True,
    status_md_path: Optional[os.PathLike] = None,
    status_html_path: Optional[os.PathLike] = None,
) -> AppendResult:
    event = build_event(
        identity=identity,
        stage=stage,
        state=state,
        producer=producer,
        config_fingerprint=config_fingerprint,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        cache=cache,
        artifacts=artifacts,
        metrics=metrics,
        error=error,
        retry=retry,
        metadata=metadata,
    )
    return append_event(
        event,
        event_path=event_path,
        refresh=refresh,
        status_md_path=status_md_path,
        status_html_path=status_html_path,
    )


def prior_attempt_context(
    cell_id: str,
    config_fingerprint: str,
    event_path: Optional[os.PathLike] = None,
) -> Tuple[int, Optional[str]]:
    """Return ``(next_attempt, latest_failed_run_id)`` for a real execution."""
    events, _warnings = read_event_stream(event_path)
    starts = [
        event
        for event in events
        if event.get("cell_id") == cell_id
        and event.get("config_fingerprint") == config_fingerprint
        and event.get("stage") == "run"
        and event.get("state") == "started"
    ]
    failed = [
        event
        for event in events
        if event.get("cell_id") == cell_id
        and event.get("config_fingerprint") == config_fingerprint
        and event.get("stage") == "run"
        and event.get("state") == "failed"
    ]
    latest_failed = failed[-1].get("run_id") if failed else None
    return len(starts) + 1, latest_failed


def refresh_status_views(
    *,
    event_path: Optional[os.PathLike] = None,
    status_md_path: Optional[os.PathLike] = None,
    status_html_path: Optional[os.PathLike] = None,
    max_cells: int = 200,
    acquire_lock: bool = True,
) -> Tuple[str, str]:
    # Local import avoids a module cycle: summary reads the event stream.
    from .summary import write_status_views

    resolved_event_path = event_path_from_env(event_path)
    if status_md_path is None and not os.environ.get(ENV_STATUS_MD_PATH):
        status_md_path = resolved_event_path.parent / "auto_report.md"
    if status_html_path is None and not os.environ.get(ENV_STATUS_HTML_PATH):
        status_html_path = resolved_event_path.parent / "auto_report.html"
    md_path, html_path = status_paths_from_env(status_md_path, status_html_path)
    def _write() -> Tuple[str, str]:
        return write_status_views(
            event_path=resolved_event_path,
            markdown_path=md_path,
            html_path=html_path,
            max_cells=max_cells,
        )

    if not acquire_lock:
        return _write()
    resolved_event_path.parent.mkdir(parents=True, exist_ok=True)
    with _exclusive_lock(resolved_event_path):
        return _write()
