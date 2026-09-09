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


@pytest.fixture
def shared_shards_dependency(monkeypatch):
    # Before integration, the registered AAGU-045 dependency can be explicitly
    # supplied to this test process. Production never imports external source.
    import importlib.util
    import os
    import sys
    path = os.environ.get('OPENGU_SHARDS_TEST_SOURCE')
    if path:
        spec = importlib.util.spec_from_file_location('experiments.modular_shards', path)
        module = importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules, spec.name, module)
        spec.loader.exec_module(module)
    else:
        import experiments.modular_shards


from test_modular_consumers import tables, run, write_yaml


def test_graphrevoker_yaml_output_metrics_and_exact_cache(tables, shared_shards_dependency):
    import numpy as np
    from experiments.unlearning_outputs import load_output, restore_model
    root = tables[0]
    value = {'kind': 'unlearning', 'schema_version': 1, 'method': 'GraphRevoker',
             'model': {'hidden_channels': 4}, 'training': {'epochs': 2},
             'parameters': {'num_shards': 2, 'opt_num_epochs': 1, 'num_opt_samples': 1,
                            'gpa_epochs': 1, 'gpa_hidden_channels': 8, 'gpa_batch_size': 64}}
    write_yaml(root / 'revoker.yaml', value)
    args = dict(selector_refs=['degree.yaml'], stage='unlearning', unlearning_refs=['revoker.yaml'])
    cold = run(tables, 'revoker_cold', **args)['unlearning'][0]
    warm = run(tables, 'revoker_warm', **args)['unlearning'][0]
    assert cold['producer_called'] and warm['hit']
    assert not cold['ensemble_preparation']['hit'] and warm['ensemble_preparation']['hit']
    assert cold['output'] == warm['output']
    index = list(root.rglob('index.sqlite'))
    assert len(index) == 1
    payload = load_output(cold['output'], index[0].parent, dataset_root=root)
    restored = restore_model(payload)
    with torch.no_grad():
        logits = restored(torch.tensor(payload.arrays['x']), torch.tensor(payload.arrays['evaluation_edge_index']))
    np.testing.assert_allclose(logits.numpy(), payload.arrays['logits'], atol=1e-6)
    assert len(restored.shard_models) == 2
    assert hasattr(restored, 'partition_encoder') and hasattr(restored, 'partitioner')
    assert len(payload.arrays['selected_nodes']) == 1
    assert not np.array_equal(payload.arrays['logits_before'], payload.auxiliary['canonical_logits_before'])
    assert cold['evaluation'] == warm['evaluation']
    write_yaml(root / 'random.yaml', {'kind': 'selector', 'schema_version': 1, 'method': 'random',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 1}})
    other = run(tables, 'revoker_random', stage='unlearning', selector_refs=['random.yaml'],
                unlearning_refs=['revoker.yaml'])['unlearning'][0]
    assert other['ensemble_preparation']['hit']
    assert other['output'] != cold['output']
    value['parameters']['gpa_lr'] = .002
    write_yaml(root / 'revoker.yaml', value)
    changed = run(tables, 'revoker_changed', **args)['unlearning'][0]
    assert not changed['hit'] and not changed['ensemble_preparation']['hit']
    assert changed['output'] != cold['output']


def test_graphrevoker_three_dataset_dryrun(tmp_path):
    import yaml
    from experiments.modular_run import execute
    path = tmp_path / 'experiment.yaml'
    path.write_text(yaml.safe_dump({'kind': 'experiment', 'schema_version': 1,
        'experiment_id': 'revoker_dry', 'stage': 'unlearning',
        'dataset_refs': ['cora.yaml', 'citeseer.yaml', 'pubmed.yaml'],
        'selector_refs': ['degree.yaml'], 'unlearning_refs': ['graphrevoker.yaml'],
        'seeds': [42, 212, 2024], 'budget_ratios': [.1], 'matrix': 'cartesian_product'}), encoding='utf-8')
    result = execute(path, dry_run=True)
    assert result['logical_cells'] == 9 and not result['producer_called']
