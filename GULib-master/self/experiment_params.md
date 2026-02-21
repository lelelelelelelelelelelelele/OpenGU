# Phase B 实验参数规范

## k 值（遗忘节点数）

- 计算方式：`k = int(num_nodes * unlearn_ratio)`
- 候选集：`train_mask` 子集（非全体节点），因为 unlearning 只针对训练数据
- 各数据集 k 值参考（unlearn_ratio=0.05）：

| 数据集 | N_train (约) | k (ratio=0.05) |
|--------|-------------|----------------|
| Cora | 1,700 | ~135 |
| Citeseer | 2,100 | ~105 |
| PubMed | 12,500 | ~625 |
| Chameleon | 1,400 | ~70 |

## MC 模拟参数

- `mc_rounds`: 100（im_strategy.py 默认）
- `propagation_prob`: 0.1（IC 模型每条边传播概率）

## Phase B 实验矩阵

- **数据集**: Cora, Citeseer, PubMed, Chameleon（4 个）
- **攻击策略**: random, degree, pagerank, tracin, im, hybrid（6 个）
- **遗忘方法**: GNNDelete, GIF, GraphEraser（3 个）
- **重复**: ≥5 seeds
- **总实验数**: 4 × 6 × 3 × 5 = 360 runs

## CELF 在各数据集的开销估算

当前 mc_rounds=100, 纯 Python BFS vs numba 加速后预估：

| 数据集 | N_train (候选集) | Edges | k (ratio=0.05) | 纯 Python 预估 | Numba 预估 |
|--------|-----------------|-------|-----------------|----------------|-----------|
| Cora | 1,700 | 5,278 | 135 | ~2 min | ~5 sec |
| Citeseer | 2,100 | 4,732 | 105 | ~2 min | ~5 sec |
| PubMed | 12,500 | 44,338 | 625 | ~2 hours | ~5 min |
| Chameleon | 1,400 | 36,101 | 70 | ~11 min | ~30 sec |

## 大规模图注意事项

- ogbn-arxiv（107k train nodes）即使 numba 加速后 CELF step1 仍不可行
- 对 ogbn-arxiv 级别的图，需使用 `candidate_fraction`（建议 0.1-0.3）裁剪候选集
- Phase B 目标数据集在 numba 加速后均可在分钟级完成
