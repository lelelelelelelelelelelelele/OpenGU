"""Build one dataset's fail-closed target-direct external Selection manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

from cache_v2.runtime import load_selection_artifact
from experiments.processed_provider import ProcessedSplitContract
from experiments.target_direct_v1 import DEFAULT_SPLIT_CONTRACT, MODEL_SEEDS
from experiments.target_direct_v1.recipe import (
    ALGORITHM_VERSION,
    APPROVED_BUDGET_RATIOS,
    SCORE_NAMES,
)
from experiments.target_direct_v1.split_profile import verify_profile
from utils.target_checkpoint import data_identity, load_target_checkpoint


SCHEMA = "target_direct_v1.external_selection_manifest"
VERSION = 2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    target = Path(path).expanduser().resolve()
    if target.exists():
        raise FileExistsError("external manifest already exists: {0}".format(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp-{0}".format(os.getpid()))
    try:
        temporary.write_text(
            json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()


def build_manifest(
    *,
    repository_root: Path,
    processed_root: Path,
    selection_store_root: Path,
    dataset: str,
    summaries: Sequence[Path],
    expected_git_sha: str,
    ratio: float,
    required_seeds: Sequence[int] = MODEL_SEEDS,
    required_parameter_scope: str = "last_layer",
    strategy_order: Sequence[str] = SCORE_NAMES,
    split_contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    selection_store_root = Path(selection_store_root).resolve()
    required_seeds = tuple(int(seed) for seed in required_seeds)
    if (
        not required_seeds
        or len(set(required_seeds)) != len(required_seeds)
        or not set(required_seeds).issubset(set(MODEL_SEEDS))
    ):
        raise ValueError(
            "required_seeds must be a non-empty unique subset of {0}".format(
                list(MODEL_SEEDS)
            )
        )
    if required_parameter_scope != "last_layer":
        raise ValueError("formal target-direct manifest requires last_layer")
    if not any(
        abs(float(ratio) - approved) < 1e-12
        for approved in APPROVED_BUDGET_RATIOS
    ):
        raise ValueError(
            "formal target-direct ratio must be one of {0}".format(
                list(APPROVED_BUDGET_RATIOS)
            )
        )
    strategy_order = tuple(str(value) for value in strategy_order)
    if (
        len(strategy_order) != len(SCORE_NAMES)
        or len(set(strategy_order)) != len(strategy_order)
        or set(strategy_order) != set(SCORE_NAMES)
    ):
        raise ValueError("strategy_order must contain the exact 17 methods")
    profile = verify_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset=dataset,
        contract=split_contract,
    )
    inputs = profile["inputs"]
    observed_data_identity = data_identity(profile["data"])
    expected_k = max(1, int(inputs.candidate_count * float(ratio)))
    cells = []
    sources = []
    seeds = []
    checkpoints_by_seed = {}
    for source_path in summaries:
        source_path = Path(source_path).expanduser().resolve()
        summary = json.loads(source_path.read_text(encoding="utf-8"))
        if (
            summary.get("schema") != "target_direct_v1.selection_summary"
            or summary.get("version") != 3
            or (summary.get("status") or {}).get("state") != "success"
            or summary.get("algorithm_version") != ALGORITHM_VERSION
            or str(summary.get("dataset", "")).lower() != dataset.lower()
            or summary.get("processed_profile")
            != split_contract.processed_profile
            or summary.get("split_contract") != split_contract.to_manifest()
            or float((summary.get("budget") or {}).get("requested_ratio", -1))
            != float(ratio)
            or int((summary.get("budget") or {}).get("expected_k", -1))
            != expected_k
            or (summary.get("budget") or {}).get("denominator")
            != "train_candidate_count"
            or (summary.get("budget") or {}).get("rounding")
            != "floor_with_minimum_one"
            or int(
                (summary.get("budget") or {}).get("denominator_count", -1)
            )
            != inputs.candidate_count
            or int(summary.get("candidate_count", -1)) != inputs.candidate_count
            or summary.get("parameter_scope") != required_parameter_scope
        ):
            raise RuntimeError(
                "target-direct Selection summary identity mismatch: {0}".format(
                    source_path
                )
            )
        provenance = summary.get("git_provenance") or {}
        if (
            provenance.get("head") != expected_git_sha
            or provenance.get("worktree_dirty") is not False
        ):
            raise RuntimeError("Selection summary Git provenance is not formal")
        seed = int(summary["seed"])
        if seed in checkpoints_by_seed:
            raise RuntimeError("duplicate target-direct summary seed")
        checkpoint = dict(summary["target_checkpoint"])
        loaded_checkpoint = load_target_checkpoint(
            checkpoint["path"],
            expected_file_sha256=checkpoint["file_sha256"],
            expected_state_hash=checkpoint["state_hash"],
            expected_metadata={
                "dataset_name": dataset.lower(),
                "base_model": "GCN",
                "seed": seed,
                "processed_profile": split_contract.processed_profile,
                "split_contract": split_contract.to_manifest(),
                "num_epochs": 100,
                "gcn_num_layers": 2,
                "gcn_hidden": 64,
            },
        )
        if loaded_checkpoint["metadata"].get("data_identity") is None:
            raise RuntimeError("target checkpoint has no dataset identity")
        if loaded_checkpoint["metadata"]["data_identity"] != observed_data_identity:
            raise RuntimeError(
                "target checkpoint dataset/split identity differs from profile"
            )
        checkpoints_by_seed[seed] = {
            "path": loaded_checkpoint["path"],
            "file_sha256": loaded_checkpoint["file_sha256"],
            "state_hash": loaded_checkpoint["state_hash"],
            "checkpoint_count": len(loaded_checkpoint["checkpoints"]),
            "metadata": dict(loaded_checkpoint["metadata"]),
        }
        artifacts = summary.get("selection_artifacts") or {}
        if set(artifacts) != set(SCORE_NAMES):
            raise RuntimeError("Selection summary does not contain all 17 methods")
        for strategy in strategy_order:
            item = artifacts[strategy]
            artifact = item.get("artifact") or {}
            loaded = load_selection_artifact(
                selection_store_root,
                artifact.get("artifact_id"),
                num_nodes=inputs.num_nodes,
                candidate_nodes=inputs.candidate_nodes,
                expected_selector=strategy,
                expected_k=expected_k,
            )
            if (
                loaded.recipe_hash != artifact.get("recipe_hash")
                or loaded.content_hash != artifact.get("content_hash")
                or len(loaded.selected_nodes) != expected_k
            ):
                raise RuntimeError("Selection Artifact identity mismatch")
            cells.append(
                {
                    "strategy": strategy,
                    "seed": seed,
                    "ratio": float(ratio),
                    "k": expected_k,
                    "artifact": {
                        "artifact_id": loaded.artifact_id,
                        "recipe_hash": loaded.recipe_hash,
                        "content_hash": loaded.content_hash,
                    },
                    "selected_nodes": list(loaded.selected_nodes),
                    "target_checkpoint": checkpoints_by_seed[seed],
                    "source_score_artifact_id": summary["method_scores"][strategy][
                        "artifact_id"
                    ],
                    "source_score_recipe_hash": summary["method_scores"][strategy][
                        "recipe_hash"
                    ],
                }
            )
        seeds.append(seed)
        sources.append(
            {
                "path": str(source_path),
                "sha256": sha256_file(source_path),
                "seed": seed,
                "ratio": float(ratio),
                "method_score_artifact_ids": {name: item["artifact_id"] for name, item in summary["method_scores"].items()},
                "target_checkpoint_state_hash": checkpoint["state_hash"],
            }
        )
    seeds = sorted(seeds)
    if tuple(seeds) != tuple(sorted(required_seeds)):
        raise RuntimeError(
            "target-direct summaries must cover exact model seeds {0}".format(
                list(required_seeds)
            )
        )
    strategy_position = {
        strategy: position for position, strategy in enumerate(strategy_order)
    }
    cells.sort(
        key=lambda item: (strategy_position[item["strategy"]], item["seed"])
    )
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "dataset": dataset.lower(),
        "base_model": "GCN",
        "processed_profile": split_contract.processed_profile,
        "split_contract": split_contract.to_manifest(),
        "ratio": float(ratio),
        "budget_denominator": "train_candidate_count",
        "expected_k": expected_k,
        "candidate_count": inputs.candidate_count,
        "budget": {
            "ratio": float(ratio),
            "denominator": "train_candidate_count",
            "denominator_count": inputs.candidate_count,
            "rounding": "floor_with_minimum_one",
            "expected_k": expected_k,
        },
        "gu_methods": ["GNNDelete"],
        "strategies": list(strategy_order),
        "seeds": seeds,
        "parameter_scope": required_parameter_scope,
        "store_root": str(selection_store_root),
        "selection_identity": profile["manifest"]["selection_identity"],
        "profile_manifest_path": profile["manifest_path"],
        "profile_manifest_sha256": sha256_file(Path(profile["manifest_path"])),
        "git_sha": expected_git_sha,
        "source_summaries": sources,
        "cells": cells,
        "claims": {
            "white_box": True,
            "selector_and_gu_share_exact_checkpoint": True,
            "test_labels_used_for_selection": False,
            "formal_count_fail_closed": True,
            "method_score_budget_semantics":
                "prefix_stable_budget_independent",
            "budget_conditioned_strategies": [],
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--selection-store-root", type=Path, required=True)
    parser.add_argument(
        "--dataset", choices=("Cora", "CiteSeer", "PubMed"), required=True
    )
    parser.add_argument("--summaries", type=Path, nargs="+", required=True)
    parser.add_argument("--expected-git-sha", required=True)
    parser.add_argument("--ratio", type=float, required=True)
    parser.add_argument(
        "--required-seeds",
        type=int,
        nargs="+",
        default=list(MODEL_SEEDS),
    )
    parser.add_argument(
        "--parameter-scope",
        choices=("last_layer",),
        default="last_layer",
    )
    parser.add_argument(
        "--strategy-order",
        nargs="+",
        default=list(SCORE_NAMES),
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    manifest = build_manifest(
        repository_root=args.repository_root,
        processed_root=args.processed_root,
        selection_store_root=args.selection_store_root,
        dataset=args.dataset,
        summaries=args.summaries,
        expected_git_sha=args.expected_git_sha,
        ratio=args.ratio,
        required_seeds=args.required_seeds,
        required_parameter_scope=args.parameter_scope,
        strategy_order=args.strategy_order,
    )
    _atomic_json(args.output, manifest)
    print(
        json.dumps(
            {
                "output": str(args.output.expanduser().resolve()),
                "sha256": sha256_file(args.output.expanduser().resolve()),
                "cells": len(manifest["cells"]),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
