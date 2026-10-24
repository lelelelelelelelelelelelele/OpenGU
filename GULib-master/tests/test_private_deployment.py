"""Real private-policy preview/dispatch; only local disposable Git peers."""
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from scripts.syncmate.deployment_policy import deployment_policy
from scripts.syncmate.recipe import preview
from scripts.syncmate.opengu_recipes import generate
from syncmate_core.devices import build_peer_config
from test_syncmate_execution_contract import workspace, tables, commit, git
from test_recipe_yaml import save_spec


def setup_controller(workspace):
    root, config, _ = workspace
    spec = generate('experiment.yaml', recipe_id='private-check', run_id='private-run', project_root=root)
    save_spec(root, spec)
    sha = commit(root)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    device['role'] = 'runner+collector'
    device['peers'] = {'cpu': build_peer_config('runner', None, str(root), transport='local')}
    device_file.write_text(yaml.safe_dump(device), encoding='utf-8')
    policy = deployment_policy(root)
    # Reviewed receipt fixture, independently exercised against real Git installation tests.
    receipt = {'status': 'installed', 'target': sha, 'head': sha,
        'project': '/autodl-fs/data/OpenGU/GULib-master', 'transport': 'private-bundle',
        'policy_sha256': policy['sha256'], 'bundle_sha256': 'd'*64, 'origin_refs_unchanged': True}
    receipt_path = root / '.workblock/runtime/install' / sha / 'receipt.json'
    receipt_path.parent.mkdir(parents=True)
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    return root, config, sha, device_file, receipt_path


def dispatch(root, device_file):
    # Global options precede the subcommands to exercise actual parser semantics.
    return subprocess.run([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
        '--config', str(device_file), '--project-root', str(root),
        'runner-agent', 'dispatch', 'cpu', '--recipe', 'private-check',
        '--job-id', 'private-job', '--json'], cwd=root, capture_output=True, text=True,
        encoding='utf-8', timeout=90)


def test_private_preview_and_real_dispatch_without_public_origin(workspace, record_property):
    root, config, sha, device, receipt = setup_controller(workspace)
    assert git(root, 'remote') == ''
    view = preview('private-check', 'cpu', device, root)
    assert view['local_checks_passed'], view
    assert view['installation_receipt']['target'] == sha
    result = dispatch(root, device)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload['status'] == 'submitted', payload
    assert payload['expected_git_sha'] == sha
    assert not (root / 'results').exists()  # queued only, no scientific execution
    record_property('private_dispatch', json.dumps({'sha': sha, 'status': payload['status'],
        'public_origin': None, 'runner_sha': payload['runner_identity']['payload']['git']['sha'],
        'receipt': view['installation_receipt'], 'scientific_execution': False}))


@pytest.mark.parametrize('condition', ['receipt_missing', 'receipt_wrong_sha', 'dirty', 'branch', 'stale_config'])
def test_private_dispatch_rejects_invalid_inputs(workspace, condition):
    root, config, sha, device, receipt = setup_controller(workspace)
    if condition == 'receipt_missing':
        receipt.unlink()
    elif condition == 'receipt_wrong_sha':
        value = json.loads(receipt.read_text(encoding='utf-8'))
        value['target'] = '0'*40
        receipt.write_text(json.dumps(value), encoding='utf-8')
    elif condition == 'dirty':
        (root / 'uncommitted.txt').write_text('dirty', encoding='utf-8')
    elif condition == 'branch':
        git(root, 'switch', '-c', 'candidate')
    else:
        config.write_text(config.read_text(encoding='utf-8') + '\n# changed reviewed input\n', encoding='utf-8')
        new_sha = commit(root)
        value = json.loads(receipt.read_text(encoding='utf-8'))
        value.update(target=new_sha, head=new_sha)
        target = receipt.parent.parent / new_sha / 'receipt.json'
        target.parent.mkdir()
        target.write_text(json.dumps(value), encoding='utf-8')
    result = dispatch(root, device)
    assert result.returncode != 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload['status'] == 'blocked', payload
    errors = json.dumps(payload)
    expected = {'receipt_missing': 'receipt is missing', 'receipt_wrong_sha': 'receipt is not successful',
                'dirty': 'clean local main', 'branch': 'clean local main', 'stale_config': 'SHA-256'}
    assert expected[condition] in errors, payload
    assert not list((root / '.syncmate/runner_queue/inbox').glob('*'))
    assert not (root / 'results').exists()


@pytest.mark.parametrize('condition', ['runner_dirty', 'runner_branch', 'runner_sha'])
def test_private_dispatch_checks_real_peer_identity(workspace, condition):
    root, config, sha, device, receipt = setup_controller(workspace)
    peer = root / '.syncmate/private-peer'
    git(root, 'clone', str(root), str(peer))
    remote_device = peer / '.syncmate/device.yaml'
    remote_device.parent.mkdir(exist_ok=True)
    remote_device.write_text(yaml.safe_dump({'version': 1, 'device_id': 'private-peer',
        'role': 'runner', 'repo_path': str(peer), 'execution_device': 'cpu', 'peers': {}}), encoding='utf-8')
    value = yaml.safe_load(device.read_text(encoding='utf-8'))
    value['peers'] = {'cpu': build_peer_config('runner', None, str(peer), transport='local')}
    device.write_text(yaml.safe_dump(value), encoding='utf-8')
    if condition == 'runner_dirty':
        (peer / 'uncommitted.txt').write_text('uncommitted', encoding='utf-8')
    elif condition == 'runner_branch':
        git(peer, 'switch', '-c', 'candidate')
    else:
        (peer / 'different.txt').write_text('different commit', encoding='utf-8')
        commit(peer)
    result = dispatch(root, device)
    assert result.returncode != 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload['status'] == 'blocked'
    assert payload['errors'] == ['dispatch requires local and runner clean main to share the same full Git SHA']
    assert not list((peer / '.syncmate/runner_queue/inbox').glob('*'))
