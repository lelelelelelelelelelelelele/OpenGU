#!/bin/bash
# MG-3: 扩展到 5 方法 (GIF, GNNDelete, GraphEraser, IDEA, MEGU)
# 在 MG-1 (Citeseer) 和 MG-2 (GAT) 基础上增加 IDEA 和 MEGU
# 只跑 4 策略 (random, tracin, im_v4, hybrid_v4) 做筛选

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
STRATEGIES="random,tracin,im_v4,hybrid_v4"
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
    METHOD_LIST_A=($(echo "$METHODS_IDEA" | tr ',' ' '))
    SEED_LIST_A=($(echo "$SEEDS" | tr ',' ' '))
    TOTAL_COLLEVAL_A=$(( ${#METHOD_LIST_A[@]} * ${#SEED_LIST_A[@]} ))
    COLLEVAL_IDX_A=0
    for METHOD in "${METHOD_LIST_A[@]}"; do
        for SEED in "${SEED_LIST_A[@]}"; do
            COLLEVAL_IDX_A=$((COLLEVAL_IDX_A + 1))
            echo ">>> [EXP ${COLLEVAL_IDX_A}/${TOTAL_COLLEVAL_A}] CollEval: $METHOD, seed: $SEED"
            "$PYTHON_BIN" eval_collateral.py \
                --dataset_name "$DATASETS" \
                --base_model "$BASE_MODEL" \
                --unlearning_methods "$METHOD" \
                --strategies "$STRATEGIES" \
                --unlearn_ratio "$RATIOS" \
                --random_seed "$SEED" \
                $REPAIR_MODE_ARG
            echo ">>> [EXP ${COLLEVAL_IDX_A}/${TOTAL_COLLEVAL_A}] CollEval complete: $METHOD, seed: $SEED"
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
    METHOD_LIST_B=($(echo "$METHODS_IDEA" | tr ',' ' '))
    SEED_LIST_B=($(echo "$SEEDS" | tr ',' ' '))
    TOTAL_COLLEVAL_B=$(( ${#METHOD_LIST_B[@]} * ${#SEED_LIST_B[@]} ))
    COLLEVAL_IDX_B=0
    for METHOD in "${METHOD_LIST_B[@]}"; do
        for SEED in "${SEED_LIST_B[@]}"; do
            COLLEVAL_IDX_B=$((COLLEVAL_IDX_B + 1))
            echo ">>> [EXP ${COLLEVAL_IDX_B}/${TOTAL_COLLEVAL_B}] CollEval: $METHOD, seed: $SEED"
            "$PYTHON_BIN" eval_collateral.py \
                --dataset_name "cora" \
                --base_model "GAT" \
                --unlearning_methods "$METHOD" \
                --strategies "$STRATEGIES" \
                --unlearn_ratio "$RATIOS" \
                --random_seed "$SEED" \
                $REPAIR_MODE_ARG
            echo ">>> [EXP ${COLLEVAL_IDX_B}/${TOTAL_COLLEVAL_B}] CollEval complete: $METHOD, seed: $SEED"
        done
    done
fi

echo ""
echo "MG-3 complete!"
