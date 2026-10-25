"""Installed bounded OpenGU entry; queue, locks and transfer stay in Core."""
from __future__ import annotations

import argparse
import base64
from importlib import metadata
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

from syncmate_core import context, devices, queue, run_handoff, versions
from syncmate_core.cli import build_parser, main as core_main
from syncmate_core.process import captured_process_options

from .adapter import OpenGUProjectExtension, implementation
from .runtime import execution_readiness


def protect_runtime_source(source, verification_root):
    if verification_root is not None:
        Path(verification_root).resolve().relative_to(Path(tempfile.gettempdir()).resolve())
        return
    protected = ('data/', 'results/cache', 'results/runtime/', 'results/runs/', '.syncmate/')
    if any(path.startswith(protected) for path in source.files()):
        raise ValueError('source commit tracks protected data/cache/runtime/results storage')


def verify_payload(pin, module_name):
    import importlib
    dist = metadata.distribution(pin['distribution'])
    module = importlib.import_module(module_name)
    if dist.version != pin['version'] or module.__version__ != pin['version']:
        raise ValueError('installed distribution differs from committed pin: ' + module_name)
    expected = Path(dist.locate_file(module_name + '/__init__.py')).resolve()
    if Path(module.__file__).resolve() != expected:
        raise ValueError('installed control dependency is shadowed: ' + module_name)
    for name, digest in pin['files'].items():
        file = Path(dist.locate_file(name))
        if file.is_symlink() or not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError('installed dependency payload differs: ' + name)
    actual = {path.relative_to(expected.parent.parent).as_posix() for path in expected.parent.rglob('*')
              if path.is_file() and '__pycache__' not in path.parts}
    if actual != {name for name in pin['files'] if name.startswith(module_name + '/')}:
        raise ValueError('installed dependency package file set differs: ' + module_name)
    return {'version': dist.version, 'verified_payload_files': len(pin['files']), 'wheel_sha256': pin['wheel_sha256']}


def dependency(source):
    return {module: verify_payload(json.loads(source.read_text('scripts/syncmate/' + filename)), module)
            for filename, module in (('core_dependency.json', 'syncmate_core'), ('control_dependency.json', 'opengu_syncmate'))}


def installed():
    import opengu_syncmate
    expected = metadata.distribution('opengu-syncmate').locate_file('opengu_syncmate/__init__.py')
    if Path(opengu_syncmate.__file__).resolve() != Path(expected).resolve():
        raise ValueError('run the installed control entry with python -I -m opengu_syncmate')


def peer_for(device, node, source, verification_root):
    node = context.validate_node_id(node)
    peer = device.get('peers', {}).get(node)
    if not isinstance(peer, dict) or peer.get('role') not in ('runner', 'runner+collector'):
        raise ValueError('select a configured runner node')
    peer = {**peer, 'node_id': node}
    if devices.peer_uses_local_transport(peer):
        if verification_root is None or Path(peer['repo_path']).resolve() != Path(verification_root).resolve():
            raise ValueError('local transport requires the explicit disposable verification root')
        Path(verification_root).resolve().relative_to(Path(tempfile.gettempdir()).resolve())
    else:
        policy = json.loads(source.read_text('scripts/syncmate/deployment.json'))
        target = policy['targets'].get(node)
        if (policy['transport'] != 'private-bundle' or not target
                or peer.get('ssh') != target['ssh'] or peer.get('repo_path') != target['repo_path']):
            raise ValueError('runner does not match committed private deployment target')
        devices.peer_python_executable(peer)
    return peer


def invoke(peer, arguments, *, payload=None, verification_root=None):
    """Only internally constructed installed-entry commands, never job commands."""
    argv = ['-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate', '--project-root', peer['repo_path'],
            '--node-id', peer['node_id']]
    if verification_root:
        argv += ['--verification-root', verification_root]
    argv += arguments
    if devices.peer_uses_local_transport(peer):
        command, cwd = [sys.executable, *argv], peer['repo_path']
    else:
        command = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20', '--', peer['ssh'],
            'cd ' + shlex.quote(peer['repo_path']) + ' && ' + shlex.join([devices.peer_python_executable(peer), *argv])]
        cwd = None
    completed = subprocess.run(command, cwd=cwd, input=json.dumps(payload) if payload is not None else None,
        capture_output=True, text=True, encoding='utf-8', timeout=240,
        **captured_process_options(piped_input=payload is not None))
    try:
        result = json.loads(completed.stdout)
    except ValueError as exc:
        raise ValueError('installed runner response unavailable: ' + completed.stderr[-1500:]) from exc
    if completed.returncode:
        raise ValueError('installed runner refused operation: ' + json.dumps(result, ensure_ascii=False))
    return result


def source_bundle(source, base):
    """Existing Git history supplies the bound commit, without temporary refs."""
    lines = versions.git(source.root, 'for-each-ref', '--contains=' + source.sha,
                         '--format=%(refname) %(objectname)', 'refs/heads/').decode().splitlines()
    if not lines:
        raise ValueError('bound commit needs a local source branch for private bundle export')
    lines.sort(key=lambda line: not line.startswith('refs/heads/main '))
    ref, head = lines[0].split()
    versions.GitSource(source.root, base)
    versions.git(source.root, 'merge-base', '--is-ancestor', base, head)
    with tempfile.TemporaryDirectory(prefix='opengu-bundle-') as folder:
        path = Path(folder) / 'source.bundle'
        versions.git(source.root, 'bundle', 'create', str(path), ref, '^' + base)
        raw = path.read_bytes()
    return {'target': source.sha, 'source_ref': ref, 'source_head': head,
            'bundle_sha256': hashlib.sha256(raw).hexdigest(), 'bundle': base64.b64encode(raw).decode('ascii')}


def import_source(request):
    """Import Git objects only; HEAD, refs, files and environments never change."""
    root = context.current().root
    target = request['target']
    from syncmate_core.contracts import GIT_SHA_RE
    if not GIT_SHA_RE.fullmatch(target) or not GIT_SHA_RE.fullmatch(request['source_head']):
        raise ValueError('full source Git identities required')
    ref = request['source_ref']
    if not ref.startswith('refs/heads/'):
        raise ValueError('private bundle requires a source branch')
    versions.git(root, 'check-ref-format', ref)
    raw = base64.b64decode(request['bundle'], validate=True)
    if hashlib.sha256(raw).hexdigest() != request['bundle_sha256']:
        raise ValueError('private source bundle SHA mismatch')
    before = versions.git(root, 'rev-parse', 'HEAD')
    before_refs = versions.git(root, 'for-each-ref', '--format=%(refname) %(objectname)')
    with tempfile.NamedTemporaryFile(suffix='.bundle', delete=False) as handle:
        path = Path(handle.name)
        handle.write(raw)
    try:
        versions.git(root, 'bundle', 'verify', str(path))
        heads = versions.git(root, 'bundle', 'list-heads', str(path)).decode().splitlines()
        if heads != [request['source_head'] + ' ' + ref]:
            raise ValueError('private bundle source ref differs')
        versions.git(root, 'fetch', '--no-tags', '--no-write-fetch-head', str(path), ref)
        versions.available(target)
        versions.git(root, 'merge-base', '--is-ancestor', target, request['source_head'])
    finally:
        path.unlink(missing_ok=True)
    if before != versions.git(root, 'rev-parse', 'HEAD') or before_refs != versions.git(root, 'for-each-ref', '--format=%(refname) %(objectname)'):
        raise ValueError('private object import changed HEAD or refs')
    return {'status': 'objects-imported', 'git_sha': target, 'bundle_sha256': request['bundle_sha256'],
            'checkout_unchanged': True, 'node_id': context.runner_node_id()}


def preview(root, recipe, node, device_file, ref, verification_root):
    source = versions.GitSource(root, ref)
    protect_runtime_source(source, verification_root)
    dependency(source)
    device, warnings = devices.load_device(device_file)
    if warnings:
        raise ValueError('; '.join(warnings))
    peer = peer_for(device, node, source, verification_root)
    bound = versions.bind(recipe, ref)
    definition = bound['definition']
    return {'recipe': recipe, 'commit': bound['git_sha'], 'source_ref': ref,
        'config_path': definition['config_path'], 'config_sha256': definition['config_sha256'],
        'recipe_sha256': bound['recipe_sha256'], 'experiment_id': definition.get('experiment_id'),
        'run_identity': definition.get('run_identity'), 'node': node,
        'argv': definition['argv'], 'remote_workdir': peer['repo_path'],
        'remote_result_roots': definition.get('collector_result_roots', []),
        'local_receiving_root': str(root / run_handoff.landing_for(node)),
        'expected_artifact_count': len(definition['expected_artifact_paths']),
        'local_checks_passed': True, 'errors': [], 'warnings': bound['warnings'],
        'runtime_preflight': 'deferred until exact checkout and execution lease',
        'remote_checks': 'NOT OBSERVED: no remote contact in preview', 'submitted': False}


def dispatch(args, *, source_ref, verification_root):
    args.job_id = args.job_id or queue.runner_queue_default_id()
    root = context.current().root
    if run_handoff.handoff_path(args.job_id).exists():
        raise ValueError('job already has a saved handoff; inspect that job before retrying')
    source = versions.GitSource(root, source_ref)
    protect_runtime_source(source, verification_root)
    dependency(source)
    device, warnings = devices.load_device(args.config)
    if warnings:
        raise ValueError('; '.join(warnings))
    peer = peer_for(device, args.node_id, source, verification_root)
    bound = versions.bind(args.recipe, source_ref)
    available = invoke(peer, ['source-status'], payload={'target': source.sha}, verification_root=verification_root)
    if available['installed_adapter'] != implementation():
        raise ValueError('selected node installed consumer identity differs')
    imported = available
    if not available['available']:
        imported = invoke(peer, ['source-import'], payload=source_bundle(source, available['head']),
                          verification_root=verification_root)
    proof = root / '.syncmate/source-imports' / (args.job_id + '.json')
    proof.parent.mkdir(parents=True, exist_ok=True)
    with proof.open('x', encoding='utf-8') as handle:
        json.dump({'node': args.node_id, 'source_sha': source.sha, 'source_ref': source_ref,
                   'observation': imported}, handle, ensure_ascii=False)
    handoff = run_handoff.create_handoff(device, args.node_id, args.recipe, args.job_id, source.sha,
                                        definition=bound['definition'])
    science = root / '.syncmate/science' / (args.job_id + '.json')
    science.parent.mkdir(parents=True, exist_ok=True)
    with science.open('x', encoding='utf-8') as handle:
        json.dump(bound['definition'], handle, ensure_ascii=False, allow_nan=False)
    submitted = invoke(peer, ['runner-queue', 'submit', '--recipe', args.recipe, '--job-id', args.job_id,
        '--expected-git-sha', source.sha, '--binding-stdin', '--json'],
        payload=handoff['execution'], verification_root=verification_root)
    if submitted.get('output_contract') != handoff['execution']:
        raise ValueError('runner reservation differs from frozen handoff')
    result = {'status': 'submitted', 'job_id': args.job_id, 'source_ref': source_ref,
            'expected_git_sha': source.sha, 'warnings': bound['warnings'],
            'source_import': imported, 'handoff': handoff, 'submission': submitted}
    if args.wait:
        from syncmate_core import dispatch as core_dispatch
        watched = core_dispatch.runner_agent_watch_payload(device, node_id=args.node_id, job_id=args.job_id,
            poll_seconds=args.poll_seconds, timeout_seconds=args.timeout_seconds)
        result.update(status=watched['status'], watch=watched)
        if watched['status'] == 'done':
            returned = core_dispatch.runner_agent_collect_and_gate(args.node_id, job_id=args.job_id,
                                                                  completed_job=watched['job'])
            result.update(status=returned['status'], delivery=returned)
    return result


def submit(args):
    args.job_id = args.job_id or queue.runner_queue_default_id()
    contract = json.load(sys.stdin) if args.binding_stdin else None
    ref = contract['git_sha'] if contract else args.expected_git_sha or 'refs/heads/main'
    source = versions.GitSource(context.current().root, ref)
    protect_runtime_source(source, context.extension().verification_root)
    dependency(source)
    bound = versions.bind(args.recipe, ref)
    actual = run_handoff.build_execution_contract(bound['definition'], project='opengu',
        job_id=args.job_id, git_sha=source.sha)
    if contract is not None and actual != contract:
        raise ValueError('runner committed definition or installed adapter differs from binding')
    rid = actual['run_identity'].get('run_id')
    if rid and (source.root / 'results/runtime/modular' / rid).exists():
        raise ValueError('shared runtime identity already exists: ' + rid)
    return queue.runner_queue_submit(args.job_id, args.recipe, expected_git_sha=source.sha, binding=actual,
        requested_by=args.requested_by, note=args.note)


def scientific_check(node, job_id):
    from syncmate_core import index
    handoff = run_handoff.load_handoff(job_id, node)
    delivery = run_handoff.load_delivery(job_id, node)
    if not delivery or delivery.get('verify', {}).get('summary', {}).get('status') != 'verified':
        raise ValueError('scientific check requires this task verified delivery')
    contract = handoff['execution']
    frozen = json.loads((context.current().root / '.syncmate/science' / (job_id + '.json')).read_text(encoding='utf-8'))
    expected = run_handoff.build_execution_contract(frozen, project='opengu', job_id=job_id, git_sha=contract['git_sha'])
    if expected != contract:
        raise ValueError('frozen scientific definition differs from saved Core contract')
    trusted = index.load_artifact_index()
    peer = trusted['peers'][node]
    selected = [entry for entry in peer['items'] if entry['remote_path'] in contract['collect_paths']]
    manifest = {entry['path']: entry for entry in delivery['completed_job']['result']['seal']['manifest']['artifacts']}
    for entry in selected:
        if (entry['sha256'] != manifest[entry['remote_path']]['sha256']
                or entry['remote_git']['sha'] != contract['git_sha']
                or entry['run_handoff'] != str(run_handoff.handoff_path(job_id).relative_to(context.current().root)).replace('\\', '/')):
            raise ValueError('trusted entry does not belong to this frozen delivery')
    scoped = {'peers': {node: {**peer, 'items': selected, 'summary': {'status': 'verified'}}}}
    result = context.extension().accept('modular-output-v1', frozen,
        {'project_root': str(context.current().root), 'node_id': node,
         'expected_git_sha': contract['git_sha'], 'artifact_index': scoped})
    result.update(job_id=job_id, node_id=node, git_sha=contract['git_sha'])
    output = context.current().sync_dir / 'science' / (job_id + '-validation.json')
    from syncmate_core.storage import write_json_atomic
    write_json_atomic(output, result)
    return result


def main(argv=None):
    raw = list(sys.argv[1:] if argv is None else argv)
    own = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    own.add_argument('--project-root', type=Path, default=Path.cwd())
    own.add_argument('--node-id')
    own.add_argument('--verification-root')
    own.add_argument('--source-ref', default='refs/heads/main')
    common, rest = own.parse_known_args(raw)
    root = common.project_root.resolve()
    prefix = ['--project-root', str(root)]
    if common.node_id:
        prefix += ['--node-id', common.node_id]
    extension = OpenGUProjectExtension(verification_root=common.verification_root)
    with context.use(root, extension=extension, node_id=common.node_id):
        parser = build_parser()
    subs = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    view = subs.add_parser('preview')
    view.add_argument('recipe')
    view.add_argument('--node', required=True)
    subs.add_parser('source-import')
    subs.add_parser('source-status')
    subs.add_parser('dependencies')
    science = subs.add_parser('scientific-check')
    science.add_argument('node')
    science.add_argument('--job-id', required=True)
    args = parser.parse_args(prefix + rest)
    node = args.node_id if getattr(args, 'command', None) != 'preview' else args.node
    try:
        installed()
        with context.use(root, extension=extension, node_id=node, execution_readiness=execution_readiness):
            if common.node_id and getattr(args, 'node', common.node_id) != common.node_id:
                raise ValueError('explicit node identities differ')
            if args.command == 'preview':
                result = preview(root, args.recipe, args.node, args.config, common.source_ref, common.verification_root)
            elif args.command == 'dependencies':
                source = versions.GitSource(root, common.source_ref)
                result = {'status': 'verified', 'git_sha': source.sha, 'dependencies': dependency(source)}
            elif args.command == 'source-import':
                device, warnings = devices.load_device(args.config)
                if warnings or Path(device['repo_path']).resolve() != root:
                    raise ValueError('source import device/project identity is unverified')
                if common.verification_root is not None:
                    if Path(common.verification_root).resolve() != root:
                        raise ValueError('source import verification root differs')
                    root.relative_to(Path(tempfile.gettempdir()).resolve())
                else:
                    policy = json.loads(versions.GitSource(root, 'HEAD').read_text('scripts/syncmate/deployment.json'))
                    if str(root) != policy['targets'][context.runner_node_id()]['repo_path']:
                        raise ValueError('source import is outside the registered execution checkout')
                result = import_source(json.load(sys.stdin))
            elif args.command == 'source-status':
                target = json.load(sys.stdin)['target']
                from syncmate_core.contracts import GIT_SHA_RE
                if not GIT_SHA_RE.fullmatch(target):
                    raise ValueError('full source SHA required')
                try:
                    versions.available(target)
                    available = True
                except ValueError:
                    available = False
                result = {'available': available, 'head': versions.git(root, 'rev-parse', 'HEAD').decode().strip(),
                          'installed_adapter': implementation()}
            elif args.command == 'scientific-check':
                result = scientific_check(args.node, args.job_id)
            elif args.command == 'runner-agent' and args.runner_agent_command == 'dispatch':
                result = dispatch(args, source_ref=common.source_ref, verification_root=common.verification_root)
            elif args.command == 'runner-queue' and args.runner_queue_command == 'submit':
                result = submit(args)
            elif args.command == 'console':
                raise ValueError('OpenGU uses its installed dispatch entry; generic console submission is unsupported')
            else:
                return core_main(prefix + rest, project_root=root, extension=extension,
                                 execution_readiness=execution_readiness)
        print(json.dumps(result, ensure_ascii=False))
        return 1 if result.get('passed') is False or result.get('status') in ('blocked', 'failed', 'timeout') else 0
    except (Exception, SystemExit) as exc:
        print(json.dumps({'status': 'blocked', 'errors': [str(exc)]}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
