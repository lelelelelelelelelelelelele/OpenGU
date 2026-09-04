# AAGU-009 · FIX · IF-family 参数写回与 Collateral 评估代码修复

Block ID: `AAGU-009`

Item Version: 2.1

当前状态: `working / claimed`

> Apply target ref：`refs/heads/main`

Execution topology: `sequential`

Item Type: Block

## Human Surface

### 核心意图

确保 GIF/IDEA 的遗忘更新实际写回评估使用的模型，使 collateral 评估比较的是遗忘后模型与完整重训练模型。009 只交付代码修复和本地软件验证；修复代码不等于历史实验结果已恢复可信。

### 本次增量

复核并整合已有 IF-family 参数写回修复及实际加载代码检查，移除会原地删除、覆盖旧结果的活动修复 helper，补齐必要的本地回归。已有修复正确时保留并验证，不为制造增量重复改写算法。SSH 配置、部署、正式 GPU 重跑、历史产物隔离、结果收集和研究证据验收统一转交 AAGU-027。

### 核心验收

- 本地隔离的模型/参数 fixture 证明 GIF 和 IDEA 的更新确实进入 collateral 消费的模型；验证未写回时能够失败，不能只匹配源码注释。
- 实际加载路径与实现身份可核对；废弃的原地删除或覆盖结果路径不再是活动入口。
- 相关代码回归通过，形成可审阅的软件候选和验证说明；不要求正式数据、SSH 或 GPU 实验作为 009 的验收条件。
- 旧 collateral/hop 数值保持未验证；本 Block 的接受不构成新实验批准或历史研究证据接受。

## Orchestration contract

- Class: `FIX`
- Priority: `P0 / first repair`.
- Source anchor: L8 IF-family write-back defect and the user's 2026-09-04 separation of software repair from experiment execution.
- Outcome: verified software repair only; replacement research evidence belongs to [AAGU-027](../AAGU-027/WORKITEM.md).
- Fact owner: [this WorkItem](WORKITEM.md) owns the software scope; [L8](../../../self/limitations.md#l8-hop-distance-decay-collateral-if-family-数值-bug-affected) retains the historical defect explanation.
- Relations: 009 software repair has no dependency on `AAGU-001` or `AAGU-002`. `AAGU-027 depends_on AAGU-009` and `AAGU-027 depends_on AAGU-001`; `AAGU-010` consumes accepted evidence from AAGU-027.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `software correctness / evaluation integration`.
- Minimum evidence: actual model write-back and consumer checks, loaded-source identity, targeted local regressions, and explicit software acceptance.
- Confirmation: user authorized narrowing 009 to code repair; retain the explicit human decision route without a formal experiment requirement.
- Report size: paired `REPORT.md` / `REPORT.html` at the software candidate stage; do not present old experiment data as current evidence.

## Boundaries

- Scope permits software changes and isolated local regression tests only. No formal experiment, SSH setup/write, deployment, historical leaf movement, result collection, or payload/cache mutation is part of 009.
- Tests and any definition-only dry-run verify software; they must not become a training, evaluation, ranking, or timing experiment under another name.
- All formal execution, including the former 120-cell repair proposal, waits for the accepted AAGU-001 experiment framework and a separately approved current experiment contract in AAGU-027.
- AAGU-010 aggregation, paper conclusions, selector changes, and unrelated repairs remain outside this Block.

## Existing candidate and restart boundary

- Preserve the existing Claim and `working / claimed` state; this scope revision is neither a new Claim nor acceptance.
- The parked source `codex/aagu-009-collateral-evidence` retains implementation `532b5ea` and the 2026-08-31 local verification record (44 passed). These are historical software evidence, not verification against today's main.
- Before software execution resumes, incorporate this canonical scope and current main into the same source and revalidate the affected code. The former Apply target and source-side formal rerun contract are superseded by this Record.
- The old source-side `evidence/repair-scope.yaml` and preflight notes are historical planning/observations only. Their 120-cell matrix, SSH blockers and move/rerun steps are not a current execution authorization. AAGU-027 must re-establish its experiment identity after AAGU-001.

## Status history

- 2026-08-26: registered from the prominent collateral repair Todo.
- 2026-08-26: corrected the registration-time `AAGU-002 -> AAGU-009` projection error; the legacy E2 repair lane has no AAGU-001/AAGU-002 task dependency.
- 2026-08-26: claimed after the user explicitly said to perform the AAGU-009 repair; the preserved Claim remains the runtime identity for recovery.
- 2026-09-04: 用户要求把 009 收窄为代码修复，将正式实验与 SSH 工作拆至 AAGU-027，并明确所有实验运行都在 AAGU-001 实验框图之后。本次按该语义修订同一 Record、补齐 2.1 Human Surface 并将 Apply target 对齐当前 main；保留原 Claim、历史和进行中状态，没有执行代码修复、实验或验收。
