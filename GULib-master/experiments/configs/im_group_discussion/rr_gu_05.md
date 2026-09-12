# AAGU-053：5% RR 跨GU比较

入口：[rr_gu_05.yaml](rr_gu_05.yaml)。2026-09-13用户提出继续推进IM跨GU实验与论文，新增此表；当前步骤为建立和校验配置，未完成Core登记或正式派发。

沿用5% RR检查的大表条件：Cora/CiteSeer/PubMed、train候选池5%、传播概率0.1、RR-1024/4096/16384和IM seeds11/22/33。另加Degree确定性选集和Random十选集（11/22/33/44/55/66/77/88/99/104245），所有训练固定seed42。

每数据集20个删除请求，共60请求；各请求使用GNNDelete、MEGU、GraphEraser、GraphRevoker、Retrain，共300格、240个GU–Retrain配对。GIF、IDEA和CELF不在本表。

## 实施与证据

- [rr_sufficiency_05.yaml](rr_sufficiency_05.yaml)拥有27个RR选点条件；本表使用完全相同的小表与预算/seed。实际Selection身份仍需运行时核对，不把dry-run当作HIT证明。
- 各方法使用同一请求选集；5%的Random十选集基线在本表明确计算/合法复用，不能直接拿051的10%基线代替。
- 采样诊断与GU效果分别报告。发现覆盖饱和时公开零增益补齐限制，不把固定RR实验升级为充分采样或理论保证。
- 正式运行前完成Core登记、SHA/数据/图split身份检查与代表性gate；实际只计算缓存MISS，保留旧结果。

## 论文问题与边界

问题：传播覆盖驱动的删除选集是否在不同GU实现中产生不同于Degree/Random的效用响应？

主指标固定原图、测试节点和标签：各GU自身before/after与有符号变化、同预算IM相对Random差异、同选集Retrain F1及GU–Retrain差距。报告每个selector seed结果与样本SD；训练seed固定，不能冒称训练稳健性或自动宣称统计显著。

GraphEraser/GraphRevoker使用自身ensemble before；与普通GCN Retrain的差距包含架构/聚合影响，不能称纯遗忘误差。F1不证明遗忘正确性。GIF/IDEA未纳入是当前方法验证边界，不能声称被全部GU普遍验证。保留弱效果和负结果，不根据结果筛选数据集或RR参数。
