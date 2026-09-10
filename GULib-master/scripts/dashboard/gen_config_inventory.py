"""Build the experiment inventory from reviewed research links and historical CSV.

No WorkItem status, graph, Git hook, job submission, or experiment execution is
performed here. Explicit experiment evidence review is a separate operation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / 'self/dashboard/experiment_inventory.json'
CSV_PATH = ROOT / 'self/dashboard/config_inventory.csv'
OUT_PATH = ROOT / 'self/dashboard/config_inventory.html'
TEMPLATE_PATH = Path(__file__).with_name('inventory.html')
RUN_STATES = {'unknown', 'pending', 'running', 'partial', 'failed', 'completed'}
ANALYSIS_STATES = {'unknown', 'pending', 'working', 'review', 'complete'}


def validate(data, rows):
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported inventory schema')
    ids, group_ids, categories = set(), set(), set()
    for group in data['groups']:
        if group['id'] in group_ids:
            raise ValueError('Duplicate research group')
        group_ids.add(group['id'])
        for category in group['legacy_categories']:
            if category in categories:
                raise ValueError('Historical category assigned twice')
            categories.add(category)
        for config in group['configs']:
            if config['id'] in ids:
                raise ValueError('Duplicate experiment config')
            ids.add(config['id'])
            state = config['run_state']
            if state not in RUN_STATES:
                raise ValueError('Unknown run state')
            expected, completed = config['expected'], config['completed']
            if expected is not None and (type(expected) is not int or expected <= 0):
                raise ValueError('Invalid expected count')
            if completed is not None and (type(completed) is not int or completed < 0 or expected is None or completed > expected):
                raise ValueError('Invalid completed count')
            if state == 'completed' and (expected is None or completed != expected or not config['runs']):
                raise ValueError('Completion requires counts and explicit run evidence')
            if state in {'running', 'partial', 'failed'} and not config['runs']:
                raise ValueError('Observed execution requires run evidence')
            if state == 'pending' and (not config['configs'] or completed != 0):
                raise ValueError('Pending requires a bound config and explicit zero completed')
            for run in config['runs']:
                if not all(run.get(k) for k in ('path', 'experiment_id', 'run_id', 'commit', 'sha256')):
                    raise ValueError('Run identity incomplete')
    for group in data['groups']:
        for analysis in group['analyses']:
            if analysis['state'] not in ANALYSIS_STATES or not set(analysis['inputs']).issubset(ids):
                raise ValueError('Invalid analysis state or input reference')
            if analysis['state'] != 'unknown' and not analysis['links']:
                raise ValueError('Analysis status needs a source')
    names = set()
    for row in rows:
        if row['name'] in names or row['cat'] not in categories:
            raise ValueError('Duplicate or unmapped historical config')
        names.add(row['name'])
        total, done = int(row['n_cells']), int(row['done'])
        if total <= 0 or not 0 <= done <= total:
            raise ValueError('Invalid historical coverage')
        for field in ('valid', 'rerun', 'accepted_remote'):
            if row.get(field) and not 0 <= int(row[field]) <= done:
                raise ValueError('Invalid historical evidence count')
        if sum(int(row.get(f) or 0) for f in ('valid','rerun','accepted_remote')) > done:
            raise ValueError('Historical evidence states overlap')


def walk_links(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'label' in obj:
            yield obj
        for value in obj.values():
            yield from walk_links(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_links(value)


def load_data(root=ROOT):
    root = Path(root)
    data = json.loads((root / 'self/dashboard/experiment_inventory.json').read_text(encoding='utf-8'))
    with (root / 'self/dashboard/config_inventory.csv').open(encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    validate(data, rows)
    # Exact archive filename match only; missing historical definitions stay unlinked.
    archive = root / 'docs/archive/experiment-configs-pre-aagu034'
    for row in rows:
        matches = list(archive.rglob(row['file'])) if Path(row['file']).name == row['file'] else []
        row['definition'] = {'label': '历史配置', 'path': matches[0].relative_to(root).as_posix()} if len(matches) == 1 else None
    data['legacy'] = rows
    return data


def check_links(data, root=ROOT):
    links = list(walk_links(data))
    missing = [link['path'] for link in links if not (root / link['path']).exists()]
    if missing:
        raise ValueError('Missing linked sources: ' + ', '.join(sorted(set(missing))))
    return len(links)


def verify_evidence(data, root=ROOT):
    """Verify only explicitly bound runs; never discover or submit an experiment."""
    files = 0
    for group in data['groups']:
        for config in group['configs']:
            observed = 0
            identities = set()
            for run in config['runs']:
                path = root / run['path']
                raw = path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != run['sha256']:
                    raise ValueError('Run manifest changed: ' + run['path'])
                manifest = json.loads(raw)
                for key in ('experiment_id', 'run_id', 'commit'):
                    if manifest[key] != run[key]:
                        raise ValueError('Run identity mismatch: ' + key)
                if manifest['config_path'] not in [c['path'] for c in config['configs']]:
                    raise ValueError('Run config does not match bound definition')
                for cell in manifest['cells']:
                    # A retry cannot add a second completion for the same logical cell.
                    identity = (run['experiment_id'], cell['cell_id'])
                    if cell['status'] == 'completed':
                        identities.add(identity)
                    for name, info in cell['files'].items():
                        artifact = (path.parent / cell['path'] / name).resolve()
                        try:
                            artifact.relative_to(path.parent.resolve())
                        except ValueError as exc:
                            raise ValueError('Artifact outside run') from exc
                        if hashlib.sha256(artifact.read_bytes()).hexdigest() != info['sha256']:
                            raise ValueError('Artifact checksum mismatch: ' + str(artifact))
                        files += 1
                files += 1
            observed = len(identities)
            if config['runs'] and observed != config['completed']:
                raise ValueError('Completion count differs from bound runs')
    return files


def render(data, root=ROOT):
    # WorkItem contents are never loaded: linking a record does not project its status.
    data = json.loads(json.dumps(data))
    for link in walk_links(data):
        target = (root / link['path']).resolve()
        relative = Path(os.path.relpath(target, root / 'self/dashboard')).as_posix()
        link['href'] = quote(relative, safe='/.:')
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('&', '\\u0026')
    return TEMPLATE_PATH.read_text(encoding='utf-8').replace('__DATA__', payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check deterministic output without writes')
    parser.add_argument('--check-links', action='store_true', help='Require linked sources on this device')
    parser.add_argument('--verify-evidence', action='store_true', help='Verify bound run identities and artifact hashes')
    args = parser.parse_args(argv)
    try:
        data = load_data()
        if args.check_links:
            print(f'Linked sources: {check_links(data)} PASS')
        if args.verify_evidence:
            print(f'Run/artifact checksums: {verify_evidence(data)} PASS')
        output = render(data)
        if args.check:
            if not OUT_PATH.exists() or OUT_PATH.read_text(encoding='utf-8') != output:
                raise ValueError('config_inventory.html is stale; regenerate from sources')
            print('Inventory check: PASS')
        else:
            OUT_PATH.write_text(output, encoding='utf-8')
            print(f'Wrote {OUT_PATH}')
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
