import glob
import json
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_rel


RESULTS_FIG_DIR = Path("results/paper_figures")
REPORT_FIG_DIR = Path("report/paper/figures")
OVERLEAF_FIG_DIR = Path("report/overleaf_upload_2026-04-14/figures/paper_figures")
FINAL_STATS_PATH = Path("results/evaluation/stats/final_paper_stats.csv")
RATIO_SUMMARY_GLOB = "results/experiments/ratio_sensitivity/phase_a/*/_summary.json"

FIG4_METHOD_ORDER = ["GIF", "GNNDelete", "GraphEraser", "IDEA", "MEGU"]
FIG_ATTACK_STRATEGIES = ["TracIn", "IM", "Hybrid"]
CORE_STRATEGY_LABELS = {
    "tracin": "TracIn",
    "im_v4": "IM",
    "hybrid_v4": "Hybrid",
}
FIG2_STRATEGY_LABELS = {
    "random": "random",
    **CORE_STRATEGY_LABELS,
}
FIG4_JSON_PATTERNS = {
    "GIF": "results/experiments/mg0_completion/phase_a/*/GIF_cora_GCN_r0.05_s*.json",
    "GNNDelete": "results/experiments/mg0_completion/phase_a/*/GNNDelete_cora_GCN_r0.05_s*.json",
    "GraphEraser": "results/experiments/mg0_completion/phase_a/*/GraphEraser_cora_GCN_r0.05_s*.json",
    "IDEA": "results/experiments/mg3_gat/phase_a/*/IDEA_cora_GAT_r0.05_s*.json",
    "MEGU": "results/experiments/mg3_gat/phase_a/*/MEGU_cora_GAT_r0.05_s*.json",
}

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "figure.titlesize": 16,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

for out_dir in (RESULTS_FIG_DIR, REPORT_FIG_DIR, OVERLEAF_FIG_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)


def load_final_stats() -> pd.DataFrame:
    return pd.read_csv(FINAL_STATS_PATH)


def save_figure(fig: plt.Figure, stem: str) -> None:
    for out_dir in (RESULTS_FIG_DIR, REPORT_FIG_DIR, OVERLEAF_FIG_DIR):
        fig.savefig(out_dir / f"{stem}.pdf", bbox_inches="tight")
        fig.savefig(out_dir / f"{stem}.png", bbox_inches="tight", dpi=300)


def build_fig2_ratio_dataframe() -> pd.DataFrame:
    baseline_f1_map = {}
    for method in ("GIF", "GNNDelete"):
        pattern = f"results/relative/{method}/cora/GCN/relative_seed*.json"
        for path in glob.glob(pattern):
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            config = payload.get("config", {})
            if config.get("unlearn_ratio") != 0.05:
                continue
            seed = int(config.get("random_seed"))
            results = payload.get("results", [])
            if results:
                baseline_f1_map[(method, seed)] = results[0].get("baseline_f1_after")

    records = []
    kept_methods = {"GIF", "GNNDelete"}
    kept_strategies = {"random", "tracin", "im_v4", "hybrid_v4"}

    for summary_path in sorted(glob.glob(RATIO_SUMMARY_GLOB)):
        with open(summary_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        seed = int(payload.get("random_seed"))
        result_groups = payload.get("results", {})
        for experiment_key, experiment_payload in result_groups.items():
            config = experiment_payload.get("config", {})
            method = config.get("unlearning_methods")
            dataset = config.get("dataset_name")
            model = config.get("base_model")
            ratio = config.get("unlearn_ratio")
            if method not in kept_methods or dataset != "cora" or model != "GCN":
                continue
            baseline_f1 = baseline_f1_map.get((method, seed))
            if baseline_f1 is None:
                continue

            strategy_results = experiment_payload.get("results", {})
            for strategy in kept_strategies:
                result = strategy_results.get(strategy)
                if not result:
                    continue
                f1_after = result.get("f1_after")
                if f1_after is None:
                    continue
                records.append(
                    {
                        "Method": method,
                        "Dataset": dataset,
                        "Model": model,
                        "Ratio": float(ratio),
                        "Strategy": strategy,
                        "StrategyLabel": FIG2_STRATEGY_LABELS[strategy],
                        "Seed": int(seed),
                        # Relative F1 drop uses the frozen k=5 random baseline F1_after.
                        "Relative_F1_Drop": (baseline_f1 - f1_after) * 100.0,
                    }
                )

    df = pd.DataFrame.from_records(records)
    if df.empty:
        raise ValueError("No ratio-sensitivity records found for FIG-2.")
    return df.sort_values(["Method", "Ratio", "Strategy", "Seed"]).reset_index(drop=True)


def collect_fig4_pairs() -> Dict[str, Dict[str, List[Tuple[float, float]]]]:
    paired_data: Dict[str, Dict[str, List[Tuple[float, float]]]] = {}
    raw_strategies = list(CORE_STRATEGY_LABELS.keys())

    for method, pattern in FIG4_JSON_PATTERNS.items():
        files = sorted(glob.glob(pattern))
        if not files:
            continue
        paired_data[method] = {strategy: [] for strategy in raw_strategies}
        for path in files:
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            results = payload.get("results", {})
            random_drop = results.get("random", {}).get("f1_drop")
            if random_drop is None:
                continue
            for strategy in raw_strategies:
                strategy_drop = results.get(strategy, {}).get("f1_drop")
                if strategy_drop is not None:
                    paired_data[method][strategy].append((strategy_drop, random_drop))

    return paired_data


def build_fig4a_logp_matrix() -> pd.DataFrame:
    paired_data = collect_fig4_pairs()
    p_matrix = pd.DataFrame(index=FIG4_METHOD_ORDER, columns=FIG_ATTACK_STRATEGIES, dtype=float)

    for method in FIG4_METHOD_ORDER:
        for raw_strategy, label in CORE_STRATEGY_LABELS.items():
            pairs = paired_data.get(method, {}).get(raw_strategy, [])
            if len(pairs) < 2:
                continue
            strategy_vals = np.array([item[0] for item in pairs], dtype=float)
            random_vals = np.array([item[1] for item in pairs], dtype=float)
            diffs = strategy_vals - random_vals
            if np.std(diffs, ddof=1) == 0:
                p_val = 0.0 if np.mean(diffs) > 0 else 1.0
            else:
                p_val = ttest_rel(strategy_vals, random_vals, alternative="greater").pvalue
            p_matrix.loc[method, label] = -np.log10(max(p_val, 1e-10))

    return p_matrix


def build_fig4b_effect_matrix() -> pd.DataFrame:
    paired_data = collect_fig4_pairs()
    effect_matrix = pd.DataFrame(index=FIG4_METHOD_ORDER, columns=FIG_ATTACK_STRATEGIES, dtype=float)

    for method in FIG4_METHOD_ORDER:
        for raw_strategy, label in CORE_STRATEGY_LABELS.items():
            pairs = paired_data.get(method, {}).get(raw_strategy, [])
            if not pairs:
                continue
            deltas = [(strategy_val - random_val) * 100.0 for strategy_val, random_val in pairs]
            effect_matrix.loc[method, label] = float(np.mean(deltas))

    return effect_matrix



def plot_fig1() -> None:
    df = load_final_stats()
    methods = ["GIF", "GNNDelete", "GraphEraser"]
    strategies = ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"]

    df_f1 = df[(df["Method"].isin(methods)) & (df["Ratio"] == 0.05) & (df["Strategy"].isin(strategies))].copy()
    df_f1["Setting"] = df_f1["Dataset"] + "-" + df_f1["Model"]
    settings = ["cora-GCN", "citeseer-GCN", "cora-GAT"]
    df_f1 = df_f1[df_f1["Setting"].isin(settings)]

    grid = sns.catplot(
        data=df_f1,
        kind="bar",
        x="Setting",
        y="Rel_F1_Drop_Mean",
        hue="Strategy",
        col="Method",
        errorbar=None,
        palette="viridis",
        height=4.8,
        aspect=1.0,
        hue_order=strategies,
    )
    grid.set_axis_labels("Dataset-Model", "Relative F1 Drop (%)")
    grid.set_titles("{col_name}")
    grid.fig.suptitle(
        "FIG-1: Generalization Potency (Relative F1 Drop vs. Random k=5 Baseline)",
        y=1.05,
    )
    save_figure(grid.fig, "FIG-1_Generalization")
    plt.close(grid.fig)
    print("FIG-1 generated.")


def plot_fig2() -> None:
    df = build_fig2_ratio_dataframe()
    palette = {
        "random": "#9aa0a6",
        "TracIn": "#1f77b4",
        "IM": "#ff7f0e",
        "Hybrid": "#d62728",
    }

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), sharey=False)
    for ax, method in zip(axes, ["GIF", "GNNDelete"]):
        subset = df[df["Method"] == method].copy()
        order = [("random", "random"), ("tracin", "TracIn"), ("im_v4", "IM"), ("hybrid_v4", "Hybrid")]
        for strategy, label in order:
            strat_subset = subset[subset["Strategy"] == strategy]
            grouped = (
                strat_subset.groupby("Ratio")["Relative_F1_Drop"]
                .agg(["mean", "std"])
                .reset_index()
                .sort_values("Ratio")
            )
            linestyle = "--" if strategy == "random" else "-"
            linewidth = 1.8 if strategy == "random" else 2.4
            alpha = 0.8 if strategy == "random" else 0.95
            marker = "o" if strategy == "random" else {"tracin": "s", "im_v4": "X", "hybrid_v4": "o"}[strategy]
            ax.plot(
                grouped["Ratio"],
                grouped["mean"],
                label=label,
                color=palette[label],
                linestyle=linestyle,
                linewidth=linewidth,
                marker=marker,
                markersize=7,
                alpha=alpha,
            )
        ax.set_title(f"{method} (Cora-GCN)")
        ax.set_xlabel("Unlearning Ratio")
        ax.set_ylabel("Relative F1 Drop (%)")
        ax.set_xticks([0.01, 0.05, 0.10, 0.20])
        ax.grid(True, linestyle="--", alpha=0.5)
        if ax.legend_:
            ax.legend_.remove()

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title="Strategy", loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.suptitle("FIG-2: Supplementary Ratio Sensitivity (Relative F1 Drop)", y=1.03)
    fig.tight_layout(rect=[0, 0, 0.9, 1])
    save_figure(fig, "FIG-2_Scaling")
    plt.close(fig)
    print("FIG-2 generated.")


def plot_fig3() -> None:
    df = load_final_stats()
    methods_gcn = ["GIF", "GNNDelete", "GraphEraser"]
    methods_gat = ["IDEA", "MEGU"]

    df_gcn = df[
        (df["Dataset"] == "cora")
        & (df["Model"] == "GCN")
        & (df["Ratio"] == 0.05)
        & (df["Method"].isin(methods_gcn))
    ].copy()
    df_gat = df[
        (df["Dataset"] == "cora")
        & (df["Model"] == "GAT")
        & (df["Ratio"] == 0.05)
        & (df["Method"].isin(methods_gat))
    ].copy()
    df_f3 = pd.concat([df_gcn, df_gat], ignore_index=True)

    pivot_mean = df_f3.pivot_table(index="Method", columns="Strategy", values="Rel_F1_Drop_Mean")
    pivot_std = df_f3.pivot_table(index="Method", columns="Strategy", values="Rel_F1_Drop_Std")

    for col in CORE_STRATEGY_LABELS:
        if col not in pivot_mean.columns:
            pivot_mean[col] = 0.0
            pivot_std[col] = 0.0

    pivot_mean = pivot_mean.reindex(FIG4_METHOD_ORDER)
    pivot_std = pivot_std.reindex(FIG4_METHOD_ORDER)

    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    x = np.arange(len(pivot_mean.index))
    width = 0.24
    bars = []
    color_map = {"tracin": "#1f77b4", "im_v4": "#ff7f0e", "hybrid_v4": "#d62728"}
    for offset, strategy in zip([-width, 0, width], ["tracin", "im_v4", "hybrid_v4"]):
        bar = ax.bar(
            x + offset,
            pivot_mean[strategy],
            width,
            yerr=pivot_std[strategy],
            capsize=4,
            label=CORE_STRATEGY_LABELS[strategy],
            color=color_map[strategy],
            edgecolor="black",
        )
        bars.append(bar)

    for bar_group in bars:
        ax.bar_label(bar_group, fmt="%.1f", padding=3, fontsize=9)

    ax.set_title(
        "FIG-3: Universal Vulnerability Spectrum (Ratio=0.05)\n"
        "GIF, GNNDelete, GraphEraser: Cora-GCN | IDEA, MEGU: Cora-GAT"
    )
    ax.set_xlabel("Unlearning Method", fontweight="bold")
    ax.set_ylabel("Relative F1 Drop (%)", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(pivot_mean.index)
    ax.legend(loc="upper right")
    ax.set_ylim(0, max((pivot_mean.max().max() + pivot_std.max().max()) * 1.2, 5))

    fig.tight_layout()
    save_figure(fig, "FIG-3_Spectrum")
    plt.close(fig)
    print("FIG-3 generated.")


def create_fig4a_figure():
    plot_df = build_fig4a_logp_matrix()
    threshold_main = -np.log10(0.10)
    threshold_strong = -np.log10(0.05)

    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    sns.heatmap(
        plot_df,
        annot=True,
        cmap="YlOrRd",
        fmt=".2f",
        cbar_kws={"label": "$-\\log_{10}(p)$"},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )

    for row_idx in range(plot_df.shape[0]):
        for col_idx in range(plot_df.shape[1]):
            value = plot_df.iloc[row_idx, col_idx]
            if np.isnan(value):
                continue
            if value < threshold_main:
                ax.add_patch(
                    plt.Rectangle(
                        (col_idx, row_idx),
                        1,
                        1,
                        fill=False,
                        edgecolor="gray",
                        linewidth=2,
                        hatch="///",
                        zorder=3,
                    )
                )
            elif value < threshold_strong:
                ax.add_patch(
                    plt.Rectangle(
                        (col_idx, row_idx),
                        1,
                        1,
                        fill=False,
                        edgecolor="#f28e2b",
                        linewidth=2.5,
                        linestyle="--",
                        zorder=3,
                    )
                )
            else:
                ax.add_patch(
                    plt.Rectangle(
                        (col_idx, row_idx),
                        1,
                        1,
                        fill=False,
                        edgecolor="#4e79a7",
                        linewidth=2.5,
                        zorder=3,
                    )
                )

    cbar = ax.collections[0].colorbar
    cbar.ax.axhline(y=threshold_main, color="black", linewidth=2, linestyle="--")
    cbar.ax.axhline(y=threshold_strong, color="#4e79a7", linewidth=2, linestyle="-")

    ax.set_title(
        "FIG-4a: Support Against Random Deletion ($-\\log_{10}(p)$)"
    )
    ax.set_ylabel("Unlearning Method")
    ax.set_xlabel("Attack Strategy")

    legend_handles = [
        Line2D([0], [0], color="#4e79a7", linewidth=2.5, label="p < 0.05"),
        Line2D([0], [0], color="#f28e2b", linewidth=2.5, linestyle="--", label="0.05 <= p < 0.10"),
        Patch(facecolor="white", edgecolor="gray", hatch="///", label="p >= 0.10"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=3,
        frameon=False,
        fontsize=9,
    )

    return fig, ax, cbar


def plot_fig4a() -> None:
    fig, _, _ = create_fig4a_figure()

    fig.tight_layout()
    save_figure(fig, "FIG-4a_Significance")
    plt.close(fig)
    print("FIG-4a generated.")


def plot_fig4b() -> None:
    effect_df = build_fig4b_effect_matrix()
    vmax = float(np.nanmax(np.abs(effect_df.to_numpy(dtype=float))))
    label_df = effect_df.applymap(lambda value: "" if pd.isna(value) else f"{value:+.1f}")

    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    sns.heatmap(
        effect_df,
        annot=label_df,
        fmt="",
        cmap="coolwarm",
        center=0,
        vmin=-vmax,
        vmax=vmax,
        cbar_kws={"label": "Mean extra drop vs random (percentage points)"},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    ax.set_title(
        "FIG-4b: Effect Size Against Random Deletion\n"
        "Cell values show mean extra relative F1 drop vs random"
    )
    ax.set_ylabel("Unlearning Method")
    ax.set_xlabel("Attack Strategy")

    fig.tight_layout()
    save_figure(fig, "FIG-4b_Effect")
    plt.close(fig)
    print("FIG-4b generated.")


def remove_demoted_fig4_outputs() -> None:
    for out_dir in (RESULTS_FIG_DIR, REPORT_FIG_DIR, OVERLEAF_FIG_DIR):
        for suffix in ("pdf", "png"):
            path = out_dir / f"FIG-4_Significance.{suffix}"
            if path.exists():
                path.unlink()


def remove_demoted_fig5_outputs() -> None:
    for out_dir in (RESULTS_FIG_DIR, REPORT_FIG_DIR, OVERLEAF_FIG_DIR):
        for suffix in ("pdf", "png"):
            path = out_dir / f"FIG-5_Collateral.{suffix}"
            if path.exists():
                path.unlink()


if __name__ == "__main__":
    print("Generating refreshed paper figures...")
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4a()
    plot_fig4b()
    remove_demoted_fig4_outputs()
    remove_demoted_fig5_outputs()
    print("All done. Figures saved to results/paper_figures, report/paper/figures, and the Overleaf bundle.")
