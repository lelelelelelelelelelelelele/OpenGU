# Report Folder - 组会汇报材料

本目录用于组织研究组会汇报材料，包括每日工作日志、组会报告、阶段报告和论文内容。

## 目录结构

```
report/
├── daily-log/              # 每日工作日志
│   ├── 2026-02-16_log.md
│   ├── 2026-02-17_log.md
│   ├── 2026-02-18_log.md
│   ├── 2026-02-19_log.md
│   └── 2026-02-21_log.md
├── meeting/               # 组会报告
│   └── 2026-02-19_算力与数据集规模.md
├── progress/              # 阶段报告
│   └── 2026-02-19_checkpoint/
│       ├── PROGRESS_REPORT.md
│       ├── appendix_demo_output.txt
│       ├── appendix_method_table.md
│       └── figures/
├── paper/                 # 论文内容
│   ├── sections/          # 各章节（待添加）
│   └── figures/           # 图表资源（待添加）
└── README.md              # 本文档
```

## 参考资源

以下文件包含项目核心背景和规划信息：

| 文件 | 位置 | 说明 |
|------|------|------|
| 项目背景 | `self/PROJECT_MASTER_CONTEXT.md` | GNN Unlearning 攻击研究背景 |
| 研究规划 | `self/宏观plan.md` | 长期研究规划 |
| 函数设计 | `self/flow.md` | 函数级设计、输入输出规格 |
| 实验结果 | `results/` | 各类实验数据 |

## 实验结果目录 (`results/`)

| 目录 | 说明 |
|------|------|
| `step0_validation/` | 初始验证结果 |
| `experiments/` | 批量实验结果 (phase_a) |
| `collateral/` | 附带损伤评估结果 |
| `checkpoint_report/` | 已移动至 `report/progress/` |

## 使用说明

### 添加新的组会报告

将组会报告复制到 `report/meeting/` 目录，命名格式：`YYYY-MM-DD_主题.md`

### 添加阶段报告

在 `report/progress/` 下创建新目录，命名格式：`YYYY-MM-DD_描述/`

### 添加论文章节

在 `report/paper/sections/` 下创建对应章节文件

## 更新日志

- 2026-02-22: 初始化 report 目录结构，移动 daily-log 和 checkpoint_report
