# OpenGU 实验证据换代树设计

**日期：** 2026-08-01

**状态：** 待人工审核的设计稿；不是运行、扩矩阵或删除授权

**可读版：** [HTML 报告](../../../reports/experiment_evidence_replacement_tree_DESIGN.html)

## 1. 结论

以 **2026-05-31 23:59:59** 为旧证据截止线，分批重跑当前实验计划仍需要的实验，并在每批新结果通过 gate、由 SyncMate 收集校验、进入 trusted index、重建下游投影之后，再退役该批对应的本机与 SSH 旧 payload。

计划采用一棵按科学依赖排列的实验树，而不是按文件夹或旧结果目录排列。批次之间即使有少量重叠，也完整执行各自注册矩阵，不做跨批次人工去重；只有身份完全相同、不可变且校验通过的 Cache V2 Score/Selection Artifact 可以精确命中复用。Legacy cache 和仅仅同名、同路径或参数看起来相似的产物不得复用。

执行在会改变研究目标或决定是否扩展矩阵的节点暂停。人先审核新证据和下一阶段目标，再继续下一个分支。

## 2. 当前事实快照

本节只记录 2026-08-01 本次只读检查可证明的状态。历史验收报告只用于设计批次、估计规模和了解既有问题，不替代新的统一证据基线。

| 项目 | 当前状态 | 对计划的影响 |
|---|---|---|
| 本机工作分支 | `codex/docs-context-architecture-20260726`，HEAD `f2b9876386ddcb8a5cce958f43e6c4c33f8043bb`，工作区干净 | 尚未进入正式运行线 |
| 本机 `main` / `origin/main` | 均为 `44b587df59763a162057f1f60ecd9446147ec5b9` | 当前分支与正式线不一致 |
| 本机 SyncMate | device role 为 `unknown`，无 peer | 需要先配置 collector 与远端 peer |
| SSH | 用户报告实例已开启但无 GPU；当前配置的 SSH alias 均不可达 | 远端 Git、Python、数据和结果库存仍是未知状态 |
| 本机旧结果 | `runs` 3,990 文件；三类 Legacy cache 共 43 文件；`cache_v2` 32 文件；另有 baseline、evaluation 和历史 archive | 只能先做身份清单，不按目录或 mtime 直接删除 |
| 历史 E1 | 50/50 曾验收，但依赖 Legacy-format scratch cache | 作为已知可行性，仍纳入统一身份下整批重跑 |
| 历史 E4 | 40/40 远端曾通过，本机同名旧目录无效，归档未闭环 | 作为已知可行性，仍纳入整批重跑与新归档 |
| E8 正式候选 | G2 为 34 个 Selection Artifacts；G3 为 2 个 GU cells；G4 为 34 cells；G5 为 306 cells / 1,224 artifacts | 只授权到逐级 gate；G4、G5 都需暂停审核 |

因此，当前不能开始正式实验。第一个暂停点是：更新 SSH endpoint、配置 SyncMate、完成远端只读快照，并让正式 Git SHA 与运行环境通过 preflight。

## 3. 单一事实归属

本设计只组织顺序、分支条件、暂停点和换代原则，不复制操作细节。

| 事实或指令 | 唯一维护源 |
|---|---|
| 当前任务、优先级和依赖 | [`self/dashboard/WORKPLAN.md`](../../../self/dashboard/WORKPLAN.md) |
| 正式入口、解释器、GPU、数据根、SHA 和 gate 规则 | [`experiments/AGENTS.md`](../../../experiments/AGENTS.md) |
| Selection 修改与 GU 修改的修复链、失效范围和人类决策 | [13 重跑与缓存修复 Runbook](../../../%E6%96%87%E6%A1%A3%E8%A7%84%E5%88%92/10_%E5%AE%9E%E9%AA%8C%E7%9F%A9%E9%98%B5/13_%E9%87%8D%E8%B7%91%E4%B8%8E%E7%BC%93%E5%AD%98%E4%BF%AE%E5%A4%8DRunbook.md) |
| 已确认修复链之后的机器端命令 | [`scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`](../../../scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md) |
| SyncMate 收集、校验和 trusted-index 协议 | [`scripts/syncmate/AGENTS.md`](../../../scripts/syncmate/AGENTS.md) |
| 当前设计的批次顺序和暂停条件 | 本文 |

本文不再维护解释器路径、SSH 命令、cache key 公式或运行命令。执行时只链接并遵循对应所有者。

## 4. 批次状态机

每个批次都独立经过同一状态机：

```text
INVALIDATED
  -> REGISTERED
  -> GATED
  -> RUNNING
  -> COLLECTED
  -> ACCEPTED
  -> PROJECTED
  -> REPLACED
  -> RETIRED
```

- **INVALIDATED**：旧结果落在截止线内，或身份/来源无法证明。它可以保留作审计，但不能支持新结论。
- **REGISTERED**：矩阵由当前正式 YAML/launcher 注册，dry-run 固化 cell 列表和完整身份。
- **GATED**：最小 GPU、数据、Selection 与 GU gate 全部通过。
- **RUNNING**：只运行该注册批次，禁止把修复前后的 cells 拼入同一批。
- **COLLECTED**：SyncMate 完成 manifest diff、缺失产物收集和 SHA-256 校验。
- **ACCEPTED**：trusted index 与接受报告确认完整性、身份和验收结论。
- **PROJECTED**：aggregate、表格、图和报告由新接受证据重建。
- **REPLACED**：旧批次到新批次存在一一可审计的替代映射，旧引用计数为 0。
- **RETIRED**：才允许清理本机和 SSH 的旧 payload；保留轻量 manifest、hash、失效原因和 replacement identity。

任何一步失败都停留在当前状态。失败不是继续跑剩余 cells 或手工补结果的理由。

## 5. 完整实验树

```text
R0 证据换代政策
├─ 固化 2026-05-31 23:59:59 截止线
├─ 建立本机 + SSH 旧批次身份清单（先不删除）
└─ 将仍在新计划中的实验登记为完整重跑批次
   │
R1 正式源代码身份
├─ 收口当前 work blocks
├─ 接受进 main
└─ local main = origin/main = SSH active checkout full SHA
   └─ [PAUSE] 任一 SHA 不一致即停止
      │
R2 SyncMate 与 SSH 只读摸牌
├─ 更新可达 endpoint
├─ 配置本机 collector 和 SSH peer
├─ 读取远端 Git / Python / GPU / data / result inventory
└─ [PAUSE] endpoint 不可达、设备身份不明或远端状态异常
      │
R3 正式运行前置
├─ GPU 可枚举，禁止 CPU fallback
├─ gnn_20 环境和正式解释器通过
├─ canonical data/processed profiles 通过
└─ 注册 dry-run 固化 batch / cells / identities
   └─ [PAUSE] 数据需 materialize 或注册矩阵与计划不一致
      │
R4 E8 target-direct 最小门禁（树干）
├─ G1：canonical processed profile preflight
├─ G2：Cora / seed 42，34/34 ratio-conditioned Selection Artifacts
└─ G3：degree 1% + 5%，2 个 GU cells / 8 个文件
   ├─ Selection / identity 缺陷 -> 13 判定 -> machine repair -> 新 SHA/identity -> 重启 G1
   ├─ GU / code 缺陷 -> 修复分支 -> 接受进 main -> 新 SHA/identity -> 重启 G1
   └─ [PAUSE] 审核 gate 结果，决定是否进入正式矩阵
      │
      ├─ R5A 核心与 target-direct
      │  ├─ 当前注册的 Cora GCN/GAT 核心矩阵（以 dry-run cell 数为准）
      │  ├─ E8 G4：Cora / seed 42，17 selectors × 2 ratios = 34 cells / 136 artifacts
      │  ├─ [PAUSE] 审核 selector 排序、预算效应和异常 cells
      │  └─ E8 G5：3 datasets × 3 seeds × 17 selectors × 2 ratios
      │             = 306 cells / 1,224 artifacts（需另行授权）
      │
      ├─ R5B 方法专项换代
      │  ├─ E4 GraphRevoker：完整 40-cell batch
      │  ├─ proper-TracIn / Hybrid：独立 Selection gate 后再运行
      │  ├─ E2 GIF/IDEA collateral：完整 120-cell batch
      │  └─ E3 K5：先 1-cell gate，再运行余下 59 cells
      │     └─ [PAUSE] 每个方法 gate 或完整性检查失败即停该分支
      │
      ├─ R5C 数据集与预算换代
      │  ├─ E1 CiteSeer stable：完整 50-cell batch
      │  ├─ A5 Cora/CiteSeer ratio sweep：完整 190-cell batch
      │  ├─ PubMed：按通过审核后的 E8 / 当前注册范围运行
      │  └─ E5 arxiv：T1 feasibility -> [PAUSE] -> T2/T3 首 seed
      │                -> [PAUSE] -> 18 cells/seed 扩展
      │
      └─ R5D 条件机制实验
         ├─ A3 alpha sweep：只有核心结果显示非平凡 hybrid synergy 才运行
         ├─ E7 C.6a：proper-TracIn 通过后先运行 5 cells
         ├─ [PAUSE] transfer ratio >= 60% 才进入 C.6b
         ├─ E7 C.6b：10 cells
         └─ 其余 ablation：只运行届时 WORKPLAN 仍登记的问题
            │
R6 下游重建
├─ E6 aggregate / hop 指标（依赖 E2）
├─ 重建 config inventory、接受报告、表格与图
├─ F3（依赖 A3 / A5 / E2）与 F5（依赖 E4 新归档）
└─ [PAUSE] 人工审核结论是否改变下一阶段研究问题
      │
R7 逐批替换与退役
├─ 生成 old batch -> new accepted batch 映射
├─ 验证旧结果无 dashboard / report / figure / paper 引用
├─ 本机与 SSH 同批旧 payload 进入待退役清单
└─ 单独授权后删除或归档；保留审计 manifest
```

## 6. 重叠批次的处理原则

实验数量目前可控，计划优先选择完整性和可复核性：

1. 每个注册 outcome batch 完整运行，即使它与另一批次包含相同参数 cell。
2. 不跨批次手工抽掉重复 cells，也不把另一个批次的结果复制进来凑齐矩阵。
3. 每个批次保留自己的 batch identity、manifest、完整性检查和接受结论。
4. Cache V2 Score/Selection Artifact 只有在 Recipe identity、输入身份和内容校验全部精确一致时才允许 `HIT`；否则重新计算。
5. Legacy cache 一律不作为新批次输入。旧文件名、目录名或可见参数相同，不构成身份相同。

代价是少量重复计算；收益是批次边界清楚、失败可局部重启、报告不依赖隐式拼接，并且退役旧证据时能够证明替代关系。

## 7. 三类暂停点

### 7.1 硬前置暂停

SSH 不可达、GPU 不可枚举、正式解释器或 processed profile 不通过、完整 SHA 不一致、SyncMate 设备/peer 未注册时，不能开始正式 gate。

### 7.2 缺陷暂停

Selection/selector 缺陷与 GU method 缺陷先由 13 Runbook 判断修复链和影响范围。确认后才执行机器端 Runbook。修复必须形成新完整 SHA、新 result/cache identity，并从该批最小 gate 重新开始，禁止混用修复前后的 cells。

### 7.3 科学决策暂停

以下节点必须看结果再决定下一目标：

- E8 G3 后是否进入 G4；G4 后是否授权 G5。
- arxiv feasibility 和首 seed 后是否扩展。
- A3 是否存在值得继续验证的 hybrid synergy。
- E7 C.6a transfer ratio 是否达到 60%，从而进入 C.6b。
- 任一新批次是否改变论文主张、对照组或后续 ablation 的必要性。

暂停时只提交可审核结果和建议，不自动扩矩阵。

## 8. 旧结果清理设计

截止线是证据政策，不是一次性文件系统删除命令。换代过程中维护一个批次级 retirement ledger，至少包含：

- old batch identity、时间证据和所在设备；
- invalidation reason；
- new accepted batch identity、完整 SHA 和 trusted-index 记录；
- 下游引用扫描结果；
- 本机与 SSH payload 状态；
- 最终动作、操作者和时间。

`results/runs/` 同时含旧数据和较新的产物，archive、zip、aggregate、表格和 figures 也可能引用旧 evidence。因此不得按目录整删，也不得只按 filesystem mtime 判定。每批达到 `REPLACED` 后进入待退役清单；实际删除是独立、可审核、可回滚优先的操作，需另行授权。

## 9. 设计落地顺序

本设计经人工确认后，才进行以下落地：

1. 把树根和当前首个暂停点写入 `WORKPLAN.md`，不复制本设计全文。
2. 建立 inventory / retirement ledger 的机器可读 schema 与只读生成器。
3. 更新 SSH endpoint 并初始化 SyncMate collector/peer。
4. 生成远端只读快照，回填实际 Git、GPU、Python、processed data 和 result inventory。
5. 用当前注册 dry-run 固化第一批真实 cell 数和身份。
6. 只执行 R4 的 G1/G2/G3；提交 gate 报告并暂停。

## 10. 非目标

- 本设计不授权删除任何本机或 SSH 文件。
- 本设计不授权 E8 G4/G5、完整矩阵或条件 ablation。
- 本设计不把历史 50/50、40/40 或其他旧验收结果宣称为新的统一基线。
- 本设计不在文档中复制正式命令、解释器路径、cache key 或远端修复协议。
- 本设计不承诺恢复已经不再服务当前研究问题的旧实验；它们只需记录失效和退役原因。

## 11. 审核问题

人工审核本设计时只需确认三点：

1. 是否接受“有重叠也按注册批次完整重跑，只有精确 Cache V2 中间证据可复用”。
2. 是否接受 E8 G1/G2/G3 作为所有正式换代实验之前的树干 gate。
3. 是否接受逐批 `ACCEPTED -> PROJECTED -> REPLACED -> RETIRED`，而不是预先整目录删除。

确认后，下一份产物应是可执行实施计划，而不是直接启动完整实验。
