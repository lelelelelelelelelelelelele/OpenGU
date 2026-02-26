# Cora/GCN 稳定性实验 技术分析报告

> 生成时间: 2026-02-22 04:05
> 实验组: mg0_completion

---

## 一、实验数据概览

| Method | Strategy | F1 Drop | Std | N | Flag |
|--------|----------|---------|-----|---|------|
| GIF | degree | 1.37% | ±0.006 | 5 | ⚠️ |
| GIF | hybrid | 1.77% | ±0.002 | 5 | ⚠️ |
| GIF | im | 1.59% | ±0.005 | 5 | ⚠️ |
| GIF | pagerank | 1.55% | ±0.005 | 5 | ⚠️ |
| GIF | random | 1.22% | ±0.005 | 5 | ⚠️ |
| GIF | tracin | 1.22% | ±0.005 | 5 | ⚠️ |
| GNNDelete | degree | 7.71% | ±0.026 | 5 |  |
| GNNDelete | hybrid | 10.26% | ±0.039 | 5 | ✅ |
| GNNDelete | im | 9.70% | ±0.036 | 5 |  |
| GNNDelete | pagerank | 10.33% | ±0.028 | 5 | ✅ |
| GNNDelete | random | 7.90% | ±0.018 | 5 |  |
| GNNDelete | tracin | 7.90% | ±0.018 | 5 |  |
| GUIDE | degree | -9.22% | ±0.037 | 5 | 🔄 |
| GUIDE | hybrid | -6.94% | ±0.042 | 5 | 🔄 |
| GUIDE | im | -9.51% | ±0.028 | 5 | 🔄 |
| GUIDE | pagerank | -8.48% | ±0.027 | 5 | 🔄 |
| GUIDE | random | -7.05% | ±0.033 | 5 | 🔄 |
| GUIDE | tracin | -8.36% | ±0.038 | 5 | 🔄 |
| GraphEraser | degree | -5.50% | ±0.022 | 5 | 🔄 |
| GraphEraser | hybrid | -4.17% | ±0.012 | 5 | 🔄 |
| GraphEraser | im | -5.09% | ±0.012 | 5 | 🔄 |
| GraphEraser | pagerank | -6.86% | ±0.027 | 5 | 🔄 |
| GraphEraser | random | -6.27% | ±0.016 | 5 | 🔄 |
| GraphEraser | tracin | -6.27% | ±0.016 | 5 | 🔄 |

---

## 二、核心发现

### 2.1 最有效攻击组合

- GNNDelete + pagerank: F1 drop = 10.33%

### 2.2 无效/反效应组合

- GIF + pagerank: F1 drop = 1.55% (效果不显著)
- GIF + tracin: F1 drop = 1.22% (效果不显著)
- GIF + random: F1 drop = 1.22% (效果不显著)
- GIF + hybrid: F1 drop = 1.77% (效果不显著)
- GIF + im: F1 drop = 1.59% (效果不显著)
- GIF + degree: F1 drop = 1.37% (效果不显著)
- GraphEraser + hybrid: F1 drop = -4.17% (反效应)
- GraphEraser + im: F1 drop = -5.09% (反效应)
- GraphEraser + pagerank: F1 drop = -6.86% (反效应)
- GraphEraser + degree: F1 drop = -5.50% (反效应)
- GraphEraser + tracin: F1 drop = -6.27% (反效应)
- GraphEraser + random: F1 drop = -6.27% (反效应)
- GUIDE + tracin: F1 drop = -8.36% (反效应)
- GUIDE + random: F1 drop = -7.05% (反效应)
- GUIDE + pagerank: F1 drop = -8.48% (反效应)
- GUIDE + hybrid: F1 drop = -6.94% (反效应)
- GUIDE + im: F1 drop = -9.51% (反效应)
- GUIDE + degree: F1 drop = -9.22% (反效应)

---

## 三、问题诊断

- ⚠️ GIF+pagerank 攻击效果不显著 (F1 drop: 1.55%)
- ⚠️ GIF+tracin 攻击效果不显著 (F1 drop: 1.22%)
- ⚠️ GIF+random 攻击效果不显著 (F1 drop: 1.22%)
- ⚠️ GIF+hybrid 攻击效果不显著 (F1 drop: 1.77%)
- ⚠️ GIF+im 攻击效果不显著 (F1 drop: 1.59%)
- ⚠️ GIF+degree 攻击效果不显著 (F1 drop: 1.37%)
- ⚠️ GraphEraser+hybrid 攻击效果不显著 (F1 drop: -4.17%)
- 🔄 GraphEraser+hybrid 出现反效应，攻击反而提升性能
- 🔄 GraphEraser+im 出现反效应，攻击反而提升性能
- 🔄 GraphEraser+pagerank 出现反效应，攻击反而提升性能
- 🔄 GraphEraser+degree 出现反效应，攻击反而提升性能
- 🔄 GraphEraser+tracin 出现反效应，攻击反而提升性能
- 🔄 GraphEraser+random 出现反效应，攻击反而提升性能
- 🔄 GUIDE+tracin 出现反效应，攻击反而提升性能
- 🔄 GUIDE+random 出现反效应，攻击反而提升性能
- 🔄 GUIDE+pagerank 出现反效应，攻击反而提升性能
- 🔄 GUIDE+hybrid 出现反效应，攻击反而提升性能
- 📊 GUIDE+hybrid 结果波动大 (std: 0.0417)
- 🔄 GUIDE+im 出现反效应，攻击反而提升性能
- 🔄 GUIDE+degree 出现反效应，攻击反而提升性能

---

## 四、改进建议

### 🔴 聚焦最有效攻击组合
GNNDelete + pagerank 效果最佳 (F1 drop: 10.33%)，建议作为主要攻击对象

### 🟡 提高攻击比例 (ratio)
部分 Learning-based 方法攻击效果不显著，建议尝试 ratio=10% 或 20%

### 🟡 Shard-based 方法反效应分析
IF/IM 策略对 Shard-based 方法无效甚至反效，可分析其防御机制作为论文贡献点

---

## 五、下一步行动

- [ ] 分析更多实验组数据
- [ ] 验证问题是否普遍存在
- [ ] 设计针对性实验

---

*本报告由自动化工作流生成*
