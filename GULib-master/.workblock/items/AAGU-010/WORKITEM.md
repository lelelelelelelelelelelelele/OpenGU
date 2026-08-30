# AAGU-010 · FIX · Hop Aggregate Fields

Block ID: `AAGU-010`

Item Version: 2.0

当前状态: `registered / not claimed`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Execution topology: `sequential`

Item Type: Block

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
