# AAGU-006 · 可复用 Dataset Split 合同

报告事实日期：2026-09-02

实现检查点：`439b876c0a9a7a18b80a1bc47fe654c8a9c6735d`

当前分支：`codex/aagu-006-dataset-split-authority`

## Human Result

### 实际增量

[`syncmate_target_direct_formal_v2.yaml`](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml) 现在显式登记 `train=0.7 / validation=0.1 / test=0.2`、`split_seed=2024` 和 `materialize_on_miss=true`。target-direct launcher、processed profile、Selection summary、外部 manifest、GU YAML 与 adapter 都消费并校验同一份 split contract，不再由运行代码悄悄覆盖为另一套比例。

实现复用 OpenGU 的两段式基础设施：cold miss 在 canonical processed root 生成 masks、data/dataset pickle pair 与 manifest；warm hit 校验后直接加载同一 pair。Cache V2 仍使用一个 selection store，不按模型或实验 seed 另建 split cache；它的 Recipe 输入身份包含注册 split contract、实际 `split_hash`、candidate IDs hash 与 target IDs hash。

### 核心观察

| 场景 | 期待 | 实际观察 | 判断 |
|---|---|---|---|
| 真实 cold path | 第一次生成并保存 split | 使用真实 PyG `Data` 在临时 canonical root 写入 data pickle、dataset pickle 和 manifest，状态为 `created` | `PASS` |
| 真实 warm path | 后续命中，不重切、不覆写 | 状态为 `reused`；三份文件的 bytes 与 `mtime_ns` 全部不变；cold/warm `data_identity`（含 `split_hash`）一致 | `PASS` |
| seed 隔离 | model/selector/unlearning seed 不改变 dataset split | model seed 42 与 212 产生完全相同的 profile、比例和 `split_seed=2024` 参数；显式 processed provider 测试证明 downstream 不调用 split 函数 | `PASS` |
| Cache V2 身份 | split 是 cache 输入而不是新 cache 目录 | Recipe 强制并保留 `data_identity.split_hash`、candidate hash；runner 同时写入完整 split contract | `PASS` |
| clean candidate 回归 | 当前候选整体成立 | 实现检查点 `439b876c` 与当前 report-bearing clean HEAD 均重跑相关集合；`111 passed`，dashboard projection check 通过 | `PASS` |
| registered dry-run | 错误环境不能物化或运行正式实验 | Cora/seed42/1% dry-run 绑定当前 clean HEAD，在非 main、非 AutoDL、设备不符、profile/receipt 缺失处停止；`generated_artifacts=[]`，本地 processed 文件数仍为 0 | `PASS · scoped` |

### 当前决定

> 当前验收决定：`待决定`

**Agent 建议：建议接受。** 本候选把 split 从隐式运行行为收敛为 YAML 声明、一次持久化、后续复用的独立数据状态，并用实际文件行为和 cache identity 验证了这一点；没有启动正式实验或改变科研结论。

决定人：刘丞毓。可以接受当前候选，或指出具体返工项。

## 关键判断详情

### 1. YAML 是否真的进入运行链 — `PASS`

在 formal recipe 声明 split 后，系统需要把它一路传到数据准备和 GU，而不是只把 YAML 当文档。实际 config loader 要求 split mapping 完整且与注册默认一致；Selection runner 接收 profile、三个比例和 split seed，生成的 GU YAML 保留同一 mapping，adapter 再与外部 manifest 和 checkpoint metadata 交叉校验。因此 YAML 是执行输入，不是旁路说明。

### 2. split 是否是可复用的独立状态 — `PASS`

在首次缺失 profile 的场景中，`stage_profile` 使用固定 split seed 生成 masks，并原子保存 OpenGU canonical pair 和 manifest。在第二次相同调用中，系统没有再次调用划分或写文件，而是验证 manifest、pickle SHA-256、图身份、masks 和 selection identity 后返回 `reused`。测试逐文件比较 bytes 与纳秒级修改时间，支持“一次生成、之后复用”的判断。

### 3. 实验 seed 会不会重新切 dataset — `PASS`

在 model seed 分别为 42 和 212 的场景中，launcher 产生的 split 参数完全相同；split seed 始终由 YAML 合同提供的 2024 决定。OpenGU `process_data` 在显式 processed root 下只允许加载已注册 pair，测试把所有 split/save 函数替换成失败钩子后仍成功加载，因此 selector 和 unlearning 阶段不会借自己的 seed 重切 dataset。

### 4. Cache 是否需要按 split 建多个根 — `PASS`

不需要。持久化 split 是 processed profile；Cache V2 继续是一个 exact-recipe store。不同 split 的实际 masks 会改变 `split_hash`，候选集会改变 candidate IDs hash，从而形成不同 Recipe 身份并自然 miss；相同 profile 与相同实际 masks 才能 hit。这样分开了“数据状态持久化”和“选择证据缓存”，没有复制一套 split-specific cache 系统。

### 5. 正式入口是否 fail closed — `PASS · scoped`

在本机对注册 Cora/seed42/1% gate 执行 dry-run。期待它读取当前 recipe，但不得在错误机器上自动创建正式 split 或实验 Artifact。实际 preflight 识别到分支、checkout、GPU、profile 与 Selection receipt 均不满足正式条件，返回非零退出和 `generated_artifacts=[]`；精确 profile path 仍不存在，本地 `data/processed` 文件数为 0。该结果只证明 gate 和零物化，不等于正式 GPU 实验通过。

## 已知缺口与边界

- `NOT OBSERVED` — 未在 AutoDL RTX 4090/main checkout 上进行正式 cold materialization、Selection/GU gate 或完整矩阵。
- `NOT OBSERVED` — 未产生攻击效果、遗忘效果、隐私或论文结论；AAGU-006 只修复数据/split 执行合同。
- `NOT CONFIRMED` — AAGU-019 的旧小预算 setup 硬退役仍是独立 Block，不在本候选中。
- AAGU-024 及其候选未被本 Block 修改；它不是 AAGU-006 的验收前置。

## 技术复核入口

- 权威 recipe：[`experiments/configs/syncmate_target_direct_formal_v2.yaml`](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml)
- 通用 split contract：[`experiments/processed_provider.py`](../../../experiments/processed_provider.py)
- cold/warm materializer：[`experiments/target_direct_v1/split_profile.py`](../../../experiments/target_direct_v1/split_profile.py)
- 正式 launcher：[`experiments/target_direct_v1/syncmate_stage.py`](../../../experiments/target_direct_v1/syncmate_stage.py)
- Cache identity consumer：[`experiments/target_direct_v1/run_selection.py`](../../../experiments/target_direct_v1/run_selection.py)
- 真实 cold/warm 测试：[`tests/test_target_direct_split_profile.py`](../../../tests/test_target_direct_split_profile.py)
- 当前 Record：[`WORKITEM.md`](WORKITEM.md)
- Apply target：`refs/heads/codex/e7-two-surrogate-groups-20260805`
