"""Disposable real MEGU update, prediction and immutable Output checks."""
import copy
import pytest
import torch
from test_modular_consumers import tables, run, write_yaml


def test_megu_real_output_cache_and_parameters(tables, monkeypatch):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance
    from experiments.unlearning_outputs import load_output, restore_model
    from experiments.modular_megu import megu_logits
    from task.MEGUTrainer import MEGUTrainer
    root, _, gu = tables
    gu = copy.deepcopy(gu)
    gu.update(method='MEGU', parameters={'unlearning_epochs': 2, 'kappa': 0.03,
        'alpha1': 0.6, 'alpha2': 0.4, 'GNN_layer': 2})
    gu['training'].update(lr=0.015, weight_decay=0.001)
    write_yaml(root / 'megu.yaml', gu)
    observed = []
    original = MEGUTrainer.megu_unlearning
    def observe(self, nodes, neighbors):
        observed.append((list(nodes), dict(self.args), self.model.config.lr, self.model.config.decay))
        assert not self.data.train_mask[nodes].any()
        assert not torch.isin(self.data.edge_index_unlearn, torch.tensor(nodes)).any()
        return original(self, nodes, neighbors)
    monkeypatch.setattr(MEGUTrainer, 'megu_unlearning', observe)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['megu.yaml'])
    first = run(tables, 'megu_first', **options)
    warm = run(tables, 'megu_warm', **options)
    assert not first['unlearning'][0]['hit'] and warm['unlearning'][0]['hit']
    assert len(observed) == 1
    assert observed[0][1]['kappa'] == 0.03 and observed[0][1]['GNN_layer'] == 2
    assert observed[0][2:] == (0.015, 0.001)
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    payload = load_output(first['unlearning'][0]['output'], root/'results/cache_v2', data=data, dataset_root=root)
    assert payload.arrays['selected_nodes'].tolist() == observed[0][0]
    assert torch.isfinite(torch.tensor(payload.arrays['logits'])).all()
    restored = restore_model(payload)
    with torch.no_grad():
        actual = megu_logits(restored, data, torch.tensor(payload.arrays['retain_mask']), gu['parameters'])
    torch.testing.assert_close(actual, torch.tensor(payload.arrays['logits']))
    gu['parameters']['kappa'] = 0.04
    write_yaml(root / 'megu.yaml', gu)
    changed = run(tables, 'megu_changed', **options)
    assert not changed['unlearning'][0]['hit']
    assert changed['selectors'][0]['selection']['cache']['hit']
    assert changed['unlearning'][0]['recipe_hash'] != first['unlearning'][0]['recipe_hash']


@pytest.mark.parametrize('parameters', [{'kappa': -1.0}, {'alpha1': 1.1}, {'GNN_layer': 0}, {'unlearning_epochs': 0}])
def test_invalid_megu_parameters(parameters):
    from experiments.modular_config import unlearning
    with pytest.raises(ValueError):
        unlearning(dict(kind='unlearning', schema_version=1, method='MEGU', parameters=parameters))


def test_megu_empty_preservation_neighbors_and_retained_evaluation(tables, monkeypatch):
    from experiments.modular_model import runtime_defaults
    runtime_defaults()
    from unlearning.unlearning_methods.MEGU.megu import megu
    monkeypatch.setattr(megu, 'neighbor_select', lambda self, features: torch.zeros(len(features), dtype=torch.bool))
    root, _, gu = tables
    gu = copy.deepcopy(gu)
    gu.update(method='MEGU', parameters={'unlearning_epochs': 2}, deletion={'evaluation_graph': 'retained'})
    write_yaml(root / 'megu.yaml', gu)
    result = run(tables, 'empty_neighbors', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['megu.yaml'])
    assert result['unlearning'][0]['producer_called']
    assert result['unlearning'][0]['evaluation']['metrics']['cross_entropy'] >= 0
