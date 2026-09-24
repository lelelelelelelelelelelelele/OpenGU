"""Ordinary Unlearning runs: cold execution, cache-only backfill and export."""
import functools
import hashlib
import json
from pathlib import Path

import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from experiments.modular_artifacts import read_run
from experiments.modular_config import load_experiment, experiment_batches, unlearning_entries
from experiments.modular_run import execute


def paired_tables(tables):
    root, _, gu = tables
    write_yaml(root / 'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {}})
    for name, case in [('gap', 'post_unlearning_utility_and_retrain_gap'),
                       ('flip', 'post_unlearning_flip_hop')]:
        write_yaml(root / (name + '.yaml'), dict(kind='evaluation', schema_version=1, case=case))
    return root


def read_result(root, name):
    path = root / 'results/runs' / name / name / 'run.json'
    return read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())


@pytest.mark.parametrize('refs', [['gu.yaml', 'retrain.yaml'], ['retrain.yaml', 'gu.yaml']])
def test_cold_paired_evaluations_and_cache_only_backfill(tables, monkeypatch, refs, record_property):
    import experiments.modular_model as model
    import experiments.modular_gu as gu
    from experiments.target_direct_v1 import methods
    root = paired_tables(tables)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=refs)
    cold = run(tables, 'cold-paired', evaluation_refs=['gap.yaml', 'flip.yaml'], **options)
    assert all(row['producer_called'] and not row['hit'] for row in cold['unlearning'])
    original_run, original_documents = read_result(root, 'cold-paired')
    hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (root / 'results/cache_v2').rglob('*') if p.is_file()}

    def forbid(*args, **kwargs):
        raise AssertionError('cache-only run invoked training, producer or forward')
    # __wrapped__ preserves the production identity while forbidding execution.
    for name in ('train_supervised',):
        original = getattr(model, name)
        monkeypatch.setattr(model, name, functools.wraps(original)(lambda *a, **k: forbid()))
    for key, original in list(gu.GU_METHODS.items()):
        monkeypatch.setitem(gu.GU_METHODS, key, functools.wraps(original)(lambda *a, **k: forbid()))
    monkeypatch.setitem(methods.METHODS, 'degree', functools.wraps(methods.METHODS['degree'])(lambda *a, **k: forbid()))
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbid)
    try:
        baseline = run(tables, 'warm-baseline', evaluation_refs=[], **options)
        warm = run(tables, 'warm-paired', evaluation_refs=['gap.yaml', 'flip.yaml'], **options)
    finally:
        hook.remove()
    assert all(row['hit'] and not row['producer_called'] for row in warm['unlearning'])
    assert not warm['selector_producer_called']
    assert warm['evaluations'] == cold['evaluations']
    assert [row['output'] for row in warm['unlearning']] == [row['output'] for row in baseline['unlearning']]
    assert hashes == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in hashes}
    exported, docs = read_result(root, 'warm-paired')
    assert len(exported['cells']) == 2
    for cell, document, original in zip(exported['cells'], docs, original_documents):
        measured = document['metrics.json']['rows']
        assert measured == original['metrics.json']['rows']
        assert {'method', 'utility'} <= {row['stage'] for row in measured}
        assert cell['cache']['method'] == 'hit'
        paired = [row for row in measured if row['stage'].startswith('post_unlearning_')]
        if cell['conditions']['method'] == 'Retrain':
            assert not paired
        else:
            assert len(paired) == 2
            flip = next(row for row in paired if row['stage'] == 'post_unlearning_flip_hop')
            values = flip['values']
            assert sum(values[h + '_hop_count'] for h in ('1', '2', '3', 'gt3')) == values['node_count']
            assert sum(values[h + '_hop_flipped_count'] for h in ('1', '2', '3', 'gt3')) == values['flipped_count']
            assert flip['baseline_output']
    record_property('ordinary_paired_result', json.dumps({'method_order': refs, 'cold_cells': 2,
        'warm_method_hits': 2, 'warm_producers_and_forward_forbidden': True,
        'same_evaluation_receipts': True, 'cache_bytes_unchanged': True}))


def test_unlearning_pairing_still_rejects_wrong_training(tables):
    root = paired_tables(tables)
    gu = tables[2]
    write_yaml(root / 'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {},
        'training': {**gu['training'], 'seed': 999}})
    with pytest.raises(ValueError, match='exactly one verified Retrain'):
        run(tables, 'mismatched', stage='unlearning', selector_refs=['degree.yaml'],
            unlearning_refs=['gu.yaml', 'retrain.yaml'], evaluation_refs=['flip.yaml'])


def test_complete_public_table_profiles_and_two_evaluations():
    root = Path(__file__).resolve().parents[1]
    path = root / 'experiments/configs/aagu011/table02_v2.yaml'
    config = load_experiment(path)
    batches = list(experiment_batches(config))
    entries = [(b, gu) for b in batches for gu, _, _, _ in unlearning_entries(b)]
    assert len(entries) == 1449
    assert len([gu for _, gu in entries if gu['method'] != 'Retrain']) == 1242
    assert len(config['evaluations']) == 2
    observed = set()
    for batch, gu in entries:
        if gu['method'] not in ('GIF', 'IDEA'):
            continue
        values = batch['matrix_values']
        assert gu['model']['hidden_channels'] == 64 and gu['model']['layers'] == 2
        assert gu['parameters']['iteration'] == 100
        assert gu['parameters']['scale'] == {'Cora': 9791, 'CiteSeer': 23004, 'PubMed': 173215}[values['dataset_name']]
        observed.add((values['dataset_name'], gu['training']['seed'], gu['method']))
    assert len(observed) == 18
    assert execute(path, dry_run=True)['logical_cells'] == 1449
    for name in ('gif', 'idea'):
        assert (root / f'experiments/configs/unlearning/{name}_h64.yaml').exists()
        assert not (root / f'experiments/configs/aagu077/{name}_h64.yaml').exists()


def test_existing_outputs_plus_new_gif_idea_form_one_complete_result(tables, record_property):
    root = paired_tables(tables)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'])
    old = run(tables, 'existing', unlearning_refs=['gu.yaml', 'retrain.yaml'], **options)
    for method in ('GIF', 'IDEA'):
        write_yaml(root / (method.lower() + '.yaml'), {**tables[2], 'method': method,
            'parameters': {'iteration': 100, 'scale': 100, 'damp': .5}})
    complete = run(tables, 'complete', unlearning_refs=['gif.yaml', 'gu.yaml', 'idea.yaml', 'retrain.yaml'],
        evaluation_refs=['gap.yaml', 'flip.yaml'], **options)
    rows = {row['target']['method']: row for row in complete['unlearning']}
    assert not complete['selector_producer_called']
    for method in ('GNNDelete', 'Retrain'):
        assert rows[method]['hit'] and not rows[method]['producer_called']
    for method in ('GIF', 'IDEA'):
        assert not rows[method]['hit'] and rows[method]['producer_called']
    assert {json.dumps(row['output'], sort_keys=True) for row in old['unlearning']} <= {
        json.dumps(row['output'], sort_keys=True) for row in complete['unlearning']}
    exported, documents = read_result(root, 'complete')
    assert len(exported['cells']) == 4
    assert all(len(evaluation['rows']) == 3 for evaluation in complete['evaluations'])
    for cell, document in zip(exported['cells'], documents):
        cases = {row['stage'] for row in document['metrics.json']['rows']}
        assert {'method', 'utility'} <= cases
        if cell['conditions']['method'] != 'Retrain':
            assert {'post_unlearning_flip_hop', 'post_unlearning_utility_and_retrain_gap'} <= cases
    record_property('mixed_hit_miss', json.dumps({'old_outputs_reused': 2,
        'new_methods': ['GIF', 'IDEA'], 'cells': 4, 'paired_metrics': 3}))
