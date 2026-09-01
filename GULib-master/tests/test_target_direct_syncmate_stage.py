import json
from pathlib import Path

import pytest
import yaml

from experiments.target_direct_v1.recipe import SCORE_NAMES
from experiments.target_direct_v1 import syncmate_stage as stage_module
from experiments.target_direct_v1 import run_selection as selection_module


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
        "split_contract": {
            "processed_profile": "planetoid_70_10_20_seed2024",
            "train_ratio": 0.7,
            "val_ratio": 0.1,
            "test_ratio": 0.2,
            "split_seed": 2024,
        },
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

    assert config["split_contract"].to_manifest() == {
        "processed_profile": "planetoid_70_10_20_seed2024",
        "train_ratio": 0.7,
        "val_ratio": 0.1,
        "test_ratio": 0.2,
        "split_seed": 2024,
    }
    assert config["split"]["materialize_on_miss"] is True
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
    assert "score_cache_root" not in config
    assert "selection_store_root" not in config
    assert "cache_v2_identity" not in config["claims"]
    assert config["paths"]["cache_v2_root"] == (
        config["repository_root"] / "results" / "cache_v2"
    ).resolve()


def _write_formal_config(tmp_path, mutate):
    repository_root = tmp_path / "repo"
    config_path = (
        repository_root
        / "experiments"
        / "configs"
        / stage_module.CONFIG_PATH.name
    )
    config_path.parent.mkdir(parents=True)
    config = yaml.safe_load(
        stage_module.CONFIG_PATH.read_text(encoding="utf-8")
    )
    mutate(config)
    config_path.write_text(
        yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
    )
    return config_path, repository_root


@pytest.mark.parametrize(
    "field,value",
    (
        ("train_ratio", 0.6),
        ("val_ratio", 0.2),
        ("test_ratio", 0.1),
        ("split_seed", 42),
        ("materialize_on_miss", False),
    ),
)
def test_formal_config_rejects_unregistered_split_contract(tmp_path, field, value):
    config_path, repository_root = _write_formal_config(
        tmp_path,
        lambda config: config["split"].update({field: value}),
    )

    with pytest.raises(stage_module.TargetDirectStageError, match="split|frozen"):
        stage_module.load_config(config_path, repository_root=repository_root)


def test_preflight_does_not_materialize_split_before_execution_gates(monkeypatch):
    config = stage_module.load_config()
    observed = []
    monkeypatch.setattr(
        stage_module,
        "_git_state",
        lambda _root: {"branch": "other", "status_short": ["dirty"], "head": GIT_SHA},
    )
    monkeypatch.setattr(
        stage_module,
        "_profile",
        lambda _config, _dataset, *, allow_materialize: (
            observed.append(allow_materialize) or {"manifest_path": "profile.json"}
        ),
    )

    result = stage_module._formal_preflight(
        config,
        "cora-seed42",
        require_gpu=False,
    )

    assert result["ready"] is False
    assert observed == [False]


def test_preflight_allows_registered_split_materialization_after_gates(monkeypatch):
    config = stage_module.load_config()
    config["required_branch"] = "ready"
    config["required_active_checkout"] = str(config["repository_root"])
    observed = []
    monkeypatch.setattr(
        stage_module,
        "_git_state",
        lambda _root: {"branch": "ready", "status_short": [], "head": GIT_SHA},
    )
    monkeypatch.setattr(
        stage_module,
        "_profile",
        lambda _config, _dataset, *, allow_materialize: (
            observed.append(allow_materialize) or {"manifest_path": "profile.json"}
        ),
    )

    result = stage_module._formal_preflight(
        config,
        "cora-seed42",
        require_gpu=False,
    )

    assert result["ready"] is True
    assert observed == [True]


@pytest.mark.parametrize(
    "legacy_root",
    (
        "results/cache_v2/target_direct_formal_v2/score",
        "results/cache_v2/cora-seed42",
    ),
)
def test_formal_config_rejects_split_or_stage_cache_roots(
    tmp_path, legacy_root
):
    def mutate(config):
        config.pop("cache_v2_root", None)
        config["score_cache_root"] = legacy_root
        config["selection_store_root"] = legacy_root

    config_path, repository_root = _write_formal_config(tmp_path, mutate)

    with pytest.raises(stage_module.TargetDirectStageError, match="cache_v2_root"):
        stage_module.load_config(
            config_path, repository_root=repository_root
        )


@pytest.mark.parametrize(
    "noncanonical_root",
    (
        "results/cache_v2/target_direct_formal_v2",
        "results/cache_v2/cora-seed42",
    ),
)
def test_formal_config_rejects_cache_root_experiment_or_stage_descendant(
    tmp_path, noncanonical_root
):
    config_path, repository_root = _write_formal_config(
        tmp_path,
        lambda config: config.update({"cache_v2_root": noncanonical_root}),
    )

    with pytest.raises(stage_module.TargetDirectStageError, match="exactly"):
        stage_module.load_config(
            config_path, repository_root=repository_root
        )


def test_each_stage_uses_one_canonical_cache_store_root():
    config = stage_module.load_config()
    cora = stage_module._stage_paths(config, "cora-seed42")
    pubmed = stage_module._stage_paths(config, "pubmed-seed2024")

    expected = config["paths"]["cache_v2_root"]
    assert cora["score_store"] == cora["selection_store"] == expected
    assert pubmed["score_store"] == pubmed["selection_store"] == expected


def test_direct_selection_rejects_unequal_cache_roots(tmp_path):
    args = selection_module.build_parser().parse_args(
        [
            "--dataset",
            "Cora",
            "--processed-root",
            str(tmp_path.resolve()),
            "--runtime-root",
            str(tmp_path.resolve()),
            "--cache-root",
            str((tmp_path / "score").resolve()),
            "--selection-cache-root",
            str((tmp_path / "selection").resolve()),
            "--checkpoint-path",
            str((tmp_path / "checkpoint.pt").resolve()),
            "--output",
            str((tmp_path / "summary.json").resolve()),
            "--seed",
            "42",
            "--ratio",
            "0.01",
        ]
    )

    with pytest.raises(ValueError, match="same canonical Cache V2 root"):
        selection_module._validate_args(args)


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
    config["paths"]["cache_v2_root"] = tmp_path / "cache_v2"
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
