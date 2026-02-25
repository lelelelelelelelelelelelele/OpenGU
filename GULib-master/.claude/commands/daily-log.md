# 生成每日工作日志

当用户输入 `/daily-log` 或明确要求生成工作日志时，自动生成今日工作总结。

## 功能说明

生成markdown格式的工作日志，记录：
- 任务概览与完成情况
- 关键发现与技术洞察
- 实验数据与代码变更统计
- 遗留问题与明日计划
- 成本统计（如果使用了API）

## 使用方式

```bash
# 生成今日日志（默认）
/daily-log

# 生成指定日期的汇总日志（包含上次日志后到指定日期的所有内容）
/daily-log 2026-02-18
```

或者用户说：
- "生成今天的工作日志"
- "总结一下今天的工作"
- "写一份今日报告"
- "生成18号的日志，把17号以来的内容都包含进去"

## 日期范围逻辑

1. **无参数**：
   - 默认进度从上一份 daily log 之后开始统计。
   - 先计算“工作日期”：
     - 当前本地时间 >= 06:00：工作日期 = 今天
     - 当前本地时间 < 06:00：工作日期 = 昨天（按加班归属前一天）
   - 文件名使用“工作日期”，不是系统当前自然日。
2. **有日期参数**（如 `2026-02-18`）：
   - 查找 `report/daily-log/` 目录下最新的已有日志文件（如 `2026-02-16_log.md`）
   - 生成 **(最新日志日期+1天)** 到 **指定日期** 期间的所有内容汇总
   - 所有内容合并输出到 **指定日期** 的日志文件中
   - 例如：最新日志是 `2026-02-16`，用户输入 `/daily-log 2026-02-18`，则将17号和18号两天的内容合并生成到 `2026-02-18_log.md`

## 输出格式

**文件名**: `YYYY-MM-DD_log.md`
**位置**: `report/daily-log/` 目录
**日期显示**:
- 日志头部需显示 `工作日期: YYYY-MM-DD`
- 日志头部需显示 `生成时间: YYYY-MM-DD HH:mm`（本地时间）
- 若无参数且当前时间 < 06:00，则“工作日期”显示为前一天日期

**内容结构**:
1. 📋 任务概览
2. ✅ 已完成工作
3. 🔑 关键决策（从当天 `auto_report.md` 中提取 DECISION 条目汇总）
4. 🔍 关键发现
5. 📊 数据统计
   - 实验运行次数（按 method/strategy 分组）
   - **NEW**: Relative 指标统计（平均 improvement vs random）
   - **NEW**: Collateral 指标统计（平均 gap, pred_shift）

## Relative/Collateral 指标统计实现

### Relative 指标统计
```python
def compute_relative_stats(results_dir="results/relative"):
    """计算 relative 指标统计数据。"""
    import json
    import glob
    import numpy as np

    stats = {
        "by_method": {},
        "by_strategy": {},
        "overall": {"mean_improvement": 0, "count": 0}
    }

    improvements = []
    for cache_file in glob.glob(f"{results_dir}/*.json"):
        with open(cache_file) as f:
            data = json.load(f)
            for r in data.get("results", []):
                improvement = r.get("relative_f1_drop", 0)
                improvements.append(improvement)

                method = r.get("method", "unknown")
                strategy = r.get("strategy", "unknown")

                if method not in stats["by_method"]:
                    stats["by_method"][method] = []
                stats["by_method"][method].append(improvement)

                if strategy not in stats["by_strategy"]:
                    stats["by_strategy"][strategy] = []
                stats["by_strategy"][strategy].append(improvement)

    if improvements:
        stats["overall"]["mean_improvement"] = np.mean(improvements)
        stats["overall"]["count"] = len(improvements)

    return stats
```

### Collateral 指标统计
```python
def compute_collateral_stats(base_dir="results/collateral"):
    """计算 collateral 指标统计数据。"""
    import json
    from pathlib import Path
    import numpy as np

    stats = {
        "by_method": {},
        "overall": {"mean_gap": 0, "mean_pred_shift": 0, "count": 0}
    }

    gaps = []
    shifts = []

    base_path = Path(base_dir)
    if not base_path.exists():
        return stats

    for method_dir in base_path.iterdir():
        if not method_dir.is_dir():
            continue

        method_gaps = []
        method_shifts = []

        for dataset_dir in method_dir.iterdir():
            for model_dir in dataset_dir.iterdir():
                json_files = list(model_dir.glob("collateral_*.json"))
                if json_files:
                    latest = max(json_files, key=lambda p: p.stat().st_mtime)
                    with open(latest) as f:
                        data = json.load(f)
                        for r in data.get("results", []):
                            gap = r.get("gap", 0)
                            shift = r.get("mean_pred_shift", 0)
                            gaps.append(gap)
                            shifts.append(shift)
                            method_gaps.append(gap)
                            method_shifts.append(shift)

        if method_gaps:
            stats["by_method"][method_dir.name] = {
                "mean_gap": np.mean(method_gaps),
                "mean_pred_shift": np.mean(method_shifts),
                "count": len(method_gaps)
            }

    if gaps:
        stats["overall"]["mean_gap"] = np.mean(gaps)
        stats["overall"]["mean_pred_shift"] = np.mean(shifts)
        stats["overall"]["count"] = len(gaps)

    return stats
```

### 日志输出格式
```markdown
### 📊 数据统计

**实验运行统计**
- 总运行次数: 45
- 完成率: 85%
- 按方法: GIF(15), GNNDelete(15), GraphEraser(15)

**Relative 指标（vs Random Baseline）**
- 平均改进: 0.0823 (8.23%)
- 最佳方法: GNNDelete (mean=0.0956)
- 最佳策略: im (mean=0.1123)

**Collateral 损伤统计**
- 平均 Retrain Gap: 0.0116 (1.16%)
- 平均 Pred Shift: 0.0156
- 按方法统计:
  - GIF: gap=0.0023, shift=0.0089
  - GNNDelete: gap=0.0201, shift=0.0213
  - GraphEraser: gap=0.0087, shift=0.0123
```
6. 💡 经验总结
7. 📝 待办事项
8. 🔧 遗留问题
9. 📚 文档产出
10. 🎯 成果总结
11. 💰 成本统计（如有）
12. 📅 下次工作预告

## 注意事项

- 自动推断今日日期（YYYY-MM-DD格式）
- 涵盖完整对话中的所有工作
- 突出关键技术发现和研究洞察
- 记录具体数据（实验次数、代码行数、API成本等）
- 提供可操作的明日计划

## 示例

详见: `report/daily-log/2026-02-16_log.md`
