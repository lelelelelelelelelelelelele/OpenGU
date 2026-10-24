"""Fixed SSH-side Git installation action. Receives data, never caller commands."""
import base64
import json
import hashlib
from pathlib import Path
import re
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


def origin_refs(repo):
    return git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes/origin/')


def check_policy(repo, target, expected_hash):
    raw = subprocess.check_output(['git', '-C', str(repo), 'show',
                                   target + ':GULib-master/scripts/syncmate/deployment.json'])
    expected = {'schema_version': 1, 'transport': 'private-bundle', 'require_origin_main': False}
    value = json.loads(raw.decode('utf-8'))
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    if (hashlib.sha256(canonical).hexdigest() != expected_hash or value != expected
            or type(value.get('schema_version')) is not int or type(value.get('require_origin_main')) is not bool):
        raise ValueError('target deployment policy mismatch')


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
    if request.get('transport') != 'private-bundle' or not re.fullmatch('[0-9a-f]{64}', request.get('policy_sha256') or ''):
        raise ValueError('explicit private-bundle policy required')
    before_origin = origin_refs(repo)
    if check_tree(repo) != old:
        raise ValueError('runner version changed since bundle preparation')
    if old == target:
        check_policy(repo, target, request['policy_sha256'])
        return {'status': 'already_installed', 'target': target, 'head': old, 'project': str(project),
                'transport': 'private-bundle', 'policy_sha256': request['policy_sha256'],
                'origin_refs_unchanged': origin_refs(repo) == before_origin}
    sys.path.insert(0, str(project))
    # Installed Core must expose maintenance; no unsafe stop/kill fallback.
    from syncmate_core import context
    from syncmate_core.maintenance import installation
    result = {'target': target, 'old': old, 'project': str(project), 'status': 'failed', 'runner_restored': False}
    with context.use(project):
        with installation() as state:
            result['runner_was_active'] = state['restart']
            check_tree(repo, old)
            bundle = repo / '.git' / ('install-' + uuid.uuid4().hex + '.bundle')
            try:
                data = base64.b64decode(request['bundle'], validate=True)
                if hashlib.sha256(data).hexdigest() != request.get('bundle_sha256'):
                    raise ValueError('bundle SHA-256 mismatch')
                bundle.write_bytes(data)
                subprocess.run(['git', '-C', str(repo), 'bundle', 'verify', str(bundle)],
                               check=True, capture_output=True)
                heads = git(repo, 'bundle', 'list-heads', str(bundle)).splitlines()
                if heads != [target + ' refs/heads/main']:
                    raise ValueError('bundle target or advertised refs mismatch')
                # Fetch only into FETCH_HEAD; never write public origin tracking refs.
                subprocess.run(['git', '-C', str(repo), 'fetch', '--no-tags', str(bundle), 'refs/heads/main'],
                               check=True, capture_output=True)
                if git(repo, 'rev-parse', 'FETCH_HEAD') != target:
                    raise ValueError('bundle target mismatch')
                check_policy(repo, target, request['policy_sha256'])
            finally:
                bundle.unlink(missing_ok=True)
            result.update(transport='private-bundle', bundle_sha256=request['bundle_sha256'],
                          policy_sha256=request['policy_sha256'])
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
            if origin_refs(repo) != before_origin:
                raise ValueError('origin tracking refs changed')
            result.update(head=target, status='installed', origin_refs_unchanged=True)
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
