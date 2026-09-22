# AAGU-062 六条件 Observer 配置约定

六个条件固定为 Cora/CiteSeer/PubMed × H16/H64。checkpoint 身份以 (dataset, hidden) 为键；每个条件的参数必须在自己的校准输出中选择，不能把 Cora 的值直接复制给 CiteSeer/PubMed，也不能在 H16/H64 间迁移。

## 三步流程

1. **理论候选与单请求校准**：先按 GIF/IDEA 原文与作者源码给出候选组，再用该条件的固定 checkpoint、Random seed 104245 和 10% 删除预算运行 observer_candidates_hXX.yaml。通用入口是 experiments/run.py，收集 linear_solver_trace、same_graph_change 和 hessian_calibration；被测 GIF/IDEA GU cache 关闭。Cora H16 增加既有 HVP 推导出的 R2 候选，要求用 Observer 复核；Cora H64 使用原有 12 个 author/shifted 候选 YAML。其他四个条件各自有 12 个 author/shifted 候选 YAML。
2. **冻结并验证**：只从同一条件的校准结果选出稳定参数。随后生成该条件的验证 YAML，让 unlearning_refs 精确指向校准时的两个选中参数文件；固定 Random seeds 104246、104247、104248。验证表不允许按 selector/seed 调参。验证 YAML 不能在校准前写入假定的最终参数，因此目前待第一步的 Observer 证据确认后补齐。
3. **汇总**：逐条件记录稳定/不稳定/证据不足、所选参数、checkpoint SHA、校准及验证运行身份；六个条件覆盖完成后由 AAGU-062 汇总，不把有限 seed 的结果外推为全谱或普遍保证。

## 六条件入口

| 条件 | PT/候选配置 | Observer 校准配置 |
| --- | --- | --- |
| Cora H16 | aagu065/gif_h16_*、idea_h16_*；PT 来自 AAGU-063 的 2-new-h16-seed42.pt | aagu065/observer_candidates_h16.yaml |
| Cora H64 | aagu065/gif_h64_*、idea_h64_*；PT 来自 AAGU-063 的 3-new-h64-seed42.pt | aagu065/observer_candidates_h64.yaml |
| CiteSeer H16 | aagu067/paired_pt.yaml 输出 0-new-h16-seed42.pt 及 H16 候选 | aagu067/observer_candidates_h16.yaml |
| CiteSeer H64 | aagu067/paired_pt.yaml 输出 1-new-h64-seed42.pt 及 H64 候选 | aagu067/observer_candidates_h64.yaml |
| PubMed H16 | aagu068/paired_pt.yaml 输出 0-new-h16-seed42.pt 及 H16 候选 | aagu068/observer_candidates_h16.yaml |
| PubMed H64 | aagu068/paired_pt.yaml 输出 1-new-h64-seed42.pt 及 H64 候选 | aagu068/observer_candidates_h64.yaml |

CiteSeer/PubMed 的 paired_pt.yaml 使用相应 persisted split、seed42、3000 epochs、Adam lr=0.05、weight_decay=0.0001，分别导出两个宽度的纯权重 PT。正式运行前仍需按实验 Runbook 在 SSH 核验数据、checkpoint 路径、代码与 SHA 身份。当前只定义配置，不启动训练或 GPU 实验。

The 12 Cora H64 candidate YAMLs named gif_h64_* and idea_h64_* are preserved as calibration definitions and are consumed by the new Observer aggregate. Historical YAMLs, reports, runs, and checkpoint artifacts are not deleted or overwritten.
