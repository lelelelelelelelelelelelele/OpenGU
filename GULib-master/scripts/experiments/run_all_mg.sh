#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "H:/project/OpenGU/GULib-master" ]; then
    REPO_ROOT="H:/project/OpenGU/GULib-master"
elif [ -d "/h/project/OpenGU/GULib-master" ]; then
    REPO_ROOT="/h/project/OpenGU/GULib-master"
else
    REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi


echo "实验开始: $(date)"
echo "Running: MG-0~3 collateral completion + ratio sensitivity"
echo "=============================================="

cd "$REPO_ROOT"

echo ""
echo "[1/5] MG-0 completion + collateral (repair)"
bash "$SCRIPT_DIR/run_mg0_completion.sh" --repair --run_collateral

echo ""
echo "[2/5] MG-1 citeseer + collateral (repair)"
bash "$SCRIPT_DIR/run_mg1_citeseer.sh" --repair --run_collateral

echo ""
echo "[3/5] MG-2 gat + collateral (repair)"
bash "$SCRIPT_DIR/run_mg2_gat.sh" --repair --run_collateral

echo ""
echo "[4/5] MG-3 extended + collateral (repair)"
bash "$SCRIPT_DIR/run_mg3_extended.sh" --repair --run_collateral

echo ""
echo "[5/5] ratio sensitivity (repair)"
bash "$SCRIPT_DIR/run_ratio_sensitivity.sh" --repair --run_collateral

echo ""
echo "=============================================="
echo "实验结束: $(date)"
