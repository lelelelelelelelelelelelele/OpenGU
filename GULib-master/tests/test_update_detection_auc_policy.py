import json
from pathlib import Path

import yaml

from scripts.gate_runs import check_cell
from experiments.run import _content_fingerprint
from utils.metric_policy import (
    update_detection_auc_enabled,
    update_detection_auc_result_value,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_complete_leaf(tmp_path: Path, mia_auc):
    (tmp_path / "attack.json").write_text(
        json.dumps({"results": {"random": {"mia_auc": mia_auc}}}),
        encoding="utf-8",
    )
    (tmp_path / "collateral.json").write_text(
        json.dumps({"results": [{"perf_before": 0.7, "gap": 0.1, "hop_decay": {}}]}),
        encoding="utf-8",
    )
    (tmp_path / "predictions.npz").write_bytes(b"test")
    (tmp_path / "_meta.json").write_text("{}", encoding="utf-8")


def test_policy_defaults_on_and_canonical_flag_wins():
    assert update_detection_auc_enabled({}) is True
    assert update_detection_auc_enabled({"run_mia": False}) is False
    assert update_detection_auc_enabled({"run_update_detection_auc": "false"}) is False
    assert update_detection_auc_enabled(
        {"run_update_detection_auc": True, "run_mia": False}
    ) is True
    assert update_detection_auc_result_value(
        {"run_update_detection_auc": False}, 0.77
    ) is None
    assert update_detection_auc_result_value(
        {"run_update_detection_auc": True}, 0.77
    ) == 0.77


def test_gate_accepts_null_only_when_auc_is_disabled(tmp_path):
    _write_complete_leaf(tmp_path, None)

    assert check_cell(
        tmp_path, "random", 0.0, 1.0, require_update_detection_auc=False
    ) == []
    assert any(
        "mia_auc not finite" in reason
        for reason in check_cell(
            tmp_path, "random", 0.0, 1.0, require_update_detection_auc=True
        )
    )


def test_gate_rejects_finite_auc_when_policy_is_disabled(tmp_path):
    _write_complete_leaf(tmp_path, 0.65)

    assert any(
        "must be null" in reason
        for reason in check_cell(
            tmp_path, "random", 0.0, 1.0, require_update_detection_auc=False
        )
    )


def test_primary_yaml_configs_make_dataset_scope_explicit():
    small = yaml.safe_load(
        (REPO_ROOT / "experiments/configs/phase_b_cora_gcn.yaml").read_text(
            encoding="utf-8"
        )
    )
    large = yaml.safe_load(
        (REPO_ROOT / "experiments/configs/phase_b_arxiv_T1_seed42.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert small["defaults"]["run_update_detection_auc"] is True
    assert large["defaults"]["run_update_detection_auc"] is False


def test_every_arxiv_phase_config_disables_optional_auc():
    for path in (REPO_ROOT / "experiments/configs").glob("phase_b_arxiv*.yaml"):
        cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert cfg["defaults"]["run_update_detection_auc"] is False, path.name


def test_cell_fingerprint_distinguishes_enabled_and_disabled_auc():
    base = {
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["random"],
        "seeds": [42],
        "defaults": {"run_update_detection_auc": True},
    }
    disabled = {
        **base,
        "defaults": {"run_update_detection_auc": False},
    }

    assert _content_fingerprint(base, "GIF", "random", 42) != _content_fingerprint(
        disabled, "GIF", "random", 42
    )
