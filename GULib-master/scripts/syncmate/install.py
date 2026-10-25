"""Private shared-checkout update after every registered runner is verified idle."""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.syncmate.deployment_policy import (
    deployment_policy, dependency_pin, installation_receipt, receipt_path, validate_peer, validate_receipt)
from opengu_syncmate import provision


class NodeOffline(ValueError):
    """A connection was refused before any remote program responded."""


def response_json(response, *, may_defer=False):
    if (may_defer and response.returncode == 255 and not response.stdout.strip()
            and re.search(r'Connection refused|Connection timed out|Operation timed out|No route to host|Network is unreachable', response.stderr)):
        raise NodeOffline(response.stderr.strip())
    try:
        result = json.loads(response.stdout)
        if not isinstance(result, dict):
            raise ValueError('response is not an object')
    except ValueError as exc:
        raise ValueError('node response unavailable; preserve state and diagnose: ' + response.stderr[-800:]) from exc
    if response.returncode:
        raise ValueError('remote action failed: ' + json.dumps(result))
    return result


def provision_node(peer, request, *, may_defer=False):
    code = Path(provision.__file__).read_text(encoding='utf-8')
    response = ssh(peer, [peer['python_executable'], '-I', '-X', 'utf8', '-B', '-c', code],
                   payload=json.dumps(request))
    return response_json(response, may_defer=may_defer)


def bundle_for(old, target, directory):
    if old == target:
        return {'bundle': '', 'bundle_sha256': None}
    subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', old, target], check=True)
    with tempfile.TemporaryDirectory(prefix='bundle-', dir=str(directory)) as temporary:
        path = Path(temporary) / 'code.bundle'
        subprocess.run(['git', '-C', str(ROOT), 'bundle', 'create', str(path), 'refs/heads/main', '^' + old],
                       check=True, capture_output=True)
        data = path.read_bytes()
        return {'bundle': base64.b64encode(data).decode('ascii'), 'bundle_sha256': hashlib.sha256(data).hexdigest()}


def bootstrap():
    """Explicit exact-wheel bootstrap; never updates the scientific base env."""
    policy = deployment_policy(ROOT)
    runners = load_runners(policy)
    target = git('rev-parse', 'HEAD')
    previous = provision.load(ROOT) if (ROOT / '.syncmate/deployments/active.json').exists() else None
    bases = {n: (previous['nodes'][n]['base_python'] if previous and n in previous['nodes']
                 else peer['python_executable']) for n, peer in runners.items()}
    manifest = {'protocol': provision.PROTOCOL, 'source_sha': target,
        'policy': {k: v for k, v in policy.items() if k != 'sha256'},
        'pins': {'core': dependency_pin(ROOT)[0], 'control': dependency_pin(ROOT, 'control_dependency.json')[0]},
        'controller': {'base_python': sys.executable, 'root': str(ROOT)},
        'nodes': {n: {'base_python': p} for n, p in bases.items()}}
    folder = provision.directory(ROOT, target)
    folder.mkdir(parents=True, exist_ok=True)
    wheels = {key: base64.b64encode((ROOT / '.syncmate/package-inputs' / pin['wheel']).read_bytes()).decode('ascii')
              for key, pin in manifest['pins'].items()}
    request = {'action': 'prepare', 'root': str(ROOT), 'manifest': manifest, 'wheels': wheels}
    provision.stage(ROOT, request)
    local = provision.ensure_runtime(ROOT, manifest)
    observed, deferred = {}, {}
    for node, configured in runners.items():
        peer = {**configured, 'python_executable': bases[node]}
        try:
            probe = provision_node(peer, {'action': 'probe', 'root': peer['repo_path'],
                                         'node': node, 'nodes': list(runners)}, may_defer=True)
        except NodeOffline as exc:
            deferred[node] = {'status': 'deferred', 'reason': str(exc)}
            continue
        if any(state.get('status') != 'idle' for state in probe['queues'].values()):
            raise ValueError('shared queues are busy or unknown: ' + json.dumps(probe['queues']))
        prepared = provision_node(peer, {**request, **bundle_for(probe['head'], target, folder),
                                         'root': peer['repo_path'], 'node': node})
        if prepared.get('status') != 'ready' or prepared.get('source_sha') != target:
            raise ValueError('node runtime is not verified: ' + node)
        observed[node] = prepared
    if not observed:
        raise ValueError('no online coordinator; deployment remains prepared only')
    print(json.dumps({'status': 'prepared', 'target': target, 'controller': local,
                      'online': observed, 'deferred': deferred}))
    return 0


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def ssh(peer, argv, *, payload=None, timeout=240):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20', '--',
                           peer['ssh'], shlex.join(argv)], input=payload,
                          capture_output=True, text=True, encoding='utf-8', timeout=timeout)


def registered_runners(device, policy):
    runners = {node: peer for node, peer in device.get('peers', {}).items()
               if isinstance(peer, dict) and peer.get('role', 'runner') in ('runner', 'runner+collector')}
    if not runners:
        raise ValueError('no registered runner peers')
    for node, peer in runners.items():
        validate_peer(peer, node, policy)
    return dict(sorted(runners.items()))


def load_runners(policy):
    from syncmate_core import context, devices
    with context.use(ROOT):
        device, warnings = devices.load_device(ROOT / '.syncmate/device.yaml')
    if warnings:
        raise ValueError('; '.join(warnings))
    return registered_runners(device, policy)


def invoke(peer, request):
    code = Path(__file__).with_name('install_remote.py').read_text(encoding='utf-8')
    response = ssh(peer, [peer['python_executable'], '-I', '-X', 'utf8', '-B', '-c', code], payload=json.dumps(request))
    return response_json(response, may_defer=request['action'] == 'inspect')


def request_for(node, peer, *, action, target, policy, pin):
    return {'action': action, 'node': node, 'ssh': peer['ssh'], 'project': peer['repo_path'],
            'python_executable': peer['python_executable'], 'target': target,
            'transport': policy['transport'], 'policy_sha256': policy['sha256'], 'core_dependency': pin,
            'control_dependency': dependency_pin(ROOT, 'control_dependency.json')[0]}


def verify_observation(result, node, peer, *, pin_sha, target=None, idle=False):
    env = result.get('environment') or {}
    if (result.get('node') != node or result.get('ssh') != peer['ssh']
            or result.get('project') != peer['repo_path']
            or env.get('node_id') != node or env.get('requested_python') != peer['python_executable']
            or env.get('core_dependency_sha256') != pin_sha or env.get('core_payload_verified') is not True
            or env.get('control_dependency_sha256') != dependency_pin(ROOT, 'control_dependency.json')[1]
            or env.get('control_payload_verified') is not True
            or not env.get('python_executable') or env.get('git_sha') != result.get('head')
            or (target is not None and result.get('head') != target)
            or result.get('status') not in ('idle', 'verified', 'restored')
            or (idle and (result.get('status') != 'idle'
                          or (result.get('node_status') or {}).get('node_id') != node))):
        raise ValueError('node identity, environment, target or idle state is unverified: ' + node)


def apply(node):
    if ROOT.resolve() != Path('E:/project/OpenGU/GULib-master').resolve():
        raise ValueError('installation must run from the canonical landed project')
    if git('branch', '--show-current') != 'main' or git('status', '--porcelain=v1', '-uall'):
        raise ValueError('installation requires clean main')
    manifest = provision.load(ROOT, git('rev-parse', 'HEAD'))
    expected = provision.runtime_python(manifest['controller']['base_python'], manifest['pins'])
    provision.probe_runtime(expected, manifest['pins'])
    if Path(sys.executable).resolve() != Path(expected).resolve():
        return subprocess.run([expected, '-I', '-X', 'utf8', '-B', str(Path(__file__).resolve()),
                               'apply', '--node', node]).returncode
    return deploy(node, manifest=manifest)


def deploy(node, *, manifest=None):
    """One shared update, all physical queues, independently reachable nodes."""
    started = time.monotonic()
    policy = deployment_policy(ROOT)
    pin, pin_sha = dependency_pin(ROOT)
    local = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
        '--project-root', str(ROOT), '--source-ref', 'HEAD', 'dependencies'],
        capture_output=True, text=True, encoding='utf-8', timeout=60)
    if local.returncode:
        raise ValueError('local control environment is unverified: ' + local.stdout + local.stderr)
    runners = load_runners(policy)
    if manifest:
        runners = {n: {**p, 'python_executable': provision.runtime_python(manifest['nodes'][n]['base_python'], manifest['pins'])}
                   for n, p in runners.items()}
    if node not in runners:
        raise ValueError('select a registered coordinator node')
    target = git('rev-parse', 'HEAD')
    directory = ROOT / '.workblock/runtime/install' / node / target
    directory.mkdir(parents=True, exist_ok=True)
    report = {'coordinator': node, 'target': target, 'nodes': list(runners),
              'status': 'blocked', 'before': {}, 'after': {}, 'deferred': {}, 'restoration': {}, 'errors': []}
    try:
        for current, peer in runners.items():
            try:
                if manifest:
                    base = {**peer, 'python_executable': manifest['nodes'][current]['base_python']}
                    prepared = provision_node(base, {'action': 'ensure-prepared', 'root': peer['repo_path'],
                        'node': current, 'source_sha': target}, may_defer=True)
                    if prepared.get('status') != 'ready' or prepared.get('runtime_python') != peer['python_executable']:
                        raise ValueError('prepared node runtime is unverified: ' + current)
                observed = invoke(peer, request_for(current, peer, action='inspect', target=target, policy=policy, pin=pin))
                report['before'][current] = observed
                verify_observation(observed, current, peer, pin_sha=pin_sha, idle=True)
            except NodeOffline as exc:
                report['deferred'][current] = {'status': 'deferred', 'reason': str(exc)}
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                report['errors'].append(current + ': ' + str(exc))
        if report['errors']:
            return 1
        online = {n: p for n, p in runners.items() if n in report['before']}
        if not online:
            raise ValueError('no reachable deployment coordinator')
        if node not in online:
            node = next(iter(online))
            report['coordinator'] = node
        versions = {r['head'] for r in report['before'].values()}
        if len(versions) != 1:
            raise ValueError('registered runners do not observe one shared code version')
        old = versions.pop()
        exported = bundle_for(old, target, directory)
        bundle, bundle_sha = exported['bundle'], exported['bundle_sha256']
        request = request_for(node, runners[node], action='apply', target=target, policy=policy, pin=pin)
        request.update(old=old, bundle=bundle, bundle_sha256=bundle_sha, node_ids=list(runners))
        installed = invoke(runners[node], request)
        report['shared_update'] = installed
        if (installed.get('status') not in ('installed', 'already_installed') or installed.get('head') != target
                or installed.get('origin_refs_unchanged') is not True
                or set(installed.get('nodes') or {}) != set(runners)):
            raise ValueError('shared update failed or omitted a registered node; retain state for diagnosis')
        for current, peer in online.items():
            try:
                observed = invoke(peer, request_for(current, peer, action='inspect', target=target, policy=policy, pin=pin))
                report['after'][current] = observed
                verify_observation(observed, current, peer, pin_sha=pin_sha, target=target, idle=True)
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                report['errors'].append(current + ': ' + str(exc))
        if report['errors']:
            return 1
        if manifest:
            active = provision_node(online[node], {'action': 'activate', 'root': online[node]['repo_path'], 'source_sha': target})
            if active.get('status') != 'active':
                raise ValueError('shared deployment activation is unverified')
            provision.atomic(ROOT / '.syncmate/deployments/active.json', {'source_sha': target})
            import yaml
            device_path = ROOT / '.syncmate/device.yaml'
            device = yaml.safe_load(device_path.read_text(encoding='utf-8'))
            for n, peer in runners.items():
                device['peers'][n]['python_executable'] = peer['python_executable']
            device_path.write_text(yaml.safe_dump(device, allow_unicode=True, sort_keys=False), encoding='utf-8')
        for current, peer in online.items():
            state = installed['nodes'][current]
            if state.get('node_id') != current:
                raise ValueError('maintenance node ownership mismatch')
            if state.get('restart'):
                request = request_for(current, peer, action='restore', target=target, policy=policy, pin=pin)
                request['runner'] = state['runner']
                restored = invoke(peer, request)
                verify_observation(restored, current, peer, pin_sha=pin_sha, target=target)
                if restored['status'] != 'restored':
                    raise ValueError('node runner restoration is unverified: ' + current)
                report['restoration'][current] = restored
        for current, peer in online.items():
            expected = {'python_executable': peer['python_executable'], 'core_dependency_sha256': pin_sha,
                        'control_dependency_sha256': dependency_pin(ROOT, 'control_dependency.json')[1]}
            receipt = {'node': current, 'ssh': peer['ssh'], 'project': peer['repo_path'],
                'target': target, 'head': target, 'status': installed['status'],
                'transport': policy['transport'], 'policy_sha256': policy['sha256'],
                'bundle_sha256': bundle_sha, 'origin_refs_unchanged': True, 'coordinator': node,
                'registered_nodes': list(runners), 'expected_environment': expected,
                'environment': report['after'][current]['environment'],
                'restoration': report['restoration'].get(current)}
            validate_receipt(receipt, current, target, policy, expected_environment=expected, bundle_sha256=bundle_sha)
            path = receipt_path(ROOT, current, target, policy)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        report['status'] = 'installed_with_deferred_nodes' if report['deferred'] else installed['status']
        if manifest:
            provision.atomic(provision.directory(ROOT, target) / 'rollout.json',
                {'source_sha': target, 'status': report['status'], 'coordinator': node,
                 'nodes': {n: {'status': 'verified' if n in online else 'deferred'} for n in runners}})
        return 0
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as exc:
        report['errors'].append(str(exc))
        return 1
    finally:
        report['elapsed_seconds'] = round(time.monotonic() - started, 2)
        path = directory / ('attempt-' + uuid.uuid4().hex + '.json')
        path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps({'report': str(path), **report}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['bootstrap', 'apply', 'receipt', 'deployment-status'])
    parser.add_argument('--node', default='gpu4090', help='preferred coordinator or receipt node')
    args = parser.parse_args(argv)
    try:
        if args.action == 'bootstrap':
            if ROOT.resolve() != Path('E:/project/OpenGU/GULib-master').resolve() or git('branch', '--show-current') != 'main' or git('status', '--porcelain=v1', '-uall'):
                raise ValueError('bootstrap requires canonical clean landed main')
            return bootstrap()
        if args.action == 'apply':
            return apply(args.node)
        if args.action == 'deployment-status':
            manifest = provision.load(ROOT)
            target = git('rev-parse', 'HEAD')
            if manifest['source_sha'] != target:
                raise ValueError('active deployment differs from landed target')
            value = json.loads((provision.directory(ROOT, target) / 'rollout.json').read_text(encoding='utf-8'))
            if value['source_sha'] != target or set(value['nodes']) != set(manifest['nodes']):
                raise ValueError('deployment receipt does not cover the registered topology')
            for node in value['nodes']:
                ready = provision.directory(ROOT, target) / 'nodes' / (node + '.json')
                if ready.exists():
                    observed = json.loads(ready.read_text(encoding='utf-8'))
                    if observed.get('status') == 'ready' and observed.get('source_sha') == target and observed.get('node') == node:
                        value['nodes'][node] = {'status': 'verified', 'runtime_python': observed['runtime_python']}
            print(json.dumps(value))
            return 0
        policy = deployment_policy(ROOT)
        runners = load_runners(policy)
        result = installation_receipt(ROOT, args.node, git('rev-parse', 'HEAD'), policy, peer=runners.get(args.node))
        print(json.dumps(result))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
