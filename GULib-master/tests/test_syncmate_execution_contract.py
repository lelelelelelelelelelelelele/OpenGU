"""Frozen behavioral acceptance: ordinary YAML + real Core + device.yaml.

Only the reviewed recipe DATA and temporary graph are fixtures. No replacement
of preflight, device resolution, subprocess execution, queue or collection.
"""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml
from test_modular_consumers import tables, write_yaml
from experiments.modular_config import configuration_fingerprint
from experiments.modular_run import execute
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from opengu_recipes import recipe_definitions
from syncmate_core import collection, context, devices, index, queue
from syncmate_core.identity import sha256_recipe_config

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


@pytest.fixture
def workspace(tables):
    root, config, gu = tables
    # Real tracked production files in a clean disposable runner checkout.
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    for relative in filter(None, paths):
        source = ROOT / relative
        if (source.suffix != '.py' and not relative.startswith('model/properties/')) or relative.startswith('tests/') or not source.is_file():
            continue
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    (root / '.gitignore').write_text('.syncmate/\nresults/\n__pycache__/\n*.pyc\ncollector/\n')
    (root / '.syncmate').mkdir()
    write_yaml(root / '.syncmate/device.yaml', {
        'version': 1, 'device_id': 'temporary-cpu', 'role': 'runner',
        'repo_path': str(root), 'execution_device': 'cpu', 'peers': {}})
    config.update(experiment_id='contract', selector_refs=['score.yaml'],
                  seeds=[122, 722], budget_ratios=[.1, .2])
    selector = yaml.safe_load((root / 'degree.yaml').read_text())
    selector['budget'] = {'mode': 'ratio', 'value': .1}
    selector.update(method='a_grad_norm', model=gu['model'], training=gu['training'])
    write_yaml(root / 'score.yaml', selector)
    write_yaml(root / 'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {}})
    path = root / 'experiment.yaml'
    write_yaml(path, config)
    git(root, 'init', '-q', '-b', 'main')
    return root, path, config


def commit(root):
    git(root, 'add', '.')
    git(root, '-c', 'user.name=Acceptance fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-q', '--allow-empty', '-m', 'reviewed temporary CPU inputs')
    return git(root, 'rev-parse', 'HEAD')


def cli(root, path, run_id):
    return subprocess.run([sys.executable, '-B', 'experiments/run.py', str(path),
        '--run-id', run_id, '--device-config', '.syncmate/device.yaml',
        '--verification-root', str(root)], cwd=root, capture_output=True, text=True,
        encoding='utf-8', timeout=120)


def declaration(root, path, stage):
    definition = copy.deepcopy(recipe_definitions()['opengu-aagu007-v1'])
    plan = execute(path, dry_run=True)
    summary = 'results/runs/modular/contract/registered/summary.json'
    # Expected OUTPUTS are specified independently of the artifact enumerator.
    paths = [summary]
    if stage == 'unlearning':
        paths += ['results/runs/modular/contract/registered/summary.outputs/{}/{}'.format(i, name)
                  for i in range(8)
                  for name in ('attack.json', 'output-references.json', 'predictions.npz', '_meta.json')]
    definition.update(id='temporary-contract', config_path='experiment.yaml',
        config_sha256=sha256_recipe_config(path),
        configuration_fingerprint=configuration_fingerprint(path),
        logical_cells=plan['logical_cells'], stage=stage,
        expected_dataset={'num_nodes': 20, 'candidate_count': 10},
        run_identity={'experiment_id': 'contract', 'run_id': 'registered'},
        argv=['{python}', 'experiments/run.py', 'experiment.yaml', '--run-id', 'registered',
              '--device-config', '.syncmate/device.yaml', '--verification-root', str(root)],
        expected_artifact_paths=paths,
        collector_result_roots=['results/runs/modular/contract/registered'])
    return definition


class FixtureRegistration(OpenGUProjectExtension):
    def __init__(self, definition):
        self.definition = definition

    def recipes(self, project_root):
        return {self.definition['id']: self.definition}


@pytest.mark.parametrize('stage', ['selector', 'unlearning', 'metrics'])
def test_real_core_and_direct_command_share_config_device_and_outputs(workspace, stage, record_property):
    root, path, config = workspace
    if stage != 'selector':
        config.update(stage='unlearning', unlearning_refs=['gu.yaml', 'retrain.yaml'])
        write_yaml(path, config)
    if stage == 'metrics':
        seed = cli(root, path, 'producer')
        assert seed.returncode == 0, seed.stdout + seed.stderr
        previous = root / 'results/runs/modular/contract/producer/summary.json'
        write_yaml(root / 'gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
                   'case': 'post_unlearning_utility_and_retrain_gap'})
        config = {'kind': 'experiment', 'schema_version': 1, 'experiment_id': 'contract',
            'stage': 'metrics', 'dataset_ref': 'dataset.yaml', 'matrix': 'cartesian_product',
            'evaluation_refs': ['gap.yaml'], 'output_inputs': [{'summary': str(previous),
                'sha256': hashlib.sha256(previous.read_bytes()).hexdigest()}]}
        write_yaml(path, config)
    sha = commit(root)
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*.yaml')}
    direct = cli(root, path, 'direct')
    assert direct.returncode == 0, direct.stdout + direct.stderr
    direct_summary = json.loads(direct.stdout)
    definition = declaration(root, path, stage)
    with context.use(root, extension=FixtureRegistration(definition)):
        submitted = queue.runner_queue_submit('contract-job', definition['id'], expected_git_sha=sha)
        assert submitted['submitted'], submitted
        device, warnings = devices.load_device(root / '.syncmate/device.yaml')
        assert not warnings
        completed = queue.runner_queue_run_once(device)
        assert completed['status'] == 'done', completed
        assert queue.runner_queue_payload()['counts']['done'] == 1
    actual = json.loads((root / definition['expected_artifact_paths'][0]).read_text())
    assert actual['configuration_fingerprint'] == direct_summary['configuration_fingerprint']
    assert actual['data_identity'] == direct_summary['data_identity']
    receipt = actual['execution_receipt']
    assert receipt['request_device'] == 'cpu'
    assert receipt['source_git_sha'] == sha
    assert Path(receipt['runtime_root']).is_relative_to(root) if hasattr(Path, 'is_relative_to') else str(receipt['runtime_root']).startswith(str(root))
    assert receipt['observed_environment']['python_executable'] == sys.executable
    assert Path(receipt['observed_environment']['working_directory']) == root
    if stage == 'unlearning':
        assert len(actual['unlearning']) == 8
        assert [r['output'] for r in actual['unlearning']] == [r['output'] for r in direct_summary['unlearning']]
        assert all(r['hit'] and not r['producer_called'] for r in actual['unlearning'])
    elif stage == 'selector':
        assert len(actual['selectors']) == 4 and actual['unlearning'] == []
        assert all(r['score']['hit'] and r['selection']['cache']['hit'] for r in actual['selectors'])
    else:
        assert actual['selectors'] == [] and actual['unlearning'] == []
        assert len(actual['evaluations'][0]['rows']) == 4
    assert before == {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*.yaml')
                      if 'runner_queue' not in p.parts}
    collector = root / 'collector'
    collector.mkdir()
    with context.use(collector, extension=FixtureRegistration(definition)):
        peer = devices.build_peer_config('runner', None, str(root), transport='local')
        args = ('runner', devices.transport_ssh_value(peer), str(root), definition['collector_result_roots'], 'results/runs/runner')
        opts = dict(artifact_names=definition['collector_artifact_names'],
                    expected_paths=definition['expected_artifact_paths'], expected_git_sha=sha, save=True)
        applied = collection.apply_collect(*args, **opts)
        assert not applied.get('errors'), applied
        checked = collection.verify_collect(*args, **opts)
        assert checked['summary']['status'] == 'verified', checked
        assert collection.apply_collect(*args, **opts)['summary']['fetched'] == 0
        entry = index.load_artifact_index()['peers']['runner']['items'][0]
        (collector / entry['local_path']).write_bytes(b'corrupted')
        assert collection.verify_collect(*args, **opts)['summary']['status'] != 'verified'
        (collector / entry['local_path']).unlink()
        assert collection.verify_collect(*args, **opts)['summary']['status'] != 'verified'
    record_property('real_core', json.dumps({'stage': stage, 'sha': sha,
        'queue_status': completed['status'], 'declared_artifacts': len(definition['expected_artifact_paths']),
        'device': receipt, 'corrupt_and_missing_rejected': True}))


@pytest.mark.parametrize('device_value', [None, 'invalid-device', 'cuda:999'])
def test_device_configuration_controls_failure_before_production(workspace, device_value):
    root, path, _ = workspace
    device_path = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_path.read_text())
    if device_value is None:
        device.pop('execution_device')
    else:
        device['execution_device'] = device_value
    write_yaml(device_path, device)
    result = cli(root, path, 'invalid')
    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload['passed'] is False and 'device' in payload['error'].lower()
    assert not (root / 'results').exists()


def test_live_registration_invokes_ordinary_yaml_directly():
    definition = recipe_definitions()['opengu-aagu007-v1']
    assert definition['argv'][:3] == ('{python}', 'experiments/run.py', definition['config_path'])
    assert '--recipe' not in definition['argv']
    assert '--run-id' in definition['argv']
    assert configuration_fingerprint(ROOT / definition['config_path']) == definition['configuration_fingerprint']
