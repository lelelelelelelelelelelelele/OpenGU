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
For detailed statistics on the datasets used in our evaluation, see the following files:

- [Node and Edge-Level Tasks Statistics](/Resources/graph_classification_stats.md)
- [Graph Classification Tasks Statistics](/Resources/graph_classification_stats.md)

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
| 🔸 **GraphEraser**  | 🔹 **GIF**       | 🔸 **GNNDelete**    | 🔹 **UtU**          |
| 🔸 **GUIDE**         | 🔹 **CGU**       | 🔸 **MEGU**         | 🔹 **Projector**    |
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


## <span id="installation">📥 Installation</span>

### **Prerequisites**

- **Python**: 3.8.0

### **Step 1: Create and Activate a Virtual Environment**

It is recommended to use a virtual environment to manage dependencies and avoid conflicts with other projects. You can create a virtual environment using either `venv` or `conda`.

#### Using `venv`

1. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**

    - **Windows**

        ```bash
        venv\Scripts\activate
        ```

    - **Unix or MacOS**

        ```bash
        source venv/bin/activate
        ```

#### Using `conda`

1. **Create a Virtual Environment**

    ```bash
    conda create -n myenv python=3.8
    ```

2. **Activate the Virtual Environment**

    ```bash
    conda activate myenv
    ```

### **Step 2: Install OpenGU**

You can install OpenGU using one of the following methods:

#### 1. **Using Pip**

TODO: To install OpenGU directly from PyPI:

```bash
pip install opengu
```

#### 2. **Installing from GitHub for Local Development**

TODO: To install OpenGU for local development, clone the GitHub repository and install it from the source:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/bwfan-bit/OpenGU.git
    cd OpenGU
    ```

2. **Install OpenGU in Editable Mode**

    ```bash
    pip install -e .
    ```

### **Step 3: Installing Dependencies**

#### General Dependencies

Install the general dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

#### CUDA-Specific Dependencies

For GPU support, install the appropriate versions of PyTorch, CuPy, and related libraries that match your CUDA version.

1. **Install PyTorch and torchvision with CUDA Support**

   Example for CUDA 12.1 (PyTorch version 2.2.1 and torchvision version 0.17.1):

   ```bash
   pip install torch==2.2.1 torchvision==0.17.1 torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

2. **Install CuPy with CUDA Support**

   Example for CUDA 12.x:

   ```bash
   pip install cupy-cuda12x
   ```

*Ensure your system has the appropriate CUDA version installed. For more information, refer to the [CuPy Installation Guide](https://docs.cupy.dev/en/stable/install.html#using-pip).*

### **Verify Installation**

After installation, verify that OpenGU is installed correctly by running:

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

#### General Dependencies
You can install the general dependencies using `pip`:

```bash
pip install -r requirement.txt
```
#### CUDA-Specific Dependencies
For CUDA-specific dependencies, refer to the detailed instructions in the [Installation section](#installation)  above.

### **Step 3: Run the Main Script**

After installing the dependencies, you can run the main script using the following command:

```bash
python main.py --cuda 0 --dataset_name <dataset_name> --base_model <base_model> --unlearning_methods <unlearning_methods> --unlearn_task <unlearn_task> --downstream_task <downstream_task> --num_epochs 100 --batch_size 64
```

#### Optional arguments:

### **Step 3: Run the Main Script**

After installing the dependencies, you can run the main script using the following command:

```bash
python GULib-master/main.py --cuda 0 --dataset_name <dataset_name> --base_model <base_model> --unlearning_methods <unlearning_methods> --unlearn_task <unlearn_task> --downstream_task <downstream_task> --num_epochs 100 --batch_size 64
```


#### Optional arguments:

- `--cuda <cuda_device>`: Specify which GPU to use. Replace `<cuda_device>` with the desired GPU number.
- `--dataset_name <dataset_name>`: The name of the graph dataset. Replace `<dataset_name>` with a dataset from the list: `cora`, `citeseer`, `pubmed`, `CS`, `Physics`, `flickr`, `ppi`, `Photo`, `Computers`, `DBLP`, `ogbl`, `ogbn-arxiv`, `ogbn-products`.
- `--base_model <base_model>`: The model architecture to use. Options include `GCN`, `GAT`, `GIN`, `SAGE`, `MLP`, etc.
- `--unlearning_methods <unlearning_methods>`: The unlearning method to use. Choose from `GraphEraser`, `GUIDE`, `CEU`, etc.
- `--unlearn_task <unlearn_task>`: The type of unlearning task. Options are `feature`, `node`, and `edge`.
- `--downstream_task <downstream_task>`: The type of downstream task. Options are `node` and `edge`.
- `--num_epochs <num_epochs>`: Number of epochs to run.
- `--batch_size <batch_size>`: The batch size to use.

Note that the above list includes only a subset of the available parameters. For more parameters and their descriptions, please refer to the `GULib-master/parameter_parser.py` file. 

### Example Command:

To run the **GCN** model using **GraphEraser** for **node-level unlearning** and **node-level downstream tasks**, you can run the following command:

```bash
python GULib-master/main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
```

This command will:
- Use the **GCN** model
- Apply **GraphEraser** as the unlearning method
- Perform **node-level unlearning** and **node-level downstream tasks**
- Use the **cora** dataset
- Train for **100 epochs** with a **batch size of 64**


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
