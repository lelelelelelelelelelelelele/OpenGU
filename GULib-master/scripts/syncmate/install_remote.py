"""Fixed SSH-side private Git actions. Receives data, never caller commands."""
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

# This standalone program is sent to the selected host before new code exists.
# Its address allowlist must agree with the reviewed deployment.json.
PRIVATE_POLICY = {
    'schema_version': 2, 'transport': 'private-bundle', 'require_origin_main': False,
    'targets': {
        'gpu4090': {'ssh': 'autodl-opengu', 'repo_path': '/autodl-fs/data/OpenGU/GULib-master'},
        'gpu4090-2': {'ssh': 'autodl-opengu-2', 'repo_path': '/autodl-fs/data/OpenGU-2/GULib-master'},
    },
}
PROTECTED = ['GULib-master/' + p for p in (
    'data', 'results/cache', 'results/selection_cache', 'results/score_cache',
    'results/cache_v2', 'results/runs', 'experiments/archive')]


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


def protected_path(path):
    return any(path == p or path.startswith(p + '/') or p.startswith(path + '/') for p in PROTECTED)


def check_paths(repo, old, target):
    paths = [p for p in git(repo, 'diff', '--name-only', '-z', '--no-renames', old, target).split('\0') if p]
    for path in paths:
        if protected_path(path):
            raise ValueError('update touches protected payload: ' + path)
    return paths


def origin_refs(repo):
    return git(repo, 'for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes/origin/')


def check_policy(repo, target, expected_hash):
    raw = subprocess.check_output(['git', '-C', str(repo), 'show',
                                   target + ':GULib-master/scripts/syncmate/deployment.json'])
    value = json.loads(raw.decode('utf-8'))
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    if (hashlib.sha256(canonical).hexdigest() != expected_hash or value != PRIVATE_POLICY
            or type(value.get('schema_version')) is not int or type(value.get('require_origin_main')) is not bool):
        raise ValueError('target deployment policy mismatch')


def check_request(request, *, initialize=False):
    identities = [request.get('target')]
    if not initialize:
        identities.append(request.get('old'))
    elif request.get('old') is not None:
        raise ValueError('initialization must not replace an old checkout')
    if any(not isinstance(v, str) or not re.fullmatch('[0-9a-f]{40}', v) for v in identities):
        raise ValueError('full Git identities required')
    if (request.get('transport') != 'private-bundle'
            or not re.fullmatch('[0-9a-f]{64}', request.get('policy_sha256') or '')):
        raise ValueError('explicit private-bundle policy required')


def check_not_linked(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('registered project must not use symlinks')


def result_binding(project, request):
    return {'node': request['node'], 'ssh': request['ssh'], 'project': str(project),
            'target': request['target'], 'transport': 'private-bundle',
            'policy_sha256': request['policy_sha256']}


def import_bundle(repo, request):
    bundle = repo / '.git' / ('install-' + uuid.uuid4().hex + '.bundle')
    try:
        data = base64.b64decode(request['bundle'], validate=True)
        if hashlib.sha256(data).hexdigest() != request.get('bundle_sha256'):
            raise ValueError('bundle SHA-256 mismatch')
        bundle.write_bytes(data)
        subprocess.run(['git', '-C', str(repo), 'bundle', 'verify', str(bundle)], check=True, capture_output=True)
        if git(repo, 'bundle', 'list-heads', str(bundle)).splitlines() != [request['target'] + ' refs/heads/main']:
            raise ValueError('bundle target or advertised refs mismatch')
        subprocess.run(['git', '-C', str(repo), 'fetch', '--no-tags', str(bundle), 'refs/heads/main'],
                       check=True, capture_output=True)
        if git(repo, 'rev-parse', 'FETCH_HEAD') != request['target']:
            raise ValueError('bundle target mismatch')
        check_policy(repo, request['target'], request['policy_sha256'])
    finally:
        bundle.unlink(missing_ok=True)


def install(request):
    registered = PRIVATE_POLICY['targets'].get(request.get('node'))
    if (registered is None or request.get('ssh') != registered['ssh']
            or request.get('project') != registered['repo_path']):
        raise ValueError('not the registered SSH node, alias and project')
    project = Path(request['project'])
    check_not_linked(project)
    if request.get('action') == 'initialize':
        return initialize_checkout(project, request)
    if request.get('action') != 'apply':
        raise ValueError('explicit apply or initialize action required')
    repo = project.parent
    if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo.resolve():
        raise ValueError('unexpected Git root')
    return install_checkout(project, request)


def initialize_checkout(project, request):
    """Create only a previously absent repository; partial failure is preserved."""
    check_request(request, initialize=True)
    check_not_linked(project)
    repo = project.parent
    if repo.exists():
        raise ValueError('initialization requires a new absent repository directory')
    if not repo.parent.is_dir():
        raise ValueError('registered repository parent must already exist')
    repo.mkdir()  # Exclusive creation also rejects a concurrent initializer.
    subprocess.run(['git', 'init', '-b', 'main', str(repo)], check=True, capture_output=True)
    before_origin = origin_refs(repo)
    import_bundle(repo, request)
    target = request['target']
    paths = [p for p in git(repo, 'ls-tree', '-r', '--name-only', '-z', target).split('\0') if p]
    for path in paths:
        if protected_path(path) or path.startswith('GULib-master/.syncmate/'):
            raise ValueError('initialization tree contains runtime payload: ' + path)
    subprocess.run(['git', '-C', str(repo), 'checkout', '-b', 'main', target], check=True, capture_output=True)
    check_tree(repo, target)
    # Runner setup is the sole ignored local addition. No datasets or runtime jobs.
    device = project / '.syncmate/device.yaml'
    subprocess.run(['git', '-C', str(repo), 'check-ignore', '-q', 'GULib-master/.syncmate/device.yaml'], check=True)
    device.parent.mkdir()
    with device.open('x', encoding='utf-8') as handle:
        json.dump({'version': 1, 'device_id': request['node'], 'role': 'runner',
                   'repo_path': str(project), 'execution_device': 'cuda:0', 'peers': {}}, handle, indent=2)
        handle.write('\n')
    check_tree(repo, target)
    if origin_refs(repo) != before_origin or git(repo, 'remote'):
        raise ValueError('initialization changed origin refs or added a remote')
    return {**result_binding(project, request), 'status': 'initialized', 'head': target,
            'bundle_sha256': request['bundle_sha256'], 'origin_refs_unchanged': True,
            'runner_device_config': str(device), 'runner_started': False}


def install_checkout(project, request):
    """Exact existing-checkout update; the CLI validates the registered address."""
    check_request(request)
    repo = project.parent
    target, old = request['target'], request['old']
    before_origin = origin_refs(repo)
    if check_tree(repo) != old:
        raise ValueError('runner version changed since bundle preparation')
    if old == target:
        check_policy(repo, target, request['policy_sha256'])
        return {**result_binding(project, request), 'status': 'already_installed', 'head': old,
                'origin_refs_unchanged': origin_refs(repo) == before_origin}
    sys.path.insert(0, str(project))
    from syncmate_core import context
    from syncmate_core.maintenance import installation
    result = {**result_binding(project, request), 'old': old, 'status': 'failed', 'runner_restored': False}
    with context.use(project):
        with installation() as state:
            result['runner_was_active'] = state['restart']
            check_tree(repo, old)
            import_bundle(repo, request)
            result['bundle_sha256'] = request['bundle_sha256']
            subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', old, target], check=True)
            paths = check_paths(repo, old, target)
            result['changed_paths'] = paths
            subprocess.run(['git', '-C', str(repo), 'merge', '--ff-only', target], check=True, capture_output=True)
            check_tree(repo, target)
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
        project = Path(request.get('project') or '.')
        try:
            head = git(project.parent, 'rev-parse', 'HEAD')
        except Exception:
            head = None
        result = {'status': 'failed', 'node': request.get('node'), 'ssh': request.get('ssh'),
                  'project': str(project), 'target': request.get('target'), 'head': head,
                  'transport': request.get('transport'), 'policy_sha256': request.get('policy_sha256'),
                  'error': str(exc) if isinstance(exc, (ValueError, RuntimeError)) else type(exc).__name__,
                  'runner_lock_present': (project / '.syncmate/runner_queue/agent.lock').exists(),
                  'maintenance_present': (project / '.syncmate/runner_queue/maintenance.json').exists()}
    print(json.dumps(result))
    return 0 if result['status'] in ('initialized', 'installed', 'already_installed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
