# AAGU-009 · FIX · L8 Collateral Evidence

Block ID: `AAGU-009`

Item Version: 2.0

当前状态: `working / claimed`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Execution topology: `sequential`

Item Type: Block

## Orchestration contract

- Class: `FIX`
- Priority: `P0 / first repair`.
- Source anchor: legacy collateral-evidence redo Todo.
- Outcome: replace invalid or incomplete L8 collateral evidence through a separately accepted repair run.
- Fact owner: OpenGU DocMap rerun/cache-fix runbook; executable identity remains in the final registered recipe.
- Relations: no dependency on `AAGU-001` or `AAGU-002`; `AAGU-010` starts only after this Block's repaired evidence is explicitly accepted.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `research evidence repair`.
- Minimum evidence: corrected runtime identity, complete artifacts, regression checks, and explicit acceptance.
- Confirmation: user explicitly authorized starting AAGU-009 after correcting the spurious experiment-definition/device dependency.
- Report size: paired `REPORT.md` / `REPORT.html`, because the decision concerns formal research evidence and invalid historical outputs.

## Boundaries

- Do not mutate historical artifacts or start a GPU run during registration.
- Formal execution requires one clean full Git SHA, the registered runtime/config identity, at least one GPU, the intended interpreter, and complete collection/read-back; fail closed rather than falling back to CPU.
- AAGU-010, paper conclusions, selector changes, and unrelated result/cache repair remain outside this Block.

## Status history

- 2026-08-26: registered from the prominent collateral repair Todo.
- 2026-08-26: corrected the registration-time `AAGU-002 -> AAGU-009` projection error; the legacy E2 repair lane has no AAGU-001/AAGU-002 task dependency.
- 2026-08-26: claimed after the user explicitly said to perform the AAGU-009 repair; the preserved Claim remains the runtime identity for recovery.
