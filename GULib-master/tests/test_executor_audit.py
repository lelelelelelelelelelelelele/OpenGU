"""Persistent real-cell evidence survives partial execution and process death."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, commit
from scripts.evaluation.reporting.events import read_event_stream, record_event


def test_hard_termination_preserves_completed_entry_and_unknown_active(workspace):
    root, path, config = workspace
    config.update(stage='unlearning', selector_refs=['degree.yaml'], seeds=[7],
                  budget_ratios=[.1], unlearning_refs=['gu.yaml', 'retrain.yaml'])
    config.pop('budget_ratios')
    write_yaml(path, config)
    sha = commit(root)
    script = root / 'kill_probe.py'
    script.write_text('''import sys,time
from pathlib import Path
from experiments.run import main
def notify(event, **value):
    if event == 'progress' and value.get('position', {}).get('stage') == 'unlearning' and value.get('current') == 1:
        Path('ready').write_text('completed first GU', encoding='utf-8')
        time.sleep(120)
main(['experiment.yaml','--run-id','killed','--device','cpu','--verification-root',str(Path.cwd())], notify=notify)
''', encoding='utf-8')
    with (root / 'process.log').open('w', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, '-B', str(script)], cwd=root, stdout=log, stderr=log)
        try:
            deadline = time.monotonic()+60
            while not (root/'ready').exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(.1)
            assert (root/'ready').exists(), (root/'process.log').read_text(encoding='utf-8')
        finally:
            process.kill()
            process.wait(timeout=10)
    journal = root/'results/runtime/modular/_journal'
    events, warnings = read_event_stream(journal/'auto_report.events.jsonl')
    assert not warnings
    attacks = [e for e in events if e['stage']=='attack']
    assert [e['state'] for e in attacks] == ['started','completed']
    assert attacks[-1]['metrics']['accuracy'] is not None
    assert attacks[-1]['metadata']['wall_seconds'] > 0
    assert not any(e['stage']=='run' and e['state']=='completed' for e in events)
    assert not (journal/'auto_report.md').exists()
    assert not (journal/'auto_report.html').exists()
    # Reconcile through the exact Core status schema and captured run contract.
    from syncmate_core.job_status import execution_digest
    from scripts.syncmate.opengu_audit import reconcile
    from experiments.modular_config import configuration_fingerprint
    from utils.target_checkpoint import sha256_file
    from syncmate_core.run_handoff import build_execution_contract
    from syncmate_core import context
    definition = dict(id='verification', experiment_id='contract', config_path='experiment.yaml',
        config_sha256=sha256_file(path), timeout_seconds=60, run_identity=dict(run_id='killed'),
        configuration_fingerprint=configuration_fingerprint(path), expected_artifact_paths=[])
    with context.use(root, node_id='runner'):
        execution = build_execution_contract(definition, project='opengu', job_id='killed-job', git_sha=sha)
    terminal = dict(protocol='syncmate.job-status/v1', job_id='killed-job', state='failed',
        observed_at='2026-10-08T00:00:01+00:00', created_at='2026-10-08T00:00:00',
        started_at='2026-10-08T00:00:00', finished_at='2026-10-08T00:00:01',exit_code=None,
        error_code='recipe_timeout', execution_digest=execution_digest(execution), node_id='runner')
    job = dict(id='killed-job', expected_git_sha=sha, recipe='verification')
    with context.use(root, node_id='runner'):
        assert reconcile(job,definition,execution,terminal,journal/'auto_report.events.jsonl') == 1
        assert reconcile(job,definition,execution,terminal,journal/'auto_report.events.jsonl') == 0
    events, _ = read_event_stream(journal/'auto_report.events.jsonl')
    assert events[-1]['state']=='failed' and events[-1]['error']['type']=='recipe_timeout'
    assert len([e for e in events if e['stage']=='attack' and e['state']=='completed']) == 1
    assert 'wall=' in (journal/'auto_report.html').read_text(encoding='utf-8')
    destination = os.environ.get('AAGU_AUDIT_EVIDENCE')
    if destination:
        output=Path(destination);output.mkdir(parents=True,exist_ok=True)
        for source in journal.iterdir():
            if source.suffix in ('.jsonl','.md','.html'):
                shutil.copyfile(source,output/source.name)
        shutil.copyfile(root/'process.log',output/'process.log')


def test_entry_scientific_failure_does_not_mark_completed(tables):
    from experiments.execution_audit import ExecutionAudit
    from experiments.modular_execution import ExecutionContext
    from pytest import raises
    root=tables[0]
    context=ExecutionContext('failed','verification','cpu',root/'results/cache_v2',root/'ckpt',
        root/'runtime/failed',root/'results/runs/f/f/run.json','pytest')
    audit=ExecutionAudit(context,'a'*64,'fixture')
    with raises(FloatingPointError):
        with audit.entry('attack',dict(dataset='fixture',model='GCN',method='GIF',ratio=.1)):
            raise FloatingPointError('nonfinite solver value')
    events,warnings=read_event_stream(audit.path)
    assert not warnings and [e['state'] for e in events]==['started','failed']
    assert events[-1]['error']['type']=='FloatingPointError'


def test_real_core_timeout_reconciles_its_own_execution(workspace):
    from test_syncmate_execution_contract import declaration, FixtureRegistration
    from syncmate_core import context, devices, queue, versions
    from opengu_syncmate.runtime import execution_readiness
    from scripts.syncmate.opengu_audit import reconcile
    root,path,config=workspace
    config.update(selector_refs=['degree.yaml'])
    config.pop('budget_ratios');config.pop('seeds')
    write_yaml(path,config)
    progress = root/'scripts/syncmate/opengu_progress.py'
    progress.write_text(progress.read_text(encoding='utf-8') + '''
_original_make_notify = make_notify
def make_notify(*args, **kwargs):
    notify = _original_make_notify(*args, **kwargs)
    def observed(event, **values):
        result = notify(event, **values)
        if event == 'progress' and values.get('position', {}).get('stage') == 'selector' and values.get('current') == 1:
            import time
            time.sleep(120)
        return result
    return observed
''',encoding='utf-8')
    definition=declaration(root,path,'selector')
    recipe_path=root/'scripts/syncmate/recipes/temporary-contract.yaml'
    import yaml
    spec=yaml.safe_load(recipe_path.read_text(encoding='utf-8'))
    spec['timeout_seconds']=20
    write_yaml(recipe_path,spec)
    sha=commit(root)
    with context.use(root,extension=FixtureRegistration(definition), node_id='runner', execution_readiness=execution_readiness):
        definition=versions.bind(definition['id'],sha)['definition']
        assert queue.runner_queue_submit('real-timeout',definition['id'],expected_git_sha=sha)['submitted']
        device,warnings=devices.load_device(root/'.syncmate/device.yaml');assert not warnings
        outcome=queue.runner_queue_run_once(device)
        assert outcome['status']=='failed',outcome
        details=queue.runner_queue_job_details('real-timeout')
        terminal=queue.runner_queue_job_status('real-timeout')
    event_path=root/'results/runtime/modular/_journal/auto_report.events.jsonl'
    before,_=read_event_stream(event_path)
    assert any(e['stage']=='selection' and e['state']=='completed' for e in before)
    with context.use(root,node_id='runner'):
        assert reconcile(details,definition,details['receipt']['output_contract'],terminal,event_path)==1
    after,_=read_event_stream(event_path)
    assert after[-1]['error']['type']=='recipe_timeout'
    assert after[-1]['metadata']['terminal_source']==terminal
    assert before==after[:-1]


@pytest.mark.parametrize('stage', ['selector', 'unlearning', 'metrics'])
def test_recipe_projects_once_after_terminal_with_live_durable_events(tables, monkeypatch, record_property, stage):
    from experiments.run import main
    from scripts.evaluation.reporting import events as reporting
    from utils.target_checkpoint import sha256_file
    root, config, gu = tables
    config.update(selector_refs=['b_param_hutch.yaml'], stage='unlearning',
                  unlearning_refs=['gu.yaml'], evaluation_refs=['utility.yaml'])
    path = root/'experiment.yaml'
    journal = root/'results/runtime/modular/_journal'
    event_path = journal/'auto_report.events.jsonl'
    projections = []
    original = reporting.refresh_status_views
    def observe(**kwargs):
        facts, warnings = read_event_stream(kwargs['event_path'])
        assert not warnings
        assert facts[-1]['stage'] == 'run' and facts[-1]['state'] == 'completed'
        projections.append(facts[-1]['metadata']['execution_run_id'])
        return original(**kwargs)
    monkeypatch.setattr(reporting, 'refresh_status_views', observe)
    def invoke(run_id):
        pages = {name: (journal/name).read_bytes() if (journal/name).exists() else None
                 for name in ('auto_report.md', 'auto_report.html')}
        observed = []
        snapshots = []
        count = len(projections)
        def notify(event, **value):
            if event != 'progress':
                return
            facts, warnings = read_event_stream(event_path)
            snapshots.append((not warnings and bool(facts), len(projections),
                {name: (journal/name).read_bytes() if (journal/name).exists() else None for name in pages}))
            observed.extend(e for e in facts if e['stage'] != 'run' and e['state'] == 'completed')
        write_yaml(path, config)
        assert main([str(path), '--run-id', run_id, '--device', 'cpu',
                     '--verification-root', str(root)], notify=notify) == 0
        assert snapshots and all(valid and renders == count and current == pages
                                 for valid, renders, current in snapshots)
        assert observed, 'no durable cell completions visible during execution'
        assert projections[count:] == [run_id]
        facts, warnings = read_event_stream(event_path)
        for name in pages:
            assert (journal/name).is_file() and facts[-1]['run_id'] in (journal/name).read_text(encoding='utf-8')
        assert not warnings
        entries = [e for e in facts if e['metadata'].get('execution_run_id') == run_id]
        assert sum(e['state']=='started' for e in entries) == sum(e['state']=='completed' for e in entries)
        assert all(e['metadata']['wall_seconds'] >= 0 for e in entries if e['state']=='completed')
        return json.loads((root/'results/runs'/config['experiment_id']/run_id/'run.json').read_text(encoding='utf-8'))
    if stage == 'metrics':
        invoke('source')
        source = root/'results/runs'/config['experiment_id']/'source/run.json'
        # A new metric request consumes the existing Output then saves Evaluation.
        write_yaml(root/'metrics.yaml', dict(kind='evaluation', schema_version=1,
            case='post_unlearning_utility', metrics=['f1_after']))
        config = dict(kind='experiment', schema_version=1, experiment_id='audit-metrics',
            stage='metrics', dataset_refs=['dataset.yaml'], matrix='cartesian_product',
            evaluation_refs=['metrics.yaml'], output_inputs=[dict(run=str(source),sha256=sha256_file(source))])
    else:
        config['stage'] = stage
        if stage == 'selector':
            config.pop('unlearning_refs');config.pop('evaluation_refs')
    cold = invoke('cold')
    warm = invoke('warm')
    assert [cell.get('output') for cell in cold['cells']] == [cell.get('output') for cell in warm['cells']]
    facts, _ = read_event_stream(event_path)
    for run_id, outcome in [('cold','miss'), ('warm','hit')]:
        evaluations = [e for e in facts if e['metadata'].get('execution_run_id') == run_id
                       for c in e.get('cache', []) if c['type']=='result']
        if stage != 'selector':
            assert evaluations
            assert all(c['outcome']==outcome for e in evaluations for c in e['cache'] if c['type']=='result')
    cold_metrics = [e['metrics'] for e in facts if e['metadata'].get('execution_run_id')=='cold' and e['stage']=='evaluation' and e['state']=='completed']
    warm_metrics = [e['metrics'] for e in facts if e['metadata'].get('execution_run_id')=='warm' and e['stage']=='evaluation' and e['state']=='completed']
    assert cold_metrics == warm_metrics
    record_property('terminal_projection', json.dumps(dict(stage=stage, projections=projections,
        during_execution=0, durable_completed_events=True, equal_cold_warm_metrics=True)))


def test_recipe_caught_failure_projects_durable_terminal_once(tables, monkeypatch, record_property):
    from experiments.run import main
    from scripts.evaluation.reporting import events as reporting
    root, config, _ = tables
    config.update(selector_refs=['degree.yaml', 'b_param_hutch.yaml'])
    path = root/'failure.yaml'
    write_yaml(path, config)
    projections = []
    original = reporting.refresh_status_views
    def observe(**kwargs):
        facts, warnings = read_event_stream(kwargs['event_path'])
        assert not warnings and facts[-1]['stage']=='run' and facts[-1]['state']=='failed'
        projections.append(facts[-1])
        return original(**kwargs)
    monkeypatch.setattr(reporting, 'refresh_status_views', observe)
    import experiments.modular_run as runner
    resolve = runner.resolve_methods
    resolved = []
    def fail_selector(**kwargs):
        assert not projections
        if not resolved:
            result = resolve(**kwargs)
            resolved.append(result)
            return result
        raise RuntimeError('owned verification interruption')
    monkeypatch.setattr(runner, 'resolve_methods', fail_selector)
    assert main([str(path),'--run-id','failed-recipe','--device','cpu',
                 '--verification-root',str(root)]) == 1
    assert len(projections)==1
    journal=root/'results/runtime/modular/_journal'
    facts, warnings=read_event_stream(journal/'auto_report.events.jsonl')
    assert not warnings and any(e['stage']=='selection' and e['state']=='completed' for e in facts)
    assert facts[-1]['error']['message'] == 'owned verification interruption'
    for name in ('auto_report.md','auto_report.html'):
        page = (journal/name).read_text(encoding='utf-8')
        assert 'run=failed' in page and facts[-1]['run_id'] in page
    record_property('caught_failure', 'one terminal projection; completed entry and failure retained')
