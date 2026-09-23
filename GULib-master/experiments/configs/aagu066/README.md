# Cora H16/H64 冻结参数的多请求验证

`validation_h16.yaml` 与 `validation_h64.yaml` 分别绑定 AAGU-063 的 Cora seed42 纯权重。GIF/IDEA 参数取自 AAGU-065 对应宽度已通过单点 stable 门槛的 rho=0.8 候选，不跨宽度迁移、不按验证结果调参。冻结来源为 AAGU-065 的 `aagu065-cora-h16-theory-candidates-104245-v1` 和 `aagu065-cora-h64-theory-candidates-104245-v1`；执行版本为 `024e5a0de7ff3e6546f196524f3f64995adb7571`。

| 宽度 | 固定 PT SHA-256 | scale | damp（GIF / IDEA） |
| --- | --- | --- | --- |
| H16 | `9584b6bb8ca53532681a4fe9d4367709fd973d86d6884a3556b8c5614872cee3` | 8701 | 0.20028347851830353 / 0.2002834785183033 |
| H64 | `44632a12d39ced225c95fa8cfce15fe2a833e18625286fa3368a4495561fc399` | 9791 | 0.20098238047209782 |

正式参数由相邻方法 YAML 拥有。两张表固定 Random seeds 104246/104247/104248、10% train-mask 删除预算，执行 seed=42。生产预算固定 T=100，T=200/400 仅为预先指定的预算一致性诊断。每个宽度包含 3 请求 ×（GIF 三预算 + IDEA 三预算 + Retrain）=21 格；两宽度共42格。

Retrain 使用同宽度模型，Adam、3000 epochs、lr=0.05、weight_decay=0.0001，从头训练。固定 PT 方法的训练超参数不参与配对比较；执行 seed、模型、数据/split、Selection、删除语义及训练图/评价图仍严格匹配。此规则要求包含 `699f8fbf` 配对修复的执行版本。

GIF/IDEA GU 缓存禁用，checkpoint、Score、Selection 正常复用，Retrain 正常按精确身份复用。Observer 提供求解轨迹、HVP 检查及同图变化；`same_graph_change` 在 original 和 retained 图分别提供原 PT 不更新参照。

阶段门槛沿用 AAGU-062：HVP 相对误差≤1e-5；三个迭代预算的移位残差≤1e-3；T200/400 更新范数相对 T100 变化≤1e-3；T100 update/RHS>1e-6、原图 logits max-abs 变化>1e-8；要求有限性和完整覆盖。原系统残差另行报告，不以 F1 选参或要求优于 Retrain。全部预定请求与两个宽度的证据收集、身份校验及配对评价完成后，才判断阶段是否通过。

对应 Recipe 为 `scripts/syncmate/recipes/opengu-aagu066-cora-h16-frozen-validation-v1.yaml` 和 H64 同名配方。每份超时1800秒是执行上限，不是耗时预测；计数通过生成器从配置绑定的真实数据证据读取。配置或引用输入改变后须重新生成哈希。

`metrics_h16.template.yaml` 与 `metrics_h64.template.yaml` 是后续 Retrain-gap 模板，run/sha256 保留 null。可信回传后绑定真实 run.json 和 SHA-256，再生成 metrics Recipe；不伪造尚不存在的结果身份。

本次仅提交配置与 Recipe。正式启动仍须完成运行前估时、统一部署、三端版本一致与 preflight；提交本身不代表实验已经运行。
