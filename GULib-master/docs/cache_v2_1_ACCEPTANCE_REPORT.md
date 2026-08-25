---
title: Cache V2.1 只读索引与机器契约验收报告
date: 2026-07-14
status: ssh-gate-1-accepted
---

# Cache V2.1 只读索引与机器契约验收报告

## 1. 验收结论

**SSH Gate 1 通过。** 在提交 `9b90ad462a618f822545fdfcd91f9c39c2d63521` 上，Cache V2.1 已在远端真实 Legacy 目录完成 dry-run、显式 apply、数据库核验和故障注入。证据表明：dry-run 零写入；apply 只新增 `results/cache_v2/index.sqlite`；扫描前后的 Legacy 文件状态与排除 `cache_v2` 后的完整 `results` 清单均保持不变；SQLite、路径和 schema 异常均 fail closed。

**该结论只验收 V2.1 的“只读索引 + 机器契约”。** 它不证明 V2 payload 的真实 cold/warm hit，不代表 runner 已切换，也不授权冻结、归档或删除任何 Legacy Cache。

| 验收面 | 结果 | 核心证据 |
|---|---|---|
| 被测版本 | 锁定 | branch HEAD `9b90ad462a618f822545fdfcd91f9c39c2d63521` |
| SSH dry-run | 通过 | 4113 个物理文件、4076 个逻辑 source，`writes=[]` |
| Legacy 完整性 | 通过 | dry-run 前后 `file_states` 逐项完全相同；完整 inventory（排除 `cache_v2`）前后亦完全相同 |
| 显式 apply 边界 | 通过 | 唯一持久化文件为 `results/cache_v2/index.sqlite` |
| SQLite 内容 | 通过 | 4076 个 Legacy source、5 个 conflict；正式 Artifact/依赖/consumer 均为 0 |
| fail-closed | 通过 | 远端 41 个 fixture 测试通过，6/6 个手工故障注入 case 通过 |
| 本地回归 | 通过 | 本地 V2.1 41 passed；既有相关测试 77 passed |
| 架构边界 | 通过 | runner、旧查询路径、Legacy payload 与现有 Cache 均未修改 |

## 2. 实施边界

本阶段只新增 metadata/index 基础设施：

- V2 一级 Artifact 仅有 Score、Selection、Prediction、Evaluation；
- Artifact identity 只取显式最小 Recipe，不接受完整实验 config；
- `config_name`、YAML path、experiment/batch/run identity 等控制字段递归拒绝；
- 正式 Artifact 对 `(artifact_type, recipe_hash)` 唯一；同 content 幂等，不同 content 进入 conflict；
- Legacy source 只做旁路索引，不自动 promotion；ResultCache 不升级成第五类 Artifact；
- V2.1 不写正式 payload，不实现 ResultCache、RunCache、checkpoint Cache、compatible/prefix 执行、GC、retire cascade 或 repair 写回；
- 未接入 `experiments/run.py`、`demo_attack.py`、`eval_collateral.py` 或现有 Cache 查询路径。

实现使用顶层 `cache_v2/`，没有放入建议的 `attack/cache_v2/`。原因是当前 `attack/__init__.py` 会连带导入实验配置并严格解析 CLI argv，独立 `cachectl legacy ...` 会在进入子命令前失败。顶层轻量包保留了 runner 与旧路径的零改动边界。

## 3. 实现清单

| 文件 | 职责 |
|---|---|
| `cache_v2/canonical.py` | 递归字段边界、稳定 canonical JSON、SHA-256 Recipe identity |
| `cache_v2/contracts.py` | Artifact/verification 枚举、Recipe、header、producer、dependency/consumer/Legacy/conflict 数据模型 |
| `cache_v2/paths.py` | Windows/Unix 路径规范化，relative/absolute source path 规则 |
| `cache_v2/schema.py` | schema version 1、DDL、完整 schema fingerprint |
| `cache_v2/index.py` | 初始化、只读查询、显式事务、幂等注册、冲突、DAG 与 consumer refs |
| `cache_v2/resolver.py` | exact-only explain；正式候选、Legacy 候选、状态、冲突与祖先健康检查 |
| `cache_v2/legacy.py` | 只读 Legacy 扫描、异常聚合、冲突/duplicate 摘要、显式 apply |
| `cache_v2/errors.py`、`cache_v2/__init__.py` | fail-closed 错误类型与公共 API |
| `scripts/cachectl.py` | 最小 CLI；真实子命令 argv 下不导入旧 runner/config |
| `tests/test_cache_v2.py` | 契约、SQLite、Legacy、路径、CLI 与零写回归测试 |

架构 source of truth 已同步更新至 OpenGU DocMap 实验部分的 Cache V2 架构说明。

## 4. 机器契约与 DDL

### 4.1 Recipe canonicalization

- dict key 顺序不影响 hash，list/tuple 顺序保留；
- float 使用有限值的稳定十六进制形式，`-0.0` 归一化；NaN/Infinity 拒绝；
- Path 带 path kind 且统一分隔符；Enum 使用 `module + qualname + value`；Unicode 使用 NFC；
- unordered set、非字符串 dict key、未知类型拒绝；
- ownership/control 字段按 snake_case、camelCase 与分隔符变体递归识别并拒绝；
- Recipe 版本进入 canonical form，完整 SHA-256 作为 `recipe_hash`。

### 4.2 Header、producer 与状态

- `ArtifactHeader` version 1 统一保存 type、Recipe、content hash、producer、status、verification、semantic path、compute time 与小型 metadata；不含 payload；
- `ProducerVersion` 同时支持 `semantic_version` 和 `source_fingerprint`；`valid` Artifact 至少具备一种 producer identity 且必须 `verified`；
- Artifact status：`valid / degraded / invalid / corrupt / missing / retired / unknown / conflict`；
- verification status：`verified / degraded / invalid / corrupt / missing / unknown`；
- `semantic_path` 可空；非空时只能是规范化相对路径。最终目录层级与 header carrier 留给后续 gate。

### 4.3 SQLite DDL

Schema version 为 `1`；DDL fingerprint 为：

~~~text
55dd8184c6e1b16778ae60f713e40ee8f33c7876b33115f263df20a223897608
~~~

| 表 | 核心内容与约束 |
|---|---|
| `schema_meta` | schema version、DDL fingerprint、创建时间；同时核对 `PRAGMA user_version` |
| `artifacts` | `UNIQUE(artifact_type, recipe_hash)`；Recipe/header 小型 JSON；不含 payload |
| `dependencies` | parent/child/relation 主键；双向索引；外键限制；DAG cycle 在访问层拒绝 |
| `consumer_refs` | consumer type/id 到 Artifact 的引用；Artifact 与 consumer 双索引 |
| `legacy_sources` | source path/root、raw/semantic hash、候选 type/Recipe、verification；`artifact_id` 可空 |
| `artifact_conflicts` | baseline 与 observed content hash、可选正式 Artifact/Legacy source/quarantine path |

数据库缺失、损坏、版本/DDL 不符、row/header 自洽性失败或事务异常时 fail closed。写事务使用回滚；SQLite 中不存大型 JSON/NPZ。append-only `index.jsonl` 明确不进入 V2.1。

## 5. SSH 真机 Gate 1

### 5.1 环境与证据口径

| 项目 | 值 |
|---|---|
| 被测提交 | `9b90ad462a618f822545fdfcd91f9c39c2d63521` |
| 真实 Legacy root | `/autodl-fs/data/OpenGU/GULib-master/results` |
| dry-run source state hash | `22c64adbd1969854ceaf2f80896008a9fcf7a3753720a735e9ad6638560642f1` |
| 完整 inventory 范围 | `results` 下除 `cache_v2` 外的全部文件 |
| 完整 inventory | 4233 files / 641,083,036 bytes |
| 完整 inventory aggregate | `a17bd3401683ddee4364f54ea08992a3a2edcfb7dea5d342ea74c4b9c1c0a7ef` |

验收先记录 active Legacy 的 `file_states`，执行 dry-run 后再逐项比较；随后执行显式 apply，并对排除 `results/cache_v2` 的整个 `results` 树重新盘点。两组前后比较均完全相等，因此 apply 的影响被隔离在唯一允许的新目录内。

### 5.2 dry-run：零写与扫描统计

~~~powershell
python scripts/cachectl.py legacy index --root results --dry-run
~~~

| 项目 | 数量 |
|---|---:|
| 物理文件 | 4113 |
| 逻辑 Legacy source | 4076 |
| ResultCache | 783 |
| SelectionCache | 110 |
| ScoreCache | 37 |
| run attack / collateral / meta / prediction | 812 / 778 / 778 / 778 |
| corrupt / degraded / invalid / unknown | 31 / 2479 / 6 / 1560 |
| conflict group / 同内容 duplicate group | 5 / 83 |

状态数量 `31 + 2479 + 6 + 1560 = 4076`，与逻辑 source 总数闭合。CLI 明确返回 `writes=[]`；dry-run 前后 `file_states` 完全相等，source state hash 均为 `22c64adbd1969854ceaf2f80896008a9fcf7a3753720a735e9ad6638560642f1`。

主要异常汇总：

| 异常 | 数量 | 处理 |
|---|---:|---|
| JSON decode | 1 | 标记异常并继续扫描 |
| JSON schema | 25 | 降级/无效记录，不伪造权威 Artifact |
| NPZ | 5 | 标记异常并继续扫描 |
| Prediction schema | 5 | 标记异常，不参与权威命中 |
| producer reported failure | 6 | 保留 provenance，状态不得提升为 valid |

### 5.3 apply：唯一允许的持久化结果

~~~powershell
python scripts/cachectl.py legacy index --root results --apply
~~~

apply 后唯一新增的持久化文件为：

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `results/cache_v2/index.sqlite` | 11,177,984 bytes | `1260d2f287fdcc73dffa6158b4f3240724783a2622061bc4ce90472e68f3c86e` |

排除 `cache_v2` 后，完整 `results` inventory 在 apply 前后均为 4233 个文件、641,083,036 bytes、aggregate `a17bd3401683ddee4364f54ea08992a3a2edcfb7dea5d342ea74c4b9c1c0a7ef`。这证明 Legacy 文件没有被编辑、移动、删除或改写。

数据库核验结果：

| 检查项 | 结果 |
|---|---|
| `PRAGMA integrity_check` | `ok` |
| schema version | `1` |
| DDL fingerprint | `55dd8184c6e1b16778ae60f713e40ee8f33c7876b33115f263df20a223897608` |
| `legacy_sources` | 4076 |
| `artifact_conflicts` | 5 |
| `artifacts` | 0 |
| `dependencies` | 0 |
| `consumer_refs` | 0 |

`artifacts=0` 是预期结果：本次只把真实 Legacy source 的 metadata 写入索引，没有 promotion、没有正式 V2 Artifact，也没有 payload 写入。

### 5.4 fail-closed 故障注入

远端 fixture 测试为 **41 passed**。此外，以下 6 个手工 case 全部按预期拒绝、回滚或保持零写：

| case | 预期且已观察到的结果 |
|---|---|
| `relative_db_path` | 拒绝依赖 cwd 的相对数据库路径 |
| `missing_db_read` | 只读查询失败，且不创建父目录或数据库 |
| `corrupt_sqlite` | 损坏的 SQLite 被拒绝，不降级为命中 |
| `schema_version_mismatch` | `PRAGMA user_version=999` 与 metadata version 1 不一致时拒绝 |
| `transaction_rollback` | 注入 writer failure 后事务回滚，`legacy_sources=0` |
| `apply_wrong_db_path` | 抛出 `ValueError`，数据库行数保持 0 |

这六个 case 覆盖路径、SQLite、schema 与事务失败面，未观察到静默 fallback 或部分成功写入。

## 6. 本地与远端统计解释

本地验收扫描仍保留为独立证据：

| 环境 | 物理文件 | 逻辑 source | conflict | duplicate | 写入 |
|---|---:|---:|---:|---:|---|
| 本地 | 2521 | 2508 | 1 | 1 | `writes=[]` |
| 远端 | 4113 | 4076 | 5 | 83 | `writes=[]` |

本地 active Legacy 的扫描前后快照均为 2521 个文件、12,644,658 bytes，aggregate `3e4fb7eb2129c69705cea626bf8ca70e2f3275fbf00ef478f6b883558e0e2b90`；Indexer source state hash 为 `e4ebda14085a0c251c5d25b9cf1ea87a4eba9fa37bfb29ab45174b80f07b42a7`。

两端计数不同来自数据内容不同，而非扫描逻辑不一致：远端比本地多 775 个 ResultCache、101 个 SelectionCache、24 个 ScoreCache，并包含本地扫描没有的 778 个 Prediction component。远端有 812 条 attack 记录，其中 778 个 leaf 同时具有 collateral、meta 与 Prediction；本地则有 826 条 attack/collateral/meta，但没有可登记的 Prediction。两端 run 组成差异会抵消部分 Cache 增量，也解释了远端更高的 source、异常、conflict 与 duplicate 数量。

## 7. CLI 与测试

~~~powershell
# 默认零写扫描
python scripts/cachectl.py legacy index --root results --dry-run

# 显式写入唯一允许的 metadata index
python scripts/cachectl.py legacy index --root results --apply

python scripts/cachectl.py artifact status <artifact_id>
python scripts/cachectl.py artifact parents <artifact_id>
python scripts/cachectl.py artifact children <artifact_id>
python scripts/cachectl.py artifact consumers <artifact_id>

python scripts/cachectl.py resolve explain --type selection --recipe <recipe.json>
~~~

`resolve explain` 只做 exact lookup。它会展示正式候选、同 Recipe Legacy source、status、verification、conflict、parent dependency 问题和 miss reasons；不执行计算、promotion 或 Artifact 写入。

| 验证 | 结果 |
|---|---|
| 本地 `pytest tests/test_cache_v2.py -q` | 41 passed |
| 远端 `pytest tests/test_cache_v2.py -q` | 41 passed |
| 本地 `pytest tests/test_score_cache.py tests/test_attack_manager.py tests/test_phase_b_invariants.py -q` | 77 passed |
| 远端手工 fail-closed cases | 6/6 passed |

既有测试仅出现 `llvmlite/pkg_resources` 弃用警告，不属于本次回归。

## 8. 后续阶段门

Gate 1 的通过只允许继续下一阶段，不允许跳级：

1. **新计算只写 V2**：先补齐 payload、header 和 conflict resolution；不得双写 Legacy；
2. **新旧结果对照**：抽样比较四类 Artifact；Selection 节点序列精确比较，Prediction 使用明确浮点容差；
3. **runner 切换 V2**：先小范围 canary，再考虑默认；查询失败不得静默回退 Legacy；
4. **Legacy 冻结**：保持完全只读，保留回滚窗口并列出未迁移 Artifact；
5. **归档或删除 Legacy**：只有迁移覆盖率、consumer refs、结果一致性和回滚备份全部通过后，才可另行授权执行。

在 runner 切换之前，**conflict 的可审计解除机制是硬门槛**。当前已具备冲突记录和 fail-closed 行为，但尚未实现人工裁决后的解除协议。

### 当前明确未完成

- V2.2 Selection canary 的真实 Cora cold miss → warm hit 尚未执行；
- 未用 producer 哨兵证明 warm hit 跳过真实计算；
- 正式 payload/header store 的完整契约尚未验收；
- conflict resolution/解除机制尚未实现；
- 未接入 runner、demo、collateral evaluator 或旧 Cache 查询；
- 未冻结、归档或删除任何 Legacy Cache。

因此，**SSH Gate 1 通过不等于“Cache 已被真实计算命中”，更不等于 Legacy 已可删除。**
