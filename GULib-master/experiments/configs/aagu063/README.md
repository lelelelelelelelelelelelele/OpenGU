# 纯 PT 参数对照与新参数实验

`paired_pt.yaml` 明确旧/新训练参数，固定 Cora 公共 Dataset/Split、OpenGU 两层 GCN、hidden16/64、配对 seed42。训练与导出复用 `modular_model.prepare_model`，不使用旧 checkpoint 封装。

```sh
python experiments/train_checkpoints.py experiments/configs/aagu063/paired_pt.yaml --dry_run
python experiments/train_checkpoints.py experiments/configs/aagu063/paired_pt.yaml --run-id aagu063-paired-pt-v1
```

正式训练使用 `.syncmate/device.yaml` 的 CUDA 与 active checkout，启动前按 experiments/AGENTS.md 完成版本、数据和注册 gate。CPU 测试仅使用临时小图。输出为 `results/runs/aagu063-paired-pt/<run-id>/run.json` 和每个配置/seed 单独的纯 PT；记录有效参数、来源、指标及导出前后 logits 一致性。显式收集本批 PT 时核对 receipt 中自动计算的文件摘要。旧/new 是训练参数组，不是算法质量排名。

`new_training_gu.yaml` 用061新训练参数运行 GIF/IDEA × hidden16/64，共4格；沿用059的100步求解参数、Random seed104245、10%删除预算，PT训练seed42，本次执行seed42。不加入数值阻尼或改求解器；非有限、求解失败必须原样记录。该表通过普通 `experiments/run.py` 执行。

```sh
python experiments/run.py experiments/configs/aagu063/new_training_gu.yaml --dry_run
python experiments/run.py experiments/configs/aagu063/new_training_gu.yaml --run-id <fresh-run-id>
```

两批先训练导出，再执行新参数GU。四个GU实例直接引用上述run-id下的 `2-new-h16-seed42.pt` / `3-new-h64-seed42.pt`，GIF和IDEA按宽度共用同一份新权重。GU只保留training.seed作为执行seed，不查基础训练缓存、不回退训练，不填写SHA。导出目录或run-id改变时，直接更新四个小表的checkpoint路径；大表不再声明seeds以免给既有权重重新贴训练seed标签。支持在 paired_pt.yaml 的 `seeds` 中声明多seed，扩展正式范围仍需登记。现有旧大表参数可保留；清理哪些历史运行和缓存以063的精确清理清单为准。
