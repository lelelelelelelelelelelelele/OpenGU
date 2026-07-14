---
title: Cache V2 Selection Cutover 与 Legacy 归档准备验收
date: 2026-07-14
status: accepted-with-delete-blocked
---

# Cache V2 Selection Cutover 与 Legacy 归档准备验收

## 结论

**Gate 3 的修订标准、Gate 4 的显式 Selection runner 路径、Gate 5 的 active Legacy freeze，以及 Gate 6 的归档准备均已完成。** 本轮到此结束。

这里的“完成”有严格边界：V2 支持 random、degree、PageRank、IM；runner 查询失败不会回退 Legacy；active 4090 上的三棵 Legacy cache 已冻结为原位只读回滚源；逐文件 hash/consumer/V2/conflict/rollback manifest 已生成。**Legacy 尚未移动或删除，当前也不允许删除**，因为代码与配置扫描仍有 70 条 Legacy consumer 引用。

旧 AutoReport 的固定“下一步建议”没有迁入新进度视图。服务器历史 journal 继续保存在 archive，SHA-256 仍为 `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b`；新 AutoReport 仍是 append-only event stream 加有界 Markdown/HTML 视图。

## Gate 状态

| Gate | 结果 | 验收证据 |
|---|---|---|
| 3. V2/Legacy 对照 | 通过修订标准 | Legacy 节点逐项相同降为迁移诊断；四类 versioned Selection exact canary 已通过；单 cell 9 项 Prediction→Evaluation smoke 最大误差 `1.1920928955078125e-7 < 1e-6` |
| 4. runner 切换 V2 | 通过当前无 GPU 范围 | exact Artifact-ID loader、同一 Artifact 传给 attack/collateral、Legacy cache 全禁用；4090 runner dry-run `writes=0`、`would_run=1` |
| 5. Legacy 冻结 | 通过 | write-once marker；970 files / 9,271,720 bytes 原位只读；受控 ResultCache 写探针抛出 `LegacyCacheFrozenError`，文件数 784→784 |
| 6. 归档准备 | 完成 | 167 KB canonical manifest；逐文件 hash、70 条 consumer refs、V2 状态与 rollback integrity anchor 齐全 |
| 物理归档/删除 | 未执行 | `physical_archive_authorized=false`；`legacy_delete_ready=false` |

## 实现合同

### Conflict resolution

- 默认 unresolved，Resolver 和 durable marker 均 fail-closed。
- 第一版只允许 `keep_existing`，且只能授权仍为 `valid/verified` 的正式 Artifact。
- resolution sidecar 绑定 conflict fingerprint、Artifact/content、actor、reason、UTC 时间，并且 write-once。
- SQLite conflict row、marker 和 quarantine observation 永久保留；后续不同 content 会重新阻塞。
- active index 的 5 条 conflict 都是 Legacy-only diagnostic，没有正式 Artifact，因此不可伪装成已解除的 V2 conflict。

### Runner / Cache hit 语义

- `cache_v2.mode=selection` 才启用新路径；支持 random、degree、PageRank、IM。
- preflight 从 materializer 的 `experiment_seeds` 建立 `(strategy, seed) → artifact_id` 映射。
- runtime 按 Artifact ID 双重 exact resolve，并校验 Recipe、producer、header、payload、candidate set、strategy 和 k；读取过程零写入。
- V2 mode 设置 `enable_score_cache=false`，AttackManager 不创建 ResultCache/SelectionCache，attack 与 collateral 使用同一 Selection Artifact。
- AutoReport 将其表达为 authoritative Selection hit，记录 Artifact/Recipe/content hash 和 `hit_source=cache_v2:<artifact_id>`，不再混写成 Legacy HIT。
- TracIn/Hybrid 或任何 index/path/schema/content 错误均直接失败，不静默回退。

### Legacy freeze / archive preparation

- freeze marker 只新增在 `results/cache_v2/legacy_freeze.json`；读取旧 Cache 仍允许。
- ResultCache save/invalidate/clear、SelectionCache save、ScoreCache save/新 namespace 全部受写保护。
- archive manifest 是只读盘点后显式发布的 write-once JSON；不会移动、截断或删除任何 Legacy 文件。

## 4090 真机证据

| 项目 | 值 |
|---|---|
| 部署 commit | `a1eae3d` |
| Evidence root | `/autodl-fs/data/opengu-experiment-evidence/cache-v2-cutover-431d5df-20260714` |
| V2 Selection Artifact | `sel_5bc434cd_7e66e515` |
| Recipe hash | `5bc434cdb68a652e5f4e4ae5974eafc56decfbdbad79ce27787baf47d28136de` |
| Content hash | `7e66e5153fdd003d633d7e2fe9459f524b5aa738bfb649f9a6dd398d990c232a` |
| Selected nodes | 108 |
| Cold / verify | cold producer called；verify exact hit、producer not called、payload mtime unchanged |
| Independent warm | exact hit、producer not called；freeze 后再次 warm 仍通过 |
| Legacy materializer invariant | 784 Result + 111 Selection + 75 Score files；before/after hash 均为 `b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa` |
| Freeze marker SHA-256 | `53a0988d5ad8a38ef5870e26b87af82426f769f2f7a7d7ca75702a2a34f9eef4` |
| Archive inventory | 970 files；9,271,720 bytes；integrity anchor `3fc323436bbc12b22e9f81c2d9c5c4613b169c5503f0cc71feae520542519d51` |

active `index.sqlite` 在 manifest 时的状态：

| 表/分类 | 数量 |
|---|---:|
| `legacy_sources` | 4,076 |
| 正式 `artifacts` | 1（Selection） |
| `artifact_conflicts` | 5 |
| Legacy diagnostic conflicts | 5 |
| formal / unresolved formal conflicts | 0 / 0 |
| dependencies / consumer refs | 0 / 0 |

manifest 的 source scan 另发现 70 条 Legacy API/path 引用，涵盖兼容实现、旧脚本、配置和 tests。它们是删除阻塞证据，不是要求本轮扩大到 TracIn 或清理所有旧工具。

## 测试

| 范围 | 结果 |
|---|---|
| 本地 Cache/runner/report/attack/collateral 相关回归 | 195 passed |
| 已知未改基线 collateral stub | 3 failed：stub 缺少 `AttackPipeline.args`，不在本改动文件 |
| 远端 conflict/runtime/freeze/archive/AutoReport focused | 30 passed |
| 远端 runner/report suite（dataset-root override 后） | 20 passed |
| changed Python compile / HTML parse | 通过 |

## 完成与保留项

- [x] Legacy exact replay 降为迁移诊断，并写入 source-of-truth 设计文档。
- [x] write-once conflict resolution 与 CLI。
- [x] explicit V2 runner preflight、Artifact-ID runtime 和 AutoReport provenance。
- [x] active 4090 Legacy freeze 与失败写探针。
- [x] 逐文件 archive-readiness manifest、consumer refs、hash 和 rollback anchor。
- [x] 历史 AutoReport archive hash 保持不变，旧固定建议不进入新视图。
- [ ] 未运行 GU/GPU canary；这是本轮明确边界，不伪装成已完成。
- [ ] 未接 TracIn/Hybrid。
- [ ] 未迁移全部 70 条 Legacy consumer 引用。
- [ ] 未移动或删除 Legacy；需要独立授权。

## 证据文件

远端 evidence root 内包含：

- `selection-materialize.json`
- `selection-warm.json`
- `selection-warm-after-freeze.json`
- `runner-dry-run.log` / `.rc`
- `legacy-freeze-dry-run.json`
- `legacy-freeze-apply.json`
- `legacy-freeze-status.json`
- `freeze-write-probe.stderr.log` / `.rc` / counts
- `archive-readiness-manifest.json`

本报告不复制 167 KB 的逐文件 manifest；manifest 是机器证据，本 Markdown 是可编辑结论源，HTML 是同结论的浏览版。
