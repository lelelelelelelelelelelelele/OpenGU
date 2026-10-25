"""Declarative recipes preserve Core's immutable job and hash contracts."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from scripts.syncmate.opengu_recipes import (
    ROOT, RECIPE_DIRECTORY, assemble, generate, load_declaration, recipe_ids, resolve_recipe)
from syncmate_core.contracts import build_job_envelope, ContractError
from syncmate_core.recipes import execution_recipe
from test_syncmate_execution_contract import workspace, tables, commit, git, cli
from test_modular_consumers import write_yaml


def test_all_recipes_are_independent_and_compact():
    """Validate every real declaration and config, without opening run outputs."""
    from experiments.modular_config import load_experiment
    from syncmate_core.contracts import resolve_repo_path

    paths = list((ROOT / RECIPE_DIRECTORY).glob('*.yaml'))
    assert len(paths) == len(recipe_ids(ROOT)) and paths
    for path in paths:
        spec = load_declaration(path)
        assert path.stem == spec['id']
        assert 'expected_artifact_paths' not in spec
        assert 'argv' not in spec
        config_path = resolve_repo_path(ROOT, spec['config_path'])
        assert config_path.is_file(), path
        if spec['runner'] == 'experiment':
            config = load_experiment(config_path)
            assert config['experiment_id'] == spec['run_identity']['experiment_id'], path
            assert config['stage'] == spec['stage'], path
            assert len(config['datasets']) == len(spec['expected_datasets']), path
            assert len(spec['outputs']['files']) == 4


def test_registered_source_independent_recipes_resolve_reviewed_entrypoints():
    """Actual registry assembly for runners that do not consume prior results."""
    specs = [load_declaration(path) for path in (ROOT / RECIPE_DIRECTORY).glob('*.yaml')]
    independent = [spec for spec in specs if spec.get('stage') not in ('metrics', 'retrain_diagnostics')]
    assert independent
    for spec in independent:
        definition = resolve_recipe(ROOT, spec['id'])
        entry = {'experiment': 'experiments/run.py',
                 'diagnostic': 'experiments/aagu059_diagnostic.py',
                 'smoke': 'scripts/syncmate/syncmate.py',
                 'opengu-preflight-v1': 'scripts/syncmate/syncmate.py'}[spec['runner']]
        assert definition['argv'][1] == entry, spec['id']


@pytest.mark.parametrize('stage', ['metrics', 'retrain_diagnostics'])
def test_source_consuming_recipe_requires_real_verified_results(workspace, stage, record_property):
    """Real producer -> real resolver; missing or corrupt results must reject."""
    from experiments.modular_artifacts import read_run

    root, config_path, config = workspace
    config.update(stage='unlearning', selector_refs=['degree.yaml'],
                  unlearning_refs=['retrain.yaml'], seeds=[122])
    config.pop('budget_ratios')  # degree.yaml declares a fixed-k budget.
    write_yaml(config_path, config)
    commit(root)
    produced = cli(root, config_path, 'source')
    assert produced.returncode == 0, produced.stdout + produced.stderr
    source_path = root / 'results/runs/contract/source/run.json'
    source_bytes = source_path.read_bytes()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    run, _ = read_run(source_path, source_sha)
    assert len(run['cells']) == 1 and run['cells'][0]['output']
    source = {'run': source_path.relative_to(root).as_posix(), 'sha256': source_sha}
    dependent = {'kind': 'experiment', 'schema_version': 1, 'experiment_id': 'contract',
                 'stage': stage, 'dataset_refs': ['dataset.yaml'],
                 'matrix': 'cartesian_product', 'output_inputs': [source]}
    if stage == 'metrics':
        dependent['evaluation_refs'] = ['utility.yaml']
    else:
        source['cell_ids'] = [run['cells'][0]['cell_id']]
    write_yaml(root / 'dependent.yaml', dependent)
    spec = generate('dependent.yaml', recipe_id='dependent', run_id='consumer', project_root=root)
    save_spec(root, spec)
    definition = resolve_recipe(root, 'dependent')
    assert definition['argv'][1] == 'experiments/run.py'
    assert definition['expected_cells'] == [
        {key: run['cells'][0][key] for key in ('cell_id', 'path', 'conditions')}]
    assert len(definition['expected_artifact_paths']) == (3 if stage == 'metrics' else 5)

    source_path.unlink()
    with pytest.raises(FileNotFoundError):
        resolve_recipe(root, 'dependent')
    source_path.write_bytes(source_bytes + b'\n')
    with pytest.raises(ValueError, match='run checksum mismatch'):
        resolve_recipe(root, 'dependent')
    source_path.write_bytes(source_bytes)

    cell_path = source_path.parent / run['cells'][0]['path'] / 'selection.json'
    cell_bytes = cell_path.read_bytes()
    cell_path.write_bytes(cell_bytes + b'\n')
    with pytest.raises(ValueError, match='checksum mismatch'):
        resolve_recipe(root, 'dependent')
    cell_path.write_bytes(cell_bytes)
    assert resolve_recipe(root, 'dependent') == definition
    record_property('real_source_recipe', json.dumps({
        'stage': stage, 'producer': produced.args, 'source_sha256': source_sha,
        'source_cells': len(run['cells']),
        'expected_artifacts': len(definition['expected_artifact_paths']),
        'missing_run_rejected': True, 'changed_run_rejected': True,
        'changed_cell_rejected': True, 'restored_source_resolves': True}))


@pytest.mark.parametrize('change', [
    lambda s: s.update(argv=['arbitrary']),
    lambda s: s.update(schema_version=2),
    lambda s: s.update(config_path='../outside.yaml'),
    lambda s: s['outputs'].update(root='results/custom'),
    lambda s: s['outputs'].update(files=['run.json', 'cells/exact/metrics.json']),
    lambda s: s['run_identity'].update(run_id='../escape'),
])
def test_invalid_or_unimplemented_declarations_fail_closed(tmp_path, change):
    spec = load_declaration(ROOT / RECIPE_DIRECTORY / 'opengu-aagu007-v2.yaml')
    change(spec)
    path = tmp_path / 'recipe.yaml'
    path.write_text(yaml.safe_dump(spec))
    with pytest.raises(ValueError):
        assemble(load_declaration(path))


def test_duplicate_yaml_keys_rejected(tmp_path):
    path = tmp_path / 'recipe.yaml'
    path.write_text('id: one\nid: two\n')
    with pytest.raises(ValueError, match='duplicate'):
        load_declaration(path)


def save_spec(root, spec):
    path = root / RECIPE_DIRECTORY / (spec['id'] + '.yaml')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(spec, sort_keys=False))
    return path


def test_generator_writes_yaml_from_configured_runner_and_never_overwrites(workspace):
    from syncmate_core.devices import build_peer_config
    root, config, _ = workspace
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text())
    device['peers'] = {'cpu': build_peer_config('runner', None, str(root), transport='local')}
    device_file.write_text(yaml.safe_dump(device))
    output = root / RECIPE_DIRECTORY / 'generated.yaml'
    command = [sys.executable, '-B', str(root / 'scripts/syncmate/recipe.py'), 'generate',
        config.relative_to(root).as_posix(), '--id', 'generated', '--run-id', 'automatic', '--node', 'cpu',
        '--output', str(output)]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    spec = load_declaration(output)
    assert spec['expected_datasets'] == [{'num_nodes': 20, 'candidate_count': 10}]
    before = output.read_bytes()
    repeat = subprocess.run(command, cwd=root, capture_output=True, text=True)
    assert repeat.returncode != 0
    assert output.read_bytes() == before


def test_generator_refuses_missing_or_changed_bound_graph(workspace):
    root, _, _ = workspace
    graph = root / 'data/processed/graph.pkl'
    graph.write_bytes(graph.read_bytes() + b'changed')
    with pytest.raises(ValueError, match='digest mismatch'):
        generate('experiment.yaml', recipe_id='invalid', run_id='invalid', project_root=root)
    graph.unlink()
    with pytest.raises(OSError):
        generate('experiment.yaml', recipe_id='missing', run_id='missing', project_root=root)


def test_config_new_commit_creates_new_job_without_mutating_old_job(workspace):
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='new-recipe', run_id='first',
        project_root=root)
    assert spec['expected_datasets'] == [{'num_nodes': 20, 'candidate_count': 10}]
    path = save_spec(root, spec)
    sha1 = commit(root)
    recipe = execution_recipe(assemble(load_declaration(path), root))
    old_job = dict(build_job_envelope(recipe, root, job_id='first-job', git_state={'clean': True, 'sha': sha1}))
    old_bytes = json.dumps(old_job, sort_keys=True)
    config.write_text(config.read_text() + '\n# deliberate versioned change\n')
    # Re-read does not silently refresh reviewed hashes.
    assert load_declaration(path)['config_sha256'] == spec['config_sha256']
    with pytest.raises(ContractError, match='SHA-256 mismatch'):
        build_job_envelope(recipe, root, job_id='stale', git_state={'clean': True, 'sha': sha1})
    with pytest.raises(ContractError, match='dirty'):
        build_job_envelope(recipe, root, job_id='dirty', git_state={'clean': False, 'sha': sha1})
    new_spec = generate('experiment.yaml', recipe_id='new-recipe', run_id='second',
        project_root=root)
    save_spec(root, new_spec)
    sha2 = commit(root)
    new_recipe = execution_recipe(assemble(load_declaration(path), root))
    new_job = dict(build_job_envelope(new_recipe, root, job_id='second-job', git_state={'clean': True, 'sha': sha2}))
    assert sha1 != sha2 and old_job['expected_config_sha256'] != new_job['expected_config_sha256']
    assert old_bytes == json.dumps(old_job, sort_keys=True)
    assert old_job['expected_git_sha'] == sha1 and new_job['expected_git_sha'] == sha2
    assert recipe.expected_artifact_paths != new_recipe.expected_artifact_paths


def test_stale_git_version_rejected_by_real_core(workspace):
    from syncmate_core import context, queue, devices
    from test_syncmate_execution_contract import declaration, FixtureRegistration
    root, config, _ = workspace
    definition = declaration(root, config, 'selector')
    sha = commit(root)
    with context.use(root, extension=FixtureRegistration(definition), node_id='runner'):
        with pytest.raises(SystemExit, match='commit|revision|source|Git'):
            queue.runner_queue_submit('wrong-version', definition['id'], expected_git_sha='f'*40)
    assert not (root / 'results').exists()

def test_preview_resolves_device_and_outputs_without_submission(workspace):
    from scripts.syncmate.recipe import preview
    from syncmate_core.devices import build_peer_config
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='visible', run_id='visible-run',
        project_root=root)
    path = save_spec(root, spec)
    with (root / '.gitignore').open('a', encoding='utf-8') as handle:
        handle.write('data/\n')
    sha = commit(root)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text())
    device['peers'] = {'gpu4090-2': build_peer_config('runner', 'autodl-opengu-2', '/autodl-fs/data/OpenGU/GULib-master', python_executable='/root/miniconda3/bin/python')}
    device_file.write_text(yaml.safe_dump(device))
    before = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    view = preview('visible', 'gpu4090-2', device_file, root)
    assert view['commit'] == sha and view['submitted'] is False
    assert view['config_path'] == 'experiment.yaml'
    assert view['remote_workdir'] == '/autodl-fs/data/OpenGU/GULib-master'
    assert view['remote_result_roots'] == ['results/runs/contract/visible-run']
    assert view['local_receiving_root'] == str(root / 'results/runs/gpu4090-2')
    assert view['argv'][1:] == ['experiments/run.py', 'experiment.yaml', '--run-id', 'visible-run', '--syncmate', '--node-id', 'gpu4090-2']
    assert view['expected_artifact_count'] == len(assemble(load_declaration(path), root)['expected_artifact_paths'])
    assert view['remote_checks'].startswith('NOT OBSERVED')
    assert view['local_checks_passed'] and view['errors'] == []
    assert view['runtime_preflight'] == 'deferred until exact checkout and execution lease'
    assert before == {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
