"""
Run targeted ratio=0.5 experiments for selected methods on Cora+GCN.
Stores logs and parsed metrics in separate files from round2.
"""
import glob
import json
import os
import re
import subprocess
import sys
import time

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

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(RESULTS_DIR, "..", "..")
LOG_DIR = os.path.join(RESULTS_DIR, "ratio05_logs")
os.makedirs(LOG_DIR, exist_ok=True)


def clean_cached_unlearning_files(ratio: str) -> None:
    pattern = os.path.join(PROJECT_DIR, "data", "unlearning_task", "**", f"*_{ratio}_cora_*.txt")
    for file_path in glob.glob(pattern, recursive=True):
        try:
            os.remove(file_path)
        except OSError:
            pass


def parse_log(log_path: str) -> dict:
    result = {"f1_after": None, "f1_before": None, "unlearn_time": None, "auc": None}
    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as file_obj:
            output = file_obj.read()
    except OSError:
        return result

    match = re.search(r"Unlearn F1 Score:\s*([\d.]+)", output)
    if match:
        result["f1_after"] = float(match.group(1))

    if result["f1_after"] is None:
        match = re.search(r"Direct F1 Score:\s*([\d.]+)", output)
        if match:
            result["f1_after"] = float(match.group(1))

    if result["f1_after"] is None:
        match = re.search(r"Final Test F1:\s*([\d.]+)", output)
        if match:
            result["f1_after"] = float(match.group(1))

    match = re.search(r"Average Unlearning Time:\s*([\d.]+)", output)
    if match:
        result["unlearn_time"] = float(match.group(1))

    match = re.search(r"Average AUC Score:\s*([\d.]+)", output)
    if match:
        result["auc"] = float(match.group(1))

    f1_before_matches = re.findall(r"Epoch:\s*\d+\s*\|\s*F1 Score:\s*([\d.]+)\s*\|\s*Loss", output)
    if f1_before_matches:
        result["f1_before"] = float(f1_before_matches[-1])

    match = re.search(r"Original F1 Score:\s*([\d.]+)", output)
    if match:
        result["f1_before"] = float(match.group(1))

    return result


def run_experiment(method: str) -> dict:
    log_file = os.path.join(LOG_DIR, f"{method}_GCN_cora_r{RATIO}.log")
    cmd = (
        f'"{sys.executable}" main.py '
        f'--cuda 0 --dataset_name cora --base_model GCN '
        f'--unlearning_methods {method} --unlearn_task node --downstream_task node '
        f'--unlearn_ratio {RATIO} --proportion_unlearned_nodes {RATIO} '
        f'--num_epochs 100 --num_runs 1'
    )
    print(f"[{method}] start")
    start = time.time()

    try:
        with open(log_file, "w", encoding="utf-8", errors="replace") as log_obj:
            ret = subprocess.run(
                cmd,
                shell=True,
                timeout=TIMEOUT,
                cwd=PROJECT_DIR,
                stdout=log_obj,
                stderr=subprocess.STDOUT,
            )
        elapsed = time.time() - start
        parsed = parse_log(log_file)

        if ret.returncode != 0:
            print(f"[{method}] FAIL ({elapsed:.1f}s)")
            return {
                "status": "X",
                "error_msg": f"returncode={ret.returncode}",
                "time_s": elapsed,
                "log_file": log_file,
            }

        if parsed["f1_after"] is None:
            print(f"[{method}] WARN no-f1 ({elapsed:.1f}s)")
            return {
                "status": "WARN",
                "error_msg": "Could not parse F1",
                "time_s": elapsed,
                "log_file": log_file,
            }

        print(f"[{method}] OK f1_after={parsed['f1_after']:.4f} ({elapsed:.1f}s)")
        return {
            "status": "OK",
            "f1_before": parsed.get("f1_before"),
            "f1_after": parsed["f1_after"],
            "unlearn_time": parsed["unlearn_time"],
            "auc": parsed["auc"],
            "time_s": elapsed,
            "log_file": log_file,
        }

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[{method}] TIMEOUT ({elapsed:.1f}s)")
        return {
            "status": "TIMEOUT",
            "error_msg": f"Timeout after {TIMEOUT}s",
            "time_s": elapsed,
            "log_file": log_file,
        }


def main() -> None:
    output_path = os.path.join(RESULTS_DIR, "ratio05_results.json")
    results = {}

    for method in METHODS:
        clean_cached_unlearning_files(RATIO)
        result = run_experiment(method)
        result["method"] = method
        result["dataset"] = "cora"
        result["model"] = "GCN"
        result["unlearn_ratio"] = float(RATIO)
        result["approx_nodes"] = APPROX_NODES
        results[method] = result

        with open(output_path, "w", encoding="utf-8") as file_obj:
            json.dump(results, file_obj, indent=2, ensure_ascii=False)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
