# Abstract

**Adversarial Deletion Attacks on Approximate Graph Unlearning**

Machine unlearning—the ability to remove specific data from trained models without full retraining—is increasingly critical for privacy-compliant vision systems operating over graph-structured data, including scene graphs, skeleton-based action recognition, and 3D point cloud networks. Approximate graph unlearning (GU) methods offer computational efficiency but introduce systematic approximation errors that, we show, can be adversarially exploited.

We present, to our knowledge, the first systematic adversarial audit of approximate GU. An adversary controlling deletion requests can strategically select nodes—via influence maximization, pseudo-influence functions, or hybrid strategies—to amplify approximation error and collapse model utility. We evaluate five representative GU methods spanning three mechanism families (learning-based, influence-function, shard-based) on Cora, Citeseer, and ogbn-arxiv (169K nodes) with GCN and GAT backbones; the framework is architecture-agnostic and applies directly to vision GNNs.

Our findings reveal a stark **vulnerability spectrum** determined by each method's mechanism: (1) learning-based GNNDelete suffers F1 collapse averaging 16% with peaks above 27% under a deletion budget below 5% of training nodes; (2) influence-function-based GIF shows marginal but statistically significant vulnerability (paired effect ≈+4% F1, p<0.001), bounded by its Newton-step approximation; (3) shard-based GraphEraser exhibits a counterintuitive **Shard Protection Effect**—both random and adversarial deletion *improve* downstream F1 by 3–6%, with the attacker's gain bounded above by random selection, as the partition aggregator absorbs deletion as regularization; (4) feature-preserving (MEGU) and certified-gradient (IDEA) families exhibit null effect (<1% F1 difference), revealing a *mechanism-incomparable* robustness dimension that current selector designs cannot exploit.

We further introduce **collateral damage** diagnostics—retrain gap, prediction shift, and a novel **hop-distance decay** quantifying disturbance propagation through the GNN's receptive field—providing a principled audit for any approximate unlearning deployment, from citation networks to vision GNN systems.

---

> Word count: ~290 words
> Target venue: ECCV 2026
> Last updated: 2026-05-04 (was 2026-02-26 — see review/abstract_review_2026-05-04.md for diff)
> Previous version: sections/abstract_v1_2026-02-26.md
> Status: **interim** — F1/effect numbers come from pre-Phase-B data; will be refreshed after server re-run with the v4-decoupled IM selector and MIA bug fixes (see self/dashboard/EXPERIMENT_DASHBOARD.md §1)
