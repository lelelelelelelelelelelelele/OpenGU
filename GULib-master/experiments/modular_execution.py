"""Execution context supplied by project policy or SyncMate, never experiment YAML."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import torch
import torch_geometric

from experiments.effective_config import ConfigurationError


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
        output=root / 'results' / 'runs' / 'modular' / str(experiment_id)
               / str(run_id) / 'summary.json',
        executor='syncmate-project-policy-v1',
    )
