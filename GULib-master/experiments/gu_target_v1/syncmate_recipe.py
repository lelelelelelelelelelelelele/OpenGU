"""Run the fixed Cora/seed42/k7/GNNDelete public-profile GU gate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

import torch
import yaml

from experiments.gu_target_v1.adapter import materialize_grandfathered_selection
from experiments.gu_target_v1.public_profile import verify_public_profile


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "experiments" / "configs" / "syncmate_small_selection_gu_gate_v5.yaml"
EVIDENCE_ROOT = Path("/autodl-fs/data/OpenGU-small-selection-gu/20260722/gate-v5")
RUN_ROOT = REPO_ROOT / "results" / "runs" / "__syncmate_small_selection_gu_v5__"
EXPECTED_LEAF = RUN_ROOT / "cora_GCN_r0.05" / "GNNDelete_degree" / "seed42"
ARTIFACT_NAMES = ("attack.json", "collateral.json", "predictions.npz", "_meta.json")
CONFIG_SCHEMA = "gu_target_v1.syncmate_gate"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_path(value: Any) -> Path:
    path = Path(str(value)).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def _config() -> Dict[str, Any]:
    value = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("GU gate config must be a mapping")
    expected = {
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "processed_profile": "planetoid_public_fixed",
        "methods": ["GNNDelete"],
        "strategies": ["degree"],
        "seeds": [42],
        "selection_k": 7,
        "processed_root": "/autodl-fs/data/OpenGU/GULib-master/data/processed",
        "runtime_root": "/autodl-fs/data/OpenGU-small-selection-gu/20260722/gate-v5/runtime",
        "run_root": "results/runs/__syncmate_small_selection_gu_v5__",
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise RuntimeError("GU gate config is not frozen: {0}".format(field))
    if value.get("claims") != {
        "lane": "controlled_public_profile_gu",
        "infrastructure_gate": True,
        "scientific_comparison": False,
        "canonical_opengu_80_20": False,
        "expands_after_gate_only": True,
    }:
        raise RuntimeError("GU gate claim boundary is not frozen")
    cache = value.get("cache_v2") or {}
    if cache.get("mode") != "external_selection":
        raise RuntimeError("GU gate must consume an external Selection manifest")
    defaults = value.get("defaults") or {}
    if (
        defaults.get("num_epochs") != 100
        or defaults.get("run_collateral") is not True
        or defaults.get("save_predictions") is not True
        or defaults.get("no_cache") is not True
    ):
        raise RuntimeError("GU gate runtime defaults are not formal")
    return value


def _git_state() -> Dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), *args], text=True
        ).strip()

    return {
        "sha": run("rev-parse", "HEAD"),
        "branch": run("branch", "--show-current"),
        "status": run("status", "--porcelain=v1", "--untracked-files=all").splitlines(),
    }


def preflight_recipe(config_path: Path = CONFIG_PATH) -> Dict[str, Any]:
    errors = []
    if Path(config_path).resolve() != CONFIG_PATH.resolve():
        errors.append("GU gate config path differs from the reviewed path")
    try:
        cfg = _config()
    except Exception as exc:
        return {"ready": False, "errors": ["config: {0}".format(exc)]}
    git = _git_state()
    if REPO_ROOT != Path("/autodl-fs/data/OpenGU/GULib-master"):
        errors.append("formal GU gate requires the SSH active checkout")
    if git["branch"] != "main" or git["status"]:
        errors.append("formal GU gate requires a clean main checkout")
    if not torch.cuda.is_available():
        errors.append("formal GU gate requires CUDA")
    elif "RTX 4090" not in torch.cuda.get_device_name(0):
        errors.append("formal GU gate requires the reviewed RTX 4090 runner")
    source = cfg["selection_source"]
    source_summary = _repo_path(source["summary_path"])
    benchmark_manifest = _repo_path(source["benchmark_manifest_path"])
    for path, expected_hash, label in (
        (source_summary, source["summary_sha256"], "Selection summary"),
        (benchmark_manifest, source["benchmark_manifest_sha256"], "benchmark manifest"),
    ):
        if not path.is_file():
            errors.append("{0} is missing".format(label))
        elif _sha256_file(path) != expected_hash:
            errors.append("{0} SHA-256 differs from the reviewed config".format(label))
    profile = None
    try:
        profile = verify_public_profile(
            repository_root=REPO_ROOT,
            processed_root=Path(cfg["processed_root"]),
            dataset="Cora",
        )
        observed_source = profile["manifest"]["dataset_source"]["source_fingerprint"]
        if observed_source != source["canonical_public_source_fingerprint"]:
            errors.append("canonical public dataset fingerprint changed")
    except Exception as exc:
        errors.append("processed public profile: {0}".format(exc))
    for path, label in ((EVIDENCE_ROOT, "evidence root"), (RUN_ROOT, "result root")):
        if path.exists():
            errors.append("cold GU gate {0} already exists".format(label))
    return {
        "schema": CONFIG_SCHEMA,
        "ready": not errors,
        "errors": errors,
        "config_path": str(CONFIG_PATH),
        "config_sha256": _sha256_file(CONFIG_PATH),
        "git": git,
        "cuda": {
            "available": torch.cuda.is_available(),
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "processed_profile": None if profile is None else profile["manifest_path"],
    }


def _validate_artifacts(selection_manifest: Mapping[str, Any]) -> Dict[str, Any]:
    missing = [name for name in ARTIFACT_NAMES if not (EXPECTED_LEAF / name).is_file()]
    if missing:
        raise RuntimeError("GU gate result leaf is incomplete: {0}".format(missing))
    attack = json.loads((EXPECTED_LEAF / "attack.json").read_text(encoding="utf-8"))
    result = (attack.get("results") or {}).get("degree") or {}
    if result.get("failed") is True or result.get("selected_nodes") != selection_manifest["cells"][0]["selected_nodes"]:
        raise RuntimeError("GU attack result failed or changed the selected-node order")
    collateral = json.loads((EXPECTED_LEAF / "collateral.json").read_text(encoding="utf-8"))
    rows = [row for row in collateral.get("results") or [] if row.get("strategy") == "degree"]
    if len(rows) != 1:
        raise RuntimeError("GU collateral result has no unique degree row")
    meta = json.loads((EXPECTED_LEAF / "_meta.json").read_text(encoding="utf-8"))
    artifact = meta.get("selection_artifact") or {}
    expected_artifact = selection_manifest["cells"][0]["artifact"]
    if (
        artifact.get("artifact_id") != expected_artifact.get("artifact_id")
        or artifact.get("recipe_hash") != expected_artifact.get("recipe_hash")
        or artifact.get("content_hash") != expected_artifact.get("content_hash")
        or artifact.get("strategy") != "degree"
        or artifact.get("k") != 7
        or artifact.get("authoritative") is not True
    ):
        raise RuntimeError("GU result metadata is not bound to the exact Selection Artifact")
    return {
        "leaf": str(EXPECTED_LEAF),
        "attack_failed": False,
        "collateral_rows": len(rows),
        "selection_artifact_id": artifact["artifact_id"],
        "artifact_sha256": {
            name: _sha256_file(EXPECTED_LEAF / name) for name in ARTIFACT_NAMES
        },
    }


def run_gate() -> Dict[str, Any]:
    preflight = preflight_recipe(CONFIG_PATH)
    if not preflight["ready"]:
        raise RuntimeError("GU gate preflight blocked: {0}".format(preflight["errors"]))
    cfg = _config()
    source = cfg["selection_source"]
    cache = cfg["cache_v2"]
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats(0)
    started = time.perf_counter()
    selection_manifest = materialize_grandfathered_selection(
        repository_root=REPO_ROOT,
        processed_root=Path(cfg["processed_root"]),
        source_summary_path=_repo_path(source["summary_path"]),
        source_summary_sha256=source["summary_sha256"],
        benchmark_manifest_path=_repo_path(source["benchmark_manifest_path"]),
        benchmark_manifest_sha256=source["benchmark_manifest_sha256"],
        expected_experiment_git_sha=source["experiment_git_sha"],
        expected_public_source_fingerprint=source[
            "canonical_public_source_fingerprint"
        ],
        dataset="Cora",
        seed=42,
        strategies=cfg["strategies"],
        k=int(cfg["selection_k"]),
        base_model=cfg["base_model"],
        gu_methods=cfg["methods"],
        store_root=Path(cache["store_root"]),
        manifest_path=Path(cache["manifest_path"]),
    )
    completed = subprocess.run(
        [sys.executable, "experiments/run.py", str(CONFIG_PATH), "--limit", "1"],
        cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHON_BIN": sys.executable},
        capture_output=True,
        text=True,
        timeout=3600,
        check=False,
    )
    logs = EVIDENCE_ROOT / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "runner.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (logs / "runner.stderr.log").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError("GU runner failed with rc={0}".format(completed.returncode))
    validation = _validate_artifacts(selection_manifest)
    elapsed = time.perf_counter() - started
    peak_allocated = int(torch.cuda.max_memory_allocated(0)) if torch.cuda.is_available() else 0
    peak_reserved = int(torch.cuda.max_memory_reserved(0)) if torch.cuda.is_available() else 0
    return {
        "schema": "gu_target_v1.syncmate_gate_result",
        "version": 1,
        "passed": True,
        "status": "accepted-infrastructure-gate",
        "git_sha": preflight["git"]["sha"],
        "hostname": socket.gethostname(),
        "config_path": str(CONFIG_PATH),
        "config_sha256": _sha256_file(CONFIG_PATH),
        "lane": cfg["claims"]["lane"],
        "scientific_comparison": False,
        "dataset": "Cora",
        "seed": 42,
        "k": 7,
        "gu_method": "GNNDelete",
        "selector": "degree",
        "source_selection": selection_manifest["source"],
        "selection_manifest": str(Path(cache["manifest_path"])),
        "selection_artifact": selection_manifest["cells"][0]["artifact"],
        "runtime": {
            "total_seconds": elapsed,
            "peak_gpu_allocated_bytes": peak_allocated,
            "peak_gpu_reserved_bytes": peak_reserved,
        },
        "validation": validation,
        "generated_artifacts": [
            str((EXPECTED_LEAF / name).relative_to(REPO_ROOT)).replace("\\", "/")
            for name in ARTIFACT_NAMES
        ],
        "errors": [],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.config.resolve() != CONFIG_PATH.resolve():
        raise SystemExit("only the reviewed GU gate config is accepted")
    payload = preflight_recipe(args.config) if args.preflight_only else run_gate()
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        print("GU gate: {0}".format("passed" if payload.get("passed") else "blocked"))
    return 0 if payload.get("passed", payload.get("ready")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
