# AAGU-019 · 硬退役旧小预算实验 setup

Block ID: `AAGU-019`

Item Version: 2.0

当前状态: `accepted`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`


> Git baseline：`cdfb8a0ece41922beb447c2279569ae9448396aa`

> Source branch：`refs/heads/codex/aagu-019-retire-legacy-budgets`

> Remote target：`origin refs/heads/codex/e7-two-surrogate-groups-20260805`
Execution topology: `sequential`

Item Type: Block

## Source

- Anchor: the confirmed repository audit found that historical `k=3/7/14` and fixed-`k=7` experiment setups remain executable and registered even though the formal target-direct contract now uses independent 1%/5% train-candidate budgets.
- Contract context: formal E8 target-direct execution uses the fixed 70/10/20 profile and dataset-specific `k=floor(r * |V_train|)` values: Cora `18/94`, CiteSeer `23/116`, PubMed `138/690`.
- Baseline: `target_direct_formal_v2` already validates the correct ratios and counts, but its implementation still imports legacy experiment packages; historical small-budget recipes remain present in the active SyncMate registry and active paper-outline evidence paths.

## Intent

- Why now: prevent obsolete small-budget execution identities and historical evidence from entering future formal runs, aggregates, figures, or paper claims.
- Change: hard-retire the old executable setup instead of rewriting its identity in place; preserve historical reports/results as read-only local evidence while making the current ratio-conditioned formal lane self-contained.
- Human outcome: there is one unambiguous executable target-direct experiment contract for the current theory budget, and historical `k=3/7/14` or fixed-`k=7` material cannot be mistaken for current evidence.

## Scope

- Remove historical small-selection and fixed-`k=7` recipes from the active SyncMate registry and remove their obsolete executable configs and launchers.
- Move the scoring, Recipe-validation, and dataset-source primitives still required by current consumers out of legacy experiment packages, then delete the obsolete source paths without compatibility fallbacks.
- Make `target_direct_formal_v2` own or depend only on current/neutral modules and retain its exact 1%/5% budget and checkpoint identities.
- Remove historical small-budget evidence from active new-figure and paper-outline inputs while preserving explicit historical navigation.
- Add regression guards that reject legacy recipe IDs, old result roots, fixed `k=7`, and `3/7/14` identities in the current formal execution and aggregation surfaces.
- Update affected tests, documentation generators, and source fingerprints in the same candidate.

## Non-goals

- Do not delete, rename, overwrite, or rewrite historical reports, accepted result payloads, Cache V2 Artifacts, or their original identities.
- Do not convert an old setup in place to the new ratios and do not add a migration or backward-compatibility layer.
- Do not change the formal 70/10/20 split, the train-candidate denominator, rounding rule, model, GU method, selector semantics, or approved dataset-specific counts.
- Do not execute a formal GPU gate or matrix and do not claim new research evidence.
- Do not absorb or bypass the independently registered AAGU-018 graph-source label-scope correction.

## Implementation and verification

- Retired executable source roots: `experiments/bc_target_v2/`,
  `experiments/gu_target_v1/`, and `experiments/tracin_v2/`.
- Retired configuration set: 13 tracked `syncmate_small_selection*.yaml`
  files; their historical result and report roots were not changed.
- Current primitives now live in `experiments/planetoid_source.py` and
  `experiments/target_direct_v1/{scoring,planetoid_io,recipe}.py`; no legacy
  compatibility import or fallback was added.
- Active SyncMate inventory changed from 76 recipes (44 retired + 29
  target-direct + 3 generic) to 32 recipes (29 target-direct + 3 generic).
- Focused verification: 331 tests passed across retirement guards,
  target-direct contracts, SyncMate/Cache/report integration, dataset-source
  consumers, and affected regressions. A separate full-repository pytest run
  was manually interrupted after about 12 minutes while still CPU-active and
  produced no terminal result; it is not counted as PASS evidence.
- Historical tracked subtrees remained unchanged at baseline tree identities:
  `results` = `3bbc950bcb0906621c8bf682eda00b70555c4bad`, `reports` =
  `4e9e6ecf8d991c6e38008dcf40f97d3d96231f6f`.
- Human decision surface: `REPORT.md` and `REPORT.html` beside this Record.

## Acceptance contract

- Route: `formal`.
- Primary surface: experiment contract, execution registry, and publication evidence boundary.
- Decision owner: human user; successful verification alone does not accept the Block.
- Report size: paired `REPORT.md` / `REPORT.html` with compact evidence under this WorkItem.

### Acceptance items

- No active SyncMate or CLI entry can launch the historical `3/7/14` or fixed-`k=7` experiment setup.
- The current target-direct implementation has no import or runtime dependency on retired experiment packages.
- Formal execution accepts only ratios 1%/5% with Cora `18/94`, CiteSeer `23/116`, and PubMed `138/690`, failing closed on mismatches.
- Historical reports/results remain available and unchanged, but no active aggregate, figure, or paper-result input treats them as current formal evidence.
- Focused and regression verification passes on a clean candidate without producing formal experiment artifacts.

### Minimum evidence

- Registry/CLI inventory before and after cleanup, including absence of all retired recipe IDs and executable configs.
- Import/dependency and evidence-routing audit showing the current lane is self-contained and historical roots are rejected.
- Targeted budget/manifest/SyncMate tests plus affected regression suites and generated-document consistency checks.

## Context and relations

- Blueprint scope: E8 target-direct white-box execution and the A.6/A.7 influence-selector evidence boundary.
- Confirmed Block relation: `AAGU-019 depends_on AAGU-018` because AAGU-018 owns a correctness change in the same D-GIF/BC-target scoring boundary that must be settled before the legacy package is moved or removed.
- No other Block relation is asserted.

## Registration and execution boundary

- Project config: `.workblock/project.json`.
- Previewed config digest: `32f7e5c4b7a1b425e2f777e32233a87fa700578f825dcabaec262c737b30546e`.
- Registration confirmation: user explicitly requested `直接注册 并写入block` on 2026-08-26 after confirming the hard-retirement design and formal acceptance route.
- Registration creates this Record and advances the project WorkItem counter only.
- A later user-visible Codex task must use `block-workflow`, re-read AAGU-018 and this Record, and claim AAGU-019 only after its dependency is satisfied.

## Status history

- 2026-08-26: registered from the user-confirmed hard-retirement design; implementation waits for AAGU-018 to settle the overlapping scoring boundary.
- 2026-08-31: upgraded the same stable WorkItem to protocol 2.0 with the current sequential topology and Apply target; no Claim, implementation, or acceptance fact changed.
- 2026-08-31: confirmed AAGU-018 is accepted, created Claim
  `7739d7a2-955f-4ef4-a5a7-1596f5fe8857` from baseline
  `cdfb8a0ece41922beb447c2279569ae9448396aa`, hard-retired the legacy
  executable setup, and completed focused CPU/static verification without
  formal GPU execution; human acceptance remains pending.
- `accepted`（2026-09-01T02:57:31.8070980+08:00）：human user 基于 User reviewed AAGU-019 and explicitly replied: 可以 accept 接受当前已验证候选。
