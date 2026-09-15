# Table01 参数来源与执行边界

本表检验作者求解参数在当前 OpenGU 两层 GCN、hidden=64 上的迁移；保留当前训练、原图测试集和 PageRank 10% 节点删除。不是完整作者实验复刻。

- GIF：[论文附录 D](https://arxiv.org/pdf/2304.02835) 的边删除比例为 5%，迭代数为 100；Cora/GCN 图示 scale=1000。这里将该数值用于已约定的 10% 节点删除。实际缩放采用 [作者代码](https://github.com/wujcan/GIF-torch/blob/main/exp/exp_GIF.py#L196-L225) 的除法约定：h0=v，h(t+1)=v+(1-damp)h(t)-Hh(t)/scale，delta=h(T)/scale，theta_new=theta+delta。
- IDEA：[作者构造器](https://github.com/yushundong/IDEA/blob/main/IDEA/src/idea.py#L26-L37) 在 Cora/GCN 覆盖为 scale=500、iteration=100；同处 gaussian_std=0.6。此处按 WorkItem 保持噪声为零，不导入作者噪声配置，不将默认值称为论文全矩阵参数。[作者递推](https://github.com/yushundong/IDEA/blob/main/IDEA/src/idea.py#L321-L350) 与上式相同。

## 当前实际实现

YAML 使用公共 Cora persisted split，训练为 Adam、100 epoch、lr=0.005、weight_decay=1e-6、seed42，GCN 两层 hidden64、dropout0.5。显式 checkpoint 路径、文件哈希与 state hash 写在六个方法实例内；因此表不再声明能覆盖 checkpoint 身份的 seeds 轴。

诊断通过现有 GIF/IDEA adapter 截获其实际 solver 输入，在模型更新前停止 adapter。H 为 eval 模式原图 train_mask 上 sum cross-entropy 的 Hessian，v 为受影响训练节点删除前后的 loss 梯度差。GIF reason_once 输出 logits；IDEA forward_once 输出 log_softmax 再传 CE。通过独立原图 logits/CE HVP 在随机向量及梯度来源 RHS 上检查数学等价与固定向量语义；邻域监督限制在 train_mask，原图指标只使用固定 test_mask。

作者原始 hvps 对内积再次求导，首次 h 含梯度图时可能引入额外导数项；当前 OpenGU 将 HVP 向量 detach。这里验证当前框架的真实固定 HVP，不声称逐位复刻该作者源码细节。每行另调用未修改的生产 solver 对照，有限 delta 应相同；非有限要两边均失败。诊断逐步记录不做 residual 早停，也不加移位。

曲率使用同一保存权重提升 float64，各方法独立起点 173/941、80 步 Lanczos、双重重正交，保存极端 Ritz 值及向量残差；不构成全谱正定认证。递推仍使用 checkpoint 的 float32 精度。

执行入口是注册 recipe `opengu-aagu059-table01-v1`，它消费 table01.yaml 的相同六格展开。输出独立数值诊断 JSON，通过 SyncMate Core 传输和 SHA-256 索引验证，随后执行项目诊断检查。它不发布 GU Cache Output；运行完成不代表收敛、科研接受或用户验收。
