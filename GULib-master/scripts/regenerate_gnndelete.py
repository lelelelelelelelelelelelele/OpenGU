"""Batch script to regenerate GNNDelete baselines and relative evaluations."""
import os
import subprocess
import time

methods = ["GNNDelete"]
datasets = ["cora", "citeseer"]
models = ["GCN", "GAT"]
seeds = [42, 212, 722, 1337, 2024]
k_seeds = [111, 333, 555, 777, 999]
ratios = [0.01, 0.05, 0.1, 0.2]

def run_cmd(cmd):
    print(f"\n>> Running: {cmd}")
    t0 = time.time()
    result = subprocess.run(cmd, shell=True)
    t1 = time.time()
    if result.returncode != 0:
        print(f"[!] Command failed (exit code {result.returncode})")
        return False
    print(f"[+] Success ({t1-t0:.1f}s)")
    return True

print("="*80)
print("PHASE 1: Generating GNNDelete K=5 Baselines")
print("="*80)
for method in methods:
    for dataset in datasets:
        for model in models:
            # Only run GCN for citeseer currently based on how things were set up
            if dataset == "citeseer" and model == "GAT":
                continue
            for k_seed in k_seeds:
                cmd = f"conda run -n gnn python experiments/baseline_k5/generate_baseline.py --dataset_name {dataset} --base_model {model} --unlearning_methods {method} --random_seed {k_seed} --baseline_k 5"
                if not run_cmd(cmd):
                    exit(1)

print("\n" + "="*80)
print("PHASE 2: Aggregating GNNDelete K=5 Baselines")
print("="*80)
cmd = "conda run -n gnn python experiments/baseline_k5/run_all_baselines.py"
if not run_cmd(cmd):
    exit(1)

print("\n" + "="*80)
print("PHASE 3: Re-running eval_relative.py for GNNDelete")
print("="*80)
for method in methods:
    for dataset in datasets:
        for model in models:
            if dataset == "citeseer" and model == "GAT":
                continue
            for seed in seeds:
                for ratio in ratios:
                    cmd = f"conda run -n gnn python experiments/baseline_k5/eval_relative.py --dataset_name {dataset} --base_model {model} --unlearning_methods {method} --random_seed {seed} --unlearn_ratio {ratio}"
                    run_cmd(cmd)

print("\n" + "="*80)
print("COMPLETED ALL PHASES")
print("================================================================================")
