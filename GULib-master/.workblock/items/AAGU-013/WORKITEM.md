# AAGU-013 · EXP · Surrogate Transfer

Block ID: `AAGU-013`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

在明确的威胁模型与选择器合同下，判断代理模型（surrogate）上形成的攻击选择能否迁移到目标模型，同时始终分开选择器身份、目标身份与直接攻击参照。

### 本次增量

按批准的分组实验配方独立执行 surrogate-transfer 分组，保存 gate 产物，并在需要时配对 Target-Direct 参考。本 Block 不重新定义影响函数（IF）、不预设迁移阈值，登记本身也不授权 GPU 执行。

### 核心验收

- 每个迁移分组都绑定批准的实验配方与可追溯证据，选择器身份和目标身份没有混写。
- 需要直接攻击参照的组提供同条件 Target-Direct 对照，报告不以预设阈值替代实际观察。
- 用户能依据 gate 产物和威胁模型边界，逐组接受、返工或拒绝 surrogate-transfer 结论。

## Orchestration contract

- Class: `EXP`
- Priority: `P2` on the single experiment timeline.
- Source anchor: legacy surrogate-transfer Todo.
- Outcome: execute independently gated surrogate-transfer groups under an approved threat-model and selector contract.
- Fact owner: OpenGU DocMap surrogate-transfer experiment plan.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `research evidence`.
- Minimum evidence: approved group recipe, selector/target identity separation, gate artifacts, paired target-direct reference where required, and explicit decision.
- Confirmation: deferred until claim/real execution.
- Report size: decide at claim.

## Boundaries

- No new IF definition, no assumed transfer threshold, and no GPU execution by registration.

## Status history

- 2026-08-26: registered from the prominent surrogate-transfer experiment Todo.
