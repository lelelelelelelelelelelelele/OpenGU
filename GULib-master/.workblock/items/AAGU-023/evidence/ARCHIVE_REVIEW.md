# AAGU-023 · 归档证据索引

这是 2026-09-04 返工的当前证据入口，范围与决定者由上级 WORKITEM.md 定义。

## 已完成范围

| 操作 | 本机文件 / bytes | SSH 文件 / bytes | 当前目录（相对各设备项目根） |
|---|---:|---:|---|
| full-v4 / Cora / seed42 失败工程尝试 | 0 / 0 | 68 / 3,836,309 | `results/_archive_aagu023_20260903/gu-full-v4-cora-seed42` |
| 三个 Legacy 根 | 43 / 777,560 | 967 / 9,259,768 | `results/_archive_aagu023_20260904/legacy_cache/{cache,selection_cache,score_cache}` |
| 旧 V2 及专属索引、旧运行记录 | 32 / 983,515 | 5 / 11,183,036 | `results/_archive_aagu023_20260904/v2_retired/cache_v2/` |

合计 1,115 个文件 / 26,040,188 bytes。15 个本机 Score 与 1 个 SSH Selection 共 16 个旧 V2 Artifact；37 个物理文件还包含 SQLite 索引和旧 telemetry，不是 37 个 Artifact。

## 原始审计包

- [完整性清单](archive/index.json)：`archive_review.py package` 从原 runtime 收据逐字节归档；清单可重建，原收据不可改写。
- [full-v4 intent 与身份映射](archive/ssh-rework-20260903/archive-intent.json)、[最终账本](archive/ssh-rework-20260903/paired-ledger-final.json)、[当时全域保全验证](archive/ssh-rework-20260903/verification.json)。计算进程退出 0，但队列协议失败 `recipe stdout is not one JSON object`；这是失败工程尝试，不是 formal REPLACED。
- [Legacy manifest](archive/cache-archive-20260904/manifest.json)、[最终账本](archive/cache-archive-20260904/ledger-final.json)：逐设备、逐根保留文件哈希及原身份字段；不同设备群体不宣称互为副本。
- [旧 V2 manifest](archive/v2-archive-20260904/manifest.json)、[最终账本](archive/v2-archive-20260904/ledger-final.json)：列出全部 16 个 Artifact ID、原 header、专属索引观察、引用核查和移动路径。
- [本机旧索引 lookup](archive/v2-archive-20260904/local-lookup-check.json)、[SSH 旧索引 lookup](archive/v2-archive-20260904/ssh-lookup-check.json)：旧活动入口查询均为 IndexNotFoundError；这不代表显式打开归档索引不能读历史。
- [本轮双端只读复核](archive/observation-20260904-r2.json)：1,115 个已移动文件和 SSH 保留冻结标记的原始字节匹配；旧活动路径不存在；远端及双端共享账本哈希匹配。

## 当前授权与历史收据的区别

原始 2026-09-02 batch-plan / inventory / retirement-ledger 以及 09-03 的 remaining / WAIT_AAGU025 字段保存当时观察，不是当前操作指令。用户随后明确：归档不等于科学替代，不必等待 025 验收；新协议不再需要的旧 V2 可以连同专属索引原样移入历史文件夹，但不永久删除。原收据中的这些旧限制已经由本次 WORKITEM 与报告明确取代，未在原账本上篡改。

三轮操作均先登记 manifest/ledger 后移动。SQLite 索引以整个原文件保留，没有删除数据库行、重建索引、修改 header/ID 或覆盖 payload。SSH `results/cache_v2/legacy_freeze.json` 保持原址、原字节；不删除空的 V2 根与锁目录。AAGU-025 拥有正常缓存能力的代码修复，023 不新增缓存选项、fallback 或迁移代码。

## 保留项不是清理遗漏的暗示

09-03 共同账本的 `locations` 列出本机 25、SSH 28 个位置（位置不自动等于科学批次）。除了本次明确的移动映射，既有 archive、tracked 报告、混合旧 runs 与 ZIP、full-v5/gate 工程证据保留。它们不升级为当前正式实验结果；不对整个 results/runs 做一刀切搬移。09-03 的 v5 配对为 616/616 哈希一致，零缺失/不匹配；本轮复用这一历史保全证据，不宣称它是 09-04 的新科学验收。

## 复核器开发记录

首轮 `observation-20260904.json` 的 FAIL 来自新复核器错误地将 manifest 中的受保护 cache_v2 也当成 Legacy 根，以及把 Legacy 账本位置误写为 payload 子目录。原始收据证明正确位置在归档父目录。复核器已改为三个显式 Legacy 根和准确的父目录路径；独立测试覆盖了这两个错误。本轮没有为让检查通过而移动、改写或删除任何实验文件。修正后的 r2 复核双端 PASS；SSH 首次代码传输还曾发生本地构造的 Python 语法错误，未执行文件操作。

## 可重复检查

使用 Python 3.9+，从项目根运行 `python -B -X utf8 .workblock/items/AAGU-023/evidence/test_archive_review.py` 和 `python -B -X utf8 .workblock/items/AAGU-023/evidence/archive_review.py check`。`observe` 是明确的只读 SSH 复核，必须指定新的 `--output` 路径，不能覆盖已有观察。

恢复须重新明确授权，确认原路径不存在且哈希吻合，按各 ledger 的精确 source/destination 逆向操作；不得覆盖后续产生的新缓存。此文不授权恢复、删除、正式实验或 Closeout。
