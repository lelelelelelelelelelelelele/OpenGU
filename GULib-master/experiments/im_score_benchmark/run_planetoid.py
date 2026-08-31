"""Preflight or run one historical public-Planetoid diagnostic cell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from experiments.planetoid_source import (
    SUPPORTED_DATASETS,
    resolve_planetoid_public_source,
    validate_public_split,
)

from .benchmark import run_selector_benchmark
from .rr_core import DirectedGraph
from .runner_common import (
    EXECUTION_TOKEN,
    REPO_ROOT,
    assert_execution_authorized,
    parse_int_list,
    parse_name_list,
    write_json_atomic,
)


DEFAULT_METHODS = ",".join(
    [
        "degree",
        "random",
        "im_batch_celf_current",
        "im_celf_strict",
        "corrected_imm",
        "opimc",
        "rr_sni",
        "rr_shapley",
        "rr_ksemivalue",
    ]
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=SUPPORTED_DATASETS, required=True)
    parser.add_argument(
        "--data-root",
        type=Path,
        default=REPO_ROOT / "data" / "raw",
    )
    parser.add_argument("--selector-seed", type=int, default=42)
    parser.add_argument("--budgets", default="3,7,14")
    parser.add_argument("--methods", default=DEFAULT_METHODS)
    parser.add_argument("--propagation-probability", type=float, default=0.1)
    parser.add_argument("--score-rr-count", type=int, default=4096)
    parser.add_argument("--legacy-mc-rounds", type=int, default=100)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--delta", type=float, default=0.01)
    parser.add_argument("--imm-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--opim-initial-rr-count", type=int, default=4096)
    parser.add_argument("--opim-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--evaluator-min-rr-sets", type=int, default=4096)
    parser.add_argument("--evaluator-batch-rr-sets", type=int, default=4096)
    parser.add_argument("--evaluator-max-rr-sets", type=int, default=2_000_000)
    parser.add_argument("--evaluator-half-width", type=float, default=0.005)
    parser.add_argument("--allow-noncanonical-data-root", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approval-token", default="")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = _parser().parse_args(argv)
    if args.formal:
        raise RuntimeError(
            "public Planetoid is diagnostic-only; formal modern-IM runs "
            "must use canonical OpenGU processed train candidates"
        )
    provenance = assert_execution_authorized(
        execute=bool(args.execute),
        approval_token=args.approval_token,
        formal=bool(args.formal),
    )
    source = resolve_planetoid_public_source(
        args.data_root,
        repository_root=REPO_ROOT,
        dataset=args.dataset,
        allow_noncanonical_root=bool(args.allow_noncanonical_data_root),
    )
    preflight = {
        "schema": "im_score_benchmark.planetoid_preflight",
        "version": 1,
        "execute": bool(args.execute),
        "formal": bool(args.formal),
        "claim_scope": "historical_public_split_diagnostic_only",
        "execution_token_required": EXECUTION_TOKEN,
        "dataset_source": source.to_manifest(),
        "git_provenance": provenance,
        "budgets": parse_int_list(args.budgets),
        "methods": parse_name_list(args.methods),
    }
    if not args.execute:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    if args.output is None:
        raise ValueError("--output is required with --execute")

    from torch_geometric.datasets import Planetoid
    from torch_geometric.transforms import NormalizeFeatures

    dataset = Planetoid(
        root=str(source.resolved_root),
        name=source.storage_name,
        split="public",
        transform=NormalizeFeatures(),
    )
    data = dataset[0]
    split_observation = validate_public_split(data, args.dataset)
    candidates = (
        data.train_mask.nonzero(as_tuple=False).view(-1).cpu().tolist()
    )
    graph = DirectedGraph.from_edge_index(data.edge_index, int(data.num_nodes))
    result = run_selector_benchmark(
        graph,
        dataset_name=args.dataset,
        candidate_nodes=candidates,
        budgets=parse_int_list(args.budgets),
        selector_seed=int(args.selector_seed),
        propagation_probability=float(args.propagation_probability),
        methods=parse_name_list(args.methods),
        score_rr_count=int(args.score_rr_count),
        legacy_mc_rounds=int(args.legacy_mc_rounds),
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
            **source.to_manifest(),
            "split_observation": split_observation,
            "git_provenance": provenance,
            "run_kind": "formal" if args.formal else "diagnostic",
        },
    )
    write_json_atomic(args.output, result, overwrite=bool(args.overwrite))
    print(
        json.dumps(
            {
                "output": str(args.output.expanduser().resolve(strict=False)),
                "dataset": args.dataset,
                "budgets": parse_int_list(args.budgets),
                "formal": bool(args.formal),
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
