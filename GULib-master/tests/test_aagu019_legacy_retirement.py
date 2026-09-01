"""Regression guards for hard retirement of legacy experiment setup."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RETIRED_PACKAGES = (
    ROOT / "experiments" / "bc_target_v2",
    ROOT / "experiments" / "gu_target_v1",
    ROOT / "experiments" / "tracin_v2",
)
LEGACY_RUNTIME_MARKERS = (
    "experiments.bc_target_v2",
    "experiments.gu_target_v1",
    "experiments.tracin_v2",
    "opengu-small-selection",
    "syncmate_small_selection",
)


def _recipes_module():
    path = ROOT / "scripts" / "syncmate" / "opengu_recipes.py"
    spec = importlib.util.spec_from_file_location("aagu019_opengu_recipes", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_legacy_packages_configs_and_registry_are_not_executable():
    assert all(not list(path.glob("*.py")) for path in RETIRED_PACKAGES)
    assert not list(
        (ROOT / "experiments" / "configs").glob("syncmate_small_selection*.yaml")
    )
    definitions = _recipes_module().recipe_definitions()
    assert len(definitions) == 32
    assert not [recipe_id for recipe_id in definitions if "small-selection" in recipe_id]


def test_active_python_surface_has_no_legacy_runtime_reference():
    files = [
        *sorted((ROOT / "experiments").rglob("*.py")),
        *sorted((ROOT / "scripts" / "syncmate").rglob("*.py")),
    ]
    matches = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        found = [marker for marker in LEGACY_RUNTIME_MARKERS if marker in text]
        if found:
            matches[path.relative_to(ROOT).as_posix()] = found
    assert matches == {}


def test_current_formal_config_derives_ratio_conditioned_contract():
    config = yaml.safe_load(
        (ROOT / "experiments" / "configs" / "syncmate_target_direct_formal_v2.yaml")
        .read_text(encoding="utf-8")
    )
    assert config["version"] == 2
    assert config["split"] == {
        "train_ratio": 0.7,
        "val_ratio": 0.1,
        "test_ratio": 0.2,
        "split_seed": 2024,
        "materialize_on_miss": True,
    }
    assert config["budget_ratios"] == [0.01, 0.05]
    assert config["budget_rounding"] == "floor_with_minimum_one"
    assert config["datasets"] == {
        "cora": {
            "display_name": "Cora",
            "num_nodes": 2708,
        },
        "citeseer": {
            "display_name": "CiteSeer",
            "num_nodes": 3327,
        },
        "pubmed": {
            "display_name": "PubMed",
            "num_nodes": 19717,
        },
    }
    train_ratio = config["split"]["train_ratio"]
    derived = {}
    for dataset, settings in config["datasets"].items():
        candidate_count = int(settings["num_nodes"] * train_ratio)
        derived[dataset] = {
            "candidate_count": candidate_count,
            "k_by_ratio": {
                str(ratio): max(
                    1,
                    int(candidate_count * ratio),
                )
                for ratio in config["budget_ratios"]
            },
        }
    assert derived == {
        "cora": {
            "candidate_count": 1895,
            "k_by_ratio": {"0.01": 18, "0.05": 94},
        },
        "citeseer": {
            "candidate_count": 2328,
            "k_by_ratio": {"0.01": 23, "0.05": 116},
        },
        "pubmed": {
            "candidate_count": 13801,
            "k_by_ratio": {"0.01": 138, "0.05": 690},
        },
    }
    assert all(
        "expected_candidate_count" not in settings
        and "expected_k_by_ratio" not in settings
        for settings in config["datasets"].values()
    )
    assert "selection_k" not in config


def test_historical_evidence_remains_read_only_and_navigable():
    assert (
        ROOT
        / "results"
        / "bc_target_v2"
        / "selection_benchmark_20260721"
        / "benchmark_manifest.json"
    ).is_file()
    assert (ROOT / "reports" / "bc_target_matrix_REPORT.md").is_file()
