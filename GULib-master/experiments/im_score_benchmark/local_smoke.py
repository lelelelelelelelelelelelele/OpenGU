"""Dataset-free local smoke for the modern IM implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Sequence

from .exact_tiny import exact_optimal_selection, exact_spread
from .rr_core import DirectedGraph, sample_rr_bundle
from .score_reducers import build_score_bundle
from .selectors import corrected_imm_select, opimc_select


def run_local_smoke() -> Dict[str, Any]:
    """Exercise every public lane on a six-node directed fixture."""

    graph = DirectedGraph.from_edges(
        6,
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2)],
    )
    candidates = list(range(graph.num_nodes))
    rr_bundle = sample_rr_bundle(
        graph,
        candidate_nodes=candidates,
        rr_count=256,
        propagation_probability=1.0,
        rr_seed=42,
        metadata={"run_kind": "local_smoke"},
    )
    scores = build_score_bundle(rr_bundle, budgets=[1, 2])
    imm = corrected_imm_select(
        graph,
        candidate_nodes=candidates,
        budget=2,
        propagation_probability=1.0,
        selector_seed=42,
        epsilon=0.5,
        delta=0.2,
        max_rr_sets=20_000,
    )
    opim = opimc_select(
        graph,
        candidate_nodes=candidates,
        budget=2,
        propagation_probability=1.0,
        selector_seed=42,
        epsilon=0.5,
        delta=0.2,
        initial_rr_count=64,
        max_rr_sets=512,
    )
    exact_optimum, exact_optimum_spread = exact_optimal_selection(
        graph,
        candidates,
        2,
        1.0,
    )
    return {
        "schema": "im_score_benchmark.local_smoke",
        "version": 1,
        "run_kind": "dataset_free_local_only",
        "ssh_used": False,
        "formal_dataset_used": False,
        "gu_cell_used": False,
        "graph": {
            "num_nodes": graph.num_nodes,
            "edge_count": graph.edge_count,
        },
        "rr_bundle": rr_bundle.summary(),
        "score_rankings": {
            name: artifact.ranking.tolist()
            for name, artifact in sorted(scores.items())
        },
        "corrected_imm": imm.to_dict(),
        "opimc": opim.to_dict(),
        "exact": {
            "optimum": list(exact_optimum),
            "optimum_spread": exact_optimum_spread,
            "imm_spread": exact_spread(
                graph,
                imm.selected_nodes.tolist(),
                1.0,
            ),
            "opimc_spread": exact_spread(
                graph,
                opim.selected_nodes.tolist(),
                1.0,
            ),
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output. Omit to avoid writing any result artifact.",
    )
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    result = run_local_smoke()
    payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
