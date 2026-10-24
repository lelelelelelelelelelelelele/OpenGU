"""Real fast-forward Git installation in disposable repositories; no SSH/GPU."""
import base64
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
import pytest
from scripts.syncmate import install_remote as installer
from syncmate_core import context, maintenance, queue
from scripts.syncmate.deployment_policy import PRIVATE_POLICY, deployment_policy, installation_receipt, receipt_path, validate_peer, validate_receipt


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


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
    git(source, 'add', str(policy))
    git(source, 'commit', '-am', 'target')
    target = git(source, 'rev-parse', 'HEAD')
    bundle = tmp_path / 'update.bundle'
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main', '^' + old)
    protected = remote / 'GULib-master/data/cache.bin'
    protected.parent.mkdir()
    protected.write_bytes(b'untouched-cache')
    return remote / 'GULib-master', {'old': old, 'target': target, 'node': 'gpu4090', 'ssh': 'autodl-opengu',
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
    assert result['runner_was_active'] is False
    assert protected.read_bytes() == b'untouched-cache'
    assert not list((project.parent / '.git').glob('install-*.bundle'))
    repeated = installer.install_checkout(project, {**request, 'old': request['target']})
    assert repeated['status'] == 'already_installed'
    assert any('fetch' in argv for argv in commands)


def test_busy_install_does_not_fetch_or_modify(checkout, monkeypatch):
    project, request, _ = checkout
    with context.use(project):
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
    with context.use(project):
        assert maintenance.marker().exists()


def test_idle_runner_is_stopped_and_restored_after_install(checkout, monkeypatch):
    project, request, _ = checkout
    device = project / '.syncmate/device.yaml'
    device.parent.mkdir(exist_ok=True)
    import yaml
    device.write_text(yaml.safe_dump({'version': 1, 'device_id': 'test', 'role': 'runner',
                                     'repo_path': str(project), 'peers': {}}))
    worker = subprocess.Popen([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
        'runner-agent', 'serve', '--poll-seconds', '1'], cwd=project,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        with context.use(project):
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if queue.runner_queue_load_json(queue.runner_agent_lock_dir() / 'owner.json').get('restartable'):
                    break
                time.sleep(.05)
            else:
                pytest.fail('test runner did not start')
        result = installer.install_checkout(project, request)
        assert result['runner_was_active'] and result['runner_restored']
        assert result['status'] == 'installed'
        worker.wait(timeout=10)
    finally:
        if worker.poll() is None:
            worker.terminate()
            worker.wait(timeout=10)
        with context.use(project):
            if queue.runner_agent_lock_dir().exists():
                with maintenance.installation(timeout=10):
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


@pytest.mark.parametrize('condition', ['dirty', 'branch'])
def test_remote_clean_main_is_mandatory(checkout, condition):
    project, request, _ = checkout
    if condition == 'dirty':
        (project / 'run.py').write_text('value = 99\n')
    else:
        git(project.parent, 'switch', '-c', 'other')
    with pytest.raises(ValueError, match='dirty|main'):
        installer.install_checkout(project, request)
    assert git(project.parent, 'rev-parse', 'HEAD') == request['old']


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
    validate_receipt(receipt, 'gpu4090', 'a'*40, policy, bundle_sha256='d'*64)
    with pytest.raises(ValueError):
        validate_receipt({**receipt, **change}, 'gpu4090', 'a'*40, policy, bundle_sha256='d'*64)


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
        validate_receipt([], 'gpu4090', 'a'*40, {**PRIVATE_POLICY, 'sha256': 'c'*64})


def initialization_request(checkout, tmp_path):
    _, request, _ = checkout
    source = tmp_path / 'source'
    bundle = tmp_path / 'initial.bundle'
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main')
    data = bundle.read_bytes()
    return {**request, 'old': None, 'action': 'initialize', 'node': 'gpu4090-2', 'ssh': 'autodl-opengu-2',
            'bundle': base64.b64encode(data).decode(), 'bundle_sha256': hashlib.sha256(data).hexdigest()}


def test_fresh_private_initialization_creates_only_code_and_runner_identity(checkout, tmp_path):
    request = initialization_request(checkout, tmp_path)
    project = tmp_path / 'fresh/GULib-master'
    result = installer.initialize_checkout(project, request)
    assert result['status'] == 'initialized' and result['node'] == 'gpu4090-2'
    assert result['head'] == request['target'] and result['runner_started'] is False
    assert git(project.parent, 'branch', '--show-current') == 'main'
    assert git(project.parent, 'rev-parse', 'HEAD') == request['target']
    assert git(project.parent, 'remote') == ''
    assert installer.origin_refs(project.parent) == ''
    import yaml
    from syncmate_core import devices
    with context.use(project):
        device, warnings = devices.load_device(project / '.syncmate/device.yaml')
    assert not warnings and device['device_id'] == 'gpu4090-2'
    assert device['role'] == 'runner' and device['execution_device'] == 'cuda:0'
    assert list((project / '.syncmate').iterdir()) == [project / '.syncmate/device.yaml']
    assert not (project / 'data').exists() and not (project / 'results').exists()
    assert git(project.parent, 'status', '--porcelain=v1', '-uall') == ''
    assert not list((project.parent / '.git').glob('install-*.bundle'))
    before = (project / 'run.py').read_bytes()
    with pytest.raises(ValueError, match='new absent'):
        installer.initialize_checkout(project, request)
    assert (project / 'run.py').read_bytes() == before


@pytest.mark.parametrize('kind', ['empty_directory', 'populated_directory', 'file'])
def test_initialization_never_reuses_an_existing_target(checkout, tmp_path, kind):
    request = initialization_request(checkout, tmp_path)
    repo = tmp_path / 'occupied'
    if kind == 'file':
        repo.write_bytes(b'owned')
    else:
        repo.mkdir()
        if kind == 'populated_directory':
            (repo / 'owner').write_bytes(b'owned')
    before = repo.read_bytes() if kind == 'file' else sorted(p.name for p in repo.iterdir())
    with pytest.raises(ValueError, match='new absent'):
        installer.initialize_checkout(repo / 'GULib-master', request)
    assert (repo.read_bytes() if kind == 'file' else sorted(p.name for p in repo.iterdir())) == before


def test_initialization_rejects_symlink_ancestor(checkout, tmp_path):
    request = initialization_request(checkout, tmp_path)
    real = tmp_path / 'real'
    real.mkdir()
    linked = tmp_path / 'linked'
    try:
        linked.symlink_to(real, target_is_directory=True)
    except OSError:
        pytest.skip('host does not permit creation of a symlink fixture')
    with pytest.raises(ValueError, match='symlinks'):
        installer.initialize_checkout(linked / 'fresh/GULib-master', request)
    assert not list(real.iterdir())


@pytest.mark.parametrize('condition', ['wrong_digest', 'incremental_bundle'])
def test_initialization_rejects_bad_or_non_self_contained_bundle(checkout, tmp_path, condition):
    request = initialization_request(checkout, tmp_path)
    if condition == 'wrong_digest':
        request['bundle_sha256'] = '0'*64
    else:
        # Existing update bundle has prerequisites and cannot initialize a new repo.
        request.update(bundle=checkout[1]['bundle'], bundle_sha256=checkout[1]['bundle_sha256'])
    project = tmp_path / 'failed/GULib-master'
    with pytest.raises((ValueError, subprocess.CalledProcessError)):
        installer.initialize_checkout(project, request)
    assert not project.exists()
    assert (project.parent / '.git').is_dir()  # Truthful partial failure, no silent retry.
    assert not list((project.parent / '.git').glob('install-*.bundle'))


def test_initialization_refuses_tracked_runtime_payload(checkout, tmp_path):
    source = tmp_path / 'source'
    payload = source / 'GULib-master/data/forbidden.bin'
    payload.parent.mkdir()
    payload.write_bytes(b'not-code')
    git(source, 'add', '-f', str(payload))
    git(source, 'commit', '-m', 'forbidden runtime payload')
    request = initialization_request(checkout, tmp_path)
    request['target'] = git(source, 'rev-parse', 'HEAD')
    with pytest.raises(ValueError, match='runtime payload'):
        installer.initialize_checkout(tmp_path / 'fresh/GULib-master', request)
    assert not (tmp_path / 'fresh/GULib-master').exists()


@pytest.mark.parametrize('change', [
    {'node': 'unknown'}, {'ssh': 'autodl-opengu'},
    {'project': '/autodl-fs/data/OpenGU/GULib-master'},
    {'project': '/autodl-fs/data/OpenGU-2/../OpenGU/GULib-master'},
])
def test_remote_entry_rejects_node_alias_path_mismatch_before_git(change, monkeypatch):
    request = {'node': 'gpu4090-2', 'ssh': 'autodl-opengu-2',
               'project': '/autodl-fs/data/OpenGU-2/GULib-master', **change}
    def forbidden(*args):
        raise AssertionError('invalid address reached Git')
    monkeypatch.setattr(installer, 'git', forbidden)
    with pytest.raises(ValueError, match='registered SSH node'):
        installer.install(request)


def test_same_sha_receipt_cannot_authorize_the_other_node(tmp_path):
    import shutil
    path = tmp_path / 'scripts/syncmate/deployment.json'
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(PRIVATE_POLICY), encoding='utf-8')
    policy = deployment_policy(tmp_path)
    sha = 'a'*40
    old = policy['targets']['gpu4090']
    receipt = {'node': 'gpu4090', 'ssh': old['ssh'], 'project': old['repo_path'],
        'target': sha, 'head': sha, 'status': 'installed', 'transport': 'private-bundle',
        'policy_sha256': policy['sha256'], 'bundle_sha256': 'd'*64, 'origin_refs_unchanged': True}
    original = receipt_path(tmp_path, 'gpu4090', sha, policy)
    original.parent.mkdir(parents=True)
    original.write_text(json.dumps(receipt), encoding='utf-8')
    peer = {'role': 'runner', 'transport': 'ssh', **policy['targets']['gpu4090-2']}
    with pytest.raises(ValueError, match='receipt is missing'):
        installation_receipt(tmp_path, 'gpu4090-2', sha, policy, peer=peer)
    wrong = receipt_path(tmp_path, 'gpu4090-2', sha, policy)
    wrong.parent.mkdir(parents=True)
    shutil.copyfile(original, wrong)
    with pytest.raises(ValueError, match='receipt is not successful'):
        installation_receipt(tmp_path, 'gpu4090-2', sha, policy, peer=peer)
    assert installation_receipt(tmp_path, 'gpu4090', sha, policy,
        peer={'role': 'runner', 'transport': 'ssh', **old})['node'] == 'gpu4090'


@pytest.mark.parametrize('key', ['ssh', 'repo_path'])
def test_selected_peer_cannot_route_new_node_to_old_address(key):
    policy = {**PRIVATE_POLICY, 'sha256': 'c'*64}
    peer = {'role': 'runner', 'transport': 'ssh', **policy['targets']['gpu4090-2']}
    peer[key] = policy['targets']['gpu4090'][key]
    with pytest.raises(ValueError, match='alias and project'):
        validate_peer(peer, 'gpu4090-2', policy)


def test_standalone_remote_allowlist_matches_reviewed_policy():
    assert installer.PRIVATE_POLICY == PRIVATE_POLICY
