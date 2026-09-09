import copy
import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml


def test_grapheraser_real_output_cache_and_reconstruction(tables):
    from experiments.unlearning_outputs import load_output, restore_model
    root, _, _ = tables
    write_yaml(root / 'eraser.yaml', {'kind': 'unlearning', 'schema_version': 1,
        'method': 'GraphEraser', 'model': {'hidden_channels': 4}, 'training': {'epochs': 3},
        'parameters': {'num_shards': 2, 'opt_num_epochs': 2, 'num_opt_samples': 1}})
    cold = run(tables, 'eraser_cold', selector_refs=['degree.yaml'],
        stage='unlearning', unlearning_refs=['eraser.yaml'])
    warm = run(tables, 'eraser_warm', selector_refs=['degree.yaml'],
        stage='unlearning', unlearning_refs=['eraser.yaml'])
    first, second = cold['unlearning'][0], warm['unlearning'][0]
    assert first['producer_called'] and second['hit']
    assert not first['ensemble_preparation']['hit']
    assert second['ensemble_preparation']['hit']
    assert first['output'] == second['output']
    # Locate the fixture's exact Store rather than guessing its layout.
    indexes = list(root.rglob('index.sqlite'))
    assert len(indexes) == 1
    payload = load_output(first['output'], indexes[0].parent, dataset_root=root)
    restored = restore_model(payload)
    with torch.no_grad():
        logits = restored(torch.tensor(payload.arrays['x']), torch.tensor(payload.arrays['edge_index']))
    np.testing.assert_allclose(logits.numpy(), payload.arrays['logits'], atol=1e-6)
    assert len(restored.shard_models) == 2
    assert 'canonical_logits_before' in payload.auxiliary
    assert not np.array_equal(payload.arrays['logits_before'], payload.auxiliary['canonical_logits_before'])
    write_yaml(root / 'random.yaml', {'kind': 'selector', 'schema_version': 1,
        'method': 'random', 'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 1}})
    other = run(tables, 'eraser_random', selector_refs=['random.yaml'],
        stage='unlearning', unlearning_refs=['eraser.yaml'])
    assert other['unlearning'][0]['ensemble_preparation']['hit']


def test_grapheraser_rejects_unavailable_configuration():
    from experiments.modular_config import unlearning
    from experiments.effective_config import ConfigurationError
    with pytest.raises(ConfigurationError, match='lpa_base'):
        unlearning({'kind': 'unlearning', 'schema_version': 1,
                    'method': 'GraphEraser', 'parameters': {'partition_method': 'gpa'}})


def test_partition_exact_training_pool(tables):
    import pickle
    from experiments.modular_config import gu_defaults
    from experiments.modular_shards import partition_nodes
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    parameters = {**gu_defaults('GraphEraser'), 'num_shards': 2}
    assignment = partition_nodes(data, parameters)
    assert (assignment[~data.train_mask] == -1).all()
    assert (assignment[data.train_mask] >= 0).all()
    assert set(assignment[data.train_mask].tolist()) == {0, 1}


def test_partition_no_edges_converges(tables):
    import pickle
    from experiments.modular_config import gu_defaults
    from experiments.modular_shards import partition_nodes
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    data.edge_index = torch.empty((2, 0), dtype=torch.long)
    assignment = partition_nodes(data, {**gu_defaults('GraphEraser'), 'num_shards': 2})
    assert (assignment[data.train_mask] >= 0).all()
