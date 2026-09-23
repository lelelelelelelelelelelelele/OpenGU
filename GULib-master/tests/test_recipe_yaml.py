"""Declarative recipes preserve Core's immutable job and hash contracts."""
import copy
import json
from pathlib import Path

import pytest
import yaml
from scripts.syncmate.opengu_recipes import (
    ROOT, RECIPE_DIRECTORY, assemble, generate, load_declaration, recipe_ids, resolve_recipe)
from syncmate_core.contracts import build_job_envelope, ContractError
from syncmate_core.recipes import execution_recipe
from test_syncmate_execution_contract import workspace, tables, commit, git


def test_all_recipes_are_independent_and_compact():
    paths = list((ROOT / RECIPE_DIRECTORY).glob('*.yaml'))
    assert len(paths) == len(recipe_ids(ROOT)) == 47
    for path in paths:
        spec = load_declaration(path)
        definition = resolve_recipe(ROOT, spec['id'])
        assert path.stem == spec['id']
        assert 'expected_artifact_paths' not in spec
        assert 'argv' not in spec
        if spec['runner'] == 'experiment':
            assert definition['argv'][1] == 'experiments/run.py'
            assert len(spec['outputs']['files']) == 4


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


def test_config_new_commit_creates_new_job_without_mutating_old_job(workspace):
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='new-recipe', run_id='first',
        expected_datasets=[{'num_nodes': 20, 'candidate_count': 10}], project_root=root)
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
        expected_datasets=spec['expected_datasets'], project_root=root)
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
    with context.use(root, extension=FixtureRegistration(definition)):
        with pytest.raises(SystemExit, match='main changed'):
            queue.runner_queue_submit('wrong-version', definition['id'], expected_git_sha='f'*40)
    assert not (root / 'results').exists()

def test_preview_resolves_device_and_outputs_without_submission(workspace):
    from scripts.syncmate.recipe import preview
    from syncmate_core.devices import build_peer_config
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='visible', run_id='visible-run',
        expected_datasets=[{'num_nodes': 20, 'candidate_count': 10}], project_root=root)
    path = save_spec(root, spec)
    sha = commit(root)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text())
    device['peers'] = {'cpu-runner': build_peer_config('runner', None, str(root), transport='local')}
    device_file.write_text(yaml.safe_dump(device))
    before = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    view = preview('visible', 'cpu-runner', device_file, root)
    assert view['commit'] == sha and view['submitted'] is False
    assert view['config_path'] == 'experiment.yaml'
    assert view['remote_workdir'] == str(root)
    assert view['remote_result_roots'] == ['results/runs/contract/visible-run']
    assert view['local_receiving_root'] == str(root / 'results/runs/cpu-runner')
    assert view['argv'][1:] == ['experiments/run.py', 'experiment.yaml', '--run-id', 'visible-run']
    assert view['expected_artifact_count'] == len(assemble(load_declaration(path), root)['expected_artifact_paths'])
    assert view['remote_checks'].startswith('NOT OBSERVED')
    assert not view['local_checks_passed']  # disposable repo has no origin
    assert before == {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
