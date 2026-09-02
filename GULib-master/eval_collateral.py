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
# (above default already uses post-2026-05-04 names, no v4 suffix)
_repair_mode = False
_repair_dry_run = False
_save_predictions = False
_output_dir = None  # if set: write collateral.json + predictions.npz here, no timestamp suffix
_cache_v2_store_root = None
_selection_artifact_id = None
_selection_k = None
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
    elif _arg == '--save_predictions':
        # Dump logits_{before,unlearned,retrained} per strategy as .npz next to JSON.
        # Lets future forward-only metrics be added offline without re-running GU+retrain.
        _save_predictions = True
    elif _arg == '--output_dir':
        # New runner mode: write collateral.json + predictions.npz directly under this dir
        # with deterministic names (no timestamp suffix). Old default path layout is kept
        # when --output_dir is not set, so legacy bash scripts are unaffected.
        if _i + 1 < len(_raw_args):
            _output_dir = _raw_args[_i + 1]
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--output_dir='):
        _output_dir = _arg.split('=', 1)[1]
    elif _arg == '--cache_v2_store_root':
        if _i + 1 < len(_raw_args):
            _cache_v2_store_root = _raw_args[_i + 1]
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--cache_v2_store_root='):
        _cache_v2_store_root = _arg.split('=', 1)[1]
    elif _arg == '--selection_artifact_id':
        if _i + 1 < len(_raw_args):
            _selection_artifact_id = _raw_args[_i + 1]
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--selection_artifact_id='):
        _selection_artifact_id = _arg.split('=', 1)[1]
    elif _arg == '--selection_k':
        if _i + 1 < len(_raw_args):
            _selection_k = int(_raw_args[_i + 1])
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--selection_k='):
        _selection_k = int(_arg.split('=', 1)[1])
    else:
        _filtered_argv.append(_arg)
    _i += 1
sys.argv = [sys.argv[0]] + _filtered_argv

if _selection_artifact_id and not _cache_v2_store_root:
    raise SystemExit(
        "--cache_v2_store_root and --selection_artifact_id must be provided together"
    )

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from parameter_parser import parameter_parser


def _seed_everything(seed_value):
    """Set random seeds for collateral evaluation and retrain reproducibility."""
    import random
    import numpy as np
    import torch

    seed_value = int(seed_value)
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    os.environ['PYTHONHASHSEED'] = str(seed_value)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def load_generic_selection(manager, strategy_name, k):
    """Read the same exact V2 Selection Recipe used by the generic attack."""
    from experiments.selection_inputs import make_dataset_selection_inputs
    inputs = make_dataset_selection_inputs(manager.data, dataset_name=manager.args["dataset_name"])
    request = manager._selection_request(strategy_name, k, inputs)
    selection = manager.selection_cache.get(request)
    if selection is None:
        return None, {"outcome": "miss", "lookup_policy": "cache_v2_exact_recipe",
                      "authoritative": True, "recipe_hash": request.recipe.recipe_hash}
    return selection, {"outcome": "hit", "artifact_id": selection.artifact_id,
        "artifact_type": "selection", "recipe_hash": selection.recipe_hash,
        "content_hash": selection.content_hash, "source_file": selection.source,
        "lookup_policy": "cache_v2_exact_recipe", "authoritative": True,
        "hit_source": "cache_v2:" + selection.artifact_id, "write_outcome": "reused"}


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


def _candidate_nodes(data):
    import numpy as np

    train_mask = getattr(data, 'train_mask', None)
    if train_mask is not None:
        nodes = train_mask.nonzero(as_tuple=False).squeeze(-1).cpu().numpy()
        return nodes.astype(np.int64, copy=False)
    return np.arange(int(data.num_nodes), dtype=np.int64)


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
    v2_selection = bool(_selection_artifact_id)
    if v2_selection:
        if _repair_mode:
            raise SystemExit("Cache V2 Selection mode does not support Legacy repair mode")
        if len(strategies) != 1:
            raise SystemExit(
                "Cache V2 Selection mode requires exactly one strategy"
            )
        import re
        if re.fullmatch(r"[a-z0-9][a-z0-9_.-]{0,80}", strategies[0]) is None:
            raise SystemExit("Cache V2 Selection strategy label is unsafe")
        if _selection_k is not None and _selection_k <= 0:
            raise SystemExit("--selection_k must be positive")

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
    args['cache_v2_store_root'] = _cache_v2_store_root
    args['seed'] = args.get('random_seed', 2024)
    seed_value = args.get('random_seed', args.get('seed', 2024))
    _seed_everything(seed_value)

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
    from attack.attack_manager import AttackManager
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
    selection_manager = None if v2_selection else AttackManager(args, pipeline)

    # Storage for results
    all_results = []
    cache_provenance = {}
    # Per-strategy prediction snapshots (only populated when --save_predictions).
    # Each entry: dict with keys logits_{before,unlearned,retrained}, retain_mask,
    # selected_nodes — already as numpy arrays.
    predictions_dump = []

    for strategy_name in strategies_to_run:
        print(f"\n--- Strategy: {strategy_name} ---")

        # 1. Read selected_nodes from cache
        if v2_selection:
            from cache_v2.runtime import load_selection_artifact

            target_k = (
                int(_selection_k)
                if _selection_k is not None
                else max(
                    1,
                    int(len(_candidate_nodes(pipeline.data)) * float(args['unlearn_ratio'])),
                )
            )
            loaded = load_selection_artifact(
                str(Path(_cache_v2_store_root).resolve()),
                _selection_artifact_id,
                num_nodes=int(pipeline.data.num_nodes),
                candidate_nodes=_candidate_nodes(pipeline.data),
                expected_selector=strategy_name,
                expected_k=target_k,
            )
            selected_nodes = torch.tensor(loaded.selected_nodes, dtype=torch.long)
            cache_info = dict(loaded.provenance(str(Path(_cache_v2_store_root).resolve())))
            cached = None
        else:
            target_k = _selection_k if _selection_k is not None else max(1, int(len(_candidate_nodes(pipeline.data)) * args['unlearn_ratio']))
            cached, cache_info = load_generic_selection(selection_manager, strategy_name, target_k)
        cache_provenance[strategy_name] = cache_info
        if not v2_selection and cached is None:
            if _output_dir is not None:
                # Runner mode (called by experiments/run.py): demo_attack just ran
                # for this exact (method, strategy, seed). A cache miss means
                # demo_attack's unlearning failed AND the cache-write guard
                # (attack_manager.py post-2026-05-06) blocked the dirty entry.
                # Abort with non-zero rc so run.py reports failed_collateral
                # and skips _meta.json — preventing the cell from being
                # falsely marked complete.
                print(
                    f"  [ERROR] No cache entry for strategy={strategy_name} in runner mode. "
                    f"demo_attack likely failed; aborting to avoid false-complete cell."
                )
                sys.exit(1)
            print(f"  [SKIP] No cache entry for strategy={strategy_name}")
            continue

        if not v2_selection:
            selected_nodes = cached.selected_nodes
            if isinstance(selected_nodes, list):
                selected_nodes = torch.tensor(selected_nodes)
        print(
            f"  Loaded {len(selected_nodes)} selected nodes from "
            "Cache V2 Artifact"
        )

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
            model_unlearned, model_retrained, data, retain_mask,
            unlearn_nodes=selected_nodes,
        )

        result = {
            "strategy": strategy_name,
            **gap_metrics,
            **collateral_metrics,
        }
        all_results.append(result)

        if _save_predictions:
            import numpy as _np

            def _logits_np(_model, _data):
                _model.eval()
                with torch.no_grad():
                    fwd = _model.forward
                    if hasattr(fwd, '__code__') and 'edge_index' in fwd.__code__.co_varnames:
                        out = _model(_data.x, _data.edge_index)
                    else:
                        out = _model(_data.x)
                return out.detach().cpu().numpy()

            predictions_dump.append({
                "strategy": strategy_name,
                "logits_before": _logits_np(model_before, data),
                "logits_unlearned": _logits_np(model_unlearned, data),
                "logits_retrained": _logits_np(model_retrained, data),
                "retain_mask": retain_mask.detach().cpu().numpy().astype(bool),
                "selected_nodes": (
                    selected_nodes.detach().cpu().numpy()
                    if isinstance(selected_nodes, torch.Tensor)
                    else _np.asarray(selected_nodes)
                ),
            })

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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if _output_dir is not None:
        # Runner mode: deterministic, timestamp-free filenames in caller-controlled dir.
        out_dir = Path(_output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "collateral.json"
    else:
        out_dir = Path(f"./results/collateral/{args['unlearning_methods']}/{args['dataset_name']}/{args['base_model']}")
        out_dir.mkdir(parents=True, exist_ok=True)
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
                "selection_artifact_id": _selection_artifact_id,
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

    # 7b. Save per-strategy predictions (forward-only metric cache, optional).
    if _save_predictions and predictions_dump:
        import numpy as _np
        # One bundled .npz keyed by `{strategy}__{field}` → keeps per-cell file count low.
        bundle = {}
        labels = data.y.detach().cpu().numpy()
        try:
            train_mask_np = data.train_mask.detach().cpu().numpy().astype(bool)
        except AttributeError:
            train_mask_np = _np.zeros(int(data.num_nodes), dtype=bool)
        try:
            test_mask_np = data.test_mask.detach().cpu().numpy().astype(bool)
        except AttributeError:
            test_mask_np = _np.zeros(int(data.num_nodes), dtype=bool)
        bundle["_meta__y"] = labels
        bundle["_meta__train_mask"] = train_mask_np
        bundle["_meta__test_mask"] = test_mask_np
        bundle["_meta__num_nodes"] = _np.int64(int(data.num_nodes))
        for entry in predictions_dump:
            s = entry["strategy"]
            bundle[f"{s}__logits_before"] = entry["logits_before"].astype(_np.float32)
            bundle[f"{s}__logits_unlearned"] = entry["logits_unlearned"].astype(_np.float32)
            bundle[f"{s}__logits_retrained"] = entry["logits_retrained"].astype(_np.float32)
            bundle[f"{s}__retain_mask"] = entry["retain_mask"]
            bundle[f"{s}__selected_nodes"] = entry["selected_nodes"].astype(_np.int64)
        pred_name = "predictions.npz" if _output_dir is not None else f"predictions_{timestamp}.npz"
        pred_path = out_dir / pred_name
        _np.savez_compressed(pred_path, **bundle)
        size_mb = pred_path.stat().st_size / (1024 * 1024)
        print(f"Predictions cache: {pred_path}  ({size_mb:.1f} MB, {len(predictions_dump)} strategies)")

    # 8. Record structured V3 events. The historical Markdown journal remains
    # append-only but is no longer duplicated by this high-volume producer.
    try:
        from scripts.evaluation.reporting.writer import record_collateral_results
        # In repair mode, only newly executed strategies are new audit facts;
        # merged historical rows stay in collateral.json but are not replayed.
        report_results = all_results
        error_type = None
        error_msg = None
        if not report_results:
            error_type = "NO_CACHE_HIT"
            error_msg = "No matching cache entries found for the requested strategies/ratio/seed."
        report_path = record_collateral_results(
            dataset=args['dataset_name'],
            model=args['base_model'],
            method=args['unlearning_methods'],
            ratio=args['unlearn_ratio'],
            seed=_target_seed(args),
            results=report_results,
            output_path=str(out_path),
            cache_provenance=cache_provenance,
            requested_strategies=strategies_to_run,
            error_type=error_type,
            error_msg=error_msg,
        )
        print(f"[AutoReport V3] Events recorded in {report_path}")
    except Exception as e:
        print(f"[WARN] Could not write AutoReport V3 events: {e}")


if __name__ == '__main__':
    main()
