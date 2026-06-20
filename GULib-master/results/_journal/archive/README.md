# `results/_journal/archive/` — frozen journal snapshots

Point-in-time, **read-only** archives of `auto_report.md` journals. These are
historical evidence, **NOT live logs** — do not append to them, and do not run
experiments that target them. The live journal stays at `../auto_report.md`.

Freezing snapshots (and dating them) prevents a future re-run's auto-append from
polluting the historical record and forcing a re-clean.

| snapshot | source | coverage | lines | pulled |
|---|---|---|---|---|
| `auto_report_2026-05_phaseB_server.md` | server `~/autodl-fs/.../results/_journal/auto_report.md` (downloaded by user) | Phase B server runs **2026-05-06 → 05-07** | 12,056 | 2026-06-20 |

**Why this snapshot matters**: the live `../auto_report.md` is only a ~198-line
fragment that does **not** contain the arxiv runs. This 12,056-line server copy
is the **authoritative audit trail**. It was used (2026-06-20) to verify the
arxiv pilot = exactly **6 completed cells** (GIF/GNNDelete × {random, tracin, im},
seed42, r0.01), all of which are present locally — i.e. **nothing was stranded**
on the now-recycled server container. The two empty local dirs
(`GIF_hybrid`, `GraphEraser_random`) never completed and are absent from this
journal. See `self/dashboard/PROGRESS.md` §1.
