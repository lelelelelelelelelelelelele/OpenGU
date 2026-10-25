"""Installed private preview/admission boundary; no SSH or production access."""
import json
import subprocess
import sys
import pytest
import yaml
from local_transport_guard import local_only_transport
from scripts.syncmate.deployment_policy import deployment_policy
from scripts.syncmate.opengu_recipes import generate
from scripts.syncmate.recipe import preview
from test_syncmate_execution_contract import workspace, tables, commit
from test_recipe_yaml import save_spec


def setup_controller(workspace):
    root, config, _ = workspace
    with (root / '.gitignore').open('a', encoding='utf-8') as handle:
        handle.write('data/\n')
    save_spec(root, generate('experiment.yaml', recipe_id='private-check', run_id='private-run', project_root=root))
    sha = commit(root)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    policy = deployment_policy(root)
    device.update(role='collector', peers={node: {'role': 'runner', 'transport': 'ssh',
        'python_executable': sys.executable, **target} for node, target in policy['targets'].items()})
    device_file.write_text(yaml.safe_dump(device), encoding='utf-8')
    return root, sha, device_file


@pytest.mark.parametrize('node', ['gpu4090', 'gpu4090-2'])
def test_preview_selects_frozen_node_without_receipt_or_remote_contact(workspace, node):
    root, sha, device = setup_controller(workspace)
    (root / 'paper.md').write_text('uncommitted manuscript', encoding='utf-8')
    (root / 'experiment.yaml').write_text('invalid current YAML', encoding='utf-8')
    receipt = root / '.workblock/runtime/install' / node / sha / 'receipt.json'
    receipt.parent.mkdir(parents=True)
    receipt.write_text('obsolete receipt', encoding='utf-8')
    view = preview('private-check', node, device, root, source_ref=sha)
    assert view['local_checks_passed'] and view['commit'] == sha
    assert view['warnings'] and view['node'] == node
    assert view['remote_workdir'] == deployment_policy(root)['targets'][node]['repo_path']
    assert view['argv'][-2:] == ['--node-id', node]
    assert view['submitted'] is False and view['remote_checks'].startswith('NOT OBSERVED')
    assert not (root / 'results').exists()
    assert not (root / '.syncmate/runner_queues').exists()


@pytest.mark.parametrize('condition', ['wrong_alias', 'wrong_path', 'unknown_node'])
def test_dispatch_rejects_unregistered_peer_before_transport(workspace, condition):
    root, sha, device_file = setup_controller(workspace)
    node = 'gpu4090-2'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    if condition == 'unknown_node':
        node = 'unknown'
    else:
        key = 'ssh' if condition == 'wrong_alias' else 'repo_path'
        device['peers'][node][key] = 'autodl-opengu' if key == 'ssh' else '/unregistered/project'
        device_file.write_text(yaml.safe_dump(device), encoding='utf-8')
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
        '--project-root', str(root), '--source-ref', sha, '--config', str(device_file),
        'runner-agent', 'dispatch', node, '--recipe', 'private-check', '--job-id', 'private-job', '--json'],
        capture_output=True, text=True, encoding='utf-8', timeout=90)
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload['status'] == 'blocked'
    assert any(word in str(payload) for word in ('runner', 'deployment target'))
    assert not (root / '.syncmate/runs').exists()
    assert not (root / 'results').exists()


def test_generic_console_cannot_bypass_installed_submission(workspace):
    root, _, _ = setup_controller(workspace)
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-m', 'opengu_syncmate',
        '--project-root', str(root), 'console'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1
    assert 'generic console submission is unsupported' in result.stdout


def test_install_actions_require_explicit_node(workspace):
    root, _, _ = setup_controller(workspace)
    for action in ('apply', 'receipt'):
        result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/install.py', action],
            cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=30)
        assert result.returncode == 2 and '--node' in result.stderr
