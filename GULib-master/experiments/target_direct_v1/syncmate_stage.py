"""Bounded target-direct Selection and GNNDelete stages for SyncMate.

The queue supplies only a reviewed action and dataset/seed stage. Paths,
methods, model settings, scope, and artifact identities come from the frozen
repository config.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import socket
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

import torch
import yaml

from experiments.path_policy import resolve_owned_path
from experiments.processed_provider import (
    ProcessedArtifactError,
)
from experiments.target_direct_v1 import (
    MODEL_SEEDS,
    target_direct_split_contract,
)
from experiments.target_direct_v1.build_gu_config import build_gu_config
from experiments.target_direct_v1.build_manifest import build_manifest
from experiments.target_direct_v1.recipe import (
    APPROVED_BUDGET_RATIOS,
    SCORE_BUDGET_SEMANTICS,
    SCORE_NAMES,
)
from experiments.target_direct_v1.methods import resolve_parameters
from experiments.effective_config import ConfigurationError, fields, read_yaml
from experiments.modular_evaluation import resolve_evaluation, require_consumer
from experiments.target_direct_v1.split_profile import stage_profile, verify_profile


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = (
    REPO_ROOT
    / "experiments"
    / "configs"
    / "syncmate_target_direct_formal_v2.yaml"
)
CONFIG_SCHEMA = "target_direct_v1.syncmate_formal"
CONFIG_VERSION = 2
RECEIPT_SCHEMA = "target_direct_v1.syncmate_selection_cell"
RECEIPT_VERSION = 3
ARTIFACT_NAMES = ("attack.json", "output-references.json", "predictions.npz", "_meta.json")
DATASETS = ("cora", "citeseer", "pubmed")
DATASET_NODE_COUNTS = {
    "cora": 2708,
    "citeseer": 3327,
    "pubmed": 19717,
}
STAGES = tuple(
    "{0}-seed{1}".format(dataset, seed)
    for dataset in DATASETS
    for seed in MODEL_SEEDS
)
FORMAL_STRATEGIES = ("degree",) + tuple(
    strategy for strategy in SCORE_NAMES if strategy != "degree"
)
BUDGET_RATIOS = APPROVED_BUDGET_RATIOS
PROJECT_EXECUTION_POLICY = {
    "required_branch": "main",
    "required_active_checkout": "/autodl-fs/data/OpenGU/GULib-master",
    "cuda": 0,
    "num_threads": 1,
    "paths": {
        "processed_root": "data/processed",
        "cache_v2_root": "results/cache_v2",
        "selection_output_root": "results/runs/target_direct_formal_v2/selection",
        "checkpoint_root": "results/runs/target_direct_formal_v2/checkpoints",
        "evidence_root": "results/runs/target_direct_formal_v2/evidence",
        "runtime_root": "results/runs/target_direct_formal_v2/runtime",
        "gu_run_root": "results/runs/target_direct_formal_v2/gu",
    },
}
OPERATIONAL_CONFIG_FIELDS = frozenset({
    "required_branch", "required_active_checkout", "required_device_name",
    "processed_root", "cache_v2_root", "selection_output_root",
    "checkpoint_root", "evidence_root", "runtime_root", "gu_run_root",
    "score_cache_root", "selection_store_root", "cuda", "device",
    "num_threads", "output",
})


class TargetDirectStageError(RuntimeError):
    """A reviewed formal stage or its evidence is invalid."""


def _scientific_references(config_path: Path, value: Mapping[str, Any]):
    """Resolve tracked method/evaluation tables; the large plan supplies shared axes."""
    root = config_path.parent.resolve()
    sources = {"selectors": [], "unlearnings": [], "evaluations": []}

    def referenced(field):
        refs = value.get(field)
        if not isinstance(refs, list) or not refs or any(not isinstance(item, str) for item in refs):
            raise TargetDirectStageError(field + " must be a nonempty list of YAML references")
        result = []
        for ref in refs:
            path = (root / ref).resolve()
            if root not in path.parents or not path.is_file():
                raise TargetDirectStageError(field + " contains an unavailable project reference")
            result.append((path, read_yaml(path)))
        return result

    selectors = []
    for path, item in referenced("selector_refs"):
        try:
            fields(item, {"kind", "schema_version", "method", "parameters"},
                   {"kind", "schema_version", "method"}, "formal selector")
        except ConfigurationError as exc:
            raise TargetDirectStageError(str(exc)) from exc
        if item["kind"] != "selector" or item["schema_version"] != 1:
            raise TargetDirectStageError("formal selector schema/version is invalid")
        try:
            parameters = resolve_parameters(item["method"], item.get("parameters"))
        except (KeyError, TypeError, ValueError) as exc:
            raise TargetDirectStageError(str(exc)) from exc
        if parameters != resolve_parameters(item["method"]):
            raise TargetDirectStageError(
                "formal selector parameters differ from the frozen method defaults"
            )
        selectors.append({"method": item["method"], "parameters": parameters})
        sources["selectors"].append(str(path))

    unlearnings = []
    for path, item in referenced("unlearning_refs"):
        try:
            fields(item, {"kind", "schema_version", "method", "parameters"},
                   {"kind", "schema_version", "method"}, "formal unlearning")
        except ConfigurationError as exc:
            raise TargetDirectStageError(str(exc)) from exc
        if (item["kind"] != "unlearning" or item["schema_version"] != 1
                or item["method"] not in ("GNNDelete", "Retrain") or item.get("parameters")):
            raise TargetDirectStageError("formal method table must select default GNNDelete or Retrain")
        unlearnings.append({"method": item["method"]})
        sources["unlearnings"].append(str(path))

    evaluations = []
    for path, item in referenced("evaluation_refs"):
        try:
            resolved = resolve_evaluation(item)
            require_consumer(resolved, "target_direct_syncmate_v2")
        except ValueError as exc:
            raise TargetDirectStageError(str(exc)) from exc
        evaluations.append(resolved)
        sources["evaluations"].append(str(path))
    return selectors, unlearnings, evaluations, sources


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _write_immutable_json(path: Path, value: Mapping[str, Any]) -> None:
    payload = _canonical_json(value)
    if path.exists():
        if path.read_bytes() != payload:
            raise TargetDirectStageError(
                "existing immutable JSON conflicts: {0}".format(path)
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-{0}".format(os.getpid()))
    try:
        temporary.write_bytes(payload)
        os.replace(str(temporary), str(path))
    finally:
        if temporary.exists():
            temporary.unlink()


def _git_state(root: Path) -> Dict[str, Any]:
    def run(*arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout.strip()

    return {
        "head": run("rev-parse", "HEAD"),
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "status_short": run(
            "status", "--short", "--untracked-files=all"
        ).splitlines(),
    }


def parse_stage(stage: str) -> Tuple[str, int]:
    if stage not in STAGES:
        raise TargetDirectStageError(
            "stage is outside the reviewed 3-dataset x 3-seed matrix"
        )
    dataset, seed_text = stage.rsplit("-seed", 1)
    return dataset, int(seed_text)


def ratio_key(ratio: float) -> str:
    value = float(ratio)
    if not any(abs(value - expected) < 1e-12 for expected in BUDGET_RATIOS):
        raise TargetDirectStageError(
            "ratio is outside the reviewed {0} budget set".format(
                list(BUDGET_RATIOS)
            )
        )
    return "{0:.2f}".format(value)


def ratio_token(ratio: float) -> str:
    return "r" + ratio_key(ratio)


def _expected_k(
    config: Mapping[str, Any], dataset: str, ratio: float
) -> int:
    return int(
        config["datasets"][dataset]["expected_k_by_ratio"][ratio_key(ratio)]
    )


def load_config(
    config_path: Path = CONFIG_PATH,
    *,
    repository_root: Optional[Path] = None,
) -> Dict[str, Any]:
    root = Path(repository_root or REPO_ROOT).resolve()
    path = Path(config_path).resolve()
    if path != (
        root / "experiments" / "configs" / CONFIG_PATH.name
    ).resolve():
        raise TargetDirectStageError("only the reviewed formal config is accepted")
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TargetDirectStageError("formal config root must be a mapping")
    forbidden = sorted(set(value) & OPERATIONAL_CONFIG_FIELDS)
    if forbidden:
        raise TargetDirectStageError(
            "scientific config contains SyncMate/project execution fields: {0}".format(
                forbidden
            )
        )
    try:
        split_contract = target_direct_split_contract(
            value,
            require_explicit=True,
        )
    except ProcessedArtifactError as exc:
        raise TargetDirectStageError(str(exc)) from exc
    selectors, unlearnings, evaluations, configuration_sources = (
        _scientific_references(path, value)
    )
    split_registration = value.get("split") or {}
    if (
        value.get("schema") != CONFIG_SCHEMA
        or value.get("version") != CONFIG_VERSION
        or "processed_profile" in value
        or split_registration.get("materialize_on_miss") is not True
        or value.get("base_model") != "GCN"
        or value.get("main_parameter_scope") != "last_layer"
        or tuple(float(item) for item in value.get("budget_ratios") or ())
        != BUDGET_RATIOS
        or value.get("budget_rounding") != "floor_with_minimum_one"
        or value.get("score_budget_semantics")
        != SCORE_BUDGET_SEMANTICS
        or tuple(value.get("budget_conditioned_strategies") or ()) != ()
        or tuple(value.get("seeds") or ()) != MODEL_SEEDS
        or tuple(item["method"] for item in selectors) != FORMAL_STRATEGIES
        or tuple(item["method"] for item in unlearnings) != ("GNNDelete", "Retrain")
        or tuple(item["case"] for item in evaluations)
        != ("post_unlearning_utility_and_retrain_gap",)
        or set(value.get("datasets") or {}) != set(DATASETS)
    ):
        raise TargetDirectStageError("formal target-direct config is not frozen")
    claims = value.get("claims") or {}
    if (
        claims.get("selector_and_gu_share_exact_checkpoint") is not True
        or claims.get("budget_denominator") != "train_candidate_count"
        or tuple(
            float(item) for item in claims.get("deletion_budget_ratios") or ()
        )
        != BUDGET_RATIOS
        or int(claims.get("method_score_compute_per_dataset_seed", -1)) != 1
        or claims.get("selection_artifact_identity_is_ratio_conditioned")
        is not True
        or claims.get("formal_matrix_scope") != "last_layer"
        or claims.get("old_public_or_surrogate_results_reusable") is not False
        or int(claims.get("formal_gate_cells", -1)) != 2
        or int(claims.get("candidate_full_matrix_cells", -1)) != 306
        or claims.get("candidate_full_matrix_authorized") is not False
        or claims.get("execution_scope") != "dual_budget_canary_only"
    ):
        raise TargetDirectStageError("formal claim boundary is not frozen")
    resolved = {}
    for key, registered in PROJECT_EXECUTION_POLICY["paths"].items():
        resolved[key] = resolve_owned_path(root, registered, key)
    expected_processed = (root / "data" / "processed").resolve()
    if resolved["processed_root"] != expected_processed:
        raise TargetDirectStageError("processed_root is not checkout-canonical")
    expected_cache_v2 = (root / "results" / "cache_v2").resolve()
    if resolved["cache_v2_root"] != expected_cache_v2:
        raise TargetDirectStageError(
            "cache_v2_root must resolve exactly to results/cache_v2"
        )
    for key in (
        "selection_output_root",
        "checkpoint_root",
        "evidence_root",
        "runtime_root",
        "gu_run_root",
    ):
        if (root / "results" / "runs").resolve() not in resolved[key].parents:
            raise TargetDirectStageError(key + " must be under results/runs")
    normalized_datasets = {}
    for dataset in DATASETS:
        item = value["datasets"][dataset]
        if not isinstance(item, Mapping):
            raise TargetDirectStageError("dataset registration must be a mapping")
        if any(
            key in item for key in ("expected_candidate_count", "expected_k_by_ratio")
        ):
            raise TargetDirectStageError(
                "candidate count and k must be derived from the split contract"
            )
        if int(item.get("num_nodes", -1)) != DATASET_NODE_COUNTS[dataset]:
            raise TargetDirectStageError(
                "registered node count changed for " + dataset
            )
        candidate_count = int(
            DATASET_NODE_COUNTS[dataset] * split_contract.train_ratio
        )
        normalized_datasets[dataset] = {
            **item,
            "expected_candidate_count": candidate_count,
            "expected_k_by_ratio": {
                ratio_key(ratio): max(1, int(candidate_count * float(ratio)))
                for ratio in BUDGET_RATIOS
            },
        }
    return {
        **value,
        "strategy_order": [item["method"] for item in selectors],
        "gu_method": unlearnings[0]["method"],
        "selector_instances": selectors,
        "unlearning_instances": unlearnings,
        "evaluation_instances": evaluations,
        "configuration_sources": configuration_sources,
        **{key: PROJECT_EXECUTION_POLICY[key]
           for key in ("required_branch", "required_active_checkout", "cuda", "num_threads")},
        "datasets": normalized_datasets,
        "repository_root": root,
        "config_path": path,
        "paths": resolved,
        "split_contract": split_contract,
    }


def _stage_paths(config: Mapping[str, Any], stage: str) -> Dict[str, Any]:
    dataset, seed = parse_stage(stage)
    cell_root = (
        Path(config["paths"]["selection_output_root"]) / "cells" / stage
    )
    evidence_root = Path(config["paths"]["evidence_root"])
    return {
        "cold": {
            ratio_key(ratio): cell_root
            / "cold-{0}.json".format(ratio_token(ratio))
            for ratio in BUDGET_RATIOS
        },
        "warm": {
            ratio_key(ratio): cell_root
            / "warm-{0}.json".format(ratio_token(ratio))
            for ratio in BUDGET_RATIOS
        },
        "receipt": cell_root / "cell.json",
        "score_store": Path(config["paths"]["cache_v2_root"]),
        "selection_store": Path(config["paths"]["cache_v2_root"]),
        "checkpoint": Path(config["paths"]["checkpoint_root"])
        / "{0}_seed{1}_target.pt".format(dataset, seed),
        "manifest": {
            ratio_key(ratio): evidence_root
            / "manifests"
            / ratio_token(ratio)
            / (stage + ".json")
            for ratio in BUDGET_RATIOS
        },
        "gu_config": {
            ratio_key(ratio): evidence_root
            / "configs"
            / ratio_token(ratio)
            / (stage + ".yaml")
            for ratio in BUDGET_RATIOS
        },
        "logs": evidence_root / "logs" / stage,
    }


def selection_artifacts(
    stage: str, config: Optional[Mapping[str, Any]] = None
) -> Tuple[str, ...]:
    cfg = dict(config or load_config())
    root = Path(cfg["repository_root"])
    paths = _stage_paths(cfg, stage)
    artifacts = []
    for key in ("cold", "warm"):
        artifacts.extend(
            paths[key][ratio_key(ratio)].relative_to(root).as_posix()
            for ratio in BUDGET_RATIOS
        )
    artifacts.append(paths["receipt"].relative_to(root).as_posix())
    return tuple(artifacts)


def gu_artifacts(
    stage: str,
    *,
    ratio: float,
    gate_only: bool = False,
    config: Optional[Mapping[str, Any]] = None,
) -> Tuple[str, ...]:
    cfg = dict(config or load_config())
    root = Path(cfg["repository_root"])
    dataset, seed = parse_stage(stage)
    strategies = ("degree",) if gate_only else FORMAL_STRATEGIES
    paths = []
    for method in (item['method'] for item in cfg['unlearning_instances']):
        for strategy in strategies:
            leaf = (
                Path(cfg["paths"]["gu_run_root"])
                / "{0}_GCN_{1}".format(dataset, ratio_token(ratio))
                / "{0}_{1}".format(method, strategy)
                / "seed{0}".format(seed)
            )
            paths.extend(
                (leaf / name).relative_to(root).as_posix()
                for name in ARTIFACT_NAMES
            )
    return tuple(paths)


def _profile(
    config: Mapping[str, Any],
    dataset: str,
    *,
    allow_materialize: bool,
) -> Mapping[str, Any]:
    display_name = str(config["datasets"][dataset]["display_name"])
    contract = config["split_contract"]
    profile_loader = (
        stage_profile
        if allow_materialize
        and (config.get("split") or {}).get("materialize_on_miss") is True
        else verify_profile
    )
    profile = profile_loader(
        repository_root=Path(config["repository_root"]),
        processed_root=Path(config["paths"]["processed_root"]),
        dataset=display_name,
        contract=contract,
    )
    observed_count = int(profile["inputs"].candidate_count)
    expected = config["datasets"][dataset]
    observed_k_by_ratio = {
        ratio_key(ratio): max(1, int(observed_count * float(ratio)))
        for ratio in BUDGET_RATIOS
    }
    if observed_count != int(expected["expected_candidate_count"]):
        raise TargetDirectStageError(
            "derived candidate count differs from the reviewed expectation"
        )
    for ratio in BUDGET_RATIOS:
        key = ratio_key(ratio)
        if observed_k_by_ratio[key] != _expected_k(config, dataset, ratio):
            raise TargetDirectStageError(
                "derived k differs from the reviewed expectation at ratio "
                + key
            )
    return profile


def _formal_preflight(
    config: Mapping[str, Any],
    stage: str,
    *,
    require_gpu: bool = True,
) -> Dict[str, Any]:
    errors = []
    dataset, seed = parse_stage(stage)
    git = _git_state(Path(config["repository_root"]))
    if git["branch"] != config["required_branch"] or git["status_short"]:
        errors.append("formal execution requires a clean main checkout")
    required_checkout = Path(str(config["required_active_checkout"]))
    if Path(config["repository_root"]) != required_checkout:
        errors.append(
            "formal execution requires active checkout {0}".format(
                required_checkout
            )
        )
    gpu = {
        "required": require_gpu,
        "available": bool(torch.cuda.is_available()),
        "device_name": None,
    }
    if require_gpu:
        if not torch.cuda.is_available():
            errors.append("CUDA GPU is not available")
        else:
            gpu["device_name"] = str(torch.cuda.get_device_name(int(config["cuda"])))
    profile = None
    try:
        profile = _profile(config, dataset, allow_materialize=not errors)
    except Exception as exc:
        errors.append("processed profile: {0}".format(exc))
    return {
        "ready": not errors,
        "stage": stage,
        "dataset": dataset,
        "seed": seed,
        "git": git,
        "gpu": gpu,
        "profile_manifest": None if profile is None else profile["manifest_path"],
        "errors": errors,
    }


def _load_summary(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TargetDirectStageError("selection summary root is not an object")
    return value


def _validate_selection_pair(
    config: Mapping[str, Any], stage: str, expected_head: str
) -> Dict[str, Any]:
    """Validate one shared cold method Scores and two ratio projections."""

    dataset, seed = parse_stage(stage)
    paths = _stage_paths(config, stage)
    summaries: Dict[Tuple[str, str], Mapping[str, Any]] = {}
    score_identities = {name: set() for name in SCORE_NAMES}
    checkpoint_identities = set()
    ratio_results = {}
    score_warm_reads = {}

    for position, ratio in enumerate(BUDGET_RATIOS):
        key = ratio_key(ratio)
        expected_k = _expected_k(config, dataset, ratio)
        cold = _load_summary(paths["cold"][key])
        warm = _load_summary(paths["warm"][key])
        summaries[(key, "cold")] = cold
        summaries[(key, "warm")] = warm
        for label, summary in (("cold", cold), ("warm", warm)):
            budget = summary.get("budget") or {}
            projection = summary.get("budget_projection") or {}
            if (
                summary.get("schema")
                != "target_direct_v1.selection_summary"
                or summary.get("version") != 3
                or (summary.get("status") or {}).get("state") != "success"
                or str(summary.get("dataset", "")).lower() != dataset
                or int(summary.get("seed", -1)) != seed
                or summary.get("processed_profile")
                != config["split_contract"].processed_profile
                or summary.get("split_contract")
                != config["split_contract"].to_manifest()
                or summary.get("parameter_scope") != "last_layer"
                or float(budget.get("requested_ratio", -1)) != float(ratio)
                or budget.get("denominator") != "train_candidate_count"
                or budget.get("rounding") != "floor_with_minimum_one"
                or int(budget.get("denominator_count", -1))
                != int(config["datasets"][dataset]["expected_candidate_count"])
                or int(budget.get("expected_k", -1)) != expected_k
                or projection.get("score_semantics")
                != SCORE_BUDGET_SEMANTICS
                or tuple(
                    float(item)
                    for item in projection.get("supported_ratios") or ()
                )
                != BUDGET_RATIOS
                or projection.get("budget_conditioned_strategies") != []
                or projection.get("method_scores_shared_across_ratios")
                is not True
                or projection.get("selection_artifact_ratio_conditioned")
                is not True
                or (summary.get("git_provenance") or {}).get("head")
                != expected_head
                or (summary.get("git_provenance") or {}).get(
                    "worktree_dirty"
                )
                is not False
                or set(summary.get("selection_artifacts") or {})
                != set(SCORE_NAMES)
            ):
                raise TargetDirectStageError(
                    "{0} {1} target-direct summary identity mismatch".format(
                        key, label
                    )
                )

            scores = summary.get("method_scores") or {}
            if set(scores) != set(SCORE_NAMES):
                raise TargetDirectStageError('method Score set is incomplete')
            checkpoint = summary.get("target_checkpoint") or {}
            for name, score in scores.items():
                timing_key = 'warm_read_seconds' if score.get('hit') is True else 'cold_total_seconds'
                timing = score.get(timing_key)
                digest = score.get('recipe_hash')
                if (type(score.get('hit')) is not bool or score.get('producer_called') is not (not score['hit'])
                        or not isinstance(digest, str) or len(digest) != 64
                        or any(c not in '0123456789abcdef' for c in digest)
                        or not score.get('artifact_id') or type(timing) not in (int, float)
                        or not math.isfinite(timing) or timing < 0):
                    raise TargetDirectStageError(name + ' method Score identity/timing is incomplete')
                score_identities[name].add((score.get('artifact_id'), score.get('recipe_hash')))
            checkpoint_identities.add(
                (checkpoint.get("file_sha256"), checkpoint.get("state_hash"))
            )

        cold_score_hit = all(item.get("hit") is True for item in cold["method_scores"].values())
        expected_cold_score_hit = position != 0
        if any(item.get("hit") is not expected_cold_score_hit for item in cold["method_scores"].values()):
            raise TargetDirectStageError(
                "{0} cold method Scores sharing outcome changed".format(key)
            )
        if any(item.get("hit") is not True or item.get("producer_called") is not False for item in warm["method_scores"].values()):
            raise TargetDirectStageError(
                "{0} warm method Scores was not an exact hit".format(key)
            )
        cold_timings = (
            (cold.get("selection_cache") or {}).get("method_timings") or {}
        )
        warm_timings = (
            (warm.get("selection_cache") or {}).get("method_timings") or {}
        )
        if (
            set(cold_timings) != set(SCORE_NAMES)
            or set(warm_timings) != set(SCORE_NAMES)
        ):
            raise TargetDirectStageError(
                "{0} selection timing method set is not 17".format(key)
            )
        if any(
            item.get("cache_hit") is not False
            or item.get("selection_projection_cache_hit") is not False
            or not isinstance(
                item.get("cold_selection_projection_seconds"), (int, float)
            )
            for item in cold_timings.values()
        ):
            raise TargetDirectStageError(
                "{0} cold Selection projection unexpectedly hit".format(key)
            )
        if any(
            item.get("cache_hit") is not True
            or item.get("selection_projection_cache_hit") is not True
            for item in warm_timings.values()
        ):
            raise TargetDirectStageError(
                "{0} warm Selection Artifact was not an exact hit".format(key)
            )
        if cold_score_hit:
            score_warm_reads[key + "_cold_projection"] = (
                sum(item["warm_read_seconds"] for item in cold["method_scores"].values())
            )
        score_warm_reads[key + "_warm"] = (
            sum(item["warm_read_seconds"] for item in warm["method_scores"].values())
        )
        ratio_results[key] = {
            "ratio": float(ratio),
            "k": expected_k,
            "cold_method_scores_hit": bool(cold_score_hit),
            "cold_method_timings": cold_timings,
            "warm_method_timings": warm_timings,
            "failure_state": cold["status"],
            "cold_sha256": _sha256_file(paths["cold"][key]),
            "warm_sha256": _sha256_file(paths["warm"][key]),
        }

    if any(len(values) != 1 or None in next(iter(values)) for values in score_identities.values()):
        raise TargetDirectStageError(
            "1%/5% summaries do not share one exact method Scores identity"
        )
    if len(checkpoint_identities) != 1 or None in next(
        iter(checkpoint_identities)
    ):
        raise TargetDirectStageError(
            "1%/5% summaries do not share one exact target checkpoint"
        )
    first_key = ratio_key(BUDGET_RATIOS[0])
    first_cold = summaries[(first_key, "cold")]
    first_checkpoint = first_cold["target_checkpoint"]
    first_score = {"cold_total_seconds": sum(item["cold_total_seconds"] for item in first_cold["method_scores"].values())}
    if not isinstance(first_score.get("cold_total_seconds"), (int, float)):
        raise TargetDirectStageError(
            "shared cold method Scores total timing is missing"
        )
    if any(
        not isinstance(value, (int, float))
        for value in score_warm_reads.values()
    ):
        raise TargetDirectStageError("shared method Scores warm timing is missing")
    gpu = first_cold.get("gpu_memory") or {}
    device_name = str(
        ((gpu.get("method_scores") or {}).get("device_name")) or ""
    )
    peak_allocated = int(gpu.get("process_peak_allocated_bytes") or 0)
    peak_reserved = int(gpu.get("process_peak_reserved_bytes") or 0)
    if not device_name or peak_allocated <= 0 or peak_reserved <= 0:
        raise TargetDirectStageError("selection GPU evidence is incomplete")
    return {
        "schema": RECEIPT_SCHEMA,
        "version": RECEIPT_VERSION,
        "dataset": config["datasets"][dataset]["display_name"],
        "seed": seed,
        "status": "success",
        "experiment_git_sha": expected_head,
        "parameter_scope": "last_layer",
        "processed_profile": config["split_contract"].processed_profile,
        "split_contract": config["split_contract"].to_manifest(),
        "candidate_count": int(first_cold["candidate_count"]),
        "budget_ratios": list(BUDGET_RATIOS),
        "expected_k_by_ratio": {
            ratio_key(ratio): _expected_k(config, dataset, ratio)
            for ratio in BUDGET_RATIOS
        },
        "formal_score_count": len(SCORE_NAMES),
        "score_budget_semantics": SCORE_BUDGET_SEMANTICS,
        "budget_conditioned_strategies": [],
        "method_score_identities": {name: {'artifact_id': next(iter(values))[0], 'recipe_hash': next(iter(values))[1]} for name, values in score_identities.items()},
        "method_scores_cold_total_seconds": first_score[
            "cold_total_seconds"
        ],
        "method_scores_warm_read_seconds": score_warm_reads,
        "ratio_results": ratio_results,
        "target_checkpoint": {
            "path": first_checkpoint["path"],
            "file_sha256": first_checkpoint["file_sha256"],
            "state_hash": first_checkpoint["state_hash"],
        },
        "device_name": device_name,
        "peak_gpu_allocated_bytes": peak_allocated,
        "peak_gpu_reserved_bytes": peak_reserved,
    }


def preflight_selection(
    stage: str,
    config_path: Path = CONFIG_PATH,
    *,
    repository_root: Optional[Path] = None,
    require_gpu: bool = True,
) -> Dict[str, Any]:
    try:
        config = load_config(config_path, repository_root=repository_root)
    except Exception as exc:
        return {"ready": False, "stage": stage, "errors": [str(exc)]}
    result = _formal_preflight(config, stage, require_gpu=require_gpu)
    paths = _stage_paths(config, stage)
    if paths["receipt"].is_file():
        try:
            expected = _validate_selection_pair(
                config, stage, result["git"]["head"]
            )
            if json.loads(paths["receipt"].read_text(encoding="utf-8")) != expected:
                result["errors"].append("selection receipt conflicts with evidence")
            else:
                result["resumed"] = True
        except Exception as exc:
            result["errors"].append("selection resume evidence: {0}".format(exc))
    elif any(
        path.exists()
        for path in (
            *paths["cold"].values(),
            *paths["warm"].values(),
            paths["score_store"],
            paths["selection_store"],
            paths["checkpoint"],
        )
    ):
        result["errors"].append(
            "partial cold selection state exists without an accepted receipt"
        )
    result["ready"] = not result["errors"]
    return result


def _run_command(command: Sequence[str], log_prefix: Path) -> subprocess.CompletedProcess:
    completed = subprocess.run(
        list(command),
        cwd=str(REPO_ROOT),
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHON_BIN": sys.executable,
        },
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    log_prefix.parent.mkdir(parents=True, exist_ok=True)
    log_prefix.with_suffix(".stdout.log").write_text(
        completed.stdout, encoding="utf-8"
    )
    log_prefix.with_suffix(".stderr.log").write_text(
        completed.stderr, encoding="utf-8"
    )
    if completed.returncode != 0:
        raise TargetDirectStageError(
            "subprocess failed with rc={0}: {1}".format(
                completed.returncode, " ".join(command[:4])
            )
        )
    return completed


def execute_selection(
    stage: str, config_path: Path = CONFIG_PATH
) -> Dict[str, Any]:
    config = load_config(config_path)
    preflight = preflight_selection(stage, config_path)
    if not preflight["ready"]:
        return {
            "passed": False,
            "stage": stage,
            "preflight": preflight,
            "generated_artifacts": [],
            "errors": preflight["errors"],
        }
    if preflight.get("resumed"):
        return {
            "passed": True,
            "stage": stage,
            "resumed": True,
            "preflight": preflight,
            "generated_artifacts": list(selection_artifacts(stage, config)),
            "errors": [],
        }
    dataset, seed = parse_stage(stage)
    paths = _stage_paths(config, stage)
    display_name = config["datasets"][dataset]["display_name"]
    base = [
        sys.executable,
        "-m",
        "experiments.target_direct_v1.run_selection",
        "--dataset",
        str(display_name),
        "--processed-root",
        str(config["paths"]["processed_root"]),
        "--train-ratio",
        str(config["split_contract"].train_ratio),
        "--val-ratio",
        str(config["split_contract"].val_ratio),
        "--test-ratio",
        str(config["split_contract"].test_ratio),
        "--split-seed",
        str(config["split_contract"].split_seed),
        "--materialize-split-on-miss",
        "--runtime-root",
        str(config["paths"]["runtime_root"]),
        "--cache-root",
        str(paths["score_store"]),
        "--selection-cache-root",
        str(paths["selection_store"]),
        "--checkpoint-path",
        str(paths["checkpoint"]),
        "--seed",
        str(seed),
        "--cuda",
        str(config["cuda"]),
        "--num-threads",
        str(config["num_threads"]),
        "--epochs",
        str(config["epochs"]),
        "--checkpoint-epochs",
        ",".join(str(value) for value in config["checkpoint_epochs"]),
        "--gcn-num-layers",
        str(config["gcn_num_layers"]),
        "--gcn-hidden",
        str(config["gcn_hidden"]),
        "--parameter-scope",
        "last_layer",
        "--experiment-git-sha",
        preflight["git"]["head"],
    ]
    for position, ratio in enumerate(BUDGET_RATIOS):
        key = ratio_key(ratio)
        paths["cold"][key].parent.mkdir(parents=True, exist_ok=True)
        command = [
            *base,
            "--ratio",
            key,
            "--output",
            str(paths["cold"][key]),
        ]
        if position:
            command.extend(
                ["--reuse-checkpoint", "--fail-if-score-producer-called"]
            )
        _run_command(
            command,
            paths["logs"] / "selection_cold_{0}".format(ratio_token(ratio)),
        )
    for ratio in BUDGET_RATIOS:
        key = ratio_key(ratio)
        _run_command(
            [
                *base,
                "--ratio",
                key,
                "--output",
                str(paths["warm"][key]),
                "--reuse-checkpoint",
                "--fail-if-producer-called",
            ],
            paths["logs"] / "selection_warm_{0}".format(ratio_token(ratio)),
        )
    receipt = _validate_selection_pair(
        config, stage, preflight["git"]["head"]
    )
    _write_immutable_json(paths["receipt"], receipt)
    return {
        "passed": True,
        "stage": stage,
        "resumed": False,
        "preflight": preflight,
        "receipt": receipt,
        "generated_artifacts": list(selection_artifacts(stage, config)),
        "errors": [],
    }


def _ensure_gu_inputs(
    config: Mapping[str, Any],
    stage: str,
    ratio: float,
    expected_head: str,
) -> Mapping[str, Any]:
    dataset, seed = parse_stage(stage)
    key = ratio_key(ratio)
    paths = _stage_paths(config, stage)
    receipt = _validate_selection_pair(config, stage, expected_head)
    if (
        not paths["receipt"].is_file()
        or json.loads(paths["receipt"].read_text(encoding="utf-8")) != receipt
    ):
        raise TargetDirectStageError("accepted selection receipt is missing")
    manifest = build_manifest(
        repository_root=Path(config["repository_root"]),
        processed_root=Path(config["paths"]["processed_root"]),
        selection_store_root=paths["selection_store"],
        dataset=config["datasets"][dataset]["display_name"],
        summaries=[paths["cold"][key]],
        expected_git_sha=expected_head,
        ratio=float(ratio),
        required_seeds=(seed,),
        required_parameter_scope="last_layer",
        strategy_order=FORMAL_STRATEGIES,
        split_contract=config["split_contract"],
    )
    _write_immutable_json(paths["manifest"][key], manifest)
    gu_config = build_gu_config(
        manifest_path=paths["manifest"][key],
        processed_root=Path(config["paths"]["processed_root"]),
        runtime_root=Path(config["paths"]["runtime_root"])
        / ratio_token(ratio)
        / stage,
        run_root=Path(config["paths"]["gu_run_root"]),
        unlearning_refs=config["configuration_sources"]["unlearnings"],
    )
    yaml_payload = yaml.safe_dump(
        gu_config, sort_keys=False, allow_unicode=True
    )
    if paths["gu_config"][key].exists():
        if yaml.safe_load(
            paths["gu_config"][key].read_text(encoding="utf-8")
        ) != gu_config:
            raise TargetDirectStageError("existing GU config conflicts")
    else:
        paths["gu_config"][key].parent.mkdir(parents=True, exist_ok=True)
        paths["gu_config"][key].write_text(yaml_payload, encoding="utf-8")
    return manifest


def _validate_gu(
    config: Mapping[str, Any],
    stage: str,
    ratio: float,
    manifest: Mapping[str, Any],
    *,
    gate_only: bool,
    expected_head: str,
) -> Dict[str, Any]:
    dataset, seed = parse_stage(stage)
    strategies = ("degree",) if gate_only else FORMAL_STRATEGIES
    cells = {
        (str(cell["strategy"]), int(cell["seed"])): cell
        for cell in manifest["cells"]
    }
    accepted = []
    for method in (item['method'] for item in config['unlearning_instances']):
        for strategy in strategies:
            leaf = (
                Path(config["paths"]["gu_run_root"])
                / "{0}_GCN_{1}".format(dataset, ratio_token(ratio))
                / "{0}_{1}".format(method, strategy)
                / "seed{0}".format(seed)
            )
            missing = [name for name in ARTIFACT_NAMES if not (leaf / name).is_file()]
            if missing:
                raise TargetDirectStageError(
                    "GU leaf is incomplete for {0}: {1}".format(strategy, missing)
                )
            attack = json.loads((leaf / "attack.json").read_text(encoding="utf-8"))
            attack_row = (attack.get("results") or {}).get(strategy) or {}
            if not attack_row or attack_row.get("failed") is True:
                raise TargetDirectStageError("GU attack failed for " + strategy)
            meta = json.loads((leaf / "_meta.json").read_text(encoding="utf-8"))
            artifact = meta.get("selection_artifact") or {}
            expected_cell = cells[(strategy, seed)]
            expected_artifact = expected_cell["artifact"]
            expected_checkpoint = expected_cell["target_checkpoint"]
            if (
                meta.get("git_sha") != expected_head
                or meta.get("method") != method
                or meta.get("strategy") != strategy
                or int(meta.get("seed", -1)) != seed
                or float(artifact.get("ratio", -1)) != float(ratio)
                or artifact.get("artifact_id")
                != expected_artifact["artifact_id"]
                or artifact.get("recipe_hash")
                != expected_artifact["recipe_hash"]
                or artifact.get("content_hash")
                != expected_artifact["content_hash"]
                or int(artifact.get("k", -1)) != int(expected_cell["k"])
                or float(expected_cell.get("ratio", -1)) != float(ratio)
                or artifact.get("authoritative") is not True
                or (artifact.get("target_checkpoint") or {}).get("state_hash")
                != expected_checkpoint["state_hash"]
                or (artifact.get("target_checkpoint") or {}).get("file_sha256")
                != expected_checkpoint["file_sha256"]
            ):
                raise TargetDirectStageError(
                    "GU target-direct provenance mismatch for " + strategy
                )
            from experiments.unlearning_outputs import load_output
            from experiments.output_metrics import evaluate_method
            reference = meta.get('output_reference')
            payload = load_output(reference, config['paths']['cache_v2_root'])
            if payload.identity['target']['method'] != method:
                raise TargetDirectStageError('method output identity mismatch')
            if payload.identity['selection'] != {key: artifact[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}:
                raise TargetDirectStageError('method output Selection mismatch')
            if (leaf / 'predictions.npz').read_bytes() != payload.canonical_bytes:
                raise TargetDirectStageError('collected predictions differ from the immutable output')
            if attack_row.get('evaluation') != evaluate_method(reference, payload):
                raise TargetDirectStageError('single-method metrics differ from saved predictions')
            accepted.append(
                {
                    "strategy": strategy,
                    "ratio": float(ratio),
                    "k": int(expected_cell["k"]),
                    "selection_artifact_id": artifact["artifact_id"],
                    "target_checkpoint_state_hash": expected_checkpoint["state_hash"],
                    "attack": attack_row,
                    "method": method,
                    "output_reference": reference,
                }
            )
    return {"accepted_cells": len(accepted), "cells": accepted}


def preflight_gu(
    stage: str,
    ratio: float,
    config_path: Path = CONFIG_PATH,
    *,
    gate_only: bool = False,
    repository_root: Optional[Path] = None,
    require_gpu: bool = True,
) -> Dict[str, Any]:
    try:
        config = load_config(config_path, repository_root=repository_root)
    except Exception as exc:
        return {
            "ready": False,
            "stage": stage,
            "ratio": ratio,
            "errors": [str(exc)],
        }
    ratio = float(ratio_key(ratio))
    result = _formal_preflight(config, stage, require_gpu=require_gpu)
    result["ratio"] = ratio
    result["gate_only"] = gate_only
    paths = _stage_paths(config, stage)
    try:
        receipt = _validate_selection_pair(
            config, stage, result["git"]["head"]
        )
        if (
            not paths["receipt"].is_file()
            or json.loads(paths["receipt"].read_text(encoding="utf-8"))
            != receipt
        ):
            raise TargetDirectStageError(
                "accepted selection receipt is missing or changed"
            )
    except Exception as exc:
        result["errors"].append("selection prerequisite: {0}".format(exc))
    if not gate_only:
        if (
            (config.get("claims") or {}).get(
                "candidate_full_matrix_authorized"
            )
            is not True
        ):
            result["errors"].append(
                "306-cell candidate expansion is not authorized"
            )
        for gate_ratio in BUDGET_RATIOS:
            gate_paths = gu_artifacts(
                "cora-seed42",
                ratio=gate_ratio,
                gate_only=True,
                config=config,
            )
            if any(
                not (Path(config["repository_root"]) / relative).is_file()
                for relative in gate_paths
            ):
                result["errors"].append(
                    "{0} formal degree gate has not completed".format(
                        ratio_key(gate_ratio)
                    )
                )
    result["ready"] = not result["errors"]
    return result


def execute_gu(
    stage: str,
    ratio: float,
    config_path: Path = CONFIG_PATH,
    *,
    gate_only: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    if gate_only and stage != "cora-seed42":
        raise TargetDirectStageError("the reviewed gate is Cora seed42 only")
    ratio = float(ratio_key(ratio))
    config = load_config(config_path)
    preflight = preflight_gu(
        stage, ratio, config_path, gate_only=gate_only
    )
    if not preflight["ready"]:
        return {
            "passed": False,
            "stage": stage,
            "ratio": ratio,
            "gate_only": gate_only,
            "dry_run": dry_run,
            "preflight": preflight,
            "generated_artifacts": [],
            "errors": preflight["errors"],
        }
    manifest = _ensure_gu_inputs(
        config, stage, ratio, preflight["git"]["head"]
    )
    paths = _stage_paths(config, stage)
    key = ratio_key(ratio)
    command = [
        sys.executable,
        "experiments/run.py",
        str(paths["gu_config"][key]),
    ]
    if dry_run:
        command.append("--dry_run")
    elif gate_only:
        command.extend(["--strategy", "degree"])
    started = time.perf_counter()
    completed = _run_command(
        command,
        paths["logs"]
        / (
            "gu_dry_run"
            if dry_run
            else ("gu_gate" if gate_only else "gu_stage")
        ),
    )
    if dry_run:
        return {
            "passed": True,
            "stage": stage,
            "gate_only": gate_only,
            "dry_run": True,
            "preflight": preflight,
            "command": command,
            "stdout": completed.stdout,
            "generated_artifacts": [],
            "errors": [],
        }
    validation = _validate_gu(
        config,
        stage,
        ratio,
        manifest,
        gate_only=gate_only,
        expected_head=preflight["git"]["head"],
    )
    return {
        "schema": "target_direct_v1.syncmate_gu_result",
        "version": 2,
        "passed": True,
        "stage": stage,
        "ratio": ratio,
        "gate_only": gate_only,
        "dry_run": False,
        "git_sha": preflight["git"]["head"],
        "hostname": socket.gethostname(),
        "elapsed_seconds": time.perf_counter() - started,
        "manifest_path": str(paths["manifest"][key]),
        "manifest_sha256": _sha256_file(paths["manifest"][key]),
        "config_path": str(paths["gu_config"][key]),
        "config_sha256": _sha256_file(paths["gu_config"][key]),
        "validation": validation,
        "generated_artifacts": list(
            gu_artifacts(
                stage,
                ratio=ratio,
                gate_only=gate_only,
                config=config,
            )
        ),
        "errors": [],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--action", choices=("selection", "gu"), required=True
    )
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument(
        "--ratio", type=float, choices=BUDGET_RATIOS, default=None
    )
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    parser.add_argument("--gate-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.action == "selection":
            if args.gate_only or args.dry_run or args.ratio is not None:
                raise TargetDirectStageError(
                    "selection does not accept ratio, gate-only, or dry-run"
                )
            payload = (
                preflight_selection(args.stage, args.config)
                if args.preflight_only
                else execute_selection(args.stage, args.config)
            )
        else:
            if args.ratio is None:
                raise TargetDirectStageError(
                    "GU action requires an explicit reviewed ratio"
                )
            payload = (
                preflight_gu(
                    args.stage,
                    args.ratio,
                    args.config,
                    gate_only=args.gate_only,
                )
                if args.preflight_only
                else execute_gu(
                    args.stage,
                    args.ratio,
                    args.config,
                    gate_only=args.gate_only,
                    dry_run=args.dry_run,
                )
            )
    except Exception as exc:
        payload = {
            "passed": False,
            "ready": False,
            "stage": args.stage,
            "ratio": args.ratio,
            "generated_artifacts": [],
            "errors": ["{0}: {1}".format(type(exc).__name__, exc)],
        }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, default=str))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0 if payload.get("passed", payload.get("ready", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
