#!/bin/bash
# MG-3: 扩展到 5 方法 (GIF, GNNDelete, GraphEraser, IDEA, MEGU)
# 在 MG-1 (Citeseer) 和 MG-2 (GAT) 基础上增加 IDEA 和 MEGU
# 只跑 4 策略 (random, tracin, im, hybrid) 做筛选

set -e

# ============ MG-3a: Citeseer + IDEA/MEGU ============
echo "=============================================="
echo "MG-3a: Extended Methods on Citeseer"
echo "=============================================="

cd H:/project/OpenGU/GULib-master

METHODS_IDEA="IDEA,MEGU"
DATASETS="citeseer"
BASE_MODEL="GCN"
STRATEGIES="random,tracin,im,hybrid"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

H:/conda_package/envs/gnn/python.exe run_experiments.py \
    --methods $METHODS_IDEA \
    --datasets $DATASETS \
    --base_model $BASE_MODEL \
    --strategies $STRATEGIES \
    --ratios $RATIOS \
    --seeds $SEEDS \
    --cuda $CUDA \
    --output results/experiments/mg3_citeseer

# ============ MG-3b: GAT + IDEA/MEGU ============
echo ""
echo "=============================================="
echo "MG-3b: Extended Methods on GAT"
echo "=============================================="

# run_experiments.py 现在支持 --base_model
H:/conda_package/envs/gnn/python.exe run_experiments.py \
    --methods $METHODS_IDEA \
    --datasets cora \
    --base_model GAT \
    --strategies $STRATEGIES \
    --ratios $RATIOS \
    --seeds $SEEDS \
    --cuda $CUDA \
    --output results/experiments/mg3_gat

echo ""
echo "MG-3 complete!"
