import sys
import os
import time
import random
import heapq
import numpy as np
import torch
import json

# --- START: Early Argument Parsing ---
# We must parse and remove our custom arguments before any main project imports
# because main project config.py runs parameter_parser() at module level.
class BenchArgs:
    def __init__(self):
        self.seed = 2024
        self.resume = False
        self.branch = "all"
        self.dataset_name = "cora"
        self.k = 135
        
global_bench_args = BenchArgs()

original_argv = sys.argv.copy()
sys.argv = [original_argv[0]] # Keep only the script name for parameter_parser

i = 1
while i < len(original_argv):
    arg = original_argv[i]
    if arg == "--seed" and i + 1 < len(original_argv):
        global_bench_args.seed = int(original_argv[i + 1])
        i += 2
    elif arg == "--resume":
        global_bench_args.resume = True
        i += 1
    elif arg == "--branch" and i + 1 < len(original_argv):
        global_bench_args.branch = original_argv[i + 1]
        i += 2
    elif arg == "--dataset_name" and i + 1 < len(original_argv):
        global_bench_args.dataset_name = original_argv[i + 1]
        i += 2
    elif arg == "--k" and i + 1 < len(original_argv):
        global_bench_args.k = int(original_argv[i + 1])
        i += 2
    else:
        # If it's something else, let parameter_parser handle it
        sys.argv.append(arg)
        i += 1
# --- END: Early Argument Parsing ---

# Add project root to path so we can import attack modules and config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from parameter_parser import parameter_parser
from utils.logger import create_logger
from dataset.original_dataset import original_dataset
from utils.dataset_utils import process_data

from attack.attack_strategies.im_strategy import IMStrategy, _estimate_spread_numba, HAS_NUMBA

# Check Numba availability once
if HAS_NUMBA:
    print("Numba is available. Using accelerated spread estimations.")
else:
    print("Numba is NOT available. Falling back to pure Python.")

# --- Evaluation Function ---
def evaluate_spread(edge_index, num_nodes, selected_nodes, propagation_prob=0.1, mc_rounds=1000):
    """
    Independent evaluation of the final spread using fixed random seeds for fair comparison.
    """
    # Create IMStrategy instance just to use its adjacency builders
    im = IMStrategy({'propagation_prob': propagation_prob, 'mc_rounds': mc_rounds})
    
    selected_tensor = torch.tensor(selected_nodes, dtype=torch.long)
    
    if HAS_NUMBA:
        indptr, indices = im._build_adjacency_csr(edge_index, num_nodes)
        
        # We need a fixed seed sequence for fair evaluation.
        # We'll run mc_rounds simulations, summing up the spread.
        total_spread = 0.0
        
        # The numba kernel expects a seed_array of type int32
        seed_arr = selected_tensor.cpu().numpy().astype(np.int32)
        
        # To ensure the exact same evaluation across different variants,
        # we fix a universal base seed for this evaluation process.
        eval_base_seed = 99999
        
        # Numba's _estimate_spread_numba does all rounds and averages them
        avg_spread = _estimate_spread_numba(
            indptr, indices, seed_arr, propagation_prob, num_nodes, mc_rounds, eval_base_seed
        )
        return float(avg_spread)
        
    else:
        # Fallback to pure Python if numba is absent
        adj = im._build_adjacency_python(edge_index, num_nodes)
        seed_set = set(selected_nodes)
        
        total_spread = 0.0
        for r in range(mc_rounds):
            # Deterministic seed per round
            random.seed(99999 + r)
            total_spread += im._simulate_spread(adj, seed_set, propagation_prob, num_nodes)
            
        return total_spread / mc_rounds


# --- Variant Implementations ---

# V0: Baseline
def run_v0(im_strategy, edge_index, num_nodes, k, candidate_set):
    # Just run the standard compute_im_celf
    selected, _ = im_strategy.compute_im_celf(edge_index, num_nodes, k, candidate_set)
    return selected

# V1: FastHash
def run_v1(im_strategy, edge_index, num_nodes, k, candidate_set):
    # We must redefine _compute_im_celf_numba to change the base_seed line.
    # Since IMStrategy has a python and numba path, we'll patch both or just use Numba if available.
    if not HAS_NUMBA:
        print("Warning: V1 fallback to Python is identical to V0 because purely Python doesn't use the np arr sort in IMStrategy. Run skipped/matched.")
        return im_strategy._compute_im_celf_python(edge_index, num_nodes, k, candidate_set)[0]
        
    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds

    heap = []
    for node in candidate_set:
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = im_strategy.random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        heapq.heappush(heap, (-spread, 0, node))

    selected = []
    selected_set_list = []
    current_spread = 0.0

    for i in range(k):
        while True:
            neg_gain, last_updated, node = heapq.heappop(heap)

            if last_updated == i:
                selected.append(node)
                selected_set_list.append(node)
                current_spread += (-neg_gain)
                break
            else:
                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                # --- V1 FastHash Optimization ---
                base_seed = im_strategy.random_seed * 10000 + abs(hash(frozenset(selected_set_list + [node]))) % 10000
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, i, node))

    return selected

# V2: Top-K
def run_v2(im_strategy, edge_index, num_nodes, k, candidate_set):
    scores = im_strategy.compute_initial_marginal_gains(edge_index, num_nodes, candidate_set)
    # Directly pick top-k initial gains
    _, top_idx = torch.topk(scores, k)
    # Map back to original candidate nodes
    selected = [candidate_set[i] for i in top_idx.tolist()]
    return selected

# V3: Pruning
def run_v3(im_strategy, edge_index, num_nodes, k, candidate_set, M=400):
    # Prune candidates to top M
    pruned_candidates = im_strategy._prune_candidates_by_degree(
        edge_index, num_nodes, candidate_set, fraction=(M / len(candidate_set)), min_k=k
    )
    # Ensure we strictly have at most M and at least k
    pruned_candidates = pruned_candidates[:max(M, k)]
    
    # Run V1 (FastHash) on the pruned dataset
    return run_v1(im_strategy, edge_index, num_nodes, k, pruned_candidates)

# V4: Batch CELF
def run_v4(im_strategy, edge_index, num_nodes, k, candidate_set, B=5):
    if not HAS_NUMBA:
         print("Warning: V4 fallback to Python not implemented optimally in this isolated test.")
         return im_strategy._compute_im_celf_python(edge_index, num_nodes, k, candidate_set)[0]

    indptr, indices = im_strategy._build_adjacency_csr(edge_index, num_nodes)
    prob = im_strategy.propagation_prob
    mc = im_strategy.mc_rounds

    heap = []
    for node in candidate_set:
        seed_arr = np.array([node], dtype=np.int32)
        base_seed = im_strategy.random_seed * 10000 + node % 10000
        spread = _estimate_spread_numba(indptr, indices, seed_arr, prob, num_nodes, mc, base_seed)
        heapq.heappush(heap, (-spread, 0, node))

    selected = []
    selected_set_list = []
    current_spread = 0.0

    # Instead of outer loop `for i in range(k)`, we loop until len(selected) == k
    i = 0
    while len(selected) < k:
        # Determine how many we can pop in this batch
        batch_size = min(B, k - len(selected))
        
        while True:
            # Re-eval the top node
            neg_gain, last_updated, node = heapq.heappop(heap)

            if last_updated == i:
                # Top node is confirmed highest marginal gain.
                # In standard CELF, we accept it.
                # In Batch CELF, we accept this node AND the next (batch_size - 1) nodes in the heap without re-evaluating!
                
                selected.append(node)
                selected_set_list.append(node)
                current_spread += (-neg_gain)
                
                # Pop next batch_size - 1 nodes
                popped_count = 1
                while popped_count < batch_size and heap:
                    # We just assume they are good enough
                    next_neg_gain, _, next_node = heapq.heappop(heap)
                    selected.append(next_node)
                    selected_set_list.append(next_node)
                    # Note: adding them might change real spread non-linearly, 
                    # but we approximate by just taking them
                    current_spread += (-next_neg_gain)
                    popped_count += 1
                
                break
            else:
                seed_arr = np.array(selected_set_list + [node], dtype=np.int32)
                # Use FastHash V1 methodology to avoid np.sort overhead
                base_seed = im_strategy.random_seed * 10000 + abs(hash(frozenset(selected_set_list + [node]))) % 10000
                new_spread = _estimate_spread_numba(
                    indptr, indices, seed_arr, prob, num_nodes, mc, base_seed
                )
                marginal = new_spread - current_spread
                heapq.heappush(heap, (-marginal, i, node))
        i += 1
        
    return selected

def main():
    bench_args = global_bench_args
    print(f"Loading {bench_args.dataset_name} dataset via original_dataset (Seed: {bench_args.seed})...", flush=True)
    args = parameter_parser()
    args['dataset_name'] = bench_args.dataset_name
    args['base_model'] = 'GCN' # Dummy required for logger
    args['random_seed'] = bench_args.seed
    
    logger = create_logger(args)
    orig_data = original_dataset(args, logger)
    data, dataset = orig_data.load_data()
    data = process_data(logger, data, args)
    
    num_nodes = data.num_nodes
    edge_index = data.edge_index
    
    k = bench_args.k
    prob = 0.1
    celf_mc = 100
    eval_mc = 1000
    
    print(f"Dataset: {bench_args.dataset_name} (Nodes: {num_nodes}, Edges: {edge_index.shape[1]})")
    print(f"Target nodes k = {k}, prob p = {prob}, CELF MC = {celf_mc}, Eval MC = {eval_mc}")
    
    # Use training nodes as candidates (following IM strategy rules)
    candidate_set = data.train_indices
    
    im_strategy = IMStrategy({
        'propagation_prob': prob,
        'mc_rounds': celf_mc,
        'random_seed': bench_args.seed
    })
    
    results = {}
    cache_file = "experiments/im_benchmark/bench_results.json"
    
    if bench_args.resume and os.path.exists(cache_file):
        print(f"Loading cached results from {cache_file}...", flush=True)
        with open(cache_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
            
    baseline_selected = set()
    baseline_spread = 0.0
    
    if "V0: Baseline" in results:
        baseline_selected = set(results["V0: Baseline"]['selected'])
        baseline_spread = results["V0: Baseline"]['spread']
    
    def measure_variant(name, func, *args):
        # We need to distinguish between completely missing from cache
        # vs. present in cache but spread == 0.0 (like injected by find_v0.py)
        if bench_args.resume and name in results:
            cached_res = results[name]
            if cached_res.get('spread', 0.0) > 0.0:
                print(f"Skipping {name} (Already in cache with spread={cached_res['spread']})", flush=True)
                return cached_res
            else:
                print(f"Found {name} in cache but spread is 0.0. Will evaluate spread only.", flush=True)
                # Instead of running the full function, we just evaluate spread of the cached selected nodes
                print(f"Evaluating Final Spread ({eval_mc} MC simulations)...", flush=True)
                spread = evaluate_spread(edge_index, num_nodes, cached_res['selected'], prob, eval_mc)
                cached_res['spread'] = spread
                results[name] = cached_res
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                return cached_res
                
        print(f"\n--- Running {name} ---", flush=True)
        start_t = time.time()
        selected = func(*args)
        end_t = time.time()
        elapsed = end_t - start_t
        
        print(f"Evaluating Final Spread ({eval_mc} MC simulations)...", flush=True)
        spread = evaluate_spread(edge_index, num_nodes, selected, prob, eval_mc)
        
        res_dict = {
            'time': elapsed,
            'selected': selected,
            'spread': spread
        }
        
        results[name] = res_dict
        # Save cache immediately after each run
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        return res_dict

    # Determine which branches to run
    branches = [b.lower().strip() for b in bench_args.branch.split(',')]
    run_all = 'all' in branches
    
    # Run variants based on filter
    
    # V0
    if run_all or 'v0' in branches:
        v0_res = measure_variant("V0: Baseline", run_v0, im_strategy, edge_index, num_nodes, k, candidate_set)
        baseline_selected = set(v0_res['selected'])
        baseline_spread = v0_res['spread']
    
    # V1
    if run_all or 'v1' in branches:
        v1_res = measure_variant("V1: Fast-Hash", run_v1, im_strategy, edge_index, num_nodes, k, candidate_set)
    
    # V2
    if run_all or 'v2' in branches:
        v2_res = measure_variant("V2: Top-K", run_v2, im_strategy, edge_index, num_nodes, k, candidate_set)
    
    # V3 (M=400)
    if run_all or 'v3' in branches:
        v3_res = measure_variant("V3: Pruning (M=400)", run_v3, im_strategy, edge_index, num_nodes, k, candidate_set, 400)
    
    # V4 (B=5)
    if run_all or 'v4' in branches:
        v4_res = measure_variant("V4: Batch (B=5)", run_v4, im_strategy, edge_index, num_nodes, k, candidate_set, 5)
    
    # Markdown Table Output
    print("\n\n# Benchmark Results\n")
    print("| 策略方案 | 耗时 (秒) | 选出节点数 | 与 Baseline 交集数 | 重叠率 (%) | 最终 Spread | 相对 Spread 损失 (%) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    
    for name, metrics in results.items():
        time_sec = metrics['time']
        sel = metrics['selected']
        spread = metrics['spread']
        
        if name == "V0: Baseline":
            intersection = len(baseline_selected)
            overlap_pct = 100.0
            loss_pct = 0.0
        else:
            intersection = len(set(sel).intersection(baseline_selected)) if baseline_selected else 0
            overlap_pct = (intersection / k) * 100.0 if k > 0 else 0.0
            if baseline_spread > 0.0:
                loss_pct = ((baseline_spread - spread) / baseline_spread) * 100.0
            else:
                loss_pct = float('nan') # Prevent ZeroDivisionError if V0 hasn't been run or spread is 0
            
        loss_str = f"{loss_pct:.2f}%" if not np.isnan(loss_pct) else "N/A"
        print(f"| **{name}** | {time_sec:.2f}s | {len(sel)} | {intersection} | {overlap_pct:.1f}% | {spread:.2f} | {loss_str} |")

if __name__ == "__main__":
    main()
