"""Data-driven attack chart generation."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT_JSON = REPO_ROOT / "results" / "evaluation" / "attack" / "attack_matrix.json"
DEFAULT_OUT_DIR = REPO_ROOT / "results" / "evaluation" / "attack" / "plots"

METHOD_COLORS = {
    "GIF": "#2ecc71",
    "GNNDelete": "#e74c3c",
    "GraphEraser": "#3498db",
    "GUIDE": "#9b59b6",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_attack_matrix(input_json: Path) -> dict:
    with input_json.open("r", encoding="utf-8") as file_obj:
        payload = json.load(file_obj)

    _require(isinstance(payload, dict), "Input JSON must be an object")
    for key in ("methods", "strategies", "values", "unit"):
        _require(key in payload, f"Missing required key: {key}")

    methods = payload["methods"]
    strategies = payload["strategies"]
    values = payload["values"]
    unit = payload["unit"]

    _require(isinstance(methods, list) and methods, "'methods' must be a non-empty list")
    _require(isinstance(strategies, list) and strategies, "'strategies' must be a non-empty list")
    _require(unit == "ratio", "Only unit='ratio' is supported")
    _require(isinstance(values, dict), "'values' must be an object")

    for method in methods:
        _require(method in values, f"values missing method: {method}")
        row = values[method]
        _require(isinstance(row, dict), f"values[{method}] must be an object")
        for strategy in strategies:
            _require(strategy in row, f"values[{method}] missing strategy: {strategy}")
            try:
                float(row[strategy])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"values[{method}][{strategy}] must be numeric") from exc

    return payload


def _save_plot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def generate_attack_charts(payload: dict, out_dir: Path):
    methods = payload["methods"]
    strategies = payload["strategies"]
    data = payload["values"]

    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(strategies))
    width = 0.8 / len(methods)

    for idx, method in enumerate(methods):
        vals = [float(data[method][strategy]) * 100 for strategy in strategies]
        offset = width * idx
        color = METHOD_COLORS.get(method, "#95a5a6")
        ax.bar(x + offset, vals, width, label=method, color=color)

    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    ax.set_xlabel("Attack Strategy", fontsize=12)
    ax.set_ylabel("F1 Drop (%)", fontsize=12)
    ax.set_title("Attack Effectiveness by Method and Strategy", fontsize=14)
    ax.set_xticks(x + width * (len(methods) - 1) / 2)
    ax.set_xticklabels(strategies)
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    plot1 = out_dir / "attack_effectiveness_by_method.png"
    _save_plot(plot1)

    fig, ax = plt.subplots(figsize=(10, 6))
    matrix = np.array([[float(data[m][s]) * 100 for s in strategies] for m in methods])
    image = ax.imshow(matrix, cmap="RdYlGn_r", aspect="auto", vmin=-15, vmax=15)

    for i in range(len(methods)):
        for j in range(len(strategies)):
            val = matrix[i, j]
            color = "white" if abs(val) > 7 else "black"
            ax.text(j, i, f"{val:.1f}%", ha="center", va="center", color=color, fontsize=10)

    ax.set_xticks(np.arange(len(strategies)))
    ax.set_yticks(np.arange(len(methods)))
    ax.set_xticklabels(strategies)
    ax.set_yticklabels(methods)
    ax.set_xlabel("Attack Strategy", fontsize=12)
    ax.set_ylabel("GU Method", fontsize=12)
    ax.set_title("Attack Effectiveness Heatmap (F1 Drop %)", fontsize=14)

    plt.colorbar(image, ax=ax, label="F1 Drop (%)")
    plot2 = out_dir / "attack_heatmap.png"
    _save_plot(plot2)

    fig, ax = plt.subplots(figsize=(10, 6))
    categories = [
        ("IF-based (GIF)", ["GIF"]),
        ("Learning-based (GNNDelete)", ["GNNDelete"]),
        ("Shard-based (GraphEraser, GUIDE)", ["GraphEraser", "GUIDE"]),
    ]

    x = np.arange(len(strategies))
    width = 0.25
    for idx, (label, members) in enumerate(categories):
        existing = [m for m in members if m in methods]
        if not existing:
            continue
        vals = []
        for strategy in strategies:
            mean_val = np.mean([float(data[m][strategy]) for m in existing]) * 100
            vals.append(mean_val)
        ax.bar(x + (idx - 1) * width, vals, width, label=label)

    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    ax.set_xlabel("Attack Strategy", fontsize=12)
    ax.set_ylabel("F1 Drop (%)", fontsize=12)
    ax.set_title("Attack Effectiveness by Method Type", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(strategies)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plot3 = out_dir / "attack_by_type.png"
    _save_plot(plot3)

    return [plot1, plot2, plot3]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate attack effectiveness charts from JSON")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT_JSON)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    payload = load_attack_matrix(args.input_json)
    outputs = generate_attack_charts(payload, args.out_dir)
    for path in outputs:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
