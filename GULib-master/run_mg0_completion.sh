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

REPAIR_MODE=0
EXTRA_ARGS=()
for arg in "$@"; do
    if [ "$arg" = "--repair" ]; then
        REPAIR_MODE=1
    else
        EXTRA_ARGS+=("$arg")
    fi
done

echo "=============================================="
echo "MG-0 Stability Experiment Completion"
echo "Methods: $METHODS"
echo "Model: $BASE_MODEL"
echo "Seeds: $SEEDS"
echo "Strategies: $STRATEGIES"
if [ "$REPAIR_MODE" -eq 1 ]; then
    echo "Mode: REPAIR (in-place, auto-missing-detection)"
fi
echo "=============================================="

cd H:/project/OpenGU/GULib-master

# 基础参数（普通模式与修补模式共用）
COMMON_ARGS=(
    --methods $METHODS \
    --datasets $DATASETS \
    --base_model $BASE_MODEL \
    --strategies $STRATEGIES \
    --ratios $RATIOS \
    --seeds $SEEDS \
    --cuda $CUDA \
    --output results/experiments/mg0_completion
)

if [ "$REPAIR_MODE" -eq 1 ]; then
    H:/conda_package/envs/gnn/python.exe run_experiments.py \
        "${COMMON_ARGS[@]}" \
        --repair \
        "${EXTRA_ARGS[@]}"
else
    H:/conda_package/envs/gnn/python.exe run_experiments.py \
        "${COMMON_ARGS[@]}" \
        "${EXTRA_ARGS[@]}"
fi

echo ""
echo "=============================================="
echo "Experiment complete!"
echo "=============================================="
