"""
gate_runs.py — automated pass/fail gate for a Phase B yaml.

Replaces the eyeball metric check at runbook §B.0 / §B.1. Reads a yaml
config, expands the (method, strategy, seed) matrix, and verifies every
expected leaf directory exists with sane metrics.

Usage:
    # B.0 sanity (1 cell, lenient)
    python scripts/gate_runs.py experiments/configs/sanity_one_cell.yaml

    # B.1 arxiv feasibility (5 cells, strict f1 range from §5.3.2.1)
    python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml \\
        --f1-min 0.55 --f1-max 0.85

Exit codes:
    0  all cells pass every check
    1  one or more cells failed (table printed for triage)
    2  yaml or directory layout broken (cannot proceed)

Checks per cell:
    - 4 files present: attack.json, collateral.json, predictions.npz, _meta.json
    - attack.json: results[strategy].mia_auc present and finite
    - mia_auc not collapsed: 0.001 < mia_auc < 0.999
    - collateral.json: results[0].{perf_before, gap, hop_decay} present
    - perf_before in [--f1-min, --f1-max] (default [0.0, 1.0])

Note: we read the gate's F1 sanity value from collateral.json (`perf_before`),
not from attack.json (`f1_before`). The attack.json field is sourced from
self.method.poison_f1 and node-task cells often leave it None. `perf_before`
is the current method's train_only before model; for shard/SISA methods this
is not guaranteed to be a method-agnostic vanilla base-model F1. See
self/dashboard/METRIC_FIELD_SEMANTICS.md before using before-fields in paper
tables.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import yaml
except ImportError:
    print("[FATAL] pyyaml not installed: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


EXPECTED_FILES = ["attack.json", "collateral.json", "predictions.npz", "_meta.json"]


def cell_path(repo_root: Path, cfg: dict, method: str, strategy: str, seed: int) -> Path:
    cell = f"{cfg['dataset']}_{cfg['base_model']}_r{cfg['ratio']}"
    return repo_root / "results" / "runs" / cell / f"{method}_{strategy}" / f"seed{seed}"


def is_finite_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def check_cell(leaf: Path, strategy: str, f1_min: float, f1_max: float) -> List[str]:
    """Return list of failure reasons; empty list = pass."""
    reasons = []

    if not leaf.is_dir():
        return [f"leaf-missing: {leaf}"]

    for fname in EXPECTED_FILES:
        if not (leaf / fname).is_file():
            reasons.append(f"file-missing: {fname}")

    attack_fp = leaf / "attack.json"
    if attack_fp.is_file():
        try:
            attack = json.loads(attack_fp.read_text(encoding="utf-8"))
        except Exception as e:
            reasons.append(f"attack.json unreadable: {e}")
        else:
            res = attack.get("results", {}).get(strategy)
            if not isinstance(res, dict):
                reasons.append(f"attack.json missing results[{strategy!r}]")
            else:
                mia = res.get("mia_auc")
                if not is_finite_number(mia):
                    reasons.append(f"mia_auc not finite: {mia!r}")
                elif not (0.001 < mia < 0.999):
                    reasons.append(f"mia_auc collapsed: {mia:.4f} (expected (0.001, 0.999))")

    collat_fp = leaf / "collateral.json"
    if collat_fp.is_file():
        try:
            collat = json.loads(collat_fp.read_text(encoding="utf-8"))
        except Exception as e:
            reasons.append(f"collateral.json unreadable: {e}")
        else:
            results = collat.get("results", [])
            if not (isinstance(results, list) and results):
                reasons.append("collateral.json results[] empty")
            else:
                row = results[0]
                pb = row.get("perf_before")
                if not is_finite_number(pb):
                    reasons.append(f"perf_before not finite: {pb!r}")
                elif not (f1_min <= pb <= f1_max):
                    reasons.append(f"perf_before={pb:.4f} outside [{f1_min}, {f1_max}]")
                if not is_finite_number(row.get("gap")):
                    reasons.append(f"collateral.gap not finite: {row.get('gap')!r}")
                if not isinstance(row.get("hop_decay"), dict):
                    reasons.append("collateral.hop_decay missing or wrong type")

    return reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("yaml_path", type=str)
    ap.add_argument("--f1-min", type=float, default=0.0)
    ap.add_argument("--f1-max", type=float, default=1.0)
    args = ap.parse_args()

    yaml_path = Path(args.yaml_path).resolve()
    if not yaml_path.is_file():
        print(f"[FATAL] yaml not found: {yaml_path}", file=sys.stderr)
        sys.exit(2)

    with yaml_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    for key in ("dataset", "base_model", "ratio", "methods", "strategies", "seeds"):
        if key not in cfg:
            print(f"[FATAL] yaml missing required key: {key}", file=sys.stderr)
            sys.exit(2)

    repo_root = Path(__file__).resolve().parent.parent

    cells: List[Tuple[str, str, int, Path]] = []
    for method in cfg["methods"]:
        for strategy in cfg["strategies"]:
            for seed in cfg["seeds"]:
                cells.append((method, strategy, int(seed),
                              cell_path(repo_root, cfg, method, strategy, int(seed))))

    print(f"[gate] yaml={yaml_path.name}  cells={len(cells)}  "
          f"f1 range=[{args.f1_min}, {args.f1_max}]  mia range=(0.001, 0.999)")
    print("-" * 72)

    failed = []
    for method, strategy, seed, leaf in cells:
        reasons = check_cell(leaf, strategy, args.f1_min, args.f1_max)
        tag = f"{method}/{strategy}/seed{seed}"
        if reasons:
            failed.append((tag, reasons))
            print(f"[FAIL] {tag}")
            for r in reasons:
                print(f"         - {r}")
        else:
            print(f"[ OK ] {tag}")

    print("-" * 72)
    if failed:
        print(f"[gate] {len(failed)}/{len(cells)} cells FAILED — do NOT proceed")
        sys.exit(1)
    print(f"[gate] {len(cells)}/{len(cells)} cells PASSED — safe to proceed")
    sys.exit(0)


if __name__ == "__main__":
    main()
