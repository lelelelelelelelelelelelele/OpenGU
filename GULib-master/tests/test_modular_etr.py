"""Real ETR execution, exact request/cache identity and edit boundaries."""
import copy

import pytest
import torch
from test_modular_consumers import tables, run, write_yaml


@pytest.mark.parametrize('parameters', [
    {'etr_erase_ratio': 0}, {'etr_erase_ratio': 1.1}, {'etr_erase_ratio': float('nan')},
    {'etr_l': -1}, {'etr_l': float('inf')}, {'etr_l': True}, {'etr_lr': .01},
])
def test_invalid_etr_parameters(parameters):
    from experiments.modular_config import unlearning
    with pytest.raises(ValueError):
        unlearning(dict(kind='unlearning', schema_version=1, method='ETR', parameters=parameters))


@pytest.mark.parametrize('evaluation_graph', ['original', 'retained'])
def test_etr_real_output_and_parameter_identity(tables, monkeypatch, evaluation_graph):
    from experiments import modular_etr
    from experiments.modular_config import load_instance
    from experiments.modular_run import read_dataset
    from experiments.unlearning_outputs import load_output, restore_model
    root, _, gu = tables
    gu = copy.deepcopy(gu)
    gu.update(method='ETR', parameters={'etr_erase_ratio': .1, 'etr_l': .3},
              deletion={'evaluation_graph': evaluation_graph})
    write_yaml(root / 'etr.yaml', gu)
    retrain = {k: v for k, v in gu.items() if k != 'parameters'}
    retrain['method'] = 'Retrain'
    write_yaml(root / 'retrain.yaml', retrain)
    write_yaml(root / 'paired.yaml', dict(kind='evaluation', schema_version=1,
        case='post_unlearning_utility_and_retrain_gap'))
    observed = []
    original = modular_etr.run_etr

    def observe(model, data, nodes, **kwargs):
        before = {k: v.clone() for k, v in model.state_dict().items()}
        stages = {}
        edited, seconds = original(model, data, nodes, trace=lambda stage, m: stages.update(
            {stage: {k: v.clone() for k, v in m.state_dict().items()}}), **kwargs)
        assert all(torch.equal(v, before[k]) for k, v in model.state_dict().items())
        assert set(stages) == {'erase', 'rectify'}
        observed.append((list(nodes), kwargs, stages))
        return edited, seconds

    monkeypatch.setattr(modular_etr, 'run_etr', observe)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['retrain.yaml', 'etr.yaml'], evaluation_refs=['paired.yaml'])
    cold = run(tables, 'etr_cold', **options)
    warm = run(tables, 'etr_warm', **options)
    cold_etr = next(r for r in cold['unlearning'] if r['target']['method'] == 'ETR')
    warm_etr = next(r for r in warm['unlearning'] if r['target']['method'] == 'ETR')
    assert not cold_etr['hit'] and warm_etr['hit'] and len(observed) == 1
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    payload = load_output(cold_etr['output'], root/'results/cache_v2', data=data, dataset_root=root)
    assert payload.arrays['selected_nodes'].tolist() == observed[0][0]
    model = restore_model(payload)
    model.eval()
    if evaluation_graph == 'retained':
        from experiments.node_deletion import retained_graph
        data = retained_graph(data, observed[0][0])
    with torch.no_grad():
        torch.testing.assert_close(model(data.x, data.edge_index), torch.tensor(payload.arrays['logits']))
    gu['parameters']['etr_l'] = .2
    write_yaml(root/'etr.yaml', gu)
    changed = run(tables, 'etr_changed', **options)
    row = next(r for r in changed['unlearning'] if r['target']['method'] == 'ETR')
    assert not row['hit'] and row['recipe_hash'] != cold_etr['recipe_hash']
    assert next(r for r in changed['unlearning'] if r['target']['method'] == 'Retrain')['hit']
    assert changed['selectors'][0]['selection']['cache']['hit']


def test_subgraph_mapping_and_empty_population():
    from torch_geometric.data import Data
    from unlearning.unlearning_methods.ETR.etr import seed_subgraph, training_graph
    data = Data(x=torch.eye(4), y=torch.tensor([0, 1, 0, 1]),
        edge_index=torch.tensor([[0, 2, 1, 2], [2, 0, 2, 1]]),
        train_mask=torch.tensor([True, False, True, True]))
    graph = training_graph(data)
    assert graph.edge_index.tolist() == [[0, 2], [2, 0]]
    subgraph = seed_subgraph([2], graph)
    assert subgraph.mapping.tolist() == [1]
    assert subgraph.global_nodes[subgraph.mapping].tolist() == [2]
    with pytest.raises(ValueError, match='nonempty connected seed'):
        seed_subgraph([3], graph)


def test_zero_quantile_fails_without_nan():
    from unlearning.unlearning_methods.ETR.etr import erase
    model = torch.nn.Linear(2, 2)
    zeros = {n: torch.zeros_like(p) for n, p in model.named_parameters()}
    ones = {n: torch.ones_like(p) for n, p in model.named_parameters()}
    with pytest.raises(ValueError, match='quantile is zero'):
        erase(model, zeros, ones, ones, .01)
    assert all(torch.isfinite(p).all() for p in model.parameters())
