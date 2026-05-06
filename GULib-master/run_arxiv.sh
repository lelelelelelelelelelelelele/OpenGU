#!/bin/bash
# arxiv 部署脚本（用相对路径；前提：你已 cd 到 GULib-master 目录）
#
# 用法：
#   bash run_arxiv.sh                    # MODE=full（默认）：smoke + T1，~7h
#   MODE=prewarm bash run_arxiv.sh       # 只跑 TracIn prewarm 写 cache，~4h
#   后台跑：nohup bash run_arxiv.sh > /dev/null 2>&1 & disown
#   调试：SKIP_SHUTDOWN=1 bash run_arxiv.sh
#
# MODE=prewarm
#   只跑 prewarm_selection_cache.py --strategies tracin × 3 method
#   写 results/score_cache/if/ + results/selection_cache/
#   不跑 GU/MIA/retrain。完了关机。
#
# MODE=full
#   STAGE A: smoke (phase_b_arxiv_tracin_smoke.yaml, 1 cell, 限 SMOKE_TIMEOUT)
#   STAGE B: smoke 通过才进 T1 (phase_b_arxiv_T1_seed42.yaml, 18 cell)
#   smoke 失败/超时 → 立即关机不跑 T1。完了关机。

set -u
MODE="${MODE:-full}"
BRANCH="${BRANCH:-release/phase-b-fixes}"
NUMBA_NUM_THREADS="${NUMBA_NUM_THREADS:-$(nproc 2>/dev/null || echo 18)}"
SMOKE_TIMEOUT="${SMOKE_TIMEOUT:-3h}"
PREWARM_TIMEOUT="${PREWARM_TIMEOUT:-6h}"
SKIP_SHUTDOWN="${SKIP_SHUTDOWN:-0}"

LOG="run_arxiv_${MODE}_$(date +%Y%m%d_%H%M%S).log"

do_shutdown() {
    if [ "$SKIP_SHUTDOWN" = "1" ]; then
        echo "[shutdown] SKIP_SHUTDOWN=1，不关机（exit ${1:-0}）"
        exit "${1:-0}"
    fi
    /usr/bin/shutdown
    exit "${1:-0}"
}

{
    echo "===== ARXIV DEPLOY  MODE=$MODE  $(date) ====="
    echo "PWD:               $(pwd)"
    echo "BRANCH:            $BRANCH"
    echo "NUMBA_NUM_THREADS: $NUMBA_NUM_THREADS"
    echo "LOG:               $LOG"
    echo ""

    # Sync (相对路径；前提你在 GULib-master 目录里)
    git fetch origin                          || { echo "FATAL git fetch"; do_shutdown 1; }
    git checkout "$BRANCH"                    || { echo "FATAL git checkout"; do_shutdown 1; }
    git pull --ff-only origin "$BRANCH"       || echo "[warn] pull --ff-only failed, 用 HEAD"
    echo "Commit: $(git log -1 --oneline)"
    echo ""

    export NUMBA_NUM_THREADS=$NUMBA_NUM_THREADS

    case "$MODE" in
        prewarm)
            echo "=== TRACIN PREWARM (3 method × ~75 min ≈ 4h, budget=$PREWARM_TIMEOUT) ==="
            timeout "$PREWARM_TIMEOUT" python scripts/prewarm_selection_cache.py \
                experiments/configs/phase_b_arxiv_T1_seed42.yaml \
                --strategies tracin
            status=$?
            n_if=$(ls results/score_cache/if/*.npz 2>/dev/null | wc -l)
            echo ""
            echo "exit=$status   IF cache=$n_if (expected 3)"
            ;;

        full)
            echo "=== STAGE A: smoke (budget=$SMOKE_TIMEOUT) ==="
            timeout "$SMOKE_TIMEOUT" python experiments/run.py \
                experiments/configs/phase_b_arxiv_tracin_smoke.yaml
            smoke_status=$?

            smoke_cell="results/runs/ogbn-arxiv_GCN_r0.01/GIF_tracin/seed42"
            smoke_ok=1
            for f in attack.json collateral.json predictions.npz _meta.json; do
                [ -f "$smoke_cell/$f" ] || { echo "MISSING $smoke_cell/$f"; smoke_ok=0; }
            done
            echo "SMOKE exit=$smoke_status files_ok=$smoke_ok"

            if [ $smoke_status -ne 0 ] || [ $smoke_ok -ne 1 ]; then
                echo "=== SMOKE FAILED $(date) — 关机不跑 T1 ==="
                do_shutdown "$smoke_status"
            fi

            echo ""
            echo "=== STAGE B: T1 (18 cells) ==="
            python experiments/run.py \
                experiments/configs/phase_b_arxiv_T1_seed42.yaml
            status=$?
            cells=$(ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed42/attack.json 2>/dev/null | wc -l)
            echo ""
            echo "T1 exit=$status   cells_complete=$cells/18"
            ;;

        *)
            echo "FATAL: unknown MODE=$MODE (use 'prewarm' or 'full')"
            do_shutdown 1
            ;;
    esac

    echo ""
    echo "===== ALL DONE  $(date) ====="
    do_shutdown "${status:-0}"

} > "$LOG" 2>&1
