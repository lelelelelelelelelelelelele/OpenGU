"""Stage and verify one registered Planetoid OpenGU split profile."""

from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path
from typing import Any, Dict, Sequence

from torch_geometric.datasets import Planetoid

from experiments.bc_target_v2.dataset_source import (
    assert_same_dataset_source,
    resolve_planetoid_public_source,
)
from experiments.gu_target_v1.public_profile import (
    _atomic_bytes,
    _load_offline_planetoid,
    _opengu_graph_contract,
    _opengu_split_contract,
    _sha256_file,
    manifest_path_for,
)
from experiments.processed_provider import (
    ProcessedSplitContract,
    processed_artifact_paths,
)
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1 import (
    DEFAULT_SPLIT_CONTRACT,
    target_direct_split_contract,
)
from utils.node_split import apply_transductive_node_split, observe_node_split


MANIFEST_SCHEMA = "target_direct_v1.processed_split_profile"
MANIFEST_VERSION = 2
SPLIT_POLICY = "seeded-randperm-disjoint-v1"


def assert_canonical_processed_root(
    repository_root: Path, processed_root: Path
) -> Path:
    repository_root = Path(repository_root).expanduser().resolve()
    observed = Path(processed_root).expanduser().resolve()
    expected = (repository_root / "data" / "processed").resolve()
    if observed != expected:
        raise RuntimeError(
            "target-direct processed_root must be the active checkout canonical "
            "root: {0}".format(expected)
        )
    return observed


def _paths(
    repository_root: Path,
    processed_root: Path,
    dataset: str,
    contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
):
    return processed_artifact_paths(
        {
            "root_path": str(repository_root),
            "processed_root": str(processed_root),
            "processed_profile": contract.processed_profile,
            "dataset_name": dataset.lower(),
            "train_ratio": contract.train_ratio,
            "val_ratio": contract.val_ratio,
            "test_ratio": contract.test_ratio,
            "is_transductive": True,
            "is_balanced": False,
        }
    )


def apply_fixed_split(
    data,
    seed: int | None = None,
    *,
    contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
) -> Dict[str, Any]:
    split_seed = contract.split_seed if seed is None else int(seed)
    apply_transductive_node_split(
        data,
        train_ratio=contract.train_ratio,
        val_ratio=contract.val_ratio,
        test_ratio=contract.test_ratio,
        split_seed=split_seed,
    )
    return split_observation(data, seed=split_seed, contract=contract)


def split_observation(
    data,
    seed: int | None = None,
    *,
    contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
) -> Dict[str, Any]:
    split_seed = contract.split_seed if seed is None else int(seed)
    observed = observe_node_split(data)
    result = {
        "policy": SPLIT_POLICY,
        "seed": split_seed,
        "ratios": {
            "train": contract.train_ratio,
            "validation": contract.val_ratio,
            "test": contract.test_ratio,
        },
        **observed,
    }
    if result["counts"]["val"] <= 0:
        raise RuntimeError("fixed split contract is not satisfied")
    return result


def verify_profile(
    *,
    repository_root: Path,
    processed_root: Path,
    dataset: str,
    contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    processed_root = assert_canonical_processed_root(
        repository_root, processed_root
    )
    paths = _paths(repository_root, processed_root, dataset, contract)
    manifest_path = manifest_path_for(paths.data_path)
    for path in (paths.data_path, paths.dataset_path, manifest_path):
        if not path.is_file():
            raise RuntimeError(
                "target-direct processed profile is incomplete: {0}".format(path)
            )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema") != MANIFEST_SCHEMA
        or manifest.get("version") != MANIFEST_VERSION
        or manifest.get("profile") != contract.processed_profile
        or str(manifest.get("dataset", "")).lower() != dataset.lower()
    ):
        raise RuntimeError("target-direct profile manifest identity is invalid")
    for field, path in (
        ("data_sha256", paths.data_path),
        ("dataset_sha256", paths.dataset_path),
    ):
        if manifest.get(field) != _sha256_file(path):
            raise RuntimeError(
                "target-direct processed profile {0} mismatch".format(field)
            )

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
        raise RuntimeError("target-direct dataset pickle is not native Planetoid")
    observed_graph = _opengu_graph_contract(
        data, dataset_name=dataset, materialize=False
    )
    observed_processed = _opengu_split_contract(data, materialize=False)
    observed_split = split_observation(data, contract=contract)
    if observed_graph != manifest.get("opengu_graph_contract"):
        raise RuntimeError("target-direct graph contract changed")
    if observed_processed != manifest.get("opengu_processed_contract"):
        raise RuntimeError("target-direct OpenGU split fields changed")
    if observed_split != manifest.get("split_observation"):
        raise RuntimeError("target-direct split observation changed")
    inputs = make_dataset_selection_inputs(
        data, dataset_name=dataset.lower(), source_path=paths.data_path
    )
    observed_identity = {
        "dataset_fingerprint": inputs.dataset_fingerprint,
        "graph_fingerprint": inputs.graph_fingerprint,
        "candidate_set_hash": inputs.candidate_set_hash,
        "candidate_count": inputs.candidate_count,
        "num_nodes": inputs.num_nodes,
    }
    if observed_identity != manifest.get("selection_identity"):
        raise RuntimeError("target-direct Selection identity changed")
    return {
        "manifest": manifest,
        "manifest_path": str(manifest_path),
        "data_path": str(paths.data_path),
        "dataset_path": str(paths.dataset_path),
        "inputs": inputs,
        "data": data,
    }


def stage_profile(
    *,
    repository_root: Path,
    processed_root: Path,
    dataset: str,
    contract: ProcessedSplitContract = DEFAULT_SPLIT_CONTRACT,
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    processed_root = assert_canonical_processed_root(
        repository_root, processed_root
    )
    paths = _paths(repository_root, processed_root, dataset, contract)
    manifest_path = manifest_path_for(paths.data_path)
    existing = [
        path.exists() for path in (paths.data_path, paths.dataset_path, manifest_path)
    ]
    if any(existing):
        if not all(existing):
            raise RuntimeError(
                "refusing to replace an incomplete target-direct profile"
            )
        return {
            "status": "reused",
            **verify_profile(
                repository_root=repository_root,
                processed_root=processed_root,
                dataset=dataset,
                contract=contract,
            ),
        }

    source = resolve_planetoid_public_source(
        repository_root / "data" / "raw",
        repository_root=repository_root,
        dataset=dataset,
    )
    pyg_dataset = _load_offline_planetoid(source)
    data = pyg_dataset[0]
    split = apply_fixed_split(data, contract=contract)
    graph_contract = _opengu_graph_contract(
        data, dataset_name=source.storage_name, materialize=True
    )
    processed_contract = _opengu_split_contract(data, materialize=True)
    inputs = make_dataset_selection_inputs(
        data, dataset_name=dataset.lower(), source_path=paths.data_path
    )
    _atomic_bytes(
        paths.data_path, pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    )
    _atomic_bytes(
        paths.dataset_path,
        pickle.dumps(pyg_dataset, protocol=pickle.HIGHEST_PROTOCOL),
    )
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": MANIFEST_VERSION,
        "profile": contract.processed_profile,
        "dataset": source.dataset,
        "lane": "transductive",
        "data_path": str(paths.data_path),
        "dataset_path": str(paths.dataset_path),
        "data_sha256": _sha256_file(paths.data_path),
        "dataset_sha256": _sha256_file(paths.dataset_path),
        "dataset_source": source.to_manifest(),
        "split_observation": split,
        "opengu_graph_contract": graph_contract,
        "opengu_processed_contract": processed_contract,
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
    return {
        "status": "created",
        **verify_profile(
            repository_root=repository_root,
            processed_root=processed_root,
            dataset=dataset,
            contract=contract,
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument(
        "--dataset", choices=("Cora", "CiteSeer", "PubMed"), required=True
    )
    parser.add_argument(
        "--processed-profile",
        default=None,
    )
    parser.add_argument(
        "--train-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.train_ratio
    )
    parser.add_argument(
        "--val-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.val_ratio
    )
    parser.add_argument(
        "--test-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.test_ratio
    )
    parser.add_argument(
        "--split-seed", type=int, default=DEFAULT_SPLIT_CONTRACT.split_seed
    )
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    function = verify_profile if args.verify_only else stage_profile
    contract = target_direct_split_contract(
        {
            "processed_profile": args.processed_profile,
            "split": {
                "train_ratio": args.train_ratio,
                "val_ratio": args.val_ratio,
                "test_ratio": args.test_ratio,
                "split_seed": args.split_seed,
            },
        },
        require_explicit=True,
    )
    result = function(
        repository_root=args.repository_root,
        processed_root=args.processed_root,
        dataset=args.dataset,
        contract=contract,
    )
    payload = {
        key: value for key, value in result.items() if key not in {"inputs", "data"}
    }
    if args.json:
        print(json.dumps(payload, indent=2, default=str))
    else:
        print("target-direct profile: {0}".format(payload.get("status", "verified")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
