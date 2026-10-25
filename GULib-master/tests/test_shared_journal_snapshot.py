"""Concurrency and integrity regressions for shared AutoReport snapshots."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.evaluation.reporting import events


def fact(run, state='completed'):
    return events.build_event(identity=dict(dataset='cpu', model='GCN', method='GIF', ratio=.1),
        stage='attack', state=state, producer='test', config_fingerprint='fp', git_sha='sha',
        run_id='run_' + run, error=dict(type='test',message='failed') if state=='failed' else None)


def test_cold_validation_releases_lock_for_other_writer(tmp_path, monkeypatch):
    path = tmp_path / 'events.jsonl'
    path.write_text(json.dumps(fact('initial'))+'\n', encoding='utf-8')
    original = events.read_event_stream
    reads = []

    def read(source):
        lock = path.with_name(path.name+'.lock')
        assert not lock.exists(), 'Historical parsing must not hold the append lock'
        result = original(source)
        reads.append(source)
        if len(reads) == 1:
            with path.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(fact('parallel'))+'\n')
        return result

    monkeypatch.setattr(events, 'read_event_stream', read)
    assert events.append_event(fact('current'), event_path=path, refresh=False).written
    actual, warnings = original(path)
    assert len(reads) == 2
    assert not warnings and {e['run_id'] for e in actual} == {'run_initial','run_parallel','run_current'}


def test_changed_snapshot_cannot_bypass_new_terminal_conflict(tmp_path, monkeypatch):
    path = tmp_path / 'events.jsonl'
    path.write_text(json.dumps(fact('current','started'))+'\n', encoding='utf-8')
    original = events.read_event_stream
    changed = []

    def read(source):
        result = original(source)
        if not changed:
            changed.append(True)
            with path.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(fact('current','failed'))+'\n')
        return result

    monkeypatch.setattr(events, 'read_event_stream', read)
    with pytest.raises(events.EventValidationError, match='conflicting terminal'):
        events.append_event(fact('current'), event_path=path, refresh=False)
    actual, warnings = original(path)
    assert not warnings and [e['state'] for e in actual] == ['started','failed']


def test_old_lock_is_never_stolen_by_age(tmp_path):
    path = tmp_path / 'events.jsonl'
    lock = path.with_name(path.name+'.lock')
    lock.write_bytes(b'other-writer retained-owner\n')
    os.utime(lock, (1,1))
    with pytest.raises(TimeoutError):
        with events._exclusive_lock(path, timeout_s=.01):
            pytest.fail('another writer lock was stolen')
    assert lock.read_bytes() == b'other-writer retained-owner\n'


def test_two_cold_processes_append_without_loss_or_duplicate(tmp_path):
    path = tmp_path / 'events.jsonl'
    history = [fact('historical-'+str(i)) for i in range(500)]
    path.write_text(''.join(json.dumps(e)+'\n' for e in history), encoding='utf-8')
    worker = tmp_path / 'writer.py'
    worker.write_text('''import json,sys,time,os
from pathlib import Path
from scripts.evaluation.reporting import events
path=Path(sys.argv[1]);name=sys.argv[2];folder=path.parent
original=events.read_event_stream;first=True
def read(source):
 global first
 lock=path.with_name(path.name+'.lock')
 try:owner=lock.read_text(encoding='utf-8').split()[0]
 except FileNotFoundError:owner=None
 assert owner!=str(os.getpid()),'cold reader owns append lock'
 result=original(source)
 if first:
  first=False;(folder/('ready-'+name)).write_text('ready',encoding='utf-8')
  deadline=time.monotonic()+15
  while len(list(folder.glob('ready-*')))!=2:
   assert time.monotonic()<deadline,'second cold reader never arrived'
   time.sleep(.01)
 return result
events.read_event_stream=read
for i in range(12):
 event=events.build_event(identity=dict(dataset='cpu',model='GCN',method='GIF',ratio=.1),stage='attack',state='completed',producer='test',config_fingerprint='fp',git_sha='sha',run_id='run_'+name+'-'+str(i))
 assert events.append_event(event,event_path=path,refresh=False).written
 assert not events.append_event(event,event_path=path,refresh=False).written
print(json.dumps(dict(writer=name,written=12)))
''', encoding='utf-8')
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1])+os.pathsep+os.environ.get('PYTHONPATH',''),
               PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    processes = [subprocess.Popen([sys.executable,'-B',str(worker),str(path),name],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env) for name in ('node-a','node-b')]
    try:
        for process in processes:
            stdout, stderr = process.communicate(timeout=25)
            assert process.returncode == 0, stderr.decode('utf-8',errors='replace')
            assert json.loads(stdout)['written'] == 12
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill(); process.communicate()
    actual, warnings = events.read_event_stream(path)
    assert not warnings and len(actual) == 524
    assert len({event['dedup_key'] for event in actual}) == 524
    assert not path.with_name(path.name+'.lock').exists()
