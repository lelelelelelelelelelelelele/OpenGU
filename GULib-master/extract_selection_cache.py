"""
Extract selected_nodes from phase_a results and create selection_cache entries.

This enables cache hits for random/pagerank/im strategies when running
GraphEraser/GUIDE experiments with the same seeds.

Usage:
    # Extract caches for k=135 (ratio=0.05) from existing results
    python extract_selection_cache.py --seeds 42,212,722,1337

    # Generate smaller k cache from larger k results
    python extract_selection_cache.py --generate-subset --source-k 270 --target-k 135
"""
import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import hashlib
import numpy as np

# Base paths
PHASE_A_DIR = Path("results/experiments/phase_a")
CACHE_DIR = Path("results/selection_cache")

# Seeds and strategies
SEEDS = [42, 212, 722, 1337]
# Only cacheable strategies (per REUSABLE_SELECTION_STRATEGIES in attack_manager.py)
CACHEABLE_STRATEGIES = ["random", "pagerank", "im"]

# Fixed config values (must match what attack_manager uses)
DATASET_NAME = "cora"
BASE_MODEL = "GCN"
UNLEARN_RATIO = 0.05
IS_TRANSDUCTIVE = True
IS_BALANCED = False
TRAIN_RATIO = 0.8
VAL_RATIO = 0.0
TEST_RATIO = 0.2

# All seeds have same fingerprint (seed doesn't affect data split in original_dataset)
GRAPH_FINGERPRINT = "a3761845fa1231ca9ff4c4bfbb97fe89"

# Cora node count
CORA_NUM_NODES = 2708


def stable_json(config: dict) -> str:
    """Match SelectionCache._stable_json"""
    return json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def build_selection_key(config: dict) -> str:
    """Match SelectionCache.build_selection_key"""
    key_string = stable_json(config)
    digest = hashlib.sha256(key_string.encode("utf-8")).hexdigest()
    return digest[:32]


def get_strategy_params_fingerprint(strategy_name: str) -> str:
    """Match _strategy_params_for_cache + _stable_hash"""
    if strategy_name == "im":
        params = {"propagation_prob": 0.1, "mc_rounds": 100, "candidate_fraction": 1.0}
    elif strategy_name == "pagerank":
        params = {"pagerank_alpha": 0.85}
    else:
        params = {}
    return build_selection_key(params)


def create_cache_entry(strategy_name: str, seed: int, selected_nodes: list,
                      selection_time: float, k: int, source_k: int = None):
    """Create a selection_cache entry."""
    strategy_params_fp = get_strategy_params_fingerprint(strategy_name)

    # Calculate unlearn_ratio from k if not default
    if source_k and source_k != CORA_NUM_NODES:
        unlearn_ratio = k / CORA_NUM_NODES
    else:
        unlearn_ratio = UNLEARN_RATIO

    config = {
        "dataset_name": DATASET_NAME,
        "base_model": BASE_MODEL,
        "unlearn_ratio": unlearn_ratio,
        "seed": seed,
        "strategy_name": strategy_name,
        "k": k,
        "is_transductive": IS_TRANSDUCTIVE,
        "is_balanced": IS_BALANCED,
        "train_ratio": TRAIN_RATIO,
        "val_ratio": VAL_RATIO,
        "test_ratio": TEST_RATIO,
        "graph_fingerprint": GRAPH_FINGERPRINT,
        "strategy_params_fingerprint": strategy_params_fp,
    }

    cache_key = build_selection_key(config)

    entry = {
        "cache_key": cache_key,
        "cached_at": datetime.now().isoformat(),
        "config": config,
        "selection_result": {
            "strategy_name": strategy_name,
            "selected_nodes": selected_nodes,
            "selection_time": selection_time,
            "selection_key": cache_key,
            "created_at": datetime.now().isoformat(),
            "metadata": {
                "dataset_name": DATASET_NAME,
                "base_model": BASE_MODEL,
                "seed": seed,
                "graph_fingerprint": GRAPH_FINGERPRINT,
                "source_k": source_k,
                "generated_subset": True if source_k and source_k != k else False,
            }
        }
    }

    return cache_key, entry


def extract_from_phase_a():
    """Extract caches from existing phase_a results."""
    print("Extracting selected_nodes from phase_a results...")
    print(f"Seeds: {SEEDS}")
    print(f"Cacheable strategies: {CACHEABLE_STRATEGIES}")
    print(f"Graph fingerprint: {GRAPH_FINGERPRINT}")
    print()

    # Find all phase_a result directories
    phase_dirs = sorted([d for d in PHASE_A_DIR.iterdir() if d.is_dir() and "_seed" in d.name])
    print(f"Found {len(phase_dirs)} phase_a directories")

    created = 0

    for phase_dir in phase_dirs:
        # Extract seed from directory name (e.g., "20260220_195416_seed42" -> 42)
        dir_name = phase_dir.name
        if "_seed" not in dir_name:
            continue
        seed = int(dir_name.split("_seed")[1])
        if seed not in SEEDS:
            continue

        print(f"\nProcessing seed={seed}...")

        # Find GNNDelete result file
        gnn_delete_file = phase_dir / f"GNNDelete_cora_GCN_r0.05_s{seed}.json"
        if not gnn_delete_file.exists():
            print(f"  Warning: {gnn_delete_file.name} not found")
            continue

        with open(gnn_delete_file, "r") as f:
            data = json.load(f)

        results = data.get("results", {})

        for strategy_name in CACHEABLE_STRATEGIES:
            if strategy_name not in results:
                print(f"  Warning: strategy {strategy_name} not found in results")
                continue

            strategy_result = results[strategy_name]
            selected_nodes = strategy_result.get("selected_nodes", [])
            selection_time = strategy_result.get("total_time", 1.0)

            if not selected_nodes:
                print(f"  Warning: no selected_nodes for {strategy_name}")
                continue

            k = len(selected_nodes)
            cache_key, entry = create_cache_entry(
                strategy_name, seed, selected_nodes, selection_time, k
            )

            # Write cache file
            cache_file = CACHE_DIR / f"{cache_key}.json"
            with open(cache_file, "w") as f:
                json.dump(entry, f, indent=2, ensure_ascii=True)

            print(f"  Created: {strategy_name} (k={k}) -> {cache_file.name}")
            created += 1

    print(f"\n{'='*60}")
    print(f"Created {created} selection_cache entries")
    print(f"Cache directory: {CACHE_DIR}")
    print(f"{'='*60}")


def generate_subset_from_source(source_k: int, target_k: int):
    """
    Generate smaller k caches from larger k results.

    For example, if we have results for k=270 (ratio=0.1), we can extract
    the first 135 nodes to create caches for k=135 (ratio=0.05).
    """
    print(f"Generating subset caches: source_k={source_k} -> target_k={target_k}")
    print(f"Ratio: {target_k}/{CORA_NUM_NODES} = {target_k/CORA_NUM_NODES:.4f}")
    print()

    # Find result files with source_k
    # Look for ratio = source_k / 2708
    source_ratio = source_k / CORA_NUM_NODES

    # Find all phase_a directories
    phase_dirs = sorted([d for d in PHASE_A_DIR.iterdir() if d.is_dir() and "_seed" in d.name])

    if not phase_dirs:
        print("No phase_a directories found!")
        return

    # Find a directory with source_k results
    source_dir = None
    for d in phase_dirs:
        # Check for files with source ratio
        ratio_str = f"r{source_ratio:.2f}"
        files = list(d.glob(f"*_cora_GCN_{ratio_str}_*.json"))
        if files:
            source_dir = d
            break

    if not source_dir:
        print(f"No results found for k={source_k} (ratio={source_ratio:.2f})")
        print("Available files:")
        for d in phase_dirs[:3]:
            files = list(d.glob("*.json"))
            for f in files:
                print(f"  {f.name}")
        return

    print(f"Using source directory: {source_dir.name}")

    created = 0

    # Get seeds from directory names
    for phase_dir in phase_dirs:
        dir_name = phase_dir.name
        if "_seed" not in dir_name:
            continue
        seed = int(dir_name.split("_seed")[1])
        if seed not in SEEDS:
            continue

        # Look for result file with source_k
        source_file = None
        for strategy_name in CACHEABLE_STRATEGIES:
            # Try different method names and ratio formats
            for ratio_str in [f"r{source_ratio:.2f}", f"r{source_ratio:.1f}"]:
                for method in ["GNNDelete", "GIF"]:
                    f = phase_dir / f"{method}_cora_GCN_{ratio_str}_s{seed}.json"
                    if f.exists():
                        source_file = f
                        break
                if source_file:
                    break
            if source_file:
                break

        if not source_file:
            # Try default ratio 0.05
            f = phase_dir / f"GNNDelete_cora_GCN_r0.05_s{seed}.json"
            if f.exists():
                source_file = f
                source_k_actual = 135  # 2708 * 0.05
            else:
                continue
        else:
            # Infer actual source_k from filename
            source_k_actual = source_k

        print(f"\nProcessing seed={seed} from {source_file.name}...")

        with open(source_file, "r") as f:
            data = json.load(f)

        results = data.get("results", {})

        for strategy_name in CACHEABLE_STRATEGIES:
            if strategy_name not in results:
                continue

            strategy_result = results[strategy_name]
            all_nodes = strategy_result.get("selected_nodes", [])
            selection_time = strategy_result.get("total_time", 1.0)

            if not all_nodes or len(all_nodes) < target_k:
                print(f"  Warning: not enough nodes for {strategy_name} ({len(all_nodes)} < {target_k})")
                continue

            # Take first target_k nodes
            selected_nodes = all_nodes[:target_k]

            cache_key, entry = create_cache_entry(
                strategy_name, seed, selected_nodes, selection_time,
                k=target_k, source_k=source_k_actual
            )

            # Write cache file
            cache_file = CACHE_DIR / f"{cache_key}.json"
            with open(cache_file, "w") as f:
                json.dump(entry, f, indent=2, ensure_ascii=True)

            print(f"  Created: {strategy_name} (k={target_k} from {len(all_nodes)}) -> {cache_file.name}")
            created += 1

    print(f"\n{'='*60}")
    print(f"Created {created} subset selection_cache entries (k={target_k})")
    print(f"Cache directory: {CACHE_DIR}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Extract selection_cache from phase_a results")
    parser.add_argument("--seeds", type=str, default="42,212,722,1337",
                       help="Comma-separated seeds")
    parser.add_argument("--strategies", type=str, default="random,pagerank,im",
                       help="Comma-separated strategies")
    parser.add_argument("--generate-subset", action="store_true",
                       help="Generate subset caches from larger k results")
    parser.add_argument("--source-k", type=int, default=270,
                       help="Source k for subset generation (default: 270)")
    parser.add_argument("--target-k", type=int, default=135,
                       help="Target k for subset generation (default: 135)")

    args = parser.parse_args()

    global SEEDS, CACHEABLE_STRATEGIES
    SEEDS = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    CACHEABLE_STRATEGIES = [s.strip() for s in args.strategies.split(",") if s.strip()]

    if args.generate_subset:
        generate_subset_from_source(args.source_k, args.target_k)
    else:
        extract_from_phase_a()


if __name__ == "__main__":
    main()
