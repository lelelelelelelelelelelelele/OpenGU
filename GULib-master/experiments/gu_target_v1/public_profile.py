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

import torch
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
MANIFEST_VERSION = 3
OPENGU_SPLIT_CONTRACT = "public-mask-indices-and-induced-edges-v1"
OPENGU_GRAPH_CONTRACT = "planetoid-graph-metadata-v1"


class OfflineCanonicalPlanetoid(Planetoid):
    """Load an already-verified PyG cache and forbid network/preprocessing fallback."""

    def download(self) -> None:
        raise RuntimeError("canonical Planetoid raw cache is incomplete; download is forbidden")

    def process(self) -> None:
        raise RuntimeError("canonical Planetoid processed cache is incomplete; processing is forbidden")


def _load_offline_planetoid(source):
    dataset = OfflineCanonicalPlanetoid(
        root=str(source.resolved_root),
        name=source.storage_name,
        transform=NormalizeFeatures(),
    )
    # The guard subclass must never cross a pickle/process boundary: when the
    # module is launched with `python -m`, its pickle name becomes `__main__`
    # and downstream entry points cannot import it. The instance layout is the
    # native Planetoid layout, so restore its portable upstream class first.
    dataset.__class__ = Planetoid
    return dataset


def _opengu_split_contract(data, *, materialize: bool) -> Dict[str, Any]:
    """Materialize or verify the split fields OpenGU consumes downstream.

    PyG's Planetoid object persists the public ``*_mask`` tensors, while
    OpenGU's processed-data path also requires ``*_indices`` and expects the
    split edge tensors to be present.  Keep the public masks authoritative and
    derive every OpenGU compatibility field deterministically from them.
    """

    num_nodes = int(data.num_nodes)
    edge_index = data.edge_index
    if not torch.is_tensor(edge_index) or edge_index.dim() != 2 or edge_index.size(0) != 2:
        raise RuntimeError("processed public profile edge_index is invalid")
    if edge_index.numel() and (
        int(edge_index.min().item()) < 0 or int(edge_index.max().item()) >= num_nodes
    ):
        raise RuntimeError("processed public profile edge_index exceeds num_nodes")

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
        if not torch.is_tensor(mask) or mask.dim() != 1 or mask.numel() != num_nodes:
            raise RuntimeError(
                "processed public profile {0} must be a one-dimensional node mask".format(
                    mask_name
                )
            )
        normalized_mask = mask.bool()
        expected_indices = normalized_mask.nonzero(as_tuple=True)[0].tolist()
        expected_edges = edge_index[:, normalized_mask[src] & normalized_mask[dst]].clone()

        if materialize:
            setattr(data, mask_name, normalized_mask)
            setattr(data, indices_name, expected_indices)
            setattr(data, edge_name, expected_edges)
        else:
            observed_indices = getattr(data, indices_name, None)
            if not isinstance(observed_indices, list) or observed_indices != expected_indices:
                raise RuntimeError(
                    "processed public profile {0} does not match {1}".format(
                        indices_name, mask_name
                    )
                )
            observed_edges = getattr(data, edge_name, None)
            if not torch.is_tensor(observed_edges) or not torch.equal(
                observed_edges, expected_edges
            ):
                raise RuntimeError(
                    "processed public profile {0} is not induced by {1}".format(
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
    """Materialize or verify graph metadata skipped by explicit-pair loading."""

    if not torch.is_tensor(data.x) or data.x.dim() != 2:
        raise RuntimeError("processed public profile x tensor is invalid")
    if not torch.is_tensor(data.y) or data.y.numel() != int(data.num_nodes):
        raise RuntimeError("processed public profile y tensor is invalid")
    expected = {
        "contract": OPENGU_GRAPH_CONTRACT,
        "name": dataset_name.lower(),
        "num_nodes": int(data.num_nodes),
        "num_edges": int(data.edge_index.size(1)),
        "num_features": int(data.x.size(1)),
        "num_classes": int(data.y.max().item()) + 1,
    }
    if materialize:
        for field in ("name", "num_edges", "num_features", "num_classes"):
            setattr(data, field, expected[field])
    else:
        for field in ("name", "num_edges", "num_features", "num_classes"):
            observed = getattr(data, field, None)
            if observed != expected[field]:
                raise RuntimeError(
                    "processed public profile {0} differs from graph tensors".format(
                        field
                    )
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
    with paths.dataset_path.open("rb") as handle:
        pyg_dataset = pickle.load(handle)
    if type(pyg_dataset) is not Planetoid:
        raise RuntimeError("processed public profile dataset pickle is not native Planetoid")
    observed_graph_contract = _opengu_graph_contract(
        data, dataset_name=dataset, materialize=False
    )
    if observed_graph_contract != manifest.get("opengu_graph_contract"):
        raise RuntimeError("processed public profile OpenGU graph contract changed")
    observed_contract = _opengu_split_contract(data, materialize=False)
    if observed_contract != manifest.get("opengu_processed_contract"):
        raise RuntimeError("processed public profile OpenGU split contract changed")
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
    # This PyG version expands root/name/raw. OpenGU's accepted cache leaves
    # are lowercase, so the exact binding is data/raw + storage_name.
    pyg_dataset = _load_offline_planetoid(source)
    data = pyg_dataset[0]
    split = validate_public_split(data, source.dataset)
    opengu_graph_contract = _opengu_graph_contract(
        data, dataset_name=source.storage_name, materialize=True
    )
    opengu_contract = _opengu_split_contract(data, materialize=True)
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
        "opengu_graph_contract": opengu_graph_contract,
        "opengu_processed_contract": opengu_contract,
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
