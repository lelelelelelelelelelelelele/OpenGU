"""Preflight or run the canonical OpenGU ogbn-arxiv selector gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from experiments.selection_inputs import (
    load_processed_selection_inputs,
    processed_data_path,
)

from .benchmark import run_selector_benchmark
from .rr_core import DirectedGraph
from .runner_common import (
    EXECUTION_TOKEN,
    REPO_ROOT,
    assert_execution_authorized,
    budgets_from_ratios,
    parse_float_list,
    parse_name_list,
    write_json_atomic,
)


DEFAULT_METHODS = ",".join(
    [
        "degree",
        "corrected_imm",
        "opimc",
        "rr_sni",
        "rr_shapley",
        "rr_ksemivalue",
    ]
)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--processed-root",
        type=Path,
        default=REPO_ROOT / "data" / "processed",
    )
    parser.add_argument(
        "--dataset",
        choices=("ogbn-arxiv",),
        default="ogbn-arxiv",
    )
    parser.add_argument("--selector-seed", type=int, default=42)
    parser.add_argument("--budget-ratios", default="0.001,0.005,0.01")
    parser.add_argument("--methods", default=DEFAULT_METHODS)
    parser.add_argument("--propagation-probability", type=float, default=0.1)
    parser.add_argument("--score-rr-count", type=int, default=4096)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--delta", type=float, default=0.01)
    parser.add_argument("--imm-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--opim-initial-rr-count", type=int, default=4096)
    parser.add_argument("--opim-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--evaluator-min-rr-sets", type=int, default=4096)
    parser.add_argument("--evaluator-batch-rr-sets", type=int, default=4096)
    parser.add_argument("--evaluator-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--evaluator-half-width", type=float, default=0.005)
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approval-token", default="")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    provenance = assert_execution_authorized(
        execute=bool(args.execute),
        approval_token=args.approval_token,
        formal=bool(args.formal),
    )
    canonical_root = (REPO_ROOT / "data" / "processed").resolve(strict=False)
    observed_root = args.processed_root.expanduser().resolve(strict=False)
    if observed_root != canonical_root:
        raise RuntimeError(
            "ogbn-arxiv runner requires checkout-local canonical processed root: "
            "{0}".format(canonical_root)
        )
    source_path = processed_data_path(
        observed_root,
        dataset_name=args.dataset,
        train_ratio=0.8,
        val_ratio=0.0,
        test_ratio=0.2,
        is_transductive=True,
        is_balanced=False,
    )
    source_exists = source_path.is_file()
    source_manifest = {
        "profile": "opengu_canonical_processed_transductive_80_20",
        "path": str(source_path),
        "exists": source_exists,
        "size_bytes": source_path.stat().st_size if source_exists else None,
        "sha256": _sha256_file(source_path) if source_exists else None,
        "git_provenance": provenance,
    }
    preflight = {
        "schema": "im_score_benchmark.arxiv_preflight",
        "version": 1,
        "execute": bool(args.execute),
        "formal": bool(args.formal),
        "execution_token_required": EXECUTION_TOKEN,
        "dataset": args.dataset,
        "source": source_manifest,
        "budget_ratios": parse_float_list(args.budget_ratios),
        "methods": parse_name_list(args.methods),
    }
    if not args.execute:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    if not source_exists:
        raise FileNotFoundError(
            "canonical ogbn-arxiv processed graph is missing: {0}".format(
                source_path
            )
        )
    if args.output is None:
        raise ValueError("--output is required with --execute")

    inputs = load_processed_selection_inputs(
        processed_root=observed_root,
        dataset_name=args.dataset,
        train_ratio=0.8,
        val_ratio=0.0,
        test_ratio=0.2,
        is_transductive=True,
        is_balanced=False,
    )
    graph = DirectedGraph.from_edge_index(inputs.edge_index, inputs.num_nodes)
    budgets = budgets_from_ratios(
        inputs.candidate_count,
        parse_float_list(args.budget_ratios),
    )
    result = run_selector_benchmark(
        graph,
        dataset_name=args.dataset,
        candidate_nodes=inputs.candidate_nodes,
        budgets=budgets,
        selector_seed=int(args.selector_seed),
        propagation_probability=float(args.propagation_probability),
        methods=parse_name_list(args.methods),
        score_rr_count=int(args.score_rr_count),
        epsilon=float(args.epsilon),
        delta=float(args.delta),
        imm_max_rr_sets=int(args.imm_max_rr_sets),
        opim_initial_rr_count=int(args.opim_initial_rr_count),
        opim_max_rr_sets=int(args.opim_max_rr_sets),
        evaluator_seed=99_999 + int(args.selector_seed),
        evaluator_min_rr_sets=int(args.evaluator_min_rr_sets),
        evaluator_batch_rr_sets=int(args.evaluator_batch_rr_sets),
        evaluator_max_rr_sets=int(args.evaluator_max_rr_sets),
        evaluator_half_width=float(args.evaluator_half_width),
        source_manifest={
            **source_manifest,
            "dataset_fingerprint": inputs.dataset_fingerprint,
            "graph_fingerprint": inputs.graph_fingerprint,
            "candidate_set_hash": inputs.candidate_set_hash,
            "candidate_count": inputs.candidate_count,
            "run_kind": "formal" if args.formal else "diagnostic",
        },
    )
    write_json_atomic(args.output, result, overwrite=bool(args.overwrite))
    print(
        json.dumps(
            {
                "output": str(args.output.expanduser().resolve(strict=False)),
                "dataset": args.dataset,
                "budgets": budgets,
                "formal": bool(args.formal),
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
