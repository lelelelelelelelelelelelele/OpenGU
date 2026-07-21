"""Fail-closed preflight for the formal k=5 noise-anchor matrix."""

from __future__ import annotations

import hashlib
import json
import pickle
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

try:
    from experiments.processed_provider import require_processed_artifacts
except ModuleNotFoundError:
    _REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
    if str(_REPOSITORY_ROOT) not in sys.path:
        sys.path.insert(0, str(_REPOSITORY_ROOT))
    from experiments.processed_provider import require_processed_artifacts


PREFLIGHT_SCHEMA = "opengu.k5_noise_anchor.preflight"
PREFLIGHT_VERSION = 1
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _mask_indices(mask: Any) -> Iterable[int]:
    try:
        values = mask.nonzero(as_tuple=True)[0].detach().cpu().tolist()
        return (int(value) for value in values)
    except (AttributeError, TypeError):
        return (index for index, value in enumerate(mask) if bool(value))


def _index_fingerprint(indices: Iterable[int]) -> str:
    payload = json.dumps(
        sorted(int(index) for index in indices), separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def resolve_processed_source(
    repository_root: Path,
    *,
    dataset: str,
    train_ratio: float = 0.8,
    val_ratio: float = 0,
    test_ratio: float = 0.2,
    is_transductive: bool = True,
    is_balanced: bool = False,
) -> Dict[str, Any]:
    """Resolve and fingerprint the exact canonical OpenGU processed pair."""
    repository_root = Path(repository_root).resolve(strict=True)
    requested_root = repository_root / "data" / "processed"
    args = {
        "root_path": str(repository_root),
        "processed_root": str(requested_root),
        "dataset_name": str(dataset),
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
        "test_ratio": test_ratio,
        "is_transductive": bool(is_transductive),
        "is_balanced": bool(is_balanced),
    }
    paths = require_processed_artifacts(args)
    resolved_root = paths.root.resolve(strict=True)
    data_path = paths.data_path.resolve(strict=True)
    dataset_path = paths.dataset_path.resolve(strict=True)
    for path in (resolved_root, data_path, dataset_path):
        if not _is_within(path, repository_root):
            raise RuntimeError(
                f"canonical processed source escapes active checkout: {path}"
            )

    with data_path.open("rb") as handle:
        data = pickle.load(handle)
    num_nodes = int(data.num_nodes)
    edge_index = data.edge_index
    num_edges = int(edge_index.shape[1])
    split_indices = {
        name: tuple(_mask_indices(getattr(data, f"{name}_mask")))
        for name in ("train", "val", "test")
    }
    split_sets = {name: set(values) for name, values in split_indices.items()}
    if any(
        split_sets[left].intersection(split_sets[right])
        for left, right in (("train", "val"), ("train", "test"), ("val", "test"))
    ):
        raise RuntimeError("canonical processed split masks overlap")
    covered = set().union(*split_sets.values())
    if covered != set(range(num_nodes)):
        raise RuntimeError(
            "canonical processed split masks do not cover every node exactly once"
        )

    files = []
    for role, path in (("data", data_path), ("dataset", dataset_path)):
        files.append(
            {
                "role": role,
                "requested_path": str(
                    paths.data_path if role == "data" else paths.dataset_path
                ),
                "real_path": str(path),
                "relative_path": path.relative_to(repository_root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": _sha256_file(path),
            }
        )
    split_identity = {
        "lane": paths.lane,
        "balanced": bool(is_balanced),
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
        "test_ratio": test_ratio,
        "num_nodes": num_nodes,
        "num_edges_directed": num_edges,
        "counts": {name: len(values) for name, values in split_indices.items()},
        "index_sha256": {
            name: _index_fingerprint(values)
            for name, values in split_indices.items()
        },
    }
    fingerprint_payload = {
        "dataset": str(dataset),
        "files": [
            {
                "role": item["role"],
                "relative_path": item["relative_path"],
                "size_bytes": item["size_bytes"],
                "sha256": item["sha256"],
            }
            for item in files
        ],
        "split_identity": split_identity,
    }
    source_fingerprint = hashlib.sha256(
        json.dumps(
            fingerprint_payload,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "profile": "opengu_canonical_processed_pair",
        "dataset": str(dataset),
        "requested_root": str(requested_root),
        "resolved_root": str(resolved_root),
        "active_checkout": str(repository_root),
        "files": files,
        "split_identity": split_identity,
        "source_fingerprint": source_fingerprint,
        "automatic_download_allowed": False,
        "runtime_preprocessing_allowed": False,
    }


def collect_git_provenance(repository_root: Path) -> Dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), *args],
            text=True,
            encoding="utf-8",
        ).strip()

    status = subprocess.check_output(
        [
            "git",
            "-C",
            str(repository_root),
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        text=True,
        encoding="utf-8",
    ).rstrip("\r\n")
    return {
        "toplevel": run("rev-parse", "--show-toplevel"),
        "branch": run("branch", "--show-current"),
        "git_sha": run("rev-parse", "HEAD"),
        "dirty": bool(status),
        "status_entries": status.splitlines() if status else [],
    }


def collect_gpu_provenance() -> Dict[str, Any]:
    query = subprocess.check_output(
        [
            "nvidia-smi",
            "--query-gpu=index,name,uuid,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ],
        text=True,
        encoding="utf-8",
    ).strip()
    devices = []
    for line in query.splitlines():
        fields = [value.strip() for value in line.split(",", 4)]
        if len(fields) != 5:
            raise RuntimeError(f"unexpected nvidia-smi row: {line}")
        devices.append(
            {
                "index": int(fields[0]),
                "name": fields[1],
                "uuid": fields[2],
                "memory_total_mib": int(fields[3]),
                "driver_version": fields[4],
            }
        )
    if not devices:
        raise RuntimeError("nvidia-smi returned no GPUs")

    import torch

    cuda_available = bool(torch.cuda.is_available())
    torch_name = torch.cuda.get_device_name(0) if cuda_available else None
    return {
        "selected_index": 0,
        "devices": devices,
        "torch_cuda_available": cuda_available,
        "torch_device_name": torch_name,
    }


def build_formal_preflight(
    repository_root: Path,
    *,
    expected_git_sha: Optional[str] = None,
    dataset: str = "cora",
) -> Dict[str, Any]:
    errors = []
    try:
        git = collect_git_provenance(repository_root)
    except Exception as exc:
        git = None
        errors.append(f"git-provenance: {type(exc).__name__}: {exc}")
    if git is not None:
        if git["branch"] != "main":
            errors.append(f"git-branch: expected main, observed {git['branch']!r}")
        if not FULL_SHA_RE.fullmatch(str(git["git_sha"])):
            errors.append(f"git-sha: not a full 40-character SHA: {git['git_sha']!r}")
        if expected_git_sha is not None and git["git_sha"] != expected_git_sha:
            errors.append(
                f"git-sha: expected {expected_git_sha}, observed {git['git_sha']}"
            )
        if git["dirty"]:
            errors.append(
                "git-dirty: " + "; ".join(git["status_entries"][:20])
            )

    try:
        dataset_source = resolve_processed_source(
            repository_root, dataset=dataset
        )
    except Exception as exc:
        dataset_source = None
        errors.append(f"dataset-source: {type(exc).__name__}: {exc}")

    try:
        gpu = collect_gpu_provenance()
    except Exception as exc:
        gpu = None
        errors.append(f"gpu: {type(exc).__name__}: {exc}")
    if gpu is not None:
        gpu0 = next(
            (item for item in gpu["devices"] if item["index"] == 0), None
        )
        if gpu0 is None or "RTX 4090" not in gpu0["name"]:
            errors.append(f"gpu0: RTX 4090 required, observed {gpu0}")
        if not gpu["torch_cuda_available"]:
            errors.append("gpu0: torch.cuda.is_available() is false")
        elif "RTX 4090" not in str(gpu["torch_device_name"]):
            errors.append(
                "gpu0: torch device is not RTX 4090: "
                + str(gpu["torch_device_name"])
            )

    return {
        "schema": PREFLIGHT_SCHEMA,
        "schema_version": PREFLIGHT_VERSION,
        "ready": not errors,
        "expected_git_sha": expected_git_sha,
        "git": git,
        "gpu": gpu,
        "dataset_source": dataset_source,
        "errors": errors,
    }


__all__ = [
    "FULL_SHA_RE",
    "PREFLIGHT_SCHEMA",
    "PREFLIGHT_VERSION",
    "build_formal_preflight",
    "collect_git_provenance",
    "collect_gpu_provenance",
    "resolve_processed_source",
]
