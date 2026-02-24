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

TOTAL_STEPS=5
SECONDS=0

run_step() {
    local idx="$1"
    local title="$2"
    shift 2
    local step_start=$SECONDS
    local started_at
    started_at="$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "[START ${idx}/${TOTAL_STEPS}] ${title} @ ${started_at}"
    "$@"
    local elapsed=$((SECONDS - step_start))
    echo "[DONE  ${idx}/${TOTAL_STEPS}] ${title} (elapsed: ${elapsed}s)"
}

run_step 1 "MG-0 completion + collateral (repair)" \
    bash "$SCRIPT_DIR/run_mg0_completion.sh" --repair --run_collateral

run_step 2 "MG-1 citeseer + collateral (repair)" \
    bash "$SCRIPT_DIR/run_mg1_citeseer.sh" --repair --run_collateral

run_step 3 "MG-2 gat + collateral (repair)" \
    bash "$SCRIPT_DIR/run_mg2_gat.sh" --repair --run_collateral

run_step 4 "MG-3 extended + collateral (repair)" \
    bash "$SCRIPT_DIR/run_mg3_extended.sh" --repair --run_collateral

run_step 5 "ratio sensitivity (repair)" \
    bash "$SCRIPT_DIR/run_ratio_sensitivity.sh" --repair --run_collateral

echo ""
echo "=============================================="
echo "总耗时: ${SECONDS}s"
echo "实验结束: $(date)"
