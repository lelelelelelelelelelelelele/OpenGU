"""
Batch experiment runner for systematic attack evaluation.

Runs attack strategies across multiple GU methods, datasets, and ratios.
Each experiment is a separate subprocess to ensure clean state.

Usage:
    # Phase A: 4 methods x 4 strategies on Cora/GCN
    python run_experiments.py --phase A --cuda 0

    # Phase B: cross-dataset (3 datasets x 4 methods)
    python run_experiments.py --phase B --cuda 0

    # Phase C: ratio sensitivity (4 ratios x 2 methods x 2 strategies)
    python run_experiments.py --phase C --cuda 0

    # Custom single run
    python run_experiments.py --methods GNNDelete,GIF --datasets cora --cuda 0
"""
import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

PYTHON = sys.executable  # Use the same Python interpreter

# Experiment configurations
PHASE_A = {
    "name": "Phase A: Method Comparison (Cora/GCN)",
    "methods": ["GNNDelete", "GIF", "GraphEraser", "GUIDE"],
    "datasets": ["cora"],
    "models": ["GCN"],
    "strategies": "random,degree,pagerank,tracin",
    "ratios": [0.05],
}

PHASE_B = {
    "name": "Phase B: Cross-Dataset Generalization",
    "methods": ["GNNDelete", "GIF", "GraphEraser", "GUIDE"],
    "datasets": ["cora", "citeseer", "pubmed"],
    "models": ["GCN"],
    "strategies": "random,tracin",
    "ratios": [0.05],
}

PHASE_C = {
    "name": "Phase C: Ratio Sensitivity",
    "methods": ["GNNDelete", "GIF"],
    "datasets": ["cora"],
    "models": ["GCN"],
    "strategies": "random,tracin",
    "ratios": [0.01, 0.05, 0.1, 0.2],
}


def run_single_experiment(method, dataset, model, strategies, ratio, cuda, output_dir, random_seed):
    """Run a single experiment via demo_attack.py subprocess."""
    save_path = os.path.join(
        output_dir,
        f"{method}_{dataset}_{model}_r{ratio}.json"
    )

    cmd = [
        PYTHON, "demo_attack.py",
        "--cuda", str(cuda),
        "--dataset_name", dataset,
        "--base_model", model,
        "--unlearning_methods", method,
        "--strategies", strategies,
        "--unlearn_ratio", str(ratio),
        "--seed", str(random_seed),
        "--no_cache",
        "--save_path", save_path,
    ]

    label = f"{method}/{dataset}/{model}/r={ratio}"
    print(f"\n{'='*60}")
    print(f"  Running: {label}")
    print(f"  Strategies: {strategies}")
    print(f"{'='*60}")

    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 min max per experiment
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        elapsed = time.time() - start

        if result.returncode != 0:
            print(f"  FAILED ({elapsed:.1f}s)")
            # Save error log
            err_path = save_path.replace(".json", "_error.log")
            with open(err_path, "w") as f:
                f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
            print(f"  Error log: {err_path}")
            # Print last few lines of error
            stderr_lines = result.stderr.strip().split("\n")
            for line in stderr_lines[-5:]:
                print(f"  | {line}")
            return None
        else:
            print(f"  OK ({elapsed:.1f}s)")
            # Extract summary from stdout
            for line in result.stdout.split("\n"):
                if any(kw in line for kw in ["Rank", "Best Strategy", "tracin", "random", "degree", "pagerank"]):
                    if "Rank" in line and "Strategy" in line:
                        print(f"  {line.strip()}")
                    elif line.strip().startswith(("1", "2", "3", "4")):
                        print(f"  {line.strip()}")

            # Load and return result
            if os.path.exists(save_path):
                with open(save_path, "r") as f:
                    return json.load(f)
            return {"status": "ok", "time": elapsed}

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT (>600s)")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def run_phase(phase_config, cuda, output_base, random_seed):
    """Run all experiments in a phase."""
    phase_name = phase_config["name"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(output_base, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    methods = phase_config["methods"]
    datasets = phase_config["datasets"]
    models = phase_config["models"]
    strategies = phase_config["strategies"]
    ratios = phase_config["ratios"]

    total = len(methods) * len(datasets) * len(models) * len(ratios)

    print(f"\n{'#'*70}")
    print(f"  {phase_name}")
    print(f"  Methods: {methods}")
    print(f"  Datasets: {datasets}")
    print(f"  Strategies: {strategies}")
    print(f"  Ratios: {ratios}")
    print(f"  Random Seed: {random_seed}")
    print(f"  Total experiments: {total}")
    print(f"  Output: {output_dir}")
    print(f"{'#'*70}")

    results = {}
    completed = 0
    failed = 0
    phase_start = time.time()

    for method in methods:
        for dataset in datasets:
            for model in models:
                for ratio in ratios:
                    key = f"{method}_{dataset}_{model}_r{ratio}"
                    result = run_single_experiment(
                        method, dataset, model, strategies, ratio, cuda, output_dir, random_seed
                    )
                    if result is not None:
                        results[key] = result
                        completed += 1
                    else:
                        failed += 1

    phase_time = time.time() - phase_start

    # Save summary
    summary = {
        "phase": phase_name,
        "timestamp": timestamp,
        "total_experiments": total,
        "completed": completed,
        "failed": failed,
        "total_time": phase_time,
        "config": phase_config,
        "results": results,
    }

    summary_path = os.path.join(output_dir, "_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    # Print summary
    print(f"\n{'='*70}")
    print(f"  {phase_name} - COMPLETE")
    print(f"  Completed: {completed}/{total} | Failed: {failed}")
    print(f"  Total time: {phase_time:.1f}s")
    print(f"  Results: {output_dir}")
    print(f"{'='*70}")

    # Print comparison table
    _print_summary_table(results, strategies)

    return summary


def _print_summary_table(results, strategies_str):
    """Print a summary table from collected results."""
    strategy_list = strategies_str.split(",")

    print(f"\n{'='*80}")
    print("Summary Table: F1 Drop by Method x Strategy")
    print(f"{'='*80}")

    header = f"{'Method':<15} {'Dataset':<10}"
    for s in strategy_list:
        header += f" {s:<12}"
    header += " Best"
    print(header)
    print("-" * 80)

    for key, data in sorted(results.items()):
        if not isinstance(data, dict):
            continue

        parts = key.split("_")
        method = parts[0]
        dataset = parts[1]

        row = f"{method:<15} {dataset:<10}"
        best_drop = -999
        best_strategy = ""

        # ComparisonResult.to_dict() stores results as {strategy_name: result_dict}
        result_dict = data.get("results", {})
        for name in strategy_list:
            # Strategy names in results may have "Strategy" suffix
            r = None
            for rkey, rval in result_dict.items():
                if rkey.lower().startswith(name.lower()):
                    r = rval
                    break
            if r:
                f1_drop = r.get("f1_drop", 0)
                row += f" {f1_drop:>10.4f}  "
                if f1_drop > best_drop:
                    best_drop = f1_drop
                    best_strategy = name
            else:
                row += f" {'N/A':>10}  "

        row += f" {best_strategy}"
        print(row)

    print(f"{'='*80}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Batch experiment runner")
    parser.add_argument("--phase", type=str, choices=["A", "B", "C", "all"],
                        default="A", help="Experiment phase to run")
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--output", type=str, default="results/experiments",
                        help="Base output directory")
    parser.add_argument("--random_seed", type=int, default=2024,
                        help="Random seed passed to demo_attack.py")

    # Custom overrides
    parser.add_argument("--methods", type=str, default=None,
                        help="Comma-separated methods (overrides phase config)")
    parser.add_argument("--datasets", type=str, default=None,
                        help="Comma-separated datasets (overrides phase config)")
    parser.add_argument("--strategies", type=str, default=None,
                        help="Comma-separated strategies (overrides phase config)")
    parser.add_argument("--ratios", type=str, default=None,
                        help="Comma-separated ratios (overrides phase config)")

    args = parser.parse_args()

    phases = {
        "A": PHASE_A,
        "B": PHASE_B,
        "C": PHASE_C,
    }

    if args.phase == "all":
        phase_list = ["A", "B", "C"]
    else:
        phase_list = [args.phase]

    for phase_key in phase_list:
        config = phases[phase_key].copy()

        # Apply overrides
        if args.methods:
            config["methods"] = args.methods.split(",")
        if args.datasets:
            config["datasets"] = args.datasets.split(",")
        if args.strategies:
            config["strategies"] = args.strategies
        if args.ratios:
            config["ratios"] = [float(r) for r in args.ratios.split(",")]

        output_dir = os.path.join(args.output, f"phase_{phase_key.lower()}")
        run_phase(config, args.cuda, output_dir, args.random_seed)


if __name__ == "__main__":
    main()
