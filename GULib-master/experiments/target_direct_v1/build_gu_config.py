"""Generate a runnable GU YAML bound to one target-direct manifest digest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import yaml

from experiments.target_direct_v1.build_manifest import SCHEMA, VERSION, sha256_file


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest_path = args.manifest.expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("version") != VERSION:
        raise ValueError("target-direct manifest schema/version mismatch")
    for path, label in (
        (args.processed_root, "processed_root"),
        (args.runtime_root, "runtime_root"),
        (args.run_root, "run_root"),
    ):
        if not path.expanduser().is_absolute():
            raise ValueError("{0} must be absolute".format(label))
    config = {
        "name": "target_direct_v1_{0}_r{1}".format(
            manifest["dataset"], manifest["ratio"]
        ),
        "dataset": manifest["dataset"],
        "base_model": "GCN",
        "processed_profile": manifest["processed_profile"],
        "ratio": float(manifest["ratio"]),
        "methods": ["GNNDelete"],
        "strategies": list(manifest["strategies"]),
        "seeds": [int(value) for value in manifest["seeds"]],
        "processed_root": str(args.processed_root.expanduser().resolve()),
        "runtime_root": str(args.runtime_root.expanduser().resolve()),
        "run_root": str(args.run_root.expanduser().resolve()),
        "cache_v2": {
            "mode": "target_direct_external_selection",
            "store_root": manifest["store_root"],
            "legacy_results_root": str(
                args.runtime_root.expanduser().resolve() / "results"
            ),
            "manifest_path": str(manifest_path),
            "manifest_sha256": sha256_file(manifest_path),
        },
        "defaults": {
            "save_predictions": True,
            "run_collateral": True,
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
            "expected_k": int(manifest["expected_k"]),
        },
    }
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
