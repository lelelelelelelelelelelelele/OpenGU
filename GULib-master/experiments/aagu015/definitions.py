"""Expand AAGU-015 into existing modular YAML, without an execution shortcut.

`generate` writes configuration only. `check` and `dry-run` never write files,
read datasets, construct a Store, train a model or invoke a selector/GU producer.
All generated experiment files use the already accepted modular schema.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import yaml

from experiments.effective_config import ConfigurationError, fields, read_yaml
from experiments.modular_config import load_experiment, load_instance, resolve_budget
from experiments.modular_run import execute
from experiments.target_direct_v1.methods import selected_checkpoint_indices, uses_model

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'experiments/configs/aagu015'
SELECTORS = (
    'degree', 'random', 'a_grad_norm', 'b_param_hutch', 'r_point', 'gt_simple',
    'gt_full', 'p_point', 'p_simple', 'p_graph', 'tracin_cp_point_3',
    'tracin_cp_point_6', 'tracin_cp_simple_3', 'tracin_cp_simple_6',
    'tracin_cp_graph_3', 'tracin_cp_graph_6', 'legacy',
)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_tables(directory=CONFIG):
    directory = Path(directory)
    stage_s, stage_u = (read_yaml(directory / name) for name in ('stage_s.yaml', 'stage_u.yaml'))
    fields(stage_s, {'schema', 'version', 'datasets', 'selector_refs', 'seeds', 'budget_ratios'},
           {'schema', 'version', 'datasets', 'selector_refs', 'seeds', 'budget_ratios'}, 'AAGU-015 Stage S')
    fields(stage_u, {'schema', 'version', 'selection_source', 'unlearning_refs', 'evaluation_refs'},
           {'schema', 'version', 'selection_source', 'unlearning_refs', 'evaluation_refs'}, 'AAGU-015 Stage U')
    if stage_s['schema'] != 'aagu015.stage_s' or stage_u['schema'] != 'aagu015.stage_u':
        raise ConfigurationError('unknown AAGU-015 matrix schema')
    if type(stage_s['version']) is not int or type(stage_u['version']) is not int or stage_s['version'] != 1 or stage_u['version'] != 1:
        raise ConfigurationError('AAGU-015 requires matrix version 1')
    if stage_u['selection_source'] != 'stage_s.yaml':
        raise ConfigurationError('Stage U must consume this Stage S; no new selector route')
    if stage_s['seeds'] != [42, 212, 2024] or stage_s['budget_ratios'] != [0.01, 0.05]:
        raise ConfigurationError('matrix differs from the registered training seeds/budgets')
    selectors = [load_instance(directory / ref, 'selector') for ref in stage_s['selector_refs']]
    if [item['method'] for item in selectors] != list(SELECTORS):
        raise ConfigurationError('matrix must contain the 17 registered selectors once, in order')
    datasets = []
    for row in stage_s['datasets']:
        fields(row, {'ref', 'expected_num_nodes'}, {'ref', 'expected_num_nodes'}, 'dataset row')
        instance = load_instance(directory / row['ref'], 'dataset_split')
        fields(instance['dataset'], {'name', 'family'}, {'name', 'family'}, 'dataset')
        fields(instance['artifacts'], {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'},
               {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'}, 'artifacts')
        if instance['split'] != {'profile': 'planetoid_70_10_20_seed2024',
                'train_ratio': 0.7, 'val_ratio': 0.1, 'test_ratio': 0.2, 'seed': 2024}:
            raise ConfigurationError('Dataset/Split differs from the registered contract')
        datasets.append(instance)
    if [(d['dataset']['name'], r['expected_num_nodes']) for d, r in zip(datasets, stage_s['datasets'])] != [
            ('Cora', 2708), ('CiteSeer', 3327), ('PubMed', 19717)]:
        raise ConfigurationError('matrix dataset names/count expectations differ from registration')
    gus = [load_instance(directory / ref, 'unlearning') for ref in stage_u['unlearning_refs']]
    if [item['method'] for item in gus] != ['GNNDelete', 'GIF']:
        raise ConfigurationError('Stage U requires independent GNNDelete and GIF instances')
    evaluations = [load_instance(directory / ref, 'evaluation') for ref in stage_u['evaluation_refs']]
    if len(evaluations) != 1 or evaluations[0]['case'] != 'post_unlearning_utility_and_retrain_gap':
        raise ConfigurationError('Stage U cannot downgrade to utility-only evaluation')
    return stage_s, stage_u, datasets, selectors, gus


def generated_documents(directory=CONFIG):
    """Return ordinary YAML documents, relative to generated/, in memory."""
    directory = Path(directory)
    stage_s, stage_u, datasets, selectors, gus = load_tables(directory)
    documents = {}
    for seed in stage_s['seeds']:
        for ratio in stage_s['budget_ratios']:
            for ref, selector in zip(stage_s['selector_refs'], selectors):
                item = read_yaml(directory / ref)
                item['budget']['value'] = ratio
                if uses_model(selector['method']):
                    item.setdefault('training', {})['seed'] = seed
                label = f"{selector['method']}-seed{seed if uses_model(selector['method']) else 'independent'}-r{ratio:.2f}"
                documents['selectors/' + label + '.yaml'] = item
        for ref, gu in zip(stage_u['unlearning_refs'], gus):
            item = read_yaml(directory / ref)
            item.setdefault('training', {})['seed'] = seed
            documents[f"unlearning/{gu['method']}-seed{seed}.yaml"] = item
    for row, dataset in zip(stage_s['datasets'], datasets):
        name = dataset['dataset']['name'].lower()
        for seed in stage_s['seeds']:
            for ratio in stage_s['budget_ratios']:
                cell = f'{name}-seed{seed}-r{ratio:.2f}'
                refs = [f"../selectors/{s['method']}-seed{seed if uses_model(s['method']) else 'independent'}-r{ratio:.2f}.yaml"
                        for s in selectors]
                documents[f'stage_s/{cell}.yaml'] = {
                    'kind': 'experiment', 'schema_version': 1, 'experiment_id': 'aagu015-s-' + cell,
                    'stage': 'selector', 'dataset_ref': '../../' + row['ref'],
                    'selector_refs': refs, 'matrix': 'cartesian_product',
                }
                for selector in selectors:
                    logical_cell = cell + '-' + selector['method']
                    documents[f'stage_u/{logical_cell}.yaml'] = {
                        'kind': 'experiment', 'schema_version': 1,
                        'experiment_id': 'aagu015-u-' + logical_cell,
                        'case_id': 'aagu015-s-' + cell + '/' + selector['method'],
                        'stage': 'unlearning', 'dataset_ref': '../../' + row['ref'],
                        # These are missing inputs, never invented Artifact identities.
                        'selection_input': {'artifact_id': None, 'recipe_hash': None, 'content_hash': None},
                        'unlearning_refs': [f"../unlearning/{g['method']}-seed{seed}.yaml" for g in gus],
                        'evaluation_refs': ['../../' + ref for ref in stage_u['evaluation_refs']],
                        'matrix': 'cartesian_product',
                    }
    return documents


def rendered_documents(directory=CONFIG):
    return {name: '# Generated by experiments.aagu015.definitions; edit source tables, then regenerate.\n'
            + yaml.safe_dump(value, sort_keys=False, allow_unicode=True)
            for name, value in generated_documents(directory).items()}


def check_generated(directory=CONFIG):
    directory = Path(directory)
    expected = rendered_documents(directory)
    actual = {p.relative_to(directory / 'generated').as_posix(): p for p in (directory / 'generated').rglob('*.yaml')}
    if set(actual) != set(expected):
        raise ConfigurationError('generated YAML file set drift')
    for name, content in expected.items():
        if actual[name].read_text(encoding='utf-8') != content:
            raise ConfigurationError('generated YAML content drift: ' + name)
    return len(expected)


def dry_run(directory=CONFIG):
    """Use the accepted parser/consumer dry-run for every emitted plan."""
    directory = Path(directory)
    check_generated(directory)
    stage_s, stage_u, datasets, _, _ = load_tables(directory)
    rows_s, rows_u, sources = [], [], {}
    effective_selectors, effective_gu = {}, {}
    preparation, scores, selections = {}, {}, {}
    expectations = {d['dataset']['name']: row['expected_num_nodes']
                    for d, row in zip(datasets, stage_s['datasets'])}
    for path in sorted((directory / 'generated/stage_s').glob('*.yaml')):
        config = load_experiment(path)
        observed = execute(path, dry_run=True)
        if observed['producer_called'] is not False:
            raise AssertionError('dry-run unexpectedly invoked a producer')
        sources[path.relative_to(directory).as_posix()] = observed['configuration_sources']
        dataset = config['dataset']['dataset']['name']
        dataset_key = digest(config['dataset'])
        expected_count = int(expectations[dataset] * config['dataset']['split']['train_ratio'])
        for selector in observed['effective_selectors']:
            selector = copy.deepcopy(selector)
            budget = resolve_budget(selector['budget'], expected_count)
            selector['budget'] = {k: v for k, v in budget.items() if k != 'k'}
            selector_key = digest(selector)
            effective_selectors[selector_key] = selector
            model_group = None
            if uses_model(selector['method']):
                model_identity = {k: selector[k] for k in ('model', 'training')}
                model_group = digest([dataset_key, model_identity])
                preparation.setdefault(model_group, {'dataset': dataset, **model_identity, 'cells': []})
            score_config = {k: v for k, v in selector.items() if k not in ('budget', 'selection_rule')}
            score_group = digest([dataset_key, score_config])
            selection_group = digest([score_group, selector['budget'], selector['selection_rule']])
            cell = observed['experiment_id'] + '/' + selector['method']
            scores.setdefault(score_group, {'dataset': dataset, 'selector': selector['method'], 'cells': []})['cells'].append(cell)
            selections.setdefault(selection_group, {'score_group': score_group, 'budget': selector['budget'], 'cells': []})['cells'].append(cell)
            if model_group:
                preparation[model_group]['cells'].append(cell)
            checkpoint_steps = None
            if selector['method'].startswith('tracin_cp_'):
                checkpoints = [{'global_step': i} for i in range(1, selector['training']['epochs'] + 1)]
                indices = selected_checkpoint_indices(checkpoints, selector['parameters'])
                checkpoint_steps = [checkpoints[i]['global_step'] for i in indices]
                required_count = int(selector['method'].rsplit('_', 1)[1])
                if len(checkpoint_steps) != required_count:
                    raise ConfigurationError('checkpoint count does not match selector definition')
            rows_s.append({'cell': cell, 'dataset': dataset, 'selector': selector['method'],
                'configuration': path.relative_to(directory).as_posix(), 'effective_selector': selector_key,
                'expected_candidate_count': expected_count, 'planned_k': budget['k'], 'actual_candidate_hash': None,
                'checkpoint_steps': checkpoint_steps, 'preparation_group': model_group,
                'score_group': score_group, 'selection_group': selection_group})
    known = {row['cell'] for row in rows_s}
    for path in sorted((directory / 'generated/stage_u').glob('*.yaml')):
        config = load_experiment(path)
        observed = execute(path, dry_run=True)
        if config['selectors'] or observed['producer_called'] or config['case_id'] not in known:
            raise ConfigurationError('Stage U selection lineage is invalid')
        sources[path.relative_to(directory).as_posix()] = observed['configuration_sources']
        for gu in observed['effective_unlearning']:
            gu_key = digest(gu)
            effective_gu[gu_key] = gu
            rows_u.append({'cell': config['experiment_id'] + '/' + gu['method'],
                'selection_source_cell': config['case_id'], 'method': gu['method'],
                'configuration': path.relative_to(directory).as_posix(), 'effective_gu': gu_key,
                'selection_input': config['selection_input'], 'evaluation': observed['effective_evaluations'],
                'selector_refs': [], 'execution_ready': False})
    if len(rows_s) != 306 or len(rows_u) != 612 or len(known) != 306:
        raise ConfigurationError('expanded matrix does not match 306 S / 612 U')
    yaml_files = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(directory.rglob('*.yaml'))}
    return {'schema': 'aagu015.definition_expansion', 'version': 1,
        'evidence_level': 'configuration_only', 'execution_ready': False,
        'accepted_parser': 'experiments.modular_config.load_experiment',
        'accepted_dry_run': 'experiments.modular_run.execute(dry_run=True)',
        'producer_called': False, 'dataset_read': False, 'generated_result_artifacts': [],
        'counts': {'stage_s': len(rows_s), 'stage_u': len(rows_u),
            'conditional_preparation_groups': len(preparation), 'conditional_score_groups': len(scores),
            'conditional_selection_groups': len(selections)},
        'sharing_caveat': 'Configuration dependency groups only, not Recipe/Artifact hashes or observed HITs. Actual data/candidate/checkpoint/producer identities must agree.',
        'dataset_bindings': {d['dataset']['name']: d['artifacts'] for d in datasets},
        'blocking_inputs': ['three verified Dataset/Split manifests and actual data/split/candidate hashes',
            'checkpoint/trajectory preparation with exact identities under an approved real-input canary',
            'verified Stage S Selection references; Stage U null inputs must be bound from collected receipts',
            'registered AAGU-015 launcher, exact retrain and full evaluation consumer',
            'clean local/origin/SSH main at the same accepted SHA, device setup and GPU preflight',
            'canary and Stage S cost evidence followed by user scheduling decision'],
        'source_yaml_sha256': yaml_files, 'configuration_digest': digest(yaml_files),
        'effective_selectors': effective_selectors, 'effective_gu': effective_gu,
        'configuration_sources': sources, 'preparation_groups': preparation,
        'score_groups': scores, 'selection_groups': selections,
        'stage_s': rows_s, 'stage_u': rows_u}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('generate', 'check', 'dry-run'))
    args = parser.parse_args()
    if args.action == 'generate':
        documents = rendered_documents()
        existing = {p.relative_to(CONFIG / 'generated').as_posix() for p in (CONFIG / 'generated').rglob('*.yaml')}
        if existing - set(documents):
            raise ConfigurationError('obsolete generated paths require explicit scoped review')
        for name, content in documents.items():
            path = CONFIG / 'generated' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                with path.open('w', encoding='utf-8', newline='\n') as handle:
                    handle.write(content)
        print(json.dumps({'configuration_files': len(documents), 'result_artifacts': []}))
    elif args.action == 'check':
        print(json.dumps({'generated_yaml_checked': check_generated()}))
    else:
        print(json.dumps(dry_run(), ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
