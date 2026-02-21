"""Plot and report utilities for Step0 evaluation outputs."""

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Dict, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT_JSON = REPO_ROOT / "results" / "step0_validation" / "round2_results.json"
DEFAULT_PLOT_DIR = REPO_ROOT / "results" / "evaluation" / "step0" / "plots"
DEFAULT_COMPAT_JSON = REPO_ROOT / "results" / "evaluation" / "step0" / "method_compatibility.json"
DEFAULT_REPORT_MD = REPO_ROOT / "results" / "evaluation" / "step0" / "round2_detail.md"

RATIO_NODES = {"0.005": 13, "0.02": 54, "0.05": 135, "0.1": 270, "0.2": 541}

METHOD_CATEGORIES = {
    "Shard-based": ["GraphEraser", "GUIDE", "GraphRevoker"],
    "IF-based": ["GIF", "IDEA"],
    "Learning-based": ["GNNDelete", "SGU", "MEGU", "GUKD", "D2DGN"],
    "Standalone": ["Projector"],
}

CATEGORY_COLORS = {
    "Shard-based": "#e74c3c",
    "IF-based": "#3498db",
    "Learning-based": "#2ecc71",
    "Standalone": "#f39c12",
}

METHOD_COLORS = {
    "GraphEraser": "#e74c3c",
    "GUIDE": "#c0392b",
    "GraphRevoker": "#e67e22",
    "GIF": "#3498db",
    "IDEA": "#2980b9",
    "GNNDelete": "#2ecc71",
    "SGU": "#27ae60",
    "MEGU": "#1abc9c",
    "GUKD": "#9b59b6",
    "D2DGN": "#8e44ad",
    "Projector": "#f39c12",
}


def get_category(method: str) -> str:
    for category, methods in METHOD_CATEGORIES.items():
        if method in methods:
            return category
    return "Other"


def load_round2(input_json: Path):
    with input_json.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def get_method_data(results: dict, method: str):
    data = []
    for ratio_str, info in results.get(method, {}).items():
        if info.get("status") in ("OK", "SKIP") and info.get("f1_after") is not None:
            ratio = float(ratio_str)
            nodes = RATIO_NODES.get(ratio_str, int(ratio * 2708))
            data.append((ratio, nodes, info["f1_after"], info.get("unlearn_time")))
    data.sort(key=lambda item: item[0])
    return data


def _get_plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def _get_np():
    import numpy as np

    return np


def _save_plot(path: Path, plt) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_per_method(results: dict, out_dir: Path) -> None:
    plt = _get_plt()
    for method in results:
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        ratios = [item[0] for item in data]
        nodes = [item[1] for item in data]
        f1s = [item[2] for item in data]

        category = get_category(method)
        color = METHOD_COLORS.get(method, "#95a5a6")

        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(nodes, f1s, "o-", color=color, linewidth=2.5, markersize=10, zorder=3)
        ax.fill_between(nodes, f1s, alpha=0.08, color=color)

        for x, y, ratio in zip(nodes, f1s, ratios):
            ax.annotate(
                f"{y:.4f}\n(r={ratio})",
                (x, y),
                textcoords="offset points",
                xytext=(0, 14),
                ha="center",
                fontsize=9,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

        drop = f1s[0] - f1s[-1]
        color_label = "red" if drop > 0.02 else "green"
        ax.annotate(
            f"Total F1 drop: {drop:.4f} ({drop / f1s[0] * 100:.1f}%)",
            xy=(0.98, 0.02),
            xycoords="axes fraction",
            ha="right",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=color_label,
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9),
        )

        ax.set_xlabel("Approx. Number of Unlearned Nodes", fontsize=12)
        ax.set_ylabel("F1 Score After Unlearning", fontsize=12)
        ax.set_title(f"{method} ({category})\nF1 vs. Unlearn Ratio - GCN x Cora", fontsize=14, fontweight="bold")
        ax.set_ylim(min(f1s) - 0.03, max(f1s) + 0.04)
        ax.grid(True, alpha=0.3)

        _save_plot(out_dir / f"{method}_f1_curve.png", plt)


def plot_combined(results: dict, out_dir: Path) -> None:
    plt = _get_plt()
    fig, ax = plt.subplots(figsize=(14, 8))
    markers = ["o", "s", "^", "D", "v", "<", ">", "p", "*", "h", "X"]

    for idx, method in enumerate(sorted(results.keys())):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        nodes = [item[1] for item in data]
        f1s = [item[2] for item in data]
        color = METHOD_COLORS.get(method, "#95a5a6")
        marker = markers[idx % len(markers)]
        category = get_category(method)

        ax.plot(nodes, f1s, f"{marker}-", color=color, linewidth=2, markersize=8, label=f"{method} ({category})", alpha=0.9)

    ax.set_xlabel("Approx. Number of Unlearned Nodes", fontsize=13)
    ax.set_ylabel("F1 Score After Unlearning", fontsize=13)
    ax.set_title("All GU Methods: F1 vs. Unlearn Size\n(GCN x Cora, 100 epochs)", fontsize=14, fontweight="bold")
    ax.set_ylim(0.7, 0.95)
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=10, framealpha=0.95)
    _save_plot(out_dir / "all_methods_combined.png", plt)


def plot_f1_drop_bar(results: dict, out_dir: Path) -> None:
    plt = _get_plt()
    np = _get_np()
    methods = []
    drops = []
    colors = []

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue
        drop = data[0][2] - data[-1][2]
        methods.append(method)
        drops.append(drop)
        colors.append(METHOD_COLORS.get(method, "#95a5a6"))

    sorted_idx = np.argsort(drops)[::-1]
    methods = [methods[idx] for idx in sorted_idx]
    drops = [drops[idx] for idx in sorted_idx]
    colors = [colors[idx] for idx in sorted_idx]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(methods)), drops, color=colors, alpha=0.85, edgecolor="white")

    for bar, drop, method in zip(bars, drops, methods):
        category = get_category(method)
        label = f"{drop:.4f} ({drop * 100:.1f}%)"
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height() / 2, f"  {label}  [{category}]", va="center", fontsize=10)

    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, fontsize=11)
    ax.set_xlabel("F1 Drop (ratio=0.005 -> ratio=0.2)", fontsize=12)
    ax.set_title("Vulnerability Ranking: F1 Drop Under Increasing Unlearning", fontsize=13, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="x")
    ax.invert_yaxis()

    _save_plot(out_dir / "vulnerability_ranking.png", plt)


def plot_time_vs_ratio(results: dict, out_dir: Path) -> None:
    plt = _get_plt()
    fig, ax = plt.subplots(figsize=(12, 7))
    markers = ["o", "s", "^", "D", "v", "<", ">", "p", "*", "h", "X"]

    for idx, method in enumerate(sorted(results.keys())):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        nodes = [item[1] for item in data]
        times = [item[3] for item in data if item[3] is not None]
        if len(times) != len(nodes):
            continue

        color = METHOD_COLORS.get(method, "#95a5a6")
        marker = markers[idx % len(markers)]
        ax.plot(nodes, times, f"{marker}-", color=color, linewidth=1.5, markersize=7, label=method, alpha=0.85)

    ax.set_xlabel("Approx. Number of Unlearned Nodes", fontsize=12)
    ax.set_ylabel("Unlearning Time (seconds)", fontsize=12)
    ax.set_title("Unlearning Time vs. Unlearn Size\n(GCN x Cora)", fontsize=13, fontweight="bold")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=10)

    _save_plot(out_dir / "time_vs_ratio.png", plt)


def plot_round1_bar(out_dir: Path) -> None:
    plt = _get_plt()
    np = _get_np()
    round1_data = {
        "GraphEraser": (0.8432, "OK"),
        "GIF": (0.8708, "OK"),
        "GUIDE": (0.8303, "OK"),
        "GST": (0, "FAIL"),
        "GNNDelete": (0.8229, "OK"),
        "CEU": (0, "FAIL"),
        "CGU": (0, "FAIL"),
        "SGU": (0.8838, "OK"),
        "MEGU": (0.8745, "OK"),
        "UTU": (0, "FAIL"),
        "GUKD": (0.9022, "OK"),
        "D2DGN": (0.9004, "OK"),
        "IDEA": (0.8561, "OK"),
        "Projector": (0.8395, "OK"),
        "GraphRevoker": (0.8432, "OK"),
    }

    methods = list(round1_data.keys())
    f1s = [round1_data[method][0] for method in methods]
    statuses = [round1_data[method][1] for method in methods]

    colors = []
    for method, status in zip(methods, statuses):
        if status == "FAIL":
            colors.append("#e74c3c")
        else:
            colors.append(METHOD_COLORS.get(method, "#95a5a6"))

    sorted_idx = np.argsort(f1s)[::-1]
    methods = [methods[idx] for idx in sorted_idx]
    f1s = [f1s[idx] for idx in sorted_idx]
    statuses = [statuses[idx] for idx in sorted_idx]
    colors = [colors[idx] for idx in sorted_idx]

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(range(len(methods)), f1s, color=colors, alpha=0.85, edgecolor="white")

    for bar, f1_value, status in zip(bars, f1s, statuses):
        if status == "FAIL":
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                0.02,
                "FAIL",
                ha="center",
                va="bottom",
                fontsize=9,
                color="white",
                fontweight="bold",
                bbox=dict(boxstyle="round", facecolor="red", alpha=0.8),
            )
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005, f"{f1_value:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=45, ha="right", fontsize=10)
    ax.set_ylabel("F1 Score After Unlearning", fontsize=12)
    ax.set_title("Round 1 Overview: All 15 GU Methods (GCN x Cora x 270 nodes)\n11 Passed / 4 Failed", fontsize=13, fontweight="bold")
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis="y")

    _save_plot(out_dir / "round1_overview.png", plt)


def plot_category_comparison(results: dict, out_dir: Path) -> None:
    plt = _get_plt()
    np = _get_np()
    category_drops = {}
    for category, methods in METHOD_CATEGORIES.items():
        drops = []
        for method in methods:
            data = get_method_data(results, method)
            if len(data) >= 2:
                drops.append(data[0][2] - data[-1][2])
        if drops:
            category_drops[category] = {"mean": np.mean(drops), "std": np.std(drops)}

    fig, ax = plt.subplots(figsize=(8, 5))
    categories = list(category_drops.keys())
    means = [category_drops[cat]["mean"] for cat in categories]
    stds = [category_drops[cat]["std"] for cat in categories]
    colors = [CATEGORY_COLORS[cat] for cat in categories]

    bars = ax.bar(categories, means, yerr=stds, color=colors, alpha=0.85, capsize=8, edgecolor="white")
    for bar, mean, std in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + std + 0.002, f"{mean:.4f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_ylabel("Average F1 Drop", fontsize=12)
    ax.set_title("Average Vulnerability by Method Category", fontsize=13, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")

    _save_plot(out_dir / "category_comparison.png", plt)


def generate_compatibility_json(results: dict, out_path: Path) -> dict:
    compat = {}

    for method, configs in results.items():
        entry = {
            "status": "OK",
            "compatible_models": ["GCN"],
            "compatible_datasets": ["cora"],
            "max_unlearn_ratio_tested": 0,
            "known_issues": [],
            "notes": "",
            "f1_by_ratio": {},
            "time_by_ratio": {},
        }

        max_ratio = 0.0
        for ratio_str, data in configs.items():
            if data.get("status") in ("OK", "SKIP"):
                ratio = float(ratio_str)
                max_ratio = max(max_ratio, ratio)
                entry["f1_by_ratio"][ratio_str] = data.get("f1_after")
                entry["time_by_ratio"][ratio_str] = data.get("unlearn_time")
            elif data.get("status") in ("X", "TIMEOUT"):
                entry["known_issues"].append(f"ratio={ratio_str}: {data.get('error_msg', 'failed')}")

        entry["max_unlearn_ratio_tested"] = max_ratio
        f1_values = [val for val in entry["f1_by_ratio"].values() if val is not None]
        if len(f1_values) >= 2:
            drop = max(f1_values) - min(f1_values)
            if drop > 0.05:
                entry["notes"] = f"Significant F1 sensitivity (drop={drop:.4f})"
            elif drop > 0.01:
                entry["notes"] = f"Moderate F1 sensitivity (drop={drop:.4f})"
            else:
                entry["notes"] = f"Stable across ratios (drop={drop:.4f})"

        compat[method] = entry

    for method, err in [
        ("GST", "forward() got unexpected keyword argument 'use_batch'"),
        ("CEU", "'dict' has no attribute 'num_features'"),
        ("CGU", "Only supports SGC backbone"),
        ("UTU", "UTUTrainer not registered"),
    ]:
        compat[method] = {
            "status": "FAIL",
            "compatible_models": [] if method != "CGU" else ["SGC"],
            "compatible_datasets": [],
            "max_unlearn_ratio_tested": 0,
            "known_issues": [err],
            "notes": "Failed in Round 1",
        }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as file_obj:
        json.dump(compat, file_obj, indent=2, ensure_ascii=False)
    return compat


def generate_round2_detail_md(results: dict, compat: dict, out_path: Path, plot_rel_dir: str = "plots") -> Path:
    del compat
    today = date.today().isoformat()
    lines = [
        "# Round 2: Deep Validation Results\n",
        f"**Date**: {today}",
        "**Config**: GCN x Cora x 5 unlearn ratios x 100 epochs x 1 run\n",
        "## F1 Score by Method and Unlearn Ratio\n",
        "| Method | Category | r=0.005 (~13n) | r=0.02 (~54n) | r=0.05 (~135n) | r=0.1 (~270n) | r=0.2 (~541n) | F1 Drop |",
        "|--------|----------|----------------|---------------|----------------|---------------|---------------|---------|",
    ]

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        category = get_category(method)
        f1_map = {item[0]: item[2] for item in data}

        row = f"| {method} | {category} |"
        for ratio in [0.005, 0.02, 0.05, 0.1, 0.2]:
            f1 = f1_map.get(ratio)
            row += f" {f1:.4f} |" if f1 is not None else " SKIP |"

        if len(data) >= 2:
            drop = data[0][2] - data[-1][2]
            row += f" {drop:.4f} |"
        else:
            row += " - |"
        lines.append(row)

    lines.extend(
        [
            "\n## Unlearning Time by Method and Unlearn Ratio\n",
            "| Method | r=0.005 | r=0.02 | r=0.05 | r=0.1 | r=0.2 |",
            "|--------|---------|--------|--------|-------|-------|",
        ]
    )

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        t_map = {item[0]: item[3] for item in data}
        row = f"| {method} |"
        for ratio in [0.005, 0.02, 0.05, 0.1, 0.2]:
            value = t_map.get(ratio)
            row += f" {value:.2f}s |" if value is not None else " - |"
        lines.append(row)

    lines.extend(
        [
            "\n## Plots\n",
            f"See `{plot_rel_dir}/` directory for generated figures.",
        ]
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def run_step0_plotting(results: dict, plot_dir: Path, compat_json: Path, report_md: Path) -> Tuple[Path, Path]:
    plot_dir.mkdir(parents=True, exist_ok=True)

    plot_round1_bar(plot_dir)
    plot_per_method(results, plot_dir)
    plot_combined(results, plot_dir)
    plot_f1_drop_bar(results, plot_dir)
    plot_time_vs_ratio(results, plot_dir)
    plot_category_comparison(results, plot_dir)

    compat = generate_compatibility_json(results, compat_json)
    generate_round2_detail_md(results, compat, report_md, plot_rel_dir=plot_dir.name)
    return compat_json, report_md


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Step0 plots and reports")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT_JSON)
    parser.add_argument("--plot-dir", type=Path, default=DEFAULT_PLOT_DIR)
    parser.add_argument("--compat-json", type=Path, default=DEFAULT_COMPAT_JSON)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    results = load_round2(args.input_json)
    compat_json, report_md = run_step0_plotting(results, args.plot_dir, args.compat_json, args.report_md)
    print(f"Plots saved to: {args.plot_dir}")
    print(f"Compatibility JSON saved to: {compat_json}")
    print(f"Report saved to: {report_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
