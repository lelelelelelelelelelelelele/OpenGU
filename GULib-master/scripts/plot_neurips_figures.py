"""Generate the 6 NeurIPS paper figures from Phase B aggregate data.

This is the canonical figure generator for the current paper revision.
It reads ONLY two inputs and writes 6 PDFs to the Overleaf figures dir:

    Inputs
    ------
    results/_phase_b_aggregate.csv             (360 rows, all cells, 2 backbones)
    results/baseline/k5_random/                (used by FIG-2 noise floor)
    data/processed/transductive/cora0.8_0_0.2.pkl
        (used only by FIG-5 to look up node degrees in Cora; if missing,
         falls back to torch_geometric.datasets.Planetoid which downloads.)

    Outputs (under --out, default report/paper/overleaf/figures/)
    -------
    FIG-1_Generalization.pdf    fingerprint geometry across Cora/GCN + GAT
    FIG-2_Scaling.pdf           k=5 noise floor per method
    FIG-3_Spectrum.pdf          vulnerability fingerprint on Cora/GCN
    FIG-4a_Significance.pdf     -log10(p) heatmap (Cora/GCN)
    FIG-4b_Effect.pdf           paired effect-size heatmap (Cora/GCN)
    FIG-5_Alignment.pdf         mean-degree of selected nodes vs paired effect

    Usage
    -----
    python scripts/plot_neurips_figures.py
    python scripts/plot_neurips_figures.py --out my_figs/ --only fig3 fig5

The script is intentionally self-contained: no project-internal imports,
all helpers live in this file. Edit the constants at the top to change
methods, strategies, or color palette globally.
"""
from __future__ import annotations

import argparse
import json
import glob
import os
import pickle
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import pearsonr, spearmanr, ttest_rel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Configuration (edit here, not inside individual figure functions)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = REPO_ROOT / "results" / "_phase_b_aggregate.csv"
DEFAULT_OUT = REPO_ROOT / "report" / "paper" / "overleaf" / "figures"
CORA_PKL = REPO_ROOT / "data" / "processed" / "transductive" / "cora0.8_0_0.2.pkl"
RUNS_ROOT = REPO_ROOT / "results" / "runs" / "4090"  # for FIG-5 selected_nodes

# Six methods, three families, two members each — keep the family ordering
# consistent across all figures.
METHODS = ["GIF", "IDEA", "GNNDelete", "MEGU", "GraphEraser", "GraphRevoker"]
ATTACK_STRATS = ["degree", "pagerank", "tracin", "im", "hybrid"]  # excludes 'random'
FAMILY = {
    "GIF": "IF", "IDEA": "IF",
    "GNNDelete": "Learning", "MEGU": "Learning",
    "GraphEraser": "Partition", "GraphRevoker": "Partition",
}
FAMILY_COLOR = {"IF": "#d62728", "Learning": "#1f77b4", "Partition": "#2ca02c"}

# Marker shape per method (within a family the two methods get different
# shapes so paired members are visually distinguishable).
METHOD_MARKER = {
    "GIF": "o", "IDEA": "s",
    "GNNDelete": "o", "MEGU": "s",
    "GraphEraser": "o", "GraphRevoker": "s",
}

# Per-strategy color palette for FIG-5 (not used by other figures).
STRAT_COLOR = {
    "degree":   "#d62728",
    "pagerank": "#9467bd",
    "im":       "#2ca02c",
    "hybrid":   "#ff7f0e",
    "tracin":   "#1f77b4",
}
STRAT_LABEL = {
    "degree": "Degree (L1)", "pagerank": "PageRank (L1)",
    "im": "IM-CELF (L1)", "hybrid": "Hybrid (L2)",
    "tracin": "TracIn (L2-direct)",
}

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "legend.fontsize": 9,
    "figure.dpi": 110,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,   # editable text in PDF (Type 42 = TrueType)
    "ps.fonttype": 42,
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_aggregate(csv_path: Path) -> pd.DataFrame:
    """Load the Phase B aggregate CSV. Each row is one
    (cell, method, strategy, seed) tuple."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Aggregate CSV missing: {csv_path}\n"
            f"  Run scripts/aggregate_phase_b.py first."
        )
    return pd.read_csv(csv_path)


def paired_effects(df: pd.DataFrame, cell: str, method: str, strat: str) -> np.ndarray:
    """Per-seed paired ΔF^attack for one (cell, method, strategy) cell.

    Returns the paired difference (strat.f1_drop − random.f1_drop) per
    matching seed, in F1 percentage points (so multiplied by 100).
    """
    rand = df[(df["cell"] == cell)
              & (df["method"] == method)
              & (df["strategy"] == "random")].set_index("seed")["f1_drop"]
    s = df[(df["cell"] == cell)
           & (df["method"] == method)
           & (df["strategy"] == strat)].set_index("seed")["f1_drop"]
    common = sorted(set(rand.index).intersection(set(s.index)))
    return (s.loc[common].values - rand.loc[common].values) * 100.0


def fingerprint_df(df: pd.DataFrame, cell: str) -> pd.DataFrame:
    """Build the per-method fingerprint coordinates for one cell.

    Columns:
        method, family, im_mean, im_std, tr_mean, tr_std
    where im_mean/tr_mean are the mean paired ΔF^attack on the IM and
    TracIn axes respectively (in % pts).
    """
    rows = []
    for m in METHODS:
        im = paired_effects(df, cell, m, "im")
        tr = paired_effects(df, cell, m, "tracin")
        rows.append({
            "method": m,
            "family": FAMILY[m],
            "im_mean": float(np.mean(im)) if len(im) else float("nan"),
            "im_std":  float(np.std(im, ddof=1)) if len(im) > 1 else 0.0,
            "tr_mean": float(np.mean(tr)) if len(tr) else float("nan"),
            "tr_std":  float(np.std(tr, ddof=1)) if len(tr) > 1 else 0.0,
        })
    return pd.DataFrame(rows)


def load_cora_degrees() -> np.ndarray:
    """Return numpy array of length N=2708, value = degree of each Cora node.

    Tries the cached pickle first (fast); falls back to PyG download.
    Used only by FIG-5.
    """
    if CORA_PKL.exists():
        with open(CORA_PKL, "rb") as f:
            d = pickle.load(f)
        ei = d.edge_index if hasattr(d, "edge_index") else d[0].edge_index
    else:
        # Fallback — heavier dependency but works on any machine
        import torch  # noqa: F401  (referenced via torch_geometric)
        from torch_geometric.datasets import Planetoid
        from torch_geometric.utils import degree as _deg
        ds = Planetoid(root=str(REPO_ROOT / "data" / "raw"), name="Cora")
        ei = ds[0].edge_index
        return _deg(ei[0]).numpy()
    from torch_geometric.utils import degree as _deg
    return _deg(ei[0]).numpy()


def collect_alignment_tuples(df: pd.DataFrame, deg: np.ndarray) -> pd.DataFrame:
    """Collect (cell, method, strategy, seed, mean_d, paired_pct) tuples for
    every non-random run that has a saved selected_nodes list. Used by
    FIG-5 only.
    """
    df_idx = df.set_index(["cell", "method", "strategy", "seed"])
    records = []
    for cell_dir in sorted(glob.glob(str(RUNS_ROOT / "cora_*_r0.05"))):
        cell = os.path.basename(cell_dir)
        for ms_dir in sorted(glob.glob(f"{cell_dir}/*")):
            leaf = os.path.basename(ms_dir)
            if "_" not in leaf:
                continue
            method, strategy = leaf.rsplit("_", 1)
            for seed_dir in sorted(glob.glob(f"{ms_dir}/seed*")):
                seed = int(os.path.basename(seed_dir).replace("seed", ""))
                attack_path = Path(seed_dir) / "attack.json"
                if not attack_path.exists():
                    continue
                payload = json.loads(attack_path.read_text(encoding="utf-8")).get("results", {})
                if not payload:
                    continue
                # results is dict-of-strategies; for an attack run there's one key
                sn = list(payload.values())[0].get("selected_nodes", [])
                if not sn:
                    continue
                sn = np.asarray(sn, dtype=int)
                sn = sn[(sn >= 0) & (sn < len(deg))]
                if sn.size == 0:
                    continue
                mean_d = float(deg[sn].mean())
                try:
                    strat_drop = df_idx.loc[(cell, method, strategy, seed), "f1_drop"]
                    rand_drop = df_idx.loc[(cell, method, "random", seed), "f1_drop"]
                except KeyError:
                    continue
                records.append({
                    "cell": cell, "method": method, "strategy": strategy,
                    "seed": seed, "mean_d": mean_d,
                    "paired_pct": (strat_drop - rand_drop) * 100.0,
                })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def fig3_spectrum(df: pd.DataFrame, out: Path) -> None:
    """FIG-3: 2D fingerprint scatter (Cora/GCN). Single panel.

    Each method is one marker at (paired ΔF^attack_IM, paired ΔF^attack_TracIn);
    a 1σ ellipse covers the seed spread; intra-family pairs are joined by
    a chord to visualise within-pair distance.
    """
    fc = fingerprint_df(df, "cora_GCN_r0.05")
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    ax.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax.axvline(0, color="gray", lw=0.8, alpha=0.5)
    # within-family chords
    for fam in ["IF", "Learning", "Partition"]:
        sub = fc[fc["family"] == fam]
        if len(sub) == 2:
            ax.plot(sub["im_mean"].values, sub["tr_mean"].values, "-",
                    color=FAMILY_COLOR[fam], alpha=0.45, lw=1.2, zorder=1)
    # markers + 1σ ellipses
    for _, r in fc.iterrows():
        c = FAMILY_COLOR[r["family"]]
        mk = METHOD_MARKER[r["method"]]
        ax.scatter(r["im_mean"], r["tr_mean"], s=130, marker=mk,
                   facecolor=c, edgecolor="black", linewidth=1.0, zorder=3,
                   label=f"{r['method']} ({r['family']})")
        if r["im_std"] > 0 or r["tr_std"] > 0:
            ax.add_patch(Ellipse(
                (r["im_mean"], r["tr_mean"]),
                width=2 * r["im_std"], height=2 * r["tr_std"],
                facecolor=c, alpha=0.13, edgecolor=c, lw=0.8, zorder=2,
            ))
        ax.annotate(r["method"], (r["im_mean"], r["tr_mean"]),
                    xytext=(7, 5), textcoords="offset points",
                    fontsize=9, fontweight="bold")
    ax.set_xlabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{IM}}$  (paired, %)")
    ax.set_ylabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{TracIn}}$  (paired, %)")
    ax.set_title(r"Vulnerability Fingerprint (Cora/GCN, $r{=}0.05$, $N{=}5$ seeds)")
    handles, labels = ax.get_legend_handles_labels()
    seen, uniq = set(), []
    for h, lab in zip(handles, labels):
        if lab not in seen:
            seen.add(lab); uniq.append((h, lab))
    ax.legend([h for h, _ in uniq], [l for _, l in uniq],
              loc="lower left", fontsize=8, frameon=True)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "FIG-3_Spectrum.pdf")
    plt.close(fig)
    print("  FIG-3_Spectrum.pdf")


def fig1_generalization(df: pd.DataFrame, out: Path) -> None:
    """FIG-1: same fingerprint geometry across Cora/GCN and Cora/GAT, side by side."""
    cells = [("cora_GCN_r0.05", "Cora · GCN"),
             ("cora_GAT_r0.05", "Cora · GAT")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, (cell, title) in zip(axes, cells):
        fc = fingerprint_df(df, cell)
        ax.axhline(0, color="gray", lw=0.7, alpha=0.5)
        ax.axvline(0, color="gray", lw=0.7, alpha=0.5)
        for fam in ["IF", "Learning", "Partition"]:
            sub = fc[fc["family"] == fam]
            if len(sub) == 2:
                ax.plot(sub["im_mean"].values, sub["tr_mean"].values, "-",
                        color=FAMILY_COLOR[fam], alpha=0.4, lw=1.0)
        for _, r in fc.iterrows():
            c = FAMILY_COLOR[r["family"]]
            mk = METHOD_MARKER[r["method"]]
            ax.scatter(r["im_mean"], r["tr_mean"], s=110, marker=mk,
                       facecolor=c, edgecolor="black", linewidth=0.9, zorder=3)
            ax.annotate(r["method"], (r["im_mean"], r["tr_mean"]),
                        xytext=(6, 4), textcoords="offset points", fontsize=8)
        ax.set_xlabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{IM}}$  (%)")
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{TracIn}}$  (%)")
    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=FAMILY_COLOR[f], markeredgecolor="k",
                   markersize=9, label=f)
        for f in ["IF", "Learning", "Partition"]
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=3,
               frameon=True, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("Fingerprint geometry generalises across GNN backbones",
                 y=1.07, fontsize=13)
    fig.tight_layout()
    fig.savefig(out / "FIG-1_Generalization.pdf")
    plt.close(fig)
    print("  FIG-1_Generalization.pdf")


def fig2_arch(df: pd.DataFrame, out: Path) -> None:
    """FIG-2: ΔF_noise (k=5 noise floor) per (method, backbone).

    The F1 shift induced by deleting just 5 random nodes (~0.18% of
    train) isolates the unlearning algorithm's near-zero-volume response.
    Bar height = F1_before - F1_k=5,
    in F1 percentage points; negative means F1 actually rises (Shard
    Protection). F1_before is read from the Phase B aggregate (random
    strategy's f1_after + f1_drop in any seed); F1_k=5 is the average
    over 5 seeds in results/baseline/k5_random/.
    """
    k5_root = REPO_ROOT / "results" / "baseline" / "k5_random"
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cells = [("cora_GCN_r0.05", "GCN", "Cora·GCN"),
             ("cora_GAT_r0.05", "GAT", "Cora·GAT")]
    bar_w = 0.38
    x = np.arange(len(METHODS))
    for i, (cell, bk, label) in enumerate(cells):
        means, stds = [], []
        for m in METHODS:
            # F1_before from Phase B (random row's f1_after + f1_drop, both per-seed)
            sub_rand = df[(df["cell"] == cell)
                          & (df["method"] == m)
                          & (df["strategy"] == "random")]
            f1_before = (sub_rand["f1_after"] + sub_rand["f1_drop"]).mean()
            # F1_k=5 from baseline_averaged_k5.json
            avg_path = k5_root / m / "cora" / bk / "baseline_averaged_k5.json"
            if not avg_path.exists():
                means.append(np.nan); stds.append(0.0)
                continue
            j = json.loads(avg_path.read_text(encoding="utf-8"))
            f1_k5 = j["f1_after"]
            f1_k5_std = j.get("f1_after_std", 0.0)
            means.append((f1_before - f1_k5) * 100.0)
            stds.append(f1_k5_std * 100.0)
        offset = (i - 0.5) * bar_w
        colors = [FAMILY_COLOR[FAMILY[m]] for m in METHODS]
        edge = "black" if i == 0 else "#444"
        ax.bar(x + offset, means, bar_w, yerr=stds, capsize=3,
               color=colors, edgecolor=edge, lw=0.8,
               alpha=0.85 if i == 0 else 0.55, label=label)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(METHODS, rotation=20, ha="right")
    ax.set_ylabel(r"$\Delta F_{\mathrm{noise}}$ at $k{=}5$  (\% pts)")
    ax.set_title(r"$k{=}5$ noise floor  (negative ${=}$ Shard Protection)")
    family_handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=FAMILY_COLOR[f],
                      edgecolor="black", label=f)
        for f in ["IF", "Learning", "Partition"]
    ]
    backbone_handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor="gray", edgecolor="black",
                      alpha=0.85, label="Cora·GCN"),
        plt.Rectangle((0, 0), 1, 1, facecolor="gray", edgecolor="#444",
                      alpha=0.55, label="Cora·GAT"),
    ]
    leg1 = ax.legend(handles=family_handles, loc="upper left",
                     title="Family", fontsize=9, title_fontsize=10)
    ax.add_artist(leg1)
    ax.legend(handles=backbone_handles, loc="upper right",
              title="Backbone", fontsize=9, title_fontsize=10)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "FIG-2_Scaling.pdf")
    plt.close(fig)
    print("  FIG-2_Scaling.pdf")


def fig4_heatmaps(df: pd.DataFrame, out: Path) -> None:
    """FIG-4a + FIG-4b: significance and effect-size heatmaps on Cora/GCN.

    FIG-4a colors each (method, strategy) cell by -log10(one-sided p) of
    the paired t-test; FIG-4b colors by paired mean effect (% pts).
    """
    cell = "cora_GCN_r0.05"
    p_mat = np.full((len(METHODS), len(ATTACK_STRATS)), np.nan)
    e_mat = np.full((len(METHODS), len(ATTACK_STRATS)), np.nan)
    for i, m in enumerate(METHODS):
        rand_drop = df[(df["cell"] == cell)
                       & (df["method"] == m)
                       & (df["strategy"] == "random")].set_index("seed").sort_index()["f1_drop"]
        for j, s in enumerate(ATTACK_STRATS):
            paired = paired_effects(df, cell, m, s)
            if len(paired) < 2:
                continue
            strat_drop = df[(df["cell"] == cell)
                            & (df["method"] == m)
                            & (df["strategy"] == s)].set_index("seed").sort_index()["f1_drop"]
            common = sorted(set(rand_drop.index).intersection(set(strat_drop.index)))
            t, p = ttest_rel(strat_drop.loc[common].values, rand_drop.loc[common].values)
            p_one = (p / 2) if t > 0 else (1 - p / 2)
            p_mat[i, j] = -np.log10(max(p_one, 1e-10))
            e_mat[i, j] = float(np.mean(paired))

    # ---- FIG-4a: significance ----
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    im = ax.imshow(p_mat, cmap="YlOrRd", aspect="auto", vmin=0, vmax=4)
    ax.set_xticks(range(len(ATTACK_STRATS)))
    ax.set_xticklabels([s.title() for s in ATTACK_STRATS], rotation=30, ha="right")
    ax.set_yticks(range(len(METHODS)))
    ax.set_yticklabels(METHODS)
    for i in range(len(METHODS)):
        for j in range(len(ATTACK_STRATS)):
            v = p_mat[i, j]
            if np.isnan(v):
                continue
            color = "white" if v > 2 else "black"
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=8.5, color=color)
    cbar = plt.colorbar(im, ax=ax, shrink=0.9)
    cbar.set_label(r"$-\log_{10}(p)$  (one-sided)")
    ax.set_title(r"Significance vs. random (Cora/GCN, $N{=}5$)", fontsize=11)
    fig.tight_layout()
    fig.savefig(out / "FIG-4a_Significance.pdf")
    plt.close(fig)
    print("  FIG-4a_Significance.pdf")

    # ---- FIG-4b: effect size ----
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    vmax = max(abs(np.nanmin(e_mat)), abs(np.nanmax(e_mat)))
    im = ax.imshow(e_mat, cmap="RdBu_r", aspect="auto", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(ATTACK_STRATS)))
    ax.set_xticklabels([s.title() for s in ATTACK_STRATS], rotation=30, ha="right")
    ax.set_yticks(range(len(METHODS)))
    ax.set_yticklabels(METHODS)
    for i in range(len(METHODS)):
        for j in range(len(ATTACK_STRATS)):
            v = e_mat[i, j]
            if np.isnan(v):
                continue
            color = "white" if abs(v) > 0.6 * vmax else "black"
            ax.text(j, i, f"{v:+.1f}", ha="center", va="center",
                    fontsize=8.5, color=color)
    cbar = plt.colorbar(im, ax=ax, shrink=0.9)
    cbar.set_label(r"paired $\Delta F^{\mathrm{attack}}$  (% pts)")
    ax.set_title(r"Effect size vs. random (Cora/GCN)", fontsize=11)
    fig.tight_layout()
    fig.savefig(out / "FIG-4b_Effect.pdf")
    plt.close(fig)
    print("  FIG-4b_Effect.pdf")


def fig5_alignment(df: pd.DataFrame, out: Path) -> None:
    """FIG-5: structural alignment panel.

    (a) scatter: each tuple (method, strategy, backbone, seed) plotted
        as (mean degree of selected nodes, paired ΔF^attack); strategies
        order monotonically along the degree axis.
    (b) bar chart: strategy-level mean paired effect, annotated with d̄.
    """
    deg = load_cora_degrees()
    align = collect_alignment_tuples(df, deg)
    nonrand = align[align["strategy"] != "random"].copy()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4),
                             gridspec_kw={"width_ratios": [1.4, 1.0]})

    # ---- panel (a): scatter + strategy-mean error bars ----
    ax = axes[0]
    strat_order = ["degree", "pagerank", "im", "hybrid", "tracin"]
    for s in strat_order:
        sub = nonrand[nonrand["strategy"] == s]
        ax.scatter(sub["mean_d"], sub["paired_pct"], s=18, alpha=0.22,
                   color=STRAT_COLOR[s], edgecolor="none")
    ax.axhline(0, color="gray", lw=0.7, alpha=0.6)
    rand_mean_d = align[align["strategy"] == "random"]["mean_d"].mean()
    ax.axvline(rand_mean_d, color="gray", lw=0.7, alpha=0.6, linestyle="--")
    ax.text(rand_mean_d + 0.3, ax.get_ylim()[0] + 0.5,
            r"random $\bar{d}$", fontsize=8, color="gray")
    for s in strat_order:
        sub = nonrand[nonrand["strategy"] == s]
        mx, my = sub["mean_d"].mean(), sub["paired_pct"].mean()
        ex = sub["mean_d"].std(ddof=1)
        ey = sub["paired_pct"].std(ddof=1)
        c = STRAT_COLOR[s]
        ax.errorbar(mx, my, xerr=ex, yerr=ey, fmt="o", markersize=10,
                    color=c, ecolor=c, markeredgecolor="black",
                    markeredgewidth=0.9, capsize=3, zorder=5,
                    label=STRAT_LABEL[s])
    r, p = pearsonr(nonrand["mean_d"], nonrand["paired_pct"])
    rs, ps = spearmanr(nonrand["mean_d"], nonrand["paired_pct"])
    ax.text(0.02, 0.97,
            f"Pearson $r={r:.2f}$, $p={p:.0e}$\n"
            f"Spearman $\\rho={rs:.2f}$, $p={ps:.0e}$\n"
            f"$n={len(nonrand)}$ tuples",
            transform=ax.transAxes, va="top", ha="left", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="gray", alpha=0.85))
    ax.set_xlabel(r"$\bar{d}$  (mean degree of selected nodes)")
    ax.set_ylabel(r"paired $\Delta F^{\mathrm{attack}}$  (% pts vs same-seed random)")
    ax.set_title("(a) Selection-degree predicts attack effect")
    ax.legend(loc="lower right", fontsize=8, frameon=True)
    ax.grid(True, alpha=0.25)

    # ---- panel (b): strategy-level bars ----
    ax = axes[1]
    summary = nonrand.groupby("strategy")[["mean_d", "paired_pct"]].agg(["mean", "std"])
    xs = np.arange(len(strat_order))
    means = [summary.loc[s, ("paired_pct", "mean")] for s in strat_order]
    stds = [summary.loc[s, ("paired_pct", "std")] for s in strat_order]
    colors = [STRAT_COLOR[s] for s in strat_order]
    ax.bar(xs, means, yerr=stds, capsize=3, color=colors,
           edgecolor="black", lw=0.8, alpha=0.88)
    for i, s in enumerate(strat_order):
        d_mean = summary.loc[s, ("mean_d", "mean")]
        ax.annotate(rf"$\bar{{d}}={d_mean:.1f}$", (xs[i], means[i]),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8.5)
    ax.axhline(0, color="black", lw=0.7)
    ax.set_xticks(xs)
    ax.set_xticklabels([STRAT_LABEL[s].split(" (")[0] for s in strat_order],
                       rotation=20, ha="right")
    ax.set_ylabel(r"mean paired $\Delta F^{\mathrm{attack}}$  (% pts)")
    ax.set_title("(b) Strategy means")
    ax.grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out / "FIG-5_Alignment.pdf")
    plt.close(fig)
    print("  FIG-5_Alignment.pdf")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

FIGURES = {
    "fig1": ("FIG-1_Generalization", fig1_generalization),
    "fig2": ("FIG-2_Scaling",        fig2_arch),
    "fig3": ("FIG-3_Spectrum",       fig3_spectrum),
    "fig4": ("FIG-4_Heatmaps",       fig4_heatmaps),
    "fig5": ("FIG-5_Alignment",      fig5_alignment),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV,
                    help=f"Phase B aggregate CSV (default: {DEFAULT_CSV})")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"Output directory for PDFs (default: {DEFAULT_OUT})")
    ap.add_argument("--only", nargs="+", choices=list(FIGURES) + ["all"],
                    default=["all"],
                    help="Subset of figures to generate (default: all)")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    df = load_aggregate(args.csv)

    targets = list(FIGURES) if "all" in args.only else args.only
    print(f"[plot] csv = {args.csv}")
    print(f"[plot] out = {args.out}")
    print(f"[plot] generating: {targets}")
    print()

    for key in targets:
        _, fn = FIGURES[key]
        fn(df, args.out)

    print()
    print("Done. PDFs:")
    for f in sorted(args.out.glob("FIG-*.pdf")):
        print(f"  {f.name}: {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
