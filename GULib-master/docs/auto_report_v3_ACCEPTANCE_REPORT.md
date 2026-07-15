# AutoReport V3 acceptance report

> Date: 2026-07-15
>
> Branch: `codex/autoreport-v3-20260714`
>
> Accepted tip: `ef1def3`
>
> Verdict: **PASS — REMOTE DEPLOYED, TERMINAL CONSISTENCY VERIFIED**

## Outcome

AutoReport V3 is deployed in the active 4090 checkout and accepted for current use. The append-only JSONL stream, bounded Markdown/HTML views, retry linkage, typed Cache provenance, and legacy archive boundary all passed local and remote validation.

The live probe exposed one final correctness gap after the earlier local acceptance: an empty `attack.json` result set could be reported as `attack.failed`, followed by collateral work and a false `run.completed`. The accepted fix now enforces the terminal contract at four layers:

- `demo_attack.py` exits nonzero when no attack result is produced;
- `experiments/run.py` validates the semantic contents of `attack.json` before collateral;
- the event writer rejects `run.completed` or `run.skipped` after a failed stage in the same run;
- the bounded view gives stage failure precedence when projecting an already-recorded inconsistent historical sequence.

## Acceptance summary

| Evidence | Result |
|---|---:|
| Focused AutoReport tests, local | **32 passed** |
| Distinct local regression union | **233 passed, 3 known baseline tests deselected** |
| Focused AutoReport tests, remote 4090 checkout | **32 passed** |
| Remote deployed commit | **`ef1def3`** |
| Live V3 stream after probes | **16 events, 0 parse warnings** |
| Latest live state | **failed, attempt 3; no collateral or false completion** |
| Frozen legacy archive | **19,020 lines / 2,015 entries** |
| TracIn algorithm changes | **0** |

The three deselected tests are the unchanged `tests/test_collateral.py::TestGetTrainedModel` stubs that construct `AttackPipeline` without `args`. This AutoReport work does not modify `attack/pipeline_adapter.py`.

## Live server verification

The active checkout is `/autodl-fs/data/OpenGU/GULib-master`, on `codex/autoreport-v3-20260714@ef1def3`. The server-side focused suite passed with `/root/miniconda3/bin/python`.

The smallest closed-loop probe used `experiments/configs/sanity_one_cell.yaml` for Cora/GCN/GIF/random/seed42. The existing leaf was backed up before regeneration at:

`/autodl-fs/data/OpenGU/_backups/autoreport_sanity_before_fa67c13_20260715`

The probe sequence provided three useful observations:

| Attempt | Observation | AutoReport result |
|---:|---|---|
| 1 | Attack subprocess returned nonzero | `attack.failed` + `run.failed` |
| 2 | Pre-fix empty attack result continued into collateral | Contradictory historical sequence exposed the terminal-consistency gap |
| 3 | Post-fix Legacy Cache freeze again prevented an attack result | Failed fast in 8.2 seconds; `attack.failed` + `run.failed`; no collateral; no `run.completed` |

The Legacy Cache freeze is an intentional Cache V2 policy. It is therefore correct for this old writer path to fail. AutoReport acceptance depends on recording that failure accurately and preventing a false completion, which attempt 3 verified.

## Current machine and human surfaces

- `results/_journal/auto_report.events.jsonl` is the immutable audit authority.
- `results/_journal/auto_report.md` and `.html` are bounded projections rebuilt from JSONL plus the curated baseline.
- The current server projection reports `failed=1`, attempt 3, with 0 parse warnings.
- The pre-fix contradictory attempt remains in the append-only stream. It was not deleted or rewritten; the corrected projection classifies it as failure rather than complete.
- The frozen v1/v2 server archive remains byte-for-byte preserved with SHA-256 `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b`.

## Terminal and append policy

| Situation | Accepted behavior |
|---|---|
| Real attempt begins | Append `run.started`; retries add `run.retrying`, `retry_of`, and incremented attempt |
| First terminal stage result | Append `selection`, `attack`, or `collateral` completion/failure |
| Attack payload is missing, empty, or lacks the requested strategy | Mark attack and run failed; stop before collateral |
| A stage has failed in a run | Reject later `run.completed` / `run.skipped` for that run |
| Old stream already contains stage failure plus run completion | Preserve bytes; project the run as failed |
| Standalone unchanged Cache reuse | Compress by Cache/Recipe/Artifact/config identity |
| Runner-managed retry reuses Cache | Preserve per-attempt stage history |
| Dry-run, fixed suggestions, internal probes | Append nothing |
| Existing JSONL is malformed or unverifiable | Refuse append without rewriting or truncating the stream |

## Cache and historical boundaries

A Cache HIT in the human view includes Cache type, authority, source, lookup policy, formal Recipe hash or Legacy key, and write outcome. A whole ResultCache hit does not replay a historical SelectionCache hit as a current fact.

The curated baseline retains only explicitly bounded evidence:

- the 4090 archive integrity anchor;
- the verified six-cell Phase B arxiv pilot: GIF/GNNDelete × random/tracin/im, seed42, ratio 0.01;
- GraphRevoker server-tail evidence marked archive-only because legacy HIT provenance is incomplete;
- duplicate GraphEraser probes marked non-promoted;
- retirement of all 2,015 fixed next-step suggestions.

None of these historical facts is backfilled as a current V3 completion event.

## Validation evidence

| Validation | Result |
|---|---|
| `tests/test_auto_report_v3.py`, local | 32 passed |
| Runner, attack, evaluation, demo, collateral, Cache V2, and legacy-freeze union | 233 passed, 3 deselected |
| `tests/test_auto_report_v3.py`, remote | 32 passed |
| Python compilation of changed modules | passed |
| `git diff --check` | passed |
| Pre-fix stream rebuild under corrected projector | 11 events, 0 warnings, state changed from false complete to `failed:attack` |
| Post-fix real attempt | 16 total events, 0 warnings, latest state `failed`, no collateral or false completion |
| Historical archive integrity | 980,451 bytes; 19,020 lines; 2,015 entries; SHA-256 preserved |

## Known boundaries

1. The append path still validates and deduplicates by scanning JSONL. A future read-only index may improve scale but must remain rebuildable from JSONL.
2. The contradictory pre-fix attempt remains immutable audit evidence. It is corrected at projection time and superseded operationally by attempt 3.
3. The three unrelated collateral stub tests remain a known baseline gap.
4. This acceptance verifies reporting correctness, not promotion of the failed GIF sanity cell as research evidence.

## Primary files

- `scripts/evaluation/reporting/events.py`, `writer.py`, `summary.py`, `reader.py`, and `baseline.py`
- `demo_attack.py`, `eval_collateral.py`, and `experiments/run.py`
- `results/_journal/RULES.md`, `auto_report_baseline.json`, `auto_report.md`, and `auto_report.html`
- `tests/test_auto_report_v3.py` and `tests/fixtures/auto_report/`
- `docs/auto_report_v3_DESIGN.md`
