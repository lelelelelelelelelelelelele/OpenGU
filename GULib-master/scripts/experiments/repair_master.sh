#!/bin/bash
# Master Repair Script: Fixing GNNDelete Corruption & Completing GIF P2-EXT
# Target: MG-1, MG-2, P2-EXT

REPO_ROOT="H:/project/OpenGU/GULib-master"
PYTHON_BIN="H:/conda_package/envs/gnn/python.exe"
export PYTHONPATH="$PYTHONPATH;$REPO_ROOT/scripts/evaluation"

cd "$REPO_ROOT"

echo "=========================================================="
echo "PHASE 1: Re-running GNNDelete (MG-1 & MG-2) Main Experiments"
echo "Reason: Previous results were corrupted by AssertionError"
echo "=========================================================="

# 1.1 MG-1: Citeseer / GCN
echo ">>> Running GNNDelete MG-1 (Citeseer/GCN)..."
"$PYTHON_BIN" demo_attack.py --methods GNNDelete --datasets citeseer --base_model GCN --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --ratios 0.05 --seeds 42,212,722,1337,2024 --no_cache

# 1.2 MG-2: Cora / GAT
echo ">>> Running GNNDelete MG-2 (Cora/GAT)..."
"$PYTHON_BIN" demo_attack.py --methods GNNDelete --datasets cora --base_model GAT --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --ratios 0.05 --seeds 42,212,722,1337,2024 --no_cache

echo "=========================================================="
echo "PHASE 2: Filling Evaluation Gaps (Relative & Collateral)"
echo "Targeting: GNNDelete (MG-1/2) and GIF (P2-EXT)"
echo "=========================================================="

# 2.1 GIF P2-EXT Evaluations
echo ">>> Filling GIF P2-EXT Gaps (Relative)..."
bash scripts/experiments/run_p2_ext_gif.sh --run_relative

echo ">>> Filling GIF P2-EXT Gaps (Collateral)..."
bash scripts/experiments/run_p2_ext_gif.sh --run_collateral

# 2.2 GNNDelete Evaluation Completion
echo ">>> Filling GNNDelete MG-1/2 Gaps (Relative)..."
for DS in citeseer cora; do
    MOD="GCN"
    if [ "$DS" == "cora" ]; then MOD="GAT"; fi
    for SEED in 42 212 722 1337 2024; do
        "$PYTHON_BIN" experiments/baseline_k5/eval_relative.py --unlearning_methods GNNDelete --dataset_name "$DS" --base_model "$MOD" --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --unlearn_ratio 0.05 --random_seed "$SEED" --repair
    done
done

echo ">>> Filling GNNDelete MG-1/2 Gaps (Collateral)..."
for DS in citeseer cora; do
    MOD="GCN"
    if [ "$DS" == "cora" ]; then MOD="GAT"; fi
    "$PYTHON_BIN" eval_collateral.py --unlearning_methods GNNDelete --dataset_name "$DS" --base_model "$MOD" --unlearn_ratio 0.05 --repair
done

echo "=========================================================="
echo "PHASE 3: Final Data Aggregation & Reporting"
echo "=========================================================="
"$PYTHON_BIN" scripts/evaluation/final_data_aggregator.py
"$PYTHON_BIN" scripts/evaluation/gen_md_report_v2.py

echo "Master Repair Complete. Check report/paper/sections/cross_seed_tables.md"
