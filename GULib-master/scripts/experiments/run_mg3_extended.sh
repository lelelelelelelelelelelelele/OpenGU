#!/bin/bash
# MG-3: 扩展到 5 方法 (GIF, GNNDelete, GraphEraser, IDEA, MEGU)
# 在 MG-1 (Citeseer) 和 MG-2 (GAT) 基础上增加 IDEA 和 MEGU
# 只跑 4 策略 (random, tracin, im, hybrid) 做筛选

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

# 参数解析
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

if [ "$REPAIR_MODE" -eq 1 ]; then
    REPAIR_MODE_ARG="--repair"
fi

# ============ MG-3a: Citeseer + IDEA/MEGU ============
echo "=============================================="
echo "MG-3a: Extended Methods on Citeseer"
if [ "$REPAIR_MODE" -eq 1 ]; then
    echo "Mode: REPAIR"
fi
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo "Collateral: YES"
fi
echo "=============================================="

cd "$REPO_ROOT"

METHODS_IDEA="IDEA,MEGU"
DATASETS="citeseer"
BASE_MODEL="GCN"
STRATEGIES="random,tracin,im,hybrid"
RATIOS="0.05"
SEEDS="42,212,722,1337,2024"
CUDA=0

COMMON_ARGS=(
    --methods $METHODS_IDEA
    --datasets $DATASETS
    --base_model $BASE_MODEL
    --strategies $STRATEGIES
    --ratios $RATIOS
    --seeds $SEEDS
    --cuda $CUDA
    --output results/experiments/mg3_citeseer
)

if [ "$REPAIR_MODE" -eq 1 ]; then
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" --repair "${EXTRA_ARGS[@]}"
else
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" "${EXTRA_ARGS[@]}"
fi

# MG-3a collateral 评估
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo ""
    echo "=== MG-3a Collateral Evaluation ==="
    for METHOD in $(echo "$METHODS_IDEA" | tr ',' ' '); do
        for SEED in $(echo "$SEEDS" | tr ',' ' '); do
            echo ">>> CollEval: $METHOD, seed: $SEED"
            "$PYTHON_BIN" eval_collateral.py \
                --dataset_name "$DATASETS" \
                --base_model "$BASE_MODEL" \
                --unlearning_methods "$METHOD" \
                --strategies "$STRATEGIES" \
                --unlearn_ratio "$RATIOS" \
                --random_seed "$SEED" \
                $REPAIR_MODE_ARG
            echo ">>> CollEval complete: $METHOD, seed: $SEED"
        done
    done
fi

# ============ MG-3b: GAT + IDEA/MEGU ============
echo ""
echo "=============================================="
echo "MG-3b: Extended Methods on GAT"
echo "=============================================="

COMMON_ARGS_B=(
    --methods $METHODS_IDEA
    --datasets cora
    --base_model GAT
    --strategies $STRATEGIES
    --ratios $RATIOS
    --seeds $SEEDS
    --cuda $CUDA
    --output results/experiments/mg3_gat
)

if [ "$REPAIR_MODE" -eq 1 ]; then
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS_B[@]}" --repair "${EXTRA_ARGS[@]}"
else
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS_B[@]}" "${EXTRA_ARGS[@]}"
fi

# MG-3b collateral 评估
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo ""
    echo "=== MG-3b Collateral Evaluation ==="
    for METHOD in $(echo "$METHODS_IDEA" | tr ',' ' '); do
        for SEED in $(echo "$SEEDS" | tr ',' ' '); do
            echo ">>> CollEval: $METHOD, seed: $SEED"
            "$PYTHON_BIN" eval_collateral.py \
                --dataset_name "cora" \
                --base_model "GAT" \
                --unlearning_methods "$METHOD" \
                --strategies "$STRATEGIES" \
                --unlearn_ratio "$RATIOS" \
                --random_seed "$SEED" \
                $REPAIR_MODE_ARG
            echo ">>> CollEval complete: $METHOD, seed: $SEED"
        done
    done
fi

echo ""
echo "MG-3 complete!"
