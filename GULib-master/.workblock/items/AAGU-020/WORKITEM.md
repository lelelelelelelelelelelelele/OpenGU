# AAGU-020 · D-full GIF 计算原语与计时应用

Block ID: `AAGU-020`

Item Version: 2.1

当前状态: `registered / not claimed`

Item Type: Block

## Human Surface

### 核心意图

把 D-full GIF 的候选评分成本从完整 Selector 的多分数准备、排序和缓存流程中分离出来，得到可复用、可验证的评分原语，为后续小图计时验证和大图容量探针建立同一条可信测量路径。

### 本次增量

从现有 Selector 内部提取唯一的 D-full GIF 评分原语与小型计时应用；输入一个或多个有序 candidate node IDs，输出同序的有限 `gt_full` 分数，并分别记录共享准备与候选计算 wall time。生产 Selector 改为复用同一原语，不保留第二套公式实现，也不改变 affected-source、全图消息传递、IHVP、目标集、参数范围或节点删除语义。

### 核心验收

- 单候选和多候选输入都返回同序、有限的 D-full GIF 分数，并在固定上下文中与现有 Selector 的 `gt_full` 结果满足明确数值容差。
- 共享准备和候选计算分别计时，设备同步边界正确；生产 Selector 只消费这一条 D-full GIF 公式路径。
- 计时应用不进入排序、Top-k、Selection Artifact、GU、Retrain 或 Metrics；用户查看短验证说明后再决定接受，测试通过不会自动接受本 Block。

## Source

- Anchor: `experiments/c_target_v1/core.py::graph_source_scores` and the `gt_full` path consumed by `experiments/target_direct_v1/run_selection.py`.
- Scientific contract: D-full GIF uses `D(v;E) = <grad1_v - grad2_v, H^-1 g_E>` under the current corrected affected-training-source semantics.
- Baseline: the existing Selector computes D-full GIF inside a complete multi-score ScoreBundle and then ranks all candidates; it does not expose a focused timing application for an arbitrary candidate subset.

## Scope

- Preserve the current D-full GIF formula, affected-source, full-graph message-passing, IHVP, target-set, parameter-scope, and node-deletion semantics.
- Expose shared D-full GIF context preparation separately from scoring a non-empty ordered candidate-ID batch.
- Support both one-candidate and multi-candidate calls and preserve input ID to output score order.
- Synchronize the active device at timing boundaries so recorded CPU/GPU wall times represent completed work.
- Emit structured candidate IDs, finite `gt_full` scores, shared-preparation time, and candidate-compute time.
- Refactor the current Selector to call the extracted primitive as the sole D-full GIF implementation.
- Add focused contract and regression coverage proportional to this extraction.

## Non-goals

- Do not rank candidates, select Top-k nodes, or create a Selection Artifact.
- Do not expose `p_graph`, `r_point`, TracIn, or other score families through this timing application.
- Do not run or fit the small-graph timing experiment; that is a separate dependent Block.
- Do not run a large-graph probe, SSH job, or formal GPU experiment; that is a later dependent Block.
- Do not run graph unlearning, exact retraining, Metrics, or change their data flow.
- Do not change D-full GIF scientific semantics or add a compatibility fallback or duplicate scoring implementation.

## Acceptance contract

- Route: `direct`.
- Primary surface: IF scoring contract.
- Decision owner: human user after reviewing the short verification note; successful tests alone do not accept the Block.
- Report size: short verification note in this WorkItem; no Markdown/HTML report pair.

### Acceptance items

- The application accepts one or more candidate IDs and returns one ordered finite D-full GIF score per candidate.
- For the same candidate IDs and fixed context, the extracted primitive agrees with the existing Selector's `gt_full` result within an explicit numerical tolerance.
- Shared preparation and candidate computation are separately timed with correct device synchronization.
- The production Selector consumes the extracted primitive, leaving one D-full GIF formula path.
- No ranking, Selection, GU, Retrain, or Metrics path is entered by the timing application.

### Minimum evidence

- Focused one-candidate and multi-candidate contract evidence, including ID-score order and finite outputs.
- Before/after numerical equivalence evidence for a fixed candidate subset and fixed D-full GIF context.
- Structured timing-output evidence showing separate shared and candidate phases and proving the timing lane does not invoke downstream selection or unlearning work.

## Context and relations

- Blueprint scope: D-GIF graph-source scoring and the preparation boundary for later large-graph scalability probes.
- Confirmed Block relations: none.
- The future small-graph timing Block and large-graph probe Block are not registered here; each must receive its own identity and declare the appropriate dependency when registered.
- `AAGU-015` is not promoted, modified, or related by this registration.

## Registration and execution boundary

- Project config: `.workblock/project.json`.
- Previewed config digest: `83bd45c406abae135c83968331f6e5bc7b66dce8327a784c6ae933676273c705`.
- Registration confirmation: the user explicitly confirmed registration on 2026-08-27 after reviewing the acceptance contract and complete preview.
- Registration creates this Record and advances the project WorkItem counter only.
- A later user-visible Codex task must use `block-workflow`, claim this same stable locator, and implement within this Record.

## Status history

- 2026-08-27: registered from the confirmed D-full GIF primitive and timing-application preview; ready for a separate execution task to claim.
