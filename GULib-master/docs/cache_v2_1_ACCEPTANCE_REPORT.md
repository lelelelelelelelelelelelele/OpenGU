---
title: Cache V2.1 只读索引与机器契约验收报告
date: 2026-07-13
status: accepted-with-v2.2-gates
---

# Cache V2.1 只读索引与机器契约验收报告

## 1. 验收结论

**通过。** Cache V2.1 已完成“只读索引 + 机器契约”基础设施；临时 fixture 可以建库和查询，真实 Legacy 目录的默认 dry-run 完成零写扫描，新增测试与指定既有测试均通过。

| 验收面 | 结果 | 证据 |
|---|---|---|
| 机器契约 | 通过 | 四类 Artifact、Recipe canonicalization、header、producer 与状态模型已落地 |
| SQLite CacheIndex | 通过 | schema v1，六张表，三重 schema 校验，事务 fail closed |
| LegacyIndexer | 通过 | 2521 个物理文件、2508 个逻辑 source；坏单文件不中断 |
| 零写保证 | 通过 | dry-run `writes=[]`；扫描前后 hash/mtime/size manifest 完全一致 |
| CLI | 通过 | status / parents / children / consumers / exact explain 可查询 |
| 回归 | 通过 | V2.1 41 passed；既有相关测试 77 passed |
| 架构边界 | 通过 | runner、旧查询路径、Legacy Cache 与 payload 均未修改 |

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

## 3. 新增实现

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

架构 source of truth 已同步更新：`文档规划/10_实验矩阵/19_Cache架构重设计与迁移方案.md` 与同名 HTML。

## 4. 机器契约

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
- `semantic_path` 可空；非空时只能是规范化相对路径。最终目录层级与 header carrier 留给 V2.2 gate。

## 5. SQLite DDL

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

## 6. Legacy dry-run

执行命令：

~~~powershell
python scripts/cachectl.py legacy index --root results --dry-run
~~~

### 6.1 盘点

| 项目 | 数量 |
|---|---:|
| 物理文件 | 2521 |
| 逻辑 Legacy source | 2508 |
| ResultCache / SelectionCache / ScoreCache | 8 / 9 / 13 |
| run attack / collateral / meta | 826 / 826 / 826 |
| 候选 Score / Selection / Evaluation / 未归类 | 13 / 835 / 826 / 834 |
| degraded / invalid / unknown | 1673 / 1 / 834 |
| conflict group / 同内容 duplicate group | 1 / 1 |
| 默认排除路径 | 2 |

主要异常：

| 异常 | 数量 | 解释 |
|---|---:|---|
| `dangling_selection_ref` | 706 | run 引用的 selection source 无法权威联接 |
| `graph_fingerprint_missing` | 826 | run provenance 不足，不能 promotion |
| `run_component_missing` | 826 | 当前 run leaf 缺 `predictions.npz` |
| `recipe_incomplete` | 1652 | 最小 Recipe identity 不完整 |
| `producer_version_missing` | 22 | producer identity 不足 |
| `producer_reported_failure` | 1 | producer 自报失败 |
| `recipe_content_conflict` | 1 | 同一可比较 Recipe 观察到不同 semantic content |
| `duplicate_same_content` | 1 | 同 Recipe 同 semantic content 的重复 source |

### 6.2 零写证明

独立夹心快照对 active Legacy 文件逐一记录相对路径、大小、mtime 与文件 SHA-256：

| 快照 | 文件数 | bytes | aggregate |
|---|---:|---:|---|
| 扫描前 | 2521 | 12,644,658 | `3e4fb7eb2129c69705cea626bf8ca70e2f3275fbf00ef478f6b883558e0e2b90` |
| 扫描后 | 2521 | 12,644,658 | `3e4fb7eb2129c69705cea626bf8ca70e2f3275fbf00ef478f6b883558e0e2b90` |

逐项 manifest 完全相等；CLI 报告 `writes=[]`。`results/cache_v2/index.sqlite` 与 `results/cache_v2/` 均未创建。Indexer 自身的 source state hash 为 `e4ebda14085a0c251c5d25b9cf1ea87a4eba9fa37bfb29ab45174b80f07b42a7`。

## 7. CLI

~~~powershell
# 默认零写扫描
python scripts/cachectl.py legacy index --root results --dry-run

# 显式把 metadata 写入唯一允许的目标；本次未对真实目录执行
python scripts/cachectl.py legacy index --root results --apply

python scripts/cachectl.py artifact status <artifact_id>
python scripts/cachectl.py artifact parents <artifact_id>
python scripts/cachectl.py artifact children <artifact_id>
python scripts/cachectl.py artifact consumers <artifact_id>

python scripts/cachectl.py resolve explain --type selection --recipe <recipe.json>
~~~

`resolve explain` 只做 exact lookup。它会展示正式候选、同 Recipe Legacy source、status、verification、conflict、parent dependency 问题和 miss reasons；不执行计算、promotion 或 Artifact 写入。

## 8. 验证结果

~~~powershell
E:/conda_package/envs/gnn/python.exe -m pytest tests/test_cache_v2.py -q
# 41 passed

E:/conda_package/envs/gnn/python.exe -m pytest tests/test_score_cache.py tests/test_attack_manager.py tests/test_phase_b_invariants.py -q
# 77 passed
~~~

临时 fixture 额外验证了：显式初始化、schema version/fingerprint、正式 Artifact 创建、同 content 幂等、不同 content conflict、正式行不被覆盖、parents/children、consumer refs、Legacy-only source、exact explain 与事务回滚。

测试只有 `llvmlite/pkg_resources` 弃用警告，不是本次回归。

## 9. 未完成边界与 V2.2 gate

本次明确未做：

- 未对真实 Legacy 树执行 `--apply`，也未创建正式 V2 Artifact/payload；
- 未选定 header 嵌入方式或最终 semantic directory；
- 未建立 Legacy promotion policy；
- 未接入 runner、demo、collateral evaluator 或旧 Cache 查询；
- 未实现 compatible/prefix hit、repair、retire cascade、GC 或 payload store；
- 未迁移 ResultCache、Prediction、checkpoint 或任何大型 payload。

进入 V2.2 前必须同时满足：

1. 评审并冻结 Score/Selection 最小 Recipe 与 Legacy promotion policy；
2. 决定 header carrier 与 semantic directory，验证 payload/header 可重建 index；
3. 对唯一 conflict 给出人工裁决，不允许 Resolver 猜测；
4. provenance 不完整的 `unknown/degraded` source 不得直接 promotion；
5. 先在临时/隔离 index 上完成 Score/Selection canary，再讨论主查询路径接入；
6. runner 接入必须另立变更，继续保持 Legacy 路径只读并有旧路径回归证据。
