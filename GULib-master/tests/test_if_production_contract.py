"""Independent references for the production GIF/IDEA finite update."""
import copy
from types import SimpleNamespace

import pytest
import torch

from test_modular_consumers import tables


@pytest.mark.parametrize('method', ['GIF', 'IDEA'])
@pytest.mark.parametrize('dataset', ['fixture', 'Photo'])
@pytest.mark.parametrize('steps', [1, 4])
def test_production_matches_matrix_polynomial(method, dataset, steps):
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.IDEA.idea import idea
    model = torch.nn.Linear(2, 1, bias=False).double()
    with torch.no_grad():
        model.weight.copy_(torch.tensor([[.2, -.3]]))
    theta = model.weight
    initial = theta.detach().clone()
    h = torch.tensor([[4., 1.], [1., -2.]], dtype=torch.double)
    loss = .5 * theta.flatten() @ h @ theta.flatten()
    gradient = torch.autograd.grad(loss, [theta], create_graph=True)
    rhs = torch.autograd.grad(.5 * theta.square().sum(), [theta], create_graph=True)
    instance = (gif if method == 'GIF' else idea).__new__(gif if method == 'GIF' else idea)
    instance.args = dict(iteration=steps, scale=6., damp=0., dataset_name=dataset,
                         GIF_method='GIF', gaussian_mean=0., gaussian_std=0.)
    instance.edge_weight_unlearn = None
    instance.target_model = SimpleNamespace(model=model, eval_unlearn=lambda _: 0.,
        evaluate_unlearn_F1=lambda *a, **kw: 0.)
    transition = torch.eye(2, dtype=torch.double) - h / 6
    expected = sum(torch.linalg.matrix_power(transition, j) @ initial.flatten()
                   for j in range(steps + 1)) / 6
    instance.approxi((gradient, rhs, (torch.zeros_like(theta),)))
    torch.testing.assert_close(theta, initial + expected.reshape_as(theta))
    assert instance.solver_diagnostics['iterations'] == steps


def test_idea_nonfinite_rejected_before_evaluation_or_write():
    from unlearning.unlearning_methods.IDEA.idea import idea
    from unlearning.unlearning_methods.GIF.solver import GIFNumericalError
    model = torch.nn.Linear(1, 1, bias=False).double()
    initial = model.weight.detach().clone()
    gradient = torch.autograd.grad(model.weight.square().sum(), [model.weight], create_graph=True)
    instance = idea.__new__(idea)
    instance.args = dict(iteration=1, scale=1., damp=0., gaussian_mean=0., gaussian_std=0.)
    instance.target_model = SimpleNamespace(model=model,
        evaluate_unlearn_F1=lambda *a, **kw: pytest.fail('evaluated failed update'))
    with pytest.raises(GIFNumericalError):
        instance.approxi((tuple(g * float('nan') for g in gradient),
                         (torch.ones_like(model.weight),), (torch.zeros_like(model.weight),)))
    torch.testing.assert_close(model.weight, initial, rtol=0, atol=0)


def test_idea_hessian_uses_actual_training_forward(tables, monkeypatch):
    from experiments.modular_run import read_dataset
    from experiments.modular_config import load_instance, gu_defaults
    from experiments.modular_model import runtime_defaults, create_model
    from experiments.modular_idea import idea_node
    from unlearning.unlearning_methods.IDEA.idea import idea
    root, _, _ = tables
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    data.num_classes = 2
    data.train_indices = data.train_mask.nonzero().flatten().numpy()
    model = create_model({'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 4},
                         'cpu_fixture', data, 'cpu')
    args = runtime_defaults()
    args.update(gu_defaults('IDEA'))
    args.update(base_model='GCN', downstream_task='node', unlearn_task='node',
                unlearning_methods='IDEA', num_runs=1, num_unlearned_nodes=1,
                dataset_name='cpu_fixture', iteration=2, scale=65536, damp=0.,
                gaussian_mean=0., gaussian_std=0.)
    original = idea.get_grad
    checked = []
    def verify(self, request):
        result = original(self, request)
        params = list(self.target_model.model.parameters())
        logits = self.target_model.model(self.data.x, self.data.edge_index)
        loss = torch.nn.functional.cross_entropy(logits[self.data.train_mask],
            self.data.y[self.data.train_mask], reduction='sum')
        reference = torch.autograd.grad(loss, params, create_graph=True)
        vectors = tuple(torch.ones_like(p) for p in params)
        actual_hvp = self.hvps(result[0], params, vectors)
        expected_hvp = torch.autograd.grad(reference, params, grad_outputs=vectors)
        for actual, expected in zip(result[0], reference):
            torch.testing.assert_close(actual, expected, rtol=1e-4, atol=1e-6)
        for actual, expected in zip(actual_hvp, expected_hvp):
            torch.testing.assert_close(actual, expected, rtol=1e-4, atol=1e-5)
        checked.append(True)
        return result
    monkeypatch.setattr(idea, 'get_grad', verify)
    idea_node(args, model, data, [8], root)
    assert checked == [True]
