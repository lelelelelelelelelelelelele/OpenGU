from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
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
    if len(by_remote) != len(items):
        errors.append(f"{label} artifact index contains duplicate or invalid paths")
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
            receipt.get("version") != 3
            or set(receipt.get("method_score_identities") or {}) != set(TARGET_DIRECT_STRATEGIES)
            or any(not isinstance(item, dict) or not item.get('artifact_id')
                   or not isinstance(item.get('recipe_hash'), str) or len(item['recipe_hash']) != 64
                   or any(c not in '0123456789abcdef' for c in item['recipe_hash'])
                   for item in (receipt.get('method_score_identities') or {}).values())
            or receipt.get("parameter_scope") != matrix.get("parameter_scope")
            or receipt.get("candidate_count") != matrix.get("candidate_count")
            or tuple(float(value) for value in receipt.get("budget_ratios") or ()) != expected_ratios
            or receipt.get("expected_k_by_ratio") != expected_k
            or receipt.get("score_budget_semantics") != matrix.get("score_budget_semantics")
            or tuple(receipt.get("budget_conditioned_strategies") or ()) != tuple(matrix.get("budget_conditioned_strategies") or ())
            or type(receipt.get("method_scores_cold_total_seconds")) not in (int, float)
            or not math.isfinite(receipt.get("method_scores_cold_total_seconds", -1))
            or receipt.get("method_scores_cold_total_seconds", -1) < 0
            or not isinstance(receipt.get("method_scores_warm_read_seconds"), dict)
            or not receipt.get("method_scores_warm_read_seconds")
            or any(type(value) not in (int, float) or not math.isfinite(value) or value < 0
                   for value in (receipt.get("method_scores_warm_read_seconds") or {}).values())
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


def _gu_acceptance(definition: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    from opengu_method_output import read_method_output
    from cache_v2.contracts import validate_sha256, validate_artifact_id

    is_gate = "gu_gate" in definition
    scope = definition.get("gu_gate" if is_gate else "gu_stage") or {}
    selectors = (scope.get("selector"),) if is_gate else tuple(scope.get("selectors") or ())
    methods = tuple(scope.get("gu_methods") or ())
    project_root = Path(context.get("project_root") or Path.cwd())
    expected_sha = context.get("expected_git_sha")
    _, errors, expected_paths, by_remote, observed_sha = _peer_evidence(definition, context, "GU")
    if not isinstance(expected_sha, str) or len(expected_sha) != 40 or any(c not in '0123456789abcdef' for c in expected_sha):
        errors.append("GU acceptance requires the full dispatched Git SHA")
    if scope.get("lane") != "target_direct_white_box" or scope.get("parameter_scope") != "last_layer":
        errors.append("GU recipe is not the reviewed target-direct scope")
    if not methods or len(set(methods)) != len(methods) or not selectors or len(set(selectors)) != len(selectors):
        errors.append("GU recipe needs unique methods and selectors")
    if len(by_remote) != len(expected_paths):
        errors.append("GU evidence has duplicate or missing artifacts")
    accepted = []
    checkpoints = set()
    selections = {}
    pairings = {}
    reviewed_paths = set()
    for method in methods:
        for selector in selectors:
            label = str(method) + '/' + str(selector)
            parent = (f"results/runs/target_direct_formal_v2/gu/{scope['stage'].rsplit('-seed', 1)[0]}"
                      f"_{scope['base_model']}_r{scope['ratio']:.2f}/{method}_{selector}/seed{scope['seed']}")
            paths = {name: parent + '/' + name for name in TARGET_DIRECT_GU_ARTIFACT_NAMES}
            reviewed_paths.update(paths.values())
            try:
                read = read_method_output({name: by_remote.get(remote) for name, remote in paths.items()}, project_root)
                meta, result, payload = read['meta'], read['result'], read['payload']
                artifact = meta['selection_artifact']
                checkpoint = artifact.get('target_checkpoint') or {}
                if any(meta.get(key) != value for key, value in
                       (('git_sha', expected_sha), ('method', method), ('strategy', selector), ('seed', scope['seed']))):
                    raise ValueError('GU metadata differs from dispatched cell identity')
                validate_sha256(meta.get('config_fingerprint'), 'configuration fingerprint')
                if meta.get('fingerprint_version') != 'v5-single-method-output' or meta.get('comparison_stage') != 'deferred':
                    raise ValueError('GU metadata does not declare independent method outputs')
                if any(artifact.get(key) != value for key, value in
                       (('strategy', selector), ('ratio', scope['ratio']), ('k', scope['k']), ('authoritative', True))):
                    raise ValueError('Selection provenance differs from reviewed cell')
                validate_artifact_id(artifact.get('artifact_id'))
                for field in ('recipe_hash', 'content_hash'):
                    validate_sha256(artifact.get(field), 'Selection ' + field)
                for field in ('state_hash', 'file_sha256'):
                    validate_sha256(checkpoint.get(field), 'target checkpoint ' + field)
                pairing = payload.identity['pairing']
                instance = scope['method_instances'][method]
                if (any(pairing[key] != instance[key] for key in ('model', 'training', 'deletion'))
                        or payload.identity['target']['parameters'] != instance['parameters']):
                    raise ValueError('method conditions differ from reviewed configuration')
                if (len(payload.arrays['selected_nodes']) != scope['k']
                        or int(payload.arrays['train_mask'].sum()) != scope['candidate_count']
                        or pairing['training']['seed'] != scope['seed']
                        or pairing['model']['architecture'] != 'OpenGU.GCNNet'):
                    raise ValueError('saved input, request or model differs from reviewed cell')
                selection = payload.identity['selection']
                if selector in selections and selections[selector] != selection:
                    raise ValueError('methods did not consume the same Selection')
                if selector in pairings and pairings[selector] != pairing:
                    raise ValueError('methods do not share Dataset/Split, request and training conditions')
                selections[selector], pairings[selector] = selection, pairing
                checkpoints.add((checkpoint['state_hash'], checkpoint['file_sha256']))
                accepted.append({'method': method, 'selector': selector, 'ratio': scope['ratio'],
                    'selection_artifact_id': artifact['artifact_id'],
                    'target_checkpoint_state_hash': checkpoint['state_hash'],
                    'output': read['output'], 'evaluation': read['evaluation'],
                    'f1_after': result['f1_after'], 'f1_drop': result['f1_drop'],
                    'compute_seconds': result['compute_seconds']})
            except Exception as exc:
                errors.append(f'{label}: {type(exc).__name__}: {exc}')
    if reviewed_paths != set(expected_paths):
        errors.append('GU recipe artifact declaration differs from its method/selector cells')
    if len(accepted) != len(methods) * len(selectors):
        errors.append('accepted GU method count differs from the reviewed recipe')
    if len(checkpoints) != 1:
        errors.append('target-direct GU stage does not share one exact Selection checkpoint')
    return {
        'generated_at': _now_iso(),
        'mode': 'target-direct-gu-acceptance' if is_gate else 'target-direct-gu-stage-acceptance',
        'node_id': context.get('node_id'), 'recipe': definition.get('id'),
        'expected_git_sha': expected_sha, 'observed_remote_git_sha': observed_sha,
        'expected_artifacts': len(expected_paths), 'verified_artifacts': len(by_remote),
        'gate' if is_gate else 'stage': dict(scope),
        'expected_cells': len(methods) * len(selectors), 'accepted_cells': len(accepted), 'cells': accepted,
        'target_checkpoint_state_hash': next(iter(checkpoints))[0] if len(checkpoints) == 1 else None,
        'comparison_stage': 'deferred', 'passed': not errors, 'errors': errors,
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
    else:
        result = _gu_acceptance(definition, context)
    result = dict(result)
    result["owner"] = "opengu"
    result["profile"] = profile
    result["status"] = "accepted" if result.get("passed") is True else "rejected"
    return result
