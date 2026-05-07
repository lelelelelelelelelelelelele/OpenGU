"""Phase B paper figures — cora-only (replaces stale plot_paper_figures.py).

Reads results/_phase_b_aggregate.csv (produced by scripts/aggregate_phase_b.py)
and writes the cora-portion of the paper figure inventory:

  results/paper_figures/
    fig1_f1_drop.pdf / .png      -- F1 drop by method × strategy on cora_GCN, cora_GAT
    fig2_mia_auc.pdf / .png      -- MIA AUC by method × strategy (0.5 baseline)
    fig3_paired_delta.pdf / .png -- paired Δ(strategy - same-seed random) per method
    fig4_hop_decay.pdf / .png    -- 1/2/3/>3-hop flip rate per method (tracin vs random)
    fig5_retrain_gap.pdf / .png  -- collateral retrain gap per method × strategy

Run:
    H:/conda_package/envs/gnn/python.exe scripts/plot_phase_b_cora.py
"""
from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV = pathlib.Path("results/_phase_b_aggregate.csv")
OUT = pathlib.Path("results/paper_figures")
OUT.mkdir(parents=True, exist_ok=True)

METHOD_ORDER = ["GIF", "GNNDelete", "GraphEraser", "GraphRevoker", "IDEA", "MEGU"]
STRAT_ORDER = ["random", "degree", "pagerank", "tracin", "im", "hybrid"]
STRAT_COLOR = {
    "random":   "#7f7f7f",
    "degree":   "#1f77b4",
    "pagerank": "#9467bd",
    "tracin":   "#d62728",
    "im":       "#2ca02c",
    "hybrid":   "#ff7f0e",
}
CELL_TITLES = {"cora_GCN_r0.05": "Cora · GCN (r=0.05)",
               "cora_GAT_r0.05": "Cora · GAT (r=0.05)"}

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 110,
    "savefig.bbox": "tight",
})


def save(fig: plt.Figure, name: str) -> None:
    for ext in ("pdf", "png"):
        p = OUT / f"{name}.{ext}"
        fig.savefig(p)
    plt.close(fig)
    print(f"  -> {OUT / (name + '.{pdf,png}')}")


def grouped_bars(df: pd.DataFrame, value: str, ylabel: str,
                 fname: str, hline: float | None = None,
                 ylim: tuple[float, float] | None = None) -> None:
    """Grouped bar chart: x=method, hue=strategy, panel=cell.  Mean ± std (n=5)."""
    cells = sorted(df["cell"].unique())
    fig, axes = plt.subplots(1, len(cells), figsize=(7.5 * len(cells), 4.5), sharey=True)
    if len(cells) == 1:
        axes = [axes]
    n_strat = len(STRAT_ORDER)
    bar_w = 0.8 / n_strat
    x_idx = np.arange(len(METHOD_ORDER))
    for ax, cell in zip(axes, cells):
        sub = df[df["cell"] == cell]
        for j, strat in enumerate(STRAT_ORDER):
            means = []
            stds = []
            for m in METHOD_ORDER:
                cell_data = sub[(sub["method"] == m) & (sub["strategy"] == strat)][value]
                means.append(cell_data.mean() if len(cell_data) else np.nan)
                stds.append(cell_data.std(ddof=1) if len(cell_data) > 1 else 0.0)
            offset = (j - (n_strat - 1) / 2) * bar_w
            ax.bar(x_idx + offset, means, bar_w, yerr=stds, capsize=2,
                   color=STRAT_COLOR[strat], label=strat,
                   edgecolor="black", linewidth=0.4, alpha=0.92)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(METHOD_ORDER, rotation=18, ha="right")
        ax.set_title(CELL_TITLES.get(cell, cell))
        if hline is not None:
            ax.axhline(hline, color="black", linewidth=0.7, linestyle="--", alpha=0.6)
        if ylim:
            ax.set_ylim(*ylim)
        ax.grid(axis="y", linestyle=":", alpha=0.5)
    axes[0].set_ylabel(ylabel)
    axes[-1].legend(loc="upper right", ncol=2, framealpha=0.9, title="strategy")
    fig.tight_layout()
    save(fig, fname)


def paired_delta(df: pd.DataFrame) -> None:
    """Per (cell, method, seed), compute Δ = strategy − random for non-random strategies.

    Plotted as box-strip per method, panel per cell.
    """
    rows = []
    pivot = df.pivot_table(index=["cell", "method", "seed"], columns="strategy",
                           values="f1_drop", aggfunc="first")
    for (cell, method, seed), r in pivot.iterrows():
        rnd = r.get("random")
        if pd.isna(rnd):
            continue
        for s in ["degree", "pagerank", "tracin", "im", "hybrid"]:
            v = r.get(s)
            if pd.isna(v):
                continue
            rows.append({"cell": cell, "method": method, "seed": seed,
                         "strategy": s, "delta": v - rnd})
    pd_df = pd.DataFrame(rows)

    cells = sorted(pd_df["cell"].unique())
    fig, axes = plt.subplots(1, len(cells), figsize=(7.5 * len(cells), 4.5), sharey=True)
    if len(cells) == 1:
        axes = [axes]
    strats_no_rnd = ["degree", "pagerank", "tracin", "im", "hybrid"]
    n_strat = len(strats_no_rnd)
    point_w = 0.8 / n_strat
    rng = np.random.default_rng(0)

    for ax, cell in zip(axes, cells):
        sub = pd_df[pd_df["cell"] == cell]
        for j, strat in enumerate(strats_no_rnd):
            for i, m in enumerate(METHOD_ORDER):
                ds = sub[(sub["method"] == m) & (sub["strategy"] == strat)]["delta"].values
                if len(ds) == 0:
                    continue
                cx = i + (j - (n_strat - 1) / 2) * point_w
                jitter = rng.uniform(-point_w * 0.2, point_w * 0.2, size=len(ds))
                ax.scatter([cx + dx for dx in jitter], ds,
                           s=28, color=STRAT_COLOR[strat], alpha=0.85,
                           edgecolor="black", linewidth=0.3,
                           label=strat if i == 0 else None)
                ax.hlines(ds.mean(), cx - point_w * 0.4, cx + point_w * 0.4,
                          color="black", linewidth=1.5)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.7)
        ax.set_xticks(range(len(METHOD_ORDER)))
        ax.set_xticklabels(METHOD_ORDER, rotation=18, ha="right")
        ax.set_title(CELL_TITLES.get(cell, cell))
        ax.grid(axis="y", linestyle=":", alpha=0.5)
    axes[0].set_ylabel("Δ F1-drop  (strategy − same-seed random)")
    axes[-1].legend(loc="upper right", ncol=2, framealpha=0.9, title="strategy")
    fig.suptitle("Paired effect at fixed budget (>0 = strategy beats random)", y=1.02)
    fig.tight_layout()
    save(fig, "fig3_paired_delta")


def hop_decay(df: pd.DataFrame) -> None:
    """Hop-flip-rate decay curves for tracin vs random per method.

    For each (cell, method, strategy) average over seeds.
    """
    hops = ["hop_1_flip_rate", "hop_2_flip_rate", "hop_3_flip_rate", "hop_gt3_flip_rate"]
    hop_labels = ["1-hop", "2-hop", "3-hop", ">3-hop"]
    target_strats = ["random", "tracin", "hybrid"]

    cells = sorted(df["cell"].unique())
    fig, axes = plt.subplots(2, len(cells), figsize=(7.5 * len(cells), 8),
                              sharex=True, sharey=False)
    if axes.ndim == 1:
        axes = axes.reshape(2, -1)

    for col, cell in enumerate(cells):
        sub = df[df["cell"] == cell]
        for row_i, strat_set in enumerate([("random", "tracin"), ("random", "hybrid")]):
            ax = axes[row_i, col]
            for strat in strat_set:
                for m_i, m in enumerate(METHOD_ORDER):
                    vals = []
                    for h in hops:
                        v = sub[(sub["method"] == m) & (sub["strategy"] == strat)][h]
                        vals.append(v.mean())
                    style = "--" if strat == "random" else "-"
                    ax.plot(range(len(hops)), vals, style,
                            color=plt.cm.tab10(m_i % 10), linewidth=1.6,
                            marker="o", markersize=5, alpha=0.9,
                            label=f"{m} ({strat})" if col == 0 else None)
            ax.set_xticks(range(len(hops)))
            ax.set_xticklabels(hop_labels)
            title = f"{CELL_TITLES.get(cell, cell)} — {strat_set[1]} vs random"
            ax.set_title(title, fontsize=10)
            ax.grid(linestyle=":", alpha=0.5)
            if col == 0:
                ax.set_ylabel("flip rate")
    axes[0, 0].legend(fontsize=7, ncol=2, loc="upper right")
    fig.tight_layout()
    save(fig, "fig4_hop_decay")


def main() -> int:
    if not CSV.exists():
        print(f"missing {CSV}; run scripts/aggregate_phase_b.py first")
        return 2
    df = pd.read_csv(CSV)
    print(f"[load] {CSV} rows={len(df)} cells={sorted(df['cell'].unique())}")

    print("[fig1] f1_drop by method × strategy")
    grouped_bars(df, "f1_drop", "F1 drop  (perf_before − f1_after)",
                 "fig1_f1_drop", hline=0.0)

    print("[fig2] mia_auc by method × strategy")
    grouped_bars(df, "mia_auc", "MIA AUC", "fig2_mia_auc", hline=0.5,
                 ylim=(0.0, 1.0))

    print("[fig3] paired Δ vs same-seed random")
    paired_delta(df)

    print("[fig4] hop-decay flip rate")
    hop_decay(df)

    print("[fig5] retrain gap by method × strategy")
    grouped_bars(df, "gap", "Retrain gap  (perf_unlearn − perf_retrain)",
                 "fig5_retrain_gap", hline=0.0)

    print(f"\nall figures -> {OUT.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
