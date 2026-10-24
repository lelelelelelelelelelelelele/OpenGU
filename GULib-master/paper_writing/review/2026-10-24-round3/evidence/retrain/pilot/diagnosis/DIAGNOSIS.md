# Ret pilot 不一致：当前能确定什么

2026-10-24。根任务的有界原因审查，基于正式e85rtg1、冻结分析、只读端点审计和本地程序路径。**原因尚未确定；剩余六条不启动，原一致性阈值不放宽。**

## 直接证据

13份轻量文件正式accepted，9000轮记录完整；远端只读审计逐一核对旧Output、新best/final权重与保存logits，producer调用0、forward调用0、cache index不变。三个请求的新旧final权重均不同，测试预测变化为Random10、Degree9、R-point9个，最大logit绝对差分别0.953027、2.138839、0.906697。accuracy差小于0.31pp不能消除这些实际差异。

新轨迹的三个validation最大值与终轮差为3.303303、2.702703、4.204204pp，均触发预定1pp阈值；两个末段窗口CE均略降，没有触发CE上升阈值。只允许称新运行具有选模敏感性，不能回推旧输出的训练轨迹，不能把best选为新的有利主参照。

## 程序检查及其边界

原Ret路径为`modular_gu.retrain_node → run_retrain`，显式构造retained图、在seeded_execution内初始化、重新从同seed开始train_supervised。新诊断路径按精确旧Output恢复模型、3000轮参数及有序Selection，采用同样的初始化／训练seed边界，并在每轮后调用Observer。Observer恢复Python、NumPy及Torch RNG与module train/eval状态；原CPU3000轮对照证明其在该CPU例子中不改变最终state。

将已知来源运行a217daf5c67b485afed63c393b5e8bb23820b237与本次b3481f571880b0ee1a631f87277f6209501dad8b比较：run_retrain、node_deletion、GCN模型和seeded_execution所在源文件没有差异；modular_model与train_trajectory的相关变化是可选epoch_end观察接口。该检查没有找到足以解释本次差异的明确参数／请求变更。

这个Git比较不是旧缓存首次生产环境的完整重建。来源运行含缓存复用，消费运行SHA不能自动当成每个旧Output的首次生成SHA。当前numerical_environment仅记录dtype，不能凭它证明两次GPU、驱动、Torch/PyG或数值执行环境相同。CPU不变性也不能外推为GPU不变性。

目前没有观察器开／关的同GPU正式对照、无观察器重复训练差异分布或旧生成环境完整快照。因而既不能断言Observer改变了训练，也不能把差异直接归为CUDA随机性。这三个输出保持有效的当前运行记录，但不满足“重建旧Ret训练历史”的冻结接纳要求。

## 下一项应如何设计

若继续B路线，应先冻结一个原因定位协议：仍用三个既定请求、相同split和参数，逐次记录初始化state、RNG、实际软件／GPU环境，比较无观察器重复与开观察器执行的逐段状态。必须同时保留两类差异，不能只拿最接近旧输出的一次。优先明确旧Output首次生成身份与可恢复环境；无法恢复时公开说明。

这需要正式配置、预算和必要实现验证；本审查未提交新GPU任务，也未改动当前冻结协议。若未来只能得到新的可复现参考，应形成与旧参考分离的新验证方案，并覆盖5%和33%完整请求关系；本次三条或仅33%的best比较不能替代原预算交互。是否值得执行，还取决于近邻贡献审查，不能只为达到评分不断追加实验。
