# Paper Library Synthesis (Top-Conference Reviewer Mode)

Scope: this document is grounded in the materials already in this repo:
- Metadata: `papers/papers.csv`
- Rough cards: `papers/notes/*.md` (abstract-level; sometimes generic)
- Full text evidence (searchable): `papers/raw/text/*.txt` extracted from local PDFs via `papers/extract_pdf_text.py`
- Evidence links: arXiv / Semantic Scholar / Crossref in `papers/papers.csv` and rough cards

Hard constraint honored:
- I do **not** inject paper details that are not supported by the above sources. When unclear from PDF text extraction, I label it as **unknown / needs verification**.

Date anchor:
- “recent two years” relative to **2026-02-16** (priority window 2024-02-16 to 2026-02-16)

---

## 1) Structured Survey (3–5 Threads, Not Chronological)

### Thread A: Partition / Sharding + Partial Retraining (Exact-ish by Construction)
Core question:
- How to get **fast unlearning** without full retraining, while avoiding **utility collapse** caused by partition edge cuts / semantic imbalance / weak sub-model aggregation.

Representative papers:
- GraphRevoker: `2403.07353`
- CGE / GSMU: `2408.09705`
- Benchmark context: `2501.02728` (OpenGU taxonomy)

Common evaluation paradigm:
- Utility: F1/Accuracy on retained data (node classification) and/or link prediction.
- Efficiency: deployment time + unlearning time; or total retraining time vs “Retrain from scratch”.
- Stressors: dataset scale differences, deletion ratio/intensity.

Largest blind spots:
- “Exactness” is usually **conditional**: partitioning drops inter-shard edges; retrain baselines are not always standardized under the same information scope.
- Robustness to **adversarial deletion selection** is under-specified (often random deletions).

How it feeds your attack design:
- Use these as “harder-to-break” comparison class: if approximate GU collapses but sharding-based retraining holds, that supports “attack exploits approximation brittleness, not just removing important nodes”.

---

### Thread B: Certified GU Meets Scalability (Approximation Error as Bottleneck)
Core question:
- Can we **scale certified unlearning** to large graphs without violating certification conditions, given scalable propagation introduces approximation error?

Representative papers:
- ScaleGUN: `2408.09212`
- Benchmark context: `2501.02728`

Common evaluation paradigm:
- Utility vs (ε, δ) guarantee vs runtime (embedding update cost + total unlearning time), with certified baselines (CGU/CEU as named in text).

Largest blind spots:
- Certification is practically demonstrated for **specific model classes**; deep models remain outside certification scope.

How it feeds your attack design:
- Provides a clean baseline: either certification resists your attack (important) or you show your setting is outside its scope (also publishable if stated precisely).

---

### Thread C: Influence / Edit-Sensitivity / Approximate Updates
Core question:
- How to update under deletions/edits quickly, and how to reason about collateral effects (over-forgetting, propagation change, approximation brittleness).

Representative papers:
- UtU: `2402.10695`
- Edge-edit influence: `2506.04694`
- SGU / NIM: `2501.11823`

Common evaluation paradigm:
- Downstream utility (AUC/F1/Acc) + additional stability signals (over-forgetting; predicted-vs-actual influence; MIA AUC).

Largest blind spot:
- Many methods assume “reasonable” deletion requests; targeted deletions can amplify design/approximation flaws.

---

### Thread D: Auditing and Attacks (GU as Attack Surface)
Core question:
- How attackers exploit GU outputs/procedures (privacy leakage, reconstruction, auditing).

Representative papers:
- GraphToxin: `2511.10936`
- MGP-MIA: `2511.17989`

Common evaluation paradigm:
- Attack metrics (ACC/F1 for MIA; reconstruction + performance-level metrics; white-box vs black-box).

Key takeaway for your work:
- MIA alone can be insufficient; threat models must be explicit and multi-metric.

---

### Thread E (Lens): Benchmarks + Sequential Forgetting
Representative papers:
- OpenGU: `2501.02728`
- Continual forgetting lens: `2505.10040`

Key takeaway:
- Your project is sequence/strategy driven (choose D_unlearn, possibly multi-round). Continual-learning-style forgetting metrics can make “collapse” claims more measurable.

---

## 1.5) Paper-Writing Kit (Related Work + Positioning + Experiments)

### Related Work Structure (drop-in outline)
- **RW1 Retraining/Partition-based GU**: partial retraining via sharding and aggregation; key challenge is utility loss from edge cuts and weak submodels. Use `2403.07353`, `2408.09705` as representatives; cite OpenGU taxonomy `2501.02728` for categorization.
- **RW2 Certified GU at scale**: certified guarantees vs scalability; approximation error as a certification bottleneck. Use `2408.09212` as the core anchor; optionally mention OpenGU’s certified-family summary `2501.02728`.
- **RW3 Influence/Approximate updates and collateral effects**: influence-based selection/updates and collateral damage (over-forgetting) under graph propagation. Use `2402.10695`, `2501.11823`, and `2506.04694` (as an influence primitive).
- **RW4 Auditing and attacks on GU**: GU introduces attack surfaces beyond standard MIA; consider reconstruction and auditing pipelines that weaponize unlearning. Use `2511.10936`, `2511.17989`.
- **RW5 Benchmarks and sequential forgetting lens**: standardized evaluation axes (utility/privacy/efficiency/robustness) and multi-round forgetting dynamics. Use `2501.02728` and the forgetting-metric lens from `2505.10040`.

### Positioning Sentence Bank (academic English templates)
- “Unlike prior work that designs unlearning algorithms to improve efficiency or certification (e.g., `2403.07353`, `2408.09212`, `2408.09705`, `2501.11823`), we treat **deletion requests as an attack surface** and study adversarial selection of the unlearning set.”
- “In contrast to reconstruction-centric attacks on GU (e.g., `2511.10936`), our objective is to **maximize collateral utility collapse** on retained data under a fixed deletion budget, and to attribute the collapse to approximation-induced brittleness via retrain-after-deletion controls.”
- “We build on OpenGU’s unified evaluation axes (`2501.02728`) and extend it with **adversarial request generators** to stress-test GU methods under worst-case deletions.”
- “Motivated by over-forgetting analyses in edge unlearning (`2402.10695`), we quantify and optimize collateral damage under adversarial deletions across request types.”
- “Our attack leverages influence primitives (e.g., influence maximization in `2501.11823` and propagation-aware influence estimation in `2506.04694`) but repurposes them to generate worst-case unlearning requests rather than to improve unlearning.”
- “We show that unlearning can be weaponized for privacy compromise (cf. unlearning-amplified auditing in `2511.17989`), highlighting the need for threat-model-aligned GU evaluation beyond standard MIA metrics.”

### Experiment Checklist (minimum set to clear a top-tier bar)
- **Threat model**: who chooses deletions; whether deletions must be “self-owned”; model access (white/gray/black-box); what the attacker observes (before/after outputs, gradients, logs).
- **Attack strategies**: Random/Degree/PageRank; SGU-style NIM/HIE (`2501.11823`); proxy-IF/TracIn variants (your plan); worst-case heuristics inspired by `2511.10936`.
- **Targets (GU methods)**: at least one retraining/partition-based (`2403.07353`-style), one certified/IF-based (`2408.09212`-style if applicable), one learning-based/heuristic family (OpenGU taxonomy `2501.02728`).
- **Datasets**: start with Cora/Citeseer/PubMed (appearing across multiple papers), then add one large-scale graph if feasible (ogbn-arxiv is repeatedly used in `2408.09212`/`2501.11823`/`2501.02728`).
- **Metrics**: utility (Acc/F1/AUC as task requires); completeness (MIA AUC where applicable); efficiency (selection time + unlearning time + memory); collateral damage (UtU-style over-forgetting when applicable); approximation gap (Unlearn vs Retrain-after-deletion).
- **Ablations**: IF vs IM vs Hybrid; fusion type (linear vs rank); α/β sweep; deletion budget K; deletion ratio; stability across seeds/runs; boundary-node vs core-node deletions (for mapping/sharding methods).
- **Core tables/figures**: (1) attack success vs deletion budget, (2) approximation gap vs deletion budget, (3) cross-family robustness summary, (4) efficiency vs attack strength trade-off, (5) sequential deletion curves (optional but strong).

## 2) Per-Paper “Writeable-Grade” Extraction (11 papers)

Notation:
- Evidence (local): PDF in `papers/` and extracted text in `papers/raw/text/`.
- Evidence (links): arXiv + S2 + Crossref links in `papers/papers.csv`.

### 2402.10695 — Unlink to Unlearn: Simplifying Edge Unlearning in GNNs
Evidence:
- PDF: `papers/2402.10695_unlink_to_unlearn_simplifying_edge_unlearning_in_gnns.pdf`
- Text: `papers/raw/text/2402.10695.txt`
- arXiv: https://arxiv.org/abs/2402.10695

Card correction (rough card issues):
- The rough claim is a generic opener; the technical core is **diagnosing over-forgetting in GNNDelete and removing DEC/NI losses**.
- The evaluation is explicit in the PDF text: link prediction ROC-AUC, MI attack AUC, and an over-forgetting indicator Δp.

Claim (precise rewrite):
- Over-forgetting in edge unlearning is caused by specific loss designs in GNNDelete (DEC/NI), and a minimalist method (UtU) can avoid it by performing unlearning through **inference-time unlinking** on the retained graph.

Novelty (relative to who, based on the paper text):
- Relative to GNNDelete: mechanistic diagnosis linking DEC/NI to over-forgetting and a simplified redesign.
- Relative to baselines listed (Retrain / Gradient Ascent / GIF): “nearly zero-cost” inference-time structural change as an edge-unlearning solution.

Methods (mechanism):
- The paper defines over-forgetting as collateral degradation on retained edges after unlearning, measured by a retained-edge probability drop averaged as Δp_r. It analyzes GNNDelete’s DEC loss as matching forget edges to random node pairs, injecting structural noise that propagates via message passing, and NI loss as regularizing toward original embeddings that still encode forgotten-edge influence.
- UtU removes DEC and then NI, and performs edge unlearning by removing the forgotten edges from the graph used at inference (run the original parameters on the retained graph G_r). The paper argues this blocks message propagation paths from forgotten edges during inference.

Overstatement check:
- The paper argues “unlinking at inference suffices to eliminate an edge’s influence” under a message-passing view; however, parameters are unchanged, so this is a **prediction/inference** notion of influence rather than a universal guarantee of “training-data removal” in all senses.

GU connection:
- Directly targets GU for **edge unlearning** and introduces “over-forgetting” as an operational collateral-damage concept you can reuse as an attack objective/metric.

What I can borrow (method/eval/baselines):
- Method: loss-term diagnosis (“loss-term surgery”) + separating parameter update from propagation change.
- Eval: include explicit collateral damage metrics (Δp_r) plus MI attack AUC; always compare to retrain.
- Baselines: Retrain, Gradient Ascent, GIF, GNNDelete, and ablated GNNDelete variants.

What I should not borrow:
- UtU is specific to **edge unlearning** (link prediction protocol). Do not present it as general node/feature unlearning.

Related-work sentence (English):
- “Tan et al. analyze over-forgetting in edge unlearning and propose UtU, a minimalist inference-time unlinking strategy that avoids loss-induced collateral degradation observed in GNNDelete.”

---

### 2403.07353 — Graph Unlearning with Efficient Partial Retraining (GraphRevoker)
Evidence:
- PDF: `papers/2403.07353_graph_unlearning_with_efficient_partial_retraining.pdf`
- Text: `papers/raw/text/2403.07353.txt`
- arXiv: https://arxiv.org/abs/2403.07353

Card correction:
- The rough card’s claim is generic; the paper’s method is **GraphRevoker**.
- This is **retraining-based** (SISA-style sharding + partial retraining), not IF-based unlearning.

Claim (precise rewrite):
- GraphRevoker improves retraining-based GU by learning graph partitions that optimize expected retraining time while preserving structure/label semantics, and by using a contrastive-learning-based aggregator to better fuse sub-model outputs.

Novelty:
- Relative to SISA/GraphEraser (explicitly discussed): graph-specific sharding objectives (time + normalized cut + label-entropy) and a local-global contrastive aggregation mechanism.

Methods (mechanism):
- GraphRevoker follows SISA: partition into disjoint shards, train isolated sub-models, and partially retrain the affected sub-models under deletion requests. It defines three partition objectives: expected retraining time (cost proxy via shard node/edge counts), structure preservation via normalized edge-cut, and label semantic preservation via entropy of label distribution.
- For aggregation, it aligns sub-model embeddings with learnable projections, fuses via attention, and trains a small aggregator using an InfoNCE-style local-global contrastive objective where the global fused embedding is contrasted with a randomly masked fusion (local view).

Overstatement check:
- The paper frames the goal as “efficient and exact unlearning capability” within a SISA-style framework; in practice, correctness depends on the partitioning protocol (edge cuts) and how retrain-after-deletion is defined under the same information scope.

GU connection:
- Provides a strong retraining-based baseline family: useful to show your attack targets **approximate** GU brittleness rather than “importance removal” (if retraining-based methods resist under the same deletion budget).

What I can borrow (method/eval/baselines):
- Method: objective decomposition for sharding; attention + contrastive aggregation as a concrete utility-recovery mechanism.
- Eval: report unlearning time and utility across multiple backbones/datasets.
- Baselines: Retrain, SISA, GraphEraser; ablate partition terms and aggregation.

What I should not borrow:
- Avoid claiming “partial retraining implies exact unlearning” without matching the retrain protocol to the same information scope (partition drops edges).

Related-work sentence (English):
- “Zhang et al. propose GraphRevoker, a SISA-style retraining-based graph unlearning framework with graph-property-aware sharding objectives and a contrastive attention aggregator to recover utility under partial retraining.”

---

### 2408.09212 — Scalable and Certifiable Graph Unlearning: Overcoming the Approximation Error Barrier (ScaleGUN)
Evidence:
- PDF: `papers/2408.09212_scalable_and_certifiable_graph_unlearning_overcoming_the_approxi.pdf`
- Text: `papers/raw/text/2408.09212.txt`
- arXiv: https://arxiv.org/abs/2408.09212

Card correction:
- The rough card implies attack-based auditing; the paper’s core evidence is **(ε, δ)-certified unlearning** with scalability analysis.

Claim (precise rewrite):
- ScaleGUN integrates approximate propagation into certified graph unlearning and shows (theoretically and empirically) that approximation error can be bounded so certification is preserved, enabling scalable certified node/edge/feature unlearning.

Novelty:
- Relative to certified baselines named in text (CGU/CEU): explicit analysis of approximation error’s impact on certified guarantees, and a lazy local propagation framework for generalized PageRank/propagation schemes.

Methods (mechanism):
- The paper identifies a discrepancy: scalable propagation uses approximate embeddings ˆZ while certification requires bounding model error on exact D′. It derives bounds showing approximation error only marginally increases model error and can be masked by noise perturbation, preserving certification for node feature/edge/node unlearning.
- It implements scalable updates via a lazy local propagation framework (Forward Push / residue-reserve style) extended from dynamic PPR to generalized propagation schemes used in certified GU backbones.

Overstatement check:
- “Certified” and “scalable” claims are scoped to the paper’s certification definition, assumptions, and target backbone class; do not generalize robustness to deep GNN unlearning settings without explicitly matching conditions.

GU connection:
- Serves as a principled baseline for the certified regime and introduces an explicit approximation-error knob (e.g., rmax) that can be studied as a brittleness boundary or a defensive control.

What I can borrow (method/eval/baselines):
- Method: “approximation error budget” framing (e.g., rmax as a knob) for arguing brittleness boundaries.
- Eval: certified setting trade-offs among utility, runtime, and privacy parameters; small-to-large graphs.
- Baselines: certified methods and scalable propagation baselines named in the paper.

What I should not borrow:
- Don’t generalize certification claims to deep GNNs; keep scope aligned with the paper’s model class/assumptions.

Related-work sentence (English):
- “Yi and Wei introduce ScaleGUN, which couples lazy local propagation with certified graph unlearning by bounding approximation-induced model error, enabling scalable (ε, δ)-certified removals on large graphs.”

---

### 2408.09705 — Community-Centric Graph Unlearning (GSMU + CGE)
Evidence:
- PDF: `papers/2408.09705_community_centric_graph_unlearning.pdf`
- Text: `papers/raw/text/2408.09705.txt`
- arXiv: https://arxiv.org/abs/2408.09705

Card correction:
- The rough card misses the paradigm name GSMU and the mapping mechanism (community → node).
- The paper explicitly positions itself under deterministic GU and critiques BP-SM-TA style frameworks.

Claim (precise rewrite):
- The paper proposes Graph Structure Mapping Unlearning (GSMU) and CGE, mapping community subgraphs to nodes to reconstruct node-level unlearning on a reduced mapped graph, reducing training/unlearning computation while preserving utility.

Novelty:
- Relative to BP-SM-TA baselines discussed (GraphEraser/Guide): “structure mapping” that preserves inter-community relations and reduces redundant submodel/unlearning parameter computation.

Methods (mechanism):
- CGE runs community detection, then maps G → Ĝ where communities become mapped nodes; node/feature/label mapping plus edge mapping define the reduced graph. The goal is to keep structural relations between subgraphs that balanced partitioning destroys.
- On node unlearning requests, it identifies affected communities and updates only the corresponding mapped nodes, reporting efficiency split into deployment vs unlearning stages; it evaluates unlearning ability using MIA AUC (AUC≈0.5 as random guessing).

Overstatement check:
- The paper claims “exponential reduction” of training data and unlearning parameters via mapping; treat this as an empirical claim tied to community detection/mapping choices and verify sensitivity to boundary cases (community overlaps, instability).

GU connection:
- A deterministic-style GU mechanism whose vulnerability/robustness can be probed by choosing UE that spans many communities or lies near community boundaries, aligning with your adversarial deletion selection theme.

What I can borrow (method/eval/baselines):
- Method: reduce-and-map as a concrete scalability mechanism; test boundary-node deletions to stress this mapping.
- Eval: report deployment vs unlearning time; include MIA AUC + utility.
- Baselines: SISA, GraphEraser, GUIDE, retrain.

What I should not borrow:
- Assuming community detection is stable. In adversarial deletion selection, boundary/community-spanning UE may maximize damage.

Related-work sentence (English):
- “Li et al. propose GSMU and CGE, mapping community subgraphs into a reduced graph to enable efficient deterministic node unlearning with improved deployment/unlearning time trade-offs over BP-SM-TA baselines.”

---

### 2501.02728 — OpenGU: A Comprehensive Benchmark for Graph Unlearning
Evidence:
- PDF: `papers/2501.02728_opengu_a_comprehensive_benchmark_for_graph_unlearning.pdf`
- Text: `papers/raw/text/2501.02728.txt`
- arXiv: https://arxiv.org/abs/2501.02728

Card correction:
- The rough card is too vague. OpenGU explicitly defines request types, downstream tasks, algorithm families, attacks, metrics, datasets, plus complexity/robustness axes.

Claim (precise rewrite):
- OpenGU standardizes GU evaluation across a 3×3 combination of unlearning requests (node/edge/feature) and downstream tasks, integrates utility + privacy attacks (MIA/poisoning) + efficiency profiling, and reports a large-scale empirical study revealing inconsistent practices and open problems.

Novelty:
- Infrastructure + methodology: unified APIs, unified metrics, cross-request/task comparability, and systematic stress tests.

Methods (mechanism):
- It formalizes GU as updating a trained model under ΔG = {ΔV, ΔE, ΔX}, provides a taxonomy of GU methods (partition-based, IF-based, learning-based, plus direct/projection-style), and defines a metric suite including predictive metrics, MIA AUC-ROC (AUC close to 0.5 as effective unlearning), poisoning attacks, and time/memory/storage.

Overstatement check:
- OpenGU is broad, but “comprehensive” does not automatically imply threat-model coverage: adversarial deletion selection and reconstruction-centric attacks require explicit extensions if they are core to your paper’s claim.

GU connection:
- This is your best “evaluation scaffold”: use its taxonomy/metrics/dataset suite as the default, and clearly state what you extend (adversarial request generation; sequential deletions; additional leakage metrics).

What I can borrow (method/eval/baselines):
- Method: the taxonomy + unified APIs as the organizing backbone of your paper.
- Eval: the metric triad (utility + privacy attack + efficiency) and robustness stressors (deletion intensity, noise/sparsity, scaling).
- Baselines: cross-family comparisons (partition-based vs IF-based vs learning-based) under matched request/task settings.

What I should not borrow:
- Don’t overclaim “benchmark already covers adversarial deletions”. You still need adversarial request generators (see Gap 1).

Related-work sentence (English):
- “Fan et al. introduce OpenGU, a comprehensive benchmark that standardizes graph unlearning across request/task combinations and evaluates algorithms under utility, privacy attacks (e.g., MIA), robustness stressors, and efficiency constraints.”

---

### 2501.11823 — Toward Scalable Graph Unlearning: A Node Influence Maximization based Approach (NIM + SGU)
Evidence:
- PDF: `papers/2501.11823_toward_scalable_graph_unlearning_a_node_influence_maximization_b.pdf`
- Text: `papers/raw/text/2501.11823.txt`
- arXiv: https://arxiv.org/abs/2501.11823

Card correction:
- The rough card under-specifies the evaluation and baselines. The paper reports a broad baseline suite and a two-part evaluation: Model Update (Edge Attack + MIA) and Inference Protection (Non-UE F1).
- The technical core is the UE/HIE/Non-UE decomposition + NIM for reliable HIE selection + SGU lightweight fine-tuning.

Claim (precise rewrite):
- The paper bridges graph unlearning with social influence maximization by proposing Node Influence Maximization (NIM) to identify high-influenced entities (HIE) activated by unlearning entities (UE), and proposes SGU, a scalable fine-tuning framework that leverages UE/HIE/Non-UE-specific objectives (with prototype/contrastive components) to balance forgetting capability and reasoning capability at scale.

Novelty:
- Reliable HIE selection framed as an influence maximization problem (UE as seed set; HIE as activated set) using a decoupled influence propagation model + a fine-grained influence function (topology + feature influence).
- A lightweight GU framework (SGU) built around entity-specific fine-tuning rather than full retraining, evaluated across diverse request types and backbones.

Methods (mechanism):
- The paper formalizes GU requests as ΔG = {ΔV, ΔE, ΔX} and distinguishes UE (entities to be unlearned), Non-UE, and HIE (entities influenced by UE gradients but hidden in Non-UE). It argues that naive neighborhood-based HIE selection can hinder complete UE knowledge removal under message passing.
- NIM treats UE as a seed set and selects HIE as the activated set under an influence propagation model; it leverages a decoupled propagation view and a fine-grained influence function combining topology and feature influence, with threshold/budget controls. SGU then performs lightweight entity-specific fine-tuning (prototype/contrastive elements are used in its objectives) and is evaluated via Model Update (Edge Attack + MIA AUC; higher AUC indicates more leakage) and Inference Protection (Non-UE F1).

Overstatement check:
- “High influence” is defined by the paper’s influence model and HIE selection; it should not be taken as a universal proxy for “maximal damage” without validation (especially outside the paper’s backbone/setting choices).

GU connection:
- NIM is directly relevant to your project’s “adversarial deletion selection” axis: it is a strong IM-style selector to include as a baseline attacker (or as a component to outperform), and it provides a clean influenced-set abstraction (HIE) that you can reuse for region-based collapse analysis.

What I can borrow (method/eval/baselines):
- Method: UE/HIE/Non-UE decomposition and NIM’s budget/threshold knobs as explicit “influenced-set size” controls.
- Eval: report both forgetting (MIA; Edge Attack) and retained utility (Non-UE F1), and track OOT cases where unlearning exceeds retrain runtime.
- Baselines: the paper’s cross-family suite (e.g., GraphEditor, GUIDE, GraphRevoker, CGU, CEU, GIF, D2DGN, GNNDelete, UtU, MEGU, ScaleGUN) provides ready-made anchors for “attack across GU families”.

What I should not borrow:
- SGU is designed for *better unlearning*, not *max damage*. You must empirically show the alignment (or mismatch) between “high influence” and “maximal collapse” under approximate GU.

Related-work sentence (English):
- “Li et al. bridge graph unlearning with influence maximization by proposing NIM to select highly influenced entities (HIE) activated by unlearning entities and introduce SGU, a scalable entity-specific fine-tuning framework that balances forgetting and reasoning.”

---

### 2506.04694 — Influence Functions for Edge Edits in Non-Convex Graph Neural Networks
Evidence:
- PDF: `papers/2506.04694_influence_functions_for_edge_edits_in_non_convex_graph_neural_ne.pdf`
- Text: `papers/raw/text/2506.04694.txt`
- arXiv: https://arxiv.org/abs/2506.04694

Card correction:
- This is not a GU algorithm paper; it provides a propagation-aware influence estimator for edge insertions/deletions under non-convex GNNs.

Claim (precise rewrite):
- The paper derives influence functions for edge insertions/deletions in non-convex GNNs using a proximal Bregman response function that relaxes convexity assumptions and explicitly models message propagation changes, enabling accurate impact prediction without retraining.

Novelty:
- Influence prediction under edge deletions and insertions for non-convex GNNs via a proximal Bregman response function (weaker assumptions than convex IF), explicitly decomposing parameter shift and message propagation effects.

Methods (mechanism):
- The paper defines edge edits (deletions/insertions) as perturbations that change both (i) model parameters after re-optimization and (ii) the message propagation paths that determine intermediate representations. It derives an influence estimator that combines a parameter-shift term derived from a proximal Bregman response function with an explicit message-propagation term.
- It validates the estimator by comparing predicted vs actual changes after retraining/fine-tuning under edge edits across multiple evaluation functions (e.g., validation loss and over-smoothing/over-squashing proxies), and uses the influence scores as a tool for tasks such as graph rewiring and adversarial edge-edit attacks.

Overstatement check:
- The paper notes accuracy degrades as the number of simultaneous edits grows and that scalability to deep GNNs is challenging; treat this as a bounded-scope influence primitive rather than a universal “fast retraining replacement”.

GU connection:
- If your GU attack/defense uses influence proxies, this paper provides a propagation-aware alternative to GIF-style scores for *edge* edits, plus a discipline: report predicted-vs-actual correlation before trusting influence-guided deletion selection.

What I can borrow (method/eval/baselines):
- Method: propagation-aware influence scoring for edge edits via proximal Bregman response; extend or adapt if you need edge-deletion request generation.
- Eval: predicted-vs-actual correlation as a first-class sanity check; include side-effect metrics (e.g., over-smoothing/over-squashing proxies) so attacks aren’t “utility-only”.
- Baselines: datasets (Cora, CiteSeer, PubMed, Chameleon, Squirrel), backbones (GCN, GAT, ChebNet), and comparisons (GIF; plus adversarial-edge-edit baselines like DICE/PRBCD in their attack experiments).

What I should not borrow:
- Node deletion ≠ edge edit by default; scope carefully or extend explicitly.

Related-work sentence (English):
- “Heo et al. derive propagation-aware influence functions for edge insertions and deletions in non-convex GNNs via a proximal Bregman response, enabling accurate edit-impact prediction without full retraining.”

---

### 2511.17989 — Privacy Auditing of Multi-domain Graph Pre-trained Model under Membership Inference Attacks (MGP-MIA)
Evidence:
- PDF: `papers/2511.17989_privacy_auditing_of_multi_domain_graph_pre_trained_model_under_m.pdf`
- Text: `papers/raw/text/2511.17989.txt`
- arXiv: https://arxiv.org/abs/2511.17989

Card correction:
- Primarily an auditing attack paper; GU connection is that it uses **machine unlearning as an attack primitive** to amplify membership signals.

Claim (precise rewrite):
- The paper audits privacy leakage of multi-domain graph pre-trained models under node-level membership inference and proposes MGP-MIA, which amplifies membership signals via machine unlearning and constructs a stronger shadow model by incrementally fine-tuning the target model with limited shadow graphs, using a similarity-based inference mechanism over embedding outputs.

Novelty:
- “First work” claim in the paper: targeting MIAs at *multi-domain graph pre-trained models* rather than standard single-domain GNN training.
- A 3-component attack pipeline tailored to embedding outputs: unlearning-based membership signal amplification, incremental shadow model construction (fine-tune target vs train from scratch), and similarity-based inference features.

Methods (mechanism):
- Threat model: a white-box attacker with full access to the target model (architecture/parameters/training algorithm) but without the full multi-domain training data/process; the attacker has a shadow graph from one domain with a similar distribution to the target node.
- MGP-MIA argues existing MIAs struggle because multi-domain pre-training reduces overfitting signals and shadow graphs are unrepresentative. It first applies a membership signal amplification mechanism via (inexact) machine unlearning to increase overfitting signals, then constructs a shadow model by incrementally fine-tuning the (unlearned) target with parameter regularization, and finally trains a 2-layer MLP attack model on similarity-based features computed from a node’s embedding and its positive/negative counterparts.

Overstatement check:
- The paper’s attack assumes a strong white-box adversary and the ability to run machine unlearning/fine-tuning. When you cite it as a GU-security motivation, keep this threat-model scope explicit.

GU connection:
- It directly supports a “GU can be weaponized” narrative: unlearning is not only a defense tool but can amplify membership signals. For your work, it motivates reporting privacy leakage under adversarial deletion selection rather than focusing only on utility collapse.

What I can borrow (method/eval/baselines):
- Method: the unlearning-based signal amplification idea; incremental shadow-model construction by fine-tuning the target; similarity-based attack features for embedding-output models.
- Eval: report attack ACC/F1 across multiple victim pre-training paradigms; keep the explicit member/non-member construction (train graph nodes as members; held-out graph nodes as non-members).
- Baselines: Embed-MIA, Grad-MIA, NLO-MIA, GLO-MIA, GE-MIA, and GPIA; victims include representative multi-domain pre-trained models (e.g., GCOPE, SAMGPT, MDGPT, BRIDGE in the paper).

What I should not borrow:
- Don’t treat it as a GU baseline; it is an MIA framework.

Related-work sentence (English):
- “Luo et al. audit privacy leakage of multi-domain graph pre-trained models and propose MGP-MIA, which amplifies membership signals via machine unlearning and incrementally constructs shadow models from limited shadow graphs.”

---

### 2505.10040 — Instance-Prototype Affinity Learning for Non-Exemplar Continual Graph Learning (IPAL)
Evidence:
- PDF: `papers/2505.10040_instance_prototype_affinity_learning_for_non_exemplar_continual.pdf`
- Text: `papers/raw/text/2505.10040.txt`
- arXiv: https://arxiv.org/abs/2505.10040

Card correction:
- Continual learning, not GU: it is *non-exemplar continual graph learning* (no raw replay), motivated by memory and privacy constraints.
- The main value for you is sequential forgetting measurement (AP/AF) and prototype-based mechanisms that resemble sequential deletion dynamics.

Claim (precise rewrite):
- IPAL mitigates catastrophic forgetting in non-exemplar continual graph learning by constructing topology-integrated Gaussian prototypes (TIGP; using PageRank-based node impact) and distilling instance–prototype affinity relations (IPAD), with an added decision-boundary perception mechanism to sharpen inter-class separation.

Novelty:
- Relative to prototype replay + feature distillation: distill *instance–prototype affinities* (positive/negative relations) rather than directly constraining features, aiming for a better stability-plasticity trade-off.
- Topology-integrated Gaussian prototypes guided by node impact (PageRank) rather than mean-only prototypes.

Methods (mechanism):
- Setting: class-incremental learning over a task sequence where past raw data access is restricted (non-exemplar). The paper argues prototype replay alone suffers from prototype drift as the encoder changes, and feature distillation can over-regularize and harm plasticity.
- IPAL constructs TIGP to represent class distributions and uses IPAD to align instance–prototype relationships (positives to class-aligned prototypes; negatives to inter-class prototypes) for flexible regularization; it further adds a decision-boundary perception mechanism to repel boundary-near instances and improve separability. It evaluates on four continual node classification benchmarks (CS-CL, CoraFull-CL, Arxiv-CL, Reddit-CL) using Average Performance (AP) and Average Forgetting (AF).

Overstatement check:
- This is not “unlearning correctness”: continual learning optimizes retention under privacy/memory constraints, while GU optimizes *removal* of specific data influence. Use it as a sequential-forgetting lens/metric, not as evidence of compliance.

GU connection:
- Your GU setting with multi-round deletions can be evaluated with CGL-style forgetting curves (AP/AF-like), making sequential collapse measurable rather than a single terminal score.

What I can borrow (method/eval/baselines):
- Method: prototype-based summarization under privacy constraints; PageRank-style “impact node” weighting as a general selection prior; affinity distillation as a lighter alternative to feature distillation.
- Eval: AP/AF metrics and learning-dynamics plots across deletion rounds.
- Baselines: Bare (naive fine-tuning), Joint (upper bound), ER-GNN (rehearsal), regularization methods (EWC, MAS, LWF, GEM, TWP) and non-exemplar baselines (POLO, EFC).

What I should not borrow:
- Don’t conflate continual-learning gains with unlearning correctness.

Related-work sentence (English):
- “Song et al. study non-exemplar continual graph learning and propose IPAL with topology-integrated Gaussian prototypes and affinity distillation, providing explicit forgetting metrics that can be repurposed to quantify collapse under sequential unlearning.”

---

### 2508.02485 — Federated Graph Unlearning (PAGE)
Evidence:
- PDF: `papers/2508.02485_federated_graph_unlearning.pdf`
- Text: `papers/raw/text/2508.02485.txt`
- arXiv: https://arxiv.org/abs/2508.02485

Card correction:
- PAGE defines federated graph unlearning with two request types: meta unlearning (node/edge/feature removal within a client) and client unlearning (client withdrawal).
- The method is not “just federated + distillation”: it uses prototypes for (i) local unlearning guidance and (ii) influenced-client identification, and uses adversarial graph generation as a sensitive probe for residual knowledge.

Claim (precise rewrite):
- PAGE is a federated graph unlearning framework that supports both meta and client unlearning by combining prototype matching for precise local unlearning, adversarial graph generation for verification/residual-knowledge probing, and negative knowledge distillation for influenced clients to mitigate cross-client knowledge permeation.

Novelty:
- A unified FGU formulation spanning both meta-unlearning and client-unlearning, with an explicit objective of matching retrain-after-deletion behavior.
- Influenced-set identification via prototype similarity plus an “adversarial graph generation” verification module coupled with negative distillation to purge permeated knowledge.

Methods (mechanism):
- Problem setting: clients train local GNNs and the server aggregates; unlearning requests are either meta (ΔGi = {ΔVi, ΔEi, ΔXi} per client) or client withdrawal (remove all contributions from selected clients). The paper defines retraining as training from scratch on retained clients/graphs and frames federated unlearning as minimizing the gap between the unlearned model and this retrained reference.
- PAGE’s pipeline: clients upload class prototypes; the server uses prototype cosine similarity to identify influenced clients. For meta-unlearning, it guides local forgetting by prototype matching; it then generates adversarial graph samples that maximize discrepancies between pre- and post-unlearning models to detect residual knowledge. Finally, it performs influenced unlearning via negative knowledge distillation guided by the adversarial samples. For client unlearning, it skips prototype matching for the departing client and applies the influenced-unlearning components to purge its permeated knowledge.

Overstatement check:
- The paper’s comparisons are split because many baselines support only one request type; cite its “SOTA” claims within the paper’s evaluation protocol (simulated client partitions, random unlearning ratios) rather than as a blanket statement.

GU connection:
- PAGE operationalizes “influenced set” explicitly (clients). This maps cleanly to centralized GU where influenced nodes/regions can be defined and attacked/defended. Its adversarial graph generation module is also a concrete template for “verification probes” beyond vanilla MIA.

What I can borrow (method/eval/baselines):
- Method: influenced-set identification (prototype similarity) + negative distillation to purge permeated knowledge; adversarial-sample generation as a verification probe for residual influence.
- Eval: separate meta vs client unlearning settings; report accuracy plus MIA-based verification; include explicit unlearning ratios (10% for node/edge/feature meta unlearning; 20% clients for client unlearning in the paper).
- Baselines: client unlearning (FedEraser, FUSED, MoDe, ReGEnUnlearn) and meta unlearning (GIF, CEU, D2DGN, MEGU, FedLU, FedDM), plus Retrain.

What I should not borrow:
- Federated assumptions don’t transfer directly; treat as motivation and lens.

Related-work sentence (English):
- “Ai et al. propose PAGE for federated graph unlearning, unifying meta- and client-unlearning via prototype-guided local forgetting, adversarial graph generation for verification, and influenced-client distillation to mitigate cross-client knowledge permeation.”

---

### 2511.10936 — GraphToxin: Reconstructing Full Unlearned Graphs from Graph Unlearning
Evidence:
- PDF: `papers/2511.10936_graphtoxin_reconstructing_full_unlearned_graphs_from_graph_unlea.pdf`
- Text: `papers/raw/text/2511.10936.txt`
- arXiv: https://arxiv.org/abs/2511.10936

Card correction:
- This is a GU-focused full graph reconstruction attack (GU-FGRA) with explicit metrics and worst-case removal protocols.

Claim (precise rewrite):
- GraphToxin is a full-graph reconstruction attack against graph unlearning that exploits the publicly accessible gradient difference between the original and unlearned GNNs to recover the unlearned graph, extends to multiple-node removal, and adapts to data-free black-box settings; it also proposes a systematic evaluation framework including worst-case removal and multi-level reconstruction metrics.

Novelty:
- First GU-FGRA framing in the paper: reconstructing the *full unlearned graph* rather than inferring membership of a single edge/node.
- Attack design with multiple modules (gradient matching + curvature matching + feature smoothness; plus semantic calibration for black-box) and an evaluation framework that explicitly includes worst-case removals and metrics beyond RNMSE.

Methods (mechanism):
- White-box setting: GraphToxin uses the difference between gradients of the original and unlearned GNNs as the signal of what was removed. It optimizes a recovered graph so that gradients induced by the recovered graph match the ground-truth gradient difference (gradient matching), refines solutions by downweighting high-curvature directions (curvature matching), and regularizes with feature smoothness to encourage plausible local consistency.
- Black-box setting: when gradients are unavailable and only posteriors can be queried, the paper uses data-free model extraction (“copycats”) and introduces a semantic calibration module to reduce inconsistency between recovered node labels and predictions. Experiments are reported on Cora, PubMed, and Amazon-Photo, across GNN backbones (GCN/GraphSAGE/SGC) and GU methods (Retraining; approximate GU such as MEGU and ETR).

Overstatement check:
- “Defenses are ineffective” depends on the defenses evaluated (e.g., Node-DP and gradient compression variants in the paper) and the chosen backbones/datasets; keep the claim scoped to those settings unless you reproduce broader coverage.

GU connection:
- This is the strongest “GU introduces new attack surfaces” evidence in your set. Even if your paper’s objective is collapse (not reconstruction), GraphToxin motivates adding leakage metrics beyond MIA and adopting worst-case deletion selection protocols rather than random deletions.

What I can borrow (method/eval/baselines):
- Method: worst-case removal protocol definition (e.g., high-degree targets) as a stress test; defense evaluation structure.
- Eval: multi-level metrics for reconstruction quality (feature/topology/global/performance-level metrics in the paper) and the random-vs-worst-case comparison.
- Baselines: the paper evaluates against Retraining, MEGU, and ETR as GU methods; attacker baselines include Rand. and FewE. plus ablations of simplified attack components.

What I should not borrow:
- Don’t claim reconstruction results if your paper’s objective is collapse; position as complementary prior attack surface.

Related-work sentence (English):
- “Song and Palanisamy propose GraphToxin, a full-graph reconstruction attack against graph unlearning that leverages gradient differences and introduces worst-case removal and multi-level evaluation protocols, revealing severe reconstruction risks under both white-box and black-box settings.”

---

## 3) Research Opportunity Map (5–8 testable gaps)

Each gap below is (a) testable, (b) contrasts ≥2 papers from your set, (c) states minimum contribution + biggest risk.

### Gap 1: Adversarial deletion selection is missing from standard GU benchmarks
Contrast:
- OpenGU (`2501.02728`) standardizes broad metrics but does not center adversarial request generation.
- GraphToxin (`2511.10936`) motivates worst-case removal, but focuses on reconstruction risk rather than retained-utility collapse.

Testable statement:
- Under a fixed deletion budget |D_unlearn|, influence-guided deletion requests cause a significantly larger retained-utility drop for approximate GU methods than random deletion, while the same deletion set under retrain-after-deletion has a smaller drop.

Minimum contribution:
- Add an “adversarial request generator” suite (Random/Degree/PageRank + IF/TracIn proxies + IM/NIM-style) and integrate it into OpenGU-style evaluation across GU families.

Biggest risk:
- Reviewer pushback: “you are just removing important nodes.” Mitigation: always report Retrain-after-deletion and the “approximation gap” (Unlearn vs Retrain).

---

### Gap 2: Collateral damage (over-forgetting) is under-measured and under-defended
Contrast:
- UtU (`2402.10695`) defines and measures over-forgetting and ties it to loss design.
- Partition methods (GraphRevoker `2403.07353`, CGE `2408.09705`) emphasize efficiency/utility without a unified collateral damage suite.

Testable statement:
- Adversarial UE selection increases collateral damage metrics (e.g., retained-edge probability drop Δp_r; retained-node utility) disproportionately for specific loss designs and approximation rules.

Minimum contribution:
- Generalize “over-forgetting” into a unified collateral-damage metric suite across request types and use it as both an attack objective and a defense target.

Biggest risk:
- Too many metrics. Mitigation: define one primary collateral metric per request type tied to user-facing harm.

---

### Gap 3: Influence proxies need calibration, not just intuition
Contrast:
- Edge-edit IF (`2506.04694`) validates influence by predicted-vs-actual correlation.
- SGU (`2501.11823`) uses influence to select HIE for better unlearning, not for worst-case collapse.

Testable statement:
- A proxy influence score that correlates with local edit impact does not necessarily maximize global retained-utility collapse under GU; calibration is required.

Minimum contribution:
- Add a calibration protocol: correlate proxy scores with retrain deltas; ablate propagation-driven vs parameter-driven influence components.

Biggest risk:
- Compute overhead. Mitigation: calibrate on small graphs; scale via sampling.

---

### Gap 4: Certified GU has a theory–practice boundary that can be attacked
Contrast:
- ScaleGUN (`2408.09212`) controls approximation error to preserve certification.
- Practical GU methods in OpenGU (`2501.02728`) include deep/heuristic settings without certification.

Testable statement:
- When certification assumptions are violated (e.g., deep backbones / non-linear modules), approximation-error control alone does not prevent worst-case deletion-induced collapse.

Minimum contribution:
- Boundary map: certified linear setting vs practical deep setting under matched deletion budgets and identical evaluation.

Biggest risk:
- Scope creep into theory. Mitigation: keep claims empirical and scoped.

---

### Gap 5: Unlearning can be weaponized as an attack primitive
Contrast:
- MGP-MIA (`2511.17989`) uses unlearning to amplify membership signals.
- GraphToxin (`2511.10936`) shows GU introduces reconstruction attack surfaces.

Testable statement:
- Adversarial deletion strategies can increase privacy leakage signals even when utility remains acceptable.

Minimum contribution:
- Jointly evaluate utility collapse + privacy leakage under the same adversarial deletion selection.

Biggest risk:
- Threat model confusion. Mitigation: provide a threat-model table separating “who chooses deletions” vs “who observes outputs”.

---

### Gap 6: Influenced-set modeling is underused in centralized GU security
Contrast:
- PAGE (`2508.02485`) models influenced clients and distills them.
- SGU (`2501.11823`) defines HIE influenced nodes; partition methods also expose cross-region effects.

Testable statement:
- In centralized GU, influenced-set size/shape predicts vulnerability to collapse under adversarial UE selection.

Minimum contribution:
- Define influenced-region statistics (size, boundary, homophily) and show they predict approximation gap and collapse.

Biggest risk:
- Correlation-only story. Mitigation: intervene by controlling influenced-set thresholds/budgets.

---

### Gap 7 (optional): Sequential deletion is closer to continual forgetting than one-shot GU
Contrast:
- OpenGU (`2501.02728`) covers deletion intensity sweeps but not necessarily multi-round adversarial sequences.
- IPAL (`2505.10040`) provides explicit forgetting metrics for sequences.

Testable statement:
- Under multi-round adversarial deletion requests, approximate GU exhibits compounding forgetting dynamics not captured by single-shot metrics.

Minimum contribution:
- Add a sequential deletion protocol and report forgetting curves (AF-like) in addition to final utility.

Biggest risk:
- Experimental load. Mitigation: start with 2–3 datasets and 2–3 methods to show qualitative failure modes.

---

## 4) Reviewer-Style Rubric for *Your* Idea (Initial + Revised)

Your stated idea (grounded in `self/PROJECT_MASTER_CONTEXT.md` and `self/宏观plan.md`):
- Attack goal: choose a deletion set D_unlearn to induce catastrophic forgetting / performance collapse in **approximate** GU methods (GIF/GST-like), arguing brittleness of approximations.
- Core mechanism: IF-IM hybrid node selection: pseudo-IF (TracIn / gradient proxies / XAI) + influence maximization (CELF, PageRank etc), fused by weighted/rank-based scoring.
- Key experimental anchor: compare against Random and structure heuristics; include Retrain gap to attribute brittleness to approximation error.

### Initial Rubric (1–5)
Novelty: 3/5
- Overlapping conceptual space exists with influence-maximization-for-GU (SGU `2501.11823`) and worst-case attack framing (GraphToxin `2511.10936`). Your novelty must be stated as “adversarial deletion-request attack against approximate GU” + a measurable attribution to approximation gap.

Soundness: 3/5
- Threat model realism is the main risk: who can request deletion of arbitrary nodes? If only self-owned nodes are deletable, you need an explicit mapping (e.g., attacker controls many accounts / nodes).
- Attribution risk: without retrain-after-deletion comparisons, collapse can be dismissed as “you deleted important nodes”.

Significance: 4/5
- If you show a robust, scalable vulnerability that differentiates method families (approximate collapses; retraining-based resists), it is a strong security message for GU.

Evaluation: 3/5
- Your plan already includes retrain comparisons and baselines, which is good. To reach top-tier bar, you need threat-model-aligned baselines and multi-metric leakage beyond MIA AUC (GraphToxin’s critique).

Reproducibility: 4/5
- Building on OpenGU/GULib with a clear module plan is a strength if you ship scripts/configs and fixed seeds.

Story: 3/5
- Risk: being perceived as “a heuristic to pick nodes”. You need a crisp conceptual claim + evidence chain: (i) adversarial deletion selection is realistic, (ii) collapse is tied to approximation brittleness, (iii) defenses/limits are mapped.

### “Top-Conference Bar” Hard Checklist (>=8, prioritized)
1. Threat model table (must): attacker capability for choosing deletions; constraints (self-owned nodes only? multiple accounts? query access?).
2. Attribution via retrain gap (must): always report Unlearn vs Retrain-after-deletion; define “approximation gap”.
3. Strong baselines (must): Random/Degree/PageRank + SGU-style NIM/HIE selection (`2501.11823`) + GraphToxin-style worst-case heuristics (`2511.10936`) + gradient-norm/TracIn variants.
4. Coverage across GU families (must): include at least one partition-based, one IF/approx, one learning-based method; use OpenGU taxonomy (`2501.02728`) to justify.
5. Multi-metric leakage (must): don’t rely solely on MIA AUC; add at least one reconstruction-related or alternative leakage signal motivated by GraphToxin.
6. Efficiency accounting (must): selection time + unlearning time; show feasibility under realistic budgets.
7. Ablations (must): IF vs IM vs Hybrid; fusion type; α/β sensitivity; budget K; stability over runs.
8. Boundary conditions (should): homophily/heterophily; sparse/dense; small/large; explain via influenced-region stats.
9. Mechanistic explanation (should): connect collapse to at least one concrete failure mode seen in literature (e.g., over-forgetting in `2402.10695`, propagation sensitivity in `2506.04694`, influenced-set contamination lens in `2508.02485`).
10. Positioning vs prior attacks (should): differentiate from reconstruction (GraphToxin) and auditing (MGP-MIA) by objective, observables, and defenses.

### Revised Rubric (if checklist items 1–8 are done)
Novelty: 4/5
Soundness: 4/5
Significance: 4–5/5
Evaluation: 4/5
Reproducibility: 4–5/5
Story: 4/5

---

## Appendix: Evidence Pointers
- Full PDFs: `papers/`
- Searchable texts: `papers/raw/text/*.txt`
- Metadata: `papers/papers.csv`
- Rough cards: `papers/notes/*.md`

