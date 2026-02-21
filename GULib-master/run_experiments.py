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
import ast
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
STRATEGIES_COMPARE_PATTERN = re.compile(r"Strategies to compare:\s*(\[[^\n]+\])")
STRATEGIES_DICT_PATTERN = re.compile(r"'strategies'\s*:\s*(\[[^\]]+\])")


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


def _normalize_strategies(raw):
    if raw is None:
        return None
    if isinstance(raw, str):
        values = [s.strip() for s in raw.split(",") if s.strip()]
    elif isinstance(raw, (list, tuple)):
        values = [str(s).strip() for s in raw if str(s).strip()]
    else:
        return None
    if not values:
        return None
    return ",".join(values)


def _load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _parse_strategies_literal(text):
    try:
        parsed = ast.literal_eval(text)
    except (SyntaxError, ValueError):
        return None
    return _normalize_strategies(parsed)


def _parse_strategies_from_error_log(error_file):
    try:
        with open(error_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except OSError:
        return None

    match = STRATEGIES_COMPARE_PATTERN.search(text)
    if match:
        parsed = _parse_strategies_literal(match.group(1))
        if parsed:
            return parsed

    match = STRATEGIES_DICT_PATTERN.search(text)
    if match:
        parsed = _parse_strategies_literal(match.group(1))
        if parsed:
            return parsed

    return None


def _resolve_run_strategies(run_dir, fallback_strategies):
    run_dir = Path(run_dir)

    summary = _load_json_file(run_dir / "_summary.json")
    if isinstance(summary, dict):
        config = summary.get("config")
        if isinstance(config, dict):
            strategies = _normalize_strategies(config.get("strategies"))
            if strategies:
                return strategies, "summary"

    for json_file in sorted(run_dir.glob("*.json")):
        if json_file.name == "_summary.json":
            continue
        data = _load_json_file(json_file)
        if not isinstance(data, dict):
            continue
        config = data.get("config")
        if not isinstance(config, dict):
            continue
        strategies = _normalize_strategies(config.get("strategies"))
        if strategies:
            return strategies, f"result_json:{json_file.name}"

    for error_file in sorted(run_dir.glob("*_error.log")):
        strategies = _parse_strategies_from_error_log(error_file)
        if strategies:
            return strategies, f"error_log:{error_file.name}"

    fallback = _normalize_strategies(fallback_strategies)
    if fallback:
        return fallback, "fallback"

    return "random,degree,pagerank,tracin", "fallback_default"


def _collect_result_map(expected_items):
    result_map = {}
    for item in expected_items:
        json_path = Path(item["json_path"])
        if not json_path.exists():
            continue
        data = _load_json_file(json_path)
        if data is None:
            continue
        result_map[_result_key(item["method"], item["dataset"], item["model"], item["ratio"])] = data
    return result_map


def _summary_needs_rebuild(run_dir, total, completed, failed, result_keys):
    summary = _load_json_file(Path(run_dir) / "_summary.json")
    if not isinstance(summary, dict):
        return True
    if summary.get("total_experiments") != total:
        return True
    if summary.get("completed") != completed:
        return True
    if summary.get("failed") != failed:
        return True
    summary_results = summary.get("results")
    if not isinstance(summary_results, dict):
        return True
    return set(summary_results.keys()) != set(result_keys)


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
        try:
            ratio_value = float(ratio_text)
        except ValueError:
            ratio_value = ratio_text
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


def _resolve_repair_targets(repair_dir, seed_list, repair_select):
    repair_path = Path(repair_dir)
    if not repair_path.exists():
        raise FileNotFoundError(f"Repair directory not found: {repair_dir}")

    seed_filter = sorted(set(seed_list)) if seed_list else []
    seed_filter_set = set(seed_filter) if seed_filter else None

    direct_seed = _parse_seed_from_run_dir(repair_path)
    if direct_seed is not None:
        if seed_filter_set is None or direct_seed in seed_filter_set:
            return [{
                "seed": direct_seed,
                "run_dir": repair_path,
                "is_new": False,
            }]
        return []

    candidates = [p for p in repair_path.rglob("*") if p.is_dir() and _parse_seed_from_run_dir(p) is not None]
    if seed_filter_set is not None:
        candidates = [p for p in candidates if _parse_seed_from_run_dir(p) in seed_filter_set]

    by_seed = {}
    for run_dir in candidates:
        seed = _parse_seed_from_run_dir(run_dir)
        by_seed.setdefault(seed, []).append(run_dir)
    for seed in by_seed:
        by_seed[seed].sort(key=lambda p: p.name)

    if seed_filter:
        target_seeds = seed_filter
    else:
        target_seeds = sorted(by_seed.keys())

    targets = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if repair_select == "all_runs":
        for seed in target_seeds:
            runs = by_seed.get(seed, [])
            if runs:
                for run_dir in runs:
                    targets.append({"seed": seed, "run_dir": run_dir, "is_new": False})
            else:
                targets.append({
                    "seed": seed,
                    "run_dir": repair_path / f"{timestamp}_seed{seed}",
                    "is_new": True,
                })
        return targets

    for seed in target_seeds:
        runs = by_seed.get(seed, [])
        if runs:
            targets.append({"seed": seed, "run_dir": runs[-1], "is_new": False})
        else:
            targets.append({
                "seed": seed,
                "run_dir": repair_path / f"{timestamp}_seed{seed}",
                "is_new": True,
            })

    return targets


def _rebuild_summary_in_place(
    run_dir,
    config,
    seed,
    disable_cache,
    repair_meta,
    expected_items,
    resolved_strategies,
):
    run_dir = Path(run_dir)
    summary_path = run_dir / "_summary.json"
    old_summary = {}
    loaded = _load_json_file(summary_path)
    if isinstance(loaded, dict):
        old_summary = loaded

    result_map = _collect_result_map(expected_items)

    total = len(expected_items)
    completed = len(result_map)
    failed = max(total - completed, 0)

    summary = old_summary.copy()
    summary["phase"] = old_summary.get("phase", config.get("name", f"Repair: {run_dir.parent.name}"))
    summary["timestamp"] = old_summary.get("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
    summary["total_experiments"] = total
    summary["completed"] = completed
    summary["failed"] = failed
    summary_config = {}
    if isinstance(old_summary.get("config"), dict):
        summary_config = old_summary["config"].copy()
    for key in ("name", "methods", "datasets", "models", "ratios"):
        if key in config:
            summary_config[key] = config[key]
    summary_config["strategies"] = resolved_strategies
    summary["config"] = summary_config
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
    targets = _resolve_repair_targets(repair_dir, seed_list, repair_select)
    if not targets:
        print("[REPAIR] No target run directories found.")
        return

    print(f"[REPAIR] scan_dir={repair_dir} mode={repair_from} select={repair_select}")
    all_missing = []
    per_run = {}
    summary_only_runs = []
    fallback_strategies = config.get("strategies", "")

    for target in targets:
        run_dir = Path(target["run_dir"])
        run_key = str(run_dir)
        seed = int(target["seed"])
        is_new = bool(target["is_new"])

        effective_repair_from = repair_from
        if is_new and repair_from == "error_only":
            effective_repair_from = "grid"

        if effective_repair_from == "grid":
            expected_items, missing_items = _scan_missing_items_grid(run_dir, config, seed)
        else:
            expected_items, missing_items = _scan_missing_items_error_only(run_dir, seed)

        strategies, strategy_source = _resolve_run_strategies(run_dir, fallback_strategies)
        existing_result_map = _collect_result_map(expected_items)
        total = len(expected_items)
        completed = len(existing_result_map)
        failed_count = max(total - completed, 0)
        summary_needs_rebuild = is_new or _summary_needs_rebuild(
            run_dir=run_dir,
            total=total,
            completed=completed,
            failed=failed_count,
            result_keys=existing_result_map.keys(),
        )

        per_run[run_key] = {
            "seed": seed,
            "run_dir": run_dir,
            "is_new": is_new,
            "expected_items": expected_items,
            "missing_items": missing_items,
            "attempted": len(missing_items),
            "success": 0,
            "failed_exec": 0,
            "summary_needs_rebuild": summary_needs_rebuild,
            "effective_repair_from": effective_repair_from,
            "strategies": strategies,
            "strategies_source": strategy_source,
        }

        state = "NEW_RUN" if is_new else "EXISTING_RUN"
        print(
            f"[REPAIR] {state} seed={seed} run={run_dir} "
            f"missing={len(missing_items)} "
            f"strategies={strategies} source={strategy_source}"
        )

        if summary_needs_rebuild and not missing_items:
            summary_only_runs.append(run_key)

        all_missing.extend(missing_items)

    if all_missing:
        print(f"[REPAIR] Found {len(all_missing)} missing experiments:")
        for item in all_missing:
            print(f"[REPAIR]   {item['method']}/{item['dataset']}/{item['model']}/r={item['ratio']}/seed={item['seed']} @ {item['run_dir']}")
    else:
        print("[REPAIR] No missing experiments found")

    if summary_only_runs:
        print(f"[REPAIR] Found {len(summary_only_runs)} runs with inconsistent summary metadata")

    if not all_missing and not summary_only_runs:
        return

    if repair_dry_run:
        print("[REPAIR] Dry-run mode enabled. No experiments executed.")
        return

    if all_missing:
        print("[REPAIR] Running repair...")
    for item in all_missing:
        run_stats = per_run[item["run_dir"]]
        run_dir = run_stats["run_dir"]
        if run_stats["is_new"]:
            os.makedirs(run_dir, exist_ok=True)
        result = run_single_experiment(
            method=item["method"],
            dataset=item["dataset"],
            model=item["model"],
            strategies=run_stats["strategies"],
            ratio=item["ratio"],
            cuda=cuda,
            output_dir=str(run_dir),
            random_seed=item["seed"],
            disable_cache=disable_cache,
            timeout_map=timeout_map,
        )
        if result is not None and Path(item["json_path"]).exists():
            run_stats["success"] += 1
        else:
            run_stats["failed_exec"] += 1

    for run_dir, stats in per_run.items():
        should_rebuild_summary = stats["summary_needs_rebuild"] or stats["attempted"] > 0
        if not stats["expected_items"] or not should_rebuild_summary:
            continue
        repair_meta = {
            "repaired_at": datetime.now().isoformat(),
            "repair_mode": "auto",
            "seed": stats["seed"],
            "repair_from": stats["effective_repair_from"],
            "repair_select": repair_select,
            "attempted": stats["attempted"],
            "success": stats["success"],
            "failed": stats["failed_exec"],
            "summary_only": stats["attempted"] == 0,
            "strategies_source": stats["strategies_source"],
            "strategies_used": stats["strategies"],
        }
        summary = _rebuild_summary_in_place(
            run_dir=run_dir,
            config=config,
            seed=stats["seed"],
            disable_cache=disable_cache,
            repair_meta=repair_meta,
            expected_items=stats["expected_items"],
            resolved_strategies=stats["strategies"],
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
                stripped = line.strip()
                if not stripped:
                    continue
                if "Rank" in stripped and "Strategy" in stripped:
                    print(f"  {stripped}")
                    continue
                if "Best Strategy" in stripped:
                    print(f"  {stripped}")
                    continue
                if re.match(r"^\d+\s+", stripped):
                    print(f"  {stripped}")

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
                        help="Auto repair mode: patch missing items in latest runs, create new run only for missing seeds")
    parser.add_argument("--repair_dir", type=str, default=None,
                        help="Optional target run dir or parent dir. Defaults to <output>/phase_<phase>")
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
        if len(phase_list) > 1:
            print(f"[WARN] --repair ignores multiple phases; using {phase_list[0]}")
        repair_phase = phase_list[0]
        repair_dir = args.repair_dir or os.path.join(args.output, f"phase_{repair_phase.lower()}")
        config = apply_overrides(phases[phase_list[0]])
        _run_repair(
            config=config,
            cuda=args.cuda,
            repair_dir=repair_dir,
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
