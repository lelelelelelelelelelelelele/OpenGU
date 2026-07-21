"""Contract tests for the hypothesis-preserving Selection-to-GU adapter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import torch
from torch_geometric.data import Data

from experiments.bc_target_v2.recipe import SCORE_NAMES
from experiments.gu_target_v1 import adapter
from experiments.gu_target_v1 import syncmate_recipe
from experiments.gu_target_v1 import syncmate_stage
from experiments.processed_provider import processed_artifact_paths
from experiments.selection_inputs import make_dataset_selection_inputs


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inputs(tmp_path: Path):
    data = Data(
        x=torch.eye(5),
        y=torch.tensor([0, 1, 0, 1, 0]),
        edge_index=torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]]),
    )
    data.train_mask = torch.tensor([True, True, True, True, False])
    return make_dataset_selection_inputs(
        data, dataset_name="cora", source_path=tmp_path / "cora.pkl"
    )


def test_named_processed_profile_uses_explicit_non_ratio_stem(tmp_path):
    paths = processed_artifact_paths(
        {
            "processed_root": str(tmp_path),
            "processed_profile": "planetoid_public_fixed",
            "dataset_name": "cora",
            "train_ratio": 0.8,
            "val_ratio": 0.0,
            "test_ratio": 0.2,
            "is_transductive": True,
            "is_balanced": False,
        }
    )

    assert paths.data_path == tmp_path / "transductive" / "cora__planetoid_public_fixed.pkl"
    assert paths.dataset_path == tmp_path / "transductive" / "cora__planetoid_public_fixeddataset.pkl"


def test_fixed_gu_gate_config_preserves_claim_boundary():
    config = syncmate_recipe._config()

    assert config["methods"] == ["GNNDelete"]
    assert config["strategies"] == ["degree"]
    assert config["selection_k"] == 7
    assert config["processed_profile"] == "planetoid_public_fixed"
    assert config["claims"]["infrastructure_gate"] is True
    assert config["claims"]["scientific_comparison"] is False
    assert config["claims"]["canonical_opengu_80_20"] is False


def test_fixed_gu_full_config_covers_exact_17_by_3_by_3_matrix():
    config = syncmate_stage._config()

    assert config["strategies"] == list(SCORE_NAMES)
    assert config["seeds"] == [42, 212, 2024]
    assert set(config["datasets"]) == {"cora", "citeseer", "pubmed"}
    assert config["selection_k"] == 7
    assert config["claims"]["gate_required"] is True
    assert config["claims"]["total_cells"] == 153
    assert len(syncmate_stage.expected_artifacts("pubmed-seed2024", config)) == 68


def test_adapter_materializes_and_loads_custom_formula_label(tmp_path, monkeypatch):
    inputs = _inputs(tmp_path)
    profile_manifest = {
        "dataset_source": {"source_fingerprint": "c" * 64},
        "selection_identity": {
            "dataset_fingerprint": inputs.dataset_fingerprint,
            "graph_fingerprint": inputs.graph_fingerprint,
            "candidate_set_hash": inputs.candidate_set_hash,
            "candidate_count": inputs.candidate_count,
            "num_nodes": inputs.num_nodes,
        }
    }

    def fake_profile(**kwargs):
        return {
            "inputs": inputs,
            "manifest": profile_manifest,
            "manifest_path": str(tmp_path / "profile.manifest.json"),
        }

    monkeypatch.setattr(adapter, "verify_public_profile", fake_profile)
    summary = {
        "schema": "bc_target_v2.selection_summary",
        "version": 2,
        "algorithm_version": "bc-target-matrix-v3.0",
        "dataset": "Cora",
        "seed": 42,
        "status": {"state": "success", "failure": None},
        "candidate_count": inputs.candidate_count,
        "cache": {"artifact_id": "score_12345678_90abcdef"},
        "selector_model_final_state_hash": "a" * 64,
        "rankings": {
            name: list(inputs.candidate_nodes) for name in SCORE_NAMES
        },
    }
    benchmark = {
        "schema": "bc_target_v2.small_graph_selection_benchmark",
        "version": 1,
        "experiment_git_sha": "b" * 40,
        "cells": [{"dataset": "Cora", "seed": 42, "status": "success"}],
    }
    summary_path = tmp_path / "cold.json"
    benchmark_path = tmp_path / "benchmark.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    benchmark_path.write_text(json.dumps(benchmark), encoding="utf-8")
    store_root = tmp_path / "store"
    manifest_path = tmp_path / "external.json"

    manifest = adapter.materialize_grandfathered_selection(
        repository_root=tmp_path,
        processed_root=tmp_path / "processed",
        source_summary_path=summary_path,
        source_summary_sha256=_sha(summary_path),
        benchmark_manifest_path=benchmark_path,
        benchmark_manifest_sha256=_sha(benchmark_path),
        expected_experiment_git_sha="b" * 40,
        expected_public_source_fingerprint="c" * 64,
        dataset="Cora",
        seed=42,
        strategies=("a_grad_norm",),
        k=3,
        base_model="GCN",
        gu_methods=("GNNDelete",),
        store_root=store_root,
        manifest_path=manifest_path,
    )

    assert manifest["cells"][0]["strategy"] == "a_grad_norm"
    assert manifest["cells"][0]["research_group"] == "a_b"
    assert manifest["claims"]["canonical_opengu_80_20"] is False
    cfg = {
        "dataset": "cora",
        "base_model": "GCN",
        "processed_profile": "planetoid_public_fixed",
        "methods": ["GNNDelete"],
        "strategies": ["a_grad_norm"],
        "seeds": [42],
    }
    mapping, document = adapter.load_external_selection_manifest(
        cfg,
        manifest_path=manifest_path,
        expected_store_root=store_root,
        processed_root=tmp_path / "processed",
    )

    artifact = mapping[("a_grad_norm", 42)]
    assert artifact["strategy"] == "a_grad_norm"
    assert artifact["k"] == 3
    assert artifact["selected_node_count"] == 3
    assert artifact["source_selection"]["profile"] == "grandfathered-public-selection-gt-v1"
    assert document["mode"] == "external_selection"
