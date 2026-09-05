"""Exact retained-graph training using the existing supervised trainer."""
from __future__ import annotations

import time
from attack.cache_identity import seeded_execution
from experiments.modular_model import create_model, train_supervised
from experiments.node_deletion import retained_graph


def run_retrain(instance, data, selected_nodes, dataset_name):
    """Fresh initialization; no original checkpoint and no GU-method dispatch."""
    retained = retained_graph(data, selected_nodes)
    started = time.perf_counter()
    with seeded_execution(instance['training']['seed']):
        model = create_model(instance['model'], dataset_name, retained, data.x.device)
    with seeded_execution(instance['training']['seed']):
        train_supervised(model, retained, instance['training'], ())
    return model, time.perf_counter() - started
