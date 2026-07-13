---
title: Cache V2 Citeseer Selection Canary 真机验收报告
date: 2026-07-14
status: selection-canary-accepted
---

# Cache V2 Citeseer Selection Canary 真机验收报告

## 1. 验收结论

**真实 Citeseer Selection cold miss → warm exact hit canary 通过。** 在远端隔离 checkout `83842e6dfb39b36e20725ea632913c5b8c2b8e5f` 上，真实 Planetoid Citeseer 图和项目现有 `IMStrategy` 首次计算产生一个 V2 Selection Artifact；第二个独立进程使用相同 Artifact Recipe 时精确命中同一 Artifact，并由 fail-if-called producer 哨兵证明没有重新执行 IM 计算。

**这不是完整架构 Gate 2 或 runner 切换验收。** 本次只证明隔离 V2 store 中一条真实 Selection producer 路径可安全 miss、写入、校验和命中；`experiments/run.py`、`demo_attack.py`、`eval_collateral.py` 与既有 Cache 查询路径均未接入。Prediction、Evaluation、正式 E1 矩阵和 conflict 解除流程尚未验收，Legacy Cache 也没有获得冻结、迁移或删除授权。

| 验收面 | 结果 | 核心证据 |
|---|---|---|
| 真实 workload | 通过 | Citeseer 3327 nodes；seed 42 的 80/0/20 split；2661 candidates；IM 选 133 nodes |
| cold | 通过 | `hit=false`，`producer_called=true`，producer 总调用数 1 |
| warm | 通过 | `hit=true`，`producer_called=false`，producer 总调用数仍为 1 |
| Artifact 稳定性 | 通过 | Artifact ID、Recipe/content/payload hash、有序节点、payload mtime/size 全部相同 |
| identity 解耦 | 通过 | 修改 `config_name`、YAML path、experiment ID 后仍命中同一 Recipe |
| fail closed | 通过 | `k=134` 必须 miss；篡改副本 payload 必须触发 `ArtifactIntegrityError` |
| Legacy 只读 | 通过 | 三个 Legacy Cache 树的 path/size/mtime/SHA-256 聚合状态前后相同 |
| SQLite | 通过 | integrity `ok`；schema v1；1 Artifact；0 conflict；无多余依赖或 consumer |
| 测试 | 通过 | 本地 147 passed；远端 canary/store/contract 70 passed |

## 2. 为什么选 Citeseer，以及今天没有跑什么

仓库已有实验集合 `experiments/configs/A5_citeseer_r0.05.yaml`，WORKPLAN 将其列为尚无 clean Phase-B 结果的 Citeseer 集合。更准确地说，Citeseer 不是历史上从未触碰过：旧 archive 中有 Phase-B 前的污染数据；但远端 active Legacy ResultCache JSON 为 0/783、SelectionCache JSON 为 0/110、ScoreCache sidecar JSON 为 0/37，`results/runs` 中的 Citeseer 路径也为 0。因此当前没有可引用的 clean Phase-B end-to-end 结果。

本次按讨论先排除 TracIn 和 Hybrid，只选 IM 验证真实 Selection producer。GraphRevoker 也没有纳入正式实验矩阵，因为当前 aggregator 先修问题尚未关闭。没有保留新的“clean runner YAML”：现有 runner 仍会读写 Legacy ResultCache、SelectionCache 和 ScoreCache，直接运行 A5 会越过“Legacy 只读”和“新计算只写 V2”的阶段门。

因此，本次使用 A5 名称只作为 request envelope 标签，不执行 A5 runner，也不让 YAML/config/experiment 字段进入 Artifact identity。

## 3. 被测版本与隔离环境

| 项目 | 值 |
|---|---|
| Git branch | `codex/citeseer-v2-canary-20260714` |
| 被测 commit | `83842e6dfb39b36e20725ea632913c5b8c2b8e5f` |
| fresh code checkout | `/tmp/opengu-citeseer-v2-canary-83842e6/GULib-master` |
| run root | `/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2` |
| dataset root | `/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2/dataset` |
| V2 store root | `/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2/store` |
| evidence root | `/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2/evidence` |
| Legacy snapshot root | `/autodl-fs/data/OpenGU/GULib-master/results` |
| 运行环境 | torch `2.1.2+cu118`；PyG `2.6.1`；Numba `0.65.1`；CUDA available |
| 设备边界 | RTX 4090 24GB 可用，但该 Selection canary 是 CPU/Numba workload，未跑 GPU GU 实验 |

远端原有 dirty checkout 始终保持在原 branch/HEAD，没有切 branch、暂存、清理或执行 canary。代码使用 fresh clone，数据与 V2 store 使用独立绝对路径；store 和 dataset 路径均被程序验证为不在 Legacy `results` 树内。

## 4. Recipe 与真实输入口径

| 字段 | 值 |
|---|---|
| dataset | Planetoid Citeseer，3327 nodes |
| graph fingerprint | `eedd2c0c5748d3818076bf700673781c5079052122988c2df10ab9b9e11c5fc9` |
| candidate split | OpenGU transductive randperm；seed 42；80/0/20 |
| candidates | 2661 |
| candidate set hash | `ada531f36ff1aeddcb8c60658b845d00ec3c3be3ac73f606ad98829c706a450b` |
| selector | IM |
| semantic algorithm | `opengu-im-batch-celf-numba-canary-v1` |
| parameters | propagation 0.1；100 MC rounds；candidate fraction 1.0；selector seed 2024；batch size 5 |
| budget | ratio 0.05；`k=133` |
| producer version | `opengu-im-selection-canary-v1` + source fingerprint |

Recipe 只包含 graph fingerprint、candidate set hash、node ID space、selector/algorithm version、`k` 和真实 IM 参数。`dataset` 名、model 名、YAML path、`config_name`、experiment ID 与展示用 selection ratio 不进入 Recipe。两个 Legacy IM ScoreCache 层均显式关闭，避免“V2 canary 内部又命中旧 ScoreCache”。

## 5. Cold / warm 命中证据

| 字段 | cold | warm |
|---|---:|---:|
| `hit` | `false` | `true` |
| `producer_called` | `true` | `false` |
| producer call count | 1 | 1 |
| resolve time | 34.769674 s | 0.147032 s |
| end-to-end time | 55.117240 s | 2.954911 s |
| miss reasons | `no_exact_candidate` | empty |

resolve 阶段加速为 **236.48×**，端到端加速为 **18.65×**。warm 端到端仍需约 2.95 秒，是因为第二个进程仍会加载并 fingerprint 真实 Citeseer 输入；关键的 IM producer 没有再次执行。

| 不变量 | cold 与 warm 的共同值 |
|---|---|
| Artifact ID | `sel_82ce3701_c25a3ec2` |
| Recipe hash | `82ce3701ea07851534a0b77a615472d25f7af649a3d88f0c0751e34fb6783a02` |
| content / payload SHA-256 | `c25a3ec2d9e44806fbe98444eadacb974b11bbceea78d595bfb0b42524ed0597` |
| ordered nodes hash | `8876e4f21b49bac3e04a94e3e0fd2ee44c8e462d99cb9d0a671d2f21f706950b` |
| selected nodes | 133，顺序逐项完全相同 |
| payload | 1097 bytes；mtime ns `1783973809373716696`，warm 后不变 |

warm 在独立进程中启用 fail-if-called producer 哨兵。如果 resolver 先计算再声称命中，该进程会以错误退出；本次 warm 正常返回 `hit=true`，并且持久化 producer counter 仍为 1。

## 6. Experiment 标签与 Artifact identity 解耦

| request envelope | cold | warm |
|---|---|---|
| `config_name` | `A5_citeseer_r0.05` | `renamed-config` |
| YAML path | `experiments/configs/A5_citeseer_r0.05.yaml` | `elsewhere/renamed.yaml` |
| experiment ID | `cache-v2-citeseer-cold` | `cache-v2-citeseer-warm-different-request` |

三个实验拥有的标签全部改变，但 Recipe hash、Artifact ID 和 content hash 不变，warm 仍 exact hit。这直接验证了“Experiment 是消费者，不拥有 Cache；修改 YAML/config/experiment identity 不 invalid Artifact”的核心契约。

## 7. 负向与完整性测试

| case | 操作 | 已观察结果 | 正式 store 结果 |
|---|---|---|---|
| changed Recipe | warm 请求把 `k` 从 133 改为 134 | 新 Recipe `13a5182c…` 没有候选；触发 `ProducerCalledError` 哨兵，进程退出 2 | Artifact 仍为 1；producer count 仍为 1 |
| tampered payload | 复制 store 后只在副本 payload 末尾追加字节 | header size/content 校验失败，触发 `ArtifactIntegrityError`，进程退出 2 | 原正式 store 未修改；Artifact 仍可正常核验 |

changed-`k` 证明不同 Recipe 不能误命中；tamper 证明损坏 payload 不能被静默当作 hit。篡改只发生在隔离副本，正式 store 与 Legacy 文件都未被更改。

## 8. SQLite、Store 与 Legacy 不变量

### 8.1 正式 canary store

| 检查 | 结果 |
|---|---|
| `PRAGMA integrity_check` | `ok` |
| `PRAGMA user_version` / `schema_meta.schema_version` | `1` / `1` |
| DDL fingerprint | `55dd8184c6e1b16778ae60f713e40ee8f33c7876b33115f263df20a223897608` |
| `artifacts` | 1 |
| `dependencies` / `consumer_refs` / `legacy_sources` | 0 / 0 / 0 |
| `artifact_conflicts` | 0 |
| Artifact status / verification | `valid` / `verified` |

没有 dependency 和 consumer 是当前隔离边界的预期结果：本次没有接 runner，也没有创建 Prediction/Evaluation descendants。`artifact_conflicts=0` 只说明本次真实计算没有产生冲突，不能替代尚未实现的可审计 conflict resolution。

### 8.2 Legacy 与旧 checkout

canary 在 cold 和 warm 前后分别递归记录 active Legacy `cache`、`selection_cache`、`score_cache` 中每个文件的相对路径、size、mtime ns 和 SHA-256。四次聚合状态 hash 均为：

~~~text
b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa
~~~

快照覆盖物理文件数为 ResultCache 784、SelectionCache 111、ScoreCache 75；这些数字包含各目录的 `CLAUDE.md`，ScoreCache 的 JSON sidecar 与 NPZ 分开计数，因此不能与 Gate 1 的逻辑 source 数直接相加比较。旧 dirty checkout 的 `git status --short` 前后文件 SHA-256 也完全相同。

## 9. 测试与证据入口

### 9.1 测试

~~~powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_cache_v2_selection_canary.py `
  tests/test_cache_v2_store.py `
  tests/test_cache_v2.py `
  tests/test_score_cache.py `
  tests/test_attack_manager.py `
  tests/test_phase_b_invariants.py -q
# 147 passed in 2.35s
~~~

远端 fresh checkout：

~~~bash
/root/miniconda3/bin/python -m pytest \
  tests/test_cache_v2_selection_canary.py \
  tests/test_cache_v2_store.py \
  tests/test_cache_v2.py -q
# 70 passed in 2.33s
~~~

本地仅出现既有 `llvmlite/pkg_resources` deprecation warnings；没有测试失败。

### 9.2 Cold / warm 复现入口

~~~bash
PY=/root/miniconda3/bin/python
CODE=/tmp/opengu-citeseer-v2-canary-83842e6/GULib-master
RUN=/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2
LEGACY=/autodl-fs/data/OpenGU/GULib-master/results

cd "$CODE"
$PY scripts/cache_v2_selection_canary.py cold \
  --store-root "$RUN/store" \
  --dataset-root "$RUN/dataset" \
  --legacy-results-root "$LEGACY" \
  --allow-download \
  --selection-ratio 0.05 \
  --config-name A5_citeseer_r0.05 \
  --yaml-path experiments/configs/A5_citeseer_r0.05.yaml \
  --experiment-id cache-v2-citeseer-cold

$PY scripts/cache_v2_selection_canary.py warm \
  --store-root "$RUN/store" \
  --dataset-root "$RUN/dataset" \
  --legacy-results-root "$LEGACY" \
  --selection-ratio 0.05 \
  --config-name renamed-config \
  --yaml-path elsewhere/renamed.yaml \
  --experiment-id cache-v2-citeseer-warm-different-request
~~~

`cold` 要求 store 中不存在 index；`warm` 要求同一绝对 store 已存在且 schema 可核验。任一条件不满足都会 fail closed。

### 9.3 机器证据与校验和

机器汇总位于：

~~~text
/autodl-fs/data/cache-v2-canary/citeseer-83842e6-gate2/evidence/gate2_acceptance.json
~~~

该文件中的 16 个验收检查均为 `true`，整体 `accepted=true`；SHA-256 为 `a67f52c82854c22f085d84b8e47a6801c0ef25d6209a4f28922f431d9e67b113`。同目录 `evidence_sha256.txt` 覆盖 evidence、正式 store 与 tamper-store 的全部 28 个文件（manifest 自身除外），已经由 `sha256sum -c` 核验通过；manifest SHA-256 为 `d6a6d378dda6478a0c56404e44bf6fe9d3d43f545d0d3b7ad7ac9fd6e8bd19ce`。关键文件校验和：

| 文件 | SHA-256 |
|---|---|
| `cold.json` | `a0f967dca62a1fd477f13dc7c83ef8d734366f4b3587f6617f60457b4704f703` |
| `warm.json` | `ea816383a5c42ff99463062316a77a9cf0cd80d7b988bfbe9744b150bf2e4cd7` |
| `index.sqlite` | `ee9f2534c248e5f2c9f1215d24f5a5c3c21bbbe1c1bc66ea8d2f0900f1b25199` |
| `payload.json` | `c25a3ec2d9e44806fbe98444eadacb974b11bbceea78d595bfb0b42524ed0597` |
| `header.json` | `e98c0884ccadda2af7e4409c9990c12d61bd962c50da155ecca99a050c117081` |

## 10. 未完成边界与下一 Gate

本次没有运行正式 E1 GU/retrain 矩阵，也没有验证 Score、Prediction 或 Evaluation Artifact。TracIn、Hybrid 和 GraphRevoker 均是“未纳入”，不是失败。现有 A5 runner 仍走 Legacy Cache，因此不能用它的第一次计算/第二次跳过来声称 V2 命中。

下一步应先满足完整 Gate 2：

1. 把 versioned header/payload store 从隔离 canary 收敛为正式 Selection producer 契约；
2. 实现可审计的 conflict resolution，而不只有 conflict fail-closed；
3. 为 Prediction 与 Evaluation 补齐 V2-only 写入和一致性校验；
4. 让 runner canary 显式使用 V2，查询异常禁止静默回退 Legacy；
5. 通过后再派生 Citeseer clean E1：先 seed 42 小矩阵，再扩展 5 seeds；继续排除 TracIn/Hybrid，并在 GraphRevoker 先修问题关闭前不纳入其验收。

在以上门槛通过前，Legacy 继续只读，不能归档或删除。
