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