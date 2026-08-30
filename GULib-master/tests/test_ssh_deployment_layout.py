"""Contracts for the AutoDL deployment-root boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from experiments import path_policy
from experiments import run as experiment_runner
from scripts.validate_ssh_deployment_layout import inspect_layout
from scripts.validate_retired_ssh_references import (
    inspect_repository,
    inspect_text,
)


def test_layout_accepts_only_platform_entries_and_active_checkout(tmp_path):
    for name in (".sys", "OpenGU"):
        (tmp_path / name).mkdir()
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")

    payload = inspect_layout(tmp_path, (".gitignore", ".sys", "OpenGU"))

    assert payload["passed"] is True
    assert payload["unexpected"] == []


def test_layout_rejects_peer_directory(tmp_path):
    (tmp_path / "OpenGU").mkdir()
    (tmp_path / "opengu-experiments").mkdir()

    payload = inspect_layout(tmp_path, ("OpenGU",))

    assert payload["passed"] is False
    assert payload["unexpected"] == ["opengu-experiments"]


def test_active_autodl_checkout_rejects_external_runtime_path(
    tmp_path,
    monkeypatch,
):
    root = (tmp_path / "OpenGU" / "GULib-master").resolve()
    root.mkdir(parents=True)
    external = (tmp_path / "opengu-experiments" / "new-run").resolve()
    monkeypatch.setattr(path_policy, "AUTODL_ACTIVE_REPO_ROOT", root)

    with pytest.raises(ValueError, match="runtime_root must resolve inside"):
        path_policy.resolve_owned_path(
            root,
            external,
            "runtime_root",
        )


def test_noncanonical_checkout_can_use_test_temp_paths(tmp_path):
    repository = tmp_path / "checkout"
    repository.mkdir()
    external = tmp_path / "runtime"

    assert path_policy.resolve_owned_path(
        repository,
        external,
        "runtime_root",
    ) == external.resolve()


def test_runner_blocks_historical_peer_root_on_active_checkout(
    tmp_path,
    monkeypatch,
):
    root = (tmp_path / "OpenGU" / "GULib-master").resolve()
    root.mkdir(parents=True)
    external = (tmp_path / "OpenGU-small-selection-gu" / "gate-v4").resolve()
    monkeypatch.setattr(path_policy, "AUTODL_ACTIVE_REPO_ROOT", root)
    monkeypatch.setattr(experiment_runner, "REPO_ROOT", root)

    with pytest.raises(ValueError, match="runtime_root must resolve inside"):
        experiment_runner.experiment_runtime_root({"runtime_root": external})


def test_retired_reference_validator_detects_old_peer_root():
    old_prefix = "/".join(("/autodl-fs/data", "opengu-experiments"))

    matches = inspect_text("report.md", "checkout: {0}/run".format(old_prefix))

    assert matches == [
        {
            "path": "report.md",
            "line": 1,
            "prefix": old_prefix,
            "count": 1,
        }
    ]


def test_retired_reference_validator_accepts_archive_and_active_paths():
    text = "\n".join(
        (
            "/autodl-fs/data/OpenGU/GULib-master/results/_archive_example",
            "/autodl-fs/data/OpenGU/GULib-master/data/raw",
        )
    )

    assert inspect_text("report.md", text) == []


def test_repository_has_no_tracked_retired_peer_prefixes():
    repository_root = Path(__file__).resolve().parents[1]

    payload = inspect_repository(repository_root)

    assert payload["passed"] is True
    assert payload["match_count"] == 0


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_historical_benchmark_is_preserved_without_active_legacy_configs():
    repository_root = Path(__file__).resolve().parents[1]
    benchmark_root = (
        repository_root
        / "results"
        / "bc_target_v2"
        / "selection_benchmark_20260721"
    )
    manifest_path = benchmark_root / "benchmark_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_sha256 = _sha256(manifest_path)
    assert manifest["path_migration"] == {
        "date": "2026-07-24",
        "baseline_git_commit": (
            "41708162a4f3e2c4fd89c30c47b6b35feb1b8d75"
        ),
        "original_reference_set_sha256": (
            "2709ba4bd103042d98f10370e38787715b22fd87bdafe8c526ba5047e2489b7f"
        ),
        "policy": (
            "retired SSH sibling prefixes normalized to active-checkout or "
            "archive access paths; experiment measurements unchanged"
        ),
    }

    config_root = repository_root / "experiments" / "configs"
    configs = sorted(config_root.glob("syncmate_small_selection_gu_*_v*.yaml"))
    assert manifest_sha256
    assert configs == []
