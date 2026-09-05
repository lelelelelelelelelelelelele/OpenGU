"""Check OpenGU 002's device/contract/smoke scope; never submit an experiment."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.syncmate import syncmate
from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
from scripts.syncmate.verify_core_dependency import verify_core_dependency
from syncmate_core import context, run_handoff


def main():
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=str(ROOT), text=True).strip()
    dependency = verify_core_dependency()
    extension = OpenGUProjectExtension()
    handoffs = []
    with context.use(ROOT, extension=extension):
        for name, definition in sorted(extension.recipes(ROOT).items()):
            contract = run_handoff.execution_contract(name, 'aagu002-contract-only', head)
            assert contract['timeout_seconds'] == definition['timeout_seconds']
            assert contract['recipe'] == name and contract['git_sha'] == head
            assert contract['config_sha256'] == definition['config_sha256']
            handoffs.append({'recipe': name, 'timeout_seconds': contract['timeout_seconds']})
    smoke = subprocess.run([sys.executable, '-B', str(ROOT/'scripts/syncmate/syncmate.py'), 'smoke', '--json'],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=90)
    result = json.loads(smoke.stdout)
    assert smoke.returncode == 0 and result['passed'] and all(result['checks'].values())
    canonical = Path('E:/project/OpenGU/GULib-master')
    audit = canonical/'.planning/cost-baseline-20260906/recent_timings.csv'
    with audit.open(encoding='utf-8-sig', newline='') as handle:
        records = list(csv.DictReader(handle))
    timing_evidence = []
    for row in records:
        path = Path(row['source'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == row['sha256'] and row['index_verified'] == 'True'
        timing_evidence.append({key: row[key] for key in (
            'run', 'source', 'sha256', 'score_hit', 'score_access_s', 'selection_access_s',
            'baseline_score_path_s', 'stored_gu_unlearn_s', 'fresh_gu_compute_s', 'current_gu_access_s')})
    payload = {
        'passed': dependency['ready'] and bool(handoffs) and len(timing_evidence) == 5,
        'source_checkpoint': head, 'dependency': dependency,
        'recipe_count': len(handoffs), 'handoffs': handoffs,
        'smoke_exit_code': smoke.returncode, 'smoke': result,
        'timing_evidence': timing_evidence,
        'timing_limits': [
            'timeout_seconds bounds a whole job, not an independently timed selector subphase',
            'HIT preserves historical baseline; current access cost is separate',
            'Missing GU access/model preparation timing remains unknown, not zero',
            'No claim that historical timing predicts the current formal 007 run',
        ],
        'scope': 'AAGU-002 device facts, existing field integration and smoke only; formal minimum experiment belongs to AAGU-007',
        'submitted_jobs': 0,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
