from pathlib import Path
import torch

from experiments import syncmate_atomic_stage as stage
from experiments.modular_run import execute


def test_registered_atomic_plan_expands_exactly_one_cell():
    plan = execute(stage.ROOT / stage.CONFIG, dry_run=True)
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
    result = stage.preflight()
    assert not result['ready']
    assert any('no CPU fallback' in e for e in result['errors'])
    assert any('canonical SSH' in e for e in result['errors'])
