#!/bin/bash
# MG-1: 最小跨数据集泛化 (Citeseer / GCN)
# 验证攻击方法在不同数据集上的泛化能力

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
DATASETS="citeseer"
BASE_MODEL="GCN"
STRATEGIES="random,degree,pagerank,tracin,im_v4,hybrid_v4"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

REPAIR_MODE=0
RUN_COLLATERAL=0
REPAIR_MODE_ARG=""
EXTRA_ARGS=()
for arg in "$@"; do
    if [ "$arg" = "--repair" ]; then
        REPAIR_MODE=1
    elif [ "$arg" = "--run_collateral" ]; then
        RUN_COLLATERAL=1
    else
        EXTRA_ARGS+=("$arg")
    fi
done

echo "=============================================="
echo "MG-1: Cross-Dataset Generalization"
echo "Dataset: Citeseer / GCN"
echo "Methods: $METHODS"
echo "Seeds: $SEEDS"
if [ "$REPAIR_MODE" -eq 1 ]; then
    echo "Mode: REPAIR"
fi
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo "Collateral: YES"
fi
echo "=============================================="

cd "$REPO_ROOT"

STAGE_TOTAL=1
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    STAGE_TOTAL=2
fi
echo "[Stage 1/${STAGE_TOTAL}] Running attack batch (run_experiments.py)"

# 构建命令参数
COMMON_ARGS=(
    --methods $METHODS
    --datasets $DATASETS
    --base_model $BASE_MODEL
    --strategies $STRATEGIES
    --ratios $RATIOS
    --seeds $SEEDS
    --cuda $CUDA
    --output results/experiments/mg1_citeseer
)

if [ "$REPAIR_MODE" -eq 1 ]; then
    REPAIR_MODE_ARG="--repair"
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" --repair "${EXTRA_ARGS[@]}"
else
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" "${EXTRA_ARGS[@]}"
fi

echo ""
echo "MG-1 experiment complete!"

# 运行 collateral 评估
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo ""
    echo "=== Running Collateral Evaluation ==="

    METHOD_LIST=($(echo "$METHODS" | tr ',' ' '))
    SEED_LIST=($(echo "$SEEDS" | tr ',' ' '))
    TOTAL_COLLEVAL=$(( ${#METHOD_LIST[@]} * ${#SEED_LIST[@]} ))
    COLLEVAL_IDX=0

    for METHOD in "${METHOD_LIST[@]}"; do
        for SEED in "${SEED_LIST[@]}"; do
            COLLEVAL_IDX=$((COLLEVAL_IDX + 1))
            echo ""
            echo ">>> [${COLLEVAL_IDX}/${TOTAL_COLLEVAL}] CollEval: $METHOD, seed: $SEED"

            "$PYTHON_BIN" eval_collateral.py \
                --dataset_name "$DATASETS" \
                --base_model "$BASE_MODEL" \
                --unlearning_methods "$METHOD" \
                --strategies "$STRATEGIES" \
                --unlearn_ratio "$RATIOS" \
                --random_seed "$SEED" \
                $REPAIR_MODE_ARG

            echo ">>> [${COLLEVAL_IDX}/${TOTAL_COLLEVAL}] CollEval complete: $METHOD, seed: $SEED"
        done
    done

    echo ""
    echo "=== Collateral Evaluation Complete ==="
fi

echo ""
echo "MG-1 complete!"
