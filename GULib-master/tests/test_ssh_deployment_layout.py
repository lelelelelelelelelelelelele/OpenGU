"""Contracts for the AutoDL deployment-root boundary."""

from __future__ import annotations

from pathlib import Path

import pytest

from experiments import path_policy
from experiments import run as experiment_runner
from scripts.validate_ssh_deployment_layout import inspect_layout


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
