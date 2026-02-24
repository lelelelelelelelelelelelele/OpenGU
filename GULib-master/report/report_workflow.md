# 实验报告生成工作流

## 概述

本工作流用于从实验结果自动生成技术分析报告，包含：
1. 数据汇总与统计分析
2. 攻击效果评估
3. 问题识别
4. 改进建议

> 说明：本工作流保持独立，不并入 `scripts/evaluation` 的 Step0 CLI。

## 使用方式

```bash
# 生成报告（指定实验组）
python -m report_workflow generate --group mg0_completion

# 生成完整报告（所有实验组）
python -m report_workflow generate --all

# 仅分析数据，不生成报告
python -m report_workflow analyze --group mg0_completion

# 对比两个实验组
python -m report_workflow compare --group1 mg0_completion --group2 mg1_citeseer
```

## 工作流步骤

### Step 1: 数据收集

**输入：**
- `results/experiments/{group}/phase_a/*/_summary.json` - 实验汇总数据
- `results/collateral/` - 附带损伤数据

**处理：**
1. 遍历指定实验组的所有 `_summary.json`
2. 解析每个实验的：method, strategy, f1_drop, retrain_gap, mia_auc 等

### Step 2: 统计分析

**计算：**
- 按 method × strategy 聚合 f1_drop 的均值/标准差
- 计算不同 strategy 之间的相对效果
- 识别最大值/最小值

**输出中间结果：**
```json
{
  "method": "GNNDelete",
  "strategy": "im",
  "f1_drop_mean": 0.138,
  "f1_drop_std": 0.015,
  "sample_count": 5
}
```

### Step 3: 问题识别

**自动识别规则：**

| 问题类型 | 识别条件 | 标记 |
|----------|----------|------|
| 攻击无效 | f1_drop < 0.01 | ⚠️ 无显著效果 |
| 反向效果 | f1_drop < -0.05 | 🔄 反效应 |
| 效果不显著 | std > mean | 📊 波动大 |
| retrain_gap过大 | retrain_gap > 10% | 🛡️ 近似质量差 |

### Step 4: 改进建议生成

**基于问题类型的建议模板：**

| 问题 | 建议 |
|------|------|
| 攻击无效（Learning-based） | 提高 ratio，或尝试其他策略 |
| 攻击无效（Shard-based） | 设计 Shard-aware 策略 |
| 效果不显著 | 增加实验次数，或聚焦有效策略 |
| 反效应 | 分析防御机制，可作为防御启示 |

### Step 5: 报告渲染

**模板：** `report/templates/technical_analysis.md`

**填充内容：**
1. 实验概览表格
2. 核心发现（自动提取显著结果）
3. 问题诊断列表
4. 改进方向建议
5. 下一步行动建议

## 文件结构

```
report_workflow/
├── __init__.py
├── data_loader.py      # Step 1: 数据收集
├── analyzer.py         # Step 2: 统计分析
├── problem_detector.py # Step 3: 问题识别
├── advisor.py          # Step 4: 改进建议
├── generator.py        # Step 5: 报告渲染
├── templates/
│   └── technical_analysis.md
└── config.yaml         # 报告配置
```

## 报告输出

**位置：** `report/analysis/reports/{timestamp}_{group}_analysis.md`

**内容结构：**
```markdown
# {实验组} 技术分析报告

> 生成时间: {timestamp}

## 一、实验数据概览

| Method | Strategy | F1 Drop | Std | N |
|--------|----------|---------|-----|---|
| ... | ... | ... | ... | ... |

## 二、核心发现

### 2.1 最有效攻击组合
- {method} + {strategy}: {f1_drop}%

### 2.2 无效/反效应组合
- {method} + {strategy}: {f1_drop}% (反效应)

## 三、问题诊断

- ⚠️ {问题描述}
- 🔄 {问题描述}

## 四、改进建议

### 建议 1: {标题}
{描述}

## 五、下一步行动

- [ ] {任务}
```

## 配置选项

`config.yaml`:
```yaml
report:
  output_dir: "report/analysis/reports"
  template: "technical_analysis.md"

thresholds:
  significant_effect: 0.05   # 显著效果阈值
  reverse_effect: -0.03      # 反效应阈值
  high_variance: 0.5         # 高方差阈值 (std/mean)

groups:
  - name: "mg0_completion"
    label: "Cora/GCN 稳定性"
  - name: "mg1_citeseer"
    label: "Citeseer 数据集"
```

## 扩展建议

1. **对比功能**：自动对比两个实验组的差异
2. **图表生成**：自动生成热力图/柱状图
3. **自动归档**：将生成的报告移动到 `report/analysis/reports/`
4. **邮件通知**：生成后自动发送邮件
