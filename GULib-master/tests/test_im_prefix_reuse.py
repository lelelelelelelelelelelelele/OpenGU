"""Real producers, empty-store controls and GU/Result prefix consumers."""
import copy
import hashlib
import json
from dataclasses import replace

import pytest
import torch
from torch_geometric.data import Data

from experiments.modular_im import resolve_im, resolve_im_parameters
from experiments.modular_rr import resolve_rr, resolve_rr_parameters
from experiments.selection_inputs import make_dataset_selection_inputs
from tests.test_modular_consumers import tables, run, write_yaml


def fixture_inputs(empty=False, count=80):
    n = 100
    edges = torch.stack([torch.arange(n-1), torch.arange(1, n)])
    data = Data(x=torch.arange(n*3, dtype=torch.float32).reshape(n, 3)/100,
        y=torch.arange(n)%2, edge_index=(torch.empty((2, 0), dtype=torch.long) if empty
        else torch.cat([edges, edges.flip(0)], dim=1)), train_mask=torch.arange(n)<count,
        val_mask=(torch.arange(n)>=80)&(torch.arange(n)<90), test_mask=torch.arange(n)>=90)
    return data, make_dataset_selection_inputs(data, dataset_name='im_prefix_cpu')


def item(method, k, **params):
    resolve = resolve_im_parameters if method == 'im' else resolve_rr_parameters
    return {'method': method, 'budget': {'k': k}, 'parameters': resolve(params)}


def invoke(spec, root, data, inputs):
    return (resolve_im if spec['method']=='im' else resolve_rr)(spec,
        store_root=root, data=data, inputs=inputs)['selection']


CONDITIONS = [('im_rr_greedy', {'rr_count': count, 'im_selector_seed': seed})
    for count in (1024, 4096, 16384) for seed in (11, 22, 33)] + [
    ('im', {'mc_rounds': 100, 'im_batch_size': 1, 'im_selector_seed': seed})
    for seed in (11, 22, 33)]


@pytest.mark.parametrize('method,params', CONDITIONS)
def test_production_parameters_with_independent_empty_control(tmp_path, method, params, record_property, monkeypatch):
    data, inputs = fixture_inputs()
    calls = []
    if method == 'im':
        from experiments.selection_producer import load_im_strategy
        strategy, _, _ = load_im_strategy()
        original = strategy.compute_im_celf
        def counted(self, edges, n, k, candidates):
            calls.append(k)
            return original(self, edges, n, k, candidates)
        monkeypatch.setattr(strategy, 'compute_im_celf', counted)
    else:
        import experiments.modular_rr as rr
        original = rr.select_rr
        def counted(inputs, k, params):
            calls.append(k)
            return original(inputs, k, params)
        counted.__wrapped__ = original
        monkeypatch.setattr(rr, 'select_rr', counted)
    cold = invoke(item(method, 8, **params), tmp_path/'shared', data, inputs)
    small = invoke(item(method, 4, **params), tmp_path/'shared', data, inputs)
    warm = invoke(item(method, 4, **params), tmp_path/'shared', data, inputs)
    exact = invoke(item(method, 8, **params), tmp_path/'shared', data, inputs)
    control = invoke(item(method, 4, **params), tmp_path/'empty_control', data, inputs)
    assert calls == [8, 4]
    assert cold['cache']['producer_called'] and control['cache']['producer_called']
    assert not cold['cache']['hit'] and not control['cache']['hit']
    for result in (small, warm, exact):
        assert result['cache']['hit'] and not result['cache']['producer_called']
        assert result['artifact']==cold['artifact']
        assert result['artifact_k']==8
    assert small['views']['4']['requested_k']==4
    assert small['views']['4']['selected_nodes']==cold['views']['8']['selected_nodes'][:4]
    assert small['views']['4']['selected_nodes']==control['views']['4']['selected_nodes']
    record_property('prefix_evidence', json.dumps(dict(method=method, params=params,
        cold=cold, small=small, warm=warm, exact=exact, empty_control=control, actual_producer_calls=calls)))


@pytest.mark.parametrize('method', ['im', 'im_rr_greedy'])
@pytest.mark.parametrize('empty', [True, False])
def test_boundaries_and_zero_gain_ties(tmp_path, method, empty):
    data, inputs = fixture_inputs(empty=empty, count=7)
    params = {'im_batch_size': 1, 'mc_rounds': 7, 'parallel_mc': False} if method=='im' else {'rr_count': 7}
    full = invoke(item(method, 7, **params), tmp_path/'full', data, inputs)
    for k in (1, 3, 6):
        direct = invoke(item(method, k, **params), tmp_path/str(k), data, inputs)
        assert direct['views'][str(k)]['selected_nodes']==full['views']['7']['selected_nodes'][:k]
    assert sorted(full['views']['7']['selected_nodes'])==list(inputs.candidate_nodes)
    for k in (0, 8):
        with pytest.raises(ValueError):
            invoke(item(method, k, **params), tmp_path/'invalid', data, inputs)


@pytest.mark.parametrize('method', ['im', 'im_rr_greedy'])
def test_identity_changes_and_larger_budget_miss(tmp_path, method, monkeypatch):
    data, inputs = fixture_inputs(count=10)
    params = {'im_batch_size': 1, 'mc_rounds': 3, 'parallel_mc': False} if method=='im' else {'rr_count': 32}
    spec = item(method, 8, **params)
    invoke(spec, tmp_path, data, inputs)
    smaller = item(method, 4, **params)
    variants = [('im_selector_seed', 999), ('propagation_prob', .5)]
    variants += [('mc_rounds', 4), ('parallel_mc', True), ('im_batch_size', 2),
                 ('candidate_fraction', .9)] if method=='im' else [('rr_count', 33)]
    for key, value in variants:
        changed = copy.deepcopy(smaller); changed['parameters'][key]=value
        result = invoke(changed, tmp_path, data, inputs)
        assert not result['cache']['hit'] and result['cache']['producer_called']
    for changed_inputs in (replace(inputs, dataset_fingerprint='a'*64),
                           replace(inputs, graph_fingerprint='b'*64)):
        assert invoke(smaller, tmp_path, data, changed_inputs)['cache']['producer_called']
    changed_graph = data.clone(); changed_graph.edge_index = data.edge_index[:, :-2]
    graph_inputs = make_dataset_selection_inputs(changed_graph, dataset_name='im_prefix_cpu')
    assert invoke(smaller, tmp_path, changed_graph, graph_inputs)['cache']['producer_called']
    changed_data = data.clone(); changed_data.val_mask[80]=False
    assert invoke(smaller, tmp_path, changed_data, inputs)['cache']['producer_called']
    changed_data = data.clone(); changed_data.train_mask[0]=False
    changed_inputs = make_dataset_selection_inputs(changed_data, dataset_name='im_prefix_cpu')
    assert invoke(smaller, tmp_path, changed_data, changed_inputs)['cache']['producer_called']
    assert invoke(item(method, 9, **params), tmp_path, data, inputs)['cache']['producer_called']
    if method=='im':
        import experiments.modular_im as adapter
        monkeypatch.setattr(adapter, 'producer_source_fingerprint', lambda *a: 'c'*64)
    else:
        import experiments.modular_rr as adapter
        monkeypatch.setattr(adapter, 'implementation_fingerprint', lambda *a: 'c'*64)
    assert invoke(smaller, tmp_path, data, inputs)['cache']['producer_called']


@pytest.mark.parametrize('params', [{'im_batch_size': 2}, {'candidate_fraction': .5}])
def test_unverified_celf_parameters_explicitly_remain_exact(tmp_path, params):
    data, inputs = fixture_inputs(count=10)
    params = {'mc_rounds': 3, 'parallel_mc': False, 'im_batch_size': 1, **params}
    large = invoke(item('im', 8, **params), tmp_path, data, inputs)
    small = invoke(item('im', 4, **params), tmp_path, data, inputs)
    assert small['cache']['producer_called'] and not small['cache']['hit']
    assert small['cache']['lookup_policy']=='exact_k'
    assert 'requires' in small['cache']['prefix_reuse_unavailable']
    assert small['artifact']!=large['artifact']


@pytest.mark.parametrize('method', ['im', 'im_rr_greedy'])
def test_ordinary_multibudget_gu_retrain_and_output_identity(tables, method, record_property):
    root, base, gu = tables
    params = {'im_batch_size': 1, 'mc_rounds': 3, 'parallel_mc': False} if method=='im' else {'rr_count': 32}
    write_yaml(root/'prefix.yaml', {'kind':'selector', 'schema_version':1, 'method':method,
        'candidate':{'pool':'train_mask'}, 'budget':{'mode':'ratio','value':.8}, 'parameters':params})
    write_yaml(root/'retrain.yaml', {**gu, 'method':'Retrain', 'parameters':{}})
    changes = dict(stage='unlearning', selector_refs=['prefix.yaml'],
        unlearning_refs=['gu.yaml', 'retrain.yaml'], budget_ratios=[.4, .8])
    result = run(tables, 'prefix_cold', **changes)
    assert sum(s['selection']['cache']['producer_called'] for s in result['selectors'])==1
    selectors = {s['requested_k']:s['selection'] for s in result['selectors']}
    assert selectors[4]['artifact']==selectors[8]['artifact']
    assert all(not u['hit'] and u['producer_called'] for u in result['unlearning'])
    assert len({u['artifact_id'] for u in result['unlearning']})==4
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_output
    path = root/'results/runs/prefix_cold/prefix_cold/run.json'
    manifest, documents = read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
    for cell, doc in zip(manifest['cells'], documents):
        k = doc['selection.json']['requested_k']
        expected = selectors[8]['views']['8']['selected_nodes'][:k]
        assert doc['selection.json']['selected_nodes']==expected
        output = load_output(cell['output'], root/'results/cache_v2', dataset_root=root)
        assert output.arrays['selected_nodes'].tolist()==expected
        assert output.identity['pairing']['selected_nodes']==expected
    warm = run(tables, 'prefix_warm', **changes)
    assert all(u['hit'] for u in warm['unlearning'])
    assert not warm['selector_producer_called']
    record_property('consumer_evidence', json.dumps(dict(selectors=result['selectors'],
        outputs=result['unlearning'], cells=manifest['cells'])))


def test_python_celf_prefix_and_backend_identity(tmp_path, monkeypatch):
    from experiments.selection_producer import load_im_strategy
    load_im_strategy()
    import attack.attack_strategies.im_strategy as backend
    data, inputs = fixture_inputs(count=7)
    spec = item('im', 7, im_batch_size=1, mc_rounds=5, parallel_mc=False)
    numba = invoke(spec, tmp_path/'shared', data, inputs)
    monkeypatch.setattr(backend, 'HAS_NUMBA', False)
    python = invoke(spec, tmp_path/'shared', data, inputs)
    assert python['cache']['producer_called'] and python['artifact']!=numba['artifact']
    for k in (1, 4):
        small = invoke(item('im', k, im_batch_size=1, mc_rounds=5, parallel_mc=False),
            tmp_path/str(k), data, inputs)
        assert small['views'][str(k)]['selected_nodes']==python['views']['7']['selected_nodes'][:k]


@pytest.mark.parametrize('method', ['im', 'im_rr_greedy'])
def test_old_producer_artifact_cannot_be_promoted(tmp_path, method):
    from cache_v2 import ProducerVersion
    from experiments.selection_producer import (SelectionInputs, build_selection_job,
        resolve_or_produce_selection, build_im_producer, ImParameters, load_im_strategy,
        im_algorithm_version, producer_source_fingerprint, IM_PRODUCER_SEMANTIC_VERSION)
    from experiments.modular_rr import select_rr
    from experiments.implementation_identity import implementation_fingerprint
    from experiments.im_score_benchmark.rr_core import DirectedGraph, sample_rr_bundle
    from experiments.im_score_benchmark.selectors import maximum_coverage_greedy
    from utils.target_checkpoint import data_identity
    data, inputs = fixture_inputs(count=10)
    params = {'im_batch_size':1, 'mc_rounds':3, 'parallel_mc':False} if method=='im' else {'rr_count':32}
    spec = item(method, 8, **params)
    effective = spec['parameters']
    identity = {**effective, 'split_hash':data_identity(data)['split_hash'], 'prefix_stable':False}
    if method=='im':
        strategy, has_numba, source = load_im_strategy()
        producer = ProducerVersion(IM_PRODUCER_SEMANTIC_VERSION, producer_source_fingerprint(source, 'im'))
        algorithm = im_algorithm_version(has_numba)
        compute = build_im_producer(inputs, 8, ImParameters(**effective), strategy)
    else:
        identity.update(root_domain='all_nodes', diffusion='directed_static_ic')
        producer = ProducerVersion('opengu-fixed-rr-selection-v1', implementation_fingerprint(
            select_rr, DirectedGraph, sample_rr_bundle, maximum_coverage_greedy))
        algorithm = 'fixed-rr-maximum-coverage-greedy-v1'
        compute = lambda: select_rr(inputs, 8, effective)
    job = build_selection_job(SelectionInputs(inputs, method, effective['im_selector_seed'],
        8, producer, algorithm, identity), compute)
    old = resolve_or_produce_selection(job, tmp_path)
    old_files = {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in tmp_path.rglob('*') if p.is_file()}
    new = invoke(item(method, 4, **params), tmp_path, data, inputs)
    assert new['cache']['producer_called'] and new['artifact']['artifact_id']!=old.artifact_id
    # Immutable payload files retain their exact bytes. Store indexes may grow.
    for path, digest in old_files.items():
        if path.suffix == '.npz':
            assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
