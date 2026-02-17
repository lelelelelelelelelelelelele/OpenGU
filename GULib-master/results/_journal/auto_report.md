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

