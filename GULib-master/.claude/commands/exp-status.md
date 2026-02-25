# 实验进度查询

查询当前实验完成情况，对比 checklist 与实际结果，支持自动填补清单。

## 用法

```bash
/exp-status                          # 显示所有实验总体进度
/exp-status --phase mg0              # 只看 MG-0
/exp-status --phase mg1              # 只看 MG-1（跨数据集）
/exp-status --phase mg2              # 只看 MG-2（跨模型）
/exp-status --phase mg3              # 只看 MG-3（扩展方法）
/exp-status --method GIF             # 按方法筛选
/exp-status --dataset cora           # 按数据集筛选
/exp-status --detail                 # 显示缺失实验详情
/exp-status --fill                   # 自动填补 checklist（交互式）
/exp-status --fill --yes             # 自动填补 checklist（自动确认）
/exp-status --fill --dry-run         # 只显示建议的修改，不实际写入
```

## 输出格式

### 总体进度（默认）
```
========== Experiment Progress ==========
Phase       Total   Completed   Remaining   Progress
----------- ------- ----------- ----------- ----------
MG-0        120     120         0           100%
MG-1        90      90          0           100%
MG-2        90      90          0           100%
MG-3        80      80          0           100%
P2-Ratio    120     0           120         0%
P5-MIA      180     0           180         0%
----------- ------- ----------- ----------- ----------
Total       680     470         210         69%
==========================================
```

### 详细模式（--detail）
```
MG-0: Citeseer / GCN (5 seeds x 6 strategies = 30 runs)
  Completed: 30/30
  Methods: GIF, GNNDelete, GraphEraser, GUIDE
  Seeds: 42, 212, 722, 1337, 2024

MG-1: Missing 6 runs
  Missing: GIF/citeseer/GCN/seed=1337/tracin
           GIF/citeseer/GCN/seed=2024/hybrid
           ...
```

### 填补模式（--fill）
```
========== Checklist Gap Analysis ==========

[缺失 - 实际有但清单未记录]
- MG-0: GUIDE/cora/GCN/seed=42/random (已自动添加)
- MG-3: MEGU/citeseer/GCN/seed=2024/hybrid (已自动添加)

[额外 - 清单规划但未实际运行]
- P2-Ratio: GIF/cora/GCN/ratio=0.10 (建议标记为待完成或跳过)

[修改总结]
已添加 2 条缺失记录到 checklist
建议处理 1 条额外记录

文件已更新: self/generalization_experiment_checklist.md
==========================================
```

## 实现逻辑

### 1. 解析实验清单 (`self/generalization_experiment_checklist.md`)
   - 提取所有 `[x]`/`[ ]`/`[-]` 项
   - 解析 Sh 文件配置对照表中的配置
   - 构建"期望实验集合"（method × dataset × model × seed × strategy）

### 2. 扫描实际结果 (`results/experiments/`)
   - MG-0: `mg0_completion/phase_a/*_seed*/_summary.json`
   - MG-1: `mg1_citeseer/phase_a/*_seed*/_summary.json`
   - MG-2: `mg2_gat/phase_a/*_seed*/_summary.json`
   - MG-3: `mg3_citeseer/phase_a/*_seed*/_summary.json`, `mg3_gat/phase_a/*_seed*/_summary.json`

### 3. 对比并生成报告
   - 计算完成率
   - 识别缺失配置（实际有但清单未记录）
   - 识别额外配置（清单规划但未实际运行）
   - 标记高优先级缺失

### 4. 填补模式 (`--fill`)
   - **缺失实验**：自动添加到 checklist 的"已完成配置"部分，标记为 `[x]`
   - **额外实验**：提示用户选择标记为 `[ ]`（待完成）或 `[-]`（跳过）
   - **写入文件**：更新 `self/generalization_experiment_checklist.md`
   - **备份**：写入前自动创建 `.bak` 备份

## 具体配置映射

| Phase | 目录 | Methods | Dataset | Model | Seeds | Strategies | Total Runs |
|-------|------|---------|---------|-------|-------|------------|------------|
| MG-0 | `mg0_completion` | GIF,GNNDelete,GraphEraser,GUIDE | cora | GCN | 42,212,722,1337,2024 | random,degree,pagerank,tracin,im,hybrid | 4x6x5=120 |
| MG-1 | `mg1_citeseer` | GIF,GNNDelete,GraphEraser | citeseer | GCN | 42,212,722,1337,2024 | random,degree,pagerank,tracin,im,hybrid | 3x6x5=90 |
| MG-2 | `mg2_gat` | GIF,GNNDelete,GraphEraser | cora | GAT | 42,212,722,1337,2024 | random,degree,pagerank,tracin,im,hybrid | 3x6x5=90 |
| MG-3 | `mg3_citeseer` | IDEA,MEGU | citeseer | GCN | 42,212,722,1337,2024 | random,tracin,im,hybrid | 2x4x5=40 |
| MG-3 | `mg3_gat` | IDEA,MEGU | cora | GAT | 42,212,722,1337,2024 | random,tracin,im,hybrid | 2x4x5=40 |

## Checklist 修改规则

### 添加缺失实验（实际有但清单未记录）
```markdown
## 1. 已完成配置（基线与阶段结论）

- [x] `Phase A`：`Cora / GCN / unlearn_ratio=0.05 / seed=2024`，`3 methods × 6 strategies`
  - methods: `GIF, GNNDelete, GraphEraser`（已完成）
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 输出：F1 Drop + 初步机制分组结论（Learning-based: IM最强, IF-based: Hybrid最强, Shard-based: 免疫）
# [AUTO-FILLED] 以下记录由 /exp-status --fill 自动添加
- [x] `MG-0`：`Cora / GCN / GUIDE / seed=42 / random`（自动识别）
- [x] `MG-3`：`Citeseer / GCN / MEGU / seed=2024 / hybrid`（自动识别）
```

### 处理额外实验（清单规划但未实际运行）
交互式询问用户：
```
发现以下实验在 checklist 中规划但未实际运行：
1. P2-Ratio: GIF/cora/GCN/ratio=0.10
   选择操作：[m]标记为待完成 [s]标记为跳过 [i]忽略 [a]全部标记为待完成
```

## 实现步骤

1. 读取 checklist 文件，提取实验配置
2. 扫描结果目录，统计实际完成的实验
3. 对比期望与实际，计算完成率
4. **填补模式**：
   - 识别缺失实验（actual - expected）
   - 识别额外实验（expected - actual）
   - 根据用户选择更新 checklist
   - 创建备份文件
5. 根据 `--phase`/`--method`/`--dataset` 筛选显示
6. `--detail` 模式下列出具体缺失配置

## 安全机制

1. **备份**：修改 checklist 前自动创建 `.bak` 文件
2. **Dry Run**：默认显示建议修改，不实际写入
3. **交互确认**：`--fill` 无 `--yes` 时每条修改需用户确认
4. **标记来源**：自动添加的记录带有 `[AUTO-FILLED]` 标记

用户输入: $ARGUMENTS
