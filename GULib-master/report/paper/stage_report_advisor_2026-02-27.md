# 导师汇报材料（提纲 + 文字稿）  
**日期：2026-02-27**

## 一、给导师看的提纲（1 页版）

### 1. 本次汇报目标
1. 汇报阶段性进展是否达到“可投稿分析”标准。  
2. 说明为什么需要新增 `Relative F1 Drop` 指标。  
3. 请导师拍板下一阶段优先路线（补证据 vs 扩展 CV 方向）。

### 2. 三条核心结论
1. **实验体系已从单点结果升级为端到端矩阵评估**：当前累计 `950 runs`，覆盖方法、数据集、模型、ratio、策略和 `5 seeds`。  
2. **算力路径已明确**：IF 选点在工程上采用 `TracIn`，IM 选点采用 `IM v4`（`34.55x` 提速，spread 仅 `1.26%` 损失），大图下一步是 `D-SSA/IMM`。  
3. **结论解释力显著提升**：通过 `Relative F1 Drop`（基线：`k=5 random`），把“攻击效果”与“方法自身增益”拆开，解释了 Shard-based 的反直觉现象。

### 3. 关键证据（导师重点看）
1. **覆盖规模**：`results/experiments/auto_discovered.json`，总计 `950 runs`。  
2. **IM benchmark**：`experiments/im_benchmark/results/bench_results.json`  
   - `V0=652.97s`，`V4=18.90s`，加速 `34.55x`。  
   - spread `2700 -> 2666`，损失 `1.26%`。  
3. **Shard-based 解释**：  
   - 绝对口径下 GraphEraser 存在负 drop（看起来“越删越好”）。  
   - Relative 口径下仍有可测攻击增益（例：`cora/gcn/r=0.05`，GraphEraser: `tracin=1.70`, `im_v4=4.87`, `hybrid_v4=4.39`）。

### 4. 当前结论边界（风险与不足）
1. 主实验仍集中在 `cora/citeseer`，外推到 CV 场景的证据还不够。  
2. MIA 审计尚未闭环。  
3. 机制层 ablation（尤其 GNNDelete）还需要补齐。

### 5. 需要导师拍板的 3 个决策
1. 下一轮优先级：先补 `MIA + ablation`，还是直接推进 CV 数据集扩展。  
2. 目标投稿路径：CV 导向（ECCV）还是通用 ML 导向（NeurIPS/ICML/KDD）。  
3. 是否接受“Shard-based 双层结论”作为论文主叙事之一：  
   - 绝对性能可能上升；  
   - 但相对基线仍有攻击增益。

### 6. 下一阶段（2-3 周最小包）
1. **必做**：`GNNDelete + GIF` 的 MIA 最小闭环。  
2. **必做**：GNNDelete 机制 ablation（DEC/NI 最小分解）。  
3. **可选扩展**：CV-Exp-1（scene graph，一组主表 + 一组可视化）。

---

## 二、口头汇报文字稿（可直接讲，约 8-10 分钟）

### 开场（约 30 秒）
老师好，我今天主要汇报三件事：第一，实验体系目前做到什么完整度；第二，为什么我们要引入 Relative 指标；第三，请您帮我拍板下一阶段优先路线。  
一句话结论是：我们现在已经能把“攻击效果”与“方法自身偏置”分开看，结论比之前稳，也更适合写成论文叙事。

### 1. 本轮进展（约 1.5 分钟）
这轮我把流程打通为端到端链路：主实验、relative 评估、collateral 评估、图表汇总和状态核查都串起来了。  
覆盖规模上，累计 `950 runs`，包含 `GIF/GNNDelete/GraphEraser/IDEA/MEGU`，数据集是 `cora/citeseer`，模型是 `GCN/GAT/GIN`，ratio 覆盖 `0.01/0.05/0.10/0.20`，并且统一用了 5 个 seeds。  
所以当前不是单点实验，而是一个可复验的矩阵。

### 2. 算力与方法决策（约 1.5 分钟）
您之前问过 IF 和 IM 在算力上的可行性，这里结论比较明确：  
IF 这条线上，精确 IF 在组合搜索里成本过高，所以我在攻击框架里用 `TracIn` 作为工程可执行替代。  
IM 这条线上，`IM v4` 的 benchmark 是 `652.97s -> 18.90s`，提速 `34.55x`，传播能力只损失 `1.26%`，所以当前阶段可以稳定使用。  
如果后续转更大图，我会按既定路线转 `D-SSA/IMM`。

### 3. 为什么一定要用 Relative 指标（约 2 分钟）
核心原因是：绝对 F1 drop 会混入“方法自身漂移”，无法单独回答攻击是否真正有效。  
我现在用的定义是以 `k=5 random` 的 after-F1 作为 baseline，然后计算各攻击策略相对该基线的下降。  
这样就能把“算法本身让模型变好/变坏”与“攻击额外造成的变化”拆开。  
这一步是目前最关键的解释升级。

### 4. 关键发现：Shard-based 的双层结论（约 2 分钟）
我们确实观察到 GraphEraser 在绝对指标里常见负 drop，也就是表面上“越删越好”。  
如果只看绝对值，会得出“攻击没效果”甚至“攻击有利”的误判。  
但改用 Relative 后，在同等基线下仍能看到攻击增益，比如 `cora/gcn/r=0.05` 下，GraphEraser 的 `tracin=1.70`、`im_v4=4.87`、`hybrid_v4=4.39`。  
所以论文叙事上我建议明确“双层结论”：  
第一层，Shard-based 可能带来自身提升；第二层，攻击相对基线仍然有效。

### 5. 方法族结论与图表（约 1 分钟）
方法族层面，GNNDelete 依然是最脆弱的方法；GIF/IDEA/MEGU 相对稳定；GraphEraser 是最需要谨慎解释的对象。  
配图上我准备了 5 张图，分别对应泛化对比、ratio 敏感性、脆弱性谱、显著性、relative 与 collateral 的关系，组会上可以按这个顺序讲。

### 6. 请导师拍板（约 1 分钟）
我需要您帮我定三个优先级：  
第一，下一轮先补 `MIA + ablation`，还是先做 CV 扩展。  
第二，投稿目标偏 ECCV 还是先走 NeurIPS/ICML/KDD。  
第三，是否认可“Shard-based 双层结论”作为主叙事。  
如果您同意，我接下来 2-3 周按“先补证据闭环，再做 CV 最小扩展包”的顺序执行。

---

## 三、汇报时可直接展示的图

1. `FIG-1` 泛化与方法族对比：`../../results/paper_figures/FIG-1_Generalization.png`  
2. `FIG-2` ratio 敏感性：`../../results/paper_figures/FIG-2_Scaling.png`  
3. `FIG-3` 全方法脆弱性谱：`../../results/paper_figures/FIG-3_Spectrum.png`  
4. `FIG-4` 统计显著性：`../../results/paper_figures/FIG-4_Significance.png`  
5. `FIG-5` relative vs collateral：`../../results/paper_figures/FIG-5_Collateral.png`
