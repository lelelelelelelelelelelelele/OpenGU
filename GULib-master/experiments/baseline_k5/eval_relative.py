"""
eval_relative.py - Compute real attack metrics by factoring out protective behavior.

Extracts the environment baseline from highly specific random minimal attacks (K=5)
and compares it with genuine substantive attacks to measure true disruption.

Usage:
    python experiments/baseline_k5/eval_relative.py \
        --dataset_name cora \
        --base_model GCN \
        --unlearning_methods GraphEraser \
        --strategies im_v4,tracin \
        --unlearn_ratio 0.05 \
        --random_seed 2024 \
        --baseline_k 5
"""
import os
import sys
import json
import numpy as np
import torch
from pathlib import Path
from datetime import datetime

# Extract custom args BEFORE parameter_parser (which rejects unknown args)
_strategies_str = 'im_v4,tracin,hybrid_v4'
_baseline_k = 5
_repair_mode = False
_repair_dry_run = False
_raw_args = list(sys.argv[1:])
_filtered_argv = []
_i = 0
while _i < len(_raw_args):
    _arg = _raw_args[_i]
    if _arg == '--strategies':
        if _i + 1 < len(_raw_args):
            _strategies_str = _raw_args[_i + 1]
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--strategies='):
        _strategies_str = _arg.split('=', 1)[1]
    elif _arg == '--baseline_k':
        if _i + 1 < len(_raw_args):
            _baseline_k = int(_raw_args[_i + 1])
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--baseline_k='):
        _baseline_k = int(_arg.split('=', 1)[1])
    elif _arg == '--repair':
        _repair_mode = True
    elif _arg == '--repair_dry_run':
        _repair_mode = True
        _repair_dry_run = True
    else:
        _filtered_argv.append(_arg)
    _i += 1
sys.argv = [sys.argv[0]] + _filtered_argv

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser
from attack.pipeline_adapter import AttackPipeline
from attack.attack_strategies import RandomStrategy
from attack.result_cache import ResultCache


def find_cache_entry_for_attack(cache: ResultCache, args: dict, strategy_name: str):
    import json as _json
    target = {
        'dataset_name': str(args.get('dataset_name', '')),
        'base_model': str(args.get('base_model', '')),
        'unlearning_methods': str(args.get('unlearning_methods', '')),
        'strategy_name': strategy_name,
    }
    target_ratio = float(args.get('unlearn_ratio', 0.05))
    target_seed = args.get('random_seed', args.get('seed', 2024))
    try:
        target_seed = int(target_seed)
    except (TypeError, ValueError):
        target_seed = None

    cache_dir = Path(cache.cache_dir)
    if not cache_dir.exists():
        return None

    target_k = args.get('k')
    best_match = None
    best_k = None  # track k to prefer explicit-k entries over legacy (k=None)

    for fpath in cache_dir.glob('*.json'):
        try:
            with open(fpath, encoding='utf-8') as f:
                data = _json.load(f)
            c = data.get('config', {})
            cache_seed = c.get('random_seed', c.get('seed'))
            if cache_seed is None:
                cache_seed = 2024
            try:
                cache_seed = int(cache_seed)
            except (TypeError, ValueError):
                continue

            if target_seed is not None and cache_seed != target_seed:
                continue

            if (str(c.get('dataset_name', '')) == target['dataset_name'] and
                str(c.get('base_model', '')) == target['base_model'] and
                str(c.get('unlearning_methods', '')) == target['unlearning_methods'] and
                str(c.get('strategy_name', '')) == target['strategy_name'] and
                abs(float(c.get('unlearn_ratio', -1)) - target_ratio) < 1e-6):
                cache_k = c.get('k')

                # If target_k is specified, require exact match
                if target_k is not None:
                    if cache_k is None or int(cache_k) != int(target_k):
                        continue
                    return data.get('result', {})

                # No target_k: prefer entries with explicit k over legacy (k=None)
                if best_match is None:
                    best_match = data
                    best_k = cache_k
                elif cache_k is not None and best_k is None:
                    best_match = data
                    best_k = cache_k
        except Exception:
            continue

    if best_match is not None:
        return best_match.get('result', {})
    return None


def get_baseline_from_cache(args: dict, baseline_k: int) -> dict:
    """
    Load baseline data. Priority:
      1. Averaged baseline (from run_all_baselines.py) — cross-seed mean
      2. Per-seed baseline (from generate_baseline.py) — single seed fallback
    """
    dataset = args.get('dataset_name', 'cora')
    model = args.get('base_model', 'GCN')
    method = args.get('unlearning_methods', 'GraphEraser')
    seed = int(args.get('random_seed', 2024))
    
    cache_dir = Path(f"./results/baseline/k5_random/{method}/{dataset}/{model}")
    
    # Priority 1: averaged baseline (recommended, generated by run_all_baselines.py)
    avg_file = cache_dir / f"baseline_averaged_k{baseline_k}.json"
    if avg_file.exists():
        try:
            with open(avg_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            n = data.get('n_seeds', '?')
            print(f"  [Baseline] Using AVERAGED baseline (n={n} seeds)")
            return data
        except Exception:
            pass
    
    # Priority 2: per-seed fallback
    seed_file = cache_dir / f"baseline_seed{seed}_k{baseline_k}.json"
    if seed_file.exists():
        try:
            with open(seed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  [Baseline] WARNING: Using single-seed baseline (seed={seed}). "
                  f"Run `run_all_baselines.py` to generate averaged baseline.")
            return data
        except Exception:
            pass
            
    return None


def _matches_relative_config(config: dict, args: dict, target_seed: int):
    if str(config.get('dataset_name', '')) != str(args.get('dataset_name', '')): return False
    if str(config.get('base_model', '')) != str(args.get('base_model', '')): return False
    if str(config.get('unlearning_methods', '')) != str(args.get('unlearning_methods', '')): return False
    if abs(float(config.get('unlearn_ratio', -1)) - float(args.get('unlearn_ratio', 0.05))) > 1e-6: return False
    
    cfg_seed = config.get('random_seed', config.get('seed'))
    if cfg_seed is None: return False
    try:
        cfg_seed = int(cfg_seed)
    except (TypeError, ValueError):
        return False
    return cfg_seed == target_seed


def _scan_existing_relative(args: dict, target_seed: int):
    out_dir = Path(f"./results/relative/{args['unlearning_methods']}/{args['dataset_name']}/{args['base_model']}")
    strategy_map = {}
    if not out_dir.exists():
        return strategy_map
        
    for path in sorted(out_dir.glob("relative_seed*.json"), key=lambda p: p.stat().st_mtime):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            continue
            
        if not _matches_relative_config(data.get('config', {}), args, target_seed):
            continue
            
        for result in data.get('results', []):
            strategy = result.get('strategy')
            if strategy:
                strategy_map[strategy] = result
                
    return strategy_map


def main():
    strategies = [s.strip() for s in _strategies_str.split(',') if s.strip()]
    args = parameter_parser()
    
    passed_unlearn_ratio = any(
        a == '--unlearn_ratio' or str(a).startswith('--unlearn_ratio=')
        for a in sys.argv[1:]
    )
    if not passed_unlearn_ratio:
        args['unlearn_ratio'] = 0.05
        
    args['proportion_unlearned_nodes'] = args['unlearn_ratio']
    
    print(f"Dataset: {args['dataset_name']}, Model: {args['base_model']}, Method: {args['unlearning_methods']}")
    print(f"Seed: {args['random_seed']}, Unlearn Ratio: {args['unlearn_ratio']}, Baseline K: {_baseline_k}")
    print(f"Strategies: {strategies}")
    print("=" * 80)
    
    target_seed = int(args.get('random_seed', 2024))
    
    existing_results_by_strategy = {}
    strategies_to_run = list(strategies)
    completed_before = []

    if _repair_mode:
        existing_results_by_strategy = _scan_existing_relative(args, target_seed)
        completed_before = [s for s in strategies if s in existing_results_by_strategy]
        strategies_to_run = [s for s in strategies if s not in existing_results_by_strategy]

        print(
            f"[REPAIR] requested={len(strategies)} "
            f"completed_before={len(completed_before)} "
            f"missing={len(strategies_to_run)}"
        )
        if strategies_to_run:
            print(f"[REPAIR] missing_strategies={','.join(strategies_to_run)}")
        else:
            print("[REPAIR] No missing strategies found. Exiting.")
            return
        if _repair_dry_run:
            print("[REPAIR] Dry-run mode enabled. Exiting.")
            return
    
    baseline_data = get_baseline_from_cache(args, _baseline_k)
    
    if baseline_data is None:
        print(f"\n[ERROR] Missing Baseline! Could not find K={_baseline_k} random extraction for:")
        print(f"        Dataset={args['dataset_name']}, Model={args['base_model']}, Method={args['unlearning_methods']}, Seed={target_seed}")
        print(f"        => Action: Please run `python experiments/baseline_k5/generate_baseline.py` with these exact parameters first.")
        return
        
    baseline_f1_after = baseline_data.get('f1_after')
    if baseline_f1_after is None:
        print(f"\n[ERROR] Baseline cache was found but lacks 'f1_after' data.")
        return
        
    print(f"\n[Baseline] {args['unlearning_methods']} Random K={_baseline_k} f1_after: {baseline_f1_after:.4f}\n")
    
    cache = ResultCache(cache_dir="./results/cache")
    all_results = []
    
    print("--- Strategy Evaluation ---")
    for strategy_name in strategies_to_run:
        attack_data = find_cache_entry_for_attack(cache, args, strategy_name)
        if attack_data is None:
            print(f"\n  [ERROR] {strategy_name:<10}: No cache entry found for this exact config!")
            print(f"          => Missing attack cache for: Method={args['unlearning_methods']}, "
                  f"Dataset={args['dataset_name']}, Model={args['base_model']}, "
                  f"Seed={target_seed}, Ratio={args['unlearn_ratio']}, Strategy={strategy_name}")
            print(f"          => Action: Please run `demo_attack.py` or mg3 script first to generate missing data.")
            continue
            
        attack_f1_after = attack_data.get('f1_after')
        if attack_f1_after is None:
            print(f"  [ERROR] {strategy_name:<10}: Found cache but missing f1_after in attack result!")
            continue
            
        gap = attack_f1_after - baseline_f1_after
        relative_f1_drop = -gap
        
        effect = "effective" if relative_f1_drop > 0 else "ineffective"
        
        print(f"  {strategy_name:<10}: attack_f1={attack_f1_after:.4f}, gap={gap:>7.4f}, relative_drop={relative_f1_drop:>7.4f} ({effect})")
        
        all_results.append({
            "strategy": strategy_name,
            "baseline_f1_after": baseline_f1_after,
            "attack_f1_after": attack_f1_after,
            "gap": gap,
            "relative_f1_drop": relative_f1_drop,
        })
        
    print("\n" + "=" * 80)
    print(f"Relative Evaluation Summary: {args['unlearning_methods']} / {args['dataset_name']} / {args['base_model']} / Seed {args['random_seed']}")
    print("=" * 80)
    header = f"{'Strategy':<12}| {'Attack F1':>10} | {'Base F1':>9} | {'Gap':>8} | {'Rel Drop':>8}"
    print(header)
    print("-" * 80)
    final_results = all_results
    if _repair_mode:
        merged = dict(existing_results_by_strategy)
        for r in all_results:
            merged[r['strategy']] = r
        ordered = []
        seen = set()
        for s in strategies:
            if s in merged:
                ordered.append(merged[s])
                seen.add(s)
        for s in sorted(merged.keys()):
            if s not in seen:
                ordered.append(merged[s])
        final_results = ordered

    for r in final_results:
        print(f"{r['strategy']:<12}| {r['attack_f1_after']:>10.4f} | {r['baseline_f1_after']:>9.4f} | {r['gap']:>8.4f} | {r['relative_f1_drop']:>8.4f}")
    print("=" * 80)
    
    out_dir = Path(f"./results/relative/{args['unlearning_methods']}/{args['dataset_name']}/{args['base_model']}")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"relative_seed{args.get('random_seed')}_{timestamp}.json"
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({
            "config": {
                "dataset_name": args['dataset_name'],
                "base_model": args['base_model'],
                "unlearning_methods": args['unlearning_methods'],
                "unlearn_ratio": args['unlearn_ratio'],
                "random_seed": args.get('random_seed', 2024),
                "baseline_k": _baseline_k,
                "strategies_requested": strategies,
            },
            "results": final_results,
            "timestamp": datetime.now().isoformat(),
            **({
                "repair_meta": {
                    "repair_mode": True,
                    "dry_run": _repair_dry_run,
                    "requested": len(strategies),
                    "completed_before": len(completed_before),
                    "executed_now": len(all_results),
                    "missing_before": len(strategies_to_run),
                }
            } if _repair_mode else {}),
        }, f, indent=2)
        
    print(f"\nResults saved to: {out_path}")


if __name__ == '__main__':
    main()
