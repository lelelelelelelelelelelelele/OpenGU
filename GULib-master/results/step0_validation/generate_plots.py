"""
Generate visualization plots for Step 0 validation results.
"""
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
PLOT_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# Ratio -> approx node count for axis labels
RATIO_NODES = {"0.005": 13, "0.02": 54, "0.05": 135, "0.1": 270, "0.2": 541}

METHOD_CATEGORIES = {
    "Shard-based": ["GraphEraser", "GUIDE", "GraphRevoker"],
    "IF-based": ["GIF", "IDEA"],
    "Learning-based": ["GNNDelete", "SGU", "MEGU", "GUKD", "D2DGN", "Projector"],
}

CATEGORY_COLORS = {
    "Shard-based": "#e74c3c",
    "IF-based": "#3498db",
    "Learning-based": "#2ecc71",
}

METHOD_COLORS = {
    "GraphEraser": "#e74c3c", "GUIDE": "#c0392b", "GraphRevoker": "#e67e22",
    "GIF": "#3498db", "IDEA": "#2980b9",
    "GNNDelete": "#2ecc71", "SGU": "#27ae60", "MEGU": "#1abc9c",
    "GUKD": "#9b59b6", "D2DGN": "#8e44ad", "Projector": "#f39c12",
}

def get_category(method):
    for cat, methods in METHOD_CATEGORIES.items():
        if method in methods:
            return cat
    return "Other"


def load_round2():
    path = os.path.join(RESULTS_DIR, "round2_results.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_method_data(results, method):
    """Extract sorted (ratio, approx_nodes, f1) tuples for a method."""
    data = []
    for ratio_str, info in results.get(method, {}).items():
        if info.get("status") == "OK" and info.get("f1_after") is not None:
            r = float(ratio_str)
            n = RATIO_NODES.get(ratio_str, int(r * 2708))
            data.append((r, n, info["f1_after"], info.get("unlearn_time")))
    data.sort(key=lambda x: x[0])
    return data


def plot_per_method(results):
    """One plot per method: F1 vs unlearn ratio/nodes."""
    for method in results:
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        ratios = [d[0] for d in data]
        nodes = [d[1] for d in data]
        f1s = [d[2] for d in data]

        cat = get_category(method)
        color = METHOD_COLORS.get(method, "#95a5a6")

        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(nodes, f1s, 'o-', color=color, linewidth=2.5, markersize=10, zorder=3)
        ax.fill_between(nodes, f1s, alpha=0.08, color=color)

        for x, y, r in zip(nodes, f1s, ratios):
            ax.annotate(f'{y:.4f}\n(r={r})', (x, y), textcoords="offset points",
                       xytext=(0, 14), ha='center', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        # F1 drop annotation
        if len(f1s) >= 2:
            drop = f1s[0] - f1s[-1]
            ax.annotate(f'Total F1 drop: {drop:.4f} ({drop/f1s[0]*100:.1f}%)',
                       xy=(0.98, 0.02), xycoords='axes fraction', ha='right', va='bottom',
                       fontsize=11, fontweight='bold', color='red' if drop > 0.02 else 'green',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

        ax.set_xlabel('Approx. Number of Unlearned Nodes', fontsize=12)
        ax.set_ylabel('F1 Score After Unlearning', fontsize=12)
        ax.set_title(f'{method} ({cat})\nF1 vs. Unlearn Ratio - GCN x Cora', fontsize=14, fontweight='bold')
        ax.set_ylim(min(f1s) - 0.03, max(f1s) + 0.04)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f"{method}_f1_curve.png"), dpi=150)
        plt.close()
        print(f"  Saved {method}_f1_curve.png")


def plot_combined(results):
    """All methods on one chart."""
    fig, ax = plt.subplots(figsize=(14, 8))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'X']

    methods_sorted = sorted(results.keys())
    for i, method in enumerate(methods_sorted):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        nodes = [d[1] for d in data]
        f1s = [d[2] for d in data]
        color = METHOD_COLORS.get(method, "#95a5a6")
        marker = markers[i % len(markers)]
        cat = get_category(method)

        ax.plot(nodes, f1s, f'{marker}-', color=color, linewidth=2,
                markersize=8, label=f'{method} ({cat})', alpha=0.9)

    ax.set_xlabel('Approx. Number of Unlearned Nodes', fontsize=13)
    ax.set_ylabel('F1 Score After Unlearning', fontsize=13)
    ax.set_title('All GU Methods: F1 vs. Unlearn Size\n(GCN x Cora, 100 epochs)', fontsize=14, fontweight='bold')
    ax.set_ylim(0.7, 0.95)
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10, framealpha=0.95)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "all_methods_combined.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved all_methods_combined.png")


def plot_f1_drop_bar(results):
    """Bar chart showing F1 drop from smallest to largest unlearn ratio."""
    methods = []
    drops = []
    colors = []

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue
        f1_min_ratio = data[0][2]  # F1 at smallest ratio
        f1_max_ratio = data[-1][2]  # F1 at largest ratio
        drop = f1_min_ratio - f1_max_ratio
        methods.append(method)
        drops.append(drop)
        colors.append(METHOD_COLORS.get(method, "#95a5a6"))

    # Sort by drop descending
    sorted_idx = np.argsort(drops)[::-1]
    methods = [methods[i] for i in sorted_idx]
    drops = [drops[i] for i in sorted_idx]
    colors = [colors[i] for i in sorted_idx]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(methods)), drops, color=colors, alpha=0.85, edgecolor='white')

    for i, (bar, d, m) in enumerate(zip(bars, drops, methods)):
        cat = get_category(m)
        label = f'{d:.4f} ({d*100:.1f}%)'
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
               f'  {label}  [{cat}]', va='center', fontsize=10)

    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, fontsize=11)
    ax.set_xlabel('F1 Drop (ratio=0.005 -> ratio=0.2)', fontsize=12)
    ax.set_title('Vulnerability Ranking: F1 Drop Under Increasing Unlearning\n(Larger = More Vulnerable to Attack)',
                fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "vulnerability_ranking.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved vulnerability_ranking.png")


def plot_time_vs_ratio(results):
    """Unlearning time vs ratio for each method."""
    fig, ax = plt.subplots(figsize=(12, 7))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'X']

    for i, method in enumerate(sorted(results.keys())):
        data = get_method_data(results, method)
        if len(data) < 2:
            continue

        nodes = [d[1] for d in data]
        times = [d[3] for d in data if d[3] is not None]
        if len(times) != len(nodes):
            continue

        color = METHOD_COLORS.get(method, "#95a5a6")
        marker = markers[i % len(markers)]
        ax.plot(nodes, times, f'{marker}-', color=color, linewidth=1.5,
                markersize=7, label=method, alpha=0.85)

    ax.set_xlabel('Approx. Number of Unlearned Nodes', fontsize=12)
    ax.set_ylabel('Unlearning Time (seconds)', fontsize=12)
    ax.set_title('Unlearning Time vs. Unlearn Size\n(GCN x Cora)', fontsize=13, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "time_vs_ratio.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved time_vs_ratio.png")


def plot_round1_bar():
    """Round 1 bar chart: F1 at default ratio for all methods, including failed."""
    round1_data = {
        "GraphEraser": (0.8432, "OK"), "GIF": (0.8708, "OK"), "GUIDE": (0.8303, "OK"),
        "GST": (0, "FAIL"), "GNNDelete": (0.8229, "OK"), "CEU": (0, "FAIL"),
        "CGU": (0, "FAIL"), "SGU": (0.8838, "OK"), "MEGU": (0.8745, "OK"),
        "UTU": (0, "FAIL"), "GUKD": (0.9022, "OK"), "D2DGN": (0.9004, "OK"),
        "IDEA": (0.8561, "OK"), "Projector": (0.8395, "OK"), "GraphRevoker": (0.8432, "OK"),
    }

    methods = list(round1_data.keys())
    f1s = [round1_data[m][0] for m in methods]
    statuses = [round1_data[m][1] for m in methods]

    colors = []
    for m, s in zip(methods, statuses):
        if s == "FAIL":
            colors.append("#e74c3c")
        else:
            colors.append(METHOD_COLORS.get(m, "#95a5a6"))

    # Sort by F1 descending
    sorted_idx = np.argsort(f1s)[::-1]
    methods = [methods[i] for i in sorted_idx]
    f1s = [f1s[i] for i in sorted_idx]
    statuses = [statuses[i] for i in sorted_idx]
    colors = [colors[i] for i in sorted_idx]

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(range(len(methods)), f1s, color=colors, alpha=0.85, edgecolor='white')

    for i, (bar, f1, s) in enumerate(zip(bars, f1s, statuses)):
        if s == "FAIL":
            ax.text(bar.get_x() + bar.get_width()/2., 0.02, 'FAIL',
                   ha='center', va='bottom', fontsize=9, color='white', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='red', alpha=0.8))
        else:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
                   f'{f1:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('F1 Score After Unlearning', fontsize=12)
    ax.set_title('Round 1 Overview: All 15 GU Methods (GCN x Cora x 270 nodes)\n11 Passed / 4 Failed',
                fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "round1_overview.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved round1_overview.png")


def plot_category_comparison(results):
    """Group by method category, show average F1 drop per category."""
    cat_drops = {}
    for cat, methods in METHOD_CATEGORIES.items():
        drops = []
        for method in methods:
            data = get_method_data(results, method)
            if len(data) >= 2:
                drops.append(data[0][2] - data[-1][2])
        if drops:
            cat_drops[cat] = {"mean": np.mean(drops), "std": np.std(drops), "n": len(drops)}

    fig, ax = plt.subplots(figsize=(8, 5))
    cats = list(cat_drops.keys())
    means = [cat_drops[c]["mean"] for c in cats]
    stds = [cat_drops[c]["std"] for c in cats]
    colors = [CATEGORY_COLORS[c] for c in cats]

    bars = ax.bar(cats, means, yerr=stds, color=colors, alpha=0.85, capsize=8, edgecolor='white')
    for bar, m, s in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + s + 0.002,
               f'{m:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Average F1 Drop', fontsize=12)
    ax.set_title('Average Vulnerability by Method Category\n(F1 drop from ratio=0.005 to max ratio)',
                fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, "category_comparison.png"), dpi=150)
    plt.close()
    print("  Saved category_comparison.png")


def generate_compatibility_json(results):
    """Generate method_compatibility.json."""
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

        max_ratio = 0
        for ratio_str, data in configs.items():
            if data.get("status") == "OK":
                r = float(ratio_str)
                if r > max_ratio:
                    max_ratio = r
                entry["f1_by_ratio"][ratio_str] = data.get("f1_after")
                entry["time_by_ratio"][ratio_str] = data.get("unlearn_time")
            elif data.get("status") in ("X", "TIMEOUT"):
                entry["known_issues"].append(f"ratio={ratio_str}: {data.get('error_msg', 'failed')}")

        entry["max_unlearn_ratio_tested"] = max_ratio

        f1_vals = [v for v in entry["f1_by_ratio"].values() if v is not None]
        if len(f1_vals) >= 2:
            drop = max(f1_vals) - min(f1_vals)
            if drop > 0.05:
                entry["notes"] = f"Significant F1 sensitivity (drop={drop:.4f})"
            elif drop > 0.01:
                entry["notes"] = f"Moderate F1 sensitivity (drop={drop:.4f})"
            else:
                entry["notes"] = f"Stable across ratios (drop={drop:.4f})"

        compat[method] = entry

    # Add failed methods from Round 1
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

    out_path = os.path.join(RESULTS_DIR, "method_compatibility.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(compat, f, indent=2, ensure_ascii=False)
    print(f"  Saved method_compatibility.json")
    return compat


def generate_round2_detail_md(results, compat):
    """Generate round2_detail.md summary."""
    lines = [
        "# Round 2: Deep Validation Results\n",
        f"**Date**: 2026-02-16",
        f"**Config**: GCN x Cora x 5 unlearn ratios x 100 epochs x 1 run\n",
        "## F1 Score by Method and Unlearn Ratio\n",
        "| Method | Category | r=0.005 (~13n) | r=0.02 (~54n) | r=0.05 (~135n) | r=0.1 (~270n) | r=0.2 (~541n) | F1 Drop |",
        "|--------|----------|----------------|---------------|----------------|---------------|---------------|---------|",
    ]

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        cat = get_category(method)
        f1_map = {d[0]: d[2] for d in data}

        row = f"| {method} | {cat} |"
        for r in [0.005, 0.02, 0.05, 0.1, 0.2]:
            f1 = f1_map.get(r)
            row += f" {f1:.4f} |" if f1 is not None else " SKIP |"

        if len(data) >= 2:
            drop = data[0][2] - data[-1][2]
            row += f" {drop:.4f} |"
        else:
            row += " - |"
        lines.append(row)

    lines.extend([
        "\n## Unlearning Time by Method and Unlearn Ratio\n",
        "| Method | r=0.005 | r=0.02 | r=0.05 | r=0.1 | r=0.2 |",
        "|--------|---------|--------|--------|-------|-------|",
    ])

    for method in sorted(results.keys()):
        data = get_method_data(results, method)
        t_map = {d[0]: d[3] for d in data}
        row = f"| {method} |"
        for r in [0.005, 0.02, 0.05, 0.1, 0.2]:
            t = t_map.get(r)
            row += f" {t:.2f}s |" if t is not None else " - |"
        lines.append(row)

    lines.extend([
        "\n## Key Findings\n",
        "### Most Vulnerable Methods (highest F1 drop):",
    ])

    # Rank by drop
    method_drops = []
    for method in results:
        data = get_method_data(results, method)
        if len(data) >= 2:
            method_drops.append((method, data[0][2] - data[-1][2]))
    method_drops.sort(key=lambda x: x[1], reverse=True)

    for i, (m, d) in enumerate(method_drops):
        lines.append(f"{i+1}. **{m}**: F1 drop = {d:.4f} ({d*100:.1f}%)")

    lines.extend([
        "\n### Most Robust Methods (lowest F1 drop):",
    ])
    for m, d in reversed(method_drops[-3:]):
        lines.append(f"- **{m}**: F1 drop = {d:.4f}")

    lines.extend([
        "\n### GUIDE Anomaly",
        "GUIDE shows identical F1 (0.8303) across all ratios. This suggests it may be re-training",
        "sub-models from scratch rather than performing incremental unlearning, making it inherently",
        "robust but also meaning the unlearning mechanism is effectively a full retrain.\n",
        "\n## Implications for Attack Research\n",
        "1. **GNNDelete** is the most promising attack target (10.0% F1 drop at r=0.2)",
        "2. **GIF** and **MEGU** show moderate vulnerability (~2-3% drop)",
        "3. **GUIDE**, **SGU**, **GUKD**, **D2DGN** are robust to random node removal",
        "4. Attack strategies (TracIn/IM/Hybrid) may amplify these drops by selecting critical nodes",
        "\n## Plots\n",
        "See `plots/` directory for:",
        "- `round1_overview.png`: All 15 methods bar chart",
        "- `all_methods_combined.png`: F1 vs unlearn size for all methods",
        "- `vulnerability_ranking.png`: Methods ranked by F1 drop",
        "- `{Method}_f1_curve.png`: Individual method F1 curves",
        "- `category_comparison.png`: Average vulnerability by method category",
        "- `time_vs_ratio.png`: Unlearning time scaling",
    ])

    out_path = os.path.join(RESULTS_DIR, "round2_detail.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Saved round2_detail.md")


def main():
    print("Loading Round 2 results...")
    results = load_round2()

    print(f"\nLoaded {len(results)} methods.\n")

    print("1. Round 1 overview bar chart")
    plot_round1_bar()

    print("\n2. Per-method F1 curves")
    plot_per_method(results)

    print("\n3. Combined comparison chart")
    plot_combined(results)

    print("\n4. Vulnerability ranking")
    plot_f1_drop_bar(results)

    print("\n5. Time vs ratio")
    plot_time_vs_ratio(results)

    print("\n6. Category comparison")
    plot_category_comparison(results)

    print("\n7. Method compatibility JSON")
    compat = generate_compatibility_json(results)

    print("\n8. Round 2 detail report")
    generate_round2_detail_md(results, compat)

    print(f"\nAll outputs saved to:")
    print(f"  Plots: {PLOT_DIR}")
    print(f"  Reports: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
