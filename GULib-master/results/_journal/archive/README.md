# `results/_journal/archive/` — frozen journal snapshots

Point-in-time, **read-only** archives of `auto_report.md` journals. These are
historical evidence, **NOT live logs** — do not append to them, and do not run
experiments that target them. `../auto_report.md` is now a bounded generated
view; the append-only live source is `../auto_report.events.jsonl`.

Freezing snapshots (and dating them) prevents a future re-run's auto-append from
polluting the historical record and forcing a re-clean.

| snapshot | source | coverage | lines | pulled |
|---|---|---|---|---|
| `auto_report_2026-05_phaseB_server.md` | server `~/autodl-fs/.../results/_journal/auto_report.md` (downloaded by user) | Phase B server runs **2026-05-06 → 05-07** | 18,968 | 2026-06-20 |
| `auto_report_2026-05-06_to_2026-07-10_active4090.md` | active 4090 `/autodl-fs/data/OpenGU/GULib-master` | 2,010 prior entries + 5 server-only tail entries | 19,020 | 2026-07-14 |

**Why the server snapshot matters**: the old local journal was only a small
fragment that does **not** contain the arxiv runs. The 18,968-line server copy
is the **authoritative audit trail**. It was used (2026-06-20) to verify the
arxiv pilot = exactly **6 completed cells** (GIF/GNNDelete × {random, tracin, im},
seed42, r0.01), all of which are present locally — i.e. **nothing was stranded**
on the now-recycled server container. The two empty local dirs
(`GIF_hybrid`, `GraphEraser_random`) never completed and are absent from this
journal. See `self/dashboard/PROGRESS.md` §1.

The active 19,020-line 4090 cutover snapshot has SHA-256
`0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b`.
Its five server-only tail entries are inventoried in `../auto_report_baseline.json`;
fixed “下一步建议” prose is intentionally not carried forward.
