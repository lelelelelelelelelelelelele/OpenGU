#!/usr/bin/env bash
# Fill k=5 noise floor for the 4 (method, backbone) combos missing on Cora:
#   GraphRevoker × GCN     (added post dispatcher fix; not in original k=5 batch)
#   GraphRevoker × GAT     (same reason)
#   IDEA         × GCN     (original k=5 batch only ran GAT for IDEA)
#   MEGU         × GCN     (same)
#
# Outputs (per cell, idempotent — skips if file exists):
#   results/baseline/k5_random/{method}/cora/{backbone}/baseline_seed{111,333,555,777,999}_k5.json
#   results/baseline/k5_random/{method}/cora/{backbone}/baseline_averaged_k5.json
#
# Usage:
#   bash experiments/baseline_k5/fill_missing_cora.sh
#
# Override python binary if needed:
#   PYTHON=python3 bash experiments/baseline_k5/fill_missing_cora.sh
#   PYTHON=H:/conda_package/envs/gnn/python.exe bash experiments/baseline_k5/fill_missing_cora.sh
#
# Exit codes: 0 = all per-seed runs OK; non-zero = at least one cell failed.

set -u

# ---- config ----
# Try in order: $PYTHON env var, "python" on PATH, then known Windows paths.
SEEDS=(111 333 555 777 999)

resolve_python() {
    local cand attempts=()
    if [ -n "${PYTHON:-}" ]; then
        attempts+=("$PYTHON")
        if "$PYTHON" -c "import sys" >/dev/null 2>&1; then
            echo "$PYTHON"; return 0
        fi
    fi
    for cand in \
        "python" \
        "python3" \
        "H:/conda_package/envs/gnn/python.exe" \
        "/h/conda_package/envs/gnn/python.exe" \
        "/H/conda_package/envs/gnn/python.exe" \
        "/c/conda_package/envs/gnn/python.exe" \
        "C:/ProgramData/Anaconda3/envs/gnn/python.exe" \
        "/c/ProgramData/Anaconda3/envs/gnn/python.exe" \
        "$HOME/anaconda3/envs/gnn/bin/python" \
        "$HOME/miniconda3/envs/gnn/bin/python" \
        "/opt/conda/envs/gnn/bin/python"
    do
        attempts+=("$cand")
        if "$cand" -c "import sys" >/dev/null 2>&1; then
            echo "$cand"; return 0
        fi
    done
    echo "DIAG: tried (none worked):" >&2
    for a in "${attempts[@]}"; do echo "  - $a" >&2; done
    echo "DIAG: bash PATH = $PATH" >&2
    echo "DIAG: try one of:" >&2
    echo "      PYTHON=H:/conda_package/envs/gnn/python.exe bash $0" >&2
    echo "      PYTHON=python bash $0    # if 'python' resolves in your shell" >&2
    return 1
}
PY="$(resolve_python)" || { echo "ERROR: no working python found." >&2; exit 2; }
echo "[*] using python: $PY"
COMBOS=(
    "GraphRevoker GCN"
    "GraphRevoker GAT"
    "IDEA         GCN"
    "MEGU         GCN"
)
DATASET="cora"
BASELINE_K=5

# ---- locate repo root ----
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GEN_SCRIPT="$REPO_ROOT/experiments/baseline_k5/generate_baseline.py"
RUN_ALL="$REPO_ROOT/experiments/baseline_k5/run_all_baselines.py"
LOG="$REPO_ROOT/logs/fill_k5_missing_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$REPO_ROOT/logs"

if [ ! -f "$GEN_SCRIPT" ]; then
    echo "ERROR: generator script not found at $GEN_SCRIPT" >&2
    exit 2
fi

cd "$REPO_ROOT" || exit 2

echo "===== fill_missing_cora.sh  $(date) =====" | tee -a "$LOG"
echo "PY:          $PY"            | tee -a "$LOG"
echo "REPO_ROOT:   $REPO_ROOT"     | tee -a "$LOG"
echo "DATASET:     $DATASET"       | tee -a "$LOG"
echo "BASELINE_K:  $BASELINE_K"    | tee -a "$LOG"
echo "SEEDS:       ${SEEDS[*]}"    | tee -a "$LOG"
echo "COMBOS (4):"                  | tee -a "$LOG"
for c in "${COMBOS[@]}"; do echo "  $c" | tee -a "$LOG"; done
echo ""                             | tee -a "$LOG"

ok_count=0
fail_count=0
skip_count=0
total=$(( ${#COMBOS[@]} * ${#SEEDS[@]} ))
i=0

for combo in "${COMBOS[@]}"; do
    # Squash internal whitespace so "GraphRevoker         GCN" -> two tokens cleanly
    read -r method backbone <<<"$(echo "$combo" | tr -s ' ')"
    cache_dir="$REPO_ROOT/results/baseline/k5_random/$method/$DATASET/$backbone"
    mkdir -p "$cache_dir"

    echo "----- $method × $DATASET / $backbone -----" | tee -a "$LOG"
    for seed in "${SEEDS[@]}"; do
        i=$((i + 1))
        cache_file="$cache_dir/baseline_seed${seed}_k${BASELINE_K}.json"
        progress="[$i/$total]"

        if [ -f "$cache_file" ]; then
            echo "$progress [SKIP] $method/$backbone/seed=$seed (exists)" | tee -a "$LOG"
            skip_count=$((skip_count + 1))
            continue
        fi

        echo "$progress [RUN]  $method/$backbone/seed=$seed ..." | tee -a "$LOG"
        if "$PY" "$GEN_SCRIPT" \
            --dataset_name "$DATASET" \
            --base_model "$backbone" \
            --unlearning_methods "$method" \
            --random_seed "$seed" \
            --baseline_k "$BASELINE_K" >>"$LOG" 2>&1; then
            if [ -f "$cache_file" ]; then
                echo "$progress [OK]   $method/$backbone/seed=$seed" | tee -a "$LOG"
                ok_count=$((ok_count + 1))
            else
                echo "$progress [FAIL] $method/$backbone/seed=$seed (rc=0 but output missing)" | tee -a "$LOG"
                fail_count=$((fail_count + 1))
            fi
        else
            echo "$progress [FAIL] $method/$backbone/seed=$seed (see log tail below)" | tee -a "$LOG"
            tail -n 8 "$LOG" | sed 's/^/    /'
            fail_count=$((fail_count + 1))
        fi
    done
done

echo ""                                                                | tee -a "$LOG"
echo "===== per-seed phase done: ok=$ok_count skip=$skip_count fail=$fail_count =====" | tee -a "$LOG"
echo ""                                                                | tee -a "$LOG"

# ---- aggregate per-seed → baseline_averaged_k5.json (only for the 4 missing combos) ----
echo "===== aggregating into baseline_averaged_k${BASELINE_K}.json =====" | tee -a "$LOG"
"$PY" - "$DATASET" "$BASELINE_K" "${COMBOS[@]}" <<'PYEOF' | tee -a "$LOG"
"""Aggregate per-seed k=5 baseline JSONs into baseline_averaged_k{k}.json.

Reuses the canonical compute_averaged_baseline() in run_all_baselines.py
so the schema is identical to the existing files.
"""
import json, sys, os
from pathlib import Path
from datetime import datetime
import numpy as np

dataset = sys.argv[1]
baseline_k = int(sys.argv[2])
combos_raw = sys.argv[3:]

# Each combo arg arrives as a single "method backbone" string
combos = []
for c in combos_raw:
    parts = c.split()
    if len(parts) >= 2:
        combos.append((parts[0], parts[1]))

REPO = Path(os.environ.get("REPO_ROOT", os.getcwd()))
ROOT = REPO / "results" / "baseline" / "k5_random"
SEEDS = [111, 333, 555, 777, 999]

agg_ok = 0
agg_fail = 0
for method, bk in combos:
    cdir = ROOT / method / dataset / bk
    if not cdir.exists():
        print(f"  [SKIP] {method}/{dataset}/{bk}: cache dir missing")
        agg_fail += 1
        continue
    f1a, f1b, f1d, details = [], [], [], []
    for s in SEEDS:
        p = cdir / f"baseline_seed{s}_k{baseline_k}.json"
        if not p.exists():
            print(f"  [WARN] {method}/{dataset}/{bk}: missing seed={s}")
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [WARN] {method}/{dataset}/{bk}/seed={s}: read failed {e}")
            continue
        if d.get("f1_after") is not None: f1a.append(d["f1_after"])
        if d.get("f1_before") is not None: f1b.append(d["f1_before"])
        if d.get("f1_drop") is not None: f1d.append(d["f1_drop"])
        details.append({"seed": s, "f1_after": d.get("f1_after"),
                        "f1_before": d.get("f1_before"), "f1_drop": d.get("f1_drop")})
    if not f1a:
        print(f"  [ERROR] {method}/{dataset}/{bk}: zero usable seeds; skipping")
        agg_fail += 1
        continue
    avg = {
        "f1_after": float(np.mean(f1a)),
        "f1_after_std": float(np.std(f1a)),
        "f1_before": float(np.mean(f1b)) if f1b else None,
        "f1_drop": float(np.mean(f1d)) if f1d else None,
        "n_seeds": len(f1a),
        "seeds_used": [d["seed"] for d in details if d.get("f1_after") is not None],
        "per_seed_details": details,
        "config": {
            "dataset_name": dataset, "base_model": bk,
            "unlearning_methods": method, "k": baseline_k,
            "strategy": "random", "averaged": True,
            "timestamp": datetime.now().isoformat(),
        },
    }
    out = cdir / f"baseline_averaged_k{baseline_k}.json"
    out.write_text(json.dumps(avg, indent=2), encoding="utf-8")
    print(f"  [AVG] {method}/{dataset}/{bk}: f1_after={avg['f1_after']:.4f} ± {avg['f1_after_std']:.4f}  n={avg['n_seeds']}")
    agg_ok += 1

print()
print(f"aggregation: ok={agg_ok}  fail={agg_fail}")
sys.exit(0 if agg_fail == 0 else 1)
PYEOF
agg_rc=$?

echo ""                                              | tee -a "$LOG"
echo "===== ALL DONE  $(date) ====="                 | tee -a "$LOG"
echo "  per-seed: ok=$ok_count skip=$skip_count fail=$fail_count" | tee -a "$LOG"
echo "  aggregate: rc=$agg_rc"                       | tee -a "$LOG"
echo "  log: $LOG"                                   | tee -a "$LOG"

if [ $fail_count -ne 0 ] || [ $agg_rc -ne 0 ]; then
    exit 1
fi
exit 0
