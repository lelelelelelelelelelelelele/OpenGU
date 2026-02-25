# 结果分析

读取 `results/` 目录下的实验结果，进行对比分析并生成报告。

## 分析类型

根据用户输入判断分析类型：

### 1. 策略对比（默认）
比较同一实验条件下不同攻击策略的效果。
- 读取同一 dataset/model/unlearning_method 下所有策略的结果
- 按 F1 drop 排序
- 输出对比表格

### 2. 跨数据集分析
输入含 "dataset" 或 "跨数据集" 时触发。
- 比较同一策略在不同数据集上的效果

### 3. 跨方法分析
输入含 "method" 或 "跨方法" 时触发。
- 比较同一策略对不同遗忘方法的攻击效果

### 4. 新增：Relative 对比分析
输入含 "relative" 或 "对比 baseline" 时触发。
- 读取 `results/relative/*.json`
- 对比各策略 vs random 的 relative_f1_drop
- 输出改进倍数排序

### 5. 新增：Collateral 损伤分析
输入含 "collateral" 或 "副作用" 时触发。
- 读取 `results/collateral/` 下的结果
- 比较不同方法的 gap 和 mean_pred_shift
- 识别高副作用配置

## 输出格式

### 标准分析表
```
## Analysis Report: [分析类型]

### Configuration
- Fixed: dataset=cora, model=GCN, method=GIF
- Variable: attack_strategy

### Results Table
| Strategy | F1 Before | F1 After | F1 Drop (%) | MIA AUC | Time (s) |
|----------|-----------|----------|-------------|---------|----------|
| hybrid   | 0.82      | 0.45     | -45.1       | 0.73    | 12.3     |
| tracin   | 0.82      | 0.52     | -36.6       | 0.68    | 10.1     |
| ...      | ...       | ...      | ...         | ...     | ...      |

### Key Findings
- [自动生成的发现，如：hybrid 比 random 高出 X 个百分点]

### Suggestions
- [基于结果的下一步建议]
```

### Relative 分析表
```
## Relative Analysis: vs Random Baseline

| Method   | Strategy | Baseline F1 | Attack F1 | Gap     | Relative Drop | Interpretation          |
|----------|----------|-------------|-----------|---------|---------------|-------------------------|
| GNNDelete| im       | 0.8801      | 0.7523    | -0.1278 | 0.1278        | attack effective        |
| GNNDelete| tracin   | 0.8801      | 0.7934    | -0.0867 | 0.0867        | attack effective        |
| ...      | ...      | ...         | ...       | ...     | ...           | ...                     |
```

### Collateral 分析表
```
## Collateral Damage Analysis

| Method   | Strategy | Retrain F1 | Unlearn F1 | Gap    | Gap%  | Pred Shift | Flipped  |
|----------|----------|------------|------------|--------|-------|------------|----------|
| GNNDelete| random   | 0.8764     | 0.8856     | -0.0092| -1.05%| 0.0130     | 1.07%    |
| GNNDelete| tracin   | 0.8653     | 0.8856     | -0.0203| -2.35%| 0.0151     | 0.79%    |
| ...      | ...      | ...        | ...        | ...    | ...   | ...        | ...      |
```

## 数据源路径

| 用途 | 路径 |
|------|------|
| 实验结果 | `results/experiments/*/_summary.json` |
| Relative 缓存 | `results/relative/*.json` |
| Collateral 结果 | `results/collateral/{method}/{dataset}/{model}/*.json` |
| 实验日志 | `results/_journal/auto_report.md` |

## 上下文
- 结果目录: results/
- 实验计划: self/宏观plan.md

用户输入: $ARGUMENTS
