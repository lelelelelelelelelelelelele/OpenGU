"""
eval_collateral.py - Evaluate collateral damage and retrain gap metrics.

Reads selected_nodes from cache, re-runs unlearning to get model_unlearned,
trains from scratch excluding selected_nodes to get model_retrained,
then computes retrain gap and collateral damage.

Usage:
    python eval_collateral.py \
        --dataset_name cora --base_model GCN \
        --unlearning_methods GNNDelete \
        --strategies random,degree,pagerank,tracin,im,hybrid \
        --unlearn_ratio 0.05

IMPORTANT: Always pass --unlearn_ratio explicitly to match the cached attack results.
  - Default experiment ratio: 0.05 (used in demo_attack.py runs)
  - parameter_parser() default is 0.1 — cache lookup will fail silently if mismatched
  - When not passed, this script defaults to 0.05 (not parameter_parser's 0.1)
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Extract custom args from sys.argv BEFORE any import that triggers
# config.py (which calls parameter_parser() at import time and rejects
# unknown args).
_strategies_str = 'random,degree,pagerank,tracin,im,hybrid'
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
    elif _arg == '--repair':
        _repair_mode = True
    elif _arg == '--repair_dry_run':
        _repair_mode = True
        _repair_dry_run = True
    else:
        _filtered_argv.append(_arg)
    _i += 1
sys.argv = [sys.argv[0]] + _filtered_argv

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from parameter_parser import parameter_parser


def find_cache_entry(cache, args: dict, strategy_name: str):
    """Find a cache entry by scanning all cache files and matching key fields.

    We scan rather than hash-lookup because the original cache entries may have
    been saved with slightly different type representations (e.g., args from
    AttackManager vs parameter_parser).
    """
    import json as _json
    target = {
        'dataset_name': str(args.get('dataset_name', '')),
        'base_model': str(args.get('base_model', '')),
        'unlearning_methods': str(args.get('unlearning_methods', '')),
        'strategy_name': strategy_name,
    }
    target_ratio = float(args.get('unlearn_ratio', 0.1))
    target_seed = args.get('random_seed', args.get('seed'))
    if target_seed is not None:
        try:
            target_seed = int(target_seed)
        except (TypeError, ValueError):
            target_seed = None

    # Fast path: try hash-based cache lookup first when possible.
    cache_key_fields = getattr(cache, 'CACHE_KEY_FIELDS', None)
    if not isinstance(cache_key_fields, (list, tuple)):
        cache_key_fields = [
            'dataset_name',
            'base_model',
            'unlearning_methods',
            'unlearn_ratio',
            'random_seed',
            'seed',
            'strategy_name',
        ]

    lookup_config = {}
    for key in cache_key_fields:
        if key == 'strategy_name':
            lookup_config[key] = strategy_name
            continue
        value = args.get(key)
        if key == 'random_seed' and value is None:
            value = args.get('seed')
        if key == 'seed' and value is None:
            value = args.get('random_seed')
        if isinstance(value, (str, int, float, bool, type(None))):
            lookup_config[key] = value

    if hasattr(cache, 'get'):
        cached = cache.get(lookup_config)
        if cached is not None:
            return cached

    cache_dir_value = getattr(cache, 'cache_dir', None)
    if not isinstance(cache_dir_value, (str, os.PathLike, Path)):
        return None
    cache_dir = Path(cache_dir_value)
    if not cache_dir.exists():
        return None

    # Determine target k: prefer explicit k from args, otherwise derive from ratio
    target_k = args.get('k')
    if target_k is None:
        # k is typically ratio * num_nodes; not available here, so prefer
        # entries with explicit k over legacy entries without k.
        target_k = None

    best_match = None
    best_k = None  # track k to prefer explicit-k entries over k=MISSING

    for fpath in cache_dir.glob('*.json'):
        try:
            with open(fpath, encoding='utf-8') as f:
                data = _json.load(f)
            c = data.get('config', {})
            cache_seed = c.get('random_seed', c.get('seed'))
            if target_seed is not None:
                # 兼容旧缓存：cache_seed 为 null 时，假设为 2024（早期实验默认 seed）
                if cache_seed is None:
                    cache_seed = 2024
                try:
                    cache_seed = int(cache_seed)
                except (TypeError, ValueError):
                    continue
                if cache_seed != target_seed:
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
                    from attack.attack_result import AttackResult
                    return AttackResult.from_dict(data['result'])

                # No target_k: prefer entries with explicit k over legacy (k=None)
                if best_match is None:
                    best_match = data
                    best_k = cache_k
                elif cache_k is not None and best_k is None:
                    # Prefer explicit k over missing k
                    best_match = data
                    best_k = cache_k
        except (ValueError, KeyError, TypeError, _json.JSONDecodeError):
            continue

    if best_match is not None:
        from attack.attack_result import AttackResult
        return AttackResult.from_dict(best_match['result'])
    return None


def _normalize_strategies(strategies):
    seen = set()
    normalized = []
    for s in strategies:
        s = str(s).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        normalized.append(s)
    return normalized


def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _target_seed(args):
    seed = args.get('random_seed', args.get('seed'))
    try:
        return int(seed)
    except (TypeError, ValueError):
        return None


def _matches_collateral_config(config: dict, args: dict):
    if not isinstance(config, dict):
        return False
    if str(config.get('dataset_name', '')) != str(args.get('dataset_name', '')):
        return False
    if str(config.get('base_model', '')) != str(args.get('base_model', '')):
        return False
    if str(config.get('unlearning_methods', '')) != str(args.get('unlearning_methods', '')):
        return False

    cfg_ratio = _safe_float(config.get('unlearn_ratio'))
    target_ratio = _safe_float(args.get('unlearn_ratio'))
    if cfg_ratio is None or target_ratio is None or abs(cfg_ratio - target_ratio) > 1e-6:
        return False

    # Strict seed match in repair mode: old files without seed are non-exact matches.
    cfg_seed = config.get('random_seed')
    if cfg_seed is None:
        return False
    try:
        cfg_seed = int(cfg_seed)
    except (TypeError, ValueError):
        return False

    tgt_seed = _target_seed(args)
    if tgt_seed is None:
        return False
    return cfg_seed == tgt_seed


def _scan_existing_collateral(args: dict):
    out_dir = Path(f"./results/collateral/{args['unlearning_methods']}/{args['dataset_name']}/{args['base_model']}")
    strategy_map = {}
    matched_files = []
    if not out_dir.exists():
        return strategy_map, matched_files

    files = sorted(
        out_dir.glob("collateral_*.json"),
        key=lambda p: p.stat().st_mtime
    )
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if not _matches_collateral_config(data.get('config', {}), args):
            continue

        matched_files.append(str(path))
        for result in data.get('results', []):
            if not isinstance(result, dict):
                continue
            strategy = str(result.get('strategy', '')).strip()
            if not strategy:
                continue
            strategy_map[strategy] = result
    return strategy_map, matched_files


def main():
    strategies = _normalize_strategies(_strategies_str.split(','))

    # Parse CLI args (inherits all main.py args via parameter_parser)
    args = parameter_parser()

    # parameter_parser() defaults unlearn_ratio=0.1, but experiment caches use 0.05.
    # Override to 0.05 unless the user explicitly passed --unlearn_ratio.
    passed_unlearn_ratio = any(
        a == '--unlearn_ratio' or str(a).startswith('--unlearn_ratio=')
        for a in sys.argv[1:]
    )
    if not passed_unlearn_ratio:
        args['unlearn_ratio'] = 0.05

    # Sync proportion_unlearned_nodes with unlearn_ratio so that GNNDelete's
    # df_size assertion passes (it uses proportion_unlearned_nodes, not unlearn_ratio)
    args['proportion_unlearned_nodes'] = args['unlearn_ratio']

    print(f"Dataset: {args['dataset_name']}, Model: {args['base_model']}, "
          f"Method: {args['unlearning_methods']}")
    print(f"Strategies: {strategies}")
    print("=" * 80)

    existing_results_by_strategy = {}
    matched_collateral_files = []
    strategies_to_run = list(strategies)
    completed_before = []

    if _repair_mode:
        existing_results_by_strategy, matched_collateral_files = _scan_existing_collateral(args)
        completed_before = [s for s in strategies if s in existing_results_by_strategy]
        strategies_to_run = [s for s in strategies if s not in existing_results_by_strategy]

        print(
            f"[REPAIR] requested={len(strategies)} "
            f"completed_before={len(completed_before)} "
            f"missing={len(strategies_to_run)}"
        )
        if matched_collateral_files:
            print(f"[REPAIR] matched_files={len(matched_collateral_files)}")
        if strategies_to_run:
            print(f"[REPAIR] missing_strategies={','.join(strategies_to_run)}")
        else:
            print("[REPAIR] No missing strategies found")
            return
        if _repair_dry_run:
            print("[REPAIR] Dry-run mode enabled. No collateral evaluation executed.")
            return

    # Delay heavy imports until we know we need to run
    import torch
    import numpy as np
    from attack.pipeline_adapter import AttackPipeline
    from attack.result_cache import ResultCache
    from attack.attack_eval import evaluate_retrain_gap, evaluate_collateral_damage

    # Pre-training `model_before` once
    if strategies_to_run:
        from model.model_zoo import model_zoo as mz
        from unlearning_manager import UnlearningManager
        print(f"\n[*] Pre-training 'model_before' once for all strategies...")
        # Initialize pipeline just for original data
        pipeline = AttackPipeline(args)
        pipeline.args["train_only"] = True
        pipeline.args["num_runs"] = 1
        pipeline.model_zoo = mz(pipeline.args, pipeline.data)
        pipeline.model = pipeline.model_zoo.model
        pipeline.manager = UnlearningManager(
            pipeline.args, pipeline.original_data, pipeline.data,
            pipeline.logger, pipeline.model_zoo, pipeline.dataset
        )
        pipeline.method = pipeline.manager.get_method()
        pipeline.method.run_exp()
        model_before = pipeline._get_trained_model()
        pipeline.args["train_only"] = False

    # Initialize pipeline for main loop
    pipeline = AttackPipeline(args)
    cache = ResultCache(cache_dir="./results/cache")

    # Storage for results
    all_results = []

    for strategy_name in strategies_to_run:
        print(f"\n--- Strategy: {strategy_name} ---")

        # 1. Read selected_nodes from cache
        cached = find_cache_entry(cache, args, strategy_name)
        if cached is None:
            print(f"  [SKIP] No cache entry for strategy={strategy_name}")
            continue

        selected_nodes = cached.selected_nodes
        if isinstance(selected_nodes, list):
            selected_nodes = torch.tensor(selected_nodes)
        print(f"  Loaded {len(selected_nodes)} selected nodes from cache")

        # 2. Inject nodes and run unlearning to get model_unlearned
        pipeline._inject_unlearn_nodes(selected_nodes, run_id=0)

        # Reset method to pick up the new unlearning nodes
        pipeline.args["train_only"] = False
        pipeline.args["num_runs"] = 1
        from model.model_zoo import model_zoo as mz
        from unlearning_manager import UnlearningManager

        pipeline.model_zoo = mz(pipeline.args, pipeline.data)
        pipeline.model = pipeline.model_zoo.model
        pipeline.manager = UnlearningManager(
            pipeline.args, pipeline.original_data, pipeline.data,
            pipeline.logger, pipeline.model_zoo, pipeline.dataset
        )
        pipeline.method = pipeline.manager.get_method()
        pipeline.method.run_exp()

        model_unlearned = pipeline._get_trained_model()

        # We use the pre-trained `model_before` here instead of re-training
        # (It is passed to evaluate_retrain_gap below)

        # 3. Retrain-from-scratch excluding selected_nodes
        model_retrained, f1_retrained = pipeline.run_retrain(selected_nodes)

        # 4. Build masks
        test_mask = pipeline.data.test_mask
        retain_mask = pipeline.data.train_mask.clone()
        retain_mask[selected_nodes.long()] = False

        # 5. Compute metrics — ensure all models and data on same device
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        model_before = model_before.to(device)
        model_unlearned = model_unlearned.to(device)
        model_retrained = model_retrained.to(device)
        data = pipeline.data.to(device)

        gap_metrics = evaluate_retrain_gap(
            model_before, model_unlearned, model_retrained, data, test_mask
        )
        collateral_metrics = evaluate_collateral_damage(
            model_unlearned, model_retrained, data, retain_mask
        )

        result = {
            "strategy": strategy_name,
            **gap_metrics,
            **collateral_metrics,
        }
        all_results.append(result)

        print(f"  Gap: {gap_metrics['gap']:.4f} ({gap_metrics['gap_pct']:.2f}%)")
        print(f"  MeanShift: {collateral_metrics['mean_pred_shift']:.4f}, "
              f"MaxShift: {collateral_metrics['max_pred_shift']:.4f}, "
              f"Flipped: {collateral_metrics['fraction_flipped']:.4f}")

    # 6. Print summary table
    print("\n" + "=" * 90)
    print(f"Collateral Damage Summary: {args['unlearning_methods']} / "
          f"{args['dataset_name']} / {args['base_model']}")
    print("=" * 90)
    header = f"{'Strategy':<12}| {'Gap':>8} | {'Gap%':>7} | {'MeanShift':>10} | {'MaxShift':>9} | {'Flipped%':>9}"
    print(header)
    print("-" * 90)
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
        print(f"{r['strategy']:<12}| {r['gap']:>8.4f} | {r['gap_pct']:>6.2f}% | "
              f"{r['mean_pred_shift']:>10.4f} | {r['max_pred_shift']:>9.4f} | "
              f"{r['fraction_flipped']*100:>8.2f}%")
    print("=" * 90)

    # 7. Save results to JSON
    out_dir = Path(f"./results/collateral/{args['unlearning_methods']}/{args['dataset_name']}/{args['base_model']}")
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"collateral_{timestamp}.json"
    with open(out_path, 'w') as f:
        json.dump({
            "config": {
                "dataset_name": args['dataset_name'],
                "base_model": args['base_model'],
                "unlearning_methods": args['unlearning_methods'],
                "unlearn_ratio": args['unlearn_ratio'],
                "random_seed": args.get('random_seed', args.get('seed')),
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

    # 8. Append to auto_report.md
    try:
        from scripts.evaluation.reporting.writer import append_collateral_entry
        report_results = final_results if _repair_mode else all_results
        status = "OK" if report_results else "WARN"
        error_type = None
        error_msg = None
        next_step = None
        if not report_results:
            error_type = "NO_CACHE_HIT"
            error_msg = "No matching cache entries found for the requested strategies/ratio/seed."
            next_step = "先运行 demo_attack.py 生成对应 seed/ratio 的缓存，再重跑 eval_collateral.py。"
        append_collateral_entry(
            dataset=args['dataset_name'],
            model=args['base_model'],
            method=args['unlearning_methods'],
            ratio=str(args['unlearn_ratio']),
            results=report_results,
            log_file=str(out_path),
            status=status,
            error_type=error_type,
            error_msg=error_msg,
            next_step=next_step,
        )
        print("Report entry appended to auto_report.md")
    except Exception as e:
        print(f"[WARN] Could not append to auto_report.md: {e}")


if __name__ == '__main__':
    main()
