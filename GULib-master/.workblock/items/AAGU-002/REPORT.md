# AAGU-002 · OpenGU Smoke Test 与 Timeout 验收

## Human Result

### 实际增量

已完成设备与字段核查、20 节点小图的真实 CPU 组件 Smoke、传输与证据链 Smoke，以及实际子进程的 Timeout 验证。所有运行均为有界软件测试，没有启动 007 正式实验。

### 核心观察

组件与实验入口检查 15/15 通过；传输 Smoke 12/12 通过；38 个 recipe 的超时合同字段一致。1 秒预算的小任务实际触发超时，整次处理耗时 1.183 秒，保存 failed 回执、子进程已退出、没有最终成功产物；随后正常任务完成，最终队列 idle。

### 当前决定

Agent 建议接受本轮 Smoke 与 Timeout 准备验证。按用户最后澄清，先提供本报告供审阅，当前不写 accepted、不合并或安装。最小正式科研实验和研究结果由 007 单独运行与验收；本次通过不表示完整组件计时或大图成本预测已实现。

> 当前验收决定：`接受`

## 各部件验证

| 部件 | 证据 | 结果 |
|---|---|---|
| 设备与环境 | 真实 SSH 观察 | 固定 gpu4090 身份、唯一活跃检出、RTX 4090 和两端 60 个 Core 文件核验通过；现有 adapter 对缺 GPU 注入和已有输出明确拒绝。 |
| 实验字段 | 38/38 recipe | timeout_seconds、recipe ID、完整 Git SHA 和配置 SHA 在实际 Core 执行合同中吻合，预算沿用配方。ready 是检查输出，不是新增的用户参数。 |
| Selector / Score / Selection | 20 节点 CPU 实跑 | 实际调用现有消费者；冷运行计算，热运行复用；Hutch 参数改变只使对应身份失效。额外单 Selector → 单 GNNDelete 验证构成最小组件链。 |
| GU 与 Metrics | 真实 CPU 消费者 | GNNDelete 使用已有 Selection；禁止 Selector producer 后仍能冷运行/热复用。离线指标独立读取，缺失 Retrain 证据明确拒绝。 |
| 实验入口 | 共 15 项检查通过 | 包括上述三个组件场景，以及原子配方、输出合同、缺 GPU、旧输出和非法 recipe 等入口检查。小图训练 3 epochs，GU 2 epochs。 |
| 传输和证据链 | 12/12 Smoke 检查 | 3 个示例 Artifact 完成传输、SHA 校验、可信索引和导出；独立临时目录已清理。 |
| 已有耗时证据 | 5 份 summary 哈希吻合 | 可读取 Score 基准、本次访问、Selection 时间和 GU 历史时间。HIT 不改写首次基准；未知访问耗时没有填成 0。 |

## Timeout 实测

| 场景 | 配置上限 | 整次处理耗时 | 作业状态 | 观察 |
|---|---|---|---|---|
| 正常对照 | 5 秒 | 0.202 秒 | done | 正常完成并保存产物 |
| 实际超时 | 1 秒 | 1.183 秒 | failed | 预期失败；进程退出、无成功产物 |
| 超时后的正常任务 | 5 秒 | 0.202 秒 | done | 正常完成并保存产物 |

三组验证均 PASS：中间任务的 failed 正是预期结果。三次处理后没有 running 作业，额外 run_once 返回 idle，没有自动重试失败任务。

## 结论边界

- Timeout 测试在本地临时干净 Git 仓库中使用已安装 Core 的真实队列和 subprocess.run，受控任务本应等待 4 秒，预算为 1 秒。没有 mock 超时异常，也没有改写任何正式 recipe。
- 表中的处理耗时包含预检、启动和回执开销，不能把约 1.18 秒解释为精确 CPU 计算时间。只确认直接子进程终止，未测试任意后代进程树。
- 组件 Smoke 使用 CPU；导入时出现本机 RTX 5070 与现有 PyTorch CUDA build 不兼容警告，不代表这些 CPU 测试使用了本机 GPU。正式 GPU 环境仍是既有 SSH 4090。
- 作业级 timeout 已接通；完整模型准备、GU 访问计时、逐组件首次测量以及大图外推仍有缺口。这些不能写成“所有计时能力已经完成”，也不阻塞当前有限 Smoke 验收。
- 工具层仍保留预检拒绝后可入队、空预检对象可能被误判的隔离发现；明确拒绝的测试在执行前被挡住。它们不是实际 OpenGU 已在缺 GPU 时运行的证据，本轮不接手 SM-001。
- 设备证据有时间和版本边界；007 正式运行前仍须重新核对当时的设备、三方代码身份、数据、配方及已有产物。002 不替代其科研接受。

## 证据与复核

- [正常→超时→继续正常：完整回执](evidence/timeout-smoke.json)
- [Timeout 可重跑脚本](evidence/timeout_smoke.py)
- [15 项测试及 CPU 运行原始证据](evidence/component-smoke.xml)
- [组件运行摘要](evidence/component-observations.json)
- [38 个合同、传输 Smoke 与耗时证据](evidence/scope-smoke.json)
- [真实 SSH 设备观察](evidence/remote-probe.stdout.json)
- [同一 WorkItem](WORKITEM.md)

此前范围讨论曾把 007 的正式最小实验重复加入 002，后又提出直接接受；用户最后明确先交付 Smoke、Timeout 和验收报告。当前以这一要求为准，历史原始观测保留，不沿用先前的自动 Closeout 建议。
