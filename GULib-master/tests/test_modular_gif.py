"""GIF must not use held-out labels to compute a parameter update."""
import copy

import pytest
import torch

from test_modular_consumers import tables


@pytest.mark.parametrize('population', ['val', 'test', 'train'])
def test_gif_update_label_boundary(tables, population):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance, gu_defaults
    from experiments.modular_model import runtime_defaults, create_model
    from experiments.modular_gu import gif_node
    from attack.cache_identity import seeded_execution

    root, _, _ = tables
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    # A real graph neighborhood crosses both validation and test populations.
    data.edge_index = torch.cat([data.edge_index, torch.tensor([[8, 16], [16, 8]])], dim=1)
    data.num_classes = 2
    for name in ('train', 'val', 'test'):
        setattr(data, name + '_indices', getattr(data, name + '_mask').nonzero().flatten().numpy())
    args = runtime_defaults()
    args.update(gu_defaults('GIF'))
    args.update(base_model='GCN', downstream_task='node', unlearn_task='node',
                unlearning_methods='GIF', num_runs=1, num_unlearned_nodes=1,
                dataset_name='cpu_fixture', iteration=100, scale=100.0, damp=0.5,
                run_update_detection_auc=False)
    model = create_model({'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 4},
                         'cpu_fixture', data, 'cpu')
    changed = data.clone()
    mask = getattr(data, population + '_mask')
    changed.y[mask] = 1 - changed.y[mask]
    with seeded_execution(42):
        first, _ = gif_node(copy.deepcopy(args), copy.deepcopy(model), data.clone(), [8], root)
    with seeded_execution(42):
        second, _ = gif_node(copy.deepcopy(args), copy.deepcopy(model), changed, [8], root)
    equal = all(torch.equal(value, second.state_dict()[name]) for name, value in first.state_dict().items())
    assert equal == (population != 'train')
    assert any(not torch.equal(value, model.state_dict()[name]) for name, value in first.state_dict().items())


def test_failed_solve_leaves_actual_model_untouched():
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.GIF.solver import GIFConvergenceError
    model = torch.nn.Linear(2, 1, bias=False).double()
    original = copy.deepcopy(model.state_dict())
    params = list(model.parameters())
    gradient = torch.autograd.grad(sum((p*p).sum() for p in params), params, create_graph=True)
    instance = gif.__new__(gif)
    instance.args = dict(iteration=100, scale=1e9, damp=0., dataset_name='fixture', GIF_method='GIF')
    instance.target_model = SimpleNamespace(model=model, eval_unlearn=lambda _: pytest.fail('evaluated failed update'))
    with pytest.raises(GIFConvergenceError):
        instance.approxi((gradient, tuple(torch.ones_like(p) for p in params), tuple(torch.zeros_like(p) for p in params)))
    assert instance.solver_diagnostics['status'] == 'not_converged'
    for name, value in model.state_dict().items():
        assert torch.equal(value, original[name])


def test_node_deletion_removes_exact_incident_edges_independent_of_order():
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    edges = torch.tensor([[0,1,1,2,2,3,3,0], [1,0,2,1,3,2,0,3]])
    for index in (torch.arange(8), torch.tensor([5,0,7,2,3,6,1,4])):
        instance = gif.__new__(gif)
        instance.args = {'unlearn_task': 'node'}
        instance.data = SimpleNamespace(edge_index=edges[:,index])
        expected = instance.data.edge_index[:, ~(instance.data.edge_index == 1).any(0)]
        assert torch.equal(instance.update_edge_index_unlearn([1]), expected)
