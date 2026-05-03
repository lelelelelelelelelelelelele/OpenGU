# Report Folder - 组会汇报材料

> Status: active
> Role: `report/` 目录说明；定义阶段性汇报、课程报告和答辩材料的存放边界。
> Use this when: 你要找某个阶段性的报告、演示稿、progress report 或分析性 writeup。
> See also: `../self/README.md`, `../results/README.md`, `0417_5003report/main_report/msc_project_report.md`

本目录用于组织**阶段性**研究输出，包括每日工作日志、组会报告、阶段报告、课程报告、答辩材料和阶段分析写作。

长期维护的研究方法论、假说、thesis 方向与流程骨架已经收束到 [`../self/`](../self/)；`report/` 不再承担“长期主入口”的角色。

## 目录结构

```
report/
├── 0417_5003report/          # 2026-04 EE5003 最终课程报告与答辩材料
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
├── paper/                     # 阶段性 paper-facing 草稿与汇报材料
└── README.md                  # 本文档
```

## 参考资源

以下目录分工建议作为当前默认口径：

| 目录 | 作用 |
|------|------|
| `self/` | 长期研究控制中心：方法论、研究逻辑、假说、thesis 方向 |
| `report/` | 阶段性输出：progress report、课程报告、答辩材料、组会笔记 |
| `results/` | 证据产物：实验结果、relative/collateral 结果、缓存与统计表 |

如果你要找项目核心背景与规划信息，优先从 `self/` 开始：

| 文件 | 位置 | 说明 |
|------|------|------|
| `self/README.md` | `self/README.md` | `self/` 主入口，说明当前阅读顺序与文档状态 |
| Thesis 过渡文档 | `self/thesis_transition_memo.md` | 当前 thesis 方向、假说与 proposed 收束入口 |
| 项目背景 | `self/PROJECT_MASTER_CONTEXT.md` | 早期统一背景与方法口径 |
| 函数设计 | `self/flow.md` | 方法与实现流程参考 |
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

如果是**阶段性** paper-facing 草稿，可放在 `report/paper/` 下。

如果是长期维护的 thesis 研究逻辑、假说、方法论与规划，请优先更新 `self/`。

## 更新日志

- 2026-02-22: 初始化 report 目录结构，移动 daily-log 和 checkpoint_report
- 2026-02-25: `analysis` 目录重构为 `reports/notes/assets/scripts` 分层，统一分析材料组织
- 2026-04-17: 明确 `report/` 为阶段性输出空间，长期研究入口迁移到 `self/`
