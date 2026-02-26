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
- 读取 `results/relative/{Method}/{Dataset}/{Model}/*.json`
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

## 实现步骤

### 1. 判断分析类型
根据用户输入关键词判断分析类型：
- 含 "relative" / "baseline" / "对比" → Relative 分析
- 含 "collateral" / "副作用" / "gap" → Collateral 分析
- 含 "dataset" / "跨数据集" → 跨数据集分析
- 含 "method" / "跨方法" → 跨方法分析
- 默认 → 策略对比分析

### 2. Relative 分析实现
```python
def analyze_relative(method_filter=None, dataset_filter=None):
    """读取 results/relative/{Method}/{Dataset}/{Model}/*.json 并生成对比表。"""
    import json
    import glob

    results = []
    for cache_file in glob.glob("results/relative/**/*.json", recursive=True):
        with open(cache_file) as f:
            data = json.load(f)
            for r in data.get("results", []):
                if method_filter and r["method"] != method_filter:
                    continue
                if dataset_filter and r["dataset"] != dataset_filter:
                    continue
                results.append(r)

    # 按 relative_f1_drop 降序排列
    results.sort(key=lambda x: x["relative_f1_drop"], reverse=True)
    return results
```

**输出字段**：
- `method`: 遗忘方法
- `dataset`: 数据集
- `strategy`: 攻击策略
- `gap`: attack_f1 - baseline_f1（负值表示攻击有效）
- `relative_f1_drop`: -gap（正值表示攻击有效）
- `interpretation`: 人类可读的解释

### 3. Collateral 分析实现
```python
def analyze_collateral(method_filter=None, dataset_filter=None, model_filter=None):
    """读取 results/collateral/ 下的结果。"""
    import json
    from pathlib import Path

    results = []
    collateral_dir = Path("results/collateral")

    for method_dir in collateral_dir.iterdir():
        if not method_dir.is_dir():
            continue
        if method_filter and method_dir.name != method_filter:
            continue

        for dataset_dir in method_dir.iterdir():
            if dataset_filter and dataset_dir.name != dataset_filter:
                continue

            for model_dir in dataset_dir.iterdir():
                if model_filter and model_dir.name != model_filter:
                    continue

                # 读取最新的 collateral_*.json
                json_files = sorted(model_dir.glob("collateral_*.json"))
                if json_files:
                    latest = json_files[-1]
                    with open(latest) as f:
                        data = json.load(f)
                        for r in data.get("results", []):
                            r["method"] = method_dir.name
                            r["dataset"] = dataset_dir.name
                            r["model"] = model_dir.name
                            results.append(r)

    return results
```

**输出字段**：
- `strategy`: 攻击策略
- `perf_before`: 遗忘前 F1
- `perf_retrain`: 重训练 F1
- `perf_unlearn`: 近似遗忘 F1
- `gap`: perf_retrain - perf_unlearn
- `gap_pct`: gap 百分比
- `mean_pred_shift`: 留存节点预测概率平均偏移
- `max_pred_shift`: 最大偏移
- `fraction_flipped`: 预测翻转比例

### 4. 筛选支持
支持按以下维度筛选：
- `--method GIF`: 只分析特定方法
- `--dataset cora`: 只分析特定数据集
- `--model GCN`: 只分析特定模型
- `--strategy hybrid`: 只分析特定策略

### 5. 高副作用配置识别
在 Collateral 分析中，标记以下情况：
- `gap > 0.02` 或 `gap_pct > 2%`: 高 retrain gap
- `mean_pred_shift > 0.02`: 高预测偏移
- `fraction_flipped > 0.01`: 高翻转比例

## 数据源路径

| 用途 | 路径 |
|------|------|
| 实验结果 | `results/experiments/*/_summary.json` |
| Relative 缓存 | `results/relative/{Method}/{Dataset}/{Model}/*.json` |
| Collateral 结果 | `results/collateral/{method}/{dataset}/{model}/*.json` |
| 实验日志 | `results/_journal/auto_report.md` |

## 上下文
- 结果目录: results/
- 实验计划: self/宏观plan.md

用户输入: $ARGUMENTS
