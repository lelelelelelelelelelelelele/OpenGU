"""Independent IM seeds through the real ordinary-table and Result consumers."""
import hashlib
import json
from pathlib import Path

import pytest

from tests.test_modular_consumers import tables, run, write_yaml
from experiments.modular_config import load_experiment
from experiments.modular_artifacts import planned_cells, read_run
from experiments.modular_run import execute


def setup_im(tables):
    root, base, gu = tables
    write_yaml(root / 'im.yaml', {'kind': 'selector', 'schema_version': 1, 'method': 'im',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2},
        'parameters': {'mc_rounds': 3, 'parallel_mc': False, 'im_selector_seed': 17}})
    write_yaml(root / 'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {}})
    return dict(stage='unlearning', selector_refs=['im.yaml'], unlearning_refs=['retrain.yaml'],
                evaluation_refs=['utility.yaml'], seeds=[42, 212, 2024], im_selector_seeds=[11, 22, 33])


def test_nine_effects_three_selections_and_warm_return(tables, monkeypatch):
    changes = setup_im(tables)
    from attack.attack_strategies.im_strategy import IMStrategy
    original = IMStrategy.compute_im_celf
    calls = []
    def counted(self, edges, n, k, candidates):
        calls.append((self.random_seed, k))
        return original(self, edges, n, k, candidates)
    monkeypatch.setattr(IMStrategy, 'compute_im_celf', counted)
    cold = run(tables, 'im_cold', **changes)
    assert sorted(calls) == [(11, 2), (22, 2), (33, 2)]
    assert len(cold['unlearning']) == 9
    ids = {s['selection']['artifact']['artifact_id'] for s in cold['selectors']}
    assert len(ids) == 3
    assert sum(s['selection']['cache']['producer_called'] for s in cold['selectors']) == 3
    assert all(s['score']['hit'] is None for s in cold['selectors'])
    calls.clear()
    warm = run(tables, 'im_warm', **changes)
    assert not calls
    assert all(s['selection']['cache']['hit'] for s in warm['selectors'])
    root = tables[0]
    for name in ('im_cold', 'im_warm'):
        path = root / 'results/runs' / name / name / 'run.json'
        manifest, documents = read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
        assert len(manifest['cells']) == 9
        for cell, doc in zip(manifest['cells'], documents):
            sel = doc['selection.json']
            assert sel['training_seed'] == cell['conditions']['seed']
            assert sel['im_selector_seed'] == cell['conditions']['im_selector_seed']
            assert sel['selector_seed_source'] == 'experiment:im_selector_seeds'
            assert len(sel['selected_nodes']) == 2
            assert cell['cache']['score'] == 'not_applicable'
            assert 'scores.npz' not in cell['files']
    # New GU seed must still reuse the same exact selections.
    run(tables, 'im_new_training_seed', **{**changes, 'seeds': [99]})
    assert not calls
    # K is part of IM identity, never a prefix view of another budget.
    import yaml
    instance = yaml.safe_load((root / 'im.yaml').read_text())
    instance['budget']['value'] = 1
    write_yaml(root / 'im.yaml', instance)
    smaller = run(tables, 'im_k1', **{**changes, 'seeds': [99]})
    assert sorted(calls) == [(11, 1), (22, 1), (33, 1)]
    assert ids.isdisjoint(s['selection']['artifact']['artifact_id'] for s in smaller['selectors'])


def test_axis_only_expands_im_and_dry_run_never_calls_producer(tables, monkeypatch):
    changes = setup_im(tables)
    changes['selector_refs'] += ['degree.yaml', 'r_point.yaml']
    root, base, _ = tables
    random = {'kind': 'selector', 'schema_version': 1, 'method': 'random',
              'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2}}
    write_yaml(root / 'random.yaml', random)
    changes['selector_refs'].append('random.yaml')
    path = root / 'matrix.yaml'
    write_yaml(path, {**base, **changes})
    import experiments.modular_im as im
    monkeypatch.setattr(im, 'load_im_strategy', lambda: pytest.fail('dry-run loaded algorithm'))
    monkeypatch.setattr(Path, 'mkdir', lambda *a, **k: pytest.fail('dry-run wrote directories'))
    config = load_experiment(path)
    cells = planned_cells(config)
    assert execute(path, dry_run=True)['logical_cells'] == 18
    assert sum(c['conditions']['selector'] == 'im' for c in cells) == 9
    for name in ('degree', 'random', 'r_point'):
        subset = [c for c in cells if c['conditions']['selector'] == name]
        assert len(subset) == 3
        assert all('im_selector_seed' not in c['conditions'] for c in subset)
    assert len({c['conditions']['dataset_fingerprint'] for c in cells}) == 1


@pytest.mark.parametrize('values', [[], [True], [-1], [1.5], ['1'], [1, 1], '1'])
def test_invalid_axis_rejected(tables, values):
    changes = setup_im(tables)
    root, base, _ = tables
    path = root / 'invalid.yaml'
    write_yaml(path, {**base, **changes, 'im_selector_seeds': values})
    with pytest.raises(ValueError):
        load_experiment(path)


def test_seed_priority_and_no_unrecorded_scores(tables):
    changes = setup_im(tables)
    changes.pop('im_selector_seeds')
    root, base, _ = tables
    path = root / 'instance_seed.yaml'
    write_yaml(path, {**base, **changes})
    assert {c['conditions']['im_selector_seed'] for c in planned_cells(load_experiment(path))} == {17}
    write_yaml(root / 'im.yaml', {'kind': 'selector', 'schema_version': 1, 'method': 'im',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2}})
    assert {c['conditions']['im_selector_seed'] for c in planned_cells(load_experiment(path))} == {2024}
    write_yaml(path, {**base, **changes, 'return_scores': True})
    with pytest.raises(ValueError, match='return_scores'):
        load_experiment(path)


def test_wrong_im_seed_reference_rejected(tables):
    changes = setup_im(tables)
    result = run(tables, 'identity', **{**changes, 'seeds': [42], 'im_selector_seeds': [11]})
    from experiments.modular_run import verified_selection
    from experiments.dataset_inputs import read_dataset
    root = tables[0]
    config = load_experiment(root / 'identity.yaml')
    data, inputs = read_dataset(config['datasets'][0], str(root))
    from cache_v2.errors import CacheResolutionError
    with pytest.raises(CacheResolutionError, match='im_selector_seed'):
        verified_selection(result['selectors'][0]['selection']['artifact'],
            store_root=root / 'results/cache_v2', data=data, inputs=inputs,
            expected_selector='im', expected_k=2, expected_parameters={'im_selector_seed': 22})


def test_returned_seed_conflict_rejected_even_with_updated_file_hash(tables):
    changes = setup_im(tables)
    run(tables, 'tamper', **{**changes, 'seeds': [42], 'im_selector_seeds': [11]})
    path = tables[0] / 'results/runs/tamper/tamper/run.json'
    manifest = json.loads(path.read_text())
    cell = manifest['cells'][0]
    selection_path = path.parent / cell['path'] / 'selection.json'
    selected = json.loads(selection_path.read_text())
    selected['im_selector_seed'] = 22
    selection_path.write_text(json.dumps(selected))
    cell['files']['selection.json']['sha256'] = hashlib.sha256(selection_path.read_bytes()).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='IM seed'):
        read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
