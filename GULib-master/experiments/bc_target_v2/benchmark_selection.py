"""Run the complete small-graph cold/warm selection benchmark matrix."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from .recipe import ALGORITHM_VERSION, SCORE_NAMES
from .render_markdown import render_document


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = Path("E:/project/OpenGU/GULib-master/data/raw/Planetoid")
DEFAULT_CACHE_ROOT = (
    REPO_ROOT / "results" / "cache_v2" / "bc_target_v3_benchmark_20260721"
)
DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "results" / "bc_target_v2" / "selection_benchmark_20260721"
)
DEFAULT_REPORT_MD = REPO_ROOT / "reports" / "small_graph_selection_BENCHMARK_REPORT.md"
DEFAULT_REPORT_HTML = (
    REPO_ROOT / "reports" / "small_graph_selection_BENCHMARK_REPORT.html"
)
BENCHMARK_SCHEMA = "bc_target_v2.small_graph_selection_benchmark"
BENCHMARK_VERSION = 1


def _names(value: str) -> Tuple[str, ...]:
    result = tuple(item.strip() for item in str(value).split(",") if item.strip())
    if not result or len(set(result)) != len(result):
        raise argparse.ArgumentTypeError("expected unique comma-separated names")
    allowed = {"Cora", "CiteSeer", "PubMed"}
    if any(item not in allowed for item in result):
        raise argparse.ArgumentTypeError("datasets must be Cora, CiteSeer, or PubMed")
    return result


def _integers(value: str) -> Tuple[int, ...]:
    try:
        result = tuple(int(item.strip()) for item in str(value).split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if not result or len(set(result)) != len(result) or any(item < 0 for item in result):
        raise argparse.ArgumentTypeError("expected unique non-negative integers")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--report-html", type=Path, default=DEFAULT_REPORT_HTML)
    parser.add_argument(
        "--datasets", type=_names, default=("Cora", "CiteSeer", "PubMed")
    )
    parser.add_argument("--seeds", type=_integers, default=(42, 212, 2024))
    parser.add_argument("--budgets", default="14,7,3")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--resume", action="store_true")
    return parser


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True
    ).encode("utf-8")
    temporary = path.with_name(path.name + ".tmp-{0}".format(os.getpid()))
    temporary.write_bytes(payload)
    os.replace(str(temporary), str(path))


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object: {0}".format(path))
    return value


def _run(command: Sequence[str], timeout_seconds: float) -> Mapping[str, Any]:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=float(timeout_seconds),
            check=False,
        )
        return {
            "returncode": int(completed.returncode),
            "elapsed_seconds": time.perf_counter() - started,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": None,
            "elapsed_seconds": time.perf_counter() - started,
            "stdout_tail": (exc.stdout or "")[-4000:],
            "stderr_tail": (exc.stderr or "")[-4000:],
            "timed_out": True,
        }


def _command(
    *,
    dataset: str,
    seed: int,
    data_root: Path,
    cache_root: Path,
    output: Path,
    budgets: str,
    device: str,
    warm: bool,
) -> Tuple[str, ...]:
    result = [
        sys.executable,
        "-m",
        "experiments.bc_target_v2.run_selection",
        "--dataset",
        dataset,
        "--seed",
        str(seed),
        "--data-root",
        str(data_root),
        "--cache-root",
        str(cache_root),
        "--output",
        str(output),
        "--overwrite-output",
        "--budgets",
        budgets,
        "--device",
        device,
    ]
    if warm:
        result.append("--fail-if-producer-called")
    return tuple(result)


def _method_timings(summary: Mapping[str, Any]) -> Mapping[str, Any]:
    value = summary.get("selection_cache", {}).get("method_timings", {})
    if set(value) != set(SCORE_NAMES):
        raise ValueError("selection timings do not contain the frozen 17 methods")
    return value


def _build_cell_record(
    *,
    dataset: str,
    seed: int,
    cold_path: Path,
    warm_path: Path,
    cold: Mapping[str, Any],
    warm: Mapping[str, Any],
) -> Mapping[str, Any]:
    cold_methods = _method_timings(cold)
    warm_methods = _method_timings(warm)
    if cold.get("cache", {}).get("hit") is not False:
        raise ValueError("cold ScoreBundle access was not a cache miss")
    if warm.get("cache", {}).get("hit") is not True:
        raise ValueError("warm ScoreBundle access was not an exact hit")
    if int(cold.get("selection_cache", {}).get("miss_saved_count", -1)) != len(
        SCORE_NAMES
    ):
        raise ValueError("cold run did not materialize all 17 Selection Artifacts")
    if int(warm.get("selection_cache", {}).get("hit_count", -1)) != len(SCORE_NAMES):
        raise ValueError("warm run did not hit all 17 Selection Artifacts")
    methods = {}
    for name in SCORE_NAMES:
        methods[name] = {
            "cold_selection_seconds": float(cold_methods[name]["seconds"]),
            "cold_cache_hit": bool(cold_methods[name]["cache_hit"]),
            "warm_selection_seconds": float(warm_methods[name]["seconds"]),
            "warm_cache_hit": bool(warm_methods[name]["cache_hit"]),
            "status": "success",
            "failure": None,
        }
    return {
        "dataset": dataset,
        "seed": int(seed),
        "status": "success",
        "failure": None,
        "cold_summary_path": str(cold_path),
        "warm_summary_path": str(warm_path),
        "score_bundle_cold_total_seconds": float(
            cold["runtime"]["score_bundle_cold_total_seconds"]
        ),
        "score_bundle_warm_read_seconds": float(
            warm["runtime"]["score_bundle_warm_read_seconds"]
        ),
        "cold_total_process_seconds": float(cold["runtime"]["total_seconds"]),
        "warm_total_process_seconds": float(warm["runtime"]["total_seconds"]),
        "peak_gpu_allocated_bytes": cold["gpu_memory"][
            "process_peak_allocated_bytes"
        ],
        "peak_gpu_reserved_bytes": cold["gpu_memory"]["process_peak_reserved_bytes"],
        "device": cold["environment"]["device"],
        "score_artifact_id": cold["cache"]["artifact_id"],
        "methods": methods,
    }


def _failure_record(dataset: str, seed: int, stage: str, detail: Any) -> Mapping[str, Any]:
    return {
        "dataset": dataset,
        "seed": int(seed),
        "status": "failed",
        "failure": {"stage": stage, "detail": detail},
        "methods": {
            name: {
                "cold_selection_seconds": None,
                "cold_cache_hit": None,
                "warm_selection_seconds": None,
                "warm_cache_hit": None,
                "status": "failed",
                "failure": stage,
            }
            for name in SCORE_NAMES
        },
    }


def _fmt_seconds(value: Optional[float]) -> str:
    return "—" if value is None else "{0:.4f}".format(float(value))


def _fmt_mib(value: Optional[int]) -> str:
    return "N/A" if value is None else "{0:.1f}".format(int(value) / (1024 ** 2))


def _render_report(document: Mapping[str, Any], md_path: Path, html_path: Path) -> None:
    cells = list(document["cells"])
    passed = [cell for cell in cells if cell["status"] == "success"]
    failed = [cell for cell in cells if cell["status"] != "success"]
    gpu_cells = [cell for cell in passed if cell.get("peak_gpu_allocated_bytes") is not None]
    if failed:
        verdict = "FAIL — {0}/{1} cells failed".format(len(failed), len(cells))
        badge = "FAILED"
    elif len(passed) != len(cells):
        verdict = "INCOMPLETE — matrix has unfinished cells"
        badge = "INCOMPLETE"
    elif not gpu_cells:
        verdict = "CPU PASS — full matrix complete; GPU VRAM evidence pending"
        badge = "CPU PASS · GPU PENDING"
    else:
        verdict = "PASS — full cold/warm matrix and GPU telemetry complete"
        badge = "ACCEPTED"

    lines = [
        "# 小图 Selection 全量实测报告",
        "",
        "> **Verdict:** {0}".format(verdict),
        "",
        "## 1. 实测口径",
        "",
        "- 正式矩阵：`Cora/CiteSeer/PubMed × seeds 42/212/2024`，共 {0} cells。".format(
            len(cells)
        ),
        "- 正式 ScoreBundle 固定为 **17 个 score/ranking 输出**；`b_param_lissa` 仅是历史数值验证项，不进入本轮 bundle。",
        "- cold method time：共享 ScoreBundle 已生成后，每个 ranking 首次物化 max-k Selection Artifact 的完整冷路径。",
        "- cold ScoreBundle total：exact miss lookup、共享计算、17 输出构造、校验和落盘的总时间。",
        "- warm read：同一 recipe 在 producer-call sentinel 下的 exact ScoreBundle 读取时间；17 个 Selection Artifact 也必须全部命中。",
        "",
        "## 2. Cell 总览",
        "",
        "| Dataset | Seed | Status | Device | Cold bundle (s) | Warm read (s) | Peak alloc (MiB) | Peak reserve (MiB) | Failure |",
        "|---|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for cell in cells:
        failure = cell.get("failure")
        lines.append(
            "| {dataset} | {seed} | {status} | {device} | {cold} | {warm} | {alloc} | {reserved} | {failure} |".format(
                dataset=cell["dataset"],
                seed=cell["seed"],
                status=cell["status"],
                device=cell.get("device", "—"),
                cold=_fmt_seconds(cell.get("score_bundle_cold_total_seconds")),
                warm=_fmt_seconds(cell.get("score_bundle_warm_read_seconds")),
                alloc=_fmt_mib(cell.get("peak_gpu_allocated_bytes")),
                reserved=_fmt_mib(cell.get("peak_gpu_reserved_bytes")),
                failure="—" if failure is None else str(failure).replace("|", "/"),
            )
        )

    lines.extend(
        [
            "",
            "## 3. 方法级 cold / warm Selection 时间",
            "",
            "| Dataset | Seed | Method | Cold selection (ms) | Warm selection (ms) | Cold outcome | Warm outcome | Status |",
            "|---|---:|---|---:|---:|---|---|---|",
        ]
    )
    for cell in cells:
        for name in SCORE_NAMES:
            item = cell["methods"][name]
            cold_s = item.get("cold_selection_seconds")
            warm_s = item.get("warm_selection_seconds")
            lines.append(
                "| {dataset} | {seed} | `{method}` | {cold} | {warm} | {cold_outcome} | {warm_outcome} | {status} |".format(
                    dataset=cell["dataset"],
                    seed=cell["seed"],
                    method=name,
                    cold="—" if cold_s is None else "{0:.3f}".format(1000 * float(cold_s)),
                    warm="—" if warm_s is None else "{0:.3f}".format(1000 * float(warm_s)),
                    cold_outcome=(
                        "—" if item.get("cold_cache_hit") is None else "hit" if item["cold_cache_hit"] else "miss_saved"
                    ),
                    warm_outcome=(
                        "—" if item.get("warm_cache_hit") is None else "hit" if item["warm_cache_hit"] else "miss"
                    ),
                    status=item["status"],
                )
            )

    successful_method_rows = [
        cell["methods"][name]
        for cell in passed
        for name in SCORE_NAMES
        if cell["methods"][name]["status"] == "success"
    ]
    lines.extend(["", "## 4. 汇总与失败状态", ""])
    if passed:
        cold_bundle = [cell["score_bundle_cold_total_seconds"] for cell in passed]
        warm_bundle = [cell["score_bundle_warm_read_seconds"] for cell in passed]
        lines.extend(
            [
                "- 成功 cells：**{0}/{1}**；失败 cells：**{2}**。".format(
                    len(passed), len(cells), len(failed)
                ),
                "- ScoreBundle cold total：mean `{0:.4f}s`，max `{1:.4f}s`。".format(
                    statistics.mean(cold_bundle), max(cold_bundle)
                ),
                "- ScoreBundle warm exact read：mean `{0:.4f}s`，max `{1:.4f}s`。".format(
                    statistics.mean(warm_bundle), max(warm_bundle)
                ),
            ]
        )
    if successful_method_rows:
        cold_methods = [row["cold_selection_seconds"] for row in successful_method_rows]
        warm_methods = [row["warm_selection_seconds"] for row in successful_method_rows]
        lines.extend(
            [
                "- 方法级 cold selection：mean `{0:.3f}ms`，max `{1:.3f}ms`。".format(
                    1000 * statistics.mean(cold_methods), 1000 * max(cold_methods)
                ),
                "- 方法级 warm selection：mean `{0:.3f}ms`，max `{1:.3f}ms`。".format(
                    1000 * statistics.mean(warm_methods), 1000 * max(warm_methods)
                ),
            ]
        )
    if failed:
        lines.extend(["", "### 失败明细", ""])
        for cell in failed:
            lines.append(
                "- `{0}/seed{1}`: `{2}`".format(
                    cell["dataset"], cell["seed"], cell["failure"]
                )
            )
    lines.extend(
        [
            "",
            "## 5. Evidence",
            "",
            "- Machine-readable manifest: `{0}`".format(document["manifest_path"]),
            "- Cache root: `{0}`".format(document["cache_root"]),
            "- Cell summaries: `{0}`".format(document["output_root"]),
            "- Algorithm version: `{0}`".format(document["algorithm_version"]),
            "",
        ]
    )
    md_path = md_path.expanduser().resolve()
    html_path = html_path.expanduser().resolve()
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    render_document(
        md_path,
        html_path,
        "小图 Selection 全量实测",
        badge,
        "17-METHOD COLD/WARM BENCHMARK",
        brand="OpenGU Research",
    )


def main(argv: Sequence[str] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be positive")
    cache_root = args.cache_root.expanduser().resolve()
    output_root = args.output_root.expanduser().resolve()
    manifest_path = output_root / "benchmark_manifest.json"
    if not args.resume:
        if cache_root.exists() and any(cache_root.iterdir()):
            raise FileExistsError("benchmark cache root is not empty: {0}".format(cache_root))
        if output_root.exists() and any(output_root.iterdir()):
            raise FileExistsError("benchmark output root is not empty: {0}".format(output_root))
    cache_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    records = []
    for dataset in args.datasets:
        for seed in args.seeds:
            label = "{0}_seed{1}".format(dataset.lower(), seed)
            cell_dir = output_root / "cells" / label
            cell_cache = cache_root / label
            cold_path = cell_dir / "cold.json"
            warm_path = cell_dir / "warm.json"
            try:
                if args.resume and cold_path.is_file():
                    cold = _load_json(cold_path)
                else:
                    cold_run = _run(
                        _command(
                            dataset=dataset,
                            seed=seed,
                            data_root=args.data_root.expanduser().resolve(),
                            cache_root=cell_cache,
                            output=cold_path,
                            budgets=args.budgets,
                            device=args.device,
                            warm=False,
                        ),
                        args.timeout_seconds,
                    )
                    if cold_run["returncode"] != 0 or not cold_path.is_file():
                        records.append(_failure_record(dataset, seed, "cold", cold_run))
                        continue
                    cold = _load_json(cold_path)

                if args.resume and warm_path.is_file():
                    warm = _load_json(warm_path)
                else:
                    warm_run = _run(
                        _command(
                            dataset=dataset,
                            seed=seed,
                            data_root=args.data_root.expanduser().resolve(),
                            cache_root=cell_cache,
                            output=warm_path,
                            budgets=args.budgets,
                            device=args.device,
                            warm=True,
                        ),
                        args.timeout_seconds,
                    )
                    if warm_run["returncode"] != 0 or not warm_path.is_file():
                        records.append(_failure_record(dataset, seed, "warm", warm_run))
                        continue
                    warm = _load_json(warm_path)

                records.append(
                    _build_cell_record(
                        dataset=dataset,
                        seed=seed,
                        cold_path=cold_path,
                        warm_path=warm_path,
                        cold=cold,
                        warm=warm,
                    )
                )
            except Exception as exc:
                records.append(
                    _failure_record(
                        dataset,
                        seed,
                        "validation",
                        {"type": type(exc).__name__, "message": str(exc)},
                    )
                )
            finally:
                document = {
                    "schema": BENCHMARK_SCHEMA,
                    "version": BENCHMARK_VERSION,
                    "algorithm_version": ALGORITHM_VERSION,
                    "formal_score_names": list(SCORE_NAMES),
                    "formal_score_count": len(SCORE_NAMES),
                    "datasets": list(args.datasets),
                    "seeds": list(args.seeds),
                    "device_requested": args.device,
                    "cache_root": str(cache_root),
                    "output_root": str(output_root),
                    "manifest_path": str(manifest_path),
                    "cells": records,
                }
                _write_json_atomic(manifest_path, document)
                _render_report(document, args.report_md, args.report_html)

    passed = sum(1 for record in records if record["status"] == "success")
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "report_md": str(args.report_md.expanduser().resolve()),
                "report_html": str(args.report_html.expanduser().resolve()),
                "cells_passed": passed,
                "cells_total": len(records),
                "formal_score_count": len(SCORE_NAMES),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
