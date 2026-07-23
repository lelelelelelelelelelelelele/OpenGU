"""Aggregate selector benchmark JSON files without rerunning selectors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import numpy as np

from .runner_common import write_json_atomic


def _require_benchmark(document: Mapping[str, Any]) -> None:
    if (
        document.get("schema")
        != "im_score_benchmark.selector_benchmark"
        or document.get("version") != 1
    ):
        raise ValueError("input is not a selector benchmark v1 document")


def aggregate_documents(
    documents: Iterable[Mapping[str, Any]],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    sources: List[Dict[str, Any]] = []
    for document in documents:
        _require_benchmark(document)
        dataset = str(document["dataset"])
        config = dict(document["config"])
        sources.append(
            {
                "dataset": dataset,
                "selector_seed": int(config["selector_seed"]),
                "source_manifest": dict(document.get("source_manifest") or {}),
            }
        )
        for budget_text, budget_result in sorted(
            document["budgets"].items(),
            key=lambda item: int(item[0]),
        ):
            budget = int(budget_text)
            evaluation = budget_result["independent_evaluation"]["methods"]
            for method, payload in sorted(budget_result["methods"].items()):
                selection = payload["selection"]
                certificate = selection.get("certificate")
                observed = evaluation[method]
                telemetry = payload["telemetry"]
                rows.append(
                    {
                        "dataset": dataset,
                        "selector_seed": int(config["selector_seed"]),
                        "budget": budget,
                        "method": method,
                        "wall_seconds": float(telemetry["wall_seconds"]),
                        "online_wall_seconds": float(
                            telemetry.get(
                                "online_wall_seconds",
                                telemetry["wall_seconds"],
                            )
                        ),
                        "shared_precompute_wall_seconds": float(
                            telemetry.get("shared_precompute_wall_seconds", 0.0)
                        ),
                        "excluded_one_time_setup_wall_seconds": float(
                            telemetry.get(
                                "excluded_one_time_setup_wall_seconds",
                                0.0,
                            )
                        ),
                        "time_semantics": telemetry.get(
                            "time_semantics",
                            "legacy_unspecified",
                        ),
                        "peak_rss_bytes": telemetry.get("peak_rss_bytes"),
                        "spread_estimate": float(observed["spread_estimate"]),
                        "spread_ratio_vs_degree": observed[
                            "spread_ratio_vs_degree"
                        ],
                        "paired_difference_probability": float(
                            observed["paired_difference_probability"]
                        ),
                        "paired_ci95_lower_probability": float(
                            observed["paired_ci95_probability"][0]
                        ),
                        "paired_ci95_upper_probability": float(
                            observed["paired_ci95_probability"][1]
                        ),
                        "certificate_kind": (
                            None if certificate is None else certificate["kind"]
                        ),
                        "certificate_ratio_lower_bound": (
                            None
                            if certificate is None
                            else float(certificate["ratio_lower_bound"])
                        ),
                        "certificate_paper_equivalent": (
                            None
                            if certificate is None
                            else bool(certificate["paper_equivalent"])
                        ),
                    }
                )
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["method"], []).append(row)
    method_summary = {}
    for method, method_rows in sorted(grouped.items()):
        ratios = [
            float(row["spread_ratio_vs_degree"])
            for row in method_rows
            if row["spread_ratio_vs_degree"] is not None
        ]
        wins = [
            row
            for row in method_rows
            if row["spread_ratio_vs_degree"] is not None
            and float(row["spread_ratio_vs_degree"]) >= 1.02
            and float(row["paired_ci95_lower_probability"]) > 0.0
        ]
        method_summary[method] = {
            "row_count": len(method_rows),
            "wall_seconds_mean": float(
                np.mean([row["wall_seconds"] for row in method_rows])
            ),
            "wall_seconds_max": float(
                np.max([row["wall_seconds"] for row in method_rows])
            ),
            "spread_ratio_vs_degree_mean": (
                None if not ratios else float(np.mean(ratios))
            ),
            "registered_degree_win_row_count": len(wins),
        }
    return {
        "schema": "im_score_benchmark.aggregate",
        "version": 1,
        "rows": rows,
        "method_summary": method_summary,
        "sources": sources,
        "interpretation": {
            "degree_win_row": (
                "spread_ratio_vs_degree >= 1.02 and paired CI95 lower > 0"
            ),
            "formal_claim_requires_matrix_gate": True,
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    documents = [
        json.loads(path.read_text(encoding="utf-8")) for path in args.inputs
    ]
    aggregate = aggregate_documents(documents)
    write_json_atomic(args.output, aggregate, overwrite=bool(args.overwrite))
    print(
        json.dumps(
            {
                "output": str(args.output.expanduser().resolve(strict=False)),
                "input_count": len(documents),
                "row_count": len(aggregate["rows"]),
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
