from __future__ import annotations

import copy
from typing import Any


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

SMALL_SELECTION_RECIPE_INTRODUCED_SHA = "57bdefdf62d304f83352ce0f5de2adadd594a8cb"
SMALL_SELECTION_OUTPUT_ROOT = "results/runs/__syncmate_small_selection_v1__"
SMALL_SELECTION_ARTIFACT_NAMES = ("cold.json", "warm.json", "cell.json")
SMALL_SELECTION_GU_ARTIFACT_NAMES = (
    "attack.json", "collateral.json", "predictions.npz", "_meta.json"
)
SMALL_SELECTION_GU_FULL_DATASETS = ("cora", "citeseer", "pubmed")
SMALL_SELECTION_GU_FULL_SEEDS = (42, 212, 2024)
SMALL_SELECTION_GU_FULL_STRATEGIES = (
    "a_grad_norm", "b_param_hutch", "degree", "gt_full", "gt_simple",
    "legacy", "p_graph", "p_point", "p_simple", "r_point", "random",
    "tracin_cp_graph_3", "tracin_cp_graph_6", "tracin_cp_point_3",
    "tracin_cp_point_6", "tracin_cp_simple_3", "tracin_cp_simple_6",
)
SMALL_SELECTION_GU_FULL_STAGES = tuple(
    f"{dataset}-seed{seed}"
    for dataset in SMALL_SELECTION_GU_FULL_DATASETS
    for seed in SMALL_SELECTION_GU_FULL_SEEDS
)

_GU_VERSIONS = {
    1: {
        "introduced": "218f6421c2cb31b71ebfad113fee15b9ad0a3d36",
        "gate_config": "experiments/configs/syncmate_small_selection_gu_gate_v1.yaml",
        "gate_sha": "0e277fa5871ec2fa9b1b9049de8878504ceea7507150e45b8b5ec43d30b88833",
        "gate_root": "results/runs/__syncmate_small_selection_gu_v1__",
    },
    2: {
        "introduced": "5e8502d915d7f311f26e659fcbe58c463e96d3ae",
        "gate_config": "experiments/configs/syncmate_small_selection_gu_gate_v2.yaml",
        "gate_sha": "342ae520de154dfabf861736448c8c8bcddcccf05a58f247d38706e44aad8dda",
        "gate_root": "results/runs/__syncmate_small_selection_gu_v2__",
        "full_config": "experiments/configs/syncmate_small_selection_gu_full_v2.yaml",
        "full_sha": "5b94c51aa950ebda34a31498aaf92dbabb69f65099cbca1848a346f4dce80ad6",
        "full_root": "results/runs/__syncmate_small_selection_gu_full_v2__",
    },
    3: {
        "introduced": "d8eda635dd5c8bd5ab7489340a3c00b00df46e1b",
        "gate_config": "experiments/configs/syncmate_small_selection_gu_gate_v3.yaml",
        "gate_sha": "adb00f5e76097953415cea27e9e621b6c98e658685a1bf0450df5c6a96a0bd71",
        "gate_root": "results/runs/__syncmate_small_selection_gu_v3__",
        "full_config": "experiments/configs/syncmate_small_selection_gu_full_v3.yaml",
        "full_sha": "f3eca0b813acbf582ba357e6ee3ac3b2ec90bfb064d7475f8324d7b0ada92dac",
        "full_root": "results/runs/__syncmate_small_selection_gu_full_v3__",
    },
    4: {
        "introduced": "544eab7ece867a406a4bdc703f7e4c10bb9a313c",
        "gate_config": "experiments/configs/syncmate_small_selection_gu_gate_v4.yaml",
        "gate_sha": "ec0ec36da6d5e65ed72dcd37e8cc2fbd854ffda2da134154e6c566444876264e",
        "gate_root": "results/runs/__syncmate_small_selection_gu_v4__",
        "full_config": "experiments/configs/syncmate_small_selection_gu_full_v4.yaml",
        "full_sha": "551c5360ec424b1eb35d6c6fce06f251bfe01c3380a0fa731cb136c8e3022f21",
        "full_root": "results/runs/__syncmate_small_selection_gu_full_v4__",
    },
    5: {
        "introduced": "324d3a0434614ec0d206e18f784560ae90f5f945",
        "gate_config": "experiments/configs/syncmate_small_selection_gu_gate_v5.yaml",
        "gate_sha": "26c1b120c91cc96c14a659e15881687605be9b1e8fedd12aa54e085120e1bd10",
        "gate_root": "results/runs/__syncmate_small_selection_gu_v5__",
        "full_config": "experiments/configs/syncmate_small_selection_gu_full_v5.yaml",
        "full_sha": "bdabc12b1a1cb83938c21eeb3b0e899d80855af38f036e38d08186a1ae4451dd",
        "full_root": "results/runs/__syncmate_small_selection_gu_full_v5__",
    },
}

SMALL_SELECTION_GU_RECIPE_INTRODUCED_SHA = _GU_VERSIONS[1]["introduced"]
SMALL_SELECTION_GU_V2_RECIPE_INTRODUCED_SHA = _GU_VERSIONS[2]["introduced"]
SMALL_SELECTION_GU_V3_RECIPE_INTRODUCED_SHA = _GU_VERSIONS[3]["introduced"]
SMALL_SELECTION_GU_V4_RECIPE_INTRODUCED_SHA = _GU_VERSIONS[4]["introduced"]
SMALL_SELECTION_GU_V5_RECIPE_INTRODUCED_SHA = _GU_VERSIONS[5]["introduced"]
SMALL_SELECTION_GU_OUTPUT_ROOT = _GU_VERSIONS[1]["gate_root"]
SMALL_SELECTION_GU_V2_OUTPUT_ROOT = _GU_VERSIONS[2]["gate_root"]
SMALL_SELECTION_GU_V3_OUTPUT_ROOT = _GU_VERSIONS[3]["gate_root"]
SMALL_SELECTION_GU_V4_OUTPUT_ROOT = _GU_VERSIONS[4]["gate_root"]
SMALL_SELECTION_GU_V5_OUTPUT_ROOT = _GU_VERSIONS[5]["gate_root"]
SMALL_SELECTION_GU_EXPECTED_ARTIFACTS = tuple(
    f"{SMALL_SELECTION_GU_OUTPUT_ROOT}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
    for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
)
SMALL_SELECTION_GU_V2_EXPECTED_ARTIFACTS = tuple(
    f"{SMALL_SELECTION_GU_V2_OUTPUT_ROOT}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
    for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
)
SMALL_SELECTION_GU_V3_EXPECTED_ARTIFACTS = tuple(
    f"{SMALL_SELECTION_GU_V3_OUTPUT_ROOT}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
    for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
)
SMALL_SELECTION_GU_V4_EXPECTED_ARTIFACTS = tuple(
    f"{SMALL_SELECTION_GU_V4_OUTPUT_ROOT}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
    for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
)
SMALL_SELECTION_GU_V5_EXPECTED_ARTIFACTS = tuple(
    f"{SMALL_SELECTION_GU_V5_OUTPUT_ROOT}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
    for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
)
SMALL_SELECTION_GU_FULL_OUTPUT_ROOT = _GU_VERSIONS[2]["full_root"]
SMALL_SELECTION_GU_FULL_CONFIG = _GU_VERSIONS[2]["full_config"]
SMALL_SELECTION_GU_FULL_CONFIG_SHA256 = _GU_VERSIONS[2]["full_sha"]
SMALL_SELECTION_GU_V3_FULL_OUTPUT_ROOT = _GU_VERSIONS[3]["full_root"]
SMALL_SELECTION_GU_V3_FULL_CONFIG = _GU_VERSIONS[3]["full_config"]
SMALL_SELECTION_GU_V3_FULL_CONFIG_SHA256 = _GU_VERSIONS[3]["full_sha"]
SMALL_SELECTION_GU_V4_FULL_OUTPUT_ROOT = _GU_VERSIONS[4]["full_root"]
SMALL_SELECTION_GU_V4_FULL_CONFIG = _GU_VERSIONS[4]["full_config"]
SMALL_SELECTION_GU_V4_FULL_CONFIG_SHA256 = _GU_VERSIONS[4]["full_sha"]
SMALL_SELECTION_GU_V5_FULL_OUTPUT_ROOT = _GU_VERSIONS[5]["full_root"]
SMALL_SELECTION_GU_V5_FULL_CONFIG = _GU_VERSIONS[5]["full_config"]
SMALL_SELECTION_GU_V5_FULL_CONFIG_SHA256 = _GU_VERSIONS[5]["full_sha"]

TARGET_DIRECT_RECIPE_INTRODUCED_SHA = "264b38995cebc84d10402d8113ea949ca2cfa34f"
TARGET_DIRECT_CONFIG = "experiments/configs/syncmate_target_direct_formal_v2.yaml"
TARGET_DIRECT_CONFIG_SHA256 = "3a51a4d46c84e261c8df40c764dfc725349f8979c7d43f676c60cb9ab1693798"
TARGET_DIRECT_SELECTION_OUTPUT_ROOT = "results/runs/target_direct_formal_v2/selection"
TARGET_DIRECT_GU_OUTPUT_ROOT = "results/runs/target_direct_formal_v2/gu"
TARGET_DIRECT_SELECTION_ARTIFACT_NAMES = (
    "cold-r0.01.json", "cold-r0.05.json",
    "warm-r0.01.json", "warm-r0.05.json", "cell.json",
)
TARGET_DIRECT_GU_ARTIFACT_NAMES = SMALL_SELECTION_GU_ARTIFACT_NAMES
TARGET_DIRECT_DATASETS = ("cora", "citeseer", "pubmed")
TARGET_DIRECT_DATASET_DISPLAY = {
    "cora": "Cora", "citeseer": "CiteSeer", "pubmed": "PubMed",
}
TARGET_DIRECT_CANDIDATE_COUNTS = {
    "cora": 1895, "citeseer": 2328, "pubmed": 13801,
}
TARGET_DIRECT_RATIOS = (0.01, 0.05)
TARGET_DIRECT_K_BY_RATIO = {
    "cora": {"0.01": 18, "0.05": 94},
    "citeseer": {"0.01": 23, "0.05": 116},
    "pubmed": {"0.01": 138, "0.05": 690},
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


def _selection_artifacts(datasets: tuple[str, ...], seeds: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(
        f"{SMALL_SELECTION_OUTPUT_ROOT}/cells/{dataset.lower()}_seed{seed}/{name}"
        for dataset in datasets
        for seed in seeds
        for name in SMALL_SELECTION_ARTIFACT_NAMES
    )


def _selection_recipe(
    recipe_id: str,
    config_name: str,
    config_sha256: str,
    datasets: tuple[str, ...],
    seeds: tuple[int, ...],
) -> dict[str, Any]:
    config_path = f"experiments/configs/{config_name}"
    return {
        "id": recipe_id,
        "argv": ("{python}", "-m", "experiments.bc_target_v2.syncmate_recipe", "--config", config_path, "--json"),
        "config_path": config_path,
        "config_sha256": config_sha256,
        "recipe_introduced_git_sha": SMALL_SELECTION_RECIPE_INTRODUCED_SHA,
        "git_binding_policy": "job-exact-main-v1",
        "requires_job_expected_git_sha": True,
        "timeout_seconds": RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
        "expected_artifact_paths": _selection_artifacts(datasets, seeds),
        "success_predicate": "json.passed == true and generated_artifacts exactly equal expected_artifact_paths",
        "execution_validator": "exact-artifacts-json-v1",
        "preflight_profile": "small-selection-4090-v1",
        "collector_acceptance": True,
        "collector_profile": "small-selection-v1",
        "collector_result_roots": (SMALL_SELECTION_OUTPUT_ROOT,),
        "collector_artifact_names": SMALL_SELECTION_ARTIFACT_NAMES,
        "selection_matrix": {"datasets": datasets, "seeds": seeds, "score_count": 17},
    }


def _gu_gate_recipe(version: int) -> dict[str, Any]:
    spec = _GU_VERSIONS[version]
    root = str(spec["gate_root"])
    expected = tuple(
        f"{root}/cora_GCN_r0.05/GNNDelete_degree/seed42/{name}"
        for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
    )
    return {
        "id": f"opengu-small-selection-gu-gate-v{version}",
        "argv": ("{python}", "-m", "experiments.gu_target_v1.syncmate_recipe", "--config", spec["gate_config"], "--json"),
        "config_path": spec["gate_config"],
        "config_sha256": spec["gate_sha"],
        "recipe_introduced_git_sha": spec["introduced"],
        "git_binding_policy": "job-exact-main-v1",
        "requires_job_expected_git_sha": True,
        "timeout_seconds": RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
        "expected_artifact_paths": expected,
        "success_predicate": "json.passed == true and generated_artifacts exactly equal expected_artifact_paths",
        "execution_validator": "exact-artifacts-json-v1",
        "preflight_profile": "small-selection-gu-4090-v1",
        "collector_acceptance": True,
        "collector_profile": "small-selection-gu-v1",
        "collector_result_roots": (root,),
        "collector_artifact_names": SMALL_SELECTION_GU_ARTIFACT_NAMES,
        "gu_gate": {
            "dataset": "Cora", "base_model": "GCN", "gu_method": "GNNDelete",
            "selector": "degree", "seed": 42, "k": 7,
            "lane": "controlled_public_profile_gu", "scientific_comparison": False,
        },
    }


def _gu_stage_artifacts(version: int, stage: str) -> tuple[str, ...]:
    spec = _GU_VERSIONS[version]
    dataset, seed_text = stage.rsplit("-seed", 1)
    seed = int(seed_text)
    return tuple(
        f"{spec['full_root']}/{dataset}_GCN_r0.05/GNNDelete_{strategy}/seed{seed}/{name}"
        for strategy in SMALL_SELECTION_GU_FULL_STRATEGIES
        for name in SMALL_SELECTION_GU_ARTIFACT_NAMES
    )


def _gu_stage_recipe(version: int, stage: str) -> dict[str, Any]:
    spec = _GU_VERSIONS[version]
    dataset, seed_text = stage.rsplit("-seed", 1)
    seed = int(seed_text)
    artifacts = _gu_stage_artifacts(version, stage)
    return {
        "id": f"opengu-small-selection-gu-{stage}-v{version}",
        "argv": ("{python}", "-m", "experiments.gu_target_v1.syncmate_stage", "--config", spec["full_config"], "--stage", stage, "--json"),
        "config_path": spec["full_config"],
        "config_sha256": spec["full_sha"],
        "recipe_introduced_git_sha": spec["introduced"],
        "git_binding_policy": "job-exact-main-v1",
        "requires_job_expected_git_sha": True,
        "timeout_seconds": RUNNER_AGENT_MAX_TIMEOUT_SECONDS,
        "expected_artifact_paths": artifacts,
        "success_predicate": "json.passed == true and generated_artifacts exactly equal expected_artifact_paths",
        "execution_validator": "exact-artifacts-json-v1",
        "preflight_profile": "small-selection-gu-stage-4090-v1",
        "collector_acceptance": True,
        "collector_profile": "small-selection-gu-stage-v1",
        "collector_result_roots": tuple(path.rsplit("/", 1)[0] for path in artifacts[::4]),
        "collector_artifact_names": SMALL_SELECTION_GU_ARTIFACT_NAMES,
        "gu_stage": {
            "stage": stage, "dataset": dataset, "base_model": "GCN",
            "gu_method": "GNNDelete", "selectors": SMALL_SELECTION_GU_FULL_STRATEGIES,
            "seed": seed, "k": 7, "lane": "controlled_public_profile_gu",
            "scientific_comparison": True,
        },
    }


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
        "opengu-small-selection-mvp-v1": _selection_recipe(
            "opengu-small-selection-mvp-v1", "syncmate_small_selection_mvp_v1.yaml",
            "d75a8d89a212fd3bdb71fce101b17fd4d2f3ed05dd426c5410183b1c59eec5d0", ("Cora",), (42,),
        ),
        "opengu-small-selection-dataset-gate-v1": _selection_recipe(
            "opengu-small-selection-dataset-gate-v1", "syncmate_small_selection_dataset_gate_v1.yaml",
            "8394325534bee937ff8a5459671cbf20918f82c5615efc3e8cb7c6340b2cc214", ("Cora", "CiteSeer", "PubMed"), (42,),
        ),
        "opengu-small-selection-full-v1": _selection_recipe(
            "opengu-small-selection-full-v1", "syncmate_small_selection_full_v1.yaml",
            "29149a559ac14c0f4e13cc677417f4633002bc55c06ddb06f33f1b3bca62079d",
            ("Cora", "CiteSeer", "PubMed"), (42, 212, 2024),
        ),
    }
    definitions.update({
        f"opengu-small-selection-gu-gate-v{version}": _gu_gate_recipe(version)
        for version in range(1, 6)
    })
    definitions.update({
        f"opengu-small-selection-gu-{stage}-v{version}": _gu_stage_recipe(version, stage)
        for version in range(2, 6)
        for stage in SMALL_SELECTION_GU_FULL_STAGES
    })
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
