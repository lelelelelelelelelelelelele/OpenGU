"""Fail-closed source identity for repository-local Planetoid datasets."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple, Union


DATASET_SOURCE_SCHEMA = "bc_target_v2.planetoid_public_source"
DATASET_SOURCE_VERSION = 1
DATASET_ADAPTER = "torch_geometric.datasets.Planetoid"
PATH_CONTRACT = "opengu-repository-data-raw-v1"
SUPPORTED_DATASETS = ("Cora", "CiteSeer", "PubMed")
PUBLIC_SPLIT_COUNTS: Mapping[str, Tuple[int, int, int, int, int]] = {
    "Cora": (2708, 10556, 140, 500, 1000),
    "CiteSeer": (3327, 9104, 120, 500, 1000),
    "PubMed": (19717, 88648, 60, 500, 1000),
}
_RAW_SUFFIXES = (
    "x",
    "tx",
    "allx",
    "y",
    "ty",
    "ally",
    "graph",
    "test.index",
)


class DatasetSourceError(RuntimeError):
    """Raised when the dataset location or persisted split violates the contract."""


def canonical_data_root(repository_root: Union[str, Path]) -> Path:
    return (
        Path(repository_root).expanduser().resolve(strict=False) / "data" / "raw"
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_fingerprint(
    dataset: str,
    raw_files: Tuple[Mapping[str, Any], ...],
    processed_data: Mapping[str, Any],
) -> str:
    value = {
        "dataset": dataset,
        "raw_files": list(raw_files),
        "processed_data": dict(processed_data),
    }
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class PlanetoidPublicSource:
    dataset: str
    storage_name: str
    requested_root: str
    requested_root_absolute: Path
    resolved_root: Path
    canonical_root: Path
    dataset_dir: Path
    resolved_dataset_dir: Path
    raw_dir: Path
    processed_dir: Path
    processed_data_path: Path
    raw_files: Tuple[Mapping[str, Any], ...]
    processed_data: Mapping[str, Any]
    source_fingerprint: str

    @property
    def canonical_root_match(self) -> bool:
        return self.resolved_root == self.canonical_root

    def to_manifest(self) -> Dict[str, Any]:
        return {
            "schema": DATASET_SOURCE_SCHEMA,
            "version": DATASET_SOURCE_VERSION,
            "profile": "planetoid_public_fixed_split",
            "adapter": DATASET_ADAPTER,
            "path_contract": PATH_CONTRACT,
            "dataset": self.dataset,
            "storage_name": self.storage_name,
            "split_policy": "public",
            "feature_transform": "torch_geometric.transforms.NormalizeFeatures",
            "automatic_download_allowed": False,
            "runtime_processing_allowed": False,
            "requested_root": self.requested_root,
            "requested_root_absolute": str(self.requested_root_absolute),
            "resolved_root": str(self.resolved_root),
            "canonical_root": str(self.canonical_root),
            "canonical_root_match": self.canonical_root_match,
            "dataset_dir": str(self.dataset_dir),
            "resolved_dataset_dir": str(self.resolved_dataset_dir),
            "raw_dir": str(self.raw_dir),
            "processed_dir": str(self.processed_dir),
            "processed_data_path": str(self.processed_data_path),
            "raw_files": [dict(item) for item in self.raw_files],
            "processed_data": dict(self.processed_data),
            "source_fingerprint": self.source_fingerprint,
        }


def resolve_planetoid_public_source(
    data_root: Union[str, Path],
    *,
    repository_root: Union[str, Path],
    dataset: str,
    allow_noncanonical_root: bool = False,
) -> PlanetoidPublicSource:
    """Resolve and fingerprint an already-materialized public Planetoid cache."""

    if dataset not in SUPPORTED_DATASETS:
        raise DatasetSourceError("unsupported Planetoid dataset: {0}".format(dataset))
    supplied = Path(data_root).expanduser()
    supplied_absolute = supplied if supplied.is_absolute() else Path.cwd() / supplied
    supplied_absolute = supplied_absolute.resolve(strict=False)
    if not supplied_absolute.is_dir():
        raise DatasetSourceError(
            "dataset root does not exist or is not a directory: {0}".format(
                supplied_absolute
            )
        )
    resolved_root = supplied_absolute.resolve(strict=True)
    expected_root = canonical_data_root(repository_root).resolve(strict=False)
    if not allow_noncanonical_root and resolved_root != expected_root:
        raise DatasetSourceError(
            "non-canonical data root is forbidden: observed {0}; expected {1}. "
            "Use --allow-noncanonical-data-root only for explicitly labeled "
            "diagnostic reruns.".format(resolved_root, expected_root)
        )

    storage_name = dataset.lower()
    dataset_dir = resolved_root / storage_name
    raw_dir = dataset_dir / "raw"
    processed_dir = dataset_dir / "processed"
    processed_data_path = processed_dir / "data.pt"
    required_raw = tuple(
        raw_dir / "ind.{0}.{1}".format(storage_name, suffix)
        for suffix in _RAW_SUFFIXES
    )
    missing = [path for path in required_raw if not path.is_file()]
    if missing:
        raise DatasetSourceError(
            "complete existing Planetoid raw cache is required; automatic download "
            "is disabled; missing: {0}".format(", ".join(str(path) for path in missing))
        )
    if not processed_data_path.is_file():
        raise DatasetSourceError(
            "existing Planetoid processed/data.pt is required; runtime processing is "
            "disabled: {0}".format(processed_data_path)
        )

    raw_files = tuple(
        {
            "relative_path": path.relative_to(dataset_dir).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
        }
        for path in required_raw
    )
    processed_data = {
        "relative_path": processed_data_path.relative_to(dataset_dir).as_posix(),
        "size_bytes": processed_data_path.stat().st_size,
        "sha256": _sha256_file(processed_data_path),
    }
    return PlanetoidPublicSource(
        dataset=dataset,
        storage_name=storage_name,
        requested_root=str(data_root),
        requested_root_absolute=supplied_absolute,
        resolved_root=resolved_root,
        canonical_root=expected_root,
        dataset_dir=dataset_dir,
        resolved_dataset_dir=dataset_dir.resolve(strict=True),
        raw_dir=raw_dir.resolve(strict=True),
        processed_dir=processed_dir.resolve(strict=True),
        processed_data_path=processed_data_path.resolve(strict=True),
        raw_files=raw_files,
        processed_data=processed_data,
        source_fingerprint=_source_fingerprint(dataset, raw_files, processed_data),
    )


def validate_public_split(data: Any, dataset: str) -> Dict[str, int]:
    """Reject a canonical OpenGU 80/20 pickle or any other unexpected split."""

    if dataset not in PUBLIC_SPLIT_COUNTS:
        raise DatasetSourceError("unsupported Planetoid dataset: {0}".format(dataset))
    observed = {
        "num_nodes": int(data.num_nodes),
        "num_edges_directed": int(data.edge_index.shape[1]),
        "train_count": int(data.train_mask.sum().item()),
        "validation_count": int(data.val_mask.sum().item()),
        "test_count": int(data.test_mask.sum().item()),
    }
    expected_values = PUBLIC_SPLIT_COUNTS[dataset]
    expected = dict(zip(observed, expected_values))
    if observed != expected:
        raise DatasetSourceError(
            "persisted Planetoid graph does not match the frozen public split for "
            "{0}; observed {1}, expected {2}".format(dataset, observed, expected)
        )
    return observed


def assert_same_dataset_source(
    expected: Mapping[str, Any], observed: Mapping[str, Any]
) -> None:
    """Require downstream/cold/warm reads to consume the exact same source."""

    identity_fields = (
        "schema",
        "version",
        "profile",
        "dataset",
        "storage_name",
        "split_policy",
        "resolved_root",
        "resolved_dataset_dir",
        "raw_dir",
        "processed_data_path",
        "source_fingerprint",
    )
    mismatches = {
        name: {"expected": expected.get(name), "observed": observed.get(name)}
        for name in identity_fields
        if expected.get(name) != observed.get(name)
    }
    if mismatches:
        raise DatasetSourceError(
            "dataset source changed between experiment stages: {0}".format(mismatches)
        )


__all__ = [
    "DATASET_SOURCE_SCHEMA",
    "DATASET_SOURCE_VERSION",
    "DatasetSourceError",
    "PATH_CONTRACT",
    "PUBLIC_SPLIT_COUNTS",
    "PlanetoidPublicSource",
    "SUPPORTED_DATASETS",
    "assert_same_dataset_source",
    "canonical_data_root",
    "resolve_planetoid_public_source",
    "validate_public_split",
]
