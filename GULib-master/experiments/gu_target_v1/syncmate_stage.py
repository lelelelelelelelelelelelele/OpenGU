"""Run one reviewed dataset/seed stage of the 17-selector GU matrix."""

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
from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np
import torch
import yaml

from experiments.bc_target_v2.recipe import SCORE_NAMES
from experiments.gu_target_v1.adapter import (
    load_external_selection_manifest,
    materialize_grandfathered_selection,
)
from experiments.gu_target_v1.public_profile import PROFILE, verify_public_profile
from experiments.path_policy import resolve_owned_path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = (
    REPO_ROOT / "experiments" / "configs" / "syncmate_small_selection_gu_full_v5.yaml"
)
EVIDENCE_ROOT = (
    REPO_ROOT
    / "results"
    / "runs"
    / "__syncmate_small_selection_gu_full_v5_evidence__"
)
RUN_ROOT = REPO_ROOT / "results" / "runs" / "__syncmate_small_selection_gu_full_v5__"
ARTIFACT_NAMES = ("attack.json", "collateral.json", "predictions.npz", "_meta.json")
DATASETS = ("cora", "citeseer", "pubmed")
SEEDS = (42, 212, 2024)
STAGES = tuple("{0}-seed{1}".format(dataset, seed) for dataset in DATASETS for seed in SEEDS)
CONFIG_SCHEMA = "gu_target_v1.syncmate_stage"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_path(value: Any) -> Path:
    return resolve_owned_path(REPO_ROOT, value, "GU stage path")


def parse_stage(stage: str) -> Tuple[str, int]:
    if stage not in STAGES:
        raise ValueError("stage is outside the reviewed 3x3 matrix")
    dataset, seed_text = stage.rsplit("-seed", 1)
    return dataset, int(seed_text)


def _config() -> Dict[str, Any]:
    value = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("full GU config must be a mapping")
    expected = {
        "base_model": "GCN",
        "processed_profile": PROFILE,
        "methods": ["GNNDelete"],
        "strategies": list(SCORE_NAMES),
        "seeds": list(SEEDS),
        "selection_k": 7,
        "processed_root": "data/processed",
        "evidence_root": (
            "results/runs/__syncmate_small_selection_gu_full_v5_evidence__"
        ),
        "run_root": "results/runs/__syncmate_small_selection_gu_full_v5__",
        "selection_experiment_git_sha": "9240b9a7bd61b17b4c841981ec2892fdf100dc4b",
        "benchmark_manifest_sha256": "3212232a4274190e4c5a075eeea20fc92f982e7f4293670037795c2932e0e479",
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise RuntimeError("full GU config is not frozen: {0}".format(field))
    if set(value.get("datasets") or {}) != set(DATASETS):
        raise RuntimeError("full GU config dataset set is not frozen")
    claims = value.get("claims") or {}
    if claims != {
        "lane": "controlled_public_profile_gu",
        "scientific_comparison": True,
        "canonical_opengu_80_20": False,
        "gate_required": True,
        "selectors": 17,
        "datasets": 3,
        "seeds": 3,
        "total_cells": 153,
    }:
        raise RuntimeError("full GU claim boundary is not frozen")
    defaults = value.get("defaults") or {}
    if (
        defaults.get("num_epochs") != 100
        or defaults.get("run_collateral") is not True
        or defaults.get("save_predictions") is not True
        or defaults.get("no_cache") is not True
    ):
        raise RuntimeError("full GU runtime defaults are not formal")
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


def _stage_paths(stage: str, cfg: Mapping[str, Any]) -> Dict[str, Path]:
    dataset, seed = parse_stage(stage)
    root = EVIDENCE_ROOT / stage
    dataset_cfg = cfg["datasets"][dataset]
    return {
        "root": root,
        "runtime": root / "runtime",
        "store": root / "store",
        "manifest": root / "selection_manifest.json",
        "runtime_config": root / "runtime_config.yaml",
        "logs": root / "logs",
        "source_summary": _repo_path(dataset_cfg["summaries"][str(seed)]["path"]),
        "benchmark_manifest": _repo_path(cfg["benchmark_manifest_path"]),
    }


def _expected_leaf(dataset: str, strategy: str, seed: int, ratio: float) -> Path:
    return (
        RUN_ROOT
        / "{0}_GCN_r{1}".format(dataset, ratio)
        / "GNNDelete_{0}".format(strategy)
        / "seed{0}".format(seed)
    )


def expected_artifacts(stage: str, cfg: Mapping[str, Any] | None = None) -> Tuple[str, ...]:
    cfg = dict(cfg or _config())
    dataset, seed = parse_stage(stage)
    ratio = float(cfg["datasets"][dataset]["ratio"])
    paths = []
    for strategy in SCORE_NAMES:
        leaf = _expected_leaf(dataset, strategy, seed, ratio)
        paths.extend(
            str((leaf / name).relative_to(REPO_ROOT)).replace("\\", "/")
            for name in ARTIFACT_NAMES
        )
    return tuple(paths)


def _projected_config(stage: str, cfg: Mapping[str, Any]) -> Dict[str, Any]:
    dataset, seed = parse_stage(stage)
    dataset_cfg = cfg["datasets"][dataset]
    paths = _stage_paths(stage, cfg)
    return {
        "name": "syncmate_small_selection_gu_full_v5__{0}".format(stage),
        "dataset": dataset,
        "base_model": cfg["base_model"],
        "ratio": float(dataset_cfg["ratio"]),
        "processed_profile": cfg["processed_profile"],
        "methods": list(cfg["methods"]),
        "strategies": list(cfg["strategies"]),
        "seeds": [seed],
        "processed_root": cfg["processed_root"],
        "runtime_root": str(paths["runtime"]),
        "run_root": cfg["run_root"],
        "selection_k": int(cfg["selection_k"]),
        "defaults": dict(cfg["defaults"]),
        "model_overrides": dict(cfg["model_overrides"]),
        "cache_v2": {
            "mode": "external_selection",
            "store_root": str(paths["store"]),
            "manifest_path": str(paths["manifest"]),
            "legacy_results_root": str(paths["root"] / "legacy-empty"),
        },
        "extra_args": list(cfg["extra_args"]),
        "claims": {
            "lane": cfg["claims"]["lane"],
            "scientific_comparison": True,
            "canonical_opengu_80_20": False,
            "parent_config_sha256": _sha256_file(CONFIG_PATH),
            "stage": stage,
        },
    }


def _gate_errors(cfg: Mapping[str, Any], git_sha: str) -> Sequence[str]:
    gate = cfg["required_gate"]
    leaf = _repo_path(gate["result_root"]) / gate["leaf"]
    errors = []
    for name in ARTIFACT_NAMES:
        if not (leaf / name).is_file():
            errors.append("required GU gate artifact is missing: {0}".format(name))
    if errors:
        return errors
    try:
        attack = json.loads((leaf / "attack.json").read_text(encoding="utf-8"))
        meta = json.loads((leaf / "_meta.json").read_text(encoding="utf-8"))
        if ((attack.get("results") or {}).get("degree") or {}).get("failed") is True:
            errors.append("required GU gate attack failed")
        if meta.get("git_sha") != git_sha:
            errors.append("required GU gate was not produced by the current main SHA")
        artifact = meta.get("selection_artifact") or {}
        if artifact.get("strategy") != "degree" or artifact.get("k") != 7:
            errors.append("required GU gate Selection identity changed")
    except Exception as exc:
        errors.append("required GU gate is invalid: {0}".format(exc))
    return errors


def preflight_stage(stage: str, config_path: Path = CONFIG_PATH) -> Dict[str, Any]:
    errors = []
    try:
        dataset, seed = parse_stage(stage)
    except Exception as exc:
        return {"ready": False, "errors": [str(exc)]}
    if Path(config_path).resolve() != CONFIG_PATH.resolve():
        errors.append("full GU config path differs from the reviewed path")
    try:
        cfg = _config()
    except Exception as exc:
        return {"ready": False, "errors": ["config: {0}".format(exc)]}
    git = _git_state()
    if REPO_ROOT != Path("/autodl-fs/data/OpenGU/GULib-master"):
        errors.append("formal GU stage requires the SSH active checkout")
    if git["branch"] != "main" or git["status"]:
        errors.append("formal GU stage requires a clean main checkout")
    if not torch.cuda.is_available():
        errors.append("formal GU stage requires CUDA")
    elif "RTX 4090" not in torch.cuda.get_device_name(0):
        errors.append("formal GU stage requires the reviewed RTX 4090 runner")
    errors.extend(_gate_errors(cfg, git["sha"]))

    dataset_cfg = cfg["datasets"][dataset]
    paths = _stage_paths(stage, cfg)
    summary_cfg = dataset_cfg["summaries"][str(seed)]
    for path, expected_hash, label in (
        (paths["source_summary"], summary_cfg["sha256"], "Selection summary"),
        (paths["benchmark_manifest"], cfg["benchmark_manifest_sha256"], "benchmark manifest"),
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
            dataset=dataset_cfg["display_name"],
        )
        observed = profile["manifest"]["dataset_source"]["source_fingerprint"]
        if observed != dataset_cfg["canonical_public_source_fingerprint"]:
            errors.append("canonical public dataset fingerprint changed")
    except Exception as exc:
        errors.append("processed public profile: {0}".format(exc))

    store_exists = paths["store"].exists()
    manifest_exists = paths["manifest"].is_file()
    if store_exists != manifest_exists:
        errors.append("GU stage has an incomplete Selection adapter checkpoint")
    ratio = float(dataset_cfg["ratio"])
    for strategy in SCORE_NAMES:
        meta_path = _expected_leaf(dataset, strategy, seed, ratio) / "_meta.json"
        if meta_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if meta.get("git_sha") != git["sha"]:
                    errors.append("existing GU stage leaf crosses Git SHA: {0}".format(strategy))
            except Exception as exc:
                errors.append("existing GU stage metadata is invalid: {0}: {1}".format(strategy, exc))
    return {
        "schema": CONFIG_SCHEMA,
        "ready": not errors,
        "errors": errors,
        "stage": stage,
        "dataset": dataset_cfg["display_name"],
        "seed": seed,
        "config_path": str(CONFIG_PATH),
        "config_sha256": _sha256_file(CONFIG_PATH),
        "git": git,
        "cuda": {
            "available": torch.cuda.is_available(),
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "processed_profile": None if profile is None else profile["manifest_path"],
        "resume": store_exists,
    }


def _ensure_selection_manifest(
    stage: str, cfg: Mapping[str, Any], projected: Mapping[str, Any]
) -> Dict[str, Any]:
    dataset, seed = parse_stage(stage)
    dataset_cfg = cfg["datasets"][dataset]
    paths = _stage_paths(stage, cfg)
    summary_cfg = dataset_cfg["summaries"][str(seed)]
    if not paths["manifest"].exists():
        return materialize_grandfathered_selection(
            repository_root=REPO_ROOT,
            processed_root=Path(cfg["processed_root"]),
            source_summary_path=paths["source_summary"],
            source_summary_sha256=summary_cfg["sha256"],
            benchmark_manifest_path=paths["benchmark_manifest"],
            benchmark_manifest_sha256=cfg["benchmark_manifest_sha256"],
            expected_experiment_git_sha=cfg["selection_experiment_git_sha"],
            expected_public_source_fingerprint=dataset_cfg[
                "canonical_public_source_fingerprint"
            ],
            dataset=dataset_cfg["display_name"],
            seed=seed,
            strategies=cfg["strategies"],
            k=int(cfg["selection_k"]),
            base_model=cfg["base_model"],
            gu_methods=cfg["methods"],
            store_root=paths["store"],
            manifest_path=paths["manifest"],
        )
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    source = manifest.get("source") or {}
    if (
        source.get("selection_summary_sha256") != summary_cfg["sha256"]
        or source.get("benchmark_manifest_sha256") != cfg["benchmark_manifest_sha256"]
        or source.get("experiment_git_sha") != cfg["selection_experiment_git_sha"]
        or source.get("canonical_public_source_fingerprint")
        != dataset_cfg["canonical_public_source_fingerprint"]
    ):
        raise RuntimeError("resumed Selection manifest source identity changed")
    load_external_selection_manifest(
        projected,
        manifest_path=paths["manifest"],
        expected_store_root=paths["store"],
        processed_root=Path(cfg["processed_root"]),
    )
    return manifest


def _write_runtime_config(path: Path, projected: Mapping[str, Any]) -> None:
    payload = yaml.safe_dump(dict(projected), sort_keys=False, allow_unicode=True)
    if path.exists() and path.read_text(encoding="utf-8") != payload:
        raise RuntimeError("resumed GU stage runtime config changed")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def _validate_stage_artifacts(
    stage: str, cfg: Mapping[str, Any], manifest: Mapping[str, Any], git_sha: str
) -> Dict[str, Any]:
    dataset, seed = parse_stage(stage)
    ratio = float(cfg["datasets"][dataset]["ratio"])
    manifest_cells = {cell["strategy"]: cell for cell in manifest["cells"]}
    validations = []
    for strategy in SCORE_NAMES:
        leaf = _expected_leaf(dataset, strategy, seed, ratio)
        missing = [name for name in ARTIFACT_NAMES if not (leaf / name).is_file()]
        if missing:
            raise RuntimeError("GU stage result leaf is incomplete: {0}: {1}".format(strategy, missing))
        attack = json.loads((leaf / "attack.json").read_text(encoding="utf-8"))
        attack_row = (attack.get("results") or {}).get(strategy) or {}
        if (
            attack_row.get("failed") is True
            or attack_row.get("selected_nodes") != manifest_cells[strategy]["selected_nodes"]
        ):
            raise RuntimeError("GU attack failed or changed selected-node order: {0}".format(strategy))
        collateral = json.loads((leaf / "collateral.json").read_text(encoding="utf-8"))
        collateral_rows = [
            row for row in collateral.get("results") or [] if row.get("strategy") == strategy
        ]
        if len(collateral_rows) != 1:
            raise RuntimeError("GU collateral row is missing or ambiguous: {0}".format(strategy))
        meta = json.loads((leaf / "_meta.json").read_text(encoding="utf-8"))
        artifact = meta.get("selection_artifact") or {}
        expected_artifact = manifest_cells[strategy]["artifact"]
        if (
            meta.get("git_sha") != git_sha
            or meta.get("strategy") != strategy
            or meta.get("seed") != seed
            or artifact.get("artifact_id") != expected_artifact.get("artifact_id")
            or artifact.get("recipe_hash") != expected_artifact.get("recipe_hash")
            or artifact.get("content_hash") != expected_artifact.get("content_hash")
            or artifact.get("strategy") != strategy
            or artifact.get("k") != 7
            or artifact.get("authoritative") is not True
        ):
            raise RuntimeError("GU metadata provenance changed: {0}".format(strategy))
        with np.load(leaf / "predictions.npz") as predictions:
            if "{0}__selected_nodes".format(strategy) not in predictions.files:
                raise RuntimeError("GU prediction bundle is missing selector identity: {0}".format(strategy))
        validations.append(
            {
                "strategy": strategy,
                "artifact_id": artifact["artifact_id"],
                "attack_total_seconds": attack_row.get("total_time"),
                "unlearn_seconds": attack_row.get("unlearn_time"),
                "selection_reuse_seconds": attack_row.get("selection_reuse_time"),
                "collateral": collateral_rows[0],
                "sha256": {name: _sha256_file(leaf / name) for name in ARTIFACT_NAMES},
            }
        )
    return {"accepted_cells": len(validations), "cells": validations}


def run_stage(stage: str) -> Dict[str, Any]:
    preflight = preflight_stage(stage, CONFIG_PATH)
    if not preflight["ready"]:
        raise RuntimeError("GU stage preflight blocked: {0}".format(preflight["errors"]))
    cfg = _config()
    paths = _stage_paths(stage, cfg)
    projected = _projected_config(stage, cfg)
    manifest = _ensure_selection_manifest(stage, cfg, projected)
    _write_runtime_config(paths["runtime_config"], projected)
    started = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, "experiments/run.py", str(paths["runtime_config"])],
        cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHON_BIN": sys.executable},
        capture_output=True,
        text=True,
        timeout=21600,
        check=False,
    )
    paths["logs"].mkdir(parents=True, exist_ok=True)
    (paths["logs"] / "runner.stdout.log").write_text(completed.stdout, encoding="utf-8")
    (paths["logs"] / "runner.stderr.log").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError("GU stage runner failed with rc={0}".format(completed.returncode))
    validation = _validate_stage_artifacts(stage, cfg, manifest, preflight["git"]["sha"])
    dataset, seed = parse_stage(stage)
    return {
        "schema": "gu_target_v1.syncmate_stage_result",
        "version": 1,
        "passed": True,
        "status": "accepted-scientific-stage",
        "git_sha": preflight["git"]["sha"],
        "hostname": socket.gethostname(),
        "config_path": str(CONFIG_PATH),
        "config_sha256": _sha256_file(CONFIG_PATH),
        "stage": stage,
        "dataset": cfg["datasets"][dataset]["display_name"],
        "seed": seed,
        "k": 7,
        "gu_method": "GNNDelete",
        "selectors": list(SCORE_NAMES),
        "scientific_comparison": True,
        "selection_manifest": str(paths["manifest"]),
        "runtime": {"total_seconds": time.perf_counter() - started},
        "validation": validation,
        "generated_artifacts": list(expected_artifacts(stage, cfg)),
        "errors": [],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.config.resolve() != CONFIG_PATH.resolve():
        raise SystemExit("only the reviewed full GU config is accepted")
    payload = (
        preflight_stage(args.stage, args.config)
        if args.preflight_only
        else run_stage(args.stage)
    )
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        print("GU stage {0}: {1}".format(args.stage, "passed" if payload.get("passed") else "blocked"))
    return 0 if payload.get("passed", payload.get("ready")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
