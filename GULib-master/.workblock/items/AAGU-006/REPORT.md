# AAGU-006 · 默认可覆盖、合同可复用的 Dataset Split

报告事实日期：2026-09-02

已验证实现检查点：`13083d6822ccaf23d1801732c4af3c16c7abe4d6`

当前分支：`codex/aagu-006-dataset-split-authority`

## Human Result

### 实际增量

[`syncmate_target_direct_formal_v2.yaml`](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml) 现在只用 split mapping 声明数据划分：当前 default 是 `train=0.7 / validation=0.1 / test=0.2`、`split_seed=2024` 和 `materialize_on_miss=true`。processed profile 与训练候选集合/数量由这份 split 合同确定；删除预算仍由实验注册中的 budget ratio 或固定 `k` 独立拥有，不属于 split 参数。

同 dataset、同规范化 ratios、同 split seed 只对应一个 canonical profile 和一组 OpenGU pickle；`0.7` 与 `0.70` 会命中同一路径。另一组满足实验目标语义的合法合同会得到不同 profile，可以和 default 并存，不会被“只允许默认值”的 gate 拒绝。Cache V2 仍只有一个 root，通过实际 `split_hash`、candidate hash 和 target hash 区分 exact identity。

### 核心观察

| 场景 | 期待 | 实际观察 | 判断 |
|---|---|---|---|
| 当前注册 default | YAML 是唯一 split 输入 | loader 派生 `planetoid_70_10_20_seed2024`，Cora/CiteSeer/PubMed 的训练候选数仍为 1895/2328/13801；独立注册的删除预算未被 AAGU-006 改写 | `PASS` |
| 合法 alternate | 非默认比例不能被 default gate 拒绝 | `0.6/0.2/0.2 + seed42` 通过同一 formal loader 和 direct runner 校验，派生 `planetoid_60_20_20_seed42` 与对应候选集合；budget 参数保持独立 | `PASS` |
| 等价合同真实复用 | `0.7` 与 `0.70` 只物化一次 | 真实 PyG/文件 cold 先创建 pair 与 manifest；等价合同 warm 返回 `reused`，原文件 bytes、`mtime_ns` 与 `split_hash` 不变 | `PASS` |
| 不同合同并存 | 多样性不能因复用而消失 | `0.6/0.2/0.2` 创建另一条 profile、另一组 pickle 与不同 `split_hash`；default 文件保持原样 | `PASS` |
| 注册消费 | 当前实验注册都读取同一合同 | AAGU-006 与 AAGU-007 都指向 formal-v2 YAML；29 个 target-direct Selection/GU recipe 全部投影同一 default split contract 与新配置摘要 | `PASS` |
| clean checkpoint 回归 | 当前实现整体成立 | `250 passed, 1 deselected`；deselect 的唯一测试要求本机安装独立 SyncMate Core distribution，该环境依赖当前未安装 | `PASS · scoped` |
| registered local preflight | 错误环境不能顺手物化正式数据 | preflight 绑定 clean SHA `13083d68`，因非 main、非 AutoDL、设备不符和前置证据缺失而停止；`generated_artifacts=[]`，processed 文件前后均为 0 | `PASS · scoped` |

### 当前决定

> 当前验收决定：`待决定`

**Agent 建议：建议接受。** 本候选已经取消 frozen-default 错误语义，证明相同合同只保存一次、不同合法合同可以并存，并让正式注册与运行链消费 YAML split；删除预算继续由实验注册独立管理。它没有启动正式实验，也没有禁止历史或其他实验使用 `0.8/0/0.2` 等不同合同。

决定人：刘丞毓。可以接受当前候选，或指出具体返工项。

## 关键判断详情

### 1. default 与“唯一允许值”已经分开 — `PASS`

在 formal YAML 保持 `0.7/0.1/0.2 + seed2024` 的场景中，系统期待它是当前注册的 default，而不是 loader 白名单。实际 loader 不再比较 `DEFAULT_SPLIT_CONTRACT`；只校验比例、seed、target-direct 非空 validation 语义和其他正式边界。完整的 `0.6/0.2/0.2 + seed42` 合同通过同一入口，支持“默认可覆盖”的判断。

通用 OpenGU 合同仍接受 `0.8/0/0.2`，并可派生 `planetoid_80_0_20_seed42`。target-direct 本身的攻击目标来自 validation mask，所以它不能执行空 validation 合同；这是专题方法的输入语义，不是对仓库其他 split 的全局禁止。

### 2. 相同比例不会出现多份 — `PASS`

canonical profile 只由 dataset family、规范化后的三个比例和 split seed 派生。`0.7`、`0.70`、数值或等价字符串得到完全相同的 `ProcessedSplitContract` 和文件名。在真实 cold/warm 文件测试中，第二次调用没有重切或覆写，三份持久化文件的 bytes 与纳秒修改时间都保持不变，实际 masks 的 `split_hash` 也一致。

### 3. 不同合法比例仍保留多样性 — `PASS`

在同一临时 canonical processed root 中先物化 default，再物化 `0.6/0.2/0.2`。后者得到不同 profile、不同 pickle path 和不同 `split_hash`；两组文件同时存在，default 文件未被改写。这证明“复用相同合同”和“允许实验多样性”没有冲突。

### 4. 注册与运行链是否真的消费 YAML — `PASS`

formal YAML 不再手填 `processed_profile` 或 `expected_candidate_count`；target-direct stage、direct selection runner 和 SyncMate registry 从 split mapping 派生数据身份与候选集合。删除预算的 ratio/固定 `k` 仍是独立实验参数；若注册的是 ratio，运行时才把该 ratio 投影到候选集合得到实际删除数量，这不改变参数归属。审计当前控制面时，AAGU-006 与 AAGU-007 都指向同一 formal-v2 fact owner；注册表中的 9 个 Selection、2 个 GU gate 和 18 个 GU stage recipe 共 29 个定义，都携带与 loader 完全相同的 default split contract。

### 5. Cache 是否需要按 split 建多个根 — `PASS`

不需要。持久化 split 是 processed profile；Selection 证据由一个 Cache V2 exact-recipe store 管理。相同合同和实际 masks 产生相同 `split_hash`，具备精确 hit 的前提；不同合同会改变 profile、candidate pool 和 `split_hash`，自然形成不同 Recipe identity。这里没有建立 split-specific cache root。

### 6. 正式入口是否 fail closed — `PASS · scoped`

在 clean checkpoint 上调用注册 Cora/seed42/1% GU gate。期待本机只读取合同并检查前置，不在错误机器上创建正式 split。实际 preflight 读取到了派生的 default profile，然后因分支、checkout、GPU 型号、profile 与 Selection receipt 不符合而返回失败；`generated_artifacts=[]`，本地 `data/processed` 文件数从 0 保持为 0。该结果只证明 gate 与零物化，不等于正式 GPU 实验通过。

## 已知缺口与边界

- `NOT OBSERVED` — 未在 AutoDL RTX 4090/main checkout 上执行正式 cold materialization、Selection/GU gate 或完整矩阵。
- `NOT OBSERVED` — 未产生攻击效果、遗忘效果、隐私或论文结论；AAGU-006 只修复 dataset/split 合同与注册消费。
- `NOT CONFIRMED` — 当前本机未安装项目声明的独立 SyncMate Core distribution；依赖该已安装包的 bootstrap 测试未进入本次 PASS 数，源代码注入下的 target-direct registry 测试已通过。
- AAGU-006 是 split 基础设施前置；AAGU-001 仍是后续实验定义/注册 gate，并同时等待 AAGU-015。AAGU-024 未被修改，也不是 AAGU-006 的验收前置。

## 技术复核入口

- 权威 recipe：[`experiments/configs/syncmate_target_direct_formal_v2.yaml`](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml)
- 通用 split contract：[`experiments/processed_provider.py`](../../../experiments/processed_provider.py)
- cold/warm materializer：[`experiments/target_direct_v1/split_profile.py`](../../../experiments/target_direct_v1/split_profile.py)
- 正式 launcher：[`experiments/target_direct_v1/syncmate_stage.py`](../../../experiments/target_direct_v1/syncmate_stage.py)
- 注册投影：[`scripts/syncmate/opengu_recipes.py`](../../../scripts/syncmate/opengu_recipes.py)
- 真实复用/并存测试：[`tests/test_target_direct_split_profile.py`](../../../tests/test_target_direct_split_profile.py)
- 当前 Record：[`WORKITEM.md`](WORKITEM.md)
- Apply target：`refs/heads/codex/e7-two-surrogate-groups-20260805`
