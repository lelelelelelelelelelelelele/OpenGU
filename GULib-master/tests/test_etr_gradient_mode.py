"""Dropout must not confound the gradients compared by ETR."""
import torch
from torch_geometric.data import Data
from unlearning.unlearning_methods.ETR.etr import gradient_information


class DropoutClassifier(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.input = torch.nn.Linear(2, 3, bias=False)
        self.dropout = torch.nn.Dropout(p=1.0)
        self.output = torch.nn.Linear(3, 2, bias=False)
        with torch.no_grad():
            self.input.weight.fill_(0.25)
            self.output.weight.copy_(torch.tensor([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]))

    def forward(self, x, edge_index):
        return self.output(self.dropout(self.input(x).relu()))


def test_edit_gradients_disable_dropout_and_keep_autograd():
    model = DropoutClassifier().train()
    graph = Data(x=torch.tensor([[1., 2.], [2., 1.], [1., 1.]]),
                 y=torch.tensor([0, 0, 1]),
                 edge_index=torch.empty((2, 0), dtype=torch.long),
                 train_mask=torch.tensor([True, True, True]), mapping=torch.tensor([0, 1]))
    before = {name: p.clone() for name, p in model.named_parameters()}
    for seed_loss in (False, True):
        gradients, importance = gradient_information(model, graph, seed_loss=seed_loss)
        assert not model.training
        assert all(torch.count_nonzero(g) > 0 and torch.isfinite(g).all() for g in gradients.values())
        assert all(torch.equal(importance[n], g.square()) for n, g in gradients.items())
        torch.rand(31)
        repeated, _ = gradient_information(model.train(), graph, seed_loss=seed_loss)
        assert all(torch.equal(gradients[n], g) for n, g in repeated.items())
    assert all(torch.equal(before[n], p) for n, p in model.named_parameters())
