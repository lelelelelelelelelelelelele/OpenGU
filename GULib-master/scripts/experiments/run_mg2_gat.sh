#!/bin/bash
# MG-2: 最小跨模型泛化 (Cora / GAT)
# 验证攻击方法在不同 GNN backbone 上的泛化能力

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "H:/project/OpenGU/GULib-master" ]; then
    REPO_ROOT="H:/project/OpenGU/GULib-master"
elif [ -d "/h/project/OpenGU/GULib-master" ]; then
    REPO_ROOT="/h/project/OpenGU/GULib-master"
else
    REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

if [ -x "H:/conda_package/envs/gnn/python.exe" ]; then
    PYTHON_BIN="H:/conda_package/envs/gnn/python.exe"
elif [ -x "/h/conda_package/envs/gnn/python.exe" ]; then
    PYTHON_BIN="/h/conda_package/envs/gnn/python.exe"
else
    PYTHON_BIN="python"
fi

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

cd "$REPO_ROOT"

# 使用 run_experiments.py
"$PYTHON_BIN" run_experiments.py \
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
