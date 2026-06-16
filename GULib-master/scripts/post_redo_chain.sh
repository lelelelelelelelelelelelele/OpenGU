#!/bin/bash
# Post-redo chain: redo(skip) → A.5 ratio sweep → A.3 alpha sweep → gate → ship → shutdown
# Usage: nohup bash scripts/post_redo_chain.sh > logs/chain_$(date +%Y%m%d_%H%M).log 2>&1 &
set -e

# Fix: disable numba multi-threading to avoid TBB/workqueue hangs on small datasets
export NUMBA_NUM_THREADS=1

cd ~/autodl-fs/OpenGU/GULib-master
mkdir -p logs

TS=$(date +%Y%m%d_%H%M)
LOG="logs/post_redo_chain_${TS}.log"
exec > >(tee -a "$LOG") 2>&1

echo "[$(date)] Chain start on $(hostname)"
echo "[$(date)] Git: $(git rev-parse --short HEAD)"

# ── Step 1: redo GCN + GAT (will skip if already complete) ──
echo ""
echo "=== Step 1: redo GCN ==="
python -u experiments/run.py experiments/configs/phase_b_cora_gcn.yaml

echo ""
echo "=== Step 2: redo GAT ==="
python -u experiments/run.py experiments/configs/phase_b_cora_gat.yaml

# ── Step 3: A.5 ratio sweep (r=0.01 → 0.10 → 0.20) ──
echo ""
echo "=== Step 3: A.5 ratio sweep ==="
# NOTE: GraphEraser/GraphRevoker dropped from r=0.20 to avoid shard imbalance.
# If you want them back, manually edit A5_ratio_0.20.yaml and re-run.
for yaml in \
    experiments/configs/A5_ratio_0.01.yaml \
    experiments/configs/A5_ratio_0.10.yaml \
    experiments/configs/A5_ratio_0.20.yaml; do
    echo "[$(date)] Running $yaml"
    python -u experiments/run.py "$yaml"
done

# ── Step 4: A.3 alpha sweep (8 yaml, ~1h) ──
echo ""
echo "=== Step 4: A.3 alpha sweep ==="
for yaml in \
    experiments/configs/A3_cora_GCN_alpha0.00.yaml \
    experiments/configs/A3_cora_GCN_alpha0.25.yaml \
    experiments/configs/A3_cora_GCN_alpha0.75.yaml \
    experiments/configs/A3_cora_GCN_alpha1.00.yaml \
    experiments/configs/A3_cora_GAT_alpha0.00.yaml \
    experiments/configs/A3_cora_GAT_alpha0.25.yaml \
    experiments/configs/A3_cora_GAT_alpha0.75.yaml \
    experiments/configs/A3_cora_GAT_alpha1.00.yaml; do
    echo "[$(date)] Running $yaml"
    python -u experiments/run.py "$yaml"
done

# ── Step 5: gate ──
echo ""
echo "=== Step 5: gate ==="
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml

# ── Step 6: ship (json + meta only, no npz) ──
echo ""
echo "=== Step 6: ship ==="
SHIP="cora_ship_${TS}.tar.gz"
find results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05 \
     results/runs/cora_GCN_r0.01 results/runs/cora_GCN_r0.10 results/runs/cora_GCN_r0.20 \
     -type f \( -name '*.json' -o -name '_meta.json' \) 2>/dev/null \
     | tar czf "$SHIP" -T -
ls -lh "$SHIP"
md5sum "$SHIP" | tee "${SHIP}.md5"

# ── Step 7: shutdown ──
echo ""
echo "[$(date)] ALL DONE. Shutting down in 60 seconds..."
sleep 60
poweroff || halt || echo "[warn] poweroff failed — stop instance manually from autodl console"
