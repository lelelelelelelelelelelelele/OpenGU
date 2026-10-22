"""Separate shard budgets, exact Selection reuse, and persisted ensemble semantics."""
import copy
import functools
import json
import pickle

import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
def test_budget_validation_and_base_isolation(method):
    from experiments.modular_config import unlearning
    from experiments.effective_config import ConfigurationError
    value = dict(kind='unlearning', schema_version=1, method=method)
    resolved = unlearning(value)
    assert resolved['parameters']['shard_epochs'] == 300
    assert resolved['training']['epochs'] == 3000
    if method == 'GraphRevoker':
        assert resolved['parameters']['gpa_epochs'] == 10
    for invalid in (0, -1, 1.5, True, '300'):
        with pytest.raises(ConfigurationError, match='shard_epochs'):
            unlearning({**value, 'parameters': {'shard_epochs': invalid}})


@pytest.mark.parametrize('method', ['GraphEraser', 'GraphRevoker'])
def test_real_training_budget_reuse_before_and_restore(tables, method, monkeypatch):
    from experiments import modular_model as models
    from experiments.modular_config import unlearning
    from experiments.checkpoint_references import ensemble_identity, training_identity
    from experiments.unlearning_outputs import load_output, restore_model
    root = tables[0]
    parameters = dict(shard_epochs=3, num_shards=2, opt_num_epochs=1, num_opt_samples=1)
    if method == 'GraphRevoker':
        parameters.update(gpa_epochs=1, gpa_hidden_channels=8, gpa_batch_size=64)
    value = dict(kind='unlearning', schema_version=1, method=method,
                 model={'hidden_channels': 4}, training={'epochs': 2}, parameters=parameters)
    write_yaml(root / 'method.yaml', value)
    options = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['method.yaml'])
    observed = []
    original = models.train_supervised

    @functools.wraps(original)
    def record(model, data, training, steps):
        observed.append((copy.deepcopy(training), steps, data.train_mask.clone()))
        return original(model, data, training, steps)

    monkeypatch.setattr(models, 'train_supervised', record)
    first = run(tables, 'budget_cold', **options)
    cold = first['unlearning'][0]
    exported = json.loads((root / 'results/runs/budget_cold/budget_cold/run.json').read_text(encoding='utf-8'))['cells'][0]
    assert exported['timing']['shard_training'] == cold['training_timing']
    assert exported['cache_provenance']['ensemble'] == cold['ensemble_preparation']
    assert cold['producer_called'] and not cold['ensemble_preparation']['hit']
    assert sum(t['epochs'] == 2 for t, _, _ in observed) == (2 if method == 'GraphRevoker' else 1)
    assert sum(t['epochs'] == 3 for t, _, _ in observed) == 2 + cold['training_timing']['affected_shards']
    assert all(tuple(steps) == (3,) for t, steps, _ in observed if t['epochs'] == 3)
    data = pickle.loads((root / 'graph.pkl').read_bytes())
    instance = unlearning(value)
    assert ensemble_identity(instance, data) == cold['ensemble_preparation']['consumption_metadata']
    base_identity = training_identity(instance, data)
    store = next(root.rglob('index.sqlite')).parent
    payload = load_output(cold['output'], store, dataset_root=root)
    selected = payload.arrays['selected_nodes'].tolist()
    for _, _, mask in observed[-cold['training_timing']['affected_shards']:]:
        assert not mask[selected].any()
    restored = restore_model(payload)
    with torch.no_grad():
        logits = restored(torch.tensor(payload.arrays['x']), torch.tensor(payload.arrays['evaluation_edge_index']))
    np.testing.assert_allclose(logits.numpy(), payload.arrays['logits'], atol=1e-6)
    # Re-open the exact initial ensemble; before is method-specific, on the same graph.
    if method == 'GraphEraser':
        from experiments.modular_shards import prepare_ensemble as prepare
    else:
        from experiments.modular_graphrevoker import prepare_graphrevoker_ensemble as prepare
    ensemble, _ = prepare(instance, data, root / 'results/runtime/modular/checkpoints')
    with torch.no_grad():
        before = ensemble(data.x, data.edge_index)
    np.testing.assert_allclose(before.numpy(), payload.arrays['logits_before'], atol=1e-6)
    previous_calls = len(observed)
    warm = run(tables, 'budget_warm', **options)
    assert len(observed) == previous_calls
    assert warm['unlearning'][0]['output'] == cold['output']
    # A shard-only change reuses Selection and the base model but neither ensemble nor Output.
    value['parameters']['shard_epochs'] = 4
    write_yaml(root / 'method.yaml', value)
    assert training_identity(unlearning(value), data) == base_identity
    changed = run(tables, 'budget_changed', **options)
    new = changed['unlearning'][0]
    assert changed['selectors'][0]['selection']['artifact'] == first['selectors'][0]['selection']['artifact']
    assert changed['selectors'][0]['selection']['cache']['hit'] and not changed['selectors'][0]['selection']['cache']['producer_called']
    assert new['checkpoint']['state_hash'] == cold['checkpoint']['state_hash']
    assert new['producer_called'] and not new['ensemble_preparation']['hit']
    assert new['output'] != cold['output']
    assert new['ensemble_preparation']['consumption_metadata'] != cold['ensemble_preparation']['consumption_metadata']
    # The old exact artifact remains readable and unchanged.
    old = load_output(cold['output'], store, dataset_root=root)
    np.testing.assert_array_equal(old.arrays['logits'], payload.arrays['logits'])
