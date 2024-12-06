<div align="center">
  <img src="Resources/OpenGU.jpg" alt="OpenGU Logo" border="0" width=600px/>
</div>

------

<p align="center">
  <a href="https://gu.readthedocs.io/en/latest/">Docs</a> •
  <a href="#overview-of-the-benchmark">Overview of the Benchmark</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#reference">Reference</a>
</p>

<p align="center">
  <a href="https://gu.readthedocs.io/en/latest/?badge=latest">
  <img src="https://img.shields.io/readthedocs/gu.svg?style=flat-square" alt="Documentation Status"/></a>
  <img src="https://badgen.net/github/license/FrankCoding00/GU" alt="license" />
  <img src="https://img.shields.io/badge/version-0.1-green" alt="version" />
</p>

# OpenGU

## Abstract

> **Graph Machine Learning (GML)** has become integral to understanding and analyzing complex relational data, highlighting the growing necessity for **Graph Unlearning (GU)** to address challenges in removing sensitive information from trained graph neural networks (GNNs). Differing from machine unlearning in computer vision (CV) or large language models (LLMs), GU presents unique challenges due to the intricate interactions within graph entities, the diversity of downstream tasks, and the varied nature of unlearning requests. Despite the proliferation of diverse GU strategies, the lack of standardized experimental setups and evaluation criteria, and the limited flexibility in combining downstream tasks and unlearning requests have yielded inconsistencies in comparisons, hindering the thriving development of this research domain. To fill this gap, we have integrated **16 SOTA GU algorithms** and **19 multi-domain datasets** within OpenGU, enabling a variety of downstream tasks on **7 GNN backbones** when responding to flexible unlearning requests. Based on this unified benchmark framework, we are able to provide a comprehensive and fair evaluation for GU. Through extensive experimentation, we have drawn crucial **conclusions** about the effectiveness of existing GU methods, while also gaining valuable insights into its limitations, shedding light on potential avenues for future research.

## Introduction

OpenGU is an open-source platform designed to provide a comprehensive benchmark for **Graph Unlearning**. This project aims to facilitate the evaluation and development of Graph Unlearning methodologies by offering standardized datasets, frameworks, and tools. OpenGU leverages advanced techniques in Graph Structure Learning (GSL) to enhance the performance and robustness of Graph Neural Networks (GNNs) across various applications.

<div align="center">
  <img src="Resources/methods_overview.png" alt="Methods Overview" border="0" width=600px/>
  <p align="center"><em>Figure 1: Overview of the Graph Unlearning Methods Implemented in OpenGU.</em></p>
</div>

## Overview of the Benchmark

OpenGU offers a robust and standardized benchmark for evaluating **Graph Unlearning** methods. It ensures a fair comparison between different approaches by providing consistent datasets, evaluation metrics, and experimental setups. This benchmark is instrumental in advancing research in Graph Unlearning, promoting reproducibility, and accelerating innovation in the field.

<div align="center">
  <img src="Resources/Framework.png" alt="Benchmark Framework" border="0" width=600px/>
  <p align="center"><em>Figure 2: Overall Benchmark Framework of OpenGU.</em></p>
</div>

## Dataset Overview

Graph unlearning scenarios are fundamentally data-driven, making the meticulous selection of datasets indispensable for evaluating the effectiveness of graph unlearning strategies. To assess the effectiveness, efficiency, and robustness of these methods for node or edge-related tasks, we have carefully selected **19 datasets** [24].

### Node and Edge-Level Tasks:

- **Citation Networks:** Cora, Citeseer, PubMed [57]
- **Co-author Networks:** CS, Physics [40]
- **Image Networks:** Flickr [61]
- **E-commerce and Product Networks:** Photo, Computers [40], ogbn-products [23], Amazon-ratings [36]
- **Scientific and Knowledge Networks:** DBLP [60], ogbn-arxiv [23]
- **Webpage Networks:** Squirrel, Chameleon [35]
- **Actor Networks:** Actor [35]
- **Online Gaming:** Minesweeper [36]
- **Crowdsourcing Platform:** Tolokers [36]
- **Historical and Social Q&A Contexts:** Roman-empire [36], Questions [36]

### Graph Classification Tasks:

- **Compounds Networks:** MUTAG, PTC-MR, BZR, COX2, DHFR, AIDS, NCI1, ogbg-molhiv, ogbg-molpcba [12, 22, 23, 39, 43, 46]
- **Protein Networks:** ENZYMES, DD, PROTEINS, ogbg-ppa [5, 14, 21, 23]
- **Movie Networks:** IMDB-BINARY, IMDB-MULTI [55]
- **Collaboration Networks:** COLLAB [27]
- **3D Shapes and Image Superpixels:** ShapeNet [58], MNISTSuperPixels [32]

#### Statistical Overview

**Table 2: Statistical Overview of Datasets for Node and Edge-Level Tasks in OpenGU Benchmarking**

| Datasets         | Nodes   | Edges      | Features | Classes | Type        | Description           |
|------------------|---------|------------|----------|---------|-------------|-----------------------|
| Cora             | 2,708   | 5,278      | 1,433    | 7       | Homophily   | Citation Network      |
| Citeseer         | 3,327   | 4,732      | 3,703    | 6       | Homophily   | Citation Network      |
| PubMed           | 19,717  | 44,338     | 500      | 3       | Homophily   | Citation Network      |
| DBLP             | 17,716  | 52,867     | 1,639    | 4       | Heterophily | Co-author Network     |
| ogbn-arxiv       | 169,343 | 1,166,243  | 128      | 40      | Homophily   | Citation Network      |
| CS               | 18,333  | 81,894     | 6,805    | 15      | Homophily   | Co-author Network     |
| Physics          | 34,493  | 247,962    | 8,415    | 5       | Homophily   | Co-author Network     |
| Photo            | 7,487   | 119,043    | 745      | 8       | Homophily   | Co-purchasing Network |
| Computers        | 13,381  | 245,778    | 767      | 10      | Homophily   | Co-purchasing Network |
| ogbn-products    | 2,449,029| 61,859,140 | 100      | 47      | Homophily   | Co-purchasing Network |
| Chameleon        | 2,277   | 36,101     | 2,325    | 5       | Heterophily | Wiki-page Network     |
| Squirrel         | 5,201   | 216,933    | 2,089    | 5       | Heterophily | Wiki-page Network     |
| Actor            | 7,600   | 29,926     | 931      | 5       | Heterophily | Actor Network         |
| Minesweeper      | 10,000  | 39,402     | 7        | 2       | Homophily   | Game Synthetic Network|
| Tolokers         | 11,758  | 519,000    | 10       | 2       | Homophily   | Crowd-sourcing Network|
| Roman-empire     | 22,662  | 32,927     | 300      | 18      | Heterophily | Article Syntax Network|
| Amazon-ratings   | 24,492  | 93,050     | 300      | 5       | Heterophily | Rating Network        |
| Questions        | 48,921  | 153,540    | 301      | 2       | Homophily   | Social Network        |
| Flickr           | 89,250  | 899,756    | 500      | 7       | Heterophily | Image Network         |

**Table 3: Statistical Overview of Datasets for Graph-Level Tasks in OpenGU Benchmarking**

| Datasets         | Graphs | Nodes   | Edges  | Features | Classes | Description           |
|------------------|--------|---------|--------|----------|---------|-----------------------|
| MUTAG            | 188    | 17.93   | 19.79  | 7        | 2       | Compounds Network     |
| PTC-MR           | 344    | 14.29   | 14.69  | 18       | 2       | Compounds Network     |
| BZR              | 405    | 35.75   | 38.36  | 56       | 2       | Compounds Network     |
| COX2             | 467    | 41.22   | 43.45  | 38       | 2       | Compounds Network     |
| DHFR             | 467    | 42.43   | 44.54  | 56       | 2       | Compounds Network     |
| AIDS             | 2,000  | 15.69   | 16.20  | 42       | 2       | Compounds Network     |
| NCI1             | 4,110  | 29.87   | 32.30  | 37       | 2       | Compounds Network     |
| ogbg-molhiv      | 41,127 | 25.50   | 27.50  | 9        | 2       | Compounds Network     |
| ogbg-molpcba     | 437,929| 26.00   | 28.10  | 9        | 2       | Compounds Network     |
| ENZYMES          | 600    | 32.63   | 62.14  | 21       | 6       | Protein Network       |
| DD               | 1,178  | 284.32  | 715.66 | 89       | 2       | Protein Network       |
| PROTEINS         | 1,113  | 39.06   | 72.82  | 4        | 2       | Protein Network       |
| ogbg-ppa         | 158,100| 243.40  |2,266.10|4        | 37      | Protein Network       |
| IMDB-BINARY      | 1,000  | 19.77   | 96.53  | degree  | 2       | Movie Network         |
| IMDB-MULTI       | 1,500  | 13.00   | 65.94  | degree  | 3       | Movie Network         |
| COLLAB           | 5,000  | 74.49   |2,457.78| degree | 3       | Collaboration Network |
| ShapeNet         | 16,881 | 2,616.20| KNN    | 3        | 50      | Point Cloud Network   |
| MNISTSuperPixels | 70,000 | 75.00   |1,393.03| 1       | 10      | Super-pixel Network   |

#### Data Preprocessing Enhancements

To achieve a standardized and versatile partitioning in OpenGU, we implemented code that allows arbitrary dataset split ratios, enabling researchers to customize partitions to suit their needs and experiment requirements. In addition to flexible splitting, we also consider label balance within class distributions by providing both balanced and random partitioning options. Furthermore, we introduce preprocessing enhancements that allow datasets to function under both transductive and inductive inference scenarios, permitting evaluations under various settings and offering a broader assessment of algorithm performance.

## Algorithm Framework

### GNN Backbones

To evaluate the generalizability of GU algorithms, we incorporate three predominant paradigms of GNN models within our benchmark:

1. **Traditional GNNs:**
   - **GCN (Graph Convolutional Network)**
   - **GAT (Graph Attention Network)** [45]
   - **GCNII** [6]
   - **GIN (Graph Isomorphism Network)** [54]
   - **Others** [2, 16, 20]

   These models represent a broad spectrum of architectural variations, providing a solid foundation for evaluating GU methods.

2. **Sampling GNNs:**
   - **GraphSAGE** [19]
   - **GraphSAINT** [61]
   - **ClusterGNN** [9]

   Sampling-based approaches offer scalability advantages by reducing computational overhead through node sampling techniques.

3. **Decoupled GNNs:**
   - **SGC (Simplified Graph Convolution)**
   - **SSGC (Simple Spectral Graph Convolution)** [64]
   - **SIGN (Scalable Inception Graph Neural Networks)** [18]
   - **APPNP (Approximate Personalized Propagation of Neural Predictions)** [25]

   These models decouple feature propagation and model training, enhancing scalability and efficiency, especially for larger datasets.

### GU Algorithms

Our framework encompasses **16 state-of-the-art GU algorithms**, each meticulously reproduced based on source code or detailed descriptions in the relevant publications. These algorithms are categorized as follows:

1. **Partition-based:**
   - **GraphEraser**
   - **GUIDE**
   - **GraphRevoker**

2. **IF-based (Influence Function-based):**
   - **GIF**
   - **CGU**
   - **CEU**
   - **GST**
   - **IDEA**
   - **ScaleGUN**

3. **Learning-based:**
   - **GNNDelete**
   - **MEGU**
   - **SGU**
   - **D2DGN**
   - **GUKD**

We aim to deliver a unified interface for these methods, merging them under a cohesive API to facilitate easier access, experimentation, and potential future expansion. By standardizing these methods within OpenGU, we provide a streamlined platform for researchers and practitioners to conduct robust and reproducible benchmarking studies.

## Evaluation Strategy

To provide a thorough assessment of GU algorithms in diverse real-world scenarios, our benchmark evaluation spans three critical dimensions tailored to GU contexts: **effectiveness**, **robustness**, and **efficiency**. Each dimension includes custom evaluation methods reflecting OpenGU’s mission to serve as a flexible, high-standard benchmark.

### Cross-over Design

In previous GU studies, node and feature unlearning typically align with node classification tasks, while edge unlearning is often evaluated in the context of link prediction. However, real-world applications frequently demand the removal of data in scenarios where unlearning requests and downstream tasks intersect. For instance, in a node classification task, it may be necessary to remove edges between nodes, effectively combining edge unlearning with a task traditionally associated with node unlearning. To address this gap, we designed cross-task evaluations in OpenGU, allowing us to measure GU algorithm performance in more complex, realistic scenarios where different unlearning types may apply across diverse downstream tasks. This approach provides a comprehensive and practical evaluation framework to assess the flexibility of GU algorithms in real-world applications.

### Effectiveness

For the effectiveness of GU algorithms within OpenGU, we conduct evaluations tailored to key downstream tasks while specifically examining GU’s performance on **Non-UE**.

- **Node Classification Tasks:**
  - **Metrics:** Accuracy, Precision, F1-score
  - **Purpose:** Gauge GU’s predictive capability on nodes that remain part of the graph, ensuring that the unlearning process does not degrade the model’s performance on retained data.

- **Link Prediction:**
  - **Metrics:** AUC-ROC
  - **Purpose:** Assess the model’s ability to correctly predict relationships between nodes post-unlearning, ensuring that the removal of specific edges does not adversely affect the model’s overall predictive performance.

- **Membership Inference Attack and Poisoning Attack:**
  - **Membership Inference Attack:** Determines whether specific nodes were included in the training data. An AUC-ROC close to 0.5 indicates minimal information leakage.
  - **Poisoning Attack:** Introduces mismatched or "poisoned" edges to degrade prediction performance, followed by an unlearning request to remove these edges. Improvement in link prediction performance post-removal validates the GU algorithm’s effectiveness in erasing unwanted relationships.

This multi-faceted approach ensures a comprehensive evaluation of both retained and unlearned information within OpenGU.

### Robustness

To evaluate the robustness of GU algorithms in OpenGU, we systematically examine model performance under varying levels of deletion intensity. This involves assessing how different proportions of data removal affect the model’s predictive capabilities. Robust GU algorithms should ideally demonstrate minimal performance degradation as deletion intensity increases, reflecting strong resilience in maintaining effective predictions for both retained and partially affected entities.

### Efficiency

In evaluating the efficiency of GU algorithms in OpenGU, we focus on **scalability**, **time complexity**, and **space complexity**:

- **Scalability:** Assesses each method’s adaptability to different dataset sizes, offering insight into performance stability across varying graph scales.
- **Time Complexity:** Includes both theoretical and empirical evaluation to understand computational demands.
- **Space Complexity:** Examines memory efficiency by measuring peak memory usage and storage requirements during unlearning, determining which algorithms are viable in resource-limited environments.

Together, these metrics provide a comprehensive view of each method’s suitability for real-time and scalable deployment.

## Installation

**Note:** OpenGU depends on several external libraries. To streamline the installation, OpenGU does **NOT** install these libraries for you. Please install them from the provided links before running OpenGU.

### **Dependencies:**
- **Python:** `3.8.0`
- **PyTorch:** `2.2.1`
- **TorchVision:** `0.17.1`
- **torch_scatter:** `2.1.2`
- **Scipy:** `1.10.1`
- **torch_sparse:** `0.6.18`
- **torch_geometric:** `2.6.1`
- **Matplotlib:** `3.7.5`
- **Scikit-learn:** `1.3.2`
- **OGB:** `1.3.6`
- **PyYAML:** `6.0.2`
- **DeepRobust:** `0.2.11`
- **Cupy:** Install via `pip install cupy-cuda12x`
- **Seaborn:** `0.13.2`
- **Munkres:** `1.1.4`
- **CVXPY:** `1.5.2`
- **PyMetis:** `2023.1.1`
- **IPDB:** `0.13.13`

### **Installing with Pip**
```bash
pip install opengu
```

### **Installation for Local Development:**
```bash
git clone https://github.com/OpenGU/OpenGU
cd opengu
pip install -e .
```

## Quick Start

You can use the command `python examples/example.py` or follow the steps below to get started quickly.

### **Step 1: Load Configuration**
```python
import opengu
conf = opengu.config.load_conf(method="method_name", dataset="dataset_name")
```

### **Step 2: Load Data**
```python
dataset = opengu.data.Dataset("dataset_name", n_splits=1, feat_norm=conf.dataset['feat_norm'])
```

### **Step 3: Build Model**
```python
solver = opengu.method.MethodSolver(conf, dataset)
```

### **Step 4: Training and Evaluation**
```python
exp = opengu.ExpManager(solver)
exp.run(n_runs=10)
```

## How to Contribute

We welcome contributions from the community to enhance OpenGU. Whether it's adding new methods, datasets, or improving documentation, your input is valuable.

### **Contributing Guidelines:**

1. **Fork the Repository:** Create a fork of the OpenGU repository on GitHub.
2. **Create a Branch:** Develop your feature or fix on a separate branch.
3. **Submit a Pull Request:** Once your changes are ready, submit a pull request for review.
4. **Report Issues:** If you encounter any issues or have suggestions, feel free to open an issue on GitHub.

Please ensure that your contributions adhere to the project's coding standards and include appropriate tests.

## Cite Us

If you use OpenGU in your research, please cite our paper:

```bibtex
@article{your2024opengu,
  title={OpenGU: An Open-Source Benchmark for Graph Unlearning},
  author={Your Name and Co-author's Name},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2024}
}
```

## Reference

| **ID** | **Paper**                                                                                                                                                                                               | **Method** | **Conference** |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------: | :------------: |
| 1      | [Semi-supervised classification with graph convolutional networks](https://arxiv.org/pdf/1609.02907.pdf)                                                                                             | GCN        | ICLR 2017      |
| 2      | [Learning Discrete Structures for Graph Neural Networks](https://arxiv.org/abs/1903.11960)                                                                                                              | LDS        | ICML 2019      |
| 3      | [Graph Structure Learning for Robust Graph Neural Networks](https://dl.acm.org/doi/pdf/10.1145/3394486.3403049)                                                                                         | ProGNN     | KDD 2020       |
| 4      | [Iterative Deep Graph Learning for Graph Neural Networks: Better and Robust Node Embeddings](https://proceedings.neurips.cc/paper/2020/file/e05c7ba4e087beea9410929698dc41a6-Paper.pdf)                 | IDGL       | NeurIPS 2020    |
| 5      | [Graph-Revised Convolutional Network](https://arxiv.org/pdf/1911.07123)                                                                                                                                 | GRCN       | ECML-PKDD 2020  |
| 6      | [Data Augmentation for Graph Neural Networks](https://ojs.aaai.org/index.php/AAAI/article/view/17315/17122)                                                                                             | GAug(O)    | AAAI 2021       |
| 7      | [SLAPS: Self-Supervision Improves Structure Learning for Graph Neural Networks](https://proceedings.neurips.cc/paper/2021/file/bf499a12e998d178afd964adf64a60cb-Paper.pdf)                              | SLAPS      | ICML 2021       |
| 8      | [Variational Inference for Training Graph Neural Networks in Low-Data Regime through Joint Structure-Label Estimation](https://dl.acm.org/doi/abs/10.1145/3534678.3539283)                              | WSGNN      | KDD 2022        |
| 9      | [Nodeformer: A scalable graph structure learning transformer for node classification](https://proceedings.neurips.cc/paper_files/paper/2022/file/af790b7ae573771689438bbcfc5933fe-Paper-Conference.pdf) | Nodeformer | NeurIPS 2022    |
| 10     | [Graph Structure Estimation Neural Networks](http://shichuan.org/doc/103.pdf)                                                                                                                           | GEN        | WWW 2021        |
| 11     | [Compact Graph Structure Learning via Mutual Information Compression](https://arxiv.org/pdf/2201.05540)                                                                                                 | CoGSL      | WWW 2022        |
| 12     | [SE-GSL: A General and Effective Graph Structure Learning Framework through Structural Entropy Optimization](https://arxiv.org/pdf/2303.09778)                                                          | SEGSL      | WWW 2023        |
| 13     | [Towards Unsupervised Deep Graph Structure Learning](https://arxiv.org/pdf/2201.06367)                                                                                                                  | SUBLIME    | WWW 2022        |
| 14     | [Reliable Representations Make A Stronger Defender: Unsupervised Structure Refinement for Robust GNN](https://dl.acm.org/doi/pdf/10.1145/3534678.3539484)                                               | STABLE     | KDD 2022        |
| 15     | [Semi-Supervised Learning With Graph Learning-Convolutional Networks](https://ieeexplore.ieee.org/document/8953909/authors#authors)                                                                     | GLCN       | CVPR 2019        |
| 16     | [Block Modeling-Guided Graph Convolutional Neural Networks](http://arxiv.org/abs/2112.13507)                                                                                                            | BM-GCN     | AAAI 2022        |