import math
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REPORT_PATH = REPO_ROOT / "results" / "_journal" / "auto_report.md"
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
    "- 下一步建议：{next_step}\n\n"
)


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


def _default_next_step(status: str) -> str:
    if status == "SKIP":
        return "继续执行下一个未完成配置。"
    if status == "OK":
        return "检查该方法在其他比例或数据集的趋势。"
    if status == "TIMEOUT":
        return "提高超时阈值或先降低比例后再重试。"
    return "打开日志定位根因并重跑该配置。"


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
    "- 下一步建议：{next_step}\n\n"
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
    final_report_path = Path(report_path).resolve() if report_path else DEFAULT_REPORT_PATH
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

    suggestion = next_step or _default_next_step(normalized_status)
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
        next_step=suggestion,
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
    final_report_path = Path(report_path).resolve() if report_path else DEFAULT_REPORT_PATH
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

    suggestion = next_step or _default_next_step(normalized_status)
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
        next_step=suggestion,
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
    final_report_path = Path(report_path).resolve() if report_path else DEFAULT_REPORT_PATH
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
    lines.append("- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。\n")

    with final_report_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write("\n".join(lines))
    return str(final_report_path)
