import sys
import os
import time
import numba
import numpy as np
import heapq
import torch
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from attack.attack_strategies.im_strategy import IMStrategy, _simulate_spread_numba

# Project-specific imports
from parameter_parser import parameter_parser
from utils.logger import create_logger
from dataset.original_dataset import original_dataset
from utils.dataset_utils import process_data

# 1. Define the No-GIL version of the evaluation kernel
@numba.njit(cache=True, nogil=True)
def _estimate_spread_numba_nogil(indptr, indices, seed_array, prob, num_nodes, mc_rounds, base_seed):
    visited = np.zeros(num_nodes, dtype=np.int32)
    frontier = np.empty(num_nodes, dtype=np.int32)
    total = np.float64(0.0)
    stamp = np.int32(0)

    for r in range(mc_rounds):
        stamp += np.int32(1)
        if stamp >= np.int32(2_000_000_000):
            visited[:] = np.int32(0)
            stamp = np.int32(1)
        total += _simulate_spread_numba(
            indptr, indices, seed_array, prob,
            num_nodes, base_seed + r, visited,
            stamp, frontier
        )

    return total / np.float64(mc_rounds)

# 2. Parallel Implementation of CELF
def run_v5_parallel(im_strategy, edge_index, num_nodes, k, candidate_set):
    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds
    random_seed = im_strategy.random_seed

    heap = []
    
    # --- PHASE 1: Parallel Evaluation ---
    def eval_node(node):
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba_nogil(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        return (-spread, 0, node)

    # Automatically scales to optimal CPU threads for I/O and nogil tasks
    with ThreadPoolExecutor() as executor:
        results = executor.map(eval_node, candidate_set)
        
    for res in results:
        heapq.heappush(heap, res)
        
    # --- PHASE 2: Sequential Greedy Selection ---
    selected = []
    selected_set_list = []
    scores = []
    current_spread = 0.0

    for i in range(k):
        while True:
            neg_gain, last_updated, node = heapq.heappop(heap)
            if last_updated == i:
                selected.append(node)
                selected_set_list.append(node)
                scores.append(-neg_gain)
                current_spread += (-neg_gain)
                break
            else:
                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                base_seed = random_seed * 10000 + int(np.sum(np.sort(seed_arr))) % 10000
                new_spread = _estimate_spread_numba_nogil(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, i, node))

    return selected

def evaluate_final_spread(edge_index, num_nodes, selected_nodes, prob=0.1, mc_rounds=1000):
    indptr, indices = IMStrategy({})._build_adjacency_csr(edge_index, num_nodes)
    seed_arr = np.array(selected_nodes, dtype=np.int32)
    eval_base_seed = 99999
    
    avg_spread = _estimate_spread_numba_nogil(
        indptr, indices, seed_arr, prob, num_nodes, mc_rounds, eval_base_seed
    )
    return float(avg_spread)

# 3. Batch Testing Logic
experiments = [
    # Baseline Results (Time, Spread) from previous V0 runs for assertion
    ("citeseer", 2024, 50,  36.49, 2480.00),
    ("citeseer", 2024, 135, 78.11, 2763.00),
    ("cora",     2024, 50,  38.35, 2652.00),
    ("cora",     2024, 135, 652.97,2700.00),
]

print("# Independent Parallel V5 Verification Log")
print("-" * 65)
print(f"| {'Dataset':<10} | {'Seed':<4} | {'K':<3} | {'V0 Time':<8} | {'V5 Time':<8} | {'Speedup':<7} | {'Lossless?':<10} |")
print("-" * 65)

# Patch argv to avoid parameter_parser breaking
original_argv = sys.argv.copy()
sys.argv = [original_argv[0]] 

for dataset_name, seed, k, v0_time, v0_spread in experiments:
    # Suppress output from dataset loading
    sys.stdout = open(os.devnull, 'w')
    try:
        args = parameter_parser()
        args['dataset_name'] = dataset_name
        args['base_model'] = 'GCN'
        args['random_seed'] = seed
        
        logger = create_logger(args)
        orig_data = original_dataset(args, logger)
        data, _ = orig_data.load_data()
        data = process_data(logger, data, args)
        
        im = IMStrategy({"random_seed": seed, "mc_rounds": 100})
        candidate_set = data.train_indices
    finally:
        sys.stdout = sys.__stdout__
    
    # Run V5 (Parallel CELF)
    start_time = time.time()
    v5_selected = run_v5_parallel(im, data.edge_index, data.num_nodes, k, candidate_set)
    v5_time = time.time() - start_time
    
    # Calculate Spread
    v5_spread = evaluate_final_spread(data.edge_index, data.num_nodes, v5_selected)
    
    speedup = v0_time / v5_time
    
    is_lossless = abs(v5_spread - v0_spread) < 0.1
    lossless_str = "YES" if is_lossless else f"NO (Diff)"
    
    print(f"| {dataset_name:<10} | {seed:<4} | {k:<3} | {v0_time:<8.2f} | {v5_time:<8.2f} | {speedup:<6.1f}x | {lossless_str:<10} |", flush=True)

print("-" * 65)
print("Testing done!")
