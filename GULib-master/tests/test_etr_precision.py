"""ETR numerical boundaries checked against independent high-precision arithmetic."""
from decimal import Decimal, localcontext

import pytest
import torch
from torch_geometric.data import Data
from unlearning.unlearning_methods.ETR.etr import erase, gradient_information


@pytest.mark.parametrize('dtype', [torch.float32, torch.float64])
def test_second_ratio_underflow_matches_decimal_and_keeps_parameter_dtype(dtype):
    model = torch.nn.Linear(100, 1, bias=False).to(dtype)
    with torch.no_grad():
        model.weight.fill_(1.)
    original = torch.ones(1, 100)
    forgotten = original.clone()
    influenced = original.clone()
    original[0, :3] = torch.tensor([1e-24, 1e-24, 2e-24])
    forgotten[0, :3] = torch.tensor([1e-18, 1e-20, 1e-20])
    influenced[0, :3] = torch.tensor([1e-30, 1e-18, 1e-18])
    assert original.square()[0, 1] == 0  # The former computation loses this numerator.
    with localcontext() as ctx:
        ctx.prec = 70
        dec = lambda x: Decimal.from_float(float(x))
        first = [min(dec(o) / dec(f), Decimal(1)) for o, f in zip(original[0], forgotten[0])]
        second = [min(dec(o)**2 / (dec(f)*dec(k)), Decimal(1))
                  for o, f, k in zip(original[0], forgotten[0], influenced[0])]
        quantile = lambda values: sorted(values)[0] * Decimal('.01') + sorted(values)[1] * Decimal('.99')
        q1, q2 = quantile(first), quantile(second)
        expected = [float(b1/q1) if b1 <= q1 else float(b2/q2) if b2 <= q2 else 1.
                    for b1, b2 in zip(first, second)]
    erase(model, {'weight': original}, {'weight': forgotten}, {'weight': influenced}, .01)
    assert model.weight.dtype == dtype and torch.isfinite(model.weight).all()
    torch.testing.assert_close(model.weight[0], torch.tensor(expected, dtype=dtype), atol=1e-7, rtol=1e-6)
    assert 0 < model.weight[0, 1] < 1  # Second group is a real, nonzero update.


def test_importance_preserves_nonzero_gradient_before_first_square():
    class Classifier(torch.nn.Linear):
        def forward(self, x, edge_index):
            return super().forward(x)
    model = Classifier(2, 2, bias=False)
    graph = Data(x=torch.full((2, 2), 1e-23), y=torch.zeros(2, dtype=torch.long),
                 edge_index=torch.empty((2, 0), dtype=torch.long), train_mask=torch.ones(2, dtype=torch.bool))
    gradients, importance = gradient_information(model, graph, seed_loss=False)
    assert gradients['weight'].dtype == torch.float32
    assert torch.all(gradients['weight'] != 0) and torch.all(gradients['weight'].square() == 0)
    assert importance['weight'].dtype == torch.float64 and torch.all(importance['weight'] > 0)


@pytest.mark.parametrize('invalid', [float('nan'), float('inf'), -1.])
def test_invalid_importance_is_rejected_instead_of_becoming_a_valid_edit(invalid):
    model = torch.nn.Linear(100, 1, bias=False)
    before = model.weight.detach().clone()
    original = torch.ones_like(model.weight)
    original[0, 0] = invalid
    ones = {'weight': torch.ones_like(original)}
    with pytest.raises(ValueError, match='finite and nonnegative'):
        erase(model, {'weight': original}, ones, ones, .01)
    assert torch.equal(before, model.weight)


def test_float32_etr_producer_is_not_a_compatible_output_candidate():
    from experiments.modular_gu import gu_producer
    from cache_v2.source_compatibility import source_candidates
    model = {'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 64, 'dropout': .5}
    producer = gu_producer('ETR', model).to_dict()
    legacy = 'a15eb8b2d58ba5d70997aa3c46f6c797ca96109a8f65cfe4427a0efbe408527b'
    candidates = list(source_candidates('prediction', 'ETR',
        {'semantic_version': producer['semantic_version'], 'model': model},
        {'source_fingerprint': producer['source_fingerprint']}))
    assert producer['source_fingerprint'] != legacy
    assert all(member['source_fingerprint'] != legacy for member in candidates)
