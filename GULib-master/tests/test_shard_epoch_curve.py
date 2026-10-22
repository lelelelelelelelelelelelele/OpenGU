"""Run the real diagnostic loop on tiny graphs, without its standalone setup."""
import ast
import copy
import csv
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import time
from types import SimpleNamespace, MethodType

import numpy as np
import pytest
import torch
from torch.nn import functional as F
from torch_geometric.data import Data
from torch_geometric.utils import subgraph

from attack.cache_identity import seeded_execution
from experiments.modular_model import create_model, runtime_defaults
from experiments.modular_shards import ShardEnsemble, aggregate_weights
from experiments.modular_graphrevoker import graphrevoker_weights
from experiments.node_deletion import retained_graph
from utils.target_checkpoint import capture_state, data_identity, state_hash


SCRIPT = Path(__file__).resolve().parents[1] / 'experiments/diagnostics/shard_epoch_curve.py'


def diagnostic(tmp_path, method, train_count):
    runtime_defaults()
    from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator as Eraser
    from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.optimal_aggregator import OptimalAggregator as Revoker
    torch.set_num_threads(1)
    torch.manual_seed(8)
    n = train_count + 2
    ids = torch.arange(n)
    edges = torch.stack([ids[:-1], ids[1:]])
    data = Data(x=torch.randn(n, 3), y=ids % 2,
                edge_index=torch.cat([edges, edges.flip(0)], dim=1),
                train_mask=ids < train_count, val_mask=ids == train_count,
                test_mask=ids == train_count + 1)
    assignment = (ids % 2).masked_fill(~data.train_mask, -1)
    cfg = dict(model=dict(architecture='OpenGU.GCNNet', layers=2, hidden_channels=4, dropout=.5),
               training=dict(seed=42, epochs=2, optimizer='Adam', lr=.05, weight_decay=.0001),
               parameters=dict(num_shards=2, num_opt_samples=1000, opt_lr=.001, opt_num_epochs=2),
               dataset_input={}, data_identity=data_identity(data), assignment=assignment.tolist())
    study = dict(source_sha='unit-test', device='cpu', data_root=str(tmp_path), seed=42, epochs=2,
                 evaluation_epochs=[1, 2], methods={method: cfg},
                 requests={'IF': {'selected_nodes': [0]}, 'Random': {'selected_nodes': [1]}})
    (tmp_path / 'verification').mkdir()
    (tmp_path / 'verification/validation.json').write_text('{"complete": true}', encoding='utf-8')
    (tmp_path / 'study.yaml').write_text('synthetic fixture', encoding='utf-8')
    namespace = dict(globals(), ROOT=tmp_path, STUDY=study, __file__=str(SCRIPT),
                     Eraser=Eraser, Revoker=Revoker, resolve_input=lambda *args: data.clone())
    tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
    # Execute original function bodies; avoid importing a real study or changing cwd.
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    exec(compile(tree, str(SCRIPT), 'exec'), namespace)
    namespace['event'] = lambda *args, **kwargs: None
    calls = []
    trajectory = namespace['trajectory']

    def counted(*args, **kwargs):
        calls.append(args[3])
        return trajectory(*args, **kwargs)

    namespace['trajectory'] = counted
    return namespace, calls


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
@pytest.mark.parametrize('train_count', [8, 1100])
def test_partial_deletions_match_fresh_production_aggregation(tmp_path, method, train_count, monkeypatch):
    ns, calls = diagnostic(tmp_path, method, train_count)
    monkeypatch.setattr(torch, 'save', lambda *a, **k: pytest.fail('must not save checkpoints'))
    out = tmp_path / 'run'
    out.mkdir()
    ns['run'](out)
    result = json.loads((out / 'run.json').read_text(encoding='utf-8'))
    assert result['complete'] and result['saved_checkpoints'] == 0
    assert calls == [0, 1, 0, 1]  # before: both; each request: just its affected shard
    assert [g['affected_shards'] for g in result['groups']] == [[0, 1], [0], [1]]
    for group in result['groups']:
        # The runner compares weights and predictions to a fresh real adapter.
        assert group['terminal_production_adapter_exact'] is True
        assert len(group['rows']) == 8
        assert {r['aggregation_arm'] for r in group['rows']} == {'original', 'corrected', 'equal', 'fixed_before_final'}
        assert len(group['sample_nodes']) == min(1000, group['retained_train_nodes'])
        assert len(group['shard_metrics']) == 2 * len(group['affected_shards'])
    fixed = [r['weights'] for g in result['groups'] for r in g['rows'] if r['aggregation_arm'] == 'fixed_before_final']
    assert all(w == fixed[0] for w in fixed)
    assert len(list(out.glob('*epoch_loss.csv'))) == 3


def test_empty_sampling_pool_rejected(tmp_path):
    ns, _ = diagnostic(tmp_path, 'GraphEraser', 8)
    data = ns['resolve_input']()
    data.train_mask[:] = False
    cfg = ns['STUDY']['methods']['GraphEraser']
    with pytest.raises(ValueError, match='retained training nodes'):
        ns['sample'](data, cfg)


def test_corrected_objective_uses_logits_and_original_regularizer(tmp_path):
    ns, _ = diagnostic(tmp_path, 'GraphEraser', 8)
    posts = {0: torch.tensor([[-.1, -2.3], [-.3, -1.4]]),
             1: torch.tensor([[-.2, -1.7], [-1.7, -.2]])}
    labels = torch.tensor([0, 1])
    weights = torch.tensor([.3, .7], requires_grad=True)
    loss = ns['corrected_loss'](SimpleNamespace(num_shards=2), posts, labels, weights)
    logits = sum(weights[i] * posts[i] for i in range(2))
    expected = F.cross_entropy(logits, labels) + torch.linalg.vector_norm(weights)
    torch.testing.assert_close(loss, expected, rtol=0, atol=0)
    old = F.cross_entropy(F.softmax(logits, dim=1), labels) + torch.linalg.vector_norm(weights)
    assert not torch.allclose(loss, old)
    torch.testing.assert_close(torch.autograd.grad(loss, weights, retain_graph=True)[0],
                               torch.autograd.grad(expected, weights)[0], rtol=0, atol=0)
