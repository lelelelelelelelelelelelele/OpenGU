import glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from .log_resume import parse_log_quality, should_skip
from ..reporting.writer import append_report_entry

METHODS = [
    "GIF",
    "IDEA",
    "MEGU",
    "GraphEraser",
    "GraphRevoker",
    "GUIDE",
    "SGU",
    "GUKD",
    "D2DGN",
]

RATIO = "0.5"
APPROX_NODES = 1354
TIMEOUT = 1200

PROJECT_DIR = Path(__file__).resolve().parents[3]
OUTPUT_ROOT = PROJECT_DIR / "results" / "evaluation" / "step0"
LEGACY_ROOT = PROJECT_DIR / "results" / "step0_validation"

LOG_DIR = OUTPUT_ROOT / "ratio05_logs"
ROUND2_LOG_DIR = OUTPUT_ROOT / "round2_logs"
ROUND1_LOG_DIR = OUTPUT_ROOT / "round1_logs"
SEARCH_LOG_DIRS = [
    str(LOG_DIR),
    str(ROUND2_LOG_DIR),
    str(ROUND1_LOG_DIR),
    str(LEGACY_ROOT / "ratio05_logs"),
    str(LEGACY_ROOT / "round2_logs"),
    str(LEGACY_ROOT / "round1_logs"),
]
OUTPUT_PATH = OUTPUT_ROOT / "ratio05_results.json"
SCRIPT_NAME = Path(__file__).name
LOG_DIR.mkdir(parents=True, exist_ok=True)


def clean_cached_unlearning_files(ratio: str, dataset: str = "cora") -> None:
    pattern = PROJECT_DIR / "data" / "unlearning_task" / "**" / f"*_{ratio}_{dataset}_*.txt"
    for file_path in glob.glob(str(pattern), recursive=True):
        try:
            os.remove(file_path)
        except OSError:
            pass


def parse_log_metrics(log_path: str) -> dict:
    metrics = {"f1_before": None, "f1_after": None, "unlearn_time": None, "auc": None}
    quality = parse_log_quality(log_path)
    metrics["f1_after"] = quality.get("f1_after")

    if not log_path or not os.path.isfile(log_path):
        return metrics

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as file_obj:
            content = file_obj.read()
    except OSError:
        return metrics

    match = re.search(r"Average Unlearning Time:\s*([0-9]*\.?[0-9]+)", content)
    if match:
        metrics["unlearn_time"] = float(match.group(1))

    match = re.search(r"Average AUC Score:\s*([0-9]*\.?[0-9]+)", content)
    if match:
        metrics["auc"] = float(match.group(1))

    f1_before_matches = re.findall(r"Epoch:\s*\d+\s*\|\s*F1 Score:\s*([0-9]*\.?[0-9]+)\s*\|\s*Loss", content)
    if f1_before_matches:
        metrics["f1_before"] = float(f1_before_matches[-1])

    match = re.search(r"Original F1 Score:\s*([0-9]*\.?[0-9]+)", content)
    if match:
        metrics["f1_before"] = float(match.group(1))

    return metrics


def run_experiment(method: str, dataset: str = "cora", model: str = "GCN") -> dict:
    log_file = LOG_DIR / f"{method}_{model}_{dataset}_r{RATIO}.log"
    cmd = (
        f'"{sys.executable}" main.py '
        f"--cuda 0 --dataset_name {dataset} --base_model {model} "
        f"--unlearning_methods {method} --unlearn_task node --downstream_task node "
        f"--unlearn_ratio {RATIO} --proportion_unlearned_nodes {RATIO} "
        f"--num_epochs 100 --num_runs 1"
    )
    print(f"[{method}] start")
    start = time.time()
    try:
        with log_file.open("w", encoding="utf-8", errors="replace") as log_obj:
            completed = subprocess.run(
                cmd,
                shell=True,
                timeout=TIMEOUT,
                cwd=str(PROJECT_DIR),
                stdout=log_obj,
                stderr=subprocess.STDOUT,
            )
        elapsed = time.time() - start
        quality = parse_log_quality(str(log_file))
        parsed = parse_log_metrics(str(log_file))

        if completed.returncode != 0:
            print(f"[{method}] X ({elapsed:.1f}s)")
            return {
                "status": "X",
                "error_type": quality.get("error_type") or "RETURN_CODE_NONZERO",
                "error_msg": quality.get("error_msg") or f"returncode={completed.returncode}",
                "time_s": elapsed,
                "log_file": str(log_file),
                **parsed,
            }

        if quality["ok"]:
            print(f"[{method}] OK f1_after={parsed['f1_after']:.4f} ({elapsed:.1f}s)")
            return {"status": "OK", "time_s": elapsed, "log_file": str(log_file), **parsed}

        print(f"[{method}] WARN ({elapsed:.1f}s)")
        return {
            "status": "WARN",
            "error_type": quality.get("error_type") or "LOG_INCOMPLETE",
            "error_msg": quality.get("error_msg") or "Log missing strict completion markers",
            "time_s": elapsed,
            "log_file": str(log_file),
            **parsed,
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[{method}] TIMEOUT ({elapsed:.1f}s)")
        return {
            "status": "TIMEOUT",
            "error_type": "TIMEOUT",
            "error_msg": f"Timeout after {TIMEOUT}s",
            "time_s": elapsed,
            "log_file": str(log_file),
        }


def main() -> None:
    results = {}
    for method in METHODS:
        skip, _, existing_log = should_skip(
            dataset="cora",
            method=method,
            model="GCN",
            ratio=RATIO,
            base_dir=SEARCH_LOG_DIRS,
        )
        if skip:
            parsed = parse_log_metrics(existing_log)
            print(f"[{method}] SKIP strict-ok ({existing_log})")
            result = {
                "status": "SKIP",
                "error_type": None,
                "error_msg": "Strict OK log exists",
                "time_s": 0.0,
                "log_file": existing_log,
                **parsed,
            }
        else:
            clean_cached_unlearning_files(RATIO)
            result = run_experiment(method)

        result["method"] = method
        result["dataset"] = "cora"
        result["model"] = "GCN"
        result["unlearn_ratio"] = float(RATIO)
        result["approx_nodes"] = APPROX_NODES
        results[method] = result

        append_report_entry(
            script=SCRIPT_NAME,
            dataset="cora",
            model="GCN",
            method=method,
            ratio=RATIO,
            status=result.get("status", "X"),
            log_file=result.get("log_file") or existing_log or "",
            f1_before=result.get("f1_before"),
            f1_after=result.get("f1_after"),
            unlearn_time=result.get("unlearn_time"),
            auc=result.get("auc"),
            time_s=result.get("time_s"),
            error_type=result.get("error_type"),
            error_msg=result.get("error_msg"),
        )

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT_PATH.open("w", encoding="utf-8") as file_obj:
            json.dump(results, file_obj, indent=2, ensure_ascii=False)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
