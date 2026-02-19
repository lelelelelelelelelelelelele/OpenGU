# 运行实验

根据用户指定的参数运行攻击实验，并将结果写入标准位置。

## 实验流程
1. 解析用户输入的实验参数
2. 确认实验配置（数据集、模型、遗忘方法、攻击策略、unlearn ratio）
3. 构造并执行命令
4. 收集结果并写入 `results/` 目录
5. 追加实验记录到 `results/_journal/auto_report.md`（见下方规范）
6. 输出结构化结果摘要

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
- 异常与定位：<error_type>: <error_msg> 或 无
- 下一步建议：<one actionable sentence>
```

**状态字典**: OK / WARN / X / TIMEOUT（同 RULES.md v1）

**注意事项**:
- 使用 Bash `cat >> results/_journal/auto_report.md << 'EOF' ... EOF` 追加，不要覆盖
- 时间戳取实验完成时刻
- 如果是多策略批量运行，每个策略单独一条，或用一条汇总（列出所有策略的 drop 值）
- 失败实验也要记录（status=X），方便排查

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
Time:      12.3s (select) + 5.6s (unlearn)
========================================
[✓] Logged to results/_journal/auto_report.md
```

用户输入: $ARGUMENTS
