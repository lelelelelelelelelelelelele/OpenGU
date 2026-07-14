# AutoReport V3 acceptance report

> Date: 2026-07-14
>
> Branch: `codex/autoreport-v3-20260714`
>
> Validation scope: local CPU/fixture tests; SSH final deployment is deferred because the server is offline
>
> Verdict: **LOCAL PASS — REMOTE REFRESH PENDING**

## Outcome

AutoReport V3 now separates the append-only machine audit from the bounded human progress view. The old fixed “下一步建议” text is retired; the frozen 4090 journal remains historical evidence, while the new `auto_report.md` and `auto_report.html` are rebuildable views over V3 JSONL plus a small curated baseline.

This local completion pass closes the gaps found after the earlier cutover:

- repeated standalone SelectionCache/ResultCache reuse is compressed by Cache/Recipe/Artifact/config identity instead of growing with every new `run_id`;
- runner-managed attempts keep their own stage history, so retry evidence is not removed by cache-noise compression;
- runner and child processes share a canonical normalized identity envelope; `cell_id` must match it;
- append recomputes event identity, validates the existing stream, and fails closed without modifying a corrupt JSONL;
- append and Markdown/HTML refresh are serialized, preventing an older concurrent projection from overwriting a newer one;
- the human Cache column now distinguishes authoritative Cache V2 hits from Legacy/non-authoritative hits and shows source, lookup policy, Recipe hash or Legacy key.

## Acceptance summary

| Evidence | Result |
|---|---:|
| Focused `tests/test_auto_report_v3.py` | **29 passed** |
| Related attack/runner/evaluation/collateral suite | **117 passed, 3 known baseline tests deselected** |
| AutoReport plus relevant Cache V2 regression suite | **205 passed, 3 known baseline tests deselected** |
| Python compilation | **passed** |
| Existing-stream corruption test | **fail-closed; bytes unchanged** |
| Post-build event tamper test | **rejected before append** |
| Current local status rebuild | **0 events, 0 warnings; Markdown + HTML regenerated** |
| GPU executions / TracIn algorithm changes | **0 / 0** |
| SSH activity in this completion pass | **0** |

The three deselected tests are the unchanged `tests/test_collateral.py::TestGetTrainedModel` stubs that construct `AttackPipeline` without `args`. Running them still produces the same baseline `AttributeError`; this AutoReport change does not modify `attack/pipeline_adapter.py`.

## Append and compression policy

| Situation | Audit behavior |
|---|---|
| Real runner attempt begins | append `run.started`; retries also append `run.retrying` with `retry_of` and incremented `attempt` |
| Selection, attack, or collateral reaches a first terminal state | append the terminal stage event |
| Runner and child report the same run/stage/state | retain one event by the shared transition identity |
| Standalone stage is wholly served by the same SelectionCache/ResultCache entry | append one semantic cache-reuse event; suppress unchanged repeats |
| Runner attempt reuses Cache but still performs downstream work | retain the per-attempt stage event |
| Complete cell is repeatedly encountered | append one `run.skipped` per unchanged config/Artifact identity |
| Dry-run, internal probes, fixed suggestions | append nothing |
| Existing JSONL has malformed or unverifiable content | refuse append; do not rewrite, truncate, or repair automatically |

## Cache meaning in the human view

A HIT is no longer displayed as a bare `cache=HIT`. The projection includes:

- Cache type: `selection`, `result`, `score`, `artifact`, or `run_artifact`;
- authority: `authoritative` for verified formal artifacts, otherwise `legacy/non-authoritative`;
- hit source and lookup policy;
- formal Recipe hash or Legacy cache key;
- write outcome in the machine event.

A whole ResultCache hit does not replay the historical `selection_cache_hit` stored inside the cached `AttackResult` as a current SelectionCache hit.

## Historical content retained without log noise

The verified server archive remains the 19,020-line / 2,015-entry file with SHA-256 `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b`. It is not rewritten into V3 events.

The bounded baseline now carries only useful, explicitly scoped facts:

- the 4090 cutover integrity anchor;
- the verified six-cell Phase B arxiv pilot: GIF/GNNDelete × random/tracin/im, seed 42, ratio 0.01;
- the GraphRevoker server-tail attack/collateral evidence, marked archive-only because the old HIT provenance is incomplete;
- the duplicate GraphEraser temporary probes, marked non-promoted;
- retirement of all 2,015 fixed next-step suggestions.

The six-cell pilot is a historical summary, not a fabricated V3 completion state and not a claim that the arxiv matrix is complete.

## Implemented checklist

- [x] Append-only machine event schema with stable cell/run identity, git SHA, and config fingerprint.
- [x] Selection, attack, collateral, and run stages with partial completion and failure/retry states.
- [x] Explicit Cache type, Recipe/Legacy key, Artifact/source, authority, policy, and write outcome.
- [x] Standalone repeated Cache reuse compression without erasing runner retry history.
- [x] Existing-stream fail-closed append and post-build tamper detection.
- [x] Canonical identity propagation from runner to child producers.
- [x] Bounded Markdown and HTML current-state views.
- [x] v1/v2 Markdown reader compatibility without migration or history rewrite.
- [x] Fixed automatic suggestions retired from new reports.
- [x] Useful historical content organized into a curated baseline instead of copied wholesale.
- [x] Local fixture, integration, Cache V2 regression, compilation, and report-parity validation.
- [ ] Final server fast-forward/rebuild verification — deferred until SSH is reopened.
- [ ] GPU experiment execution — deliberately not part of reporting acceptance.

## Boundaries and known gaps

1. This pass did not connect to the server and did not modify remote user data, caches, runs, or the archived journal.
2. The append path currently validates/deduplicates by scanning JSONL. A read-only derived index may be added later if V3 volume becomes large; it must not replace JSONL as audit authority.
3. Three unrelated collateral stub tests remain a known baseline gap.
4. Final remote deployment and regeneration of the live views remain pending while SSH is closed.

## Primary files

- `scripts/evaluation/reporting/events.py`, `writer.py`, `summary.py`, `reader.py`, and `baseline.py`
- `demo_attack.py`, `eval_collateral.py`, and `experiments/run.py`
- `results/_journal/RULES.md`, `auto_report_baseline.json`, `auto_report.md`, and `auto_report.html`
- `tests/test_auto_report_v3.py` and `tests/fixtures/auto_report/`
- `docs/auto_report_v3_DESIGN.md`
