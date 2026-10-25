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


def test_warm_score_does_not_acquire_writer_lock_and_reports_parse_errors(tmp_path, monkeypatch):
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
    with pytest.raises(ScoreBundleIntegrityError, match='cannot be read'):
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


def test_locally_invisible_writer_releases_lock_then_reader_hits(tmp_path, monkeypatch):
    import threading
    from concurrent.futures import ThreadPoolExecutor
    import experiments.cache_locks as locks
    writer = ScoreBundleStore(tmp_path.resolve(), producer_version=ProducerVersion('test-v1', _sha('producer')), lock_timeout_seconds=2)
    reader = ScoreBundleStore(tmp_path.resolve(), producer_version=ProducerVersion('test-v1', _sha('producer')), lock_timeout_seconds=2)
    payload = _payload((3, 8, 10))
    recipe = _recipe(payload.candidate_ids_hash)
    started, contended, release = threading.Event(), threading.Event(), threading.Event()
    calls = []
    def compute():
        calls.append('writer')
        started.set()
        assert release.wait(2)
        return payload
    inspect = locks.inspect_score_lock
    monkeypatch.setattr(locks, 'owner_status', lambda pid: 'orphan')
    def invisible(path):
        result = inspect(path)
        contended.set()
        return result
    monkeypatch.setattr(locks, 'inspect_score_lock', invisible)
    with ThreadPoolExecutor(max_workers=2) as workers:
        first = workers.submit(writer.get_or_compute, recipe, compute)
        assert started.wait(2)
        second = workers.submit(reader.get_or_compute, recipe, lambda: pytest.fail('second producer must not run'))
        assert contended.wait(2)
        release.set()
        a, b = first.result(timeout=3), second.result(timeout=3)
    assert calls == ['writer']
    assert b.hit and not b.producer_called and a.artifact_id == b.artifact_id
    assert not list((tmp_path / '.locks').iterdir())


def test_unreleased_foreign_pid_lock_times_out_and_remains_unchanged(tmp_path, monkeypatch):
    import time
    import experiments.cache_locks as locks
    s = ScoreBundleStore(tmp_path.resolve(), producer_version=ProducerVersion('test-v1', _sha('producer')), lock_timeout_seconds=.05)
    payload = _payload((3,8,10))
    recipe = _recipe(payload.candidate_ids_hash)
    s.initialize()
    path = tmp_path / '.locks' / ('score-' + recipe.recipe_hash + '.lock')
    path.write_bytes(b'54496')
    monkeypatch.setattr(locks, 'owner_status', lambda pid: 'orphan')
    started = time.monotonic()
    with pytest.raises(CacheResolutionError, match='timed out waiting.*54496'):
        s.get_or_compute(recipe, lambda: pytest.fail('lock was not acquired'))
    assert .04 <= time.monotonic()-started < 2
    assert path.read_bytes() == b'54496'


def test_unrelated_lock_does_not_block_entry_before_model_preparation(tables, monkeypatch):
    import experiments.modular_run as module
    root = tables[0]
    folder = root / 'results/cache_v2/.locks'
    folder.mkdir(parents=True)
    lock = folder / 'score-unrelated.lock'
    lock.write_text('unknown-other-host', encoding='ascii')
    class PreparationReached(Exception):
        pass
    def reached(*args, **kwargs):
        raise PreparationReached('CPU test stops before any model preparation')
    monkeypatch.setattr(module, 'prepare_model', reached)
    with pytest.raises(PreparationReached):
        run(tables, 'entry-boundary')
    assert lock.read_text(encoding='ascii') == 'unknown-other-host'


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
