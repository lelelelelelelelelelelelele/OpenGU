# AAGU-002 · 设备可用，任务下发门禁仍需修复

## Human Result

### 实际增量

已完成固定 SSH 目标的真实设备探测、现有实验预检与缺 GPU 注入检查，并在临时 Git 仓库中用当前已安装的 SyncMate Core 复现拒绝下发路径。远端新增任务为 0，队列前后哈希一致。

### 核心观察

gpu4090 身份、活跃检出、RTX 4090 和 Core 依赖核验通过。但预检明确拒绝时，任务仍能入队；预检遗漏 ready 字段时，绑定检查也会通过。设备可用这项成立，002 整体门禁未通过。

### 当前决定

Agent 建议返工：由同一 SM-001 补齐通用门禁，再回到 002 复验。当前不进入 awaiting_acceptance，不放行后续实验。需要先确认 SM-001 同号旧记录的协议修正；报告中的“待决定”不代表验收条件已满足。

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
| 生产 READY 回执与门禁贯通 | NOT OBSERVED | 本轮形成的是人工规范化的设备观察，不是生产入口已强制消费的就绪回执。SM-001 尚未实现并接受该闭环。 |

## 剩余修复

1. 保留 SM-001 的 ID、范围、formal 路线、非目标和历史，把缺失版本的 1.0 记录修正为 2.1 Human Surface，并把 AGUR-002 关系更正为现有 AAGU-002。当前只提供修正建议，原记录未修改。
2. 在 SyncMate Core 的下发与 runner 入队边界消费完整的就绪检查，必须显式 ready=true 且无错误；拒绝、缺字段、异常、身份或绑定不符都应在写入 inbox 前失败。保留执行前复检。
3. 复用现有 Device Contract 的 resolver、固定只读 probes 和反馈码；精确 GPU、路径及能力要求继续由 OpenGU/设备配置拥有。回执绑定已核验目标与当前 recipe、完整 Git SHA、配置指纹，不能把历史 READY 当成新任务通行证。
4. 用隔离仓库验证拒绝时没有新任务、允许时仅有审阅任务，再补真实目标上的贯通证据。SM-001 独立验收后，002 才作研究侧 gate 决定。正式矩阵仍由后续实验授权。

## 证据与边界

设备实测时间为 2026-09-05T20:54:43.715291+00:00；SSH 检出为 b4da08647756810d24a7e51a23422bee7fbea3db。本地 main 因本轮 002 登记提交向前推进，当前不满足正式实验的三方 SHA 对齐条件。本轮未推送、安装、开通设备、运行正式实验，也未运行 029 的未来部分节点接口。

干净检查点 e3ce4a1cd1e2cd03107b3b63b92a6fdaa167b2fc 上的证据复核完成；11 项核验说明证据完整、缺口可复现，不等于产品 gate 通过。最终候选只增加报告、Record 及修正建议；实际门禁结论仍为 FAIL。

- [规范化核验与整体 REFUSED 结论](evidence/verification.json)
- [真实远端观察和两种 adapter 预检](evidence/remote-probe.stdout.json)
- [隔离队列复现](evidence/queue-guard-repro.json)
- [可重跑的远端只读探针](evidence/remote_probe.py)
- [可重跑的本地 Core 复现](evidence/queue_guard_repro.py)
- [SM-001 同号记录修正建议（未应用）](evidence/SM001-record-proposal.md)
- [同一 WorkItem](WORKITEM.md)
