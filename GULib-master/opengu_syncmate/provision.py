"""Authorized immutable control runtimes, independent of node availability.

This program also runs with the configured base Python before the control wheel
exists. It uses only the standard library; it never updates the base environment.
Scientific jobs do not carry packages, installation commands or runtime paths.
"""
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import tempfile


PROTOCOL = 'opengu.deployment/v1'
FILES = (('core', 'syncmate', 'syncmate_core'), ('control', 'opengu-syncmate', 'opengu_syncmate'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, **kwargs):
    result = subprocess.run([str(a) for a in argv], capture_output=True, text=True,
        encoding='utf-8', timeout=kwargs.pop('timeout', 240),
        **({'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}), **kwargs)
    if result.returncode:
        raise ValueError('runtime operation failed: ' + result.stderr[-1800:])
    return result.stdout.strip()


def git(root, *args):
    return run(['git', '-C', root, *args])


def committed(root, sha, name):
    if not re.fullmatch('[0-9a-f]{40}', sha):
        raise ValueError('full deployment source SHA required')
    prefix = git(root, 'rev-parse', '--show-prefix')
    if not re.fullmatch(r'100644 blob [0-9a-f]+\s+.*', git(root, 'ls-tree', '--full-tree', sha, '--', prefix + name)):
        raise ValueError('deployment input is not a committed regular file: ' + name)
    return git(root, 'show', sha + ':' + prefix + name)


def runtime_python(base_python, pins):
    path = PurePosixPath(base_python) if base_python.startswith('/') else PureWindowsPath(base_python)
    if not path.is_absolute():
        raise ValueError('absolute base interpreter required')
    prefix = path.parent.parent if path.parent.name.lower() in ('bin', 'scripts') else path.parent
    identity = digest(('\0'.join(pins[k]['wheel_sha256'] for k, _, _ in FILES)).encode())[:16]
    prefix = prefix / 'envs' / ('opengu-control-' + identity)
    return str(prefix / ('Scripts/python.exe' if isinstance(path, PureWindowsPath) else 'bin/python'))


def checked_root(value):
    root = Path(value)
    if not root.is_absolute() or not root.is_dir():
        raise ValueError('existing absolute project root required')
    for part in (root, *root.parents):
        if part.is_symlink():
            raise ValueError('deployment root must not follow links')
    return root.resolve()


def directory(root, sha):
    if not re.fullmatch('[0-9a-f]{40}', sha):
        raise ValueError('invalid deployment source')
    path = root / '.syncmate/deployments' / sha
    for part in (path, path.parent, path.parent.parent):
        if part.is_symlink():
            raise ValueError('linked deployment storage')
    return path


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError('linked deployment record')
    data = (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        temporary = Path(f.name)
        f.write(data)
    try:
        os.replace(str(temporary), str(path))
    finally:
        temporary.unlink(missing_ok=True)


def validate(root, manifest):
    if manifest.get('protocol') != PROTOCOL:
        raise ValueError('unsupported deployment manifest')
    sha = manifest['source_sha']
    policy = json.loads(committed(root, sha, 'scripts/syncmate/deployment.json'))
    if manifest['policy'] != policy:
        raise ValueError('deployment policy differs from committed source')
    for key, distribution, _ in FILES:
        filename = 'core_dependency.json' if key == 'core' else 'control_dependency.json'
        pin = manifest['pins'][key]
        if (pin != json.loads(committed(root, sha, 'scripts/syncmate/' + filename))
                or pin['distribution'] != distribution
                or not re.fullmatch('[0-9a-f]{64}', pin['wheel_sha256'])
                or Path(pin['wheel']).name != pin['wheel']):
            raise ValueError('deployment package differs from committed pin: ' + key)
    if (not manifest['nodes'] or any(node not in policy['targets'] for node in manifest['nodes'])
            or any(not re.fullmatch('[a-z0-9][a-z0-9_-]{0,63}', node) for node in manifest['nodes'])):
        raise ValueError('deployment nodes differ from registered policy')
    return manifest


def import_objects(root, request):
    target = request['manifest']['source_sha']
    try:
        git(root, 'rev-parse', '--verify', target + '^{commit}')
        return
    except ValueError:
        pass
    raw = base64.b64decode(request['bundle'], validate=True)
    if digest(raw) != request['bundle_sha256']:
        raise ValueError('deployment source bundle digest differs')
    staging = directory(root, target)
    staging.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=staging, suffix='.bundle', delete=False) as f:
        temporary = Path(f.name)
        f.write(raw)
    before = git(root, 'for-each-ref', '--format=%(refname) %(objectname)')
    head = git(root, 'rev-parse', 'HEAD')
    try:
        git(root, 'bundle', 'verify', str(temporary))
        if git(root, 'bundle', 'list-heads', str(temporary)) != target + ' refs/heads/main':
            raise ValueError('deployment bundle must advertise exactly the landed main')
        git(root, 'bundle', 'unbundle', str(temporary))
        git(root, 'rev-parse', '--verify', target + '^{commit}')
    finally:
        temporary.unlink(missing_ok=True)
    if head != git(root, 'rev-parse', 'HEAD') or before != git(root, 'for-each-ref', '--format=%(refname) %(objectname)'):
        raise ValueError('object import changed checkout or references')


def load(root, sha=None):
    if sha is None:
        pointer = root / '.syncmate/deployments/active.json'
        if pointer.is_symlink():
            raise ValueError('linked deployment pointer')
        sha = json.loads(pointer.read_text(encoding='utf-8'))['source_sha']
    path = directory(root, sha) / 'manifest.json'
    if path.is_symlink():
        raise ValueError('linked deployment manifest')
    return validate(root, json.loads(path.read_text(encoding='utf-8')))


def stage(root, request):
    import_objects(root, request)
    manifest = validate(root, request['manifest'])
    folder = directory(root, manifest['source_sha'])
    folder.mkdir(parents=True, exist_ok=True)
    for key, _, _ in FILES:
        pin = manifest['pins'][key]
        raw = base64.b64decode(request['wheels'][key], validate=True)
        if digest(raw) != pin['wheel_sha256']:
            raise ValueError('deployment wheel digest differs: ' + key)
        path = folder / pin['wheel']
        if path.is_symlink() or (path.exists() and path.read_bytes() != raw):
            raise ValueError('deployment wheel storage conflicts')
        if not path.exists():
            with path.open('xb') as f:
                f.write(raw)
    path = folder / 'manifest.json'
    if path.is_symlink():
        raise ValueError('linked deployment manifest')
    if path.exists() and json.loads(path.read_text(encoding='utf-8')) != manifest:
        raise ValueError('immutable deployment manifest conflicts')
    if not path.exists():
        atomic(path, manifest)
    return manifest


def probe_runtime(python, pins):
    code = '''import json,sys,importlib
from pathlib import Path
from opengu_syncmate.control import verify_payload
pins=json.load(sys.stdin)
for module in ('syncmate_core','opengu_syncmate'):
    Path(importlib.import_module(module).__file__).resolve().relative_to(Path(sys.prefix).resolve())
print(json.dumps({'python':sys.executable,'pins':{module:verify_payload(pins[key],module) for key,module in [('core','syncmate_core'),('control','opengu_syncmate')]}}))'''
    return json.loads(run([python, '-I', '-X', 'utf8', '-B', '-c', code], input=json.dumps(pins), timeout=60))


def ensure_runtime(root, manifest, node=None):
    role = manifest['nodes'][node] if node is not None else manifest['controller']
    expected = manifest['policy']['targets'][node]['repo_path'] if node else role['root']
    if str(root) != expected:
        temporary = manifest.get('verification_roots', [])
        if str(root) not in temporary:
            raise ValueError('runtime request is outside the registered node project')
        for value in temporary:
            Path(value).resolve().relative_to(Path(tempfile.gettempdir()).resolve())
    if Path(role['base_python']).resolve() != Path(sys.executable).resolve():
        raise ValueError('bootstrap must use the registered base interpreter')
    python = Path(runtime_python(role['base_python'], manifest['pins']))
    prefix = python.parent.parent
    prefix.resolve().relative_to(Path(sys.prefix).resolve())
    for part in (prefix, *prefix.parents):
        if part.is_symlink():
            raise ValueError('runtime prefix follows a link')
    state = prefix / 'opengu-runtime.json'
    identity = {'protocol': 'opengu.control-runtime/v1', 'base_python': role['base_python'],
                'pins': {k: manifest['pins'][k]['wheel_sha256'] for k, _, _ in FILES}}
    if prefix.exists():
        if not state.is_file() or state.is_symlink():
            raise ValueError('runtime prefix has unknown ownership; preserve it')
        old = json.loads(state.read_text(encoding='utf-8'))
        if old != {**identity, 'status': 'ready'}:
            raise ValueError('incomplete runtime requires explicit installation diagnosis')
    else:
        prefix.mkdir(parents=True)
        atomic(state, {**identity, 'status': 'building'})
        try:
            run([sys.executable, '-I', '-B', '-m', 'venv', '--without-pip', '--system-site-packages', prefix], timeout=180)
            folder = directory(root, manifest['source_sha'])
            wheels = []
            for key, _, _ in FILES:
                pin = manifest['pins'][key]
                file = folder / pin['wheel']
                if file.is_symlink() or digest(file.read_bytes()) != pin['wheel_sha256']:
                    raise ValueError('staged wheel integrity failed')
                wheels.append(file)
            run([python, '-I', '-B', '-m', 'pip', 'install', '--no-index', '--no-deps', '--no-compile', '--ignore-installed',
                 '--no-cache-dir', '--disable-pip-version-check', *wheels], timeout=180)
            probe_runtime(python, manifest['pins'])
            atomic(state, {**identity, 'status': 'ready'})
        except BaseException:
            atomic(state, {**identity, 'status': 'failed'})
            raise
    observed = probe_runtime(python, manifest['pins'])
    receipt = {'status': 'ready', 'node': node, 'source_sha': manifest['source_sha'],
               'runtime_python': str(python), 'base_unchanged': True, 'observed': observed}
    atomic(directory(root, manifest['source_sha']) / 'nodes' / ((node or 'controller') + '.json'), receipt)
    return receipt


def main():
    request = json.load(sys.stdin)
    try:
        root = checked_root(request['root'])
        action = request['action']
        if action == 'probe':
            from syncmate_core import context, maintenance
            with context.use(root, node_id=request['node']):
                queues = {}
                for node in request['nodes']:
                    with context.node(node):
                        queues[node] = maintenance.node_status()
            result = {'status': 'reachable', 'head': git(root, 'rev-parse', 'HEAD'),
                      'python': sys.executable, 'queues': queues}
        elif action == 'prepare':
            manifest = stage(root, request)
            result = ensure_runtime(root, manifest, request.get('node'))
        elif action in ('ensure', 'ensure-prepared'):
            manifest = load(root, request['source_sha'] if action == 'ensure-prepared' else None)
            if request.get('source_sha') and manifest['source_sha'] != request['source_sha']:
                raise ValueError('node active deployment differs from controller')
            result = ensure_runtime(root, manifest, request.get('node'))
        elif action == 'activate':
            manifest = load(root, request['source_sha'])
            if git(root, 'rev-parse', 'HEAD') != manifest['source_sha'] or git(root, 'status', '--porcelain=v1', '-uall'):
                raise ValueError('activation requires the exact clean deployed source')
            atomic(root / '.syncmate/deployments/active.json', {'source_sha': manifest['source_sha']})
            result = {'status': 'active', 'source_sha': manifest['source_sha']}
        else:
            raise ValueError('unsupported provisioning action')
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({'status': 'blocked', 'errors': [str(exc)]}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
