# Bug Report：OpenGU 评估指标错误（GUIDE & GraphEraser）

**发现日期**: 2026-02-26
**修复 Commit（GUIDE）**: `c8810587` (2026-02-26 03:39)
**修复状态（GraphEraser）**: 未修复
**影响范围**: GUIDE 全部实验结果；GraphEraser 历史 node task 实验结果
**严重程度**: CRITICAL

---

## 问题描述

在使用 `demo_attack.py` 对多种方法运行攻击实验时，发现 GUIDE 方法所有策略的 F1 Drop 均为 0.0000，而 GraphEraser 的历史 f1_before 值来源不可靠。均由 OpenGU 源库实现缺陷导致，根本原因相同：`poison_f1`（pre-unlearning F1）在 node task 下从未被写入。

---

## GUIDE Bug

### Bug 1：Node 分类任务 — `poison_f1` 缺少赋值分支

**文件**: `unlearning/unlearning_methods/GUIDE/guide.py`
**函数**: `store_metrics()`（被 `exp_unlearn()` 调用）

**问题代码**（修复前）:
```python
if after_unlearning:
    self.average_f1[self.run]  = test_f1macro   # 存储 unlearn 后 F1
    self.average_auc[self.run] = test_aucroc
# 缺少 else 分支 —— after_unlearning=False 时 poison_f1 从未被写入
```

**修复后（commit c8810587）**:
```python
if after_unlearning:
    self.average_f1[self.run]  = test_f1macro
    self.average_auc[self.run] = test_aucroc
else:
    self.poison_f1[self.run]   = test_f1macro   # 新增：存储 unlearn 前 F1
```

**错误传播路径**:
1. `poison_f1` 初始化为 `np.zeros(num_runs)` → 始终为 0
2. `pipeline_adapter.py`：`f1_before_arr[0] > 0` 判断失败 → `f1_before = None`
3. 旧版代码有 fallback：`_evaluate_model()` 在 unlearning **后**评估 → `f1_before = f1_after`
4. 结果：`F1 Drop = 0`（旧版）或 `F1 Drop = NA`（当前版）

### Bug 2：Edge 预测任务 — AUC 误存为 F1

**文件**: `unlearning/unlearning_methods/GUIDE/guide.py`
**函数**: `store_metrics()`，edge task 分支

**问题代码**（修复前）:
```python
AUC_score = roc_auc_score(target_labels.cpu(), edge_pred.detach().cpu().numpy())
# 未计算 F1，直接把 AUC 存入 F1 字段
if after_unlearning:
    self.average_f1[self.run] = AUC_score    # BUG: AUC → F1
else:
    self.poison_f1[self.run]  = AUC_score    # BUG: AUC → F1
```

**修复后（commit c8810587）**:
```python
AUC_score = roc_auc_score(target_labels.cpu(), edge_pred.detach().cpu().numpy())
F1_score  = f1_score(target_labels.cpu(), edge_pred.detach().cpu().numpy())   # 新增
if after_unlearning:
    self.average_f1[self.run] = F1_score
else:
    self.poison_f1[self.run]  = F1_score
```

---

## GraphEraser Bug（未修复）

### Bug 3：Node 分类任务 — `poison_f1` 有条件守卫，node task 永不写入

**文件**: `unlearning/unlearning_methods/GraphEraser/grapheraser.py`
**函数**: `run_exp_train()` 和 `aggregate_shard_model()`

**问题代码**:
```python
# run_exp_train()，line 178
if self.args["poison"] and self.args["unlearn_task"] == "edge":
    self.poison_f1[self.run] = self.aggregate(self.run)

# aggregate_shard_model()，line 272
if self.args["poison"] and self.args["unlearn_task"] == "edge":
    self.poison_f1[self.run] = aggregate_f1_score
```

两处均用 `unlearn_task == "edge"` 守卫，**node task 时 `poison_f1` 永远不会被赋值**，与 GUIDE Bug 1 模式相同。

**错误传播路径**:
1. node task 下 `poison_f1` 始终为 `np.zeros(num_runs)`
2. `pipeline_adapter.py`：`f1_before = None`
3. **旧版 fallback 阶段（已记录进 cache 的历史结果）**：`_evaluate_model()` 在 unlearning 后评估，结果存入 `f1_before`——这是 **post-unlearning 值**，不是真正的 pre-unlearning baseline
4. **当前代码**：fallback 已移除，直接返回 `f1_before = None`，F1 Drop = NA

**历史 cache 结果的具体问题**：

auto_report 中可见 GraphEraser node task 的缓存结果：
```
pagerank: F1 Drop = -0.0295 (f1_before=0.8100, f1_after=0.8395)
degree:   F1 Drop = -0.0443 (f1_before=0.7970, f1_after=0.8413)
random:   F1 Drop = -0.0683 (f1_before=0.7675, f1_after=0.8358)
```

这些 `f1_before` 值（0.81, 0.797, 0.7675）**不是同一时刻的 pre-unlearning 值**，而是旧 fallback 用 post-unlearning 模型评估所得，且三次值各不相同（因不同 shard 配置导致聚合结果差异）。**不能用于计算真实 F1 Drop**。

> 注：由此推论，之前观察到的"GraphEraser Shard 保护效应"（F1 Drop 为负）**可能是该 bug 的假象**，需修复后重新验证。

---

## 方法影响汇总

| 方法 | task | `poison_f1` 状态 | `average_f1` 状态 | F1 Drop 可信度 | 修复状态 |
|------|------|-----------------|-------------------|----------------|---------|
| GUIDE | node | Bug 1：缺 else 分支 → 0 | ✅ 正确（f1macro） | ❌ 不可信 | ✅ 已修复 |
| GUIDE | edge | Bug 2：存的是 AUC | Bug 2：存的是 AUC | ❌ 不可信 | ✅ 已修复 |
| GraphEraser | node | Bug 3：有 edge 守卫 → 0 | ✅ 正确（aggregate F1） | ❌ 不可信 | ❌ 未修复 |
| CGU | node | 同 Bug 3 模式 → 0 | ⚠️ 存的是 accuracy | ❌ 不可信 | ❌ 未修复 |

---

## 历史数据影响评估

**GUIDE（已修复，需重跑）**：
- `results/collateral/GUIDE/` 全部 89 条数据点无效
- `results/_journal/auto_report.md` 中所有 `method=GUIDE` 条目无效
- 历史 F1 Drop = 0 均为 bug 产生的假值

**GraphEraser（未修复，历史缓存不可信）**：
- `results/collateral/GraphEraser/` 中的数据：collateral gap 计算依赖 f1_before/after，但 GraphEraser 的 average_f1（f1_after）来自聚合评估，相对可信；gap 本身影响较小
- 历史 `demo_attack.py` GraphEraser 结果（cache=HIT）中的 `f1_before` 均为 post-unlearning 值，**F1 Drop 不可信**
- "Shard 保护效应"结论存疑，需重验证

---

## Relative 指标框架的影响评估

**结论：Relative 指标不受本 bug 影响，历史 relative 结果对 node task 可信。**

Relative 指标的计算公式：
```
relative_f1_drop = baseline_f1_after（random k=5 均值）- attack_f1_after（策略结果）
```

两侧均只读取 `average_f1`（post-unlearning F1），完全不依赖 `poison_f1`。而各方法的 `average_f1` 在 node task 下均设置正确：

| 方法 | `average_f1` 来源 | node task 可信度 |
|------|------------------|-----------------|
| GUIDE | `test_f1macro`（`after_unlearning=True` 分支） | ✅ 正确 |
| GraphEraser | `self.aggregate(self.run)`（shard 聚合 F1） | ✅ 正确 |
| GIF / GNNDelete | 正常 IF-based / Learning-based pipeline | ✅ 正确 |

因此：
- **历史 relative 结果（node task）可信**，无需因本 bug 重做
- **需要重做的是**：GUIDE 在 relative 框架下的实验尚未跑（之前跑的是 demo_attack 绝对指标，F1 Drop=0 是绝对指标的问题，不影响 relative 框架）
- **GraphEraser 需确认**：relative 结果中使用的 `f1_after` 是否来自新鲜运行而非旧缓存污染

---

## 根因分析

这是 **OpenGU 上游库的实现 bug**，非本项目 attack 框架问题：

- GUIDE / GraphEraser / CGU 均对 `poison_f1` 赋值加了 `unlearn_task == "edge"` 的守卫，导致 node task 时 pre-unlearning F1 永远不被记录
- 本项目 `pipeline_adapter.py` 旧版 fallback（`_evaluate_model()` 在 unlearning 后调用）掩盖了症状，产生了貌似合理但实为错误的 f1_before 值
- 当前 `pipeline_adapter.py` 已移除该 fallback，node task 时会正确返回 `f1_before = NA`

---

## 修复方案

GraphEraser 修复思路（参照 GUIDE Bug 1 修复方式）：

**`grapheraser.py` — `run_exp_train()`**:
```python
# 修复前
if self.args["poison"] and self.args["unlearn_task"] == "edge":
    self.poison_f1[self.run] = self.aggregate(self.run)

# 修复后：拆分 node/edge 两条路径
if self.args["unlearn_task"] == "node":
    self.poison_f1[self.run] = self.aggregate(self.run)   # 新增
elif self.args["poison"] and self.args["unlearn_task"] == "edge":
    self.poison_f1[self.run] = self.aggregate(self.run)
```

类似地修改 `aggregate_shard_model()`。

---

## 验证方法

```bash
conda activate gnn
cd H:/project/OpenGU/GULib-master

# GUIDE 验证（已修复）
python demo_attack.py --dataset cora --model GCN --method GUIDE --strategies random --ratio 0.05
# 预期：F1 Drop ≠ 0，f1_before ≠ f1_after

# GraphEraser 验证（修复后）
python demo_attack.py --dataset cora --model GCN --method GraphEraser --strategies random --ratio 0.05
# 预期：F1 Drop ≠ NA，f1_before 为真实 pre-unlearning 值
```

---

## 后续行动

- [x] 修复 GUIDE node/edge task 评估指标（commit c8810587）
- [ ] **修复 GraphEraser `poison_f1` node task 赋值缺失**
- [ ] 修复后重新运行全部 GraphEraser node task 实验，验证 Shard 保护效应是否真实存在
- [ ] 修复后重新运行全部 GUIDE 实验（Cora/GCN, Cora/GAT, Citeseer/GCN）
- [ ] 清理 GraphEraser 相关历史缓存（`results/` 下 cache=HIT 的旧结果）
- [ ] 排查 CGU node task `poison_f1` 赋值缺失（同类问题）
- [ ] 将修复后结果纳入论文实验表格
