# Bug Report：OpenGU GUIDE 评估指标错误

**发现日期**: 2026-02-26
**修复 Commit**: `c8810587` (2026-02-26 03:39)
**影响范围**: 所有涉及 GUIDE 方法的攻击实验历史结果
**严重程度**: CRITICAL — 导致 GUIDE 攻击效果评估完全失效

---

## 问题描述

在使用 `demo_attack.py` 对 GUIDE 方法运行攻击实验时，所有策略（random/degree/tracin/im_v4/hybrid_v4）的 F1 Drop 均为 **0.0000**，f1_before = f1_after。

初步误判为"GUIDE 对攻击免疫"，后经代码审查确认是 OpenGU 源库 `guide.py` 中的两处实现 bug。

---

## Bug 详情

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

**修复后**:
```python
if after_unlearning:
    self.average_f1[self.run]  = test_f1macro
    self.average_auc[self.run] = test_aucroc
else:
    self.poison_f1[self.run]   = test_f1macro   # 新增：存储 unlearn 前 F1
```

**错误传播路径**:
1. `poison_f1` 初始化为 `np.zeros(num_runs)` → 始终为 0
2. `pipeline_adapter.py` 读取：`f1_before_arr[0] > 0` 判断失败
3. fallback：用当前模型（已完成 unlearning）重新 evaluate → 得到的是 **unlearn 后**的 F1
4. `f1_before = f1_after`（同一个模型评估两次）→ `F1 Drop = 0`

---

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

**修复后**:
```python
AUC_score = roc_auc_score(target_labels.cpu(), edge_pred.detach().cpu().numpy())
F1_score  = f1_score(target_labels.cpu(), edge_pred.detach().cpu().numpy())   # 新增
if after_unlearning:
    self.average_f1[self.run] = F1_score     # 存储真实 F1
else:
    self.poison_f1[self.run]  = F1_score     # 存储真实 F1
```

---

## 涉及实验场景

| 任务类型 | Bug | 现象 | 影响 |
|---------|-----|------|------|
| Node 分类（Cora/GCN 等） | Bug 1 | F1 Drop = 0，f1_before = f1_after | 所有 GUIDE node 实验无效 |
| Edge 预测 | Bug 2 | F1 字段实为 AUC，数值偏高 | 所有 GUIDE edge 实验无效 |

---

## 历史数据影响评估

以下所有 GUIDE 实验结果**不可信**，需在修复后重新运行：

- `results/collateral/GUIDE/` 下的全部 collateral 评估（89 条数据点，gap=-0.39%，无意义）
- `results/relative/GUIDE/`（如有）下的全部 relative 评估
- `results/_journal/auto_report.md` 中所有 `method=GUIDE` 的实验条目
- 历史 `demo_attack.py` GUIDE 实验（F1 Drop=0 均为错误值）

---

## 根因分析

这是 **OpenGU 上游库的实现 bug**，不是本项目 attack 框架的问题：

- GUIDE 的 `store_metrics()` 在 node task 中本应用同一逻辑分别记录 before/after，但 `else` 分支遗漏
- GUIDE 的 edge task 代码直接复用了 AUC 计算，未区分 F1 和 AUC 指标

`pipeline_adapter.py` 的 fallback 机制（`f1_after == 0` 时调用 `_evaluate_model()`）隐藏了 Bug 1 的表面症状：不报错，但给出错误的 F1 Drop = 0。

---

## 修复验证方法

修复后，运行以下命令验证 GUIDE 的 F1 Drop 不为 0：

```bash
conda activate gnn
cd H:/project/OpenGU/GULib-master
python demo_attack.py --dataset cora --model GCN --method GUIDE --strategies random --ratio 0.05
# 预期：F1 Drop ≠ 0，f1_before ≠ f1_after
```

---

## 后续行动

- [ ] 重新运行全部 GUIDE 实验（node task，Cora/GCN, Cora/GAT, Citeseer/GCN）
- [ ] 检查其他 Shard_based 方法（GraphEraser、GraphRevoker）是否存在同类 `poison_f1` 赋值遗漏
- [ ] 检查 CGU 方法（commit c881058 同时修改了 `cgu.py`）是否有类似 bug
- [ ] 将修复后的 GUIDE 结果纳入论文实验表格
