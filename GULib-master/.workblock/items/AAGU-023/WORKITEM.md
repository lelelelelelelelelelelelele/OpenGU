# AAGU-023 · Legacy 实验证据归档与清理

Todo ID: `AAGU-023`
Item Version: 2.0
Item Type: `Todo`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-023/WORKITEM.md`

## Initial idea

将不再支持当前正式 claim 的旧实验 payload 与 Legacy Cache 集中归档，保留批次身份、来源、失效原因和可追溯 manifest，并防止其被当前正式运行或论文结论误用。优先归档而非直接删除，只重跑当前研究计划仍需要的证据。

## Recorded context

- 当前 target-direct formal Cache 权威是统一的 `results/cache_v2`，不是三个 Legacy 目录。
- `results/cache`、`results/selection_cache`、`results/score_cache` 分别是旧架构的 ResultCache、SelectionCache 和 ScoreCache 物理位置。generic AttackManager 目前仍有默认引用，但是否连 Legacy 执行路径一起彻底退役、以及是否需要保留空目录，留待本 Todo Promote 时确认。
- 归档范围需分清 pre-2026-06 `80/0/20` 证据、2026-07 public/fixed-`k` 工程证据、tracked 轻量报告、ignored 重型 payload，不得把不同身份混成一个结果批次。
- 本机与 SSH 的 Legacy 证据应使用同一份批次清单和 replacement/retirement ledger；实际归档或删除必须在后续独立验收范围内明确授权。

## Boundary

Registered as Todo only; not claimed and not implemented. No result, cache, report, runtime state, local file, SSH payload, Git ref, or current Cache V2 Artifact is moved, deleted, rewritten, or reclassified by this registration.
