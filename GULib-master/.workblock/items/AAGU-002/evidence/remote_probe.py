"""AAGU-002 reviewed read-only pilot; send on stdin to the fixed SSH target.

No queue submission, training, dataset materialization, or artifact writes.
The missing-GPU case changes only this probe process, never device setup.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

ROOT = Path('/autodl-fs/data/OpenGU/GULib-master')
sys.dont_write_bytecode = True
os.chdir(str(ROOT))
sys.path.insert(0, str(ROOT))


def command(args):
    result = subprocess.run(args, cwd=str(ROOT), capture_output=True,
                            text=True, timeout=15)
    return {'exit_code': result.returncode, 'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()}


def queue_snapshot():
    base = ROOT / '.syncmate/runner_queue'
    files = {}
    for directory in ('inbox', 'running', 'done', 'failed', 'blocked', 'receipts'):
        for path in sorted((base / directory).glob('*')):
            if path.is_file():
                files[path.relative_to(base).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


before = queue_snapshot()
import torch
import yaml
from scripts.syncmate import syncmate  # Registers this checkout's import path.
from scripts.syncmate.verify_core_dependency import verify_core_dependency
from experiments.syncmate_atomic_stage import preflight

device = yaml.safe_load((ROOT / '.syncmate/device.yaml').read_text())
recipe = 'opengu-sm005-atomic-gpu-v1'
baseline = preflight(recipe, ROOT)
with patch.object(torch.cuda, 'is_available', return_value=False):
    negative = preflight(recipe, ROOT)
after = queue_snapshot()
print(json.dumps({
    'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'evidence_kind': 'real-ssh-read-only-observation',
    'project_path': str(ROOT.resolve()),
    'device': {key: device.get(key) for key in ('device_id', 'role', 'repo_path')},
    'gpu': {'available': torch.cuda.is_available(), 'count': torch.cuda.device_count(),
            'names': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]},
    'python': sys.version.split()[0], 'torch': torch.__version__,
    'nvidia_smi': command(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader']),
    'git_head': command(['git', 'rev-parse', 'HEAD']),
    'git_branch': command(['git', 'branch', '--show-current']),
    'git_status': command(['git', 'status', '--porcelain=v1', '--untracked-files=no']),
    'core_dependency': verify_core_dependency(),
    'recipe': recipe,
    'real_existing_recipe_preflight': baseline,
    'controlled_missing_gpu_preflight': {
        'evidence_kind': 'in-process-fault-injection-on-real-target',
        'injection': 'torch.cuda.is_available=False only inside this process',
        'result': negative},
    'queue_before': before, 'queue_after': after,
    'queue_unchanged': before == after,
    'submitted_jobs': 0,
}, ensure_ascii=False, indent=2))
