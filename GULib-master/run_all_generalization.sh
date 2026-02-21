#!/bin/bash
# 运行所有泛化实验的汇总脚本

set -e

echo "=============================================="
echo "Running All Generalization Experiments"
echo "=============================================="

cd H:/project/OpenGU/GULib-master

# MG-0: 补全 GraphEraser + GUIDE (5 seeds x 6 strategies x 2 methods = 60 runs)
echo ""
echo "[1/4] MG-0: Stability (completion)"
bash run_mg0_completion.sh

# MG-1: Citeseer 跨数据集 (5 seeds x 6 strategies x 3 methods = 90 runs)
echo ""
echo "[2/4] MG-1: Cross-Dataset (Citeseer)"
bash run_mg1_citeseer.sh

# MG-2: GAT 跨模型 (5 seeds x 6 strategies x 3 methods = 90 runs)
echo ""
echo "[3/4] MG-2: Cross-Model (GAT)"
bash run_mg2_gat.sh

# MG-3: IDEA + MEGU 扩展 (5 seeds x 4 strategies x 2 methods x 2 configs = 80 runs)
echo ""
echo "[4/4] MG-3: Extended Methods"
bash run_mg3_extended.sh

echo ""
echo "=============================================="
echo "All experiments complete!"
echo "=============================================="
