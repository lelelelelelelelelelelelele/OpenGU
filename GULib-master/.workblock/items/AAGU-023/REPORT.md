# AAGU-023 · Legacy evidence inventory and archive

## Human Result

### 实际增量

本候选把散落在 `results/` 的旧证据按真实身份拆成 20 个批次，并新增一个只读、write-once 的 inventory / retirement-ledger 生成器。它逐文件记录路径、大小、mtime、SHA-256 与 tracked/ignored 状态，分别登记本机和 SSH 位置，保护 `results/cache_v2`，并把 AAGU-023 的 Repair 生命周期及其对 AAGU-003 的依赖投影回生成器拥有的 dashboard。

这次没有把“归档”误写成“删除”或“整目录搬走”：三个既有 archive 的隔离状态得到复核；其余批次因尚未达到 `REPLACED`、仍有消费者或属于保留的工程证据而保持原位。新增物理移动为 0，删除为 0，Cache V2 写入为 0。

### 核心观察

- **PASS · 本地 data**：20 个登记批次覆盖 7,044 个 evidence 文件；仅排除两个当前治理文件 `results/AGENTS.md` 与 `results/README.md`。三棵 Legacy 根保持为独立批次：ResultCache 8 个文件、SelectionCache 9 个、ScoreCache 26 个。
- **PASS · 本地 lifecycle**：前后两次 manifest 对比没有 batch 或 protected-path 变化；`moves_observed=0`、`deletions_observed=0`，Cache V2 锚保持 32 个文件 / 983,515 bytes。
- **PASS · integration**：clean implementation checkpoint `67be158e77460a26ca3aaa201f0eeb3fc1815a05` 基于 baseline `3ec3d56476f008f7bfc94b4e62a70efd239be6e2`，相关回归通过 21/21，dashboard projection check 通过，候选 tracked diff 不含任何 `results/` payload。
- **NOT OBSERVED · SSH**：`autodl-opengu`、`opengu-4090` 与 `4090` 均在执行任何远端命令前拒绝 banner exchange；因此 5 个双端批次的实时哈希、远端消费者与 local/SSH ledger parity 没有被观察，共同 ledger 正确保持 `device_parity_confirmed=false`。
- **NOT CONFIRMED · 新物理归档**：当前没有批次达到 `REPLACED` 且旧引用为零；源码扫描仍有 74 条 Legacy API/path 引用，所以本候选没有资格移动三棵活动 Cache 或混合的 `results/runs`。

### 当前决定

> 当前验收决定：`待决定`

Agent 建议：**证据不足**。本地 inventory、零删除、既有 archive 隔离和 Cache V2 保护已经形成可接受的精确候选，但 Human Surface 要求的本机/SSH ledger 一致性尚未得到实时证据支持。决定者为用户；建议在 AutoDL endpoint 可达后复核同一 Block 的远端 manifest 与 parity，再决定接受或返工，不应把本地 scoped PASS 升级成整体 PASS。

## Data · 前后状态

| 判断面 | 目标状态 | 当前实测 | 结论 |
|---|---|---|---|
| 批次边界 | 不按目录/mtime混批，逐批有身份与失效/替代依据 | 20 个批次；`runs` 拆为 4090、ablating、2026-07 engineering、H20、arXiv 五个子批 | `PASS` |
| Legacy Cache | 三根分开登记，新批次禁止复用 | 8 / 9 / 26 文件；74 条消费者引用仍存在 | `PASS`（登记）；`NOT CONFIRMED`（可移动） |
| 既有 archive | 原位隔离、可追溯、内容不变 | 2026-05-06 / 2026-05-07 / 2026-07-21 为 2,675 / 28 / 126 文件，前后哈希不变 | `PASS` |
| Cache V2 | 不进入 retirement batch，不写、不移、不修复 | protected anchor 32 文件 / 983,515 bytes；前后无变化 | `PASS` |
| 双端一致 | 本机与 SSH 同一批次 ledger 可对照 | 本机已观察；SSH endpoint 不可达 | `NOT OBSERVED` |

关键机器证据：

- [批次计划](evidence/batch-plan.json)
- [本地前置 manifest](evidence/local-inventory-before.json)
- [本地后置 manifest](evidence/local-inventory-after.json)
- [前后比较](evidence/local-inventory-comparison.json)
- [共同 retirement ledger](evidence/retirement-ledger.json)

这些文件能证明本地批次、内容锚和零动作；它们不能证明 2026-09-02 的 SSH 实时内容或双端 parity。

## Lifecycle · 实际过程

1. 同一 AAGU-023 在 `main@3ec3d564…` 上由 `run_git.py start` Claim，建立 source branch 和 canonical Claim；没有创建 sibling Record。
2. 读取本地 7,046 个 `results/` 非 Cache-V2 文件，将 7,044 个 evidence 文件归入 19 个本地批次，两个治理文件显式留在 retirement scope 外。
3. 在任何移动前生成 write-once manifest；三次 SSH 连接均在远端命令前失败，因此没有远端 Git、文件或进程动作。
4. 第二次读取同一批次并对比：batch changes 0、protected changes 0、moves 0、deletions 0。
5. 共同 ledger 登记 20 个逻辑批次；5 个带 SSH location 的批次标为 `NOT_OBSERVED`，没有从旧文档补写成当前观察。
6. 形成并验证 implementation checkpoint；生成 formal Report 后，决定候选将以同一 source branch 的 clean report-bearing `HEAD` 为准。

这个过程证明 archive gate 在数据不足时保持关闭；脚本存在和测试通过本身并不替代远端真实观察。

## Integration · 候选整体行为

在当前候选中，生成器、批次计划、两次本地 manifest、comparison、共同 ledger、WorkItem 与 dashboard projection 作为一个整体工作：plan 禁止 Cache V2 进入 retirement batch；inventory 只读结果树；comparison 证明零变化；ledger 在 SSH 缺失时 fail closed；dashboard 不再把已 Claim 的 AAGU-023 显示成待 Promote Todo。

预期是错误或不完整身份不能产生“已配对、可归档”的结论。实际观察到 SSH 不可达时 ledger 保持 `device_parity_confirmed=false`，没有 archive-eligible batch，所有 action list 为空；因此本地集成判断得到支持，但跨设备核心验收仍不能成立。

## 已知缺口与边界

- 尚未观察：SSH 当前 `results/` 内容、三棵 Legacy 根的逐文件哈希、远端 Cache V2 保护锚、远端 consumer scan 与 5 个双端批次 parity。
- 本次不判断：任何正式 GPU 实验、科学性能结论、旧 payload 删除、Cache V2 Artifact 修复或重写。
- 若接受当前本地增量，仍需承担：远端恢复后可能发现 batch drift、额外未登记 payload 或消费者差异；这些事实必须回到同一 AAGU-023 返工，不能通过 Closeout 猜测补齐。
- 不要重复：在 AutoDL 不可达时用 2026-07/08 文档快照冒充当前 SSH inventory，或把 `results/runs` 当成一个批次整体移动。

## 技术附录

- Baseline：`3ec3d56476f008f7bfc94b4e62a70efd239be6e2`
- Source branch：`refs/heads/codex/aagu-023-legacy-evidence-archive`
- 已验证 implementation checkpoint：`67be158e77460a26ca3aaa201f0eeb3fc1815a05`
- 当前决定对象：完成 Report/status 投影后同一 source branch 的 clean report-bearing `HEAD`；最终 OID 由本轮候选形成回执与 Claim read-back 给出。
- 验证：`pytest` 相关集合 `21 passed`；changed Python compile、dashboard `--check`、evidence invariant assertions、candidate ancestry、clean status、tracked result diff 与 `git diff --check` 均通过。
- 证据 SHA-256：plan `d0bd91b8…`；before `618e274b…`；after `3d7b5e8a…`；comparison `3a88d561…`；ledger `d5eca3d0…`。
- 证据层：data / lifecycle / integration。本地内容是 fresh 读取；SSH 是真实连接失败记录，不是远端内容快照。
- HTML 渲染检查：`NOT OBSERVED`。结构 validator 已通过；in-app browser 无法从隔离环境连接本机 loopback，且安全策略禁止本地 `file:` URL，因此没有声称桌面/窄屏视觉 PASS，也没有绕过浏览器策略。
