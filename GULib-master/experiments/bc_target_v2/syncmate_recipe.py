"""Bounded SyncMate executor for the formal small-graph Selection benchmark.

The queue selects one reviewed YAML configuration.  It never supplies commands,
paths, or experiment arguments dynamically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

import torch
import yaml

from .dataset_source import canonical_data_root, resolve_planetoid_public_source
from .recipe import SCORE_NAMES


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_SCHEMA = "bc_target_v2.syncmate_small_selection_recipe"
CONFIG_VERSION = 1
CELL_RECEIPT_SCHEMA = "bc_target_v2.syncmate_selection_cell"
CELL_RECEIPT_VERSION = 1
ALLOWED_STAGES = ("mvp", "dataset_gate", "full")
CONFIG_KEYS = {
    "schema",
    "version",
    "recipe_id",
    "stage",
    "datasets",
    "seeds",
    "budgets",
    "device",
    "required_device_name",
    "data_root",
    "cache_root",
    "output_root",
    "timeout_seconds",
    "resume",
    "require_empty_roots",
    "required_prior_cells",
}


class SyncMateSelectionRecipeError(RuntimeError):
    """A reviewed recipe or its runtime evidence is invalid."""


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SyncMateSelectionRecipeError("JSON root is not an object: {0}".format(path))
    return value


def _repo_path(root: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise SyncMateSelectionRecipeError("{0} must be a non-empty repo-relative path".format(label))
    supplied = Path(value)
    if supplied.is_absolute():
        raise SyncMateSelectionRecipeError("{0} must be repo-relative".format(label))
    resolved = (root / supplied).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise SyncMateSelectionRecipeError("{0} escapes the repository".format(label)) from exc
    return resolved


def _unique_strings(value: Any, label: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise SyncMateSelectionRecipeError("{0} must be a non-empty string list".format(label))
    result = tuple(value)
    if len(set(result)) != len(result):
        raise SyncMateSelectionRecipeError("{0} contains duplicates".format(label))
    return result


def _unique_ints(value: Any, label: str) -> Tuple[int, ...]:
    if not isinstance(value, list) or not value or not all(isinstance(item, int) for item in value):
        raise SyncMateSelectionRecipeError("{0} must be a non-empty integer list".format(label))
    result = tuple(value)
    if len(set(result)) != len(result) or any(item < 0 for item in result):
        raise SyncMateSelectionRecipeError("{0} must contain unique non-negative integers".format(label))
    return result


def load_recipe_config(
    config_path: Path, *, repository_root: Optional[Path] = None
) -> Mapping[str, Any]:
    root = (repository_root or REPO_ROOT).resolve()
    path = Path(config_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SyncMateSelectionRecipeError("recipe config is outside the repository") from exc
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SyncMateSelectionRecipeError("recipe config root must be a mapping")
    unknown = sorted(set(value) - CONFIG_KEYS)
    missing = sorted(CONFIG_KEYS - set(value))
    if unknown or missing:
        raise SyncMateSelectionRecipeError(
            "recipe config keys mismatch: missing={0} unknown={1}".format(missing, unknown)
        )
    if value["schema"] != CONFIG_SCHEMA or value["version"] != CONFIG_VERSION:
        raise SyncMateSelectionRecipeError("recipe schema/version mismatch")
    if value["stage"] not in ALLOWED_STAGES:
        raise SyncMateSelectionRecipeError("unsupported recipe stage")
    datasets = _unique_strings(value["datasets"], "datasets")
    if any(item not in ("Cora", "CiteSeer", "PubMed") for item in datasets):
        raise SyncMateSelectionRecipeError("datasets are outside the reviewed Planetoid set")
    seeds = _unique_ints(value["seeds"], "seeds")
    budgets = _unique_ints(value["budgets"], "budgets")
    if tuple(sorted(budgets, reverse=True)) != budgets:
        raise SyncMateSelectionRecipeError("budgets must be unique and descending")
    if value["device"] != "cuda":
        raise SyncMateSelectionRecipeError("formal SyncMate recipe must require CUDA")
    if not isinstance(value["required_device_name"], str) or not value["required_device_name"].strip():
        raise SyncMateSelectionRecipeError("required_device_name must be non-empty")
    if not isinstance(value["timeout_seconds"], int) or value["timeout_seconds"] <= 0:
        raise SyncMateSelectionRecipeError("timeout_seconds must be positive")
    for key in ("resume", "require_empty_roots"):
        if not isinstance(value[key], bool):
            raise SyncMateSelectionRecipeError("{0} must be boolean".format(key))
    prior = _unique_strings(value["required_prior_cells"], "required_prior_cells") if value["required_prior_cells"] else ()
    expected_labels = {
        "{0}_seed{1}".format(dataset.lower(), seed)
        for dataset in datasets
        for seed in seeds
    }
    if any(label not in expected_labels for label in prior):
        raise SyncMateSelectionRecipeError("required_prior_cells is outside the configured matrix")
    data_root = _repo_path(root, value["data_root"], "data_root")
    cache_root = _repo_path(root, value["cache_root"], "cache_root")
    output_root = _repo_path(root, value["output_root"], "output_root")
    if data_root != canonical_data_root(root).resolve():
        raise SyncMateSelectionRecipeError("data_root is not the canonical checkout-local data/raw")
    expected_cache_parent = (root / "results" / "cache_v2").resolve()
    expected_output_parent = (root / "results" / "runs").resolve()
    if expected_cache_parent not in cache_root.parents:
        raise SyncMateSelectionRecipeError("cache_root must be below results/cache_v2")
    if expected_output_parent not in output_root.parents:
        raise SyncMateSelectionRecipeError("output_root must be below results/runs")
    return {
        **value,
        "datasets": datasets,
        "seeds": seeds,
        "budgets": budgets,
        "required_prior_cells": prior,
        "config_path": path,
        "repository_root": root,
        "data_root_resolved": data_root,
        "cache_root_resolved": cache_root,
        "output_root_resolved": output_root,
    }


def _git_state(root: Path) -> Mapping[str, Any]:
    def run(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout.strip()

    return {
        "head": run("rev-parse", "HEAD"),
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "status_short": run("status", "--short", "--untracked-files=all").splitlines(),
    }


def _prior_manifest_errors(config: Mapping[str, Any], head: str) -> Sequence[str]:
    required = tuple(config["required_prior_cells"])
    if not required:
        return ()
    manifest_path = Path(config["output_root_resolved"]) / "benchmark_manifest.json"
    if not manifest_path.is_file():
        return ("required prior benchmark manifest is missing",)
    try:
        manifest = _load_json(manifest_path)
    except Exception as exc:
        return ("required prior benchmark manifest is invalid: {0}".format(exc),)
    if manifest.get("experiment_git_sha") != head:
        return ("prior benchmark Git SHA differs from runner HEAD",)
    cells = {
        "{0}_seed{1}".format(str(cell.get("dataset", "")).lower(), cell.get("seed")): cell
        for cell in manifest.get("cells", ())
        if isinstance(cell, dict)
    }
    errors = []
    for label in required:
        cell = cells.get(label)
        if not isinstance(cell, dict) or cell.get("status") != "success":
            errors.append("required prior cell is not accepted: {0}".format(label))
    return tuple(errors)


def preflight_recipe(
    config_path: Path,
    *,
    repository_root: Optional[Path] = None,
    require_gpu: bool = True,
) -> Mapping[str, Any]:
    errors = []
    try:
        config = load_recipe_config(config_path, repository_root=repository_root)
    except Exception as exc:
        return {"ready": False, "errors": [str(exc)]}
    git = _git_state(Path(config["repository_root"]))
    if git["status_short"]:
        errors.append("runner worktree is dirty")
    if config["require_empty_roots"]:
        for label in ("cache_root_resolved", "output_root_resolved"):
            root = Path(config[label])
            if root.exists() and any(root.iterdir()):
                errors.append("{0} is not empty".format(label.replace("_resolved", "")))
    errors.extend(_prior_manifest_errors(config, str(git["head"])))
    dataset_sources = {}
    for dataset in config["datasets"]:
        try:
            dataset_sources[dataset] = resolve_planetoid_public_source(
                Path(config["data_root_resolved"]),
                repository_root=Path(config["repository_root"]),
                dataset=dataset,
            ).to_manifest()
        except Exception as exc:
            errors.append("{0} dataset preflight failed: {1}".format(dataset, exc))
    gpu = {
        "required": bool(require_gpu),
        "available": bool(torch.cuda.is_available()),
        "count": int(torch.cuda.device_count()),
        "device_name": None,
    }
    if require_gpu:
        if not gpu["available"] or gpu["count"] < 1:
            errors.append("CUDA GPU is not available")
        else:
            gpu["device_name"] = str(torch.cuda.get_device_name(torch.cuda.current_device()))
            if config["required_device_name"].lower() not in gpu["device_name"].lower():
                errors.append(
                    "GPU is not the required device: expected {0}, observed {1}".format(
                        config["required_device_name"], gpu["device_name"]
                    )
                )
    return {
        "ready": not errors,
        "recipe_id": config["recipe_id"],
        "stage": config["stage"],
        "git": git,
        "gpu": gpu,
        "dataset_sources": dataset_sources,
        "errors": errors,
    }


def cell_artifact_paths(config: Mapping[str, Any]) -> Tuple[str, ...]:
    root = Path(config["repository_root"])
    output = Path(config["output_root_resolved"])
    paths = []
    for dataset in config["datasets"]:
        for seed in config["seeds"]:
            leaf = output / "cells" / "{0}_seed{1}".format(dataset.lower(), seed)
            for name in ("cold.json", "warm.json", "cell.json"):
                paths.append((leaf / name).relative_to(root).as_posix())
    return tuple(paths)


def _validate_cell(
    config: Mapping[str, Any], cell: Mapping[str, Any], expected_head: str
) -> Mapping[str, Any]:
    dataset = str(cell.get("dataset"))
    seed = int(cell.get("seed"))
    label = "{0}_seed{1}".format(dataset.lower(), seed)
    leaf = Path(config["output_root_resolved"]) / "cells" / label
    cold_path = leaf / "cold.json"
    warm_path = leaf / "warm.json"
    if not cold_path.is_file() or not warm_path.is_file():
        raise SyncMateSelectionRecipeError("cell summaries are missing: {0}".format(label))
    cold = _load_json(cold_path)
    warm = _load_json(warm_path)
    if cell.get("status") != "success" or cold.get("cache", {}).get("hit") is not False:
        raise SyncMateSelectionRecipeError("cold evidence is invalid: {0}".format(label))
    if warm.get("cache", {}).get("hit") is not True:
        raise SyncMateSelectionRecipeError("warm evidence is not an exact hit: {0}".format(label))
    if cold.get("selection_cache", {}).get("miss_saved_count") != len(SCORE_NAMES):
        raise SyncMateSelectionRecipeError("cold Selection count is not 17: {0}".format(label))
    if warm.get("selection_cache", {}).get("hit_count") != len(SCORE_NAMES):
        raise SyncMateSelectionRecipeError("warm Selection hit count is not 17: {0}".format(label))
    if cold.get("git_provenance", {}).get("head") != expected_head:
        raise SyncMateSelectionRecipeError("cell Git SHA differs from runner HEAD: {0}".format(label))
    if cold.get("git_provenance", {}).get("worktree_dirty"):
        raise SyncMateSelectionRecipeError("cell recorded a dirty worktree: {0}".format(label))
    source = cold.get("dataset_source") or {}
    if not source.get("canonical_root_match"):
        raise SyncMateSelectionRecipeError("cell did not use canonical data root: {0}".format(label))
    gpu = (cold.get("gpu_memory") or {}).get("score_bundle") or {}
    device_name = str(gpu.get("device_name") or "")
    if config["required_device_name"].lower() not in device_name.lower():
        raise SyncMateSelectionRecipeError("cell did not run on the required GPU: {0}".format(label))
    if not isinstance(cell.get("peak_gpu_allocated_bytes"), int) or cell["peak_gpu_allocated_bytes"] <= 0:
        raise SyncMateSelectionRecipeError("cell has no peak allocated GPU evidence: {0}".format(label))
    if not isinstance(cell.get("peak_gpu_reserved_bytes"), int) or cell["peak_gpu_reserved_bytes"] <= 0:
        raise SyncMateSelectionRecipeError("cell has no peak reserved GPU evidence: {0}".format(label))
    methods = cell.get("methods") or {}
    if set(methods) != set(SCORE_NAMES):
        raise SyncMateSelectionRecipeError("cell method set is not the formal 17 outputs: {0}".format(label))
    if any(
        item.get("status") != "success"
        or item.get("cold_cache_hit") is not False
        or item.get("warm_cache_hit") is not True
        for item in methods.values()
    ):
        raise SyncMateSelectionRecipeError("cell method-level cold/warm contract failed: {0}".format(label))
    receipt = {
        "schema": CELL_RECEIPT_SCHEMA,
        "version": CELL_RECEIPT_VERSION,
        "dataset": dataset,
        "seed": seed,
        "status": "success",
        "experiment_git_sha": expected_head,
        "formal_score_count": len(SCORE_NAMES),
        "source_fingerprint": source.get("source_fingerprint"),
        "score_artifact_id": cell.get("score_artifact_id"),
        "device": cell.get("device"),
        "device_name": device_name,
        "peak_gpu_allocated_bytes": cell.get("peak_gpu_allocated_bytes"),
        "peak_gpu_reserved_bytes": cell.get("peak_gpu_reserved_bytes"),
        "score_bundle_cold_total_seconds": cell.get("score_bundle_cold_total_seconds"),
        "score_bundle_warm_read_seconds": cell.get("score_bundle_warm_read_seconds"),
        "cold_sha256": _sha256_file(cold_path),
        "warm_sha256": _sha256_file(warm_path),
    }
    receipt_path = leaf / "cell.json"
    payload = _canonical_json_bytes(receipt)
    if receipt_path.exists() and receipt_path.read_bytes() != payload:
        raise SyncMateSelectionRecipeError("existing cell receipt conflicts: {0}".format(label))
    if not receipt_path.exists():
        receipt_path.write_bytes(payload)
    return receipt


def validate_benchmark_result(
    config: Mapping[str, Any], *, expected_head: str
) -> Mapping[str, Any]:
    manifest_path = Path(config["output_root_resolved"]) / "benchmark_manifest.json"
    manifest = _load_json(manifest_path)
    if manifest.get("experiment_git_sha") != expected_head:
        raise SyncMateSelectionRecipeError("benchmark manifest Git SHA mismatch")
    if tuple(manifest.get("datasets") or ()) != tuple(config["datasets"]):
        raise SyncMateSelectionRecipeError("benchmark manifest dataset matrix mismatch")
    if tuple(manifest.get("seeds") or ()) != tuple(config["seeds"]):
        raise SyncMateSelectionRecipeError("benchmark manifest seed matrix mismatch")
    if manifest.get("formal_score_count") != len(SCORE_NAMES):
        raise SyncMateSelectionRecipeError("benchmark manifest score count is not 17")
    expected = {
        (dataset, seed)
        for dataset in config["datasets"]
        for seed in config["seeds"]
    }
    cells = manifest.get("cells") or []
    observed = {
        (str(cell.get("dataset")), int(cell.get("seed")))
        for cell in cells
        if isinstance(cell, dict) and cell.get("seed") is not None
    }
    if observed != expected or len(cells) != len(expected):
        raise SyncMateSelectionRecipeError("benchmark manifest cell matrix mismatch")
    receipts = [_validate_cell(config, cell, expected_head) for cell in cells]
    return {
        "manifest": manifest_path.relative_to(Path(config["repository_root"])).as_posix(),
        "cells": receipts,
        "generated_artifacts": list(cell_artifact_paths(config)),
    }


def execute_recipe(config_path: Path) -> Mapping[str, Any]:
    config = load_recipe_config(config_path)
    preflight = preflight_recipe(config_path)
    if not preflight["ready"]:
        return {
            "passed": False,
            "recipe_id": config["recipe_id"],
            "stage": config["stage"],
            "preflight": preflight,
            "generated_artifacts": [],
            "errors": preflight["errors"],
        }
    head = str(preflight["git"]["head"])
    output = Path(config["output_root_resolved"])
    command = [
        sys.executable,
        "-m",
        "experiments.bc_target_v2.benchmark_selection",
        "--data-root",
        str(config["data_root_resolved"]),
        "--cache-root",
        str(config["cache_root_resolved"]),
        "--output-root",
        str(output),
        "--report-md",
        str(output / "benchmark_report.md"),
        "--report-html",
        str(output / "benchmark_report.html"),
        "--datasets",
        ",".join(config["datasets"]),
        "--seeds",
        ",".join(str(item) for item in config["seeds"]),
        "--budgets",
        ",".join(str(item) for item in config["budgets"]),
        "--device",
        "cuda",
        "--timeout-seconds",
        str(config["timeout_seconds"]),
        "--experiment-git-sha",
        head,
    ]
    if config["resume"]:
        command.append("--resume")
    completed = subprocess.run(
        command,
        cwd=Path(config["repository_root"]),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        return {
            "passed": False,
            "recipe_id": config["recipe_id"],
            "stage": config["stage"],
            "preflight": preflight,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-16000:],
            "stderr": completed.stderr[-16000:],
            "generated_artifacts": [],
            "errors": ["benchmark exited with code {0}".format(completed.returncode)],
        }
    try:
        evidence = validate_benchmark_result(config, expected_head=head)
    except Exception as exc:
        return {
            "passed": False,
            "recipe_id": config["recipe_id"],
            "stage": config["stage"],
            "preflight": preflight,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-16000:],
            "stderr": completed.stderr[-16000:],
            "generated_artifacts": [],
            "errors": [str(exc)],
        }
    return {
        "passed": True,
        "recipe_id": config["recipe_id"],
        "stage": config["stage"],
        "preflight": preflight,
        "command": command,
        "returncode": completed.returncode,
        **evidence,
        "errors": [],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = (
            preflight_recipe(args.config)
            if args.preflight_only
            else execute_recipe(args.config)
        )
    except Exception as exc:
        data = {"passed": False, "ready": False, "generated_artifacts": [], "errors": [str(exc)]}
    if args.json:
        print(json.dumps(data, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data.get("passed", data.get("ready", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
