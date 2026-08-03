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
    "bb36f6943f7c519f9c7309a837c5e7a93598a72359d28da6fb0fa3614efc016a"
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
def adapter_module(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.syspath_prepend(str(SYNC_DIR))
    return _load_module(
        "opengu_adapter_full_test",
        SYNC_DIR / "opengu_adapter.py",
    )


@pytest.fixture
def project_extension(adapter_module):
    return adapter_module.OpenGUProjectExtension()


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


def test_all_reviewed_preflight_profiles_dispatch_to_project_handlers(
    adapter_module,
    project_extension,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    calls: list[tuple[str, str]] = []

    def handler(definition, config_path):
        calls.append((definition["id"], str(config_path)))
        return {"ready": True, "errors": [], "source": "project-handler"}

    profiles = {
        "small-selection-4090-v1": "opengu-small-selection-mvp-v1",
        "small-selection-gu-4090-v1": "opengu-small-selection-gu-gate-v5",
        "small-selection-gu-stage-4090-v1": "opengu-small-selection-gu-cora-seed42-v5",
        "target-direct-selection-4090-v1": "opengu-target-direct-selection-cora-seed42-v2",
        "target-direct-gu-4090-v1": "opengu-target-direct-gu-cora-seed42-r005-v2",
    }
    monkeypatch.setattr(
        adapter_module,
        "_PREFLIGHT_HANDLERS",
        {profile: handler for profile in profiles},
    )
    definitions = project_extension.recipes(PROJECT_ROOT)

    for profile, recipe_id in profiles.items():
        result = project_extension.preflight(
            profile,
            definitions[recipe_id],
            tmp_path / "config.yaml",
        )
        assert result["ready"] is True
        assert result["owner"] == "opengu"
        assert result["profile"] == profile

    assert [recipe_id for recipe_id, _ in calls] == list(profiles.values())


def test_unknown_preflight_profile_refuses_with_expected_observed_action(
    project_extension,
    tmp_path: Path,
):
    result = project_extension.preflight(
        "unknown-profile",
        {"id": "unknown"},
        tmp_path / "missing.yaml",
    )

    assert result["ready"] is False
    assert result["owner"] == "opengu"
    assert result["expected"]["profile"] == "reviewed OpenGU preflight profile"
    assert result["observed"]["profile"] == "unknown-profile"
    assert result["action"] == "select a reviewed OpenGU recipe"


def test_results_parser_reads_only_verified_index_artifacts(
    project_extension,
    tmp_path: Path,
):
    leaf = tmp_path / "results" / "runs" / "gpu4090" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    leaf.mkdir(parents=True)
    payloads = {
        "attack.json": {"results": {"im": {"f1_after": 0.71, "mia_auc": 0.64}}},
        "collateral.json": {"results": [{"strategy": "im", "perf_before": 0.8}]},
        "_meta.json": {"git_sha": "abcdef123", "hostname": "gpu4090"},
    }
    items = []
    for name, payload in payloads.items():
        path = leaf / name
        encoded = json.dumps(payload).encode("utf-8")
        path.write_bytes(encoded)
        items.append(
            {
                "remote_path": f"results/runs/cora_GCN_r0.05/GIF_im/seed42/{name}",
                "local_path": path.relative_to(tmp_path).as_posix(),
                "sha256": hashlib.sha256(encoded).hexdigest(),
            }
        )
    index = {
        "index_path": ".syncmate/artifact_index.json",
        "peers": {
            "gpu4090": {
                "node_id": "gpu4090",
                "artifact_policy": {"include": list(payloads)},
                "summary": {"indexed": 3, "status": "verified"},
                "items": items,
            }
        },
    }

    result = project_extension.results(
        index,
        {"project_root": tmp_path, "node_ids": ["gpu4090"], "include_incomplete": False},
    )

    assert result["owner"] == "opengu"
    assert result["summary"]["rows"] == 1
    assert result["summary"]["parse_errors"] == 0
    assert result["rows"][0]["strategy"] == "im"


@pytest.mark.parametrize(
    "profile,recipe_id",
    [
        ("small-selection-v1", "opengu-small-selection-mvp-v1"),
        ("small-selection-gu-v1", "opengu-small-selection-gu-gate-v5"),
        ("small-selection-gu-stage-v1", "opengu-small-selection-gu-cora-seed42-v5"),
        ("target-direct-selection-v2", "opengu-target-direct-selection-cora-seed42-v2"),
        ("target-direct-gu-v2", "opengu-target-direct-gu-gate-r005-v2"),
        ("target-direct-gu-stage-v2", "opengu-target-direct-gu-cora-seed42-r005-v2"),
    ],
)
def test_unverified_index_never_passes_project_acceptance(
    project_extension,
    profile: str,
    recipe_id: str,
    tmp_path: Path,
):
    definition = project_extension.recipes(PROJECT_ROOT)[recipe_id]
    result = project_extension.accept(
        profile,
        definition,
        {
            "artifact_index": {
                "peers": {"gpu4090": {"summary": {"status": "failed"}, "items": []}}
            },
            "node_id": "gpu4090",
            "expected_git_sha": "a" * 40,
            "project_root": tmp_path,
        },
    )

    assert result["owner"] == "opengu"
    assert result["passed"] is False
    assert result["status"] == "rejected"
    assert any("not verified" in error for error in result["errors"])
