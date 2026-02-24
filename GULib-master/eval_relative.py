"""
eval_relative.py - Compute relative F1 metrics for attack evaluation.

Compares attack strategies against baseline (random) to isolate
the true attack effect from the unlearning method's inherent behavior.

Usage:
    python eval_relative.py \
        --methods GraphEraser,GUIDE,GNNDelete \
        --datasets cora \
        --baseline_dir results/experiments/mg0_completion/phase_a

Cache behavior:
    - Checks results/relative/ for existing computed results
    - Skips computation if cache hit (use --force to recalculate)
    - Saves computed results to cache
"""
import os
import sys
import json
import glob
import hashlib
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class RelativeMetricsCache:
    """Cache for computed relative metrics."""

    CACHE_KEY_FIELDS = ['methods', 'datasets', 'strategies', 'k', 'ratio', 'baseline_dir']

    def __init__(self, cache_dir: str = "./results/relative", max_age_days: int = 30):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_days = max_age_days

    def _generate_cache_key(self, args: argparse.Namespace) -> str:
        """Generate cache key from args."""
        key_parts = []
        for field in self.CACHE_KEY_FIELDS:
            value = getattr(args, field, None)
            if value is not None:
                if isinstance(value, list):
                    value = ','.join(map(str, value))
                key_parts.append(f"{field}={value}")
        key_string = "_".join(key_parts)
        hash_obj = hashlib.md5(key_string.encode())
        return hash_obj.hexdigest()[:16]

    def _get_cache_path(self, cache_key: str) -> Path:
        return self.cache_dir / f"relative_{cache_key}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache entry is valid."""
        if not cache_path.exists():
            return False
        if self.max_age_days <= 0:
            return True

        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age = datetime.now() - mtime
        return age < timedelta(days=self.max_age_days)

    def get(self, args: argparse.Namespace) -> Optional[Dict[str, Any]]:
        """Get cached results if available."""
        cache_key = self._generate_cache_key(args)
        cache_path = self._get_cache_path(cache_key)

        if not self._is_cache_valid(cache_path):
            return None

        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            print(f"[Cache] Hit: {cache_path.name}")
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Cache] Error reading: {e}")
            return None

    def save(self, args: argparse.Namespace, results: List[Dict[str, Any]]):
        """Save computed results to cache."""
        cache_key = self._generate_cache_key(args)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            'cache_key': cache_key,
            'cached_at': datetime.now().isoformat(),
            'config': {k: getattr(args, k, None) for k in self.CACHE_KEY_FIELDS},
            'results': results
        }

        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)

        print(f"[Cache] Saved: {cache_path}")


def find_summary_files(results_dir: str, method: str, dataset: str,
                       ratio: Optional[float] = None) -> List[Path]:
    """
    Find _summary.json files in results directory.

    Searches in directories like:
    - results/experiments/mg0_completion/phase_a/20260221_184153_seed2024/_summary.json
    - results/experiments/mg0_completion/phase_a/*/_summary.json

    Returns all summary files - filtering by method/dataset happens during parsing.
    """
    results_dir = Path(results_dir)
    if not results_dir.exists():
        return []

    # Find all _summary.json files recursively
    summary_files = list(results_dir.rglob("_summary.json"))

    return summary_files


def find_result_files(results_dir: str, method: str, dataset: str,
                     strategy: Optional[str] = None, k: Optional[int] = None) -> List[Path]:
    """
    Find individual result JSON files (not _summary.json).

    For k=5 experiments, files are saved as:
    - results/baseline/k5_random/GraphEraser/cora/run_20260225_143022.json

    Args:
        results_dir: Base results directory
        method: Unlearning method name
        dataset: Dataset name
        strategy: Attack strategy name (optional)
        k: Number of nodes (optional, e.g., 5)

    Returns:
        List of result JSON file paths
    """
    results_dir = Path(results_dir)
    if not results_dir.exists():
        return []

    # Search for JSON files matching method and dataset
    # Pattern: {method}_{dataset}_*.json or subdirectories
    files = list(results_dir.rglob(f"{method}_{dataset}_*.json"))

    # Exclude _summary.json
    files = [f for f in files if '_summary' not in f.name]

    # Filter by strategy if specified
    if strategy:
        files = [f for f in files if strategy.lower() in f.name.lower()]

    # Filter by k if specified (look for _k5_ or _k5.json in path or filename)
    if k is not None:
        files = [f for f in files if f'_k{k}_' in f.name or f'_{k}_' in f.name
                 or f'/k{k}/' in str(f) or f'\\k{k}\\' in str(f)]

    return sorted(files)


def extract_f1_from_result_file(file_path: Path) -> Optional[Dict[str, float]]:
    """
    Extract f1_before, f1_after, f1_drop from a single result JSON file.

    Handles two formats:
    1. AttackResult format (from demo_attack.py): has 'strategy_name', 'f1_before', etc.
    2. Simple format: has 'f1_before', 'f1_after', etc.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Handle AttackResult format
        if 'strategy_name' in data:
            return {
                'strategy': data.get('strategy_name'),
                'f1_before': data.get('f1_before'),
                'f1_after': data.get('f1_after'),
                'f1_drop': data.get('f1_drop'),
            }

        # Handle simple format
        return {
            'strategy': data.get('strategy_name', 'unknown'),
            'f1_before': data.get('f1_before'),
            'f1_after': data.get('f1_after'),
            'f1_drop': data.get('f1_drop'),
        }

    except Exception as e:
        print(f"Warning: Failed to parse {file_path.name}: {e}")
        return None


def load_k5_results(results_dir: str, method: str, dataset: str,
                    strategy: Optional[str] = None, k: Optional[int] = None) -> Dict[str, List[float]]:
    """
    Load f1_after values from individual result files (for k=5 experiments).

    Returns:
        Dict[str, List[float]] - strategy -> [f1_after values]
    """
    files = find_result_files(results_dir, method, dataset, strategy, k)

    strategy_f1 = {
        'random': {'f1_after': [], 'f1_before': [], 'f1_drop': []},
    }

    for f in files:
        metrics = extract_f1_from_result_file(f)
        if metrics and metrics.get('f1_after') is not None:
            strat = metrics.get('strategy', 'unknown')
            if strat not in strategy_f1:
                strategy_f1[strat] = {'f1_after': [], 'f1_before': [], 'f1_drop': []}

            strategy_f1[strat]['f1_after'].append(metrics['f1_after'])
            strategy_f1[strat]['f1_before'].append(metrics.get('f1_before'))
            strategy_f1[strat]['f1_drop'].append(metrics.get('f1_drop'))

    return strategy_f1


def extract_strategy_results(summary_file: Path, method: str, ratio: float) -> Dict[str, Dict]:
    """
    Extract f1_after for each strategy from _summary.json.

    Returns:
        Dict[str, Dict] - strategy_name -> {f1_before, f1_after, f1_drop}
    """
    try:
        with open(summary_file, 'r') as f:
            data = json.load(f)

        results = {}

        # Navigate to the method-specific results
        # Structure: results -> {method}_{dataset}_{model}_r{ratio} -> results (dict)
        # where keys are strategy names like 'im_v4', 'random', etc.
        for key, value in data.get('results', {}).items():
            if method.lower() in key.lower():
                entries = value.get('results', {})
                if isinstance(entries, dict):
                    for strategy, entry in entries.items():
                        if strategy and strategy != 'comparison':
                            results[strategy] = {
                                'f1_before': entry.get('f1_before'),
                                'f1_after': entry.get('f1_after'),
                                'f1_drop': entry.get('f1_drop'),
                            }

        return results

    except Exception as e:
        print(f"Warning: Failed to parse {summary_file.name}: {e}")
        return {}


def load_strategy_f1_summary(results_dir: str, method: str, dataset: str,
                             ratio: float) -> Dict[str, List[float]]:
    """
    Load f1_after values for all strategies from summary files.

    Returns:
        Dict[str, List[float]] - strategy -> [f1_after values]
    """
    summary_files = find_summary_files(results_dir, method, dataset, ratio)

    # Aggregate f1_after by strategy
    strategy_f1 = {}

    for sf in summary_files:
        strategy_results = extract_strategy_results(sf, method, ratio)

        for strategy, metrics in strategy_results.items():
            if strategy not in strategy_f1:
                strategy_f1[strategy] = {
                    'f1_before': [],
                    'f1_after': [],
                    'f1_drop': []
                }

            if metrics.get('f1_after') is not None:
                strategy_f1[strategy]['f1_after'].append(metrics['f1_after'])
                strategy_f1[strategy]['f1_before'].append(metrics.get('f1_before'))
                strategy_f1[strategy]['f1_drop'].append(metrics.get('f1_drop'))

    return strategy_f1


def compute_relative_metrics(baseline_f1_list: List[float],
                           attack_f1_list: List[float]) -> Dict[str, Any]:
    """Compute relative F1 metrics between baseline and attack."""
    if not baseline_f1_list or not attack_f1_list:
        return None

    baseline_f1 = np.mean(baseline_f1_list)
    attack_f1 = np.mean(attack_f1_list)

    baseline_std = np.std(baseline_f1_list) if len(baseline_f1_list) > 1 else 0.0
    attack_std = np.std(attack_f1_list) if len(attack_f1_list) > 1 else 0.0

    # Gap: attack - baseline (negative = attack more effective)
    gap = attack_f1 - baseline_f1

    # Relative drop (positive = attack effective)
    relative_f1_drop = -gap

    return {
        'baseline': {
            'f1_after_mean': float(baseline_f1),
            'f1_after_std': float(baseline_std),
            'n_samples': len(baseline_f1_list)
        },
        'attack': {
            'f1_after_mean': float(attack_f1),
            'f1_after_std': float(attack_std),
            'n_samples': len(attack_f1_list)
        },
        'gap': float(gap),
        'relative_f1_drop': float(relative_f1_drop),
        'interpretation': _interpret_gap(gap)
    }


def _interpret_gap(gap: float) -> str:
    """Interpret the gap value."""
    if gap < -0.02:
        return "attack effective: F1 significantly lower than baseline"
    elif gap < 0:
        return "attack slightly effective: F1 lower than baseline"
    elif gap < 0.02:
        return "no significant difference"
    else:
        return "baseline outperforms: attack may be counterproductive"


def main():
    parser = argparse.ArgumentParser(description='Compute relative F1 metrics')
    parser.add_argument('--methods', type=str,
                        default='GraphEraser,GUIDE,GNNDelete,GIF',
                        help='Comma-separated list of methods')
    parser.add_argument('--datasets', type=str, default='cora',
                        help='Comma-separated list of datasets')
    parser.add_argument('--strategies', type=str,
                        default='im,tracin,hybrid,degree,pagerank',
                        help='Comma-separated list of attack strategies to compare vs random')
    parser.add_argument('--baseline_dir', type=str,
                        default='results/experiments/mg0_completion/phase_a',
                        help='Directory containing results')
    parser.add_argument('--mode', type=str, choices=['summary', 'k5'], default='summary',
                        help='Data source: summary (_summary.json) or k5 (individual result files)')
    parser.add_argument('--ratio', type=float, default=0.05,
                        help='Unlearn ratio (for summary mode, e.g., 0.05)')
    parser.add_argument('--k', type=int, default=None,
                        help='Number of nodes to unlearn (for k5 mode)')
    parser.add_argument('--output_dir', type=str, default='results/relative',
                        help='Output directory for relative metrics')
    parser.add_argument('--force', action='store_true',
                        help='Force recalculation (ignore cache)')
    parser.add_argument('--max_age_days', type=int, default=30,
                        help='Cache max age in days')
    args = parser.parse_args()

    # Use baseline_dir as attack_dir for summary mode
    if args.mode == 'summary':
        args.attack_dir = args.baseline_dir
    else:
        # For k5 mode, default k to 5 if not specified
        if args.k is None:
            args.k = 5
            print(f"[Info] Using default k={args.k}")

    # Initialize cache
    cache = RelativeMetricsCache(args.output_dir, args.max_age_days)

    # Check cache first
    if not args.force:
        cached = cache.get(args)
        if cached:
            print(f"\n[Cache] Using cached results from {cached.get('cached_at')}")
            for r in cached.get('results', []):
                print(f"  {r['method']} | {r['dataset']} | {r['strategy']}: "
                      f"gap={r['gap']:.4f}, relative_f1_drop={r['relative_f1_drop']:.4f}")
            return cached

    # Parse inputs
    methods = args.methods.split(',')
    datasets = args.datasets.split(',')
    strategies = args.strategies.split(',')

    print(f"\nComputing relative F1 metrics:")
    print(f"  Methods: {methods}")
    print(f"  Datasets: {datasets}")
    print(f"  Strategies (vs random): {strategies}")
    print(f"  Baseline dir: {args.baseline_dir}")
    print(f"  Mode: {args.mode}")
    if args.mode == 'summary':
        print(f"  Ratio: {args.ratio}")
    else:
        print(f"  K: {args.k}")
    print()

    results = []

    for method in methods:
        for dataset in datasets:
            # Load strategy results based on mode
            if args.mode == 'summary':
                strategy_f1 = load_strategy_f1_summary(
                    args.baseline_dir, method, dataset, args.ratio
                )
            else:  # k5 mode
                # Load baseline (random) from baseline_dir
                baseline_f1 = load_k5_results(
                    args.baseline_dir, method, dataset,
                    strategy='random', k=args.k
                )
                # Load attack strategies from baseline_dir (same dir for now)
                attack_f1 = load_k5_results(
                    args.baseline_dir, method, dataset,
                    strategy=None, k=args.k
                )
                # Merge baseline into strategy_f1 format
                strategy_f1 = attack_f1
                if 'random' not in strategy_f1 and baseline_f1.get('random', {}).get('f1_after'):
                    strategy_f1['random'] = baseline_f1['random']

            if 'random' not in strategy_f1:
                print(f"[Warning] No 'random' baseline found for {method}_{dataset}")
                print(f"  Available strategies: {list(strategy_f1.keys())}")
                continue

            baseline_f1_list = strategy_f1['random']['f1_after']
            baseline_n = len(baseline_f1_list)
            print(f"[{method}_{dataset}] Random baseline: {baseline_n} samples, "
                  f"f1_after={np.mean(baseline_f1_list):.4f}")

            # Compare each strategy against random
            for strategy in strategies:
                if strategy not in strategy_f1:
                    print(f"  [Warning] No results for strategy '{strategy}'")
                    continue

                attack_f1_list = strategy_f1[strategy]['f1_after']
                attack_n = len(attack_f1_list)

                if not attack_f1_list:
                    continue

                metrics = compute_relative_metrics(baseline_f1_list, attack_f1_list)

                if metrics is None:
                    continue

                result = {
                    'method': method,
                    'dataset': dataset,
                    'strategy': strategy,
                    'baseline_strategy': 'random',
                    'ratio': args.ratio,
                    **metrics
                }
                results.append(result)

                print(f"  {strategy}: gap={metrics['gap']:.4f}, "
                      f"relative_f1_drop={metrics['relative_f1_drop']:.4f} "
                      f"({metrics['interpretation']})")

    # Save to cache
    if results:
        cache.save(args, results)
        output_file = cache._get_cache_path(cache._generate_cache_key(args))
        print(f"\n[Output] Results saved to: {output_file}")
    else:
        print("\n[Warning] No results computed!")

    return results


if __name__ == '__main__':
    main()
