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
        'gpu4090-2': {'ssh': 'autodl-opengu-2', 'repo_path': '/autodl-fs/data/OpenGU/GULib-master'},
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


def check_policy(repo, target, expected_hash, expected_core):
    raw = subprocess.check_output(['git', '-C', str(repo), 'show',
                                   target + ':GULib-master/scripts/syncmate/deployment.json'])
    value = json.loads(raw.decode('utf-8'))
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    if (hashlib.sha256(canonical).hexdigest() != expected_hash or value != PRIVATE_POLICY
            or type(value.get('schema_version')) is not int or type(value.get('require_origin_main')) is not bool):
        raise ValueError('target deployment policy mismatch')
    raw_pin = subprocess.check_output(['git', '-C', str(repo), 'show', target + ':GULib-master/scripts/syncmate/core_dependency.json'])
    if canonical_hash(json.loads(raw_pin.decode('utf-8'))) != canonical_hash(expected_core):
        raise ValueError('target Core dependency mismatch')


def check_request(request):
    identities = [request.get('target'), request.get('old')]
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
        check_policy(repo, request['target'], request['policy_sha256'], request['core_dependency'])
    finally:
        bundle.unlink(missing_ok=True)


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def inspect_environment(request):
    """Read this container's interpreter and exact reviewed Core payload."""
    from importlib import metadata
    import platform
    import syncmate_core
    pin = request['core_dependency']
    dist = metadata.distribution(pin['distribution'])
    expected_module = Path(dist.locate_file('syncmate_core/__init__.py')).resolve()
    if (dist.version != pin['version'] or syncmate_core.__version__ != pin['version']
            or Path(syncmate_core.__file__).resolve() != expected_module):
        raise ValueError('node Core distribution or import mismatch')
    expected = {p for p in pin['files'] if p.startswith('syncmate_core/')}
    actual = {p.relative_to(expected_module.parent.parent).as_posix()
              for p in expected_module.parent.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if expected != actual:
        raise ValueError('node Core payload file set mismatch')
    for relative, digest in pin['files'].items():
        file = Path(dist.locate_file(relative))
        if file.is_symlink() or not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError('node Core payload mismatch: ' + relative)
    requested = Path(request['python_executable'])
    if not requested.is_absolute() or requested.resolve() != Path(sys.executable).resolve():
        raise ValueError('node interpreter differs from the configured environment')
    return {'node_id': request['node'], 'requested_python': str(request['python_executable']),
            'python_executable': str(Path(sys.executable).resolve()), 'python_version': platform.python_version(),
            'platform_node': platform.node(), 'core_version': dist.version,
            'core_dependency_sha256': canonical_hash(pin), 'core_payload_verified': True,
            'verified_payload_files': len(pin['files'])}


def inspect_checkout(project, request, *, status=True):
    environment = inspect_environment(request)
    head = check_tree(project.parent)
    environment['git_sha'] = head
    result = {**result_binding(project, request), 'head': head, 'environment': environment, 'status': 'verified'}
    if status:
        from syncmate_core import context, maintenance
        with context.use(project, node_id=request['node']):
            observed = maintenance.node_status()
        result.update(status=observed['status'], node_status=observed)
    return result


def restore_runner(project, request):
    from syncmate_core import context, queue, maintenance
    observed = inspect_checkout(project, request)
    if observed['head'] != request['target'] or observed['status'] != 'idle':
        raise ValueError('node must verify the installed target and idle queue before restoration')
    node = request['node']
    poll = request['runner']['poll_seconds']
    with context.use(project, node_id=node):
        if queue.runner_agent_lock_dir().exists():
            raise ValueError('restoration refuses an existing runner lock')
        log = project / '.syncmate' / ('runner-install-' + node + '.log')
        with log.open('ab') as output:
            proc = subprocess.Popen([sys.executable, '-B', 'scripts/syncmate/syncmate.py', '--node-id', node,
                'runner-agent', 'serve', '--poll-seconds', str(poll)], cwd=project,
                stdin=subprocess.DEVNULL, stdout=output, stderr=output, start_new_session=True)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            owner = queue.runner_queue_load_json(queue.runner_agent_lock_dir() / 'owner.json')
            if owner.get('pid') == proc.pid and owner.get('node_id') == node:
                return {**observed, 'status': 'restored', 'pid': proc.pid, 'runner_log': str(log)}
            if proc.poll() is not None:
                break
            time.sleep(.1)
    raise ValueError('code installed, node runner restoration failed; do not retry automatically')


def install(request):
    registered = PRIVATE_POLICY['targets'].get(request.get('node'))
    if (registered is None or request.get('ssh') != registered['ssh']
            or request.get('project') != registered['repo_path']):
        raise ValueError('not the registered SSH node, alias and shared project')
    project = Path(request['project'])
    check_not_linked(project)
    repo = project.parent
    if Path(git(repo, 'rev-parse', '--show-toplevel')).resolve() != repo.resolve():
        raise ValueError('unexpected Git root')
    if request.get('action') in ('inspect', 'verify'):
        return inspect_checkout(project, request, status=request['action'] == 'inspect')
    if request.get('action') == 'restore':
        return restore_runner(project, request)
    if request.get('action') != 'apply':
        raise ValueError('explicit apply, inspect, verify or restore action required')
    nodes = request.get('node_ids')
    if (not isinstance(nodes, list) or not nodes or len(set(nodes)) != len(nodes)
            or request['node'] not in nodes or any(n not in PRIVATE_POLICY['targets'] for n in nodes)):
        raise ValueError('complete registered runner node set required')
    inspect_environment(request)
    return install_checkout(project, request)


def install_checkout(project, request):
    """Exact existing-checkout update; the CLI validates the registered address."""
    check_request(request)
    repo = project.parent
    target, old = request['target'], request['old']
    before_origin = origin_refs(repo)
    if check_tree(repo) != old:
        raise ValueError('runner version changed since bundle preparation')
    sys.path.insert(0, str(project))
    from syncmate_core import context
    from syncmate_core.maintenance import installation
    result = {**result_binding(project, request), 'old': old, 'status': 'failed'}
    with context.use(project, node_id=request['node']):
        with installation(node_ids=request['node_ids']) as state:
            result['nodes'] = state['nodes']
            check_tree(repo, old)
            if old != target:
                import_bundle(repo, request)
            else:
                check_policy(repo, target, request['policy_sha256'], request['core_dependency'])
            result['bundle_sha256'] = request.get('bundle_sha256')
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
            result.update(head=target, status='installed' if old != target else 'already_installed', origin_refs_unchanged=True)
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
        node = request.get('node')
        queue_root = project / '.syncmate/runner_queues' / node if node in PRIVATE_POLICY['targets'] else None
        result = {'status': 'failed', 'node': node, 'ssh': request.get('ssh'),
                  'project': str(project), 'target': request.get('target'), 'head': head,
                  'transport': request.get('transport'), 'policy_sha256': request.get('policy_sha256'),
                  'error': str(exc) if isinstance(exc, (ValueError, RuntimeError)) else type(exc).__name__,
                  'runner_lock_present': (queue_root / 'agent.lock').exists() if queue_root is not None else None,
                  'maintenance_present': (queue_root / 'maintenance.json').exists() if queue_root is not None else None}
    print(json.dumps(result))
    return 0 if result['status'] in ('idle', 'verified', 'restored', 'installed', 'already_installed') else 1


if __name__ == '__main__':
    raise SystemExit(main())
