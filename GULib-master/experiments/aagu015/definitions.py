"""Inspect the registered ordinary AAGU-015 tables without writing leaf YAML."""
from pathlib import Path
import argparse
import json
from experiments.modular_config import load_experiment, experiment_batches, resolve_budget
from experiments.modular_run import execute
from experiments.target_direct_v1.methods import SCORE_NAMES, selected_checkpoint_indices, uses_model

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'experiments/configs/aagu015'
SELECTORS = SCORE_NAMES


def dry_run(directory=CONFIG):
    directory = Path(directory)
    rows, stages, models, scores, selections = [], {}, set(), set(), set()
    for dataset, count in [('cora',2708),('citeseer',3327),('pubmed',19717)]:
        for stage in ('s','u','retrain'):
            path = directory / ('stage_' + stage + '_' + dataset + '.yaml')
            plan = execute(path, dry_run=True)
            stages[stage] = stages.get(stage,0) + plan['logical_cells']
            if stage != 's':
                continue
            config = load_experiment(path)
            if config['seeds'] != [42,212,2024] or config['budget_ratios'] != [.01,.05]:
                raise ValueError('AAGU-015 scientific axes changed')
            for batch in experiment_batches(config):
                if sorted(s['method'] for s in batch['selectors']) != sorted(SELECTORS):
                    raise ValueError('AAGU-015 requires all 17 registered selectors')
                for selector in batch['selectors']:
                    budget = resolve_budget(selector['budget'], int(count * .7))
                    name = selector['method']; seed = selector.get('training',{}).get('seed')
                    key = (dataset,name,seed)
                    scores.add(key);selections.add(key+(budget['k'],))
                    if uses_model(name): models.add((dataset,seed))
                    steps = None
                    if name.startswith('tracin_cp_'):
                        trajectory = [{'global_step':i} for i in range(1,selector['training']['epochs']+1)]
                        steps = [trajectory[i]['global_step'] for i in selected_checkpoint_indices(trajectory,selector['parameters'])]
                        if len(steps) != int(name[-1]):raise ValueError('TracIn checkpoint count drift')
                    rows.append({'dataset':config['dataset']['dataset']['name'],'selector':name,
                        'training_seed':seed,'matrix_values':batch['matrix_values'],
                        'planned_k':budget['k'],'checkpoint_steps':steps})
    if stages != {'s':306,'u':612,'retrain':306}:
        raise ValueError('AAGU-015 stage cardinality drift')
    return {'evidence_level':'configuration_only','execution_ready':False,'producer_called':False,
        'generated_result_artifacts':[], 'maintained_yaml':len(list(directory.glob('*.yaml'))),
        'generated_yaml':0,'counts':{'stage_s':stages['s'],'stage_u':stages['u'],
            'independent_retrain':stages['retrain'],'conditional_preparation_groups':len(models),
            'conditional_score_groups':len(scores),'conditional_selection_groups':len(selections)},
        'stage_s':rows,'boundary':'Real Dataset/Output bindings and approved formal execution remain required.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('check','dry-run'))
    args=parser.parse_args()
    result=dry_run()
    print(json.dumps(result if args.action=='dry-run' else result['counts'],indent=2))


if __name__=='__main__':main()
