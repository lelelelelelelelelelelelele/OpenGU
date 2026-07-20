---
title: Cache V2 SUP Selection 最大 k 复用增补验收报告
date: 2026-07-20
status: accepted-within-selection-scope
---

# Cache V2 SUP Selection 最大 k 复用增补验收报告

## 1. 验收结论

**本次 Selection-only 增补验收通过。** B/C SUP 实验现在会先把多预算归一化，以 `request_max_k` 做唯一 grouped resolve：exact k 优先；没有 exact 时选择 identity 完全一致的最小 `artifact_k >= request_max_k`；仍无覆盖项时只调用一次最大 k producer，并用该有序节点序列的前缀服务所有小 k。

`gt_full`、`p_graph`、`tracin_cp_graph_6` 等 B/C 的 18 个 score method 均已接入正式 Cache V2 Selection Artifact。每个 method/selection identity 只保存一个最大 k Artifact，不创建 k=3、k=7 等子 Artifact。downstream 不再从 ScoreBundle ranking 直接选择节点，而是每个 method 显式加载一次 Selection Artifact，再为各预算取前缀；每个 `(method, k)` result 仍拥有独立记录和 Selection provenance。

| 验收面 | 结果 | 核心证据 |
|---|---|---|
| Legacy 行为 | 保持 | 未修改 `attack/selection_cache.py`；既有大 k 覆盖小 k golden test 纳入 149-test 回归 |
| 多 k cold | 通过 | `[14,7,3]` 每个 method 只调用 k=14 producer 一次；18 个 method 各保存 1 个 Artifact |
| 多 k warm | 通过 | 18/18 Selection hit；fail-if-called 未触发；Selection store path/size/mtime/SHA 序列零变化 |
| 跨次大覆盖小 | 通过 | 已有 k=14 后请求 `[7,3]`：18/18 hit，`request_max_k=7`、`artifact_k=14`，producer=0 |
| covering 优先级 | 通过 | 单测锁定 exact 优先；无 exact 时选择最小 covering k |
| SUP 消费 | 通过 | Cora/seed42 对 `gt_full`、`p_graph`、`tracin_cp_graph_6` 真机验证 |
| results 解耦 | 通过 | 3 methods × 3 budgets = 9/9 独立 result key，全部引用明确 Selection Artifact |
| 回归 | 通过 | Cache V2、B/C、Legacy strategy golden 共 150 passed in 7.70s |

## 2. 最终行为契约

对同一 selection identity 的预算集合 `K`：

~~~text
budgets 14,3,7,3
  -> validate + deduplicate
  -> canonical max-first order [14,7,3]
  -> grouped lookup request_max_k = 14

exact k=14 exists
  -> load once; k=14/7/3 use nodes[:k]

otherwise compatible k=20 and k=30 exist
  -> choose k=20; load once; use nodes[:k]

otherwise only smaller k=7 exists
  -> not a group hit
  -> producer(14) once; save k=14; fan out prefixes
~~~

covering 只忽略 Recipe 中的 `k`。dataset fingerprint、graph fingerprint、candidate set hash、node-id space、selector、selector seed、algorithm/producer version、source Score Artifact 和全部 selector parameters 必须 canonical 等价。任何 identity 变化都 miss；冲突、损坏、未验证 Artifact 继续 fail closed。

只有显式声明 `prefix_stable=true` 的 experiment adapter 才能启用该行为。B/C ScoreBundle 的 ranking 契约是 `score_desc_node_id_asc`，因此这 18 个 method 满足稳定前缀条件。Cache 不硬编码 `gt_full` 或 TracIn 名称，SUP 名称与 Score ranking 的解释仍归 experiment 层所有。

## 3. 代码增补

| 文件 | 修改内容 |
|---|---|
| `cache_v2/index.py` | 新增按 Artifact type 的确定性、只读、逐行契约校验枚举，为 Selection covering resolver 提供 metadata 候选 |
| `cache_v2/selection_materializer.py` | 保留 exact resolver；新增 exact→最小 covering k 的 Selection-only resolver；选中后仍走原 exact/integrity 校验 |
| `experiments/selection_budget_planner.py` | 新增 budgets 去重降序、最大 k 单次 producer、prefix fan-out、逐 k provenance 与 manifest 生成 |
| `experiments/bc_target_v2/run_selection.py` | 18 个 Score ranking 各物化一个 max-k Selection Artifact；selection summary 升级为 v2 |
| `experiments/bc_target_v2/run_downstream.py` | 要求 v2 summary；按显式 Artifact ID 每个 method load 一次；每个 result 记录 Artifact/prefix provenance |
| `experiments/bc_target_v2/run_matrix.py` | 新增 `--budgets` 与可选 `--selection-cache-root` 透传 |
| `tests/test_selection_budget_planner.py` | 新增 cold/warm/zero-write/covering/exact/identity/prefix-stable/fail-if-called 测试 |
| `tests/test_bc_target_v2.py` | 新增乱序和重复 budgets CLI 归一化测试 |

ScoreBundle store 保持现状：它继续使用 B/C 实验自有的 `index.sqlite3`。正式 Selection Artifact 使用独立的 `selection_artifacts/index.sqlite`；没有迁移、改写或混用两个 index，也没有修改 Score、Prediction 或 Evaluation Artifact 契约。

## 4. Summary 与 provenance 增补

`bc_target_v2.selection_summary` 从 version 1 升级到 version 2，新增：

~~~text
selection_cache
  root / request_max_k / method_count
  hit_count / miss_saved_count / producer_call_count

selection_artifacts[method]
  request_max_k / artifact_k
  cache.hit / cache.lookup_policy
  artifact.artifact_id / recipe_hash / content_hash
  artifact.source_score_artifact_id
  views[k].cache_outcome / prefix_reuse / reuse_kind / selected_nodes
~~~

逐 k provenance 口径：

| 场景 | 最大请求 | 小请求 |
|---|---|---|
| cold | `cache_miss_saved` | `same_run_prefix_reuse` |
| exact warm | `cache_hit` | `cache_hit_prefix_reuse` |
| larger-k warm | `cache_hit_prefix_reuse` | `cache_hit_prefix_reuse` |

downstream summary/recipe 同步升级为 version 2，并把每个使用的 Selection Artifact identity 纳入 downstream recipe。结果仍按 `(method, budget)` 分开记录；Selection 的前缀复用不用于推导任何非线性 downstream metric。

## 5. 自动化测试

最终回归命令：

~~~powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_cache_v2.py `
  tests/test_cache_v2_archive_readiness.py `
  tests/test_cache_v2_conflict_resolution.py `
  tests/test_cache_v2_dataset_boundary.py `
  tests/test_cache_v2_formal_artifacts.py `
  tests/test_cache_v2_gate3_comparison.py `
  tests/test_cache_v2_gate3_degree_adapter.py `
  tests/test_cache_v2_gate4_canary.py `
  tests/test_cache_v2_materializer.py `
  tests/test_cache_v2_runtime.py `
  tests/test_cache_v2_selection_canary.py `
  tests/test_cache_v2_store.py `
  tests/test_selection_budget_planner.py `
  tests/test_bc_target_v2.py `
  tests/test_strategy_goldens.py -q
# 150 passed in 7.70s
~~~

新增测试直接证明：

- cold `14,3,7,3` 归一化后只调用 `producer(14)` 一次；
- warm 同组 producer=0，且 store 文件状态零写；
- k=10、k=14 同时存在而请求 max=7 时选 k=10；
- k=7 exact 与 k=14 同时存在时优先 k=7；
- 只有较小 Artifact 时不能覆盖较大请求，必须计算新的最大 k；
- selector seed 等 identity 变化不能复用；
- 未声明 `prefix_stable=true` 时拒绝 max-k 复用；
- Legacy IM 的既有大 k→小 k 行为没有回归。

测试只有既有 `llvmlite/pkg_resources` deprecation warnings，无失败或新增 warning 类别。

另以 final canary 的一份 v2 selection + 一份 v2 downstream 执行 aggregate smoke：`selection_cells=1`、`downstream_cells=1`、`selection_rows=42`、`downstream_rows=9`，成功生成 `matrix_summary.json` 及 6 个 CSV；因此 `run_matrix --stage all` 的末端汇总契约未被 schema v2 截断。单 seed 输入下 `cross_seed_stability.csv` 为空是预期行为。

## 6. Cora/seed42 最终 canary

最终 canary 使用当前代码、CPU、真实 Planetoid Cora，所有输出与 Cache 均位于独立系统临时目录：

~~~text
C:\Users\ADMIN\AppData\Local\Temp\opengu_cache_v2_sup_maxk_final_desc_20260720
~~~

没有把 canary 写入仓库 active Cache、Legacy cache 或历史 results。

### 6.1 Cold / warm / future-smaller

| 项目 | cold `[14,7,3]` | warm `[14,7,3]` | 已有 k=14 后 `[7,3]` |
|---|---:|---:|---:|
| Score Artifact | `score_a4403e0f_1635edf3` | 同一 Artifact hit | 同一 Artifact hit |
| Selection hit / miss | 0 / 18 | 18 / 0 | 18 / 0 |
| Selection producer | 18 次，均只产 k=14 | 0 | 0 |
| end-to-end | 61.267s | 3.137s | 3.091s |
| store 文件数 | 38 | 38 | 38 |
| store 零写 | 不适用 | true | true |

输入 CLI 为 `3,14,7,3`，summary canonical budgets 为 `[14,7,3]`。cold 中三个重点 SUP 的 k=7 节点都逐项等于各自 k=14 的前 7 项；future-smaller 中它们均记录 `request_max_k=7`、`artifact_k=14`、`reuse_kind=cache_artifact_prefix`。

| method | Selection Artifact | k=14 Recipe | k=14 content |
|---|---|---|---|
| `gt_full` | `sel_9f322d5e_98386c3a` | `9f322d5e5051…` | `98386c3af4d2…` |
| `p_graph` | `sel_c44b45af_6d5d4348` | `c44b45afd0bf…` | `6d5d43489ee2…` |
| `tracin_cp_graph_6` | `sel_97b6c1dd_1944dff0` | `97b6c1dd39d4…` | `1944dff0aed2…` |

warm 与 future-smaller 前后都比较了 Selection store 全部文件的相对路径、size、mtime UTC ticks 和 SHA-256；两次比较均完全相同。`--fail-if-producer-called` 同时约束 Score 和 Selection producer，命令正常退出。

### 6.2 Artifact-backed downstream

只选择 `gt_full`、`p_graph`、`tracin_cp_graph_6`，对 k=3/7/14 执行真实 set-deletion downstream：

| 检查 | 结果 |
|---|---|
| downstream schema | `bc_target_v2.downstream_summary` version 2 |
| result keys | 9/9 唯一 `(method,budget)` |
| Selection Artifact | 3 个；每个 method 只使用 1 个 k=14 Artifact |
| provenance | 9/9 result 均包含 Artifact ID、Recipe/content hash、requested/max/artifact k 与 reuse kind |
| prefix 一致性 | 9/9 `selected_rank_order` 与 selection manifest 对应前缀逐项一致 |
| training | 8 个唯一 selected set 训练；1 个跨 method 完全相同的 k=3 set沿用既有 memo 语义复用 observation |
| runtime | 22.567s |

“8 次训练、9 个 result”不是从大 k result 推导小 k result：它只表示 `gt_full` 与 `p_graph` 的一个 k=3 selected set 完全相同，因此沿用了改动前就存在的 identical-set memo。9 个 result 仍分别存在并可单独验收。

## 7. 机器证据校验和

| 文件 | SHA-256 |
|---|---|
| `selection_cold.json` | `bb0da22455cb676180b7acfa1935e405bf0946fb9b1225477fc5f3f56e5160a2` |
| `selection_warm.json` | `497c6d75225ef11dc516efbd7d2b9305a262d6503518dd38bab3b50381d117cf` |
| `selection_covering.json` | `c976bb98065504d87c5aabcae52bdeea23e7c0bc44c5a44900bfd273e2f479f8` |
| `downstream_three_sup.json` | `e16298ae9de87fe0c1805417c10d57741190c74bf8534e754a0670adacf34108` |

这些文件是本地临时 canary 证据，可能随系统临时目录清理；本报告保存了验收数值与校验和，但没有把完整实验 JSON 加入 Git。

## 8. 兼容性与使用方式

`run_matrix` 现在可直接接受：

~~~powershell
E:/conda_package/envs/gnn/python.exe -m experiments.bc_target_v2.run_matrix `
  --datasets Cora `
  --seeds 42 `
  --budgets 14,3,7,3 `
  --stage all
~~~

默认 Selection root 为 `<cache-root>/selection_artifacts`，也可用 `--selection-cache-root` 指向独立绝对路径。

旧的 B/C selection summary version 1 没有 Selection Artifact manifest，新的 downstream 会明确拒绝它，而不会退回直接读取 Score ranking。需要用新 selection stage 重新生成 version 2 summary；若原 result 文件已存在，matrix 需按既有规则显式使用 `--overwrite`。由于 B/C Score Recipe 绑定 `run_selection.py` 的 source fingerprint，本次 rollout 后第一次 selection 可能产生一次新的 ScoreBundle cold compute；之后不同预算集合共享同一 Score Artifact，并按本报告规则复用 Selection Artifact。

## 9. 未扩大结论的边界

- 本次只改 Selection 层；没有实现或声称 Score、Prediction、Evaluation 的跨 k 复用。
- 没有创建小 k 子 Artifact，也没有从大 k downstream result 推导小 k result。
- 真机 canary 只覆盖 Cora/seed42 和三个重点 SUP method；没有执行 3 datasets × 3 seeds full matrix，也没有 GPU GU 矩阵。
- B/C 的 18 个 prefix-stable ranking 已全部物化并完成 cold/warm Selection smoke；真实 downstream 只抽验三个指定 method。
- active Legacy cache、active Cache V2 和历史 results 没有迁移、删除或重写授权；本次 canary 只写系统 scratch。
- 当前改动位于 `codex/feat-cache-v2-sup-selection-maxk-20260720`，parent 为 `main@0f904e6`；尚未 commit、push 或 merge。

在上述边界内，Gate S1（语义）、S2（最大 k 调度）、S3（SUP Artifact 消费）和 S4（results/Cache 隔离）均通过。
