# Handoff: 弄懂 IF、A/B/C 与 target loss 的关系

## Session Metadata
- Created: 2026-07-15 15:55:34
- Project: C:\Users\ADMIN\.codex\worktrees\if-target-comparison-plan\OpenGU\GULib-master
- Branch: codex/docs-if-target-comparison-plan-20260714
- Session duration: approximately 2 hours of guided discussion and document work

### Recent Commits (for context)
  - 3b53875 merge: integrate codex/citeseer-e1-graphrevoker-20260714 into main
  - 7232a60 merge: integrate codex/autoreport-v3-20260714 into codex/citeseer-e1-graphrevoker-20260714
  - a743a5a docs(reporting): document AutoReport V3 contract and acceptance
  - b78422d test(reporting): cover AutoReport V3 event flows
  - 0d5f7d6 feat(reporting): integrate AutoReport V3 runtime provenance

## Handoff Chain

- **Continues from**: None (fresh start)
- **Supersedes**: None

> This is the first handoff for this task.

## Current State Summary

The user is learning what influence functions mean in the OpenGU node-selection setting. The discussion has progressed from “IF 是否等于模型权重对样本权重的导数” to a three-level distinction: A = raw gradient magnitude, B = parameter-change IF, and C = effect on a chosen evaluation/query loss. The user agrees that C is usually the main target-aware attack objective, while B is a useful small comparison/appendix question. A plan-only A/B/C experiment document was created, but no experiment was implemented or run. The next session should return to slow conceptual teaching and exclude the distracting literature-ingestion and Obsidian-sync work from this session.

## Codebase Understanding

## Architecture Overview

For a candidate deletion node `v`, let `g_v = grad_theta loss_v`, and let `H` be the Hessian of the training objective near the trained parameters.

- A: `||g_v||` asks how large the candidate's raw training-loss push is.
- B: `||H^-1 g_v||` asks how far the model parameters are predicted to move after deleting/upweighting the candidate.
- C: `<g_v, H^-1 g_E>` (equivalently `<g_E, H^-1 g_v>` under the symmetry approximation) asks whether that parameter movement changes a chosen target loss `L_E` in the harmful direction.

`T` is the training/candidate pool. `E` is the evaluation/query set defining what “harm” means. In a formal attack selector, `E` should be a validation/query set, not the true test labels. Test may be used only for final evaluation; historical use of `test_mask` was mechanism calibration, not a deployable attack contract.

GIF/IF and TracIn are two approximation routes to C: final-point curvature versus training-trajectory gradient alignment. The old deployed TracIn uses the final-model direction `-sum_T g_j`, not `g_E`, so it answers a different question. Proposed TracIn V2 would use multiple checkpoints and explicit `E`, but it is currently contract/design only and has not been implemented.

## Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `E:/project/OpenGU/GULib-master/文档规划/20_研究框架/21_TracIn变体与GIF关系.md` | Main human-readable explanation of A/B/C, T/E, GIF, TracIn and legacy behavior | Primary teaching source; begin near the story at lines 14-156, then the A/B/C table around lines 232-260 |
| `C:/Users/ADMIN/.codex/worktrees/if-target-comparison-plan/OpenGU/GULib-master/文档规划/10_实验矩阵/20_IF目标层级对比实验计划.md` | Plan-only selector and small end-to-end comparison | Use only after the concepts are clear; do not implement without a new request |
| `E:/project/OpenGU/GULib-master/self/related_work/concordance/data/ifdiag_cora_GCN_r0.05_seed2024.json` | Historical Cora/GCN selector-overlap evidence | Supports the current numerical observations, not a general theorem |
| `E:/project/OpenGU/GULib-master/self/related_work/concordance/if_selector_diagnostic.py` | Selector-only diagnostic implementation | Read only if formulas or score names need verification |

## Key Patterns Discovered

- Keep the deletion candidate set `T` separate from the evaluation target `E`.
- Do not collapse IM, IF and Hybrid into a generic “proxy” story; state the concrete score each one uses.
- Distinguish a selector from an unlearning updater: the eval-target IF/GIF-inspired score selects nodes; OpenGU GIF is an updater after a deletion request is already known.
- State whether a TracIn-like score uses one final checkpoint or multiple checkpoints, and state its reference direction.
- Treat existing Cora numbers as a one-dataset, one-backbone, one-seed mechanism diagnostic.

## Work Completed

## Tasks Finished

- [x] Clarified that `d theta / d epsilon_v` is the parameter IF when `epsilon_v` is the infinitesimal sample-upweighting variable.
- [x] Separated the roles of training loss (`g_v`, `H`) and target/evaluation loss (`g_E`).
- [x] Established the A/B/C taxonomy and the user's current preference for C as the main attack objective.
- [x] Explained why validation/query `E` is reasonable when the true test set is unavailable.
- [x] Compared GIF/IF and TracIn as two routes to the same target-aware question C.
- [x] Recorded a plan-only 30-cell small experiment; no implementation or run was performed.
- [x] Added three prerequisite papers to the Learning-vault global reading ledger: No Change, No Gain; Witches' Brew; Expected Error Reduction.

## Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `文档规划/10_实验矩阵/20_IF目标层级对比实验计划.md` | Added literature-grounded A/B/C selector and end-to-end plan | Preserve the experiment idea without prematurely implementing it |
| `文档规划/10_实验矩阵/20_IF目标层级对比实验计划.html` | Static readable version of the same plan | Human-readable paired artifact |
| `.claude/handoffs/2026-07-15-155534-understand-if-abc-target-loss.md` | Captured conceptual learning state for a clean new session | Prevent literature/sync details from distracting the next discussion |
| `C:/Users/ADMIN/Documents/Obsidian/notes/Learning/10 Topics/研究阅读系统/00 全局论文阅读台账.md` | Added the three prerequisite papers and publication metadata | Durable reading queue; not the main topic of the next session |
| `C:/Users/ADMIN/Documents/Obsidian/notes/Learning/50 Outputs/HTML Format References/global_reading_ledger_REPORT.html` | Matching HTML update | Kept Markdown and browser view consistent |

## Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| C is the main target-aware attack objective | B parameter norm; C target-loss projection | A large parameter movement is not automatically harmful to the task; C names the target loss explicitly |
| Keep B as a mechanism comparison, potentially appendix-sized | Remove B; make B a second main method | B is conceptually important for A vs B curvature, but current Cora overlap with A is high |
| Formal selector uses validation/query `E` | Test labels; parameter norm only | The attacker does not know the true test set; validation/query data can define an observable target without test leakage |
| Do not implement the experiment yet | Run immediately; overlap-only conclusion | The user requested a small experiment plan only, and overlap alone is not an end-to-end attack result |
| Read three cross-domain prerequisites | Restrict reading to graph unlearning | They illuminate B→C and target-aware attack selection, while not replacing the A vs B experiment |

## Pending Work

## Immediate Next Steps

1. Resume at the user's exact conceptual question: “IF 和哪个 loss 有关系；`delta W / delta xi` 到底是哪一层定义？” Explain sample upweighting `epsilon_v`, training objective, and the first-order derivative slowly.
2. Ask the user to distinguish the two roles in one concrete toy example: which loss produces `H`/`g_v`, and which loss produces `g_E`? Use a two-parameter or one-dimensional model if helpful.
3. Only after that is stable, revisit A vs B, then B vs C, and finally connect IF/GIF to multi-checkpoint TracIn. Do not begin with the 30-cell experiment table.

## Blockers/Open Questions

- [ ] Does the user interpret `xi` as a per-example weight/upweighting variable, a feature, or the deletion indicator? Resolve notation explicitly before deriving formulas.
- [ ] What target set `E` is available in the eventual threat model: labeled validation nodes, pseudo-labeled probes, or another query set?
- [ ] Does parameter-change magnitude B ever add stable signal beyond A on more than the single historical Cora/GCN diagnostic?
- [ ] Does the proposed C-style selector increase actual unlearning attack damage, rather than only overlapping with the IF/GIF reference?

## Deferred Items

- Implementing or running the A/B/C experiment is deferred because the user explicitly asked for a plan only.
- TracIn V2 implementation and Cache V2 gates are deferred; the current topic is understanding the definitions.
- Detailed reading of the three prerequisite papers is deferred to later sessions; they are now registered in the reading ledger.

## Context for Resuming Agent

## Important Context

The user wants to *understand*, not receive a polished literature review or a large formula dump. Proceed slowly, one distinction at a time, and invite the user to restate the idea in their own words. Their current intuition is partially correct: IF can be seen as the derivative of trained parameters with respect to an infinitesimal sample-weight perturbation, but the loss role depends on which quantity is being measured. Training loss defines the local parameter response; a separate validation/query loss is required only for C-style target impact.

The user's current mental model is:

```text
A: the node pushes hard
B: the model actually moves far after curvature correction
C: that movement points toward harming the chosen target E
```

They already agree that C is the likely main method direction and B may remain a small comparison. Do not simply repeat this conclusion. The unresolved learning goal is to derive why it is true from `theta*(epsilon)` and the chain rule, including exactly where `H^-1`, `g_v`, and `g_E` come from.

Start the new conversation by summarizing the above in at most five lines and then teach the derivative definition. Keep literature administration, Obsidian sync, git workflow and experiment execution out of the foreground unless the user asks.

## Assumptions Made

- The task concerns node-level training-example deletion/upweighting near a trained local optimum.
- `H` is treated as invertible or suitably damped/approximated, and symmetric for the equivalent C formulas.
- A validation/query distribution is an acceptable observable surrogate for unknown test distribution when defining C.
- The historical diagnostic numbers are descriptive evidence only.

## Potential Gotchas

- Do not say IF is generically `delta W / delta xi` without defining `xi` as a sample-weight perturbation and specifying the optimized training objective.
- Do not say B is independent of loss: it depends on the training loss through both `g_v` and `H`; it is only independent of a separate target/evaluation loss.
- Do not call the final-checkpoint `<g_v,g_E>` score “proper TracInCP”; original TracInCP accumulates over checkpoints.
- Do not equate the eval-target IF/GIF-inspired selector with the full OpenGU GIF unlearning algorithm.
- Do not use test labels for formal attack selection.
- Do not treat high A/B overlap (`0.8462`) as conceptual equivalence or low B/C overlap (`0.2343`) as an end-to-end damage result.

## Environment State

### Tools/Services Used

- Local filesystem/document inspection only is sufficient for the next conceptual session.
- Formal experiments belong on the approved remote GPU path; no experiment is currently authorized.

### Active Processes

- None.

### Environment Variables

- None required.

## Related Resources

- Main framework note: `E:/project/OpenGU/GULib-master/文档规划/20_研究框架/21_TracIn变体与GIF关系.md`
- Plan-only experiment note: `C:/Users/ADMIN/.codex/worktrees/if-target-comparison-plan/OpenGU/GULib-master/文档规划/10_实验矩阵/20_IF目标层级对比实验计划.md`
- Koh & Liang influence functions: https://proceedings.mlr.press/v70/koh17a.html
- TracIn: https://proceedings.neurips.cc/paper/2020/hash/e6385d39ec9394f2f3a354d9d2b88eec-Abstract.html
- No Change, No Gain: https://proceedings.neurips.cc/paper_files/paper/2023/hash/944ecf65a46feb578a43abfd5cddd960-Abstract-Conference.html
- Witches' Brew: https://iclr.cc/virtual/2021/poster/2561
- Expected Error Reduction: https://groups.csail.mit.edu/rrg/papers/icml01.pdf

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
