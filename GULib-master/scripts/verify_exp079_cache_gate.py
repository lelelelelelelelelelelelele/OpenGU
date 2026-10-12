"""Read collected cold/warm evidence for the 252-cell EXP-079 effect test.

No submission, cache writes, recovery or scientific acceptance. Ordinary Recipe
bindings and SyncMate's completed delivery precede this project-level check.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.syncmate.opengu_recipes import load_declaration
from syncmate_core.contracts import JOB_ID_RE
import yaml


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def audit_summary(snapshot, run_id, sha, mode):
    require(snapshot['run_id'] == run_id, 'audit run identity differs')
    stages, active, cache, phases = {}, {}, {}, Counter()
    terminal = None
    for event in snapshot['events']:
        require(event['git_sha'] == sha and event['metadata']['execution_run_id'] == run_id,
                'audit execution identity differs')
        stage, state, token = event['stage'], event['state'], event['run_id']
        stages.setdefault(stage, Counter())[state] += 1
        if state == 'started':
            require(token not in active, 'duplicate active audit entry')
            active[token] = stage
        elif state == 'completed':
            require(active.pop(token, None) == stage, 'unpaired completed audit entry')
            if stage == 'run':
                terminal = event['metadata']
            else:
                for name, seconds in event['metadata'].get('phase_seconds_exclusive', {}).items():
                    require(isinstance(seconds, (int, float)) and math.isfinite(seconds) and seconds >= 0,
                            'invalid audit phase duration')
                    phases[name] += seconds
                for fact in event.get('cache', []):
                    cache.setdefault(fact['type'], Counter())[fact['outcome']] += 1
        else:
            raise ValueError('failed or unknown audit state')
    require(not active and stages.get('run') == {'started': 1, 'completed': 1}, 'incomplete run audit')
    require(all(counts['started'] == counts['completed'] for counts in stages.values()), 'incomplete stage audit')
    require(cache.get('selection') == {'hit': 36} and cache.get('artifact') == {'hit': 252},
            'upstream audit is not all HIT')
    require(cache.get('result') == {'miss' if mode == 'cold' else 'hit': 684},
            'Evaluation audit does not match cold/warm requirement')
    return dict(cache=cache, entry_phase_seconds=dict(phases), run_metadata=terminal)


def verify_round(root, recipe_id, job_id, audit_path, sha, mode):
    require(JOB_ID_RE.fullmatch(job_id) and JOB_ID_RE.fullmatch(recipe_id), 'unsafe job or recipe ID')
    spec = load_declaration(root / 'scripts/syncmate/recipes' / (recipe_id + '.yaml'))
    config_file = root / spec['config_path']
    require(hashlib.sha256(config_file.read_bytes()).hexdigest() == spec['config_sha256'], 'configuration SHA differs')
    config = yaml.safe_load(config_file.read_text(encoding='utf-8'))
    require(len(config['seeds']) == 1 and spec['logical_cells'] == 252, 'not a single-seed 252-cell gate')
    delivery = read(root / '.syncmate/deliveries' / (job_id + '.json'))['result']
    require(delivery['ok'] and delivery['gate_passed'] and delivery['project_acceptance']['passed'],
            'SyncMate delivery or project result checks did not pass')
    require(delivery['project_acceptance']['accepted_cells'] == 252, 'delivery has partial cells')
    verified = delivery['verify']['summary']
    require(verified['status'] == 'verified' and verified['verified_current'] == 505
            and verified['missing'] == 0 and verified['conflicts'] == 0, 'delivery checksum verification is incomplete')
    job = delivery['completed_job']
    require(job['id'] == job_id and job['state'] == 'done' and job['recipe'] == recipe_id
            and job['expected_git_sha'] == sha, 'completed job identity differs')
    receipt = job['receipt']
    binding = receipt['output_contract']
    handoff = read(root / '.syncmate/runs' / (job_id + '.json'))['execution']
    for observed in (binding, handoff):
        require(observed['git_sha'] == sha and observed['recipe'] == recipe_id
                and observed['config_path'] == spec['config_path'] and observed['config_sha256'] == spec['config_sha256']
                and observed['run_identity'] == spec['run_identity'], 'execution binding differs from Recipe')
    require(binding['job_id'] == job_id and receipt['state'] == 'done', 'receipt identity differs')
    wall = (datetime.fromisoformat(receipt['finished_at']) - datetime.fromisoformat(receipt['started_at'])).total_seconds()
    queue = (datetime.fromisoformat(receipt['started_at']) - datetime.fromisoformat(receipt['submitted_at'])).total_seconds()
    require(0 < wall <= spec['timeout_seconds'] and queue >= 0, 'invalid or over-budget receipt time')
    run_id = spec['run_identity']['run_id']
    run_root = root / 'results/runs/gpu4090' / spec['run_identity']['experiment_id'] / run_id
    run = read(run_root / 'run.json')
    require(run['commit'] == sha and run['status'] == 'completed' and run['stage'] == 'unlearning'
            and run['experiment_id'] == spec['run_identity']['experiment_id'] and run['run_id'] == run_id
            and run['config_path'] == spec['config_path'], 'run identity differs')
    require(len(run['cells']) == 252 and len({c['cell_id'] for c in run['cells']}) == 252, 'partial or duplicate cells')
    datasets, methods, evaluation_counts, phases = Counter(), Counter(), Counter(), Counter()
    files = {}
    for cell in run['cells']:
        condition = cell['conditions']
        require(cell['status'] == 'completed' and condition['seed'] == config['seeds'][0]
                and condition['training_seed'] == config['seeds'][0] and condition['budget_ratio'] == 0.1,
                'cell conditions or completion differ')
        datasets[condition['dataset_name']] += 1
        methods[condition['method']] += 1
        for layer in ('score', 'selection', 'method'):
            require(cell['cache'][layer] == 'hit' and cell['producer_called'][layer] is False, 'upstream MISS or producer called')
        keys = {'evaluation'} | set(cell['cache_provenance']['evaluations'] if 'evaluations' in cell['cache_provenance'] else ())
        require(keys == {'evaluation'} | {k for k in cell['cache'] if k.startswith('post_')}, 'missing Evaluation provenance')
        for key in keys:
            require(cell['cache'][key] == ('miss' if mode == 'cold' else 'hit')
                    and cell['producer_called'][key] is (mode == 'cold'), 'unexpected Evaluation HIT/MISS or producer state')
            evaluation_counts[key] += 1
        phases.update(cell['timing']['current_access']['phase_seconds_exclusive'])
        for name in ('metrics.json', 'selection.json'):
            path = (run_root / cell['path'] / name).resolve()
            try:
                path.relative_to(run_root.resolve())
            except ValueError:
                raise ValueError('cell path escapes result root')
            content = path.read_bytes()
            require(hashlib.sha256(content).hexdigest() == cell['files'][name]['sha256'], 'collected file digest differs')
            files[(cell['cell_id'], name)] = content
    require(datasets == {'Cora': 84, 'CiteSeer': 84, 'PubMed': 84}, 'dataset matrix differs')
    require(methods == {name: 36 for name in ('GNNDelete','GIF','IDEA','MEGU','GraphEraser','GraphRevoker','Retrain')}, 'method matrix differs')
    require(evaluation_counts == {'evaluation': 252, 'post_unlearning_utility_and_retrain_gap': 216,
                                  'post_unlearning_flip_hop': 216}, 'Evaluation request matrix differs')
    audit = audit_summary(read(audit_path), run_id, sha, mode)
    facts = dict(run_id=run_id, job_id=job_id, seed=config['seeds'][0], runner_seconds=wall, queue_seconds=queue,
        started_at=receipt['started_at'], finished_at=receipt['finished_at'],
        cache_evaluations=dict(evaluation_counts), cell_method_phase_seconds=dict(phases), audit=audit)
    return spec, run, files, facts


def verify_pair(root, cold_recipe, warm_recipe, cold_job, warm_job, cold_audit, warm_audit, sha):
    require(re.fullmatch('[0-9a-f]{40}', sha), 'expected SHA must be a complete Git SHA')
    cold = verify_round(Path(root), cold_recipe, cold_job, cold_audit, sha, 'cold')
    warm = verify_round(Path(root), warm_recipe, warm_job, warm_audit, sha, 'warm')
    require(cold[0]['run_identity']['run_id'] != warm[0]['run_identity']['run_id'], 'cold and warm RID must differ')
    require(datetime.fromisoformat(warm[3]['started_at']) >= datetime.fromisoformat(cold[3]['finished_at']),
            'warm run started before cold run completed')
    for field in ('config_path', 'config_sha256', 'configuration_fingerprint', 'expected_datasets'):
        require(cold[0][field] == warm[0][field], 'cold/warm Recipe inputs differ')
    c = {cell['cell_id']:cell for cell in cold[1]['cells']}
    w = {cell['cell_id']:cell for cell in warm[1]['cells']}
    require(c.keys() == w.keys(), 'cold/warm cell identities differ')
    for key in c:
        for field in ('conditions', 'output', 'selection_id', 'cache_provenance'):
            require(c[key][field] == w[key][field], 'cold/warm scientific identity or reference differs')
    require(cold[2] == warm[2], 'cold/warm metric or Selection bytes differ')
    comparison = {}
    for mode, facts, seconds in (('cold',cold[3],790),('warm',warm[3],91)):
        comparison[mode] = dict(historical_seed=2024, historical_seconds=seconds,
            measured_seconds=facts['runner_seconds'], reduction_percent=100*(1-facts['runner_seconds']/seconds),
            improved=facts['runner_seconds'] < seconds, under_300_seconds=facts['runner_seconds'] < 300)
    return dict(passed=True, scope='252-cell engineering cold/warm effect test; no full-matrix scientific acceptance',
        execution_sha=sha, cold=cold[3], warm=warm[3], same_metric_and_selection_files=504,
        same_scientific_cells=252, historical_comparison=comparison,
        comparison_limit='Different training seed/environment from history; improvement booleans are observations, not acceptance thresholds')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=ROOT)
    parser.add_argument('--cold-recipe', default='opengu-exp079-cache-speed-gate-252-s212-cold')
    parser.add_argument('--warm-recipe', default='opengu-exp079-cache-speed-gate-252-s212-warm')
    for name in ('cold-job','warm-job','cold-audit','warm-audit','expected-sha'):
        parser.add_argument('--'+name, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = verify_pair(args.project,args.cold_recipe,args.warm_recipe,args.cold_job,args.warm_job,
            args.cold_audit,args.warm_audit,args.expected_sha)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps(dict(passed=False,error=str(exc)),ensure_ascii=False))
        return 1
    if args.output:
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
