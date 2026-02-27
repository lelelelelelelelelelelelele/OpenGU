# Visualization Plan for Adversarial GNN Unlearning Paper (V2)

This document outlines the systematic visualization of experiment results, strictly adhering to the **Relative F1 Drop** definition (using k=5 random baseline) to isolate attack potency from unlearning method characteristics.

## Core Metric Definition
*   **Baseline F1**: $\overline{F1}_{after}(k=5, random)$ — Mean F1 after random unlearning of 5 nodes (across 5 independent seeds). This isolates the "intrinsic method effect" or "protection effect".
*   **Relative F1 Drop**: $\Delta F1_{rel} = \overline{F1}_{after}(k=5, random) - F1_{after}(ratio=0.05, attack)$
*   **Relative Gain**: $Gain = \frac{\Delta F1_{rel}(Attack) - \Delta F1_{rel}(Random\_Ratio)}{\Delta F1_{rel}(Random\_Ratio)}$ (Used for vulnerability comparison).

---

## Summary Table of Charts

| Chart ID | Target Section | Focus | Form | Key Metrics | Methods |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FIG-1** | Generalization | Cross-Dataset/Model Potency | Grouped Bar + Error | **Relative F1 Drop** | GIF, GDel, GEraser |
| **FIG-2** | Scaling | Ratio Sensitivity | Line + Shaded Area | Relative F1 Drop | GIF, GDel (All algorithmic strategies) |
| **FIG-3** | **Spectrum** | **Universal Vulnerability** | **Stacked/Grouped Bar** | **Relative F1 Drop & Gain** | **All 5 Methods** |
| **FIG-4** | Significance | Statistical Rigor | Heatmap | -log10(p-value) | All 5 Methods |
| **FIG-5** | Collateral | Mimicry Quality | **Scatter Plot** | **Rel. F1 Drop vs. Gap** | All 5 Methods |

---

## Detailed Specifications

### FIG-1: Generalization Potency (The "Clean" Drop)
*   **Purpose**: To prove structured attacks cause real damage beyond method-inherent F1 fluctuations.
*   **Metrics**: **Relative F1 Drop** (k=5 baseline).
*   **Settings**: (Cora, GCN), (Citeseer, GCN), (Cora, GAT).
*   **Logic**: By using the k=5 baseline, we show that even if GraphEraser has a "self-repair" effect (F1 up on random k=5), our Hybrid/IM strategies still force a significant *relative* drop.

### FIG-2: Attack Scaling Efficiency
*   **Purpose**: To define the "strength-vs-budget" curve for different algorithmic selection strategies.
*   **Metrics**: Relative F1 Drop across ratios (0.01, 0.05, 0.10, 0.20).
*   **Settings**: GIF and GNNDelete on Cora-GCN.
*   **Logic**: Excludes the random baseline (to isolate algorithm efficacy) and compares `hybrid_v4`, `im_v4`, `tracin`, `pagerank`, and `degree` to show which algorithm scales damage most efficiently as budget increases.

### FIG-3: The Unlearning Vulnerability Spectrum (5-Method View)
*   **Purpose**: The "Grand Summary" showing the attack's platform-agnostic nature.
*   **Methods**: GIF, GNNDelete, GraphEraser (GCN); IDEA, MEGU (GAT). All at ratio 0.05.
*   **Metric 1**: **Relative F1 Drop** (Absolute damage).
*   **Metric 2**: **Relative Gain (V-Factor)**: Vulnerability factor showing how much worse Hybrid is than Random.
*   **Logic**: Demonstrates that IF-based (GIF, IDEA), Learning-based (GDel, MEGU), and Shard-based (GEraser) all possess structural vulnerabilities. *(Note: V-Factor is omitted for IDEA/MEGU due to intentionally uncollected random baselines for those expensive runs).*

### FIG-4: Statistical Significance Heatmap
*   **Purpose**: Prove that findings are not due to seed-level noise.
*   **Metric**: P-value (Paired T-test between `Hybrid_v4` and the **k=5 baseline**).
*   **Logic**: Stronger evidence than comparing against ratio-matched random, as it proves the attack breaks the "equilibrium" of the unlearning method.

### FIG-5: Attack Depth & Mimicry (Collateral Damage)
*   **Purpose**: To prove the attack is "deeply structural" and mimics exact retraining.
*   **X-Axis**: **Relative F1 Drop** (Attack Potency).
*   **Y-Axis**: **Retrain Gap** (Mimicry error: $|F1_{unlearn} - F1_{retrain}|$).
*   **Logic**: We want to show that Hybrid-selected nodes don't just "break" the model (high drop), they "unlearn" it (low gap to retrain). Points in the bottom-right represent "Perfect Adversarial Unlearning".

---

## Integrity Check (Experimental Logic)

1.  **k=5 Baseline (Standardization)**: Every chart now uses this as the "zero point", ensuring fairness across methods with different inherent F1 behaviors.
2.  **Relative F1 Drop (Purified Metric)**: Removes "protection effects" of Shard-based methods and "natural degradation" of Learning-based methods.
3.  **MG-3 Integration (Modern Algorithms)**: FIG-3 and FIG-5 ensure that state-of-the-art methods (IDEA, MEGU) are held to the same standard as baselines.
4.  **Mimicry Check (Collateral)**: FIG-5 connects "Attack Success" to "Structural Correctness", proving our attack strategy targets the core influence mechanism.

**Data Reference**: `results/relative/` for Relative F1 Drop; `results/collateral/` for Retrain Gap; `results/evaluation/stats/` for aggregated means.
