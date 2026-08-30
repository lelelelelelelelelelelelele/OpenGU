"""Fail-closed Planetoid persistence helpers for target-direct profiles."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from typing import Any, Dict

import torch
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures


OPENGU_SPLIT_CONTRACT = "public-mask-indices-and-induced-edges-v1"
OPENGU_GRAPH_CONTRACT = "planetoid-graph-metadata-v1"


class OfflineCanonicalPlanetoid(Planetoid):
    """Load a verified PyG cache and forbid network or preprocessing fallback."""

    def download(self) -> None:
        raise RuntimeError(
            "canonical Planetoid raw cache is incomplete; download is forbidden"
        )

    def process(self) -> None:
        raise RuntimeError(
            "canonical Planetoid processed cache is incomplete; processing is forbidden"
        )


def _load_offline_planetoid(source):
    dataset = OfflineCanonicalPlanetoid(
        root=str(source.resolved_root),
        name=source.storage_name,
        transform=NormalizeFeatures(),
    )
    dataset.__class__ = Planetoid
    return dataset


def _opengu_split_contract(data, *, materialize: bool) -> Dict[str, Any]:
    num_nodes = int(data.num_nodes)
    edge_index = data.edge_index
    if (
        not torch.is_tensor(edge_index)
        or edge_index.dim() != 2
        or edge_index.size(0) != 2
    ):
        raise RuntimeError("target-direct profile edge_index is invalid")
    if edge_index.numel() and (
        int(edge_index.min().item()) < 0
        or int(edge_index.max().item()) >= num_nodes
    ):
        raise RuntimeError("target-direct profile edge_index exceeds num_nodes")

    observation: Dict[str, Any] = {
        "contract": OPENGU_SPLIT_CONTRACT,
        "num_nodes": num_nodes,
        "splits": {},
    }
    src, dst = edge_index[0], edge_index[1]
    for split_name in ("train", "val", "test"):
        mask_name = "{0}_mask".format(split_name)
        indices_name = "{0}_indices".format(split_name)
        edge_name = "{0}_edge_index".format(split_name)
        mask = getattr(data, mask_name, None)
        if (
            not torch.is_tensor(mask)
            or mask.dim() != 1
            or mask.numel() != num_nodes
        ):
            raise RuntimeError(
                "target-direct profile {0} must be a node mask".format(mask_name)
            )
        normalized_mask = mask.bool()
        expected_indices = normalized_mask.nonzero(as_tuple=True)[0].tolist()
        expected_edges = edge_index[
            :, normalized_mask[src] & normalized_mask[dst]
        ].clone()
        if materialize:
            setattr(data, mask_name, normalized_mask)
            setattr(data, indices_name, expected_indices)
            setattr(data, edge_name, expected_edges)
        else:
            if getattr(data, indices_name, None) != expected_indices:
                raise RuntimeError(
                    "target-direct profile {0} differs from {1}".format(
                        indices_name, mask_name
                    )
                )
            observed_edges = getattr(data, edge_name, None)
            if not torch.is_tensor(observed_edges) or not torch.equal(
                observed_edges, expected_edges
            ):
                raise RuntimeError(
                    "target-direct profile {0} is not induced by {1}".format(
                        edge_name, mask_name
                    )
                )
        observation["splits"][split_name] = {
            "node_count": len(expected_indices),
            "edge_count": int(expected_edges.size(1)),
        }
    return observation


def _opengu_graph_contract(
    data, *, dataset_name: str, materialize: bool
) -> Dict[str, Any]:
    if not torch.is_tensor(data.x) or data.x.dim() != 2:
        raise RuntimeError("target-direct profile x tensor is invalid")
    if not torch.is_tensor(data.y) or data.y.numel() != int(data.num_nodes):
        raise RuntimeError("target-direct profile y tensor is invalid")
    expected = {
        "contract": OPENGU_GRAPH_CONTRACT,
        "name": dataset_name.lower(),
        "num_nodes": int(data.num_nodes),
        "num_edges": int(data.edge_index.size(1)),
        "num_features": int(data.x.size(1)),
        "num_classes": int(data.y.max().item()) + 1,
    }
    for field in ("name", "num_edges", "num_features", "num_classes"):
        if materialize:
            setattr(data, field, expected[field])
        elif getattr(data, field, None) != expected[field]:
            raise RuntimeError(
                "target-direct profile {0} differs from graph tensors".format(field)
            )
    return expected


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def manifest_path_for(data_path: Path) -> Path:
    return data_path.with_suffix(".manifest.json")
