# PROGRESS — Resume Phase（2026-06 →）

> Last updated: 2026-06-15
> Role: **当前阶段的操作中枢**。休整一个月后回流数据 → reframe + rebuttal/重投准备。
> 与 `EXPERIMENT_DASHBOARD.md` 的关系：那份**冻结在 2026-05-07**（围绕已结束的 NeurIPS 4 天 push），现降级为"历史覆盖矩阵 + bug 档案"；**当前状态以本文件为准**。
> 维护规则：本文件只放 **状态 / 原因 / 勾选 / 链接**，不复制其他文档内容（遵守 `CLAUDE.md` 的 no-duplication 铁律）。每改一项勾选就更新 Last updated。

---

## 0. 一句话现状

数据回来了、**cora 跑得很全**（GCN+GAT 满 6×6×5），但回流数据**证伪了 paper 原核心贡献**（informed selector 打不过 degree）→ 需要 reframe。环境待重建（盘迁成 E:，可恢复），一个月整合工作未提交。**大方向（rebuttal vs 重投）待定**。

---

## 1. 现状快照（状态 + 为什么）

| 维度 | 状态 | 原因 / 细节 | 权威出处 |
|---|---|---|---|
| **数据** | 🟡 cora 满，arxiv 仅 pilot | cora_GCN/GAT_r0.05 满矩阵 + r0.01 切片 + α=0 ablation = 460 行 1 failed；arxiv = GIF+GNNDelete×3 selector，仅 seed42，不在主 CSV | 记忆 `project-state-resume-2026-06`；`results/_phase_b_aggregate.csv` |
| **环境** | 🔴 待重建（可恢复） | 换电脑、硬盘迁过来现为 **E: 盘**，conda `gnn` 的旧 `H:` 路径失效；本地暂时跑不了，需从 `../requirements.txt` 重建 + 把 CLAUDE.md/yaml 里 `H:`→`E:` | 同上 |
| **数据安全** | 🟢 已多处备份 | 服务器有完整原件；本地已备份到 `D:\backups\OpenGU_GULib\2026-06-15\` + `F:\…`（2482 文件校验通过） | 备份 MANIFEST |
| **代码** | 🟡 改动未提交 | 5/7 后改动很少、可修复；改过 7 个 paper 章节 + CSV + 图，未跟踪 `test1.py`/`arxiv_pilot_table.tex`；canonical 分支 `release/phase-b-fixes` | — |
| **L8 修复** | 🟢 代码已修 / 🔴 数据仍坏 | 写回逻辑 `d674f62` 已在 HEAD（与 `949d0f8` 逐字相同，**不用合分支**）；数据坏是服务器 **stale `.pyc`**（run 的 `git_sha=78872fc` 已含修复但跑了旧字节码）→ 只需清缓存重跑 | `limitations.md` L8 |
| **paper** | 🟡 已填实但有硬伤 | 0 个 `\interim`、图已重生、§5.2 已转 objective-misalignment；但 4 处数字 data 撑不住（见 §2） | 记忆 `paper-correctness-liabilities` |
| **大方向** | ⏸️ 待定 | 用户选了"先保住现状"。我的建议=重投+reframe（理由见 §4） | — |

---

## 2. 核心结论 & 必须处理的硬伤

1. **C1 — 贡献被证伪（决定性）**：全局 `degree +1.85 > pagerank +1.53 > im +1.19 > hybrid +0.21 > tracin −0.31`；逐方法 degree≥im≥tracin。→ reframe 成"结构杠杆是主攻击轴，influence 信号失配"。详 → 记忆 `paper-contribution-falsified`、`self/research_path_degree_severity_decomposition.md`。
2. **C2 — GNNDelete 在 n=5 不显著**（sd≫mean）。"最脆弱方法"措辞需带 n.s. 对冲。
3. **C3 — §A.4 hop-decay 被 L8 污染且 CSV 4 列全空**（GIF≡IDEA 逐位相同）。
4. **C4 — ΔF_noise(k=5) 磁盘上 5/6 方法 `f1_before`=null**，"F1 反升"暂不可复现。
5. **C5 — GraphRevoker 整 method 退化可疑**：`perf_before` 在所有 cell 都退化（cora_GCN_r0.05=0.583 / r0.01=0.570 / GAT=0.500，vs 其它方法 0.766~0.865）。根因=`e3bbd54` 自己标的未修完聚合器 bug（`opt_dataset.py:17` IndexError，"needs substantial work"）。后果：所有 paired ≈0 且 strategy 排序紊乱（IM/pagerank/tracin>degree 的"特例"是坏底座噪声，非真反例）；**paper §5.2 拿 GraphRevoker×GAT(perf_before=0.500) 当唯一 mechanism wedge —— 站不住**。另有 1 个 cell 因损坏分片 checkpoint（`torch.load: not a ZIP archive`）崩溃（小 transient）。**决策：修聚合器+整 method 重跑 vs paper 撤掉 GraphRevoker（报 5 个干净 method）。** 详 → 记忆 `project_graphrevoker_dispatcher_history`。

> C3/C4 详见 `limitations.md` L7/L8 + 记忆 `paper-correctness-liabilities`；C5 详见记忆 `project_graphrevoker_dispatcher_history`。

---

## 3. TODO 框架（勾选 + 为什么 + 卡在哪）

### P0 — 防灾 / 现在可做（多数不需环境）
- [x] 备份回流数据到 D:/F:（2026-06-15）
- [ ] **大方向决策**：rebuttal vs 重投（卡所有 P2）→ §4
- [ ] 提交这一个月工作到 `release/phase-b-fixes`（用户暂缓 commit，待确认）
- [ ] 把 arxiv pilot JSON 纳入版本控制 / 并进 CSV（同上待确认）
- [ ] 给硬伤数字加 caveat：§A.4 hop(C3)、GNNDelete n.s.(C2)、ΔF_noise(C4)、`A_appendix` 460/92 笔误 —— *纯 paper 编辑，不需环境*

### P1 — 投稿前必补（★=被环境重建阻塞）
- [ ] **重建 conda `gnn`**（E: 盘 / `../requirements.txt`）+ 把 `H:`→`E:` 重指 —— **解锁项**
- [ ] ★ **L8 redo**：清 `.pyc` + `python scripts/cleanup_if_family_collateral.py` + 重跑 cora GCN/GAT collateral（**代码不用改**；三个 cache 别动）→ 干净 GIF/IDEA gap+hop。关 C3
- [ ] ★ 把 4 个 hop 列灌进 `_phase_b_aggregate.csv`（扩 aggregator 读 `collateral.json::hop_decay`）。关 C3
- [ ] ★ 修 ΔF_noise `f1_before` null（重跑 k=5 或注明 anchor）。关 C4
- [ ] 收敛 figure 生成器分叉（`test1.py` vs `scripts/plot_neurips_figures.py`），删一个重生 6 图
- [ ] ★ **GraphRevoker 决策（C5）**：(a) 修 `e3bbd54` 标的聚合器 bug（`opt_dataset.py:17` IndexError）→ 整 method 重跑（perf_before 现 0.50-0.58 退化）；或 (b) paper 撤掉 GraphRevoker，报 5 个干净 method + 删 §5.2 GR×GAT 反例。**先定 (a)/(b)**。附带：1 个 cell 的损坏分片 checkpoint transient（`torch.load: not a ZIP archive`，删 `data/GraphRevoker/cora/` 损坏 .pt + 重跑即可）随 (a) 一起解
- [ ] 术语审计 "MIA" → "update-detection AUC"（纯写作）

### P2 — 加强（新实验=重投实质，全被环境阻塞）
- [ ] ★ **degree 分解 + 安全指数**二级结论（用已有数据 + L8 干净后）→ `research_path_degree_severity_decomposition.md`
- [ ] ★ GNNDelete 加 seed（n.s.→显著）或 reframe 成 budget/volume 驱动。关 C2
- [ ] ★ arxiv 全矩阵（≥3 seed、6 method）。关"scalability 只是 pilot"
- [ ] ★ **跑干净 citeseer（性价比最高）**：yaml 现成 `A5_citeseer_r0.05.yaml`(+r0.20)，6 method×{random,im,tracin}×5 seed=180 cell，~1h。关"单数据集"风险。⚠️ 2 月的 citeseer(MG-1/MG-3,在 `results/_archive_20260506/`)是 **pre-Phase-B 污染数据,不能引**；当前 `0_abstract.tex` 写"Cora, Citeseer, ogbn-arxiv"是 over-claim（citeseer 还没干净版）——要么跑 A5_citeseer，要么 abstract 改成 Cora+arxiv（565aaf6 已是后者）
- [ ] ★ 跨架构共识：加 1 个**非-MP** backbone（Cheb/APPNP）→ `idea_cross_arch_consensus.md`
- [ ] ★ IDEA/MEGU 定向 selector 审计（它们对 degree 有响应，"鲁棒"框架是错的）

---

## 4. 开放决策：rebuttal vs 重投

**我的建议：重投 + reframe**。三条驱动事实：(1) 数据证伪的是贡献本身（C1），prose 救不了；(2) 环境待重建，rebuttal 承诺的补充实验当下跑不出；(3) 无任何 rebuttal 痕迹（无 review 分数/response 文件）。
→ 但这是**用户的决定**，当前 `⏸️ 待定`。定了之后 P2 才好动。

---

## 5. 链接索引（详情看这些，本文件不复制）

- 现状/环境/数据：记忆 `project-state-resume-2026-06`
- 贡献证伪 + reframe：记忆 `paper-contribution-falsified`、`self/research_path_degree_severity_decomposition.md`
- paper 硬伤：记忆 `paper-correctness-liabilities`、`self/limitations.md`（L1-L8）
- 跨架构 idea：`self/idea_cross_arch_consensus.md`
- **进展库（Obsidian vault，往回看）**：`report/progress/_Home.md`（MOC 入口）→ 内含 [[Macro-Timeline]] 宏观 + [[2026-05_NeurIPS-Push]] 冲刺汇报 + [[Milestones]] + [[Findings-and-Decisions]]
- 历史覆盖矩阵 + bug 档案：`self/dashboard/EXPERIMENT_DASHBOARD.md`（冻结 2026-05-07）
- metric 定义：`self/dashboard/METRICS_CATALOG.md`
- 服务器执行：`SERVER_RUNBOOK.md`、`experiments/configs/README.md`

---

## 6. Changelog

- **2026-06-15** 建档。整合 status survey 结论：cora 满矩阵确认、C1 selector 倒置、L8 code-fixed/data-stale 定位、degree 分解路径、跨架构 idea、环境/数据更正。大方向待定。
