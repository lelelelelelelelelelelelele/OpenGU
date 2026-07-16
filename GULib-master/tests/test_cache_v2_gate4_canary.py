"""Static and CPU-only contract tests for the fixed Cache V2 Gate 4 canary."""

from __future__ import annotations

import ast
import os
from pathlib import Path
import subprocess
import sys

import pytest

from scripts import cache_v2_gate4_canary as gate4


def _event(stage: str, timestamp: str):
    return {
        "timestamp": timestamp,
        "cell_id": "cora-gcn-gif-degree-seed42",
        "run_id": "gate4-run",
        "attempt": 1,
        "identity": {
            "dataset": "cora",
            "model": "GCN",
            "method": "GIF",
            "strategy": "degree",
            "seed": 42,
            "ratio": 0.05,
        },
        "stage": stage,
        "state": "completed",
    }


def test_gate4_config_is_one_cell_and_dataset_owned_by_experiment_layer():
    config = gate4._config()

    assert config["methods"] == ["GIF"]
    assert config["strategies"] == ["degree"]
    assert config["seeds"] == [42]
    assert config["processed_root"] == str(gate4.CANONICAL_PROCESSED_ROOT)
    assert config["run_root"] == "results/runs/__syncmate_gate4__"
    assert gate4.RUN_ROOT == (
        gate4.REPO_ROOT / "results" / "runs" / "__syncmate_gate4__"
    )
    assert gate4.EVIDENCE_ROOT not in gate4.RUN_ROOT.parents
    assert config["defaults"]["num_epochs"] == 5
    assert config["defaults"]["no_cache"] is True
    assert set(config["cache_v2"]) == {"mode", "store_root", "legacy_results_root"}


def test_gate4_wrapper_has_no_dataset_framework_or_download_imports():
    source = gate4.__file__
    tree = ast.parse(open(source, encoding="utf-8").read(), filename=source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)

    assert not any(
        name.split(".", 1)[0] in {"ogb", "torch_geometric", "dataset"}
        for name in imports
    )
    text = open(source, encoding="utf-8").read()
    assert "--allow-download" not in text
    assert "data/raw" not in text


def test_gate4_phase_projection_preserves_staged_runner_states():
    events = [
        _event("selection", "2026-07-17T01:00:00+00:00"),
        _event("attack", "2026-07-17T01:01:00+00:00"),
        _event("collateral", "2026-07-17T01:02:00+00:00"),
        _event("run", "2026-07-17T01:03:00+00:00"),
    ]

    assert gate4._phase_projection(events) == {
        "selection": "selection-only",
        "attack": "attack-only",
        "collateral": "collateral",
        "run": "complete",
    }


def test_gate4_cli_exposes_no_arbitrary_recipe_inputs():
    args = gate4._parser().parse_args(["--json"])
    assert args.json is True
    with pytest.raises(SystemExit):
        gate4._parser().parse_args(["--dataset-root", "data/raw/cora"])


def test_gate4_selection_commands_are_fixed_and_download_free():
    cold = list(gate4._selection_canary_args("cold", gate4.STORE_ROOT))
    warm = list(gate4._selection_canary_args("warm", gate4.STORE_ROOT))

    assert cold[2] == "cold"
    assert warm[2] == "warm"
    assert "--processed-root" in cold
    assert str(gate4.CANONICAL_PROCESSED_ROOT) in cold
    assert "--allow-download" not in cold
    assert "--dataset-root" not in cold


def test_gate4_wrapper_is_directly_executable_from_repo_root():
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(Path(gate4.__file__)), "--help"],
        cwd=gate4.REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "fixed, isolated Cache V2 Gate 4" in completed.stdout
