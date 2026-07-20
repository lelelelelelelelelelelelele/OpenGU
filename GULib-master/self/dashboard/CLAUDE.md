# self/dashboard/ — Single Source of Truth

> Created: 2026-05-03
> Last updated: 2026-07-20
> Role: 实验状态、metrics、bug、findings 的**唯一权威落点**。其他文档（thesis_transition_memo、PROJECT_MASTER_CONTEXT 等）应**链接到此**，不应复制内容。

## 文件分工

| 文件 | 内容 | 维护方式 | 读取时机 |
|------|------|---------|---------|
| `WORKPLAN.md` | **当前阶段唯一操作中枢**：现状快照 + 硬伤 C1–C5 + 方向 + 实验/ablation/写作/画图 四阶段任务计划 + 链接索引；生成 `progress.html` | **手写**（改完跑 `refresh.py` 或靠 pre-commit hook 重生看板） | **每次开 session 第一件事（2026-06-27 起）** |
| `progress.html` | WORKPLAN.md 的可视化看板（派生快照，**别手改**） | `scripts/dashboard/refresh.py` 生成 | 扫一眼进度 |
| `PROGRESS.md` | ⚠️ **已退役 2026-06-27**：内容并入 `WORKPLAN.md`，只留指针 | 不再更新 | 旧链接落地点 |
| `EXPERIMENT_DASHBOARD.md` | ⚠️ **FROZEN 2026-05-07**：历史 coverage 矩阵 + bug 档案 | 不再更新；只读参考 | 查历史覆盖 / pre-Phase-B bug 溯源 |
| `METRICS_CATALOG.md` | 6 个 v2 metric 的定义 + 实测覆盖 + bug 位置 + v3 候选 | **半手写**：metric 定义稳定，状态字段每日更新 | 写 paper §metric / 修 metric bug 时 |
| `VALIDATION_LOG.md` | append-only 实证 finding 与 sanity check 记录 | **append-only**，禁止删改历史条目 | 验证假说 / 引用证据时 |
| `config_inventory.csv` / `.html` | cell 级 produced、local usable、accepted-remote/archive-pending、rerun 四态看板 | CSV 为数据源，HTML 由 `scripts/dashboard/gen_config_inventory.py` 生成 | 判断实验能否本地复核与下一步 rerun/import |
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
| `report/progress/2026-04-17_EE5003-report/` | 课程报告快照，已冻结 |
| `results/_journal/auto_report.md` / `.html` / `auto_report.events.jsonl` | `auto_report.md/.html` 是有限当前视图，JSONL 是 append-only V3 审计；v1/v2 原文在 `results/_journal/archive/`，baseline 只携带仍有用的事实和失效边界；本目录的 VALIDATION_LOG 是**人/AI 验证类**的对位 |

## 何时不要用本目录

- 写 paper 正文 → 写到 `report/<某 paper 目录>/`
- 跑实验配置 → 写到 `scripts/experiments/`
- 实验自动产出日志 → 让 pipeline 写到 `results/_journal/`
