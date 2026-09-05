"""Reviewed one-cell GPU verifications, using AAGU-026's independent instances."""
from __future__ import annotations

import contextlib
import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml
from scripts.syncmate.opengu_layout import atomic_output_path as output_path

ROOT = Path(__file__).resolve().parents[1]
PLANS = {
    'opengu-sm005-atomic-gpu-v1': {
        'config': 'experiments/configs/sm005_atomic/experiment.yaml',
        'experiment_id': 'sm005-cora-degree-gnndelete',
        'run_id': 'sm005-gpu-v1',
        'expected_counts': (1, 1, 1),
        'config_sha256': 'd954af660d61bb095ca00f987344b45b4d78870068c9d427c970d200407b43b5',
    },
    **{
        f'opengu-sm005-b-hutch32-{attempt}-v1': {
            'config': 'experiments/configs/sm005_atomic/experiment_b_hutch32.yaml',
            'experiment_id': 'sm005-cora-b-hutch32-gnndelete',
            'run_id': f'sm005-b-hutch32-{attempt}-v1',
            'expected_counts': (1, 1, 1),
            'config_sha256': 'e14d0dd8b65528d3021ca6634263d9f4b3343ba5035f9f9db37eedfed1534a26',
        }
        for attempt in ('first', 'warm')
    },
    'opengu-sm005-d-full-selector-v1': {
        'config': 'experiments/configs/sm005_atomic/experiment_d_full_selector.yaml',
        'experiment_id': 'sm005-cora-d-full-selector',
        'run_id': 'sm005-d-full-selector-v1',
        'expected_counts': (1, 0, 0),
        'config_sha256': '1a0f8a2764e4f8c772d29afed43931faa12e078edccdd51c720d8eff5f5543a2',
    },
    'opengu-sm005-d-full-return-v1': {
        'config': 'experiments/configs/sm005_atomic/experiment_d_full_selector.yaml',
        'experiment_id': 'sm005-cora-d-full-selector',
        'run_id': 'sm005-d-full-return-v1',
        'expected_counts': (1, 0, 0),
        'config_sha256': '1a0f8a2764e4f8c772d29afed43931faa12e078edccdd51c720d8eff5f5543a2',
    },
    'opengu-sm005-d-full-handoff-v1': {
        'config': 'experiments/configs/sm005_atomic/experiment_d_full_selector.yaml',
        'experiment_id': 'sm005-cora-d-full-selector',
        'run_id': 'sm005-d-full-handoff-v1',
        'expected_counts': (1, 0, 0),
        'config_sha256': '1a0f8a2764e4f8c772d29afed43931faa12e078edccdd51c720d8eff5f5543a2',
    },
}


def preflight(recipe_id, root=ROOT):
    plan = PLANS[recipe_id]
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
    config = load_experiment(root / plan['config'])
    counts = tuple(len(config[key]) for key in ('selectors', 'unlearnings', 'evaluations'))
    if counts != plan['expected_counts']:
        errors.append('configuration exceeds the reviewed Selector/GU/Evaluation counts')
    dataset = None
    if not errors:
        data, inputs = read_dataset(config['dataset'], config['dataset_directory'])
        dataset = {'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count,
                   'split_hash': config['dataset']['artifacts']['split_hash']}
        if inputs.num_nodes != 2708 or inputs.candidate_count != 1895:
            errors.append('reviewed Cora dataset or candidate count differs')
    if (root / output_path(plan)).exists():
        errors.append('atomic output already exists; inspect it, do not overwrite or retry')
    return {'ready': not errors, 'errors': errors, 'gpu': gpu,
            'dependency': dependency, 'dataset': dataset, 'level': 'verification'}


def run(recipe_id):
    plan = PLANS[recipe_id]
    from experiments.modular_execution import project_context
    from experiments.modular_run import execute
    checked = preflight(recipe_id)
    if not checked['ready']:
        return {'passed': False, 'preflight': checked, 'generated_artifacts': []}
    # The immutable recipe owns the run layout; the queue owns submission identity.
    jobs = [yaml.safe_load(p.read_text()) for p in
            (ROOT / '.syncmate/runner_queue/running').glob('*.yaml')]
    matching = [j for j in jobs if j.get('recipe') == recipe_id]
    if len(matching) != 1:
        raise RuntimeError('stage must be invoked by exactly one matching running queue job')
    job = matching[0]
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if job['expected_git_sha'] != sha:
        raise RuntimeError('running queue job source identity changed')
    from syncmate_core.run_handoff import build_execution_contract
    from scripts.syncmate.opengu_recipes import recipe_definitions
    expected = build_execution_contract(recipe_definitions()[recipe_id], project='opengu',
                                        job_id=job['id'], git_sha=sha)
    receipt = json.loads((ROOT / '.syncmate/runner_queue/receipts' / f"{job['id']}.json").read_text(encoding='utf-8'))
    contract = receipt.get('output_contract')
    if contract != expected:
        raise RuntimeError('runner output contract differs from the reviewed experiment')
    context = project_context(plan['experiment_id'], run_id=plan['run_id'],
                              request_device='cuda', level='verification', repository_root=ROOT)
    if [context.output.relative_to(ROOT).as_posix()] != contract['artifact_paths']:
        raise RuntimeError('executor output differs from the SyncMate handoff')
    summary = execute(ROOT / plan['config'], context=context)
    if tuple(len(summary[key]) for key in ('selectors', 'unlearning', 'evaluations')) != plan['expected_counts']:
        raise RuntimeError('atomic execution differs from reviewed Selector/GU/Evaluation counts')
    return {'passed': True, 'generated_artifacts': contract['artifact_paths'], 'queue_job_id': job['id'],
            'git_sha': sha, 'run_id': plan['run_id'], 'preflight': checked,
            'scientific_acceptance': 'not_evaluated'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', choices=tuple(PLANS), required=True)
    args = parser.parse_args()
    # Training libraries may print; reserve stdout for the executor's JSON contract.
    # OpenGU's config module parses process argv at import time. Stage arguments
    # belong to this entry point; downstream defaults come from the reviewed YAML.
    process_argv = sys.argv
    try:
        sys.argv = [process_argv[0]]
        with contextlib.redirect_stdout(sys.stderr):
            result = run(args.recipe)
    finally:
        sys.argv = process_argv
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
