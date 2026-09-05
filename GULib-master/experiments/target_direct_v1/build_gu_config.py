"""Generate a runnable GU YAML bound to one target-direct manifest digest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import yaml

from experiments.target_direct_v1.build_manifest import SCHEMA, VERSION, sha256_file


def build_gu_config(
    *,
    manifest_path: Path,
    processed_root: Path,
    runtime_root: Path,
    run_root: Path,
    unlearning_refs: Sequence[Path] | None = None,
) -> dict:
    manifest_path = Path(manifest_path).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("version") != VERSION:
        raise ValueError("target-direct manifest schema/version mismatch")
    if manifest.get("parameter_scope") != "last_layer":
        raise ValueError("formal target-direct GU config requires last_layer")
    budget = manifest.get("budget") or {}
    if (
        float(budget.get("ratio", -1)) != float(manifest.get("ratio", -2))
        or budget.get("denominator") != "train_candidate_count"
        or budget.get("rounding") != "floor_with_minimum_one"
        or int(budget.get("denominator_count", -1))
        != int(manifest.get("candidate_count", -2))
        or int(budget.get("expected_k", -1))
        != int(manifest.get("expected_k", -2))
    ):
        raise ValueError("target-direct manifest budget contract mismatch")
    resolved = {}
    for path, label in (
        (processed_root, "processed_root"),
        (runtime_root, "runtime_root"),
        (run_root, "run_root"),
    ):
        supplied = Path(path).expanduser()
        if not supplied.is_absolute():
            raise ValueError("{0} must be absolute".format(label))
        resolved[label] = supplied.resolve()
    from experiments.modular_config import load_instance
    refs = [Path(path).resolve() for path in unlearning_refs] if unlearning_refs is not None else [
        Path(__file__).resolve().parents[1] / 'configs/target_direct_formal_v2/unlearning' / name
        for name in ('gnndelete.yaml', 'retrain.yaml')]
    instances = [load_instance(path, 'unlearning') for path in refs]
    if not instances or len({item['method'] for item in instances}) != len(instances):
        raise ValueError('each configured method requires one independent YAML')
    return {
        "name": "target_direct_v1_{0}_r{1}".format(
            manifest["dataset"], manifest["ratio"]
        ),
        "dataset": manifest["dataset"],
        "base_model": "GCN",
        "processed_profile": manifest["processed_profile"],
        "split": {
            key: value
            for key, value in manifest["split_contract"].items()
            if key != "processed_profile"
        },
        "ratio": float(manifest["ratio"]),
        "methods": [item['method'] for item in instances],
        "unlearning_refs": [str(path) for path in refs],
        "strategies": list(manifest["strategies"]),
        "seeds": [int(value) for value in manifest["seeds"]],
        "processed_root": str(resolved["processed_root"]),
        "runtime_root": str(resolved["runtime_root"]),
        "run_root": str(resolved["run_root"]),
        "cache_v2": {
            "mode": "target_direct_external_selection",
            "store_root": manifest["store_root"],
            "legacy_results_root": str(resolved["runtime_root"] / "results"),
            "manifest_path": str(manifest_path),
            "manifest_sha256": sha256_file(manifest_path),
        },
        "defaults": {
            "save_predictions": True,
            "run_collateral": False,
            "run_update_detection_auc": True,
            "no_cache": True,
            "num_epochs": 100,
            "batch_size": 64,
            "cuda": 0,
        },
        "model_overrides": {
            "GCN": {"gcn_num_layers": 2, "gcn_hidden": 64}
        },
        "extra_args": ["--num_threads", "1"],
        "claims": {
            "white_box_target_direct": True,
            "target_checkpoint_reused_exactly": True,
            "budget_denominator": "train_candidate_count",
            "deletion_ratio": float(manifest["ratio"]),
            "expected_k": int(manifest["expected_k"]),
            "parameter_scope": "last_layer",
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest_path = args.manifest.expanduser().resolve()
    config = build_gu_config(
        manifest_path=manifest_path,
        processed_root=args.processed_root,
        runtime_root=args.runtime_root,
        run_root=args.run_root,
    )
    output = args.output.expanduser().resolve()
    if output.exists():
        raise FileExistsError("GU config already exists: {0}".format(output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "cells": len(config["methods"])
                * len(config["strategies"])
                * len(config["seeds"]),
                "manifest_sha256": config["cache_v2"]["manifest_sha256"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
