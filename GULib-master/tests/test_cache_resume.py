"""Interrupted cache recovery and run-local preparation isolation."""
import copy
import os
from contextlib import contextmanager
from types import SimpleNamespace

import pytest
import torch

from test_modular_consumers import tables, run, write_yaml, identities
from test_c_target_v1 import _payload, _recipe, _sha
from cache_v2 import ProducerVersion
from cache_v2.errors import CacheResolutionError
from experiments.c_target_v1.score_store import ScoreBundleStore, ScoreBundleIntegrityError


def store(tmp_path):
    return ScoreBundleStore(tmp_path.resolve(),
        producer_version=ProducerVersion('test-v1', _sha('producer')), lock_timeout_seconds=0)


@pytest.mark.parametrize('error, expected', [(None, 'active'),
    (ProcessLookupError(), 'orphan'), (PermissionError(), 'unknown'), (OSError(), 'unknown')])
def test_posix_owner_probe_never_sends_a_signal(monkeypatch, error, expected):
    import experiments.cache_locks as locks
    def kill(pid, signal):
        assert (pid, signal) == (54496, 0)
        if error is not None:
            raise error
    monkeypatch.setattr(locks, 'os', SimpleNamespace(name='posix', getpid=lambda: 42, kill=kill))
    assert locks.owner_status(54496) == expected


def test_warm_score_does_not_acquire_writer_lock_and_still_checks_bytes(tmp_path, monkeypatch):
    s = store(tmp_path)
    payload = _payload((3, 8, 10))
    recipe = _recipe(payload.candidate_ids_hash)
    cold = s.get_or_compute(recipe, lambda: payload)
    lock = tmp_path / '.locks' / ('score-' + recipe.recipe_hash + '.lock')
    lock.write_text(str(os.getpid()), encoding='ascii')
    def forbidden(*args):
        pytest.fail('immutable HIT must not acquire the writer lock')
    monkeypatch.setattr(s, '_recipe_lock', forbidden)
    assert s.get_or_compute(recipe, forbidden).artifact_id == cold.artifact_id
    assert lock.exists()
    (tmp_path / cold.semantic_path).write_bytes(b'corrupt')
    with pytest.raises(ScoreBundleIntegrityError, match='hash mismatch'):
        s.get_or_compute(recipe, forbidden)


def test_miss_rechecks_after_writer_finishes(tmp_path, monkeypatch):
    s = store(tmp_path)
    payload = _payload((3, 8, 10))
    recipe = _recipe(payload.candidate_ids_hash)
    @contextmanager
    def other_writer_finished(_):
        store(tmp_path).get_or_compute(recipe, lambda: payload)
        yield
    monkeypatch.setattr(s, '_recipe_lock', other_writer_finished)
    result = s.get_or_compute(recipe, lambda: pytest.fail('duplicate producer'))
    assert result.hit and not result.producer_called


@pytest.mark.parametrize('status', ['active', 'orphan', 'unknown'])
def test_lock_preflight_blocks_without_deleting(tmp_path, monkeypatch, status):
    import experiments.cache_locks as locks
    folder = tmp_path / '.locks'
    folder.mkdir()
    path = folder / ('score-' + 'a' * 64 + '.lock')
    path.write_text('54496', encoding='ascii')
    monkeypatch.setattr(locks, 'owner_status', lambda pid: status)
    result = locks.score_lock_preflight(tmp_path)
    assert not result['ready'] and result['locks'][0]['status'] == status
    assert str(path) in result['errors'][0] and '54496' in result['errors'][0]
    assert path.read_text(encoding='ascii') == '54496'


@pytest.mark.parametrize('content', ['', '-1', '0', 'oops', '9' * 40])
def test_unknown_lock_fails_closed(tmp_path, content):
    from experiments.cache_locks import score_lock_preflight
    (tmp_path / '.locks').mkdir()
    (tmp_path / '.locks' / 'score-x.lock').write_text(content, encoding='ascii')
    assert not score_lock_preflight(tmp_path)['ready']


def test_orphan_miss_fails_immediately_with_exact_owner(tmp_path, monkeypatch):
    import experiments.cache_locks as locks
    import experiments.c_target_v1.score_store as module
    s = store(tmp_path)
    payload = _payload((3, 8, 10))
    recipe = _recipe(payload.candidate_ids_hash)
    s.initialize()
    path = tmp_path / '.locks' / ('score-' + recipe.recipe_hash + '.lock')
    path.write_text('54496', encoding='ascii')
    monkeypatch.setattr(locks, 'owner_status', lambda pid: 'orphan')
    monkeypatch.setattr(module.time, 'sleep', lambda _: pytest.fail('orphan must not wait'))
    with pytest.raises(CacheResolutionError, match='orphan.*54496'):
        s.get_or_compute(recipe, lambda: pytest.fail('blocked producer'))
    assert path.exists()


def test_entry_blocks_before_model_preparation_and_output_creation(tables, monkeypatch):
    import experiments.modular_run as module
    root = tables[0]
    folder = root / 'results/cache_v2/.locks'
    folder.mkdir(parents=True)
    (folder / 'score-x.lock').write_text(str(os.getpid()), encoding='ascii')
    monkeypatch.setattr(module, 'prepare_model', lambda *a, **k: pytest.fail('preflight too late'))
    with pytest.raises(CacheResolutionError, match='ScoreBundle lock active'):
        run(tables, 'blocked')
    assert not (root / 'results/runs/blocked').exists()


def test_registered_preflight_uses_bound_runner_root(tmp_path, monkeypatch):
    from syncmate_core.context import use
    from scripts.syncmate.opengu_adapter import _modular_preflight
    import experiments.modular_run as module
    folder = tmp_path / 'results/cache_v2/.locks'
    folder.mkdir(parents=True)
    (folder / 'score-x.lock').write_text('invalid', encoding='ascii')
    monkeypatch.setattr(module, 'execute', lambda *a, **k: dict(stage='unlearning',
        configuration_fingerprint='same', logical_cells=1, experiment_id='test'))
    definition = dict(configuration_fingerprint='same', logical_cells=1, run_identity={'experiment_id':'test'})
    with use(tmp_path):
        result = _modular_preflight(definition, tmp_path / 'experiment.yaml')
    assert not result['ready'] and result['cache_recovery']['locks'][0]['status'] == 'unknown'


def test_prepared_models_are_private_and_keyed_by_training_input():
    from experiments.prepared_models import PreparedModels
    calls = []
    def prepare(instance, **kwargs):
        calls.append(copy.deepcopy(instance))
        return torch.nn.Linear(2, 1), [{'state': torch.ones(2)}], {'hit':False, 'state_hash':'verified'}
    pool = PreparedModels(prepare)
    pool.select_group((0, 42))
    item = dict(kind='unlearning', method='GIF', model={'hidden':2}, training={'seed':42})
    first = pool.get(item)
    original = first[0].weight.detach().clone()
    with torch.no_grad():
        first[0].weight.add_(100)
    first[1][0]['state'].zero_()
    first[2]['state_hash'] = 'changed'
    second = pool.get({**item, 'method':'MEGU'})
    torch.testing.assert_close(second[0].weight, original)
    assert second[1][0]['state'].sum() == 2 and second[2]['state_hash'] == 'verified'
    assert len(calls) == 1
    pool.get({**item, 'training':{'seed':43}})
    pool.get({**item, 'checkpoint':'external.pt'})
    pool.select_group((1, 42))
    pool.get(item)
    assert len(calls) == 4


def test_fingerprint_memo_is_run_scoped_and_resets_after_failure(monkeypatch):
    import experiments.implementation_identity as identity
    from experiments.output_metrics import method_metrics
    original = identity.computation_source
    calls = []
    def source(fn):
        calls.append(fn)
        return original(fn)
    monkeypatch.setattr(identity, 'computation_source', source)
    expected = identity.implementation_fingerprint(method_metrics)
    calls.clear()
    with pytest.raises(RuntimeError):
        with identity.fingerprint_session():
            assert identity.implementation_fingerprint(method_metrics) == expected
            count = len(calls)
            assert identity.implementation_fingerprint(method_metrics) == expected
            assert len(calls) == count
            raise RuntimeError('interrupted run')
    identity.implementation_fingerprint(method_metrics)
    assert len(calls) > count


def test_real_warm_matrix_prepares_once_per_model_group(tables, monkeypatch):
    import experiments.modular_run as module
    calls = []
    original = module.prepare_model
    def measured(*a, **k):
        calls.append(a[0])
        return original(*a, **k)
    monkeypatch.setattr(module, 'prepare_model', measured)
    options = dict(stage='unlearning', selector_refs=['r_point.yaml','b_param_hutch.yaml'],
                   unlearning_refs=['gu.yaml'], seeds=[42,212])
    cold = run(tables, 'pool_cold', **options)
    assert len(calls) == 2  # eight requests share two immutable initial models
    calls.clear()
    warm = run(tables, 'pool_warm', **options)
    assert len(calls) == 2 and all(row['hit'] for row in warm['unlearning'])
    assert identities(cold) == identities(warm)
    assert [r['output'] for r in cold['unlearning']] == [r['output'] for r in warm['unlearning']]
    assert [r['evaluation'] for r in cold['unlearning']] == [r['evaluation'] for r in warm['unlearning']]
