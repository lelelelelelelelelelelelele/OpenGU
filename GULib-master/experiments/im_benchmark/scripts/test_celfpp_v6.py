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

def run_v6_celfpp(im_strategy, edge_index, num_nodes, k, candidate_set):
    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds
    random_seed = im_strategy.random_seed

    heap = []
    
    # Phase 1: Standard CELF eval
    for node in candidate_set:
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        
        # (-mg1, flag, prev_best, mg2_node, node)
        heapq.heappush(heap, (-spread, 0, 0.0, -1, node))
        
    selected = []
    selected_set_list = []
    scores = []
    current_spread = 0.0
    last_seed = -1

    for i in range(k):
        # Cache for `spread(S U {top_node})` to avoid redundant MCs in same iteration
        top_spread_cache = {}
        
        while True:
            neg_gain, flag, prev_best, mg2_node, node = heapq.heappop(heap)
            
            if flag == i:
                selected.append(node)
                selected_set_list.append(node)
                scores.append(-neg_gain)
                current_spread += (-neg_gain)
                last_seed = node
                break
                
            elif flag == i - 1 and mg2_node == last_seed:
                # CELF++ HIT: We perfectly predicted the next seed and computed mg1 implicitly!
                heapq.heappush(heap, (-prev_best, i, 0.0, -1, node))
                
            else:
                # CELF++ MISS: We must re-evaluate
                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                base_seed = random_seed * 10000 + int(np.sum(np.sort(seed_arr))) % 10000
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                mg1 = new_spread - current_spread
                
                # CELF++ "Lookahead": Compute prev_best for the current top node
                if len(heap) > 0:
                    top_node = heap[0][4]
                    
                    # 1. We identically need spread(S U {top_node})
                    if top_node not in top_spread_cache:
                        arr_top = np.array(selected_set_list + [top_node], dtype=np.int32)
                        bs_top = random_seed * 10000 + int(np.sum(np.sort(arr_top))) % 10000
                        ts = _estimate_spread_numba(
                            indptr, indices, arr_top, prob, num_nodes, mc, bs_top
                        )
                        top_spread_cache[top_node] = ts
                    cached_top_spread = top_spread_cache[top_node]
                    
                    # 2. We identically need spread(S U {top_node} U {node})
                    arr_both = np.array(selected_set_list + [node, top_node], dtype=np.int32)
                    bs_both = random_seed * 10000 + int(np.sum(np.sort(arr_both))) % 10000
                    spread_both = _estimate_spread_numba(
                        indptr, indices, arr_both, prob, num_nodes, mc, bs_both
                    )
                    
                    # mg2 is the marginal gain of node GIVEN top_node is selected
                    mg2 = spread_both - cached_top_spread
                else:
                    top_node = -1
                    mg2 = 0.0
                
                heapq.heappush(heap, (-mg1, i, mg2, top_node, node))

    return selected

def evaluate_final_spread(edge_index, num_nodes, selected_nodes, prob=0.1, mc_rounds=1000):
    indptr, indices = IMStrategy({})._build_adjacency_csr(edge_index, num_nodes)
    seed_arr = np.array(selected_nodes, dtype=np.int32)
    eval_base_seed = 99999
    
    avg_spread = _estimate_spread_numba(
        indptr, indices, seed_arr, prob, num_nodes, mc_rounds, eval_base_seed
    )
    return float(avg_spread)

# Batch Testing Logic
experiments = [
    ("citeseer", 2024, 50,  36.49, 2480.00),
    ("citeseer", 2024, 135, 78.11, 2763.00),
    ("cora",     2024, 50,  38.35, 2652.00),
    ("cora",     2024, 135, 652.97,2700.00),
]

print("# Independent CELF++ (V6) Verification Log")
print("-" * 65)
print(f"| {'Dataset':<10} | {'Seed':<4} | {'K':<3} | {'V0 Time':<8} | {'V6 Time':<8} | {'Speedup':<7} | {'Lossless?':<10} |")
print("-" * 65)

original_argv = sys.argv.copy()
sys.argv = [original_argv[0]] 

for dataset_name, seed, k, v0_time, v0_spread in experiments:
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
    
    start_time = time.time()
    v6_selected = run_v6_celfpp(im, data.edge_index, data.num_nodes, k, candidate_set)
    v6_time = time.time() - start_time
    
    v6_spread = evaluate_final_spread(data.edge_index, data.num_nodes, v6_selected)
    speedup = v0_time / v6_time
    is_lossless = abs(v6_spread - v0_spread) < 0.1
    lossless_str = "YES" if is_lossless else f"NO (Diff)"
    
    print(f"| {dataset_name:<10} | {seed:<4} | {k:<3} | {v0_time:<8.2f} | {v6_time:<8.2f} | {speedup:<6.1f}x | {lossless_str:<10} |", flush=True)

print("-" * 65)
print("Testing done!")
