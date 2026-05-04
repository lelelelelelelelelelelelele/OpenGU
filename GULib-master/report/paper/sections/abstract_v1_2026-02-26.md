# Abstract

**Adversarial Deletion Attacks on Approximate Graph Unlearning**

Machine unlearning—the ability to remove specific data from trained models without full retraining—is increasingly critical for privacy-compliant vision systems operating over graph-structured data, including scene graphs, skeleton-based action recognition, and 3D point cloud networks. Approximate graph unlearning (GU) methods offer computational efficiency but introduce systematic approximation errors that, we show, can be adversarially exploited.

We present the first systematic adversarial audit of approximate graph unlearning. An adversary controlling deletion requests can strategically select nodes—using influence maximization, influence functions, or hybrid strategies—to amplify the approximation error of the unlearning procedure and collapse model utility. We evaluate five representative GU methods spanning three mechanism families (learning-based, influence-function-based, and shard-based) across multiple graph datasets and backbone architectures (GCN, GAT).

Our findings reveal a stark **vulnerability spectrum** determined by each method's internal mechanism: (1) learning-based methods (GNNDelete) suffer catastrophic F1 collapse exceeding 17% under a deletion budget of less than 1% of the graph; (2) influence-function-based methods (GIF) show marginal vulnerability owing to tight Newton-step approximation; (3) shard-based methods (GraphEraser) exhibit a counterintuitive immunity—a *Shard Protection Effect* in which adversarial deletion actually *improves* downstream performance. We further introduce **collateral damage** metrics (retrain gap, prediction shift) that attribute performance collapse to approximation error rather than information loss, providing a principled diagnostic for auditing any approximate unlearning deployment. Our framework directly applies to vision GNN systems where privacy-compliant unlearning is required, exposing a fundamental security risk in current approximate unlearning practice.

---

> Word count: ~230 words
> Target venue: ECCV 2026
> Last updated: 2026-02-26
