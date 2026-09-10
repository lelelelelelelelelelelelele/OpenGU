"""GIF must not use held-out labels to compute a parameter update."""
import copy
import json

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


def test_nonfinite_hvp_leaves_actual_model_untouched():
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.GIF.solver import GIFNumericalError
    model = torch.nn.Linear(2, 1, bias=False).double()
    original = copy.deepcopy(model.state_dict())
    params = list(model.parameters())
    gradient = torch.autograd.grad(sum((p*p).sum() for p in params), params, create_graph=True)
    instance = gif.__new__(gif)
    instance.args = dict(iteration=1, scale=1e9, damp=0., dataset_name='fixture', GIF_method='GIF')
    instance.target_model = SimpleNamespace(model=model, eval_unlearn=lambda _: pytest.fail('evaluated failed update'))
    with pytest.raises(GIFNumericalError):
        # A numerical failure must never mutate the target model.
        instance.approxi((tuple(g*float("nan") for g in gradient), tuple(torch.ones_like(p) for p in params), tuple(torch.zeros_like(p) for p in params)))
    assert instance.solver_diagnostics['status'] == 'nonfinite'
    for name, value in model.state_dict().items():
        assert torch.equal(value, original[name])


def test_first_hvp_treats_gradient_derived_rhs_as_a_fixed_vector():
    """L=theta^2, v=theta: H=2 and delta=0.5 at theta=1.

    Differentiating v again gives 4 instead of H*v=2 in the first old HVP;
    with scale=2 and one step the historical implementation returns delta=0.
    Exercise the actual update entry with a RHS that retains its autograd graph.
    """
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    model = torch.nn.Linear(1, 1, bias=False).double()
    with torch.no_grad():
        model.weight.fill_(1.)
    params = list(model.parameters())
    all_gradient = torch.autograd.grad((model.weight**2).sum(), params, create_graph=True)
    rhs = torch.autograd.grad(.5*(model.weight**2).sum(), params, create_graph=True)
    assert rhs[0].requires_grad
    instance = gif.__new__(gif)
    instance.args = dict(iteration=1, scale=2., damp=0., dataset_name='fixture', GIF_method='GIF')
    instance.target_model = SimpleNamespace(model=model, eval_unlearn=lambda _: 0.)
    instance.approxi((all_gradient, rhs, tuple(torch.zeros_like(p) for p in params)))
    torch.testing.assert_close(model.weight, torch.tensor([[1.5]], dtype=torch.double))
    assert instance.solver_diagnostics['relative_residual'] <= 1e-3


def test_finite_solve_cannot_write_overflowed_parameters():
    from types import SimpleNamespace
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.GIF.solver import GIFNumericalError
    model = torch.nn.Linear(1, 1, bias=False)
    with torch.no_grad():
        model.weight.fill_(3e38)
    original = model.weight.detach().clone()
    instance = gif.__new__(gif)
    instance.args = dict(iteration=1, scale=1., damp=0., dataset_name='fixture', GIF_method='GIF')
    instance.target_model = SimpleNamespace(model=model, eval_unlearn=lambda _: pytest.fail('nonfinite write'))
    with pytest.raises(GIFNumericalError):
        instance.approxi(((model.weight,), (torch.full_like(model.weight, 1e38),),
                         (torch.zeros_like(model.weight),)))
    assert instance.solver_diagnostics['status'] == 'nonfinite_parameters'
    assert torch.equal(model.weight, original)


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


def test_finite_truncated_update_publishes_output_with_honest_diagnostics(tables):
    from test_modular_consumers import run, write_yaml
    root,_,gu=tables
    gu['method']='GIF'
    gu['parameters']={'iteration': 1}
    write_yaml(root/'gif-default.yaml',gu)
    run(tables,'gif-default-experiment',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['gif-default.yaml'])
    assert list((root/'results/cache_v2/artifacts/prediction').glob('*/payload.npz'))
    receipts=list(root.rglob('gif-solver.json'))
    assert len(receipts)==1
    diagnostics=json.loads(receipts[0].read_text())
    assert diagnostics['status']=='finite_truncation'
    assert diagnostics['relative_residual'] > diagnostics['rtol']
    assert not diagnostics['residual_within_tolerance']


def test_nonfinite_update_cannot_publish_output(tables, monkeypatch):
    from test_modular_consumers import run, write_yaml
    import unlearning.unlearning_methods.GIF.solver as solver
    from unlearning.unlearning_methods.GIF.solver import GIFNumericalError
    original=solver.solve_gif_system
    def broken_hvp(matvec, rhs, **kwargs):
        return original(lambda v:v*float('nan'), rhs, **kwargs)
    monkeypatch.setattr(solver, 'solve_gif_system', broken_hvp)
    # gif imports the function directly, so patch the actual adapter consumer.
    import importlib
    module=importlib.import_module('unlearning.unlearning_methods.GIF.gif')
    monkeypatch.setattr(module, 'solve_gif_system', broken_hvp)
    root,_,gu=tables
    gu['method']='GIF'
    gu['parameters']={'iteration':1}
    write_yaml(root/'gif-failure.yaml',gu)
    with pytest.raises(GIFNumericalError):
        run(tables,'gif-failure-experiment',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['gif-failure.yaml'])
    assert not list((root/'results/cache_v2/artifacts/prediction').glob('*/payload.npz'))
    receipts=list(root.rglob('gif-solver.json'))
    assert len(receipts)==1
    assert json.loads(receipts[0].read_text())['status']=='nonfinite'


def solver_variant(*args, **kwargs):
    raise RuntimeError('identity test only')


def test_solver_source_participates_in_gif_producer(monkeypatch):
    from experiments.modular_gu import gu_producer
    import unlearning.unlearning_methods.GIF.solver as solver
    config={'architecture':'OpenGU.GCNNet'}
    before=gu_producer('GIF',config)
    retrain=gu_producer('Retrain',config)
    monkeypatch.setattr(solver,'solve_gif_system',solver_variant)
    assert gu_producer('GIF',config)!=before
    assert gu_producer('Retrain',config)==retrain
