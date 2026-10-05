---
tags: [report/progress, status/active]
type: report-index
created: 2026-06-15
updated: 2026-10-05
---

# Progress Reports

`report/progress/` is a chronological archive of progress reports, checkpoints,
and presentation deliverables. It is not the project Obsidian/MOC hub anymore.

- Current experiment state and scientific decisions: [Work Plan](../../self/research/index.html)
- Project document map / Obsidian-style planning hub: see OpenGU DocMap.
- Daily logs: [report/daily-log/](../daily-log/)

## Read First

| Need | Open |
|---|---|
| Current experiment state and next actions | [Work Plan](../../self/research/index.html) |
| Cell-level produced / usable / rerun ledger | [config_inventory.html](../../self/dashboard/config_inventory.html) |
| Complete experiment-framework briefing | [REPORT.html](2026-07-14_project-framework-briefing/REPORT.html) |
| Advisor-facing progress narrative | [2026-10-05 REPORT.html](2026-10-05_advisor-meeting/REPORT.html) · [editable Markdown](2026-10-05_advisor-meeting/REPORT.md) |
| Historical advisor/review diagnostic source | [advisor_report_2026-06-16.html](../advisor_report_2026-06-16.html) |
| Historical NeurIPS push summary | [2026-05_NeurIPS-Push.md](2026-07-01_advisor-report/2026-05_NeurIPS-Push.md) |
| Project-wide document navigation | See OpenGU DocMap. |

## Chronological Index

| Date | Entry | Function | Status |
|---|---|---|---|
| 2026-02-19 | [2026-02-19_checkpoint/](2026-02-19_checkpoint/) | Early Phase A checkpoint: report, method table, figures | frozen |
| 2026-02-22 | [2026-02-22_checkpoint/](2026-02-22_checkpoint/) | MG checkpoint: report, appendix, figures | frozen |
| 2026-04-17 | [2026-04-17_EE5003-report/](2026-04-17_EE5003-report/) | EE5003 course report and defense package | frozen |
| 2026-05-07 | [2026-05_NeurIPS-Push.md](2026-07-01_advisor-report/2026-05_NeurIPS-Push.md) | NeurIPS push retrospective, filed under the 2026-07-01 checkpoint bundle | frozen |
| 2026-06-16 | [advisor_report_2026-06-16.html](../advisor_report_2026-06-16.html) | Advisor/review diagnostic snapshot; now points forward to the 2026-07-01 current report and dashboard ledger | historical source |
| 2026-06-16 | [2026-06_resume-diagnosis.md](2026-07-01_advisor-report/2026-06_resume-diagnosis.md) | Resume diagnosis after data return and audit, filed under the 2026-07-01 checkpoint bundle | frozen source |
| 2026-07-01 | [2026-07-01_advisor-report/](2026-07-01_advisor-report/) | Advisor checkpoint bundle with current-status HTML report and 05/06 source snapshots | ready |
| 2026-07-14 | [2026-07-14_project-framework-briefing/](2026-07-14_project-framework-briefing/) | Full experiment setup + access spectrum + live Cache/TracIn lanes + scoped result snapshot | ready |
| 2026-10-05 | [2026-10-05_advisor-meeting/REPORT.html](2026-10-05_advisor-meeting/REPORT.html) · [Markdown](2026-10-05_advisor-meeting/REPORT.md) | 18–20-minute advisor manuscript: IF → Retrain → GU, theory candidates, experiment data and Work Plan acceptance | discussion draft |

## New Report Convention

Use this directory only for report-like deliverables: advisor updates, stage
reports, checkpoint bundles, and presentation packages.

- If the report has assets, create `YYYY-MM-DD_short-topic/` with a `README.md`
  or main report file inside.
- If it is a single markdown report, use `YYYY-MM-DD_short-topic.md`.
- Put planning maps, loose notes, and cross-document indexes in the sibling OpenGU DocMap, not here.
- Put current experiment state in `self/research/experiments/` and scientific analysis/decisions in `self/research/analyses/`; Work Plan owns their presentation.
