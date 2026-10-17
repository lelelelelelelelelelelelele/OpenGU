"""Bounded old/new comparisons; CPU float32 uses rtol=1e-6, atol=1e-7.

The old expression is test-only. Both paths execute the real callers and real
GNNDeleteTrainer; the only substituted computation is the incident-edge mask.
"""
import copy
import importlib
import json
import logging
import os
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch
from torch_geometric import seed_everything
from torch_geometric.data import Data

from experiments.modular_model import runtime_defaults
from model.base_gnn.gcn import GCNNet
from model.model_zoo import model_zoo
from task.GNNDeleteTrainer import GNNDeleteTrainer


implementation = importlib.import_module('unlearning.unlearning_methods.GNNDelete.gnndelete')
trainer_module = importlib.import_module('task.GNNDeleteTrainer')
NEW_MASK = implementation._incident_edge_mask
RTOL, ATOL = 1e-6, 1e-7


def old_mask(edge_index, nodes, num_nodes):
    # Verbatim three-statement expression from the pre-optimization callers.
    res = [torch.eq(edge_index, aelem).logical_or_(torch.eq(edge_index, aelem)) for aelem in nodes]
    df_mask_edge = torch.any(torch.stack(res, dim=0), dim=0)
    df_mask_edge = df_mask_edge.sum(0).bool()
    return df_mask_edge


def evidence(name, value):
    directory = os.environ.get('AAGU099_EVIDENCE_DIR')
    if directory:
        path = Path(directory) / (name + '.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')


def exact(left, right):
    if isinstance(left, torch.Tensor):
        assert left.dtype == right.dtype and left.device == right.device
        assert left.shape == right.shape and torch.equal(left, right)
    elif isinstance(left, np.ndarray):
        assert left.dtype == right.dtype and np.array_equal(left, right, equal_nan=True)
    elif isinstance(left, dict):
        assert left.keys() == right.keys()
        for key in left:
            exact(left[key], right[key])
    elif isinstance(left, (list, tuple)):
        assert len(left) == len(right)
        for a, b in zip(left, right):
            exact(a, b)
    else:
        assert left == right


@pytest.mark.parametrize('index_dtype', [torch.int32, torch.int64])
@pytest.mark.parametrize('nodes', [[2, 2], [0], [7], [6, 7], list(range(8)), [-1, 2]])
def test_mask_endpoints_and_order(index_dtype, nodes):
    edges = torch.tensor([[0, 1, 1, 2, 2, 3, 4, 4, 5],
                          [1, 0, 1, 1, 3, 2, 4, 5, 4]], dtype=index_dtype)
    request = np.asarray(nodes, dtype=int)
    before = edges.clone()
    expected, observed = old_mask(edges, request, 8), NEW_MASK(edges, request, 8)
    exact(expected, observed)
    exact(edges[:, expected], edges[:, observed])
    exact(edges[:, ~expected], edges[:, ~observed])
    exact(before, edges)


def test_random_masks_and_edgeless_graph():
    generator = torch.Generator().manual_seed(299)
    for n in (1, 4, 17, 71):
        for e in (0, 1, 7, 93):
            edges = torch.randint(n, (2, e), generator=generator)
            for k in (1, 3, 9):
                nodes = torch.randint(n, (k,), generator=generator).numpy()
                exact(old_mask(edges, nodes, n), NEW_MASK(edges, nodes, n))
    evidence('mask_random', dict(status='PASS', comparisons=48, device='cpu', index_dtype='int64'))


def graph():
    seed_everything(730)
    chain = torch.arange(14)
    edges = torch.stack((chain, chain + 1))
    edges = torch.cat((edges, edges.flip(0), torch.tensor([[2, 6], [2, 6]])), dim=1)
    data = Data(x=torch.randn(16, 4), y=torch.arange(16) % 2, edge_index=edges, num_nodes=16)
    data.num_classes = 2
    for name, indices in [('train', list(range(10))), ('val', [10, 11]), ('test', [12, 13, 14, 15])]:
        mask = torch.zeros(16, dtype=torch.bool)
        mask[indices] = True
        setattr(data, name + '_mask', mask)
        setattr(data, name + '_indices', np.asarray(indices, dtype=int))
    return data


def arguments(depth=2, seed=42):
    args = runtime_defaults()
    args.update(dataset_name='cora', downstream_task='node', base_model='GCN',
                unlearning_methods='GNNDelete', unlearning_model='gnndelete_nodeemb',
                unlearn_task='node', num_runs=1, num_shards=1, out_dim=2,
                gcn_num_layers=depth, gcn_hidden=8, hidden_dim=8, device='cpu',
                random_seed=seed, loss_type='both_layerwise', loss_fct='mse_mean',
                unlearn_lr=0.01, unlearning_epochs=3, test_freq=1,
                num_unlearned_nodes=1, formal_expected_k=1, formal_fail_closed=True,
                alpha=0.5, run_update_detection_auc=False)
    return args


class Prepared(Exception):
    """Stop only after the caller has produced all mask-dependent graph state."""


def prepare(monkeypatch, tmp_path, path, nodes, mask_function, formal=False):
    args, data = arguments(), graph()
    args.update(checkpoint_dir=str(tmp_path), formal_fail_closed=formal,
                formal_expected_k=1, num_unlearned_nodes=1)
    def stop(*a, **kw):
        raise Prepared()
    method = implementation.gnndelete(args, logging.getLogger('mask-test'),
                                      SimpleNamespace(data=data, get_model=stop))
    method.device = torch.device('cpu')
    args['checkpoint_dir'] = str(tmp_path)
    request = tmp_path / 'request_0.txt'
    request.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(request, np.asarray(nodes, dtype=int), fmt='%d')
    with monkeypatch.context() as patch:
        patch.setattr(implementation, '_incident_edge_mask', mask_function)
        patch.setattr(implementation, 'root_path', str(tmp_path))
        patch.setattr(implementation, 'unlearning_path', str(tmp_path / 'request'))
        try:
            if path == 'node':
                result = method.delete_node(nodes)
            else:
                result = method.delete_feature()
        except (Prepared, RuntimeError, IndexError, ValueError) as exc:
            result = (type(exc).__name__, str(exc))
    return result, copy.deepcopy(data.to_dict()), method.unlearning_nodes.copy()


@pytest.mark.parametrize('path', ['node', 'feature'])
@pytest.mark.parametrize('nodes', [[2, 2], [2], [15], [0, 15], [], [-1], [16], [-17]])
def test_callers_graph_state_and_original_errors(monkeypatch, tmp_path, path, nodes):
    old = prepare(monkeypatch, tmp_path / 'old', path, nodes, old_mask)
    new = prepare(monkeypatch, tmp_path / 'new', path, nodes, NEW_MASK)
    exact(old, new)
    if nodes == []:
        assert new[0] == ('RuntimeError', 'stack expects a non-empty TensorList')
    elif nodes in ([16], [-17]):
        assert new[0][0] == 'IndexError'
    else:
        assert new[0][0] == 'Prepared'
    evidence('state_' + path + '_' + str(nodes), dict(status='PASS', path=path,
             nodes=nodes, outcome=list(new[0]), compared_data_fields=sorted(new[1])))


@pytest.mark.parametrize('nodes', [[12], [2, 3], [-1]])
def test_formal_validation_unchanged(monkeypatch, tmp_path, nodes):
    old = prepare(monkeypatch, tmp_path / 'old', 'node', nodes, old_mask, formal=True)
    new = prepare(monkeypatch, tmp_path / 'new', 'node', nodes, NEW_MASK, formal=True)
    exact(old, new)
    assert new[0][0] == 'ValueError'


def clone_parameters(model):
    return {name: value.detach().clone() for name, value in model.named_parameters()}


def run_training(monkeypatch, directory, lane, mask_function, depth, seed):
    seed_everything(seed)
    args, data = arguments(depth, seed), graph()
    seed_everything(seed)
    original = GCNNet(args, 4, 2)
    initial = clone_parameters(original)
    trace = dict(losses=[], steps=[], negative_samples=[])
    created = []
    original_factory = model_zoo.get_model
    original_step = torch.optim.Adam.step
    original_backward = torch.Tensor.backward
    original_sampling = trainer_module.negative_sampling

    def factory(zoo, *a, **kw):
        model = original_factory(zoo, *a, **kw)
        created.append(model)
        return model

    def step(optimizer, *a, **kw):
        model = created[-1]
        gradients = {n: None if p.grad is None else p.grad.detach().clone()
                     for n, p in model.named_parameters()}
        result = original_step(optimizer, *a, **kw)
        trace['steps'].append(dict(gradients=gradients, parameters=clone_parameters(model)))
        return result

    def backward(tensor, *a, **kw):
        trace['losses'].append(tensor.detach().clone())
        return original_backward(tensor, *a, **kw)

    def sampling(*a, **kw):
        result = original_sampling(*a, **kw)
        trace['negative_samples'].append(result.clone())
        return result

    directory.mkdir(parents=True)
    args['checkpoint_dir'] = str(directory)
    with monkeypatch.context() as patch:
        patch.setattr(implementation, '_incident_edge_mask', mask_function)
        patch.setattr(model_zoo, 'get_model', factory)
        patch.setattr(torch.optim.Adam, 'step', step)
        patch.setattr(torch.Tensor, 'backward', backward)
        patch.setattr(trainer_module, 'negative_sampling', sampling)
        patch.setattr(implementation, 'root_path', str(directory))
        patch.setattr(implementation, 'unlearning_path', str(directory / 'request'))
        if lane == 'modular':
            from experiments.modular_gu import gnndelete_node
            model, _seconds = gnndelete_node(args, original, data, [2, 2], directory)
            result = None
        else:
            zoo = model_zoo(args, data)
            zoo.model = original
            method = implementation.gnndelete(args, logging.getLogger('training-test'), zoo)
            method.device = torch.device('cpu')
            args.update(checkpoint_dir=str(directory), unlearning_model='gnndelete_nodeemb')
            method.target_model = GNNDeleteTrainer(args, method.logger, original, data)
            if lane == 'feature':
                np.savetxt(directory / 'request_0.txt', [2, 2], fmt='%d')
                checkpoint = directory / 'data/model/node_level/cora/GCN'
                checkpoint.parent.mkdir(parents=True)
                torch.save(original.state_dict(), checkpoint)
                result = method.delete_feature()
            else:
                result = method.delete_node([2, 2])
            model = method.target_model.model
        model.eval()
        with torch.no_grad():
            predictions = model(data.x, data.edge_index).clone()
    assert result is None
    assert len(trace['losses']) == 6 and len(trace['steps']) == 6
    assert len(trace['negative_samples']) == 1
    assert trace['negative_samples'][0].shape[1] == int(data.df_mask.sum())
    assert any(g is not None and g.abs().max() > 0
               for s in trace['steps'] for g in s['gradients'].values())
    assert any(not torch.equal(trace['steps'][0]['parameters'][n], p)
               for n, p in trace['steps'][-1]['parameters'].items())
    return dict(initial=initial, data=data.to_dict(), trace=trace,
                final=clone_parameters(model), predictions=predictions)


@pytest.mark.parametrize('lane', ['node', 'feature', 'modular'])
@pytest.mark.parametrize('depth,seed', [(2, 42), (3, 42), (2, 212), (3, 212)])
def test_real_training_regression(monkeypatch, tmp_path, lane, depth, seed):
    old = run_training(monkeypatch, tmp_path / 'old', lane, old_mask, depth, seed)
    new = run_training(monkeypatch, tmp_path / 'new', lane, NEW_MASK, depth, seed)
    exact(old['initial'], new['initial'])
    exact(old['data'], new['data'])
    exact(old['trace']['negative_samples'], new['trace']['negative_samples'])
    differences = []
    def close(a, b):
        if isinstance(a, torch.Tensor):
            assert a.dtype == b.dtype and a.device == b.device and a.shape == b.shape
            assert torch.isfinite(a).all() and torch.isfinite(b).all()
            torch.testing.assert_close(a, b, rtol=RTOL, atol=ATOL)
            differences.append(float((a - b).abs().max()))
        elif isinstance(a, dict):
            assert a.keys() == b.keys()
            for key in a:
                close(a[key], b[key])
        elif isinstance(a, list):
            assert len(a) == len(b)
            for x, y in zip(a, b):
                close(x, y)
        else:
            assert a == b
    close(old['trace'], new['trace'])
    close(old['final'], new['final'])
    close(old['predictions'], new['predictions'])
    evidence('training_' + lane + '_' + str(depth) + '_' + str(seed),
             dict(status='PASS', lane=lane, depth=depth, seed=seed, epochs=3,
                  device='cpu', dtype='float32', rtol=RTOL, atol=ATOL,
                  max_absolute_difference=max(differences),
                  backward_calls=6, optimizer_steps=6,
                  negative_samples=old['trace']['negative_samples'][0].tolist(),
                  losses=[float(v) for v in old['trace']['losses']],
                  compared=['initial weights', 'all graph fields', 'negative samples',
                            'losses', 'all parameter gradients at every step',
                            'all parameters after every step', 'final parameters', 'predictions']))
