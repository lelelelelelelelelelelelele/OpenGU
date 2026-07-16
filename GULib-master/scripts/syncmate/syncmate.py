#!/usr/bin/env python
"""Device-local status and incremental result collection for multi-node work.

Syncmate is intentionally small: it reads the untracked .syncmate/device.yaml
file, scans local artifacts, and prints safe next-step commands for humans or
AI agents. Its executable automation path is result-only collection:
collectors can diff a remote manifest, pull missing selected artifacts, and
verify local landings with SHA-256.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import html
import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import webbrowser
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - friendly CLI failure
    yaml = None


REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_DIR = REPO_ROOT / ".syncmate"
DEFAULT_DEVICE_FILE = SYNC_DIR / "device.yaml"
STATE_FILE = SYNC_DIR / "state.json"
STATUS_HTML = SYNC_DIR / "status.html"
RESULTS_RUNS = REPO_ROOT / "results" / "runs"
LOG_DIR_NAME = "log"
ARTIFACT_NAMES = ("attack.json", "collateral.json", "_meta.json")
BUNDLE_MANIFEST_NAME = "syncmate_bundle.json"
HANDOFF_PACK_MANIFEST_NAME = "syncmate_handoff_pack.json"
STRATEGY_NAMES = ("random", "degree", "pagerank", "tracin", "im", "hybrid")
RUNS_PREFIX = ("results", "runs")
ROLE_CHOICES = ("collector", "runner", "runner+collector")
TRANSPORT_CHOICES = ("ssh", "local")
LOCAL_SSH_SENTINEL = "__syncmate_local__"
REPORT_STALE_HOURS = 24
LOG_TEXT_SUFFIXES = (".log", ".txt", ".out", ".err")
LOG_ERROR_KEYWORDS = (
    "traceback",
    "runtimeerror",
    "cuda out of memory",
    "outofmemory",
    "oom",
    "exception",
    "killed",
    "failed",
)
QUEUE_PROTOCOL = "syncmate-runner-queue/v1"
QUEUE_STATES = ("inbox", "running", "done", "failed", "blocked")
QUEUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
RUNNER_AGENT_MIN_POLL_SECONDS = 1.0
RUNNER_AGENT_MAX_POLL_SECONDS = 60.0
RUNNER_AGENT_MAX_TIMEOUT_SECONDS = 3600
RUNNER_RECIPE_BASE_SHA = "a177e2c3bdf2a5a152c0e7be9fa5385c9b462b2a"
RUNNER_RECIPE_ALLOWED_TOOL_DELTA = (
    "GULib-master/scripts/syncmate/",
    "GULib-master/tests/test_syncmate.py",
    "GULib-master/docs/syncmate_bounded_runner_agent_ACCEPTANCE_REPORT.",
)
GATE4_RECIPE_BASE_SHA = "dbe79efd8fd70a9a455a8055a6627bd0bd95ed0e"
GATE4_RECIPE_ALLOWED_DELTA = (
    "GULib-master/attack/pipeline_adapter.py",
    "GULib-master/config.py",
    "GULib-master/dataset/original_dataset.py",
    "GULib-master/experiments/run.py",
    "GULib-master/experiments/configs/cache_v2_gate4_cora_degree_canary.yaml",
    "GULib-master/experiments/processed_provider.py",
    "GULib-master/parameter_parser.py",
    "GULib-master/scripts/cache_v2_gate4_canary.py",
    "GULib-master/scripts/syncmate/syncmate.py",
    "GULib-master/tests/test_auto_report_v3.py",
    "GULib-master/tests/test_cache_v2_gate4_canary.py",
    "GULib-master/tests/test_demo.py",
    "GULib-master/tests/test_experiment_processed_provider.py",
    "GULib-master/tests/test_phase_b_invariants.py",
    "GULib-master/tests/test_syncmate.py",
    "GULib-master/utils/dataset_utils.py",
    "GULib-master/utils/logger.py",
)
RUNNER_RECIPE_DEFINITIONS = {
    "smoke": {
        "id": "smoke",
        "argv": ("{python}", "scripts/syncmate/syncmate.py", "smoke", "--json"),
        "config_path": "scripts/syncmate/setup.example.yaml",
        "config_sha256": "34f0ad2d462d6575a285760ddfd45f17f01672c1342881a7719b27ed8efafa56",
        "expected_git_sha": RUNNER_RECIPE_BASE_SHA,
        "timeout_seconds": 180,
        "expected_artifact_paths": (),
        "success_predicate": "json.passed == true",
        "collector_acceptance": False,
    },
    "opengu-preflight-v1": {
        "id": "opengu-preflight-v1",
        "argv": (
            "{python}", "scripts/syncmate/syncmate.py", "runner-preflight",
            "--recipe", "opengu-preflight-v1", "--json",
        ),
        "config_path": "experiments/configs/phase_b_cora_gcn.yaml",
        "config_sha256": "8c31c6c05aa3737cab457a0ae0a6937d4c99c30499b5f54b620c500a0c967c2e",
        "expected_git_sha": RUNNER_RECIPE_BASE_SHA,
        "timeout_seconds": 180,
        "expected_artifact_paths": (
            "results/runs/__syncmate_preflight__/opengu_preflight/seed0/attack.json",
            "results/runs/__syncmate_preflight__/opengu_preflight/seed0/collateral.json",
            "results/runs/__syncmate_preflight__/opengu_preflight/seed0/_meta.json",
        ),
        "success_predicate": "json.passed == true and generated_artifacts == expected_artifact_paths",
        "collector_acceptance": True,
    },
    "opengu-cache-v2-gate4-v1": {
        "id": "opengu-cache-v2-gate4-v1",
        "argv": (
            "{python}", "-m", "scripts.cache_v2_gate4_canary", "--json",
        ),
        "config_path": "experiments/configs/cache_v2_gate4_cora_degree_canary.yaml",
        "config_sha256": "45f587853aee6a91e85efd82ee40350435969a7b51b9539062762ae06b875980",
        "expected_git_sha": GATE4_RECIPE_BASE_SHA,
        "allowed_git_delta_paths": GATE4_RECIPE_ALLOWED_DELTA,
        "timeout_seconds": 3600,
        "expected_artifact_paths": (
            "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/attack.json",
            "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/collateral.json",
            "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/predictions.npz",
            "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/_meta.json",
        ),
        "success_predicate": "json.passed == true and collector gate passes for the exact result leaf",
        "collector_acceptance": True,
    },
}
QUEUE_ALLOWED_RECIPES = tuple(RUNNER_RECIPE_DEFINITIONS)
QUEUE_ALLOWED_JOB_FIELDS = {
    "protocol", "version", "id", "recipe", "created_at", "requested_by", "note",
}


def artifact_index_file() -> Path:
    return SYNC_DIR / "artifact_index.json"


def export_manifest_file() -> Path:
    return SYNC_DIR / "export_manifest.json"


def export_csv_file() -> Path:
    return SYNC_DIR / "export_manifest.csv"


def results_table_file() -> Path:
    return SYNC_DIR / "results_table.json"


def results_csv_file() -> Path:
    return SYNC_DIR / "results_table.csv"


def history_file() -> Path:
    return SYNC_DIR / "history.jsonl"


def brief_file() -> Path:
    return SYNC_DIR / "brief.md"


def checklist_file() -> Path:
    return SYNC_DIR / "checklist.md"


def runbook_file() -> Path:
    return SYNC_DIR / "runbook.md"


def workflow_file() -> Path:
    return SYNC_DIR / "workflow.json"


def automation_core_file() -> Path:
    return SYNC_DIR / "automation_core.json"


def automation_core_markdown_file() -> Path:
    return SYNC_DIR / "automation_core.md"


def acceptance_file() -> Path:
    return SYNC_DIR / "acceptance.json"


def action_plan_file() -> Path:
    return SYNC_DIR / "action_plan.json"


def action_plan_markdown_file() -> Path:
    return SYNC_DIR / "action_plan.md"


def setup_plan_file() -> Path:
    return SYNC_DIR / "setup_plan.md"


def last_preflight_file() -> Path:
    return SYNC_DIR / "last_preflight.json"


def safe_file_stem(value: Any) -> str:
    text = str(value or "").strip()
    return "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in text) or "all"


def receipt_file(node_id: Optional[str] = None) -> Path:
    if node_id:
        return SYNC_DIR / f"receipt_{safe_file_stem(node_id)}.md"
    return SYNC_DIR / "receipt.md"


def publish_file(device_id: Optional[str] = None) -> Path:
    if device_id:
        return SYNC_DIR / f"publish_{safe_file_stem(device_id)}.json"
    return SYNC_DIR / "publish.json"


def bundle_file(device_id: Optional[str] = None) -> Path:
    if device_id:
        return SYNC_DIR / f"bundle_{safe_file_stem(device_id)}.zip"
    return SYNC_DIR / "bundle.zip"


def handoff_pack_file(device_id: Optional[str] = None) -> Path:
    if device_id:
        return SYNC_DIR / f"handoff_pack_{safe_file_stem(device_id)}.zip"
    return SYNC_DIR / "handoff_pack.zip"


def log_root(repo_root: Optional[Path] = None) -> Path:
    return (repo_root or REPO_ROOT) / LOG_DIR_NAME


def now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def parse_iso_time(value: Any) -> Optional[_dt.datetime]:
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        return _dt.datetime.fromisoformat(text)
    except ValueError:
        return None


def report_age_hours(generated_at: Any, now_value: Optional[str] = None) -> Optional[float]:
    ts = parse_iso_time(generated_at)
    now_ts = parse_iso_time(now_value or now_iso())
    if ts is None or now_ts is None:
        return None
    if ts.tzinfo is not None and now_ts.tzinfo is None:
        now_ts = now_ts.replace(tzinfo=ts.tzinfo)
    if ts.tzinfo is None and now_ts.tzinfo is not None:
        ts = ts.replace(tzinfo=now_ts.tzinfo)
    return max((now_ts - ts).total_seconds() / 3600, 0.0)


def is_report_stale(generated_at: Any, *, stale_hours: int = REPORT_STALE_HOURS) -> bool:
    age = report_age_hours(generated_at)
    return age is None or age > stale_hours


def format_age(generated_at: Any) -> str:
    age = report_age_hours(generated_at)
    if age is None:
        return "unknown"
    if age < 1:
        return f"{int(age * 60)}m"
    if age < 48:
        return f"{age:.1f}h"
    return f"{age / 24:.1f}d"


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def run_git_at(repo_root: Path, args: List[str]) -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo_root), *args],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8", errors="replace").strip()
    except Exception:
        return "unknown"


def run_git(args: List[str]) -> str:
    return run_git_at(REPO_ROOT, args)


def git_state_for_root(repo_root: Path) -> Dict[str, Any]:
    status = run_git_at(repo_root, ["status", "--short"])
    return {
        "branch": run_git_at(repo_root, ["branch", "--show-current"]),
        "sha": run_git_at(repo_root, ["rev-parse", "HEAD"]),
        "short_sha": run_git_at(repo_root, ["rev-parse", "--short", "HEAD"]),
        "dirty": bool(status.strip()) if status != "unknown" else None,
        "status_short": status.splitlines() if status and status != "unknown" else [],
    }


def git_state() -> Dict[str, Any]:
    return git_state_for_root(REPO_ROOT)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_artifact_names(names: Any, *, allow_empty: bool = False) -> List[str]:
    if names is None:
        return []
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise SystemExit("artifact policy include/exclude must be a list of file names")
    normalized = []
    seen = set()
    for name in names:
        value = name.strip()
        if not value:
            continue
        if "/" in value or "\\" in value or value in (".", ".."):
            raise SystemExit(f"artifact policy entries must be file names, got: {name!r}")
        if value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    if not normalized and not allow_empty:
        raise SystemExit("artifact policy include must contain at least one file name")
    return normalized


def apply_artifact_policy(base: List[str], policy: Any) -> List[str]:
    names = list(base)
    if policy is None:
        return names
    if not isinstance(policy, dict):
        raise SystemExit("artifact_policy must be a mapping")
    if "include" in policy:
        names = normalize_artifact_names(policy.get("include"))
    if "exclude" in policy:
        excluded = set(normalize_artifact_names(policy.get("exclude"), allow_empty=True))
        names = [name for name in names if name not in excluded]
    if not names:
        raise SystemExit("artifact policy resolved to an empty include set")
    return names


def artifact_names_for_peer(device: Optional[Dict[str, Any]] = None,
                            peer: Optional[Dict[str, Any]] = None) -> Tuple[str, ...]:
    names = list(ARTIFACT_NAMES)
    if device:
        names = apply_artifact_policy(names, device.get("artifact_policy"))
    if peer:
        names = apply_artifact_policy(names, peer.get("artifact_policy"))
    return tuple(names)


def artifact_policy_payload(artifact_names: Optional[Tuple[str, ...]] = None) -> Dict[str, Any]:
    names = ARTIFACT_NAMES if artifact_names is None else artifact_names
    return {"include": list(names)}


def normalize_transport(value: Any) -> str:
    transport = str(value or "ssh").strip().lower()
    if transport not in TRANSPORT_CHOICES:
        raise SystemExit(f"transport must be one of: {', '.join(TRANSPORT_CHOICES)}")
    return transport


def peer_transport(peer: Optional[Dict[str, Any]]) -> str:
    return normalize_transport((peer or {}).get("transport") or "ssh")


def peer_uses_local_transport(peer: Optional[Dict[str, Any]]) -> bool:
    return peer_transport(peer) == "local"


def transport_ssh_value(peer: Optional[Dict[str, Any]]) -> str:
    if peer_uses_local_transport(peer):
        return LOCAL_SSH_SENTINEL
    return str((peer or {}).get("ssh") or "")


def peer_python_executable(peer: Optional[Dict[str, Any]]) -> str:
    value = (peer or {}).get("python_executable")
    if value is None:
        return "python"
    if not isinstance(value, str) or not value.strip():
        raise SystemExit("peer python_executable must be a non-empty string")
    return value.strip()


def peer_python_kwargs(peer: Optional[Dict[str, Any]]) -> Dict[str, str]:
    python_executable = peer_python_executable(peer)
    if python_executable == "python":
        return {}
    return {"python_executable": python_executable}


def is_local_transport_ref(value: Any) -> bool:
    return str(value or "") == LOCAL_SSH_SENTINEL


def transport_payload(ssh: str) -> Dict[str, Any]:
    if is_local_transport_ref(ssh):
        return {"transport": "local", "ssh": None}
    return {"transport": "ssh", "ssh": ssh}


def resolve_local_repo_root(repo_path: str) -> Path:
    path = Path(repo_path).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def flatten_cli_values(values: Optional[List[List[str]]]) -> List[str]:
    if not values:
        return []
    return [item for group in values for item in group]


def artifact_policy_from_cli(include: Optional[List[List[str]]] = None,
                             exclude: Optional[List[List[str]]] = None) -> Optional[Dict[str, Any]]:
    include_names = normalize_artifact_names(flatten_cli_values(include), allow_empty=True)
    exclude_names = normalize_artifact_names(flatten_cli_values(exclude), allow_empty=True)
    if not include_names and not exclude_names:
        return None
    policy: Dict[str, Any] = {}
    if include_names:
        policy["include"] = include_names
    if exclude_names:
        policy["exclude"] = exclude_names
    apply_artifact_policy(list(ARTIFACT_NAMES), policy)
    return policy


def is_artifact(path: Path, artifact_names: Optional[Tuple[str, ...]] = None) -> bool:
    return path.name in (artifact_names or ARTIFACT_NAMES)


def manifest_for_roots(roots: List[str], artifact_names: Optional[Tuple[str, ...]] = None,
                       *, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    names = artifact_names or ARTIFACT_NAMES
    base = (repo_root or REPO_ROOT).resolve()
    items = []
    for root_s in roots:
        root = (base / root_s).resolve()
        try:
            root.relative_to(base)
        except ValueError:
            continue
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or not is_artifact(path, names):
                continue
            try:
                rel_path = path.relative_to(base).as_posix()
            except ValueError:
                continue
            stat = path.stat()
            items.append({
                "path": rel_path,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "sha256": sha256_file(path),
            })
    inventory = manifest_inventory_from_items(items, names)
    return {
        "generated_at": now_iso(),
        "repo_root": str(base),
        "git": git_state_for_root(base),
        "roots": roots,
        "artifact_policy": artifact_policy_payload(names),
        "inventory": inventory,
        "items": items,
        "count": len(items),
    }


def manifest_inventory_from_items(items: List[Dict[str, Any]],
                                  artifact_names: Optional[Tuple[str, ...]] = None) -> Dict[str, Any]:
    expected = tuple(artifact_names or ARTIFACT_NAMES)
    leaves: Dict[str, Any] = {}
    for item in items or []:
        if not isinstance(item, dict):
            continue
        remote_path = str(item.get("path") or "")
        if not remote_path:
            continue
        artifact_name = Path(remote_path).name
        remote_leaf = str(Path(remote_path).parent).replace("\\", "/")
        leaf = leaves.setdefault(remote_leaf, {
            "remote_leaf": remote_leaf,
            "cell": "unknown",
            "method_strategy": "unknown",
            "seed": "unknown",
            "layout": "unknown",
            "artifacts": [],
            "missing": [],
            "complete": False,
        })
        _node, cell, method_strategy, seed, layout = classify_repo_leaf_path(remote_path)
        leaf.update({
            "cell": cell,
            "method_strategy": method_strategy,
            "seed": seed,
            "layout": layout,
        })
        if artifact_name and artifact_name not in leaf["artifacts"]:
            leaf["artifacts"].append(artifact_name)

    leaf_values = []
    for leaf in leaves.values():
        artifacts = sorted(leaf["artifacts"])
        missing = [name for name in expected if name not in artifacts]
        leaf["artifacts"] = artifacts
        leaf["missing"] = missing
        leaf["complete"] = not missing
        leaf_values.append(leaf)

    leaf_values.sort(key=lambda item: item["remote_leaf"])
    return {
        "summary": {
            "leaves": len(leaf_values),
            "complete": sum(1 for item in leaf_values if item["complete"]),
            "incomplete": sum(1 for item in leaf_values if not item["complete"]),
            "artifacts": sum(len(item["artifacts"]) for item in leaf_values),
            "expected_artifacts": list(expected),
        },
        "leaves": leaf_values,
    }


def load_device(path: Path) -> Tuple[Dict[str, Any], List[str]]:
    warnings: List[str] = []
    if yaml is None:
        raise SystemExit("PyYAML is required. Use the project gnn environment or install pyyaml.")

    if not path.exists():
        warnings.append(f"device setup missing: {rel(path)}")
        return {
            "version": 0,
            "device_id": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "unknown",
            "role": "unknown",
            "repo_path": str(REPO_ROOT),
            "peers": {},
        }, warnings

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid setup file: {path}")

    data.setdefault("version", 0)
    data.setdefault("device_id", "unknown")
    data.setdefault("role", "unknown")
    data.setdefault("repo_path", str(REPO_ROOT))
    data.setdefault("peers", {})
    if not isinstance(data.get("peers"), dict):
        raise SystemExit("device.yaml field 'peers' must be a mapping")
    return data, warnings


def classify_leaf(seed_dir: Path, results_runs: Optional[Path] = None) -> Tuple[str, str, str, str, str]:
    """Return node_id, cell, method_strategy, seed, layout for an artifact leaf."""
    runs_root = results_runs or RESULTS_RUNS
    try:
        parts = seed_dir.relative_to(runs_root).parts
    except ValueError:
        return "outside", "unknown", "unknown", seed_dir.name, "outside"

    if len(parts) < 3:
        return "unknown", "unknown", "unknown", seed_dir.name, "short"

    first = parts[0]
    if "_r" in first:
        return "bare", first, parts[1], parts[2], "bare"
    if len(parts) >= 6 and parts[1:3] == RUNS_PREFIX:
        return first, parts[3], parts[4], parts[5], "nested-results-wrapper"
    if len(parts) >= 4:
        return first, parts[1], parts[2], parts[3], "node"
    return first, "unknown", parts[-2], parts[-1], "unknown"


def classify_repo_leaf_path(local_path: Any) -> Tuple[str, str, str, str, str]:
    if not isinstance(local_path, str) or not local_path:
        return "unknown", "unknown", "unknown", "unknown", "unknown"
    parts = Path(local_path).parent.parts
    if len(parts) < 3 or tuple(parts[:2]) != RUNS_PREFIX:
        return "unknown", "unknown", "unknown", "unknown", "unknown"
    rel_parts = parts[2:]
    if len(rel_parts) < 3:
        return "unknown", "unknown", "unknown", rel_parts[-1] if rel_parts else "unknown", "short"
    first = rel_parts[0]
    if "_r" in first:
        return "bare", first, rel_parts[1], rel_parts[2], "bare"
    if len(rel_parts) >= 6 and tuple(rel_parts[1:3]) == RUNS_PREFIX:
        return first, rel_parts[3], rel_parts[4], rel_parts[5], "nested-results-wrapper"
    if len(rel_parts) >= 4:
        return first, rel_parts[1], rel_parts[2], rel_parts[3], "node"
    return first, "unknown", rel_parts[-2], rel_parts[-1], "unknown"


def artifact_leaf_dirs(results_runs: Optional[Path] = None,
                       artifact_names: Optional[Tuple[str, ...]] = None) -> List[Path]:
    runs_root = results_runs or RESULTS_RUNS
    names = artifact_names or ARTIFACT_NAMES
    if not runs_root.exists():
        return []
    leaves = set()
    for name in names:
        for p in runs_root.rglob(name):
            if p.is_file():
                leaves.add(p.parent)
    return sorted(leaves)


def read_meta(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def scan_results(*, repo_root: Optional[Path] = None,
                 results_runs: Optional[Path] = None,
                 artifact_names: Optional[Tuple[str, ...]] = None) -> Dict[str, Any]:
    base = repo_root or REPO_ROOT
    runs_root = results_runs or (RESULTS_RUNS if repo_root is None else base / "results" / "runs")
    names = artifact_names or ARTIFACT_NAMES
    nodes: Dict[str, Any] = defaultdict(lambda: {
        "leaves": 0,
        "files": Counter(),
        "missing": Counter(),
        "cells": Counter(),
        "git_shas": Counter(),
        "hosts": Counter(),
        "layouts": Counter(),
        "examples": [],
    })

    for leaf in artifact_leaf_dirs(runs_root, names):
        node, cell, _method_strategy, _seed, layout = classify_leaf(leaf, runs_root)
        info = nodes[node]
        info["leaves"] += 1
        info["cells"][cell] += 1
        info["layouts"][layout] += 1
        if len(info["examples"]) < 5:
            try:
                info["examples"].append(leaf.relative_to(base).as_posix())
            except ValueError:
                info["examples"].append(rel(leaf))

        for name in names:
            if (leaf / name).is_file():
                info["files"][name] += 1
            else:
                info["missing"][name] += 1

        meta = read_meta(leaf / "_meta.json")
        sha = (meta.get("git_sha") or "")[:7]
        host = meta.get("hostname") or ""
        if sha:
            info["git_shas"][sha] += 1
        if host:
            info["hosts"][host] += 1

    out_nodes = {}
    for node, info in sorted(nodes.items()):
        issues = []
        if info["missing"]:
            issues.append("missing-artifacts")
        if len(info["git_shas"]) > 1:
            issues.append("multiple-git-shas")
        if node == "bare":
            issues.append("bare-results-layout")
        if info["layouts"].get("nested-results-wrapper"):
            issues.append("nested-results-wrapper")
        out_nodes[node] = {
            "leaves": info["leaves"],
            "files": dict(info["files"]),
            "missing": dict(info["missing"]),
            "cells": dict(info["cells"]),
            "git_shas": dict(info["git_shas"]),
            "hosts": dict(info["hosts"]),
            "layouts": dict(info["layouts"]),
            "examples": info["examples"],
            "issues": issues,
        }
    return {
        "root": rel(runs_root) if base == REPO_ROOT else runs_root.relative_to(base).as_posix(),
        "nodes": out_nodes,
        "total_leaves": sum(n["leaves"] for n in out_nodes.values()),
    }


def iso_from_timestamp(timestamp: float) -> str:
    return _dt.datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()


def log_candidates(repo_root: Optional[Path] = None) -> List[Path]:
    root = log_root(repo_root)
    if not root.exists():
        return []
    return sorted(
        [
            path for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in LOG_TEXT_SUFFIXES
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def read_tail_text(path: Path, max_bytes: int = 8192) -> str:
    try:
        size = path.stat().st_size
        with path.open("rb") as fh:
            if size > max_bytes:
                fh.seek(-max_bytes, os.SEEK_END)
            data = fh.read(max_bytes)
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def last_nonempty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped[:500]
    return ""


def log_error_keywords(text: str) -> List[str]:
    lower = text.lower()
    return [keyword for keyword in LOG_ERROR_KEYWORDS if keyword in lower]


def compact_log_entry(path: Path, *, tail_bytes: int = 8192) -> Dict[str, Any]:
    stat = path.stat()
    tail = read_tail_text(path, tail_bytes)
    keywords = log_error_keywords(tail)
    return {
        "path": rel(path),
        "size": stat.st_size,
        "mtime": iso_from_timestamp(stat.st_mtime),
        "age": format_age(iso_from_timestamp(stat.st_mtime)),
        "status": "error" if keywords else "ok",
        "keywords": keywords,
        "last_line": last_nonempty_line(tail),
    }


def scan_progress(*, limit: int = 10, scan_limit: int = 200, tail_bytes: int = 8192,
                  repo_root: Optional[Path] = None) -> Dict[str, Any]:
    base = repo_root or REPO_ROOT
    root = log_root(base)
    files = log_candidates(base)
    scanned = [compact_log_entry(path, tail_bytes=tail_bytes) for path in files[:max(0, scan_limit)]]
    errors = [entry for entry in scanned if entry.get("status") == "error"]
    recent = scanned[:max(0, limit)]
    error_examples = errors[:max(0, limit)]
    newest = files[0] if files else None
    newest_mtime = iso_from_timestamp(newest.stat().st_mtime) if newest else None
    return {
        "root": rel(root) if base == REPO_ROOT else root.relative_to(base).as_posix(),
        "exists": root.exists(),
        "summary": {
            "total_log_files": len(files),
            "scanned_log_files": len(scanned),
            "shown_recent": len(recent),
            "error_logs": len(errors),
            "newest_mtime": newest_mtime,
            "newest_age": format_age(newest_mtime),
        },
        "recent_logs": recent,
        "error_logs": error_examples,
    }


def build_snapshot(device: Dict[str, Any], warnings: List[str]) -> Dict[str, Any]:
    peer_configs = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    snapshot = {
        "generated_at": now_iso(),
        "repo_root": str(REPO_ROOT),
        "device": {
            "id": device.get("device_id"),
            "role": device.get("role"),
            "repo_path": device.get("repo_path"),
            "setup_file": rel(DEFAULT_DEVICE_FILE),
            "setup_warnings": warnings,
            "artifact_policy": device.get("artifact_policy"),
            "peers": sorted(peer_configs.keys()),
            "peer_configs": peer_configs,
        },
        "git": git_state(),
        "results": scan_results(),
        "progress": scan_progress(),
        "remote_status": load_remote_status_reports(),
        "bundle_inspect_reports": load_bundle_inspect_reports(),
        "diff_reports": load_diff_reports(),
        "collect_reports": load_collect_reports(),
        "verify_reports": load_verify_reports(),
        "artifact_index": load_artifact_index(),
        "export_manifest": load_optional_json(export_manifest_file()),
        "results_table": load_optional_json(results_table_file()),
        "preflight": load_optional_json(last_preflight_file()),
    }
    snapshot["fingerprint"] = fingerprint_payload(snapshot)
    return snapshot


def ensure_sync_dir() -> None:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)


def history_entry_from_snapshot(snapshot: Dict[str, Any], event: str = "snapshot") -> Dict[str, Any]:
    results = snapshot.get("results") or {}
    progress = (snapshot.get("progress") or {}).get("summary") or {}
    artifact_index = snapshot.get("artifact_index") or {}
    return {
        "generated_at": snapshot.get("generated_at"),
        "event": event,
        "device": {
            "id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "peers": len((snapshot.get("device") or {}).get("peers") or []),
        },
        "git": {
            "short_sha": (snapshot.get("git") or {}).get("short_sha"),
            "dirty": (snapshot.get("git") or {}).get("dirty"),
        },
        "results": {
            "leaves": results.get("total_leaves", 0),
            "nodes": len(results.get("nodes") or {}),
        },
        "progress": {
            "log_files": progress.get("total_log_files", 0),
            "log_errors": progress.get("error_logs", 0),
            "newest_age": progress.get("newest_age"),
        },
        "reports": {
            "remote": len(snapshot.get("remote_status") or {}),
            "bundle_inspect": len(snapshot.get("bundle_inspect_reports") or {}),
            "diff": len(snapshot.get("diff_reports") or {}),
            "collect": len(snapshot.get("collect_reports") or {}),
            "verify": len(snapshot.get("verify_reports") or {}),
        },
        "artifact_index": {
            "peers": len(artifact_index.get("peers") or {}),
            "indexed": artifact_index_total(artifact_index),
        },
    }


def history_delta(previous: Optional[Dict[str, Any]], current: Dict[str, Any]) -> Dict[str, Any]:
    if not previous:
        return {}

    def nested_int(data: Dict[str, Any], *keys: str) -> int:
        value: Any = data
        for key in keys:
            if not isinstance(value, dict):
                return 0
            value = value.get(key)
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    fields = [
        ("result_leaves", ("results", "leaves")),
        ("log_errors", ("progress", "log_errors")),
        ("indexed_artifacts", ("artifact_index", "indexed")),
        ("remote_reports", ("reports", "remote")),
        ("bundle_inspect_reports", ("reports", "bundle_inspect")),
        ("diff_reports", ("reports", "diff")),
        ("collect_reports", ("reports", "collect")),
        ("verify_reports", ("reports", "verify")),
    ]
    delta = {}
    for name, path in fields:
        value = nested_int(current, *path) - nested_int(previous, *path)
        if value:
            delta[name] = value
    return delta


def read_history(limit: int = 20) -> List[Dict[str, Any]]:
    path = history_file()
    if not path.exists():
        return []
    entries: List[Dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except Exception:
        return []
    for line in lines[-max(0, limit):]:
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        if isinstance(item, dict):
            entries.append(item)
    return entries


def append_history(snapshot: Dict[str, Any], event: str = "snapshot") -> Dict[str, Any]:
    ensure_sync_dir()
    entry = history_entry_from_snapshot(snapshot, event)
    previous = read_history(limit=1)
    entry["delta"] = history_delta(previous[-1] if previous else None, entry)
    path = history_file()
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def write_state(snapshot: Dict[str, Any], event: str = "snapshot") -> None:
    ensure_sync_dir()
    STATE_FILE.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    append_history(snapshot, event)


def write_sync_report(prefix: str, node_id: str, report: Dict[str, Any]) -> Dict[str, Any]:
    ensure_sync_dir()
    report_path = SYNC_DIR / f"{prefix}_{node_id}.json"
    report["report_path"] = rel(report_path)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def empty_artifact_index(errors: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "version": 0,
        "updated_at": None,
        "index_path": rel(artifact_index_file()),
        "peers": {},
        "errors": errors or [],
    }


def load_artifact_index() -> Dict[str, Any]:
    path = artifact_index_file()
    if not path.exists():
        return empty_artifact_index()
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return empty_artifact_index([f"invalid artifact index: {type(e).__name__}: {e}"])
    if not isinstance(data, dict):
        return empty_artifact_index(["invalid artifact index: top-level value is not a mapping"])
    peers = data.get("peers")
    if not isinstance(peers, dict):
        peers = {}
    return {
        "version": data.get("version", 0),
        "updated_at": data.get("updated_at"),
        "index_path": rel(path),
        "peers": peers,
        "errors": data.get("errors") if isinstance(data.get("errors"), list) else [],
    }


def write_artifact_index(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    path = artifact_index_file()
    data["index_path"] = rel(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def sync_archive_root() -> Path:
    return SYNC_DIR / "archive"


def safe_sync_file(value: Any) -> Optional[Path]:
    if not isinstance(value, str) or not value.startswith(".syncmate/"):
        return None
    target = (REPO_ROOT / value).resolve()
    try:
        target.relative_to(SYNC_DIR.resolve())
    except ValueError:
        return None
    return target


def unique_archive_path(archive_dir: Path, name: str) -> Path:
    target = archive_dir / name
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    for idx in range(1, 1000):
        candidate = archive_dir / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not allocate archive path for {name}")


def artifact_index_total(index: Dict[str, Any]) -> int:
    total = 0
    for entry in (index.get("peers") or {}).values():
        summary = entry.get("summary") or {}
        total += int(summary.get("indexed") or len(entry.get("items") or []))
    return total


def inventory_from_index(index: Optional[Dict[str, Any]] = None,
                         node_ids: Optional[List[str]] = None,
                         only_incomplete: bool = False) -> Dict[str, Any]:
    data = load_artifact_index() if index is None else index
    selected = set(node_ids or [])
    peers: Dict[str, Any] = {}
    total_leaves = 0
    complete_leaves = 0
    incomplete_leaves = 0

    for node_id, peer_entry in sorted((data.get("peers") or {}).items()):
        if selected and node_id not in selected:
            continue
        expected = tuple((peer_entry.get("artifact_policy") or {}).get("include") or ARTIFACT_NAMES)
        leaves: Dict[str, Any] = {}
        for item in peer_entry.get("items") or []:
            if not isinstance(item, dict):
                continue
            local_path = item.get("local_path")
            artifact_name = Path(str(local_path or item.get("remote_path") or item.get("path") or "")).name
            local_leaf = str(Path(str(local_path))).replace("\\", "/").rsplit("/", 1)[0] if local_path else "unknown"
            leaf = leaves.setdefault(local_leaf, {
                "local_leaf": local_leaf,
                "remote_leaf": str(Path(str(item.get("remote_path") or item.get("path") or "")).parent).replace("\\", "/"),
                "cell": "unknown",
                "method_strategy": "unknown",
                "seed": "unknown",
                "layout": "unknown",
                "artifacts": [],
                "missing": [],
                "complete": False,
            })
            if local_path:
                _node, cell, method_strategy, seed, layout = classify_repo_leaf_path(local_path)
                leaf.update({
                    "cell": cell,
                    "method_strategy": method_strategy,
                    "seed": seed,
                    "layout": layout,
                })
            if artifact_name and artifact_name not in leaf["artifacts"]:
                leaf["artifacts"].append(artifact_name)

        leaf_values = []
        for leaf in leaves.values():
            artifacts = sorted(leaf["artifacts"])
            missing = [name for name in expected if name not in artifacts]
            leaf["artifacts"] = artifacts
            leaf["missing"] = missing
            leaf["complete"] = not missing
            if only_incomplete and leaf["complete"]:
                continue
            leaf_values.append(leaf)

        leaf_values.sort(key=lambda item: item["local_leaf"])
        summary = {
            "leaves": len(leaves),
            "shown": len(leaf_values),
            "complete": sum(1 for item in leaves.values() if item["complete"]),
            "incomplete": sum(1 for item in leaves.values() if not item["complete"]),
            "artifacts": sum(len(item["artifacts"]) for item in leaves.values()),
            "expected_artifacts": list(expected),
        }
        peers[node_id] = {
            "node_id": node_id,
            "landing": peer_entry.get("landing"),
            "updated_at": peer_entry.get("updated_at"),
            "summary": summary,
            "leaves": leaf_values,
        }
        total_leaves += summary["leaves"]
        complete_leaves += summary["complete"]
        incomplete_leaves += summary["incomplete"]

    return {
        "generated_at": now_iso(),
        "mode": "inventory",
        "index_path": data.get("index_path") or rel(artifact_index_file()),
        "only_incomplete": only_incomplete,
        "requested_peers": sorted(selected),
        "summary": {
            "peers": len(peers),
            "leaves": total_leaves,
            "complete": complete_leaves,
            "incomplete": incomplete_leaves,
            "indexed_artifacts": artifact_index_total(data),
        },
        "peers": peers,
        "errors": data.get("errors") or [],
    }


INVENTORY_CSV_FIELDS = [
    "node_id",
    "complete",
    "cell",
    "method_strategy",
    "seed",
    "layout",
    "local_leaf",
    "remote_leaf",
    "artifacts",
    "missing",
    "artifact_count",
    "missing_count",
]


def inventory_csv_rows(inventory: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for node_id, peer in sorted((inventory.get("peers") or {}).items()):
        for leaf in peer.get("leaves") or []:
            rows.append({
                "node_id": node_id,
                "complete": "true" if leaf.get("complete") else "false",
                "cell": leaf.get("cell") or "",
                "method_strategy": leaf.get("method_strategy") or "",
                "seed": leaf.get("seed") or "",
                "layout": leaf.get("layout") or "",
                "local_leaf": leaf.get("local_leaf") or "",
                "remote_leaf": leaf.get("remote_leaf") or "",
                "artifacts": ";".join(leaf.get("artifacts") or []),
                "missing": ";".join(leaf.get("missing") or []),
                "artifact_count": len(leaf.get("artifacts") or []),
                "missing_count": len(leaf.get("missing") or []),
            })
    return rows


EXPORT_CSV_FIELDS = [
    "node_id",
    "complete",
    "cell",
    "method_strategy",
    "seed",
    "artifact",
    "local_path",
    "sha256",
    "remote_path",
    "source_report",
    "remote_git",
    "verified_at",
]


def export_payload_from_index(index: Optional[Dict[str, Any]] = None,
                              node_ids: Optional[List[str]] = None,
                              include_incomplete: bool = False) -> Dict[str, Any]:
    data = load_artifact_index() if index is None else index
    selected = set(node_ids or [])
    leaves: List[Dict[str, Any]] = []
    skipped_incomplete = 0
    total_index_leaves = 0

    for node_id, peer_entry in sorted((data.get("peers") or {}).items()):
        if selected and node_id not in selected:
            continue
        expected = tuple((peer_entry.get("artifact_policy") or {}).get("include") or ARTIFACT_NAMES)
        grouped: Dict[str, Dict[str, Any]] = {}
        for item in peer_entry.get("items") or []:
            if not isinstance(item, dict):
                continue
            local_path = item.get("local_path")
            remote_path = item.get("remote_path") or item.get("path")
            artifact_name = Path(str(local_path or remote_path or "")).name
            if not artifact_name:
                continue
            local_leaf = str(Path(str(local_path))).replace("\\", "/").rsplit("/", 1)[0] if local_path else "unknown"
            leaf = grouped.setdefault(local_leaf, {
                "node_id": node_id,
                "landing": peer_entry.get("landing"),
                "local_leaf": local_leaf,
                "remote_leaf": str(Path(str(remote_path or "")).parent).replace("\\", "/"),
                "cell": "unknown",
                "method_strategy": "unknown",
                "seed": "unknown",
                "layout": "unknown",
                "expected_artifacts": list(expected),
                "artifacts": {},
                "missing": [],
                "complete": False,
                "source_report": peer_entry.get("source_report"),
                "updated_at": peer_entry.get("updated_at"),
            })
            if local_path:
                _node, cell, method_strategy, seed, layout = classify_repo_leaf_path(local_path)
                leaf.update({
                    "cell": cell,
                    "method_strategy": method_strategy,
                    "seed": seed,
                    "layout": layout,
                })
            leaf["artifacts"][artifact_name] = {
                "artifact": artifact_name,
                "local_path": local_path,
                "remote_path": remote_path,
                "sha256": item.get("sha256"),
                "source_report": peer_entry.get("source_report"),
                "remote_git": item.get("remote_git") or (peer_entry.get("remote") or {}).get("git") or {},
                "verified_at": item.get("verified_at") or peer_entry.get("updated_at"),
            }

        for leaf in grouped.values():
            total_index_leaves += 1
            present = set(leaf["artifacts"])
            leaf["missing"] = [name for name in expected if name not in present]
            leaf["complete"] = not leaf["missing"]
            leaf["artifact_count"] = len(leaf["artifacts"])
            leaf["artifacts"] = {
                name: leaf["artifacts"][name]
                for name in sorted(leaf["artifacts"])
            }
            if not include_incomplete and not leaf["complete"]:
                skipped_incomplete += 1
                continue
            leaves.append(leaf)

    leaves.sort(key=lambda item: (item.get("node_id", ""), item.get("cell", ""), item.get("method_strategy", ""), item.get("seed", "")))
    artifact_rows = sum(len(leaf.get("artifacts") or {}) for leaf in leaves)
    return {
        "generated_at": now_iso(),
        "mode": "export",
        "index_path": data.get("index_path") or rel(artifact_index_file()),
        "include_incomplete": include_incomplete,
        "requested_peers": sorted(selected),
        "summary": {
            "peers": len({leaf["node_id"] for leaf in leaves}),
            "leaves": len(leaves),
            "artifacts": artifact_rows,
            "complete_leaves": sum(1 for leaf in leaves if leaf.get("complete")),
            "incomplete_leaves": sum(1 for leaf in leaves if not leaf.get("complete")),
            "skipped_incomplete": skipped_incomplete,
            "indexed_leaves": total_index_leaves,
            "indexed_artifacts": artifact_index_total(data),
        },
        "leaves": leaves,
        "errors": data.get("errors") or [],
        "files": {
            "manifest": rel(export_manifest_file()),
            "csv": rel(export_csv_file()),
        },
    }


def export_csv_rows(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for leaf in data.get("leaves") or []:
        for artifact_name, artifact in sorted((leaf.get("artifacts") or {}).items()):
            remote_git = artifact.get("remote_git") or {}
            if isinstance(remote_git, dict):
                remote_git_value = remote_git.get("short_sha") or remote_git.get("sha") or ""
            else:
                remote_git_value = str(remote_git or "")
            rows.append({
                "node_id": leaf.get("node_id") or "",
                "complete": "true" if leaf.get("complete") else "false",
                "cell": leaf.get("cell") or "",
                "method_strategy": leaf.get("method_strategy") or "",
                "seed": leaf.get("seed") or "",
                "artifact": artifact_name,
                "local_path": artifact.get("local_path") or "",
                "sha256": artifact.get("sha256") or "",
                "remote_path": artifact.get("remote_path") or "",
                "source_report": artifact.get("source_report") or leaf.get("source_report") or "",
                "remote_git": remote_git_value,
                "verified_at": artifact.get("verified_at") or "",
            })
    return rows


def write_export_files(data: Dict[str, Any]) -> Dict[str, str]:
    ensure_sync_dir()
    manifest_path = export_manifest_file()
    csv_path = export_csv_file()
    manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=EXPORT_CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(export_csv_rows(data))
    return {
        "manifest": rel(manifest_path),
        "csv": rel(csv_path),
    }


RESULTS_CSV_FIELDS = [
    "node_id",
    "complete",
    "cell",
    "dataset",
    "base_model",
    "ratio",
    "method",
    "strategy",
    "strategy_full",
    "method_strategy",
    "seed",
    "layout",
    "f1_after",
    "f1_drop",
    "mia_auc",
    "unlearn_time",
    "selection_time",
    "selection_cache_hit",
    "selected_n",
    "perf_before",
    "perf_unlearn",
    "perf_retrain",
    "drop_retrain",
    "gap",
    "gap_pct",
    "mean_pred_shift",
    "max_pred_shift",
    "fraction_flipped",
    "hop_1_flip_rate",
    "hop_1_count",
    "hop_2_flip_rate",
    "hop_2_count",
    "hop_3_flip_rate",
    "hop_3_count",
    "hop_gt3_flip_rate",
    "hop_gt3_count",
    "git_sha",
    "hostname",
    "timestamp",
    "attack_sha256",
    "collateral_sha256",
    "meta_sha256",
    "local_leaf",
    "source_report",
    "status",
    "parse_errors",
]


def split_cell_name(cell: Any) -> Tuple[str, str, str]:
    text = str(cell or "")
    head = text
    ratio = ""
    marker = text.rfind("_r")
    if marker >= 0:
        head = text[:marker]
        ratio = text[marker + 2:]
    dataset, sep, base_model = head.rpartition("_")
    if not sep:
        dataset = head
        base_model = ""
    return dataset, base_model, ratio


def split_method_strategy_name(method_strategy: Any) -> Tuple[str, str, str]:
    text = str(method_strategy or "")
    for strategy in sorted(STRATEGY_NAMES, key=len, reverse=True):
        token = f"_{strategy}"
        idx = text.find(token)
        if idx <= 0:
            continue
        tail = text[idx + len(token):]
        if tail and not tail.startswith("_"):
            continue
        return text[:idx], strategy, strategy + tail
    method, sep, strategy_full = text.rpartition("_")
    if sep and method and strategy_full:
        return method, strategy_full, strategy_full
    return text or "unknown", "unknown", "unknown"


def read_indexed_json_artifact(leaf: Dict[str, Any], artifact_name: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    artifact = (leaf.get("artifacts") or {}).get(artifact_name) or {}
    local_path = artifact.get("local_path")
    if not local_path:
        return None, f"{artifact_name} missing from trusted leaf"
    target = safe_repo_path(local_path)
    if target is None:
        return None, f"{artifact_name} has unsafe local_path: {local_path!r}"
    if not target.is_file():
        return None, f"{artifact_name} local file missing: {rel(target)}"
    try:
        data = json.loads(target.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return None, f"{artifact_name} unreadable json: {type(e).__name__}: {e}"
    if not isinstance(data, dict):
        return None, f"{artifact_name} json root is not an object"
    return data, None


def attack_result_entries(data: Optional[Dict[str, Any]], fallback_strategy: str) -> Tuple[List[Tuple[str, Dict[str, Any]]], List[str]]:
    if not data:
        return [(fallback_strategy, {})], ["attack.json missing or unreadable"]
    results = data.get("results")
    entries: List[Tuple[str, Dict[str, Any]]] = []
    errors: List[str] = []
    if isinstance(results, dict):
        for key, value in sorted(results.items(), key=lambda pair: str(pair[0])):
            if isinstance(value, dict):
                entries.append((str(key), value))
            else:
                errors.append(f"attack result {key!r} is not an object")
    elif isinstance(results, list):
        for idx, value in enumerate(results):
            if not isinstance(value, dict):
                errors.append(f"attack result #{idx} is not an object")
                continue
            key = value.get("strategy") or value.get("strategy_name") or fallback_strategy
            entries.append((str(key), value))
    else:
        errors.append("attack.json has no results object")
    if not entries:
        entries.append((fallback_strategy, {}))
    return entries, errors


def collateral_rows_by_strategy(data: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Any], List[str]]:
    if not data:
        return {}, {}, ["collateral.json missing or unreadable"]
    raw = data.get("results")
    if isinstance(raw, dict):
        rows = [value for value in raw.values() if isinstance(value, dict)]
    elif isinstance(raw, list):
        rows = [value for value in raw if isinstance(value, dict)]
    else:
        return {}, {}, ["collateral.json has no results list"]
    if not rows:
        return {}, {}, ["collateral.json results[] empty"]
    by_strategy: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = row.get("strategy") or row.get("strategy_name")
        if key:
            by_strategy[str(key)] = row
    return by_strategy, rows[0], []


def collateral_metric_fields(row: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "perf_before": row.get("perf_before"),
        "perf_unlearn": row.get("perf_unlearn"),
        "perf_retrain": row.get("perf_retrain"),
        "drop_retrain": row.get("drop_retrain"),
        "gap": row.get("gap"),
        "gap_pct": row.get("gap_pct"),
        "mean_pred_shift": row.get("mean_pred_shift"),
        "max_pred_shift": row.get("max_pred_shift"),
        "fraction_flipped": row.get("fraction_flipped"),
    }
    hop = row.get("hop_decay") or {}
    if isinstance(hop, dict):
        for label, key in (("1", "1_hop"), ("2", "2_hop"), ("3", "3_hop"), ("gt3", "gt3_hop")):
            out[f"hop_{label}_flip_rate"] = hop.get(f"{key}_flip_rate")
            out[f"hop_{label}_count"] = hop.get(f"{key}_count")
    return out


def meta_fields(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not data:
        return {"git_sha": None, "hostname": None, "timestamp": None}
    return {
        "git_sha": str(data.get("git_sha") or "")[:7] or None,
        "hostname": data.get("hostname"),
        "timestamp": data.get("timestamp"),
    }


def numeric_value(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def artifact_sha_map(leaf: Dict[str, Any]) -> Dict[str, Any]:
    artifacts = leaf.get("artifacts") or {}
    return {
        "attack_sha256": (artifacts.get("attack.json") or {}).get("sha256"),
        "collateral_sha256": (artifacts.get("collateral.json") or {}).get("sha256"),
        "meta_sha256": (artifacts.get("_meta.json") or {}).get("sha256"),
    }


def results_payload_from_index(index: Optional[Dict[str, Any]] = None,
                               node_ids: Optional[List[str]] = None,
                               include_incomplete: bool = False) -> Dict[str, Any]:
    data = load_artifact_index() if index is None else index
    trusted = export_payload_from_index(data, node_ids=node_ids, include_incomplete=include_incomplete)
    rows: List[Dict[str, Any]] = []
    parse_errors: List[Dict[str, Any]] = []

    for leaf in trusted.get("leaves") or []:
        method, directory_strategy, strategy_full = split_method_strategy_name(leaf.get("method_strategy"))
        dataset, base_model, ratio = split_cell_name(leaf.get("cell"))
        leaf_errors = [f"missing artifact: {name}" for name in (leaf.get("missing") or [])]

        attack_data, attack_error = read_indexed_json_artifact(leaf, "attack.json")
        collateral_data, collateral_error = read_indexed_json_artifact(leaf, "collateral.json")
        meta_data, meta_error = read_indexed_json_artifact(leaf, "_meta.json")
        for error in (attack_error, collateral_error, meta_error):
            if error:
                leaf_errors.append(error)

        attack_entries, attack_errors = attack_result_entries(attack_data, directory_strategy)
        collateral_by_strategy, collateral_default, collateral_errors = collateral_rows_by_strategy(collateral_data)
        leaf_errors.extend(attack_errors)
        leaf_errors.extend(collateral_errors)
        meta = meta_fields(meta_data)
        shas = artifact_sha_map(leaf)

        for strategy_key, attack_result in attack_entries:
            result_strategy = str(strategy_key or directory_strategy)
            strategy = result_strategy if result_strategy in STRATEGY_NAMES else directory_strategy
            collateral_row = (
                collateral_by_strategy.get(result_strategy)
                or collateral_by_strategy.get(strategy)
                or collateral_by_strategy.get(strategy_full)
                or collateral_default
            )
            collateral = collateral_metric_fields(collateral_row)
            f1_after = attack_result.get("f1_after")
            perf_before = collateral.get("perf_before")
            f1_drop = None
            f1_after_num = numeric_value(f1_after)
            perf_before_num = numeric_value(perf_before)
            if f1_after_num is not None and perf_before_num is not None:
                f1_drop = perf_before_num - f1_after_num

            selected_nodes = attack_result.get("selected_nodes")
            selected_n = len(selected_nodes) if isinstance(selected_nodes, list) else None
            row_errors = list(leaf_errors)
            status = "ok" if leaf.get("complete") and not row_errors else "incomplete" if not leaf.get("complete") else "parse-error"
            row = {
                "node_id": leaf.get("node_id"),
                "complete": bool(leaf.get("complete")),
                "cell": leaf.get("cell"),
                "dataset": dataset,
                "base_model": base_model,
                "ratio": ratio,
                "method": method,
                "strategy": strategy,
                "strategy_full": strategy_full,
                "method_strategy": leaf.get("method_strategy"),
                "seed": leaf.get("seed"),
                "layout": leaf.get("layout"),
                "f1_after": f1_after,
                "f1_drop": f1_drop,
                "mia_auc": attack_result.get("mia_auc"),
                "unlearn_time": attack_result.get("unlearn_time"),
                "selection_time": attack_result.get("selection_time"),
                "selection_cache_hit": attack_result.get("selection_cache_hit"),
                "selected_n": selected_n,
                **collateral,
                **meta,
                **shas,
                "local_leaf": leaf.get("local_leaf"),
                "remote_leaf": leaf.get("remote_leaf"),
                "source_report": leaf.get("source_report"),
                "status": status,
                "parse_errors": row_errors,
            }
            rows.append(row)
            for error in row_errors:
                parse_errors.append({
                    "node_id": leaf.get("node_id"),
                    "local_leaf": leaf.get("local_leaf"),
                    "strategy": strategy,
                    "error": error,
                })

    rows.sort(key=lambda item: (
        str(item.get("node_id") or ""),
        str(item.get("cell") or ""),
        str(item.get("method") or ""),
        str(item.get("strategy_full") or ""),
        str(item.get("seed") or ""),
    ))
    return {
        "generated_at": now_iso(),
        "mode": "results",
        "index_path": data.get("index_path") or rel(artifact_index_file()),
        "include_incomplete": include_incomplete,
        "requested_peers": sorted(set(node_ids or [])),
        "summary": {
            "peers": len({row.get("node_id") for row in rows}),
            "leaves": (trusted.get("summary") or {}).get("leaves", 0),
            "rows": len(rows),
            "complete_leaves": (trusted.get("summary") or {}).get("complete_leaves", 0),
            "incomplete_leaves": (trusted.get("summary") or {}).get("incomplete_leaves", 0),
            "skipped_incomplete": (trusted.get("summary") or {}).get("skipped_incomplete", 0),
            "parse_error_rows": sum(1 for row in rows if row.get("parse_errors")),
            "parse_errors": len(parse_errors),
        },
        "rows": rows,
        "parse_errors": parse_errors,
        "errors": trusted.get("errors") or [],
        "files": {
            "json": rel(results_table_file()),
            "csv": rel(results_csv_file()),
        },
    }


def results_csv_rows(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    for item in data.get("rows") or []:
        row = {field: item.get(field, "") for field in RESULTS_CSV_FIELDS}
        row["complete"] = "true" if item.get("complete") else "false"
        row["parse_errors"] = ";".join(item.get("parse_errors") or [])
        rows.append(row)
    return rows


def write_results_table_files(data: Dict[str, Any]) -> Dict[str, str]:
    ensure_sync_dir()
    json_path = results_table_file()
    csv_path = results_csv_file()
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=RESULTS_CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results_csv_rows(data))
    return {
        "json": rel(json_path),
        "csv": rel(csv_path),
    }


def incomplete_inventory_peers(index: Dict[str, Any],
                               node_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    inventory = inventory_from_index(index, node_ids=node_ids, only_incomplete=True)
    peers = []
    for node_id, peer in sorted((inventory.get("peers") or {}).items()):
        leaves = peer.get("leaves") or []
        if not leaves:
            continue
        missing_counts: Counter[str] = Counter()
        examples = []
        for leaf in leaves:
            for name in leaf.get("missing") or []:
                missing_counts[str(name)] += 1
            if len(examples) < 3:
                examples.append({
                    "local_leaf": leaf.get("local_leaf"),
                    "cell": leaf.get("cell"),
                    "method_strategy": leaf.get("method_strategy"),
                    "seed": leaf.get("seed"),
                    "missing": leaf.get("missing") or [],
                })
        peers.append({
            "node_id": node_id,
            "incomplete": len(leaves),
            "missing_counts": dict(sorted(missing_counts.items())),
            "examples": examples,
        })
    return peers


def incomplete_remote_inventory(report: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    inventory = report.get("remote_inventory") or {}
    leaves = inventory.get("leaves") or []
    incomplete = [leaf for leaf in leaves if not leaf.get("complete")]
    if not incomplete:
        return None
    missing_counts: Counter[str] = Counter()
    examples = []
    for leaf in incomplete:
        for name in leaf.get("missing") or []:
            missing_counts[str(name)] += 1
        if len(examples) < 3:
            examples.append({
                "remote_leaf": leaf.get("remote_leaf"),
                "cell": leaf.get("cell"),
                "method_strategy": leaf.get("method_strategy"),
                "seed": leaf.get("seed"),
                "missing": leaf.get("missing") or [],
            })
    return {
        "incomplete": len(incomplete),
        "missing_counts": dict(sorted(missing_counts.items())),
        "examples": examples,
    }


def format_missing_counts(counts: Dict[str, Any]) -> str:
    return ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))


def check_artifact_index(index: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = load_artifact_index() if index is None else index
    errors = list(data.get("errors") or [])
    missing: List[Dict[str, Any]] = []
    mismatched: List[Dict[str, Any]] = []
    unsafe: List[Dict[str, Any]] = []
    peer_summaries: Dict[str, Any] = {}

    for node_id, entry in sorted((data.get("peers") or {}).items()):
        items = entry.get("items") or []
        if not isinstance(items, list):
            errors.append(f"peer {node_id} index items must be a list")
            items = []
        peer_summary = {
            "indexed": len(items),
            "checked": 0,
            "ok": 0,
            "missing": 0,
            "mismatched": 0,
            "unsafe": 0,
        }
        for item in items:
            if not isinstance(item, dict):
                errors.append(f"peer {node_id} contains a non-object index item")
                continue
            local_path = item.get("local_path")
            expected_sha = item.get("sha256")
            remote_path = item.get("remote_path") or item.get("path")
            target = safe_repo_path(local_path)
            if target is None:
                unsafe.append({
                    "node_id": node_id,
                    "local_path": local_path,
                    "remote_path": remote_path,
                    "reason": "not a safe repo-relative path",
                })
                peer_summary["unsafe"] += 1
                continue
            if not target.is_file():
                missing.append({
                    "node_id": node_id,
                    "local_path": rel(target),
                    "remote_path": remote_path,
                    "sha256": expected_sha,
                })
                peer_summary["missing"] += 1
                continue
            if not expected_sha:
                errors.append(f"peer {node_id} item {remote_path or local_path} has no sha256")
                continue
            peer_summary["checked"] += 1
            actual_sha = sha256_file(target)
            if actual_sha == expected_sha:
                peer_summary["ok"] += 1
            else:
                mismatched.append({
                    "node_id": node_id,
                    "local_path": rel(target),
                    "remote_path": remote_path,
                    "expected_sha256": expected_sha,
                    "actual_sha256": actual_sha,
                })
                peer_summary["mismatched"] += 1
        peer_summaries[node_id] = peer_summary

    checked = sum(item["checked"] for item in peer_summaries.values())
    ok = sum(item["ok"] for item in peer_summaries.values())
    failed = bool(errors or missing or mismatched or unsafe)
    return {
        "generated_at": now_iso(),
        "mode": "index-check",
        "index_path": data.get("index_path") or rel(artifact_index_file()),
        "summary": {
            "peers": len(data.get("peers") or {}),
            "indexed": artifact_index_total(data),
            "checked": checked,
            "ok": ok,
            "missing": len(missing),
            "mismatched": len(mismatched),
            "unsafe": len(unsafe),
            "errors": len(errors),
            "status": "failed" if failed else "ok",
        },
        "peers": peer_summaries,
        "missing": missing,
        "mismatched": mismatched,
        "unsafe": unsafe,
        "errors": errors,
    }


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


FINGERPRINT_TIME_KEYS = {
    "generated_at",
    "updated_at",
    "verified_at",
    "remote_mtime_ns",
    "newest_mtime",
    "newest_age",
    "latest_log_age",
    "age",
}


def stable_for_hash(value: Any, *, include_timestamps: bool = False) -> Any:
    if isinstance(value, dict):
        return {
            str(key): stable_for_hash(item, include_timestamps=include_timestamps)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if include_timestamps or str(key) not in FINGERPRINT_TIME_KEYS
        }
    if isinstance(value, list):
        return [stable_for_hash(item, include_timestamps=include_timestamps) for item in value]
    if isinstance(value, tuple):
        return [stable_for_hash(item, include_timestamps=include_timestamps) for item in value]
    return value


def stable_json(value: Any, *, include_timestamps: bool = False) -> str:
    return json.dumps(
        stable_for_hash(value, include_timestamps=include_timestamps),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def stable_hash(value: Any, *, include_timestamps: bool = False, length: int = 16) -> str:
    digest = hashlib.sha256(stable_json(value, include_timestamps=include_timestamps).encode("utf-8")).hexdigest()
    return digest[:length] if length else digest


def selected_report_fields(report: Dict[str, Any]) -> Dict[str, Any]:
    keys = (
        "generated_at",
        "mode",
        "bundle_path",
        "package_generated_at",
        "device",
        "git",
        "fingerprint",
        "manifest",
        "audit",
        "landing",
        "artifact_policy",
        "summary",
        "remote_inventory",
        "missing",
        "conflicts",
        "verified",
        "fetched",
        "verification_failed",
        "errors",
        "artifact_index",
        "report_path",
    )
    return {key: report.get(key) for key in keys if key in report}


def reports_fingerprint_data(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for section, key in (
        ("remote_status", "remote_status"),
        ("bundle_inspect", "bundle_inspect_reports"),
        ("diff", "diff_reports"),
        ("collect", "collect_reports"),
        ("verify", "verify_reports"),
    ):
        out[section] = {
            node_id: selected_report_fields(report)
            for node_id, report in sorted((snapshot.get(key) or {}).items())
        }
    return out


def artifact_index_fingerprint_data(index: Dict[str, Any]) -> Dict[str, Any]:
    peers = {}
    for node_id, entry in sorted((index.get("peers") or {}).items()):
        items = []
        for item in entry.get("items") or []:
            if not isinstance(item, dict):
                continue
            items.append({
                key: item.get(key)
                for key in (
                    "source_node",
                    "remote_path",
                    "local_path",
                    "sha256",
                    "local_sha256",
                    "remote_git",
                    "verified_at",
                    "remote_mtime_ns",
                )
                if key in item
            })
        items.sort(key=lambda item: (str(item.get("local_path") or ""), str(item.get("remote_path") or "")))
        peers[node_id] = {
            "landing": entry.get("landing"),
            "artifact_policy": entry.get("artifact_policy"),
            "source_report": entry.get("source_report"),
            "summary": entry.get("summary"),
            "updated_at": entry.get("updated_at"),
            "items": items,
        }
    return {
        "updated_at": index.get("updated_at"),
        "index_path": index.get("index_path"),
        "errors": index.get("errors") or [],
        "peers": peers,
    }


def load_optional_json(path: Path) -> Optional[Any]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return {"errors": [f"invalid json: {type(e).__name__}: {e}"], "path": rel(path)}


def fingerprint_basis(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    results = snapshot.get("results") or {}
    progress = snapshot.get("progress") or {}
    progress_summary = progress.get("summary") or {}
    artifact_index = snapshot.get("artifact_index") or {}
    export_manifest = snapshot["export_manifest"] if "export_manifest" in snapshot else load_optional_json(export_manifest_file())
    results_table = snapshot["results_table"] if "results_table" in snapshot else load_optional_json(results_table_file())
    preflight = snapshot["preflight"] if "preflight" in snapshot else load_optional_json(last_preflight_file())
    return {
        "device": {
            "id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "artifact_policy": (snapshot.get("device") or {}).get("artifact_policy"),
            "peers": (snapshot.get("device") or {}).get("peers") or [],
            "peer_configs": (snapshot.get("device") or {}).get("peer_configs") or {},
            "setup_warnings": (snapshot.get("device") or {}).get("setup_warnings") or [],
        },
        "git": {
            "branch": (snapshot.get("git") or {}).get("branch"),
            "short_sha": (snapshot.get("git") or {}).get("short_sha"),
            "dirty": (snapshot.get("git") or {}).get("dirty"),
            "status_short": sorted((snapshot.get("git") or {}).get("status_short") or []),
        },
        "results": {
            "root": results.get("root"),
            "total_leaves": results.get("total_leaves", 0),
            "nodes": results.get("nodes") or {},
            "issues": results.get("issues") or [],
        },
        "progress": {
            "summary": progress_summary,
            "error_logs": progress.get("error_logs") or [],
        },
        "reports": reports_fingerprint_data(snapshot),
        "artifact_index": artifact_index_fingerprint_data(artifact_index),
        "export_manifest": export_manifest,
        "results_table": results_table,
        "preflight": preflight,
    }


def fingerprint_payload(snapshot: Dict[str, Any], *, include_timestamps: bool = False) -> Dict[str, Any]:
    basis = fingerprint_basis(snapshot)
    components = {
        key: stable_hash(value, include_timestamps=include_timestamps, length=12)
        for key, value in sorted(basis.items())
    }
    entry = history_entry_from_snapshot(snapshot, "fingerprint")
    entry.pop("generated_at", None)
    entry.pop("event", None)
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "fingerprint",
        "include_timestamps": include_timestamps,
        "token": stable_hash(basis, include_timestamps=include_timestamps, length=16),
        "components": components,
        "counts": entry,
        "files": {
            "state": rel(STATE_FILE),
            "artifact_index": rel(artifact_index_file()),
            "export_manifest": rel(export_manifest_file()),
            "results_table": rel(results_table_file()),
            "preflight": rel(last_preflight_file()),
        },
    }


FINGERPRINT_COMPONENT_NOTES = {
    "device": "device-local identity and peer setup normally differ",
    "git": "tracked branch, commit, and dirty state should usually match",
    "results": "runner and collector result layouts can differ by role",
    "progress": "local log progress naturally differs between devices",
    "reports": "collector-side saved sync reports often differ",
    "artifact_index": "collector-side verified artifact landing state",
    "export_manifest": "collector-side downstream artifact manifest",
    "results_table": "collector-side parsed trusted metric table",
    "preflight": "latest saved local preflight decision and blockers",
}
FINGERPRINT_ATTENTION_COMPONENTS = {"git"}


def remote_fingerprint_from_report(report: Dict[str, Any]) -> Dict[str, Any]:
    summary = report.get("summary") or {}
    snapshot = report.get("snapshot") or {}
    snapshot_fp = (snapshot.get("fingerprint") or {}) if isinstance(snapshot, dict) else {}
    token = summary.get("fingerprint") or snapshot_fp.get("token")
    components = summary.get("fingerprint_components") or snapshot_fp.get("components") or {}
    source = "summary" if summary.get("fingerprint") or summary.get("fingerprint_components") else "snapshot"
    if (not token or not components) and isinstance(snapshot, dict) and snapshot:
        snapshot_copy = json.loads(json.dumps(snapshot))
        snapshot_copy.setdefault("export_manifest", None)
        snapshot_copy.setdefault("results_table", None)
        computed = fingerprint_payload(snapshot_copy)
        token = token or computed.get("token")
        components = components or computed.get("components") or {}
        source = "computed-from-snapshot"
    return {
        "token": token,
        "components": components if isinstance(components, dict) else {},
        "source": source,
    }


def compare_fingerprint_payload(snapshot: Dict[str, Any],
                                node_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    local_fp = snapshot.get("fingerprint") or fingerprint_payload(snapshot)
    local_components = local_fp.get("components") or {}
    remote_reports = snapshot.get("remote_status") or {}
    if node_ids:
        selected = sorted(str(node_id) for node_id in node_ids)
    else:
        selected = sorted(set(configured_peers(snapshot)) | set(remote_reports))

    peers: Dict[str, Any] = {}
    counts = Counter()
    for node_id in selected:
        report = remote_reports.get(node_id) or {}
        if not report:
            counts["no_remote_status"] += 1
            peers[node_id] = {
                "node_id": node_id,
                "known": node_id in configured_peers(snapshot),
                "status": "no-remote-status",
                "remote_report": f".syncmate/remote_status_{node_id}.json",
                "remote_generated_at": None,
                "remote_token": None,
                "different_components": [],
                "attention_components": [],
                "components": {},
                "errors": [],
                "action": f"Run python scripts/syncmate/syncmate.py remote-status {node_id} --apply.",
            }
            continue

        remote_fp = remote_fingerprint_from_report(report)
        remote_components = remote_fp.get("components") or {}
        component_keys = sorted(set(local_components) | set(remote_components))
        comparisons = {}
        different = []
        attention = []
        for key in component_keys:
            local_hash = local_components.get(key)
            remote_hash = remote_components.get(key)
            matches = bool(local_hash and remote_hash and local_hash == remote_hash)
            if not matches:
                different.append(key)
                if key in FINGERPRINT_ATTENTION_COMPONENTS:
                    attention.append(key)
            comparisons[key] = {
                "local": local_hash,
                "remote": remote_hash,
                "match": matches,
                "note": FINGERPRINT_COMPONENT_NOTES.get(key, ""),
            }

        errors = list(report.get("errors") or [])
        if errors:
            status = "remote-status-error"
        elif not remote_fp.get("token"):
            status = "missing-remote-fingerprint"
        elif local_fp.get("token") == remote_fp.get("token"):
            status = "same"
        elif attention:
            status = "attention"
        else:
            status = "different"

        counts[status.replace("-", "_")] += 1
        action = "No action needed."
        if status == "remote-status-error":
            action = f"Fix remote-status error, then rerun python scripts/syncmate/syncmate.py remote-status {node_id} --apply."
        elif status == "missing-remote-fingerprint":
            action = f"Rerun python scripts/syncmate/syncmate.py remote-status {node_id} --apply to refresh fingerprint metadata."
        elif attention:
            action = f"Inspect attention components ({', '.join(attention)}); tracked code may be out of sync."
        elif different:
            action = "Review differing components; role-local state may explain device/results/report differences."

        peers[node_id] = {
            "node_id": node_id,
            "known": node_id in configured_peers(snapshot),
            "status": status,
            "remote_report": report.get("report_path") or f".syncmate/remote_status_{node_id}.json",
            "remote_generated_at": report.get("generated_at"),
            "remote_age": format_age(report.get("generated_at")),
            "remote_token": remote_fp.get("token"),
            "remote_source": remote_fp.get("source"),
            "matched_components": sum(1 for item in comparisons.values() if item["match"]),
            "different_components": different,
            "attention_components": attention,
            "components": comparisons,
            "errors": errors,
            "action": action,
        }

    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "compare",
        "local": {
            "token": local_fp.get("token"),
            "components": local_components,
            "counts": local_fp.get("counts") or {},
        },
        "requested_peers": selected,
        "summary": {
            "peers": len(selected),
            "same": counts.get("same", 0),
            "different": counts.get("different", 0),
            "attention": counts.get("attention", 0),
            "missing": counts.get("no_remote_status", 0) + counts.get("missing_remote_fingerprint", 0),
            "errors": counts.get("remote_status_error", 0),
        },
        "peers": peers,
    }


def fingerprint_compare_diagnostics(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    compare = compare_fingerprint_payload(snapshot)
    for node_id, peer in sorted((compare.get("peers") or {}).items()):
        status = peer.get("status")
        if status in ("same", "no-remote-status", "remote-status-error"):
            continue
        if status == "attention":
            components = ", ".join(peer.get("attention_components") or []) or "unknown"
            diagnostics.append({
                "severity": "error",
                "code": "fingerprint-attention",
                "node": node_id,
                "message": f"{node_id} fingerprint attention component(s) differ from local state: {components}.",
                "action": f"Run python scripts/syncmate/syncmate.py compare {node_id} --json; synchronize tracked files before collecting or aggregating results.",
            })
            continue
        if status == "missing-remote-fingerprint":
            diagnostics.append({
                "severity": "warn",
                "code": "fingerprint-missing",
                "node": node_id,
                "message": f"{node_id} remote status report has no fingerprint metadata.",
                "action": f"Run python scripts/syncmate/syncmate.py remote-status {node_id} --apply to refresh the saved peer snapshot.",
            })
            continue
        if status == "different":
            components = ", ".join(peer.get("different_components") or []) or "unknown"
            diagnostics.append({
                "severity": "info",
                "code": "fingerprint-different",
                "node": node_id,
                "message": f"{node_id} fingerprint differs in component(s): {components}.",
                "action": f"Run python scripts/syncmate/syncmate.py compare {node_id} to inspect whether the difference is role-local state or a sync issue.",
            })
    return diagnostics


def shell_quote(value: Any) -> str:
    return shlex.quote(str(value))


def command_arg(value: Any) -> str:
    text = str(value)
    if text.startswith("<") and text.endswith(">"):
        return text
    return shell_quote(text)


def command_line(parts: List[Any]) -> str:
    return " ".join(command_arg(part) for part in parts)


def syncmate_command_prefix(config_path: Optional[Path] = None) -> List[Any]:
    parts: List[Any] = ["python", "scripts/syncmate/syncmate.py"]
    if config_path and config_path != DEFAULT_DEVICE_FILE:
        parts.extend(["--config", rel(config_path)])
    return parts


def remote_status_command(repo_path: str, python_executable: str = "python") -> str:
    return (
        f"cd {shell_quote(repo_path)} && "
        + command_line([
            python_executable,
            "scripts/syncmate/syncmate.py",
            "status",
            "--json",
            "--no-write-state",
        ])
    )


def remote_manifest_command(repo_path: str, roots: List[str],
                            artifact_names: Optional[Tuple[str, ...]] = None,
                            python_executable: str = "python") -> str:
    return (
        f"cd {shell_quote(repo_path)} && "
        + command_line([
            python_executable,
            "scripts/syncmate/syncmate.py",
            "manifest",
            "--json",
            "--roots",
            *roots,
            "--include",
            *(artifact_names or ARTIFACT_NAMES),
        ])
    )


def remote_tar_command(repo_path: str) -> str:
    return f"cd {shell_quote(repo_path)} && tar czf - -T -"


def runner_init_command(repo_path: str, node_id: str, role: str,
                        collector_id: Any, artifact_names: Tuple[str, ...],
                        python_executable: str = "python") -> str:
    parts = [
        python_executable,
        "scripts/syncmate/syncmate.py",
        "init-device",
        "--device-id",
        node_id,
        "--role",
        role,
        "--repo-path",
        repo_path,
    ]
    if collector_id:
        parts.extend(["--collector-hint", str(collector_id)])
    if artifact_names:
        parts.extend(["--artifact-include", *artifact_names])
    return f"cd {shell_quote(repo_path)} && " + " ".join(shell_quote(part) for part in parts)


def load_remote_status_reports() -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    if not SYNC_DIR.exists():
        return reports
    for path in sorted(SYNC_DIR.glob("remote_status_*.json")):
        node_id = path.stem.replace("remote_status_", "", 1)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            reports[node_id] = {
                "node_id": node_id,
                "report_path": rel(path),
                "errors": [f"invalid remote status report: {type(e).__name__}: {e}"],
            }
            continue

        summary = data.get("summary") or {}
        snapshot = data.get("snapshot") or {}
        reports[node_id] = {
            "node_id": data.get("node_id") or node_id,
            "generated_at": data.get("generated_at") or snapshot.get("generated_at"),
            "report_path": rel(path),
            "summary": summary,
            "snapshot": snapshot,
            "remote": data.get("remote") or {},
            "errors": data.get("errors") or [],
        }
    return reports


def load_bundle_inspect_reports() -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    if not SYNC_DIR.exists():
        return reports
    for path in sorted(SYNC_DIR.glob("last_bundle_inspect_*.json")):
        node_id = path.stem.replace("last_bundle_inspect_", "", 1)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            reports[node_id] = {
                "node_id": node_id,
                "report_path": rel(path),
                "errors": [f"invalid bundle inspect report: {type(e).__name__}: {e}"],
            }
            continue

        reports[node_id] = {
            "node_id": data.get("node_id") or node_id,
            "generated_at": data.get("generated_at"),
            "mode": data.get("mode"),
            "bundle_path": data.get("bundle_path"),
            "package_generated_at": data.get("package_generated_at"),
            "device": data.get("device") or {},
            "git": data.get("git") or {},
            "fingerprint": data.get("fingerprint") or {},
            "manifest": data.get("manifest") or {},
            "audit": data.get("audit") or {},
            "commands": data.get("commands") or {},
            "errors": data.get("errors") or [],
            "report_path": rel(path),
        }
    return reports


def load_collect_reports() -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    if not SYNC_DIR.exists():
        return reports
    for path in sorted(SYNC_DIR.glob("last_collect_*.json")):
        node_id = path.stem.replace("last_collect_", "", 1)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            reports[node_id] = {
                "node_id": node_id,
                "report_path": rel(path),
                "errors": [f"invalid collect report: {type(e).__name__}: {e}"],
            }
            continue

        reports[node_id] = {
            "node_id": data.get("node_id") or node_id,
            "generated_at": data.get("generated_at"),
            "mode": data.get("mode"),
            "landing": data.get("landing"),
            "remote": data.get("remote") or {},
            "summary": data.get("summary") or {},
            "remote_inventory": data.get("remote_inventory") or {},
            "conflicts": data.get("conflicts") or [],
            "fetched": data.get("fetched") or [],
            "verification_failed": data.get("verification_failed") or [],
            "errors": data.get("errors") or [],
            "artifact_index": data.get("artifact_index"),
            "report_path": rel(path),
        }
    return reports


def load_diff_reports() -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    if not SYNC_DIR.exists():
        return reports
    for path in sorted(SYNC_DIR.glob("last_diff_*.json")):
        node_id = path.stem.replace("last_diff_", "", 1)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            reports[node_id] = {
                "node_id": node_id,
                "report_path": rel(path),
                "errors": [f"invalid diff report: {type(e).__name__}: {e}"],
            }
            continue

        reports[node_id] = {
            "node_id": data.get("node_id") or node_id,
            "generated_at": data.get("generated_at"),
            "mode": data.get("mode"),
            "landing": data.get("landing"),
            "remote": data.get("remote") or {},
            "summary": data.get("summary") or {},
            "remote_inventory": data.get("remote_inventory") or {},
            "missing": data.get("missing") or [],
            "conflicts": data.get("conflicts") or [],
            "errors": data.get("errors") or [],
            "artifact_index": data.get("artifact_index"),
            "report_path": rel(path),
        }
    return reports


def load_verify_reports() -> Dict[str, Any]:
    reports: Dict[str, Any] = {}
    if not SYNC_DIR.exists():
        return reports
    for path in sorted(SYNC_DIR.glob("last_verify_*.json")):
        node_id = path.stem.replace("last_verify_", "", 1)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            reports[node_id] = {
                "node_id": node_id,
                "report_path": rel(path),
                "errors": [f"invalid verify report: {type(e).__name__}: {e}"],
            }
            continue

        reports[node_id] = {
            "node_id": data.get("node_id") or node_id,
            "generated_at": data.get("generated_at"),
            "mode": data.get("mode"),
            "landing": data.get("landing"),
            "artifact_policy": data.get("artifact_policy") or {},
            "remote": data.get("remote") or {},
            "summary": data.get("summary") or {},
            "remote_inventory": data.get("remote_inventory") or {},
            "verified": data.get("verified") or [],
            "missing": data.get("missing") or [],
            "conflicts": data.get("conflicts") or [],
            "errors": data.get("errors") or [],
            "artifact_index": data.get("artifact_index"),
            "report_path": rel(path),
        }
    return reports


def default_device_id() -> str:
    return os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "unknown"


def build_device_config(device_id: str, role: str, repo_path: str,
                        collector_hint: Optional[str] = None,
                        artifact_policy: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if role not in ROLE_CHOICES:
        raise ValueError(f"role must be one of: {', '.join(ROLE_CHOICES)}")
    data: Dict[str, Any] = {
        "version": 0,
        "device_id": device_id,
        "role": role,
        "repo_path": repo_path,
    }
    if "collector" in role:
        data["peers"] = {}
    if collector_hint:
        data["collector_hint"] = collector_hint
    if artifact_policy:
        data["artifact_policy"] = artifact_policy
    return data


def write_device_config(path: Path, config: Dict[str, Any], *, force: bool = False) -> None:
    if yaml is None:
        raise SystemExit("PyYAML is required. Use the project gnn environment or install pyyaml.")
    if path.exists() and not force:
        raise SystemExit(f"{rel(path)} already exists; use --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(config, sort_keys=False, allow_unicode=False)
    path.write_text(text, encoding="utf-8")


def build_peer_config(role: str, ssh: Optional[str], repo_path: str, landing: str,
                      result_roots: List[str],
                      artifact_policy: Optional[Dict[str, Any]] = None,
                      transport: str = "ssh",
                      python_executable: Optional[str] = None) -> Dict[str, Any]:
    if role not in ROLE_CHOICES:
        raise ValueError(f"role must be one of: {', '.join(ROLE_CHOICES)}")
    mode = normalize_transport(transport)
    roots = result_roots or ["results/runs"]
    data: Dict[str, Any] = {
        "role": role,
        "transport": mode,
        "repo_path": repo_path,
        "landing": landing,
        "result_roots": roots,
    }
    if ssh:
        data["ssh"] = ssh
    elif mode == "local":
        data["ssh"] = "local"
    if python_executable is not None:
        if not isinstance(python_executable, str) or not python_executable.strip():
            raise ValueError("python_executable must be a non-empty string")
        data["python_executable"] = python_executable.strip()
    if artifact_policy:
        data["artifact_policy"] = artifact_policy
    return data


def add_peer_to_device(device: Dict[str, Any], node_id: str, peer: Dict[str, Any],
                       *, force: bool = False) -> Dict[str, Any]:
    if "collector" not in str(device.get("role") or ""):
        raise SystemExit("add-peer requires this device role to be collector or runner+collector")
    peers = device.setdefault("peers", {})
    if not isinstance(peers, dict):
        raise SystemExit("device.yaml field 'peers' must be a mapping")
    if node_id in peers and not force:
        raise SystemExit(f"peer {node_id!r} already exists; use --force to replace it")
    peers[node_id] = peer
    return device


def setup_action(action_id: str, title: str, command: str, *,
                 status: str = "optional", reason: str = "") -> Dict[str, Any]:
    return {
        "id": action_id,
        "title": title,
        "status": status,
        "reason": reason,
        "command": command,
    }


def setup_plan_payload(device: Dict[str, Any], warnings: List[str], *,
                       setup_path: Optional[Path] = None,
                       target_role: Optional[str] = None,
                       device_id: Optional[str] = None,
                       repo_path: Optional[str] = None,
                       collector_id: Optional[str] = None,
                       peer_id: Optional[str] = None,
                       peer_ssh: Optional[str] = None,
                       peer_repo_path: Optional[str] = None,
                       peer_python_executable: Optional[str] = None,
                       peer_local: bool = False,
                       landing: Optional[str] = None,
                       result_roots: Optional[List[str]] = None,
                       artifact_policy: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    current_role = str(device.get("role") or "unknown")
    role = target_role or (current_role if current_role in ROLE_CHOICES else "collector")
    current_device_id = str(device.get("device_id") or default_device_id())
    local_device_id = device_id or current_device_id
    local_repo_path = repo_path or str(device.get("repo_path") or REPO_ROOT)
    config_path = setup_path or DEFAULT_DEVICE_FILE
    base_cmd = syncmate_command_prefix(config_path)
    runner_id = peer_id or "<node_id>"
    peer_transport = "local" if peer_local else "ssh"
    runner_ssh = None if peer_local else peer_ssh or "<ssh_alias>"
    runner_repo = peer_repo_path or ("<local_runner_repo_path>" if peer_local else "<remote_repo_path>")
    runner_python = peer_python_executable or "python"
    roots = result_roots or ["results/runs"]
    local_landing = landing or f"results/runs/{runner_id}"
    collector_hint = collector_id or local_device_id
    policy = artifact_policy if artifact_policy is not None else device.get("artifact_policy")
    artifact_names = tuple(apply_artifact_policy(list(ARTIFACT_NAMES), policy))

    config_exists = not warnings
    known_peers = sorted((device.get("peers") or {}).keys())
    init_parts = [
        *base_cmd, "init-device",
        "--device-id", local_device_id,
        "--role", role,
        "--repo-path", local_repo_path,
        "--artifact-include", *artifact_names,
    ]
    if "runner" in role and collector_hint:
        init_parts.extend(["--collector-hint", collector_hint])
    init_status = "not-needed" if config_exists and current_role == role else "needed"
    init_reason = "device setup is missing or role differs" if init_status == "needed" else "current device.yaml already matches the target role"
    if config_exists and init_status == "needed":
        init_parts.append("--force")

    actions = [
        setup_action(
            "init-current",
            "Initialize this checkout",
            command_line(init_parts),
            status=init_status,
            reason=init_reason,
        )
    ]

    if "collector" in role:
        if not peer_local:
            runner_init_parts = [
                runner_python, "scripts/syncmate/syncmate.py", "init-device",
                "--device-id", runner_id,
                "--role", "runner",
                "--repo-path", runner_repo,
                "--collector-hint", local_device_id,
                "--artifact-include", *artifact_names,
            ]
            remote_init_inner = f"cd {command_arg(runner_repo)} && {command_line(runner_init_parts)}"
            remote_init = f"ssh {command_arg(runner_ssh)} \"{remote_init_inner}\""
            actions.append(setup_action(
                "init-runner",
                "Initialize the runner peer",
                remote_init,
                status="optional",
                reason="run this on the collector when SSH can reach the runner",
            ))
        add_peer_parts = [
            *base_cmd, "add-peer", runner_id,
            "--repo-path", runner_repo,
            "--landing", local_landing,
        ]
        if peer_local:
            add_peer_parts.insert(len(base_cmd) + 2, "--local")
        else:
            add_peer_parts[len(base_cmd) + 2:len(base_cmd) + 2] = ["--ssh", runner_ssh]
            if runner_python != "python":
                add_peer_parts.extend(["--python-executable", runner_python])
        for root in roots:
            add_peer_parts.extend(["--result-root", root])
        add_peer_parts.extend(["--artifact-include", *artifact_names])
        peer_known = runner_id in known_peers
        actions.append(setup_action(
            "add-peer",
            "Register the local runner checkout" if peer_local else "Register the runner on this collector",
            command_line(add_peer_parts),
            status="not-needed" if peer_known else "needed",
            reason=(
                "peer already configured" if peer_known
                else "collector needs a local runner checkout before sync" if peer_local
                else "collector needs at least one runner peer before sync"
            ),
        ))
        actions.extend([
            setup_action(
                "preflight",
                "Validate the sync setup without SSH",
                command_line([*base_cmd, "preflight", runner_id]),
                status="optional",
                reason="checks peer config, landing path, result roots, and artifact policy before any remote contact",
            ),
            setup_action(
                "sync-dry-run",
                "Probe the peer without collecting",
                command_line([*base_cmd, "sync", runner_id, "--dry-run"]),
                status="optional",
                reason="checks peer status, result manifest, and diff without copying artifacts",
            ),
            setup_action(
                "sync-apply",
                "Collect and verify current results",
                command_line([*base_cmd, "sync", runner_id]),
                status="optional",
                reason="runs the full incremental collection and checksum acceptance path",
            ),
        ])
    else:
        actions.extend([
            setup_action(
                "runner-status",
                "Show runner status for the collector",
                command_line([*base_cmd, "status", "--json", "--no-write-state"]),
                status="optional",
                reason="safe command a collector can run over SSH",
            ),
            setup_action(
                "runner-manifest",
                "Emit runner result manifest",
                command_line([
                    *base_cmd, "manifest",
                    "--json", "--roots", *roots,
                    "--include", *artifact_names,
                ]),
                status="optional",
                reason="safe command a collector uses for checksum diff",
            ),
        ])

    missing_inputs = []
    missing_candidates = {
        "peer_id": runner_id,
        "peer_repo_path": runner_repo,
    }
    if not peer_local:
        missing_candidates["peer_ssh"] = runner_ssh
    for key, value in missing_candidates.items():
        if str(value).startswith("<") and str(value).endswith(">"):
            missing_inputs.append(key)

    return {
        "generated_at": now_iso(),
        "mode": "setup-plan",
        "setup_file": rel(config_path),
        "current": {
            "config_exists": config_exists,
            "device_id": current_device_id,
            "role": current_role,
            "peers": known_peers,
            "warnings": warnings,
        },
        "target": {
            "role": role,
            "device_id": local_device_id,
            "repo_path": local_repo_path,
            "collector_id": collector_hint if "runner" in role else local_device_id,
            "peer_id": runner_id,
            "peer_transport": peer_transport,
            "peer_ssh": runner_ssh,
            "peer_repo_path": runner_repo,
            "peer_python_executable": runner_python,
            "landing": local_landing,
            "result_roots": roots,
            "artifact_policy": artifact_policy_payload(artifact_names),
        },
        "missing_inputs": missing_inputs,
        "actions": actions,
        "files": {
            "setup": rel(config_path),
            "setup_plan": rel(setup_plan_file()),
        },
    }


def render_setup_plan_markdown(data: Dict[str, Any]) -> str:
    current = data.get("current") or {}
    target = data.get("target") or {}
    lines = [
        "# Syncmate Setup Plan",
        "",
        f"Generated: {data.get('generated_at')}",
        f"Current: device={current.get('device_id')} role={current.get('role')} "
        f"config_exists={current.get('config_exists')} peers={','.join(current.get('peers') or []) or 'none'}",
        f"Target: role={target.get('role')} device={target.get('device_id')} "
        f"peer={target.get('peer_id')} transport={target.get('peer_transport') or 'ssh'} "
        f"landing={target.get('landing')}",
    ]
    warnings = current.get("warnings") or []
    if warnings:
        lines.extend(["", "## Warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
    missing = data.get("missing_inputs") or []
    if missing:
        lines.extend(["", "## Fill These Values", ""])
        for item in missing:
            lines.append(f"- {item}")
    lines.extend(["", "## Commands", ""])
    for action in data.get("actions") or []:
        lines.append(f"### {action.get('title')}")
        lines.append("")
        lines.append(f"Status: {action.get('status')}")
        if action.get("reason"):
            lines.append(f"Reason: {action.get('reason')}")
        lines.append("")
        lines.append("```bash")
        lines.append(action.get("command") or "")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def write_setup_plan(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = setup_plan_file()
    out.write_text(render_setup_plan_markdown(data), encoding="utf-8")
    return out


def is_safe_repo_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.replace("\\", "/")
    if text.startswith("/") or text.startswith("~"):
        return False
    if len(text) >= 3 and text[1] == ":" and text[2] == "/":
        return False
    return ".." not in [part for part in text.split("/") if part]


def safe_repo_path(value: Any) -> Optional[Path]:
    if not is_safe_repo_relative_path(value):
        return None
    target = (REPO_ROOT / str(value)).resolve()
    try:
        target.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return None
    return target


def normalize_git_id(value: Any) -> str:
    text = str(value or "").strip()
    return "" if not text or text == "unknown" else text


def git_ids_match(local_id: Any, remote_id: Any) -> bool:
    local = normalize_git_id(local_id)
    remote = normalize_git_id(remote_id)
    if not local or not remote:
        return True
    return local.startswith(remote) or remote.startswith(local)


def report_remote_git_short(report: Dict[str, Any]) -> str:
    remote_git = (report.get("remote") or {}).get("git") or {}
    if not isinstance(remote_git, dict):
        return ""
    return normalize_git_id(remote_git.get("short_sha") or str(remote_git.get("sha") or "")[:7])


def report_remote_source(report: Dict[str, Any]) -> str:
    remote = report.get("remote") if isinstance(report.get("remote"), dict) else {}
    return str(remote.get("source") or remote.get("transport") or "").strip()


def report_bundle_path(report: Dict[str, Any], node_id: Optional[str] = None) -> str:
    remote = report.get("remote") if isinstance(report.get("remote"), dict) else {}
    path = remote.get("bundle_path") or report.get("bundle_path")
    if path:
        return str(path)
    suffix = f"_{node_id}" if node_id else ""
    return f"<bundle{suffix}.zip>"


def is_bundle_diff_report(report: Dict[str, Any]) -> bool:
    mode = str(report.get("mode") or "")
    return report_remote_source(report) == "bundle" or mode.startswith("import-bundle")


def import_bundle_command(report: Dict[str, Any], node_id: str, *, overwrite: bool = False,
                          dry_run: bool = False, write_plan: bool = False) -> str:
    parts: List[Any] = ["python", "scripts/syncmate/syncmate.py", "import-bundle", report_bundle_path(report, node_id)]
    if overwrite:
        parts.append("--overwrite")
    if dry_run:
        parts.append("--dry-run")
    if write_plan:
        parts.append("--write-plan")
    return command_line(parts)


def peer_config_diagnostics(device: Dict[str, Any]) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    peer_configs = device.get("peer_configs") or {}
    if not isinstance(peer_configs, dict):
        return diagnostics

    base_artifact_names = list(ARTIFACT_NAMES)
    global_artifact_policy_ok = True
    if device.get("artifact_policy") is not None:
        try:
            base_artifact_names = apply_artifact_policy(base_artifact_names, device.get("artifact_policy"))
        except SystemExit as exc:
            global_artifact_policy_ok = False
            diagnostics.append({
                "severity": "error",
                "code": "artifact-policy-invalid",
                "node": device.get("id") or "local",
                "message": f"Device artifact_policy is invalid: {exc}.",
                "action": "Use artifact_policy include/exclude lists with file names such as attack.json or _meta.json.",
            })

    landings: Dict[str, List[str]] = {}
    for node, peer in sorted(peer_configs.items()):
        if not isinstance(peer, dict):
            diagnostics.append({
                "severity": "error",
                "code": "peer-config-invalid",
                "node": node,
                "message": f"Peer {node} config must be a mapping.",
                "action": "Recreate this peer with add-peer or fix .syncmate/device.yaml.",
            })
            continue

        try:
            transport = peer_transport(peer)
        except SystemExit as exc:
            transport = "invalid"
            diagnostics.append({
                "severity": "error",
                "code": "peer-transport-invalid",
                "node": node,
                "message": f"Peer {node} transport is invalid: {exc}.",
                "action": "Use transport: ssh or transport: local.",
            })

        required_fields = ["repo_path"] if transport == "local" else ["ssh", "repo_path"]
        for field in required_fields:
            if not isinstance(peer.get(field), str) or not peer.get(field, "").strip():
                diagnostics.append({
                    "severity": "error",
                    "code": "peer-config-missing-field",
                    "node": node,
                    "message": f"Peer {node} is missing required field {field}.",
                    "action": f"Run add-peer {node} --force with repo path and {'--local' if transport == 'local' else 'ssh'}.",
                })

        python_executable = peer.get("python_executable")
        if python_executable is not None and (
                not isinstance(python_executable, str) or not python_executable.strip()):
            diagnostics.append({
                "severity": "error",
                "code": "peer-python-invalid",
                "node": node,
                "message": f"Peer {node} python_executable must be a non-empty string.",
                "action": f"Run add-peer {node} --force with --python-executable <remote-python>.",
            })

        role = peer.get("role", "runner")
        if role not in ROLE_CHOICES:
            diagnostics.append({
                "severity": "warn",
                "code": "peer-role-invalid",
                "node": node,
                "message": f"Peer {node} has unknown role {role!r}.",
                "action": f"Set role to one of: {', '.join(ROLE_CHOICES)}.",
            })

        if global_artifact_policy_ok and peer.get("artifact_policy") is not None:
            try:
                apply_artifact_policy(base_artifact_names, peer.get("artifact_policy"))
            except SystemExit as exc:
                diagnostics.append({
                    "severity": "error",
                    "code": "peer-artifact-policy-invalid",
                    "node": node,
                    "message": f"Peer {node} artifact_policy is invalid: {exc}.",
                    "action": "Use peer artifact_policy include/exclude lists with file names only.",
                })

        landing = peer.get("landing") or f"results/runs/{node}"
        if not is_safe_repo_relative_path(landing):
            diagnostics.append({
                "severity": "error",
                "code": "peer-landing-unsafe",
                "node": node,
                "message": f"Peer {node} landing must be a repo-relative path without '..': {landing!r}.",
                "action": f"Use add-peer {node} --force --landing results/runs/{node}.",
            })
        else:
            landings.setdefault(landing, []).append(node)

        roots = peer.get("result_roots") or ["results/runs"]
        if not isinstance(roots, list) or not all(isinstance(root, str) and root.strip() for root in roots):
            diagnostics.append({
                "severity": "error",
                "code": "peer-result-roots-invalid",
                "node": node,
                "message": f"Peer {node} result_roots must be a list of non-empty strings.",
                "action": f"Use add-peer {node} --force and repeat --result-root for each remote root.",
            })
        elif any(not is_safe_repo_relative_path(root) for root in roots):
            diagnostics.append({
                "severity": "warn",
                "code": "peer-result-root-unsafe",
                "node": node,
                "message": f"Peer {node} has result_roots outside the repo-relative convention.",
                "action": "Prefer roots like results/runs or results/runs/<cell>.",
            })

    for landing, nodes in sorted(landings.items()):
        if len(nodes) > 1:
            diagnostics.append({
                "severity": "error",
                "code": "peer-landing-duplicate",
                "node": ",".join(nodes),
                "message": f"Multiple peers share landing {landing}: {', '.join(nodes)}.",
                "action": "Give each peer a separate landing path such as results/runs/<node_id>.",
            })
    return diagnostics


def preflight_check(severity: str, code: str, message: str, *,
                    action: Optional[str] = None,
                    node: Optional[str] = None) -> Dict[str, Any]:
    item = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if action:
        item["action"] = action
    if node:
        item["node"] = node
    return item


def preflight_status_from_checks(checks: List[Dict[str, Any]]) -> str:
    if any(item.get("severity") == "error" for item in checks):
        return "blocked"
    if any(item.get("severity") == "warn" for item in checks):
        return "warn"
    return "ready"


def selected_preflight_nodes(peers: Dict[str, Any], node_ids: List[str]) -> Tuple[List[str], List[str]]:
    selected = node_ids or sorted(peers)
    known = [node_id for node_id in selected if node_id in peers]
    unknown = [node_id for node_id in selected if node_id not in peers]
    return known, unknown


def preflight_peer_payload(device: Dict[str, Any], node_id: str, peer: Any,
                           config_path: Path) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    base_cmd = syncmate_command_prefix(config_path)
    if not isinstance(peer, dict):
        checks.append(preflight_check(
            "error",
            "peer-config-invalid",
            f"Peer {node_id} config must be a mapping.",
            action="Recreate this peer with add-peer or fix .syncmate/device.yaml.",
            node=node_id,
        ))
        return {
            "node_id": node_id,
            "known": True,
            "ready": False,
            "status": "blocked",
            "checks": checks,
            "commands": {},
        }

    role = peer.get("role", "runner")
    try:
        transport = peer_transport(peer)
    except SystemExit as exc:
        transport = "invalid"
        checks.append(preflight_check(
            "error",
            "peer-transport-invalid",
            f"Peer {node_id} transport is invalid: {exc}.",
            action="Use transport: ssh or transport: local.",
            node=node_id,
        ))
    ssh = peer.get("ssh")
    repo_path = peer.get("repo_path")
    try:
        python_executable = peer_python_executable(peer)
    except SystemExit as exc:
        python_executable = "python"
        checks.append(preflight_check(
            "error",
            "peer-python-invalid",
            f"Peer {node_id} python_executable is invalid: {exc}.",
            action=f"Run add-peer {node_id} --force with --python-executable <remote-python>.",
            node=node_id,
        ))
    landing = peer.get("landing") or f"results/runs/{node_id}"
    roots = peer.get("result_roots") or ["results/runs"]
    artifact_names: Tuple[str, ...] = ()

    if transport != "local" and (not isinstance(ssh, str) or not ssh.strip()):
        checks.append(preflight_check(
            "error",
            "peer-ssh-missing",
            f"Peer {node_id} is missing ssh.",
            action=f"Run add-peer {node_id} --force with --ssh and --repo-path.",
            node=node_id,
        ))
    elif transport == "local" and isinstance(repo_path, str) and repo_path.strip():
        local_root = resolve_local_repo_root(repo_path)
        if not local_root.exists():
            checks.append(preflight_check(
                "error",
                "peer-local-repo-missing",
                f"Peer {node_id} local repo_path does not exist: {local_root}.",
                action=f"Create the local runner checkout or update add-peer {node_id} --force --local --repo-path.",
                node=node_id,
            ))
        elif not local_root.is_dir():
            checks.append(preflight_check(
                "error",
                "peer-local-repo-not-directory",
                f"Peer {node_id} local repo_path is not a directory: {local_root}.",
                action=f"Point add-peer {node_id} --force --local --repo-path at a checkout directory.",
                node=node_id,
            ))
    if not isinstance(repo_path, str) or not repo_path.strip():
        checks.append(preflight_check(
            "error",
            "peer-repo-path-missing",
            f"Peer {node_id} is missing repo_path.",
            action=f"Run add-peer {node_id} --force with --ssh and --repo-path.",
            node=node_id,
        ))
    if role not in ROLE_CHOICES:
        checks.append(preflight_check(
            "warn",
            "peer-role-invalid",
            f"Peer {node_id} has unknown role {role!r}.",
            action=f"Set role to one of: {', '.join(ROLE_CHOICES)}.",
            node=node_id,
        ))
    if not is_safe_repo_relative_path(landing):
        checks.append(preflight_check(
            "error",
            "peer-landing-unsafe",
            f"Peer {node_id} landing must be a repo-relative path without '..': {landing!r}.",
            action=f"Use add-peer {node_id} --force --landing results/runs/{node_id}.",
            node=node_id,
        ))
    if not isinstance(roots, list) or not all(isinstance(root, str) and root.strip() for root in roots):
        checks.append(preflight_check(
            "error",
            "peer-result-roots-invalid",
            f"Peer {node_id} result_roots must be a list of non-empty strings.",
            action=f"Use add-peer {node_id} --force and repeat --result-root for each remote root.",
            node=node_id,
        ))
    elif any(not is_safe_repo_relative_path(root) for root in roots):
        checks.append(preflight_check(
            "error",
            "peer-result-root-unsafe",
            f"Peer {node_id} has unsafe result_roots outside the repo-relative convention.",
            action="Use roots like results/runs or results/runs/<cell>.",
            node=node_id,
        ))

    try:
        artifact_names = artifact_names_for_peer(device, peer)
    except SystemExit as exc:
        checks.append(preflight_check(
            "error",
            "peer-artifact-policy-invalid",
            f"Peer {node_id} artifact policy is invalid: {exc}.",
            action="Use artifact_policy include/exclude lists with file names only.",
            node=node_id,
        ))
        artifact_names = ()

    if not checks:
        checks.append(preflight_check(
            "ok",
            "peer-ready",
            f"Peer {node_id} is ready for remote-status, diff, collect, verify, and results extraction.",
            node=node_id,
        ))

    status = preflight_status_from_checks(checks)
    commands = {
        "remote_status": command_line([*base_cmd, "remote-status", node_id, "--apply"]),
        "diff": command_line([*base_cmd, "collect", node_id, "--diff"]),
        "collect": command_line([*base_cmd, "collect", node_id, "--apply"]),
        "verify": command_line([*base_cmd, "verify", node_id, "--apply"]),
        "sync": command_line([*base_cmd, "sync", node_id]),
        "results": command_line([*base_cmd, "results", "--write", "--check"]),
        "gate": command_line([*base_cmd, "gate", "--require-verify"]),
    }
    return {
        "node_id": node_id,
        "known": True,
        "ready": status != "blocked",
        "status": status,
        "role": role,
        "transport": transport,
        "ssh": ssh,
        "repo_path": repo_path,
        "python_executable": python_executable,
        "landing": landing,
        "local_landing": rel(REPO_ROOT / landing) if is_safe_repo_relative_path(landing) else landing,
        "result_roots": roots,
        "artifact_policy": artifact_policy_payload(artifact_names),
        "automation": [
            "remote-status",
            "manifest-diff",
            "incremental-collect",
            "checksum-verify",
            "trusted-results",
        ],
        "checks": checks,
        "commands": commands,
    }


def preflight_payload(device: Dict[str, Any], warnings: List[str], *,
                      config_path: Path = DEFAULT_DEVICE_FILE,
                      node_ids: Optional[List[str]] = None,
                      require_sync_targets: bool = False) -> Dict[str, Any]:
    node_ids = node_ids or []
    role = str(device.get("role") or "unknown")
    device_id = str(device.get("device_id") or default_device_id())
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    base_cmd = syncmate_command_prefix(config_path)
    device_checks: List[Dict[str, Any]] = []

    for warning in warnings:
        device_checks.append(preflight_check(
            "error",
            "setup-missing",
            warning,
            action=command_line([*base_cmd, "setup-plan"]),
        ))
    if role == "unknown":
        device_checks.append(preflight_check(
            "error",
            "device-role-unknown",
            "Device role is unknown.",
            action=command_line([*base_cmd, "setup-plan", "--role", "collector"]),
        ))
    elif role not in ROLE_CHOICES:
        device_checks.append(preflight_check(
            "error",
            "device-role-invalid",
            f"Device role {role!r} is invalid.",
            action=f"Set role to one of: {', '.join(ROLE_CHOICES)}.",
        ))
    elif require_sync_targets and "collector" not in role:
        device_checks.append(preflight_check(
            "error",
            "device-not-collector",
            f"Device role {role!r} cannot run collector sync automation.",
            action=command_line([*base_cmd, "setup-plan", "--role", "collector"]),
        ))

    try:
        device_artifacts = artifact_names_for_peer(device, None)
    except SystemExit as exc:
        device_artifacts = ()
        device_checks.append(preflight_check(
            "error",
            "artifact-policy-invalid",
            f"Device artifact_policy is invalid: {exc}.",
            action="Use artifact_policy include/exclude lists with file names only.",
        ))

    known_nodes, unknown_nodes = selected_preflight_nodes(peers, node_ids)
    peer_payloads: Dict[str, Any] = {}
    for node_id in unknown_nodes:
        peer_payloads[node_id] = {
            "node_id": node_id,
            "known": False,
            "ready": False,
            "status": "blocked",
            "checks": [
                preflight_check(
                    "error",
                    "peer-unknown",
                    f"Unknown peer {node_id}.",
                    action=command_line([*base_cmd, "add-peer", node_id, "--ssh", "<ssh_alias>", "--repo-path", "<remote_repo>"]),
                    node=node_id,
                )
            ],
            "commands": {},
        }

    if ("collector" in role or require_sync_targets) and not peers:
        device_checks.append(preflight_check(
            "error",
            "collector-has-no-peers",
            "Collector sync automation has no configured peers.",
            action=command_line([*base_cmd, "add-peer", "<node_id>", "--ssh", "<ssh_alias>", "--repo-path", "<remote_repo>"]),
        ))
    elif "collector" in role and not known_nodes and peers and not node_ids:
        device_checks.append(preflight_check(
            "warn",
            "collector-no-selection",
            "Collector has peers, but no peer was selected for this preflight.",
            action=command_line([*base_cmd, "preflight", *sorted(peers)]),
        ))

    for node_id in known_nodes:
        peer_payloads[node_id] = preflight_peer_payload(device, node_id, peers[node_id], config_path)

    if "collector" not in role and not node_ids and role in ROLE_CHOICES:
        device_checks.append(preflight_check(
            "ok",
            "runner-local-ready",
            "Runner-side setup is ready to answer status and manifest commands; collector-side sync needs peers on a collector device.",
            action=command_line([*base_cmd, "status", "--json", "--no-write-state"]),
        ))
    elif not device_checks:
        device_checks.append(preflight_check(
            "ok",
            "device-ready",
            "Device setup is ready for Syncmate automation.",
        ))

    all_checks = list(device_checks)
    for peer in peer_payloads.values():
        all_checks.extend(peer.get("checks") or [])

    peer_values = list(peer_payloads.values())
    ready_peers = sum(1 for peer in peer_values if peer.get("ready"))
    blocked_peers = sum(1 for peer in peer_values if not peer.get("ready"))
    errors = [item for item in all_checks if item.get("severity") == "error"]
    warnings_out = [item for item in all_checks if item.get("severity") == "warn"]
    status = preflight_status_from_checks(all_checks)
    next_commands = []
    for node_id in known_nodes:
        peer = peer_payloads.get(node_id) or {}
        if peer.get("ready") and peer.get("commands"):
            next_commands.append({
                "node_id": node_id,
                "command": peer["commands"]["sync"],
                "reason": "run full incremental collect, checksum verify, and trusted results extraction",
            })
    if status == "blocked":
        for item in errors[:5]:
            if item.get("action"):
                next_commands.append({
                    "command": item["action"],
                    "reason": item.get("message"),
                })

    return {
        "generated_at": now_iso(),
        "mode": "preflight",
        "setup_file": rel(config_path),
        "status": status,
        "device": {
            "id": device_id,
            "role": role,
            "repo_path": device.get("repo_path"),
            "ready": not any(item.get("severity") == "error" for item in device_checks),
            "artifact_policy": artifact_policy_payload(device_artifacts),
            "warnings": warnings,
            "checks": device_checks,
        },
        "summary": {
            "status": status,
            "peers": len(peer_values),
            "ready": ready_peers,
            "blocked": blocked_peers,
            "unknown": len(unknown_nodes),
            "errors": len(errors),
            "warnings": len(warnings_out),
        },
        "peers": peer_payloads,
        "next_commands": next_commands,
    }


def print_preflight(data: Dict[str, Any], *, limit: int = 8) -> None:
    summary = data.get("summary") or {}
    device = data.get("device") or {}
    print(
        f"syncmate preflight: {summary.get('status')} "
        f"peers={summary.get('peers', 0)} ready={summary.get('ready', 0)} "
        f"blocked={summary.get('blocked', 0)} errors={summary.get('errors', 0)} "
        f"warnings={summary.get('warnings', 0)}"
    )
    print(f"  device: {device.get('id')} ({device.get('role')}) setup={data.get('setup_file')}")
    for item in (device.get("checks") or [])[:max(0, limit)]:
        if item.get("severity") == "ok":
            continue
        print(f"  [{item.get('severity')}] {item.get('code')}: {item.get('message')}")
        if item.get("action"):
            print(f"    action: {item.get('action')}")

    peers = data.get("peers") or {}
    if peers:
        print("  peers:")
        for node_id, peer in sorted(peers.items()):
            artifacts = ", ".join((peer.get("artifact_policy") or {}).get("include") or [])
            roots = ", ".join(peer.get("result_roots") or [])
            print(
                f"    - {node_id}: {peer.get('status')} landing={peer.get('landing')} "
                f"roots={roots or 'none'} artifacts={artifacts or 'none'}"
            )
            shown = 0
            for item in peer.get("checks") or []:
                if item.get("severity") == "ok":
                    continue
                if shown >= limit:
                    break
                shown += 1
                print(f"      [{item.get('severity')}] {item.get('code')}: {item.get('message')}")
                if item.get("action"):
                    print(f"        action: {item.get('action')}")

    commands = data.get("next_commands") or []
    if commands:
        print("  next:")
        for item in commands[:max(0, limit)]:
            print(f"    {item.get('command')}")
    if data.get("report_path"):
        print(f"  report: {data.get('report_path')}")


def write_preflight_report(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = last_preflight_file()
    data["report_path"] = rel(out)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def maybe_write_preflight_report(data: Dict[str, Any], *, save: bool) -> Optional[Path]:
    if not save:
        return None
    return write_preflight_report(data)


def preflight_error_messages(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for item in ((data.get("device") or {}).get("checks") or []):
        if item.get("severity") == "error":
            errors.append(f"{item.get('code')}: {item.get('message')}")
    for node_id, peer in sorted((data.get("peers") or {}).items()):
        for item in peer.get("checks") or []:
            if item.get("severity") == "error":
                errors.append(f"{node_id}: {item.get('code')}: {item.get('message')}")
    return errors


def blocked_by_preflight_payload(command: str, preflight: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "generated_at": preflight.get("generated_at") or now_iso(),
        "mode": command,
        "status": "blocked",
        "preflight": preflight,
        "peer_results": {},
        "errors": preflight_error_messages(preflight),
    }


def print_blocked_by_preflight(command: str, preflight: Dict[str, Any], *, limit: int = 8) -> None:
    print(f"syncmate {command}: blocked by preflight")
    print_preflight(preflight, limit=limit)


def diagnostics_for_snapshot(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    device = snapshot.get("device", {})
    git = snapshot.get("git", {})
    results = snapshot.get("results", {})
    remote_status = snapshot.get("remote_status") or {}
    bundle_inspect_reports = snapshot.get("bundle_inspect_reports") or {}
    diff_reports = snapshot.get("diff_reports") or {}
    collect_reports = snapshot.get("collect_reports") or {}
    verify_reports = snapshot.get("verify_reports") or {}
    artifact_index = snapshot.get("artifact_index") or {}
    local_git_short = git.get("short_sha")

    for warning in device.get("setup_warnings") or []:
        diagnostics.append({
            "severity": "warn",
            "code": "setup-warning",
            "message": warning,
            "action": "Run python scripts/syncmate/syncmate.py setup-plan, then run the matching init-device command.",
        })

    if device.get("role") == "unknown":
        diagnostics.append({
            "severity": "warn",
            "code": "unknown-role",
            "message": "Device role is unknown.",
            "action": "Run python scripts/syncmate/syncmate.py setup-plan --role collector, then run init-device with --force if replacing the setup is intentional.",
        })

    diagnostics.extend(peer_config_diagnostics(device))

    if git.get("dirty"):
        diagnostics.append({
            "severity": "info",
            "code": "dirty-worktree",
            "message": f"Worktree has {len(git.get('status_short') or [])} changed path(s).",
            "action": "Review git status before treating this device as a reproducible runner.",
        })

    if not results.get("nodes"):
        diagnostics.append({
            "severity": "info",
            "code": "no-results",
            "message": "No json/meta result artifacts were found under results/runs.",
            "action": "Run experiments on a runner or use collect --apply from a collector.",
        })

    for error in artifact_index.get("errors") or []:
        diagnostics.append({
            "severity": "error",
            "code": "artifact-index-invalid",
            "message": error,
            "action": "Delete or repair .syncmate/artifact_index.json, then rerun verify <node_id> --apply.",
        })

    for peer in incomplete_inventory_peers(artifact_index, configured_peers(snapshot)):
        missing = ", ".join(f"{name}={count}" for name, count in peer["missing_counts"].items())
        diagnostics.append({
            "severity": "warn",
            "code": "artifact-inventory-incomplete",
            "node": peer["node_id"],
            "message": f"{peer['node_id']} trusted inventory has {peer['incomplete']} incomplete experiment leaf/leaves"
                       f"{f' ({missing})' if missing else ''}.",
            "action": f"Run python scripts/syncmate/syncmate.py inventory {peer['node_id']} --only-incomplete, "
                      "then rerun collect/verify after fixing missing result artifacts.",
        })

    for entry in orphaned_sync_entries(snapshot):
        node_id = entry.get("node_id")
        kind = entry.get("kind")
        path = entry.get("path") or ".syncmate/"
        if kind == "artifact_index":
            diagnostics.append({
                "severity": "warn",
                "code": "orphaned-artifact-index",
                "node": node_id,
                "message": f"Artifact index contains entry for unconfigured peer {node_id}.",
                "action": "Run python scripts/syncmate/syncmate.py archive-orphans to preview safe archival.",
            })
        else:
            diagnostics.append({
                "severity": "warn",
                "code": "orphaned-sync-report",
                "node": node_id,
                "report_type": kind,
                "message": f"Saved {kind} report exists for unconfigured peer {node_id}: {path}.",
                "action": "Run python scripts/syncmate/syncmate.py archive-orphans to preview safe archival.",
            })

    for node, info in sorted((results.get("nodes") or {}).items()):
        issues = set(info.get("issues") or [])
        if "missing-artifacts" in issues:
            missing = ", ".join(f"{k}={v}" for k, v in sorted((info.get("missing") or {}).items()))
            diagnostics.append({
                "severity": "error",
                "code": "missing-artifacts",
                "node": node,
                "message": f"{node} has incomplete artifact leaves: {missing}.",
                "action": "Re-run or recollect the affected cells before aggregation.",
            })
        if "multiple-git-shas" in issues:
            shas = ", ".join(f"{k}:{v}" for k, v in sorted((info.get("git_shas") or {}).items()))
            diagnostics.append({
                "severity": "warn",
                "code": "multiple-git-shas",
                "node": node,
                "message": f"{node} contains artifacts from multiple git SHAs: {shas}.",
                "action": "Confirm this is intentional; otherwise recollect into a fresh node landing directory.",
            })
        if "bare-results-layout" in issues:
            diagnostics.append({
                "severity": "warn",
                "code": "bare-results-layout",
                "node": node,
                "message": "Bare results live directly under results/runs/<cell>.",
                "action": "Prefer collector landing results/runs/<node_id>/<cell> for future imports.",
            })
        if "nested-results-wrapper" in issues:
            diagnostics.append({
                "severity": "warn",
                "code": "nested-results-wrapper",
                "node": node,
                "message": f"{node} contains a nested results/runs wrapper from an older extraction.",
                "action": "Leave it read-only or recollect the source into a clean node landing when convenient.",
            })

    for peer in sorted(device.get("peers") or []):
        if peer not in remote_status:
            diagnostics.append({
                "severity": "warn",
                "code": "remote-status-missing",
                "node": peer,
                "message": f"No saved remote status report exists for configured peer {peer}.",
                "action": f"Run python scripts/syncmate/syncmate.py remote-status {peer} --apply.",
            })

    for peer, report in sorted(remote_status.items()):
        errors = report.get("errors") or []
        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "warn",
                "code": "remote-status-stale",
                "node": peer,
                "message": f"{peer} remote status report is stale or has an invalid timestamp: {report.get('generated_at')}.",
                "action": f"Run python scripts/syncmate/syncmate.py remote-status {peer} --apply or refresh {peer}.",
            })
        if errors:
            diagnostics.append({
                "severity": "error",
                "code": "remote-status-error",
                "node": peer,
                "message": f"{peer} remote status report has error(s): {'; '.join(errors)}.",
                "action": f"Fix SSH/repo setup, then rerun remote-status {peer} --apply.",
            })
            continue

        summary = report.get("summary") or {}
        remote_git_short = summary.get("git_short_sha")
        if not git_ids_match(local_git_short, remote_git_short):
            diagnostics.append({
                "severity": "error",
                "code": "remote-git-mismatch",
                "node": peer,
                "message": f"{peer} reports git {remote_git_short}, but local git is {local_git_short}.",
                "action": f"Synchronize tracked files with git on both devices, then rerun remote-status {peer} --apply.",
            })
        if summary.get("git_dirty"):
            diagnostics.append({
                "severity": "warn",
                "code": "remote-dirty-worktree",
                "node": peer,
                "message": f"{peer} reports a dirty worktree at {summary.get('git_short_sha')}.",
                "action": "Review remote git status before treating new artifacts as reproducible.",
            })

        remote_results = ((report.get("snapshot") or {}).get("results") or {})
        for remote_node, info in sorted((remote_results.get("nodes") or {}).items()):
            issues = set(info.get("issues") or [])
            if "missing-artifacts" in issues:
                missing = ", ".join(f"{k}={v}" for k, v in sorted((info.get("missing") or {}).items()))
                diagnostics.append({
                    "severity": "error",
                    "code": "remote-missing-artifacts",
                    "node": peer,
                    "remote_node": remote_node,
                    "message": f"{peer}/{remote_node} has incomplete artifact leaves: {missing}.",
                    "action": f"Re-run failed cells on {peer}, then rerun remote-status {peer} --apply.",
                })
            if "multiple-git-shas" in issues:
                shas = ", ".join(f"{k}:{v}" for k, v in sorted((info.get("git_shas") or {}).items()))
                diagnostics.append({
                    "severity": "warn",
                    "code": "remote-multiple-git-shas",
                    "node": peer,
                    "remote_node": remote_node,
                    "message": f"{peer}/{remote_node} reports artifacts from multiple git SHAs: {shas}.",
                    "action": f"Confirm this is intentional before collecting from {peer}.",
                })

    diagnostics.extend(fingerprint_compare_diagnostics(snapshot))

    for peer, report in sorted(bundle_inspect_reports.items()):
        errors = report.get("errors") or []
        audit = report.get("audit") or {}
        audit_errors = audit.get("errors") or []
        audit_warnings = audit.get("warnings") or []
        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "warn",
                "code": "bundle-inspect-stale",
                "node": peer,
                "message": f"{peer} bundle inspect report is stale or has an invalid timestamp: {report.get('generated_at')}.",
                "action": f"Rerun inspect-bundle on the copied bundle with --write before importing from {peer}.",
            })
        if errors or audit.get("status") == "invalid" or audit_errors:
            messages = errors or audit_errors or [f"audit status={audit.get('status')}"]
            diagnostics.append({
                "severity": "error",
                "code": "bundle-inspect-error",
                "node": peer,
                "message": f"{peer} bundle inspect report has error(s): {'; '.join(str(item) for item in messages)}.",
                "action": f"Inspect {report.get('report_path')}, rebuild/copy the bundle, then rerun inspect-bundle --write.",
            })
        if audit_warnings:
            diagnostics.append({
                "severity": "warn",
                "code": "bundle-inspect-warning",
                "node": peer,
                "message": f"{peer} bundle inspect report has warning(s): {'; '.join(str(item) for item in audit_warnings)}.",
                "action": f"Review {report.get('report_path')} before running import-bundle.",
            })
        bundle_git_short = ((report.get("git") or {}).get("short_sha"))
        if not git_ids_match(local_git_short, bundle_git_short):
            diagnostics.append({
                "severity": "error",
                "code": "bundle-inspect-git-mismatch",
                "node": peer,
                "message": f"{peer} inspected bundle used git {bundle_git_short}, but local git is {local_git_short}.",
                "action": "Synchronize tracked files with git before importing the bundle.",
            })

    for peer, report in sorted(diff_reports.items()):
        errors = report.get("errors") or []
        is_bundle_plan = is_bundle_diff_report(report)
        refresh_diff_action = (
            f"Run {import_bundle_command(report, peer, dry_run=True, write_plan=True)} to refresh the saved bundle delta."
            if is_bundle_plan else
            f"Run python scripts/syncmate/syncmate.py collect {peer} --diff or refresh {peer}."
        )
        diff_error_action = (
            f"Inspect {report.get('report_path')}, rebuild/copy the bundle, then rerun "
            f"{import_bundle_command(report, peer, dry_run=True, write_plan=True)}."
            if is_bundle_plan else
            f"Inspect {report.get('report_path')}, fix SSH/repo setup, then rerun collect {peer} --diff."
        )
        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "warn",
                "code": "diff-stale",
                "node": peer,
                "message": f"{peer} diff report is stale or has an invalid timestamp: {report.get('generated_at')}.",
                "action": refresh_diff_action,
            })
        if errors:
            diagnostics.append({
                "severity": "error",
                "code": "diff-error",
                "node": peer,
                "message": f"{peer} last diff reported error(s): {'; '.join(errors)}.",
                "action": diff_error_action,
            })
            continue

        remote_git_short = report_remote_git_short(report)
        if not git_ids_match(local_git_short, remote_git_short):
            diagnostics.append({
                "severity": "error",
                "code": "diff-git-mismatch",
                "node": peer,
                "message": f"{peer} diff manifest used git {remote_git_short}, but local git is {local_git_short}.",
                "action": "Synchronize tracked files with git, then rebuild or recollect the diff source.",
            })

        summary = report.get("summary") or {}
        missing_count = summary.get("missing", len(report.get("missing") or []))
        conflict_count = summary.get("conflicts", len(report.get("conflicts") or []))
        if missing_count:
            action = (
                f"Run {import_bundle_command(report, peer)} to extract and verify missing selected artifacts from the copied bundle."
                if is_bundle_plan else
                f"Run collect {peer} --apply to fetch and verify missing selected artifacts."
            )
            diagnostics.append({
                "severity": "warn",
                "code": "diff-missing",
                "node": peer,
                "message": f"{peer} diff found {missing_count} remote artifact file(s) not present locally.",
                "action": action,
            })
        if conflict_count:
            action = (
                f"Review conflicts in {report.get('report_path')} before using "
                f"{import_bundle_command(report, peer, overwrite=True)}."
                if is_bundle_plan else
                f"Review conflicts in {report.get('report_path')} before using collect {peer} --apply --overwrite."
            )
            diagnostics.append({
                "severity": "warn",
                "code": "diff-conflicts",
                "node": peer,
                "message": f"{peer} diff found {conflict_count} checksum-conflicting local file(s).",
                "action": action,
            })
        remote_inventory = incomplete_remote_inventory(report)
        if remote_inventory:
            missing = format_missing_counts(remote_inventory["missing_counts"])
            diagnostics.append({
                "severity": "warn",
                "code": "diff-remote-inventory-incomplete",
                "node": peer,
                "message": f"{peer} remote manifest has {remote_inventory['incomplete']} incomplete experiment leaf/leaves"
                           f"{f' ({missing})' if missing else ''}.",
                "action": f"Re-run the missing result artifacts on {peer}, then rerun collect {peer} --diff.",
            })

    for peer in sorted(device.get("peers") or []):
        if peer not in collect_reports:
            diagnostics.append({
                "severity": "info",
                "code": "collect-report-missing",
                "node": peer,
                "message": f"No saved collection report exists for configured peer {peer}.",
                "action": f"Run python scripts/syncmate/syncmate.py collect {peer} --diff, then collect {peer} --apply when ready.",
            })

    for peer, report in sorted(collect_reports.items()):
        errors = report.get("errors") or []
        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "warn",
                "code": "collect-stale",
                "node": peer,
                "message": f"{peer} collection report is stale or has an invalid timestamp: {report.get('generated_at')}.",
                "action": f"Run python scripts/syncmate/syncmate.py collect {peer} --apply when ready.",
            })
        remote_git_short = report_remote_git_short(report)
        if not git_ids_match(local_git_short, remote_git_short):
            diagnostics.append({
                "severity": "error",
                "code": "collect-git-mismatch",
                "node": peer,
                "message": f"{peer} collection manifest used git {remote_git_short}, but local git is {local_git_short}.",
                "action": f"Synchronize tracked files with git, then rerun collect {peer} --apply.",
            })
        if errors:
            diagnostics.append({
                "severity": "error",
                "code": "collect-error",
                "node": peer,
                "message": f"{peer} last collection reported error(s): {'; '.join(errors)}.",
                "action": f"Inspect {report.get('report_path')}, fix the transfer/checksum issue, then rerun collect {peer} --apply.",
            })
        failed = report.get("verification_failed") or []
        if failed:
            diagnostics.append({
                "severity": "error",
                "code": "collect-checksum-failed",
                "node": peer,
                "message": f"{peer} last collection failed checksum verification for {len(failed)} file(s).",
                "action": f"Inspect {report.get('report_path')} and rerun collect {peer} --apply after fixing transfer integrity.",
            })
        conflicts = report.get("conflicts") or []
        if conflicts:
            diagnostics.append({
                "severity": "warn",
                "code": "collect-conflicts",
                "node": peer,
                "message": f"{peer} last collection found {len(conflicts)} checksum-conflicting local file(s).",
                "action": f"Review conflicts in {report.get('report_path')}; use collect {peer} --apply --overwrite only if remote is authoritative.",
            })
        remote_inventory = incomplete_remote_inventory(report)
        if remote_inventory:
            missing = format_missing_counts(remote_inventory["missing_counts"])
            diagnostics.append({
                "severity": "warn",
                "code": "collect-remote-inventory-incomplete",
                "node": peer,
                "message": f"{peer} collected from a remote manifest with {remote_inventory['incomplete']} incomplete experiment leaf/leaves"
                           f"{f' ({missing})' if missing else ''}.",
                "action": f"Re-run the missing result artifacts on {peer}, then rerun collect {peer} --apply and verify {peer} --apply.",
            })

    for peer, report in sorted(verify_reports.items()):
        errors = report.get("errors") or []
        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "warn",
                "code": "verify-stale",
                "node": peer,
                "message": f"{peer} verification report is stale or has an invalid timestamp: {report.get('generated_at')}.",
                "action": f"Run python scripts/syncmate/syncmate.py verify {peer} --apply.",
            })
        remote_git_short = report_remote_git_short(report)
        if not git_ids_match(local_git_short, remote_git_short):
            diagnostics.append({
                "severity": "error",
                "code": "verify-git-mismatch",
                "node": peer,
                "message": f"{peer} verification manifest used git {remote_git_short}, but local git is {local_git_short}.",
                "action": f"Synchronize tracked files with git, then rerun verify {peer} --apply.",
            })
        if errors:
            diagnostics.append({
                "severity": "error",
                "code": "verify-error",
                "node": peer,
                "message": f"{peer} last verification reported error(s): {'; '.join(errors)}.",
                "action": f"Inspect {report.get('report_path')}, fix SSH/repo setup, then rerun verify {peer} --apply.",
            })
            continue

        summary = report.get("summary") or {}
        missing_count = summary.get("missing", len(report.get("missing") or []))
        conflict_count = summary.get("conflicts", len(report.get("conflicts") or []))
        if missing_count:
            diagnostics.append({
                "severity": "error",
                "code": "verify-missing",
                "node": peer,
                "message": f"{peer} verification found {missing_count} remote artifact file(s) missing from the local landing.",
                "action": f"Run collect {peer} --apply, then rerun verify {peer} --apply.",
            })
        if conflict_count:
            diagnostics.append({
                "severity": "error",
                "code": "verify-conflicts",
                "node": peer,
                "message": f"{peer} verification found {conflict_count} checksum-conflicting local file(s).",
                "action": f"Review conflicts in {report.get('report_path')} before using collect {peer} --apply --overwrite.",
            })
        remote_inventory = incomplete_remote_inventory(report)
        if remote_inventory:
            missing = format_missing_counts(remote_inventory["missing_counts"])
            diagnostics.append({
                "severity": "error",
                "code": "verify-remote-inventory-incomplete",
                "node": peer,
                "message": f"{peer} verification matched an incomplete remote manifest with {remote_inventory['incomplete']} incomplete experiment leaf/leaves"
                           f"{f' ({missing})' if missing else ''}.",
                "action": f"Re-run the missing result artifacts on {peer}, then rerun collect {peer} --apply and verify {peer} --apply.",
            })

    indexed_peers = artifact_index.get("peers") or {}
    for peer in sorted(device.get("peers") or []):
        verify_summary = (verify_reports.get(peer) or {}).get("summary") or {}
        if verify_summary.get("status") == "verified" and peer not in indexed_peers:
            diagnostics.append({
                "severity": "warn",
                "code": "artifact-index-missing",
                "node": peer,
                "message": f"{peer} has a verified report but no trusted artifact index entry.",
                "action": f"Run python scripts/syncmate/syncmate.py verify {peer} --apply to refresh .syncmate/artifact_index.json.",
            })

    return diagnostics


def severity_rank(severity: str) -> int:
    return {"error": 3, "warn": 2, "info": 1}.get(severity, 0)


def status_label(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]]) -> str:
    max_rank = max([severity_rank(d["severity"]) for d in diagnostics] or [0])
    if max_rank >= 3:
        return "attention"
    if max_rank >= 2:
        return "review"
    return "ready"


def configured_peers(snapshot: Dict[str, Any]) -> List[str]:
    peers = (snapshot.get("device") or {}).get("peers") or []
    if isinstance(peers, dict):
        return sorted(peers)
    if isinstance(peers, list):
        return sorted(str(peer) for peer in peers)
    return []


def orphaned_sync_entries(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    configured = set(configured_peers(snapshot))
    entries: List[Dict[str, Any]] = []
    report_specs = [
        ("remote_status", snapshot.get("remote_status") or {}),
        ("bundle_inspect", snapshot.get("bundle_inspect_reports") or {}),
        ("diff", snapshot.get("diff_reports") or {}),
        ("collect", snapshot.get("collect_reports") or {}),
        ("verify", snapshot.get("verify_reports") or {}),
    ]
    for kind, reports in report_specs:
        for node_id, report in sorted(reports.items()):
            if node_id in configured:
                continue
            entries.append({
                "kind": kind,
                "node_id": node_id,
                "path": report.get("report_path"),
            })

    for node_id, entry in sorted(((snapshot.get("artifact_index") or {}).get("peers") or {}).items()):
        if node_id in configured:
            continue
        entries.append({
            "kind": "artifact_index",
            "node_id": node_id,
            "path": (snapshot.get("artifact_index") or {}).get("index_path"),
            "indexed": (entry.get("summary") or {}).get("indexed", len(entry.get("items") or [])),
        })
    return entries


def archive_orphaned_sync_state(snapshot: Dict[str, Any], *, apply: bool = False) -> Dict[str, Any]:
    entries = orphaned_sync_entries(snapshot)
    timestamp = now_iso()
    archive_name = timestamp.replace(":", "-") + "_orphaned"
    archive_dir = sync_archive_root() / archive_name
    actions: List[Dict[str, Any]] = []
    errors: List[str] = []

    report_entries = [entry for entry in entries if entry.get("kind") != "artifact_index"]
    index_nodes = sorted({entry["node_id"] for entry in entries if entry.get("kind") == "artifact_index"})

    for entry in report_entries:
        source = safe_sync_file(entry.get("path"))
        archive_path = None
        status = "planned"
        if source is None:
            status = "unsafe"
            errors.append(f"unsafe orphaned report path for {entry.get('node_id')}: {entry.get('path')}")
        else:
            archive_path = unique_archive_path(archive_dir, source.name)
            if apply:
                if source.is_file():
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(archive_path))
                    status = "archived"
                else:
                    status = "missing"
                    errors.append(f"orphaned report no longer exists: {rel(source)}")
        actions.append({
            "kind": entry.get("kind"),
            "node_id": entry.get("node_id"),
            "source": entry.get("path"),
            "archive_path": rel(archive_path) if archive_path else None,
            "status": status,
        })

    if index_nodes:
        archive_path = archive_dir / "artifact_index_before_orphan_archive.json"
        status = "planned"
        if apply:
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            index = load_artifact_index()
            archive_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
            peers = index.get("peers") or {}
            for node_id in index_nodes:
                peers.pop(node_id, None)
            index["peers"] = peers
            index["updated_at"] = timestamp
            write_artifact_index(index)
            status = "archived"
        actions.append({
            "kind": "artifact_index",
            "node_id": ",".join(index_nodes),
            "source": rel(artifact_index_file()),
            "archive_path": rel(archive_path),
            "status": status,
        })

    return {
        "generated_at": timestamp,
        "mode": "archive-orphans",
        "applied": apply,
        "archive_dir": rel(archive_dir),
        "summary": {
            "orphaned_entries": len(entries),
            "report_files": len(report_entries),
            "index_entries": len(index_nodes),
            "actions": len(actions),
            "errors": len(errors),
        },
        "actions": actions,
        "errors": errors,
    }


def verify_gate_diagnostics(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    verify_reports = snapshot.get("verify_reports") or {}
    for peer in configured_peers(snapshot):
        report = verify_reports.get(peer)
        if not report:
            diagnostics.append({
                "severity": "error",
                "code": "gate-verify-missing",
                "node": peer,
                "message": f"No verification report exists for configured peer {peer}.",
                "action": f"Run python scripts/syncmate/syncmate.py verify {peer} --apply.",
            })
            continue

        if is_report_stale(report.get("generated_at")):
            diagnostics.append({
                "severity": "error",
                "code": "gate-verify-stale",
                "node": peer,
                "message": f"{peer} verification report is stale or invalid: {report.get('generated_at')}.",
                "action": f"Run python scripts/syncmate/syncmate.py verify {peer} --apply.",
            })

        errors = report.get("errors") or []
        if errors:
            diagnostics.append({
                "severity": "error",
                "code": "gate-verify-error",
                "node": peer,
                "message": f"{peer} verification report has error(s): {'; '.join(errors)}.",
                "action": f"Inspect {report.get('report_path')}, fix the issue, then rerun verify {peer} --apply.",
            })

        summary = report.get("summary") or {}
        missing_count = summary.get("missing", len(report.get("missing") or []))
        conflict_count = summary.get("conflicts", len(report.get("conflicts") or []))
        if missing_count or conflict_count:
            diagnostics.append({
                "severity": "error",
                "code": "gate-verify-incomplete",
                "node": peer,
                "message": f"{peer} verification is incomplete: missing={missing_count}, conflicts={conflict_count}.",
                "action": f"Run collect {peer} --apply, resolve conflicts if any, then rerun verify {peer} --apply.",
            })

        remote_inventory = incomplete_remote_inventory(report)
        if remote_inventory:
            missing = format_missing_counts(remote_inventory["missing_counts"])
            diagnostics.append({
                "severity": "error",
                "code": "gate-remote-inventory-incomplete",
                "node": peer,
                "message": f"{peer} remote manifest has {remote_inventory['incomplete']} incomplete experiment leaf/leaves"
                           f"{f' ({missing})' if missing else ''}.",
                "action": f"Re-run the missing result artifacts on {peer}, then rerun collect {peer} --apply and verify {peer} --apply.",
            })

        if summary.get("status") != "verified":
            diagnostics.append({
                "severity": "error",
                "code": "gate-verify-status",
                "node": peer,
                "message": f"{peer} verification status is {summary.get('status', 'unknown')!r}, not 'verified'.",
                "action": f"Rerun python scripts/syncmate/syncmate.py verify {peer} --apply after collection is complete.",
            })
    return diagnostics


def index_gate_diagnostics(snapshot: Dict[str, Any],
                           index_check: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    artifact_index = snapshot.get("artifact_index") or {}
    indexed_peers = artifact_index.get("peers") or {}
    for peer in configured_peers(snapshot):
        if peer not in indexed_peers:
            diagnostics.append({
                "severity": "error",
                "code": "gate-index-missing",
                "node": peer,
                "message": f"No trusted artifact index entry exists for configured peer {peer}.",
                "action": f"Run python scripts/syncmate/syncmate.py verify {peer} --apply to refresh the artifact index.",
            })

    for peer in incomplete_inventory_peers(artifact_index, configured_peers(snapshot)):
        missing = ", ".join(f"{name}={count}" for name, count in peer["missing_counts"].items())
        diagnostics.append({
            "severity": "error",
            "code": "gate-inventory-incomplete",
            "node": peer["node_id"],
            "message": f"{peer['node_id']} trusted inventory has {peer['incomplete']} incomplete experiment leaf/leaves"
                       f"{f' ({missing})' if missing else ''}.",
            "action": f"Run python scripts/syncmate/syncmate.py inventory {peer['node_id']} --only-incomplete, "
                      "then collect/verify the missing result artifacts before aggregation.",
        })

    result = index_check or check_artifact_index(artifact_index)
    for error in result.get("errors") or []:
        diagnostics.append({
            "severity": "error",
            "code": "gate-index-error",
            "message": error,
            "action": "Repair .syncmate/artifact_index.json, then rerun verify <node_id> --apply.",
        })

    for peer, summary in sorted((result.get("peers") or {}).items()):
        missing = int(summary.get("missing") or 0)
        mismatched = int(summary.get("mismatched") or 0)
        unsafe = int(summary.get("unsafe") or 0)
        if missing:
            diagnostics.append({
                "severity": "error",
                "code": "gate-index-missing-files",
                "node": peer,
                "message": f"{peer} artifact index references {missing} local file(s) that are missing.",
                "action": f"Run collect {peer} --apply, then verify {peer} --apply.",
            })
        if mismatched:
            diagnostics.append({
                "severity": "error",
                "code": "gate-index-checksum-mismatch",
                "node": peer,
                "message": f"{peer} artifact index found {mismatched} local checksum mismatch(es).",
                "action": f"Inspect local edits under the peer landing, then rerun verify {peer} --apply.",
            })
        if unsafe:
            diagnostics.append({
                "severity": "error",
                "code": "gate-index-unsafe-path",
                "node": peer,
                "message": f"{peer} artifact index contains {unsafe} unsafe local path(s).",
                "action": "Repair .syncmate/artifact_index.json and rerun verify after confirming the landing path.",
            })
    return diagnostics


def results_table_signature(data: Dict[str, Any]) -> Dict[str, Any]:
    summary = data.get("summary") or {}
    rows = data.get("rows") if isinstance(data.get("rows"), list) else []
    parse_errors = data.get("parse_errors") if isinstance(data.get("parse_errors"), list) else []
    return {
        "summary": {
            key: summary.get(key, 0)
            for key in (
                "peers",
                "leaves",
                "rows",
                "complete_leaves",
                "incomplete_leaves",
                "skipped_incomplete",
                "parse_error_rows",
                "parse_errors",
            )
        },
        "rows_hash": stable_hash(rows, length=16),
        "parse_errors_hash": stable_hash(parse_errors, length=16),
    }


RESULT_ROW_ID_FIELDS = (
    "node_id",
    "cell",
    "method",
    "method_strategy",
    "strategy",
    "strategy_full",
    "seed",
    "local_leaf",
)


def result_rows_from_table(data: Optional[Any]) -> List[Dict[str, Any]]:
    if not isinstance(data, dict):
        return []
    rows = data.get("rows")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def result_row_key(row: Dict[str, Any]) -> str:
    key = {field: row.get(field) for field in RESULT_ROW_ID_FIELDS}
    return stable_json(key)


def compact_result_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "node_id": row.get("node_id"),
        "cell": row.get("cell"),
        "method": row.get("method"),
        "strategy_full": row.get("strategy_full"),
        "seed": row.get("seed"),
        "status": row.get("status"),
        "f1_after": row.get("f1_after"),
        "f1_drop": row.get("f1_drop"),
        "mia_auc": row.get("mia_auc"),
        "local_leaf": row.get("local_leaf"),
    }


def result_row_map(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    mapped: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = result_row_key(row)
        if key in mapped:
            key = stable_json({"row": key, "hash": stable_hash(row, length=16)})
        mapped[key] = row
    return mapped


def results_table_delta(previous: Optional[Any], current: Optional[Any],
                        *, limit: int = 5) -> Dict[str, Any]:
    previous_rows = result_rows_from_table(previous)
    current_rows = result_rows_from_table(current)
    previous_map = result_row_map(previous_rows)
    current_map = result_row_map(current_rows)
    previous_keys = set(previous_map)
    current_keys = set(current_map)
    added_keys = sorted(current_keys - previous_keys)
    removed_keys = sorted(previous_keys - current_keys)
    changed_keys = sorted(
        key for key in (previous_keys & current_keys)
        if stable_hash(previous_map[key], length=16) != stable_hash(current_map[key], length=16)
    )
    sample_limit = max(0, limit)
    return {
        "previous_rows": len(previous_rows),
        "current_rows": len(current_rows),
        "added_rows": len(added_keys),
        "removed_rows": len(removed_keys),
        "changed_rows": len(changed_keys),
        "previous_hash": stable_hash(previous_rows, length=16),
        "current_hash": stable_hash(current_rows, length=16),
        "examples": {
            "added": [compact_result_row(current_map[key]) for key in added_keys[:sample_limit]],
            "removed": [compact_result_row(previous_map[key]) for key in removed_keys[:sample_limit]],
            "changed": [compact_result_row(current_map[key]) for key in changed_keys[:sample_limit]],
        },
    }


def results_gate_diagnostics(snapshot: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    artifact_index = snapshot.get("artifact_index") or {}
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    expected = results_payload_from_index(artifact_index, include_incomplete=False)
    expected_summary = expected.get("summary") or {}
    actual_summary = (results_table.get("summary") or {}) if results_table else {}
    check = {
        "status": "ok",
        "expected": results_table_signature(expected),
        "actual": results_table_signature(results_table) if results_table else None,
        "path": rel(results_table_file()),
        "csv": rel(results_csv_file()),
    }

    if not artifact_index_total(artifact_index):
        diagnostics.append({
            "severity": "error",
            "code": "gate-results-no-indexed-artifacts",
            "message": "No trusted artifacts are indexed, so no trusted results table can be required.",
            "action": "Run sync <node_id> or verify <node_id> --apply before requiring results.",
        })

    if not results_table:
        diagnostics.append({
            "severity": "error",
            "code": "gate-results-missing",
            "message": "No saved trusted results table exists.",
            "action": "Run python scripts/syncmate/syncmate.py results --write --check.",
        })
    else:
        load_errors = results_table.get("errors") or []
        parse_errors = results_table.get("parse_errors") or []
        if load_errors:
            diagnostics.append({
                "severity": "error",
                "code": "gate-results-error",
                "message": f"Saved trusted results table has error(s): {'; '.join(str(item) for item in load_errors)}.",
                "action": "Inspect .syncmate/results_table.json, then rerun results --write --check.",
            })
        if parse_errors or int(actual_summary.get("parse_errors") or 0):
            diagnostics.append({
                "severity": "error",
                "code": "gate-results-parse-error",
                "message": f"Saved trusted results table has parse error(s): {actual_summary.get('parse_errors', len(parse_errors))}.",
                "action": "Inspect .syncmate/results_table.json parse_errors, fix the source artifact, then rerun results --write --check.",
            })
        if results_table_signature(results_table) != check["expected"]:
            diagnostics.append({
                "severity": "error",
                "code": "gate-results-stale",
                "message": "Saved trusted results table does not match the current artifact index.",
                "action": "Run python scripts/syncmate/syncmate.py results --write --check to refresh .syncmate/results_table.*.",
            })

    expected_errors = expected.get("errors") or []
    expected_parse_errors = expected.get("parse_errors") or []
    if expected_errors:
        diagnostics.append({
            "severity": "error",
            "code": "gate-results-current-error",
            "message": f"Current trusted results extraction reports error(s): {'; '.join(str(item) for item in expected_errors)}.",
            "action": "Repair .syncmate/artifact_index.json or rerun verify <node_id> --apply, then rerun results --write --check.",
        })
    if expected_parse_errors or int(expected_summary.get("parse_errors") or 0):
        diagnostics.append({
            "severity": "error",
            "code": "gate-results-current-parse-error",
            "message": f"Current trusted results extraction has parse error(s): {expected_summary.get('parse_errors', len(expected_parse_errors))}.",
            "action": "Inspect source result artifacts, fix or recollect them, then rerun results --write --check.",
        })

    if diagnostics:
        check["status"] = "failed"
    return diagnostics, check


def preflight_gate_diagnostics(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    diagnostics: List[Dict[str, Any]] = []
    preflight = snapshot.get("preflight")
    if not isinstance(preflight, dict) or not preflight:
        diagnostics.append({
            "severity": "error",
            "code": "gate-preflight-missing",
            "message": "No saved preflight report exists.",
            "action": "Run python scripts/syncmate/syncmate.py preflight --write.",
        })
        return diagnostics

    report_path = preflight.get("report_path") or preflight.get("path") or rel(last_preflight_file())
    load_errors = preflight.get("errors") or []
    if load_errors and not preflight.get("summary"):
        diagnostics.append({
            "severity": "error",
            "code": "gate-preflight-invalid",
            "message": f"Saved preflight report is invalid: {'; '.join(str(item) for item in load_errors)}.",
            "action": f"Inspect {report_path}, then rerun python scripts/syncmate/syncmate.py preflight --write.",
        })
        return diagnostics

    if is_report_stale(preflight.get("generated_at")):
        diagnostics.append({
            "severity": "error",
            "code": "gate-preflight-stale",
            "message": f"Saved preflight report is stale or invalid: {preflight.get('generated_at')}.",
            "action": "Run python scripts/syncmate/syncmate.py preflight --write.",
        })

    status = preflight.get("status") or "unknown"
    summary = preflight.get("summary") or {}
    if status == "blocked" or int(summary.get("errors") or 0):
        diagnostics.append({
            "severity": "error",
            "code": "gate-preflight-blocked",
            "message": f"Saved preflight is blocked: errors={summary.get('errors', 0)}, peers_blocked={summary.get('blocked', 0)}.",
            "action": "Fix the preflight blockers, then rerun python scripts/syncmate/syncmate.py preflight --write.",
        })
    elif status not in ("ready", "warn"):
        diagnostics.append({
            "severity": "error",
            "code": "gate-preflight-status",
            "message": f"Saved preflight status is {status!r}, not ready.",
            "action": "Rerun python scripts/syncmate/syncmate.py preflight --write and inspect the report.",
        })
    elif status == "warn" or int(summary.get("warnings") or 0):
        diagnostics.append({
            "severity": "warn",
            "code": "gate-preflight-warn",
            "message": f"Saved preflight has warning(s): warnings={summary.get('warnings', 0)}.",
            "action": "Inspect .syncmate/last_preflight.json before treating the setup as fully ready.",
        })

    peers = preflight.get("peers") if isinstance(preflight.get("peers"), dict) else {}
    for peer in configured_peers(snapshot):
        if peer not in peers:
            diagnostics.append({
                "severity": "error",
                "code": "gate-preflight-peer-missing",
                "node": peer,
                "message": f"Saved preflight report does not include configured peer {peer}.",
                "action": f"Run python scripts/syncmate/syncmate.py preflight {peer} --write or preflight --write.",
            })
    return diagnostics


def gate_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                 fail_on: str = "warn", require_verify: bool = False,
                 require_preflight: bool = False,
                 require_results: bool = False) -> Dict[str, Any]:
    if fail_on not in ("error", "warn", "info"):
        raise SystemExit("fail_on must be one of: error, warn, info")
    index_check = check_artifact_index(snapshot.get("artifact_index") or {}) if require_verify else None
    gate_diagnostics = []
    results_check = None
    if require_preflight:
        gate_diagnostics.extend(preflight_gate_diagnostics(snapshot))
    if require_verify:
        gate_diagnostics.extend(verify_gate_diagnostics(snapshot))
        gate_diagnostics.extend(index_gate_diagnostics(snapshot, index_check))
    if require_results:
        results_diagnostics, results_check = results_gate_diagnostics(snapshot)
        gate_diagnostics.extend(results_diagnostics)
    threshold = severity_rank(fail_on)
    failures = [
        item for item in [*diagnostics, *gate_diagnostics]
        if severity_rank(item.get("severity", "")) >= threshold
    ]
    return {
        "generated_at": snapshot.get("generated_at"),
        "device_id": (snapshot.get("device") or {}).get("id"),
        "status": status_label(snapshot, diagnostics),
        "mode": "gate",
        "fail_on": fail_on,
        "require_verify": require_verify,
        "require_preflight": require_preflight,
        "require_results": require_results,
        "index_check": index_check,
        "results_check": results_check,
        "passed": not failures,
        "diagnostics": diagnostics,
        "gate_diagnostics": gate_diagnostics,
        "failure_count": len(failures),
        "failures": failures,
    }


def cmd_self(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    data = {
        "generated_at": now_iso(),
        "repo_root": str(REPO_ROOT),
        "device": {
            "id": device.get("device_id"),
            "role": device.get("role"),
            "repo_path": device.get("repo_path"),
            "setup_file": rel(args.config),
            "setup_warnings": warnings,
            "peers": sorted((device.get("peers") or {}).keys()),
        },
        "git": git_state(),
    }
    if args.json:
        print_json(data)
        return 0
    print(f"syncmate self: {data['device']['id']} ({data['device']['role']})")
    print(f"  repo: {data['repo_root']}")
    print(f"  setup: {data['device']['setup_file']}")
    for warning in warnings:
        print(f"  warning: {warning}")
    print(f"  git: {data['git']['branch']} @ {data['git']['short_sha']} dirty={data['git']['dirty']}")
    peers = data["device"]["peers"]
    print(f"  peers: {', '.join(peers) if peers else 'none'}")
    return 0


def cmd_init_device(args: argparse.Namespace) -> int:
    device_id = args.device_id or default_device_id()
    repo_path = args.repo_path or str(REPO_ROOT)
    artifact_policy = artifact_policy_from_cli(args.artifact_include, args.artifact_exclude)
    config = build_device_config(
        device_id=device_id,
        role=args.role,
        repo_path=repo_path,
        collector_hint=args.collector_hint,
        artifact_policy=artifact_policy,
    )
    write_device_config(args.config, config, force=args.force)
    data = {
        "generated_at": now_iso(),
        "setup_file": rel(args.config),
        "device": config,
        "overwrote": bool(args.force),
    }
    if args.json:
        print_json(data)
        return 0

    print(f"syncmate init-device: wrote {data['setup_file']}")
    print(f"  device: {device_id} ({args.role})")
    print(f"  repo: {repo_path}")
    if artifact_policy:
        print(f"  artifact policy: {artifact_policy}")
    if "collector" in args.role:
        print("  peers: add runner peers in .syncmate/device.yaml when ready")
    if args.collector_hint:
        print(f"  collector hint: {args.collector_hint}")
    return 0


def cmd_add_peer(args: argparse.Namespace) -> int:
    if not args.config.exists():
        raise SystemExit(f"{rel(args.config)} missing; run init-device --role collector first")

    device, warnings = load_device(args.config)
    if warnings:
        raise SystemExit("; ".join(warnings))

    landing = args.landing or f"results/runs/{args.node_id}"
    artifact_policy = artifact_policy_from_cli(args.artifact_include, args.artifact_exclude)
    transport = "local" if args.local else "ssh"
    if transport == "ssh" and not args.ssh:
        raise SystemExit("add-peer requires --ssh unless --local is used")
    peer = build_peer_config(
        role=args.role,
        ssh=args.ssh,
        repo_path=args.repo_path,
        landing=landing,
        result_roots=args.result_roots or ["results/runs"],
        artifact_policy=artifact_policy,
        transport=transport,
        python_executable=args.python_executable,
    )
    add_peer_to_device(device, args.node_id, peer, force=args.force)
    write_device_config(args.config, device, force=True)

    data = {
        "generated_at": now_iso(),
        "setup_file": rel(args.config),
        "node_id": args.node_id,
        "peer": peer,
        "replaced": bool(args.force),
        "peers": sorted((device.get("peers") or {}).keys()),
    }
    if args.json:
        print_json(data)
        return 0

    print(f"syncmate add-peer: {args.node_id}")
    print(f"  transport: {transport}")
    if peer.get("ssh"):
        print(f"  ssh: {peer.get('ssh')}")
    if peer.get("python_executable"):
        print(f"  python: {peer.get('python_executable')}")
    print(f"  repo: {args.repo_path}")
    print(f"  landing: {landing}")
    print(f"  result roots: {', '.join(peer['result_roots'])}")
    if artifact_policy:
        print(f"  artifact policy: {artifact_policy}")
    print(f"  setup: {data['setup_file']}")
    return 0


def cmd_setup_plan(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    artifact_policy = artifact_policy_from_cli(args.artifact_include, args.artifact_exclude)
    data = setup_plan_payload(
        device,
        warnings,
        setup_path=args.config,
        target_role=args.role,
        device_id=args.device_id,
        repo_path=args.repo_path,
        collector_id=args.collector_id,
        peer_id=args.peer_id,
        peer_ssh=args.peer_ssh,
        peer_repo_path=args.peer_repo_path,
        peer_python_executable=args.peer_python_executable,
        peer_local=args.peer_local,
        landing=args.landing,
        result_roots=args.result_roots,
        artifact_policy=artifact_policy,
    )
    out_path = None
    if args.write:
        out_path = write_setup_plan(data)
        data["setup_plan_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0
    if args.write:
        print(f"syncmate setup-plan: {rel(out_path)}")
    else:
        print(render_setup_plan_markdown(data))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    data = {
        "generated_at": snapshot["generated_at"],
        "device_id": snapshot["device"]["id"],
        "status": status_label(snapshot, diagnostics),
        "diagnostics": diagnostics,
    }
    if args.json:
        print_json(data)
        return 0

    print(f"syncmate doctor: {data['device_id']} status={data['status']}")
    if not diagnostics:
        print("  ok: no diagnostics")
        return 0
    for item in diagnostics:
        node = f" node={item['node']}" if item.get("node") else ""
        print(f"  [{item['severity']}] {item['code']}{node}: {item['message']}")
        print(f"       action: {item['action']}")
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = gate_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=args.require_verify,
        require_preflight=args.require_preflight,
        require_results=args.require_results,
    )
    if args.json:
        print_json(data)
        return 0 if data["passed"] else 1

    state = "pass" if data["passed"] else "fail"
    print(
        f"syncmate gate: {state} status={data['status']} fail_on={data['fail_on']} "
        f"require_preflight={data['require_preflight']} "
        f"require_verify={data['require_verify']} "
        f"require_results={data['require_results']}"
    )
    if data["passed"]:
        print("  ok: no blocking diagnostics")
        return 0

    print(f"  failures: {data['failure_count']}")
    for item in data["failures"]:
        node = f" node={item['node']}" if item.get("node") else ""
        print(f"  [{item['severity']}] {item['code']}{node}: {item['message']}")
        print(f"       action: {item['action']}")
    return 1


def peer_summary(snapshot: Dict[str, Any], node_id: str) -> Dict[str, Any]:
    remote_status = (snapshot.get("remote_status") or {}).get(node_id) or {}
    diff_report = (snapshot.get("diff_reports") or {}).get(node_id) or {}
    bundle_inspect_report = (snapshot.get("bundle_inspect_reports") or {}).get(node_id) or {}
    collect_report = (snapshot.get("collect_reports") or {}).get(node_id) or {}
    verify_report = (snapshot.get("verify_reports") or {}).get(node_id) or {}
    index_entry = ((snapshot.get("artifact_index") or {}).get("peers") or {}).get(node_id) or {}

    remote_summary = remote_status.get("summary") or {}
    diff_summary = diff_report.get("summary") or {}
    bundle_audit = bundle_inspect_report.get("audit") or {}
    bundle_manifest = bundle_inspect_report.get("manifest") or {}
    bundle_inventory = bundle_manifest.get("inventory_summary") or {}
    collect_summary = collect_report.get("summary") or {}
    verify_summary = verify_report.get("summary") or {}
    index_summary = index_entry.get("summary") or {}
    return {
        "node_id": node_id,
        "remote": {
            "age": format_age(remote_status.get("generated_at")) if remote_status else None,
            "git": remote_summary.get("git_short_sha"),
            "dirty": remote_summary.get("git_dirty"),
            "fingerprint": remote_summary.get("fingerprint"),
            "leaves": remote_summary.get("result_leaves"),
            "log_files": remote_summary.get("log_files"),
            "log_errors": remote_summary.get("log_errors"),
            "latest_log_age": remote_summary.get("latest_log_age"),
            "errors": len(remote_status.get("errors") or []),
        },
        "diff": {
            "age": format_age(diff_report.get("generated_at")) if diff_report else None,
            "remote_files": diff_summary.get("remote_files"),
            "remote_leaves": diff_summary.get("remote_leaves"),
            "remote_incomplete": diff_summary.get("remote_incomplete"),
            "missing": diff_summary.get("missing", len(diff_report.get("missing") or [])),
            "conflicts": diff_summary.get("conflicts", len(diff_report.get("conflicts") or [])),
            "errors": len(diff_report.get("errors") or []),
        },
        "bundle_inspect": {
            "age": format_age(bundle_inspect_report.get("generated_at")) if bundle_inspect_report else None,
            "status": bundle_audit.get("status"),
            "bundle_path": bundle_inspect_report.get("bundle_path"),
            "manifest_files": bundle_manifest.get("count"),
            "manifest_leaves": bundle_inventory.get("leaves"),
            "manifest_incomplete": bundle_inventory.get("incomplete"),
            "warnings": len(bundle_audit.get("warnings") or []),
            "errors": len(bundle_inspect_report.get("errors") or bundle_audit.get("errors") or []),
        },
        "collect": {
            "age": format_age(collect_report.get("generated_at")) if collect_report else None,
            "remote_leaves": collect_summary.get("remote_leaves"),
            "remote_incomplete": collect_summary.get("remote_incomplete"),
            "fetched": collect_summary.get("missing_fetched"),
            "verified": collect_summary.get("verified"),
            "conflicts": len(collect_report.get("conflicts") or []),
            "failed": len(collect_report.get("verification_failed") or []),
            "errors": len(collect_report.get("errors") or []),
        },
        "verify": {
            "age": format_age(verify_report.get("generated_at")) if verify_report else None,
            "status": verify_summary.get("status"),
            "remote_leaves": verify_summary.get("remote_leaves"),
            "remote_incomplete": verify_summary.get("remote_incomplete"),
            "missing": verify_summary.get("missing", len(verify_report.get("missing") or [])),
            "conflicts": verify_summary.get("conflicts", len(verify_report.get("conflicts") or [])),
            "errors": len(verify_report.get("errors") or []),
        },
        "index": {
            "age": format_age(index_entry.get("updated_at")) if index_entry else None,
            "remote_leaves": index_summary.get("remote_leaves"),
            "remote_incomplete": index_summary.get("remote_incomplete"),
            "indexed": index_summary.get("indexed", len(index_entry.get("items") or [])),
            "status": index_summary.get("status"),
            "missing": index_summary.get("missing"),
            "conflicts": index_summary.get("conflicts"),
        },
    }


COMPACT_ITEM_KEYS = (
    "path",
    "remote_path",
    "local_path",
    "sha256",
    "local_sha256",
    "expected_sha256",
    "actual_sha256",
)

COMPACT_RESULT_ROW_KEYS = (
    "node_id",
    "cell",
    "dataset",
    "base_model",
    "ratio",
    "method",
    "strategy",
    "strategy_full",
    "method_strategy",
    "seed",
    "f1_after",
    "f1_drop",
    "mia_auc",
    "gap",
    "local_leaf",
    "remote_leaf",
    "status",
    "attack_sha256",
    "collateral_sha256",
    "meta_sha256",
    "parse_errors",
)


def known_report_nodes(snapshot: Dict[str, Any]) -> List[str]:
    nodes = set(configured_peers(snapshot))
    nodes.update((snapshot.get("remote_status") or {}).keys())
    nodes.update((snapshot.get("bundle_inspect_reports") or {}).keys())
    nodes.update((snapshot.get("diff_reports") or {}).keys())
    nodes.update((snapshot.get("collect_reports") or {}).keys())
    nodes.update((snapshot.get("verify_reports") or {}).keys())
    nodes.update(((snapshot.get("artifact_index") or {}).get("peers") or {}).keys())
    return sorted(str(node) for node in nodes)


def compact_items(items: List[Any], limit: int) -> List[Any]:
    out: List[Any] = []
    for item in (items or [])[:max(0, limit)]:
        if isinstance(item, dict):
            compact = {key: item[key] for key in COMPACT_ITEM_KEYS if key in item}
            out.append(compact or item)
        else:
            out.append(item)
    return out


def compact_result_rows(rows: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    out = []
    for row in (rows or [])[:max(0, limit)]:
        if not isinstance(row, dict):
            continue
        out.append({key: row[key] for key in COMPACT_RESULT_ROW_KEYS if key in row})
    return out


def compact_remote_inventory(report: Dict[str, Any], limit: int) -> Optional[Dict[str, Any]]:
    info = incomplete_remote_inventory(report)
    if not info:
        return None
    return {
        "incomplete": info["incomplete"],
        "missing_counts": info["missing_counts"],
        "examples": (info.get("examples") or [])[:max(0, limit)],
    }


def compact_report(report: Dict[str, Any], kind: str, limit: int) -> Dict[str, Any]:
    if not report:
        return {"present": False}
    summary = report.get("summary") or {}
    out: Dict[str, Any] = {
        "present": True,
        "generated_at": report.get("generated_at"),
        "age": format_age(report.get("generated_at")),
        "report_path": report.get("report_path"),
        "errors": list(report.get("errors") or []),
    }
    if kind == "remote":
        out["summary"] = {
            "device_id": summary.get("device_id"),
            "role": summary.get("role"),
            "git_short_sha": summary.get("git_short_sha"),
            "git_dirty": summary.get("git_dirty"),
            "fingerprint": summary.get("fingerprint"),
            "fingerprint_components": summary.get("fingerprint_components") or {},
            "result_leaves": summary.get("result_leaves"),
            "result_nodes": summary.get("result_nodes") or [],
            "log_files": summary.get("log_files"),
            "log_errors": summary.get("log_errors"),
            "latest_log_age": summary.get("latest_log_age"),
        }
    elif kind == "diff":
        out["landing"] = report.get("landing")
        out["source"] = report_remote_source(report)
        if is_bundle_diff_report(report):
            out["bundle_path"] = report_bundle_path(report)
        out["summary"] = {
            "remote_files": summary.get("remote_files"),
            "remote_leaves": summary.get("remote_leaves"),
            "remote_incomplete": summary.get("remote_incomplete", 0),
            "already_current": summary.get("already_current"),
            "missing": summary.get("missing", len(report.get("missing") or [])),
            "conflicts": summary.get("conflicts", len(report.get("conflicts") or [])),
            "to_fetch": summary.get("to_fetch"),
        }
        out["examples"] = {
            "missing": compact_items(report.get("missing") or [], limit),
            "conflicts": compact_items(report.get("conflicts") or [], limit),
        }
    elif kind == "bundle_inspect":
        manifest = report.get("manifest") or {}
        inventory = manifest.get("inventory_summary") or {}
        audit = report.get("audit") or {}
        out["bundle_path"] = report.get("bundle_path")
        out["summary"] = {
            "audit_status": audit.get("status"),
            "manifest_files": manifest.get("count"),
            "manifest_leaves": inventory.get("leaves"),
            "manifest_incomplete": inventory.get("incomplete"),
            "audit_errors": len(audit.get("errors") or []),
            "audit_warnings": len(audit.get("warnings") or []),
        }
        out["examples"] = {
            "sample_items": compact_items(manifest.get("sample_items") or [], limit),
        }
    elif kind == "collect":
        out["landing"] = report.get("landing")
        out["artifact_index"] = report.get("artifact_index")
        out["summary"] = {
            "remote_files": summary.get("remote_files"),
            "remote_leaves": summary.get("remote_leaves"),
            "remote_incomplete": summary.get("remote_incomplete", 0),
            "already_current": summary.get("already_current"),
            "fetched_missing": summary.get("missing_fetched"),
            "conflicts": summary.get("conflicts", len(report.get("conflicts") or [])),
            "verified": summary.get("verified"),
            "failed": len(report.get("verification_failed") or []),
        }
        out["examples"] = {
            "fetched": compact_items(report.get("fetched") or [], limit),
            "conflicts": compact_items(report.get("conflicts") or [], limit),
            "verification_failed": compact_items(report.get("verification_failed") or [], limit),
        }
    elif kind == "verify":
        out["landing"] = report.get("landing")
        out["artifact_index"] = report.get("artifact_index")
        out["summary"] = {
            "remote_files": summary.get("remote_files"),
            "remote_leaves": summary.get("remote_leaves"),
            "remote_incomplete": summary.get("remote_incomplete", 0),
            "verified_current": summary.get("verified_current", summary.get("already_current")),
            "missing": summary.get("missing", len(report.get("missing") or [])),
            "conflicts": summary.get("conflicts", len(report.get("conflicts") or [])),
            "status": summary.get("status"),
        }
        out["examples"] = {
            "missing": compact_items(report.get("missing") or [], limit),
            "conflicts": compact_items(report.get("conflicts") or [], limit),
        }
    else:
        out["summary"] = summary

    remote_inventory = compact_remote_inventory(report, limit)
    if remote_inventory:
        out["remote_inventory_incomplete"] = remote_inventory
    return out


def compact_index_entry(entry: Dict[str, Any], limit: int) -> Dict[str, Any]:
    if not entry:
        return {"present": False}
    summary = entry.get("summary") or {}
    return {
        "present": True,
        "updated_at": entry.get("updated_at"),
        "age": format_age(entry.get("updated_at")),
        "landing": entry.get("landing"),
        "source_report": entry.get("source_report"),
        "summary": {
            "remote_files": summary.get("remote_files"),
            "remote_leaves": summary.get("remote_leaves"),
            "remote_incomplete": summary.get("remote_incomplete", 0),
            "indexed": summary.get("indexed", len(entry.get("items") or [])),
            "missing": summary.get("missing"),
            "conflicts": summary.get("conflicts"),
            "status": summary.get("status"),
        },
        "examples": {
            "items": compact_items(entry.get("items") or [], limit),
        },
    }


def peer_reports_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                         node_ids: Optional[List[str]] = None,
                         limit: int = 5) -> Dict[str, Any]:
    known_nodes = known_report_nodes(snapshot)
    selected = [str(node) for node in (node_ids or known_nodes)]
    unknown = [node for node in selected if node not in known_nodes]
    ranked_diagnostics = sorted(
        diagnostics,
        key=lambda item: severity_rank(item.get("severity", "")),
        reverse=True,
    )
    peers: Dict[str, Any] = {}
    for node_id in selected:
        node_diagnostics = [
            item for item in ranked_diagnostics
            if item.get("node") == node_id
        ][:max(0, limit)]
        peers[node_id] = {
            "node_id": node_id,
            "known": node_id in known_nodes,
            "remote": compact_report((snapshot.get("remote_status") or {}).get(node_id) or {}, "remote", limit),
            "bundle_inspect": compact_report(
                (snapshot.get("bundle_inspect_reports") or {}).get(node_id) or {},
                "bundle_inspect",
                limit,
            ),
            "diff": compact_report((snapshot.get("diff_reports") or {}).get(node_id) or {}, "diff", limit),
            "collect": compact_report((snapshot.get("collect_reports") or {}).get(node_id) or {}, "collect", limit),
            "verify": compact_report((snapshot.get("verify_reports") or {}).get(node_id) or {}, "verify", limit),
            "index": compact_index_entry(((snapshot.get("artifact_index") or {}).get("peers") or {}).get(node_id) or {}, limit),
            "diagnostics": node_diagnostics,
        }
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "reports",
        "limit": limit,
        "known_peers": known_nodes,
        "requested_peers": selected if node_ids else [],
        "unknown_peers": unknown,
        "summary": {
            "peers": len(peers),
            "known": len([peer for peer in peers.values() if peer["known"]]),
            "unknown": len(unknown),
        },
        "peers": peers,
    }


def count_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def report_errors(report: Dict[str, Any]) -> List[str]:
    return [str(item) for item in (report.get("errors") or [])]


def receipt_peer_payload(snapshot: Dict[str, Any], node_id: str, *, limit: int = 5) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    peer_configs = device.get("peer_configs") or {}
    diff_report = (snapshot.get("diff_reports") or {}).get(node_id) or {}
    collect_report = (snapshot.get("collect_reports") or {}).get(node_id) or {}
    verify_report = (snapshot.get("verify_reports") or {}).get(node_id) or {}
    index_entry = ((snapshot.get("artifact_index") or {}).get("peers") or {}).get(node_id) or {}

    diff = compact_report(diff_report, "diff", limit)
    collect = compact_report(collect_report, "collect", limit)
    verify = compact_report(verify_report, "verify", limit)
    index = compact_index_entry(index_entry, limit)

    diff_summary = diff.get("summary") or {}
    collect_summary = collect.get("summary") or {}
    verify_summary = verify.get("summary") or {}
    index_summary = index.get("summary") or {}

    missing = count_int(first_present(verify_summary.get("missing"), diff_summary.get("missing")))
    conflicts = count_int(first_present(verify_summary.get("conflicts"), collect_summary.get("conflicts"), diff_summary.get("conflicts")))
    checksum_failed = count_int(collect_summary.get("failed"))
    remote_incomplete = max(
        count_int(diff_summary.get("remote_incomplete")),
        count_int(collect_summary.get("remote_incomplete")),
        count_int(verify_summary.get("remote_incomplete")),
        count_int(index_summary.get("remote_incomplete")),
    )
    verified = count_int(first_present(verify_summary.get("verified_current"), collect_summary.get("verified")))
    indexed = count_int(index_summary.get("indexed"))
    fetched = count_int(collect_summary.get("fetched_missing"))
    errors = (
        report_errors(diff_report)
        + report_errors(collect_report)
        + report_errors(verify_report)
        + report_errors(index_entry)
    )

    has_any_report = any(
        report.get("present")
        for report in (diff, collect, verify, index)
    )
    verify_status = verify_summary.get("status")
    index_status = index_summary.get("status")
    if not has_any_report:
        state = "no-reports"
    elif errors or checksum_failed or conflicts:
        state = "blocked"
    elif verify_status == "verified" and index_status == "verified" and not missing and not remote_incomplete:
        state = "accepted"
    elif verify.get("present") and verify_status != "verified":
        state = "incomplete"
    elif collect.get("present") and not verify.get("present"):
        state = "collected-not-verified"
    elif missing or remote_incomplete:
        state = "incomplete"
    else:
        state = "pending"

    landing = first_present(
        verify.get("landing"),
        collect.get("landing"),
        diff.get("landing"),
        index.get("landing"),
        (peer_configs.get(node_id) or {}).get("landing"),
    )
    return {
        "node_id": node_id,
        "known": node_id in known_report_nodes(snapshot),
        "state": state,
        "landing": landing,
        "counts": {
            "remote_files": count_int(first_present(verify_summary.get("remote_files"), collect_summary.get("remote_files"), diff_summary.get("remote_files"))),
            "remote_leaves": count_int(first_present(verify_summary.get("remote_leaves"), collect_summary.get("remote_leaves"), diff_summary.get("remote_leaves"), index_summary.get("remote_leaves"))),
            "remote_incomplete": remote_incomplete,
            "already_current": count_int(diff_summary.get("already_current")),
            "fetched_missing": fetched,
            "verified": verified,
            "indexed": indexed,
            "missing": missing,
            "conflicts": conflicts,
            "checksum_failed": checksum_failed,
            "errors": len(errors),
        },
        "statuses": {
            "verify": verify_status,
            "index": index_status,
        },
        "reports": {
            "diff": diff.get("report_path"),
            "collect": collect.get("report_path"),
            "verify": verify.get("report_path"),
            "index": index.get("source_report"),
            "artifact_index": (collect.get("artifact_index") or verify.get("artifact_index") or rel(artifact_index_file())) if index.get("present") else None,
        },
        "examples": {
            "local_artifacts": (index.get("examples") or {}).get("items") or [],
            "fetched": (collect.get("examples") or {}).get("fetched") or [],
            "missing": (verify.get("examples") or {}).get("missing") or (diff.get("examples") or {}).get("missing") or [],
            "conflicts": (
                (verify.get("examples") or {}).get("conflicts")
                or (collect.get("examples") or {}).get("conflicts")
                or (diff.get("examples") or {}).get("conflicts")
                or []
            ),
            "verification_failed": (collect.get("examples") or {}).get("verification_failed") or [],
        },
        "errors": errors[:max(0, limit)],
    }


def receipt_payload(snapshot: Dict[str, Any], *, node_ids: Optional[List[str]] = None,
                    limit: int = 5) -> Dict[str, Any]:
    known_nodes = known_report_nodes(snapshot)
    selected = [str(node) for node in (node_ids or known_nodes)]
    peers = {node_id: receipt_peer_payload(snapshot, node_id, limit=limit) for node_id in selected}
    state_counts = Counter(peer.get("state") for peer in peers.values())
    totals = Counter()
    for peer in peers.values():
        for key, value in (peer.get("counts") or {}).items():
            totals[key] += count_int(value)
    preflight = snapshot.get("preflight") if isinstance(snapshot.get("preflight"), dict) else {}
    preflight_summary = preflight.get("summary") or {}
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    results_summary = results_table.get("summary") or {}
    results_errors = results_table.get("errors") or []
    results_parse_errors = results_table.get("parse_errors") or []
    if not results_table:
        results_status = "missing"
    elif results_errors:
        results_status = "error"
    elif results_parse_errors:
        results_status = "parse-warn"
    else:
        results_status = "ok"
    result_paths = (results_table.get("files") or {}) if results_table else None
    automation_core = sync_automation_core(
        None,
        snapshot,
        results_table if results_table else None,
        None,
        result_paths,
        node_ids=selected,
        limit=limit,
        include_result_delta=False,
    )
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "receipt",
        "limit": limit,
        "known_peers": known_nodes,
        "requested_peers": selected if node_ids else [],
        "summary": {
            "peers": len(peers),
            "accepted": state_counts.get("accepted", 0),
            "blocked": state_counts.get("blocked", 0),
            "incomplete": state_counts.get("incomplete", 0),
            "collected_not_verified": state_counts.get("collected-not-verified", 0),
            "no_reports": state_counts.get("no-reports", 0),
            "states": dict(sorted(state_counts.items())),
            "totals": dict(sorted(totals.items())),
        },
        "preflight": {
            "present": bool(preflight),
            "status": preflight.get("status") if preflight else "missing",
            "generated_at": preflight.get("generated_at"),
            "age": format_age(preflight.get("generated_at")) if preflight else "unknown",
            "report_path": preflight.get("report_path") if preflight else rel(last_preflight_file()),
            "summary": {
                "peers": preflight_summary.get("peers", 0),
                "ready": preflight_summary.get("ready", 0),
                "blocked": preflight_summary.get("blocked", 0),
                "errors": preflight_summary.get("errors", len(preflight.get("errors") or [])),
                "warnings": preflight_summary.get("warnings", 0),
            },
        },
        "trusted_results": {
            "present": bool(results_table),
            "status": results_status,
            "generated_at": results_table.get("generated_at"),
            "age": format_age(results_table.get("generated_at")) if results_table else "unknown",
            "summary": {
                "rows": results_summary.get("rows", 0),
                "leaves": results_summary.get("leaves", 0),
                "complete_leaves": results_summary.get("complete_leaves", 0),
                "incomplete_leaves": results_summary.get("incomplete_leaves", 0),
                "parse_errors": results_summary.get("parse_errors", len(results_parse_errors)),
                "errors": len(results_errors),
            },
            "files": {
                "json": ((results_table.get("files") or {}).get("json")) or rel(results_table_file()),
                "csv": ((results_table.get("files") or {}).get("csv")) or rel(results_csv_file()),
            },
        },
        "automation_core": automation_core,
        "peers": peers,
        "files": {
            "artifact_index": rel(artifact_index_file()),
            "receipt": rel(receipt_file(selected[0] if len(selected) == 1 else None)),
        },
    }


def render_receipt_markdown(data: Dict[str, Any]) -> str:
    summary = data.get("summary") or {}
    totals = summary.get("totals") or {}
    preflight = data.get("preflight") or {}
    preflight_summary = preflight.get("summary") or {}
    trusted_results = data.get("trusted_results") or {}
    trusted_summary = trusted_results.get("summary") or {}
    trusted_files = trusted_results.get("files") or {}
    automation_core = data.get("automation_core") or {}
    lines = [
        "# Syncmate Receipt",
        "",
        f"Generated: {data.get('generated_at')}",
        f"Peers: {summary.get('peers', 0)} | accepted={summary.get('accepted', 0)} "
        f"blocked={summary.get('blocked', 0)} incomplete={summary.get('incomplete', 0)} "
        f"collected-not-verified={summary.get('collected_not_verified', 0)} no-reports={summary.get('no_reports', 0)}",
        f"Totals: fetched={totals.get('fetched_missing', 0)} verified={totals.get('verified', 0)} "
        f"indexed={totals.get('indexed', 0)} missing={totals.get('missing', 0)} "
        f"conflicts={totals.get('conflicts', 0)} checksum_failed={totals.get('checksum_failed', 0)} "
        f"remote_incomplete={totals.get('remote_incomplete', 0)}",
        "",
        "## Automation Evidence",
        "",
        f"- Preflight: status={preflight.get('status', 'missing')} age={preflight.get('age', 'unknown')} "
        f"ready={preflight_summary.get('ready', 0)} blocked={preflight_summary.get('blocked', 0)} "
        f"errors={preflight_summary.get('errors', 0)} warnings={preflight_summary.get('warnings', 0)} "
        f"report={preflight.get('report_path')}",
        f"- Trusted results: status={trusted_results.get('status', 'missing')} "
        f"rows={trusted_summary.get('rows', 0)} leaves={trusted_summary.get('leaves', 0)} "
        f"complete={trusted_summary.get('complete_leaves', 0)} parse_errors={trusted_summary.get('parse_errors', 0)} "
        f"json={trusted_files.get('json')} csv={trusted_files.get('csv')}",
    ]
    if automation_core:
        core_totals = automation_core.get("totals") or {}
        core_results = automation_core.get("results") or {}
        delta = core_results.get("delta") or {}
        if core_results.get("delta") is None:
            delta_text = "delta=unavailable"
        else:
            delta_text = (
                f"previous={delta.get('previous_rows', 0)} current={delta.get('current_rows', 0)} "
                f"added={delta.get('added_rows', 0)} changed={delta.get('changed_rows', 0)} "
                f"removed={delta.get('removed_rows', 0)}"
            )
        lines.extend([
            "",
            "## Automation Core",
            "",
            f"- Chain: {' -> '.join(automation_core.get('pipeline') or [])}",
            f"- Transfer/checksum: status={automation_core.get('status')} "
            f"missing={core_totals.get('missing', 0)} fetched={core_totals.get('fetched_missing', 0)} "
            f"checksum_verified={core_totals.get('checksum_verified', 0)} "
            f"checksum_failed={core_totals.get('checksum_failed', 0)} indexed={core_totals.get('indexed', 0)}",
            f"- Results delta: status={core_results.get('status')} rows={core_results.get('rows', 0)} "
            f"{delta_text}",
        ])
    lines.extend([
        "",
        "## Peers",
        "",
    ])
    peers = data.get("peers") or {}
    if not peers:
        lines.append("- No peer reports yet.")
    for node_id, peer in sorted(peers.items()):
        counts = peer.get("counts") or {}
        statuses = peer.get("statuses") or {}
        lines.append(
            f"- {node_id}: state={peer.get('state')} landing={peer.get('landing') or 'unknown'} "
            f"fetched={counts.get('fetched_missing', 0)} verified={counts.get('verified', 0)} "
            f"indexed={counts.get('indexed', 0)} missing={counts.get('missing', 0)} "
            f"conflicts={counts.get('conflicts', 0)} checksum_failed={counts.get('checksum_failed', 0)} "
            f"remote_incomplete={counts.get('remote_incomplete', 0)} "
            f"verify={statuses.get('verify') or 'none'} index={statuses.get('index') or 'none'}"
        )
        reports = peer.get("reports") or {}
        report_bits = [f"{key}={value}" for key, value in reports.items() if value]
        if report_bits:
            lines.append(f"  Reports: {', '.join(report_bits)}")
        examples = peer.get("examples") or {}
        local = examples.get("local_artifacts") or []
        if local:
            lines.append("  Local artifact examples:")
            for item in local:
                lines.append(f"    - {item.get('local_path') or item.get('remote_path') or item.get('path')}")
        for label in ("missing", "conflicts", "verification_failed"):
            items = examples.get(label) or []
            if items:
                lines.append(f"  {label.replace('_', ' ').title()}:")
                for item in items:
                    if isinstance(item, dict):
                        lines.append(f"    - {item.get('local_path') or item.get('remote_path') or item.get('path')}")
                    else:
                        lines.append(f"    - {item}")
        if peer.get("errors"):
            lines.append("  Errors:")
            for err in peer["errors"]:
                lines.append(f"    - {err}")
    lines.extend([
        "",
        "## Follow-Up Commands",
        "",
        "```bash",
        "python scripts/syncmate/syncmate.py preflight --write",
        "python scripts/syncmate/syncmate.py reports",
        "python scripts/syncmate/syncmate.py inventory",
        "python scripts/syncmate/syncmate.py results --write --check",
        "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify",
        "```",
        "",
    ])
    return "\n".join(lines)


def write_receipt(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    peers = list((data.get("peers") or {}).keys())
    out = receipt_file(peers[0] if len(peers) == 1 else None)
    out.write_text(render_receipt_markdown(data), encoding="utf-8")
    return out


def report_path_for(prefix: str, node_id: str) -> str:
    return rel(SYNC_DIR / f"{prefix}_{node_id}.json")


def example_remote_artifact(root: str, artifact_name: str) -> str:
    normalized = str(root or "results/runs").replace("\\", "/").strip("/")
    if normalized == "results/runs":
        return f"{normalized}/cora_GCN_r0.05/GIF_random/seed42/{artifact_name}"
    return f"{normalized}/GIF_random/seed42/{artifact_name}"


def landing_example(landing: str, remote_example: str) -> Dict[str, Any]:
    try:
        local_path = rel(local_landing_path(landing, remote_example))
        return {"remote": remote_example, "local": local_path}
    except SystemExit as exc:
        return {"remote": remote_example, "local": None, "error": str(exc)}


def layout_peer_payload(device: Dict[str, Any], node_id: str, peer: Dict[str, Any],
                        index: Dict[str, Any], results_table: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    artifact_names = artifact_names_for_peer(device, peer)
    roots = list(peer.get("result_roots") or ["results/runs"])
    landing = str(peer.get("landing") or f"results/runs/{node_id}")
    repo_path = str(peer.get("repo_path") or "")
    transport = peer_transport(peer)
    remote_example = example_remote_artifact(roots[0] if roots else "results/runs", artifact_names[0])
    index_entry = ((index.get("peers") or {}).get(node_id) or {})
    index_summary = index_entry.get("summary") or {}
    result_rows = [
        row for row in ((results_table or {}).get("rows") or [])
        if str(row.get("node_id") or "") == node_id
    ]
    return {
        "node_id": node_id,
        "transport": transport,
        "ssh": None if transport == "local" else peer.get("ssh"),
        "repo_path": repo_path,
        "remote_result_roots": roots,
        "local_landing": landing,
        "artifact_policy": artifact_policy_payload(artifact_names),
        "example_mapping": landing_example(landing, remote_example),
        "reports": {
            "remote_status": report_path_for("remote_status", node_id),
            "diff": report_path_for("last_diff", node_id),
            "collect": report_path_for("last_collect", node_id),
            "verify": report_path_for("last_verify", node_id),
            "receipt": rel(receipt_file(node_id)),
        },
        "trusted": {
            "artifact_index": rel(artifact_index_file()),
            "indexed_artifacts": int(index_summary.get("indexed") or len(index_entry.get("items") or [])),
            "index_status": index_summary.get("status") or "missing",
            "results_table_json": rel(results_table_file()),
            "results_table_csv": rel(results_csv_file()),
            "result_rows": len(result_rows),
        },
        "commands": {
            "preflight": f"python scripts/syncmate/syncmate.py preflight {node_id}",
            "dry_run": f"python scripts/syncmate/syncmate.py sync {node_id} --dry-run",
            "sync": f"python scripts/syncmate/syncmate.py sync {node_id}",
            "trace": f"python scripts/syncmate/syncmate.py trace {node_id} --check",
            "receipt": f"python scripts/syncmate/syncmate.py receipt {node_id}",
        },
    }


def layout_local_paths_payload() -> Dict[str, Any]:
    return {
        "sync_dir": rel(SYNC_DIR),
        "device_setup": rel(DEFAULT_DEVICE_FILE),
        "state": rel(STATE_FILE),
        "history": rel(history_file()),
        "preflight": rel(last_preflight_file()),
        "artifact_index": rel(artifact_index_file()),
        "results_table_json": rel(results_table_file()),
        "results_table_csv": rel(results_csv_file()),
        "dashboard": rel(STATUS_HTML),
        "brief": rel(brief_file()),
        "checklist": rel(checklist_file()),
        "runbook": rel(runbook_file()),
        "workflow": rel(workflow_file()),
        "automation_core": rel(automation_core_file()),
        "automation_core_markdown": rel(automation_core_markdown_file()),
        "acceptance": rel(acceptance_file()),
        "action_plan": rel(action_plan_file()),
        "action_plan_markdown": rel(action_plan_markdown_file()),
        "receipt": rel(receipt_file()),
        "handoff_pack": rel(handoff_pack_file()),
    }


def layout_payload_for_device(device_id: Any, role: Any, repo_path: Any,
                              artifact_policy: Any, peers: Dict[str, Any],
                              warnings: List[str], index: Dict[str, Any],
                              results_table: Optional[Dict[str, Any]], *,
                              node_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    selected = peer_ids_or_die(peers, node_ids or []) if peers else []
    device_for_policy = {"artifact_policy": artifact_policy}
    peer_payloads = {
        node_id: layout_peer_payload(device_for_policy, node_id, peers[node_id], index, results_table)
        for node_id in selected
    }
    return {
        "generated_at": now_iso(),
        "mode": "layout",
        "device": {
            "id": device_id,
            "role": role,
            "repo_path": repo_path,
            "setup_file": rel(DEFAULT_DEVICE_FILE),
            "setup_warnings": warnings,
            "peers": sorted(peers),
        },
        "local_paths": layout_local_paths_payload(),
        "core_flow": [
            "preflight",
            "remote-status",
            "manifest diff",
            "collect missing artifacts",
            "verify SHA-256",
            "artifact index",
            "trusted results table",
            "acceptance",
        ],
        "peers": peer_payloads,
    }


def layout_payload(device: Dict[str, Any], warnings: List[str], *,
                   node_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    return layout_payload_for_device(
        device.get("device_id"),
        device.get("role"),
        device.get("repo_path"),
        device.get("artifact_policy"),
        peers,
        warnings,
        load_artifact_index(),
        load_optional_json(results_table_file()),
        node_ids=node_ids,
    )


def layout_payload_from_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    peers = device.get("peer_configs") if isinstance(device.get("peer_configs"), dict) else {}
    return layout_payload_for_device(
        device.get("id"),
        device.get("role"),
        device.get("repo_path"),
        device.get("artifact_policy"),
        peers,
        device.get("setup_warnings") or [],
        snapshot.get("artifact_index") or {},
        snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {},
    )


def cmd_layout(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    data = layout_payload(device, warnings, node_ids=args.node_ids)
    if args.json:
        print_json(data)
        return 0

    device_data = data.get("device") or {}
    local_paths = data.get("local_paths") or {}
    print(f"syncmate layout: {device_data.get('id')} ({device_data.get('role')})")
    print(f"  setup: {local_paths.get('device_setup')}")
    print(f"  sync state: {local_paths.get('sync_dir')}")
    print(f"  artifact index: {local_paths.get('artifact_index')}")
    print(f"  trusted results: {local_paths.get('results_table_json')} / {local_paths.get('results_table_csv')}")
    print(f"  acceptance: {local_paths.get('acceptance')}")
    if warnings:
        for warning in warnings:
            print(f"  warning: {warning}")
    peers = data.get("peers") or {}
    if not peers:
        print("  peers: none")
        return 0
    print("  peers:")
    for node_id, peer in peers.items():
        trusted = peer.get("trusted") or {}
        example = peer.get("example_mapping") or {}
        print(f"  - {node_id}: transport={peer.get('transport')} landing={peer.get('local_landing')}")
        if peer.get("ssh"):
            print(f"    ssh: {peer.get('ssh')}")
        print(f"    repo: {peer.get('repo_path')}")
        print(f"    roots: {', '.join(peer.get('remote_result_roots') or [])}")
        print(f"    artifacts: {', '.join((peer.get('artifact_policy') or {}).get('include') or [])}")
        print(f"    example: {example.get('remote')} -> {example.get('local') or 'blocked'}")
        if example.get("error"):
            print(f"    example error: {example.get('error')}")
        print(
            f"    trusted: indexed={trusted.get('indexed_artifacts', 0)} "
            f"index_status={trusted.get('index_status')} result_rows={trusted.get('result_rows', 0)}"
        )
        print(f"    sync: {(peer.get('commands') or {}).get('sync')}")
    return 0


def compact_gate_payload(gate: Dict[str, Any], *, limit: int = 5) -> Dict[str, Any]:
    return {
        "passed": gate.get("passed"),
        "fail_on": gate.get("fail_on"),
        "require_verify": gate.get("require_verify"),
        "require_preflight": gate.get("require_preflight"),
        "require_results": gate.get("require_results"),
        "failure_count": gate.get("failure_count", 0),
        "failures": (gate.get("failures") or [])[:max(0, limit)],
        "gate_diagnostics": (gate.get("gate_diagnostics") or [])[:max(0, limit)],
        "index_check": gate.get("index_check"),
        "results_check": gate.get("results_check"),
    }


def overview_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                     fail_on: str = "warn", require_verify: bool = False,
                     require_preflight: bool = False, require_results: bool = False,
                     limit: int = 5) -> Dict[str, Any]:
    strict_gate = gate_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
    )
    summary = summary_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        max_diagnostics=limit,
    )
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    receipt = receipt_payload(snapshot, limit=limit)
    layout = layout_payload_from_snapshot(snapshot)
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    results_summary = results_table.get("summary") or {}
    preflight = snapshot.get("preflight") if isinstance(snapshot.get("preflight"), dict) else {}
    preflight_summary = preflight.get("summary") or {}
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "overview",
        "status": status_label(snapshot, diagnostics),
        "device": summary.get("device"),
        "policy": {
            "fail_on": fail_on,
            "require_verify": require_verify,
            "require_preflight": require_preflight,
            "require_results": require_results,
        },
        "totals": {
            **(summary.get("totals") or {}),
            "result_rows": results_summary.get("rows", 0),
            "parse_errors": results_summary.get("parse_errors", 0),
        },
        "preflight": {
            "status": preflight.get("status") if preflight else "missing",
            "summary": preflight_summary,
            "report_path": preflight.get("report_path") if preflight else rel(last_preflight_file()),
        },
        "layout": {
            "local_paths": layout.get("local_paths") or {},
            "core_flow": layout.get("core_flow") or [],
            "peers": layout.get("peers") or {},
        },
        "gate": compact_gate_payload(strict_gate, limit=limit),
        "summary": summary,
        "receipt": receipt,
        "workflow": {
            "status": workflow.get("status"),
            "summary": workflow.get("summary"),
            "global_stages": workflow.get("global_stages"),
        },
        "acceptance": {
            "status": acceptance.get("status"),
            "ready": acceptance.get("ready"),
            "blockers": acceptance.get("blockers") or [],
            "path": rel(acceptance_file()),
        },
        "next": next_steps,
        "diagnostics": diagnostics[:max(0, limit)],
        "files": {
            "setup": rel(DEFAULT_DEVICE_FILE),
            "state": rel(STATE_FILE),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "checklist": rel(checklist_file()),
            "runbook": rel(runbook_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "automation_core_markdown": rel(automation_core_markdown_file()),
            "acceptance": rel(acceptance_file()),
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
            "receipt": (receipt.get("files") or {}).get("receipt") or rel(receipt_file()),
        },
    }


def cmd_overview(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = overview_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=args.require_verify,
        require_preflight=args.require_preflight,
        require_results=args.require_results,
        limit=args.limit,
    )
    if args.json:
        print_json(data)
        return 0 if data["gate"]["passed"] else 1

    totals = data.get("totals") or {}
    gate = data.get("gate") or {}
    preflight = data.get("preflight") or {}
    print(
        f"syncmate overview: {((data.get('device') or {}).get('id'))} "
        f"status={data.get('status')} gate={'pass' if gate.get('passed') else 'fail'}"
    )
    print(
        f"  peers={totals.get('peers', 0)} indexed={totals.get('indexed_artifacts', 0)} "
        f"result_rows={totals.get('result_rows', 0)} diagnostics={totals.get('diagnostics', 0)}"
    )
    print(
        f"  preflight={preflight.get('status')} report={preflight.get('report_path')} "
        f"require_preflight={gate.get('require_preflight')} "
        f"require_verify={gate.get('require_verify')} "
        f"require_results={gate.get('require_results')}"
    )
    layout = data.get("layout") or {}
    peers = layout.get("peers") or {}
    if peers:
        print("  layout:")
        for node_id, peer in sorted(peers.items()):
            trusted = peer.get("trusted") or {}
            print(
                f"    - {node_id}: {peer.get('transport')} landing={peer.get('local_landing')} "
                f"indexed={trusted.get('indexed_artifacts', 0)} rows={trusted.get('result_rows', 0)}"
            )
    commands = (data.get("next") or {}).get("commands") or []
    if commands:
        print("  next:")
        for item in commands[:max(0, args.limit)]:
            print(f"    {item.get('command')}")
    failures = gate.get("failures") or []
    if failures:
        print("  gate failures:")
        for item in failures[:max(0, args.limit)]:
            node = f" [{item.get('node')}]" if item.get("node") else ""
            print(f"    {item.get('severity')}:{item.get('code')}{node} - {item.get('message')}")
    return 0 if gate.get("passed") else 1


LIFECYCLE_PHASES = [
    "setup-needed",
    "peer-needed",
    "preflight-needed",
    "sync-needed",
    "collect-needed",
    "verify-needed",
    "results-needed",
    "gate-needed",
    "accepted",
    "review",
]


def lifecycle_phase_index(phase: str) -> int:
    try:
        return LIFECYCLE_PHASES.index(phase)
    except ValueError:
        return len(LIFECYCLE_PHASES)


def lifecycle_stage_phase(stage: Dict[str, Any]) -> str:
    stage_id = stage.get("id")
    status = stage.get("status")
    if stage_id == "setup":
        return "setup-needed"
    if stage_id == "preflight":
        return "preflight-needed"
    if stage_id in ("remote-status", "diff"):
        return "sync-needed"
    if stage_id == "collect":
        return "collect-needed"
    if stage_id in ("verify", "index"):
        return "verify-needed"
    if stage_id == "results":
        return "results-needed"
    if stage_id == "gate":
        return "gate-needed" if status != "ok" else "accepted"
    return "review"


def lifecycle_attention_stages(workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
    attention = []
    for stage in workflow.get("global_stages") or []:
        if stage.get("status") in ("blocked", "action-needed", "waiting"):
            attention.append({**stage, "scope": "global"})
    for node_id, peer in sorted((workflow.get("peers") or {}).items()):
        for stage in peer.get("stages") or []:
            if stage.get("status") in ("blocked", "action-needed", "waiting"):
                attention.append({**stage, "scope": node_id, "node_id": stage.get("node_id") or node_id})
    attention.sort(key=lambda item: (
        lifecycle_phase_index(lifecycle_stage_phase(item)),
        0 if item.get("status") == "blocked" else 1 if item.get("status") == "action-needed" else 2,
        str(item.get("scope") or ""),
        str(item.get("id") or ""),
    ))
    return attention


def lifecycle_primary_command(next_steps: Dict[str, Any], phase: str,
                              snapshot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    commands = next_steps.get("commands") or []
    if commands:
        return commands[0]
    if phase == "accepted":
        node_ids = configured_peers(snapshot)
        command = "python scripts/syncmate/syncmate.py trace --check"
        if len(node_ids) == 1:
            command = f"python scripts/syncmate/syncmate.py trace {node_ids[0]} --check"
        return {
            "kind": "trace",
            "command": command,
            "reason": "inspect trusted artifact-to-result evidence and recompute checksums",
            "evidence": {
                "reads": [rel(artifact_index_file()), rel(results_table_file())],
                "writes": [],
                "inspects": [],
            },
            "effects": ["read-only", "verifies-local-checksums"],
        }
    return None


def lifecycle_current(snapshot: Dict[str, Any], workflow: Dict[str, Any],
                      acceptance: Dict[str, Any], next_steps: Dict[str, Any]) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    role = device.get("role")
    warnings = device.get("setup_warnings") or []
    peer_configs = device.get("peer_configs") or {}

    if warnings or role == "unknown":
        phase = "setup-needed"
        return {
            "phase": phase,
            "ready": False,
            "scope": "local",
            "stage": "setup",
            "status": "action-needed",
            "reason": warnings[0] if warnings else "device role is unknown",
            "primary_command": {
                "kind": "setup",
                "command": "python scripts/syncmate/syncmate.py setup-plan",
                "reason": "create the device-local setup plan",
            },
        }

    if role in ("collector", "runner+collector") and not peer_configs:
        phase = "peer-needed"
        return {
            "phase": phase,
            "ready": False,
            "scope": "local",
            "stage": "peers",
            "status": "action-needed",
            "reason": "collector has no configured runner peers",
            "primary_command": {
                "kind": "setup",
                "command": "python scripts/syncmate/syncmate.py setup-plan --role collector --peer-id <runner_id> --peer-ssh <ssh_alias> --peer-repo-path <remote_repo>",
                "reason": "prepare collector peer setup commands",
            },
        }

    if acceptance.get("ready"):
        phase = "accepted"
        return {
            "phase": phase,
            "ready": True,
            "scope": "global",
            "stage": "accepted",
            "status": "ok",
            "reason": "preflight, checksum verification, trusted index, and trusted results are accepted",
            "primary_command": lifecycle_primary_command({"commands": []}, phase, snapshot),
        }

    attention = lifecycle_attention_stages(workflow)
    actionable = next((item for item in attention if item.get("status") in ("blocked", "action-needed")), None)
    current = actionable or (attention[0] if attention else None)
    if current:
        phase = lifecycle_stage_phase(current)
        return {
            "phase": phase,
            "ready": False,
            "scope": current.get("scope"),
            "node_id": current.get("node_id"),
            "stage": current.get("id"),
            "status": current.get("status"),
            "reason": current.get("reason"),
            "stage_command": current.get("command"),
            "primary_command": lifecycle_primary_command(next_steps, phase, snapshot),
        }

    phase = "review"
    return {
        "phase": phase,
        "ready": False,
        "scope": "global",
        "stage": "review",
        "status": acceptance.get("status") or workflow.get("status") or "review",
        "reason": "no executable lifecycle stage is active, but final acceptance is not ready",
        "primary_command": lifecycle_primary_command(next_steps, phase, snapshot),
    }


def lifecycle_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                      fail_on: str = "warn",
                      require_preflight: bool = True,
                      require_verify: bool = True,
                      require_results: bool = True,
                      limit: int = 8) -> Dict[str, Any]:
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    current = lifecycle_current(snapshot, workflow, acceptance, next_steps)
    trace = trace_payload(snapshot, limit=limit, check=False)
    automation_core = automation_core_payload_from_snapshot(snapshot, limit=limit)
    commands = next_steps.get("commands") or []
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "lifecycle",
        "phase_order": LIFECYCLE_PHASES,
        "current": current,
        "ready": bool(acceptance.get("ready")),
        "policy": {
            "fail_on": fail_on,
            "require_preflight": require_preflight,
            "require_verify": require_verify,
            "require_results": require_results,
        },
        "device": {
            "id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "peers": configured_peers(snapshot),
        },
        "summary": {
            "workflow_status": workflow.get("status"),
            "acceptance_status": acceptance.get("status"),
            "automation_status": automation_core.get("status"),
            "indexed_artifacts": artifact_index_total(snapshot.get("artifact_index") or {}),
            "result_rows": ((snapshot.get("results_table") or {}).get("summary") or {}).get("rows", 0)
            if isinstance(snapshot.get("results_table"), dict) else 0,
            "trace_leaves": (trace.get("summary") or {}).get("shown_leaves", 0),
            "next_commands": len(commands),
            "manual_actions": len(next_steps.get("manual_actions") or []),
            "diagnostics": len(diagnostics),
        },
        "attention": lifecycle_attention_stages(workflow)[:max(0, limit)],
        "next": {
            "primary": current.get("primary_command"),
            "commands": commands[:max(0, limit)],
            "manual_actions": (next_steps.get("manual_actions") or [])[:max(0, limit)],
            "truncated": next_steps.get("truncated"),
        },
        "checks": {
            "trace": "python scripts/syncmate/syncmate.py trace --check",
            "acceptance": "python scripts/syncmate/syncmate.py acceptance --write --json",
            "gate": "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify --require-results",
        },
        "files": {
            "device_setup": rel(DEFAULT_DEVICE_FILE),
            "preflight": rel(last_preflight_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "acceptance": rel(acceptance_file()),
            "action_plan": rel(action_plan_file()),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
        },
    }


def print_lifecycle(data: Dict[str, Any], *, limit: int = 8) -> None:
    current = data.get("current") or {}
    summary = data.get("summary") or {}
    device = data.get("device") or {}
    print(
        f"syncmate lifecycle: phase={current.get('phase')} ready={data.get('ready')} "
        f"device={device.get('id')} role={device.get('role')}"
    )
    print(
        f"  status: workflow={summary.get('workflow_status')} acceptance={summary.get('acceptance_status')} "
        f"automation={summary.get('automation_status')}"
    )
    print(
        f"  evidence: indexed={summary.get('indexed_artifacts', 0)} rows={summary.get('result_rows', 0)} "
        f"trace_leaves={summary.get('trace_leaves', 0)} diagnostics={summary.get('diagnostics', 0)}"
    )
    print(
        f"  current: scope={current.get('scope')} stage={current.get('stage')} "
        f"status={current.get('status')} reason={current.get('reason')}"
    )
    primary = current.get("primary_command") or {}
    if primary:
        print(f"  primary: {primary.get('command')}")
        if primary.get("reason"):
            print(f"    reason: {primary.get('reason')}")
    commands = (data.get("next") or {}).get("commands") or []
    if commands:
        print("  next queue:")
        for item in commands[:max(0, limit)]:
            node = f" [{item.get('node_id')}]" if item.get("node_id") else ""
            print(f"    - {item.get('kind')}{node}: {item.get('command')}")
    manual = (data.get("next") or {}).get("manual_actions") or []
    if manual:
        print("  manual actions:")
        for item in manual[:max(0, limit)]:
            print(f"    - {item.get('kind')}: {item.get('action')}")
    checks = data.get("checks") or {}
    print(f"  checks: trace={checks.get('trace')} acceptance={checks.get('acceptance')}")
    files = data.get("files") or {}
    print(f"  files: dashboard={files.get('dashboard')} action_plan={files.get('action_plan')} acceptance={files.get('acceptance')}")


def cmd_lifecycle(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = lifecycle_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_preflight=args.require_preflight,
        require_verify=args.require_verify,
        require_results=args.require_results,
        limit=args.limit,
    )
    if args.json:
        print_json(data)
        return 0
    print_lifecycle(data, limit=args.limit)
    return 0


def summary_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                    fail_on: str = "warn", require_verify: bool = False,
                    require_preflight: bool = False, require_results: bool = False,
                    max_diagnostics: int = 5) -> Dict[str, Any]:
    gate = gate_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
    )
    peers = configured_peers(snapshot)
    orphaned_entries = orphaned_sync_entries(snapshot)
    ranked_diagnostics = sorted(
        [*diagnostics, *gate.get("gate_diagnostics", [])],
        key=lambda item: severity_rank(item.get("severity", "")),
        reverse=True,
    )
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "summary",
        "device": {
            "id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
        },
        "status": status_label(snapshot, diagnostics),
        "gate": {
            "passed": gate["passed"],
            "fail_on": gate["fail_on"],
            "require_verify": gate["require_verify"],
            "require_preflight": gate["require_preflight"],
            "require_results": gate["require_results"],
            "failure_count": gate["failure_count"],
        },
        "totals": {
            "peers": len(peers),
            "result_leaves": (snapshot.get("results") or {}).get("total_leaves", 0),
            "log_files": ((snapshot.get("progress") or {}).get("summary") or {}).get("total_log_files", 0),
            "log_errors": ((snapshot.get("progress") or {}).get("summary") or {}).get("error_logs", 0),
            "remote_reports": len(snapshot.get("remote_status") or {}),
            "bundle_inspect_reports": len(snapshot.get("bundle_inspect_reports") or {}),
            "diff_reports": len(snapshot.get("diff_reports") or {}),
            "collect_reports": len(snapshot.get("collect_reports") or {}),
            "verify_reports": len(snapshot.get("verify_reports") or {}),
            "indexed_artifacts": artifact_index_total(snapshot.get("artifact_index") or {}),
            "orphaned_sync_state": len(orphaned_entries),
            "diagnostics": len(diagnostics),
            "gate_diagnostics": len(gate.get("gate_diagnostics") or []),
        },
        "peers": [peer_summary(snapshot, peer) for peer in peers],
        "orphaned_sync_state": orphaned_entries,
        "top_diagnostics": ranked_diagnostics[:max(0, max_diagnostics)],
        "next_actions": [item.get("action") for item in ranked_diagnostics[:max(0, max_diagnostics)] if item.get("action")],
    }


def compact_workflow_attention(workflow: Dict[str, Any], *, limit: int = 5) -> List[Dict[str, Any]]:
    attention_statuses = {"blocked", "action-needed", "waiting"}
    items: List[Dict[str, Any]] = []
    for stage in workflow.get("global_stages") or []:
        if stage.get("status") in attention_statuses:
            items.append({
                "scope": "global",
                "stage": stage.get("id"),
                "status": stage.get("status"),
                "reason": stage.get("reason"),
                "command": stage.get("command"),
            })
    for node_id, peer in sorted((workflow.get("peers") or {}).items()):
        for stage in peer.get("stages") or []:
            if stage.get("status") in attention_statuses:
                items.append({
                    "scope": node_id,
                    "stage": stage.get("id"),
                    "status": stage.get("status"),
                    "reason": stage.get("reason"),
                    "command": stage.get("command"),
                })
    return items[:max(0, limit)]


def brief_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                  require_verify: bool = True, require_preflight: bool = False,
                  require_results: bool = False, limit: int = 5) -> Dict[str, Any]:
    summary = summary_payload(
        snapshot,
        diagnostics,
        fail_on="warn",
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        max_diagnostics=limit,
    )
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    reports = peer_reports_payload(
        snapshot,
        diagnostics,
        node_ids=configured_peers(snapshot) or None,
        limit=2,
    )
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    automation_core = automation_core_payload_from_snapshot(snapshot, limit=limit)
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        fail_on="warn",
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "brief",
        "require_verify": require_verify,
        "require_preflight": require_preflight,
        "require_results": require_results,
        "status": summary["status"],
        "device": summary["device"],
        "gate": summary["gate"],
        "totals": summary["totals"],
        "peers": summary["peers"],
        "top_diagnostics": summary["top_diagnostics"],
        "next_commands": next_steps.get("commands") or [],
        "manual_actions": next_steps.get("manual_actions") or [],
        "history": read_history(limit=limit),
        "reports": reports,
        "workflow": {
            "status": workflow.get("status"),
            "summary": workflow.get("summary"),
            "policy": workflow.get("policy"),
            "attention": compact_workflow_attention(workflow, limit=limit),
            "path": rel(workflow_file()),
        },
        "automation_core": automation_core,
        "acceptance": acceptance,
        "preflight": snapshot.get("preflight"),
        "files": {
            "state": rel(STATE_FILE),
            "history": rel(history_file()),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "checklist": rel(checklist_file()),
            "runbook": rel(runbook_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "acceptance": rel(acceptance_file()),
            "action_plan": rel(action_plan_file()),
            "action_plan_markdown": rel(action_plan_markdown_file()),
            "preflight": rel(last_preflight_file()),
            "results_table": rel(results_table_file()),
        },
    }


def render_brief_markdown(data: Dict[str, Any]) -> str:
    totals = data.get("totals") or {}
    gate = data.get("gate") or {}
    device = data.get("device") or {}
    files = data.get("files") or {}
    preflight = data.get("preflight") if isinstance(data.get("preflight"), dict) else {}
    preflight_summary = preflight.get("summary") or {}
    workflow = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
    workflow_summary = workflow.get("summary") or {}
    stage_statuses = workflow_summary.get("stage_statuses") or {}
    automation_core = data.get("automation_core") if isinstance(data.get("automation_core"), dict) else {}
    automation_totals = automation_core.get("totals") or {}
    automation_results = automation_core.get("results") or {}
    automation_delta = automation_results.get("delta")
    acceptance = data.get("acceptance") if isinstance(data.get("acceptance"), dict) else {}
    acceptance_core = acceptance.get("automation_core") or {}
    acceptance_results = acceptance_core.get("results") or {}
    lines = [
        "# Syncmate Brief",
        "",
        f"Generated: {data.get('generated_at')}",
        f"Device: {device.get('id')} ({device.get('role')})",
        f"Status: {data.get('status')} | Gate: {'pass' if gate.get('passed') else 'fail'} "
        f"| require_preflight={gate.get('require_preflight')} "
        f"| require_verify={gate.get('require_verify')} "
        f"| require_results={gate.get('require_results')}",
        "",
        "## Snapshot",
        "",
        f"- Peers: {totals.get('peers', 0)}",
        f"- Result leaves: {totals.get('result_leaves', 0)}",
        f"- Indexed artifacts: {totals.get('indexed_artifacts', 0)}",
        f"- Logs: {totals.get('log_files', 0)} total, {totals.get('log_errors', 0)} error-like",
        f"- Reports remote/bundle/diff/collect/verify: "
        f"{totals.get('remote_reports', 0)}/{totals.get('bundle_inspect_reports', 0)}/"
        f"{totals.get('diff_reports', 0)}/"
        f"{totals.get('collect_reports', 0)}/{totals.get('verify_reports', 0)}",
        f"- Orphaned sync state: {totals.get('orphaned_sync_state', 0)}",
        f"- Acceptance: {acceptance.get('status', 'unknown')} ready={acceptance.get('ready', False)}",
        f"- Acceptance report: {acceptance.get('acceptance_path') or files.get('acceptance')}",
        "",
        "## Acceptance",
        "",
        f"- Status: {acceptance.get('status', 'unknown')} ready={acceptance.get('ready', False)}",
        f"- Gate failures: {(acceptance.get('gate') or {}).get('failure_count', 0)}",
        f"- Workflow/Core: {(acceptance.get('workflow') or {}).get('status')} / {acceptance_core.get('status')}",
        f"- Results: status={acceptance_results.get('status')} rows={acceptance_results.get('rows', 0)}",
        f"- Landing rule: {acceptance.get('landing_rule')}",
        f"- Report: {acceptance.get('acceptance_path') or files.get('acceptance')}",
        "",
        "## Latest Preflight",
        "",
    ]
    if preflight:
        lines.extend([
            f"- Status: {preflight.get('status')}",
            f"- Generated: {preflight.get('generated_at')}",
            f"- Peers: {preflight_summary.get('peers', 0)} "
            f"ready={preflight_summary.get('ready', 0)} "
            f"blocked={preflight_summary.get('blocked', 0)}",
            f"- Errors/warnings: {preflight_summary.get('errors', 0)}/{preflight_summary.get('warnings', 0)}",
            f"- Report: {preflight.get('report_path') or files.get('preflight')}",
        ])
    else:
        lines.append("- No saved preflight report. Run `python scripts/syncmate/syncmate.py preflight --write`.")

    lines.extend(["", "## Workflow", ""])
    if workflow:
        stage_counts = ", ".join(f"{key}={value}" for key, value in sorted(stage_statuses.items())) or "none"
        lines.extend([
            f"- Status: {workflow.get('status')}",
            f"- Stage statuses: {stage_counts}",
            f"- Next/manual: {workflow_summary.get('next_commands', 0)}/{workflow_summary.get('manual_actions', 0)}",
            f"- Report: {workflow.get('path') or files.get('workflow')}",
        ])
        attention = workflow.get("attention") or []
        if attention:
            lines.append("- Attention:")
            for item in attention:
                command = f" -> `{item.get('command')}`" if item.get("command") else ""
                lines.append(
                    f"  - {item.get('scope')}/{item.get('stage')}: "
                    f"{item.get('status')} - {item.get('reason')}{command}"
                )
        else:
            lines.append("- No blocked/action-needed/waiting workflow stages.")
    else:
        lines.append("- Workflow summary unavailable. Run `python scripts/syncmate/syncmate.py workflow --write`.")

    lines.extend(["", "## Automation Core", ""])
    if automation_core:
        if automation_delta is None:
            delta_text = "unavailable"
        else:
            delta_text = (
                f"previous={automation_delta.get('previous_rows', 0)} "
                f"current={automation_delta.get('current_rows', 0)} "
                f"added={automation_delta.get('added_rows', 0)} "
                f"changed={automation_delta.get('changed_rows', 0)} "
                f"removed={automation_delta.get('removed_rows', 0)}"
            )
        lines.extend([
            f"- Status: {automation_core.get('status')}",
            f"- Missing/fetched: {automation_totals.get('missing', 0)}/{automation_totals.get('fetched_missing', 0)}",
            f"- Checksum OK/failed: {automation_totals.get('checksum_verified', 0)}/{automation_totals.get('checksum_failed', 0)}",
            f"- Verify missing/indexed: {automation_totals.get('verify_missing', 0)}/{automation_totals.get('indexed', 0)}",
            f"- Result rows: {automation_results.get('rows', 0)} status={automation_results.get('status')} delta={delta_text}",
            f"- Report: {automation_core.get('automation_core_path') or files.get('automation_core')}",
            f"- Markdown: {automation_core.get('automation_core_markdown_path') or files.get('automation_core_markdown')}",
        ])
        peers = automation_core.get("peers") or {}
        if peers:
            lines.append("- Peers:")
            for node_id, peer in sorted(peers.items()):
                counts = peer.get("counts") or {}
                lines.append(
                    f"  - {node_id}: missing={counts.get('missing', 0)} "
                    f"fetched={counts.get('fetched_missing', 0)} "
                    f"checksum_ok={counts.get('checksum_verified', 0)} "
                    f"failed={counts.get('checksum_failed', 0)} "
                    f"indexed={counts.get('indexed', 0)} verify={peer.get('verify_status')}"
                )
    else:
        lines.append("- Automation Core unavailable. Run `python scripts/syncmate/syncmate.py automation-core --write`.")

    lines.extend([
        "",
        "## Peers",
        "",
    ])
    peers = data.get("peers") or []
    if peers:
        for peer in peers:
            diff = peer.get("diff") or {}
            verify = peer.get("verify") or {}
            index = peer.get("index") or {}
            lines.append(
                f"- {peer.get('node_id')}: diff missing={diff.get('missing')} "
                f"conflicts={diff.get('conflicts')} remote_incomplete="
                f"{verify.get('remote_incomplete') or diff.get('remote_incomplete') or 0} "
                f"verify={verify.get('status') or 'none'} indexed={index.get('indexed') or 0}"
            )
    else:
        lines.append("- No configured peers.")

    lines.extend(["", "## Top Diagnostics", ""])
    diagnostics = data.get("top_diagnostics") or []
    if diagnostics:
        for item in diagnostics:
            node = f" node={item.get('node')}" if item.get("node") else ""
            lines.append(f"- [{item.get('severity')}] {item.get('code')}{node}: {item.get('message')}")
            if item.get("action"):
                lines.append(f"  Action: {item.get('action')}")
    else:
        lines.append("- No diagnostics.")

    lines.extend(["", "## Next Commands", ""])
    commands = data.get("next_commands") or []
    if commands:
        lines.append("```bash")
        for item in commands:
            lines.append(str(item.get("command")))
        lines.append("```")
    else:
        lines.append("- No executable sync commands suggested.")

    manual = data.get("manual_actions") or []
    if manual:
        lines.extend(["", "## Manual Actions", ""])
        for item in manual:
            lines.append(f"- {item.get('reason')}: {item.get('action')}")

    lines.extend(["", "## Recent History", ""])
    history = data.get("history") or []
    if history:
        for item in history:
            lines.append(
                f"- {item.get('generated_at')} {item.get('event')}: "
                f"leaves={(item.get('results') or {}).get('leaves', 0)} "
                f"indexed={(item.get('artifact_index') or {}).get('indexed', 0)} "
                f"log_errors={(item.get('progress') or {}).get('log_errors', 0)} "
                f"delta={format_history_delta(item.get('delta') or {})}"
            )
    else:
        lines.append("- No local history yet.")

    lines.extend([
        "",
        "## Useful Files",
        "",
        f"- State: {files.get('state')}",
        f"- History: {files.get('history')}",
        f"- Dashboard: {files.get('dashboard')}",
        f"- Brief: {files.get('brief')}",
        f"- Checklist: {files.get('checklist')}",
        f"- Runbook: {files.get('runbook')}",
        f"- Workflow: {files.get('workflow')}",
        f"- Automation core: {files.get('automation_core')}",
        f"- Action plan: {files.get('action_plan')}",
        f"- Action plan markdown: {files.get('action_plan_markdown')}",
        f"- Preflight: {files.get('preflight')}",
        f"- Results table: {files.get('results_table')}",
        "",
        "## Follow-Up Commands",
        "",
        "```bash",
        "python scripts/syncmate/syncmate.py preflight --write",
        "python scripts/syncmate/syncmate.py sync",
        "python scripts/syncmate/syncmate.py lifecycle --json",
        "python scripts/syncmate/syncmate.py fingerprint",
        "python scripts/syncmate/syncmate.py compare",
        "python scripts/syncmate/syncmate.py summary --require-preflight --require-verify",
        "python scripts/syncmate/syncmate.py reports",
        "python scripts/syncmate/syncmate.py receipt",
        "python scripts/syncmate/syncmate.py automation-core --write",
        "python scripts/syncmate/syncmate.py checklist --write",
        "python scripts/syncmate/syncmate.py runbook --write",
        "python scripts/syncmate/syncmate.py export --write --check",
        "python scripts/syncmate/syncmate.py results --write --check",
        "python scripts/syncmate/syncmate.py trace --check",
        "python scripts/syncmate/syncmate.py next --write --require-preflight --require-verify --require-results",
        "python scripts/syncmate/syncmate.py next --require-preflight --require-verify",
        "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify",
        "```",
        "",
    ])
    return "\n".join(lines)


def write_brief(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = brief_file()
    out.write_text(render_brief_markdown(data), encoding="utf-8")
    return out


def cmd_summary(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = summary_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=args.require_verify,
        require_preflight=args.require_preflight,
        require_results=args.require_results,
        max_diagnostics=args.max_diagnostics,
    )
    if args.json:
        print_json(data)
        return 0 if data["gate"]["passed"] else 1

    device_info = data["device"]
    gate_state = "pass" if data["gate"]["passed"] else "fail"
    print(
        f"syncmate summary: {device_info.get('id')} ({device_info.get('role')}) "
        f"status={data['status']} gate={gate_state} "
        f"require_preflight={data['gate'].get('require_preflight')} "
        f"require_verify={data['gate'].get('require_verify')} "
        f"require_results={data['gate'].get('require_results')}"
    )
    totals = data["totals"]
    print(
        f"  peers={totals['peers']} leaves={totals['result_leaves']} indexed={totals['indexed_artifacts']} "
        f"logs={totals['log_files']} log_errors={totals['log_errors']} "
        f"orphaned={totals['orphaned_sync_state']} "
        f"reports remote/bundle/diff/collect/verify="
        f"{totals['remote_reports']}/{totals.get('bundle_inspect_reports', 0)}/"
        f"{totals['diff_reports']}/{totals['collect_reports']}/{totals['verify_reports']}"
    )
    for peer in data["peers"]:
        diff = peer["diff"]
        verify = peer["verify"]
        index = peer["index"]
        print(
            f"  - {peer['node_id']}: diff missing={diff.get('missing')} conflicts={diff.get('conflicts')} "
            f"remote_incomplete={verify.get('remote_incomplete') or diff.get('remote_incomplete') or 0} "
            f"verify={verify.get('status') or 'none'} index={index.get('indexed') or 0}"
        )
    if data["top_diagnostics"]:
        print("  top diagnostics:")
        for item in data["top_diagnostics"]:
            node = f" node={item['node']}" if item.get("node") else ""
            print(f"    [{item['severity']}] {item['code']}{node}: {item['message']}")
            print(f"       action: {item['action']}")
    else:
        print("  ok: no diagnostics")
    return 0 if data["gate"]["passed"] else 1


def cmd_brief(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    data = brief_payload(
        snapshot,
        diagnostics,
        require_verify=args.require_verify,
        require_preflight=args.require_preflight,
        require_results=args.require_results,
        limit=args.limit,
    )
    out_path = None
    written_action_plan = None
    if args.write:
        action_plan = next_steps_payload(
            snapshot,
            diagnostics,
            require_verify=args.require_verify,
            require_preflight=args.require_preflight,
            require_results=args.require_results,
            limit=args.limit,
        )
        written_action_plan = write_action_plan(action_plan)
        data["action_plan_path"] = written_action_plan["json"]
        data["action_plan_markdown_path"] = written_action_plan["markdown"]
        data.setdefault("files", {})["action_plan"] = written_action_plan["json"]
        data.setdefault("files", {})["action_plan_markdown"] = written_action_plan["markdown"]
        out_path = write_brief(data)
        data["brief_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0 if data["gate"]["passed"] else 1
    if args.write:
        print(f"syncmate brief: {rel(out_path)}")
        print(f"  status: {data['status']} gate={'pass' if data['gate']['passed'] else 'fail'}")
        print(f"  diagnostics: {len(data.get('top_diagnostics') or [])}")
        print(f"  next commands: {len(data.get('next_commands') or [])}")
        if written_action_plan:
            print(f"  action plan: {written_action_plan['json']}")
            print(f"  markdown: {written_action_plan['markdown']}")
    else:
        print(render_brief_markdown(data))
    return 0 if data["gate"]["passed"] else 1


def print_examples(label: str, items: List[Any]) -> None:
    if not items:
        return
    print(f"      {label}:")
    for item in items:
        if isinstance(item, dict):
            path = item.get("path") or item.get("remote_path") or item.get("local_path") or str(item)
            extra = []
            if item.get("local_path") and item.get("path"):
                extra.append(f"local={item.get('local_path')}")
            if item.get("local_sha256"):
                extra.append(f"local_sha={str(item.get('local_sha256'))[:10]}")
            if item.get("actual_sha256"):
                extra.append(f"actual={str(item.get('actual_sha256'))[:10]}")
            suffix = f" ({', '.join(extra)})" if extra else ""
            print(f"        - {path}{suffix}")
        else:
            print(f"        - {item}")


def print_remote_inventory_incomplete(info: Optional[Dict[str, Any]]) -> None:
    if not info:
        return
    missing = format_missing_counts(info.get("missing_counts") or {})
    suffix = f" ({missing})" if missing else ""
    print(f"      remote incomplete: {info.get('incomplete', 0)} leaf/leaves{suffix}")
    for item in info.get("examples") or []:
        leaf = item.get("remote_leaf") or f"{item.get('cell')}/{item.get('method_strategy')}/{item.get('seed')}"
        missing_names = ",".join(item.get("missing") or [])
        print(f"        - {leaf} missing={missing_names or 'unknown'}")


def print_report_line(kind: str, report: Dict[str, Any]) -> None:
    if not report.get("present"):
        print(f"    {kind}: none")
        return
    summary = report.get("summary") or {}
    path = report.get("report_path") or report.get("source_report") or ""
    if kind == "remote":
        print(
            f"    remote: age={report.get('age')} git={summary.get('git_short_sha')} "
            f"dirty={summary.get('git_dirty')} leaves={summary.get('result_leaves')} "
            f"fingerprint={summary.get('fingerprint') or 'none'} "
            f"log_errors={summary.get('log_errors', 0)} "
            f"errors={len(report.get('errors') or [])} {path}"
        )
    elif kind == "diff":
        print(
            f"    diff: age={report.get('age')} remote={summary.get('remote_files')} "
            f"leaves={summary.get('remote_leaves')} incomplete={summary.get('remote_incomplete', 0)} "
            f"missing={summary.get('missing')} conflicts={summary.get('conflicts')} {path}"
        )
    elif kind == "bundle_inspect":
        print(
            f"    bundle: age={report.get('age')} status={summary.get('audit_status')} "
            f"files={summary.get('manifest_files')} leaves={summary.get('manifest_leaves')} "
            f"incomplete={summary.get('manifest_incomplete')} warnings={summary.get('audit_warnings')} "
            f"errors={summary.get('audit_errors')} {path}"
        )
    elif kind == "collect":
        print(
            f"    collect: age={report.get('age')} fetched={summary.get('fetched_missing')} "
            f"verified={summary.get('verified')} incomplete={summary.get('remote_incomplete', 0)} "
            f"conflicts={summary.get('conflicts')} failed={summary.get('failed')} {path}"
        )
    elif kind == "verify":
        print(
            f"    verify: age={report.get('age')} status={summary.get('status')} "
            f"current={summary.get('verified_current')} missing={summary.get('missing')} "
            f"conflicts={summary.get('conflicts')} remote_incomplete={summary.get('remote_incomplete', 0)} {path}"
        )
    elif kind == "index":
        print(
            f"    index: age={report.get('age')} status={summary.get('status')} "
            f"indexed={summary.get('indexed')} remote_incomplete={summary.get('remote_incomplete', 0)} {path}"
        )
    for label, items in (report.get("examples") or {}).items():
        print_examples(label, items)
    print_remote_inventory_incomplete(report.get("remote_inventory_incomplete"))


def cmd_reports(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    data = peer_reports_payload(
        snapshot,
        diagnostics,
        node_ids=args.node_ids or None,
        limit=args.limit,
    )
    if args.json:
        print_json(data)
        return 0

    print(f"syncmate reports: peers={data['summary']['peers']} known={data['summary']['known']} unknown={data['summary']['unknown']}")
    if not data["peers"]:
        print("  no saved peer reports yet")
        print("  next: run remote-status <node_id> --apply or collect <node_id> --diff")
        return 0
    for node_id, peer in sorted(data["peers"].items()):
        marker = "" if peer.get("known") else " (unknown)"
        print(f"  - {node_id}{marker}")
        print_report_line("remote", peer["remote"])
        print_report_line("bundle_inspect", peer["bundle_inspect"])
        print_report_line("diff", peer["diff"])
        print_report_line("collect", peer["collect"])
        print_report_line("verify", peer["verify"])
        print_report_line("index", peer["index"])
        if peer.get("diagnostics"):
            print("    diagnostics:")
            for item in peer["diagnostics"]:
                print(f"      [{item['severity']}] {item['code']}: {item['message']}")
    return 0


def cmd_preflight(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    data = preflight_payload(
        device,
        warnings,
        config_path=args.config,
        node_ids=args.node_ids,
    )
    out_path = None
    if args.write:
        out_path = write_preflight_report(data)
        data["report_path"] = rel(out_path)
    if args.json:
        print_json(data)
    else:
        print_preflight(data, limit=args.limit)
    return 0 if data.get("status") != "blocked" else 1


def cmd_receipt(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = receipt_payload(
        snapshot,
        node_ids=args.node_ids or None,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_receipt(data)
        data["receipt_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0
    if args.write:
        print(f"syncmate receipt: {rel(out_path)}")
    else:
        print(render_receipt_markdown(data))
    return 0


def result_rows_for_node(results_table: Any, node_id: str) -> List[Dict[str, Any]]:
    if not isinstance(results_table, dict):
        return []
    return [
        row for row in (results_table.get("rows") or [])
        if isinstance(row, dict) and str(row.get("node_id") or "") == node_id
    ]


def landing_path_status(landing: Any) -> Dict[str, Any]:
    target = safe_repo_path(landing)
    if target is None:
        return {
            "safe": False,
            "exists": False,
            "absolute": None,
            "reason": "landing is not a safe repo-relative path",
        }
    return {
        "safe": True,
        "exists": target.is_dir(),
        "absolute": str(target),
        "reason": None,
    }


def landings_payload(snapshot: Dict[str, Any], *,
                     node_ids: Optional[List[str]] = None,
                     limit: int = 5) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    peer_configs = device.get("peer_configs") or {}
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    result_nodes = {
        str(row.get("node_id"))
        for row in (results_table.get("rows") or [])
        if isinstance(row, dict) and row.get("node_id")
    }
    known_nodes = sorted(set(known_report_nodes(snapshot)) | result_nodes)
    selected = [str(node) for node in (node_ids or known_nodes)]
    inventory = inventory_from_index(snapshot.get("artifact_index") or {}, node_ids=selected or None)
    peers: Dict[str, Any] = {}
    state_counts: Counter[str] = Counter()
    totals = Counter()

    for node_id in selected:
        receipt_peer = receipt_peer_payload(snapshot, node_id, limit=limit)
        peer_config = peer_configs.get(node_id) or {}
        inv_peer = (inventory.get("peers") or {}).get(node_id) or {}
        inv_summary = inv_peer.get("summary") or {}
        rows = result_rows_for_node(results_table, node_id)
        landing = (
            receipt_peer.get("landing")
            or inv_peer.get("landing")
            or peer_config.get("landing")
            or f"results/runs/{node_id}"
        )
        path_status = landing_path_status(landing)
        counts = receipt_peer.get("counts") or {}
        for key, value in counts.items():
            totals[key] += count_int(value)
        totals["result_rows"] += len(rows)
        totals["complete_leaves"] += count_int(inv_summary.get("complete"))
        totals["incomplete_leaves"] += count_int(inv_summary.get("incomplete"))
        totals["existing_landings"] += 1 if path_status.get("exists") else 0
        state_counts[str(receipt_peer.get("state") or "unknown")] += 1
        peers[node_id] = {
            "node_id": node_id,
            "configured": node_id in configured_peers(snapshot),
            "state": receipt_peer.get("state"),
            "landing": landing,
            "landing_path": path_status,
            "counts": counts,
            "statuses": receipt_peer.get("statuses") or {},
            "reports": receipt_peer.get("reports") or {},
            "inventory": {
                "summary": inv_summary,
                "examples": (inv_peer.get("leaves") or [])[:max(0, limit)],
            },
            "results": {
                "rows": len(rows),
                "examples": [compact_result_row(row) for row in rows[:max(0, limit)]],
                "table": rel(results_table_file()) if results_table else None,
                "csv": rel(results_csv_file()) if results_table else None,
            },
            "examples": receipt_peer.get("examples") or {},
            "commands": {
                "layout": f"python scripts/syncmate/syncmate.py layout {node_id}",
                "reports": f"python scripts/syncmate/syncmate.py reports {node_id}",
                "diff": f"python scripts/syncmate/syncmate.py collect {node_id} --diff",
                "collect": f"python scripts/syncmate/syncmate.py collect {node_id} --apply",
                "verify": f"python scripts/syncmate/syncmate.py verify {node_id} --apply",
                "results": "python scripts/syncmate/syncmate.py results --write --check",
                "trace": f"python scripts/syncmate/syncmate.py trace {node_id} --check",
                "acceptance": f"python scripts/syncmate/syncmate.py acceptance {node_id} --write --json",
                "sync": f"python scripts/syncmate/syncmate.py sync {node_id}",
            },
        }

    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "landings",
        "device": {
            "id": device.get("id"),
            "role": device.get("role"),
        },
        "landing_rule": "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/",
        "known_peers": known_nodes,
        "requested_peers": selected if node_ids else [],
        "summary": {
            "peers": len(peers),
            "states": dict(sorted(state_counts.items())),
            "totals": dict(sorted(totals.items())),
        },
        "peers": peers,
        "files": {
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
            "acceptance": rel(acceptance_file()),
            "dashboard": rel(STATUS_HTML),
        },
        "errors": inventory.get("errors") or [],
    }


def cmd_landings(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = landings_payload(
        snapshot,
        node_ids=args.node_ids or None,
        limit=args.limit,
    )
    if args.json:
        print_json(data)
        return 0

    summary = data.get("summary") or {}
    totals = summary.get("totals") or {}
    print(f"syncmate landings: {((data.get('device') or {}).get('id'))} ({((data.get('device') or {}).get('role'))})")
    print(f"  rule: {data.get('landing_rule')}")
    print(
        f"  peers={summary.get('peers', 0)} existing={totals.get('existing_landings', 0)} "
        f"indexed={totals.get('indexed', 0)} rows={totals.get('result_rows', 0)} "
        f"missing={totals.get('missing', 0)} checksum_failed={totals.get('checksum_failed', 0)}"
    )
    peers = data.get("peers") or {}
    if not peers:
        print("  peers: none")
    for node_id, peer in sorted(peers.items()):
        counts = peer.get("counts") or {}
        inv_summary = ((peer.get("inventory") or {}).get("summary") or {})
        rows = ((peer.get("results") or {}).get("rows") or 0)
        path_status = peer.get("landing_path") or {}
        print(
            f"  - {node_id}: state={peer.get('state')} landing={peer.get('landing')} "
            f"exists={path_status.get('exists')} rows={rows} indexed={counts.get('indexed', 0)} "
            f"complete={inv_summary.get('complete', 0)} incomplete={inv_summary.get('incomplete', 0)}"
        )
        if not path_status.get("safe"):
            print(f"    landing issue: {path_status.get('reason')}")
        examples = ((peer.get("inventory") or {}).get("examples") or [])
        for leaf in examples[:max(0, args.limit)]:
            print(
                f"    leaf: {leaf.get('local_leaf')} complete={leaf.get('complete')} "
                f"artifacts={','.join(leaf.get('artifacts') or [])} "
                f"missing={','.join(leaf.get('missing') or []) or 'none'}"
            )
        print(f"    next: {landing_next_command(peer)}")
    files = data.get("files") or {}
    print(f"  files: index={files.get('artifact_index')} results={files.get('results_json')} acceptance={files.get('acceptance')}")
    return 0


def landing_next_command(peer: Dict[str, Any]) -> Optional[str]:
    commands = peer.get("commands") or {}
    counts = peer.get("counts") or {}
    rows = ((peer.get("results") or {}).get("rows") or 0)
    state = peer.get("state")
    if counts.get("missing"):
        return commands.get("collect")
    if counts.get("verify_missing") or state in ("collected-not-verified", "incomplete"):
        return commands.get("verify")
    if rows == 0 and counts.get("indexed"):
        return commands.get("results")
    if state == "accepted" and rows:
        return commands.get("acceptance")
    return commands.get("sync")


CHECKSUM_FAILURE_STATES = {"mismatch", "local-missing", "unsafe-path", "missing-expected-sha"}


def trace_result_rows_for_leaf(rows: List[Dict[str, Any]], leaf: Dict[str, Any]) -> List[Dict[str, Any]]:
    node_id = leaf.get("node_id")
    local_leaf = leaf.get("local_leaf")
    exact = [
        row for row in rows
        if row.get("node_id") == node_id and row.get("local_leaf") == local_leaf
    ]
    if exact:
        return exact
    return [
        row for row in rows
        if row.get("node_id") == node_id
        and row.get("cell") == leaf.get("cell")
        and row.get("method_strategy") == leaf.get("method_strategy")
        and row.get("seed") == leaf.get("seed")
    ]


def trace_artifact_entry(artifact_name: str, artifact: Optional[Dict[str, Any]], *,
                         check: bool) -> Dict[str, Any]:
    artifact = artifact or {}
    local_path = artifact.get("local_path")
    expected_sha = artifact.get("sha256")
    target = safe_repo_path(local_path) if local_path else None
    safe = bool(target) if local_path else True
    exists = bool(target and target.is_file())
    actual_sha = None
    if not artifact:
        checksum_status = "not-indexed"
    elif not check:
        checksum_status = "not-checked"
    elif not local_path:
        checksum_status = "not-indexed"
    elif target is None:
        checksum_status = "unsafe-path"
    elif not target.is_file():
        checksum_status = "local-missing"
    else:
        actual_sha = sha256_file(target)
        if not expected_sha:
            checksum_status = "missing-expected-sha"
        elif actual_sha == expected_sha:
            checksum_status = "ok"
        else:
            checksum_status = "mismatch"

    return {
        "artifact": artifact_name,
        "indexed": bool(artifact),
        "remote_path": artifact.get("remote_path"),
        "local_path": local_path,
        "sha256": expected_sha,
        "exists": exists,
        "safe": safe,
        "checksum_status": checksum_status,
        "actual_sha256": actual_sha,
        "verified_at": artifact.get("verified_at"),
        "source_report": artifact.get("source_report"),
    }


def trace_leaf_status(leaf: Dict[str, Any], artifacts: List[Dict[str, Any]],
                      result_rows: List[Dict[str, Any]]) -> str:
    statuses = {item.get("checksum_status") for item in artifacts}
    if statuses & CHECKSUM_FAILURE_STATES:
        return "checksum-failed"
    if leaf.get("missing"):
        return "incomplete"
    if result_rows:
        return "trusted-result"
    if leaf.get("complete"):
        return "indexed-no-results"
    return "indexed"


def trace_payload(snapshot: Dict[str, Any], *,
                  node_ids: Optional[List[str]] = None,
                  limit: int = 20,
                  check: bool = False) -> Dict[str, Any]:
    index = snapshot.get("artifact_index") or {}
    trusted = export_payload_from_index(index, node_ids=node_ids, include_incomplete=True)
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    result_rows = result_rows_from_table(results_table)
    selected_leaves = (trusted.get("leaves") or [])[:max(0, limit)]
    leaves: List[Dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    checksum_counts: Counter[str] = Counter()

    for leaf in selected_leaves:
        artifact_map = leaf.get("artifacts") or {}
        expected = leaf.get("expected_artifacts") or sorted(artifact_map)
        artifacts = [
            trace_artifact_entry(name, artifact_map.get(name), check=check)
            for name in expected
        ]
        rows = trace_result_rows_for_leaf(result_rows, leaf)
        status = trace_leaf_status(leaf, artifacts, rows)
        status_counts[status] += 1
        for artifact in artifacts:
            checksum_counts[str(artifact.get("checksum_status") or "unknown")] += 1
        leaves.append({
            "node_id": leaf.get("node_id"),
            "landing": leaf.get("landing"),
            "status": status,
            "complete": bool(leaf.get("complete")),
            "trusted_for_results": status == "trusted-result",
            "cell": leaf.get("cell"),
            "method_strategy": leaf.get("method_strategy"),
            "seed": leaf.get("seed"),
            "layout": leaf.get("layout"),
            "remote_leaf": leaf.get("remote_leaf"),
            "local_leaf": leaf.get("local_leaf"),
            "expected_artifacts": expected,
            "missing": leaf.get("missing") or [],
            "artifacts": artifacts,
            "results": {
                "rows": len(rows),
                "examples": [compact_result_row(row) for row in rows[:max(0, limit)]],
                "table": rel(results_table_file()) if results_table else None,
                "csv": rel(results_csv_file()) if results_table else None,
            },
            "evidence": {
                "source_report": leaf.get("source_report"),
                "artifact_index": trusted.get("index_path") or rel(artifact_index_file()),
                "results_table": rel(results_table_file()) if results_table else None,
            },
        })

    summary = trusted.get("summary") or {}
    checksum_failed = sum(checksum_counts.get(state, 0) for state in CHECKSUM_FAILURE_STATES)
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "trace",
        "check": check,
        "device": {
            "id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
        },
        "requested_peers": sorted(set(node_ids or [])),
        "landing_rule": "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/",
        "summary": {
            "shown_leaves": len(leaves),
            "indexed_leaves": summary.get("indexed_leaves", summary.get("leaves", 0)),
            "complete_leaves": summary.get("complete_leaves", 0),
            "incomplete_leaves": summary.get("incomplete_leaves", 0),
            "indexed_artifacts": summary.get("indexed_artifacts", artifact_index_total(index)),
            "result_rows": len(result_rows),
            "status_counts": dict(sorted(status_counts.items())),
            "checksum_counts": dict(sorted(checksum_counts.items())),
            "checksum_failed": checksum_failed,
            "truncated": len(trusted.get("leaves") or []) > len(leaves),
        },
        "leaves": leaves,
        "files": {
            "artifact_index": trusted.get("index_path") or rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
            "automation_core": rel(automation_core_file()),
            "acceptance": rel(acceptance_file()),
        },
        "errors": trusted.get("errors") or [],
    }


def print_trace(data: Dict[str, Any], *, limit: int = 20) -> None:
    device = data.get("device") or {}
    summary = data.get("summary") or {}
    print(f"syncmate trace: {device.get('id')} ({device.get('role')}) check={data.get('check')}")
    print(f"  rule: {data.get('landing_rule')}")
    print(
        f"  leaves shown/indexed={summary.get('shown_leaves', 0)}/{summary.get('indexed_leaves', 0)} "
        f"complete={summary.get('complete_leaves', 0)} incomplete={summary.get('incomplete_leaves', 0)} "
        f"artifacts={summary.get('indexed_artifacts', 0)} result_rows={summary.get('result_rows', 0)} "
        f"checksum_failed={summary.get('checksum_failed', 0)}"
    )
    for error in data.get("errors") or []:
        print(f"  error: {error}")
    leaves = data.get("leaves") or []
    if not leaves:
        print("  no trusted trace leaves yet")
        print("  next: run sync <node_id>, or collect <node_id> --apply then results --write --check")
    for leaf in leaves[:max(0, limit)]:
        results = leaf.get("results") or {}
        print(
            f"  - {leaf.get('node_id')}: {leaf.get('cell')}/{leaf.get('method_strategy')}/{leaf.get('seed')} "
            f"status={leaf.get('status')} complete={leaf.get('complete')} rows={results.get('rows', 0)}"
        )
        print(f"    remote: {leaf.get('remote_leaf')}")
        print(f"    local: {leaf.get('local_leaf')}")
        for artifact in leaf.get("artifacts") or []:
            sha = str(artifact.get("sha256") or "")[:10] or "none"
            actual = str(artifact.get("actual_sha256") or "")[:10]
            actual_text = f" actual={actual}" if actual else ""
            print(
                f"    artifact: {artifact.get('artifact')} status={artifact.get('checksum_status')} "
                f"exists={artifact.get('exists')} sha={sha}{actual_text} "
                f"local={artifact.get('local_path')}"
            )
        for row in results.get("examples") or []:
            print(
                f"    result: method={row.get('method')} strategy={row.get('strategy_full')} "
                f"status={row.get('status')} f1_after={row.get('f1_after')} mia_auc={row.get('mia_auc')}"
            )
    if summary.get("truncated"):
        print("  note: output truncated; rerun with --limit for more leaves")
    files = data.get("files") or {}
    print(f"  files: index={files.get('artifact_index')} results={files.get('results_json')} acceptance={files.get('acceptance')}")


def cmd_trace(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = trace_payload(
        snapshot,
        node_ids=args.node_ids or None,
        limit=args.limit,
        check=args.check,
    )
    failed = bool(data.get("errors") or ((data.get("summary") or {}).get("checksum_failed") or 0))
    if args.json:
        print_json(data)
        return 1 if failed else 0
    print_trace(data, limit=args.limit)
    return 1 if failed else 0


def compact_checklist_peer(peer: Dict[str, Any], *, limit: int = 5) -> Dict[str, Any]:
    inventory = peer.get("inventory") or {}
    results = peer.get("results") or {}
    return {
        "node_id": peer.get("node_id"),
        "configured": peer.get("configured"),
        "state": peer.get("state"),
        "landing": peer.get("landing"),
        "landing_exists": (peer.get("landing_path") or {}).get("exists"),
        "counts": peer.get("counts") or {},
        "inventory_summary": inventory.get("summary") or {},
        "result_rows": results.get("rows", 0),
        "result_examples": (results.get("examples") or [])[:max(0, limit)],
        "next_command": landing_next_command(peer),
    }


def checklist_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                      node_ids: Optional[List[str]] = None,
                      fail_on: str = "warn",
                      require_preflight: bool = True,
                      require_verify: bool = True,
                      require_results: bool = True,
                      limit: int = 8) -> Dict[str, Any]:
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        node_ids=node_ids,
        fail_on=fail_on,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    landings = landings_payload(
        snapshot,
        node_ids=node_ids,
        limit=limit,
    )
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    peers = {
        node_id: compact_checklist_peer(peer, limit=limit)
        for node_id, peer in sorted((landings.get("peers") or {}).items())
    }
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "checklist",
        "checklist_path": rel(checklist_file()),
        "device": landings.get("device") or {},
        "status": acceptance.get("status"),
        "ready": acceptance.get("ready"),
        "landing_rule": landings.get("landing_rule"),
        "policy": acceptance.get("policy") or {},
        "acceptance": {
            "status": acceptance.get("status"),
            "ready": acceptance.get("ready"),
            "blockers": acceptance.get("blockers") or [],
            "path": acceptance.get("acceptance_path") or rel(acceptance_file()),
            "gate": acceptance.get("gate") or {},
        },
        "landings": {
            "summary": landings.get("summary") or {},
            "peers": peers,
        },
        "next": {
            "commands": (next_steps.get("commands") or [])[:max(0, limit)],
            "manual_actions": (next_steps.get("manual_actions") or [])[:max(0, limit)],
        },
        "files": {
            "checklist": rel(checklist_file()),
            "acceptance": rel(acceptance_file()),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
        },
    }


def render_checklist_markdown(data: Dict[str, Any]) -> str:
    device = data.get("device") or {}
    acceptance = data.get("acceptance") or {}
    landings = data.get("landings") or {}
    summary = landings.get("summary") or {}
    totals = (summary.get("totals") or {})
    files = data.get("files") or {}
    lines = [
        "# Syncmate Checklist",
        "",
        f"Generated: {data.get('generated_at')}",
        f"Device: {device.get('id')} ({device.get('role')})",
        f"Status: {data.get('status')} ready={data.get('ready')}",
        f"Landing rule: {data.get('landing_rule')}",
        "",
        "## Acceptance",
        "",
        f"- Verdict: {acceptance.get('status')} ready={acceptance.get('ready')}",
        f"- Blockers: {', '.join(acceptance.get('blockers') or []) or 'none'}",
        f"- Report: {acceptance.get('path')}",
        "",
        "## Landings",
        "",
        f"- Peers: {summary.get('peers', 0)}",
        f"- Existing landing folders: {totals.get('existing_landings', 0)}",
        f"- Indexed artifacts: {totals.get('indexed', 0)}",
        f"- Trusted result rows: {totals.get('result_rows', 0)}",
        f"- Missing/checksum failed: {totals.get('missing', 0)}/{totals.get('checksum_failed', 0)}",
        "",
    ]
    peers = (landings.get("peers") or {})
    if not peers:
        lines.append("- No peer landings yet.")
    for node_id, peer in peers.items():
        counts = peer.get("counts") or {}
        inv = peer.get("inventory_summary") or {}
        lines.append(
            f"- {node_id}: state={peer.get('state')} landing={peer.get('landing')} "
            f"exists={peer.get('landing_exists')} rows={peer.get('result_rows', 0)} "
            f"indexed={counts.get('indexed', 0)} complete={inv.get('complete', 0)} "
            f"incomplete={inv.get('incomplete', 0)}"
        )
        if peer.get("next_command"):
            lines.append(f"  next: `{peer.get('next_command')}`")
    lines.extend(["", "## Next Commands", ""])
    commands = (data.get("next") or {}).get("commands") or []
    if commands:
        for idx, item in enumerate(commands, start=1):
            lines.append(f"{idx}. `{item.get('command')}`")
            lines.append(f"   {item.get('kind')}: {item.get('reason')}")
    else:
        lines.append("- No executable next commands suggested.")
    manual = (data.get("next") or {}).get("manual_actions") or []
    lines.extend(["", "## Manual Actions", ""])
    if manual:
        for item in manual:
            lines.append(f"- {item.get('kind')}: {item.get('reason')} :: `{item.get('action')}`")
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Files",
        "",
        f"- Checklist: {files.get('checklist')}",
        f"- Acceptance: {files.get('acceptance')}",
        f"- Dashboard: {files.get('dashboard')}",
        f"- Brief: {files.get('brief')}",
        f"- Workflow: {files.get('workflow')}",
        f"- Automation core: {files.get('automation_core')}",
        f"- Results: {files.get('results_json')} / {files.get('results_csv')}",
        f"- Artifact index: {files.get('artifact_index')}",
    ])
    return "\n".join(lines) + "\n"


def write_checklist(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = checklist_file()
    data = {**data, "checklist_path": rel(out)}
    out.write_text(render_checklist_markdown(data), encoding="utf-8")
    return out


def cmd_checklist(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = checklist_payload(
        snapshot,
        diagnostics,
        node_ids=args.node_ids or None,
        fail_on=fail_on,
        require_preflight=args.require_preflight,
        require_verify=args.require_verify,
        require_results=args.require_results,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_checklist(data)
        data["checklist_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0 if data.get("ready") else 1
    if args.write:
        print(f"syncmate checklist: {rel(out_path)}")
        print(f"  status={data.get('status')} ready={data.get('ready')}")
        print(f"  acceptance: {(data.get('files') or {}).get('acceptance')}")
    else:
        print(render_checklist_markdown(data), end="")
    return 0 if data.get("ready") else 1


def runbook_command(kind: str, command: str, reason: str,
                    *, node_id: Optional[str] = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "kind": kind,
        "command": command,
        "reason": reason,
    }
    if node_id:
        item["node_id"] = node_id
    return item


def runbook_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                    node_ids: Optional[List[str]] = None,
                    limit: int = 8) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    peer_configs = device.get("peer_configs") if isinstance(device.get("peer_configs"), dict) else {}
    role = str(device.get("role") or "unknown")
    warnings = list(device.get("setup_warnings") or [])
    selected = peer_ids_or_die(peer_configs, node_ids or []) if node_ids and peer_configs else sorted(peer_configs)
    if node_ids and not peer_configs:
        selected = []
    landings = landings_payload(snapshot, node_ids=selected, limit=limit) if selected else {
        "summary": {"peers": 0, "totals": {}},
        "peers": {},
    }

    commands: List[Dict[str, Any]] = [
        runbook_command("inspect", "python scripts/syncmate/syncmate.py self", "identify this checkout and role"),
        runbook_command("inspect", "python scripts/syncmate/syncmate.py layout", "show the result landing contract"),
    ]
    manual_actions: List[Dict[str, Any]] = []

    if warnings or role == "unknown":
        commands.extend([
            runbook_command("setup", "python scripts/syncmate/syncmate.py setup-plan", "draft a safe first-run setup"),
            runbook_command(
                "setup",
                "python scripts/syncmate/syncmate.py init-device --role collector --device-id <local_id>",
                "create the untracked collector setup on the receiving machine",
            ),
            runbook_command(
                "setup",
                "python scripts/syncmate/syncmate.py init-device --role runner --device-id <runner_id> --collector-hint <local_id>",
                "create the untracked runner setup on the experiment machine",
            ),
        ])
        manual_actions.append({
            "kind": "setup",
            "reason": "device setup is missing or incomplete",
            "action": "choose which checkout is collector and which checkout is runner before running sync",
        })

    if role in ("collector", "runner+collector"):
        if selected:
            commands.append(runbook_command(
                "preflight",
                "python scripts/syncmate/syncmate.py preflight --write",
                "record local setup readiness before contacting peers",
            ))
            for node_id in selected[:max(0, limit)]:
                commands.extend([
                    runbook_command(
                        "sync",
                        f"python scripts/syncmate/syncmate.py sync {node_id}",
                        "run the full incremental collect, checksum, results, and checklist path",
                        node_id=node_id,
                    ),
                    runbook_command(
                        "inspect",
                        f"python scripts/syncmate/syncmate.py landings {node_id}",
                        "inspect where this peer's trusted artifacts landed",
                        node_id=node_id,
                    ),
                    runbook_command(
                        "handoff",
                        f"python scripts/syncmate/syncmate.py checklist {node_id} --write",
                        "refresh the short operation checklist from saved evidence",
                        node_id=node_id,
                    ),
                ])
            commands.append(runbook_command(
                "view",
                "python scripts/syncmate/syncmate.py dashboard",
                "refresh the local static dashboard after sync evidence changes",
            ))
        else:
            commands.append(runbook_command(
                "setup",
                "python scripts/syncmate/syncmate.py setup-plan --role collector --peer-id <runner_id> --peer-ssh <ssh_alias> --peer-repo-path <remote_repo>",
                "prepare the add-peer and sync commands for a collector checkout",
            ))
            manual_actions.append({
                "kind": "peer",
                "reason": "collector has no configured peers",
                "action": "add at least one runner peer with add-peer before running sync",
            })

    if role in ("runner", "runner+collector"):
        commands.extend([
            runbook_command(
                "publish",
                "python scripts/syncmate/syncmate.py publish --write",
                "write a copyable runner status and manifest package",
            ),
            runbook_command(
                "bundle",
                "python scripts/syncmate/syncmate.py bundle",
                "create an offline status plus artifact bundle when SSH is unavailable",
            ),
            runbook_command(
                "manifest",
                "python scripts/syncmate/syncmate.py manifest --json",
                "emit the runner artifact manifest and SHA-256 values",
            ),
        ])

    commands.append(runbook_command(
        "handoff",
        "python scripts/syncmate/syncmate.py handoff-pack",
        "write an evidence-only zip for another AI or machine",
    ))
    commands.append(runbook_command(
        "inspect-handoff",
        "python scripts/syncmate/syncmate.py inspect-handoff-pack <handoff_pack.zip> --write",
        "audit a copied evidence-only handoff zip without extracting files",
    ))
    commands.append(runbook_command(
        "rehearse",
        "python scripts/syncmate/syncmate.py smoke",
        "run a local end-to-end rehearsal without touching this checkout's .syncmate state",
    ))

    peer_guides: Dict[str, Any] = {}
    for node_id in selected:
        peer = peer_configs.get(node_id) or {}
        landing_peer = (landings.get("peers") or {}).get(node_id) or {}
        artifact_names = artifact_names_for_peer({"artifact_policy": device.get("artifact_policy")}, peer)
        peer_guides[node_id] = {
            "node_id": node_id,
            "role": peer.get("role", "runner"),
            "transport": peer_transport(peer),
            "ssh": peer.get("ssh"),
            "repo_path": peer.get("repo_path"),
            "result_roots": peer.get("result_roots") or ["results/runs"],
            "landing": peer.get("landing") or landing_peer.get("landing") or f"results/runs/{node_id}",
            "landing_state": landing_peer.get("state"),
            "landing_exists": (landing_peer.get("landing_path") or {}).get("exists"),
            "result_rows": ((landing_peer.get("results") or {}).get("rows") or 0),
            "artifact_policy": artifact_policy_payload(artifact_names),
            "commands": {
                "remote_status": f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply",
                "diff": f"python scripts/syncmate/syncmate.py collect {node_id} --diff",
                "sync": f"python scripts/syncmate/syncmate.py sync {node_id}",
                "landings": f"python scripts/syncmate/syncmate.py landings {node_id}",
                "checklist": f"python scripts/syncmate/syncmate.py checklist {node_id} --write",
                "handoff": f"python scripts/syncmate/syncmate.py handoff {node_id} --write",
            },
        }

    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    results_summary = results_table.get("summary") or {}
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "runbook",
        "runbook_path": rel(runbook_file()),
        "device": {
            "id": device.get("id"),
            "role": role,
            "repo_path": device.get("repo_path"),
            "setup_file": device.get("setup_file"),
            "setup_ready": not warnings and role != "unknown",
            "setup_warnings": warnings,
        },
        "status": status_label(snapshot, diagnostics),
        "landing_rule": "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/",
        "summary": {
            "configured_peers": len(peer_configs),
            "selected_peers": len(selected),
            "indexed_artifacts": artifact_index_total(snapshot.get("artifact_index") or {}),
            "result_rows": results_summary.get("rows", 0),
            "diagnostics": len(diagnostics),
        },
        "commands": commands,
        "manual_actions": manual_actions,
        "peers": peer_guides,
        "files": {
            "runbook": rel(runbook_file()),
            "device_setup": rel(DEFAULT_DEVICE_FILE),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "checklist": rel(checklist_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "acceptance": rel(acceptance_file()),
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
        },
    }


def render_runbook_markdown(data: Dict[str, Any]) -> str:
    device = data.get("device") or {}
    summary = data.get("summary") or {}
    files = data.get("files") or {}
    lines = [
        "# Syncmate Runbook",
        "",
        f"Generated: {data.get('generated_at')}",
        f"Device: {device.get('id')} ({device.get('role')})",
        f"Setup ready: {device.get('setup_ready')}",
        f"Status: {data.get('status')}",
        "",
        "## Result Landing Contract",
        "",
        f"- Rule: `{data.get('landing_rule')}`",
        f"- Trusted results table: `{files.get('results_csv')}`",
        f"- Artifact index: `{files.get('artifact_index')}`",
        "",
        "## Current Counts",
        "",
        f"- Configured peers: {summary.get('configured_peers', 0)}",
        f"- Indexed artifacts: {summary.get('indexed_artifacts', 0)}",
        f"- Result rows: {summary.get('result_rows', 0)}",
        f"- Diagnostics: {summary.get('diagnostics', 0)}",
        "",
        "## Setup Warnings",
        "",
    ]
    warnings = device.get("setup_warnings") or []
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- none")

    lines.extend(["", "## Commands", ""])
    for idx, item in enumerate(data.get("commands") or [], start=1):
        node = f" [{item.get('node_id')}]" if item.get("node_id") else ""
        lines.append(f"{idx}. `{item.get('command')}`")
        lines.append(f"   {item.get('kind')}{node}: {item.get('reason')}")

    lines.extend(["", "## Manual Actions", ""])
    manual = data.get("manual_actions") or []
    if manual:
        for item in manual:
            lines.append(f"- {item.get('kind')}: {item.get('reason')} :: {item.get('action')}")
    else:
        lines.append("- none")

    lines.extend(["", "## Peers", ""])
    peers = data.get("peers") or {}
    if not peers:
        lines.append("- No configured peers yet.")
    for node_id, peer in peers.items():
        policy = peer.get("artifact_policy") or {}
        lines.extend([
            f"- {node_id}: transport={peer.get('transport')} landing={peer.get('landing')} "
            f"state={peer.get('landing_state')} rows={peer.get('result_rows', 0)}",
            f"  repo: `{peer.get('repo_path')}`",
            f"  artifacts: {', '.join(policy.get('include') or []) or 'default'}",
        ])
        for label, command in (peer.get("commands") or {}).items():
            lines.append(f"  {label}: `{command}`")

    lines.extend([
        "",
        "## Evidence Files",
        "",
        f"- Runbook: {files.get('runbook')}",
        f"- Device setup: {files.get('device_setup')}",
        f"- Dashboard: {files.get('dashboard')}",
        f"- Brief: {files.get('brief')}",
        f"- Checklist: {files.get('checklist')}",
        f"- Workflow: {files.get('workflow')}",
        f"- Automation core: {files.get('automation_core')}",
        f"- Acceptance: {files.get('acceptance')}",
        f"- Results: {files.get('results_json')} / {files.get('results_csv')}",
    ])
    return "\n".join(lines) + "\n"


def write_runbook(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = runbook_file()
    data = {**data, "runbook_path": rel(out)}
    out.write_text(render_runbook_markdown(data), encoding="utf-8")
    return out


def cmd_runbook(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    data = runbook_payload(
        snapshot,
        diagnostics,
        node_ids=args.node_ids or None,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_runbook(data)
        data["runbook_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0
    if args.write:
        print(f"syncmate runbook: {rel(out_path)}")
        print(f"  setup_ready={((data.get('device') or {}).get('setup_ready'))} status={data.get('status')}")
        print(f"  peers={((data.get('summary') or {}).get('configured_peers', 0))}")
    else:
        print(render_runbook_markdown(data), end="")
    return 0


def next_command_contract(kind: str, *, node_id: Optional[str] = None,
                          command: Optional[str] = None) -> Dict[str, Any]:
    peer = safe_file_stem(node_id) if node_id else None
    evidence: Dict[str, List[str]] = {"reads": [], "writes": [], "inspects": []}
    effects: List[str] = []

    def read(path: str) -> None:
        if path not in evidence["reads"]:
            evidence["reads"].append(path)

    def write(path: str) -> None:
        if path not in evidence["writes"]:
            evidence["writes"].append(path)

    def inspect(path: str) -> None:
        if path not in evidence["inspects"]:
            evidence["inspects"].append(path)

    def effect(value: str) -> None:
        if value not in effects:
            effects.append(value)

    if kind == "preflight":
        read(rel(DEFAULT_DEVICE_FILE))
        write(rel(last_preflight_file()))
        effect("writes-sync-evidence")
    elif kind == "remote-status" and peer:
        read(rel(DEFAULT_DEVICE_FILE))
        write(f".syncmate/remote_status_{peer}.json")
        effect("contacts-peer")
        effect("writes-sync-evidence")
    elif kind == "diff" and peer:
        read(f".syncmate/remote_status_{peer}.json")
        write(f".syncmate/last_diff_{peer}.json")
        effect("contacts-peer")
        effect("reads-remote-manifest")
        effect("writes-sync-evidence")
    elif kind == "bundle-diff" and peer:
        inspect("copied bundle zip")
        write(f".syncmate/remote_status_{peer}.json")
        write(f".syncmate/last_diff_{peer}.json")
        effect("offline")
        effect("no-extract")
        effect("writes-sync-evidence")
    elif kind == "import-bundle" and peer:
        inspect("copied bundle zip")
        write(f"results/runs/{peer}/")
        write(f".syncmate/last_collect_{peer}.json")
        write(f".syncmate/last_verify_{peer}.json")
        write(rel(artifact_index_file()))
        write(rel(results_table_file()))
        write(rel(results_csv_file()))
        effect("offline")
        effect("extracts-selected-artifacts")
        effect("verifies-checksums")
        effect("updates-trusted-index")
        effect("extracts-trusted-results")
    elif kind == "collect" and peer:
        read(f".syncmate/last_diff_{peer}.json")
        write(f"results/runs/{peer}/")
        write(f".syncmate/last_collect_{peer}.json")
        write(f".syncmate/last_verify_{peer}.json")
        write(rel(artifact_index_file()))
        effect("contacts-peer")
        effect("copies-selected-artifacts")
        effect("verifies-checksums")
        effect("updates-trusted-index")
    elif kind == "verify" and peer:
        read(f"results/runs/{peer}/")
        write(f".syncmate/last_verify_{peer}.json")
        write(rel(artifact_index_file()))
        effect("contacts-peer")
        effect("verifies-checksums")
        effect("updates-trusted-index")
    elif kind == "results":
        read(rel(artifact_index_file()))
        write(rel(results_table_file()))
        write(rel(results_csv_file()))
        effect("checks-trusted-index")
        effect("extracts-trusted-results")
    elif kind == "gate":
        read(rel(last_preflight_file()))
        read(rel(artifact_index_file()))
        read(rel(results_table_file()))
        read(rel(results_csv_file()))
        effect("read-only-gate")
    elif kind == "summary":
        read(rel(artifact_index_file()))
        read(rel(results_table_file()))
        effect("read-only-summary")
    elif kind == "maintenance":
        read(rel(artifact_index_file()))
        inspect(".syncmate/orphaned reports")
        effect("dry-run-by-default")

    if command and "archive-orphans" in command and "--apply" in command:
        write(".syncmate/archive/")
        write(rel(artifact_index_file()))
    return {
        "evidence": {key: value for key, value in evidence.items() if value},
        "effects": effects,
    }


def add_next_command(commands: List[Dict[str, Any]], command: str, reason: str,
                     *, node_id: Optional[str] = None, kind: str = "sync") -> None:
    if any(item.get("command") == command for item in commands):
        return
    item: Dict[str, Any] = {
        "command": command,
        "kind": kind,
        "reason": reason,
    }
    if node_id:
        item["node_id"] = node_id
    item.update(next_command_contract(kind, node_id=node_id, command=command))
    commands.append(item)


def next_steps_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                       require_verify: bool = False,
                       require_preflight: bool = False,
                       require_results: bool = False,
                       limit: int = 12) -> Dict[str, Any]:
    commands: List[Dict[str, Any]] = []
    manual_actions: List[Dict[str, Any]] = []
    device = snapshot.get("device") or {}
    peer_configs = device.get("peer_configs") or {}
    remote_status = snapshot.get("remote_status") or {}
    diff_reports = snapshot.get("diff_reports") or {}
    collect_reports = snapshot.get("collect_reports") or {}
    verify_reports = snapshot.get("verify_reports") or {}
    artifact_index = snapshot.get("artifact_index") or {}
    indexed_peers = artifact_index.get("peers") or {}

    setup_needed = bool(device.get("setup_warnings") or device.get("role") == "unknown")
    if setup_needed:
        manual_actions.append({
            "kind": "setup",
            "reason": "device setup is missing or role is unknown",
            "action": "Run python scripts/syncmate/syncmate.py setup-plan, then run the matching init-device command.",
        })

    peers = configured_peers(snapshot)
    preflight_diagnostics = preflight_gate_diagnostics(snapshot) if require_preflight else []
    preflight_error_codes = {
        item.get("code")
        for item in preflight_diagnostics
        if item.get("severity") == "error"
    }
    if require_preflight and not setup_needed and preflight_error_codes:
        add_next_command(
            commands,
            "python scripts/syncmate/syncmate.py preflight --write",
            "write a fresh setup-readiness report before remote sync or strict gate",
            kind="preflight",
        )

    bundle_diff_peers = {
        str(node_id)
        for node_id, report in (diff_reports or {}).items()
        if is_bundle_diff_report(report)
    }
    peers = sorted(set(configured_peers(snapshot)) | bundle_diff_peers)

    for peer in peers:
        peer_config = peer_configs.get(peer) or {}
        diff = diff_reports.get(peer)
        has_bundle_diff = is_bundle_diff_report(diff or {})
        if (not has_bundle_diff
                and ((not peer_uses_local_transport(peer_config) and not peer_config.get("ssh"))
                     or not peer_config.get("repo_path"))):
            manual_actions.append({
                "kind": "peer-config",
                "node_id": peer,
                "reason": "peer is missing ssh or repo_path",
                "action": f"Fix .syncmate/device.yaml for {peer}, then rerun summary.",
            })
            continue

        remote = remote_status.get(peer)
        if (not has_bundle_diff
                and (not remote or remote.get("errors") or is_report_stale(remote.get("generated_at")))):
            add_next_command(
                commands,
                f"python scripts/syncmate/syncmate.py remote-status {peer} --apply",
                "refresh peer status before deciding what to collect",
                node_id=peer,
                kind="remote-status",
            )
            continue

        if not diff or diff.get("errors") or is_report_stale(diff.get("generated_at")):
            if has_bundle_diff:
                add_next_command(
                    commands,
                    import_bundle_command(diff or {}, peer, dry_run=True, write_plan=True),
                    "refresh saved offline bundle delta before import",
                    node_id=peer,
                    kind="bundle-diff",
                )
            else:
                add_next_command(
                    commands,
                    f"python scripts/syncmate/syncmate.py collect {peer} --diff",
                    "compare remote manifest with local landing",
                    node_id=peer,
                    kind="diff",
                )
            continue

        diff_summary = diff.get("summary") or {}
        missing = diff_summary.get("missing", len(diff.get("missing") or []))
        conflicts = diff_summary.get("conflicts", len(diff.get("conflicts") or []))
        verify = verify_reports.get(peer)
        verify_summary = (verify or {}).get("summary") or {}
        verify_missing = verify_summary.get("missing", len((verify or {}).get("missing") or []))
        verify_conflicts = verify_summary.get("conflicts", len((verify or {}).get("conflicts") or []))
        needs_verify = (
            not verify
            or (verify.get("errors") if verify else False)
            or is_report_stale((verify or {}).get("generated_at"))
            or verify_summary.get("status") != "verified"
            or bool(verify_missing or verify_conflicts)
            or peer not in indexed_peers
        )
        if has_bundle_diff:
            if missing or (needs_verify and not conflicts):
                add_next_command(
                    commands,
                    import_bundle_command(diff, peer),
                    "extract, checksum, and index artifacts from the copied bundle",
                    node_id=peer,
                    kind="import-bundle",
                )
            if conflicts:
                manual_actions.append({
                    "kind": "conflict",
                    "node_id": peer,
                    "reason": f"bundle diff reports {conflicts} checksum conflict(s)",
                    "action": f"Inspect .syncmate/last_diff_{peer}.json before using {import_bundle_command(diff, peer, overwrite=True)}.",
                })
            continue

        if missing:
            add_next_command(
                commands,
                f"python scripts/syncmate/syncmate.py collect {peer} --apply",
                f"fetch and checksum {missing} missing selected artifact(s)",
                node_id=peer,
                kind="collect",
            )
        if conflicts:
            manual_actions.append({
                "kind": "conflict",
                "node_id": peer,
                "reason": f"diff reports {conflicts} checksum conflict(s)",
                "action": f"Inspect .syncmate/last_diff_{peer}.json before using collect {peer} --apply --overwrite.",
            })
            continue

        collect = collect_reports.get(peer)
        if collect:
            failed = len(collect.get("verification_failed") or [])
            errors = collect.get("errors") or []
            if failed or errors:
                add_next_command(
                    commands,
                    f"python scripts/syncmate/syncmate.py collect {peer} --apply",
                    "retry collection after previous transfer/checksum errors",
                    node_id=peer,
                    kind="collect",
                )

        if needs_verify:
            add_next_command(
                commands,
                f"python scripts/syncmate/syncmate.py verify {peer} --apply",
                "refresh acceptance report and trusted artifact index",
                node_id=peer,
                kind="verify",
            )

    if orphaned_sync_entries(snapshot):
        add_next_command(
            commands,
            "python scripts/syncmate/syncmate.py archive-orphans",
            "preview archiving obsolete local sync reports/index entries",
            kind="maintenance",
        )

    results_diagnostics: List[Dict[str, Any]] = []
    if require_results:
        results_diagnostics, _results_check = results_gate_diagnostics(snapshot)
        if results_diagnostics:
            add_next_command(
                commands,
                "python scripts/syncmate/syncmate.py results --write --check",
                "refresh trusted metric table from the verified artifact index",
                kind="results",
            )

    gate_flags = []
    if require_preflight:
        gate_flags.append("--require-preflight")
    if require_verify:
        gate_flags.append("--require-verify")
    if require_results:
        gate_flags.append("--require-results")

    if require_verify:
        gate_command = " ".join(["python scripts/syncmate/syncmate.py gate", *gate_flags])
        gate_reason = "confirm all configured peers pass verification, artifact-index integrity, and required result extraction"
        add_next_command(
            commands,
            gate_command,
            gate_reason,
            kind="gate",
        )
    else:
        summary_flags = []
        if require_preflight:
            summary_flags.append("--require-preflight")
        if require_results:
            summary_flags.append("--require-results")
        summary_command = " ".join(["python scripts/syncmate/syncmate.py summary", *summary_flags])
        summary_reason = "review compact sync status after completing the queued step(s)"
        if require_preflight or require_results:
            summary_reason = "review compact sync status with the requested saved gate checks"
        add_next_command(
            commands,
            summary_command,
            summary_reason,
            kind="summary",
        )

    ranked = sorted(
        [*diagnostics, *preflight_diagnostics, *results_diagnostics],
        key=lambda item: severity_rank(item.get("severity", "")),
        reverse=True,
    )
    for item in ranked:
        action = item.get("action")
        if not action:
            continue
        if setup_needed and item.get("code") in ("setup-warning", "unknown-role"):
            continue
        if action.startswith("Run python scripts/syncmate/syncmate.py"):
            continue
        if action.startswith("Run collect ") or action.startswith("Rerun python scripts/syncmate/syncmate.py"):
            continue
        manual_item = {
            "kind": "diagnostic",
            "reason": f"{item.get('severity')}:{item.get('code')}",
            "action": action,
        }
        if item.get("node"):
            manual_item["node_id"] = item.get("node")
        manual_actions.append(manual_item)

    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "next",
        "device_id": device.get("id"),
        "commands": commands[:max(0, limit)],
        "manual_actions": manual_actions[:max(0, limit)],
        "truncated": len(commands) > max(0, limit) or len(manual_actions) > max(0, limit),
        "require_verify": require_verify,
        "require_preflight": require_preflight,
        "require_results": require_results,
    }


def render_action_plan_markdown(data: Dict[str, Any]) -> str:
    lines = [
        "# Syncmate Action Plan",
        "",
        f"- Generated: `{data.get('generated_at')}`",
        f"- Device: `{data.get('device_id')}`",
        f"- Requires preflight: `{data.get('require_preflight')}`",
        f"- Requires verify: `{data.get('require_verify')}`",
        f"- Requires results: `{data.get('require_results')}`",
        "",
        "## Commands",
        "",
    ]
    commands = data.get("commands") or []
    if not commands:
        lines.append("- No executable commands suggested.")
    for idx, item in enumerate(commands, start=1):
        node = f" [{item.get('node_id')}]" if item.get("node_id") else ""
        lines.extend([
            f"{idx}. `{item.get('command')}`",
            f"   - Kind: `{item.get('kind')}`{node}",
            f"   - Reason: {item.get('reason')}",
        ])
        evidence = item.get("evidence") or {}
        for key in ("reads", "writes", "inspects"):
            values = evidence.get(key) or []
            if values:
                lines.append(f"   - {key.title()}: " + ", ".join(f"`{value}`" for value in values))
        effects = item.get("effects") or []
        if effects:
            lines.append("   - Effects: " + ", ".join(f"`{value}`" for value in effects))
    lines.extend(["", "## Manual Actions", ""])
    manual_actions = data.get("manual_actions") or []
    if not manual_actions:
        lines.append("- No manual actions suggested.")
    for idx, item in enumerate(manual_actions, start=1):
        node = f" [{item.get('node_id')}]" if item.get("node_id") else ""
        lines.extend([
            f"{idx}. {item.get('action')}",
            f"   - Kind: `{item.get('kind')}`{node}",
            f"   - Reason: {item.get('reason')}",
        ])
    if data.get("truncated"):
        lines.extend(["", "> Output was truncated. Re-run `next --write --limit <N>` with a larger limit."])
    lines.append("")
    return "\n".join(lines)


def write_action_plan(data: Dict[str, Any]) -> Dict[str, str]:
    ensure_sync_dir()
    json_path = action_plan_file()
    markdown_path = action_plan_markdown_file()
    data["action_plan_path"] = rel(json_path)
    data["action_plan_markdown_path"] = rel(markdown_path)
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_action_plan_markdown(data), encoding="utf-8")
    return {
        "json": rel(json_path),
        "markdown": rel(markdown_path),
    }


WORKFLOW_STATUS_RANK = {
    "not-required": 0,
    "ok": 1,
    "waiting": 2,
    "action-needed": 3,
    "blocked": 4,
}


def workflow_stage(stage_id: str, status: str, reason: str, *, node_id: Optional[str] = None,
                   command: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "id": stage_id,
        "status": status,
        "reason": reason,
    }
    if node_id:
        item["node_id"] = node_id
    if command:
        item["command"] = command
    if details:
        item["details"] = details
    return item


def workflow_worst_status(stages: List[Dict[str, Any]]) -> str:
    active = [stage.get("status", "ok") for stage in stages if stage.get("status") != "not-required"]
    if not active:
        return "ok"
    return max(active, key=lambda status: WORKFLOW_STATUS_RANK.get(status, 0))


def workflow_preflight_stage(snapshot: Dict[str, Any], *, require_preflight: bool) -> Dict[str, Any]:
    if not require_preflight:
        return workflow_stage(
            "preflight",
            "not-required",
            "Saved preflight is not required by this workflow view.",
            command="python scripts/syncmate/syncmate.py preflight --write",
        )
    diagnostics = preflight_gate_diagnostics(snapshot)
    if not diagnostics:
        preflight = snapshot.get("preflight") if isinstance(snapshot.get("preflight"), dict) else {}
        return workflow_stage(
            "preflight",
            "ok",
            "Saved preflight report is fresh and covers configured peers.",
            details={"report_path": preflight.get("report_path") or rel(last_preflight_file())},
        )
    codes = {item.get("code") for item in diagnostics}
    status = "action-needed"
    if "gate-preflight-blocked" in codes or "gate-preflight-status" in codes:
        status = "blocked"
    return workflow_stage(
        "preflight",
        status,
        diagnostics[0].get("message") or "Saved preflight report needs attention.",
        command="python scripts/syncmate/syncmate.py preflight --write",
        details={"diagnostics": diagnostics},
    )


def workflow_peer_payload(snapshot: Dict[str, Any], node_id: str) -> Dict[str, Any]:
    device = snapshot.get("device") or {}
    peer_configs = device.get("peer_configs") or {}
    peer_config = peer_configs.get(node_id) or {}
    remote_status = (snapshot.get("remote_status") or {}).get(node_id) or {}
    diff_report = (snapshot.get("diff_reports") or {}).get(node_id) or {}
    collect_report = (snapshot.get("collect_reports") or {}).get(node_id) or {}
    verify_report = (snapshot.get("verify_reports") or {}).get(node_id) or {}
    index_entry = ((snapshot.get("artifact_index") or {}).get("peers") or {}).get(node_id) or {}

    stages: List[Dict[str, Any]] = []
    configured = node_id in configured_peers(snapshot)
    has_bundle_diff = is_bundle_diff_report(diff_report) if diff_report else False
    missing_setup = []
    if not configured:
        missing_setup.append("peer is not configured")
    if not peer_config.get("repo_path") and not has_bundle_diff:
        missing_setup.append("repo_path is missing")
    if not has_bundle_diff and not peer_uses_local_transport(peer_config) and not peer_config.get("ssh"):
        missing_setup.append("ssh is missing")
    if missing_setup:
        stages.append(workflow_stage(
            "setup",
            "blocked",
            "; ".join(missing_setup),
            node_id=node_id,
            command=f"python scripts/syncmate/syncmate.py add-peer {node_id} --help",
        ))
    else:
        stages.append(workflow_stage(
            "setup",
            "ok",
            "Peer setup has the fields needed for the saved sync path.",
            node_id=node_id,
            details={
                "transport": peer_transport(peer_config),
                "landing": peer_config.get("landing"),
                "repo_path": peer_config.get("repo_path"),
            },
        ))

    setup_ready = stages[-1]["status"] == "ok"
    if has_bundle_diff:
        stages.append(workflow_stage(
            "remote-status",
            "ok",
            "Offline bundle diff plan is saved; live remote status is not required for import.",
            node_id=node_id,
            details={"source": "bundle", "bundle_path": report_bundle_path(diff_report, node_id)},
        ))
        remote_ready = True
    elif not setup_ready:
        stages.append(workflow_stage(
            "remote-status",
            "waiting",
            "Peer setup must be fixed before remote status can be refreshed.",
            node_id=node_id,
        ))
        remote_ready = False
    elif not remote_status:
        stages.append(workflow_stage(
            "remote-status",
            "action-needed",
            "No saved remote status report exists.",
            node_id=node_id,
            command=f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply",
        ))
        remote_ready = False
    elif remote_status.get("errors"):
        stages.append(workflow_stage(
            "remote-status",
            "action-needed",
            "Saved remote status report has error(s).",
            node_id=node_id,
            command=f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply",
            details={"errors": remote_status.get("errors") or []},
        ))
        remote_ready = False
    elif is_report_stale(remote_status.get("generated_at")):
        stages.append(workflow_stage(
            "remote-status",
            "action-needed",
            "Saved remote status report is stale.",
            node_id=node_id,
            command=f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply",
            details={"generated_at": remote_status.get("generated_at"), "age": format_age(remote_status.get("generated_at"))},
        ))
        remote_ready = False
    else:
        remote_summary = remote_status.get("summary") or {}
        stages.append(workflow_stage(
            "remote-status",
            "ok",
            "Saved remote status report is fresh.",
            node_id=node_id,
            details={
                "generated_at": remote_status.get("generated_at"),
                "age": format_age(remote_status.get("generated_at")),
                "leaves": remote_summary.get("result_leaves"),
                "git": remote_summary.get("git_short_sha"),
            },
        ))
        remote_ready = True

    diff_command = (
        import_bundle_command(diff_report, node_id, dry_run=True, write_plan=True)
        if has_bundle_diff else
        f"python scripts/syncmate/syncmate.py collect {node_id} --diff"
    )
    if not remote_ready:
        stages.append(workflow_stage(
            "diff",
            "waiting",
            "Remote status or offline bundle evidence is needed before diff can be trusted.",
            node_id=node_id,
        ))
        diff_ready = False
    elif not diff_report:
        stages.append(workflow_stage(
            "diff",
            "action-needed",
            "No saved manifest diff exists.",
            node_id=node_id,
            command=diff_command,
        ))
        diff_ready = False
    elif diff_report.get("errors") or is_report_stale(diff_report.get("generated_at")):
        stages.append(workflow_stage(
            "diff",
            "action-needed",
            "Saved manifest diff has error(s) or is stale.",
            node_id=node_id,
            command=diff_command,
            details={"errors": diff_report.get("errors") or [], "age": format_age(diff_report.get("generated_at"))},
        ))
        diff_ready = False
    else:
        diff_summary = diff_report.get("summary") or {}
        stages.append(workflow_stage(
            "diff",
            "ok",
            "Saved manifest diff is fresh.",
            node_id=node_id,
            details={
                "missing": count_int(diff_summary.get("missing", len(diff_report.get("missing") or []))),
                "conflicts": count_int(diff_summary.get("conflicts", len(diff_report.get("conflicts") or []))),
                "remote_incomplete": count_int(diff_summary.get("remote_incomplete")),
                "source": report_remote_source(diff_report) or "remote",
            },
        ))
        diff_ready = True

    diff_summary = diff_report.get("summary") or {}
    missing = count_int(diff_summary.get("missing", len(diff_report.get("missing") or [])))
    conflicts = count_int(diff_summary.get("conflicts", len(diff_report.get("conflicts") or [])))
    collect_command = import_bundle_command(diff_report, node_id) if has_bundle_diff else f"python scripts/syncmate/syncmate.py collect {node_id} --apply"
    overwrite_command = (
        import_bundle_command(diff_report, node_id, overwrite=True)
        if has_bundle_diff else
        f"python scripts/syncmate/syncmate.py collect {node_id} --apply --overwrite"
    )
    if not diff_ready:
        stages.append(workflow_stage(
            "collect",
            "waiting",
            "A fresh diff is needed before incremental collection/import.",
            node_id=node_id,
        ))
        collect_ready = False
    elif conflicts:
        stages.append(workflow_stage(
            "collect",
            "blocked",
            f"Diff reports {conflicts} checksum conflict(s).",
            node_id=node_id,
            command=overwrite_command,
            details={"conflicts": conflicts},
        ))
        collect_ready = False
    elif missing:
        stages.append(workflow_stage(
            "collect",
            "action-needed",
            f"{missing} selected artifact(s) are missing locally.",
            node_id=node_id,
            command=collect_command,
            details={"missing": missing},
        ))
        collect_ready = False
    elif collect_report.get("errors") or collect_report.get("verification_failed"):
        stages.append(workflow_stage(
            "collect",
            "action-needed",
            "Previous collection/import report has transfer or checksum failures.",
            node_id=node_id,
            command=collect_command,
            details={
                "errors": collect_report.get("errors") or [],
                "failed": len(collect_report.get("verification_failed") or []),
            },
        ))
        collect_ready = False
    else:
        collect_summary = collect_report.get("summary") or {}
        stages.append(workflow_stage(
            "collect",
            "ok",
            "No missing selected artifacts remain in the latest diff.",
            node_id=node_id,
            details={
                "fetched": collect_summary.get("missing_fetched"),
                "verified": collect_summary.get("verified"),
            },
        ))
        collect_ready = True

    verify_command = f"python scripts/syncmate/syncmate.py verify {node_id} --apply"
    if not collect_ready:
        stages.append(workflow_stage(
            "verify",
            "waiting",
            "Collection/import must be complete before checksum acceptance can be refreshed.",
            node_id=node_id,
        ))
        verify_ready = False
    elif not verify_report:
        stages.append(workflow_stage(
            "verify",
            "action-needed",
            "No saved checksum verification report exists.",
            node_id=node_id,
            command=verify_command,
        ))
        verify_ready = False
    elif verify_report.get("errors") or is_report_stale(verify_report.get("generated_at")):
        stages.append(workflow_stage(
            "verify",
            "action-needed",
            "Saved checksum verification report has error(s) or is stale.",
            node_id=node_id,
            command=verify_command,
            details={"errors": verify_report.get("errors") or [], "age": format_age(verify_report.get("generated_at"))},
        ))
        verify_ready = False
    else:
        verify_summary = verify_report.get("summary") or {}
        verify_missing = count_int(verify_summary.get("missing", len(verify_report.get("missing") or [])))
        verify_conflicts = count_int(verify_summary.get("conflicts", len(verify_report.get("conflicts") or [])))
        remote_incomplete = count_int(verify_summary.get("remote_incomplete"))
        verify_status = verify_summary.get("status")
        if verify_conflicts:
            stages.append(workflow_stage(
                "verify",
                "blocked",
                f"Verification reports {verify_conflicts} checksum conflict(s).",
                node_id=node_id,
                command=overwrite_command,
                details={"conflicts": verify_conflicts},
            ))
            verify_ready = False
        elif verify_missing:
            stages.append(workflow_stage(
                "verify",
                "action-needed",
                f"Verification reports {verify_missing} missing artifact(s).",
                node_id=node_id,
                command=collect_command,
                details={"missing": verify_missing},
            ))
            verify_ready = False
        elif remote_incomplete:
            stages.append(workflow_stage(
                "verify",
                "blocked",
                f"Remote manifest has {remote_incomplete} incomplete experiment leaf/leaves.",
                node_id=node_id,
                details={"remote_incomplete": remote_incomplete},
            ))
            verify_ready = False
        elif verify_status != "verified":
            stages.append(workflow_stage(
                "verify",
                "action-needed",
                f"Verification status is {verify_status!r}, not 'verified'.",
                node_id=node_id,
                command=verify_command,
            ))
            verify_ready = False
        else:
            stages.append(workflow_stage(
                "verify",
                "ok",
                "Latest checksum verification report is accepted.",
                node_id=node_id,
                details={
                    "verified_current": verify_summary.get("verified_current", verify_summary.get("already_current")),
                    "generated_at": verify_report.get("generated_at"),
                    "age": format_age(verify_report.get("generated_at")),
                },
            ))
            verify_ready = True

    if not verify_ready:
        stages.append(workflow_stage(
            "index",
            "waiting",
            "A clean verification report is needed before the trusted artifact index is accepted.",
            node_id=node_id,
        ))
    elif not index_entry:
        stages.append(workflow_stage(
            "index",
            "action-needed",
            "No trusted artifact index entry exists for this peer.",
            node_id=node_id,
            command=verify_command,
        ))
    else:
        index_summary = index_entry.get("summary") or {}
        indexed = count_int(index_summary.get("indexed", len(index_entry.get("items") or [])))
        index_missing = count_int(index_summary.get("missing"))
        index_conflicts = count_int(index_summary.get("conflicts"))
        index_incomplete = count_int(index_summary.get("remote_incomplete"))
        index_status = index_summary.get("status")
        if index_status == "verified" and indexed and not index_missing and not index_conflicts and not index_incomplete:
            stages.append(workflow_stage(
                "index",
                "ok",
                "Trusted artifact index is present for this peer.",
                node_id=node_id,
                details={"indexed": indexed, "updated_at": index_entry.get("updated_at"), "age": format_age(index_entry.get("updated_at"))},
            ))
        elif index_missing or index_conflicts or index_incomplete:
            stages.append(workflow_stage(
                "index",
                "blocked",
                "Trusted artifact index is incomplete or conflicted.",
                node_id=node_id,
                command=verify_command,
                details={"indexed": indexed, "missing": index_missing, "conflicts": index_conflicts, "remote_incomplete": index_incomplete},
            ))
        else:
            stages.append(workflow_stage(
                "index",
                "action-needed",
                f"Trusted artifact index status is {index_status!r}.",
                node_id=node_id,
                command=verify_command,
                details={"indexed": indexed},
            ))

    return {
        "node_id": node_id,
        "status": workflow_worst_status(stages),
        "stages": stages,
    }


def workflow_results_stage(snapshot: Dict[str, Any], *, require_results: bool) -> Dict[str, Any]:
    if not require_results:
        return workflow_stage(
            "results",
            "not-required",
            "Trusted metric table freshness is not required by this workflow view.",
            command="python scripts/syncmate/syncmate.py results --write --check",
        )
    diagnostics, check = results_gate_diagnostics(snapshot)
    if not diagnostics:
        return workflow_stage(
            "results",
            "ok",
            "Saved trusted results table matches the current artifact index.",
            command="python scripts/syncmate/syncmate.py results --write --check",
            details=check,
        )
    codes = {item.get("code") for item in diagnostics}
    if "gate-results-no-indexed-artifacts" in codes:
        status = "waiting"
        reason = "Trusted artifacts must be indexed before metric extraction can be required."
        command = None
    elif codes <= {"gate-results-missing", "gate-results-stale"}:
        status = "action-needed"
        reason = diagnostics[0].get("message") or "Saved trusted results table is missing or stale."
        command = "python scripts/syncmate/syncmate.py results --write --check"
    else:
        status = "blocked"
        reason = diagnostics[0].get("message") or "Trusted results extraction needs attention."
        command = "python scripts/syncmate/syncmate.py results --write --check"
    return workflow_stage(
        "results",
        status,
        reason,
        command=command,
        details={"check": check, "diagnostics": diagnostics},
    )


def workflow_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                     node_ids: Optional[List[str]] = None, fail_on: str = "warn",
                     require_preflight: bool = False, require_verify: bool = True,
                     require_results: bool = True, limit: int = 12) -> Dict[str, Any]:
    selected = [str(node) for node in (node_ids or configured_peers(snapshot) or known_report_nodes(snapshot))]
    peers = {node_id: workflow_peer_payload(snapshot, node_id) for node_id in selected}
    global_stages = [
        workflow_preflight_stage(snapshot, require_preflight=require_preflight),
        workflow_results_stage(snapshot, require_results=require_results),
    ]
    gate = gate_payload(
        snapshot,
        diagnostics,
        fail_on=fail_on,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
    )
    gate_flags = []
    if require_preflight:
        gate_flags.append("--require-preflight")
    if require_verify:
        gate_flags.append("--require-verify")
    if require_results:
        gate_flags.append("--require-results")
    gate_command = " ".join(["python scripts/syncmate/syncmate.py gate", *gate_flags])
    global_stages.append(workflow_stage(
        "gate",
        "ok" if gate.get("passed") else "blocked",
        "Final automation gate passes." if gate.get("passed") else "Final automation gate still has blocking diagnostics.",
        command=gate_command,
        details={"failure_count": gate.get("failure_count", 0), "fail_on": gate.get("fail_on")},
    ))
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_verify=require_verify,
        require_preflight=require_preflight,
        require_results=require_results,
        limit=limit,
    )
    all_stages = [*global_stages]
    for peer in peers.values():
        all_stages.extend(peer.get("stages") or [])
    stage_counts = Counter(stage.get("status") for stage in all_stages)
    peer_counts = Counter(peer.get("status") for peer in peers.values())
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "workflow",
        "device_id": (snapshot.get("device") or {}).get("id"),
        "status": workflow_worst_status(all_stages),
        "policy": {
            "fail_on": fail_on,
            "require_preflight": require_preflight,
            "require_verify": require_verify,
            "require_results": require_results,
        },
        "summary": {
            "peers": len(peers),
            "peer_statuses": dict(sorted(peer_counts.items())),
            "stage_statuses": dict(sorted(stage_counts.items())),
            "next_commands": len(next_steps.get("commands") or []),
            "manual_actions": len(next_steps.get("manual_actions") or []),
        },
        "global_stages": global_stages,
        "peers": peers,
        "gate": compact_gate_payload(gate, limit=limit),
        "next": next_steps,
    }


def write_workflow(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = workflow_file()
    data = {**data, "workflow_path": rel(out)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def cmd_workflow(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = workflow_payload(
        snapshot,
        diagnostics,
        node_ids=args.node_ids or None,
        fail_on=fail_on,
        require_preflight=args.require_preflight,
        require_verify=args.require_verify,
        require_results=args.require_results,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_workflow(data)
        data["workflow_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0 if data["gate"]["passed"] else 1

    if args.write:
        print(f"syncmate workflow: {rel(out_path)}")
        print(
            f"  device={data['device_id']} status={data['status']} "
            f"gate={'pass' if data['gate'].get('passed') else 'fail'}"
        )
    else:
        print(
            f"syncmate workflow: {data['device_id']} status={data['status']} "
            f"gate={'pass' if data['gate'].get('passed') else 'fail'}"
        )
    print(
        f"  peers={data['summary']['peers']} next_commands={data['summary']['next_commands']} "
        f"manual_actions={data['summary']['manual_actions']}"
    )
    print("  global:")
    for stage in data["global_stages"]:
        command = f" -> {stage.get('command')}" if stage.get("command") else ""
        print(f"    - {stage['id']}: {stage['status']} - {stage['reason']}{command}")
    if data["peers"]:
        print("  peers:")
        for node_id, peer in sorted(data["peers"].items()):
            print(f"    - {node_id}: {peer['status']}")
            for stage in peer.get("stages") or []:
                command = f" -> {stage.get('command')}" if stage.get("command") else ""
                print(f"      {stage['id']}: {stage['status']} - {stage['reason']}{command}")
    commands = (data.get("next") or {}).get("commands") or []
    if commands:
        print("  next:")
        for idx, item in enumerate(commands[:max(0, args.limit)], start=1):
            print(f"    {idx}. {item['command']}")
            print(f"       {item['kind']}: {item['reason']}")
    return 0 if data["gate"]["passed"] else 1


def cmd_automation_core(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = automation_core_payload_from_snapshot(
        snapshot,
        node_ids=args.node_ids or None,
        limit=args.limit,
    )
    out_path = None
    markdown_path = None
    if args.write:
        out_path = write_automation_core(data)
        data["automation_core_path"] = rel(out_path)
        markdown_path = write_automation_core_markdown(data)
        data["automation_core_markdown_path"] = rel(markdown_path)
    if args.json:
        print_json(data)
        return 0

    if args.write:
        print(f"syncmate automation-core: {rel(out_path)}")
        print(f"  markdown: {rel(markdown_path)}")
    else:
        print(f"syncmate automation-core: {data.get('automation_core_path')}")
    totals = data.get("totals") or {}
    results = data.get("results") or {}
    delta = results.get("delta")
    delta_text = "unavailable" if delta is None else (
        f"added={delta.get('added_rows', 0)} changed={delta.get('changed_rows', 0)} "
        f"removed={delta.get('removed_rows', 0)}"
    )
    print(
        f"  status={data.get('status')} missing={totals.get('missing', 0)} "
        f"fetched={totals.get('fetched_missing', 0)} checksum_ok={totals.get('checksum_verified', 0)} "
        f"checksum_failed={totals.get('checksum_failed', 0)} indexed={totals.get('indexed', 0)}"
    )
    print(
        f"  results: status={results.get('status')} rows={results.get('rows', 0)} "
        f"parse_errors={results.get('parse_errors', 0)} delta={delta_text}"
    )
    files = data.get("files") or {}
    print(f"  files: index={files.get('artifact_index')} csv={files.get('results_csv')}")
    peers = data.get("peers") or {}
    if peers:
        print("  peers:")
        for node_id, peer in sorted(peers.items()):
            counts = peer.get("counts") or {}
            print(
                f"    - {node_id}: landing={peer.get('landing') or 'unknown'} "
                f"missing={counts.get('missing', 0)} fetched={counts.get('fetched_missing', 0)} "
                f"checksum_ok={counts.get('checksum_verified', 0)} failed={counts.get('checksum_failed', 0)} "
                f"indexed={counts.get('indexed', 0)} verify={peer.get('verify_status')}"
            )
            examples = peer.get("examples") or {}
            if examples.get("fetched"):
                first = examples["fetched"][0]
                if isinstance(first, dict):
                    print(f"      fetched: {first.get('path')} -> {first.get('local_path')}")
            if examples.get("indexed"):
                first = examples["indexed"][0]
                if isinstance(first, dict):
                    print(f"      indexed: {first.get('remote_path') or first.get('path')} sha256={first.get('sha256')}")
            trusted = peer.get("trusted_results") or {}
            if trusted.get("examples"):
                row = trusted["examples"][0]
                print(
                    f"      result: {row.get('cell')} {row.get('method_strategy')} "
                    f"{row.get('seed')} status={row.get('status')}"
                )
    return 0


def cmd_acceptance(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    fail_on = "info" if args.strict else args.fail_on
    data = acceptance_payload(
        snapshot,
        diagnostics,
        node_ids=args.node_ids or None,
        fail_on=fail_on,
        require_preflight=args.require_preflight,
        require_verify=args.require_verify,
        require_results=args.require_results,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_acceptance(data)
        data["acceptance_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0 if data.get("ready") else 1

    if args.write:
        print(f"syncmate acceptance: {rel(out_path)}")
    else:
        print(f"syncmate acceptance: {data.get('acceptance_path')}")
    gate = data.get("gate") or {}
    workflow = data.get("workflow") or {}
    core = data.get("automation_core") or {}
    totals = core.get("totals") or {}
    results = core.get("results") or {}
    print(
        f"  status={data.get('status')} ready={data.get('ready')} "
        f"gate={'pass' if gate.get('passed') else 'fail'} "
        f"workflow={workflow.get('status')} automation={core.get('status')}"
    )
    print(
        f"  missing={totals.get('missing', 0)} fetched={totals.get('fetched_missing', 0)} "
        f"checksum_ok={totals.get('checksum_verified', 0)} "
        f"checksum_failed={totals.get('checksum_failed', 0)} "
        f"indexed={totals.get('indexed', 0)} result_rows={results.get('rows', 0)}"
    )
    if data.get("blockers"):
        print(f"  blockers: {', '.join(data.get('blockers') or [])}")
    commands = ((data.get("next") or {}).get("commands") or [])[:max(0, args.limit)]
    if commands:
        print("  next:")
        for idx, item in enumerate(commands, start=1):
            print(f"    {idx}. {item.get('command')}")
            print(f"       {item.get('kind')}: {item.get('reason')}")
    return 0 if data.get("ready") else 1


def cmd_next(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    data = next_steps_payload(
        snapshot,
        diagnostics,
        require_verify=args.require_verify,
        require_preflight=args.require_preflight,
        require_results=args.require_results,
        limit=args.limit,
    )
    written = None
    if args.write:
        written = write_action_plan(data)
    if args.json:
        print_json(data)
        return 0

    print(f"syncmate next: {data['device_id']}")
    if data["commands"]:
        print("  commands:")
        for idx, item in enumerate(data["commands"], start=1):
            node = f" [{item['node_id']}]" if item.get("node_id") else ""
            print(f"    {idx}. {item['command']}")
            print(f"       {item['kind']}{node}: {item['reason']}")
            evidence = item.get("evidence") or {}
            writes = evidence.get("writes") or []
            if writes:
                print(f"       writes: {', '.join(writes)}")
            effects = item.get("effects") or []
            if effects:
                print(f"       effects: {', '.join(effects)}")
    else:
        print("  commands: none")
    if data["manual_actions"]:
        print("  manual actions:")
        for idx, item in enumerate(data["manual_actions"], start=1):
            node = f" [{item['node_id']}]" if item.get("node_id") else ""
            print(f"    {idx}. {item['action']}")
            print(f"       {item['kind']}{node}: {item['reason']}")
    if data["truncated"]:
        print("  note: output truncated; rerun with --limit for more")
    if written:
        print(f"  action plan: {written['json']}")
        print(f"  markdown: {written['markdown']}")
    return 0


def cmd_archive_orphans(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = archive_orphaned_sync_state(snapshot, apply=args.apply)
    if args.json:
        print_json(data)
        return 0 if not data.get("errors") else 1

    mode = "apply" if args.apply else "plan"
    summary = data["summary"]
    print(f"syncmate archive-orphans {mode}: {summary['orphaned_entries']} orphaned entrie(s)")
    print(f"  archive: {data['archive_dir']}")
    print(
        f"  reports={summary['report_files']} index_entries={summary['index_entries']} "
        f"actions={summary['actions']} errors={summary['errors']}"
    )
    for item in data["actions"]:
        print(
            f"  - {item['kind']} {item.get('node_id')}: {item['status']} "
            f"{item.get('source')} -> {item.get('archive_path')}"
        )
    for error in data.get("errors") or []:
        print(f"  error: {error}")
    if not args.apply and summary["actions"]:
        print("  next: rerun with --apply to move reports and rewrite orphaned index entries")
    return 0 if not data.get("errors") else 1


def cmd_status(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    if args.write_state:
        write_state(snapshot, "status")
    if args.json:
        print_json(snapshot)
        return 0

    print(f"syncmate status: {snapshot['device']['id']} ({snapshot['device']['role']})")
    print(f"  generated: {snapshot['generated_at']}")
    print(f"  git: {snapshot['git']['branch']} @ {snapshot['git']['short_sha']} dirty={snapshot['git']['dirty']}")
    print(f"  results: {snapshot['results']['total_leaves']} artifact leaves under {snapshot['results']['root']}")
    progress_summary = ((snapshot.get("progress") or {}).get("summary") or {})
    print(
        f"  logs: total={progress_summary.get('total_log_files', 0)} "
        f"scanned={progress_summary.get('scanned_log_files', 0)} "
        f"errors={progress_summary.get('error_logs', 0)} "
        f"newest={progress_summary.get('newest_age', 'unknown')}"
    )
    print(f"  remote reports: {len(snapshot.get('remote_status') or {})}")
    print(f"  bundle inspect reports: {len(snapshot.get('bundle_inspect_reports') or {})}")
    print(f"  diff reports: {len(snapshot.get('diff_reports') or {})}")
    print(f"  collect reports: {len(snapshot.get('collect_reports') or {})}")
    print(f"  verify reports: {len(snapshot.get('verify_reports') or {})}")
    index = snapshot.get("artifact_index") or {}
    print(f"  artifact index: {artifact_index_total(index)} verified artifact(s) across {len(index.get('peers') or {})} peer(s)")
    for node, info in snapshot["results"]["nodes"].items():
        files = ", ".join(f"{k}={v}" for k, v in sorted(info["files"].items()))
        layouts = ", ".join(f"{k}={v}" for k, v in sorted(info.get("layouts", {}).items()))
        issues = ", ".join(info["issues"]) if info["issues"] else "ok"
        print(f"  - {node}: leaves={info['leaves']} {files} layouts=[{layouts}] issues={issues}")
    if args.write_state:
        print(f"  wrote: {rel(STATE_FILE)}")
    return 0


def compact_git_for_publish(git: Dict[str, Any], *, limit: int = 10) -> Dict[str, Any]:
    status_short = git.get("status_short") or []
    return {
        "branch": git.get("branch"),
        "sha": git.get("sha"),
        "short_sha": git.get("short_sha"),
        "dirty": git.get("dirty"),
        "status_short_count": len(status_short),
        "status_short_sample": status_short[:max(0, limit)],
        "status_short_truncated": len(status_short) > max(0, limit),
    }


def compact_inventory_for_publish(inventory: Dict[str, Any], *, limit: int = 10) -> Dict[str, Any]:
    leaves = inventory.get("leaves") or []
    return {
        "summary": inventory.get("summary") or {},
        "sample_leaves": leaves[:max(0, limit)],
        "leaves_truncated": len(leaves) > max(0, limit),
    }


def compact_manifest_for_publish(manifest: Dict[str, Any], *, include_items: bool,
                                 limit: int = 10) -> Dict[str, Any]:
    items = manifest.get("items") or []
    data = {
        "generated_at": manifest.get("generated_at"),
        "repo_root": manifest.get("repo_root"),
        "roots": manifest.get("roots") or [],
        "artifact_policy": manifest.get("artifact_policy") or {},
        "count": manifest.get("count", len(items)),
        "git": compact_git_for_publish(manifest.get("git") or {}, limit=limit),
        "inventory": compact_inventory_for_publish(manifest.get("inventory") or {}, limit=limit),
    }
    if include_items:
        data["items"] = items
    else:
        data["sample_items"] = [public_manifest_item(item) for item in items[:max(0, limit)]]
        data["items_truncated"] = len(items) > max(0, limit)
    return data


def publish_payload(device: Dict[str, Any], warnings: List[str], *, roots: Optional[List[str]] = None,
                    include_items: bool = False, limit: int = 10) -> Dict[str, Any]:
    snapshot = build_snapshot(device, warnings)
    artifact_names = artifact_names_for_peer(device, None)
    manifest = manifest_for_roots(roots or ["results/runs"], artifact_names)
    progress_summary = ((snapshot.get("progress") or {}).get("summary") or {})
    results_summary = ((snapshot.get("results") or {}))
    manifest_summary = ((manifest.get("inventory") or {}).get("summary") or {})
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "publish",
        "package_version": 0,
        "device": snapshot.get("device") or {},
        "git": compact_git_for_publish(snapshot.get("git") or {}, limit=limit),
        "fingerprint": snapshot.get("fingerprint") or {},
        "progress": {
            "summary": progress_summary,
            "recent_logs": (snapshot.get("progress") or {}).get("recent_logs") or [],
            "error_logs": (snapshot.get("progress") or {}).get("error_logs") or [],
        },
        "results": {
            "root": results_summary.get("root"),
            "total_leaves": results_summary.get("total_leaves", 0),
            "nodes": results_summary.get("nodes") or {},
        },
        "manifest": compact_manifest_for_publish(manifest, include_items=include_items, limit=limit),
        "summary": {
            "device_id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "git_short_sha": (snapshot.get("git") or {}).get("short_sha"),
            "git_dirty": (snapshot.get("git") or {}).get("dirty"),
            "fingerprint": ((snapshot.get("fingerprint") or {}).get("token")),
            "result_leaves": results_summary.get("total_leaves", 0),
            "manifest_files": manifest.get("count", 0),
            "manifest_leaves": manifest_summary.get("leaves", 0),
            "manifest_incomplete": manifest_summary.get("incomplete", 0),
            "log_files": progress_summary.get("total_log_files", 0),
            "log_errors": progress_summary.get("error_logs", 0),
            "latest_log_age": progress_summary.get("newest_age"),
        },
        "files": {
            "publish": rel(publish_file((snapshot.get("device") or {}).get("id"))),
            "setup": rel(DEFAULT_DEVICE_FILE),
        },
        "errors": [],
    }


def write_publish(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    device_id = ((data.get("device") or {}).get("id")) or None
    out = publish_file(device_id)
    data["publish_path"] = rel(out)
    data.setdefault("files", {})["publish"] = rel(out)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out


def cmd_publish(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    data = publish_payload(
        device,
        warnings,
        roots=args.roots,
        include_items=args.include_items,
        limit=args.limit,
    )
    out_path = None
    if args.write:
        out_path = write_publish(data)
    if args.json:
        print_json(data)
        return 0

    summary = data.get("summary") or {}
    manifest = data.get("manifest") or {}
    print(f"syncmate publish: {summary.get('device_id')} ({summary.get('role')})")
    print(f"  git: {summary.get('git_short_sha')} dirty={summary.get('git_dirty')}")
    print(f"  fingerprint: {summary.get('fingerprint')}")
    print(
        f"  results: leaves={summary.get('result_leaves', 0)} "
        f"manifest_files={summary.get('manifest_files', 0)} "
        f"manifest_leaves={summary.get('manifest_leaves', 0)} "
        f"incomplete={summary.get('manifest_incomplete', 0)}"
    )
    print(
        f"  logs: total={summary.get('log_files', 0)} "
        f"errors={summary.get('log_errors', 0)} newest={summary.get('latest_log_age', 'unknown')}"
    )
    print(f"  roots: {', '.join(manifest.get('roots') or []) or 'none'}")
    if args.write:
        print(f"  wrote: {rel(out_path)}")
    else:
        print(f"  publish file: {data.get('files', {}).get('publish')}")
    if not args.include_items:
        print("  note: full manifest items are omitted; rerun with --include-items for complete checksums")
    return 0


def load_publish_package(package_path: str) -> Dict[str, Any]:
    if str(package_path) == "-":
        data = json.load(sys.stdin)
    else:
        path = Path(package_path)
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("publish package must be a JSON object")
    if data.get("mode") != "publish":
        raise SystemExit("publish package must have mode='publish'")
    return data


def node_id_from_publish(package: Dict[str, Any], override: Optional[str] = None) -> str:
    node_id = (
        override
        or ((package.get("summary") or {}).get("device_id"))
        or ((package.get("device") or {}).get("id"))
    )
    node_id = str(node_id or "").strip()
    if not node_id:
        raise SystemExit("publish package has no device id; pass --node-id")
    return node_id


def package_remote_source(peer: Optional[Dict[str, Any]], package: Dict[str, Any],
                          source: str) -> Dict[str, Any]:
    device = package.get("device") or {}
    remote: Dict[str, Any] = {
        "transport": peer_transport(peer) if peer else source,
        "source": source,
        "repo_path": (peer or {}).get("repo_path") or device.get("repo_path"),
        f"{source}_generated_at": package.get("generated_at"),
    }
    if peer:
        ssh_value = transport_ssh_value(peer)
        if is_local_transport_ref(ssh_value):
            remote["ssh"] = None
        elif ssh_value:
            remote["ssh"] = ssh_value
    return remote


def package_meta_payload(package: Dict[str, Any]) -> Dict[str, Any]:
    manifest = package.get("manifest") or {}
    return {
        "package_version": package.get("package_version"),
        "package_generated_at": package.get("generated_at"),
        "manifest_count": manifest.get("count", 0),
        "manifest_roots": manifest.get("roots") or [],
        "manifest_has_items": "items" in manifest,
        "items_truncated": manifest.get("items_truncated"),
    }


def remote_status_from_package(package: Dict[str, Any], node_id: str,
                               peer: Optional[Dict[str, Any]] = None,
                               *, source: str, mode: str) -> Dict[str, Any]:
    fingerprint = package.get("fingerprint") or {}
    progress = package.get("progress") or {}
    results = package.get("results") or {}
    manifest = package.get("manifest") or {}
    summary = package.get("summary") or {}
    device = package.get("device") or {}
    git = package.get("git") or {}

    snapshot = {
        "generated_at": package.get("generated_at"),
        "repo_root": device.get("repo_path") or manifest.get("repo_root"),
        "device": device,
        "git": git,
        "results": results,
        "progress": progress,
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": empty_artifact_index(),
        "export_manifest": None,
        "results_table": None,
        "preflight": None,
        "fingerprint": fingerprint,
        "published_manifest": manifest,
    }

    return {
        "generated_at": now_iso(),
        "node_id": node_id,
        "mode": mode,
        "remote": package_remote_source(peer, package, source),
        "snapshot": snapshot,
        "summary": {
            "device_id": summary.get("device_id") or device.get("id"),
            "role": summary.get("role") or device.get("role"),
            "git_short_sha": summary.get("git_short_sha") or git.get("short_sha"),
            "git_dirty": summary.get("git_dirty") if "git_dirty" in summary else git.get("dirty"),
            "result_leaves": summary.get("result_leaves", results.get("total_leaves", 0)),
            "result_nodes": sorted((results.get("nodes") or {}).keys()),
            "log_files": summary.get("log_files", (progress.get("summary") or {}).get("total_log_files", 0)),
            "log_errors": summary.get("log_errors", (progress.get("summary") or {}).get("error_logs", 0)),
            "latest_log_age": summary.get("latest_log_age", (progress.get("summary") or {}).get("newest_age")),
            "fingerprint": summary.get("fingerprint") or fingerprint.get("token"),
            "fingerprint_components": fingerprint.get("components") or {},
            "manifest_files": summary.get("manifest_files", manifest.get("count", 0)),
            "manifest_leaves": summary.get("manifest_leaves", ((manifest.get("inventory") or {}).get("summary") or {}).get("leaves", 0)),
            "manifest_incomplete": summary.get("manifest_incomplete", ((manifest.get("inventory") or {}).get("summary") or {}).get("incomplete", 0)),
        },
        source: package_meta_payload(package),
        "errors": [],
    }


def remote_status_from_publish(package: Dict[str, Any], node_id: str,
                               peer: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return remote_status_from_package(package, node_id, peer, source="publish", mode="import-publish")


def cmd_import_publish(args: argparse.Namespace) -> int:
    device, _warnings = load_device(args.config)
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    package = load_publish_package(args.package)
    node_id = node_id_from_publish(package, args.node_id)
    peer = peers.get(node_id) if isinstance(peers, dict) else None
    result = remote_status_from_publish(package, node_id, peer)
    result["known_peer"] = bool(peer)
    result["saved"] = not args.no_save
    if not args.no_save:
        write_sync_report("remote_status", node_id, result)

    if args.json:
        print_json(result)
        return 0

    summary = result.get("summary") or {}
    publish = result.get("publish") or {}
    print(f"syncmate import-publish: {node_id}")
    print(f"  known peer: {result.get('known_peer')}")
    print(f"  device: {summary.get('device_id')} ({summary.get('role')})")
    print(f"  git: {summary.get('git_short_sha')} dirty={summary.get('git_dirty')}")
    print(f"  fingerprint: {summary.get('fingerprint')}")
    print(
        f"  results: leaves={summary.get('result_leaves', 0)} "
        f"manifest_files={summary.get('manifest_files', 0)} "
        f"manifest_leaves={summary.get('manifest_leaves', 0)} "
        f"incomplete={summary.get('manifest_incomplete', 0)}"
    )
    print(
        f"  publish: generated={publish.get('package_generated_at')} "
        f"items={'full' if publish.get('manifest_has_items') else 'sample'}"
    )
    if result.get("report_path"):
        print(f"  report: {result['report_path']}")
    elif args.no_save:
        print("  report: not saved (--no-save)")
    return 0


def bundle_payload(device: Dict[str, Any], warnings: List[str], *, roots: Optional[List[str]] = None) -> Dict[str, Any]:
    snapshot = build_snapshot(device, warnings)
    artifact_names = artifact_names_for_peer(device, None)
    manifest = manifest_for_roots(roots or ["results/runs"], artifact_names)
    progress_summary = ((snapshot.get("progress") or {}).get("summary") or {})
    results_summary = snapshot.get("results") or {}
    manifest_summary = ((manifest.get("inventory") or {}).get("summary") or {})
    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "bundle",
        "package_version": 0,
        "device": snapshot.get("device") or {},
        "git": compact_git_for_publish(snapshot.get("git") or {}),
        "fingerprint": snapshot.get("fingerprint") or {},
        "progress": {
            "summary": progress_summary,
            "recent_logs": (snapshot.get("progress") or {}).get("recent_logs") or [],
            "error_logs": (snapshot.get("progress") or {}).get("error_logs") or [],
        },
        "results": {
            "root": results_summary.get("root"),
            "total_leaves": results_summary.get("total_leaves", 0),
            "nodes": results_summary.get("nodes") or {},
        },
        "manifest": manifest,
        "summary": {
            "device_id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "git_short_sha": (snapshot.get("git") or {}).get("short_sha"),
            "git_dirty": (snapshot.get("git") or {}).get("dirty"),
            "fingerprint": ((snapshot.get("fingerprint") or {}).get("token")),
            "result_leaves": results_summary.get("total_leaves", 0),
            "manifest_files": manifest.get("count", 0),
            "manifest_leaves": manifest_summary.get("leaves", 0),
            "manifest_incomplete": manifest_summary.get("incomplete", 0),
            "log_files": progress_summary.get("total_log_files", 0),
            "log_errors": progress_summary.get("error_logs", 0),
            "latest_log_age": progress_summary.get("newest_age"),
        },
        "files": {
            "bundle": rel(bundle_file((snapshot.get("device") or {}).get("id"))),
            "setup": rel(DEFAULT_DEVICE_FILE),
        },
        "errors": [],
    }


def resolve_output_path(path: Optional[Path], default_path: Path) -> Path:
    out = path or default_path
    if not out.is_absolute():
        out = REPO_ROOT / out
    return out


def write_bundle(data: Dict[str, Any], output: Optional[Path] = None) -> Path:
    ensure_sync_dir()
    device_id = ((data.get("device") or {}).get("id")) or None
    out = resolve_output_path(output, bundle_file(device_id))
    out.parent.mkdir(parents=True, exist_ok=True)
    data["bundle_path"] = rel(out)
    data.setdefault("files", {})["bundle"] = rel(out)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(BUNDLE_MANIFEST_NAME, json.dumps(data, indent=2, ensure_ascii=False))
        for item in (data.get("manifest") or {}).get("items") or []:
            remote_rel = str(item.get("path") or "")
            if not remote_rel:
                continue
            source = (REPO_ROOT / remote_rel).resolve()
            try:
                source.relative_to(REPO_ROOT)
            except ValueError:
                raise SystemExit(f"Unsafe bundle source path: {remote_rel}")
            if not source.is_file():
                raise SystemExit(f"Bundle source file disappeared: {remote_rel}")
            zf.write(source, remote_rel)
    return out


HANDOFF_PACK_PATTERNS = (
    "status.html",
    "runbook.md",
    "checklist.md",
    "brief.md",
    "workflow.json",
    "automation_core.json",
    "automation_core.md",
    "acceptance.json",
    "action_plan.json",
    "action_plan.md",
    "last_preflight.json",
    "state.json",
    "history.jsonl",
    "artifact_index.json",
    "results_table.json",
    "results_table.csv",
    "export_manifest.json",
    "export_manifest.csv",
    "receipt*.md",
    "handoff*.md",
    "remote_status_*.json",
    "last_bundle_inspect_*.json",
    "last_handoff_pack_inspect_*.json",
    "last_diff_*.json",
    "last_collect_*.json",
    "last_verify_*.json",
    "import_bundle_plan_*.json",
    "publish_*.json",
)


def handoff_pack_candidates(*, include_setup: bool = False) -> List[Path]:
    candidates: Dict[str, Path] = {}
    if include_setup and DEFAULT_DEVICE_FILE.is_file():
        candidates[DEFAULT_DEVICE_FILE.resolve().as_posix()] = DEFAULT_DEVICE_FILE.resolve()
    for pattern in HANDOFF_PACK_PATTERNS:
        for path in SYNC_DIR.glob(pattern):
            if not path.is_file():
                continue
            if path.suffix.lower() == ".zip":
                continue
            resolved = path.resolve()
            try:
                resolved.relative_to(SYNC_DIR.resolve())
            except ValueError:
                continue
            candidates[resolved.as_posix()] = resolved
    return sorted(candidates.values(), key=lambda item: rel(item))


def handoff_pack_payload(snapshot: Dict[str, Any], *,
                         files: List[Path],
                         output: Path,
                         include_setup: bool) -> Dict[str, Any]:
    file_rows = []
    for path in files:
        stat = path.stat()
        file_rows.append({
            "path": rel(path),
            "size": stat.st_size,
            "sha256": sha256_file(path),
        })
    return {
        "generated_at": now_iso(),
        "mode": "handoff-pack",
        "package_version": 0,
        "handoff_pack_path": rel(output),
        "device": (snapshot.get("device") or {}),
        "git": compact_git_for_publish(snapshot.get("git") or {}),
        "fingerprint": snapshot.get("fingerprint") or {},
        "include_setup": include_setup,
        "policy": {
            "contains_raw_artifacts": False,
            "contains_device_setup": include_setup,
            "root": rel(SYNC_DIR),
            "patterns": list(HANDOFF_PACK_PATTERNS),
        },
        "summary": {
            "files": len(file_rows),
            "bytes": sum(item["size"] for item in file_rows),
            "configured_peers": len(((snapshot.get("device") or {}).get("peers") or [])),
            "indexed_artifacts": artifact_index_total(snapshot.get("artifact_index") or {}),
            "result_rows": (((snapshot.get("results_table") or {}).get("summary") or {}).get("rows", 0)
                            if isinstance(snapshot.get("results_table"), dict) else 0),
        },
        "files": file_rows,
    }


def write_handoff_pack(data: Dict[str, Any], files: List[Path], output: Optional[Path] = None) -> Path:
    ensure_sync_dir()
    device_id = ((data.get("device") or {}).get("id")) or None
    out = resolve_output_path(output, handoff_pack_file(device_id))
    out.parent.mkdir(parents=True, exist_ok=True)
    data["handoff_pack_path"] = rel(out)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(HANDOFF_PACK_MANIFEST_NAME, json.dumps(data, indent=2, ensure_ascii=False))
        out_resolved = out.resolve()
        for path in files:
            resolved = path.resolve()
            if resolved == out_resolved:
                continue
            try:
                arcname = resolved.relative_to(REPO_ROOT.resolve()).as_posix()
            except ValueError:
                arcname = f".syncmate/{resolved.name}"
            zf.write(resolved, arcname)
    return out


def cmd_handoff_pack(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    if not args.no_refresh:
        write_dashboard(snapshot, diagnostics)
        brief_data = brief_payload(snapshot, diagnostics, require_verify=True, limit=args.limit)
        brief_path = write_brief(brief_data)
        brief_data["brief_path"] = rel(brief_path)
    files = handoff_pack_candidates(include_setup=args.include_setup)
    device_id = ((snapshot.get("device") or {}).get("id")) or None
    output = resolve_output_path(args.output, handoff_pack_file(device_id))
    data = handoff_pack_payload(
        snapshot,
        files=files,
        output=output,
        include_setup=args.include_setup,
    )
    out_path = write_handoff_pack(data, files, args.output)
    data["handoff_pack_path"] = rel(out_path)
    if args.json:
        print_json(data)
        return 0
    summary = data.get("summary") or {}
    print(f"syncmate handoff-pack: {data['handoff_pack_path']}")
    print(f"  files: {summary.get('files', 0)} bytes={summary.get('bytes', 0)}")
    print(f"  raw artifacts: no")
    print(f"  device setup: {'included' if args.include_setup else 'excluded'}")
    return 0


def load_handoff_pack_package(pack_path: str) -> Dict[str, Any]:
    path = Path(pack_path)
    with zipfile.ZipFile(path) as zf:
        try:
            raw = zf.read(HANDOFF_PACK_MANIFEST_NAME)
        except KeyError:
            raise SystemExit(f"Handoff pack is missing {HANDOFF_PACK_MANIFEST_NAME}")
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("handoff pack manifest must be a JSON object")
    if data.get("mode") != "handoff-pack":
        raise SystemExit("handoff pack manifest must have mode='handoff-pack'")
    data["_handoff_pack_path"] = str(path)
    return data


def audit_handoff_pack_package(package: Dict[str, Any]) -> Dict[str, Any]:
    pack_path = Path(package.get("_handoff_pack_path") or "")
    errors: List[str] = []
    warnings: List[str] = []
    policy = package.get("policy")
    if not isinstance(policy, dict):
        policy = {}
        errors.append("handoff pack policy must be an object")
    if policy.get("contains_raw_artifacts") is not False:
        errors.append("handoff pack policy must declare contains_raw_artifacts=false")

    raw_files = package.get("files")
    if not isinstance(raw_files, list):
        files: List[Dict[str, Any]] = []
        errors.append("handoff pack manifest must include a files list")
    else:
        files = [item for item in raw_files if isinstance(item, dict)]
        if len(files) != len(raw_files):
            errors.append("handoff pack files must all be objects")

    manifest_paths: List[str] = []
    for idx, item in enumerate(files):
        path = item.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"handoff pack file #{idx} has no path")
            continue
        if path == HANDOFF_PACK_MANIFEST_NAME or not is_safe_repo_relative_path(path):
            errors.append(f"handoff pack file has unsafe path: {path!r}")
            continue
        if path.replace("\\", "/").startswith("results/runs/"):
            errors.append(f"handoff pack file points at raw results artifact: {path}")
            continue
        manifest_paths.append(path)
        if not is_sha256_hex(item.get("sha256")):
            errors.append(f"handoff pack file {path} has invalid sha256")

    for path in sorted(path for path, count in Counter(manifest_paths).items() if count > 1):
        errors.append(f"handoff pack manifest has duplicate file path: {path}")
    summary = package.get("summary") if isinstance(package.get("summary"), dict) else {}
    if "files" in summary and summary.get("files") != len(files):
        errors.append(f"handoff pack summary files={summary.get('files')} but manifest files={len(files)}")

    member_files: List[str] = []
    verified_files = 0
    try:
        with zipfile.ZipFile(pack_path) as zf:
            member_files = [name.replace("\\", "/") for name in zf.namelist() if not name.endswith("/")]
            member_set = set(member_files)
            for item in files:
                path = item.get("path")
                expected = item.get("sha256")
                if not isinstance(path, str) or path not in member_set or not is_sha256_hex(expected):
                    continue
                digest = hashlib.sha256()
                with zf.open(path) as src:
                    for chunk in iter(lambda: src.read(1024 * 1024), b""):
                        digest.update(chunk)
                actual = digest.hexdigest()
                if actual == str(expected).lower():
                    verified_files += 1
                else:
                    errors.append(f"handoff pack checksum mismatch: {path} expected {expected} got {actual}")
    except Exception as e:
        errors.append(f"handoff pack zip unreadable: {type(e).__name__}: {e}")
        member_files = []

    for name in sorted(name for name, count in Counter(member_files).items() if count > 1):
        errors.append(f"handoff pack zip has duplicate member: {name}")

    member_set = set(member_files)
    if HANDOFF_PACK_MANIFEST_NAME not in member_set:
        errors.append(f"handoff pack zip is missing {HANDOFF_PACK_MANIFEST_NAME}")
    for name in sorted(member_set):
        if name == HANDOFF_PACK_MANIFEST_NAME:
            continue
        if not is_safe_repo_relative_path(name):
            errors.append(f"handoff pack zip has unsafe member: {name!r}")
        if name.startswith("results/runs/"):
            errors.append(f"handoff pack zip contains raw results artifact: {name}")

    expected_members = set(manifest_paths)
    for path in sorted(expected_members - member_set):
        errors.append(f"handoff pack zip missing manifest file: {path}")
    for name in sorted(member_set - expected_members - {HANDOFF_PACK_MANIFEST_NAME}):
        warnings.append(f"handoff pack zip has extra member not listed in manifest: {name}")

    setup_member = ".syncmate/device.yaml" in member_set
    declares_setup = bool(policy.get("contains_device_setup") or package.get("include_setup"))
    if setup_member and not declares_setup:
        errors.append("handoff pack includes .syncmate/device.yaml but policy does not declare setup inclusion")
    if declares_setup and not setup_member:
        warnings.append("handoff pack declares setup inclusion but .syncmate/device.yaml is absent")

    return {
        "status": "invalid" if errors else "ok",
        "zip_sha256": sha256_file(pack_path) if pack_path.is_file() else None,
        "manifest_files": len(files),
        "zip_members": len(member_files),
        "verified_files": verified_files,
        "contains_raw_artifacts": any(name.startswith("results/runs/") for name in member_set),
        "contains_device_setup": setup_member,
        "errors": errors,
        "warnings": warnings,
    }


def inspect_handoff_pack_payload(pack_path: str, *, limit: int = 20) -> Dict[str, Any]:
    path = Path(pack_path)
    try:
        package = load_handoff_pack_package(pack_path)
    except SystemExit as e:
        message = str(e)
        return {
            "generated_at": now_iso(),
            "mode": "inspect-handoff-pack",
            "handoff_pack_path": path.as_posix(),
            "audit": {
                "status": "invalid",
                "manifest_files": 0,
                "zip_members": 0,
                "verified_files": 0,
                "errors": [message],
                "warnings": [],
            },
            "errors": [message],
        }
    except Exception as e:
        message = f"handoff pack inspect failed: {type(e).__name__}: {e}"
        return {
            "generated_at": now_iso(),
            "mode": "inspect-handoff-pack",
            "handoff_pack_path": path.as_posix(),
            "audit": {
                "status": "invalid",
                "manifest_files": 0,
                "zip_members": 0,
                "verified_files": 0,
                "errors": [message],
                "warnings": [],
            },
            "errors": [message],
        }

    audit = audit_handoff_pack_package(package)
    device = package.get("device") if isinstance(package.get("device"), dict) else {}
    files = [item for item in package.get("files") or [] if isinstance(item, dict)]
    sample_limit = max(0, limit)
    return {
        "generated_at": now_iso(),
        "mode": "inspect-handoff-pack",
        "node_id": device.get("id"),
        "handoff_pack_path": rel(path.resolve()) if path.exists() else path.as_posix(),
        "package_generated_at": package.get("generated_at"),
        "package_version": package.get("package_version"),
        "device": {
            "id": device.get("id"),
            "role": device.get("role"),
            "repo_path": device.get("repo_path"),
        },
        "git": package.get("git") or {},
        "fingerprint": package.get("fingerprint") or {},
        "policy": package.get("policy") or {},
        "summary": package.get("summary") or {},
        "files": {
            "count": len(files),
            "sample": files[:sample_limit],
            "truncated": len(files) > sample_limit,
        },
        "audit": audit,
        "errors": list(audit.get("errors") or []),
    }


def handoff_pack_inspect_node_id(data: Dict[str, Any], override: Optional[str] = None) -> str:
    node_id = override or data.get("node_id") or ((data.get("device") or {}).get("id"))
    node_id = str(node_id or "").strip()
    if not node_id:
        pack_path = str(data.get("handoff_pack_path") or "")
        stem = Path(pack_path).stem
        node_id = stem.replace("handoff_pack_", "", 1) if stem else ""
    if not node_id:
        raise SystemExit("handoff pack inspect report has no device id; pass --node-id")
    return node_id


def cmd_inspect_handoff_pack(args: argparse.Namespace) -> int:
    data = inspect_handoff_pack_payload(args.handoff_pack, limit=args.limit)
    out_path = None
    if args.write:
        node_id = handoff_pack_inspect_node_id(data, args.node_id)
        data["node_id"] = node_id
        out_path = write_sync_report("last_handoff_pack_inspect", node_id, data).get("report_path")
    if args.json:
        print_json(data)
        return 0 if not data.get("errors") else 1

    audit = data.get("audit") or {}
    device = data.get("device") or {}
    print(f"syncmate inspect-handoff-pack: {data.get('handoff_pack_path')}")
    print(f"  audit: {audit.get('status')} errors={len(audit.get('errors') or [])} warnings={len(audit.get('warnings') or [])}")
    print(f"  device: {device.get('id')} ({device.get('role')})")
    print(f"  files: {audit.get('verified_files', 0)}/{audit.get('manifest_files', 0)} verified")
    print(f"  zip_sha256: {audit.get('zip_sha256')}")
    print(f"  raw artifacts: {'yes' if audit.get('contains_raw_artifacts') else 'no'}")
    print(f"  device setup: {'included' if audit.get('contains_device_setup') else 'excluded'}")
    for warning in audit.get("warnings") or []:
        print(f"  warning: {warning}")
    for error in audit.get("errors") or []:
        print(f"  error: {error}")
    if out_path:
        print(f"  report: {out_path}")
    return 0 if not data.get("errors") else 1


def cmd_bundle(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    data = bundle_payload(device, warnings, roots=args.roots)
    out_path = write_bundle(data, args.output)
    if args.json:
        print_json(data)
        return 0

    summary = data.get("summary") or {}
    manifest = data.get("manifest") or {}
    print(f"syncmate bundle: {summary.get('device_id')} ({summary.get('role')})")
    print(f"  git: {summary.get('git_short_sha')} dirty={summary.get('git_dirty')}")
    print(f"  fingerprint: {summary.get('fingerprint')}")
    print(
        f"  results: leaves={summary.get('result_leaves', 0)} "
        f"manifest_files={summary.get('manifest_files', 0)} "
        f"manifest_leaves={summary.get('manifest_leaves', 0)} "
        f"incomplete={summary.get('manifest_incomplete', 0)}"
    )
    print(f"  roots: {', '.join(manifest.get('roots') or []) or 'none'}")
    print(f"  wrote: {rel(out_path)}")
    return 0


def inspect_bundle_payload(bundle_path: str, *, limit: int = 10) -> Dict[str, Any]:
    path = Path(bundle_path)
    try:
        package = load_bundle_package(bundle_path)
    except SystemExit as e:
        message = str(e)
        return {
            "generated_at": now_iso(),
            "mode": "inspect-bundle",
            "bundle_path": path.as_posix(),
            "audit": {
                "status": "invalid",
                "manifest_items": 0,
                "zip_members": 0,
                "errors": [message],
                "warnings": [],
            },
            "errors": [message],
        }
    except Exception as e:
        message = f"bundle inspect failed: {type(e).__name__}: {e}"
        return {
            "generated_at": now_iso(),
            "mode": "inspect-bundle",
            "bundle_path": path.as_posix(),
            "audit": {
                "status": "invalid",
                "manifest_items": 0,
                "zip_members": 0,
                "errors": [message],
                "warnings": [],
            },
            "errors": [message],
        }

    audit = audit_bundle_package(package)
    manifest = package.get("manifest") if isinstance(package.get("manifest"), dict) else {}
    raw_items = manifest.get("items") if isinstance(manifest.get("items"), list) else []
    items = [item for item in raw_items if isinstance(item, dict)]
    inventory = manifest.get("inventory") or manifest_inventory_from_items(items)
    inventory_summary = inventory.get("summary") or {}
    summary = package.get("summary") or {}
    device = package.get("device") or {}
    git = package.get("git") or {}
    fingerprint = package.get("fingerprint") or {}
    sample_limit = max(0, limit)
    return {
        "generated_at": now_iso(),
        "mode": "inspect-bundle",
        "node_id": summary.get("device_id") or device.get("id"),
        "bundle_path": rel(path.resolve()) if path.exists() else path.as_posix(),
        "package_generated_at": package.get("generated_at"),
        "package_version": package.get("package_version"),
        "device": {
            "id": summary.get("device_id") or device.get("id"),
            "role": summary.get("role") or device.get("role"),
            "repo_path": device.get("repo_path"),
        },
        "git": {
            "short_sha": summary.get("git_short_sha") or git.get("short_sha"),
            "dirty": summary.get("git_dirty") if "git_dirty" in summary else git.get("dirty"),
        },
        "fingerprint": {
            "token": summary.get("fingerprint") or fingerprint.get("token"),
            "components": fingerprint.get("components") or {},
        },
        "manifest": {
            "roots": manifest.get("roots") or [],
            "artifact_policy": manifest.get("artifact_policy") or {},
            "count": manifest.get("count", len(items)),
            "inventory_summary": inventory_summary,
            "sample_items": [public_manifest_item(item) for item in items[:sample_limit]],
            "items_truncated": len(items) > sample_limit,
        },
        "audit": audit,
        "commands": {
            "dry_run": command_line(["python", "scripts/syncmate/syncmate.py", "import-bundle", str(path), "--dry-run"]),
            "import": command_line(["python", "scripts/syncmate/syncmate.py", "import-bundle", str(path)]),
        },
        "errors": list(audit.get("errors") or []),
    }


def bundle_inspect_node_id(data: Dict[str, Any], override: Optional[str] = None) -> str:
    node_id = override or data.get("node_id") or ((data.get("device") or {}).get("id"))
    node_id = str(node_id or "").strip()
    if not node_id:
        raise SystemExit("bundle inspect report has no device id; pass --node-id")
    return node_id


def cmd_inspect_bundle(args: argparse.Namespace) -> int:
    data = inspect_bundle_payload(args.bundle, limit=args.limit)
    out_path = None
    if args.write:
        node_id = bundle_inspect_node_id(data, args.node_id)
        data["node_id"] = node_id
        out_path = write_sync_report("last_bundle_inspect", node_id, data).get("report_path")
    if args.json:
        print_json(data)
        return 0 if not data.get("errors") else 1

    audit = data.get("audit") or {}
    manifest = data.get("manifest") or {}
    inventory = manifest.get("inventory_summary") or {}
    device = data.get("device") or {}
    git = data.get("git") or {}
    fingerprint = data.get("fingerprint") or {}
    print(f"syncmate inspect-bundle: {data.get('bundle_path')}")
    print(f"  audit: {audit.get('status')} errors={len(audit.get('errors') or [])} warnings={len(audit.get('warnings') or [])}")
    print(f"  device: {device.get('id')} ({device.get('role')})")
    print(f"  git: {git.get('short_sha')} dirty={git.get('dirty')}")
    print(f"  fingerprint: {fingerprint.get('token')}")
    print(
        f"  manifest: files={manifest.get('count', 0)} "
        f"leaves={inventory.get('leaves', 0)} "
        f"incomplete={inventory.get('incomplete', 0)}"
    )
    for item in manifest.get("sample_items") or []:
        print(f"    - {item.get('path')} {item.get('sha256')}")
    if manifest.get("items_truncated"):
        print("    ... more items omitted")
    for warning in audit.get("warnings") or []:
        print(f"  warning: {warning}")
    for error in audit.get("errors") or []:
        print(f"  error: {error}")
    commands = data.get("commands") or {}
    if commands:
        print(f"  dry-run: {commands.get('dry_run')}")
        print(f"  import: {commands.get('import')}")
    if out_path:
        print(f"  report: {out_path}")
    return 0 if not data.get("errors") else 1


def load_bundle_package(bundle_path: str) -> Dict[str, Any]:
    path = Path(bundle_path)
    with zipfile.ZipFile(path) as zf:
        try:
            raw = zf.read(BUNDLE_MANIFEST_NAME)
        except KeyError:
            raise SystemExit(f"Bundle is missing {BUNDLE_MANIFEST_NAME}")
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("bundle manifest must be a JSON object")
    if data.get("mode") != "bundle":
        raise SystemExit("bundle manifest must have mode='bundle'")
    data["_bundle_path"] = str(path)
    return data


def is_sha256_hex(value: Any) -> bool:
    text = str(value or "")
    return len(text) == 64 and all(ch in "0123456789abcdefABCDEF" for ch in text)


def audit_bundle_package(package: Dict[str, Any]) -> Dict[str, Any]:
    bundle_path = Path(package.get("_bundle_path") or "")
    errors: List[str] = []
    warnings: List[str] = []
    manifest = package.get("manifest")
    if not isinstance(manifest, dict):
        manifest = {}
        errors.append("bundle manifest field 'manifest' must be an object")
    raw_items = manifest.get("items")
    if not isinstance(raw_items, list):
        items: List[Dict[str, Any]] = []
        errors.append("bundle manifest must include a full items list")
    else:
        items = [item for item in raw_items if isinstance(item, dict)]
        if len(items) != len(raw_items):
            errors.append("bundle manifest items must all be objects")

    manifest_paths: List[str] = []
    for idx, item in enumerate(items):
        path = item.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"bundle manifest item #{idx} has no path")
            continue
        if path == BUNDLE_MANIFEST_NAME or not is_safe_repo_relative_path(path):
            errors.append(f"bundle manifest item has unsafe path: {path!r}")
            continue
        manifest_paths.append(path)
        if not is_sha256_hex(item.get("sha256")):
            errors.append(f"bundle manifest item {path} has invalid sha256")

    duplicate_manifest_paths = sorted(path for path, count in Counter(manifest_paths).items() if count > 1)
    for path in duplicate_manifest_paths:
        errors.append(f"bundle manifest has duplicate item path: {path}")

    if "count" in manifest and manifest.get("count") != len(items):
        errors.append(f"bundle manifest count={manifest.get('count')} but items={len(items)}")

    member_files: List[str] = []
    try:
        with zipfile.ZipFile(bundle_path) as zf:
            member_files = [name.replace("\\", "/") for name in zf.namelist() if not name.endswith("/")]
    except Exception as e:
        errors.append(f"bundle zip unreadable: {type(e).__name__}: {e}")
        member_files = []

    duplicate_members = sorted(name for name, count in Counter(member_files).items() if count > 1)
    for name in duplicate_members:
        errors.append(f"bundle zip has duplicate member: {name}")

    member_set = set(member_files)
    if BUNDLE_MANIFEST_NAME not in member_set:
        errors.append(f"bundle zip is missing {BUNDLE_MANIFEST_NAME}")

    expected = set(manifest_paths)
    for path in sorted(expected - member_set):
        errors.append(f"bundle zip missing manifest item: {path}")
    for name in sorted(member_set - expected - {BUNDLE_MANIFEST_NAME}):
        if not is_safe_repo_relative_path(name):
            errors.append(f"bundle zip has unsafe extra member: {name!r}")
        else:
            warnings.append(f"bundle zip has extra member not listed in manifest: {name}")

    return {
        "status": "invalid" if errors else "ok",
        "manifest_items": len(items),
        "zip_members": len(member_files),
        "errors": errors,
        "warnings": warnings,
    }


def bundle_peer_context(device: Dict[str, Any], node_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    peer = peers.get(node_id) if isinstance(peers, dict) else None
    landing = (peer or {}).get("landing") or f"results/runs/{node_id}"
    return peer, landing


def extract_bundle_items(bundle_path: Path, items: List[Dict[str, Any]], landing: str
                         ) -> Tuple[List[Dict[str, Any]], List[str]]:
    fetched: List[Dict[str, Any]] = []
    errors: List[str] = []
    with zipfile.ZipFile(bundle_path) as zf:
        names = set(zf.namelist())
        for item in items:
            remote_rel = str(item.get("path") or "")
            if not remote_rel:
                continue
            if remote_rel not in names:
                errors.append(f"bundle missing member: {remote_rel}")
                continue
            target = local_landing_path(landing, remote_rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp_path: Optional[Path] = None
            try:
                digest = hashlib.sha256()
                with zf.open(remote_rel) as src:
                    with tempfile.NamedTemporaryFile(
                        "wb",
                        delete=False,
                        dir=str(target.parent),
                        prefix=".syncmate_import_",
                        suffix=".part",
                    ) as tmp:
                        tmp_path = Path(tmp.name)
                        for chunk in iter(lambda: src.read(1024 * 1024), b""):
                            digest.update(chunk)
                            tmp.write(chunk)
                actual = digest.hexdigest()
                expected = item.get("sha256")
                if expected and actual != expected:
                    errors.append(f"bundle checksum mismatch: {remote_rel} expected {expected} got {actual}")
                    try:
                        tmp_path.unlink()
                    except OSError:
                        pass
                    continue
                tmp_path.replace(target)
                fetched.append({"path": remote_rel, "local_path": rel(target), "sha256": actual})
            except Exception as e:
                if tmp_path and tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except OSError:
                        pass
                errors.append(f"bundle extract failed: {remote_rel}: {type(e).__name__}: {e}")
    return fetched, errors


def bundle_remote_payload(package: Dict[str, Any], peer: Optional[Dict[str, Any]],
                          bundle_path: Path) -> Dict[str, Any]:
    remote = package_remote_source(peer, package, "bundle")
    manifest = package.get("manifest") or {}
    remote.update({
        "bundle_path": rel(bundle_path),
        "roots": manifest.get("roots") or [],
        "git": manifest.get("git") or package.get("git"),
        "count": manifest.get("count", 0),
    })
    return remote


def bundle_report_base(package: Dict[str, Any], node_id: str, landing: str,
                       peer: Optional[Dict[str, Any]], bundle_path: Path,
                       manifest: Dict[str, Any]) -> Dict[str, Any]:
    items = manifest.get("items") or []
    remote_inventory = manifest.get("inventory") or manifest_inventory_from_items(items)
    inventory_summary = remote_inventory.get("summary") or {}
    return {
        "generated_at": now_iso(),
        "node_id": node_id,
        "landing": landing,
        "artifact_policy": manifest.get("artifact_policy") or {},
        "remote": bundle_remote_payload(package, peer, bundle_path),
        "summary": {
            "remote_files": len(items),
            "remote_leaves": inventory_summary.get("leaves", 0),
            "remote_incomplete": inventory_summary.get("incomplete", 0),
        },
        "remote_inventory": remote_inventory,
        "errors": [],
    }


def import_bundle_payload(device: Dict[str, Any], package: Dict[str, Any], *,
                          node_id: str, overwrite: bool, save: bool,
                          dry_run: bool = False, write_results: bool = False,
                          save_plan: bool = False) -> Dict[str, Any]:
    bundle_path = Path(package.get("_bundle_path") or "")
    manifest = package.get("manifest") or {}
    peer, landing = bundle_peer_context(device, node_id)
    audit = audit_bundle_package(package)
    if audit.get("errors"):
        remote_status = remote_status_from_package(
            package,
            node_id,
            peer,
            source="bundle",
            mode="import-bundle-status",
        )
        remote_status["known_peer"] = bool(peer)
        collect = bundle_report_base(package, node_id, landing, peer, bundle_path, manifest if isinstance(manifest, dict) else {})
        collect["mode"] = "import-bundle-invalid"
        collect["bundle_audit"] = audit
        collect["errors"] = list(audit.get("errors") or [])
        verify = bundle_report_base(package, node_id, landing, peer, bundle_path, manifest if isinstance(manifest, dict) else {})
        verify["mode"] = "verify"
        verify["summary"].update({
            "verified_current": 0,
            "missing": 0,
            "conflicts": 0,
            "status": "invalid-bundle",
        })
        verify["bundle_audit"] = audit
        verify["missing"] = []
        verify["conflicts"] = []
        verify["verified"] = []
        verify["errors"] = list(audit.get("errors") or [])
        plan_report_path = None
        remote_status_report_path = None
        if dry_run and save_plan:
            remote_status_report_path = write_sync_report("remote_status", node_id, remote_status).get("report_path")
            plan_report_path = write_sync_report("last_diff", node_id, collect).get("report_path")
        return {
            "generated_at": now_iso(),
            "mode": "import-bundle-invalid",
            "node_id": node_id,
            "known_peer": bool(peer),
            "saved": False,
            "plan_saved": bool(plan_report_path),
            "dry_run": bool(dry_run),
            "landing": landing,
            "bundle_audit": audit,
            "remote_status": remote_status,
            "collect": collect,
            "verify": verify,
            "results": {"written": False, "reason": "invalid-bundle"},
            "results_table_path": None,
            "results_csv_path": None,
            "plan_report_path": plan_report_path,
            "remote_status_report_path": remote_status_report_path,
            "errors": list(audit.get("errors") or []),
        }

    missing, same, conflicts = compare_manifest(landing, manifest)
    if dry_run:
        save = False

    to_fetch = list(missing)
    if overwrite:
        to_fetch += [{k: v for k, v in item.items() if k not in ("local_path", "local_sha256")}
                     for item in conflicts]

    fetched: List[Dict[str, Any]] = []
    errors: List[str] = []
    if to_fetch and not dry_run:
        fetched, errors = extract_bundle_items(bundle_path, to_fetch, landing)

    verified_paths = []
    verification_failed = []
    if not dry_run:
        for item in to_fetch:
            target = local_landing_path(landing, item["path"])
            if target.exists() and sha256_file(target) == item.get("sha256"):
                verified_paths.append(item["path"])
            else:
                verification_failed.append(item["path"])
    if verification_failed and not dry_run:
        errors.append(f"checksum failed for {len(verification_failed)} file(s)")

    missing_after, same_after, conflicts_after = compare_manifest(landing, manifest)
    collect = bundle_report_base(package, node_id, landing, peer, bundle_path, manifest)
    fetched_paths = {item.get("path") for item in fetched}
    missing_paths = {item.get("path") for item in missing}
    conflict_paths = {item.get("path") for item in conflicts}
    collect["mode"] = "import-bundle-dry-run" if dry_run else "import-bundle"
    collect["summary"].update({
        "already_current": len(same),
        "missing": len(missing),
        "conflicts": len(conflicts),
        "to_fetch": len(to_fetch),
        "missing_fetched": len([path for path in fetched_paths if path in missing_paths]),
        "fetched": len(fetched),
        "overwritten": len([path for path in fetched_paths if path in conflict_paths]) if overwrite else 0,
        "will_overwrite": len(conflicts) if overwrite else 0,
        "verified": len(verified_paths),
        "verification_failed": len(verification_failed),
    })
    collect["missing"] = [public_manifest_item(item) for item in missing]
    collect["conflicts"] = conflicts
    collect["fetched"] = fetched
    collect["verification_failed"] = verification_failed
    collect["errors"] = errors

    verify = bundle_report_base(package, node_id, landing, peer, bundle_path, manifest)
    remote_incomplete = int((verify.get("summary") or {}).get("remote_incomplete") or 0)
    verify["mode"] = "verify"
    verify["summary"].update({
        "verified_current": len(same_after),
        "missing": len(missing_after),
        "conflicts": len(conflicts_after),
        "status": "verified" if not missing_after and not conflicts_after and not remote_incomplete and not errors else "incomplete",
    })
    verify["missing"] = [public_manifest_item(item) for item in missing_after]
    verify["conflicts"] = conflicts_after
    verify["verified"] = [public_manifest_item(item) for item in same_after]
    verify["errors"] = errors

    remote_status = remote_status_from_package(
        package,
        node_id,
        peer,
        source="bundle",
        mode="import-bundle-status",
    )
    remote_status["known_peer"] = bool(peer)

    if save:
        write_sync_report("remote_status", node_id, remote_status)
        collect_index = update_artifact_index(
            node_id,
            landing,
            collect,
            list(same) + [item for item in to_fetch if item.get("path") in set(verified_paths)],
            "last_collect",
        )
        collect["artifact_index"] = rel(collect_index)
        write_sync_report("last_collect", node_id, collect)
        verify_index = update_artifact_index(node_id, landing, verify, same_after, "last_verify")
        verify["artifact_index"] = rel(verify_index)
        write_sync_report("last_verify", node_id, verify)

    plan_report_path = None
    remote_status_report_path = None
    if dry_run and save_plan:
        remote_status_report_path = write_sync_report("remote_status", node_id, remote_status).get("report_path")
        plan_report_path = write_sync_report("last_diff", node_id, collect).get("report_path")

    results_data = None
    result_table_paths = None
    results_reason = "disabled"
    if write_results:
        if dry_run:
            results_reason = "dry-run"
        elif not save:
            results_reason = "not-saved"
        elif errors or verify["summary"].get("status") != "verified":
            results_reason = "verification-not-clean"
        else:
            results_data = results_payload_from_index(
                node_ids=[node_id],
                include_incomplete=False,
            )
            result_table_paths = write_results_table_files(results_data)
            results_data["written"] = result_table_paths
            results_reason = "written"

    return {
        "generated_at": now_iso(),
        "mode": "import-bundle-dry-run" if dry_run else "import-bundle",
        "node_id": node_id,
        "known_peer": bool(peer),
        "saved": bool(save),
        "plan_saved": bool(plan_report_path),
        "dry_run": bool(dry_run),
        "landing": landing,
        "bundle_audit": audit,
        "remote_status": remote_status,
        "collect": collect,
        "verify": verify,
        "results": {
            "written": bool(result_table_paths),
            "reason": results_reason,
            "summary": (results_data or {}).get("summary"),
            "parse_errors": len((results_data or {}).get("parse_errors") or []),
            "errors": len((results_data or {}).get("errors") or []),
        },
        "results_table_path": result_table_paths.get("json") if result_table_paths else None,
        "results_csv_path": result_table_paths.get("csv") if result_table_paths else None,
        "plan_report_path": plan_report_path,
        "remote_status_report_path": remote_status_report_path,
        "errors": errors,
    }


def cmd_import_bundle(args: argparse.Namespace) -> int:
    if args.write_plan and not args.dry_run:
        raise SystemExit("--write-plan is only valid with --dry-run")
    if args.write_plan and args.no_save:
        raise SystemExit("--write-plan cannot be combined with --no-save")
    device, _warnings = load_device(args.config)
    package = load_bundle_package(args.bundle)
    node_id = node_id_from_publish(package, args.node_id)
    data = import_bundle_payload(
        device,
        package,
        node_id=node_id,
        overwrite=args.overwrite,
        save=(not args.no_save and not args.dry_run),
        dry_run=args.dry_run,
        write_results=args.results,
        save_plan=args.write_plan,
    )
    if args.json:
        print_json(data)
        return 0 if not data.get("errors") else 1

    collect_summary = (data.get("collect") or {}).get("summary") or {}
    verify_summary = (data.get("verify") or {}).get("summary") or {}
    print(f"syncmate import-bundle: {node_id}")
    print(f"  dry-run: {data.get('dry_run')}")
    if data.get("bundle_audit"):
        print(f"  bundle audit: {(data.get('bundle_audit') or {}).get('status')}")
    print(f"  known peer: {data.get('known_peer')}")
    print(f"  landing: {data.get('landing')}")
    print(
        f"  remote: files={collect_summary.get('remote_files', 0)} "
        f"leaves={collect_summary.get('remote_leaves', 0)} "
        f"incomplete={collect_summary.get('remote_incomplete', 0)}"
    )
    print(
        f"  fetched={collect_summary.get('fetched', 0)} "
        f"verified={collect_summary.get('verified', 0)} "
        f"conflicts={collect_summary.get('conflicts', 0)} "
        f"final_status={verify_summary.get('status')}"
    )
    results_info = data.get("results") or {}
    print(f"  results: written={results_info.get('written')} reason={results_info.get('reason')}")
    if data.get("results_table_path"):
        summary = results_info.get("summary") or {}
        print(f"  results table: {data.get('results_table_path')} rows={summary.get('rows', 0)}")
    if args.dry_run and data.get("plan_saved"):
        print(f"  reports: {data.get('remote_status_report_path')}, {data.get('plan_report_path')}")
    elif args.dry_run:
        print("  reports: not saved (--dry-run)")
    elif not args.no_save:
        print(f"  reports: .syncmate/last_collect_{node_id}.json, .syncmate/last_verify_{node_id}.json")
    else:
        print("  reports: not saved (--no-save)")
    for error in data.get("errors") or []:
        print(f"  error: {error}")
    return 0 if not data.get("errors") else 1


def cmd_fingerprint(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = fingerprint_payload(snapshot, include_timestamps=args.include_timestamps)
    matched = True
    if args.expect:
        expected = str(args.expect).strip()
        matched = bool(expected) and data["token"].startswith(expected)
        data["expect"] = expected
        data["matched"] = matched
    if args.json:
        print_json(data)
        return 0 if matched else 1

    print(f"syncmate fingerprint: {data['token']}")
    print(f"  device: {data['counts']['device']['id']} ({data['counts']['device']['role']})")
    print(f"  git: {data['counts']['git']['short_sha']} dirty={data['counts']['git']['dirty']}")
    print(
        f"  results: leaves={data['counts']['results']['leaves']} "
        f"nodes={data['counts']['results']['nodes']}"
    )
    print(
        f"  reports: remote={data['counts']['reports']['remote']} "
        f"diff={data['counts']['reports']['diff']} "
        f"collect={data['counts']['reports']['collect']} "
        f"verify={data['counts']['reports']['verify']}"
    )
    print(
        f"  artifact index: peers={data['counts']['artifact_index']['peers']} "
        f"indexed={data['counts']['artifact_index']['indexed']}"
    )
    print("  components:")
    for key, value in sorted(data["components"].items()):
        print(f"    {key}: {value}")
    if args.expect:
        print(f"  expect: {args.expect} matched={matched}")
    if not args.include_timestamps:
        print("  note: volatile timestamps/ages are excluded; use --include-timestamps for audit-exact tokens")
    return 0 if matched else 1


def cmd_compare(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    data = compare_fingerprint_payload(snapshot, args.node_ids)
    if args.json:
        print_json(data)
        return 0

    summary = data.get("summary") or {}
    local = data.get("local") or {}
    print(f"syncmate compare: peers={summary.get('peers', 0)} local={local.get('token')}")
    print(
        f"  same={summary.get('same', 0)} different={summary.get('different', 0)} "
        f"attention={summary.get('attention', 0)} missing={summary.get('missing', 0)} "
        f"errors={summary.get('errors', 0)}"
    )
    if not data.get("peers"):
        print("  no peers to compare; run add-peer or remote-status <node_id> --apply first")
        return 0
    for node_id, peer in sorted((data.get("peers") or {}).items()):
        print(
            f"  - {node_id}: {peer.get('status')} remote={peer.get('remote_token') or 'none'} "
            f"age={peer.get('remote_age') or 'unknown'} report={peer.get('remote_report')}"
        )
        if peer.get("different_components"):
            print(f"      different: {', '.join(peer['different_components'])}")
        if peer.get("attention_components"):
            print(f"      attention: {', '.join(peer['attention_components'])}")
        if peer.get("errors"):
            for error in peer["errors"][:args.limit]:
                print(f"      error: {error}")
        elif peer.get("action"):
            print(f"      next: {peer.get('action')}")
        components = peer.get("components") or {}
        for key, item in list(sorted(components.items()))[:max(0, args.limit)]:
            mark = "==" if item.get("match") else "!="
            print(f"      {key}: {mark} local={item.get('local')} remote={item.get('remote')}")
    return 0


def cmd_progress(args: argparse.Namespace) -> int:
    data = scan_progress(limit=args.limit, scan_limit=args.scan_limit)
    if args.json:
        print_json(data)
        return 0
    summary = data["summary"]
    print(f"syncmate progress: logs under {data['root']}")
    if not data["exists"]:
        print("  no log directory yet")
        return 0
    print(
        f"  total={summary['total_log_files']} scanned={summary['scanned_log_files']} "
        f"errors={summary['error_logs']} newest={summary['newest_age']}"
    )
    if data["error_logs"]:
        print("  error-like recent logs:")
        for item in data["error_logs"]:
            keywords = ",".join(item.get("keywords") or [])
            print(f"    - {item['path']} age={item['age']} keywords={keywords}")
            if item.get("last_line"):
                print(f"      last: {item['last_line']}")
    if data["recent_logs"]:
        print("  recent logs:")
        for item in data["recent_logs"]:
            print(f"    - {item['path']} age={item['age']} status={item['status']} size={item['size']}")
            if item.get("last_line"):
                print(f"      last: {item['last_line']}")
    return 0


def format_history_delta(delta: Dict[str, Any]) -> str:
    if not delta:
        return "baseline"
    return " ".join(f"{key}={value:+d}" for key, value in sorted(delta.items()))


def cmd_history(args: argparse.Namespace) -> int:
    entries = read_history(limit=args.limit)
    data = {
        "generated_at": now_iso(),
        "mode": "history",
        "history_path": rel(history_file()),
        "limit": args.limit,
        "entries": entries,
    }
    if args.json:
        print_json(data)
        return 0
    print(f"syncmate history: {data['history_path']}")
    if not entries:
        print("  no history yet")
        print("  next: run status, refresh, or dashboard without --no-write-state")
        return 0
    for item in entries:
        results = item.get("results") or {}
        progress = item.get("progress") or {}
        reports = item.get("reports") or {}
        index = item.get("artifact_index") or {}
        print(
            f"  - {item.get('generated_at')} event={item.get('event')} "
            f"leaves={results.get('leaves', 0)} indexed={index.get('indexed', 0)} "
            f"log_errors={progress.get('log_errors', 0)} "
            f"reports={reports.get('remote', 0)}/{reports.get('diff', 0)}/{reports.get('collect', 0)}/{reports.get('verify', 0)} "
            f"delta=[{format_history_delta(item.get('delta') or {})}]"
        )
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    index = load_artifact_index()
    if args.check:
        result = check_artifact_index(index)
        failed = result["summary"]["status"] != "ok"
        if args.json:
            print_json(result)
            return 1 if failed else 0

        summary = result["summary"]
        print(f"syncmate artifact index check: {summary['status']}")
        print(f"  path: {result.get('index_path')}")
        print(
            f"  checked: {summary['checked']}/{summary['indexed']} "
            f"ok={summary['ok']} missing={summary['missing']} "
            f"mismatched={summary['mismatched']} unsafe={summary['unsafe']} errors={summary['errors']}"
        )
        for item in result["missing"][:5]:
            print(f"  missing: {item.get('local_path')} <- {item.get('remote_path')}")
        for item in result["mismatched"][:5]:
            print(f"  mismatch: {item.get('local_path')} expected={item.get('expected_sha256')} actual={item.get('actual_sha256')}")
        for item in result["unsafe"][:5]:
            print(f"  unsafe: {item.get('local_path')} ({item.get('reason')})")
        for error in result["errors"][:5]:
            print(f"  error: {error}")
        return 1 if failed else 0

    if args.json:
        print_json(index)
        return 0 if not index.get("errors") else 1

    print(f"syncmate artifact index: {artifact_index_total(index)} verified artifact(s)")
    print(f"  path: {index.get('index_path')}")
    print(f"  updated: {index.get('updated_at') or 'never'}")
    if index.get("errors"):
        for error in index["errors"]:
            print(f"  error: {error}")
        return 1

    peers = index.get("peers") or {}
    if not peers:
        print("  no indexed artifacts yet")
        print("  next: run collect <node_id> --apply, then verify <node_id> --apply")
        return 0

    for node, entry in sorted(peers.items()):
        summary = entry.get("summary") or {}
        print(
            f"  - {node}: indexed={summary.get('indexed', len(entry.get('items') or []))} "
            f"status={summary.get('status', 'unknown')} landing={entry.get('landing')}"
        )
        print(f"       source: {entry.get('source_report')}")
    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    if args.json and args.csv:
        raise SystemExit("--json and --csv are mutually exclusive")
    data = inventory_from_index(
        load_artifact_index(),
        node_ids=args.node_ids,
        only_incomplete=args.only_incomplete,
    )
    if args.json:
        print_json(data)
        return 0 if not data.get("errors") else 1
    if args.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=INVENTORY_CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(inventory_csv_rows(data))
        return 0 if not data.get("errors") else 1

    summary = data["summary"]
    print(
        f"syncmate inventory: peers={summary['peers']} leaves={summary['leaves']} "
        f"complete={summary['complete']} incomplete={summary['incomplete']}"
    )
    if data.get("errors"):
        for error in data["errors"]:
            print(f"  error: {error}")
        return 1
    if not data["peers"]:
        print("  no indexed artifacts yet")
        return 0
    for node_id, peer in sorted(data["peers"].items()):
        ps = peer["summary"]
        print(
            f"  - {node_id}: leaves={ps['leaves']} complete={ps['complete']} "
            f"incomplete={ps['incomplete']} artifacts={ps['artifacts']}"
        )
        for leaf in peer["leaves"][:args.limit]:
            missing = ",".join(leaf["missing"]) if leaf["missing"] else "none"
            state = "ok" if leaf["complete"] else "missing"
            print(
                f"      {state}: {leaf['cell']}/{leaf['method_strategy']}/{leaf['seed']} "
                f"artifacts={','.join(leaf['artifacts']) or 'none'} missing={missing}"
            )
        if len(peer["leaves"]) > args.limit:
            print(f"      ... {len(peer['leaves']) - args.limit} more leaf/leaves")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    if args.json and args.csv:
        raise SystemExit("--json and --csv are mutually exclusive")
    index = load_artifact_index()
    data = export_payload_from_index(
        index,
        node_ids=args.node_ids,
        include_incomplete=args.include_incomplete,
    )
    index_check = None
    failed = bool(data.get("errors"))
    if args.check:
        index_check = check_artifact_index(index)
        data["index_check"] = {
            "status": (index_check.get("summary") or {}).get("status"),
            "missing": (index_check.get("summary") or {}).get("missing"),
            "mismatched": (index_check.get("summary") or {}).get("mismatched"),
            "unsafe": (index_check.get("summary") or {}).get("unsafe"),
            "errors": (index_check.get("summary") or {}).get("errors"),
        }
        failed = failed or data["index_check"]["status"] != "ok"

    written = None
    if args.write:
        written = write_export_files(data)
        data["written"] = written

    if args.json:
        print_json(data)
        return 1 if failed else 0
    if args.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=EXPORT_CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(export_csv_rows(data))
        return 1 if failed else 0

    summary = data["summary"]
    print(
        f"syncmate export: leaves={summary['leaves']} artifacts={summary['artifacts']} "
        f"complete={summary['complete_leaves']} incomplete={summary['incomplete_leaves']} "
        f"skipped_incomplete={summary['skipped_incomplete']}"
    )
    print(f"  source: {data['index_path']}")
    if written:
        print(f"  manifest: {written['manifest']}")
        print(f"  csv: {written['csv']}")
    if index_check:
        check_summary = index_check.get("summary") or {}
        print(
            f"  check: {check_summary.get('status')} missing={check_summary.get('missing')} "
            f"mismatched={check_summary.get('mismatched')} unsafe={check_summary.get('unsafe')}"
        )
    if data.get("errors"):
        for error in data["errors"]:
            print(f"  error: {error}")
    if not data["leaves"]:
        print("  no trusted export leaves; run sync <node_id> or verify <node_id> --apply first")
    else:
        for leaf in data["leaves"][:args.limit]:
            artifacts = ",".join(sorted((leaf.get("artifacts") or {}).keys()))
            state = "complete" if leaf.get("complete") else "incomplete"
            print(
                f"  - {leaf['node_id']}: {leaf['cell']}/{leaf['method_strategy']}/{leaf['seed']} "
                f"{state} artifacts={artifacts or 'none'}"
            )
        if len(data["leaves"]) > args.limit:
            print(f"  ... {len(data['leaves']) - args.limit} more leaf/leaves")
    return 1 if failed else 0


def cmd_results(args: argparse.Namespace) -> int:
    if args.json and args.csv:
        raise SystemExit("--json and --csv are mutually exclusive")
    index = load_artifact_index()
    data = results_payload_from_index(
        index,
        node_ids=args.node_ids,
        include_incomplete=args.include_incomplete,
    )
    failed = bool(data.get("errors") or data.get("parse_errors"))
    index_check = None
    if args.check:
        index_check = check_artifact_index(index)
        summary = index_check.get("summary") or {}
        data["index_check"] = {
            "status": summary.get("status"),
            "missing": summary.get("missing"),
            "mismatched": summary.get("mismatched"),
            "unsafe": summary.get("unsafe"),
            "errors": summary.get("errors"),
        }
        failed = failed or summary.get("status") != "ok"

    written = None
    if args.write:
        written = write_results_table_files(data)
        data["written"] = written

    if args.json:
        print_json(data)
        return 1 if failed else 0
    if args.csv:
        writer = csv.DictWriter(sys.stdout, fieldnames=RESULTS_CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results_csv_rows(data))
        return 1 if failed else 0

    summary = data["summary"]
    print(
        f"syncmate results: rows={summary['rows']} leaves={summary['leaves']} "
        f"complete={summary['complete_leaves']} incomplete={summary['incomplete_leaves']} "
        f"parse_errors={summary['parse_errors']}"
    )
    print(f"  source: {data['index_path']}")
    if written:
        print(f"  json: {written['json']}")
        print(f"  csv: {written['csv']}")
    if index_check:
        check_summary = index_check.get("summary") or {}
        print(
            f"  check: {check_summary.get('status')} missing={check_summary.get('missing')} "
            f"mismatched={check_summary.get('mismatched')} unsafe={check_summary.get('unsafe')}"
        )
    if data.get("errors"):
        for error in data["errors"]:
            print(f"  error: {error}")
    if data.get("parse_errors"):
        for item in data["parse_errors"][:args.limit]:
            print(f"  parse: {item.get('local_leaf')} [{item.get('strategy')}]: {item.get('error')}")
        if len(data["parse_errors"]) > args.limit:
            print(f"  ... {len(data['parse_errors']) - args.limit} more parse error(s)")
    if not data["rows"]:
        print("  no trusted result rows; run sync <node_id> or verify <node_id> --apply first")
    else:
        for row in data["rows"][:args.limit]:
            print(
                f"  - {row['node_id']}: {row['cell']}/{row['method']}_{row['strategy_full']}/{row['seed']} "
                f"f1_after={row.get('f1_after')} f1_drop={row.get('f1_drop')} "
                f"mia_auc={row.get('mia_auc')} gap={row.get('gap')} status={row.get('status')}"
            )
        if len(data["rows"]) > args.limit:
            print(f"  ... {len(data['rows']) - args.limit} more row(s)")
    return 1 if failed else 0


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def render_status_html(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]],
                       workflow_data: Optional[Dict[str, Any]] = None,
                       automation_core_data: Optional[Dict[str, Any]] = None,
                       acceptance_data: Optional[Dict[str, Any]] = None) -> str:
    device = snapshot["device"]
    git = snapshot["git"]
    results = snapshot["results"]
    progress = snapshot.get("progress") or {}
    progress_summary = progress.get("summary") or {}
    remote_status = snapshot.get("remote_status") or {}
    diff_reports = snapshot.get("diff_reports") or {}
    collect_reports = snapshot.get("collect_reports") or {}
    verify_reports = snapshot.get("verify_reports") or {}
    artifact_index = snapshot.get("artifact_index") or {}
    index_peers = artifact_index.get("peers") or {}
    indexed_total = artifact_index_total(artifact_index)
    fingerprint = snapshot.get("fingerprint") or {}
    compare = compare_fingerprint_payload(snapshot)
    compare_summary = compare.get("summary") or {}
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    results_table_summary = results_table.get("summary") or {}
    results_table_errors = results_table.get("errors") or []
    results_table_parse_errors = results_table.get("parse_errors") or []
    preflight = snapshot.get("preflight") if isinstance(snapshot.get("preflight"), dict) else {}
    preflight_summary = preflight.get("summary") or {}
    preflight_errors = preflight_summary.get("errors", len(preflight.get("errors") or [])) if preflight else 0
    preflight_warnings = preflight_summary.get("warnings", 0) if preflight else 0
    preflight_status = preflight.get("status") if preflight else "missing"
    state = status_label(snapshot, diagnostics)
    layout = layout_payload_from_snapshot(snapshot)
    workflow = workflow_data or workflow_payload(
        snapshot,
        diagnostics,
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=8,
    )
    workflow_summary = workflow.get("summary") or {}
    automation_core = automation_core_data or automation_core_payload_from_snapshot(snapshot, limit=8)
    automation_totals = automation_core.get("totals") or {}
    automation_results = automation_core.get("results") or {}
    automation_delta = automation_results.get("delta")
    acceptance = acceptance_data or acceptance_payload(
        snapshot,
        diagnostics,
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=8,
    )
    acceptance_core = acceptance.get("automation_core") or {}
    acceptance_totals = acceptance_core.get("totals") or {}
    acceptance_results = acceptance_core.get("results") or {}
    acceptance_gate = acceptance.get("gate") or {}
    if automation_delta is None:
        automation_delta_text = "unavailable"
    else:
        automation_delta_text = (
            f"added {automation_delta.get('added_rows', 0)}, "
            f"changed {automation_delta.get('changed_rows', 0)}, "
            f"removed {automation_delta.get('removed_rows', 0)}"
        )
    automation_summary_rows = [
        "<tr>"
        f"<td class='status {esc(automation_core.get('status'))}'>{esc(automation_core.get('status'))}</td>"
        f"<td class='num'>{automation_totals.get('missing', 0)}</td>"
        f"<td class='num'>{automation_totals.get('fetched_missing', 0)}</td>"
        f"<td class='num'>{automation_totals.get('checksum_verified', 0)}</td>"
        f"<td class='num'>{automation_totals.get('checksum_failed', 0)}</td>"
        f"<td class='num'>{automation_totals.get('verify_missing', 0)}</td>"
        f"<td class='num'>{automation_totals.get('indexed', 0)}</td>"
        f"<td class='num'>{automation_results.get('rows', 0)}</td>"
        f"<td>{esc(automation_results.get('status'))}</td>"
        f"<td>{esc(automation_delta_text)}</td>"
        f"<td class='mono'>{esc((automation_core.get('files') or {}).get('artifact_index'))}</td>"
        f"<td class='mono'>{esc((automation_core.get('files') or {}).get('results_csv'))}</td>"
        "</tr>"
    ]
    automation_peer_rows = []
    for node_id, peer in sorted((automation_core.get("peers") or {}).items()):
        counts = peer.get("counts") or {}
        automation_peer_rows.append(
            "<tr>"
            f"<td>{esc(node_id)}</td>"
            f"<td class='mono'>{esc(peer.get('landing'))}</td>"
            f"<td class='num'>{counts.get('missing', 0)}</td>"
            f"<td class='num'>{counts.get('fetched_missing', 0)}</td>"
            f"<td class='num'>{counts.get('checksum_verified', 0)}</td>"
            f"<td class='num'>{counts.get('checksum_failed', 0)}</td>"
            f"<td class='num'>{counts.get('verify_missing', 0)}</td>"
            f"<td class='num'>{counts.get('indexed', 0)}</td>"
            f"<td>{esc(peer.get('verify_status'))}</td>"
            f"<td class='mono'>{esc(peer.get('artifact_index'))}</td>"
            "</tr>"
        )
    if not automation_peer_rows:
        automation_peer_rows.append(
            "<tr><td colspan='10' class='muted'>No saved automation evidence yet. "
            "Run sync &lt;node_id&gt; or collect/verify/results first.</td></tr>"
        )
    operation_rows = [
        (
            "global",
            "device runbook",
            "python scripts/syncmate/syncmate.py runbook --write",
            rel(runbook_file()),
        ),
        (
            "global",
            "operation checklist",
            "python scripts/syncmate/syncmate.py checklist --write",
            rel(checklist_file()),
        ),
        (
            "global",
            "landing inbox",
            "python scripts/syncmate/syncmate.py landings",
            "results/runs/<node_id>/",
        ),
        (
            "global",
            "trusted trace",
            "python scripts/syncmate/syncmate.py trace --check",
            rel(artifact_index_file()),
        ),
        (
            "global",
            "lifecycle phase",
            "python scripts/syncmate/syncmate.py lifecycle --json",
            rel(action_plan_file()),
        ),
        (
            "global",
            "core receipt",
            "python scripts/syncmate/syncmate.py automation-core --write",
            rel(automation_core_markdown_file()),
        ),
        (
            "global",
            "refresh dashboard",
            "python scripts/syncmate/syncmate.py dashboard",
            rel(STATUS_HTML),
        ),
        (
            "global",
            "write action plan",
            "python scripts/syncmate/syncmate.py next --write --require-preflight --require-verify --require-results",
            rel(action_plan_file()),
        ),
        (
            "global",
            "local rehearsal",
            "python scripts/syncmate/syncmate.py smoke",
            "temporary workspace",
        ),
        (
            "global",
            "evidence handoff pack",
            "python scripts/syncmate/syncmate.py handoff-pack",
            rel(handoff_pack_file()),
        ),
        (
            "global",
            "audit handoff pack",
            "python scripts/syncmate/syncmate.py inspect-handoff-pack <handoff_pack.zip> --write",
            ".syncmate/last_handoff_pack_inspect_<node_id>.json",
        ),
    ]
    for node_id in sorted((layout.get("peers") or {}).keys()):
        operation_rows.extend([
            (
                node_id,
                "full sync",
                f"python scripts/syncmate/syncmate.py sync {node_id}",
                rel(checklist_file()),
            ),
            (
                node_id,
                "inspect landing",
                f"python scripts/syncmate/syncmate.py landings {node_id}",
                f"results/runs/{node_id}/",
            ),
            (
                node_id,
                "trace checksums",
                f"python scripts/syncmate/syncmate.py trace {node_id} --check",
                rel(artifact_index_file()),
            ),
            (
                node_id,
                "write checklist",
                f"python scripts/syncmate/syncmate.py checklist {node_id} --write",
                rel(checklist_file()),
            ),
            (
                node_id,
                "peer handoff",
                f"python scripts/syncmate/syncmate.py handoff {node_id} --write",
                f".syncmate/handoff_{safe_file_stem(node_id)}.md",
            ),
        ])
    operation_entry_rows = [
        "<tr>"
        f"<td>{esc(scope)}</td>"
        f"<td>{esc(purpose)}</td>"
        f"<td class='mono'>{esc(command)}</td>"
        f"<td class='mono'>{esc(evidence)}</td>"
        "</tr>"
        for scope, purpose, command, evidence in operation_rows
    ]
    acceptance_rows = [
        "<tr>"
        f"<td class='status {esc(acceptance.get('status'))}'>{esc(acceptance.get('status'))}</td>"
        f"<td>{esc(acceptance.get('ready'))}</td>"
        f"<td>{esc('pass' if acceptance_gate.get('passed') else 'fail')}</td>"
        f"<td class='num'>{acceptance_gate.get('failure_count', 0)}</td>"
        f"<td>{esc((acceptance.get('workflow') or {}).get('status'))}</td>"
        f"<td>{esc(acceptance_core.get('status'))}</td>"
        f"<td class='num'>{acceptance_totals.get('missing', 0)}</td>"
        f"<td class='num'>{acceptance_totals.get('fetched_missing', 0)}</td>"
        f"<td class='num'>{acceptance_totals.get('checksum_verified', 0)}</td>"
        f"<td class='num'>{acceptance_totals.get('checksum_failed', 0)}</td>"
        f"<td class='num'>{acceptance_totals.get('indexed', 0)}</td>"
        f"<td class='num'>{acceptance_results.get('rows', 0)}</td>"
        f"<td class='mono'>{esc(acceptance.get('acceptance_path'))}</td>"
        "</tr>"
    ]
    workflow_rows = []
    workflow_path = workflow.get("workflow_path") or rel(workflow_file())
    for stage in workflow.get("global_stages") or []:
        status = stage.get("status")
        workflow_rows.append(
            "<tr>"
            "<td>global</td>"
            f"<td>{esc(stage.get('id'))}</td>"
            f"<td class='status {esc(status)}'>{esc(status)}</td>"
            f"<td>{esc(stage.get('reason'))}</td>"
            f"<td class='mono'>{esc(stage.get('command'))}</td>"
            "</tr>"
        )
    for node_id, peer in sorted((workflow.get("peers") or {}).items()):
        for stage in peer.get("stages") or []:
            status = stage.get("status")
            workflow_rows.append(
                "<tr>"
                f"<td>{esc(node_id)}</td>"
                f"<td>{esc(stage.get('id'))}</td>"
                f"<td class='status {esc(status)}'>{esc(status)}</td>"
                f"<td>{esc(stage.get('reason'))}</td>"
                f"<td class='mono'>{esc(stage.get('command'))}</td>"
                "</tr>"
            )
    if not workflow_rows:
        workflow_rows.append(
            "<tr><td colspan='5' class='muted'>No workflow stages yet. Configure peers, then run workflow --write.</td></tr>"
        )
    workflow_next = workflow.get("next") or {}
    next_command_rows = []
    for idx, item in enumerate(workflow_next.get("commands") or [], start=1):
        evidence = item.get("evidence") or {}
        writes = evidence.get("writes") or []
        inspects = evidence.get("inspects") or []
        evidence_text = "; ".join(
            part for part in [
                f"writes: {', '.join(writes)}" if writes else "",
                f"inspects: {', '.join(inspects)}" if inspects else "",
            ] if part
        )
        next_command_rows.append(
            "<tr>"
            f"<td class='num'>{idx}</td>"
            f"<td>{esc(item.get('kind'))}</td>"
            f"<td>{esc(item.get('node_id') or '')}</td>"
            f"<td>{esc(item.get('reason'))}</td>"
            f"<td class='mono'>{esc(evidence_text)}</td>"
            f"<td class='mono'>{esc(item.get('command'))}</td>"
            "</tr>"
        )
    if not next_command_rows:
        next_command_rows.append(
            "<tr><td colspan='6' class='muted'>No executable next commands suggested.</td></tr>"
        )
    manual_action_rows = []
    for idx, item in enumerate(workflow_next.get("manual_actions") or [], start=1):
        manual_action_rows.append(
            "<tr>"
            f"<td class='num'>{idx}</td>"
            f"<td>{esc(item.get('kind'))}</td>"
            f"<td>{esc(item.get('node_id') or '')}</td>"
            f"<td>{esc(item.get('reason'))}</td>"
            f"<td class='mono'>{esc(item.get('action'))}</td>"
            "</tr>"
        )
    if not manual_action_rows:
        manual_action_rows.append(
            "<tr><td colspan='5' class='muted'>No manual actions suggested.</td></tr>"
        )
    bundle_inspect_reports = snapshot.get("bundle_inspect_reports") or {}
    layout_rows = []
    for node_id, peer in sorted((layout.get("peers") or {}).items()):
        trusted = peer.get("trusted") or {}
        example = peer.get("example_mapping") or {}
        roots = ", ".join(peer.get("remote_result_roots") or [])
        artifacts = ", ".join((peer.get("artifact_policy") or {}).get("include") or [])
        layout_rows.append(
            "<tr>"
            f"<td>{esc(node_id)}</td>"
            f"<td>{esc(peer.get('transport'))}</td>"
            f"<td class='mono'>{esc(peer.get('repo_path'))}</td>"
            f"<td class='mono'>{esc(roots)}</td>"
            f"<td class='mono'>{esc(peer.get('local_landing'))}</td>"
            f"<td>{esc(artifacts)}</td>"
            f"<td class='mono'>{esc(example.get('remote'))}<br><span class='muted'>-&gt; {esc(example.get('local') or 'blocked')}</span></td>"
            f"<td class='num'>{trusted.get('indexed_artifacts', 0)}</td>"
            f"<td class='num'>{trusted.get('result_rows', 0)}</td>"
            f"<td class='mono'>{esc((peer.get('commands') or {}).get('sync'))}</td>"
            "</tr>"
        )
    if not layout_rows:
        layout_rows.append(
            "<tr><td colspan='10' class='muted'>No configured peers. Run setup-plan or add-peer first.</td></tr>"
        )
    node_rows = []
    for node, info in sorted((results.get("nodes") or {}).items()):
        files = ", ".join(f"{k} {v}" for k, v in sorted((info.get("files") or {}).items()))
        layouts = ", ".join(f"{k} {v}" for k, v in sorted((info.get("layouts") or {}).items()))
        issues = ", ".join(info.get("issues") or ["ok"])
        node_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td class='num'>{info.get('leaves', 0)}</td>"
            f"<td>{esc(files)}</td>"
            f"<td>{esc(layouts)}</td>"
            f"<td>{esc(issues)}</td>"
            "</tr>"
        )
    if not node_rows:
        node_rows.append("<tr><td colspan='5' class='muted'>No result artifacts found.</td></tr>")

    diag_rows = []
    for item in diagnostics:
        diag_rows.append(
            f"<div class='diag {esc(item['severity'])}'>"
            f"<b>{esc(item['severity'].upper())}</b>"
            f"<span>{esc(item['code'])}</span>"
            f"<p>{esc(item['message'])}</p>"
            f"<code>{esc(item['action'])}</code>"
            "</div>"
        )
    if not diag_rows:
        diag_rows.append("<div class='diag ok'><b>OK</b><span>ready</span><p>No diagnostics.</p><code>Continue.</code></div>")

    remote_rows = []
    for node, report in sorted(remote_status.items()):
        summary = report.get("summary") or {}
        errors = report.get("errors") or []
        remote_nodes = ", ".join(summary.get("result_nodes") or [])
        status_text = "error" if errors else "ok"
        remote_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(report.get('generated_at')))}</td>"
            f"<td>{esc(report.get('generated_at'))}</td>"
            f"<td>{esc(summary.get('device_id'))}</td>"
            f"<td>{esc(summary.get('role'))}</td>"
            f"<td class='mono'>{esc(summary.get('git_short_sha'))}</td>"
            f"<td>{esc(summary.get('git_dirty'))}</td>"
            f"<td class='num'>{summary.get('result_leaves', 0)}</td>"
            f"<td>{esc(remote_nodes or 'none')}</td>"
            f"<td>{esc(status_text)}</td>"
            f"<td class='mono'>{esc(report.get('report_path'))}</td>"
            "</tr>"
        )
    if not remote_rows:
        remote_rows.append(
            "<tr><td colspan='11' class='muted'>No saved remote snapshots. "
            "Run remote-status &lt;node_id&gt; --apply from the collector.</td></tr>"
        )

    bundle_rows = []
    for node, report in sorted(bundle_inspect_reports.items()):
        manifest = report.get("manifest") or {}
        inventory = manifest.get("inventory_summary") or {}
        audit = report.get("audit") or {}
        errors = report.get("errors") or audit.get("errors") or []
        warnings = audit.get("warnings") or []
        status_text = "error" if errors or audit.get("status") == "invalid" else "warn" if warnings else audit.get("status")
        bundle_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(report.get('generated_at')))}</td>"
            f"<td>{esc(report.get('generated_at'))}</td>"
            f"<td>{esc(status_text)}</td>"
            f"<td class='mono'>{esc((report.get('git') or {}).get('short_sha'))}</td>"
            f"<td class='mono'>{esc(((report.get('fingerprint') or {}).get('token')))}</td>"
            f"<td class='num'>{manifest.get('count', 0)}</td>"
            f"<td class='num'>{inventory.get('leaves', 0)}</td>"
            f"<td class='num'>{inventory.get('incomplete', 0)}</td>"
            f"<td class='num'>{len(warnings)}</td>"
            f"<td class='num'>{len(errors)}</td>"
            f"<td class='mono'>{esc(report.get('bundle_path'))}</td>"
            f"<td class='mono'>{esc(report.get('report_path'))}</td>"
            "</tr>"
        )
    if not bundle_rows:
        bundle_rows.append(
            "<tr><td colspan='13' class='muted'>No saved bundle inspections. "
            "Run inspect-bundle &lt;bundle.zip&gt; --write before importing copied bundles.</td></tr>"
        )

    compare_rows = []
    for node, peer in sorted((compare.get("peers") or {}).items()):
        different = ", ".join(peer.get("different_components") or []) or "none"
        attention = ", ".join(peer.get("attention_components") or []) or "none"
        compare_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(peer.get('status'))}</td>"
            f"<td>{esc(peer.get('remote_age') or 'unknown')}</td>"
            f"<td class='mono'>{esc((compare.get('local') or {}).get('token'))}</td>"
            f"<td class='mono'>{esc(peer.get('remote_token'))}</td>"
            f"<td class='num'>{peer.get('matched_components', 0)}</td>"
            f"<td>{esc(different)}</td>"
            f"<td>{esc(attention)}</td>"
            f"<td class='mono'>{esc(peer.get('remote_report'))}</td>"
            "</tr>"
        )
    if not compare_rows:
        compare_rows.append(
            "<tr><td colspan='9' class='muted'>No saved peer fingerprints. "
            "Run remote-status &lt;node_id&gt; --apply, then compare.</td></tr>"
        )

    result_table_rows = []
    result_table_status = "missing"
    if isinstance(results_table, dict) and results_table:
        if results_table_errors:
            result_table_status = "error"
        elif results_table_parse_errors:
            result_table_status = "parse-warn"
        else:
            result_table_status = "ok"
        result_table_rows.append(
            "<tr>"
            f"<td>{esc(result_table_status)}</td>"
            f"<td>{esc(results_table.get('generated_at'))}</td>"
            f"<td class='num'>{results_table_summary.get('rows', 0)}</td>"
            f"<td class='num'>{results_table_summary.get('leaves', 0)}</td>"
            f"<td class='num'>{results_table_summary.get('complete_leaves', 0)}</td>"
            f"<td class='num'>{results_table_summary.get('parse_errors', len(results_table_parse_errors))}</td>"
            f"<td class='mono'>{esc(((results_table.get('files') or {}).get('json')) or rel(results_table_file()))}</td>"
            f"<td class='mono'>{esc(((results_table.get('files') or {}).get('csv')) or rel(results_csv_file()))}</td>"
            "</tr>"
        )
    else:
        result_table_rows.append(
            "<tr><td colspan='8' class='muted'>No trusted results table yet. "
            "Run results --write --check or sync without --no-results.</td></tr>"
        )

    preflight_rows = []
    if preflight:
        if preflight.get("errors") and not preflight.get("summary"):
            preflight_status = "error"
        preflight_rows.append(
            "<tr>"
            f"<td>{esc(preflight_status)}</td>"
            f"<td>{esc(format_age(preflight.get('generated_at')))}</td>"
            f"<td>{esc(preflight.get('generated_at'))}</td>"
            f"<td class='num'>{preflight_summary.get('peers', 0)}</td>"
            f"<td class='num'>{preflight_summary.get('ready', 0)}</td>"
            f"<td class='num'>{preflight_summary.get('blocked', 0)}</td>"
            f"<td class='num'>{preflight_errors}</td>"
            f"<td class='num'>{preflight_warnings}</td>"
            f"<td class='mono'>{esc(preflight.get('report_path') or rel(last_preflight_file()))}</td>"
            "</tr>"
        )
    else:
        preflight_rows.append(
            "<tr><td colspan='9' class='muted'>No saved preflight report yet. "
            "Run preflight --write before or after setup changes.</td></tr>"
        )

    collect_rows = []
    for node, report in sorted(collect_reports.items()):
        summary = report.get("summary") or {}
        errors = report.get("errors") or []
        conflict_count = len(report.get("conflicts") or [])
        failed_count = len(report.get("verification_failed") or [])
        remote_incomplete = int(summary.get("remote_incomplete") or 0)
        status_text = "error" if errors or failed_count else "incomplete" if remote_incomplete else "conflict" if conflict_count else "ok"
        collect_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(report.get('generated_at')))}</td>"
            f"<td>{esc(report.get('generated_at'))}</td>"
            f"<td>{esc(report.get('landing'))}</td>"
            f"<td class='num'>{summary.get('remote_files', 0)}</td>"
            f"<td class='num'>{summary.get('remote_leaves', 0)}</td>"
            f"<td class='num'>{remote_incomplete}</td>"
            f"<td class='num'>{summary.get('already_current', 0)}</td>"
            f"<td class='num'>{summary.get('missing_fetched', 0)}</td>"
            f"<td class='num'>{conflict_count}</td>"
            f"<td class='num'>{summary.get('verified', 0)}</td>"
            f"<td class='num'>{failed_count}</td>"
            f"<td>{esc(status_text)}</td>"
            f"<td class='mono'>{esc(report.get('report_path'))}</td>"
            "</tr>"
        )
    if not collect_rows:
        collect_rows.append(
            "<tr><td colspan='14' class='muted'>No saved collection reports. "
            "Run collect &lt;node_id&gt; --apply from the collector.</td></tr>"
        )

    diff_rows = []
    for node, report in sorted(diff_reports.items()):
        summary = report.get("summary") or {}
        errors = report.get("errors") or []
        missing_count = summary.get("missing", len(report.get("missing") or []))
        conflict_count = summary.get("conflicts", len(report.get("conflicts") or []))
        remote_incomplete = int(summary.get("remote_incomplete") or 0)
        status_text = "error" if errors else "incomplete" if remote_incomplete else "conflict" if conflict_count else "new" if missing_count else "current"
        diff_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(report.get('generated_at')))}</td>"
            f"<td>{esc(report.get('generated_at'))}</td>"
            f"<td>{esc(report.get('landing'))}</td>"
            f"<td class='num'>{summary.get('remote_files', 0)}</td>"
            f"<td class='num'>{summary.get('remote_leaves', 0)}</td>"
            f"<td class='num'>{remote_incomplete}</td>"
            f"<td class='num'>{summary.get('already_current', 0)}</td>"
            f"<td class='num'>{missing_count}</td>"
            f"<td class='num'>{conflict_count}</td>"
            f"<td class='num'>{summary.get('to_fetch', missing_count)}</td>"
            f"<td>{esc(status_text)}</td>"
            f"<td class='mono'>{esc(report.get('report_path'))}</td>"
            "</tr>"
        )
    if not diff_rows:
        diff_rows.append(
            "<tr><td colspan='13' class='muted'>No saved diff reports. "
            "Run collect &lt;node_id&gt; --diff from the collector.</td></tr>"
        )

    verify_rows = []
    for node, report in sorted(verify_reports.items()):
        summary = report.get("summary") or {}
        errors = report.get("errors") or []
        missing_count = summary.get("missing", len(report.get("missing") or []))
        conflict_count = summary.get("conflicts", len(report.get("conflicts") or []))
        remote_incomplete = int(summary.get("remote_incomplete") or 0)
        status_text = "error" if errors else "fail" if missing_count or conflict_count or remote_incomplete else "verified"
        verify_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(report.get('generated_at')))}</td>"
            f"<td>{esc(report.get('generated_at'))}</td>"
            f"<td>{esc(report.get('landing'))}</td>"
            f"<td class='num'>{summary.get('remote_files', 0)}</td>"
            f"<td class='num'>{summary.get('remote_leaves', 0)}</td>"
            f"<td class='num'>{remote_incomplete}</td>"
            f"<td class='num'>{summary.get('verified_current', summary.get('already_current', 0))}</td>"
            f"<td class='num'>{missing_count}</td>"
            f"<td class='num'>{conflict_count}</td>"
            f"<td>{esc(status_text)}</td>"
            f"<td class='mono'>{esc(report.get('report_path'))}</td>"
            "</tr>"
        )
    if not verify_rows:
        verify_rows.append(
            "<tr><td colspan='12' class='muted'>No saved verification reports. "
            "Run verify &lt;node_id&gt; --apply from the collector.</td></tr>"
        )

    index_rows = []
    for node, entry in sorted(index_peers.items()):
        summary = entry.get("summary") or {}
        index_rows.append(
            "<tr>"
            f"<td>{esc(node)}</td>"
            f"<td>{esc(format_age(entry.get('updated_at')))}</td>"
            f"<td>{esc(entry.get('updated_at'))}</td>"
            f"<td>{esc(entry.get('landing'))}</td>"
            f"<td class='num'>{summary.get('remote_files', 0)}</td>"
            f"<td class='num'>{summary.get('remote_leaves', 0)}</td>"
            f"<td class='num'>{summary.get('remote_incomplete', 0)}</td>"
            f"<td class='num'>{summary.get('indexed', len(entry.get('items') or []))}</td>"
            f"<td class='num'>{summary.get('missing', 0)}</td>"
            f"<td class='num'>{summary.get('conflicts', 0)}</td>"
            f"<td>{esc(summary.get('status'))}</td>"
            f"<td class='mono'>{esc(entry.get('source_report'))}</td>"
            "</tr>"
        )
    if artifact_index.get("errors"):
        index_rows.append(
            "<tr><td colspan='12' class='muted'>Artifact index is invalid. Run doctor for details.</td></tr>"
        )
    elif not index_rows:
        index_rows.append(
            "<tr><td colspan='12' class='muted'>No verified artifact index yet. "
            "Run collect &lt;node_id&gt; --apply or verify &lt;node_id&gt; --apply.</td></tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Syncmate Status</title>
<style>
:root {{
  --bg:#101316; --panel:#171b20; --panel2:#1f252c; --line:#313943;
  --text:#e8edf2; --muted:#9aa6b2; --green:#46c36f; --amber:#d9aa3f;
  --red:#e05d55; --blue:#6da8ff; --ink:#0b0d10;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; padding:24px; background:var(--bg); color:var(--text);
  font:13px/1.45 "Segoe UI", "Microsoft YaHei", sans-serif;
}}
.shell {{ max-width:1180px; margin:0 auto; }}
header {{ display:flex; align-items:flex-end; justify-content:space-between; gap:18px;
  border-bottom:1px solid var(--line); padding-bottom:14px; margin-bottom:18px; }}
h1 {{ margin:0; font-size:22px; font-weight:700; letter-spacing:0; }}
.sub {{ margin-top:5px; color:var(--muted); font-family:Consolas, monospace; font-size:12px; }}
.pill {{ border:1px solid var(--line); border-radius:6px; padding:6px 9px;
  background:var(--panel2); font-family:Consolas, monospace; text-transform:uppercase; }}
.pill.ready {{ color:var(--green); }} .pill.review {{ color:var(--amber); }}
.pill.attention {{ color:var(--red); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:10px; margin-bottom:18px; }}
.metric {{ border:1px solid var(--line); background:var(--panel); border-radius:6px; padding:12px; }}
.metric span {{ display:block; color:var(--muted); font-size:10px; text-transform:uppercase; letter-spacing:.06em; }}
.metric b {{ display:block; font-size:18px; margin-top:5px; }}
section {{ margin-top:20px; }}
h2 {{ font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:0 0 9px; }}
table {{ width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--line); border-radius:6px; overflow:hidden; }}
th,td {{ text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.05em; background:var(--panel2); }}
tr:last-child td {{ border-bottom:none; }}
.num {{ font-family:Consolas, monospace; text-align:right; }}
.mono {{ font-family:Consolas, monospace; }}
.muted {{ color:var(--muted); }}
.status {{ font-family:Consolas, monospace; font-weight:700; }}
.status.ok {{ color:var(--green); }}
.status.waiting, .status.action-needed, .status.partial, .status.skipped {{ color:var(--amber); }}
.status.blocked, .status.error {{ color:var(--red); }}
.status.not-required {{ color:var(--muted); }}
.diags {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:10px; }}
.diag {{ border:1px solid var(--line); border-left:4px solid var(--blue); background:var(--panel); border-radius:6px; padding:10px; }}
.diag b {{ margin-right:8px; font-family:Consolas, monospace; }}
.diag span {{ color:var(--muted); font-family:Consolas, monospace; }}
.diag p {{ margin:8px 0; }}
.diag code {{ display:block; color:#c9d4df; background:var(--panel2); border:1px solid var(--line);
  border-radius:4px; padding:6px; white-space:normal; }}
.diag.error {{ border-left-color:var(--red); }} .diag.warn {{ border-left-color:var(--amber); }}
.diag.info {{ border-left-color:var(--blue); }} .diag.ok {{ border-left-color:var(--green); }}
@media (max-width:760px) {{
  body {{ padding:14px; }} header {{ align-items:flex-start; flex-direction:column; }}
  .grid {{ grid-template-columns:1fr 1fr; }}
  table {{ font-size:12px; }}
}}
</style>
</head>
<body>
<main class="shell">
<header>
  <div>
    <h1>Syncmate Status</h1>
    <div class="sub">{esc(snapshot['generated_at'])} · {esc(device.get('id'))} · {esc(device.get('role'))}</div>
  </div>
  <div class="pill {esc(state)}">{esc(state)}</div>
</header>
<div class="grid">
  <div class="metric"><span>Git</span><b>{esc(git.get('short_sha'))}</b><div class="muted">{esc(git.get('branch'))}</div></div>
  <div class="metric"><span>Dirty</span><b>{esc(git.get('dirty'))}</b><div class="muted">{len(git.get('status_short') or [])} changed path(s)</div></div>
  <div class="metric"><span>Result Leaves</span><b>{results.get('total_leaves', 0)}</b><div class="muted">{esc(results.get('root'))}</div></div>
  <div class="metric"><span>Log Errors</span><b>{progress_summary.get('error_logs', 0)}</b><div class="muted">{progress_summary.get('total_log_files', 0)} logs, newest {esc(progress_summary.get('newest_age', 'unknown'))}</div></div>
  <div class="metric"><span>Peers</span><b>{len(device.get('peers') or [])}</b><div class="muted">{len(remote_status)} remote / {len(bundle_inspect_reports)} bundle / {len(diff_reports)} diff / {len(collect_reports)} collect / {len(verify_reports)} verify</div></div>
  <div class="metric"><span>Indexed Artifacts</span><b>{indexed_total}</b><div class="muted">{len(index_peers)} peer(s) in .syncmate index</div></div>
  <div class="metric"><span>Workflow</span><b>{esc(workflow.get('status'))}</b><div class="muted">{workflow_summary.get('next_commands', 0)} next command(s), {workflow_summary.get('manual_actions', 0)} manual action(s)</div></div>
  <div class="metric"><span>Acceptance</span><b>{esc(acceptance.get('status'))}</b><div class="muted">ready={esc(acceptance.get('ready'))}, gate {'pass' if acceptance_gate.get('passed') else 'fail'}</div></div>
  <div class="metric"><span>Fingerprint</span><b>{esc(fingerprint.get('token') or 'none')}</b><div class="muted">attention {compare_summary.get('attention', 0)}, missing {compare_summary.get('missing', 0)}</div></div>
  <div class="metric"><span>Preflight</span><b>{esc(preflight_status)}</b><div class="muted">{preflight_errors} errors, {preflight_warnings} warnings</div></div>
  <div class="metric"><span>Result Rows</span><b>{results_table_summary.get('rows', 0)}</b><div class="muted">{esc(result_table_status)}, parse errors {results_table_summary.get('parse_errors', 0)}</div></div>
</div>
<section>
  <h2>Operation Entry Points</h2>
  <div class="muted">Local commands and evidence files for humans, local AI agents, and remote AI agents.</div>
  <table>
    <thead><tr><th>Scope</th><th>Purpose</th><th>Command</th><th>Evidence</th></tr></thead>
    <tbody>{''.join(operation_entry_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Acceptance</h2>
  <div class="muted">Final machine verdict for the sync path: incremental delta, checksum acceptance, trusted index, and trusted results table.</div>
  <table>
    <thead><tr><th>Status</th><th>Ready</th><th>Gate</th><th class="num">Failures</th><th>Workflow</th><th>Core</th><th class="num">Missing</th><th class="num">Fetched</th><th class="num">Checksum OK</th><th class="num">Checksum Failed</th><th class="num">Indexed</th><th class="num">Rows</th><th>Report</th></tr></thead>
    <tbody>{''.join(acceptance_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Latest Preflight</h2>
  <table>
    <thead><tr><th>Status</th><th>Age</th><th>Generated</th><th class="num">Peers</th><th class="num">Ready</th><th class="num">Blocked</th><th class="num">Errors</th><th class="num">Warnings</th><th>Report</th></tr></thead>
    <tbody>{''.join(preflight_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Automation Core</h2>
  <div class="muted">Executable evidence chain: remote manifest -> incremental collect -> SHA-256 verify -> trusted index -> results table.</div>
  <table>
    <thead><tr><th>Status</th><th class="num">Missing</th><th class="num">Fetched</th><th class="num">Checksum OK</th><th class="num">Checksum Failed</th><th class="num">Verify Missing</th><th class="num">Indexed</th><th class="num">Result Rows</th><th>Results</th><th>Delta</th><th>Index</th><th>CSV</th></tr></thead>
    <tbody>{''.join(automation_summary_rows)}</tbody>
  </table>
  <table style="margin-top:10px">
    <thead><tr><th>Peer</th><th>Landing</th><th class="num">Missing</th><th class="num">Fetched</th><th class="num">Checksum OK</th><th class="num">Checksum Failed</th><th class="num">Verify Missing</th><th class="num">Indexed</th><th>Verify</th><th>Index</th></tr></thead>
    <tbody>{''.join(automation_peer_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Automation Workflow</h2>
  <div class="muted">Saved stage report: <span class="mono">{esc(workflow_path)}</span></div>
  <table>
    <thead><tr><th>Scope</th><th>Stage</th><th>Status</th><th>Reason</th><th>Command</th></tr></thead>
    <tbody>{''.join(workflow_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Next Commands</h2>
  <table>
    <thead><tr><th class="num">#</th><th>Kind</th><th>Peer</th><th>Reason</th><th>Evidence</th><th>Command</th></tr></thead>
    <tbody>{''.join(next_command_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Manual Actions</h2>
  <table>
    <thead><tr><th class="num">#</th><th>Kind</th><th>Peer</th><th>Reason</th><th>Action</th></tr></thead>
    <tbody>{''.join(manual_action_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Sync Layout</h2>
  <table>
    <thead><tr><th>Peer</th><th>Transport</th><th>Repo</th><th>Remote Roots</th><th>Local Landing</th><th>Artifacts</th><th>Example Mapping</th><th class="num">Indexed</th><th class="num">Rows</th><th>Command</th></tr></thead>
    <tbody>{''.join(layout_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Diagnostics</h2>
  <div class="diags">{''.join(diag_rows)}</div>
</section>
<section>
  <h2>Fingerprint Compare</h2>
  <table>
    <thead><tr><th>Peer</th><th>Status</th><th>Age</th><th>Local Token</th><th>Remote Token</th><th class="num">Matched</th><th>Different Components</th><th>Attention</th><th>Report</th></tr></thead>
    <tbody>{''.join(compare_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Trusted Results Table</h2>
  <table>
    <thead><tr><th>Status</th><th>Generated</th><th class="num">Rows</th><th class="num">Leaves</th><th class="num">Complete</th><th class="num">Parse Errors</th><th>JSON</th><th>CSV</th></tr></thead>
    <tbody>{''.join(result_table_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Remote Peers</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Last Seen</th><th>Device</th><th>Role</th><th>Git</th><th>Dirty</th><th class="num">Leaves</th><th>Nodes</th><th>Status</th><th>Report</th></tr></thead>
    <tbody>{''.join(remote_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Bundle Inspections</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Inspected</th><th>Status</th><th>Git</th><th>Fingerprint</th><th class="num">Files</th><th class="num">Leaves</th><th class="num">Incomplete</th><th class="num">Warnings</th><th class="num">Errors</th><th>Bundle</th><th>Report</th></tr></thead>
    <tbody>{''.join(bundle_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Collect Diffs</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Checked</th><th>Landing</th><th class="num">Remote</th><th class="num">Leaves</th><th class="num">Incomplete</th><th class="num">Current</th><th class="num">Missing</th><th class="num">Conflicts</th><th class="num">To Fetch</th><th>Status</th><th>Report</th></tr></thead>
    <tbody>{''.join(diff_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Last Collections</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Collected</th><th>Landing</th><th class="num">Remote</th><th class="num">Leaves</th><th class="num">Incomplete</th><th class="num">Current</th><th class="num">Fetched</th><th class="num">Conflicts</th><th class="num">Verified</th><th class="num">Failed</th><th>Status</th><th>Report</th></tr></thead>
    <tbody>{''.join(collect_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Latest Verifications</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Verified At</th><th>Landing</th><th class="num">Remote</th><th class="num">Leaves</th><th class="num">Incomplete</th><th class="num">Current</th><th class="num">Missing</th><th class="num">Conflicts</th><th>Status</th><th>Report</th></tr></thead>
    <tbody>{''.join(verify_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Artifact Index</h2>
  <table>
    <thead><tr><th>Peer</th><th>Age</th><th>Updated</th><th>Landing</th><th class="num">Remote</th><th class="num">Leaves</th><th class="num">Incomplete</th><th class="num">Indexed</th><th class="num">Missing</th><th class="num">Conflicts</th><th>Status</th><th>Source</th></tr></thead>
    <tbody>{''.join(index_rows)}</tbody>
  </table>
</section>
<section>
  <h2>Result Nodes</h2>
  <table>
    <thead><tr><th>Node</th><th class="num">Leaves</th><th>Files</th><th>Layouts</th><th>Issues</th></tr></thead>
    <tbody>{''.join(node_rows)}</tbody>
  </table>
</section>
</main>
</body>
</html>
"""


def write_dashboard(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                    write_runbook_doc: bool = True,
                    write_checklist_doc: bool = True) -> Path:
    ensure_sync_dir()
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=8,
    )
    workflow_path = write_workflow(workflow)
    workflow["workflow_path"] = rel(workflow_path)
    automation_core = automation_core_payload_from_snapshot(snapshot, limit=8)
    automation_path = write_automation_core(automation_core)
    automation_core["automation_core_path"] = rel(automation_path)
    automation_markdown_path = write_automation_core_markdown(automation_core)
    automation_core["automation_core_markdown_path"] = rel(automation_markdown_path)
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=8,
    )
    acceptance_path = write_acceptance(acceptance)
    acceptance["acceptance_path"] = rel(acceptance_path)
    action_plan = next_steps_payload(
        snapshot,
        diagnostics,
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=8,
    )
    write_action_plan(action_plan)
    if write_runbook_doc:
        write_runbook(runbook_payload(snapshot, diagnostics, limit=8))
    if write_checklist_doc:
        write_checklist(checklist_payload(
            snapshot,
            diagnostics,
            require_preflight=True,
            require_verify=True,
            require_results=True,
            limit=8,
        ))
    STATUS_HTML.write_text(
        render_status_html(
            snapshot,
            diagnostics,
            workflow_data=workflow,
            automation_core_data=automation_core,
            acceptance_data=acceptance,
        ),
        encoding="utf-8",
    )
    return STATUS_HTML


def peer_or_die(device: Dict[str, Any], node_id: str) -> Dict[str, Any]:
    peers = device.get("peers") or {}
    peer = peers.get(node_id)
    if not peer:
        known = ", ".join(sorted(peers)) or "none"
        raise SystemExit(f"Unknown peer {node_id!r}. Known peers: {known}")
    return peer


def handoff_next_items(items: List[Dict[str, Any]], node_id: str, *, limit: int = 5) -> List[Dict[str, Any]]:
    selected = []
    for item in items:
        if not isinstance(item, dict):
            continue
        item_node = item.get("node_id")
        if item_node not in (None, "", node_id):
            continue
        selected.append(item)
        if len(selected) >= max(0, limit):
            break
    return selected


def handoff_state_payload(snapshot: Optional[Dict[str, Any]],
                          diagnostics: Optional[List[Dict[str, Any]]],
                          node_id: str,
                          *,
                          limit: int = 5) -> Dict[str, Any]:
    if not snapshot:
        return {
            "available": False,
            "reason": "No local snapshot was provided.",
            "workflow": {"path": rel(workflow_file())},
            "automation_core": {"path": rel(automation_core_file())},
            "acceptance": {"path": rel(acceptance_file())},
        }
    diagnostics = diagnostics or []
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        node_ids=[node_id],
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=limit,
    )
    automation_core = automation_core_payload_from_snapshot(
        snapshot,
        node_ids=[node_id],
        limit=limit,
    )
    acceptance = acceptance_payload(
        snapshot,
        diagnostics,
        node_ids=[node_id],
        require_preflight=True,
        require_verify=True,
        require_results=True,
        limit=limit,
    )
    peer_workflow = (workflow.get("peers") or {}).get(node_id) or {}
    peer_core = (automation_core.get("peers") or {}).get(node_id) or {}
    next_payload = workflow.get("next") or {}
    return {
        "available": True,
        "workflow": {
            "path": rel(workflow_file()),
            "status": workflow.get("status"),
            "peer_status": peer_workflow.get("status"),
            "gate_passed": ((workflow.get("gate") or {}).get("passed")),
            "next_commands": handoff_next_items(next_payload.get("commands") or [], node_id, limit=limit),
            "manual_actions": handoff_next_items(next_payload.get("manual_actions") or [], node_id, limit=limit),
        },
        "automation_core": {
            "path": rel(automation_core_file()),
            "status": automation_core.get("status"),
            "totals": automation_core.get("totals") or {},
            "peer": peer_core,
            "results": automation_core.get("results") or {},
            "files": automation_core.get("files") or {},
        },
        "acceptance": {
            "path": rel(acceptance_file()),
            "status": acceptance.get("status"),
            "ready": acceptance.get("ready"),
            "blockers": acceptance.get("blockers") or [],
        },
    }


def handoff_payload(device: Dict[str, Any], node_id: str, peer: Dict[str, Any],
                    config_path: Path,
                    snapshot: Optional[Dict[str, Any]] = None,
                    diagnostics: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    ssh = transport_ssh_value(peer)
    repo_path = peer.get("repo_path")
    if (not ssh and not peer_uses_local_transport(peer)) or not repo_path:
        raise SystemExit(f"Peer {node_id!r} needs 'ssh' and 'repo_path'")

    roots = peer.get("result_roots") or ["results/runs"]
    landing = peer.get("landing") or f"results/runs/{node_id}"
    artifact_names = artifact_names_for_peer(device, peer)
    python_executable = peer_python_executable(peer)
    remote_status_cmd = remote_status_command(repo_path, python_executable)
    remote_manifest_cmd = remote_manifest_command(
        repo_path,
        roots,
        artifact_names,
        python_executable,
    )
    local_mode = peer_uses_local_transport(peer)
    remote_init_cmd = runner_init_command(
        repo_path,
        node_id,
        peer.get("role", "runner"),
        device.get("device_id"),
        artifact_names,
        python_executable,
    )
    return {
        "generated_at": now_iso(),
        "mode": "handoff",
        "device": {
            "id": device.get("device_id"),
            "role": device.get("role"),
            "setup_file": rel(config_path),
        },
        "node_id": node_id,
        "peer": {
            "role": peer.get("role", "runner"),
            "transport": peer_transport(peer),
            "ssh": peer.get("ssh"),
            "repo_path": repo_path,
            "python_executable": python_executable,
            "result_roots": roots,
            "landing": landing,
        },
        "artifact_policy": artifact_policy_payload(artifact_names),
        "reports": {
            "remote_status": f".syncmate/remote_status_{node_id}.json",
            "diff": f".syncmate/last_diff_{node_id}.json",
            "collect": f".syncmate/last_collect_{node_id}.json",
            "verify": f".syncmate/last_verify_{node_id}.json",
            "workflow": ".syncmate/workflow.json",
            "automation_core": ".syncmate/automation_core.json",
            "acceptance": ".syncmate/acceptance.json",
            "checklist": ".syncmate/checklist.md",
            "runbook": ".syncmate/runbook.md",
            "results_table": ".syncmate/results_table.json",
            "receipt": f".syncmate/receipt_{node_id}.md",
            "dashboard": ".syncmate/status.html",
        },
        "commands": {
            "collector": {
                "summary": "python scripts/syncmate/syncmate.py summary",
                "brief": "python scripts/syncmate/syncmate.py brief",
                "preflight": f"python scripts/syncmate/syncmate.py preflight {node_id}",
                "preflight_write": "python scripts/syncmate/syncmate.py preflight --write",
                "sync": f"python scripts/syncmate/syncmate.py sync {node_id}",
                "workflow": f"python scripts/syncmate/syncmate.py workflow {node_id} --write --json",
                "automation_core": f"python scripts/syncmate/syncmate.py automation-core {node_id} --write --json",
                "acceptance": f"python scripts/syncmate/syncmate.py acceptance {node_id} --write --json",
                "checklist": f"python scripts/syncmate/syncmate.py checklist {node_id} --write",
                "runbook": f"python scripts/syncmate/syncmate.py runbook {node_id} --write",
                "next": "python scripts/syncmate/syncmate.py next --require-preflight --require-verify",
                "status": "python scripts/syncmate/syncmate.py status",
                "fingerprint": "python scripts/syncmate/syncmate.py fingerprint",
                "compare": f"python scripts/syncmate/syncmate.py compare {node_id}",
                "progress": "python scripts/syncmate/syncmate.py progress",
                "history": "python scripts/syncmate/syncmate.py history",
                "inventory": "python scripts/syncmate/syncmate.py inventory",
                "export": "python scripts/syncmate/syncmate.py export --write --check",
                "results": "python scripts/syncmate/syncmate.py results --write --check",
                "receipt": f"python scripts/syncmate/syncmate.py receipt {node_id}",
                "doctor": "python scripts/syncmate/syncmate.py doctor",
                "remote_status": f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply",
                "diff": f"python scripts/syncmate/syncmate.py collect {node_id} --diff",
                "collect": f"python scripts/syncmate/syncmate.py collect {node_id} --apply",
                "import_bundle": f"python scripts/syncmate/syncmate.py import-bundle <bundle_{node_id}.zip>",
                "verify": f"python scripts/syncmate/syncmate.py verify {node_id} --apply",
                "gate": "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify",
                "dashboard": "python scripts/syncmate/syncmate.py dashboard",
            },
            "remote_agent": {
                "init_device": remote_init_cmd,
                "self": f"cd {shell_quote(repo_path)} && {command_line([python_executable, 'scripts/syncmate/syncmate.py', 'self'])}",
                "progress_json": f"cd {shell_quote(repo_path)} && {command_line([python_executable, 'scripts/syncmate/syncmate.py', 'progress', '--json'])}",
                "status_json": remote_status_cmd,
                "manifest_json": remote_manifest_cmd,
                "publish": f"cd {shell_quote(repo_path)} && {command_line([python_executable, 'scripts/syncmate/syncmate.py', 'publish', '--write'])}",
                "bundle": f"cd {shell_quote(repo_path)} && {command_line([python_executable, 'scripts/syncmate/syncmate.py', 'bundle'])}",
            },
            "ssh": {
                "status_json": (
                    f"python scripts/syncmate/syncmate.py remote-status {node_id} --apply"
                    if local_mode else f'ssh {ssh} "{remote_status_cmd}"'
                ),
                "manifest_json": (
                    f"python scripts/syncmate/syncmate.py collect {node_id} --diff"
                    if local_mode else f'ssh {ssh} "{remote_manifest_cmd}"'
                ),
            },
        },
        "state": handoff_state_payload(snapshot, diagnostics, node_id),
        "checks": [
            "Keep tracked project files synchronized with git; Syncmate only moves selected result artifacts.",
            "Treat git mismatch diagnostics as blocking until both devices are on the intended revision.",
            "Review doctor output before treating collected artifacts as accepted.",
            "Run preflight --write before strict automation; it records the device-local setup contract.",
            "If SSH is unavailable, ask the remote agent to run bundle, copy the zip back, then run import-bundle locally.",
            "Run verify after collect; a clean handoff has missing=0, conflicts=0, status=verified.",
            "Run results --write --check before downstream aggregation; it extracts metrics only from indexed artifacts.",
            "Run gate --require-preflight --require-verify before downstream aggregation; it also checks the local artifact index.",
            "Do not use --overwrite unless the peer artifacts are the intended source of truth.",
        ],
    }


def render_handoff_items(items: List[Dict[str, Any]], key: str) -> List[str]:
    if not items:
        return ["- none"]
    lines = []
    for item in items:
        if not isinstance(item, dict):
            continue
        label = item.get("kind") or item.get("id") or "step"
        reason = item.get("reason") or ""
        value = item.get(key) or ""
        peer = item.get("node_id")
        peer_text = f" [{peer}]" if peer else ""
        lines.append(f"- {label}{peer_text}: {reason} :: `{value}`")
    return lines or ["- none"]


def render_handoff_state_markdown(state: Dict[str, Any]) -> str:
    workflow = state.get("workflow") or {}
    automation = state.get("automation_core") or {}
    acceptance = state.get("acceptance") or {}
    totals = automation.get("totals") or {}
    peer = automation.get("peer") or {}
    peer_counts = peer.get("counts") or {}
    results = automation.get("results") or {}
    if not state.get("available"):
        return "\n".join([
            "## Current State",
            "",
            f"- Snapshot: unavailable ({state.get('reason') or 'no local evidence loaded'})",
            f"- Workflow path: {workflow.get('path')}",
            f"- Automation core path: {automation.get('path')}",
            f"- Acceptance path: {acceptance.get('path')}",
        ])
    lines = [
        "## Current State",
        "",
        f"- Workflow: status={workflow.get('status')} peer_status={workflow.get('peer_status')} gate_passed={workflow.get('gate_passed')} path={workflow.get('path')}",
        f"- Automation core: status={automation.get('status')} path={automation.get('path')}",
        f"- Acceptance: status={acceptance.get('status')} ready={acceptance.get('ready')} path={acceptance.get('path')} blockers={','.join(acceptance.get('blockers') or []) or 'none'}",
        f"- Totals: missing={totals.get('missing', 0)} fetched={totals.get('fetched_missing', 0)} "
        f"checksum_ok={totals.get('checksum_verified', 0)} checksum_failed={totals.get('checksum_failed', 0)} "
        f"indexed={totals.get('indexed', 0)} result_rows={results.get('rows', 0)}",
        f"- Peer counts: landing={peer.get('landing') or 'unknown'} missing={peer_counts.get('missing', 0)} "
        f"fetched={peer_counts.get('fetched_missing', 0)} checksum_ok={peer_counts.get('checksum_verified', 0)} "
        f"failed={peer_counts.get('checksum_failed', 0)} indexed={peer_counts.get('indexed', 0)} "
        f"verify={peer.get('verify_status')}",
        "",
        "### Suggested Next Commands",
        "",
        *render_handoff_items(workflow.get("next_commands") or [], "command"),
        "",
        "### Manual Actions",
        "",
        *render_handoff_items(workflow.get("manual_actions") or [], "action"),
    ]
    return "\n".join(lines)


def render_handoff_markdown(payload: Dict[str, Any]) -> str:
    peer = payload["peer"]
    artifacts = ", ".join(payload["artifact_policy"]["include"])
    roots = ", ".join(peer["result_roots"])
    collector = payload["commands"]["collector"]
    remote_agent = payload["commands"]["remote_agent"]
    ssh_cmds = payload["commands"]["ssh"]
    reports = payload["reports"]
    checks = "\n".join(f"- {item}" for item in payload["checks"])
    current_state = render_handoff_state_markdown(payload.get("state") or {})
    return f"""# Syncmate Handoff: {payload['node_id']}

Generated: {payload['generated_at']}

## Contract

- Collector device: {payload['device']['id']} ({payload['device']['role']})
- Setup file: {payload['device']['setup_file']}
- Peer role: {peer['role']}
- Transport: {peer.get('transport', 'ssh')}
- SSH: {peer.get('ssh') or 'none'}
- Peer repo: {peer['repo_path']}
- Remote result roots: {roots}
- Local landing: {peer['landing']}
- Artifacts: {artifacts}

{current_state}

## Collector Commands

```bash
{collector['summary']}
{collector['brief']}
{collector['preflight']}
{collector['preflight_write']}
{collector['sync']}
{collector['workflow']}
{collector['automation_core']}
{collector['acceptance']}
{collector['checklist']}
{collector['runbook']}
{collector['next']}
{collector['status']}
{collector['fingerprint']}
{collector['compare']}
{collector['progress']}
{collector['history']}
{collector['inventory']}
{collector['export']}
{collector['results']}
{collector['receipt']}
{collector['doctor']}
{collector['remote_status']}
{collector['diff']}
{collector['collect']}
{collector['import_bundle']}
{collector['verify']}
{collector['gate']}
{collector['dashboard']}
```

## Remote AI Commands

Run these on the runner when a remote AI needs to inspect local state without pushing files:

```bash
{remote_agent['init_device']}
{remote_agent['self']}
{remote_agent['progress_json']}
{remote_agent['status_json']}
{remote_agent['manifest_json']}
{remote_agent['publish']}
{remote_agent['bundle']}
```

## Collector Peer Probes

```bash
{ssh_cmds['status_json']}
{ssh_cmds['manifest_json']}
```

## Reports

- Remote status: {reports['remote_status']}
- Diff: {reports['diff']}
- Collection: {reports['collect']}
- Verification: {reports['verify']}
- Workflow: {reports['workflow']}
- Automation core: {reports['automation_core']}
- Acceptance: {reports['acceptance']}
- Checklist: {reports['checklist']}
- Runbook: {reports['runbook']}
- Results table: {reports['results_table']}
- Receipt: {reports['receipt']}
- Dashboard: {reports['dashboard']}

## Checks

{checks}
"""


def write_handoff(payload: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = SYNC_DIR / f"handoff_{payload['node_id']}.md"
    out.write_text(render_handoff_markdown(payload), encoding="utf-8")
    return out


def render_handoff_bundle_markdown(payloads: List[Dict[str, Any]]) -> str:
    if not payloads:
        return "# Syncmate Handoffs\n\nNo peer handoffs.\n"
    lines = [
        "# Syncmate Handoffs",
        "",
        f"Generated: {now_iso()}",
        "",
        "## Peers",
        "",
    ]
    for payload in payloads:
        peer = payload["peer"]
        lines.append(
            f"- {payload['node_id']}: transport={peer.get('transport', 'ssh')} "
            f"ssh={peer.get('ssh') or 'none'} repo={peer['repo_path']} "
            f"landing={peer['landing']}"
        )
    lines.append("")
    for payload in payloads:
        lines.append("---")
        lines.append("")
        lines.append(render_handoff_markdown(payload).strip())
        lines.append("")
    return "\n".join(lines)


def write_handoff_bundle(payloads: List[Dict[str, Any]]) -> Path:
    ensure_sync_dir()
    out = SYNC_DIR / "handoff_all.md"
    out.write_text(render_handoff_bundle_markdown(payloads), encoding="utf-8")
    return out


def cmd_remote_status(args: argparse.Namespace) -> int:
    device, _warnings = load_device(args.config)
    peer = peer_or_die(device, args.node_id)
    ssh = transport_ssh_value(peer)
    repo_path = peer.get("repo_path")
    python_executable = peer_python_executable(peer)
    python_kwargs = peer_python_kwargs(peer)
    if (not ssh and not peer_uses_local_transport(peer)) or not repo_path:
        raise SystemExit(f"Peer {args.node_id!r} needs 'ssh' and 'repo_path'")

    remote_cmd = remote_status_command(repo_path, python_executable)
    local_mode = peer_uses_local_transport(peer)
    data = {
        "node_id": args.node_id,
        "mode": "apply" if args.apply else "plan-only",
        **transport_payload(ssh),
        "repo_path": repo_path,
        "python_executable": python_executable,
        "command": (
            f"python scripts/syncmate/syncmate.py remote-status {args.node_id} --apply"
            if local_mode else f'ssh {ssh} "{remote_cmd}"'
        ),
    }
    if args.apply:
        result = apply_remote_status(
            args.node_id,
            ssh,
            repo_path,
            save=not args.no_save,
            **python_kwargs,
        )
        if args.json:
            print_json(result)
            return 0 if not result.get("errors") else 1
        print_remote_status_result(result)
        return 0 if not result.get("errors") else 1

    if args.json:
        print_json(data)
        return 0
    print(f"syncmate remote-status plan: {args.node_id}")
    print("  This command is read-only. Run it from the collector or give it to the remote AI:")
    print("")
    print(data["command"])
    print("")
    print(f"  or run: python scripts/syncmate/syncmate.py remote-status {args.node_id} --apply")
    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    if args.apply and args.diff:
        raise SystemExit("--diff and --apply are mutually exclusive")

    device, _warnings = load_device(args.config)
    peer = peer_or_die(device, args.node_id)
    ssh = transport_ssh_value(peer)
    repo_path = peer.get("repo_path")
    python_executable = peer_python_executable(peer)
    python_kwargs = peer_python_kwargs(peer)
    if (not ssh and not peer_uses_local_transport(peer)) or not repo_path:
        raise SystemExit(f"Peer {args.node_id!r} needs 'ssh' and 'repo_path'")

    roots = peer.get("result_roots") or ["results/runs"]
    landing = peer.get("landing") or f"results/runs/{args.node_id}"
    artifact_names = artifact_names_for_peer(device, peer)
    diff_command = f"python scripts/syncmate/syncmate.py collect {args.node_id} --diff"
    apply_command = f"python scripts/syncmate/syncmate.py collect {args.node_id} --apply"
    data = {
        "node_id": args.node_id,
        "mode": "apply" if args.apply else "diff" if args.diff else "plan-only",
        "artifact_policy": artifact_policy_payload(artifact_names),
        **transport_payload(ssh),
        "repo_path": repo_path,
        "python_executable": python_executable,
        "result_roots": roots,
        "landing": landing,
        "commands": {
            "diff": diff_command,
            "apply": apply_command,
        },
        "notes": [
            "collect --diff contacts the peer and compares remote checksums with the local landing directory.",
            "collect --apply fetches only missing selected artifacts and verifies SHA-256 after extraction.",
            "Checksum conflicts are reported and left untouched unless --overwrite is explicit.",
        ],
    }
    if args.diff:
        result = diff_collect(args.node_id, ssh, repo_path, roots, landing,
                              artifact_names=artifact_names, save=not args.no_save,
                              **python_kwargs)
        if args.json:
            print_json(result)
            return 0 if not result.get("errors") else 1
        print_collect_diff(result)
        return 0 if not result.get("errors") else 1

    if args.apply:
        result = apply_collect(args.node_id, ssh, repo_path, roots, landing,
                               artifact_names=artifact_names, overwrite=args.overwrite,
                               save=not args.no_save, **python_kwargs)
        if args.json:
            print_json(result)
            return 0 if not result.get("errors") else 1
        print_collect_result(result)
        return 0 if not result.get("errors") else 1

    if args.json:
        print_json(data)
        return 0
    print(f"syncmate collect plan: {args.node_id}")
    print(f"  artifacts: {', '.join(artifact_names)}")
    print(f"  landing: {landing}")
    print("  inspect remote delta:")
    print("")
    print(diff_command)
    print("")
    print("  apply incremental collection:")
    print("")
    print(apply_command)
    print("")
    for note in data["notes"]:
        print(f"  note: {note}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    device, _warnings = load_device(args.config)
    peer = peer_or_die(device, args.node_id)
    ssh = transport_ssh_value(peer)
    repo_path = peer.get("repo_path")
    python_executable = peer_python_executable(peer)
    python_kwargs = peer_python_kwargs(peer)
    if (not ssh and not peer_uses_local_transport(peer)) or not repo_path:
        raise SystemExit(f"Peer {args.node_id!r} needs 'ssh' and 'repo_path'")

    roots = peer.get("result_roots") or ["results/runs"]
    landing = peer.get("landing") or f"results/runs/{args.node_id}"
    artifact_names = artifact_names_for_peer(device, peer)
    apply_command = f"python scripts/syncmate/syncmate.py verify {args.node_id} --apply"
    data = {
        "node_id": args.node_id,
        "mode": "apply" if args.apply else "plan-only",
        "artifact_policy": artifact_policy_payload(artifact_names),
        **transport_payload(ssh),
        "repo_path": repo_path,
        "python_executable": python_executable,
        "result_roots": roots,
        "landing": landing,
        "commands": {
            "apply": apply_command,
        },
        "notes": [
            "verify --apply contacts the peer, reads its manifest, and checks the local landing checksums.",
            "verify never downloads files; run collect --apply first if artifacts are missing.",
            "A verified report has missing=0 and conflicts=0.",
        ],
    }
    if args.apply:
        result = verify_collect(args.node_id, ssh, repo_path, roots, landing,
                                artifact_names=artifact_names, save=not args.no_save,
                                **python_kwargs)
        failures = verify_result_failures(result)
        if args.json:
            print_json(result)
            return 0 if not failures else 1
        print_verify_result(result)
        return 0 if not failures else 1

    if args.json:
        print_json(data)
        return 0
    print(f"syncmate verify plan: {args.node_id}")
    print(f"  artifacts: {', '.join(artifact_names)}")
    print(f"  landing: {landing}")
    print("  apply remote checksum verification:")
    print("")
    print(apply_command)
    print("")
    for note in data["notes"]:
        print(f"  note: {note}")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    peers = device.get("peers") or {}
    if not peers:
        raise SystemExit("No peers configured. Use add-peer first.")

    node_ids = args.node_ids or sorted(peers)
    unknown = [node_id for node_id in node_ids if node_id not in peers]
    if unknown:
        known = ", ".join(sorted(peers)) or "none"
        raise SystemExit(f"Unknown peer(s): {', '.join(unknown)}. Known peers: {known}")

    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    payloads = [
        handoff_payload(device, node_id, peers[node_id], args.config, snapshot, diagnostics)
        for node_id in node_ids
    ]
    written_paths: List[str] = []
    if args.write:
        for payload in payloads:
            out = write_handoff(payload)
            payload["handoff_path"] = rel(out)
            written_paths.append(rel(out))
        if len(payloads) > 1:
            bundle = write_handoff_bundle(payloads)
            written_paths.append(rel(bundle))

    if args.json:
        if len(payloads) == 1:
            print_json(payloads[0])
        else:
            print_json({
                "generated_at": now_iso(),
                "mode": "handoff-set",
                "count": len(payloads),
                "node_ids": [payload["node_id"] for payload in payloads],
                "handoffs": payloads,
                "handoff_paths": written_paths,
            })
        return 0

    if len(payloads) == 1:
        print(render_handoff_markdown(payloads[0]))
    else:
        print(render_handoff_bundle_markdown(payloads))
    for path in written_paths:
        print(f"wrote: {path}")
    return 0


def refresh_peer(node_id: str, peer: Dict[str, Any], *,
                 artifact_names: Optional[Tuple[str, ...]] = None,
                 apply: bool = False, verify: bool = False,
                 overwrite: bool = False, save: bool = True) -> Dict[str, Any]:
    ssh = transport_ssh_value(peer)
    repo_path = peer.get("repo_path")
    if (not ssh and not peer_uses_local_transport(peer)) or not repo_path:
        return {
            "node_id": node_id,
            "errors": [f"Peer {node_id!r} needs 'ssh' and 'repo_path'"],
        }

    roots = peer.get("result_roots") or ["results/runs"]
    landing = peer.get("landing") or f"results/runs/{node_id}"
    names = artifact_names or ARTIFACT_NAMES
    python_kwargs = peer_python_kwargs(peer)
    remote = apply_remote_status(node_id, ssh, repo_path, save=save, **python_kwargs)
    diff = diff_collect(node_id, ssh, repo_path, roots, landing,
                        artifact_names=names, save=save, **python_kwargs)
    collect = None
    if apply:
        collect = apply_collect(node_id, ssh, repo_path, roots, landing,
                                artifact_names=names, overwrite=overwrite, save=save,
                                **python_kwargs)
    verify_report = None
    if verify:
        verify_report = verify_collect(node_id, ssh, repo_path, roots, landing,
                                       artifact_names=names, save=save, **python_kwargs)

    errors = []
    for item in (remote, diff, collect):
        if item:
            errors.extend(item.get("errors") or [])
    errors.extend(verify_result_failures(verify_report))
    result = {
        "node_id": node_id,
        "remote_status": remote,
        "diff": diff,
        "collect": collect,
        "verify": verify_report,
        "errors": errors,
    }
    return result


def overlay_peer_results(snapshot: Dict[str, Any], peer_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    for node_id, result in peer_results.items():
        if result.get("remote_status"):
            snapshot.setdefault("remote_status", {})[node_id] = result["remote_status"]
        if result.get("diff"):
            snapshot.setdefault("diff_reports", {})[node_id] = result["diff"]
        if result.get("collect"):
            snapshot.setdefault("collect_reports", {})[node_id] = result["collect"]
        if result.get("verify"):
            snapshot.setdefault("verify_reports", {})[node_id] = result["verify"]
    return snapshot


def peer_results_from_snapshot(snapshot: Dict[str, Any], node_ids: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    selected = [str(node) for node in (node_ids or known_report_nodes(snapshot))]
    out: Dict[str, Dict[str, Any]] = {}
    for node_id in selected:
        remote = (snapshot.get("remote_status") or {}).get(node_id) or {}
        diff = (snapshot.get("diff_reports") or {}).get(node_id) or {}
        collect = (snapshot.get("collect_reports") or {}).get(node_id) or {}
        verify = (snapshot.get("verify_reports") or {}).get(node_id) or {}
        errors: List[str] = []
        for report in (remote, diff, collect):
            errors.extend(report.get("errors") or [])
        errors.extend(verify_result_failures(verify))
        out[node_id] = {
            "node_id": node_id,
            "remote_status": remote,
            "diff": diff,
            "collect": collect,
            "verify": verify,
            "errors": errors,
        }
    return out


def sync_automation_core(peer_results: Optional[Dict[str, Dict[str, Any]]],
                         snapshot: Dict[str, Any],
                         results_data: Optional[Dict[str, Any]],
                         previous_results_table: Optional[Any],
                         result_table_paths: Optional[Dict[str, str]],
                         *, node_ids: Optional[List[str]] = None,
                         limit: int = 5,
                         include_result_delta: bool = True) -> Dict[str, Any]:
    peer_results = peer_results or peer_results_from_snapshot(snapshot, node_ids)
    totals = Counter()
    peers: Dict[str, Dict[str, Any]] = {}
    index_peers = ((snapshot.get("artifact_index") or {}).get("peers") or {})
    result_rows_by_peer: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in (results_data or {}).get("rows") or []:
        if not isinstance(row, dict):
            continue
        row_node = row.get("node_id")
        if row_node not in (None, ""):
            result_rows_by_peer[str(row_node)].append(row)
    for node_id, result in sorted(peer_results.items()):
        diff = result.get("diff") or {}
        collect = result.get("collect") or {}
        verify = result.get("verify") or {}
        diff_summary = diff.get("summary") or {}
        collect_summary = collect.get("summary") or {}
        verify_summary = verify.get("summary") or {}
        index_entry = index_peers.get(node_id) or {}
        index_summary = index_entry.get("summary") or {}
        indexed = count_int(index_summary.get("indexed") or len(index_entry.get("items") or []))
        checksum_verified = count_int(
            first_present(
                verify_summary.get("verified_current") if verify else None,
                collect_summary.get("verified"),
            )
        )
        checksum_failed = count_int(
            first_present(
                collect_summary.get("verification_failed"),
                len(collect.get("verification_failed") or []),
            )
        )
        result_rows = result_rows_by_peer.get(str(node_id), [])
        conflict_examples = (
            verify.get("conflicts")
            or collect.get("conflicts")
            or diff.get("conflicts")
            or []
        )
        peer_counts = {
            "remote_files": count_int(first_present(verify_summary.get("remote_files"), collect_summary.get("remote_files"), diff_summary.get("remote_files"))),
            "remote_leaves": count_int(first_present(verify_summary.get("remote_leaves"), collect_summary.get("remote_leaves"), diff_summary.get("remote_leaves"), index_summary.get("remote_leaves"))),
            "remote_incomplete": max(
                count_int(diff_summary.get("remote_incomplete")),
                count_int(collect_summary.get("remote_incomplete")),
                count_int(verify_summary.get("remote_incomplete")),
                count_int(index_summary.get("remote_incomplete")),
            ),
            "already_current": count_int(diff_summary.get("already_current")),
            "missing": count_int(first_present(diff_summary.get("missing"), verify_summary.get("missing"))),
            "conflicts": max(count_int(diff_summary.get("conflicts")), count_int(verify_summary.get("conflicts"))),
            "to_fetch": count_int(collect_summary.get("to_fetch") or diff_summary.get("to_fetch")),
            "fetched": count_int(first_present(collect_summary.get("fetched"), len(collect.get("fetched") or []))),
            "fetched_missing": count_int(collect_summary.get("missing_fetched")),
            "checksum_verified": checksum_verified,
            "checksum_failed": checksum_failed,
            "verify_missing": count_int(verify_summary.get("missing")),
            "indexed": indexed,
            "errors": len(result.get("errors") or []),
        }
        for key, value in peer_counts.items():
            totals[key] += count_int(value)
        peers[node_id] = {
            "landing": (
                verify.get("landing")
                or collect.get("landing")
                or diff.get("landing")
                or (index_entry.get("landing") if isinstance(index_entry, dict) else None)
            ),
            "counts": peer_counts,
            "verify_status": verify_summary.get("status") if verify else "skipped",
            "artifact_index": rel(artifact_index_file()) if indexed else None,
            "trusted_results": {
                "rows": len(result_rows),
                "examples": compact_result_rows(result_rows, limit),
            },
            "examples": {
                "missing": compact_items(diff.get("missing") or [], limit),
                "fetched": compact_items(collect.get("fetched") or [], limit),
                "verified": compact_items(verify.get("verified") or [], limit),
                "indexed": compact_items(index_entry.get("items") or [], limit),
                "checksum_failed": compact_items(collect.get("verification_failed") or [], limit),
                "conflicts": compact_items(conflict_examples, limit),
            },
        }

    results_summary = (results_data or {}).get("summary") or {}
    results_errors = len((results_data or {}).get("errors") or []) if results_data else 0
    results_parse_errors = len((results_data or {}).get("parse_errors") or []) if results_data else 0
    if results_data:
        result_delta = (
            results_table_delta(previous_results_table, results_data, limit=limit)
            if include_result_delta else None
        )
        results_status = "ok" if not results_errors and not results_parse_errors else "error"
    else:
        result_delta = None
        results_status = "skipped"

    status = "ok"
    if totals.get("errors") or totals.get("checksum_failed") or totals.get("conflicts") or totals.get("verify_missing"):
        status = "blocked"
    elif results_status == "error":
        status = "blocked"
    elif results_status == "skipped":
        status = "partial"

    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "automation_core",
        "automation_core_path": rel(automation_core_file()),
        "automation_core_markdown_path": rel(automation_core_markdown_file()),
        "status": status,
        "pipeline": [
            "remote-status",
            "manifest-diff",
            "incremental-collect",
            "checksum-verify",
            "trusted-results",
        ],
        "totals": dict(sorted(totals.items())),
        "results": {
            "status": results_status,
            "rows": results_summary.get("rows", 0),
            "parse_errors": results_parse_errors,
            "errors": results_errors,
            "delta": result_delta,
        },
        "files": {
            "artifact_index": rel(artifact_index_file()),
            "results_json": result_table_paths.get("json") if result_table_paths else None,
            "results_csv": result_table_paths.get("csv") if result_table_paths else None,
        },
        "peers": peers,
    }


def automation_core_payload_from_snapshot(snapshot: Dict[str, Any],
                                          *,
                                          node_ids: Optional[List[str]] = None,
                                          limit: int = 8) -> Dict[str, Any]:
    results_table = snapshot.get("results_table") if isinstance(snapshot.get("results_table"), dict) else {}
    result_paths = (results_table.get("files") or {}) if results_table else None
    return sync_automation_core(
        None,
        snapshot,
        results_table if results_table else None,
        None,
        result_paths,
        node_ids=node_ids,
        limit=limit,
        include_result_delta=False,
    )


def write_automation_core(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = automation_core_file()
    data = {**data, "automation_core_path": rel(out)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def render_automation_core_markdown(data: Dict[str, Any]) -> str:
    totals = data.get("totals") or {}
    results = data.get("results") or {}
    files = data.get("files") or {}
    lines = [
        "# Syncmate Automation Core",
        "",
        f"- Generated: {data.get('generated_at') or 'unknown'}",
        f"- Status: {data.get('status') or 'unknown'}",
        f"- Pipeline: {' -> '.join(data.get('pipeline') or [])}",
        f"- JSON: {data.get('automation_core_path') or rel(automation_core_file())}",
        f"- Artifact index: {files.get('artifact_index') or rel(artifact_index_file())}",
        f"- Results JSON: {files.get('results_json') or 'not written'}",
        f"- Results CSV: {files.get('results_csv') or 'not written'}",
        "",
        "## Totals",
        "",
        (
            f"- Missing/fetched: {totals.get('missing', 0)}/"
            f"{totals.get('fetched_missing', 0)}"
        ),
        (
            f"- Checksum OK/failed: {totals.get('checksum_verified', 0)}/"
            f"{totals.get('checksum_failed', 0)}"
        ),
        f"- Verify missing/conflicts: {totals.get('verify_missing', 0)}/{totals.get('conflicts', 0)}",
        f"- Indexed artifacts: {totals.get('indexed', 0)}",
        f"- Trusted result rows: {results.get('rows', 0)}",
        f"- Result parse errors: {results.get('parse_errors', 0)}",
    ]
    delta = results.get("delta")
    if isinstance(delta, dict):
        lines.append(
            "- Result delta: "
            f"previous={delta.get('previous_rows', 0)} current={delta.get('current_rows', 0)} "
            f"added={delta.get('added_rows', 0)} changed={delta.get('changed_rows', 0)} "
            f"removed={delta.get('removed_rows', 0)}"
        )
    else:
        lines.append("- Result delta: unavailable")

    peers = data.get("peers") or {}
    if peers:
        lines.extend(["", "## Peers", ""])
        for node_id, peer in sorted(peers.items()):
            counts = peer.get("counts") or {}
            trusted = peer.get("trusted_results") or {}
            lines.extend([
                f"### {node_id}",
                "",
                f"- Landing: {peer.get('landing') or 'unknown'}",
                f"- Verify status: {peer.get('verify_status') or 'unknown'}",
                f"- Artifact index: {peer.get('artifact_index') or 'not indexed'}",
                (
                    f"- Counts: missing={counts.get('missing', 0)} "
                    f"fetched={counts.get('fetched_missing', 0)} "
                    f"checksum_ok={counts.get('checksum_verified', 0)} "
                    f"checksum_failed={counts.get('checksum_failed', 0)} "
                    f"indexed={counts.get('indexed', 0)}"
                ),
                f"- Trusted result rows: {trusted.get('rows', 0)}",
            ])
            examples = peer.get("examples") or {}
            for label, title in (
                ("missing", "Missing"),
                ("fetched", "Fetched"),
                ("verified", "Verified"),
                ("indexed", "Indexed"),
                ("checksum_failed", "Checksum Failed"),
                ("conflicts", "Conflicts"),
            ):
                items = examples.get(label) or []
                if not items:
                    continue
                lines.append(f"- {title}:")
                for item in items[:3]:
                    if isinstance(item, dict):
                        remote = item.get("remote_path") or item.get("path") or "unknown"
                        local = item.get("local_path")
                        sha = item.get("sha256") or item.get("expected_sha256")
                        suffix = f" -> {local}" if local else ""
                        sha_text = f" sha256={sha}" if sha else ""
                        lines.append(f"  - {remote}{suffix}{sha_text}")
                    else:
                        lines.append(f"  - {item}")
            result_examples = trusted.get("examples") or []
            if result_examples:
                lines.append("- Trusted result examples:")
                for row in result_examples[:3]:
                    lines.append(
                        "  - "
                        f"{row.get('cell')} {row.get('method_strategy')} {row.get('seed')} "
                        f"status={row.get('status')}"
                    )
    else:
        lines.extend(["", "## Peers", "", "- No peer evidence is available yet."])

    return "\n".join(lines).rstrip() + "\n"


def write_automation_core_markdown(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = automation_core_markdown_file()
    data = {
        **data,
        "automation_core_path": data.get("automation_core_path") or rel(automation_core_file()),
        "automation_core_markdown_path": rel(out),
    }
    out.write_text(render_automation_core_markdown(data), encoding="utf-8")
    return out


def acceptance_status_label(*, ready: bool, workflow_status: Any,
                            automation_status: Any, gate_passed: bool) -> str:
    if ready:
        return "ready"
    if not gate_passed or automation_status == "blocked":
        return "blocked"
    if workflow_status in ("waiting", "action-needed") or automation_status in ("partial", "skipped"):
        return "pending"
    return "review"


def compact_acceptance_next(next_steps: Dict[str, Any], limit: int) -> Dict[str, Any]:
    return {
        "commands": (next_steps.get("commands") or [])[:max(0, limit)],
        "manual_actions": (next_steps.get("manual_actions") or [])[:max(0, limit)],
    }


def acceptance_payload(snapshot: Dict[str, Any], diagnostics: List[Dict[str, Any]], *,
                       node_ids: Optional[List[str]] = None, fail_on: str = "warn",
                       require_preflight: bool = True, require_verify: bool = True,
                       require_results: bool = True, limit: int = 8) -> Dict[str, Any]:
    workflow = workflow_payload(
        snapshot,
        diagnostics,
        node_ids=node_ids,
        fail_on=fail_on,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    automation_core = automation_core_payload_from_snapshot(
        snapshot,
        node_ids=node_ids,
        limit=limit,
    )
    gate = gate_payload(
        snapshot,
        [],
        fail_on=fail_on,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
    )
    next_steps = next_steps_payload(
        snapshot,
        diagnostics,
        require_preflight=require_preflight,
        require_verify=require_verify,
        require_results=require_results,
        limit=limit,
    )
    preflight = snapshot.get("preflight") if isinstance(snapshot.get("preflight"), dict) else {}
    preflight_summary = preflight.get("summary") or {}
    workflow_status = workflow.get("status")
    automation_status = automation_core.get("status")
    ready = bool(
        gate.get("passed")
        and automation_status == "ok"
        and (not require_results or (automation_core.get("results") or {}).get("status") == "ok")
    )
    blockers = []
    if not gate.get("passed"):
        blockers.append("gate")
    if automation_status != "ok":
        blockers.append("automation_core")
    if require_results and (automation_core.get("results") or {}).get("status") != "ok":
        blockers.append("results")

    return {
        "generated_at": snapshot.get("generated_at"),
        "mode": "acceptance",
        "acceptance_path": rel(acceptance_file()),
        "device_id": (snapshot.get("device") or {}).get("id"),
        "status": acceptance_status_label(
            ready=ready,
            workflow_status=workflow_status,
            automation_status=automation_status,
            gate_passed=bool(gate.get("passed")),
        ),
        "ready": ready,
        "blockers": sorted(set(blockers)),
        "policy": {
            "fail_on": fail_on,
            "require_preflight": require_preflight,
            "require_verify": require_verify,
            "require_results": require_results,
        },
        "landing_rule": "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/",
        "pipeline": automation_core.get("pipeline") or [
            "remote-status",
            "manifest-diff",
            "incremental-collect",
            "checksum-verify",
            "trusted-results",
        ],
        "preflight": {
            "status": preflight.get("status") if preflight else "missing",
            "summary": preflight_summary,
            "report_path": preflight.get("report_path") if preflight else rel(last_preflight_file()),
        },
        "workflow": {
            "status": workflow_status,
            "summary": workflow.get("summary"),
            "attention": compact_workflow_attention(workflow, limit=limit),
            "path": rel(workflow_file()),
        },
        "automation_core": {
            "status": automation_status,
            "totals": automation_core.get("totals") or {},
            "results": automation_core.get("results") or {},
            "peers": automation_core.get("peers") or {},
            "path": rel(automation_core_file()),
        },
        "gate": compact_gate_payload(gate, limit=limit),
        "next": compact_acceptance_next(next_steps, limit),
        "diagnostics": diagnostics[:max(0, limit)],
        "files": {
            "acceptance": rel(acceptance_file()),
            "workflow": rel(workflow_file()),
            "automation_core": rel(automation_core_file()),
            "automation_core_markdown": rel(automation_core_markdown_file()),
            "preflight": rel(last_preflight_file()),
            "artifact_index": rel(artifact_index_file()),
            "results_json": rel(results_table_file()),
            "results_csv": rel(results_csv_file()),
            "dashboard": rel(STATUS_HTML),
            "brief": rel(brief_file()),
            "receipt": rel(receipt_file()),
        },
    }


def write_acceptance(data: Dict[str, Any]) -> Path:
    ensure_sync_dir()
    out = acceptance_file()
    data = {**data, "acceptance_path": rel(out)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def peer_ids_or_die(peers: Dict[str, Any], node_ids: List[str]) -> List[str]:
    if not peers:
        raise SystemExit("No peers configured. Use add-peer first.")
    selected = node_ids or sorted(peers)
    unknown = [node_id for node_id in selected if node_id not in peers]
    if unknown:
        known = ", ".join(sorted(peers)) or "none"
        raise SystemExit(f"Unknown peer(s): {', '.join(unknown)}. Known peers: {known}")
    return selected


def cmd_refresh(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    peers = device.get("peers") or {}
    preflight = preflight_payload(
        device,
        warnings,
        config_path=args.config,
        node_ids=args.node_ids,
        require_sync_targets=True,
    )
    maybe_write_preflight_report(preflight, save=not args.no_save)
    if preflight.get("status") == "blocked":
        data = blocked_by_preflight_payload("refresh", preflight)
        if args.json:
            print_json(data)
        else:
            print_blocked_by_preflight("refresh", preflight)
        return 1
    node_ids = peer_ids_or_die(peers, args.node_ids)

    peer_results = {}
    for node_id in node_ids:
        peer_results[node_id] = refresh_peer(
            node_id,
            peers[node_id],
            artifact_names=artifact_names_for_peer(device, peers[node_id]),
            apply=args.apply,
            verify=args.verify,
            overwrite=args.overwrite,
            save=not args.no_save,
        )

    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    if args.write_state:
        write_state(snapshot, "refresh")

    dashboard_path = None
    if args.dashboard:
        dashboard_path = write_dashboard(snapshot, diagnostics)

    errors = []
    for result in peer_results.values():
        errors.extend(result.get("errors") or [])

    data = {
        "generated_at": snapshot["generated_at"],
        "mode": "apply" if args.apply else "diff",
        "verify": bool(args.verify),
        "device_id": snapshot["device"]["id"],
        "peers": sorted(peer_results),
        "preflight": preflight,
        "status": status_label(snapshot, diagnostics),
        "diagnostics": len(diagnostics),
        "dashboard": rel(dashboard_path) if dashboard_path else None,
        "workflow": rel(workflow_file()) if dashboard_path else None,
        "automation_core_path": rel(automation_core_file()) if dashboard_path else None,
        "automation_core_markdown_path": rel(automation_core_markdown_file()) if dashboard_path else None,
        "acceptance": rel(acceptance_file()) if dashboard_path else None,
        "action_plan": rel(action_plan_file()) if dashboard_path else None,
        "action_plan_markdown": rel(action_plan_markdown_file()) if dashboard_path else None,
        "checklist": rel(checklist_file()) if dashboard_path else None,
        "runbook": rel(runbook_file()) if dashboard_path else None,
        "remote_reports": len(snapshot.get("remote_status") or {}),
        "bundle_inspect_reports": len(snapshot.get("bundle_inspect_reports") or {}),
        "diff_reports": len(snapshot.get("diff_reports") or {}),
        "collect_reports": len(snapshot.get("collect_reports") or {}),
        "verify_reports": len(snapshot.get("verify_reports") or {}),
        "peer_results": peer_results,
        "errors": errors,
    }
    if args.json:
        print_json(data)
        return 0 if not errors else 1

    print(f"syncmate refresh: {', '.join(data['peers'])}")
    print(f"  mode: {data['mode']}")
    print(f"  verify: {data['verify']}")
    print(
        f"  preflight: {preflight.get('status')} "
        f"ready={((preflight.get('summary') or {}).get('ready', 0))} "
        f"blocked={((preflight.get('summary') or {}).get('blocked', 0))}"
    )
    print(f"  status: {data['status']} diagnostics={data['diagnostics']}")
    print(
        f"  reports: remote={data['remote_reports']} bundle={data['bundle_inspect_reports']} "
        f"diff={data['diff_reports']} collect={data['collect_reports']} verify={data['verify_reports']}"
    )
    if dashboard_path:
        print(f"  dashboard: {rel(dashboard_path)}")
        print(f"  workflow: {rel(workflow_file())}")
        print(f"  automation core: {rel(automation_core_file())}")
        print(f"  automation core markdown: {rel(automation_core_markdown_file())}")
        print(f"  acceptance: {rel(acceptance_file())}")
        print(f"  action plan: {rel(action_plan_file())}")
        print(f"  action plan markdown: {rel(action_plan_markdown_file())}")
        print(f"  checklist: {rel(checklist_file())}")
        print(f"  runbook: {rel(runbook_file())}")
    for node_id, result in peer_results.items():
        remote_errors = len((result.get("remote_status") or {}).get("errors") or [])
        diff_errors = len((result.get("diff") or {}).get("errors") or [])
        collect_errors = len((result.get("collect") or {}).get("errors") or []) if result.get("collect") else 0
        verify_errors = len(verify_result_failures(result.get("verify"))) if result.get("verify") else 0
        print(f"  - {node_id}: remote_errors={remote_errors} diff_errors={diff_errors} collect_errors={collect_errors} verify_errors={verify_errors}")
    if errors:
        print("  errors:")
        for err in errors:
            print(f"    {err}")
    return 0 if not errors else 1


def cmd_sync(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    peers = device.get("peers") or {}
    preflight = preflight_payload(
        device,
        warnings,
        config_path=args.config,
        node_ids=args.node_ids,
        require_sync_targets=True,
    )
    maybe_write_preflight_report(preflight, save=True)
    if preflight.get("status") == "blocked":
        data = blocked_by_preflight_payload("sync", preflight)
        if args.json:
            print_json(data)
        else:
            print_blocked_by_preflight("sync", preflight, limit=args.limit)
        return 1
    node_ids = peer_ids_or_die(peers, args.node_ids)

    apply_results = not args.dry_run
    verify_results = apply_results and not args.no_verify
    write_result_table = apply_results and verify_results and args.results
    previous_results_table = load_optional_json(results_table_file()) if write_result_table else None
    peer_results = {}
    for node_id in node_ids:
        peer_results[node_id] = refresh_peer(
            node_id,
            peers[node_id],
            artifact_names=artifact_names_for_peer(device, peers[node_id]),
            apply=apply_results,
            verify=verify_results,
            overwrite=args.overwrite,
            save=True,
        )

    snapshot = overlay_peer_results(build_snapshot(device, warnings), peer_results)
    results_data = None
    result_table_paths = None
    if write_result_table:
        results_data = results_payload_from_index(
            snapshot.get("artifact_index") or {},
            node_ids=node_ids,
            include_incomplete=False,
        )
        result_table_paths = write_results_table_files(results_data)
        results_data["written"] = result_table_paths
        snapshot["results_table"] = results_data
        snapshot["fingerprint"] = fingerprint_payload(snapshot)

    diagnostics = diagnostics_for_snapshot(snapshot)
    automation_core = sync_automation_core(
        peer_results,
        snapshot,
        results_data,
        previous_results_table,
        result_table_paths,
        limit=args.limit,
    )
    if args.write_state:
        write_state(snapshot, "sync")

    dashboard_path = None
    if args.dashboard:
        dashboard_path = write_dashboard(snapshot, diagnostics, write_checklist_doc=False)

    receipt_data = receipt_payload(snapshot, node_ids=node_ids, limit=args.limit)
    receipt_data["automation_core"] = automation_core
    receipt_path = None
    if args.receipt:
        receipt_path = write_receipt(receipt_data)
        receipt_data["receipt_path"] = rel(receipt_path)

    brief_data = brief_payload(snapshot, diagnostics, require_verify=True, limit=args.limit)
    brief_data["automation_core"] = automation_core
    brief_path = None
    if args.brief:
        brief_path = write_brief(brief_data)
        brief_data["brief_path"] = rel(brief_path)

    checklist_data = None
    checklist_path = None
    if args.checklist and apply_results and write_result_table and dashboard_path:
        checklist_data = checklist_payload(
            snapshot,
            diagnostics,
            node_ids=node_ids,
            fail_on="warn",
            require_preflight=True,
            require_verify=True,
            require_results=True,
            limit=args.limit,
        )
        checklist_path = write_checklist(checklist_data)
        checklist_data["checklist_path"] = rel(checklist_path)

    gate = gate_payload(snapshot, diagnostics, fail_on="warn", require_verify=True)
    next_steps = next_steps_payload(snapshot, diagnostics, require_verify=True, limit=args.limit)
    errors = []
    for result in peer_results.values():
        errors.extend(result.get("errors") or [])

    data = {
        "generated_at": snapshot["generated_at"],
        "mode": "sync",
        "dry_run": bool(args.dry_run),
        "apply": apply_results,
        "verify": verify_results,
        "device_id": snapshot["device"]["id"],
        "peers": node_ids,
        "preflight": preflight,
        "status": status_label(snapshot, diagnostics),
        "diagnostics": len(diagnostics),
        "dashboard": rel(dashboard_path) if dashboard_path else None,
        "workflow": rel(workflow_file()) if dashboard_path else None,
        "automation_core_path": rel(automation_core_file()) if dashboard_path else None,
        "automation_core_markdown_path": rel(automation_core_markdown_file()) if dashboard_path else None,
        "acceptance": rel(acceptance_file()) if dashboard_path else None,
        "action_plan": rel(action_plan_file()) if dashboard_path else None,
        "action_plan_markdown": rel(action_plan_markdown_file()) if dashboard_path else None,
        "receipt_path": rel(receipt_path) if receipt_path else None,
        "brief_path": rel(brief_path) if brief_path else None,
        "runbook_path": rel(runbook_file()) if dashboard_path else None,
        "checklist_path": rel(checklist_path) if checklist_path else None,
        "results_table_path": result_table_paths.get("json") if result_table_paths else None,
        "results_csv_path": result_table_paths.get("csv") if result_table_paths else None,
        "results": {
            "written": bool(result_table_paths),
            "summary": (results_data or {}).get("summary"),
            "parse_errors": len((results_data or {}).get("parse_errors") or []),
            "errors": len((results_data or {}).get("errors") or []),
        },
        "automation_core": automation_core,
        "receipt": receipt_data,
        "checklist": checklist_data,
        "gate": {
            "passed": gate["passed"],
            "require_verify": gate["require_verify"],
            "failure_count": gate["failure_count"],
        },
        "next_commands": next_steps.get("commands") or [],
        "peer_results": peer_results,
        "errors": errors,
    }
    if args.json:
        print_json(data)
        return 0 if not errors else 1

    print(f"syncmate sync: {', '.join(node_ids)}")
    print(f"  mode: {'dry-run' if args.dry_run else 'apply'} verify={verify_results}")
    print(
        f"  preflight: {preflight.get('status')} "
        f"ready={((preflight.get('summary') or {}).get('ready', 0))} "
        f"blocked={((preflight.get('summary') or {}).get('blocked', 0))}"
    )
    print(f"  status: {data['status']} diagnostics={data['diagnostics']}")
    if dashboard_path:
        print(f"  dashboard: {rel(dashboard_path)}")
        print(f"  workflow: {rel(workflow_file())}")
        print(f"  acceptance: {rel(acceptance_file())}")
        print(f"  action plan: {rel(action_plan_file())}")
        print(f"  action plan markdown: {rel(action_plan_markdown_file())}")
        print(f"  runbook: {rel(runbook_file())}")
    if receipt_path:
        print(f"  receipt: {rel(receipt_path)}")
    if brief_path:
        print(f"  brief: {rel(brief_path)}")
    if checklist_path:
        print(f"  checklist: {rel(checklist_path)}")
    if result_table_paths:
        summary = (results_data or {}).get("summary") or {}
        print(
            f"  results: {result_table_paths.get('json')} rows={summary.get('rows', 0)} "
            f"parse_errors={summary.get('parse_errors', 0)}"
        )
    core_totals = automation_core.get("totals") or {}
    core_results = automation_core.get("results") or {}
    core_delta = core_results.get("delta") or {}
    print(
        f"  automation: status={automation_core.get('status')} "
        f"missing={core_totals.get('missing', 0)} fetched={core_totals.get('fetched_missing', 0)} "
        f"checksum_verified={core_totals.get('checksum_verified', 0)} "
        f"checksum_failed={core_totals.get('checksum_failed', 0)} "
        f"result_rows={core_results.get('rows', 0)} added_rows={core_delta.get('added_rows', 0)}"
    )
    receipt_summary = receipt_data.get("summary") or {}
    print(
        f"  receipt: accepted={receipt_summary.get('accepted', 0)} "
        f"blocked={receipt_summary.get('blocked', 0)} "
        f"incomplete={receipt_summary.get('incomplete', 0)} "
        f"collected-not-verified={receipt_summary.get('collected_not_verified', 0)}"
    )
    print(f"  gate: {'pass' if gate['passed'] else 'fail'} failures={gate['failure_count']}")
    for node_id, result in peer_results.items():
        remote_errors = len((result.get("remote_status") or {}).get("errors") or [])
        diff_errors = len((result.get("diff") or {}).get("errors") or [])
        collect_errors = len((result.get("collect") or {}).get("errors") or []) if result.get("collect") else 0
        verify_errors = len(verify_result_failures(result.get("verify"))) if result.get("verify") else 0
        state = ((receipt_data.get("peers") or {}).get(node_id) or {}).get("state")
        print(
            f"  - {node_id}: state={state} remote_errors={remote_errors} "
            f"diff_errors={diff_errors} collect_errors={collect_errors} verify_errors={verify_errors}"
        )
    if next_steps.get("commands"):
        print("  next:")
        for item in next_steps["commands"][:max(0, args.limit)]:
            print(f"    {item['command']}")
    if errors:
        print("  errors:")
        for err in errors:
            print(f"    {err}")
    return 0 if not errors else 1


def local_status_snapshot(repo_path: str) -> Dict[str, Any]:
    repo_root = resolve_local_repo_root(repo_path)
    snapshot = {
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "device": {
            "id": repo_root.name or "local-peer",
            "role": "runner",
            "repo_path": str(repo_root),
            "setup_file": ".syncmate/device.yaml",
            "setup_warnings": [],
            "artifact_policy": None,
            "peers": [],
            "peer_configs": {},
        },
        "git": git_state_for_root(repo_root),
        "results": scan_results(repo_root=repo_root),
        "progress": scan_progress(repo_root=repo_root),
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": empty_artifact_index(),
        "export_manifest": None,
        "results_table": None,
        "preflight": None,
    }
    snapshot["fingerprint"] = fingerprint_payload(snapshot)
    return snapshot


def remote_manifest(ssh: str, repo_path: str, roots: List[str],
                    artifact_names: Optional[Tuple[str, ...]] = None,
                    python_executable: str = "python") -> Dict[str, Any]:
    if is_local_transport_ref(ssh):
        return manifest_for_roots(
            roots,
            artifact_names,
            repo_root=resolve_local_repo_root(repo_path),
        )
    cmd = remote_manifest_command(repo_path, roots, artifact_names, python_executable)
    out = subprocess.check_output(["ssh", ssh, cmd], stderr=subprocess.STDOUT)
    return json.loads(out.decode("utf-8", errors="replace"))


def remote_status_snapshot(ssh: str, repo_path: str,
                           python_executable: str = "python") -> Dict[str, Any]:
    if is_local_transport_ref(ssh):
        return local_status_snapshot(repo_path)
    cmd = remote_status_command(repo_path, python_executable)
    out = subprocess.check_output(["ssh", ssh, cmd], stderr=subprocess.STDOUT)
    return json.loads(out.decode("utf-8", errors="replace"))


def remote_status_failure(node_id: str, error: Exception) -> Dict[str, Any]:
    if isinstance(error, subprocess.CalledProcessError):
        msg = error.output.decode("utf-8", errors="replace") if error.output else str(error)
        detail = msg.strip()
    else:
        detail = f"{type(error).__name__}: {error}"
    return {
        "generated_at": now_iso(),
        "node_id": node_id,
        "mode": "apply",
        "errors": [f"remote status failed: {detail}"],
    }


def apply_remote_status(node_id: str, ssh: str, repo_path: str, *,
                        python_executable: str = "python",
                        save: bool = True) -> Dict[str, Any]:
    try:
        snapshot = (
            remote_status_snapshot(ssh, repo_path)
            if python_executable == "python"
            else remote_status_snapshot(ssh, repo_path, python_executable)
        )
    except Exception as e:
        result = remote_status_failure(node_id, e)
        if save:
            return write_sync_report("remote_status", node_id, result)
        return result
    snapshot.setdefault("export_manifest", None)
    snapshot.setdefault("fingerprint", fingerprint_payload(snapshot))
    fingerprint = snapshot.get("fingerprint") or {}

    result = {
        "generated_at": now_iso(),
        "node_id": node_id,
        "mode": "apply",
        "remote": {
            **transport_payload(ssh),
            "repo_path": repo_path,
        },
        "snapshot": snapshot,
        "summary": {
            "device_id": (snapshot.get("device") or {}).get("id"),
            "role": (snapshot.get("device") or {}).get("role"),
            "git_short_sha": (snapshot.get("git") or {}).get("short_sha"),
            "git_dirty": (snapshot.get("git") or {}).get("dirty"),
            "result_leaves": (snapshot.get("results") or {}).get("total_leaves", 0),
            "result_nodes": sorted((snapshot.get("results") or {}).get("nodes") or {}),
            "log_files": ((snapshot.get("progress") or {}).get("summary") or {}).get("total_log_files", 0),
            "log_errors": ((snapshot.get("progress") or {}).get("summary") or {}).get("error_logs", 0),
            "latest_log_age": ((snapshot.get("progress") or {}).get("summary") or {}).get("newest_age"),
            "fingerprint": fingerprint.get("token"),
            "fingerprint_components": fingerprint.get("components") or {},
        },
        "errors": [],
    }
    if save:
        write_sync_report("remote_status", node_id, result)
    return result


def print_remote_status_result(result: Dict[str, Any]) -> None:
    print(f"syncmate remote-status apply: {result.get('node_id')}")
    if result.get("errors"):
        for err in result["errors"]:
            print(f"  error: {err}")
        return
    summary = result.get("summary") or {}
    print(f"  device: {summary.get('device_id')} ({summary.get('role')})")
    print(f"  git: {summary.get('git_short_sha')} dirty={summary.get('git_dirty')}")
    if summary.get("fingerprint"):
        print(f"  fingerprint: {summary.get('fingerprint')}")
    print(f"  result leaves: {summary.get('result_leaves')}")
    print(
        f"  logs: total={summary.get('log_files', 0)} "
        f"errors={summary.get('log_errors', 0)} newest={summary.get('latest_log_age', 'unknown')}"
    )
    nodes = ", ".join(summary.get("result_nodes") or []) or "none"
    print(f"  result nodes: {nodes}")
    if result.get("report_path"):
        print(f"  report: {result['report_path']}")


def local_landing_path(landing: str, remote_rel: str) -> Path:
    if not is_safe_repo_relative_path(landing):
        raise SystemExit(f"Unsafe landing path: {landing}")
    parts = Path(remote_rel).parts
    if len(parts) >= 3 and parts[:2] == RUNS_PREFIX:
        stripped = Path(*parts[2:])
    else:
        stripped = Path(remote_rel)
    target = (REPO_ROOT / landing / stripped).resolve()
    landing_root = (REPO_ROOT / landing).resolve()
    try:
        target.relative_to(landing_root)
    except ValueError:
        raise SystemExit(f"Unsafe target path from remote manifest: {remote_rel}")
    return target


def compare_manifest(landing: str, manifest: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    missing: List[Dict[str, Any]] = []
    same: List[Dict[str, Any]] = []
    conflicts: List[Dict[str, Any]] = []
    for item in manifest.get("items", []):
        target = local_landing_path(landing, item["path"])
        if not target.exists():
            missing.append(item)
            continue
        local_hash = sha256_file(target)
        if local_hash == item.get("sha256"):
            same.append(item)
        else:
            conflicts.append({**item, "local_path": rel(target), "local_sha256": local_hash})
    return missing, same, conflicts


def public_manifest_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: item[k] for k in ("path", "size", "sha256") if k in item}


def artifact_index_status(report: Dict[str, Any], report_prefix: str) -> str:
    summary = report.get("summary") or {}
    errors = report.get("errors") or []
    failed = report.get("verification_failed") or []
    conflicts = summary.get("conflicts", len(report.get("conflicts") or []))
    missing = summary.get("missing", len(report.get("missing") or []))
    remote_incomplete = summary.get("remote_incomplete", 0)
    if errors or failed or remote_incomplete:
        return "incomplete"
    if report_prefix == "last_verify":
        return "verified" if not missing and not conflicts else "incomplete"
    if conflicts:
        return "partial"
    return "collected"


def update_artifact_index(node_id: str, landing: str, report: Dict[str, Any],
                          verified_items: List[Dict[str, Any]],
                          report_prefix: str) -> Path:
    timestamp = now_iso()
    entries = []
    remote_git = ((report.get("remote") or {}).get("git") or {})
    for item in sorted(verified_items, key=lambda value: value.get("path", "")):
        remote_path = item.get("path")
        if not remote_path:
            continue
        target = local_landing_path(landing, remote_path)
        entry = public_manifest_item(item)
        entry.update({
            "source_node": node_id,
            "remote_path": remote_path,
            "local_path": rel(target),
            "verified_at": timestamp,
            "remote_git": remote_git,
        })
        if "mtime_ns" in item:
            entry["remote_mtime_ns"] = item["mtime_ns"]
        entries.append(entry)

    index = load_artifact_index()
    if index.get("errors"):
        index = empty_artifact_index()
    summary = report.get("summary") or {}
    report_path = rel(SYNC_DIR / f"{report_prefix}_{node_id}.json")
    index.setdefault("peers", {})[node_id] = {
        "node_id": node_id,
        "updated_at": timestamp,
        "landing": landing,
        "artifact_policy": report.get("artifact_policy") or {},
        "remote": report.get("remote") or {},
        "source_report": report_path,
        "summary": {
            "remote_files": summary.get("remote_files", len(verified_items)),
            "remote_leaves": summary.get("remote_leaves", 0),
            "remote_incomplete": summary.get("remote_incomplete", 0),
            "indexed": len(entries),
            "missing": summary.get("missing", len(report.get("missing") or [])),
            "conflicts": summary.get("conflicts", len(report.get("conflicts") or [])),
            "errors": len(report.get("errors") or []),
            "status": artifact_index_status(report, report_prefix),
        },
        "items": entries,
    }
    index["version"] = 0
    index["updated_at"] = timestamp
    index["errors"] = []
    return write_artifact_index(index)


def collect_diff_payload(node_id: str, ssh: str, repo_path: str, roots: List[str],
                         landing: str, artifact_names: Optional[Tuple[str, ...]] = None,
                         python_executable: str = "python"
                         ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    names = artifact_names or ARTIFACT_NAMES
    manifest = (
        remote_manifest(ssh, repo_path, roots, names)
        if python_executable == "python"
        else remote_manifest(ssh, repo_path, roots, names, python_executable)
    )
    missing, same, conflicts = compare_manifest(landing, manifest)
    items = manifest.get("items", [])
    remote_inventory = manifest.get("inventory") or manifest_inventory_from_items(items, names)
    inventory_summary = remote_inventory.get("summary") or {}
    payload = {
        "generated_at": now_iso(),
        "node_id": node_id,
        "mode": "diff",
        "landing": landing,
        "artifact_policy": artifact_policy_payload(names),
        "remote": {
            **transport_payload(ssh),
            "repo_path": repo_path,
            "roots": roots,
            "git": manifest.get("git"),
            "count": manifest.get("count"),
        },
        "summary": {
            "remote_files": len(items),
            "remote_leaves": inventory_summary.get("leaves", 0),
            "remote_incomplete": inventory_summary.get("incomplete", 0),
            "already_current": len(same),
            "missing": len(missing),
            "conflicts": len(conflicts),
            "to_fetch": len(missing),
            "will_overwrite": 0,
        },
        "remote_inventory": remote_inventory,
        "missing": [public_manifest_item(item) for item in missing],
        "conflicts": conflicts,
        "errors": [],
    }
    return payload, missing, same, conflicts


def remote_manifest_failure(node_id: str, error: Exception) -> Dict[str, Any]:
    if isinstance(error, subprocess.CalledProcessError):
        msg = error.output.decode("utf-8", errors="replace") if error.output else str(error)
        detail = msg.strip()
    else:
        detail = f"{type(error).__name__}: {error}"
    return {
        "generated_at": now_iso(),
        "node_id": node_id,
        "errors": [f"remote manifest failed: {detail}"],
    }


def diff_collect(node_id: str, ssh: str, repo_path: str, roots: List[str],
                 landing: str, *, artifact_names: Optional[Tuple[str, ...]] = None,
                 python_executable: str = "python",
                 save: bool = True) -> Dict[str, Any]:
    try:
        payload, _missing, _same, _conflicts = collect_diff_payload(
            node_id, ssh, repo_path, roots, landing, artifact_names, python_executable
        )
    except Exception as e:
        result = {**remote_manifest_failure(node_id, e), "mode": "diff", "landing": landing}
        if save:
            return write_sync_report("last_diff", node_id, result)
        return result
    if save:
        write_sync_report("last_diff", node_id, payload)
    return payload


def verify_collect(node_id: str, ssh: str, repo_path: str, roots: List[str],
                   landing: str, *, artifact_names: Optional[Tuple[str, ...]] = None,
                   python_executable: str = "python",
                   save: bool = True) -> Dict[str, Any]:
    try:
        payload, missing, same, conflicts = collect_diff_payload(
            node_id, ssh, repo_path, roots, landing, artifact_names, python_executable
        )
    except Exception as e:
        result = {**remote_manifest_failure(node_id, e), "mode": "verify", "landing": landing}
        if save:
            return write_sync_report("last_verify", node_id, result)
        return result

    payload["mode"] = "verify"
    remote_incomplete = int((payload.get("summary") or {}).get("remote_incomplete") or 0)
    payload["summary"].update({
        "verified_current": len(same),
        "status": "verified" if not missing and not conflicts and not remote_incomplete else "incomplete",
    })
    payload["verified"] = [public_manifest_item(item) for item in same]
    if save:
        index_path = update_artifact_index(node_id, landing, payload, same, "last_verify")
        payload["artifact_index"] = rel(index_path)
        write_sync_report("last_verify", node_id, payload)
    return payload


def source_file_from_local_manifest(repo_root: Path, remote_rel: str) -> Path:
    source = (repo_root / remote_rel).resolve()
    try:
        source.relative_to(repo_root)
    except ValueError:
        raise SystemExit(f"Unsafe local source path from manifest: {remote_rel}")
    return source


def fetch_items_local(repo_path: str, items: List[Dict[str, Any]], landing: str) -> List[Dict[str, Any]]:
    if not items:
        return []
    repo_root = resolve_local_repo_root(repo_path)
    fetched = []
    for item in items:
        remote_rel = item.get("path")
        if not remote_rel:
            continue
        source = source_file_from_local_manifest(repo_root, remote_rel)
        if not source.is_file():
            continue
        target = local_landing_path(landing, remote_rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        fetched.append({"path": remote_rel, "local_path": rel(target)})
    return fetched


def fetch_items(ssh: str, repo_path: str, items: List[Dict[str, Any]], landing: str) -> List[Dict[str, Any]]:
    if not items:
        return []
    if is_local_transport_ref(ssh):
        return fetch_items_local(repo_path, items, landing)

    landing_root = (REPO_ROOT / landing).resolve()
    landing_root.mkdir(parents=True, exist_ok=True)
    file_list = "".join(item["path"] + "\n" for item in items).encode("utf-8")
    expected = {item["path"]: item for item in items}
    cmd = remote_tar_command(repo_path)
    proc = subprocess.Popen(
        ["ssh", ssh, cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None
    assert proc.stdout is not None
    proc.stdin.write(file_list)
    proc.stdin.close()

    fetched = []
    with tarfile.open(fileobj=proc.stdout, mode="r|gz") as tf:
        for member in tf:
            if not member.isfile():
                continue
            remote_rel = member.name.replace("\\", "/")
            if remote_rel not in expected:
                continue
            target = local_landing_path(landing, remote_rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            with target.open("wb") as out:
                shutil.copyfileobj(src, out)
            fetched.append({"path": remote_rel, "local_path": rel(target)})

    stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"remote tar failed rc={rc}: {stderr.strip()}")
    return fetched


def apply_collect(node_id: str, ssh: str, repo_path: str, roots: List[str],
                  landing: str, *, artifact_names: Optional[Tuple[str, ...]] = None,
                  python_executable: str = "python",
                  overwrite: bool = False, save: bool = True) -> Dict[str, Any]:
    errors: List[str] = []
    ensure_sync_dir()
    try:
        report, missing, same, conflicts = collect_diff_payload(
            node_id, ssh, repo_path, roots, landing, artifact_names, python_executable
        )
    except Exception as e:
        result = {**remote_manifest_failure(node_id, e), "mode": "apply", "landing": landing}
        if save:
            return write_sync_report("last_collect", node_id, result)
        return result

    to_fetch = list(missing)
    if overwrite:
        to_fetch += [{k: v for k, v in item.items() if k not in ("local_path", "local_sha256")}
                     for item in conflicts]

    fetched: List[Dict[str, Any]] = []
    if to_fetch:
        try:
            fetched = fetch_items(ssh, repo_path, to_fetch, landing)
        except Exception as e:
            errors.append(f"fetch failed: {type(e).__name__}: {e}")

    verified = []
    verification_failed = []
    for item in to_fetch:
        target = local_landing_path(landing, item["path"])
        if target.exists() and sha256_file(target) == item.get("sha256"):
            verified.append(item["path"])
        else:
            verification_failed.append(item["path"])
    if verification_failed:
        errors.append(f"checksum failed for {len(verification_failed)} file(s)")

    fetched_paths = {item.get("path") for item in fetched}
    missing_paths = {item.get("path") for item in missing}
    conflict_paths = {item.get("path") for item in conflicts}
    fetched_missing = len([path for path in fetched_paths if path in missing_paths])
    overwritten = len([path for path in fetched_paths if path in conflict_paths]) if overwrite else 0
    report["mode"] = "apply"
    report["summary"].update({
        "missing_fetched": fetched_missing,
        "to_fetch": len(to_fetch),
        "fetched": len(fetched),
        "overwritten": overwritten,
        "will_overwrite": len(conflicts) if overwrite else 0,
        "verified": len(verified),
        "verification_failed": len(verification_failed),
    })
    report["conflicts"] = conflicts
    report["fetched"] = fetched
    report["verification_failed"] = verification_failed
    report["errors"] = errors
    if save:
        verified_paths = set(verified)
        verified_items = list(same) + [item for item in to_fetch if item.get("path") in verified_paths]
        index_path = update_artifact_index(node_id, landing, report, verified_items, "last_collect")
        report["artifact_index"] = rel(index_path)
        write_sync_report("last_collect", node_id, report)
    return report


def print_collect_diff(result: Dict[str, Any]) -> None:
    print(f"syncmate collect diff: {result.get('node_id')}")
    if result.get("errors"):
        for err in result["errors"]:
            print(f"  error: {err}")
        return
    summary = result.get("summary") or {}
    policy = result.get("artifact_policy") or {}
    print(f"  landing: {result.get('landing')}")
    if policy.get("include"):
        print(f"  artifacts: {', '.join(policy['include'])}")
    print(f"  remote files: {summary.get('remote_files', 0)}")
    print(f"  remote leaves: {summary.get('remote_leaves', 0)}")
    print(f"  remote incomplete leaves: {summary.get('remote_incomplete', 0)}")
    print(f"  already current: {summary.get('already_current', 0)}")
    print(f"  missing to fetch: {summary.get('missing', 0)}")
    print(f"  conflicts: {summary.get('conflicts', 0)}")
    for item in (result.get("missing") or [])[:5]:
        print(f"    + {item.get('path')}")
    if len(result.get("missing") or []) > 5:
        print(f"    ... {len(result['missing']) - 5} more")
    if result.get("conflicts"):
        print("  conflict policy: checksum-mismatched local files will not be overwritten by default")
    if result.get("report_path"):
        print(f"  report: {result['report_path']}")


def print_collect_result(result: Dict[str, Any]) -> None:
    print(f"syncmate collect apply: {result.get('node_id')}")
    if result.get("errors"):
        for err in result["errors"]:
            print(f"  error: {err}")
    summary = result.get("summary") or {}
    policy = result.get("artifact_policy") or {}
    if summary:
        if policy.get("include"):
            print(f"  artifacts: {', '.join(policy['include'])}")
        print(f"  remote files: {summary.get('remote_files', 0)}")
        print(f"  remote leaves: {summary.get('remote_leaves', 0)}")
        print(f"  remote incomplete leaves: {summary.get('remote_incomplete', 0)}")
        print(f"  already current: {summary.get('already_current', 0)}")
        print(f"  to fetch: {summary.get('to_fetch', 0)}")
        print(f"  fetched total: {summary.get('fetched', summary.get('missing_fetched', 0))}")
        print(f"  fetched missing: {summary.get('missing_fetched', 0)}")
        print(f"  conflicts: {summary.get('conflicts', 0)}")
        print(f"  verified: {summary.get('verified', 0)}")
        if summary.get("verification_failed"):
            print(f"  checksum failed: {summary.get('verification_failed', 0)}")
    if result.get("conflicts"):
        print("  conflict policy: existing mismatched files were not overwritten")
        print("  rerun with --overwrite if these changed artifacts are intentional")
    if result.get("report_path"):
        print(f"  report: {result['report_path']}")


def print_verify_result(result: Dict[str, Any]) -> None:
    print(f"syncmate verify apply: {result.get('node_id')}")
    if result.get("errors"):
        for err in result["errors"]:
            print(f"  error: {err}")
    summary = result.get("summary") or {}
    policy = result.get("artifact_policy") or {}
    if policy.get("include"):
        print(f"  artifacts: {', '.join(policy['include'])}")
    print(f"  landing: {result.get('landing')}")
    print(f"  remote files: {summary.get('remote_files', 0)}")
    print(f"  remote leaves: {summary.get('remote_leaves', 0)}")
    print(f"  remote incomplete leaves: {summary.get('remote_incomplete', 0)}")
    print(f"  verified current: {summary.get('verified_current', summary.get('already_current', 0))}")
    print(f"  missing: {summary.get('missing', len(result.get('missing') or []))}")
    print(f"  conflicts: {summary.get('conflicts', len(result.get('conflicts') or []))}")
    print(f"  status: {summary.get('status', 'unknown')}")
    if result.get("report_path"):
        print(f"  report: {result['report_path']}")


def verify_result_failures(result: Optional[Dict[str, Any]]) -> List[str]:
    if not result:
        return []
    failures = list(result.get("errors") or [])
    summary = result.get("summary") or {}
    missing_count = summary.get("missing", len(result.get("missing") or []))
    conflict_count = summary.get("conflicts", len(result.get("conflicts") or []))
    remote_incomplete = int(summary.get("remote_incomplete") or 0)
    if missing_count or conflict_count:
        failures.append(f"verification incomplete: missing={missing_count}, conflicts={conflict_count}")
    if remote_incomplete:
        failures.append(f"remote inventory incomplete: leaves={remote_incomplete}")
    if summary.get("status") and summary.get("status") != "verified":
        failures.append(f"verification status is {summary.get('status')!r}")
    return failures


def cmd_integrate(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    commands = [
        "python scripts/aggregate_phase_b.py",
        "python scripts/dashboard/gen_config_inventory.py",
    ]
    data = {
        "generated_at": snapshot["generated_at"],
        "mode": "plan-only",
        "device_id": snapshot["device"]["id"],
        "result_nodes": sorted(snapshot["results"]["nodes"]),
        "commands": commands,
        "notes": [
            "Run aggregate only after reviewing node issues in syncmate status.",
            "Dashboard refresh may create tracked diffs; review before committing.",
        ],
    }
    if args.write_state:
        write_state(snapshot, "integrate")
    if args.json:
        print_json(data)
        return 0
    print("syncmate integrate plan")
    nodes = ", ".join(data["result_nodes"]) if data["result_nodes"] else "none"
    print(f"  nodes: {nodes}")
    print("  suggested local commands:")
    for command in commands:
        print(f"    {command}")
    for note in data["notes"]:
        print(f"  note: {note}")
    if args.write_state:
        print(f"  wrote: {rel(STATE_FILE)}")
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    roots = args.roots or ["results/runs"]
    artifact_names = tuple(normalize_artifact_names(args.include)) if args.include else ARTIFACT_NAMES
    data = manifest_for_roots(roots, artifact_names)
    if args.json:
        print_json(data)
        return 0
    print(f"syncmate manifest: {data['count']} file(s)")
    print(f"  roots: {', '.join(roots)}")
    print(f"  artifacts: {', '.join(artifact_names)}")
    inventory_summary = (data.get("inventory") or {}).get("summary") or {}
    print(
        f"  leaves: {inventory_summary.get('leaves', 0)} "
        f"complete={inventory_summary.get('complete', 0)} "
        f"incomplete={inventory_summary.get('incomplete', 0)}"
    )
    print(f"  git: {data['git']['branch']} @ {data['git']['short_sha']} dirty={data['git']['dirty']}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    snapshot = build_snapshot(device, warnings)
    diagnostics = diagnostics_for_snapshot(snapshot)
    if args.write_state:
        write_state(snapshot, "dashboard")
    out = write_dashboard(snapshot, diagnostics)
    data = {
        "generated_at": snapshot["generated_at"],
        "device_id": snapshot["device"]["id"],
        "status": status_label(snapshot, diagnostics),
        "dashboard": rel(out),
        "workflow": rel(workflow_file()),
        "automation_core": rel(automation_core_file()),
        "automation_core_markdown": rel(automation_core_markdown_file()),
        "acceptance": rel(acceptance_file()),
        "action_plan": rel(action_plan_file()),
        "action_plan_markdown": rel(action_plan_markdown_file()),
        "checklist": rel(checklist_file()),
        "runbook": rel(runbook_file()),
        "diagnostics": len(diagnostics),
        "remote_reports": len(snapshot.get("remote_status") or {}),
        "bundle_inspect_reports": len(snapshot.get("bundle_inspect_reports") or {}),
        "diff_reports": len(snapshot.get("diff_reports") or {}),
        "collect_reports": len(snapshot.get("collect_reports") or {}),
        "verify_reports": len(snapshot.get("verify_reports") or {}),
        "indexed_artifacts": artifact_index_total(snapshot.get("artifact_index") or {}),
    }
    if args.json:
        print_json(data)
    else:
        print(f"syncmate dashboard: {data['dashboard']}")
        print(f"  workflow: {data['workflow']}")
        print(f"  automation core: {data['automation_core']}")
        print(f"  automation core markdown: {data['automation_core_markdown']}")
        print(f"  acceptance: {data['acceptance']}")
        print(f"  action plan: {data['action_plan']}")
        print(f"  action plan markdown: {data['action_plan_markdown']}")
        print(f"  checklist: {data['checklist']}")
        print(f"  runbook: {data['runbook']}")
        print(f"  status: {data['status']}")
        print(f"  diagnostics: {data['diagnostics']}")
        print(
            f"  reports: remote={data['remote_reports']} bundle={data['bundle_inspect_reports']} "
            f"diff={data['diff_reports']} collect={data['collect_reports']} verify={data['verify_reports']}"
        )
        print(f"  indexed artifacts: {data['indexed_artifacts']}")
        if args.write_state:
            print(f"  wrote: {rel(STATE_FILE)}")
    if args.open:
        webbrowser.open(out.resolve().as_uri())
    return 0


def unique_child_dir(parent: Path, prefix: str) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = parent / f"{prefix}-{stamp}"
    if not base.exists():
        return base
    for idx in range(1, 1000):
        candidate = parent / f"{prefix}-{stamp}-{idx}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not allocate {prefix} directory under {parent}")


def write_json_artifact(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_smoke_runner_artifacts(runner_root: Path) -> Dict[str, Any]:
    leaf_rel = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    leaf = runner_root / leaf_rel
    attack = {
        "results": {
            "im": {
                "f1_after": 0.72,
                "mia_auc": 0.61,
                "unlearn_time": 1.25,
                "selection_time": 0.33,
                "selection_cache_hit": False,
                "selected_nodes": [1, 3, 5],
            }
        }
    }
    collateral = {
        "results": [
            {
                "strategy": "im",
                "perf_before": 0.81,
                "gap": 0.04,
                "prediction_shift": 0.08,
            }
        ]
    }
    meta = {
        "git_sha": "smoke1234567890",
        "hostname": "syncmate-smoke-runner",
        "timestamp": now_iso(),
    }
    write_json_artifact(leaf / "attack.json", attack)
    write_json_artifact(leaf / "collateral.json", collateral)
    write_json_artifact(leaf / "_meta.json", meta)
    return {
        "leaf": leaf_rel,
        "artifacts": ["attack.json", "collateral.json", "_meta.json"],
    }


def syncmate_runtime_paths() -> Dict[str, Path]:
    return {
        "REPO_ROOT": REPO_ROOT,
        "SYNC_DIR": SYNC_DIR,
        "DEFAULT_DEVICE_FILE": DEFAULT_DEVICE_FILE,
        "STATE_FILE": STATE_FILE,
        "STATUS_HTML": STATUS_HTML,
        "RESULTS_RUNS": RESULTS_RUNS,
    }


def set_runtime_repo_root(repo_root: Path) -> None:
    global REPO_ROOT, SYNC_DIR, DEFAULT_DEVICE_FILE, STATE_FILE, STATUS_HTML, RESULTS_RUNS
    REPO_ROOT = repo_root
    SYNC_DIR = REPO_ROOT / ".syncmate"
    DEFAULT_DEVICE_FILE = SYNC_DIR / "device.yaml"
    STATE_FILE = SYNC_DIR / "state.json"
    STATUS_HTML = SYNC_DIR / "status.html"
    RESULTS_RUNS = REPO_ROOT / "results" / "runs"


def restore_runtime_paths(paths: Dict[str, Path]) -> None:
    global REPO_ROOT, SYNC_DIR, DEFAULT_DEVICE_FILE, STATE_FILE, STATUS_HTML, RESULTS_RUNS
    REPO_ROOT = paths["REPO_ROOT"]
    SYNC_DIR = paths["SYNC_DIR"]
    DEFAULT_DEVICE_FILE = paths["DEFAULT_DEVICE_FILE"]
    STATE_FILE = paths["STATE_FILE"]
    STATUS_HTML = paths["STATUS_HTML"]
    RESULTS_RUNS = paths["RESULTS_RUNS"]


def smoke_workspace(args: argparse.Namespace) -> Tuple[Path, bool]:
    if args.workdir:
        return unique_child_dir(args.workdir.resolve(), "syncmate-smoke"), False
    return Path(tempfile.mkdtemp(prefix="syncmate-smoke-")).resolve(), True


def smoke_payload(args: argparse.Namespace) -> Dict[str, Any]:
    work_root, temporary = smoke_workspace(args)
    collector_root = work_root / "collector"
    runner_root = work_root / "runner"
    collector_root.mkdir(parents=True, exist_ok=True)
    runner_root.mkdir(parents=True, exist_ok=True)
    sample = write_smoke_runner_artifacts(runner_root)
    original_paths = syncmate_runtime_paths()
    node_id = "local-runner"
    landing = f"results/runs/{node_id}"
    errors: List[str] = []
    cleaned = False

    try:
        set_runtime_repo_root(collector_root)
        config = build_device_config("smoke-collector", "collector", str(collector_root))
        peer = build_peer_config(
            "runner",
            None,
            str(runner_root),
            landing,
            ["results/runs"],
            transport="local",
        )
        add_peer_to_device(config, node_id, peer)
        write_device_config(DEFAULT_DEVICE_FILE, config, force=True)

        preflight = preflight_payload(
            config,
            [],
            config_path=DEFAULT_DEVICE_FILE,
            node_ids=[node_id],
            require_sync_targets=True,
        )
        write_preflight_report(preflight)
        ssh = transport_ssh_value(peer)
        roots = peer.get("result_roots") or ["results/runs"]
        artifact_names = artifact_names_for_peer(config, peer)
        diff = diff_collect(node_id, ssh, str(runner_root), roots, landing,
                            artifact_names=artifact_names, save=True)
        collect = apply_collect(node_id, ssh, str(runner_root), roots, landing,
                                artifact_names=artifact_names, save=True)
        verify = verify_collect(node_id, ssh, str(runner_root), roots, landing,
                                artifact_names=artifact_names, save=True)
        index = load_artifact_index()
        results_data = results_payload_from_index(index, node_ids=[node_id], include_incomplete=False)
        written_results = write_results_table_files(results_data)
        results_data["written"] = written_results
        snapshot = build_snapshot(config, [])
        diagnostics = diagnostics_for_snapshot(snapshot)
        dashboard_path = write_dashboard(snapshot, diagnostics)
        checklist_data = checklist_payload(
            snapshot,
            diagnostics,
            node_ids=[node_id],
            require_preflight=True,
            require_verify=True,
            require_results=True,
        )
        checklist_path = write_checklist(checklist_data)
        receipt_data = receipt_payload(snapshot, node_ids=[node_id])
        receipt_path = write_receipt(receipt_data)
        local_attack = local_landing_path(landing, f"{sample['leaf']}/attack.json")
        checklist_text = checklist_path.read_text(encoding="utf-8")
        runbook_path = runbook_file()
        runbook_text = runbook_path.read_text(encoding="utf-8") if runbook_path.is_file() else ""
        action_plan_path = action_plan_file()
        action_plan_markdown_path = action_plan_markdown_file()
        action_plan = (
            json.loads(action_plan_path.read_text(encoding="utf-8-sig"))
            if action_plan_path.is_file() else {}
        )
        automation_core_markdown_path = automation_core_markdown_file()
        automation_core_markdown = (
            automation_core_markdown_path.read_text(encoding="utf-8")
            if automation_core_markdown_path.is_file() else ""
        )
        checks = {
            "preflight_ready": preflight.get("status") == "ready",
            "diff_found_missing": (diff.get("summary") or {}).get("missing") == len(sample["artifacts"]),
            "collect_fetched_missing": (collect.get("summary") or {}).get("missing_fetched") == len(sample["artifacts"]),
            "collect_checksum_ok": not collect.get("verification_failed") and not collect.get("errors"),
            "verify_status": (verify.get("summary") or {}).get("status") == "verified",
            "trusted_results_rows": (results_data.get("summary") or {}).get("rows", 0) >= 1,
            "trusted_results_parse_clean": (results_data.get("summary") or {}).get("parse_errors", 0) == 0,
            "checklist_written": checklist_path.is_file() and ".syncmate/acceptance.json" in checklist_text,
            "runbook_written": runbook_path.is_file() and "python scripts/syncmate/syncmate.py sync local-runner" in runbook_text,
            "action_plan_written": (
                action_plan_path.is_file()
                and action_plan_markdown_path.is_file()
                and action_plan.get("mode") == "next"
            ),
            "automation_core_markdown_written": (
                automation_core_markdown_path.is_file()
                and "Syncmate Automation Core" in automation_core_markdown
            ),
            "local_artifact_exists": local_attack.is_file(),
        }
        passed = all(checks.values())
        data = {
            "generated_at": now_iso(),
            "mode": "smoke",
            "passed": passed,
            "kept": bool(args.keep or not temporary),
            "temporary": temporary,
            "workdir": str(work_root),
            "collector_root": str(collector_root),
            "runner_root": str(runner_root),
            "node_id": node_id,
            "landing": landing,
            "sample": sample,
            "checks": checks,
            "summary": {
                "diff_missing": (diff.get("summary") or {}).get("missing", 0),
                "collected": (collect.get("summary") or {}).get("missing_fetched", 0),
                "verified": (verify.get("summary") or {}).get("verified_current", 0),
                "indexed": artifact_index_total(index),
                "result_rows": (results_data.get("summary") or {}).get("rows", 0),
                "parse_errors": (results_data.get("summary") or {}).get("parse_errors", 0),
            },
            "files": {
                "device": rel(DEFAULT_DEVICE_FILE),
                "preflight": rel(last_preflight_file()),
                "diff": diff.get("report_path"),
                "collect": collect.get("report_path"),
                "verify": verify.get("report_path"),
                "artifact_index": rel(artifact_index_file()),
                "results_json": written_results.get("json"),
                "results_csv": written_results.get("csv"),
                "dashboard": rel(dashboard_path),
                "automation_core": rel(automation_core_file()),
                "automation_core_markdown": rel(automation_core_markdown_file()),
                "acceptance": rel(acceptance_file()),
                "action_plan": rel(action_plan_path),
                "action_plan_markdown": rel(action_plan_markdown_path),
                "checklist": rel(checklist_path),
                "runbook": rel(runbook_path),
                "receipt": rel(receipt_path),
                "local_attack": rel(local_attack),
            },
            "errors": errors,
        }
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        data = {
            "generated_at": now_iso(),
            "mode": "smoke",
            "passed": False,
            "kept": True,
            "temporary": temporary,
            "workdir": str(work_root),
            "collector_root": str(collector_root),
            "runner_root": str(runner_root),
            "node_id": node_id,
            "landing": landing,
            "sample": sample,
            "checks": {},
            "summary": {},
            "files": {},
            "errors": errors,
        }
    finally:
        restore_runtime_paths(original_paths)

    if temporary and not args.keep and data.get("passed"):
        shutil.rmtree(work_root, ignore_errors=True)
        cleaned = True
    data["cleaned"] = cleaned
    if cleaned:
        data["kept"] = False
    return data


def runner_preflight_leaf() -> Path:
    """Return the deliberately isolated no-GPU runner-agent evidence leaf."""
    return RESULTS_RUNS / "__syncmate_preflight__" / "opengu_preflight" / "seed0"


def runner_preflight_payload(recipe: str) -> Dict[str, Any]:
    """Create only schema-valid, clearly marked preflight evidence.

    This is intentionally *not* an OpenGU experiment invocation.  It binds the
    declared experiment configuration and proves the controller's normal
    collection/verification path without consuming a GPU or changing cache
    semantics.
    """
    if recipe != "opengu-preflight-v1":
        return {"passed": False, "recipe": recipe, "errors": ["unsupported runner preflight recipe"]}
    binding = runner_recipe_binding(recipe)
    if not binding.get("ready"):
        return {"passed": False, "recipe": recipe, "binding": binding, "errors": binding.get("errors") or []}
    leaf = runner_preflight_leaf()
    expected = list((runner_recipe_definition(recipe) or {}).get("expected_artifact_paths") or [])
    existing = [path for path in expected if (REPO_ROOT / path).exists()]
    if existing:
        return {
            "passed": False,
            "recipe": recipe,
            "binding": binding,
            "generated_artifacts": [],
            "errors": ["preflight evidence already exists; no artifact was overwritten: " + ", ".join(existing)],
        }
    try:
        git_sha = run_git(["rev-parse", "HEAD"]) or "unknown"
    except Exception:
        git_sha = "unknown"
    attack = {
        "results": {
            "opengu_preflight": {
                "f1_after": 1.0,
                "mia_auc": 0.5,
                "unlearn_time": 0.0,
                "selection_time": 0.0,
                "selected_nodes": [],
            }
        }
    }
    collateral = {"results": [{"strategy": "opengu_preflight", "perf_before": 1.0, "gap": 0.0, "prediction_shift": 0.0}]}
    meta = {
        "git_sha": git_sha,
        "hostname": socket.gethostname(),
        "timestamp": now_iso(),
        "syncmate_runner_preflight": True,
        "recipe": recipe,
        "config_path": binding["expected"]["config_path"],
        "config_sha256": binding["expected"]["config_sha256"],
        "note": "Synthetic bounded-runner evidence only; no OpenGU experiment or cache operation was run.",
    }
    write_json_artifact(leaf / "attack.json", attack)
    write_json_artifact(leaf / "collateral.json", collateral)
    write_json_artifact(leaf / "_meta.json", meta)
    generated = [rel(leaf / name) for name in ("attack.json", "collateral.json", "_meta.json")]
    passed = generated == expected
    return {
        "passed": passed,
        "recipe": recipe,
        "binding": binding,
        "generated_artifacts": generated,
        "errors": [] if passed else ["generated artifact paths did not match the immutable recipe declaration"],
    }


def cmd_runner_preflight(args: argparse.Namespace) -> int:
    data = runner_preflight_payload(args.recipe)
    if args.json:
        print_json(data)
    else:
        print(f"runner preflight: {'passed' if data.get('passed') else 'failed'}")
        for path in data.get("generated_artifacts") or []:
            print(f"  artifact: {path}")
        for error in data.get("errors") or []:
            print(f"  error: {error}")
    return 0 if data.get("passed") else 1


def runner_queue_root() -> Path:
    return SYNC_DIR / "runner_queue"


def runner_queue_state_dir(state: str) -> Path:
    if state not in QUEUE_STATES:
        raise ValueError(f"unknown runner queue state: {state}")
    return runner_queue_root() / state


def runner_queue_receipts_dir() -> Path:
    return runner_queue_root() / "receipts"


def runner_queue_results_dir() -> Path:
    return runner_queue_root() / "results"


def runner_queue_manifest_file() -> Path:
    return runner_queue_root() / "manifest.json"


def runner_queue_status_file() -> Path:
    return runner_queue_root() / "status.html"


def runner_queue_contract_file() -> Path:
    return runner_queue_root() / "contract.json"


def runner_agent_lock_dir() -> Path:
    return runner_queue_root() / "agent.lock"


def runner_agent_recovery_file() -> Path:
    return runner_queue_root() / "recovery.jsonl"


def runner_recipe_definition(recipe: str) -> Dict[str, Any]:
    definition = RUNNER_RECIPE_DEFINITIONS.get(recipe)
    if not definition:
        raise ValueError(f"recipe {recipe!r} is not allowlisted")
    return json.loads(json.dumps(definition))


def runner_recipe_command(definition: Dict[str, Any]) -> List[str]:
    return [sys.executable if value == "{python}" else str(value) for value in definition["argv"]]


def _runner_delta_path_allowed(path: str, allowed_paths: Tuple[str, ...]) -> bool:
    return any(
        path.startswith(allowed) if allowed.endswith("/") else path == allowed
        for allowed in allowed_paths
    )


def runner_recipe_git_binding(
    expected_sha: str,
    allowed_delta_paths: Optional[Tuple[str, ...]] = None,
) -> Dict[str, Any]:
    observed_sha = run_git(["rev-parse", "HEAD"])
    data: Dict[str, Any] = {
        "expected_git_sha": expected_sha,
        "observed_git_sha": observed_sha,
        "mode": "exact" if observed_sha == expected_sha else "tooling-delta",
        "ok": observed_sha == expected_sha,
        "changed_paths": [],
        "errors": [],
    }
    if data["ok"]:
        return data
    try:
        ancestor = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "merge-base", "--is-ancestor", expected_sha, observed_sha],
            check=False,
            capture_output=True,
        ).returncode == 0
        changed = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "diff", "--name-only", f"{expected_sha}..{observed_sha}"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace").splitlines()
    except Exception as exc:
        data["errors"].append(f"could not verify Git binding: {type(exc).__name__}: {exc}")
        return data
    data["changed_paths"] = changed
    allowed_paths = (
        tuple(allowed_delta_paths)
        if allowed_delta_paths is not None
        else RUNNER_RECIPE_ALLOWED_TOOL_DELTA
    )
    disallowed = [
        path for path in changed
        if not _runner_delta_path_allowed(path, allowed_paths)
    ]
    if not ancestor:
        data["errors"].append("expected OpenGU baseline is not an ancestor of the runner checkout")
    if disallowed:
        data["errors"].append("runner checkout contains non-tooling commits after the expected baseline: " + ", ".join(disallowed))
    data["ok"] = ancestor and not disallowed
    return data


def runner_recipe_binding(recipe: str) -> Dict[str, Any]:
    definition = runner_recipe_definition(recipe)
    config_rel = str(definition["config_path"])
    config_path = safe_repo_path(config_rel)
    errors: List[str] = []
    observed_config_sha = None
    if config_path is None or not config_path.is_file():
        errors.append(f"fixed recipe config is missing or unsafe: {config_rel}")
    else:
        observed_config_sha = sha256_file(config_path)
        if observed_config_sha != definition["config_sha256"]:
            errors.append("fixed recipe config SHA-256 differs from recipe metadata")
    allowed_delta_paths = definition.get("allowed_git_delta_paths")
    git = runner_recipe_git_binding(
        str(definition["expected_git_sha"]),
        tuple(allowed_delta_paths) if allowed_delta_paths is not None else None,
    )
    errors.extend(git.get("errors") or [])
    return {
        "recipe": definition,
        "expected": {
            "git_sha": definition["expected_git_sha"],
            "config_path": config_rel,
            "config_sha256": definition["config_sha256"],
            "timeout_seconds": definition["timeout_seconds"],
            "artifact_paths": definition["expected_artifact_paths"],
            "collector_acceptance": definition["collector_acceptance"],
        },
        "observed": {
            "git_sha": git.get("observed_git_sha"),
            "config_sha256": observed_config_sha,
            "git_binding_mode": git.get("mode"),
            "git_changed_paths": git.get("changed_paths") or [],
        },
        "git": git,
        "ready": not errors,
        "errors": errors,
    }


def runner_queue_existing_paths(job_id: str) -> Dict[str, str]:
    paths = {
        state: runner_queue_job_path(state, job_id)
        for state in QUEUE_STATES
        if runner_queue_job_path(state, job_id).exists()
    }
    if runner_queue_result_path(job_id).exists():
        paths["result"] = runner_queue_result_path(job_id)
    return {key: runner_queue_rel(path) for key, path in paths.items()}


def runner_queue_duplicate_errors(payload: Dict[str, Any]) -> List[str]:
    return [
        str(error) for error in ((payload.get("validation") or {}).get("errors") or [])
        if str(error).startswith("job id appears in multiple states:")
    ]


def runner_agent_acquire_lock(device_id: str) -> Dict[str, Any]:
    ensure_runner_queue_dirs()
    lock = runner_agent_lock_dir()
    try:
        lock.mkdir()
    except FileExistsError:
        owner = runner_queue_load_json(lock / "owner.json")
        raise RuntimeError(f"runner agent lock already exists: {runner_queue_rel(lock)} owner={owner or 'unknown'}")
    owner = {
        "protocol": QUEUE_PROTOCOL,
        "device_id": device_id,
        "pid": os.getpid(),
        "acquired_at": now_iso(),
    }
    write_runner_queue_json(lock / "owner.json", owner)
    return owner


def runner_agent_release_lock() -> None:
    lock = runner_agent_lock_dir()
    if not lock.exists():
        return
    owner = lock / "owner.json"
    if owner.exists():
        owner.unlink()
    lock.rmdir()


def runner_agent_append_recovery(event: Dict[str, Any]) -> None:
    ensure_runner_queue_dirs()
    data = {"generated_at": now_iso(), **event}
    with runner_agent_recovery_file().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + "\n")


def runner_queue_contract_payload() -> Dict[str, Any]:
    """Return the stable external boundary for optional queue integrations.

    This is deliberately data-only: callers can discover the protocol without
    creating a queue directory or changing runner state.
    """
    return {
        "protocol": QUEUE_PROTOCOL,
        "version": 1,
        "job_schema": {
            "required": ["protocol", "version", "id", "recipe", "created_at"],
            "optional": ["requested_by", "note"],
            "additional_fields": False,
            "id_pattern": QUEUE_ID_RE.pattern,
            "file_name": "<id>.yaml",
        },
        "state_machine": {
            "states": list(QUEUE_STATES),
            "transitions": {
                "submit": ["inbox"],
                "claim": ["inbox", "running"],
                "complete": ["running", "done"],
                "fail": ["running", "failed"],
                "block": ["inbox", "blocked"],
            },
            "owner": "Only runner-queue run --once or runner-agent serve may claim or transition a job.",
        },
        "execution": {
            "mode": "single-shot or bounded runner-agent serve",
            "single_shot_flag": "--once",
            "agent_limit": "one exclusive local lock and one concurrent job",
            "allowlisted_recipes": list(QUEUE_ALLOWED_RECIPES),
            "recipe_inputs": "Jobs select only a recipe id; they cannot provide commands, arguments, paths, or cache operations.",
        },
        "evidence": {
            "job": "inbox|running|done|failed|blocked/<id>.yaml",
            "receipt": "receipts/<id>.json",
            "result": "results/<id>.json",
            "manifest": "manifest.json",
            "dashboard": "status.html",
        },
        "integration": {
            "syncmate": "Keeps collector, checksum verifier, trusted-index, and acceptance-gate authority.",
            "opengu": "May submit or observe declared jobs through this contract; it must not directly mutate queue state or treat a queue result as trusted experiment evidence.",
            "forbidden": [
                "arbitrary shell or Python command fields in job YAML",
                "direct writes to running, done, failed, or blocked",
                "cache deletion, cache invalidation, or result-schema changes through the queue",
                "bypassing SyncMate collection, checksum verification, or gate evidence",
            ],
            "extension_rule": "Adding an OpenGU recipe is a reviewed code change to the static allowlist, with a frozen input schema and dedicated tests; it is not a job-YAML feature flag.",
        },
    }


def ensure_runner_queue_dirs() -> None:
    for state in QUEUE_STATES:
        runner_queue_state_dir(state).mkdir(parents=True, exist_ok=True)
    runner_queue_receipts_dir().mkdir(parents=True, exist_ok=True)
    runner_queue_results_dir().mkdir(parents=True, exist_ok=True)


def runner_queue_safe_id(value: Any) -> bool:
    return isinstance(value, str) and bool(QUEUE_ID_RE.fullmatch(value))


def runner_queue_default_id() -> str:
    return "smoke-" + _dt.datetime.now().strftime("%Y%m%d%H%M%S%f")


def runner_queue_rel(path: Path) -> str:
    return rel(path)


def write_runner_queue_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_runner_queue_yaml(path: Path, data: Dict[str, Any]) -> None:
    if yaml is None:
        raise SystemExit("PyYAML is required. Use the project gnn environment or install pyyaml.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def runner_queue_job_path(state: str, job_id: str) -> Path:
    if not runner_queue_safe_id(job_id):
        raise ValueError(f"unsafe runner queue job id: {job_id!r}")
    return runner_queue_state_dir(state) / f"{job_id}.yaml"


def runner_queue_read_job(path: Path, state: str) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "path": runner_queue_rel(path), "state": state, "valid": False, "errors": [],
    }
    try:
        if yaml is None:
            raise ValueError("PyYAML is unavailable")
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        entry["errors"].append(f"invalid YAML: {type(exc).__name__}: {exc}")
        entry["id"] = path.stem
        return entry
    if not isinstance(raw, dict):
        entry["errors"].append("job must be a YAML mapping")
        entry["id"] = path.stem
        return entry
    entry["job"] = raw
    job_id = raw.get("id")
    entry["id"] = job_id if isinstance(job_id, str) else path.stem
    unknown = sorted(set(raw) - QUEUE_ALLOWED_JOB_FIELDS)
    if unknown:
        entry["errors"].append("unsupported job fields: " + ", ".join(unknown))
    if raw.get("protocol") != QUEUE_PROTOCOL:
        entry["errors"].append(f"protocol must be {QUEUE_PROTOCOL!r}")
    if raw.get("version") != 1:
        entry["errors"].append("version must be 1")
    if not runner_queue_safe_id(job_id):
        entry["errors"].append("id must match [A-Za-z0-9][A-Za-z0-9_.-]{0,80}")
    elif path.name != f"{job_id}.yaml":
        entry["errors"].append("file name must match job id")
    if raw.get("recipe") not in QUEUE_ALLOWED_RECIPES:
        entry["errors"].append("recipe is not allowlisted")
    if not isinstance(raw.get("created_at"), str) or parse_iso_time(raw.get("created_at")) is None:
        entry["errors"].append("created_at must be an ISO-8601 timestamp")
    for field in ("requested_by", "note"):
        if field in raw and (not isinstance(raw[field], str) or len(raw[field]) > 500):
            entry["errors"].append(f"{field} must be a short string")
    entry["recipe"] = raw.get("recipe")
    entry["created_at"] = raw.get("created_at")
    entry["valid"] = not entry["errors"]
    return entry


def runner_queue_receipt_path(job_id: str) -> Path:
    return runner_queue_receipts_dir() / f"{job_id}.json"


def runner_queue_result_path(job_id: str) -> Path:
    return runner_queue_results_dir() / f"{job_id}.json"


def runner_queue_load_json(path: Path) -> Dict[str, Any]:
    value = load_optional_json(path)
    return value if isinstance(value, dict) else {}


def runner_queue_write_receipt(job_id: str, **updates: Any) -> Dict[str, Any]:
    prior = runner_queue_load_json(runner_queue_receipt_path(job_id))
    prior.update(updates)
    prior.setdefault("protocol", QUEUE_PROTOCOL)
    prior.setdefault("job_id", job_id)
    prior["updated_at"] = now_iso()
    write_runner_queue_json(runner_queue_receipt_path(job_id), prior)
    return prior


def runner_queue_job_summary(entry: Dict[str, Any]) -> Dict[str, Any]:
    job_id = str(entry.get("id") or "unknown")
    receipt = runner_queue_load_json(runner_queue_receipt_path(job_id))
    result = runner_queue_load_json(runner_queue_result_path(job_id))
    return {
        "id": job_id,
        "state": entry.get("state"),
        "recipe": entry.get("recipe"),
        "created_at": entry.get("created_at"),
        "valid": bool(entry.get("valid")),
        "errors": entry.get("errors") or [],
        "path": entry.get("path"),
        "receipt": {
            key: receipt.get(key) for key in ("state", "submitted_at", "claimed_at", "started_at", "finished_at", "blocked_at", "runner_id")
            if receipt.get(key) is not None
        },
        "result": {
            key: result.get(key) for key in ("status", "exit_code", "reason", "finished_at", "recipe_passed")
            if result.get(key) is not None
        },
    }


def runner_queue_payload() -> Dict[str, Any]:
    ensure_runner_queue_dirs()
    entries: List[Dict[str, Any]] = []
    errors: List[str] = []
    for state in QUEUE_STATES:
        directory = runner_queue_state_dir(state)
        for path in sorted(directory.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() != ".yaml":
                errors.append(f"unexpected file in {state}: {runner_queue_rel(path)}")
                continue
            entries.append(runner_queue_read_job(path, state))
    ids: Dict[str, List[str]] = defaultdict(list)
    for entry in entries:
        if runner_queue_safe_id(entry.get("id")):
            ids[str(entry["id"])].append(str(entry.get("state")))
    for job_id, states in sorted(ids.items()):
        if len(states) > 1:
            errors.append(f"job id appears in multiple states: {job_id} ({', '.join(states)})")
    jobs = [runner_queue_job_summary(entry) for entry in entries]
    jobs.sort(key=lambda item: (QUEUE_STATES.index(str(item["state"])), str(item["id"])))
    counts = {state: sum(1 for job in jobs if job["state"] == state) for state in QUEUE_STATES}
    invalid = [job for job in jobs if not job["valid"]]
    return {
        "protocol": QUEUE_PROTOCOL,
        "generated_at": now_iso(),
        "paths": {
            "root": runner_queue_rel(runner_queue_root()),
            "manifest": runner_queue_rel(runner_queue_manifest_file()),
            "status": runner_queue_rel(runner_queue_status_file()),
            "receipts": runner_queue_rel(runner_queue_receipts_dir()),
            "results": runner_queue_rel(runner_queue_results_dir()),
        },
        "allowlisted_recipes": list(QUEUE_ALLOWED_RECIPES),
        "counts": counts,
        "jobs": jobs,
        "validation": {"valid": not errors and not invalid, "errors": errors, "invalid_jobs": len(invalid)},
    }


def write_runner_queue_manifest(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = payload or runner_queue_payload()
    data["manifest_path"] = runner_queue_rel(runner_queue_manifest_file())
    write_runner_queue_json(runner_queue_manifest_file(), data)
    return data


def render_runner_queue_status(payload: Dict[str, Any]) -> str:
    counts = payload.get("counts") or {}
    jobs = payload.get("jobs") or []
    validation = payload.get("validation") or {}
    cards = "".join(
        f'<section class="card {state}"><span>{html.escape(state)}</span><strong>{int(counts.get(state, 0))}</strong></section>'
        for state in QUEUE_STATES
    )
    rows = []
    for job in jobs:
        result = job.get("result") or {}
        reason = result.get("reason") or "; ".join(job.get("errors") or []) or "—"
        rows.append(
            "<tr>"
            f'<td><code>{html.escape(str(job.get("id") or "—"))}</code></td>'
            f'<td><span class="pill {html.escape(str(job.get("state") or "unknown"))}">{html.escape(str(job.get("state") or "unknown"))}</span></td>'
            f'<td>{html.escape(str(job.get("recipe") or "—"))}</td>'
            f'<td>{html.escape(str(job.get("created_at") or "—"))}</td>'
            f'<td>{html.escape(str(result.get("exit_code", "—")))}</td>'
            f'<td>{html.escape(str(reason))}</td></tr>'
        )
    table = "\n".join(rows) or '<tr><td colspan="6" class="empty">No jobs yet. Submit an allowlisted smoke job to begin.</td></tr>'
    validation_text = "Protocol valid" if validation.get("valid") else "Protocol needs attention"
    errors = "".join(f"<li>{html.escape(str(error))}</li>" for error in validation.get("errors") or [])
    generated_at = html.escape(str(payload.get("generated_at") or "—"))
    health_class = "ok" if validation.get("valid") else "warn"
    errors_block = "<ul>" + errors + "</ul>" if errors else ""
    template = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SyncMate Runner Queue</title><style>
:root{{color-scheme:dark;--bg:#0b1020;--panel:#141b31;--line:#2c385b;--text:#eef3ff;--muted:#9ba8c7;--blue:#69a7ff;--green:#53d39a;--amber:#f4bd63;--red:#ff7884;--purple:#aa8cff}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 20% -10%,#213565,transparent 35%),var(--bg);color:var(--text);font:15px/1.5 Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1250px;margin:auto;padding:42px 24px 64px}}header{{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:28px}}h1{{margin:0;font-size:32px;letter-spacing:-.03em}}h1 span{{color:var(--blue)}}.sub{{color:var(--muted);margin:7px 0 0}}.stamp{{text-align:right;color:var(--muted);font-size:13px}}.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:22px 0}}.card{{background:linear-gradient(145deg,#18233f,#121a2e);border:1px solid var(--line);border-radius:14px;padding:16px}.card span{{display:block;color:var(--muted);text-transform:uppercase;font-size:11px;letter-spacing:.1em}}.card strong{{font-size:30px}}.card.done strong{{color:var(--green)}}.card.failed strong{{color:var(--red)}}.card.blocked strong{{color:var(--amber)}}.panel{{background:rgba(20,27,49,.88);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin-top:18px}}.panel h2{{font-size:16px;margin:0;padding:16px 18px;border-bottom:1px solid var(--line)}}.ok,.warn{{padding:12px 18px;font-weight:600}}.ok{{color:var(--green)}}.warn{{color:var(--amber)}}ul{{margin:0 18px 16px;color:var(--muted)}}table{{width:100%;border-collapse:collapse;min-width:850px}}.table-wrap{{overflow:auto}}th,td{{padding:13px 16px;text-align:left;border-bottom:1px solid #263252;vertical-align:top}}th{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}}code{{color:#c8dcff;font-family:ui-monospace,Consolas,monospace}}.pill{{display:inline-block;border-radius:99px;padding:2px 9px;font-size:12px;background:#2b3658}}.pill.done{{background:#174635;color:#9bf0c4}}.pill.failed{{background:#5a2732;color:#ffb3bd}}.pill.blocked{{background:#62491d;color:#ffe0a0}}.pill.running{{background:#283d70;color:#bfd3ff}}.empty{{color:var(--muted);text-align:center;padding:28px}}.contract{{color:var(--muted);padding:0 18px 18px}}@media(max-width:760px){{header{{display:block}}.stamp{{text-align:left;margin-top:12px}}.grid{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><main><header><div><h1>SyncMate <span>Runner Queue</span></h1><p class="sub">Local, allowlisted work protocol. SyncMate remains collector, verifier, and gate.</p></div><div class="stamp">Generated __GENERATED_AT__<br>Recipe allowlist: <code>smoke</code></div></header>
<div class="grid">__CARDS__</div><section class="panel"><h2>Protocol health</h2><div class="__HEALTH_CLASS__">__VALIDATION_TEXT__</div>__ERRORS_BLOCK__<p class="contract">Inbox → running → done | failed | blocked. The runner accepts only <code>smoke</code>, which is SyncMate’s temporary local smoke check; it cannot run experiment commands or alter cache semantics.</p></section>
<section class="panel"><h2>Jobs</h2><div class="table-wrap"><table><thead><tr><th>Job</th><th>State</th><th>Recipe</th><th>Created</th><th>Exit</th><th>Result / reason</th></tr></thead><tbody>__TABLE__</tbody></table></div></section>
</main></body></html>"""
    template = template.replace("{{", "{").replace("}}", "}")
    return (template.replace("__GENERATED_AT__", generated_at)
            .replace("__CARDS__", cards)
            .replace("__HEALTH_CLASS__", health_class)
            .replace("__VALIDATION_TEXT__", html.escape(validation_text))
            .replace("__ERRORS_BLOCK__", errors_block)
            .replace("__TABLE__", table))


def write_runner_queue_status(payload: Optional[Dict[str, Any]] = None) -> Path:
    data = payload or runner_queue_payload()
    out = runner_queue_status_file()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_runner_queue_status(data), encoding="utf-8")
    return out


def runner_queue_unique_destination(state: str, job_id: str) -> Path:
    destination = runner_queue_job_path(state, job_id)
    if not destination.exists() and not runner_queue_result_path(job_id).exists():
        return destination
    candidate_id = f"{job_id[:60].rstrip('.-')}-{_dt.datetime.now().strftime('%H%M%S%f')}"
    return runner_queue_job_path(state, candidate_id)


def runner_queue_block_invalid(path: Path, entry: Dict[str, Any], *, binding: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    raw_id = entry.get("id")
    job_id = str(raw_id) if runner_queue_safe_id(raw_id) else f"invalid-{safe_file_stem(path.stem)[:60]}"
    destination = runner_queue_unique_destination("blocked", job_id)
    result_id = destination.stem
    path.replace(destination)
    reason = "; ".join(entry.get("errors") or ["invalid runner queue job"])
    runner_queue_write_receipt(
        result_id,
        state="blocked",
        blocked_at=now_iso(),
        reason=reason,
        recipe_binding=binding,
    )
    result = {
        "protocol": QUEUE_PROTOCOL,
        "job_id": result_id,
        "status": "blocked",
        "reason": reason,
        "finished_at": now_iso(),
        "recipe_binding": binding,
    }
    write_runner_queue_json(runner_queue_result_path(result_id), result)
    return {"job_id": result_id, "state": "blocked", "reason": reason, "path": runner_queue_rel(destination)}


def runner_queue_output_text(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value or "")


def runner_queue_recipe_command(recipe: str) -> Tuple[List[str], int]:
    definition = runner_recipe_definition(recipe)
    return runner_recipe_command(definition), int(definition["timeout_seconds"])


def runner_queue_submit(job_id: str, recipe: str, *, requested_by: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
    ensure_runner_queue_dirs()
    if not runner_queue_safe_id(job_id):
        raise SystemExit("job id must match [A-Za-z0-9][A-Za-z0-9_.-]{0,80}")
    if recipe not in QUEUE_ALLOWED_RECIPES:
        raise SystemExit("recipe is not allowlisted")
    if requested_by is not None and (not isinstance(requested_by, str) or len(requested_by) > 500):
        raise SystemExit("requested_by must be a short string")
    if note is not None and (not isinstance(note, str) or len(note) > 500):
        raise SystemExit("note must be a short string")
    existing = runner_queue_existing_paths(job_id)
    if existing:
        raise SystemExit(f"job id is already reserved by queue evidence: {existing}")
    job = {"protocol": QUEUE_PROTOCOL, "version": 1, "id": job_id, "recipe": recipe, "created_at": now_iso()}
    if requested_by:
        job["requested_by"] = requested_by
    if note:
        job["note"] = note
    path = runner_queue_job_path("inbox", job_id)
    write_runner_queue_yaml(path, job)
    runner_queue_write_receipt(job_id, state="inbox", submitted_at=job["created_at"])
    payload = write_runner_queue_manifest()
    return {"submitted": True, "job": job, "path": runner_queue_rel(path), "manifest": payload["manifest_path"]}


def runner_queue_run_once(config: Dict[str, Any]) -> Dict[str, Any]:
    ensure_runner_queue_dirs()
    role = config.get("role")
    if role not in ("runner", "runner+collector"):
        return {"status": "blocked", "errors": ["runner-queue run requires device role runner or runner+collector"], "processed": False}
    queue = runner_queue_payload()
    duplicates = runner_queue_duplicate_errors(queue)
    if duplicates:
        return {"status": "blocked", "processed": False, "errors": duplicates}
    if queue["counts"]["running"]:
        return {
            "status": "blocked",
            "processed": False,
            "errors": ["a running job requires explicit manual recovery; automatic retry is disabled"],
        }
    inbox = sorted(runner_queue_state_dir("inbox").glob("*.yaml"))
    if not inbox:
        return {"status": "idle", "processed": False}
    source = inbox[0]
    entry = runner_queue_read_job(source, "inbox")
    if not entry["valid"]:
        return {"status": "blocked", "processed": True, "blocked": runner_queue_block_invalid(source, entry)}
    job = entry["job"]
    job_id = str(job["id"])
    binding = runner_recipe_binding(str(job["recipe"]))
    if not binding["ready"]:
        entry["errors"].extend(binding["errors"])
        return {
            "status": "blocked",
            "processed": True,
            "blocked": runner_queue_block_invalid(source, entry, binding=binding),
        }
    running_path = runner_queue_job_path("running", job_id)
    if running_path.exists():
        entry["errors"].append("job id already exists in running; refusing to overwrite")
        return {"status": "blocked", "processed": True, "blocked": runner_queue_block_invalid(source, entry, binding=binding)}
    try:
        source.replace(running_path)
    except FileNotFoundError:
        return {"status": "contended", "processed": False, "errors": ["job was claimed by another runner"]}
    runner_queue_write_receipt(
        job_id,
        state="running",
        claimed_at=now_iso(),
        started_at=now_iso(),
        runner_id=config.get("device_id"),
        recipe_binding=binding,
    )
    command, timeout = runner_queue_recipe_command(str(job["recipe"]))
    try:
        completed = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout, check=False)
        stdout = runner_queue_output_text(completed.stdout)[-16000:]
        stderr = runner_queue_output_text(completed.stderr)[-16000:]
        recipe_data = None
        try:
            recipe_data = json.loads(stdout)
        except json.JSONDecodeError:
            pass
        succeeded = completed.returncode == 0 and (not isinstance(recipe_data, dict) or recipe_data.get("passed") is not False)
        state = "done" if succeeded else "failed"
        reason = None if succeeded else f"recipe exited with code {completed.returncode}"
        result = {
            "protocol": QUEUE_PROTOCOL, "job_id": job_id, "recipe": job["recipe"], "status": state,
            "exit_code": completed.returncode, "finished_at": now_iso(), "command": command,
            "recipe_passed": recipe_data.get("passed") if isinstance(recipe_data, dict) else None,
            "stdout": stdout, "stderr": stderr, "reason": reason, "recipe_binding": binding,
        }
    except subprocess.TimeoutExpired as exc:
        state = "failed"
        result = {
            "protocol": QUEUE_PROTOCOL, "job_id": job_id, "recipe": job["recipe"], "status": state,
            "exit_code": None, "finished_at": now_iso(), "command": command, "recipe_passed": False,
            "stdout": runner_queue_output_text(exc.stdout)[-16000:], "stderr": runner_queue_output_text(exc.stderr)[-16000:],
            "reason": f"recipe timed out after {timeout}s", "recipe_binding": binding,
        }
    conflicting = runner_queue_existing_paths(job_id)
    conflicting.pop("running", None)
    if conflicting:
        return {
            "status": "conflict",
            "processed": True,
            "job_id": job_id,
            "errors": ["terminal transition refused; duplicate queue evidence exists: " + json.dumps(conflicting)],
        }
    destination = runner_queue_job_path(state, job_id)
    running_path.replace(destination)
    write_runner_queue_json(runner_queue_result_path(job_id), result)
    runner_queue_write_receipt(job_id, state=state, finished_at=result["finished_at"], exit_code=result["exit_code"])
    return {"status": state, "processed": True, "job_id": job_id, "result": result, "path": runner_queue_rel(destination)}


def cmd_runner_queue_submit(args: argparse.Namespace) -> int:
    data = runner_queue_submit(args.job_id or runner_queue_default_id(), args.recipe, requested_by=args.requested_by, note=args.note)
    if args.json:
        print_json(data)
    else:
        print(f"queued {data['job']['id']} ({data['job']['recipe']}) -> {data['path']}")
    return 0


def cmd_runner_queue_contract(args: argparse.Namespace) -> int:
    data = runner_queue_contract_payload()
    if args.write:
        ensure_runner_queue_dirs()
        data["contract_path"] = runner_queue_rel(runner_queue_contract_file())
        write_runner_queue_json(runner_queue_contract_file(), data)
    if args.json:
        print_json(data)
    else:
        print(f"runner queue contract: {data['protocol']}")
        print("  states: " + " -> ".join(QUEUE_STATES))
        print("  recipes: " + ", ".join(QUEUE_ALLOWED_RECIPES))
        print("  owner: runner-queue run --once")
        if data.get("contract_path"):
            print(f"  written: {data['contract_path']}")
    return 0


def cmd_runner_queue_validate(args: argparse.Namespace) -> int:
    data = runner_queue_payload()
    if args.write:
        data = write_runner_queue_manifest(data)
    if args.json:
        print_json(data)
    else:
        print(f"runner queue: {'valid' if data['validation']['valid'] else 'invalid'}")
        print("  " + " ".join(f"{state}={data['counts'][state]}" for state in QUEUE_STATES))
        for error in data['validation']['errors']:
            print(f"  error: {error}")
    return 0 if data["validation"]["valid"] else 1


def cmd_runner_queue_status(args: argparse.Namespace) -> int:
    data = runner_queue_payload()
    if args.json:
        print_json(data)
    else:
        print("runner queue: " + " ".join(f"{state}={data['counts'][state]}" for state in QUEUE_STATES))
        for job in data["jobs"]:
            print(f"  {job['state']:7} {job['id']} ({job.get('recipe') or 'invalid'})")
    return 0 if data["validation"]["valid"] else 1


def cmd_runner_queue_dashboard(args: argparse.Namespace) -> int:
    data = write_runner_queue_manifest()
    out = write_runner_queue_status(data)
    if args.open:
        webbrowser.open(out.resolve().as_uri())
    response = {"dashboard": runner_queue_rel(out), "manifest": data["manifest_path"], "counts": data["counts"], "validation": data["validation"]}
    if args.json:
        print_json(response)
    else:
        print(f"runner queue dashboard: {response['dashboard']}")
    return 0 if data["validation"]["valid"] else 1


def cmd_runner_queue_run(args: argparse.Namespace) -> int:
    config, _warnings = load_device(args.config)
    data = runner_queue_run_once(config)
    payload = write_runner_queue_manifest()
    data["manifest"] = payload["manifest_path"]
    if args.json:
        print_json(data)
    else:
        print(f"runner queue run: {data['status']}")
        if data.get("job_id"):
            print(f"  job: {data['job_id']}")
        for error in data.get("errors") or []:
            print(f"  error: {error}")
    return 0 if data["status"] in ("done", "idle") else 1


def runner_agent_validate_poll_seconds(value: float) -> float:
    if value < RUNNER_AGENT_MIN_POLL_SECONDS or value > RUNNER_AGENT_MAX_POLL_SECONDS:
        raise ValueError(
            f"poll seconds must be between {RUNNER_AGENT_MIN_POLL_SECONDS:g} and {RUNNER_AGENT_MAX_POLL_SECONDS:g}"
        )
    return value


def runner_agent_serve(config: Dict[str, Any], *, poll_seconds: float, max_jobs: Optional[int] = None,
                       max_idle_polls: Optional[int] = None) -> Dict[str, Any]:
    """Run the deliberately small, exclusive runner-agent loop.

    The loop executes at most one queue job at a time and stops on any blocked,
    failed, stale, or conflicted state.  It never retries a running job.
    """
    poll_seconds = runner_agent_validate_poll_seconds(float(poll_seconds))
    if config.get("role") not in ("runner", "runner+collector"):
        return {"status": "blocked", "errors": ["runner-agent serve requires device role runner or runner+collector"], "processed": 0}
    if max_jobs is not None and max_jobs < 1:
        return {"status": "blocked", "errors": ["max_jobs must be at least 1"], "processed": 0}
    if max_idle_polls is not None and max_idle_polls < 0:
        return {"status": "blocked", "errors": ["max_idle_polls cannot be negative"], "processed": 0}
    try:
        owner = runner_agent_acquire_lock(str(config.get("device_id") or "unknown-runner"))
    except RuntimeError as exc:
        return {"status": "locked", "errors": [str(exc)], "processed": 0}
    processed = 0
    idle_polls = 0
    events: List[Dict[str, Any]] = []
    try:
        while True:
            outcome = runner_queue_run_once(config)
            events.append({key: value for key, value in outcome.items() if key != "result"})
            status = str(outcome.get("status"))
            if status == "done":
                processed += 1
                if max_jobs is not None and processed >= max_jobs:
                    return {"status": "completed", "processed": processed, "owner": owner, "events": events}
                time.sleep(poll_seconds)
                continue
            if status == "idle":
                idle_polls += 1
                if max_idle_polls is not None and idle_polls >= max_idle_polls:
                    return {"status": "idle", "processed": processed, "owner": owner, "events": events}
                time.sleep(poll_seconds)
                continue
            # A failed recipe is terminal evidence, not a prompt to retry.
            return {"status": status, "processed": processed, "owner": owner, "events": events,
                    "errors": outcome.get("errors") or []}
    finally:
        runner_agent_release_lock()


def runner_agent_inspect_payload() -> Dict[str, Any]:
    queue = runner_queue_payload()
    lock = runner_agent_lock_dir()
    recovery_entries: List[Dict[str, Any]] = []
    if runner_agent_recovery_file().is_file():
        for line in runner_agent_recovery_file().read_text(encoding="utf-8").splitlines()[-20:]:
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    recovery_entries.append(value)
            except json.JSONDecodeError:
                recovery_entries.append({"invalid_line": line[:300]})
    return {
        "protocol": QUEUE_PROTOCOL,
        "generated_at": now_iso(),
        "lock": {"present": lock.exists(), "owner": runner_queue_load_json(lock / "owner.json") if lock.exists() else {}},
        "queue": queue,
        "stale_running": queue["counts"].get("running", 0) > 0,
        "recovery_events": recovery_entries,
    }


def runner_agent_recover(*, job_id: Optional[str], clear_lock: bool, block_running: bool, confirm: bool) -> Dict[str, Any]:
    """Perform one explicit, append-only recovery operation after inspection."""
    if not confirm:
        return {"status": "blocked", "errors": ["recovery requires --confirm after runner-agent inspect"]}
    if int(bool(clear_lock)) + int(bool(block_running)) != 1:
        return {"status": "blocked", "errors": ["choose exactly one of --clear-lock or --block-running"]}
    if clear_lock:
        lock = runner_agent_lock_dir()
        if not lock.exists():
            return {"status": "idle", "action": "clear-lock", "errors": ["no agent lock exists"]}
        owner = runner_queue_load_json(lock / "owner.json")
        runner_agent_release_lock()
        event = {"action": "clear-lock", "owner": owner, "reason": "explicit operator recovery"}
        runner_agent_append_recovery(event)
        return {"status": "recovered", **event}
    if not job_id or not runner_queue_safe_id(job_id):
        return {"status": "blocked", "errors": ["--block-running requires a safe --job-id"]}
    if runner_agent_lock_dir().exists():
        return {"status": "blocked", "errors": ["refusing recovery while an agent lock exists; inspect and clear it explicitly first"]}
    source = runner_queue_job_path("running", job_id)
    if not source.exists():
        return {"status": "blocked", "errors": ["no matching running job exists"]}
    conflicts = runner_queue_existing_paths(job_id)
    conflicts.pop("running", None)
    if conflicts:
        return {"status": "blocked", "errors": ["refusing recovery because terminal evidence already exists: " + json.dumps(conflicts)]}
    entry = runner_queue_read_job(source, "running")
    destination = runner_queue_job_path("blocked", job_id)
    source.replace(destination)
    reason = "explicit operator recovery blocked a stale running job; retry requires a new job id"
    runner_queue_write_receipt(job_id, state="blocked", blocked_at=now_iso(), reason=reason, recovery=True)
    write_runner_queue_json(runner_queue_result_path(job_id), {
        "protocol": QUEUE_PROTOCOL, "job_id": job_id, "recipe": entry.get("recipe"), "status": "blocked",
        "finished_at": now_iso(), "reason": reason, "recovery": True,
    })
    event = {"action": "block-running", "job_id": job_id, "reason": reason}
    runner_agent_append_recovery(event)
    return {"status": "recovered", **event, "path": runner_queue_rel(destination)}


def cmd_runner_agent_serve(args: argparse.Namespace) -> int:
    config, _warnings = load_device(args.config)
    data = runner_agent_serve(config, poll_seconds=args.poll_seconds, max_jobs=args.max_jobs,
                              max_idle_polls=args.max_idle_polls)
    if args.json:
        print_json(data)
    else:
        print(f"runner agent: {data['status']} processed={data.get('processed', 0)}")
        for error in data.get("errors") or []:
            print(f"  error: {error}")
    return 0 if data["status"] in ("completed", "idle") else 1


def cmd_runner_agent_inspect(args: argparse.Namespace) -> int:
    data = runner_agent_inspect_payload()
    if args.json:
        print_json(data)
    else:
        print(f"runner agent: lock={'present' if data['lock']['present'] else 'clear'} stale_running={data['stale_running']}")
    return 0 if data["queue"]["validation"]["valid"] else 1


def cmd_runner_agent_recover(args: argparse.Namespace) -> int:
    data = runner_agent_recover(job_id=args.job_id, clear_lock=args.clear_lock,
                                block_running=args.block_running, confirm=args.confirm)
    if args.json:
        print_json(data)
    else:
        print(f"runner agent recovery: {data['status']}")
        for error in data.get("errors") or []:
            print(f"  error: {error}")
    return 0 if data["status"] in ("recovered", "idle") else 1


def runner_agent_peer_invoke(peer: Dict[str, Any], arguments: List[str], *, timeout: int = 60) -> Dict[str, Any]:
    """Invoke one fixed SyncMate CLI on a configured runner peer.

    `arguments` is built internally from validated schema values only; it is
    never accepted as a user-provided remote command string.
    """
    repo_path = str(peer.get("repo_path") or "")
    if not repo_path:
        return {"ok": False, "errors": ["configured runner peer has no repo_path"]}
    if peer_uses_local_transport(peer):
        command = [sys.executable, "scripts/syncmate/syncmate.py", *arguments]
        completed = subprocess.run(command, cwd=resolve_local_repo_root(repo_path), capture_output=True, text=True,
                                   timeout=timeout, check=False)
    else:
        ssh = transport_ssh_value(peer)
        if not ssh:
            return {"ok": False, "errors": ["configured SSH runner peer has no ssh target"]}
        python_executable = peer_python_executable(peer)
        remote = "cd " + shell_quote(repo_path) + " && PYTHONDONTWRITEBYTECODE=1 " + " ".join(
            shell_quote(part) for part in [python_executable, "scripts/syncmate/syncmate.py", *arguments]
        )
        command = ["ssh", ssh, remote]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    stdout = runner_queue_output_text(completed.stdout)[-16000:]
    stderr = runner_queue_output_text(completed.stderr)[-16000:]
    payload: Dict[str, Any] = {}
    try:
        raw = json.loads(stdout)
        if isinstance(raw, dict):
            payload = raw
    except json.JSONDecodeError:
        pass
    return {
        "ok": completed.returncode == 0 and bool(payload),
        "returncode": completed.returncode,
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "payload": payload,
        "errors": [] if completed.returncode == 0 else [f"runner peer command exited {completed.returncode}"],
    }


def runner_agent_dispatch_payload(device: Dict[str, Any], warnings: List[str], *, config_path: Path,
                                  node_id: str, job_id: str, recipe: str, requested_by: Optional[str],
                                  note: Optional[str]) -> Dict[str, Any]:
    """Controller-side guarded enqueue; this does not run an experiment."""
    if recipe not in QUEUE_ALLOWED_RECIPES:
        return {"status": "blocked", "errors": ["recipe is not allowlisted"]}
    if not runner_queue_safe_id(job_id):
        return {"status": "blocked", "errors": ["job id is unsafe"]}
    if requested_by is not None and (not isinstance(requested_by, str) or len(requested_by) > 500):
        return {"status": "blocked", "errors": ["requested_by must be a short string"]}
    if note is not None and (not isinstance(note, str) or len(note) > 500):
        return {"status": "blocked", "errors": ["note must be a short string"]}
    preflight = preflight_payload(device, warnings, config_path=config_path, node_ids=[node_id], require_sync_targets=True)
    maybe_write_preflight_report(preflight, save=True)
    if preflight.get("status") == "blocked":
        return {"status": "blocked", "errors": ["controller preflight blocked dispatch"], "preflight": preflight}
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    peer = peers.get(node_id)
    if not isinstance(peer, dict):
        return {"status": "blocked", "errors": ["runner peer is unknown"], "preflight": preflight}
    if peer.get("role", "runner") not in ("runner", "runner+collector"):
        return {"status": "blocked", "errors": ["dispatch target must be a runner or runner+collector peer"], "preflight": preflight}
    result = runner_agent_peer_invoke(
        peer,
        ["runner-queue", "submit", "--job-id", job_id, "--recipe", recipe,
         "--requested-by", requested_by or str(device.get("device_id") or "syncmate-controller"),
         "--note", note or "controller-dispatch", "--json"],
    )
    if not result.get("ok"):
        return {"status": "blocked", "errors": result.get("errors") or ["runner submit failed"],
                "preflight": preflight, "peer_command": result}
    return {"status": "submitted", "job_id": job_id, "recipe": recipe, "node_id": node_id,
            "preflight": preflight, "peer_command": result, "submission": result.get("payload")}


def runner_agent_watch_payload(device: Dict[str, Any], *, node_id: str, job_id: str, poll_seconds: float,
                               timeout_seconds: int) -> Dict[str, Any]:
    poll_seconds = runner_agent_validate_poll_seconds(float(poll_seconds))
    if timeout_seconds < 1 or timeout_seconds > RUNNER_AGENT_MAX_TIMEOUT_SECONDS:
        return {"status": "blocked", "errors": [f"timeout seconds must be between 1 and {RUNNER_AGENT_MAX_TIMEOUT_SECONDS}"]}
    peers = device.get("peers") if isinstance(device.get("peers"), dict) else {}
    peer = peers.get(node_id)
    if not isinstance(peer, dict) or peer.get("role", "runner") not in ("runner", "runner+collector"):
        return {"status": "blocked", "errors": ["watch target must be a configured runner peer"]}
    started = time.monotonic()
    observations: List[Dict[str, Any]] = []
    while True:
        response = runner_agent_peer_invoke(peer, ["runner-queue", "status", "--json"])
        observations.append({key: value for key, value in response.items() if key not in ("stdout", "stderr")})
        if not response.get("ok"):
            return {"status": "blocked", "errors": response.get("errors") or ["could not read runner queue"],
                    "observations": observations}
        jobs = (response.get("payload") or {}).get("jobs") or []
        matched = [job for job in jobs if job.get("id") == job_id]
        if matched and matched[0].get("state") in ("done", "failed", "blocked"):
            job = matched[0]
            state = str(job["state"])
            return {"status": state, "job": job, "observations": observations}
        if time.monotonic() - started >= timeout_seconds:
            return {"status": "timeout", "errors": ["watch timed out; no retry or acceptance was attempted"],
                    "observations": observations}
        time.sleep(poll_seconds)


def runner_agent_collect_and_gate(config_path: Path, node_id: str) -> Dict[str, Any]:
    """Run the existing collector command only after the runner reaches done."""
    command = [sys.executable, "scripts/syncmate/syncmate.py"]
    if config_path != DEFAULT_DEVICE_FILE:
        command.extend(["--config", str(config_path)])
    command.extend(["sync", node_id, "--json"])
    completed = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, timeout=RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
                               check=False)
    stdout = runner_queue_output_text(completed.stdout)[-16000:]
    stderr = runner_queue_output_text(completed.stderr)[-16000:]
    payload: Dict[str, Any] = {}
    try:
        raw = json.loads(stdout)
        if isinstance(raw, dict):
            payload = raw
    except json.JSONDecodeError:
        pass
    gate_passed = bool((payload.get("gate") or {}).get("passed"))
    return {"ok": completed.returncode == 0 and gate_passed, "returncode": completed.returncode,
            "gate_passed": gate_passed, "command": command, "payload": payload,
            "stdout": stdout, "stderr": stderr,
            "errors": [] if completed.returncode == 0 and gate_passed else ["collector verification or acceptance gate failed"]}


def cmd_runner_agent_dispatch(args: argparse.Namespace) -> int:
    device, warnings = load_device(args.config)
    job_id = args.job_id or runner_queue_default_id()
    data = runner_agent_dispatch_payload(device, warnings, config_path=args.config, node_id=args.node_id,
                                         job_id=job_id, recipe=args.recipe, requested_by=args.requested_by, note=args.note)
    if data.get("status") == "submitted" and args.wait:
        watched = runner_agent_watch_payload(device, node_id=args.node_id, job_id=job_id,
                                             poll_seconds=args.poll_seconds, timeout_seconds=args.timeout_seconds)
        data["watch"] = watched
        if watched.get("status") == "done":
            definition = runner_recipe_definition(args.recipe)
            if definition.get("collector_acceptance"):
                data["acceptance"] = runner_agent_collect_and_gate(args.config, args.node_id)
                if not data["acceptance"].get("ok"):
                    data["status"] = "blocked"
                else:
                    data["status"] = "accepted"
            else:
                data["status"] = "done-not-eligible"
        else:
            data["status"] = str(watched.get("status"))
    if args.json:
        print_json(data)
    else:
        print(f"runner dispatch: {data.get('status')} job={job_id}")
        for error in data.get("errors") or []:
            print(f"  error: {error}")
    return 0 if data.get("status") in ("submitted", "accepted", "done-not-eligible") else 1


def cmd_runner_agent_watch(args: argparse.Namespace) -> int:
    device, _warnings = load_device(args.config)
    data = runner_agent_watch_payload(device, node_id=args.node_id, job_id=args.job_id,
                                      poll_seconds=args.poll_seconds, timeout_seconds=args.timeout_seconds)
    if args.json:
        print_json(data)
    else:
        print(f"runner watch: {data['status']}")
    return 0 if data["status"] == "done" else 1


def cmd_smoke(args: argparse.Namespace) -> int:
    data = smoke_payload(args)
    if args.json:
        print_json(data)
        return 0 if data.get("passed") else 1

    print(f"syncmate smoke: {'passed' if data.get('passed') else 'failed'}")
    print(f"  workdir: {data.get('workdir')}")
    print(f"  kept: {data.get('kept')} cleaned={data.get('cleaned')}")
    summary = data.get("summary") or {}
    print(
        f"  diff_missing={summary.get('diff_missing', 0)} "
        f"collected={summary.get('collected', 0)} "
        f"verified={summary.get('verified', 0)} "
        f"indexed={summary.get('indexed', 0)} "
        f"result_rows={summary.get('result_rows', 0)} "
        f"parse_errors={summary.get('parse_errors', 0)}"
    )
    files = data.get("files") or {}
    if files:
        print(f"  landing: {data.get('landing')}")
        print(f"  local artifact: {files.get('local_attack')}")
        print(f"  artifact index: {files.get('artifact_index')}")
        print(f"  results: {files.get('results_json')} / {files.get('results_csv')}")
        print(f"  dashboard: {files.get('dashboard')}")
    for error in data.get("errors") or []:
        print(f"  error: {error}")
    if data.get("passed") and data.get("cleaned"):
        print("  note: temporary smoke workspace was removed; rerun with --keep to inspect files")
    return 0 if data.get("passed") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Device-local sync guidance for this repo.")
    parser.add_argument("--config", type=Path, default=DEFAULT_DEVICE_FILE,
                        help="device setup file (default: .syncmate/device.yaml)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_self = sub.add_parser("self", help="show this device identity and git state")
    p_self.add_argument("--json", action="store_true")
    p_self.set_defaults(func=cmd_self)

    p_layout = sub.add_parser("layout", help="show sync paths, peer landings, and trusted output files")
    p_layout.add_argument("node_ids", nargs="*", help="optional peer node ids to show")
    p_layout.add_argument("--json", action="store_true")
    p_layout.set_defaults(func=cmd_layout)

    p_landings = sub.add_parser("landings", help="show local peer landing folders and trusted result rows")
    p_landings.add_argument("node_ids", nargs="*", help="optional peer node ids to show")
    p_landings.add_argument("--json", action="store_true")
    p_landings.add_argument("--limit", type=int, default=5,
                            help="maximum landing leaf/result examples per peer (default: 5)")
    p_landings.set_defaults(func=cmd_landings)

    p_trace = sub.add_parser("trace", help="trace trusted artifacts from remote path to landing and result rows")
    p_trace.add_argument("node_ids", nargs="*", help="optional peer node ids to trace")
    p_trace.add_argument("--json", action="store_true")
    p_trace.add_argument("--check", action="store_true",
                         help="recompute local SHA-256 values and fail on drift")
    p_trace.add_argument("--limit", type=int, default=20,
                         help="maximum trusted leaves to include (default: 20)")
    p_trace.set_defaults(func=cmd_trace)

    p_checklist = sub.add_parser("checklist", help="print or write a short current-state sync checklist")
    p_checklist.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_checklist.add_argument("--json", action="store_true")
    p_checklist.add_argument("--write", action="store_true",
                             help="write .syncmate/checklist.md")
    p_checklist.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                             help="lowest diagnostic severity that blocks checklist readiness (default: warn)")
    p_checklist.add_argument("--strict", action="store_true",
                             help="shortcut for --fail-on info")
    p_checklist.add_argument("--require-preflight", dest="require_preflight", action="store_true",
                             default=True, help="require a fresh saved preflight report (default)")
    p_checklist.add_argument("--no-require-preflight", dest="require_preflight", action="store_false",
                             help="omit saved preflight from checklist readiness")
    p_checklist.add_argument("--require-verify", dest="require_verify", action="store_true",
                             default=True, help="require clean verify reports and artifact index (default)")
    p_checklist.add_argument("--no-require-verify", dest="require_verify", action="store_false",
                             help="omit verification/index from checklist readiness")
    p_checklist.add_argument("--require-results", dest="require_results", action="store_true",
                             default=True, help="require a fresh trusted results table (default)")
    p_checklist.add_argument("--no-require-results", dest="require_results", action="store_false",
                             help="omit trusted results-table freshness from checklist readiness")
    p_checklist.add_argument("--limit", type=int, default=8,
                             help="maximum commands, actions, and examples to include (default: 8)")
    p_checklist.set_defaults(func=cmd_checklist)

    p_runbook = sub.add_parser("runbook", help="print or write a device-level Syncmate operating runbook")
    p_runbook.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_runbook.add_argument("--json", action="store_true")
    p_runbook.add_argument("--write", action="store_true",
                           help="write .syncmate/runbook.md")
    p_runbook.add_argument("--limit", type=int, default=8,
                           help="maximum peers and commands to include (default: 8)")
    p_runbook.set_defaults(func=cmd_runbook)

    p_overview = sub.add_parser("overview", help="show one read-only sync overview for AI agents or dashboards")
    p_overview.add_argument("--json", action="store_true")
    p_overview.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                            help="lowest diagnostic severity that fails the overview gate (default: warn)")
    p_overview.add_argument("--strict", action="store_true",
                            help="shortcut for --fail-on info")
    p_overview.add_argument("--require-verify", action="store_true",
                            help="include strict verification and artifact-index checks")
    p_overview.add_argument("--require-preflight", action="store_true",
                            help="require a fresh saved preflight report")
    p_overview.add_argument("--require-results", action="store_true",
                            help="require a saved parse-clean trusted results table")
    p_overview.add_argument("--limit", type=int, default=5,
                            help="maximum diagnostics, commands, and failures to include (default: 5)")
    p_overview.set_defaults(func=cmd_overview)

    p_lifecycle = sub.add_parser("lifecycle", help="show the current setup-to-acceptance lifecycle phase")
    p_lifecycle.add_argument("--json", action="store_true")
    p_lifecycle.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                             help="lowest diagnostic severity that blocks final acceptance (default: warn)")
    p_lifecycle.add_argument("--strict", action="store_true",
                             help="shortcut for --fail-on info")
    p_lifecycle.add_argument("--require-preflight", dest="require_preflight", action="store_true",
                             default=True, help="require a fresh saved preflight report (default)")
    p_lifecycle.add_argument("--no-require-preflight", dest="require_preflight", action="store_false",
                             help="omit saved preflight from lifecycle acceptance")
    p_lifecycle.add_argument("--require-verify", dest="require_verify", action="store_true",
                             default=True, help="require clean verify reports and artifact index (default)")
    p_lifecycle.add_argument("--no-require-verify", dest="require_verify", action="store_false",
                             help="omit verification/index from lifecycle acceptance")
    p_lifecycle.add_argument("--require-results", dest="require_results", action="store_true",
                             default=True, help="require a fresh trusted results table (default)")
    p_lifecycle.add_argument("--no-require-results", dest="require_results", action="store_false",
                             help="omit trusted results-table freshness from lifecycle acceptance")
    p_lifecycle.add_argument("--limit", type=int, default=8,
                             help="maximum next commands and attention stages to include (default: 8)")
    p_lifecycle.set_defaults(func=cmd_lifecycle)

    p_smoke = sub.add_parser("smoke", help="run a temporary local end-to-end sync smoke test")
    p_smoke.add_argument("--json", action="store_true")
    p_smoke.add_argument("--keep", action="store_true",
                         help="keep the temporary smoke workspace for inspection")
    p_smoke.add_argument("--workdir", type=Path,
                         help="parent directory for a kept smoke workspace")
    p_smoke.set_defaults(func=cmd_smoke)

    p_runner_preflight = sub.add_parser(
        "runner-preflight",
        help="write only isolated, no-GPU bounded-runner evidence for a declared recipe",
    )
    p_runner_preflight.add_argument("--recipe", choices=("opengu-preflight-v1",), required=True)
    p_runner_preflight.add_argument("--json", action="store_true")
    p_runner_preflight.set_defaults(func=cmd_runner_preflight)

    p_runner_agent = sub.add_parser(
        "runner-agent",
        help="bounded local runner agent: one lock, one queue job, declared recipes only",
    )
    runner_agent_sub = p_runner_agent.add_subparsers(dest="runner_agent_command", required=True)
    p_agent_serve = runner_agent_sub.add_parser("serve", help="poll the local inbox under one exclusive lock")
    p_agent_serve.add_argument("--poll-seconds", type=float, default=5.0,
                               help="bounded poll interval, 1 to 60 seconds (default: 5)")
    p_agent_serve.add_argument("--max-jobs", type=int,
                               help="optional bounded job count; useful for supervised runs/tests")
    p_agent_serve.add_argument("--max-idle-polls", type=int,
                               help="optional bounded idle polls; useful for supervised runs/tests")
    p_agent_serve.add_argument("--json", action="store_true")
    p_agent_serve.set_defaults(func=cmd_runner_agent_serve)
    p_agent_inspect = runner_agent_sub.add_parser("inspect", help="read lock, queue, stale state, and recovery audit")
    p_agent_inspect.add_argument("--json", action="store_true")
    p_agent_inspect.set_defaults(func=cmd_runner_agent_inspect)
    p_agent_recover = runner_agent_sub.add_parser("recover", help="explicitly recover a stale lock or running job")
    p_agent_recover.add_argument("--clear-lock", action="store_true", help="remove an inspected stale agent lock")
    p_agent_recover.add_argument("--block-running", action="store_true", help="move one stale running job to blocked")
    p_agent_recover.add_argument("--job-id", help="required with --block-running")
    p_agent_recover.add_argument("--confirm", action="store_true", help="required acknowledgement after inspect")
    p_agent_recover.add_argument("--json", action="store_true")
    p_agent_recover.set_defaults(func=cmd_runner_agent_recover)
    p_agent_dispatch = runner_agent_sub.add_parser(
        "dispatch", help="collector-side guarded submission to one configured runner peer",
    )
    p_agent_dispatch.add_argument("node_id", help="configured runner peer id")
    p_agent_dispatch.add_argument("--recipe", choices=QUEUE_ALLOWED_RECIPES, required=True)
    p_agent_dispatch.add_argument("--job-id", help="stable unique job id; default is generated")
    p_agent_dispatch.add_argument("--requested-by", help="short requester label recorded remotely")
    p_agent_dispatch.add_argument("--note", help="short immutable submission note")
    p_agent_dispatch.add_argument("--wait", action="store_true", help="watch terminal state and then run normal collector verification")
    p_agent_dispatch.add_argument("--poll-seconds", type=float, default=5.0)
    p_agent_dispatch.add_argument("--timeout-seconds", type=int, default=300)
    p_agent_dispatch.add_argument("--json", action="store_true")
    p_agent_dispatch.set_defaults(func=cmd_runner_agent_dispatch)
    p_agent_watch = runner_agent_sub.add_parser("watch", help="watch one remote job without dispatching or accepting it")
    p_agent_watch.add_argument("node_id", help="configured runner peer id")
    p_agent_watch.add_argument("--job-id", required=True)
    p_agent_watch.add_argument("--poll-seconds", type=float, default=5.0)
    p_agent_watch.add_argument("--timeout-seconds", type=int, default=300)
    p_agent_watch.add_argument("--json", action="store_true")
    p_agent_watch.set_defaults(func=cmd_runner_agent_watch)

    p_runner_queue = sub.add_parser(
        "runner-queue",
        help="local YAML inbox for allowlisted runner smoke checks; never runs experiments",
    )
    runner_queue_sub = p_runner_queue.add_subparsers(dest="runner_queue_command", required=True)
    p_queue_submit = runner_queue_sub.add_parser("submit", help="write one allowlisted YAML job into the local inbox")
    p_queue_submit.add_argument("--recipe", choices=QUEUE_ALLOWED_RECIPES, default="smoke",
                                help="allowlisted recipe (default: smoke)")
    p_queue_submit.add_argument("--job-id", help="optional stable job id; default is generated")
    p_queue_submit.add_argument("--requested-by", help="short local requester label recorded in the job")
    p_queue_submit.add_argument("--note", help="short local note recorded in the job")
    p_queue_submit.add_argument("--json", action="store_true")
    p_queue_submit.set_defaults(func=cmd_runner_queue_submit)

    p_queue_contract = runner_queue_sub.add_parser(
        "contract",
        help="print the stable read-only boundary for SyncMate/OpenGU integration",
    )
    p_queue_contract.add_argument("--write", action="store_true",
                                  help="also write .syncmate/runner_queue/contract.json")
    p_queue_contract.add_argument("--json", action="store_true")
    p_queue_contract.set_defaults(func=cmd_runner_queue_contract)

    p_queue_validate = runner_queue_sub.add_parser("validate", help="validate YAML queue protocol and state exclusivity")
    p_queue_validate.add_argument("--write", action="store_true", help="also write .syncmate/runner_queue/manifest.json")
    p_queue_validate.add_argument("--json", action="store_true")
    p_queue_validate.set_defaults(func=cmd_runner_queue_validate)

    p_queue_status = runner_queue_sub.add_parser("status", help="read queue state without executing jobs")
    p_queue_status.add_argument("--json", action="store_true")
    p_queue_status.set_defaults(func=cmd_runner_queue_status)

    p_queue_dashboard = runner_queue_sub.add_parser("dashboard", help="write static .syncmate/runner_queue/status.html")
    p_queue_dashboard.add_argument("--open", action="store_true", help="open the generated static status page")
    p_queue_dashboard.add_argument("--json", action="store_true")
    p_queue_dashboard.set_defaults(func=cmd_runner_queue_dashboard)

    p_queue_run = runner_queue_sub.add_parser("run", help="claim and run exactly one allowlisted inbox job")
    p_queue_run.add_argument("--once", action="store_true", required=True,
                             help="required: process at most one job; use runner-agent serve for bounded polling")
    p_queue_run.add_argument("--json", action="store_true")
    p_queue_run.set_defaults(func=cmd_runner_queue_run)

    p_init = sub.add_parser("init-device", help="create the untracked device-local setup file")
    p_init.add_argument("--device-id", default=default_device_id(),
                        help="local node id (default: hostname)")
    p_init.add_argument("--role", choices=ROLE_CHOICES, required=True,
                        help="device role in the syncmate protocol")
    p_init.add_argument("--repo-path", default=str(REPO_ROOT),
                        help="repo path recorded for this device")
    p_init.add_argument("--collector-hint",
                        help="optional collector id/name for runner-side configs")
    p_init.add_argument("--artifact-include", nargs="+", action="append",
                        help="artifact file names to include in this device policy")
    p_init.add_argument("--artifact-exclude", nargs="+", action="append",
                        help="artifact file names to exclude from this device policy")
    p_init.add_argument("--force", action="store_true",
                        help="overwrite an existing setup file")
    p_init.add_argument("--json", action="store_true")
    p_init.set_defaults(func=cmd_init_device)

    p_add = sub.add_parser("add-peer", help="add or replace a runner peer in device-local setup")
    p_add.add_argument("node_id", help="peer node id, e.g. gpu4090 or h800")
    p_add.add_argument("--ssh", help="SSH host alias or user@host")
    p_add.add_argument("--local", action="store_true",
                       help="use a local filesystem repo-path instead of SSH")
    p_add.add_argument("--repo-path", required=True, help="repo path on the peer")
    p_add.add_argument("--python-executable",
                       help="Python executable on an SSH peer (default: python)")
    p_add.add_argument("--role", choices=ROLE_CHOICES, default="runner",
                       help="peer role (default: runner)")
    p_add.add_argument("--landing",
                       help="local landing path (default: results/runs/<node_id>)")
    p_add.add_argument("--result-root", dest="result_roots", action="append",
                       help="remote result root to collect; repeat for multiple roots")
    p_add.add_argument("--artifact-include", nargs="+", action="append",
                       help="artifact file names to include for this peer")
    p_add.add_argument("--artifact-exclude", nargs="+", action="append",
                       help="artifact file names to exclude for this peer")
    p_add.add_argument("--force", action="store_true",
                       help="replace an existing peer entry")
    p_add.add_argument("--json", action="store_true")
    p_add.set_defaults(func=cmd_add_peer)

    p_setup = sub.add_parser("setup-plan", help="print a safe first-run setup plan")
    p_setup.add_argument("--role", choices=ROLE_CHOICES,
                         help="target role for this checkout (default: current role or collector)")
    p_setup.add_argument("--device-id",
                         help="device id to use in the init-device command")
    p_setup.add_argument("--repo-path",
                         help="repo path to use in the local init-device command")
    p_setup.add_argument("--collector-id",
                         help="collector id/hint to pass to a runner setup")
    p_setup.add_argument("--peer-id",
                         help="runner peer id to include in collector commands")
    p_setup.add_argument("--peer-ssh",
                         help="SSH alias or user@host for the runner peer")
    p_setup.add_argument("--peer-local", action="store_true",
                         help="generate local-transport peer commands instead of SSH commands")
    p_setup.add_argument("--peer-repo-path",
                         help="repo path on the runner peer")
    p_setup.add_argument("--peer-python-executable",
                         help="Python executable on the runner peer (default: python)")
    p_setup.add_argument("--landing",
                         help="collector landing path for this peer")
    p_setup.add_argument("--result-root", dest="result_roots", action="append",
                         help="remote result root to collect; repeat for multiple roots")
    p_setup.add_argument("--artifact-include", nargs="+", action="append",
                         help="artifact file names to include in generated commands")
    p_setup.add_argument("--artifact-exclude", nargs="+", action="append",
                         help="artifact file names to exclude in generated commands")
    p_setup.add_argument("--write", action="store_true",
                         help="write .syncmate/setup_plan.md")
    p_setup.add_argument("--json", action="store_true")
    p_setup.set_defaults(func=cmd_setup_plan)

    p_preflight = sub.add_parser("preflight", help="validate local setup before SSH sync automation")
    p_preflight.add_argument("node_ids", nargs="*", help="optional peer node ids to validate")
    p_preflight.add_argument("--json", action="store_true")
    p_preflight.add_argument("--write", action="store_true",
                             help="write .syncmate/last_preflight.json")
    p_preflight.add_argument("--limit", type=int, default=8,
                             help="maximum check/action lines to print per section (default: 8)")
    p_preflight.set_defaults(func=cmd_preflight)

    p_status = sub.add_parser("status", help="scan local artifact status")
    p_status.add_argument("--json", action="store_true")
    p_status.add_argument("--no-write-state", dest="write_state", action="store_false",
                          default=True, help="do not write .syncmate/state.json")
    p_status.set_defaults(func=cmd_status)

    p_publish = sub.add_parser("publish", help="emit a copyable local status/manifest package")
    p_publish.add_argument("--json", action="store_true")
    p_publish.add_argument("--write", action="store_true",
                           help="write .syncmate/publish_<device_id>.json")
    p_publish.add_argument("--roots", nargs="+",
                           help="result roots to include in the manifest summary (default: results/runs)")
    p_publish.add_argument("--include-items", action="store_true",
                           help="include full manifest items/checksums instead of a compact sample")
    p_publish.add_argument("--limit", type=int, default=10,
                           help="maximum sample manifest items when --include-items is omitted (default: 10)")
    p_publish.set_defaults(func=cmd_publish)

    p_handoff_pack = sub.add_parser("handoff-pack", help="write an evidence-only Syncmate handoff zip")
    p_handoff_pack.add_argument("--json", action="store_true")
    p_handoff_pack.add_argument("--output", type=Path,
                                help="handoff pack zip path (default: .syncmate/handoff_pack_<device_id>.zip)")
    p_handoff_pack.add_argument("--include-setup", action="store_true",
                                help="include .syncmate/device.yaml in the pack")
    p_handoff_pack.add_argument("--no-refresh", action="store_true",
                                help="do not regenerate dashboard/runbook/checklist/brief before packing")
    p_handoff_pack.add_argument("--limit", type=int, default=8,
                                help="maximum examples used when refreshing brief/runbook/checklist (default: 8)")
    p_handoff_pack.set_defaults(func=cmd_handoff_pack)

    p_inspect_handoff_pack = sub.add_parser(
        "inspect-handoff-pack",
        help="inspect and audit an evidence-only handoff pack without extracting files",
    )
    p_inspect_handoff_pack.add_argument("handoff_pack", help="path to handoff pack zip")
    p_inspect_handoff_pack.add_argument("--node-id",
                                        help="override the node id used when --write saves the inspect report")
    p_inspect_handoff_pack.add_argument("--write", action="store_true",
                                        help="write .syncmate/last_handoff_pack_inspect_<node_id>.json")
    p_inspect_handoff_pack.add_argument("--limit", type=int, default=20,
                                        help="maximum evidence files to show (default: 20)")
    p_inspect_handoff_pack.add_argument("--json", action="store_true")
    p_inspect_handoff_pack.set_defaults(func=cmd_inspect_handoff_pack)

    p_bundle = sub.add_parser("bundle", help="write a portable status plus artifact bundle for offline transfer")
    p_bundle.add_argument("--json", action="store_true")
    p_bundle.add_argument("--output", type=Path,
                          help="bundle zip path (default: .syncmate/bundle_<device_id>.zip)")
    p_bundle.add_argument("--roots", nargs="+",
                          help="result roots to include in the bundle (default: results/runs)")
    p_bundle.set_defaults(func=cmd_bundle)

    p_inspect_bundle = sub.add_parser("inspect-bundle", help="inspect and audit a portable bundle without extracting files")
    p_inspect_bundle.add_argument("bundle", help="path to bundle zip")
    p_inspect_bundle.add_argument("--node-id",
                                  help="override the node id used when --write saves the inspect report")
    p_inspect_bundle.add_argument("--write", action="store_true",
                                  help="write .syncmate/last_bundle_inspect_<node_id>.json")
    p_inspect_bundle.add_argument("--limit", type=int, default=10,
                                  help="maximum sample manifest items to show (default: 10)")
    p_inspect_bundle.add_argument("--json", action="store_true")
    p_inspect_bundle.set_defaults(func=cmd_inspect_bundle)

    p_import_publish = sub.add_parser("import-publish", help="ingest a copied publish package as a saved remote-status report")
    p_import_publish.add_argument("package",
                                  help="path to publish JSON, or '-' to read JSON from stdin")
    p_import_publish.add_argument("--node-id",
                                  help="override the node id from the publish package")
    p_import_publish.add_argument("--no-save", action="store_true",
                                  help="preview without writing .syncmate/remote_status_<node_id>.json")
    p_import_publish.add_argument("--json", action="store_true")
    p_import_publish.set_defaults(func=cmd_import_publish)

    p_import_bundle = sub.add_parser("import-bundle", help="ingest a portable bundle, extract missing artifacts, and verify checksums")
    p_import_bundle.add_argument("bundle", help="path to bundle zip")
    p_import_bundle.add_argument("--node-id",
                                 help="override the node id from the bundle manifest")
    p_import_bundle.add_argument("--overwrite", action="store_true",
                                 help="replace local files whose checksum differs")
    p_import_bundle.add_argument("--dry-run", action="store_true",
                                 help="compare bundle manifest with the landing without extracting files or writing reports")
    p_import_bundle.add_argument("--write-plan", action="store_true",
                                 help="with --dry-run, save remote_status and last_diff reports without extracting files")
    p_import_bundle.add_argument("--no-save", action="store_true",
                                 help="extract files without writing sync reports or artifact index")
    p_import_bundle.add_argument("--no-results", dest="results", action="store_false",
                                 default=True, help="do not write .syncmate/results_table.* after clean verification")
    p_import_bundle.add_argument("--json", action="store_true")
    p_import_bundle.set_defaults(func=cmd_import_bundle)

    p_fingerprint = sub.add_parser("fingerprint", help="print a stable local sync-state token")
    p_fingerprint.add_argument("--json", action="store_true")
    p_fingerprint.add_argument("--include-timestamps", action="store_true",
                               help="include generated_at/updated_at/age fields in the token")
    p_fingerprint.add_argument("--expect",
                               help="return nonzero unless the token starts with this value")
    p_fingerprint.set_defaults(func=cmd_fingerprint)

    p_compare = sub.add_parser("compare", help="compare local fingerprint with saved remote peer fingerprints")
    p_compare.add_argument("node_ids", nargs="*", help="optional peer node ids to compare")
    p_compare.add_argument("--json", action="store_true")
    p_compare.add_argument("--limit", type=int, default=8,
                           help="maximum component/error lines to print per peer (default: 8)")
    p_compare.set_defaults(func=cmd_compare)

    p_progress = sub.add_parser("progress", help="show lightweight local run-log progress")
    p_progress.add_argument("--json", action="store_true")
    p_progress.add_argument("--limit", type=int, default=10,
                            help="maximum recent/error logs to show (default: 10)")
    p_progress.add_argument("--scan-limit", type=int, default=200,
                            help="maximum newest logs to inspect for error keywords (default: 200)")
    p_progress.set_defaults(func=cmd_progress)

    p_history = sub.add_parser("history", help="show compact local sync history")
    p_history.add_argument("--json", action="store_true")
    p_history.add_argument("--limit", type=int, default=20,
                           help="maximum history entries to show (default: 20)")
    p_history.set_defaults(func=cmd_history)

    p_index = sub.add_parser("index", help="show the persistent verified artifact index")
    p_index.add_argument("--json", action="store_true")
    p_index.add_argument("--check", action="store_true",
                         help="recompute local checksums for indexed artifacts")
    p_index.set_defaults(func=cmd_index)

    p_inventory = sub.add_parser("inventory", help="summarize indexed artifacts as experiment leaves")
    p_inventory.add_argument("node_ids", nargs="*", help="optional peer node ids to show")
    p_inventory.add_argument("--json", action="store_true")
    p_inventory.add_argument("--csv", action="store_true",
                             help="emit one CSV row per indexed experiment leaf")
    p_inventory.add_argument("--only-incomplete", action="store_true",
                             help="show only leaves missing one or more expected artifacts")
    p_inventory.add_argument("--limit", type=int, default=20,
                             help="maximum leaves to print per peer in text mode (default: 20)")
    p_inventory.set_defaults(func=cmd_inventory)

    p_export = sub.add_parser("export", help="export trusted artifacts from the verified artifact index")
    p_export.add_argument("node_ids", nargs="*", help="optional peer node ids to export")
    p_export.add_argument("--json", action="store_true")
    p_export.add_argument("--csv", action="store_true",
                          help="emit one CSV row per trusted artifact")
    p_export.add_argument("--write", action="store_true",
                          help="write .syncmate/export_manifest.json and export_manifest.csv")
    p_export.add_argument("--include-incomplete", action="store_true",
                          help="include incomplete trusted leaves instead of exporting complete leaves only")
    p_export.add_argument("--check", action="store_true",
                          help="recompute local checksums before returning success")
    p_export.add_argument("--limit", type=int, default=20,
                          help="maximum leaves to print in text mode (default: 20)")
    p_export.set_defaults(func=cmd_export)

    p_results = sub.add_parser("results", help="extract trusted result metrics from the verified artifact index")
    p_results.add_argument("node_ids", nargs="*", help="optional peer node ids to extract")
    p_results.add_argument("--json", action="store_true")
    p_results.add_argument("--csv", action="store_true",
                           help="emit one CSV row per parsed trusted result")
    p_results.add_argument("--write", action="store_true",
                           help="write .syncmate/results_table.json and results_table.csv")
    p_results.add_argument("--include-incomplete", action="store_true",
                           help="include incomplete trusted leaves and report parse/missing errors")
    p_results.add_argument("--check", action="store_true",
                           help="recompute local checksums before returning success")
    p_results.add_argument("--limit", type=int, default=20,
                           help="maximum rows or parse errors to print in text mode (default: 20)")
    p_results.set_defaults(func=cmd_results)

    p_doctor = sub.add_parser("doctor", help="explain local sync issues and recommended actions")
    p_doctor.add_argument("--json", action="store_true")
    p_doctor.set_defaults(func=cmd_doctor)

    p_gate = sub.add_parser("gate", help="return pass/fail for automation based on sync diagnostics")
    p_gate.add_argument("--json", action="store_true")
    p_gate.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                        help="lowest diagnostic severity that fails the gate (default: warn)")
    p_gate.add_argument("--strict", action="store_true",
                        help="shortcut for --fail-on info")
    p_gate.add_argument("--require-verify", action="store_true",
                        help="require fresh clean verify reports and a passing artifact index check")
    p_gate.add_argument("--require-preflight", action="store_true",
                        help="require a fresh saved preflight report with no blocking errors")
    p_gate.add_argument("--require-results", action="store_true",
                        help="require .syncmate/results_table.* to match the trusted artifact index")
    p_gate.set_defaults(func=cmd_gate)

    p_summary = sub.add_parser("summary", help="print a compact sync status summary for humans or AI agents")
    p_summary.add_argument("--json", action="store_true")
    p_summary.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                           help="lowest diagnostic severity that fails the summary gate (default: warn)")
    p_summary.add_argument("--strict", action="store_true",
                           help="shortcut for --fail-on info")
    p_summary.add_argument("--require-verify", action="store_true",
                           help="include gate verification and artifact index integrity checks")
    p_summary.add_argument("--require-preflight", action="store_true",
                           help="include the saved preflight report in the summary gate")
    p_summary.add_argument("--require-results", action="store_true",
                           help="include trusted results-table gate checks")
    p_summary.add_argument("--max-diagnostics", type=int, default=5,
                           help="number of top diagnostics/actions to include (default: 5)")
    p_summary.set_defaults(func=cmd_summary)

    p_brief = sub.add_parser("brief", help="print or write a current-state AI handoff brief")
    p_brief.add_argument("--json", action="store_true")
    p_brief.add_argument("--write", action="store_true",
                         help="write .syncmate/brief.md")
    p_brief.add_argument("--require-verify", action="store_true", default=True,
                         help="include verification and artifact-index gate checks (default)")
    p_brief.add_argument("--no-require-verify", dest="require_verify", action="store_false",
                         help="omit the strict verification gate from this brief")
    p_brief.add_argument("--require-preflight", action="store_true",
                         help="include the saved preflight report in the brief gate")
    p_brief.add_argument("--require-results", action="store_true",
                         help="include trusted results-table gate checks")
    p_brief.add_argument("--limit", type=int, default=5,
                         help="maximum diagnostics, commands, and history entries to include (default: 5)")
    p_brief.set_defaults(func=cmd_brief)

    p_reports = sub.add_parser("reports", help="inspect compact saved peer reports without full manifests")
    p_reports.add_argument("node_ids", nargs="*", help="optional peer node ids to inspect")
    p_reports.add_argument("--json", action="store_true")
    p_reports.add_argument("--limit", type=int, default=5,
                           help="maximum examples/diagnostics per section (default: 5)")
    p_reports.set_defaults(func=cmd_reports)

    p_receipt = sub.add_parser("receipt", help="summarize latest collection and checksum evidence")
    p_receipt.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_receipt.add_argument("--json", action="store_true")
    p_receipt.add_argument("--write", action="store_true",
                           help="write .syncmate/receipt.md or receipt_<node_id>.md")
    p_receipt.add_argument("--limit", type=int, default=5,
                           help="maximum example artifacts per peer (default: 5)")
    p_receipt.set_defaults(func=cmd_receipt)

    p_sync = sub.add_parser("sync", help="one-shot peer sync: status, diff, collect, verify, results, checklist")
    p_sync.add_argument("node_ids", nargs="*", help="peer node ids; defaults to all configured peers")
    p_sync.add_argument("--json", action="store_true")
    p_sync.add_argument("--dry-run", action="store_true",
                        help="only refresh remote status and diff reports; do not collect or verify")
    p_sync.add_argument("--no-verify", action="store_true",
                        help="with apply mode, skip the final checksum acceptance report")
    p_sync.add_argument("--overwrite", action="store_true",
                        help="replace local files whose checksum differs")
    p_sync.add_argument("--no-dashboard", dest="dashboard", action="store_false",
                        default=True, help="do not write .syncmate/status.html")
    p_sync.add_argument("--no-receipt", dest="receipt", action="store_false",
                        default=True, help="do not write .syncmate/receipt*.md")
    p_sync.add_argument("--no-brief", dest="brief", action="store_false",
                        default=True, help="do not write .syncmate/brief.md")
    p_sync.add_argument("--no-checklist", dest="checklist", action="store_false",
                        default=True, help="do not write .syncmate/checklist.md")
    p_sync.add_argument("--no-results", dest="results", action="store_false",
                        default=True, help="do not write .syncmate/results_table.*")
    p_sync.add_argument("--no-write-state", dest="write_state", action="store_false",
                        default=True, help="do not write .syncmate/state.json or history")
    p_sync.add_argument("--limit", type=int, default=5,
                        help="maximum diagnostics, commands, and examples to include (default: 5)")
    p_sync.set_defaults(func=cmd_sync)

    p_workflow = sub.add_parser("workflow", help="show read-only sync automation stage state")
    p_workflow.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_workflow.add_argument("--json", action="store_true")
    p_workflow.add_argument("--write", action="store_true",
                            help="write .syncmate/workflow.json")
    p_workflow.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                            help="lowest diagnostic severity that fails the final gate (default: warn)")
    p_workflow.add_argument("--strict", action="store_true",
                            help="shortcut for --fail-on info")
    p_workflow.add_argument("--require-preflight", action="store_true",
                            help="require a fresh saved preflight report in the workflow gate")
    p_workflow.add_argument("--require-verify", action="store_true", default=True,
                            help="include verification and artifact-index gate checks (default)")
    p_workflow.add_argument("--no-require-verify", dest="require_verify", action="store_false",
                            help="omit the verification/index requirement from the final gate")
    p_workflow.add_argument("--require-results", action="store_true", default=True,
                            help="include trusted results-table gate checks (default)")
    p_workflow.add_argument("--no-require-results", dest="require_results", action="store_false",
                            help="omit trusted results-table freshness from the final gate")
    p_workflow.add_argument("--limit", type=int, default=12,
                            help="maximum next commands and failures to include (default: 12)")
    p_workflow.set_defaults(func=cmd_workflow)

    p_automation = sub.add_parser("automation-core", help="show the machine-readable transfer/checksum/results ledger")
    p_automation.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_automation.add_argument("--json", action="store_true")
    p_automation.add_argument("--write", action="store_true",
                              help="write .syncmate/automation_core.json and automation_core.md")
    p_automation.add_argument("--limit", type=int, default=8,
                              help="maximum examples to keep in nested payloads (default: 8)")
    p_automation.set_defaults(func=cmd_automation_core)

    p_acceptance = sub.add_parser("acceptance", help="show the final sync acceptance verdict")
    p_acceptance.add_argument("node_ids", nargs="*", help="optional peer node ids to include")
    p_acceptance.add_argument("--json", action="store_true")
    p_acceptance.add_argument("--write", action="store_true",
                              help="write .syncmate/acceptance.json")
    p_acceptance.add_argument("--fail-on", choices=("error", "warn", "info"), default="warn",
                              help="lowest diagnostic severity that blocks acceptance (default: warn)")
    p_acceptance.add_argument("--strict", action="store_true",
                              help="shortcut for --fail-on info")
    p_acceptance.add_argument("--require-preflight", dest="require_preflight", action="store_true",
                              default=True, help="require a fresh saved preflight report (default)")
    p_acceptance.add_argument("--no-require-preflight", dest="require_preflight", action="store_false",
                              help="omit saved preflight from acceptance")
    p_acceptance.add_argument("--require-verify", dest="require_verify", action="store_true",
                              default=True, help="require clean verify reports and artifact index (default)")
    p_acceptance.add_argument("--no-require-verify", dest="require_verify", action="store_false",
                              help="omit verification/index from acceptance")
    p_acceptance.add_argument("--require-results", dest="require_results", action="store_true",
                              default=True, help="require a fresh trusted results table (default)")
    p_acceptance.add_argument("--no-require-results", dest="require_results", action="store_false",
                              help="omit trusted results-table freshness from acceptance")
    p_acceptance.add_argument("--limit", type=int, default=8,
                              help="maximum failures, commands, and examples to include (default: 8)")
    p_acceptance.set_defaults(func=cmd_acceptance)

    p_next = sub.add_parser("next", help="print an ordered next-step command queue")
    p_next.add_argument("--json", action="store_true")
    p_next.add_argument("--write", action="store_true",
                        help="write .syncmate/action_plan.json and action_plan.md")
    p_next.add_argument("--require-verify", action="store_true",
                        help="end the queue with a verification gate")
    p_next.add_argument("--require-preflight", action="store_true",
                        help="require a fresh saved preflight report before the final gate/summary")
    p_next.add_argument("--require-results", action="store_true",
                        help="include trusted results-table refresh/check before the final gate/summary")
    p_next.add_argument("--limit", type=int, default=12,
                        help="maximum commands and manual actions to show (default: 12)")
    p_next.set_defaults(func=cmd_next)

    p_archive = sub.add_parser("archive-orphans", help="archive sync reports/index entries for unconfigured peers")
    p_archive.add_argument("--json", action="store_true")
    p_archive.add_argument("--apply", action="store_true",
                           help="move orphaned reports into .syncmate/archive/ and rewrite artifact_index.json")
    p_archive.set_defaults(func=cmd_archive_orphans)

    p_remote = sub.add_parser("remote-status", help="print read-only remote status command")
    p_remote.add_argument("node_id")
    p_remote.add_argument("--json", action="store_true")
    p_remote.add_argument("--apply", action="store_true",
                          help="execute the remote status command over SSH and save the snapshot")
    p_remote.add_argument("--no-save", action="store_true",
                          help="with --apply, do not write .syncmate/remote_status_<node_id>.json")
    p_remote.set_defaults(func=cmd_remote_status)

    p_collect = sub.add_parser("collect", help="print result collection plan")
    p_collect.add_argument("node_id")
    p_collect.add_argument("--json", action="store_true")
    p_collect.add_argument("--diff", action="store_true",
                           help="contact peer, compare manifests, and print missing/conflicting artifacts")
    p_collect.add_argument("--apply", action="store_true",
                           help="execute incremental artifact collection and checksum verification")
    p_collect.add_argument("--overwrite", action="store_true",
                           help="with --apply, replace local files whose checksum differs")
    p_collect.add_argument("--no-save", action="store_true",
                           help="with --diff/--apply, do not write last_diff/last_collect report files")
    p_collect.set_defaults(func=cmd_collect)

    p_verify = sub.add_parser("verify", help="verify local landing checksums against a peer manifest")
    p_verify.add_argument("node_id")
    p_verify.add_argument("--json", action="store_true")
    p_verify.add_argument("--apply", action="store_true",
                          help="contact peer and save .syncmate/last_verify_<node_id>.json")
    p_verify.add_argument("--no-save", action="store_true",
                          help="with --apply, do not write last_verify report files")
    p_verify.set_defaults(func=cmd_verify)

    p_handoff = sub.add_parser("handoff", help="print or write a peer runbook for local/remote AI agents")
    p_handoff.add_argument("node_ids", nargs="*",
                           help="peer node ids; defaults to all configured peers")
    p_handoff.add_argument("--json", action="store_true")
    p_handoff.add_argument("--write", action="store_true",
                           help="write .syncmate/handoff_<node_id>.md and handoff_all.md for multiple peers")
    p_handoff.set_defaults(func=cmd_handoff)

    p_refresh = sub.add_parser("refresh", help="update remote status, diff reports, and dashboard for peers")
    p_refresh.add_argument("node_ids", nargs="*", help="peer node ids; defaults to all configured peers")
    p_refresh.add_argument("--json", action="store_true")
    p_refresh.add_argument("--apply", action="store_true",
                           help="after diff, also fetch and verify missing artifacts")
    p_refresh.add_argument("--verify", action="store_true",
                           help="after diff/apply, also run checksum verification reports")
    p_refresh.add_argument("--overwrite", action="store_true",
                           help="with --apply, replace local files whose checksum differs")
    p_refresh.add_argument("--no-save", action="store_true",
                           help="do not write remote_status/last_diff/last_collect/last_verify report files")
    p_refresh.add_argument("--no-dashboard", dest="dashboard", action="store_false",
                           default=True, help="do not regenerate .syncmate/status.html")
    p_refresh.add_argument("--no-write-state", dest="write_state", action="store_false",
                           default=True, help="do not write .syncmate/state.json")
    p_refresh.set_defaults(func=cmd_refresh)

    p_integrate = sub.add_parser("integrate", help="print local integration plan")
    p_integrate.add_argument("--json", action="store_true")
    p_integrate.add_argument("--no-write-state", dest="write_state", action="store_false",
                             default=True, help="do not write .syncmate/state.json")
    p_integrate.set_defaults(func=cmd_integrate)

    p_manifest = sub.add_parser("manifest", help="emit artifact manifest for local roots")
    p_manifest.add_argument("--roots", nargs="+", default=["results/runs"])
    p_manifest.add_argument("--include", nargs="+",
                            help="artifact file names to include; default is attack.json collateral.json _meta.json")
    p_manifest.add_argument("--json", action="store_true")
    p_manifest.set_defaults(func=cmd_manifest)

    p_dashboard = sub.add_parser("dashboard", help="write .syncmate/status.html")
    p_dashboard.add_argument("--json", action="store_true")
    p_dashboard.add_argument("--open", action="store_true", help="open the generated status page")
    p_dashboard.add_argument("--no-write-state", dest="write_state", action="store_false",
                             default=True, help="do not write .syncmate/state.json")
    p_dashboard.set_defaults(func=cmd_dashboard)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
