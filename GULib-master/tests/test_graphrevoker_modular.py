"""Real GPA and GraphRevoker aggregation without global file-backed datasets."""
import logging
import pytest
import torch
from torch_geometric.data import Data
from experiments.modular_graphrevoker import (
    graphrevoker_defaults, validate_graphrevoker, graphrevoker_weights, graphrevoker_partition)
from experiments.modular_model import runtime_defaults
from experiments.modular_config import model_training


def inputs():
    torch.set_num_threads(1)
    torch.manual_seed(4)
    n = 24
    nodes = torch.arange(n)
    # Interleaved train/test nodes exercise global->local remapping.
    train = nodes % 3 != 2
    chain = torch.stack([nodes[:-1], nodes[1:]])
    jump = torch.stack([nodes[:-2], nodes[2:]])
    edges = torch.cat([chain, chain.flip(0), jump, jump.flip(0)], 1)
    return Data(x=torch.randn(n, 3), y=nodes % 2, edge_index=edges,
                train_mask=train, val_mask=(~train) & (nodes < 12), test_mask=(~train) & (nodes >= 12))


def settings():
    p = graphrevoker_defaults(runtime_defaults())
    p.update(num_shards=2, gpa_epochs=1, gpa_hidden_channels=8, gpa_batch_size=64,
             opt_num_epochs=1, num_opt_samples=1, shard_size_delta=0.)
    return p


def test_real_gpa_train_subgraph_nondefault_parameters_and_determinism():
    from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition_gpa import partition_embeddings
    data, p = inputs(), settings()
    embeddings = torch.log_softmax(torch.randn(int(data.train_mask.sum()), 2), -1)
    torch.manual_seed(11)
    assignment, model = partition_embeddings(data, embeddings, p, logging.getLogger('test'))
    assert len(assignment) == int(data.train_mask.sum())
    assert set(assignment.tolist()) == {0, 1}
    assert model.cls[0].in_features == 8
    torch.manual_seed(11)
    again, _ = partition_embeddings(data, embeddings, p, logging.getLogger('test'))
    assert torch.equal(assignment, again)


def test_real_node_embedding_and_partition_have_saved_models():
    data, p = inputs(), settings()
    model, training = model_training({'model': {'hidden_channels': 4}, 'training': {'epochs': 2}})
    assignment, encoder, partitioner = graphrevoker_partition(
        {'model': model, 'training': training, 'parameters': p}, data)
    assert (assignment[~data.train_mask] == -1).all()
    assert set(assignment[data.train_mask].tolist()) == {0, 1}
    assert encoder.state_dict() and partitioner.state_dict()


def test_original_optimal_aggregator_executes_and_normalizes():
    data, p = inputs(), settings()
    class Model(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = torch.nn.Linear(3, 2)
        def forward(self, x, edge_index):
            return self.linear(x)
    class Ensemble(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.shard_models = torch.nn.ModuleList([Model(), Model()])
    weights = graphrevoker_weights(Ensemble(), data, p)
    assert weights.shape == (2,)
    assert torch.isfinite(weights).all() and (weights >= 0).all()
    assert weights.sum().item() == pytest.approx(1.)


def test_invalid_partition_rejected():
    from experiments.effective_config import ConfigurationError
    p = settings()
    p['partition_method'] = 'random'
    with pytest.raises(ConfigurationError):
        validate_graphrevoker(p)
