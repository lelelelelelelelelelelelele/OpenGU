"""Clean k=5 random-baseline rerun for the paper's Cora noise anchor.

The run starts from the canonical ``results/baseline/k5_random`` directory;
the pre-v2 evidence is preserved in ``k5_random_OLD_20260227``.  By default
the canonical root must contain no JSON artifacts; pass
``--resume`` only to reuse schema-validated v2 cells after an interruption.
It covers the entire Cora x {GCN, GAT} six-method scorecard,
uses five independent baseline seeds, and writes ``method_perf_before`` for
every retained cell.

Usage (on the formal GPU checkout):
    PYTHON=/path/to/python python experiments/baseline_k5/rerun_cora_noise_anchor.py
"""
from __future__ import annotations

import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

from run_all_baselines import (
    BASELINE_K,
    BASELINE_ROOT,
    SEEDS,
    compute_averaged_baseline,
    run_single_baseline,
)
from baseline_contract import SCHEMA, SCHEMA_VERSION


DATASET = "cora"
BACKBONES = ("GCN", "GAT")
METHODS = ("GIF", "GNNDelete", "GraphEraser", "GraphRevoker", "IDEA", "MEGU")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reuse only compatible v2 cells already present in the canonical root",
    )
    return parser


def _git_provenance():
    repo_root = Path(__file__).resolve().parents[2]
    sha = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        text=True,
        encoding="utf-8",
    ).strip()
    dirty = bool(
        subprocess.check_output(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            text=True,
            encoding="utf-8",
        ).strip()
    )
    return {"git_sha": sha, "git_dirty": dirty}


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    existing = list(BASELINE_ROOT.rglob("*.json")) if BASELINE_ROOT.exists() else []
    if existing and not args.resume:
        print(
            f"Refusing non-empty v2 root ({len(existing)} JSON files): {BASELINE_ROOT}"
        )
        print("Use --resume to validate and reuse v2 artifacts; nothing is overwritten.")
        return 2

    summary = []
    failures = []
    total = len(BACKBONES) * len(METHODS) * len(SEEDS)
    position = 0

    print(f"Clean k={BASELINE_K} Cora noise-anchor rerun: {total} cells")
    for backbone in BACKBONES:
        for method in METHODS:
            successes = 0
            for seed in SEEDS:
                position += 1
                ok = run_single_baseline(method, DATASET, backbone, seed, BASELINE_K)
                print(f"[{position}/{total}] {method}/{backbone}/seed{seed}: {'OK' if ok else 'FAIL'}")
                if ok:
                    successes += 1
                else:
                    failures.append(f"{method}/{backbone}/seed{seed}")

            averaged = compute_averaged_baseline(method, DATASET, backbone, BASELINE_K)
            has_anchor = averaged is not None and averaged.get("method_perf_before") is not None
            summary.append({
                "method": method,
                "backbone": backbone,
                "seeds_ok": successes,
                "method_perf_before": averaged.get("method_perf_before") if averaged else None,
                "method_noise_drop": averaged.get("method_noise_drop") if averaged else None,
                "anchor_present": has_anchor,
            })
            if successes != len(SEEDS) or not has_anchor:
                failures.append(f"{method}/{backbone}: incomplete aggregate or missing method_perf_before")

    BASELINE_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "kind": "clean_cora_k5_noise_anchor",
        "timestamp": datetime.now().isoformat(),
        "dataset": DATASET,
        "backbones": list(BACKBONES),
        "methods": list(METHODS),
        "seeds": list(SEEDS),
        "baseline_k": BASELINE_K,
        "before_metric": "method_train_only_f1",
        "result_root": str(BASELINE_ROOT.resolve()),
        **_git_provenance(),
        "summary": summary,
        "failures": failures,
    }
    path = BASELINE_ROOT / "clean_cora_noise_anchor_manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest: {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
