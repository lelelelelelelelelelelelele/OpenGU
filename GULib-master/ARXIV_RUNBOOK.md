# ARXIV_RUNBOOK — ogbn-arxiv Phase B 专属执行手册

> Created: 2026-05-07
> Last updated: 2026-05-07（重写，对齐当前 yaml 实际配置）
> Scope: ogbn-arxiv 一族（Phase B.1 / B.2-T1/T2/T3 + IM-only slice）
> 上层手册：`SERVER_RUNBOOK.md`（cora、universal 步骤）

## 0. TL;DR — arxiv 跟 cora 不一样的地方

| 维度 | cora（在 SERVER_RUNBOOK.md） | **arxiv（本手册）** |
|---|---|---|
| 训练节点 | 135 / 2,166 | **135,474** |
| 总节点 | 2,708 | **169,343** |
| 边 | 10K | **1.3M** |
| GCN 参数 | 92K | **109K (3 层 / 256 hidden)** |
| TracIn G 矩阵 | 800 MB（dense 直接跑）| **55-68 GB（必须走 chunked）** |
| 单 GPU cell 时长 | ~2 min | **~50-90 min（含 retrain）** |
| 推荐硬件 | RTX 4090 24GB | **A800/H800 80GB**（retrain 22GB peak，4090 边缘 OOM）|
| 推荐流程 | 单机一把跑 | **按 strategy 类型解耦**：IM-only 可 4090；TracIn/Hybrid 上 80GB |

**核心 fix（部署前提）**：分支 `release/phase-b-fixes` 必须 pull
- chunked TracIn — 解决 G 矩阵 OOM
- IM CELF cross-cell cache（im_selector_seed=2024 anchored）— 解决"每个 cell 重跑 IM"
- topology-only seed anchoring — degree/pagerank 跨 method/seed 共享 cache
- prewarm cache-check before FATAL — shard 方法可命中 GIF/GNNDelete 写的 SelectionCache（commit 待 push）

---

## 1. 当前 yaml 矩阵（事实表，所有数字基于此）

| yaml | dataset | model | ratio | methods | strategies | seeds | cell 数 |
|---|---|---|---|---|---|---|---|
| `phase_b_arxiv_T1_seed42.yaml` | ogbn-arxiv | GCN | 0.01 | GIF, GNNDelete, GraphEraser | random, degree, pagerank, tracin, im, hybrid | [42] | **18** (3×6×1) |
| `phase_b_arxiv_T2_seed212.yaml` | 同 | 同 | 0.01 | 同 | 同 | [212] | 18 |
| `phase_b_arxiv_T3_seed722.yaml` | 同 | 同 | 0.01 | 同 | 同 | [722] | 18 |
| `phase_b_arxiv_im_only_r01.yaml` | 同 | 同 | 0.01 | 同 | **im 只** | [42, 212, 722] | **9** (3×1×3) |
| `phase_b_arxiv_im_only.yaml` | 同 | 同 | **0.05** | 同 | im 只 | [42, 212, 722] | 9 |
| `phase_b_arxiv_tracin_smoke.yaml` | 同 | 同 | 0.01 | GIF | tracin | [42] | 1 |
| `phase_b_arxiv_hybrid_smoke.yaml` | 同 | 同 | 0.01 | GIF | hybrid | [42] | 1 |

`extra_args` 关键参数（所有 arxiv yaml 共用）：
- `--candidate_fraction 0.1`（IM 只看 train_node 度数 top-10%，约 13.5K 候选）
- `--mc_rounds 50`（IM 每候选 MC 模拟次数）
- `--im_v4_batch_size 1`（classic CELF lazy greedy；k≈1355 不要用 batch 近似）

`k`（被攻击的节点数）= `train_nodes × ratio` = 135474 × 0.01 ≈ **1355**

---

## 2. Quick Reference — copy-paste 命令

> 前提：已经 `git checkout release/phase-b-fixes && git pull`

### 2.1 `run_arxiv.sh` 一键部署（3 种 MODE）

```bash
ssh <gpu-host>
cd ~/autodl-fs/OpenGU/GULib-master
git fetch origin && git checkout release/phase-b-fixes && git pull

# 先 dry-run（前台跑 STAGE A 看到 base train 进度条就 Ctrl+C）
SKIP_SHUTDOWN=1 bash run_arxiv.sh

# 正式跑（三选一）：
nohup MODE=prewarm bash run_arxiv.sh > /dev/null 2>&1 &     # A. TracIn cache prewarm，~4h
nohup MODE=im_only bash run_arxiv.sh > /dev/null 2>&1 &     # B. IM-only @ r=0.01，~30 min
nohup bash run_arxiv.sh > /dev/null 2>&1 &                  # C. smoke + T1 全套，~7-11h（默认 full）

disown && exit
```

| MODE | yaml | 跑啥 | cell 数 | 时长 | 关机 |
|---|---|---|---|---|---|
| `prewarm` | T1 | TracIn selection prewarm | 1（GIF 实算）+ 2 hit | ~1.5h | ✅ |
| `im_only` | im_only_r01 | 3 method × 3 seed × IM | 9 | ~30 min | ✅ |
| `full`（默认）| smoke → T1 | smoke 1 cell + T1 18 cell | 1 + 18 | ~10-11h | ✅ |

可调环境变量：`SMOKE_TIMEOUT=4h`、`PREWARM_TIMEOUT=6h`、`IM_TIMEOUT=2h`、`SKIP_SHUTDOWN=1`、`NUMBA_NUM_THREADS=18`

### 2.2 直接 python（不要关机时用）

```bash
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_arxiv_im_only_r01.yaml
H:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/ogbn-arxiv_GCN_r0.01    # pass/fail
```

### 2.3 跑完检查

```bash
ls -lt logs/run_arxiv_*.log | head -1
tail -100 <log>                                                       # 看 ALL DONE 行 + cells_complete=N/M
ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed42/attack.json | wc -l     # T1 期望 18
ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed*/attack.json | wc -l      # T1+T2+T3 期望 54
ls results/runs/ogbn-arxiv_GCN_r0.01/*_im/seed*/attack.json | wc -l   # im_only 期望 9
ls results/score_cache/if/*.npz | wc -l                               # 见 §4.2 真实期望
```

---

## 3. 硬件规划

### 3.1 Stage 选择硬件对照

| 阶段 | peak GPU mem | 4090 24GB | **A800 80GB** | H20 95GB |
|---|---|---|---|---|
| Base train | <2 GB | ✅ | ✅ | ✅ |
| **TracIn chunked** | **~5 GB** | ✅ | ✅ | ✅ |
| IM (numba CPU bound) | <2 GB | ✅ | ✅ | ✅ |
| Hybrid (TracIn + IM) | ~5 GB | ✅ | ✅ | ✅ |
| Unlearn | <5 GB | ✅ | ✅ | ✅ |
| MIA | <1 GB（CPU-bound）| ✅ | ✅ | ✅ |
| **Collateral retrain** | **~22 GB** | ⚠ **边缘 OOM**（B.1 实测 3/5 cell OOM） | ✅ | ✅ |

**推荐**：
- IM-only / smoke / 不带 collateral 的探针 → 4090 OK
- T1/T2/T3 含 collateral retrain → A800/H800 80GB
- ❌ 不推荐 H20（实测 H800 1/3 算力，T1 拉到 ~30h）

### 3.2 IM 算法本身的硬件特性

`im_strategy.py` 是纯 numba JIT（`numba.prange` + `@njit`），**不走 GPU**：
- IM-only 在 4090 上：**host CPU** 跑 IM 选点；**GPU** 跑 base train + unlearn + MIA
- CPU-only 机器也能跑 IM-only？❌ 不行 —— yaml 流程含 base train + unlearn，需要 GPU
- 只想 prewarm IM cache 一份给 GPU 用？走 `prewarm_selection_cache.py --strategies im`，CPU 实例足够（见 §5）

---

## 4. 工作流（按场景）

### 4.1 场景 A：单机 4090 跑 IM-only（你今晚的方案）

CPU 满了，把 IM 这片单独切到 4090：

```bash
# 4090 host
ssh <4090-host>
cd ~/autodl-fs/OpenGU/GULib-master
git pull
NUMBA_NUM_THREADS=8 nohup MODE=im_only bash run_arxiv.sh > /dev/null 2>&1 &
disown
```

注意 `phase_b_arxiv_im_only_r01.yaml` 已设 `run_collateral: false`（避开 4090 22GB OOM）。retrain gap 留给后续 80GB GPU 补。

预期产物：9 个 `attack.json` + `predictions.npz` + `_meta.json`（无 `collateral.json`）。

### 4.2 场景 B：单机 80GB GPU 跑 T1/T2/T3 完整矩阵

```bash
ssh <a800-host>
cd ~/autodl-fs/OpenGU/GULib-master
git pull

# 先 smoke 一遍（1 cell, ~90 min）
nohup bash run_arxiv.sh > /dev/null 2>&1 &     # MODE=full：smoke + T1

# T2/T3 串行（T1 完成后手动启）
nohup python experiments/run.py experiments/configs/phase_b_arxiv_T2_seed212.yaml > logs/t2_$(date +%s).log 2>&1 &
nohup python experiments/run.py experiments/configs/phase_b_arxiv_T3_seed722.yaml > logs/t3_$(date +%s).log 2>&1 &
```

### 4.3 场景 C：双机分工（CPU prewarm IM + GPU 跑主矩阵）

如果 IM 选点想在便宜 CPU 实例上提前算好，再传给 GPU：

**机 CPU**（autodl 32 核 ~¥0.5-1/h，~5 min）：
```bash
ssh <cpu-host>
cd ~/autodl-fs/OpenGU/GULib-master
git pull
export NUMBA_NUM_THREADS=32
python scripts/prewarm_selection_cache.py \
    experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    --strategies im,degree,pagerank
tar czf topology_cache.tar.gz results/score_cache/im_celf/ results/selection_cache/
scp topology_cache.tar.gz <gpu-host>:~/autodl-fs/OpenGU/GULib-master/
```

**机 GPU**：
```bash
tar xzf topology_cache.tar.gz
nohup bash run_arxiv.sh > /dev/null 2>&1 &
```

**为什么 IM 拆出来跑划算**：IM 不走 GPU，跑在 80GB 卡上的 host CPU 是浪费贵实例时间。CPU 实例 ¥0.15 vs A800 ¥0.5/cell IM 选点。

---

## 5. Cache 行为（实测，非推算）

### 5.1 SelectionCache（顶层选点结果）

`attack_manager.py:_build_selection_config:240-254` —— key 字段：
```
dataset_name, base_model, unlearn_ratio, seed, strategy_name, k,
is_transductive, is_balanced, train_ratio, val_ratio, test_ratio,
graph_fingerprint, strategy_params_fingerprint
```

**关键：key 里没有 `unlearning_methods`**（只有 `seed`，且对 IM/topology-only 还有 anchor 替换）：

| strategy | seed_for_key | 跨 method 共享？ | 跨 GU seed 共享？ | 文件数（T1）|
|---|---|---|---|---|
| `random` | GU seed | ✅ | ❌ | 1（per seed）|
| `degree` | TOPOLOGY_ONLY_SEED_ANCHOR | ✅ | ✅ | **1**（全局）|
| `pagerank` | 同上 | ✅ | ✅ | **1**（全局）|
| `im` | im_selector_seed=2024 | ✅ | ✅ | **1**（全局）|
| `tracin` | GU seed | ✅ | ❌ | 1（per seed）|
| `hybrid` | GU seed | ✅ | ❌ | 1（per seed，含 alpha 进 fingerprint）|

T1（seed=42）SelectionCache 文件期望：
- 1 random + 1 degree + 1 pagerank + 1 im + 1 tracin + 1 hybrid = **6 个 .json**

T1+T2+T3 累计：
- topology-only (degree/pagerank/im) = 3 个（跨 seed 共享）
- random/tracin/hybrid = 3 seed × 3 strategy = 9 个
- = **12 个 .json**

### 5.2 ScoreCache (TracIn IF, `score_cache/if/`)

`tracin_strategy.py:_build_cache_config:136-148` —— key 含 `unlearning_methods` + `seed`。

**但实际上**：GIF 第一个跑时算 IF + 写 ScoreCache + 写 SelectionCache。后续 GNNDelete/GraphEraser 在 **SelectionCache 层就 hit**（method-agnostic key），**不会进 ScoreCache 路径**，**不会再写 IF 文件**。

T1 IF 文件实测期望 = **1 个**（仅第一个跑的 method 写）
T1+T2+T3 IF 文件实测期望 = **3 个**（每 seed 一个）

⚠ `prewarm_selection_cache.py` 的 `expected 3` 是过度估计 —— 假设每 method 都要写 IF。实测只 1 个就够。

⚠ 历史残留：你机器上 `score_cache/if/` 可能有 11+ 个 .npz —— 来自 r=0.05 / 其他 seed / pre-Phase-B 的旧 schema。**不影响新跑**，要清的话每 .json sidecar 里有该 cache 的 (ratio, seed, method) 标签。

### 5.3 ScoreCache (IM CELF, `score_cache/im_celf/`)

IM CELF 完整 spread 计算的中间结果。key 为 `(dataset, num_nodes, k, candidate_fraction, mc_rounds, propagation_prob, im_selector_seed)`，**完全不含 method/GU seed**。

T1 期望 = **1 个**（首个 IM cell 写，后 17 cell 全 hit）
T1+T2+T3 期望 = **1 个**（im_selector_seed=2024 跨所有 seed 共享）

### 5.4 ResultCache (`results/cache/`)

完整 cell 输出的 hash-named 缓存。key 含所有训练/攻击/评估超参（含 `gcn_hidden`、`gcn_num_layers`），见 `results/cache/CLAUDE.md`。完全相同配置重跑会全 hit。

---

## 6. Cell 内监控

### 6.1 GPU + CPU 双窗

```bash
watch -n 5 'echo "=== GPU ==="; \
            nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv; \
            echo; echo "=== CPU ==="; free -h | head -2'
```

**预期内存爬升曲线**（一个含 retrain 的 cell）：
```
T+0:00   GPU ~2 GB（base model 训练）
T+0:30   GPU ~3-5 GB（TracIn chunked，G 矩阵在 CPU side）
T+76:00  GPU ~3 GB（TracIn 结束）
T+78:00  GPU ~5 GB（unlearn）
T+90:00  GPU ~22 GB（collateral retrain ← 4090 这里 OOM）
T+91:00  GPU ~5 GB（cell 收尾）
```

IM-only cell（无 retrain）：
```
T+0:00   GPU ~2 GB（base train）
T+0:30   CPU 8 核 100%（IM CELF lazy greedy）
T+3:00   GPU ~5 GB（unlearn）
T+5:00   GPU ~1 GB（MIA, CPU bound）
T+8:00   完成
```

### 6.2 进度计数

```bash
ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed42/attack.json 2>/dev/null | wc -l       # T1: 18
ls results/runs/ogbn-arxiv_GCN_r0.01/*/seed*/attack.json 2>/dev/null | wc -l        # T1+T2+T3: 54
ls results/runs/ogbn-arxiv_GCN_r0.01/*_im/seed*/attack.json 2>/dev/null | wc -l     # im_only: 9
```

### 6.3 Cache 命中率 sanity（T1 跑完）

```bash
# IM cache hit 数（T1 应有 5 次：18 cell 里有 6 个 im+hybrid，第 1 个写 → 后 5 个 hit）
grep -c "HIT  im_celf\|hit ] im\|hit ] hybrid" logs/run_arxiv_full_*.log

# TracIn cache hit 数（T1 应有 5 次：6 个 tracin/hybrid cell，第 1 个写 → 后 5 个 hit selection）
grep -c "HIT  if\|hit ] tracin\|hit ] hybrid" logs/run_arxiv_full_*.log

# Chunked path 触发数（T1 应有 1 次：仅首个真算 IF 的 cell）
grep -c "chunked path" logs/run_arxiv_full_*.log
```

---

## 7. 故障处理

### 7.1 TracIn 仍然 OOM（不应该）

```
torch.cuda.OutOfMemoryError: Tried to allocate XX.XX GiB ...
```
1. grep `[TracIn] G matrix` 看是否走 chunked path
2. yaml 加 `tracin_chunk_size: 500`（默认 1000）
3. `nvidia-smi` 看是否别的进程占了

### 7.2 collateral retrain 在 4090 OOM

```
torch.cuda.OutOfMemoryError ... while training ...
```
- 预期内：4090 24GB 跑 22GB peak retrain 边缘 OOM
- 解：yaml 设 `run_collateral: false`，retrain 留给 80GB GPU 补
- 或：`PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb=128` 减碎片

### 7.3 IM cache MISS（应该 HIT 却显示 MISS）

```
[ScoreCache] MISS im_celf  key=<hash>
```
1. CPU 实例 prewarm 用的 IM hyperparams 跟主跑不一致（candidate_fraction / mc_rounds / propagation_prob / im_v4_batch_size / im_selector_seed 任一不同 → key 不同）
2. tar 解错位置：cache 应该在 `results/score_cache/im_celf/`，不要解到 `results/score_cache/`
3. 文件权限：`chmod -R u+rwX results/score_cache/`

调试：
```bash
ls results/score_cache/im_celf/
cat results/score_cache/im_celf/<key>.json | python -m json.tool   # 看 key 对应的 config
```

### 7.4 prewarm script 对 GraphEraser 报 FATAL

```
[FATAL] prewarm_selection_cache cannot compute trained-model selectors
        from shard/SISA method GraphEraser
```

**原因**：旧版 prewarm 在 cache 查询前就 FATAL，无视 GIF/GNNDelete 已写好的 SelectionCache。

**fix（commit 待 push）**：cache 查询挪到 FATAL 前。修后 GraphEraser 在 GIF/GNNDelete 已 prewarm 过的前提下全 hit，不再 FATAL。

**临时解法**：把 GraphEraser 从 prewarm yaml 拿掉，跑 `experiments/run.py <主 yaml>` 时它走 attack_manager 正常路径，自动 hit GIF 写的 SelectionCache。

### 7.5 单 cell 跑超过 2 小时

可能挂在：
- TracIn pass-1 backprop 慢（应 ~1 min/1000 candidates，arxiv ~13 min for k=1355）
- MIA CPU-bound（cell 100 iter × 3.6s × 2 round = 12 min 是正常）
- IM cache miss 后跑全 CELF（不应该；如果 prewarm 配置不一致就会发生 → §7.3）

`tail -f logs/<cell>.log` 看具体卡哪。

---

## 8. 时间 + 成本预算

### 8.1 T1 单 seed（A800 80GB，所有 fix 已合）

| 阶段 | 单 cell | 18 cell（T1）| 备注 |
|---|---|---|---|
| Base train | 30 s | 9 min | 每 cell 重训 |
| TracIn selection | 76 min | **76 min**（仅首个 method × strategy 实算）| 后续 SelectionCache hit |
| IM selection | 3 min | **3 min**（仅首个 cell 实算）| 后 17 cell hit |
| Hybrid IF/IM 部分 | cache hit | 0 | 完全复用 §5.1/5.2 |
| GU + MIA | ~12 min | ~3.6 h | per cell |
| Collateral retrain | ~5 min | ~1.5 h | per cell |
| **T1 总计** | | **~7-9 h** | |

### 8.2 IM-only（4090 / r=0.01 / 9 cell / 无 collateral）

| 阶段 | 9 cell |
|---|---|
| Base train | ~5 min |
| IM selection（首次） | ~3 min |
| IM cache hit × 8 | <1 s |
| Unlearn | ~9 min |
| MIA | ~12 min |
| **总计** | **~30-40 min** |

### 8.3 完整成本（autodl 价目，参考）

| 项 | 成本 |
|---|---|
| CPU prewarm（场景 C, 5 min × ¥0.8/h）| ¥0.07 |
| IM-only（4090, 30 min × ¥1-2/h）| ¥0.5-1 |
| T1 单 seed（A800, ~8h × ¥4-5/h）| ¥32-40 |
| T1+T2+T3 三 seed | ¥96-120 |

---

## 9. 文件结构地图（arxiv 跑完之后）

```
results/
├── score_cache/                                ← 跨 cell 共享的 score 缓存
│   ├── if/<key>.npz                            ← TracIn IF：1 个/seed（实测）
│   ├── im/<key>.npz                            ← Hybrid IM step-1，跨方法共享
│   └── im_celf/<key>.npz                       ← IM 完整 CELF：1 个全局
│
├── selection_cache/                            ← AttackManager-level 顶层选点
│   └── *.json                                  ← T1: 6 个 / T1+T2+T3: 12 个（见 §5.1）
│
├── runs/ogbn-arxiv_GCN_r0.01/                  ← cell 产物
│   ├── GIF_random/seed42/{attack,collateral,predictions,_meta}.json/.npz
│   ├── GIF_degree/seed42/...
│   ├── ... (T1: 18 dirs / T1+T2+T3: 54 dirs / im_only: 9 dirs)
│   └── GraphEraser_hybrid/seed722/...
│
├── cache/                                      ← cell-level ResultCache
│   └── *.json                                  ← hash-named, 见 results/cache/CLAUDE.md
│
└── _journal/auto_report.md                     ← 自动追加的实验日志
```

---

## 10. 验证 deployment 是否成功（30 秒检查清单）

跑完 T1 第一个 cell 后：

```bash
# 1) cell 4 文件齐全（im_only 模式无 collateral.json）
ls results/runs/ogbn-arxiv_GCN_r0.01/GIF_tracin/seed42/
# 期望: attack.json collateral.json predictions.npz _meta.json

# 2) attack.json 数字合理
python -c "
import json
d = json.load(open('results/runs/ogbn-arxiv_GCN_r0.01/GIF_tracin/seed42/attack.json'))
for r in d.get('results', []):
    print(r.get('strategy'), 'f1_drop=', r.get('f1_drop'), 'mia_auc=', r.get('mia_auc'))
"
# 期望：tracin f1_drop > random f1_drop（攻击有效）；mia_auc > 0.5（不是 bug）

# 3) cache 落盘
ls results/score_cache/if/        # 至少 1 个 .npz
ls results/score_cache/im_celf/   # 至少 1 个 .npz
ls results/selection_cache/       # 至少 6 个 .json

# 4) chunked TracIn 触发
grep "chunked path" logs/*.log | head -1
# 期望：[TracIn] G matrix ~XX.X GB > 4.0 GB threshold → chunked path
```

四项过 = arxiv 部署成功。

---

## 11. 与 SERVER_RUNBOOK.md 的关系

**这本手册替代** SERVER_RUNBOOK.md 的：
- arxiv 时长表
- B.1 / B.2 arxiv 流程
- 显存外推探针
- arxiv 一键串

**仍然查 SERVER_RUNBOOK.md**：
- Phase 表（顶层概览）
- ssh + tmux 标准流程
- cora B.3/B.4 流程
- fresh-clone bootstrap
- universal 故障处理
- 数据回收与合并
