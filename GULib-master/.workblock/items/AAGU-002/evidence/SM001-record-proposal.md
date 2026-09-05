# SM-001 同号记录修正建议（未应用）

> 已撤回：用户明确本轮仅处理 OpenGU 002，不接手 SM-001。以下内容保留为上一轮建议的历史，不作为 002 的执行前置条件。

原记录：`E:/project/SyncMate/.workblock/items/SM-001/WORKITEM.md`。
只读检查返回 `workitem-version-upgrade-required`：缺失 Item Version，按实际版本 1.0 处理；当前支持 2.1。尚未修改 SM-001、创建 Claim 或改动 SyncMate 产品源码。

建议保留同一 ID、原验收含义及历史，补充如下字段与 Human Surface；原 Context、Confirmed acceptance contract、非目标继续保留。旧 `AGUR-002` 引用同步更正为已存在的 `AAGU-002`，不新建 Block。

```text
Item Version: 2.1
Item Type: Block
当前状态: registered / not claimed
Stable locator: .workblock/items/SM-001/WORKITEM.md
Acceptance Route: formal
Execution topology: parallel
Apply target ref: 从 SyncMate canonical checkout 重新读取准确 symbolic ref 后登记
```

## Human Surface（替换旧的 Block human acceptance surface）

### 核心意图

在 SyncMate 中实现可审计的设备就绪门禁，使上层实验只向身份、路径、GPU 和能力满足约定的设备下发已审阅任务；明确拒绝或证据不完整时不得入队。

### 本次增量

沿用现有 Device Contract，将别名解析、有界 SSH 连通、只读身份/GPU/路径/能力探测、READY/REFUSED 回执和下发门禁贯通。复用现有实现，补齐 AAGU-002 实测定位的“拒绝仍入队”和“缺失 ready 仍通过”问题；保留执行前复检。项目要求由 adapter/设备配置拥有，Core 不加入 OpenGU 科研语义。

### 核心验收

- 别名与预期逻辑设备唯一绑定；错误身份、路径、GPU 或缺少能力均有可定位的拒绝原因。
- 就绪回执包含真实 resolver、SSH、probe 证据；下发与入队必须消费完整且匹配本次目标及任务绑定的 READY，不接受 REFUSED、不完整或失效回执。
- 拒绝时没有新 inbox/执行进程；真实目标上的允许/拒绝链路有可复核证据。SyncMate owner 与 AAGU gate owner 决定接受、返工或拒绝。

## 执行边界建议

记录修正经用户同意后，使用独立工作区接手同一 SM-001，实施通用门禁、隔离 CPU 测试、现有固定 SSH 目标的有界只读探测，并形成 formal 配对报告。真实任务提交仅在该 Block 明确批准的最小验证范围内进行，不扩展正式科研矩阵。

不增加付费设备操作、自动 bootstrap、自动重试、缓存清理或 FlowChunk 功能。候选完成不等于接受；发布/安装继续走该项目已有 Closeout。SM-001 独立接受后，AAGU-002 复验并作研究侧放行决定。

## 同号历史追加建议

- 2026-09-06：AAGU-002 实测完成设备观察并复现两处门禁缺口。准备同号协议修正，保留原范围与历史；用户批准修正后再登记实际写入事件和执行授权。
