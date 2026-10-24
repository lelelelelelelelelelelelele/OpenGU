# Ret 验证轨迹：pilot

可信回传诊断3条、完整逐轮记录9000行。科学状态：stop_unexplained_final_difference。

best、final、old-final同时报告；best只由retained图原validation mask的accuracy决定，并列选最早。测试端点不参与选择。

新旧final存在差异的条件3条；触发预定优化敏感阈值3条。任何新旧final差异均暂停扩展和科学解释，需要有证据的原因审查，不自动归因CUDA随机性。

pilot无触发不能排除其他seed；B若仍承担核心，必须完整九条。未触发不证明收敛或训练充分。

三个seed是固定split上的请求与训练程序重复，按seed配对，不把epoch或测试节点当独立样本；这里只给描述性均值/SD，不作功效或收敛保证。

完整数值见full_trace.csv、trajectories.csv、endpoints.csv、paired_request_contrasts.csv和condition_summary.csv。此范围只有33% Ret，不能单独证明B的5%→33%分歧关系，也不能挑测试更好的checkpoint替代原参照。

直接配对固定6个GIF/MEGU旧Output与三类Ret端点，共18条记录；分歧和accuracy均由四格正确性及格内分歧整数独立重建。GU_reference/REPORT.html展示每个seed的R-point−Random/Degree的D差与相对旧参照的变化，不从Ret utility推断。

全部六类别的配对整数还原全局N=666；该解释是在查看B后新增的post-hoc descriptive分析，不能当预注册机制或因果证据。

端点通过另行只读资产审计，绑定本run哈希、旧Output、权重及预测文件哈希；不重新训练或选择模型。writing_gate保持not_met。

| seed | selector | best_epoch | validation_accuracy_gap_pp | val_ce_2001_2500 | val_ce_2501_3000 | optimization_sensitive | old_final_exact | best_minus_final_test_accuracy_pp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | random | 26 | 3.303303 | 0.928812 | 0.926298 | True | False | 2.102102 |
| 42 | degree | 29 | 2.702703 | 0.989820 | 0.989054 | True | False | 1.951952 |
| 42 | r_point | 209 | 4.204204 | 1.534950 | 1.530952 | True | False | 1.201201 |
