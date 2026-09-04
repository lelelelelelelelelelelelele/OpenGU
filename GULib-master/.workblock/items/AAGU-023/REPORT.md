# AAGU-023 · Legacy evidence inventory and archive

## Human Result

### 实际增量

本机和 SSH 已完成三轮零删除归档：失败的 full-v4 工程尝试、三个 Legacy Cache 根，以及追加授权的 16 个旧 V2 Artifact（含专属索引）。共 **1,115 个文件 / 26,040,188 bytes** 从旧活动位置移入可恢复归档。本候选将实际操作、原始账本、保留项和新复核纳入同一份正式验收报告。

### 核心观察

- **PASS · 保全与配对**：09-04 双端只读复核，1,115 个归档文件哈希全匹配，共享 manifest/ledger 一致。见[归档总览](evidence/ARCHIVE_REVIEW.md)与[双端复核](evidence/archive/observation-20260904-r2.json)。
- **PASS · 隔离**：双端三个 Legacy 原目录均不存在；旧 V2 的活动索引与 Artifact 路径已移出，SSH 冻结标记原样保留。没有改写 payload/header/SQL，也没有删除文件。
- **边界清楚**：归档不等于新实验已完成科学替代；未清空其他历史 results。正常缓存代码修复属于 AAGU-025。

### 当前决定

> 当前验收决定：`待决定`

Agent **建议接受**本次明确范围的归档与证据整理：原入口隔离、字节保全和双端账本均有实际观察支持。由用户决定接受或返工；当前停在 `awaiting_acceptance`，未合并、推送或部署。接受不授权永久删除、恢复旧缓存或重跑实验。

## Data · 从哪里移到哪里

本机项目根：`E:/project/OpenGU/GULib-master`；SSH 项目根：`/autodl-fs/data/OpenGU/GULib-master`。以下路径相对于各设备项目根。两边文件群体不同，账本一致不等于 payload 相同。

| 批次 | 旧活动位置 | 可恢复归档位置 | 本机文件 / bytes | SSH 文件 / bytes |
|---|---|---|---:|---:|
| full-v4 / Cora / seed42 失败尝试 | `results/runs/__syncmate_small_selection_gu_full_v4__` | `results/_archive_aagu023_20260903/gu-full-v4-cora-seed42` | 0 / 0 | 68 / 3,836,309 |
| ResultCache | `results/cache` | `results/_archive_aagu023_20260904/legacy_cache/cache` | 8 / 59,952 | 783 / 6,239,427 |
| SelectionCache | `results/selection_cache` | `results/_archive_aagu023_20260904/legacy_cache/selection_cache` | 9 / 19,696 | 110 / 366,313 |
| ScoreCache | `results/score_cache` | `results/_archive_aagu023_20260904/legacy_cache/score_cache` | 26 / 697,912 | 74 / 2,654,028 |
| 旧 V2 | `results/cache_v2` 下的精确旧存储单元 | `results/_archive_aagu023_20260904/v2_retired/cache_v2` | 32 / 983,515 | 5 / 11,183,036 |

新 V2 活动根仍是 `results/cache_v2`，没有换运行目录。改变的是旧存档被移出：本机 `c_target_v1`、`bc_target_v2` 整组归档；SSH 的旧 `index.sqlite`、`artifacts`、`producer_counter.json`、`trace.jsonl` 原样归档。`legacy_freeze.json` 留在 SSH 原处，992 bytes，哈希见双端复核。

“保留索引”指旧 SQLite 文件与其旧 Artifact 一起进归档，不是在活动入口保留可命中的数据库。6 个本机 C-target Score、9 个 BC-target Score、1 个 SSH degree Selection，共 16 个 Artifact；37 是含索引和旧运行记录的物理文件数。

## Lifecycle · 先登记，再移动，再核对

1. **09-03 SSH 恢复后**：核查 full-v4 身份、队列与引用，先登记 intent/ledger，再移动 68 文件。计算进程退出 0，但队列协议失败 `recipe stdout is not one JSON object`。保留 17 个 GNNDelete / Cora / GCN / seed42 / k7 单元及原 SHA，不伪造成功实验。
2. **09-04 Legacy 三根**：用户明确归档不必等 025 验收。双端登记共同 manifest/ledger 后，分别移动 43 与 967 文件。此阶段 V2 完全未动。
3. **09-04 旧 V2**：用户进一步明确“挪进一个文件夹，不永久删除”。对 16 个已审计 Artifact、三个无 consumer_refs 的专属索引及旧运行记录先登记，再整组移动；不执行 SQL，不改 ID、header 或 payload。
4. **本次候选返工**：恢复原分支和同一个 Claim，保存 27 份原始审计文件。09-04 18:23（北京时间）只读复核本机 75 个归档文件、SSH 1,040 个归档文件及 1 个保留冻结标记，均与原始哈希匹配。

完整审计链：[full-v4 账本](evidence/archive/ssh-rework-20260903/paired-ledger-final.json)、[Legacy 账本](evidence/archive/cache-archive-20260904/ledger-final.json)、[旧 V2 账本](evidence/archive/v2-archive-20260904/ledger-final.json)。复核器检查原收据字节、manifest/prepared-ledger 绑定、双端登记早于首次移动、最终发布哈希与实际文件。

旧报告的“SSH 不可达”“0 移动”“等 025 后归档”和 blanket `REPLACED` 限制已被后续观察或明确授权取代。原收据保留当时文本；`REPLACED` 仍指科学替代，不能把历史归档冒充新科学证据。

## Integration · 为什么旧缓存不会从原入口命中

在归档后查询原 Artifact，期待旧活动索引不可访问。实际 [15 个本机查询](evidence/archive/v2-archive-20260904/local-lookup-check.json)与 [1 个 SSH 查询](evidence/archive/v2-archive-20260904/ssh-lookup-check.json)均得到 `IndexNotFoundError`。本次再次观察到本机活动 V2 无文件、SSH 活动 V2 只有冻结标记；没有链接或 fallback 指回归档，所以这些旧对象不能从原入口命中。**PASS**。

不宣称旧缓存全部数值算错：部分旧 Score 含 AAGU-018 影响字段；旧 degree Selection 按协议退役，不判为数值错误。完整 ID、header、来源及消费者核查见[旧 V2 manifest](evidence/archive/v2-archive-20260904/manifest.json)。显式打开归档索引仍能读取历史；本次不授权恢复，也不声称能阻止未来人为重新接入。

代码修复与物理归档分别验收。V2 归档当时双端代码是 `b2c741a6e584c32e5f30bed8b64a08e08c33aa93`，本次 SSH 仍为该 SHA。023 原分支基线较早，**不包含后来接受的 025 修复**；不要在此分支运行正式实验或据此判断当前部署的缓存默认行为。接受后的 main 组合检查归 Closeout，本轮未合并或重写基线。

## 保留项与残余边界

- 既有本机 2026-05-06、05-07、07-21 archives、SSH peer-layout archive、tracked 报告和 provenance 保留。
- 混合旧 runs、ZIP、baseline 按 [09-03 locations 清单](evidence/archive/ssh-rework-20260903/paired-ledger-final.json)保留，不升级为当前正式证据；本次没有把整个 results/runs 搬空的授权。
- full-v5/gate 历史工程证据保留。09-03 配对为 616/616，零缺失或不匹配；这是已保存的历史保全观察，不是本轮新科学实验。
- 原 20 批次 inventory/ledger 是 09-02 快照，不是当前物理位置表；当前入口是[归档总览](evidence/ARCHIVE_REVIEW.md)。

接受后仍须使用已接受的代码、数据与 split 身份开展新实验；历史归档不进入当前 aggregate 或论文主张。恢复须另行授权、核对哈希及精确逆向路径，原位置必须为空，不得覆盖后来产生的新缓存。

## 候选验证与复核入口

- [权威 WorkItem](WORKITEM.md)：formal；data / lifecycle / integration；用户决定。
- source branch：`refs/heads/codex/aagu-023-legacy-evidence-archive`；原基线 `3ec3d56476f008f7bfc94b4e62a70efd239be6e2`；旧候选 `2f9dd79d19a81b91c1b3ec7aeaba0b03245f8996`。
- 内容检查点 `ba50b19f247a61cfcbff6c8f839f0a104fecba29` 提交后验证：5 项复核器测试、27 文件证据包/哈希链/计数检查、dashboard projection、clean status、diff check 均 PASS。双端观察绑定原始文件 SHA 与时间戳，不运行旧实验代码。
- 最终候选是本报告及状态投影提交后的同分支 clean HEAD，完整 OID 由交付回执提供。后续差异仅报告、渲染器、状态及验证说明，沿用上述数据验证，另查人类表面、链接、渲染一致性与 dashboard。
- 原 `67be158e77460a26ca3aaa201f0eeb3fc1815a05` 的 21 项 inventory/guard 检查只复用为未变代码的历史回归证据，不代替新归档核验。
- 新复核器首轮曾误读 protected 根和账本位置而报 FAIL；修正脚本后 r2 双端 PASS。失败观察和解释保留在[开发记录](evidence/ARCHIVE_REVIEW.md)，未为检查通过而改动实验数据。
- HTML 视觉检查：`NOT OBSERVED`。本轮内置浏览器安全策略拒绝本地 file URL；未绕过策略或换浏览器。MD/HTML 由同源渲染器生成，结构、一致性与链接另有静态检查，但不冒充视觉 PASS。本轮没有新正式实验、payload 移动或永久删除。

最终 ledger SHA-256：full-v4 `8039295f509cedbab7e13de7364250670b44f2fcac52eca877efdee2dbb1ecc9`；Legacy `cb8b23678d0f0e33feaa2ce64b27c944674dd484bc2de770a58eadf9be5418c2`；旧 V2 `c99fef13f5eccb0886aee69d147d11d12dd37f6076e5ba42e0a8ce589da4b103`。完整性清单：[archive/index.json](evidence/archive/index.json)。
