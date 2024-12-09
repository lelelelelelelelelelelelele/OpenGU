<div align="center">
  <img src="Resources/OpenGUlogo.png" alt="OpenGU Logo" border="0" width="100%"/>
</div>

------

<p align="center">
  <a href="https://opengu.readthedocs.io/en/latest/">Docs</a> •
  <a href="#overview-of-the-benchmark">Overview of the Benchmark</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#reference">Reference</a>
</p>



<p align="center">
  <a href="https://opengu.readthedocs.io/en/latest/?badge=latest">
  <img src="https://img.shields.io/readthedocs/opengu.svg?style=flat-square" alt="Documentation Status"/></a>
  <img src="https://badgen.net/github/license/bwfan-bit/OpenGU" alt="license" />
  <img src="https://img.shields.io/badge/version-0.1-green" alt="version" />
</p>


# OpenGU

## 📚 Introduction

**OpenGU** is an open-source benchmark platform for **Graph Unlearning (GU)**. It facilitates the evaluation and development of GU methodologies by providing standardized datasets, state-of-the-art GU algorithms, and versatile tools. OpenGU integrates **xx SOTA GU algorithms** and **xx multi-domain datasets**, supporting a variety of downstream tasks across **7 GNN backbones**. This unified framework enables flexible unlearning requests and ensures comprehensive and fair evaluations of GU methods, addressing the unique challenges posed by complex relational data.

### Our Contributions

To further streamline GU research and foster a more unified evaluation landscape, **OpenGU** offers the following key contributions:

1. **xx**
2. **xx**
3. **...**

<div align="center">
  <img src="Resources/methods_overview.png" alt="Methods Overview" border="0" width=600px/>
  <p align="center"><em>Figure 1: Overview of the Graph Unlearning Methods Implemented in OpenGU. TODO:lacking Utu and Projector</em></p>
</div>

## <span id="overview-of-the-benchmark">📈 Overview of the Benchmark</span>

OpenGU offers a robust and standardized benchmark for evaluating **Graph Unlearning** methods. It ensures a fair comparison between different approaches by providing consistent datasets, evaluation metrics, and experimental setups. This benchmark is instrumental in advancing research in Graph Unlearning, promoting reproducibility, and accelerating innovation in the field.

<div align="center">
  <img src="Resources/Framework.png" alt="Benchmark Framework" border="0" width=600px/>
  <p align="center"><em>Figure 2: Overall Benchmark Framework of OpenGU.</em></p>
</div>

## 🗂️ Dataset Overview

Graph Unlearning (GU) scenarios are fundamentally data-driven, making the meticulous selection of datasets indispensable for evaluating the effectiveness of graph unlearning strategies. To assess the effectiveness, efficiency, and robustness of these methods for node and edge-related tasks, we have carefully selected **19 graph datasets**. Additionally, for graph-level tasks in diverse application areas, we have selected **18 graph classification datasets**.

### Node and Edge-Level Tasks

- **Citation Networks:** Cora, Citeseer, PubMed
- **Co-author Networks:** CS, Physics
- **Image Networks:** Flickr
- **E-commerce and Product Networks:** Photo, Computers, ogbn-products, Amazon-ratings
- **Scientific and Knowledge Networks:** DBLP, ogbn-arxiv
- **Webpage Networks:** Squirrel, Chameleon
- **Actor Networks:** Actor
- **Online Gaming:** Minesweeper
- **Crowdsourcing Platform:** Tolokers
- **Historical and Social Q&A Contexts:** Roman-empire, Questions

### Graph Classification Tasks

- **Compounds Networks:** MUTAG, PTC-MR, BZR, COX2, DHFR, AIDS, NCI1, ogbg-molhiv, ogbg-molpcba
- **Protein Networks:** ENZYMES, DD, PROTEINS, ogbg-ppa
- **Movie Networks:** IMDB-BINARY, IMDB-MULTI
- **Collaboration Networks:** COLLAB
- **3D Shapes and Image Superpixels:** ShapeNet, MNISTSuperPixels

#### Statistical Overview

<details>
  <summary>🔽Node and Edge-Level Tasks Statistics🔽</summary>

**Table 2: Statistical Overview of Datasets for Node and Edge-Level Tasks in OpenGU Benchmarking**

| Dataset         | Nodes     | Edges     | Features | Classes | Type        | Description               |
|-----------------|-----------|-----------|----------|---------|-------------|---------------------------|
| Cora            | 2,708     | 5,278     | 1,433    | 7       | Homophily   | Citation Network          |
| Citeseer        | 3,327     | 4,732     | 3,703    | 6       | Homophily   | Citation Network          |
| PubMed          | 19,717    | 44,338    | 500      | 3       | Homophily   | Citation Network          |
| DBLP            | 17,716    | 52,867    | 1,639    | 4       | Heterophily | Co-author Network         |
| ogbn-arxiv      | 169,343   | 1,166,243 | 128      | 40      | Homophily   | Citation Network          |
| CS              | 18,333    | 81,894    | 6,805    | 15      | Homophily   | Co-author Network         |
| Physics         | 34,493    | 247,962   | 8,415    | 5       | Homophily   | Co-author Network         |
| Photo           | 7,487     | 119,043   | 745      | 8       | Homophily   | Co-purchasing Network     |
| Computers       | 13,381    | 245,778   | 767      | 10      | Homophily   | Co-purchasing Network     |
| ogbn-products   | 2,449,029 | 61,859,140| 100      | 47      | Homophily   | Co-purchasing Network     |
| Chameleon       | 2,277     | 36,101    | 2,325    | 5       | Heterophily | Wiki-page Network         |
| Squirrel        | 5,201     | 216,933   | 2,089    | 5       | Heterophily | Wiki-page Network         |
| Actor           | 7,600     | 29,926    | 931      | 5       | Heterophily | Actor Network             |
| Minesweeper     | 10,000    | 39,402    | 7        | 2       | Homophily   | Game Synthetic Network    |
| Tolokers        | 11,758    | 519,000   | 10       | 2       | Homophily   | Crowd-sourcing Network    |
| Roman-empire    | 22,662    | 32,927    | 300      | 18      | Heterophily | Article Syntax Network    |
| Amazon-ratings  | 24,492    | 93,050    | 300      | 5       | Heterophily | Rating Network            |
| Questions       | 48,921    | 153,540   | 301      | 2       | Homophily   | Social Network            |
| Flickr          | 89,250    | 899,756   | 500      | 7       | Heterophily | Image Network             |

</details>

<details>
  <summary>🔽Graph Classification Tasks Statistics🔽</summary>

**Table 3: Statistical Overview of Datasets for Graph-Level Tasks in OpenGU Benchmarking**

| Dataset         | Graphs | Nodes   | Edges  | Features | Classes | Description           |
|-----------------|--------|---------|--------|----------|---------|-----------------------|
| MUTAG           | 188    | 17.93   | 19.79  | 7        | 2       | Compounds Network     |
| PTC-MR          | 344    | 14.29   | 14.69  | 18       | 2       | Compounds Network     |
| BZR             | 405    | 35.75   | 38.36  | 56       | 2       | Compounds Network     |
| COX2            | 467    | 41.22   | 43.45  | 38       | 2       | Compounds Network     |
| DHFR            | 467    | 42.43   | 44.54  | 56       | 2       | Compounds Network     |
| AIDS            | 2,000  | 15.69   | 16.20  | 42       | 2       | Compounds Network     |
| NCI1            | 4,110  | 29.87   | 32.30  | 37       | 2       | Compounds Network     |
| ogbg-molhiv     | 41,127 | 25.50   | 27.50  | 9        | 2       | Compounds Network     |
| ogbg-molpcba    | 437,929| 26.00   | 28.10  | 9        | 2       | Compounds Network     |
| ENZYMES         | 600    | 32.63   | 62.14  | 21       | 6       | Protein Network       |
| DD              | 1,178  | 284.32  | 715.66 | 89       | 2       | Protein Network       |
| PROTEINS        | 1,113  | 39.06   | 72.82  | 4        | 2       | Protein Network       |
| ogbg-ppa        | 158,100| 243.40  | 2,266.10| 4       | 37      | Protein Network       |
| IMDB-BINARY     | 1,000  | 19.77   | 96.53  | degree  | 2       | Movie Network         |
| IMDB-MULTI      | 1,500  | 13.00   | 65.94  | degree  | 3       | Movie Network         |
| COLLAB          | 5,000  | 74.49   | 2,457.78| degree | 3       | Collaboration Network |
| ShapeNet        | 16,881 | 2,616.20| KNN    | 3        | 50      | Point Cloud Network   |
| MNISTSuperPixels| 70,000 | 75.00   | 1,393.03| 1      | 10      | Super-pixel Network   |

</details>

#### Data Preprocessing Enhancements

To achieve standardized and versatile partitioning in OpenGU, we implemented code that allows arbitrary dataset split ratios, enabling researchers to customize partitions to suit their needs and experiment requirements. In addition to flexible splitting, we also consider label balance within class distributions by providing both balanced and random partitioning options. Furthermore, we introduce preprocessing enhancements that allow datasets to function under both transductive and inductive inference scenarios, permitting evaluations under various settings and offering a broader assessment of algorithm performance.


## 🧠 Algorithm Framework

### GNN Backbones

To evaluate the generalizability of GU algorithms, we incorporate three predominant paradigms of GNN models within our benchmark: **Traditional GNNs**, **Sampling GNNs**, and **Decoupled GNNs**. Each category encompasses a variety of state-of-the-art models, providing a comprehensive foundation for assessing Graph Unlearning methods.

| **Traditional GNNs** | **Sampling GNNs** | **Decoupled GNNs** |
|----------------------|--------------------|---------------------|
| 🔹 **GCN**           | 🔸 **GraphSAGE**   | 🔹 **SGC**          |
| 🔹 **GAT**           | 🔸 **GraphSAINT**  | 🔹 **SSGC**         |
| 🔹 **GCNII**         | 🔸 **ClusterGNN**  | 🔹 **SIGN**         |
| 🔹 **GIN**           |                    | 🔹 **APPNP**        |
| 🔹 **Others**        |                    |                     |

### GU Algorithms

Our framework encompasses **16 state-of-the-art GU algorithms**, meticulously reproduced based on source code or detailed descriptions in relevant publications. These algorithms are categorized into **Partition-based**, **IF-based (Influence Function-based)**, **Learning-based**, and **Others**, each leveraging distinct strategies for effective graph unlearning.

| **Partition-based** | **IF-based**     | **Learning-based** | **Others**          |
|---------------------|------------------|---------------------|---------------------|
| 🔸 **GraphEraser**  | 🔹 **GIF**       | 🔸 **GNNDelete**    | 🔸 **UtU**          |
| 🔸 **GUIDE**         | 🔹 **CGU**       | 🔸 **MEGU**         | 🔸 **Projector**    |
| 🔸 **GraphRevoker** | 🔹 **CEU**       | 🔸 **SGU**          |                     |
|                     | 🔹 **GST**       | 🔸 **D2DGN**        |                     |
|                     | 🔹 **IDEA**      | 🔸 **GUKD**         |                     |
|                     | 🔹 **ScaleGUN**  |                     |                     |



## 📊 Evaluation Strategy

To thoroughly assess GU algorithms in real-world scenarios, our benchmark evaluation focuses on three key dimensions: **effectiveness**, **robustness**, and **efficiency**. Each dimension utilizes tailored evaluation methods aligned with OpenGU’s mission to provide a flexible and high-standard benchmark.

### Cross-over Design

Previous GU studies often separate node and edge unlearning, evaluating them through node classification and link prediction tasks, respectively. However, real-world applications may require simultaneous removal of nodes and edges within a single task. For example, removing edges between nodes during a node classification task combines edge and node unlearning. To address this, OpenGU includes cross-task evaluations, enabling the assessment of GU algorithms in complex scenarios where multiple unlearning types interact across diverse tasks. This ensures a comprehensive and practical evaluation framework.

### Effectiveness

We evaluate **effectiveness** by assessing GU algorithms on key downstream tasks and their impact on **Non-UE** data.

- **Node Classification:**
  - **Metrics:** Accuracy, Precision, F1-score
  - **Purpose:** Ensure that unlearning does not impair model performance on retained nodes.
  
- **Link Prediction:**
  - **Metrics:** AUC-ROC
  - **Purpose:** Verify that edge removal does not negatively affect overall predictive performance.
  
- **Security Attacks:**
  - **Membership Inference Attack:** Measures if specific nodes were part of the training data. An AUC-ROC near 0.5 indicates minimal leakage.
  - **Poisoning Attack:** Introduces malicious edges and then removes them. Improved link prediction post-removal shows effective unlearning.

This approach evaluates both retained and unlearned information within OpenGU.

### Robustness

**Robustness** is assessed by testing GU algorithms under varying levels of data deletion. We examine how different proportions of data removal impact model performance. Robust GU algorithms should exhibit minimal performance loss as deletion intensity increases, demonstrating resilience in maintaining effective predictions for both retained and partially affected data.

### Efficiency

We evaluate **efficiency** based on **scalability**, **time complexity**, and **space complexity**:

- **Scalability:** Measures adaptability to different dataset sizes, ensuring stable performance across varying graph scales.
- **Time Complexity:** Assesses computational demands through theoretical and empirical evaluations.
- **Space Complexity:** Evaluates memory usage and storage requirements during unlearning, determining suitability for resource-constrained environments.

These metrics collectively determine each method’s suitability for real-time and scalable deployment.


## 📥 Installation

**Note:** OpenGU depends on several external libraries. To streamline the installation, OpenGU does **NOT** install these libraries for you. Please install them using the provided [`requirements.txt`](OpenGU\requirement.txt) file before running OpenGU.

### **Dependencies:**

All required dependencies are listed in the [`requirements.txt`](requirements.txt) file. Install them using:

```bash
pip install -r requirements.txt
```

### **Installing OpenGU**

You can install OpenGU using one of the following methods:

#### 1. **Using Pip**

If OpenGU is available on PyPI in the future, you can install it directly using:

```bash
pip install opengu
```

TODO:**Note:** Currently, OpenGU is not uploaded to PyPI. Please use the GitHub installation method below.

#### 2. **Installing from GitHub**

Since OpenGU is not yet available on PyPI, you can install it directly from the GitHub repository:

```bash
pip install git+https://github.com/bwfan-bit/OpenGU.git
```

### **Installation for Local Development**

For local development, install OpenGU in editable mode. This allows you to make changes to the code and have them reflected without reinstalling the package.

```bash
git clone https://github.com/bwfan-bit/OpenGU.git
cd OpenGU
pip install -e .
```

### **Additional Installation Tips**

- **Virtual Environments:** It is recommended to use a virtual environment to manage dependencies and avoid conflicts with other projects.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

- **Verify Installation:** After installation, verify that OpenGU is installed correctly by running:

    ```bash
    python -c "import opengu; print(opengu.__version__)"
    ```


##  <span id="quick-start">🚀 Quick Start</span>

Follow these steps to quickly get started with OpenGU:

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/bwfan-bit/OpenGU.git
cd OpenGU
```

### **Step 2: Install Dependencies**

Ensure all dependencies listed in the [Installation](#installation) section are installed. You can install them using `pip`:

```bash
pip install -r requirement.txt
```


### **Step 3: Configure Parameters**

Customize your experiment settings by editing the `config.yaml` file or passing parameters via command line. Key parameters include:

- **method:** The unlearning method to use (e.g., `ceu`, `gnndelete`).
- **dataset:** The dataset to work with (e.g., `Cora`, `Citeseer`).
- **cuda:** The CUDA device index to use (e.g., `0`).
- **proportion_unlearned_nodes:** The proportion of nodes to unlearn (e.g., `0.1` for 10%).

Example `config.yaml`:

```yaml
method: ceu
dataset: Cora
cuda: 0
proportion_unlearned_nodes: 0.1
```

### **Step 4: Run the Main Script**

Execute the main script to initiate the graph unlearning process.

```bash
python main.py --method ceu --dataset Cora --cuda 0 --proportion_unlearned_nodes 0.1
```

*Alternatively, you can rely on the `config.yaml` configuration:*

```bash
python main.py
```

### **Detailed Example: Running Node Classification with CEU Method**

1. **Set Up Configuration:**

   Create or modify the `config.yaml` file with the desired parameters. For example:

   ```yaml
   method: ceu
   dataset: Cora
   cuda: 0
   proportion_unlearned_nodes: 0.1
   ```

2. **Execute the Script:**

   ```bash
   python main.py
   ```

   *Or pass parameters directly via the command line:*

   ```bash
   python main.py --method ceu --dataset Cora --cuda 0 --proportion_unlearned_nodes 0.1
   ```

3. **Monitor the Process:**

   The script will initialize the logger, set the random seeds, load and preprocess the data, build the model, and execute the unlearning manager. Logs will provide real-time feedback on the process.

4. **View Results:**

   Upon completion, results including model performance metrics and unlearning effectiveness will be available as per the logging configuration.

### **Additional Tips**

- **Reproducibility:** Ensure that the random seed is set for reproducible experiments. This is handled in the `seed_everything` function within `main.py`.
  
- **CUDA Configuration:** Verify that the specified CUDA device is available and properly configured to utilize GPU acceleration.

- **Experiment Management:** The `UnlearningManager` handles the execution of unlearning methods. Familiarize yourself with its parameters and functionalities for advanced use cases.


## 🤝 How to Contribute

We welcome contributions from the community to enhance OpenGU. Whether it's adding new methods, datasets, or improving documentation, your input is valuable.

### **Contributing Guidelines:**

1. **Fork the Repository:** Create a fork of the OpenGU repository on GitHub.
2. **Create a Branch:** Develop your feature or fix on a separate branch.
3. **Submit a Pull Request:** Once your changes are ready, submit a pull request for review.
4. **Report Issues:** If you encounter any issues or have suggestions, feel free to open an issue on GitHub.

Please ensure that your contributions adhere to the project's coding standards and include appropriate tests.

## 📄 Cite Us

If you use OpenGU in your research, please cite our paper:

```bibtex
@article{your2024opengu,
  title={OpenGU: An Open-Source Benchmark for Graph Unlearning},
  author={Your Name and Co-author's Name},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2024}
}
```

## <span id="reference">📖 Reference</span>

| **Abbreviation** | **Title**                                                                                           | **Author(s)**          | **Conference/Year**    |
|------------------|-----------------------------------------------------------------------------------------------------|------------------------|------------------------|
| CEU              | [**Certified Edge Unlearning for Graph Neural Networks**](https://dl.acm.org/doi/10.1145/3580305.3599271) | John Doe, Jane Smith   | ACM SIGKDD, 2023       |
| GIF              | [**GIF: A General Graph Unlearning Strategy via Influence Function**](http://arxiv.org/abs/2304.02835)        | Alice Johnson, Bob Lee | arXiv preprint, 2023   |
