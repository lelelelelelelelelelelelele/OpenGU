import subprocess
import sys
from pathlib import Path

import pytest
import torch
from torch_geometric.data import Data

from utils.node_split import (
    apply_transductive_node_split,
    node_split_indices,
    observe_node_split,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _data(num_nodes=101):
    node_ids = torch.arange(num_nodes, dtype=torch.long)
    return Data(
        x=torch.randn(num_nodes, 3),
        y=node_ids % 3,
        edge_index=torch.stack((node_ids, node_ids.roll(-1))),
        num_nodes=num_nodes,
    )


def _attributes_equal(first, second):
    for name in (
        "train_mask",
        "val_mask",
        "test_mask",
        "train_edge_index",
        "val_edge_index",
        "test_edge_index",
    ):
        assert torch.equal(getattr(first, name), getattr(second, name))
    for name in ("train_indices", "val_indices", "test_indices"):
        assert getattr(first, name) == getattr(second, name)


def test_node_split_module_is_import_safe_without_config_side_effects():
    script = (
        "import sys; "
        "import utils.node_split; "
        "assert 'config' not in sys.modules"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, "--unknown-opengu-argument"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_seed_and_generator_produce_the_same_deterministic_identity():
    seeded = _data()
    generated = _data()
    apply_transductive_node_split(
        seeded,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
        split_seed=2024,
    )
    generator = torch.Generator(device="cpu")
    generator.manual_seed(2024)
    apply_transductive_node_split(
        generated,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
        generator=generator,
    )

    _attributes_equal(seeded, generated)
    assert observe_node_split(seeded) == {
        "counts": {"train": 70, "val": 10, "test": 21},
        "disjoint": True,
        "exhaustive": True,
    }


def test_native_default_rng_behavior_matches_the_common_helper():
    from utils.dataset_utils import transductive_split_node

    native = _data()
    common = _data()
    torch.manual_seed(212)
    transductive_split_node(
        None,
        {},
        native,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
    )
    torch.manual_seed(212)
    apply_transductive_node_split(
        common,
        train_ratio=0.7,
        val_ratio=0.1,
        test_ratio=0.2,
    )
    _attributes_equal(native, common)


@pytest.mark.parametrize(
    "ratios",
    [
        (0.7, 0.1, 0.1),
        (0.7, -0.1, 0.4),
        (float("nan"), 0.1, 0.2),
    ],
)
def test_split_ratios_fail_closed(ratios):
    with pytest.raises(ValueError, match="ratios"):
        node_split_indices(
            101,
            train_ratio=ratios[0],
            val_ratio=ratios[1],
            test_ratio=ratios[2],
            split_seed=2024,
        )


def test_seed_and_generator_are_mutually_exclusive():
    with pytest.raises(ValueError, match="not both"):
        node_split_indices(
            101,
            train_ratio=0.7,
            val_ratio=0.1,
            test_ratio=0.2,
            split_seed=2024,
            generator=torch.Generator(device="cpu"),
        )
