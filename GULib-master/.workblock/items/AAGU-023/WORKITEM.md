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

盘点本机与 SSH 的旧实验及 Cache，并把已获授权的退役内容隔离到可恢复归档：SSH 的 full-v4 失败尝试、双端三个 Legacy Cache 根，以及用户追加确认的 15 个本机旧 Score Artifact 和 1 个 SSH 旧 Selection Artifact（连同其专属索引和旧运行记录）。逐批先登记 manifest/ledger，再移动，最后校验原始字节与活动入口隔离。代码接入修复归 AAGU-025；本次只归档证据，不改变缓存机制，不删除文件，不改写 Artifact 或数据库内容。

### 核心验收

能够逐批回答“它是什么、来自哪里、为何退役、是否存在科学替代、现在在哪里、怎样恢复”；双端共享 ledger 一致但不把不同设备的文件群体说成相同副本；已归档的旧缓存不在活动索引中命中；保留项、冻结标记与未授权内容未被误伤。删除、payload/header 改写和 SQL 写入均为零。归档旧协议证据不等于宣布新实验已完成科学替代；只验收本次明确范围，不要求清空全部历史 results。

## Scope

- 盘点三个 Legacy Cache 根、相关本机/SSH 旧实验 payload 及其当前消费者。
- 建立保留路径/设备、批次身份、来源、失效原因、替代依据、校验与状态的 manifest 和本机/SSH 共同 retirement ledger。
- 将确认退役的内容移入可追溯归档，从当前正式证据入口隔离；仅在消费者确认过时且有可复核依据时退役旧路径引用。
- 为归档、隔离、原字节保全和双端账本一致性建立确定性验证与配对报告；V2 只包含上述 16 个已授权旧 Artifact 的整组移动例外。

## Non-goals

- 不删除任何本机或 SSH payload，不以归档授权替代删除授权。
- 不改写旧实验结果，不修复、重命名内部身份、覆盖或删除任何 Cache V2 Artifact；获授权的旧 Artifact 连同专属索引原样移到归档，其他 V2 内容仍不可改动。
- 不重跑正式 GPU 实验；需要新证据时另行按当前研究计划注册与执行。

## Acceptance contract

- Route: `formal`。
- Primary surface: data / lifecycle / integration。
- Minimum real evidence: 消费者核查、逐批 manifest、退役与替代依据、移动前后路径及 SHA-256、本机/SSH ledger 对照、16 个旧 V2 Artifact 的隔离与零字节改写证明，以及保留项边界。
- Decision owner: 用户。
- Post-candidate decision: 形成 clean exact candidate 后停在 `awaiting_acceptance`，由用户决定接受或返工；Verify PASS 不自动 Apply。
- Report size: paired Markdown/HTML Report。

## Initial idea

将不再支持当前正式 claim 的旧实验 payload 与 Legacy Cache 集中归档，保留批次身份、来源、失效原因和可追溯 manifest，并防止其被当前正式运行或论文结论误用。优先归档而非直接删除，只重跑当前研究计划仍需要的证据。

## Historical registration context (superseded where noted below)

- 当前 target-direct formal Cache 权威是统一的 `results/cache_v2`，不是三个 Legacy 目录。
- `results/cache`、`results/selection_cache`、`results/score_cache` 分别是旧架构的 ResultCache、SelectionCache 和 ScoreCache 物理位置。generic AttackManager 目前仍有默认引用，但是否连 Legacy 执行路径一起彻底退役、以及是否需要保留空目录，留待本 Todo Promote 时确认。
- 归档范围需分清 pre-2026-06 `80/0/20` 证据、2026-07 public/fixed-`k` 工程证据、tracked 轻量报告、ignored 重型 payload，不得把不同身份混成一个结果批次。
- 本机与 SSH 的 Legacy 证据应使用同一份批次清单和 replacement/retirement ledger；实际归档或删除必须在后续独立验收范围内明确授权。

## Historical Promote boundary (not the current Run authorization)

- 本次 Promote 只注册可执行 Block；不 Claim、不实施、不访问 SSH，不移动或改写任何 result/cache payload。
- 后续 Run 可在完成实时盘点、身份与消费者核实后执行已确认的归档移动与正式入口隔离；每一批均必须先进入 manifest/ledger。
- 删除本机或 SSH payload 未获授权；任何删除均需新的明确人类授权。
- `results/cache_v2` 是当前 target-direct formal Cache 边界，本 Block 不修复、重命名、覆盖或手工删除其 Artifact。

## Status history

- 2026-08-31: Registered as Todo only; not claimed or implemented.
- 2026-09-02: Upgraded the same Todo from WorkItem 2.0 to 2.1 without changing its identity, status, or cleanup authority.
- 2026-09-02: Promoted the same `AAGU-023` to a formal, sequential Block after human confirmation; remains `registered / not claimed`.
- 2026-09-02: Claimed as the same Block by session `AAGU-023 · Legacy evidence inventory and archive`; Claim `2c8e25f2-5ca9-42a1-82ee-a3a3c2b6693e` is `ongoing` revision 1.
- 2026-09-02: Paired formal Report completed and the same Claim transitioned to `awaiting_acceptance` revision 2. Agent recommendation remains `证据不足` because live SSH parity is `NOT OBSERVED`; this status is not human acceptance.
- 2026-09-03: The same Claim returned to `ongoing` revision 3 for SSH rework; no new Block or Claim was created.
- 2026-09-04: User confirmed that physical archive does not wait for AAGU-025 acceptance, then explicitly authorized moving the audited old V2 artifacts and their indexes without permanent deletion. These instructions supersede the blanket V2 no-move boundary only for the exact 16 identities and the blanket REPLACED prerequisite for historical quarantine.
- 2026-09-04: User requested a refreshed candidate. After the unrelated graph revision was committed, the user authorized continuing on the parked original branch. The same Claim was resumed to `ongoing` revision 4; baseline and source branch remain unchanged. No merge, push, install, new archive move, or deletion is part of this report rework.

## Current rework envelope

- Owned paths: this AAGU-023 item package and, only if its projection changes, generator-owned `self/dashboard/WORKPLAN.md` / `progress.html`. Do not modify graph relations, AAGU-025 code, shared Skills, or any result/cache payload.
- Consolidate the three completed operations' original manifests, registration receipts, move receipts and ledgers under `evidence/archive/`. Preserve their bytes and historical wording; the current review explicitly supersedes obsolete wait-for-25 and no-move conclusions instead of altering old audit facts.
- Add a read-only archive verifier and fresh local/SSH hash observations; generate one formal paired Report. Stop at a clean verified candidate and `awaiting_acceptance` for a new human decision.
- Retain existing 2026-05-06 / 2026-05-07 / 2026-07-21 archives, mixed historical experiment/report evidence, retained full-v5/gate engineering evidence and SSH `results/cache_v2/legacy_freeze.json`. These are not silently accepted as current scientific evidence and are not new move targets.
- The original 20-batch plan and inventories below are immutable 2026-09-02 audit snapshots, not the current move plan. Their historical REPLACED gate remains meaningful for scientific replacement, not for the subsequent explicitly authorized historical quarantine.

## Historical 2026-09-02 inventory and archive decision

- Execution envelope: parent `refs/heads/main` at `3ec3d56476f008f7bfc94b4e62a70efd239be6e2`; source `refs/heads/codex/aagu-023-legacy-evidence-archive`; owned paths are this item package, `scripts/legacy_evidence_inventory.py`, its focused tests, and the generator-owned WORKPLAN/progress projection. This Run stops at a committed candidate; no merge, push, install, cleanup, or deletion is authorized.
- Machine-readable plan: `evidence/batch-plan.json` declares 20 exact batches, the 2026-05-31 cutoff, `archive_requires_state=REPLACED`, `delete_authorized=false`, forbidden Legacy reuse for new batches, and `results/cache_v2` as the sole protected path rather than a retirement batch.
- Local inventory: `evidence/local-inventory-before.json` and `evidence/local-inventory-after.json` cover 7,044 evidence files. The only unassigned `results/` files are the current governance files `results/AGENTS.md` and `results/README.md`.
- Legacy roots remain distinct: ResultCache 8 files / 59,952 bytes; SelectionCache 9 / 19,696; ScoreCache 26 / 697,912. The live source scan records 74 API/path references across production code, legacy tools/configuration, and tests, so none of the three roots is archive-eligible.
- Existing isolation is preserved: the 2026-05-06, 2026-05-07, and 2026-07-21 archive batches contain 2,675 / 28 / 126 files and remain in their existing archive locations. `results/runs` is split into exact 4090, ablating, 2026-07 engineering, H20, and arXiv sub-batches; it is never treated as one retirement batch.
- Local before/after comparison: `evidence/local-inventory-comparison.json` reports no batch changes, no protected-path changes, `moves_observed=0`, `deletions_observed=0`, and `cache_v2_unchanged=true`. The protected Cache V2 anchor remains 32 files / 983,515 bytes.
- Common ledger: `evidence/retirement-ledger.json` registers every local/SSH location and contains empty move, deletion, and Cache V2 write lists. No batch is in `REPLACED`, so no new physical archive action is valid in this Run.
- SSH observation: live access is `NOT_OBSERVED`. The configured OpenGU aliases `autodl-opengu`, `opengu-4090`, and `4090` each refused banner exchange before any remote command ran. The ledger therefore keeps the five planned SSH pairings at `NOT_OBSERVED` and truthfully sets `device_parity_confirmed=false`; historical 2026-07/08 counts are not promoted into a 2026-09 live observation.
- Integration projection: AAGU-023 now has one Repair mapping in `self/dashboard/WORKPLAN.md`, the registered dependency into AAGU-003 is projected, and `self/dashboard/progress.html` is rebuilt by `scripts/dashboard/refresh.py`.

## Historical 2026-09-02 pre-candidate validation

- `PASS` — `tests/test_legacy_evidence_inventory.py`, Cache V2 archive-readiness/freeze guards, AAGU-019 retirement guards, and dashboard generator tests pass `21/21`.
- `PASS` — the changed Python files compile, `scripts/dashboard/refresh.py --check` passes, and `git diff --check` passes.
- `PASS` — the local data/lifecycle surface is deterministic: 20 declared batches, 7,044 assigned evidence files, two explicitly excluded governance files, zero moves, zero deletions, and unchanged Cache V2 anchor.
- `NOT OBSERVED` — live SSH payload hashes, remote consumer count, and local/SSH ledger parity could not be verified while the AutoDL endpoint was unavailable.
- `NOT CONFIRMED` — no physical archive action is eligible because no newly observed batch has reached `REPLACED` with zero downstream references; this is a gate result, not permission to weaken the state machine.

## Historical 2026-09-02 candidate verification

- Implementation checkpoint `67be158e77460a26ca3aaa201f0eeb3fc1815a05` is a clean descendant of baseline `3ec3d56476f008f7bfc94b4e62a70efd239be6e2`; its tracked diff contains only this item package, the inventory generator and test, and generator-owned dashboard sources/projection. No tracked `results/` or Cache V2 path changed.
- Candidate Verify reproduced `21/21` relevant tests, Python compilation, dashboard projection check, evidence invariant assertions, ancestry, clean status, and diff checks. Machine evidence hashes are plan `d0bd91b8…`, before `618e274b…`, after `3d7b5e8a…`, comparison `3a88d561…`, and ledger `d5eca3d0…`.
- Formal paired decision surface: `REPORT.md` and `REPORT.html`. It recommends `证据不足`, keeps the user decision pending, and does not convert the missing SSH parity into a PASS.
- Report structure validator passes. HTML visual QA is `NOT OBSERVED`: the in-app browser could not reach the local loopback server and its security policy blocked local `file:` navigation; no alternate browser or policy bypass was used.
- The final decision candidate is the clean report-bearing `HEAD` formed after the paired Report, HTML inspection result, and `awaiting_acceptance` Record projection are committed. The implementation checkpoint above remains the tested content anchor for report-only evidence reuse.
