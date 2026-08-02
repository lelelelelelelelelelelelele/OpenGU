from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import syncmate_core


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYNC_DIR = PROJECT_ROOT / "scripts" / "syncmate"
CORE_ROOT = Path(syncmate_core.__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def adapter_module(monkeypatch):
    monkeypatch.syspath_prepend(str(SYNC_DIR))
    return load_module("opengu_adapter_m1_test", SYNC_DIR / "opengu_adapter.py")


@pytest.fixture
def candidate_module(monkeypatch):
    monkeypatch.syspath_prepend(str(SYNC_DIR))
    return load_module("opengu_syncmate_m1_test", SYNC_DIR / "syncmate_m1.py")


def test_candidate_wrapper_imports_independent_core(candidate_module):
    imported_core = Path(candidate_module.core_module_file).resolve()

    assert os.path.commonpath([str(imported_core), str(CORE_ROOT)]) == str(CORE_ROOT)
    assert os.path.commonpath([str(imported_core), str(SYNC_DIR)]) != str(SYNC_DIR)
    assert not hasattr(candidate_module, "run_job")
    assert not hasattr(candidate_module, "Recipe")


def test_opengu_recipe_preflight_and_acceptance_are_adapter_owned(
    adapter_module,
    tmp_path: Path,
):
    adapter = adapter_module.ADAPTER
    recipes = adapter.recipes()
    recipe = recipes["smoke"]
    config = tmp_path / recipe.config_path
    config.parent.mkdir(parents=True)
    config.write_text(
        (SYNC_DIR / "setup.example.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    preflight = adapter.preflight(recipe, tmp_path)
    acceptance = adapter.acceptance(
        {"status": "done", "project_acceptance": {"status": "not_evaluated"}},
        {"status": "verified", "artifacts": []},
    )

    assert set(recipes) == {"smoke"}
    assert recipe.argv == (
        "{python}",
        "scripts/syncmate/syncmate.py",
        "smoke",
        "--json",
    )
    assert recipe.config_sha256 == (
        "03fb31feae5edb3fde21b9eab2fcc892fecb764e05fafe44b38c753fdde9f8a1"
    )
    assert preflight["ready"] is True
    assert acceptance == {
        "accepted": False,
        "status": "not_evaluated",
        "formal_evidence": False,
        "reason": "execution done is not OpenGU project acceptance",
    }


def test_opengu_preflight_reports_config_mismatch_expected_observed_action(
    adapter_module,
    tmp_path: Path,
):
    adapter = adapter_module.ADAPTER
    recipe = adapter.recipes()["smoke"]
    config = tmp_path / recipe.config_path
    config.parent.mkdir(parents=True)
    config.write_text("version: changed\n", encoding="utf-8")

    result = adapter.preflight(recipe, tmp_path)

    assert result["ready"] is False
    assert result["expected"]["config_sha256"] == recipe.config_sha256
    assert result["observed"]["config_sha256"] != recipe.config_sha256
    assert result["action"] == "restore the reviewed OpenGU setup example"


def test_candidate_contract_cli_reports_adapter_and_external_core(
    candidate_module,
    capsys,
):
    assert candidate_module.main(["contract", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["adapter"] == "opengu"
    assert payload["recipe_ids"] == ["smoke"]
    assert Path(payload["core_module"]).resolve() == Path(syncmate_core.__file__).resolve()
    assert payload["core_contract"]["job"]["additional_fields"] is False


def test_candidate_gate1_smoke_is_temporary_and_non_formal(
    candidate_module,
    capsys,
):
    assert candidate_module.main(["smoke", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["passed"] is True
    assert payload["temporary"] is True
    assert payload["cleaned"] is True
    assert payload["formal_evidence"] is False
    assert payload["project_acceptance"] == "not_evaluated"
    assert not Path(payload["workdir"]).exists()


def test_candidate_gate2_runner_smoke_uses_clean_exact_compatibility_fixture(
    candidate_module,
    capsys,
):
    assert candidate_module.main(["runner-smoke", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["passed"] is True
    assert payload["temporary"] is True
    assert payload["cleaned"] is True
    assert payload["formal_evidence"] is False
    assert payload["fixture"]["compatibility_path"] == "scripts/syncmate/syncmate.py"
    assert payload["fixture"]["tracked_tree_clean_at_dispatch"] is True
    assert len(payload["job"]["expected_git_sha"]) == 40
    assert payload["job"]["expected_config_sha256"] == (
        "03fb31feae5edb3fde21b9eab2fcc892fecb764e05fafe44b38c753fdde9f8a1"
    )
    assert payload["receipt"]["status"] == "done"
    assert payload["receipt"]["command"][1:] == [
        "scripts/syncmate/syncmate.py",
        "smoke",
        "--json",
    ]
    assert payload["receipt"]["stdout_sha256"]
    assert payload["receipt"]["stderr_sha256"]
    assert payload["receipt"]["manifest"]["status"] == "verified"
    assert payload["receipt"]["project_acceptance"] == {
        "status": "not_evaluated",
        "owner": "project",
    }
    assert payload["runtime_evidence"]["receipt_sha256"]
    assert payload["runtime_evidence"]["manifest_sha256"]
    assert payload["execution_output"]["passed"] is True
    assert payload["execution_output"]["formal_evidence"] is False


def test_candidate_cli_runs_in_a_fresh_process_with_external_core():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(CORE_ROOT), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)
    completed = subprocess.run(
        [sys.executable, str(SYNC_DIR / "syncmate_m1.py"), "contract", "--json"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["adapter"] == "opengu"
    assert os.path.commonpath([payload["core_module"], str(CORE_ROOT)]) == str(CORE_ROOT)
