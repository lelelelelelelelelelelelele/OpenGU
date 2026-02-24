import sys
import os
import time
import numba
import numpy as np
import heapq
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from attack.attack_strategies.im_strategy import IMStrategy, _estimate_spread_numba
from parameter_parser import parameter_parser
from utils.logger import create_logger
from dataset.original_dataset import original_dataset
from utils.dataset_utils import process_data

# --- Version 0: Baseline CELF ---
def run_v0_baseline(im_strategy, edge_index, num_nodes, k, candidate_set):
    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds
    random_seed = im_strategy.random_seed

    heap = []
    # Phase 1
    for node in candidate_set:
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        heapq.heappush(heap, (-spread, 0, node))

    selected = []
    selected_set_list = []
    scores = []
    current_spread = 0.0

    # Phase 2
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
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, i, node))
    return selected

# --- Version 4: Batch CELF (B=5) ---
def run_v4_batch(im_strategy, edge_index, num_nodes, k, candidate_set, B=5):
    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds

    heap = []
    # Phase 1
    for node in candidate_set:
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = im_strategy.random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        heapq.heappush(heap, (-spread, 0, node))

    selected = []
    selected_set_list = []
    current_spread = 0.0

    # Phase 2
    i = 0
    while len(selected) < k:
        batch_size = min(B, k - len(selected))
        while True:
            neg_gain, last_updated, node = heapq.heappop(heap)
            if last_updated == i:
                selected.append(node)
                selected_set_list.append(node)
                current_spread += (-neg_gain)
                popped_count = 1
                while popped_count < batch_size and heap:
                    next_neg_gain, _, next_node = heapq.heappop(heap)
                    selected.append(next_node)
                    selected_set_list.append(next_node)
                    current_spread += (-next_neg_gain)
                    popped_count += 1
                break
            else:
                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                base_seed = im_strategy.random_seed * 10000 + int(np.sum(np.sort(seed_arr))) % 10000
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, i, node))
        i += 1
    return selected

def evaluate_final_spread(edge_index, num_nodes, selected_nodes, prob=0.1, mc_rounds=1000):
    indptr, indices = IMStrategy({})._build_adjacency_csr(edge_index, num_nodes)
    seed_arr = np.array(selected_nodes, dtype=np.int32)
    eval_base_seed = 99999
    avg_spread = _estimate_spread_numba(
        indptr, indices, seed_arr, prob, num_nodes, mc_rounds, eval_base_seed
    )
    return float(avg_spread)

# Test Matrix Definition
datasets = ["citeseer", "cora", "pubmed"] # pubmed: N=19,717
K_values = [10, 50, 150]
seed = 42

print("# Comprehensive V0 vs V4 Scalability Profiling")
print(f"{'-'*75}")
print(f"| {'Dataset':<10} | {'Nodes':<6} | {'K':<4} | {'V0 Time(s)':<11} | {'V4 Time(s)':<11} | {'Speedup':<7} |")
print(f"{'-'*75}")

original_argv = sys.argv.copy()
sys.argv = [original_argv[0]] 

for dataset_name in datasets:
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
        
    for k in K_values:
        # Evaluate V0
        t0 = time.time()
        v0_nodes = run_v0_baseline(im, data.edge_index, data.num_nodes, k, candidate_set)
        v0_time = time.time() - t0
        
        # Evaluate V4 (Batch CELF, B=5)
        t0 = time.time()
        v4_nodes = run_v4_batch(im, data.edge_index, data.num_nodes, k, candidate_set, B=5)
        v4_time = time.time() - t0
        
        speedup = (v0_time / v4_time) if v4_time > 0 else 0
        
        print(f"| {dataset_name:<10} | {data.num_nodes:<6} | {k:<4} | {v0_time:<11.2f} | {v4_time:<11.2f} | {speedup:<6.1f}x |", flush=True)

print(f"{'-'*75}")
print("Testing done!")
