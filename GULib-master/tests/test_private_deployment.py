"""Node-bound preview and CLI admission; no SSH, GPU or observer service."""
import json
import subprocess
import sys

import pytest
from local_transport_guard import local_only_transport
import yaml
from scripts.syncmate.deployment_policy import deployment_policy, receipt_path, dependency_pin
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
    device['peers'] = {node: {'role': 'runner', 'transport': 'ssh', 'python_executable': sys.executable, **target}
                       for node, target in policy['targets'].items()}
    device_file.write_text(yaml.safe_dump(device), encoding='utf-8')
    paths = {}
    for node, target in policy['targets'].items():
        receipt = {'status': 'installed', 'node': node, 'ssh': target['ssh'],
            'target': sha, 'head': sha, 'project': target['repo_path'], 'transport': 'private-bundle',
            'policy_sha256': policy['sha256'], 'bundle_sha256': 'd'*64, 'origin_refs_unchanged': True}
        _, digest = dependency_pin(root)
        receipt.update(expected_environment={'python_executable': sys.executable, 'core_dependency_sha256': digest}, environment={'node_id': node, 'git_sha': sha, 'requested_python': sys.executable, 'python_executable': sys.executable, 'core_dependency_sha256': digest, 'core_payload_verified': True})
        path = receipt_path(root, node, sha, policy)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(receipt), encoding='utf-8')
        paths[node] = path
    return root, config, sha, device_file, paths


def dispatch_argv(root, device_file, node):
    return ['--config', str(device_file), '--project-root', str(root),
            'runner-agent', 'dispatch', node, '--recipe', 'private-check',
            '--job-id', 'private-job', '--json']


def native_fixture_identity(root,calls):
    """Translate SSH transport only to a real disposable native self command."""
    def invoke(peer,argv,**kwargs):
        assert argv==['self','--json']
        node=peer['node_id']
        calls.append(node)
        result=subprocess.run([sys.executable,'-B','scripts/syncmate/syncmate.py',
            '--project-root',str(root),'--node-id',node,'self','--json'],cwd=root,
            capture_output=True,text=True,encoding='utf-8',timeout=30)
        assert result.returncode==0,result.stdout+result.stderr
        return {'ok':True,'payload':json.loads(result.stdout),'errors':[]}
    return invoke


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
        value['peers'][node][key] = 'autodl-opengu' if key == 'ssh' else '/unregistered/project'
        device.write_text(yaml.safe_dump(value), encoding='utf-8')
    view = preview('private-check', node, device, root)
    assert not view['local_checks_passed']
    result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
        *dispatch_argv(root, device, node)], cwd=root, capture_output=True, text=True,
        encoding='utf-8', timeout=90)
    assert result.returncode == 1, result.stdout + result.stderr
    assert result.stdout, result.stderr
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
    for action in ('apply', 'receipt'):
        result = subprocess.run([sys.executable, '-B', 'scripts/syncmate/install.py', action],
            cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=30)
        assert result.returncode == 2
        assert '--node' in result.stderr


def test_core_ui_readiness_uses_selected_node_receipt(workspace,monkeypatch):
    from syncmate_core import context
    from syncmate_core.controller import readiness
    from syncmate_core import dispatch
    from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
    from scripts.syncmate.deployment_policy import execution_readiness
    root, _, _, device, paths = setup_controller(workspace)
    paths['gpu4090-2'].write_bytes(paths['gpu4090'].read_bytes())
    local_self=[]
    monkeypatch.setattr(dispatch,'runner_agent_peer_invoke',native_fixture_identity(root,local_self))
    with context.use(root, extension=OpenGUProjectExtension(), require_origin_main=False):
        valid = readiness('gpu4090', 'private-check', execution_readiness)
        invalid = readiness('gpu4090-2', 'private-check', execution_readiness)
    assert valid['ready'], valid
    assert local_self==['gpu4090']
    assert not invalid['ready'] and 'receipt is not successful' in json.dumps(invalid)
    assert not (root / '.syncmate/runs').exists()
    assert not (root / 'results').exists()


def test_console_entry_binds_native_execution_readiness_hook(workspace,monkeypatch):
    from syncmate_core import console
    from scripts.syncmate.deployment_policy import execution_readiness
    root, _, _, _, _ = setup_controller(workspace)
    calls=[]
    def serve(projects,port,desktop):
        calls.append((projects,port,desktop))
    monkeypatch.setattr(console,'serve_console',serve)
    assert syncmate.main(['--project-root',str(root),'console','--port','8767']) == 0
    assert calls[0][0][root.name].execution_readiness is syncmate.execution_readiness


@pytest.mark.parametrize('node',['gpu4090','gpu4090-2'])
@pytest.mark.parametrize('condition',['wrong_receipt','wrong_alias','ambiguous_peer'])
def test_actual_controller_submit_blocks_wrong_node_before_dispatch(workspace,monkeypatch,node,condition):
    from dataclasses import replace
    from syncmate_core import context,dispatch
    from syncmate_core.controller import Controller
    from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
    root, _, _, device, paths = setup_controller(workspace)
    original_device=device.read_bytes()
    original_receipt=paths[node].read_bytes()
    other='gpu4090-2' if node=='gpu4090' else 'gpu4090'
    expected_error='receipt is not successful'
    if condition=='wrong_receipt':
        paths[node].write_bytes(paths[other].read_bytes())
    else:
        value=yaml.safe_load(device.read_text(encoding='utf-8'))
        if condition=='wrong_alias':
            value['peers'][node]['ssh']=value['peers'][other]['ssh']
            value['peers'][node]['artifact_policy']={'include':['run.json']}
            expected_error='alias and project'
        else:
            value['peers'][node]=dict(value['peers'][other])
            expected_error='one registered node'
        device.write_text(yaml.safe_dump(value),encoding='utf-8')
    with context.use(root,extension=OpenGUProjectExtension()) as project:
        project=replace(project,execution_readiness=syncmate.execution_readiness)
    controller=Controller(project)
    started=[]
    remote=[]
    monkeypatch.setattr(controller,'start_thread',lambda target,args:started.append((target,args)))
    def forbidden(*args,**kwargs):
        remote.append(args)
        pytest.fail('blocked GUI submission reached dispatch or a remote call')
    monkeypatch.setattr(dispatch,'runner_agent_peer_invoke',forbidden)
    monkeypatch.setattr(dispatch,'runner_agent_dispatch_payload',forbidden)
    with pytest.raises(ValueError,match=expected_error):
        controller.submit(node,'private-check','11111111-1111-1111-1111-111111111111')
    assert started==[] and remote==[]
    assert not (root/'.syncmate/controller').exists()
    device.write_bytes(original_device)
    paths[node].write_bytes(original_receipt)
    # Preserve the original Core dispatch continuation without executing it.
    local_self=[]
    monkeypatch.setattr(dispatch,'runner_agent_peer_invoke',native_fixture_identity(root,local_self))
    saved=controller.submit(node,'private-check','22222222-2222-2222-2222-222222222222')
    assert local_self==[node]
    assert saved['node_id']==node
    assert len(started)==1 and started[0][0]==controller._dispatch
    assert started[0][1][0]['job_id']==saved['job_id'] and remote==[]
