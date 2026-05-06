"""Build paper Table 1 — cora rows.

Reads results/_phase_b_aggregate.csv and emits:
  results/_paper_table1_cora.md   -- Markdown view (for review / dashboard)
  results/_paper_table1_cora.tex  -- LaTeX booktabs view (for Overleaf paste)

Layout: per cell, rows = method, columns = strategy × {F1-drop, MIA-AUC, Gap}.
Reports mean ± std across 5 seeds.
"""
from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

CSV = pathlib.Path("results/_phase_b_aggregate.csv")
OUT_MD = pathlib.Path("results/_paper_table1_cora.md")
OUT_TEX = pathlib.Path("results/_paper_table1_cora.tex")

METHOD_ORDER = ["GIF", "GNNDelete", "GraphEraser", "GraphRevoker", "IDEA", "MEGU"]
STRAT_ORDER = ["random", "degree", "pagerank", "tracin", "im", "hybrid"]

CELL_LABEL = {"cora_GCN_r0.05": "Cora · GCN (r=0.05)",
              "cora_GAT_r0.05": "Cora · GAT (r=0.05)"}


def fmt(mean: float, std: float, sig: int = 3) -> str:
    if pd.isna(mean):
        return "—"
    return f"{mean:.{sig}f} ± {std:.{sig}f}"


def fmt_tex(mean: float, std: float, sig: int = 3) -> str:
    if pd.isna(mean):
        return "---"
    return f"${mean:.{sig}f}_{{\\pm {std:.{sig}f}}}$"


def build_metric_table(df: pd.DataFrame, metric: str, sig: int = 3) -> pd.DataFrame:
    """Long → wide: rows=(cell,method), cols=strategy, values='mean ± std'."""
    g = (df.groupby(["cell", "method", "strategy"])[metric]
           .agg(["mean", "std"]).reset_index())
    g["std"] = g["std"].fillna(0.0)
    g["display"] = g.apply(lambda r: fmt(r["mean"], r["std"], sig), axis=1)
    g["display_tex"] = g.apply(lambda r: fmt_tex(r["mean"], r["std"], sig), axis=1)
    wide = g.pivot_table(index=["cell", "method"], columns="strategy",
                         values="display", aggfunc="first")
    wide_tex = g.pivot_table(index=["cell", "method"], columns="strategy",
                             values="display_tex", aggfunc="first")
    return wide[STRAT_ORDER], wide_tex[STRAT_ORDER]


def emit_markdown(df: pd.DataFrame) -> str:
    out = ["# Phase B · Table 1 — Cora\n"]
    out.append(f"_Source: `{CSV}` (n=5 seeds per cell, 6 methods × 6 strategies × 2 backbones)_\n")

    for metric, label, sig in [
        ("f1_drop", "F1 drop  (perf_before − f1_after; ↑ = attack worked)", 3),
        ("mia_auc", "MIA AUC  (0.5 = random guess; |AUC−0.5| measures leakage)", 3),
        ("gap", "Retrain gap  (perf_unlearn − perf_retrain; ↑ = unlearn fails to mimic retrain)", 3),
    ]:
        out.append(f"\n## {label}\n")
        wide, _ = build_metric_table(df, metric, sig)
        for cell in sorted(wide.index.get_level_values(0).unique()):
            sub = wide.loc[cell].reindex(METHOD_ORDER)
            out.append(f"\n**{CELL_LABEL.get(cell, cell)}**\n")
            out.append("| Method | " + " | ".join(STRAT_ORDER) + " |")
            out.append("|" + "---|" * (len(STRAT_ORDER) + 1))
            for m in METHOD_ORDER:
                row_vals = sub.loc[m].tolist()
                out.append(f"| **{m}** | " + " | ".join(row_vals) + " |")
    return "\n".join(out) + "\n"


def emit_latex(df: pd.DataFrame) -> str:
    """Per-cell LaTeX longtable fragments (paste into Overleaf, wrap with \\begin{table}...)."""
    parts = ["% Phase B · Table 1 — Cora",
             f"% Source: {CSV}, n=5 seeds, 2026-05-07 aggregate",
             ""]
    for metric, caption, sig in [
        ("f1_drop", "F1 drop on Cora (perf\\_before $-$ f1\\_after; n=5 seeds, mean$\\pm$std)", 3),
        ("mia_auc", "MIA AUC on Cora", 3),
        ("gap", "Retrain gap on Cora (perf\\_unlearn $-$ perf\\_retrain)", 3),
    ]:
        _, tex = build_metric_table(df, metric, sig)
        parts.append(f"% ----- {metric} -----")
        parts.append("\\begin{table*}[t]")
        parts.append("\\centering\\small")
        parts.append("\\setlength{\\tabcolsep}{4pt}")
        parts.append(f"\\caption{{{caption}}}")
        parts.append(f"\\label{{tab:phaseB-{metric}-cora}}")
        col_spec = "l" + "c" * (1 + len(STRAT_ORDER))   # backbone + method + strategies
        parts.append(f"\\begin{{tabular}}{{{col_spec}}}")
        parts.append("\\toprule")
        parts.append("Backbone & Method & " + " & ".join(STRAT_ORDER) + " \\\\")
        parts.append("\\midrule")
        for cell in sorted(tex.index.get_level_values(0).unique()):
            sub = tex.loc[cell].reindex(METHOD_ORDER)
            backbone = CELL_LABEL.get(cell, cell).split("·")[-1].strip()
            for i, m in enumerate(METHOD_ORDER):
                row_vals = sub.loc[m].tolist()
                bb_cell = f"\\multirow{{6}}{{*}}{{{backbone}}}" if i == 0 else ""
                parts.append(f"{bb_cell} & {m} & " + " & ".join(row_vals) + " \\\\")
            parts.append("\\midrule")
        # remove the trailing \midrule, replace with \bottomrule
        parts[-1] = "\\bottomrule"
        parts.append("\\end{tabular}")
        parts.append("\\end{table*}")
        parts.append("")
    return "\n".join(parts) + "\n"


def main() -> int:
    if not CSV.exists():
        print(f"missing {CSV}; run scripts/aggregate_phase_b.py first")
        return 2
    df = pd.read_csv(CSV)
    df = df[df["cell"].str.startswith("cora_")].copy()

    md = emit_markdown(df)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"wrote {OUT_MD}")

    tex = emit_latex(df)
    OUT_TEX.write_text(tex, encoding="utf-8")
    print(f"wrote {OUT_TEX}")

    summary = (df.groupby(["cell", "method"])
                 .agg(f1_drop_max=("f1_drop", "max"),
                      f1_drop_mean=("f1_drop", "mean"),
                      mia_max=("mia_auc", "max"),
                      gap_mean=("gap", "mean")).round(3))
    print("\n[per-method headline] (max f1_drop, mean f1_drop, max MIA AUC, mean retrain gap)")
    print(summary.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
