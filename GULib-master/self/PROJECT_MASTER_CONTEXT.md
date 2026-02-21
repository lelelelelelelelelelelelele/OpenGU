# PROJECT_MASTER_CONTEXT.md

## 1. 项目概览 (Project Overview)

*   **项目名称**: Adversarial Attacks on Graph Unlearning (GNN 遗忘攻击研究)
*   **当前阶段**: 核心算法实现与攻坚阶段
*   **核心目标**: 
    *   设计一种针对 **GNN Unlearning（图遗忘学习）** 的攻击机制。
    *   通过精心选择一组节点（$D_{unlearn}$）进行强制遗忘，诱导模型发生 **灾难性遗忘 (Catastrophic Forgetting)** 或 **性能塌缩 (Performance Collapse)**。
    *   证明现有的近似遗忘算法（Approximate Unlearning）在特定攻击下是脆弱的。
*   **基础框架**: 基于 `bwfan-bit/OpenGU` (Open Graph Unlearning) 进行二次开发。

---

## 2. 核心假设与思维路径 (Hypothesis & Reasoning)

### 2.1 攻击动机
现有的 GNN Unlearning 研究多关注“如何遗忘”，而忽略了“遗忘机制的安全性”。我的假设是：**并非所有数据点的遗忘代价都是相等的。** 存在某些“关键点（Structural & Feature-rich Anchors）”，一旦被强制移除，会导致模型对保留数据的推理能力大幅下降。

### 2.2 战略转折 (Critical Pivot)
*   **Phase 1 (已废弃思路)**: 针对基于重训练 (Retraining/Exact) 的方法（如 GraphEraser）。
    *   *放弃原因*: 精确遗忘难以被攻击，且计算代价高，不符合“四两拨千斤”的攻击美学。
*   **Phase 2 (当前核心)**: 针对 **近似遗忘 (Approximate Unlearning)** 方法（如 GIF, GST）。
    *   *选择原因*: 这类方法依赖梯度更新或影响函数近似，存在数学上的不稳定性。
    *   *攻击切入点*: 利用其依赖的 **Influence Function (IF)** 机制，反向利用，寻找 IF 值最大的点进行恶意遗忘。

### 2.3 方法论创新：IF-IM 混合机制 (The Hybrid Mechanism)
单一指标存在局限性，我提出了 **IF-IM 混合选择策略**：
1.  **Influence Function (IF)**: 捕捉 **"Feature-Model Interaction"**。衡量节点特征对模型参数 $\theta$ 的敏感度。
2.  **Influence Maximization (IM)**: 捕捉 **"Structure Propagation"**。衡量节点在图拓扑中的传播能力（如 CELF 算法）。
3.  **融合公式 (待定)**: $Score(v) = \alpha \cdot \text{Norm}(IF(v)) + \beta \cdot \text{Norm}(IM(v))$

### 2.4 现实挑战与解决方案 (From White-box to Black-box)
*   **挑战**: 原始 IF 计算需要 $H^{-1}$ (Hessian 逆) 和完整模型参数 $\theta$，属于强白盒攻击，且计算昂贵，被师兄指出缺乏实用性。
*   **解决方案 (Pseudo-IF)**: 寻找不需要 $\theta$ 或仅需梯度的替代指标。
    *   **Plan A (Gray-box)**: **TracIn**。使用训练阶段的梯度点积近似 IF ($\nabla \mathcal{L}_{train} \cdot \nabla \mathcal{L}_{test}$)，避免求逆。
    *   **Plan B (Black-box)**: **GNNExplainer / XAI**。使用解释性模型的输出作为重要性得分。

---

## 3. 技术栈与环境 (Technical Stack)

*   **Language**: Python 3.9+
*   **DL Framework**: PyTorch, PyTorch Geometric (PyG)
*   **Base Framework**: OpenGU
*   **Datasets**: Cora (Dev), Citeseer, PubMed (Test)
*   **Key Libraries**: `networkx` (Graph structure), `captum` (XAI/Interpretation), `torch_influence` (if applicable)

---

## 4. 当前进展 (Progress Log)

### ✅ 已完成 (Done)
1.  **基线复现**: GCN, GAT, GIN 在 Cora 上达到 SOTA 水平 (Acc ~80-82%)。
2.  **OpenGU 跑通**: 成功运行 GraphEraser，熟悉了 `config` 和 `pipeline`。
3.  **MIA 验证 (Pre-study)**: 在 CIFAR-10 上验证了“梯度范数”分布差异，证明了梯度作为攻击指标的可行性。
4.  **理论闭环**: 确立了从 Exact Unlearning 到 Approximate Unlearning 的转型。

### 🚧 进行中 (In Progress - February Focus)
1.  **Pseudo-IF 实现**:
    *   编写 `TracIn` 算法适配 GNN。
    *   调研 `GNNExplainer` 的 score 提取接口。
2.  **攻击模块构建**:
    *   在 OpenGU 中新建 `attack_strategies` 模块。
    *   实现 IF-IM 融合的打分排序逻辑。

---

## 5. 实验设计与评估体系 (Experimental Design)

### 5.1 攻击流程
1.  **Pre-train**: 训练标准 GNN 模型。
2.  **Select**: 使用 IF-IM / Pseudo-IF 策略选出 Top-K 个节点作为 $D_{unlearn}$。
3.  **Unlearn**: 运行目标 Unlearning 算法 (GIF/GST) 移除 $D_{unlearn}$。
4.  **Evaluate**: 评估遗忘后模型在 $D_{test}$ (保留集) 上的表现。

### 5.2 核心指标 (Metrics)
*   **Effectiveness (Utility)**: **Node Classification F1 Score Drop**。
    *   *Target*: 下降幅度显著大于 Random Unlearning。
*   **Completeness (Privacy)**: **MIA AUC**。
    *   *Target*: AUC 偏离 0.5 (证明模型残留了信息或泄露了遗忘痕迹)。
*   **Efficiency**: 节点选择算法的时间复杂度。

### 5.3 Baselines
*   **Random**: 随机选择节点遗忘。
*   **Degree-based**: 仅基于度中心性选择。
*   **PageRank**: 仅基于图结构选择。
*   **Pure IF (White-box)**: 理想情况下的上限对比。

---

## 6. AI 助手指令 (Instructions for AI Agent)

**作为我的科研助手，在与我对话时，请遵循以下原则：**
1.  **上下文感知**: 始终记得我是做 **GNN Unlearning 攻击** 的，不要给我通用的 GNN 建议。
2.  **代码优先**: 当我询问实现细节时，优先提供基于 **PyTorch Geometric** 的代码片段，并考虑 **OpenGU** 的接口兼容性。
3.  **批判性思维**: 如果我提出的想法有逻辑漏洞（例如忽略了计算复杂度），请直接指出并提供替代方案（如 Pseudo-IF）。
4.  **格式规范**: 涉及公式时使用 LaTeX，涉及文件结构时使用 Tree 格式。
5.  **伪代码风格**: 在解释算法时，先给出高层逻辑的伪代码，再给 Python 实现。

---

# 下一步操作建议

将上述内容保存后，你可以在 AI 工作区（如 ChatGPT 的 Custom Instructions 或 Project Description）中设置如下**System Prompt（系统提示词）**，以激活这个“人设”：

```text
你现在是我的专属科研助手 "GNN-Attacker"。
你的核心知识库是 "PROJECT_MASTER_CONTEXT.md"。
你需要根据这个文档中的背景、目标和技术路线，辅助我完成代码编写、论文阅读和实验分析。
当前我们的首要任务是：攻克 Pseudo-IF 的代码实现，并将其集成到 OpenGU 框架中。
请时刻准备好根据我的指令生成 Python 代码或分析论文。
```

这样设置后，你只需要对它说：“帮我写一个基于 TracIn 的节点选择器类”，它就能立刻根据 OpenGU 的风格和你的需求生成非常精准的代码，而不需要你再解释一遍什么是 GNN 什么是 Unlearning。