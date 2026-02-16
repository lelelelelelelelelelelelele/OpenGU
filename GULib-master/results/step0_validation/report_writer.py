import math
import os
from datetime import datetime
from typing import Optional


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT_PATH = os.path.join(THIS_DIR, "..", "_journal", "auto_report.md")


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
    final_report_path = os.path.abspath(report_path or DEFAULT_REPORT_PATH)
    os.makedirs(os.path.dirname(final_report_path), exist_ok=True)
    if not os.path.exists(final_report_path):
        with open(final_report_path, "w", encoding="utf-8") as file_obj:
            file_obj.write("# 自动实验汇报（追加）\n\n")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    suggestion = next_step or _default_next_step(status)
    error_summary = f"{error_type}: {error_msg}" if error_type else (error_msg or "无")
    entry = (
        f"### [{now}] {script}\n"
        f"- 任务：dataset={dataset}, model={model}, method={method}, ratio={ratio}\n"
        f"- 日志路径：`{log_file}`\n"
        f"- 执行结果：{status} | f1_before={_fmt_metric(f1_before)} | f1_after={_fmt_metric(f1_after)} | "
        f"auc={_fmt_metric(auc)} | unlearn_time={_fmt_metric(unlearn_time)} | wall_time={_fmt_metric(time_s, digits=2)}s\n"
        f"- 异常与定位：{error_summary}\n"
        f"- 下一步建议：{suggestion}\n\n"
    )
    with open(final_report_path, "a", encoding="utf-8") as file_obj:
        file_obj.write(entry)
    return final_report_path
