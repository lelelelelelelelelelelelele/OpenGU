import json

import pytest

from scripts.evaluation.reporting import events


def fact(run, stage="attack", state="completed", **kwargs):
    return events.build_event(
        identity=dict(dataset="cpu", model="GCN", method="GIF", ratio=0.1),
        stage=stage, state=state, producer="test", config_fingerprint="fp",
        git_sha="abc", run_id="run_" + run, **kwargs,
    )


def test_append_checks_only_current_attempt_and_detaches_caller(tmp_path, monkeypatch):
    path = tmp_path / "events.jsonl"
    history = [fact("old-{0}".format(i)) for i in range(1000)]
    path.write_text("".join(json.dumps(e) + "\n" for e in history), encoding="utf-8")
    started = fact("current", state="started", metadata={"nested": [1]})
    events.append_event(started, event_path=path, refresh=False)
    started["metadata"]["nested"].append(2)
    original = events._check_transition_conflict
    checked = []

    def check(existing, event):
        checked.append(list(existing))
        original(existing, event)

    monkeypatch.setattr(events, "_check_transition_conflict", check)
    monkeypatch.setattr(events, "read_event_stream", lambda *a: pytest.fail("unchanged stream reread"))
    completed = fact("current")
    assert events.append_event(completed, event_path=path, refresh=False).written
    assert not events.append_event(completed, event_path=path, refresh=False).written
    assert len(checked) == 1 and len(checked[0]) == 1
    assert checked[0][0]["metadata"]["nested"] == [1]
    with pytest.raises(events.EventValidationError, match="conflicting terminal"):
        events.append_event(fact("current", state="skipped"), event_path=path, refresh=False)


def test_external_append_rebuilds_dedup_and_transition_indices(tmp_path):
    path = tmp_path / "events.jsonl"
    events.append_event(fact("current", state="started"), event_path=path, refresh=False)
    failed = fact("current", state="failed", error={"type": "test", "message": "failed"})
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(failed) + "\n")
    assert not events.append_event(failed, event_path=path, refresh=False).written
    with pytest.raises(events.EventValidationError, match="cannot mark run"):
        events.append_event(fact("current", stage="run"), event_path=path, refresh=False)
    with path.open("a", encoding="utf-8") as stream:
        stream.write("broken JSON\n")
    with pytest.raises(events.EventStreamCorruptionError):
        events.append_event(fact("next"), event_path=path, refresh=False)


def test_failed_flush_does_not_mark_event_deduplicated(tmp_path, monkeypatch):
    path = tmp_path / "events.jsonl"
    events.append_event(fact("first"), event_path=path, refresh=False)
    before = events._validated_streams[path.resolve()]
    event = fact("second")

    def fail(_):
        raise OSError("fsync failed")

    monkeypatch.setattr(events.os, "fsync", fail)
    with pytest.raises(OSError, match="fsync failed"):
        events.append_event(event, event_path=path, refresh=False)
    assert event["dedup_key"] not in before.dedup_keys
