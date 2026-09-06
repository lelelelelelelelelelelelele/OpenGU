from __future__ import annotations

import copy
import datetime as dt
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from syncmate_core.index import export_payload_from_index
from syncmate_core.context import use as project_context


STRATEGY_NAMES = ("random", "degree", "pagerank", "tracin", "im", "hybrid")
OPENGU_ARTIFACT_NAMES = ("attack.json", "collateral.json", "_meta.json")


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


def _split_cell_name(cell: Any) -> tuple[str, str, str]:
    text = str(cell or "")
    head = text
    ratio = ""
    marker = text.rfind("_r")
    if marker >= 0:
        head = text[:marker]
        ratio = text[marker + 2:]
    dataset, sep, base_model = head.rpartition("_")
    if not sep:
        dataset = head
        base_model = ""
    return dataset, base_model, ratio


def _split_method_strategy_name(method_strategy: Any) -> tuple[str, str, str]:
    text = str(method_strategy or "")
    for strategy in sorted(STRATEGY_NAMES, key=len, reverse=True):
        token = f"_{strategy}"
        idx = text.find(token)
        if idx <= 0:
            continue
        tail = text[idx + len(token):]
        if tail and not tail.startswith("_"):
            continue
        return text[:idx], strategy, strategy + tail
    method, sep, strategy_full = text.rpartition("_")
    if sep and method and strategy_full:
        return method, strategy_full, strategy_full
    return text or "unknown", "unknown", "unknown"


def _read_json(
    project_root: Path,
    leaf: Mapping[str, Any],
    artifact_name: str,
) -> tuple[dict[str, Any] | None, str | None]:
    artifact = (leaf.get("artifacts") or {}).get(artifact_name) or {}
    local_path = artifact.get("local_path")
    if not local_path:
        return None, f"{artifact_name} missing from trusted leaf"
    target = _safe_project_path(project_root, local_path)
    if target is None:
        return None, f"{artifact_name} has unsafe local_path: {local_path!r}"
    if not target.is_file():
        return None, f"{artifact_name} local file missing: {local_path}"
    try:
        data = json.loads(target.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        return None, f"{artifact_name} unreadable json: {type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, f"{artifact_name} json root is not an object"
    return data, None


def _attack_entries(
    data: dict[str, Any] | None,
    fallback_strategy: str,
) -> tuple[list[tuple[str, dict[str, Any]]], list[str]]:
    if not data:
        return [(fallback_strategy, {})], ["attack.json missing or unreadable"]
    results = data.get("results")
    entries: list[tuple[str, dict[str, Any]]] = []
    errors: list[str] = []
    if isinstance(results, dict):
        for key, value in sorted(results.items(), key=lambda pair: str(pair[0])):
            if isinstance(value, dict):
                entries.append((str(key), value))
            else:
                errors.append(f"attack result {key!r} is not an object")
    elif isinstance(results, list):
        for idx, value in enumerate(results):
            if not isinstance(value, dict):
                errors.append(f"attack result #{idx} is not an object")
                continue
            key = value.get("strategy") or value.get("strategy_name") or fallback_strategy
            entries.append((str(key), value))
    else:
        errors.append("attack.json has no results object")
    if not entries:
        entries.append((fallback_strategy, {}))
    return entries, errors


def _collateral_rows(
    data: dict[str, Any] | None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any], list[str]]:
    if not data:
        return {}, {}, ["collateral.json missing or unreadable"]
    raw = data.get("results")
    if isinstance(raw, dict):
        rows = [value for value in raw.values() if isinstance(value, dict)]
    elif isinstance(raw, list):
        rows = [value for value in raw if isinstance(value, dict)]
    else:
        return {}, {}, ["collateral.json has no results list"]
    if not rows:
        return {}, {}, ["collateral.json results[] empty"]
    by_strategy: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = row.get("strategy") or row.get("strategy_name")
        if key:
            by_strategy[str(key)] = row
    return by_strategy, rows[0], []


def _collateral_fields(row: Mapping[str, Any]) -> dict[str, Any]:
    output = {
        "perf_before": row.get("perf_before"),
        "perf_unlearn": row.get("perf_unlearn"),
        "perf_retrain": row.get("perf_retrain"),
        "drop_retrain": row.get("drop_retrain"),
        "gap": row.get("gap"),
        "gap_pct": row.get("gap_pct"),
        "mean_pred_shift": row.get("mean_pred_shift"),
        "max_pred_shift": row.get("max_pred_shift"),
        "fraction_flipped": row.get("fraction_flipped"),
    }
    hop = row.get("hop_decay") or {}
    if isinstance(hop, dict):
        for label, key in (("1", "1_hop"), ("2", "2_hop"), ("3", "3_hop"), ("gt3", "gt3_hop")):
            output[f"hop_{label}_flip_rate"] = hop.get(f"{key}_flip_rate")
            output[f"hop_{label}_count"] = hop.get(f"{key}_count")
    return output


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _with_opengu_policy(index: Mapping[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy(dict(index))
    for peer in (data.get("peers") or {}).values():
        if not isinstance(peer, dict):
            continue
        policy = peer.setdefault("artifact_policy", {})
        if not policy.get("include"):
            policy["include"] = list(OPENGU_ARTIFACT_NAMES)
    return data


def results_payload(
    index: Mapping[str, Any],
    options: Mapping[str, Any],
) -> dict[str, Any]:
    project_root = Path(options.get("project_root") or Path.cwd()).resolve()
    node_ids = options.get("node_ids")
    include_incomplete = bool(options.get("include_incomplete"))
    data = _with_opengu_policy(index)
    with project_context(project_root):
        trusted = export_payload_from_index(
            data,
            node_ids=list(node_ids) if node_ids is not None else None,
            include_incomplete=include_incomplete,
        )
    rows: list[dict[str, Any]] = []
    parse_errors: list[dict[str, Any]] = []

    for leaf in trusted.get("leaves") or []:
        if 'summary.json' in (leaf.get('artifacts') or {}) and 'attack.json' not in (leaf.get('artifacts') or {}):
            continue
        if ("output-references.json" in (leaf.get("artifacts") or {})
                or "target_direct_formal_v2/gu/" in str(leaf.get("remote_leaf") or "")):
            from opengu_method_output import read_method_output
            dataset, base_model, ratio = _split_cell_name(leaf.get("cell"))
            row = {"node_id": leaf.get("node_id"), "cell": leaf.get("cell"),
                "dataset": dataset, "base_model": base_model, "ratio": ratio,
                "method_strategy": leaf.get("method_strategy"), "seed": leaf.get("seed"),
                "layout": leaf.get("layout"), "complete": bool(leaf.get("complete")),
                "local_leaf": leaf.get("local_leaf"), "remote_leaf": leaf.get("remote_leaf"),
                "source_report": leaf.get("source_report"), "comparison_stage": "deferred"}
            try:
                if not leaf.get('complete'):
                    raise ValueError('collected method leaf is incomplete')
                read = read_method_output(leaf.get("artifacts") or {}, project_root)
                meta, result = read['meta'], read['result']
                row.update(method=meta['method'], strategy=meta['strategy'], strategy_full=meta['strategy'],
                    git_sha=meta['git_sha'][:7], output=read['output'], evaluation=read['evaluation'],
                    f1_after=result['f1_after'], f1_drop=result['f1_drop'],
                    selected_n=len(result['selected_nodes']), compute_seconds=result['compute_seconds'],
                    cache_hit=result['cache_hit'], status='ok', parse_errors=[])
            except Exception as exc:
                error = f'{type(exc).__name__}: {exc}'
                row.update(status='parse-error', parse_errors=[error])
                parse_errors.append({'node_id': leaf.get('node_id'), 'local_leaf': leaf.get('local_leaf'),
                                     'error': error})
            rows.append(row)
            continue
        method, directory_strategy, strategy_full = _split_method_strategy_name(leaf.get("method_strategy"))
        dataset, base_model, ratio = _split_cell_name(leaf.get("cell"))
        leaf_errors = [f"missing artifact: {name}" for name in (leaf.get("missing") or [])]
        attack, attack_error = _read_json(project_root, leaf, "attack.json")
        collateral, collateral_error = _read_json(project_root, leaf, "collateral.json")
        meta, meta_error = _read_json(project_root, leaf, "_meta.json")
        leaf_errors.extend(error for error in (attack_error, collateral_error, meta_error) if error)
        attack_entries, attack_errors = _attack_entries(attack, directory_strategy)
        collateral_by_strategy, collateral_default, collateral_errors = _collateral_rows(collateral)
        leaf_errors.extend(attack_errors)
        leaf_errors.extend(collateral_errors)
        meta_fields = {
            "git_sha": str((meta or {}).get("git_sha") or "")[:7] or None,
            "hostname": (meta or {}).get("hostname"),
            "timestamp": (meta or {}).get("timestamp"),
        }
        artifacts = leaf.get("artifacts") or {}
        shas = {
            "attack_sha256": (artifacts.get("attack.json") or {}).get("sha256"),
            "collateral_sha256": (artifacts.get("collateral.json") or {}).get("sha256"),
            "meta_sha256": (artifacts.get("_meta.json") or {}).get("sha256"),
        }
        for strategy_key, attack_result in attack_entries:
            result_strategy = str(strategy_key or directory_strategy)
            strategy = result_strategy if result_strategy in STRATEGY_NAMES else directory_strategy
            collateral_row = (
                collateral_by_strategy.get(result_strategy)
                or collateral_by_strategy.get(strategy)
                or collateral_by_strategy.get(strategy_full)
                or collateral_default
            )
            collateral_fields = _collateral_fields(collateral_row)
            f1_after = attack_result.get("f1_after")
            f1_drop = None
            if _numeric(f1_after) is not None and _numeric(collateral_fields.get("perf_before")) is not None:
                f1_drop = _numeric(collateral_fields["perf_before"]) - _numeric(f1_after)
            selected_nodes = attack_result.get("selected_nodes")
            row_errors = list(leaf_errors)
            status = "ok" if leaf.get("complete") and not row_errors else "incomplete" if not leaf.get("complete") else "parse-error"
            row = {
                "node_id": leaf.get("node_id"), "complete": bool(leaf.get("complete")),
                "cell": leaf.get("cell"), "dataset": dataset, "base_model": base_model,
                "ratio": ratio, "method": method, "strategy": strategy,
                "strategy_full": strategy_full, "method_strategy": leaf.get("method_strategy"),
                "seed": leaf.get("seed"), "layout": leaf.get("layout"),
                "f1_after": f1_after, "f1_drop": f1_drop,
                "mia_auc": attack_result.get("mia_auc"),
                "unlearn_time": attack_result.get("unlearn_time"),
                "selection_time": attack_result.get("selection_time"),
                "selection_cache_hit": attack_result.get("selection_cache_hit"),
                "selected_n": len(selected_nodes) if isinstance(selected_nodes, list) else None,
                **collateral_fields, **meta_fields, **shas,
                "local_leaf": leaf.get("local_leaf"), "remote_leaf": leaf.get("remote_leaf"),
                "source_report": leaf.get("source_report"), "status": status,
                "parse_errors": row_errors,
            }
            rows.append(row)
            parse_errors.extend({
                "node_id": leaf.get("node_id"), "local_leaf": leaf.get("local_leaf"),
                "strategy": strategy, "error": error,
            } for error in row_errors)

    rows.sort(key=lambda item: (
        str(item.get("node_id") or ""), str(item.get("cell") or ""),
        str(item.get("method") or ""), str(item.get("strategy_full") or ""),
        str(item.get("seed") or ""),
    ))
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": "results", "owner": "opengu",
        "index_path": data.get("index_path") or ".syncmate/artifact_index.json",
        "include_incomplete": include_incomplete,
        "requested_peers": sorted(set(node_ids or [])),
        "summary": {
            "peers": len({row.get("node_id") for row in rows}),
            "leaves": (trusted.get("summary") or {}).get("leaves", 0),
            "rows": len(rows),
            "complete_leaves": (trusted.get("summary") or {}).get("complete_leaves", 0),
            "incomplete_leaves": (trusted.get("summary") or {}).get("incomplete_leaves", 0),
            "skipped_incomplete": (trusted.get("summary") or {}).get("skipped_incomplete", 0),
            "parse_error_rows": sum(1 for row in rows if row.get("parse_errors")),
            "parse_errors": len(parse_errors),
        },
        "rows": rows, "parse_errors": parse_errors,
        "errors": trusted.get("errors") or [],
        "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
    }
