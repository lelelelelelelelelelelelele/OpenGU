# Paper Liabilities Map — 2026-06-20

> Status: historical evidence snapshot (2026-06-20).
> 本文的数字、缺陷状态与论文行号只对应当时核查；用于当前稿件前需要重新核对。当前研究入口见 [OpenGU DocMap](../../../../OpenGU-DocMap/_文档地图.md)，任务安排见 [WORKPLAN](WORKPLAN.md)。

> One-page file/line map of claims the current disk does **not** cleanly support.
> Complements `paper-correctness-liabilities` memory and `self/dashboard/PROGRESS.md` §2.
> Target: the latest Overleaf draft (`report/paper/overleaf/`).

---

## Verified facts used below

- `results/_phase_b_aggregate.csv`: **460 rows**, all **4 hop-flip columns blank** (0/460).
- Global paired effect by strategy:
  `degree +1.85 > pagerank +1.53 > im +1.19 > hybrid +0.21 > tracin −0.31` (pp, mean over seeds).
- `GraphRevoker` `perf_before` mean = **0.548** (sd 0.047, n=75); all other methods 0.755–0.867.
- `results/baseline/k5_random/*/baseline_averaged_k5.json` has `f1_before=null` for **5/6 methods** (only `GNNDelete` populates it).
- GIF/IDEA `collateral.json` hop-flip rates are **bit-identical** in the returned data (L8 stale-bytecode signature).

---

| ID | Liability | File / Line(s) | Current claim | Why it is unsupported | Proposed fix | Priority |
|---|---|---|---|---|---|---|
| L1 | **Abstract still pitches IM/TracIn/Hybrid as the attack toolkit** | `sec/0_abstract.tex` ll. 10–12 | "The attacker chooses a small deletion set---using influence maximization, pseudo-influence functions, or their hybrid---to amplify approximation error." | Current data shows a free `degree` baseline (+1.85 pp) beats all of them except the α=0 endpoint; `tracin` is negative on average. The prose still reads as if the informed selectors are the contribution. | Rewrite abstract to: (a) list all six selectors including structural baselines, (b) state that **degree/PageRank dominate**, (c) frame IM/TracIn/Hybrid as tested but **objective-misaligned** signals. Keep "first systematic adversarial audit" if desired, but make the structural-leverage finding the headline. | P0 (pure prose) |
| L2 | **GNNDelete "largest collapse" lacks significance hedge in abstract** | `sec/0_abstract.tex` ll. 22–24 | "GNNDelete suffers the largest absolute collapse (≈13% average F1 across attack selectors, peaks above 23%), albeit with high seed variance" | Mean degree effect +6.02 pp with sd 7.34 (n=5, p≈0.07); IM p=0.21. "Albeit with high variance" is too weak; the effect is **not significant** at conventional levels. | Add "…but no single cell clears p<.05 at N=5 due to high seed-to-seed variance; the GNNDelete signal is therefore an unstable collapse mode rather than a reliably reproducible attack." | P0 |
| L3 | **Hop-decay section reports corrupted IF-family numbers as fact** | `sec/5_results.tex` ll. 332–337; `sec/A_appendix.tex` ll. 222–230 | "GIF and IDEA flips are sharply concentrated within the 1-hop receptive field (≈7% flip rate at h=1, <0.3% at h≥2); GNNDelete is far more diffuse…" | CSV hop columns are 100% null; the GIF/IDEA numbers are from L8-bugged data (computed against original model, not post-unlearn). GNNDelete/partition numbers may also be stale. | Insert a prominent caveat: "The IF-family hop-decay diagnostics in this section reflect the pre-fix unlearn state and are being regenerated after clearing stale server bytecode; the qualitative GNNDelete-vs-partition contrast is provisional." Or move the entire hop-decay quantitative discussion to a deferred/caveated paragraph. | P1 (needs env + re-run) |
| L4 | **Shard Protection ΔF_noise numbers lack a reproducible before-anchor** | `sec/4_experiment.tex` ll. 47–64; `sec/5_results.tex` Table `tab:benchmark` ll. 24–28, 51–67, and §`results-shard` ll. 260–294 | Partition pair ΔF_noise = −9.6 to −19.3 pp; non-partition pair stays near zero. | `f1_before` is null in 5/6 `k5_random` baseline JSONs. The headline "F1 rises 6–15%" is therefore not reproducible from disk. | Add footnote in Table `tab:benchmark`: "ΔF_noise is reported from the Phase B.1 k=5 random runs; the original-model F1 anchor was not persisted for all methods in these baseline files, so these values are provisional and will be regenerated with the anchor." Also soften "confirms" in §`results-shard` to "suggests, pending anchor completion". | P1 (re-run k=5 with anchor) |
| L5 | **GraphRevoker×GAT mechanism wedge rests on a broken baseline** | `sec/5_results.tex` Table `tab:benchmark` ll. 39–40, 54–55; §`results-alignment` ll. 198–217 | GraphRevoker×GAT is the lone negative-alignment cell where Hybrid/TracIn win; used as the "mechanism wedge" for objective-misalignment. | GraphRevoker `perf_before` = 0.500–0.583 across cells (other methods 0.77–0.87). The method is dispatching through a known-broken aggregator (`e3bbd54`, `opt_dataset.py:17`). Its attack effects are noise from a degenerate trained model, not a real exception. | **Decision needed**: (a) drop GraphRevoker from the main matrix and report 5 clean methods, removing §`results-alignment` wedge; or (b) keep it but add a strong caveat that GraphRevoker's trained-model F1 is anomalously low and the negative-correlation cell is likely an artifact. Recommend (a) for a resubmission. | P0/P1 (decision first) |
| L6 | **Citeseer is claimed but not run cleanly** | `sec/0_abstract.tex` l. 16; `sec/4_experiment.tex` ll. 5–8 | "We evaluate … across Cora, Citeseer, and ogbn-arxiv … with GCN/GAT backbones." | No clean Phase B data for Citeseer exists (only pre-2026-05-06 polluted archives). `experiments/configs/A5_citeseer_r0.05.yaml` exists but has not been executed. | Either (a) run `A5_citeseer_r0.05.yaml` (180 cells, ~1h once env is back) and keep the claim, or (b) rewrite scope to "Cora plus an ogbn-arxiv pilot" and move Citeseer to future work. The dormant resubmission option is preserved in `report/paper/RESUBMISSION_BLUEPRINT.md`. | P2 (env-blocked) |
| L7 | **ogbn-arxiv scope is overstated** | `sec/0_abstract.tex` ll. 16–17; `sec/4_experiment.tex` §`setup-arxiv` ll. 79–93 | "3 seeds … GCN/GAT … three selectors" implied full-ish scale check. | Arxiv is a **seed-42-only pilot**: 2 methods × 3 selectors, GCN only. Not in the aggregate CSV. | Change abstract to "ogbn-arxiv pilot (seed 42, GCN, two methods, three selectors)"; in §`setup-arxiv` explicitly state "we report a single-seed pilot as a qualitative sanity check, not a full Cartesian scale sweep." | P0 |
| L8 | **Appendix row-count typo** | `sec/A_appendix.tex` ll. 115–119 and ll. 143–146 | "460 rows" then later "92 rows, including the r=0.01 ablation …" | 92 is wrong; the CSV has 460 rows (360 cora GCN/GAT r0.05 + 90 r0.01 + 10 α=0). | Replace "92 rows" with "360 rows for the main r=0.05 matrix plus 90 r0.01 and 10 α=0 endpoint rows." | P0 |
| L9 | **Verdict labels may over-interpret null effects** | `sec/5_results.tex` Table `tab:benchmark` Verdict column | "Immune", "Structural", "Mild", "Unstable", "Uniform". | With only 5 seeds and many near-zero effects, "Immune" and "Uniform" imply stronger negative evidence than the data supports. | Keep labels but add a sentence in the Reading Guide: "Verdict labels are descriptive shorthand; they do not imply statistical proof of zero vulnerability." | P0 |

---

## Open decisions that block edits

1. **Resubmit vs rebuttal** (PROGRESS §4). If resubmit, all P0/P1 caveats can be applied now and the data fixed later; if rebuttal, we need the env rebuilt before answering reviewers.
2. **GraphRevoker keep/drop** (L5). Dropping it is the cleanest path; keeping it requires a large caveat that weakens §5.2.
3. **Citeseer scope** (L6). Decide before touching abstract/experiment setup.

---

## Suggested edit order (no env needed)

1. Fix L1, L2, L7, L8 in `sec/0_abstract.tex` and `sec/A_appendix.tex`.
2. Add L4 caveat footnote to Table `tab:benchmark` and soften §`results-shard` language.
3. Add L3 caveat in §`results-hop` and appendix hop-decay.
4. Decide L5 (GraphRevoker) and apply keep/drop accordingly.
5. Decide L6 (Citeseer) and adjust scope claims.

---

Last updated: 2026-06-20
