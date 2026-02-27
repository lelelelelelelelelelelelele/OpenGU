import subprocess
import os

python_path = "H:/conda_package/envs/gnn/python.exe"
methods = ["GIF", "GNNDelete", "GraphEraser"]
datasets = ["cora", "citeseer"]
models = ["GCN", "GAT", "GIN"]
ratios = [0.01, 0.05, 0.1, 0.2]
seeds = [42, 212, 722, 1337, 2024]

for method in methods:
    for dataset in datasets:
        for model in models:
            for ratio in ratios:
                for seed in seeds:
                    # Check if relative file already exists for this config? 
                    # Actually eval_relative.py has a --repair mode but we just want to run random
                    cmd = [
                        python_path, "experiments/baseline_k5/eval_relative.py",
                        "--unlearning_methods", method,
                        "--dataset_name", dataset,
                        "--base_model", model,
                        "--unlearn_ratio", str(ratio),
                        "--random_seed", str(seed),
                        "--strategies", "random"
                    ]
                    print(f"Running: {' '.join(cmd)}")
                    # We use subprocess.run and ignore errors (missing cache is fine)
                    subprocess.run(cmd, capture_output=True)

print("Batch evaluation complete.")
