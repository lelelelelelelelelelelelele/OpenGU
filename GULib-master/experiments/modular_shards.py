"""Independent GraphEraser lane with persisted shard models and aggregation.

Partition and aggregation reuse the method's existing implementations. Dataset
loading, checkpoint storage and training parameters belong to the modular lane.
"""
from __future__ import annotations

import copy
import logging
import math
import time
from pathlib import Path

import numpy as np
import torch
from torch_geometric.utils import subgraph

from experiments.effective_config import ConfigurationError


def grapheraser_defaults(defaults):
    return {name: defaults[name] for name in (
        'num_shards', 'partition_method', 'shard_size_delta', 'terminate_delta',
        'aggregator', 'opt_lr', 'opt_num_epochs', 'num_opt_samples')}


def validate_grapheraser(parameters):
    if parameters['partition_method'] != 'lpa_base' or parameters['aggregator'] != 'optimal':
        raise ConfigurationError('GraphEraser node lane requires lpa_base / optimal')
    for key in ('num_shards', 'opt_num_epochs', 'num_opt_samples'):
        if type(parameters[key]) is not int or parameters[key] <= 0:
            raise ConfigurationError('invalid GraphEraser ' + key)
    if parameters['num_shards'] < 2 or parameters['opt_lr'] <= 0 or parameters['shard_size_delta'] < 0:
        raise ConfigurationError('invalid GraphEraser partition/optimizer settings')


def partition_nodes(data, parameters):
    from unlearning.unlearning_methods.GraphEraser.partition.constrained_lpa_base import ConstrainedLPABase
    nodes = data.train_mask.nonzero().flatten().cpu().numpy()
    if len(nodes) < parameters['num_shards']:
        raise ConfigurationError('fewer training nodes than GraphEraser shards')
    edges, _ = subgraph(torch.as_tensor(nodes, device=data.x.device), data.edge_index,
                        relabel_nodes=True, num_nodes=data.num_nodes)
    adjacency = np.zeros((len(nodes), len(nodes)), dtype=bool)
    source, target = edges.cpu().numpy()
    adjacency[source, target] = True
    adjacency[target, source] = True
    threshold = math.ceil(len(nodes) / parameters['num_shards'] + parameters['shard_size_delta'] *
                          (len(nodes) - len(nodes) / parameters['num_shards']))
    algorithm = ConstrainedLPABase(logging.getLogger('modular.GraphEraser'), adjacency,
        parameters['num_shards'], threshold, parameters['terminate_delta'])
    algorithm.initialization()
    communities, _ = algorithm.community_detection()
    assignment = torch.full((data.num_nodes,), -1, dtype=torch.long, device=data.x.device)
    for shard in range(parameters['num_shards']):
        members = sorted(communities[shard])
        if not members:
            raise ConfigurationError('GraphEraser partition produced an empty shard')
        assignment[torch.as_tensor(nodes[members], device=data.x.device)] = shard
    if (assignment[data.train_mask] < 0).any():
        raise ConfigurationError('GraphEraser partition omitted training nodes')
    return assignment


class ShardEnsemble(torch.nn.Module):
    """Full-node posterior interface; state includes every shard and partition."""
    def __init__(self, models, assignment, weights):
        super().__init__()
        self.shard_models = torch.nn.ModuleList(models)
        self.register_buffer('assignment', assignment)
        self.register_buffer('weights', weights)

    def shard_predictions(self, x, edge_index):
        values = []
        for shard, model in enumerate(self.shard_models):
            # Keep held-out nodes in each shard's inference graph. Other
            # shards' training nodes stay isolated and cannot send messages.
            allowed = (self.assignment == shard) | (self.assignment < 0)
            keep = allowed[edge_index[0]] & allowed[edge_index[1]]
            values.append(torch.log_softmax(model(x, edge_index[:, keep]), dim=-1))
        return values

    def forward(self, x, edge_index):
        return sum(weight * logits for weight, logits in
                   zip(self.weights, self.shard_predictions(x, edge_index)))


def train_shard(instance, data, assignment, shard):
    from experiments.modular_model import create_model, train_supervised, numerical_environment
    from attack.cache_identity import seeded_execution
    training = copy.deepcopy(instance['training'])
    shard_data = data.clone()
    shard_data.train_mask = data.train_mask & (assignment == shard)
    if not shard_data.train_mask.any():
        raise ConfigurationError('deletion leaves an empty supervised shard')
    allowed = (assignment == shard) | (assignment < 0)
    keep = allowed[data.edge_index[0]] & allowed[data.edge_index[1]]
    shard_data.edge_index = data.edge_index[:, keep]
    with seeded_execution(training['seed']):
        model = create_model(instance['model'], 'shard', data, data.x.device)
        train_supervised(model, shard_data, training, (training['epochs'],))
    return model.eval()


def aggregate_weights(ensemble, data, parameters):
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator
    nodes = data.train_mask.nonzero().flatten()
    count = parameters['num_opt_samples']
    if count == 10000:
        count = max(1, int(len(nodes) * 0.1))
    elif count == 1:
        count = len(nodes)
    if count > len(nodes):
        raise ConfigurationError('aggregation sample count exceeds retained training nodes')
    nodes = nodes[torch.as_tensor(np.random.choice(len(nodes), count, replace=False), device=nodes.device)].sort().values
    # The original optimal aggregator evaluates its sampled induced graph.
    edge_index, _ = subgraph(nodes, data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)
    optimizer = OptimalAggregator(0, SimpleNamespace(model=ensemble), data, parameters, logging.getLogger('modular.GraphEraser'))
    optimizer.device = data.x.device
    optimizer.true_labels = data.y[nodes]
    with torch.no_grad():
        optimizer.posteriors = {index: torch.log_softmax(model(data.x[nodes], edge_index), dim=-1)
                                for index, model in enumerate(ensemble.shard_models)}
    weights = optimizer.optimization().detach()
    if not torch.isfinite(weights).all() or (weights < 0).any() or weights.sum() <= 0:
        raise ConfigurationError('invalid learned aggregation weights')
    return weights


def initial_ensemble(instance, data):
    assignment = partition_nodes(data, instance['parameters'])
    models = [train_shard(instance, data, assignment, shard) for shard in range(instance['parameters']['num_shards'])]
    ensemble = ShardEnsemble(models, assignment, torch.ones(len(models), device=data.x.device) / len(models)).eval()
    ensemble.weights.copy_(aggregate_weights(ensemble, data, instance['parameters']))
    return ensemble


def prepare_ensemble(instance, data, checkpoint_root):
    from cache_v2 import canonical_sha256
    from utils.target_checkpoint import data_identity, load_target_checkpoint, save_target_checkpoint, capture_state
    from experiments.modular_model import create_model, train_supervised
    from experiments.implementation_identity import implementation_fingerprint
    from unlearning.unlearning_methods.GraphEraser.partition.constrained_lpa_base import ConstrainedLPABase
    from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator
    from model.base_gnn.gcn import GCNNet
    from attack.cache_identity import seeded_execution
    metadata = {'method': 'GraphEraser', 'data_identity': data_identity(data),
        'model': instance['model'], 'training': instance['training'], 'parameters': instance['parameters'],
        'numerics': str(data.x.dtype),
        'implementation': implementation_fingerprint(initial_ensemble, partition_nodes, ConstrainedLPABase,
            ShardEnsemble, train_shard, train_supervised, GCNNet, aggregate_weights, OptimalAggregator)}
    path = Path(checkpoint_root) / ('grapheraser-' + canonical_sha256(metadata) + '.pt')
    hit = path.exists()
    if not hit:
        with seeded_execution(instance['training']['seed']):
            ensemble = initial_ensemble(instance, data)
        state = capture_state(ensemble)
        save_target_checkpoint(path, state_dict=state, metadata=metadata, checkpoints=[{
            'global_step': instance['training']['epochs'], 'update_lr': instance['training']['lr'], 'state': state}])
    loaded = load_target_checkpoint(path, expected_metadata=metadata)
    state = loaded['state_dict']
    models = [create_model(instance['model'], 'shard', data, data.x.device) for _ in state['weights']]
    ensemble = ShardEnsemble(models, state['assignment'].to(data.x.device), state['weights'].to(data.x.device))
    ensemble.load_state_dict(state, strict=True)
    return ensemble.eval(), {'state_hash': loaded['state_hash'], 'file_sha256': loaded['file_sha256'], 'hit': hit}


def run_grapheraser(instance, data, nodes, ensemble):
    from experiments.node_deletion import retained_graph
    assignment = ensemble.assignment
    retained = retained_graph(data, nodes)
    evaluation = data if instance['deletion']['evaluation_graph'] == 'original' else retained
    with torch.no_grad():
        method_before = ensemble(evaluation.x, evaluation.edge_index).detach().clone()
    affected = sorted(set(assignment[torch.as_tensor(nodes, device=data.x.device)].tolist()))
    start = time.perf_counter()
    for shard in affected:
        ensemble.shard_models[shard] = train_shard(instance, retained, assignment, shard)
    ensemble.weights.copy_(aggregate_weights(ensemble, retained, instance['parameters']))
    return ensemble.eval(), method_before, time.perf_counter() - start


def shard_producer(method, model_config):
    from cache_v2 import ProducerVersion
    from experiments.implementation_identity import implementation_fingerprint, model_functions
    from experiments.modular_model import create_model, train_supervised, runtime_defaults
    from experiments.node_deletion import retained_graph, pairing_identity
    runtime_defaults()
    from unlearning.unlearning_methods.GraphEraser.partition.constrained_lpa_base import ConstrainedLPABase
    from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator
    from unlearning.unlearning_methods.GraphEraser.aggregation.opt_dataset import OptDataset
    from model.base_gnn.gcn import GCNNet
    if method != 'GraphEraser':
        raise ConfigurationError('unsupported shard lane: ' + method)
    return ProducerVersion('opengu-independent-grapheraser-output-v1', implementation_fingerprint(
        partition_nodes, ConstrainedLPABase, ShardEnsemble, train_shard, aggregate_weights,
        OptimalAggregator, OptDataset, initial_ensemble, prepare_ensemble, run_grapheraser, run_shard_unlearning,
        create_model, train_supervised, GCNNet, retained_graph, pairing_identity))


def run_shard_unlearning(instance, *, selection, model, data, dataset_name, checkpoint,
                        store_root, runtime_root, dataset_input, dataset_root):
    from cache_v2 import ArtifactRecipe, ArtifactType
    from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
    from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact
    from experiments.unlearning_outputs import output_reference, load_output, utility
    from experiments.node_deletion import pairing_identity, retained_graph
    from experiments.selection_inputs import make_dataset_selection_inputs
    from experiments.output_metrics import evaluate_method
    from attack.cache_identity import seeded_execution
    inputs = make_dataset_selection_inputs(data, dataset_name=dataset_name)
    ensemble, preparation = prepare_ensemble(instance, data,
        Path(store_root).parent / 'runtime' / 'modular' / 'checkpoints')
    target = {'method': instance['method'], 'parameters': instance['parameters'],
              'checkpoint_state_hash': checkpoint['state_hash'], 'initialization': 'independent-shard-training',
              'ensemble_state_hash': preparation['state_hash']}
    producer = shard_producer(instance['method'], instance['model'])
    identity = {'dataset_input': dataset_input, 'target': target,
        'pairing': pairing_identity(instance, data, selection.selected_nodes),
        'selection': {k: getattr(selection, k) for k in ('artifact_id', 'recipe_hash', 'content_hash')},
        'graph_fingerprint': inputs.graph_fingerprint, 'producer_version': producer.to_dict()}
    request = FormalArtifactRequest(ArtifactType.PREDICTION,
        ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity}), producer)
    stored = resolve_formal_artifact(Path(store_root), request)
    hit, seconds = stored is not None, 0.0
    if not hit:
        with seeded_execution(instance['training']['seed']):
            ensemble, method_before, seconds = run_grapheraser(instance, data, list(selection.selected_nodes), ensemble)
        evaluation = data if instance['deletion']['evaluation_graph'] == 'original' else retained_graph(data, selection.selected_nodes)
        with torch.no_grad():
            logits = ensemble(evaluation.x, evaluation.edge_index)
            canonical_before = model(evaluation.x, evaluation.edge_index)
        arrays = {'logits': logits.cpu().numpy(), 'logits_before': method_before.cpu().numpy(),
                  'selected_nodes': np.asarray(selection.selected_nodes, dtype=np.int64)}
        payload = UnlearningOutputPayload(identity, arrays,
            {key: value.detach().cpu().numpy() for key, value in ensemble.state_dict().items()},
            {'canonical_logits_before': canonical_before.cpu().numpy()})
        stored = store_formal_artifact(store_root, request, payload, compute_seconds=seconds)
    reference = output_reference(stored, request.recipe.recipe_hash)
    verified = load_output(reference, store_root, data=data, dataset_root=dataset_root)
    return {**reference, 'output': reference, 'hit': hit, 'producer_called': not hit,
            'compute_seconds': seconds, 'result': utility(verified), 'target': target, 'ensemble_preparation': preparation,
            'evaluation': evaluate_method(reference, verified)}
