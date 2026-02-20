#!/bin/bash
# MG-2: 最小跨模型泛化 (Cora / GAT)
# 验证攻击方法在不同 GNN backbone 上的泛化能力

set -e

METHODS="GIF,GNNDelete,GraphEraser"
DATASETS="cora"
BASE_MODEL="GAT"
STRATEGIES="random,degree,pagerank,tracin,im,hybrid"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

echo "=============================================="
echo "MG-2: Cross-Model Generalization"
echo "Dataset: Cora / GAT"
echo "Methods: $METHODS"
echo "Seeds: $SEEDS"
echo "=============================================="

cd H:/project/OpenGU/GULib-master

# 使用 run_experiments.py
H:/conda_package/envs/gnn/python.exe run_experiments.py \
    --methods $METHODS \
    --datasets $DATASETS \
    --base_model $BASE_MODEL \
    --strategies $STRATEGIES \
    --ratios $RATIOS \
    --seeds $SEEDS \
    --cuda $CUDA \
    --output results/experiments/mg2_gat

echo ""
echo "MG-2 complete!"
