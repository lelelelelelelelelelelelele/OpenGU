"""Persist and verify the Planetoid public split as an OpenGU processed pair."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

from experiments.bc_target_v2.dataset_source import (
    assert_same_dataset_source,
    resolve_planetoid_public_source,
    validate_public_split,
)
from experiments.processed_provider import processed_artifact_paths
from experiments.selection_inputs import make_dataset_selection_inputs


PROFILE = "planetoid_public_fixed"
MANIFEST_SCHEMA = "gu_target_v1.processed_public_profile"
MANIFEST_VERSION = 1


class OfflineCanonicalPlanetoid(Planetoid):
    """Load an already-verified PyG cache and forbid network/preprocessing fallback."""

    def download(self) -> None:
        raise RuntimeError("canonical Planetoid raw cache is incomplete; download is forbidden")

    def process(self) -> None:
        raise RuntimeError("canonical Planetoid processed cache is incomplete; processing is forbidden")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _paths(repository_root: Path, processed_root: Path, dataset: str):
    return processed_artifact_paths(
        {
            "root_path": str(repository_root),
            "processed_root": str(processed_root),
            "processed_profile": PROFILE,
            "dataset_name": dataset.lower(),
            "train_ratio": 0.8,
            "val_ratio": 0.0,
            "test_ratio": 0.2,
            "is_transductive": True,
            "is_balanced": False,
        }
    )


def manifest_path_for(data_path: Path) -> Path:
    return data_path.with_suffix(".manifest.json")


def verify_public_profile(
    *, repository_root: Path, processed_root: Path, dataset: str
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    processed_root = Path(processed_root).resolve()
    paths = _paths(repository_root, processed_root, dataset)
    manifest_path = manifest_path_for(paths.data_path)
    for path in (paths.data_path, paths.dataset_path, manifest_path):
        if not path.is_file():
            raise RuntimeError("processed public profile is incomplete: {0}".format(path))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema") != MANIFEST_SCHEMA
        or manifest.get("version") != MANIFEST_VERSION
        or manifest.get("profile") != PROFILE
        or str(manifest.get("dataset", "")).lower() != dataset.lower()
    ):
        raise RuntimeError("processed public profile manifest identity is invalid")
    observed_hashes = {
        "data_sha256": _sha256_file(paths.data_path),
        "dataset_sha256": _sha256_file(paths.dataset_path),
    }
    for field, value in observed_hashes.items():
        if manifest.get(field) != value:
            raise RuntimeError("processed public profile {0} mismatch".format(field))

    source = resolve_planetoid_public_source(
        repository_root / "data" / "raw",
        repository_root=repository_root,
        dataset=dataset,
    )
    assert_same_dataset_source(manifest["dataset_source"], source.to_manifest())
    with paths.data_path.open("rb") as handle:
        data = pickle.load(handle)
    split = validate_public_split(data, source.dataset)
    if split != manifest.get("split_observation"):
        raise RuntimeError("processed public profile split observation changed")
    inputs = make_dataset_selection_inputs(
        data, dataset_name=dataset.lower(), source_path=paths.data_path
    )
    expected_identity = manifest.get("selection_identity") or {}
    observed_identity = {
        "dataset_fingerprint": inputs.dataset_fingerprint,
        "graph_fingerprint": inputs.graph_fingerprint,
        "candidate_set_hash": inputs.candidate_set_hash,
        "candidate_count": inputs.candidate_count,
        "num_nodes": inputs.num_nodes,
    }
    if expected_identity != observed_identity:
        raise RuntimeError("processed public profile Selection identity changed")
    return {
        "manifest": manifest,
        "manifest_path": str(manifest_path),
        "data_path": str(paths.data_path),
        "dataset_path": str(paths.dataset_path),
        "inputs": inputs,
    }


def stage_public_profile(
    *, repository_root: Path, processed_root: Path, dataset: str
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    processed_root = Path(processed_root).resolve()
    paths = _paths(repository_root, processed_root, dataset)
    manifest_path = manifest_path_for(paths.data_path)
    existing = [path.exists() for path in (paths.data_path, paths.dataset_path, manifest_path)]
    if any(existing):
        if not all(existing):
            raise RuntimeError("refusing to replace an incomplete processed public profile")
        verified = verify_public_profile(
            repository_root=repository_root,
            processed_root=processed_root,
            dataset=dataset,
        )
        return {"status": "reused", **verified}

    source = resolve_planetoid_public_source(
        repository_root / "data" / "raw",
        repository_root=repository_root,
        dataset=dataset,
    )
    pyg_dataset = OfflineCanonicalPlanetoid(
        # This PyG version expands root/name/raw. OpenGU's accepted cache leaves
        # are lowercase, so the exact binding is data/raw + storage_name.
        root=str(source.resolved_root),
        name=source.storage_name,
        transform=NormalizeFeatures(),
    )
    data = pyg_dataset[0]
    split = validate_public_split(data, source.dataset)
    inputs = make_dataset_selection_inputs(
        data, dataset_name=dataset.lower(), source_path=paths.data_path
    )
    data_payload = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    dataset_payload = pickle.dumps(pyg_dataset, protocol=pickle.HIGHEST_PROTOCOL)
    _atomic_bytes(paths.data_path, data_payload)
    _atomic_bytes(paths.dataset_path, dataset_payload)
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": MANIFEST_VERSION,
        "profile": PROFILE,
        "dataset": source.dataset,
        "lane": "transductive",
        "data_path": str(paths.data_path),
        "dataset_path": str(paths.dataset_path),
        "data_sha256": _sha256_file(paths.data_path),
        "dataset_sha256": _sha256_file(paths.dataset_path),
        "dataset_source": source.to_manifest(),
        "split_observation": split,
        "selection_identity": {
            "dataset_fingerprint": inputs.dataset_fingerprint,
            "graph_fingerprint": inputs.graph_fingerprint,
            "candidate_set_hash": inputs.candidate_set_hash,
            "candidate_count": inputs.candidate_count,
            "num_nodes": inputs.num_nodes,
        },
        "timed_run_preprocessing_allowed": False,
    }
    _atomic_bytes(
        manifest_path,
        (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    verified = verify_public_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset=dataset,
    )
    return {"status": "created", **verified}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument("--dataset", choices=("Cora", "CiteSeer", "PubMed"), required=True)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    function = verify_public_profile if args.verify_only else stage_public_profile
    result = function(
        repository_root=args.repository_root,
        processed_root=args.processed_root,
        dataset=args.dataset,
    )
    payload = {key: value for key, value in result.items() if key != "inputs"}
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        print("public profile: {0}".format(payload.get("status", "verified")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
