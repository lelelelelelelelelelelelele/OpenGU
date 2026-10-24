"""Node-bound preview and CLI admission; no SSH, GPU or observer service."""
import json
import subprocess
import sys

import pytest
import yaml
from scripts.syncmate.deployment_policy import deployment_policy, receipt_path
from scripts.syncmate.recipe import preview
from scripts.syncmate.opengu_recipes import generate
from scripts.syncmate import syncmate
from test_syncmate_execution_contract import workspace, tables, commit, git
from test_recipe_yaml import save_spec


def setup_controller(workspace):
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='private-check', run_id='private-run', project_root=root)
    save_spec(root, spec)
    sha = commit(root)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    policy = deployment_policy(root)
    device['role'] = 'runner+collector'
    device['peers'] = {node: {'role': 'runner', 'transport': 'ssh', **target}
                       for node, target in policy['targets'].items()}
    device_file.write_text(yaml.safe_dump(device), encoding='utf-8')
    paths = {}
    for node, target in policy['targets'].items():
        receipt = {'status': 'installed', 'node': node, 'ssh': target['ssh'],
            'target': sha, 'head': sha, 'project': target['repo_path'], 'transport': 'private-bundle',
            'policy_sha256': policy['sha256'], 'bundle_sha256': 'd'*64, 'origin_refs_unchanged': True}
        path = receipt_path(root, node, sha, policy)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(receipt), encoding='utf-8')
        paths[node] = path
    return root, config, sha, device_file, paths


def dispatch_argv(root, device_file, node):
    return ['--config', str(device_file), '--project-root', str(root),
            'runner-agent', 'dispatch', node, '--recipe', 'private-check',
            '--job-id', 'private-job', '--json']


@pytest.mark.parametrize('node', ['gpu4090', 'gpu4090-2'])
def test_native_preview_selects_exact_node_without_remote_contact(workspace, node, record_property):
    root, _, sha, device, paths = setup_controller(workspace)
    result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/recipe.py',
        'preview', 'private-check', '--node', node, '--device-config', str(device)],
        cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=90)
    assert result.returncode == 0, result.stdout + result.stderr
    view = json.loads(result.stdout)
    assert view['local_checks_passed'], view
    assert view['installation_receipt'] == {'path': str(paths[node]), 'node': node,
                                           'target': sha, 'status': 'installed'}
    assert view['ssh_alias'] == deployment_policy(root)['targets'][node]['ssh']
    assert view['remote_workdir'] == deployment_policy(root)['targets'][node]['repo_path']
    assert view['local_receiving_root'].endswith(str(root / 'results/runs' / node))
    assert view['submitted'] is False and view['remote_checks'].startswith('NOT OBSERVED')
    assert not (root / 'results').exists()
    assert not (root / '.syncmate/runner_queue').exists()
    record_property('node_preview', json.dumps({'node': node, 'sha': sha,
        'local_checks_passed': True, 'receipt': view['installation_receipt'], 'remote_contact': False}))


@pytest.mark.parametrize('condition', ['receipt_missing', 'receipt_wrong_sha', 'other_node_receipt',
                                       'wrong_alias', 'wrong_path'])
def test_native_dispatch_rejects_before_core_or_ssh(workspace, condition):
    root, _, sha, device, paths = setup_controller(workspace)
    node = 'gpu4090-2'
    path = paths[node]
    if condition == 'receipt_missing':
        path.unlink()
    elif condition == 'other_node_receipt':
        path.write_bytes(paths['gpu4090'].read_bytes())
    elif condition == 'receipt_wrong_sha':
        value = json.loads(path.read_text(encoding='utf-8'))
        value['target'] = '0'*40
        path.write_text(json.dumps(value), encoding='utf-8')
    else:
        value = yaml.safe_load(device.read_text(encoding='utf-8'))
        key = 'ssh' if condition == 'wrong_alias' else 'repo_path'
        value['peers'][node][key] = value['peers']['gpu4090'][key]
        device.write_text(yaml.safe_dump(value), encoding='utf-8')
    view = preview('private-check', node, device, root)
    assert not view['local_checks_passed']
    result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
        *dispatch_argv(root, device, node)], cwd=root, capture_output=True, text=True,
        encoding='utf-8', timeout=90)
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload['status'] == 'blocked', payload
    expected = ('receipt is missing' if condition == 'receipt_missing' else
                'alias and project' if condition in ('wrong_alias', 'wrong_path') else 'receipt is not successful')
    assert expected in json.dumps(payload), payload
    assert not (root / '.syncmate/runs').exists()
    assert not (root / '.syncmate/controller').exists()
    assert not (root / 'results').exists()


@pytest.mark.parametrize('node', ['gpu4090', 'gpu4090-2'])
def test_dispatch_wrapper_uses_parsed_node_id_and_selected_device_file(workspace, node, monkeypatch):
    root, _, _, device, _ = setup_controller(workspace)
    calls = []
    # A narrow wrapper seam: no replacement of Core preflight/queue/transport.
    # This proves admission reaches Core with the original args, not execution.
    def core_entry(argv, **kwargs):
        calls.append((argv, kwargs))
        return 0
    monkeypatch.setattr(syncmate, 'core_main', core_entry)
    argv = dispatch_argv(root, device, node)
    assert syncmate.main(argv) == 0
    assert len(calls) == 1 and calls[0][0] == argv
    assert calls[0][1]['project_root'] == root
    assert calls[0][1]['require_origin_main'] is False


def test_install_actions_require_explicit_node(workspace):
    root, _, _, _, _ = setup_controller(workspace)
    for action in ('apply', 'initialize', 'receipt'):
        result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/install.py', action],
            cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=30)
        assert result.returncode == 2
        assert '--node' in result.stderr
