from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYNC_DIR = PROJECT_ROOT / "scripts" / "syncmate"
RECIPE_REGISTRY_SHA256 = (
    "c8ae1581f2346f3c4d79e9867bcd3642703651581cad9e3357d29cf843a7adaa"
)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_sha256(definitions: Mapping[str, Mapping[str, Any]]) -> str:
    payload = json.dumps(
        definitions,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@pytest.fixture
def project_extension(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(SYNC_DIR))
    module = _load_module(
        "opengu_adapter_full_test",
        SYNC_DIR / "opengu_adapter.py",
    )
    return module.OpenGUProjectExtension()


def test_full_registry_matches_reviewed_literal_contract(project_extension):
    definitions = project_extension.recipes(PROJECT_ROOT)
    expected_ids = {
        "smoke",
        "opengu-preflight-v1",
        "opengu-cache-v2-gate4-v1",
        "opengu-small-selection-mvp-v1",
        "opengu-small-selection-dataset-gate-v1",
        "opengu-small-selection-full-v1",
        *{f"opengu-small-selection-gu-gate-v{version}" for version in range(1, 6)},
        *{
            f"opengu-small-selection-gu-{dataset}-seed{seed}-v{version}"
            for version in range(2, 6)
            for dataset in ("cora", "citeseer", "pubmed")
            for seed in (42, 212, 2024)
        },
        *{
            f"opengu-target-direct-selection-{dataset}-seed{seed}-v2"
            for dataset in ("cora", "citeseer", "pubmed")
            for seed in (42, 212, 2024)
        },
        "opengu-target-direct-gu-gate-r001-v2",
        "opengu-target-direct-gu-gate-r005-v2",
        *{
            f"opengu-target-direct-gu-{dataset}-seed{seed}-{ratio}-v2"
            for dataset in ("cora", "citeseer", "pubmed")
            for seed in (42, 212, 2024)
            for ratio in ("r001", "r005")
        },
    }

    assert len(definitions) == 76
    assert set(definitions) == expected_ids
    assert _canonical_sha256(definitions) == RECIPE_REGISTRY_SHA256


def test_representative_recipe_fields_remain_exact(project_extension):
    definitions = project_extension.recipes(PROJECT_ROOT)

    assert definitions["smoke"]["argv"] == (
        "{python}",
        "scripts/syncmate/syncmate.py",
        "smoke",
        "--json",
    )
    assert definitions["opengu-cache-v2-gate4-v1"]["timeout_seconds"] == 3600
    assert definitions["opengu-small-selection-full-v1"]["selection_matrix"] == {
        "datasets": ("Cora", "CiteSeer", "PubMed"),
        "seeds": (42, 212, 2024),
        "score_count": 17,
    }
    gu_stage = definitions["opengu-small-selection-gu-pubmed-seed2024-v5"]
    assert gu_stage["gu_stage"]["selectors"][-1] == "tracin_cp_simple_6"
    assert len(gu_stage["expected_artifact_paths"]) == 68
    target = definitions["opengu-target-direct-gu-citeseer-seed212-r001-v2"]
    assert target["gu_stage"]["k"] == 23
    assert target["gu_stage"]["target_checkpoint_required"] is True


def test_all_recipe_commands_and_artifact_paths_are_bounded(project_extension):
    definitions = project_extension.recipes(PROJECT_ROOT)

    for recipe_id, definition in definitions.items():
        assert definition["id"] == recipe_id
        assert isinstance(definition["argv"], (tuple, list))
        assert definition["argv"]
        assert all(isinstance(token, str) and token for token in definition["argv"])
        for artifact in definition.get("expected_artifact_paths", ()):
            path = PurePosixPath(artifact)
            assert not path.is_absolute()
            assert ".." not in path.parts
            assert path.parts[:2] == ("results", "runs")


def test_recipe_results_are_copy_safe(project_extension):
    first = project_extension.recipes(PROJECT_ROOT)
    first["smoke"]["argv"] = ("mutated",)

    assert project_extension.recipes(PROJECT_ROOT)["smoke"]["argv"][0] == "{python}"
