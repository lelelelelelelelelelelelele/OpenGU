"""External pure weights skip training and drive the real GIF/IDEA consumers."""
import copy
import functools
import importlib
import json

import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from experiments.effective_config import ConfigurationError
from experiments.modular_config import load_instance, configuration_sources
from experiments.modular_model import create_model, prepare_model
from experiments.modular_run import read_dataset
from utils.target_checkpoint import state_hash, sha256_file

UNUSED = ('lr', 'weight_decay', 'epochs', 'optimizer', 'scheduler')


def external(tables, method='GIF'):
    root, _, base = tables
    data, _ = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    item = copy.deepcopy(base)
    item.update(method=method, checkpoint='weights.pt', training={'seed': 17},
                parameters={'iteration': 2, 'scale': 1000, 'damp': .1})
    if method == 'IDEA':
        item['parameters'].update(gaussian_mean=0., gaussian_std=.001)
    config = root / 'external.yaml'
    write_yaml(config, item)
    resolved = load_instance(config, 'unlearning')
    model = create_model(resolved['model'], 'cpu_fixture', data, 'cpu')
    weights = copy.deepcopy(model.state_dict())
    torch.save(weights, root / 'weights.pt')
    return data, item, resolved, weights


@pytest.mark.parametrize('settings', [{}, dict.fromkeys(UNUSED),
    dict(lr=.9, weight_decay=.1, epochs=888, optimizer='SGD', scheduler='none')])
def test_only_initial_training_settings_are_inactive(tables, settings):
    root = tables[0]
    _, item, _, _ = external(tables)
    item['training'] = {**settings, 'seed': 17}
    write_yaml(root / 'external.yaml', item)
    resolved = load_instance(root / 'external.yaml', 'unlearning')
    assert resolved['training'] == {**dict.fromkeys(UNUSED), 'seed': 17}
    assert resolved['checkpoint'] == str((root / 'weights.pt').resolve())
    sources = configuration_sources(root / 'external.yaml', resolved)
    assert all(sources['training.' + key] == 'not_applicable:external_checkpoint' for key in UNUSED)


@pytest.mark.parametrize('training', [None, {'seed': None}, {'seed': -1}, {'unknown': 1}])
def test_seed_and_training_mapping_remain_validated(tables, training):
    root = tables[0]
    _, item, _, _ = external(tables)
    item['training'] = training
    write_yaml(root / 'external.yaml', item)
    with pytest.raises(ConfigurationError):
        load_instance(root / 'external.yaml', 'unlearning')


@pytest.mark.parametrize('checkpoint', ['', {}, {'path': 'weights.pt'}, 123])
def test_invalid_checkpoint_declarations_rejected(tables, checkpoint):
    root = tables[0]
    _, item, _, _ = external(tables)
    item['checkpoint'] = checkpoint
    write_yaml(root / 'external.yaml', item)
    with pytest.raises(ConfigurationError):
        load_instance(root / 'external.yaml', 'unlearning')


@pytest.mark.parametrize('checkpoint', ['absent', None])
def test_no_checkpoint_still_trains_then_reuses_cache(tables, checkpoint):
    root = tables[0]
    data, item, _, _ = external(tables)
    if checkpoint == 'absent':
        del item['checkpoint']
    else:
        item['checkpoint'] = None
    item['training'] = {'seed': 17, 'epochs': 2}
    write_yaml(root / 'external.yaml', item)
    resolved = load_instance(root / 'external.yaml', 'unlearning')
    kwargs = dict(data=data, dataset_name='cpu_fixture', checkpoint_root=root / 'cached',
                  device='cpu', reference_directory=root)
    first, _, cold = prepare_model(resolved, **kwargs)
    second, _, warm = prepare_model(resolved, **kwargs)
    assert not cold['hit'] and warm['hit']
    assert state_hash(first.state_dict()) == state_hash(second.state_dict())
    item['training']['lr'] = None
    write_yaml(root / 'external.yaml', item)
    with pytest.raises(ConfigurationError):
        load_instance(root / 'external.yaml', 'unlearning')


@pytest.mark.parametrize('defect', ['missing', 'corrupt', 'wrapped', 'shape', 'key', 'dtype', 'nan'])
def test_bad_external_weights_never_fall_back_to_training(tables, monkeypatch, defect):
    root = tables[0]
    data, _, resolved, weights = external(tables)
    path = root / 'weights.pt'
    key = next(iter(weights))
    if defect == 'missing':
        path.unlink()
    elif defect == 'corrupt':
        path.write_bytes(b'not a checkpoint')
    else:
        if defect == 'wrapped':
            weights = {'state_dict': weights}
        elif defect == 'shape':
            weights[key] = torch.zeros(100)
        elif defect == 'key':
            del weights[key]
        elif defect == 'dtype':
            weights[key] = weights[key].double()
        elif defect == 'nan':
            weights[key].fill_(float('nan'))
        torch.save(weights, path)
    def forbidden(*args, **kwargs):
        pytest.fail('explicit PT must not inspect training cache or train')
    monkeypatch.setattr('experiments.modular_model.train_supervised', forbidden)
    monkeypatch.setattr('experiments.modular_model.load_cached_weights', forbidden)
    with pytest.raises(Exception):
        prepare_model(resolved, data=data, dataset_name='cpu_fixture', checkpoint_root=root / 'cached',
                      device='cpu', reference_directory=root)
    assert not (root / 'cached').exists()


@pytest.mark.parametrize('method', ['GIF', 'IDEA'])
def test_external_pt_reaches_real_solver_and_output_identity(tables, monkeypatch, method):
    root = tables[0]
    _, item, _, weights = external(tables, method)
    original_file_hash = sha256_file(root / 'weights.pt')
    # Producer discovery imports Retrain. Do that before patching so its module
    # cannot retain the forbidden test double after monkeypatch teardown.
    importlib.import_module('unlearning.unlearning_methods.Retrain.retrain')
    def forbidden(*args, **kwargs):
        pytest.fail('external weight execution trained or accessed training cache')
    monkeypatch.setattr('experiments.modular_model.train_supervised', forbidden)
    monkeypatch.setattr('experiments.modular_model.load_cached_weights', forbidden)
    module = importlib.import_module('unlearning.unlearning_methods.GIF.' + ('gif' if method == 'GIF' else 'solver'))
    actual_solver = module.solve_gif_system
    calls = []
    @functools.wraps(actual_solver)
    def observe(matvec, rhs, **kwargs):
        calls.append(kwargs.copy())
        return actual_solver(matvec, rhs, **kwargs)
    monkeypatch.setattr(module, 'solve_gif_system', observe)
    opts = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['external.yaml'])
    first = run(tables, method + '-external', **opts)
    first_row = first['unlearning'][0]
    cp = first_row['checkpoint']
    assert cp['state_hash'] == state_hash(weights)
    assert cp['file_sha256'] == original_file_hash and cp['source'] == 'external_state_dict'
    assert cp['effective_identity']['execution_seed'] == 17
    run_file = root / 'results/runs' / (method + '-external') / (method + '-external') / 'run.json'
    persisted = json.loads(run_file.read_text(encoding='utf-8'))
    assert persisted['cells'][0]['cache']['method_checkpoint'] == 'not_applicable'
    assert calls[0]['iterations'] == 2 and calls[0]['scale'] == 1000. and calls[0]['damp'] == .1
    assert not (root / 'checkpoints').exists()
    # Unused training values do not invalidate the already computed output.
    item['training'].update(lr=.99, epochs=999, weight_decay=.9, optimizer='SGD', scheduler='none')
    write_yaml(root / 'external.yaml', item)
    warm = run(tables, method + '-warm', **opts)['unlearning'][0]
    assert warm['hit'] and warm['recipe_hash'] == first_row['recipe_hash']
    assert len(calls) == 1
    item['parameters'].update(iteration=3, scale=2000, damp=.2)
    write_yaml(root / 'external.yaml', item)
    changed = run(tables, method + '-parameters', **opts)['unlearning'][0]
    assert not changed['hit'] and changed['recipe_hash'] != first_row['recipe_hash']
    assert calls[-1]['iterations'] == 3 and calls[-1]['scale'] == 2000. and calls[-1]['damp'] == .2
    assert sha256_file(root / 'weights.pt') == original_file_hash
    # Replacing contents at the same path must not reuse the old GU output.
    weights[next(iter(weights))].add_(.01)
    torch.save(weights, root / 'weights.pt')
    replaced = run(tables, method + '-replaced', **opts)['unlearning'][0]
    assert not replaced['hit'] and replaced['recipe_hash'] != changed['recipe_hash']
    assert replaced['checkpoint']['state_hash'] == state_hash(weights)

@pytest.mark.parametrize('method', ['MEGU', 'GNNDelete'])
def test_external_pt_real_non_solver_consumers(tables, monkeypatch, method):
    root, _, base = tables
    data, _, _, weights = external(tables)
    item = copy.deepcopy(base)
    item.update(method=method, checkpoint='weights.pt', training={'seed': 17},
                parameters={'unlearning_epochs': 2})
    if method == 'MEGU':
        item['parameters'].update(unlearn_lr=.015, unlearn_weight_decay=.001)
    write_yaml(root / 'external.yaml', item)
    def forbidden(*args, **kwargs):
        pytest.fail('explicit weights must skip initial training and cache')
    monkeypatch.setattr('experiments.modular_model.train_supervised', forbidden)
    monkeypatch.setattr('experiments.modular_model.load_cached_weights', forbidden)
    opts = dict(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['external.yaml'])
    first = run(tables, method + '-pure', **opts)['unlearning'][0]
    assert first['checkpoint']['state_hash'] == state_hash(weights)
    assert not first['hit']
    assert run(tables, method + '-warm', **opts)['unlearning'][0]['hit']
    assert not (root / 'checkpoints').exists()
    weights[next(iter(weights))].add_(.01)
    torch.save(weights, root / 'weights.pt')
    changed = run(tables, method + '-changed', **opts)['unlearning'][0]
    assert not changed['hit'] and changed['recipe_hash'] != first['recipe_hash']


def test_ordinary_cache_has_only_final_weights_and_external_needs_no_sidecar(tables):
    root, _, base = tables
    data, item, _, _ = external(tables)
    item.pop('checkpoint')
    item['training'] = {'epochs': 3, 'seed': 42}
    write_yaml(root / 'ordinary.yaml', item)
    resolved = load_instance(root / 'ordinary.yaml', 'unlearning')
    _, trajectory, obs = prepare_model(resolved, data=data, dataset_name='fixture',
        checkpoint_root=root / 'cached', device='cpu', reference_directory=root)
    assert trajectory == []
    assert all(isinstance(v, torch.Tensor) for v in torch.load(obs['path'], weights_only=True).values())
    from pathlib import Path
    Path(obs['path']).with_suffix('.json').unlink()
    item['checkpoint'] = obs['path']
    write_yaml(root / 'external.yaml', item)
    resolved = load_instance(root / 'external.yaml', 'unlearning')
    _, trajectory, explicit = prepare_model(resolved, data=data, dataset_name='fixture',
        checkpoint_root=root / 'forbidden-cache', device='cpu', reference_directory=root)
    assert explicit['state_hash'] == obs['state_hash'] and not trajectory


def test_selector_trajectory_is_independent_and_cache_verified(tables):
    from experiments.modular_config import selector
    root = tables[0]
    data, _, _, _ = external(tables)
    instance = selector({'kind': 'selector', 'schema_version': 1, 'method': 'tracin_cp_point_3',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 1},
        'model': {'hidden_channels': 4}, 'training': {'epochs': 8},
        'parameters': {'checkpoint_steps': [1, 3, 5]}})
    kwargs = dict(data=data, dataset_name='fixture', checkpoint_root=root/'cached', device='cpu', reference_directory=root)
    _, steps, cold = prepare_model(instance, **kwargs)
    _, _, warm = prepare_model(instance, **kwargs)
    assert [c['global_step'] for c in steps] == [1, 3, 5]
    assert not cold['hit'] and warm['hit']
    payload = torch.load(cold['path'], weights_only=True)
    assert payload['final_state_hash'] != steps[-1]['state_hash']
    payload['checkpoints'][0]['state'][next(iter(payload['checkpoints'][0]['state']))].add_(1.)
    torch.save(payload, cold['path'])
    with pytest.raises(ValueError, match='corrupt'):
        prepare_model(instance, **kwargs)
