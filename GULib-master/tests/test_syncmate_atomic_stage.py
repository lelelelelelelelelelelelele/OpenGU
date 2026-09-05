from pathlib import Path
import pytest
import torch

from experiments import syncmate_atomic_stage as stage
from experiments.modular_run import execute


def test_registered_atomic_plan_expands_exactly_one_cell():
    plan = execute(stage.ROOT / stage.PLANS['opengu-sm005-atomic-gpu-v1']['config'], dry_run=True)
    assert [x['method'] for x in plan['effective_selectors']] == ['degree']
    assert [x['method'] for x in plan['effective_unlearning']] == ['GNNDelete']
    assert [x['case'] for x in plan['effective_evaluations']] == ['post_unlearning_utility']
    gu = plan['effective_unlearning'][0]
    assert gu['training']['seed'] == 42 and gu['training']['epochs'] == 100
    assert gu['parameters']['unlearning_epochs'] == 50
    assert plan['producer_called'] is False


def test_absent_gpu_and_wrong_checkout_refuse_before_data_read(monkeypatch):
    from experiments import modular_run
    from scripts.syncmate import verify_core_dependency
    monkeypatch.setattr(torch.cuda, 'is_available', lambda: False)
    monkeypatch.setattr(verify_core_dependency, 'verify_core_dependency', lambda: {'errors': []})
    def forbidden(*args):
        raise AssertionError('device refusal must precede dataset access')
    monkeypatch.setattr(modular_run, 'read_dataset', forbidden)
    result = stage.preflight('opengu-sm005-b-hutch32-first-v1')
    assert not result['ready']
    assert any('no CPU fallback' in e for e in result['errors'])
    assert any('canonical SSH' in e for e in result['errors'])


def test_hutch_pair_preserves_scientific_config_and_shares_cache_only():
    from experiments.modular_execution import project_context
    from scripts.syncmate.opengu_recipes import recipe_definitions
    from syncmate_core.identity import sha256_recipe_config
    first, warm = [stage.PLANS[f'opengu-sm005-b-hutch32-{name}-v1'] for name in ('first', 'warm')]
    assert first['config'] == warm['config']
    expanded = execute(stage.ROOT / first['config'], dry_run=True)
    selector, = expanded['effective_selectors']
    assert selector['method'] == 'b_param_hutch'
    assert selector['parameters']['hutchinson'] == {'probes': 32, 'seed': 1729}
    assert selector['parameters']['lissa'] == {'iterations': 20, 'scale': 25.0, 'damp': 0.01}
    assert selector['budget'] == {'mode': 'ratio', 'value': 0.01}
    assert [x['method'] for x in expanded['effective_unlearning']] == ['GNNDelete']
    assert [x['case'] for x in expanded['effective_evaluations']] == ['post_unlearning_utility']
    contexts = [project_context(p['experiment_id'], run_id=p['run_id'], request_device='cuda',
                level='verification', repository_root=stage.ROOT) for p in (first, warm)]
    assert contexts[0].store_root == contexts[1].store_root
    assert contexts[0].checkpoint_root == contexts[1].checkpoint_root
    assert stage.output_path(first) != stage.output_path(warm)
    registry = recipe_definitions()
    for recipe_id, plan in stage.PLANS.items():
        definition = registry[recipe_id]
        assert sha256_recipe_config(stage.ROOT / plan['config']) == definition['config_sha256']
        assert definition['expected_artifact_paths'] == (stage.output_path(plan),)
        assert definition['argv'][-2:] == ('--recipe', recipe_id)


def test_unregistered_recipe_refused_before_runtime_access():
    with pytest.raises(KeyError):
        stage.preflight('arbitrary-run-id')


def test_existing_output_refuses_repeat_even_before_execution(tmp_path, monkeypatch):
    from scripts.syncmate import verify_core_dependency
    from experiments import modular_config
    recipe_id = 'opengu-sm005-b-hutch32-warm-v1'
    output = tmp_path / stage.output_path(stage.PLANS[recipe_id])
    output.parent.mkdir(parents=True)
    output.write_text('preserved evidence')
    monkeypatch.setattr(torch.cuda, 'is_available', lambda: False)
    monkeypatch.setattr(verify_core_dependency, 'verify_core_dependency', lambda: {'errors': []})
    monkeypatch.setattr(modular_config, 'load_experiment', lambda path: {})
    result = stage.preflight(recipe_id, root=tmp_path)
    assert any('output already exists' in e for e in result['errors'])
    assert output.read_text() == 'preserved evidence'
