---
title: CPU-GPU 估时与资源分工
created: 2026-07-09
updated: 2026-07-09
type: runtime-estimation
tags: [runtime, cpu, gpu, im, tracin, resource-planning]
---

# CPU-GPU 估时与资源分工

这页回答两个问题：

1. 哪些任务是 GPU 瓶颈，哪些其实是 CPU 瓶颈？
2. 一个结果慢，是正常慢，还是配置/代码出了问题？

原始来源：

- [experiments/im_benchmark/docs/runtime_estimation.md](../../experiments/im_benchmark/docs/runtime_estimation.md)
- [当前 WORKPLAN](../../self/dashboard/WORKPLAN.md)
- [[15_实验运行入口与脚本]] 与 [[16_4090小数据集运行与回收]]

---

## 一句话结论

| 任务 | 主要瓶颈 | 资源判断 |
|---|---|---|
| Cora / Citeseer 小图主矩阵 | pipeline 调度 + method 训练 | 4090 足够，通常不挑卡 |
| IM / CELF | CPU + graph traversal | 不要只看 GPU 利用率；GPU 空闲不代表卡死 |
| TracIn / Hybrid 的 IF 分数 | GPU 显存 + backward | arxiv 需要 80GB 级别；小图 4090 足够 |
| collateral retrain | GPU 显存 + retrain | 小图 4090 足够；arxiv 24GB 边缘或 OOM |
| aggregate / plot / paper table | CPU / 文件 IO | 本地可以做，不需要 GPU |

---

## 小数据集估时

| 阶段 | 规模 | 4090 估时 | 判断 |
|---|---:|---:|---|
| sanity one cell | 1 cell | 秒级到几十秒 | 环境烟测 |
| Cora GCN 主矩阵 | 180 cell | 4-6h 量级 | 可在 4090 跑 |
| Cora GAT 主矩阵 | 180 cell | 4-6h 量级 | 可在 4090 跑 |
| Cora ratio sweep | 270 cell | 3-5h 量级 | 可在 4090 跑 |
| Citeseer sweep | 180 cell | 约 1h 量级 | 条件补证 |
| GIN backbone ablation | 75 cell | 约 1h 量级 | 附加 ablation |
| alpha sweep | 200 cell | 60-80min 量级 | 只在需要 hybrid 曲线时补 |

这些任务若已经有完整产物，原则上不因换机器或换 session 重跑。

---

## IM 估时模型

当前 IM 路线的关键分解：

| 阶段 | 含义 | V0 / V4 差异 |
|---|---|---|
| Phase 1 | 遍历候选节点，估计 initial marginal gain | V0 和 V4 基本一样 |
| Phase 2 | 贪心选节点，反复重估 marginal gain | V4 batch CELF 主要加速这里 |

原估时文档的核心结论：

- 小图小 K：V4 与 V0 差距不大，因为 Phase 1 占主导。
- 小图大 K：V4 优势很明显；Cora K=150 曾有约 37x 加速。
- 大图：瓶颈转到 Phase 1，单纯 batch CELF 无法根治。
- 高密图 / 超临界图：MC-CELF 可能完全不可行，应考虑 RR-set / IMM / D-SSA。

---

## 数据集可行性

| 数据集 | 图规模 / 密度判断 | IM 策略建议 |
|---|---|---|
| Cora | 小图、亚临界 | V4 batch CELF 足够 |
| Citeseer | 小图、亚临界 | V4 batch CELF 足够 |
| PubMed | 中等图、亚临界 | 可跑，但要预估 Phase 1 |
| Chameleon | 高密，可能超临界 | MC-CELF 风险高 |
| Physics | 高密，可能超临界 | MC-CELF 不适合 |
| ogbn-arxiv | 大图 | 不应纳入 4090 小数据集主线；IM 可 CPU-bound，TracIn/Hybrid 需另设资源 |

---

## GPU 利用率误读

| 现象 | 正确解释 |
|---|---|
| GPU 空闲但进程还在跑 | 可能在 IM / CELF CPU 阶段 |
| GPU 显存高但利用率低 | 可能保留模型 / 图 / G 矩阵，不代表在有效训练 |
| TracIn 很慢 | 小图可接受；arxiv 候选太多时 backward 成本巨大 |
| Hybrid 第二次突然很快 | IF / IM score cache 命中，不代表实验少跑 |
| 本地 RTX 5070 不能跑 pinned torch | 本地只做 CPU 分析和文档；GPU 实验走 AutoDL 镜像 |

---

## 资源分工规则

| 工作 | 推荐位置 |
|---|---|
| coding / 配置编辑 / `--dry_run` / CPU 基本调试 | 本地 5070 机器，但不启用 CUDA |
| GraphRevoker sanity / 小图修复后冒烟 | 4090 AutoDL |
| 小数据集完整矩阵 | 4090 AutoDL |
| 小数据集结果回收后的 aggregate / plot | 本地 |
| arxiv random / IM-only 小切片 | 可用 4090，但不要混进小数据集主线 |
| arxiv TracIn / Hybrid / collateral retrain | 80GB GPU |
| paper 表格、OB、dashboard 文档同步 | 本地 |

---

## 下一步算法方向

`runtime_estimation.md` 里最有长期价值的不是具体秒数，而是这个判断：

> MC-CELF 的根本瓶颈来自“逐候选正向模拟”，RR-set / IMM / D-SSA 通过反向采样把问题改成最大覆盖。

所以未来如果要把 IM 从小图扩到 PubMed / Physics / arxiv，优先级不是继续调 batch size，而是：

1. 把当前 V4 batch CELF 保留为小图 baseline。
2. 为大图增加 RR-set / IMM / D-SSA 路线。
3. 在 paper / rebuttal 中把现有 IM 结果定位成 diagnostic selector，而不是声称大图最优 influence maximization 已完全解决。
