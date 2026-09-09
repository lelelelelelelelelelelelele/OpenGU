"""RR uses the real sampler, prefix cache, matrix and Result consumers."""
import hashlib

import pytest

from tests.test_modular_consumers import tables, run, write_yaml
from tests.test_modular_im import setup_im
from experiments.modular_artifacts import read_run
from experiments.modular_config import selector


def rr_instance(**params):
    return {'kind': 'selector', 'schema_version': 1, 'method': 'im_rr_greedy',
            'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2},
            'parameters': {'rr_count': 64, 'im_selector_seed': 17, **params}}


def test_mixed_rr_real_sampling_identity_and_return(tables, monkeypatch):
    changes = setup_im(tables)
    changes.update(selector_refs=['r_point.yaml', 'im.yaml', 'rr.yaml'], seeds=[42, 212],
                   im_selector_seeds=[11, 22])
    root = tables[0]
    write_yaml(root / 'rr.yaml', rr_instance())
    import experiments.modular_rr as rr
    original = rr.select_rr
    calls = []
    def counted(inputs, k, params):
        calls.append((k, dict(params)))
        return original(inputs, k, params)
    monkeypatch.setattr(rr, 'select_rr', counted)
    # Spy instrumentation must not change the implementation identity under test.
    counted.__wrapped__ = original
    cold = run(tables, 'rr_cold', **changes)
    assert [p['im_selector_seed'] for _, p in calls] == [11, 22]
    assert len(cold['unlearning']) == 10
    rr_entries = [s for s in cold['selectors'] if s['selection']['strategy'] == 'im_rr_greedy']
    rr_ids = {s['selection']['artifact']['artifact_id'] for s in rr_entries}
    assert len(rr_ids) == 2
    assert rr_ids.isdisjoint(s['selection']['artifact']['artifact_id'] for s in cold['selectors']
                            if s['selection']['strategy'] == 'im')
    calls.clear()
    warm = run(tables, 'rr_warm', **{**changes, 'seeds': [99]})
    assert not calls
    assert all(s['selection']['cache']['hit'] for s in warm['selectors']
               if s['selection']['strategy'] != 'r_point')
    path = root / 'results/runs/rr_warm/rr_warm/run.json'
    manifest, documents = read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
    for cell, doc in zip(manifest['cells'], documents):
        if cell['conditions']['selector'] == 'im_rr_greedy':
            assert doc['selection.json']['im_selector_seed'] == cell['conditions']['im_selector_seed']
            assert doc['selection.json']['training_seed'] == 99
            assert len(doc['selection.json']['selected_nodes']) == 2
    # Sampling changes miss; a smaller K reuses that new RR artifact.
    for label, instance in [('samples', rr_instance(rr_count=65)),
                            ('k', {**rr_instance(rr_count=65), 'budget': {'mode': 'k', 'value': 1}})]:
        write_yaml(root / 'rr.yaml', instance)
        calls.clear()
        result = run(tables, 'rr_' + label, **{**changes, 'seeds': [42]})
        assert len(calls) == (2 if label == 'samples' else 0)
        assert all(s['selection']['cache']['hit'] for s in result['selectors']
                   if s['selection']['strategy'] != 'im_rr_greedy')


@pytest.mark.parametrize('params', [{'rr_count': 0}, {'rr_count': True}, {'rr_count': 1.5},
    {'im_selector_seed': -1}, {'propagation_prob': float('nan')}, {'propagation_prob': 1.1},
    {'mc_rounds': 100}, {'im_batch_size': 5}])
def test_invalid_or_wrong_algorithm_parameters(params):
    with pytest.raises(ValueError):
        selector(rr_instance(**params))


def test_fixed_rr_greedy_accounts_for_overlap():
    from experiments.im_score_benchmark.rr_core import RRBundle
    from experiments.im_score_benchmark.selectors import maximum_coverage_greedy
    bundle = RRBundle.from_rr_sets(num_nodes=4, candidate_nodes=[0, 1, 2],
        rr_sets=[[0, 1], [0, 1], [0, 1], [2], [2]], roots=[0, 0, 0, 2, 2],
        propagation_probability=0.1, rr_seed=7, root_domain_size=4)
    result = maximum_coverage_greedy(bundle, 2)
    assert result.selected_nodes.tolist() == [0, 2]
    assert bundle.coverage_count(result.selected_nodes) == 5
