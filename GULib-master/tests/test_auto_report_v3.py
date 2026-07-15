import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from attack.attack_result import AttackResult
from attack.result_cache import ResultCache

from scripts.evaluation.reporting.baseline import read_baseline
from scripts.evaluation.reporting.events import (
    DEFAULT_STATUS_HTML_PATH,
    DEFAULT_STATUS_MD_PATH,
    ENV_EVENT_PATH,
    ENV_IDENTITY_JSON,
    ENV_STATUS_HTML_PATH,
    ENV_STATUS_MD_PATH,
    EventStreamCorruptionError,
    EventValidationError,
    append_event,
    artifact_ref,
    build_event,
    cache_observation,
    make_cell_id,
    make_config_fingerprint,
    new_run_id,
    normalize_identity,
    read_event_stream,
)
from scripts.evaluation.reporting.reader import parse_legacy_markdown
from scripts.evaluation.reporting.summary import build_status_rows, write_status_views
from scripts.evaluation.reporting.writer import (
    LegacyReportWriteDisabledError,
    append_report_entry,
    record_attack_results,
    record_collateral_results,
    record_evaluation_result,
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
    markdown_path = tmp_path / "auto_report.md"
    html_path = tmp_path / "auto_report.html"
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


def test_run_cannot_complete_after_a_failed_stage(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    identity = _identity()
    cell_id = make_cell_id(identity)
    run_id = new_run_id(cell_id)
    failed = build_event(
        identity=identity,
        stage="attack",
        state="failed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=run_id,
        error={"type": "fixture", "message": "boom", "retryable": True},
    )
    append_event(failed, event_path=event_path)
    completed = build_event(
        identity=identity,
        stage="run",
        state="completed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=run_id,
    )
    with pytest.raises(EventValidationError, match="after attack.failed"):
        append_event(completed, event_path=event_path)
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert [event["event_type"] for event in events] == ["attack.failed"]


def test_failed_stage_dominates_inconsistent_historical_run_completion():
    identity = _identity()
    cell_id = make_cell_id(identity)
    run_id = new_run_id(cell_id)
    failed = build_event(
        identity=identity,
        stage="attack",
        state="failed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=run_id,
        error={"type": "fixture", "message": "boom", "retryable": True},
    )
    completed = build_event(
        identity=identity,
        stage="run",
        state="completed",
        producer="legacy-test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cell_id=cell_id,
        run_id=run_id,
    )
    rows, total = build_status_rows([failed, completed])
    assert total == 1
    assert rows[0]["state"] == "failed:attack"


def test_repeated_result_cache_hit_is_compressed_across_new_run_ids(tmp_path, monkeypatch):
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
    kwargs = {
        "method": "GIF",
        "dataset": "cora",
        "model": "GCN",
        "strategies": ["degree"],
        "unlearn_ratio": 0.05,
        "k": 2,
        "seed": 42,
        "results": [result],
        "save_path": "attack.json",
        "event_path": str(event_path),
    }
    record_attack_results(**kwargs)
    record_attack_results(**kwargs)
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert [event["event_type"] for event in events] == ["attack.completed"]
    assert events[0]["metadata"]["stage_execution"] == "cache_reuse"


def test_repeated_selection_hit_is_compressed_but_new_attack_compute_is_kept(
    tmp_path, monkeypatch
):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=True,
        selection_cache_key="selection-key",
        selection_cache_source="selection.json",
        selection_cache_lookup_mode="exact",
        selection_time=0.5,
        selection_reuse_time=0.001,
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
    kwargs = {
        "method": "GIF",
        "dataset": "cora",
        "model": "GCN",
        "strategies": ["degree"],
        "unlearn_ratio": 0.05,
        "k": 2,
        "seed": 42,
        "results": [result],
        "event_path": str(event_path),
    }
    record_attack_results(**kwargs)
    record_attack_results(**kwargs)
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert [event["event_type"] for event in events].count("selection.completed") == 1
    assert [event["event_type"] for event in events].count("attack.completed") == 2


def test_append_fails_closed_when_existing_stream_is_corrupt(tmp_path):
    event_path = tmp_path / "auto_report.events.jsonl"
    original = b'{"schema":"opengu.autoreport.event"\n'
    event_path.write_bytes(original)
    event = build_event(
        identity=_identity(),
        stage="attack",
        state="completed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
    )
    with pytest.raises(EventStreamCorruptionError, match="refusing to append"):
        append_event(event, event_path=event_path, refresh=False)
    assert event_path.read_bytes() == original


def test_append_rejects_event_tampering_after_build(tmp_path):
    event = build_event(
        identity=_identity(),
        stage="attack",
        state="completed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
    )
    event["config_fingerprint"] = "tampered"
    with pytest.raises(EventValidationError, match="dedup_key"):
        append_event(event, event_path=tmp_path / "events.jsonl", refresh=False)


def test_failed_and_retrying_events_require_structured_evidence():
    with pytest.raises(EventValidationError, match="error.type and error.message"):
        build_event(
            identity=_identity(),
            stage="attack",
            state="failed",
            producer="test",
            config_fingerprint="fp-a",
            git_sha="abc",
            error={"type": "BOOM"},
        )
    with pytest.raises(EventValidationError, match="retrying event requires"):
        build_event(
            identity=_identity(),
            stage="run",
            state="retrying",
            producer="test",
            config_fingerprint="fp-a",
            git_sha="abc",
            attempt=2,
        )


def test_concurrent_appends_leave_projection_at_latest_stream_length(tmp_path, monkeypatch):
    event_path, markdown_path, html_path = _paths(tmp_path, monkeypatch)
    events = [
        build_event(
            identity=_identity(strategy="degree-{0}".format(index)),
            stage="attack",
            state="completed",
            producer="worker-{0}".format(index),
            config_fingerprint="fp-{0}".format(index),
            git_sha="abc",
        )
        for index in range(8)
    ]

    def write(event):
        return append_event(event, event_path=event_path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(write, events))
    parsed, warnings = read_event_stream(event_path)
    assert warnings == []
    assert len(parsed) == 8
    assert all(result.written for result in results)
    assert "Events parsed: 8" in markdown_path.read_text(encoding="utf-8")
    assert "Events parsed: 8" in html_path.read_text(encoding="utf-8")


def test_runner_identity_envelope_keeps_child_identity_and_cell_id_consistent(
    tmp_path, monkeypatch
):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    runner_identity = _identity()
    runner_identity["k"] = None
    cell_id = make_cell_id(runner_identity)
    monkeypatch.setenv(ENV_IDENTITY_JSON, json.dumps(runner_identity))
    monkeypatch.setenv("OPENGU_AUTOREPORT_CELL_ID", cell_id)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=False,
        selection_cache_key="selection-key",
        selection_cache_source="selection.json",
        result_cache_hit=False,
        result_cache_key="result-key",
        result_cache_source="result.json",
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
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert events
    assert all(event["identity"] == normalize_identity(runner_identity) for event in events)
    assert all(event["cell_id"] == make_cell_id(event["identity"]) for event in events)


def test_human_cache_summary_names_authority_source_policy_and_recipe():
    identity = _identity()
    event = build_event(
        identity=identity,
        stage="selection",
        state="completed",
        producer="test",
        config_fingerprint="fp-a",
        git_sha="abc",
        cache=[cache_observation(
            cache_type="selection",
            outcome="hit",
            recipe={"strategy": "degree", "k": 5},
            recipe_hash="a" * 64,
            artifact=artifact_ref(
                artifact_id="sel_12345678_90abcdef",
                artifact_type="selection",
                recipe_hash="a" * 64,
                content_hash="b" * 64,
            ),
            hit_source="cache_v2:sel_12345678_90abcdef",
            lookup_policy="cache_v2_exact_artifact_id",
            authoritative=True,
            write_outcome="reused",
        ), cache_observation(
            cache_type="result",
            outcome="hit",
            recipe={"strategy": "degree", "legacy_cache_key": "result-key-123456"},
            artifact=artifact_ref(path="result.json", artifact_type="evaluation"),
            hit_source="result.json",
            lookup_policy="legacy_primary_hash",
            authoritative=False,
            write_outcome="reused",
        )],
    )
    rows, total = build_status_rows([event])
    assert total == 1
    cache_text = rows[0]["cache"]
    assert "selection:hit[authoritative]" in cache_text
    assert "sel_12345678_90abcdef" in cache_text
    assert "cache_v2_exact_artifact_id" in cache_text
    assert "recipe=aaaaaaaaaaaa" in cache_text
    assert "result:hit[legacy/non-authoritative]" in cache_text
    assert "legacy_primary_hash" in cache_text
    assert "legacy_key=result-key-1" in cache_text


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
    with pytest.warns(DeprecationWarning):
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
    assert "下一步建议" not in report_path.read_text(encoding="utf-8")


def test_legacy_writer_cannot_append_to_live_auto_report_by_default():
    with pytest.raises(LegacyReportWriteDisabledError):
        append_report_entry(
            script="fixture.py",
            dataset="cora",
            model="GCN",
            method="GIF",
            ratio="0.05",
            status="OK",
            log_file="fixture.log",
        )


def test_production_baseline_matches_frozen_archive():
    baseline_path = Path(__file__).parents[1] / "results" / "_journal" / "auto_report_baseline.json"
    baseline, warnings = read_baseline(baseline_path)
    assert warnings == []
    assert baseline["archive"]["lines"] == 19020
    assert baseline["archive"]["legacy_entries"] == 2015
    assert baseline["archive"]["decision_entries"] == 0
    assert baseline["policy"]["fixed_next_step"] == "retired"
    assert any(item["status"] == "duplicate-probe" for item in baseline["items"])
    assert any(item["status"] == "historical-verified" for item in baseline["items"])


def test_new_auto_report_names_and_baseline_projection(tmp_path):
    assert DEFAULT_STATUS_MD_PATH.name == "auto_report.md"
    assert DEFAULT_STATUS_HTML_PATH.name == "auto_report.html"
    event_path = tmp_path / "auto_report.events.jsonl"
    markdown_path = tmp_path / "auto_report.md"
    html_path = tmp_path / "auto_report.html"
    baseline_path = Path(__file__).parents[1] / "results" / "_journal" / "auto_report_baseline.json"
    write_status_views(
        event_path=event_path,
        markdown_path=markdown_path,
        html_path=html_path,
        baseline_path=baseline_path,
    )
    markdown = markdown_path.read_text(encoding="utf-8")
    browser = html_path.read_text(encoding="utf-8")
    assert "## Legacy baseline" in markdown
    assert "No V3 events yet" in markdown
    assert "Fixed next-step prose is retired" in browser


def test_legacy_evaluation_runner_uses_v3_skip_dedup(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    kwargs = {
        "script": "run_ratio05.py",
        "dataset": "cora",
        "model": "GCN",
        "method": "GIF",
        "ratio": "0.05",
        "status": "SKIP",
        "log_file": "strict-ok.log",
        "event_path": str(event_path),
    }
    record_evaluation_result(**kwargs)
    record_evaluation_result(**kwargs)
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert len(events) == 1
    assert events[0]["event_type"] == "run.skipped"
    assert events[0]["cache"][0]["type"] == "run_artifact"


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


def test_v2_selection_hit_is_authoritative_and_identifies_artifact(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    result = SimpleNamespace(
        strategy_name="degree",
        selected_nodes=[1, 2],
        selection_cache_hit=True,
        selection_cache_source="v2/payload.json",
        selection_cache_lookup_mode="cache_v2_exact_artifact_id",
        selection_artifact_id="sel_12345678_90abcdef",
        selection_recipe_hash="a" * 64,
        selection_content_hash="b" * 64,
        selection_authoritative=True,
        selection_time=0.0,
        selection_reuse_time=0.001,
        result_cache_hit=None,
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
        cache_enabled=False,
    )
    events, _warnings = read_event_stream(event_path)
    selection = events[0]["cache"][0]
    assert selection["type"] == "selection"
    assert selection["outcome"] == "hit"
    assert selection["authoritative"] is True
    assert selection["artifact"]["artifact_id"] == result.selection_artifact_id


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
        Path(command[command.index("--save_path") + 1]).write_text(
            json.dumps({"results": {"degree": {"failed": False}}}),
            encoding="utf-8",
        )
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


def test_runner_rejects_empty_attack_payload_before_collateral(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    runner = _load_experiment_runner()
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    out_dir = tmp_path / "cell"
    monkeypatch.setattr(runner, "cell_dir", lambda *_args, **_kwargs: out_dir)
    monkeypatch.setattr(runner, "_git_sha", lambda: "abc123")
    cfg = {
        "name": "fixture-empty-attack",
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "defaults": {"run_collateral": True},
    }
    calls = []

    def fake_run(command, cwd, env):
        calls.append(command)
        Path(command[command.index("--save_path") + 1]).write_text(
            json.dumps({"results": {}}), encoding="utf-8"
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run_cell(
        cfg, "GIF", "degree", 42, force=False, dry_run=False
    ) == "failed_attack"
    assert len(calls) == 1
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    assert events[-1]["event_type"] == "run.failed"
    assert events[-1]["error"]["type"] == "INVALID_ATTACK_ARTIFACT"
    assert not any(event["stage"] == "collateral" for event in events)
    assert not any(event["event_type"] == "run.completed" for event in events)


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


def test_runner_v2_selection_passes_one_artifact_without_legacy_fallback(tmp_path, monkeypatch):
    event_path, _markdown_path, _html_path = _paths(tmp_path, monkeypatch)
    runner = _load_experiment_runner()
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    out_dir = tmp_path / "cell"
    monkeypatch.setattr(runner, "cell_dir", lambda *_args, **_kwargs: out_dir)
    monkeypatch.setattr(runner, "_git_sha", lambda: "abc123")
    cfg = {
        "name": "fixture-v2",
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "defaults": {"run_collateral": False},
        "cache_v2": {"mode": "selection", "store_root": "v2-store"},
    }
    selection = {
        "store_root": str(tmp_path / "v2-store"),
        "artifact_id": "sel_12345678_90abcdef",
        "artifact_type": "selection",
        "recipe_hash": "a" * 64,
        "content_hash": "b" * 64,
        "source_file": str(tmp_path / "v2-store" / "payload.json"),
        "hit_source": "cache_v2:sel_12345678_90abcdef",
        "lookup_policy": "cache_v2_exact_artifact_id",
        "authoritative": True,
        "write_outcome": "reused",
        "strategy": "degree",
        "k": 2,
        "selected_node_count": 2,
    }
    commands = []
    child_envs = []

    def fake_run(command, cwd, env):
        commands.append(command)
        child_envs.append(env)
        Path(command[command.index("--save_path") + 1]).write_text(
            json.dumps({"results": {"degree": {"failed": False}}}),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    assert runner.run_cell(
        cfg,
        "GIF",
        "degree",
        42,
        force=False,
        dry_run=False,
        selection_artifact=selection,
    ) == "completed"
    command = commands[0]
    assert "--no_cache" in command
    assert command[command.index("--selection_artifact_id") + 1] == selection["artifact_id"]
    assert command[command.index("--cache_v2_store_root") + 1] == selection["store_root"]
    propagated_identity = json.loads(child_envs[0][ENV_IDENTITY_JSON])
    assert make_cell_id(propagated_identity) == child_envs[0]["OPENGU_AUTOREPORT_CELL_ID"]
    events, warnings = read_event_stream(event_path)
    assert warnings == []
    selection_event = next(event for event in events if event["stage"] == "selection")
    observation = selection_event["cache"][0]
    assert observation["authoritative"] is True
    assert observation["artifact"]["artifact_id"] == selection["artifact_id"]
    meta = json.loads((out_dir / "_meta.json").read_text(encoding="utf-8"))
    assert meta["selection_artifact"]["artifact_id"] == selection["artifact_id"]


def test_runner_v2_preflight_maps_materializer_envelope_and_rejects_unsupported(tmp_path, monkeypatch):
    runner = _load_experiment_runner()
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    config_path = tmp_path / "fixture.yaml"
    config_path.write_text("fixture", encoding="utf-8")
    cfg = {
        "_source_path": str(config_path),
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42, 212],
        "cache_v2": {"mode": "selection", "store_root": "v2-store"},
    }
    document = {
        "mode": "materialize",
        "writes": [],
        "plan": {
            "skipped": [],
            "jobs": [{
                "strategy": "degree",
                "recipe_hash": "a" * 64,
                "k": 2,
                "request_envelope": {"experiment_seeds": [42, 212]},
            }],
        },
        "results": [{
            "recipe_hash": "a" * 64,
            "artifact_id": "sel_12345678_90abcdef",
            "content_hash": "b" * 64,
            "payload_path": str(tmp_path / "v2-store" / "payload.json"),
            "selected_node_count": 2,
            "hit": True,
        }],
    }
    import cache_v2.selection_materializer as materializer

    monkeypatch.setattr(materializer, "materialize_selection", lambda **_kwargs: document)
    mapping, observed = runner.prepare_cache_v2_selection(cfg, dry_run=False)
    assert observed is document
    assert set(mapping) == {("degree", 42), ("degree", 212)}
    assert len({item["artifact_id"] for item in mapping.values()}) == 1

    bad = dict(cfg)
    bad["strategies"] = ["tracin"]
    with pytest.raises(ValueError, match="no producer"):
        runner.prepare_cache_v2_selection(bad, dry_run=False)


def test_runner_fingerprint_includes_effective_v2_dataset_root(tmp_path):
    runner = _load_experiment_runner()
    cfg = {
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "methods": ["GIF"],
        "strategies": ["degree"],
        "seeds": [42],
        "cache_v2": {
            "mode": "selection",
            "dataset_root": str(tmp_path / "data-a"),
        },
    }
    changed = dict(cfg)
    changed["cache_v2"] = dict(cfg["cache_v2"])
    changed["cache_v2"]["dataset_root"] = str(tmp_path / "data-b")
    assert runner._content_fingerprint(cfg, "GIF", "degree", 42) != runner._content_fingerprint(
        changed, "GIF", "degree", 42
    )


def test_acceptance_markdown_and_html_agree_on_architecture_contract_and_counts():
    root = Path(__file__).parents[1]
    markdown = (root / "docs" / "auto_report_v3_ACCEPTANCE_REPORT.md").read_text(
        encoding="utf-8"
    )
    browser = (root / "report" / "auto_report_v3_ACCEPTANCE_REPORT.html").read_text(
        encoding="utf-8"
    )
    for expected in (
        "events.jsonl",
        "INVALID_ATTACK_ARTIFACT",
        "run.started",
        "attack.failed",
        "run.failed",
        "cell_id",
        "run_id",
        "attempt",
        "config_fingerprint",
        "git_sha",
        "32 passed",
        "233 passed",
        "16 events",
        "19,020",
        "2,015",
    ):
        assert expected in markdown
        assert expected in browser
