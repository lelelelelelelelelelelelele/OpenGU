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

DATASETS = ["cora", "citeseer", "pubmed"]
METHODS = [
    "GraphEraser",
    "GIF",
    "GUIDE",
    "GNNDelete",
    "SGU",
    "MEGU",
    "GUKD",
    "D2DGN",
    "IDEA",
    "GraphRevoker",
]
RATIOS = ["0.005", "0.01", "0.02", "0.05", "0.1", "0.2", "0.5"]
NODE_COUNTS = {"cora": 2708, "citeseer": 3327, "pubmed": 19717}
TIMEOUT = 1200

PROJECT_DIR = Path(__file__).resolve().parents[3]
OUTPUT_ROOT = PROJECT_DIR / "results" / "evaluation" / "step0"
LEGACY_ROOT = PROJECT_DIR / "results" / "step0_validation"

CROSS_LOG_ROOT = OUTPUT_ROOT / "cross_logs"
ROUND1_LOG_DIR = OUTPUT_ROOT / "round1_logs"
ROUND2_LOG_DIR = OUTPUT_ROOT / "round2_logs"
RATIO05_LOG_DIR = OUTPUT_ROOT / "ratio05_logs"
OUTPUT_PATH = OUTPUT_ROOT / "cross_dataset_results.json"
SCRIPT_NAME = Path(__file__).name
CROSS_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def approx_nodes(dataset: str, ratio: str):
    if dataset not in NODE_COUNTS:
        return None
    return int(round(NODE_COUNTS[dataset] * float(ratio)))


def clean_cached_unlearning_files(dataset: str, ratio: str) -> None:
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


def get_search_dirs(dataset_dir: Path, dataset: str):
    dirs = [str(dataset_dir)]
    if dataset == "cora":
        dirs.extend(
            [
                str(ROUND2_LOG_DIR),
                str(RATIO05_LOG_DIR),
                str(ROUND1_LOG_DIR),
                str(LEGACY_ROOT / "round2_logs"),
                str(LEGACY_ROOT / "ratio05_logs"),
                str(LEGACY_ROOT / "round1_logs"),
            ]
        )
    return dirs


def run_experiment(dataset: str, method: str, ratio: str, model: str = "GCN") -> dict:
    dataset_dir = CROSS_LOG_ROOT / dataset
    dataset_dir.mkdir(parents=True, exist_ok=True)
    log_file = dataset_dir / f"{method}_{model}_{dataset}_r{ratio}.log"
    cmd = (
        f'"{sys.executable}" main.py '
        f"--cuda 0 --dataset_name {dataset} --base_model {model} "
        f"--unlearning_methods {method} --unlearn_task node --downstream_task node "
        f"--unlearn_ratio {ratio} --proportion_unlearned_nodes {ratio} "
        f"--num_epochs 100 --num_runs 1"
    )

    print(f"[{dataset}|{method}|r={ratio}] start")
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
            print(f"[{dataset}|{method}|r={ratio}] X ({elapsed:.1f}s)")
            return {
                "status": "X",
                "error_type": quality.get("error_type") or "RETURN_CODE_NONZERO",
                "error_msg": quality.get("error_msg") or f"returncode={completed.returncode}",
                "time_s": elapsed,
                "log_file": str(log_file),
                **parsed,
            }

        if quality["ok"]:
            print(f"[{dataset}|{method}|r={ratio}] OK f1_after={parsed['f1_after']:.4f} ({elapsed:.1f}s)")
            return {"status": "OK", "time_s": elapsed, "log_file": str(log_file), **parsed}

        print(f"[{dataset}|{method}|r={ratio}] WARN ({elapsed:.1f}s)")
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
        print(f"[{dataset}|{method}|r={ratio}] TIMEOUT ({elapsed:.1f}s)")
        return {
            "status": "TIMEOUT",
            "error_type": "TIMEOUT",
            "error_msg": f"Timeout after {TIMEOUT}s",
            "time_s": elapsed,
            "log_file": str(log_file),
        }


def main() -> None:
    all_results = {}
    for dataset in DATASETS:
        dataset_dir = CROSS_LOG_ROOT / dataset
        dataset_dir.mkdir(parents=True, exist_ok=True)
        all_results[dataset] = {}
        for method in METHODS:
            all_results[dataset][method] = {}
            for ratio in RATIOS:
                search_dirs = get_search_dirs(dataset_dir=dataset_dir, dataset=dataset)
                skip, _, existing_log = should_skip(
                    dataset=dataset,
                    method=method,
                    model="GCN",
                    ratio=ratio,
                    base_dir=search_dirs,
                )
                if skip:
                    parsed = parse_log_metrics(existing_log)
                    print(f"[{dataset}|{method}|r={ratio}] SKIP strict-ok ({existing_log})")
                    result = {
                        "status": "SKIP",
                        "error_type": None,
                        "error_msg": "Strict OK log exists",
                        "time_s": 0.0,
                        "log_file": existing_log,
                        **parsed,
                    }
                else:
                    clean_cached_unlearning_files(dataset=dataset, ratio=ratio)
                    result = run_experiment(dataset=dataset, method=method, ratio=ratio, model="GCN")

                result["dataset"] = dataset
                result["method"] = method
                result["model"] = "GCN"
                result["unlearn_ratio"] = float(ratio)
                result["approx_nodes"] = approx_nodes(dataset, ratio)
                all_results[dataset][method][ratio] = result

                append_report_entry(
                    script=SCRIPT_NAME,
                    dataset=dataset,
                    model="GCN",
                    method=method,
                    ratio=ratio,
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
                    json.dump(all_results, file_obj, indent=2, ensure_ascii=False)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
