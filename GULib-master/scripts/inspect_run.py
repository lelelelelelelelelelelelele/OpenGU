"""
inspect_run.py — quick health-check for one Phase B run leaf directory.

Usage (from repo root):
    python scripts/inspect_run.py results/runs/cora_GCN_r0.05/GIF_random/seed42

Prints:
  1. file presence (4 expected: attack.json, collateral.json, predictions.npz, _meta.json)
  2. attack.json key metrics (f1, mia_auc, etc) with full path
  3. collateral.json key metrics (gap, pred_shift, hop_decay)
  4. selection_cache hits in last 10 minutes (assumes user just ran B.0/B.1)

Designed for quick "is the cell sane?" reporting after a run completes,
without requiring multiline shell paste.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path


EXPECTED_FILES = ["attack.json", "collateral.json", "predictions.npz", "_meta.json"]
KEY_METRICS = [
    "f1_clean", "f1_unlearn", "f1_retrain",
    "f1_drop", "effect", "paired_effect",
    "mia_auc",
    "gap", "gap_pct", "retrain_gap",
    "pred_shift", "fraction_flipped",
    "hop_decay_h1", "hop_decay_h2", "hop_decay_h3", "hop_decay_h4",
]


def walk_keys(obj, path=""):
    """Yield (path, value) for every leaf in a nested dict."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_keys(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        # Leaves only; arrays are reported as shape
        yield path, f"list[{len(obj)}]"
    else:
        yield path, obj


def find_metrics(d):
    """Return dict of {full_path: value} for any path whose leaf key matches KEY_METRICS."""
    found = {}
    for path, val in walk_keys(d):
        leaf = path.split(".")[-1]
        if leaf in KEY_METRICS:
            found[path] = val
    return found


def print_section(title):
    print(f"\n=== {title} ===")


def inspect(run_dir: Path):
    if not run_dir.is_dir():
        print(f"[ERROR] {run_dir} is not a directory")
        sys.exit(1)

    # 1. file presence
    print_section(f"files in {run_dir}")
    for fname in EXPECTED_FILES:
        fp = run_dir / fname
        if fp.is_file():
            size_kb = fp.stat().st_size / 1024
            print(f"  ✓ {fname:<20} ({size_kb:>8.1f} KB)")
        else:
            print(f"  ✗ {fname:<20} MISSING")

    # 2. attack.json metrics
    attack_fp = run_dir / "attack.json"
    if attack_fp.is_file():
        print_section("attack.json key metrics")
        with attack_fp.open() as f:
            d = json.load(f)
        metrics = find_metrics(d)
        if not metrics:
            print("  (no recognized metric keys; dumping top-level keys instead)")
            for k in d.keys():
                print(f"  • {k}")
        else:
            for path in sorted(metrics):
                v = metrics[path]
                if isinstance(v, float):
                    print(f"  {path:<40} = {v:.4f}")
                else:
                    print(f"  {path:<40} = {v}")

    # 3. collateral.json metrics
    coll_fp = run_dir / "collateral.json"
    if coll_fp.is_file():
        print_section("collateral.json key metrics")
        with coll_fp.open() as f:
            d = json.load(f)
        metrics = find_metrics(d)
        if not metrics:
            print("  (no recognized metric keys; dumping top-level keys instead)")
            for k in d.keys():
                print(f"  • {k}")
        else:
            for path in sorted(metrics):
                v = metrics[path]
                if isinstance(v, float):
                    print(f"  {path:<40} = {v:.4f}")
                else:
                    print(f"  {path:<40} = {v}")

    # 4. selection_cache fresh entries (modified within last 10 min)
    repo_root = Path(__file__).resolve().parents[1]
    sel_dir = repo_root / "results" / "selection_cache"
    if sel_dir.is_dir():
        now = time.time()
        recent = [
            (p, p.stat().st_mtime)
            for p in sel_dir.glob("*.json")
            if (now - p.stat().st_mtime) < 600
        ]
        recent.sort(key=lambda t: -t[1])
        print_section(f"selection_cache (last 10 min, {len(recent)} entries)")
        for p, mtime in recent[:5]:
            print(f"  • {p.name}  ({(now - mtime):>4.0f}s ago, {p.stat().st_size} bytes)")

    # 5. quick sanity verdict
    print_section("verdict")
    issues = []
    if attack_fp.is_file():
        with attack_fp.open() as f:
            d = json.load(f)
        for path, v in walk_keys(d):
            if path.endswith("mia_auc") and isinstance(v, (int, float)) and v == 0.0:
                issues.append(f"  ⚠ {path} = 0.0 (Phase A bug or stale cache)")
    if all((run_dir / fn).is_file() for fn in EXPECTED_FILES) and not issues:
        print("  ✓ all 4 files present, no zero-MIA flags. Looks healthy.")
    else:
        if not all((run_dir / fn).is_file() for fn in EXPECTED_FILES):
            print("  ✗ missing one or more expected files")
        for issue in issues:
            print(issue)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    inspect(Path(sys.argv[1]))
