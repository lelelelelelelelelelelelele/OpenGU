# AAGU-009 · Legacy 入口退役与写回验证

## Human Result

### 实际增量

退役两个会删除或局部覆盖旧实验结果的 helper，移除旧分支残留的 120-cell 重跑 profile。保留已经有效的 GIF/IDEA 算法实现，把验证器升级为实际方法到 collateral/hop 消费者的检查，并将活动说明中的实验入口改指 027。

### 核心观察

40 项本地软件回归通过。GIF、IDEA 实际写回的参数与评估收到的参数一致，冻结参数不变；保留原源码和注释、仅在内存中去掉写回时，两种方法均被验证器拒绝。错误加载路径也会被拒绝。[软件验证回执](evidence/software-verification.json)

### 当前决定

> 当前验收决定：`待决定`

**建议接受 009 软件候选。** 由用户决定接受或返工；本次未启动正式实验，旧研究数值仍未恢复可信。SSH 准备、重跑、收集和研究证据验收继续由 027 承担。

## Legacy 清理范围

- `scripts/cleanup_if_family_collateral.py`：旧的原地删除入口已从候选移除。
- `scripts/redo_collateral_if_family.py`：旧的局部重算/覆盖入口已从候选移除，没有兼容 wrapper 或回退入口。
- 009 旧分支中的 `evidence/repair-scope.yaml`：不再保留为活动执行合同；历史在 Git 中。两份带日期的 baseline/preflight 记录保留，并在开头标明仅作历史观察。
- [L8 说明](../../../self/limitations.md#l8-hop-distance-decay-collateral-if-family-数值-bug-affected)和[研究路径说明](../../../self/research_path_degree_severity_decomposition.md)已取消旧命令，改为 009 软件验证、027 实验与证据、010 汇总的职责划分。

本次清理的是上述代码与执行入口。历史实验产物、真实缓存和既有归档均不在本次删除范围；带日期的历史审计/验收报告可以保留旧文件名，它们不构成当前执行入口。

## 行为观察

### 实际写回到评估消费者 — PASS

在固定 CPU 参数和三节点 fixture 中，直接调用当前 checkout 的 GIF/IDEA `approxi()`，用可控的 Hessian 替身隔离写回行为，不调用训练器或数据加载器。`AttackPipeline._get_trained_model()` 返回同一个已更新模型；实际 collateral/hop 计算与预期 fixture 参数一致，冻结参数保持不变。IDEA 的非零、确定性噪声均值也包含在评估与写回的同一组参数中。

对照 fixture 能区分旧权重与更新权重：旧权重在两个保留节点均预测不同，写回后与参考 fixture 一致。参考模型不是重训练实验产物，这个结果只证明软件链路正确，不是遗忘效果指标。[直接验证输出](evidence/writeback.txt)

### 缺失写回和错误来源能否被识别 — PASS

回归在内存中从实际方法移除写回语句，保留原文件字节和注释；验证器因模型保留旧权重而失败。另一个反例把预期来源设为其他 checkout，也被明确拒绝。这避免旧验证器“模拟代码正确、源码含标记就通过”的缺口。

### 局部回归和旧入口退役 — PASS

7 项本次回归与 33 项现有 attack/collateral 回归共 40 项通过，包含从仓库外目录直接启动验证器。两个旧 helper 和旧 profile 均不存在。生产 GIF/IDEA、模型抽取与指标算法相对纳入的 main 未改变。[回归日志](evidence/regression.txt)

## 验证身份与边界

完整软件检查运行于干净 checkpoint `fdbf2cd885d1e4902ae104a6d6258281c6792fef`。回执记录命令、退出码和所用源文件 SHA-256。随后只加入报告、验证记录和状态投影；最终干净候选、实际差异及复用依据由[最终验证回执](../../runtime/evidence/AAGU-009/final-verification.json)绑定。

本轮未访问 SSH、加载正式数据、训练模型、执行实验矩阵或收集结果。027 仍需按 001 框架形成当前批准的实验合同；历史 120 格不能直接作为新执行批准。测试环境的可选 CUDA 路径提示不影响这些 CPU fixture，也不证明 GPU 可用。

## 后续决定

接受对象是本报告所对应的 009 软件候选；接受后再按同一 WorkItem 进入 closeout。当前没有 Apply、push、安装、实验执行或历史 payload 清理的完成声明。
