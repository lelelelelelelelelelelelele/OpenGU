"""Real fast-forward Git installation in disposable repositories; no SSH/GPU."""
import base64
import subprocess
import sys
import time
from pathlib import Path
import pytest
from scripts.syncmate import install_remote as installer
from syncmate_core import context, maintenance, queue


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
    git(source, 'commit', '-am', 'target')
    target = git(source, 'rev-parse', 'HEAD')
    bundle = tmp_path / 'update.bundle'
    git(source, 'bundle', 'create', str(bundle), 'refs/heads/main', '^' + old)
    protected = remote / 'GULib-master/data/cache.bin'
    protected.parent.mkdir()
    protected.write_bytes(b'untouched-cache')
    return remote / 'GULib-master', {'old': old, 'target': target,
        'bundle': base64.b64encode(bundle.read_bytes()).decode()}, protected


@pytest.mark.parametrize('transport', ['fetch', 'bundle', 'timeout'])
def test_exact_install_preserves_ignored_cache(checkout, monkeypatch, transport):
    project, request, protected = checkout
    def fetch(repo):
        if transport != 'fetch':
            return 124 if transport == 'timeout' else 1
        git(repo, 'fetch', 'origin', 'refs/heads/main')
        return 0
    monkeypatch.setattr(installer, 'accelerated_fetch', fetch)
    result = installer.install_checkout(project, request)
    assert result['status'] == 'installed'
    assert result['head'] == request['target']
    assert result['runner_was_active'] is False
    assert protected.read_bytes() == b'untouched-cache'
    assert not list((project.parent / '.git').glob('install-*.bundle'))
    repeated = installer.install_checkout(project, {**request, 'old': request['target']})
    assert repeated['status'] == 'already_installed'


def test_busy_install_does_not_fetch_or_modify(checkout, monkeypatch):
    project, request, _ = checkout
    monkeypatch.setattr(installer, 'accelerated_fetch', lambda *a: pytest.fail('busy install fetched'))
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
    monkeypatch.setattr(installer, 'accelerated_fetch', lambda repo: (git(repo, 'fetch', 'origin', 'main'), 0)[1])
    request['target'] = 'a' * 40
    with pytest.raises(ValueError, match='different target'):
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
        monkeypatch.setattr(installer, 'accelerated_fetch', lambda *args: 1)
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
