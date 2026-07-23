"""Fail-closed persistence for a target-direct pre-unlearning checkpoint."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

import torch
from torch import Tensor


SCHEMA = "opengu.target_direct_checkpoint"
VERSION = 1


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
        result[name] = value.detach().cpu().clone()
    return result


def build_payload(
    *,
    state_dict: Mapping[str, Tensor],
    metadata: Mapping[str, Any],
    checkpoints: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    final_state = _normalized_state(state_dict)
    normalized_checkpoints = []
    previous_step = None
    for item in checkpoints:
        step = int(item["global_step"])
        if step <= 0 or (previous_step is not None and step <= previous_step):
            raise TargetCheckpointError(
                "checkpoint global steps must be positive and increasing"
            )
        state = _normalized_state(item["state"])
        observed_hash = state_hash(state)
        declared_hash = item.get("state_hash")
        if declared_hash not in (None, observed_hash):
            raise TargetCheckpointError(
                "checkpoint state hash differs from its tensors"
            )
        normalized_checkpoints.append(
            {
                "global_step": step,
                "update_lr": float(item["update_lr"]),
                "state_hash": observed_hash,
                "state": state,
            }
        )
        previous_step = step
    if not normalized_checkpoints:
        raise TargetCheckpointError("at least one trajectory checkpoint is required")
    final_hash = state_hash(final_state)
    if normalized_checkpoints[-1]["state_hash"] != final_hash:
        raise TargetCheckpointError(
            "final trajectory checkpoint differs from target state"
        )
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "state_hash": final_hash,
        "state_dict": final_state,
        "metadata": dict(metadata),
        "checkpoints": normalized_checkpoints,
    }


def save_target_checkpoint(
    path: Path,
    *,
    state_dict: Mapping[str, Tensor],
    metadata: Mapping[str, Any],
    checkpoints: Sequence[Mapping[str, Any]],
    overwrite: bool = False,
) -> Dict[str, Any]:
    target = Path(path).expanduser().resolve()
    if target.exists() and not overwrite:
        raise FileExistsError("target checkpoint already exists: {0}".format(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = build_payload(
        state_dict=state_dict,
        metadata=metadata,
        checkpoints=checkpoints,
    )
    temporary = target.with_name(target.name + ".tmp-{0}".format(os.getpid()))
    try:
        torch.save(payload, temporary)
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()
    return {
        "path": str(target),
        "file_sha256": sha256_file(target),
        "state_hash": payload["state_hash"],
        "checkpoint_count": len(payload["checkpoints"]),
        "metadata": dict(payload["metadata"]),
    }


def _torch_load(path: Path, map_location: Any) -> Any:
    try:
        return torch.load(path, map_location=map_location, weights_only=True)
    except TypeError:  # PyTorch versions before weights_only support.
        return torch.load(path, map_location=map_location)


def load_target_checkpoint(
    path: Path,
    *,
    expected_file_sha256: Optional[str] = None,
    expected_state_hash: Optional[str] = None,
    expected_metadata: Optional[Mapping[str, Any]] = None,
    map_location: Any = "cpu",
) -> Dict[str, Any]:
    target = Path(path).expanduser().resolve()
    if not target.is_file():
        raise TargetCheckpointError(
            "target checkpoint is missing: {0}".format(target)
        )
    observed_file_hash = sha256_file(target)
    if (
        expected_file_sha256 is not None
        and observed_file_hash != str(expected_file_sha256)
    ):
        raise TargetCheckpointError("target checkpoint file SHA-256 mismatch")
    payload = _torch_load(target, map_location)
    if not isinstance(payload, dict):
        raise TargetCheckpointError("target checkpoint payload must be a mapping")
    if payload.get("schema") != SCHEMA or payload.get("version") != VERSION:
        raise TargetCheckpointError("target checkpoint schema/version mismatch")
    state = _normalized_state(payload.get("state_dict"))
    observed_state_hash = state_hash(state)
    if payload.get("state_hash") != observed_state_hash:
        raise TargetCheckpointError("target checkpoint state hash is corrupt")
    if expected_state_hash is not None and observed_state_hash != str(
        expected_state_hash
    ):
        raise TargetCheckpointError("target checkpoint state identity mismatch")
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise TargetCheckpointError("target checkpoint metadata must be a mapping")
    for name, expected in dict(expected_metadata or {}).items():
        if metadata.get(name) != expected:
            raise TargetCheckpointError(
                "target checkpoint metadata {0} mismatch".format(name)
            )
    checkpoints = payload.get("checkpoints")
    if not isinstance(checkpoints, list) or not checkpoints:
        raise TargetCheckpointError("target checkpoint trajectory is empty")
    previous_step = None
    for item in checkpoints:
        if not isinstance(item, dict):
            raise TargetCheckpointError("trajectory checkpoint must be a mapping")
        step = int(item.get("global_step", -1))
        if step <= 0 or (previous_step is not None and step <= previous_step):
            raise TargetCheckpointError("trajectory checkpoint steps are invalid")
        checkpoint_state = _normalized_state(item.get("state"))
        if item.get("state_hash") != state_hash(checkpoint_state):
            raise TargetCheckpointError("trajectory checkpoint state hash is corrupt")
        item["state"] = checkpoint_state
        previous_step = step
    if checkpoints[-1].get("state_hash") != observed_state_hash:
        raise TargetCheckpointError(
            "final trajectory checkpoint differs from target state"
        )
    payload["state_dict"] = state
    payload["file_sha256"] = observed_file_hash
    payload["path"] = str(target)
    return payload
