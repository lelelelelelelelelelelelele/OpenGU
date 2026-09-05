# AAGU-005 · OpenGU 接入交接与当前缺口

## Human Result

### 实际增量

把 SM-005 此前直接提交到 OpenGU 的消费端改动、真实运行与代码检查证据归入同一 AAGU-005。已核对主线承接、SSH 同步和双端 Core 依赖。本轮新增交接报告与只读核对脚本，没有修改实验或接入实现。

### 核心观察

6 个 SM-005 原子配方的配置与输出合同一致，13 项针对性检查通过；本地与 SSH 均通过 Core 0.4.0 的 60 文件检查。同时发现 20 个 target-direct 正式 GU 配方与当前执行器的产物声明不一致，预检调用还把配置路径误传给删除比例。已有原子链路可用，但全部正式 GU 接入尚未对齐。

### 当前决定

建议先补齐下方正式 GU 接口缺口，再接受 AAGU-005 的完整接入范围。SM-005 已接受的 Core 与原子实验成果继续有效。本报告由用户决定；当前保留待决定，不把已落地代码或局部测试通过写成 AAGU-005 整体接受。

> 当前验收决定：`待决定`

## 此前已经交付的 OpenGU 改动

| 内容 | 已实现行为 | 主要位置 |
|---|---|---|
| 原子实验入口与配方 | Degree、B-Hutch first/warm、D-full Selector-only、自动回传及新版 handoff 共 6 个固定配方，绑定配置摘要、运行身份与输出。 | experiments/syncmate_atomic_stage.py；scripts/syncmate/opengu_recipes.py |
| 启动参数隔离 | 隔离 --recipe，避免被 OpenGU import-time 参数解析误读。失败与拒绝不会进入训练。 | experiments/syncmate_atomic_stage.py |
| 输出交接 | 配方与执行器共用 modular_output_path；执行前核对 queue receipt 的 output_contract。 | scripts/syncmate/opengu_layout.py；experiments/modular_execution.py |
| Core 安装身份 | 消费端核对 0.4.0 的完整文件集合与内容哈希；设备配置保留接入事实，项目代码拥有结果规则。 | scripts/syncmate/core_dependency.json；verify_core_dependency.py；opengu_adapter.py |

最后一轮输出交接覆盖 13 个文件；这里承接既有 Git 交付，不创建重复实现。

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

版本：`OpenGU e8f23a94 / Core 5dd378cb`。本轮复用相同产品文件的证据；新协议未新增 GPU 实测。 [原始证据](E:/project/SyncMate/.workblock/items/SM-005/evidence/output-handoff/verification.json)

## 当前发现的正式 GU 接口缺口

### 预检参数传错

OpenGU Adapter 调用 preflight_gu(stage, config_path)，但消费者签名为 preflight_gu(stage, ratio, config_path, gate_only=...)。只读复现得到 TypeError：float() 不能接收 WindowsPath，且尚未进入设备或数据预检。

**需修复**：正确传递登记的 ratio、配置路径和 gate_only；用真实消费者签名核验。 [源码位置](../../../scripts/syncmate/opengu_adapter.py)

### 配方与执行器产物不一致

队列配方仍要求 GNNDelete 的 attack.json、collateral.json、predictions.npz、_meta.json；028 后执行器输出 output-references.json，并同时枚举独立 GNNDelete / Retrain。2 个 gate 配方各声明 4 个文件、执行器枚举 8 个；18 个整组配方各声明 68 个、执行器枚举 136 个。20/20 集合不相等。

**需修复**：让配方、执行器与收集声明消费同一已确认单方法产物合同；不能只改文件名而遗漏 Retrain。 [源码位置](../../../scripts/syncmate/opengu_recipes.py)

### 消费端接受检查仍依赖旧 collateral

OpenGU 的 GU gate / stage 接受检查仍读取 collateral.json 和旧比较结果；这与独立方法输出、收集后计算差值的当前合同不一致。该项依据源码定位，尚未运行端到端正式 GU 作业。

**需修复**：按独立方法输出及其内容/依赖身份完成消费检查；跨方法比较保持后处理。 [源码位置](../../../scripts/syncmate/opengu_acceptance.py)

## 本轮核验与解释

- 本轮检查调用真实配方与真实执行器的产物枚举函数，比较各自输出集合；它不提交任务、不读取正式数据、不运行 GPU 或训练。13 项既有针对性检查覆盖原子入口、拒绝路径和指标无损读回。
- 这些缺口属于 OpenGU 消费端。现有测试各自使用自己的配方/执行器夹具，局部通过不能证明两侧合同一致；本次跨接口比较补出了这层证据。
- F1 读回差异的根因是保存时先舍入基础指标、读回后重新计算差值。028 已改为保存原始浮点精度，本轮无损往返检查通过；历史四舍五入后的结果文件没有被改写或自动修复。
- OpenGU 当前产品基线与 SSH 均为 c9e094c55b42b2833fb24fcef5fe08f057605f68，包含 e8f23a94 的消费端交付。上述接入文件相对交接提交未改，后续底层独立方法变更的复用边界由 028 检查与本次跨接口核对共同说明。
- SM-005 已在 6a938e2a 接受、合并、推送；双端 0.4.0 安装已验证。其安装回执保留 partial，仅因本地临时 payload 删除被自动审批拒绝。AAGU-005 不处理该清理、不重放安装。
- 重建 wheel 的容器 SHA-256 为 ab22f394…，原消费端清单记录 a6ecf6de…；两端实际 60 个载荷文件均与原精确清单匹配。当前依赖验证按内容身份通过，不把两个 wheel 容器哈希说成相同。

## 下一步

沿用 AAGU-005，先修复正式 GU 的预检、产物声明和接受检查，增加配方→执行器→收集的真实消费验证；不重新实现已交付原子链路。核验通过后更新本报告，再交用户决定完整接入范围是否接受。

## 证据入口

- [当前 WorkItem](WORKITEM.md)
- [本轮完整观察与原证据哈希](evidence/observations.json)
- [只读跨接口复现脚本](evidence/audit.py)
- [13 项检查的原始结果](evidence/targeted-checks.xml)
- [SSH 代码与 Core 依赖读回](evidence/remote-readback.json)
- [028 已接受的独立方法与 Metrics 说明](../AAGU-028/REPORT.md)
- [SM-005 原始报告](E:/project/SyncMate/.workblock/items/SM-005/REPORT.md)
