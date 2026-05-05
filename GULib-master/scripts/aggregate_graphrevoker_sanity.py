"""Aggregate GraphRevoker sanity-test metrics (r=0.05 + r=0.10) into a single table."""
import json
import glob
import os
import sys

ROOT = "H:/project/OpenGU/GULib-master/results/runs"
RATIOS = ["0.05", "0.1"]

def collect(ratio):
    rows = []
    pattern = f"{ROOT}/cora_GCN_r{ratio}/GraphRevoker_*/seed42"
    for d in sorted(glob.glob(pattern)):
        d = d.replace("\\", "/")
        strat = os.path.basename(os.path.dirname(d)).split("GraphRevoker_", 1)[1]
        try:
            a = json.load(open(d + "/attack.json"))
            c = json.load(open(d + "/collateral.json"))
            ar = a["results"][strat]
            cr = c["results"][0]
            rows.append({
                "ratio": ratio,
                "strategy": strat,
                "f1_after": ar.get("f1_after"),
                "mia_auc": ar.get("mia_auc"),
                "f1_before": cr.get("perf_before"),
                "f1_retrain": cr.get("perf_retrain"),
                "f1_unlearn": cr.get("perf_unlearn"),
                "gap": cr.get("gap"),
                "gap_pct": cr.get("gap_pct"),
                "mean_shift": cr.get("mean_pred_shift"),
                "flipped": cr.get("fraction_flipped"),
                "time_s": ar.get("total_time"),
                "cache_hit": ar.get("selection_cache_hit"),
            })
        except FileNotFoundError as e:
            rows.append({"ratio": ratio, "strategy": strat, "error": "missing: " + str(e)})
        except Exception as e:
            rows.append({"ratio": ratio, "strategy": strat, "error": str(e)})
    return rows

def fmt(x, w, prec=4, sign=False):
    if x is None:
        return "—".ljust(w)
    if isinstance(x, bool):
        return str(x).ljust(w)
    if isinstance(x, (int, float)):
        f = f"{{:{'+' if sign else ''}.{prec}f}}"
        return f.format(x).ljust(w)
    return str(x).ljust(w)

hdr = f'{"r":<5} {"strat":<9} {"F1_b":<7} {"F1_un":<7} {"F1_re":<7} {"Gap":<8} {"Gap%":<7} {"MIA":<6} {"MShift":<7} {"Flip%":<7} {"t(s)":<6} cache'
print(hdr)
print("-" * len(hdr))
for ratio in RATIOS:
    rows = collect(ratio)
    if not rows:
        print(f"r={ratio}: (no results yet)")
        continue
    for r in rows:
        if "error" in r:
            print(f'{r["ratio"]:<5} {r["strategy"]:<9} ERROR: {r["error"]}')
            continue
        print(
            f'{r["ratio"]:<5} {r["strategy"]:<9} '
            f'{fmt(r["f1_before"], 7)}'
            f'{fmt(r["f1_unlearn"], 7)}'
            f'{fmt(r["f1_retrain"], 7)}'
            f'{fmt(r["gap"], 8, sign=True)}'
            f'{fmt(r["gap_pct"], 7, prec=2, sign=True)}'
            f'{fmt(r["mia_auc"], 6, prec=3)}'
            f'{fmt(r["mean_shift"], 7)}'
            f'{fmt(r["flipped"]*100 if r["flipped"] is not None else None, 7, prec=2)}'
            f'{fmt(r["time_s"], 6, prec=1)}'
            f'{"hit" if r["cache_hit"] else "miss"}'
        )
    print()
