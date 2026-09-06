"""AutoReport acceptance through the real ordinary command and Core runner.

Fix these observations before changing production: real attempts are audited,
dry-run is not an attempt, and an untrusted journal cannot be silently replaced.
"""
import hashlib
import json
import subprocess
import sys

import pytest
from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import (
    workspace, cli, commit, declaration, FixtureRegistration,
)
from experiments.modular_config import configuration_fingerprint
from scripts.evaluation.reporting.events import read_event_stream
from syncmate_core import context, devices, queue


@pytest.fixture
def experiment(workspace):
    root, path, config = workspace
    config.update(selector_refs=['degree.yaml'])
    config.pop('seeds')
    config.pop('budget_ratios')
    write_yaml(path, config)
    sha = commit(root)
    return root, path, sha


def journal(root):
    events, warnings = read_event_stream(root / 'results/runtime/modular/_journal/auto_report.events.jsonl')
    assert not warnings
    return events


def test_real_success_and_cached_repeat_are_separate_audited_attempts(experiment):
    root, path, sha = experiment
    for run_id in ('cold', 'warm'):
        result = cli(root, path, run_id)
        assert result.returncode == 0, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        assert payload['passed']
    assert payload['selectors'][0]['selection']['cache']['hit']
    events = journal(root)
    assert [(e['stage'], e['state']) for e in events] == [
        ('run', 'started'), ('run', 'completed'), ('run', 'started'), ('run', 'completed')]
    assert len({e['cell_id'] for e in events}) == 1
    assert events[0]['run_id'] == events[1]['run_id'] != events[2]['run_id'] == events[3]['run_id']
    assert [e['attempt'] for e in events] == [1, 1, 2, 2]
    assert [e['metadata']['execution_run_id'] for e in events] == ['cold', 'cold', 'warm', 'warm']
    assert all(e['git_sha'] == sha and e['config_fingerprint'] == configuration_fingerprint(path)
               for e in events)
    assert all(e['identity']['experiment_id'] == 'contract' and
               e['identity']['dataset'] == 'cpu_fixture' for e in events)
    summary = root / 'results/runs/modular/contract/warm/summary.json'
    assert any(a['path'] == str(summary) and a['content_hash'] == hashlib.sha256(summary.read_bytes()).hexdigest()
               for a in events[-1]['artifacts'])
    for name in ('auto_report.md', 'auto_report.html'):
        text = (root / 'results/runtime/modular/_journal' / name).read_text(encoding='utf-8')
        assert 'contract' in text and 'complete' in text


def test_real_execution_failure_is_audited_without_completion(experiment):
    root, path, _ = experiment
    (root / 'graph.pkl').write_bytes(b'invalid graph bytes')
    commit(root)
    result = cli(root, path, 'failed')
    assert result.returncode != 0
    assert 'mismatch' in json.loads(result.stdout)['error']
    events = journal(root)
    assert [e['state'] for e in events] == ['started', 'failed']
    assert events[0]['run_id'] == events[1]['run_id']
    assert events[-1]['error']['type'] and 'mismatch' in events[-1]['error']['message']
    assert not (root / 'results/runs/modular/contract/failed/summary.json').exists()


def test_dry_run_creates_no_audit_attempt(experiment):
    root, path, _ = experiment
    result = subprocess.run([sys.executable, '-B', 'experiments/run.py', str(path), '--dry_run'],
        cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['logical_cells'] == 1
    assert not (root / 'results').exists()


def test_corrupt_journal_stops_before_production_and_preserves_evidence(experiment):
    root, path, _ = experiment
    event_path = root / 'results/runtime/modular/_journal/auto_report.events.jsonl'
    event_path.parent.mkdir(parents=True)
    event_path.write_bytes(b'not a valid audit event\n')
    result = cli(root, path, 'corrupt-journal')
    assert result.returncode != 0
    assert event_path.read_bytes() == b'not a valid audit event\n'
    assert not (root / 'results/cache_v2').exists()
    assert not (root / 'results/runs').exists()


def test_real_core_submission_uses_the_same_audit_producer(experiment):
    root, path, sha = experiment
    definition = declaration(root, path, 'selector')
    with context.use(root, extension=FixtureRegistration(definition)):
        submitted = queue.runner_queue_submit('audit-job', definition['id'], expected_git_sha=sha)
        assert submitted['submitted'], submitted
        device, warnings = devices.load_device(root / '.syncmate/device.yaml')
        assert not warnings
        completed = queue.runner_queue_run_once(device)
        assert completed['status'] == 'done', completed
    events = journal(root)
    assert [e['state'] for e in events] == ['started', 'completed']
    assert all(e['metadata']['execution_run_id'] == 'registered' and e['git_sha'] == sha for e in events)
