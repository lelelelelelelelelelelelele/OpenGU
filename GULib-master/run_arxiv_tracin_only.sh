#!/bin/bash
# arxiv TracIn prewarm 单跑脚本：只跑 selection（不做 GU/MIA/retrain），完了关机
#
# 用途：晚上跑 TracIn × 3 method（GIF/GNNDelete/GraphEraser）的 IF 选择 cache，
# 第二天 T1 主矩阵直接 cache hit 跳过 selection，只跑 GU+MIA+retrain（~3-4h）。
#
# 跑完产物：
#   results/score_cache/if/<key>.npz × 3        (IF 分数，per method)
#   results/selection_cache/<key>.json × 3      (TracIn 选出的 top-k 节点列表)
#
# 用法（A800 ssh 进去）：
#   cd /autodl-fs/data/OpenGU/GULib-master   # pwd 确认
#   nohup bash run_arxiv_tracin_only.sh > /dev/null 2>&1 &
#   disown
#   exit
#
# 调参（可选环境变量）：
#   PROJECT_DIR             项目路径（默认 /autodl-fs/data/OpenGU/GULib-master）
#   PREWARM_TIMEOUT         强制超时（默认 6h；预期 ~3.5-4h）
#   NUMBA_NUM_THREADS       numba 线程（默认 18，匹配 NVLink 实例的 18 核）
#   BRANCH                  分支（默认 release/phase-b-fixes）
#   SKIP_SHUTDOWN=1         调试不关机

set -u

PROJECT_DIR="${PROJECT_DIR:-/autodl-fs/data/OpenGU/GULib-master}"
PREWARM_TIMEOUT="${PREWARM_TIMEOUT:-6h}"
NUMBA_NUM_THREADS="${NUMBA_NUM_THREADS:-18}"
BRANCH="${BRANCH:-release/phase-b-fixes}"
SKIP_SHUTDOWN="${SKIP_SHUTDOWN:-0}"

LOG="run_arxiv_tracin_only_$(date +%Y%m%d_%H%M%S).log"

do_shutdown() {
    if [ "$SKIP_SHUTDOWN" = "1" ]; then
        echo "[shutdown] SKIP_SHUTDOWN=1，不关机（exit ${1:-0}）"
        exit "${1:-0}"
    fi
    echo "[shutdown] 调用 /usr/bin/shutdown ..."
    /usr/bin/shutdown
    exit "${1:-0}"
}

cd "$PROJECT_DIR" || { echo "FATAL: cannot cd to $PROJECT_DIR"; do_shutdown 1; }

{
    echo "============================================================"
    echo "ARXIV TRACIN PREWARM ONLY  $(date)"
    echo "============================================================"
    echo "PROJECT_DIR        = $PROJECT_DIR"
    echo "BRANCH             = $BRANCH"
    echo "PREWARM_TIMEOUT    = $PREWARM_TIMEOUT"
    echo "NUMBA_NUM_THREADS  = $NUMBA_NUM_THREADS"
    echo "SKIP_SHUTDOWN      = $SKIP_SHUTDOWN"
    echo "LOG                = $LOG"
    echo ""

    # ============ Sync ============
    echo "=== SYNC: git fetch + checkout $BRANCH ==="
    git fetch origin                              || { echo "FATAL: git fetch failed";    do_shutdown 1; }
    git checkout "$BRANCH"                        || { echo "FATAL: git checkout failed"; do_shutdown 1; }
    git pull --ff-only origin "$BRANCH"           || echo "[warn] git pull --ff-only failed (本地有 commit?), 用 HEAD 继续"
    echo "Branch: $(git branch --show-current)"
    echo "Commit: $(git log -1 --oneline)"
    echo ""

    export NUMBA_NUM_THREADS=$NUMBA_NUM_THREADS

    # ============ TracIn prewarm ============
    echo "============================================================"
    echo "TRACIN PREWARM  (3 method × ~75 min ≈ 3.5-4h, budget=$PREWARM_TIMEOUT)"
    echo "============================================================"
    echo "Started at $(date)"
    echo ""
    echo "method-loop ON: prewarm 会按 yaml 的 methods 顺序跑"
    echo "  1. GIF        ~75 min   (chunked TracIn forward + 13.5K backprops)"
    echo "  2. GNNDelete  ~75 min"
    echo "  3. GraphEraser ~75 min"
    echo ""

    timeout "$PREWARM_TIMEOUT" python scripts/prewarm_selection_cache.py \
        experiments/configs/phase_b_arxiv_T1_seed42.yaml \
        --strategies tracin
    status=$?

    echo ""
    echo "PREWARM exit code: $status   (0=pass, 124=timeout, other=python error)"
    echo "Finished at $(date)"
    echo ""

    # ============ 产物校验 ============
    echo "=== PRODUCT CHECK ==="
    n_if=$(ls results/score_cache/if/*.npz 2>/dev/null | wc -l)
    n_sel=$(ls results/selection_cache/*.json 2>/dev/null | wc -l)
    echo "IF score cache files (results/score_cache/if/*.npz):  $n_if"
    echo "Selection cache files (results/selection_cache/*.json): $n_sel"
    echo ""
    echo "expected: ≥3 IF cache .npz (一个 method 一个), ≥3 selection cache .json"
    echo ""
    echo "ls results/score_cache/if/:"
    ls -la results/score_cache/if/ 2>&1 | tail -10 || true
    echo ""

    if [ $status -ne 0 ]; then
        echo "============================================================"
        echo "PREWARM FAILED  $(date)"
        echo "============================================================"
        echo "exit_code=$status"
        echo "查 $LOG 末尾看 traceback"
    elif [ "$n_if" -lt 3 ]; then
        echo "============================================================"
        echo "PREWARM PARTIAL  $(date)"
        echo "============================================================"
        echo "IF cache 只有 $n_if 个（< 3），可能某 method 中途挂了"
        status=2
    else
        echo "============================================================"
        echo "PREWARM ALL DONE  $(date)"
        echo "============================================================"
        echo "明天 T1 主矩阵 selection 全 cache hit，~3-4h 出全 18 cell。"
        echo ""
        echo "明天部署命令："
        echo "  PROJECT_DIR=\$(pwd) NUMBA_NUM_THREADS=18 \\"
        echo "      nohup bash run_arxiv_t1.sh > /dev/null 2>&1 &"
    fi

    do_shutdown "$status"

} > "$LOG" 2>&1
