import json
from pathlib import Path

import pytest

from experiments.target_direct_v1.recipe import SCORE_NAMES
from experiments.target_direct_v1 import syncmate_stage as stage_module


GIT_SHA = "a" * 40


def _summary(
    *,
    ratio: float,
    score_hit: bool,
    selection_hit: bool,
):
    expected_k = 18 if ratio == 0.01 else 94
    method_timings = {
        strategy: {
            "cache_hit": selection_hit,
            "selection_projection_cache_hit": selection_hit,
            "status": "success",
            "cold_selection_projection_seconds": (
                None if selection_hit else 0.01
            ),
            "cold_incremental_seconds": (
                None if score_hit else 0.1
            ),
        }
        for strategy in SCORE_NAMES
    }
    return {
        "schema": "target_direct_v1.selection_summary",
        "version": 2,
        "status": {"state": "success", "failure": None},
        "dataset": "Cora",
        "seed": 42,
        "processed_profile": "planetoid_70_10_20_seed2024",
        "parameter_scope": "last_layer",
        "candidate_count": 1895,
        "budget": {
            "requested_ratio": ratio,
            "denominator": "train_candidate_count",
            "denominator_count": 1895,
            "rounding": "floor_with_minimum_one",
            "expected_k": expected_k,
        },
        "budget_projection": {
            "score_semantics": "prefix_stable_budget_independent",
            "supported_ratios": [0.01, 0.05],
            "budget_conditioned_strategies": [],
            "score_bundle_shared_across_ratios": True,
            "selection_artifact_ratio_conditioned": True,
        },
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
            "hit": score_hit,
            "artifact_id": "score_1",
            "recipe_hash": "d" * 64,
            "cold_total_seconds": None if score_hit else 3.0,
            "warm_read_seconds": 0.02 if score_hit else None,
        },
        "selection_cache": {"method_timings": method_timings},
        "gpu_memory": {
            "score_bundle": {"device_name": "NVIDIA GeForce RTX 4090"},
            "process_peak_allocated_bytes": 1024,
            "process_peak_reserved_bytes": 2048,
        },
    }


def test_formal_config_freezes_scope_budget_and_excludes_stress():
    config = stage_module.load_config()

    assert config["main_parameter_scope"] == "last_layer"
    assert "stress_parameter_scope" not in config
    assert "stress_ladder" not in config
    assert config["budget_ratios"] == [0.01, 0.05]
    assert config["score_budget_semantics"] == (
        "prefix_stable_budget_independent"
    )
    assert config["datasets"]["cora"]["expected_candidate_count"] == 1895
    assert config["datasets"]["cora"]["expected_k_by_ratio"] == {
        "0.01": 18,
        "0.05": 94,
    }
    assert config["datasets"]["citeseer"]["expected_k_by_ratio"] == {
        "0.01": 23,
        "0.05": 116,
    }
    assert config["datasets"]["pubmed"]["expected_k_by_ratio"] == {
        "0.01": 138,
        "0.05": 690,
    }
    assert config["claims"]["formal_gate_cells"] == 2
    assert config["claims"]["candidate_full_matrix_cells"] == 306
    assert config["claims"]["candidate_full_matrix_authorized"] is False
    assert tuple(config["strategy_order"]) == stage_module.FORMAL_STRATEGIES


def test_static_stage_artifact_sets_are_exact_and_bounded():
    selection = stage_module.selection_artifacts("cora-seed42")
    gate_1 = stage_module.gu_artifacts(
        "cora-seed42", ratio=0.01, gate_only=True
    )
    gate_5 = stage_module.gu_artifacts(
        "cora-seed42", ratio=0.05, gate_only=True
    )
    full = stage_module.gu_artifacts(
        "pubmed-seed2024", ratio=0.05
    )

    assert len(selection) == 5
    assert selection[-1].endswith("/cora-seed42/cell.json")
    assert {Path(path).name for path in selection[:-1]} == {
        "cold-r0.01.json",
        "cold-r0.05.json",
        "warm-r0.01.json",
        "warm-r0.05.json",
    }
    assert len(gate_1) == len(gate_5) == 4
    assert all("/cora_GCN_r0.01/" in path for path in gate_1)
    assert all("/cora_GCN_r0.05/" in path for path in gate_5)
    assert all("/GNNDelete_degree/seed42/" in path for path in gate_1)
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
    for position, ratio in enumerate(stage_module.BUDGET_RATIOS):
        key = stage_module.ratio_key(ratio)
        paths["cold"][key].parent.mkdir(parents=True, exist_ok=True)
        paths["cold"][key].write_text(
            json.dumps(
                _summary(
                    ratio=ratio,
                    score_hit=position != 0,
                    selection_hit=False,
                )
            ),
            encoding="utf-8",
        )
        paths["warm"][key].write_text(
            json.dumps(
                _summary(
                    ratio=ratio,
                    score_hit=True,
                    selection_hit=True,
                )
            ),
            encoding="utf-8",
        )

    receipt = stage_module._validate_selection_pair(
        config, "cora-seed42", GIT_SHA
    )

    assert receipt["schema"] == stage_module.RECEIPT_SCHEMA
    assert receipt["parameter_scope"] == "last_layer"
    assert receipt["candidate_count"] == 1895
    assert receipt["budget_ratios"] == [0.01, 0.05]
    assert receipt["expected_k_by_ratio"] == {
        "0.01": 18,
        "0.05": 94,
    }
    assert receipt["formal_score_count"] == 17
    assert receipt["score_bundle_cold_total_seconds"] == 3.0
    assert set(receipt["score_bundle_warm_read_seconds"]) == {
        "0.01_warm",
        "0.05_cold_projection",
        "0.05_warm",
    }
    assert set(
        receipt["ratio_results"]["0.01"]["cold_method_timings"]
    ) == set(SCORE_NAMES)
    assert receipt["ratio_results"]["0.01"]["k"] == 18
    assert receipt["ratio_results"]["0.05"]["k"] == 94
    assert receipt["target_checkpoint"]["state_hash"] == "c" * 64


def test_stage_parser_rejects_non_matrix_seed():
    with pytest.raises(stage_module.TargetDirectStageError):
        stage_module.parse_stage("cora-seed7")
