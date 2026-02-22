#!/bin/bash
# Ratio 敏感性实验脚本 - 攻击强度曲线
# 运行不同 unlearn_ratio 下的攻击效果评估

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

# 参数配置
# RATIOS 从大到小：利于 cache 复用（大 ratio 先跑，后续小 ratio 可复用部分 cache）
METHODS="GIF,GNNDelete" #,GraphEraser,GUIDE
DATASETS="cora"
BASE_MODEL="GCN"
STRATEGIES="random,degree,pagerank,tracin,im,hybrid"
RATIOS="0.20,0.10,0.05,0.01"
SEEDS="42,212,722,1337,2024"
CUDA=0
OUTPUT="results/experiments/ratio_sensitivity"

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

echo "=============================================="
echo "Ratio Sensitivity Experiments"
echo "Dataset: $DATASETS / $BASE_MODEL"
echo "Methods: $METHODS"
echo "Strategies: $STRATEGIES"
echo "Ratios: $RATIOS"
echo "Seeds: $SEEDS"
echo "Output: $OUTPUT"
if [ "$REPAIR_MODE" -eq 1 ]; then
    echo "Mode: REPAIR"
fi
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo "Collateral: YES"
fi
echo "=============================================="

cd "$REPO_ROOT"

# 使用 run_experiments.py 运行批量实验
COMMON_ARGS=(
    --methods "$METHODS"
    --datasets "$DATASETS"
    --base_model "$BASE_MODEL"
    --strategies "$STRATEGIES"
    --ratios "$RATIOS"
    --seeds "$SEEDS"
    --cuda "$CUDA"
    --output "$OUTPUT"
)

if [ "$REPAIR_MODE" -eq 1 ]; then
    mkdir -p "$OUTPUT/phase_a"
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" --repair "${EXTRA_ARGS[@]}"
else
    "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" "${EXTRA_ARGS[@]}"
fi

echo ""
echo "Ratio sensitivity experiments complete!"

# 运行 collateral 评估
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo ""
    echo "=== Running Collateral Evaluation (for each ratio) ==="

    for RATIO in $(echo "$RATIOS" | tr ',' ' '); do
        echo ""
        echo ">>> Collateral for ratio: $RATIO"

        for METHOD in $(echo "$METHODS" | tr ',' ' '); do
            for SEED in $(echo "$SEEDS" | tr ',' ' '); do
                echo ">>> CollEval: $METHOD, seed: $SEED, ratio: $RATIO"

                "$PYTHON_BIN" eval_collateral.py \
                    --dataset_name "$DATASETS" \
                    --base_model "$BASE_MODEL" \
                    --unlearning_methods "$METHOD" \
                    --strategies "$STRATEGIES" \
                    --unlearn_ratio "$RATIO" \
                    --random_seed "$SEED" \
                    $REPAIR_MODE_ARG

                echo ">>> CollEval complete: $METHOD, seed: $SEED"
            done
        done
    done

    echo ""
    echo "=== Collateral Evaluation Complete ==="
fi

echo ""
echo "=============================================="
echo "All done! Results saved to: $OUTPUT"
echo "=============================================="
