"""
Demo script for adversarial attacks on GNN unlearning.

This script demonstrates the attack framework by comparing different
node selection strategies for forced unlearning attacks.

Example usage:
    # Compare Random vs TracIn on Cora with SGC+SGU
    python demo_attack.py --dataset_name cora --base_model SGC --unlearning_methods SGU

    # Compare all 4 strategies with custom ratio
    python demo_attack.py --strategies random,degree,pagerank,tracin --unlearn_ratio 0.1

    # Run with caching disabled
    python demo_attack.py --no_cache
"""
import os
import sys
import argparse

# IMPORTANT: Parse and clean sys.argv BEFORE importing any module that might
# trigger config.py (which calls parameter_parser() at import time)
def _add_cli_arg(argv, name, value):
    argv.extend([name, str(value)])


def _extract_demo_args():
    """Extract demo-specific arguments from sys.argv before importing other modules."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--strategies", type=str, default="random,degree,pagerank,tracin,im,hybrid")
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--no_cache", action="store_true")
    parser.add_argument("--save_path", type=str, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--random_seed", type=int, default=None)
    # Also include common args that parameter_parser needs
    parser.add_argument("--dataset_name", type=str, default="cora")
    parser.add_argument("--base_model", type=str, default="SGC")
    parser.add_argument("--unlearning_methods", type=str, default="SGU")
    parser.add_argument("--unlearn_ratio", type=float, default=0.05)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--batch_size", type=int, default=64)

    demo_args, remaining_args = parser.parse_known_args()
    if demo_args.seed is None:
        demo_args.seed = demo_args.random_seed if demo_args.random_seed is not None else 2024

    # Reconstruct sys.argv without demo-only args, while preserving the shared
    # args that config.py/parameter_parser.py must see during import-time parse.
    shared_args = list(remaining_args)
    for name, value in (
        ("--cuda", demo_args.cuda),
        ("--dataset_name", demo_args.dataset_name),
        ("--base_model", demo_args.base_model),
        ("--unlearning_methods", demo_args.unlearning_methods),
        ("--unlearn_ratio", demo_args.unlearn_ratio),
        ("--proportion_unlearned_nodes", demo_args.unlearn_ratio),
        ("--num_epochs", demo_args.num_epochs),
        ("--batch_size", demo_args.batch_size),
        ("--random_seed", demo_args.seed),
    ):
        _add_cli_arg(shared_args, name, value)
    sys.argv = [sys.argv[0]] + shared_args

    return demo_args

# Extract demo args BEFORE importing other modules
_demo_args = _extract_demo_args()

import torch

# Ensure the current directory is in the path
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser
from attack import AttackManager
from attack.attack_result import ComparisonResult


def seed_everything(seed_value):
    """Set random seeds for reproducibility."""
    import random
    import numpy as np

    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    os.environ['PYTHONHASHSEED'] = str(seed_value)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _candidate_node_count(data):
    train_mask = getattr(data, "train_mask", None)
    if train_mask is not None:
        if train_mask.dim() > 1:
            train_mask = train_mask.squeeze(-1)
        return int(train_mask.nonzero(as_tuple=False).view(-1).numel())

    train_indices = getattr(data, "train_indices", None)
    if train_indices is not None:
        return int(len(train_indices))

    return int(data.num_nodes)


def main():
    """Main demo function."""
    # Demo args were already extracted at module import time
    # to avoid conflicts with config.py's automatic parameter_parser() call
    demo_args = _demo_args

    # Parse arguments using parameter_parser
    print("=" * 70)
    print("Attack Demo - Adversarial Attacks on GNN Unlearning")
    print("=" * 70)
    print("\nParsing arguments...")

    args = parameter_parser()

    # Keep the runtime args aligned with the sanitized argv used by config.py.
    args['cuda'] = demo_args.cuda
    args['dataset_name'] = demo_args.dataset_name
    args['base_model'] = demo_args.base_model
    args['unlearning_methods'] = demo_args.unlearning_methods
    args['unlearn_ratio'] = demo_args.unlearn_ratio
    args['proportion_unlearned_nodes'] = demo_args.unlearn_ratio
    args['num_epochs'] = demo_args.num_epochs
    args['batch_size'] = demo_args.batch_size
    args['random_seed'] = demo_args.seed
    args['seed'] = demo_args.seed

    # Set random seed
    seed_everything(demo_args.seed)

    # Set CUDA device
    if args.get('cuda', 0) >= 0 and torch.cuda.is_available():
        torch.cuda.set_device(args['cuda'])
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args['cuda'])
        print(f"Using CUDA device: {args['cuda']}")
    else:
        print("Using CPU")

    # Parse strategies
    strategies = [s.strip() for s in demo_args.strategies.split(',')]
    print(f"\nStrategies to compare: {strategies}")

    # Create AttackManager
    print("\n" + "-" * 70)
    print("Initializing AttackManager...")
    print("-" * 70)

    try:
        manager = AttackManager(
            args,
            use_cache=not demo_args.no_cache,
        )
    except Exception as e:
        print(f"\nError initializing AttackManager: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(f"\nDataset: {args['dataset_name']}")
    print(f"Model: {args['base_model']}")
    print(f"Unlearning Method: {args['unlearning_methods']}")
    print(f"Number of nodes: {manager.data.num_nodes}")

    # Determine k
    if demo_args.k is not None:
        k = demo_args.k
    else:
        k = int(_candidate_node_count(manager.data) * args.get('unlearn_ratio', 0.05))

    print(f"Nodes to unlearn (k): {k} ({args.get('unlearn_ratio', 0.05)*100:.1f}%)")

    # Validate strategies
    available_strategies = manager.list_strategies()
    invalid_strategies = [s for s in strategies if s not in available_strategies]

    if invalid_strategies:
        print(f"\nWarning: Invalid strategies: {invalid_strategies}")
        print(f"Available strategies: {available_strategies}")
        strategies = [s for s in strategies if s in available_strategies]

    if not strategies:
        print("No valid strategies to run. Exiting.")
        sys.exit(1)

    # Run comparison
    print("\n" + "=" * 70)
    print("Running Strategy Comparison")
    print("=" * 70)

    try:
        comparison = manager.compare_strategies(
            strategy_names=strategies,
            k=k,
            save_path=demo_args.save_path,
        )
    except Exception as e:
        print(f"\nError running comparison: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Print final summary
    print("\n" + "=" * 70)
    print("Demo Complete")
    print("=" * 70)

    if demo_args.save_path:
        print(f"Results saved to: {demo_args.save_path}")

    # Detect per-strategy failures and surface them via non-zero rc.
    # Without this, run.py's `failed_attack` gate is never tripped: a
    # strategy whose unlearning crashed inside pipeline_adapter's except
    # block returns a placeholder AttackResult with failed=True, which
    # leaks into attack.json as a NA row but lets demo_attack exit 0.
    # That, combined with the post-2026-05-06 cache-write guard preventing
    # eval_collateral from re-discovering the same crash, would let cells
    # falsely complete. Surface the failure here so run.py reports
    # failed_attack and skips _meta.json.
    failed_runs = [r for r in comparison.results if getattr(r, "failed", False)]
    if failed_runs:
        print("\n[Demo] Strategy failures detected:")
        for r in failed_runs:
            print(f"  - {r.strategy_name}: {r.failure_reason or 'unknown'}")
        sys.exit(1)

    # Write to auto_report.md
    try:
        from scripts.evaluation.reporting.writer import append_attack_result
        report_path = append_attack_result(
            method=args['unlearning_methods'],
            dataset=args['dataset_name'],
            model=args['base_model'],
            strategies=strategies,
            unlearn_ratio=args.get('unlearn_ratio', 0.05),
            k=k,
            seed=demo_args.seed,
            results=comparison.results,
        )
        print(f"[Report] Results appended to {report_path}")
    except Exception as e:
        print(f"[Report] Warning: Could not write to auto_report.md: {e}")

    return comparison


if __name__ == '__main__':
    main()
