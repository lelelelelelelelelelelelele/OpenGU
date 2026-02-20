"""
Extract selected_nodes from phase_a results and create selection_cache entries.

This enables cache hits for random/pagerank/im strategies when running
GraphEraser/GUIDE experiments with the same seeds.
"""
import json
import os
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


def create_cache_entry(strategy_name: str, seed: int, selected_nodes: list, selection_time: float):
    """Create a selection_cache entry."""
    strategy_params_fp = get_strategy_params_fingerprint(strategy_name)

    # k = number of nodes = unlearn_ratio * num_nodes
    # For cora: 2708 nodes * 0.05 = 135.4 -> 135
    k = int(2708 * UNLEARN_RATIO)

    config = {
        "dataset_name": DATASET_NAME,
        "base_model": BASE_MODEL,
        "unlearn_ratio": UNLEARN_RATIO,
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
            }
        }
    }

    return cache_key, entry


def main():
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
            selection_time = strategy_result.get("total_time", 1.0)  # Use total_time as proxy

            if not selected_nodes:
                print(f"  Warning: no selected_nodes for {strategy_name}")
                continue

            cache_key, entry = create_cache_entry(
                strategy_name, seed, selected_nodes, selection_time
            )

            # Write cache file
            cache_file = CACHE_DIR / f"{cache_key}.json"
            with open(cache_file, "w") as f:
                json.dump(entry, f, indent=2, ensure_ascii=True)

            print(f"  Created: {strategy_name} -> {cache_file.name}")
            created += 1

    print(f"\n{'='*60}")
    print(f"Created {created} selection_cache entries")
    print(f"Cache directory: {CACHE_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
