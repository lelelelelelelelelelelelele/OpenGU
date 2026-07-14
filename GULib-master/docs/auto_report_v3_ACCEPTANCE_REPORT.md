# AutoReport V3 acceptance report

> Date: 2026-07-14
>
> Branch: `codex/autoreport-v3-20260714`
>
> Source baseline: `648a6f1` on `codex/citeseer-e1-graphrevoker-20260714`
>
> Verdict: **PASS WITH KNOWN BASELINE GAP**

## Verdict

AutoReport V3 is implemented and deployed to the active 4090 checkout. The former server `auto_report.md` was renamed byte-for-byte into an archive, its five server-only tail entries were inventoried, and the live `auto_report.md` / `.html` names now hold a bounded view rebuilt from the append-only V3 event stream plus a curated baseline.

The 2,015 fixed “下一步建议” lines were not migrated. Legacy writer APIs remain importable only for explicit fixture/export paths; the three old evaluation runners now write V3 events.

One unrelated baseline gap remains: three `tests/test_collateral.py::TestGetTrainedModel` tests use an `AttackPipeline` stub without `args`. The implementation file is unchanged from the requested base, so this work did not repair that separate issue.

## Acceptance summary

| Evidence | Result |
|---|---:|
| Focused AutoReport tests, local | **16 passed** |
| Focused AutoReport tests, active 4090 | **16 passed** |
| Selected local regressions | **206 passed** |
| Known unrelated collateral baseline | **3 deselected** in scoped run |
| Server legacy archive | **980,451 bytes / 19,020 lines / 2,015 entries / 0 decisions** |
| Server archive SHA-256 | `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b` |
| Server summary rebuild | **0 warnings; MD/HTML hashes stable** |
| Runner dry-run | **1 would_run; report hashes unchanged; no JSONL created** |
| Changes/deletions under server caches or runs | **0** |
| GPU executions / TracIn changes | **0 / 0** |

## Deployed layout

```text
runner + attack + collateral producers
                │ stage/state/cache/error facts
                ▼
auto_report.events.jsonl              append-only audit authority
                │
                ├──────────────┐
                ▼              ▼
auto_report.md          auto_report.html       bounded, rebuildable views
                ▲              ▲
                └──── baseline ┘

archive/auto_report_2026-05-06_to_2026-07-10_active4090.md
                └─ frozen v1/v2 source; never rewritten
```

Server deployment root: `/autodl-fs/data/OpenGU/GULib-master`.

The archive remains untracked user data on the server. The tracked `auto_report_baseline.json` stores its verified size, line/entry counts, checksum, and the disposition of useful tail content. Missing local copies are allowed; when the archive exists beside the baseline, its checksum and line count are verified during rebuild.

## Server-content triage

The active server journal was compared with the earlier 2,010-entry snapshot. Exactly five entries were server-only:

| Server-only content | Disposition |
|---|---|
| GraphRevoker random attack, `f1_after=0.7140`, Legacy `cache=HIT` | Archive-only: `f1_before=NA` and HIT provenance is insufficient for a V3 current fact |
| GraphRevoker random collateral, gap `-1.54%`, mean shift `0.0361`, flipped `2.96%` | Recorded in baseline as historical tail evidence; not a completed V3 cell |
| GraphEraser random collateral probe ×2, identical gap `11.81%` | Duplicate temporary probe; not promoted |
| GraphEraser degree collateral probe, gap `11.81%` | Temporary probe; not promoted |

The old file contained 1,040 cache-check suggestions and 975 trend-check suggestions. All remain intact in the archive and are absent from the new live report.

## Implemented checklist

- [x] Append-only V3 JSONL schema with stable `cell_id`, per-attempt `run_id`, `git_sha`, and config fingerprint.
- [x] `selection`, `attack`, `collateral`, and `run` stages with started/completed/failed/skipped/retrying states.
- [x] Typed Cache observations: type, outcome, Recipe/Legacy key, Artifact/source, lookup policy, authority, write outcome, and miss reason.
- [x] Whole ResultCache hits no longer replay an old SelectionCache HIT.
- [x] Exact transition dedup and unchanged skip/HIT compression without rewriting prior lines.
- [x] Selection-only, attack-only, collateral, complete/cached, running, and failed projections.
- [x] Active server legacy journal archived with before/after checksum equality.
- [x] Five server-only entries classified; duplicate probes and ambiguous Legacy HIT not promoted.
- [x] New `auto_report.md` and `.html` deployed and rebuilt on the active 4090 checkout.
- [x] Automatic next-step prose retired.
- [x] Default legacy Markdown writing disabled; explicit fixture/export compatibility retained.
- [x] Old evaluation runners migrated to V3 events.
- [x] v1/v2 reader compatibility retained against frozen archives.
- [x] A6 user config, caches, score/selection caches, runs, and current E4 fresh checkout left untouched.
- [ ] GPU experiment execution — deliberately not done.

## Validation evidence

| Validation | Result |
|---|---|
| `tests/test_auto_report_v3.py` locally | 16 passed |
| Same focused suite on active 4090 | 16 passed |
| AutoReport + AttackManager + Phase B invariants | 75 passed |
| Evaluation CLI + demo + repair/timeout runners | 36 passed |
| Cache V2 core/materializer/canary/store | 79 passed |
| Collateral excluding unchanged stub gap | 16 passed, 3 deselected |
| Selected regression total | 206 passed |
| Python compilation of changed reporting/runners | passed locally and on server reporting modules |
| Local runner dry-run | `would_run=1`; report hashes stable; event stream absent |
| Server summary rebuild | parse warnings `0`; MD/HTML hashes unchanged; event stream absent |
| Server archive integrity | checksum, 980,451 bytes, 19,020 lines, and 2,015 headings verified |
| `git diff --check` | passed |

## Files and boundaries

Primary additions/changes include:

- `scripts/evaluation/reporting/events.py`, `summary.py`, `baseline.py`, `reader.py`, and `writer.py`
- `scripts/evaluation/runners/run_cross_dataset_resume.py`, `run_ratio05.py`, and `run_round2.py`
- `demo_attack.py`, `eval_collateral.py`, and `experiments/run.py`
- `results/_journal/auto_report.md`, `auto_report.html`, `auto_report_baseline.json`, `RULES.md`, and `archive/README.md`
- `tests/test_auto_report_v3.py` and fixtures

The server archive itself is intentionally not committed. It stays at:

`/autodl-fs/data/OpenGU/GULib-master/results/_journal/archive/auto_report_2026-05-06_to_2026-07-10_active4090.md`

## Known gaps

1. Three pre-existing collateral stub tests remain outside this change.
2. Event rebuild/dedup scans the JSONL stream. A read-only derived index may be added if the machine stream later becomes large.
3. No GPU experiment was run as part of reporting acceptance; current E4 work continued in its separate fresh checkout.
