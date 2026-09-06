"""Execution context supplied by project policy or SyncMate, never experiment YAML."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import torch
import torch_geometric

from experiments.effective_config import ConfigurationError
from scripts.syncmate.opengu_layout import modular_output_path


REPO_ROOT = Path(__file__).resolve().parents[1]
_SAFE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}')


@dataclass(frozen=True)
class ExecutionContext:
    run_id: str
    level: str
    request_device: str
    store_root: Path
    checkpoint_root: Path
    runtime_root: Path
    output: Path
    executor: str
    source_git_sha: str = None

    def __post_init__(self):
        if _SAFE_ID.fullmatch(str(self.run_id)) is None:
            raise ConfigurationError('run_id is not a safe execution identifier')
        if self.level not in ('verification', 'formal'):
            raise ConfigurationError('execution level must be verification or formal')
        if self.request_device not in ('cpu', 'cuda'):
            raise ConfigurationError('request_device must be cpu or cuda')
        if not self.executor:
            raise ConfigurationError('execution context needs an executor')
        for name in ('store_root', 'checkpoint_root', 'runtime_root', 'output'):
            object.__setattr__(self, name, Path(getattr(self, name)).expanduser().resolve())

    def receipt(self):
        cuda_name = None
        if self.request_device == 'cuda' and torch.cuda.is_available():
            cuda_name = torch.cuda.get_device_name(0)
        return {
            'run_id': self.run_id, 'level': self.level,
            'request_device': self.request_device, 'executor': self.executor,
            'source_git_sha': self.source_git_sha,
            'store_root': str(self.store_root),
            'checkpoint_root': str(self.checkpoint_root),
            'runtime_root': str(self.runtime_root), 'output': str(self.output),
            'observed_environment': {
                'torch': str(torch.__version__),
                'torch_geometric': str(torch_geometric.__version__),
                'cuda_version': torch.version.cuda,
                'cuda_device_name': cuda_name,
            },
        }


def project_context(experiment_id, *, run_id, request_device, level,
                    repository_root=REPO_ROOT):
    """Build the fixed project layout selected by a registered SyncMate job."""
    if _SAFE_ID.fullmatch(str(experiment_id)) is None:
        raise ConfigurationError('experiment_id is not safe for the project result layout')
    root = Path(repository_root).resolve()
    return ExecutionContext(
        run_id=str(run_id), level=level, request_device=request_device,
        store_root=root / 'results' / 'cache_v2',
        checkpoint_root=root / 'results' / 'runtime' / 'modular' / 'checkpoints',
        runtime_root=root / 'results' / 'runtime' / 'modular' / str(run_id),
        output=root / modular_output_path(experiment_id, str(run_id)),
        executor='syncmate-project-policy-v1',
    )


def verification_context(experiment_id, *, run_id, root):
    """An explicit disposable CPU workspace, never a formal project directory."""
    root = Path(root).expanduser()
    if not root.is_absolute() or not root.is_dir():
        raise ConfigurationError('verification root must be an existing absolute temporary directory')
    root = root.resolve()
    if root == REPO_ROOT or root in REPO_ROOT.parents or REPO_ROOT in root.parents:
        raise ConfigurationError('verification root must be outside the source checkout')
    context = project_context(experiment_id, run_id=run_id, request_device='cpu',
                              level='verification', repository_root=root)
    from dataclasses import replace
    return replace(context, executor='local-cpu-verification')


def verify_temporary_dataset(config, context):
    """Local CLI verification may read only assets inside its disposable root."""
    import json
    root = context.store_root.parent.parent
    artifacts = config['dataset']['artifacts']
    if not artifacts['manifest']:
        raise ConfigurationError('temporary dataset manifest is not bound')
    path = (Path(config['dataset_directory']) / artifacts['manifest']).resolve()
    try:
        path.relative_to(root)
        manifest = json.loads(path.read_text(encoding='utf-8'))
        (path.parent / manifest['data_path']).resolve().relative_to(root)
    except ValueError as exc:
        raise ConfigurationError('verification assets must stay inside the temporary root') from exc
