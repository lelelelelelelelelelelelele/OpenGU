"""One registered project action: exact Git deployment with Core coordination."""
import argparse
import base64
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def ssh(peer, argv, *, payload=None, timeout=240):
    return subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=20', '--',
                           peer['ssh'], shlex.join(argv)], input=payload,
                          capture_output=True, text=True, encoding='utf-8', timeout=timeout)


def apply():
    if ROOT.resolve() != Path('E:/project/OpenGU/GULib-master').resolve():
        raise ValueError('installation must run from the canonical landed project')
    from syncmate_core import context, devices
    with context.use(ROOT):
        device, warnings = devices.load_device(ROOT / '.syncmate/device.yaml')
    if warnings:
        raise ValueError('; '.join(warnings))
    peer = device['peers']['gpu4090']
    if peer['ssh'] != 'autodl-opengu' or peer['repo_path'].rstrip('/') != '/autodl-fs/data/OpenGU/GULib-master':
        raise ValueError('device does not match registered install target')
    target = git('rev-parse', 'HEAD')
    if git('branch', '--show-current') != 'main' or git('status', '--porcelain=v1', '-uall'):
        raise ValueError('installation requires clean main')
    origin = git('ls-remote', 'origin', 'refs/heads/main').split()[0]
    if origin != target:
        raise ValueError('origin main differs from landed target')
    remote_repo = '/autodl-fs/data/OpenGU'
    probe = ssh(peer, ['git', '-C', remote_repo, 'rev-parse', 'HEAD'], timeout=30)
    if probe.returncode:
        raise ValueError('could not read remote Git identity')
    old = probe.stdout.strip()
    import re
    if not re.fullmatch('[0-9a-f]{40}', old):
        raise ValueError('invalid remote Git identity')
    # Bundle is an immutable bounded fallback; no remote state is changed here.
    bundle = ''
    if old != target:
        subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', old, target], check=True)
        staging = ROOT / '.workblock/runtime/install'
        staging.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='bundle-', dir=str(staging)) as directory:
            path = Path(directory) / 'code.bundle'
            subprocess.run(['git', '-C', str(ROOT), 'bundle', 'create', str(path),
                            'refs/heads/main', '^' + old], check=True, capture_output=True)
            bundle = base64.b64encode(path.read_bytes()).decode('ascii')
    code = Path(__file__).with_name('install_remote.py').read_text(encoding='utf-8')
    request = json.dumps({'target': target, 'old': old, 'project': peer['repo_path'], 'bundle': bundle})
    response = ssh(peer, [devices.peer_python_executable(peer), '-B', '-c', code], payload=request)
    try:
        result = json.loads(response.stdout)
    except ValueError as exc:
        raise ValueError('installation response unavailable; do not retry until remote state is diagnosed') from exc
    directory = ROOT / '.workblock/runtime/install' / target
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / 'receipt.json'
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'receipt': str(path), **result}, ensure_ascii=False))
    return 0 if response.returncode == 0 and result['status'] in ('installed', 'already_installed') else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['apply', 'receipt'])
    args = parser.parse_args(argv)
    try:
        if args.action == 'apply':
            return apply()
        target = git('rev-parse', 'HEAD')
        path = ROOT / '.workblock/runtime/install' / target / 'receipt.json'
        result = json.loads(path.read_text(encoding='utf-8'))
        if result.get('target') != target or result.get('head') != target or result.get('status') not in ('installed', 'already_installed'):
            raise ValueError('installation receipt is not successful for this target')
        print(json.dumps({'receipt': str(path), **result}))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc) if isinstance(exc, ValueError) else type(exc).__name__}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
