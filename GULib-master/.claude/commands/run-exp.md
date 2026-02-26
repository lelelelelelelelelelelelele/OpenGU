# 运行实验

根据用户指定的参数运行攻击实验，并将结果写入标准位置。

## 实验流程
1. 解析用户输入的实验参数
2. 确认实验配置（数据集、模型、遗忘方法、攻击策略、unlearn ratio）
3. 构造并执行命令
4. **NEW**: 如有需要，自动触发 `eval_relative.py` 计算 relative 指标
5. **NEW**: 如有需要，自动触发 `eval_collateral.py` 计算 collateral 指标
6. 收集结果并写入 `results/` 目录
7. 追加实验记录到 `results/_journal/auto_report.md`（见下方规范）
8. 输出结构化结果摘要

## 结果写入规范
- 路径: `results/{attack_strategy}/{unlearning_method}/{dataset}/{model}/`
- 文件名: `run_{timestamp}.json`
- JSON 格式:
```json
{
  "config": {
    "dataset": "cora",
    "model": "GCN",
    "unlearning_method": "GIF",
    "attack_strategy": "hybrid",
    "unlearn_ratio": 0.1,
    "num_unlearned_nodes": 270,
    "seed": 2024
  },
  "metrics": {
    "f1_before": 0.82,
    "f1_after": 0.45,
    "f1_drop": 0.37,
    "f1_drop_pct": 45.1,
    "mia_auc": 0.73,
    "selection_time_s": 12.3,
    "unlearn_time_s": 5.6
  },
  "relative_metrics": {
    "gap": -0.0153,
    "relative_f1_drop": 0.0153,
    "interpretation": "attack effective: F1 significantly lower than baseline",
    "baseline_f1_after": 0.8801,
    "attack_f1_after": 0.8648
  },
  "collateral_metrics": {
    "perf_before": 0.8930,
    "perf_retrain": 0.8764,
    "perf_unlearn": 0.8648,
    "gap": 0.0116,
    "gap_pct": 1.32,
    "mean_pred_shift": 0.0156,
    "max_pred_shift": 0.4858,
    "fraction_flipped": 0.0079
  },
  "selected_nodes": [12, 45, 78, ...]
}
```

## auto_report.md 追加规范

每次实验完成后（无论成功或失败），必须追加一条记录到 `results/_journal/auto_report.md`。

遵循 `results/_journal/RULES.md` v1/v2 模板格式：

```md
### [YYYY-MM-DD HH:MM:SS] /run-exp
- 任务：dataset=<dataset>, model=<model>, method=<method>, strategy=<strategy>, ratio=<ratio>
- 日志路径：`results/<strategy>/<method>/<dataset>/<model>/run_<timestamp>.json`
- 执行结果：<status> | f1_before=<f1_before> | f1_after=<f1_after> | f1_drop=<f1_drop> | drop_ratio=<vs_random>x | selection_time=<time>s | unlearn_time=<time>s
- **NEW**: Relative | gap=<gap> | relative_f1_drop=<relative_f1_drop> | interpretation=<interpretation>
- **NEW**: Collateral | retrain_gap=<gap> | gap_pct=<gap_pct>% | mean_pred_shift=<mean_pred_shift> | fraction_flipped=<fraction_flipped>
- 异常与定位：<error_type>: <error_msg> 或 无
- 下一步建议：<one actionable sentence>
```

**状态字典**: OK / WARN / X / TIMEOUT（同 RULES.md v1）

**注意事项**:
- 使用 Bash `cat >> results/_journal/auto_report.md << 'EOF' ... EOF` 追加，不要覆盖
- 时间戳取实验完成时刻
- 如果是多策略批量运行，每个策略单独一条，或用一条汇总（列出所有策略的 drop 值）
- 失败实验也要记录（status=X），方便排查

## 新增指标计算

### Relative 指标（vs random baseline）
```bash
H:/conda_package/envs/gnn/python.exe experiments/baseline_k5/eval_relative.py \
    --unlearning_methods <method> \
    --dataset_name <dataset> \
    --base_model <model> \
    --strategies <strategy> \
    --unlearn_ratio <ratio>
```
输出字段：
- `gap`: attack_f1 - baseline_f1（负值表示攻击有效）
- `relative_f1_drop`: -gap（正值表示攻击有效）
- `interpretation`: 人类可读的解释

### Collateral 指标（retrain gap + 留存节点扰动）
```bash
H:/conda_package/envs/gnn/python.exe eval_collateral.py \
    --dataset_name <dataset> \
    --base_model <model> \
    --unlearning_methods <method> \
    --strategies <strategy> \
    --unlearn_ratio <ratio>
```
输出字段：
- `gap`: perf_retrain - perf_unlearn
- `gap_pct`: gap 百分比
- `mean_pred_shift`: 留存节点预测概率平均偏移
- `fraction_flipped`: 预测翻转比例

## 汇报格式（输出到终端）
```
========== Experiment Report ==========
Strategy:  hybrid (alpha=0.5, rank-based)
Target:    GIF on Cora (GCN)
Unlearn:   270 nodes (10%)
---
F1 Before: 0.8200
F1 After:  0.4500
F1 Drop:   -45.1%
MIA AUC:   0.7300
---
Relative:  gap=-0.0153 | vs_baseline=1.8x
Collateral: gap=0.0116 (1.32%) | pred_shift=0.0156 | flipped=0.79%
Time:      12.3s (select) + 5.6s (unlearn)
========================================
[✓] Logged to results/_journal/auto_report.md
```

## 执行步骤

> **重要**：所有 Python 命令必须使用完整路径 `H:/conda_package/envs/gnn/python.exe`，
> 不得使用 `conda activate gnn && python`（非交互式 bash 中 conda 不可用）。

### 1. 运行主实验
```bash
H:/conda_package/envs/gnn/python.exe demo_attack.py \
    --dataset_name <dataset> \
    --base_model <model> \
    --unlearning_methods <method> \
    --attack_strategies <strategy> \
    --unlearn_ratio <ratio> \
    --random_seed <seed>
```

### 2. 自动计算 Relative 指标
实验成功后，自动调用：
```bash
H:/conda_package/envs/gnn/python.exe experiments/baseline_k5/eval_relative.py \
    --unlearning_methods <method> \
    --dataset_name <dataset> \
    --base_model <model> \
    --strategies <strategy> \
    --unlearn_ratio <ratio> \
    --repair
```
- 从 `results/relative/{Method}/{Dataset}/{Model}/*.json` 读取缓存结果
- 提取 gap 和 relative_f1_drop

### 3. 自动计算 Collateral 指标
实验成功后，自动调用（使用 `--repair` 模式进行增量补全）：
```bash
H:/conda_package/envs/gnn/python.exe eval_collateral.py \
    --dataset_name <dataset> \
    --base_model <model> \
    --unlearning_methods <method> \
    --strategies <strategy> \
    --unlearn_ratio <ratio> \
    --repair
```
- 从缓存读取 selected_nodes
- 计算 retrain gap 和 collateral damage
- 结果保存到 `results/collateral/{method}/{dataset}/{model}/`
- `--repair` 模式会扫描已有结果，跳过已计算的策略，只补全缺失的部分

**注意**: 如需预览哪些策略会被补全而不实际执行，可使用 `--repair_dry_run`:
```bash
python eval_collateral.py ... --repair_dry_run
```

### 4. 整合结果并写入
读取以上两个评估脚本的输出，整合到统一的 JSON 文件：
```json
{
  "config": { ... },
  "metrics": { ... },
  "relative_metrics": { ... },
  "collateral_metrics": { ... },
  "selected_nodes": [ ... ]
}
```
保存路径: `results/{strategy}/{method}/{dataset}/{model}/run_{timestamp}.json`

### 5. 追加到 auto_report.md
调用 `scripts/evaluation/reporting/writer.py::append_collateral_entry()` 追加记录。

## 参数映射

| 用户输入 | 主实验参数 | eval_relative 参数 | eval_collateral 参数 |
|----------|-----------|-------------------|---------------------|
| `dataset=cora` | `--dataset_name cora` | `--dataset_name cora` | `--dataset_name cora` |
| `model=GCN` | `--base_model GCN` | `--base_model GCN` | `--base_model GCN` |
| `method=GIF` | `--unlearning_methods GIF` | `--unlearning_methods GIF` | `--unlearning_methods GIF` |
| `strategy=hybrid` | `--attack_strategies hybrid` | `--strategies hybrid` | `--strategies hybrid` |
| `ratio=0.05` | `--unlearn_ratio 0.05` | `--unlearn_ratio 0.05` | `--unlearn_ratio 0.05` |
| `seed=2024` | `--random_seed 2024` | `--random_seed 2024` | (使用默认或推断) |

## 文件位置

| 用途 | 路径 |
|------|------|
| 主实验脚本 | `demo_attack.py` |
| Relative 评估 | `experiments/baseline_k5/eval_relative.py` |
| Collateral 评估 | `eval_collateral.py` |
| Relative 缓存 | `results/relative/{Method}/{Dataset}/{Model}/*.json` |
| Collateral 结果 | `results/collateral/{method}/{dataset}/{model}/*.json` |
| 实验日志 | `results/_journal/auto_report.md` |

用户输入: $ARGUMENTS
