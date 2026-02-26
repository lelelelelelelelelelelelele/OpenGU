# Report Folder - 组会汇报材料

本目录用于组织研究组会汇报材料，包括每日工作日志、组会报告、阶段报告和论文内容。

## 目录结构

```
report/
├── analysis/                  # 技术分析材料（统一入口）
│   ├── reports/               # 自动生成报告
│   ├── notes/                 # 人工分析/组会笔记
│   ├── assets/
│   │   ├── data/              # 图表输入数据（json）
│   │   └── figures/           # 图表输出（png）
│   ├── scripts/               # 分析脚本
│   └── README.md              # analysis 子目录说明
├── daily-log/                 # 每日工作日志
├── progress/                  # 阶段报告
├── paper/                     # 论文内容
└── README.md                  # 本文档
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
| `step0_validation/` | Step0 历史只读结果 |
| `evaluation/` | 统一评估产物（step0/attack/stats） |
| `experiments/` | 批量实验结果 (phase_a) |
| `relative/` | 相对评估结果（相对 random baseline 的 F1 drop） |
| `collateral/` | 附带损伤评估结果 |
| `cache/` | ResultCache（按配置哈希缓存） |
| `selection_cache/` | SelectionCache（选点缓存，跨方法复用） |
| `checkpoint_report/` | 已移动至 `report/progress/` |

Step0 工具代码已统一到 `scripts/evaluation/`，入口为 `python -m scripts.evaluation`。

## 使用说明

### 添加新的分析/组会笔记

将文档放到 `report/analysis/notes/`，命名格式：`YYYY-MM-DD_主题.md`

### 添加新的自动分析报告

自动生成脚本默认写入 `report/analysis/reports/`，命名格式：`YYYY-MM-DD_HHMMSS_{group}_analysis.md`

### 添加阶段报告

在 `report/progress/` 下创建新目录，命名格式：`YYYY-MM-DD_描述/`

### 添加论文章节

在 `report/paper/sections/` 下创建对应章节文件

## 更新日志

- 2026-02-22: 初始化 report 目录结构，移动 daily-log 和 checkpoint_report
- 2026-02-25: `analysis` 目录重构为 `reports/notes/assets/scripts` 分层，统一分析材料组织
