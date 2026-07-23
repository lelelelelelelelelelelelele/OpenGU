from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn
from torch_geometric.data import Data

from experiments.c_target_v1.core import state_hash as experiment_state_hash
from utils.target_checkpoint import (
    TargetCheckpointError,
    build_payload,
    load_target_checkpoint,
    save_target_checkpoint,
    state_hash,
    data_identity,
)


def _state(offset: float):
    return {
        "weight": torch.tensor([[1.0 + offset, 2.0]], dtype=torch.float32),
        "bias": torch.tensor([offset], dtype=torch.float32),
    }


def test_target_checkpoint_round_trip_and_hash_compatibility(tmp_path: Path):
    first = _state(0.0)
    final = _state(1.0)
    path = tmp_path / "target.pt"
    manifest = save_target_checkpoint(
        path,
        state_dict=final,
        metadata={"dataset_name": "cora", "seed": 42},
        checkpoints=(
            {"global_step": 1, "update_lr": 0.01, "state": first},
            {"global_step": 2, "update_lr": 0.01, "state": final},
        ),
    )

    assert manifest["state_hash"] == state_hash(final)
    assert manifest["state_hash"] == experiment_state_hash(final)
    loaded = load_target_checkpoint(
        path,
        expected_file_sha256=manifest["file_sha256"],
        expected_state_hash=manifest["state_hash"],
        expected_metadata={"dataset_name": "cora", "seed": 42},
    )
    assert loaded["state_hash"] == manifest["state_hash"]
    assert len(loaded["checkpoints"]) == 2


def test_target_checkpoint_rejects_wrong_identity(tmp_path: Path):
    path = tmp_path / "target.pt"
    manifest = save_target_checkpoint(
        path,
        state_dict=_state(1.0),
        metadata={"dataset_name": "cora"},
        checkpoints=(
            {"global_step": 1, "update_lr": 0.01, "state": _state(1.0)},
        ),
    )
    with pytest.raises(TargetCheckpointError, match="file SHA-256"):
        load_target_checkpoint(path, expected_file_sha256="0" * 64)
    with pytest.raises(TargetCheckpointError, match="state identity"):
        load_target_checkpoint(path, expected_state_hash="0" * 64)
    with pytest.raises(TargetCheckpointError, match="dataset_name mismatch"):
        load_target_checkpoint(
            path, expected_metadata={"dataset_name": "citeseer"}
        )
    assert manifest["checkpoint_count"] == 1


def test_target_checkpoint_rejects_final_trajectory_mismatch():
    with pytest.raises(TargetCheckpointError, match="final trajectory"):
        build_payload(
            state_dict=_state(2.0),
            metadata={},
            checkpoints=(
                {"global_step": 1, "update_lr": 0.01, "state": _state(1.0)},
            ),
        )


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
    manifest = save_target_checkpoint(
        checkpoint_path,
        state_dict=state,
        metadata={
            "dataset_name": "cora",
            "base_model": "GCN",
            "seed": 42,
            "processed_profile": "planetoid_70_10_20_seed2024",
            "num_epochs": 100,
            "gcn_num_layers": 2,
            "gcn_hidden": 64,
            "data_identity": data_identity(data),
        },
        checkpoints=(
            {"global_step": 100, "update_lr": 0.01, "state": state},
        ),
    )
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
        "target_checkpoint_sha256": manifest["file_sha256"],
        "target_checkpoint_state_hash": manifest["state_hash"],
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
