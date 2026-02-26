# Visualization Plan for Adversarial GNN Unlearning Paper

This document outlines the systematic visualization of experiment results (620 runs, 5 seeds) to support the research claims.

## Summary Table of Charts

| Chart ID | Target Section | Focus | Form | Key Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **FIG-1** | Generalization | Cross-Dataset/Model Stability | Grouped Bar + Error | F1 Drop (%) |
| **FIG-2** | Scaling | Ratio Sensitivity Curves | Line + Shaded Area | F1 Drop (%) |
| **FIG-3** | Method Comparison | Performance on Modern Algorithms | Horiz. Relative Bar | Rel. Gain over Random |
| **FIG-4** | Significance | P-value Heatmap | Heatmap | -log10(p) |
| **FIG-5** | Trade-off | Success vs. Collateral Damage | Scatter Plot | F1 Drop vs. Gap |

---

## Detailed Specifications

### FIG-1: The "Generalization Matrix"
*   **Purpose**: To prove the attack works reliably across different graph environments.
*   **Config**:
    *   **Phase**: MG-0, MG-1, MG-2
    *   **Settings**: (Cora, GCN), (Citeseer, GCN), (Cora, GAT)
    *   **Methods**: GIF, GNNDelete, GraphEraser
    *   **Strategies**: `random` vs `hybrid_v4`
*   **Narrative**: "Structural attacks consistently outperform random baselines across both dataset and model boundaries."

### FIG-2: Attack Scalability Curve
*   **Purpose**: To show how the budget affects attack potency.
*   **Config**:
    *   **Phase**: ratio_sensitivity
    *   **Ratios**: 0.01, 0.05, 0.10, 0.20
    *   **Methods**: GIF, GNNDelete
    *   **Strategies**: `random`, `degree`, `im_v4`, `hybrid_v4`
*   **Narrative**: "The attack effectiveness exhibits a non-linear scaling with deletion budget, maintaining a significant gap even at 1% deletion."

### FIG-3: Generalization to Modern Algorithms
*   **Purpose**: To show the attack is not overfitted to basic algorithms.
*   **Config**:
    *   **Phase**: MG-3 (Citeseer-GCN, Cora-GAT)
    *   **Methods**: IDEA, MEGU, GIF (for reference)
    *   **Metric**: Relative improvement: `(Hybrid - Random) / Random`
*   **Narrative**: "Modern, state-of-the-art unlearning algorithms (IDEA, MEGU) remain vulnerable to structural influence-based attacks."

### FIG-4: Statistical Significance Map
*   **Purpose**: To provide rigorous evidence for the claims.
*   **Config**:
    *   **Data**: `all_phases_stats.csv`
    *   **Y-Axis**: All (Method, Dataset, Model) pairs
    *   **X-Axis**: Tracin, IM_v4, Hybrid_v4
    *   **Cell Value**: -log10(p-value) vs. Random
*   **Narrative**: "Most structured attacks achieve p < 0.05 across almost all tested configurations."

---

## Integrity Check (Workflow Significance)

1.  **MG-0 (Baseline)**: Established in FIG-1. Essential as the ground truth.
2.  **MG-1/2 (Generalization)**: Consolidated in FIG-1. Proves the research isn't a "one-trick pony" on Cora.
3.  **MG-3 (Neutrality)**: Visualized in FIG-3. Critical for peer-reviewed journals to show the attack doesn't just exploit "weak" baselines.
4.  **Ratio Sensitivity**: Visualized in FIG-2. Shows the practical limits and budget efficiency of the attack.
5.  **Multi-Seed Statistics**: Reflected in all error bars and p-value charts. Essential for scientific rigor.

**File Reference**: Data should be pulled from `results/evaluation/stats/all_phases_stats.csv`.
