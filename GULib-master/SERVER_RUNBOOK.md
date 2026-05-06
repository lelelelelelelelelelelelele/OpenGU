# 服务器执行手册 v4 — Phase B 双机执行

> v4 重写: 2026-05-06。原 v3 740 行散在 §5 / §5A / §0.9，本版按"先看什么 → 跑什么 → 出问题怎么办"线性整理。
> NeurIPS 截稿: 2026-05-07。

---

## 0. TL;DR — 我现在该跳到哪节

| 我现在的状态 | 跳到 |
|---|---|
| 第一次进这个 runbook | §1 + §2 + §3 |
| 刚 ssh 进任意一台 | §2 |
| 要烟测一下环境 | §3.1 (B.0) |
| 4090 实例上要启 cora 大跑 | §3.5 (机器 A) |
| 80GB 实例上要启 arxiv 大跑 | §3.3 → §3.4 (机器 B；T1 必跑、T2/T3 deadline 富余才跑) |
| 全新 H800/H20，没有镜像 | §4 (fresh-clone) → 然后 §3 |
| nohup 跑了几秒就 fail / 5 cell 全挂 | §5.1 ⭐ |
| OOM / cache 错 / 各种红字 | §5 |
| 两机都跑完，要回收数据 | §6 |

---

## 1. 阶段总览

### 1.1 Phase 表

| Phase | 内容 | 哪台 | 估时 | yaml |
|---|---|---|---|---|
| **B.0** | sanity 烟测：cora + GIF + random + seed42 | 任意 | ~20s | `sanity_one_cell.yaml` |
| **B.1** | arxiv 5 GU method × random × seed42（feasibility baseline） | B | ~75-120 min | `phase_b_arxiv_feasibility.yaml` |
| **B.2-T1** | arxiv 3 method × 4 strategy × **seed=42** = 12 cell（**必跑**，paper Table 1 的 arxiv 列骨架） | B | ~6-8h | `phase_b_arxiv_T1_seed42.yaml` |
| **B.2-T2** | arxiv 同上 + **seed=212** = 12 cell（条件跑，给 n=2 误差棒） | B | ~7-8h | `phase_b_arxiv_T2_seed212.yaml` |
| **B.2-T3** | arxiv 同上 + **seed=722** = 12 cell（条件跑，n=3） | B | ~7-8h | `phase_b_arxiv_T3_seed722.yaml` |
| **B.3** | cora_GCN 6 method × 6 strategy × 5 seed = 180 cell（含 GraphRevoker；旧 5 method 已完成时只补 GraphRevoker） | A | ~4-6h | `phase_b_cora_gcn.yaml` |
| **B.4** | cora_GAT 同上 = 180 cell | A | ~4-6h | `phase_b_cora_gat.yaml` |
| **A.5-1** | cora/GCN ratio sweep r ∈ {0.01, 0.10, 0.20}，6 method × 3 strategy × 5 seed = 270 cell（必跑） | A | ~3-5h | `A5_ratio_*.yaml` |
| **A.5-2** | citeseer/GCN 两端 r ∈ {0.05, 0.20}，6 method × 3 strategy × 5 seed = 180 cell（**条件跑**） | A | ~1h | `A5_citeseer_r0.05.yaml`, `A5_citeseer_r0.20.yaml` |
| **A.6** | cora/GIN backbone ablation r=0.05，5 method × 3 strategy × 5 seed = 75 cell（**条件跑**） | A | ~1h | `A6_cora_gin_r0.05.yaml` |
| **A.3** | Alpha sweep（hybrid_alpha ∈ {0.00, 0.25, 0.75, 1.00}，0.50 复用主矩阵），cora/GCN + cora/GAT × 5 method × 5 seed = 200 cell（**条件跑**） | A | ~60-80 min | `A3_cora_{GCN,GAT}_alpha{0.00,0.25,0.75,1.00}.yaml` (8 yaml) |
| **A.7** | Cross-arch surrogate transferability（GCN↔GAT，仅 tracin/hybrid，复用 sister cell 选点）；**spec only，实现待定** | A | ~30min（实现后） | `A7_xfer_*.yaml` (TBD) |
| Prewarm（可选） | 跨 cell 共享 IF/IM 选择，B.2 前跑节省 alpha-sweep | B | ~50-100 min | — |

### 1.2 时长 & 显存参考（看这张表决定"是否合理"）

每 cell 平均成本，按 strategy/数据集分类：

| dataset | strategy | 时长（H800 80GB） | 时长（4090 24GB） | peak mem | 备注 |
|---|---|---|---|---|---|
| cora | 任意 | <1 min | <1 min | <4 GB | cora 全套都不挑卡 |
| arxiv | random | ~10 min | ~10 min | ~8 GB | selection 0.002s，瓶颈在 GU+retrain |
| arxiv | im (CELF) | ~3 min | ~3 min | ~8 GB | yaml 必须带 `candidate_fraction=0.1, mc_rounds=50` |
| arxiv | **tracin** | **~50-90 min** | ~81 min（已测） | **~68 GB** | **24GB 卡 OOM**；候选 = 全 train ~90K，逐节点 backward |
| arxiv | hybrid | ~50-90 min（首次） | ~81 min（首次） | ~68 GB | IF + IM 共用 ScoreCache，第二次同 (dataset, model, seed, ratio) 几秒回 |
| arxiv | retrain（collateral） | ~30s | ~22 GB peak | — | 24GB 卡边缘 OOM，必须走 80GB |

⚠ **TracIn 1.5h 是正常的**。`tracin_strategy.py:_compute_tracin_scores` 里候选数 = `train_mask` ≈ 90K，每个节点一次 backward retain_graph。Forward-once 优化（commit `6b7285b`）只把时间砍半（~3h → ~1.5h），mem 没变。要再压：yaml 加 `candidate_fraction=0.1` 限流（10× 加速，但改语义，论文要写）。

### 1.3 双机分工 & 数据合并

| 机器 | GPU | 角色 | 跑 |
|---|---|---|---|
| **A** | RTX 4090 24GB | cora workload | B.0 + B.3 + B.4 + A.5-1 (+ A.5-2 / A.6 / A.7 if 富余)（360 + 270 + 条件 180 + 条件 75 + 条件 ~50） |
| **B** | H800 / H20 / A100 ≥80GB | arxiv workload | B.0 + B.1 + **B.2-T1（必跑，12 cell ~6-8h）** + B.2-T2 + B.2-T3（条件跑） |

不冲突：各自写 `results/runs/{dataset}_*` 不同子目录。跑完 §6 各 tar 一份 scp 回本地合并。

**显存红线**（违反则不能跑该 cell）：
- arxiv tracin / hybrid → ≥80GB
- arxiv collateral retrain → ≥40GB（24GB 边缘 OOM）
- arxiv random / im → ≥16GB（24GB 也行）
- cora 全套 → 任意

---

## 2. 每次 ssh 都做的三步

```bash
# 1) 进实例
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master   # 或 ~/OpenGU/GULib-master 看部署位置

# 2) 进会话（Ctrl-b d 是 detach；Ctrl+C 之后会话还在）
tmux attach -t phaseB || tmux new -s phaseB

# 3) 同步 + 检查
unset http_proxy https_proxy
git pull --ff-only && git log --oneline -3
```

> **VSCode 用户**：`Ctrl-b` 被侧边栏拦截。先鼠标点 terminal 再按；或一次性把 prefix 改成 `Ctrl-a`：
> ```bash
> printf 'set -g prefix C-a\nunbind C-b\nbind C-a send-prefix\nset -g history-limit 50000\n' > ~/.tmux.conf
> tmux kill-server && tmux new -s phaseB
> ```

---

## 3. Phase 执行流程（按顺序）

> 全部 phase 都遵循同一个回路：**`yaml → run.py → gate_runs.py`**。
> `run.py` 吃 yaml 展开 (method, strategy, seed) 矩阵，每 cell 跑 `demo_attack` + `eval_collateral`，写四件 (`attack.json`, `collateral.json`, `predictions.npz`, `_meta.json`) 到 `results/runs/{cell}/seed{N}/`。
> `gate_runs.py` 自动 PASS/FAIL：4 件齐 + `mia_auc∈(0.001, 0.999)` + `collateral.perf_before∈[min,max]` + `gap` 是有限数。

### 3.1 B.0 — 烟测（任意机，~20s，每次大跑前必跑）

```bash
python experiments/run.py experiments/configs/sanity_one_cell.yaml 2>&1 | tee /tmp/b0.log
ls -la results/runs/cora_GCN_r0.05/GIF_random/seed42/   # 4 件齐？
python scripts/gate_runs.py experiments/configs/sanity_one_cell.yaml --f1-min 0.7
```

`gate exit 0` = 通过。FAIL → §5.1，**不要继续上 B.1+**。

> 关于 `gate_runs.py`：node task 下 `attack.json[results][strategy].f1_before` 常为 `None`（它来自 method `poison_f1`），gate 已绕开这个字段。`collateral.perf_before` 也只是当前 method 的 train-only before；对 GraphEraser/GraphRevoker 可能是 SISA/shard before。字段口径见 `self/dashboard/METRIC_FIELD_SEMANTICS.md`。

### 3.2 现在跑到哪了 — 实时计数

```bash
# B.0
ls results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json 2>/dev/null && echo B.0 done

# B.1（期望 5）
ls results/runs/ogbn-arxiv_GCN_r0.05/*_random/seed42/attack.json     2>/dev/null | wc -l
ls results/runs/ogbn-arxiv_GCN_r0.05/*_random/seed42/collateral.json 2>/dev/null | wc -l

# B.2-T1（期望 12 = 3 method × 4 strategy × seed42）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/attack.json | wc -l
# B.2-T2（条件跑后期望 +12，seed=212）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed212/attack.json | wc -l
# B.2-T3（条件跑后期望 +12，seed=722）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed722/attack.json | wc -l
# 总览（任意 seed）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json | wc -l

# B.3 / B.4（各期望 180）
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l
```

### 3.3 B.1 — arxiv random baseline（机 B，~75-120 min）

只 5 cell，random only。验三件：(a) refactor 后端到端通；(b) GU 方法在 169K 节点 arxiv 上不崩；(c) gate 的 f1 范围设对了。

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml \
    > logs/phase_b1_arxiv_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b1_arxiv.pid
echo "PID: $(cat logs/phase_b1_arxiv.pid)"

# 15s 后看是不是真起来了（不是 import 阶段秒挂）
sleep 15
ps -p $(cat logs/phase_b1_arxiv.pid) -o pid,etime,cmd
tail -30 logs/phase_b1_arxiv_*.log
nvidia-smi | head -12

# Ctrl-b d  detach 出 tmux
```

**或者交互式跑（前台 + tee，能盯着看）**：

```bash
mkdir -p logs
LOG=logs/phase_b1_arxiv_$(date +%Y%m%d_%H%M).log

# tmux 会话里前台跑，stdout 同时进 terminal 和 logfile
python -u experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml 2>&1 | tee "$LOG"

# 中途要走：Ctrl-b d  detach（任务继续跑），回来 tmux attach -t phaseB
# 真要停：tmux 里 Ctrl+C
```

`-u` 关 Python 输出 buffering，否则 tee 看不到实时进度。

> **nohup vs 交互式没本质区别**——cell-level checkpoint 在 `results/runs/`、ScoreCache / SelectionCache 在 autodl-fs 持久盘，tmux 死或实例重启都最多丢当前 mid-flight 那一个 cell，重 ssh + attach + 重跑同 yaml 自动跳过已完成的。**真正的风险是账户欠费实例被销毁**，这个 nohup 也救不了。任选。

跑完后：

```bash
bash scripts/diag_b1.sh   # 当前 cell 输出 + log 错误尾
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml --f1-min 0.55 --f1-max 0.85
```

> **如果 B.1 是从 4090 镜像继承过来的**（已有 5/5 attack 但 collateral 缺）：跳过上面 nohup，跑 §A.1 的 `redo_collateral.sh` 单补 collateral，~5 min 完事。
>
> **如果是 fresh-clone**（机器 B 上之前没跑过 attack）：上面 nohup 全跑，attack + collateral 一起出。两条路径**不要混用**——pre-refactor 的 attack 数据跟新代码混会污染。

### 3.4 B.2 — arxiv 主矩阵（机 B，分级跑 T1 必跑 → T2/T3 条件跑）

**前置**：B.0 PASS + B.1 PASS（5/5 attack + 5/5 collateral + gate exit 0）。

> 2026-05-06 决策：原 `phase_b_arxiv.yaml`（3 seed × 36 cell ≈ 21-24h on H800，每 seed 独立算 IF）压不进 ~24h deadline。拆成 T1/T2/T3 三个单 seed yaml，**串行执行，到 deadline 直接 kill**。已完成的 cell 都是 fingerprint-stamped 的（见 `experiments/run.py`），重跑安全。
>
> **Tier split 不省时间**——ScoreCache IF key 含 `seed`，T1 的 IF 分跨 seed 不命中。每 tier 独立 ~7-8h。意义在于"deadline 时永远有完整 n=1 / n=2 落盘"，而不是"后跑得越快"。
>
> 论文 fallback：T1 完成 = arxiv 列 n=1（无误差棒，cora n=5 做统计锚），T2 完成 = n=2（最低可见 spread），T3 完成 = n=3。

#### 3.4.1 T1（必跑，~6-8h，12 cell, seed=42）

paper Table 1 的 arxiv 列骨架。**这一段没跑完整个 arxiv 列就缺**。

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    > logs/phase_b_arxiv_T1_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b_arxiv_T1.pid
# Ctrl-b d
```

或交互式：

```bash
mkdir -p logs
LOG=logs/phase_b_arxiv_T1_$(date +%Y%m%d_%H%M).log
python -u experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml 2>&1 | tee "$LOG"
```

T1 预算（H800 80GB，12 cell）：
- 3 random × 10 min = 0.5h
- 3 im × 3 min = ~10 min
- 3 tracin × ~50 min = 2.5h（首次填 ScoreCache）
- 3 hybrid × ~5 min = ~15 min（命中 tracin 的 ScoreCache + im 的 SelectionCache）
- GU+retrain+MIA per cell ~20 min × 12 = 4h
- **total ~7-8h**，¥50-100

T1 跑完 gate：

```bash
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T1_seed42.yaml --f1-min 0.55 --f1-max 0.85
```

T1 PASS → §3.4.2 T2；FAIL → §5.

#### 3.4.2 T2（条件跑，仅在 T1 完成且 deadline 富余 ≥6h 时启）

```bash
nohup python experiments/run.py experiments/configs/phase_b_arxiv_T2_seed212.yaml \
    > logs/phase_b_arxiv_T2_$(date +%Y%m%d_%H%M).log 2>&1 &
```

T2 预算 **~7-8h**，**和 T1 同价**——`tracin_strategy.py:_build_cache_config` 的 IF cache key 含 `seed`，T1 的 IF 分跨 seed 不命中。分级 split 只是 deadline 安全停点，不省时间。

跑完 gate：

```bash
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T2_seed212.yaml --f1-min 0.55 --f1-max 0.85
```

#### 3.4.3 T3（条件跑，仅在 T2 完成且 deadline 富余 ≥5h 时启）

```bash
nohup python experiments/run.py experiments/configs/phase_b_arxiv_T3_seed722.yaml \
    > logs/phase_b_arxiv_T3_$(date +%Y%m%d_%H%M).log 2>&1 &
```

预算 **~7-8h**（同 T1/T2，无跨 seed 复用）。跑完 gate 同 §3.4.2。

#### 3.4.4 一键串（T1 必跑 + T2/T3 富余跑）

把三段 yaml 串成一条 nohup —— deadline 到时 `kill` 整条，已完成的 cell 都已落盘，没完成的下次 `--force` 再续：

```bash
nohup bash -c '
python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T1_seed42.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv_T2_seed212.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T2_seed212.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv_T3_seed722.yaml
' > logs/h800_b2_chain_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/h800_b2_chain.pid
# Ctrl-b d
```

`&&` 链断点保护：T1 gate FAIL 不会浪费 GPU 跑 T2/T3。

#### 3.4.5 监控

```bash
tail -f logs/phase_b_arxiv_T*_*.log
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/attack.json  | wc -l   # T1 进度，→ 12
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed212/attack.json | wc -l   # T2，→ 12
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed722/attack.json | wc -l   # T3，→ 12
grep -c "ScoreCache.*HIT\|SelectionCache.*HIT" logs/phase_b_arxiv_T*_*.log
nvidia-smi
```

#### 3.4.6 deadline 临近怎么办

到 deadline 还在 T2 / T3 中途：直接 `kill $(cat logs/h800_b2_chain.pid)`。**已写盘的 cell 不会被破坏**（`run.py` 写文件是分步原子操作，`_meta.json` 最后写；中断 cell 会被 `cell_status` 判为 `incomplete` 或 `corrupt`，下次 run 自动跳过 / 续跑）。

paper 写法对应 §3.4 的 fallback 表：T1=n=1、T1+T2=n=2、全完=n=3。

### 3.5 B.3 + B.4 — cora（机 A，串行 ~7-12h；如旧 5 method 已完成则只补 GraphRevoker）

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs

# 串行：GCN 完了直接接 GAT
nohup bash -c '
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml && \
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
' > logs/cora_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/cora_full.pid
# Ctrl-b d
```

**或者交互式（tmux 前台 + tee）**：

```bash
mkdir -p logs
LOG=logs/cora_full_$(date +%Y%m%d_%H%M).log
{ python -u experiments/run.py experiments/configs/phase_b_cora_gcn.yaml && \
  python -u experiments/run.py experiments/configs/phase_b_cora_gat.yaml && \
  python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
  python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml; } 2>&1 | tee "$LOG"
# Ctrl-b d 中途 detach
```

cora 全跑 ~6-10h，想盯实时输出选这条；checkpoint 同样在持久盘，断了重跑跳过已完成。

监控：

```bash
tail -f logs/cora_full_*.log
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l   # → 180
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l   # → 180
```

GraphRevoker 说明：B.3/B.4 yaml 通过 `method_overrides` 只给 GraphRevoker 注入
`--partition_method gpa`；GIF/GNNDelete/MEGU/IDEA/GraphEraser 的 fingerprint 不受
新增方法影响，已完成 cell 会继续 skip。GraphRevoker 的 TracIn/Hybrid 必须命中
已有 SelectionCache（通常由先前 5-method 主矩阵中的 GIF/GNNDelete 产生）；若缺
cache，runner 会 fail fast，而不是用 GraphRevoker 的 shard/SISA train_only 模型算梯度。

### 3.6 A.5 — Ratio Ablation（机 A，分两阶段）

**何时跑**：B.3 (cora_GCN main matrix) 完成后。给 paper §A.5 提供 deletion-ratio elasticity 切片。
**为何分阶段**：deadline 紧；先 cora 取最小可发表切片，citeseer 留作富余时的 reviewer 对冲（防"single-dataset elasticity"质疑）。
**Spec**：`experiments/configs/A5_README.md`（已存在，含 ratio 网格 + caveat）。

#### Phase 1 — cora/GCN 全 sweep（必跑，~3-5h，270 cell）

r ∈ {0.01, 0.05, 0.10, 0.20}。**r=0.05 直接复用 B.3 主矩阵 cell（不重跑）**，新增 r ∈ {0.01, 0.10, 0.20} = 3 ratio × 6 method × 3 strategy（random/im/tracin）× 5 seed = 270 cell。

⚠ **r=0.20 在 GraphEraser/GraphRevoker 上可能因 shard 失衡崩**（A5_README §Caveats）。先单 cell 烟测：

```bash
python experiments/run.py experiments/configs/A5_ratio_0.20.yaml --limit 1 \
    2>&1 | tee /tmp/a5_r020_smoke.log
```

崩了 → yaml 删掉 GraphEraser/GraphRevoker 那两行，paper §A.5 caveat 写"shard 系在 r=0.20 budget 下崩，drop"。烟测 PASS 后串行三 ratio：

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs
nohup bash -c '
python experiments/run.py experiments/configs/A5_ratio_0.01.yaml && \
python experiments/run.py experiments/configs/A5_ratio_0.10.yaml && \
python experiments/run.py experiments/configs/A5_ratio_0.20.yaml
' > logs/A5_cora_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/A5_cora.pid
# Ctrl-b d
```

监控：

```bash
tail -f logs/A5_cora_*.log
ls results/runs/cora_GCN_r0.01/*/seed*/attack.json | wc -l   # → 90
ls results/runs/cora_GCN_r0.10/*/seed*/attack.json | wc -l   # → 90
ls results/runs/cora_GCN_r0.20/*/seed*/attack.json | wc -l   # → 90
```

#### Phase 2 — citeseer 两端（条件跑，~1h，180 cell）

**触发条件**：Phase 1 完成 + paper deadline 富余 ≥1h。**不满足就跳过**，§A.5 写"single-dataset elasticity; multi-dataset 留 future work"——这是 §limitation 不是致命缺陷。

**最小切片**：citeseer/GCN × r ∈ {0.05, 0.20}（只取曲线两端验形状一致）× 6 method × 3 strategy × 5 seed = 180 cell。

**前置**：yaml 已建好（与 cora 配置一致，仅换 `dataset` + `ratio`）：
- `experiments/configs/A5_citeseer_r0.05.yaml`
- `experiments/configs/A5_citeseer_r0.20.yaml`

如 Phase 1 r=0.20 烟测删了 shard 系（GraphEraser/GraphRevoker），citeseer r=0.20 yaml 同步删。

```bash
nohup bash -c '
python experiments/run.py experiments/configs/A5_citeseer_r0.05.yaml && \
python experiments/run.py experiments/configs/A5_citeseer_r0.20.yaml
' > logs/A5_citeseer_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/A5_citeseer.pid
```

监控：

```bash
ls results/runs/citeseer_GCN_r0.05/*/seed*/attack.json | wc -l   # → 90
ls results/runs/citeseer_GCN_r0.20/*/seed*/attack.json | wc -l   # → 90
```

#### 数据回收（合到 §6 流程）

A.5 输出在 `results/runs/cora_GCN_r{0.01,0.10,0.20}/` 和 `results/runs/citeseer_GCN_r{0.05,0.20}/`，§6 的机器 A tar 命令需相应扩展（见 §6 修订）。

---

### 3.7 A.6 — Backbone Ablation（机 A，**条件跑**，~1h）

**何时跑**：B.3/B.4 + A.5-1 完成后，若 paper deadline 富余 ≥1h。
**目的**：reviewer 对冲——证攻击不挑 message-passing aggregator（GCN mean / GAT attention 之外，GIN 用 sum）。
**最小切片**：cora/GIN × r=0.05 × 5 method × 3 strategy（random/im/tracin）× 5 seed = 75 cell。

**前置**：yaml 已建好 `experiments/configs/A6_cora_gin_r0.05.yaml`。如需扩 SAGE，复制改 `base_model: SAGE` 即可（model_zoo 已注册，无需额外参数）。

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs

# 单 cell 烟测（GIN 在 cora 上没跑过，先验环境）
python experiments/run.py experiments/configs/A6_cora_gin_r0.05.yaml --limit 1 \
    2>&1 | tee /tmp/a6_gin_smoke.log

# 烟测 PASS 后全量
nohup python experiments/run.py experiments/configs/A6_cora_gin_r0.05.yaml \
    > logs/A6_cora_gin_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/A6_cora_gin.pid
# Ctrl-b d
```

监控：

```bash
ls results/runs/cora_GIN_r0.05/*/seed*/attack.json | wc -l   # → 75
```

**跳过的写法**：paper §A.6 写 "Backbone ablation (GIN/SAGE) deferred; main results on GCN + GAT cover mean-aggregator and attention-aggregator paradigms"——这是 §limitation 措辞，不致命。

#### 数据回收（合到 §6）

`results/runs/cora_GIN_r0.05/`，§6 机 A tar 命令需追加（已在 §6 备注列出）。

---

### 3.7b A.3 — Alpha Sweep（机 A，**条件跑**，~60-80 min）

**何时跑**：B.3/B.4 (cora 主矩阵) 完成后，paper deadline 富余 ≥1h。
**目的**：扫 hybrid_alpha ∈ {0.00, 0.25, 0.75, 1.00} 看 IF/IM 融合权重的曲线形状。0.50 在主矩阵已有，自动跳过。
**Spec**：`experiments/configs/A3_alpha_sweep_SPEC.md`（standing; 2026-05-06 实现完成）

**前置**：B.3 + B.4 PASS。`feat/a3-alpha-sweep` merge 进 main 之后，老 ResultCache 全失效（key 加了 5 个字段），不要在 B.x 跑中途 pull。

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs

# 8 yaml 串行（4 alpha × 2 backbone）。每 yaml 25 cell，每 cell ~30s
nohup bash -c '
for yaml in experiments/configs/A3_cora_GCN_alpha0.00.yaml \
            experiments/configs/A3_cora_GCN_alpha0.25.yaml \
            experiments/configs/A3_cora_GCN_alpha0.75.yaml \
            experiments/configs/A3_cora_GCN_alpha1.00.yaml \
            experiments/configs/A3_cora_GAT_alpha0.00.yaml \
            experiments/configs/A3_cora_GAT_alpha0.25.yaml \
            experiments/configs/A3_cora_GAT_alpha0.75.yaml \
            experiments/configs/A3_cora_GAT_alpha1.00.yaml; do
    python experiments/run.py "$yaml"
done
' > logs/A3_alpha_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/A3_alpha.pid
```

监控：

```bash
ls results/runs/cora_GCN_r0.05/*_hybrid_alpha*/seed*/attack.json | wc -l   # → 100 (5 method × 4 alpha × 5 seed)
ls results/runs/cora_GAT_r0.05/*_hybrid_alpha*/seed*/attack.json | wc -l   # → 100
```

**跳过的写法**：paper §A.3 写 "Alpha sweep deferred; main matrix's hybrid (alpha=0.5) is reported. The fusion-weight elasticity is left to future work."

#### 数据回收（合到 §6）

`results/runs/cora_GCN_r0.05/*_hybrid_alpha*/` + `results/runs/cora_GAT_r0.05/*_hybrid_alpha*/`。§6 机 A tar 默认 glob 已经覆盖（基于 `cora_*_r0.05/` 全包），无需追加。

---

### 3.8 A.7 — Cross-arch Surrogate Transferability（**设计稿，实现待定**）

> 状态：spec only。代码未写，yaml 未建。下面是设计书面化，时间富余再实现。
> 设计动机：见与 reviewer 对话——TracIn/Hybrid 是 model-coupled 唯一两条策略，"换架构是不是天然防御"是 reviewer 必问；同时若转移率高，threat model 升级到"无需白盒访问受害者"，contribution 更硬。

#### 3.8.1 设计目标

复用已跑出来的 sister cell（如 `cora_GCN_r0.05/{method}_tracin/seed42/`）里的 `selected_nodes`，**跳过昂贵的 selection 步骤**，把这些节点注入到不同 backbone 的 pipeline 跑 unlearn + retrain，得到 cross-arch effect。

约束：
- **必须同 dataset、同 ratio、同 seed**——node id 跨 dataset 无意义；同 seed 保证 GU 训练划分一致，差异只来自 backbone
- 仅对 `requires_trained_model=True` 的策略有意义（tracin、hybrid）
- 4 件输出文件命名加后缀 `_xfromGCN` / `_xfromGAT` 与 native cell 物理隔离

#### 3.8.2 Yaml schema 草稿

```yaml
# experiments/configs/A7_xfer_GCN_to_GAT.yaml
name: A7_xfer_GCN_to_GAT
dataset: cora
ratio: 0.05

# 受害者 backbone（实际跑 unlearn + retrain 的）
target_base_model: GAT

# 攻击者代理 backbone（提供 selected_nodes 的 sister cell）
source_base_model: GCN

methods:
  - GIF
  - GNNDelete
  - MEGU
  - IDEA
  - GraphEraser

strategies:
  - tracin
  - hybrid    # 视 source cell 是否有 hybrid 数据决定

seeds: [42, 212, 722, 1337, 2024]

defaults:
  save_predictions: true
  run_collateral: true
  num_epochs: 100
  batch_size: 64
  cuda: 0
```

对称 yaml `A7_xfer_GAT_to_GCN.yaml` 把 source / target 反过来即可。

#### 3.8.3 Runner 草稿（`experiments/run_transfer.py`，~80 行）

伪代码：

```python
# 1. 读 yaml + 展开 (method, strategy, seed) 矩阵
for method, strategy, seed in expand_matrix(cfg):
    # 2. 读 sister cell 的 attack.json 拿 selected_nodes
    src_path = f"results/runs/{cfg['dataset']}_{cfg['source_base_model']}_r{cfg['ratio']}/" \
               f"{method}_{strategy}/seed{seed}/attack.json"
    src_data = json.load(open(src_path))
    selected_nodes = src_data["results"][strategy]["selected_nodes"]   # List[int]

    # 3. 调 demo_attack 的"借选点"模式（见 3.8.4 demo_attack 改动）
    out_dir = f"results/runs/{cfg['dataset']}_{cfg['target_base_model']}_r{cfg['ratio']}/" \
              f"{method}_{strategy}_xfrom_{cfg['source_base_model']}/seed{seed}/"
    subprocess.run([py, "demo_attack.py",
                    "--dataset_name", cfg["dataset"],
                    "--base_model", cfg["target_base_model"],
                    "--unlearning_methods", method,
                    "--strategies", strategy,
                    "--unlearn_ratio", str(cfg["ratio"]),
                    "--seed", str(seed),
                    "--selected_nodes_file", src_path,        # NEW
                    "--strategy_label_suffix", f"_xfrom_{cfg['source_base_model']}",  # NEW
                    "--save_path", out_dir + "attack.json",
                    ...])
    # 4. eval_collateral 同样跑（不需要改，selected_nodes 已注入磁盘文件）
```

skip-if-exists、git_sha audit、`_meta.json` 都复用 `run.py` 的工具函数（重构成 `experiments/_runner_lib.py` 共享）。

#### 3.8.4 demo_attack.py 需加的两个 flag

| flag | 行为 |
|---|---|
| `--selected_nodes_file <path>` | 读 path 里 `results[<strategy>][selected_nodes]`，绕过 `manager.compare_strategies` 内部的 `strategy.select_nodes`，直接调 `pipeline.run_with_selected_nodes(...)`。`pipeline_adapter.py:336` 已现成支持 |
| `--strategy_label_suffix <str>` | 写 attack.json 时给 strategy_name 加后缀（如 `tracin_xfrom_GCN`），保证下游 metric aggregator 能区分 native vs cross-arch |

实现量：~30 行 python 改 demo_attack.py + ~80 行新 `run_transfer.py` + 2 yaml + 一份 sanity 烟测。**估 1.5-2h 实现 + 30min 烟测**。

#### 3.8.5 Sanity 检查（实现后必跑）

```bash
# A7-0: 借自己的选点跑自己（应得到与 native cell 完全一致的结果，验证 plumbing）
python experiments/run_transfer.py experiments/configs/A7_xfer_self_GCN.yaml --limit 1
# 输出应满足：mia_auc / f1_after / gap 与 cora_GCN_r0.05/GIF_tracin/seed42 native 相同
```

#### 3.8.6 跑（实现 + sanity PASS 后）

```bash
nohup bash -c '
python experiments/run_transfer.py experiments/configs/A7_xfer_GCN_to_GAT.yaml && \
python experiments/run_transfer.py experiments/configs/A7_xfer_GAT_to_GCN.yaml
' > logs/A7_xfer_$(date +%Y%m%d_%H%M).log 2>&1 &
```

成本：5 method × 2 strategy × 5 seed × 2 方向 = 100 cell，但 **selection 全 cache hit（直接从 sister cell 复制 selected_nodes，0s）**，只跑 unlearn + retrain ≈ 单 cell 30s × 100 ≈ ~50min。

#### 3.8.7 不实现的兜底（paper 里写法）

§A.7 future work 一段：

> "Our threat model assumes the attacker has white-box access to the victim's model architecture and weights for gradient-based strategies (TracIn, Hybrid). A natural defense is architecture obfuscation: if the attacker's surrogate is structurally different from the victim, transferability may degrade. We leave a systematic cross-architecture transferability study to future work."

reviewer 戳就是 §limitation，不致命。

#### 数据回收

新增子目录 `results/runs/{dataset}_{target_arch}_r{ratio}/{method}_{strategy}_xfrom_{source_arch}/`，§6 tar 命令需追加（已在 §6 备注列出）。

---

### 3.9 Prewarm — 何时跑（可选，机 B）

`scripts/prewarm_selection_cache.py` 把跨 cell 共享的 selection 提前算到 `results/selection_cache/` 和 `results/score_cache/`。2026-05-06 审核后要求：TracIn/Hybrid prewarm 必须通过 GIF/GNNDelete 这类 canonical full-model method 训练 selector；脚本已在 shard/SISA method 上 fail fast。

**何时值得跑**：
- 计划做 hybrid alpha-sweep（5+ alpha 值同一 (dataset, model, seed, ratio)）→ 跑一次 prewarm，sweep 阶段每 alpha < 1 min
- 跨 strategy / 跨 method 但同 IF 输入 → 第一次填，后续 cell 命中

**何时不跑**：B.2 yaml 的 36 cell 各 (method, strategy, seed) 不同，prewarm 帮不上多少（除非 IF cache key 复用）。直接 §3.4 nohup 让 run.py 自己 lazy 算。

如果要跑：

```bash
python scripts/prewarm_selection_cache.py experiments/configs/phase_b_arxiv_T1_seed42.yaml \
    --strategies tracin,im
# 之后再跑 §3.4 的 B.2/T1 全矩阵，GraphEraser 的 tracin/hybrid cell 必须命中 SelectionCache
```

ScoreCache key 故意不含 model_fingerprint（`tracin_strategy.py:115-133` 的 docstring 写了 why：跨进程 cuDNN 1e-5 权重漂移会让 fingerprint 失效，丢命中率 → 改用 (dataset, model, seed, ratio) 静态 key）。

---

## 4. 全新机器初始化

### 4.1 优先：从镜像复用（~10 min）

老实例上：autodl 控制台 → 实例 → 更多操作 → 保存镜像（~10-30 min，~¥0.3-0.5/天存储）。

新实例：创建实例 → 选 H800 80G → 镜像 → 我的镜像。

⚠ **GPU 选型**：
- ✅ H800 80GB / A100 80GB（sm_90，cu118 PyTorch 2.1.2 OK）
- ✅ H20 96GB（cu118 不一定认 sm_90，必要时 cu121；算力 ~H800 1/3，B.2 拉到 ~38-40h）
- ❌ PRO 6000（Blackwell sm_100，cu118 不支持）
- ❌ vGPU / A6000 48GB（tracin 68GB peak 不够）

### 4.2 备用：fresh-clone（无镜像或代码大改）

```bash
ssh ...new-instance
source /etc/network_turbo
cd ~

# Phase B 已 merge 进 main（2026-05-06，commit b3181db）。直接 clone main，
# 不要再用旧的 -b nips-prep（origin/nips-prep 停在 pre-Phase-B 状态）。
git clone https://github.com/lelelelelelelelelelelelele/OpenGU.git
cd OpenGU/GULib-master
git log --oneline -3   # 期望看到 b3181db Merge branch 'fix/blocker-1-train-before-select'

# autodl PyTorch 镜像默认 2.1.2+cu118，先验
python -c "import torch; print(torch.__version__, 'cuda:', torch.cuda.is_available())"
# 期望: 2.1.2+cu118 cuda: True

# 装 PyG 扩展
pip install torch_scatter==2.1.2 torch_sparse==0.6.18 \
    -f https://data.pyg.org/whl/torch-2.1.2+cu118.html
pip install -r requirements.txt

# 自检
python -c "
import torch, torch_geometric, torch_scatter, torch_sparse, ogb, yaml
print('torch:', torch.__version__, '| cuda:', torch.cuda.is_available())
print('GPU:', torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
torch.zeros(1).cuda(); print('alloc ok')
"

which tmux || apt update && apt install -y tmux
tmux new -s phaseB
```

> torch 不是 2.1.2+cu118 → wheel URL 切到对应版本（如 `torch-2.3.0+cu121.html`）。
> GitHub 慢 → `git clone --depth 1` 或加 `https://ghproxy.com/` 前缀。

### 4.3 完了 → §3.1 跑 B.0 验证

B.0 PASS 才往下跑 B.1+。FAIL 不继续。

---

## 5. 故障处理

### 5.1 nohup 全 5 cell 几秒就挂 ⭐

**症状**：log 里 `failed_attack: 5/5` + 各 cell `elapsed: <30s`，attack.json 一个都没出。

**含义**：子进程在 import / argparse / 早期 segfault 阶段挂了，nohup buffer 把 traceback 吞了。

**回滚流程**：

```bash
# 1) kill 跑飞的
ps -ef | grep -E "run\.py" | grep -v grep
kill <PID>; pkill -f "experiments/run.py"

# 2) 前台跑一个 cell 拿真 traceback（路径与 nohup 一致）
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml --limit 1

# 3) 还看不出 → 直接调 demo_attack（最薄，对照 yaml 看 args）
python demo_attack.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --unlearning_methods GIF --strategies random \
    --unlearn_ratio 0.05 --seed 42 \
    --num_epochs 200 --batch_size 256 --cuda 0 \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --save_path /tmp/test_attack.json

# 4) 修好之后回 nohup（别在前台跑全 5 cell，shell 一断又重来）
```

### 5.2 OOM / GPU 错

| 症状 | 处理 |
|---|---|
| `CUDA out of memory` 在 retrain 阶段 | 24GB 卡跑 arxiv collateral，必出。切 80GB 卡或 `--gcn_hidden 128` 降配（会改 baseline，论文一致性要管） |
| `CUDA out of memory` 在 tracin selection | <80GB 卡跑 tracin。切 H800/A100 80GB，或 yaml 加 `candidate_fraction=0.1` 限流 |
| `no kernel image is available` | GPU 架构 PyTorch 不支持（Blackwell sm_100 + cu118）。换 H800/A100，或 PyTorch 2.4+cu124 |
| `ImportError: torch_scatter` | wheel mismatch，按 §4.2 装回去 |

### 5.3 Cache 污染 / mia_auc 异常

```bash
# mia_auc=0.0 或 =1.0 → cache 污染或老 bug
find results/cache results/selection_cache results/score_cache \
    \( -name '*.json' -o -name '*.npz' \) -delete

# 别碰：results/runs/（实验输出）、data/processed/（dataset split）
```

### 5.4 速查

| 现象 | 处理 |
|---|---|
| 4090 跑 B.2 没看到 `[SelectionCache] HIT` | cache 没解压或路径错。根目录 `tar xzf selection_cache.tar.gz` |
| B.1 全 5 cell `mia_auc` 同值 | dispatcher / cache key bug。`python scripts/diag_mia_dup.py` |
| `git pull --ff-only` 报 conflict | 远端推了新代码本地有 patch。`git stash && git pull && git stash pop` |
| SSH 断了 | tmux 会话 + 进程不受影响（tmux 守在服务器端），重 ssh + `tmux attach -t phaseB` 接着看 |
| tmux 找不到会话（实例真重启过） | 所有会话清零，但 cell-level checkpoint 在 `results/runs/`、cache 在 autodl-fs 持久盘。`tmux new -s phaseB` 重起，重跑同 yaml 自动跳过完成的 cell |
| autodl 实例显示运行中但 ssh 不上 | 网络抽风。等几分钟或控制台"重启实例"——重启会杀 tmux + 进程，但持久盘数据还在，按上一行处理 |
| 磁盘满 | `du -sh results/*`；arxiv 单 cell ~140K × 36 + npz 大头，总 ~10GB |
| 翻不到 OOM 日志 | tmux 默认 history 2000 行。`set -g history-limit 50000` 或 `tee /tmp/log.txt` |

紧急停止任务：

```bash
ps -ef | grep -E "run\.py|prewarm" | grep -v grep
kill <PID>             # 优雅
kill -9 <PID>          # 不响应再这样
pkill -f "experiments/run.py"
```

---

## 6. 数据回收（两机都跑完之后）

机器 A：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
# B.3/B.4 主矩阵 + A.5 Phase 1 (cora ratio sweep)
tar czf cora_results.tar.gz \
    results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05 \
    results/runs/cora_GCN_r0.01 results/runs/cora_GCN_r0.10 results/runs/cora_GCN_r0.20
# 若 A.5 Phase 2 也跑了，追加 citeseer：
# tar czf cora_results.tar.gz ... results/runs/citeseer_GCN_r0.05 results/runs/citeseer_GCN_r0.20
# 若 A.6 backbone ablation 也跑了，追加 GIN：
# tar czf cora_results.tar.gz ... results/runs/cora_GIN_r0.05
# 若 A.7 cross-arch transferability 实现并跑了：
# tar czf cora_results.tar.gz ... results/runs/cora_GAT_r0.05/*_xfrom_GCN \
#                                  results/runs/cora_GCN_r0.05/*_xfrom_GAT
ls -lh cora_results.tar.gz
```

机器 B：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
tar czf arxiv_results.tar.gz results/runs/ogbn-arxiv_GCN_r0.05
ls -lh arxiv_results.tar.gz
```

本地 PowerShell：

```powershell
scp 4090-host:~/autodl-fs/OpenGU/GULib-master/cora_results.tar.gz H:\project\OpenGU\GULib-master\
scp h800-host:~/autodl-fs/OpenGU/GULib-master/arxiv_results.tar.gz H:\project\OpenGU\GULib-master\
cd H:\project\OpenGU\GULib-master
tar xzf cora_results.tar.gz
tar xzf arxiv_results.tar.gz
```

通知 "phase B 数据回来了" → 进 Phase C（figure / Table 1 / abstract refresh）。

---

## 附录 A — 一次性脚本

### A.1 redo_collateral.sh（B.1 缺 collateral 时单补）

```bash
cat > scripts/redo_collateral.sh << 'EOF'
#!/bin/bash
EXTRA="--num_epochs 200 --batch_size 256 --gcn_num_layers 3 --gcn_hidden 256"
for method in GIF GNNDelete IDEA GraphEraser MEGU; do
    out="results/runs/ogbn-arxiv_GCN_r0.05/${method}_random/seed42"
    if [ -f "$out/collateral.json" ] && [ "$(du -k "$out/collateral.json" | cut -f1)" -gt 0 ]; then
        echo "[skip] $method"; continue
    fi
    echo "[run] $method"
    python eval_collateral.py \
        --dataset_name ogbn-arxiv --base_model GCN \
        --unlearning_methods $method --strategies random \
        --unlearn_ratio 0.05 --random_seed 42 \
        --cuda 0 --save_predictions \
        --output_dir "$out" \
        $EXTRA 2>&1 | tee -a /tmp/redo_collateral.log
done
EOF
chmod +x scripts/redo_collateral.sh
bash scripts/redo_collateral.sh
```

H800 上 5 cell 共 ~2-5 min。

### A.2 显存外推探针

```bash
python scripts/feasibility_selection_only.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --candidate_subset_size 1000 --strategies tracin
```

输出 peak_mem(MB)。subset=1000 时 ~5.9 GB，外推全量 N=135474 → ~68 GB peak（**注意：脚本默认线性外推会输出 "OOM 785 GB" 之类吓人数字，那是 forward 固定开销被错误线性外推；真值 ~68 GB**）。

### A.3 机器 B 一键串：B.1 补 + B.2 T1→T2→T3

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs
nohup bash -c '
bash scripts/redo_collateral.sh && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv_T1_seed42.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T1_seed42.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv_T2_seed212.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T2_seed212.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv_T3_seed722.yaml
' > logs/h800_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/h800_full.pid
```

deadline 到时 `kill $(cat logs/h800_full.pid)` —— 已落盘 cell 不损，未完成的下次 `run.py` 续跑（fingerprint 保护）。

### A.4 监控命令汇总

```bash
# 实时日志
tail -f logs/<name>.log

# cache 命中率
grep -cE "ScoreCache.*HIT|SelectionCache.*HIT|ResultCache.*HIT" logs/<name>.log

# 进度计数
ls results/runs/<dataset>_<model>_r<ratio>/*/seed*/attack.json | wc -l

# 资源
nvidia-smi
watch -n 2 nvidia-smi
df -h ~
du -sh results/
```

---

## 附录 B — 各 cell 内部时序

调试卡死位置必看 `self/attack_flow.md`。每 cell 大致：
1. base train（CPU+GPU 满，~1-3 min on arxiv）
2. selection（strategy 决定，详见 §1.2 表）
3. unlearn（GU 方法决定，~1-15 min）
4. retrain from scratch（peak mem 在这，~30s on H800 / OOM on 4090 for arxiv）
5. MIA（CPU bound，~6 min × 2 rounds for GraphEraser；GPU idle）
6. 写 4 件 + collateral.json
