"""Independent supervised model preparation, with exact checkpoint reuse."""
from __future__ import annotations

from pathlib import Path
import sys
import torch
from cache_v2 import canonical_sha256
from experiments.c_target_v1.core import train_trajectory
from experiments.implementation_identity import implementation_fingerprint, model_functions
from utils.target_checkpoint import data_identity, capture_state, load_weights, load_cached_weights, save_cached_weights


def runtime_defaults():
    from parameter_parser import parameter_parser
    previous = sys.argv
    try:
        sys.argv = ['modular-runtime']
        args = parameter_parser()
        # Import-time CLI belongs to this process's already parsed entry.
        import config
    finally:
        sys.argv = previous
    return args


def create_model(model_config, dataset_name, data, device):
    args = runtime_defaults()
    args.update(dataset_name=dataset_name, downstream_task='node', unlearning_methods='GIF',
                gcn_num_layers=model_config['layers'], gcn_hidden=model_config['hidden_channels'])
    if model_config['architecture'] == 'OpenGU.GCNNet':
        from model.base_gnn.gcn import GCNNet
        args['base_model'] = 'GCN'
        model = GCNNet(args, data.x.shape[1], int(data.y.max()) + 1)
    elif model_config['architecture'] == 'OpenGU.SGCNet':
        from model.base_gnn.sgc import SGCNet
        args['base_model'] = 'SGC'
        model = SGCNet(args, data.x.shape[1], int(data.y.max()) + 1, num_layers=model_config['layers'])
    elif model_config['architecture'] == 'OpenGU.GATNet':
        from model.base_gnn.gat import GATNet
        args['base_model'] = 'GAT'
        model = GATNet(args, data.x.shape[1], int(data.y.max()) + 1,
                       num_layers=model_config['layers'], dropout=model_config['dropout'])
    elif model_config['architecture'] == 'OpenGU.GINNet':
        from model.base_gnn.gin import GINNet
        args['base_model'] = 'GIN'
        model = GINNet(args, data.x.shape[1], int(data.y.max()) + 1, num_layers=model_config['layers'])
    else:
        raise ValueError('unsupported model architecture: ' + model_config['architecture'])
    return model.to(device)


def train_supervised(model, data, training, checkpoint_epochs):
    return train_trajectory(model, data, checkpoint_epochs=checkpoint_epochs,
        epochs=training['epochs'], lr=training['lr'], weight_decay=training['weight_decay'],
        milestones=(), gamma=1.0, optimizer_name=training['optimizer'])


def training_metadata(model, instance, data):
    return {'format': 'pure-state-dict-v1', 'data_identity': data_identity(data), 'model': instance['model'], 'training': instance['training'],
            'numerics': numerical_environment(data),
            'implementation': implementation_fingerprint(*model_functions(model), train_supervised)}


def prepare_model(instance, *, data, dataset_name, checkpoint_root, device, reference_directory):
    from attack.cache_identity import seeded_execution
    model_config, training = instance['model'], instance['training']
    with seeded_execution(training['seed']):
        model = create_model(model_config, dataset_name, data, device)
    if instance.get('checkpoint') is not None:
        path = (Path(reference_directory) / instance['checkpoint']).resolve()
        loaded = load_weights(path, model)
        return model, [], {**{key: loaded[key] for key in ('path', 'file_sha256', 'state_hash')},
            'hit': False, 'source': 'external_state_dict',
            'effective_identity': {'data_identity': data_identity(data), 'model': model_config,
                'execution_seed': training['seed'], 'numerics': numerical_environment(data),
                'implementation': implementation_fingerprint(*model_functions(model))}}
    if instance.get('kind') == 'selector' and instance['method'].startswith('tracin_cp_'):
        from experiments.model_trajectory import prepare_trajectory
        return prepare_trajectory(model, instance, data, checkpoint_root)
    metadata = training_metadata(model, instance, data)
    path = Path(checkpoint_root) / (canonical_sha256(metadata) + '.pt')
    hit = path.exists()
    if not hit:
        with seeded_execution(training['seed']):
            train_supervised(model, data, training, ())
        save_cached_weights(path, capture_state(model), metadata)
    loaded = load_cached_weights(path, metadata, model)
    return model, [], {**{key: loaded[key] for key in ('path', 'file_sha256', 'state_hash')},
        'hit': hit, 'source': 'training_cache', 'effective_identity': metadata}


def numerical_environment(data):
    """Numerical semantics used by computation identities, excluding placement."""
    return {'dtype': str(data.x.dtype)}
