"""CPU-only Gate 3 adapter tests using canonical Cora dimensions."""

from __future__ import annotations

import hashlib
import json
import pickle
from pathlib import Path

import numpy as np
import pytest
import torch
from torch_geometric.data import Data

from attack.attack_strategies.degree_strategy import DegreeStrategy
from cache_v2.errors import ContractValidationError
from experiments.gate3_degree_adapter import materialize_degree_gate3_bundle


def _tree_state(root: Path):
    return {
        path.relative_to(root).as_posix(): (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            path.stat().st_mtime_ns,
            path.stat().st_size,
        )
        for path in root.rglob("*")
        if path.is_file()
    }


def _canonical_cora_data() -> Data:
    num_nodes = 2708
    edge_count = 10556
    edge_ids = torch.arange(edge_count, dtype=torch.long)
    edge_index = torch.stack((edge_ids // num_nodes, edge_ids % num_nodes))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[: int(0.8 * num_nodes)] = True
    test_mask = ~train_mask
    return Data(
        x=torch.arange(num_nodes * 4, dtype=torch.float32).reshape(num_nodes, 4),
        y=torch.arange(num_nodes, dtype=torch.long) % 7,
        edge_index=edge_index,
        train_mask=train_mask,
        test_mask=test_mask,
        train_indices=train_mask.nonzero(as_tuple=False).view(-1),
        num_nodes=num_nodes,
    )


def _write_fixture(tmp_path: Path, *, mismatch: bool = False):
    data = _canonical_cora_data()
    processed_root = (tmp_path / "processed").resolve()
    processed = processed_root / "transductive" / "cora0.8_0_0.2.pkl"
    processed.parent.mkdir(parents=True)
    with processed.open("wb") as handle:
        pickle.dump(data, handle)

    selected = DegreeStrategy({}).select_nodes(
        Data(
            edge_index=data.edge_index,
            num_nodes=data.num_nodes,
            train_indices=data.train_indices,
        ),
        torch.nn.Identity(),
        108,
    ).numpy()
    if mismatch:
        selected = selected.copy()
        replacement = next(
            node
            for node in data.train_indices.tolist()
            if node not in set(int(item) for item in selected)
        )
        selected[-1] = replacement

    num_nodes = int(data.num_nodes)
    num_classes = 7
    y = data.y.numpy()
    logits = np.full((num_nodes, num_classes), -4.0, dtype=np.float32)
    logits[np.arange(num_nodes), y] = 4.0
    retain_mask = data.train_mask.numpy().copy()
    retain_mask[selected] = False

    leaf = (
        tmp_path
        / "reference"
        / "cora_GCN_r0.05"
        / "GIF_degree"
        / "seed42"
    ).resolve()
    leaf.mkdir(parents=True)
    attack = {
        "config": {
            "dataset_name": "cora",
            "base_model": "GCN",
            "unlearning_methods": "GIF",
            "train_ratio": 0.8,
            "val_ratio": 0.0,
            "test_ratio": 0.2,
            "is_transductive": True,
            "is_balanced": False,
            "unlearn_ratio": 0.05,
            "random_seed": 42,
        },
        "results": {
            "degree": {
                "strategy_name": "degree",
                "selected_nodes": selected.tolist(),
                "config": {"k": 108},
                "failed": False,
            }
        },
    }
    collateral = {
        "config": {
            "dataset_name": "cora",
            "base_model": "GCN",
            "unlearning_methods": "GIF",
            "unlearn_ratio": 0.05,
            "random_seed": 42,
            "strategies_requested": ["degree"],
        },
        "results": [
            {
                "strategy": "degree",
                "perf_before": 1.0,
                "perf_retrain": 1.0,
                "perf_unlearn": 1.0,
                "drop_retrain": 0.0,
                "gap": 0.0,
                "gap_pct": 0.0,
                "mean_pred_shift": 0.0,
                "max_pred_shift": 0.0,
                "fraction_flipped": 0.0,
                "hop_decay": {},
            }
        ],
    }
    meta = {
        "config_name": "fixture",
        "method": "GIF",
        "strategy": "degree",
        "seed": 42,
        "git_sha": "1" * 40,
        "config_fingerprint": "fixture",
        "fingerprint_version": "v1",
    }
    (leaf / "attack.json").write_text(
        json.dumps(attack, indent=2), encoding="utf-8"
    )
    (leaf / "collateral.json").write_text(
        json.dumps(collateral, indent=2), encoding="utf-8"
    )
    (leaf / "_meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )
    np.savez(
        leaf / "predictions.npz",
        _meta__y=y,
        _meta__train_mask=data.train_mask.numpy(),
        _meta__test_mask=data.test_mask.numpy(),
        _meta__num_nodes=np.int64(num_nodes),
        degree__logits_before=logits,
        degree__logits_unlearned=logits.copy(),
        degree__logits_retrained=logits.copy(),
        degree__retain_mask=retain_mask,
        degree__selected_nodes=selected,
    )
    return processed_root, leaf


def test_gate3_degree_adapter_materializes_exact_four_artifact_chain(tmp_path):
    processed_root, leaf = _write_fixture(tmp_path)
    store_root = (tmp_path / "isolated-v2").resolve()
    source_before = _tree_state(leaf)

    cold = materialize_degree_gate3_bundle(
        source_leaf=leaf,
        processed_root=processed_root,
        store_root=store_root,
    )
    warm = materialize_degree_gate3_bundle(
        source_leaf=leaf,
        processed_root=processed_root,
        store_root=store_root,
    )

    assert cold["passed"] is True
    assert cold["comparison"]["status"] == "passed"
    assert cold["canonical_dataset"]["num_nodes"] == 2708
    assert cold["canonical_dataset"]["edge_count"] == 10556
    assert cold["selection"]["ordered_exact"] is True
    assert cold["artifacts"]["score"]["artifact_id"].startswith("score_")
    assert cold["artifacts"]["selection"]["artifact_id"].startswith("sel_")
    assert cold["artifacts"]["prediction"]["artifact_id"].startswith("pred_")
    assert cold["artifacts"]["evaluation"]["artifact_id"].startswith("eval_")
    assert (
        cold["artifacts"]["selection"]["source_score_artifact_id"]
        == cold["artifacts"]["score"]["artifact_id"]
    )
    assert all(
        cold["artifacts"][name]["producer_called"]
        for name in ("score", "selection", "prediction", "evaluation")
    )
    assert not any(
        warm["artifacts"][name]["producer_called"]
        for name in ("score", "selection", "prediction", "evaluation")
    )
    assert cold["artifact_ids"] == warm["artifact_ids"]
    assert cold["source_unchanged"] is True
    assert warm["source_unchanged"] is True
    assert _tree_state(leaf) == source_before


def test_gate3_degree_adapter_fails_closed_on_selector_content_mismatch(tmp_path):
    processed_root, leaf = _write_fixture(tmp_path, mismatch=True)

    with pytest.raises(ContractValidationError, match="ordered Selection mismatch"):
        materialize_degree_gate3_bundle(
            source_leaf=leaf,
            processed_root=processed_root,
            store_root=(tmp_path / "isolated-v2").resolve(),
        )
