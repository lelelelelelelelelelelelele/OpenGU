"""Registered node-specific private Git installation and fresh initialization."""
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

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.syncmate.deployment_policy import (
    deployment_policy, receipt_path, validate_peer, validate_receipt)


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def ssh(peer, argv, *, payload=None, timeout=240):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20', '--',
                           peer['ssh'], shlex.join(argv)], input=payload,
                          capture_output=True, text=True, encoding='utf-8', timeout=timeout)


def selected_peer(node, policy):
    from syncmate_core import context, devices
    with context.use(ROOT):
        device, warnings = devices.load_device(ROOT / '.syncmate/device.yaml')
    if warnings:
        raise ValueError('; '.join(warnings))
    peer = device.get('peers', {}).get(node)
    validate_peer(peer, node, policy)
    return peer


def apply(node, *, initialize=False):
    started = time.monotonic()
    if ROOT.resolve() != Path('E:/project/OpenGU/GULib-master').resolve():
        raise ValueError('installation must run from the canonical landed project')
    policy = deployment_policy(ROOT)
    peer = selected_peer(node, policy)
    target = git('rev-parse', 'HEAD')
    if git('branch', '--show-current') != 'main' or git('status', '--porcelain=v1', '-uall'):
        raise ValueError('installation requires clean main')
    old = None
    if not initialize:
        remote_repo = str(Path(peer['repo_path']).parent).replace('\\', '/')
        probe = ssh(peer, ['git', '-C', remote_repo, 'rev-parse', 'HEAD'], timeout=30)
        if probe.returncode:
            raise ValueError('could not read remote Git identity')
        old = probe.stdout.strip()
        import re
        if not re.fullmatch('[0-9a-f]{40}', old):
            raise ValueError('invalid remote Git identity')
        if old != target:
            subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', old, target], check=True)
    bundle = ''
    bundle_sha256 = None
    if initialize or old != target:
        staging = ROOT / '.workblock/runtime/install' / node
        staging.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='bundle-', dir=str(staging)) as directory:
            path = Path(directory) / 'code.bundle'
            command = ['git', '-C', str(ROOT), 'bundle', 'create', str(path), 'refs/heads/main']
            if old is not None:
                command.append('^' + old)
            subprocess.run(command, check=True, capture_output=True)
            data = path.read_bytes()
            bundle_sha256 = hashlib.sha256(data).hexdigest()
            bundle = base64.b64encode(data).decode('ascii')
    code = Path(__file__).with_name('install_remote.py').read_text(encoding='utf-8')
    request = json.dumps({'action': 'initialize' if initialize else 'apply', 'node': node,
        'ssh': peer['ssh'], 'target': target, 'old': old, 'project': peer['repo_path'],
        'bundle': bundle, 'bundle_sha256': bundle_sha256,
        'transport': policy['transport'], 'policy_sha256': policy['sha256']})
    from syncmate_core import devices
    response = ssh(peer, [devices.peer_python_executable(peer), '-B', '-c', code], payload=request)
    try:
        result = json.loads(response.stdout)
        if not isinstance(result, dict):
            raise ValueError('installation response must be an object')
    except ValueError as exc:
        raise ValueError('installation response unavailable; do not retry until remote state is diagnosed') from exc
    if response.returncode == 0:
        try:
            validate_receipt(result, node, target, policy, bundle_sha256=bundle_sha256)
        except ValueError as exc:
            result.update(status='failed', error=str(exc))
    result['elapsed_seconds'] = round(time.monotonic() - started, 2)
    path = receipt_path(ROOT, node, target, policy)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'receipt': str(path), **result}, ensure_ascii=False))
    return 0 if response.returncode == 0 and result['status'] in ('initialized', 'installed', 'already_installed') else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['apply', 'initialize', 'receipt'])
    parser.add_argument('--node', required=True, help='registered deployment peer ID')
    args = parser.parse_args(argv)
    try:
        if args.action != 'receipt':
            return apply(args.node, initialize=args.action == 'initialize')
        policy = deployment_policy(ROOT)
        selected_peer(args.node, policy)
        target = git('rev-parse', 'HEAD')
        path = receipt_path(ROOT, args.node, target, policy)
        if path.is_symlink():
            raise ValueError('installation receipt must not be linked')
        result = json.loads(path.read_text(encoding='utf-8'))
        validate_receipt(result, args.node, target, policy)
        print(json.dumps({'receipt': str(path), **result}))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc) if isinstance(exc, ValueError) else type(exc).__name__}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
