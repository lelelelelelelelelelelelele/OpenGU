# 实验报告生成工作流（手动分析版）

## 概述

本工作流用于从实验结果生成技术分析报告，包含：
1. 数据汇总与统计分析（需手动执行）
2. 攻击效果评估
3. 问题识别
4. 改进建议

**注意**：本文件为**手动分析指南**，不是自动化脚本。自动化脚本 `report_workflow.py` 存在 bug 需要修复。

---

## 第一步：数据收集

### 1.1 定位实验结果

实验结果的目录结构：
```
results/experiments/{group}/phase_a/{timestamp}_seed{seed}/_summary.json
```

**常用实验组**：
| Group | 描述 | 位置 |
|-------|------|------|
| mg0_completion | Cora/GCN 稳定性 | results/experiments/mg0_completion/ |
| mg1_citeseer | Citeseer 数据集 | results/experiments/mg1_citeseer/ |
| mg2_gat | GAT 模型 | results/experiments/mg2_gat/ |
| mg3_citeseer | Citeseer 扩展 | results/experiments/mg3_citeseer/ |
| mg3_gat | GAT 扩展 | results/experiments/mg3_gat/ |

### 1.2 数据结构分析

打开任意 `_summary.json`，结构如下：

```json
{
  "phase": "Phase A: Method Comparison (Cora/GCN)",
  "timestamp": "20260221_182253",
  "random_seed": 42,
  "results": {
    "GNNDelete_cora_GCN_r0.05": {
      "config": { ... },
      "attacks": [
        {
          "strategy_name": "im",
          "selected_nodes": [...],
          "f1_drop": 0.1458,
          "f1_drop_ratio": 16.32,
          "mia_auc": 0.65,
          "attack_time": 12.3
        },
        ...
      ]
    },
    "GraphEraser_cora_GCN_r0.05": { ... },
    ...
  }
}
```

### 1.3 手动提取数据

**快速查看方法**：
```bash
# 查看某个 seed 的关键指标
cat results/experiments/mg0_completion/phase_a/20260221_182253_seed42/_summary.json \
  | python -c "import json,sys; d=json.load(sys.stdin); \
    for k,v in d['results'].items(): \
      for a in v.get('attacks',[]): \
        print(f\"{k.split('_')[0]}_{a['strategy_name']}: f1_drop={a['f1_drop']:.4f}\")"
```

---

## 第二步：统计分析

### 2.1 核心指标表

按以下格式整理数据：

| Method | Strategy | Seed 1 | Seed 2 | Seed 3 | Seed 4 | Seed 5 | Mean | Std |
|--------|----------|--------|--------|--------|--------|--------|------|-----|
| GNNDelete | random | 0.092 | ... | ... | ... | ... | | |
| GNNDelete | im | 0.146 | ... | ... | ... | ... | | |
| GraphEraser | random | -0.083 | ... | ... | ... | ... | | |
| ... | ... | | | | | | | |

### 2.2 方法类型分类

| 类别 | 方法 | 攻击特性 |
|------|------|----------|
| **Learning-based** | GNNDelete | 对 IF/IM 策略敏感，IM 最有效 |
| **IF-based** | GIF | 攻击效果较小（~1-3%） |
| **Shard-based** | GraphEraser | 免疫/反效应，random 更有效 |

### 2.3 统计计算规则

- **Mean**: (Seed1 + Seed2 + ... + Seed5) / 5
- **Std**: 标准差
- **显著性判定**: mean > 0.05 为"有效攻击"，mean < -0.03 为"反效应"

---

## 第三步：问题诊断

### 3.1 自动识别规则

| 问题类型 | 识别条件 | 标记 | 可能的根因 |
|----------|----------|------|------------|
| 攻击无效 | f1_drop_mean < 0.01 | ⚠️ | ratio 太小，或方法天然抗攻击 |
| 反效应 | f1_drop_mean < -0.03 | 🔄 | Shard-based 分区机制，删除 hub 反而优化子图 |
| 波动大 | std / mean > 0.5 | 📊 | seed 敏感，结果不稳定 |
| MIA 弱 | mia_auc < 0.55 | 🛡️ | 近似质量好，难以推断 |

### 3.2 方法特异性诊断

**Learning-based (GNNDelete)**：
- IM 策略是否最有效？（应该是）
- ratio=5% 是否足够？（可尝试 10%/20%）

**IF-based (GIF)**：
- 所有策略效果都小（~1-3%）？
- 可能是近似误差本身较小

**Shard-based (GraphEraser)**：
- 是否出现反效应？（f1_drop < 0）
- random 是否优于 IF/IM 策略？（应该是）
- 尝试选择 shard 边界节点能否打破免疫？

### 3.3 数据完整性检查

运行前确认：
- [ ] 每个 method × strategy 组合有 5 个 seed 的数据
- [ ] 没有缺失值（NA）
- [ ] f1_drop_ratio 与 f1_drop 一致（f1_drop_ratio = f1_drop / f1_before * 100）

---

## 第四步：生成报告

### 4.1 报告模板

复制 `report/progress/2026-02-22_checkpoint/report/PROGRESS_REPORT.md` 作为基础，按以下结构填充：

```markdown
## 一、实验数据概览

[插入上面 2.1 的统计表格]

## 二、核心发现

### 2.1 最有效攻击组合
- {method} + {strategy}: f1_drop = {mean:.1%}

### 2.2 无效/反效应组合
- {method} + {strategy}: f1_drop = {mean:.1%} ({反效应/无效})

### 2.3 方法类型差异
- Learning-based: ...
- IF-based: ...
- Shard-based: ...

## 三、问题诊断

- ⚠️ {问题描述}
- 🔄 {问题描述}

## 四、改进建议

[根据 3.2 的方法特异性诊断给出建议]

## 五、下一步行动

| 优先级 | 任务 | 预期产出 |
|--------|------|----------|
| 高 | ... | ... |
```

### 4.2 图表生成

可选生成以下图表：
- 热力图：method × strategy 的 f1_drop
- 柱状图：按 strategy 分组的效果对比
- 折线图：不同 ratio 的攻击效果变化

图表脚本位置：`scripts/evaluation/plotting/attack_charts.py`

---

## 第五步：Collateral 评估补充

### 5.1 何时需要

当攻击实验完成后，需要评估：
1. **Retrain Gap**: unlearned 模型 vs 真实 retrain 模型的性能差距
2. **Collateral Damage**: 删除节点对保留节点预测的影响

### 5.2 运行方式

```bash
# 先检查缓存是否存在
ls results/cache/*.json | head -5

# 运行 collateral 评估
python eval_collateral.py \
    --dataset_name cora \
    --base_model GCN \
    --unlearning_methods GNNDelete \
    --strategies random,degree,pagerank,tracin,im,hybrid \
    --unlearn_ratio 0.05 \
    --random_seed 2024 \
    --repair

# 或使用脚本批量运行
bash scripts/experiments/run_mg0_completion.sh --run_collateral
```

### 5.3 结果位置

```
results/collateral/{method}/{dataset}/{model}/collateral_{timestamp}.json
```

### 5.4 诊断指标

| 指标 | 含义 | 健康范围 |
|------|------|----------|
| gap | Retrain Gap (unlearned - retrained) | < 5% |
| gap_pct | Gap 百分比 | < 10% |
| mean_pred_shift | 保留节点预测变化均值 | < 0.1 |
| max_pred_shift | 保留节点预测变化最大值 | < 0.3 |
| fraction_flipped | 预测翻转比例 | < 0.1 |

---

## 附录：已知问题

### A.1 自动化脚本 bug

`report_workflow.py` 存在以下问题需要修复：

1. **Glob 模式错误**（第 34 行）：
   ```python
   # 错误
   summary_files = list(RESULTS_DIR / group / "phase_a" / "*" / "_summary.json")
   # 正确
   summary_files = list((RESULTS_DIR / group / "phase_a").glob("*_seed*_/_summary.json"))
   ```

2. **数据结构解析错误**（第 52 行）：
   ```python
   # 错误：期望 data["experiments"]
   # 正确：遍历 data["results"]["{method}_{dataset}_{model}_r{ratio}"]["attacks"]
   ```

### A.2 缓存不匹配问题

运行 `eval_collateral.py` 时可能找不到缓存，原因是：
- seed 不匹配（实验用 2024，默认脚本可能用其他值）
- ratio 不匹配（实验用 0.05，默认参数是 0.1）

解决：显式传递 `--unlearn_ratio 0.05 --random_seed 2024`

---

## 快速检查清单

- [ ] 确认所有实验组数据已收集
- [ ] 统计表格完整（所有 method × strategy 组合）
- [ ] 标记显著/无效/反效应的组合
- [ ] 分析方法类型差异
- [ ] 给出针对性改进建议
- [ ] 补充 collateral 评估（如果需要）
- [ ] 更新 PROGRESS_REPORT.md 状态
