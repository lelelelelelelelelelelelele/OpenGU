"""Verify configuration evidence; all process logs are ignored runtime evidence."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RUNTIME = ROOT / '.workblock/runtime/aagu015'


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def run(label, args):
    result = subprocess.run(args, cwd=ROOT, text=True, encoding='utf-8', capture_output=True)
    (RUNTIME / (label + '.stdout.txt')).write_text(result.stdout, encoding='utf-8')
    (RUNTIME / (label + '.stderr.txt')).write_text(result.stderr, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(label + ' failed: ' + result.stderr[-2000:] + result.stdout[-2000:])
    return result


def protected_snapshot():
    result = {}
    for relative in ('data', 'results/cache_v2', 'results/cache', 'results/selection_cache',
                     'results/score_cache', 'results/runs', 'results/_journal'):
        root = ROOT / relative
        if not root.exists():
            result[relative] = None
        else:
            result[relative] = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in sorted(root.rglob('*')) if path.is_file()}
    return result


def main():
    sys.path.insert(0, str(ROOT))
    from experiments.aagu015.definitions import dry_run

    RUNTIME.mkdir(parents=True, exist_ok=True)
    identity = run('git-head', ['git', 'rev-parse', 'HEAD']).stdout.strip()
    source_status = run('git-status', ['git', 'status', '--porcelain', '--untracked-files=all']).stdout
    before = protected_snapshot()
    python = [sys.executable, '-B', '-X', 'utf8']
    tests = run('tests', python + ['-m', 'pytest', 'tests/test_aagu015_definitions.py', '-q', '-p', 'no:cacheprovider'])
    expansion = dry_run()
    write_json(RUNTIME / 'definition-expansion.json', expansion)
    examples = {'cli-stage-s': 'stage_s/cora-seed42-r0.01.yaml',
                'cli-stage-u': 'stage_u/cora-seed42-r0.01-degree.yaml'}
    for label, relative in examples.items():
        result = run(label, python + ['experiments/run.py', 'experiments/configs/aagu015/generated/' + relative, '--dry_run'])
        parsed = json.loads(result.stdout)
        assert parsed['dry_run'] is True and parsed['producer_called'] is False
    run('dashboard-check', python + ['scripts/dashboard/refresh.py', '--check'])
    after = protected_snapshot()
    assert before == after, 'protected dataset/cache/result tree changed during verification'
    summary = {key: value for key, value in expansion.items() if key not in (
        'configuration_sources', 'stage_s', 'stage_u', 'preparation_groups', 'score_groups', 'selection_groups')}
    summary['full_expansion'] = '.workblock/runtime/aagu015/definition-expansion.json'
    summary['cli_examples'] = examples
    summary['verification'] = {'targeted_tests': 8, 'real_cli_examples': 2,
        'protected_tree_unchanged': True, 'files_hashed': sum(len(v) for v in before.values() if v is not None)}
    write_json(HERE / 'definition-summary.json', summary)
    for stage in ('s', 'u'):
        rows = expansion['stage_' + stage]
        keys = ('cell', 'dataset', 'selector', 'expected_candidate_count', 'planned_k', 'preparation_group',
                'score_group', 'selection_group', 'configuration') if stage == 's' else (
                'cell', 'selection_source_cell', 'method', 'effective_gu', 'configuration', 'execution_ready')
        with (HERE / ('stage-' + stage + '-cells.csv')).open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
    receipt = {'tested_checkpoint': identity if not source_status else None,
        'source_head': identity, 'source_clean': not source_status,
        'configuration_digest': expansion['configuration_digest'],
        'checks': ['8 targeted tests', '324 accepted-parser plans', '2 real CLI dry-runs', 'dashboard projection'],
        'protected_tree_before': before, 'protected_tree_after_equal': True,
        'experiment_execution': 'NOT OBSERVED', 'whole_block_verify': 'NOT OBSERVED',
        'claim_phase': 'ongoing', 'test_stdout': tests.stdout}
    write_json(RUNTIME / 'verification.json', receipt)
    print(json.dumps({'checkpoint': identity, 'counts': expansion['counts'], **summary['verification']}))


if __name__ == '__main__':
    main()
