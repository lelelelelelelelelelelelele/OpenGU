"""Merged Random and IM axes must preserve independent selections and Results."""
from tests.test_modular_consumers import tables, run, write_yaml
from experiments.modular_artifacts import read_run
from utils.target_checkpoint import sha256_file


def test_mixed_axes_real_cold_warm_and_result(tables):
    root, base, gu = tables
    common = {'kind': 'selector', 'schema_version': 1,
              'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2}}
    write_yaml(root / 'random.yaml', {**common, 'method': 'random'})
    write_yaml(root / 'rr.yaml', {**common, 'method': 'im_rr_greedy',
                                'parameters': {'rr_count': 32}})
    write_yaml(root / 'degree.yaml', {**common, 'method': 'degree'})
    write_yaml(root / 'retrain.yaml', {**gu, 'method': 'Retrain', 'parameters': {}})
    args = dict(stage='unlearning', selector_refs=['degree.yaml', 'random.yaml', 'rr.yaml'],
                unlearning_refs=['retrain.yaml'], evaluation_refs=['utility.yaml'],
                seeds=[42, 212], random_selector_seeds=[104245, 11, 22],
                im_selector_seeds=[11, 22], return_scores=False)
    cold = run(tables, 'mixed_cold', **args)
    assert len(cold['unlearning']) == 12  # (Degree + 3 Random + 2 RR) x 2 training
    assert len({s['selection']['artifact']['artifact_id'] for s in cold['selectors']}) == 6
    assert sum(s['selection']['cache']['producer_called'] for s in cold['selectors']) == 6
    warm = run(tables, 'mixed_warm', **args)
    assert all(s['selection']['cache']['hit'] for s in warm['selectors'])
    assert all(r['hit'] and not r['producer_called'] for r in warm['unlearning'])
    path = root / 'results/runs/mixed_warm/mixed_warm/run.json'
    result, docs = read_run(path, sha256_file(path))
    assert len(result['cells']) == len(docs) == 12
    for cell in result['cells']:
        c = cell['conditions']
        assert ('random_selector_seed' in c) == (c['selector'] == 'random')
        assert ('im_selector_seed' in c) == (c['selector'] == 'im_rr_greedy')
