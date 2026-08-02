# Related Work — reading notes & positioning

> Citation library for the GNN-unlearning attack/audit thesis. BibTeX in `refs.bib`.
> Relevance order: **Chen 2022 (closest)** > Zhang 2026 (concurrent).

---

## ⭐ Chen et al. 2022 — *Characterizing the Influence of Graph Elements* `chen2022characterizing`

arXiv:2210.07441 · Brandeis · cs.LG · no venue listed.

**The most relevant prior work — the direct ancestor of the IF-based node-*selection* idea.**

- **What:** derives *exact* influence functions ($-H^{-1}\nabla\ell$) for **SGC** (chosen for convexity); selects high-influence nodes/edges, **removes them by EXACT retrain-from-scratch**, measures degradation.
- **Result:** IF-selection beats naive baselines hard. Cora, 10% node removal: Random 80.3 / Degree 78.7 / **IF 59.8**; "outperforms baseline >20% at 15% removal". Edge removal used as grey-box attack on GCN, and also to *improve* performance.
- **Why it's the real threat to my contribution:** it already shows "select high-influence nodes → big drop, beats degree/random."

**My surviving delta (this is the whole thesis):**
1. **Setting:** they remove by **exact retrain** on **convex SGC**. I study **approximate graph unlearning** (GIF/GNNDelete/MEGU/IDEA/... 16 methods). They touch **zero** unlearning algorithms.
2. **The contrast = the finding:** IF-selection's ~20pp advantage holds under exact-retrain/convex, but **vanishes/inverts under approximate unlearning** (IF/IM lose to degree → volume-driven, not architectural). Chen 2022 is the *foil* that makes my negative result meaningful, not a scoop.
3. **IF flavor:** they use exact $H^{-1}$ (rung-3); I use TracIn (rung-2, Hessian-free). ⚠️ Must align or explicitly acknowledge, else the contrast is confounded by "TracIn ≠ exact IF" rather than "unlearning regime."
4. They never touch unlearning robustness or MIA.

**Must-do experiment to lock the contribution:** 2×2 — does IF-selection beat degree under (a) exact retrain [replicate Chen] vs (b) approximate unlearning [my finding]? The gap between the two settings IS the paper.

---

## Zhang et al. 2026 — *Attack by Unlearning* `zhang2026attack` (brief)

arXiv:2603.18570 · Penn State · **unrefereed preprint, no venue, no code**.

- **What:** attacker **injects** 5% dirty-label nodes (bi-level optimized features/edges, surrogate + pseudo-labels), then requests their **deletion**; the approximate-unlearning step detonates the payload. Threat novelty = **dormant + non-refusable (RTBF) deletion channel**.
- **Key numbers:** dormant before deletion (Original ≈ NoAttack, e.g. Pubmed+GIF 0.8351 vs 0.8308), collapses after (→0.2443, ΔAcc 0.59). −59% at 5% is far outside the ordinary-poisoning envelope (~3–12pp at 5%) → genuinely unlearning-amplified, **not** reproducible by plain/random poisoning on the GIF cells.
- **But internally inconsistent:** under **GA** unlearning and **CEU-Pubmed**, *random* injection already collapses accuracy (GA-Cora Random −31.3% vs Optim −34.7%, only +3.4pp); optimization adds almost nothing. There the fragility is **method-intrinsic**, which the paper hides behind "consistently highest ΔAcc."

**Positioning (cite as CONCURRENT work, ~1 sentence):**
- Credit the dormant/non-refusable-channel novelty honestly (don't dismiss as "just poisoning" — the dormancy data refutes that and a referee will catch it).
- Distinguish: they **inject**; I **audit budget-matched selection of existing nodes** across the method family.
- **Turn it into my witness:** their GA/Random cells independently corroborate "collapse is method-intrinsic / volume-driven."
- My whitespace they omit: per-cell **ΔAcc decomposition = method-intrinsic floor (random-then-unlearn) + optimization margin** (my k=5-noise-floor methodology); plus no defense/detectability eval; gray-box-by-proxy ("black-box" is white-box on a surrogate trained on the same poisoned graph); transductive/node-only/2-layer-GCN/4 homophilous datasets only.

Draft RW sentence:
> Concurrent work [Zhang et al. 2026], an unrefereed preprint, weaponizes the non-refusable deletion channel via a bi-level *injected-node* poisoning attack. Our setting differs — we audit budget-matched *selection* of existing nodes across N approximate unlearning methods rather than craft injected payloads — and their own results corroborate our central finding that collapse is method-intrinsic: under gradient-ascent unlearning, random injection alone drives a ~31% accuracy drop, within ~3 points of their optimized attack.

⚠️ All Zhang numbers are from arXiv-v1 HTML extraction; re-verify against the PDF before quoting. Absolute injected-node counts are not reported.

---

## Queued to add (say the word — I have the metadata)
- Marchant, Rubinstein, Alfeld 2022, *Hard to Forget: Poisoning Attacks on Certified Machine Unlearning*, AAAI. (non-graph ancestor of Zhang)
- Chen et al. 2021, *When Machine Unlearning Jeopardizes Privacy*, CCS. (before/after-unlearning MIA — ancestor of the audit/MIA angle)

---

## Selection-concordance study (2026-06-27) → `concordance/report.html`

Training-free set-overlap (Jaccard@k) of selector outputs across 5 datasets (GCN, r=0.05).
- **IM ≠ degree** on every dataset (0.03–0.19, mean 0.10) — the "IM degenerates to degree" worry is **false at the set level** (single-node spread ~ degree, but the CELF *combination* diverges).
- **degree ≈ pagerank** but dataset-varying (0.50–0.83).
- **TracIn ⟂ degree & IM** (cora 0.02–0.03) → influence targets different nodes; degree wins anyway ⇒ volume-driven.
- **GIF-as-scorer（历史）**：早期 34%-acc GNNDelete checkpoint feasibility 结果已被 trained base-GCN diagnostic 取代；旧称 “proper TracIn” 的 single-final proxy 标签已经退役。见 [[related-work-zhang-chen-2026]]、`concordance/FINDING_tracin_misspecification.md` 和当前实验入口 `../../文档规划/10_实验矩阵/12_近似策略重合度实验.md`。
