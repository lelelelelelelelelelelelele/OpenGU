# AAGU-009 · FIX · L8 Collateral Evidence

Block ID: `AAGU-009`

当前状态: `working / claimed`

> Apply target ref：`refs/heads/codex/e7-two-surrogate-groups-20260805`

Item Type: Block

## Orchestration contract

- Class: `FIX`
- Priority: `P0 / first repair`.
- Source anchor: legacy collateral-evidence redo Todo.
- Outcome: replace invalid or incomplete L8 collateral evidence through a separately accepted repair run.
- Fact owner: OpenGU DocMap rerun/cache-fix runbook; executable identity remains in the final registered recipe.
- Relations: no dependency on `AAGU-001` or `AAGU-002`; `AAGU-010` starts only after this Block's repaired evidence is explicitly accepted.

## Acceptance route proposal

- Route: `formal`.
- Primary surface: `research evidence repair`.
- Minimum evidence: corrected runtime identity, complete artifacts, regression checks, and explicit acceptance.
- Confirmation: user explicitly authorized starting AAGU-009 after correcting the spurious experiment-definition/device dependency.
- Report size: paired `REPORT.md` / `REPORT.html`, because the decision concerns formal research evidence and invalid historical outputs.

## Confirmed acceptance brief

### 当前基线

GIF/IDEA 的参数写回代码已经修复，但历史 120 个 Cora collateral cell 仍来自修复前语义；旧 helper 还会原地删除或覆盖结果，因此现有数字不能重新获得信任。

### 这次增量

冻结精确受影响范围，保留并隔离旧输出，在一个可复核的 clean full-SHA 运行身份下重新生成 GIF/IDEA collateral evidence，完成收集、完整性校验和单独接受。

### 完成后人会看到什么

GIF/IDEA × GCN/GAT × 6 strategies × 5 seeds 的 120 个修复后 collateral cell 具有完整、可追溯且不与旧污染结果混淆的证据，新结果可以被明确接受或拒绝。

### 验收项目

- 受影响范围严格限定为 120 个 IF-family collateral cell；Selection/Result cache 与其他 GU method 不被失效或改写。
- 历史完整 leaf 被可逆隔离且保持原样；新 active leaf 由 canonical runner 完整重建，不会把局部重算冒充为原运行身份。
- 隔离前后的 `attack.json.selected_nodes` 必须逐格相等（120/120），证明删除请求没有漂移。
- 120 个新 cell 的 runtime/config/Git 身份一致，产物完整可解析，collateral 与 hop-decay 字段通过回归和正式 gate。
- 收集后的 SHA-256、trusted index 与结果 read-back 一致；旧污染数字继续保持 invalid，直到本候选被明确接受。

### 主要证据

- 受影响范围与隔离清单：帮助判断旧证据是否被完整冻结且没有扩大破坏范围。
- 正式重跑与 gate 证据：帮助判断 120 个 cell 是否真正使用修复后 IF-family 状态生成。
- SyncMate 收集、校验与 trusted read-back：帮助判断本地接受面是否对应远端同一批产物。

### 关键 non-goals

- 不修改 selector、SelectionCache、attack 结果或其他 GU method；不在本 Block 修复 aggregate hop 列（由 AAGU-010 独立负责）。
- 不从修复后的数字提前形成论文机制结论，也不删除历史证据。

### 需要人的决定

结果尚未观测。完成 Verify 后由用户明确接受、返工或拒绝这批修复证据。

## Boundaries

- Do not mutate or delete historical artifacts. The only permitted runner-side action is the exact whole-leaf quarantine and no-`--force` rerun defined in `evidence/repair-scope.yaml`.
- Formal execution requires one clean full Git SHA, the registered runtime/config identity, at least one GPU, the intended interpreter, and complete collection/read-back; fail closed rather than falling back to CPU.
- AAGU-010, paper conclusions, selector changes, and unrelated result/cache repair remain outside this Block.

## Status history

- 2026-08-26: registered from the prominent collateral repair Todo.
- 2026-08-26: corrected the registration-time `AAGU-002 -> AAGU-009` projection error; the legacy E2 repair lane has no AAGU-001/AAGU-002 task dependency.
- 2026-08-26: claimed by the current Codex task after the user explicitly said to perform the AAGU-009 repair.
- 2026-08-26: local inventory confirmed the exact 120-leaf scope and retired the destructive partial-redo route. Formal preflight failed closed because the Apply target is not yet accepted into `main`, `.syncmate/device.yaml` is absent, the active SSH aliases refuse connection, and AAGU-004/AAGU-006 remain active.

## Claim and runtime record

- Stable locator: `.workblock/items/AAGU-009/WORKITEM.md`; this task owns only Block `AAGU-009`.
- Baseline: `6be95c74f230cbfcb6a99d0166ba8b1d143e5416` on `refs/heads/codex/e7-two-surrogate-groups-20260805`.
- Source branch/worktree: `codex/aagu-009-collateral-evidence` at `C:\Users\ADMIN\.codex\worktrees\aagu009\OpenGU\GULib-master`.
- Inherited state: accepted AAGU-018 is already on the Apply target. The existing IF-family write-back fix is inherited and must be re-proven against the formal runtime before rerun.
- Excluded state: the separate AAGU-006 candidate/worktree and AAGU-004 acceptance decision are not owned or modified here; AAGU-010 remains independently accepted follow-up work.
- Runtime profile: Git-backed local repair candidate plus formal SSH evidence execution. Tracked writes are limited to AAGU-009 orchestration/repair tooling, focused tests, this item package, and the user-authorized AAGU-010 priority projection.
- External boundary: the user authorized the AAGU-009 repair. No deletion, overwrite, CPU fallback, unrelated cache invalidation, push, Apply, or acceptance is authorized; remote result changes must be exact-scope and reversible.
- Candidate: pending; the clean source branch `HEAD` will become the candidate after implementation, evidence, Record, and Report converge.
- Evidence paths: `.workblock/items/AAGU-009/evidence/`, the formal run root selected by the repair profile, and verified SyncMate trusted outputs.
- Human surface: `.workblock/items/AAGU-009/REPORT.md` and `.workblock/items/AAGU-009/REPORT.html` after Verify.
- Policy: `.workblock/policy.json`; after explicit acceptance, closeout routes to remote `push` and skips install.
- Restart point: satisfy every precondition in `evidence/repair-scope.yaml`, then inventory and quarantine exactly 120 whole leaves and run the two canonical configs without `--force`. Start no GPU cell until every formal-run gate is observed.
