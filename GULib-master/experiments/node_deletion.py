"""Explicit node request semantics shared by Retrain and its comparisons."""
from __future__ import annotations

import torch
from experiments.effective_config import ConfigurationError, effective, choice
from utils.target_checkpoint import data_identity


def resolve_deletion(value=None):
    result = effective(value or {}, {
        'task': 'node',
        'supervision': 'exclude_selected',
        'training_graph': 'remove_incident_edges',
        'features': 'retain_isolated_rows',
        'evaluation_graph': 'original',
    }, 'deletion')
    for name, expected in (
        ('task', 'node'), ('supervision', 'exclude_selected'),
        ('training_graph', 'remove_incident_edges'), ('features', 'retain_isolated_rows'),
    ):
        choice(result[name], (expected,), 'deletion.' + name)
    choice(result['evaluation_graph'], ('original', 'retained'), 'deletion.evaluation_graph')
    return result


def retained_graph(data, nodes):
    indices = torch.tensor(list(nodes), device=data.x.device, dtype=torch.long)
    if (indices.ndim != 1 or not indices.numel()
            or indices.unique().numel() != indices.numel()
            or (indices < 0).any() or (indices >= data.num_nodes).any()
            or not data.train_mask[indices].all()):
        raise ConfigurationError('node deletion needs unique selected training nodes')
    result = data.clone()
    result.train_mask[indices] = False
    if not result.train_mask.any():
        raise ConfigurationError('node deletion leaves no supervised training nodes')
    removed = torch.zeros(data.num_nodes, dtype=torch.bool, device=data.x.device)
    removed[indices] = True
    edge_mask = ~(removed[data.edge_index[0]] | removed[data.edge_index[1]])
    result.edge_index = data.edge_index[:, edge_mask].clone()
    for name in ('train', 'val', 'test'):
        setattr(result, name + '_indices', getattr(result, name + '_mask').nonzero().flatten().cpu().numpy())
    return result


def pairing_identity(instance, data, nodes):
    retained = retained_graph(data, nodes)
    evaluation = data if instance['deletion']['evaluation_graph'] == 'original' else retained
    return {
        'data_identity': data_identity(data),
        'selected_nodes': list(map(int, nodes)),
        'model': instance['model'], 'training': instance['training'],
        'deletion': instance['deletion'],
        'training_graph_identity': data_identity(retained),
        'evaluation_graph_identity': data_identity(evaluation),
    }
