---
title: Cache V2 IM Selection Materializer 真机验收报告
date: 2026-07-14
status: partial-cache-contract-accepted-legacy-equivalence-rejected
---

# Cache V2 IM Selection Materializer 真机验收报告

> [!NOTE]
> **路径迁移说明（2026-07-24）**：本文显示的 SSH 文件系统路径已更新为当前 archive/canonical access 位置，不能据旧执行语境重建 `/autodl-fs/data` sibling。原始执行字符串可从 Git `41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` 与迁移报告复核；实验数值和验收结论未改。

## 1. 验收结论

本轮得到的是一个必须拆分表达的 **partial verdict**：

- **V2 exact Cache 契约通过。** 真实 `ogbn-arxiv` IM 首次 cold miss 只调用一次 producer，生成并登记一个 versioned SelectionArtifact；另一份 YAML 在独立进程中 exact hit 同一 Artifact，fail-if-called 哨兵证明没有重新计算。
- **同 seed Legacy 等价性不通过。** V2 与匹配到的 Legacy SelectionCache 都是 1354 个节点，但有序序列和集合均不同；Gate 3 不能通过，也不能把 Legacy 自动 promotion 成权威 V2 Artifact。
- **整体 Gate 2 仍未通过。** 当前只落地独立 Selection materializer；正式 ScoreArtifact、runner、Prediction/Evaluation、conflict resolution、random/degree/PageRank producer 都尚未完成。

| 验收面 | 结论 | 核心证据 |
|---|---|---|
| cold → warm exact hit | 通过 | cold `hit=false, producer_called=true`；warm `hit=true, producer_called=false` |
| producer 哨兵 | 通过 | warm 使用 `--fail-if-producer-called`，正常返回同一 Artifact |
| Artifact 稳定性 | 通过 | Artifact ID、Recipe/content/ordered hash、payload mtime 全部不变 |
| YAML / consumer 解耦 | 通过 | cold 9 个 consumer 请求去重为 1 个 Recipe；另一 YAML 仍命中同一 Recipe |
| direct lookup | 通过 | `resolve explain` 由 `(artifact_type, recipe_hash)` 返回唯一 exact candidate；不执行计算、不扫描 payload 目录 |
| TracIn / Hybrid 边界 | 通过 | 两者为 `producer_not_registered`，`future_registry_extension=true` |
| Legacy 只读 | 通过 | 970 个 Legacy 物理文件的 path/size/mtime/SHA-256 聚合快照前后完全相同 |
| Legacy ordered/set 对照 | **不通过** | 前 164 项相同；交集 1252/1354，Jaccard 0.859890，双方各 102 个独有节点 |
| SQLite / store | 通过 | integrity `ok`、schema v1、1 Artifact、0 formal V2 conflict |
| runner 切换 | 未实施 | `experiments/run.py`、现有 Cache 查询路径均未修改 |

## 2. 实现落点

被测代码 commit 为 `b10f672d3de2bd8c5c2714245c05dc7015dfffbb`，分支为 `codex/citeseer-e1-graphrevoker-20260714`。主要文件：

- `cache_v2/selection_materializer.py`：YAML request 投影、数据输入、IM producer registry、plan/materialize、Legacy 只读对照；
- `cache_v2/store.py`：versioned Selection payload/header、exact resolve、完整性校验、producer 哨兵；
- `scripts/cachectl.py`：`selection plan` 与显式 `selection materialize --apply`；
- `tests/test_cache_v2_materializer.py`：请求去重、结构化 skip、zero-write plan、cold/warm、Legacy 对照与只读 loader 测试。

当前 registry 只注册 IM。TracIn/Hybrid 被标记为未来 registry 扩展；random/degree/PageRank 也尚未注册，但不带 TracIn/Hybrid 的 future-provenance 标记。没有 compatible/prefix hit，只有 exact hit。

## 3. 请求、Recipe 与直接匹配

### 3.1 Cold 请求

| 字段 | 值 |
|---|---|
| YAML | `experiments/configs/phase_b_arxiv_im_only_r01.yaml` |
| dataset | `ogbn-arxiv`，169343 nodes |
| methods | GIF / GNNDelete / GraphEraser |
| experiment seeds | 42 / 212 / 722 |
| split / selector seed | 42 / 2024 |
| train candidates | 135474 |
| degree-pruned CELF pool | 13547（`candidate_fraction=0.1`） |
| k | 1354 |
| IM params | propagation 0.1；50 MC；batch-CELF size 1 |
| consumer requests | 9 |
| unique Artifact Recipes | 1 |
| deduplicated requests | 8 |

Recipe 只包含 graph/candidate identity、node ID space、selector/algorithm version、`k` 和 IM 参数。YAML path、`config_name`、GU method、base model request label 与 experiment seed 不进入 Artifact identity。

### 3.2 Warm 请求

warm 使用不同 YAML `experiments/configs/phase_b_arxiv_T1_seed42.yaml`。该文件声明 3 methods × 6 strategies × 1 seed，共 18 个 consumer 请求：

- IM 的 3 个请求去重为同一 Recipe；
- random / degree / PageRank / TracIn / Hybrid 共 15 个请求结构化跳过；
- TracIn / Hybrid 明确标记 `future_registry_extension=true`；
- IM Recipe hash 仍为 `5ef96a92830d4d032f7a4651997905fde41dd6929a43a930a2920db171c6d39e`。

这证明 materializer 先从请求构造最小 Recipe，再按 SQLite 唯一键直接匹配，不按 YAML 名、实验名或目录做全量搜索。

## 4. 真实 cold / warm 命中

| 字段 | cold | warm |
|---|---:|---:|
| `hit` | `false` | `true` |
| `producer_called` | `true` | `false` |
| miss reason | `no_exact_candidate` | none |
| resolve seconds | 13,583.907650 | 0.341279 |
| end-to-end seconds | 13,597.096808 | 5.501375 |
| fail-if-called | false | true |

cold resolve 用时约 **3 小时 46 分 24 秒**。warm resolve 加速约 **39,802.93×**，端到端加速约 **2,471.58×**；warm 端到端仍需约 5.5 秒加载并 fingerprint 真实大图，但没有执行 IM producer。

| 不变量 | cold / warm 共同值 |
|---|---|
| Artifact ID | `sel_5ef96a92_0d24a6da` |
| Recipe hash | `5ef96a92830d4d032f7a4651997905fde41dd6929a43a930a2920db171c6d39e` |
| content / payload SHA-256 | `0d24a6da899d8636ca3d01bf974bacc443688edf0ae55a40bab2520a57253299` |
| ordered nodes hash | `bd401f195da4e5779d7e5066554e5b3916a7384877e1c5cf1b47afb35adbebdd` |
| selected nodes | 1354 |
| payload size | 9085 bytes |
| payload mtime ns | `1784007450108570064` |

cold 命令还在第二个独立 store handle 上立即 verify：`hit=true`、`producer_called=false`、selected nodes 完全相同、payload mtime 不变。warm 再在独立 CLI 进程中用 producer trap 重复验证。

## 5. Legacy 对照为何不通过

### 5.1 匹配到的 Legacy source

只读对照候选为：

```text
/autodl-fs/data/OpenGU/GULib-master/results/selection_cache/ce8117dc5bf55cbad0eceba989b3e5e2.json
```

其 SelectionCache metadata 与当前请求一致的可见字段包括：dataset `ogbn-arxiv`、ratio 0.01、selector seed 2024、`k=1354`、graph fingerprint `05e152a...`、IM params fingerprint `5f41e319...`。Legacy ordered hash 为 `f592275caed46ee36554fe7ad6211debe2d71f96fc35da2bcc53aa2d3c4a075f`。

### 5.2 差异量化

| 对照 | 结果 |
|---|---:|
| V2 / Legacy 节点数 | 1354 / 1354 |
| 相同前缀 | 前 164 项完全相同；index 164 首次不同 |
| set intersection | 1252 |
| set union | 1456 |
| Jaccard | 0.859890110 |
| V2-only / Legacy-only | 102 / 102 |
| ordered match | false |
| set match | false |

当前代码重新计算出的剪枝后 candidate pool fingerprint 为 `7237f1cd80d5d4eadd5c6d33484b9e47`，与 Legacy `im_celf` sidecar 完全相同，故本次 mismatch 不能归因于候选池不同。

### 5.3 能确认什么，不能确认什么

能确认：

- Legacy source 生成于 2026-05-07 17:56，之后 IM producer 源码仍有提交变化；
- Legacy SelectionCache 和 `im_celf` sidecar 没有 producer source fingerprint；
- 当前 V2 Artifact 有 `opengu-im-selection-v1` 与 source fingerprint `ba5a8d48...`；
- Legacy 从未参与 V2 resolve，比较结果为 `content_mismatch`、`authoritative=false`、`used_for_resolution=false`。

不能确认：仅凭现存 Legacy metadata，无法区分 mismatch 来自历史 producer source 变化、Numba/执行环境差异，还是未记录的其他运行条件。它因此不能被宣称为“同一正式 Artifact Recipe 的权威重算”。

`artifact_conflicts=0` 只表示没有第二个 **正式 V2** Artifact 以同一 Recipe 注册不同 content。把 provenance 不足的 Legacy source 强行写成 V2 conflict，反而会伪造其 Recipe 等价性；本轮正确动作是保留 V2 Artifact、报告 Legacy mismatch，并让 Gate 3 失败。

## 6. SQLite、路径与 Legacy 不变性

| 检查 | 结果 |
|---|---|
| `PRAGMA integrity_check` | `ok` |
| schema version | `1` |
| formal artifacts | 1 |
| formal conflicts | 0 |
| status / verification | `valid / verified` |
| semantic path | `artifacts/selection/sel_5ef96a92_0d24a6da/payload.json` |
| store manifest hash | `74dd8d50f56280619ccaca7fdd0485a235cb4641af56b10b94afeeef27b2a711` |

Legacy 夹心快照覆盖 `results/cache`、`results/selection_cache`、`results/score_cache` 的 970 个物理文件。前后 manifest hash 均为：

```text
caaca31e5c6f791acd42bb868fe45e76d1401bf0d95c328d6722eef96e54ac26
```

快照还记录远端旧 checkout HEAD `3f631fb057a42e62db5f612e66e53edc2937459a`、原有四项 dirty status 和 arxiv processed marker；before/after JSON 逐字段相同。fresh checkout 在测试后 clean，无残留进程。

额外 Cora plan 因显式 dataset root 下缺少 `cora/processed/data.pt` 而 fail closed；没有创建 Cora V2 store，也没有下载或复制 dataset payload。这条失败没有被扩大成 loader/Legacy 迁移改动。

## 7. 测试

本地：

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_cache_v2.py tests/test_cache_v2_store.py `
  tests/test_cache_v2_selection_canary.py tests/test_cache_v2_materializer.py -q
# 75 passed

E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_score_cache.py tests/test_attack_manager.py `
  tests/test_phase_b_invariants.py -q
# 77 passed
```

远端 fresh checkout 对上述七个文件合并运行：

```text
152 passed, 1 warning in 39.69s
```

唯一 warning 是环境 TBB 版本导致 Numba TBB threading layer disabled；真实 IM 进程仍稳定使用约 16 个 CPU 核。没有测试失败。

## 8. CLI 复现入口

以下仅是非正式 replay。归档内 clone/store 均保持只读；如需重放，使用
active checkout 与新的 repo-local disposable store，生成新的执行身份。

```bash
PY=/root/miniconda3/bin/python
ACTIVE=/autodl-fs/data/OpenGU/GULib-master
CODE=$ACTIVE
STORE=$ACTIVE/results/cache_v2/__replay_im_materializer__

cd "$CODE"
$PY scripts/cachectl.py selection plan \
  --config experiments/configs/phase_b_arxiv_im_only_r01.yaml \
  --dataset-root "$ACTIVE/data/raw" \
  --store-root "$STORE" \
  --legacy-results-root "$ACTIVE/results"

$PY scripts/cachectl.py selection materialize \
  --config experiments/configs/phase_b_arxiv_im_only_r01.yaml \
  --dataset-root "$ACTIVE/data/raw" \
  --store-root "$STORE" \
  --legacy-results-root "$ACTIVE/results" \
  --apply --verify --compare-legacy

$PY scripts/cachectl.py selection materialize \
  --config experiments/configs/phase_b_arxiv_T1_seed42.yaml \
  --dataset-root "$ACTIVE/data/raw" \
  --store-root "$STORE" \
  --legacy-results-root "$ACTIVE/results" \
  --apply --fail-if-producer-called --compare-legacy

$PY scripts/cachectl.py resolve explain \
  --type selection --recipe /path/to/recipe.json \
  --db "$STORE/index.sqlite"
```

`resolve explain` 实测返回 `hit=true`、`valid/verified`、0 conflict、0 dependency issue、`execution_performed=false`。

## 9. 证据位置

远端机器证据：

```text
/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiment-evidence/cache-v2-im-b10f672-bundle/
```

关键文件包括 `plan.json`、`cold.json`、`warm.json`、`acceptance.json`、`legacy-before.json`、`legacy-after.json`、`resolve-explain.json` 和 `pytest.log`。V2 store 位于：

```text
/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/cache-v2-materializer/arxiv-b10f672-bundle/
```

它与旧 checkout 和 Legacy results 物理隔离。

## 10. 未完成边界与下一 V2.2 gate

本轮没有接 runner，没有运行 GU/GPU 实验，没有修改或删除 Legacy，没有执行 promotion、compatible hit、repair、retire、GC 或 conflict resolution。

下一 gate 必须按以下顺序收口：

1. 将 IM 初始 spread / CELF ranking 建成正式 ScoreArtifact，消除本次 3.8 小时 cold 中不可复用的 Step 1；
2. 对 post-prune candidate pool、producer semantic version 与 source fingerprint 建立可比较的正式 provenance；
3. 在同一 commit / 环境中做一次强制重算 determinism canary；不同 content 必须 quarantine 并登记 formal V2 conflict；
4. 定义 Legacy promotion policy，缺 source fingerprint 的历史 IM 只能 degraded/unknown，不能凭参数名自动等价；
5. 注册 random / degree / PageRank；TracIn 必须等 Score/model provenance 与 `proper-tracin-v1` 就绪后再扩 registry，Hybrid 随其后；
6. 完成可审计 conflict resolution 后，才允许 runner canary 使用 V2；查询异常禁止静默回退 Legacy。

Gate 3 当前已有一条明确反例，因此在解释并复现该 mismatch 前，不能推进 Legacy 冻结、归档或删除。
