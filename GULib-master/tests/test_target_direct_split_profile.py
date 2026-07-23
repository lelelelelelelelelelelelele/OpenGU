import torch
import pytest
from torch_geometric.data import Data

from experiments.target_direct_v1.split_profile import (
    apply_fixed_split,
    assert_canonical_processed_root,
    split_observation,
)


def _data(num_nodes: int = 101):
    return Data(
        x=torch.randn(num_nodes, 3),
        y=torch.arange(num_nodes) % 3,
        edge_index=torch.tensor([[0, 1], [1, 2]], dtype=torch.long),
        num_nodes=num_nodes,
    )


def test_fixed_split_is_disjoint_exhaustive_and_reproducible():
    first = _data()
    second = _data()
    observation = apply_fixed_split(first, seed=2024)
    apply_fixed_split(second, seed=2024)

    assert observation["counts"] == {"train": 70, "val": 10, "test": 21}
    assert observation["disjoint"] is True
    assert observation["exhaustive"] is True
    for name in ("train_mask", "val_mask", "test_mask"):
        assert torch.equal(getattr(first, name), getattr(second, name))
    assert split_observation(first) == observation


def test_fixed_split_changes_with_seed():
    first = _data()
    second = _data()
    apply_fixed_split(first, seed=2024)
    apply_fixed_split(second, seed=212)
    assert not torch.equal(first.train_mask, second.train_mask)


def test_processed_root_must_be_inside_active_checkout(tmp_path):
    repository_root = tmp_path / "active" / "GULib-master"
    canonical = repository_root / "data" / "processed"
    assert assert_canonical_processed_root(repository_root, canonical) == canonical.resolve()
    with pytest.raises(RuntimeError, match="active checkout canonical root"):
        assert_canonical_processed_root(
            repository_root, tmp_path / "OpenGU-shared" / "data" / "processed"
        )
