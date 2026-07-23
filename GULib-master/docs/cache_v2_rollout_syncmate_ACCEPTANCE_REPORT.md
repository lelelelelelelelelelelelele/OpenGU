---
title: Cache V2 Gates 2–4、Dataset 解耦与 SyncMate Rollout 验收
date: 2026-07-17
status: accepted-legacy-physical-retirement-deferred
---

# Cache V2 Gates 2–4、Dataset 解耦与 SyncMate Rollout 验收

> [!NOTE]
> **路径迁移说明（2026-07-24）**：本文显示的 SSH 文件系统路径已更新为当前 archive/canonical access 位置，不能据旧执行语境重建 `/autodl-fs/data` sibling。原始执行字符串可从 Git `41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` 与迁移报告复核；实验数值和验收结论未改。

## 1. 验收结论

**ACCEPTED。Cache V2 当前范围已经整体完成，dataset 职责越界已关闭，Gates 2–4 均有真实证据。**

Cache exact HIT 不访问 dataset、不下载、不调用 producer、不重新决定 split/candidate；clean MISS 只由 experiment/GU 层通过规范化 `SelectionInputs` 调用 producer，再写入 V2。正式 Gate 4 单 cell GU/GPU canary、完整性 fail-closed、AutoReport provenance、分阶段 runner 与 SyncMate 收集/校验均通过。

本次没有全量重建 Cache。只在隔离 store 的 cold MISS 生成一个 Selection Artifact，随后 runner 与 warm lookup exact reuse。Active Cache、Legacy、journal、标准 runs、canonical Cora 和历史 archive 均未被清理、覆盖或迁移。

Legacy 的 **active authority/fallback 清理已完成**：显式 V2 路径零 Legacy fallback。Legacy 的 **物理退役未执行**：970 个冻结 payload 和 70 条兼容/旧工具/测试 consumer refs 仍原位保留；`physical_archive_authorized=false`。这是一条独立 retirement 边界，不影响 Cache V2 的 accepted 判定。

## 2. Gate 状态

| Gate | 结果 | 核心证据 |
|---|---|---|
| Dataset boundary | 通过 | `cache_v2` 静态扫描对 Planetoid、OGB、OpenGU dataset loader、`allow_download`、`dataset_root` 为 0 命中 |
| Gate 2：正式 Artifact | 通过 | Score、Selection、Prediction、Evaluation exact-only Recipe/payload、依赖 DAG、conflict/quarantine、递归 integrity |
| Gate 3：四 Artifact 对照 | 通过 | 真实 Cora/GIF/Degree 四件套；Selection ordered exact；Prediction/Evaluation 使用显式 float tolerance；warm producer 均为 0 |
| Gate 4：真实 runner canary | 通过 | Cora/GCN/GIF/Degree/seed42、5 epochs；cold producer 1、warm producer 0；四个 runner Artifact 通过 |
| AutoReport / phase | 通过 | 7 events；selection-only → attack-only → collateral → complete；authority/source/Recipe 正确 |
| Integrity / fallback | 通过 | tamper 返回非零并抛 integrity failure；`legacy_fallback=false` |
| SyncMate acceptance | 通过 | 4/4 SHA-256、0 missing、0 conflict、1 trusted row、strict gate failure_count=0 |

已知 ogbn-arxiv IM Legacy/V2 mismatch 继续保留为 provenance 不完整的非权威诊断，没有用 Jaccard 或 Legacy replay 强迫 V2 复制。TracIn/Hybrid 机制未修改。

## 3. Gate 4 真实 canary

| 字段 | 值 |
|---|---|
| 执行 commit | `e6091f9c4ac1998987a7645b111910d03ae570e2` |
| 最终 validated code pin | `f62a3e0ccea5aee1b9fb5423e29bfdc89a1736e3` |
| config SHA-256 | `45f587853aee6a91e85efd82ee40350435969a7b51b9539062762ae06b875980` |
| cell | Cora / GCN / GIF / Degree / seed42 |
| epochs | 5 |
| Selection Artifact | `sel_08afe166_4673b877` |
| Recipe hash | `08afe1660ffb0e64cb3961642f106820588cb7d828eaa4773412875521e44fe9` |
| Content hash | `4673b877e3327d870893e5691a692720105017cdf61b16608337c55ae5c24c28` |
| selected nodes | 108，ordered exact |
| logits | before / unlearned / retrained 均 `[2708, 7]` |
| cold / warm | producer `1 / 0`；warm exact HIT |
| download / full rebuild | `false / false` |
| protected roots | 前后 hash 全部一致 |

Runner 四件套：

| Artifact | SHA-256 |
|---|---|
| `_meta.json` | `136a4611a5d07d29fa93825ecee822453090993982bfd5d1e82dceca06f5bda3` |
| `attack.json` | `c9853a5190f2daf5d79873ecc612b1253d1c2f5f330ef5d7ac78cc6e2066c557` |
| `collateral.json` | `6ea733cd8289fc13533af84e33e454c9dd73cf0d4773626b5d6f36ebdce9b060` |
| `predictions.npz` | `b42ca924f1508cce39e86eee129a266c026a522ecc08de68bc9e0aa794f29dbe` |

远端 evidence root：

`/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/OpenGU-cache-v2-rollout/20260717/gate4`

正式 result leaf：

`/autodl-fs/data/OpenGU/GULib-master/results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42`

## 4. Dataset ownership 与 fail-closed

`experiments/processed_provider.py` 只接受现有 canonical processed pair：

- `cora0.8_0_0.2.pkl`
- `cora0.8_0_0.2dataset.pkl`

`experiments/run.py` 将 `processed_root` 与 `runtime_root` 明确传入 attack/collateral；`config.py` 区分代码根与可变 runtime 根。显式 processed pair 不完整时，实验层直接失败，不进入 Planetoid/OGB，不下载，不重建 split。

Cache V2 只接收 Recipe、identity/fingerprint 与上游 payload。旧 Recipe 不隐式升级；旧 Artifact 仍可按显式 Artifact ID 读取，版本边界 fail closed。

## 5. AutoReport 与 runner

AutoReport V3 记录：

- `authoritative=true`
- `hit_source=cache_v2:sel_08afe166_4673b877`
- `lookup_policy=cache_v2_exact_artifact_id`
- Recipe hash 与 Artifact identity
- selection-only、attack-only、collateral、complete 四阶段

Attack 与 collateral 使用同一 verified Selection Artifact。篡改隔离副本后，resolver 没有调用 producer，也没有回退 Legacy。

## 6. SyncMate 与 SSH

执行路径为：

```text
static recipe -> bounded runner (max jobs 1)
-> remote result leaf
-> manifest diff
-> incremental collect
-> SHA-256 verify
-> trusted Artifact index/results
-> strict acceptance gate
```

首次 collect：4 fetched / 4 verified / 0 conflicts。最终 `f62a3e0` 幂等 sync：0 fetched / 4 already-current / 4 verified；strict acceptance 与独立 gate 均通过，corrected trusted row 为 `cora_GCN_r0.05 / GIF / degree / seed42`，row hash `563b4b2ab8b0c7e8`。

本轮同时完成四个 bounded SyncMate TODO：

- clean verify 覆盖旧 planning diff 的 missing 提示；
- 双层 landing 使用远端正式 leaf 解析 result identity；
- inspect 区分 active running 与无锁 stale running；
- 新 dispatch 将 clean runner exact Git SHA 写入 job envelope，并在执行前再次核验。

历史 Attempt-04 receipt 仍诚实保留：它以 `dbe79ef` 为 recipe base，通过 17 个明确 allowlisted delta 接受实际 `e6091f9`。Artifact、Meta、collector 与 acceptance 均明确属于 `e6091f9`；没有重写历史 receipt。Exact job-envelope pin 是随后在 `f62a3e0` 完成的未来运行加固，因此无需重跑本次 Cache canary。

## 7. Legacy 状态

远端只读再盘点：

| Root | Files | Bytes |
|---|---:|---:|
| ResultCache | 784 | 6,242,823 |
| SelectionCache | 111 | 369,280 |
| ScoreCache | 75 | 2,659,617 |
| 合计 | 970 | 9,271,720 |

- Legacy aggregate SHA-256：`3fc323436bbc12b22e9f81c2d9c5c4613b169c5503f0cc71feae520542519d51`
- freeze marker SHA-256：`53a0988d5ad8a38ef5870e26b87af82426f769f2f7a7d7ca75702a2a34f9eef4`
- formal V2 conflicts：0
- unresolved formal conflicts：0
- source consumer refs：70
- rollback mode：`in_place_read_only`
- moved / deleted：`false / false`

因此本轮完成的是 V2 active authority/fallback 收口与 Legacy 状态复核，不是物理删除。70 条引用包含兼容实现、旧实验/工具和测试；清零它们会扩大到旧 runner、TracIn/Hybrid 或历史工具迁移，必须作为独立 retirement 项目处理。

## 8. 测试与对齐

| 验证 | 结果 |
|---|---|
| 最终本地 Cache/runner/AutoReport/SyncMate CPU 回归 | **450 passed in 15.95s** |
| 最终远端 SyncMate 回归 | **173 passed in 5.14s** |
| dataset forbidden static scan | 0 matches |
| 最终 collector sync | ready；0 fetched；4 already-current；4 verified |
| 最终 strict acceptance | ready；gate passed；failure_count 0；attention 0 |
| Git 对齐 | 可执行代码验证 pin 为 `f62a3e0`；报告发布 commit 只新增文档，handoff 前同样对齐 local/origin/collector/remote |

Gate 4 行为代码在 `e6091f9` 已通过远端相关组合回归 416 tests；`f62a3e0` 只修改 SyncMate 与其测试，没有重新运行 GPU。

## 9. 尝试记录与边界

- Attempt-01/02 在 canary 正文前暴露模块调用问题，没有触发 GPU 或 store。
- Attempt-03 cold Selection 成功，但 experiment dataset 路径回退 Planetoid 并发起下载请求后超时；没有下载完成、没有实际 GPU 计算。该失败证据已保留，没有从历史中抹除。
- Attempt-04 在修复 canonical processed provider 与 runtime isolation 后通过；本次 accepted 结论只引用 Attempt-04。

未下载数据；未全量重建 Cache；未删除或移动 `results/cache`、`results/cache_v2`、`results/runs`；未修改服务器历史 AutoReport archive；未修改 TracIn/Hybrid。

## 10. 完成清单

- [x] Dataset/experiment ownership 回归 OpenGU，Cache 无 dataset/download/split/selector 职责。
- [x] Gate 2 Score/Selection/Prediction/Evaluation 正式 Artifact。
- [x] Gate 3 真实四 Artifact 对照与显式 tolerance。
- [x] Gate 4 最小真实 GU/GPU canary。
- [x] Cache HIT 零 dataset access、零 producer、零下载。
- [x] Cache MISS 只通过上游 producer。
- [x] selection-only / attack-only / collateral / complete 与 fail-closed 回归。
- [x] AutoReport authority/source/Recipe。
- [x] SyncMate 增量收集、校验、trusted results 与 exact job pin 加固。
- [x] Legacy active authority/fallback 收口、freeze/rollback/consumer 再盘点。
- [x] 本地、origin、collector、远端 Git pin 对齐。
- [x] Markdown 设计说明与 Markdown/HTML 成对报告。
- [ ] 未物理移动或删除 Legacy payload；需单独授权并先清零 70 条 consumer refs。
- [ ] 当前分支尚未 merge；合并需按仓库 parent/merge-commit 流程单独接受。
