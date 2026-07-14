import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from attack.attack_result import AttackResult
from attack.result_cache import ResultCache

from scripts.evaluation.reporting.events import (
    ENV_EVENT_PATH,
    ENV_STATUS_HTML_PATH,
    ENV_STATUS_MD_PATH,
    append_event,
    artifact_ref,
    build_event,
    cache_observation,
    make_cell_id,
    make_config_fingerprint,
    new_run_id,
    read_event_stream,
)
from scripts.evaluation.reporting.reader import parse_legacy_markdown
from scripts.evaluation.reporting.summary import build_status_rows
from scripts.evaluation.reporting.writer import (
    append_report_entry,
    record_attack_results,
    record_collateral_results,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "auto_report"


def _identity(strategy="degree"):
    return {
        "dataset": "cora",
        "model": "GCN",
        "method": "GIF",
        "strategy": strategy,
        "ratio": 0.05,
        "seed": 42,
        "k": 5,
    }


def _paths(tmp_path, monkeypatch):
    event_path = tmp_path / "auto_report.events.jsonl"
    markdown_path = tmp_path / "auto_report_status.md"
    html_path = tmp_path / "auto_report_status.html"
    monkeypatch.setenv(ENV_EVENT_PATH, str(event_path))
    monkeypatch.setenv(ENV_STATUS_MD_PATH, str(markdown_path))
    monkeypatch.setenv(ENV_STATUS_HTML_PATH, str(html_path))
    return event_path, markdown_path, html_path


def test_cell_and_config_identity_are_stable_and_separate():
    identity = _identity()
    assert make_cell_id(identity) == make_cell_id(dict(reversed(list(identity.items()))))
    assert make_config_fingerprint({"epochs": 10}) != make_config_fingerprint({"epochs": 20})
    assert make_cell_id(identity) == make_cell_id(identity)


def test_exact_transition_and_repeated_skip_are_deduplicated(tmp_path, monkeypatch):
    event_path, markdown_path, html_path = _paths(tmp_path, monkeypatch)
    identity = _identity()
    cell_id = make_cell_id(identity)
    run_id = new_run_id(cell_id)
    event = build_event(
        identity=identity,
        stage="attack",
        state="completed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=run_id,
    )
    assert append_event(event, event_path=event_path).written is True
    assert append_event(event, event_path=event_path).written is False

    cache = [cache_observation(
        cache_type="run_artifact",
        outcome="hit",
        recipe={"config_fingerprint": "fp-a"},
        artifact=artifact_ref(path="cell", artifact_type="artifact"),
        hit_source="cell",
        lookup_policy="complete_files_and_fingerprint",
        authoritative=True,
        write_outcome="reused",
    )]
    first_skip = build_event(
        identity=identity,
        stage="run",
        state="skipped",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=new_run_id(cell_id),
        cache=cache,
        metadata={"reason": "complete cell already materialized"},
    )
    second_skip = build_event(
        identity=identity,
        stage="run",
        state="skipped",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=new_run_id(cell_id),
        cache=cache,
        metadata={"reason": "complete cell already materialized"},
    )
    assert first_skip["dedup_key"] == second_skip["dedup_key"]
    assert append_event(first_skip, event_path=event_path).written is True
    assert append_event(second_skip, event_path=event_path).written is False
    changed_skip = build_event(
        identity=identity,
        stage="run",
        state="skipped",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=new_run_id(cell_id),
        cache=cache,
        artifacts=[artifact_ref(
            path="attack.json", artifact_type="evaluation", content_hash="changed"
        )],
        metadata={"reason": "complete cell already materialized"},
    )
    assert changed_skip["dedup_key"] != first_skip["dedup_key"]
    assert append_event(changed_skip, event_path=event_path).written is True
    events, warnings = read_event_stream(event_path)
    assert len(events) == 3
    assert warnings == []
    assert "Events parsed: 3" in markdown_path.read_text(encoding="utf-8")
    assert "Events parsed: 3" in html_path.read_text(encoding="utf-8")


def test_partial_workflow_fixture_projects_selection_attack_complete_and_failed():
    events, warnings = read_event_stream(FIXTURE_DIR / "events_partial.jsonl")
    rows, total = build_status_rows(events, max_cells=20)
    assert warnings == []
    assert total == 4
    states = {row["cell_id"]: row["state"] for row in rows}
    assert states == {
        "cell_selection": "selection-only",
        "cell_attack": "attack-only",
        "cell_complete": "complete",
        "cell_failed": "failed:collateral",
    }


def test_legacy_v1_v2_fixture_is_parsed_without_migration():
    records, warnings = parse_legacy_markdown(FIXTURE_DIR / "legacy_v1_v2.md")
    assert warnings == []
    assert [(record["schema_version"], record["kind"]) for record in records] == [
        (1, "experiment"),
        (2, "session"),
        (2, "decision"),
    ]
    assert records[0]["fields"]["任务"].startswith("dataset=cora")


def test_legacy_v1_writer_api_remains_available(tmp_path):
    report_path = tmp_path / "legacy.md"
    append_report_entry(
        script="fixture.py",
        dataset="cora",
        model="GCN",
        method="GIF",
        ratio="0.05",
        status="OK",
        log_file="fixture.log",
        report_path=str(report_path),
    )
    records, warnings = parse_legacy_markdown(report_path)
    assert warnings == []
    assert len(records) == 1
    assert records[0]["kind"] == "experiment"


def test_result_cache_hit_is_not_replayed_as_current_selection_hit(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=True,
        selection_cache_key="old-selection",
        selection_cache_source="old-selection.json",
        result_cache_hit=True,
        result_cache_key="result-key",
        result_cache_source="result.json",
        result_cache_lookup_mode="legacy_primary_hash",
        f1_before=0.9,
        f1_after=0.8,
        f1_drop=0.1,
        unlearn_time=1.0,
        total_time=2.0,
        mia_auc=0.55,
    )
    record_attack_results(
        method="GIF",
        dataset="cora",
        model="GCN",
        strategies=["degree"],
        unlearn_ratio=0.05,
        k=2,
        seed=42,
        results=[result],
        save_path="attack.json",
        event_path=str(event_path),
    )
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert [event["stage"] for event in events] == ["attack"]
    assert events[0]["cache"][0]["type"] == "result"
    assert events[0]["cache"][0]["outcome"] == "hit"


def test_result_and_selection_misses_are_one_terminal_event_each(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=False,
        selection_cache_key="selection-key",
        selection_cache_source="selection.json",
        selection_cache_lookup_mode="exact",
        selection_cache_source_k=None,
        selection_time=0.5,
        selection_reuse_time=None,
        result_cache_hit=False,
        result_cache_key="result-key",
        result_cache_source="result.json",
        result_cache_lookup_mode="legacy_primary_hash",
        f1_before=0.9,
        f1_after=0.8,
        f1_drop=0.1,
        unlearn_time=1.0,
        total_time=2.0,
        mia_auc=0.55,
    )
    record_attack_results(
        method="GIF",
        dataset="cora",
        model="GCN",
        strategies=["degree"],
        unlearn_ratio=0.05,
        k=2,
        seed=42,
        results=[result],
        event_path=str(event_path),
    )
    events, _warnings = read_event_stream(event_path)
    assert [(event["stage"], event["cache"][0]["outcome"]) for event in events] == [
        ("selection", "miss"),
        ("attack", "miss"),
    ]


def test_failed_attack_result_is_a_failed_terminal_event(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=False,
        selection_cache_key="selection-key",
        selection_cache_source="selection.json",
        selection_time=0.5,
        selection_reuse_time=None,
        result_cache_hit=False,
        result_cache_key=None,
        result_cache_source=None,
        f1_before=None,
        f1_after=0.0,
        f1_drop=None,
        unlearn_time=0.0,
        total_time=1.0,
        mia_auc=None,
        failed=True,
        failure_reason="fixture crash",
    )
    record_attack_results(
        method="GIF",
        dataset="cora",
        model="GCN",
        strategies=["degree"],
        unlearn_ratio=0.05,
        k=2,
        seed=42,
        results=[result],
        event_path=str(event_path),
    )
    events, _warnings = read_event_stream(event_path)
    assert events[-1]["event_type"] == "attack.failed"
    assert events[-1]["error"]["message"] == "fixture crash"


def test_result_cache_exposes_hit_source_without_changing_get(tmp_path):
    cache = ResultCache(cache_dir=str(tmp_path / "cache"), max_age_days=0)
    config = {
        "dataset_name": "cora",
        "base_model": "GCN",
        "unlearning_methods": "GIF",
        "unlearn_ratio": 0.05,
        "random_seed": 42,
        "seed": 42,
        "strategy_name": "degree",
        "k": 2,
    }
    result = AttackResult(
        strategy_name="degree",
        selected_nodes=torch.tensor([1, 2]),
        f1_before=0.9,
        f1_after=0.8,
        unlearn_time=1.0,
        total_time=2.0,
    )
    saved_path = cache.save(result, config)
    loaded, provenance = cache.get_with_provenance(config)
    assert loaded is not None
    assert provenance["source_file"] == saved_path
    assert provenance["cache_key"] == Path(saved_path).stem
    assert provenance["lookup_policy"] == "legacy_primary_hash"
    assert cache.get(config) is not None


def test_collateral_partial_results_record_success_and_missing_failure(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    record_collateral_results(
        dataset="cora",
        model="GCN",
        method="GIF",
        ratio=0.05,
        seed=42,
        results=[{
            "strategy": "degree",
            "gap": 0.1,
            "gap_pct": 1.0,
            "mean_pred_shift": 0.01,
            "max_pred_shift": 0.1,
            "fraction_flipped": 0.02,
        }],
        output_path="collateral.json",
        requested_strategies=["degree", "pagerank"],
        cache_provenance={
            "degree": {
                "outcome": "hit",
                "cache_key": "degree-key",
                "source_file": "degree.json",
                "lookup_policy": "legacy_primary_hash",
            },
            "pagerank": {
                "outcome": "miss",
                "miss_reason": "not found",
            },
        },
        event_path=str(event_path),
    )
    events, _warnings = read_event_stream(event_path)
    assert [(event["identity"]["strategy"], event["state"]) for event in events] == [
        ("pagerank", "failed"),
        ("degree", "completed"),
    ]
    assert events[0]["cache"][0]["outcome"] == "miss"
    assert events[1]["cache"][0]["outcome"] == "hit"


def _load_experiment_runner():
    path = Path(__file__).parents[1] / "experiments" / "run.py"
    spec = importlib.util.spec_from_file_location("opengu_experiments_run", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_runner_records_shared_run_id_and_retry(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    runner = _load_experiment_runner()
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    out_dir = tmp_path / "cell"
    monkeypatch.setattr(runner, "cell_dir", lambda *_args, **_kwargs: out_dir)
    monkeypatch.setattr(runner, "_git_sha", lambda: "abc123")
    cfg = {
        "name": "fixture",
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "defaults": {"run_collateral": False},
    }
    calls = {"count": 0}

    def fake_run(command, cwd, env):
        calls["count"] += 1
        if calls["count"] == 1:
            return SimpleNamespace(returncode=7)
        Path(command[command.index("--save_path") + 1]).write_text("{}", encoding="utf-8")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run_cell(cfg, "GIF", "degree", 42, force=False, dry_run=False) == "failed_attack"
    assert runner.run_cell(cfg, "GIF", "degree", 42, force=False, dry_run=False) == "completed"
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    run_starts = [event for event in events if event["event_type"] == "run.started"]
    assert [event["attempt"] for event in run_starts] == [1, 2]
    retrying = [event for event in events if event["event_type"] == "run.retrying"]
    assert len(retrying) == 1
    second_run_id = run_starts[1]["run_id"]
    assert all(
        event["run_id"] == second_run_id
        for event in events
        if event["attempt"] == 2
    )
    assert events[-1]["event_type"] == "run.completed"


def test_runner_dry_run_emits_no_audit_event(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    runner = _load_experiment_runner()
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(runner, "cell_dir", lambda *_args, **_kwargs: tmp_path / "missing-cell")
    monkeypatch.setattr(runner, "_git_sha", lambda: "abc123")
    cfg = {
        "name": "fixture",
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "defaults": {"run_collateral": False},
    }
    assert runner.run_cell(cfg, "GIF", "degree", 42, force=False, dry_run=True) == "would_run"
    assert not event_path.exists()
