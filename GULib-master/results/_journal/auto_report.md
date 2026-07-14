# AutoReport

> Rebuildable projection of the append-only V3 event stream. This file is not the audit log.

- Machine events: `auto_report.events.jsonl`
- Events parsed: 0
- Cells shown: 0 of 0 (bounded to 200)
- Current states: none
- Parse warnings: 0

## Legacy baseline

The former live Markdown journal was frozen byte-for-byte. The items below are a curated carry-forward, not reconstructed V3 run events.

- Archived source: `archive/auto_report_2026-05-06_to_2026-07-10_active4090.md`
- Integrity: `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b`; 19020 lines; 2015 parsed entries
- Fixed next-step prose: retired; it is preserved only inside the archive

| Status | Item | Carried-forward fact | Boundary |
|---|---|---|---|
| archived | 4090 live journal cutover | 服务器旧日志覆盖 2026-05-06 至 2026-07-10，共 19,020 行、2,015 条；其中 2,015 条都带固定下一步建议，DECISION 条目为 0。 | 原文件只允许整体归档；不清洗、不压缩、不回填成 V3 当前完成状态。 |
| archive-only | 2026-07-10 GraphRevoker tail | 相对旧 server snapshot 新增 1 条 random attack 与 1 条 collateral：f1_after=0.7140，collateral gap=-1.54%，mean shift=0.0361，flipped=2.96%。 | 旧 attack 的 f1_before=NA 且 cache=HIT 含义不完整；仅作历史证据，不宣称当前 V3 cell complete。 |
| duplicate-probe | 2026-07-10 GraphEraser probes | 新增 3 条临时 collateral probe：random 两次结果完全重复（gap=11.81%），degree 一次（gap=11.81%），路径位于 results/_tmp 或 /tmp。 | 重复 probe 不进入当前进度表，也不提升为新的实验结论。 |
| retired | 固定“下一步建议” | 1,040 条 cache 检查建议与 975 条趋势检查建议不迁入新 AutoReport；V3 只呈现阶段、状态、Cache 来源、错误和重试事实。 | 旧建议原文只保留在服务器 archive 中。 |

## Current V3 cells

| Updated (UTC) | Cell | State | Stages | Cache | Attempt | Run | Config |
|---|---|---|---|---|---:|---|---|
| - | No V3 events yet | - | - | - | - | - | - |

Audit authority stays in `auto_report.events.jsonl`; archived v1/v2 Markdown and the curated baseline are read-only evidence.
