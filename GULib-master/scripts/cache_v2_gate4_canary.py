#!/usr/bin/env python3
"""Run the fixed, isolated Cache V2 Gate 4 Cora/GIF/Degree canary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import torch
import yaml

from scripts.evaluation.reporting.events import read_event_stream
from scripts.evaluation.reporting.summary import (
    build_status_rows,
    write_status_views,
)

CONFIG_PATH = (
    REPO_ROOT / "experiments" / "configs" / "cache_v2_gate4_cora_degree_canary.yaml"
)
EVIDENCE_ROOT = REPO_ROOT / "results" / "runs" / "__syncmate_gate4_evidence__"
STORE_ROOT = REPO_ROOT / "results" / "cache_v2" / "syncmate_gate4"
RUNTIME_ROOT = REPO_ROOT / "results" / "runs" / "__syncmate_gate4_runtime__"
RUN_ROOT = REPO_ROOT / "results" / "runs" / "__syncmate_gate4__"
LEGACY_INVARIANT_ROOT = (
    REPO_ROOT / "results" / "runs" / "__syncmate_gate4_legacy_empty__"
)
AUTOREPORT_ROOT = EVIDENCE_ROOT / "autoreport"
EVENT_PATH = AUTOREPORT_ROOT / "auto_report.events.jsonl"
STATUS_MD_PATH = AUTOREPORT_ROOT / "AUTO_REPORT_STATUS.md"
STATUS_HTML_PATH = AUTOREPORT_ROOT / "AUTO_REPORT_STATUS.html"
CANONICAL_REPO_ROOT = REPO_ROOT
CANONICAL_PROCESSED_ROOT = CANONICAL_REPO_ROOT / "data" / "processed"
CANONICAL_CORA_PATH = (
    CANONICAL_PROCESSED_ROOT / "transductive" / "cora0.8_0_0.2.pkl"
)
CANONICAL_CORA_DATASET_PATH = (
    CANONICAL_PROCESSED_ROOT / "transductive" / "cora0.8_0_0.2dataset.pkl"
)
ACTIVE_RESULTS_ROOT = CANONICAL_REPO_ROOT / "results"
PROTECTED_ROOTS = {
    "result_cache": ACTIVE_RESULTS_ROOT / "cache",
    "selection_cache": ACTIVE_RESULTS_ROOT / "selection_cache",
    "score_cache": ACTIVE_RESULTS_ROOT / "score_cache",
    "active_cache_v2": ACTIVE_RESULTS_ROOT / "cache_v2",
    "journal_archive": ACTIVE_RESULTS_ROOT / "_journal",
    "canonical_cora": CANONICAL_CORA_PATH,
    "canonical_cora_dataset": CANONICAL_CORA_DATASET_PATH,
    "standard_gate4_log": CANONICAL_REPO_ROOT / "log" / "GIF" / "cora" / "GCN",
    "worktree_gate4_log": REPO_ROOT / "log" / "GIF" / "cora" / "GCN",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_digest(root: Path) -> Dict[str, Any]:
    if not root.exists():
        return {"exists": False, "file_count": 0, "size_bytes": 0, "sha256": None}
    if root.is_file():
        stat = root.stat()
        return {
            "exists": True,
            "file_count": 1,
            "size_bytes": stat.st_size,
            "sha256": _sha256_file(root),
        }
    digest = hashlib.sha256()
    count = 0
    size = 0
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        stat = path.stat()
        relative = path.relative_to(root).as_posix()
        content = _sha256_file(path)
        digest.update(relative.encode("utf-8") + b"\x00")
        digest.update(str(stat.st_size).encode("ascii") + b"\x00")
        digest.update(str(stat.st_mtime_ns).encode("ascii") + b"\x00")
        digest.update(content.encode("ascii") + b"\x00")
        count += 1
        size += stat.st_size
    return {
        "exists": True,
        "file_count": count,
        "size_bytes": size,
        "sha256": digest.hexdigest(),
    }


def _protected_snapshot() -> Dict[str, Any]:
    return {
        name: _tree_digest(path)
        for name, path in PROTECTED_ROOTS.items()
    }


def _portable_path(path: Path) -> str:
    return path.as_posix()


def _config() -> Dict[str, Any]:
    value = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("Gate 4 config must be a mapping")
    expected = {
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "processed_root": "data/processed",
        "runtime_root": "results/runs/__syncmate_gate4_runtime__",
        "run_root": "results/runs/__syncmate_gate4__",
    }
    for name, observed in expected.items():
        if value.get(name) != observed:
            raise RuntimeError(
                "Gate 4 config {0} is not frozen: {1!r}".format(
                    name, value.get(name)
                )
            )
    cache = value.get("cache_v2")
    if not isinstance(cache, Mapping):
        raise RuntimeError("Gate 4 config cache_v2 block is missing")
    if cache.get("store_root") != "results/cache_v2/syncmate_gate4":
        raise RuntimeError("Gate 4 store root is not isolated")
    if (
        cache.get("legacy_results_root")
        != "results/runs/__syncmate_gate4_legacy_empty__"
    ):
        raise RuntimeError("Gate 4 Legacy invariant root is not isolated")
    for forbidden in ("dataset_root", "allow_download", "processed_root"):
        if forbidden in cache:
            raise RuntimeError(
                "dataset ownership leaked into cache_v2.{0}".format(forbidden)
            )
    return value


def _run(
    name: str,
    argv: Sequence[str],
    *,
    env: Mapping[str, str],
    timeout: int,
    expect_success: bool = True,
) -> Dict[str, Any]:
    completed = subprocess.run(
        list(argv),
        cwd=str(REPO_ROOT),
        env=dict(env),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    logs = EVIDENCE_ROOT / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "{0}.stdout.log".format(name)).write_text(
        completed.stdout, encoding="utf-8"
    )
    (logs / "{0}.stderr.log".format(name)).write_text(
        completed.stderr, encoding="utf-8"
    )
    if expect_success and completed.returncode != 0:
        raise RuntimeError(
            "{0} failed with rc={1}".format(name, completed.returncode)
        )
    if not expect_success and completed.returncode == 0:
        raise RuntimeError("{0} unexpectedly succeeded".format(name))
    payload = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
    return {
        "returncode": completed.returncode,
        "stdout_log": str(logs / "{0}.stdout.log".format(name)),
        "stderr_log": str(logs / "{0}.stderr.log".format(name)),
        "payload": payload,
    }


def _selection_canary_args(mode: str, store_root: Path) -> Sequence[str]:
    return (
        sys.executable,
        "-m",
        "scripts.cache_v2_selection_canary",
        mode,
        "--store-root",
        str(store_root),
        "--processed-root",
        str(CANONICAL_PROCESSED_ROOT),
        "--legacy-results-root",
        str(LEGACY_INVARIANT_ROOT),
        "--dataset",
        "cora",
        "--base-model",
        "GCN",
        "--method",
        "GIF",
        "--strategy",
        "degree",
        "--seed",
        "42",
        "--selection-ratio",
        "0.05",
    )


def _single_result(document: Mapping[str, Any], label: str) -> Dict[str, Any]:
    results = document.get("results")
    if not isinstance(results, list) or len(results) != 1:
        raise RuntimeError("{0} must contain exactly one result".format(label))
    result = results[0]
    if not isinstance(result, dict):
        raise RuntimeError("{0} result must be a mapping".format(label))
    return result


def _phase_projection(events: Sequence[Mapping[str, Any]]) -> Dict[str, str]:
    completed_indices = {}
    for index, event in enumerate(events):
        if event.get("state") == "completed":
            completed_indices[str(event.get("stage"))] = index
    required = ("selection", "attack", "collateral", "run")
    missing = [stage for stage in required if stage not in completed_indices]
    if missing:
        raise RuntimeError(
            "AutoReport is missing completed stages: {0}".format(",".join(missing))
        )
    states = {}
    for stage in required:
        rows, _ = build_status_rows(
            events[: completed_indices[stage] + 1],
            max_cells=10,
        )
        if len(rows) != 1:
            raise RuntimeError("AutoReport projection did not yield one cell")
        states[stage] = str(rows[0]["state"])
    expected = {
        "selection": "selection-only",
        "attack": "attack-only",
        "collateral": "collateral",
        "run": "complete",
    }
    if states != expected:
        raise RuntimeError(
            "AutoReport phased projection changed: {0}".format(states)
        )
    return states


def _validate_run_artifacts(
    selection_artifact_id: str,
) -> Dict[str, Any]:
    leaf = RUN_ROOT / "cora_GCN_r0.05" / "GIF_degree" / "seed42"
    paths = {
        name: leaf / name
        for name in ("attack.json", "collateral.json", "predictions.npz", "_meta.json")
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise RuntimeError(
            "Gate 4 run leaf is incomplete: {0}".format(",".join(missing))
        )
    attack = json.loads(paths["attack.json"].read_text(encoding="utf-8"))
    collateral = json.loads(paths["collateral.json"].read_text(encoding="utf-8"))
    meta = json.loads(paths["_meta.json"].read_text(encoding="utf-8"))
    attack_nodes = tuple(
        int(item)
        for item in attack["results"]["degree"]["selected_nodes"]
    )
    with np.load(paths["predictions.npz"], allow_pickle=False) as archive:
        prediction_nodes = tuple(
            int(item) for item in archive["degree__selected_nodes"].tolist()
        )
        logits_shapes = {
            name: list(archive["degree__" + name].shape)
            for name in (
                "logits_before",
                "logits_unlearned",
                "logits_retrained",
            )
        }
    if attack_nodes != prediction_nodes:
        raise RuntimeError("attack and collateral did not consume the same Selection")
    selection_meta = meta.get("selection_artifact")
    if not isinstance(selection_meta, dict):
        raise RuntimeError("_meta selection_artifact is missing")
    if selection_meta.get("artifact_id") != selection_artifact_id:
        raise RuntimeError("_meta references the wrong Selection Artifact")
    collateral_rows = collateral.get("results")
    if not isinstance(collateral_rows, list) or len(collateral_rows) != 1:
        raise RuntimeError("collateral result is incomplete")
    return {
        "leaf": str(leaf),
        "files": {
            name: {
                "sha256": _sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
            for name, path in paths.items()
        },
        "selected_node_count": len(attack_nodes),
        "selection_artifact_id": selection_artifact_id,
        "selection_order_exact": True,
        "logits_shapes": logits_shapes,
    }


def _integrity_probe(
    *,
    env: Mapping[str, str],
    selection_payload_path: Path,
) -> Dict[str, Any]:
    probe_store = EVIDENCE_ROOT / "integrity-probe" / "store"
    shutil.copytree(STORE_ROOT, probe_store)
    relative = selection_payload_path.resolve().relative_to(STORE_ROOT.resolve())
    probe_payload = probe_store / relative
    probe_payload.write_bytes(probe_payload.read_bytes() + b" ")
    observed = _run(
        "integrity-probe",
        _selection_canary_args("warm", probe_store),
        env=env,
        timeout=300,
        expect_success=False,
    )
    combined = (
        Path(observed["stdout_log"]).read_text(encoding="utf-8")
        + Path(observed["stderr_log"]).read_text(encoding="utf-8")
    ).lower()
    if not any(
        token in combined
        for token in ("integrity", "canonical", "content hash", "payload")
    ):
        raise RuntimeError("integrity probe failed for an unrelated reason")
    return {
        "returncode": observed["returncode"],
        "tampered_store": str(probe_store),
        "fail_closed": True,
        "legacy_fallback": False,
        "stdout_log": observed["stdout_log"],
        "stderr_log": observed["stderr_log"],
    }


def run_gate4_canary() -> Dict[str, Any]:
    _config()
    missing_canonical = [
        path
        for path in (CANONICAL_CORA_PATH, CANONICAL_CORA_DATASET_PATH)
        if not path.is_file()
    ]
    if missing_canonical:
        raise RuntimeError(
            "canonical Cora processed artifacts are missing: {0}".format(
                ", ".join(str(path) for path in missing_canonical)
            )
        )
    if EVIDENCE_ROOT.exists():
        raise RuntimeError(
            "Gate 4 evidence root already exists; cold canary refuses reuse"
        )
    if RUN_ROOT.exists():
        raise RuntimeError(
            "Gate 4 SyncMate result root already exists; cold canary refuses reuse"
        )
    if not torch.cuda.is_available():
        raise RuntimeError("Gate 4 requires one available CUDA device")

    protected_before = _protected_snapshot()
    cora_before = {
        "sha256": _sha256_file(CANONICAL_CORA_PATH),
        "size_bytes": CANONICAL_CORA_PATH.stat().st_size,
        "mtime_ns": CANONICAL_CORA_PATH.stat().st_mtime_ns,
    }
    EVIDENCE_ROOT.mkdir(parents=True)
    env = os.environ.copy()
    env.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHON_BIN": sys.executable,
            "OPENGU_AUTOREPORT_EVENT_PATH": str(EVENT_PATH),
        }
    )

    cold = _run(
        "selection-cold",
        _selection_canary_args("cold", STORE_ROOT),
        env=env,
        timeout=600,
    )
    if not isinstance(cold["payload"], dict):
        raise RuntimeError("cold Selection canary did not return JSON")
    cold_result = _single_result(cold["payload"], "cold Selection")
    if cold_result.get("producer_called") is not True or cold_result.get("hit"):
        raise RuntimeError("cold Selection was not an upstream MISS production")
    artifact_id = str(cold_result["artifact_id"])
    selection_payload_path = Path(str(cold_result["payload_path"]))
    store_before_runner = _tree_digest(STORE_ROOT)

    runner = _run(
        "runner",
        (
            sys.executable,
            "experiments/run.py",
            str(CONFIG_PATH),
            "--limit",
            "1",
        ),
        env=env,
        timeout=3000,
    )
    run_artifacts = _validate_run_artifacts(artifact_id)

    warm = _run(
        "selection-warm",
        _selection_canary_args("warm", STORE_ROOT),
        env=env,
        timeout=600,
    )
    if not isinstance(warm["payload"], dict):
        raise RuntimeError("warm Selection canary did not return JSON")
    warm_result = _single_result(warm["payload"], "warm Selection")
    if warm_result.get("hit") is not True or warm_result.get("producer_called"):
        raise RuntimeError("warm Selection did not exact-hit with zero producer calls")
    if warm_result.get("artifact_id") != artifact_id:
        raise RuntimeError("warm Selection resolved a different Artifact")
    store_after_warm = _tree_digest(STORE_ROOT)
    if store_after_warm != store_before_runner:
        raise RuntimeError("runner/warm path modified the exact-hit Selection store")

    events, event_warnings = read_event_stream(EVENT_PATH)
    if event_warnings:
        raise RuntimeError(
            "AutoReport event stream has warnings: {0}".format(event_warnings)
        )
    phase_states = _phase_projection(events)
    selection_events = [
        event
        for event in events
        if event.get("stage") == "selection"
        and event.get("state") == "completed"
    ]
    if len(selection_events) != 1:
        raise RuntimeError("AutoReport must contain one completed selection stage")
    observations = selection_events[0].get("cache") or []
    if len(observations) != 1:
        raise RuntimeError("AutoReport selection cache observation is missing")
    observation = observations[0]
    observed_artifact = observation.get("artifact") or {}
    if (
        observation.get("authoritative") is not True
        or observation.get("hit_source") != "cache_v2:{0}".format(artifact_id)
        or observation.get("lookup_policy") != "cache_v2_exact_artifact_id"
        or observed_artifact.get("artifact_id") != artifact_id
        or not observation.get("recipe_hash")
    ):
        raise RuntimeError("AutoReport Cache authority/source/Recipe is incorrect")
    write_status_views(
        event_path=EVENT_PATH,
        markdown_path=STATUS_MD_PATH,
        html_path=STATUS_HTML_PATH,
        max_cells=10,
        baseline_path=AUTOREPORT_ROOT / "no-baseline.json",
    )
    markdown = STATUS_MD_PATH.read_text(encoding="utf-8")
    for token in (
        "complete",
        "selection:hit[authoritative]",
        artifact_id,
        "cache_v2_exact_artifact_id",
        str(observation["recipe_hash"])[:12],
    ):
        if token not in markdown:
            raise RuntimeError(
                "AutoReport status view is missing {0}".format(token)
            )

    integrity = _integrity_probe(
        env=env,
        selection_payload_path=selection_payload_path,
    )
    protected_after = _protected_snapshot()
    if protected_after != protected_before:
        raise RuntimeError("Gate 4 modified an active Cache/Legacy/journal root")
    cora_after = {
        "sha256": _sha256_file(CANONICAL_CORA_PATH),
        "size_bytes": CANONICAL_CORA_PATH.stat().st_size,
        "mtime_ns": CANONICAL_CORA_PATH.stat().st_mtime_ns,
    }
    if cora_after != cora_before:
        raise RuntimeError("Gate 4 modified canonical processed Cora")

    return {
        "gate": "cache-v2-gate4",
        "passed": True,
        "status": "accepted",
        "git_sha": subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            text=True,
        ).strip(),
        "config_path": str(CONFIG_PATH),
        "config_sha256": _sha256_file(CONFIG_PATH),
        "evidence_root": str(EVIDENCE_ROOT),
        "syncmate_result_root": str(RUN_ROOT),
        "cuda": {
            "available": True,
            "device_count": torch.cuda.device_count(),
            "device_name": torch.cuda.get_device_name(0),
        },
        "selection": {
            "artifact_id": artifact_id,
            "recipe_hash": cold_result["recipe_hash"],
            "content_hash": cold_result["content_hash"],
            "cold_producer_called": True,
            "warm_hit": True,
            "warm_producer_called": False,
            "store_unchanged_after_runner_and_warm": True,
        },
        "runner": {
            "returncode": runner["returncode"],
            "stdout_log": runner["stdout_log"],
            "stderr_log": runner["stderr_log"],
            "artifacts": run_artifacts,
        },
        "generated_artifacts": [
            str(
                Path(run_artifacts["leaf"])
                .joinpath(name)
                .resolve()
                .relative_to(REPO_ROOT.resolve())
            ).replace("\\", "/")
            for name in (
                "attack.json",
                "collateral.json",
                "predictions.npz",
                "_meta.json",
            )
        ],
        "autoreport": {
            "events": str(EVENT_PATH),
            "event_count": len(events),
            "phase_states": phase_states,
            "authority": True,
            "hit_source": observation["hit_source"],
            "lookup_policy": observation["lookup_policy"],
            "recipe_hash": observation["recipe_hash"],
            "markdown": str(STATUS_MD_PATH),
            "html": str(STATUS_HTML_PATH),
        },
        "integrity_probe": integrity,
        "protected_roots_unchanged": True,
        "protected_roots": protected_before,
        "canonical_cora_unchanged": True,
        "canonical_cora": cora_before,
        "downloads_performed": False,
        "full_cache_rebuild_performed": False,
        "tracin_hybrid_modified": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    document = run_gate4_canary()
    report_path = EVIDENCE_ROOT / "acceptance.json"
    report_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.json:
        print(json.dumps(document, ensure_ascii=False, sort_keys=True))
    else:
        print("Gate 4 accepted: {0}".format(report_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
