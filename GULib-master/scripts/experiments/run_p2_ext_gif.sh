#!/bin/bash
# GIF Ratio 扩展实验 (P2-EXT)
# 目标：测试 GIF 在 ratio=0.10/0.20，2数据集 × 3模型 组合

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="H:/project/OpenGU/GULib-master"

if [ -x "H:/conda_package/envs/gnn/python.exe" ]; then
    PYTHON_BIN="H:/conda_package/envs/gnn/python.exe"
else
    PYTHON_BIN="python"
fi

# 实验参数
METHODS="GIF"
DATASETS="cora,citeseer"
BASE_MODELS="GCN,GAT,GIN"
STRATEGIES="random,degree,pagerank,tracin,im_v4,hybrid_v4"
RATIOS="0.10,0.20"
SEEDS="42,212,722,1337,2024"
CUDA=0

# 解析参数
REPAIR_MODE=1  # 默认启用 repair 模式
RUN_COLLATERAL=0
RUN_RELATIVE=0
DRY_RUN=0
EXTRA_ARGS=()
for arg in "$@"; do
    if [ "$arg" = "--repair" ]; then
        REPAIR_MODE=1
    elif [ "$arg" = "--run_collateral" ]; then
        RUN_COLLATERAL=1
    elif [ "$arg" = "--run_relative" ]; then
        RUN_RELATIVE=1
    elif [ "$arg" = "--dry-run" ]; then
        DRY_RUN=1
    else
        EXTRA_ARGS+=("$arg")
    fi
done

# Dry-run: 显示需要运行的实验配置（调用 repair_dry_run）
if [ "$DRY_RUN" -eq 1 ]; then
    echo "=============================================="
    echo "DRY RUN - Checking missing experiments..."
    echo "=============================================="

    cd "$REPO_ROOT"

    # 1. Main experiments dry-run
    if [ "$RUN_COLLATERAL" -eq 0 ] && [ "$RUN_RELATIVE" -eq 0 ]; then
        for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
            echo ""
            echo "=== [EXP] Checking model: $MODEL ==="

            COMMON_ARGS=(
                --methods $METHODS \
                --datasets $DATASETS \
                --base_model $MODEL \
                --strategies $STRATEGIES \
                --ratios $RATIOS \
                --seeds $SEEDS \
                --cuda $CUDA \
                --output results/experiments/p2_ext_gif_${MODEL}
            )

            "$PYTHON_BIN" run_experiments.py \
                "${COMMON_ARGS[@]}" \
                --repair \
                --repair_dry_run
        done
    fi

    # 2. Collateral dry-run
    if [ "$RUN_COLLATERAL" -eq 1 ]; then
        echo ""
        echo "=== [COLLATERAL] Checking..."

        for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
            for DATASET in $(echo "$DATASETS" | tr ',' ' '); do
                for RATIO in $(echo "$RATIOS" | tr ',' ' '); do
                    echo "--- Checking: $METHODS / $DATASET / $MODEL / r=$RATIO ---"

                    "$PYTHON_BIN" eval_collateral.py \
                        --dataset_name "$DATASET" \
                        --base_model "$MODEL" \
                        --unlearning_methods "$METHODS" \
                        --strategies "$STRATEGIES" \
                        --unlearn_ratio "$RATIO" \
                        --repair_dry_run
                done
            done
        done
    fi

    # 3. Relative dry-run
    if [ "$RUN_RELATIVE" -eq 1 ]; then
        echo ""
        echo "=== [RELATIVE] Checking..."

        for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
            for DATASET in $(echo "$DATASETS" | tr ',' ' '); do
                for RATIO in $(echo "$RATIOS" | tr ',' ' '); do
                    for SEED in $(echo "$SEEDS" | tr ',' ' '); do
                        echo "--- Checking: $METHODS / $DATASET / $MODEL / r=$RATIO / seed=$SEED ---"

                        "$PYTHON_BIN" experiments/baseline_k5/eval_relative.py \
                            --dataset_name "$DATASET" \
                            --base_model "$MODEL" \
                            --unlearning_methods "$METHODS" \
                            --strategies "$STRATEGIES" \
                            --unlearn_ratio "$RATIO" \
                            --random_seed "$SEED" \
                            --repair_dry_run
                    done
                done
            done
        done
    fi

    echo ""
    echo "=============================================="
    echo "DRY RUN complete"
    echo "=============================================="
    exit 0
fi

echo "=============================================="
echo "GIF Ratio Extension Experiment (P2-EXT)"
echo "Methods: $METHODS"
echo "Datasets: $DATASETS"
echo "Models: $BASE_MODELS"
echo "Ratios: $RATIOS"
echo "Seeds: $SEEDS"
echo "Strategies: $STRATEGIES"
echo "=============================================="

cd "$REPO_ROOT"

# 分模型运行（GCN, GAT, GIN）
for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
    echo ""
    echo "=== Running experiments for model: $MODEL ==="

    COMMON_ARGS=(
        --methods $METHODS \
        --datasets $DATASETS \
        --base_model $MODEL \
        --strategies $STRATEGIES \
        --ratios $RATIOS \
        --seeds $SEEDS \
        --cuda $CUDA \
        --output results/experiments/p2_ext_gif_${MODEL}
    )

    if [ "$REPAIR_MODE" -eq 1 ]; then
        "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" --repair "${EXTRA_ARGS[@]}"
    else
        "$PYTHON_BIN" run_experiments.py "${COMMON_ARGS[@]}" "${EXTRA_ARGS[@]}"
    fi
done

echo ""
echo "=== All experiments complete ==="

# 运行 collateral 评估 (如果指定 --run_collateral)
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    echo ""
    echo "=== Running Collateral Evaluation ==="

    for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
        for DATASET in $(echo "$DATASETS" | tr ',' ' '); do
            for RATIO in $(echo "$RATIOS" | tr ',' ' '); do
                echo ">>> CollEval: GIF / $DATASET / $MODEL / r=$RATIO"

                "$PYTHON_BIN" eval_collateral.py \
                    --dataset_name "$DATASET" \
                    --base_model "$MODEL" \
                    --unlearning_methods "$METHODS" \
                    --strategies "$STRATEGIES" \
                    --unlearn_ratio "$RATIO"
            done
        done
    done

    echo ""
    echo "=== Collateral Evaluation Complete ==="
fi

# 运行 relative 评估 (如果指定 --run_relative)
if [ "$RUN_RELATIVE" -eq 1 ]; then
    echo ""
    echo "=== Running Relative Evaluation ==="

    for MODEL in $(echo "$BASE_MODELS" | tr ',' ' '); do
        for DATASET in $(echo "$DATASETS" | tr ',' ' '); do
            for RATIO in $(echo "$RATIOS" | tr ',' ' '); do
                for SEED in $(echo "$SEEDS" | tr ',' ' '); do
                    echo ">>> Relative: GIF / $DATASET / $MODEL / r=$RATIO / seed=$SEED"

                    "$PYTHON_BIN" experiments/baseline_k5/eval_relative.py \
                        --dataset_name "$DATASET" \
                        --base_model "$MODEL" \
                        --unlearning_methods "$METHODS" \
                        --strategies "$STRATEGIES" \
                        --unlearn_ratio "$RATIO" \
                        --random_seed "$SEED"
                done
            done
        done
    done

    echo ""
    echo "=== Relative Evaluation Complete ==="
fi