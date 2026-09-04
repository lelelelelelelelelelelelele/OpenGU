from __future__ import annotations

import datetime as dt
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from opengu_recipes import (
    TARGET_DIRECT_GU_ARTIFACT_NAMES,
    TARGET_DIRECT_STRATEGIES,
)


_SELECTION_PROFILES = {"target-direct-selection-v2"}
_GU_GATE_PROFILES = {"target-direct-gu-v2"}
_GU_STAGE_PROFILES = {"target-direct-gu-stage-v2"}
REVIEWED_PROFILES = _SELECTION_PROFILES | _GU_GATE_PROFILES | _GU_STAGE_PROFILES


def _now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_project_path(project_root: Path, value: Any) -> Path | None:
    text = str(value or "").replace("\\", "/")
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        return None
    root = project_root.resolve()
    candidate = (root / Path(*path.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _peer_evidence(
    definition: Mapping[str, Any],
    context: Mapping[str, Any],
    label: str,
) -> tuple[dict[str, Any], list[str], list[str], dict[str, Mapping[str, Any]], str | None]:
    node_id = str(context.get("node_id") or "")
    index = context.get("artifact_index") or {}
    peer = ((index.get("peers") or {}).get(node_id) or {}) if isinstance(index, Mapping) else {}
    errors: list[str] = []
    expected_paths = list(definition.get("expected_artifact_paths") or [])
    items = peer.get("items") or []
    by_remote = {
        str(item.get("remote_path") or item.get("path")): item
        for item in items
        if isinstance(item, Mapping) and (item.get("remote_path") or item.get("path"))
    }
    if (peer.get("summary") or {}).get("status") != "verified":
        errors.append(f"{label} artifact index is not verified")
    if set(by_remote) != set(expected_paths):
        errors.append(f"verified {label} artifact set differs from the reviewed recipe")
    observed_sha = ((peer.get("remote") or {}).get("git") or {}).get("sha")
    expected_sha = context.get("expected_git_sha")
    if expected_sha and observed_sha != expected_sha:
        errors.append(f"verified {label} artifact Git SHA differs from the dispatched SHA")
    return peer, errors, expected_paths, by_remote, observed_sha


def _selection_acceptance(
    definition: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    node_id = str(context.get("node_id") or "")
    expected_git_sha = context.get("expected_git_sha")
    project_root = Path(context.get("project_root") or Path.cwd())
    _, errors, expected_paths, by_remote, observed_sha = _peer_evidence(
        definition, context, "selection"
    )
    receipt_schema = str(definition.get("selection_receipt_schema") or "")
    if receipt_schema != "target_direct_v1.syncmate_selection_cell":
        errors.append("target-direct selection receipt schema is not declared")
    matrix = definition.get("selection_matrix") or {}
    expected_cells = {
        (dataset, int(seed))
        for dataset in matrix.get("datasets") or ()
        for seed in matrix.get("seeds") or ()
    }
    observed_cells: set[tuple[str, int]] = set()
    receipts: list[dict[str, Any]] = []
    for remote_path in sorted(path for path in expected_paths if path.endswith("/cell.json")):
        item = by_remote.get(remote_path) or {}
        local_path = _safe_project_path(project_root, item.get("local_path"))
        if local_path is None or not local_path.is_file():
            errors.append("verified cell receipt is missing locally: " + remote_path)
            continue
        try:
            receipt = json.loads(local_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid cell receipt {remote_path}: {exc}")
            continue
        if not isinstance(receipt, dict):
            errors.append("cell receipt root is not an object: " + remote_path)
            continue
        dataset, seed = receipt.get("dataset"), receipt.get("seed")
        if not isinstance(dataset, str) or not isinstance(seed, int):
            errors.append("cell receipt identity is invalid: " + remote_path)
            continue
        observed_cells.add((dataset, seed))
        if receipt.get("schema") != receipt_schema:
            errors.append("cell receipt schema mismatch: " + remote_path)
        if receipt.get("status") != "success" or receipt.get("formal_score_count") != 17:
            errors.append("cell receipt is not a successful 17-output result: " + remote_path)
        if expected_git_sha and receipt.get("experiment_git_sha") != expected_git_sha:
            errors.append("cell receipt Git SHA mismatch: " + remote_path)
        if "RTX 4090" not in str(receipt.get("device_name") or ""):
            errors.append("cell receipt is not from RTX 4090: " + remote_path)
        for field in ("peak_gpu_allocated_bytes", "peak_gpu_reserved_bytes"):
            if not isinstance(receipt.get(field), int) or receipt[field] <= 0:
                errors.append(f"cell receipt has no valid {field}: {remote_path}")
        parent = remote_path.rsplit("/", 1)[0]
        expected_ratios = tuple(float(value) for value in matrix.get("budget_ratios") or ())
        expected_k = matrix.get("expected_k_by_ratio") or {}
        ratio_results = receipt.get("ratio_results") or {}
        checkpoint = receipt.get("target_checkpoint") or {}
        if (
            receipt.get("version") != 2
            or receipt.get("parameter_scope") != matrix.get("parameter_scope")
            or receipt.get("candidate_count") != matrix.get("candidate_count")
            or tuple(float(value) for value in receipt.get("budget_ratios") or ()) != expected_ratios
            or receipt.get("expected_k_by_ratio") != expected_k
            or receipt.get("score_budget_semantics") != matrix.get("score_budget_semantics")
            or tuple(receipt.get("budget_conditioned_strategies") or ()) != tuple(matrix.get("budget_conditioned_strategies") or ())
            or not isinstance(receipt.get("score_bundle_cold_total_seconds"), (int, float))
            or not isinstance(receipt.get("score_bundle_warm_read_seconds"), dict)
            or not receipt.get("score_bundle_warm_read_seconds")
            or any(not isinstance(value, (int, float)) for value in (receipt.get("score_bundle_warm_read_seconds") or {}).values())
            or set(ratio_results) != {f"{ratio:.2f}" for ratio in expected_ratios}
            or not checkpoint.get("file_sha256")
            or not checkpoint.get("state_hash")
        ):
            errors.append("target-direct receipt timing/scope/checkpoint contract is incomplete: " + remote_path)
        for ratio in expected_ratios:
            ratio_key = f"{ratio:.2f}"
            ratio_result = ratio_results.get(ratio_key) or {}
            cold_methods = ratio_result.get("cold_method_timings") or {}
            warm_methods = ratio_result.get("warm_method_timings") or {}
            if (
                float(ratio_result.get("ratio", -1)) != ratio
                or ratio_result.get("k") != expected_k.get(ratio_key)
                or set(cold_methods) != set(TARGET_DIRECT_STRATEGIES)
                or set(warm_methods) != set(TARGET_DIRECT_STRATEGIES)
                or any(
                    item.get("status") != "success"
                    or item.get("cache_hit") is not False
                    or item.get("selection_projection_cache_hit") is not False
                    or not isinstance(item.get("cold_selection_projection_seconds"), (int, float))
                    for item in cold_methods.values()
                )
                or any(
                    item.get("status") != "success"
                    or item.get("cache_hit") is not True
                    or item.get("selection_projection_cache_hit") is not True
                    for item in warm_methods.values()
                )
                or (ratio_result.get("failure_state") or {}).get("state") != "success"
            ):
                errors.append("target-direct ratio projection contract is incomplete: " + ratio_key)
            for phase, hash_field in (("cold", "cold_sha256"), ("warm", "warm_sha256")):
                name = f"{phase}-r{ratio_key}.json"
                evidence = by_remote.get(parent + "/" + name) or {}
                local = _safe_project_path(project_root, evidence.get("local_path"))
                if local is None or not local.is_file() or _sha256(local) != ratio_result.get(hash_field):
                    errors.append(f"cell receipt does not bind verified {name}: {remote_path}")
        receipts.append(receipt)
    if observed_cells != expected_cells:
        errors.append("accepted cell matrix differs from the reviewed recipe")
    return {
        "generated_at": _now_iso(),
        "mode": "target-direct-selection-acceptance",
        "node_id": node_id, "recipe": definition.get("id"),
        "expected_git_sha": expected_git_sha, "observed_remote_git_sha": observed_sha,
        "expected_artifacts": len(expected_paths), "verified_artifacts": len(by_remote),
        "expected_cells": len(expected_cells), "accepted_cells": len(observed_cells),
        "receipts": receipts, "passed": not errors, "errors": errors,
    }


def _read_documents(
    expected_paths: list[str],
    by_remote: Mapping[str, Mapping[str, Any]],
    project_root: Path,
    errors: list[str],
    label: str,
) -> tuple[dict[str, Any], dict[str, Path]]:
    documents: dict[str, Any] = {}
    local_by_remote: dict[str, Path] = {}
    for remote_path in expected_paths:
        local = _safe_project_path(project_root, (by_remote.get(remote_path) or {}).get("local_path"))
        if local is None or not local.is_file():
            errors.append(f"verified {label} artifact is missing locally: {remote_path}")
            continue
        local_by_remote[remote_path] = local
        if remote_path.endswith(".json"):
            try:
                documents[remote_path.rsplit("/", 1)[-1]] = json.loads(local.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"invalid {label} JSON {remote_path}: {exc}")
    return documents, local_by_remote


def _gu_gate_acceptance(definition: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    node_id = str(context.get("node_id") or "")
    expected_git_sha = context.get("expected_git_sha")
    project_root = Path(context.get("project_root") or Path.cwd())
    _, errors, expected_paths, by_remote, observed_sha = _peer_evidence(definition, context, "GU")
    documents, _ = _read_documents(expected_paths, by_remote, project_root, errors, "GU")
    gate = definition.get("gu_gate") or {}
    target_direct = gate.get("lane") == "target_direct_white_box"
    if not target_direct:
        errors.append("GU gate is not the target-direct white-box lane")
    meta = documents.get("_meta.json") or {}
    artifact = meta.get("selection_artifact") or {}
    checkpoint = artifact.get("target_checkpoint") or {}
    if expected_git_sha and meta.get("git_sha") != expected_git_sha:
        errors.append("GU _meta Git SHA differs from the dispatched SHA")
    for field, expected in (("method", gate.get("gu_method")), ("strategy", gate.get("selector")), ("seed", gate.get("seed"))):
        if meta.get(field) != expected:
            errors.append(f"GU _meta {field} mismatch")
    if (
        artifact.get("strategy") != gate.get("selector")
        or artifact.get("ratio") != gate.get("ratio")
        or artifact.get("k") != gate.get("k")
        or artifact.get("authoritative") is not True
        or not artifact.get("artifact_id") or not artifact.get("recipe_hash") or not artifact.get("content_hash")
    ):
        errors.append("GU _meta Selection Artifact provenance is incomplete or changed")
    if target_direct:
        claims = ((meta.get("config") or {}).get("claims") or {})
        if (
            gate.get("parameter_scope") != "last_layer"
            or claims.get("parameter_scope") != "last_layer"
            or claims.get("deletion_ratio") != gate.get("ratio")
            or not checkpoint.get("state_hash") or not checkpoint.get("file_sha256")
        ):
            errors.append("GU gate target-direct checkpoint/scope provenance is incomplete")
    attack_row = ((documents.get("attack.json") or {}).get("results") or {}).get(gate.get("selector")) or {}
    if not attack_row or attack_row.get("failed") is True:
        errors.append("GU attack result is missing or failed")
    collateral_rows = [
        row for row in (documents.get("collateral.json") or {}).get("results") or []
        if row.get("strategy") == gate.get("selector")
    ]
    if len(collateral_rows) != 1:
        errors.append("GU collateral result has no unique selector row")
    return {
        "generated_at": _now_iso(),
        "mode": "target-direct-gu-acceptance",
        "node_id": node_id, "recipe": definition.get("id"),
        "expected_git_sha": expected_git_sha, "observed_remote_git_sha": observed_sha,
        "expected_artifacts": len(expected_paths), "verified_artifacts": len(by_remote),
        "gate": dict(gate), "selection_artifact_id": artifact.get("artifact_id"),
        "target_checkpoint_state_hash": checkpoint.get("state_hash"),
        "passed": not errors, "errors": errors,
    }


def _gu_stage_acceptance(definition: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    node_id = str(context.get("node_id") or "")
    expected_git_sha = context.get("expected_git_sha")
    project_root = Path(context.get("project_root") or Path.cwd())
    _, errors, expected_paths, by_remote, observed_sha = _peer_evidence(definition, context, "GU stage")
    _, local_by_remote = _read_documents(expected_paths, by_remote, project_root, errors, "GU stage")
    stage = definition.get("gu_stage") or {}
    target_direct = stage.get("lane") == "target_direct_white_box"
    selectors = tuple(stage.get("selectors") or ())
    accepted: list[dict[str, Any]] = []
    checkpoint_hashes: set[tuple[str, str]] = set()
    for selector in selectors:
        suffix = f"/GNNDelete_{selector}/seed{stage.get('seed')}"
        parents = {remote.rsplit("/", 1)[0] for remote in expected_paths if suffix in remote}
        if len(parents) != 1:
            errors.append("GU stage has no unique reviewed leaf: " + str(selector))
            continue
        parent = next(iter(parents))
        paths = {name: parent + "/" + name for name in TARGET_DIRECT_GU_ARTIFACT_NAMES}
        if any(remote not in local_by_remote for remote in paths.values()):
            continue
        try:
            attack = json.loads(local_by_remote[paths["attack.json"]].read_text(encoding="utf-8"))
            collateral = json.loads(local_by_remote[paths["collateral.json"]].read_text(encoding="utf-8"))
            meta = json.loads(local_by_remote[paths["_meta.json"]].read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid GU stage JSON for {selector}: {exc}")
            continue
        artifact = meta.get("selection_artifact") or {}
        checkpoint = artifact.get("target_checkpoint") or {}
        if expected_git_sha and meta.get("git_sha") != expected_git_sha:
            errors.append("GU stage _meta Git SHA mismatch: " + str(selector))
        if meta.get("method") != stage.get("gu_method") or meta.get("strategy") != selector or meta.get("seed") != stage.get("seed"):
            errors.append("GU stage _meta identity mismatch: " + str(selector))
        if (
            artifact.get("strategy") != selector
            or artifact.get("ratio") != stage.get("ratio")
            or artifact.get("k") != stage.get("k")
            or artifact.get("authoritative") is not True
            or not artifact.get("artifact_id") or not artifact.get("recipe_hash") or not artifact.get("content_hash")
        ):
            errors.append("GU stage Selection provenance mismatch: " + str(selector))
        if target_direct:
            claims = ((meta.get("config") or {}).get("claims") or {})
            state_hash, file_sha = checkpoint.get("state_hash"), checkpoint.get("file_sha256")
            if (
                stage.get("parameter_scope") != "last_layer"
                or claims.get("parameter_scope") != "last_layer"
                or claims.get("deletion_ratio") != stage.get("ratio")
                or not state_hash or not file_sha
            ):
                errors.append("GU stage target-direct checkpoint/scope provenance mismatch: " + str(selector))
            else:
                checkpoint_hashes.add((state_hash, file_sha))
        attack_row = (attack.get("results") or {}).get(selector) or {}
        if not attack_row or attack_row.get("failed") is True:
            errors.append("GU stage attack result is missing or failed: " + str(selector))
        collateral_rows = [row for row in collateral.get("results") or [] if row.get("strategy") == selector]
        if len(collateral_rows) != 1:
            errors.append("GU stage collateral row is missing or ambiguous: " + str(selector))
        try:
            with zipfile.ZipFile(local_by_remote[paths["predictions.npz"]]) as archive:
                if f"{selector}__selected_nodes.npy" not in archive.namelist():
                    errors.append("GU stage prediction identity is missing: " + str(selector))
        except Exception as exc:
            errors.append(f"invalid GU stage prediction bundle {selector}: {exc}")
        accepted.append({
            "selector": selector, "ratio": stage.get("ratio"),
            "selection_artifact_id": artifact.get("artifact_id"),
            "target_checkpoint_state_hash": checkpoint.get("state_hash"),
            "attack_total_seconds": attack_row.get("total_time"),
            "unlearn_seconds": attack_row.get("unlearn_time"),
            "selection_reuse_seconds": attack_row.get("selection_reuse_time"),
            "f1_drop": attack_row.get("f1_drop"),
            "collateral": collateral_rows[0] if len(collateral_rows) == 1 else None,
        })
    if len(accepted) != len(selectors):
        errors.append("accepted GU stage selector count differs from the reviewed recipe")
    if target_direct and len(checkpoint_hashes) != 1:
        errors.append("target-direct GU stage does not share one exact target checkpoint")
    return {
        "generated_at": _now_iso(),
        "mode": "target-direct-gu-stage-acceptance",
        "node_id": node_id, "recipe": definition.get("id"),
        "expected_git_sha": expected_git_sha, "observed_remote_git_sha": observed_sha,
        "expected_artifacts": len(expected_paths), "verified_artifacts": len(by_remote),
        "stage": dict(stage), "expected_cells": len(selectors),
        "accepted_cells": len(accepted), "cells": accepted,
        "passed": not errors, "errors": errors,
    }


def acceptance_payload(
    profile: str,
    definition: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    if profile not in REVIEWED_PROFILES:
        result = {"passed": False, "errors": ["OpenGU acceptance profile is not reviewed"]}
    elif profile in _SELECTION_PROFILES:
        result = _selection_acceptance(definition, context)
    elif profile in _GU_GATE_PROFILES:
        result = _gu_gate_acceptance(definition, context)
    else:
        result = _gu_stage_acceptance(definition, context)
    result = dict(result)
    result["owner"] = "opengu"
    result["profile"] = profile
    result["status"] = "accepted" if result.get("passed") is True else "rejected"
    return result
