---
title: NeurIPS 21636 争议数字与理论主张首轮审计
date: 2026-07-24
status: initial-audit-experiment-environment-blocked
scope: Table 2/3, Figure 5, Appendix, threat model, Retrain Gap
branch: codex/docs-neurips-reviews-20260724
parent: main@ea4f34a
---

# NeurIPS 21636 争议数字与理论主张首轮审计

## 执行摘要

> [!warning] 当前判定
> 近两个月的代码修复和 provenance 工作已经提供了解题基础，但尚未让投稿中的争议数字自动变得可信。当前 paper 的 GraphRevoker 数字、全部 $\Delta F_{\mathrm{noise}}$ headline、GraphRevoker-dependent Figure 5 机制楔子，以及 “L2-surrogate is bounded above by L2-direct” 均不得继续作为已证实结论。它们应标记为 `do_not_claim`，直到新 evidence 回填或文字删除。

本轮已经确认：

- 远端 active checkout 是干净 `main@ea4f34a29f5211079e1f7a7caf5a4c296f14ff08`，但 GPU 返回 `No devices were found`，且 `/root/miniconda3/envs/gnn_20/bin/python` 缺失，formal E3/E8 gate 暂不能启动。
- `results/_phase_b_aggregate.csv` 仍包含 pre-fix GraphRevoker；抽查 `perf_before` 约为 0.47–0.55，符合已知单-shard失效特征。
- 当前 checkout 不存在 `results/baseline/k5_random/`，而 paper README 和 `scripts/plot_neurips_figures.py` 仍把它声明为 $\Delta F_{\mathrm{noise}}$ 输入。
- GraphRevoker E4 的修复与远端 40/40 已通过，但完整 post-fix 多 seed evidence 仍是 archive pending，当前不能据此补写新数字。
- Citeseer E1 的 50/50 accepted evidence 可以补 scope，但真实范围仅为 5 methods × random/IM × GCN × 5 seeds。
- E3 K5 当前为 0/60 formal cells；runner/gate contract 就绪不等于已经产生实验结果。

## 1. 状态词

| 状态 | 含义 |
|---|---|
| `candidate_keep` | 当前有可追溯输入，但仍需统一生成器、sign/unit/seed 复核 |
| `replace_from_accepted` | 旧数字失效；已有新 accepted evidence，待归档/聚合后替换 |
| `pending_formal_gate` | 必须由新的 fixed-SHA formal experiment 决定 |
| `rewrite_only` | 不需要新实验；删除、降级或澄清即可 |
| `do_not_claim` | 当前不得进入论文、rebuttal 或图表结论 |

## 2. 争议数字账本

| ID | Paper 位置 | 当前显示 | 当前来源/生成器 | 审计结果 | 状态与动作 |
|---|---|---|---|---|---|
| N01 | `sec/5_results.tex:54`, Table 2, GraphRevoker/GCN attack columns | DG `+0.7`, PR `+1.5`, IM `+1.0`, HY `+0.2`, TC `+0.7` pp | 未在 table 内记录 generator；当前 aggregate 的 GraphRevoker 是 pre-fix | 与 Appendix N03 不一致；current aggregate baseline invalid | `do_not_claim`; 从 post-fix E4 重算 random/DG/PR/IM；HY/TC 等 proper-TracIn outcome |
| N02 | `sec/5_results.tex:55`, Table 2, GraphRevoker/GAT attack columns | DG `+2.6`, PR `+0.7`, IM `+1.6`, HY `+3.6`, TC `+3.6` pp | current aggregate + 历史生成链 | 与 Appendix N04 不一致；GraphRevoker×GAT mechanism wedge 依赖旧坏数据 | `do_not_claim`; E4 只能替换 random/DG/PR/IM，HY/TC 仍未正式补齐 |
| N03 | `sec/A_appendix.tex:174`, GraphRevoker/GCN | `+0.11±0.85`, `+0.33±0.84`, `+0.19±0.89`, `+0.07±0.87`, `−0.04±1.09` pp | Appendix 未绑定 manifest；文字仍提 dispatcher fix | 与 N01 不一致；来源身份不足 | `do_not_claim`; 不从旧 aggregate 重新生成 |
| N04 | `sec/A_appendix.tex:201`, GraphRevoker/GAT | `+1.44±1.23`, `+1.29±1.05`, `+1.25±1.45`, `+1.37±1.74`, `+0.22±1.99` pp | Appendix 未绑定 manifest | 与 N02 不一致；旧 GraphRevoker invalid | `do_not_claim`; 待 E4 archive 与 proper-TracIn GU outcome |
| N05 | `sec/5_results.tex:54–55,356`, GraphRevoker Gap/AUC | GCN Gap `−0.4`, AUC `0.81`; GAT Gap `−1.2`, AUC `0.79`; Table 3 `+1.0` paired effect | current aggregate 包含异常 `perf_before`; 表间 sign/metric 描述不统一 | reviewer 已指出跨表不一致；旧 collateral path invalid | `do_not_claim`; 从 post-fix `collateral.json` 与 accepted predictions 统一重算 |
| N06 | `sec/5_results.tex:52–67,244–294`, 全部 $\Delta F_{\mathrm{noise}}$ | `−19.3`、`−16.9`、`−11.9`、`−9.6` 等 12 个 method×backbone 值 | 预期 `results/baseline/k5_random/.../baseline_averaged_k5.json`; 当前目录缺失；历史 5/6 methods `f1_before=null` | 当前无法从工作树重生；负值被解释成 F1 大幅提升 | `do_not_claim`, `pending_formal_gate`; E3 one-cell gate→同 SHA 60-cell matrix |
| N07 | `sec/5_results.tex:157–215`, Figure 5 alignment | Pearson/Spearman、strategy means、GraphRevoker×GAT wedge | `scripts/plot_neurips_figures.py` 读取 `_phase_b_aggregate.csv` 与 selection artifacts | current aggregate 含 invalid GraphRevoker；F5 仍 blocked | `do_not_claim` 当前成品；导入 E4 或显式排除 GraphRevoker后重生 |
| N08 | `sec/5_results.tex:232–236`, ogbn-arxiv scope | “3 seeds… final Phase B.2 refresh will report” | 磁盘实际只有 seed42、GCN、2 methods × 3 selectors pilot | 论文把计划写成结果范围 | `rewrite_only`; 改为 single-seed qualitative pilot，不等待虚构 refresh |
| N09 | `sec/5_results.tex:58–67`, non-GraphRevoker paired attack effects | Table 内多个 DG/PR/IM/HY/TC mean | `_phase_b_aggregate.csv::paired_dF_pct`, same-seed random pairing | 多数可追溯，但主表未给 std，且 generator/rounding 未登记 | `candidate_keep`; ledger 第二阶段补 N、std、unit、seed set、generator hash |
| N10 | Citeseer scope | 当前主文声称 Citeseer evaluation，但可见结果不足 | `docs/citeseer_e1_stable_ACCEPTANCE_REPORT.md` | 新 evidence 是 50/50 accepted，但仅 stable scope | `replace_from_accepted`; 只写 5 methods × random/IM × GCN × 5 seeds |

## 3. 理论主张账本

| ID | 主张 | 当前证据 | 判定 | 最小动作 |
|---|---|---|---|---|
| C01 | `L2-surrogate is bounded above by L2-direct` | 没有形式证明；E7 surrogate-transfer GU outcome 未完成 | `do_not_claim` | 改为 “L2-direct white-box reference setting”; transfer 是否低于 direct 作为待测经验问题 |
| C02 | GIF 是 degree-aligned | 当前 Cora paired effect 与 concordance 支持 degree-aligned reading | `candidate_keep` | Conclusion 删除 “weakly TracIn-aligned”，等待 final ledger 数字 |
| C03 | Shard Protection / architectural immunity | 两个 partition methods、Cora为主；K5 anchor 不可重生；GraphRevoker旧数失效 | `do_not_claim` 作为普遍规律 | 改为 evaluated matrix 下的 conditional partition pattern；E3/E4 后再决定是否保留命名 |
| C04 | 当前 selector 是 method-adaptive attack | 旧 cross-TracIn 已证实退化；proper-TracIn只通过 Score→Selection；target-direct GU outcome 未开始 | 证据不足 | E8 G1/G2/G3 gate；在此之前写 systematic selector audit，不写已证实的 approximation-error adaptive exploit |
| C05 | Retrain Gap 足够代表 unlearning distance | F1 Gap 是任务级效用差；accepted predictions 提供 retrain/unlearn logits | 部分支持 | 保留 F1 Gap，但增加 KL/JS/L2 posterior distance 和 mean±std，明确互补关系 |
| C06 | 普通用户可以任意选高影响节点 | 现有 access tiers 主要刻画知识，不等于删除权限 | 证据不足 | threat model 改成 permission axis × knowledge axis；coalition 只能在其合法候选/owned set 内选点 |
| C07 | Verdict: Immune/Structural/Mild/Uniform | 无显式可复现阈值；`Immune` 暗示零脆弱性的统计证明 | 不支持 | 给出预注册 rubric，或删除 Verdict 列 |

## 4. 理论与实验并行依赖

```text
理论：permission×knowledge threat model ─────┐
理论：删除 surrogate 上界断言 ──────────────┤
理论：F1 Gap + KL/JS/L2 互补定义 ──────────┤
                                             ├─► 最终 claim / rebuttal
实验：E3 K5 formal gate ─► ΔF_noise          │
实验：E4 evidence import ─► GraphRevoker      │
实验：E8 target-direct gate ─► adaptivity ───┘
```

理论线现在可以完成 C01、C05、C06、C07 的定义与降级，不需要等待 GPU。实验线只有在 GPU、accepted `gnn_20`、canonical data、clean `main` 和 dry-run 全部通过后才可启动。

## 5. 下一步

1. 扩展 N09：为当前主表每个保留值登记 seed set、mean/std、sign、unit、source row filter 与 generator commit。
2. 从 accepted predictions 设计离线 KL/JS 统计合同；缺 predictions 的 cell 显式标 missing。
3. 环境恢复后先跑 E3 one-cell formal gate；不要先开大矩阵。
4. 导入/注册 GraphRevoker E4 远端 40-cell manifest，再决定主表 inclusion。
5. E8 target-direct 先跑 G1/G2/G3 gate；只有 outcome 支持时才恢复 adaptive/model-aware claim。
6. 论文立即删除 upper-bound 断言、GIF alignment 矛盾、开发残留和过强 immunity 语言。

## 6. 边界

- 本报告是首轮 ledger，不声称已审完论文中每一个数字。
- 本轮没有启动 GPU 实验，没有修改 cache、results、论文正文或现有图。
- GUIDE 按 paper protocol 完全排除。
- Markdown 是源事实版本；同名 HTML 与本报告的结论、数值和状态一致。
