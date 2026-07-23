---
type: topic-map
status: active
owner: ai
source: ai-draft
created: 2026-07-23
updated: 2026-07-23
tags: [论文阅读, GNN, 图机器遗忘, influence-selector, unlearning-attack]
---

# GNN influence-selector 与 unlearning attack 精读线

> [!important] 状态边界
> 跨项目的“待读 / 在读 / 已读”状态只在 Learning vault 的《全局论文阅读台账》维护。本页只保存 OpenGU/GULib 的阅读顺序、项目问题和证据链接，避免制造第二份全局状态。

## 这条线回答什么

这不是泛化的 graph-unlearning related work 清单，而是围绕一个更窄的问题组织：**怎样从候选图元素中选择删除对象，以及选择目标怎样从单点局部影响走向集合级、unlearning-operator-aware 的攻击目标。**

它直接服务：

- A / B / C-point / C-simple / D-GIF influence-selector 的定义与边界；
- graph source 是否需要删后图梯度（项目中的 `grad2`）；
- exact retrain、影响估计、删后攻击 outcome 与 approximate GU gap 的分离；
- 潜在 E 层的 set-level、operator-aware selector。

## 建议顺序与深度

| 顺序 | 论文 | 深度 | 在本项目中负责回答 |
|---:|---|---|---|
| 1 | [[2210.07441_Characterizing-the-Influence-of-Graph-Elements\|Characterizing the Influence of Graph Elements]] | **精读** | 完整 graph-deletion source 如何进入 IF；为何初步映射到 D-GIF；exact retrain 如何校准估计；为何可能超过 Degree |
| 2 | [Attack by Unlearning: Unlearning-Induced Adversarial Attacks on Graph Neural Networks](https://arxiv.org/abs/2603.18570) | **精读，紧随第 1 篇** | bilevel objective、one-step differentiable GU surrogate、注入集合与 stealth constraints；哪些结构可启发 E，哪些因 threat model 不同不能搬用 |
| 3 | [No Change, No Gain](https://proceedings.neurips.cc/paper_files/paper/2023/hash/944ecf65a46feb578a43abfd5cddd960-Abstract-Conference.html) | 主读 | GNN active learning 中 expected model change（B）何时能代理 expected prediction error（C） |
| 4 | [Witches' Brew](https://iclr.cc/virtual/2021/poster/2561) | 主读 | 从攻击角度理解 target alignment 为什么比 gradient magnitude 更接近 C |
| 5 | [Expected Error Reduction](https://groups.csail.mit.edu/rrg/papers/icml01.pdf) | 伴读 / 按需 | 给“最终选择目标应落在任务误差”提供经典思想来源 |

> [!warning] 第二篇的发表边界
> 截至 2026-07-23，`arXiv:2603.18570` 仅核对到 v1（2026-03-19），尚未确认正式发表或录用。仍列为精读，是因为它直接覆盖 set-level、operator-aware unlearning attack 的 novelty / threat-model gate；这不等于把预印本当作已同行评审证据。

## 核心双篇的分工

| 维度 | Chen et al. 2023 | Zhang et al. 2026 | 对 A–E 的意义 |
|---|---|---|---|
| 起点 | 从已有图中删除节点/边 | 先注入攻击节点，再请求删除这批节点 | 第二篇的优化权限严格更强，不能直接当作已有节点 selector |
| 方法核心 | graph-aware influence function | bilevel attack + differentiable unlearning surrogate | 前者给 D 的 reference，后者给 E 的优化结构 |
| 真实目标 | validation/test loss 或删后 accuracy | post-unlearning attack loss + stealth | 项目强目标应显式区分 retrain outcome 与 approximate-GU gap |
| 单点/集合 | 单点局部 score，随后 top-$k$ | 联合优化注入/删除集合 | E 需要建模集合交互，而非只累计单点分数 |
| 最值得复用 | graph source、target projection、exact-retrain calibration | bilevel 写法、one-step surrogate、约束化集合优化 | 复用机制，不复用不相同的 threat model |

## 精读完成标准

每篇逐节记录以下八项，并用 `[原文]`、`[项目映射·推断]`、`[项目假说]` 分开：

1. 研究问题与 threat model；
2. 符号和关键公式的逐步解释；
3. 假设与访问级别；
4. 优化目标；
5. 算法步骤；
6. 实验怎样验证核心 claim；
7. 局限和证据边界；
8. 与 A–E、Degree、exact retrain / approximate GU 的对应关系。

第二篇开始正式伴读时，再创建它唯一的 `paper-note`；不提前制造一份看似已经开始的空笔记。
