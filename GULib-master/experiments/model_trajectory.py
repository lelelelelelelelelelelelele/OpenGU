"""Selector-owned trajectory cache; ordinary GU never reads these epoch states."""
from pathlib import Path
import math
import torch
from cache_v2 import canonical_sha256
from utils.target_checkpoint import capture_state, state_hash
from experiments.modular_model import training_metadata, train_supervised
from experiments.implementation_identity import implementation_fingerprint
from attack.cache_identity import seeded_execution


def trajectory_steps(instance):
    epochs = instance['training']['epochs']
    params = instance['parameters']
    steps = params['checkpoint_steps'] or list(range(1, epochs + 1))
    if any(step > epochs for step in steps) or len(steps) < 3:
        raise ValueError('trajectory checkpoint steps must fit training epochs and contain at least three steps')
    if params['checkpoint_view'] == 'cp3' and not params['checkpoint_steps']:
        steps = [steps[0], steps[len(steps) // 2], steps[-1]]
    elif params['checkpoint_view'] == 'cp_all' and len(steps) != 6:
        raise ValueError('TracIn _6 requires exactly six checkpoint steps')
    return steps


def prepare_trajectory(model, instance, data, checkpoint_root):
    steps = trajectory_steps(instance)
    metadata = {**training_metadata(model, instance, data), 'steps': steps,
                'trajectory_implementation': implementation_fingerprint(trajectory_steps, prepare_trajectory)}
    path = Path(checkpoint_root) / 'selector-trajectories' / (canonical_sha256(metadata) + '.pt')
    hit = path.exists()
    if not hit:
        with seeded_execution(instance['training']['seed']):
            checkpoints, _ = train_supervised(model, data, instance['training'], tuple(steps))
        payload = {'metadata': metadata, 'checkpoints': checkpoints, 'final_state': capture_state(model), 'final_state_hash': state_hash(model.state_dict())}
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            torch.save(payload, stream)
    payload = torch.load(path, map_location='cpu', weights_only=True)
    if payload['metadata'] != metadata or [c['global_step'] for c in payload['checkpoints']] != steps:
        raise ValueError('selector trajectory identity mismatch')
    expected = model.state_dict()
    for state in [payload['final_state']] + [c['state'] for c in payload['checkpoints']]:
        if set(state) != set(expected) or any(v.shape != expected[k].shape or v.dtype != expected[k].dtype
                or not torch.isfinite(v).all() for k, v in state.items()):
            raise ValueError('invalid selector trajectory weights')
    for c in payload['checkpoints']:
        if c['state_hash'] != state_hash(c['state']) or not math.isfinite(c['update_lr']) or c['update_lr'] <= 0:
            raise ValueError('corrupt selector trajectory checkpoint')
    if state_hash(payload['final_state']) != payload['final_state_hash']:
        raise ValueError('corrupt final trajectory state')
    model.load_state_dict(payload['final_state'], strict=True)
    model.eval()
    from utils.target_checkpoint import sha256_file
    return model, payload['checkpoints'], {'path': str(path), 'file_sha256': sha256_file(path),
        'state_hash': state_hash(payload['final_state']), 'hit': hit, 'source': 'selector_trajectory',
        'effective_identity': metadata}
