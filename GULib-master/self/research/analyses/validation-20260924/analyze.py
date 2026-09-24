"""Audit the accepted EXP-067/068 H64 Validate runs from verified local returns.

Reuses the calibration analyzer's numerical criteria per fixed candidate/request.
This analysis reads original run-commit configuration and never changes parameters.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from experiments.analyze_observer_calibration import (
    evaluate_candidate, load_theory, read_git_yaml, resolve_config_ref,
    OBSERVER_VERSIONS, LIMITS,
)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def analyze(number):
    dataset = {'067': 'CiteSeer', '068': 'PubMed'}[number]
    job = f'aagu{number}-h64-validation-20260924'
    handoff = read(ROOT/f'.syncmate/runs/{job}.json')
    delivery = read(ROOT/f'.syncmate/deliveries/{job}.json')
    execution = handoff['execution']
    assert delivery['execution'] == execution
    result = delivery['result']
    verify = result['verify']
    assert result['status'] == 'accepted' and not result['errors']
    assert not any(verify[k] for k in ['missing', 'conflicts', 'errors'])
    verified = {a['path']: a['sha256'] for a in verify['verified']}
    assert len(verified) == len(verify['verified']) == 115
    assert set(verified) == set(execution['artifact_paths'])
    for relative, sha in verified.items():
        p = ROOT/'results/runs/gpu4090'/Path(relative).relative_to('results/runs')
        assert hashlib.sha256(p.read_bytes()).hexdigest() == sha
    run_relative = next(p for p in verified if p.endswith('/run.json'))
    run_path = ROOT/'results/runs/gpu4090'/Path(run_relative).relative_to('results/runs')
    run = read(run_path)
    assert run['status'] == 'completed' and run['commit'] == execution['git_sha']
    assert run['run_id'] == execution['run_identity']['run_id']
    assert run['config_path'] == execution['config_path']
    assert len(run['cells']) == 21 and len({c['cell_id'] for c in run['cells']}) == 21
    table, _ = read_git_yaml(ROOT, run['commit'], run['config_path'], 'Validate table')
    assert table['random_selector_seeds'] == [104246, 104247, 104248]
    assert table['budget_ratios'] == [0.1]
    config_directory = str(Path(run['config_path']).parent).replace('\\', '/')
    configs = {}
    for ref in table['unlearning_refs']:
        path = resolve_config_ref(config_directory, ref, 'unlearning_refs')
        configs[ref], _ = read_git_yaml(ROOT, run['commit'], path, 'method')
    archive = read(ROOT/f'self/research/analyses/EXP-{number}/observer-calibration-h64-20260924.json')
    frozen = next(c for c in archive['cases'] if c['dataset'] == dataset and c['hidden_channels'] == 64)
    theory, methods, _ = load_theory(ROOT/f'self/research/analyses/h64-theory-20260924/{dataset.lower()}.json')
    groups = collections.defaultdict(list)
    selections = collections.defaultdict(set)
    utility = collections.defaultdict(dict)
    cache_counts = collections.defaultdict(collections.Counter)
    for cell in run['cells']:
        conditions = cell['conditions']
        seed, method = conditions['random_selector_seed'], conditions['method']
        config = configs[conditions['unlearning_ref']]
        assert conditions['dataset_name'] == dataset and conditions['seed'] == 42
        assert conditions['budget_ratio'] == 0.1 and cell['status'] == 'completed'
        assert config['model']['hidden_channels'] == 64
        folder = run_path.parent/cell['path']
        selection = read(folder/'selection.json')
        selections[seed].add(tuple(selection['selected_nodes']))
        metrics = read(folder/'metrics.json')
        f1 = next(row['values']['f1'] for row in metrics['rows'] if row['stage'] == 'method')
        cache_counts[method][cell['cache']['method']] += 1
        if method == 'Retrain':
            assert config['training'] == {'seed':42,'epochs':3000,'optimizer':'Adam','lr':0.05,'weight_decay':0.0001,'scheduler':'none'}
            utility[seed]['retrain_f1'] = f1
            continue
        assert cell['producer_called']['method'] and cell['cache']['method'] == 'disabled'
        for key in ['scale', 'damp']:
            assert config['parameters'][key] == frozen['methods'][method]['frozen_parameters'][key]
        refs = {ref['name']: ref for ref in cell['observers']}
        assert set(refs) == set(OBSERVER_VERSIONS)
        documents = {}
        for name, ref in refs.items():
            identity = ref['identity']
            assert ref['status'] == 'completed' and ref['semantic_version'] == OBSERVER_VERSIONS[name]
            assert identity['commit'] == run['commit'] and identity['run_id'] == run['run_id']
            assert identity['cell_id'] == cell['cell_id'] and identity['conditions'] == conditions
            assert identity['output_identity']['target']['checkpoint_state_hash'] == frozen['checkpoint']['state_hash']
            for relative, info in ref['files'].items():
                assert cell['files'][relative] == info
                raw = (folder/relative).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == info['sha256']
                kind = 'trace' if relative.endswith('.jsonl') else 'result'
                documents[(cell['cell_id'],name,kind)] = [json.loads(x) for x in raw.decode('utf-8').splitlines() if x] if kind == 'trace' else json.loads(raw)
        entry = {'cell':cell,'observer_refs':refs,'documents':documents,'output_target':refs['hessian_calibration']['identity']['output_identity']['target'],'candidate_config':config}
        groups[(seed,method)].append(entry)
        if config['parameters']['iteration'] == 100:
            change = documents[(cell['cell_id'],'same_graph_change','result')]['measurements']['graphs']
            utility[seed][method] = {'f1':f1,'no_update_f1_original':change['original']['baseline_f1'],'no_update_f1_retained':change['retained']['baseline_f1'],'updated_f1_retained':change['retained']['f1']}
    assert set(selections) == {104246,104247,104248} and all(len(v)==1 for v in selections.values())
    numerical = []
    for seed in [104246,104247,104248]:
        for method in ['GIF','IDEA']:
            entries = groups[(seed,method)]
            assert sorted(e['candidate_config']['parameters']['iteration'] for e in entries) == [100,200,400]
            row = evaluate_candidate(entries, methods[method], method, frozen['methods'][method]['frozen_candidate'])
            row.update(seed=seed,method=method)
            numerical.append(row)
            utility[seed][method]['f1_minus_retrain'] = utility[seed][method]['f1']-utility[seed]['retrain_f1']
    return {'experiment':f'EXP-{number}','dataset':dataset,'hidden_channels':64,'job_id':job,'run_id':run['run_id'],'execution_sha':run['commit'],'config_path':run['config_path'],'run_sha256':verified[run_relative],'verified_artifacts':115,'cells':21,'criteria':LIMITS,'numerical_gate':'passed' if all(r['status']=='stable' for r in numerical) else 'failed','numerical_results':numerical,'utility':dict(utility),'method_cache_counts':{k:dict(v) for k,v in cache_counts.items()},'scope':'Three registered Random requests at 10% train-mask deletion; same H64 checkpoint, fixed parameters; T100 production and T200/400 consistency diagnostics.','limitations':['F1 differences are descriptive paired utility comparisons, not prediction/parameter retrain-gap metrics.','Does not establish stability for other selectors, budgets, training seeds or widths.','No final user scientific acceptance is inferred.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('number', choices=['067', '068'])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    number = args.number
    report = analyze(number)
    output = args.output or ROOT/f'self/research/experiments/drafts/EXP-{number}-validate-analysis-20260924.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'numerical_results'},ensure_ascii=False))
