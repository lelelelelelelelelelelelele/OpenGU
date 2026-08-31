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


def test_current_formal_config_keeps_exact_ratio_conditioned_contract():
    config = yaml.safe_load(
        (ROOT / "experiments" / "configs" / "syncmate_target_direct_formal_v2.yaml")
        .read_text(encoding="utf-8")
    )
    assert config["version"] == 2
    assert config["budget_ratios"] == [0.01, 0.05]
    assert config["budget_rounding"] == "floor_with_minimum_one"
    assert config["datasets"] == {
        "cora": {
            "display_name": "Cora",
            "expected_candidate_count": 1895,
            "expected_k_by_ratio": {"0.01": 18, "0.05": 94},
        },
        "citeseer": {
            "display_name": "CiteSeer",
            "expected_candidate_count": 2328,
            "expected_k_by_ratio": {"0.01": 23, "0.05": 116},
        },
        "pubmed": {
            "display_name": "PubMed",
            "expected_candidate_count": 13801,
            "expected_k_by_ratio": {"0.01": 138, "0.05": 690},
        },
    }
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
