# Graph Unlearning + GNN Paper Library (Reproducible Build)

- Build time (UTC): `2026-02-16T03:56:33.985931+00:00`
- Priority window: `2024-02-16 to now`
- Metadata sources: arXiv + Semantic Scholar + Crossref (if DOI available)

## Search Queries (arXiv)

- `all:"graph unlearning"`
- `all:"graph neural network" AND (all:unlearning OR all:"machine unlearning" OR all:forgetting OR all:deletion)`
- `all:"graph learning" AND (all:unlearning OR all:"machine unlearning" OR all:forgetting OR all:deletion)`
- `all:"graph neural network" AND (all:"membership inference" OR all:"privacy auditing" OR all:privacy)`
- `all:"graph learning" AND (all:"membership inference" OR all:"privacy auditing" OR all:privacy)`
- `all:"graph neural network" AND (all:distillation OR all:"influence function" OR all:partition OR all:"efficient retraining")`
- `all:"graph learning" AND (all:distillation OR all:"influence function" OR all:partition OR all:"efficient retraining")`

## Scoring

- relevance (0-3): keyword-group match to GU topics
- venue gate (0-3): top venue > known venue > unknown
- influence (0-3): Semantic Scholar citation count
- reproducibility (0-2): PDF + code signal

## Candidate Table (>=20)

| # | arXiv | Year | Title | Scores (R+V+I+Rep) | Citations | Selected | Evidence |
|---|---|---:|---|---|---:|---|---|
| 1 | 2408.09212 | 2024 | Scalable and Certifiable Graph Unlearning: Overcoming the Approximation Error Barrier | 3+2+2+2=9 | 10 | yes | [arXiv](https://arxiv.org/abs/2408.09212) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2408.09212?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) |
| 2 | 2402.10695 | 2024 | Unlink to Unlearn: Simplifying Edge Unlearning in GNNs | 3+3+2+1=9 | 17 | yes | [arXiv](https://arxiv.org/abs/2402.10695) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.10695?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2402.10695) |
| 3 | 2403.07353 | 2024 | Graph Unlearning with Efficient Partial Retraining | 3+2+2+1=8 | 23 | yes | [arXiv](https://arxiv.org/abs/2403.07353) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2403.07353?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.1145%2F3589335.3651265) |
| 4 | 2505.22649 | 2025 | Pre-training for Recommendation Unlearning | 3+2+1+2=8 | 2 | no | [arXiv](https://arxiv.org/abs/2505.22649) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2505.22649?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.1145%2F3726302.3730060) |
| 5 | 2408.09705 | 2024 | Community-Centric Graph Unlearning | 3+3+1+1=8 | 3 | yes | [arXiv](https://arxiv.org/abs/2408.09705) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2408.09705?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2408.09705) |
| 6 | 2507.05649 | 2025 | DESIGN: Encrypted GNN Inference via Server-Side Input Graph Pruning | 3+1+1+2=7 | 1 | no | [arXiv](https://arxiv.org/abs/2507.05649) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2507.05649?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2507.05649) |
| 7 | 2505.12614 | 2025 | Adaptive Graph Unlearning | 3+2+1+1=7 | 2 | no | [arXiv](https://arxiv.org/abs/2505.12614) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2505.12614?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2505.12614) |
| 8 | 2502.06327 | 2025 | Prompt-Driven Continual Graph Learning | 3+1+1+2=7 | 1 | no | [arXiv](https://arxiv.org/abs/2502.06327) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2502.06327?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2502.06327) |
| 9 | 2601.09469 | 2026 | FairGU: Fairness-aware Graph Unlearning in Social Networks | 3+1+0+2=6 | 0 | no | [arXiv](https://arxiv.org/abs/2601.09469) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2601.09469?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) |
| 10 | 2511.17989 | 2025 | Privacy Auditing of Multi-domain Graph Pre-trained Model under Membership Inference Attacks | 3+0+1+1=5 | 1 | yes | [arXiv](https://arxiv.org/abs/2511.17989) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2511.17989?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2511.17989) |
| 11 | 2508.02485 | 2025 | Federated Graph Unlearning | 3+0+1+1=5 | 1 | yes | [arXiv](https://arxiv.org/abs/2508.02485) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2508.02485?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2508.02485) |
| 12 | 2506.00808 | 2025 | Unlearning Inversion Attacks for Graph Neural Networks | 3+0+1+1=5 | 2 | no | [arXiv](https://arxiv.org/abs/2506.00808) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.00808?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.1145%2F3773966.3777929) |
| 13 | 2503.02959 | 2025 | Node-level Contrastive Unlearning on Graph Neural Networks | 3+0+1+1=5 | 1 | no | [arXiv](https://arxiv.org/abs/2503.02959) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2503.02959?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2503.02959) |
| 14 | 2501.11823 | 2025 | Toward Scalable Graph Unlearning: A Node Influence Maximization based Approach | 3+0+1+1=5 | 4 | yes | [arXiv](https://arxiv.org/abs/2501.11823) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2501.11823?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2501.11823) |
| 15 | 2501.02728 | 2025 | OpenGU: A Comprehensive Benchmark for Graph Unlearning | 3+0+1+1=5 | 8 | yes | [arXiv](https://arxiv.org/abs/2501.02728) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2501.02728?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2501.02728) |
| 16 | 2512.02460 | 2025 | UniCom: Towards a Unified and Cohesiveness-aware Framework for Community Search and Detection | 3+0+0+1=4 | 0 | no | [arXiv](https://arxiv.org/abs/2512.02460) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2512.02460?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2512.02460) |
| 17 | 2511.14168 | 2025 | Certified Signed Graph Unlearning | 3+0+0+1=4 | 0 | no | [arXiv](https://arxiv.org/abs/2511.14168) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2511.14168?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2511.14168) |
| 18 | 2511.10936 | 2025 | GraphToxin: Reconstructing Full Unlearned Graphs from Graph Unlearning | 3+0+0+1=4 | 0 | yes | [arXiv](https://arxiv.org/abs/2511.10936) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2511.10936?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2511.10936) |
| 19 | 2509.04785 | 2025 | Graph Unlearning: Efficient Node Removal in Graph Neural Networks | 3+0+0+1=4 | unknown | no | [arXiv](https://arxiv.org/abs/2509.04785) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2509.04785?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) |
| 20 | 2508.02044 | 2025 | Graph Unlearning via Embedding Reconstruction -- A Range-Null Space Decomposition Approach | 3+0+0+1=4 | 0 | no | [arXiv](https://arxiv.org/abs/2508.02044) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2508.02044?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2508.02044) |
| 21 | 2506.04694 | 2025 | Influence Functions for Edge Edits in Non-Convex Graph Neural Networks | 3+0+0+1=4 | 0 | yes | [arXiv](https://arxiv.org/abs/2506.04694) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.04694?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2506.04694) |
| 22 | 2505.14945 | 2025 | Unlearning Algorithmic Biases over Graphs | 3+0+0+1=4 | 0 | no | [arXiv](https://arxiv.org/abs/2505.14945) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2505.14945?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2505.14945) |
| 23 | 2505.10040 | 2025 | Instance-Prototype Affinity Learning for Non-Exemplar Continual Graph Learning | 3+0+0+1=4 | 0 | yes | [arXiv](https://arxiv.org/abs/2505.10040) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2505.10040?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) / [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2505.10040) |
| 24 | 2401.11760 | 2024 | Towards Effective and General Graph Unlearning via Mutual Evolution | 3+0+0+1=4 | unknown | no | [arXiv](https://arxiv.org/abs/2401.11760) / [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2401.11760?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue) |

## Selected Papers (8-12)

### 1. 2402.10695 - Unlink to Unlearn: Simplifying Edge Unlearning in GNNs
- score: `3+3+2+1=9`
- keywords: `mia,privacy,unlearning`
- screening reason: relevance=3 from keyword groups: mia,privacy,unlearning
- evidence: [arXiv](https://arxiv.org/abs/2402.10695), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.10695?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2402.10695)
- note card: `papers/notes/2402.10695.md`

### 2. 2403.07353 - Graph Unlearning with Efficient Partial Retraining
- score: `3+2+2+1=8`
- keywords: `partition,retraining,unlearning`
- screening reason: relevance=3 from keyword groups: partition,retraining,unlearning
- evidence: [arXiv](https://arxiv.org/abs/2403.07353), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2403.07353?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.1145%2F3589335.3651265)
- note card: `papers/notes/2403.07353.md`

### 3. 2408.09212 - Scalable and Certifiable Graph Unlearning: Overcoming the Approximation Error Barrier
- score: `3+2+2+2=9`
- keywords: `privacy,retraining,unlearning`
- screening reason: relevance=3 from keyword groups: privacy,retraining,unlearning; doi unknown
- evidence: [arXiv](https://arxiv.org/abs/2408.09212), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2408.09212?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue)
- note card: `papers/notes/2408.09212.md`

### 4. 2408.09705 - Community-Centric Graph Unlearning
- score: `3+3+1+1=8`
- keywords: `partition,privacy,unlearning`
- screening reason: relevance=3 from keyword groups: partition,privacy,unlearning
- evidence: [arXiv](https://arxiv.org/abs/2408.09705), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2408.09705?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2408.09705)
- note card: `papers/notes/2408.09705.md`

### 5. 2501.02728 - OpenGU: A Comprehensive Benchmark for Graph Unlearning
- score: `3+0+1+1=5`
- keywords: `privacy,retraining,unlearning`
- screening reason: relevance=3 from keyword groups: privacy,retraining,unlearning
- evidence: [arXiv](https://arxiv.org/abs/2501.02728), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2501.02728?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2501.02728)
- note card: `papers/notes/2501.02728.md`

### 6. 2501.11823 - Toward Scalable Graph Unlearning: A Node Influence Maximization based Approach
- score: `3+0+1+1=5`
- keywords: `influence,privacy,unlearning`
- screening reason: relevance=3 from keyword groups: influence,privacy,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2501.11823), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2501.11823?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2501.11823)
- note card: `papers/notes/2501.11823.md`

### 7. 2506.04694 - Influence Functions for Edge Edits in Non-Convex Graph Neural Networks
- score: `3+0+0+1=4`
- keywords: `influence,retraining,unlearning`
- screening reason: relevance=3 from keyword groups: influence,retraining,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2506.04694), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.04694?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2506.04694)
- note card: `papers/notes/2506.04694.md`

### 8. 2511.17989 - Privacy Auditing of Multi-domain Graph Pre-trained Model under Membership Inference Attacks
- score: `3+0+1+1=5`
- keywords: `mia,privacy,unlearning`
- screening reason: relevance=3 from keyword groups: mia,privacy,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2511.17989), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2511.17989?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2511.17989)
- note card: `papers/notes/2511.17989.md`

### 9. 2505.10040 - Instance-Prototype Affinity Learning for Non-Exemplar Continual Graph Learning
- score: `3+0+0+1=4`
- keywords: `distillation,privacy,unlearning`
- screening reason: relevance=3 from keyword groups: distillation,privacy,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2505.10040), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2505.10040?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2505.10040)
- note card: `papers/notes/2505.10040.md`

### 10. 2508.02485 - Federated Graph Unlearning
- score: `3+0+1+1=5`
- keywords: `privacy,unlearning`
- screening reason: relevance=3 from keyword groups: privacy,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2508.02485), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2508.02485?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2508.02485)
- note card: `papers/notes/2508.02485.md`

### 11. 2511.10936 - GraphToxin: Reconstructing Full Unlearned Graphs from Graph Unlearning
- score: `3+0+0+1=4`
- keywords: `privacy,unlearning`
- screening reason: relevance=3 from keyword groups: privacy,unlearning; early citation stage
- evidence: [arXiv](https://arxiv.org/abs/2511.10936), [S2](https://api.semanticscholar.org/graph/v1/paper/arXiv:2511.10936?fields=title%2Cyear%2CcitationCount%2Cvenue%2CexternalIds%2Cauthors%2Curl%2CpublicationVenue), [Crossref](https://api.crossref.org/works/10.48550%2FarXiv.2511.10936)
- note card: `papers/notes/2511.10936.md`

## Outputs

- `papers/papers.csv`
- `papers/candidates.csv`
- `papers/library.bib`
- `papers/notes/*.md`
- `papers/raw/*.json`
