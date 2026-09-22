# AAGU-032 / AAGU-053：3000 轮参数下的论文结果分析

日期：2026-09-23　｜　状态：结果分析草稿，待科学审阅

## 范围与证据身份

本稿只使用当前 3000 轮默认参数对应的 AAGU-032 与 AAGU-053 运行及产物，不读取或对照此前参数版本的结果。两项运行的 YAML 都省略了 `training.epochs`；它们各自运行 commit 中的 `experiments/modular_config.py` 将默认 epoch 设为 3000（AAGU-032：`ee4ea59509523a650fe67bacf9bc961dfe9db78b`；AAGU-053：`38ca4e76e2fd45d30d88dc47cf7aad950193bdc7`）。

| 实验 | 当前运行 | 条件格 | 数据集分布 | Manifest SHA-256 | 产物核验 |
|---|---|---:|---|---|---:|
| AAGU-032 | `aagu032-recovery-full-20260920` | 360 | Cora/CiteSeer/PubMed 各 120 | `8391e397c1c12075e66249844fe93ca70423a0fede0785faae23185e0541e1ed` | 720 个声明文件通过 SHA-256 |
| AAGU-053 | `aagu053-newtraining-full-20260920` | 96 | Cora/CiteSeer/PubMed 各 32 | `dfb6f7c88021291847765a901d61efa698df889a8157fedc2f9639d50a852e7e` | 192 个声明文件通过 SHA-256 |

032 是 10 个 selector × 4 个删除预算 × 3 个训练 seed 的完整 Retrain 表；053 是 6 个 selector × 3 个数据集 × 2 种方法，含 48 组严格匹配的 GNNDelete/Retrain 请求。032 的 360 个 method 产物在恢复运行中均为 Cache HIT，未调用 method producer；053 有 24 个 method Cache MISS 且 producer 被调用，另 72 个 method HIT；053 的 Selection 96/96 HIT。因此“已归档并核验”不等于恢复运行重新计算了全部模型。

### 指标口径核验

归档字段 `utility.f1_before` / `utility.f1_after` 的生成代码位于 `experiments/unlearning_outputs.py::utility`。代码对测试节点的 `argmax(logits) == label` 求均值，实际是 test accuracy；虽然 JSON 字段名为 F1，但没有执行 macro-F1 计算。以下正文统一按 test accuracy 表述。单标签多分类任务的 micro-F1 数值会等于 accuracy；若论文需要 macro-F1，须从同一已归档 Output 与 test mask 重算后再替换表内结果。

## 结果分析

### AAGU-032：D-full 请求在完整 Retrain 下的测试效用

这里的端点是同一删除请求下完整 Retrain 的测试准确率 `utility.f1_after`。它回答不同 selector 选出的请求对 Retrain 后测试效用的影响，不是 GNNDelete/GU 的结果，也不单独测量遗忘质量。

将三个 GCN D-full 配置（`gt_full`、`gt_full_all_trainable`、`gt_full_all_trainable_hops3`）与同数据集、同预算、同训练 seed 的 Degree 结果作描述性配对。先在每个配置和预算内对三个训练 seed 求差，再统计每个数据集 12 个“配置 × 预算”均值：

| 数据集 | D-full 相对 Degree 的测试准确率差 | 低于 / 持平 / 高于 Degree 的配置预算组 | 与 Random 的平均差 |
|---|---:|---:|---:|
| Cora | −0.277 pp | 8 / 2 / 2（12 组） | −0.062 pp |
| CiteSeer | +0.188 pp | 4 / 0 / 8（12 组） | +0.526 pp |
| PubMed | −0.922 pp | 10 / 0 / 2（12 组） | −0.949 pp |

差值保留符号，负值表示该 D-full 配置在完整 Retrain 后的测试准确率更低。Cora 与 PubMed 上 D-full 配置多数低于 Degree/Random；CiteSeer 上这一方向减弱并对 Degree 反转。因此当前结果支持的是数据集和配置条件下的差异，不能写成 D-full 普遍优于 Degree 或 Random。三个预算 × 配置组不是独立样本，以上汇总不作显著性检验。

10% 预算下，三个 D-full GCN 配置与 Degree 的节点交集占 D-full 选集比例，在 3 个训练 seed 上共 9 个配对：Cora `21.22 ± 1.41%`，CiteSeer `13.22 ± 3.38%`，PubMed `22.39 ± 3.05%`（均值 ± 样本 SD）。这显示本矩阵中的两类选择集合有明显差异；它不证明两种选择机制因果独立。当前矩阵最高预算为 15%，因此不能据此重述 20% Degree 预筛的包含率。

作为近似选择补充，`r_point.yaml` 相对 `gt_full.yaml` 的 Retrain 测试准确率配对差（R-point − gt_full；同数据集、预算、训练 seed，n=3）如下。10% / 15% 下 Cora 为 `−1.046 ± 0.564 / −0.984 ± 1.296 pp`，CiteSeer 为 `+0.100 ± 1.107 / −0.050 ± 0.677 pp`，PubMed 为 `−0.372 ± 1.003 / −0.735 ± 1.038 pp`。它说明该 Retrain 端点上的差异幅度较小且跨数据集有异质性；这些数据不支持逐条件等效，也没有提供当前参数下可比的 selector MISS 计时。

### AAGU-053：同一请求下 GNNDelete 与完整 Retrain 的分解

每个删除请求的 GNNDelete 与 Retrain 使用同一个 `selection_id` 和相同 `selected_nodes`。表中是每个数据集 16 个请求等权的均值；每个预算均为 10%。`P0` 取 GNNDelete 记录的删除前 `utility.f1_before`。差值按统计协议保留符号：

`P0 − GNNDelete = (P0 − Retrain) + (Retrain − GNNDelete)`

| 数据集 | P0 测试准确率 | GNNDelete | Retrain | P0−GU | P0−Retrain | Retrain−GU |
|---|---:|---:|---:|---:|---:|---:|
| Cora | 90.22% | 70.64% | 89.67% | +19.580 pp | +0.554 pp | +19.027 pp |
| CiteSeer | 74.47% | 74.64% | 74.81% | −0.169 pp | −0.338 pp | +0.169 pp |
| PubMed | 88.56% | 85.80% | 88.48% | +2.764 pp | +0.087 pp | +2.677 pp |

在这批请求中，Cora 的 GNNDelete 与 Retrain 测试效用相差约 19 pp，PubMed 相差约 2.7 pp，而 CiteSeer 的数据集平均 gap 接近零。CiteSeer 的 selector 组内 gap 同时出现正负值；Cora 与 PubMed 的六类 selector 组均值则为正。因而不应将 CiteSeer 的近零均值写成等效性，也不应从任一单一数据集推广出统一 GU 响应。正的 `Retrain−GU` 只说明 GNNDelete 测试准确率低于相同删除请求下的 Retrain；它不是遗忘正确性或隐私保证。

`update_detection_auc` 也存在于 053 结果中：按 16 个请求等权，Cora/CiteSeer/PubMed 均值分别为 `0.587/0.731/0.509`。GNNDelete 实现把删除节点标为正例、测试节点标为负例，并以删除前后预测概率的 L2 变化作为分数计算 AUC。该项可作为后验变化检测诊断；若用于论文隐私结论，还需独立审查威胁模型、采样/控制设计和统计单位，不能将其直接称为通用 MIA 或隐私风险结论。

## 可直接进入论文的英文草稿

> **Selector-dependent retraining outcomes.** Across the three datasets, the retraining endpoint does not yield a dataset-invariant ordering of deletion selectors. Averaged over the three GCN D-full configurations and four deletion budgets, D-full requests produced a test-accuracy change of −0.277 pp relative to Degree on Cora and −0.922 pp on PubMed, whereas the corresponding difference was +0.188 pp on CiteSeer. The direction also varied across configuration-budget groups, particularly on CiteSeer. These results characterize the utility of full retraining under the selected requests; they do not establish the behavior of an approximate unlearning method.

> **Matched GNNDelete–Retrain outcomes.** For the 48 requests in AAGU-053, GNNDelete and full retraining were evaluated on identical selected-node sets. Averaged over 16 requests per dataset, the test-accuracy gap (F_R(S)-F_{GU}(S)) was 19.027 pp on Cora, 0.169 pp on CiteSeer, and 2.677 pp on PubMed. The decomposition (F_0-F_{GU}(S)=[F_0-F_R(S)]+[F_R(S)-F_{GU}(S)]) shows that the corresponding (F_0-F_R(S)) component was +0.554, −0.338, and +0.087 pp, respectively. Thus, the observed endpoint gap is strongly dataset dependent. Because the current matrix contains one training seed per dataset and the logged endpoint is test accuracy, these results should be interpreted descriptively and should not be equated with forgetting quality or privacy.

## 理论—证据对照与审稿边界

| 待检验主张 | 当前可观测量与对照 | 当前证据判断 | 限制 |
|---|---|---|---|
| Selector 会改变请求在 Retrain 下的测试效用 | AAGU-032 `utility.f1_after`；同数据集/预算/训练 seed，对比 Degree 和 Random | 条件性支持；跨数据集有方向反转 | 只有 Retrain；n=3 training seeds；不推出 GU 效果 |
| 同一请求下 GU 相对 Retrain 的性能偏差随数据集/selector 改变 | AAGU-053 同 `selection_id` 的 GNNDelete/Retrain `utility.f1_after`，计算有符号 gap | 描述性支持 | 训练 seed 固定为 42；Degree 仅 1 个请求，其他 selector 各 3 个选点 seed |
| 更低的 GU 准确率代表遗忘更充分/更安全 | 当前准确率、Retrain gap、update-detection AUC | 证据不足 | 缺预测接近度/指定遗忘对象审计、隐私威胁模型和充分的 MIA 控制；不得作此结论 |
| D-full 与 Degree 的差异由结构杠杆等机制导致 | 当前选集交集与 Retrain 结果 | 证据不足 | 选集差异和结果差异不是因果机制证据；预筛 20% 范围当前未覆盖 |

### 定稿前的最小核验

1. 确认论文主指标是 accuracy、micro-F1 还是 macro-F1。若需要 macro-F1，从当前不可变 Output 与对应 test mask 重算指标并生成新的分析产物；不手改 Cache Artifact。
2. 若 053 需要论证对训练随机性的稳健性，为同一三数据集/10%/selector 范围补充独立训练 seed；现有三次 selector 抽样不能代替训练 seed。
3. 若主张隐私/MIA，补足明确攻击者知识、正负样本和控制设置，并将现有 posterior-change AUC 限定为所实现的检测器结果。
4. 当前 AAGU-032 没有对应的 GU outcome；若论文要把 D-full/Random 的 Retrain 发现延伸成 GU 攻击有效性，还需取得同请求、同预算下的 GU 端点。

## 三张数据集结果表

- [Cora 结果表](evidence/AAGU-032-AAGU-053-3000epoch-20260923/cora-3000-only-tables.md)
- [CiteSeer 结果表](evidence/AAGU-032-AAGU-053-3000epoch-20260923/citeseer-3000-only-tables.md)
- [PubMed 结果表](evidence/AAGU-032-AAGU-053-3000epoch-20260923/pubmed-3000-only-tables.md)

全矩阵复算文件与身份核验摘要在 `self/research/analyses/evidence/AAGU-032-AAGU-053-3000epoch-20260923/`：`analyze_current_only.py`、`summary-current-only.json`、AAGU-032 120 组 selector-budget 均值及配对对照 CSV、AAGU-053 48 对请求明细与 selector/dataset 汇总 CSV。
