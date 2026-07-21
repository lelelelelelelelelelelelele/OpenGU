"""
run_all_baselines.py - Batch-generate K=5 random baselines for ALL experiment configs.

Iterates over all (method, dataset, model, seed) combos used in the project,
runs generate_baseline.py for each, then averages per-seed results into a
single canonical baseline file per (method, dataset, model).

The averaged baseline file is what eval_relative.py reads.

Usage:
    python experiments/baseline_k5/run_all_baselines.py
    python experiments/baseline_k5/run_all_baselines.py --baseline_k 5
"""
import os
import sys
import json
import subprocess
import numpy as np
from pathlib import Path
from datetime import datetime

try:
    from .baseline_contract import (
        BEFORE_METRIC,
        SCHEMA,
        SCHEMA_VERSION,
        default_result_root,
        expected_before_metric_source,
        expected_config,
        load_valid_record,
    )
except ImportError:
    from baseline_contract import (
        BEFORE_METRIC,
        SCHEMA,
        SCHEMA_VERSION,
        default_result_root,
        expected_before_metric_source,
        expected_config,
        load_valid_record,
    )

# ============================================================
# Configuration: mirrors self/generalization_experiment_checklist.md
# Each entry = (dataset, model, [methods])
# ============================================================
EXPERIMENTS = [
    # MG-0: 稳定性 — Cora / GCN / 3 methods
    ('cora',     'GCN', ['GIF', 'GNNDelete', 'GraphEraser']),
    # MG-1: 跨数据集 — Citeseer / GCN / 3 methods
    ('citeseer', 'GCN', ['GIF', 'GNNDelete', 'GraphEraser']),
    # MG-2: 跨模型 — Cora / GAT / 3 methods
    ('cora',     'GAT', ['GIF', 'GNNDelete', 'GraphEraser']),
    # MG-3a: 扩展方法 — Citeseer / GCN / IDEA, MEGU
    ('citeseer', 'GCN', ['IDEA', 'MEGU']),
    # MG-3b: 扩展方法 — Cora / GAT / IDEA, MEGU
    ('cora',     'GAT', ['IDEA', 'MEGU']),
    # P2-EXT: GIF Extension — GAT/GIN models across datasets
    ('citeseer', 'GAT', ['GIF']),
    ('cora',     'GIN', ['GIF']),
    ('citeseer', 'GIN', ['GIF']),
]
SEEDS = [111, 333, 555, 777, 999]  # Independent from main experiment seeds (42,212,722,1337,2024)
BASELINE_K = 5
DATASET_NUM_NODES = {'cora': 2708, 'citeseer': 3327, 'pubmed': 19717}
METHOD_EXTRA_ARGS = {
    # GraphRevoker's supported partition default for the current runner.
    'GraphRevoker': ['--partition_method', 'gpa'],
}

# Resolve paths
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = SCRIPT_DIR.parent.parent
GENERATE_SCRIPT = SCRIPT_DIR / "generate_baseline.py"
BASELINE_ROOT = default_result_root(REPO_ROOT)

# Python executable: use the gnn conda env if available
PYTHON_BIN = sys.executable


def run_single_baseline(method, dataset, model, seed, baseline_k):
    """Run generate_baseline.py for a single configuration."""
    cmd = [
        PYTHON_BIN,
        str(GENERATE_SCRIPT),
        '--dataset_name', dataset,
        '--base_model', model,
        '--unlearning_methods', method,
        '--random_seed', str(seed),
        '--baseline_k', str(baseline_k),
        '--output_root', str(BASELINE_ROOT),
        '--root_path', str(REPO_ROOT.resolve()),
        '--processed_root', str((REPO_ROOT / 'data' / 'processed').resolve()),
        '--unlearn_ratio', str(baseline_k / DATASET_NUM_NODES[dataset]),
        '--proportion_unlearned_nodes', str(baseline_k / DATASET_NUM_NODES[dataset]),
    ]
    cmd.extend(METHOD_EXTRA_ARGS.get(method, []))
    
    cache_file = BASELINE_ROOT / method / dataset / model / f"baseline_seed{seed}_k{baseline_k}.json"
    if cache_file.exists():
        expected = expected_config(
            dataset=dataset, model=model, method=method, seed=seed, k=baseline_k
        )
        try:
            load_valid_record(cache_file, expected)
        except Exception as exc:
            print(f"  [STALE] Refusing incompatible output: {cache_file}")
            print(f"          {exc}")
            return False
        print(f"  [SKIP] Compatible v2 artifact exists: seed={seed}")
        return True
    
    print(f"  [RUN]  Generating: seed={seed} ...")
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=600  # 10 min timeout per run
        )
        if result.returncode != 0:
            print(f"  [FAIL] seed={seed}, returncode={result.returncode}")
            if result.stderr:
                # Print last 5 lines of stderr 
                lines = result.stderr.strip().split('\n')
                for line in lines[-5:]:
                    print(f"         {line}")
            return False
        print(f"  [OK]   seed={seed}")
        return True
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] seed={seed}")
        return False
    except Exception as e:
        print(f"  [ERROR] seed={seed}: {e}")
        return False


def compute_averaged_baseline(method, dataset, model, baseline_k):
    """
    Read all per-seed baseline files for a (method, dataset, model) combo,
    average them, and write a canonical 'baseline_averaged_k{k}.json'.
    """
    cache_dir = BASELINE_ROOT / method / dataset / model
    if not cache_dir.exists():
        return None
    
    f1_afters = []
    f1_befores = []
    f1_drops = []
    method_perf_befores = []
    method_noise_drops = []
    seed_details = []
    
    for seed in SEEDS:
        seed_file = cache_dir / f"baseline_seed{seed}_k{baseline_k}.json"
        if not seed_file.exists():
            print(f"  [WARN] Missing seed={seed} for averaging")
            continue
        try:
            data = load_valid_record(
                seed_file,
                expected_config(
                    dataset=dataset,
                    model=model,
                    method=method,
                    seed=seed,
                    k=baseline_k,
                ),
            )
            f1_after = data.get('f1_after')
            f1_before = data.get('f1_before')
            f1_drop = data.get('f1_drop')
            method_perf_before = data.get('method_perf_before')
            method_noise_drop = data.get('method_noise_drop')
            
            if f1_after is not None:
                f1_afters.append(f1_after)
            if f1_before is not None:
                f1_befores.append(f1_before)
            if f1_drop is not None:
                f1_drops.append(f1_drop)
            if method_perf_before is not None:
                method_perf_befores.append(method_perf_before)
            if method_noise_drop is not None:
                method_noise_drops.append(method_noise_drop)
                
            seed_details.append({
                'seed': seed,
                'f1_after': f1_after,
                'f1_before': f1_before,
                'f1_drop': f1_drop,
                'method_perf_before': method_perf_before,
                'method_noise_drop': method_noise_drop,
            })
        except Exception as e:
            print(f"  [WARN] Failed to read seed={seed}: {e}")
    
    if len(f1_afters) != len(SEEDS) or len(method_perf_befores) != len(SEEDS):
        print(
            f"  [ERROR] Incomplete v2 aggregate: "
            f"after={len(f1_afters)}/{len(SEEDS)}, "
            f"before={len(method_perf_befores)}/{len(SEEDS)}"
        )
        return None
    
    averaged = {
        'schema': SCHEMA,
        'schema_version': SCHEMA_VERSION,
        'f1_after': float(np.mean(f1_afters)),
        'f1_after_std': float(np.std(f1_afters)),
        'f1_before': float(np.mean(f1_befores)) if f1_befores else None,
        'f1_drop': float(np.mean(f1_drops)) if f1_drops else None,
        'method_perf_before': float(np.mean(method_perf_befores)) if method_perf_befores else None,
        'method_noise_drop': float(np.mean(method_noise_drops)) if method_noise_drops else None,
        'n_seeds': len(f1_afters),
        'seeds_used': [d['seed'] for d in seed_details if d['f1_after'] is not None],
        'per_seed_details': seed_details,
        'config': {
            'dataset_name': dataset,
            'base_model': model,
            'unlearning_methods': method,
            'k': baseline_k,
            'strategy': 'random',
            'averaged': True,
            'before_metric': BEFORE_METRIC,
            'before_metric_source': expected_before_metric_source(method),
            'output_root': str(BASELINE_ROOT.resolve()),
            'timestamp': datetime.now().isoformat(),
        }
    }
    
    avg_file = cache_dir / f"baseline_averaged_k{baseline_k}.json"
    with open(avg_file, 'w', encoding='utf-8') as f:
        json.dump(averaged, f, indent=2)
    
    print(f"  [AVG]  f1_after={averaged['f1_after']:.4f} ± {averaged['f1_after_std']:.4f}  (n={averaged['n_seeds']} seeds)")
    print(f"         Saved to: {avg_file}")
    return averaged


def main():
    # Parse optional baseline_k from CLI
    baseline_k = BASELINE_K
    for i, arg in enumerate(sys.argv[1:]):
        if arg == '--baseline_k' and i + 1 < len(sys.argv) - 1:
            baseline_k = int(sys.argv[i + 2])
        elif arg.startswith('--baseline_k='):
            baseline_k = int(arg.split('=', 1)[1])
    
    # Count total combos
    total_combos = sum(len(methods) for _, _, methods in EXPERIMENTS)
    total_runs = total_combos * len(SEEDS)
    
    print("=" * 70)
    print(f"Batch Baseline Generation (K={baseline_k})")
    print(f"  Experiment groups: {len(EXPERIMENTS)}")
    for ds, mdl, methods in EXPERIMENTS:
        print(f"    {ds}/{mdl}: {methods}")
    print(f"  Seeds:     {SEEDS}")
    print(f"  Total:     {total_combos} combos × {len(SEEDS)} seeds = {total_runs} runs")
    print("=" * 70)
    
    combo_idx = 0
    summary = []
    
    for dataset, model, methods in EXPERIMENTS:
        for method in methods:
            combo_idx += 1
            print(f"\n[{combo_idx}/{total_combos}] {method} / {dataset} / {model}")
            print("-" * 50)
            
            # Phase 1: Generate per-seed baselines
            successes = 0
            for seed in SEEDS:
                ok = run_single_baseline(method, dataset, model, seed, baseline_k)
                if ok:
                    successes += 1
            
            # Phase 2: Average across seeds
            if successes == len(SEEDS):
                avg = compute_averaged_baseline(method, dataset, model, baseline_k)
                summary.append({
                    'method': method,
                    'dataset': dataset,
                    'model': model,
                    'seeds_ok': successes,
                    'seeds_total': len(SEEDS),
                    'f1_after_avg': avg['f1_after'] if avg else None,
                })
            else:
                print(f"  [SKIP] Incomplete per-seed run; refusing aggregate")
                summary.append({
                    'method': method,
                    'dataset': dataset,
                    'model': model,
                    'seeds_ok': 0,
                    'seeds_total': len(SEEDS),
                    'f1_after_avg': None,
                })
    
    # Final summary table
    print("\n" + "=" * 70)
    print("BATCH BASELINE SUMMARY")
    print("=" * 70)
    header = f"{'Method':<14}| {'Dataset':<10}| {'Model':<6}| {'Seeds':>6} | {'Avg F1':>8}"
    print(header)
    print("-" * 70)
    for s in summary:
        f1_str = f"{s['f1_after_avg']:.4f}" if s['f1_after_avg'] is not None else "N/A"
        print(f"{s['method']:<14}| {s['dataset']:<10}| {s['model']:<6}| {s['seeds_ok']:>2}/{s['seeds_total']:<3} | {f1_str:>8}")
    print("=" * 70)
    
    # Save summary
    summary_file = BASELINE_ROOT / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    BASELINE_ROOT.mkdir(parents=True, exist_ok=True)
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'config': {
                'experiments': [{'dataset': d, 'model': m, 'methods': mths} for d, m, mths in EXPERIMENTS],
                'seeds': SEEDS,
                'baseline_k': baseline_k,
            },
            'results': summary,
            'timestamp': datetime.now().isoformat(),
        }, f, indent=2)
    print(f"\nBatch summary saved to: {summary_file}")


if __name__ == '__main__':
    main()
