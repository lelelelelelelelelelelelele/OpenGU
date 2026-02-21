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
