"""Verify captured pilot evidence; report gate failure separately from evidence integrity."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.syncmate import syncmate
from scripts.syncmate.verify_core_dependency import verify_core_dependency
from syncmate_core.readiness import compare_readiness

BASE = Path(__file__).parent
def read(name):
    return json.loads((BASE / name).read_text(encoding='utf-8-sig'))


def main():
    remote = read('remote-probe.stdout.json')
    alias = read('alias-resolution.json')
    repro = read('queue-guard-repro.json')
    installed = verify_core_dependency()
    expected = {
        'device_identity': 'gpu4090',
        'gpu_model': 'NVIDIA GeForce RTX 4090', 'gpu_count': 1,
        'project_path': '/autodl-fs/data/OpenGU/GULib-master',
        'capabilities': ['ssh-runner', 'nvidia-gpu', 'verified-syncmate-core'],
    }
    capabilities = []
    if alias['resolved'] and remote['device']['role'] == 'runner':
        capabilities.append('ssh-runner')
    if remote['gpu']['available'] and remote['nvidia_smi']['exit_code'] == 0:
        capabilities.append('nvidia-gpu')
    if remote['core_dependency']['ready']:
        capabilities.append('verified-syncmate-core')
    observed = {
        'device_identity': remote['device']['device_id'],
        'gpu_model': (remote['gpu']['names'] or [None])[0],
        'gpu_count': remote['gpu']['count'], 'project_path': remote['project_path'],
        'capabilities': capabilities,
    }
    device = compare_readiness('gpu4090', 'AAGU-002 read-only pilot', expected, observed)
    refused = repro['cases']['explicit_refusal']
    incomplete = repro['cases']['missing_readiness']
    checks = {
        'alias_resolves_one_endpoint': alias['resolved'] and alias['single_endpoint'],
        'remote_clean_main': remote['git_branch']['stdout'] == 'main' and remote['git_status']['stdout'] == '',
        'device_facts_match_pilot_expectations': device['code'] == 'DEVICE_READY',
        'local_remote_exact_core_payload': installed['ready'] and remote['core_dependency']['ready']
            and installed['expected'] == remote['core_dependency']['expected'],
        'real_recipe_refused_existing_output': remote['real_existing_recipe_preflight']['ready'] is False
            and any('already exists' in error for error in remote['real_existing_recipe_preflight']['errors']),
        'controlled_missing_gpu_refused': remote['controlled_missing_gpu_preflight']['result']['ready'] is False
            and any('no CPU fallback' in error for error in remote['controlled_missing_gpu_preflight']['result']['errors']),
        'remote_queue_preserved': remote['queue_unchanged'] and remote['queue_before'] == remote['queue_after'],
        'no_remote_submission': remote['submitted_jobs'] == repro['remote_submissions'] == 0,
        'enqueue_gap_reproduced': refused['submitted'] is True and refused['inbox_created'] is True
            and refused['preflight_calls_before_enqueue'] == 0,
        'execution_refusal_retained': refused['run_once']['status'] == 'blocked' and refused['process_calls'] == 0,
        'incomplete_preflight_gap_reproduced': incomplete['binding']['ready'] is True,
    }
    payload = {
        'evidence_integrity_passed': all(checks.values()), 'checks': checks,
        'device_comparison': device,
        'expectation_sources': [
            'Accepted SM-005 evidence/d-full/queue-receipt.json runner_id=gpu4090',
            'Current ignored controller peer binding: gpu4090 -> autodl-opengu and canonical path',
            'Tracked experiments/syncmate_atomic_stage.py exact GPU and checkout checks',
        ],
        'device_comparison_limit': 'Manual normalized pilot comparison; not an enforced or reusable production dispatch receipt. GPU capacity was not measured.',
        'scope_note': 'This pilot checks device observations and isolated tool behavior. Current 002 acceptance also uses scope-smoke.json under the user clarified 002/007 boundary.',
        'local_core_dependency': installed,
        'sources_sha256': {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in (
            'remote_probe.py', 'remote-probe.stdout.json', 'alias-resolution.json',
            'queue_guard_repro.py', 'queue-guard-repro.json')},
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload['evidence_integrity_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
