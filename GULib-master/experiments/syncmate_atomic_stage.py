"""Reviewed one-cell GPU verification, using AAGU-026's independent instances."""
from __future__ import annotations

import contextlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = 'experiments/configs/sm005_atomic/experiment.yaml'
RECIPE = 'opengu-sm005-atomic-gpu-v1'
RUN_ID = 'sm005-gpu-v1'
OUTPUT = 'results/runs/modular/sm005-cora-degree-gnndelete/sm005-gpu-v1/summary.json'


def preflight(root=ROOT):
    import torch
    from experiments.modular_config import load_experiment
    from experiments.modular_run import read_dataset
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    errors = []
    root = Path(root).resolve()
    if root != Path('/autodl-fs/data/OpenGU/GULib-master'):
        errors.append('atomic GPU stage requires the canonical SSH active checkout')
    dependency = verify_core_dependency()
    errors.extend(dependency['errors'])
    gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    if gpu != 'NVIDIA GeForce RTX 4090':
        errors.append('registered RTX 4090 is unavailable; no CPU fallback')
    config = load_experiment(root / CONFIG)
    dataset = None
    if not errors:
        data, inputs = read_dataset(config['dataset'], config['dataset_directory'])
        dataset = {'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count,
                   'split_hash': config['dataset']['artifacts']['split_hash']}
        if inputs.num_nodes != 2708 or inputs.candidate_count != 1895:
            errors.append('reviewed Cora dataset or candidate count differs')
    if (root / OUTPUT).exists():
        errors.append('atomic output already exists; inspect it, do not overwrite or retry')
    return {'ready': not errors, 'errors': errors, 'gpu': gpu,
            'dependency': dependency, 'dataset': dataset, 'level': 'verification'}


def run():
    from experiments.modular_execution import project_context
    from experiments.modular_run import execute
    checked = preflight()
    if not checked['ready']:
        return {'passed': False, 'preflight': checked, 'generated_artifacts': []}
    # The immutable recipe owns the run layout; the queue owns submission identity.
    jobs = [yaml.safe_load(p.read_text()) for p in
            (ROOT / '.syncmate/runner_queue/running').glob('*.yaml')]
    matching = [j for j in jobs if j.get('recipe') == RECIPE]
    if len(matching) != 1:
        raise RuntimeError('stage must be invoked by exactly one matching running queue job')
    job = matching[0]
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if job['expected_git_sha'] != sha:
        raise RuntimeError('running queue job source identity changed')
    context = project_context('sm005-cora-degree-gnndelete', run_id=RUN_ID,
                              request_device='cuda', level='verification', repository_root=ROOT)
    summary = execute(ROOT / CONFIG, context=context)
    if (len(summary['selectors']), len(summary['unlearning']), len(summary['evaluations'])) != (1, 1, 1):
        raise RuntimeError('atomic execution did not produce exactly one cell')
    return {'passed': True, 'generated_artifacts': [OUTPUT], 'queue_job_id': job['id'],
            'git_sha': sha, 'run_id': RUN_ID, 'preflight': checked,
            'scientific_acceptance': 'not_evaluated'}


def main():
    # Training libraries may print; reserve stdout for the executor's JSON contract.
    with contextlib.redirect_stdout(sys.stderr):
        result = run()
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
