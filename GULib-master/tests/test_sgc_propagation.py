"""Validate configured SGC depth against an independent normalized adjacency."""
import pytest
import torch
from torch_geometric.data import Data

from experiments.modular_config import model_training
from experiments.modular_model import create_model


@pytest.mark.parametrize('layers', [2, 3])
def test_sgc_forward_matches_requested_propagation(layers):
    torch.manual_seed(71)
    edges = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 4], [1, 0, 2, 1, 3, 2, 4, 3]])
    data = Data(x=torch.randn(5, 3, dtype=torch.float64), y=torch.arange(5) % 2,
                edge_index=edges)
    config, _ = model_training({'model': {'architecture': 'OpenGU.SGCNet', 'layers': layers}})
    model = create_model(config, 'fixture', data, torch.device('cpu')).double().eval()
    adjacency = torch.eye(5, dtype=torch.float64)
    adjacency[edges[1], edges[0]] = 1
    inverse_degree = adjacency.sum(1).rsqrt()
    normalized = inverse_degree[:, None] * adjacency * inverse_degree[None, :]
    weights = model.convs[0].lin.weight.T
    expected = torch.linalg.matrix_power(normalized, layers) @ data.x @ weights
    other_depth = torch.linalg.matrix_power(normalized, 5-layers) @ data.x @ weights
    actual = model(data.x, data.edge_index)
    torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
    assert not torch.allclose(actual, other_depth)


@pytest.mark.parametrize('layers', [0, -1, 2.5, True])
def test_sgc_rejects_invalid_propagation_count(layers):
    with pytest.raises(ValueError):
        model_training({'model': {'architecture': 'OpenGU.SGCNet', 'layers': layers}})


def test_gcn_depth_contract_is_unchanged():
    with pytest.raises(ValueError):
        model_training({'model': {'architecture': 'OpenGU.GCNNet', 'layers': 3}})
