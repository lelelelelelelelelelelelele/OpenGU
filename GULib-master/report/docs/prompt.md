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

* GraphEraser（Shard-based）+ GIF（IF-based）
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

## 0-3 paper loading

-1 ：
你是一个 research engineering agent。对我当前项目：Graph Unlearning + GNN。你的任务是“建一个可复现的论文库”，覆盖最近两年（以今天为准，优先 2024-02-16 至今）的 GNN/graph learning 论文，并尽量与 graph unlearning / deletion / privacy auditing / membership inference / efficient retraining / influence functions / distillation / partition-based training 等相关。

硬性要求：
1) 你必须使用可验证来源获取元数据：arXiv +（Semantic Scholar 或 OpenAlex）+（publisher/Crossref 如有）。
2) 不允许编造 citation counts、venue、DOI、作者信息；不确定就标 unknown，并记录证据链接。
3) 输出必须可复现：创建目录 papers/；下载 PDF；生成 papers.csv + library.bib + 一份 markdown 总览。

步骤：
A. 检索与候选（>=20 篇）
- arXiv 检索：GNN/graph neural network/graph learning +（unlearning/deletion/forgetting/privacy/MIA/influence/distillation/partition/efficient retraining）。
- 过滤：日期近两年优先；主题必须与图学习强相关。
- 为每篇补充：arXiv id、标题、年份、作者、primary category、pdf link。

B. 门槛筛选与打分（最终 8–12 篇）
- 给每篇打分：相关度(0-3) + venue 门槛(0-3) + 影响力(0-3) + 可复现性(0-2)。
- venue 门槛：若有顶会/高刊信息则加分；若无则按影响力/作者群体/开源实现作为替代，但要写依据。
- 影响力：优先引用数（S2/OpenAlex）；新论文引用低则标“early”并记录证据。
- 输出：候选表 + 入选表（含筛选理由）。

C. 下载与整理
- 下载入选论文 PDF 到 papers/<arxiv_id>_<short_title>.pdf
- 生成 library.bib（BibTeX）与 papers.csv（字段：arxiv_id,title,year,authors,venue,doi,citations,source_links,keywords,match_score,notes,local_path）

D. 每篇生成“粗提炼卡片”（先结构化、别深度发挥）
为每篇入选论文生成 1 个 markdown 卡片（papers/notes/<arxiv_id>.md），模板：
- one-sentence claim
- task setting + threat model（如果相关）
- method sketch（3-6 bullet）
- evaluation: datasets/baselines/metrics
- “possible reuse for GU” (>=3 bullet)
- “flags / uncertainties” (>=2 bullet with evidence links)

最后输出：
1) 入选论文列表（含证据链接）
2) papers.csv + library.bib 的路径
3) 每篇卡片路径列表

- 2：

你是一个顶会审稿人 + 论文导师。你将看到我用脚本搜集的最近两年 GNN 相关论文库（包含 papers.csv 元数据与每篇粗提炼卡片 notes/*.md）。你的任务是做“高门槛学术提炼 + 反哺我的研究设计”。

硬性要求：
- 只基于给定材料与其中的证据链接推断，不要凭空补论文细节。
- 对每篇论文：纠正粗卡片可能的误读；指出 claim 是否 overstated；补齐“与 GU 的真实连接点”。
- 产出必须能直接写进论文：related work 结构、positioning 句式、实验清单、gap 的可检验表述。

步骤：
1) 论文群的结构化综述（不要按时间流水账）
- 用 3-5 条主线组织：例如 partition/sharding, IF/approx, distill/learning-based, privacy auditing/MIA, efficiency/scalability。
- 每条主线给：核心问题、代表论文、它们的共同评估范式、最大盲点。

2) 每篇论文的“可写作级提炼”
对入选 8–12 篇，每篇输出：
- claim（更精确重写）
- novelty 判断（相对谁）
- methods（用 1-2 段讲清楚机制，不要泛）
- what I can borrow（method/eval/baseline 分开）
- what I should not borrow（assumption mismatch）
- 1 句可放 related work 的写法（学术英文句子）

3) 研究机会地图（可投稿级）
- 给 5–8 个 gaps，每个 gap 必须满足：
  (a) 可检验（能用实验或理论验证）
  (b) 与至少 2 篇论文形成明确对比
  (c) 指出最小增量贡献 + 最大风险

4) 审稿人式 rubric 评估我的 idea（先初评，再复评）
按 novelty/soundness/significance/eval/reproducibility/story 各 1-5 分，
并给“达到顶会门槛”的硬性补充清单（最少 8 条，按优先级排序）。



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