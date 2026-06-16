---
tags: [progress/findings, status/active]
type: index
created: 2026-06-15
updated: 2026-06-15
up: "[[_Home]]"
---

# 🔍 Findings & Decisions（活·索引）

> 当前在动的关键发现与待决策。**只放摘要 + 链接**，正文在各权威文档。

## 🧨 数据复查发现（2026-06-15，修正 5.7 旧叙事）

| ID | 一句话 | 严重度 | 正文 |
|---|---|---|---|
| **C1** | informed selector（TracIn/IM/Hybrid）打不过 degree，TracIn 平均为负 → **原贡献被证伪**，需 reframe | 🔴 决定性 | [PROGRESS §2](../../../self/dashboard/PROGRESS.md) |
| C2 | GNNDelete 在 n=5 不显著（sd≫mean） | 🟠 | 同上 |
| C3 | §A.4 hop-decay 被 L8 污染 + CSV 4 列全空（GIF≡IDEA 逐位相同） | 🟠 | [limitations L8](../../../self/limitations.md) |
| C4 | ΔF_noise(k=5) 磁盘 5/6 方法 `f1_before`=null | 🟠 | [limitations L7](../../../self/limitations.md) |
| **C5** | GraphRevoker 整 method 退化（perf_before 0.50-0.58 vs 0.77-0.87）+ 聚合器 bug 未修完 → 全部结果可疑，§5.2 GR×GAT 反例站不住 | 🟠 | [PROGRESS §2/P1.5](../../../self/dashboard/PROGRESS.md) |

## 🧭 研究路径 / idea（候选方向）

- **degree 最严重 → 重要性×脆弱性分解 → GU 安全指数** → [research_path（外部）](../../../self/research_path_degree_severity_decomposition.md)（已用 gap 数据部分验证，是 reframe 的正向落点）
- **跨架构共识当可信信号** → [idea_cross_arch（外部）](../../../self/idea_cross_arch_consensus.md)（future-work；caveat#1 戳中"GCN+GAT 都 MP"弱点）

## ⏸️ 待决策

- **大方向：rebuttal vs 重投** —— 我的建议=重投+reframe（理由见 [PROGRESS §4](../../../self/dashboard/PROGRESS.md)）。用户当前选"先保住现状"。**未定**。

## 🧱 已知瓶颈/限制

- L1-L8 全表 → [limitations（外部）](../../../self/limitations.md)。当前 OPEN：L7（k=5 缺 5/12）、L8（hop/gap IF-family 污染，代码已修待重跑）。
- **GraphRevoker 损坏分片 checkpoint transient**：cora_GCN_r0.01/random/seed42 因 `torch.load: not a ZIP archive`（截断/空 .pt）崩 1 个 cell。这是**在 C5 整 method 退化之上的另一个独立小问题**，删 `data/GraphRevoker/cora/` 损坏 .pt + 重跑即可，随 C5 的重跑一起解。

> 决策定了或发现解决了，更新本页 + 对应正文 + [PROGRESS](../../../self/dashboard/PROGRESS.md)。
