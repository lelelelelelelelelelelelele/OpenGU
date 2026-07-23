import json
from pathlib import Path

import pytest

from experiments.target_direct_v1.recipe import SCORE_NAMES
from experiments.target_direct_v1 import syncmate_stage as stage_module


GIT_SHA = "a" * 40


def _summary(*, warm: bool):
    method_timings = {
        strategy: {
            "cache_hit": warm,
            "status": "success",
            "cold_incremental_seconds": None if warm else 0.1,
        }
        for strategy in SCORE_NAMES
    }
    return {
        "schema": "target_direct_v1.selection_summary",
        "version": 1,
        "status": {"state": "success", "failure": None},
        "dataset": "Cora",
        "seed": 42,
        "processed_profile": "planetoid_70_10_20_seed2024",
        "parameter_scope": "last_layer",
        "candidate_count": 1895,
        "budget": {"expected_k": 94},
        "git_provenance": {"head": GIT_SHA, "worktree_dirty": False},
        "selection_artifacts": {
            strategy: {"artifact": {"artifact_id": strategy}}
            for strategy in SCORE_NAMES
        },
        "target_checkpoint": {
            "path": "/checkpoint.pt",
            "file_sha256": "b" * 64,
            "state_hash": "c" * 64,
        },
        "score_bundle": {
            "hit": warm,
            "artifact_id": "score_1",
            "recipe_hash": "d" * 64,
            "cold_total_seconds": None if warm else 3.0,
            "warm_read_seconds": 0.02 if warm else None,
        },
        "selection_cache": {"method_timings": method_timings},
        "gpu_memory": {
            "score_bundle": {"device_name": "NVIDIA GeForce RTX 4090"},
            "process_peak_allocated_bytes": 1024,
            "process_peak_reserved_bytes": 2048,
        },
    }


def test_formal_config_freezes_scope_budget_and_stress_boundary():
    config = stage_module.load_config()

    assert config["main_parameter_scope"] == "last_layer"
    assert config["stress_parameter_scope"] == "all_trainable"
    assert config["stress_ladder"] == [
        "cora-seed42",
        "pubmed-seed42",
        "citeseer-seed42",
    ]
    assert config["datasets"]["cora"]["expected_candidate_count"] == 1895
    assert config["datasets"]["cora"]["expected_k"] == 94
    assert config["datasets"]["citeseer"]["expected_k"] == 116
    assert config["datasets"]["pubmed"]["expected_k"] == 690
    assert tuple(config["strategy_order"]) == stage_module.FORMAL_STRATEGIES


def test_static_stage_artifact_sets_are_exact_and_bounded():
    selection = stage_module.selection_artifacts("cora-seed42")
    gate = stage_module.gu_artifacts("cora-seed42", gate_only=True)
    full = stage_module.gu_artifacts("pubmed-seed2024")

    assert len(selection) == 3
    assert selection[-1].endswith("/cora-seed42/cell.json")
    assert len(gate) == 4
    assert all("/GNNDelete_degree/seed42/" in path for path in gate)
    assert len(full) == 68
    assert all("/pubmed_GCN_r0.05/" in path for path in full)
    assert all("/seed2024/" in path for path in full)


def test_selection_receipt_binds_cold_warm_checkpoint_and_timings(tmp_path):
    config = stage_module.load_config()
    config["paths"] = dict(config["paths"])
    config["paths"]["selection_output_root"] = tmp_path / "selection"
    config["paths"]["score_cache_root"] = tmp_path / "score"
    config["paths"]["selection_store_root"] = tmp_path / "selection-store"
    config["paths"]["checkpoint_root"] = tmp_path / "checkpoints"
    config["paths"]["evidence_root"] = tmp_path / "evidence"
    paths = stage_module._stage_paths(config, "cora-seed42")
    paths["cold"].parent.mkdir(parents=True)
    paths["cold"].write_text(json.dumps(_summary(warm=False)), encoding="utf-8")
    paths["warm"].write_text(json.dumps(_summary(warm=True)), encoding="utf-8")

    receipt = stage_module._validate_selection_pair(
        config, "cora-seed42", GIT_SHA
    )

    assert receipt["schema"] == stage_module.RECEIPT_SCHEMA
    assert receipt["parameter_scope"] == "last_layer"
    assert receipt["candidate_count"] == 1895
    assert receipt["k"] == 94
    assert receipt["formal_score_count"] == 17
    assert receipt["score_bundle_cold_total_seconds"] == 3.0
    assert receipt["score_bundle_warm_read_seconds"] == 0.02
    assert set(receipt["method_timings"]) == set(SCORE_NAMES)
    assert receipt["target_checkpoint"]["state_hash"] == "c" * 64


def test_stage_parser_rejects_non_matrix_seed():
    with pytest.raises(stage_module.TargetDirectStageError):
        stage_module.parse_stage("cora-seed7")
