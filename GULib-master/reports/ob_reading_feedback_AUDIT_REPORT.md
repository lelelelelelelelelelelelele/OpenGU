---
title: OB 阅读反馈逐条核对报告
date: 2026-07-20
status: corrected-and-synchronized
source_branch: codex/docs-tracin-checkpoint-clarification-20260720
parent: main@2f0d22a
---

# OB 阅读反馈逐条核对报告

## 总结

你的阅读判断是对的；本轮已把底层证据、旧 OB 页面、实验计划与论文 SUP 按最终 A/B–C–D 分类同步。

- **已解决**：GraphRevoker 修复结论与回归台账；Cache V2 体系化重构；A/B、C-IF、D-GIF 的组内与组间实验；旧 21 的表格、重复章节和 IF/GIF 命名；OB 11→Appendix A.6 与 OB 12→Appendix A.7 的联动。
- **边界保留**：三数据集 × 三 seed 只作描述性机制证据；production proper-TracIn gate 与具体 GU end-to-end canary 仍是独立后续。

本报告先完成核对，随后已按用户确认的分类改写相关 OB、报告与 SUP。验证基线为本地 `main@2f0d22a` 加当前工作树中的 GraphRevoker 文档清理；初始定向回归共 **177 passed in 8.21s**，本轮文档回归结果见末尾更新。

## 逐条核对

| 你的意见 | 判定 | 当前证据与准确解释 |
|---|---|---|
| `21` §2 表格看起来奇怪 | **已解决** | 旧宽表已改成 A/B 参数变化、C-IF、D-GIF 三组短表，公式和角色不再挤在一个伞形表中。 |
| §3.4 与 §3.5 很像 | **已解决** | A=\(\lVert g_v\rVert\) 与 B=\(\lVert H^{-1}g_v\rVert\) 已合并为 A/B 对照组；A 明确是当前矩阵中 B 排序的强 Hessian-free 代理。 |
| §3.5 最后一段是什么意思 | **已解决并降级为技术细节** | 正文只写“\(H^{-1}g\) 通过迭代 IHVP 求解”；具体 solver、HVP、shared probes 与数量移到实现/复现配置。 |
| Hutchinson shared probes 和 HVP 是否类似 | **不再作为方法问题展开** | 它们都属于 IHVP 求解链的实现细节，不构成不同 selector、近似路线或贡献点。 |
| A 是否是 B 的近似 | **是强排序代理，但不是定义等价** | A vs B reference Spearman=`0.962`，因此在本矩阵里应明确称 A 为 B 排序的强 Hessian-free proxy；它与 self-TracIn 的代理思路一致。 |
| §3.3 当前仍是 IF，不是 GIF | **已解决** | `<g_v,H^{-1}g_E>` 与 `<grad1,H^{-1}g_E>` 均归 C-IF；只有 `q_v=grad1-grad2` 的 `<q_v,H^{-1}g_E>` 归 D-GIF。 |
| 需要测试 A/B 相似度 | **已完成并已回写** | 9 个 dataset-seed cell 上：A vs B reference Spearman=`0.962`；Jaccard@k 为 `0.656/0.684/0.793`（k=`3/7/14`）。IHVP 实现间的 `0.968` 只保留为复现 sanity check。 |
| 需要测试 GIF 与 IF 相似度 | **已完成，而且结果说明必须分层命名** | point IF vs full GIF Spearman=`0.112`；simple IF vs full GIF=`0.040`，二者都不能冒充 full GIF。固定 full graph source 后，Hessian-free `p_graph` vs `gt_full` Spearman=`0.984`，这是当前正确的 GIF proxy 对照。 |
| `13` 仍是 Runbook，GraphRevoker 应写结论/测试 | **内容已解决；文件名兼容保留** | 当前标题已是“修复验收与回归测试台账”，列出 `PASS / PASS(remote) / ARCHIVE PENDING / INVALID`、GR-01—GR-08、永久失效范围和剩余归档闭环。旧文件名只为保留 Obsidian 链接。GraphRevoker 远端 E4 为 40/40 passed；本地完整 evidence import 仍是 `ARCHIVE PENDING`。 |
| 指导书应标明成功与否 | **已解决** | 13 已把“代码修好”“远端矩阵通过”“本地产物归档未闭环”“旧数据永久失效”“TracIn/Hybrid 未包含”拆开，不再用一个模糊的 done 覆盖所有状态。 |
| Runbook 仍是旧 cache 写法 | **已解决于当前 13/19；其他旧文档仍需防漂移** | 13 已链接 Cache V2/Legacy 边界，并规定 Legacy IF/Selection Cache 只读、新算法建 versioned Recipe。19 已成为完整 V2 架构与迁移文档。 |
| Cache 重构应是大内容 | **已成为独立的大型工程成果** | V2 固定 Score/Selection/Prediction/Evaluation 四类 Artifact；移除“大而全 ResultCache”；使用 immutable Recipe、依赖 DAG、可重建 SQLite 索引、真实 consumer refs 与 fail-closed mismatch。Legacy 痛点也有量化：远端 783 个 ResultCache JSON，一次全解析约 26.1 秒，fallback 接近 `O(cells × cache_files)`。本次相关回归包含在 177 个通过测试中。 |
| `11` 应和 SUP 论文部分同步 | **已解决** | OB 11 已扩成结构轴 + A/B–C–D 的组内/组间矩阵；paper outline 新增 A.6，Overleaf appendix 已加入一致的 taxonomy 与关键数字。 |
| `12` 是否可以开始写成 SUP/Appendix | **已开始并形成首个闭环** | OB 12 已升级为 proxy-validity bridge；IM 六数据集 set-level 证据与 TracIn V2 的 3 datasets × 2 backbones × 3 seeds gate 已进入 paper outline A.7 和 Overleaf Appendix。production Cache/Hybrid/GU 仍明确 pending。 |
| 应设计多步快跑，而不是全部改好再开始 | **已写成固定闭环** | OB 11 规定 reference/proxy gate → 组间比较 → set-deletion → OB 回填 → SUP 增量的五步快跑；每个 accepted slice 都有可汇报结论。 |

## 数学关系的最短正确读法

| 层 | 分数 | 回答的问题 | 可扩展近似 |
|---|---|---|---|
| A | \(\lVert g_v\rVert\) | 这个点自己的训练梯度大不大 | 当前设置下是 B 排序的强 Hessian-free proxy（0.962） |
| B | \(\lVert H^{-1}g_v\rVert\) | 删除这个点预计让参数移动多远 | 通过迭代 IHVP 求解；solver 细节见复现配置 |
| C-point IF | `<g_v,H^{-1}g_E>` | candidate-only 参数变化是否伤害 E | `<g_v,g_E>` |
| C-simple IF | `<grad1_v,H^{-1}g_E>` | 受影响邻域的一侧梯度是否伤害 E | `<grad1_v,g_E>` |
| D-full GIF | `<(grad1_v-grad2_v),H^{-1}g_E>` | 图删除干预的完整源是否伤害 E | `<(grad1_v-grad2_v),g_E>`，即 `p_graph` |

这里有两个不同的“近似”问题，不能混写：

1. **B 的排序代理**：A 强代理 B reference；当前 Spearman=`0.962`。
2. **D-full GIF 的 Hessian-free 近似**：`p_graph` 近似 `gt_full`；当前 Spearman=`0.984`。

IHVP 实现之间的 `0.968` 只作数值复现 sanity check，不作为第三条方法近似结论。

A 与 B 的 `0.962` 足以支持“强排序代理”，但不支持定义等价。C-point/C-simple IF 与 D-full GIF 的低相关证明 `grad2` source correction 不能省略。

## 建议的多步快跑契约

不要把“做完所有实验”定义为一次迭代。每个主题改成一个可在 0.5—2 天内闭环的 vertical slice：

1. **定义锁定**：OB 写清问题、reference、proxy、metric、接受边界；同时在 SUP 建空小节和目标表格，不等数字齐。
2. **最小证据**：先跑 1 dataset × 1 seed × 1 budget；产出双格式验收、回填 OB，并把 SUP 从“计划”改成“pilot finding + limitation”。
3. **扩展闸门**：pilot 有解释价值才扩到 3 datasets × 3 seeds；无价值则记录 negative result 并关闭，不开启全矩阵。
4. **下游闸门**：selection fidelity 与实际 damage 分开；只有 selector 层通过后，再做 set deletion 或 GU canary。
5. **论文增量**：每次 accepted slice 必须在同一分支同步四处：证据报告、OB bridge、SUP/outline、WORKPLAN 状态。缺一项就不能叫“文档完成”。
6. **汇报增量**：baseline 阶段也汇报可验证成果，例如 cache 命中/复杂度、错误边界、被否定的近似、pilot 数字和下一 gate，不把“主矩阵没跑完”写成“本阶段没有内容”。

### 对 11/SUP 的具体四个 sprint

| Sprint | 最小范围 | 当次即可汇报的内容 | 扩展条件 |
|---|---|---|---|
| S1 · topology overlap | 现有 degree/PageRank/IM/legacy TracIn | selector axis 确实不全是同一批点 | 已完成；整理进 SUP |
| S2 · target taxonomy | 现有 3 datasets × 3 seeds A/B–C–D matrix | A 强代理 B；C-IF 不等于 D-GIF | 已完成并同步 OB 11/21 与 SUP |
| S3 · scalable proxy | `p_graph` 对 D-full | `0.984` 验证 D 的 Hessian-free proxy；IHVP solver 一致性留在复现记录 | 已完成；形成 SUP proxy 结论 |
| S3b · approximation validity | IM vs degree 六数据集 + TracIn V2 18-run selector gate | IM vs degree mean Jaccard=`0.089`；trajectory proxy 对 eval-IF 的配置均值 Spearman=`0.762–0.962`，但存在 PubMed/GAT 边界 | 已同步 OB 12 与 Appendix A.7；仅 selector/prototype 证据 |
| S4 · production/attack | proper-TracIn runner gate + 最小 GU canary | 机制 proxy 能否进入真实 approximate-GU attack | 正式 Artifact/cache、Legacy 隔离、Hybrid parent 与 GU canary 仍待闭环；通过后再扩 C.6 |

这种节奏允许每个 sprint 都形成新结论；S4 没完成不会抹掉 S1—S3 已经可写、可讲、可审阅的成果。

## 建议优先修正顺序

1. 已修旧 `21`：A/B、C-IF、D-GIF 分开；IHVP 统一写法已锁定，solver/probe 细节移到复现配置。
2. 已扩写 OB 11 为 SUP evidence bridge，并在 paper outline/Overleaf 新建 A.6。
3. 已把 OB 12 的 IM / trajectory proxy-validity 证据写入 paper outline/Overleaf A.7，不等待 production 接入才开始写附录。
4. 下一步按 vertical-slice 契约完成正式 Artifact/cache、Legacy 隔离、Hybrid 与最小 GU canary；通过后再把新版 outcome 接入 main-results。

## 证据入口

- `文档规划/20_研究框架/21_TracIn变体与GIF关系.md`
- `文档规划/10_实验矩阵/11_策略输出重合度实验.md`
- `文档规划/10_实验矩阵/12_近似策略重合度实验.md`
- `文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md`
- `文档规划/10_实验矩阵/19_Cache架构重设计与迁移方案.md`
- `文档规划/10_实验矩阵/21_C目标TracIn与GIF近似有效性实验计划.md`
- `reports/c_target_v1_REPORT.md`
- `reports/bc_target_matrix_REPORT.md`
- `docs/workplan_parallel_modules_REPORT.md`
- `docs/tracin_v2_gates_ACCEPTANCE_REPORT.md`
- `report/paper/outline_v2.md`
- `report/paper/outline/A7_approximation_validity.md`
- `report/paper/overleaf/sec/A_appendix.tex`

## 本轮修正验收

- `tests/test_c_target_v1.py` + `tests/test_bc_target_v2.py`：**11 passed**；
- 本次重建的 OB 11、OB 12 与 audit HTML：均含渲染后的 table，无原始 `|...|` 表格残留；
- 上述 3 份 HTML 的本地链接：**0 missing**；
- A.7 关键数字 `0.089 / 0.762 / 0.962`：OB 12 Markdown/HTML、paper outline 与 Overleaf 一致；
- Overleaf appendix 花括号计数：`561 / 561`，table/tabular 均为 `9 / 9`，无重复 label；
- `git diff --check`：通过，仅有既有 CRLF 提示。
