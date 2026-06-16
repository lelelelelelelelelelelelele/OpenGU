"""Phase B interim aggregator.

Walks results/runs/{machine}/{cell}/{method}_{strategy}/seed*/{attack,collateral,_meta}.json
and dumps a flat CSV with the canonical paper-input fields.

Usage:
    python scripts/aggregate_phase_b.py            # all machines under results/runs/
    python scripts/aggregate_phase_b.py 4090       # only cora (machine A)
    python scripts/aggregate_phase_b.py h20        # only arxiv (machine B)
    python scripts/aggregate_phase_b.py 4090 h20   # explicit both

Output: results/_phase_b_aggregate.csv

Field semantics (per self/dashboard/METRIC_FIELD_SEMANTICS.md):
  perf_before    -- pre-unlearning test F1 (gold "f1_before"; from collateral.json)
  f1_after       -- post-unlearning test F1 (from attack.json; the attack effect)
  f1_drop        -- perf_before - f1_after (derived; positive = attack worked)
  perf_unlearn   -- collateral.json view of post-unlearn F1 (sanity cross-check vs f1_after)
  perf_retrain   -- gold-standard retrain-from-scratch F1
  gap            -- perf_unlearn - perf_retrain (retrain gap; positive = unlearn over-shoots)
  mia_auc        -- membership inference AUC against the unlearned model
  hop_{k}_flip_rate -- prediction-flip rate at k-hop (k in {1,2,3,gt3})
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Optional

import pandas as pd

STRATEGIES = ("random", "degree", "pagerank", "tracin", "im", "hybrid")
DEFAULT_MACHINES = ("4090", "h20")


def split_method_strategy(dirname: str) -> tuple[str, str, str]:
    """Cell dir is `{Method}_{strategy}` or `{Method}_{strategy}_{suffix}` (e.g. hybrid_alpha0.25).

    Returns (method, strategy_canonical, strategy_full) where strategy_canonical is one of
    STRATEGIES and strategy_full carries any suffix.
    """
    for s in sorted(STRATEGIES, key=len, reverse=True):
        token = f"_{s}"
        idx = dirname.find(token)
        if idx <= 0:
            continue
        tail = dirname[idx + len(token):]
        if tail and not tail.startswith("_"):
            continue
        method = dirname[:idx]
        strategy_full = s + tail
        return method, s, strategy_full
    method, _, strategy_full = dirname.rpartition("_")
    return method, strategy_full, strategy_full


def load_collateral(p: pathlib.Path) -> dict:
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text())
    except Exception as e:
        return {"_collateral_err": str(e)}
    res = (d.get("results") or [{}])[0]
    out = {
        "perf_before": res.get("perf_before"),
        "perf_unlearn": res.get("perf_unlearn"),
        "perf_retrain": res.get("perf_retrain"),
        "drop_retrain": res.get("drop_retrain"),
        "gap": res.get("gap"),
        "gap_pct": res.get("gap_pct"),
        "mean_pred_shift": res.get("mean_pred_shift"),
        "max_pred_shift": res.get("max_pred_shift"),
        "fraction_flipped": res.get("fraction_flipped"),
    }
    hop = res.get("hop_decay") or {}
    for k_label, k_key in [("1", "1_hop"), ("2", "2_hop"), ("3", "3_hop"), ("gt3", "gt3_hop")]:
        out[f"hop_{k_label}_flip_rate"] = hop.get(f"{k_key}_flip_rate")
        out[f"hop_{k_label}_count"] = hop.get(f"{k_key}_count")
    return out


def load_meta(p: pathlib.Path) -> dict:
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text())
    except Exception:
        return {}
    return {
        "git_sha": (d.get("git_sha") or "")[:7],
        "hostname": d.get("hostname"),
        "timestamp": d.get("timestamp"),
    }


def aggregate(machines: list[str], root: pathlib.Path) -> pd.DataFrame:
    rows: list[dict] = []
    for machine in machines:
        base = root / machine
        if not base.exists():
            print(f"[skip] {base} not found")
            continue
        for ap in base.glob("*/*/seed*/attack.json"):
            cell = ap.parts[-4]                 # cora_GCN_r0.05
            method, strategy, strategy_full = split_method_strategy(ap.parts[-3])
            seed_dir = ap.parts[-2]
            if not seed_dir.startswith("seed"):
                continue
            try:
                seed = int(seed_dir[4:])
            except ValueError:
                continue
            try:
                d = json.loads(ap.read_text())
            except Exception as e:
                rows.append({
                    "machine": machine, "cell": cell, "method": method,
                    "strategy": strategy, "strategy_full": strategy_full, "seed": seed,
                    "_attack_err": str(e),
                })
                continue

            collateral = load_collateral(ap.parent / "collateral.json")
            meta = load_meta(ap.parent / "_meta.json")
            results = d.get("results") or {}

            for s_key, r in results.items():
                f1_after = r.get("f1_after")
                perf_before = collateral.get("perf_before")
                f1_drop: Optional[float] = None
                if perf_before is not None and f1_after is not None:
                    f1_drop = perf_before - f1_after
                row = {
                    "machine": machine,
                    "cell": cell,
                    "method": method,
                    "strategy": s_key if s_key in STRATEGIES else strategy,
                    "strategy_full": strategy_full,
                    "seed": seed,
                    "f1_after": f1_after,
                    "f1_drop": f1_drop,
                    "mia_auc": r.get("mia_auc"),
                    "unlearn_time": r.get("unlearn_time"),
                    "selection_time": r.get("selection_time"),
                    "selection_cache_hit": r.get("selection_cache_hit"),
                    "selected_n": len(r.get("selected_nodes") or []),
                    **collateral,
                    **meta,
                }
                rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    args = sys.argv[1:]
    machines = list(args) if args else list(DEFAULT_MACHINES)
    root = pathlib.Path("results/runs")
    df = aggregate(machines, root)
    out = pathlib.Path("results/_phase_b_aggregate.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"\nwrote {out}  rows={len(df)}  machines={sorted(df['machine'].unique().tolist()) if len(df) else []}")
    if len(df):
        print("\n[summary] mia_auc by (cell, method, strategy):")
        s = (df.groupby(["cell", "method", "strategy"])["mia_auc"]
               .agg(["count", "mean", "std"]).round(3))
        print(s.to_string())
        print("\n[summary] f1_drop by (cell, method, strategy):")
        s = (df.groupby(["cell", "method", "strategy"])["f1_drop"]
               .agg(["count", "mean", "std"]).round(3))
        print(s.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
