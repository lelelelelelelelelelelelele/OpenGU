# AAGU-023 · Legacy 实验证据归档与清理

Block ID: `AAGU-023`
Item Version: 2.1
Item Type: `Block`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/main`

> Git baseline：`3ec3d56476f008f7bfc94b4e62a70efd239be6e2`

> Source branch：`refs/heads/codex/aagu-023-legacy-evidence-archive`

> Remote target：`origin refs/heads/main`
当前状态: `working / claimed`
Stable locator: `.workblock/items/AAGU-023/WORKITEM.md`

## Human Surface

### 核心意图

集中归档不再支持当前正式结论的旧实验 payload 与 Legacy Cache，完整保留批次身份、来源、失效原因、替代依据及可追溯 manifest，避免旧证据继续被正式运行或论文结论误用。

### 本次增量

盘点本机与 SSH 上的 `results/cache`、`results/selection_cache`、`results/score_cache` 及相关旧实验 payload；核实仍存活的代码消费者；建立统一 manifest 和 replacement/retirement ledger；将确认退役的内容归档并从当前正式证据入口隔离。不得删除 payload，也不得改动 `results/cache_v2`。

### 核心验收

能够逐批回答“它是什么、来自哪里、为何失效、由什么替代、现在归档在哪里”；本机与 SSH ledger 一致；旧 payload 不再能被误认为当前正式证据；现行消费者、正式结果和 Cache V2 未被误伤；所有删除仍为零。

## Scope

- 盘点三个 Legacy Cache 根、相关本机/SSH 旧实验 payload 及其当前消费者。
- 建立保留路径/设备、批次身份、来源、失效原因、替代依据、校验与状态的 manifest 和本机/SSH 共同 retirement ledger。
- 将确认退役的内容移入可追溯归档，从当前正式证据入口隔离；仅在消费者确认过时且有可复核依据时退役旧路径引用。
- 为归档、隔离、消费者退役及 Cache V2 零改动建立确定性验证和配对报告。

## Non-goals

- 不删除任何本机或 SSH payload，不以归档授权替代删除授权。
- 不改写旧实验结果，不修复、重命名、覆盖或手工删除任何 Cache V2 Artifact。
- 不重跑正式 GPU 实验；需要新证据时另行按当前研究计划注册与执行。

## Acceptance contract

- Route: `formal`。
- Primary surface: data / lifecycle / integration。
- Minimum real evidence: 消费者扫描、逐批 manifest、失效与替代依据、归档前后路径及校验信息、本机/SSH ledger 对照、Cache V2 未改动证明。
- Decision owner: 用户。
- Post-candidate decision: 形成 clean exact candidate 后停在 `awaiting_acceptance`，由用户决定接受或返工；Verify PASS 不自动 Apply。
- Report size: paired Markdown/HTML Report。

## Initial idea

将不再支持当前正式 claim 的旧实验 payload 与 Legacy Cache 集中归档，保留批次身份、来源、失效原因和可追溯 manifest，并防止其被当前正式运行或论文结论误用。优先归档而非直接删除，只重跑当前研究计划仍需要的证据。

## Recorded context

- 当前 target-direct formal Cache 权威是统一的 `results/cache_v2`，不是三个 Legacy 目录。
- `results/cache`、`results/selection_cache`、`results/score_cache` 分别是旧架构的 ResultCache、SelectionCache 和 ScoreCache 物理位置。generic AttackManager 目前仍有默认引用，但是否连 Legacy 执行路径一起彻底退役、以及是否需要保留空目录，留待本 Todo Promote 时确认。
- 归档范围需分清 pre-2026-06 `80/0/20` 证据、2026-07 public/fixed-`k` 工程证据、tracked 轻量报告、ignored 重型 payload，不得把不同身份混成一个结果批次。
- 本机与 SSH 的 Legacy 证据应使用同一份批次清单和 replacement/retirement ledger；实际归档或删除必须在后续独立验收范围内明确授权。

## Boundary

- 本次 Promote 只注册可执行 Block；不 Claim、不实施、不访问 SSH，不移动或改写任何 result/cache payload。
- 后续 Run 可在完成实时盘点、身份与消费者核实后执行已确认的归档移动与正式入口隔离；每一批均必须先进入 manifest/ledger。
- 删除本机或 SSH payload 未获授权；任何删除均需新的明确人类授权。
- `results/cache_v2` 是当前 target-direct formal Cache 边界，本 Block 不修复、重命名、覆盖或手工删除其 Artifact。

## Status history

- 2026-08-31: Registered as Todo only; not claimed or implemented.
- 2026-09-02: Upgraded the same Todo from WorkItem 2.0 to 2.1 without changing its identity, status, or cleanup authority.
- 2026-09-02: Promoted the same `AAGU-023` to a formal, sequential Block after human confirmation; remains `registered / not claimed`.
- 2026-09-02: Claimed as the same Block by session `AAGU-023 · Legacy evidence inventory and archive`; Claim `2c8e25f2-5ca9-42a1-82ee-a3a3c2b6693e` is `ongoing` revision 1.

## Run inventory and archive decision

- Execution envelope: parent `refs/heads/main` at `3ec3d56476f008f7bfc94b4e62a70efd239be6e2`; source `refs/heads/codex/aagu-023-legacy-evidence-archive`; owned paths are this item package, `scripts/legacy_evidence_inventory.py`, its focused tests, and the generator-owned WORKPLAN/progress projection. This Run stops at a committed candidate; no merge, push, install, cleanup, or deletion is authorized.
- Machine-readable plan: `evidence/batch-plan.json` declares 20 exact batches, the 2026-05-31 cutoff, `archive_requires_state=REPLACED`, `delete_authorized=false`, forbidden Legacy reuse for new batches, and `results/cache_v2` as the sole protected path rather than a retirement batch.
- Local inventory: `evidence/local-inventory-before.json` and `evidence/local-inventory-after.json` cover 7,044 evidence files. The only unassigned `results/` files are the current governance files `results/AGENTS.md` and `results/README.md`.
- Legacy roots remain distinct: ResultCache 8 files / 59,952 bytes; SelectionCache 9 / 19,696; ScoreCache 26 / 697,912. The live source scan records 74 API/path references across production code, legacy tools/configuration, and tests, so none of the three roots is archive-eligible.
- Existing isolation is preserved: the 2026-05-06, 2026-05-07, and 2026-07-21 archive batches contain 2,675 / 28 / 126 files and remain in their existing archive locations. `results/runs` is split into exact 4090, ablating, 2026-07 engineering, H20, and arXiv sub-batches; it is never treated as one retirement batch.
- Local before/after comparison: `evidence/local-inventory-comparison.json` reports no batch changes, no protected-path changes, `moves_observed=0`, `deletions_observed=0`, and `cache_v2_unchanged=true`. The protected Cache V2 anchor remains 32 files / 983,515 bytes.
- Common ledger: `evidence/retirement-ledger.json` registers every local/SSH location and contains empty move, deletion, and Cache V2 write lists. No batch is in `REPLACED`, so no new physical archive action is valid in this Run.
- SSH observation: live access is `NOT_OBSERVED`. The configured OpenGU aliases `autodl-opengu`, `opengu-4090`, and `4090` each refused banner exchange before any remote command ran. The ledger therefore keeps the five planned SSH pairings at `NOT_OBSERVED` and truthfully sets `device_parity_confirmed=false`; historical 2026-07/08 counts are not promoted into a 2026-09 live observation.
- Integration projection: AAGU-023 now has one Repair mapping in `self/dashboard/WORKPLAN.md`, the registered dependency into AAGU-003 is projected, and `self/dashboard/progress.html` is rebuilt by `scripts/dashboard/refresh.py`.

## Pre-candidate validation

- `PASS` — `tests/test_legacy_evidence_inventory.py`, Cache V2 archive-readiness/freeze guards, AAGU-019 retirement guards, and dashboard generator tests pass `21/21`.
- `PASS` — the changed Python files compile, `scripts/dashboard/refresh.py --check` passes, and `git diff --check` passes.
- `PASS` — the local data/lifecycle surface is deterministic: 20 declared batches, 7,044 assigned evidence files, two explicitly excluded governance files, zero moves, zero deletions, and unchanged Cache V2 anchor.
- `NOT OBSERVED` — live SSH payload hashes, remote consumer count, and local/SSH ledger parity could not be verified while the AutoDL endpoint was unavailable.
- `NOT CONFIRMED` — no physical archive action is eligible because no newly observed batch has reached `REPLACED` with zero downstream references; this is a gate result, not permission to weaken the state machine.
