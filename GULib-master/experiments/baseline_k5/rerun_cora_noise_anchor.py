"""Clean k=5 random-baseline rerun for the paper's Cora noise anchor.

The run starts from the canonical ``results/baseline/k5_random`` directory;
the pre-v2 evidence is preserved in ``k5_random_OLD_20260227``.  By default
the canonical root must contain no JSON artifacts; pass
``--resume`` only to reuse schema-validated v2 cells after an interruption.
It covers the entire Cora x {GCN, GAT} six-method scorecard,
uses five independent baseline seeds, and writes ``method_perf_before`` for
every retained cell.

Usage (on the formal GPU checkout):
    python experiments/baseline_k5/rerun_cora_noise_anchor.py --preflight-only
    python experiments/baseline_k5/rerun_cora_noise_anchor.py \
        --expected-git-sha <40-character-accepted-main-sha>
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
    REPO_ROOT,
    SEEDS,
    compute_averaged_baseline,
    run_single_baseline,
)
from baseline_contract import BEFORE_METRIC, SCHEMA, SCHEMA_VERSION
from formal_preflight import build_formal_preflight, collect_git_provenance


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
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="report formal readiness without creating artifacts or starting GPU work",
    )
    parser.add_argument(
        "--expected-git-sha",
        help="full accepted main SHA; required for an actual formal run",
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
    if not args.preflight_only and not args.expected_git_sha:
        print("Refusing formal run without --expected-git-sha <40-character SHA>")
        return 2
    preflight = build_formal_preflight(
        REPO_ROOT,
        expected_git_sha=args.expected_git_sha,
        dataset=DATASET,
    )
    print(json.dumps(preflight, indent=2))
    if not preflight["ready"]:
        return 2
    if args.preflight_only:
        return 0

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
    final_git = collect_git_provenance(REPO_ROOT)
    if (
        final_git["git_sha"] != preflight["git"]["git_sha"]
        or final_git["branch"] != "main"
        or final_git["dirty"]
    ):
        failures.append("Git provenance changed or became dirty during the run")

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
        "before_metric": BEFORE_METRIC,
        "result_root": str(BASELINE_ROOT.resolve()),
        "formal_preflight": preflight,
        "final_git": final_git,
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
