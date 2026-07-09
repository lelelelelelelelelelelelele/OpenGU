---
title: 重跑与缓存修复 Runbook
created: 2026-07-09
updated: 2026-07-09
type: repair-runbook
tags: [runbook, cache, rerun, graphrevoker, tracin]
---

# 重跑与缓存修复 Runbook

这页处理一种具体事故：某个 method / selector / config 跑出来了，但后来发现实现或设置有问题，必须判断哪些结果还能用、哪些 cache 要清、哪些矩阵要重跑。

配套页：

- cache / result 分层：[[14_Cache与结果层级]]
- 正式运行入口、yaml、`.sh` 包装：[[15_实验运行入口与脚本]]

> 核心规则：先判定故障属于 **method 线** 还是 **selector 线**。不要一上来全删 cache。

---

## Run + Modify 闭环

如果某个设置报错或结果不能用，允许进入“改 + 跑”的闭环，但每一步都要留痕：

```mermaid
flowchart LR
  A[发现异常] --> B[判定 method 线 / selector 线]
  B --> C[标 produced but not usable]
  C --> D[最小代码或 config 修改]
  D --> E[清对应 cache / state]
  E --> F[sanity run]
  F --> G[gate / inspect outputs]
  G --> H[扩大 rerun]
  H --> I[同步 WORKPLAN / config_inventory / OB]
```

| 步骤 | 要求 |
|---|---|
| 改代码 | 只改触发故障的最小范围；不要顺手重构无关模块 |
| 改 yaml | 写清楚为什么改 method / strategy / seed / ratio |
| 清 cache | 先按 [[14_Cache与结果层级]] 判定层级；不要全删 |
| 小跑 | 先 `--limit 1` 或 sanity yaml，别直接开全矩阵 |
| gate | 至少确认四件产物齐、指标 finite、F1 区间合理 |
| 同步 | `WORKPLAN`、`config_inventory`、`VALIDATION_LOG`、OB 页一起更新 |

---

## 快速分流

| 故障 | 类型 | 受影响结果 | 不受影响结果 | 关键 cache |
|---|---|---|---|---|
| GraphRevoker 聚合器 / dispatcher / 方法实现错误 | GU method 线 | 所有 `GraphRevoker_*` cells | 其他 GU methods；同一 selector 在其他 method 上的选点 | method state + GraphRevoker result outputs |
| TracIn 定义不匹配 | selector 线 | `*_tracin` 和 `*_hybrid` cells | random / degree / pagerank / IM；非 TracIn 分支 | `score_cache/if` + TracIn/Hybrid selection cache |

原则：

- GraphRevoker 出错：选点策略本身通常没错，别清 `selection_cache` / `score_cache` 的 IM、degree、pagerank。
- TracIn 出错：GU method 本身通常没错，别重跑 random / degree / pagerank / IM。
- `results/cache/` 是完整 attack metrics；`results/selection_cache/` 是选点；`results/score_cache/if/` 是 TracIn 分数。
- `--no_cache` 只用于定位问题，不作为正式重跑默认选项。

---

## Cache 层级

| 层 | 路径 | 存什么 | 什么时候清 |
|---|---|---|---|
| ResultCache | `results/cache/` | 旧 pipeline 的完整 cell metrics | metric / method / selector 输出已污染时，清对应配置；不要手改 hash 文件 |
| Phase B outputs | `results/runs/<cell>/<method>_<strategy>/seed*/` | 当前主矩阵 attack / collateral / predictions / meta | 对应 cell 不能用时，重跑或标 rerun |
| SelectionCache | `results/selection_cache/` | selector 选出的节点 ID | selector 算法或节点语义变了才清 |
| ScoreCache IF | `results/score_cache/if/` | TracIn per-candidate score | TracIn 公式、eval/query loss、梯度定义变了必须清 |
| ScoreCache IM | `results/score_cache/im*/` | IM spread / CELF | GraphRevoker 或 TracIn 修复不应清 |
| Method state | `data/<Method>/` | 方法自己的 partition/checkpoint/中间状态 | GU method 实现、聚合器、架构维度或磁盘状态污染时清对应 method |

---

## GraphRevoker 修复线

### 触发条件

- GraphRevoker cell 的 `perf_before` 明显退化，例如落到 `0.50-0.58`，不像同配置其他 method。
- 日志里出现 GraphRevoker aggregator / partition 相关异常，例如 `opt_dataset.py:17`。
- 旧数据来自 dispatcher alias：`"GraphRevoker"` 实际跑成 `grapheraser`。
- GraphRevoker 结果已 produced，但不能当 usable evidence。

### 受影响范围

| 范围 | 决策 |
|---|---|
| `GraphRevoker_*` 主矩阵结果 | 全部标 rerun，修后整 method 重跑 |
| GraphRevoker k=5 baseline | 如果来自 dispatcher 修复前，也标 rerun |
| 其他 method 的 random / degree / pagerank / IM / TracIn | 不受 GraphRevoker 方法 bug 影响 |
| selection cache | 不清，除非同时改了 selector |
| score cache | 不清，除非同时改了 TracIn / IM |

### 修复步骤

1. 确认 dispatcher 走真实 GraphRevoker。
   - 文件：`unlearning_manager.py`
   - 期望：`"GraphRevoker"` 指向 `graphrevoker`，不是 `grapheraser`。

2. 修复 GraphRevoker 聚合器 / partition 报错。
   - 已知关注点：`opt_dataset.py:17`、GraphRevoker 自己的 partition / aggregator / trainer 调用链。
   - 修完先跑最小 sanity，不直接开全矩阵。

3. 清对应 method state。
   - 优先只处理 `data/GraphRevoker/` 或 GraphRevoker checkpoint/partition 目录。
   - 不清 `results/selection_cache/`。
   - 不清 `results/score_cache/im*`。
   - 不清其他 method 的 `data/<Method>/`。

4. 跑 sanity。

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/sanity_graphrevoker.yaml --force
```

通过条件：

| 检查 | 期望 |
|---|---|
| 进程退出 | `completed: 1`，无异常 |
| 输出文件 | `results/runs/cora_GCN_r0.05/GraphRevoker_random/seed42/` 下 4 件齐 |
| F1 | 不应退化到 0.5 左右；Cora sanity 应接近正常 GCN 水平 |
| MIA / update-detection AUC | finite，不是无意义全 0 |

5. 整 method 重跑。
   - Cora GCN / GAT 主矩阵中所有 `GraphRevoker_*`。
   - 如果 k=5 baseline 或 ratio sweep 依赖 GraphRevoker，也一并列入 rerun。

6. 验证与同步。

```powershell
E:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/cora_GCN_r0.05
E:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/cora_GAT_r0.05
```

同步位置：

- [WORKPLAN.md](../../self/dashboard/WORKPLAN.md)：E4 状态。
- [config_inventory.html](../../self/dashboard/config_inventory.html)：GraphRevoker produced / usable / rerun。
- [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)：记录修复 sha、sanity 指标、重跑范围。
- [[02_TODO台账]]：E4 状态。

---

## TracIn 修复线

### 触发条件

- deployed TracIn 使用 `-(G @ G.sum(dim=0))`，实际是 training-gradient / regularization direction。
- 正确的 proper TracIn 应 contract with `∇L_E`，也就是 held-out eval/query loss gradient。
- concordance 显示 deployed cross-TracIn 与 GIF top-k overlap 只有约 `0.10-0.14`，proper TracIn 约 `0.65-0.74`。

### 受影响范围

| 范围 | 决策 |
|---|---|
| `*_tracin` cells | 必须 rerun |
| `*_hybrid` cells | 必须 rerun，因为 Hybrid 复用 TracIn 分数 |
| random / degree / pagerank / IM | 不受影响 |
| GU method training / unlearning code | 不受 TracIn 定义问题直接影响 |
| `results/score_cache/if/` | 旧 TracIn 分数无效，必须清或版本隔离 |
| `results/selection_cache/` 的 tracin / hybrid entries | 旧选点无效，必须清或版本隔离 |
| `results/score_cache/im*` | 不清 |

### 修复步骤

1. 改 TracIn 公式。
   - 文件：`attack/attack_strategies/tracin_strategy.py`
   - 从 deployed cross-TracIn 改为 proper TracIn：

```python
# old: wrong direction
col_sum = G.sum(dim=0)
scores = -(G @ col_sum)

# new: eval/query loss direction
g_eval = grad(L_E)
scores = G @ g_eval
```

2. 明确 `E` 的来源。
   - diagnostic 可用 test split 对齐 GIF。
   - 正式 attack/rebuttal 口径应使用 validation / query / pseudo-label probe set，避免 test-label leakage。
   - 把这个选择写进 `_meta.json` 或 config 注释，否则后续无法审计。

3. 处理 TracIn cache。
   - 清或隔离 `results/score_cache/if/` 中旧公式条目。
   - 清或隔离 `results/selection_cache/` 中 `strategy_name = tracin / hybrid / hybrid_v4` 的选点条目。
   - 保留 `results/score_cache/im/` 和 `results/score_cache/im_celf/`。
   - 保留 random / degree / pagerank / IM 的 result outputs。

4. 跑小图 sanity。
   - 先跑 Cora / GCN / GIF / TracIn 单 cell，确认公式、cache miss/save、输出路径正常。
   - 再跑 Hybrid 单 cell，确认 IM cache hit + proper TracIn 分支生效。

5. 跑 corrected TracIn / Hybrid 矩阵。
   - 对主矩阵：只重跑 `strategies in {tracin, hybrid}`。
   - 对 arxiv：先 smoke，再全量。

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_arxiv_tracin_smoke.yaml --force
```

期望：

| 检查 | 期望 |
|---|---|
| stdout | 出现 TracIn chunked path 或 ScoreCache miss/save |
| cache | 新 `results/score_cache/if/<key>.npz` 写入 |
| outputs | `results/runs/.../*_tracin/seed*/` 4 件齐 |
| Hybrid | IM cache 可 hit；TracIn 分支使用新公式 |

6. 验证与同步。
   - `config_inventory` 中旧 TracIn / Hybrid 从 usable 改为 rerun，重跑后再改 usable。
   - `VALIDATION_LOG` 记录 proper-TracIn 公式、`E` 的定义、cache 处理范围。
   - [[10_实验矩阵/12_近似策略重合度实验]] 更新“old TracIn produced != usable”的口径。
   - [[02_TODO台账]] 增加或更新 TracIn refresh TODO。

---

## 判定 produced / usable / rerun

| 状态 | 含义 |
|---|---|
| produced | 文件存在，但不一定能作为证据 |
| usable | 实现、cache、metric 口径均正确，可进 paper / rebuttal |
| rerun | 文件存在但因 bug / 公式 / cache 污染不能作为当前口径证据 |

GraphRevoker 和 TracIn 都要避免一句“跑过了”：

- GraphRevoker：旧 produced 可能是错 method 或坏 aggregator，必须标 rerun。
- TracIn：旧 produced 是错 selector 公式，必须标 rerun；Hybrid 同理。

---

## 最小同步清单

每次修复 / 重跑后，至少同步这些地方：

- [[01_WORKPLAN同步]]
- [[02_TODO台账]]
- [WORKPLAN.md](../../self/dashboard/WORKPLAN.md)
- [config_inventory.html](../../self/dashboard/config_inventory.html)
- [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)
- [PAPER_LIABILITIES_MAP.md](../../self/dashboard/PAPER_LIABILITIES_MAP.md)，如果影响 paper 硬伤
- [[14_Cache与结果层级]]
- [[15_实验运行入口与脚本]]
- [[10_实验矩阵/10_实验-框架总览]]
- [[10_实验矩阵/12_近似策略重合度实验]]
- [[30_评审与汇报/31_评审意见与rebuttal]]
