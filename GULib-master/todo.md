# 0
## 0-1
开始执行 flow.md 中的 Step 0（OpenGU 基础设施验证）。

  请先读取 self/flow.md 的 Step 0 部分了解具体要求。

  任务：
  1. 创建 git 分支 feat/attack-strategies
  2. 创建 results/step0_validation/ 目录结构
  3. 执行第一轮广度扫描：15 个 GU 方法 × GCN × Cora × 默认参数
  4. 记录每个方法的状态（✅❌⚠️）和指标，生成 round1_scan.md
  5. 对 ✅ 方法执行第二轮深度验证
  6. 生成 method_compatibility.json
  7. /checkpoint step-0

  第一轮的 15 个方法请逐个串行运行，每个跑完立即记录结果。
  如果某方法超过 10 分钟未完成，标记为 ⚠️ 超时并跳过。
  完成第一轮后，汇报结果再继续第二轮。

## 0-2

你是一个严格但友好的研究型代码导师。你正在阅读我当前打开的仓库（OpenGU/GULib-master）。我的目标：**深入理解 graph unlearning（GU）各类方法**，并把**论文思想 ↔ 代码实现**一一对照起来。请你把仓库当作“可执行的综述”，用**分类+流程+代码定位**的方式讲解。

### 1) 先给我一张“总地图”（必须结合代码）

用 10-20 行解释这个 repo 的执行主流程，并给出具体入口与调用链（文件+函数/类名）：

* `main.py` → 参数解析 → 数据加载/切分 → model_zoo → UnlearningManager → method.run_exp
* 指出：数据处理在哪里缓存、unlearning 目标（nodes/edges/features）存哪里、log/ results 输出结构是什么
  （你必须给出在仓库中的具体路径和关键函数名，不要抽象讲）。

### 2) 按流派分类讲 GU（每类都要“论文直觉 + 代码骨架”）

请按 OpenGU/GULib 的框架，把方法分成至少三类，并对每一类给出：

* **核心思想**（一句话 + 一段解释，能对应到常见论文叙述）
* **适用的 unlearn task**（node/edge/feature）与 downstream task（node/edge）
* **典型实现套路**（这个 repo 里如何落地：pipeline 基类、trainer、method 类分别负责什么）
* **你认为最关键的 3 个实现细节**（例如：哪些张量被重算、哪些缓存复用、哪里做近似、哪里可能引入不彻底遗忘）
* 给一个“我应该先读哪里”的最短阅读路径（文件列表，按顺序）

分类建议（但你可以按代码实际结构微调）：

* shard/partition-based（GraphEraser / GraphRevoker）
* influence-function / certified / approximation family（GIF / GUIDE / CEU / CGU / GST / IDEA / ScaleGUN 等）
* learning-based / distillation-based（GNNDelete / MEGU / GUKD / D2DGN / SGU / UTU 等）
  （方法名单以仓库 `UnlearningManager` 映射为准。）

### 3) 选 2 个代表方法做“逐行导读式 walkthrough”

从每个方法的 `run_exp()` 开始，按调用顺序解释：

* 输入是什么（args、data、split、targets）
* 中间状态如何保存（缓存/中间文件/日志）
* 输出哪些指标（effectiveness/robustness/efficiency + MIA 等）
  并在讲解时把关键函数用“文件:行号/函数名”的形式标出来（如果你无法给行号，就给函数名+相邻代码片段定位点）。

建议你优先选：

* GraphEraser（partition-based）+ GIF 或 GUIDE（IF-based）
  如果仓库里更适合别的组合，也可以调整，但必须解释你为何这么选。

### 4) 把评估与攻击联系起来（这是 GULib 的重点）

请解释这个库如何做 MIA（membership inference attack）与（如果有）poisoning / robustness 测试：

* attack 相关模块在哪里、输入输出是什么、AUC≈0.5 的含义如何在代码里被计算
* 给我一个“最小可复现实验命令”，并解释每个参数会触发哪条代码路径（例如 trainer 的选择、transductive/inductive、balanced/imbalanced、unlearn_ratio 等）。

### 5) 你的输出格式（务必遵守）

* 先给 **repo 总流程图（文字版）**
* 再给 **方法分类表（每类 5-8 行）**
* 再给 **两种方法的 walkthrough（分小节）**
* 最后给 **我下一步的阅读/实验清单（5-8 条）**
  不要泛泛科普；我需要的是“读代码能跟得上”的解释。遇到你不确定的部分，明确标注“需要我打开/运行哪段代码来确认”，但不要停下来等我回复——先给出你基于当前仓库结构的最佳推断。



<!-- 
  开始执行 flow.md 中的 Step 1。

  请先读取以下文件了解背景：
  - self/flow.md（Section 8 的 Step 1 部分）
  - self/宏观plan.md（整体计划）

  任务：
  1. 创建 git 分支 feat/attack-strategies
  2. 新建 attack/attack_strategies/__init__.py
  3. 新建 attack/attack_strategies/base_strategy.py（BaseStrategy 抽象基类）
  4. 新建 attack/attack_strategies/random_strategy.py（RandomStrategy）
  5. 新建 tests/test_strategies.py（4 个单元测试）
  6. 运行测试确认全部通过

  完成后用 /checkpoint step-1 存档。 -->