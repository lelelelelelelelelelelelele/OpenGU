from types import SimpleNamespace
from pathlib import Path

import torch
import pytest
from torch_geometric.data import Data

from experiments.processed_provider import processed_split_contract
from experiments.target_direct_v1 import (
    DEFAULT_SPLIT_CONTRACT,
    target_direct_split_contract,
)
from experiments.target_direct_v1 import split_profile as profile_module
from experiments.target_direct_v1.split_profile import (
    apply_fixed_split,
    assert_canonical_processed_root,
    stage_profile,
    split_observation,
)
from utils.target_checkpoint import data_identity
from utils.node_split import apply_transductive_node_split


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


def test_target_direct_split_is_the_common_opengu_split():
    target_direct = _data()
    common = _data()
    apply_fixed_split(target_direct, seed=2024)
    apply_transductive_node_split(
        common,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
        split_seed=2024,
    )
    for name in (
        "train_mask",
        "val_mask",
        "test_mask",
        "train_edge_index",
        "val_edge_index",
        "test_edge_index",
    ):
        assert torch.equal(getattr(target_direct, name), getattr(common, name))
    for name in ("train_indices", "val_indices", "test_indices"):
        assert getattr(target_direct, name) == getattr(common, name)


def test_native_and_target_direct_seeded_calls_are_equivalent():
    from utils.dataset_utils import transductive_split_node

    native = _data()
    target_direct = _data()
    transductive_split_node(
        None,
        {},
        native,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
        split_seed=2024,
    )
    apply_fixed_split(target_direct, seed=2024)
    for name in (
        "train_mask",
        "val_mask",
        "test_mask",
        "train_edge_index",
        "val_edge_index",
        "test_edge_index",
    ):
        assert torch.equal(getattr(native, name), getattr(target_direct, name))
    for name in ("train_indices", "val_indices", "test_indices"):
        assert getattr(native, name) == getattr(target_direct, name)


def test_processed_root_must_be_inside_active_checkout(tmp_path):
    repository_root = tmp_path / "active" / "GULib-master"
    canonical = repository_root / "data" / "processed"
    assert assert_canonical_processed_root(repository_root, canonical) == canonical.resolve()
    with pytest.raises(RuntimeError, match="active checkout canonical root"):
        assert_canonical_processed_root(
            repository_root, tmp_path / "OpenGU-shared" / "data" / "processed"
        )


def test_split_contract_defaults_are_70_10_20_seed2024():
    contract = processed_split_contract(
        {"processed_profile": "registered-profile"},
        require_profile=True,
    )
    assert contract.to_manifest() == {
        "processed_profile": "registered-profile",
        "train_ratio": 0.7,
        "val_ratio": 0.1,
        "test_ratio": 0.2,
        "split_seed": 2024,
    }


def test_target_direct_equivalent_ratio_values_share_one_contract():
    equivalent = target_direct_split_contract(
        {
            "split": {
                "train_ratio": "0.70",
                "val_ratio": "0.10",
                "test_ratio": "0.20",
                "split_seed": "2024",
            }
        },
        require_explicit=True,
    )

    assert equivalent == DEFAULT_SPLIT_CONTRACT
    assert equivalent.processed_profile == "planetoid_70_10_20_seed2024"


def test_target_direct_requires_a_nonempty_validation_target():
    with pytest.raises(RuntimeError, match="positive validation"):
        target_direct_split_contract(
            {
                "split": {
                    "train_ratio": 0.8,
                    "val_ratio": 0,
                    "test_ratio": 0.2,
                    "split_seed": 2024,
                }
            },
            require_explicit=True,
        )


class _PersistedPlanetoid:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        if index != 0:
            raise IndexError(index)
        return self.data


class _DatasetSource:
    dataset = "Cora"
    storage_name = "Cora"

    def __init__(self, repository_root):
        raw_root = repository_root / "data" / "raw"
        dataset_root = raw_root / "cora"
        self._manifest = {
            "schema": "test.planetoid_source",
            "version": 1,
            "profile": "raw-planetoid",
            "dataset": "Cora",
            "storage_name": "Cora",
            "split_policy": "raw_source_only",
            "resolved_root": str(raw_root),
            "resolved_dataset_dir": str(dataset_root),
            "raw_dir": str(dataset_root / "raw"),
            "processed_data_path": str(dataset_root / "processed" / "data.pt"),
            "source_fingerprint": "f" * 64,
        }

    def to_manifest(self):
        return dict(self._manifest)


def test_real_processed_profile_cold_create_then_warm_hit_without_rewrite(
    tmp_path, monkeypatch
):
    repository_root = tmp_path / "GULib-master"
    processed_root = repository_root / "data" / "processed"
    source = _DatasetSource(repository_root)
    monkeypatch.setattr(profile_module, "Planetoid", _PersistedPlanetoid)
    monkeypatch.setattr(
        profile_module,
        "resolve_planetoid_public_source",
        lambda *args, **kwargs: source,
    )
    monkeypatch.setattr(
        profile_module,
        "_load_offline_planetoid",
        lambda observed: _PersistedPlanetoid(_data()),
    )

    cold = stage_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset="Cora",
        contract=DEFAULT_SPLIT_CONTRACT,
    )
    paths = tuple(
        cold[name] for name in ("data_path", "dataset_path", "manifest_path")
    )
    before = {
        path: (Path(path).read_bytes(), Path(path).stat().st_mtime_ns)
        for path in paths
    }

    warm = stage_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset="Cora",
        contract=DEFAULT_SPLIT_CONTRACT,
    )

    assert cold["status"] == "created"
    assert warm["status"] == "reused"
    assert warm["manifest"]["split_observation"] == cold["manifest"][
        "split_observation"
    ]
    assert data_identity(warm["data"]) == data_identity(cold["data"])
    for path in paths:
        payload, modified = before[path]
        assert Path(path).read_bytes() == payload
        assert Path(path).stat().st_mtime_ns == modified


def test_real_profiles_reuse_equivalent_contract_and_keep_alternates_distinct(
    tmp_path, monkeypatch
):
    repository_root = tmp_path / "GULib-master"
    processed_root = repository_root / "data" / "processed"
    source = _DatasetSource(repository_root)
    base_data = _data()
    monkeypatch.setattr(profile_module, "Planetoid", _PersistedPlanetoid)
    monkeypatch.setattr(
        profile_module,
        "resolve_planetoid_public_source",
        lambda *args, **kwargs: source,
    )
    monkeypatch.setattr(
        profile_module,
        "_load_offline_planetoid",
        lambda observed: _PersistedPlanetoid(base_data.clone()),
    )
    equivalent_default = target_direct_split_contract(
        {
            "split": {
                "train_ratio": "0.70",
                "val_ratio": "0.10",
                "test_ratio": "0.20",
                "split_seed": 2024,
            }
        },
        require_explicit=True,
    )
    alternate = target_direct_split_contract(
        {
            "split": {
                "train_ratio": 0.6,
                "val_ratio": 0.2,
                "test_ratio": 0.2,
                "split_seed": 2024,
            }
        },
        require_explicit=True,
    )

    cold_default = stage_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset="Cora",
        contract=DEFAULT_SPLIT_CONTRACT,
    )
    default_before = {
        Path(cold_default[name]): (
            Path(cold_default[name]).read_bytes(),
            Path(cold_default[name]).stat().st_mtime_ns,
        )
        for name in ("data_path", "dataset_path", "manifest_path")
    }
    warm_equivalent = stage_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset="Cora",
        contract=equivalent_default,
    )
    cold_alternate = stage_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset="Cora",
        contract=alternate,
    )

    assert warm_equivalent["status"] == "reused"
    assert cold_alternate["status"] == "created"
    assert warm_equivalent["data_path"] == cold_default["data_path"]
    assert cold_alternate["data_path"] != cold_default["data_path"]
    assert Path(cold_alternate["data_path"]).is_file()
    assert data_identity(warm_equivalent["data"])["split_hash"] == (
        data_identity(cold_default["data"])["split_hash"]
    )
    assert data_identity(cold_alternate["data"])["split_hash"] != (
        data_identity(cold_default["data"])["split_hash"]
    )
    for path, (payload, modified) in default_before.items():
        assert path.read_bytes() == payload
        assert path.stat().st_mtime_ns == modified
