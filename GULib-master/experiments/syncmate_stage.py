"""Project policy around the same ordinary experiment parser and execution kernel."""
from pathlib import Path
import json
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]


def preflight(recipe_id, root=ROOT):
    import torch
    from scripts.syncmate.opengu_recipes import recipe_definitions
    from experiments.modular_config import load_experiment, configuration_fingerprint
    from experiments.modular_run import execute, read_dataset
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    from syncmate_core.identity import sha256_recipe_config
    definition = recipe_definitions()[recipe_id]
    if definition.get('preflight_profile') != 'modular-project-v1':
        raise ValueError('recipe is not an ordinary experiment')
    root = Path(root).resolve()
    errors = []
    path = root / definition['config_path']
    if sha256_recipe_config(path) != definition['config_sha256']:
        errors.append('experiment YAML fingerprint changed')
    if configuration_fingerprint(path) != definition['configuration_fingerprint']:
        errors.append('referenced configuration fingerprint changed')
    plan = execute(path, dry_run=True)
    if plan['logical_cells'] != definition['logical_cells']:
        errors.append('expanded conditions differ from registration')
    if root != Path('/autodl-fs/data/OpenGU/GULib-master'):
        errors.append('formal stage requires the canonical SSH active checkout')
    dependency = verify_core_dependency()
    errors.extend(dependency['errors'])
    gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    if gpu != 'NVIDIA GeForce RTX 4090':
        errors.append('registered RTX 4090 unavailable; no CPU fallback')
    for relative in definition['expected_artifact_paths']:
        if (root / relative).exists():
            errors.append('registered output already exists; no implicit retry or overwrite')
            break
    data_info = None
    if not errors:
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
        shas = git('rev-parse', 'HEAD', 'main', 'origin/main').splitlines()
        if git('branch', '--show-current') != 'main' or len(set(shas)) != 1 or git('status', '--porcelain', '--untracked-files=no'):
            errors.append('formal stage requires clean main = origin/main = HEAD')
        config = load_experiment(path)
        manifest = (Path(config['dataset_directory']) / config['dataset']['artifacts']['manifest']).resolve()
        try:
            canonical = root / 'data/processed'
            manifest.relative_to(canonical)
            payload = json.loads(manifest.read_text(encoding='utf-8'))
            (manifest.parent / payload['data_path']).resolve().relative_to(canonical)
        except (ValueError, OSError) as exc:
            errors.append('dataset must bind existing canonical processed assets: ' + str(exc))
        if not errors:
            data, inputs = read_dataset(config['dataset'], config['dataset_directory'])
            data_info = {'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count}
            if data_info != definition['expected_dataset']:
                errors.append('actual dataset/candidate count differs from registration')
    return {'ready': not errors, 'errors': errors, 'gpu': gpu, 'dependency': dependency,
            'dataset': data_info, 'configuration_fingerprint': plan['configuration_fingerprint']}


def run(recipe_id, root=ROOT):
    from scripts.syncmate.opengu_recipes import recipe_definitions
    from experiments.modular_execution import project_context
    from experiments.modular_run import execute
    from syncmate_core.run_handoff import build_execution_contract
    root = Path(root).resolve()
    definition = recipe_definitions()[recipe_id]
    checked = preflight(recipe_id, root=root)
    if not checked['ready']:
        return {'passed': False, 'preflight': checked, 'generated_artifacts': []}
    jobs = [yaml.safe_load(p.read_text(encoding='utf-8')) for p in
            (root / '.syncmate/runner_queue/running').glob('*.yaml')]
    matching = [j for j in jobs if j.get('recipe') == recipe_id]
    if len(matching) != 1:
        raise RuntimeError('stage requires exactly one matching running queue job')
    job = matching[0]
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    if job['expected_git_sha'] != sha:
        raise RuntimeError('running queue job source identity changed')
    expected = build_execution_contract(definition, project='opengu', job_id=job['id'], git_sha=sha)
    receipt = json.loads((root / '.syncmate/runner_queue/receipts' / (job['id'] + '.json')).read_text(encoding='utf-8'))
    if receipt.get('output_contract') != expected:
        raise RuntimeError('runner output contract differs from registration')
    identity = definition['run_identity']
    context = project_context(identity['experiment_id'], run_id=identity['run_id'],
        request_device='cuda', level='formal', repository_root=root)
    from dataclasses import replace
    context = replace(context, source_git_sha=sha)
    summary = execute(root / definition['config_path'], context=context)
    if summary['logical_cells'] != definition['logical_cells']:
        raise RuntimeError('executed conditions differ from registration')
    actual = [context.output.relative_to(root).as_posix()]
    actual += [(context.output.parent / item['path']).relative_to(root).as_posix()
               for row in summary['unlearning'] for item in row['collected_artifacts'].values()]
    if sorted(actual) != sorted(expected['artifact_paths']) or any(not (root / p).is_file() for p in actual):
        raise RuntimeError('produced artifacts differ from the exact output contract')
    return {'passed': True, 'generated_artifacts': actual, 'queue_job_id': job['id'],
            'git_sha': sha, 'run_id': identity['run_id'], 'preflight': checked,
            'scientific_acceptance': 'not_evaluated'}
