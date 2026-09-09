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


def run_graphrevoker_unlearning(instance, *, selection, model, data, dataset_name, checkpoint,
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
    ensemble, preparation = prepare_graphrevoker_ensemble(instance, data,
        Path(store_root).parent / 'runtime' / 'modular' / 'checkpoints')
    target = {'method': instance['method'], 'parameters': instance['parameters'],
              'checkpoint_state_hash': checkpoint['state_hash'], 'initialization': 'independent-shard-training',
              'ensemble_state_hash': preparation['state_hash']}
    producer = graphrevoker_producer(instance['model'])
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
            ensemble, method_before, seconds = run_graphrevoker(instance, data, list(selection.selected_nodes), ensemble)
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



def graphrevoker_producer(model_config):
    from cache_v2 import ProducerVersion
    from experiments.implementation_identity import implementation_fingerprint
    from experiments.modular_shards import ShardEnsemble, train_shard
    from experiments.modular_model import create_model, train_supervised, runtime_defaults
    from experiments.node_deletion import retained_graph, pairing_identity
    runtime_defaults()
    if model_config['architecture'] == 'OpenGU.GCNNet':
        from model.base_gnn.gcn import GCNNet as model_class
    else:
        from model.base_gnn.sgc import SGCNet as model_class
    return ProducerVersion('opengu-independent-graphrevoker-output-v1', implementation_fingerprint(
        *graphrevoker_implementation_functions(), run_graphrevoker_unlearning,
        ShardEnsemble, train_shard, create_model, train_supervised, model_class,
        retained_graph, pairing_identity))


def restore_graphrevoker(payload):
    from types import SimpleNamespace
    from experiments.modular_model import create_model
    from experiments.modular_shards import ShardEnsemble
    from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition_gpa import Partitioner
    config = payload.identity['pairing']['model']
    params = payload.identity['target']['parameters']
    data = SimpleNamespace(x=torch.tensor(payload.arrays['x']), y=torch.tensor(payload.arrays['y']))
    state = {key: torch.tensor(value) for key, value in payload.state.items()}
    models = [create_model(config, 'shard', data, torch.device('cpu')) for _ in state['weights']]
    ensemble = ShardEnsemble(models, state['assignment'], state['weights'])
    ensemble.partition_encoder = create_model(config, 'graphrevoker', data, torch.device('cpu'))
    ensemble.partitioner = Partitioner(int(data.y.max()) + 1, params['gpa_hidden_channels'], params['num_shards'])
    ensemble.load_state_dict(state, strict=True)
    return ensemble.eval()
