# WORKPLAN — 操作中枢 + 阶段计划（实验 / ablation / 写作 / 画图）

> Last updated: 2026-06-27
> Role: **当前阶段的唯一操作中枢**（2026-06-27 起取代 `PROGRESS.md`）。现状快照 + 硬伤 + 方向 + 按工作流阶段拆的任务计划，全在这一份。
> 看板 `progress.html` 由 `scripts/dashboard/refresh.py` 从本文件生成（§0 现状 + §1 快照 + §5–§8 四阶段 kanban）；改完本文件跑一次 refresh（或靠 pre-commit hook 自动重生）。**单一真相是这份 markdown。**
> 维护规则：只放 **状态 / 原因 / 任务 / 链接**，不复制其他文档内容（`config_inventory.html` 管 cell 级进度、`PAPER_LIABILITIES_MAP.md` 管 overleaf 行号、`limitations.md` 管实测瓶颈——这里只链接）。
>
> 🔒 **thesis 锁死**：投出去的 contribution = *systematic audit + extreme heterogeneity + Vulnerability Fingerprint*。这轮（NeurIPS rebuttal 备战）只在框架内补证 + 写作；"结构杠杆主轴" reframe(`565aaf6`) 留给"不中→重投"，**rebuttal 里做 = 自投降**。
>
> 图例：☐ 未做 · ◐ 进行中 · ✅ 完成 · ★ 需 GPU（AutoDL 镜像 `gnn_20`，可随时租）

---

## 0. 一句话现状

已投 NeurIPS、在等审稿、**rebuttal 还远 = 完善期**。回流数据 `degree ≥ IM/IF`（raw-F1 和 retrain gap 都是）——但**这没证伪贡献**：投出去的 thesis 本就是 *systematic audit + extreme heterogeneity + fingerprint*，不是"IM/IF 最强"。这轮的活 = **thesis 内**把主指标 raw-F1 换成 **retrain gap**（它把异质性讲得最干净：GNNDelete 崩 16%、partition/IF 鲁棒）、IM/IF 降为诊断轴——**不重写故事**（那是重投 / `565aaf6` 的事）。环境已厘清（H→E 已重指、本地 CPU 就绪、GPU 走 AutoDL 镜像 `gnn_20`、**可随时租服务器**）。

---

## 1. 状态快照

| 维度 | 状态 | 原因 / 细节 | 权威出处 |
|---|---|---|---|
| **数据** | 🟢 cora 全+双备份 / arxiv 6-cell pilot（已核实） | cora 460（`ablating/` 460 + `4090/` 360 两份）+ D:/F: 备份，5 seed 无缺口。arxiv=6 cell（GIF/GNNDelete×{random,tracin,im}，seed42，r0.01）——**服务器权威 journal 核实只完成 6、全在本地、nothing stranded**；2 空壳（GIF_hybrid/GraphEraser）=中断未完成，T2/T3/r0.05/degree/pagerank 从没跑 | server journal 存档 `results/_journal/archive/`；`_phase_b_aggregate.csv` |
| **环境** | 🟡 本地分析就绪 / 本地 GPU 不可用 | H→E 已重指；conda `gnn` 在 `E:/conda_package/envs/gnn/python.exe`（torch 2.2.1+cu121/Py3.8），CPU 栈全 import OK。**本地 GPU 死**：RTX 5070=sm_120(Blackwell)，此 torch 只到 sm_90 → CUDA kernel 全崩；按 requirements.txt 重建救不了。GPU 环境**封存在 AutoDL 镜像 `gnn_20`**，随起随用、可随时租 → 本地只做非实验 | 本 session 实测 + 记忆 `project_stack_reproducibility_constraint` |
| **数据安全** | 🟢 已多处备份 | 服务器有完整原件；本地备份 `D:\backups\OpenGU_GULib\2026-06-15\` + `F:\…`（2482 文件校验通过） | 备份 MANIFEST |
| **代码** | 🟡 dashboard 已提交 / paper 改动待提交 | 看板 + WORKPLAN + inventory 已提交（`44f7988`）；paper 7 章节 + CSV + 图改动仍在工作树，未跟踪 `test1.py`/`arxiv_pilot_table.tex`；canonical 分支 `release/phase-b-fixes` | git |
| **L8 修复** | 🟢 代码已修 / 🔴 数据仍坏 | 写回逻辑 `d674f62` 已在 HEAD（**不用合分支**）；数据坏是服务器 **stale `.pyc`** → 只需清缓存重跑（见 E2） | `limitations.md` L8 |
| **paper** | 🟡 thesis 站得住 / 有 rebuttal 硬伤 | contribution = audit + 异质性 + fingerprint，**未被 degree 证伪**（§2 C1）。这轮 = 换主指标 retrain gap + 压异质性，thesis 内不改写。两道必答题：① vs degree ② citeseer/arxiv scope（L6/L7，需租服务器补）。§2 数字硬伤待 caveat | 记忆 `paper-correctness-liabilities`；§2/§3 |
| **大方向** | 🟡 已厘清 | **不是"rebuttal vs 重投"二选一**：先备 rebuttal（thesis 内，§3）；不中再重投+reframe（`565aaf6`）。别在 rebuttal 里改 thesis | §3 |

---

## 2. 硬伤 C1–C5（必须处理；overleaf 行号见 `PAPER_LIABILITIES_MAP.md`）

1. **C1 — 指标选错，非贡献被证伪**：`degree ≥ IM/IF` 在 **raw-F1**（degree +1.85 > im +1.19 > tracin −0.31）**和 retrain gap**（全局 degree .0286 > im .0233；逐方法只有 GNNDelete 有真 gap、degree .158 第一、IF 家族≈0）**都成立**。但 thesis 本是 *audit + 异质性*，不是"IM/IF 最强" → **degree 赢不证伪它**。rebuttal 内：换主指标 retrain gap、异质性当头条、IM/IF 降诊断轴；TracIn 最弱本身是 finding。唯一可能翻盘的 IM/IF niche：GIF/IDEA gap 现≈0 且 L8 污染 → **E2** 是唯一能验出真 niche 的实验。→ 记忆 `paper-contribution-falsified`。
2. **C2 — GNNDelete 在 n=5 不显著**（sd≫mean）。"最脆弱方法"措辞需带 n.s. 对冲 → W3-L2 / A7。
3. **C3 — §A.4 hop-decay 被 L8 污染且 CSV 4 列全空**（GIF≡IDEA 逐位相同）→ E2/E6/W3-L3。
4. **C4 — ΔF_noise(k=5) 磁盘上 5/6 方法 `f1_before`=null**，"F1 反升"暂不可复现 → E3/W3-L4。
5. **C5 — GraphRevoker 整 method 退化**：`perf_before` 所有 cell 退化（0.50–0.58，vs 其它 0.77–0.87），根因 `e3bbd54` 未修完聚合器 bug（`opt_dataset.py:17` IndexError）。**决策已定（2026-06-27）：修聚合器 + 整 method 重跑（E4），不 drop、不 caveat**——不报、也不洗坏数据；重跑前 §5.2 GR×GAT wedge 标 *pending re-run*、不下机制结论，方法保留在 6-method audit。→ 记忆 `project_graphrevoker_dispatcher_history`、`feedback-fix-dont-drop-broken-data`。

---

## 3. 方向：rebuttal-prep（这轮）→ 重投（仅当不中）

**已投 NeurIPS，在等审稿，rebuttal 还远 = 完善期。** 顺序是先 rebuttal、不中再重投；GPU 不是约束（可随时租）。

- **这轮 rebuttal（thesis 锁死，不改框架）**：换主指标 raw-F1 → **retrain gap**；头条压 **extreme heterogeneity**（GNNDelete 崩 16% / partition·IF 鲁棒）；IM/IF 降为 **fingerprint 诊断轴**；备两道必答题（① vs degree ② citeseer/arxiv scope）。
- **下一站（仅当不中 → 重投）**：才做"结构杠杆主轴、influence 失配"叙事转换（`565aaf6` 蓝本 + 强版机制 §7）。**这轮做它 = 自投降。**

---

## 4. 排序 / 依赖（章法 —— 先看这张，别乱序开工）

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

**本轮主线**：`W1 指标切换 retrain gap → W2 必答题 → W3 纯 prose 那几条(L1/L2/L7/L8/L9) → 租服务器跑 E1/E2/E3/E4(含 GraphRevoker 修复) → 回填 W3 剩余(L3/L4/L5/L6) + F3`。

---

## 5. 实验（主矩阵补证 / 关硬伤）★ 全部需 GPU

> 目标：把 paper 已写但磁盘撑不住的数字补干净。**不是新故事，是给 thesis 补证。** 进度数字源 = `config_inventory.html`。

| ID | 任务 | config / 脚本 | 规模·耗时 | 关 | 状态 |
|---|---|---|---|---|---|
| **E1** ★ | **跑干净 citeseer**（堵 scope 漏洞，最高优先） | `A5_citeseer_r0.05.yaml` | 6×3×5=90 cell, ~1h | L6 / C-scope | ☐ 0/90 |
| **E2** ★ | **L8 redo**：清 `__pycache__/*.pyc` + 重跑 GIF/IDEA collateral（代码已修 `d674f62`，三 cache 别动） | `scripts/redo_collateral_if_family.py` `phase_b_cora_{gcn,gat}.yaml` | GIF+IDEA×6×5×2=120 cell | C3 / L8 | ☐ |
| **E3** ★ | **修 ΔF_noise anchor**：重跑 k=5 把 `f1_before` 持久化（或注明 anchor 缺失） | `experiments/baseline_k5/fill_missing_cora.py` | 4×5=20 run, ~15min | C4 / L4 | ☐ |
| **E4** ★ | **GraphRevoker 修复**（决策已定 = **修，不 drop / 不 caveat**）：修聚合器 `opt_dataset.py:17` IndexError（`e3bbd54` 未完成）→ 清损坏 `data/GraphRevoker/cora/` .pt → 整 method 重跑 | `phase_b_cora_{gcn,gat}.yaml` + 聚合器修复 | 整 method 重跑 | C5 / L5 | ☐ |
| **E5** ★ | **arxiv 补量**：补 T2/T3 seed 或扩 6 method，关"只是 pilot" | `phase_b_arxiv_T2_seed212.yaml` `..._T3_seed722.yaml` | 18 cell/seed | L7 | ◐ T1 6/18 |
| **E6** ★ | **hop 列灌进 aggregate CSV**：扩 aggregator 读 `collateral.json::hop_decay`（**依赖 E2**） | aggregator 扩展 | 4 列 ×460 行 | C3 | ☐ 0/460 |

**坑提醒**：E1 的 2 月 citeseer 数据在 `_archive_20260506/` 是**污染数据，不能引**；改 GNN 架构维度才需清 `data/{Method}/`，E1–E6 不改架构故不用清。

---

## 6. Ablation

> 目标：把"现象沿某个轴怎么变"讲清楚。**多数有 decision gate**（先验证主矩阵 fingerprint 再决定值不值得跑），别无脑全开。

| ID | 任务 | config | 规模 | gate / 备注 | 状态 |
|---|---|---|---|---|---|
| **A3** ★ | **alpha-sweep**：hybrid_alpha {0,.25,.5,.75,1}×{GCN,GAT}×cora r0.05 | `A3_cora_{GCN,GAT}_alpha{0.00,0.25,0.75,1.00}.yaml` | 有效新增 ~180 cell（α=0≡im, α=1≡tracin） | **gate**：主矩阵 fingerprint 出来后，若 MEGU/IDEA 有非平凡坐标才值得跑。⚠ IM 整体打不过 degree → 价值有限 | ☐ 0/200 |
| **A5** ★ | **ratio-sweep**：r∈{0.01,0.10,0.20} cora GCN（+citeseer 见 E1） | `A5_ratio_{0.01,0.10,0.20}.yaml` | 90 cell/ratio | r0.01 **已完成**；r0.10/0.20 待跑。⚠ r0.20 可能崩 GraphEraser（空 shard），先 sanity | ◐ 90/450 |
| **A6** ★ | **新 backbone / 跨架构共识**：GIN 已有 config；加 1 个**非-MP**(Cheb/APPNP) | `A6_cora_gin_r0.05.yaml` + 新建 | 75 cell/backbone | → `idea_cross_arch_consensus.md`。P2 加分 | ☐ 0/75 |
| **A7** ★ | **GNNDelete +seed**（n.s.→显著）或 reframe 成 volume-driven | 扩 `phase_b_cora_*` seeds | +N seed | 关 C2（n=5 sd≫mean）。P2 | ☐ |
| **A8** | **RR-set IM / RR-IF-Hybrid**（统一 IMM 框架，IF 作 bicriteria） | 新算法 | ~2-3 天实现 | limitations L6-(C)，**ICLR-tier follow-up**；rebuttal 不做 | ☐ option |

**Aggregator 待建**：`scripts/plot_supp_figures.py::plot_alpha_synergy`（A3）、`::plot_ratio_elasticity`（A5）—— 见 F3。

---

## 7. 写作（thesis 锁死，框架内）

> 目标：把 thesis 讲法对齐到现有数据。多数**纯 prose、现在就能做**；少数等阶段实验回填。

| ID | 任务 | 关 | 依赖 | 状态 |
|---|---|---|---|---|
| **W1** | **指标切换（本轮核心）**：主指标 raw-F1 → **retrain gap**；头条压 *extreme heterogeneity*（GNNDelete 崩~16% / partition·IF 鲁棒）；IM/IF 降为 fingerprint 诊断轴 | C1 | — | ☐ 纯 prose |
| **W2** | **两道 rebuttal 必答题**：① vs degree —"approximation-gap 上 degree/IM 都强，contribution 是异质性、非某 selector 最强"；② citeseer/arxiv scope | C1 / L6 / L7 | ②待 E1 | ☐ |
| **W3** | **硬伤逐条 caveat**（对照 `PAPER_LIABILITIES_MAP.md` overleaf 行号） | L1–L9 / C2–C4 | 见下 | ☐ |
| **W4** | **paper 整理/融合 + 重查表格**：多版收敛（云端基底 + 并入 reframe 框架 + 落 C1–C6 + 清弃用如 `arxiv_pilot_table.tex`），逐表 check | — | W1–W3 | ☐ |
| **W5** | **术语审计** "MIA" → "update-detection AUC"（全文） | — | — | ☐ 纯 prose |
| **W6** | **review collection**：汇总 评审/导师/AI 修改意见（起点 `report/advisor_report_2026-06-16.html`） | — | — | ☐ |
| **W7** | **读未读论文**：GraphRevoker / MEGU / UTU 等 → related work + 反防审稿人引用 | — | — | ☐ |
| **W8** | **Supplementary 整理**：appendix（hop §A.4 / 460 行说明 / 诊断 suite 定义）成形 | L8 / C3 | A.4 待 E2 | ☐ |

**W3 拆解（按能否现在做）**：
- **现在就能改（纯 prose）**：`L1` abstract selector reframe（列全 6 selector、degree/PageRank 主导、IM/IF 标 objective-misaligned）· `L2` GNNDelete n.s. 对冲· `L7` arxiv pilot scope· `L8` 460/92 笔误· `L9` verdict label 加"描述性非统计证明"一句。
- **等实验回填**：`L3` hop caveat ←**E2**· `L4` ΔF_noise anchor footnote ←**E3**· `L5` §5.2 wedge（重跑前标 *pending*、不下结论）←**E4** 修复后回填真数据· `L6` citeseer scope ←**E1**。

---

## 8. 画图

| ID | 任务 | 依赖 | 状态 |
|---|---|---|---|
| **F1** | **方法 / pipeline 示意图**：一张步骤图 / 机制图（≠ 结果图） | 独立 | ☐ |
| **F2** | **收敛图生成器分叉**：`test1.py` vs `scripts/plot_neurips_figures.py`，删一个、重生结果图 | 独立 | ☐ |
| **F3** | **Supp 图**：A3 alpha-synergy 图 + A5 ratio-elasticity 图；hop-decay 图重生 | A3 / A5 / E2 | ☐ |

---

## 9. 链接索引

- 配置矩阵监督：[`config_inventory.html`](config_inventory.html) · 数据 [`config_inventory.csv`](config_inventory.csv)
- 硬伤映射：[`PAPER_LIABILITIES_MAP.md`](PAPER_LIABILITIES_MAP.md)（L1–L9 + overleaf 行号）
- 实测瓶颈：[`self/limitations.md`](../limitations.md)（L1–L8）
- ablation 设计原典：`experiments/configs/A3_alpha_sweep_SPEC.md` · `A5_README.md` · `SANITY_GRAPHREVOKER.md`
- 跨架构 idea：`self/idea_cross_arch_consensus.md`
- 历史覆盖矩阵 + bug 档案（冻结 2026-05-07）：[`EXPERIMENT_DASHBOARD.md`](EXPERIMENT_DASHBOARD.md)
- 旧状态中枢（已并入本文件）：[`PROGRESS.md`](PROGRESS.md)
- 重投蓝本（**这轮不碰**）：reframe commit `565aaf6` + 强版机制 §7

---

## 10. Changelog

- **2026-06-27** 建档（实验/ablation/写作/画图 四阶段，收敛 PROGRESS §2/§3 + limitations + PAPER_LIABILITIES_MAP + 配置矩阵）；配套 `config_inventory.{csv,html}` 监督看板。
- **2026-06-27（晚）** E4 决策定为 **修 + 重跑**（不 drop / 不 caveat）；并 **升级为唯一操作中枢**：折入 PROGRESS §0/§1/§2/§4（现状/快照/硬伤/方向），`refresh.py` 重指到本文件生成 `progress.html`（看板列改为四阶段），`PROGRESS.md` 退成指针。
