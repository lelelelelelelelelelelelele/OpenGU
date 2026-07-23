"""Dataset-free end-to-end acceptance run for the IM benchmark engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .aggregate import aggregate_documents
from .benchmark import SUPPORTED_METHODS, run_selector_benchmark
from .render_report import render_html, render_markdown
from .rr_core import DirectedGraph
from .runner_common import write_json_atomic


def run_local_acceptance():
    """Exercise all selector lanes on a deterministic in-memory fixture."""

    graph = DirectedGraph.from_edges(
        8,
        [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 6),
            (2, 6),
            (6, 7),
        ],
    )
    benchmark = run_selector_benchmark(
        graph,
        dataset_name="dataset-free-eight-node-fixture",
        candidate_nodes=list(range(graph.num_nodes)),
        budgets=[1, 2],
        selector_seed=42,
        propagation_probability=1.0,
        methods=SUPPORTED_METHODS,
        score_rr_count=256,
        legacy_mc_rounds=4,
        current_celf_batch_size=2,
        epsilon=0.5,
        delta=0.2,
        imm_max_rr_sets=20_000,
        opim_initial_rr_count=64,
        opim_max_rr_sets=512,
        evaluator_seed=91_337,
        evaluator_min_rr_sets=256,
        evaluator_batch_rr_sets=256,
        evaluator_max_rr_sets=512,
        evaluator_half_width=0.02,
        source_manifest={
            "run_kind": "dataset_free_local_only",
            "ssh_used": False,
            "formal_dataset_used": False,
            "gu_cell_used": False,
            "claim_scope": "implementation_acceptance_only",
        },
    )
    aggregate = aggregate_documents([benchmark])
    return {
        "benchmark": benchmark,
        "aggregate": aggregate,
        "markdown": render_markdown(aggregate),
        "html": render_html(render_markdown(aggregate), aggregate),
    }


def _write_text(path: Path, value: str, overwrite: bool) -> None:
    target = path.expanduser().resolve(strict=False)
    if target.exists() and not overwrite:
        raise FileExistsError(
            "output already exists; pass --overwrite explicitly: {0}".format(
                target
            )
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    result = run_local_acceptance()
    write_json_atomic(args.json, result["benchmark"], overwrite=args.overwrite)
    _write_text(args.markdown, result["markdown"], args.overwrite)
    _write_text(args.html, result["html"], args.overwrite)
    print(
        json.dumps(
            {
                "json": str(args.json.expanduser().resolve(strict=False)),
                "markdown": str(args.markdown.expanduser().resolve(strict=False)),
                "html": str(args.html.expanduser().resolve(strict=False)),
                "row_count": len(result["aggregate"]["rows"]),
                "run_kind": "dataset_free_local_only",
                "ssh_used": False,
                "formal_dataset_used": False,
                "gu_cell_used": False,
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
