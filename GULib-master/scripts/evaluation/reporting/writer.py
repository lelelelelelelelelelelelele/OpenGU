import math
import os
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from .events import (
    ENV_ATTEMPT,
    ENV_CELL_ID,
    ENV_CONFIG_FINGERPRINT,
    ENV_GIT_SHA,
    ENV_RUN_ID,
    artifact_ref,
    cache_observation,
    current_git_sha,
    event_path_from_env,
    make_cell_id,
    make_config_fingerprint,
    new_run_id,
    record_event,
    refresh_status_views,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
REPORT_STYLE_VERSION = "v1"
STATUS_SET = {"OK", "X", "TIMEOUT", "WARN", "SKIP"}
REPORT_HEADER = (
    "# 自动实验汇报（追加）\n\n"
    f"- report_style_version = {REPORT_STYLE_VERSION}\n"
    "- 写入策略：append-only\n\n"
)
ENTRY_TEMPLATE = (
    "### [{timestamp}] {script}\n"
    "- 任务：dataset={dataset}, model={model}, method={method}, ratio={ratio}\n"
    "- 日志路径：`{log_file}`\n"
    "- 执行结果：{status} | f1_before={f1_before} | f1_after={f1_after} | auc={auc} | "
    "unlearn_time={unlearn_time} | wall_time={wall_time}s\n"
    "- 异常与定位：{error_summary}\n"
    "{next_step_line}\n"
)


class LegacyReportWriteDisabledError(RuntimeError):
    """Raised when retired v1 writers are called without an explicit fixture path."""


def _legacy_report_path(report_path: Optional[str]) -> Path:
    if not report_path:
        raise LegacyReportWriteDisabledError(
            "The default v1 Markdown writer is retired. Use AutoReport V3 events, "
            "or pass report_path explicitly for a compatibility fixture/export."
        )
    warnings.warn(
        "AutoReport v1 Markdown writers are deprecated; use V3 events.",
        DeprecationWarning,
        stacklevel=3,
    )
    return Path(report_path).resolve()


def _fmt_metric(value: Optional[float], digits: int = 4) -> str:
    if value is None:
        return "NA"
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(as_float):
        return "NaN"
    return f"{as_float:.{digits}f}"


def _normalize_status(status: str) -> Tuple[str, Optional[str]]:
    normalized = str(status or "").strip().upper()
    if normalized in STATUS_SET:
        return normalized, None
    return "WARN", normalized or "EMPTY"


def _compose_error_summary(error_type: Optional[str], error_msg: Optional[str]) -> str:
    if error_type:
        return f"{error_type}: {error_msg or 'NA'}"
    if error_msg:
        return str(error_msg)
    return "无"


COLLATERAL_TEMPLATE = (
    "### [{timestamp}] eval_collateral.py\n"
    "- 任务：dataset={dataset}, model={model}, method={method}, ratio={ratio}\n"
    "- 策略结果：\n"
    "{strategy_table}\n"
    "- 日志路径：`{log_file}`\n"
    "- 执行结果：{status}\n"
    "- 异常与定位：{error_summary}\n"
    "{next_step_line}\n"
)


def _build_strategy_table(results: list) -> str:
    lines = [
        "| Strategy | Gap% | MeanShift | Flipped% |",
        "|----------|------|-----------|----------|",
    ]
    for result in results:
        gap_pct = _fmt_metric(result.get("gap_pct"), digits=2) + "%"
        mean_shift = _fmt_metric(result.get("mean_pred_shift"), digits=4)
        flipped = _fmt_metric(
            result.get("fraction_flipped", 0) * 100 if result.get("fraction_flipped") is not None else None,
            digits=2,
        ) + "%"
        lines.append(f"| {result.get('strategy', '?'):<8} | {gap_pct:>4} | {mean_shift:>9} | {flipped:>8} |")
    return "\n".join(lines)


def append_collateral_entry(
    dataset: str,
    model: str,
    method: str,
    ratio: str,
    results: list,
    log_file: str,
    status: str = "OK",
    error_type: Optional[str] = None,
    error_msg: Optional[str] = None,
    next_step: Optional[str] = None,
    report_path: Optional[str] = None,
) -> str:
    final_report_path = _legacy_report_path(report_path)
    final_report_path.parent.mkdir(parents=True, exist_ok=True)
    if not final_report_path.exists():
        final_report_path.write_text(REPORT_HEADER, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalized_status, invalid_status = _normalize_status(status)
    final_error_type = error_type
    final_error_msg = error_msg
    if invalid_status:
        prefix = f"Invalid status input: {invalid_status}; normalized to WARN."
        final_error_type = final_error_type or "INVALID_STATUS"
        final_error_msg = f"{prefix} {final_error_msg}" if final_error_msg else prefix

    strategy_table = _build_strategy_table(results) if results else "（无策略结果）"
    entry = COLLATERAL_TEMPLATE.format(
        timestamp=now,
        dataset=dataset,
        model=model,
        method=method,
        ratio=ratio,
        strategy_table=strategy_table,
        log_file=log_file,
        status=normalized_status,
        error_summary=_compose_error_summary(final_error_type, final_error_msg),
        next_step_line="- 下一步建议：{0}".format(next_step) if next_step else "",
    )
    with final_report_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write(entry)
    return str(final_report_path)


def append_report_entry(
    script: str,
    dataset: str,
    model: str,
    method: str,
    ratio: str,
    status: str,
    log_file: str,
    f1_before: Optional[float] = None,
    f1_after: Optional[float] = None,
    unlearn_time: Optional[float] = None,
    auc: Optional[float] = None,
    time_s: Optional[float] = None,
    error_type: Optional[str] = None,
    error_msg: Optional[str] = None,
    next_step: Optional[str] = None,
    report_path: Optional[str] = None,
) -> str:
    final_report_path = _legacy_report_path(report_path)
    final_report_path.parent.mkdir(parents=True, exist_ok=True)
    if not final_report_path.exists():
        final_report_path.write_text(REPORT_HEADER, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalized_status, invalid_status = _normalize_status(status)
    final_error_type = error_type
    final_error_msg = error_msg
    if invalid_status:
        prefix = f"Invalid status input: {invalid_status}; normalized to WARN."
        final_error_type = final_error_type or "INVALID_STATUS"
        final_error_msg = f"{prefix} {final_error_msg}" if final_error_msg else prefix

    entry = ENTRY_TEMPLATE.format(
        timestamp=now,
        script=script,
        dataset=dataset,
        model=model,
        method=method,
        ratio=ratio,
        log_file=log_file,
        status=normalized_status,
        f1_before=_fmt_metric(f1_before),
        f1_after=_fmt_metric(f1_after),
        auc=_fmt_metric(auc),
        unlearn_time=_fmt_metric(unlearn_time),
        wall_time=_fmt_metric(time_s, digits=2),
        error_summary=_compose_error_summary(final_error_type, final_error_msg),
        next_step_line="- 下一步建议：{0}".format(next_step) if next_step else "",
    )
    with final_report_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write(entry)
    return str(final_report_path)


def append_attack_result(
    method: str,
    dataset: str,
    model: str,
    strategies: list,
    unlearn_ratio: float,
    k: int,
    seed: int,
    results,
    report_path: Optional[str] = None,
) -> str:
    final_report_path = _legacy_report_path(report_path)
    final_report_path.parent.mkdir(parents=True, exist_ok=True)
    if not final_report_path.exists():
        final_report_path.write_text(REPORT_HEADER, encoding="utf-8")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"\n### [{now}] demo_attack.py - {method} 攻击实验",
        f"- 任务：dataset={dataset}, model={model}, method={method}, strategies={strategies}, ratio={unlearn_ratio}",
        f"- 配置：unlearn_ratio={unlearn_ratio} ({k} nodes), seed={seed}",
        "- 执行结果：",
    ]
    for result in results:
        name = getattr(result, "strategy_name", "?")
        f1_drop = getattr(result, "f1_drop", None)
        f1_before = getattr(result, "f1_before", None)
        f1_after = getattr(result, "f1_after", None)
        total_time = getattr(result, "total_time", None)
        selection_cache_hit = getattr(result, "selection_cache_hit", None)
        selection_time = getattr(result, "selection_time", None)
        selection_reuse_time = getattr(result, "selection_reuse_time", None)
        selection_cache_key = getattr(result, "selection_cache_key", None)

        cache_parts = []
        if selection_cache_hit is True:
            cache_parts.append(f"cache=HIT(key={selection_cache_key or 'NA'})")
            cache_parts.append(f"selection={_fmt_metric(selection_time, digits=4)}s")
            cache_parts.append(f"reuse={_fmt_metric(selection_reuse_time, digits=6)}s")
            if selection_time is not None and selection_reuse_time is not None and float(selection_reuse_time) > 0:
                speedup = float(selection_time) / float(selection_reuse_time)
                cache_parts.append(f"speedup={_fmt_metric(speedup, digits=2)}x")
        elif selection_cache_hit is False:
            cache_parts.append("cache=MISS")
            cache_parts.append(f"selection={_fmt_metric(selection_time, digits=4)}s")
        else:
            cache_parts.append("cache=NA")

        lines.append(
            f"  - {name}: F1 Drop = {_fmt_metric(f1_drop)} "
            f"(f1_before={_fmt_metric(f1_before)}, f1_after={_fmt_metric(f1_after)}, "
            f"time={_fmt_metric(total_time, digits=1)}s, {', '.join(cache_parts)})"
        )
    lines.append("- 异常与定位：无")
    lines.append("")

    with final_report_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write("\n".join(lines))
    return str(final_report_path)


# ---------------------------------------------------------------------------
# AutoReport V3 event writers
# ---------------------------------------------------------------------------


def _attempt_from_env() -> int:
    try:
        return max(1, int(os.environ.get(ENV_ATTEMPT, "1")))
    except (TypeError, ValueError):
        return 1


def _runtime_context(identity: Mapping[str, Any], config_payload: Mapping[str, Any], single_cell: bool):
    derived_cell_id = make_cell_id(identity)
    cell_id = os.environ.get(ENV_CELL_ID) if single_cell else None
    cell_id = cell_id or derived_cell_id
    run_id = os.environ.get(ENV_RUN_ID) or new_run_id(cell_id)
    config_fingerprint = os.environ.get(ENV_CONFIG_FINGERPRINT) or make_config_fingerprint(
        config_payload
    )
    git_sha = os.environ.get(ENV_GIT_SHA) or current_git_sha()
    return cell_id, run_id, config_fingerprint, git_sha, _attempt_from_env()


def record_evaluation_result(
    *,
    script: str,
    dataset: str,
    model: str,
    method: str,
    ratio: str,
    status: str,
    log_file: str,
    f1_before: Optional[float] = None,
    f1_after: Optional[float] = None,
    unlearn_time: Optional[float] = None,
    auc: Optional[float] = None,
    time_s: Optional[float] = None,
    error_type: Optional[str] = None,
    error_msg: Optional[str] = None,
    event_path: Optional[str] = None,
) -> str:
    """Record old evaluation-runner results as V3 facts, without prose advice."""
    normalized_status, invalid_status = _normalize_status(status)
    identity = {
        "dataset": dataset,
        "model": model,
        "method": method,
        "strategy": None,
        "ratio": ratio,
        "seed": None,
        "k": None,
    }
    payload = {"identity": identity, "producer": script}
    cell_id, run_id, config_fingerprint, git_sha, attempt = _runtime_context(
        identity, payload, True
    )
    state = {
        "OK": "completed",
        "SKIP": "skipped",
        "X": "failed",
        "TIMEOUT": "failed",
        "WARN": "completed",
    }[normalized_status]
    artifacts = []
    log_artifact = _artifact_from_path(log_file, "log")
    if log_artifact:
        artifacts.append(log_artifact)
    cache_values = []
    if normalized_status == "SKIP":
        hit_source = log_file or "legacy_strict_ok_log"
        cache_values.append(
            cache_observation(
                cache_type="run_artifact",
                outcome="hit",
                recipe={"legacy_gate": "strict_ok_log"},
                artifact=log_artifact,
                hit_source=hit_source,
                lookup_policy="legacy_strict_ok_log",
                authoritative=False,
                write_outcome="reused",
            )
        )
    error = None
    if state == "failed":
        error = {
            "type": error_type or normalized_status,
            "message": error_msg or "Legacy evaluation runner failed.",
            "retryable": True,
        }
    metadata = {
        "legacy_status": normalized_status,
        "reason": "strict OK legacy log exists" if normalized_status == "SKIP" else None,
    }
    if invalid_status:
        metadata["invalid_status_input"] = invalid_status
    if normalized_status == "WARN" and (error_type or error_msg):
        metadata["warning"] = _compose_error_summary(error_type, error_msg)
    record_event(
        identity=identity,
        stage="run",
        state=state,
        producer=script,
        config_fingerprint=config_fingerprint,
        git_sha=git_sha,
        cell_id=cell_id,
        run_id=run_id,
        attempt=attempt,
        cache=cache_values,
        artifacts=artifacts,
        metrics={
            "f1_before": f1_before,
            "f1_after": f1_after,
            "unlearn_time": unlearn_time,
            "auc": auc,
            "wall_time_s": time_s,
        },
        error=error,
        metadata=metadata,
        event_path=event_path,
    )
    return str(event_path_from_env(event_path))


def _artifact_from_path(path: Optional[str], artifact_type: str) -> Optional[Dict[str, Any]]:
    if not path:
        return None
    return artifact_ref(path=path, artifact_type=artifact_type)


def _selected_node_count(result) -> Optional[int]:
    selected_nodes = getattr(result, "selected_nodes", None)
    if selected_nodes is None:
        return None
    try:
        return int(len(selected_nodes))
    except (TypeError, ValueError):
        return None


def _selection_cache_observation(result, *, strategy: str, k: int, cache_enabled: bool):
    artifact_id = getattr(result, "selection_artifact_id", None)
    if artifact_id:
        source = getattr(result, "selection_cache_source", None)
        recipe_hash = getattr(result, "selection_recipe_hash", None)
        content_hash = getattr(result, "selection_content_hash", None)
        lookup_mode = (
            getattr(result, "selection_cache_lookup_mode", None)
            or "cache_v2_exact_artifact_id"
        )
        return cache_observation(
            cache_type="selection",
            outcome="hit",
            recipe={"strategy": strategy, "k": int(k)},
            recipe_hash=recipe_hash,
            artifact=artifact_ref(
                path=source,
                artifact_id=str(artifact_id),
                artifact_type="selection",
                recipe_hash=recipe_hash,
                content_hash=content_hash,
            ),
            hit_source="cache_v2:{0}".format(artifact_id),
            lookup_policy=lookup_mode,
            authoritative=True,
            write_outcome="reused",
        )
    cache_hit = getattr(result, "selection_cache_hit", None)
    source = getattr(result, "selection_cache_source", None)
    cache_key = getattr(result, "selection_cache_key", None)
    lookup_mode = getattr(result, "selection_cache_lookup_mode", None) or "legacy_exact_key"
    source_k = getattr(result, "selection_cache_source_k", None)
    recipe = {"strategy": strategy, "k": int(k)}
    if source_k is not None:
        recipe["source_k"] = int(source_k)
    if cache_key:
        recipe["legacy_cache_key"] = str(cache_key)
    if not cache_enabled:
        outcome = "bypass"
        write_outcome = "not_written"
    elif cache_hit is True:
        outcome = "hit"
        write_outcome = "reused"
    elif cache_hit is False:
        outcome = "miss"
        write_outcome = "saved" if source else "unknown"
    else:
        outcome = "unknown"
        write_outcome = "unknown"
    hit_source = source if outcome == "hit" else None
    if outcome == "hit" and not hit_source:
        hit_source = "legacy_selection_cache:{0}".format(cache_key or "unknown")
    return cache_observation(
        cache_type="selection",
        outcome=outcome,
        recipe=recipe,
        artifact=_artifact_from_path(source, "selection"),
        hit_source=hit_source,
        lookup_policy=lookup_mode,
        authoritative=False,
        write_outcome=write_outcome,
        miss_reason="no matching selection entry" if outcome == "miss" else None,
    )


def _result_cache_observation(result, *, strategy: str, k: int, cache_enabled: bool):
    cache_hit = getattr(result, "result_cache_hit", None)
    source = getattr(result, "result_cache_source", None)
    cache_key = getattr(result, "result_cache_key", None)
    lookup_mode = getattr(result, "result_cache_lookup_mode", None) or "legacy_hash_or_fallback"
    recipe = {"strategy": strategy, "k": int(k)}
    if cache_key:
        recipe["legacy_cache_key"] = str(cache_key)
    if not cache_enabled:
        outcome = "bypass"
        write_outcome = "not_written"
    elif cache_hit is True:
        outcome = "hit"
        write_outcome = "reused"
    elif cache_hit is False:
        outcome = "miss"
        write_outcome = "saved" if source else "unknown"
    else:
        outcome = "unknown"
        write_outcome = "unknown"
    hit_source = source if outcome == "hit" else None
    if outcome == "hit" and not hit_source:
        hit_source = "legacy_result_cache:{0}".format(cache_key or "unknown")
    return cache_observation(
        cache_type="result",
        outcome=outcome,
        recipe=recipe,
        artifact=_artifact_from_path(source, "evaluation"),
        hit_source=hit_source,
        lookup_policy=lookup_mode,
        authoritative=False,
        write_outcome=write_outcome,
        miss_reason="no matching result entry" if outcome == "miss" else None,
    )


def record_attack_results(
    *,
    method: str,
    dataset: str,
    model: str,
    strategies: Sequence[str],
    unlearn_ratio: float,
    k: int,
    seed: int,
    results: Sequence[Any],
    save_path: Optional[str] = None,
    cache_enabled: bool = True,
    event_path: Optional[str] = None,
) -> str:
    """Record selection/attack terminal events without appending Markdown noise."""
    result_values = list(results)
    single_cell = len(result_values) == 1
    if not result_values:
        identity = {
            "dataset": dataset,
            "model": model,
            "method": method,
            "strategy": strategies[0] if len(strategies) == 1 else None,
            "ratio": unlearn_ratio,
            "seed": int(seed),
            "k": int(k),
        }
        config_payload = {
            "identity": identity,
            "strategies_requested": list(strategies),
            "cache_enabled": bool(cache_enabled),
        }
        cell_id, run_id, config_fingerprint, git_sha, attempt = _runtime_context(
            identity, config_payload, len(strategies) == 1
        )
        record_event(
            identity=identity,
            stage="attack",
            state="failed",
            producer="demo_attack.py",
            config_fingerprint=config_fingerprint,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            error={
                "type": "NO_ATTACK_RESULT",
                "message": "No attack result was produced.",
                "retryable": True,
            },
            event_path=event_path,
        )
        return str(event_path_from_env(event_path))
    wrote_any = False
    for result in result_values:
        strategy = str(getattr(result, "strategy_name", "") or "unknown")
        identity = {
            "dataset": dataset,
            "model": model,
            "method": method,
            "strategy": strategy,
            "ratio": unlearn_ratio,
            "seed": int(seed),
            "k": int(k),
        }
        config_payload = {
            "identity": identity,
            "strategies_requested": list(strategies),
            "cache_enabled": bool(cache_enabled),
        }
        cell_id, run_id, config_fingerprint, git_sha, attempt = _runtime_context(
            identity, config_payload, single_cell
        )

        # A whole ResultCache hit means selection did not run in this process;
        # never replay the cached result's historical selection_cache_hit as a
        # current selection HIT.
        result_cache_hit = getattr(result, "result_cache_hit", None)
        if result_cache_hit is not True:
            selection_result = record_event(
                identity=identity,
                stage="selection",
                state="completed",
                producer="demo_attack.py",
                config_fingerprint=config_fingerprint,
                git_sha=git_sha,
                cell_id=cell_id,
                run_id=run_id,
                attempt=attempt,
                cache=[
                    _selection_cache_observation(
                        result, strategy=strategy, k=k, cache_enabled=cache_enabled
                    )
                ],
                metrics={
                    "selection_time_s": getattr(result, "selection_time", None),
                    "selection_reuse_time_s": getattr(result, "selection_reuse_time", None),
                    "selected_node_count": _selected_node_count(result),
                },
                event_path=event_path,
                refresh=False,
            )
            wrote_any = wrote_any or selection_result.written

        attack_artifacts = []
        if save_path:
            attack_artifacts.append(artifact_ref(path=save_path, artifact_type="evaluation"))
        failed = bool(getattr(result, "failed", False))
        failure_reason = getattr(result, "failure_reason", None)
        attack_result = record_event(
            identity=identity,
            stage="attack",
            state="failed" if failed else "completed",
            producer="demo_attack.py",
            config_fingerprint=config_fingerprint,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            cache=[_result_cache_observation(result, strategy=strategy, k=k, cache_enabled=cache_enabled)],
            artifacts=attack_artifacts,
            metrics={
                "f1_before": getattr(result, "f1_before", None),
                "f1_after": getattr(result, "f1_after", None),
                "f1_drop": getattr(result, "f1_drop", None),
                "unlearn_time_s": getattr(result, "unlearn_time", None),
                "total_time_s": getattr(result, "total_time", None),
                "mia_auc": getattr(result, "mia_auc", None),
            },
            error=(
                {
                    "type": "ATTACK_FAILED",
                    "message": failure_reason or "Attack pipeline reported failure.",
                    "retryable": True,
                }
                if failed
                else None
            ),
            event_path=event_path,
            refresh=False,
        )
        wrote_any = wrote_any or attack_result.written

    resolved_path = event_path_from_env(event_path)
    if result_values or wrote_any:
        refresh_status_views(event_path=resolved_path)
    return str(resolved_path)


def _collateral_cache_observation(strategy: str, provenance: Optional[Mapping[str, Any]]):
    info = dict(provenance or {})
    artifact_id = info.get("artifact_id")
    if artifact_id:
        source = info.get("source_file")
        return cache_observation(
            cache_type="selection",
            outcome=str(info.get("outcome") or "hit"),
            recipe=dict(info.get("recipe") or {"strategy": strategy}),
            recipe_hash=info.get("recipe_hash"),
            artifact=artifact_ref(
                path=source,
                artifact_id=str(artifact_id),
                artifact_type="selection",
                recipe_hash=info.get("recipe_hash"),
                content_hash=info.get("content_hash"),
            ),
            hit_source=info.get("hit_source") or "cache_v2:{0}".format(artifact_id),
            lookup_policy=info.get("lookup_policy") or "cache_v2_exact_artifact_id",
            authoritative=info.get("authoritative") is True,
            write_outcome=info.get("write_outcome") or "reused",
            miss_reason=info.get("miss_reason"),
        )
    outcome = str(info.get("outcome") or "unknown")
    source = info.get("source_file")
    cache_key = info.get("cache_key")
    hit_source = source if outcome == "hit" else None
    if outcome == "hit" and not hit_source:
        hit_source = "legacy_result_cache:{0}".format(cache_key or "unknown")
    recipe = dict(info.get("recipe") or {"strategy": strategy})
    if cache_key:
        recipe["legacy_cache_key"] = str(cache_key)
    return cache_observation(
        cache_type="result",
        outcome=outcome,
        recipe=recipe,
        artifact=_artifact_from_path(source, "evaluation"),
        hit_source=hit_source,
        lookup_policy=info.get("lookup_policy") or "legacy_hash_or_scan",
        authoritative=False,
        write_outcome="reused" if outcome == "hit" else "not_written",
        miss_reason=info.get("miss_reason"),
    )


def record_collateral_results(
    *,
    dataset: str,
    model: str,
    method: str,
    ratio: float,
    seed: Optional[int],
    results: Sequence[Mapping[str, Any]],
    output_path: str,
    cache_provenance: Optional[Mapping[str, Mapping[str, Any]]] = None,
    requested_strategies: Optional[Sequence[str]] = None,
    error_type: Optional[str] = None,
    error_msg: Optional[str] = None,
    event_path: Optional[str] = None,
) -> str:
    result_values = list(results)
    requested = [str(item) for item in (requested_strategies or [])]
    successful = {str(item.get("strategy") or "unknown") for item in result_values}
    missing_strategies = [strategy for strategy in requested if strategy not in successful]
    single_cell = len(requested or result_values) <= 1
    provenance_by_strategy = dict(cache_provenance or {})
    if not result_values:
        missing_strategies = requested or [None]

    for missing_strategy in missing_strategies:
        identity = {
            "dataset": dataset,
            "model": model,
            "method": method,
            "strategy": missing_strategy,
            "ratio": ratio,
            "seed": seed,
            "k": None,
        }
        payload = {"identity": identity, "output_path": output_path}
        cell_id, run_id, config_fingerprint, git_sha, attempt = _runtime_context(
            identity, payload, single_cell
        )
        cache_values = []
        if missing_strategy is not None:
            cache_values.append(
                _collateral_cache_observation(
                    str(missing_strategy), provenance_by_strategy.get(str(missing_strategy))
                )
            )
        record_event(
            identity=identity,
            stage="collateral",
            state="failed",
            producer="eval_collateral.py",
            config_fingerprint=config_fingerprint,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            cache=cache_values,
            error={
                "type": error_type or "NO_RESULT",
                "message": error_msg or "No collateral result was produced.",
                "retryable": True,
            },
            event_path=event_path,
            refresh=False,
        )
    if not result_values:
        refresh_status_views(event_path=event_path_from_env(event_path))
        return str(event_path_from_env(event_path))

    for result in result_values:
        strategy = str(result.get("strategy") or "unknown")
        identity = {
            "dataset": dataset,
            "model": model,
            "method": method,
            "strategy": strategy,
            "ratio": ratio,
            "seed": seed,
            "k": None,
        }
        payload = {"identity": identity, "output_path": output_path}
        cell_id, run_id, config_fingerprint, git_sha, attempt = _runtime_context(
            identity, payload, single_cell
        )
        record_event(
            identity=identity,
            stage="collateral",
            state="completed",
            producer="eval_collateral.py",
            config_fingerprint=config_fingerprint,
            git_sha=git_sha,
            cell_id=cell_id,
            run_id=run_id,
            attempt=attempt,
            cache=[_collateral_cache_observation(strategy, provenance_by_strategy.get(strategy))],
            artifacts=[artifact_ref(path=output_path, artifact_type="evaluation")],
            metrics={
                "gap": result.get("gap"),
                "gap_pct": result.get("gap_pct"),
                "mean_pred_shift": result.get("mean_pred_shift"),
                "max_pred_shift": result.get("max_pred_shift"),
                "fraction_flipped": result.get("fraction_flipped"),
            },
            event_path=event_path,
            refresh=False,
        )
    refresh_status_views(event_path=event_path_from_env(event_path))
    return str(event_path_from_env(event_path))
