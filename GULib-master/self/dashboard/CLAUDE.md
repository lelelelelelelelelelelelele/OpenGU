# self/dashboard/ — 编排与投影边界

> Last updated: 2026-08-26

## 文件分工

| 文件 | 权威内容 | 维护方式 |
|---|---|---|
| `WORKPLAN.md` | 做什么、优先级、依赖、当前唯一执行线、下一步 | 节点表手写；状态区由生成器重建 |
| `.workblock/items/*/WORKITEM.md` | Todo/Block 身份与生命周期状态 | WorkBlock workflow |
| `progress.html` | WORKPLAN + WorkItem 的可视化投影 | `scripts/dashboard/refresh.py` 生成，禁止手改 |
| `EXPERIMENT_DASHBOARD.md` | 2026-05-07 冻结的历史覆盖与缺陷档案 | 只读 |
| `VALIDATION_LOG.md` | append-only 验证 finding | 只追加；纠错用 superseded 记录 |
| `config_inventory.csv/.html` | 实验配置覆盖数据与派生视图 | CSV/生成器各自维护 |

## 事实 owner

- 科学问题、实验计划、selector/metrics 论证、矩阵解释和论文内容由 [OpenGU DocMap](../../../../OpenGU-DocMap/_文档地图.md) 及对应论文入口拥有；WORKPLAN 只保留短节点与唯一 owner 链接。
- YAML/recipe 只保存最终可执行配置，不承担人类实验计划或运行结论。
- 正式运行事实归 evidence、journal、acceptance/report；不得倒灌到 WORKPLAN。
- 修复节点关闭后从活动投影隐藏，历史由 WorkItem、验收记录与 Git 保留。

## 重建与验证

```powershell
python -B -X utf8 scripts/dashboard/refresh.py
python -B -X utf8 scripts/dashboard/refresh.py --check
python -B -X utf8 -m unittest tests.test_dashboard_refresh -v
```

生成器必须从 WorkItem 读取状态，并检测失效链接、重复映射、未映射 WorkItem、关闭节点占用当前线、未满足依赖和 Todo stale-blocked 漂移。修改事实源或生成器后重建派生物；不要手改 `progress.html` 或 WORKPLAN 的生成状态区。
