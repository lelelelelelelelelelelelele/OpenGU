"""Evaluate real set-deletion effects for one cached B/C selection cell."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

import torch
import torch_geometric
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

from cache_v2.runtime import load_selection_artifact
from experiments.c_target_v1.core import ids_hash, source_fingerprint
from experiments.c_target_v1.score_store import ScoreBundlePayload
from experiments.selection_budget_planner import MAXK_SELECTION_PLAN_SCHEMA

from .core import remove_selected_nodes, train_model_once


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "results" / "bc_target_v2" / "downstream"


def _int_list(value: str) -> Sequence[int]:
    result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return tuple(sorted(set(result), reverse=True))


def _str_list(value: str) -> Sequence[str]:
    result = tuple(item.strip() for item in value.split(",") if item.strip())
    if not result:
        raise argparse.ArgumentTypeError("expected comma-separated names")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--budgets", type=_int_list, default=None)
    parser.add_argument("--methods", type=_str_list, default=None)
    parser.add_argument("--fail-if-compute-called", action="store_true")
    parser.add_argument("--overwrite-output", action="store_true")
    return parser


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-{0}".format(os.getpid()))
    temporary.write_bytes(
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            sort_keys=True,
        ).encode("utf-8")
    )
    os.replace(str(temporary), str(path))


def _load_exact_output(
    path: Path,
    recipe_hash: str,
    *,
    overwrite: bool,
    fail_if_compute_called: bool,
) -> Optional[Mapping[str, Any]]:
    if not path.is_file():
        if fail_if_compute_called:
            raise RuntimeError(
                "downstream compute would run on an asserted exact hit"
            )
        return None
    existing = json.loads(path.read_text(encoding="utf-8"))
    observed = existing.get("recipe_hash")
    if observed != recipe_hash:
        raise RuntimeError(
            "downstream output Recipe mismatch: expected={0}, observed={1}".format(
                recipe_hash, observed
            )
        )
    if overwrite:
        if fail_if_compute_called:
            raise ValueError(
                "--overwrite-output conflicts with --fail-if-compute-called"
            )
        return None
    return existing


def _method_family(name: str) -> str:
    if name in ("random", "degree"):
        return "control"
    if name == "a_grad_norm":
        return "A"
    if name.startswith("b_param_"):
        return "B"
    if name == "legacy":
        return "legacy"
    if "graph" in name or name == "gt_full":
        return "C-GIF"
    if "simple" in name or name == "gt_simple":
        return "C-IF"
    return "C-point"


def _effect(base: Mapping[str, float], deleted: Mapping[str, float]) -> Dict[str, float]:
    return {
        "validation_loss_increase": float(
            deleted["validation_loss"] - base["validation_loss"]
        ),
        "validation_accuracy_drop": float(
            base["validation_accuracy"] - deleted["validation_accuracy"]
        ),
        "test_loss_increase": float(
            deleted["test_loss"] - base["test_loss"]
        ),
        "test_accuracy_drop": float(
            base["test_accuracy"] - deleted["test_accuracy"]
        ),
        "retained_train_accuracy_drop": float(
            base["train_accuracy"] - deleted["train_accuracy"]
        ),
    }


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    started = time.perf_counter()
    selection_path = args.selection_summary.expanduser().resolve()
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    if selection.get("schema") != "bc_target_v2.selection_summary":
        raise ValueError("selection summary schema is unsupported")
    if selection.get("version") != 2:
        raise ValueError(
            "selection summary must be version 2 with max-k Selection Artifacts"
        )

    payload_path = Path(selection["cache"]["payload_path"]).resolve()
    payload = ScoreBundlePayload.from_bytes(payload_path.read_bytes())
    payload.validate_against(
        __import__("cache_v2").ArtifactRecipe(
            {
                "candidate_set": {
                    "ordered_ids_hash": payload.candidate_ids_hash
                },
                "score_names": list(payload.scores),
            }
        )
    )
    # The lightweight validation above checks the two payload-to-recipe axes
    # used by ScoreBundlePayload without importing tagged header JSON.

    config = selection["config"]
    budgets = (
        tuple(int(value) for value in selection["budgets"])
        if args.budgets is None
        else tuple(int(value) for value in args.budgets)
    )
    methods = (
        tuple(sorted(selection["selection_artifacts"]))
        if args.methods is None
        else tuple(args.methods)
    )
    if any(value > len(payload.candidate_nodes_ordered) for value in budgets):
        raise ValueError("a downstream budget exceeds the candidate count")
    unknown = sorted(set(methods) - set(payload.scores))
    if unknown:
        raise ValueError("unknown downstream methods: {0}".format(unknown))
    missing_artifacts = sorted(set(methods) - set(selection["selection_artifacts"]))
    if missing_artifacts:
        raise ValueError(
            "methods have no Selection Artifact: {0}".format(missing_artifacts)
        )
    unsupported_budgets = sorted(set(budgets) - set(int(v) for v in selection["budgets"]))
    if unsupported_budgets:
        raise ValueError(
            "downstream budgets were not materialized by selection: {0}".format(
                unsupported_budgets
            )
        )

    selection_identities = {
        method: {
            "artifact_id": selection["selection_artifacts"][method]["artifact"][
                "artifact_id"
            ],
            "recipe_hash": selection["selection_artifacts"][method]["artifact"][
                "recipe_hash"
            ],
            "content_hash": selection["selection_artifacts"][method]["artifact"][
                "content_hash"
            ],
            "artifact_k": int(
                selection["selection_artifacts"][method]["artifact_k"]
            ),
            "request_max_k": int(
                selection["selection_artifacts"][method]["request_max_k"]
            ),
        }
        for method in methods
    }

    code_fingerprint = source_fingerprint(
        (
            Path(__file__).resolve(),
            Path(__file__).with_name("core.py"),
            REPO_ROOT / "experiments" / "c_target_v1" / "core.py",
        )
    )
    recipe = {
        "schema": "bc_target_v2.downstream_recipe",
        "version": 2,
        "producer": code_fingerprint,
        "source_score_artifact_id": selection["cache"]["artifact_id"],
        "source_score_content_hash": selection["cache"]["content_hash"],
        "selection_candidate_hash": payload.candidate_ids_hash,
        "selection_artifacts": selection_identities,
        "dataset": selection["dataset"],
        "seed": int(selection["seed"]),
        "methods": list(methods),
        "budgets": list(budgets),
        "deletion": {
            "train_mask": "selected_false",
            "graph": "remove_all_incident_edges",
            "per_candidate_exact_retrain": False,
            "set_level_retrain_once": True,
        },
        "training": {
            "architecture": "GateGCN",
            "hidden_channels": int(config["hidden_channels"]),
            "dropout": float(config["dropout"]),
            "epochs": int(config["epochs"]),
            "optimizer": config["optimizer"],
            "lr": float(config["lr"]),
            "weight_decay": float(config["weight_decay"]),
            "milestones": list(config["milestones"]),
            "gamma": float(config["gamma"]),
            "seed": int(selection["seed"]),
            "num_threads": int(config["num_threads"]),
        },
        "evaluation": {
            "target": "validation_mask",
            "utility": "test_mask",
            "loss": "mean_cross_entropy",
            "accuracy": "node_classification_accuracy",
        },
    }
    recipe_hash = _sha(recipe)
    output_path = args.output
    if output_path is None:
        output_path = DEFAULT_OUTPUT_ROOT / (
            "{0}_gcn_seed{1}_downstream.json".format(
                str(selection["dataset"]).lower(), int(selection["seed"])
            )
        )
    output_path = output_path.expanduser().resolve()
    existing = _load_exact_output(
        output_path,
        recipe_hash,
        overwrite=args.overwrite_output,
        fail_if_compute_called=args.fail_if_compute_called,
    )
    if existing is not None:
        print(
            json.dumps(
                {
                    "output": str(output_path),
                    "cache_hit": True,
                    "recipe_hash": recipe_hash,
                    "result_count": len(existing["results"]),
                },
                ensure_ascii=False,
            )
        )
        return 0

    dataset = Planetoid(
        root=str(Path(config["data_root"]).expanduser().resolve()),
        name=selection["dataset"],
        transform=NormalizeFeatures(),
    )
    data = dataset[0].to(torch.device("cpu"))
    observed_candidates = torch.where(data.train_mask)[0].sort().values
    if ids_hash(observed_candidates) != payload.candidate_ids_hash:
        raise RuntimeError("downstream candidate set does not match selection")

    loaded_selections = {}
    for method in methods:
        manifest = selection["selection_artifacts"][method]
        if manifest.get("schema") != MAXK_SELECTION_PLAN_SCHEMA:
            raise ValueError(
                "Selection Artifact manifest schema is unsupported for {0}".format(
                    method
                )
            )
        artifact = manifest["artifact"]
        loaded = load_selection_artifact(
            Path(manifest["cache"]["root"]).expanduser().resolve(),
            artifact["artifact_id"],
            num_nodes=int(data.num_nodes),
            candidate_nodes=tuple(int(value) for value in observed_candidates.tolist()),
            expected_selector=method,
            expected_k=int(manifest["artifact_k"]),
        )
        if (
            loaded.recipe_hash != artifact["recipe_hash"]
            or loaded.content_hash != artifact["content_hash"]
        ):
            raise RuntimeError(
                "Selection Artifact identity changed for {0}".format(method)
            )
        loaded_selections[method] = loaded

    training_kwargs = {
        "in_channels": int(dataset.num_features),
        "hidden_channels": int(config["hidden_channels"]),
        "out_channels": int(dataset.num_classes),
        "dropout": float(config["dropout"]),
        "seed": int(selection["seed"]),
        "num_threads": int(config["num_threads"]),
        "epochs": int(config["epochs"]),
        "lr": float(config["lr"]),
        "weight_decay": float(config["weight_decay"]),
        "milestones": tuple(int(value) for value in config["milestones"]),
        "gamma": float(config["gamma"]),
        "optimizer_name": str(config["optimizer"]),
    }
    base_model, base_observation = train_model_once(data, **training_kwargs)
    del base_model
    expected_state_hash = selection["selector_model_final_state_hash"]
    if base_observation["state_hash"] != expected_state_hash:
        raise RuntimeError(
            "downstream base model does not reproduce the selector model"
        )
    base_metrics = base_observation["metrics"]

    results = []
    memo: Dict[Tuple[int, ...], Mapping[str, Any]] = {}
    for method in methods:
        loaded = loaded_selections[method]
        ranking = tuple(int(value) for value in loaded.selected_nodes)
        manifest = selection["selection_artifacts"][method]
        for budget in budgets:
            selected_rank_order = ranking[: int(budget)]
            view = manifest["views"].get(str(int(budget)))
            if view is None or tuple(view["selected_nodes"]) != selected_rank_order:
                raise RuntimeError(
                    "Selection prefix manifest mismatch for {0} k={1}".format(
                        method, budget
                    )
                )
            selected_key = tuple(sorted(selected_rank_order))
            if selected_key in memo:
                observation = memo[selected_key]
                reused = True
            else:
                deleted_data = data.clone()
                (
                    deleted_data.edge_index,
                    deleted_data.train_mask,
                ) = remove_selected_nodes(
                    data.edge_index, data.train_mask, selected_key
                )
                edge_count_before = int(data.edge_index.shape[1])
                model, trained = train_model_once(
                    deleted_data, **training_kwargs
                )
                del model
                observation = {
                    "state_hash": trained["state_hash"],
                    "training": trained["training"],
                    "metrics": trained["metrics"],
                    "edge_count_before": edge_count_before,
                    "edge_count_after": int(
                        deleted_data.edge_index.shape[1]
                    ),
                    "removed_directed_edges": edge_count_before
                    - int(deleted_data.edge_index.shape[1]),
                }
                memo[selected_key] = observation
                reused = False
            results.append(
                {
                    "dataset": selection["dataset"],
                    "seed": int(selection["seed"]),
                    "method": method,
                    "family": _method_family(method),
                    "budget": int(budget),
                    "selected_rank_order": list(selected_rank_order),
                    "selected_set": list(selected_key),
                    "selected_set_hash": hashlib.sha256(
                        ",".join(str(value) for value in selected_key).encode(
                            "ascii"
                        )
                    ).hexdigest(),
                    "selection_provenance": {
                        "artifact_id": loaded.artifact_id,
                        "recipe_hash": loaded.recipe_hash,
                        "content_hash": loaded.content_hash,
                        "artifact_k": loaded.k,
                        "requested_k": int(budget),
                        "request_max_k": int(manifest["request_max_k"]),
                        "cache_outcome": view["cache_outcome"],
                        "prefix_reuse": bool(view["prefix_reuse"]),
                        "reuse_kind": view["reuse_kind"],
                        "lookup_policy": manifest["cache"]["lookup_policy"],
                    },
                    "reused_identical_selected_set": reused,
                    "deleted_model": dict(observation),
                    "effect": _effect(
                        base_metrics, observation["metrics"]
                    ),
                }
            )

    output = {
        "schema": "bc_target_v2.downstream_summary",
        "version": 2,
        "recipe": recipe,
        "recipe_hash": recipe_hash,
        "cache_hit": False,
        "selection_summary": str(selection_path),
        "source_score_artifact_id": selection["cache"]["artifact_id"],
        "source_score_content_hash": selection["cache"]["content_hash"],
        "selection_artifacts": selection_identities,
        "dataset": selection["dataset"],
        "seed": int(selection["seed"]),
        "budgets": list(budgets),
        "methods": list(methods),
        "base_model": base_observation,
        "unique_selected_sets_trained": len(memo),
        "result_count": len(results),
        "results": results,
        "runtime": {"total_seconds": time.perf_counter() - started},
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torch_geometric": torch_geometric.__version__,
            "platform": platform.platform(),
            "executable": sys.executable,
        },
        "per_candidate_exact_retrain_performed": False,
    }
    _write_json_atomic(output_path, output)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "cache_hit": False,
                "recipe_hash": recipe_hash,
                "result_count": len(results),
                "unique_selected_sets_trained": len(memo),
                "seconds": output["runtime"]["total_seconds"],
            },
            ensure_ascii=False,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
