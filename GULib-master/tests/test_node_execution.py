"""Explicit execution routing is separate from scientific Recipe/Cache identity."""
import copy
import json
from pathlib import Path

import pytest
from syncmate_core import context, queue, maintenance
from syncmate_core.run_handoff import build_execution_contract
from scripts.syncmate.opengu_adapter import bind_execution_node


def test_node_binding_changes_only_execution_argv():
    base = {'id': 'same', 'argv': ('{python}', 'experiments/run.py', 'x.yaml', '--syncmate'),
            'config_path': 'x.yaml', 'config_sha256': 'a'*64, 'timeout_seconds': 30,
            'run_identity': {'experiment_id': 'science', 'run_id': 'same'},
            'expected_artifact_paths': ('results/runs/science/same/run.json',)}
    original = copy.deepcopy(base)
    a = bind_execution_node(base, 'gpu4090')
    b = bind_execution_node(base, 'gpu4090-2')
    assert a['argv'][-2:] == ('--node-id', 'gpu4090')
    assert b['argv'][-2:] == ('--node-id', 'gpu4090-2')
    assert base == original
    assert {k:v for k,v in a.items() if k != 'argv'} == {k:v for k,v in b.items() if k != 'argv'}
    assert build_execution_contract(a, project='opengu', job_id='one', git_sha='b'*40) == build_execution_contract(b, project='opengu', job_id='one', git_sha='b'*40)
    smoke = bind_execution_node({**base, 'argv': ('{python}', 'scripts/syncmate/syncmate.py', 'smoke', '--json')}, 'gpu4090-2')
    assert smoke['argv'][2:5] == ('--node-id', 'gpu4090-2', 'smoke')


def test_shared_root_has_only_node_queue_separation(tmp_path):
    import subprocess
    subprocess.run(['git', '-C', str(tmp_path), 'init', '-b', 'main'], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(tmp_path), '-c', 'user.name=Node fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-m', 'node fixture'], check=True, capture_output=True)
    roots = []
    for node in ('gpu4090', 'gpu4090-2'):
        with context.use(tmp_path, node_id=node):
            queue.ensure_runner_queue_dirs()
            roots.append(queue.runner_queue_root())
            status = maintenance.node_status()
            assert status['status'] == 'idle', status
    assert roots == [tmp_path / '.syncmate/runner_queues' / n for n in ('gpu4090', 'gpu4090-2')]
    assert not (tmp_path / '.syncmate/runner_queue').exists()
    with context.use(tmp_path):
        with pytest.raises(ValueError, match='explicit node_id'):
            queue.runner_queue_root()


def test_old_score_global_helpers_are_not_execution_requirements(tmp_path, monkeypatch):
    from scripts.syncmate.opengu_adapter import _modular_preflight
    import experiments.modular_run as module
    lock = tmp_path / 'results/cache_v2/.locks/score-other.lock'
    lock.parent.mkdir(parents=True)
    lock.write_text('unknown-other-host', encoding='utf-8')
    monkeypatch.setattr(module, 'execute', lambda *a, **k: dict(stage='unlearning',
        configuration_fingerprint='same', logical_cells=1, experiment_id='test'))
    definition = dict(configuration_fingerprint='same', logical_cells=1, run_identity={'experiment_id':'test'})
    with context.use(tmp_path, node_id='gpu4090'):
        assert _modular_preflight(definition, tmp_path / 'experiment.yaml') == {'ready': True, 'errors': []}
    assert lock.read_text(encoding='utf-8') == 'unknown-other-host'


def test_execution_receipt_records_node_without_changing_shared_paths(tmp_path):
    from dataclasses import replace
    from experiments.modular_execution import project_context
    context_a = project_context('science', run_id='one', request_device='cpu', level='verification', repository_root=tmp_path)
    a = replace(context_a, node_id='gpu4090')
    b = replace(context_a, node_id='gpu4090-2')
    assert a.receipt()['node_id'] == 'gpu4090' and b.receipt()['node_id'] == 'gpu4090-2'
    for field in ('store_root','checkpoint_root','runtime_root','output'):
        assert getattr(a, field) == getattr(b, field)


def test_candidate_core_payload_verifies_without_installation():
    import os
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    candidate_pin = os.environ.get('AAGU121_CORE_PIN')
    if candidate_pin is None:
        pytest.skip('isolated candidate verification requires explicit evidence pin')
    result = verify_core_dependency(pin_path=Path(candidate_pin))
    assert result['ready'], result
