"""OpenGU-owned normalized inputs for Selection producers.

This module reads only OpenGU's canonical ``data/processed`` pickle.  It never
downloads a dataset and never constructs a split: candidate nodes come from the
persisted ``train_mask``/``train_indices`` on the processed graph.
"""

from __future__ import annotations

import hashlib
import json
import math
import operator
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence, Tuple, Union

import numpy as np
import torch

from cache_v2.canonical import sha256_bytes
from cache_v2.contracts import validate_sha256
from cache_v2.errors import ContractValidationError


DATASET_FINGERPRINT_VERSION = 1
GRAPH_FINGERPRINT_VERSION = 1
NODE_ID_SPACE = "pyg-global-node-index-v1"


def _plain_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_candidate_nodes(
    nodes: Iterable[int], num_nodes: int
) -> Tuple[int, ...]:
    if isinstance(num_nodes, bool) or not isinstance(num_nodes, int) or num_nodes < 0:
        raise ContractValidationError("num_nodes must be a non-negative integer")
    values = []
    for position, node in enumerate(nodes):
        if isinstance(node, bool):
            raise ContractValidationError(
                "candidate node at position {0} must be an integer".format(position)
            )
        try:
            integer = operator.index(node)
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "candidate node at position {0} must be an integer".format(position)
            )
        if integer < 0 or integer >= num_nodes:
            raise ContractValidationError(
                "candidate node {0} is outside [0, {1})".format(integer, num_nodes)
            )
        values.append(int(integer))
    if len(values) != len(set(values)):
        raise ContractValidationError("candidate nodes contain duplicates")
    return tuple(sorted(values))


def canonical_edge_index(edge_index: Any, num_nodes: int) -> torch.Tensor:
    tensor = torch.as_tensor(edge_index, dtype=torch.long).detach().cpu()
    if tensor.ndim != 2 or tensor.shape[0] != 2:
        raise ContractValidationError("edge_index must have shape [2, E]")
    if tensor.numel() == 0:
        return tensor.reshape(2, 0).contiguous()
    if bool((tensor < 0).any()) or bool((tensor >= num_nodes).any()):
        raise ContractValidationError("edge_index contains a node outside graph bounds")
    pairs = tensor.t().numpy().astype(np.int64, copy=False)
    order = np.lexsort((pairs[:, 1], pairs[:, 0]))
    pairs = pairs[order]
    keep = np.ones(pairs.shape[0], dtype=np.bool_)
    if pairs.shape[0] > 1:
        keep[1:] = np.any(pairs[1:] != pairs[:-1], axis=1)
    canonical = np.ascontiguousarray(pairs[keep], dtype=np.int64)
    return torch.from_numpy(canonical.T.copy()).long().contiguous()


def graph_fingerprint(edge_index: Any, num_nodes: int) -> str:
    canonical = canonical_edge_index(edge_index, num_nodes)
    edges = canonical.numpy().astype("<i8", copy=False)
    digest = hashlib.sha256()
    digest.update(b"cache-v2-graph\x00")
    digest.update(np.asarray([GRAPH_FINGERPRINT_VERSION], dtype="<i8").tobytes())
    digest.update(np.asarray([num_nodes, edges.shape[1]], dtype="<i8").tobytes())
    digest.update(edges.tobytes(order="C"))
    return digest.hexdigest()


def candidate_fingerprint(candidate_nodes: Sequence[int], num_nodes: int) -> str:
    candidates = canonical_candidate_nodes(candidate_nodes, num_nodes)
    return sha256_bytes(_plain_json_bytes(list(candidates)))


def legacy_graph_fingerprint(
    edge_index: Any, num_nodes: int, candidate_nodes: Sequence[int]
) -> str:
    edges = torch.as_tensor(edge_index, dtype=torch.long).detach().cpu().numpy()
    candidates = np.asarray(candidate_nodes, dtype=np.int64)
    digest = hashlib.sha256()
    digest.update(np.int64(num_nodes).tobytes())
    digest.update(edges.astype(np.int64, copy=False).tobytes())
    digest.update(candidates.tobytes())
    return digest.hexdigest()[:32]


def _update_tensor(digest: "hashlib._Hash", label: bytes, value: Any) -> None:
    digest.update(label + b"\x00")
    if value is None:
        digest.update(b"none\x00")
        return
    tensor = torch.as_tensor(value).detach().cpu().contiguous()
    array = tensor.numpy()
    digest.update(str(tensor.dtype).encode("ascii") + b"\x00")
    digest.update(_plain_json_bytes(list(tensor.shape)) + b"\x00")
    digest.update(array.tobytes(order="C"))


def dataset_fingerprint(data: Any, dataset_name: str, num_nodes: int) -> str:
    name = str(dataset_name).strip()
    if not name or "\x00" in name:
        raise ContractValidationError("dataset_name must be a non-empty string")
    digest = hashlib.sha256()
    digest.update(b"opengu-processed-dataset\x00")
    digest.update(
        np.asarray([DATASET_FINGERPRINT_VERSION, num_nodes], dtype="<i8").tobytes()
    )
    digest.update(name.encode("utf-8") + b"\x00")
    _update_tensor(digest, b"edge_index", getattr(data, "edge_index", None))
    _update_tensor(digest, b"x", getattr(data, "x", None))
    _update_tensor(digest, b"y", getattr(data, "y", None))
    return digest.hexdigest()


def _persisted_candidates(data: Any, num_nodes: int) -> Tuple[int, ...]:
    mask = getattr(data, "train_mask", None)
    if mask is not None:
        tensor = torch.as_tensor(mask).detach().cpu()
        if tensor.ndim > 1:
            tensor = tensor.squeeze(-1)
        if tensor.ndim != 1 or int(tensor.numel()) != num_nodes:
            raise ContractValidationError(
                "processed train_mask must be one-dimensional and match num_nodes"
            )
        return canonical_candidate_nodes(
            tensor.to(dtype=torch.bool).nonzero(as_tuple=False).view(-1).tolist(),
            num_nodes,
        )
    indices = getattr(data, "train_indices", None)
    if indices is None:
        raise ContractValidationError(
            "processed graph has no persisted train_mask or train_indices; "
            "Selection must not reconstruct the split"
        )
    return canonical_candidate_nodes(torch.as_tensor(indices).view(-1).tolist(), num_nodes)


@dataclass(frozen=True)
class DatasetSelectionInputs:
    dataset_name: str
    edge_index: torch.Tensor
    num_nodes: int
    candidate_nodes: Tuple[int, ...]
    dataset_fingerprint: str
    graph_fingerprint: str
    candidate_set_hash: str
    legacy_graph_fingerprint: str
    source_path: Optional[Path] = None
    node_id_space: str = NODE_ID_SPACE

    def __post_init__(self) -> None:
        if not self.dataset_name or "\x00" in self.dataset_name:
            raise ContractValidationError("dataset_name must be a non-empty string")
        canonical_edges = canonical_edge_index(self.edge_index, self.num_nodes)
        candidates = canonical_candidate_nodes(self.candidate_nodes, self.num_nodes)
        if not candidates:
            raise ContractValidationError("persisted candidate set is empty")
        for name in (
            "dataset_fingerprint",
            "graph_fingerprint",
            "candidate_set_hash",
        ):
            object.__setattr__(self, name, validate_sha256(getattr(self, name), name))
        source = self.source_path
        if source is not None:
            source = Path(source).resolve(strict=False)
        object.__setattr__(self, "edge_index", canonical_edges)
        object.__setattr__(self, "candidate_nodes", candidates)
        object.__setattr__(self, "source_path", source)

    @property
    def candidate_count(self) -> int:
        return len(self.candidate_nodes)


def make_dataset_selection_inputs(
    data: Any,
    *,
    dataset_name: str,
    source_path: Optional[Union[str, Path]] = None,
) -> DatasetSelectionInputs:
    if not hasattr(data, "edge_index"):
        raise ContractValidationError("processed graph has no edge_index")
    try:
        num_nodes = int(data.num_nodes)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ContractValidationError("processed graph has invalid num_nodes") from exc
    candidates = _persisted_candidates(data, num_nodes)
    canonical_edges = canonical_edge_index(data.edge_index, num_nodes)
    return DatasetSelectionInputs(
        dataset_name=str(dataset_name),
        edge_index=canonical_edges,
        num_nodes=num_nodes,
        candidate_nodes=candidates,
        dataset_fingerprint=dataset_fingerprint(data, str(dataset_name), num_nodes),
        graph_fingerprint=graph_fingerprint(canonical_edges, num_nodes),
        candidate_set_hash=candidate_fingerprint(candidates, num_nodes),
        legacy_graph_fingerprint=legacy_graph_fingerprint(
            data.edge_index, num_nodes, candidates
        ),
        source_path=Path(source_path) if source_path is not None else None,
    )


def _ratio_token(value: float) -> str:
    number = float(value)
    if not math.isfinite(number) or number < 0.0 or number > 1.0:
        raise ContractValidationError("split ratios must be finite and in [0, 1]")
    return str(int(number)) if number.is_integer() else format(number, ".15g")


def processed_data_path(
    processed_root: Union[str, Path],
    *,
    dataset_name: str,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    is_transductive: bool,
    is_balanced: bool,
) -> Path:
    if not math.isclose(
        float(train_ratio) + float(val_ratio) + float(test_ratio),
        1.0,
        abs_tol=1e-9,
    ):
        raise ContractValidationError("train/val/test ratios must sum to 1")
    split = "_".join(
        _ratio_token(value) for value in (train_ratio, val_ratio, test_ratio)
    )
    suffix = "_balanced" if is_balanced else ""
    lane = "transductive" if is_transductive else "inductive"
    return (
        Path(processed_root).expanduser().resolve(strict=False)
        / lane
        / ("{0}{1}{2}.pkl".format(dataset_name, split, suffix))
    )


def load_processed_selection_inputs(
    *,
    processed_root: Union[str, Path],
    dataset_name: str,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    is_transductive: bool,
    is_balanced: bool,
) -> DatasetSelectionInputs:
    path = processed_data_path(
        processed_root,
        dataset_name=dataset_name,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        is_transductive=is_transductive,
        is_balanced=is_balanced,
    )
    if not path.is_file():
        raise FileNotFoundError(
            "canonical OpenGU processed graph is missing: {0}; run the OpenGU "
            "dataset/experiment preprocessing flow first".format(path)
        )
    with path.open("rb") as handle:
        data = pickle.load(handle)
    return make_dataset_selection_inputs(
        data,
        dataset_name=dataset_name,
        source_path=path,
    )


__all__ = [
    "DATASET_FINGERPRINT_VERSION",
    "GRAPH_FINGERPRINT_VERSION",
    "NODE_ID_SPACE",
    "DatasetSelectionInputs",
    "candidate_fingerprint",
    "canonical_candidate_nodes",
    "canonical_edge_index",
    "dataset_fingerprint",
    "graph_fingerprint",
    "legacy_graph_fingerprint",
    "load_processed_selection_inputs",
    "make_dataset_selection_inputs",
    "processed_data_path",
]
