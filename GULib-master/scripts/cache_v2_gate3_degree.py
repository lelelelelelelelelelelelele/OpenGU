#!/usr/bin/env python3
"""Materialize and compare one real Cora Degree Gate 3 Artifact bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from experiments.artifact_comparison import ComparisonPolicy
from experiments.gate3_degree_adapter import materialize_degree_gate3_bundle


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source-leaf", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--store-root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--score-atol", type=float, default=0.0)
    parser.add_argument("--prediction-atol", type=float, default=0.0)
    parser.add_argument("--evaluation-atol", type=float, default=1e-6)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.report.is_absolute():
        raise SystemExit("--report must be an absolute path")
    policy = ComparisonPolicy.from_atol(
        score_atol=args.score_atol,
        prediction_atol=args.prediction_atol,
        evaluation_atol=args.evaluation_atol,
    )
    document = materialize_degree_gate3_bundle(
        source_leaf=args.source_leaf,
        processed_root=args.processed_root,
        store_root=args.store_root,
        policy=policy,
    )
    report = args.report.resolve(strict=False)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": document["status"],
                "passed": document["passed"],
                "artifact_ids": document["artifact_ids"],
                "comparison_report_hash": document["comparison_report_hash"],
                "report": str(report),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if document["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
