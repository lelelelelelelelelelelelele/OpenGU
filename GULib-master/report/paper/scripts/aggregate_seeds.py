"""
aggregate_seeds.py — Scan all relative & collateral result files,
aggregate across seeds, and produce mean ± std tables.

Output:
  - report/paper/sections/cross_seed_tables.md
  - Console summary

Usage:
  python report/paper/scripts/aggregate_seeds.py
"""
import json
import os
import sys
from pathlib import Path
from collections import defaultdict
import math

BASE = Path(__file__).resolve().parents[3]  # GULib-master
RELATIVE_DIR = BASE / "results" / "relative"
COLLATERAL_DIR = BASE / "results" / "collateral"
OUTPUT_MD = BASE / "report" / "paper" / "sections" / "cross_seed_tables.md"

EXCLUDE_METHODS = {"GUIDE"}  # Source-library bug

# ──────────────────────────────────────────────────────────
# 1) Aggregate RELATIVE results
# ──────────────────────────────────────────────────────────
def scan_relative():
    """Returns dict[(method,dataset,model,strategy)] -> list of relative_f1_drop values (one per seed)."""
    data = defaultdict(list)
    seed_tracker = defaultdict(set)  # track unique seeds per cell

    if not RELATIVE_DIR.exists():
        print(f"[WARN] {RELATIVE_DIR} does not exist")
        return data

    for method_dir in sorted(RELATIVE_DIR.iterdir()):
        if not method_dir.is_dir():
            continue
        method = method_dir.name
        if method in EXCLUDE_METHODS:
            continue
        for dataset_dir in sorted(method_dir.iterdir()):
            if not dataset_dir.is_dir():
                continue
            dataset = dataset_dir.name
            for model_dir in sorted(dataset_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                model = model_dir.name
                for fpath in sorted(model_dir.glob("relative_seed*.json")):
                    try:
                        with open(fpath, encoding="utf-8") as f:
                            doc = json.load(f)
                        seed = doc.get("config", {}).get("random_seed", "?")
                        for r in doc.get("results", []):
                            strat = r.get("strategy", "")
                            val = r.get("relative_f1_drop")
                            if val is not None and strat:
                                key = (method, dataset, model, strat)
                                # Deduplicate: only take first file per seed per key
                                seed_key = (method, dataset, model, strat, seed)
                                if seed_key not in seed_tracker:
                                    seed_tracker[seed_key] = True
                                    data[key].append(float(val))
                    except (json.JSONDecodeError, OSError):
                        continue
    return data


# ──────────────────────────────────────────────────────────
# 2) Aggregate COLLATERAL results
# ──────────────────────────────────────────────────────────
def scan_collateral():
    """Returns dict[(method,dataset,model,strategy)] -> list of dicts with gap/shift/flipped per seed."""
    data = defaultdict(list)
    seed_tracker = defaultdict(set)

    if not COLLATERAL_DIR.exists():
        print(f"[WARN] {COLLATERAL_DIR} does not exist")
        return data

    for method_dir in sorted(COLLATERAL_DIR.iterdir()):
        if not method_dir.is_dir():
            continue
        method = method_dir.name
        if method in EXCLUDE_METHODS:
            continue
        for dataset_dir in sorted(method_dir.iterdir()):
            if not dataset_dir.is_dir():
                continue
            dataset = dataset_dir.name
            for model_dir in sorted(dataset_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                model = model_dir.name
                for fpath in sorted(model_dir.glob("collateral_*.json")):
                    try:
                        with open(fpath, encoding="utf-8") as f:
                            doc = json.load(f)
                        cfg = doc.get("config", {})
                        seed = cfg.get("random_seed")
                        ratio = cfg.get("unlearn_ratio")
                        for r in doc.get("results", []):
                            strat = r.get("strategy", "")
                            gap_pct = r.get("gap_pct")
                            mean_shift = r.get("mean_pred_shift")
                            flipped = r.get("fraction_flipped")
                            if strat and gap_pct is not None:
                                key = (method, dataset, model, strat, ratio)
                                seed_key = (method, dataset, model, strat, ratio, seed)
                                if seed_key not in seed_tracker:
                                    seed_tracker[seed_key] = True
                                    data[key].append({
                                        "gap_pct": float(gap_pct),
                                        "mean_pred_shift": float(mean_shift) if mean_shift is not None else None,
                                        "fraction_flipped": float(flipped) if flipped is not None else None,
                                    })
                    except (json.JSONDecodeError, OSError):
                        continue
    return data


# ──────────────────────────────────────────────────────────
# 3) Stats helpers
# ──────────────────────────────────────────────────────────
def mean_std(vals):
    n = len(vals)
    if n == 0:
        return None, None, 0
    m = sum(vals) / n
    if n == 1:
        return m, 0.0, n
    var = sum((x - m) ** 2 for x in vals) / (n - 1)
    return m, math.sqrt(var), n


def fmt(m, s, n, pct=False):
    if m is None:
        return "—"
    suffix = "%" if pct else ""
    if n >= 2:
        return f"{m:.4f} ± {s:.4f}{suffix} (n={n})"
    return f"{m:.4f}{suffix} (n={n})"


def fmt_short(m, s, n, pct=False):
    if m is None:
        return "—"
    suffix = "%" if pct else ""
    if n >= 2:
        return f"{m:.4f}±{s:.4f}{suffix}"
    return f"{m:.4f}{suffix}"


# ──────────────────────────────────────────────────────────
# 4) Build markdown tables
# ──────────────────────────────────────────────────────────
def build_relative_tables(rel_data):
    lines = []
    lines.append("# Cross-Seed Aggregated Results\n")
    lines.append("> Generated by `report/paper/scripts/aggregate_seeds.py`\n")
    lines.append("> **GUIDE excluded** (source-library bug)\n")
    lines.append("---\n")
    lines.append("## A. Relative F1 Drop (vs k=5 Random Baseline)\n")
    lines.append("Positive value = attack effective (F1 lower than random baseline)\n")

    # Group by (method, dataset, model)
    groups = defaultdict(dict)
    for (method, dataset, model, strat), vals in rel_data.items():
        groups[(method, dataset, model)][strat] = vals

    # Collect all strategies
    all_strats = sorted({k[3] for k in rel_data.keys()})

    for (method, dataset, model) in sorted(groups.keys()):
        lines.append(f"\n### {method} / {dataset} / {model}\n")
        # Header
        lines.append("| Strategy | Mean | Std | n (seeds) |")
        lines.append("|----------|------|-----|-----------|")
        strat_data = groups[(method, dataset, model)]
        for strat in all_strats:
            vals = strat_data.get(strat, [])
            m, s, n = mean_std(vals)
            if m is not None:
                lines.append(f"| {strat} | {m:.4f} | {s:.4f} | {n} |")
        lines.append("")

    # Summary table: all methods × strategies for primary config (cora/GCN)
    lines.append("\n### Summary: Cora/GCN (Primary Config)\n")
    lines.append("| Method | " + " | ".join(all_strats) + " |")
    lines.append("|--------" + "|------" * len(all_strats) + "|")

    methods_in_cora_gcn = sorted({k[0] for k in groups.keys() if k[1] == "cora" and k[2] == "GCN"})
    for method in methods_in_cora_gcn:
        strat_data = groups.get((method, "cora", "GCN"), {})
        cells = []
        for strat in all_strats:
            vals = strat_data.get(strat, [])
            m, s, n = mean_std(vals)
            cells.append(fmt_short(m, s, n))
        lines.append(f"| {method} | " + " | ".join(cells) + " |")
    lines.append("")

    return lines


def build_collateral_tables(col_data):
    lines = []
    lines.append("\n---\n")
    lines.append("## B. Collateral Damage (Retrain Gap + Prediction Shift)\n")

    # Group by (method, dataset, model, ratio)
    groups = defaultdict(dict)
    for (method, dataset, model, strat, ratio), vals in col_data.items():
        groups[(method, dataset, model, ratio)][strat] = vals

    all_strats = sorted({k[3] for k in col_data.keys()})

    for (method, dataset, model, ratio) in sorted(groups.keys()):
        lines.append(f"\n### {method} / {dataset} / {model} (ratio={ratio})\n")
        lines.append("| Strategy | Gap% (mean±std) | PredShift (mean±std) | Flipped% (mean±std) | n |")
        lines.append("|----------|-----------------|---------------------|--------------------|----|")
        strat_data = groups[(method, dataset, model, ratio)]
        for strat in all_strats:
            entries = strat_data.get(strat, [])
            if not entries:
                continue
            gaps = [e["gap_pct"] for e in entries]
            shifts = [e["mean_pred_shift"] for e in entries if e["mean_pred_shift"] is not None]
            flips = [e["fraction_flipped"] for e in entries if e["fraction_flipped"] is not None]
            gm, gs, gn = mean_std(gaps)
            sm, ss, sn = mean_std(shifts)
            fm, fs, fn = mean_std(flips)
            lines.append(
                f"| {strat} "
                f"| {fmt_short(gm, gs, gn, pct=True)} "
                f"| {fmt_short(sm, ss, sn)} "
                f"| {fmt_short(fm*100 if fm else None, fs*100 if fs else None, fn, pct=True)} "
                f"| {gn} |"
            )
        lines.append("")

    # Summary: collateral gap for primary config cora/GCN
    lines.append("\n### Summary: Collateral Gap% by Method (Cora/GCN, all ratios merged)\n")
    lines.append("| Method | Strategy | Ratio | Gap% (mean±std) | n |")
    lines.append("|--------|----------|-------|-----------------|---|")
    for (method, dataset, model, ratio) in sorted(groups.keys()):
        if dataset != "cora" or model != "GCN":
            continue
        strat_data = groups[(method, dataset, model, ratio)]
        for strat in sorted(strat_data.keys()):
            entries = strat_data[strat]
            gaps = [e["gap_pct"] for e in entries]
            gm, gs, gn = mean_std(gaps)
            lines.append(f"| {method} | {strat} | {ratio} | {fmt_short(gm, gs, gn, pct=True)} | {gn} |")
    lines.append("")

    return lines


def build_coverage_table(rel_data, col_data):
    lines = []
    lines.append("\n---\n")
    lines.append("## C. Coverage Matrix\n")

    # Relative coverage
    lines.append("### Relative Results Coverage\n")
    lines.append("| Method | Dataset | Model | Strategies | Seeds (min–max per strategy) |")
    lines.append("|--------|---------|-------|------------|----------------------------|")
    rel_groups = defaultdict(lambda: defaultdict(list))
    for (method, dataset, model, strat), vals in rel_data.items():
        rel_groups[(method, dataset, model)][strat] = len(vals)
    for (method, dataset, model) in sorted(rel_groups.keys()):
        strats = rel_groups[(method, dataset, model)]
        s_names = ", ".join(sorted(strats.keys()))
        counts = list(strats.values())
        lines.append(f"| {method} | {dataset} | {model} | {s_names} | {min(counts)}–{max(counts)} |")
    lines.append("")

    # Collateral coverage
    lines.append("### Collateral Results Coverage\n")
    lines.append("| Method | Dataset | Model | Ratio | Strategies | Seeds (min–max) |")
    lines.append("|--------|---------|-------|-------|------------|-----------------|")
    col_groups = defaultdict(lambda: defaultdict(list))
    for (method, dataset, model, strat, ratio), vals in col_data.items():
        col_groups[(method, dataset, model, ratio)][strat] = len(vals)
    for (method, dataset, model, ratio) in sorted(col_groups.keys()):
        strats = col_groups[(method, dataset, model, ratio)]
        s_names = ", ".join(sorted(strats.keys()))
        counts = list(strats.values())
        lines.append(f"| {method} | {dataset} | {model} | {ratio} | {s_names} | {min(counts)}–{max(counts)} |")
    lines.append("")

    # Gap analysis: where we have <5 seeds
    lines.append("### ⚠️ Cells with <5 seeds (need more runs)\n")
    lines.append("| Source | Method | Dataset | Model | Strategy | n |")
    lines.append("|--------|--------|---------|-------|----------|---|")
    for (method, dataset, model, strat), vals in sorted(rel_data.items()):
        if len(vals) < 5:
            lines.append(f"| relative | {method} | {dataset} | {model} | {strat} | {len(vals)} |")
    for (method, dataset, model, strat, ratio), vals in sorted(col_data.items()):
        if len(vals) < 5:
            lines.append(f"| collateral (r={ratio}) | {method} | {dataset} | {model} | {strat} | {len(vals)} |")
    lines.append("")

    return lines


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("Cross-Seed Aggregation")
    print("=" * 70)

    # Scan
    print("\n[1/3] Scanning relative results...")
    rel_data = scan_relative()
    print(f"  Found {len(rel_data)} unique (method,dataset,model,strategy) cells")
    total_rel = sum(len(v) for v in rel_data.values())
    print(f"  Total data points: {total_rel}")

    print("\n[2/3] Scanning collateral results...")
    col_data = scan_collateral()
    print(f"  Found {len(col_data)} unique (method,dataset,model,strategy,ratio) cells")
    total_col = sum(len(v) for v in col_data.values())
    print(f"  Total data points: {total_col}")

    # Build tables
    print("\n[3/3] Building tables...")
    all_lines = []
    all_lines.extend(build_relative_tables(rel_data))
    all_lines.extend(build_collateral_tables(col_data))
    all_lines.extend(build_coverage_table(rel_data, col_data))

    # Write
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))
    print(f"\n[OK] Output written to: {OUTPUT_MD}")
    print(f"   Relative cells: {len(rel_data)}, Collateral cells: {len(col_data)}")

    # Print compact summary to console
    print("\n" + "=" * 70)
    print("COMPACT SUMMARY: Relative F1 Drop (Cora/GCN)")
    print("=" * 70)
    all_strats = sorted({k[3] for k in rel_data.keys()})
    header = f"{'Method':<14}" + "".join(f"{s:<20}" for s in all_strats)
    print(header)
    print("-" * len(header))
    methods_in_cora = sorted({k[0] for k in rel_data.keys() if k[1] == "cora" and k[2] == "GCN"})
    for method in methods_in_cora:
        row = f"{method:<14}"
        for strat in all_strats:
            vals = rel_data.get((method, "cora", "GCN", strat), [])
            m, s, n = mean_std(vals)
            if m is not None:
                row += f"{m:+.4f}±{s:.4f} ({n}) "
            else:
                row += f"{'—':<20}"
        print(row)

    print("\n" + "=" * 70)
    print("COMPACT SUMMARY: Collateral Gap% (Cora/GCN)")
    print("=" * 70)
    col_strats = sorted({k[3] for k in col_data.keys() if k[1] == "cora" and k[2] == "GCN"})
    for method in sorted({k[0] for k in col_data.keys() if k[1] == "cora" and k[2] == "GCN"}):
        ratios = sorted({k[4] for k in col_data.keys() if k[0] == method and k[1] == "cora" and k[2] == "GCN"})
        for ratio in ratios:
            print(f"\n  {method} (ratio={ratio}):")
            for strat in col_strats:
                entries = col_data.get((method, "cora", "GCN", strat, ratio), [])
                if entries:
                    gaps = [e["gap_pct"] for e in entries]
                    gm, gs, gn = mean_std(gaps)
                    print(f"    {strat:<12} gap={gm:+.2f}±{gs:.2f}% (n={gn})")


if __name__ == "__main__":
    main()
