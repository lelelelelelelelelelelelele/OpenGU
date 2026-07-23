"""Load target-direct Selection Artifacts and exact target checkpoints for GU."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from cache_v2.runtime import load_selection_artifact
from experiments.target_direct_v1 import PROFILE
from experiments.target_direct_v1.build_manifest import SCHEMA, VERSION, sha256_file
from experiments.target_direct_v1.split_profile import verify_profile
from utils.target_checkpoint import data_identity, load_target_checkpoint


def load_external_selection_manifest(
    cfg: Mapping[str, Any],
    *,
    manifest_path: Path,
    expected_manifest_sha256: str,
    expected_store_root: Path,
    processed_root: Path,
) -> Tuple[Dict[Tuple[str, int], Dict[str, Any]], Dict[str, Any]]:
    manifest_path = Path(manifest_path).resolve()
    if sha256_file(manifest_path) != str(expected_manifest_sha256):
        raise ValueError("target-direct external manifest SHA-256 mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("schema") != SCHEMA
        or manifest.get("version") != VERSION
    ):
        raise ValueError("target-direct external manifest schema/version mismatch")
    expected = {
        "dataset": str(cfg["dataset"]).lower(),
        "base_model": str(cfg["base_model"]),
        "processed_profile": str(cfg.get("processed_profile") or ""),
        "ratio": float(cfg["ratio"]),
        "gu_methods": list(cfg["methods"]),
        "strategies": list(cfg["strategies"]),
        "seeds": [int(value) for value in cfg["seeds"]],
    }
    for field, value in expected.items():
        if manifest.get(field) != value:
            raise ValueError(
                "target-direct external manifest {0} mismatch".format(field)
            )
    if manifest.get("processed_profile") != PROFILE:
        raise ValueError("target-direct processed profile is not canonical")
    store_root = Path(str(manifest.get("store_root") or "")).resolve()
    if store_root != Path(expected_store_root).resolve():
        raise ValueError("target-direct Selection store root mismatch")
    profile = verify_profile(
        repository_root=Path(__file__).resolve().parents[2],
        processed_root=processed_root,
        dataset=str(cfg["dataset"]),
    )
    inputs = profile["inputs"]
    if manifest.get("selection_identity") != profile["manifest"][
        "selection_identity"
    ]:
        raise ValueError("target-direct dataset identity changed")
    expected_k = max(1, int(inputs.candidate_count * float(cfg["ratio"])))
    if (
        int(manifest.get("candidate_count", -1)) != inputs.candidate_count
        or int(manifest.get("expected_k", -1)) != expected_k
        or manifest.get("budget_denominator") != "train_candidate_count"
        or (manifest.get("budget") or {}).get("denominator")
        != "train_candidate_count"
        or (manifest.get("budget") or {}).get("rounding")
        != "floor_with_minimum_one"
        or float((manifest.get("budget") or {}).get("ratio", -1))
        != float(cfg["ratio"])
        or int((manifest.get("budget") or {}).get("denominator_count", -1))
        != inputs.candidate_count
        or int((manifest.get("budget") or {}).get("expected_k", -1))
        != expected_k
    ):
        raise ValueError("target-direct budget identity mismatch")
    observed_data_identity = data_identity(profile["data"])
    mapping: Dict[Tuple[str, int], Dict[str, Any]] = {}
    checkpoint_by_seed = {}
    for cell in manifest.get("cells") or []:
        strategy = str(cell.get("strategy") or "")
        seed = int(cell.get("seed"))
        ratio = float(cell.get("ratio", -1))
        k = int(cell.get("k"))
        if ratio != float(cfg["ratio"]) or k != expected_k:
            raise ValueError("target-direct cell ratio/k mismatch")
        artifact = cell.get("artifact") or {}
        loaded = load_selection_artifact(
            store_root,
            str(artifact.get("artifact_id") or ""),
            num_nodes=inputs.num_nodes,
            candidate_nodes=inputs.candidate_nodes,
            expected_selector=strategy,
            expected_k=k,
        )
        if (
            loaded.recipe_hash != artifact.get("recipe_hash")
            or loaded.content_hash != artifact.get("content_hash")
            or list(loaded.selected_nodes) != cell.get("selected_nodes")
        ):
            raise ValueError("target-direct Selection Artifact identity changed")
        declared_checkpoint = cell.get("target_checkpoint") or {}
        loaded_checkpoint = load_target_checkpoint(
            declared_checkpoint.get("path"),
            expected_file_sha256=declared_checkpoint.get("file_sha256"),
            expected_state_hash=declared_checkpoint.get("state_hash"),
            expected_metadata={
                "dataset_name": str(cfg["dataset"]).lower(),
                "base_model": "GCN",
                "seed": seed,
                "processed_profile": PROFILE,
                "num_epochs": int((cfg.get("defaults") or {}).get("num_epochs", 100)),
                "gcn_num_layers": int(
                    ((cfg.get("model_overrides") or {}).get("GCN") or {}).get(
                        "gcn_num_layers", 2
                    )
                ),
                "gcn_hidden": int(
                    ((cfg.get("model_overrides") or {}).get("GCN") or {}).get(
                        "gcn_hidden", 64
                    )
                ),
            },
        )
        if loaded_checkpoint["metadata"].get("data_identity") != observed_data_identity:
            raise ValueError("target-direct checkpoint dataset/split identity changed")
        checkpoint_identity = {
            "path": loaded_checkpoint["path"],
            "file_sha256": loaded_checkpoint["file_sha256"],
            "state_hash": loaded_checkpoint["state_hash"],
            "checkpoint_count": len(loaded_checkpoint["checkpoints"]),
        }
        previous = checkpoint_by_seed.setdefault(seed, checkpoint_identity)
        if previous != checkpoint_identity:
            raise ValueError("strategies do not share one target checkpoint per seed")
        key = (strategy, seed)
        if key in mapping:
            raise ValueError("target-direct manifest contains duplicate cells")
        provenance = dict(loaded.provenance(store_root))
        mapping[key] = {
            "store_root": str(store_root),
            "artifact_id": loaded.artifact_id,
            "artifact_type": "selection",
            "recipe_hash": loaded.recipe_hash,
            "content_hash": loaded.content_hash,
            "source_file": provenance["source_file"],
            "hit_source": provenance["hit_source"],
            "lookup_policy": provenance["lookup_policy"],
            "authoritative": True,
            "write_outcome": "reused",
            "strategy": strategy,
            "ratio": ratio,
            "k": k,
            "selected_node_count": len(loaded.selected_nodes),
            "source_score_artifact_id": cell.get("source_score_artifact_id"),
            "source_score_recipe_hash": cell.get("source_score_recipe_hash"),
            "target_checkpoint": checkpoint_identity,
            "external_selection_manifest": str(manifest_path),
            "external_selection_manifest_sha256": expected_manifest_sha256,
        }
    expected_keys = {
        (str(strategy), int(seed))
        for strategy in cfg["strategies"]
        for seed in cfg["seeds"]
    }
    if set(mapping) != expected_keys:
        raise ValueError("target-direct external Selection matrix is incomplete")
    return mapping, {
        "mode": "target_direct_external_selection",
        "manifest_path": str(manifest_path),
        "manifest_sha256": expected_manifest_sha256,
        "writes": [],
        "cells": len(mapping),
        "target_checkpoint_count": len(checkpoint_by_seed),
    }
