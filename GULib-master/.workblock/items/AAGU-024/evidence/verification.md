# AAGU-024 · Final verification record

Verification date: 2026-09-01
Git baseline: `be0dd0fad09458d6111ab2e422c8c8bdd3d90bfc`
Source branch: `refs/heads/codex/aagu-024-workitem-2-1`
COMP-042 exact candidate: `08be674abc60c9249982a1c3f341a080cd8b5121`

This record consolidates the final pre-candidate checks. It does not accept, Apply, merge, push, install, clean up, run experiments, or access SSH.

## WorkItem 2.1 migration

- Scope is exactly AAGU-001、002、003、005、007、008、010、011、012、013、014、020、021、022.
- The current Human Surface validator passes for all 14 members and the AAGU-024 owner: `15/15 PASS`.
- Every migrated member has exactly one `Item Version: 2.1`; its first level-two section is the only `## Human Surface`; the three required subsections are present, ordered, and non-empty.
- After removing the protocol version and the old/new human-facing section, every other non-empty line remains byte-for-byte equal to baseline: `14/14 NON_HUMAN_EXACT=True`.
- The AAGU-010 Record/WORKPLAN priority divergence already existed at baseline and remains unresolved rather than being rewritten by this migration.

## Protected paths and Claim guards

- AAGU-004、006、009、015、016、017、018、019、023 and `self/dashboard/WORKPLAN.md` are unchanged from baseline.
- Existing runtime Claim hashes for AAGU-004、006、009 are unchanged.
- The 14 migrated members have zero runtime Claims.
- No experiment code, Cache V2, results, generated dashboard, DocMap, SSH state, or external project source is part of the AAGU candidate.

## Exact-product Companion evidence

- The superseded COMP candidate `f6832b9dec0be903d9f8d83f50ba2bc2864dfbd7` failed closed on the real AAGU snapshot; that failure is preserved in `companion-aagu-probe.md` and is not counted as acceptance evidence.
- Exact COMP candidate `08be674abc60c9249982a1c3f341a080cd8b5121` passes the targeted parser/projection suites: 18/18 tests.
- A fresh isolated registry loaded the clean AAGU snapshot as 24 nodes, 20 relations, Graph factVersion 5, with version counts 1.0/2.0/2.1 = 5/4/15.
- All 14 migrated members project `human.surface.status=available`; nine protected legacy/2.0 representatives project both Human Surface and Human Result as `not_applicable` with null fields.
- AAGU-020's three Human Surface fields match its WorkItem text exactly.

## Native and report evidence

- Three real Windows native captures cover the mixed-version graph, the AAGU-020 2.1 positive case, and the AAGU-004 legacy no-fallback case. Each PNG is 1792×1196.
- The temporary snapshot and registry physically isolate product writes from live AAGU; the snapshot remained Git-clean and inspected WorkItem/graph hashes remained unchanged.
- `REPORT.md` and `REPORT.html` pass the current paired-report validator.
- Final HTML QA at 1280×720 and 390×844 shows one Human Result, one decision projection, all three evidence images loaded, no horizontal overflow, and zero warning/error console entries.

## Toolchain boundary

The AAGU candidate is formed by the currently installed reversible nested-project `run_git.py finish` hotfix, SHA-256 `BC2B64DD7EC8F2ABC68500D0598BC1D09009D25841F4DFD48AC81A876AB272C0`. The hotfix normalizes Git-root-relative porcelain paths to project-relative owned paths, locates the valid `.git` above the nested project, and skips an empty `.git/` directory without `HEAD`. A dedicated nested fixture containing that empty marker completed with the same three Git commands while the outside-project dirt guard remained fail-closed. It is backed up at `C:\Users\ADMIN\.codex\skill-backups\aagu-nested-finish-pre-hotfix-bbb2990\block-workflow` and is not part of WB-228 candidate `bbb299034a58438c691a3f7a5380b005cfe80219`.

## Stop point

The intended terminal state for this turn is one clean AAGU-024 candidate with the owner Claim at `awaiting_acceptance`. Human acceptance and every closeout action remain pending.
