"""Aggregate B/C selection and downstream JSON outputs into report tables."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULT_ROOT = REPO_ROOT / "results" / "bc_target_v2"


PAIR_SET = (
    ("gt_simple", "gt_full"),
    ("r_point", "gt_full"),
    ("p_point", "r_point"),
    ("p_simple", "gt_simple"),
    ("p_graph", "gt_full"),
    ("tracin_cp_point_3", "r_point"),
    ("tracin_cp_point_6", "r_point"),
    ("tracin_cp_simple_3", "gt_simple"),
    ("tracin_cp_simple_6", "gt_simple"),
    ("tracin_cp_graph_3", "gt_full"),
    ("tracin_cp_graph_6", "gt_full"),
)

HISTORICAL_VALIDATION_PAIR_SET = (
    ("a_grad_norm", "b_param_lissa"),
    ("b_param_hutch", "b_param_lissa"),
    ("b_param_lissa", "gt_full"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selection-dir",
        type=Path,
        default=DEFAULT_RESULT_ROOT / "selection",
    )
    parser.add_argument(
        "--downstream-dir",
        type=Path,
        default=DEFAULT_RESULT_ROOT / "downstream",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_RESULT_ROOT / "aggregate",
    )
    return parser


def _mean_std(values: Sequence[float]) -> Tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    return (
        float(statistics.mean(values)),
        float(statistics.stdev(values)) if len(values) > 1 else 0.0,
    )


def _pair_key(left: str, right: str) -> str:
    return "__".join(sorted((left, right)))


def _jaccard(left: Iterable[int], right: Iterable[int]) -> float:
    first = set(int(value) for value in left)
    second = set(int(value) for value in right)
    union = first | second
    return float(len(first & second) / len(union)) if union else 1.0


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    selection_paths = sorted(
        args.selection_dir.expanduser().resolve().glob("*_selection.json")
    )
    downstream_paths = sorted(
        args.downstream_dir.expanduser().resolve().glob("*_downstream.json")
    )
    if not selection_paths:
        raise FileNotFoundError("no selection summaries found")

    selections = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in selection_paths
    ]
    downstream = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in downstream_paths
    ]

    selection_rows = []
    for cell in selections:
        available_pairs = tuple(PAIR_SET) + tuple(
            pair
            for pair in HISTORICAL_VALIDATION_PAIR_SET
            if all(name in cell["rankings"] for name in pair)
        )
        for left, right in available_pairs:
            key = _pair_key(left, right)
            metrics_by_k = cell["pairwise_metrics"][key]
            for budget in cell["budgets"]:
                metric = metrics_by_k[str(budget)]
                selection_rows.append(
                    {
                        "dataset": cell["dataset"],
                        "seed": int(cell["seed"]),
                        "budget": int(budget),
                        "left": left,
                        "right": right,
                        "intersection": int(metric["intersection"]),
                        "jaccard": float(metric["jaccard"]),
                        "common_fraction": float(
                            metric["common_fraction"]
                        ),
                        "spearman": metric["spearman"],
                        "kendall": metric["kendall"],
                        "sign_agreement": float(
                            metric["sign_agreement"]
                        ),
                    }
                )

    selection_aggregate = []
    grouped_selection = defaultdict(list)
    for row in selection_rows:
        grouped_selection[
            (row["dataset"], row["budget"], row["left"], row["right"])
        ].append(row)
    for key, rows in sorted(grouped_selection.items()):
        dataset, budget, left, right = key
        j_mean, j_std = _mean_std([row["jaccard"] for row in rows])
        c_mean, c_std = _mean_std(
            [row["common_fraction"] for row in rows]
        )
        s_values = [
            float(row["spearman"])
            for row in rows
            if row["spearman"] is not None
        ]
        s_mean, s_std = _mean_std(s_values)
        selection_aggregate.append(
            {
                "dataset": dataset,
                "budget": budget,
                "left": left,
                "right": right,
                "n_seeds": len(rows),
                "jaccard_mean": j_mean,
                "jaccard_std": j_std,
                "common_fraction_mean": c_mean,
                "common_fraction_std": c_std,
                "spearman_mean": s_mean,
                "spearman_std": s_std,
            }
        )

    cross_seed_rows = []
    by_dataset = defaultdict(list)
    for cell in selections:
        by_dataset[cell["dataset"]].append(cell)
    for dataset, cells in sorted(by_dataset.items()):
        cells = sorted(cells, key=lambda item: int(item["seed"]))
        for left, right in itertools.combinations(cells, 2):
            for method in sorted(left["rankings"]):
                for budget in left["budgets"]:
                    cross_seed_rows.append(
                        {
                            "dataset": dataset,
                            "method": method,
                            "budget": int(budget),
                            "seed_left": int(left["seed"]),
                            "seed_right": int(right["seed"]),
                            "jaccard": _jaccard(
                                left["rankings"][method][: int(budget)],
                                right["rankings"][method][: int(budget)],
                            ),
                        }
                    )

    downstream_rows = []
    for cell in downstream:
        for row in cell["results"]:
            effect = row["effect"]
            downstream_rows.append(
                {
                    "dataset": row["dataset"],
                    "seed": int(row["seed"]),
                    "method": row["method"],
                    "family": row["family"],
                    "budget": int(row["budget"]),
                    "validation_loss_increase": float(
                        effect["validation_loss_increase"]
                    ),
                    "validation_accuracy_drop": float(
                        effect["validation_accuracy_drop"]
                    ),
                    "test_loss_increase": float(
                        effect["test_loss_increase"]
                    ),
                    "test_accuracy_drop": float(
                        effect["test_accuracy_drop"]
                    ),
                    "retained_train_accuracy_drop": float(
                        effect["retained_train_accuracy_drop"]
                    ),
                    "removed_directed_edges": int(
                        row["deleted_model"]["removed_directed_edges"]
                    ),
                    "reused_identical_selected_set": bool(
                        row["reused_identical_selected_set"]
                    ),
                }
            )

    downstream_aggregate = []
    grouped_downstream = defaultdict(list)
    for row in downstream_rows:
        grouped_downstream[
            (row["dataset"], row["method"], row["family"], row["budget"])
        ].append(row)
    for key, rows in sorted(grouped_downstream.items()):
        dataset, method, family, budget = key
        aggregate = {
            "dataset": dataset,
            "method": method,
            "family": family,
            "budget": budget,
            "n_seeds": len(rows),
        }
        for metric in (
            "validation_loss_increase",
            "validation_accuracy_drop",
            "test_loss_increase",
            "test_accuracy_drop",
            "retained_train_accuracy_drop",
            "removed_directed_edges",
        ):
            mean, std = _mean_std([float(row[metric]) for row in rows])
            aggregate[metric + "_mean"] = mean
            aggregate[metric + "_std"] = std
        downstream_aggregate.append(aggregate)

    global_downstream = []
    grouped_global = defaultdict(list)
    for row in downstream_rows:
        grouped_global[(row["method"], row["family"], row["budget"])].append(
            row
        )
    for key, rows in sorted(grouped_global.items()):
        method, family, budget = key
        aggregate = {
            "method": method,
            "family": family,
            "budget": budget,
            "n_cells": len(rows),
        }
        for metric in (
            "validation_loss_increase",
            "validation_accuracy_drop",
            "test_loss_increase",
            "test_accuracy_drop",
        ):
            mean, std = _mean_std([float(row[metric]) for row in rows])
            aggregate[metric + "_mean"] = mean
            aggregate[metric + "_std"] = std
        global_downstream.append(aggregate)

    output = {
        "schema": "bc_target_v2.aggregate",
        "version": 1,
        "selection_cell_count": len(selections),
        "downstream_cell_count": len(downstream),
        "selection_rows": selection_rows,
        "selection_aggregate": selection_aggregate,
        "cross_seed_rows": cross_seed_rows,
        "downstream_rows": downstream_rows,
        "downstream_aggregate": downstream_aggregate,
        "global_downstream": global_downstream,
        "coverage": {
            "datasets": sorted({cell["dataset"] for cell in selections}),
            "seeds": sorted({int(cell["seed"]) for cell in selections}),
            "budgets": sorted(
                {int(value) for cell in selections for value in cell["budgets"]}
            ),
            "methods": sorted(
                {name for cell in selections for name in cell["rankings"]}
            ),
        },
    }
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "matrix_summary.json").write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_csv(output_dir / "selection_metrics.csv", selection_rows)
    _write_csv(
        output_dir / "selection_aggregate.csv", selection_aggregate
    )
    _write_csv(output_dir / "cross_seed_stability.csv", cross_seed_rows)
    _write_csv(output_dir / "downstream_metrics.csv", downstream_rows)
    _write_csv(
        output_dir / "downstream_aggregate.csv", downstream_aggregate
    )
    _write_csv(output_dir / "global_downstream.csv", global_downstream)
    print(
        json.dumps(
            {
                "output": str(output_dir / "matrix_summary.json"),
                "selection_cells": len(selections),
                "downstream_cells": len(downstream),
                "selection_rows": len(selection_rows),
                "downstream_rows": len(downstream_rows),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
