"""Observer semantics, noninterference and ordinary run/metrics return contract."""
import copy
import hashlib
import json
import random

import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from experiments.observers import LinearSolverTrace, SameGraphChange, validate_capabilities
from unlearning.unlearning_methods.GIF.solver import solve_gif_system


@pytest.mark.parametrize('method', ['GIF', 'IDEA'])
def test_exact_linear_residual_and_no_interference(method):
    matrix = torch.diag(torch.tensor([2., 3.], dtype=torch.double))
    rhs = torch.tensor([1., -2.], dtype=torch.double)
    original = rhs.clone()
    observer = LinearSolverTrace({})
    rng = torch.random.get_rng_state().clone()
    plain, _ = solve_gif_system(lambda x: matrix@x, rhs, iterations=400, scale=5., damp=.1)
    observed, _ = solve_gif_system(lambda x: matrix@x, rhs, iterations=400, scale=5., damp=.1,
                                    observer=observer, method=method)
    assert torch.equal(plain, observed) and torch.equal(rhs, original)
    assert torch.equal(rng, torch.random.get_rng_state())
    assert [row['step'] for row in observer.rows] == list(range(401))
    expected = torch.linalg.solve(matrix+.5*torch.eye(2), rhs)
    torch.testing.assert_close(observed, expected)
    last = observer.rows[-1]
    assert last['shifted_relative_residual'] < 1e-12
    assert last['original_relative_residual'] > .1
    assert observer.rows[0]['update_l2'] == pytest.approx(float(torch.linalg.vector_norm(rhs/5)))


def test_zero_rhs_is_undefined_not_pass():
    observer = LinearSolverTrace({})
    solve_gif_system(lambda x: x, torch.zeros(2), iterations=100, scale=5., damp=.1, observer=observer)
    assert observer.rows[0]['shifted_relative_residual'] is None
    assert observer.rows[0]['denominator_status'] == 'zero_rhs_undefined_relative'


def test_callable_replacement_and_autograd_graph_survives():
    parameter = torch.tensor([1., 2.], requires_grad=True)
    parameter.grad = torch.tensor([7., 8.])
    gradient, = torch.autograd.grad((parameter**2).sum(), parameter, create_graph=True)
    def matvec(v):
        return torch.autograd.grad((gradient*v).sum(), parameter, retain_graph=True)[0]
    trace = LinearSolverTrace({})
    events = []
    first, _ = solve_gif_system(matvec, torch.ones(2), iterations=3, scale=5, damp=.1, observer=trace)
    second, _ = solve_gif_system(matvec, torch.ones(2), iterations=3, scale=5, damp=.1, observer=events.append)
    assert torch.equal(first, second)
    assert [e['step'] for e in events] == [0, 1, 2, 3]
    assert torch.equal(parameter.grad, torch.tensor([7., 8.]))
    assert torch.equal(matvec(torch.ones(2)), torch.tensor([2., 2.]))


def test_capabilities_and_cache_fail_closed():
    spec = {'name': 'linear_solver_trace', 'parameters': {}}
    with pytest.raises(ValueError, match='does not provide'):
        validate_capabilities('Retrain', [spec], 'disabled')
    with pytest.raises(ValueError, match='requires'):
        validate_capabilities('GIF', [spec], 'reuse')


@pytest.mark.parametrize('method', ['GIF', 'IDEA'])
def test_real_graph_run_uncached_observers_metrics_and_hashes(tables, method):
    from experiments.modular_artifacts import read_run, output_paths
    from experiments.modular_config import load_experiment
    from experiments.unlearning_outputs import load_output
    root, _, gu = tables
    gu.update(method=method, parameters=dict(iteration=2, scale=100, damp=.1))
    if method == 'IDEA':
        gu['parameters'].update(gaussian_mean=0., gaussian_std=0.)
    write_yaml(root/'method.yaml', gu)
    write_yaml(root/'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {}})
    for name in ('linear_solver_trace', 'same_graph_change'):
        write_yaml(root/(name+'.yaml'), dict(kind='observer', schema_version=1, name=name))
    opts = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['method.yaml', 'retrain.yaml'])
    plain = run(tables, 'plain', **opts)
    policies = dict(execution={'gu_cache': {method: 'disabled', 'Retrain': 'reuse'}},
        observers=[dict(ref='./'+name+'.yaml', methods=[method]) for name in ('linear_solver_trace', 'same_graph_change')])
    cached_outputs = set((root/'results/cache_v2/artifacts/prediction').glob('*/payload.npz'))
    observed = run(tables, 'observed', **opts, **policies)
    again = run(tables, 'again', **opts, **policies)
    assert set((root/'results/cache_v2/artifacts/prediction').glob('*/payload.npz')) == cached_outputs
    assert observed['unlearning'][0]['producer_called'] and again['unlearning'][0]['producer_called']
    assert observed['unlearning'][1]['hit'] and again['unlearning'][1]['hit']
    assert not observed['selector_producer_called']
    assert observed['unlearning'][0]['checkpoint']['hit']
    store = root/'results/cache_v2'
    before = load_output(plain['unlearning'][0]['output'], store, dataset_root=root)
    after = load_output(observed['unlearning'][0]['output'], store, dataset_root=root)
    assert np.array_equal(before.arrays['logits'], after.arrays['logits'])
    assert all(np.array_equal(before.state[k], after.state[k]) for k in before.state)
    source = root/'results/runs/observed/observed/run.json'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    result, documents = read_run(source, digest)
    cell = result['cells'][0]
    assert cell['cache']['method'] == 'disabled'
    assert len(cell['observers']) == 2
    trace = documents[0]['observers/linear_solver_trace/trace.jsonl']
    assert [r['step'] for r in trace] == [0, 1, 2]
    assert set(documents[0]['observers/same_graph_change/result.json']['measurements']['graphs']) == {'original', 'retained'}
    declared = set(output_paths(source, load_experiment(root/'observed.yaml')))
    actual = {(source.parent/c['path']/f).as_posix() for c in result['cells'] for f in c['files']}
    assert actual == declared
    assert not any(p.endswith('output.npz') for p in declared)
    metrics = run(tables, 'metrics-observed', stage='metrics', selector_refs=[],
        output_inputs=[{'run': str(source), 'sha256': digest}], evaluation_refs=['utility.yaml'])
    assert metrics['evaluations']
    # Corrupt only a scalar return file: normal read_run must reject it.
    trace_path = source.parent/cell['path']/'observers/linear_solver_trace/trace.jsonl'
    trace_path.write_text('{}\n', encoding='utf-8')
    with pytest.raises(ValueError, match='checksum'):
        read_run(source, digest)


def test_same_graph_preserves_modes_gradients_and_rng(tables):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance
    from experiments.modular_model import create_model
    root, _, _ = tables
    data, _ = read_dataset(load_instance(root/'dataset.yaml', 'dataset_split'), root)
    model = create_model({'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 4}, 'cpu_fixture', data, 'cpu')
    model.train()
    for p in model.parameters():
        p.grad = torch.ones_like(p)
    params = copy.deepcopy(model.state_dict())
    grads = [p.grad.clone() for p in model.parameters()]
    graph = data.clone()
    rng, py, numpy = torch.random.get_rng_state().clone(), random.getstate(), np.random.get_state()
    observer = SameGraphChange({})
    for phase in ('unlearning_start', 'unlearning_end'):
        observer(dict(method='GIF', phase=phase, step=None, values=dict(model=model, graphs={'original': data, 'retained': data})))
    assert model.training and all(module.training for module in model.modules())
    assert all(torch.equal(params[k], v) for k, v in model.state_dict().items())
    assert all(torch.equal(g, p.grad) for g, p in zip(grads, model.parameters()))
    assert torch.equal(graph.x, data.x) and torch.equal(graph.edge_index, data.edge_index)
    assert torch.equal(rng, torch.random.get_rng_state()) and py == random.getstate()
    assert np.array_equal(numpy[1], np.random.get_state()[1])


def test_failure_keeps_partial_observation(tables, monkeypatch):
    from experiments.observers import LinearSolverTrace
    root, _, gu = tables
    gu.update(method='GIF', parameters=dict(iteration=3, scale=100, damp=.1))
    write_yaml(root/'method.yaml', gu)
    write_yaml(root/'trace.yaml', dict(kind='observer', schema_version=1, name='linear_solver_trace'))
    original = LinearSolverTrace.__call__
    def fail(self, event):
        original(self, event)
        if event['step'] == 1:
            raise RuntimeError('diagnostic failure')
    monkeypatch.setattr(LinearSolverTrace, '__call__', fail)
    with pytest.raises(RuntimeError, match='diagnostic failure'):
        run(tables, 'failed', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['method.yaml'],
            execution={'gu_cache': {'GIF': 'disabled'}}, observers=[{'ref': './trace.yaml', 'methods': ['GIF']}])
    source = root/'results/runs/failed/failed/run.json'
    value = json.loads(source.read_text())
    assert value['status'] == 'failed' and value['cells'][0]['status'] == 'failed'
    result = json.loads(next(source.parent.rglob('result.json')).read_text())
    assert result['status'] == 'failed' and result['coverage'] == [0, 1]
    assert not list(source.parent.rglob('output.npz'))

