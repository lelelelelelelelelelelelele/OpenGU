"""Adapt immutable B/C rankings into label-preserving GU Selection Artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

from cache_v2 import ProducerVersion
from cache_v2.runtime import load_selection_artifact
from experiments.bc_target_v2.recipe import SCORE_NAMES
from experiments.gu_target_v1.public_profile import PROFILE, verify_public_profile
from experiments.selection_budget_planner import materialize_budget_selection


EXTERNAL_SELECTION_MANIFEST_SCHEMA = "gu_target_v1.external_selection_manifest"
EXTERNAL_SELECTION_MANIFEST_VERSION = 1
ADAPTER_ALGORITHM_VERSION = "bc-target-public-ranking-to-opengu-gu-v1"
SAFE_LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,80}$")
DATASET_DISPLAY_NAMES = {
    "cora": "Cora",
    "citeseer": "CiteSeer",
    "pubmed": "PubMed",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_fingerprint(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        resolved = Path(path).resolve()
        digest.update(resolved.name.encode("utf-8") + b"\x00")
        digest.update(resolved.read_bytes())
    return digest.hexdigest()


def _read_json(path: Path, label: str) -> Dict[str, Any]:
    if not path.is_file():
        raise RuntimeError("{0} is missing: {1}".format(label, path))
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("{0} must contain one JSON object".format(label))
    return value


def _research_group(name: str) -> str:
    if name in {"random", "degree"}:
        return "controls"
    if name in {"a_grad_norm", "b_param_hutch"}:
        return "a_b"
    if name in {"r_point", "p_point", "tracin_cp_point_3", "tracin_cp_point_6"}:
        return "c_point"
    if name in {"gt_simple", "p_simple", "tracin_cp_simple_3", "tracin_cp_simple_6"}:
        return "c_simple"
    if name in {"gt_full", "p_graph", "tracin_cp_graph_3", "tracin_cp_graph_6"}:
        return "d_full"
    if name == "legacy":
        return "negative_control"
    return "external"


def materialize_grandfathered_selection(
    *,
    repository_root: Path,
    processed_root: Path,
    source_summary_path: Path,
    source_summary_sha256: str,
    benchmark_manifest_path: Path,
    benchmark_manifest_sha256: str,
    expected_experiment_git_sha: str,
    expected_public_source_fingerprint: str,
    dataset: str,
    seed: int,
    strategies: Sequence[str],
    k: int,
    base_model: str,
    gu_methods: Sequence[str],
    store_root: Path,
    manifest_path: Path,
) -> Dict[str, Any]:
    repository_root = Path(repository_root).resolve()
    processed_root = Path(processed_root).resolve()
    source_summary_path = Path(source_summary_path).resolve()
    benchmark_manifest_path = Path(benchmark_manifest_path).resolve()
    store_root = Path(store_root).resolve()
    manifest_path = Path(manifest_path).resolve()
    if manifest_path.exists() or store_root.exists():
        raise RuntimeError("cold GU adapter refuses to reuse its manifest or store root")
    if _sha256_file(source_summary_path) != source_summary_sha256:
        raise RuntimeError("grandfathered Selection summary SHA-256 mismatch")
    if _sha256_file(benchmark_manifest_path) != benchmark_manifest_sha256:
        raise RuntimeError("grandfathered benchmark manifest SHA-256 mismatch")
    summary = _read_json(source_summary_path, "Selection summary")
    benchmark = _read_json(benchmark_manifest_path, "benchmark manifest")
    if (
        summary.get("schema") != "bc_target_v2.selection_summary"
        or summary.get("version") != 2
        or summary.get("algorithm_version") != "bc-target-matrix-v3.0"
        or summary.get("dataset") != dataset
        or int(summary.get("seed", -1)) != int(seed)
        or (summary.get("status") or {}).get("state") != "success"
        or int(summary.get("candidate_count", -1)) <= 0
    ):
        raise RuntimeError("grandfathered Selection summary identity is invalid")
    if (
        benchmark.get("schema") != "bc_target_v2.small_graph_selection_benchmark"
        or benchmark.get("version") != 1
        or benchmark.get("experiment_git_sha") != expected_experiment_git_sha
    ):
        raise RuntimeError("grandfathered benchmark identity is invalid")
    matched_cells = [
        cell for cell in benchmark.get("cells") or []
        if cell.get("dataset") == dataset and int(cell.get("seed", -1)) == int(seed)
    ]
    if len(matched_cells) != 1 or matched_cells[0].get("status") != "success":
        raise RuntimeError("grandfathered benchmark has no unique successful source cell")

    profile = verify_public_profile(
        repository_root=repository_root,
        processed_root=processed_root,
        dataset=dataset,
    )
    observed_public_source = profile["manifest"]["dataset_source"][
        "source_fingerprint"
    ]
    if observed_public_source != expected_public_source_fingerprint:
        raise RuntimeError("canonical public dataset source fingerprint changed")
    inputs = profile["inputs"]
    if int(summary["candidate_count"]) != inputs.candidate_count:
        raise RuntimeError("Selection summary candidate count differs from public profile")
    rankings = summary.get("rankings")
    if not isinstance(rankings, dict) or set(rankings) != set(SCORE_NAMES):
        raise RuntimeError("Selection summary does not contain the exact 17-output grid")
    normalized_strategies = tuple(str(value) for value in strategies)
    if not normalized_strategies or len(set(normalized_strategies)) != len(normalized_strategies):
        raise RuntimeError("GU adapter strategies must be unique and non-empty")
    if set(normalized_strategies).difference(SCORE_NAMES):
        raise RuntimeError("GU adapter requested a strategy outside the 17-output grid")
    if k <= 0 or k > inputs.candidate_count:
        raise RuntimeError("GU adapter k is outside the candidate set")

    producer_version = ProducerVersion(
        semantic_version=ADAPTER_ALGORITHM_VERSION,
        source_fingerprint=_source_fingerprint(
            (Path(__file__), Path(__file__).parents[1] / "selection_budget_planner.py")
        ),
    )
    cells = []
    source_score_artifact_id = str((summary.get("cache") or {}).get("artifact_id") or "")
    if not source_score_artifact_id.startswith("score_"):
        raise RuntimeError("Selection summary has no valid source Score Artifact ID")
    for strategy in normalized_strategies:
        ranking = tuple(int(node) for node in rankings[strategy])
        if (
            len(ranking) != inputs.candidate_count
            or len(set(ranking)) != len(ranking)
            or set(ranking) != set(inputs.candidate_nodes)
        ):
            raise RuntimeError("ranking is not an exact candidate permutation: {0}".format(strategy))
        materialized = materialize_budget_selection(
            store_root=store_root,
            dataset=inputs,
            strategy=strategy,
            selector_seed=int(seed),
            budgets=(int(k),),
            producer_version=producer_version,
            algorithm_version=ADAPTER_ALGORITHM_VERSION,
            parameters={
                "prefix_stable": True,
                "score_name": strategy,
                "score_family": "bc_target_selection_score_bundle",
                "source_profile": "grandfathered-public-selection-gt-v1",
                "source_summary_sha256": source_summary_sha256,
                "benchmark_manifest_sha256": benchmark_manifest_sha256,
                "source_experiment_git_sha": expected_experiment_git_sha,
                "source_selector_model_final_state_hash": summary.get(
                    "selector_model_final_state_hash"
                ),
                "orientation": "score_desc_more_influential_or_harmful_if_removed",
                "ranking": "score_desc_node_id_asc",
            },
            source_score_artifact_id=source_score_artifact_id,
            producer=lambda max_k, ordered=ranking: ordered[:max_k],
        )
        artifact = materialized.to_manifest(store_root)
        cells.append(
            {
                "strategy": strategy,
                "research_group": _research_group(strategy),
                "seed": int(seed),
                "k": int(k),
                "artifact": artifact["artifact"],
                "selected_nodes": artifact["views"][str(int(k))]["selected_nodes"],
            }
        )
    manifest = {
        "schema": EXTERNAL_SELECTION_MANIFEST_SCHEMA,
        "version": EXTERNAL_SELECTION_MANIFEST_VERSION,
        "dataset": dataset.lower(),
        "base_model": base_model,
        "processed_profile": PROFILE,
        "gu_methods": list(gu_methods),
        "strategies": list(normalized_strategies),
        "seeds": [int(seed)],
        "k": int(k),
        "store_root": str(store_root),
        "processed_profile_manifest": profile["manifest_path"],
        "selection_identity": dict(profile["manifest"]["selection_identity"]),
        "source": {
            "profile": "grandfathered-public-selection-gt-v1",
            "selection_summary_path": str(source_summary_path),
            "selection_summary_sha256": source_summary_sha256,
            "benchmark_manifest_path": str(benchmark_manifest_path),
            "benchmark_manifest_sha256": benchmark_manifest_sha256,
            "experiment_git_sha": expected_experiment_git_sha,
            "canonical_public_source_fingerprint": expected_public_source_fingerprint,
            "score_artifact_id": source_score_artifact_id,
            "selector_model_final_state_hash": summary.get(
                "selector_model_final_state_hash"
            ),
        },
        "cells": cells,
        "claims": {
            "lane": "controlled_public_profile_gu",
            "canonical_opengu_80_20": False,
            "selection_timing_authority": "grandfathered GT",
            "gu_outcome_authority": "this manifest and downstream cells",
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def load_external_selection_manifest(
    cfg: Mapping[str, Any],
    *,
    manifest_path: Path,
    expected_store_root: Path,
    processed_root: Path,
) -> Tuple[Dict[Tuple[str, int], Dict[str, Any]], Dict[str, Any]]:
    manifest_path = Path(manifest_path).resolve()
    manifest = _read_json(manifest_path, "external Selection manifest")
    if (
        manifest.get("schema") != EXTERNAL_SELECTION_MANIFEST_SCHEMA
        or manifest.get("version") != EXTERNAL_SELECTION_MANIFEST_VERSION
    ):
        raise ValueError("external Selection manifest schema/version mismatch")
    expected = {
        "dataset": str(cfg["dataset"]).lower(),
        "base_model": str(cfg["base_model"]),
        "processed_profile": str(cfg.get("processed_profile") or ""),
        "gu_methods": list(cfg["methods"]),
        "strategies": list(cfg["strategies"]),
        "seeds": [int(value) for value in cfg["seeds"]],
    }
    for field, value in expected.items():
        if manifest.get(field) != value:
            raise ValueError("external Selection manifest {0} mismatch".format(field))
    store_root = Path(str(manifest.get("store_root") or "")).resolve()
    if store_root != Path(expected_store_root).resolve():
        raise ValueError("external Selection store root differs from runner config")
    profile = verify_public_profile(
        repository_root=Path(__file__).resolve().parents[2],
        processed_root=Path(processed_root),
        dataset=DATASET_DISPLAY_NAMES.get(
            str(cfg["dataset"]).lower(), str(cfg["dataset"])
        ),
    )
    inputs = profile["inputs"]
    if manifest.get("selection_identity") != profile["manifest"]["selection_identity"]:
        raise ValueError("external Selection manifest dataset identity changed")
    mapping: Dict[Tuple[str, int], Dict[str, Any]] = {}
    for cell in manifest.get("cells") or []:
        strategy = str(cell.get("strategy") or "")
        seed = int(cell.get("seed"))
        k = int(cell.get("k"))
        if SAFE_LABEL_RE.fullmatch(strategy) is None:
            raise ValueError("external Selection manifest strategy label is unsafe")
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
            raise ValueError("external Selection Artifact identity changed")
        key = (strategy, seed)
        if key in mapping:
            raise ValueError("external Selection manifest contains duplicate cells")
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
            "k": k,
            "selected_node_count": len(loaded.selected_nodes),
            "research_group": cell.get("research_group"),
            "source_selection": dict(manifest.get("source") or {}),
            "external_selection_manifest": str(manifest_path),
        }
    expected_keys = {
        (str(strategy), int(seed))
        for strategy in cfg["strategies"]
        for seed in cfg["seeds"]
    }
    if set(mapping) != expected_keys:
        raise ValueError("external Selection manifest matrix is incomplete")
    return mapping, {
        "mode": "external_selection",
        "manifest_path": str(manifest_path),
        "writes": [],
        "cells": len(mapping),
        "source": manifest.get("source"),
    }
