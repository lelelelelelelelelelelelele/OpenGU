# AAGU-010 · FIX · Hop Aggregate Fields

Block ID: `AAGU-010`

当前状态: `registered / not claimed`

Item Type: Block

## Orchestration contract

- Class: `FIX`
- Priority: `P0` immediately after accepted AAGU-009 collateral evidence.
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
- 2026-08-26: priority raised to P0 by explicit user direction; implementation remains unclaimed and depends only on accepted AAGU-009 evidence.
