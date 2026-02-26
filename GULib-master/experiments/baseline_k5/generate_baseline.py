"""
generate_baseline.py - Pre-generate K=5 random baseline metrics for unlearning methods.

This script should be run BEFORE `eval_relative.py`. It runs a bare-bones 
evaluation using the `random` strategy for a tiny number of nodes (default K=5)
to extract the inherent F1 shift protecting the unlearning method.

Usage:
    python experiments/baseline_k5/generate_baseline.py \
        --dataset_name cora \
        --base_model GCN \
        --unlearning_methods GraphEraser \
        --random_seed 2024 \
        --baseline_k 5
"""
import os
import sys
import json
import numpy as np
import torch
import random
from pathlib import Path
from datetime import datetime

# Extract custom args BEFORE parameter_parser (which rejects unknown args)
_baseline_k = 5
_raw_args = list(sys.argv[1:])
_filtered_argv = []
_i = 0
while _i < len(_raw_args):
    _arg = _raw_args[_i]
    if _arg == '--baseline_k':
        if _i + 1 < len(_raw_args):
            _baseline_k = int(_raw_args[_i + 1])
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--baseline_k='):
        _baseline_k = int(_arg.split('=', 1)[1])
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

def generate_baseline(args: dict, k: int):
    dataset = args.get('dataset_name', 'cora')
    model = args.get('base_model', 'GCN')
    method = args.get('unlearning_methods', 'GraphEraser')
    seed = int(args.get('random_seed', 2024))
    
    # Target output path for eval_relative.py to automatically discover
    cache_dir = Path(f"./results/baseline/k5_random/{method}/{dataset}/{model}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"baseline_seed{seed}_k{k}.json"
    
    print(f"\n==================================================")
    print(f"[Generate Baseline] Method: {method} | Dataset: {dataset} | Model: {model}")
    print(f"                    Seed: {seed} | K: {k}")
    print(f"==================================================")
    
    if cache_file.exists():
        print(f"[INFO] Cache already exists at:")
        print(f"       {cache_file}")
        print(f"       Skipping generation. (Delete file manually if you want to re-run)")
        return
        
    print(f"[*] Initializing pipeline...")
    
    # 1. Lock seeds
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        
    # 2. Setup
    pipeline = AttackPipeline(args)
    strategy = RandomStrategy(args)

    # CRITICAL: Sync proportion_unlearned_nodes with actual k / num_nodes.
    # GNNDelete's delete_node() computes df_size = int(num_nodes * proportion_unlearned_nodes)
    # and asserts df_mask_node.sum() == df_size.  If proportion_unlearned_nodes stays at the
    # parameter_parser default (0.1), the assertion fails (5 != 270), the exception is caught
    # silently by pipeline_adapter, and a garbage f1_after is returned.
    # Also sync unlearn_ratio so _inject_unlearn_nodes writes the correct file path.
    num_nodes = pipeline.data.num_nodes
    ratio_for_k = k / num_nodes
    args['proportion_unlearned_nodes'] = ratio_for_k
    args['unlearn_ratio'] = ratio_for_k
    print(f"[*] Synced proportion_unlearned_nodes = {ratio_for_k:.6f} (k={k}, num_nodes={num_nodes})")
    
    # 3. Execution
    print(f"[*] Executing random unlearning to extract inherent F1 metric...")
    result_dict = pipeline.run_with_strategy(strategy, k)
    
    # 4. Collection
    f1_after = result_dict.get("f1_after")
    f1_before = result_dict.get("f1_before")
    f1_drop = result_dict.get("f1_drop")
    if f1_drop is None and f1_before is not None and f1_after is not None:
        f1_drop = f1_before - f1_after
    
    data = {
        "f1_after": f1_after,
        "f1_before": f1_before,
        "f1_drop": f1_drop,
        "config": {
            "dataset_name": dataset,
            "base_model": model,
            "unlearning_methods": method,
            "seed": seed,
            "k": k,
            "strategy": "random",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # 5. Sanity check — catch garbage results from silently swallowed exceptions
    if f1_after is not None and f1_after < 0.3:
        print(f"\n[CRITICAL WARNING] f1_after = {f1_after:.4f} is suspiciously low!")
        print(f"  This may indicate GNNDelete's df_size assertion failed silently.")
        print(f"  proportion_unlearned_nodes = {args.get('proportion_unlearned_nodes')}")
        print(f"  k = {k}, expected df_size = {int(pipeline.data.num_nodes * args.get('proportion_unlearned_nodes', 0.1))}")
        print(f"  NOT saving this result. Please investigate before re-running.")
        return

    # 6. Saving
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"[*] Completed! F1 After: {f1_after:.4f}")
    print(f"[*] Baseline saved to: {cache_file}")


def main():
    args = parameter_parser()
    
    # We enforce ratio=0 internally during generation of the base model 
    # to avoid conflict, but since AttackPipeline only triggers the 'k'
    # we pass to 'run_with_strategy(strategy, k)', standard args are fine.
    
    generate_baseline(args, _baseline_k)


if __name__ == '__main__':
    main()
