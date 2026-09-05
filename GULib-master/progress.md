# AAGU-028 progress

- 2026-09-05: Claim ongoing revision 1, claimId b9cb5e56-6c94-4ea3-abd7-f665012b4b74. Owner codex; task 01a07195-b039-7e41-8697-79771fbf7f4f.
- Worktree source: E:/project/OpenGU-worktrees/aagu-028-retrain-metrics/GULib-master/GULib-master.
- Read configuration, modular execution, ResultCache, existing retrain helper and dependent launcher references. No producer run yet.

- 28 real CPU consumer checks passed (new Retrain/output tests plus existing modular consumers). Independent Retrain has no baseline checkpoint producer; hot read and Metrics-only pass with optimizer steps forbidden.
- Directory recovery: a tool state variable did not persist; three edits briefly landed in canonical A. Exact owned differences moved into linked source and baseline CRLF restored; canonical git status is clean. All following commands name the literal full source path.
- Initial output archive rejected nested ZIP members/order; now flat deterministic member names and explicit group order, validated by warm read.

- Clean checkpoint 936394329433bf518fb22c800ca7233af1fb5dbe: 160/160 tests and standalone 24-node example passed; 3,995 protected historical files unchanged. First Verify exposed an obsolete rounded-result assertion, corrected in the same Block.
- Paired formal report generated from observed evidence and inspected in Chromium; current decision pending. Report-only final diff reuses the exact checkpoint checks, with independent report/link/render verification. No formal run or acceptance action performed.
