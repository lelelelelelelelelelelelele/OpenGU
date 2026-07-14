# AutoReport V3 acceptance report

> Date: 2026-07-14
> Branch: `codex/autoreport-v3-20260714`
> Base: `d38df14` (`codex/citeseer-e1-graphrevoker-20260714`)
> Verdict: **PASS WITH KNOWN BASELINE GAP**

## Verdict

The scoped AutoReport redesign is implemented and locally accepted. New high-volume experiment reporting is an append-only JSONL event stream with stable cell/run identity, explicit stages, typed Cache provenance, errors/retries, semantic deduplication, and bounded Markdown/HTML current-state views. Historical v1/v2 Markdown remains untouched and readable.

One unrelated baseline gap remains: three `tests/test_collateral.py::TestGetTrainedModel` tests fail because their `AttackPipeline` stub has no `args`. `attack/pipeline_adapter.py` is byte-identical to the requested base (`c3416918…`), so this implementation did not introduce or repair that failure.

## Acceptance summary

| Evidence | Result |
|---|---:|
| AutoReport V3 focused tests | **12 passed** |
| Selected regression tests across attack, runner, evaluation, collateral, and Cache V2 | **202 passed** |
| Known unrelated baseline tests | **3 failed** when included; **3 deselected** in the clean scoped regression run |
| Large local v1 archive compatibility read | **18,968 lines / 2,010 entries / 0 warnings** |
| Runner dry-run | **1 would_run / 0 runtime journal or status files created** |
| Changes to `results/_journal/auto_report.md` | **0** |
| Changes/deletions under `results/cache` or `results/runs` | **0** |
| GPU executions | **0** |

## Delivered design

```text
experiments/run.py ── shared cell_id/run_id/fingerprint/git SHA ─┐
demo_attack.py ── selection + attack facts ──────────────────────┼─> auto_report.events.jsonl
eval_collateral.py ── collateral + ResultCache provenance ───────┘        append-only
                                                                          │
                                                                          └─> summary.py
                                                                              ├─ auto_report_status.md
                                                                              └─ auto_report_status.html

auto_report.md (v1/v2 history) ── read-only compatibility ──> reader.py
```

The machine stream and human view have different duties:

- `auto_report.events.jsonl` is the immutable audit source.
- `auto_report_status.md` and `.html` are atomically rebuilt, capped at 200 latest cells by default, and never treated as audit originals.
- `auto_report.md` remains the historical v1/v2 source; there is no migration step.

## Implemented checklist

- [x] Append-only V3 JSONL schema with one JSON object per accepted transition.
- [x] Stable `cell_id`; one `run_id` shared by runner, attack, and collateral within an attempt.
- [x] Independent `git_sha` and `config_fingerprint` fields.
- [x] `selection`, `attack`, `collateral`, and `run` stages.
- [x] `started`, `completed`, `failed`, `skipped`, and `retrying` states.
- [x] Selection-only, attack-only, collateral, complete/cached, legacy-skip, running, and failed status projection.
- [x] Retry ordinal plus `retry_of` linkage and subprocess return-code errors.
- [x] Cache `type`, `outcome`, Recipe/Legacy key, Artifact/source, lookup policy, authority, write outcome, and miss reason.
- [x] Separate SelectionCache and ResultCache provenance in `AttackResult`.
- [x] Whole ResultCache hits no longer replay a historical selection HIT as a current fact.
- [x] Exact transition deduplication and unchanged complete-cell skip compression.
- [x] Dry-runs append nothing.
- [x] v1 experiment plus v2 session/decision parsing without migration.
- [x] Old v1 append functions remain callable.
- [x] Fixture coverage for partial, complete, failed, repeated HIT/skip, and retry flows.
- [x] Markdown and HTML acceptance reports agree on verdict and validation counts.
- [ ] Remote 19k-line dirty journal exercised in place — deliberately not done; remote user data was out of mutation scope.
- [ ] GPU experiment execution — deliberately not done.

## Cache hit meaning after the change

| Case | V3 expression |
|---|---|
| SelectionCache reused nodes | `type=selection`, `outcome=hit`, source path/key, lookup mode, `authoritative=false` for Legacy |
| Selection computed after miss | one `selection.completed` with `outcome=miss` and `write_outcome=saved/unknown` |
| Whole ResultCache reused attack output | `type=result`, `outcome=hit`; no current selection HIT is emitted |
| Collateral reads selected nodes from ResultCache | `type=result`, with hash or scan policy and exact source when known |
| Complete run directory satisfies fingerprint/file gates | `type=run_artifact`, `outcome=hit`, authoritative complete-cell skip |
| Cache disabled | `outcome=bypass`, not MISS |
| Provenance unavailable | `outcome=unknown`; authority is never invented |

Legacy keys are stored inside the Recipe description as Legacy identifiers. They are not presented as Cache V2 `recipe_hash` or `artifact_id`.

## Append/noise policy verified

The stream appends real starts, first terminal transitions, retries, errors, and the first unchanged complete-cell skip. It does not append dry-runs, internal probe-by-probe cache messages, fixed “next step” prose, identical runner/child terminal reports, or repeated unchanged HIT/skip observations.

Dedup does not rewrite prior lines. It decides not to append a semantic duplicate while preserving every accepted line.

## Validation evidence

| Validation | Result |
|---|---|
| `tests/test_auto_report_v3.py` | 12 passed |
| AutoReport + AttackManager + Phase B invariants | 71 passed |
| Evaluation CLI + demo + repair/timeout runners | 36 passed |
| Cache V2 core/materializer/canary/store | 79 passed |
| Collateral tests excluding known unchanged stub gap | 16 passed, 3 deselected |
| Python compilation of all changed Python modules | passed |
| `experiments/run.py ... --dry_run --limit 1` | `would_run=1`; no V3 runtime files before or after |
| Local large archived v1 journal parse | 997,027 bytes; 18,968 lines; 2,010 experiments; 0 warnings |
| `git diff --check` | passed |

## Files and boundaries

Primary implementation:

- `scripts/evaluation/reporting/events.py`
- `scripts/evaluation/reporting/reader.py`
- `scripts/evaluation/reporting/summary.py`
- `scripts/evaluation/reporting/writer.py`
- `experiments/run.py`
- `demo_attack.py`
- `eval_collateral.py`
- `attack/attack_result.py`, `attack/result_cache.py`, `attack/attack_manager.py`

Contract and documentation:

- `results/_journal/RULES.md`
- `docs/auto_report_v3_DESIGN.md`
- this report and `report/auto_report_v3_ACCEPTANCE_REPORT.html`

No production V3 event/status file was created during local validation. No historical journal, result cache, selection cache, run directory, or TracIn algorithm was changed or deleted.

The requested source ref advanced after this worktree was created, from the opening snapshot `d38df14` to `648a6f1`, through two documentation-only Git consistency reports. Those paths do not overlap this implementation and were not imported; this branch intentionally retains the audited opening parent `d38df14`.

## Known gaps

1. V3 has not been deployed against the remote dirty journal; the local 18,968-line archive was used for compatibility evidence.
2. The bounded view is small, but rebuilding/dedup currently scans the V3 JSONL stream. If the machine stream becomes very large, a read-only derived index can be added without changing the append-only source.
3. Legacy callers that explicitly invoke the v1 append APIs still produce verbose Markdown by design; the main runner/attack/collateral path no longer does.
4. Three pre-existing collateral stub tests remain outside this change. Their failing implementation file is identical to the base branch.
