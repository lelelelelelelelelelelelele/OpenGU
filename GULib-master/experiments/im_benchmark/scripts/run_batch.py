import os
import subprocess
import json

datasets = ["cora", "citeseer"]
seeds = [2024, 42]
k_values = [50, 135]
branches = "v0,v4" # Focus on baseline vs best new method
python_path = r"H:\conda_package\envs\gnn\python.exe"
bench_script = r"experiments\im_benchmark\run_benchmark.py"
res_file = "experiments/im_benchmark/bench_results.json"
summary_file = "experiments/im_benchmark/multi_run_summary.md"

with open(summary_file, "w", encoding="utf-8") as out_md:
    out_md.write("# Multi-Parameter Benchmark Results\n\n")

for dataset in datasets:
    for seed in seeds:
        for k in k_values:
            print(f"--- Running: Dataset={dataset}, Seed={seed}, K={k} ---")
            
            # Wipe previous cache to ensure fresh run for these parameters
            if os.path.exists(res_file):
                os.remove(res_file)
                
            cmd = [
                python_path, 
                bench_script, 
                "--dataset_name", dataset, 
                "--seed", str(seed), 
                "--k", str(k),
                "--branch", branches
            ]
            
            subprocess.run(cmd, check=True)
            
            # Read results
            if os.path.exists(res_file):
                with open(res_file, "r", encoding="utf-8") as rf:
                    res = json.load(rf)
                
                v0_res = res.get("V0: Baseline", {})
                v4_res = res.get("V4: Batch (B=5)", {})
                
                v0_time = v0_res.get("time", 0)
                v0_spread = v0_res.get("spread", 0)
                
                v4_time = v4_res.get("time", 0)
                v4_spread = v4_res.get("spread", 0)
                
                overlap = 0
                if v0_res and v4_res:
                    s1 = set(v0_res.get("selected", []))
                    s2 = set(v4_res.get("selected", []))
                    overlap = len(s1.intersection(s2)) / k * 100 if k > 0 else 0
                
                loss = 0
                if v0_spread > 0:
                    loss = (v0_spread - v4_spread) / v0_spread * 100
                
                with open(summary_file, "a", encoding="utf-8") as out_md:
                    out_md.write(f"### Dataset: `{dataset}`, Seed: `{seed}`, K: `{k}`\n")
                    out_md.write(f"- **V0 (Baseline)**: Time = {v0_time:.2f}s, Spread = {v0_spread:.2f}\n")
                    out_md.write(f"- **V4 (Batch B=5)**: Time = {v4_time:.2f}s, Spread = {v4_spread:.2f}\n")
                    out_md.write(f"- **Comparison**: Speedup = {v0_time/v4_time:.1f}x, Spread Loss = {loss:.2f}%, Overlap = {overlap:.1f}%\n\n")

print(f"Done. Summary saved to {summary_file}")
