# 实验与节点选择 (Node Selection) Benchmark 总览

本目录存放与“对抗攻击选点”（IF-IM Hybrid Selection Strategy）相关的实验基准测试代码、性能探测脚本以及运行日志分析工具。

主要功能是用于探究在超大规模图谱下不同遗忘（Unlearning）方法的计算底座，特别是分析针对节点选择 (Selection Phase) 的时间代价，从而论证攻击路线设计的合理性和计算边界。

注意：在这个环境里进行的所有改动最好retain在这个文件夹当中。
---

## 核心实验结论 (Conclusions)

经过系列 Benchmark 测试与理论推导，针对大规模图数据的节点攻击选择，得出以下关键结论：

### 1. 结构影响力测算 (Influence Maximization, IM)
- **中小图可行性**：经典的 CELF (含 V0 到 V4 加速版) 算法可以直接应用于规模较小的图数据集。
- **大图与稠密图瓶颈**：在超大图（如 `ogbn-arxiv`）或极其稠密的超临界图（如 `Physics`）上，CELF 面临着级联效应导致的无限扩散问题，时间复杂度发生指数级灾难爆炸。
- **解决方案**：针对大图，**必须引入基于反向蒙特卡洛抽样的 RR-set (Reverse Reachable Set) 算法**（例如 IMM 或 D-SSA 等），才能在保证 $(1 - 1/e - \epsilon)$ 近似比的同时，将时间复杂度压制在可行范围内。

### 2. 特征-模型相互作用力测算 (Influence Function, IF)
- **精确 IF (GIF 的牛顿迭代逼近法)**：使用共轭梯度或 IHVP 去拟合海森矩阵逆 ($H^{-1}v$) 的方法，虽然对执行一次脱敏（Unlearn）非常精确，但在攻击者进行 **组合搜索打分 ($N_{train}$ 次迭代)** 时，其**时间复杂度爆炸**。在 `ogbn-arxiv` 上预计选点需要耗时数月，甚至引发频繁 OOM。因此，使用全参二阶导数做攻击选点在工程上被证明为**完全不可行 (❌)**。
- **Pseudo-IF (TracIn一阶梯度法)**：由于只保留一阶梯度点积，避免了深层海森曲率算子，使得打分时间从数月/数天级暴降至 **分钟/小时级**。
- **超大图的“降阶简化”与“白盒”权衡**：
  - 为了追求极致的选择效率，文档中曾提出通过仅采集最后一层分类器梯度 (“Only Last-Layer”) 来将大图 TracIn 的耗时压缩到秒级。
  - **但在学术实验视角下**，攻击者在发起超大图攻击时通常允许长期的离线准备（即所谓的“白盒攻击设定”或“强灰盒设定”）。因此，**即使在超大图上直接跑未经简化的原味完整 TracIn 梯度（需耗时约 6 ~ 12 小时），也是被允许且完全合理的。** 我们可以保留未简化的全参数梯度测算来保证攻击深度的严谨性。

---

## 目录结构 (Directory Structure)

为保持整洁，相关脚本与文档被划分为以下三大类：

### 1. `im_benchmark/` (Influence Maximization 结构测算)
包含所有纯图论节点选择相关的探针测试框架：
- `/scripts`: Python 基准测试运行代码 (`test_*.py`, `run_batch.py` 等)，包含了 CELF 并行与性能探测。
- `/docs`: 分析文档（如 `multi_v1_v3_summary.md`，`runtime_estimation.md`），详述了大图传播下 CELF 的崩溃原因。
- `/results`: 各测试集上产生的 JSON 运行计时与结果。

### 2. `if_benchmark/` (Influence Function 模型影响力测算)
专注于提取和比较不同梯度逼近法的算力开销：
- `/scripts`: 包含了向原始 `result/cache/` 或 `log/` 读取、清洗原始选点耗时的工具 (`get_tracin_cache.py`, `get_if_logs.py` 等)，以还原最真实的物理硬件评估表现。
- `/docs`: `tracin_vs_gif_newton.md`，深度对比评估 GIF 迭代牛顿法与 TracIn 一阶近似的时间可行性。

### 3. `legacy_probes/`
历史废弃脚本或杂项：
- `inject_v0.py`, `find_v0.py` 等。用于早期项目注入或特定版本测试。
