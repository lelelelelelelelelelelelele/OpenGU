---
tags: [progress/phase, status/frozen, diagnosis]
phase: "2026-06 Resume Diagnosis"
date-range: 2026-06-15 → (进行中)
status: superseded-snapshot
created: 2026-06-16
up: "[[_Home]]"
---

# 2026-06 Resume Diagnosis — 全面状态整理

> **SUPERSEDED SNAPSHOT（2026-07-20）**：本文件保留 2026-06 诊断过程，不再表示当前状态。GraphRevoker 代码与远端四策略 E4 已通过，本地 evidence archive 待闭环；当前结论见 `self/dashboard/WORKPLAN.md` 与 `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`。

> **2026-07-22 归档更新**：旧活动分支已由正式蓝本 [`RESUBMISSION_BLUEPRINT.md`](../../paper/RESUBMISSION_BLUEPRINT.md) 取代；精确历史内容改由 `archive/paper-alignment-20260507` 和 `archive/paper-alignment-wip-20260507` 恢复。下文出现的旧分支名只保留为历史叙述。

> 范围: 休整一个月后回流数据 + 找回旧记忆 + 逐项核查后的**完整诊断**。回答"现在到底是什么处境、paper 该变成什么、怎么走"。
> 配对: 操作 TODO → [PROGRESS（外部）](../../../self/dashboard/PROGRESS.md)；冲刺历史 → [2026-05_NeurIPS-Push](2026-05_NeurIPS-Push.md)；当前汇报 → [current-status-report.html](current-status-report.html)。

> **2026-07-01 更新**：本文件是 2026-06-15 的诊断快照，保留“数据复盘暴露原 selector 叙事风险”的判断；但“直接重投 / 大幅 reframe”的路线判断已经被当前 WORKPLAN 与 0701 汇报收窄。当前口径是：NeurIPS 已提交，短期按 rebuttal-prep 处理；主 thesis 收束为 systematic audit + extreme heterogeneity + Vulnerability Fingerprint；GraphRevoker 与 proper-TracIn refresh 作为证据链修复任务。

---

## 0. 一句话

**原 paper 的中心卖点（"我们造了 informed selector，能攻破 GU、且优于 baseline"）已被干净数据证伪。** 这不是"结论不够显著"的小修，而是**需要换一篇 paper 的骨架**——而且诚实版骨架 2026-05-07 就草拟过（`565aaf6`，当时被搁置）。叠加 5 类相互关联的硬伤 + 覆盖缺口。

---

## 1. 中心问题：这已经是"另一篇 paper"

| | 原 paper（当前 working tree）| 干净数据实际支持的 |
|---|---|---|
| 卖点 | informed selector（TracIn/IM/Hybrid）放大近似误差、攻破 GU | **degree（免费结构启发式）通吃；TracIn 平均比 random 还差** |
| selector 排序 | informed > baseline | **全局 degree +1.85 > pagerank +1.53 > im +1.19 > hybrid +0.21 > tracin −0.31**；逐方法 degree≥im≥tracin |
| 诚实落点 | — | **"结构中心性是主攻击轴；influence 信号与 unlearning 脆弱性 objective-misaligned"**（诊断/负结果框架）|

→ 没有 prose 能救"5 行 baseline 打过你的方法"。诚实版已半写好：§5.2 alignment 小节（r≈0.24）+ FIG-5 已在当前 paper；更狠的 abstract/intro 版本在 `565aaf6`。

---

## 2. 问题全清单（4 类）

### A. paper 宣称 vs 干净数据：矛盾/不可支持

| ID | paper 现状 | 数据实况 | 处理 |
|---|---|---|---|
| **C1** | informed selector 是贡献 | degree 通吃、TracIn 为负（已核 CSV）| reframe（§4）|
| **C2** | GNNDelete "最大 collapse ≈13% F1" | n=5 不显著（sd 5-10 ≫ mean）| 改用 **retrain gap**（≈12%，单调干净）领头，不用噪声 F1 |
| **C3** | §A.4 hop-decay 数字（GIF/IDEA ~7% 等）| L8 bug 污染（GIF≡IDEA 逐位相同）+ CSV 4 列全空；**代码已修(`d674f62`)、数据因 stale `.pyc` 仍坏** | 清 `.pyc`+重跑 IF-family collateral；先加 caveat |
| **C4** | "Shard Protection：random 让 F1 升 6-15%" | 磁盘 5/6 方法 `f1_before`=null，**不可复现** | 重跑 k=5 补 anchor，或改定性表述 |
| **C5** | GraphRevoker 是第 6 个 method；§5.2 拿 GR×GAT 当 mechanism wedge | **整 method 退化**（perf_before 0.50-0.58 vs 0.77-0.87）+ 聚合器 bug 未修完(`e3bbd54` "REMAINING BLOCKER") | **修聚合器+整 method 重跑；重跑前 GraphRevoker 相关结论 pending，不下机制结论** |
| **C6** | abstract 写 "Cora, **Citeseer**, ogbn-arxiv" | citeseer 只有 2 月 pre-fix 数据（不能引）；干净版 yaml 现成但**没跑** | 跑 `A5_citeseer`(~1h) 或 abstract 改成 Cora+arxiv |

### B. 覆盖 / 规模缺口（reviewer 攻击面）

- **只有 1 个干净数据集 = cora**。arxiv 是 pilot（seed42、2 method、GraphEraser 空）；citeseer 没干净版 → "single-dataset" 质疑成立。
- **当前只有 5 个可直接使用的 method**（GraphRevoker 退化，见 C5）；GraphRevoker 不丢，修复重跑后回填 6-method audit。
- **隐私 metric 是非标准的 "update-detection AUC"**（不是 shadow-model MIA）——reviewer 软肋；L2-surrogate transferability 只有 L2-direct，没真做。
- k=5 noise floor 缺 5/12 cell（L7）。

### C. 基建 / 流程

- **环境待重建**（盘迁成 E:，可恢复，`../requirements.txt`）；本地暂时跑不了，所有 `H:` 硬编码失效。
- **一个月整合工作未提交**（working tree 脏；服务器有数据原件，丢失风险低）。
- 图生成器分叉（`test1.py` vs `scripts/plot_neurips_figures.py`，FIG-2 语义不一）。

### D. 找回的旧上下文（2026-06-15 从孤立的 H 盘记忆库迁回）

- **reframe 早提过**：`paper/alignment-experiment` 分支 `565aaf6`（access-tier-inverted + objective-misalignment 的 abstract/intro），你当时**没采纳、切回去跑 arxiv 想看会不会反转 degree 优势**。现在 arxiv pilot 回来仍 degree-主导 → **reframe 依然 honest**。
- **5 条你给过的 feedback**（必须遵守）：① 不在 paper 写 bug-fix journey（post-fix 就是 the data）② 效应≈0 也是 finding ③ shard 负 gap 别当 finding（k=5 cover）④ 新脚本先确认 ⑤ ScoreCache key。
- GraphRevoker dispatcher 史（2026-05-05 前全是 GraphEraser 别名）；IDEA MIA 不是 bug（~0.55）。

---

## 3. 诚实版 paper 应该长啥样

1. **中心论点改成"倒置 + 失配"**：access tier 不预测攻击成功（本段旧数字仅为历史快照；GraphRevoker 重跑前不用于机制结论）；机制是 objective-misalignment。重投时使用 [`RESUBMISSION_BLUEPRINT.md`](../../paper/RESUBMISSION_BLUEPRINT.md)（**不 cherry-pick**；从届时 main 手动重写 + 回填 accepted matrix 的真实数字）。
2. **GNNDelete 用 gap 领头**（绕开 C2，且跟 degree 分解路径一脉相承）。
3. **GraphRevoker 标记 pending，修复并重跑**；重跑前删除或冻结 §5.2 GR×GAT wedge，不把坏数据写成机制结论（C5）。
4. **修/caveat 不可支持的数字**：hop-decay（C3）、ΔF_noise（C4）、citeseer（C6）。
5. **正向贡献（核心，把"很水"翻过来）= 识别正确的攻击 target = $\mathcal{U}$ 的近似误差（gap），证 degree 只是其廉价代理、IF/IM 瞄错 object，并试 U-aware selector**（[research_path §7（外部）](../../../self/research_path_degree_severity_decomposition.md)）。IF/IM 成探针、degree 成被识别的代理、"正确目标"成 hero；两种结局都可发（U-aware > degree = 新方法；≈ degree = 廉价近最优代理）。
6. **不写 bug-fix journey**（feedback ①）；把 MEGU/IDEA 的小效应当 finding 写（feedback ②）。

---

## 4. 历史判断 + 2026-07-01 收窄

**历史判断（2026-06-15）：倾向重投（reframe），不是 rebuttal。** 当时的理由是：原 selector-centered 贡献被干净数据削弱；本地环境不可跑；补充实验尚未完成。

**当前收窄（2026-07-01）：不把它作为当前决策。** 现在 NeurIPS 已提交、等待 review，短期不应把论文改成另一篇。更稳的路径是保留已投 thesis 的外壳，把主线收束到 systematic audit、extreme heterogeneity、Vulnerability Fingerprint；`565aaf6` 一类更激进 reframe 保留为不中后的重投蓝本。

**路线（环境重建是总闸）：**
- **P0**：备份(已)+ 提交 + 大方向决策。
- **P1（重建环境后）**：L8 清 `.pyc`+重跑 IF-family；GraphRevoker 修复+整 method 重跑；跑干净 citeseer(~1h)；修 ΔF_noise anchor；hop 列灌进 CSV；图生成器收敛。
- **P2（仅重投时启用）**：按蓝本重写 abstract/intro（reframe）；GNNDelete 加 seed 或 gap-reframe；arxiv 全矩阵；degree 分解二级结论。

> 全部 TODO 勾选见 [PROGRESS §3（外部）](../../../self/dashboard/PROGRESS.md)。

---

## 5. 一句话总结

2026-06 的核心价值不是最终路线，而是指出：原 selector-centered 叙事不稳，且 GraphRevoker、TracIn/Hybrid、hop-decay、scope 等证据链需要清理。2026-07-01 后的当前任务不是立刻换骨架，而是先修 GraphRevoker、刷新 proper-TracIn、补 clean scope，让现有 thesis 以 audit + heterogeneity + fingerprint 的方式站稳。
