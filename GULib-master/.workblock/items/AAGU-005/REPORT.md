# AAGU-005 · OpenGU 与 SyncMate 接入修复

## Human Result

### 实际增量

已修复 OpenGU 消费端的预检参数、静态配置摘要、GNNDelete / Retrain 产物声明、收集后校验与结果表读取。20 个 GU 配方直接复用执行器的文件清单；无需在每个方法结果中生成 collateral.json。

### 核心观察

311 项相关检查通过。20/20 正式 GU 配方与执行器一致，6/6 原子配方保持一致。临时 CPU 图上真实运行两种方法，再经 SyncMate 收集、SHA 校验、OpenGU 接受检查及结果表读取；重复收集新增 0 个文件。12 类错误均被拒绝。

### 当前决定

建议接受 AAGU-005 本轮约定的代码正确性与 CPU 接入验证范围。旧版 GPU 实测仅作为历史证据；本次修复尚未在远端 GPU 上重跑，也尚未合入或部署。当前由用户作验收决定。

> 当前验收决定：`待决定`

## 此前已经交付的 OpenGU 改动

| 内容 | 已实现行为 | 主要位置 |
|---|---|---|
| 原子实验入口与配方 | Degree、B-Hutch first/warm、D-full Selector-only、自动回传及新版 handoff 共 6 个固定配方，绑定配置摘要、运行身份与输出。 | experiments/syncmate_atomic_stage.py；scripts/syncmate/opengu_recipes.py |
| 启动参数隔离 | 隔离 --recipe，避免被 OpenGU import-time 参数解析误读。失败与拒绝不会进入训练。 | experiments/syncmate_atomic_stage.py |
| 输出交接 | 配方与执行器共用 modular_output_path；执行前核对 queue receipt 的 output_contract。 | scripts/syncmate/opengu_layout.py；experiments/modular_execution.py |
| Core 安装身份 | 消费端核对 0.4.0 的完整文件集合与内容哈希；设备配置保留接入事实，项目代码拥有结果规则。 | scripts/syncmate/core_dependency.json；verify_core_dependency.py；opengu_adapter.py |

最后一轮输出交接覆盖 13 个文件；本轮承接这些既有 Git 交付，并修复当前正式 GU 消费端。

## 真实运行证据与适用范围

### Degree → GNNDelete → utility

真实 RTX 4090 运行、返回 summary 并校验；重复收集为 0。

版本：`OpenGU 93e6e56b / Core 0.3.1`。证明该版本真实执行与回传链。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/verify-final.json)

### B-Hutch 32 probes first / warm

Score、Selection、GU 首遍 MISS，热读 HIT 且 producer=false；传输校验通过。原记录保留 F1 差值读回失败。

版本：`OpenGU 6dc1aa92 / Core 0.3.1`。复用缓存与传输证据；不把旧指标失败改成 PASS。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/b-hutch32/cache-comparison.json)

### D-full Selector-only

1895 个有限分数、完整降序排名、18 个节点；1 Selector / 0 GU / 0 Evaluation。

版本：`OpenGU 53e1da5b / Core 0.3.1`。证明该版本 Selector 输出和回传。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/d-full/verification.json)

### D-full warm 自动回传

checkpoint / Score / Selection 全 HIT，producer=false；同一后台流程完成回传和 SHA 校验。

版本：`OpenGU e27425e6 / Core 0.3.2`。证明旧版无需 Agent 补 collect；不覆盖 0.4.0 的新 GPU 运行。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/auto-return/verification.json)

### 0.4.0 执行交接

Core 91 项、OpenGU 221 项检查；两个真实本地 Git 检出、独立 worker、自动回传及改设备后的手动补收通过。

版本：`OpenGU e8f23a94 / Core 5dd378cb`。保留当时的 Core 交接证据；本轮变更部分另以 311 项检查核验，未新增 GPU 实测。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/output-handoff/verification.json)

## 本轮修复与验证

### 预检与配置摘要

此前配置路径误传为 ratio，gate_only 丢失；配置摘要也停留在 028 增加 Retrain 之前。现按登记配方准确传递参数并固定当前配置摘要，20 项真实预检签名检查通过。

**核验边界**：正式设备、Selection 前置与矩阵授权继续由原 preflight 检查；测试没有绕过正式运行门槛。 [源码位置](../../../scripts/syncmate/opengu_adapter.py)

### 独立方法产物声明

此前只声明 GNNDelete 与旧 collateral 文件。现在直接复用执行器 gu_artifacts：gate 8 文件、17-selector stage 136 文件，完整包含 GNNDelete 与 Retrain。20 个配方全部一致。

**核验边界**：方法参数同时与实际矩阵消费者对照，避免配方和运行入口各自维护不同条件。 [源码位置](../../../scripts/syncmate/opengu_recipes.py)

### 收集后的内容与身份核验

现从已收集的 predictions.npz 解析完整模型/预测，核对 SHA、Recipe/Artifact/内容身份、三处 Output 引用、Selection、checkpoint、方法条件和共享输入，再重算单方法指标。

**核验边界**：真实 CPU 结果通过；缺少 Retrain、重复/未验证索引、Git 不符、字节损坏、引用/指标/checkpoint/Selection 不符、预测缺失/无效、方法参数不符均拒绝。 [源码位置](../../../scripts/syncmate/opengu_method_output.py)

### 结果表与相邻入口

results 按独立输出格式读取两种方法，保留完整策略名称，跨方法比较仍是后处理。基础 smoke Adapter 按需加载实验模块，相邻 M1 独立入口也通过回归。

**核验边界**：没有新建兼容分支或复制 Core；旧测试中的假 collateral、无效 npz 通过案例已被真实生产与收集测试替代。 [源码位置](../../../scripts/syncmate/opengu_results.py)

## 本轮核验与解释

- 代码检查使用本地项目 Python 与 Core 0.4.0。完整测试包括 SyncMate、完整与基础 Adapter、Core 依赖、原子入口、target-direct stage、独立 Retrain/输出及新增 GU 收集测试；311 passed、0 failure/error/skip。
- 两个正向收集场景分别覆盖 gate 与 stage 接受路径。执行和收集使用临时目录与真实本地 Git runner；测试图只有 20 个节点、10 个候选、k=1，正式配方与数据未被改写。正式 20 个配方另做完整静态合同与预检参数检查。
- 收集与接受期间禁止模型 forward 和训练更新；远端 Cache V2 没有复制到 collector，源 Store 的前后文件哈希不变。这里证明的是代码消费闭环，不把 CPU 场景写成新的 GPU 实验。
- 最终产品检查点为 f7956bb994b20b629b60e8f1a4da20fc78ea6b88。后续提交只更新本 item 的证据/报告/状态和看板；实现、依赖、配置与测试无差异时复用该检查结果。CLI 编译与独立 smoke 亦通过。
- 最初失败证据 observations.json、13 项旧检查及历史实测保留；新核验写入 repair-observations.json 和 repair-tests.xml，未把过去失败改写成过去通过。
- F1 冷热差异来自保存基础指标时舍入后又重算差值；028 已改为保存完整浮点精度，相关回归继续通过。
- 此前已读回本地与 SSH Core 0.4.0 的 60 文件依赖一致；SSH OpenGU 仍是已落地主线 c9e094c5。本次修复是独立分支上的待验收代码，不能说远端已安装此修复。

## 下一步

由用户验收当前代码与 CPU 接入验证结果；接受后沿用同一 AAGU-005 完成合入和已登记的同步动作。新的正式 GPU 运行仍按项目门槛及其独立授权执行。

## 证据入口

- [当前 WorkItem](WORKITEM.md)
- [修复后的合同与预检观察](evidence/repair-observations.json)
- [311 项原始测试结果](evidence/repair-tests.xml)
- [真实收集、接受与结果表证据](evidence/repair-verification.json)
- [修复核验说明](evidence/repair-verification.md)
- [最初缺口观察（历史）](evidence/observations.json)
- [只读跨接口核对脚本](evidence/audit.py)
- [028 已接受的独立方法与 Metrics 说明](../AAGU-028/REPORT.md)
- [SM-005 原始报告](E:/project/SyncMate/.workblock/items/SM-005/REPORT.md)
