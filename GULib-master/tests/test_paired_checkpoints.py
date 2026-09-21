"""Small disposable training/export roundtrip, not formal experiment evidence."""
import copy
import json
from pathlib import Path
import torch
import pytest
from test_modular_consumers import tables, write_yaml
from experiments.train_checkpoints import load_plan, train_matrix
from experiments.modular_run import read_dataset
from experiments.modular_execution import project_context


@pytest.mark.parametrize('corrupt_export', [False, True])
def test_paired_export_cold_warm_and_strict_roundtrip(tables, monkeypatch, corrupt_export):
    root = tables[0]
    path = root / 'paired.yaml'
    write_yaml(path, {'kind': 'checkpoint_training', 'schema_version': 1, 'experiment_id': 'paired',
        'dataset_ref': './dataset.yaml', 'models': [{'hidden_channels': 4}], 'seeds': [42, 43],
        'groups': {'old': {'epochs': 2, 'lr': .005}, 'new': {'epochs': 3, 'lr': .05}}})
    plan = load_plan(path)
    data, _ = read_dataset(plan['dataset'], plan['dataset_directory'])
    def execute(run_id):
        context = project_context('paired', run_id=run_id, request_device='cpu', level='verification', repository_root=root)
        return train_matrix(plan, data, context)
    if corrupt_export:
        from utils import target_checkpoint
        save = target_checkpoint.save_weights
        def corrupt(path, state):
            if Path(path).name.startswith('0-old-'):
                state = {key: value + 1 for key, value in state.items()}
            return save(path, state)
        monkeypatch.setattr(target_checkpoint, 'save_weights', corrupt)
        with pytest.raises(ValueError, match='export changed'):
            execute('corrupt')
        return
    cold, warm = execute('cold'), execute('warm')
    assert cold['status'] == warm['status'] == 'completed'
    assert len(cold['cells']) == 4
    for a, b in zip(cold['cells'], warm['cells']):
        assert a['output']['state_hash'] == b['output']['state_hash']
        assert not a['preparation']['hit'] and b['preparation']['hit']
        assert a['logits_max_abs_error'] == 0
        assert a['roundtrip_device'] == 'cpu'
        assert all(isinstance(v, torch.Tensor) for v in torch.load(a['output']['path'], weights_only=True).values())
    with pytest.raises(FileExistsError):
        execute('cold')
