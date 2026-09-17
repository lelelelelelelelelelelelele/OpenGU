from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn
from torch_geometric.data import Data

from experiments.c_target_v1.core import state_hash as experiment_state_hash
from utils.target_checkpoint import (
    TargetCheckpointError,
    load_weights,
    load_cached_weights,
    save_cached_weights,
    save_weights,
    state_hash,
    data_identity,
)


def _state(offset: float):
    return {
        "weight": torch.tensor([[1.0 + offset, 2.0]], dtype=torch.float32),
        "bias": torch.tensor([offset], dtype=torch.float32),
    }


def test_pure_weight_roundtrip_and_cache_provenance(tmp_path):
    path = tmp_path / 'model.pt'
    final = _state(1.)
    saved = save_cached_weights(path, final, {'seed': 42})
    assert set(torch.load(path, weights_only=True)) == set(final)
    assert saved['state_hash'] == experiment_state_hash(final)
    assert load_cached_weights(path, {'seed': 42})['state_hash'] == saved['state_hash']
    with pytest.raises(TargetCheckpointError, match='metadata'):
        load_cached_weights(path, {'seed': 43})
    torch.save(_state(2.), path)
    with pytest.raises(TargetCheckpointError, match='provenance'):
        load_cached_weights(path, {'seed': 42})


class _TwoInputModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 2)

    def forward(self, x, edge_index):
        return self.linear(x)


class _TargetTrainer:
    def __init__(self, model):
        self.model = model

    def evaluate(self):
        return 0.75


class _Logger:
    def info(self, *_args, **_kwargs):
        pass

    def warning(self, *_args, **_kwargs):
        pass


def test_gnndelete_loads_exact_target_checkpoint_without_training(tmp_path: Path):
    from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete

    data = Data(
        x=torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
        y=torch.tensor([0, 1]),
        edge_index=torch.tensor([[0, 1], [1, 0]], dtype=torch.long),
        train_mask=torch.tensor([True, False]),
        val_mask=torch.tensor([False, True]),
        test_mask=torch.tensor([False, True]),
        num_nodes=2,
    )
    source = _TwoInputModel()
    with torch.no_grad():
        source.linear.weight.fill_(2.0)
        source.linear.bias.fill_(1.0)
    state = {name: value.detach().clone() for name, value in source.state_dict().items()}
    checkpoint_path = tmp_path / "target.pt"
    manifest = save_weights(checkpoint_path, state)
    target = _TwoInputModel()
    method = object.__new__(gnndelete)
    method.args = {
        "dataset_name": "cora",
        "base_model": "GCN",
        "random_seed": 42,
        "processed_profile": "planetoid_70_10_20_seed2024",
        "num_epochs": 100,
        "gcn_num_layers": 2,
        "gcn_hidden": 64,
        "target_checkpoint_path": str(checkpoint_path),
        "formal_fail_closed": True,
    }
    method.data = data
    method.device = torch.device("cpu")
    method.target_model = _TargetTrainer(target)
    method.poison_f1 = np.zeros(1)
    method.run = 0
    method.logger = _Logger()

    method.train_original_model()

    assert state_hash(method.target_model.model.state_dict()) == manifest["state_hash"]
    assert method.poison_f1[0] == pytest.approx(0.75)
    assert method.target_checkpoint_observation["state_hash"] == manifest["state_hash"]


def test_attack_pipeline_formal_selection_validation():
    from attack.pipeline_adapter import AttackPipeline

    pipeline = object.__new__(AttackPipeline)
    pipeline.args = {"formal_fail_closed": True, "formal_expected_k": 2}
    pipeline.data = Data(
        num_nodes=4,
        train_mask=torch.tensor([True, True, True, False]),
    )
    pipeline._validate_formal_selected_nodes(torch.tensor([0, 2]))
    with pytest.raises(ValueError, match="count mismatch"):
        pipeline._validate_formal_selected_nodes(torch.tensor([0]))
    with pytest.raises(ValueError, match="unique"):
        pipeline._validate_formal_selected_nodes(torch.tensor([0, 0]))
    with pytest.raises(ValueError, match="outside the candidate"):
        pipeline._validate_formal_selected_nodes(torch.tensor([0, 3]))


def test_plain_cli_cache_identity_tracks_weights_not_path(tmp_path):
    from attack.cache_identity import target_parameters
    path = tmp_path / 'same.pt'
    save_weights(path, _state(0.))
    first = target_parameters({'target_checkpoint_path': str(path), 'num_epochs': 100, 'opt_lr': .01})
    torch.save(_state(1.), path)
    second = target_parameters({'target_checkpoint_path': str(path), 'num_epochs': 100, 'opt_lr': .01})
    assert first['checkpoint_state_hash'] != second['checkpoint_state_hash']
    assert 'num_epochs' not in first and 'opt_lr' not in first
