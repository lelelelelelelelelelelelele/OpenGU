---
title: GraphRevoker E4 修复与证据归档验收报告
date: 2026-07-20
status: conditional-accepted-archive-pending
source_of_truth: self/dashboard/WORKPLAN.md
---

# GraphRevoker E4 修复与证据归档验收报告

## 1. 验收结论

**GraphRevoker 的实现修复已通过，E4 规定的远端 40-cell 执行已由当前 `WORKPLAN` 记录为 40/40 passed；但完整多 seed 产物尚未在本地形成可复核归档，因此本报告给出 `CONDITIONAL ACCEPT / ARCHIVE PENDING`。**

这不是把 E4 改回“未完成”：代码修复和远端执行均已完成。剩余事项是 evidence import、manifest 与本地总验收闭环。旧 GraphRevoker 数据继续永久禁止引用。

| 验收面 | 结论 | 边界 |
|---|---|---|
| dispatcher / 真实方法路径 | `PASS` | 当前 `"GraphRevoker": graphrevoker` |
| shard-ensemble collateral | `PASS` | adapter 不再把单 shard 当全图模型 |
| 本地回归测试 | `PASS` | 2026-07-20：`tests/test_phase_b_invariants.py` 41 passed |
| seed42 真机 canary | `PASS` | Cora/GCN/r=0.05，四策略 4/4 |
| E4 远端矩阵 | `PASS (remote)` | GCN 20/20 + GAT 20/20；两阶段 gate；queue exit=0 |
| E4 本地证据归档 | `ARCHIVE PENDING` | 当前本地同名目录仍是 2026-05-07 旧视图，不能代替新 E4 |
| GraphRevoker TracIn/Hybrid | `OUT OF SCOPE / PENDING` | 不属于已通过的四策略 E4 |
| pre-fix / 单-shard 旧数据 | `INVALID` | 只作历史溯源，禁止 paper/aggregate |

## 2. 验收范围

E4 的权威范围来自 `self/dashboard/WORKPLAN.md` C5、依赖图和 E4 行：

| 维度 | 范围 |
|---|---|
| Method | GraphRevoker |
| Dataset / ratio | Cora / 0.05 |
| Backbone | GCN、GAT |
| Strategy | random、degree、pagerank、IM |
| Seed | 5 seeds |
| 总量 | 2 × 4 × 5 = 40 cells |
| 远端状态 | GCN 20/20、GAT 20/20；queue exit=0 |

TracIn 和 Hybrid 被明确排除，原因是它们需要独立的 proper-TracIn 版本化 gate。不得把 40-cell 结论扩写成 6-selector 全矩阵完成。

## 3. 本地可复核证据

### 3.1 当前代码

- `unlearning_manager.py`：`"GraphRevoker": graphrevoker`；
- `attack/pipeline_adapter.py`：存在 `_GraphRevokerEnsembleModel`；
- `AttackPipeline._get_trained_model()`：GraphRevoker 路由到 `_build_graphrevoker_ensemble_model()`；
- `tests/test_phase_b_invariants.py`：覆盖 GraphRevoker ensemble 与 GraphEraser 不变量。

2026-07-20 本地命令：

```text
E:/conda_package/envs/gnn/python.exe -m pytest tests/test_phase_b_invariants.py -q
41 passed in 0.20s
```

### 3.2 seed42 真机 canary

阶段报告：

- Markdown：`docs/graphrevoker_postfix_canary_ACCEPTANCE_REPORT.md`
- HTML：`report/graphrevoker_postfix_canary_ACCEPTANCE_REPORT.html`

该报告验证 Cora/GCN/r=0.05、seed42 的 random/degree/pagerank/IM 4/4、shard checkpoint、aggregation weight、NPZ 复算与 active Legacy 不变量。它支持“修复链正确”，但其自身明确不是完整 E4。

### 3.3 当前本地结果视图的限制

本地 `results/runs/4090/cora_{GCN,GAT}_r0.05/GraphRevoker_{random,degree,pagerank,im}/seed*` 可枚举出 40 个同名目录，但抽查/汇总显示：

- `_meta.json` 时间为 2026-05-07；
- git SHA 为 `b8fc3d59...`；
- 按既定回收策略未带 `predictions.npz`；
- 这些目录早于 2026-07-14 post-fix E4。

因此它们是历史本地视图，不是新 E4 的落盘证据。当前不能从这些目录重新计算或引用 post-fix 40-cell 统计。

## 4. 远端 40/40 结论的证据等级

当前仓库对完整 E4 的直接证据是 `WORKPLAN` 的操作记录：

- C5：固定源码完成 40/40，两阶段 gate 通过、queue exit=0；
- E4：GCN 20/20、GAT 20/20；
- 依赖图：新 40-cell 矩阵被指定为 GraphRevoker 权威证据。

这足以关闭“代码是否仍未修好”和“是否已经执行 E4”两个状态问题；但缺少本地完整 manifest、逐 cell `_meta.json` 汇总和最终机器验收附件，所以本报告不补写不存在的多 seed 数值，也不声称本地归档已通过。

## 5. 历史数据失效声明

以下数据永久 `INVALID`：

1. 2026-05-05 dispatcher 修复前，所有标成 GraphRevoker、实际执行 GraphEraser 的结果；
2. collateral adapter 抽取单 shard 导致 `perf_before=0.50–0.58` 的结果；
3. 当前本地 2026-05-07、SHA `b8fc3d59...` 的同名旧矩阵；
4. 基于这些数据生成的 GraphRevoker 机制 wedge、显著性、图表和汇总行。

代码修复成功不改变上述失效判定。新旧产物必须以 git SHA、timestamp、config fingerprint 和 manifest 区分。

## 6. 提升为完整归档验收的最小清单

- [ ] 回收或注册远端 40-cell manifest；
- [ ] 保存每格 `_meta.json`、`attack.json`、`collateral.json` 的完整索引；
- [ ] 对未回收 `predictions.npz` 的策略写明服务器 gate 证据与本地缺失边界；
- [ ] 汇总 git SHA、config/fingerprint、seed、strategy、exit/gate 状态；
- [ ] 将 dashboard 的 `accepted_remote` 20 cells/模型提升为本地 `usable`；
- [ ] 用归档证据补充本报告，不改写 seed42 阶段报告。

## 7. 最终判定

| 问题 | 回答 |
|---|---|
| GraphRevoker 代码是否修好？ | **是，PASS。** |
| seed42 四策略是否通过？ | **是，4/4 PASS。** |
| 完整 E4 是否执行成功？ | **按当前权威 WORKPLAN，是，远端 40/40 PASS。** |
| 完整 E4 是否已在本地完成可复核归档？ | **否，ARCHIVE PENDING。** |
| 旧 GraphRevoker 数据能否重新使用？ | **不能，永久 INVALID。** |
| 当前能否声称 TracIn/Hybrid 也完成？ | **不能，不在 E4 四策略范围内。** |

**Overall verdict: `CONDITIONAL ACCEPT — implementation and remote E4 accepted; local evidence archive pending`.**
