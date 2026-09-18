"""Strict pure state_dict persistence and optional cache provenance."""

from __future__ import annotations

import io
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping

import torch
from torch import Tensor




class TargetCheckpointError(RuntimeError):
    """Raised when a target checkpoint cannot satisfy its declared identity."""


def tensor_hash(tensor: Tensor) -> str:
    value = tensor.detach().cpu().contiguous()
    header = json.dumps(
        {"dtype": str(value.dtype), "shape": list(value.shape)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(
        header + value.numpy().tobytes(order="C")
    ).hexdigest()


def state_hash(state: Mapping[str, Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        value = state[name]
        if not isinstance(name, str) or not isinstance(value, Tensor):
            raise TargetCheckpointError(
                "state_dict must map string names to tensors"
            )
        name_bytes = name.encode("utf-8")
        value_bytes = bytes.fromhex(tensor_hash(value))
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(value_bytes).to_bytes(8, "big"))
        digest.update(value_bytes)
    return digest.hexdigest()


def capture_state(model: torch.nn.Module) -> Dict[str, Tensor]:
    return {
        name: value.detach().cpu().clone()
        for name, value in model.state_dict().items()
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def data_identity(data: Any) -> Dict[str, Any]:
    masks = torch.stack(
        [
            data.train_mask.detach().cpu().to(torch.uint8),
            data.val_mask.detach().cpu().to(torch.uint8),
            data.test_mask.detach().cpu().to(torch.uint8),
        ]
    )
    return {
        "num_nodes": int(data.num_nodes),
        "edge_index_hash": tensor_hash(data.edge_index),
        "features_hash": tensor_hash(data.x),
        "labels_hash": tensor_hash(data.y),
        "split_hash": tensor_hash(masks),
    }


def _normalized_state(state: Mapping[str, Tensor]) -> Dict[str, Tensor]:
    if not isinstance(state, Mapping) or not state:
        raise TargetCheckpointError("state_dict must be a non-empty mapping")
    result = {}
    for name, value in state.items():
        if not isinstance(name, str) or not isinstance(value, Tensor):
            raise TargetCheckpointError(
                "state_dict must map string names to tensors"
            )
        if not torch.isfinite(value).all():
            raise TargetCheckpointError("checkpoint contains non-finite weights: " + name)
        result[name] = value.detach().cpu().clone()
    return result


def load_weights(path, model=None):
    """Read pure weights once; identity describes the exact bytes consumed."""
    target = Path(path).expanduser().resolve()
    contents = target.read_bytes()
    state = _normalized_state(torch.load(io.BytesIO(contents), map_location='cpu', weights_only=True))
    if model is not None:
        expected = model.state_dict()
        if set(state) != set(expected):
            raise TargetCheckpointError('checkpoint keys differ from model')
        for name, value in state.items():
            if value.shape != expected[name].shape or value.dtype != expected[name].dtype:
                raise TargetCheckpointError('checkpoint shape/dtype differs from model: ' + name)
        model.load_state_dict(state, strict=True)
        model.eval()
    return {'path': str(target), 'state_dict': state,
            'file_sha256': hashlib.sha256(contents).hexdigest(), 'state_hash': state_hash(state)}


def save_weights(path, state):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never silently replace an existing trained model.
    with target.open('xb') as stream:
        torch.save(_normalized_state(state), stream)
    return load_weights(target)


def save_cached_weights(path, state, metadata):
    loaded = save_weights(path, state)
    record = {'metadata': metadata, 'file_sha256': loaded['file_sha256'], 'state_hash': loaded['state_hash']}
    with Path(path).with_suffix('.json').open('x', encoding='utf-8') as stream:
        json.dump(record, stream, sort_keys=True, allow_nan=False)
    return loaded


def load_cached_weights(path, metadata, model=None):
    record = json.loads(Path(path).with_suffix('.json').read_text(encoding='utf-8'))
    if record['metadata'] != metadata:
        raise TargetCheckpointError('cached weight metadata mismatch')
    loaded = load_weights(path, model)
    if any(record[key] != loaded[key] for key in ('file_sha256', 'state_hash')):
        raise TargetCheckpointError('cached weight contents differ from provenance')
    return loaded
