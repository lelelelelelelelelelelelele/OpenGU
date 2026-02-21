#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建日志目录
mkdir -p logs

# 日志文件
LOG_FILE="logs/experiment_$(date +%Y%m%d_%H%M%S).log"

# 重定向所有输出到日志
exec > >(tee -a "$LOG_FILE") 2>&1

echo "实验开始: $(date)"
echo "Running: MG-0, MG-2, MG-3 (skipping MG-1)"
echo "=============================================="

bash "$SCRIPT_DIR/run_mg0_completion.sh"

bash "$SCRIPT_DIR/run_mg2_gat.sh"

bash "$SCRIPT_DIR/run_mg3_extended.sh"

echo "=============================================="
echo "实验结束: $(date)"
