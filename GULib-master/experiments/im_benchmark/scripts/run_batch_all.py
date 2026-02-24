import os
import subprocess
import json

datasets = ["citeseer", "cora"]
seeds = [2024]
k_values = [50, 135]
python_path = r"H:\conda_package\envs\gnn\python.exe"
bench_script = r"experiments\im_benchmark\run_benchmark.py"
res_file = "experiments/im_benchmark/bench_results.json"
summary_file = "experiments/im_benchmark/multi_v1_v3_summary.md"

variants = ["V1: Fast-Hash", "V2: Top-K", "V3: Pruning (M=400)", "V4: Batch (B=5)"]

with open(summary_file, "w", encoding="utf-8") as out_md:
    out_md.write("# All Variants Benchmark Results (Seed=2024)\n\n")

for dataset in datasets:
    for k in k_values:
        print(f"--- Running: Dataset={dataset}, K={k} ---")
        
        # Skip V1 on Cora K=135 because it takes 15+ minutes
        branches = "all"
        if dataset == "cora" and k == 135:
            branches = "v0,v2,v3,v4"
            
        if os.path.exists(res_file):
            os.remove(res_file)
            
        cmd = [
            python_path, 
            bench_script, 
            "--dataset_name", dataset, 
            "--seed", "2024", 
            "--k", str(k),
            "--branch", branches
        ]
        
        subprocess.run(cmd, check=True)
        
        if os.path.exists(res_file):
            with open(res_file, "r", encoding="utf-8") as rf:
                res = json.load(rf)
            
            v0_res = res.get("V0: Baseline", {})
            v0_time = v0_res.get("time", 0)
            v0_spread = v0_res.get("spread", 0)
            v0_sel = set(v0_res.get("selected", []))
            
            with open(summary_file, "a", encoding="utf-8") as out_md:
                out_md.write(f"### Dataset: `{dataset}`, K: `{k}`\n")
                out_md.write(f"**Baseline (V0)**: Time = {v0_time:.2f}s, Spread = {v0_spread:.2f}\n\n")
                out_md.write("| Variant | Time (s) | Speedup | Spread | Spread Loss (%) | Overlap (%) |\n")
                out_md.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
                
                for var_name in variants:
                    if var_name not in res:
                        out_md.write(f"| **{var_name}** | Skipped (Too slow) | - | - | - | - |\n")
                        continue
                        
                    vr = res[var_name]
                    v_time = vr.get("time", 0)
                    v_spread = vr.get("spread", 0)
                    v_sel = set(vr.get("selected", []))
                    
                    speedup = v0_time / v_time if v_time > 0 else 0
                    spread_loss = (v0_spread - v_spread) / v0_spread * 100 if v0_spread > 0 else 0
                    overlap = len(v0_sel.intersection(v_sel)) / k * 100 if k > 0 else 0
                    
                    out_md.write(f"| **{var_name}** | {v_time:.2f}s | **{speedup:.1f}x** | {v_spread:.2f} | {spread_loss:.2f}% | {overlap:.1f}% |\n")
                out_md.write("\n")

print(f"Done. Summary saved to {summary_file}")
