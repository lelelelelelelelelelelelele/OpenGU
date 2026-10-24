"""Explicit Ret-only numerical policy and four fixed training interventions."""
import os
import platform
import subprocess

import torch
import torch_geometric

from experiments.effective_config import ConfigurationError, fields, choice

ARMS = ('joint', 'supervision_only', 'topology_only', 'none')
DETERMINISTIC = 'ret-deterministic-v1'
OBSERVED = 'ret-observed-v1'
_configured = None


def reference_cell(source, spec, arm):
    from cache_v2 import canonical_sha256
    conditions = {**source['conditions'], 'reference_policy':spec['policy'],
                  'reference_arm':arm, 'reference_mode':spec['mode']}
    cell_id = canonical_sha256(conditions)[:20]
    return dict(cell_id=cell_id, conditions=conditions,
                path=source['path'].replace(source['cell_id'],cell_id))


def resolve_reference(value, *, source=False):
    allowed = {'policy', 'arms', 'mode'} if source else {'policy', 'arm'}
    fields(value, allowed, allowed, 'Ret reference')
    result = dict(value)
    choice(result['policy'], (DETERMINISTIC, OBSERVED), 'Ret reference policy')
    if source:
        choice(result['mode'], ('reference', 'probe'), 'Ret reference mode')
        arms = result['arms']
        if not isinstance(arms, list) or not arms or len(set(arms)) != len(arms) or set(arms)-set(ARMS):
            raise ConfigurationError('Ret reference arms must be a nonempty unique fixed-arm list')
        if result['mode'] == 'probe' and arms != ['joint']:
            raise ConfigurationError('Ret reproducibility probe uses only joint')
    else:
        choice(result['arm'], ARMS, 'Ret reference arm')
    if result['policy'] == OBSERVED and (not source or result['mode'] != 'probe'):
        raise ConfigurationError('observed numerical settings belong only to the explicit probe')
    return result


def configure_for_experiment(config):
    """Called before native/device context can initialize CUDA; never downgrade."""
    global _configured
    specs = ([config['ret_reference']] if 'ret_reference' in config else
             [item['reference'] for item in config.get('unlearnings', []) if 'reference' in item])
    if not specs:
        return
    policies = {item['policy'] for item in specs}
    if len(policies) != 1:
        raise ConfigurationError('one Ret invocation needs one numerical policy')
    policy = next(iter(policies))
    if _configured == policy:
        if policy == DETERMINISTIC:
            verify_deterministic()
        return
    if _configured is not None or torch.cuda.is_initialized():
        raise ConfigurationError('Ret policy must be selected before CUDA initialization in a fresh process')
    if policy == DETERMINISTIC:
        workspace = os.environ.get('CUBLAS_WORKSPACE_CONFIG')
        if workspace not in (None, ':4096:8'):
            raise ConfigurationError('Ret policy conflicts with CUBLAS_WORKSPACE_CONFIG')
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
        torch.use_deterministic_algorithms(True, warn_only=False)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        verify_deterministic()
    elif policy != OBSERVED:
        raise ConfigurationError('unknown Ret numerical policy')
    _configured = policy


def backend_settings():
    return dict(deterministic_algorithms=torch.are_deterministic_algorithms_enabled(),
        deterministic_warn_only=torch.is_deterministic_algorithms_warn_only_enabled(),
        cudnn_deterministic=torch.backends.cudnn.deterministic,
        cudnn_benchmark=torch.backends.cudnn.benchmark,
        matmul_tf32=torch.backends.cuda.matmul.allow_tf32,
        cudnn_tf32=torch.backends.cudnn.allow_tf32,
        cublas_workspace_config=os.environ.get('CUBLAS_WORKSPACE_CONFIG'))


def verify_deterministic():
    expected = dict(deterministic_algorithms=True, deterministic_warn_only=False,
        cudnn_deterministic=True, cudnn_benchmark=False, matmul_tf32=False,
        cudnn_tf32=False, cublas_workspace_config=':4096:8')
    if backend_settings() != expected:
        raise ConfigurationError('Ret deterministic backend readback mismatch')


def environment(policy, device, dtype):
    if _configured != policy:
        raise ConfigurationError('Ret numerical policy was not initialized at the execution boundary')
    if policy == DETERMINISTIC:
        verify_deterministic()
    device = torch.device(device)
    gpu, driver = None, None
    if device.type == 'cuda':
        gpu = torch.cuda.get_device_name(device)
        try:
            driver = subprocess.check_output(['nvidia-smi', '--query-gpu=driver_version',
                '--format=csv,noheader'], text=True, timeout=5).strip().splitlines()
        except (OSError, subprocess.SubprocessError):
            driver = None  # Unavailable is recorded, never replaced with a guessed value.
    return dict(policy=policy, backend=backend_settings(), python=platform.python_version(),
        torch=str(torch.__version__), torch_geometric=str(torch_geometric.__version__),
        cuda_version=torch.version.cuda, device=str(device), gpu=gpu,
        driver_versions=driver, driver_status='observed' if driver else 'unavailable' if gpu else 'not_applicable',
        dtype=str(dtype), cpu_threads=torch.get_num_threads(),
        configured_before_cuda=True)


def training_graph(original, nodes, arm):
    from experiments.node_deletion import retained_graph
    choice(arm, ARMS, 'Ret reference arm')
    retained = retained_graph(original, nodes)
    result = original.clone()
    if arm in ('joint', 'supervision_only'):
        result.train_mask = retained.train_mask.clone()
    if arm in ('joint', 'topology_only'):
        result.edge_index = retained.edge_index.clone()
    for name in ('train', 'val', 'test'):
        setattr(result, name+'_indices', getattr(result, name+'_mask').nonzero().flatten().cpu().numpy())
    return result, retained
