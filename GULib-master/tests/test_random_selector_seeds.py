"""Random repetition axis, real consumers and complete expanded Results."""
import pytest
import yaml

from experiments.modular_config import ROOT, load_experiment, experiment_batches
from experiments.modular_artifacts import planned_cells, read_run
from experiments.modular_run import execute
from test_modular_consumers import tables, write_yaml, run
from utils.target_checkpoint import sha256_file


def table(tmp_path, **overrides):
    value = yaml.safe_load((ROOT / 'experiments/configs/aagu011/table01.yaml').read_text())
    value.update(dataset_refs=['cora.yaml'], **overrides)
    path = tmp_path / 'table.yaml'
    path.write_text(yaml.safe_dump(value), encoding='utf-8')
    return path


def test_axis_counts_and_ordinary_isolation(tmp_path):
    path = table(tmp_path, random_selector_seeds=[104245, 11, 22])
    config = load_experiment(path)
    cells = planned_cells(config)
    assert len(cells) == 126  # (4 ordinary + 3 Random) x 3 training x 6 GU
    random = [c['conditions'] for c in cells if c['conditions']['selector'] == 'random']
    assert len(random) == 54
    assert {(c['random_selector_seed'], c['training_seed']) for c in random} == {
        (s, t) for s in [104245, 11, 22] for t in [42, 212, 2024]}
    assert all('random_selector_seed' not in c['conditions'] for c in cells if c['conditions']['selector'] != 'random')
    assert execute(path, dry_run=True)['logical_cells'] == len(cells)


@pytest.mark.parametrize('values', [[], [-1], [True], [1.2], ['11'], [11, 11], '11', None])
def test_invalid_axis_rejected(tmp_path, values):
    with pytest.raises(ValueError, match='random_selector_seeds'):
        load_experiment(table(tmp_path, random_selector_seeds=values))


def test_axis_without_random_rejected(tmp_path):
    with pytest.raises(ValueError, match='requires a Random selector'):
        load_experiment(table(tmp_path, random_selector_seeds=[11], selector_refs=['degree.yaml']))


def test_axis_in_metrics_rejected(tmp_path):
    with pytest.raises(ValueError, match='cannot declare repeat axes'):
        load_experiment(table(tmp_path, stage='metrics', selector_refs=[], unlearning_refs=[],
            output_inputs=[{'run': 'old/run.json', 'sha256': 'digest'}], random_selector_seeds=[11]))


def test_precedence_and_omission(tmp_path):
    selector = yaml.safe_load((ROOT / 'experiments/configs/selectors/random.yaml').read_text())
    selector['parameters'] = {'seed': 91}
    small = tmp_path / 'custom.yaml'
    small.write_text(yaml.safe_dump(selector), encoding='utf-8')
    config = load_experiment(table(tmp_path, selector_refs=[str(small)]))
    assert {b['selectors'][0]['parameters']['seed'] for b in experiment_batches(config)} == {91}
    assert all('random_selector_seed' not in b['matrix_values'] for b in experiment_batches(config))
    config = load_experiment(table(tmp_path, selector_refs=[str(small)], random_selector_seeds=[0, 11]))
    batches = list(experiment_batches(config))
    assert {b['selectors'][0]['parameters']['seed'] for b in batches} == {0, 11}
    assert all(b['configuration_sources']['selectors'][0]['parameters.seed'] == 'experiment:random_selector_seeds' for b in batches)
    assert yaml.safe_load(small.read_text())['parameters']['seed'] == 91


def test_real_expansion_preserves_old_outputs(tables):
    root, base, gu = tables
    write_yaml(root / 'random.yaml', {'kind': 'selector', 'schema_version': 1, 'method': 'random',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2}})
    write_yaml(root / 'retrain.yaml', {k: v for k, v in {**gu, 'method': 'Retrain'}.items() if k != 'parameters'})
    args = dict(stage='unlearning', selector_refs=['random.yaml'], unlearning_refs=['gu.yaml', 'retrain.yaml'],
                seeds=[42, 212, 2024], return_scores=True)
    old = run(tables, 'old', **args)
    old_path = root / 'results/runs/old/old/run.json'
    digest = sha256_file(old_path)
    single = run(tables, 'single', random_selector_seeds=[104245], **args)
    expanded = run(tables, 'expanded', random_selector_seeds=[104245, 11, 22], **args)
    assert all(r['hit'] and not r['producer_called'] for r in single['unlearning'])
    assert [r['output'] for r in single['unlearning']] == [r['output'] for r in old['unlearning']]
    assert len(expanded['selectors']) == 9 and len(expanded['unlearning']) == 18
    assert len({r['selection']['artifact']['artifact_id'] for r in expanded['selectors']}) == 3
    assert sum(r['score']['producer_called'] for r in expanded['selectors']) == 2
    assert sum(r['selection']['cache']['producer_called'] for r in expanded['selectors']) == 2
    for row in expanded['unlearning']:
        assert row['hit'] == (row['matrix_values']['random_selector_seed'] == 104245)
        assert row['producer_called'] != row['hit']
    assert sha256_file(old_path) == digest
    path = root / 'results/runs/expanded/expanded/run.json'
    result, documents = read_run(path, sha256_file(path))
    assert len(result['cells']) == len(documents) == 18
    assert all(len(d['selection.json']['selected_nodes']) == 2 for d in documents)
