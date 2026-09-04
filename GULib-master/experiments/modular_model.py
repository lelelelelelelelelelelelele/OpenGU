"""Independent supervised model preparation, with exact checkpoint reuse."""
from __future__ import annotations

from pathlib import Path
import sys
import torch
import torch_geometric
from cache_v2 import canonical_sha256
from experiments.c_target_v1.core import train_trajectory
from experiments.implementation_identity import implementation_fingerprint, model_functions
from utils.target_checkpoint import data_identity, capture_state, load_target_checkpoint, save_target_checkpoint


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
    else:
        from model.base_gnn.sgc import SGCNet
        args['base_model'] = 'SGC'
        model = SGCNet(args, data.x.shape[1], int(data.y.max()) + 1, num_layers=model_config['layers'])
    return model.to(device)


def train_supervised(model, data, training, checkpoint_epochs):
    return train_trajectory(model, data, checkpoint_epochs=checkpoint_epochs,
        epochs=training['epochs'], lr=training['lr'], weight_decay=training['weight_decay'],
        milestones=(), gamma=1.0, optimizer_name=training['optimizer'])


def prepare_model(instance, *, data, dataset_name, runtime_root, device, reference_directory):
    from attack.cache_identity import seeded_execution
    model_config, training = instance['model'], instance['training']
    with seeded_execution(training['seed']):
        model = create_model(model_config, dataset_name, data, device)
    metadata = {'data_identity': data_identity(data), 'model': model_config, 'training': training,
                'numerics': numerical_environment(data),
                'implementation': implementation_fingerprint(*model_functions(model), train_supervised)}
    checkpoint = instance.get('checkpoint')
    if checkpoint:
        from experiments.effective_config import fields
        fields(checkpoint, {'path', 'file_sha256', 'state_hash'}, {'path', 'file_sha256', 'state_hash'}, 'checkpoint')
        path = (Path(reference_directory) / checkpoint['path']).resolve()
        loaded = load_target_checkpoint(path, expected_file_sha256=checkpoint['file_sha256'],
            expected_state_hash=checkpoint['state_hash'], expected_metadata=metadata)
        hit = True
    else:
        identity = canonical_sha256(metadata)
        path = Path(runtime_root) / 'checkpoints' / (identity + '.pt')
        if path.exists():
            loaded = load_target_checkpoint(path, expected_metadata=metadata)
            hit = True
        else:
            # Capture every epoch once. A selector's view selects only its actual
            # dependencies; asking for another view does not change training.
            with seeded_execution(training['seed']):
                checkpoints, _ = train_supervised(model, data, training, tuple(range(1, training['epochs'] + 1)))
            save_target_checkpoint(path, state_dict=capture_state(model), metadata=metadata, checkpoints=checkpoints)
            loaded = load_target_checkpoint(path, expected_metadata=metadata)
            hit = False
    model.load_state_dict(loaded['state_dict'], strict=True)
    return model, loaded['checkpoints'], {'path': str(path), 'file_sha256': loaded['file_sha256'],
        'state_hash': loaded['state_hash'], 'hit': hit, 'effective_identity': metadata}


def numerical_environment(data):
    return {'dtype': str(data.x.dtype), 'device_type': data.x.device.type,
            'torch': str(torch.__version__), 'torch_geometric': str(torch_geometric.__version__),
            'cuda_version': torch.version.cuda if data.x.device.type == 'cuda' else None}
