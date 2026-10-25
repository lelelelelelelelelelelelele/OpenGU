"""Real packages and shared Git/queues; only unavailable SSH is simulated."""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from syncmate_core import context, queue
from opengu_syncmate import provision
from test_experiment_install import checkout, local_transport, git, isolated_node


def offline_second(client, monkeypatch):
    original = client.invoke
    def invoke(peer, request):
        if request['node'] == 'gpu4090-2':
            raise client.NodeOffline('Connection refused')
        return original(peer, request)
    monkeypatch.setattr(client, 'invoke', invoke)


def test_offline_idle_node_does_not_block_online_shared_update(local_transport, monkeypatch, capsys):
    client, project, source, request, protected, peers, calls = local_transport
    offline_second(client, monkeypatch)
    assert client.deploy('gpu4090-2') == 0
    result = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert result['coordinator'] == 'gpu4090'
    assert result['status'] == 'installed_with_deferred_nodes'
    assert result['deferred']['gpu4090-2']['status'] == 'deferred'
    assert set(result['shared_update']['nodes']) == set(peers)
    assert set(result['after']) == {'gpu4090'}
    assert git(project, 'rev-parse', 'HEAD') == request['target']
    assert protected.read_bytes() == b'untouched-cache'
    assert not (source / '.workblock/runtime/install/gpu4090-2' / request['target'] / 'receipt.json').exists()


@pytest.mark.parametrize('condition', ['busy', 'unknown'])
def test_offline_does_not_turn_physical_occupancy_into_idle(local_transport, monkeypatch, condition):
    client, project, source, request, protected, peers, calls = local_transport
    offline_second(client, monkeypatch)
    with context.use(project, node_id='gpu4090-2'):
        if condition == 'unknown':
            queue.runner_agent_lock_dir().mkdir()
            (queue.runner_agent_lock_dir() / 'owner.json').write_text('{}', encoding='utf-8')
        else:
            queue.runner_queue_job_path('inbox', 'reserved').write_text('id: reserved', encoding='utf-8')
    assert client.deploy('gpu4090') == 1
    assert git(project, 'rev-parse', 'HEAD') == request['old']
    assert protected.read_bytes() == b'untouched-cache'


def test_only_initial_connection_failure_can_be_deferred():
    from scripts.syncmate.install import NodeOffline, response_json
    refused = subprocess.CompletedProcess([], 255, '', 'Connection refused')
    with pytest.raises(NodeOffline):
        response_json(refused, may_defer=True)
    with pytest.raises(ValueError) as error:
        response_json(refused)
    assert not isinstance(error.value, NodeOffline)
    for result in [subprocess.CompletedProcess([],255,'','Permission denied (publickey)'),
                   subprocess.CompletedProcess([],1,'{"status":"blocked"}','')]:
        with pytest.raises(ValueError) as error:
            response_json(result, may_defer=True)
        assert not isinstance(error.value, NodeOffline)


def provision_process(python, request, *, success=True):
    code = Path(provision.__file__).read_text(encoding='utf-8')
    result = subprocess.run([str(python), '-I', '-X', 'utf8', '-B', '-c', code],
        input=json.dumps(request), capture_output=True, text=True, encoding='utf-8', timeout=240)
    if success:
        assert result.returncode == 0, result.stdout + result.stderr
    else:
        assert result.returncode != 0
    return json.loads(result.stdout)


def test_returning_old_node_installs_exact_runtime_and_real_entry_works(checkout, tmp_path, monkeypatch):
    project, request, protected = checkout
    source = tmp_path / 'source/GULib-master'
    repository = Path(__file__).resolve().parents[1]
    for name in ('scripts/syncmate/syncmate.py', 'opengu_syncmate/provision.py'):
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((repository / name).read_bytes())
    git(source, 'add', 'scripts/syncmate/syncmate.py', 'opengu_syncmate/provision.py')
    git(source, 'commit', '-m', 'bounded deployment bootstrap')
    sha = git(source, 'rev-parse', 'HEAD')
    bundle = tmp_path / 'bootstrap.bundle'
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main', '^' + request['old'])
    request.update(target=sha, bundle=base64.b64encode(bundle.read_bytes()).decode(),
                   bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest())
    bases = {}
    for node in ('gpu4090', 'gpu4090-2'):
        prefix = tmp_path / ('base-' + node)
        subprocess.run([sys.executable, '-I', '-B', '-m', 'venv', '--without-pip', '--system-site-packages', str(prefix)], check=True)
        bases[node] = prefix / 'Scripts/python.exe'
    pins = {'core': request['core_dependency'], 'control': request['control_dependency']}
    manifest = {'protocol': provision.PROTOCOL, 'source_sha': sha, 'policy': json.loads((source / 'scripts/syncmate/deployment.json').read_text(encoding='utf-8')),
                'pins': pins, 'controller': {'base_python': sys.executable, 'root': str(source)},
                'nodes': {n: {'base_python': str(p)} for n,p in bases.items()}, 'verification_roots': [str(project)]}
    # Use the exact reviewed deployment wheels, supplied explicitly by the test owner.
    wheels = {key: base64.b64encode(Path(os.environ['OPENGU_TEST_' + key.upper() + '_WHEEL']).read_bytes()).decode()
              for key in pins}
    prepare = {'action': 'prepare', 'node': 'gpu4090', 'root': str(project), 'manifest': manifest, 'wheels': wheels,
               'bundle': request['bundle'], 'bundle_sha256': request['bundle_sha256']}
    online = provision_process(bases['gpu4090'], prepare)
    assert online['status'] == 'ready'
    offline_runtime = Path(provision.runtime_python(str(bases['gpu4090-2']), pins))
    assert not offline_runtime.exists()
    corrupt = provision_process(bases['gpu4090-2'], {**prepare, 'node': 'gpu4090-2',
        'wheels': {**wheels, 'control': base64.b64encode(b'corrupt wheel').decode()}}, success=False)
    assert 'wheel digest differs' in str(corrupt) and not offline_runtime.exists()
    # Execute the actual rollout client, translating only the disposable address.
    from scripts.syncmate import install as client, install_remote
    import yaml
    monkeypatch.setattr(client, 'ROOT', source)
    peers = {n: {'role':'runner', 'transport':'ssh', 'python_executable':str(bases[n]), **target}
             for n,target in manifest['policy']['targets'].items()}
    config = source / '.syncmate/device.yaml'
    config.parent.mkdir(exist_ok=True)
    config.write_text(yaml.safe_dump({'version':1,'device_id':'fixture','role':'collector',
                                    'repo_path':str(source),'peers':peers}), encoding='utf-8')
    provision.stage(source, {**prepare, 'root':str(source)})
    def remote(peer, supplied):
        if supplied['node'] == 'gpu4090-2':
            raise client.NodeOffline('Connection refused')
        code = '''import json,runpy,sys
from pathlib import Path
module=runpy.run_path(sys.argv[1]);request=json.load(sys.stdin)
try:
 action=request['action'];root=Path(sys.argv[2])
 result=module['install_checkout'](root,request) if action=='apply' else module['inspect_checkout'](root,request)
 print(json.dumps(result))
except Exception as exc:
 print(json.dumps({'status':'blocked','error':str(exc)}));raise SystemExit(1)
'''
        result = subprocess.run([peer['python_executable'],'-I','-X','utf8','-B','-c',code,
            install_remote.__file__,str(project)],input=json.dumps(supplied),capture_output=True,text=True,encoding='utf-8',timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr
        return {**json.loads(result.stdout), 'project':peer['repo_path']}
    monkeypatch.setattr(client, 'invoke', remote)
    def node_provision(peer, supplied, **kwargs):
        if supplied.get('node') == 'gpu4090-2':
            raise client.NodeOffline('Connection refused')
        return provision_process(peer['python_executable'], {**supplied,'root':str(project)})
    monkeypatch.setattr(client, 'provision_node', node_provision)
    assert client.deploy('gpu4090-2', manifest=manifest) == 0
    assert git(project,'rev-parse','HEAD') == sha
    rollout = json.loads((provision.directory(source,sha)/'rollout.json').read_text(encoding='utf-8'))
    assert rollout['nodes'] == {'gpu4090':{'status':'verified'},'gpu4090-2':{'status':'deferred'}}
    updated = yaml.safe_load(config.read_text(encoding='utf-8'))
    assert updated['peers']['gpu4090-2']['python_executable'] == str(offline_runtime)
    # A returning node has only its old 0.6 base, not a preinstalled control package.
    for base in bases.values():
        check = subprocess.check_output([str(base), '-I', '-B', '-c', 'import syncmate_core;print(syncmate_core.__version__)'], text=True).strip()
        assert check == '0.6.0'
    returned = subprocess.run([str(bases['gpu4090-2']), '-I', '-X', 'utf8', '-B',
        str(project / 'scripts/syncmate/syncmate.py'), '--node-id', 'gpu4090-2', 'dependencies'],
        capture_output=True, text=True, encoding='utf-8', timeout=240)
    assert returned.returncode == 0, returned.stdout + returned.stderr
    result = json.loads(returned.stdout)
    assert result['status'] == 'verified' and result['git_sha'] == sha
    assert result['dependencies']['syncmate_core']['version'] == '0.7.0'
    assert result['dependencies']['opengu_syncmate']['version'] == '0.2.0'
    supplied = subprocess.run([str(offline_runtime), '-I', '-X', 'utf8', '-B',
        str(project / 'scripts/syncmate/syncmate.py'), '--node-id', 'gpu4090-2', 'source-status'],
        input=json.dumps({'target':sha}), capture_output=True, text=True, encoding='utf-8', timeout=60)
    assert supplied.returncode == 0, supplied.stdout + supplied.stderr
    assert json.loads(supplied.stdout)['available'] is True
    assert offline_runtime.exists() and protected.read_bytes() == b'untouched-cache'
    receipt = json.loads((provision.directory(project, sha) / 'nodes/gpu4090-2.json').read_text(encoding='utf-8'))
    assert receipt['node'] == 'gpu4090-2' and receipt['runtime_python'] == str(offline_runtime)
    # A ready runtime is verified on every reconnect; corruption is preserved.
    payload = offline_runtime.parent.parent / 'Lib/site-packages/opengu_syncmate/runtime.py'
    payload.write_bytes(payload.read_bytes() + b'\n# controlled corruption\n')
    rejected = provision_process(bases['gpu4090-2'], {'action':'ensure','node':'gpu4090-2','root':str(project)}, success=False)
    assert rejected['status'] == 'blocked' and 'payload differs' in str(rejected)
    assert payload.read_bytes().endswith(b'# controlled corruption\n')
    for base in bases.values():
        assert subprocess.check_output([str(base),'-I','-B','-c','import syncmate_core;print(syncmate_core.__version__)'],text=True).strip() == '0.6.0'
