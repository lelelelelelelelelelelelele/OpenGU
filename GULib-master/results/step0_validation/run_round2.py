"""
Round 2 Deep Validation: 11 methods x varying unlearn_ratio
Uses --unlearn_ratio since num_unlearned_nodes gets overwritten by original_dataset.py
Cora training set ~2166 nodes, so:
  ratio 0.005 -> ~13 nodes
  ratio 0.02  -> ~54 nodes
  ratio 0.05  -> ~135 nodes
  ratio 0.1   -> ~270 nodes (default, already tested in round1)
  ratio 0.2   -> ~541 nodes
"""
import subprocess
import json
import re
import time
import os
import sys
import glob

METHODS = [
    "GraphEraser", "GIF", "GUIDE", "GNNDelete", "SGU",
    "MEGU", "GUKD", "D2DGN", "IDEA", "Projector", "GraphRevoker"
]

SLOW_METHODS = {"Projector"}

# ratio -> approximate node count for Cora
UNLEARN_RATIOS = {
    "0.005": 13,
    "0.02": 54,
    "0.05": 135,
    "0.1": 270,
    "0.2": 541,
}

TIMEOUT = 600

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(RESULTS_DIR, "..", "..")
LOG_DIR = os.path.join(RESULTS_DIR, "round2_logs")
os.makedirs(LOG_DIR, exist_ok=True)


def clean_cached_unlearning_files(ratio):
    """Remove cached unlearning node files so new ratio takes effect."""
    patterns = [
        os.path.join(PROJECT_DIR, "data", "unlearning_task", "**", f"*_{ratio}_cora_*.txt"),
    ]
    for pat in patterns:
        for f in glob.glob(pat, recursive=True):
            try:
                os.remove(f)
            except Exception:
                pass


def parse_log(log_path):
    result = {"f1_after": None, "f1_before": None, "unlearn_time": None, "auc": None}
    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            output = f.read()
    except Exception:
        return result

    m = re.search(r'Unlearn F1 Score:\s*([\d.]+)', output)
    if m:
        result["f1_after"] = float(m.group(1))

    if result["f1_after"] is None:
        m = re.search(r'Direct F1 Score:\s*([\d.]+)', output)
        if m:
            result["f1_after"] = float(m.group(1))

    if result["f1_after"] is None:
        m = re.search(r'Final Test F1:\s*([\d.]+)', output)
        if m:
            result["f1_after"] = float(m.group(1))

    m = re.search(r'Average Unlearning Time:\s*([\d.]+)', output)
    if m:
        result["unlearn_time"] = float(m.group(1))

    m = re.search(r'Average AUC Score:\s*([\d.]+)', output)
    if m:
        result["auc"] = float(m.group(1))

    # F1 before: last training F1 before unlearning starts
    f1_before_matches = re.findall(r'Epoch:\s*\d+\s*\|\s*F1 Score:\s*([\d.]+)\s*\|\s*Loss', output)
    if f1_before_matches:
        result["f1_before"] = float(f1_before_matches[-1])

    m = re.search(r'Original F1 Score:\s*([\d.]+)', output)
    if m:
        result["f1_before"] = float(m.group(1))

    # Also look for "best" F1
    m = re.search(r'best:([\d.]+)', output)
    if m and result["f1_before"] is None:
        result["f1_before"] = float(m.group(1))

    return result


def run_experiment(method, ratio):
    approx_nodes = UNLEARN_RATIOS[ratio]
    log_file = os.path.join(LOG_DIR, f"{method}_GCN_cora_r{ratio}.log")

    cmd = (
        f'"{sys.executable}" main.py '
        f'--cuda 0 --dataset_name cora --base_model GCN '
        f'--unlearning_methods {method} --unlearn_task node --downstream_task node '
        f'--unlearn_ratio {ratio} --proportion_unlearned_nodes {ratio} '
        f'--num_epochs 100 --num_runs 1'
    )

    print(f"  [{method} x ratio={ratio} (~{approx_nodes}n)]", end=" ", flush=True)
    start = time.time()

    try:
        with open(log_file, "w", encoding="utf-8", errors="replace") as log_f:
            ret = subprocess.run(
                cmd, shell=True, timeout=TIMEOUT, cwd=PROJECT_DIR,
                stdout=log_f, stderr=subprocess.STDOUT,
            )
        elapsed = time.time() - start

        parsed = parse_log(log_file)

        if ret.returncode != 0:
            print(f"FAIL ({elapsed:.1f}s)")
            try:
                with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
                err = [l.strip() for l in lines if "Error" in l]
                error_msg = err[-1][:200] if err else "returncode != 0"
            except Exception:
                error_msg = "returncode != 0"
            return {"status": "X", "error_msg": error_msg, "time_s": elapsed}

        if parsed["f1_after"] is not None:
            print(f"OK F1={parsed['f1_after']:.4f} t={parsed.get('unlearn_time', '?')}s ({elapsed:.1f}s)")
            return {
                "status": "OK",
                "f1_before": parsed.get("f1_before"),
                "f1_after": parsed["f1_after"],
                "unlearn_time": parsed["unlearn_time"],
                "auc": parsed["auc"],
                "time_s": elapsed,
            }
        else:
            print(f"WARN no-f1 ({elapsed:.1f}s)")
            return {"status": "WARN", "error_msg": "Could not parse F1", "time_s": elapsed}

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"TIMEOUT ({elapsed:.1f}s)")
        return {"status": "TIMEOUT", "error_msg": f"Timeout after {TIMEOUT}s", "time_s": elapsed}


def main():
    all_results = {}
    output_path = os.path.join(RESULTS_DIR, "round2_results.json")

    ratios = sorted(UNLEARN_RATIOS.keys(), key=float)

    for method in METHODS:
        print(f"\n{'='*60}")
        print(f"Method: {method}")
        print(f"{'='*60}")
        all_results[method] = {}

        for ratio in ratios:
            approx_nodes = UNLEARN_RATIOS[ratio]

            if method in SLOW_METHODS and float(ratio) > 0.1:
                print(f"  [{method} x ratio={ratio}] SKIP (slow)")
                all_results[method][ratio] = {"status": "SKIP"}
                continue

            # Clean cached files for this ratio so fresh generation happens
            clean_cached_unlearning_files(ratio)

            result = run_experiment(method, ratio)
            result["method"] = method
            result["model"] = "GCN"
            result["dataset"] = "cora"
            result["unlearn_ratio"] = float(ratio)
            result["approx_nodes"] = approx_nodes
            all_results[method][ratio] = result

        # Save after each method
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"All experiments complete.")
    print(f"Results saved to: {output_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
