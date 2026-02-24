import json
from pathlib import Path

import run_experiments


def _write_json(path: Path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_validate_experiment_json_missing_file(tmp_path):
    expected = {"im_v4", "hybrid_v4"}
    is_complete, reason, parsed = run_experiments._validate_experiment_json(
        tmp_path / "missing.json",
        expected_strategies=expected,
        validation_mode="strict",
    )
    assert is_complete is False
    assert reason == "missing_file"
    assert parsed is None


def test_validate_experiment_json_invalid_json(tmp_path):
    json_path = tmp_path / "bad.json"
    json_path.write_text("{not-valid-json", encoding="utf-8")
    expected = {"im_v4", "hybrid_v4"}
    is_complete, reason, parsed = run_experiments._validate_experiment_json(
        json_path,
        expected_strategies=expected,
        validation_mode="strict",
    )
    assert is_complete is False
    assert reason == "invalid_json"
    assert parsed is None


def test_validate_experiment_json_missing_results(tmp_path):
    json_path = tmp_path / "no_results.json"
    _write_json(json_path, {"config": {"strategies": "im_v4,hybrid_v4"}})
    expected = {"im_v4", "hybrid_v4"}
    is_complete, reason, parsed = run_experiments._validate_experiment_json(
        json_path,
        expected_strategies=expected,
        validation_mode="strict",
    )
    assert is_complete is False
    assert reason == "missing_results"
    assert isinstance(parsed, dict)


def test_validate_experiment_json_strategy_mismatch(tmp_path):
    json_path = tmp_path / "legacy.json"
    _write_json(
        json_path,
        {
            "config": {"strategies": "im,hybrid"},
            "results": {"im": {}, "hybrid": {}},
        },
    )
    expected = {"im_v4", "hybrid_v4"}
    is_complete, reason, parsed = run_experiments._validate_experiment_json(
        json_path,
        expected_strategies=expected,
        validation_mode="strict",
    )
    assert is_complete is False
    assert reason == "strategy_mismatch"
    assert isinstance(parsed, dict)


def test_validate_experiment_json_complete_allows_extra_strategies(tmp_path):
    json_path = tmp_path / "complete.json"
    _write_json(
        json_path,
        {
            "config": {"strategies": "im_v4,hybrid_v4"},
            "results": {
                "im_v4": {},
                "hybrid_v4Strategy": {},
                "randomStrategy": {},
            },
        },
    )
    expected = {"im_v4", "hybrid_v4"}
    is_complete, reason, parsed = run_experiments._validate_experiment_json(
        json_path,
        expected_strategies=expected,
        validation_mode="strict",
    )
    assert is_complete is True
    assert reason == "complete"
    assert isinstance(parsed, dict)


def test_scan_missing_items_grid_respects_validation_mode(tmp_path):
    run_dir = tmp_path / "20260224_000000_seed42"
    run_dir.mkdir(parents=True)
    json_path = run_dir / "GIF_cora_GCN_r0.05_s42.json"
    _write_json(
        json_path,
        {
            "config": {"strategies": "im,hybrid"},
            "results": {"im": {}, "hybrid": {}},
        },
    )
    config = {
        "methods": ["GIF"],
        "datasets": ["cora"],
        "models": ["GCN"],
        "ratios": [0.05],
        "strategies": "im_v4,hybrid_v4",
    }

    _, strict_missing = run_experiments._scan_missing_items_grid(
        run_dir=run_dir,
        config=config,
        seed=42,
        validation_mode="strict",
    )
    assert len(strict_missing) == 1
    assert strict_missing[0]["missing_reason"] == "strategy_mismatch"

    _, legacy_missing = run_experiments._scan_missing_items_grid(
        run_dir=run_dir,
        config=config,
        seed=42,
        validation_mode="legacy_missing_only",
    )
    assert legacy_missing == []


def test_run_repair_uses_current_config_strategies_and_records_meta(tmp_path, monkeypatch):
    run_dir = tmp_path / "20260224_000000_seed42"
    run_dir.mkdir(parents=True)
    _write_json(
        run_dir / "_summary.json",
        {
            "config": {"strategies": "im,hybrid"},
            "results": {},
        },
    )
    _write_json(
        run_dir / "GIF_cora_GCN_r0.05_s42.json",
        {
            "config": {"strategies": "im,hybrid"},
            "results": {"im": {}, "hybrid": {}},
        },
    )

    captured = []

    def _fake_run_single_experiment(
        method,
        dataset,
        model,
        strategies,
        ratio,
        cuda,
        output_dir,
        random_seed,
        **kwargs,
    ):
        captured.append(strategies)
        save_path = Path(output_dir) / f"{method}_{dataset}_{model}_r{ratio}_s{random_seed}.json"
        _write_json(
            save_path,
            {
                "config": {"strategies": strategies},
                "results": {"im_v4": {}, "hybrid_v4": {}},
            },
        )
        return {"ok": True}

    monkeypatch.setattr(run_experiments, "run_single_experiment", _fake_run_single_experiment)

    run_experiments._run_repair(
        config={
            "name": "test",
            "methods": ["GIF"],
            "datasets": ["cora"],
            "models": ["GCN"],
            "ratios": [0.05],
            "strategies": "im_v4,hybrid_v4",
        },
        cuda=0,
        repair_dir=str(run_dir),
        seed_list=[42],
        repair_from="grid",
        repair_select="latest_per_seed",
        repair_dry_run=False,
        validation_mode="strict",
    )

    assert captured == ["im_v4,hybrid_v4"]
    summary = json.loads((run_dir / "_summary.json").read_text(encoding="utf-8"))
    assert summary["config"]["strategies"] == "im_v4,hybrid_v4"
    assert summary["completed"] == 1
    assert summary["failed"] == 0
    meta = summary["repair_meta"][-1]
    assert meta["validation_mode"] == "strict"
    assert meta["target_strategies"] == "im_v4,hybrid_v4"
    assert meta["existing_strategies_source"] == "summary"
    assert meta["missing_by_reason"]["strategy_mismatch"] == 1
