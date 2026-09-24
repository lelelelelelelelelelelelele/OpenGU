# Table02 · GIF/IDEA 补充表

这两张真实 `kind: experiment` 表补充已有 Table02 的 GIF/IDEA 列，直接由
`experiments/run.py` 消费。其余四种 GU 和 Retrain 沿用原表，本补充表不重复声明。

| 表 | 数据与模型 | 训练 seed | 选点条件 | 方法 | 格数 |
| --- | --- | --- | --- | --- | ---: |
| [gate](table02_gif_idea_gate.yaml) | Cora/CiteSeer/PubMed，GCN H64 | 42 | PageRank，10% | GIF、IDEA，T100 | 6 |
| [完整补充表](table02_gif_idea.yaml) | 同上 | 42/212/2024 | 原 Table02 全部策略与抽样 seed，10% | GIF、IDEA，T100 | 414 |

完整表每个数据集、训练 seed 下共有23个选点条件：R-point、D-full、Degree、
PageRank各1个，Random共10个，RR三种R各3个抽样seed。因此为
`3数据集 × 3训练seed × 23选点条件 × 2方法 = 414格`；gate 的6格是其子集。
训练seed、Random抽样seed与RR抽样seed是不同轴，Random与RR不互相交叉。

## 怎样消费参数

两张大表的 `parameter_profile_ref` 均指向
[`gif_idea_fixed_pt.yaml`](../profiles/gif_idea_fixed_pt.yaml)。
`unlearning_refs` 分别读取 [GIF](gif_h64.yaml) 和 [IDEA](idea_h64.yaml)：
这两个方法小表提供 `model.hidden_channels: 64` 和 `iteration: 100`，
不填写 scale/damp。解析器从 `dataset_refs` 得到数据集名称，以“数据集 + GCN宽度”
选择 Profile，再按 GIF/IDEA 取得参数。

| 匹配条件 | GIF/IDEA scale | GIF damp | IDEA damp |
| --- | ---: | --- | --- |
| Cora H64 | 9791 | 0.20098238047209782 | 0.20098238047209782 |
| CiteSeer H64 | 23004 | 0.20094722036615764 | 0.20094722036615764 |
| PubMed H64 | 173215 | 0.20037196190824003 | 0.20037196190823992 |

每个训练seed使用同一条件的参数。`checkpoint: null` 表示按该seed读取精确匹配的
模型缓存，未命中时正常训练，不把校准的seed42权重重标为212/2024。训练沿用公共
GCN默认协议。参数的既有稳定性证据来自校准及多请求验证所用的checkpoint；
这些新表在其他模型seed和选点策略上的数值表现，仍须由后续真实实验观察。
Cora H16 映射仍在 Profile 中，供独立H16实验消费；本次保留原Table02的H64范围。

## 审阅与执行入口

在仓库项目根目录使用项目Python：

```powershell
python experiments/run.py experiments/configs/aagu077/table02_gif_idea_gate.yaml --dry_run
python experiments/run.py experiments/configs/aagu077/table02_gif_idea.yaml --dry_run
```

检查输出的 `batches`：每批的 `effective_parameter_profile`、
`effective_unlearning` 和 `configuration_sources` 分别回答“选中了谁”、
“最终参数是什么”和“每个字段来自哪里”。不要仅看顶层摘要；不同数据集的实际参数
在各自batch中。AAGU-077验收报告附两表原文、参数映射与完整逐格展开清单。

两表目前作为配置候选接受审阅。dry-run不执行模型或遗忘。正式运行前按Work Plan
注册新run及对应Recipe，重新绑定配置SHA/指纹并完成三端版本、输入与估时检查。
既有Table02和校准Recipe绑定旧配置，不能直接用于这两张新表。
