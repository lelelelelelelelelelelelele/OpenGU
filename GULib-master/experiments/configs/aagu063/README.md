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

## AAGU-059 完整矩阵的新训练配置

`aagu059_h64_training/table01.yaml` 保留旧059完整6格：GIF/IDEA × 100/200/400步，Cora、GCN hidden64、seed42、Random seed104245、10%删除。方法参数不变，六个方法小表省略checkpoint，按统一基础训练默认值查缓存。

此表使用普通 `experiments/run.py`；旧059诊断runner不能直接执行它。新配置不改变历史结果及其绑定。

## 四方法默认值等价最小验证

`checkpoint_gate/table.yaml` 为四方法 × 省略基础训练默认值/显式填写同值，共8格；GIF/IDEA仅2步，MEGU/GNNDelete仅2个遗忘epoch，Random seed104245、10%请求。两侧有效训练配置一致，应共享基础模型缓存。此前v1运行验证的是显式PT与training入口；新表需使用新run-id，不将历史v1证据当作本表已执行。

活动实验小表不再指定checkpoint路径；纯PT显式加载API及对应软件测试仍保留。Selector的checkpoint_steps属于轨迹采样设置，不是PT路径，不删除。

## 统一基础训练默认值

基础训练默认采用 Adam、3000 epochs、lr=0.05、weight_decay=0.0001、无 scheduler；seed默认42。模型 properties 的学习率与衰减、CLI基础训练epochs及普通实验解析器一致。Selector和Unlearning分别解析，省略training与显式填写同值等价。Retrain也使用这一训练配置，但在删后图从头训练，不加载原始图PT。

已有新参数Cora/GCN hidden16/64 seed42 PT仅在完整数据、结构和训练身份相同的消费者中复用；其他模型、seed或数据不能保证HIT。方法自身遗忘步数、学习率和求解器参数独立。paired_pt.yaml的old组保留旧参数用于明确的对照；已产生的历史运行配置与证据不回写成新参数结果。
