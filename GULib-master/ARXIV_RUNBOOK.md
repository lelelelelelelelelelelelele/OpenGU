# ARXIV_RUNBOOK — ogbn-arxiv Phase B 专属执行手册

> Created: 2026-05-07
> Last updated: 2026-05-07
> Scope: ogbn-arxiv 一族（Phase B.1 / B.2-T1/T2/T3）
> 上层手册：`SERVER_RUNBOOK.md`（cora、universal 步骤）

## 0. TL;DR — arxiv 跟 cora 不一样的地方

| 维度 | cora（在 SERVER_RUNBOOK.md） | **arxiv（本手册）** |
|---|---|---|
| 训练节点 | 135 / 2,166 | **135,474** |
| 总节点 | 2,708 | **169,343** |
| 边 | 10K | **1.3M** |
| GCN 参数 | 92K | **109K (3 层 / 256 hidden)** |
| TracIn G 矩阵 | 800 MB（dense 直接跑）| **55 GB（必须走 chunked）** |
| 单 GPU cell 时长 | ~2 min | **~50-90 min** |
| 推荐硬件 | RTX 4090 24GB | **A800 80GB + CPU 32 核** |
| 推荐流程 | 单机一把跑 | **2 机解耦：CPU 算 IM → GPU 跑主矩阵** |

**核心 fix（部署前提）**：分支 `release/phase-b-fixes` 必须 pull
- chunked TracIn（commit `194f549`）— 解决 OOM
- IM CELF cross-cell cache（commit `3f4d557`）— 解决"每个 cell 重跑 2-4h IM"
- topology-only seed anchoring（commit pending）— degree/pagerank 共享 cache

---

## Quick Reference — 你只想 copy-paste 命令的话看这里

> 前提：已经 `git checkout release/phase-b-fixes && git pull`

### 0. CPU 实例（机 A'，~¥0.5-1/h）— prewarm IM

```bash
export NUMBA_NUM_THREADS=32

# 跑 IM 完整 CELF，写到 results/score_cache/im_celf/<key>.npz
python scripts/prewarm_selection_cache.py \
    experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    --strategies im

# 打包传输给 GPU 实例
tar czf im_celf_cache.tar.gz results/score_cache/im_celf/
scp im_celf_cache.tar.gz <a800-host>:~/autodl-fs/OpenGU/GULib-master/
```

预期：5-10 min 出 cache（~30s 如果 1% ratio）。

### 1. A800 实例（机 B）— 解 cache + 烟囱

```bash
tar xzf im_celf_cache.tar.gz   # 解到 results/score_cache/im_celf/
```

#### 1a. TracIn 单 cell 烟囱（验 chunked TracIn）

```bash
python experiments/run.py \
    experiments/configs/phase_b_arxiv_tracin_smoke.yaml
```

预期 **~90 min**。必看 `[TracIn] G matrix ... → chunked path`。

#### 1b. Hybrid 单 cell 烟囱（验 TracIn + IM cache 联动）

```bash
python experiments/run.py \
    experiments/configs/phase_b_arxiv_hybrid_smoke.yaml
```

预期 **~17 min**（如果 1a TracIn cache + IM prewarm cache 都有）/ **~95 min**（cache 都没）。
必看 `[ScoreCache] HIT  im  key=...`（im 命中=机 A' prewarm 成功传过来）。

### 2. A800 实例 — 主矩阵（T1 必跑，T2/T3 条件跑）

```bash
# T1 (12 cell, seed=42, ~10-11h)
python experiments/run.py \
    experiments/configs/phase_b_arxiv_T1_seed42.yaml

# T2 (条件跑, seed=212)
python experiments/run.py \
    experiments/configs/phase_b_arxiv_T2_seed212.yaml

# T3 (条件跑, seed=722)
python experiments/run.py \
    experiments/configs/phase_b_arxiv_T3_seed722.yaml
```

### Cache 共享矩阵（一次跑出来后哪些 cell 受益）

| Cache 路径 | 写入触发 | 受益的 cell |
|---|---|---|
| `results/score_cache/if/<key>.npz` | TracIn 在某 method 第一次跑 | 同 method × {tracin, hybrid} 后续 cell |
| `results/score_cache/im/<key>.npz` | Hybrid 第一次调 IM step1 | 全 18 cell × {hybrid}（跨 method、跨 GU seed）|
| **`results/score_cache/im_celf/<key>.npz`** | IM 完整 CELF 第一次跑（机 A' prewarm 或机 B 第一次 IM cell）| **全 18 cell × {im}（跨 method、跨 GU seed）** |
| `results/cache/<key>.json` | 任何 cell 完整跑完 | 完全相同配置的重跑 |

### 失败兜底命令

```bash
# 检查 4 个产物文件齐全
ls results/runs/ogbn-arxiv_GCN_r0.05/GIF_tracin/seed42/
# 应有: attack.json collateral.json predictions.npz _meta.json

# 看 attack.json 的关键数字
python -c "
import json
d = json.load(open('results/runs/ogbn-arxiv_GCN_r0.05/GIF_tracin/seed42/attack.json'))
for r in d.get('results', []):
    print(r.get('strategy'), 'f1_drop=', r.get('f1_drop'), 'mia_auc=', r.get('mia_auc'))
"

# 验证 chunked path 触发
grep "chunked path" logs/*.log | tail -1

# 验证 cache 命中
grep "HIT  im_celf\|HIT  if\|HIT  im " logs/*.log | head -10
```

---

## 1. 硬件规划

### 1.1 GPU 实例（机 B，跑 B.2 主矩阵）

| 阶段 | peak GPU mem | 4090 24GB | **A800 80GB** | H20 95GB |
|---|---|---|---|---|
| Base train | <2 GB | ✅ | ✅ | ✅ |
| **TracIn chunked** | **~5 GB** | ✅ | ✅（58 GB 余量）| ✅ |
| Random / IM | <2 GB | ✅ | ✅ | ✅ |
| Unlearn | <5 GB | ✅ | ✅ | ✅ |
| MIA | <1 GB（CPU-bound）| ✅ | ✅ | ✅ |
| **Collateral retrain** | **~22 GB** | ⚠ 边缘 OOM | ✅（58 GB 余量）| ✅ |

**推荐：A800 80GB**。retrain 22GB 是真红线（pre-fix 实测 3/5 cell OOM 在 4090 上）。
**不推荐：4090**（retrain 边缘风险）。
**不推荐：H20**（per `SERVER_RUNBOOK.md:648` 实测 H800 1/3 算力 → B.2 拉到 38-40h）。

### 1.2 CPU 实例（机 A'，跑 IM prewarm）

| 资源 | 需求 | autodl 32 核实例典型 |
|---|---|---|
| CPU | numba prange MC 并行 | 32 核 Xeon Gold/Platinum |
| RAM | adj + 32 thread state ~5 GB | 60 GB（典型）|
| 磁盘 | cache + repo ~2 GB | 50 GB+ |
| GPU | **不需要** | 0 |
| CUDA | **不需要** | 任意 |

**典型机型**：autodl 通用计算型 32 核 Xeon Platinum，~¥0.5-1/h。

### 1.3 双机分工（推荐）

```
机 A' (CPU 32 核, ~¥0.5-1/h)
    └─ Stage 1: IM prewarm   ~5-10 min
                                    │
                                    ▼
                        scp im_celf_cache.tar.gz
                                    │
                                    ▼
机 B  (A800 80GB, ~¥4-5/h)
    └─ Stage 2: B.2 主矩阵   ~10-12h（含全 cell 缓存命中）
```

**为什么这样拆**：
- IM 是纯 CPU（select_nodes 不碰 GPU），跑在 GPU 上是浪费
- IM 需要 1 次实算 × 18 cell 共享（cross-method/seed）
- TracIn 必须 GPU（autograd），但 chunked 后只占 5GB 显存
- retrain 必须 GPU，22GB peak

---

## 2. 代码前置（两机都要做一次）

```bash
# 1) 拉分支（一次性）
cd ~/autodl-fs/OpenGU/GULib-master  # 你实际项目路径
git fetch origin
git checkout release/phase-b-fixes
git pull

# 2) 验证分支正确（应看到三个关键 commit）
git log --oneline -5
# 期望前三行包含：
#   bde2a2e docs(dashboard): bump Last updated...
#   3055979 merge fix/im-celf-shared-cache...
#   2e52160 merge fix/tracin-chunked-arxiv...

# 3) sanity（cora，本地 ~30s 验环境，不算 GPU 时间）
python experiments/run.py experiments/configs/sanity_one_cell.yaml
```

---

## 3. Stage 1 — CPU 实例上 prewarm IM

### 3.1 启动

```bash
ssh <cpu-host>
cd ~/autodl-fs/OpenGU/GULib-master

# 强制 numba 用全 32 核（默认会但稳妥起见显式设）
export NUMBA_NUM_THREADS=32

# 进 tmux 防 ssh 断
tmux new -s im_prewarm

# Prewarm。这一次的输出会写到 results/score_cache/im_celf/<key>.npz
python scripts/prewarm_selection_cache.py \
    experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    --strategies im 2>&1 | tee logs/im_prewarm_$(date +%Y%m%d_%H%M).log

# Ctrl-b d  detach，回来 tmux attach -t im_prewarm
```

### 3.2 必看的 stdout 信号

```
[必须看到] [ScoreCache] MISS im_celf  key=<32 hex> — running full CELF on 13547 candidates...
[~5-10 min 后] [ScoreCache] SAVE im_celf  key=<32 hex> -> ./results/score_cache/im_celf/<key>.npz
```

> 如果看到 `[ScoreCache] HIT` —— 之前可能跑过 prewarm，cache 已有。直接跳到 §3.3 打包。

### 3.3 打包传输

```bash
# 打包
tar czf im_celf_cache.tar.gz results/score_cache/im_celf/
ls -lh im_celf_cache.tar.gz   # 应该几 MB（npz 压缩后很小）

# 传给机 B
scp im_celf_cache.tar.gz <a800-host>:~/autodl-fs/OpenGU/GULib-master/

# 释放 CPU 实例（不再需要）
exit
```

### 3.4 时间 + 成本

| 步骤 | 时长 | 成本（autodl ~¥0.8/h）|
|---|---|---|
| 实例启动 + git pull | 2 min | ¥0.03 |
| numba JIT 编译 | 30 s | ¥0.01 |
| IM CELF 实算（k=6773）| 5-10 min | ¥0.07-0.13 |
| tar + scp | 30 s | ¥0.01 |
| **总计** | **~10-15 min** | **~¥0.15** |

---

## 4. Stage 2 — A800 上跑 B.2 主矩阵

### 4.1 解 cache + 启动

```bash
ssh <a800-host>
cd ~/autodl-fs/OpenGU/GULib-master
git pull   # 确保最新

# 解 IM cache（机 A' 传过来的）
tar xzf im_celf_cache.tar.gz
ls results/score_cache/im_celf/   # 应看到 .npz + .json

# 进 tmux
tmux new -s phaseB
```

### 4.2 烟囱测（首次必跑，~90 min）

先跑单 cell 验证 chunked TracIn + IM cache 命中：

```bash
python experiments/run.py experiments/configs/phase_b_arxiv_tracin_smoke.yaml \
    2>&1 | tee logs/tracin_smoke_$(date +%Y%m%d_%H%M).log
```

**T+2 min 必看**：
```
[TracIn] G matrix ~57.0 GB > 4.0 GB threshold → chunked path (chunk_size=1000, CPU offload)
```

**T+76-80 min 必看**：
```
[ScoreCache] SAVE if  key=<...> -> ./results/score_cache/if/<key>.npz
```

**~90 min 后产物**：
```
results/runs/ogbn-arxiv_GCN_r0.05/GIF_tracin/seed42/
├── attack.json
├── collateral.json
├── predictions.npz
└── _meta.json
```

### 4.3 主矩阵 T1（必跑，12 cell）

烟囱测 PASS 后跑：

```bash
python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    2>&1 | tee logs/t1_seed42_$(date +%Y%m%d_%H%M).log
```

**预期 cache 行为**（每个 cell 都应该看到）：
```
# 第一次遇到某 method 的 tracin cell
[TracIn] G matrix ... → chunked path
[ScoreCache] MISS if  key=...
[ScoreCache] SAVE if  key=...

# 同 method 的 hybrid 相关 cell
[ScoreCache] HIT  if  key=...   ← TracIn IF 命中
[ScoreCache] HIT  im  key=...   ← Hybrid IM step1 命中

# 任何 IM 直接 cell
[ScoreCache] HIT  im_celf  key=...   ← 全部命中（来自机 A' prewarm）
```

### 4.4 T2 / T3（条件跑，deadline 富余时）

```bash
# T2 (seed=212) 仅在 T1 完成 + deadline 富余 ≥6h 时启
python experiments/run.py experiments/configs/phase_b_arxiv_T2_seed212.yaml ...

# T3 (seed=722) 同上
python experiments/run.py experiments/configs/phase_b_arxiv_T3_seed722.yaml ...
```

**重要事实**：T2/T3 期间 IM cache 全部 HIT（im_selector_seed=2024 跨 GU seed 共享）。
TracIn cache **每个 seed 独立 ~7-8h**（key 含 GU seed）。

---

## 5. 时间 + 成本预算

### 5.1 修订后的 T1 预算（A800 80GB，含三个 fix 后）

| 阶段 | 单 cell | 12 cell | 备注 |
|---|---|---|---|
| Base train | 30 s | 6 min | |
| TracIn selection | 76 min | 76 min × 6 method = ~7.5 h | 同 method 跨 strategy 命中 |
| IM selection | **~0 s（cache hit）** | **~0 s × 18** | ✅ prewarm 之后全免费 |
| Hybrid IF 部分 | cache hit | 0 | TracIn 同 method 复用 |
| Hybrid IM 部分 | cache hit | 0 | im namespace 跨方法共享 |
| GU + MIA + retrain | ~14 min | ~3 h | |
| **T1 总计** | | **~10-11 h** | |

> **跟 pre-fix 对比**：原 SERVER_RUNBOOK.md 估 21-24h。三个 fix 砍到 ~10-11h（缩 1/2）。

### 5.2 完整成本（T1 only，必跑）

| 项 | 成本 |
|---|---|
| CPU 实例 stage 1（10-15 min × ¥0.8/h）| ¥0.15 |
| A800 stage 2（10-11h × ¥4-5/h）| ¥45-55 |
| **T1 总成本** | **~¥45-55** |

### 5.3 T1 + T2 + T3 总成本（如果都跑）

| 项 | 成本 |
|---|---|
| CPU stage 1 (单次)| ¥0.15 |
| A800 stage 2 (3 个 seed × ~10h)| ¥130-160 |
| **三 seed 总成本** | **~¥130-160** |

---

## 6. Cell 内监控

### 6.1 GPU + CPU 双窗监控

另开 tmux 窗口：

```bash
watch -n 5 'echo "=== GPU ==="; \
            nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv; \
            echo; echo "=== CPU ==="; \
            free -h | head -2'
```

**预期内存爬升曲线**（一个 cell）：
```
T+0:00   GPU ~2 GB（base model 训练）
T+0:30   GPU ~3-5 GB 稳定（TracIn chunked）
                CPU available 从 200+ GB 缓慢降到 ~140 GB（55GB G 矩阵在 CPU）
T+76:00  GPU ~3 GB（TracIn 结束，pass 2）
T+78:00  GPU ~5 GB（unlearn）
T+90:00  GPU ~22 GB（retrain）
T+91:00  GPU ~5 GB（cell 结束，准备下一个）
```

### 6.2 进度计数（任何机器）

```bash
# T1 已完成 cell 数（应在 0-12 之间增长）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/attack.json 2>/dev/null | wc -l

# 总览（含 T2/T3）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json 2>/dev/null | wc -l
```

### 6.3 Cache 命中率 sanity

```bash
# IM cache 命中数（T1 应有 8 次：4 method × 2 strategy{im,hybrid}）
grep -c "HIT  im_celf" logs/t1_*.log

# TracIn cache miss 数（T1 应有 6 次：每 method 算一次 selection）
grep -c "MISS if " logs/t1_*.log

# Chunked path 触发数（T1 应有 6 次，对应 TracIn miss）
grep -c "chunked path" logs/t1_*.log
```

---

## 7. 故障处理（arxiv-specific）

### 7.1 TracIn 仍然 OOM（不应该但万一）

```
torch.cuda.OutOfMemoryError: Tried to allocate XX.XX GiB ...
```

**第一时间检查**：
1. 是否走了 chunked path？grep `[TracIn] G matrix` 看分支判断
2. `chunk_size=1000` 够小吗？yaml 加 `tracin_chunk_size: 500` 砍半
3. 别的 GPU 进程占用了？`nvidia-smi`

### 7.2 IM cache 没命中（应该 HIT 但显示 MISS）

```
[ScoreCache] MISS im_celf  key=<...>
```

**可能原因**：
1. CPU 实例 prewarm 用了不同的 IM hyperparams（mc_rounds、prop、fraction、batch、selector_seed 任一不同 → key 不同）
2. tar 解错位置：cache 应该在 `results/score_cache/im_celf/`，不是 `results/score_cache/`
3. 文件权限问题：`chmod -R u+rwX results/score_cache/`

**调试**：
```bash
ls results/score_cache/im_celf/
# 看 .json sidecar 内容（key 对应的 config）
cat results/score_cache/im_celf/<key>.json | python -m json.tool
```

### 7.3 retrain 22GB 在 A800 上还是 OOM（极不可能但万一）

A800 80GB 跑 22GB peak retrain 应该有 58GB 余量。如果 OOM 说明：
1. 同实例有别的进程在占 GPU（不应该但 autodl 实例共享 docker 时会）
2. PyTorch allocator 碎片严重：设 `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb=128`

### 7.4 单 cell 跑超过 2 小时

可能挂在了：
- TracIn pass 1 backprop 慢（应 ~1 min/1000 candidates）
- MIA CPU-bound 真的慢（cell 100 iter × 3.6s × 2 round = 12 min 是正常）
- IM cache miss 后跑全 CELF（不应该，但如果 prewarm 配置不一致就会发生）

`tail -f logs/<cell>.log` 看具体卡哪里。

---

## 8. 文件结构地图（arxiv 跑完之后）

```
results/
├── score_cache/                                ← 跨 cell 共享的 score 缓存
│   ├── if/<key>.npz                            ← TracIn 6 个 method 各 1 份
│   ├── im/<key>.npz                            ← IM step-1 spread，跨方法共享
│   └── im_celf/<key>.npz                       ← IM 完整 CELF，跨方法+跨 GU seed 共享
│
├── selection_cache/                            ← AttackManager-level 顶层 selection
│   └── *.json                                  ← 每个 (method, strategy, seed) 一份
│
├── runs/ogbn-arxiv_GCN_r0.05/                  ← cell 产物
│   ├── GIF_tracin/seed42/{attack,collateral,predictions,_meta}.json/.npz
│   ├── GIF_im/seed42/...
│   ├── GIF_hybrid/seed42/...
│   ├── GNNDelete_tracin/seed42/...
│   └── ... (12 dirs for T1)
│
└── _journal/auto_report.md                     ← 自动追加的实验日志
```

cache 跨方法共享的实证：B.2-T1 跑完时
- `score_cache/im_celf/`: 应该只有 **1** 个 .npz（所有 18 cell 共享）
- `score_cache/im/`: 应该只有 **1** 个 .npz（Hybrid step-1 跨方法共享）
- `score_cache/if/`: 应该有 **6** 个 .npz（每 method 1 份）

---

## 9. 与 SERVER_RUNBOOK.md 的关系

**这本手册替代** SERVER_RUNBOOK.md 的：
- §1.2 时长表（arxiv 那行）
- §3.3 B.1 arxiv random baseline
- §3.4 B.2 arxiv 主矩阵
- 附录 A.2 显存外推探针
- 附录 A.3 机 B 一键串

**仍然查 SERVER_RUNBOOK.md**：
- §1.1 Phase 表（顶层概览）
- §2 ssh + tmux 标准流程
- §3.5+ cora B.3/B.4 流程
- §4 fresh-clone bootstrap
- §5 universal 故障处理
- §6 数据回收与合并

---

## 10. 验证 deployment 是否成功（30 秒检查清单）

机 B 上跑完 T1 第一个 cell 后：

```bash
# 1) cell 4 文件齐全
ls results/runs/ogbn-arxiv_GCN_r0.05/GIF_tracin/seed42/
# 应该 4 个：attack.json collateral.json predictions.npz _meta.json

# 2) attack.json 数字合理
python -c "
import json
d = json.load(open('results/runs/ogbn-arxiv_GCN_r0.05/GIF_tracin/seed42/attack.json'))
for r in d.get('results', []):
    print(r.get('strategy'), 'f1_drop=', r.get('f1_drop'), 'mia_auc=', r.get('mia_auc'))
"
# 期望：tracin f1_drop > random f1_drop（攻击有效）
#       mia_auc > 0.5（不是 bug）

# 3) cache 落盘
ls results/score_cache/if/   # 应有 .npz + .json
ls results/score_cache/im_celf/   # 应有从机 A' scp 过来的 + .json

# 4) chunked path 触发记录
grep "chunked path" logs/*.log | head -1
# 期望：[TracIn] G matrix ~57.0 GB > 4.0 GB threshold → chunked path
```

四项都过 = arxiv 部署成功，可以放手让 T1 跑完。
