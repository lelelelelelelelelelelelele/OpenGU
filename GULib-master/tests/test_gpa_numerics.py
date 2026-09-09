"""Real GPA losses and NeighborLoader, isolated from global CLI imports."""
import ast
import logging
from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn, optim
from torch.nn import functional as F
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_dense_adj


def implementation(legacy=False):
    path = Path(__file__).resolve().parents[1] / 'unlearning/unlearning_methods/GraphRevoker/lib_partition/partition_gpa.py'
    tree = ast.parse(path.read_text())
    names = {'ncut_loss', 'eff_norm', 'LabelEntropyLoss', 'Partitioner', 'partition_embeddings'}
    tree.body = [node for node in tree.body if getattr(node, 'name', None) in names]
    namespace = dict(globals())
    exec(compile(tree, str(path), 'exec'), namespace)
    if legacy:
        # Exact pre-fix loss expressions; real Partitioner/loader/training stay.
        exec('''
def ncut_loss(Y, A):
    D = torch.sum(A, dim=1)
    Gamma = torch.mm(Y.t(), D.unsqueeze(1).float())
    return torch.sum(torch.mm(torch.div(Y.float(), Gamma.t()), (1 - Y).t().float()) * A.float())
def eff_norm(Y, A, edge_cnt):
    shard_num_nodes = torch.sum(Y, dim=0)
    y = Y.unsqueeze(2)
    shard_edges = torch.einsum('nsc,msc->snm', y, y)
    shard_num_edges = torch.sum((A.unsqueeze(0) * shard_edges).view(y.shape[1], -1), dim=1)
    return torch.sum(((shard_num_nodes / Y.shape[0]) * (shard_num_nodes / Y.shape[0]) * (shard_num_edges / edge_cnt)) ** (1/3))
''', namespace)
    torch.set_num_threads(1)
    return namespace


@pytest.mark.parametrize('values', [[[1., 0.], [1., 0.]],
                                  [[1., 1e-20], [1., 1e-20]],
                                  [[1., 0.], [0., 1.]]])
def test_saturated_and_underflow_old_red_new_green(values):
    adjacency = torch.tensor([[0., 1.], [1., 0.]])
    for legacy in (True, False):
        functions = implementation(legacy)
        y = torch.tensor(values, requires_grad=True)
        cut = functions['ncut_loss'](y, adjacency)
        balance = functions['eff_norm'](y, adjacency, 2)
        (cut + .001 * balance).backward()
        finite = bool(torch.isfinite(cut) & torch.isfinite(balance) & torch.isfinite(y.grad).all())
        assert finite is not legacy
        if not legacy:
            assert torch.isfinite(torch.linalg.vector_norm(y.grad))
            if values == [[1., 0.], [0., 1.]]:
                assert balance.item() == 0.0


def test_edgeless_neighbor_batch_old_red_new_green():
    data = Data(x=torch.tensor([[1., 0.], [0., 1.], [1., 1.]]),
                y=torch.tensor([0, 1, 0]), edge_index=torch.tensor([[0, 1], [1, 0]]),
                train_mask=torch.ones(3, dtype=torch.bool))
    assert [b.num_edges for b in NeighborLoader(data, num_neighbors=[-1, -1], batch_size=1)] == [2, 2, 0]
    parameters = dict(num_shards=2, gpa_hidden_channels=4, gpa_epochs=1,
                      gpa_batch_size=1, shard_size_delta=0.)
    torch.manual_seed(42)
    with pytest.raises(ValueError, match='GPA objective is nonfinite'):
        implementation(True)['partition_embeddings'](data, data.x, parameters, logging.getLogger('test'))
    torch.manual_seed(42)
    assignment, model = implementation()['partition_embeddings'](data, data.x, parameters, logging.getLogger('test'))
    assert set(assignment.tolist()) == {0, 1}
    assert all(torch.isfinite(p).all() for p in model.parameters())
    y = torch.tensor([[.3, .7]], requires_grad=True)
    functions = implementation()
    cut = functions['ncut_loss'](y, torch.zeros(1, 1))
    balance = functions['eff_norm'](y, torch.zeros(1, 1), 0)
    assert cut.item() == balance.item() == 0
    loss = cut + balance * .001 + functions['LabelEntropyLoss'](torch.tensor([0]), 2)(y) * .001
    loss.backward()
    assert torch.isfinite(y.grad).all() and y.grad.abs().sum() > 0


def test_normal_loss_and_gradient_change_is_bounded():
    adjacency = torch.tensor([[0., 1.], [1., 0.]])
    values = torch.tensor([[.7, .3], [.4, .6]])
    records = []
    for legacy in (True, False):
        functions = implementation(legacy)
        y = values.clone().requires_grad_()
        cut, balance = functions['ncut_loss'](y, adjacency), functions['eff_norm'](y, adjacency, 2)
        (cut + balance * .001).backward()
        records.append((cut.detach(), balance.detach(), y.grad))
    old, new = records
    assert torch.equal(old[0], new[0])
    assert abs((old[1] - new[1]).item()) <= 2 * (torch.finfo(torch.float32).eps ** 2) ** (1 / 3) + 1e-7
    torch.testing.assert_close(old[2], new[2], rtol=1e-6, atol=1e-7)


def test_nonfinite_gradient_rejected_before_optimizer_step_with_context():
    functions = implementation()
    original = functions['Partitioner']
    original_forward = original.forward
    def bad_forward(self, x, edges):
        output = original_forward(self, x, edges)
        output.register_hook(lambda gradient: torch.full_like(gradient, float('inf')))
        return output
    original.forward = bad_forward
    data = Data(x=torch.eye(2), y=torch.tensor([0, 1]),
                edge_index=torch.tensor([[0, 1], [1, 0]]), train_mask=torch.ones(2, dtype=torch.bool))
    parameters = dict(num_shards=2, gpa_hidden_channels=4, gpa_epochs=1,
                      gpa_batch_size=2, shard_size_delta=0.)
    with pytest.raises(ValueError, match='GPA gradients are nonfinite: epoch=0, batch=0, nodes=2, edges=2'):
        functions['partition_embeddings'](data, data.x, parameters, logging.getLogger('test'))


@pytest.mark.parametrize('scale', [1., 100.])
def test_real_softmax_and_partitioner_gradients_and_clip(scale):
    functions = implementation()
    edges = torch.tensor([[0, 1], [1, 0]])
    adjacency = torch.tensor([[0., 1.], [1., 0.]])
    logits = nn.Parameter(torch.tensor([[scale, -scale], [-scale, scale]]))
    y = logits.softmax(-1)
    loss = functions['ncut_loss'](y, adjacency) + .001 * functions['eff_norm'](y, adjacency, 2)
    loss.backward()
    assert torch.isfinite(nn.utils.clip_grad_norm_([logits], .5, error_if_nonfinite=True))
    torch.manual_seed(42)
    model = functions['Partitioner'](2, 4, 2)
    output = model(torch.eye(2) * scale, edges)
    objective = functions['ncut_loss'](output, adjacency) + .001 * functions['eff_norm'](output, adjacency, 2)
    objective.backward()
    assert torch.isfinite(nn.utils.clip_grad_norm_(model.parameters(), .5, error_if_nonfinite=True))
