"""Real fast-forward Git installation in disposable repositories; no SSH/GPU."""
import base64
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
import pytest
from local_transport_guard import local_only_transport
from scripts.syncmate import install_remote as installer
from syncmate_core import context, maintenance, queue
from scripts.syncmate.deployment_policy import PRIVATE_POLICY, deployment_policy, installation_receipt, receipt_path, validate_peer, validate_receipt, dependency_pin


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def isolated_node(project, request, action):
    """Match the real -I SSH process; pytest's source path must not enter it."""
    code = '''import json, runpy, sys
from pathlib import Path
module = runpy.run_path(sys.argv[1])
request = json.load(sys.stdin)
try:
    if sys.argv[3] == 'apply': result = module['install_checkout'](Path(sys.argv[2]), request)
    elif sys.argv[3] == 'restore': result = module['restore_runner'](Path(sys.argv[2]), request)
    else: result = module['inspect_checkout'](Path(sys.argv[2]), request, status=sys.argv[3] == 'inspect')
    print(json.dumps(result))
except Exception as exc:
    print(json.dumps({'error': str(exc)}))
    raise SystemExit(1)
'''
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-c', code,
        installer.__file__, str(project), action], input=json.dumps(request),
        capture_output=True, text=True, encoding='utf-8', timeout=60)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    return json.loads(result.stdout)


@pytest.fixture
def checkout(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    git(source, 'init', '-b', 'main')
    git(source, 'config', 'user.name', 'Install test')
    git(source, 'config', 'user.email', 'test@example.invalid')
    project = source / 'GULib-master'
    project.mkdir()
    (source / '.gitignore').write_text('GULib-master/.syncmate/\nGULib-master/data/\n')
    (project / 'run.py').write_text('value = 1\n')
    entry = project / 'scripts/syncmate/syncmate.py'
    entry.parent.mkdir(parents=True)
    entry.write_text('from pathlib import Path\nfrom syncmate_core.cli import main\n'
                     'raise SystemExit(main(project_root=Path(__file__).resolve().parents[2]))\n')
    git(source, 'add', '.')
    git(source, 'commit', '-m', 'base')
    remote = tmp_path / 'remote'
    git(tmp_path, 'clone', str(source), str(remote))
    old = git(source, 'rev-parse', 'HEAD')
    (project / 'run.py').write_text('value = 2\n')
    policy = project / 'scripts/syncmate/deployment.json'
    policy.write_text(json.dumps(PRIVATE_POLICY), encoding='utf-8')
    pin_path = project / 'scripts/syncmate/core_dependency.json'
    pin_path.write_bytes(Path(installer.__file__).with_name('core_dependency.json').read_bytes())
    pin = json.loads(pin_path.read_text(encoding='utf-8'))
    control_path = pin_path.with_name('control_dependency.json')
    control_path.write_bytes(Path(installer.__file__).with_name('control_dependency.json').read_bytes())
    control_pin = json.loads(control_path.read_text(encoding='utf-8'))
    git(source, 'add', str(policy), str(pin_path), str(control_path))
    git(source, 'commit', '-am', 'target')
    target = git(source, 'rev-parse', 'HEAD')
    bundle = tmp_path / 'update.bundle'
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main', '^' + old)
    protected = remote / 'GULib-master/data/cache.bin'
    protected.parent.mkdir()
    protected.write_bytes(b'untouched-cache')
    runner_project = remote / 'GULib-master'
    for node in ('gpu4090', 'gpu4090-2'):
        with context.use(runner_project, node_id=node):
            queue.ensure_runner_queue_dirs()
    import yaml
    (runner_project / '.syncmate/device.yaml').write_text(yaml.safe_dump({'version': 1, 'device_id': 'shared-fixture', 'role': 'runner', 'repo_path': str(runner_project), 'execution_device': 'cpu', 'peers': {}}), encoding='utf-8')
    return runner_project, {'core_dependency': pin, 'control_dependency': control_pin, 'node_ids': ['gpu4090', 'gpu4090-2'], 'python_executable': sys.executable, 'old': old, 'target': target, 'node': 'gpu4090', 'ssh': 'autodl-opengu',
        'bundle': base64.b64encode(bundle.read_bytes()).decode(),
        'bundle_sha256': hashlib.sha256(bundle.read_bytes()).hexdigest(),
        'transport': 'private-bundle', 'policy_sha256': hashlib.sha256(json.dumps(json.loads(policy.read_text(encoding='utf-8')), sort_keys=True, separators=(',', ':')).encode()).hexdigest()}, protected


def test_exact_private_install_preserves_cache_and_origin_without_network(checkout, monkeypatch):
    project, request, protected = checkout
    before_origin = installer.origin_refs(project.parent)
    real_run = subprocess.run
    commands = []
    def guarded_run(argv, *args, **kwargs):
        commands.append(argv)
        assert not any(v in ('ssh', 'push', 'ls-remote', 'origin') for v in argv)
        return real_run(argv, *args, **kwargs)
    monkeypatch.setattr(subprocess, 'run', guarded_run)
    result = installer.install_checkout(project, request)
    assert result['status'] == 'installed'
    assert result['head'] == request['target']
    assert result['transport'] == 'private-bundle'
    assert result['bundle_sha256'] == request['bundle_sha256']
    assert result['policy_sha256'] == request['policy_sha256']
    assert result['origin_refs_unchanged']
    assert installer.origin_refs(project.parent) == before_origin
    assert not any(n['restart'] for n in result['nodes'].values())
    assert protected.read_bytes() == b'untouched-cache'
    assert not list((project.parent / '.git').glob('install-*.bundle'))
    repeated = installer.install_checkout(project, {**request, 'old': request['target']})
    assert repeated['status'] == 'already_installed'
    assert any('fetch' in argv for argv in commands)


def test_busy_install_does_not_fetch_or_modify(checkout, monkeypatch):
    project, request, _ = checkout
    with context.use(project, node_id='gpu4090'):
        queue.ensure_runner_queue_dirs()
        queue.runner_queue_job_path('inbox', 'waiting').write_text('id: waiting')
    with pytest.raises(maintenance.Busy, match='inbox'):
        installer.install_checkout(project, request)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']


def test_protected_payload_diff_is_rejected(checkout):
    project, request, _ = checkout
    repo = project.parent
    git(repo, 'config', 'user.name', 'Install test')
    git(repo, 'config', 'user.email', 'test@example.invalid')
    (project / 'data/forbidden').write_text('payload')
    git(repo, 'add', '-f', 'GULib-master/data/forbidden')
    git(repo, 'commit', '-m', 'forbidden')
    with pytest.raises(ValueError, match='protected payload'):
        installer.check_paths(repo, request['old'], git(repo, 'rev-parse', 'HEAD'))


def test_wrong_remote_tip_leaves_truthful_failure_state(checkout, monkeypatch):
    project, request, _ = checkout
    request['target'] = 'a' * 40
    with pytest.raises(ValueError, match='bundle target or advertised refs mismatch'):
        installer.install_checkout(project, request)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']
    with context.use(project, node_id='gpu4090'):
        assert maintenance.marker().exists()


def test_idle_runner_is_stopped_and_restored_after_install(checkout, monkeypatch):
    project, request, _ = checkout
    device = project / '.syncmate/device.yaml'
    device.parent.mkdir(exist_ok=True)
    import yaml
    device.write_text(yaml.safe_dump({'version': 1, 'device_id': 'test', 'role': 'runner',
                                     'repo_path': str(project), 'peers': {}}))
    worker = subprocess.Popen([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
        '--node-id', 'gpu4090', 'runner-agent', 'serve', '--poll-seconds', '1'], cwd=project,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        with context.use(project, node_id='gpu4090'):
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if queue.runner_queue_load_json(queue.runner_agent_lock_dir() / 'owner.json').get('restartable'):
                    break
                time.sleep(.05)
            else:
                pytest.fail('test runner did not start')
        result = installer.install_checkout(project, request)
        assert result['nodes']['gpu4090']['restart']
        restored = isolated_node(project, {**request, 'runner': result['nodes']['gpu4090']['runner']}, 'restore')
        assert restored['status'] == 'restored'
        assert result['status'] == 'installed'
        worker.wait(timeout=10)
    finally:
        if worker.poll() is None:
            worker.terminate()
            worker.wait(timeout=10)
        with context.use(project, node_id='gpu4090'):
            if queue.runner_agent_lock_dir().exists():
                with maintenance.installation(node_ids=['gpu4090', 'gpu4090-2'], timeout=10):
                    pass


@pytest.mark.parametrize('field,value,match', [
    ('bundle_sha256', '0'*64, 'bundle SHA-256 mismatch'),
    ('policy_sha256', '0'*64, 'target deployment policy mismatch'),
    ('transport', 'accelerated-git', 'explicit private-bundle'),
    ('old', '0'*40, 'runner version changed'),
])
def test_mismatched_private_inputs_never_merge(checkout, field, value, match):
    project, request, _ = checkout
    before = installer.origin_refs(project.parent)
    with pytest.raises(ValueError, match=match):
        installer.install_checkout(project, {**request, field: value})
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']
    assert installer.origin_refs(project.parent) == before
    assert not list((project.parent / '.git').glob('install-*.bundle'))


def test_remote_clean_source_is_mandatory(checkout):
    project, request, _ = checkout
    (project / 'run.py').write_text('value = 99\n')
    with pytest.raises(ValueError, match='dirty'):
        installer.install_checkout(project, request)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']


def test_clean_prepared_detached_checkout_can_be_maintained(checkout):
    project, request, _ = checkout
    git(project.parent, 'checkout', '--detach', request['old'])
    assert installer.install_checkout(project, request)['head'] == request['target']


def test_divergent_private_bundle_cannot_replace_main(checkout, tmp_path):
    project, request, _ = checkout
    source = tmp_path / 'source'
    policy_bytes = (source / 'GULib-master/scripts/syncmate/deployment.json').read_bytes()
    git(source, 'switch', '--orphan', 'unrelated')
    path = source / 'GULib-master/scripts/syncmate/deployment.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(policy_bytes)
    git(source, 'add', '.')
    git(source, 'commit', '-m', 'unrelated history')
    bundle = tmp_path / 'divergent.bundle'
    # Advertise main exactly, but make it unrelated to the receiver's old main.
    git(source, 'branch', '-M', 'main')
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main')
    data = bundle.read_bytes()
    bad = {**request, 'target': git(source, 'rev-parse', 'HEAD'),
           'bundle': base64.b64encode(data).decode(), 'bundle_sha256': hashlib.sha256(data).hexdigest()}
    with pytest.raises(subprocess.CalledProcessError):
        installer.install_checkout(project, bad)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']


@pytest.mark.parametrize('change', [
    {**PRIVATE_POLICY, 'schema_version': True},
    {**PRIVATE_POLICY, 'schema_version': 1},
    {**PRIVATE_POLICY, 'require_origin_main': True},
    {**PRIVATE_POLICY, 'transport': 'other'},
    {**PRIVATE_POLICY, 'targets': {}},
])
def test_unreviewed_policy_is_rejected(tmp_path, change):
    from scripts.syncmate.deployment_policy import deployment_policy
    path = tmp_path / 'scripts/syncmate/deployment.json'
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(change), encoding='utf-8')
    with pytest.raises(ValueError, match='unsupported'):
        deployment_policy(tmp_path)


@pytest.mark.parametrize('change', [
    {'head': 'b'*40}, {'target': 'b'*40}, {'status': 'failed'},
    {'project': '/other/project'}, {'transport': 'accelerated-git'},
    {'policy_sha256': '0'*64}, {'origin_refs_unchanged': False},
    {'bundle_sha256': 'invalid'}, {'bundle_sha256': '0'*64},
])
def test_mismatched_receipt_is_rejected(change):
    from scripts.syncmate.deployment_policy import validate_receipt
    policy = {**PRIVATE_POLICY, 'sha256': 'c'*64}
    receipt = {'node': 'gpu4090', 'ssh': 'autodl-opengu', 'target': 'a'*40, 'head': 'a'*40, 'status': 'installed',
        'project': '/autodl-fs/data/OpenGU/GULib-master', 'transport': 'private-bundle',
        'policy_sha256': 'c'*64, 'origin_refs_unchanged': True, 'bundle_sha256': 'd'*64}
    expected = {'python_executable': sys.executable, 'core_dependency_sha256': 'e'*64, 'control_dependency_sha256': 'f'*64}
    receipt.update(expected_environment=expected, environment={'node_id': 'gpu4090', 'git_sha': 'a'*40, 'requested_python': sys.executable, 'python_executable': sys.executable, 'core_dependency_sha256': 'e'*64, 'core_payload_verified': True, 'control_dependency_sha256': 'f'*64, 'control_payload_verified': True})
    validate_receipt(receipt, 'gpu4090', 'a'*40, policy, expected_environment=expected, bundle_sha256='d'*64)
    with pytest.raises(ValueError):
        validate_receipt({**receipt, **change}, 'gpu4090', 'a'*40, policy, expected_environment=expected, bundle_sha256='d'*64)


def test_private_policy_identity_survives_windows_checkout_endings(tmp_path):
    from scripts.syncmate.deployment_policy import deployment_policy
    path = tmp_path / 'scripts/syncmate/deployment.json'
    path.parent.mkdir(parents=True)
    raw = json.dumps(PRIVATE_POLICY, indent=2).encode()
    path.write_bytes(raw)
    expected = deployment_policy(tmp_path)
    path.write_bytes(raw.replace(b'\n', b'\r\n'))
    assert deployment_policy(tmp_path) == expected


def test_receipt_must_be_a_mapping():
    from scripts.syncmate.deployment_policy import validate_receipt
    with pytest.raises(ValueError, match='must be an object'):
        validate_receipt([], 'gpu4090', 'a'*40, {**PRIVATE_POLICY, 'sha256': 'c'*64}, expected_environment={})


def test_legacy_initialize_action_is_removed():
    from scripts.syncmate import install
    with pytest.raises(SystemExit) as result:
        install.main(['initialize', '--node', 'gpu4090-2'])
    assert result.value.code == 2


def test_same_sha_receipts_are_node_and_environment_bound(tmp_path):
    root = Path(__file__).resolve().parents[1]
    import shutil
    folder = tmp_path / 'scripts/syncmate'
    folder.mkdir(parents=True)
    for name in ('deployment.json', 'core_dependency.json', 'control_dependency.json'):
        shutil.copyfile(root / 'scripts/syncmate' / name, folder / name)
    policy = deployment_policy(tmp_path)
    _, digest = dependency_pin(tmp_path)
    sha = 'a'*40
    _, control_digest = dependency_pin(tmp_path, 'control_dependency.json')
    expected = {'python_executable': sys.executable, 'core_dependency_sha256': digest, 'control_dependency_sha256': control_digest}
    old = policy['targets']['gpu4090']
    value = {'node': 'gpu4090', 'ssh': old['ssh'], 'project': old['repo_path'],
        'target': sha, 'head': sha, 'status': 'installed', 'transport': 'private-bundle',
        'policy_sha256': policy['sha256'], 'bundle_sha256': 'd'*64, 'origin_refs_unchanged': True,
        'expected_environment': expected, 'environment': {'node_id': 'gpu4090', 'git_sha': sha,
        'requested_python': sys.executable, 'python_executable': sys.executable,
        'core_dependency_sha256': digest, 'core_payload_verified': True,
        'control_dependency_sha256': control_digest, 'control_payload_verified': True}}
    original = receipt_path(tmp_path, 'gpu4090', sha, policy)
    original.parent.mkdir(parents=True)
    original.write_text(json.dumps(value), encoding='utf-8')
    new_peer = {'role': 'runner', 'transport': 'ssh', 'python_executable': sys.executable, **policy['targets']['gpu4090-2']}
    with pytest.raises(ValueError, match='receipt is missing'):
        installation_receipt(tmp_path, 'gpu4090-2', sha, policy, peer=new_peer)
    second = receipt_path(tmp_path, 'gpu4090-2', sha, policy)
    second.parent.mkdir(parents=True)
    second.write_bytes(original.read_bytes())
    with pytest.raises(ValueError, match='receipt is not successful'):
        installation_receipt(tmp_path, 'gpu4090-2', sha, policy, peer=new_peer)
    value.update(node='gpu4090-2', ssh=new_peer['ssh'])
    second.write_text(json.dumps(value), encoding='utf-8')
    with pytest.raises(ValueError, match='node environment'):
        installation_receipt(tmp_path, 'gpu4090-2', sha, policy, peer=new_peer)


@pytest.mark.parametrize('change', [
    {'node': 'unknown'}, {'ssh': 'autodl-opengu'},
    {'project': '/autodl-fs/data/OpenGU-2/GULib-master'},
])
def test_remote_entry_rejects_wrong_node_alias_or_retired_checkout(change, monkeypatch):
    request = {'node': 'gpu4090-2', 'ssh': 'autodl-opengu-2',
               'project': '/autodl-fs/data/OpenGU/GULib-master', **change}
    def forbidden(*args):
        raise AssertionError('invalid registered address reached Git')
    monkeypatch.setattr(installer, 'git', forbidden)
    with pytest.raises(ValueError, match='registered SSH node'):
        installer.install(request)


@pytest.fixture
def local_transport(checkout, tmp_path, monkeypatch):
    """Only SSH address translation is a fixture; Git/Core/workers remain real."""
    from scripts.syncmate import install as client
    project, request, protected = checkout
    source = tmp_path / 'source/GULib-master'
    monkeypatch.setattr(client, 'ROOT', source)
    policy = deployment_policy(source)
    peers = {node: {'role': 'runner', 'transport': 'ssh', 'python_executable': sys.executable, **target}
             for node, target in policy['targets'].items()}
    import yaml
    config = source / '.syncmate/device.yaml'
    config.parent.mkdir(exist_ok=True)
    config.write_text(yaml.safe_dump({'version': 1, 'device_id': 'fixture-collector',
        'role': 'collector', 'repo_path': str(source), 'peers': peers}), encoding='utf-8')
    calls = []
    def transport(peer, supplied):
        supplied = dict(supplied)
        node, action = supplied['node'], supplied['action']
        assert peer == peers[node]
        assert supplied['ssh'] == peers[node]['ssh']
        calls.append((node, action))
        result = isolated_node(project, supplied, action)
        # Translate only the disposable filesystem address, as an SSH mount does.
        return {**result, 'project': peer['repo_path']}
    monkeypatch.setattr(client, 'invoke', transport)
    return client, project, source, request, protected, peers, calls


@pytest.mark.parametrize('condition', ['busy', 'unknown'])
def test_all_registered_nodes_block_shared_update(local_transport, condition):
    client, project, source, request, protected, peers, calls = local_transport
    with context.use(project, node_id='gpu4090-2'):
        if condition == 'unknown':
            lock = queue.runner_agent_lock_dir()
            lock.mkdir()
            (lock / 'owner.json').write_text('{}', encoding='utf-8')
        else:
            import yaml
            from syncmate_core.contracts import Recipe, build_job_envelope, sha256_text
            recipe = Recipe(id='fixed-fixture', argv=('{python}', 'run.py'), config_path='run.py',
                config_sha256=sha256_text((project / 'run.py').read_text(encoding='utf-8')),
                timeout_seconds=30, expected_artifact_paths=())
            job = build_job_envelope(recipe, project, job_id='waiting', git_state={'clean': True, 'sha': request['old']})
            queue.runner_queue_job_path('inbox', 'waiting').write_text(yaml.safe_dump(dict(job)), encoding='utf-8')
        assert maintenance.node_status()['status'] == condition
    assert client.deploy('gpu4090') == 1
    assert calls == [('gpu4090','inspect'), ('gpu4090-2','inspect')]
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']
    assert protected.read_bytes() == b'untouched-cache'
    assert not list((source / '.workblock/runtime/install').glob('*/*/receipt.json'))
    with context.use(project, node_id='gpu4090-2'):
        assert (queue.runner_agent_lock_dir() if condition == 'unknown' else queue.runner_queue_job_path('inbox','waiting')).exists()


def test_shared_code_is_updated_once_and_both_receipts_are_independent(local_transport):
    client, project, source, request, protected, peers, calls = local_transport
    before = installer.origin_refs(project.parent)
    assert client.deploy('gpu4090') == 0
    assert calls.count(('gpu4090','apply')) == 1
    assert not any(action == 'restore' for _,action in calls)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['target']
    assert installer.origin_refs(project.parent) == before
    assert protected.read_bytes() == b'untouched-cache'
    policy = deployment_policy(source)
    for node in peers:
        proof = installation_receipt(source, node, request['target'], policy, peer=peers[node])
        value = json.loads(Path(proof['path']).read_text(encoding='utf-8'))
        assert value['node'] == value['environment']['node_id'] == node
        assert value['ssh'] == peers[node]['ssh']
        assert value['coordinator'] == 'gpu4090'
        assert value['registered_nodes'] == sorted(peers)
    assert not (project / '.syncmate/runner_queue').exists()


def test_each_idle_worker_is_restored_via_its_own_node(local_transport):
    client, project, source, request, protected, peers, calls = local_transport
    workers = {}
    try:
        for node in peers:
            workers[node] = subprocess.Popen([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
                '--node-id', node, 'runner-agent', 'serve', '--poll-seconds','1'], cwd=project,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for node in peers:
            with context.use(project, node_id=node):
                deadline = time.monotonic()+10
                while time.monotonic()<deadline:
                    owner = queue.runner_queue_load_json(queue.runner_agent_lock_dir()/'owner.json')
                    if owner.get('node_id') == node and owner.get('restartable') is True:
                        break
                    time.sleep(.05)
                else:
                    pytest.fail('temporary node worker did not initialize')
        assert client.deploy('gpu4090') == 0
        assert calls.count(('gpu4090','apply')) == 1
        assert [(n,a) for n,a in calls if a=='restore'] == [(n,'restore') for n in sorted(peers)]
        for node, worker in workers.items():
            worker.wait(timeout=10)
            with context.use(project, node_id=node):
                owner = queue.runner_queue_load_json(queue.runner_agent_lock_dir()/'owner.json')
                assert owner['node_id'] == node and owner['pid'] != worker.pid
            path = receipt_path(source,node,request['target'],deployment_policy(source))
            receipt = json.loads(path.read_text(encoding='utf-8'))
            assert receipt['restoration']['pid'] == owner['pid']
            assert receipt['restoration']['environment']['node_id'] == node
    finally:
        with context.use(project, node_id='gpu4090'):
            with maintenance.installation(node_ids=list(peers),timeout=10):
                pass
        for worker in workers.values():
            worker.wait(timeout=10)


@pytest.mark.parametrize('phase', ['before', 'after'])
def test_other_nodes_actual_corrupt_core_cannot_borrow_coordinator_environment(local_transport, tmp_path, monkeypatch, phase):
    import os
    import shutil
    import syncmate_core
    client, project, source, request, protected, peers, calls = local_transport
    variant = tmp_path / 'other-environment'
    package_root = Path(syncmate_core.__file__).resolve().parent.parent
    # A second isolated import environment, not an installed-package mutation.
    shutil.copytree(package_root / 'syncmate_core', variant / 'syncmate_core')
    for info in package_root.glob('syncmate-*.dist-info'):
        shutil.copytree(info, variant / info.name)
    shutil.copyfile(package_root / 'syncmate.py', variant / 'syncmate.py')
    file = variant / 'syncmate_core/readiness.py'
    file.write_bytes(file.read_bytes() + b'\n# corrupt controlled payload\n')
    original = client.invoke
    def transport(peer, supplied):
        changed = (phase == 'before' or git(project.parent, 'rev-parse', 'HEAD') == request['target'])
        if supplied['node'] != 'gpu4090-2' or supplied['action'] != 'inspect' or not changed:
            return original(peer, supplied)
        calls.append((supplied['node'], supplied['action']))
        env = dict(os.environ)
        env['PYTHONPATH'] = str(variant) + os.pathsep + env.get('PYTHONPATH', '')
        code = ('import json,sys; from pathlib import Path; '
                'from scripts.syncmate.install_remote import inspect_checkout; '
                'request=json.load(sys.stdin); '
                'print(json.dumps(inspect_checkout(Path(sys.argv[1]),request)))')
        result = subprocess.run([sys.executable, '-B', '-c', code, str(project)],
            input=json.dumps(supplied), cwd=source, env=env, capture_output=True, text=True, encoding='utf-8')
        assert result.returncode != 0 and 'installed dependency payload differs: syncmate_core/readiness.py' in result.stderr
        raise ValueError('gpu4090-2 actual isolated Core payload mismatch')
    monkeypatch.setattr(client, 'invoke', transport)
    assert client.deploy('gpu4090') == 1
    assert git(project.parent, 'rev-parse', 'HEAD') == (request['old'] if phase == 'before' else request['target'])
    assert calls.count(('gpu4090','apply')) == (0 if phase == 'before' else 1)
    assert not any(action=='restore' for _,action in calls)
    assert not list((source / '.workblock/runtime/install').glob('*/*/receipt.json'))
    assert protected.read_bytes() == b'untouched-cache'


def test_local_core_mismatch_blocks_before_any_peer_probe(local_transport):
    client,project,source,request,protected,peers,calls=local_transport
    pin=source/'scripts/syncmate/core_dependency.json'
    value=json.loads(pin.read_text(encoding='utf-8'))
    value['version']='unverified-version'
    pin.write_text(json.dumps(value),encoding='utf-8')
    git(source, 'add', str(pin))
    git(source, 'commit', '-m', 'unverified dependency')
    with pytest.raises(ValueError,match='local control environment is unverified'):
        client.deploy('gpu4090')
    assert calls==[] and git(project.parent,'rev-parse','HEAD')==request['old']
