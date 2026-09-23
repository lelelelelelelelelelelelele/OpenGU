# AAGU-062 六条件理论校准与验证约定

六个独立条件为 Cora/CiteSeer/PubMed × H16/H64。Work Plan AAGU-062 定义顺序与冻结门槛；每个参数组只绑定自己的 `(dataset, hidden)` checkpoint，不跨数据集或宽度迁移。

## 三步流程

1. **理论计算**：每个 `theory_hXX.yaml` 只声明 dataset/split、模型训练身份、checkpoint 和 GIF/IDEA，不预设 `scale/damp`。`experiments/aagu062_theory.py` 对该 checkpoint 的方法生产 sum-CE Hessian 做双起点 Lanczos，再按递推谱因子 `q(λ)=1-damp-λ/scale` 生成 `rho=0.8/0.5` 两组 proposal。有限 Ritz 范围只是估计，不证明全谱稳定。
2. **单请求 Observer 校准与冻结**：`experiments/aagu062_generate_candidates.py` 从该条件的理论 JSON 生成 GIF/IDEA 参数 YAML（T=100/200/400）和 `experiments/run.py` Observer 表。固定 Random seed 104245、10% train-mask 请求；关闭 GIF/IDEA GU 输出缓存。收集并校验 run/artifact SHA 后，独立运行 `experiments/aagu062_after_exp.py`。只有两组 proposal 均完整覆盖三个预算时，才按 Work Plan 门槛判断并从通过者里选最小 `mu=scale*damp`；不按 F1 选参。随后才创建多请求验证 YAML，固定 seeds 104246/104247/104248。
3. **六条件汇总**：AAGU-062 汇总每个条件与方法的 stable/unstable/inconclusive、冻结参数、checkpoint 与运行身份。单点校准通过只放行多请求验证，不代表所有 selector 已稳定或科研结论已接受。

Observer 冻结门槛：HVP probe/RHS/repeat 相对误差均有限且 <=1e-5；T=100/200/400 的 update 有限且 shifted relative residual <=1e-3；T=200/400 的更新范数相对 T=100 变化 <=1e-3；T=100 的 update/RHS 比值 >1e-6、原图同图 logits max-abs 变化 >1e-8。原系统残差单独报告，不作为正移位候选的同一门槛。

## 六条件输入和当前准备状态

| 条件 | 理论输入 | checkpoint 状态（SSH active checkout，2026-09-23） | 单点 Observer 表 |
| --- | --- | --- | --- |
| Cora H16 | `aagu065/theory_h16.yaml` | AAGU-063 seed42 PT 已核验；本轮已计算理论 proposal | `aagu065/observer_candidates_h16.yaml` |
| Cora H64 | `aagu065/theory_h64.yaml` | AAGU-063 seed42 PT 已核验；本轮已计算理论 proposal | `aagu065/observer_h64_calibration.yaml`（唯一 H64 表） |
| CiteSeer H16 | `aagu067/theory_h16.yaml` | 注册 PT 不在 SSH active checkout；待配方执行和核验 | checkpoint 到位并完成理论计算后生成 |
| CiteSeer H64 | `aagu067/theory_h64.yaml` | 注册 PT 不在 SSH active checkout；待配方执行和核验 | checkpoint 到位并完成理论计算后生成 |
| PubMed H16 | `aagu068/theory_h16.yaml` | 注册 PT 不在 SSH active checkout；待配方执行和核验 | checkpoint 到位并完成理论计算后生成 |
| PubMed H64 | `aagu068/theory_h64.yaml` | 注册 PT 不在 SSH active checkout；待配方执行和核验 | checkpoint 到位并完成理论计算后生成 |

`aagu067/paired_pt.yaml` 和 `aagu068/paired_pt.yaml` 是缺失 checkpoint 时的训练准备。CiteSeer/PubMed 当前不保留 author/shifted 固定候选表或单点 Observer aggregate；不得拿 Cora 参数代填。Cora 旧 author/shifted 和 H16 R2 方法 YAML 保留作历史来源，但不进入新的理论候选表。

`experiments/aagu062_after_exp.py` 读取已收集的 completed `run.json`、其可信 SHA-256 回执、同条件理论 JSON 和 Observer 文件。它仅输出分析报告，不改参数或创建下游验证表。
