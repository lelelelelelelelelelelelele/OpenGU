"""Explicit Selection adapter for the existing IDEA influence update."""
from __future__ import annotations

import logging
import time
from types import SimpleNamespace

import numpy as np
import torch
from torch_geometric.nn.conv.gcn_conv import gcn_norm

from experiments.node_deletion import retained_graph


def idea_node(args, model, data, nodes, runtime_root):
    from unlearning.unlearning_methods.IDEA.idea import idea
    from task.IDEATrainer import IDEATrainer

    started = time.perf_counter()
    logger = logging.getLogger('modular.IDEA')
    retained = retained_graph(data, nodes)
    method = idea(args, logger, SimpleNamespace(data=data, model=model))
    method.device = next(model.parameters()).device
    method.target_model = IDEATrainer(args, logger, model, data)
    method.target_model.device = method.device
    data.x_unlearn = data.x.clone()
    data.edge_index_unlearn = retained.edge_index
    selected = np.asarray(nodes, dtype=np.int64)
    method.unlearning_nodes = selected
    method.samples_to_be_unlearned = float(len(selected))
    method.attack_preparations['removed_nodes'] = selected
    method.find_k_hops(selected)
    # Neighborhood discovery uses structure from all nodes, but influence
    # losses must use only the persisted supervised training population.
    method.influence_nodes = np.intersect1d(method.influence_nodes, data.train_indices)
    # Same normalization as IDEA._gen_train_loader. The legacy sampler is not
    # consumed by get_grad; no sampled or synthetic edge graph is necessary.
    _, method.edge_weight = gcn_norm(data.edge_index, num_nodes=data.num_nodes, add_self_loops=False)
    _, method.edge_weight_unlearn = gcn_norm(data.edge_index_unlearn, num_nodes=data.num_nodes, add_self_loops=False)
    model.eval()
    gradients = method.get_grad((method.deleted_nodes, method.feature_nodes, method.influence_nodes))
    method.approxi(gradients)
    if not all(torch.isfinite(p).all() for p in model.parameters()):
        raise ValueError('IDEA produced non-finite model parameters')
    return method.target_model.model, time.perf_counter() - started
