"""Bounded CPU verification; raw logs and manifests stay in ignored runtime."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

TESTS = [
    'tests/test_retrain_outputs.py', 'tests/test_modular_consumers.py', 'tests/test_generic_cache_v2.py',
    'tests/test_collateral.py', 'tests/test_aagu009_collateral_repair.py', 'tests/test_update_detection_auc_policy.py',
    'tests/test_target_direct_recipe.py', 'tests/test_target_direct_manifest.py',
    'tests/test_target_direct_syncmate_stage.py', 'tests/test_cache_v2_runtime.py',
    'tests/test_target_checkpoint.py', 'tests/test_gnndelete_architecture.py',
    'tests/test_attack_manager.py', 'tests/test_selection_budget_planner.py',
    'tests/test_cache_v2_formal_artifacts.py', 'tests/test_run_experiments_timeouts.py',
    'tests/test_run_experiments_repair_validation.py',
]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def snapshot(roots):
    result = {}
    for root in roots:
        entries = {str(p.relative_to(root)): {'size': p.stat().st_size, 'sha256': digest(p)}
                   for p in sorted(root.rglob('*')) if p.is_file()}
        result[str(root)] = {'exists': root.exists(), 'files': entries}
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gnn-python', required=True)
    parser.add_argument('--authority', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[4]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    roots = [base / 'results' / name for base in (repo, args.authority.resolve())
             for name in ('cache', 'selection_cache', 'score_cache', 'cache_v2', 'runs')]
    before = snapshot(roots)
    write_json(output / 'protected-before.json', before)
    candidate = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
    dirty = subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo, text=True)
    if dirty:
        raise RuntimeError('Verify needs a clean candidate: ' + dirty)
    env = {**os.environ, 'CUDA_VISIBLE_DEVICES': '-1', 'PYTHONDONTWRITEBYTECODE': '1',
           'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1'}
    commands = [
        ('cpu', [args.gnn_python, '-B', '-X', 'utf8', '-m', 'pytest', *TESTS,
                 '-q', '--tb=short', '-o', 'junit_family=legacy', '--junitxml=' + str(output/'cpu.xml')]),
    ]
    results, consumers = [], []
    for label, command in commands:
        completed = subprocess.run(command, cwd=repo, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        (output / (label + '.log')).write_text(completed.stdout, encoding='utf-8')
        xml = ET.parse(output/(label+'.xml')).getroot()
        suites = [dict(suite.attrib) for suite in xml.iter('testsuite')]
        results.append({'label': label, 'command': command, 'exit_code': completed.returncode, 'suites': suites})
        for case in xml.iter('testcase'):
            values = {p.attrib['name']: p.attrib['value'] for p in case.iter('property')}
            if values:
                consumers.append({'test': case.attrib['name'], 'evidence': values})
        print(label, completed.returncode, suites, flush=True)
    command = [args.gnn_python, '-B', '-X', 'utf8', 'experiments/examples/retrain_cpu.py',
               '--directory', str(output / 'example')]
    completed = subprocess.run(command, cwd=repo, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
    (output / 'example.log').write_text(completed.stdout, encoding='utf-8')
    results.append({'label': 'example', 'command': command, 'exit_code': completed.returncode})
    example = json.loads((output / 'example/receipt.json').read_text(encoding='utf-8')) if completed.returncode == 0 else None
    after = snapshot(roots)
    write_json(output/'protected-after.json', after)
    protected = [{'root': root, 'exists': before[root]['exists'], 'file_count': len(before[root]['files']),
                  'before_sha256': hashlib.sha256(json.dumps(before[root], sort_keys=True).encode()).hexdigest(),
                  'after_sha256': hashlib.sha256(json.dumps(after[root], sort_keys=True).encode()).hexdigest(),
                  'unchanged': before[root] == after[root]} for root in before]
    receipt = {'candidate':candidate, 'source': str(repo), 'checks': results, 'protected_roots':protected,
               'protected_unchanged':before == after, 'consumer_evidence':consumers,
               'raw_evidence_directory': str(output), 'example': example}
    write_json(output/'verification.json', receipt)
    if before != after or any(item['exit_code'] for item in results):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
