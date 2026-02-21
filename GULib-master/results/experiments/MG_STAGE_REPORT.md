# MG 实验阶段报告

> 日期: 2026-02-21
> 状态: 接近完成 (MG-0 缺 2 个实验)

---

## 实验完成情况

| 实验 | Dataset | Model | Methods | Seeds | 状态 |
|------|---------|-------|---------|-------|------|
| MG-0 | Cora | GCN | GIF,GNNDelete,GraphEraser,GUIDE | 5 | 🔄 缺 2 个 |
| MG-1 | Citeseer | GCN | GIF,GNNDelete,GraphEraser | 5 | ✅ 完成 |
| MG-2 | Cora | GAT | GIF,GNNDelete,GraphEraser | 5 | ✅ 完成 |
| MG-3a | Citeseer | GCN | IDEA,MEGU | 5 | ✅ 完成 |
| MG-3b | Cora | GAT | IDEA,MEGU | 5 | ✅ 完成 |

---

## 待补跑

- **MG-0 seed 2024**: GIF, GNNDelete (6 strategies each)

---

## 结果目录

```
results/experiments/
├── phase_a/                    # MG-0: Cora/GCN (4 methods × 5 seeds)
├── mg1_citeseer/phase_a/       # MG-1: Citeseer/GCN (3 methods × 5 seeds)
├── mg2_gat/phase_a/            # MG-2: Cora/GAT (3 methods × 5 seeds)
├── mg3_citeseer/phase_a/       # MG-3a: Citeseer IDEA/MEGU (2 methods × 5 seeds)
└── mg3_gat/phase_a/            # MG-3b: GAT IDEA/MEGU (2 methods × 5 seeds)
```

---

## 下一步

1. 补跑 MG-0 seed 2024 的 GIF/GNNDelete
2. 生成汇总统计表 (mean ± std)
3. 绘制泛化性图表
