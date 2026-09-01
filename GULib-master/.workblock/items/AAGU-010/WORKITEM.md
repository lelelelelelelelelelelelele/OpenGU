# AAGU-010 · FIX · Hop Aggregate Fields

Block ID: `AAGU-010`

Item Version: 2.1

当前状态: `registered / not claimed`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Execution topology: `sequential`

Item Type: Block

## Human Surface

### 核心意图

让 hop-decay 汇总输出从已接受的 collateral evidence 中真实暴露所需 hop 字段，使后续读者和工具可以直接使用这些值，同时对证据里不存在的字段保持明确失败，而不是补造数据。

### 本次增量

在 AAGU-009 的 collateral evidence 前置满足后，按执行时选定的汇总结构修复汇总路径，让测试样例与真实回读都能产生必需的 hop 字段，并保留字段缺失时明确拒绝或标记未知的 fail-closed 行为。本 Block 不生成新的科研结论，也不运行 GPU 实验。

### 核心验收

- 测试样例支撑的汇总输出包含结构要求的 hop 字段，并能回读到已接受的 collateral evidence。
- 证据缺少所需字段时，汇总明确失败或标记未知，不伪造默认值或推断值。
- 人能够通过短验证说明确认数据集成行为正确，成功测试本身不自动构成接受。

## Orchestration contract

- Class: `FIX`
- Priority: `P1` after accepted collateral evidence.
- Source anchor: legacy hop-decay aggregate-field Todo.
- Outcome: aggregate output exposes the required hop fields from accepted evidence without fabricating missing values.
- Fact owner: OpenGU DocMap rerun/cache-fix runbook and the aggregate schema selected during execution.

## Acceptance route proposal

- Route: `practical`.
- Primary surface: `data integration`.
- Minimum evidence: fixture-backed aggregate output, missing-field fail-closed behavior, and read-back against accepted collateral evidence.
- Confirmation: deferred until claim/real execution.
- Report size: short verification note unless claim review changes it.

## Boundaries

- No new scientific conclusion and no GPU run.

## Status history

- 2026-08-26: registered from the prominent aggregate repair Todo.
- 2026-08-31: upgraded the same stable WorkItem to protocol 2.0 with the current sequential topology and Apply target; no dependency, Claim, or acceptance fact changed.
