# Target-direct Selection→GU 正式实验准备报告

日期：2026-07-23

分支：`codex/fix-target-direct-selection-20260723`

父提交：`main@fc27f70e92b8544cf68e368953e5c35806a71328`

> [!IMPORTANT]
> **结论：旧 153-cell 矩阵不是严格白盒实验。** 它使用 GateGCN hidden=16、200 epochs 的 selector 去影响 OpenGU GCN hidden=64、100 epochs 的 GNNDelete target，且实际每格只删除 7 个节点。它应保留为 **L1 surrogate-transfer / engineering screen**，不能支持“新 IF 普遍优于旧 IF、random 或 degree”的 target-direct 结论。

> [!SUCCESS]
> **修正链已经在隔离分支实现并通过本地定向测试，但正式结果尚未产生。** 下一步必须先验收并以 `--no-ff` 合入 `main`，然后从 SSH active clean checkout 的新 `main` SHA 启动数据 preflight 和 GPU gate；不得从本分支/worktree 直接跑正式格。

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

不继续使用 80/0/20，是因为其 validation mask 为空；17 个 IF/TracIn 公式需要一个与 train、test 均隔离的 target objective。用 test labels 会泄漏，用 train labels则改变问题定义。

### 2.2 预算

首轮只跑 `r=0.05`，并以 train candidate count 为唯一分母：

$$
k = \max\left(1,\left\lfloor 0.05\,|V_{train}|\right\rfloor\right).
$$

| Dataset | 全图节点 | 理论 train/val/test | 理论 $k$（5% train） |
|---|---:|---:|---:|
| Cora | 2,708 | 1,895 / 271 / 542 | 94 |
| CiteSeer | 3,327 | 2,328 / 333 / 666 | 116 |
| PubMed | 19,717 | 13,801 / 1,972 / 3,944 | 690 |

这些是按节点总数推导的预期值；正式值必须由 SSH staged manifest 实测并冻结。`expected_k` 会作为唯一事实源同时传给 Selection 和 GNNDelete。任何 `actual_k != expected_k`、重复节点或越出 train candidates 都立即失败。

`r=0.10` 若后续需要，将使用独立 result/cache identity 做 ratio sweep，不与 5% 主矩阵混写。

### 2.3 严格白盒 checkpoint 绑定

每个 `(dataset, model seed)` 只训练一次 OpenGU GNNDelete target，并持久化最终 state 与 6 个 trajectory checkpoints。随后：

1. ScoreBundle 从这份 checkpoint 计算 17 个 score/ranking；
2. 该 seed 的 17 个 Selection Artifact 全部引用同一 checkpoint state hash；
3. 每个 GNNDelete cell 加载同一 checkpoint，不重新训练“近似相同”的 target；
4. `attack.json` 记录实际观察到的 checkpoint 文件 SHA-256 和 state hash；
5. retained-data retrain reference 清除 checkpoint binding，从随机初始化重新训练。

checkpoint metadata 同时绑定 dataset/split fingerprint、模型结构、训练 seed/epochs、候选预算与 Git provenance。任何不一致均 fail closed。

### 2.4 参数域与可行性

主 gate 先使用 `parameter_scope=last_layer`。它仍是 target-direct white-box，因为参数来自同一实际 target checkpoint，但明确属于“last-layer IF approximation”，不能写成 full-parameter exact IF。

另加 Cora seed 42 的 `all_trainable` feasibility/fidelity gate，比较：

- 总时间与峰值显存；
- 是否出现 OOM/数值失败；
- 与 last-layer 的 Kendall/Spearman、top-k overlap；
- GU outcome 是否改变。

只有该 gate 证明全参数口径可承受，才扩展到其余 8 个 dataset-seed stage。这样同时回答“效果更强吗”和“代价是否可行”。

## 3. 正式执行顺序

| Gate | 内容 | 通过条件 |
|---|---|---|
| G0 分支验收 | 本地单元/集成测试、CLI、静态检查、报告 | 无本次代码失败；实现报告一致 |
| G1 数据 preflight | 在 SSH active root stage/verify 三个 70/10/20 pairs | 路径、realpath、source/data/split hashes、counts 全部冻结且位于 active checkout |
| G2 Selection gate | Cora seed 42、5%、last-layer，一次生成全部 17 法；随后 exact warm reuse | 17/17 artifacts；cold/warm timing、ScoreBundle 总时、显存、失败状态齐全；warm producer 未调用 |
| G2b 参数域 gate | 同格 all-trainable | 无 OOM/NaN；形成耗时、显存、ranking fidelity 证据 |
| G3 GU 一格 | Cora seed 42 的 degree 先跑一个 cell | 四件套完整；checkpoint/state/count/provenance 一致；无 failure |
| G4 单 stage | G3 通过后跑同一 Cora seed 的 17 cells | 17/17 cells、68/68 files，通过 checksum 验证 |
| G5 全矩阵 | 3 datasets × 3 seeds × 17 selectors | 153/153 cells、612/612 四件套、0 identity drift；失败单独记录，绝不静默跳过 |

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
- PubMed 必须按真实 `k≈690` 重测；旧 `k=7` null regime 不再作为 dataset-insensitive 证据。

## 6. 已完成实现

| 模块 | 修正 |
|---|---|
| `utils/target_checkpoint.py` | target checkpoint 原子保存/加载、文件哈希、state hash、trajectory 与 data identity 校验 |
| `experiments/target_direct_v1/` | 70/10/20 profile staging、target-direct recipe、17 法 ScoreBundle、manifest/adapter、GU config builder |
| `attack/pipeline_adapter.py` | formal expected-k 单一事实源、candidate/count fail-closed、retrain 清除 target binding |
| `unlearning/.../gnndelete.py` | 精确加载 target checkpoint，校验 metadata/data/state，禁止 formal warning 后继续 |
| `experiments/run.py` | 新 `target_direct_external_selection` 模式，把 checkpoint 与 expected-k 传给 attack/collateral |
| `AttackResult/Manager` | 把实际加载 checkpoint 的 path/file/state hashes 写入结果 |
| `GNNDeleteTrainer` | 捕获指定 epoch 的 target trajectory checkpoints |

旧 Cache V2 与旧 k=7 result identity 不覆盖、不续跑。

## 7. 本地验证与边界

- 本次受影响路径定向测试：`183 passed, 1 warning`。
- 更宽定向组合：`191 passed`；另有 1 个旧 `gu_target_v1` 测试失败，因为它把 `evidence_root` 冻结成另一个 worktree 的绝对路径。该失败与 target-direct 行为无关，已单独记录，不计作通过。
- `compileall`、4 个新 CLI 的 `--help`、`git diff --check` 均通过。
- 本地没有可用 CUDA，也没有在隔离 worktree 复制正式数据，因此尚未做 disposable GPU end-to-end smoke；正式 GPU 工作必须等合入 main 后在 SSH active checkout 执行。

## 8. 当前验收结论与下一步

当前状态是 **implementation ready for review，formal experiment not started**。还不能说“A.7 已完成”，也不能用旧矩阵回答新 IF 与 baseline 的白盒优劣。

需要的下一步授权是：验收本分支后提交，并以显式 `--no-ff` 合入 `main`。合并后再生成绑定新 `main` SHA 的 SyncMate recipe，先做 G1→G3；一格通过后按 G4→G5 自动扩展，并把远端 results 逐文件 SHA-256 回传到本地作为正式分析输入。
