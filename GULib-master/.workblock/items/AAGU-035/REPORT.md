# AAGU-035 · 多数据集实验矩阵验收

## Human Result

### 实际增量

普通 YAML 现在统一使用 dataset_refs 列表，按数据集独立执行、汇总和回传。extension v2 三张表合为一张：3 × 10 × 1 × 3 × 4 = 360 条件，保留原有 288 条件并增加 72 条件。

[打开合并 YAML](../../../experiments/configs/aagu032_extend_v2/experiment.yaml)

### 核心观察

| 判断 | 实际观察 | 结果 |
|---|---|---|
| 矩阵与划分 | 三数据集统一表 dry-run 为 360 条件、36 个 seed/比例批次；均保持 70/10/20、split seed 2024。 | PASS |
| 实际 CPU 链路 | 两个独立临时图（20/24 节点）完成 16 个 GNNDelete/Retrain 条件；实际 train/val/test mask、删除集合及预测产物归属一致。 | PASS |
| 缓存隔离 | 首次单图运行后加入第二图，原图 Score/Selection/Output 全部 HIT；改名、重排后仍 HIT。只改变第二图 split 后重新计算，第一图保持 HIT。 | PASS |
| 真实收集 | Core 实际队列 → 普通入口 → 本地 transport 收集 → SHA-256/index → OpenGU 验收，65 个文件、16 个 cell 通过；结果表正确显示数据集、seed 和比例。缺失、重复、错误归属均拒绝。 | PASS |
| 独立指标 | 普通 Metrics 入口按两个 Dataset/Split 读取已导出输出并计算指标，未调用 Selector producer。 | PASS |

### 当前决定

建议接受：本 Block 的 practical 软件与配置验收已有实际证据。由用户决定接受或返工；360 条件科研矩阵未运行，本报告不作科研效果判断。

> 当前验收决定：`接受`

## 核验入口

完整测试检查点：`f865dd0240b4a28f1b8178fa2aac4e70f752ebfd`。消费者与矩阵 110 项、SyncMate 205 项，共 **315 项通过**；6 份实验 recipe 指纹匹配，16 个变更文档本地链接有效。

[查看实际身份、HIT/MISS、producer_called 和产物哈希](evidence/verification.json)。完整测试后只补验收报告和同一 WorkItem 投影，最终候选为本报告所在 source branch 的干净 HEAD；这些展示变化复用上述测试证据，并单独检查报告结构、链接和渲染。

| Dataset | split hash 前 16 位 |
|---|---|
| Cora | `246ce2ffe94f40b2` |
| CiteSeer | `b8877443252d36d5` |
| PubMed | `6ec0440916aefbd5` |

HTML 结构与本地链接检查 PASS；浏览器 URL 安全策略拒绝打开本地 HTML，因此视觉渲染为 **NOT OBSERVED**。本次以 Markdown 作为验收入口。

完整 manifest 摘要、split hash 和每个批次的数据集指纹见 evidence。未改变公共 Selector、SGC、训练参数或算法；未启动正式 GPU、合并或推送。
