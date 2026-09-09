"""GraphRevoker's GPA partition and optimal aggregation in the independent lane."""
from __future__ import annotations
import logging
from pathlib import Path
import math
import time
from types import SimpleNamespace
import numpy as np
import torch
from torch_geometric.utils import subgraph
from experiments.effective_config import ConfigurationError


def graphrevoker_defaults(defaults):
    value = {key: defaults[key] for key in (
        'num_shards', 'shard_size_delta', 'aggregator', 'opt_lr', 'opt_num_epochs', 'num_opt_samples')}
    value.update(partition_method='gpa', gpa_epochs=10, gpa_hidden_channels=256,
                 gpa_batch_size=512, gpa_lr=.001, gpa_weight_decay=.00001)
    return value


def validate_graphrevoker(parameters):
    if parameters['partition_method'] != 'gpa' or parameters['aggregator'] != 'optimal':
        raise ConfigurationError('GraphRevoker node lane requires gpa / optimal')
    for key in ('num_shards', 'opt_num_epochs', 'num_opt_samples', 'gpa_epochs', 'gpa_hidden_channels', 'gpa_batch_size'):
        if type(parameters[key]) is not int or parameters[key] <= 0:
            raise ConfigurationError('invalid GraphRevoker ' + key)
    if parameters['num_shards'] < 2:
        raise ConfigurationError('GraphRevoker requires at least two shards')
    for key in ('opt_lr', 'gpa_lr', 'gpa_weight_decay', 'shard_size_delta'):
        if not math.isfinite(parameters[key]) or parameters[key] < 0:
            raise ConfigurationError('invalid GraphRevoker ' + key)
    if parameters['gpa_lr'] == 0 or parameters['opt_lr'] == 0:
        raise ConfigurationError('GraphRevoker learning rates must be positive')


def graphrevoker_partition(instance, data):
    from experiments.modular_model import create_model, train_supervised
    from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition_gpa import partition_embeddings
    # NodeEmbedding.encoder actually trains the base classifier and returns its
    # train-node log-softmax outputs. The modular lane keeps those semantics
    # without its global checkpoint/embedding files.
    encoder = create_model(instance['model'], 'graphrevoker', data, data.x.device)
    train_supervised(encoder, data, instance['training'], (instance['training']['epochs'],))
    encoder.eval()
    with torch.no_grad():
        embeddings = torch.log_softmax(encoder(data.x, data.edge_index)[data.train_mask], dim=-1)
    local, partitioner = partition_embeddings(data, embeddings, instance['parameters'],
                                             logging.getLogger('modular.GraphRevoker'))
    assignment = torch.full((data.num_nodes,), -1, dtype=torch.long, device=data.x.device)
    assignment[data.train_mask] = local
    return assignment, encoder, partitioner


def graphrevoker_weights(ensemble, data, parameters):
    from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.optimal_aggregator import OptimalAggregator
    nodes = data.train_mask.nonzero().flatten()
    count = parameters['num_opt_samples']
    if count == 10000:
        count = max(1, int(len(nodes) * .1))
    elif count == 1:
        count = len(nodes)
    if count > len(nodes):
        raise ConfigurationError('GraphRevoker aggregation sample count exceeds retained training nodes')
    nodes = nodes[torch.as_tensor(np.random.choice(len(nodes), count, replace=False), device=nodes.device)].sort().values
    edges, _ = subgraph(nodes, data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)
    optimizer = OptimalAggregator(0, SimpleNamespace(model=ensemble), data, parameters,
                                  logging.getLogger('modular.GraphRevoker'))
    optimizer.device = data.x.device
    optimizer.true_labels = data.y[nodes]
    with torch.no_grad():
        optimizer.posteriors = {i: torch.log_softmax(model(data.x[nodes], edges), dim=-1)
                                for i, model in enumerate(ensemble.shard_models)}
    weights = optimizer.optimization().detach().to(data.x.device)
    if not torch.isfinite(weights).all() or (weights < 0).any() or weights.sum() <= 0:
        raise ConfigurationError('invalid GraphRevoker aggregation weights')
    return weights


def initial_graphrevoker_ensemble(instance, data):
    from experiments.modular_shards import ShardEnsemble, train_shard
    from experiments.node_deletion import retained_graph
    assignment, encoder, partitioner = graphrevoker_partition(instance, data)
    models = [train_shard(instance, data, assignment, i) for i in range(instance['parameters']['num_shards'])]
    ensemble = ShardEnsemble(models, assignment, torch.ones(len(models), device=data.x.device) / len(models)).eval()
    # Include the actual encoder/partitioner states in the persisted state_dict.
    ensemble.partition_encoder = encoder
    ensemble.partitioner = partitioner
    ensemble.weights.copy_(graphrevoker_weights(ensemble, data, instance['parameters']))
    return ensemble.eval()


def prepare_graphrevoker_ensemble(instance, data, checkpoint_root):
    from cache_v2 import canonical_sha256
    from utils.target_checkpoint import data_identity, load_target_checkpoint, save_target_checkpoint, capture_state
    from experiments.modular_model import create_model, train_supervised, numerical_environment
    from experiments.modular_shards import ShardEnsemble, train_shard
    from experiments.implementation_identity import implementation_fingerprint, model_functions
    from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition_gpa import Partitioner
    from attack.cache_identity import seeded_execution
    encoder = create_model(instance['model'], 'graphrevoker', data, data.x.device)
    metadata = {'method': 'GraphRevoker', 'data_identity': data_identity(data),
        'model': instance['model'], 'training': instance['training'], 'parameters': instance['parameters'],
        'numerics': numerical_environment(data),
        'implementation': implementation_fingerprint(initial_graphrevoker_ensemble,
            *graphrevoker_implementation_functions(), ShardEnsemble, train_shard,
            create_model, train_supervised, *model_functions(encoder))}
    path = Path(checkpoint_root) / ('graphrevoker-' + canonical_sha256(metadata) + '.pt')
    hit = path.exists()
    if not hit:
        with seeded_execution(instance['training']['seed']):
            ensemble = initial_graphrevoker_ensemble(instance, data)
        state = capture_state(ensemble)
        save_target_checkpoint(path, state_dict=state, metadata=metadata, checkpoints=[{
            'global_step': instance['training']['epochs'], 'update_lr': instance['training']['lr'], 'state': state}])
    loaded = load_target_checkpoint(path, expected_metadata=metadata)
    state = loaded['state_dict']
    models = [create_model(instance['model'], 'shard', data, data.x.device) for _ in state['weights']]
    ensemble = ShardEnsemble(models, state['assignment'].to(data.x.device), state['weights'].to(data.x.device))
    ensemble.partition_encoder = encoder
    ensemble.partitioner = Partitioner(int(data.y.max()) + 1,
        instance['parameters']['gpa_hidden_channels'], instance['parameters']['num_shards']).to(data.x.device)
    ensemble.load_state_dict(state, strict=True)
    return ensemble.eval(), {'state_hash': loaded['state_hash'], 'file_sha256': loaded['file_sha256'], 'hit': hit}


def run_graphrevoker(instance, data, nodes, ensemble):
    from experiments.modular_shards import train_shard
    from experiments.node_deletion import retained_graph
    assignment = ensemble.assignment
    retained = retained_graph(data, nodes)
    evaluation = data if instance['deletion']['evaluation_graph'] == 'original' else retained
    with torch.no_grad():
        method_before = ensemble(evaluation.x, evaluation.edge_index).detach().clone()
    affected = sorted(set(assignment[torch.as_tensor(nodes, device=data.x.device)].tolist()))
    started = time.perf_counter()
    for shard in affected:
        ensemble.shard_models[shard] = train_shard(instance, retained, assignment, shard)
    ensemble.weights.copy_(graphrevoker_weights(ensemble, retained, instance['parameters']))
    return ensemble.eval(), method_before, time.perf_counter() - started


def graphrevoker_implementation_functions():
    from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition_gpa import (
        partition_embeddings, Partitioner, LabelEntropyLoss, ncut_loss, eff_norm)
    from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.optimal_aggregator import OptimalAggregator
    from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.opt_dataset import OptDataset
    return [run_graphrevoker, graphrevoker_partition, graphrevoker_weights, initial_graphrevoker_ensemble,
            prepare_graphrevoker_ensemble,
            partition_embeddings, Partitioner, LabelEntropyLoss, ncut_loss, eff_norm,
            OptimalAggregator, OptDataset]
