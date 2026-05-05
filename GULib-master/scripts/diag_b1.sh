#!/bin/bash
# 快速看 B.1 状态。用法: bash scripts/diag_b1.sh [cell_dir]
CELL="${1:-ogbn-arxiv_GCN_r0.05}"
RUNS="results/runs/$CELL"

echo "=== attack.json ==="
ls -la $RUNS/*/seed*/attack.json 2>/dev/null

echo ""
echo "=== collateral.json ==="
ls -la $RUNS/*/seed*/collateral.json 2>/dev/null

echo ""
echo "=== predictions.npz ==="
ls -la $RUNS/*/seed*/predictions.npz 2>/dev/null

echo ""
echo "=== errors in /tmp/log.txt ==="
grep -iE "OutOfMemory|FAIL|Error during" /tmp/log.txt 2>/dev/null | tail -10
