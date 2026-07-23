---
title: 现代 Influence Maximization 算法调研与 OpenGU 实验计划
date: 2026-07-24
status: research-plan
scope: static-IC-cardinality-IM
datasets: [Cora, CiteSeer, PubMed]
---

# 现代 Influence Maximization 算法调研与 OpenGU 实验计划

## 执行结论

建议推进，而且不应只继续优化 CELF。下一阶段应建立一条独立的 **Modern-IM approximation-validity lane**，优先顺序为：

1. **首选实现：OPIM-C。** 它基于两批独立 RR sets，在运行中同时给出候选解、影响下界、最优值上界和可检查的停止证书，最符合当前项目的 Cache V2 与审计需求。
2. **理论/生态对照：corrected IMM。** 使用 Wei Chen 2018 的独立重采样修正版，不能直接照搬原始 IMM 实现并宣称原证明成立。
3. **小图质量锚点：TipTop。** 其目标是 $(1-\epsilon)$ 近最优，保证强于常见的 $(1-1/e-\epsilon)$，但依赖整数规划；只作为小图 reference，不阻塞主线。
4. **第二阶段加速：OPIM-C + SUBSIM。** 先验证 OPIM-C 语义，再替换 RR-set generator；只有高 influence 压力测试证明 RR sets 过大时才上 HIST。
5. **可选多预算方法：SKIM。** 一次生成 seed sequence、各 prefix 都可分析，适合 ratio sweep；实现优先级低于 OPIM-C。

不建议第一轮实现原始 SSA/D-SSA、把 CELF++包装成新近似、直接引入深度强化学习 IM，或直接覆盖现有 `im`。这些路线分别存在保证纠偏、语义重复、目标不可比和证据污染问题。

> [!IMPORTANT]
> 现代 IM 的第一研究问题不是“选点与旧 CELF 重合多少”，而是“新算法是否更可靠地优化 IC spread，以及这种目标改进是否真的传递到 approximate-GU 的 retrain gap”。低 Jaccard 但等 spread 可能只是多个近最优解；高 spread 但攻击不更强则是更有价值的 objective-mismatch 发现。

## 1. 为什么现在值得做

当前 [IMStrategy](../attack/attack_strategies/im_strategy.py) 使用 IC + MC-CELF，但 canonical 默认包含 `im_batch_size=5`。`batch_size>1` 会一次接受多个未经逐步重新验证的候选，因此它不是经典 CELF 的纯工程等价实现。

历史 prototype 已显示明显的 dataset interaction：

| Dataset / budget | Batch-CELF speedup | 独立评估 spread loss |
|---|---:|---:|
| Cora, $k=135$ | 34.6x | 1.26% |
| CiteSeer, $k=50$ | 1.6x | 11.98% |
| CiteSeer, $k=135$ | 3.9x | 17.05% |

来源为 [旧 V0–V4 prototype](../experiments/im_benchmark/docs/multi_v1_v3_summary.md)。这些结果只有 Cora/CiteSeer、单一历史实现口径，不能作为正式三数据集证据；但它们足以说明“Batch 近似是否保真”不是一个已经解决的问题。

同时，`ogbn-arxiv` 的历史 Cache V2 IM cold run 在 degree-pruned、50 MC、classic CELF 条件下仍耗时约 3 小时 46 分，见 [IM materializer 验收](../docs/cache_v2_im_selection_materializer_ACCEPTANCE_REPORT.md)。现代 RR-set 路线因此既有方法学价值，也有现实扩展性价值。

## 2. “理论下界”应分成三件事

用户关心的“理论下界保证”不能笼统书写。现代 IM 文献至少讨论三种不同保证：

| 保证类型 | 正确问题 | 例子 |
|---|---|---|
| 解质量下界 | 返回解至少达到 OPT 的多少 | $sigma(S)\ge(1-1/e-\epsilon)\mathrm{OPT}$ |
| 成功概率 | 上述质量下界多大概率成立 | $1-\delta$ 或 $1-n^{-\ell}$ |
| 时间/样本下界 | 任何算法至少需要多少图访问或样本 | 对网络规模近线性最优；或样本数渐近下界 |

经典 IC influence function 是 monotone submodular。[Kempe, Kleinberg, and Tardos](https://doi.org/10.1145/956750.956769) 证明，在可准确查询 influence 的前提下，逐步加入最大 marginal-gain 节点的 greedy 至少达到 $1-1/e$。但有限轮 MC 只是一个随机 value oracle；如果没有样本复杂度和置信控制，就不能自动把该保证贴到现有 MC-CELF 结果上。

RR-set 方法利用恒等式

$$
\sigma(S)=n\Pr[R\cap S\neq\varnothing],
$$

把 influence maximization 转成随机超边上的 maximum coverage。现代算法的主要差别在于：如何确定 RR-set 数量、如何验证解质量、如何降低每个 RR set 的生成与存储成本。

## 3. 算法谱系与项目角色

| 方法 | 核心机制 | 理论状态 | 本项目角色 | 优先级 |
|---|---|---|---|---:|
| Strict MC-Greedy/CELF | forward MC + 逐点 greedy | 仅在受控 oracle 下继承 $1-1/e$ | operational reference | 必须保留 |
| CELF++ | 缓存下一轮 marginal | 与同一 greedy 目标等价 | equivalence sanity | 低 |
| PMC | pruned Monte Carlo snapshots | 高质量 MC 路线，论文给出保证 | MC-family 对照 | 中低 |
| TIM/TIM+ | RR sets + 预计算样本界 | $(1-1/e-\epsilon)$，高概率 | 历史 RR 基线 | 低 |
| corrected IMM | 自适应估计 OPT 下界 + 独立最终 RR batch | $(1-1/e-\epsilon)$，高概率 | 理论/生态对照 | 高 |
| SSA/D-SSA original | stop-and-stare | 原始保证被后续工作指出缺口 | 不进入主矩阵 | 排除 |
| SSA-Fix | 修正 stop-and-stare | 恢复声明保证 | 可选复核 | 低 |
| OPIM-C | 双独立 RR batch + online certificate | $(1-1/e-\epsilon)$，高概率 | 第一实现候选 | 最高 |
| SKIM | bottom-$k$ reachability sketches | prefix-level 概率近似 | 多 budget 候选 | 中 |
| TipTop | RR sampling + integer programming | $(1-\epsilon)$ 近最优 | 小图质量 anchor | 中 |
| SUBSIM | 更快的 RR subset sampling | 保留上层算法保证 | OPIM-C estimator backend | 第二阶段 |
| HIST | sentinel seeds 截断大 RR sets | 高 influence 场景保证 | 条件扩展 | 第二阶段 |
| Ripples/cuRipples | 多核/多 GPU RR 系统 | 保留所实现算法语义 | 外部大图 oracle | 后续 |
| EPIC/AdaptiveGreedy | expected guarantee + adaptive feedback | 问题与保证语义不同 | related work | 排除 |

### 3.1 OPIM-C：第一推荐

[OPIM-C](https://doi.org/10.1145/3183713.3183749) 的优势不是“年份较新”，而是验证结构与本项目匹配：

1. 从第一批 RR sets $\mathcal R_1$ 上贪心得到 $S_k$，并估计最优解的上界；
2. 用独立第二批 RR sets $\mathcal R_2$ 估计 $S_k$ 的影响下界；
3. 当 lower/upper ratio 达到目标阈值时停止；否则增加样本；
4. 随时可以输出当前解和可解释的质量证书。

这使一个 Selection Artifact 不再只有节点列表，还可以记录：`rr_count_train`、`rr_count_verify`、上下界、certificate ratio、$\epsilon$、$\delta$、两批样本 hash 和运行资源。与当前只凭 `mc_rounds=100` 的结果相比，证据链明显更完整。

### 3.2 corrected IMM：不能忽略后续纠偏

[IMM](https://doi.org/10.1145/2723372.2723734) 是成熟 RR-set 基线，但 [Chen 2018](https://arxiv.org/abs/1808.09363) 指出原始鞅分析对自适应停止样本与最终 NodeSelection 的依赖处理存在技术问题。

建议采用最简单的 workaround：确定最终样本量后，重新独立生成整批 RR sets 再做最终选点。该修复最多把 RR 生成量增加约一倍，期望渐近复杂度仍保持

$$
O\!\left((k+\ell)(n+m)\log n/\epsilon^2\right).
$$

算法标识必须写成 `imm-corrected-independent-final-v1`，不能只在报告中补一句 caveat 而继续使用不明版本的 `IMM`。

### 3.3 SSA/D-SSA：速度声明不能脱离修正版

[Stop-and-Stare](https://arxiv.org/abs/1605.07990) 原论文声明 SSA/D-SSA 具有 $(1-1/e-\epsilon)$ 保证与渐近最少样本，并报告极高加速。但 [Huang et al. 2017](https://doi.org/10.14778/3099622.3099623) 复核后指出原始证明与部分实验结论存在缺口，并提出 SSA-Fix。

复核结果还显示明显 budget interaction：IC、小 $k$ 时 IMM 可能更快，大 $k$ 时 SSA/D-SSA 才更有优势。因此第一轮不应投入 SSA/D-SSA；若以后纳入，只能使用明确修正版并单独记录 recipe。

### 3.4 TipTop：更强保证，但不是第一生产方案

[TipTop](https://arxiv.org/abs/1701.08462) 通过在采样空间上求解整数规划，目标是任意 $\epsilon>0$ 下的 $(1-\epsilon)$ 近最优。这比 $1-1/e-\epsilon$ 强，适合回答“OPIM-C/IMM 实际距离近最优还有多远”。

代价是 MIP solver、模型构造与随机规划验证。建议只在 Cora/CiteSeer 的小 $k$ 运行；TipTop 失败或超时不能阻塞 OPIM-C 主线。

### 3.5 SUBSIM/HIST：确认瓶颈后再加

[Guo et al.](https://doi.org/10.1145/3318464.3389740) 的 SUBSIM 改进 RR-set generation，而不改变上层 maximum-coverage 目标。在入边概率和有界条件下，其分析把现有 RR-based IM 的期望时间改善到 $O(kn\log n/\epsilon^2)$；偏斜权重使用 SKIP subset sampler。

HIST 先找 sentinel seeds，再在反向传播命中 sentinel 时截断 RR set，主要解决高 influence 图上 RR set 过大的问题。当前 Planetoid、$p=0.1$ 未必处于这个区间，因此应先记录 RR-size 分布；只有 average/p95 RR size 明显膨胀时才实现 HIST。

### 3.6 SKIM、PMC 与并行系统

[SKIM](https://arxiv.org/abs/1408.6282) 输出一条 seed sequence，各 prefix 均可分析，适合一次支持多个 deletion budget。[PMC](https://doi.org/10.1609/aaai.v28i1.8726) 更接近现有 forward-MC 语义，可作为“RR 路线是否真的必要”的对照。

[PNNL Ripples](https://github.com/pnnl/ripples) 提供 C++/CUDA 的并行 IM 框架。其价值在大图吞吐，不在改变 selection objective。第一阶段把它当外部 oracle；等 Python 语义 gate 通过后，再决定是否接入 C++/GPU。

## 4. 与 OpenGU 契约的适配

### 4.1 候选节点受限

OpenGU 只能从 persisted `train_mask/train_indices` 选删除节点，而 influence spread 仍在全图上计算。建议定义：

$$
\max_{S\subseteq C,\ |S|=k}\sigma(S),\qquad C=\text{persisted training candidates}.
$$

将 monotone submodular function 的 ground set 从 $V$ 限制到 $C$ 后，greedy 保证相对于受限最优解仍成立。这是由子模性得到的项目适配推论，不冒充原论文已经验证 OpenGU train-mask 契约。

RR roots 必须从全体目标节点域采样；maximum coverage 选种子时才过滤到 $C$。如果只从训练节点采 RR roots，优化目标会悄悄变成“训练子集上的 spread”。

### 4.2 图方向与边概率

当前 canonical graph fingerprint 去除完全重复的 directed arcs，但保留 $(u,v)$ 与 $(v,u)$。Planetoid 常以双向 arc 表示无向边；现有 forward MC 实际把两个方向视为独立 IC 尝试。RR sampler 必须严格复现这一语义：

- 为每个 directed arc 独立采样 live/dead；
- 使用 reverse adjacency 生成 RR set；
- 不再次无向化，不把两条 arc 合并成一次 Bernoulli；
- `edge_direction_mode` 与 `edge_probability_semantics` 进入 recipe。

### 4.3 Cache V2 与命名

第一阶段新增策略标识：

- `im_celf_strict`
- `im_batch_celf_current`
- `im_imm_corrected`
- `im_opimc`
- `im_tiptop_anchor`（可选）

不要把新结果直接写成 `im`，也不要读取/覆盖 Legacy `im_celf` / `im` ScoreCache。Selection Recipe 至少包含：

| Identity field | 内容 |
|---|---|
| Algorithm | family、algorithm version、修正版标识 |
| Diffusion | IC、$p$ 或 per-edge probability hash、方向语义 |
| Guarantee | $\epsilon$、$\delta$、certificate mode |
| Randomness | selector/RR seed、PRNG algorithm/version |
| Data | dataset、graph、candidate、root-domain fingerprints |
| Budget | $k$ 与 candidate ratio |
| Backend | Python/Numba/C++，仅作 execution provenance |

固定 RR batch 上的 greedy sequence 可以复用前缀，但 max-$k$ 的证书不自动覆盖其他预算。每个报告 budget 必须单独保存 certificate；在实现 per-prefix certificate 之前，不把 max-$k$ prefix 标成“已认证”。

## 5. 研究问题与假设

| ID | 研究问题 | 可证伪假设 |
|---|---|---|
| RQ1 | 新方法是否更好优化同一个 IC spread？ | OPIM-C/corrected IMM 的独立 spread 不低于 current Batch-CELF |
| RQ2 | 理论保证的代价是什么？ | runtime/sample 随 $\epsilon^{-2}$ 增长，但 PubMed 仍优于 strict CELF |
| RQ3 | 多个近最优解是否导致低集合重合？ | Jaccard 可低，但 spread regret 仍接近 0 |
| RQ4 | 更高 IC spread 是否带来更强 GU 攻击？ | spread 提升与 retrain gap 提升并不必然一致 |
| RQ5 | 算法优势是否依赖图与 budget？ | CiteSeer/PubMed、small/large $k$ 存在明显 interaction |

## 6. 分阶段实验计划

### Phase 0：实现契约与最小原语

建议新建隔离目录 `experiments/im_modern/`，不改 production `IMStrategy` 路由。最小模块为：

1. deterministic IC live-edge / reverse-RR sampler；
2. candidate-restricted maximum coverage greedy；
3. OPIM-C 双样本循环与 certificate；
4. corrected IMM 独立最终样本；
5. paired independent-MC evaluator；
6. versioned recipe、manifest 与 cold/warm store boundary。

首版优先 Python/Numba，便于逐项验证；不先绑定 Ripples 或 GPU。

### Phase 1：精确小图与契约 gate

在 $n\le 12$ 的 directed synthetic graphs 上枚举 live-edge worlds 与所有 $k$-subsets，得到真正 OPT。覆盖 chain、star、disconnected、双向 arc、重复输入 arc、candidate-restricted 等情况。

必须全部通过：

- RR estimator 对 exact influence 无系统偏差；
- maximum coverage 与手工 RR hypergraph 一致；
- candidate 外节点绝不被选，但仍可被传播覆盖；
- OPIM-C 上下界、停止条件和 failure probability 参数实现正确；
- corrected IMM 最终 RR batch 与估计阶段独立；
- same recipe + same seed 的 selected order、certificate 和 sample hashes 可复现；
- recipe 任一语义字段变化都产生 cache miss。

### Phase 2：三数据集 canonical selector-validity

直接使用 active checkout 内 canonical `data/processed/transductive/` 80/0/20 split。public Planetoid 固定小候选集不再作为新实验的 bridge；旧结果只在原报告中作为机制诊断留档。

| Dimension | Values |
|---|---|
| Datasets | Cora / CiteSeer / PubMed |
| Candidate pool | complete persisted OpenGU train candidates |
| Expected candidate counts | 2,166 / 2,661 / 15,773；正式值由 manifest 冻结 |
| Ratios | 0.01 / 0.05 |
| Expected $k$ | Cora 21/108；CiteSeer 26/133；PubMed 157/788 |
| Selector/RR seeds | 42 / 212 / 2024 |
| Primary $p$ | 0.1 |
| Primary guarantee | $\epsilon=0.1,\ \delta=0.01$ |
| Main algorithms | degree / random / corrected IMM / OPIM-C / RR-SNI / RR-Shapley / RR-$k$-semivalue |
| Diagnostic anchors | current Batch-CELF / strict CELF 仅限 Cora、seed42、1% feasibility |

主矩阵为 $3\ datasets\times3\ seeds\times2\ ratios\times7\ methods=126$ 行。可以复用 RR batches 降低计算，但每个 budget 的 certificate 必须单独报告。旧 CELF 诊断不进入 promotion 统计。

补充两组单 seed sensitivity：

- $\epsilon\in\{0.20,0.10,0.05\}$，验证时间/样本与质量曲线；
- $p\in\{0.05,0.10,0.20\}$，观察 subcritical/high-influence 转换和 RR-size 膨胀。

### Phase 3：ogbn-arxiv 大图 Gate

Phase 2 通过后，使用 active checkout 内 canonical ogbn-arxiv processed graph/split，禁止下载、临时预处理、外部数据根或 degree candidate pruning。

| Dimension | Values |
|---|---|
| Dataset | ogbn-arxiv |
| Candidate pool | persisted OpenGU train mask |
| Ratios | 0.01 / 0.05 |
| Selector seeds | 42 / 212 / 2024 |
| Algorithms | degree / corrected IMM / OPIM-C / RR-SNI / RR-Shapley / RR-$k$-semivalue |
| Rows | $3\ seeds\times2\ ratios\times6\ methods=36$ |

这一层回答成熟 IM 在完整大图候选域上是否仍能满足时间、RSS、certificate 和 independent-spread gate。任何正式矩阵必须等代码线完整合入 `main` 后，在 clean SSH active checkout 上固定 full `main` SHA 运行。

### Phase 4：GU downstream canary

只把三种有解释意义的删除集送入 GU：

- degree；
- random；
- Phase 2/3 通过 spread promotion 的最佳一个现代 IM 方法。

首个 canary：Cora + CiteSeer、ratio 0.05、GIF + GNNDelete、3 GU seeds，共 $2\times2\times3\times3=36$ cells。主指标为 retrain gap，辅指标为 relative F1 drop、collateral 和 update-detection AUC。

扩展条件：

- 若 IM winner 相对 degree 的 paired retrain-gap gain 达到至少 1 percentage point，或改变方法脆弱性排序，则扩 PubMed 和一个稳健方法；
- 若 IC spread 明显提升但 GU outcome 不变/变弱，不继续调参追求“更好看”，而报告 objective mismatch；
- 若 selector 层没有可测差异，则停止 GU 扩矩阵。

### Phase 5：条件扩展

- RR-size p95/maximum 成为主要瓶颈：实现 SUBSIM，必要时 HIST；
- 多 ratio 重复计算成为主要瓶颈：评估 SKIM 或 per-prefix OPIM-C certificate；
- `ogbn-arxiv` CPU 仍不可接受：以 Ripples/CuRipples 作外部 oracle，再决定 C++ integration；
- 需要强质量 anchor：扩大 TipTop 小图范围，但不让 MIP 阻塞主线。

## 7. 指标与验收门槛

### 7.1 Selection objective

统一使用一批独立、固定的 common-random live-edge worlds 评估所有算法；优化样本与评估样本必须隔离。

| Metric | 角色 |
|---|---|
| Independent spread mean + 95% CI | 主质量指标 |
| Spread regret / ratio to best anchor | 主 fidelity 指标 |
| OPIM-C lower / upper / certificate ratio | 理论证书 |
| Jaccard、common fraction、prefix overlap | 解多样性辅指标 |
| Runtime、peak RSS | 工程指标 |
| RR count、total memberships、mean/p95/max size | RR 成本解释 |
| Repeatability across selector seeds | 随机稳定性 |

建议 promotion gate：

1. synthetic exact gate 全通过；
2. 27 个三数据集 primary cells 无 certificate/recipe/provenance 错误；
3. OPIM-C 对 best independently evaluated set 的 mean spread ratio 至少 0.99，worst-cell 至少 0.97；
4. PubMed cold runtime 相对 current Batch-CELF 至少 5x 改善，或在相同时间预算下给出显著更窄证书；
5. 同 recipe/seed 重跑输出 bit-stable ordered nodes 与 manifest；
6. 没有读取、覆盖或 promotion Legacy IM cache。

这些 0.99/0.97 是项目 promotion gate，不是论文理论常数。以 $\epsilon=0.1$ 为例，通用理论阈值只有

$$
1-1/e-0.1\approx0.5321,
$$

实际研究要求应明显高于这个 worst-case 下界。

### 7.2 Downstream

Downstream 不设置“必须复现旧 IM”的单一通过条件，因为新算法可能找到 spread 更高但集合不同的解。结果按四类解释：

| IC spread | GU damage | 结论 |
|---|---|---|
| 提高 | 提高 | 新 IM 同时改善目标与攻击 |
| 提高 | 不变/降低 | IC objective 与 GU vulnerability 失配 |
| 近似相同 | 集合差异大 | 多个近最优 seed sets |
| 提高不明显 | 速度大幅提高 | 工程替代价值，研究增量有限 |

## 8. 预计工作量与停止条件

| 阶段 | 预计投入 | 明确停止条件 |
|---|---:|---|
| OPIM-C + corrected IMM MVP | 2–3 人日 | exact/certificate gate 无法闭环则不跑数据集 |
| synthetic + Cora pilot | 1 人日 | spread estimator 或 candidate contract 不一致 |
| 三数据集 selector matrix | 1–2 CPU 日 | OPIM-C 全部慢且无质量/证书优势 |
| canonical transfer | 1 CPU/SSH 日 | public → canonical 结论不稳定则先解释 split interaction |
| GU canary | 1 GPU 日量级 | selector 层无差异则不启动 |
| SUBSIM/HIST/Ripples | 2–4 人日 | 只有实测瓶颈触发才投入 |

## 9. 最终建议

这条线值得做，但应把论文贡献目标定为：

> **Modern IM algorithms can provide auditable spread guarantees and major scalability gains, but whether better influence maximization yields stronger attacks on approximate graph unlearning is an empirical question.**

第一步不是实现十个算法，而是用 `OPIM-C + corrected IMM + current Batch-CELF + strict reference` 建立一个可证明、可复现、可向 GU outcome 传递的最小闭环。TipTop、SUBSIM/HIST、SKIM 和 Ripples分别承担质量 anchor、RR backend、多预算、系统扩展角色；只有对应 gate 触发才进入。

## 参考文献

1. Kempe, D., Kleinberg, J., & Tardos, É. (2003/2015). [Maximizing the Spread of Influence through a Social Network](https://doi.org/10.1145/956750.956769).
2. Leskovec, J., et al. (2007). [Cost-effective Outbreak Detection in Networks](https://doi.org/10.1145/1281192.1281239).
3. Goyal, A., Lu, W., & Lakshmanan, L. V. S. (2011). [CELF++](https://doi.org/10.1145/1963192.1963217).
4. Borgs, C., Brautbar, M., Chayes, J., & Lucier, B. (2014). [Maximizing Social Influence in Nearly Optimal Time](https://arxiv.org/abs/1212.0884).
5. Tang, Y., Xiao, X., & Shi, Y. (2014). [Influence Maximization: Near-Optimal Time Complexity Meets Practical Efficiency](https://arxiv.org/abs/1404.0900).
6. Tang, Y., Shi, Y., & Xiao, X. (2015). [Influence Maximization in Near-Linear Time: A Martingale Approach](https://doi.org/10.1145/2723372.2723734).
7. Chen, W. (2018). [An Issue in the Martingale Analysis of IMM](https://arxiv.org/abs/1808.09363).
8. Nguyen, H. T., Thai, M. T., & Dinh, T. N. (2016). [Stop-and-Stare](https://arxiv.org/abs/1605.07990).
9. Huang, K., et al. (2017). [Revisiting the Stop-and-Stare Algorithms for Influence Maximization](https://doi.org/10.14778/3099622.3099623).
10. Tang, J., Tang, X., Xiao, X., & Yuan, J. (2018). [Online Processing Algorithms for Influence Maximization](https://doi.org/10.1145/3183713.3183749).
11. Cohen, E., Delling, D., Pajor, T., & Werneck, R. F. (2014). [Sketch-based Influence Maximization and Computation](https://arxiv.org/abs/1408.6282).
12. Ohsaka, N., et al. (2014). [Fast and Accurate Influence Maximization on Large Networks with Pruned Monte-Carlo Simulations](https://doi.org/10.1609/aaai.v28i1.8726).
13. Li, X., Smith, J. D., Dinh, T. N., & Thai, M. T. (2019). [TipTop](https://arxiv.org/abs/1701.08462).
14. Guo, Q., Wang, S., Wei, Z., & Chen, M. (2020/2022). [Influence Maximization Revisited](https://doi.org/10.1145/3318464.3389740).
15. Minutoli, M., et al. [PNNL Ripples](https://github.com/pnnl/ripples).

## 已知边界

- 这是调研与执行计划，不是新 IM 的实验验收报告。
- 旧 V0–V4 数字仅作立项依据，不具备当前 formal provenance。
- 候选受限保证是由 monotone submodularity 推导出的项目适配，需用小图枚举和实现测试验证。
- OPIM-C、TipTop、SUBSIM 的第三方代码可得性与许可证尚未达到 formal dependency acceptance；计划按仓库内重实现核心语义估算。
- 没有在本轮启动 GPU/GU 实验，也没有修改 production selector 或 Legacy cache。
