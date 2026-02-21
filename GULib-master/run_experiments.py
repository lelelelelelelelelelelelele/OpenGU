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
import re
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

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
    "ratios": [0.2, 0.1, 0.05, 0.01],  # Descending order: larger k first for cache efficiency
}

METHOD_TIMEOUTS = {
    "GraphEraser": 1200,  # shard-based pipeline may exceed 10min for IM/hybrid
}

RUN_DIR_PATTERN = re.compile(r".*_seed(?P<seed>\d+)$")
ERROR_LOG_PATTERN = re.compile(
    r"^(?P<method>[^_]+)_(?P<dataset>[^_]+)_(?P<model>[^_]+)_r(?P<ratio>[^_]+)_s(?P<seed>\d+)_error\.log$"
)


def _parse_seed_from_run_dir(run_dir: Path):
    match = RUN_DIR_PATTERN.match(run_dir.name)
    if not match:
        return None
    try:
        return int(match.group("seed"))
    except ValueError:
        return None


def _ratio_text(ratio):
    return str(ratio)


def _json_name(method, dataset, model, ratio, seed):
    return f"{method}_{dataset}_{model}_r{_ratio_text(ratio)}_s{seed}.json"


def _result_key(method, dataset, model, ratio):
    return f"{method}_{dataset}_{model}_r{_ratio_text(ratio)}"


def _build_grid_items(config, seed, run_dir):
    items = []
    for method in config["methods"]:
        for dataset in config["datasets"]:
            for model in config["models"]:
                for ratio in config["ratios"]:
                    json_path = Path(run_dir) / _json_name(method, dataset, model, ratio, seed)
                    items.append({
                        "run_dir": str(run_dir),
                        "method": method,
                        "dataset": dataset,
                        "model": model,
                        "ratio": ratio,
                        "seed": seed,
                        "json_path": str(json_path),
                        "error_path": str(json_path).replace(".json", "_error.log"),
                    })
    return items


def _scan_missing_items_grid(run_dir, config, seed):
    expected_items = _build_grid_items(config, seed, run_dir)
    missing_items = [item for item in expected_items if not Path(item["json_path"]).exists()]
    return expected_items, missing_items


def _scan_missing_items_error_only(run_dir, seed):
    run_dir = Path(run_dir)
    expected_items = []
    missing_items = []
    for error_file in sorted(run_dir.glob("*_error.log")):
        match = ERROR_LOG_PATTERN.match(error_file.name)
        if not match:
            continue
        item_seed = int(match.group("seed"))
        if item_seed != seed:
            continue
        ratio_text = match.group("ratio")
        ratio_value = float(ratio_text)
        json_path = run_dir / f"{match.group('method')}_{match.group('dataset')}_{match.group('model')}_r{ratio_text}_s{item_seed}.json"
        item = {
            "run_dir": str(run_dir),
            "method": match.group("method"),
            "dataset": match.group("dataset"),
            "model": match.group("model"),
            "ratio": ratio_value,
            "seed": item_seed,
            "json_path": str(json_path),
            "error_path": str(error_file),
        }
        expected_items.append(item)
        if not json_path.exists():
            missing_items.append(item)
    return expected_items, missing_items


def _resolve_repair_run_dirs(repair_dir, seed_list, repair_select):
    repair_path = Path(repair_dir)
    if not repair_path.exists():
        raise FileNotFoundError(f"Repair directory not found: {repair_dir}")

    seed_filter = set(seed_list) if seed_list else None
    candidates = []

    direct_seed = _parse_seed_from_run_dir(repair_path)
    if direct_seed is not None:
        candidates = [repair_path]
    else:
        candidates = [p for p in repair_path.rglob("*") if p.is_dir() and _parse_seed_from_run_dir(p) is not None]

    if seed_filter is not None:
        candidates = [p for p in candidates if _parse_seed_from_run_dir(p) in seed_filter]

    if repair_select == "latest_per_seed":
        latest = {}
        for run_dir in candidates:
            seed = _parse_seed_from_run_dir(run_dir)
            prev = latest.get(seed)
            if prev is None or run_dir.name > prev.name:
                latest[seed] = run_dir
        candidates = list(latest.values())

    return sorted(candidates, key=lambda p: (_parse_seed_from_run_dir(p), p.name))


def _rebuild_summary_in_place(run_dir, config, seed, disable_cache, repair_meta, expected_items):
    run_dir = Path(run_dir)
    summary_path = run_dir / "_summary.json"
    old_summary = {}
    if summary_path.exists():
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                old_summary = json.load(f)
        except (json.JSONDecodeError, OSError):
            old_summary = {}

    result_map = {}
    for item in expected_items:
        json_path = Path(item["json_path"])
        if not json_path.exists():
            continue
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                result_map[_result_key(item["method"], item["dataset"], item["model"], item["ratio"])] = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

    total = len(expected_items)
    completed = len(result_map)
    failed = max(total - completed, 0)

    summary = old_summary.copy()
    summary["phase"] = old_summary.get("phase", f"Repair: {run_dir.parent.name}")
    summary["timestamp"] = old_summary.get("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
    summary["total_experiments"] = total
    summary["completed"] = completed
    summary["failed"] = failed
    summary["config"] = config
    summary["random_seed"] = seed
    summary["cache_enabled"] = not disable_cache
    summary["results"] = result_map

    history = summary.get("repair_meta", [])
    if not isinstance(history, list):
        history = [history]
    history.append(repair_meta)
    summary["repair_meta"] = history

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary


def _run_repair(config, cuda, repair_dir, seed_list, disable_cache=False, timeout_map=None,
                repair_select="latest_per_seed", repair_from="grid", repair_dry_run=False):
    run_dirs = _resolve_repair_run_dirs(repair_dir, seed_list, repair_select)
    if not run_dirs:
        print("[REPAIR] No target run directories found.")
        return

    print(f"[REPAIR] scan_dir={repair_dir} mode={repair_from} select={repair_select}")
    all_missing = []
    per_run = {}

    for run_dir in run_dirs:
        seed = _parse_seed_from_run_dir(run_dir)
        if seed is None:
            continue
        if repair_from == "grid":
            expected_items, missing_items = _scan_missing_items_grid(run_dir, config, seed)
        else:
            expected_items, missing_items = _scan_missing_items_error_only(run_dir, seed)
        per_run[str(run_dir)] = {
            "seed": seed,
            "expected_items": expected_items,
            "missing_items": missing_items,
            "success": 0,
            "failed": 0,
        }
        all_missing.extend(missing_items)

    if not all_missing:
        print("[REPAIR] No missing experiments found")
        return

    print(f"[REPAIR] Found {len(all_missing)} missing experiments:")
    for item in all_missing:
        print(f"[REPAIR]   {item['method']}/{item['dataset']}/{item['model']}/r={item['ratio']}/seed={item['seed']} @ {item['run_dir']}")

    if repair_dry_run:
        print("[REPAIR] Dry-run mode enabled. No experiments executed.")
        return

    print("[REPAIR] Running repair...")
    for item in all_missing:
        result = run_single_experiment(
            method=item["method"],
            dataset=item["dataset"],
            model=item["model"],
            strategies=config["strategies"],
            ratio=item["ratio"],
            cuda=cuda,
            output_dir=item["run_dir"],
            random_seed=item["seed"],
            disable_cache=disable_cache,
            timeout_map=timeout_map,
        )
        run_stats = per_run[item["run_dir"]]
        if result is not None and Path(item["json_path"]).exists():
            run_stats["success"] += 1
        else:
            run_stats["failed"] += 1

    for run_dir, stats in per_run.items():
        if not stats["expected_items"] or not stats["missing_items"]:
            continue
        repair_meta = {
            "repaired_at": datetime.now().isoformat(),
            "repair_from": repair_from,
            "repair_select": repair_select,
            "attempted": len(stats["missing_items"]),
            "success": stats["success"],
            "failed": stats["failed"],
        }
        summary = _rebuild_summary_in_place(
            run_dir=run_dir,
            config=config,
            seed=stats["seed"],
            disable_cache=disable_cache,
            repair_meta=repair_meta,
            expected_items=stats["expected_items"],
        )
        print(
            f"[REPAIR] DONE run={run_dir} "
            f"completed={summary.get('completed')}/{summary.get('total_experiments')} "
            f"failed={summary.get('failed')}"
        )


def run_single_experiment(
    method,
    dataset,
    model,
    strategies,
    ratio,
    cuda,
    output_dir,
    random_seed,
    disable_cache=False,
    timeout_map=None,
):
    """Run a single experiment via demo_attack.py subprocess with real-time output."""
    save_path = os.path.join(
        output_dir,
        f"{method}_{dataset}_{model}_r{ratio}_s{random_seed}.json"
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
        "--save_path", save_path,
    ]
    if disable_cache:
        cmd.append("--no_cache")

    label = f"{method}/{dataset}/{model}/r={ratio}/seed={random_seed}"
    timeout_s = 600
    if isinstance(timeout_map, dict):
        timeout_s = int(timeout_map.get(method, timeout_s))
    print(f"\n{'='*60}")
    print(f"  Running: {label}")
    print(f"  Strategies: {strategies}")
    print(f"  Timeout: {timeout_s}s")
    print(f"{'='*60}")

    # Set up environment for unbuffered output
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    start = time.time()
    output_lines = []

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env,
        )

        # Thread to read and display output in real-time
        def read_output():
            for line in proc.stdout:
                print(line, end='')  # Real-time print to terminal
                output_lines.append(line)

        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()

        # Wait for process with timeout
        remaining = timeout_s - (time.time() - start)
        if remaining <= 0:
            proc.kill()
            proc.wait()
            print(f"  TIMEOUT (>{timeout_s}s)")
            return None

        try:
            proc.wait(timeout=remaining)
            elapsed = time.time() - start
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            print(f"  TIMEOUT (>{timeout_s}s)")
            return None
        finally:
            output_thread.join(timeout=5)

        full_output = ''.join(output_lines)

        if proc.returncode != 0:
            print(f"  FAILED ({elapsed:.1f}s)")
            # Save error log
            err_path = save_path.replace(".json", "_error.log")
            with open(err_path, "w") as f:
                f.write(full_output)
            print(f"  Error log: {err_path}")
            # Print last few lines of error
            error_lines = full_output.strip().split("\n")
            for line in error_lines[-5:]:
                print(f"  | {line}")
            return None
        else:
            print(f"  OK ({elapsed:.1f}s)")
            # Extract summary from output
            for line in full_output.split("\n"):
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

    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def run_phase(phase_config, cuda, output_base, random_seed, disable_cache=False, timeout_map=None):
    """Run all experiments in a phase."""
    phase_name = phase_config["name"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(output_base, f"{timestamp}_seed{random_seed}")
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
    print(f"  Cache: {'disabled' if disable_cache else 'enabled'}")
    print(f"  Total experiments: {total}")
    print(f"  Output: {output_dir}")
    print(f"{'#'*70}")

    results = {}
    completed = 0
    failed = 0
    phase_start = time.time()

    # Build experiment list for progress bar
    exp_list = []
    for method in methods:
        for dataset in datasets:
            for model in models:
                for ratio in ratios:
                    exp_list.append((method, dataset, model, ratio))

    # Run experiments with progress bar
    with tqdm(total=len(exp_list), desc=phase_name, unit="exp",
              leave=True, ncols=80) as pbar:
        for method, dataset, model, ratio in exp_list:
            key = f"{method}_{dataset}_{model}_r{ratio}"
            result = run_single_experiment(
                method,
                dataset,
                model,
                strategies,
                ratio,
                cuda,
                output_dir,
                random_seed,
                disable_cache,
                timeout_map,
            )
            if result is not None:
                results[key] = result
                completed += 1
            else:
                failed += 1
            pbar.update(1)
            pbar.set_postfix({"completed": completed, "failed": failed})

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
        "random_seed": random_seed,
        "cache_enabled": not disable_cache,
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
    parser.add_argument("--seeds", type=str, default=None,
                        help="Comma-separated seeds, e.g. 2024,2025,2026")
    parser.add_argument("--no_cache", action="store_true",
                        help="Disable cache in demo_attack.py subprocess calls")
    parser.add_argument("--method_timeouts", type=str, default=None,
                        help="Per-method timeout overrides, e.g. GraphEraser:1200,GIF:900")
    parser.add_argument("--repair", action="store_true",
                        help="Repair missing experiments in-place without creating new run directories")
    parser.add_argument("--repair_dir", type=str, default=None,
                        help="Target run dir or parent dir to scan in repair mode")
    parser.add_argument("--repair_select", type=str, choices=["latest_per_seed", "all_runs"],
                        default="latest_per_seed",
                        help="When repair_dir is a parent dir, choose latest run per seed or all runs")
    parser.add_argument("--repair_from", type=str, choices=["grid", "error_only"],
                        default="grid",
                        help="Repair source: missing grid items or error.log-only items")
    parser.add_argument("--repair_dry_run", action="store_true",
                        help="Show missing items in repair mode without executing experiments")

    # Custom overrides
    parser.add_argument("--methods", type=str, default=None,
                        help="Comma-separated methods (overrides phase config)")
    parser.add_argument("--datasets", type=str, default=None,
                        help="Comma-separated datasets (overrides phase config)")
    parser.add_argument("--base_model", type=str, default=None,
                        help="Base model (overrides phase config, e.g. GCN, GAT, SGC)")
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

    seed_list = [args.random_seed]
    if args.seeds:
        seed_list = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]

    timeout_map = METHOD_TIMEOUTS.copy()
    if args.method_timeouts:
        for item in args.method_timeouts.split(","):
            item = item.strip()
            if not item or ":" not in item:
                continue
            method, value = item.split(":", 1)
            method = method.strip()
            value = value.strip()
            try:
                timeout_map[method] = int(value)
            except ValueError:
                print(f"[WARN] Invalid timeout override ignored: {item}")

    def apply_overrides(base_config):
        config = base_config.copy()
        if args.methods:
            config["methods"] = args.methods.split(",")
        if args.datasets:
            config["datasets"] = args.datasets.split(",")
        if args.base_model:
            config["models"] = [args.base_model]
        if args.strategies:
            config["strategies"] = args.strategies
        if args.ratios:
            config["ratios"] = [float(r) for r in args.ratios.split(",")]
        return config

    if args.repair:
        if not args.repair_dir:
            parser.error("--repair requires --repair_dir")
        if len(phase_list) > 1:
            print(f"[WARN] --repair ignores multiple phases; using {phase_list[0]}")
        config = apply_overrides(phases[phase_list[0]])
        _run_repair(
            config=config,
            cuda=args.cuda,
            repair_dir=args.repair_dir,
            seed_list=seed_list,
            disable_cache=args.no_cache,
            timeout_map=timeout_map,
            repair_select=args.repair_select,
            repair_from=args.repair_from,
            repair_dry_run=args.repair_dry_run,
        )
        return

    for phase_key in phase_list:
        config = apply_overrides(phases[phase_key])

        output_dir = os.path.join(args.output, f"phase_{phase_key.lower()}")
        for seed in seed_list:
            run_phase(config, args.cuda, output_dir, seed, args.no_cache, timeout_map)


if __name__ == "__main__":
    main()
