# PROGRESS — Resume Phase（2026-06 →）

> Last updated: 2026-06-20
> Role: **当前阶段的操作中枢**。已投 NeurIPS → 完善期 / rebuttal 备战（不中再重投）。
> 与 `EXPERIMENT_DASHBOARD.md` 的关系：那份**冻结在 2026-05-07**（围绕已结束的 NeurIPS 4 天 push），现降级为"历史覆盖矩阵 + bug 档案"；**当前状态以本文件为准**。
> 维护规则：本文件只放 **状态 / 原因 / 勾选 / 链接**，不复制其他文档内容（遵守 `CLAUDE.md` 的 no-duplication 铁律）。每改一项勾选就更新 Last updated。

---

## 0. 一句话现状

已投 NeurIPS、在等审稿、**rebuttal 还远 = 完善期**。回流数据 `degree ≥ IM/IF`（raw-F1 和 retrain gap 都是）——但**这没证伪贡献**：投出去的 thesis 本就是 *systematic audit + extreme heterogeneity + fingerprint*，不是"IM/IF 最强"。这轮的活 = **thesis 内**把主指标 raw-F1 换成 **retrain gap**（它把异质性讲得最干净：GNNDelete 崩 16%、partition/IF 鲁棒）、IM/IF 降为诊断轴——**不重写故事**（那是重投 / `565aaf6` 的事）。环境已厘清（H→E 已重指、本地 CPU 就绪、GPU 走 AutoDL 镜像 `gnn_20`、**可随时租服务器**）。

---

## 1. 现状快照（状态 + 为什么）

| 维度 | 状态 | 原因 / 细节 | 权威出处 |
|---|---|---|---|
| **数据** | 🟢 cora 全+双备份 / arxiv 6-cell pilot（已核实） | cora 460（`ablating/` 460 + `4090/` 360 两份）+ D:/F: 备份，5 seed 无缺口。arxiv=6 cell（GIF/GNNDelete×{random,tracin,im}，seed42，r0.01）——**服务器权威 journal 核实只完成 6、全在本地、nothing stranded**；2 空壳（GIF_hybrid/GraphEraser）=中断未完成，T2/T3/r0.05/degree/pagerank 从没跑。`predictions.npz` 按设计不回传（非丢，MIGRATION §1.2）| server journal 存档 `results/_journal/archive/`；`_phase_b_aggregate.csv` |
| **环境** | 🟡 本地分析就绪 / 本地 GPU 不可用 | H→E 已重指（2026-06-20，109 处/28 文件）；conda `gnn` 解释器活在 `E:/conda_package/envs/gnn/python.exe`（torch 2.2.1+cu121/Py3.8），CPU 栈全 import OK。**本地 GPU 死**：RTX 5070=sm_120(Blackwell)，此 torch 只到 sm_90，CUDA kernel 实测全崩；Py3.8 装不到支持 sm_120 的 torch，**照 requirements.txt 重建救不了**。GPU 环境**封存在 AutoDL 镜像 `gnn_20`(5-07)**，随起随用、可随时租 → 本地只做非实验 | 本 session 实测 + 记忆 `project_stack_reproducibility_constraint` |
| **数据安全** | 🟢 已多处备份 | 服务器有完整原件；本地已备份到 `D:\backups\OpenGU_GULib\2026-06-15\` + `F:\…`（2482 文件校验通过） | 备份 MANIFEST |
| **代码** | 🟡 改动未提交 | 5/7 后改动很少、可修复；改过 7 个 paper 章节 + CSV + 图，未跟踪 `test1.py`/`arxiv_pilot_table.tex`；canonical 分支 `release/phase-b-fixes` | — |
| **L8 修复** | 🟢 代码已修 / 🔴 数据仍坏 | 写回逻辑 `d674f62` 已在 HEAD（与 `949d0f8` 逐字相同，**不用合分支**）；数据坏是服务器 **stale `.pyc`**（run 的 `git_sha=78872fc` 已含修复但跑了旧字节码）→ 只需清缓存重跑 | `limitations.md` L8 |
| **paper** | 🟡 thesis 站得住 / 有 rebuttal 硬伤 | 投出去的 contribution = audit + 异质性 + fingerprint，**未被 degree 证伪**（见 §2 C1）。这轮 = 换主指标 retrain gap + 压异质性，thesis 内不改写。两道 rebuttal 必答题：① vs degree baseline ② citeseer/arxiv scope over-claim（L6/L7，需租服务器补）。另 §2 数字硬伤待 caveat | 记忆 `paper-correctness-liabilities`；§2/§4 |
| **大方向** | 🟡 已厘清 | **不是"rebuttal vs 重投"二选一**：已投 NeurIPS → 这轮先**备 rebuttal**（thesis 内，见 §4）；若不中再**重投+reframe**（`565aaf6`）。两条线分开，别在 rebuttal 里改 thesis | §4 |

---

## 2. 核心结论 & 必须处理的硬伤

1. **C1 — 指标选错，非贡献被证伪（重大更正 2026-06-20）**：`degree ≥ IM/IF` 在 **raw-F1**（degree +1.85 > im +1.19 > tracin −0.31）**和 retrain gap**（全局 degree .0286 > im .0233；逐方法只有 GNNDelete 有真 gap、degree .158 第一、IF 家族≈0）**都成立**。但投出去的 thesis 本是 *audit + 异质性*，不是"IM/IF 最强" → **degree 赢不证伪它**。机制：高 degree 点既是数据要害、又是局部近似最崩处，故两指标都赢。**rebuttal 内**：换主指标 retrain gap、异质性当头条（GNNDelete 崩 16% / partition·IF≈0 鲁棒）、IM/IF 降为诊断轴；TracIn 最弱（撬不动近似）本身是 finding。**"结构杠杆主轴"reframe 留给重投**（`565aaf6`）。唯一可能翻盘的 IM/IF niche：GIF/IDEA gap 现≈0 且 L8 污染 → L8-clean 重跑（P1）是唯一能验出真 niche 的实验。详 → 记忆 `paper-contribution-falsified`、`self/research_path_degree_severity_decomposition.md`。
2. **C2 — GNNDelete 在 n=5 不显著**（sd≫mean）。"最脆弱方法"措辞需带 n.s. 对冲。
3. **C3 — §A.4 hop-decay 被 L8 污染且 CSV 4 列全空**（GIF≡IDEA 逐位相同）。
4. **C4 — ΔF_noise(k=5) 磁盘上 5/6 方法 `f1_before`=null**，"F1 反升"暂不可复现。
5. **C5 — GraphRevoker 整 method 退化可疑**：`perf_before` 在所有 cell 都退化（cora_GCN_r0.05=0.583 / r0.01=0.570 / GAT=0.500，vs 其它方法 0.766~0.865）。根因=`e3bbd54` 自己标的未修完聚合器 bug（`opt_dataset.py:17` IndexError，"needs substantial work"）。后果：所有 paired ≈0 且 strategy 排序紊乱（IM/pagerank/tracin>degree 的"特例"是坏底座噪声，非真反例）；**paper §5.2 拿 GraphRevoker×GAT(perf_before=0.500) 当唯一 mechanism wedge —— 站不住**。另有 1 个 cell 因损坏分片 checkpoint（`torch.load: not a ZIP archive`）崩溃（小 transient）。**决策已定（2026-06-27）：修聚合器 + 整 method 重跑**（用户明确：不 drop、不 caveat——不报、也不洗坏数据）；重跑前 §5.2 GR×GAT wedge 标 *pending re-run*、不下机制结论，方法保留在 6-method audit。 详 → 记忆 `project_graphrevoker_dispatcher_history`。

> C3/C4 详见 `limitations.md` L7/L8 + 记忆 `paper-correctness-liabilities`；C5 详见记忆 `project_graphrevoker_dispatcher_history`。

---

## 3. TODO 框架（含 2026-06-20 收尾清单 #1–#10；★=需租服务器）

> 定位已变：不是"投稿前必补"，是 **NeurIPS rebuttal 备战**。thesis 锁死，这轮只在框架内补证 + 写作。

### P0 — 现在可做（纯写作 / 整理，不需服务器）
- [x] 备份回流数据到 D:/F:（2026-06-15）
- [x] 提交环境/数据/看板工作（2026-06-20，3 commit；`release/phase-b-fixes` 更早的写作改动仍待确认提交）
- [ ] **指标切换（这轮核心）**：主指标 raw-F1 → **retrain gap**，头条压 *extreme heterogeneity*（GNNDelete 崩 16% / partition·IF 鲁棒），IM/IF 降为 fingerprint 诊断轴 —— 纯写作，见 §2 C1 / §4
- [ ] **备两道 rebuttal 必答题**：① vs degree baseline ② citeseer/arxiv scope over-claim（话术见 §4）
- [ ] **给硬伤数字加 caveat**：§A.4 hop(C3)、GNNDelete n.s.(C2)、ΔF_noise(C4)、`A_appendix` 460/92 笔误 → 对照 [`PAPER_LIABILITIES_MAP.md`](PAPER_LIABILITIES_MAP.md) 逐条
- [ ] **paper 整理 / 融合 + 重查表格（清单#2）**：多版收敛成一份连贯稿——云端最新但仓促(打磨非照搬)/本地旧版/reframe 框架(`565aaf6`+强版机制 §7)/C1–C6；融合=云端为基底+并入 reframe+落 C1–C6+清弃用(如 `arxiv_pilot_table.tex`)；逐表 check。prose 可先搭骨架，数字等 P1 修好回填
- [ ] 术语审计 "MIA" → "update-detection AUC"（纯写作）
- [ ] **review collection（清单#4）**：汇总评审/导师/AI 给过的修改意见（起点 `report/advisor_report_2026-06-16.html`）
- [ ] **读未读论文（清单#8）**：GraphRevoker / MEGU / UTU 等 —— 备 related work + 反防审稿人引用
- [ ] **方法 / pipeline 示意图（清单#9）**：画一张步骤图 / 机制图（≠ 下面 P1 的结果图）
- [ ] **Supplementary 整理（清单#10）**：appendix（hop §A.4 / 460 行说明 / 诊断 suite 定义）成形
- [ ] 把 arxiv pilot JSON 纳入版本控制 / 并进 CSV（待确认）

### P1 — 需租服务器（rebuttal 补证；GPU 走 AutoDL 镜像 `gnn_20`，可随时租）
- [x] ~~重建 conda `gnn` + H→E 重指~~ → **已完成 2026-06-20**（解释器活在 E:；CPU 可跑；GPU 用镜像）
- [ ] ★ **跑干净 citeseer（最高优先 = 堵 scope 漏洞 / 必答题②）**：`A5_citeseer_r0.05.yaml`，6 method×{random,im,tracin}×5 seed≈180 cell，~1h。关 L6。⚠️ 2 月 citeseer 在 `_archive_20260506/` 是污染数据，不能引
- [ ] ★ **L8 redo**：清 `.pyc` + 重跑 cora GCN/GAT collateral（代码不用改；三 cache 别动）→ 干净 GIF/IDEA gap+hop。关 C3；**且是唯一能验出 IM/IF 在 IF 家族有无真 niche 的实验**（现 GIF/IDEA gap≈0 且被 L8 污染）
- [ ] ★ 把 4 个 hop 列灌进 `_phase_b_aggregate.csv`（扩 aggregator 读 `collateral.json::hop_decay`）。关 C3
- [ ] ★ 修 ΔF_noise `f1_before` null（重跑 k=5 或注明 anchor）。关 C4
- [ ] ★ **GraphRevoker 修复（C5 / 清单#1，决策已定 2026-06-27 = 修，不 drop / 不 caveat）**：修聚合器 bug（`opt_dataset.py:17` IndexError，`e3bbd54` 未完成）→ 清损坏 `data/GraphRevoker/cora/` .pt → 整 method 重跑（perf_before 现 0.50-0.58 退化）。重跑前 §5.2 GR×GAT wedge 标 *pending re-run*、不下机制结论；方法保留在 6-method audit 内
- [ ] ★ **arxiv 补量 + ssh 结果整理/review（清单#6）**：补 T2/T3 seed 或 6 method，关"scalability 只是 pilot"。服务器结果整理本 session 已起头（journal 归档 + 数据盘点）
- [ ] 收敛 figure 生成器分叉（`test1.py` vs `scripts/plot_neurips_figures.py`），删一个重生结果图

### P2 — 加分 / option（非必需）
- [ ] **新 backbone table / 跨架构共识（清单#3 + #7 a.6 cross）**：加 1 个**非-MP** backbone（Cheb/APPNP）→ `idea_cross_arch_consensus.md`
- [ ] **RR-set IM 对比（清单#5，option）**：逆-MC / RIS 式 IM vs 现 CELF。⚠️ 既然 IM 整体打不过 degree，换哪种 IM 价值有限，优先级低
- [ ] degree 分解 + 安全指数（用已有数据 + L8 干净后）→ `research_path_degree_severity_decomposition.md`
- [ ] GNNDelete 加 seed（n.s.→显著）或 reframe 成 volume 驱动。关 C2
- [ ] IDEA/MEGU 定向 selector 审计

> 清单#3 的"可视化打勾表"= 本看板 `progress.html`（`scripts/dashboard/refresh.py` 生成，已建）。citeseer 已升 P1（堵 scope 漏洞）；arxiv 全矩阵见 P1 补量。

---

## 4. 方向：rebuttal-prep（这轮）→ 重投（仅当不中）

**已投 NeurIPS，在等审稿，rebuttal 还远 = 完善期。** 此前"rebuttal vs 重投"是伪二选一——顺序是先 rebuttal，不中再重投。GPU 不是约束（可随时租服务器）。

**这轮 rebuttal（thesis 锁死，不改框架）：**
- 换主指标 raw-F1 → **retrain gap**（diagnostics suite 现成，对题，正是 abstract 说的 "approximation gap"）；
- 头条压 **extreme heterogeneity**（GNNDelete 崩 16% / partition·IF 鲁棒）；
- IM/IF 从"擂主攻击"降为 **fingerprint 诊断轴**（abstract 本就这么用）；
- 备两道必答题：**① vs degree** —— 答"approximation-gap 上 degree/IM 都强，contribution 是异质性、非某 selector 最强"；**② citeseer/arxiv scope** —— abstract 写 3 数据集，而 citeseer 无干净数据(L6)/arxiv 6-cell pilot(L7) → 租服务器补 citeseer(~1h)。

**下一站（仅当不中 → 重投）：** 才做"整个叙事转换"成"结构杠杆主轴、influence 失配"（`565aaf6` 蓝本 + 强版机制 §7）。**这轮做它 = 自投降。**

---

## 5. 链接索引（详情看这些，本文件不复制）

- 现状/环境/数据：记忆 `project-state-resume-2026-06`、`project_stack_reproducibility_constraint`
- 指标选错（非证伪）+ audit 站得住 + reframe(留重投)：记忆 `paper-contribution-falsified`（措辞已软化）、`self/research_path_degree_severity_decomposition.md`
- paper 硬伤：记忆 `paper-correctness-liabilities`、[`self/dashboard/PAPER_LIABILITIES_MAP.md`](PAPER_LIABILITIES_MAP.md)、`self/limitations.md`（L1-L8）
- 跨架构 idea：`self/idea_cross_arch_consensus.md`
- **进展库（Obsidian vault，往回看）**：`report/progress/_Home.md`（MOC 入口）→ 内含 [[Macro-Timeline]] 宏观 + [[2026-05_NeurIPS-Push]] 冲刺汇报 + [[Milestones]] + [[Findings-and-Decisions]]
- 历史覆盖矩阵 + bug 档案：`self/dashboard/EXPERIMENT_DASHBOARD.md`（冻结 2026-05-07）
- metric 定义：`self/dashboard/METRICS_CATALOG.md`
- 服务器执行：`SERVER_RUNBOOK.md`、`ARXIV_RUNBOOK.md`、`experiments/configs/README.md`

---

## 6. Changelog

- **2026-06-20（深夜）战略收口**：核实投出去的 thesis = audit/异质性（**非"IM/IF 最强"**）→ "贡献被证伪"更正为"指标选错"（C1 翻案）；实测 retrain gap 仍 `degree ≥ IM/IF`（GNNDelete 唯一真 gap 16%、IF 家族≈0+L8 污染）→ 这轮 rebuttal 走"换指标 retrain gap + 压异质性 + IM/IF 降诊断轴"，reframe 留重投；明确 timeline = 已投 NeurIPS 完善期；TODO 并入 2026-06-20 收尾清单 #1–#10。
- **2026-06-20（晚）环境/数据收口**：H→E 全仓重指（109 处/28 文件 + git-bash 残留 + settings 清死权限）；冒烟测试定位**本地 GPU 因 RTX 5070(sm_120) 不可用**、GPU 环境封存在 AutoDL 镜像 `gnn_20`；数据盘点—cora 全双备份、**arxiv=6-cell pilot 经服务器权威 journal 核实无遗漏**、`predictions.npz` 按设计不回传；完整 server journal 冻结存档 `results/_journal/archive/`；新增 `scripts/dashboard/refresh.py`→`self/dashboard/progress.html` 进度看板。
- **2026-06-20** 重验证 CSV：strategy 排序、hop 列全空、GraphRevoker perf_before 退化确认；新增 `PAPER_LIABILITIES_MAP.md` 把 C1–C9 硬伤映射到 overleaf 文件/行号。
- **2026-06-15** 建档。整合 status survey 结论：cora 满矩阵确认、C1 selector 倒置、L8 code-fixed/data-stale 定位、degree 分解路径、跨架构 idea、环境/数据更正。大方向待定。
