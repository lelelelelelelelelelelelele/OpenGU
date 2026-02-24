# 自动实验汇报（追加）

该文件由实验脚本自动追加写入，用于记录每个任务的执行结果与下一步动作。

### [2026-02-16 12:23:20] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=10.73s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=10.37s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 12:23:31] run_ratio05.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:11] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=28.11s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:39] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=10.70s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:06:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=25.04s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:07:15] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:25] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=129.71s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:09:25] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:25] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:25] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:25] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:36] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.27s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 16:09:36] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=12.04s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:09:48] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=11.59s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=10.72s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:10] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=10.31s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:21] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=10.61s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:31] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：OK | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=27.63s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:10:59] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 16:11:39] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=40.25s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:12:17] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=37.61s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:12:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=35.39s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:13:33] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=40.27s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:14:10] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=37.90s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:14:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=32.82s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:15:16] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=32.32s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:15:27] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=11.19s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:15:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=11.13s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:15:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=11.19s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:16:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=11.04s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:16:11] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=11.10s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:16:22] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=11.23s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:16:33] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=10.97s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:16:59] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=25.40s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:17:26] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=27.41s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:17:55] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=28.38s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:18:26] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=30.83s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:18:59] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=33.37s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:19:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=30.22s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:19:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=27.38s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 16:39:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 16:59:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 17:19:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 17:39:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.01s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 17:59:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:06:51] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.55s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:07:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:19:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 18:20:10] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.36s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:20:25] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.16s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:20:39] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.15s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:20:54] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.95s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:21:07] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.03s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:21:19] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.24s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:21:35] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.28s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:21:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.84s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:22:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.27s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:22:17] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=15.16s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:22:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.41s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:22:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.20s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:23:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=18.51s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:23:15] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.98s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:23:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.40s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:23:42] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.15s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:23:56] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.30s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:24:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.21s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:24:16] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.40s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:24:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.40s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:24:41] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.23s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:24:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.26s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:25:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.23s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:25:17] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.27s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:25:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.44s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:25:41] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.39s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:25:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.28s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:26:04] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.36s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:26:18] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.34s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:26:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.33s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:26:44] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.08s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:26:55] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.36s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 18:27:14] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=19.10s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:24] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=19.15s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=4.38s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=0.32s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.04s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:27:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.88s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:35:36] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=485.26s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:35:37] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=485.95s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:36:09] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=33.06s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:36:10] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=32.97s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.92 GiB is free. Of the allocated memory 49.22 MiB is allocated by PyTorch, and 2.78 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:36:22] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.87s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:36:25] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=15.57s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:36:37] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.46s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:36:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=0.6066 | f1_after=0.7538 | auc=NA | unlearn_time=NA | wall_time=34.82s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:37:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=24.20s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:37:12] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.56s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:37:13] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=15.97s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:37:26] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.88s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:37:40] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=0.6036 | f1_after=0.7538 | auc=NA | unlearn_time=NA | wall_time=26.61s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:37:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=17.15s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:37:55] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.80s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:38:15] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=0.5976 | f1_after=0.7538 | auc=NA | unlearn_time=NA | wall_time=35.31s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:38:18] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=22.88s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:38:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.56s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:38:51] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=0.5931 | f1_after=0.7538 | auc=NA | unlearn_time=NA | wall_time=36.24s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:38:54] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=23.66s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:39:14] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=23.39s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:39:15] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=21.15s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUBLAS_STATUS_ALLOC_FAILED when calling `cublasCreate(handle)`
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:39:42] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=28.00s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 35.7 MiB for an array with shape (18717, 500) and data type float32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:39:44] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=28.59s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:39:54] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.60s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:39:55] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.91s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.34s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:07] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.85s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:21] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.52s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:22] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.98s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:33] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.05s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:35] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=12.92s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:40:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.78s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:46] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=10.88s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:40:55] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.87s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:40:57] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=10.94s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:41:13] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.52s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:41:15] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=19.83s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:41:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.48s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:41:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=15.48s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:41:39] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=11.74s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:41:40] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.96s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:41:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.61s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:41:55] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=15.28s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:42:08] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.34s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:42:09] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=16.04s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:42:22] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.42s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:42:25] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=17.16s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:42:36] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.42s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:42:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=15.13s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:43:10] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=32.83s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:43:11] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=35.00s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:43:25] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.91s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:43:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=19.92s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:43:39] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=14.11s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:43:46] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.50s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:43:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=13.26s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:44:00] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.65s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:44:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=12.75s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:44:15] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.81s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:44:18] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=12.08s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:44:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.13s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:44:34] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=16.13s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:44:44] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=10.37s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:44:49] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=18.15s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1555040356 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:44:56] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=12.18s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:45:08] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.65s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:45:20] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.71s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:45:32] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.55s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:45:42] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.38s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:45:51] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.38s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.36s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:11] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.34s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:20] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.49s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:29] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.26s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:43] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.31s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:46:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.22s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.16s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:13] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.12s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:22] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.06s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.08s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:47:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:47:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.15s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:47:50] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.25s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:47:50] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-16 18:47:59] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.37s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.73s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.02s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.13s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:37] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.95s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.23s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:48:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.14s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.11s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:15] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.08s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.07s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.00s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.94s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:49:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.16s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:02] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.02s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.07s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:21] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.97s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.99s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:40] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.93s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:49] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.91s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:50:58] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.96s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:07] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.97s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.15s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.99s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:35] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.98s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:45] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.93s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:51:54] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.89s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:03] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.96s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.94s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:21] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.11s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.97s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:39] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.04s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:52:50] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.15s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:53:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.28s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:53:13] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.41s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:53:46] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=32.91s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 1418368 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:53:58] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.00s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:54:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=19.53s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:54:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.92s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:54:35] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.00s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:54:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.98s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:54:55] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=10.93s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:55:07] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.16s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:55:25] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=18.03s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: CUDA-capable device(s) is/are busy or unavailable
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:55:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.88s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:55:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=18.18s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:56:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.76s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:57:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=103.79s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:58:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.06s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 1.35 MiB for an array with shape (177296,) and data type int64
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:58:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=38.10s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 28.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.82 GiB is free. Of the allocated memory 129.78 MiB is allocated by PyTorch, and 20.22 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:59:22] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=38.38s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 28.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.82 GiB is free. Of the allocated memory 129.28 MiB is allocated by PyTorch, and 20.72 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:59:32] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.40s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:59:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.24s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:59:50] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.03s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 18:59:59] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.14s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:00:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.27s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:00:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.28s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:00:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.17s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 949. MiB for an array with shape (15773, 15773) and data type int32
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:04:50] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-16 19:05:03] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.24s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:05:33] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=29.72s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:06:10] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=37.20s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 168.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.71 GiB is free. Of the allocated memory 233.41 MiB is allocated by PyTorch, and 26.59 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:07:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=94.63s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.61 GiB is free. Of the allocated memory 328.46 MiB is allocated by PyTorch, and 33.54 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:09:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=94.01s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.61 GiB is free. Of the allocated memory 326.60 MiB is allocated by PyTorch, and 33.40 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:10:32] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=73.67s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.57 GiB is free. Of the allocated memory 369.47 MiB is allocated by PyTorch, and 36.53 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:10:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.4359 | wall_time=12.42s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:10:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.4316 | wall_time=11.69s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:11:08] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4628 | wall_time=12.00s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:11:20] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4853 | wall_time=12.17s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:11:37] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=16.60s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:12:10] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=33.17s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 148.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.63 GiB is free. Of the allocated memory 296.31 MiB is allocated by PyTorch, and 41.69 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:12:42] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=32.06s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 378.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.78 GiB is free. Of the allocated memory 157.14 MiB is allocated by PyTorch, and 28.86 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:13:21] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=38.56s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 38.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.62 GiB is free. Of the allocated memory 328.07 MiB is allocated by PyTorch, and 19.93 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:14:15] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=54.29s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:14:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8504 | auc=0.0000 | unlearn_time=0.3116 | wall_time=11.66s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:14:58] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=30.75s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:15:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8463 | auc=0.0000 | unlearn_time=0.3050 | wall_time=11.91s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:15:23] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.69s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:15:35] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8289 | auc=0.0000 | unlearn_time=0.3255 | wall_time=11.97s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:16:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=30.39s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:16:36] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=30.84s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:17:02] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=26.06s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:17:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=31.21s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:18:04] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=30.17s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:18:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=30.15s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:19:05] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=31.21s
- 异常与定位：CUDA_OOM: torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 1.45 GiB. GPU 0 has a total capacity of 6.00 GiB of which 4.94 GiB is free. Of the allocated memory 40.79 MiB is allocated by PyTorch, and 19.21 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:19:16] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8542 | f1_after=0.8542 | auc=0.0000 | unlearn_time=0.6030 | wall_time=10.66s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:19:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8545 | f1_after=0.8545 | auc=0.0000 | unlearn_time=0.6497 | wall_time=9.87s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:19:36] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.5865 | wall_time=9.82s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:19:46] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.6300 | wall_time=9.93s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:19:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8560 | f1_after=0.8578 | auc=0.0000 | unlearn_time=0.6390 | wall_time=9.98s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8567 | f1_after=0.8567 | auc=0.0000 | unlearn_time=0.6657 | wall_time=10.17s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:16] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8562 | f1_after=0.8562 | auc=0.0000 | unlearn_time=0.6566 | wall_time=10.34s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8626 | auc=0.4667 | unlearn_time=0.4036 | wall_time=9.91s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:36] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8626 | auc=0.4556 | unlearn_time=0.4508 | wall_time=9.70s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:45] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8618 | auc=0.4494 | unlearn_time=0.3956 | wall_time=9.54s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:20:55] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8588 | auc=0.4835 | unlearn_time=0.3891 | wall_time=9.56s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:21:04] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8552 | auc=0.4761 | unlearn_time=0.4364 | wall_time=9.69s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:21:14] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8499 | auc=0.4853 | unlearn_time=0.4139 | wall_time=9.61s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:21:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8349 | auc=0.4853 | unlearn_time=0.4381 | wall_time=9.94s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 19:22:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=0.8223 | f1_after=0.8611 | auc=NA | unlearn_time=NA | wall_time=36.60s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:22:39] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=0.8223 | f1_after=0.8611 | auc=NA | unlearn_time=NA | wall_time=38.17s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:23:15] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=0.8223 | f1_after=0.8611 | auc=NA | unlearn_time=NA | wall_time=36.57s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:23:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=0.8223 | f1_after=0.8611 | auc=NA | unlearn_time=NA | wall_time=37.37s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 1.35 MiB for an array with shape (177296,) and data type int64
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:24:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=0.8223 | f1_after=0.8611 | auc=NA | unlearn_time=NA | wall_time=37.85s
- 异常与定位：ValueError: ValueError: I/O operation on closed file.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:24:59] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=27.86s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221226505
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-16 19:25:07] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.38s
- 异常与定位：TRACEBACK_ERROR: numpy.core._exceptions.MemoryError: Unable to allocate 237. MiB for an array with shape (15773, 15773) and data type bool
- 下一步建议：打开日志定位根因并重跑该配置。

---
## Session 2026-02-17-1

### [2026-02-17 00:00] DECISION — Journal 系统升级至 v2
- 背景：现有 journal 仅记录实验执行结果，缺少研究过程中的决策记录，导致 flow.md 与 daily_log 之间存在断裂。
- 选项：A: RULES.md v2 双条目（实验+决策）原地扩展 / B: 新建独立 decisions.md 文件
- 选择：A — 保持单一 journal 文件，避免记录分散，降低维护成本。
- 影响：RULES.md 追加 v2 段落，CLAUDE.md 追加 Document Workflow，daily-log 命令增加关键决策章节。
- 关联 Step：N/A

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:14:52] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.19s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:04] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7252 | auc=0.9609 | unlearn_time=0.7036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7357 | auc=0.8871 | unlearn_time=0.6798 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7237 | auc=0.8477 | unlearn_time=0.7515 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:15:32] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.6997 | auc=0.7489 | unlearn_time=0.8072 | wall_time=27.38s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:15:46] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7207 | auc=0.6732 | unlearn_time=0.6273 | wall_time=14.34s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:34:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7237 | auc=0.6054 | unlearn_time=0.6533 | wall_time=1146.36s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=0.7327 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.67s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [3326, 2329]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 02:35:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:35:13] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5031 | wall_time=10.13s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:13] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:35:23] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7402 | auc=0.0000 | unlearn_time=0.4673 | wall_time=10.12s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:33] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7432 | auc=0.0000 | unlearn_time=0.4680 | wall_time=10.15s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:33] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:35:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.4733 | wall_time=10.38s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:35:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7237 | auc=0.0000 | unlearn_time=0.2930 | wall_time=9.48s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:35:53] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7192 | auc=0.0000 | unlearn_time=0.2831 | wall_time=9.52s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:12] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7147 | auc=0.0000 | unlearn_time=0.2726 | wall_time=9.69s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:21] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.6997 | auc=0.0000 | unlearn_time=0.2802 | wall_time=9.55s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.3883 | wall_time=9.38s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:31] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:40] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7447 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.3897 | wall_time=9.37s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.4005 | wall_time=9.40s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:36:59] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.7402 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.5111 | wall_time=9.47s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:36:59] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:09] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4951 | wall_time=9.41s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:37:09] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:18] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5431 | wall_time=9.75s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5117 | wall_time=9.49s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:37:37] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.6952 | auc=0.5641 | unlearn_time=0.3277 | wall_time=9.31s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:38:02] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：OK | f1_before=0.6081 | f1_after=0.7492 | auc=0.0000 | unlearn_time=5.7828 | wall_time=24.60s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:38:28] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：OK | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=6.0132 | wall_time=26.00s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:38:55] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：OK | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=7.4315 | wall_time=27.63s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:39:22] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：OK | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=6.6765 | wall_time=26.44s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:39:48] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：OK | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=6.7701 | wall_time=26.48s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:40:16] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：OK | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=7.3728 | wall_time=27.90s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:40:47] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=9.3448 | wall_time=30.51s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:41:43] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=11.2691 | wall_time=55.73s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:42:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=11.3707 | wall_time=55.28s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:43:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=12.1174 | wall_time=55.92s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:44:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=12.1369 | wall_time=56.58s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:45:22] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=9.9784 | wall_time=51.67s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:46:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=9.4838 | wall_time=47.34s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:46:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=9.4326 | wall_time=46.90s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:46:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:46:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:47:07] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8575 | auc=0.5834 | unlearn_time=0.4138 | wall_time=10.66s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:47:07] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:47:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8517 | auc=0.5938 | unlearn_time=0.4177 | wall_time=10.83s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:47:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 02:47:28] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8327 | auc=0.4955 | unlearn_time=0.4128 | wall_time=10.54s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:49:51] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=29.8813 | wall_time=142.13s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:52:09] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=28.6163 | wall_time=137.97s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:54:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.0762 | wall_time=138.78s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:56:57] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.4255 | wall_time=150.02s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 02:59:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=27.2901 | wall_time=134.81s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 03:01:18] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=24.8392 | wall_time=126.11s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 03:03:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=20.4457 | wall_time=120.72s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 03:23:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.06s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 03:43:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 04:03:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 04:23:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.02s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:20] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.69s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7252 | auc=0.9609 | unlearn_time=0.6591 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7357 | auc=0.8871 | unlearn_time=0.6798 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7237 | auc=0.8477 | unlearn_time=0.7515 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.7492 | unlearn_time=0.7564 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.6732 | unlearn_time=0.6273 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:29] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.6054 | unlearn_time=0.6533 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=0.7327 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.86s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [3326, 2329]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5031 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7402 | auc=0.0000 | unlearn_time=0.4673 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7432 | auc=0.0000 | unlearn_time=0.4680 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.4733 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.0000 | unlearn_time=0.2930 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7192 | auc=0.0000 | unlearn_time=0.2831 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.0000 | unlearn_time=0.2726 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.0000 | unlearn_time=0.2802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.3883 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7447 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.3897 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.4005 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.5111 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4951 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5431 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5117 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6952 | auc=0.5641 | unlearn_time=0.3277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6081 | f1_after=0.7492 | auc=0.0000 | unlearn_time=5.7828 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=6.0132 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=7.4315 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=6.6765 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=6.7701 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=7.3728 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=9.3448 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=11.2691 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=11.3707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=12.1174 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=12.1369 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=9.9784 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=9.4838 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=9.4326 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8575 | auc=0.5834 | unlearn_time=0.4138 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8517 | auc=0.5938 | unlearn_time=0.4177 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8327 | auc=0.4955 | unlearn_time=0.4128 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=29.8813 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=28.6163 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.0762 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.4255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=27.2901 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=24.8392 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:38:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=20.4457 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 04:43:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 04:58:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 04:59:48] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=70.15s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:03:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.03s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 05:05:10] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=322.18s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:05:19] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.30s
- 异常与定位：TRACEBACK_ERROR: Traceback detected
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:16:55] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=696.64s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:34:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1077.78s
- 异常与定位：RuntimeError: RuntimeError: [enforce fail at alloc_cpu.cpp:114] data. DefaultCPUAllocator: not enough memory: you tried to allocate 898080 bytes.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:35:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.69s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:35:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.4359 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:35:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.4316 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:35:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4628 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:35:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4853 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:35:22] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4649 | wall_time=15.55s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:35:34] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4405 | wall_time=12.03s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:36:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=43.83s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:36:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8489 | auc=0.0000 | unlearn_time=0.3265 | wall_time=12.43s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:36:40] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8507 | auc=0.0000 | unlearn_time=0.3505 | wall_time=10.47s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:36:40] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8504 | auc=0.0000 | unlearn_time=0.3116 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:36:51] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8471 | auc=0.0000 | unlearn_time=0.3036 | wall_time=10.72s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:36:51] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8463 | auc=0.0000 | unlearn_time=0.3050 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:37:02] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8436 | auc=0.0000 | unlearn_time=0.3121 | wall_time=10.85s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:37:02] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8289 | auc=0.0000 | unlearn_time=0.3255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:37:13] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.22s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:37:38] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=25.25s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:37:48] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=9.97s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=18.03s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:38:21] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=14.94s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:38:33] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.13s
- 异常与定位：CUDA_OOM: RuntimeError: CUDA error: out of memory
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.02s
- 异常与定位：RuntimeError: RuntimeError: CUDA error: unknown error
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8542 | f1_after=0.8542 | auc=0.0000 | unlearn_time=0.6030 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8545 | f1_after=0.8545 | auc=0.0000 | unlearn_time=0.6497 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.5865 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.6300 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8560 | f1_after=0.8578 | auc=0.0000 | unlearn_time=0.6390 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8567 | f1_after=0.8567 | auc=0.0000 | unlearn_time=0.6657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8562 | f1_after=0.8562 | auc=0.0000 | unlearn_time=0.6566 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4667 | unlearn_time=0.4036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4556 | unlearn_time=0.4508 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8618 | auc=0.4494 | unlearn_time=0.3956 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8588 | auc=0.4835 | unlearn_time=0.3891 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8552 | auc=0.4761 | unlearn_time=0.4364 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8499 | auc=0.4853 | unlearn_time=0.4139 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:38:47] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8349 | auc=0.4853 | unlearn_time=0.4381 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 05:39:29] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.2934 | wall_time=42.54s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:40:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=9.4887 | wall_time=43.29s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:40:56] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.5290 | wall_time=43.04s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:41:39] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.6590 | wall_time=43.10s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:42:22] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.5873 | wall_time=43.25s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:43:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=8.7754 | wall_time=43.71s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 05:43:49] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=8.5781 | wall_time=43.14s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:34] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.63s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7252 | auc=0.9609 | unlearn_time=0.6591 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7357 | auc=0.8871 | unlearn_time=0.6798 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7237 | auc=0.8477 | unlearn_time=0.7515 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.7492 | unlearn_time=0.7564 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.6732 | unlearn_time=0.6273 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:43] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.6054 | unlearn_time=0.6533 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=0.7327 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=8.91s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [3326, 2329]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5031 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7402 | auc=0.0000 | unlearn_time=0.4673 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7432 | auc=0.0000 | unlearn_time=0.4680 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.4733 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.0000 | unlearn_time=0.2930 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7192 | auc=0.0000 | unlearn_time=0.2831 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.0000 | unlearn_time=0.2726 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.0000 | unlearn_time=0.2802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.3883 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7447 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.3897 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.4005 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.5111 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4951 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5431 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5117 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6952 | auc=0.5641 | unlearn_time=0.3277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6081 | f1_after=0.7492 | auc=0.0000 | unlearn_time=5.7828 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=6.0132 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=7.4315 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=6.6765 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=6.7701 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=7.3728 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=9.3448 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=11.2691 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=11.3707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=12.1174 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=12.1369 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=9.9784 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=9.4838 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=9.4326 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8575 | auc=0.5834 | unlearn_time=0.4138 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8517 | auc=0.5938 | unlearn_time=0.4177 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8327 | auc=0.4955 | unlearn_time=0.4128 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=29.8813 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=28.6163 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.0762 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.4255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=27.2901 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=24.8392 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:02:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=20.4457 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:22:53] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：TIMEOUT | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.08s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。

### [2026-02-17 06:23:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.81s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:20] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=13.27s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=5.78s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:29] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=3.79s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:36] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=6.83s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=7.83s
- 异常与定位：OSError: OSError: [WinError 1455] 页面文件太小，无法完成操作。 Error loading "H:\conda_package\envs\gnn\lib\site-packages\torch\lib\torch_python.dll" or one of its dependencies.
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.4359 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.4316 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4628 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4853 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4649 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:23:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4405 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=102.51s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8489 | auc=0.0000 | unlearn_time=0.3265 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8507 | auc=0.0000 | unlearn_time=0.3505 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8504 | auc=0.0000 | unlearn_time=0.3116 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8471 | auc=0.0000 | unlearn_time=0.3036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8463 | auc=0.0000 | unlearn_time=0.3050 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8436 | auc=0.0000 | unlearn_time=0.3121 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:27] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8289 | auc=0.0000 | unlearn_time=0.3255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:29] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.44s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:31] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.05s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:33] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.10s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:35] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.02s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:37] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.03s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:39] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.03s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=2.03s
- 异常与定位：RETURN_CODE_NONZERO: returncode=3221225477
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8542 | f1_after=0.8542 | auc=0.0000 | unlearn_time=0.6030 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8545 | f1_after=0.8545 | auc=0.0000 | unlearn_time=0.6497 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.5865 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.6300 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8560 | f1_after=0.8578 | auc=0.0000 | unlearn_time=0.6390 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8567 | f1_after=0.8567 | auc=0.0000 | unlearn_time=0.6657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8562 | f1_after=0.8562 | auc=0.0000 | unlearn_time=0.6566 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4667 | unlearn_time=0.4036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4556 | unlearn_time=0.4508 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8618 | auc=0.4494 | unlearn_time=0.3956 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8588 | auc=0.4835 | unlearn_time=0.3891 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8552 | auc=0.4761 | unlearn_time=0.4364 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8499 | auc=0.4853 | unlearn_time=0.4139 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8349 | auc=0.4853 | unlearn_time=0.4381 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.2934 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=9.4887 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.5290 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.6590 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.5873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=8.7754 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 06:25:41] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=8.5781 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:37] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：X | f1_before=0.8838 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.87s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [2708, 1896]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7252 | auc=0.9609 | unlearn_time=0.6591 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7357 | auc=0.8871 | unlearn_time=0.6798 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7237 | auc=0.8477 | unlearn_time=0.7515 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.7492 | unlearn_time=0.7564 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.6732 | unlearn_time=0.6273 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:28:49] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.6054 | unlearn_time=0.6533 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：X | f1_before=0.7327 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=11.26s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [3326, 2329]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5031 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7402 | auc=0.0000 | unlearn_time=0.4673 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7432 | auc=0.0000 | unlearn_time=0.4680 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.4733 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.0000 | unlearn_time=0.2930 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7192 | auc=0.0000 | unlearn_time=0.2831 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.0000 | unlearn_time=0.2726 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.0000 | unlearn_time=0.2802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.3883 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:00] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7447 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.3897 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.4005 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.5111 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4951 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5431 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5117 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6952 | auc=0.5641 | unlearn_time=0.3277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6081 | f1_after=0.7492 | auc=0.0000 | unlearn_time=5.7828 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=6.0132 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=7.4315 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=6.6765 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=6.7701 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=7.3728 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=9.3448 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=11.2691 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=11.3707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=12.1174 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=12.1369 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=9.9784 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=9.4838 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=9.4326 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8575 | auc=0.5834 | unlearn_time=0.4138 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8517 | auc=0.5938 | unlearn_time=0.4177 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8327 | auc=0.4955 | unlearn_time=0.4128 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=29.8813 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=28.6163 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.0762 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.4255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=27.2901 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=24.8392 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=20.4457 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=2026.0000 | auc=0.8543 | unlearn_time=0.7840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:29:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8479 | auc=0.6647 | unlearn_time=0.8769 | wall_time=15.76s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:29:35] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8258 | auc=0.6738 | unlearn_time=1.0665 | wall_time=18.51s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:29:52] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.7809 | auc=0.5314 | unlearn_time=0.9794 | wall_time=16.82s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:30:44] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8045 | auc=0.5071 | unlearn_time=0.8011 | wall_time=51.96s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:31:00] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.7863 | auc=0.4978 | unlearn_time=0.8309 | wall_time=16.08s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=0.8628 | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=12.41s
- 异常与定位：MIA_LENGTH_MISMATCH: ValueError: Found input variables with inconsistent numbers of samples: [19716, 13802]
- 下一步建议：打开日志定位根因并重跑该配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.4359 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.4316 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4628 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4853 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4649 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:12] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4405 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.5685 | wall_time=13.57s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8489 | auc=0.0000 | unlearn_time=0.3265 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8507 | auc=0.0000 | unlearn_time=0.3505 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8504 | auc=0.0000 | unlearn_time=0.3116 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8471 | auc=0.0000 | unlearn_time=0.3036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8463 | auc=0.0000 | unlearn_time=0.3050 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8436 | auc=0.0000 | unlearn_time=0.3121 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:26] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8289 | auc=0.0000 | unlearn_time=0.3255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:31:42] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：OK | f1_before=0.8633 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.6851 | wall_time=15.52s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:31:58] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：OK | f1_before=0.8631 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.6306 | wall_time=16.65s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:32:14] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：OK | f1_before=0.8626 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.6521 | wall_time=15.54s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:32:30] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：OK | f1_before=0.8631 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.6293 | wall_time=15.88s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:32:45] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：OK | f1_before=0.8623 | f1_after=0.8623 | auc=0.0000 | unlearn_time=0.6253 | wall_time=15.28s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:33:01] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：OK | f1_before=0.8603 | f1_after=0.8603 | auc=0.0000 | unlearn_time=0.6749 | wall_time=15.53s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8585 | f1_after=0.8585 | auc=0.0000 | unlearn_time=0.7050 | wall_time=16.50s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8542 | f1_after=0.8542 | auc=0.0000 | unlearn_time=0.6030 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8545 | f1_after=0.8545 | auc=0.0000 | unlearn_time=0.6497 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.5865 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.6300 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8560 | f1_after=0.8578 | auc=0.0000 | unlearn_time=0.6390 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8567 | f1_after=0.8567 | auc=0.0000 | unlearn_time=0.6657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8562 | f1_after=0.8562 | auc=0.0000 | unlearn_time=0.6566 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4667 | unlearn_time=0.4036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4556 | unlearn_time=0.4508 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8618 | auc=0.4494 | unlearn_time=0.3956 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8588 | auc=0.4835 | unlearn_time=0.3891 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8552 | auc=0.4761 | unlearn_time=0.4364 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8499 | auc=0.4853 | unlearn_time=0.4139 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8349 | auc=0.4853 | unlearn_time=0.4381 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.2934 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=9.4887 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.5290 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.6590 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.5873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=8.7754 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:33:17] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=8.5781 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=7.0514 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphEraser_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.5187 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=9.4971 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.2095 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=8.5609 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphEraser_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.5277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphEraser_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=9.2871 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.8166 | unlearn_time=0.3873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GIF_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.7401 | unlearn_time=0.3537 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.6389 | unlearn_time=0.4064 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8764 | auc=0.6097 | unlearn_time=0.3683 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.5896 | unlearn_time=0.3851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GIF_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8579 | auc=0.5194 | unlearn_time=0.3972 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GIF_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.9153 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUIDE_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1257 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.7550 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.5220 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=8.2720 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUIDE_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=7.1983 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUIDE_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8303 | auc=0.9853 | unlearn_time=5.6250 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8303 | auc=0.9704 | unlearn_time=0.6484 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8598 | auc=0.9877 | unlearn_time=0.6886 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7989 | auc=0.7630 | unlearn_time=0.9970 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7934 | auc=0.6071 | unlearn_time=0.7755 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8155 | auc=0.6045 | unlearn_time=0.6875 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:24] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GNNDelete_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.7472 | auc=0.5476 | unlearn_time=0.8529 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GNNDelete_GCN_cora_r0.5.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.7472 | auc=0.5150 | unlearn_time=1.1425 | wall_time=24.87s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6376 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\SGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.7173 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.6418 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6229 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8893 | auc=0.0000 | unlearn_time=0.6363 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\SGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8838 | auc=0.0000 | unlearn_time=0.6408 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\SGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8875 | auc=0.0000 | unlearn_time=0.5845 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8801 | auc=0.0000 | unlearn_time=0.4021 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\MEGU_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8782 | auc=0.0000 | unlearn_time=0.3578 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3498 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8745 | auc=0.0000 | unlearn_time=0.3925 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\MEGU_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8616 | auc=0.0000 | unlearn_time=0.3433 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\MEGU_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8229 | auc=0.0000 | unlearn_time=0.3802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4817 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GUKD_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4212 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.5007 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8875 | f1_after=0.9022 | auc=0.0000 | unlearn_time=0.4869 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GUKD_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8985 | auc=0.0000 | unlearn_time=0.4889 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GUKD_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8635 | f1_after=0.8856 | auc=0.0000 | unlearn_time=0.4244 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7600 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\D2DGN_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8911 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.5802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8893 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.7818 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8948 | f1_after=0.8967 | auc=0.0000 | unlearn_time=0.6963 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8967 | f1_after=0.9004 | auc=0.0000 | unlearn_time=0.6380 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\D2DGN_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8930 | f1_after=0.8930 | auc=0.0000 | unlearn_time=0.6541 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\D2DGN_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8948 | auc=0.0000 | unlearn_time=0.6639 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6213 | unlearn_time=0.4633 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\IDEA_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6310 | unlearn_time=0.4067 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.6043 | unlearn_time=0.4879 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8653 | auc=0.5748 | unlearn_time=0.4688 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8635 | auc=0.5375 | unlearn_time=0.4424 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\IDEA_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8450 | auc=0.5312 | unlearn_time=0.4413 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\IDEA_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.8838 | f1_after=0.8339 | auc=0.5307 | unlearn_time=0.4010 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.005.log`
- 执行结果：SKIP | f1_before=0.7269 | f1_after=0.8413 | auc=0.0000 | unlearn_time=8.3839 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:49] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\cora\GraphRevoker_GCN_cora_r0.01.log`
- 执行结果：SKIP | f1_before=0.7048 | f1_after=0.8506 | auc=0.0000 | unlearn_time=7.3945 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.02.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8487 | auc=0.0000 | unlearn_time=10.2225 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.05.log`
- 执行结果：SKIP | f1_before=0.7103 | f1_after=0.8413 | auc=0.0000 | unlearn_time=9.9554 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.1.log`
- 执行结果：SKIP | f1_before=0.7085 | f1_after=0.8358 | auc=0.0000 | unlearn_time=10.6127 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\round2_logs\GraphRevoker_GCN_cora_r0.2.log`
- 执行结果：SKIP | f1_before=0.6974 | f1_after=0.8247 | auc=0.0000 | unlearn_time=9.6158 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\ratio05_logs\GraphRevoker_GCN_cora_r0.5.log`
- 执行结果：SKIP | f1_before=0.5849 | f1_after=0.8026 | auc=0.0000 | unlearn_time=7.8466 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6216 | f1_after=0.7598 | auc=0.0000 | unlearn_time=9.4910 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=9.8454 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=9.4335 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=11.6647 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=10.0551 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=9.0395 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphEraser_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=8.8926 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7177 | auc=0.6348 | unlearn_time=0.3782 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.5666 | unlearn_time=0.3774 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.5895 | unlearn_time=0.3365 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.6357 | unlearn_time=0.3503 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.6001 | unlearn_time=0.3843 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7117 | auc=0.5157 | unlearn_time=0.3638 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GIF_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7012 | auc=0.5162 | unlearn_time=0.3807 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=5.2979 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.0715 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=7.8826 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.3071 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=9.0041 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=8.2923 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUIDE_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.6721 | auc=0.9321 | unlearn_time=6.2896 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7252 | auc=0.9609 | unlearn_time=0.6591 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7357 | auc=0.8871 | unlearn_time=0.6798 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.7237 | auc=0.8477 | unlearn_time=0.7515 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.7492 | unlearn_time=0.7564 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.6732 | unlearn_time=0.6273 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:37:50] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.6054 | unlearn_time=0.6533 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GNNDelete_GCN_citeseer_r0.5.log`
- 执行结果：OK | f1_before=0.7327 | f1_after=0.7117 | auc=0.5247 | unlearn_time=0.8541 | wall_time=15.71s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7417 | auc=0.0000 | unlearn_time=0.5031 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7477 | auc=0.0000 | unlearn_time=0.5796 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7402 | auc=0.0000 | unlearn_time=0.4673 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7432 | auc=0.0000 | unlearn_time=0.4680 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.5707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\SGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7462 | auc=0.0000 | unlearn_time=0.4733 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7162 | auc=0.0000 | unlearn_time=0.3572 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7237 | auc=0.0000 | unlearn_time=0.2930 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7207 | auc=0.0000 | unlearn_time=0.3864 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:05] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7192 | auc=0.0000 | unlearn_time=0.2831 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7222 | auc=0.0000 | unlearn_time=0.3328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7147 | auc=0.0000 | unlearn_time=0.2726 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\MEGU_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.0000 | unlearn_time=0.2802 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.3883 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4496 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4753 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7523 | auc=0.0000 | unlearn_time=0.4898 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7447 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.3897 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.4005 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GUKD_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4059 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.5111 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7643 | auc=0.0000 | unlearn_time=0.5937 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7432 | f1_after=0.7553 | auc=0.0000 | unlearn_time=0.4951 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7402 | f1_after=0.7538 | auc=0.0000 | unlearn_time=0.6287 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5431 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7417 | f1_after=0.7583 | auc=0.0000 | unlearn_time=0.5117 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\D2DGN_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7477 | f1_after=0.7568 | auc=0.0000 | unlearn_time=0.6663 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.7109 | unlearn_time=0.4286 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7072 | auc=0.6309 | unlearn_time=0.4141 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.6504 | unlearn_time=0.4190 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5970 | unlearn_time=0.4151 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.7042 | auc=0.5668 | unlearn_time=0.4278 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6997 | auc=0.5645 | unlearn_time=0.4328 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\IDEA_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.7327 | f1_after=0.6952 | auc=0.5641 | unlearn_time=0.3277 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.005.log`
- 执行结果：SKIP | f1_before=0.6081 | f1_after=0.7492 | auc=0.0000 | unlearn_time=5.7828 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.01.log`
- 执行结果：SKIP | f1_before=0.6066 | f1_after=0.7538 | auc=0.0000 | unlearn_time=6.0132 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.02.log`
- 执行结果：SKIP | f1_before=0.5946 | f1_after=0.7523 | auc=0.0000 | unlearn_time=7.4315 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.05.log`
- 执行结果：SKIP | f1_before=0.5916 | f1_after=0.7568 | auc=0.0000 | unlearn_time=6.6765 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.1.log`
- 执行结果：SKIP | f1_before=0.5976 | f1_after=0.7462 | auc=0.0000 | unlearn_time=6.7701 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.2.log`
- 执行结果：SKIP | f1_before=0.5931 | f1_after=0.7432 | auc=0.0000 | unlearn_time=7.3728 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=citeseer, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\citeseer\GraphRevoker_GCN_citeseer_r0.5.log`
- 执行结果：SKIP | f1_before=0.4970 | f1_after=0.6967 | auc=0.0000 | unlearn_time=9.3448 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=11.2691 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=11.3707 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=12.1174 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=12.1369 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=9.9784 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=9.4838 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphEraser, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphEraser_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=9.4326 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8585 | auc=0.6436 | unlearn_time=0.6338 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8593 | auc=0.5902 | unlearn_time=0.4256 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8575 | auc=0.5834 | unlearn_time=0.4138 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8534 | auc=0.6008 | unlearn_time=0.4362 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8517 | auc=0.5938 | unlearn_time=0.4177 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8486 | auc=0.4981 | unlearn_time=0.4322 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GIF, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GIF_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8327 | auc=0.4955 | unlearn_time=0.4128 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=29.8813 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=28.6163 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.0762 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=30.4255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=27.2901 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=24.8392 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUIDE, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUIDE_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=NA | f1_after=0.8547 | auc=0.9577 | unlearn_time=20.4457 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=2026.0000 | auc=0.8543 | unlearn_time=0.7840 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8479 | auc=0.6647 | unlearn_time=0.8769 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8258 | auc=0.6738 | unlearn_time=1.0665 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.7809 | auc=0.5314 | unlearn_time=0.9794 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8045 | auc=0.5071 | unlearn_time=0.8011 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:06] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.7863 | auc=0.4978 | unlearn_time=0.8309 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GNNDelete, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GNNDelete_GCN_pubmed_r0.5.log`
- 执行结果：OK | f1_before=0.8628 | f1_after=0.7764 | auc=0.4950 | unlearn_time=1.2538 | wall_time=17.78s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.4359 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.4316 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4628 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4853 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.4649 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.4405 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=SGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\SGU_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8628 | auc=0.0000 | unlearn_time=0.5685 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8489 | auc=0.0000 | unlearn_time=0.3265 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8507 | auc=0.0000 | unlearn_time=0.3505 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8504 | auc=0.0000 | unlearn_time=0.3116 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8471 | auc=0.0000 | unlearn_time=0.3036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8463 | auc=0.0000 | unlearn_time=0.3050 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8436 | auc=0.0000 | unlearn_time=0.3121 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=MEGU, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\MEGU_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8289 | auc=0.0000 | unlearn_time=0.3255 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8633 | f1_after=0.8633 | auc=0.0000 | unlearn_time=0.6851 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8631 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.6306 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8626 | f1_after=0.8626 | auc=0.0000 | unlearn_time=0.6521 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8631 | f1_after=0.8631 | auc=0.0000 | unlearn_time=0.6293 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8623 | f1_after=0.8623 | auc=0.0000 | unlearn_time=0.6253 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8603 | f1_after=0.8603 | auc=0.0000 | unlearn_time=0.6749 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GUKD, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GUKD_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8585 | f1_after=0.8585 | auc=0.0000 | unlearn_time=0.7050 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8542 | f1_after=0.8542 | auc=0.0000 | unlearn_time=0.6030 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8545 | f1_after=0.8545 | auc=0.0000 | unlearn_time=0.6497 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.5865 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8552 | f1_after=0.8560 | auc=0.0000 | unlearn_time=0.6300 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8560 | f1_after=0.8578 | auc=0.0000 | unlearn_time=0.6390 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8567 | f1_after=0.8567 | auc=0.0000 | unlearn_time=0.6657 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=D2DGN, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\D2DGN_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8562 | f1_after=0.8562 | auc=0.0000 | unlearn_time=0.6566 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4667 | unlearn_time=0.4036 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8626 | auc=0.4556 | unlearn_time=0.4508 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8618 | auc=0.4494 | unlearn_time=0.3956 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8588 | auc=0.4835 | unlearn_time=0.3891 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8552 | auc=0.4761 | unlearn_time=0.4364 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8499 | auc=0.4853 | unlearn_time=0.4139 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\IDEA_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.8628 | f1_after=0.8349 | auc=0.4853 | unlearn_time=0.4381 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.005
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.005.log`
- 执行结果：SKIP | f1_before=0.8225 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.2934 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.01
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.01.log`
- 执行结果：SKIP | f1_before=0.8233 | f1_after=0.8605 | auc=0.0000 | unlearn_time=9.4887 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.02
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.02.log`
- 执行结果：SKIP | f1_before=0.8215 | f1_after=0.8613 | auc=0.0000 | unlearn_time=8.5290 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.05
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.05.log`
- 执行结果：SKIP | f1_before=0.8253 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.6590 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.1
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.1.log`
- 执行结果：SKIP | f1_before=0.8245 | f1_after=0.8600 | auc=0.0000 | unlearn_time=8.5873 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.2
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.2.log`
- 执行结果：SKIP | f1_before=0.8190 | f1_after=0.8588 | auc=0.0000 | unlearn_time=8.7754 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。

### [2026-02-17 15:38:24] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=GraphRevoker, ratio=0.5
- 日志路径：`H:\project\OpenGU\GULib-master\results\step0_validation\cross_logs\pubmed\GraphRevoker_GCN_pubmed_r0.5.log`
- 执行结果：SKIP | f1_before=0.7916 | f1_after=0.8524 | auc=0.0000 | unlearn_time=8.5781 | wall_time=0.00s
- 异常与定位：Strict OK log exists
- 下一步建议：继续执行下一个未完成配置。


---

## === SESSION: 2026-02-18 ===

### [2026-02-18] Checkpoint Report: Step 0-4 Complete

#### 进度总结
| Step | 内容 | 状态 | Commits |
|------|------|------|---------|
| 0 | 跨数据集验证 (Cora/Citeseer/Pubmed x 11 methods) | DONE | `3022383` |
| 1 | Base Strategy ABC + Random | DONE | `0f4b1ab` |
| 2/3 | Degree + PageRank baselines | DONE | `1ee45e9` |
| 4 | Attack infrastructure + TracIn + Demo | DONE | `5e67607` |

#### 核心成果
- 攻击框架端到端跑通：策略选择 -> 节点注入 -> 遗忘执行 -> 指标收集
- TracIn 验证通过：Cora/GCN/GNNDelete 上 1.32x > Random
- 4 种策略全部可用：random, degree, pagerank, tracin

#### Demo 结果 (Cora / GCN / GNNDelete)
```
Rank  Strategy   F1 Drop   Ratio(%)   vs Random
1     tracin     0.0904    10.17%     1.32x
2     random     0.0683     7.72%     baseline
3     degree     0.0535     6.05%     0.78x
4     pagerank   0.0535     6.02%     0.78x
```

#### 方法脆弱性排名 (Random baseline, Cora/GCN, ratio=0.1)
| Rank | Method | F1 Drop | Pipeline |
|------|--------|---------|----------|
| 1 | GNNDelete | 8.31% | Learning-based |
| 2 | Projector | 5.90% | Learning-based |
| 3 | GraphEraser | 2.40% | Shard-based |
| 4 | GIF | 2.22% | IF-based |
| 5 | IDEA | 2.03% | Learning-based |
| 6 | MEGU | 1.85% | Learning-based |
| 7 | D2DGN | 0.74% | Learning-based |
| 8 | SGU | 0.55% | IF-based |
| 9 | GUKD | 0.37% | Learning-based |
| 10 | GUIDE | 0.00% | IF-based |

#### Bug 修复记录
1. demo_attack.py: parse_known_args 吞参数 -> 补全覆盖
2. pipeline_adapter.py: CPU/GPU 设备不匹配 -> data.to(device)
3. gnndelete.py: poison_f1 仅 edge task 记录 -> 移除条件
4. tracin_strategy.py: O(N^2) 嵌套循环 -> 矩阵运算 + train_mask

#### 下一阶段: Phase A 深度实验
- 4 methods: GNNDelete, GIF, GraphEraser, GUIDE
- 4 strategies: random, degree, pagerank, tracin
- 关键假设: TracIn 在 IF-based 方法 (GIF) 上优势更大


---
## Session 2026-02-19-1

### [2026-02-19 00:00] DECISION — Collateral Damage 实现方案
- 背景：需要量化攻击对保留节点的附带损害，要求精确重训练（retrain-from-scratch）作为对照
- 选项：A: 在 pipeline 外独立训练新模型 / B: 复用现有 pipeline 的 train_only 模式 / C: 新建独立 retrain 脚本
- 选择：B — 复用 pipeline + train_only flag。理由：(1) 保证训练流程与原始实验完全一致（optimizer, scheduler, data split 等），避免引入训练差异；(2) 改动最小，只需在 3 个 pipeline 基类中加 early return；(3) AttackPipeline.run_retrain() 封装了模型重初始化 + train_only 调用 + 模型提取的完整流程
- 影响：修改 pipeline/Shard_based_pipeline.py, IF_based_pipeline.py, Learning_based_pipeline.py（加 train_only 分支）；新增 attack/pipeline_adapter.py 中的 run_retrain() 方法
- 关联 Step：Step 8

### [2026-02-19 00:01] DECISION — Collateral Damage 度量选择
- 背景：需要度量近似遗忘对保留节点的预测扰动，参考 UtU 论文的 Δp 指标
- 选项：A: L2 距离（概率向量欧氏距离）/ B: L-inf per node（每节点最大类别概率偏移）+ fraction_flipped / C: KL 散度
- 选择：B — L-inf + fraction_flipped。理由：(1) L-inf 捕捉最坏情况扰动，对攻击评估更有意义；(2) fraction_flipped 直观可解释（多少保留节点的预测类别被翻转）；(3) 与 UtU 的 Δp 定义最接近
- 影响：attack/attack_eval.py 新增 evaluate_collateral_damage() 返回 mean_pred_shift, max_pred_shift, fraction_flipped
- 关联 Step：Step 8

### [2026-02-19 00:02] Step 8: Retrain 基础设施实现完成
- 任务：实现 collateral damage 评估的完整基础设施
- 新增文件：
  - attack/pipeline_adapter.py (367 行): AttackPipeline 封装，含 run_retrain()、_get_trained_model()
  - attack/result_cache.py (389 行): ResultCache 磁盘缓存
  - eval_collateral.py (183 行): 端到端 CLI 评估脚本
  - tests/test_collateral.py (428 行, 17 测试): train_only、run_retrain、collateral damage 测试
- 修改文件：
  - pipeline/Shard_based_pipeline.py: 加 train_only early return
  - pipeline/IF_based_pipeline.py: 同上
  - pipeline/Learning_based_pipeline.py: 同上
  - attack/attack_eval.py: 新增 evaluate_retrain_gap (5参数6返回值)、evaluate_collateral_damage
- 测试结果：110 tests, 0 failures（含 17 新增 collateral 测试）
- 代码统计：生产代码 1150→2090 行，测试 1037→1465 行，合计 2187→3555 行
- 下一步建议：运行 eval_collateral.py 生成实际 retrain gap + collateral damage 数据

### [2026-02-19 00:03] 文档同步更新
- 任务：同步 CLAUDE.md、PROGRESS_REPORT.md、flow.md 至 Step 8 完成状态
- CLAUDE.md: Attack Module Structure 去掉 "(Under Development)"，补充 pipeline_adapter/result_cache/eval_collateral，补充 train_only 说明和 results/collateral/ 路径
- PROGRESS_REPORT.md: 代码统计更新至 3555 行，新增 Step 8 小节，Collateral Damage 标记为已实现
- flow.md: §5.3 evaluate_retrain_gap 签名修正（4参→5参, 4返回→6返回），新增 §5.4 evaluate_collateral_damage spec，§7 依赖图补充 run_retrain + eval_collateral 链路，测试 5 标记已实现
- 下一步建议：执行 Phase A+ 实验，运行 eval_collateral.py

### [2026-02-18 03:00] demo_attack.py (backfill)
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=[random,degree,pagerank,tracin], ratio=0.05
- 日志路径：`results/demo_logs/2026-02-18_cora_GCN_GNNDelete.log`
- 执行结果：OK | tracin: f1_before=0.8893, f1_after=0.7989, drop=0.0904 (1.32x) | random: drop=0.0683 | degree: drop=0.0535 | pagerank: drop=0.0535
- 异常与定位：无（修复 3 个 bug 后通过：节点注入路径、device 不匹配、poison_f1 条件）
- 下一步建议：加入 IM/Hybrid 策略扩展至 6 策略对比

### [2026-02-19 19:52] demo_6strategies.py (backfill)
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=[random,degree,pagerank,tracin,im,hybrid], ratio=0.05
- 日志路径：`results/demo_logs/2026-02-19_6strategies_cora_GCN_GNNDelete.log`
- 执行结果：OK | im: f1_before=0.8875, f1_after=0.7491, drop=0.1384 (2.03x) | tracin: drop=0.0904 (1.32x) | hybrid: drop=0.0886 (1.30x) | random: drop=0.0683 | degree: drop=0.0535 | pagerank: drop=0.0535
- 异常与定位：无
- 下一步建议：在 GIF 和 GraphEraser 上运行同配置验证泛化性

### [2026-02-19 19:53] demo_6strategies.py (backfill)
- 任务：dataset=cora, model=GCN, method=GIF, strategies=[random,degree,pagerank,tracin,im,hybrid], ratio=0.05
- 日志路径：`results/demo_logs/2026-02-19_6strategies_cora_GCN_GIF.log`
- 执行结果：OK | hybrid: f1_before=0.8930, f1_after=0.8653, drop=0.0277 (3.00x) | tracin: drop=0.0203 (2.20x) | degree: drop=0.0185 (2.00x) | im: drop=0.0166 (1.80x) | pagerank: drop=0.0129 (1.40x) | random: drop=0.0092
- 异常与定位：无
- 下一步建议：Hybrid 在 IF-based 方法上最强，验证 IF-IM 融合假设

### [2026-02-19 19:56] demo_6strategies.py (backfill)
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=[random,degree,pagerank,tracin,im,hybrid], ratio=0.05
- 日志路径：`results/demo_logs/2026-02-19_6strategies_cora_GCN_GraphEraser.log`
- 执行结果：OK | 所有策略 F1 Drop 为负值（遗忘后性能上升）| pagerank: drop=-0.0295 | degree: drop=-0.0443 | tracin: drop=-0.0480 | im: drop=-0.0517 | hybrid: drop=-0.0627 | random: drop=-0.0701
- 异常与定位：无（GraphEraser 分片聚合架构天然抗攻击，非异常）
- 下一步建议：确认 Shard-based 方法免疫性，作为论文对照组

### [2026-02-19 23:13] Phase A+ Collateral Damage — 3 Methods × 6 Strategies

**配置**: Cora / GCN / unlearn_ratio=0.05 (135 nodes) / seed=2024
**脚本**: `eval_collateral.py` (retrain gap + collateral damage)

#### GNNDelete (Learning-based)

| Strategy | Gap | Gap% | MeanShift | MaxShift | Flipped% |
|----------|-------|--------|-----------|----------|----------|
| random | 0.0609 | 6.86% | 0.2734 | 0.9244 | 11.67% |
| degree | 0.2638 | 29.48% | 0.5587 | 0.9303 | 33.35% |
| pagerank | 0.1919 | 21.44% | 0.3974 | 0.9405 | 23.47% |
| tracin | 0.0978 | 11.02% | 0.2841 | 0.9120 | 12.88% |
| im | 0.2140 | 24.02% | 0.3586 | 0.9866 | 26.54% |
| hybrid | 0.0959 | 10.83% | 0.1588 | 0.9600 | 10.14% |

> 关键观察: degree (29.48%) 和 im (24.02%) Gap 最大；hybrid 的 MeanShift 最低 (0.1588)，说明 hybrid 虽然 Gap 中等但 collateral damage 最小。

#### GIF (IF-based)

| Strategy | Gap | Gap% | MeanShift | MaxShift | Flipped% |
|----------|--------|--------|-----------|----------|----------|
| random | -0.0037 | -0.42% | 0.0152 | 0.5416 | 1.26% |
| degree | 0.0111 | 1.23% | 0.0163 | 0.3365 | 1.31% |
| pagerank | 0.0074 | 0.82% | 0.0150 | 0.3037 | 0.97% |
| tracin | 0.0055 | 0.62% | 0.0135 | 0.5575 | 1.12% |
| im | 0.0018 | 0.21% | 0.0153 | 0.4945 | 1.28% |
| hybrid | 0.0074 | 0.83% | 0.0170 | 0.5453 | 0.94% |

> 关键观察: 所有 Gap ≤ 1.23%，MeanShift ≤ 0.017，Flipped ≤ 1.31%。GIF 的近似误差极小，几乎等同于 retrain，这意味着 GIF 上的 F1 drop 主要来自**删除集本身的节点重要性**而非近似误差（支持 H0）。

#### GraphEraser (Shard-based)

| Strategy | Gap | Gap% | MeanShift | MaxShift | Flipped% |
|----------|--------|--------|-----------|----------|----------|
| random | 0.0609 | 7.64% | 0.2380 | 0.9964 | 25.52% |
| degree | -0.0037 | -0.47% | 0.2262 | 0.9937 | 24.55% |
| pagerank | 0.0387 | 4.68% | 0.2429 | 0.9956 | 21.87% |
| tracin | 0.0498 | 6.47% | 0.2679 | 0.9944 | 26.96% |
| im | -0.0221 | -2.77% | 0.2165 | 0.9920 | 21.02% |
| hybrid | 0.0609 | 7.69% | 0.2359 | 0.9966 | 23.93% |

> 关键观察: Gap 正负交替（-2.77% ~ 7.69%），无一致方向性。但 Collateral Damage 普遍高（MeanShift ~0.22-0.27, Flipped ~21-27%），说明 GraphEraser 的分片聚合架构本身就有较大的预测不稳定性（retrain 与 unlearn 的差异大），与策略选择无关。

#### 跨方法对比结论

1. **GNNDelete**: Gap 显著（6.86%-29.48%），支持 H1（近似误差是主要脆弱性来源）
2. **GIF**: Gap ≈ 0，支持 H0（F1 drop 来自删除集重要性，近似误差极小）
3. **GraphEraser**: Gap 不一致，Collateral Damage 高但无方向性，分片架构的 stochasticity 是主因
4. **归因分离验证**: 同一删除集在 GNNDelete 上 Gap >> 0 而在 GIF 上 Gap ≈ 0，证明 Gap 确实来自近似误差而非删除集本身

- 日志路径: `results/collateral/{GNNDelete,GIF,GraphEraser}/cora/GCN/collateral_20260219_*.json`
- 执行结果: OK
- 下一步建议: 多 seed (>=5) 运行 + compute_gap_statistics() 做假设检验，确认 GNNDelete Gap 显著性

### [2026-02-20 05:03] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, 6策略攻击对比
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = -0.0458 (攻击无效，性能提升)
  - degree: F1 Drop = -0.0834 (攻击无效)
  - pagerank: F1 Drop = -0.0521 (攻击无效)
  - tracin: F1 Drop = -0.0517 (攻击无效)
  - im: F1 Drop = -0.0517 (攻击无效)
  - hybrid: F1 Drop = -0.0517 (攻击无效)
- 异常与定位：GUIDE 方法在所有攻击策略下均免疫，验证了子图修复策略的鲁棒性
- 下一步建议：运行 Collateral Damage 评估

### [2026-02-20 07:18] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = -0.1231 (f1_before=0.7159, f1_after=0.8390, time=47.9s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-02-20 07:29:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.1
- 策略结果：
（无策略结果）
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260220_072942.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-20 08:21:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.69% |    0.2221 |   21.78% |
| degree   | 6.00% |    0.2468 |   25.47% |
| pagerank | 0.49% |    0.2444 |   24.10% |
| tracin   | 6.54% |    0.3143 |   32.12% |
| im       | 8.05% |    0.2557 |   22.75% |
| hybrid   | -1.96% |    0.2343 |   23.88% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260220_082118.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-20 08:31:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 8.29% |    0.2356 |   25.43% |
| degree   | 7.94% |    0.2675 |   26.59% |
| pagerank | -13.17% |    0.2805 |   28.96% |
| tracin   | -3.29% |    0.2675 |   26.29% |
| im       | 4.69% |    0.2855 |   27.82% |
| hybrid   | 4.89% |    0.2275 |   24.13% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260220_083132.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-02-20 08:21:18] eval_collateral.py - GUIDE Collateral Damage
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05, k=135
- 日志路径：`results/collateral/GUIDE/cora/GCN/collateral_20260220_082118.json`
- 执行结果：OK | 全部6策略 Cache Hit，无 SKIP

| Strategy  | F1_before | F1_retrain | F1_unlearn | gap     | gap_pct  | frac_flip |
|-----------|-----------|------------|------------|---------|----------|-----------|
| random    | 0.7269    | 0.7638     | 0.7509     | +0.0129 | +1.69%   | 21.8%     |
| degree    | 0.7491    | 0.7989     | 0.7509     | +0.0480 | +6.00%   | 25.5%     |
| pagerank  | 0.7657    | 0.7565     | 0.7528     | +0.0037 | +0.49%   | 24.1%     |
| tracin    | 0.7325    | 0.7897     | 0.7380     | +0.0517 | +6.54%   | 32.1%     |
| im        | 0.7657    | 0.8247     | 0.7583     | +0.0664 | +8.05%   | 22.7%     |
| hybrid    | 0.7362    | 0.7528     | 0.7675     | -0.0148 | -1.96%   | 23.9%     |

- 说明：gap = F1_retrain - F1_unlearn（正值=遗忘不彻底；负值=过遗忘）
- GUIDE 对 IM 策略的 retrain gap 最大（8%）；hybrid 出现负 gap（过遗忘）
- 异常与定位：无
- 下一步建议：与 GNNDelete/GIF 的 collateral 数据横向对比，分析 GUIDE 的近似遗忘质量

### [2026-02-20 20:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.5s)
  - hybrid: F1 Drop = 0.0166 (f1_before=0.8875, f1_after=0.8708, time=14.3s)
  - im: F1 Drop = 0.0166 (f1_before=0.8838, f1_after=0.8672, time=527.0s)
  - tracin: F1 Drop = 0.0092 (f1_before=0.8911, f1_after=0.8819, time=7.6s)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 20:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s)
  - tracin: F1 Drop = 0.1439 (f1_before=0.8875, f1_after=0.7435, time=6.7s)
  - pagerank: F1 Drop = 0.1033 (f1_before=0.8838, f1_after=0.7804, time=1.0s)
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=1.5s)
  - hybrid: F1 Drop = 0.0609 (f1_before=0.8819, f1_after=0.8210, time=14.6s)
  - degree: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=1.0s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 20:31] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0221 (f1_before=0.8930, f1_after=0.8708, time=6.3s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8911, f1_after=0.8727, time=0.7s)
  - im: F1 Drop = 0.0148 (f1_before=0.8856, f1_after=0.8708, time=514.2s)
  - random: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=0.9s)
  - hybrid: F1 Drop = 0.0129 (f1_before=0.8875, f1_after=0.8745, time=14.2s)
  - pagerank: F1 Drop = 0.0111 (f1_before=0.8893, f1_after=0.8782, time=0.8s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 20:41] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1384 (f1_before=0.8893, f1_after=0.7509, time=1.1s)
  - random: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=1.4s)
  - im: F1 Drop = 0.0996 (f1_before=0.8875, f1_after=0.7878, time=559.6s)
  - degree: F1 Drop = 0.0867 (f1_before=0.8875, f1_after=0.8007, time=1.1s)
  - hybrid: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=19.4s)
  - tracin: F1 Drop = 0.0406 (f1_before=0.8911, f1_after=0.8506, time=6.7s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 21:01] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=535.9s)
  - random: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=1.3s)
  - hybrid: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=14.8s)
  - pagerank: F1 Drop = 0.0166 (f1_before=0.8819, f1_after=0.8653, time=1.0s)
  - tracin: F1 Drop = 0.0111 (f1_before=0.8856, f1_after=0.8745, time=7.3s)
  - degree: F1 Drop = 0.0074 (f1_before=0.8875, f1_after=0.8801, time=1.0s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 21:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.1513 (f1_before=0.8856, f1_after=0.7343, time=15.3s)
  - pagerank: F1 Drop = 0.1089 (f1_before=0.8911, f1_after=0.7823, time=1.2s)
  - tracin: F1 Drop = 0.0830 (f1_before=0.8856, f1_after=0.8026, time=7.4s)
  - im: F1 Drop = 0.0775 (f1_before=0.8875, f1_after=0.8100, time=530.8s)
  - degree: F1 Drop = 0.0664 (f1_before=0.8819, f1_after=0.8155, time=1.1s)
  - random: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=1.5s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 21:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=530.4s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=0.8s)
  - hybrid: F1 Drop = 0.0185 (f1_before=0.8911, f1_after=0.8727, time=14.8s)
  - tracin: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=6.8s)
  - pagerank: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=0.8s)
  - random: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=1.0s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 21:39] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.1273 (f1_before=0.8893, f1_after=0.7620, time=7.5s)
  - degree: F1 Drop = 0.1236 (f1_before=0.8856, f1_after=0.7620, time=1.2s)
  - pagerank: F1 Drop = 0.1125 (f1_before=0.8893, f1_after=0.7768, time=1.2s)
  - hybrid: F1 Drop = 0.1070 (f1_before=0.8856, f1_after=0.7786, time=15.1s)
  - random: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=1.4s)
  - im: F1 Drop = 0.0443 (f1_before=0.8893, f1_after=0.8450, time=532.0s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。


### [2026-02-20 23:03:52] MG-0 Stability Report

### MG-0 Stability (5 seeds): Cora / GCN / ratio=0.05
- Seeds: 42, 212, 722, 1337, 2024
- Methods: GNNDelete (5 seeds), GIF (5 seeds), GraphEraser (1 seed), GUIDE (1 seed)
- Strategies: random, degree, pagerank, tracin, im, hybrid

| Method | Strategy | Mean F1 Drop | Std | n_seeds |
|--------|----------|-------------|-----|---------|
| GNNDelete | random | 7.90% | 1.77% | 5 |
| GNNDelete | degree | 7.71% | 2.61% | 5 |
| GNNDelete | pagerank | 10.33% | 2.77% | 5 |
| GNNDelete | tracin | 9.70% | 3.62% | 5 |
| GNNDelete | im | 10.11% | 3.79% | 5 |
| GNNDelete | hybrid | 9.08% | 3.69% | 5 |
| GIF | random | 1.22% | 0.53% | 5 |
| GIF | degree | 1.37% | 0.59% | 5 |
| GIF | pagerank | 1.55% | 0.46% | 5 |
| GIF | tracin | 1.59% | 0.50% | 5 |
| GIF | im | 1.77% | 0.22% | 5 |
| GIF | hybrid | 1.85% | 0.50% | 5 |
| GraphEraser | random | -7.01% | 0.00% | 1 |
| GraphEraser | degree | -4.43% | 0.00% | 1 |
| GraphEraser | pagerank | -2.95% | 0.00% | 1 |
| GraphEraser | tracin | -4.80% | 0.00% | 1 |
| GraphEraser | im | -5.17% | 0.00% | 1 |
| GraphEraser | hybrid | -6.27% | 0.00% | 1 |
| GUIDE | random | -4.58% | 0.00% | 1 |
| GUIDE | degree | -8.34% | 0.00% | 1 |
| GUIDE | pagerank | -5.21% | 0.00% | 1 |
| GUIDE | tracin | -5.17% | 0.00% | 1 |
| GUIDE | im | -8.67% | 0.00% | 1 |
| GUIDE | hybrid | -12.31% | 0.00% | 1 |

**Key findings:**
- GNNDelete: attack effective (~8-10%), pagerank/im best
- GIF: attack weak (~1-2%), all strategies similar
- GraphEraser/GUIDE: F1 improved (negative drop = attack backfires)
- Seed 2024 aligns with earlier 4-seed trends for GIF
- GNNDelete: seed 2024 shows im best, earlier seeds show pagerank best (some variance)

### [2026-02-20 23:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=31415
- 执行结果：
  - random: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=1.8s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-20 23:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=31415
- 执行结果：
  - random: F1 Drop = 0.0590 (f1_before=0.8893, f1_after=0.8303, time=2.1s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=1.5s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.1440 (f1_before=0.8875, f1_after=0.7435, time=6.7s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.1440 (f1_before=0.8875, f1_after=0.7435, time=6.7s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:58] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=999
- 执行结果：
  - im: F1 Drop = 0.1642 (f1_before=0.8875, f1_after=0.7232, time=533.4s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:59] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=999
- 执行结果：
  - im: F1 Drop = 0.1643 (f1_before=0.8875, f1_after=0.7232, time=533.4s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 01:59] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=999
- 执行结果：
  - im: F1 Drop = 0.1643 (f1_before=0.8875, f1_after=0.7232, time=533.4s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:09] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=999
- 执行结果：
  - im: F1 Drop = 0.1642 (f1_before=0.8875, f1_after=0.7232, time=551.5s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=514.9s, cache=NA)
  - tracin: F1 Drop = 0.1440 (f1_before=0.8875, f1_after=0.7435, time=6.7s, cache=NA)
  - pagerank: F1 Drop = 0.1034 (f1_before=0.8838, f1_after=0.7804, time=1.0s, cache=NA)
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=1.5s, cache=NA)
  - hybrid: F1 Drop = 0.0609 (f1_before=0.8819, f1_after=0.8210, time=14.6s, cache=NA)
  - degree: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=1.0s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:14] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s, cache=NA)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.5s, cache=NA)
  - hybrid: F1 Drop = 0.0167 (f1_before=0.8875, f1_after=0.8708, time=14.3s, cache=NA)
  - im: F1 Drop = 0.0166 (f1_before=0.8838, f1_after=0.8672, time=527.0s, cache=NA)
  - tracin: F1 Drop = 0.0092 (f1_before=0.8911, f1_after=0.8819, time=7.6s, cache=NA)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:52] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0369 (f1_before=0.8081, f1_after=0.8450, time=22.2s, cache=NA)
  - pagerank: F1 Drop = -0.0479 (f1_before=0.7897, f1_after=0.8376, time=17.1s, cache=NA)
  - hybrid: F1 Drop = -0.0793 (f1_before=0.7841, f1_after=0.8635, time=34.6s, cache=MISS, selection=15.5046s)
  - random: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=15.4s, cache=NA)
  - degree: F1 Drop = -0.0830 (f1_before=0.7878, f1_after=0.8708, time=16.5s, cache=NA)
  - im: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=18.2s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:55] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = -0.0393 (f1_before=0.7768, f1_after=0.8160, time=49.7s, cache=MISS, selection=18.3852s)
  - tracin: F1 Drop = -0.0637 (f1_before=0.7694, f1_after=0.8331, time=42.2s, cache=MISS, selection=7.4573s)
  - random: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=18.2s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.001505s, speedup=974.60x)
  - im: F1 Drop = -0.0979 (f1_before=0.7435, f1_after=0.8414, time=17.4s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.001001s, speedup=514235.85x)
  - degree: F1 Drop = -0.1492 (f1_before=0.6716, f1_after=0.8208, time=18.9s, cache=MISS, selection=0.0030s)
  - pagerank: F1 Drop = -0.1513 (f1_before=0.6661, f1_after=0.8174, time=17.8s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = -0.0277 (f1_before=0.8100, f1_after=0.8376, time=40.6s, cache=MISS, selection=19.9964s)
  - im: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=26.2s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.001001s, speedup=559195.16x)
  - random: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=20.0s, cache=NA)
  - degree: F1 Drop = -0.0406 (f1_before=0.8081, f1_after=0.8487, time=22.2s, cache=NA)
  - tracin: F1 Drop = -0.0609 (f1_before=0.7657, f1_after=0.8266, time=31.2s, cache=NA)
  - pagerank: F1 Drop = -0.0701 (f1_before=0.7638, f1_after=0.8339, time=23.0s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 02:59] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - random: F1 Drop = -0.0312 (f1_before=0.7841, f1_after=0.8154, time=18.0s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001000s, speedup=1427.92x)
  - degree: F1 Drop = -0.0600 (f1_before=0.7601, f1_after=0.8201, time=17.9s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = -0.0724 (f1_before=0.7583, f1_after=0.8307, time=46.4s, cache=MISS, selection=17.8999s)
  - tracin: F1 Drop = -0.0816 (f1_before=0.7565, f1_after=0.8381, time=38.1s, cache=MISS, selection=8.3370s)
  - im: F1 Drop = -0.0872 (f1_before=0.7528, f1_after=0.8399, time=17.7s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.1183 (f1_before=0.7214, f1_after=0.8397, time=17.7s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.001502s, speedup=752.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:00] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = -0.0277 (f1_before=0.8229, f1_after=0.8506, time=16.9s, cache=NA)
  - hybrid: F1 Drop = -0.0332 (f1_before=0.8229, f1_after=0.8561, time=40.1s, cache=MISS, selection=18.1100s)
  - tracin: F1 Drop = -0.0554 (f1_before=0.7970, f1_after=0.8524, time=24.7s, cache=NA)
  - random: F1 Drop = -0.0608 (f1_before=0.7934, f1_after=0.8542, time=16.2s, cache=NA)
  - im: F1 Drop = -0.0627 (f1_before=0.7934, f1_after=0.8561, time=20.8s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.1033 (f1_before=0.7491, f1_after=0.8524, time=17.3s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:03] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = -0.0313 (f1_before=0.7989, f1_after=0.8302, time=42.3s, cache=MISS, selection=16.6164s)
  - pagerank: F1 Drop = -0.0543 (f1_before=0.7731, f1_after=0.8273, time=20.4s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.001000s, speedup=1162.81x)
  - tracin: F1 Drop = -0.0679 (f1_before=0.7325, f1_after=0.8003, time=39.3s, cache=MISS, selection=8.8428s)
  - degree: F1 Drop = -0.0768 (f1_before=0.7380, f1_after=0.8148, time=16.1s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = -0.0977 (f1_before=0.7325, f1_after=0.8302, time=19.1s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.001003s, speedup=529462.11x)
  - random: F1 Drop = -0.1215 (f1_before=0.6974, f1_after=0.8189, time=19.2s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.000999s, speedup=1482.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:04] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = -0.0479 (f1_before=0.8063, f1_after=0.8542, time=23.1s, cache=NA)
  - im: F1 Drop = -0.0646 (f1_before=0.7878, f1_after=0.8524, time=20.0s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.000000s)
  - random: F1 Drop = -0.0646 (f1_before=0.7878, f1_after=0.8524, time=16.3s, cache=NA)
  - hybrid: F1 Drop = -0.0683 (f1_before=0.7823, f1_after=0.8506, time=36.5s, cache=MISS, selection=15.7610s)
  - degree: F1 Drop = -0.0812 (f1_before=0.7657, f1_after=0.8469, time=17.3s, cache=NA)
  - pagerank: F1 Drop = -0.0923 (f1_before=0.7675, f1_after=0.8598, time=18.5s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:07] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'pagerank', 'im', 'tracin', 'degree', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = -0.0323 (f1_before=0.7952, f1_after=0.8275, time=18.7s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.000000s)
  - random: F1 Drop = -0.0373 (f1_before=0.7952, f1_after=0.8325, time=18.7s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.000000s)
  - tracin: F1 Drop = -0.0497 (f1_before=0.7694, f1_after=0.8191, time=37.7s, cache=MISS, selection=7.6620s)
  - hybrid: F1 Drop = -0.0595 (f1_before=0.7657, f1_after=0.8252, time=45.8s, cache=MISS, selection=18.1744s)
  - degree: F1 Drop = -0.0711 (f1_before=0.7472, f1_after=0.8183, time=16.3s, cache=MISS, selection=0.0000s)
  - pagerank: F1 Drop = -0.0728 (f1_before=0.7601, f1_after=0.8330, time=16.1s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:44] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = -0.0295 (f1_before=0.8100, f1_after=0.8395, time=18.2s, cache=MISS, selection=0.0405s)
  - degree: F1 Drop = -0.0443 (f1_before=0.7970, f1_after=0.8413, time=17.9s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = -0.0480 (f1_before=0.7860, f1_after=0.8339, time=25.4s, cache=MISS, selection=6.7860s)
  - im: F1 Drop = -0.0517 (f1_before=0.8026, f1_after=0.8542, time=577.9s, cache=MISS, selection=559.7645s)
  - hybrid: F1 Drop = -0.0627 (f1_before=0.8007, f1_after=0.8635, time=31.4s, cache=MISS, selection=15.3211s)
  - random: F1 Drop = -0.0701 (f1_before=0.7675, f1_after=0.8376, time=18.0s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 03:44] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = -0.0457 (f1_before=0.7565, f1_after=0.8022, time=19.3s, cache=NA)
  - tracin: F1 Drop = -0.0517 (f1_before=0.0000, f1_after=0.0517, time=27.1s, cache=NA)
  - pagerank: F1 Drop = -0.0521 (f1_before=0.7638, f1_after=0.8159, time=18.7s, cache=NA)
  - degree: F1 Drop = -0.0834 (f1_before=0.7380, f1_after=0.8214, time=18.2s, cache=NA)
  - im: F1 Drop = -0.0868 (f1_before=0.7435, f1_after=0.8303, time=593.4s, cache=NA)
  - hybrid: F1 Drop = -0.1231 (f1_before=0.7159, f1_after=0.8390, time=47.9s, cache=NA)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=7.9s, cache=MISS, selection=6.5730s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=8.2s, cache=MISS, selection=7.1424s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:50] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=25.8s, cache=MISS, selection=6.5858s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:51] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0713 (f1_before=0.7657, f1_after=0.8370, time=37.7s, cache=MISS, selection=7.2103s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:51] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=8.9s, cache=MISS, selection=7.4003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=8.2s, cache=MISS, selection=7.1508s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:52] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=29.5s, cache=MISS, selection=7.2580s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:53] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = -0.0409 (f1_before=0.7823, f1_after=0.8232, time=38.8s, cache=MISS, selection=7.6158s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:53] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=8.8s, cache=MISS, selection=7.2119s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:54] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=9.8s, cache=MISS, selection=8.7071s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:54] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = -0.0627 (f1_before=0.7934, f1_after=0.8561, time=30.0s, cache=MISS, selection=7.4791s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:55] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = -0.0483 (f1_before=0.7565, f1_after=0.8048, time=43.9s, cache=MISS, selection=9.0457s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:56] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=12.7s, cache=MISS, selection=10.8470s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:56] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=10.5s, cache=MISS, selection=9.4422s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:57] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = -0.0646 (f1_before=0.7878, f1_after=0.8524, time=37.4s, cache=MISS, selection=10.5821s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:58] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = -0.1342 (f1_before=0.7011, f1_after=0.8353, time=44.6s, cache=MISS, selection=10.1508s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:58] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=10.4s, cache=MISS, selection=8.7320s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:58] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0092 (f1_before=0.8838, f1_after=0.8745, time=9.3s, cache=MISS, selection=8.0623s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 04:59] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = -0.0683 (f1_before=0.7675, f1_after=0.8358, time=28.7s, cache=MISS, selection=7.9055s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 05:00] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = -0.1231 (f1_before=0.7159, f1_after=0.8390, time=35.6s, cache=MISS, selection=6.9993s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 05:21:59] Phase A TracIn Fix — Consolidated Report

**Background**: TracIn had node ID mapping bug (commit 55c8971 fix). `topk_indices` were candidates-array indices, not actual node IDs. All prior tracin results selected wrong nodes.

**Scope**: Phase A only (cora/GCN, ratio=0.05, 4 methods x 5 seeds = 20 experiments)

**Actions taken**:
1. Moved 12 polluted files to `results/_deprecated_tracin_bug/`
2. Deleted 21 tracin cache entries from `results/cache/`
3. Rerun all 20 tracin experiments (results in `tracin_fix_phase_a/`)
4. Merged table saved to `phase_a_v2_tracin_fix.json`

### Phase A Corrected Results: Cora / GCN / ratio=0.05
- Seeds: 42, 212, 722, 1337, 2024
- Methods: GNNDelete, GIF, GraphEraser, GUIDE (all 5 seeds)
- Strategies: random, degree, pagerank, **tracin (FIXED)**, im, hybrid

| Method | Strategy | Mean F1 Drop | Std | n_seeds |
|--------|----------|-------------|-----|---------|
| GNNDelete | random | 8.17% | 1.88% | 4 |
| GNNDelete | degree | 8.30% | 2.60% | 4 |
| GNNDelete | pagerank | 11.58% | 1.35% | 4 |
| GNNDelete | tracin **(FIXED)** | 7.90% | 1.77% | 5 |
| GNNDelete | im | 9.18% | 3.69% | 4 |
| GNNDelete | hybrid | 9.13% | 4.13% | 4 |
| GIF | random | 1.29% | 0.57% | 4 |
| GIF | degree | 1.25% | 0.61% | 4 |
| GIF | pagerank | 1.61% | 0.49% | 4 |
| GIF | tracin **(FIXED)** | 1.22% | 0.53% | 5 |
| GIF | im | 1.80% | 0.24% | 4 |
| GIF | hybrid | 1.62% | 0.20% | 4 |
| GraphEraser | random | -6.27% | 1.57% | 5 |
| GraphEraser | degree | -5.54% | 2.25% | 5 |
| GraphEraser | pagerank | -6.86% | 2.73% | 5 |
| GraphEraser | tracin **(FIXED)** | -6.27% | 1.55% | 5 |
| GraphEraser | im | -5.94% | 1.58% | 5 |
| GraphEraser | hybrid | -5.42% | 2.02% | 5 |
| GUIDE | random | -6.23% | 3.33% | 5 |
| GUIDE | degree | -8.81% | 3.15% | 5 |
| GUIDE | pagerank | -8.98% | 3.89% | 5 |
| GUIDE | tracin **(FIXED)** | -8.36% | 3.83% | 5 |
| GUIDE | im | -8.04% | 2.45% | 5 |
| GUIDE | hybrid | -6.51% | 3.24% | 5 |

### TracIn old vs new comparison

| Method | Seed | Old tracin F1 Drop | New tracin F1 Drop | Nodes overlap |
|--------|------|-------------------|-------------------|---------------|
| GNNDelete | 42 | 14.39% | 9.23% | 10/135 |
| GNNDelete | 212 | 4.06% | 10.52% | 6/135 |
| GNNDelete | 722 | 8.30% | 5.54% | 9/135 |
| GNNDelete | 1337 | 12.73% | 7.38% | 10/135 |
| GNNDelete | 2024 | N/A | 6.83% | N/A |
| GIF | 42 | 0.92% | 1.85% | 12/135 |
| GIF | 212 | 2.21% | 1.29% | 9/135 |
| GIF | 722 | 1.11% | 1.66% | 10/135 |
| GIF | 1337 | 1.66% | 0.37% | 7/135 |
| GIF | 2024 | N/A | 0.92% | N/A |
| GraphEraser | 42 | -3.69% | -8.30% | 4/135 |
| GraphEraser | 212 | -6.09% | -3.51% | 7/135 |
| GraphEraser | 722 | -5.54% | -6.27% | 4/135 |
| GraphEraser | 1337 | -4.79% | -6.46% | 4/135 |
| GraphEraser | 2024 | -4.80% | -6.83% | 10/135 |
| GUIDE | 42 | -6.37% | -7.13% | 6/135 |
| GUIDE | 212 | -8.16% | -4.09% | 5/135 |
| GUIDE | 722 | -6.79% | -4.83% | 3/135 |
| GUIDE | 1337 | -4.97% | -13.42% | 6/135 |
| GUIDE | 2024 | -5.17% | -12.31% | 9/135 |

**Key findings (post-fix)**:
- GNNDelete: tracin mean F1 drop = 7.90% (was 9.87% before fix)
- GIF: tracin mean F1 drop = 1.22%
- GraphEraser/GUIDE: tracin still shows negative F1 drop (attack backfires) — consistent with all other strategies on shard-based methods
- Node selection completely changed: overlap only 3-12/135 between old and new
- Non-tracin columns unchanged from original Phase A

### [2026-02-21 17:12] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = 0.0330 (f1_before=0.7327, f1_after=0.6997, time=1.1s, cache=MISS, selection=0.0530s)
  - hybrid: F1 Drop = 0.0270 (f1_before=0.7312, f1_after=0.7042, time=15.9s, cache=MISS, selection=14.7189s)
  - im: F1 Drop = 0.0270 (f1_before=0.7327, f1_after=0.7057, time=95.9s, cache=MISS, selection=94.6729s)
  - random: F1 Drop = 0.0255 (f1_before=0.7282, f1_after=0.7027, time=1.9s, cache=MISS, selection=0.0030s)
  - pagerank: F1 Drop = 0.0225 (f1_before=0.7297, f1_after=0.7072, time=1.1s, cache=MISS, selection=0.0410s)
  - tracin: F1 Drop = 0.0180 (f1_before=0.7252, f1_after=0.7072, time=15.8s, cache=MISS, selection=14.6065s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - random: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.8s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.001013s, speedup=2.96x)
  - degree: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=MISS, selection=0.0210s)
  - pagerank: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=HIT(key=6460c53b924fd6f49294630114f1e052), selection=0.0410s, reuse=0.000988s, speedup=41.49x)
  - tracin: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=9.9s, cache=MISS, selection=9.2185s)
  - im: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=16.8s, cache=MISS, selection=15.5033s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:16] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = -0.0571 (f1_before=0.6817, f1_after=0.7387, time=31.6s, cache=HIT(key=6460c53b924fd6f49294630114f1e052), selection=0.0410s, reuse=0.001001s, speedup=40.95x)
  - degree: F1 Drop = -0.0886 (f1_before=0.6577, f1_after=0.7462, time=27.9s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0961 (f1_before=0.6607, f1_after=0.7568, time=28.7s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.000000s)
  - im: F1 Drop = -0.1096 (f1_before=0.6351, f1_after=0.7447, time=29.4s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1111 (f1_before=0.6547, f1_after=0.7658, time=39.7s, cache=MISS, selection=12.4161s)
  - hybrid: F1 Drop = -0.1231 (f1_before=0.6396, f1_after=0.7628, time=41.5s, cache=MISS, selection=19.5374s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:19] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.0330 (f1_before=0.7342, f1_after=0.7012, time=16.5s, cache=MISS, selection=15.1098s)
  - random: F1 Drop = 0.0315 (f1_before=0.7327, f1_after=0.7012, time=1.6s, cache=MISS, selection=0.0000s)
  - pagerank: F1 Drop = 0.0300 (f1_before=0.7267, f1_after=0.6967, time=1.2s, cache=MISS, selection=0.0537s)
  - degree: F1 Drop = 0.0255 (f1_before=0.7252, f1_after=0.6997, time=1.3s, cache=MISS, selection=0.0260s)
  - im: F1 Drop = 0.0225 (f1_before=0.7267, f1_after=0.7042, time=89.3s, cache=MISS, selection=87.9903s)
  - tracin: F1 Drop = 0.0210 (f1_before=0.7252, f1_after=0.7042, time=11.0s, cache=MISS, selection=9.7584s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:22] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = -0.0571 (f1_before=0.6922, f1_after=0.7492, time=33.7s, cache=MISS, selection=9.5534s)
  - pagerank: F1 Drop = -0.0796 (f1_before=0.6712, f1_after=0.7508, time=23.3s, cache=HIT(key=c7a9408a94ad210c6dbe7bccf7094cbb), selection=0.0537s, reuse=0.000000s)
  - random: F1 Drop = -0.0916 (f1_before=0.6592, f1_after=0.7508, time=22.8s, cache=HIT(key=dd631a6e85ab2aa173ab0bbb607ef87a), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - hybrid: F1 Drop = -0.0991 (f1_before=0.6532, f1_after=0.7523, time=40.3s, cache=MISS, selection=15.8799s)
  - im: F1 Drop = -0.1051 (f1_before=0.6366, f1_after=0.7417, time=25.6s, cache=HIT(key=109781dcf7a2e47f8929dbf47e9a7538), selection=87.9903s, reuse=0.001000s, speedup=87954.78x)
  - degree: F1 Drop = -0.1141 (f1_before=0.6246, f1_after=0.7387, time=23.6s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0285 (f1_before=0.7312, f1_after=0.7027, time=1.3s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = 0.0285 (f1_before=0.7312, f1_after=0.7027, time=91.0s, cache=MISS, selection=89.6796s)
  - pagerank: F1 Drop = 0.0255 (f1_before=0.7342, f1_after=0.7087, time=1.1s, cache=MISS, selection=0.0350s)
  - tracin: F1 Drop = 0.0240 (f1_before=0.7312, f1_after=0.7072, time=11.2s, cache=MISS, selection=10.1558s)
  - hybrid: F1 Drop = 0.0240 (f1_before=0.7267, f1_after=0.7027, time=16.4s, cache=MISS, selection=15.3034s)
  - degree: F1 Drop = 0.0150 (f1_before=0.7222, f1_after=0.7072, time=1.0s, cache=MISS, selection=0.0201s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:25] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - random: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.9s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.000000s)
  - degree: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.6s, cache=MISS, selection=0.0220s)
  - pagerank: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.6s, cache=HIT(key=18702d1c5f448d2a6c93e480a04345c9), selection=0.0350s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=9.7s, cache=MISS, selection=9.0621s)
  - im: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.7s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=16.4s, cache=MISS, selection=15.4302s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:27] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = -0.0601 (f1_before=0.6757, f1_after=0.7357, time=22.6s, cache=HIT(key=18702d1c5f448d2a6c93e480a04345c9), selection=0.0350s, reuse=0.001000s, speedup=34.99x)
  - tracin: F1 Drop = -0.0751 (f1_before=0.6787, f1_after=0.7538, time=30.7s, cache=MISS, selection=8.9019s)
  - degree: F1 Drop = -0.0811 (f1_before=0.6667, f1_after=0.7477, time=23.1s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0961 (f1_before=0.6456, f1_after=0.7417, time=21.8s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - hybrid: F1 Drop = -0.1171 (f1_before=0.6396, f1_after=0.7568, time=36.0s, cache=MISS, selection=15.3479s)
  - im: F1 Drop = -0.1171 (f1_before=0.6246, f1_after=0.7417, time=21.7s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = 0.0390 (f1_before=0.7387, f1_after=0.6997, time=1.0s, cache=MISS, selection=0.0370s)
  - random: F1 Drop = 0.0375 (f1_before=0.7372, f1_after=0.6997, time=1.3s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = 0.0375 (f1_before=0.7357, f1_after=0.6982, time=16.5s, cache=MISS, selection=15.1290s)
  - tracin: F1 Drop = 0.0330 (f1_before=0.7357, f1_after=0.7027, time=10.5s, cache=MISS, selection=9.4377s)
  - degree: F1 Drop = 0.0315 (f1_before=0.7327, f1_after=0.7012, time=1.0s, cache=MISS, selection=0.0210s)
  - im: F1 Drop = 0.0285 (f1_before=0.7297, f1_after=0.7012, time=85.4s, cache=MISS, selection=84.1961s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:30] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=1.3s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - degree: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.8s, cache=MISS, selection=0.0386s)
  - pagerank: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.8s, cache=HIT(key=311949fc36049248e5e42350470311dc), selection=0.0370s, reuse=0.000996s, speedup=37.15x)
  - tracin: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=12.8s, cache=MISS, selection=11.9380s)
  - im: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.9s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=22.5s, cache=MISS, selection=21.2586s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:34] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = -0.0661 (f1_before=0.6727, f1_after=0.7387, time=29.4s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.001001s, speedup=84142.04x)
  - random: F1 Drop = -0.0691 (f1_before=0.6697, f1_after=0.7387, time=28.9s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.002000s, speedup=0.00x)
  - tracin: F1 Drop = -0.0781 (f1_before=0.6622, f1_after=0.7402, time=41.5s, cache=MISS, selection=12.3114s)
  - degree: F1 Drop = -0.0841 (f1_before=0.6667, f1_after=0.7508, time=32.4s, cache=MISS, selection=0.0010s)
  - hybrid: F1 Drop = -0.0931 (f1_before=0.6637, f1_after=0.7568, time=47.6s, cache=MISS, selection=19.4022s)
  - pagerank: F1 Drop = -0.1321 (f1_before=0.6216, f1_after=0.7538, time=30.9s, cache=HIT(key=311949fc36049248e5e42350470311dc), selection=0.0370s, reuse=0.001004s, speedup=36.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.0315 (f1_before=0.7297, f1_after=0.6982, time=1.3s, cache=MISS, selection=0.0300s)
  - im: F1 Drop = 0.0315 (f1_before=0.7342, f1_after=0.7027, time=111.9s, cache=MISS, selection=110.5862s)
  - pagerank: F1 Drop = 0.0270 (f1_before=0.7357, f1_after=0.7087, time=1.4s, cache=MISS, selection=0.0476s)
  - tracin: F1 Drop = 0.0270 (f1_before=0.7327, f1_after=0.7057, time=14.4s, cache=MISS, selection=12.9156s)
  - hybrid: F1 Drop = 0.0240 (f1_before=0.7297, f1_after=0.7057, time=16.1s, cache=MISS, selection=14.9396s)
  - random: F1 Drop = 0.0210 (f1_before=0.7327, f1_after=0.7117, time=1.6s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:37] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.9s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - degree: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.7s, cache=MISS, selection=0.0210s)
  - pagerank: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.6s, cache=HIT(key=756e60c61d74eba56d02877703f9f0ce), selection=0.0476s, reuse=0.000000s)
  - tracin: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=9.7s, cache=MISS, selection=9.0975s)
  - im: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.6s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=16.3s, cache=MISS, selection=15.2594s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 17:41] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = -0.0616 (f1_before=0.6862, f1_after=0.7477, time=25.2s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = -0.0916 (f1_before=0.6562, f1_after=0.7477, time=33.2s, cache=MISS, selection=9.6950s)
  - im: F1 Drop = -0.0946 (f1_before=0.6562, f1_after=0.7508, time=22.6s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.001001s, speedup=110515.17x)
  - random: F1 Drop = -0.0946 (f1_before=0.6577, f1_after=0.7523, time=25.4s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.001004s, speedup=0.00x)
  - hybrid: F1 Drop = -0.1111 (f1_before=0.6351, f1_after=0.7462, time=38.1s, cache=MISS, selection=15.3157s)
  - pagerank: F1 Drop = -0.1141 (f1_before=0.6426, f1_after=0.7568, time=24.6s, cache=HIT(key=756e60c61d74eba56d02877703f9f0ce), selection=0.0476s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=16.5s, cache=MISS, selection=14.9414s)
  - im: F1 Drop = 0.1439 (f1_before=0.8875, f1_after=0.7435, time=1.3s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.1033 (f1_before=0.8838, f1_after=0.7804, time=1.3s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.070315s, speedup=14.63x)
  - tracin: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=7.9s, cache=MISS, selection=6.5730s)
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=2.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - degree: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=1.3s, cache=MISS, selection=0.0428s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=8.2s, cache=MISS, selection=7.1424s)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000995s, speedup=1474.74x)
  - hybrid: F1 Drop = 0.0166 (f1_before=0.8838, f1_after=0.8672, time=16.4s, cache=MISS, selection=15.2937s)
  - im: F1 Drop = 0.0092 (f1_before=0.8911, f1_after=0.8819, time=0.9s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.001005s, speedup=512284.29x)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s, cache=MISS, selection=0.0190s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:25] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = -0.0258 (f1_before=0.7934, f1_after=0.8192, time=34.7s, cache=MISS, selection=15.5197s)
  - im: F1 Drop = -0.0424 (f1_before=0.7989, f1_after=0.8413, time=18.6s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.001000s, speedup=514726.07x)
  - pagerank: F1 Drop = -0.0480 (f1_before=0.7897, f1_after=0.8376, time=20.1s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - degree: F1 Drop = -0.0812 (f1_before=0.7878, f1_after=0.8690, time=18.4s, cache=MISS, selection=0.0010s)
  - tracin: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=25.8s, cache=MISS, selection=6.5858s)
  - random: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=17.8s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:27] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0713 (f1_before=0.7657, f1_after=0.8370, time=37.7s, cache=MISS, selection=7.2103s)
  - random: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=16.7s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.0979 (f1_before=0.7435, f1_after=0.8414, time=17.6s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000990s, speedup=1038.78x)
  - hybrid: F1 Drop = -0.1339 (f1_before=0.7085, f1_after=0.8424, time=42.4s, cache=MISS, selection=16.0744s)
  - im: F1 Drop = -0.1507 (f1_before=0.6679, f1_after=0.8186, time=17.9s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.000000s)
  - degree: F1 Drop = -0.1513 (f1_before=0.6661, f1_after=0.8174, time=17.1s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:28] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1384 (f1_before=0.8893, f1_after=0.7509, time=1.4s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000992s, speedup=1139.52x)
  - tracin: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=8.9s, cache=MISS, selection=7.4003s)
  - random: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=1.8s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1416.45x)
  - hybrid: F1 Drop = 0.0996 (f1_before=0.8875, f1_after=0.7878, time=17.4s, cache=MISS, selection=15.6631s)
  - degree: F1 Drop = 0.0867 (f1_before=0.8875, f1_after=0.8007, time=1.4s, cache=MISS, selection=0.0240s)
  - im: F1 Drop = 0.0406 (f1_before=0.8911, f1_after=0.8506, time=1.4s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.001000s, speedup=559328.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.0221 (f1_before=0.8930, f1_after=0.8708, time=0.9s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.000000s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8911, f1_after=0.8727, time=1.0s, cache=MISS, selection=0.0190s)
  - hybrid: F1 Drop = 0.0148 (f1_before=0.8856, f1_after=0.8708, time=16.7s, cache=MISS, selection=15.5661s)
  - random: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=1.3s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1415.78x)
  - tracin: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=8.2s, cache=MISS, selection=7.1508s)
  - pagerank: F1 Drop = 0.0111 (f1_before=0.8893, f1_after=0.8782, time=0.9s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000990s, speedup=1141.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:31] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - random: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=19.9s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001000s, speedup=1428.26x)
  - tracin: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=29.5s, cache=MISS, selection=7.2580s)
  - degree: F1 Drop = -0.0406 (f1_before=0.8081, f1_after=0.8487, time=19.0s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = -0.0535 (f1_before=0.8007, f1_after=0.8542, time=36.4s, cache=MISS, selection=15.8716s)
  - im: F1 Drop = -0.0664 (f1_before=0.7675, f1_after=0.8339, time=20.0s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.000942s, speedup=593711.64x)
  - pagerank: F1 Drop = -0.0701 (f1_before=0.7638, f1_after=0.8339, time=20.4s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000999s, speedup=1130.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = 0.1089 (f1_before=0.8911, f1_after=0.7823, time=1.4s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.000000s)
  - im: F1 Drop = 0.0830 (f1_before=0.8856, f1_after=0.8026, time=1.3s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.000000s)
  - hybrid: F1 Drop = 0.0775 (f1_before=0.8875, f1_after=0.8100, time=17.3s, cache=MISS, selection=15.6734s)
  - degree: F1 Drop = 0.0664 (f1_before=0.8819, f1_after=0.8155, time=1.4s, cache=MISS, selection=0.0230s)
  - tracin: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=8.8s, cache=MISS, selection=7.2119s)
  - random: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=1.8s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.001000s, speedup=1481.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=16.5s, cache=MISS, selection=15.3529s)
  - random: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=1.2s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.001011s, speedup=1465.88x)
  - pagerank: F1 Drop = 0.0166 (f1_before=0.8819, f1_after=0.8653, time=1.0s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.000999s, speedup=1164.19x)
  - tracin: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=9.8s, cache=MISS, selection=8.7071s)
  - im: F1 Drop = 0.0111 (f1_before=0.8856, f1_after=0.8745, time=1.0s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.001001s, speedup=530092.42x)
  - degree: F1 Drop = 0.0074 (f1_before=0.8875, f1_after=0.8801, time=1.0s, cache=MISS, selection=0.0209s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:34] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = -0.0277 (f1_before=0.8229, f1_after=0.8506, time=19.5s, cache=MISS, selection=0.0010s)
  - hybrid: F1 Drop = -0.0295 (f1_before=0.7897, f1_after=0.8192, time=42.9s, cache=MISS, selection=16.4775s)
  - im: F1 Drop = -0.0517 (f1_before=0.8007, f1_after=0.8524, time=20.2s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.000000s)
  - tracin: F1 Drop = -0.0627 (f1_before=0.7934, f1_after=0.8561, time=30.0s, cache=MISS, selection=7.4791s)
  - random: F1 Drop = -0.0627 (f1_before=0.7934, f1_after=0.8561, time=19.1s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.1033 (f1_before=0.7491, f1_after=0.8524, time=18.8s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.001000s, speedup=1162.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:36] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = -0.0483 (f1_before=0.7565, f1_after=0.8048, time=43.9s, cache=MISS, selection=9.0457s)
  - degree: F1 Drop = -0.0543 (f1_before=0.7731, f1_after=0.8273, time=16.9s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = -0.0737 (f1_before=0.7620, f1_after=0.8357, time=44.3s, cache=MISS, selection=16.3232s)
  - im: F1 Drop = -0.0792 (f1_before=0.7251, f1_after=0.8043, time=17.6s, cache=HIT(key=cdaefa7c36b7acca9e79405840a9f58a), selection=530.8123s, reuse=0.001000s, speedup=530977.38x)
  - pagerank: F1 Drop = -0.0977 (f1_before=0.7325, f1_after=0.8302, time=16.8s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.001000s, speedup=1163.36x)
  - random: F1 Drop = -0.1215 (f1_before=0.6974, f1_after=0.8189, time=17.4s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:37] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1273 (f1_before=0.8893, f1_after=0.7620, time=1.4s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.000000s)
  - degree: F1 Drop = 0.1236 (f1_before=0.8856, f1_after=0.7620, time=1.4s, cache=MISS, selection=0.0097s)
  - pagerank: F1 Drop = 0.1125 (f1_before=0.8893, f1_after=0.7768, time=1.4s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000993s, speedup=1234.34x)
  - random: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=2.0s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.001000s, speedup=1413.27x)
  - tracin: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=12.7s, cache=MISS, selection=10.8470s)
  - hybrid: F1 Drop = 0.0443 (f1_before=0.8893, f1_after=0.8450, time=18.2s, cache=MISS, selection=16.5622s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=17.3s, cache=MISS, selection=16.2168s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=1.1s, cache=MISS, selection=0.0220s)
  - im: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=1.0s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=1.0s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=10.5s, cache=MISS, selection=9.4422s)
  - random: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=1.5s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:39] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = -0.0332 (f1_before=0.8137, f1_after=0.8469, time=19.5s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.001001s, speedup=531580.57x)
  - hybrid: F1 Drop = -0.0517 (f1_before=0.8044, f1_after=0.8561, time=34.7s, cache=MISS, selection=15.8972s)
  - random: F1 Drop = -0.0646 (f1_before=0.7878, f1_after=0.8524, time=19.8s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.000999s, speedup=1415.29x)
  - tracin: F1 Drop = -0.0646 (f1_before=0.7878, f1_after=0.8524, time=37.4s, cache=MISS, selection=10.5821s)
  - degree: F1 Drop = -0.0812 (f1_before=0.7657, f1_after=0.8469, time=19.8s, cache=MISS, selection=0.0010s)
  - pagerank: F1 Drop = -0.0923 (f1_before=0.7675, f1_after=0.8598, time=21.0s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:41] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = -0.0323 (f1_before=0.7952, f1_after=0.8275, time=17.3s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000000s)
  - random: F1 Drop = -0.0373 (f1_before=0.7952, f1_after=0.8325, time=18.3s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.001000s, speedup=1413.60x)
  - hybrid: F1 Drop = -0.0542 (f1_before=0.7657, f1_after=0.8199, time=41.9s, cache=MISS, selection=15.9487s)
  - degree: F1 Drop = -0.0728 (f1_before=0.7601, f1_after=0.8330, time=17.0s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = -0.0811 (f1_before=0.7491, f1_after=0.8302, time=18.0s, cache=HIT(key=dbc53b1d991164343b17fd73fc93cc0a), selection=532.0490s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1342 (f1_before=0.7011, f1_after=0.8353, time=44.6s, cache=MISS, selection=10.1508s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:42] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.1458 (f1_before=0.8875, f1_after=0.7417, time=17.5s, cache=MISS, selection=16.0730s)
  - im: F1 Drop = 0.0904 (f1_before=0.8893, f1_after=0.7989, time=1.4s, cache=HIT(key=75e01e91be337fd3898ff32666b9f47b), selection=577.8812s, reuse=0.001000s, speedup=577923.09x)
  - tracin: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=10.4s, cache=MISS, selection=8.7320s)
  - random: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=1.7s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.000999s, speedup=17988.57x)
  - degree: F1 Drop = 0.0535 (f1_before=0.8838, f1_after=0.8303, time=1.5s, cache=MISS, selection=0.0240s)
  - pagerank: F1 Drop = 0.0535 (f1_before=0.8893, f1_after=0.8358, time=1.4s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.001010s, speedup=17982.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:42] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=1.1s, cache=HIT(key=75e01e91be337fd3898ff32666b9f47b), selection=577.8812s, reuse=0.000000s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8948, f1_after=0.8764, time=1.0s, cache=MISS, selection=0.0220s)
  - hybrid: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=16.8s, cache=MISS, selection=15.6824s)
  - pagerank: F1 Drop = 0.0129 (f1_before=0.8875, f1_after=0.8745, time=1.0s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0093 (f1_before=0.8838, f1_after=0.8745, time=9.3s, cache=MISS, selection=8.0623s)
  - random: F1 Drop = 0.0092 (f1_before=0.8838, f1_after=0.8745, time=1.2s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.001000s, speedup=17971.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:45] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = -0.0295 (f1_before=0.8100, f1_after=0.8395, time=19.5s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.000000s)
  - degree: F1 Drop = -0.0443 (f1_before=0.7970, f1_after=0.8413, time=20.0s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = -0.0480 (f1_before=0.8026, f1_after=0.8506, time=34.8s, cache=MISS, selection=15.8759s)
  - im: F1 Drop = -0.0609 (f1_before=0.7749, f1_after=0.8358, time=20.4s, cache=HIT(key=75e01e91be337fd3898ff32666b9f47b), selection=577.8812s, reuse=0.001002s, speedup=576685.56x)
  - random: F1 Drop = -0.0683 (f1_before=0.7675, f1_after=0.8358, time=19.1s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.000999s, speedup=17992.86x)
  - tracin: F1 Drop = -0.0683 (f1_before=0.7675, f1_after=0.8358, time=28.7s, cache=MISS, selection=7.9055s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:47] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = -0.0050 (f1_before=0.8063, f1_after=0.8113, time=42.7s, cache=MISS, selection=16.1437s)
  - degree: F1 Drop = -0.0645 (f1_before=0.7417, f1_after=0.8062, time=17.4s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = -0.0776 (f1_before=0.7454, f1_after=0.8230, time=16.9s, cache=HIT(key=75e01e91be337fd3898ff32666b9f47b), selection=577.8812s, reuse=0.000000s)
  - random: F1 Drop = -0.0867 (f1_before=0.7435, f1_after=0.8303, time=17.2s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.1090 (f1_before=0.6956, f1_after=0.8046, time=17.2s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1231 (f1_before=0.7159, f1_after=0.8390, time=35.6s, cache=MISS, selection=6.9993s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = 0.0330 (f1_before=0.7327, f1_after=0.6997, time=1.1s, cache=MISS, selection=0.0530s)
  - im: F1 Drop = 0.0270 (f1_before=0.7327, f1_after=0.7057, time=95.9s, cache=MISS, selection=94.6729s)
  - hybrid: F1 Drop = 0.0270 (f1_before=0.7312, f1_after=0.7042, time=15.9s, cache=MISS, selection=14.7189s)
  - random: F1 Drop = 0.0255 (f1_before=0.7282, f1_after=0.7027, time=1.9s, cache=MISS, selection=0.0030s)
  - pagerank: F1 Drop = 0.0225 (f1_before=0.7297, f1_after=0.7072, time=1.1s, cache=MISS, selection=0.0410s)
  - tracin: F1 Drop = 0.0180 (f1_before=0.7252, f1_after=0.7072, time=15.8s, cache=MISS, selection=14.6065s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:47] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - random: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.8s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.001013s, speedup=2.96x)
  - degree: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=MISS, selection=0.0210s)
  - pagerank: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=HIT(key=6460c53b924fd6f49294630114f1e052), selection=0.0410s, reuse=0.000988s, speedup=41.50x)
  - tracin: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=9.9s, cache=MISS, selection=9.2185s)
  - im: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=0.6s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1877 (f1_before=0.0000, f1_after=0.1877, time=16.8s, cache=MISS, selection=15.5033s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:47] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = -0.0570 (f1_before=0.6817, f1_after=0.7387, time=31.6s, cache=HIT(key=6460c53b924fd6f49294630114f1e052), selection=0.0410s, reuse=0.001001s, speedup=40.96x)
  - degree: F1 Drop = -0.0885 (f1_before=0.6577, f1_after=0.7462, time=27.9s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0961 (f1_before=0.6607, f1_after=0.7568, time=28.7s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.000000s)
  - im: F1 Drop = -0.1096 (f1_before=0.6351, f1_after=0.7447, time=29.4s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1111 (f1_before=0.6547, f1_after=0.7658, time=39.7s, cache=MISS, selection=12.4161s)
  - hybrid: F1 Drop = -0.1232 (f1_before=0.6396, f1_after=0.7628, time=41.5s, cache=MISS, selection=19.5374s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.0330 (f1_before=0.7342, f1_after=0.7012, time=16.5s, cache=MISS, selection=15.1098s)
  - random: F1 Drop = 0.0315 (f1_before=0.7327, f1_after=0.7012, time=1.6s, cache=MISS, selection=0.0000s)
  - pagerank: F1 Drop = 0.0300 (f1_before=0.7267, f1_after=0.6967, time=1.2s, cache=MISS, selection=0.0537s)
  - degree: F1 Drop = 0.0255 (f1_before=0.7252, f1_after=0.6997, time=1.3s, cache=MISS, selection=0.0260s)
  - im: F1 Drop = 0.0225 (f1_before=0.7267, f1_after=0.7042, time=89.3s, cache=MISS, selection=87.9903s)
  - tracin: F1 Drop = 0.0210 (f1_before=0.7252, f1_after=0.7042, time=11.0s, cache=MISS, selection=9.7584s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:48] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - random: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=1.1s, cache=HIT(key=dd631a6e85ab2aa173ab0bbb607ef87a), selection=0.0000s, reuse=0.002001s, speedup=0.00x)
  - degree: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=0.7s, cache=MISS, selection=0.0201s)
  - pagerank: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=0.6s, cache=HIT(key=c7a9408a94ad210c6dbe7bccf7094cbb), selection=0.0537s, reuse=0.001008s, speedup=53.24x)
  - tracin: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=9.7s, cache=MISS, selection=8.9617s)
  - im: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=0.7s, cache=HIT(key=109781dcf7a2e47f8929dbf47e9a7538), selection=87.9903s, reuse=0.001011s, speedup=87021.52x)
  - hybrid: F1 Drop = -0.2102 (f1_before=0.0000, f1_after=0.2102, time=15.6s, cache=MISS, selection=14.6525s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:48] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = -0.0570 (f1_before=0.6922, f1_after=0.7492, time=33.7s, cache=MISS, selection=9.5534s)
  - pagerank: F1 Drop = -0.0796 (f1_before=0.6712, f1_after=0.7508, time=23.3s, cache=HIT(key=c7a9408a94ad210c6dbe7bccf7094cbb), selection=0.0537s, reuse=0.000000s)
  - random: F1 Drop = -0.0916 (f1_before=0.6592, f1_after=0.7508, time=22.8s, cache=HIT(key=dd631a6e85ab2aa173ab0bbb607ef87a), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - hybrid: F1 Drop = -0.0991 (f1_before=0.6532, f1_after=0.7523, time=40.3s, cache=MISS, selection=15.8799s)
  - im: F1 Drop = -0.1051 (f1_before=0.6366, f1_after=0.7417, time=25.6s, cache=HIT(key=109781dcf7a2e47f8929dbf47e9a7538), selection=87.9903s, reuse=0.001000s, speedup=87990.30x)
  - degree: F1 Drop = -0.1141 (f1_before=0.6246, f1_after=0.7387, time=23.6s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:48] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0285 (f1_before=0.7312, f1_after=0.7027, time=1.3s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = 0.0285 (f1_before=0.7312, f1_after=0.7027, time=91.0s, cache=MISS, selection=89.6796s)
  - pagerank: F1 Drop = 0.0255 (f1_before=0.7342, f1_after=0.7087, time=1.1s, cache=MISS, selection=0.0350s)
  - hybrid: F1 Drop = 0.0240 (f1_before=0.7267, f1_after=0.7027, time=16.4s, cache=MISS, selection=15.3034s)
  - tracin: F1 Drop = 0.0240 (f1_before=0.7312, f1_after=0.7072, time=11.2s, cache=MISS, selection=10.1558s)
  - degree: F1 Drop = 0.0150 (f1_before=0.7222, f1_after=0.7072, time=1.0s, cache=MISS, selection=0.0201s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:48] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - random: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.9s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.000000s)
  - degree: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.6s, cache=MISS, selection=0.0220s)
  - pagerank: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.6s, cache=HIT(key=18702d1c5f448d2a6c93e480a04345c9), selection=0.0350s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=9.7s, cache=MISS, selection=9.0621s)
  - im: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=0.7s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1637 (f1_before=0.0000, f1_after=0.1637, time=16.4s, cache=MISS, selection=15.4302s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = -0.0600 (f1_before=0.6757, f1_after=0.7357, time=22.6s, cache=HIT(key=18702d1c5f448d2a6c93e480a04345c9), selection=0.0350s, reuse=0.001000s, speedup=35.00x)
  - tracin: F1 Drop = -0.0751 (f1_before=0.6787, f1_after=0.7538, time=30.7s, cache=MISS, selection=8.9019s)
  - degree: F1 Drop = -0.0810 (f1_before=0.6667, f1_after=0.7477, time=23.1s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0961 (f1_before=0.6456, f1_after=0.7417, time=21.8s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - im: F1 Drop = -0.1171 (f1_before=0.6246, f1_after=0.7417, time=21.7s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1172 (f1_before=0.6396, f1_after=0.7568, time=36.0s, cache=MISS, selection=15.3479s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = 0.0390 (f1_before=0.7387, f1_after=0.6997, time=1.0s, cache=MISS, selection=0.0370s)
  - random: F1 Drop = 0.0375 (f1_before=0.7372, f1_after=0.6997, time=1.3s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = 0.0375 (f1_before=0.7357, f1_after=0.6982, time=16.5s, cache=MISS, selection=15.1290s)
  - tracin: F1 Drop = 0.0330 (f1_before=0.7357, f1_after=0.7027, time=10.5s, cache=MISS, selection=9.4377s)
  - degree: F1 Drop = 0.0315 (f1_before=0.7327, f1_after=0.7012, time=1.0s, cache=MISS, selection=0.0210s)
  - im: F1 Drop = 0.0285 (f1_before=0.7297, f1_after=0.7012, time=85.4s, cache=MISS, selection=84.1961s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=1.3s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - degree: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.8s, cache=MISS, selection=0.0386s)
  - pagerank: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.8s, cache=HIT(key=311949fc36049248e5e42350470311dc), selection=0.0370s, reuse=0.000996s, speedup=37.15x)
  - tracin: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=12.8s, cache=MISS, selection=11.9380s)
  - im: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=0.9s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.1967 (f1_before=0.0000, f1_after=0.1967, time=22.5s, cache=MISS, selection=21.2586s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = -0.0660 (f1_before=0.6727, f1_after=0.7387, time=29.4s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.001001s, speedup=84111.99x)
  - random: F1 Drop = -0.0690 (f1_before=0.6697, f1_after=0.7387, time=28.9s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.002000s, speedup=0.00x)
  - tracin: F1 Drop = -0.0780 (f1_before=0.6622, f1_after=0.7402, time=41.5s, cache=MISS, selection=12.3114s)
  - degree: F1 Drop = -0.0841 (f1_before=0.6667, f1_after=0.7508, time=32.4s, cache=MISS, selection=0.0010s)
  - hybrid: F1 Drop = -0.0931 (f1_before=0.6637, f1_after=0.7568, time=47.6s, cache=MISS, selection=19.4022s)
  - pagerank: F1 Drop = -0.1322 (f1_before=0.6216, f1_after=0.7538, time=30.9s, cache=HIT(key=311949fc36049248e5e42350470311dc), selection=0.0370s, reuse=0.001004s, speedup=36.85x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.0315 (f1_before=0.7297, f1_after=0.6982, time=1.3s, cache=MISS, selection=0.0300s)
  - im: F1 Drop = 0.0315 (f1_before=0.7342, f1_after=0.7027, time=111.9s, cache=MISS, selection=110.5862s)
  - pagerank: F1 Drop = 0.0270 (f1_before=0.7357, f1_after=0.7087, time=1.4s, cache=MISS, selection=0.0476s)
  - tracin: F1 Drop = 0.0270 (f1_before=0.7327, f1_after=0.7057, time=14.4s, cache=MISS, selection=12.9156s)
  - hybrid: F1 Drop = 0.0240 (f1_before=0.7297, f1_after=0.7057, time=16.1s, cache=MISS, selection=14.9396s)
  - random: F1 Drop = 0.0210 (f1_before=0.7327, f1_after=0.7117, time=1.6s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.9s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - degree: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.7s, cache=MISS, selection=0.0210s)
  - pagerank: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.6s, cache=HIT(key=756e60c61d74eba56d02877703f9f0ce), selection=0.0476s, reuse=0.000000s)
  - tracin: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=9.7s, cache=MISS, selection=9.0975s)
  - im: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=0.6s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.2087 (f1_before=0.0000, f1_after=0.2087, time=16.3s, cache=MISS, selection=15.2594s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = -0.0615 (f1_before=0.6862, f1_after=0.7477, time=25.2s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = -0.0915 (f1_before=0.6562, f1_after=0.7477, time=33.2s, cache=MISS, selection=9.6950s)
  - random: F1 Drop = -0.0946 (f1_before=0.6577, f1_after=0.7523, time=25.4s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.001004s, speedup=0.00x)
  - im: F1 Drop = -0.0946 (f1_before=0.6562, f1_after=0.7508, time=22.6s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.001001s, speedup=110475.72x)
  - hybrid: F1 Drop = -0.1111 (f1_before=0.6351, f1_after=0.7462, time=38.1s, cache=MISS, selection=15.3157s)
  - pagerank: F1 Drop = -0.1142 (f1_before=0.6426, f1_after=0.7568, time=24.6s, cache=HIT(key=756e60c61d74eba56d02877703f9f0ce), selection=0.0476s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 18:59] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0517 (f1_before=0.8782, f1_after=0.8266, time=523.7s, cache=MISS, selection=522.1562s)
  - random: F1 Drop = 0.0498 (f1_before=0.8801, f1_after=0.8303, time=2.1s, cache=MISS, selection=0.0000s)
  - degree: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=1.7s, cache=MISS, selection=0.0220s)
  - tracin: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=13.3s, cache=MISS, selection=11.4796s)
  - hybrid: F1 Drop = 0.0461 (f1_before=0.8856, f1_after=0.8395, time=19.6s, cache=MISS, selection=17.7847s)
  - pagerank: F1 Drop = 0.0351 (f1_before=0.8856, f1_after=0.8506, time=1.8s, cache=MISS, selection=0.0353s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:00] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.2435 (f1_before=0.8819, f1_after=0.6384, time=12.1s, cache=MISS, selection=10.4923s)
  - degree: F1 Drop = 0.1753 (f1_before=0.8819, f1_after=0.7066, time=1.6s, cache=MISS, selection=0.0200s)
  - im: F1 Drop = 0.1587 (f1_before=0.8875, f1_after=0.7288, time=1.7s, cache=HIT(key=7999f51fca809266b56854d7b77a5a2d), selection=522.1562s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.1052 (f1_before=0.8745, f1_after=0.7694, time=1.6s, cache=HIT(key=4a0e0d20f02de17bd56d6064d03825ad), selection=0.0353s, reuse=0.001001s, speedup=35.28x)
  - random: F1 Drop = 0.1033 (f1_before=0.8801, f1_after=0.7768, time=1.9s, cache=HIT(key=965fa46eddcbf0eb47385e24c9073fd0), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0849 (f1_before=0.8893, f1_after=0.8044, time=20.9s, cache=MISS, selection=19.1713s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:03] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = -0.0720 (f1_before=0.7694, f1_after=0.8413, time=25.6s, cache=HIT(key=4a0e0d20f02de17bd56d6064d03825ad), selection=0.0353s, reuse=0.000000s)
  - tracin: F1 Drop = -0.0867 (f1_before=0.7694, f1_after=0.8561, time=36.2s, cache=MISS, selection=11.5036s)
  - hybrid: F1 Drop = -0.0904 (f1_before=0.7601, f1_after=0.8506, time=45.3s, cache=MISS, selection=20.2151s)
  - im: F1 Drop = -0.1033 (f1_before=0.7546, f1_after=0.8579, time=26.2s, cache=HIT(key=7999f51fca809266b56854d7b77a5a2d), selection=522.1562s, reuse=0.000000s)
  - degree: F1 Drop = -0.1070 (f1_before=0.7601, f1_after=0.8672, time=24.6s, cache=MISS, selection=0.0000s)
  - random: F1 Drop = -0.1310 (f1_before=0.7085, f1_after=0.8395, time=24.4s, cache=HIT(key=965fa46eddcbf0eb47385e24c9073fd0), selection=0.0000s, reuse=0.001002s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:12] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = 0.0590 (f1_before=0.8911, f1_after=0.8321, time=1.7s, cache=MISS, selection=0.0200s)
  - pagerank: F1 Drop = 0.0572 (f1_before=0.8930, f1_after=0.8358, time=1.7s, cache=MISS, selection=0.0379s)
  - tracin: F1 Drop = 0.0572 (f1_before=0.8875, f1_after=0.8303, time=13.0s, cache=MISS, selection=11.2832s)
  - random: F1 Drop = 0.0443 (f1_before=0.8838, f1_after=0.8395, time=1.9s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = 0.0406 (f1_before=0.8782, f1_after=0.8376, time=19.5s, cache=MISS, selection=17.7935s)
  - im: F1 Drop = 0.0332 (f1_before=0.8838, f1_after=0.8506, time=523.0s, cache=MISS, selection=521.2681s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1697 (f1_before=0.8838, f1_after=0.7140, time=1.6s, cache=HIT(key=04e99b7ed8ba23d49ec6ff8f7f6d9d8c), selection=0.0379s, reuse=0.000000s)
  - hybrid: F1 Drop = 0.1439 (f1_before=0.8893, f1_after=0.7454, time=20.6s, cache=MISS, selection=18.6838s)
  - random: F1 Drop = 0.1218 (f1_before=0.8893, f1_after=0.7675, time=2.1s, cache=HIT(key=2db70d9e6e71011b3c771c1139b223b4), selection=0.0000s, reuse=0.001001s, speedup=0.00x)
  - degree: F1 Drop = 0.0959 (f1_before=0.8893, f1_after=0.7934, time=1.6s, cache=MISS, selection=0.0110s)
  - tracin: F1 Drop = 0.0720 (f1_before=0.8801, f1_after=0.8081, time=11.9s, cache=MISS, selection=10.3478s)
  - im: F1 Drop = 0.0498 (f1_before=0.8930, f1_after=0.8432, time=1.6s, cache=HIT(key=8f419effaa59f8769443ba3ded85b986), selection=521.2681s, reuse=0.001001s, speedup=520685.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:16] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = -0.0664 (f1_before=0.7952, f1_after=0.8616, time=24.5s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0793 (f1_before=0.7768, f1_after=0.8561, time=23.9s, cache=HIT(key=2db70d9e6e71011b3c771c1139b223b4), selection=0.0000s, reuse=0.001002s, speedup=0.00x)
  - im: F1 Drop = -0.0812 (f1_before=0.7712, f1_after=0.8524, time=26.4s, cache=HIT(key=8f419effaa59f8769443ba3ded85b986), selection=521.2681s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.0904 (f1_before=0.7638, f1_after=0.8542, time=46.4s, cache=MISS, selection=19.8396s)
  - tracin: F1 Drop = -0.1181 (f1_before=0.7288, f1_after=0.8469, time=36.0s, cache=MISS, selection=11.2511s)
  - pagerank: F1 Drop = -0.1292 (f1_before=0.7343, f1_after=0.8635, time=24.3s, cache=HIT(key=04e99b7ed8ba23d49ec6ff8f7f6d9d8c), selection=0.0379s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:26] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = 0.0572 (f1_before=0.8856, f1_after=0.8284, time=1.7s, cache=MISS, selection=0.0206s)
  - tracin: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=13.4s, cache=MISS, selection=11.6515s)
  - hybrid: F1 Drop = 0.0535 (f1_before=0.8875, f1_after=0.8339, time=18.9s, cache=MISS, selection=17.2724s)
  - pagerank: F1 Drop = 0.0498 (f1_before=0.8856, f1_after=0.8358, time=1.8s, cache=MISS, selection=0.0380s)
  - im: F1 Drop = 0.0406 (f1_before=0.8856, f1_after=0.8450, time=521.6s, cache=MISS, selection=519.9285s)
  - random: F1 Drop = 0.0351 (f1_before=0.8838, f1_after=0.8487, time=1.9s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:27] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1458 (f1_before=0.8801, f1_after=0.7343, time=1.6s, cache=HIT(key=186e4c19d2727c8f092924f692e52ac0), selection=519.9285s, reuse=0.000987s, speedup=526621.16x)
  - tracin: F1 Drop = 0.1365 (f1_before=0.8856, f1_after=0.7491, time=11.6s, cache=MISS, selection=10.0040s)
  - random: F1 Drop = 0.1218 (f1_before=0.8838, f1_after=0.7620, time=1.8s, cache=HIT(key=11edb024ec4398d3ca7b0a60af0a44b7), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - degree: F1 Drop = 0.1181 (f1_before=0.8893, f1_after=0.7712, time=1.5s, cache=MISS, selection=0.0080s)
  - hybrid: F1 Drop = 0.1052 (f1_before=0.8819, f1_after=0.7768, time=20.3s, cache=MISS, selection=18.5037s)
  - pagerank: F1 Drop = 0.0775 (f1_before=0.8893, f1_after=0.8118, time=1.5s, cache=HIT(key=1d13a066ed1aac00e4fa912d7d212619), selection=0.0380s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:30] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - random: F1 Drop = -0.0756 (f1_before=0.7749, f1_after=0.8506, time=23.4s, cache=HIT(key=11edb024ec4398d3ca7b0a60af0a44b7), selection=0.0000s, reuse=0.000000s)
  - im: F1 Drop = -0.0830 (f1_before=0.7601, f1_after=0.8432, time=26.0s, cache=HIT(key=186e4c19d2727c8f092924f692e52ac0), selection=519.9285s, reuse=0.000000s)
  - degree: F1 Drop = -0.0867 (f1_before=0.7768, f1_after=0.8635, time=23.6s, cache=MISS, selection=0.0000s)
  - pagerank: F1 Drop = -0.0886 (f1_before=0.7731, f1_after=0.8616, time=24.2s, cache=HIT(key=1d13a066ed1aac00e4fa912d7d212619), selection=0.0380s, reuse=0.000000s)
  - tracin: F1 Drop = -0.1310 (f1_before=0.7435, f1_after=0.8745, time=35.5s, cache=MISS, selection=11.0276s)
  - hybrid: F1 Drop = -0.1550 (f1_before=0.7048, f1_after=0.8598, time=45.3s, cache=MISS, selection=19.9495s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:39] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.0664 (f1_before=0.8801, f1_after=0.8137, time=18.8s, cache=MISS, selection=17.1120s)
  - degree: F1 Drop = 0.0609 (f1_before=0.8893, f1_after=0.8284, time=1.6s, cache=MISS, selection=0.0200s)
  - pagerank: F1 Drop = 0.0535 (f1_before=0.8893, f1_after=0.8358, time=1.7s, cache=MISS, selection=0.0360s)
  - random: F1 Drop = 0.0461 (f1_before=0.8819, f1_after=0.8358, time=1.9s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = 0.0406 (f1_before=0.8856, f1_after=0.8450, time=12.9s, cache=MISS, selection=11.1560s)
  - im: F1 Drop = 0.0258 (f1_before=0.8819, f1_after=0.8561, time=510.2s, cache=MISS, selection=508.6033s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:40] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = 0.1605 (f1_before=0.8819, f1_after=0.7214, time=1.5s, cache=MISS, selection=0.0220s)
  - pagerank: F1 Drop = 0.1587 (f1_before=0.8911, f1_after=0.7325, time=1.6s, cache=HIT(key=69333254b0755586770aa1763edf476b), selection=0.0360s, reuse=0.000000s)
  - im: F1 Drop = 0.1384 (f1_before=0.8911, f1_after=0.7528, time=1.6s, cache=HIT(key=1038fcc2464ffdf965f0582b8d969b83), selection=508.6033s, reuse=0.001001s, speedup=508034.50x)
  - random: F1 Drop = 0.1052 (f1_before=0.8819, f1_after=0.7768, time=1.9s, cache=HIT(key=847f7c6ffea6f96f834a706272a1f9a5), selection=0.0000s, reuse=0.001011s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0701 (f1_before=0.8819, f1_after=0.8118, time=20.0s, cache=MISS, selection=18.2000s)
  - tracin: F1 Drop = 0.0683 (f1_before=0.8875, f1_after=0.8192, time=11.4s, cache=MISS, selection=9.8491s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:43] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = -0.0646 (f1_before=0.7731, f1_after=0.8376, time=32.8s, cache=MISS, selection=10.3269s)
  - hybrid: F1 Drop = -0.0720 (f1_before=0.8007, f1_after=0.8727, time=42.5s, cache=MISS, selection=19.0647s)
  - im: F1 Drop = -0.0867 (f1_before=0.7731, f1_after=0.8598, time=22.8s, cache=HIT(key=1038fcc2464ffdf965f0582b8d969b83), selection=508.6033s, reuse=0.000000s)
  - degree: F1 Drop = -0.0978 (f1_before=0.7528, f1_after=0.8506, time=21.8s, cache=MISS, selection=0.0000s)
  - random: F1 Drop = -0.1125 (f1_before=0.7583, f1_after=0.8708, time=22.1s, cache=HIT(key=847f7c6ffea6f96f834a706272a1f9a5), selection=0.0000s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.1347 (f1_before=0.7085, f1_after=0.8432, time=23.2s, cache=HIT(key=69333254b0755586770aa1763edf476b), selection=0.0360s, reuse=0.001000s, speedup=36.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0701 (f1_before=0.8985, f1_after=0.8284, time=12.5s, cache=MISS, selection=10.7937s)
  - random: F1 Drop = 0.0609 (f1_before=0.8930, f1_after=0.8321, time=1.9s, cache=MISS, selection=0.0000s)
  - im: F1 Drop = 0.0480 (f1_before=0.8930, f1_after=0.8450, time=511.3s, cache=MISS, selection=509.6970s)
  - hybrid: F1 Drop = 0.0480 (f1_before=0.8856, f1_after=0.8376, time=18.6s, cache=MISS, selection=16.9581s)
  - pagerank: F1 Drop = 0.0351 (f1_before=0.8782, f1_after=0.8432, time=1.7s, cache=MISS, selection=0.0320s)
  - degree: F1 Drop = 0.0314 (f1_before=0.8838, f1_after=0.8524, time=1.6s, cache=MISS, selection=0.0200s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:53] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.1458 (f1_before=0.8838, f1_after=0.7380, time=11.6s, cache=MISS, selection=9.9749s)
  - pagerank: F1 Drop = 0.1421 (f1_before=0.8856, f1_after=0.7435, time=1.5s, cache=HIT(key=2d008fa42bcdb6837728d016a5863c0f), selection=0.0320s, reuse=0.000000s)
  - im: F1 Drop = 0.1199 (f1_before=0.8967, f1_after=0.7768, time=1.6s, cache=HIT(key=7c463b03c4a8fa904f594feb744d686c), selection=509.6970s, reuse=0.000000s)
  - degree: F1 Drop = 0.1052 (f1_before=0.8893, f1_after=0.7841, time=1.5s, cache=MISS, selection=0.0180s)
  - hybrid: F1 Drop = 0.1015 (f1_before=0.8948, f1_after=0.7934, time=19.8s, cache=MISS, selection=18.1329s)
  - random: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=1.8s, cache=HIT(key=3e8f3e45886778d02888e8b6a443ddc7), selection=0.0000s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = -0.0517 (f1_before=0.7989, f1_after=0.8506, time=22.1s, cache=HIT(key=2d008fa42bcdb6837728d016a5863c0f), selection=0.0320s, reuse=0.000996s, speedup=32.14x)
  - random: F1 Drop = -0.0775 (f1_before=0.7620, f1_after=0.8395, time=21.5s, cache=HIT(key=3e8f3e45886778d02888e8b6a443ddc7), selection=0.0000s, reuse=0.000000s)
  - hybrid: F1 Drop = -0.0830 (f1_before=0.7841, f1_after=0.8672, time=40.9s, cache=MISS, selection=18.8497s)
  - tracin: F1 Drop = -0.0923 (f1_before=0.7601, f1_after=0.8524, time=33.0s, cache=MISS, selection=10.1912s)
  - im: F1 Drop = -0.1107 (f1_before=0.7509, f1_after=0.8616, time=23.0s, cache=HIT(key=7c463b03c4a8fa904f594feb744d686c), selection=509.6970s, reuse=0.000988s, speedup=516133.35x)
  - degree: F1 Drop = -0.1144 (f1_before=0.7454, f1_after=0.8598, time=21.9s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:56] demo_attack.py - IDEA 攻击实验
- 任务：dataset=citeseer, model=GCN, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0465 (f1_before=0.7327, f1_after=0.6862, time=9.3s, cache=MISS, selection=8.2564s)
  - random: F1 Drop = 0.0435 (f1_before=0.7282, f1_after=0.6847, time=1.3s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.001036s, speedup=2.89x)
  - im: F1 Drop = 0.0375 (f1_before=0.7297, f1_after=0.6922, time=1.2s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.002002s, speedup=47283.52x)
  - hybrid: F1 Drop = 0.0330 (f1_before=0.7252, f1_after=0.6922, time=15.4s, cache=MISS, selection=14.0820s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:57] demo_attack.py - MEGU 攻击实验
- 任务：dataset=citeseer, model=GCN, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0315 (f1_before=0.7372, f1_after=0.7057, time=12.7s, cache=MISS, selection=11.2458s)
  - im: F1 Drop = 0.0300 (f1_before=0.7357, f1_after=0.7057, time=1.4s, cache=HIT(key=f980c4dad46eed23e9ce71efedc63687), selection=94.6729s, reuse=0.000990s, speedup=95614.50x)
  - hybrid: F1 Drop = 0.0180 (f1_before=0.7282, f1_after=0.7102, time=18.9s, cache=MISS, selection=17.2348s)
  - random: F1 Drop = 0.0090 (f1_before=0.7177, f1_after=0.7087, time=1.7s, cache=HIT(key=9d14b534bb024b25d6cfdcf99c4eca1e), selection=0.0030s, reuse=0.000998s, speedup=3.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=citeseer, model=GCN, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.0450 (f1_before=0.7267, f1_after=0.6817, time=1.2s, cache=HIT(key=109781dcf7a2e47f8929dbf47e9a7538), selection=87.9903s, reuse=0.000000s)
  - random: F1 Drop = 0.0405 (f1_before=0.7327, f1_after=0.6922, time=1.4s, cache=HIT(key=dd631a6e85ab2aa173ab0bbb607ef87a), selection=0.0000s, reuse=0.000998s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0405 (f1_before=0.7252, f1_after=0.6847, time=16.5s, cache=MISS, selection=15.0956s)
  - tracin: F1 Drop = 0.0390 (f1_before=0.7252, f1_after=0.6862, time=9.8s, cache=MISS, selection=8.7733s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:59] demo_attack.py - MEGU 攻击实验
- 任务：dataset=citeseer, model=GCN, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.0375 (f1_before=0.7447, f1_after=0.7072, time=1.5s, cache=HIT(key=109781dcf7a2e47f8929dbf47e9a7538), selection=87.9903s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0345 (f1_before=0.7402, f1_after=0.7057, time=15.2s, cache=MISS, selection=13.7209s)
  - random: F1 Drop = 0.0285 (f1_before=0.7387, f1_after=0.7102, time=1.7s, cache=HIT(key=dd631a6e85ab2aa173ab0bbb607ef87a), selection=0.0000s, reuse=0.001002s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0240 (f1_before=0.7342, f1_after=0.7102, time=19.8s, cache=MISS, selection=17.9680s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 19:59] demo_attack.py - IDEA 攻击实验
- 任务：dataset=citeseer, model=GCN, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0511 (f1_before=0.7312, f1_after=0.6802, time=1.3s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.001108s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0375 (f1_before=0.7312, f1_after=0.6937, time=16.9s, cache=MISS, selection=15.5013s)
  - im: F1 Drop = 0.0360 (f1_before=0.7342, f1_after=0.6982, time=1.2s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.001001s, speedup=89621.98x)
  - tracin: F1 Drop = 0.0300 (f1_before=0.7222, f1_after=0.6922, time=10.3s, cache=MISS, selection=9.1798s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:00] demo_attack.py - MEGU 攻击实验
- 任务：dataset=citeseer, model=GCN, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.0285 (f1_before=0.7447, f1_after=0.7162, time=1.5s, cache=HIT(key=9bd7d3351eeceb3910647ef30e09d65c), selection=89.6796s, reuse=0.001000s, speedup=89686.09x)
  - hybrid: F1 Drop = 0.0255 (f1_before=0.7342, f1_after=0.7087, time=19.6s, cache=MISS, selection=17.7168s)
  - random: F1 Drop = 0.0225 (f1_before=0.7282, f1_after=0.7057, time=1.9s, cache=HIT(key=e544911d8ba5ec0776ded3460cf4d55b), selection=0.0000s, reuse=0.001001s, speedup=0.00x)
  - tracin: F1 Drop = 0.0225 (f1_before=0.7267, f1_after=0.7042, time=13.7s, cache=MISS, selection=11.9662s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=citeseer, model=GCN, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.0511 (f1_before=0.7372, f1_after=0.6862, time=1.5s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.001007s, speedup=0.00x)
  - im: F1 Drop = 0.0511 (f1_before=0.7387, f1_after=0.6877, time=1.3s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.001000s, speedup=84182.16x)
  - tracin: F1 Drop = 0.0450 (f1_before=0.7327, f1_after=0.6877, time=10.5s, cache=MISS, selection=9.3518s)
  - hybrid: F1 Drop = 0.0435 (f1_before=0.7357, f1_after=0.6922, time=16.8s, cache=MISS, selection=15.3573s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:01] demo_attack.py - MEGU 攻击实验
- 任务：dataset=citeseer, model=GCN, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.0315 (f1_before=0.7357, f1_after=0.7042, time=20.2s, cache=MISS, selection=18.2237s)
  - tracin: F1 Drop = 0.0300 (f1_before=0.7402, f1_after=0.7102, time=13.8s, cache=MISS, selection=12.1507s)
  - random: F1 Drop = 0.0255 (f1_before=0.7372, f1_after=0.7117, time=1.7s, cache=HIT(key=408a817782aab10ab0036de4f7d4e982), selection=0.0000s, reuse=0.001009s, speedup=0.00x)
  - im: F1 Drop = 0.0180 (f1_before=0.7312, f1_after=0.7132, time=1.5s, cache=HIT(key=17de2a757fe32933ce27a9a94ea978ad), selection=84.1961s, reuse=0.001003s, speedup=83922.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=citeseer, model=GCN, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0405 (f1_before=0.7297, f1_after=0.6892, time=10.6s, cache=MISS, selection=9.4987s)
  - random: F1 Drop = 0.0345 (f1_before=0.7327, f1_after=0.6982, time=1.4s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.001007s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0330 (f1_before=0.7327, f1_after=0.6997, time=17.0s, cache=MISS, selection=15.5995s)
  - im: F1 Drop = 0.0300 (f1_before=0.7357, f1_after=0.7057, time=1.3s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.001995s, speedup=55422.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:03] demo_attack.py - MEGU 攻击实验
- 任务：dataset=citeseer, model=GCN, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (166 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.0315 (f1_before=0.7447, f1_after=0.7132, time=1.5s, cache=HIT(key=6fa496d8a245311fc5df3ea3bd656938), selection=110.5862s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0300 (f1_before=0.7447, f1_after=0.7147, time=13.6s, cache=MISS, selection=12.0796s)
  - random: F1 Drop = 0.0270 (f1_before=0.7372, f1_after=0.7102, time=1.8s, cache=HIT(key=4d35f9ae318e1875cedb5797d953687e), selection=0.0000s, reuse=0.000999s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0255 (f1_before=0.7372, f1_after=0.7117, time=19.8s, cache=MISS, selection=17.9889s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:04] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.0572 (f1_before=0.8893, f1_after=0.8321, time=23.8s, cache=MISS, selection=21.6388s)
  - random: F1 Drop = 0.0498 (f1_before=0.8801, f1_after=0.8303, time=2.2s, cache=HIT(key=965fa46eddcbf0eb47385e24c9073fd0), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - tracin: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=14.4s, cache=MISS, selection=12.2782s)
  - im: F1 Drop = 0.0351 (f1_before=0.8856, f1_after=0.8506, time=2.0s, cache=HIT(key=7999f51fca809266b56854d7b77a5a2d), selection=522.1562s, reuse=0.001001s, speedup=521696.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0166 (f1_before=0.8875, f1_after=0.8708, time=1.9s, cache=HIT(key=7999f51fca809266b56854d7b77a5a2d), selection=522.1562s, reuse=0.001011s, speedup=516650.62x)
  - random: F1 Drop = 0.0166 (f1_before=0.8801, f1_after=0.8635, time=2.0s, cache=HIT(key=965fa46eddcbf0eb47385e24c9073fd0), selection=0.0000s, reuse=0.000998s, speedup=0.00x)
  - tracin: F1 Drop = 0.0111 (f1_before=0.8893, f1_after=0.8782, time=12.8s, cache=MISS, selection=10.9331s)
  - hybrid: F1 Drop = 0.0037 (f1_before=0.8653, f1_after=0.8616, time=22.2s, cache=MISS, selection=20.0575s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:05] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.0535 (f1_before=0.8893, f1_after=0.8358, time=2.1s, cache=HIT(key=2db70d9e6e71011b3c771c1139b223b4), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - tracin: F1 Drop = 0.0535 (f1_before=0.8930, f1_after=0.8395, time=13.9s, cache=MISS, selection=11.9614s)
  - im: F1 Drop = 0.0498 (f1_before=0.8875, f1_after=0.8376, time=1.9s, cache=HIT(key=8f419effaa59f8769443ba3ded85b986), selection=521.2681s, reuse=0.000999s, speedup=521554.56x)
  - hybrid: F1 Drop = 0.0461 (f1_before=0.8856, f1_after=0.8395, time=22.7s, cache=MISS, selection=20.7041s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.0221 (f1_before=0.8745, f1_after=0.8524, time=21.8s, cache=MISS, selection=19.7019s)
  - im: F1 Drop = 0.0129 (f1_before=0.8782, f1_after=0.8653, time=1.8s, cache=HIT(key=8f419effaa59f8769443ba3ded85b986), selection=521.2681s, reuse=0.000986s, speedup=528744.06x)
  - random: F1 Drop = 0.0037 (f1_before=0.8782, f1_after=0.8745, time=2.1s, cache=HIT(key=2db70d9e6e71011b3c771c1139b223b4), selection=0.0000s, reuse=0.001000s, speedup=0.00x)
  - tracin: F1 Drop = -0.0055 (f1_before=0.8653, f1_after=0.8708, time=12.7s, cache=MISS, selection=10.9019s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.0590 (f1_before=0.8875, f1_after=0.8284, time=23.1s, cache=MISS, selection=20.9513s)
  - tracin: F1 Drop = 0.0572 (f1_before=0.8856, f1_after=0.8284, time=13.4s, cache=MISS, selection=11.5237s)
  - im: F1 Drop = 0.0498 (f1_before=0.8819, f1_after=0.8321, time=1.9s, cache=HIT(key=186e4c19d2727c8f092924f692e52ac0), selection=519.9285s, reuse=0.001000s, speedup=520090.20x)
  - random: F1 Drop = 0.0443 (f1_before=0.8856, f1_after=0.8413, time=2.1s, cache=HIT(key=11edb024ec4398d3ca7b0a60af0a44b7), selection=0.0000s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:08] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0111 (f1_before=0.8819, f1_after=0.8708, time=2.0s, cache=HIT(key=11edb024ec4398d3ca7b0a60af0a44b7), selection=0.0000s, reuse=0.001001s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0092 (f1_before=0.8856, f1_after=0.8764, time=21.9s, cache=MISS, selection=19.7928s)
  - tracin: F1 Drop = 0.0074 (f1_before=0.8764, f1_after=0.8690, time=12.6s, cache=MISS, selection=10.7631s)
  - im: F1 Drop = 0.0000 (f1_before=0.8745, f1_after=0.8745, time=1.8s, cache=HIT(key=186e4c19d2727c8f092924f692e52ac0), selection=519.9285s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0664 (f1_before=0.8875, f1_after=0.8210, time=13.6s, cache=MISS, selection=11.7662s)
  - im: F1 Drop = 0.0535 (f1_before=0.8893, f1_after=0.8358, time=1.9s, cache=HIT(key=1038fcc2464ffdf965f0582b8d969b83), selection=508.6033s, reuse=0.000999s, speedup=508882.84x)
  - random: F1 Drop = 0.0498 (f1_before=0.8801, f1_after=0.8303, time=2.1s, cache=HIT(key=847f7c6ffea6f96f834a706272a1f9a5), selection=0.0000s, reuse=0.000000s)
  - hybrid: F1 Drop = 0.0387 (f1_before=0.8838, f1_after=0.8450, time=22.9s, cache=MISS, selection=20.8891s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:10] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0148 (f1_before=0.8838, f1_after=0.8690, time=12.8s, cache=MISS, selection=10.8990s)
  - im: F1 Drop = 0.0055 (f1_before=0.8801, f1_after=0.8745, time=1.8s, cache=HIT(key=1038fcc2464ffdf965f0582b8d969b83), selection=508.6033s, reuse=0.001002s, speedup=507551.00x)
  - random: F1 Drop = -0.0018 (f1_before=0.8745, f1_after=0.8764, time=2.1s, cache=HIT(key=847f7c6ffea6f96f834a706272a1f9a5), selection=0.0000s, reuse=0.000998s, speedup=0.00x)
  - hybrid: F1 Drop = -0.0037 (f1_before=0.8690, f1_after=0.8727, time=21.8s, cache=MISS, selection=19.7956s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.0664 (f1_before=0.8911, f1_after=0.8247, time=23.0s, cache=MISS, selection=20.8857s)
  - random: F1 Drop = 0.0590 (f1_before=0.8911, f1_after=0.8321, time=2.1s, cache=HIT(key=3e8f3e45886778d02888e8b6a443ddc7), selection=0.0000s, reuse=0.000000s)
  - im: F1 Drop = 0.0443 (f1_before=0.8838, f1_after=0.8395, time=2.0s, cache=HIT(key=7c463b03c4a8fa904f594feb744d686c), selection=509.6970s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0314 (f1_before=0.8801, f1_after=0.8487, time=14.1s, cache=MISS, selection=12.1458s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-21 20:11] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0295 (f1_before=0.8967, f1_after=0.8672, time=1.9s, cache=HIT(key=3e8f3e45886778d02888e8b6a443ddc7), selection=0.0000s, reuse=0.001001s, speedup=0.00x)
  - hybrid: F1 Drop = 0.0221 (f1_before=0.8930, f1_after=0.8708, time=22.0s, cache=MISS, selection=19.8708s)
  - im: F1 Drop = 0.0203 (f1_before=0.8856, f1_after=0.8653, time=1.7s, cache=HIT(key=7c463b03c4a8fa904f594feb744d686c), selection=509.6970s, reuse=0.001000s, speedup=509491.02x)
  - tracin: F1 Drop = 0.0185 (f1_before=0.8856, f1_after=0.8672, time=12.5s, cache=MISS, selection=10.7083s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 01:00] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - random: F1 Drop = -0.0312 (f1_before=0.7841, f1_after=0.8154, time=18.8s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001000s, speedup=1428.94x)
  - tracin: F1 Drop = -0.0409 (f1_before=0.7823, f1_after=0.8232, time=38.8s, cache=MISS, selection=7.6158s)
  - hybrid: F1 Drop = -0.0802 (f1_before=0.7435, f1_after=0.8238, time=46.1s, cache=MISS, selection=17.5884s)
  - im: F1 Drop = -0.0869 (f1_before=0.7472, f1_after=0.8341, time=21.5s, cache=HIT(key=db6701aad57f888288e28aca1477903c), selection=559.5546s, reuse=0.000995s, speedup=562411.24x)
  - pagerank: F1 Drop = -0.0872 (f1_before=0.7528, f1_after=0.8399, time=19.1s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.001000s, speedup=1130.55x)
  - degree: F1 Drop = -0.1183 (f1_before=0.7214, f1_after=0.8397, time=20.4s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-02-22 06:01:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.55% |    0.2948 |   15.41% |
| degree   | 16.91% |    0.3529 |   21.58% |
| pagerank | 16.26% |    0.3912 |   16.91% |
| tracin   | 12.15% |    0.1614 |   14.52% |
| im       | 12.58% |    0.3255 |   18.17% |
| hybrid   | 12.03% |    0.1654 |   14.23% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260222_060159.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:02:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 9.15% |    0.3025 |   12.15% |
| degree   | 21.24% |    0.4312 |   25.67% |
| pagerank | 9.26% |    0.3846 |   10.74% |
| tracin   | 12.31% |    0.1300 |   11.96% |
| im       | 9.64% |    0.3355 |   13.39% |
| hybrid   | 13.04% |    0.1601 |   14.67% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260222_060228.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:02:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.23% |    0.4413 |   12.82% |
| degree   | 8.87% |    0.3422 |   10.74% |
| pagerank | 10.27% |    0.4056 |   12.88% |
| tracin   | 11.79% |    0.1670 |   14.82% |
| im       | 7.31% |    0.2392 |   10.68% |
| hybrid   | 15.79% |    0.1763 |   17.97% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260222_060257.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:03:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.64% |    0.3288 |    9.30% |
| degree   | 20.62% |    0.3801 |   24.94% |
| pagerank | 11.11% |    0.4064 |   15.26% |
| tracin   | 14.16% |    0.1990 |   14.52% |
| im       | 8.61% |    0.2443 |   12.95% |
| hybrid   | 11.97% |    0.1518 |   13.64% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260222_060326.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:03:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 23.59% |    0.3606 |   26.98% |
| degree   | 20.00% |    0.4053 |   26.35% |
| pagerank | 10.47% |    0.4409 |   12.10% |
| tracin   | 12.72% |    0.1582 |   12.36% |
| im       | 23.19% |    0.4571 |   25.95% |
| hybrid   | 9.28% |    0.1547 |   12.16% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260222_060357.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:04:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0130 |    1.07% |
| degree   | 0.21% |    0.0141 |    1.17% |
| pagerank | 0.41% |    0.0152 |    1.51% |
| tracin   | -2.35% |    0.0151 |    0.79% |
| im       | -1.26% |    0.0152 |    1.23% |
| hybrid   | -0.84% |    0.0168 |    1.03% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260222_060424.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:04:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0152 |    0.87% |
| degree   | 1.03% |    0.0157 |    1.17% |
| pagerank | 1.85% |    0.0145 |    0.73% |
| tracin   | -1.91% |    0.0159 |    0.98% |
| im       | -1.89% |    0.0150 |    1.08% |
| hybrid   | -0.42% |    0.0172 |    1.03% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260222_060451.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:05:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0126 |    1.26% |
| degree   | 0.21% |    0.0159 |    1.51% |
| pagerank | 0.21% |    0.0159 |    1.41% |
| tracin   | -1.89% |    0.0160 |    1.18% |
| im       | -1.05% |    0.0148 |    1.23% |
| hybrid   | -0.42% |    0.0167 |    0.94% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260222_060516.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:05:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0131 |    0.83% |
| degree   | 0.41% |    0.0180 |    1.31% |
| pagerank | 1.44% |    0.0136 |    1.02% |
| tracin   | -1.69% |    0.0166 |    1.08% |
| im       | -1.91% |    0.0141 |    1.08% |
| hybrid   | -0.63% |    0.0176 |    1.23% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260222_060544.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:06:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0150 |    0.97% |
| degree   | 0.42% |    0.0159 |    1.56% |
| pagerank | 1.23% |    0.0152 |    1.31% |
| tracin   | -3.65% |    0.0160 |    1.38% |
| im       | 1.03% |    0.0154 |    0.98% |
| hybrid   | -1.47% |    0.0160 |    0.94% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260222_060610.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:11:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.2142 |   20.76% |
| degree   | -2.93% |    0.2419 |   24.06% |
| pagerank | 0.00% |    0.2671 |   26.48% |
| tracin   | 4.54% |    0.2008 |   16.94% |
| im       | 2.53% |    0.1996 |   18.37% |
| hybrid   | -1.19% |    0.2309 |   21.57% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260222_061112.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:16:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.43% |    0.2590 |   26.53% |
| degree   | -0.47% |    0.2086 |   19.54% |
| pagerank | -6.40% |    0.2346 |   22.50% |
| tracin   | 6.11% |    0.2176 |   20.24% |
| im       | 2.48% |    0.1778 |   16.74% |
| hybrid   | -0.71% |    0.2319 |   22.26% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260222_061623.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:21:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.64% |    0.2486 |   26.81% |
| degree   | 1.67% |    0.1957 |   19.54% |
| pagerank | 3.70% |    0.2369 |   23.52% |
| tracin   | -6.18% |    0.2216 |   20.58% |
| im       | 3.78% |    0.2762 |   27.92% |
| hybrid   | 1.13% |    0.2299 |   21.02% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260222_062139.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:27:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.61% |    0.2461 |   24.68% |
| degree   | -1.84% |    0.2045 |   19.83% |
| pagerank | 3.27% |    0.2797 |   26.92% |
| tracin   | -0.71% |    0.2000 |   18.76% |
| im       | -5.67% |    0.2192 |   21.86% |
| hybrid   | -1.17% |    0.2125 |   21.42% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260222_062740.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 06:33:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.47% |    0.2087 |   20.76% |
| degree   | -0.24% |    0.2133 |   20.71% |
| pagerank | 0.92% |    0.2276 |   21.91% |
| tracin   | 0.98% |    0.2504 |   25.21% |
| im       | -1.15% |    0.2159 |   21.37% |
| hybrid   | -6.24% |    0.2244 |   22.40% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260222_063313.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:15:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -9.97% |    0.2693 |   28.49% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_171527.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:27:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.90% |    0.2456 |   24.74% |
| degree   | -1.26% |    0.2860 |   28.49% |
| pagerank | -4.83% |    0.2554 |   24.59% |
| tracin   | -10.11% |    0.2585 |   27.38% |
| im       | -7.85% |    0.2744 |   28.71% |
| hybrid   | 4.20% |    0.2669 |   27.57% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_172739.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:34:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.07% |    0.2740 |   30.47% |
| degree   | -6.83% |    0.2660 |   24.36% |
| pagerank | 0.00% |    0.2385 |   24.59% |
| tracin   | 0.50% |    0.2914 |   29.10% |
| im       | 4.95% |    0.2454 |   24.27% |
| hybrid   | 6.56% |    0.2672 |   26.44% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_173452.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:42:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.50% |    0.2504 |   23.80% |
| degree   | -10.46% |    0.2792 |   29.56% |
| pagerank | 5.22% |    0.2800 |   28.33% |
| tracin   | 3.82% |    0.2893 |   26.98% |
| im       | 8.82% |    0.2680 |   28.06% |
| hybrid   | 11.06% |    0.2617 |   27.23% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_174200.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:49:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.21% |    0.2668 |   25.17% |
| degree   | 1.16% |    0.2791 |   25.57% |
| pagerank | -14.01% |    0.2479 |   26.92% |
| tracin   | 6.97% |    0.2519 |   26.64% |
| im       | -3.49% |    0.2269 |   22.26% |
| hybrid   | 9.91% |    0.3136 |   33.33% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_174915.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:55:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -9.97% |    0.2693 |   28.49% |
| degree   | -2.78% |    0.2993 |   31.16% |
| pagerank | 1.72% |    0.2702 |   28.28% |
| tracin   | 2.43% |    0.2553 |   25.85% |
| im       | -1.77% |    0.2638 |   25.26% |
| hybrid   | -5.69% |    0.2521 |   25.11% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260222_175518.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:55:44] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.66% |    0.0239 |    3.27% |
| degree   | 0.61% |    0.0259 |    3.52% |
| pagerank | 1.21% |    0.0248 |    3.56% |
| tracin   | -2.74% |    0.0391 |    2.69% |
| im       | -0.21% |    0.0255 |    3.21% |
| hybrid   | -1.25% |    0.0300 |    4.09% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260222_175544.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:56:10] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0246 |    3.47% |
| degree   | 0.41% |    0.0243 |    3.96% |
| pagerank | 2.62% |    0.0243 |    2.92% |
| tracin   | 0.41% |    0.0419 |    2.93% |
| im       | -1.66% |    0.0253 |    3.41% |
| hybrid   | -2.32% |    0.0301 |    4.53% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260222_175610.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:56:35] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0241 |    3.36% |
| degree   | 0.00% |    0.0238 |    3.17% |
| pagerank | 1.43% |    0.0237 |    3.32% |
| tracin   | -0.82% |    0.0373 |    2.36% |
| im       | 0.21% |    0.0259 |    3.65% |
| hybrid   | -3.36% |    0.0286 |    3.77% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260222_175635.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:57:01] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.41% |    0.0249 |    3.92% |
| degree   | 1.02% |    0.0269 |    3.80% |
| pagerank | 1.21% |    0.0231 |    3.64% |
| tracin   | -1.04% |    0.0382 |    2.44% |
| im       | -1.65% |    0.0266 |    3.97% |
| hybrid   | -1.24% |    0.0273 |    3.49% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260222_175701.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:57:27] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0242 |    3.13% |
| degree   | 0.81% |    0.0233 |    3.45% |
| pagerank | 0.61% |    0.0241 |    3.83% |
| tracin   | -0.20% |    0.0363 |    2.40% |
| im       | -1.02% |    0.0241 |    3.57% |
| hybrid   | 0.61% |    0.0270 |    4.21% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260222_175727.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:57:57] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.2483 |    9.38% |
| degree   | 4.87% |    0.1414 |    7.56% |
| pagerank | 3.64% |    0.2257 |    8.93% |
| tracin   | 2.19% |    0.0643 |    5.57% |
| im       | 0.62% |    0.0556 |    6.25% |
| hybrid   | 7.65% |    0.1221 |   12.06% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260222_175757.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:58:27] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.93% |    0.1543 |   12.78% |
| degree   | 12.45% |    0.1957 |   14.65% |
| pagerank | 6.05% |    0.1821 |    8.77% |
| tracin   | 2.42% |    0.0978 |    5.97% |
| im       | -0.62% |    0.0592 |    5.45% |
| hybrid   | 1.83% |    0.0983 |    6.57% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260222_175827.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:58:58] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.26% |    0.1557 |    9.92% |
| degree   | 4.07% |    0.1586 |    9.86% |
| pagerank | 2.82% |    0.1911 |   10.51% |
| tracin   | 2.00% |    0.0789 |    5.65% |
| im       | -1.04% |    0.0549 |    4.81% |
| hybrid   | -1.02% |    0.1513 |    7.70% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260222_175858.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:59:28] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.27% |    0.1732 |   11.36% |
| degree   | 12.78% |    0.2043 |   14.10% |
| pagerank | 11.38% |    0.2145 |   16.05% |
| tracin   | 1.42% |    0.0760 |    6.65% |
| im       | 0.83% |    0.0622 |    5.25% |
| hybrid   | 5.06% |    0.1404 |    9.90% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260222_175928.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 17:59:58] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.05% |    0.2105 |    9.15% |
| degree   | 13.70% |    0.1897 |   14.73% |
| pagerank | 4.87% |    0.2038 |   10.12% |
| tracin   | 2.04% |    0.1041 |    6.57% |
| im       | -1.24% |    0.0621 |    4.97% |
| hybrid   | 5.61% |    0.1002 |    9.98% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260222_175958.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:05:12] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.66% |    0.2897 |   28.50% |
| degree   | 5.20% |    0.3084 |   30.18% |
| pagerank | 0.92% |    0.2921 |   29.05% |
| tracin   | 8.04% |    0.3007 |   28.70% |
| im       | 3.82% |    0.3314 |   32.51% |
| hybrid   | -2.95% |    0.2903 |   28.98% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260222_180512.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:10:30] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.34% |    0.3120 |   30.95% |
| degree   | 5.42% |    0.2836 |   28.36% |
| pagerank | -3.26% |    0.3045 |   31.11% |
| tracin   | 0.89% |    0.2742 |   26.97% |
| im       | -1.37% |    0.3162 |   31.50% |
| hybrid   | 1.16% |    0.2851 |   28.66% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260222_181030.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:15:44] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.14% |    0.3321 |   33.54% |
| degree   | 8.39% |    0.3485 |   34.30% |
| pagerank | -0.44% |    0.2902 |   28.42% |
| tracin   | -3.03% |    0.2830 |   26.13% |
| im       | 1.82% |    0.2849 |   28.02% |
| hybrid   | 8.46% |    0.2966 |   29.86% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260222_181544.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:20:58] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.47% |    0.2908 |   28.53% |
| degree   | 2.38% |    0.2716 |   26.93% |
| pagerank | -3.53% |    0.2840 |   28.74% |
| tracin   | -13.33% |    0.2803 |   28.18% |
| im       | 1.56% |    0.2924 |   28.50% |
| hybrid   | -0.22% |    0.2578 |   24.41% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260222_182058.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:26:07] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.80% |    0.2691 |   26.10% |
| degree   | 0.21% |    0.2612 |   24.67% |
| pagerank | -5.69% |    0.3181 |   31.34% |
| tracin   | -4.25% |    0.3136 |   31.50% |
| im       | -0.46% |    0.3103 |   30.42% |
| hybrid   | 2.57% |    0.2885 |   28.54% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260222_182607.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:26:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0304 |    2.91% |
| degree   | 1.04% |    0.0300 |    2.92% |
| pagerank | -1.25% |    0.0282 |    2.14% |
| tracin   | -0.84% |    0.0317 |    2.26% |
| im       | -1.06% |    0.0303 |    2.41% |
| hybrid   | -1.48% |    0.0311 |    2.26% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260222_182643.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:27:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0297 |    2.52% |
| degree   | 2.06% |    0.0275 |    1.99% |
| pagerank | 1.85% |    0.0287 |    2.67% |
| tracin   | -1.05% |    0.0388 |    3.00% |
| im       | -0.63% |    0.0261 |    2.17% |
| hybrid   | -1.05% |    0.0283 |    2.51% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260222_182718.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:27:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0271 |    2.14% |
| degree   | 2.44% |    0.0270 |    1.94% |
| pagerank | 0.83% |    0.0281 |    1.90% |
| tracin   | -0.63% |    0.0318 |    2.07% |
| im       | -2.76% |    0.0277 |    2.22% |
| hybrid   | -1.05% |    0.0316 |    2.61% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260222_182753.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:28:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.52% |    0.0318 |    3.44% |
| degree   | 2.05% |    0.0258 |    1.99% |
| pagerank | 0.00% |    0.0265 |    2.53% |
| tracin   | 0.00% |    0.0306 |    1.87% |
| im       | -2.99% |    0.0309 |    2.56% |
| hybrid   | 0.00% |    0.0283 |    2.22% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260222_182827.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:29:02] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0294 |    2.86% |
| degree   | -1.26% |    0.0292 |    2.43% |
| pagerank | 0.00% |    0.0264 |    2.38% |
| tracin   | 0.00% |    0.0341 |    2.61% |
| im       | -2.78% |    0.0310 |    2.66% |
| hybrid   | -1.26% |    0.0315 |    2.90% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260222_182902.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:29:39] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.40% |    0.2899 |   12.82% |
| degree   | 24.23% |    0.2854 |   27.42% |
| pagerank | 30.72% |    0.3569 |   32.41% |
| tracin   | 12.01% |    0.1830 |   16.20% |
| im       | 11.70% |    0.2857 |   16.79% |
| hybrid   | 11.72% |    0.1857 |   13.79% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260222_182939.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:30:15] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 26.39% |    0.2824 |   30.59% |
| degree   | 9.73% |    0.1813 |   14.78% |
| pagerank | 15.20% |    0.2693 |   17.88% |
| tracin   | 8.75% |    0.1715 |   12.60% |
| im       | 15.89% |    0.3300 |   20.43% |
| hybrid   | 15.45% |    0.1992 |   17.48% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260222_183015.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:30:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 18.14% |    0.3347 |   24.04% |
| degree   | 18.43% |    0.2458 |   22.65% |
| pagerank | 11.80% |    0.2359 |   14.82% |
| tracin   | 13.77% |    0.1768 |   15.46% |
| im       | 3.95% |    0.2103 |    7.24% |
| hybrid   | 14.70% |    0.2010 |   18.56% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260222_183053.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:31:29] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.74% |    0.1987 |   12.94% |
| degree   | 17.78% |    0.2985 |   21.63% |
| pagerank | 7.71% |    0.2141 |   11.47% |
| tracin   | 9.85% |    0.1451 |   11.13% |
| im       | 13.55% |    0.2509 |   20.78% |
| hybrid   | 11.68% |    0.1579 |   13.69% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260222_183129.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:32:04] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 19.33% |    0.3283 |   21.90% |
| degree   | 13.84% |    0.2589 |   16.63% |
| pagerank | 12.66% |    0.2817 |   17.78% |
| tracin   | 8.83% |    0.1489 |   13.84% |
| im       | 19.87% |    0.2572 |   23.73% |
| hybrid   | 15.48% |    0.2107 |   19.69% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260222_183204.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:37:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.53% |    0.2411 |   20.59% |
| degree   | -7.83% |    0.2702 |   29.12% |
| pagerank | -0.49% |    0.2617 |   25.46% |
| tracin   | -3.20% |    0.2652 |   27.03% |
| im       | -1.46% |    0.2559 |   24.22% |
| hybrid   | 2.69% |    0.2452 |   22.99% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260222_183759.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:44:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.46% |    0.2528 |   26.56% |
| degree   | 4.35% |    0.2471 |   25.77% |
| pagerank | 2.27% |    0.2533 |   25.22% |
| tracin   | 8.25% |    0.3247 |   32.64% |
| im       | 6.38% |    0.3092 |   31.12% |
| hybrid   | 9.95% |    0.2729 |   27.23% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260222_184401.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:49:58] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.72% |    0.2883 |   27.54% |
| degree   | 3.27% |    0.2646 |   27.61% |
| pagerank | -15.71% |    0.2772 |   28.23% |
| tracin   | 3.23% |    0.2587 |   26.14% |
| im       | 9.30% |    0.2734 |   25.70% |
| hybrid   | -2.36% |    0.2792 |   28.26% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260222_184958.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 18:55:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.67% |    0.2709 |   27.00% |
| degree   | 2.83% |    0.2732 |   25.04% |
| pagerank | -4.69% |    0.3232 |   31.92% |
| tracin   | -8.57% |    0.2693 |   27.77% |
| im       | -3.07% |    0.2208 |   20.38% |
| hybrid   | 1.48% |    0.2602 |   28.41% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260222_185550.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:01:17] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -4.46% |    0.2733 |   27.62% |
| degree   | 1.96% |    0.2460 |   26.74% |
| pagerank | -0.99% |    0.2416 |   24.30% |
| tracin   | -1.00% |    0.2476 |   26.59% |
| im       | 0.00% |    0.2648 |   24.96% |
| hybrid   | 0.96% |    0.2667 |   27.33% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260222_190117.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:01:37] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.25% |    0.0262 |    3.43% |
| tracin   | 0.00% |    0.0373 |    2.57% |
| im       | 0.21% |    0.0258 |    3.57% |
| hybrid   | -1.46% |    0.0294 |    3.69% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260222_190137.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:01:57] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0253 |    3.79% |
| tracin   | -1.45% |    0.0363 |    2.61% |
| im       | -1.23% |    0.0272 |    3.21% |
| hybrid   | -0.83% |    0.0284 |    3.25% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260222_190157.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:02:17] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.22% |    0.0241 |    3.40% |
| tracin   | -0.61% |    0.0382 |    2.24% |
| im       | -1.46% |    0.0255 |    3.45% |
| hybrid   | -5.08% |    0.0291 |    3.17% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260222_190217.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:02:37] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.50% |    0.0269 |    3.88% |
| tracin   | -2.31% |    0.0401 |    2.48% |
| im       | -0.83% |    0.0247 |    3.41% |
| hybrid   | -0.41% |    0.0257 |    3.25% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260222_190237.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:02:57] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.83% |    0.0253 |    3.72% |
| tracin   | -0.41% |    0.0362 |    2.32% |
| im       | -1.65% |    0.0257 |    3.93% |
| hybrid   | -2.51% |    0.0277 |    3.65% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260222_190257.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:03:18] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.45% |    0.0287 |    3.98% |
| tracin   | 0.00% |    0.0441 |    3.05% |
| im       | -1.04% |    0.0320 |    3.93% |
| hybrid   | -2.28% |    0.0336 |    3.65% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260222_190318.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:03:40] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.20% |    0.0260 |    3.59% |
| tracin   | -0.82% |    0.0376 |    2.77% |
| im       | -2.70% |    0.0292 |    3.89% |
| hybrid   | -0.41% |    0.0281 |    3.45% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260222_190340.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:04:00] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.23% |    0.0372 |    4.62% |
| tracin   | 1.22% |    0.0489 |    3.65% |
| im       | -0.83% |    0.0326 |    4.09% |
| hybrid   | -1.67% |    0.0280 |    3.85% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260222_190400.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:04:22] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0308 |    4.16% |
| tracin   | -2.30% |    0.0371 |    1.84% |
| im       | -3.11% |    0.0382 |    4.37% |
| hybrid   | -1.47% |    0.0309 |    3.09% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260222_190422.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:04:43] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0240 |    3.64% |
| tracin   | -0.21% |    0.0473 |    3.17% |
| im       | -0.21% |    0.0276 |    3.49% |
| hybrid   | -2.09% |    0.0280 |    3.49% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260222_190443.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:05:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.83% |    0.0334 |    3.11% |
| tracin   | -0.21% |    0.0365 |    2.02% |
| im       | 0.42% |    0.0304 |    2.71% |
| hybrid   | -0.21% |    0.0319 |    2.56% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260222_190509.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:05:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0280 |    2.76% |
| tracin   | -2.78% |    0.0292 |    1.33% |
| im       | -0.63% |    0.0283 |    2.36% |
| hybrid   | 0.84% |    0.0268 |    2.12% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260222_190535.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:06:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.41% |    0.0270 |    2.04% |
| tracin   | -2.77% |    0.0362 |    2.36% |
| im       | 1.04% |    0.0339 |    2.81% |
| hybrid   | 0.00% |    0.0319 |    2.41% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260222_190601.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:06:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0300 |    2.76% |
| tracin   | 0.21% |    0.0334 |    2.17% |
| im       | -1.48% |    0.0314 |    2.56% |
| hybrid   | 0.21% |    0.0387 |    3.35% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260222_190627.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:06:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0308 |    2.08% |
| tracin   | 0.21% |    0.0373 |    2.17% |
| im       | -1.48% |    0.0263 |    2.12% |
| hybrid   | 0.21% |    0.0321 |    2.95% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260222_190653.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:07:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.25% |    0.0867 |    4.18% |
| tracin   | -0.84% |    0.0444 |    2.81% |
| im       | 0.21% |    0.0647 |    4.48% |
| hybrid   | -1.04% |    0.0637 |    3.84% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260222_190718.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:07:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0518 |    3.30% |
| tracin   | 0.00% |    0.1012 |    3.79% |
| im       | -0.63% |    0.0588 |    4.23% |
| hybrid   | -0.84% |    0.0459 |    2.46% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260222_190742.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:08:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.08% |    0.0668 |    3.89% |
| tracin   | 0.00% |    0.0791 |    3.94% |
| im       | 1.47% |    0.0796 |    5.07% |
| hybrid   | -0.42% |    0.0494 |    2.61% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260222_190807.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:08:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.46% |    0.0558 |    3.93% |
| tracin   | 4.17% |    0.1050 |    4.63% |
| im       | 0.64% |    0.0907 |    6.94% |
| hybrid   | 2.08% |    0.0799 |    5.47% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260222_190831.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-22 19:08:56] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.66% |    0.0467 |    3.73% |
| tracin   | 0.63% |    0.0649 |    2.90% |
| im       | 2.31% |    0.0847 |    6.45% |
| hybrid   | -1.06% |    0.0676 |    3.74% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260222_190856.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-02-22 21:43] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000995s, speedup=1474.27x)
  - tracin: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=8.2s, cache=MISS, selection=7.1424s)
  - hybrid: F1 Drop = 0.0166 (f1_before=0.8838, f1_after=0.8672, time=16.4s, cache=MISS, selection=15.2937s)
  - im: F1 Drop = 0.0092 (f1_before=0.8911, f1_after=0.8819, time=0.9s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.001005s, speedup=512372.34x)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s, cache=MISS, selection=0.0190s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 21:44] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0277 (f1_before=0.8838, f1_after=0.8561, time=20.6s, cache=MISS, selection=19.6203s)
  - pagerank: F1 Drop = 0.0277 (f1_before=0.8893, f1_after=0.8616, time=0.8s, cache=MISS, selection=0.0319s)
  - tracin: F1 Drop = 0.0240 (f1_before=0.8911, f1_after=0.8672, time=6.9s, cache=MISS, selection=6.1373s)
  - random: F1 Drop = 0.0221 (f1_before=0.8838, f1_after=0.8616, time=1.1s, cache=MISS, selection=0.0000s)
  - hybrid: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=15.2s, cache=MISS, selection=14.0950s)
  - degree: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=0.8s, cache=MISS, selection=0.0220s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 22:04] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1458 (f1_before=0.8930, f1_after=0.7472, time=16.5s, cache=MISS, selection=14.9414s)
  - im: F1 Drop = 0.1440 (f1_before=0.8875, f1_after=0.7435, time=1.3s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.1034 (f1_before=0.8838, f1_after=0.7804, time=1.3s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.070315s, speedup=14.63x)
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=2.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=7.9s, cache=MISS, selection=6.5730s)
  - degree: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=1.3s, cache=MISS, selection=0.0428s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 22:05] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.1476 (f1_before=0.8875, f1_after=0.7399, time=8.7s, cache=MISS, selection=7.3013s)
  - im: F1 Drop = 0.1476 (f1_before=0.8930, f1_after=0.7454, time=1.4s, cache=HIT(key=356d862deda544f0be8d44c429fefcb6), selection=19.6203s, reuse=0.001505s, speedup=13039.70x)
  - random: F1 Drop = 0.1421 (f1_before=0.8838, f1_after=0.7417, time=1.6s, cache=HIT(key=b0768876888659d12661e2fba2d9f181), selection=0.0000s, reuse=0.002013s, speedup=0.00x)
  - hybrid: F1 Drop = 0.1384 (f1_before=0.8819, f1_after=0.7435, time=17.8s, cache=MISS, selection=16.4380s)
  - pagerank: F1 Drop = 0.1310 (f1_before=0.8838, f1_after=0.7528, time=1.5s, cache=HIT(key=1e86014f21d32064ef13966b53089d8b), selection=0.0319s, reuse=0.000000s)
  - degree: F1 Drop = 0.1292 (f1_before=0.8875, f1_after=0.7583, time=1.2s, cache=MISS, selection=0.0257s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 22:45] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = -0.0258 (f1_before=0.7934, f1_after=0.8192, time=34.7s, cache=MISS, selection=15.5197s)
  - im: F1 Drop = -0.0424 (f1_before=0.7989, f1_after=0.8413, time=18.6s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.001000s, speedup=514934.20x)
  - pagerank: F1 Drop = -0.0479 (f1_before=0.7897, f1_after=0.8376, time=20.1s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - degree: F1 Drop = -0.0812 (f1_before=0.7878, f1_after=0.8690, time=18.4s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=17.8s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - tracin: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=25.8s, cache=MISS, selection=6.5858s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 22:47] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0369 (f1_before=0.8081, f1_after=0.8450, time=25.5s, cache=MISS, selection=6.6444s)
  - hybrid: F1 Drop = -0.0461 (f1_before=0.8026, f1_after=0.8487, time=35.1s, cache=MISS, selection=15.3871s)
  - im: F1 Drop = -0.0480 (f1_before=0.7934, f1_after=0.8413, time=19.5s, cache=HIT(key=356d862deda544f0be8d44c429fefcb6), selection=19.6203s, reuse=0.001010s, speedup=19418.01x)
  - pagerank: F1 Drop = -0.0572 (f1_before=0.7897, f1_after=0.8469, time=19.8s, cache=HIT(key=1e86014f21d32064ef13966b53089d8b), selection=0.0319s, reuse=0.001002s, speedup=31.81x)
  - degree: F1 Drop = -0.0701 (f1_before=0.7878, f1_after=0.8579, time=18.9s, cache=MISS, selection=0.0000s)
  - random: F1 Drop = -0.0775 (f1_before=0.7694, f1_after=0.8469, time=17.7s, cache=HIT(key=b0768876888659d12661e2fba2d9f181), selection=0.0000s, reuse=0.001020s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 23:08] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = -0.0713 (f1_before=0.7657, f1_after=0.8370, time=37.7s, cache=MISS, selection=7.2103s)
  - random: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=16.7s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.0979 (f1_before=0.7435, f1_after=0.8414, time=17.6s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000990s, speedup=1039.19x)
  - hybrid: F1 Drop = -0.1339 (f1_before=0.7085, f1_after=0.8424, time=42.4s, cache=MISS, selection=16.0744s)
  - im: F1 Drop = -0.1507 (f1_before=0.6679, f1_after=0.8186, time=17.9s, cache=HIT(key=f8bb5e1e745afbb04088032a0dfafc70), selection=514.9342s, reuse=0.000000s)
  - degree: F1 Drop = -0.1513 (f1_before=0.6661, f1_after=0.8174, time=17.1s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-22 23:11] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = -0.0393 (f1_before=0.7768, f1_after=0.8160, time=55.8s, cache=MISS, selection=20.0731s)
  - tracin: F1 Drop = -0.0637 (f1_before=0.7694, f1_after=0.8331, time=51.6s, cache=MISS, selection=9.3169s)
  - random: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=23.8s, cache=HIT(key=b0768876888659d12661e2fba2d9f181), selection=0.0000s, reuse=0.000000s)
  - pagerank: F1 Drop = -0.0979 (f1_before=0.7435, f1_after=0.8414, time=23.5s, cache=HIT(key=1e86014f21d32064ef13966b53089d8b), selection=0.0319s, reuse=0.001004s, speedup=31.77x)
  - im: F1 Drop = -0.1492 (f1_before=0.6716, f1_after=0.8208, time=22.3s, cache=HIT(key=356d862deda544f0be8d44c429fefcb6), selection=19.6203s, reuse=0.001505s, speedup=13037.63x)
  - degree: F1 Drop = -0.1513 (f1_before=0.6661, f1_after=0.8174, time=27.1s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 15:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - im_v4: F1 Drop = 0.0129 (f1_before=0.8838, f1_after=0.8708, time=2.3s, cache=MISS, selection=1.0769s)
  - hybrid_v4: F1 Drop = 0.0092 (f1_before=0.8856, f1_after=0.8764, time=6.6s, cache=MISS, selection=5.7954s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 15:38] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im_v4: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=2.9s, cache=MISS, selection=1.0844s)
  - hybrid_v4: F1 Drop = 0.0627 (f1_before=0.8875, f1_after=0.8247, time=7.1s, cache=MISS, selection=5.8621s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 15:42] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im', 'im_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0129 (f1_before=0.8838, f1_after=0.8708, time=3.2s, cache=MISS, selection=1.8223s)
  - im_v4: F1 Drop = 0.0092 (f1_before=0.8856, f1_after=0.8764, time=1.8s, cache=MISS, selection=0.9731s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 15:42] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im', 'im_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=3.7s, cache=MISS, selection=1.9990s)
  - im_v4: F1 Drop = 0.0627 (f1_before=0.8875, f1_after=0.8247, time=2.2s, cache=MISS, selection=0.9773s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:35] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.1034 (f1_before=0.8838, f1_after=0.7804, time=1.3s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.070315s, speedup=14.63x)
  - random: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=2.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0923 (f1_before=0.8838, f1_after=0.7915, time=7.9s, cache=MISS, selection=6.5730s)
  - im_v4: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=2.7s, cache=MISS, selection=1.1484s)
  - hybrid_v4: F1 Drop = 0.0627 (f1_before=0.8875, f1_after=0.8247, time=8.6s, cache=MISS, selection=7.3692s)
  - degree: F1 Drop = 0.0554 (f1_before=0.8875, f1_after=0.8321, time=1.3s, cache=MISS, selection=0.0428s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:36] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.1s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000995s, speedup=1474.27x)
  - tracin: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=8.2s, cache=MISS, selection=7.1424s)
  - im_v4: F1 Drop = 0.0129 (f1_before=0.8838, f1_after=0.8708, time=1.0s, cache=HIT(key=740523b0ca18872055b4007aaa0360f0), selection=1.1484s, reuse=0.001005s, speedup=1142.51x)
  - hybrid_v4: F1 Drop = 0.0092 (f1_before=0.8856, f1_after=0.8764, time=7.5s, cache=MISS, selection=6.3699s)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s, cache=MISS, selection=0.0190s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:37] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = -0.0479 (f1_before=0.7897, f1_after=0.8376, time=20.1s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000000s)
  - im_v4: F1 Drop = -0.0701 (f1_before=0.7694, f1_after=0.8395, time=18.1s, cache=HIT(key=740523b0ca18872055b4007aaa0360f0), selection=1.1484s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = -0.0720 (f1_before=0.7841, f1_after=0.8561, time=25.7s, cache=MISS, selection=6.3983s)
  - degree: F1 Drop = -0.0812 (f1_before=0.7878, f1_after=0.8690, time=18.4s, cache=MISS, selection=0.0010s)
  - random: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=17.8s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - tracin: F1 Drop = -0.0830 (f1_before=0.7694, f1_after=0.8524, time=25.8s, cache=MISS, selection=6.5858s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:38] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=42
- 执行结果：
  - hybrid_v4: F1 Drop = -0.0414 (f1_before=0.7970, f1_after=0.8384, time=42.2s, cache=MISS, selection=7.2666s)
  - tracin: F1 Drop = -0.0713 (f1_before=0.7657, f1_after=0.8370, time=37.7s, cache=MISS, selection=7.2103s)
  - random: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=16.7s, cache=HIT(key=7371f3a57bd0ed670d90c6bebb239b85), selection=1.4669s, reuse=0.000000s)
  - im_v4: F1 Drop = -0.0757 (f1_before=0.7583, f1_after=0.8340, time=18.9s, cache=HIT(key=740523b0ca18872055b4007aaa0360f0), selection=1.1484s, reuse=0.001006s, speedup=1141.16x)
  - pagerank: F1 Drop = -0.0979 (f1_before=0.7435, f1_after=0.8414, time=17.6s, cache=HIT(key=80f00b75404756a7f9995bc18b86fade), selection=1.0288s, reuse=0.000990s, speedup=1039.19x)
  - degree: F1 Drop = -0.1513 (f1_before=0.6661, f1_after=0.8174, time=17.1s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:38] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1384 (f1_before=0.8893, f1_after=0.7509, time=1.4s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000992s, speedup=1139.31x)
  - random: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=1.8s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1415.76x)
  - tracin: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=8.9s, cache=MISS, selection=7.4003s)
  - degree: F1 Drop = 0.0868 (f1_before=0.8875, f1_after=0.8007, time=1.4s, cache=MISS, selection=0.0240s)
  - im_v4: F1 Drop = 0.0535 (f1_before=0.8856, f1_after=0.8321, time=3.2s, cache=MISS, selection=1.1590s)
  - hybrid_v4: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=8.7s, cache=MISS, selection=7.1933s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:39] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0203 (f1_before=0.8911, f1_after=0.8708, time=8.4s, cache=MISS, selection=7.4577s)
  - degree: F1 Drop = 0.0184 (f1_before=0.8911, f1_after=0.8727, time=1.0s, cache=MISS, selection=0.0190s)
  - im_v4: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=1.2s, cache=HIT(key=f463fe7cbaf66d291a73c8fe5fd03102), selection=1.1590s, reuse=0.000000s)
  - random: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=1.3s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1415.76x)
  - tracin: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=8.2s, cache=MISS, selection=7.1508s)
  - pagerank: F1 Drop = 0.0111 (f1_before=0.8893, f1_after=0.8782, time=0.9s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000990s, speedup=1141.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:40] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - hybrid_v4: F1 Drop = -0.0295 (f1_before=0.8100, f1_after=0.8395, time=26.4s, cache=MISS, selection=6.7537s)
  - random: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=19.9s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001000s, speedup=1428.50x)
  - tracin: F1 Drop = -0.0351 (f1_before=0.7915, f1_after=0.8266, time=29.5s, cache=MISS, selection=7.2580s)
  - degree: F1 Drop = -0.0406 (f1_before=0.8081, f1_after=0.8487, time=19.0s, cache=MISS, selection=0.0000s)
  - im_v4: F1 Drop = -0.0443 (f1_before=0.7915, f1_after=0.8358, time=20.7s, cache=HIT(key=f463fe7cbaf66d291a73c8fe5fd03102), selection=1.1590s, reuse=0.001000s, speedup=1158.80x)
  - pagerank: F1 Drop = -0.0701 (f1_before=0.7638, f1_after=0.8339, time=20.4s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000999s, speedup=1131.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 18:41] demo_attack.py - GUIDE 攻击实验
- 任务：dataset=cora, model=GCN, method=GUIDE, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - random: F1 Drop = -0.0313 (f1_before=0.7841, f1_after=0.8154, time=18.8s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001000s, speedup=1428.50x)
  - im_v4: F1 Drop = -0.0313 (f1_before=0.7841, f1_after=0.8154, time=17.9s, cache=HIT(key=f463fe7cbaf66d291a73c8fe5fd03102), selection=1.1590s, reuse=0.001005s, speedup=1153.23x)
  - hybrid_v4: F1 Drop = -0.0409 (f1_before=0.7823, f1_after=0.8232, time=37.9s, cache=MISS, selection=7.7451s)
  - tracin: F1 Drop = -0.0409 (f1_before=0.7823, f1_after=0.8232, time=38.8s, cache=MISS, selection=7.6158s)
  - pagerank: F1 Drop = -0.0871 (f1_before=0.7528, f1_after=0.8399, time=19.1s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.001000s, speedup=1130.20x)
  - degree: F1 Drop = -0.1183 (f1_before=0.7214, f1_after=0.8397, time=20.4s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-02-24 18:42:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.55% |    0.2948 |   15.41% |
| degree   | 16.91% |    0.3529 |   21.58% |
| pagerank | 16.26% |    0.3912 |   16.91% |
| tracin   | 12.15% |    0.1614 |   14.52% |
| im_v4    | 13.10% |    0.4088 |   16.79% |
| hybrid_v4 | 14.67% |    0.1740 |   12.90% |
| hybrid   | 12.03% |    0.1654 |   14.23% |
| im       | 12.58% |    0.3255 |   18.17% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_184203.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:42:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 9.15% |    0.3025 |   12.15% |
| degree   | 21.24% |    0.4312 |   25.67% |
| pagerank | 9.26% |    0.3846 |   10.74% |
| tracin   | 12.31% |    0.1300 |   11.96% |
| im_v4    | 16.28% |    0.3719 |   21.12% |
| hybrid_v4 | 12.50% |    0.2191 |   10.49% |
| hybrid   | 13.04% |    0.1601 |   14.67% |
| im       | 9.64% |    0.3355 |   13.39% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_184219.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:42:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.23% |    0.4413 |   12.82% |
| degree   | 8.87% |    0.3422 |   10.74% |
| pagerank | 10.27% |    0.4056 |   12.88% |
| tracin   | 11.79% |    0.1670 |   14.82% |
| hybrid   | 15.79% |    0.1763 |   17.97% |
| im       | 7.31% |    0.2392 |   10.68% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_184230.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:42:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.64% |    0.3288 |    9.30% |
| degree   | 20.62% |    0.3801 |   24.94% |
| pagerank | 11.11% |    0.4064 |   15.26% |
| tracin   | 14.16% |    0.1990 |   14.52% |
| hybrid   | 11.97% |    0.1518 |   13.64% |
| im       | 8.61% |    0.2443 |   12.95% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_184240.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:42:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 23.59% |    0.3606 |   26.98% |
| degree   | 20.00% |    0.4053 |   26.35% |
| pagerank | 10.47% |    0.4409 |   12.10% |
| tracin   | 12.72% |    0.1582 |   12.36% |
| hybrid   | 9.28% |    0.1547 |   12.16% |
| im       | 23.19% |    0.4571 |   25.95% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_184250.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:43:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0130 |    1.07% |
| degree   | 0.21% |    0.0141 |    1.17% |
| pagerank | 0.41% |    0.0152 |    1.51% |
| tracin   | -2.35% |    0.0151 |    0.79% |
| im_v4    | 0.41% |    0.0165 |    1.18% |
| hybrid_v4 | 0.21% |    0.0184 |    1.18% |
| hybrid   | -0.84% |    0.0168 |    1.03% |
| im       | -1.26% |    0.0152 |    1.23% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_184304.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:43:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0152 |    0.87% |
| degree   | 1.03% |    0.0157 |    1.17% |
| pagerank | 1.85% |    0.0145 |    0.73% |
| tracin   | -1.91% |    0.0159 |    0.98% |
| im_v4    | 0.00% |    0.0146 |    1.23% |
| hybrid_v4 | 1.03% |    0.0169 |    1.43% |
| hybrid   | -0.42% |    0.0172 |    1.03% |
| im       | -1.89% |    0.0150 |    1.08% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_184319.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:43:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0126 |    1.26% |
| degree   | 0.21% |    0.0159 |    1.51% |
| pagerank | 0.21% |    0.0159 |    1.41% |
| tracin   | -1.89% |    0.0160 |    1.18% |
| hybrid   | -0.42% |    0.0167 |    0.94% |
| im       | -1.05% |    0.0148 |    1.23% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_184329.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:43:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0131 |    0.83% |
| degree   | 0.41% |    0.0180 |    1.31% |
| pagerank | 1.44% |    0.0136 |    1.02% |
| tracin   | -1.69% |    0.0166 |    1.08% |
| hybrid   | -0.63% |    0.0176 |    1.23% |
| im       | -1.91% |    0.0141 |    1.08% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_184339.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:43:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0150 |    0.97% |
| degree   | 0.42% |    0.0159 |    1.56% |
| pagerank | 1.23% |    0.0152 |    1.31% |
| tracin   | -3.65% |    0.0160 |    1.38% |
| hybrid   | -1.47% |    0.0160 |    0.94% |
| im       | 1.03% |    0.0154 |    0.98% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_184349.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:45:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.2142 |   20.76% |
| degree   | -2.93% |    0.2419 |   24.06% |
| pagerank | 0.00% |    0.2671 |   26.48% |
| tracin   | 4.54% |    0.2008 |   16.94% |
| im_v4    | -1.65% |    0.2284 |   21.17% |
| hybrid_v4 | -0.92% |    0.2355 |   22.99% |
| hybrid   | -1.19% |    0.2309 |   21.57% |
| im       | 2.53% |    0.1996 |   18.37% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260224_184524.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:47:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.43% |    0.2590 |   26.53% |
| degree   | -0.47% |    0.2086 |   19.54% |
| pagerank | -6.40% |    0.2346 |   22.50% |
| tracin   | 6.11% |    0.2176 |   20.24% |
| im_v4    | 9.57% |    0.2354 |   22.11% |
| hybrid_v4 | 3.15% |    0.2216 |   20.48% |
| hybrid   | -0.71% |    0.2319 |   22.26% |
| im       | 2.48% |    0.1778 |   16.74% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260224_184707.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:47:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.64% |    0.2486 |   26.81% |
| degree   | 1.67% |    0.1957 |   19.54% |
| pagerank | 3.70% |    0.2369 |   23.52% |
| tracin   | -6.18% |    0.2216 |   20.58% |
| hybrid   | 1.13% |    0.2299 |   21.02% |
| im       | 3.78% |    0.2762 |   27.92% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260224_184717.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:47:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.61% |    0.2461 |   24.68% |
| degree   | -1.84% |    0.2045 |   19.83% |
| pagerank | 3.27% |    0.2797 |   26.92% |
| tracin   | -0.71% |    0.2000 |   18.76% |
| hybrid   | -1.17% |    0.2125 |   21.42% |
| im       | -5.67% |    0.2192 |   21.86% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260224_184728.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:47:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.47% |    0.2087 |   20.76% |
| degree   | -0.24% |    0.2133 |   20.71% |
| pagerank | 0.92% |    0.2276 |   21.91% |
| tracin   | 0.98% |    0.2504 |   25.21% |
| hybrid   | -6.24% |    0.2244 |   22.40% |
| im       | -1.15% |    0.2159 |   21.37% |
- 日志路径：`results\collateral\GraphEraser\cora\GCN\collateral_20260224_184738.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:49:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.90% |    0.2456 |   24.74% |
| degree   | -1.26% |    0.2860 |   28.49% |
| pagerank | -4.83% |    0.2554 |   24.59% |
| tracin   | -10.11% |    0.2585 |   27.38% |
| im_v4    | -2.76% |    0.2662 |   28.80% |
| hybrid_v4 | 2.86% |    0.2687 |   28.31% |
| hybrid   | 4.20% |    0.2669 |   27.57% |
| im       | -7.85% |    0.2744 |   28.71% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260224_184936.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:51:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.07% |    0.2740 |   30.47% |
| degree   | -6.83% |    0.2660 |   24.36% |
| pagerank | 0.00% |    0.2385 |   24.59% |
| tracin   | 0.50% |    0.2914 |   29.10% |
| im_v4    | -1.67% |    0.2403 |   23.49% |
| hybrid_v4 | -14.29% |    0.2683 |   28.46% |
| hybrid   | 6.56% |    0.2672 |   26.44% |
| im       | 4.95% |    0.2454 |   24.27% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260224_185132.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:51:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.50% |    0.2504 |   23.80% |
| degree   | -10.46% |    0.2792 |   29.56% |
| pagerank | 5.22% |    0.2800 |   28.33% |
| tracin   | 3.82% |    0.2893 |   26.98% |
| hybrid   | 11.06% |    0.2617 |   27.23% |
| im       | 8.82% |    0.2680 |   28.06% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260224_185142.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:51:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.21% |    0.2668 |   25.17% |
| degree   | 1.16% |    0.2791 |   25.57% |
| pagerank | -14.01% |    0.2479 |   26.92% |
| tracin   | 6.97% |    0.2519 |   26.64% |
| hybrid   | 9.91% |    0.3136 |   33.33% |
| im       | -3.49% |    0.2269 |   22.26% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260224_185152.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GUIDE, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -9.97% |    0.2693 |   28.49% |
| degree   | -2.78% |    0.2993 |   31.16% |
| pagerank | 1.72% |    0.2702 |   28.28% |
| tracin   | 2.43% |    0.2553 |   25.85% |
| hybrid   | -5.69% |    0.2521 |   25.11% |
| im       | -1.77% |    0.2638 |   25.26% |
- 日志路径：`results\collateral\GUIDE\cora\GCN\collateral_20260224_185202.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:13] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.66% |    0.0239 |    3.27% |
| degree   | 0.61% |    0.0259 |    3.52% |
| pagerank | 1.21% |    0.0248 |    3.56% |
| tracin   | -2.74% |    0.0391 |    2.69% |
| hybrid   | -1.25% |    0.0300 |    4.09% |
| im       | -0.21% |    0.0255 |    3.21% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260224_185213.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:23] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0246 |    3.47% |
| degree   | 0.41% |    0.0243 |    3.96% |
| pagerank | 2.62% |    0.0243 |    2.92% |
| tracin   | 0.41% |    0.0419 |    2.93% |
| hybrid   | -2.32% |    0.0301 |    4.53% |
| im       | -1.66% |    0.0253 |    3.41% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260224_185223.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:33] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0241 |    3.36% |
| degree   | 0.00% |    0.0238 |    3.17% |
| pagerank | 1.43% |    0.0237 |    3.32% |
| tracin   | -0.82% |    0.0373 |    2.36% |
| hybrid   | -3.36% |    0.0286 |    3.77% |
| im       | 0.21% |    0.0259 |    3.65% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260224_185233.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:43] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.41% |    0.0249 |    3.92% |
| degree   | 1.02% |    0.0269 |    3.80% |
| pagerank | 1.21% |    0.0231 |    3.64% |
| tracin   | -1.04% |    0.0382 |    2.44% |
| hybrid   | -1.24% |    0.0273 |    3.49% |
| im       | -1.65% |    0.0266 |    3.97% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260224_185243.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:52:52] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0242 |    3.13% |
| degree   | 0.81% |    0.0233 |    3.45% |
| pagerank | 0.61% |    0.0241 |    3.83% |
| tracin   | -0.20% |    0.0363 |    2.40% |
| hybrid   | 0.61% |    0.0270 |    4.21% |
| im       | -1.02% |    0.0241 |    3.57% |
- 日志路径：`results\collateral\GIF\citeseer\GCN\collateral_20260224_185252.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:02] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.2483 |    9.38% |
| degree   | 4.87% |    0.1414 |    7.56% |
| pagerank | 3.64% |    0.2257 |    8.93% |
| tracin   | 2.19% |    0.0643 |    5.57% |
| hybrid   | 7.65% |    0.1221 |   12.06% |
| im       | 0.62% |    0.0556 |    6.25% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260224_185302.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:12] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.93% |    0.1543 |   12.78% |
| degree   | 12.45% |    0.1957 |   14.65% |
| pagerank | 6.05% |    0.1821 |    8.77% |
| tracin   | 2.42% |    0.0978 |    5.97% |
| hybrid   | 1.83% |    0.0983 |    6.57% |
| im       | -0.62% |    0.0592 |    5.45% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260224_185312.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:22] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.26% |    0.1557 |    9.92% |
| degree   | 4.07% |    0.1586 |    9.86% |
| pagerank | 2.82% |    0.1911 |   10.51% |
| tracin   | 2.00% |    0.0789 |    5.65% |
| hybrid   | -1.02% |    0.1513 |    7.70% |
| im       | -1.04% |    0.0549 |    4.81% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260224_185322.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:32] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.27% |    0.1732 |   11.36% |
| degree   | 12.78% |    0.2043 |   14.10% |
| pagerank | 11.38% |    0.2145 |   16.05% |
| tracin   | 1.42% |    0.0760 |    6.65% |
| hybrid   | 5.06% |    0.1404 |    9.90% |
| im       | 0.83% |    0.0622 |    5.25% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260224_185332.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:42] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.05% |    0.2105 |    9.15% |
| degree   | 13.70% |    0.1897 |   14.73% |
| pagerank | 4.87% |    0.2038 |   10.12% |
| tracin   | 2.04% |    0.1041 |    6.57% |
| hybrid   | 5.61% |    0.1002 |    9.98% |
| im       | -1.24% |    0.0621 |    4.97% |
- 日志路径：`results\collateral\GNNDelete\citeseer\GCN\collateral_20260224_185342.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:53:51] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.66% |    0.2897 |   28.50% |
| degree   | 5.20% |    0.3084 |   30.18% |
| pagerank | 0.92% |    0.2921 |   29.05% |
| tracin   | 8.04% |    0.3007 |   28.70% |
| hybrid   | -2.95% |    0.2903 |   28.98% |
| im       | 3.82% |    0.3314 |   32.51% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260224_185351.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:01] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.34% |    0.3120 |   30.95% |
| degree   | 5.42% |    0.2836 |   28.36% |
| pagerank | -3.26% |    0.3045 |   31.11% |
| tracin   | 0.89% |    0.2742 |   26.97% |
| hybrid   | 1.16% |    0.2851 |   28.66% |
| im       | -1.37% |    0.3162 |   31.50% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260224_185401.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:11] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.14% |    0.3321 |   33.54% |
| degree   | 8.39% |    0.3485 |   34.30% |
| pagerank | -0.44% |    0.2902 |   28.42% |
| tracin   | -3.03% |    0.2830 |   26.13% |
| hybrid   | 8.46% |    0.2966 |   29.86% |
| im       | 1.82% |    0.2849 |   28.02% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260224_185411.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:20] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.47% |    0.2908 |   28.53% |
| degree   | 2.38% |    0.2716 |   26.93% |
| pagerank | -3.53% |    0.2840 |   28.74% |
| tracin   | -13.33% |    0.2803 |   28.18% |
| hybrid   | -0.22% |    0.2578 |   24.41% |
| im       | 1.56% |    0.2924 |   28.50% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260224_185420.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:30] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.80% |    0.2691 |   26.10% |
| degree   | 0.21% |    0.2612 |   24.67% |
| pagerank | -5.69% |    0.3181 |   31.34% |
| tracin   | -4.25% |    0.3136 |   31.50% |
| hybrid   | 2.57% |    0.2885 |   28.54% |
| im       | -0.46% |    0.3103 |   30.42% |
- 日志路径：`results\collateral\GraphEraser\citeseer\GCN\collateral_20260224_185430.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:41] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0304 |    2.91% |
| degree   | 1.04% |    0.0300 |    2.92% |
| pagerank | -1.25% |    0.0282 |    2.14% |
| tracin   | -0.84% |    0.0317 |    2.26% |
| hybrid   | -1.48% |    0.0311 |    2.26% |
| im       | -1.06% |    0.0303 |    2.41% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260224_185441.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:54:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0297 |    2.52% |
| degree   | 2.06% |    0.0275 |    1.99% |
| pagerank | 1.85% |    0.0287 |    2.67% |
| tracin   | -1.05% |    0.0388 |    3.00% |
| hybrid   | -1.05% |    0.0283 |    2.51% |
| im       | -0.63% |    0.0261 |    2.17% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260224_185450.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0271 |    2.14% |
| degree   | 2.44% |    0.0270 |    1.94% |
| pagerank | 0.83% |    0.0281 |    1.90% |
| tracin   | -0.63% |    0.0318 |    2.07% |
| hybrid   | -1.05% |    0.0316 |    2.61% |
| im       | -2.76% |    0.0277 |    2.22% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260224_185500.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.52% |    0.0318 |    3.44% |
| degree   | 2.05% |    0.0258 |    1.99% |
| pagerank | 0.00% |    0.0265 |    2.53% |
| tracin   | 0.00% |    0.0306 |    1.87% |
| hybrid   | 0.00% |    0.0283 |    2.22% |
| im       | -2.99% |    0.0309 |    2.56% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260224_185509.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:19] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0294 |    2.86% |
| degree   | -1.26% |    0.0292 |    2.43% |
| pagerank | 0.00% |    0.0264 |    2.38% |
| tracin   | 0.00% |    0.0341 |    2.61% |
| hybrid   | -1.26% |    0.0315 |    2.90% |
| im       | -2.78% |    0.0310 |    2.66% |
- 日志路径：`results\collateral\GIF\cora\GAT\collateral_20260224_185519.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:29] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.40% |    0.2899 |   12.82% |
| degree   | 24.23% |    0.2854 |   27.42% |
| pagerank | 30.72% |    0.3569 |   32.41% |
| tracin   | 12.01% |    0.1830 |   16.20% |
| hybrid   | 11.72% |    0.1857 |   13.79% |
| im       | 11.70% |    0.2857 |   16.79% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260224_185529.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 26.39% |    0.2824 |   30.59% |
| degree   | 9.73% |    0.1813 |   14.78% |
| pagerank | 15.20% |    0.2693 |   17.88% |
| tracin   | 8.75% |    0.1715 |   12.60% |
| hybrid   | 15.45% |    0.1992 |   17.48% |
| im       | 15.89% |    0.3300 |   20.43% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260224_185538.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:48] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 18.14% |    0.3347 |   24.04% |
| degree   | 18.43% |    0.2458 |   22.65% |
| pagerank | 11.80% |    0.2359 |   14.82% |
| tracin   | 13.77% |    0.1768 |   15.46% |
| hybrid   | 14.70% |    0.2010 |   18.56% |
| im       | 3.95% |    0.2103 |    7.24% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260224_185548.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:55:58] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.74% |    0.1987 |   12.94% |
| degree   | 17.78% |    0.2985 |   21.63% |
| pagerank | 7.71% |    0.2141 |   11.47% |
| tracin   | 9.85% |    0.1451 |   11.13% |
| hybrid   | 11.68% |    0.1579 |   13.69% |
| im       | 13.55% |    0.2509 |   20.78% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260224_185558.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 19.33% |    0.3283 |   21.90% |
| degree   | 13.84% |    0.2589 |   16.63% |
| pagerank | 12.66% |    0.2817 |   17.78% |
| tracin   | 8.83% |    0.1489 |   13.84% |
| hybrid   | 15.48% |    0.2107 |   19.69% |
| im       | 19.87% |    0.2572 |   23.73% |
- 日志路径：`results\collateral\GNNDelete\cora\GAT\collateral_20260224_185607.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:17] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.53% |    0.2411 |   20.59% |
| degree   | -7.83% |    0.2702 |   29.12% |
| pagerank | -0.49% |    0.2617 |   25.46% |
| tracin   | -3.20% |    0.2652 |   27.03% |
| hybrid   | 2.69% |    0.2452 |   22.99% |
| im       | -1.46% |    0.2559 |   24.22% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260224_185617.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.46% |    0.2528 |   26.56% |
| degree   | 4.35% |    0.2471 |   25.77% |
| pagerank | 2.27% |    0.2533 |   25.22% |
| tracin   | 8.25% |    0.3247 |   32.64% |
| hybrid   | 9.95% |    0.2729 |   27.23% |
| im       | 6.38% |    0.3092 |   31.12% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260224_185628.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.72% |    0.2883 |   27.54% |
| degree   | 3.27% |    0.2646 |   27.61% |
| pagerank | -15.71% |    0.2772 |   28.23% |
| tracin   | 3.23% |    0.2587 |   26.14% |
| hybrid   | -2.36% |    0.2792 |   28.26% |
| im       | 9.30% |    0.2734 |   25.70% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260224_185637.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:47] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -7.67% |    0.2709 |   27.00% |
| degree   | 2.83% |    0.2732 |   25.04% |
| pagerank | -4.69% |    0.3232 |   31.92% |
| tracin   | -8.57% |    0.2693 |   27.77% |
| hybrid   | 1.48% |    0.2602 |   28.41% |
| im       | -3.07% |    0.2208 |   20.38% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260224_185647.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:56:57] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -4.46% |    0.2733 |   27.62% |
| degree   | 1.96% |    0.2460 |   26.74% |
| pagerank | -0.99% |    0.2416 |   24.30% |
| tracin   | -1.00% |    0.2476 |   26.59% |
| hybrid   | 0.96% |    0.2667 |   27.33% |
| im       | 0.00% |    0.2648 |   24.96% |
- 日志路径：`results\collateral\GraphEraser\cora\GAT\collateral_20260224_185657.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:07] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.25% |    0.0262 |    3.43% |
| tracin   | 0.00% |    0.0373 |    2.57% |
| hybrid   | -1.46% |    0.0294 |    3.69% |
| im       | 0.21% |    0.0258 |    3.57% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260224_185707.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:16] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0253 |    3.79% |
| tracin   | -1.45% |    0.0363 |    2.61% |
| hybrid   | -0.83% |    0.0284 |    3.25% |
| im       | -1.23% |    0.0272 |    3.21% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260224_185716.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:26] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.22% |    0.0241 |    3.40% |
| tracin   | -0.61% |    0.0382 |    2.24% |
| hybrid   | -5.08% |    0.0291 |    3.17% |
| im       | -1.46% |    0.0255 |    3.45% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260224_185726.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:35] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.50% |    0.0269 |    3.88% |
| tracin   | -2.31% |    0.0401 |    2.48% |
| hybrid   | -0.41% |    0.0257 |    3.25% |
| im       | -0.83% |    0.0247 |    3.41% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260224_185735.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:45] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.83% |    0.0253 |    3.72% |
| tracin   | -0.41% |    0.0362 |    2.32% |
| hybrid   | -2.51% |    0.0277 |    3.65% |
| im       | -1.65% |    0.0257 |    3.93% |
- 日志路径：`results\collateral\IDEA\citeseer\GCN\collateral_20260224_185745.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:57:54] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.45% |    0.0287 |    3.98% |
| tracin   | 0.00% |    0.0441 |    3.05% |
| hybrid   | -2.28% |    0.0336 |    3.65% |
| im       | -1.04% |    0.0320 |    3.93% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260224_185754.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:04] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.20% |    0.0260 |    3.59% |
| tracin   | -0.82% |    0.0376 |    2.77% |
| hybrid   | -0.41% |    0.0281 |    3.45% |
| im       | -2.70% |    0.0292 |    3.89% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260224_185804.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:13] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.23% |    0.0372 |    4.62% |
| tracin   | 1.22% |    0.0489 |    3.65% |
| hybrid   | -1.67% |    0.0280 |    3.85% |
| im       | -0.83% |    0.0326 |    4.09% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260224_185813.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:23] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.41% |    0.0308 |    4.16% |
| tracin   | -2.30% |    0.0371 |    1.84% |
| hybrid   | -1.47% |    0.0309 |    3.09% |
| im       | -3.11% |    0.0382 |    4.37% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260224_185823.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:32] eval_collateral.py
- 任务：dataset=citeseer, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0240 |    3.64% |
| tracin   | -0.21% |    0.0473 |    3.17% |
| hybrid   | -2.09% |    0.0280 |    3.49% |
| im       | -0.21% |    0.0276 |    3.49% |
- 日志路径：`results\collateral\MEGU\citeseer\GCN\collateral_20260224_185832.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.83% |    0.0334 |    3.11% |
| tracin   | -0.21% |    0.0365 |    2.02% |
| hybrid   | -0.21% |    0.0319 |    2.56% |
| im       | 0.42% |    0.0304 |    2.71% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260224_185842.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:58:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0280 |    2.76% |
| tracin   | -2.78% |    0.0292 |    1.33% |
| hybrid   | 0.84% |    0.0268 |    2.12% |
| im       | -0.63% |    0.0283 |    2.36% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260224_185851.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.41% |    0.0270 |    2.04% |
| tracin   | -2.77% |    0.0362 |    2.36% |
| hybrid   | 0.00% |    0.0319 |    2.41% |
| im       | 1.04% |    0.0339 |    2.81% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260224_185900.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0300 |    2.76% |
| tracin   | 0.21% |    0.0334 |    2.17% |
| hybrid   | 0.21% |    0.0387 |    3.35% |
| im       | -1.48% |    0.0314 |    2.56% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260224_185909.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:19] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0308 |    2.08% |
| tracin   | 0.21% |    0.0373 |    2.17% |
| hybrid   | 0.21% |    0.0321 |    2.95% |
| im       | -1.48% |    0.0263 |    2.12% |
- 日志路径：`results\collateral\IDEA\cora\GAT\collateral_20260224_185919.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.25% |    0.0867 |    4.18% |
| tracin   | -0.84% |    0.0444 |    2.81% |
| hybrid   | -1.04% |    0.0637 |    3.84% |
| im       | 0.21% |    0.0647 |    4.48% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260224_185928.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0518 |    3.30% |
| tracin   | 0.00% |    0.1012 |    3.79% |
| hybrid   | -0.84% |    0.0459 |    2.46% |
| im       | -0.63% |    0.0588 |    4.23% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260224_185937.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:46] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.08% |    0.0668 |    3.89% |
| tracin   | 0.00% |    0.0791 |    3.94% |
| hybrid   | -0.42% |    0.0494 |    2.61% |
| im       | 1.47% |    0.0796 |    5.07% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260224_185946.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 18:59:55] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.46% |    0.0558 |    3.93% |
| tracin   | 4.17% |    0.1050 |    4.63% |
| hybrid   | 2.08% |    0.0799 |    5.47% |
| im       | 0.64% |    0.0907 |    6.94% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260224_185955.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:00:05] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.66% |    0.0467 |    3.73% |
| tracin   | 0.63% |    0.0649 |    2.90% |
| hybrid   | -1.06% |    0.0676 |    3.74% |
| im       | 2.31% |    0.0847 |    6.45% |
- 日志路径：`results\collateral\MEGU\cora\GAT\collateral_20260224_190005.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-02-24 19:00] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=0.9s, cache=MISS, selection=0.0371s)
  - random: F1 Drop = 0.0185 (f1_before=0.8838, f1_after=0.8653, time=1.4s, cache=MISS, selection=0.0021s)
  - im: F1 Drop = 0.0129 (f1_before=0.8838, f1_after=0.8708, time=4.5s, cache=MISS, selection=3.4510s)
  - hybrid: F1 Drop = 0.0092 (f1_before=0.8856, f1_after=0.8764, time=7.4s, cache=MISS, selection=6.5194s)
  - tracin: F1 Drop = 0.0092 (f1_before=0.8911, f1_after=0.8819, time=7.9s, cache=MISS, selection=7.0522s)
  - degree: F1 Drop = 0.0055 (f1_before=0.8856, f1_after=0.8801, time=0.9s, cache=MISS, selection=0.0375s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:00] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0517 (f1_before=0.8893, f1_after=0.8376, time=0.9s, cache=MISS, selection=0.0337s)
  - degree: F1 Drop = 0.0443 (f1_before=0.8856, f1_after=0.8413, time=0.9s, cache=MISS, selection=0.0259s)
  - im: F1 Drop = 0.0295 (f1_before=0.8838, f1_after=0.8542, time=3.5s, cache=MISS, selection=2.4161s)
  - tracin: F1 Drop = 0.0239 (f1_before=0.8911, f1_after=0.8672, time=7.9s, cache=MISS, selection=6.9881s)
  - hybrid: F1 Drop = 0.0221 (f1_before=0.8856, f1_after=0.8635, time=7.0s, cache=MISS, selection=6.0308s)
  - random: F1 Drop = 0.0074 (f1_before=0.8838, f1_after=0.8764, time=1.4s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1384 (f1_before=0.8875, f1_after=0.7491, time=7.7s, cache=MISS, selection=6.4536s)
  - im: F1 Drop = 0.1384 (f1_before=0.8838, f1_after=0.7454, time=1.7s, cache=HIT(key=6d5541cc84191181d48744e3ed2b2f97), selection=3.4510s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1347 (f1_before=0.8875, f1_after=0.7528, time=7.7s, cache=MISS, selection=6.4308s)
  - random: F1 Drop = 0.0886 (f1_before=0.8838, f1_after=0.7952, time=1.7s, cache=HIT(key=a757644323a45a56d4a9c783658a49b1), selection=0.0021s, reuse=0.000505s, speedup=4.16x)
  - pagerank: F1 Drop = 0.0831 (f1_before=0.8838, f1_after=0.8007, time=1.2s, cache=HIT(key=1a7db76cf77cdaf6326ffb96f8ec3fae), selection=0.0371s, reuse=0.001001s, speedup=37.06x)
  - degree: F1 Drop = 0.0572 (f1_before=0.8875, f1_after=0.8303, time=1.2s, cache=MISS, selection=0.0221s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = 0.1845 (f1_before=0.8875, f1_after=0.7030, time=1.2s, cache=MISS, selection=0.0173s)
  - hybrid: F1 Drop = 0.1827 (f1_before=0.8875, f1_after=0.7048, time=7.9s, cache=MISS, selection=6.5512s)
  - random: F1 Drop = 0.1735 (f1_before=0.8838, f1_after=0.7103, time=1.6s, cache=HIT(key=1c9b036b19bf1a1f6759bd185b6437f0), selection=0.0000s, reuse=0.001007s, speedup=0.00x)
  - tracin: F1 Drop = 0.1421 (f1_before=0.8875, f1_after=0.7454, time=7.2s, cache=MISS, selection=5.9993s)
  - im: F1 Drop = 0.0996 (f1_before=0.8838, f1_after=0.7841, time=1.7s, cache=HIT(key=edda5179c9203a24e19527556d012fb1), selection=2.4161s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=1.2s, cache=HIT(key=4bbe9fbefd8b6a68460cd22cf0ceb1bc), selection=0.0337s, reuse=0.001394s, speedup=24.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:01] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=212
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0295 (f1_before=0.8911, f1_after=0.8616, time=7.4s, cache=MISS, selection=6.5627s)
  - im_v4: F1 Drop = 0.0277 (f1_before=0.8856, f1_after=0.8579, time=2.4s, cache=MISS, selection=1.3163s)
  - tracin: F1 Drop = 0.0092 (f1_before=0.8930, f1_after=0.8838, time=10.6s, cache=MISS, selection=9.4650s)
  - degree: F1 Drop = 0.0055 (f1_before=0.8911, f1_after=0.8856, time=1.3s, cache=MISS, selection=0.0228s)
  - random: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=1.6s, cache=MISS, selection=0.0000s)
  - pagerank: F1 Drop = 0.0037 (f1_before=0.8893, f1_after=0.8856, time=1.3s, cache=MISS, selection=0.0514s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.0443 (f1_before=0.8893, f1_after=0.8450, time=1.5s, cache=MISS, selection=0.0620s)
  - degree: F1 Drop = 0.0424 (f1_before=0.8911, f1_after=0.8487, time=1.6s, cache=MISS, selection=0.0161s)
  - hybrid_v4: F1 Drop = 0.0277 (f1_before=0.8911, f1_after=0.8635, time=7.3s, cache=MISS, selection=6.4796s)
  - tracin: F1 Drop = 0.0222 (f1_before=0.8930, f1_after=0.8708, time=11.7s, cache=MISS, selection=10.2990s)
  - im_v4: F1 Drop = 0.0221 (f1_before=0.8856, f1_after=0.8635, time=2.2s, cache=MISS, selection=1.1178s)
  - random: F1 Drop = 0.0184 (f1_before=0.8856, f1_after=0.8672, time=2.0s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0203 (f1_before=0.8911, f1_after=0.8708, time=8.4s, cache=MISS, selection=7.4577s)
  - degree: F1 Drop = 0.0184 (f1_before=0.8911, f1_after=0.8727, time=1.0s, cache=MISS, selection=0.0190s)
  - im_v4: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=1.2s, cache=HIT(key=f463fe7cbaf66d291a73c8fe5fd03102), selection=1.1590s, reuse=0.000000s)
  - random: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=1.3s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1415.76x)
  - tracin: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=8.2s, cache=MISS, selection=7.1508s)
  - pagerank: F1 Drop = 0.0111 (f1_before=0.8893, f1_after=0.8782, time=0.9s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000990s, speedup=1141.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0314 (f1_before=0.8930, f1_after=0.8616, time=7.3s, cache=MISS, selection=6.4607s)
  - degree: F1 Drop = 0.0277 (f1_before=0.8911, f1_after=0.8635, time=0.9s, cache=MISS, selection=0.0186s)
  - random: F1 Drop = 0.0258 (f1_before=0.8856, f1_after=0.8598, time=1.0s, cache=MISS, selection=0.0000s)
  - hybrid_v4: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=7.3s, cache=MISS, selection=6.3585s)
  - im_v4: F1 Drop = 0.0240 (f1_before=0.8856, f1_after=0.8616, time=2.2s, cache=MISS, selection=1.1795s)
  - pagerank: F1 Drop = 0.0203 (f1_before=0.8893, f1_after=0.8690, time=0.9s, cache=MISS, selection=0.0354s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.2196 (f1_before=0.8856, f1_after=0.6661, time=1.7s, cache=HIT(key=1d810907cd8c7466967959cb21f146b5), selection=0.0000s, reuse=0.001005s, speedup=0.00x)
  - pagerank: F1 Drop = 0.1919 (f1_before=0.8893, f1_after=0.6974, time=1.3s, cache=HIT(key=fa19ad60fa4bf61df9908d55c0c6fc89), selection=0.0514s, reuse=0.001009s, speedup=50.96x)
  - degree: F1 Drop = 0.1863 (f1_before=0.8875, f1_after=0.7011, time=1.4s, cache=MISS, selection=0.0208s)
  - im_v4: F1 Drop = 0.1568 (f1_before=0.8875, f1_after=0.7306, time=1.4s, cache=HIT(key=263eadae777b04243379c4ff02bd82b6), selection=1.3163s, reuse=0.001011s, speedup=1302.10x)
  - tracin: F1 Drop = 0.1402 (f1_before=0.8911, f1_after=0.7509, time=8.0s, cache=MISS, selection=6.5967s)
  - hybrid_v4: F1 Drop = 0.1384 (f1_before=0.8875, f1_after=0.7491, time=8.1s, cache=MISS, selection=6.7627s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=212
- 执行结果：
  - im_v4: F1 Drop = 0.2140 (f1_before=0.8875, f1_after=0.6734, time=1.5s, cache=HIT(key=794252a7951690c58719693c9ccfd343), selection=1.1178s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = 0.1937 (f1_before=0.8875, f1_after=0.6937, time=8.2s, cache=MISS, selection=6.7828s)
  - random: F1 Drop = 0.1531 (f1_before=0.8856, f1_after=0.7325, time=1.7s, cache=HIT(key=533362956bd3577f000098db04492e33), selection=0.0000s, reuse=0.000505s, speedup=0.00x)
  - tracin: F1 Drop = 0.1365 (f1_before=0.8911, f1_after=0.7546, time=8.2s, cache=MISS, selection=6.8639s)
  - pagerank: F1 Drop = 0.1218 (f1_before=0.8893, f1_after=0.7675, time=1.5s, cache=HIT(key=d56f457629e80b7a3fcb54f5790fced0), selection=0.0620s, reuse=0.001008s, speedup=61.53x)
  - degree: F1 Drop = 0.0461 (f1_before=0.8875, f1_after=0.8413, time=1.4s, cache=MISS, selection=0.0219s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1384 (f1_before=0.8893, f1_after=0.7509, time=1.4s, cache=HIT(key=13614b1d971b5db3e4f11e9871486f11), selection=1.1302s, reuse=0.000992s, speedup=1139.31x)
  - random: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=1.8s, cache=HIT(key=2280f9dc6bf5490bdce17c4ed25761ae), selection=1.4285s, reuse=0.001009s, speedup=1415.76x)
  - tracin: F1 Drop = 0.1052 (f1_before=0.8856, f1_after=0.7804, time=8.9s, cache=MISS, selection=7.4003s)
  - degree: F1 Drop = 0.0868 (f1_before=0.8875, f1_after=0.8007, time=1.4s, cache=MISS, selection=0.0240s)
  - im_v4: F1 Drop = 0.0535 (f1_before=0.8856, f1_after=0.8321, time=3.2s, cache=MISS, selection=1.1590s)
  - hybrid_v4: F1 Drop = 0.0462 (f1_before=0.8875, f1_after=0.8413, time=8.7s, cache=MISS, selection=7.1933s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:04] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.2140 (f1_before=0.8893, f1_after=0.6753, time=1.5s, cache=HIT(key=dc402c34530138d633ef0ba5eaca9799), selection=0.0354s, reuse=0.000000s)
  - random: F1 Drop = 0.2048 (f1_before=0.8856, f1_after=0.6808, time=1.8s, cache=HIT(key=ca1543a92392821a4c84b2ad01eef934), selection=0.0000s, reuse=0.001076s, speedup=0.00x)
  - hybrid_v4: F1 Drop = 0.1863 (f1_before=0.8875, f1_after=0.7011, time=8.0s, cache=MISS, selection=6.6344s)
  - degree: F1 Drop = 0.1679 (f1_before=0.8875, f1_after=0.7196, time=1.4s, cache=MISS, selection=0.0218s)
  - im_v4: F1 Drop = 0.1531 (f1_before=0.8875, f1_after=0.7343, time=1.4s, cache=HIT(key=5a5568eb54094fdd520355aac3f80220), selection=1.1795s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1494 (f1_before=0.8911, f1_after=0.7417, time=8.3s, cache=MISS, selection=6.8897s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=722
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0277 (f1_before=0.8893, f1_after=0.8616, time=7.6s, cache=MISS, selection=6.6321s)
  - random: F1 Drop = 0.0258 (f1_before=0.8893, f1_after=0.8635, time=1.1s, cache=MISS, selection=0.0000s)
  - degree: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=1.0s, cache=MISS, selection=0.0211s)
  - im_v4: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=2.5s, cache=MISS, selection=1.5795s)
  - tracin: F1 Drop = 0.0221 (f1_before=0.8856, f1_after=0.8635, time=7.8s, cache=MISS, selection=6.9486s)
  - pagerank: F1 Drop = 0.0203 (f1_before=0.8819, f1_after=0.8616, time=0.9s, cache=MISS, selection=0.0375s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = 0.0517 (f1_before=0.8819, f1_after=0.8303, time=1.1s, cache=MISS, selection=0.0384s)
  - degree: F1 Drop = 0.0387 (f1_before=0.8875, f1_after=0.8487, time=1.0s, cache=MISS, selection=0.0179s)
  - im_v4: F1 Drop = 0.0332 (f1_before=0.8875, f1_after=0.8542, time=2.4s, cache=MISS, selection=1.3872s)
  - hybrid_v4: F1 Drop = 0.0258 (f1_before=0.8893, f1_after=0.8635, time=7.4s, cache=MISS, selection=6.4566s)
  - tracin: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=7.4s, cache=MISS, selection=6.5550s)
  - random: F1 Drop = 0.0129 (f1_before=0.8893, f1_after=0.8764, time=1.2s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - im_v4: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=2.3s, cache=MISS, selection=1.1585s)
  - hybrid_v4: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=7.9s, cache=MISS, selection=6.9587s)
  - pagerank: F1 Drop = 0.0166 (f1_before=0.8819, f1_after=0.8653, time=1.0s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.000999s, speedup=1164.16x)
  - random: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=1.2s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.001011s, speedup=1465.38x)
  - tracin: F1 Drop = 0.0166 (f1_before=0.8893, f1_after=0.8727, time=9.8s, cache=MISS, selection=8.7071s)
  - degree: F1 Drop = 0.0074 (f1_before=0.8875, f1_after=0.8801, time=1.0s, cache=MISS, selection=0.0209s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=722
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0258 (f1_before=0.8893, f1_after=0.8635, time=7.4s, cache=MISS, selection=6.5258s)
  - random: F1 Drop = 0.0240 (f1_before=0.8893, f1_after=0.8653, time=1.1s, cache=MISS, selection=0.0000s)
  - im_v4: F1 Drop = 0.0203 (f1_before=0.8875, f1_after=0.8672, time=2.2s, cache=MISS, selection=1.2707s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=0.9s, cache=MISS, selection=0.0077s)
  - pagerank: F1 Drop = 0.0185 (f1_before=0.8819, f1_after=0.8635, time=0.9s, cache=MISS, selection=0.0370s)
  - tracin: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=7.8s, cache=MISS, selection=6.8896s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:06] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.2528 (f1_before=0.8856, f1_after=0.6328, time=8.6s, cache=MISS, selection=7.1172s)
  - random: F1 Drop = 0.2140 (f1_before=0.8893, f1_after=0.6753, time=1.7s, cache=HIT(key=b9acb16e247b6b441f9b6952bc93820e), selection=0.0000s, reuse=0.000998s, speedup=0.00x)
  - hybrid_v4: F1 Drop = 0.2030 (f1_before=0.8856, f1_after=0.6827, time=8.3s, cache=MISS, selection=6.9212s)
  - degree: F1 Drop = 0.1771 (f1_before=0.8819, f1_after=0.7048, time=1.5s, cache=MISS, selection=0.0224s)
  - pagerank: F1 Drop = 0.1642 (f1_before=0.8911, f1_after=0.7269, time=1.4s, cache=HIT(key=bd8c57118aba251f55487c5efeb47485), selection=0.0375s, reuse=0.000000s)
  - im_v4: F1 Drop = 0.1402 (f1_before=0.8875, f1_after=0.7472, time=1.7s, cache=HIT(key=f726f6bf8378a93cea2f73f399abc87f), selection=1.5795s, reuse=0.000992s, speedup=1592.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = 0.1753 (f1_before=0.8911, f1_after=0.7159, time=1.4s, cache=HIT(key=4ccf5dcdaebabcff8e647009be07e2ab), selection=0.0384s, reuse=0.000000s)
  - im_v4: F1 Drop = 0.1384 (f1_before=0.8875, f1_after=0.7491, time=1.5s, cache=HIT(key=82c59ca6e63931cb855dd667281b5325), selection=1.3872s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1273 (f1_before=0.8856, f1_after=0.7583, time=8.5s, cache=MISS, selection=6.9958s)
  - hybrid_v4: F1 Drop = 0.1255 (f1_before=0.8856, f1_after=0.7601, time=8.5s, cache=MISS, selection=7.1493s)
  - degree: F1 Drop = 0.0738 (f1_before=0.8819, f1_after=0.8081, time=1.5s, cache=MISS, selection=0.0235s)
  - random: F1 Drop = 0.0443 (f1_before=0.8893, f1_after=0.8450, time=1.6s, cache=HIT(key=d1b7babe19dfd62ec895b73d0f91f6da), selection=0.0000s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=722
- 执行结果：
  - im_v4: F1 Drop = 0.2066 (f1_before=0.8893, f1_after=0.6827, time=1.7s, cache=HIT(key=5423bc484c31e81789207902b23485e5), selection=1.1585s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = 0.1458 (f1_before=0.8819, f1_after=0.7362, time=8.4s, cache=MISS, selection=6.9109s)
  - pagerank: F1 Drop = 0.1088 (f1_before=0.8911, f1_after=0.7823, time=1.4s, cache=HIT(key=a976a80b9a50ff17f0557321602fdf0b), selection=1.1630s, reuse=0.000000s)
  - degree: F1 Drop = 0.0664 (f1_before=0.8819, f1_after=0.8155, time=1.4s, cache=MISS, selection=0.0230s)
  - random: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=1.8s, cache=HIT(key=e5961f35e36f2d13d1667111d4a66117), selection=1.4815s, reuse=0.001000s, speedup=1481.50x)
  - tracin: F1 Drop = 0.0554 (f1_before=0.8893, f1_after=0.8339, time=8.8s, cache=MISS, selection=7.2119s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.2066 (f1_before=0.8893, f1_after=0.6827, time=1.7s, cache=HIT(key=9b3b8f4959771aa264b3c6b43d56a387), selection=0.0000s, reuse=0.001007s, speedup=0.00x)
  - degree: F1 Drop = 0.1458 (f1_before=0.8819, f1_after=0.7362, time=1.6s, cache=MISS, selection=0.0257s)
  - im_v4: F1 Drop = 0.1347 (f1_before=0.8875, f1_after=0.7528, time=1.6s, cache=HIT(key=0a9d0ea96464aaa3ed422d903706619d), selection=1.2707s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1347 (f1_before=0.8856, f1_after=0.7509, time=8.5s, cache=MISS, selection=7.0383s)
  - hybrid_v4: F1 Drop = 0.1273 (f1_before=0.8856, f1_after=0.7583, time=8.4s, cache=MISS, selection=6.8783s)
  - pagerank: F1 Drop = 0.1218 (f1_before=0.8911, f1_after=0.7694, time=1.5s, cache=HIT(key=de407d2938831d1453065608405d5816), selection=0.0370s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=0.9s, cache=MISS, selection=0.0143s)
  - im_v4: F1 Drop = 0.0240 (f1_before=0.8875, f1_after=0.8635, time=2.6s, cache=MISS, selection=1.6695s)
  - random: F1 Drop = 0.0240 (f1_before=0.8856, f1_after=0.8616, time=1.2s, cache=MISS, selection=0.0000s)
  - hybrid_v4: F1 Drop = 0.0221 (f1_before=0.8911, f1_after=0.8690, time=7.7s, cache=MISS, selection=6.8378s)
  - tracin: F1 Drop = 0.0203 (f1_before=0.8856, f1_after=0.8653, time=7.8s, cache=MISS, selection=6.9576s)
  - pagerank: F1 Drop = 0.0166 (f1_before=0.8856, f1_after=0.8690, time=1.0s, cache=MISS, selection=0.0372s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = 0.0443 (f1_before=0.8856, f1_after=0.8413, time=0.9s, cache=MISS, selection=0.0374s)
  - degree: F1 Drop = 0.0424 (f1_before=0.8875, f1_after=0.8450, time=1.0s, cache=MISS, selection=0.0204s)
  - hybrid_v4: F1 Drop = 0.0332 (f1_before=0.8911, f1_after=0.8579, time=7.6s, cache=MISS, selection=6.6871s)
  - im_v4: F1 Drop = 0.0277 (f1_before=0.8875, f1_after=0.8598, time=2.5s, cache=MISS, selection=1.4792s)
  - random: F1 Drop = 0.0185 (f1_before=0.8856, f1_after=0.8672, time=1.2s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=8.1s, cache=MISS, selection=7.0621s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0332 (f1_before=0.8875, f1_after=0.8542, time=7.6s, cache=MISS, selection=6.6651s)
  - im_v4: F1 Drop = 0.0221 (f1_before=0.8856, f1_after=0.8635, time=2.5s, cache=MISS, selection=1.2346s)
  - degree: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=1.1s, cache=MISS, selection=0.0220s)
  - pagerank: F1 Drop = 0.0129 (f1_before=0.8856, f1_after=0.8727, time=1.0s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000000s)
  - random: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=1.5s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.000000s)
  - tracin: F1 Drop = 0.0037 (f1_before=0.8856, f1_after=0.8819, time=10.5s, cache=MISS, selection=9.4422s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = 0.0332 (f1_before=0.8875, f1_after=0.8542, time=1.0s, cache=MISS, selection=0.0202s)
  - im_v4: F1 Drop = 0.0332 (f1_before=0.8875, f1_after=0.8542, time=2.4s, cache=MISS, selection=1.4119s)
  - hybrid_v4: F1 Drop = 0.0332 (f1_before=0.8911, f1_after=0.8579, time=7.9s, cache=MISS, selection=6.9522s)
  - tracin: F1 Drop = 0.0277 (f1_before=0.8856, f1_after=0.8579, time=8.3s, cache=MISS, selection=7.2814s)
  - pagerank: F1 Drop = 0.0240 (f1_before=0.8856, f1_after=0.8616, time=1.0s, cache=MISS, selection=0.0372s)
  - random: F1 Drop = 0.0221 (f1_before=0.8856, f1_after=0.8635, time=1.2s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1568 (f1_before=0.8856, f1_after=0.7288, time=1.7s, cache=HIT(key=2ae100dd4d996360f4bc072310261266), selection=0.0000s, reuse=0.000000s)
  - degree: F1 Drop = 0.1550 (f1_before=0.8856, f1_after=0.7306, time=1.5s, cache=MISS, selection=0.0214s)
  - hybrid_v4: F1 Drop = 0.1531 (f1_before=0.8856, f1_after=0.7325, time=8.3s, cache=MISS, selection=6.7798s)
  - im_v4: F1 Drop = 0.1402 (f1_before=0.8893, f1_after=0.7491, time=1.6s, cache=HIT(key=d7d789d871c34671a8c9f19848874a10), selection=1.6695s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1089 (f1_before=0.8893, f1_after=0.7804, time=8.3s, cache=MISS, selection=6.9206s)
  - pagerank: F1 Drop = 0.1052 (f1_before=0.8893, f1_after=0.7841, time=1.5s, cache=HIT(key=07cc8a431bcd0294345eac8d7a67b433), selection=0.0372s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1919 (f1_before=0.8856, f1_after=0.6937, time=1.6s, cache=HIT(key=9a8452536333f0c203a3096ca82adf8c), selection=0.0000s, reuse=0.000988s, speedup=0.00x)
  - im_v4: F1 Drop = 0.1845 (f1_before=0.8893, f1_after=0.7048, time=1.5s, cache=HIT(key=77c04540252e744c2025c1482fc67452), selection=1.4792s, reuse=0.000000s)
  - degree: F1 Drop = 0.1476 (f1_before=0.8856, f1_after=0.7380, time=1.5s, cache=MISS, selection=0.0228s)
  - hybrid_v4: F1 Drop = 0.1458 (f1_before=0.8856, f1_after=0.7399, time=8.5s, cache=MISS, selection=7.0622s)
  - tracin: F1 Drop = 0.1292 (f1_before=0.8893, f1_after=0.7601, time=8.7s, cache=MISS, selection=7.2868s)
  - pagerank: F1 Drop = 0.0701 (f1_before=0.8893, f1_after=0.8192, time=1.4s, cache=HIT(key=a067a666de6cc2d09a2a3b0449be087b), selection=0.0374s, reuse=0.001006s, speedup=37.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=1337
- 执行结果：
  - im_v4: F1 Drop = 0.1439 (f1_before=0.8856, f1_after=0.7417, time=1.7s, cache=HIT(key=7e8f5298922b5ed267f58a6c0b858475), selection=1.2346s, reuse=0.000515s, speedup=2395.09x)
  - hybrid_v4: F1 Drop = 0.1365 (f1_before=0.8856, f1_after=0.7491, time=8.7s, cache=MISS, selection=7.2873s)
  - degree: F1 Drop = 0.1236 (f1_before=0.8856, f1_after=0.7620, time=1.4s, cache=MISS, selection=0.0097s)
  - pagerank: F1 Drop = 0.1125 (f1_before=0.8893, f1_after=0.7768, time=1.4s, cache=HIT(key=1830a6ec641cfd0a2ae2a8125a19880b), selection=1.2263s, reuse=0.000993s, speedup=1234.94x)
  - random: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=2.0s, cache=HIT(key=3ba51faf54a244365c973259084dcbaa), selection=1.4135s, reuse=0.001000s, speedup=1413.50x)
  - tracin: F1 Drop = 0.0738 (f1_before=0.8856, f1_after=0.8118, time=12.7s, cache=MISS, selection=10.8470s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1439 (f1_before=0.8856, f1_after=0.7417, time=1.6s, cache=HIT(key=174b7d507bb6c4d02892740217b03d92), selection=0.0000s, reuse=0.000000s)
  - degree: F1 Drop = 0.1365 (f1_before=0.8856, f1_after=0.7491, time=1.4s, cache=MISS, selection=0.0219s)
  - pagerank: F1 Drop = 0.1365 (f1_before=0.8893, f1_after=0.7528, time=1.4s, cache=HIT(key=8cd4fafc0efa2180d098fd91d7730a44), selection=0.0372s, reuse=0.000993s, speedup=37.49x)
  - im_v4: F1 Drop = 0.1292 (f1_before=0.8893, f1_after=0.7601, time=1.4s, cache=HIT(key=dc539c6baa7f746b40854330fba45901), selection=1.4119s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1218 (f1_before=0.8893, f1_after=0.7675, time=8.4s, cache=MISS, selection=6.8961s)
  - hybrid_v4: F1 Drop = 0.1199 (f1_before=0.8856, f1_after=0.7657, time=8.8s, cache=MISS, selection=7.4636s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:12] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=2024
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0369 (f1_before=0.8930, f1_after=0.8561, time=7.8s, cache=MISS, selection=6.8505s)
  - degree: F1 Drop = 0.0277 (f1_before=0.8948, f1_after=0.8672, time=1.0s, cache=MISS, selection=0.0209s)
  - pagerank: F1 Drop = 0.0277 (f1_before=0.8875, f1_after=0.8598, time=1.0s, cache=MISS, selection=0.0366s)
  - tracin: F1 Drop = 0.0258 (f1_before=0.8875, f1_after=0.8616, time=8.0s, cache=MISS, selection=7.0408s)
  - random: F1 Drop = 0.0258 (f1_before=0.8838, f1_after=0.8579, time=1.2s, cache=MISS, selection=0.0000s)
  - im_v4: F1 Drop = 0.0258 (f1_before=0.8893, f1_after=0.8635, time=2.5s, cache=MISS, selection=1.5613s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:13] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = 0.0517 (f1_before=0.8875, f1_after=0.8358, time=1.0s, cache=MISS, selection=0.0395s)
  - degree: F1 Drop = 0.0517 (f1_before=0.8948, f1_after=0.8432, time=0.9s, cache=MISS, selection=0.0231s)
  - hybrid_v4: F1 Drop = 0.0369 (f1_before=0.8930, f1_after=0.8561, time=8.0s, cache=MISS, selection=7.0590s)
  - im_v4: F1 Drop = 0.0332 (f1_before=0.8893, f1_after=0.8561, time=2.4s, cache=MISS, selection=1.3975s)
  - tracin: F1 Drop = 0.0185 (f1_before=0.8875, f1_after=0.8690, time=7.7s, cache=MISS, selection=6.7693s)
  - random: F1 Drop = 0.0148 (f1_before=0.8838, f1_after=0.8690, time=1.1s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:13] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid_v4: F1 Drop = 0.0424 (f1_before=0.8948, f1_after=0.8524, time=7.9s, cache=MISS, selection=6.9457s)
  - im_v4: F1 Drop = 0.0332 (f1_before=0.8838, f1_after=0.8506, time=2.5s, cache=MISS, selection=1.2120s)
  - degree: F1 Drop = 0.0184 (f1_before=0.8948, f1_after=0.8764, time=1.0s, cache=MISS, selection=0.0220s)
  - pagerank: F1 Drop = 0.0130 (f1_before=0.8875, f1_after=0.8745, time=1.0s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.000000s)
  - random: F1 Drop = 0.0093 (f1_before=0.8838, f1_after=0.8745, time=1.2s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.001000s, speedup=17974.40x)
  - tracin: F1 Drop = 0.0093 (f1_before=0.8838, f1_after=0.8745, time=9.3s, cache=MISS, selection=8.0623s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:14] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.0424 (f1_before=0.8948, f1_after=0.8524, time=1.0s, cache=MISS, selection=0.0205s)
  - hybrid_v4: F1 Drop = 0.0369 (f1_before=0.8930, f1_after=0.8561, time=7.7s, cache=MISS, selection=6.6966s)
  - im_v4: F1 Drop = 0.0369 (f1_before=0.8893, f1_after=0.8524, time=2.5s, cache=MISS, selection=1.3335s)
  - pagerank: F1 Drop = 0.0351 (f1_before=0.8875, f1_after=0.8524, time=1.0s, cache=MISS, selection=0.0476s)
  - tracin: F1 Drop = 0.0332 (f1_before=0.8875, f1_after=0.8542, time=7.6s, cache=MISS, selection=6.6812s)
  - random: F1 Drop = 0.0332 (f1_before=0.8838, f1_after=0.8506, time=1.2s, cache=MISS, selection=0.0000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.2
- 配置：unlearn_ratio=0.2 (541 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = 0.2749 (f1_before=0.8893, f1_after=0.6144, time=1.5s, cache=HIT(key=3c5d8810e25224b397edb227df480a5f), selection=0.0366s, reuse=0.001504s, speedup=24.32x)
  - degree: F1 Drop = 0.2657 (f1_before=0.8838, f1_after=0.6181, time=1.5s, cache=MISS, selection=0.0274s)
  - random: F1 Drop = 0.2103 (f1_before=0.8838, f1_after=0.6734, time=1.8s, cache=HIT(key=9d887b431c47135c3c94032f43344ec8), selection=0.0000s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = 0.2103 (f1_before=0.8838, f1_after=0.6734, time=8.5s, cache=MISS, selection=7.0209s)
  - tracin: F1 Drop = 0.2048 (f1_before=0.8893, f1_after=0.6845, time=8.4s, cache=MISS, selection=6.9691s)
  - im_v4: F1 Drop = 0.1863 (f1_before=0.8875, f1_after=0.7011, time=1.5s, cache=HIT(key=1dfe81eed602cc1715dfdedfcbdacc16), selection=1.5613s, reuse=0.001008s, speedup=1548.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.1
- 配置：unlearn_ratio=0.1 (270 nodes), seed=2024
- 执行结果：
  - im_v4: F1 Drop = 0.2232 (f1_before=0.8875, f1_after=0.6642, time=1.6s, cache=HIT(key=5c2dfa1a9feab9290d6d5218435ec77b), selection=1.3975s, reuse=0.000000s)
  - random: F1 Drop = 0.1845 (f1_before=0.8838, f1_after=0.6993, time=1.7s, cache=HIT(key=4f1adbffbc248c38b2798945bd89d953), selection=0.0000s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = 0.1587 (f1_before=0.8838, f1_after=0.7251, time=8.4s, cache=MISS, selection=6.9156s)
  - tracin: F1 Drop = 0.1402 (f1_before=0.8893, f1_after=0.7491, time=8.3s, cache=MISS, selection=6.9287s)
  - pagerank: F1 Drop = 0.1107 (f1_before=0.8893, f1_after=0.7786, time=1.5s, cache=HIT(key=5d03f0eea0534330b96b4dbfcb83aa4f), selection=0.0395s, reuse=0.000992s, speedup=39.87x)
  - degree: F1 Drop = 0.0738 (f1_before=0.8838, f1_after=0.8100, time=1.5s, cache=MISS, selection=0.0142s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.05
- 配置：unlearn_ratio=0.05 (135 nodes), seed=2024
- 执行结果：
  - hybrid_v4: F1 Drop = 0.1716 (f1_before=0.8838, f1_after=0.7122, time=8.7s, cache=MISS, selection=7.2978s)
  - im_v4: F1 Drop = 0.1439 (f1_before=0.8838, f1_after=0.7399, time=2.0s, cache=HIT(key=dbfcdcab5139986dbeb03e9abc67a84c), selection=1.2120s, reuse=0.000000s)
  - random: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=1.7s, cache=HIT(key=200bb1c0e298b92995c86986ec80ed24), selection=17.9744s, reuse=0.000999s, speedup=17992.39x)
  - tracin: F1 Drop = 0.0683 (f1_before=0.8838, f1_after=0.8155, time=10.4s, cache=MISS, selection=8.7320s)
  - degree: F1 Drop = 0.0535 (f1_before=0.8838, f1_after=0.8303, time=1.5s, cache=MISS, selection=0.0240s)
  - pagerank: F1 Drop = 0.0535 (f1_before=0.8893, f1_after=0.8358, time=1.4s, cache=HIT(key=04ab2e538243fe11bbbdcdf0461f4bc3), selection=18.1700s, reuse=0.001010s, speedup=17990.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-02-24 19:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4'], ratio=0.01
- 配置：unlearn_ratio=0.01 (27 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.1716 (f1_before=0.8838, f1_after=0.7122, time=1.5s, cache=MISS, selection=0.0277s)
  - random: F1 Drop = 0.1439 (f1_before=0.8838, f1_after=0.7399, time=1.9s, cache=HIT(key=57ce503c1b7717807fbd2d2aa3d2914c), selection=0.0000s, reuse=0.000000s)
  - hybrid_v4: F1 Drop = 0.1402 (f1_before=0.8838, f1_after=0.7435, time=8.5s, cache=MISS, selection=7.0216s)
  - im_v4: F1 Drop = 0.1328 (f1_before=0.8875, f1_after=0.7546, time=1.5s, cache=HIT(key=5433802a5df2d2bf82eb64b8c1756b7b), selection=1.3335s, reuse=0.000000s)
  - pagerank: F1 Drop = 0.1328 (f1_before=0.8893, f1_after=0.7565, time=1.5s, cache=HIT(key=dc250a74712d75cf977a30d23b86b45b), selection=0.0476s, reuse=0.000000s)
  - tracin: F1 Drop = 0.1292 (f1_before=0.8893, f1_after=0.7601, time=8.2s, cache=MISS, selection=6.7787s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-02-24 19:16:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.0192 |    1.14% |
| degree   | 0.82% |    0.0215 |    1.74% |
| pagerank | 0.82% |    0.0222 |    1.85% |
| tracin   | -6.42% |    0.0342 |    1.54% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_191631.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:16:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.47% |    0.0212 |    1.04% |
| degree   | 0.82% |    0.0237 |    1.86% |
| pagerank | 0.82% |    0.0233 |    1.68% |
| tracin   | -7.13% |    0.0364 |    1.97% |
| im_v4    | -1.26% |    0.0245 |    1.54% |
| hybrid_v4 | -3.64% |    0.0311 |    1.72% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_191656.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:17:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0211 |    1.56% |
| degree   | 0.00% |    0.0234 |    1.69% |
| pagerank | 0.82% |    0.0237 |    1.91% |
| tracin   | -5.96% |    0.0385 |    1.29% |
| im_v4    | 0.62% |    0.0258 |    1.54% |
| hybrid_v4 | -4.32% |    0.0310 |    1.23% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_191719.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:17:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0211 |    1.74% |
| degree   | 1.03% |    0.0212 |    1.57% |
| pagerank | 0.62% |    0.0233 |    1.85% |
| tracin   | -9.77% |    0.0378 |    1.72% |
| im_v4    | -0.42% |    0.0229 |    1.60% |
| hybrid_v4 | -1.05% |    0.0322 |    2.40% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_191744.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:18:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.48% |    0.0239 |    1.45% |
| degree   | 0.82% |    0.0223 |    1.69% |
| pagerank | 1.03% |    0.0245 |    1.85% |
| tracin   | -8.05% |    0.0351 |    1.48% |
| im_v4    | -1.26% |    0.0236 |    1.66% |
| hybrid_v4 | -0.42% |    0.0307 |    1.85% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_191807.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:18:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.27% |    0.3976 |   17.85% |
| degree   | 20.37% |    0.4114 |   19.87% |
| pagerank | 14.43% |    0.4039 |   17.80% |
| tracin   | 6.03% |    0.1912 |    6.40% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_191830.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:18:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 24.69% |    0.4597 |   27.26% |
| degree   | 11.93% |    0.3686 |   13.77% |
| pagerank | 19.34% |    0.3816 |   22.49% |
| tracin   | -0.75% |    0.1201 |    2.89% |
| im_v4    | 14.85% |    0.3931 |   18.09% |
| hybrid_v4 | 19.39% |    0.2279 |   13.78% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_191858.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:19:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.64% |    0.3642 |   11.23% |
| degree   | 22.06% |    0.3506 |   25.45% |
| pagerank | 11.75% |    0.3931 |   12.54% |
| tracin   | 7.12% |    0.0708 |    4.68% |
| im_v4    | 11.62% |    0.3681 |   15.69% |
| hybrid_v4 | 25.11% |    0.2859 |   19.45% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_191926.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:19:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.27% |    0.3667 |   19.97% |
| degree   | 26.13% |    0.4687 |   28.36% |
| pagerank | 3.34% |    0.3547 |    7.23% |
| tracin   | 3.44% |    0.1113 |    3.26% |
| im_v4    | 15.63% |    0.4208 |   18.34% |
| hybrid_v4 | 25.05% |    0.2759 |   17.91% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_191954.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:20:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 18.64% |    0.4003 |   23.59% |
| degree   | 27.48% |    0.4091 |   29.17% |
| pagerank | 4.55% |    0.3749 |    6.24% |
| tracin   | 8.12% |    0.0810 |    5.54% |
| im_v4    | 20.00% |    0.4532 |   23.82% |
| hybrid_v4 | 21.55% |    0.2587 |   13.35% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192022.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:20:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0153 |    1.08% |
| degree   | 1.02% |    0.0176 |    1.28% |
| pagerank | 1.43% |    0.0182 |    1.23% |
| tracin   | -2.33% |    0.0281 |    1.16% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192041.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:21:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0159 |    1.33% |
| degree   | 1.44% |    0.0164 |    1.13% |
| pagerank | 1.23% |    0.0189 |    1.64% |
| tracin   | -3.02% |    0.0286 |    1.32% |
| im_v4    | 0.82% |    0.0170 |    1.21% |
| hybrid_v4 | -0.63% |    0.0203 |    1.32% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192110.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:21:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0158 |    1.18% |
| degree   | 1.02% |    0.0178 |    1.39% |
| pagerank | 1.03% |    0.0189 |    1.39% |
| tracin   | -2.78% |    0.0323 |    1.37% |
| im_v4    | 1.03% |    0.0183 |    1.79% |
| hybrid_v4 | -1.69% |    0.0264 |    1.58% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192135.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:21:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.26% |    0.0166 |    1.28% |
| degree   | 1.03% |    0.0157 |    1.13% |
| pagerank | 0.82% |    0.0177 |    1.59% |
| tracin   | -3.22% |    0.0277 |    0.90% |
| im_v4    | -0.21% |    0.0185 |    1.37% |
| hybrid_v4 | -0.21% |    0.0220 |    1.48% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192159.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:22:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.47% |    0.0174 |    1.29% |
| degree   | 1.24% |    0.0166 |    1.54% |
| pagerank | 1.03% |    0.0187 |    1.69% |
| tracin   | -3.42% |    0.0284 |    1.11% |
| im_v4    | 0.41% |    0.0176 |    1.32% |
| hybrid_v4 | -0.42% |    0.0206 |    1.64% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192223.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:22:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 13.10% |    0.3569 |   17.55% |
| degree   | 7.41% |    0.3673 |   10.16% |
| pagerank | 4.90% |    0.3829 |    6.88% |
| tracin   | 11.66% |    0.1866 |   13.13% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192245.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:23:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.11% |    0.3418 |   14.21% |
| degree   | 6.58% |    0.4321 |    7.23% |
| pagerank | 17.83% |    0.3905 |   21.67% |
| tracin   | 7.05% |    0.0943 |    7.49% |
| im_v4    | 15.50% |    0.4043 |   19.04% |
| hybrid_v4 | 21.06% |    0.1957 |   17.99% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192312.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:23:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.53% |    0.3685 |   17.38% |
| degree   | 25.36% |    0.4402 |   28.42% |
| pagerank | 13.32% |    0.3865 |   14.12% |
| tracin   | 10.17% |    0.1271 |    9.18% |
| im_v4    | 18.24% |    0.4349 |   19.04% |
| hybrid_v4 | 14.98% |    0.2338 |   13.13% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192340.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:24:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 13.10% |    0.3321 |   16.91% |
| degree   | 12.35% |    0.3679 |   14.62% |
| pagerank | 18.56% |    0.4218 |   20.39% |
| tracin   | 8.24% |    0.0785 |    4.43% |
| im_v4    | 17.92% |    0.4353 |   23.63% |
| hybrid_v4 | 10.48% |    0.1896 |    7.38% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192408.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:24:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 12.76% |    0.3594 |   18.48% |
| degree   | 10.88% |    0.3666 |   14.01% |
| pagerank | 7.00% |    0.4081 |   12.17% |
| tracin   | 8.39% |    0.1182 |    6.80% |
| im_v4    | 21.33% |    0.3711 |   24.53% |
| hybrid_v4 | 16.38% |    0.1929 |   13.24% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192436.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:25:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0126 |    1.26% |
| degree   | 0.21% |    0.0159 |    1.51% |
| pagerank | 0.21% |    0.0159 |    1.41% |
| tracin   | -1.89% |    0.0160 |    1.18% |
| im_v4    | 0.83% |    0.0134 |    1.38% |
| hybrid_v4 | 1.23% |    0.0193 |    1.48% |
| hybrid   | -0.42% |    0.0167 |    0.94% |
| im       | -1.05% |    0.0148 |    1.23% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192509.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:25:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0131 |    0.83% |
| degree   | 0.41% |    0.0180 |    1.31% |
| pagerank | 1.44% |    0.0136 |    1.02% |
| tracin   | -1.69% |    0.0166 |    1.08% |
| im_v4    | -0.63% |    0.0178 |    1.58% |
| hybrid_v4 | 0.00% |    0.0169 |    1.18% |
| hybrid   | -0.63% |    0.0176 |    1.23% |
| im       | -1.91% |    0.0141 |    1.08% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192524.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:25:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0150 |    0.97% |
| degree   | 0.42% |    0.0159 |    1.56% |
| pagerank | 1.23% |    0.0152 |    1.31% |
| tracin   | -3.65% |    0.0160 |    1.38% |
| im_v4    | 0.62% |    0.0172 |    1.77% |
| hybrid_v4 | -0.21% |    0.0174 |    1.28% |
| hybrid   | -1.47% |    0.0160 |    0.94% |
| im       | 1.03% |    0.0154 |    0.98% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192538.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:26:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.23% |    0.4413 |   12.82% |
| degree   | 8.87% |    0.3422 |   10.74% |
| pagerank | 10.27% |    0.4056 |   12.88% |
| tracin   | 11.79% |    0.1670 |   14.82% |
| im_v4    | 17.60% |    0.3673 |   23.19% |
| hybrid_v4 | 13.54% |    0.2123 |   13.24% |
| hybrid   | 15.79% |    0.1763 |   17.97% |
| im       | 7.31% |    0.2392 |   10.68% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192612.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:26:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.64% |    0.3288 |    9.30% |
| degree   | 20.62% |    0.3801 |   24.94% |
| pagerank | 11.11% |    0.4064 |   15.26% |
| tracin   | 14.16% |    0.1990 |   14.52% |
| im_v4    | 26.32% |    0.3792 |   32.99% |
| hybrid_v4 | 13.99% |    0.1748 |   12.75% |
| hybrid   | 11.97% |    0.1518 |   13.64% |
| im       | 8.61% |    0.2443 |   12.95% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192627.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:26:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 23.59% |    0.3606 |   26.98% |
| degree   | 20.00% |    0.4053 |   26.35% |
| pagerank | 10.47% |    0.4409 |   12.10% |
| tracin   | 12.72% |    0.1582 |   12.36% |
| im_v4    | 22.52% |    0.5310 |   26.59% |
| hybrid_v4 | 11.04% |    0.1508 |   11.03% |
| hybrid   | 9.28% |    0.1547 |   12.16% |
| im       | 23.19% |    0.4571 |   25.95% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192642.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:27:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.63% |    0.0113 |    1.12% |
| degree   | -0.21% |    0.0142 |    1.35% |
| pagerank | 2.07% |    0.0128 |    1.26% |
| tracin   | 0.62% |    0.0181 |    1.17% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192701.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:27:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0110 |    1.26% |
| degree   | -0.63% |    0.0139 |    1.17% |
| pagerank | 0.21% |    0.0132 |    1.26% |
| tracin   | -1.26% |    0.0154 |    0.94% |
| im_v4    | -0.42% |    0.0149 |    1.45% |
| hybrid_v4 | 0.83% |    0.0134 |    0.94% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192724.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:27:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.42% |    0.0120 |    1.07% |
| degree   | -0.42% |    0.0131 |    1.03% |
| pagerank | 0.41% |    0.0133 |    1.12% |
| tracin   | -0.63% |    0.0164 |    0.79% |
| im_v4    | 0.21% |    0.0127 |    1.17% |
| hybrid_v4 | 0.62% |    0.0149 |    1.31% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192748.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:28:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0114 |    0.98% |
| degree   | 0.83% |    0.0135 |    1.40% |
| pagerank | 0.00% |    0.0117 |    0.84% |
| tracin   | 0.21% |    0.0156 |    0.98% |
| im_v4    | 0.41% |    0.0127 |    0.94% |
| hybrid_v4 | 0.62% |    0.0165 |    1.08% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192811.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:28:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.84% |    0.0117 |    1.17% |
| degree   | 0.21% |    0.0132 |    1.17% |
| pagerank | 0.83% |    0.0143 |    1.17% |
| tracin   | -1.26% |    0.0160 |    0.89% |
| im_v4    | 1.44% |    0.0137 |    1.08% |
| hybrid_v4 | 1.04% |    0.0148 |    1.08% |
- 日志路径：`results\collateral\GIF\cora\GCN\collateral_20260224_192834.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:28:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.87% |    0.1983 |    9.15% |
| degree   | 8.66% |    0.3462 |   11.99% |
| pagerank | 16.01% |    0.3877 |   21.22% |
| tracin   | 5.42% |    0.1274 |    8.65% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192856.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:29:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 9.36% |    0.2279 |   12.40% |
| degree   | 14.43% |    0.3756 |   16.37% |
| pagerank | 5.83% |    0.4849 |    9.79% |
| tracin   | 12.71% |    0.1659 |   13.51% |
| im_v4    | 18.67% |    0.3341 |   23.94% |
| hybrid_v4 | 11.32% |    0.1621 |   13.51% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192923.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:29:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 8.94% |    0.1734 |    9.22% |
| degree   | 23.96% |    0.5247 |   25.84% |
| pagerank | 12.03% |    0.3793 |   18.61% |
| tracin   | 10.40% |    0.1669 |   14.12% |
| im_v4    | 22.61% |    0.3967 |   25.53% |
| hybrid_v4 | 13.49% |    0.1654 |   14.87% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_192950.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:30:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.71% |    0.2137 |    8.86% |
| degree   | 7.85% |    0.3800 |    9.28% |
| pagerank | 15.03% |    0.3669 |   17.44% |
| tracin   | 11.25% |    0.1458 |   12.86% |
| im_v4    | 12.01% |    0.3388 |   15.19% |
| hybrid_v4 | 11.69% |    0.1568 |   13.74% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_193017.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-24 19:30:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.53% |    0.1725 |    6.91% |
| degree   | 18.49% |    0.3799 |   25.61% |
| pagerank | 18.05% |    0.4117 |   24.81% |
| tracin   | 3.75% |    0.0688 |    5.52% |
| im_v4    | 20.00% |    0.4480 |   24.45% |
| hybrid_v4 | 11.04% |    0.1314 |   12.86% |
- 日志路径：`results\collateral\GNNDelete\cora\GCN\collateral_20260224_193045.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

