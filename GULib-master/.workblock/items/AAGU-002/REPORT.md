# AAGU-002 · OpenGU 设备核查完成，完整 Gate 尚未交付

## Human Result

### 实际增量

已完成固定 SSH 目标的真实设备探测、现有实验预检与缺 GPU 注入检查，并在临时 Git 仓库中用当前已安装的 SyncMate Core 复现拒绝下发路径。远端新增任务为 0，队列前后哈希一致。

### 核心观察

gpu4090 身份、活跃检出、RTX 4090 和 Core 依赖核验通过。ready 是实际条件检查的输出，不是用户配置项。隔离测试中明确未就绪的任务虽已入队，执行前被挡住，进程调用为 0；空对象是工具层故障样例，不能说成真实 OpenGU 预检返回了空结果。

### 当前决定

Agent 判断完整 Gate 证据仍不足：本轮完成探测与拒绝测试，没有新跑最小 OpenGU 任务。继续只处理 OpenGU 002，撤回接手及升级 SM-001 的前置要求。当前保持 ongoing，不将设备核查或工具层异常样例等同于完整 Gate 的通过或失败。

> 当前验收决定：`待决定`

## 场景与观察

| 场景 | 判断 | 实际观察 |
|---|---|---|
| 别名、连接和身份 | PASS | OpenSSH 解析到单一端点；有界 SSH 成功，远端 device_id=gpu4090、role=runner。端点仅保存摘要，不复制连接配置。 |
| GPU 与路径 | PASS | 当前 1 张 NVIDIA GeForce RTX 4090，CUDA 可用；固定活跃检出路径正确，main 干净。GPU 空闲容量未测量。 |
| 两端 Core | PASS | 本机与 SSH 均为已接受的 1e30a329 对应 0.4.0 payload，60 个文件哈希核验通过。 |
| 真实实验预检 | PASS | 读取既有 Cora 输入：2708 节点、1895 候选。发现该 recipe 的输出已经存在而明确拒绝重跑，没有改写旧结果。 |
| 缺 GPU 情况 | PASS | 在真实 SSH 探测进程内临时注入 cuda.is_available=False，现有 adapter 明确拒绝并说明不降级到 CPU。实际设备仍有 GPU；这条是受控故障注入。 |
| 拒绝后是否入队 | FAIL | 临时仓库中的 preflight 返回 ready=false，当前 Core 仍 submitted=true 并写出 inbox；入队前 preflight 调用次数为 0。执行前第二道检查最终 blocked，进程调用次数为 0。 |
| 不完整预检 | FAIL | 同一 Core 的 recipe binding 收到空对象 {} 后返回 ready=true。未执行这个缺字段样例的进程。 |
| 完整 OpenGU Gate | NOT OBSERVED | 本轮形成的是设备观察及现有预检结果，尚未完成当前 OpenGU 最小任务与门禁路径的完整交付。SM-001 不属于本轮接手范围。 |

## 剩余修复

1. 沿用当前 OpenGU 实验已有的 GPU、路径、依赖、数据与配置要求，核查实际入口是否执行这些检查以及失败时是否阻止实验开始；不新增需要用户填写的 ready 参数。
2. 把排队、开始执行、完成最小任务和结果核验分别记录。对前序 1×1 证据先核对适用身份，补足真正缺失的 OpenGU Gate 证据；本轮不接手 SM-001，不把旧任务记录版本问题作为前置条件。

## 证据与边界

设备实测时间为 2026-09-05T20:54:43.715291+00:00；SSH 检出为 b4da08647756810d24a7e51a23422bee7fbea3db。本地 main 因本轮 002 登记提交向前推进，当前不满足正式实验的三方 SHA 对齐条件。本轮未推送、安装、开通设备、运行正式实验，也未运行 029 的未来部分节点接口。

干净检查点 e3ce4a1cd1e2cd03107b3b63b92a6fdaa167b2fc 上的证据复核完成；11 项核验说明证据完整、工具层缺口可复现。当前按用户纠正重新区分事实与结论：两项隔离测试的 FAIL 保留，不能自动升级为 OpenGU 实验失败；完整 Gate 尚未交付。真实探测与复现数据未更改。

- [规范化核验与证据范围](evidence/verification.json)
- [真实远端观察和两种 adapter 预检](evidence/remote-probe.stdout.json)
- [隔离队列复现](evidence/queue-guard-repro.json)
- [可重跑的远端只读探针](evidence/remote_probe.py)
- [可重跑的本地 Core 复现](evidence/queue_guard_repro.py)
- [同一 WorkItem](WORKITEM.md)
