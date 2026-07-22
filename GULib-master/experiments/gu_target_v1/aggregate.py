"""Aggregate the accepted small-graph Selection-to-GU matrix.

The aggregator is deliberately fail-closed.  It accepts only the formal
3-dataset x 3-seed x 17-selector GNNDelete matrix, validates the four-file
leaf contract and provenance, optionally re-verifies the remote SHA-256
manifest, and writes machine-readable analysis tables.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


DATASETS: Tuple[str, ...] = ("cora", "citeseer", "pubmed")
SEEDS: Tuple[int, ...] = (42, 212, 2024)
SELECTORS: Tuple[str, ...] = (
    "a_grad_norm",
    "b_param_hutch",
    "degree",
    "gt_full",
    "gt_simple",
    "legacy",
    "p_graph",
    "p_point",
    "p_simple",
    "r_point",
    "random",
    "tracin_cp_graph_3",
    "tracin_cp_graph_6",
    "tracin_cp_point_3",
    "tracin_cp_point_6",
    "tracin_cp_simple_3",
    "tracin_cp_simple_6",
)
ARTIFACT_NAMES: Tuple[str, ...] = (
    "attack.json",
    "collateral.json",
    "predictions.npz",
    "_meta.json",
)

FAMILY: Mapping[str, str] = {
    "random": "control",
    "degree": "control",
    "a_grad_norm": "A-gradient-magnitude",
    "b_param_hutch": "B-parameter-movement",
    "legacy": "legacy-negative-control",
    "r_point": "C-point-reference",
    "p_point": "C-point-final-proxy",
    "tracin_cp_point_3": "C-point-checkpoint",
    "tracin_cp_point_6": "C-point-checkpoint",
    "gt_simple": "C-simple-reference",
    "p_simple": "C-simple-final-proxy",
    "tracin_cp_simple_3": "C-simple-checkpoint",
    "tracin_cp_simple_6": "C-simple-checkpoint",
    "gt_full": "D-full-reference",
    "p_graph": "D-full-final-proxy",
    "tracin_cp_graph_3": "D-full-checkpoint",
    "tracin_cp_graph_6": "D-full-checkpoint",
}

KEY_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("tracin_cp_point_6", "degree"),
    ("tracin_cp_point_6", "random"),
    ("tracin_cp_point_3", "degree"),
    ("tracin_cp_graph_3", "degree"),
    ("tracin_cp_graph_6", "degree"),
    ("tracin_cp_simple_3", "degree"),
    ("tracin_cp_simple_6", "degree"),
    ("p_graph", "gt_full"),
    ("p_point", "r_point"),
    ("p_simple", "gt_simple"),
    ("tracin_cp_point_6", "tracin_cp_point_3"),
    ("tracin_cp_graph_6", "tracin_cp_graph_3"),
    ("tracin_cp_simple_6", "tracin_cp_simple_3"),
)


class AggregationError(RuntimeError):
    """Raised when the formal matrix or its provenance is incomplete."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AggregationError(message)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AggregationError(f"could not read JSON {path}: {exc}") from exc
    _require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def _finite_number(value: Any, label: str) -> float:
    _require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} is not numeric")
    number = float(value)
    _require(math.isfinite(number), f"{label} is not finite")
    return number


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_checksum_manifest(run_root: Path, manifest_path: Path) -> Dict[str, Any]:
    """Re-hash every result named by the remote manifest."""

    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    _require(len(lines) == 612, f"checksum manifest has {len(lines)} rows, expected 612")
    seen = set()
    for line in lines:
        parts = line.split("  ./", 1)
        _require(len(parts) == 2, f"invalid checksum row: {line!r}")
        expected, relative = parts
        _require(len(expected) == 64 and all(ch in "0123456789abcdef" for ch in expected), f"invalid SHA-256: {expected}")
        _require(relative not in seen, f"duplicate checksum path: {relative}")
        seen.add(relative)
        path = run_root / Path(relative)
        _require(path.is_file(), f"checksum target missing: {relative}")
        _require(_sha256(path) == expected, f"checksum mismatch: {relative}")
    actual = {path.relative_to(run_root).as_posix() for path in run_root.rglob("*") if path.is_file()}
    _require(actual == seen, "checksum manifest and run-root file sets differ")
    return {
        "manifest_path": str(manifest_path.resolve()),
        "manifest_sha256": _sha256(manifest_path),
        "verified_files": len(seen),
        "passed": True,
    }


def _attack_result(attack: Mapping[str, Any], selector: str, label: str) -> Mapping[str, Any]:
    results = attack.get("results")
    _require(isinstance(results, dict), f"{label}: attack results missing")
    result = results.get(selector)
    _require(isinstance(result, dict), f"{label}: selector result missing")
    return result


def _collateral_result(collateral: Mapping[str, Any], selector: str, label: str) -> Mapping[str, Any]:
    results = collateral.get("results")
    _require(isinstance(results, list) and len(results) == 1, f"{label}: collateral result count is not one")
    result = results[0]
    _require(isinstance(result, dict) and result.get("strategy") == selector, f"{label}: collateral selector mismatch")
    return result


def load_matrix(
    run_root: Path,
    expected_git_sha: str,
    expected_selection_manifest_sha256: str,
) -> Tuple[List[Dict[str, Any]], Dict[Tuple[str, int, str], Tuple[int, ...]]]:
    """Load and validate all 153 accepted result leaves."""

    _require(run_root.is_dir(), f"run root does not exist: {run_root}")
    rows: List[Dict[str, Any]] = []
    selected_sets: Dict[Tuple[str, int, str], Tuple[int, ...]] = {}
    for dataset in DATASETS:
        for seed in SEEDS:
            for selector in SELECTORS:
                label = f"{dataset}/seed{seed}/{selector}"
                leaf = run_root / f"{dataset}_GCN_r0.05" / f"GNNDelete_{selector}" / f"seed{seed}"
                _require(leaf.is_dir(), f"missing result leaf: {label}")
                files = {path.name for path in leaf.iterdir() if path.is_file()}
                _require(files == set(ARTIFACT_NAMES), f"{label}: four-file contract differs: {sorted(files)}")
                _require((leaf / "predictions.npz").stat().st_size > 0, f"{label}: predictions.npz is empty")

                meta = _read_json(leaf / "_meta.json")
                attack = _read_json(leaf / "attack.json")
                collateral = _read_json(leaf / "collateral.json")
                _require(meta.get("git_sha") == expected_git_sha, f"{label}: Git SHA mismatch")
                _require(meta.get("method") == "GNNDelete", f"{label}: GU method mismatch")
                _require(meta.get("strategy") == selector and meta.get("seed") == seed, f"{label}: identity mismatch")
                config = meta.get("config") or {}
                _require(config.get("dataset") == dataset and config.get("base_model") == "GCN", f"{label}: dataset/model mismatch")
                _require(config.get("processed_profile") == "planetoid_public_fixed", f"{label}: processed profile mismatch")

                selection = meta.get("selection_artifact") or {}
                source = selection.get("source_selection") or {}
                _require(selection.get("authoritative") is True, f"{label}: selection is not authoritative")
                _require(selection.get("strategy") == selector and selection.get("k") == 7, f"{label}: selection identity mismatch")
                _require(selection.get("selected_node_count") == 7, f"{label}: selected-node count mismatch")
                _require(
                    source.get("benchmark_manifest_sha256") == expected_selection_manifest_sha256,
                    f"{label}: Selection benchmark manifest mismatch",
                )

                result = _attack_result(attack, selector, label)
                failure = result.get("failed")
                _require(failure is False, f"{label}: GU result marked failed")
                nodes = result.get("selected_nodes")
                _require(isinstance(nodes, list) and len(nodes) == 7 and len(set(nodes)) == 7, f"{label}: invalid selected nodes")
                node_tuple = tuple(int(node) for node in nodes)
                selected_sets[(dataset, seed, selector)] = node_tuple
                coll = _collateral_result(collateral, selector, label)

                rows.append(
                    {
                        "dataset": dataset,
                        "seed": seed,
                        "selector": selector,
                        "family": FAMILY[selector],
                        "f1_before": _finite_number(result.get("f1_before"), f"{label}.f1_before"),
                        "f1_after": _finite_number(result.get("f1_after"), f"{label}.f1_after"),
                        "f1_drop": _finite_number(result.get("f1_drop"), f"{label}.f1_drop"),
                        "f1_drop_ratio": _finite_number(result.get("f1_drop_ratio"), f"{label}.f1_drop_ratio"),
                        "update_detection_auc": _finite_number(result.get("mia_auc"), f"{label}.mia_auc"),
                        "unlearn_seconds": _finite_number(result.get("unlearn_time"), f"{label}.unlearn_time"),
                        "attack_total_seconds": _finite_number(result.get("total_time"), f"{label}.total_time"),
                        "selection_reuse_seconds": _finite_number(result.get("selection_reuse_time"), f"{label}.selection_reuse_time"),
                        "retrain_minus_unlearn_gap": _finite_number(coll.get("gap"), f"{label}.gap"),
                        "gap_pct": _finite_number(coll.get("gap_pct"), f"{label}.gap_pct"),
                        "mean_pred_shift": _finite_number(coll.get("mean_pred_shift"), f"{label}.mean_pred_shift"),
                        "max_pred_shift": _finite_number(coll.get("max_pred_shift"), f"{label}.max_pred_shift"),
                        "fraction_flipped": _finite_number(coll.get("fraction_flipped"), f"{label}.fraction_flipped"),
                        "perf_before": _finite_number(coll.get("perf_before"), f"{label}.perf_before"),
                        "perf_retrain": _finite_number(coll.get("perf_retrain"), f"{label}.perf_retrain"),
                        "perf_unlearn": _finite_number(coll.get("perf_unlearn"), f"{label}.perf_unlearn"),
                        "selection_artifact_id": result.get("selection_artifact_id"),
                        "selection_content_hash": result.get("selection_content_hash"),
                        "selected_nodes": ";".join(str(node) for node in node_tuple),
                    }
                )

    actual_files = [path for path in run_root.rglob("*") if path.is_file()]
    _require(len(rows) == 153, f"matrix has {len(rows)} cells, expected 153")
    _require(len(actual_files) == 612, f"matrix has {len(actual_files)} files, expected 612")
    return rows, selected_sets


def _mean(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.fmean(data)


def _sample_sd(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.stdev(data) if len(data) > 1 else 0.0


def _wtl(values: Iterable[float], tolerance: float = 1e-12) -> Tuple[int, int, int]:
    wins = ties = losses = 0
    for value in values:
        if value > tolerance:
            wins += 1
        elif value < -tolerance:
            losses += 1
        else:
            ties += 1
    return wins, ties, losses


def add_paired_baselines(rows: List[Dict[str, Any]]) -> None:
    by_key = {(row["dataset"], row["seed"], row["selector"]): row for row in rows}
    for row in rows:
        key = (row["dataset"], row["seed"])
        random_drop = by_key[key + ("random",)]["f1_drop"]
        degree_drop = by_key[key + ("degree",)]["f1_drop"]
        row["paired_delta_vs_random"] = row["f1_drop"] - random_drop
        row["paired_delta_vs_degree"] = row["f1_drop"] - degree_drop


def selector_summary(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for selector in SELECTORS:
        group = [row for row in rows if row["selector"] == selector]
        _require(len(group) == 9, f"{selector}: expected nine rows")
        delta_random = [float(row["paired_delta_vs_random"]) for row in group]
        delta_degree = [float(row["paired_delta_vs_degree"]) for row in group]
        wr, tr, lr = _wtl(delta_random)
        wd, td, ld = _wtl(delta_degree)
        output.append(
            {
                "selector": selector,
                "family": FAMILY[selector],
                "mean_f1_drop": _mean(float(row["f1_drop"]) for row in group),
                "sd_f1_drop": _sample_sd(float(row["f1_drop"]) for row in group),
                "mean_paired_delta_vs_random": _mean(delta_random),
                "sd_paired_delta_vs_random": _sample_sd(delta_random),
                "wins_vs_random": wr,
                "ties_vs_random": tr,
                "losses_vs_random": lr,
                "mean_paired_delta_vs_degree": _mean(delta_degree),
                "wins_vs_degree": wd,
                "ties_vs_degree": td,
                "losses_vs_degree": ld,
                "mean_retrain_minus_unlearn_gap": _mean(float(row["retrain_minus_unlearn_gap"]) for row in group),
                "mean_fraction_flipped": _mean(float(row["fraction_flipped"]) for row in group),
                "mean_update_detection_auc": _mean(float(row["update_detection_auc"]) for row in group),
                "mean_unlearn_seconds": _mean(float(row["unlearn_seconds"]) for row in group),
                "mean_attack_total_seconds": _mean(float(row["attack_total_seconds"]) for row in group),
                "mean_selection_reuse_seconds": _mean(float(row["selection_reuse_seconds"]) for row in group),
                "failures": 0,
            }
        )
    return sorted(output, key=lambda row: (-float(row["mean_paired_delta_vs_random"]), str(row["selector"])))


def dataset_selector_summary(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for dataset in DATASETS:
        for selector in SELECTORS:
            group = [row for row in rows if row["dataset"] == dataset and row["selector"] == selector]
            _require(len(group) == 3, f"{dataset}/{selector}: expected three rows")
            output.append(
                {
                    "dataset": dataset,
                    "selector": selector,
                    "family": FAMILY[selector],
                    "mean_f1_drop": _mean(float(row["f1_drop"]) for row in group),
                    "mean_paired_delta_vs_random": _mean(float(row["paired_delta_vs_random"]) for row in group),
                    "mean_paired_delta_vs_degree": _mean(float(row["paired_delta_vs_degree"]) for row in group),
                    "mean_retrain_minus_unlearn_gap": _mean(float(row["retrain_minus_unlearn_gap"]) for row in group),
                    "mean_fraction_flipped": _mean(float(row["fraction_flipped"]) for row in group),
                }
            )
    return output


def pairwise_summary(
    rows: Sequence[Mapping[str, Any]],
    selected_sets: Mapping[Tuple[str, int, str], Tuple[int, ...]],
) -> List[Dict[str, Any]]:
    by_key = {(row["dataset"], row["seed"], row["selector"]): row for row in rows}
    output = []
    for left, right in KEY_PAIRS:
        differences = []
        identical = 0
        for dataset in DATASETS:
            for seed in SEEDS:
                differences.append(float(by_key[(dataset, seed, left)]["f1_drop"]) - float(by_key[(dataset, seed, right)]["f1_drop"]))
                identical += selected_sets[(dataset, seed, left)] == selected_sets[(dataset, seed, right)]
        wins, ties, losses = _wtl(differences)
        output.append(
            {
                "left_selector": left,
                "right_selector": right,
                "mean_f1_drop_difference_left_minus_right": _mean(differences),
                "sd_difference": _sample_sd(differences),
                "left_wins": wins,
                "ties": ties,
                "left_losses": losses,
                "identical_selected_sets": identical,
                "paired_cells": 9,
            }
        )
    return output


def load_selection_timing(manifest_path: Path, expected_sha256: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    actual_sha256 = _sha256(manifest_path)
    _require(actual_sha256 == expected_sha256, "Selection benchmark manifest SHA-256 mismatch")
    manifest = _read_json(manifest_path)
    _require(manifest.get("formal_score_names") == list(SELECTORS), "Selection selector list differs")
    cells = manifest.get("cells")
    _require(isinstance(cells, list) and len(cells) == 9, "Selection benchmark does not contain nine cells")
    per_selector: Dict[str, List[Mapping[str, Any]]] = {selector: [] for selector in SELECTORS}
    cold_bundle = []
    warm_bundle = []
    peak_allocated = []
    peak_reserved = []
    for cell in cells:
        _require(cell.get("status") == "success" and cell.get("failure") is None, "Selection cell failed")
        methods = cell.get("methods") or {}
        _require(set(methods) == set(SELECTORS), "Selection cell selector set differs")
        for selector in SELECTORS:
            method = methods[selector]
            _require(
                method.get("status") == "success"
                and method.get("failure") is None
                and method.get("cold_cache_hit") is False
                and method.get("warm_cache_hit") is True,
                f"Selection cold/warm contract failed for {selector}",
            )
            per_selector[selector].append(method)
        cold_bundle.append(_finite_number(cell.get("score_bundle_cold_total_seconds"), "cold bundle"))
        warm_bundle.append(_finite_number(cell.get("score_bundle_warm_read_seconds"), "warm bundle"))
        peak_allocated.append(int(cell.get("peak_gpu_allocated_bytes")))
        peak_reserved.append(int(cell.get("peak_gpu_reserved_bytes")))

    timing = []
    for selector in SELECTORS:
        group = per_selector[selector]
        timing.append(
            {
                "selector": selector,
                "family": FAMILY[selector],
                "mean_cold_selection_seconds": _mean(_finite_number(row.get("cold_selection_seconds"), selector) for row in group),
                "max_cold_selection_seconds": max(_finite_number(row.get("cold_selection_seconds"), selector) for row in group),
                "mean_warm_selection_seconds": _mean(_finite_number(row.get("warm_selection_seconds"), selector) for row in group),
                "max_warm_selection_seconds": max(_finite_number(row.get("warm_selection_seconds"), selector) for row in group),
                "successful_cold_miss_warm_hit_cells": len(group),
                "failures": 0,
            }
        )
    overview = {
        "manifest_path": str(manifest_path.resolve()),
        "manifest_sha256": actual_sha256,
        "cells": 9,
        "method_observations": 153,
        "failures": 0,
        "mean_score_bundle_cold_total_seconds": _mean(cold_bundle),
        "max_score_bundle_cold_total_seconds": max(cold_bundle),
        "mean_score_bundle_warm_read_seconds": _mean(warm_bundle),
        "max_score_bundle_warm_read_seconds": max(warm_bundle),
        "peak_gpu_allocated_bytes": max(peak_allocated),
        "peak_gpu_reserved_bytes": max(peak_reserved),
    }
    return timing, overview


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    _require(bool(rows), f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(
    run_root: Path,
    selection_manifest: Path,
    results_checksum_manifest: Path,
    output_dir: Path,
    expected_git_sha: str,
    expected_selection_manifest_sha256: str,
) -> Dict[str, Any]:
    checksum = verify_checksum_manifest(run_root, results_checksum_manifest)
    rows, selected_sets = load_matrix(run_root, expected_git_sha, expected_selection_manifest_sha256)
    add_paired_baselines(rows)
    selectors = selector_summary(rows)
    datasets = dataset_selector_summary(rows)
    pairs = pairwise_summary(rows, selected_sets)
    timing, timing_overview = load_selection_timing(selection_manifest, expected_selection_manifest_sha256)

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "cell_metrics.csv", rows)
    _write_csv(output_dir / "selector_summary.csv", selectors)
    _write_csv(output_dir / "dataset_selector_summary.csv", datasets)
    _write_csv(output_dir / "pairwise_summary.csv", pairs)
    _write_csv(output_dir / "selection_timing_summary.csv", timing)

    top = selectors[0]
    checkpoint_variants = [
        row for row in selectors if str(row["selector"]).startswith("tracin_cp_")
    ]
    best_checkpoint = max(
        checkpoint_variants,
        key=lambda row: float(row["mean_paired_delta_vs_random"]),
    )
    standard_tracin_variants = [
        row
        for row in checkpoint_variants
        if str(row["selector"]).startswith("tracin_cp_point_")
    ]
    best_standard_tracin = max(
        standard_tracin_variants,
        key=lambda row: float(row["mean_paired_delta_vs_random"]),
    )
    summary = {
        "schema": "opengu.small_selection_gu.aggregate.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "formal_run": {
            "run_root": str(run_root.resolve()),
            "git_sha": expected_git_sha,
            "datasets": list(DATASETS),
            "seeds": list(SEEDS),
            "selectors": list(SELECTORS),
            "selection_k": 7,
            "gu_method": "GNNDelete",
            "processed_profile": "planetoid_public_fixed",
            "cells": len(rows),
            "artifacts": len(rows) * len(ARTIFACT_NAMES),
            "failures": 0,
        },
        "checksum_verification": checksum,
        "selection_benchmark": timing_overview,
        "gu_inner_runtime": {
            "sum_unlearn_seconds": sum(float(row["unlearn_seconds"]) for row in rows),
            "mean_unlearn_seconds": _mean(float(row["unlearn_seconds"]) for row in rows),
            "max_unlearn_seconds": max(float(row["unlearn_seconds"]) for row in rows),
            "sum_attack_total_seconds": sum(float(row["attack_total_seconds"]) for row in rows),
            "mean_attack_total_seconds": _mean(float(row["attack_total_seconds"]) for row in rows),
            "max_attack_total_seconds": max(float(row["attack_total_seconds"]) for row in rows),
            "sum_selection_reuse_seconds": sum(float(row["selection_reuse_seconds"]) for row in rows),
            "mean_selection_reuse_seconds": _mean(float(row["selection_reuse_seconds"]) for row in rows),
            "max_selection_reuse_seconds": max(float(row["selection_reuse_seconds"]) for row in rows),
        },
        "descriptive_findings": {
            "top_selector_by_paired_delta_vs_random": top["selector"],
            "top_selector_mean_paired_delta_vs_random": top["mean_paired_delta_vs_random"],
            "best_checkpoint_variant": best_checkpoint["selector"],
            "best_checkpoint_variant_mean_paired_delta_vs_random": best_checkpoint[
                "mean_paired_delta_vs_random"
            ],
            "best_standard_tracin_selector": best_standard_tracin["selector"],
            "best_standard_tracin_mean_paired_delta_vs_random": best_standard_tracin[
                "mean_paired_delta_vs_random"
            ],
            "scope": "descriptive across three datasets and three seeds; not a universal significance claim",
        },
        "outputs": {
            "cell_metrics": "cell_metrics.csv",
            "selector_summary": "selector_summary.csv",
            "dataset_selector_summary": "dataset_selector_summary.csv",
            "pairwise_summary": "pairwise_summary.csv",
            "selection_timing_summary": "selection_timing_summary.csv",
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--selection-manifest", required=True, type=Path)
    parser.add_argument("--results-checksum-manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--expected-git-sha", required=True)
    parser.add_argument("--expected-selection-manifest-sha256", required=True)
    return parser


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary = aggregate(
            args.run_root.resolve(),
            args.selection_manifest.resolve(),
            args.results_checksum_manifest.resolve(),
            args.output_dir.resolve(),
            args.expected_git_sha,
            args.expected_selection_manifest_sha256,
        )
    except AggregationError as exc:
        print(f"small-selection GU aggregation failed: {exc}")
        return 1
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
