# 实验脚本说明

> **2026-05-06 重写**：`scripts/experiments/` 下原有的 `run_mg{0,1,2,3}_*.sh`、
> `run_p2_ext_gif.sh`、`run_ratio_sensitivity.sh`、`run_all_generalization.sh`、
> `run_all_mg.sh`、`repair_master.{sh,ps1}`、`IM_V4_MIGRATION_NOTE.md` 全部已删除。
> 它们对应 pre-Phase-B 的 MG-0/1/2/3/p2/im_v4 实验流，结果数据 2026-05-05 起从
> git 中移除（仍然 .gitignore 在盘上，但被声明为 bug-polluted）。
>
> **当前 canonical 流程**：yaml-driven，`experiments/run.py` 主入口。

## Phase B 标准跑法

```bash
# 单 yaml — 展开 (method × strategy × seed) 矩阵
H:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/phase_b_cora_gcn.yaml

# 跑完用 gate 判 pass/fail（4 文件 + mia_auc + f1 范围）
H:/conda_package/envs/gnn/python.exe scripts/gate_runs.py results/runs/cora_GCN_r0.05
```

可用 yaml：见 `experiments/configs/`。
执行手册：根目录 `SERVER_RUNBOOK.md`（4090 cora + H800 arxiv 双机版）。

## 仍在用的辅助 .sh

| 脚本 | 用途 |
|---|---|
| `scripts/diag_b1.sh` | 一键看 cell 输出列表 + log 错误尾（不在 git，需 cat 创建） |
| `scripts/redo_collateral.sh` | 补 OOM 失败的 collateral cell（不在 git，需 cat 创建） |

## 历史保留

仅 `scripts/experiments/` 下被删除的脚本本身离开 git；它们生成的 `results/runs_pre_phase_b/`
等结果目录早已在 .gitignore 内。如果需要回溯具体命令，去 `git log -- scripts/experiments/run_mg0_completion.sh`
看历史。
