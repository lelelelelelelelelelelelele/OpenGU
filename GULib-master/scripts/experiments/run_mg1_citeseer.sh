#!/bin/bash
# MG-1: 最小跨数据集泛化 (Citeseer / GCN)
# 验证攻击方法在不同数据集上的泛化能力

set -e

METHODS="GIF,GNNDelete,GraphEraser"
DATASETS="citeseer"
BASE_MODEL="GCN"
STRATEGIES="random,degree,pagerank,tracin,im,hybrid"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

echo "=============================================="
echo "MG-1: Cross-Dataset Generalization"
echo "Dataset: Citeseer / GCN"
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
    --output results/experiments/mg1_citeseer

echo ""
echo "MG-1 complete!"
