# self/dashboard/ — Single Source of Truth

> Created: 2026-05-03
> Role: 实验状态、metrics、bug、findings 的**唯一权威落点**。其他文档（thesis_transition_memo、PROJECT_MASTER_CONTEXT 等）应**链接到此**，不应复制内容。

## 4 个文件的分工

| 文件 | 内容 | 维护方式 | 读取时机 |
|------|------|---------|---------|
| `EXPERIMENT_DASHBOARD.md` | phase 进度 + coverage 矩阵 + 已知问题 + 当前 TODO | **手写**，每完成一项任务即时更新 | 每次开 session 第一件事 |
| `METRICS_CATALOG.md` | 6 个 v2 metric 的定义 + 实测覆盖 + bug 位置 + v3 候选 | **半手写**：metric 定义稳定，状态字段每日更新 | 写 paper §metric / 修 metric bug 时 |
| `VALIDATION_LOG.md` | append-only 实证 finding 与 sanity check 记录 | **append-only**，禁止删改历史条目 | 验证假说 / 引用证据时 |
| `CLAUDE.md`（本文件） | 这些文件本身的使用规则 | 几乎不变 | 第一次进入此文件夹 |

## 维护铁律

1. **每个文件顶部必须有 `Last updated: YYYY-MM-DD`**——4 天 NeurIPS deadline 期间一日多次更新很正常
2. **不许把 dashboard 内容复制到其他 markdown**——只能引用路径，避免 drift
3. `VALIDATION_LOG.md` 是 append-only。已有条目错了不删，标 `**SUPERSEDED**` + 新条目纠正
4. coverage 矩阵的"自动生成"段在 `scripts/dashboard/refresh.py`（待建）跑出来之前，**手写允许，但每次更新必须同步 timestamp**

## 与其他文档的关系

| 文档 | 关系 |
|------|------|
| `self/thesis_transition_memo.md` | thesis 战略层；执行细节链接到本目录 |
| `self/plan_flow_v2_delta.md` | 设计原典；本目录的 METRICS_CATALOG 是它的"实测投影" |
| `self/PROJECT_MASTER_CONTEXT.md` | 早期背景，已冻结；不再受本目录影响 |
| `report/0417_5003report/` | 课程报告快照，已冻结 |
| `results/_journal/auto_report.md` | 自动实验日志（pipeline 写入）；本目录的 VALIDATION_LOG 是**人/AI 验证类**的对位 |

## 何时不要用本目录

- 写 paper 正文 → 写到 `report/<某 paper 目录>/`
- 跑实验配置 → 写到 `scripts/experiments/`
- 实验自动产出日志 → 让 pipeline 写到 `results/_journal/`
