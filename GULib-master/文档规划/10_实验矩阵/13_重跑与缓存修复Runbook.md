---
title: 修复验收与回归测试台账
created: 2026-07-09
updated: 2026-07-20
type: repair-acceptance-ledger
status: active
tags: [acceptance, regression, cache, rerun, graphrevoker, tracin]
---

# 修复验收与回归测试台账

> 文件名保留 `13_重跑与缓存修复Runbook.md` 只是为了兼容既有 Obsidian 链接；本页自 2026-07-20 起不再充当逐步操作 Runbook，而是记录每条修复线的**结论、测试、证据边界与失效数据**。

通用故障分流与执行命令分别看：

- cache / result 分层：[[14_Cache与结果层级]]
- 正式运行入口：[[15_实验运行入口与脚本]]
- 4090 执行与回收：[[16_4090小数据集运行与回收]]
- Cache V2 / Legacy 边界：[[19_Cache架构重设计与迁移方案]]
- OpenGU 专用 cache 修复规范：`scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`

---

## 0. 状态词

| 状态 | 含义 |
|---|---|
| `PASS` | 代码、测试与要求范围内的实验 gate 已通过 |
| `PASS (remote)` | 远端执行与 gate 已报告通过，但完整产物尚未回收到本地证据库 |
| `ARCHIVE PENDING` | 结论已形成，但本地四件套、manifest 或总验收报告尚未闭环 |
| `PENDING` | 修复或规定范围的测试尚未完成 |
| `INVALID` | 已知错误实现/旧口径产物；只作历史溯源，禁止进入论文或当前 aggregate |
| `SUPERSEDED` | 指导书或状态已被本页/新工具取代 |

`produced` 只表示文件存在；`usable` 必须同时满足实现、口径、provenance 和 gate；`INVALID` 不能因为“跑过了”恢复为 `usable`。

---

## 1. 总结论

| 修复线 | 当前结论 | 能说什么 | 不能说什么 |
|---|---|---|---|
| GraphRevoker dispatcher / class path | `PASS` | 当前代码调用真实 GraphRevoker | 不能把 2026-05-05 前的 GraphRevoker 标签当真 GraphRevoker |
| GraphRevoker shard-ensemble collateral | `PASS` | 单 shard 抽取回归已关闭；当前 adapter 使用完整 ensemble | 不能恢复旧 `perf_before=0.50–0.58` cell |
| seed42 四策略 canary | `PASS` | Cora/GCN/r=0.05，random/degree/pagerank/IM 4/4 通过 | 不能从单 seed 推断多 seed 策略排序 |
| E4 四策略五 seed、GCN/GAT | `PASS (remote)` + `ARCHIVE PENDING` | `WORKPLAN` 记录 40/40、两阶段 gate 通过、queue exit=0 | 在完整产物/总验收回收到本地前，不从本地旧目录提取新 E4 数值 |
| GraphRevoker 的 TracIn/Hybrid | `PENDING` | 无 | E4 40-cell 不包含这两列，不能写成 6-selector 全完成 |
| 旧 GraphRevoker 主矩阵 / k=5 | `INVALID` | 可用于说明历史 bug 范围 | 禁止用于当前 paper、统计或 dashboard 的 clean evidence |
| deployed TracIn / Hybrid | `INVALID` | 可用于复现实验史与说明公式迁移原因 | 禁止当 proper-TracIn 证据 |
| versioned proper-TracIn refresh | `PENDING`（以当前 `main` 为准） | 当前只引用已合入主线的 concordance 结论 | 未合入主线的分支 gate 不提前记为完成 |

---

## 2. GraphRevoker 验收书

### 2.1 故障与修复边界

GraphRevoker 历史上存在两类不同问题：

1. **dispatcher alias**：2026-05-05 前，`"GraphRevoker"` 实际指向 `grapheraser`；这些结果是错标签。
2. **collateral 单 shard 抽取**：后续通用 adapter 曾把最后一个 shard 当作全图模型，造成 `perf_before=0.50–0.58` 的系统退化。

当前实现的验收对象是：

- `unlearning_manager.py` 中 `"GraphRevoker": graphrevoker`；
- `attack/pipeline_adapter.py::_GraphRevokerEnsembleModel`；
- `AttackPipeline._get_trained_model()` 的 GraphRevoker 分支；
- baseline/unlearned shard checkpoint 与 aggregation weight 的组合推理。

### 2.2 回归测试矩阵

| ID | 检查 | 证据 | 结论 |
|---|---|---|---|
| GR-01 | dispatcher 指向真实类 | `unlearning_manager.py` method map | `PASS` |
| GR-02 | collateral 取完整 ensemble | `attack/pipeline_adapter.py` wrapper + routing | `PASS` |
| GR-03 | GraphEraser 行为不被连带改变 | `tests/test_phase_b_invariants.py::test_grapheraser_get_trained_model_behavior_is_unchanged` | `PASS` |
| GR-04 | 当前相关回归 | `python -m pytest tests/test_phase_b_invariants.py -q`，2026-07-20 本地 41 passed | `PASS` |
| GR-05 | seed42 四策略真机 canary | `docs/graphrevoker_postfix_canary_ACCEPTANCE_REPORT.md` + HTML | `PASS`（4/4） |
| GR-06 | E4 GCN/GAT × 四策略 × 五 seed | `self/dashboard/WORKPLAN.md` C5/E4：GCN 20/20、GAT 20/20、queue exit=0 | `PASS (remote)`（40/40） |
| GR-07 | 完整 E4 本地证据归档 | 本地同名 `results/runs/4090` 仍是 2026-05-07 旧 SHA，且未回收 NPZ | `ARCHIVE PENDING` |
| GR-08 | 历史坏数据隔离 | `VALIDATION_LOG.md` 2026-05-05 条目 + 本页失效规则 | `INVALID` 永久锁定 |

### 2.3 当前允许的结论

- GraphRevoker **代码路径已修复**，不再写“GraphRevoker 仍未修好”。
- E4 规定的四策略、两个 backbone、五 seed **远端执行已通过**。
- GraphRevoker 可保留在 6-method audit 中。
- seed42 canary 支持“修复后的推理链正常”，不支持单 seed 机制排序。
- 完整多 seed 数值进入 paper/aggregate 前，仍需完成本地 evidence import 和同口径总验收。

### 2.4 永久失效范围

以下内容只允许留在 archive / validation history：

- 2026-05-05 dispatcher 修复前的所有 `GraphRevoker` 标签结果；
- `perf_before=0.50–0.58` 的单 shard collateral 结果；
- 本地 `results/runs/4090` 中 2026-05-07、git SHA `b8fc3d...` 的同名旧视图；
- 基于上述数据写出的 GraphRevoker 机制比较、均值、显著性与图表。

**禁止操作**：用新代码已通过这一事实给旧数值“洗白”，或直接覆盖 archive 让旧/新 provenance 混在一起。

### 2.5 剩余闭环

1. 回收/注册远端 40-cell manifest 与可用产物；若按既定策略不传 `predictions.npz`，总验收必须明确服务器 gate 证据和本地缺失边界。
2. 生成 `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md` 与 `report/graphrevoker_e4_ACCEPTANCE_REPORT.html` 的最终归档版。
3. 证据导入后再把 `config_inventory` 的 `accepted_remote` 提升为本地 `usable`。
4. TracIn/Hybrid 另走 proper-TracIn gate；不并入已完成的 E4 四策略结论。

---

## 3. TracIn / Hybrid 验收书

### 3.1 已判定失效的旧口径

deployed cross-TracIn 使用 training-gradient / regularization direction，而不是 held-out eval/query loss gradient。concordance 已显示旧 deployed TracIn 与 GIF / proper-TracIn 的选点重合明显不足。因此：

| 范围 | 结论 |
|---|---|
| 旧 `*_tracin` | `INVALID`，需 versioned proper-TracIn refresh |
| 旧 `*_hybrid` | `INVALID`，因复用旧 TracIn 分数 |
| random / degree / pagerank / IM | 不受 TracIn 公式问题影响 |
| `results/score_cache/im*` | 不受影响，不清 |
| Legacy IF / Selection Cache | V2 迁移期只读，不原地改写 |

### 3.2 proper-TracIn 通过门

只有以下项目全部有证据时，状态才能从 `PENDING` 改为 `PASS`：

- algorithm/producer version 明确，不与 deployed legacy key 共用；
- eval/query set 定义写入 Recipe / `_meta.json`，无隐式 test-label leakage；
- cold 生成与 warm exact hit 都通过；
- selected nodes 数量、顺序、payload hash 与 consumer ref 可审计；
- TracIn 与 Hybrid 各有最小真机 cell；
- paper-facing 旧 TracIn/Hybrid cell 已用新版本刷新；
- `config_inventory` 和 `VALIDATION_LOG` 同步完成。

本页只记录已经合入当前父线的证据。其他分支上的实验即使完成，也要在合入后才改变这里的状态。

---

## 4. 新事故的最小验收模板

以后新增 method / selector 修复时，在本页追加一条，不再新建一次性长指导书：

| 字段 | 必填内容 |
|---|---|
| 故障 | 可复现症状与错误范围 |
| 根因 | method / selector / metric / artifact 哪一层 |
| 修复 | commit、文件、行为变化 |
| 不变量 | 明确哪些 cache / method /旧产物不得改变 |
| 单测 | 测试命令与通过数 |
| 真机 gate | config、cell、exit code、四件套/策略字段 |
| 扩展矩阵 | method × strategy × seed × dataset/backbone |
| 结论 | `PASS / PASS (remote) / ARCHIVE PENDING / PENDING / INVALID` |
| 失效范围 | 旧 SHA、日期、目录、字段或 algorithm version |
| 同步位置 | WORKPLAN、config inventory、VALIDATION_LOG、OB、双格式报告 |

通用流程固定为：

```mermaid
flowchart LR
  A[异常] --> B[定位故障层]
  B --> C[冻结失效范围]
  C --> D[最小修复]
  D --> E[单测]
  E --> F[单格真机 gate]
  F --> G[规定矩阵]
  G --> H[双格式验收]
  H --> I[证据归档与状态提升]
```

---

## 5. 同步规则

修复状态变化时至少同步：

- [WORKPLAN.md](../../self/dashboard/WORKPLAN.md)
- [[02_TODO台账]]
- [config_inventory.html](../../self/dashboard/config_inventory.html)
- [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)（append-only）
- [[10_实验矩阵/10_实验-框架总览]]
- [[15_实验运行入口与脚本]]
- 对应的 Markdown + HTML 验收报告

活动文档只保留当前结论；旧过程细节由 Git 历史、dated report 和 `VALIDATION_LOG` 保存。
