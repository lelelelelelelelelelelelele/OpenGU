"""IDEA real CPU integration and supervision-boundary regression."""
import copy
import functools

import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml, identities
from experiments.modular_config import unlearning, gu_defaults


def test_real_idea_selection_output_cache_and_parameters(tables, monkeypatch):
    root, _, gu = tables
    gu.update(method='IDEA', parameters={'iteration': 2, 'scale': 1000, 'damp': 0.1,
                                       'gaussian_mean': 0.0, 'gaussian_std': 0.001})
    write_yaml(root / 'idea.yaml', gu)
    write_yaml(root / 'utility.yaml', {'kind': 'evaluation', 'schema_version': 1, 'case': 'post_method_metrics'})
    from unlearning.unlearning_methods.IDEA.idea import idea
    original = idea.approxi
    observed = []
    @functools.wraps(original)
    def capture(self, gradients):
        observed.append((dict(self.args), self.deleted_nodes.tolist(), self.influence_nodes.tolist(),
                         self.data.edge_index_unlearn.clone()))
        return original(self, gradients)
    monkeypatch.setattr(idea, 'approxi', capture)
    opts = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['idea.yaml'], evaluation_refs=['utility.yaml'])
    first = run(tables, 'idea_cold', **opts)
    second = run(tables, 'idea_warm', **opts)
    assert not first['unlearning'][0]['hit'] and second['unlearning'][0]['hit']
    assert identities(first) == identities(second)
    assert len(observed) == 1
    args, selected, influenced, edges = observed[0]
    assert selected == [1]
    assert all(node < 10 and node not in selected for node in influenced)
    assert not torch.isin(edges, torch.tensor(selected)).any()
    for key, value in gu['parameters'].items():
        assert args[key] == value
    assert args['num_epochs'] == 3 and args['random_seed'] == 42
    gu['parameters']['scale'] = 2000
    write_yaml(root / 'idea.yaml', gu)
    changed = run(tables, 'idea_changed', **opts)
    assert not changed['unlearning'][0]['hit']
    assert changed['unlearning'][0]['recipe_hash'] != first['unlearning'][0]['recipe_hash']
    assert len(observed) == 2


def test_idea_nontraining_labels_do_not_affect_update(tables):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance
    from experiments.modular_model import runtime_defaults, create_model
    from experiments.modular_idea import idea_node
    from attack.cache_identity import seeded_execution
    root, _, gu = tables
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    data.num_classes = 2
    data.train_indices = data.train_mask.nonzero().flatten().numpy()
    args = runtime_defaults()
    args.update(gu_defaults('IDEA'))
    args.update(base_model='GCN', downstream_task='node', unlearn_task='node',
                unlearning_methods='IDEA', num_runs=1, num_unlearned_nodes=1,
                dataset_name='cpu_fixture', iteration=2, scale=100.0, damp=0.1)
    model = create_model({'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 4},
                         'cpu_fixture', data, 'cpu')
    changed = data.clone()
    changed.y[~data.train_mask] = 1 - changed.y[~data.train_mask]
    with seeded_execution(42):
        first, _ = idea_node(copy.deepcopy(args), copy.deepcopy(model), data, [8], root)
    with seeded_execution(42):
        second, _ = idea_node(copy.deepcopy(args), copy.deepcopy(model), changed, [8], root)
    for name, value in first.state_dict().items():
        assert torch.equal(value, second.state_dict()[name]), name
    assert any(not torch.equal(value, model.state_dict()[name]) for name, value in first.state_dict().items())


@pytest.mark.parametrize('parameters', [{'iteration': 0}, {'iteration': 1.5}, {'scale': float('nan')},
    {'scale': 0}, {'damp': 1}, {'gaussian_std': -1}, {'gaussian_mean': float('inf')}])
def test_invalid_idea_parameters(parameters):
    with pytest.raises(ValueError):
        unlearning({'kind': 'unlearning', 'schema_version': 1, 'method': 'IDEA', 'parameters': parameters})
