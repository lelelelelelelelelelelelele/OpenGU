"""Whole checkpoint-backed matrices preserve the original independent cells."""
import copy
import functools
import importlib
import json
from collections import Counter
from pathlib import Path

import pytest
import torch
import yaml

from test_modular_consumers import tables, run, write_yaml
from test_modular_checkpoint_pt import external
from experiments.modular_config import load_experiment, experiment_batches, unlearning_entries
from experiments.modular_artifacts import planned_cells
from experiments.modular_progress import progress_steps

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [73001, 73003, 73007, 73009, 73013, 73019, 73021, 73027, 73033, 73039]


@pytest.mark.parametrize('number,filename,count,variants', [
    ('088', 'gu_full.yaml', 60, 1), ('089', 'megu_full.yaml', 120, 2)])
def test_registered_full_matrix_matches_original_bound_inputs(number, filename, count, variants):
    config = load_experiment(ROOT / 'experiments/configs' / ('exp' + number) / filename)
    rows = [entry for batch in experiment_batches(config) for entry in unlearning_entries(batch)]
    assert len(rows) == len(planned_cells(config)) == count
    assert len([s for s in progress_steps(config) if s['position']['stage'] == 'unlearning']) == count
    assert Counter(gu['training']['seed'] for gu, _, _, _ in rows) == {s: variants * 6 for s in SEEDS}
    for gu, gu_ref, selector, selector_ref in rows:
        seed = gu['training']['seed']
        assert '/seed{}/'.format(seed) in gu_ref
        if 'training' in selector:
            assert selector['training']['seed'] == seed
            assert '/seed{}/'.format(seed) in selector_ref
        assert Path(gu['checkpoint']).as_posix().endswith('/reference_assets/reference/final.pt')
        assert gu['training']['epochs'] is None
    # Compare with each old per-seed Cartesian table, not merely its row count.
    expected = []
    for seed in SEEDS:
        part = copy.deepcopy(config)
        part['matrix'] = 'cartesian_product'
        for kind in ('selector', 'unlearning'):
            indices = [i for i, value in enumerate(config[kind + 's'])
                       if 'training' not in value or value['training']['seed'] == seed]
            part[kind + 's'] = [config[kind + 's'][i] for i in indices]
            part[kind + '_refs'] = [config[kind + '_refs'][i] for i in indices]
            part['configuration_sources'][kind + 's'] = [config['configuration_sources'][kind + 's'][i] for i in indices]
            if kind == 'unlearning' and 'unlearnings_by_dataset' in part:
                part['unlearnings_by_dataset'] = [[items[i] for i in indices] for items in config['unlearnings_by_dataset']]
                part['configuration_sources']['unlearnings_by_dataset'] = [
                    [items[i] for i in indices] for items in config['configuration_sources']['unlearnings_by_dataset']]
        expected.extend(entry for batch in experiment_batches(part) for entry in unlearning_entries(batch))
    encode = lambda entries: Counter(json.dumps(entry, sort_keys=True) for entry in entries)
    assert encode(rows) == encode(expected)


def checkpoint_tables(tables, method):
    root = tables[0]
    _, base, _, weights = external(tables)
    selectors, methods = [], []
    for seed in (17, 23):
        checkpoint = 'input{}.pt'.format(seed)
        state = copy.deepcopy(weights)
        state[next(iter(state))].add_(seed / 100)
        torch.save(state, root / checkpoint)
        selector = yaml.safe_load((root / 'r_point.yaml').read_text(encoding='utf-8'))
        selector.update(checkpoint=checkpoint, training={'seed': seed},
                        budget={'mode': 'ratio', 'value': .1},
                        parameters={'lissa': {'iterations': 2, 'scale': 25., 'damp': .01}})
        ref = 'selector{}.yaml'.format(seed)
        write_yaml(root / ref, selector)
        selectors.append(ref)
        for variant in (1, 2):
            item = copy.deepcopy(base)
            item.update(method=method, checkpoint=checkpoint, training={'seed': seed})
            item['parameters'] = ({'iteration': variant, 'scale': 1000, 'damp': .1} if method == 'GIF'
                                  else {'unlearning_epochs': 2, 'unlearn_lr': .01 * variant})
            ref = 'gu{}v{}.yaml'.format(seed, variant)
            write_yaml(root / ref, item)
            methods.append(ref)
    write_yaml(root / 'random.yaml', dict(kind='selector', schema_version=1, method='random',
        candidate={'pool': 'train_mask'}, budget={'mode': 'ratio', 'value': .1}))
    return dict(stage='unlearning', selector_refs=selectors + ['random.yaml'], unlearning_refs=methods,
                budget_ratios=[.1, .2], random_selector_seeds=[44])


@pytest.mark.parametrize('method', ['GIF', 'MEGU'])
@pytest.mark.parametrize('first_layout', ['split', 'merged'])
def test_real_cpu_checkpoint_cache_is_shared_by_split_and_full_matrices(tables, monkeypatch, record_property,
                                                                       method, first_layout):
    root = tables[0]
    options = checkpoint_tables(tables, method)
    # Retrain imports this function by value. Load its real implementation
    # before installing the scoped guard against initial-model training.
    importlib.import_module('unlearning.unlearning_methods.Retrain.retrain')
    def forbidden(*args, **kwargs):
        pytest.fail('bound checkpoints must never train initial models')
    monkeypatch.setattr('experiments.modular_model.train_supervised', forbidden)
    import experiments.modular_run as runner
    prepare = runner.prepare_model
    prepared = []
    @functools.wraps(prepare)
    def observe(instance, **kwargs):
        prepared.append((instance['kind'], instance['training']['seed']))
        return prepare(instance, **kwargs)
    monkeypatch.setattr(runner, 'prepare_model', observe)

    def split(prefix):
        results = []
        for i, seed in enumerate((17, 23)):
            results.append(run(tables, prefix + str(seed), **{**options,
                'selector_refs': [options['selector_refs'][i], 'random.yaml'],
                'unlearning_refs': options['unlearning_refs'][i*2:i*2+2]}))
        return results

    def merged(prefix):
        return [run(tables, prefix, matrix='paired_inputs', **options)]

    first = (split if first_layout == 'split' else merged)('cold')
    before = len(prepared)
    second = (merged if first_layout == 'split' else split)('warm')
    last = merged('full_warm')
    outputs = lambda runs: Counter(row['recipe_hash'] for result in runs for row in result['unlearning'])
    selections = lambda runs: Counter((row['selector_ref'], row['requested_k'],
        row['selection']['artifact']['artifact_id']) for result in runs for row in result['selectors'])
    assert sum(len(r['unlearning']) for r in first) == 16
    assert outputs(first) == outputs(second) == outputs(last)
    assert selections(first) == selections(second) == selections(last)
    assert all(not row['hit'] for r in first for row in r['unlearning'])
    assert all(row['hit'] and not row['producer_called'] for r in second + last for row in r['unlearning'])
    assert all(row['selection']['cache']['hit'] for r in second + last for row in r['selectors'])
    assert all(kind == 'selector' for kind, _ in prepared[before:])
    assert not (root / 'checkpoints').exists()
    record_property('paired_cache_proof', json.dumps(dict(method=method, first_layout=first_layout,
        cells=16, warm_hits=32, initial_training_calls=0, warm_gu_prepare_calls=0)))


@pytest.mark.parametrize('defect', ['missing_selector', 'missing_gu', 'override', 'wrong_stage'])
def test_unpaired_or_overridden_inputs_rejected_before_execution(tables, defect):
    root = tables[0]
    options = checkpoint_tables(tables, 'GIF')
    if defect == 'missing_selector':
        options['selector_refs'].pop(1)
    elif defect == 'missing_gu':
        options['unlearning_refs'] = options['unlearning_refs'][:2]
    elif defect == 'override':
        options['seeds'] = [17, 23]
    else:
        options.update(stage='selector', unlearning_refs=[])
    with pytest.raises(ValueError, match='paired_inputs|checkpoint'):
        run(tables, 'invalid', matrix='paired_inputs', **options)
    assert not (root / 'results').exists()
