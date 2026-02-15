# OpenGU - Graph Unlearning Library

## Quick Start

```bash
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
```

## How to Change Parameters

### 1. Change Dataset (`--dataset_name`)

```bash
# Citation Networks
python main.py --cuda 0 --dataset_name citeseer --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

python main.py --cuda 0 --dataset_name pubmed --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
```

Available datasets:

| Category | Datasets |
|----------|----------|
| Citation Networks | cora, citeseer, pubmed |
| Co-authorship | CS, Physics, DBLP |
| E-commerce/Social | flickr, Photo, Computers, Amazon-ratings |
| Heterophilous | Squirrel, Chameleon, Actor, Minesweeper, Tolokers, Roman-empire, Questions |
| OGB (Node) | ogbn-arxiv, ogbn-products |
| OGB (Link) | ogbl |
| Molecular/Graph | MUTAG, COX2, AIDS, BZR, DD, PROTEINS, ENZYMES, DHFR, NCI1, PTC_MR |
| OGB (Graph) | ogbg-molhiv, ogbg-molpcba, ogbg-ppa |
| Other | MNISTSuperpixels, ShapeNet, IMDB-BINARY, IMDB-MULTI |

### 2. Change Unlearning Method (`--unlearning_methods`)

```bash
# Use GIF
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GIF --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Use MEGU
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods MEGU --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Use GNNDelete
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GNNDelete --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
```

Available methods: `GraphEraser`, `GUIDE`, `GNNDelete`, `CEU`, `GIF`, `SGU`, `CGU`, `GST`, `Projector`, `MEGU`, `GraphRevoker`, `UTU`, `GUKD`, `D2DGN`, `IDEA`, `ScaleGUN`

### 3. Change Base Model (`--base_model`)

```bash
# Use GAT
python main.py --cuda 0 --dataset_name cora --base_model GAT --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Use SAGE
python main.py --cuda 0 --dataset_name cora --base_model SAGE --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
```

Available models: `GCN`, `GAT`, `GIN`, `SAGE`, `SGC`, `S2GC`, `SIGN`, `Cheb`, `APPNP`, `GCN2`, `GATv2`, `TAG`, `LightGCN`, `GST`, `Cluster_GCN`, `SAINT`

### 4. Change Unlearning Target (`--unlearn_task`)

```bash
# Node unlearning (default)
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

# Edge unlearning
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task edge --downstream_task node --num_epochs 100 --batch_size 64

# Feature unlearning
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task feature --downstream_task node --num_epochs 100 --batch_size 64
```

### 5. Control How Many Nodes/Edges to Unlearn

```bash
# Unlearn specific number of nodes
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64 --num_unlearned_nodes 100

# Unlearn by proportion (10% of nodes)
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64 --proportion_unlearned_nodes 0.1

# Unlearn edges by proportion (10% of edges)
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task edge --downstream_task node --num_epochs 100 --batch_size 64 --proportion_unlearned_edges 0.1

# General unlearn ratio
python main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64 --unlearn_ratio 0.2
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--num_unlearned_nodes` | 270 | Absolute number of nodes to unlearn |
| `--proportion_unlearned_nodes` | 0.1 | Proportion of nodes to unlearn |
| `--proportion_unlearned_edges` | 0.1 | Proportion of edges to unlearn |
| `--unlearn_ratio` | 0.1 | General unlearning ratio |

### 6. Change Downstream Task (`--downstream_task`)

```bash
# Node classification
--downstream_task node

# Link prediction
--downstream_task edge

# Graph classification (for graph-level datasets)
--downstream_task graph
```

## Other Useful Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--cuda` | 3 | GPU device ID |
| `--num_epochs` | 100 | Training epochs |
| `--batch_size` | 1024 | Batch size |
| `--train_ratio` | 0.8 | Training set ratio |
| `--test_ratio` | 0.2 | Test set ratio |
| `--is_transductive` | True | Transductive or inductive setting |
| `--is_balanced` | False | Balanced class distribution |
| `--num_runs` | 1 | Number of experiment runs |
| `--cal_mem` | False | Enable memory profiling |

## Combined Example

```bash
# Use pubmed dataset + GAT model + MEGU method + edge unlearning + unlearn 20% edges
python main.py --cuda 0 --dataset_name pubmed --base_model GAT --unlearning_methods MEGU --unlearn_task edge --downstream_task node --num_epochs 200 --batch_size 128 --proportion_unlearned_edges 0.2
```

All parameters are defined in `parameter_parser.py`.
