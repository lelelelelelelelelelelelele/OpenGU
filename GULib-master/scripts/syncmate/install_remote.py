"""Fixed SSH-side Git installation action. Receives data, never caller commands."""
import base64
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import uuid


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def check_tree(repo, target=None):
    if git(repo, 'branch', '--show-current') != 'main':
        raise ValueError('remote must be on main')
    if git(repo, 'status', '--porcelain=v1', '--untracked-files=all'):
        raise ValueError('remote working tree is dirty')
    head = git(repo, 'rev-parse', 'HEAD')
    if target and head != target:
        raise ValueError('remote target mismatch')
    if git(repo, 'worktree', 'list', '--porcelain').count('worktree ') != 1:
        raise ValueError('remote must have one active checkout')
    return head


def check_paths(repo, old, target):
    protected = ['GULib-master/' + p for p in (
        'data', 'results/cache', 'results/selection_cache', 'results/score_cache',
        'results/cache_v2', 'results/runs', 'experiments/archive')]
    paths = [p for p in git(repo, 'diff', '--name-only', '-z', '--no-renames', old, target).split('\0') if p]
    for path in paths:
        if any(path == p or path.startswith(p + '/') or p.startswith(path + '/') for p in protected):
            raise ValueError('update touches protected payload: ' + path)
    return paths


def accelerated_fetch(repo):
    process = subprocess.Popen(['bash', '--noprofile', '--norc', '-c',
        'test -f /etc/network_turbo && test ! -L /etc/network_turbo && test -r /etc/network_turbo && '
        'source /etc/network_turbo >/dev/null 2>&1 && '
        'GIT_TERMINAL_PROMPT=0 git fetch --no-tags origin refs/heads/main:refs/remotes/origin/main'],
        cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        return process.wait(timeout=120)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        return 124


def install(request):
    project = Path(request['project']).resolve()
    if project != Path('/autodl-fs/data/OpenGU/GULib-master'):
        raise ValueError('not the registered SSH project')
    repo = project.parent
    if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo:
        raise ValueError('unexpected Git root')
    return install_checkout(project, request)


def install_checkout(project, request):
    """Project-owned implementation; CLI validates the fixed deployment address."""
    repo = project.parent
    target, old = request['target'], request['old']
    if any(not re.fullmatch('[0-9a-f]{40}', v) for v in (target, old)):
        raise ValueError('full Git identities required')
    if check_tree(repo) != old:
        raise ValueError('runner version changed since bundle preparation')
    if old == target:
        return {'status': 'already_installed', 'target': target, 'head': old}
    sys.path.insert(0, str(project))
    # Installed Core must expose maintenance; no unsafe stop/kill fallback.
    from syncmate_core import context
    from syncmate_core.maintenance import installation
    result = {'target': target, 'old': old, 'status': 'failed', 'runner_restored': False}
    with context.use(project):
        with installation() as state:
            result['runner_was_active'] = state['restart']
            check_tree(repo, old)
            # Acceleration is always sourced before the FIRST network attempt.
            fetch_code = accelerated_fetch(repo)
            result['fetch_exit_code'] = fetch_code
            if fetch_code == 0:
                if git(repo, 'rev-parse', 'FETCH_HEAD') != target:
                    raise ValueError('origin changed; refusing a different target')
                result['transport'] = 'accelerated-git'
            else:
                bundle = repo / '.git' / ('install-' + uuid.uuid4().hex + '.bundle')
                try:
                    bundle.write_bytes(base64.b64decode(request['bundle'], validate=True))
                    subprocess.run(['git', '-C', str(repo), 'bundle', 'verify', str(bundle)],
                                   check=True, capture_output=True)
                    subprocess.run(['git', '-C', str(repo), 'fetch', str(bundle),
                                    'refs/heads/main:refs/remotes/origin/main'],
                                   check=True, capture_output=True)
                    if git(repo, 'rev-parse', 'FETCH_HEAD') != target:
                        raise ValueError('bundle target mismatch')
                finally:
                    bundle.unlink(missing_ok=True)
                result['transport'] = 'bundle'
            subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', old, target], check=True)
            paths = check_paths(repo, old, target)
            result['changed_paths'] = paths
            subprocess.run(['git', '-C', str(repo), 'merge', '--ff-only', target],
                           check=True, capture_output=True)
            check_tree(repo, target)
            # Syntax validation only for changed Python; no imports/cache writes.
            import ast
            for path in paths:
                file = repo / path
                if path.endswith('.py') and file.is_file():
                    ast.parse(file.read_text(encoding='utf-8-sig'), filename=path)
            result.update(head=target, status='installed')
        if state['restart']:
            log = project / '.syncmate/runner-install.log'
            with log.open('ab') as output:
                proc = subprocess.Popen([sys.executable, '-B', 'scripts/syncmate/syncmate.py',
                    'runner-agent', 'serve', '--poll-seconds', str(state['runner']['poll_seconds'])],
                    cwd=project, stdin=subprocess.DEVNULL, stdout=output, stderr=output,
                    start_new_session=True)
            from syncmate_core import queue
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                owner = queue.runner_queue_load_json(queue.runner_agent_lock_dir() / 'owner.json')
                if owner.get('pid') == proc.pid:
                    result['runner_restored'] = True
                    break
                if proc.poll() is not None:
                    break
                time.sleep(.1)
            if not result['runner_restored']:
                result.update(status='failed', error='code installed, runner restoration failed')
    return result


def main():
    request = json.load(sys.stdin)
    try:
        result = install(request)
    except Exception as exc:
        # Do not expose command output, transport/proxy configuration or secrets.
        project = Path(request['project'])
        try:
            head = git(project.parent, 'rev-parse', 'HEAD')
        except Exception:
            head = None
        result = {'status': 'failed', 'target': request.get('target'), 'head': head,
                  'error': str(exc) if isinstance(exc, (ValueError, RuntimeError)) else type(exc).__name__,
                  'runner_lock_present': (project / '.syncmate/runner_queue/agent.lock').exists(),
                  'maintenance_present': (project / '.syncmate/runner_queue/maintenance.json').exists()}
    print(json.dumps(result))
    return 0 if result['status'] in ('installed', 'already_installed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
