"""Private shared-checkout update after every registered runner is verified idle."""
import argparse
import base64
import hashlib
import json
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
    response = ssh(peer, [peer['python_executable'], '-B', '-c', code], payload=json.dumps(request))
    try:
        result = json.loads(response.stdout)
        if not isinstance(result, dict):
            raise ValueError('response is not an object')
    except ValueError as exc:
        raise ValueError('node response unavailable; diagnose the original action before any retry') from exc
    if response.returncode != 0 and result.get('status') not in ('busy', 'unknown', 'failed'):
        result['status'] = 'failed'
    return result


def request_for(node, peer, *, action, target, policy, pin):
    return {'action': action, 'node': node, 'ssh': peer['ssh'], 'project': peer['repo_path'],
            'python_executable': peer['python_executable'], 'target': target,
            'transport': policy['transport'], 'policy_sha256': policy['sha256'], 'core_dependency': pin}


def verify_observation(result, node, peer, *, pin_sha, target=None, idle=False):
    env = result.get('environment') or {}
    if (result.get('node') != node or result.get('ssh') != peer['ssh']
            or result.get('project') != peer['repo_path']
            or env.get('node_id') != node or env.get('requested_python') != peer['python_executable']
            or env.get('core_dependency_sha256') != pin_sha or env.get('core_payload_verified') is not True
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
    return deploy(node)


def deploy(node):
    """All-node orchestration; CLI owns the canonical clean-main boundary."""
    started = time.monotonic()
    policy = deployment_policy(ROOT)
    pin, pin_sha = dependency_pin(ROOT)
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    local = verify_core_dependency(pin_path=ROOT / 'scripts/syncmate/core_dependency.json')
    if not local['ready']:
        raise ValueError('local Core environment is unverified: ' + '; '.join(local['errors']))
    runners = load_runners(policy)
    if node not in runners:
        raise ValueError('select a registered coordinator node')
    target = git('rev-parse', 'HEAD')
    directory = ROOT / '.workblock/runtime/install' / node / target
    directory.mkdir(parents=True, exist_ok=True)
    report = {'coordinator': node, 'target': target, 'nodes': list(runners),
              'status': 'blocked', 'before': {}, 'after': {}, 'restoration': {}, 'errors': []}
    try:
        for current, peer in runners.items():
            try:
                observed = invoke(peer, request_for(current, peer, action='inspect', target=target, policy=policy, pin=pin))
                report['before'][current] = observed
                verify_observation(observed, current, peer, pin_sha=pin_sha, idle=True)
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                report['errors'].append(current + ': ' + str(exc))
        if report['errors']:
            return 1
        versions = {r['head'] for r in report['before'].values()}
        if len(versions) != 1:
            raise ValueError('registered runners do not observe one shared code version')
        old = versions.pop()
        bundle, bundle_sha = '', None
        if old != target:
            subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', old, target], check=True)
            with tempfile.TemporaryDirectory(prefix='bundle-', dir=str(directory)) as temporary:
                path = Path(temporary) / 'code.bundle'
                subprocess.run(['git', '-C', str(ROOT), 'bundle', 'create', str(path), 'refs/heads/main', '^' + old],
                               check=True, capture_output=True)
                data = path.read_bytes()
                bundle, bundle_sha = base64.b64encode(data).decode('ascii'), hashlib.sha256(data).hexdigest()
        request = request_for(node, runners[node], action='apply', target=target, policy=policy, pin=pin)
        request.update(old=old, bundle=bundle, bundle_sha256=bundle_sha, node_ids=list(runners))
        installed = invoke(runners[node], request)
        report['shared_update'] = installed
        if (installed.get('status') not in ('installed', 'already_installed') or installed.get('head') != target
                or installed.get('origin_refs_unchanged') is not True
                or set(installed.get('nodes') or {}) != set(runners)):
            raise ValueError('shared update failed or omitted a registered node; retain state for diagnosis')
        for current, peer in runners.items():
            try:
                observed = invoke(peer, request_for(current, peer, action='inspect', target=target, policy=policy, pin=pin))
                report['after'][current] = observed
                verify_observation(observed, current, peer, pin_sha=pin_sha, target=target, idle=True)
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                report['errors'].append(current + ': ' + str(exc))
        if report['errors']:
            return 1
        for current, peer in runners.items():
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
        for current, peer in runners.items():
            expected = {'python_executable': peer['python_executable'], 'core_dependency_sha256': pin_sha}
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
        report['status'] = installed['status']
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
    parser.add_argument('action', choices=['apply', 'receipt'])
    parser.add_argument('--node', required=True, help='coordinator or receipt node; apply checks every registered runner')
    args = parser.parse_args(argv)
    try:
        if args.action == 'apply':
            return apply(args.node)
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
