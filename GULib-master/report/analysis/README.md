# Analysis 目录说明

`report/analysis` 用于存放技术分析相关的全部材料，按职责分层：

```
analysis/
├── reports/         # 自动生成技术分析报告（脚本输出）
├── notes/           # 人工分析/组会笔记（Markdown）
├── assets/
│   ├── data/        # 图表输入数据（JSON）
│   └── figures/     # 图表输出（PNG）
└── scripts/         # 分析脚本
```

## 命名规范

- 自动报告：`YYYY-MM-DD_HHMMSS_{group}_analysis.md`
- 人工笔记：`YYYY-MM-DD_主题.md`

## 迁移映射（2026-02-25）

- `analysis/20260222_040557_mg0_completion_analysis.md` -> `analysis/reports/2026-02-22_040557_mg0_completion_analysis.md`
- `analysis/2026-02-22_IM_CELF性能瓶颈分析.md` -> `analysis/notes/2026-02-22_IM_CELF性能瓶颈分析.md`
- `analysis/meeting/*.md` -> `analysis/notes/*.md`
- `analysis/meeting/*.json` -> `analysis/assets/data/*.json`
- `analysis/meeting/*.png` -> `analysis/assets/figures/*.png`
- `analysis/meeting/generate_shard_figures.py` -> `analysis/scripts/generate_shard_figures.py`

## 历史路径说明

- 历史 `daily-log` 中可能仍引用旧路径（如 `report/meeting/`、`report/analysis/meeting/`）。
- 这些日志属于历史记录，保持原文不改；以当前目录结构和本文件说明为准。
