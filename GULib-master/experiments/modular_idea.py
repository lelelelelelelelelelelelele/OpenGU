"""Explicit Selection adapter for the existing IDEA influence update."""
from __future__ import annotations

import json
from pathlib import Path
import logging
import time
from types import SimpleNamespace

import numpy as np
import torch

from experiments.node_deletion import retained_graph


def idea_node(args, model, data, nodes, runtime_root, observer=None):
    from unlearning.unlearning_methods.IDEA.idea import idea
    from task.IDEATrainer import IDEATrainer

    started = time.perf_counter()
    logger = logging.getLogger('modular.IDEA')
    retained = retained_graph(data, nodes)
    method = idea(args, logger, SimpleNamespace(data=data, model=model))
    method.observer = observer
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
    # The trained GCN/SGC already normalizes raw edges internally. Passing
    # gcn_norm weights here normalizes twice and changes the loss/Hessian.
    method.edge_weight = None
    method.edge_weight_unlearn = None
    model.eval()
    gradients = method.get_grad((method.deleted_nodes, method.feature_nodes, method.influence_nodes))
    try:
        method.approxi(gradients)
    finally:
        if hasattr(method, 'solver_diagnostics'):
            (Path(runtime_root) / 'idea-solver.json').write_text(
                json.dumps(method.solver_diagnostics, indent=2, allow_nan=False), encoding='utf-8')
    if not all(torch.isfinite(p).all() for p in model.parameters()):
        raise ValueError('IDEA produced non-finite model parameters')
    return method.target_model.model, time.perf_counter() - started
