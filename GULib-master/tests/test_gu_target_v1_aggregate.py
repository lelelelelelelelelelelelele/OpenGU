"""Tests for the formal small-selection GU matrix aggregator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from experiments.gu_target_v1 import aggregate


GIT_SHA = "1" * 40


def _write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def _matrix(tmp_path: Path):
    selection_manifest = tmp_path / "selection.json"
    selection_cells = []
    for dataset in aggregate.DATASETS:
        for seed in aggregate.SEEDS:
            selection_cells.append(
                {
                    "dataset": dataset,
                    "seed": seed,
                    "status": "success",
                    "failure": None,
                    "score_bundle_cold_total_seconds": 6.0,
                    "score_bundle_warm_read_seconds": 0.2,
                    "peak_gpu_allocated_bytes": 100,
                    "peak_gpu_reserved_bytes": 200,
                    "methods": {
                        selector: {
                            "status": "success",
                            "failure": None,
                            "cold_cache_hit": False,
                            "warm_cache_hit": True,
                            "cold_selection_seconds": 0.4,
                            "warm_selection_seconds": 0.3,
                        }
                        for selector in aggregate.SELECTORS
                    },
                }
            )
    _write_json(
        selection_manifest,
        {
            "formal_score_names": list(aggregate.SELECTORS),
            "cells": selection_cells,
        },
    )
    selection_sha = hashlib.sha256(selection_manifest.read_bytes()).hexdigest()

    run_root = tmp_path / "run"
    for dataset in aggregate.DATASETS:
        for seed in aggregate.SEEDS:
            for index, selector in enumerate(aggregate.SELECTORS):
                leaf = (
                    run_root
                    / f"{dataset}_GCN_r0.05"
                    / f"GNNDelete_{selector}"
                    / f"seed{seed}"
                )
                leaf.mkdir(parents=True)
                if selector == "degree":
                    drop = 0.10
                elif selector == "tracin_cp_point_6":
                    drop = 0.02
                elif selector == "random":
                    drop = 0.0
                else:
                    drop = 0.01
                nodes = list(range(index * 10, index * 10 + 7))
                _write_json(
                    leaf / "attack.json",
                    {
                        "results": {
                            selector: {
                                "selected_nodes": nodes,
                                "f1_before": 0.8,
                                "f1_after": 0.8 - drop,
                                "f1_drop": drop,
                                "f1_drop_ratio": drop / 0.8 * 100,
                                "mia_auc": 0.6,
                                "unlearn_time": 0.4,
                                "total_time": 1.1,
                                "selection_reuse_time": 0.3,
                                "selection_artifact_id": f"sel_{index}",
                                "selection_content_hash": f"hash_{index}",
                                "failed": False,
                                "config": {},
                            }
                        }
                    },
                )
                _write_json(
                    leaf / "collateral.json",
                    {
                        "results": [
                            {
                                "strategy": selector,
                                "perf_before": 0.8,
                                "perf_retrain": 0.79,
                                "perf_unlearn": 0.78,
                                "gap": 0.01,
                                "gap_pct": 1.2658,
                                "mean_pred_shift": 0.02,
                                "max_pred_shift": 0.2,
                                "fraction_flipped": 0.03,
                            }
                        ]
                    },
                )
                _write_json(
                    leaf / "_meta.json",
                    {
                        "git_sha": GIT_SHA,
                        "method": "GNNDelete",
                        "strategy": selector,
                        "seed": seed,
                        "config": {
                            "dataset": dataset,
                            "base_model": "GCN",
                            "processed_profile": "planetoid_public_fixed",
                        },
                        "selection_artifact": {
                            "authoritative": True,
                            "strategy": selector,
                            "k": 7,
                            "selected_node_count": 7,
                            "source_selection": {
                                "benchmark_manifest_sha256": selection_sha
                            },
                        },
                    },
                )
                (leaf / "predictions.npz").write_bytes(b"npz")

    checksum_manifest = tmp_path / "SHA256SUMS_RESULTS"
    lines = []
    for path in sorted(path for path in run_root.rglob("*") if path.is_file()):
        relative = path.relative_to(run_root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  ./{relative}")
    checksum_manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return run_root, checksum_manifest, selection_manifest, selection_sha


def test_aggregate_writes_complete_machine_readable_tables(tmp_path):
    run_root, checksums, selection, selection_sha = _matrix(tmp_path)
    output = tmp_path / "analysis"

    summary = aggregate.aggregate(
        run_root,
        selection,
        checksums,
        output,
        GIT_SHA,
        selection_sha,
    )

    assert summary["formal_run"]["cells"] == 153
    assert summary["checksum_verification"]["verified_files"] == 612
    assert summary["descriptive_findings"]["top_selector_by_paired_delta_vs_random"] == "degree"
    assert summary["descriptive_findings"]["best_checkpoint_variant"] == "tracin_cp_point_6"
    assert summary["descriptive_findings"]["best_standard_tracin_selector"] == "tracin_cp_point_6"
    assert len((output / "cell_metrics.csv").read_text(encoding="utf-8").splitlines()) == 154
    assert len((output / "selector_summary.csv").read_text(encoding="utf-8").splitlines()) == 18
    assert len((output / "dataset_selector_summary.csv").read_text(encoding="utf-8").splitlines()) == 52
    assert len((output / "pairwise_summary.csv").read_text(encoding="utf-8").splitlines()) == 14
    assert len((output / "selection_timing_summary.csv").read_text(encoding="utf-8").splitlines()) == 18


def test_load_matrix_rejects_wrong_git_binding(tmp_path):
    run_root, _checksums, _selection, selection_sha = _matrix(tmp_path)

    with pytest.raises(aggregate.AggregationError, match="Git SHA mismatch"):
        aggregate.load_matrix(run_root, "f" * 40, selection_sha)
