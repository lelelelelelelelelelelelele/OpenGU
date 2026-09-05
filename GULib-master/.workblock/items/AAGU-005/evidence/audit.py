"""Read-only audit of delivered OpenGU integration and its current seams.

Only this evidence directory is written. No jobs, datasets or producers run.
The exit code describes audit execution; integration findings retain PASS/FAIL.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CANONICAL = Path('E:/project/OpenGU/GULib-master')
SM = Path('E:/project/SyncMate')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts/syncmate'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    from scripts.syncmate import opengu_recipes as recipes
    from scripts.syncmate import opengu_adapter as adapter
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    from experiments import syncmate_atomic_stage as atomic
    from experiments.modular_execution import project_context
    from experiments.target_direct_v1 import syncmate_stage as target
    from syncmate_core.identity import sha256_recipe_config
    from syncmate_core.run_handoff import build_execution_contract

    delivered = 'e8f23a94dc7d753283442cadb1b45d8c1962234e'
    baseline = 'c9e094c55b42b2833fb24fcef5fe08f057605f68'
    subprocess.run(['git', 'merge-base', '--is-ancestor', delivered, baseline], cwd=ROOT, check=True)
    checked_paths = ['scripts/syncmate', 'experiments/syncmate_atomic_stage.py',
                     'experiments/modular_execution.py', 'tests/test_syncmate.py',
                     'tests/test_syncmate_atomic_stage.py']
    delta = git('diff', '--name-only', delivered, 'HEAD', '--', *checked_paths)
    registry = recipes.recipe_definitions()
    atomics = []
    for name, plan in atomic.PLANS.items():
        definition = registry[name]
        context = project_context(plan['experiment_id'], run_id=plan['run_id'],
                                  request_device='cuda', level='verification', repository_root=ROOT)
        contract = build_execution_contract(definition, project='opengu',
                                            job_id='aagu005-readonly-audit', git_sha=baseline)
        expected = [context.output.relative_to(ROOT).as_posix()]
        config_matches = sha256_recipe_config(ROOT / plan['config']) == definition['config_sha256']
        atomics.append({'recipe': name, 'config': plan['config'],
                        'config_sha256': definition['config_sha256'],
                        'declared_outputs': contract['artifact_paths'],
                        'executor_outputs': expected, 'config_matches': config_matches,
                        'status': 'PASS' if config_matches and contract['artifact_paths'] == expected else 'FAIL'})

    # Compare independent producer and queue declarations, without executing either.
    target_config = target.load_config()
    target_findings = []
    for name, definition in registry.items():
        scope = definition.get('gu_gate') or definition.get('gu_stage')
        if not scope:
            continue
        produced = set(target.gu_artifacts(scope['stage'], ratio=scope['ratio'],
                                          gate_only='gu_gate' in definition, config=target_config))
        declared = set(definition['expected_artifact_paths'])
        target_findings.append({'recipe': name, 'status': 'PASS' if declared == produced else 'FAIL',
                                'declared_count': len(declared), 'producer_count': len(produced),
                                'declared_but_not_produced': sorted(declared - produced),
                                'produced_but_not_declared': sorted(produced - declared)})

    visited = []
    original_preflight = target._formal_preflight
    original_pair = target._validate_selection_pair
    def guarded(config, stage, *, require_gpu):
        visited.append({'stage': stage, 'require_gpu': require_gpu})
        return {'git': {'head': git('rev-parse', 'HEAD')}, 'errors': ['read-only audit boundary']}
    def forbidden(*args, **kwargs):
        raise ValueError('formal data not inspected by code audit')
    target._formal_preflight = guarded
    target._validate_selection_pair = forbidden
    try:
        definition = registry['opengu-target-direct-gu-gate-r001-v2']
        result = adapter._target_gu_preflight(definition, ROOT / definition['config_path'])
        preflight = {'status': 'PASS' if (visited and result['ratio'] == .01
                     and result['gate_only'] is True and result['ready'] is False) else 'FAIL',
                     'result': result, 'calls': visited, 'runtime_ready_observed': False,
                     'scope': 'real signature, guarded device/data boundary; no runtime readiness claim'}
    finally:
        target._formal_preflight = original_preflight
        target._validate_selection_pair = original_pair

    source_files = [
        SM / '.workblock/items/SM-005/evidence/output-handoff/verification.json',
        SM / '.workblock/items/SM-005/evidence/output-handoff/opengu-tests.txt',
        SM / '.workblock/items/SM-005/evidence/output-handoff/core-tests.txt',
        SM / '.workblock/items/SM-005/evidence/verify-final.json',
        SM / '.workblock/items/SM-005/evidence/b-hutch32/cache-comparison.json',
        SM / '.workblock/items/SM-005/evidence/d-full/verification.json',
        SM / '.workblock/items/SM-005/evidence/auto-return/verification.json',
        CANONICAL / '.workblock/items/AAGU-028/evidence/observations.json',
        CANONICAL / '.workblock/runtime/aagu028-combination-verify.md',
        CANONICAL / '.workblock/runtime/install/c9e094c5-20260906/INSTALL-RESULT.json',
        SM / '.workblock/runtime/install/install-6a938e2a-20260906-46c192be/receipt.json',
    ]
    receipt = json.loads(source_files[-1].read_text(encoding='utf-8'))
    deployment = json.loads(source_files[-2].read_text(encoding='utf-8'))
    data = {
        'observed_at': dt.datetime.now().astimezone().isoformat(),
        'source': str(ROOT), 'source_head_at_audit': git('rev-parse', 'HEAD'),
        'product_baseline': git('rev-parse', 'HEAD'), 'previous_main': baseline, 'delivered_consumer': delivered,
        'delivery_is_ancestor': True, 'handoff_paths_changed_since_delivery': delta.splitlines(),
        'dependency_local': verify_core_dependency(), 'atomic_recipes': atomics,
        'formal_gu_recipe_audit': target_findings, 'formal_gu_preflight': preflight,
        'formal_config_hash_matches': sha256_recipe_config(ROOT / recipes.TARGET_DIRECT_CONFIG) == recipes.TARGET_DIRECT_CONFIG_SHA256,
        'consumer_deployment': {k: deployment.get(k) for k in
                                ('status', 'target', 'ssh_main', 'ssh_worktree', 'cache_preservation')},
        'core_install': {k: receipt.get(k) for k in
                         ('landedTarget', 'version', 'wheel_sha256', 'local_install', 'remote_install',
                          'status', 'local_temp_cleanup', 'remote_temp_cleanup')},
        'source_evidence': [{'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size}
                            for p in source_files],
        'runtime_boundary': {'jobs_submitted': 0, 'gpu_runs': 0, 'producers_called': 0,
                             'data_or_cache_mutations': False},
    }
    (HERE / 'repair-observations.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'atomic_pass': sum(r['status'] == 'PASS' for r in atomics),
                      'atomic_count': len(atomics), 'formal_gu_mismatch': sum(r['status'] == 'FAIL' for r in target_findings),
                      'formal_gu_count': len(target_findings), 'preflight': preflight,
                      'dependency_ready': data['dependency_local']['ready']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
