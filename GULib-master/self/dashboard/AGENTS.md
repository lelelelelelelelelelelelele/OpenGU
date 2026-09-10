# Dashboard — 实验清单与证据入口

仓库级规则见 [根 AGENTS.md](../../AGENTS.md)。

## 文件分工

| 文件 | 拥有的内容 | 维护方式 |
|---|---|---|
| [experiment_inventory.json](experiment_inventory.json) | 研究部分、配置单/结果/分析链接及明确核对日期的实验快照 | 按已核对来源显式更新；不读取 Block 生命周期推断运行或分析 |
| [config_inventory.csv](config_inventory.csv) | 历史配置覆盖与证据计数 | 保留历史口径，不混入本轮运行完成数 |
| [config_inventory.html](config_inventory.html) | 以上两源的实验清单与 Coverage Heatmap | [gen_config_inventory.py](../../scripts/dashboard/gen_config_inventory.py) 与 [模板](../../scripts/dashboard/inventory.html) 生成，禁止手改 |
| [WorkItems](../../.workblock/items/) / [graph](../../.workblock/graph.json) | 任务合同/生命周期及协议定义的阶段与依赖 | 由 WorkBlock / Companion 维护，不生成 tracked 任务看板 |
| [EXPERIMENT_DASHBOARD.md](EXPERIMENT_DASHBOARD.md) | 冻结的历史覆盖与缺陷档案 | 不承担当前状态 |
| [VALIDATION_LOG.md](VALIDATION_LOG.md) | append-only 验证 finding | 只追加，纠错用 superseded，不重写历史 |

## 维护边界

- 科学论证与正式分析由 [OpenGU DocMap](../../../../OpenGU-DocMap/_文档地图.md) 和对应报告拥有；实验清单只组织短问题和源链接。YAML 仍拥有可执行定义。
- 运行快照必须绑定明确 experiment_id、run_id、代码版本、manifest 摘要与条件数。结果存在不等于有效，运行结束不等于分析完成或科学接受。
- 已关联记录可以覆盖多次尝试；重试按同一逻辑条件去重，不能累加成额外完成数。新的配置/数据/代码身份需要重新核对，不能沿用旧的完成声明。
- `unknown` 表示未核对，不能当成零；只有已绑定配置、显式零完成的条目可登记 pending。分析可综合多张配置；其状态来自分析来源，不来自 Block 状态。
- 历史 CSV 缺失 valid 等字段表示未登记，不以 done 填充可用数；历史配置重叠，不汇总成独立 cell 总数或本轮总完成率。
- 普通 Block 新增、编辑、推进状态不需要修改或刷新本清单，不触发代码仓库提交。这里没有 pre-commit 自动刷新/暂存步骤，也不调用执行器或连接实时队列。
- WORKPLAN、progress.html、PROGRESS.md 与旧 refresh.py 已移除，历史在 Git。任务入口是现有 WorkBlock / Companion；研究入口是 config inventory 和 DocMap。旧报告中的路径按其日期阅读，不恢复旧权威。

## 重建与验证

```powershell
python -B -X utf8 scripts/dashboard/gen_config_inventory.py
python -B -X utf8 scripts/dashboard/gen_config_inventory.py --check
python -B -X utf8 scripts/dashboard/gen_config_inventory.py --check --check-links --verify-evidence
python -B -X utf8 -m pytest -q tests/test_config_inventory_dashboard.py
```

常规重建只读取清单与历史配置路径，不读取 WorkItem 正文或运行结果；没有日期自动变动。`--check-links` 核对当前设备源路径；`--verify-evidence` 额外核验明确绑定的运行身份与结果哈希，不扫描猜测其他运行，也不启动实验。没有本地证据包的设备不能宣称已完成这项核验。
