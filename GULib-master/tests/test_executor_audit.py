"""Persistent real-cell evidence survives partial execution and process death."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

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
    # Reconcile through the exact Core status schema and captured run contract.
    from syncmate_core.job_status import execution_digest
    from scripts.syncmate.opengu_audit import reconcile
    from experiments.modular_config import configuration_fingerprint
    from utils.target_checkpoint import sha256_file
    execution = dict(protocol='syncmate.run-handoff/v1', project='opengu', job_id='killed-job',
        recipe='verification', git_sha=sha, config_path='experiment.yaml', config_sha256=sha256_file(path),
        timeout_seconds=60, run_identity=dict(experiment_id='contract',run_id='killed'),
        artifact_paths=[],collect_paths=[])
    terminal = dict(protocol='syncmate.job-status/v1', job_id='killed-job', state='failed',
        observed_at='2026-10-08T00:00:01+00:00', created_at='2026-10-08T00:00:00',
        started_at='2026-10-08T00:00:00', finished_at='2026-10-08T00:00:01',exit_code=None,
        error_code='recipe_timeout', execution_digest=execution_digest(execution))
    job = dict(id='killed-job', expected_git_sha=sha, recipe='verification')
    definition = dict(run_identity=execution['run_identity'], config_sha256=execution['config_sha256'],
        configuration_fingerprint=configuration_fingerprint(path))
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
    from syncmate_core import context, devices, queue
    from scripts.syncmate.opengu_audit import reconcile
    root,path,config=workspace
    config.update(selector_refs=['degree.yaml'])
    config.pop('budget_ratios');config.pop('seeds')
    write_yaml(path,config)
    (root/'timeout_probe.py').write_text('''from pathlib import Path
import time
from experiments.run import main
def notify(event, **value):
    if event == 'progress' and value.get('position',{}).get('stage') == 'selector' and value.get('current') == 1:
        time.sleep(120)
main(['experiment.yaml','--run-id','registered','--device','cpu','--verification-root',str(Path.cwd())], notify=notify)
''',encoding='utf-8')
    definition=declaration(root,path,'selector')
    definition.update(argv=('{python}','timeout_probe.py'),timeout_seconds=10)
    sha=commit(root)
    with context.use(root,extension=FixtureRegistration(definition)):
        assert queue.runner_queue_submit('real-timeout',definition['id'],expected_git_sha=sha)['submitted']
        device,warnings=devices.load_device(root/'.syncmate/device.yaml');assert not warnings
        outcome=queue.runner_queue_run_once(device)
        assert outcome['status']=='failed',outcome
        details=queue.runner_queue_job_details('real-timeout')
        terminal=queue.runner_queue_job_status('real-timeout')
    event_path=root/'results/runtime/modular/_journal/auto_report.events.jsonl'
    before,_=read_event_stream(event_path)
    assert any(e['stage']=='selection' and e['state']=='completed' for e in before)
    assert reconcile(details,definition,details['receipt']['output_contract'],terminal,event_path)==1
    after,_=read_event_stream(event_path)
    assert after[-1]['error']['type']=='recipe_timeout'
    assert after[-1]['metadata']['terminal_source']==terminal
    assert before==after[:-1]
