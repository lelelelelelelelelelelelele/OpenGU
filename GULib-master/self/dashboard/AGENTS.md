# Dashboard — 编排与投影边界

本文件管理 `self/dashboard/`，仓库级规则见 [根 AGENTS.md](../../AGENTS.md)。

## 文件分工

| 文件 | 权威内容 | 维护方式 |
|---|---|---|
| [WORKPLAN.md](WORKPLAN.md) | 做什么、优先级、依赖、当前唯一执行线、下一步 | 节点表手写；状态区由生成器重建 |
| [WorkItems](../../.workblock/items/) | Todo/Block 身份与生命周期状态 | WorkBlock workflow；不要从旧报告或分支名推断状态 |
| `progress.html` | WORKPLAN + WorkItem 的可视化投影 | [refresh.py](../../scripts/dashboard/refresh.py) 生成，禁止手改 |
| [EXPERIMENT_DASHBOARD.md](EXPERIMENT_DASHBOARD.md) | 2026-05-07 冻结的历史覆盖与缺陷档案 | 只读，不承担当前状态 |
| [VALIDATION_LOG.md](VALIDATION_LOG.md) | append-only 验证 finding | 只追加；纠错用新的 superseded 记录，不重写、重排或删除旧条目 |
| `config_inventory.csv` | 配置与证据状态清单 | 只根据已核对的证据更新，再重建 HTML |
| `config_inventory.html` | CSV 的派生视图 | [gen_config_inventory.py](../../scripts/dashboard/gen_config_inventory.py) 生成，禁止手改 |

## 事实归属

- 科学问题、实验计划、selector/metrics 论证、矩阵解释和论文内容由
  [OpenGU DocMap](../../../../OpenGU-DocMap/_文档地图.md) 及对应论文入口拥有；
  WORKPLAN 只保留短节点与唯一 owner 链接。
- YAML/recipe 只保存最终可执行配置，不承担人类实验计划或运行结论。
- 正式运行事实归 evidence、journal、acceptance/report；不得倒灌到 WORKPLAN。
  AutoReport 的事件与投影分工见 [V3 设计](../../docs/auto_report_v3_DESIGN.md)。
- 修复节点关闭后从活动投影隐藏，历史由 WorkItem、验收记录与 Git 保留。
- 任务涉及当前编排时读取 WORKPLAN，不恢复旧的每次会话强制通读看板要求。

## 修改范围

- 通过事实源或生成器修改派生文件，审查重建后的 diff。
- 目录说明只定义维护规则，不抄写当前任务清单、实验定义、指标结论或运行状态。
- 文档与生成器不一致时，先核对事实源、生成器及其验证；不能因整理文档就改变
  WORKPLAN 的任务内容、生命周期事实、实验定义或历史验证记录。
- 历史资料保留其适用日期和版本；不要把某次验收报告解释成当前实验已经完成。

## 重建与验证

从 `GULib-master/` 使用项目 Python 运行：

```powershell
python -B -X utf8 scripts/dashboard/refresh.py
python -B -X utf8 scripts/dashboard/refresh.py --check
python -B -X utf8 -m unittest tests.test_dashboard_refresh -v
```

生成器必须从 WorkItem 读取状态，并检测失效链接、重复映射、未映射 WorkItem、关闭节点占用当前线、未满足依赖和 Todo stale-blocked 漂移。修改事实源或生成器后重建派生物；不要手改 `progress.html` 或 WORKPLAN 的生成状态区。

配置清单变更使用其对应生成器，并运行
`python -B -X utf8 -m pytest -q tests/test_config_inventory_dashboard.py`。
仅修改说明文件时检查链接与规则一致性，不为此改写生成物。
