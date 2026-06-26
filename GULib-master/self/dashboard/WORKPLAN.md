# WORKPLAN — 按阶段拆解（实验 / ablation / 写作 / 画图）

> Last updated: 2026-06-27
> Role: **执行计划（按工作流阶段切）**。把散落在 PROGRESS §2/§3、`limitations.md`、`PAPER_LIABILITIES_MAP.md`、配置矩阵里的"要对齐的事"收敛成一张有章法的表：**每条任务 = 做什么 + 为什么(关哪条硬伤) + 哪个 config/脚本 + 规模耗时 + 依赖/gate**。
>
> **与 PROGRESS.md 的分工**（不复制、只链接）：
> - **PROGRESS.md** = 当前状态中枢（一句话现状 + 勾选 + 开放决策）。**勾选状态以它为准。**
> - **本文件** = 把同一批任务按 *实验/ablation/写作/画图* 重排，补上 config 映射、耗时、排序依赖。**结构与排序看这里。**
> - **`config_inventory.html`** = 配置矩阵的 cell 级 done/target 监督看板。**实验进度数字以它为准。**
> - 硬伤详情：`PROGRESS.md §2`(C1–C5)、`PAPER_LIABILITIES_MAP.md`(L1–L9, 带 overleaf 文件/行号)、`self/limitations.md`(L1–L8, 实测瓶颈)。
>
> 🔒 **thesis 锁死**：投出去的 contribution = *systematic audit + extreme heterogeneity + Vulnerability Fingerprint*。这轮（NeurIPS rebuttal 备战）只在框架内补证+写作；"结构杠杆主轴" reframe(`565aaf6`) 留给"不中→重投"，**rebuttal 里做 = 自投降**。
>
> 图例：☐ 未做 · ◐ 进行中 · ✅ 完成 · ★ 需 GPU（AutoDL 镜像 `gnn_20`，可随时租）· 🔑 决策先行

---

## 阶段 0 — 关键排序 / 依赖（先看这张，别乱序开工）

```
E4 GraphRevoker 修复（修聚合器 bug + 整 method 重跑，★ code+server）──► §5.2 GR×GAT wedge
   决策已定 = 修，不 drop / 不 caveat；方法保留在 6-method audit，重跑前 wedge 标 pending、不下机制结论

★ E2 L8 redo（清 .pyc 重跑 GIF/IDEA collateral）─► E6 hop 灌 CSV ─► W3-L3 hop caveat / F3 hop 图
                                                 └─► 唯一能验 IM/IF 在 IF 家族有无真 niche

★ E1 citeseer clean ─► W2-② scope 必答题 / W3-L6 scope 改写
★ E3 ΔF_noise k=5 anchor ─► W3-L4 anchor footnote

写作主线（多数纯 prose，现在就能做）：W1 指标切换 ─► W2 两道必答题 ─► W3 逐条 caveat ─► W4 融合
画图：F1 pipeline 图（独立）· F2 生成器收敛（独立）· F3 supp 图（依赖 A3/A5/E2）
```

**本轮主线（写作锁 thesis）**：`W1 指标切换 retrain gap → W2 必答题 → W3 纯 prose 那几条(L1/L2/L7/L8/L9) → 租服务器跑 E1/E2/E3/E4(含 GraphRevoker 修复) → 回填 W3 剩余(L3/L4/L5/L6) + F3`。

---

## 阶段 1 — 实验（主矩阵补证 / 关硬伤）★ 全部需 GPU

> 目标：把 paper 已写但磁盘撑不住的数字补干净。**不是新故事，是给 thesis 补证。**
> 进度数字源 = `config_inventory.html`（cora 走 `_phase_b_aggregate.csv`，arxiv 走 disk）。

| ID | 任务 | config / 脚本 | 规模·耗时 | 关 | 状态 |
|---|---|---|---|---|---|
| **E1** ★ | **跑干净 citeseer**（堵 scope 漏洞，最高优先） | `A5_citeseer_r0.05.yaml` | 6×3×5=90 cell, ~1h | L6 / C-scope | ☐ 0/90 |
| **E2** ★ | **L8 redo**：清 `__pycache__/*.pyc` + 重跑 GIF/IDEA collateral（代码已修 `d674f62`，三 cache 别动） | `scripts/redo_collateral_if_family.py` `phase_b_cora_{gcn,gat}.yaml` | GIF+IDEA×6×5×2=120 cell collateral | C3 / L8 | ☐ |
| **E3** ★ | **修 ΔF_noise anchor**：重跑 k=5 把 `f1_before` 持久化（或注明 anchor 缺失） | `experiments/baseline_k5/fill_missing_cora.py` | 4×5=20 run, ~15min | C4 / L4 / L7(lim) | ☐ |
| **E4** ★ | **GraphRevoker 修复**（决策已定 2026-06-27 = **修，不 drop / 不 caveat**）：修聚合器 `opt_dataset.py:17` IndexError（`e3bbd54` 未完成）→ 清损坏 `data/GraphRevoker/cora/` .pt → 整 method 重跑（`perf_before` 现 0.50–0.58 退化） | `phase_b_cora_{gcn,gat}.yaml` + 聚合器修复 | 整 method 重跑 | C5 / L5 | ☐ |
| **E5** ★ | **arxiv 补量**：补 T2/T3 seed 或扩 6 method，关"只是 pilot" | `phase_b_arxiv_T2_seed212.yaml` `..._T3_seed722.yaml` | 18 cell/seed | L7 | ◐ T1 6/18 |
| **E6** ★ | **hop 列灌进 aggregate CSV**：扩 aggregator 读 `collateral.json::hop_decay`（**依赖 E2 干净数据**） | aggregator 扩展 | 4 列 ×460 行 | C3 | ☐ 0/460 |

**E4 决策已定（2026-06-27）= 修 + 重跑**（用户明确：**不 drop、不 caveat** —— 不报、也不洗坏数据）。★ code+server 任务，随租服务器做；**重跑前** paper 的 §5.2 GR×GAT wedge 标 *pending re-run*、不下机制结论，GraphRevoker 仍留在 6-method audit。
**坑提醒**：E1 的 2 月 citeseer 数据在 `_archive_20260506/` 是**污染数据，不能引**；改 GNN 架构维度才需清 `data/{Method}/`，E1–E6 不改架构故不用清。

---

## 阶段 2 — Ablation

> 目标：把"现象沿某个轴怎么变"讲清楚。**多数有 decision gate**（先验证主矩阵 fingerprint 再决定值不值得跑），别无脑全开。

| ID | 任务 | config | 规模 | gate / 备注 | 状态 |
|---|---|---|---|---|---|
| **A3** ★ | **alpha-sweep**：hybrid_alpha {0,.25,.5,.75,1}×{GCN,GAT}×cora r0.05 | `A3_cora_{GCN,GAT}_alpha{0.00,0.25,0.75,1.00}.yaml`（α=0.5 在主矩阵） | 有效新增 ~180 cell（α=0≡im, α=1≡tracin cache-reuse） | **gate**(SPEC §decision)：主矩阵 fingerprint 出来后，若 MEGU/IDEA 有非平凡坐标才值得跑；否则只确认平坦曲线。⚠ IM 整体打不过 degree → 价值有限 | ☐ 0/200 |
| **A5** ★ | **ratio-sweep**：r∈{0.01,0.10,0.20} cora GCN（+citeseer 见 E1） | `A5_ratio_{0.01,0.10,0.20}.yaml` | 90 cell/ratio | r0.01 **已完成**；r0.10/0.20 待跑。⚠ r0.20 可能崩 GraphEraser（空 shard），先 sanity | ◐ 90/450 |
| **A6** ★ | **新 backbone / 跨架构共识**：GIN 已有 config；加 1 个**非-MP**(Cheb/APPNP) | `A6_cora_gin_r0.05.yaml` + 新建 | 75 cell/backbone | → `idea_cross_arch_consensus.md`。P2 加分 | ☐ 0/75 |
| **A7** ★ | **GNNDelete +seed**（n.s.→显著）或 reframe 成 volume-driven | 扩 `phase_b_cora_*` seeds | +N seed | 关 C2（n=5 sd≫mean）。P2 | ☐ |
| **A8** | **RR-set IM / RR-IF-Hybrid**（统一 IMM 框架，IF 作 bicriteria） | 新算法 | ~2-3 天实现 | limitations L6-(C)，**ICLR-tier follow-up**；rebuttal 不做 | ☐ option |

**Aggregator 待建**：`scripts/plot_supp_figures.py::plot_alpha_synergy`（A3 曲率指数）、`::plot_ratio_elasticity`（A5 弹性曲线）—— 见 F3。

---

## 阶段 3 — 写作（thesis 锁死，框架内）

> 目标：把 thesis 讲法对齐到现有数据。多数**纯 prose、现在就能做**；少数等阶段 1 数据回填。

| ID | 任务 | 关 | 依赖 | 状态 |
|---|---|---|---|---|
| **W1** | **指标切换（本轮核心）**：主指标 raw-F1 → **retrain gap**；头条压 *extreme heterogeneity*（GNNDelete 崩~16% / partition·IF 鲁棒）；IM/IF 降为 fingerprint 诊断轴 | C1 | — | ☐ 纯 prose |
| **W2** | **两道 rebuttal 必答题**：① vs degree —"approximation-gap 上 degree/IM 都强，contribution 是异质性、非某 selector 最强"；② citeseer/arxiv scope | C1 / L6 / L7 | ②待 E1 | ☐ |
| **W3** | **硬伤逐条 caveat**（对照 `PAPER_LIABILITIES_MAP.md` overleaf 行号）| L1–L9 / C2–C4 | 见下 | ☐ |
| **W4** | **paper 整理/融合 + 重查表格**：多版收敛（云端基底 + 并入 reframe 框架 + 落 C1–C6 + 清弃用如 `arxiv_pilot_table.tex`），逐表 check | — | W1–W3 | ☐ |
| **W5** | **术语审计** "MIA" → "update-detection AUC"（全文） | — | — | ☐ 纯 prose |
| **W6** | **review collection**：汇总 评审/导师/AI 修改意见（起点 `report/advisor_report_2026-06-16.html`） | — | — | ☐ |
| **W7** | **读未读论文**：GraphRevoker / MEGU / UTU 等 → related work + 反防审稿人引用 | — | — | ☐ |
| **W8** | **Supplementary 整理**：appendix（hop §A.4 / 460 行说明 / 诊断 suite 定义）成形 | L8 / C3 | A.4 待 E2 | ☐ |

**W3 拆解（按能否现在做）**：
- **现在就能改（纯 prose）**：`L1` abstract selector reframe（列全 6 selector、degree/PageRank 主导、IM/IF 标 objective-misaligned）· `L2` GNNDelete n.s. 对冲· `L7` arxiv pilot scope· `L8` 460/92 笔误· `L9` verdict label 加"描述性非统计证明"一句。
- **等实验回填**：`L3` hop caveat ←**E2**· `L4` ΔF_noise anchor footnote ←**E3**· `L5` §5.2 wedge（重跑前标 *pending*、不下结论）←**E4** 修复后回填真数据· `L6` citeseer scope ←**E1**。

---

## 阶段 4 — 画图

| ID | 任务 | 依赖 | 状态 |
|---|---|---|---|
| **F1** | **方法 / pipeline 示意图**：一张步骤图 / 机制图（≠ 结果图） | 独立 | ☐ |
| **F2** | **收敛图生成器分叉**：`test1.py` vs `scripts/plot_neurips_figures.py`，删一个、重生结果图 | 独立 | ☐ |
| **F3** | **Supp 图**：A3 alpha-synergy 图（`plot_alpha_synergy`）+ A5 ratio-elasticity 图（`plot_ratio_elasticity`）；hop-decay 图重生 | A3 / A5 / E2 | ☐ |

---

## 链接索引

- 当前状态 / 勾选：[`PROGRESS.md`](PROGRESS.md)（§3 是 live 勾选权威）
- 配置矩阵监督：[`config_inventory.html`](config_inventory.html) · 数据 [`config_inventory.csv`](config_inventory.csv)
- 硬伤映射：[`PAPER_LIABILITIES_MAP.md`](PAPER_LIABILITIES_MAP.md)（L1–L9 + overleaf 行号）· `PROGRESS.md §2`（C1–C5）
- 实测瓶颈：[`self/limitations.md`](../limitations.md)（L1–L8）
- ablation 设计原典：`experiments/configs/A3_alpha_sweep_SPEC.md` · `A5_README.md` · `SANITY_GRAPHREVOKER.md`
- 跨架构 idea：`self/idea_cross_arch_consensus.md`
- 重投蓝本（**这轮不碰**）：reframe commit `565aaf6` + 强版机制 §7

---

## Changelog

- **2026-06-27** 建档。把 PROGRESS §2/§3 + limitations + PAPER_LIABILITIES_MAP + 配置矩阵收敛成 实验/ablation/写作/画图 四阶段；新增阶段 0 排序图与 E4/E2/E1/E3 依赖链；配套 `config_inventory.{csv,html}` 监督看板（`scripts/dashboard/` 生成器待确认是否落地）。
- **2026-06-27（晚）** E4 决策定为 **修 + 重跑**（用户明确：不 drop、不 caveat，不报也不洗坏数据）；同步落到 PROGRESS §2 C5 / §3 P1 + 本表阶段 0/1/3 + 重生 `progress.html`。
