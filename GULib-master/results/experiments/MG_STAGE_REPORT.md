# MG 实验阶段报告

> 日期: 2026-02-21
> 状态: 接近完成 (MG-0 缺 1 个实验)

---

## 实验完成情况

| 实验 | Dataset | Model | Methods | Seeds | 状态 |
|------|---------|-------|---------|-------|------|
| MG-0 | Cora | GCN | GIF,GNNDelete,GraphEraser,GUIDE | 5 | 🔄 缺 1 个 |
| MG-1 | Citeseer | GCN | GIF,GNNDelete,GraphEraser | 5 | ✅ 完成 |
| MG-2 | Cora | GAT | GIF,GNNDelete,GraphEraser | 5 | ✅ 完成 |
| MG-3a | Citeseer | GCN | IDEA,MEGU | 5 | ✅ 完成 |
| MG-3b | Cora | GAT | IDEA,MEGU | 5 | ✅ 完成 |

### MG-0 详细状态 (Cora/GCN)

| Seed | GIF | GNNDelete | GraphEraser | GUIDE |
|------|-----|-----------|-------------|-------|
| 42 | ✅ | ✅ | ✅ | ✅ |
| 212 | ✅ | ✅ | ✅ | ❌ |
| 722 | ✅ | ✅ | ✅ | ✅ |
| 1337 | ✅ | ✅ | ✅ | ✅ |
| 2024 | ✅ | ✅ | ✅ | ✅ |

---

## 待补跑

- **MG-0 seed 212**: GUIDE (6 strategies)

---

## 结果目录

```
results/experiments/
├── mg0_completion/phase_a/     # MG-0: Cora/GCN (4 methods × 5 seeds)
├── mg1_citeseer/phase_a/       # MG-1: Citeseer/GCN (3 methods × 5 seeds)
├── mg2_gat/phase_a/            # MG-2: Cora/GAT (3 methods × 5 seeds)
├── mg3_citeseer/phase_a/       # MG-3a: Citeseer IDEA/MEGU (2 methods × 5 seeds)
├── mg3_gat/phase_a/            # MG-3b: GAT IDEA/MEGU (2 methods × 5 seeds)
└── _archive/                   # 历史目录 (phase_a / tracin_fix_phase_a / phase_a_v2_tracin_fix)
```

---

## 下一步

1. 补跑 MG-0 seed 212 的 GUIDE
2. 生成汇总统计表 (mean ± std)
3. 绘制泛化性图表
