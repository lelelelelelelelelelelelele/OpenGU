#!/bin/bash
set -e

# MG-0 稳定性实验补全脚本
# 需要运行 GraphEraser 和 GUIDE 在 seeds 42, 212, 722, 1337 上

# 实验参数
METHODS="GNNDelete,GIF,GraphEraser,GUIDE"
DATASETS="cora"
BASE_MODEL="GCN"
STRATEGIES="random,degree,pagerank,tracin,im,hybrid"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

echo "=============================================="
echo "MG-0 Stability Experiment Completion"
echo "Methods: $METHODS"
echo "Model: $BASE_MODEL"
echo "Seeds: $SEEDS"
echo "Strategies: $STRATEGIES"
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
    --output results/experiments/mg0_completion

echo ""
echo "=============================================="
echo "Experiment complete!"
echo "=============================================="
