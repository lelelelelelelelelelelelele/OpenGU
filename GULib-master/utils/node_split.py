"""Import-safe helpers for deterministic transductive node splits.

This module deliberately has no dependency on ``config.py``.  The index
partition is the single source of truth used by both OpenGU preprocessing and
formal experiment profile materialization.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

import torch


def _validate_ratios(
    *, train_ratio: float, val_ratio: float, test_ratio: float
) -> None:
    ratios = (float(train_ratio), float(val_ratio), float(test_ratio))
    if any(not math.isfinite(ratio) or ratio < 0.0 for ratio in ratios):
        raise ValueError("node split ratios must be finite and non-negative")
    if not math.isclose(sum(ratios), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("node split ratios must sum to one")


def node_split_indices(
    num_nodes: int,
    *,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    split_seed: Optional[int] = None,
    generator: Optional[torch.Generator] = None,
) -> Dict[str, torch.Tensor]:
    """Return one disjoint and exhaustive random node partition.

    When neither ``split_seed`` nor ``generator`` is supplied, ``torch``'s
    global RNG is used.  This preserves the original OpenGU preprocessing
    behavior.  A seed creates a private CPU generator, while an explicit
    generator lets callers own and audit RNG state.
    """

    num_nodes = int(num_nodes)
    if num_nodes <= 0:
        raise ValueError("num_nodes must be positive")
    _validate_ratios(
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
    )
    if split_seed is not None and generator is not None:
        raise ValueError("provide split_seed or generator, not both")
    if generator is not None and str(generator.device) != "cpu":
        raise ValueError("node split generator must be a CPU generator")
    if split_seed is not None:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(int(split_seed))

    permutation = torch.randperm(num_nodes, generator=generator)
    train_end = int(float(train_ratio) * num_nodes)
    validation_end = int(
        (float(train_ratio) + float(val_ratio)) * num_nodes
    )
    return {
        "train": permutation[:train_end],
        "val": permutation[train_end:validation_end],
        "test": permutation[validation_end:],
    }


def apply_transductive_node_split(
    data: Any,
    *,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    split_seed: Optional[int] = None,
    generator: Optional[torch.Generator] = None,
) -> Any:
    """Materialize masks, sorted node IDs, and induced edges on ``data``."""

    partitions = node_split_indices(
        int(data.num_nodes),
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        split_seed=split_seed,
        generator=generator,
    )
    edge_index = data.edge_index
    device = edge_index.device
    for name, node_ids in partitions.items():
        mask = torch.zeros(int(data.num_nodes), dtype=torch.bool, device=device)
        mask[node_ids.to(device=device)] = True
        setattr(data, "{0}_mask".format(name), mask)
        setattr(
            data,
            "{0}_indices".format(name),
            mask.nonzero(as_tuple=True)[0].tolist(),
        )

    source, destination = edge_index[0], edge_index[1]
    for name in ("train", "val", "test"):
        mask = getattr(data, "{0}_mask".format(name))
        induced = mask[source] & mask[destination]
        setattr(data, "{0}_edge_index".format(name), edge_index[:, induced])
    return data


def observe_node_split(data: Any) -> Dict[str, Any]:
    """Validate and summarize materialized train/validation/test masks."""

    num_nodes = int(data.num_nodes)
    masks = {
        name: getattr(data, "{0}_mask".format(name)).bool()
        for name in ("train", "val", "test")
    }
    if any(mask.dim() != 1 or mask.numel() != num_nodes for mask in masks.values()):
        raise RuntimeError("node split masks have invalid shapes")
    disjoint = not bool(
        (masks["train"] & masks["val"]).any()
        or (masks["train"] & masks["test"]).any()
        or (masks["val"] & masks["test"]).any()
    )
    exhaustive = int(
        (masks["train"] | masks["val"] | masks["test"]).sum().item()
    ) == num_nodes
    observation = {
        "counts": {
            name: int(mask.sum().item()) for name, mask in masks.items()
        },
        "disjoint": disjoint,
        "exhaustive": exhaustive,
    }
    if not disjoint or not exhaustive:
        raise RuntimeError("node split masks must be disjoint and exhaustive")
    return observation
