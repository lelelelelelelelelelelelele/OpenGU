"""AAGU-023 bounded evidence packaging and read-only archive verification.

No move/delete, SQL, experiment imports, or result writes. `package` preserves
original receipt bytes; `observe` writes only a new evidence observation file.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
GROUPS = {
    'ssh-rework-20260903': [
        'archive-intent.json', 'archive-register-receipt.json',
        'archive-move-receipt.json', 'paired-ledger-prepared.json',
        'archive-publish-receipt.json', 'paired-ledger-final.json', 'verification.json'],
    'cache-archive-20260904': [
        'manifest.json', 'ledger-prepared.json', 'ledger-final.json',
        'local-register.json', 'ssh-register.json', 'local-move.json',
        'ssh-move.json', 'local-publish.json', 'ssh-publish.json'],
    'v2-archive-20260904': [
        'manifest.json', 'ledger-prepared.json', 'ledger-final.json',
        'local-register.json', 'ssh-register.json', 'local-move.json',
        'ssh-move.json', 'local-publish.json', 'ssh-publish.json',
        'local-lookup-check.json', 'ssh-lookup-check.json'],
}
LEDGERS = {
    'ssh-rework-20260903/paired-ledger-final.json': '8039295f509cedbab7e13de7364250670b44f2fcac52eca877efdee2dbb1ecc9',
    'cache-archive-20260904/ledger-final.json': 'cb8b23678d0f0e33feaa2ce64b27c944674dd484bc2de770a58eadf9be5418c2',
    'v2-archive-20260904/ledger-final.json': 'c99fef13f5eccb0886aee69d147d11d12dd37f6076e5ba42e0a8ce589da4b103',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(relative):
    return json.loads((HERE / 'archive' / relative).read_text(encoding='utf-8'))


def package(runtime):
    records = []
    for group, names in GROUPS.items():
        for name in names:
            relative = group + '/' + name
            data = (runtime / relative).read_bytes()
            if relative in LEDGERS and sha(data) != LEDGERS[relative]:
                raise ValueError('Original ledger drift: ' + relative)
            target = HERE / 'archive' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if target.read_bytes() != data:
                    raise ValueError('Packaged evidence drift: ' + relative)
            else:
                with target.open('xb') as out:
                    out.write(data)
            records.append({'path': relative, 'bytes': len(data), 'sha256': sha(data)})
    target = HERE / 'archive' / 'index.json'
    data = (json.dumps(records, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    # This file is a rebuildable package index; source receipts stay write-once.
    target.write_bytes(data)
    return {'packaged_files': len(records), 'bytes': sum(r['bytes'] for r in records)}


def check_bundle():
    index = json.loads((HERE / 'archive/index.json').read_text(encoding='utf-8'))
    expected = {g + '/' + n for g, names in GROUPS.items() for n in names}
    if {r['path'] for r in index} != expected or len(index) != len(expected):
        raise ValueError('Evidence index membership mismatch')
    for row in index:
        data = (HERE / 'archive' / row['path']).read_bytes()
        if (len(data), sha(data)) != (row['bytes'], row['sha256']):
            raise ValueError('Evidence bytes drift: ' + row['path'])
    for p, expected_sha in LEDGERS.items():
        if sha((HERE / 'archive' / p).read_bytes()) != expected_sha:
            raise ValueError('Ledger identity drift: ' + p)
    failed = read('ssh-rework-20260903/verification.json')
    legacy = read('cache-archive-20260904/ledger-final.json')
    v2 = read('v2-archive-20260904/ledger-final.json')
    full_register = read('ssh-rework-20260903/archive-register-receipt.json')
    full_move = read('ssh-rework-20260903/archive-move-receipt.json')
    for receipt in [full_register, full_move]:
        if receipt['intent_sha256'] != sha((HERE / 'archive/ssh-rework-20260903/archive-intent.json').read_bytes()):
            raise ValueError('Failed attempt intent mismatch')
        if receipt['ledger_sha256'] != sha((HERE / 'archive/ssh-rework-20260903/paired-ledger-prepared.json').read_bytes()):
            raise ValueError('Failed attempt prepared ledger mismatch')
    full_events = [json.loads(line) for line in full_move['events_jsonl'].splitlines()]
    if [e['state'] for e in full_events] != ['PREPARED', 'MOVE_STARTED', 'ARCHIVED_FAILED_ATTEMPT_VERIFIED']:
        raise ValueError('Failed attempt event sequence mismatch')
    if full_events[0]['timestamp'] >= full_events[1]['timestamp']:
        raise ValueError('Failed attempt registration order mismatch')
    for group, ledger in [('cache-archive-20260904', legacy), ('v2-archive-20260904', v2)]:
        for device in ['local', 'ssh']:
            register = read(group + '/' + device + '-register.json')
            publish = read(group + '/' + device + '-publish.json')
            for receipt in [register, publish]:
                for key, filename in [('manifest_sha256', 'manifest.json'), ('prepared_ledger_sha256', 'ledger-prepared.json')]:
                    if receipt[key] != sha((HERE / 'archive' / group / filename).read_bytes()):
                        raise ValueError('Registration evidence mismatch: ' + group)
            if publish['final_ledger_sha256'] != LEDGERS[group + '/ledger-final.json']:
                raise ValueError('Publication evidence mismatch: ' + group)
            recorded = ledger['verification']['receipts'][device]
            for key, suffix in [('registration_sha256', '-register.json'), ('move_sha256', '-move.json')]:
                if recorded[key] != sha((HERE / 'archive' / group / (device + suffix)).read_bytes()):
                    raise ValueError('Receipt binding mismatch: ' + group)
    if failed['deletions'] or legacy['deletions'] or v2['deletions'] or v2['sql_writes'] or v2['payload_or_header_rewrites']:
        raise ValueError('Zero-mutation boundary failed')
    for ledger, flag in [(legacy, 'both_devices_registered_before_first_move'), (v2, 'all_registered_before_first_move')]:
        if not ledger['verification'][flag]:
            raise ValueError('Registration-before-move missing')
        events = [e for r in ledger['verification']['receipts'].values() for e in r['events']]
        registrations = [e['timestamp'] for e in events if e['state'] == 'REGISTERED_BEFORE_MOVE']
        moves = [e['timestamp'] for e in events if e['state'] == 'MOVE_STARTED']
        if not registrations or not moves or max(registrations) >= min(moves):
            raise ValueError('Both devices must register before first move')
    files = failed['remote_moved_files'] + legacy['verification']['files_preserved'] + v2['verification']['files_preserved']
    sizes = failed['remote_moved_bytes'] + legacy['verification']['bytes_preserved'] + v2['verification']['bytes_preserved']
    if (files, sizes, v2['verification']['artifacts_archived']) != (1115, 26040188, 16):
        raise ValueError('Archive totals mismatch')
    return {'files': files, 'bytes': sizes, 'old_v2_artifacts': 16, 'deletions': 0, 'receipt_files': len(index)}


def request(device):
    groups, absent, ledgers = [], [], []
    legacy = read('cache-archive-20260904/manifest.json')['devices'][device]
    for name in ['cache', 'selection_cache', 'score_cache']:
        tree = legacy['roots'][name]
        src = 'results/' + name
        dst = 'results/_archive_aagu023_20260904/legacy_cache/' + name
        absent.append(src)
        groups.append({'path': dst, 'files': tree['files']})
    v2 = read('v2-archive-20260904/manifest.json')['devices'][device]['full_v2']
    files = [f for f in v2['files'] if f['path'] != 'legacy_freeze.json']
    groups.append({'path': 'results/_archive_aagu023_20260904/v2_retired/cache_v2', 'files': files})
    absent += ['results/cache_v2/c_target_v1', 'results/cache_v2/bc_target_v2',
               'results/cache_v2/index.sqlite', 'results/cache_v2/artifacts',
               'results/cache_v2/producer_counter.json', 'results/cache_v2/trace.jsonl']
    for group, folder in [('cache-archive-20260904', ''), ('v2-archive-20260904', 'v2_retired/')]:
        for filename in ['manifest.json', 'ledger-final.json']:
            ledgers.append({'path': 'results/_archive_aagu023_20260904/' + folder + filename,
                            'sha256': sha((HERE / 'archive' / group / filename).read_bytes())})
    if device == 'ssh':
        intent = read('ssh-rework-20260903/archive-intent.json')
        root = intent['source']
        absent.append(root)
        groups.append({'path': intent['destination'], 'files': [
            dict(f, path=f['path'][len(root) + 1:]) for f in intent['files']]})
        ledgers.append({'path': 'results/_archive_aagu023_20260903/paired-ledger-final.json',
                        'sha256': LEDGERS['ssh-rework-20260903/paired-ledger-final.json']})
    return {'device': device, 'groups': groups, 'absent': absent, 'ledgers': ledgers,
            'active_v2_files': [f for f in v2['files'] if f['path'] == 'legacy_freeze.json']}


def safe_path(root, relative):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != 'results':
        raise ValueError('Out-of-scope path: ' + relative)
    current = root
    for part in p.parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
            raise ValueError('Link in evidence path: ' + relative)
    current.resolve().relative_to(root.resolve())
    return current


def probe(repo, req):
    """Portable stdlib-only read operation, also used over SSH stdin."""
    root = Path(repo).resolve()
    checked, byte_count, problems = 0, 0, []
    groups = list(req['groups']) + [{'path': 'results/cache_v2', 'files': req['active_v2_files']}]
    for group in groups:
        path = safe_path(root, group['path'])
        if not path.is_dir():
            problems.append('missing directory: ' + group['path'])
            continue
        observed = set()
        for p in path.rglob('*'):
            safe_path(root, p.relative_to(root).as_posix())
            if p.is_file():
                observed.add(p.relative_to(path).as_posix())
        expected = {f['path'] for f in group['files']}
        if observed != expected:
            problems.append('file set drift: ' + group['path'])
        for f in group['files']:
            p = safe_path(root, group['path'] + '/' + f['path'])
            if not p.is_file() or p.stat().st_size != f['bytes'] or sha(p.read_bytes()) != f['sha256']:
                problems.append('file content drift: ' + p.relative_to(root).as_posix())
            else:
                checked += 1
                byte_count += f['bytes']
    for relative in req['absent']:
        if safe_path(root, relative).exists():
            problems.append('old active path exists: ' + relative)
    ledger_hashes = {}
    for f in req['ledgers']:
        p = safe_path(root, f['path'])
        actual = sha(p.read_bytes()) if p.is_file() else None
        ledger_hashes[f['path']] = actual
        if actual != f['sha256']:
            problems.append('ledger drift: ' + f['path'])
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, env=env, text=True).strip()
    return {'device': req['device'], 'observed_at': datetime.now(timezone.utc).isoformat(),
            'repo': str(root), 'head': head, 'status': 'PASS' if not problems else 'FAIL',
            'files_checked_including_retained_freeze': checked, 'bytes_checked': byte_count,
            'old_paths_absent': req['absent'], 'ledger_hashes': ledger_hashes, 'problems': problems}


def observe(repo, output):
    totals = check_bundle()
    local = probe(repo, request('local'))
    code = Path(__file__).read_text(encoding='utf-8').rsplit("\nif __name__ == '__main__':", 1)[0]
    code += "\nprint(json.dumps(probe('/autodl-fs/data/OpenGU/GULib-master', json.load(sys.stdin))))\n"
    # __file__ is only used for HERE (not by probe); no file is created on SSH.
    code = "__file__ = '/nonexistent/aagu023_readonly_probe.py'\n" + code
    encoded = base64.b64encode(code.encode()).decode()
    command = 'exec(__import__("base64").b64decode("' + encoded + '"))'
    remote = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15', 'autodl-opengu',
                             '/root/miniconda3/bin/python', '-B', '-c', "'" + command + "'"],
                            input=json.dumps(request('ssh')), capture_output=True, text=True, timeout=60)
    if remote.returncode:
        raise RuntimeError('SSH read-only verification failed: ' + remote.stderr)
    ssh = json.loads(remote.stdout)
    result = {'totals': totals, 'local': local, 'ssh': ssh,
              'status': 'PASS' if local['status'] == ssh['status'] == 'PASS' else 'FAIL'}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['package', 'check', 'observe'])
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.action == 'package':
        result = package(args.runtime)
    elif args.action == 'check':
        result = check_bundle()
    else:
        result = observe(args.repo, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get('status') == 'FAIL':
        sys.exit(1)
