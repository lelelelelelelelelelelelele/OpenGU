# Target-direct Selection→GU 正式实验准备报告

日期：2026-07-24

实施合并：`main` merge commit `71076bc`

2026-07-24 收口前复核基线：`main@fb0d9a332c4086e98c6c988d6a02851a8d7a2b79`

> [!IMPORTANT]
> **结论：旧 153-cell 矩阵不是严格白盒实验。** 它使用 GateGCN hidden=16、200 epochs 的 selector 去影响 OpenGU GCN hidden=64、100 epochs 的 GNNDelete target，且实际每格只删除 7 个节点。它应保留为 **L1 surrogate-transfer / engineering screen**，不能支持“新 IF 普遍优于旧 IF、random 或 degree”的 target-direct 结论。

> [!SUCCESS]
> **修正链已经通过 `--no-ff` 合入 `main`，2026-07-24 复核未发现新的 correctness blocker，但正式结果尚未产生。** 收口前本机、`origin/main` 与 SSH active checkout 同为 `fb0d9a3`；正式执行仍须等待 SSH 恢复 RTX 4090 与 accepted `gnn_20` 环境，并先在 active checkout stage/verify 三个 70/10/20 processed pairs。

## 1. 为什么旧实验是 surrogate transfer

validation CE 作为 selection target、test F1 作为最终评估，本身是正确的防止 test leakage 设计。问题不在两个指标不同，而在它们对应的 selector 与 GU target 不是同一个模型状态。

| 层级 | selector 与 GU target 的关系 | 能回答的问题 |
|---|---|---|
| target-direct white-box | 同一份持久化 pre-unlearning checkpoint；文件哈希和 state hash 均相同 | 某 selector 直接作用于实际被遗忘目标时是否有效 |
| L1 surrogate transfer | 同任务、相关模型族，但架构超参、训练过程或最终 state 不同 | 排名能否迁移到另一个目标模型 |
| 更强 transfer | 模型族或任务也不同 | 更广义跨模型迁移 |

旧实验属于 L1：虽然两者都可称为 GCN 系，但 hidden size、训练轮数和最终参数状态不同。即使把二者改成相同配置，若分别重训而没有校验同一 state hash，也仍不构成严格 target-direct white-box。

此外，旧目录名和配置保留了 `r=0.05`，实际 external Selection Artifact 却固定为 `k=7`。三个数据集的配置期望/实际删除数分别为 Cora `135/7`、CiteSeer `166/7`、PubMed `985/7`；旧 GNNDelete 只告警后继续。这使旧 PubMed 的有效删除比例尤其低，足以解释其部分“17 法都没有区别”的现象。

## 2. 新正式实验的科学合同

### 2.1 数据与 split

- canonical source 只允许位于 SSH active checkout：`/autodl-fs/data/OpenGU/GULib-master/data/raw/<dataset>/`。
- OpenGU split pair 只允许位于：`data/processed/transductive/`。
- 固定 profile：`planetoid_70_10_20_seed2024`。
- train/validation/test 必须互斥且穷尽全图；全图用于 message passing。
- selector candidate pool 仅为 train mask；selection target 仅为 validation-mask mean CE。
- test labels 只用于最终 test F1，不进入 selection、调参或 gate 决策。

分割算法的单一事实源现为 OpenGU 公共纯模块 `utils/node_split.py`：
原生 `transductive_split_node` 与 target-direct profile materializer 使用同一
randperm、ratio/count、mask、indices 和 induced-edge 实现。公共模块不导入
`config.py`，显式接受 ratio 以及 `split_seed` 或调用者提供的 Generator；
未提供二者时仍使用 torch 全局 RNG，保持 OpenGU 原生默认行为。
`split_profile.py` 不再另写分割算法，只负责 canonical path、materialize/verify、
manifest、文件哈希、mask 互斥/穷尽和 Selection candidate identity。

不继续使用 80/0/20，是因为其 validation mask 为空；17 个 IF/TracIn 公式需要一个与 train、test 均隔离的 target objective。用 test labels 会泄漏，用 train labels则改变问题定义。

### 2.2 预算

`70/10/20` 是防止 test leakage 的 split 身份；`r∈{0.01,0.05}`
是删除预算。两者是正交维度，不能相互替换。每个 ratio 都以 verified
train candidate count 为唯一分母：

$$
k(r) = \max\left(1,\left\lfloor r\,|V_{train}|\right\rfloor\right),
\qquad r\in\{0.01,0.05\}.
$$

| Dataset | 全图节点 | 理论 train/val/test | $k$（1% train） | $k$（5% train） |
|---|---:|---:|---:|---:|
| Cora | 2,708 | 1,895 / 271 / 542 | 18 | 94 |
| CiteSeer | 3,327 | 2,328 / 333 / 666 | 23 | 116 |
| PubMed | 19,717 | 13,801 / 1,972 / 3,944 | 138 | 690 |

这些是按节点总数推导的预期值；正式值必须由 SSH staged manifest 实测并冻结。`expected_k` 会作为唯一事实源同时传给 Selection 和 GNNDelete。任何 `actual_k != expected_k`、重复节点或越出 train candidates 都立即失败。

现有 17 法都是 budget-independent score/ranking prefix。每个
`(dataset, model seed)` 只允许一次 cold ScoreBundle 计算；1% 与 5%
Selection Artifacts 从同一 immutable score identity 分别物化，并在
Selection Recipe 中显式绑定 ratio、分母、rounding 与 `expected_k`。
未来若加入 budget-conditioned 方法，必须使用独立 score recipe，禁止伪共享。

### 2.3 严格白盒 checkpoint 绑定

每个 `(dataset, model seed)` 只训练一次 OpenGU GNNDelete target，并持久化最终 state 与 6 个 trajectory checkpoints。随后：

1. ScoreBundle 从这份 checkpoint 计算 17 个 score/ranking；
2. 该 seed 的 17 个 Selection Artifact 全部引用同一 checkpoint state hash；
3. 每个 GNNDelete cell 加载同一 checkpoint，不重新训练“近似相同”的 target；
4. `attack.json` 记录实际观察到的 checkpoint 文件 SHA-256 和 state hash；
5. retained-data retrain reference 清除 checkpoint binding，从随机初始化重新训练。

checkpoint metadata 同时绑定 dataset/split fingerprint、模型结构、训练 seed/epochs、ratio-neutral 的 verified candidate pool identity 与 Git provenance。删除 ratio 与 `expected_k` 则绑定在 Selection Recipe、manifest 和 GU config；任何不一致均 fail closed。

### 2.4 参数域与可行性

主矩阵固定使用 `parameter_scope=last_layer`。它仍是 target-direct white-box，因为参数来自同一实际 target checkpoint，但明确属于“last-layer IF approximation”，不能写成 full-parameter exact IF。当前 2-layer、hidden=64 GCN 下，last-layer / all-trainable 参数维数分别为：Cora `455/92,231`、CiteSeer `390/237,446`、PubMed `195/32,259`。

`all_trainable` 不配置、不调度，也不是本轮扩展条件。现有 IF 文献已记录全参数 Hessian/IHVP 的扩展成本，以及层级或最后一层近似的可行性路径；本轮只如实限定 claim，而不支付独立 stress ladder 的计算成本。文献依据与边界集中列在 `target_direct_formal_preflight_AUDIT_REPORT.md` 的 “Why `last_layer` is retained” 一节。未来若研究全参数 IF，必须另立成本/近似合同，使用新的 parameter-schema hash、Recipe 和 Cache V2/结果身份；不得在当前 3×3 主矩阵中切换 scope 或复用 warm artifact。

## 3. 正式执行顺序

| Gate | 内容 | 通过条件 |
|---|---|---|
| G0 分支验收 | 本地单元/集成测试、CLI、静态检查、报告 | 无本次代码失败；实现报告一致 |
| G1 数据 preflight | 在 SSH active root stage/verify 三个 70/10/20 pairs | 路径、realpath、source/data/split hashes、counts 全部冻结且位于 active checkout |
| G2 Selection gate | Cora seed 42、last-layer：1% 首次 cold ScoreBundle，5% 从同一 immutable score identity cold 物化；两者各做 exact warm reuse | 34/34 ratio-conditioned Selection Artifacts；4 summaries + receipt；仅一次 ScoreBundle producer；cold/warm timing、显存、失败状态齐全 |
| G3 双预算 GU gates | Cora seed 42 的 degree 分别跑 1% 与 5% 两个 cell | 2/2 cells、8/8 文件；各自 ratio/k、checkpoint/state/count/provenance 一致；无 failure |
| G4 候选单 stage | 双 gate 通过且另获扩展授权后，跑同一 Cora seed 的 17 selectors × 2 ratios | 34/34 cells、136/136 files，通过 checksum 验证 |
| G5 候选完整矩阵 | 3 datasets × 3 seeds × 17 selectors × 2 ratios | 候选规模 306 cells、1,224 四件套；**当前未授权执行**；失败单独记录，绝不静默跳过 |

模型 seeds 沿用 `42, 212, 2024`；split seed 固定为 2024，因此三个模型 seed 共享同一数据划分，只改变训练随机性与 random selector。

若正式 gate 暴露代码缺陷，必须停止矩阵，从 pinned `main` 建修复分支，测试并合入后以新 SHA、新 cache/result identity 重启 gate；旧 SHA 的格只保留为诊断证据。

## 4. 时间、显存和失败状态的记录口径

每个 selection summary 将同时记录：

| 字段 | 含义 |
|---|---|
| `score_bundle.cold_total_seconds` | 冷启动时，共享计算、17 法公式/排序、payload 校验与 ScoreBundle 落盘的总时间 |
| `method_timings.<name>.formula_seconds` | 该方法从共享中间量形成 score 的实测时间 |
| `method_timings.<name>.ranking_seconds` | 稳定排序的实测时间 |
| `method_timings.<name>.materialization_seconds` | 生成/校验 Selection Artifact 的实测时间 |
| `cold_incremental_seconds` | 每法公式 + 排序 + 物化；不重复计算共享前置成本 |
| `cold_standalone_equivalent_seconds` | 若该法单独 cold 运行，共享前置成本 + 该法增量的等价口径 |
| `cold_amortized_17way_seconds` | 一次生成 17 法时，共享成本按 1/17 分摊后的每法口径 |
| `score_bundle.warm_read_seconds` | 第二次运行 strict warm cache 的读取/验证时间；producer 必须未调用 |
| `gpu_memory.*` | target training、ScoreBundle 及整个进程的 peak allocated/reserved bytes |
| `status.state/failure` | success 或 exception type/message；失败也原子写 summary |

这避免把共享图梯度/Hessian/trajectory 工作重复计入 17 次，也保留“单法独跑大约多贵”的可解释口径。

GU 每格继续生成 `attack.json`、`collateral.json`、`predictions.npz`、`_meta.json`。分析至少报告 target F1 before/after/drop、retrain gap、collateral effect、MIA/update-detection AUC、wall-clock/inner time、失败状态与 checkpoint identity。

## 5. 要回答的两个核心问题

### Q1：TracIn 是否比 degree/random 更强？

- 每个 dataset-seed 做 paired comparison；不只看 pooled win count。
- 报告 `ΔF1_drop`、retrain-gap 改善、top-k overlap 和运行成本。
- 汇总 9 个 paired cells 的 win/tie/loss、均值/中位数和 bootstrap CI。
- Cora-only 优势不得写成跨数据集普遍优势。

### Q2：IF 簇内部哪种公式效果更好且可行？

- 先比较 A/B/C/D 及 point/simple/graph、single/checkpoint 变体的组内 ranking 相似性。
- 再比较 ranking 相似性是否转化为 GU outcome 相似性。
- 分开报告 reference/proxy fidelity、实际 GU 效果和计算代价，不能用 proxy 接近 GT 直接替代 GU 有效。
- PubMed 必须按真实 1%/5% 的 `k=138/690` 重测；旧 `k=7` null regime 不再作为 dataset-insensitive 证据。

## 6. 已完成实现

| 模块 | 修正 |
|---|---|
| `utils/node_split.py` | 无 `config.py` 副作用的公共 deterministic split；原生 OpenGU 与 E8 共用 |
| `utils/target_checkpoint.py` | target checkpoint 原子保存/加载、文件哈希、state hash、trajectory 与 data identity 校验 |
| `experiments/target_direct_v1/` | 薄 70/10/20 profile staging/verification、target-direct recipe、17 法 ScoreBundle、manifest/adapter、GU config builder |
| `attack/pipeline_adapter.py` | formal expected-k 单一事实源、candidate/count fail-closed、retrain 清除 target binding |
| `unlearning/.../gnndelete.py` | 精确加载 target checkpoint，校验 metadata/data/state，禁止 formal warning 后继续 |
| `experiments/run.py` | 新 `target_direct_external_selection` 模式，把 checkpoint 与 expected-k 传给 attack/collateral |
| `AttackResult/Manager` | 把实际加载 checkpoint 的 path/file/state hashes 写入结果 |
| `GNNDeleteTrainer` | 捕获指定 epoch 的 target trajectory checkpoints |

旧 Cache V2 与旧 k=7 result identity 不覆盖、不续跑。

## 7. 本地验证与边界

- 2026-07-24 复核套件：target checkpoint、split、expected-k、runner propagation、Cache V2、GNNDelete architecture 与完整 SyncMate tests 共 `316 passed, 1 warning`。
- 双预算 runner/manifest/SyncMate 定向测试：`197 passed`；包含 target checkpoint、split profile、Cache V2、budget planner 与 GU aggregate 的扩展组合：`242 passed, 1 warning`；公共 split、原生 OpenGU、target-direct recipe/manifest/SyncMate 与 processed-provider 最终定向组合：`28 passed`。
- 受影响 Python 模块 `py_compile`、`git diff --check` 与 SyncMate temporary smoke 通过；canonical Selection preflight、1%/5% GU dry-run 均按预期 fail closed，没有生成 formal artifact。
- 本地没有可用 CUDA，也没有在隔离 worktree 复制正式数据，因此没有把本地 smoke 当作正式格；正式 GPU 工作仅能在已接收的 SSH active `main` 执行。
- 2026-07-24 SSH 复核：`nvidia-smi` 仍返回 `No devices were found`，`/root/miniconda3/envs/gnn_20/bin/python` 不存在；canonical raw 三套已在 active checkout，但 `planetoid_70_10_20_seed2024` processed pairs 尚未 stage。

## 8. 当前验收结论与下一步

当前状态是 **implementation accepted and re-reviewed，formal experiment blocked by runtime availability**。还不能说“A.7 已完成”，也不能用旧矩阵回答新 IF 与 baseline 的白盒优劣。

在 SSH 基础设施恢复后，先在非计时 G1 stage/verify 三个 processed profiles，再做 Cora seed42 的 G2；随后分别执行 1% 与 5% 的 G3 `degree` formal gate。两个 gate 都通过也只完成 canary 验收，G4/G5 的 306-cell 候选扩展仍需用户另行明确授权，不会自动启动。远端 results 必须经 SyncMate collect→逐文件 SHA-256 verify→trusted index/results 回传本地。

`all_trainable` 不进入本轮配置或排期；它仅作为未来可能另行批准的研究问题保留。若重新启动，必须先完成独立成本/近似合同与分块或落盘可行性设计，再建立新的 full-parameter matrix。
