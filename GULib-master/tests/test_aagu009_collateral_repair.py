from pathlib import Path
import subprocess
import sys

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ITEM_ROOT = REPO_ROOT / ".workblock" / "items" / "AAGU-009"


def test_aagu009_repair_scope_is_exact_and_reversible():
    scope_path = ITEM_ROOT / "evidence" / "repair-scope.yaml"
    scope = yaml.safe_load(scope_path.read_text(encoding="utf-8"))

    assert scope["schema"] == "opengu.aagu009.repair-scope.v1"
    assert scope["block_id"] == "AAGU-009"
    assert scope["remote_action"] == "quarantine_whole_leaf_then_rerun"
    assert scope["destructive_actions"]["delete_allowed"] is False
    assert scope["destructive_actions"]["force_allowed"] is False

    matrix = scope["matrix"]
    expected_cells = (
        len(matrix["base_models"])
        * len(matrix["methods"])
        * len(matrix["strategies"])
        * len(matrix["seeds"])
    )
    assert expected_cells == 120
    assert scope["expected_cells"] == expected_cells
    assert scope["cache_policy"] == {
        "result_cache": "preserve",
        "selection_cache": "preserve",
        "cache_v2": "read_only",
    }

    assert scope["source_configs"] == [
        "experiments/configs/phase_b_cora_gcn.yaml",
        "experiments/configs/phase_b_cora_gat.yaml",
    ]
    for relative_config, base_model in zip(scope["source_configs"], matrix["base_models"]):
        config = yaml.safe_load((REPO_ROOT / relative_config).read_text(encoding="utf-8"))
        assert config["dataset"] == matrix["dataset"]
        assert config["base_model"] == base_model
        assert config["ratio"] == matrix["ratio"]
        assert config["strategies"] == matrix["strategies"]
        assert config["seeds"] == matrix["seeds"]
        assert set(matrix["methods"]).issubset(config["methods"])

    total_config_cells = sum(
        len(yaml.safe_load((REPO_ROOT / path).read_text(encoding="utf-8"))["methods"])
        * len(matrix["strategies"])
        * len(matrix["seeds"])
        for path in scope["source_configs"]
    )
    assert total_config_cells - expected_cells == 240


def test_aagu009_destructive_legacy_helpers_are_retired():
    assert not (REPO_ROOT / "scripts" / "redo_collateral_if_family.py").exists()
    assert not (REPO_ROOT / "scripts" / "cleanup_if_family_collateral.py").exists()


def test_if_writeback_verifier_proves_loaded_source_identity():
    completed = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", "scripts/verify_if_writeback_patch.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "loaded GIF source:" in completed.stdout
    assert "loaded IDEA source:" in completed.stdout
    assert "ALL CHECKS PASSED" in completed.stdout
