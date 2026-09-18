# 纯 PT 参数对照与新参数实验

`paired_pt.yaml` 明确旧/新训练参数，固定 Cora 公共 Dataset/Split、OpenGU 两层 GCN、hidden16/64、配对 seed42。训练与导出复用 `modular_model.prepare_model`，不使用旧 checkpoint 封装。

```sh
python experiments/train_checkpoints.py experiments/configs/aagu063/paired_pt.yaml --dry_run
python experiments/train_checkpoints.py experiments/configs/aagu063/paired_pt.yaml --run-id <fresh-run-id>
```

正式训练使用 `.syncmate/device.yaml` 的 CUDA 与 active checkout，启动前按 experiments/AGENTS.md 完成版本、数据和注册 gate。CPU 测试仅使用临时小图。输出为 `results/runs/aagu063-paired-pt/<run-id>/run.json` 和每个配置/seed 单独的纯 PT；记录有效参数、来源、指标及导出前后 logits 一致性。显式收集本批 PT 时核对 receipt 中自动计算的文件摘要。旧/new 是训练参数组，不是算法质量排名。

`new_training_gu.yaml` 用061新训练参数运行 GIF/IDEA × hidden16/64，共4格；沿用059的100步求解参数、Random seed104245、10%删除预算，模型训练seed42。不加入数值阻尼或改求解器；非有限、求解失败必须原样记录。该表通过普通 `experiments/run.py` 执行。

```sh
python experiments/run.py experiments/configs/aagu063/new_training_gu.yaml --dry_run
python experiments/run.py experiments/configs/aagu063/new_training_gu.yaml --run-id <fresh-run-id>
```

两批先训练导出，再执行新参数GU；同样的基础训练身份可命中纯PT缓存。支持在 paired_pt.yaml 的 `seeds` 中声明多seed，扩展正式范围仍需登记。现有旧大表参数可保留；清理哪些历史运行和缓存以063的精确清理清单为准。

## 用 AAGU-059 旧表替换 PT 的示例

`aagu059_h64_pt/table01.yaml` 来自 AAGU-059 的
`experiments/configs/aagu059/table01.yaml`，保留完整6格：
GIF/IDEA × 100/200/400步，Cora、两层GCN hidden64、执行seed42、
Random seed104245、10%删除，GIF scale1000、IDEA scale500、damp0。
数据/split、评估引用和方法参数均沿用旧表。

六个方法小表统一指定已完成的
`aagu063-paired-pt-v2/3-new-h64-seed42.pt`（新训练参数、训练seed42）。
原小表未指定checkpoint且training只有seed，现在显式加载新PT，
跳过基础训练及缓存，不要求用户填写SHA或sidecar。
路径相对于大表目录，指向SSH正式导出位置；本地回传副本在
`results/runs/gpu4090/` 下。

新experiment_id为 `aagu063-aagu059-table01-h64-new-pt`。
这是旧Block完整矩阵的配置改写示例，不修改059历史结果或绑定记录；
未提交、未运行GU，也没有生成新的Hessian/收敛诊断证据。
原059专属diagnostic runner及注册recipe不能直接拿来执行这张新表。

```sh
python experiments/run.py experiments/configs/aagu063/aagu059_h64_pt/table01.yaml --dry_run
```

仍用于后续执行的错误PT引用应换成经核验且结构、数据/split匹配的PT。
历史run.json和缓存身份不能通过改路径或摘要变成新实验结果。
`checkpoint: null` 表示未显式指定权重，Selector的 `checkpoint_steps`
表示轨迹采样点，都不是旧PT文件路径。

## 四方法 checkpoint 接口最小验证

`checkpoint_gate/table.yaml`：Cora/GCN hidden64、新参数seed42的已验证PT，
GIF/IDEA/MEGU/GNNDelete × 显式PT/完整training参数，共8格。
GIF/IDEA仅2步（保留scale1000/500、damp0），MEGU/GNNDelete仅2个遗忘epoch。
固定Random seed104245、10%请求；只验证两种基础权重入口和实际消费者连通，
不证明收敛、完整遗忘效果或默认预算的数值稳定性。
验收两入口加载相同state_hash，training入口记录基础训练缓存HIT。
当前GU Output身份仍包含training配对元数据，因此两入口不共享GU输出缓存；
不能把基础权重HIT解释为GU输出HIT。
