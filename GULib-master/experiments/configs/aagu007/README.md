# AAGU-007 最小实验组合表

[experiment.yaml](experiment.yaml) 已改为引用公共小表：Cora/70-10-20 split seed2024、Degree1%、训练 seeds122/722、独立 GNNDelete与Retrain，共4个方法输出。公共默认模型为GCN两层hidden64；训练100 epochs、Adam lr0.005、weight_decay1e-6；GNNDelete遗忘50 epochs、lr0.01、alpha0.5。

当前软件登记为 `opengu-aagu007-v1`，入口由 SyncMate 调用 `experiments/run.py --recipe opengu-aagu007-v1`；注册绑定组合表及全部公共引用的指纹、运行身份、1800秒超时和17个导出文件。它不创建运行许可，真实实验仍须按 [007 WorkItem](../../../.workblock/items/AAGU-007/WORKITEM.md) 审阅和批准，并满足034接受前置。

Degree不消费训练seed，四个方法输出共享其真实Selection。既有Score/Selection是否HIT，以实际Result中的精确身份与producer记录为准。预测不转化为强制HIT或禁止合法MISS的开关。

后续Metrics用公共retrain-gap小表及实际已完成Output引用单独登记；当前没有本轮Output，不预填引用，也不运行比较。旧逐seed配置已删除；先前审阅稿仍在007 WorkItem中作为历史方案材料。
