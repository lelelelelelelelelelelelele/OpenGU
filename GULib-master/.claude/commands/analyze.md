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

## 输出格式
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

## 上下文
- 结果目录: results/
- 实验计划: self/宏观plan.md

用户输入: $ARGUMENTS
