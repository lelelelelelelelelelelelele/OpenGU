# WORKPLAN — 操作中枢 + 阶段计划（实验 / ablation / 写作 / 画图）

> Last updated: 2026-07-24
> Role: **当前阶段的唯一操作中枢**（2026-06-27 起取代 `PROGRESS.md`）。现状快照 + 硬伤 + 方向 + 按工作流阶段拆的任务计划，全在这一份。
> 看板 `progress.html` 由 `scripts/dashboard/refresh.py` 从本文件生成（§0 现状 + §1 快照 + §5–§8 四阶段 kanban）；改完本文件跑一次 refresh（或靠 pre-commit hook 自动重生）。**单一真相是这份 markdown。**
> 维护规则：只放 **状态 / 原因 / 任务 / 链接**，不复制其他文档内容（`config_inventory.html` 管 cell 级进度、`PAPER_LIABILITIES_MAP.md` 管 overleaf 行号、`limitations.md` 管实测瓶颈——这里只链接）。
>
> 🔒 **thesis 锁死**：投出去的 contribution = *systematic audit + extreme heterogeneity + Vulnerability Fingerprint*。这轮（NeurIPS rebuttal 备战）只在框架内补证 + 写作；"结构杠杆主轴" reframe 留给"不中→重投"，入口为 [`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md)，**rebuttal 里做 = 自投降**。
>
> 图例：☐ 未做 · ◐ 进行中 · ✅ 完成 · ★ 需 GPU（AutoDL 镜像 `gnn_20`，可随时租）

---

## 0. 一句话现状

已投 NeurIPS、在等审稿、**rebuttal 还远 = 完善期**。回流数据 `degree ≥ IM/IF`（raw-F1 和 retrain gap 都是）——但**这没证伪贡献**：投出去的 thesis 本就是 *systematic audit + extreme heterogeneity + fingerprint*，不是"IM/IF 最强"。2026-07-22 的 153-cell GNNDelete 矩阵已于 2026-07-23 重分类为 **public-split、exact-k=7、L1 surrogate-transfer / engineering screen**：selector 与实际 GU target 不是同一 checkpoint，不能继续作为 target-direct 白盒结论。`target_direct_v1` 修正线已通过 `--no-ff` 合入 `main`；当前优先活 = 恢复 SSH GPU 与 `gnn_20` 环境后，按真实 5% train-candidate 预算执行 preflight、1-cell gate 与后续矩阵，准备合同见 `reports/target_direct_selection_PREPARATION_REPORT.{md,html}`。

---

## 1. 状态快照

| 维度 | 状态 | 原因 / 细节 | 权威出处 |
|---|---|---|---|
| **数据** | 🟢 cora 全+双备份 / arxiv 6-cell pilot（已核实） | cora 460（`ablating/` 460 + `4090/` 360 两份）+ D:/F: 备份，5 seed 无缺口。arxiv=6 cell（GIF/GNNDelete×{random,tracin,im}，seed42，r0.01）——**服务器权威 journal 核实只完成 6、全在本地、nothing stranded**；2 空壳（GIF_hybrid/GraphEraser）=中断未完成，T2/T3/r0.05/degree/pagerank 从没跑 | server journal 存档 `results/_journal/archive/`；`_phase_b_aggregate.csv` |
| **环境** | 🟡 本地分析就绪 / SSH GPU 与 `gnn_20` 未挂载 | SSH、Git 与 `/autodl-fs/data` 正常，磁盘约 196G 可用；但 2026-07-24 复测 `nvidia-smi` 仍返回 `No devices were found`，预期 `/root/miniconda3/envs/gnn_20/bin/python` 也缺失。当前容器只能做 Git/文件操作，恢复 GPU 与 accepted env 前不得启动 formal gate | 本次 SSH 实测；`reports/target_direct_selection_PREPARATION_REPORT.md` |
| **部署边界** | 🟢 SSH 同级目录已收口 | `/autodl-fs/data` 只保留 `.sys`、`.gitignore`、`OpenGU`；7 个证据树的 6952 个文件迁入 active checkout ignored archive，逐文件 SHA-256 全通过，2 个空壳删除。runner 已对 active checkout 外输出 fail closed | `reports/ssh_deployment_layout_CLOSEOUT_REPORT.{md,html}` |
| **数据安全** | 🟢 已多处备份 | 服务器有完整原件；本地备份 `D:\backups\OpenGU_GULib\2026-06-15\` + `F:\…`（2482 文件校验通过） | 备份 MANIFEST |
| **代码** | 🟢 target-direct 修正已验收并复核 | 旧 run 固定 `main@1c83bb4`，artifact/provenance 有效但科学身份降级。严格白盒修正已由 merge commit `71076bc` 合入 `main`：ScoreBundle 与 GU 绑定同一 checkpoint/state hash，真实 expected-k 与 candidate fail closed。2026-07-24 复核套件 `316 passed`；主矩阵固定 `last_layer`，`all_trainable` 已延期且不进入本轮配置/排期 | git；`reports/target_direct_selection_PREPARATION_REPORT.md` |
| **L8 修复** | 🟢 代码已修 / 🔴 数据仍坏 | 写回逻辑 `d674f62` 已在 HEAD（**不用合分支**）；数据坏是服务器 **stale `.pyc`** → 只需清缓存重跑（见 E2） | `limitations.md` L8 |
| **paper** | 🟡 thesis 站得住 / 有 rebuttal 硬伤 | contribution = audit + 异质性 + fingerprint，**未被 degree 证伪**（§2 C1）。这轮 = 换主指标 retrain gap + 压异质性，thesis 内不改写。两道必答题：① vs degree ② citeseer/arxiv scope（L6/L7，需租服务器补）。§2 数字硬伤待 caveat | 记忆 `paper-correctness-liabilities`；§2/§3 |
| **大方向** | 🟡 已厘清 | **不是"rebuttal vs 重投"二选一**：先备 rebuttal（thesis 内，§3）；不中再按 [`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md) 重投+reframe。别在 rebuttal 里改 thesis | §3 |

---

## 2. 硬伤 C1–C5（必须处理；overleaf 行号见 `PAPER_LIABILITIES_MAP.md`）

1. **C1 — 指标与实验身份均需修正，非贡献被证伪**：`degree ≥ IM/IF` 的既有 raw-F1 / retrain-gap 证据仍是 paper liability；但新增 E8 数字 `degree +2.30 pp`、TracInCP point `+0.17 pp` 只能作为 public-split、exact-k=7、L1 surrogate-transfer screen，不能再强化 target-direct 白盒 claim。严格比较必须让 selector 与 GU 复用同一 target checkpoint，并按真实 5% train candidates 删除。thesis 本是 *audit + 异质性*，不是"IM/IF 最强"；新矩阵仍需按 dataset 分层，不允许 Cora-only pooled 结论。→ `reports/target_direct_selection_PREPARATION_REPORT.md`。
2. **C2 — GNNDelete 在 n=5 不显著**（sd≫mean）。"最脆弱方法"措辞需带 n.s. 对冲 → W3-L2 / A7。
3. **C3 — §A.4 hop-decay 被 L8 污染且 CSV 4 列全空**（GIF≡IDEA 逐位相同）→ E2/E6/W3-L3。
4. **C4 — ΔF_noise(k=5) 历史 K5 口径缺 method-native before**：旧磁盘 5/6 方法 `f1_before=null`，不能继续充当 fresh anchor。→ **E3** 先走 fixed-SHA SSH formal 1-cell gate + 59-cell V2 expansion，取得 `method_perf_before/f1_after`，再本地 join 与 sanity；W3-L4 只引用新 accepted evidence。
5. **C5 — GraphRevoker 历史矩阵退化（✅ 代码与远端 E4 已通过；本地归档待闭环）**：旧 cell 的 `perf_before`=0.50–0.58 来自未完成的 aggregator/shard-ensemble 路径，旧数据继续禁止引用。2026-07-14 修复线已进入 active 基线；E4 在固定源码上完成 GCN/GAT × random/degree/pagerank/IM × 5 seeds，共 **40/40**，两阶段 gate 均通过、queue exit=0。后续不再写“代码仍未修好”；但本地同名 40-cell 仍是 2026-05-07 旧视图，完整 evidence import 前不得从它们提取 post-fix 数值。→ `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`（总状态）+ `docs/graphrevoker_postfix_canary_ACCEPTANCE_REPORT.md`（seed42）。

---

## 3. 方向：rebuttal-prep（这轮）→ 重投（仅当不中）

**已投 NeurIPS，在等审稿，rebuttal 还远 = 完善期。** 顺序是先 rebuttal、不中再重投；GPU 不是约束（可随时租）。

- **这轮 rebuttal（thesis 锁死，不改框架）**：换主指标 raw-F1 → **retrain gap**；头条压 **extreme heterogeneity**（GNNDelete 崩 16% / partition·IF 鲁棒）；IM/IF 降为 **fingerprint 诊断轴**；备两道必答题（① vs degree ② citeseer/arxiv scope）。
- **下一站（仅当不中 → 重投）**：才做"结构杠杆主轴、influence 失配"叙事转换（[`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md) + 强版机制 §7）。**这轮做它 = 自投降。**

> ⚠ **开放问题（2026-06-28）**：核心若**只剩 fingerprint** 会不会太轻？fingerprint 比旧 IF/IM 框架清晰，但作为**唯一**贡献偏描述性。强化核心 = reframe（结构杠杆，见 [`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md)）= **重投动作**；引用/对照方法与 GIF（影响函数）相关，可作强化抓手。**待定**：rebuttal 维持「audit + 异质性为实体、fingerprint 为框架」，还是认账偏轻 → 重投强化。**AI review（`文档规划/AI审稿_2026-06-28.md`）独立印证**：5→6 分条件之一就是"加更强的 mechanism-aware selector 或证明当前 selector 覆盖性"——正是此处的核心补强。

---

## 4. 排序 / 依赖（章法 —— 先看这张，别乱序开工）

```
E4 GraphRevoker 修复 + 整 method 重跑（✅ GCN/GAT 四策略五 seed，40/40）──► §5.2 GR×GAT wedge
   修复已验收；旧坏数据仍禁引，新 40-cell 矩阵作为权威证据

★ E2 L8 redo（清 .pyc 重跑 GIF/IDEA collateral）─► E6 hop 灌 CSV ─► W3-L3 hop caveat / F3 hop 图
                                                 └─► 唯一能验 IM/IF 在 IF 家族有无真 niche

★ E1 citeseer clean ─► W2-② scope 必答题 / W3-L6 scope 改写
E3 fresh K5：1-cell formal gate ─► 同 SHA 59-cell expansion ─► 本地 ΔF_noise sanity ─► W3-L4 anchor footnote

Cache V2 Selection Artifact 真实命中 + `proper-tracin-v1` versioned recipe gate ─► E7 umbrella ─► C.6a 同架构 surrogate ─► C.6b 跨 backbone surrogate

写作主线（多数纯 prose，现在就能做）：W1 指标切换 ─► W2 两道必答题 ─► W3 逐条 caveat ─► W4 融合
画图：F1 pipeline 图（独立）· F2 生成器收敛（独立）· F3 supp 图（依赖 A3/A5/E2）
```

**本轮主线**：`W1 指标切换 retrain gap → W2 必答题 → W3 纯 prose 那几条(L1/L2/L7/L8/L9) → E2 + A5 正式补量（E1/E4 已完成）+ E3 fixed-SHA K5 gate/full matrix 后本地 sanity → 回填 W3 剩余(L3/L4/L5/L6) + F3`。

---

## 5. 实验（主矩阵补证 / 关硬伤）—— 多数 ★需 GPU（E3：formal K5 生成需 GPU，后续 join/sanity 本地）

> 目标：把 paper 已写但磁盘撑不住的数字补干净。**不是新故事，是给 thesis 补证。** 进度数字源 = `config_inventory.html`。

### 正式实验运行位置（2026-07-14 锁定）

- **默认正式 lane = 已对齐、已完成预期 Git 清理的 SSH active checkout。**“正式实验”与“隔离 worktree”是两个不同维度；不能因为某次验收使用 fresh checkout，就推导以后正式实验都必须隔离。
- **部署根边界（2026-07-24）**：`/autodl-fs/data` 只允许平台 `.sys`、`.gitignore` 与单一 `OpenGU`。任何 fresh clone、worktree、evidence、ops、canary、materializer store 均须落在 active checkout 内；`scripts/validate_ssh_deployment_layout.py` 发现额外顶层条目即失败。历史 sibling 已无 symlink 地迁入 `results/_archive_ssh_peer_layout_20260724/`。
- 只有出现明确边界时才建隔离 worktree：并发分支、尚未解决的 tracked/运行态污染、未接收修复的验证，或 `experiments/run.py --dry_run` 已证明存在结果/cache identity 冲突。
- 判断前必须查 active 的 `git status --short --branch`、`git worktree list` 和 runner fingerprint 分类。ignored 历史结果本身不等于误判；若目标 cells 全部显示 `would_run`，不得再以“可能误跳过”为由强制隔离。
- 正式性的判据是固定源码/配置 provenance、每格四件套、质量 gate 和日志。用同一 full config/fingerprint 跑出的 1-cell gate 是正式矩阵的一部分，扩展时应 skip 而不是覆盖。
- **K5 formal lane（2026-07-22 锁定）**：注册 gate=`Cora/GCN/GraphRevoker/seed111/k=5`，先执行 `rerun_cora_noise_anchor.py --gate-only --expected-git-sha <full-sha>`；只有 gate manifest 的 SHA、canonical dataset fingerprint、cell identity 与 artifact SHA-256 全部匹配，才允许用同一 SHA 加 `--resume` 扩展剩余 59 cells。runner 对“无 gate 直接全跑”必须 fail closed。
- **A5 当前决定**：active 上五段 dry-run 为 `50 + 20 + 80 + 20 + 20 = 190/190 would_run`，不存在旧结果误跳过；完成 active 剩余 Git hygiene 后直接走 active formal lane。此前误建且 0 产物的 A5 worktree 不作为执行路径。
- **小图 Selection 数据合同（2026-07-21）**：public 17-method benchmark 只从 active checkout 的 `data/raw/{cora,citeseer,pubmed}` 读取，必须已有八个 raw 文件与 `processed/data.pt`，禁止自动下载/运行时加工；OpenGU integrated Selection 只从 `data/processed/{transductive,inductive}` pickle 读取。public split 与 OpenGU 80/20 split 不得混称。该合同已固化到根 `AGENTS.md`（所有 agent 强制规则）和 `CLAUDE.md`（SSH 操作规则）；shared/worktree/experiment checkout 不得作为 dataset root，既有 source-dataset 副本已在验证后清理。
- active 已补齐三套 public raw/PyG cache 与 Cora/CiteSeer canonical 80/20 pickle；PubMed canonical 80/20 pair 尚无可信历史副本。路径、逐文件 SHA-256、聚合 source fingerprint 与 split count 由 runner 写入每个 cold/warm summary。
- **一次性 GT 特例（2026-07-22）**：`9240b9a` 的 SSH public 17-output `9/9` 矩阵作为本 benchmark 的权威 GT 接受，不再重跑。依据是旧 shared 三套 public cache 的 9 个有效输入逐文件等于 active、ScoreBundle `produce()` 与两份 scorer core 在后续提交中未变、cold/warm/GPU/failure 证据已完整。该特例只接受 v3.0 result payload 与分析结论；不得把旧路径改称 active-root、把旧 cache 当 v3.1 exact hit，或扩展到 OpenGU 80/20 / GU outcome。未来新运行仍严格走 active canonical contract。
- **小图 Selection→GU 旧矩阵（2026-07-22；2026-07-23 重分类）**：clean SSH `main@1c83bb4` 上的 153 cells / 612 artifacts / 0 failures 与 SHA-256 仍是有效工程证据，但 scientific identity 仅为 public-split、exact-k=7、GateGCN-surrogate→OpenGU-GCN target 的 L1 transfer screen。它不回答 target-direct 白盒与真实 5% 预算。新正式链固定 70/10/20、同一 target checkpoint、`k=floor(0.05*train candidates)`；见 `reports/target_direct_selection_PREPARATION_REPORT.{md,html}`。

| ID | 任务 | config / 脚本 | 规模·耗时 | 关 | 状态 |
|---|---|---|---|---|---|
| **E4** ★ | **GraphRevoker 修复 + 整 method 重跑**（修正 aggregator / shard-ensemble collateral 路径；旧坏数据禁引） | GraphRevoker × `random/degree/pagerank/IM` × 5 seeds × GCN/GAT | 40 cells；两阶段 gate | C5 / L5 | ✅ **远端 40/40 passed**（GCN 20/20、GAT 20/20；queue exit=0）· ◐ **本地归档待闭环**（总状态 `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`；seed42 报告 `docs/graphrevoker_postfix_canary_ACCEPTANCE_REPORT.md`） |
| **E1** ★ | **跑干净 citeseer**（当前验收范围：stable 5 methods × random/IM × 5 seeds；TracIn 按本轮 gate 排除，GraphRevoker 转 E4） | `A5_citeseer_r0.05_stable_notracin.yaml` | 50 cells；fresh 4090 checkout | L6 / C-scope | ✅ **50/50 accepted**（0 failures；见 `docs/citeseer_e1_stable_ACCEPTANCE_REPORT.md`） |
| **E2** ★ | **L8 redo**：清 `__pycache__/*.pyc` + 重跑 GIF/IDEA collateral（代码已修 `d674f62`，三 cache 别动） | `scripts/redo_collateral_if_family.py` `phase_b_cora_{gcn,gat}.yaml` | GIF+IDEA×6×5×2=120 cell | C3 / L8 | ☐ |
| **E3** | **重建并计算 ΔF_noise anchor**：先在 clean SSH main、固定 full SHA、RTX 4090 上生成 fresh V2 K5 matrix；注册 `GraphRevoker/GCN/seed111` 1-cell gate，PASS 后同 SHA resume 剩余 59 cells。随后本地把 K5 `method_perf_before/f1_after` 与主矩阵口径核对并计算 ΔF_noise / `relative_f1_drop` sanity。⚠ K5 seed(111…)≠主矩阵 seed(42…)，跨 seed 只允许均值级近似并写入 caveat | `experiments/baseline_k5/rerun_cora_noise_anchor.py` | 1-cell gate + 59-cell expansion；再离线 join | C4 / L4 | ◐ runner gate contract 就绪；SSH dirty/GPU 阻断，0/60 formal cells |
| **E5** ★ | **arxiv 补量**：补 T2/T3 seed 或扩 6 method，关"只是 pilot" | `phase_b_arxiv_T2_seed212.yaml` `..._T3_seed722.yaml` | 18 cell/seed | L7 | ◐ T1 6/18 |
| **E6** ★ | **hop 列灌进 aggregate CSV**：扩 aggregator 读 `collateral.json::hop_decay`（**依赖 E2**） | aggregator 扩展 | 4 列 ×460 行 | C3 | ☐ 0/460 |
| **E7** ★ | **C.6 surrogate-transfer umbrella（严格门控）**：Cache V2 Selection Artifact 真实命中且 `proper-tracin-v1` versioned recipe 通过 gate 后，先做 **C.6a** 独立训练 GCN surrogate 选点 → GCN target GNNDelete，再做 **C.6b** GCN surrogate 选点 → GAT / GIN target GNNDelete。比较 target-direct TracIn、same-seed random、degree；主指标 = retrain gap transfer ratio，辅以 selection Jaccard。术语定为 query-free surrogate / 灰盒迁移，不写成纯黑盒 | 待建 `C6a_same_arch_surrogate.yaml`、`C6b_cross_backbone_surrogate.yaml`；gate = Cache V2 cold/warm exact hit + `proper-tracin-v1` recipe；显式记录 selection artifact ref，且 `selector_model_id != target_model_id` | C.6a 5 cell + C.6b 10 cell；5 seeds；若 transfer ratio ≥60% 再扩反向组合或第二个 GU family | L2-direct → L2-surrogate / threat-model realism | ◐ generic 17-output Cache V2 real-hit 已由 SSH `9/9` grandfathered GT 特例关闭，**不再要求 3×3 重跑**。仍待 `proper-tracin-v1`、E7 model-id/runner 集成与 C.6a/C.6b GU outcome |
| **E8** ★ | **小图 17-Selection → GNNDelete target-direct 白盒重做**：同一 OpenGU GCN checkpoint 同时用于 ScoreBundle 与 GU；70/10/20 无泄漏 split；真实 5% train-candidate budget；回答 TracIn vs degree/random 与 IF formula effect/feasibility | `experiments/target_direct_v1/*`; 从已验收 `main` 生成 pinned SyncMate config | G1 data preflight + G2 17-way selection + G3 1-cell GU gate + 153-cell matrix；612 artifacts；本轮仅 `last_layer`，`all_trainable` 延期 | C1 / selector×GU interaction | ◐ merge commit `71076bc` 已验收；2026-07-24 target/Cache V2/SyncMate 复核 `316 passed`，SyncMate smoke PASS。canonical raw 已齐，但三个 70/10/20 processed pairs 尚未 stage；SSH 无 GPU/`gnn_20`，故 formal gate/full 暂停 |

**坑提醒**：E1 的 2 月 citeseer 数据在 `_archive_20260506/` 是**污染数据，不能引**；改 GNN 架构维度才需清 `data/{Method}/`，E1–E6 不改架构故不用清。public Planetoid 固定 split（Cora/CiteSeer/PubMed train=`140/120/60`、val=`500`）不是 OpenGU canonical 80/20 processed split，二者结果不得互相改名。E8 是 direct selected-set → GNNDelete screen，不是 E7 query-free surrogate-transfer，不能关闭 `selector_model_id != target_model_id` 的 C.6a/C.6b。E7 禁止通过“清 IF / selection cache”切换算法口径：Legacy IF / Selection Cache 全程只读；算法换版创建带显式 algorithm / producer version 的新 V2 Recipe，旧 V2 Artifact 不删除、不覆盖，只有明确退役时才显式 retire。

---

## 6. Ablation

> 目标：把"现象沿某个轴怎么变"讲清楚。**多数有 decision gate**（先验证主矩阵 fingerprint 再决定值不值得跑），别无脑全开。

| ID | 任务 | config | 规模 | gate / 备注 | 状态 |
|---|---|---|---|---|---|
| **A3** ★ | **alpha-sweep**：hybrid_alpha {0,.25,.5,.75,1}×{GCN,GAT}×cora r0.05 | `A3_cora_{GCN,GAT}_alpha{0.00,0.25,0.75,1.00}.yaml` | 有效新增 ~180 cell（α=0≡im, α=1≡tracin） | **gate**：主矩阵 fingerprint 出来后，若 MEGU/IDEA 有非平凡坐标才值得跑。⚠ IM 整体打不过 degree → 价值有限 | ☐ 0/200 |
| **A5** ★ | **ratio-sweep**：cora r∈{0.01,0.10,0.20} + citeseer r∈{0.05,0.20} 四稳定策略补量（**active formal lane**；dry-run=`190/190 would_run`） | `A5_ratio_{0.01,0.10,0.20}.yaml`；`A5_citeseer_r{0.05,0.20}.yaml` | cora 90 cell/ratio；citeseer 缺失 190 cells | 不因 ignored 历史结果隔离。r0.20 的 GraphRevoker/GraphEraser 仍先做同配置 1-cell gate | ◐ cora r0.01=90；Citeseer E1=50 accepted；四策略 190 待跑（active） |
| **A6** | **新 backbone / 跨架构共识** — **2026-06-28 决策：不跑，降 future-work**。只用现有 GCN+GAT 两个 MP backbone；claim **收到 "across two message-passing backbones"**，limitations 主动认"两者同属 MP 家族，谱方法/graph-transformer 跨家族泛化留 future work"。要补也只在 reviewer 点名 / 下篇当卖点时，按**窄探针**(cora×1 新 backbone×degree-vs-1-informed×≥3 seed)，**别均匀撒** | (不跑) | — | → `idea_cross_arch_consensus.md` §4 | ✅ 决策：scope-to-MP |
| **A7** ★ | **GNNDelete +seed**（n.s.→显著）或 reframe 成 volume-driven | 扩 `phase_b_cora_*` seeds | +N seed | 关 C2（n=5 sd≫mean）。P2 | ☐ |
| **A8** | **RR-set IM / RR-IF-Hybrid**（统一 IMM 框架，IF 作 bicriteria） | 新算法 | ~2-3 天实现 | limitations L6-(C)，**ICLR-tier follow-up**；rebuttal 不做 | ☐ option |
| **A9** ★ | **加新 GU 方法（拓宽 audit 广度）**：现 6 method，考虑再纳 1–2 个新方法 → audit 更扎实（呼应"fingerprint 偏轻"的担忧） | 新 method 接入 | 视方法 | 拓 audit | ☐ option |

**Aggregator 待建**：`scripts/plot_supp_figures.py::plot_alpha_synergy`（A3）、`::plot_ratio_elasticity`（A5）—— 见 F3。

---

## 7. 写作（thesis 锁死，框架内）

> 目标：把 thesis 讲法对齐到现有数据。多数**纯 prose、现在就能做**；少数等阶段实验回填。
> **打底**：per-method 优劣（audit 主表）是论文的基础结果——先立住，再谈 selector / 异质性。

| ID | 任务 | 关 | 依赖 | 状态 |
|---|---|---|---|---|
| **W1** | **指标切换（本轮核心）**：主指标 raw-F1 → **retrain gap**；头条压 *extreme heterogeneity*（GNNDelete 崩~16% / partition·IF 鲁棒）；IM/IF 降为 fingerprint 诊断轴 | C1 | — | ☐ 纯 prose |
| **W2** | **两道 rebuttal 必答题**：① vs degree —"approximation-gap 上 degree/IM 都强，contribution 是异质性、非某 selector 最强"；② citeseer/arxiv scope | C1 / L6 / L7 | ②待 E1 | ☐ |
| **W3** | **硬伤逐条 caveat**（对照 `PAPER_LIABILITIES_MAP.md` overleaf 行号） | L1–L9 / C2–C4 | 见下 | ☐ |
| **W4** | **paper 整理/融合 + 重查表格**：多版收敛（云端基底 + 并入 reframe 框架 + 落 C1–C6 + 清弃用如 `arxiv_pilot_table.tex`），逐表 check | — | W1–W3 | ☐ |
| **W5** | **术语审计** "MIA" → "update-detection AUC"（全文） | — | — | ☐ 纯 prose |
| **W6** | **review collection**：汇总 评审/导师/AI 意见，建一个 **reviewer意见文件区**（放 OB/Obsidian 最好）。已有 `report/advisor_report_2026-06-16.html` + AI review `文档规划/AI审稿_2026-06-28.md`（**5/10 weak reject**；三痛点已映射到 E1·E5 / W1·W3 / C2·A7） | — | — | ☐ |
| **W7** | **读未读论文**：GraphRevoker / MEGU / UTU 等 → related work + 反防审稿人引用 | — | — | ☐ |
| **W8** | **Supplementary 整理**：appendix（hop §A.4 / 460 行说明 / 诊断 suite 定义）成形 | L8 / C3 | A.4 待 E2 | ☐ |
| **W9** | **AI 辅助数据分析**：让 AI 过一遍结果矩阵，挖异质性/反例/可写点（喂 `_phase_b_aggregate.csv` + collateral） | — | — | ☐ |
| **W10** | **重投叙事激活（仅 reject/resubmit 后）**：从届时 main 手工重写 abstract/intro，使用 [`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md) 的叙事骨架，不 cherry-pick 历史 paper；所有数字由最终 accepted matrix 回填 | resubmission gate | E4 本地归档 + F5 | ☐ dormant |

**W3 拆解（按能否现在做）**：
- **现在就能改（纯 prose）**：`L1` abstract selector reframe（列全 6 selector、degree/PageRank 主导、IM/IF 标 objective-misaligned）· `L2` GNNDelete n.s. 对冲· `L7` arxiv pilot scope· `L8` 460/92 笔误· `L9` verdict label 加"描述性非统计证明"一句· **清掉"Phase B.2 refresh / await H800 retrain"等未完成/延期语句**（AI review 头号痛点：暴露"关键实验没跑完"）· 弱化"architectural immunity / Shard Protection / strictly governed"等过满措辞（review 痛点②）。
- **等实验回填**：`L3` hop caveat ←**E2**· `L4` ΔF_noise anchor footnote ←**E3**· `L5` §5.2 wedge（重跑前标 *pending*、不下结论）←**E4** 修复后回填真数据· `L6` citeseer scope ←**E1**。

---

## 8. 画图

| ID | 任务 | 依赖 | 状态 |
|---|---|---|---|
| **F1** | **方法 / pipeline 示意图**：一张步骤图 / 机制图（≠ 结果图） | 独立 | ☐ |
| **F2** | **收敛图生成器分叉**：保留 `scripts/plot_neurips_figures.py` 为唯一入口，移植 `test1.py` 所需样式后退役后者；修 `paired_dF_pct` schema/单位、repo root、输入 manifest 与 tuple-count fail-fast contract | 可先修代码；最终图等 accepted matrix | ☐ |
| **F3** | **Supp 图**：A3 alpha-synergy 图 + A5 ratio-elasticity 图；hop-decay 图重生 | A3 / A5 / E2 | ☐ |
| **F4** | **exp 看板改进**：`config_inventory` 现在仍不够清晰，迭代成"一眼看懂跑了啥 / 缺啥" | 独立 | ✅ 验收通过(conditional)，见 [`CONFIG_INVENTORY_ACCEPTANCE.md`](CONFIG_INVENTORY_ACCEPTANCE.md)（重设计为 heatmap + CSV 生成器；遗留 F-1 A3 口径 / F-2 失败 cell 披露 待拍板） |
| **F5** | **FIG-5 最终重生 + 入库**：E4 accepted evidence 本地导入并裁定 inclusion 后，基于最终 aggregate 重算 Pearson/Spearman、strategy means 与 selection-Jaccard；生成到 temp，核对 PDF text/视觉/caption、干净 LaTeX 编译后，仅对最终 `FIG-5_Alignment.pdf` 精确 `git add -f` | E4 本地归档 + F2；若 paper 扩矩阵则等对应 exp gate | ☐ blocked |

---

## 9. 链接索引

- **全项目文档地图**：`../../文档规划/_文档地图.md`（MOC + 零散 md 归集处）
- 配置矩阵监督：[`config_inventory.html`](config_inventory.html) · 数据 [`config_inventory.csv`](config_inventory.csv) · 生成器 [`scripts/dashboard/gen_config_inventory.py`](../../scripts/dashboard/gen_config_inventory.py)（改 CSV `done` 后重跑即刷新）· 验收 [`CONFIG_INVENTORY_ACCEPTANCE.md`](CONFIG_INVENTORY_ACCEPTANCE.md)
- 硬伤映射：[`PAPER_LIABILITIES_MAP.md`](PAPER_LIABILITIES_MAP.md)（L1–L9 + overleaf 行号）
- 实测瓶颈：[`self/limitations.md`](../limitations.md)（L1–L8）
- ablation / regression 入口：`experiments/configs/A3_alpha_sweep_SPEC.md` · `A5_README.md` · `sanity_graphrevoker*.yaml`；GraphRevoker 验收结论见 `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`
- 跨架构 idea：`self/idea_cross_arch_consensus.md`
- 历史覆盖矩阵 + bug 档案（冻结 2026-05-07）：[`EXPERIMENT_DASHBOARD.md`](EXPERIMENT_DASHBOARD.md)
- 旧状态中枢（已并入本文件）：[`PROGRESS.md`](PROGRESS.md)
- 重投蓝本（**这轮不碰**）：[`RESUBMISSION_BLUEPRINT.md`](../../report/paper/RESUBMISSION_BLUEPRINT.md)；精确历史恢复点 `archive/paper-alignment-20260507` / `archive/paper-alignment-wip-20260507`

---

## 10. Changelog

- **2026-07-24** E8 target-direct 重跑复核：主矩阵参数域固定为 `last_layer`，`all_trainable` 按用户决定延期并从正式配置、SyncMate recipe 与本轮排期中移除；撤回基于 public split 60–140 candidates 的旧 small-graph 时间估算，正式 5% 理论预算更新为 Cora/CiteSeer/PubMed=`94/116/690`。target checkpoint、split、expected-k、runner propagation、Cache V2、GNNDelete architecture 与完整 SyncMate tests 共 `316 passed`，SyncMate 临时 collect/verify/index smoke PASS。SSH active Git 干净且与本地/origin 对齐，但无 GPU/`gnn_20`，三个 70/10/20 processed pairs 尚未 stage，formal E8 仍暂停。
- **2026-07-24** retired SSH path 第二轮清退：按 `main@4170816` 摸排出 49 个 tracked 文件 / 499 处旧 sibling 前缀；报告改指 archive/canonical access 并加迁移说明，GU v1–v4 配置全部 repo-relative，19 个 imported benchmark JSON 做带 baseline/aggregate-hash 元数据的路径归一化，17 个 consumer 的 69 处 SHA-256 按 canonical Git-blob/Linux LF 字节重算并由 `.gitattributes eol=lf` 固定。新增全 tracked 文本 validator，当前 1214 个 UTF-8 文件 0 matches；原始字节仍由 Git 基线保存。见 `reports/ssh_deployment_layout_CLOSEOUT_REPORT.{md,html}`。
- **2026-07-24** SSH 部署根摸排与收口：确认 2026-07-14 至 07-22 的 fresh clone / evidence / ops / canary / materializer 与两组 tracked 绝对路径配置共同造成 9 个 OpenGU sibling；2 个空壳删除，7 个证据树共 6952 files / 1,078,876,926 bytes 原子迁入 active ignored archive，逐文件 SHA-256 通过，清单锚点 `32961210ff7a874b7f13f75987be19f5d825002e9f453bb5ac015976e048882e`。runner 增加 active-checkout path fail-closed，Gate4 与 GU v5 改为 repo-relative，新增顶层布局验收器。见 `reports/ssh_deployment_layout_CLOSEOUT_REPORT.{md,html}`。
- **2026-07-22** K5 formal 顺序固化：E3 从“沿用旧 K5 后纯本地 join”更新为 fresh V2 formal lane；注册 `Cora/GCN/GraphRevoker/seed111/k=5` 单 cell gate，manifest 绑定 full main SHA、canonical dataset fingerprint、cell identity 与 artifact SHA-256。全矩阵必须在 gate PASS 后用同一 SHA `--resume`，无 gate 直接全跑由 runner 拒绝。
- **2026-07-22** 旧 `paper/alignment-experiment` 价值迁移与清理完成：叙事骨架、FIG-5 设计契约和 Jaccard 分析问题提炼到 `report/paper/RESUBMISSION_BLUEPRINT.md`；F2 展开生成链修复，新增 F5（新 evidence 后重生/入库 FIG-5）和 W10（仅重投时激活）；两个 `archive/paper-alignment-*` tag 经 peel 验证后，原 alignment stash 已 drop、旧分支已删除，不再以活动 branch/stash 充当知识库。
- **2026-06-27** 建档（实验/ablation/写作/画图 四阶段，收敛 PROGRESS §2/§3 + limitations + PAPER_LIABILITIES_MAP + 配置矩阵）；配套 `config_inventory.{csv,html}` 监督看板。
- **2026-06-27（晚）** E4 决策定为 **修 + 重跑**（不 drop / 不 caveat）；并 **升级为唯一操作中枢**：折入 PROGRESS §0/§1/§2/§4（现状/快照/硬伤/方向），`refresh.py` 重指到本文件生成 `progress.html`（看板列改为四阶段），`PROGRESS.md` 退成指针。
- **2026-06-28（SUPERSEDED 2026-07-22）** E3 当时从 ★GPU 降级为本地重算：依据旧 k=5 `f1_before=null`，计划从主矩阵取 before。该方案已被 2026-07-22 fresh V2 K5 formal gate/full-matrix 决策取代；旧证据只保留为历史背景。
- **2026-06-30** **F4 完成 + 验收**：`config_inventory` 重设计为 coverage-heatmap（分类 block + A3 α-grid + 红/黄/绿 fill）、全派生（消除 3 处硬编码）、配 CSV→HTML 生成器 `gen_config_inventory.py`（一处改 `done` 全盘联动，实测回填闭环）。验收报告 [`CONFIG_INVENTORY_ACCEPTANCE.md`](CONFIG_INVENTORY_ACCEPTANCE.md)：功能 + 数据真实性全过（headline 对得上 `_phase_b_aggregate.csv` / 磁盘）；遗留 **F-1**（A3 实有 10 个 α=0.00 alias 结果、看板报 0）/ **F-2**（A5_ratio_0.01 90/90 含 1 个已知 GraphRevoker 失败 cell）两项 done 口径待拍板（见 VALIDATION_LOG V-2026-06-30-01）。
- **2026-06-28** 并入 `p.md` 笔记：E4 提到第一（audit 底座 + OpenGU 上游老 bug + 争取交叉验证）；W6 加 reviewer意见文件区(OB)；新增 W9(AI 数据分析)/F4(exp 看板改进)/A9(加新方法)；§3 记下"fingerprint 是否偏轻"开放问题；§7 加"per-method 优劣打底"。
- **2026-06-28** 接入 AI review `文档规划/AI审稿_2026-06-28.md`（5/10 weak reject，**非官方审稿** → 现状仍完善期）→ W6；三痛点（scope 没跑完 / 叙述过满 / 统计偏弱）对应 E1·E5 / W1·W3 / C2·A7（均已在计划内）；W3 加"清未完成语句"；§3 fingerprint 偏轻被 review 印证。
- **2026-06-28** 建 `文档规划/` 文件区（零散 md 的家 + `_文档地图.md` 全项目分类 MOC）；根目录两份零散 md（规划手记、AI 审稿）归入并加 frontmatter；`daily-log` / `progress` 不动、只索引。
- **2026-07-12** 新增 E7 `L2-surrogate transfer sanity`：把旧 C.6 拆成 C.6a same-architecture surrogate（GCN→GCN）与 C.6b cross-backbone surrogate（GCN→GAT/GIN）；要求 Cache V2 显式区分 `selector_model_id` / `target_model_id`，并以 proper TracIn、5 seeds、retrain-gap transfer ratio 为执行口径。
- **2026-07-14** 同步 Git 与 E7 gate：代码基线记录为 `main` / `origin/main`=`3f631fb`，当前在 `codex/opengu-worktree-recovery-20260714` 收口多 session dirty tree；E7 统一为 Cache V2 real-hit + versioned `proper-tracin-v1` gate 后的 C.6a/C.6b umbrella，Legacy IF / Selection Cache 保持只读，V2 换版只建新 Recipe、明确退役才显式 retire。
- **2026-07-14** E1 stable scope 真机验收：Citeseer/GCN/r=0.05，GIF/IDEA/GNNDelete/MEGU/GraphEraser × random/IM × 5 seeds = **50/50 accepted**；runner rc=0、机器验收 0 errors、active Legacy path/size/mtime/SHA-256 聚合 hash 不变。该完成项不包含 TracIn/Hybrid/GraphRevoker，scratch Legacy-format cache 命中不记作 V2 runner hit；GraphRevoker 继续走 E4 独立 gate。
- **2026-07-14** E4 seed42 post-fix canary：Cora/GCN/r=0.05 的 GraphRevoker random/degree/pagerank/IM **4/4 accepted**，runner rc=0、机器验收 0 errors；10+10 shard checkpoints 与聚合权重有效，NPZ 复算 collateral 一致，旧单 shard 0.50–0.58 regression 已关闭。当前提交的独立 Cache V2 Citeseer Selection recheck 也完成 cold miss → warm exact hit；两条证据分开，E4 多 seed 和 runner V2 接入仍 pending，Hybrid/TracIn 未执行。
- **2026-07-21/22** 小图 Selection dataset 合同与 GT 特例收口：SSH active 主目录补齐 `data/raw/{cora,citeseer,pubmed}`，回填 accepted CiteSeer canonical processed pair，并区分 public fixed split 与 OpenGU 80/20 split；B/C、C-target 和正式/诊断 TracIn runner 均改为 repo-relative fail-closed source + SHA-256/split/Git provenance。相关测试本地/远端均 `52 passed`，cold/warm smoke 通过。经确认旧 shared 输入逐文件等于 active、scorer 语义未变，已有 SSH 3×3 GPU 矩阵按一次性 grandfathered GT 接受，不再安排重复运行。
- **2026-07-21** Dataset SSH 治理固化：根 `AGENTS.md` / `CLAUDE.md` 明确 canonical source 只能位于 active `data/raw` 或 `data/processed/{transductive,inductive}`；method/unlearning/runtime artifacts 不算替代 dataset root，外部副本禁作正式输入，缺失数据须先在 active staging + accepted preprocessing 后再跑。
- **2026-07-21** Dataset 历史副本清理：在逐文件/语义等价、caller reference=0、process reference=0 后，删除 SSH 65 files / 543,652,340 bytes 与本地 33 files / 116,595,446 bytes；复扫确认 SSH 外部 populated source roots=`0`，实验结果及 method-specific artifacts 未删除。PubMed canonical 80/20 pair 仍缺失。
- **2026-07-20** GraphRevoker 文档状态收敛：OB:13 从一次性 Runbook 迁移为验收/回归测试台账；代码与远端 E4 标 `PASS`，本地 40-cell evidence import 标 `ARCHIVE PENDING`，2026-05-07 旧 SHA 视图永久 `INVALID`；新增双格式总状态报告，TracIn/Hybrid 继续独立 gate。
- **2026-07-21/22** 小图 Selection cold/warm 全量实测与 authority 决议：Cora/CiteSeer/PubMed × seeds 42/212/2024，正式 17-output ScoreBundle 共 `9/9` cells、`153/153` 方法级 cold miss→warm exact hit，0 failures；cold bundle mean/max `6.8038/9.1624 s`，warm read `0.3200/0.9635 s`，峰值 allocated/reserved `357/384 MiB`。证据见 `reports/small_graph_selection_BENCHMARK_REPORT.{md,html}`；本轮作为 public benchmark GT/analysis authority 接受且不重跑，关闭 generic Cache V2 real-hit，但不替代 proper-TracIn 的 E7 集成 gate。
- **2026-07-22/23** E8 旧矩阵完成后重分类：`153/153` cells、`612/612` artifacts、0 failures 与逐文件 SHA-256 仍成立；但由于 GateGCN hidden16/200-epoch selector 与 OpenGU GCN hidden64/100-epoch target 不是同一 state，且目录标 5% 实际 exact `k=7`，所有效果数字只保留为 L1 surrogate-transfer / engineering evidence。严格 target-direct 修正已实现同一 checkpoint 双哈希绑定、70/10/20 validation target、真实 5% expected-k、candidate/count fail-closed、cold/warm/VRAM/failure 计时合同，并由 `71076bc` 合入 `main`；formal GPU gate 尚未启动。见 `reports/target_direct_selection_PREPARATION_REPORT.{md,html}`。
- **2026-07-23** Git/SSH 收口与运行环境复核：本机、`origin/main` 与 SSH active checkout 已对齐，均只保留一个 active worktree；已合并短期分支清理完成，backup/stash 继续保留。SSH 当前可连接且 `/autodl-fs/data` 约 196G 可用，但无 GPU device、无默认 Python/conda、无预期 `gnn_20` 解释器，故 E8 formal gate 在环境恢复前保持暂停。
