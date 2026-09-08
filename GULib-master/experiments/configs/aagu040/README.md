# IM selector seed 大表实例

这些表是 AAGU-040 软件验证实例，未注册为正式科研矩阵或 SyncMate recipe。

`matrix: cartesian_product` 保持普通大表合同。独立轴写在顶层，与 `seeds`、`budget_ratios` 并列；不引入任意参数矩阵或第二套嵌套语法。

```yaml
matrix: cartesian_product
seeds: [42, 212, 2024]           # 模型训练 seed
im_selector_seeds: [11, 22, 33] # 仅 IM 的 Monte Carlo seed
budget_ratios: [0.1]
```

| 实例 | IM 条件 | Degree / Random / R-point | 总效果条件 |
|---|---:|---:|---:|
| single_seed.yaml | 1 × 3 = 3 | 各3 | 12 |
| multi_seed.yaml | 3 × 3 = 9 | 各3 | 18 |

在同一图、候选集、K、算法和其他参数下，多值实例仅需3份 IM Selection。训练seed=42消费11/22/33三份选集，212和2024复用这三份。不同selector seed可以偶然得到相同节点集合；判据是身份隔离，不是强迫节点不同。

优先级为大表 `im_selector_seeds` > IM小表 `parameters.im_selector_seed` > ImParameters默认2024。省略大表轴只消费有效小表seed，不跟随训练seed。轴必须是非空、无重复的非负整数列表，拒绝布尔、字符串和浮点。没有IM时声明该轴也拒绝。Random继续使用自己的抽样参数，图和split完全由dataset小表持有。

本入口运行现有MC/Batch-CELF，按实际K生产选集。K或selector seed改变形成不同身份；不从大K选集截断复用，不计算全候选静态排名。Numba后端支持Batch-CELF；Python经典CELF仅允许batch size=1，后端变更会隔离身份。其他IM算法不属于本次实现。

IM常规结果返回实际节点、K、Selection引用及recipe/content哈希、两条seed和selector seed来源。HIT与MISS同样返回这些内容。Score状态为not_applicable。当前Selection Store未保留K步收益，因此包含IM的表拒绝 `return_scores: true`，不会为回传重新计算收益或全排名。需要评分的其他selector可使用单独的普通表。

无写入检查：

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu040/multi_seed.yaml --dry_run
```

这只是解析/展开，正式运行仍须已批准的配置、设备和完整证据链。多训练seed反复消费同一IM选集，不构成多份独立选集样本。
