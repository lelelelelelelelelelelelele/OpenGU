"""Generate the 6 NeurIPS paper figures from Phase B aggregate data.

This is the canonical figure generator for the current paper revision.
It reads ONLY two inputs and writes 6 PDFs to the Overleaf figures dir:

    Inputs
    ------
    results/_phase_b_aggregate.csv             (360 rows, all cells, 2 backbones)
    data/processed/transductive/cora0.8_0_0.2.pkl
        (used only by FIG-5 to look up node degrees in Cora; if missing,
         falls back to torch_geometric.datasets.Planetoid which downloads.)

    Outputs (under --out, default report/paper/overleaf/figures/)
    -------
    FIG-1_Generalization.pdf    fingerprint geometry across Cora/GCN + GAT
    FIG-2_Scaling.pdf           random-deletion F1 drop at r=5% per method
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

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import pearsonr, spearmanr, ttest_rel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = "results\_phase_b_aggregate.csv"
DEFAULT_OUT = REPO_ROOT / "report" / "paper" / "overleaf" / "figures"
CORA_PKL = REPO_ROOT / "data" / "processed" / "transductive" / "cora0.8_0_0.2.pkl"
RUNS_ROOT = REPO_ROOT / "results" / "runs" / "4090"  # for FIG-5 selected_nodes

METHODS = ["GIF", "IDEA", "GNNDelete", "MEGU", "GraphEraser", "GraphRevoker"]
ATTACK_STRATS = ["degree", "pagerank", "tracin", "im", "hybrid"]

FAMILY = {
    "GIF": "IF", "IDEA": "IF",
    "GNNDelete": "Learning", "MEGU": "Learning",
    "GraphEraser": "Partition", "GraphRevoker": "Partition",
}

# ---------------------------------------------------------------------------
# Paper style
# ---------------------------------------------------------------------------

COLORS = {
    "green":  "#89e0cd",
    "red":    "#efc4cd",
    "grey":   "#d0d5d8",
    "orange": "#efd3cc",
    "purple": "#c7aebb",
    "blue":   "#b7c8e8",
    "dark":   "#2f3437",
    "mid":    "#6f777d",
    "light":  "#f4f6f7",
    "white":  "#ffffff",
}

FAMILY_COLOR = {
    "IF": COLORS["red"],
    "Learning": COLORS["green"],
    "Partition": COLORS["purple"],
}

METHOD_MARKER = {
    "GIF": "o", "IDEA": "s",
    "GNNDelete": "o", "MEGU": "s",
    "GraphEraser": "o", "GraphRevoker": "s",
}

STRAT_COLOR = {
    "degree":   COLORS["red"],
    "pagerank": COLORS["purple"],
    "im":       COLORS["green"],
    "hybrid":   COLORS["orange"],
    "tracin":   COLORS["blue"],
}

STRAT_LABEL = {
    "degree": "Degree (L1)",
    "pagerank": "PageRank (L1)",
    "im": "IM-CELF (L1)",
    "hybrid": "Hybrid (L2)",
    "tracin": "TracIn (L2-direct)",
}

CMAP_SIG = LinearSegmentedColormap.from_list(
    "soft_sig",
    [COLORS["white"], COLORS["orange"], COLORS["red"]],
)

CMAP_EFF = LinearSegmentedColormap.from_list(
    "soft_eff",
    [COLORS["purple"], COLORS["white"], COLORS["green"]],
)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Optima", "DejaVu Sans", "Arial"],
    "mathtext.fontset": "dejavusans",

    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelweight": "bold",

    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "xtick.major.size": 3.5,
    "ytick.major.size": 3.5,

    "legend.fontsize": 10,
    "legend.title_fontsize": 10,
    "legend.frameon": True,
    "legend.framealpha": 0.92,
    "legend.edgecolor": COLORS["grey"],
    "legend.facecolor": "white",

    "axes.edgecolor": COLORS["dark"],
    "axes.linewidth": 1.0,
    "axes.facecolor": "white",
    "figure.facecolor": "white",

    "grid.color": COLORS["grey"],
    "grid.linewidth": 0.6,
    "grid.alpha": 0.28,

    "lines.linewidth": 1.8,
    "patch.linewidth": 0.9,

    "figure.dpi": 160,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,

    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


# ---------------------------------------------------------------------------
# Style helpers
# ---------------------------------------------------------------------------

def prettify_ax(ax, grid_axis: str = "both") -> None:
    """Apply consistent paper-style axis formatting."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["dark"])
    ax.spines["bottom"].set_color(COLORS["dark"])
    ax.tick_params(axis="both", colors=COLORS["dark"], labelcolor=COLORS["dark"])
    ax.grid(True, axis=grid_axis, alpha=0.28, linewidth=0.6)


def soft_legend(ax, **kwargs):
    """Legend with a soft white frame."""
    leg = ax.legend(**kwargs)
    if leg is not None:
        leg.get_frame().set_facecolor("white")
        leg.get_frame().set_edgecolor(COLORS["grey"])
        leg.get_frame().set_linewidth(0.8)
    return leg


def save_pdf(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def apply_heatmap_grid(ax, n_rows: int, n_cols: int) -> None:
    """White cell borders for heatmaps."""
    ax.set_xticks(np.arange(n_cols + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(n_rows + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_aggregate(csv_path: Path) -> pd.DataFrame:
    """Load the Phase B aggregate CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Aggregate CSV missing: {csv_path}\n"
            f"  Run scripts/aggregate_phase_b.py first."
        )
    return pd.read_csv(csv_path)


def paired_effects(df: pd.DataFrame, cell: str, method: str, strat: str) -> np.ndarray:
    """Per-seed paired ΔF^attack for one (cell, method, strategy) cell."""
    rand = df[
        (df["cell"] == cell)
        & (df["method"] == method)
        & (df["strategy"] == "random")
    ].set_index("seed")["paired_dF_pct"]

    s = df[
        (df["cell"] == cell)
        & (df["method"] == method)
        & (df["strategy"] == strat)
    ].set_index("seed")["paired_dF_pct"]

    common = sorted(set(rand.index).intersection(set(s.index)))
    return (s.loc[common].values - rand.loc[common].values) * 100.0


def fingerprint_df(df: pd.DataFrame, cell: str) -> pd.DataFrame:
    """Build the per-method fingerprint coordinates for one cell."""
    rows = []
    for m in METHODS:
        im = paired_effects(df, cell, m, "im")
        tr = paired_effects(df, cell, m, "tracin")
        rows.append({
            "method": m,
            "family": FAMILY[m],
            "im_mean": float(np.mean(im)) if len(im) else float("nan"),
            "im_std": float(np.std(im, ddof=1)) if len(im) > 1 else 0.0,
            "tr_mean": float(np.mean(tr)) if len(tr) else float("nan"),
            "tr_std": float(np.std(tr, ddof=1)) if len(tr) > 1 else 0.0,
        })
    return pd.DataFrame(rows)


def load_cora_degrees() -> np.ndarray:
    """Return numpy array of length N=2708, value = degree of each Cora node."""
    if CORA_PKL.exists():
        with open(CORA_PKL, "rb") as f:
            d = pickle.load(f)
        ei = d.edge_index if hasattr(d, "edge_index") else d[0].edge_index
    else:
        import torch  # noqa: F401
        from torch_geometric.datasets import Planetoid
        from torch_geometric.utils import degree as _deg
        ds = Planetoid(root=str(REPO_ROOT / "data" / "raw"), name="Cora")
        ei = ds[0].edge_index
        return _deg(ei[0]).numpy()

    from torch_geometric.utils import degree as _deg
    return _deg(ei[0]).numpy()


def collect_alignment_tuples(df: pd.DataFrame, deg: np.ndarray) -> pd.DataFrame:
    """Collect (cell, method, strategy, seed, mean_d, paired_pct) tuples."""
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

                payload = json.loads(
                    attack_path.read_text(encoding="utf-8")
                ).get("results", {})

                if not payload:
                    continue

                sn = list(payload.values())[0].get("selected_nodes", [])
                if not sn:
                    continue

                sn = np.asarray(sn, dtype=int)
                sn = sn[(sn >= 0) & (sn < len(deg))]
                if sn.size == 0:
                    continue

                mean_d = float(deg[sn].mean())

                try:
                    strat_drop = df_idx.loc[(cell, method, strategy, seed), "paired_dF_pct"]
                    rand_drop = df_idx.loc[(cell, method, "random", seed), "paired_dF_pct"]
                except KeyError:
                    continue

                records.append({
                    "cell": cell,
                    "method": method,
                    "strategy": strategy,
                    "seed": seed,
                    "mean_d": mean_d,
                    "paired_pct": (strat_drop - rand_drop) * 100.0,
                })

    return pd.DataFrame(
        records,
        columns=["cell", "method", "strategy", "seed", "mean_d", "paired_pct"],
    )


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def fig3_spectrum(df: pd.DataFrame, out: Path) -> None:
    """FIG-3: 2D fingerprint scatter (Cora/GCN).

    Labels are placed directly below points without connector lines.
    """
    fc = fingerprint_df(df, "cora_GCN_r0.05")

    fig, ax = plt.subplots(figsize=(6.8, 5.15))

    ax.axhline(0, color=COLORS["mid"], lw=0.9, alpha=0.55, zorder=0)
    ax.axvline(0, color=COLORS["mid"], lw=0.9, alpha=0.55, zorder=0)

    # within-family chords
    for fam in ["IF", "Learning", "Partition"]:
        sub = fc[fc["family"] == fam]
        if len(sub) == 2:
            ax.plot(
                sub["im_mean"].values,
                sub["tr_mean"].values,
                "-",
                color=FAMILY_COLOR[fam],
                alpha=0.45,
                lw=1.4,
                zorder=1,
            )

    # Put labels below points; small horizontal shifts to avoid collisions.
    label_offsets = {
        "GIF": (0, -14),
        "IDEA": (0, -14),
        "GNNDelete": (-8, -14),
        "MEGU": (8, -14),
        "GraphEraser": (-10, -14),
        "GraphRevoker": (10, -14),
    }

    for _, r in fc.iterrows():
        c = FAMILY_COLOR[r["family"]]
        mk = METHOD_MARKER[r["method"]]

        ax.scatter(
            r["im_mean"],
            r["tr_mean"],
            s=120,
            marker=mk,
            facecolor=c,
            edgecolor=COLORS["dark"],
            linewidth=1.05,
            alpha=0.95,
            zorder=4,
            label=f"{r['method']} ({r['family']})",
        )

        if r["im_std"] > 0 or r["tr_std"] > 0:
            ax.add_patch(Ellipse(
                (r["im_mean"], r["tr_mean"]),
                width=2 * r["im_std"],
                height=2 * r["tr_std"],
                facecolor=c,
                alpha=0.14,
                edgecolor=c,
                lw=0.9,
                zorder=2,
            ))

    # labels directly below points, no connector lines
    for _, r in fc.iterrows():
        dx, dy = label_offsets.get(r["method"], (0, -14))
        ax.annotate(
            r["method"],
            xy=(r["im_mean"], r["tr_mean"]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=9.0,
            fontweight="bold",
            color=COLORS["dark"],
            ha="center",
            va="top",
            bbox=dict(
                boxstyle="round,pad=0.18",
                facecolor="white",
                edgecolor="none",
                alpha=0.88,
            ),
            zorder=6,
        )

    ax.set_xlabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{IM}}$  (paired, %)")
    ax.set_ylabel(r"$\Delta F^{\mathrm{attack}}_{\mathrm{TracIn}}$  (paired, %)")
    ax.set_title(r"Vulnerability Fingerprint (Cora/GCN, $r{=}0.05$, $N{=}5$ seeds)")

    x_min, x_max = fc["im_mean"].min(), fc["im_mean"].max()
    y_min, y_max = fc["tr_mean"].min(), fc["tr_mean"].max()
    x_pad = max(1.0, 0.18 * (x_max - x_min))
    y_pad = max(0.8, 0.22 * (y_max - y_min))
    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)

    handles, labels = ax.get_legend_handles_labels()
    seen, uniq = set(), []
    for h, lab in zip(handles, labels):
        if lab not in seen:
            seen.add(lab)
            uniq.append((h, lab))

    soft_legend(
        ax,
        handles=[h for h, _ in uniq],
        labels=[l for _, l in uniq],
        loc="lower left",
        fontsize=8.4,
        frameon=True,
    )

    prettify_ax(ax)
    save_pdf(fig, out / "FIG-3_Spectrum.pdf")
    print("  FIG-3_Spectrum.pdf")

def fig2_arch(df: pd.DataFrame, out: Path) -> None:
    """FIG-2: ΔF_arch (intrinsic, k=5) per (method, backbone)."""
    k5_root = REPO_ROOT / "results" / "baseline" / "k5_random"

    fig, ax = plt.subplots(figsize=(8.2, 4.7))

    cells = [
        ("cora_GCN_r0.05", "GCN", "Cora·GCN"),
        ("cora_GAT_r0.05", "GAT", "Cora·GAT"),
    ]

    bar_w = 0.38
    x = np.arange(len(METHODS))

    for i, (cell, bk, label) in enumerate(cells):
        means, stds = [], []

        for m in METHODS:
            sub_rand = df[
                (df["cell"] == cell)
                & (df["method"] == m)
                & (df["strategy"] == "random")
            ]
            f1_before = (sub_rand["f1_after"] + sub_rand["paired_dF_pct"]).mean()

            avg_path = k5_root / m / "cora" / bk / "baseline_averaged_k5.json"
            if not avg_path.exists():
                means.append(np.nan)
                stds.append(0.0)
                continue

            j = json.loads(avg_path.read_text(encoding="utf-8"))
            f1_k5 = j["f1_after"]
            f1_k5_std = j.get("f1_after_std", 0.0)

            means.append((f1_before - f1_k5) * 100.0)
            stds.append(f1_k5_std * 100.0)

        offset = (i - 0.5) * bar_w
        colors = [FAMILY_COLOR[FAMILY[m]] for m in METHODS]

        ax.bar(
            x + offset,
            means,
            bar_w,
            yerr=stds,
            capsize=3,
            color=colors,
            edgecolor=COLORS["dark"],
            lw=0.9,
            alpha=0.92 if i == 0 else 0.62,
            error_kw=dict(
                elinewidth=0.9,
                ecolor=COLORS["dark"],
                capthick=0.9,
            ),
            label=label,
        )

    ax.axhline(0, color=COLORS["dark"], lw=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(METHODS, rotation=22, ha="right", fontweight="bold")
    ax.set_ylabel(r"$\Delta F_{\mathrm{arch}}$ at $k{=}5$  (\% pts)")
    ax.set_title(r"Intrinsic Architectural F1 Shift")

    family_handles = [
        plt.Rectangle(
            (0, 0), 1, 1,
            facecolor=FAMILY_COLOR[f],
            edgecolor=COLORS["dark"],
            label=f,
        )
        for f in ["IF", "Learning", "Partition"]
    ]

    backbone_handles = [
        plt.Rectangle(
            (0, 0), 1, 1,
            facecolor=COLORS["grey"],
            edgecolor=COLORS["dark"],
            alpha=0.92,
            label="Cora·GCN",
        ),
        plt.Rectangle(
            (0, 0), 1, 1,
            facecolor=COLORS["grey"],
            edgecolor=COLORS["dark"],
            alpha=0.62,
            label="Cora·GAT",
        ),
    ]

    leg1 = ax.legend(
        handles=family_handles,
        loc="upper left",
        title="Family",
        fontsize=9.5,
        title_fontsize=10,
        frameon=True,
    )
    ax.add_artist(leg1)

    soft_legend(
        ax,
        handles=backbone_handles,
        loc="upper right",
        title="Backbone",
        fontsize=9.5,
        title_fontsize=10,
        frameon=True,
    )

    prettify_ax(ax, grid_axis="y")
    save_pdf(fig, out / "FIG-2_Scaling.pdf")
    print("  FIG-2_Scaling.pdf")


def fig4_heatmaps(df: pd.DataFrame, out: Path) -> None:
    """FIG-4a + FIG-4b: significance and effect-size heatmaps on Cora/GCN."""
    cell = "cora_GCN_r0.05"

    p_mat = np.full((len(METHODS), len(ATTACK_STRATS)), np.nan)
    e_mat = np.full((len(METHODS), len(ATTACK_STRATS)), np.nan)

    for i, m in enumerate(METHODS):
        rand_drop = df[
            (df["cell"] == cell)
            & (df["method"] == m)
            & (df["strategy"] == "random")
        ].set_index("seed").sort_index()["paired_dF_pct"]

        for j, s in enumerate(ATTACK_STRATS):
            paired = paired_effects(df, cell, m, s)
            if len(paired) < 2:
                continue

            strat_drop = df[
                (df["cell"] == cell)
                & (df["method"] == m)
                & (df["strategy"] == s)
            ].set_index("seed").sort_index()["paired_dF_pct"]

            common = sorted(set(rand_drop.index).intersection(set(strat_drop.index)))
            t, p = ttest_rel(strat_drop.loc[common].values, rand_drop.loc[common].values)
            p_one = (p / 2) if t > 0 else (1 - p / 2)

            p_mat[i, j] = -np.log10(max(p_one, 1e-10))
            e_mat[i, j] = float(np.mean(paired))

    # ---- FIG-4a: significance ----
    fig, ax = plt.subplots(figsize=(7.4, 5.6))

    im = ax.imshow(p_mat, cmap=CMAP_SIG, aspect="auto", vmin=0, vmax=4)

    ax.set_xticks(range(len(ATTACK_STRATS)))
    ax.set_xticklabels(
        [s.title() for s in ATTACK_STRATS],
        rotation=28,
        ha="right",
        fontweight="bold",
        fontsize=18,
    )
    ax.set_yticks(range(len(METHODS)))
    ax.set_yticklabels(METHODS, fontweight="bold", fontsize=18)

    apply_heatmap_grid(ax, len(METHODS), len(ATTACK_STRATS))

    for i in range(len(METHODS)):
        for j in range(len(ATTACK_STRATS)):
            v = p_mat[i, j]
            if np.isnan(v):
                continue
            color = COLORS["dark"] if v < 2.6 else "white"
            ax.text(
                j,
                i,
                f"{v:.1f}",
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold",
                color=color,
            )

    cbar = plt.colorbar(im, ax=ax, shrink=0.9)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(
        r"$-\log_{10}(p)$  (one-sided)",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_title(
        r"Significance vs. Random (Cora/GCN, $N{=}5$)",
        fontsize=18,
        fontweight="bold",
        pad=12,
    )
    save_pdf(fig, out / "FIG-4a_Significance.pdf")
    print("  FIG-4a_Significance.pdf")

    # ---- FIG-4b: effect size ----
    fig, ax = plt.subplots(figsize=(7.4, 5.6))

    vmax = max(abs(np.nanmin(e_mat)), abs(np.nanmax(e_mat)))
    im = ax.imshow(e_mat, cmap=CMAP_EFF, aspect="auto", vmin=-vmax, vmax=vmax)

    ax.set_xticks(range(len(ATTACK_STRATS)))
    ax.set_xticklabels(
        [s.title() for s in ATTACK_STRATS],
        rotation=28,
        ha="right",
        fontweight="bold",
        fontsize=18,
    )
    ax.set_yticks(range(len(METHODS)))
    ax.set_yticklabels(METHODS, fontweight="bold", fontsize=18)

    apply_heatmap_grid(ax, len(METHODS), len(ATTACK_STRATS))

    for i in range(len(METHODS)):
        for j in range(len(ATTACK_STRATS)):
            v = e_mat[i, j]
            if np.isnan(v):
                continue
            color = COLORS["dark"] if abs(v) < 0.65 * vmax else "white"
            ax.text(
                j,
                i,
                f"{v:+.1f}",
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold",
                color=color,
            )

    cbar = plt.colorbar(im, ax=ax, shrink=0.9)
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(
        r"paired $\Delta F^{\mathrm{attack}}$  (% pts)",
        fontsize=18,
        fontweight="bold",
    )

    ax.set_title(
        r"Effect Size vs. Random (Cora/GCN)",
        fontsize=18,
        fontweight="bold",
        pad=12,
    )
    save_pdf(fig, out / "FIG-4b_Effect.pdf")
    print("  FIG-4b_Effect.pdf")

def fig5_alignment(df: pd.DataFrame, out: Path) -> None:
    """FIG-5: structural alignment panel."""
    deg = load_cora_degrees()
    align = collect_alignment_tuples(df, deg)

    if align.empty or "strategy" not in align.columns:
        print("[WARN] FIG-5 skipped: no alignment tuples collected.")
        print(f"[WARN] Check RUNS_ROOT = {RUNS_ROOT}")
        return

    nonrand = align[align["strategy"] != "random"].copy()

    if nonrand.empty:
        print("[WARN] FIG-5 skipped: no non-random alignment tuples collected.")
        return

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.2, 4.5),
        gridspec_kw={"width_ratios": [1.4, 1.0]},
    )

    # ---- panel (a): scatter + strategy-mean error bars ----
    ax = axes[0]
    strat_order = ["degree", "pagerank", "im", "hybrid", "tracin"]

    for s in strat_order:
        sub = nonrand[nonrand["strategy"] == s]
        ax.scatter(
            sub["mean_d"],
            sub["paired_pct"],
            s=28,
            alpha=0.28,
            color=STRAT_COLOR[s],
            edgecolor="none",
            rasterized=True,
        )

    ax.axhline(0, color=COLORS["mid"], lw=0.9, alpha=0.6)

    rand_mean_d = align[align["strategy"] == "random"]["mean_d"].mean()
    if not np.isnan(rand_mean_d):
        ax.axvline(
            rand_mean_d,
            color=COLORS["mid"],
            lw=0.9,
            alpha=0.65,
            linestyle="--",
        )
        ax.text(
            rand_mean_d + 0.3,
            ax.get_ylim()[0] + 0.5,
            r"random $\bar{d}$",
            fontsize=8.8,
            color=COLORS["mid"],
            fontweight="bold",
        )

    for s in strat_order:
        sub = nonrand[nonrand["strategy"] == s]
        if sub.empty:
            continue

        mx, my = sub["mean_d"].mean(), sub["paired_pct"].mean()
        ex = sub["mean_d"].std(ddof=1)
        ey = sub["paired_pct"].std(ddof=1)
        c = STRAT_COLOR[s]

        ax.errorbar(
            mx,
            my,
            xerr=ex,
            yerr=ey,
            fmt="o",
            markersize=11,
            color=c,
            ecolor=c,
            markeredgecolor=COLORS["dark"],
            markeredgewidth=1.0,
            capsize=3,
            elinewidth=1.1,
            zorder=5,
            label=STRAT_LABEL[s],
        )

    r, p = pearsonr(nonrand["mean_d"], nonrand["paired_pct"])
    rs, ps = spearmanr(nonrand["mean_d"], nonrand["paired_pct"])

    ax.text(
        0.02,
        0.97,
        f"Pearson $r={r:.2f}$, $p={p:.0e}$\n"
        f"Spearman $\\rho={rs:.2f}$, $p={ps:.0e}$\n"
        f"$n={len(nonrand)}$ tuples",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="white",
            edgecolor=COLORS["grey"],
            linewidth=0.8,
            alpha=0.92,
        ),
    )

    ax.set_xlabel(r"$\bar{d}$  (mean degree of selected nodes)")
    ax.set_ylabel(r"paired $\Delta F^{\mathrm{attack}}$  (% pts vs. same-seed random)")
    ax.set_title("(a) Selection Degree Predicts Attack Effect")
    soft_legend(ax, loc="lower right", fontsize=8.8, frameon=True)
    prettify_ax(ax)

    # ---- panel (b): strategy-level bars ----
    ax = axes[1]
    summary = nonrand.groupby("strategy")[["mean_d", "paired_pct"]].agg(["mean", "std"])

    xs = np.arange(len(strat_order))
    means = [summary.loc[s, ("paired_pct", "mean")] for s in strat_order]
    stds = [summary.loc[s, ("paired_pct", "std")] for s in strat_order]
    colors = [STRAT_COLOR[s] for s in strat_order]

    ax.bar(
        xs,
        means,
        yerr=stds,
        capsize=3,
        color=colors,
        edgecolor=COLORS["dark"],
        lw=0.9,
        alpha=0.92,
        error_kw=dict(
            elinewidth=0.9,
            ecolor=COLORS["dark"],
            capthick=0.9,
        ),
    )

    for i, s in enumerate(strat_order):
        d_mean = summary.loc[s, ("mean_d", "mean")]
        ax.annotate(
            rf"$\bar{{d}}={d_mean:.1f}$",
            (xs[i], means[i]),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8.8,
            fontweight="bold",
            color=COLORS["dark"],
        )

    ax.axhline(0, color=COLORS["dark"], lw=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(
        [STRAT_LABEL[s].split(" (")[0] for s in strat_order],
        rotation=22,
        ha="right",
        fontweight="bold",
    )
    ax.set_ylabel(r"mean paired $\Delta F^{\mathrm{attack}}$  (% pts)")
    ax.set_title("(b) Strategy Means")
    prettify_ax(ax, grid_axis="y")

    save_pdf(fig, out / "FIG-5_Alignment.pdf")
    print("  FIG-5_Alignment.pdf")

def fig1_generalization(df: pd.DataFrame, out: Path) -> None:
    """FIG-1: same fingerprint geometry across Cora/GCN and Cora/GAT.

    Text labels are removed from the plot area and replaced by a legend
    that jointly encodes method color and marker shape.
    """
    cells = [
        ("cora_GCN_r0.05", "Cora · GCN"),
        ("cora_GAT_r0.05", "Cora · GAT"),
    ]

    # 缩小整体图尺寸
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.2), sharey=True)

    for ax, (cell, title) in zip(axes, cells):
        fc = fingerprint_df(df, cell)

        ax.axhline(0, color=COLORS["mid"], lw=0.9, alpha=0.55, zorder=0)
        ax.axvline(0, color=COLORS["mid"], lw=0.9, alpha=0.55, zorder=0)

        # within-family chords
        for fam in ["IF", "Learning", "Partition"]:
            sub = fc[fc["family"] == fam]
            if len(sub) == 2:
                ax.plot(
                    sub["im_mean"].values,
                    sub["tr_mean"].values,
                    "-",
                    color=FAMILY_COLOR[fam],
                    alpha=0.50,
                    lw=1.5,
                    zorder=1,
                )

        # scatter points：缩小图，但把 marker 放大
        for _, r in fc.iterrows():
            c = FAMILY_COLOR[r["family"]]
            mk = METHOD_MARKER[r["method"]]

            ax.scatter(
                r["im_mean"],
                r["tr_mean"],
                s=280,   # 比之前更大
                marker=mk,
                facecolor=c,
                edgecolor=COLORS["dark"],
                linewidth=1.2,
                alpha=0.97,
                zorder=3,
            )

        ax.set_xlabel(
            r"$\Delta F^{\mathrm{attack}}_{\mathrm{IM}}$  (%)",
            fontsize=13,
            fontweight="bold",
        )
        ax.set_title(title, pad=8, fontsize=13, fontweight="bold")
        prettify_ax(ax)
        ax.tick_params(axis="both", labelsize=11)

        # 不再需要为文字额外留太多空白，但仍保留一点 padding
        x_min, x_max = fc["im_mean"].min(), fc["im_mean"].max()
        y_min, y_max = fc["tr_mean"].min(), fc["tr_mean"].max()

        x_range = max(x_max - x_min, 1.0)
        y_range = max(y_max - y_min, 1.0)

        x_pad = max(0.9, 0.18 * x_range)
        y_pad = max(0.9, 0.20 * y_range)

        ax.set_xlim(x_min - x_pad, x_max + x_pad)
        ax.set_ylim(bottom=-5.5, top=y_max + y_pad)

    axes[0].set_ylabel(
        r"$\Delta F^{\mathrm{attack}}_{\mathrm{TracIn}}$  (%)",
        fontsize=13,
        fontweight="bold",
    )

    # 用 legend 同时表示颜色 + 形状 + 方法名
    method_handles = []
    for m in METHODS:
        method_handles.append(
            plt.Line2D(
                [0], [0],
                marker=METHOD_MARKER[m],
                color="w",
                markerfacecolor=FAMILY_COLOR[FAMILY[m]],
                markeredgecolor=COLORS["dark"],
                markeredgewidth=1.1,
                markersize=11.5,
                linestyle="None",
                label=m,
            )
        )

    fig.legend(
        handles=method_handles,
        loc="center",
        ncol=3,
        frameon=True,
        bbox_to_anchor=(0.5, 1.03),
        fontsize=10.5,
        columnspacing=1.2,
        handletextpad=0.5,
    )

    save_pdf(fig, out / "FIG-1_Generalization.pdf")
    print("  FIG-1_Generalization.pdf")
# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

FIGURES = {
    "fig1": ("FIG-1_Generalization", fig1_generalization),
    "fig2": ("FIG-2_Scaling", fig2_arch),
    "fig3": ("FIG-3_Spectrum", fig3_spectrum),
    "fig4": ("FIG-4_Heatmaps", fig4_heatmaps),
    "fig5": ("FIG-5_Alignment", fig5_alignment),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"Phase B aggregate CSV (default: {DEFAULT_CSV})",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output directory for PDFs (default: {DEFAULT_OUT})",
    )
    ap.add_argument(
        "--only",
        nargs="+",
        choices=list(FIGURES) + ["all"],
        default=["all"],
        help="Subset of figures to generate (default: all)",
    )

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