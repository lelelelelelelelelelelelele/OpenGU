from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from experiments.target_direct_v1 import target_direct_split_contract


RUNNER_AGENT_MAX_TIMEOUT_SECONDS = 21600
RUNNER_RECIPE_INTRODUCED_SHA = "3331c641ce16d0d7a3def66b0e302dd4a39a919c"
RUNNER_RECIPE_ALLOWED_TOOL_DELTA = (
    "GULib-master/scripts/syncmate/",
    "GULib-master/tests/test_syncmate.py",
    "GULib-master/docs/syncmate_bounded_runner_agent_ACCEPTANCE_REPORT.",
)
GATE4_RECIPE_BASE_SHA = "dbe79efd8fd70a9a455a8055a6627bd0bd95ed0e"
GATE4_RECIPE_ALLOWED_DELTA = (
    "GULib-master/attack/pipeline_adapter.py",
    "GULib-master/config.py",
    "GULib-master/dataset/original_dataset.py",
    "GULib-master/experiments/run.py",
    "GULib-master/experiments/configs/cache_v2_gate4_cora_degree_canary.yaml",
    "GULib-master/experiments/processed_provider.py",
    "GULib-master/parameter_parser.py",
    "GULib-master/scripts/cache_v2_gate4_canary.py",
    "GULib-master/scripts/syncmate/syncmate.py",
    "GULib-master/tests/test_auto_report_v3.py",
    "GULib-master/tests/test_cache_v2_gate4_canary.py",
    "GULib-master/tests/test_demo.py",
    "GULib-master/tests/test_experiment_processed_provider.py",
    "GULib-master/tests/test_phase_b_invariants.py",
    "GULib-master/tests/test_syncmate.py",
    "GULib-master/utils/dataset_utils.py",
    "GULib-master/utils/logger.py",
)

TARGET_DIRECT_RECIPE_INTRODUCED_SHA = "264b38995cebc84d10402d8113ea949ca2cfa34f"
TARGET_DIRECT_CONFIG = "experiments/configs/syncmate_target_direct_formal_v2.yaml"
TARGET_DIRECT_CONFIG_SHA256 = "639597a62e29f7ab35569c0ae0c668ac7e55044dce494c445d40b908aec2d380"
TARGET_DIRECT_SELECTION_OUTPUT_ROOT = "results/runs/target_direct_formal_v2/selection"
TARGET_DIRECT_GU_OUTPUT_ROOT = "results/runs/target_direct_formal_v2/gu"
TARGET_DIRECT_SELECTION_ARTIFACT_NAMES = (
    "cold-r0.01.json", "cold-r0.05.json",
    "warm-r0.01.json", "warm-r0.05.json", "cell.json",
)
TARGET_DIRECT_GU_ARTIFACT_NAMES = (
    "attack.json", "collateral.json", "predictions.npz", "_meta.json",
)
TARGET_DIRECT_DATASETS = ("cora", "citeseer", "pubmed")
TARGET_DIRECT_DATASET_DISPLAY = {
    "cora": "Cora", "citeseer": "CiteSeer", "pubmed": "PubMed",
}
TARGET_DIRECT_RATIOS = (0.01, 0.05)


def _target_direct_split_registration() -> tuple[dict[str, Any], dict[str, int]]:
    path = Path(__file__).resolve().parents[2] / TARGET_DIRECT_CONFIG
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    contract = target_direct_split_contract(value, require_explicit=True)
    datasets = value.get("datasets") or {}
    candidate_counts = {
        dataset: int(int(datasets[dataset]["num_nodes"]) * contract.train_ratio)
        for dataset in TARGET_DIRECT_DATASETS
    }
    return contract.to_manifest(), candidate_counts


TARGET_DIRECT_SPLIT_CONTRACT, TARGET_DIRECT_CANDIDATE_COUNTS = (
    _target_direct_split_registration()
)
TARGET_DIRECT_K_BY_RATIO = {
    dataset: {
        f"{ratio:.2f}": max(1, int(candidate_count * ratio))
        for ratio in TARGET_DIRECT_RATIOS
    }
    for dataset, candidate_count in TARGET_DIRECT_CANDIDATE_COUNTS.items()
}
TARGET_DIRECT_SEEDS = (42, 212, 2024)
TARGET_DIRECT_STRATEGIES = (
    "degree", "a_grad_norm", "b_param_hutch", "gt_full", "gt_simple",
    "legacy", "p_graph", "p_point", "p_simple", "r_point", "random",
    "tracin_cp_graph_3", "tracin_cp_graph_6", "tracin_cp_point_3",
    "tracin_cp_point_6", "tracin_cp_simple_3", "tracin_cp_simple_6",
)
TARGET_DIRECT_STAGES = tuple(
    f"{dataset}-seed{seed}"
    for dataset in TARGET_DIRECT_DATASETS
    for seed in TARGET_DIRECT_SEEDS
)


def _target_ratio_key(ratio: float) -> str:
    if float(ratio) not in TARGET_DIRECT_RATIOS:
        raise ValueError("unsupported target-direct ratio")
    return f"{float(ratio):.2f}"


def _target_ratio_id(ratio: float) -> str:
    return "r001" if float(ratio) == 0.01 else "r005"


def _target_direct_selection_artifacts(stage: str) -> tuple[str, ...]:
    leaf = f"{TARGET_DIRECT_SELECTION_OUTPUT_ROOT}/cells/{stage}"
    return tuple(f"{leaf}/{name}" for name in TARGET_DIRECT_SELECTION_ARTIFACT_NAMES)


def _target_direct_ratio_key(ratio: float) -> str:
    return _target_ratio_key(ratio)


def _target_direct_ratio_id(ratio: float) -> str:
    return _target_ratio_id(ratio)


def _target_selection_recipe(stage: str) -> dict[str, Any]:
    dataset, seed_text = stage.rsplit("-seed", 1)
    seed = int(seed_text)
    leaf = f"{TARGET_DIRECT_SELECTION_OUTPUT_ROOT}/cells/{stage}"
    artifacts = tuple(f"{leaf}/{name}" for name in TARGET_DIRECT_SELECTION_ARTIFACT_NAMES)
    return {
        "id": f"opengu-target-direct-selection-{stage}-v2",
        "argv": ("{python}", "-m", "experiments.target_direct_v1.syncmate_stage", "--config", TARGET_DIRECT_CONFIG, "--action", "selection", "--stage", stage, "--json"),
        "config_path": TARGET_DIRECT_CONFIG,
        "config_sha256": TARGET_DIRECT_CONFIG_SHA256,
        "recipe_introduced_git_sha": TARGET_DIRECT_RECIPE_INTRODUCED_SHA,
        "git_binding_policy": "job-exact-main-v1",
        "requires_job_expected_git_sha": True,
        "timeout_seconds": RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
        "expected_artifact_paths": artifacts,
        "success_predicate": "json.passed == true and generated_artifacts exactly equal expected_artifact_paths",
        "execution_validator": "exact-artifacts-json-v1",
        "preflight_profile": "target-direct-selection-4090-v1",
        "collector_acceptance": True,
        "collector_profile": "target-direct-selection-v2",
        "collector_result_roots": (leaf,),
        "collector_artifact_names": TARGET_DIRECT_SELECTION_ARTIFACT_NAMES,
        "selection_receipt_schema": "target_direct_v1.syncmate_selection_cell",
        "selection_matrix": {
            "stage": stage, "datasets": (TARGET_DIRECT_DATASET_DISPLAY[dataset],),
            "seeds": (seed,), "score_count": 17,
            "candidate_count": TARGET_DIRECT_CANDIDATE_COUNTS[dataset],
            "split_contract": TARGET_DIRECT_SPLIT_CONTRACT,
            "budget_ratios": TARGET_DIRECT_RATIOS,
            "expected_k_by_ratio": TARGET_DIRECT_K_BY_RATIO[dataset],
            "score_budget_semantics": "prefix_stable_budget_independent",
            "budget_conditioned_strategies": (), "parameter_scope": "last_layer",
            "lane": "target_direct_white_box",
        },
    }


def _target_direct_selection_recipe(stage: str) -> dict[str, Any]:
    return _target_selection_recipe(stage)


def _target_gu_recipe(stage: str, *, ratio: float, gate_only: bool = False) -> dict[str, Any]:
    dataset, seed_text = stage.rsplit("-seed", 1)
    seed = int(seed_text)
    ratio_key = _target_ratio_key(ratio)
    ratio_id = _target_ratio_id(ratio)
    strategies = ("degree",) if gate_only else TARGET_DIRECT_STRATEGIES
    artifacts = tuple(
        f"{TARGET_DIRECT_GU_OUTPUT_ROOT}/{dataset}_GCN_r{ratio_key}/GNNDelete_{strategy}/seed{seed}/{name}"
        for strategy in strategies
        for name in TARGET_DIRECT_GU_ARTIFACT_NAMES
    )
    recipe_id = (
        f"opengu-target-direct-gu-gate-{ratio_id}-v2"
        if gate_only else f"opengu-target-direct-gu-{stage}-{ratio_id}-v2"
    )
    argv = [
        "{python}", "-m", "experiments.target_direct_v1.syncmate_stage",
        "--config", TARGET_DIRECT_CONFIG, "--action", "gu", "--stage", stage,
        "--ratio", ratio_key,
    ]
    if gate_only:
        argv.append("--gate-only")
    argv.append("--json")
    definition: dict[str, Any] = {
        "id": recipe_id, "argv": tuple(argv), "config_path": TARGET_DIRECT_CONFIG,
        "config_sha256": TARGET_DIRECT_CONFIG_SHA256,
        "recipe_introduced_git_sha": TARGET_DIRECT_RECIPE_INTRODUCED_SHA,
        "git_binding_policy": "job-exact-main-v1", "requires_job_expected_git_sha": True,
        "timeout_seconds": RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
        "expected_artifact_paths": artifacts,
        "success_predicate": "json.passed == true and generated_artifacts exactly equal expected_artifact_paths",
        "execution_validator": "exact-artifacts-json-v1",
        "preflight_profile": "target-direct-gu-4090-v1",
        "collector_acceptance": True,
        "collector_profile": "target-direct-gu-v2" if gate_only else "target-direct-gu-stage-v2",
        "collector_result_roots": tuple(path.rsplit("/", 1)[0] for path in artifacts[::4]),
        "collector_artifact_names": TARGET_DIRECT_GU_ARTIFACT_NAMES,
    }
    contract: dict[str, Any] = {
        "stage": stage, "dataset": TARGET_DIRECT_DATASET_DISPLAY[dataset],
        "base_model": "GCN", "gu_method": "GNNDelete", "seed": seed,
        "ratio": float(ratio), "k": TARGET_DIRECT_K_BY_RATIO[dataset][ratio_key],
        "candidate_count": TARGET_DIRECT_CANDIDATE_COUNTS[dataset],
        "split_contract": TARGET_DIRECT_SPLIT_CONTRACT,
        "parameter_scope": "last_layer", "lane": "target_direct_white_box",
        "target_checkpoint_required": True, "scientific_comparison": not gate_only,
        "execution_authorized": bool(gate_only), "candidate_matrix_only": not gate_only,
    }
    if gate_only:
        contract["selector"] = "degree"
        definition["gu_gate"] = contract
    else:
        contract["selectors"] = TARGET_DIRECT_STRATEGIES
        definition["gu_stage"] = contract
    return definition


def _target_direct_gu_artifacts(
    stage: str,
    *,
    ratio: float,
    gate_only: bool = False,
) -> tuple[str, ...]:
    return tuple(
        _target_gu_recipe(stage, ratio=ratio, gate_only=gate_only)[
            "expected_artifact_paths"
        ]
    )


def _target_direct_gu_roots(
    stage: str,
    *,
    ratio: float,
    gate_only: bool = False,
) -> tuple[str, ...]:
    return tuple(
        _target_gu_recipe(stage, ratio=ratio, gate_only=gate_only)[
            "collector_result_roots"
        ]
    )


def _target_direct_gu_recipe(
    stage: str,
    *,
    ratio: float,
    gate_only: bool = False,
) -> dict[str, Any]:
    return _target_gu_recipe(stage, ratio=ratio, gate_only=gate_only)


def _build_registry() -> dict[str, dict[str, Any]]:
    definitions: dict[str, dict[str, Any]] = {
        "smoke": {
            "id": "smoke",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "smoke", "--json"),
            "config_path": "scripts/syncmate/setup.example.yaml",
            "config_sha256": "03fb31feae5edb3fde21b9eab2fcc892fecb764e05fafe44b38c753fdde9f8a1",
            "recipe_introduced_git_sha": RUNNER_RECIPE_INTRODUCED_SHA,
            "git_binding_policy": "job-exact-main-v1", "timeout_seconds": 180,
            "expected_artifact_paths": (), "success_predicate": "json.passed == true",
            "collector_acceptance": False,
        },
        "opengu-preflight-v1": {
            "id": "opengu-preflight-v1",
            "argv": ("{python}", "scripts/syncmate/syncmate.py", "runner-preflight", "--recipe", "opengu-preflight-v1", "--json"),
            "config_path": "experiments/configs/phase_b_cora_gcn.yaml",
            "config_sha256": "5011d428dac128a4f5ca6ee7346cfc46880281ceb7528135f2f023cc1e683c89",
            "recipe_introduced_git_sha": RUNNER_RECIPE_INTRODUCED_SHA,
            "git_binding_policy": "job-exact-main-v1", "timeout_seconds": 180,
            "expected_artifact_paths": (
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/attack.json",
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/collateral.json",
                "results/runs/__syncmate_preflight__/opengu_preflight/seed0/_meta.json",
            ),
            "success_predicate": "json.passed == true and generated_artifacts == expected_artifact_paths",
            "collector_acceptance": True,
        },
        "opengu-cache-v2-gate4-v1": {
            "id": "opengu-cache-v2-gate4-v1",
            "argv": ("{python}", "-m", "scripts.cache_v2_gate4_canary", "--json"),
            "config_path": "experiments/configs/cache_v2_gate4_cora_degree_canary.yaml",
            "config_sha256": "45f587853aee6a91e85efd82ee40350435969a7b51b9539062762ae06b875980",
            "expected_git_sha": GATE4_RECIPE_BASE_SHA,
            "allowed_git_delta_paths": GATE4_RECIPE_ALLOWED_DELTA,
            "timeout_seconds": 3600,
            "expected_artifact_paths": (
                "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/attack.json",
                "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/collateral.json",
                "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/predictions.npz",
                "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42/_meta.json",
            ),
            "success_predicate": "json.passed == true and collector gate passes for the exact result leaf",
            "collector_acceptance": True,
        },
    }
    definitions.update({
        f"opengu-target-direct-selection-{stage}-v2": _target_selection_recipe(stage)
        for stage in TARGET_DIRECT_STAGES
    })
    definitions.update({
        f"opengu-target-direct-gu-gate-{_target_ratio_id(ratio)}-v2":
        _target_gu_recipe("cora-seed42", ratio=ratio, gate_only=True)
        for ratio in TARGET_DIRECT_RATIOS
    })
    definitions.update({
        f"opengu-target-direct-gu-{stage}-{_target_ratio_id(ratio)}-v2":
        _target_gu_recipe(stage, ratio=ratio)
        for stage in TARGET_DIRECT_STAGES
        for ratio in TARGET_DIRECT_RATIOS
    })
    return definitions


_RECIPE_DEFINITIONS = _build_registry()


def recipe_definitions() -> dict[str, dict[str, Any]]:
    return copy.deepcopy(_RECIPE_DEFINITIONS)
