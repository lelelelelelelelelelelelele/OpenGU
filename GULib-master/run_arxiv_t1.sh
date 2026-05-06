#!/bin/bash
# arxiv T1 一键部署脚本：smoke gate → full T1 → 自动关机
#
# 用法（在 A800 实例 ssh 进去后）：
#   cd /root/autodl-fs/OpenGU/GULib-master   # 你实际项目路径
#   nohup bash run_arxiv_t1.sh > /dev/null 2>&1 &
#   disown
#   exit                                       # 安全断开 ssh
#
# 行为：
#   1. git fetch + checkout release/phase-b-fixes + pull
#   2. STAGE A: 跑 phase_b_arxiv_tracin_smoke.yaml（GIF/tracin/seed42 单 cell）
#      - 限时 SMOKE_TIMEOUT（默认 3h，预期 ~90 min）
#      - 失败 / 超时 / 4 个产物文件不齐 → 立即关机
#   3. STAGE B: 跑 phase_b_arxiv_T1_seed42.yaml（18 cell 主矩阵）
#      - smoke 已 cover GIF/tracin cell，T1 自动跳过该 cell（_meta.json fingerprint）
#      - 不限时（预期 ~6-7h，含 GND/GE 的 TracIn ~2.5h + 全 GU/MIA/retrain ~4h）
#   4. 不管成功失败，最后都关机
#
# 环境变量覆盖（按需）：
#   PROJECT_DIR=/root/...           项目路径
#   SMOKE_TIMEOUT=3h                smoke 超时（默认 3h）
#   NUMBA_NUM_THREADS=14            numba 并行线程数（默认 14，A800 实例 14 核）
#   BRANCH=release/phase-b-fixes    部署分支
#   SKIP_SHUTDOWN=1                 设为 1 跳过关机（调试用）

set -u   # 未定义变量报错；不用 set -e（要保留 status 流程）

PROJECT_DIR="${PROJECT_DIR:-/autodl-fs/data/OpenGU/GULib-master}"
SMOKE_TIMEOUT="${SMOKE_TIMEOUT:-3h}"
# Auto-detect cores; fall back to 18 if nproc unavailable
NUMBA_NUM_THREADS="${NUMBA_NUM_THREADS:-$(nproc 2>/dev/null || echo 18)}"
BRANCH="${BRANCH:-release/phase-b-fixes}"
SKIP_SHUTDOWN="${SKIP_SHUTDOWN:-0}"

LOG="run_arxiv_t1_$(date +%Y%m%d_%H%M%S).log"

# 关机封装（debug 模式可跳过）
do_shutdown() {
    if [ "$SKIP_SHUTDOWN" = "1" ]; then
        echo "[shutdown] SKIP_SHUTDOWN=1 设置，不关机（exit code: ${1:-0}）"
        exit "${1:-0}"
    fi
    echo "[shutdown] 调用 /usr/bin/shutdown ..."
    /usr/bin/shutdown
    exit "${1:-0}"
}

cd "$PROJECT_DIR" || { echo "FATAL: cannot cd to $PROJECT_DIR"; do_shutdown 1; }

{
    echo "============================================================"
    echo "ARXIV T1 DEPLOY  $(date)"
    echo "============================================================"
    echo "PROJECT_DIR        = $PROJECT_DIR"
    echo "BRANCH             = $BRANCH"
    echo "SMOKE_TIMEOUT      = $SMOKE_TIMEOUT"
    echo "NUMBA_NUM_THREADS  = $NUMBA_NUM_THREADS"
    echo "SKIP_SHUTDOWN      = $SKIP_SHUTDOWN"
    echo "LOG                = $LOG"
    echo ""

    # ============ Sync ============
    echo "=== SYNC: git fetch + checkout $BRANCH ==="
    git fetch origin                                          || { echo "FATAL: git fetch failed";  do_shutdown 1; }
    git checkout "$BRANCH"                                    || { echo "FATAL: git checkout failed"; do_shutdown 1; }
    git pull --ff-only origin "$BRANCH"                       || echo "[warn] git pull --ff-only failed (本地有 commit?), 用 HEAD 继续"
    echo "Branch: $(git branch --show-current)"
    echo "Commit: $(git log -1 --oneline)"
    echo ""

    export NUMBA_NUM_THREADS=$NUMBA_NUM_THREADS

    # ============ STAGE A: smoke ============
    echo "============================================================"
    echo "STAGE A: TracIn smoke  (budget=$SMOKE_TIMEOUT)"
    echo "============================================================"
    echo "Started at $(date)"

    timeout "$SMOKE_TIMEOUT" python experiments/run.py \
        experiments/configs/phase_b_arxiv_tracin_smoke.yaml
    smoke_status=$?

    echo ""
    echo "SMOKE exit code: $smoke_status   (0=pass, 124=timeout, other=python error)"
    echo "Finished at $(date)"

    # 验证 smoke 产物完整性
    smoke_cell="results/runs/ogbn-arxiv_GCN_r0.01/GIF_tracin/seed42"
    smoke_files_ok=1
    for f in attack.json collateral.json predictions.npz _meta.json; do
        if [ ! -f "$smoke_cell/$f" ]; then
            echo "[validate] MISSING: $smoke_cell/$f"
            smoke_files_ok=0
        fi
    done

    if [ $smoke_status -ne 0 ] || [ $smoke_files_ok -ne 1 ]; then
        echo ""
        echo "============================================================"
        echo "SMOKE FAILED  $(date)"
        echo "============================================================"
        echo "原因：smoke_status=$smoke_status, smoke_files_ok=$smoke_files_ok"
        echo "smoke cell dir 内容："
        ls -la "$smoke_cell/" 2>&1 || true
        echo ""
        echo "不跑 STAGE B，直接关机。看 $LOG 排查。"
        do_shutdown "$smoke_status"
    fi

    echo ""
    echo "============================================================"
    echo "SMOKE PASSED  $(date)"
    echo "============================================================"
    echo "smoke 产物齐全。Stage B 继续。"
    echo ""

    # ============ STAGE B: full T1 ============
    echo "============================================================"
    echo "STAGE B: T1 main matrix (18 cells)"
    echo "============================================================"
    echo "Started at $(date)"

    python experiments/run.py \
        experiments/configs/phase_b_arxiv_T1_seed42.yaml
    t1_status=$?

    echo ""
    echo "T1 exit code: $t1_status"
    echo "Finished at $(date)"

    # 进度计数
    cells_complete=$(ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed42/attack.json 2>/dev/null | wc -l)
    cells_with_npz=$(ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed42/predictions.npz 2>/dev/null | wc -l)
    echo "T1 produced $cells_complete / 18 cells with attack.json"
    echo "             $cells_with_npz / 18 cells with predictions.npz (full)"

    echo ""
    echo "============================================================"
    echo "ALL DONE  $(date)"
    echo "============================================================"

    do_shutdown "$t1_status"

} > "$LOG" 2>&1
