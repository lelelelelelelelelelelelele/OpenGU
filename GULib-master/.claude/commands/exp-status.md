# 实验进度查询

查询当前实验完成情况，对比 checklist 与实际结果，支持自动填补清单。

## 用法

```bash
/exp-status                          # 显示所有实验总体进度
/exp-status --phase mg0              # 只看 MG-0
/exp-status --phase mg1              # 只看 MG-1（跨数据集）
/exp-status --phase mg2              # 只看 MG-2（跨模型）
/exp-status --phase mg3              # 只看 MG-3（扩展方法）
/exp-status --phase ratio            # 只看 P2-Ratio 敏感性实验
/exp-status --method GIF             # 按方法筛选
/exp-status --dataset cora           # 按数据集筛选
/exp-status --detail                 # 显示缺失实验详情
/exp-status --fill                   # 自动填补清单（JSON + checklist 状态更新）
/exp-status --fill --yes             # 自动填补（自动确认）
/exp-status --fill --dry-run         # 只显示建议的修改，不实际写入
```

## 输出格式

### 总体进度（默认）
```
=====================================================================================
Phase              Total  Completed  Remaining   Progress   Legacy
-------------------------------------------------------------------------------------
MG-0                 120        120          0       100%     (16)
MG-1                  90         90          0       100%        -
MG-2                  90         90          0       100%        -
MG-3-Citeseer         40         40          0       100%        -
MG-3-GAT              40         40          0       100%        -
-------------------------------------------------------------------------------------
Total                380        380          0       100%     (16)
=====================================================================================

Note: Legacy = old strategy versions kept as cache (im/hybrid -> im_v4/hybrid_v4)

=====================================================================================
Evaluation Coverage (Collateral / Relative)
=====================================================================================

  Gaps (1):
  MG-0                    GUIDE/      cora/ GCN/r=0.05    relative=MISSING

  Summary: 21 complete, 1 missing/incomplete
=====================================================================================
```

**说明**:
- **Total/Completed/Remaining/Progress**: 基于正式策略（v4版本）计算
- **Legacy**: 括号内显示旧版本策略实验数量，作为cache保留但不计入完成度
- **Evaluation Coverage**: 自动扫描 `results/collateral/` 和 `results/relative/` 检测评估缺口

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
======================================================================
CHECKLIST GAP ANALYSIS
======================================================================

[Missing in checklist - found 620 official experiments]
  - mg0:GIF/cora/GCN/seed=42/degree/r0.05
  - mg0:GIF/cora/GCN/seed=42/hybrid_v4/r0.05
  ... and 617 more

[Legacy experiments (cache only) - 16 found]
  (im/hybrid old versions kept as cache, not counted in checklist)

[DRY-RUN] Would log 620 entries to results/experiments/auto_discovered.json
         Would update checklist status (mark as [x] completed)
======================================================================
```

**说明**:
- **Step 1**: 写入 `results/experiments/auto_discovered.json`（保留详细记录）
- **Step 2**: 更新 `self/generalization_experiment_checklist.md` 完成状态
- **official experiments**: 使用正式策略（v4版本）的实验
- **legacy experiments**: 使用旧策略（im/hybrid）的实验，仅作为cache保留

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

| Phase | 目录 | Methods | Dataset | Model | Seeds | **Strategies (正式)** | Legacy | Total Runs |
|-------|------|---------|---------|-------|-------|----------------------|--------|------------|
| MG-0 | `mg0_completion` | 4 | cora | GCN | 5 | random,degree,pagerank,tracin,**im_v4,hybrid_v4** | im,hybrid | 4x6x5=120 |
| MG-1 | `mg1_citeseer` | 3 | citeseer | GCN | 5 | random,degree,pagerank,tracin,**im_v4,hybrid_v4** | im,hybrid | 3x6x5=90 |
| MG-2 | `mg2_gat` | 3 | cora | GAT | 5 | random,degree,pagerank,tracin,**im_v4,hybrid_v4** | im,hybrid | 3x6x5=90 |
| MG-3 | `mg3_citeseer` | 2 | citeseer | GCN | 5 | random,tracin,**im_v4,hybrid_v4** | im,hybrid | 2x4x5=40 |
| MG-3 | `mg3_gat` | 2 | cora | GAT | 5 | random,tracin,**im_v4,hybrid_v4** | im,hybrid | 2x4x5=40 |
| P2-Ratio | `ratio_sensitivity` | 2 | cora | GCN | 5 | random,degree,pagerank,tracin,**im_v4,hybrid_v4** | - | 2x6x4x5=240 |

### P2-Ratio 说明
- **目录**: `results/experiments/ratio_sensitivity/`
- **Ratios**: 0.20, 0.10, 0.05, 0.01 (4个)
- **配置**: 2 methods × 6 strategies × 4 ratios × 5 seeds = 240 experiments

### 策略版本说明

- **正式策略** (`strategies`): `im_v4`, `hybrid_v4` —— 用于最终报告
- **Legacy策略** (`legacy_strategies`): `im`, `hybrid` —— 作为cache保留，不计入完成度
- **进度计算**: 只基于正式策略 (v4版本)
- **Legacy显示**: 进度表中 Legacy 列显示旧版本数量（如 `(16)` 表示有16个旧版本实验作为cache保留）

## Checklist 修改规则

### 填补流程（--fill 执行两步）

**Step 1**: 写入 `auto_discovered.json`
```json
{
  "last_updated": "2026-02-25T21:57:26",
  "sources": {"mg0": 120, "mg1": 90, "ratio_sensitivity": 240},
  "entries": [
    {"phase": "mg0", "method": "GIF", "dataset": "cora", "model": "GCN", "seed": 42, "strategy": "degree", "ratio": 0.05, "discovered_at": "..."}
  ]
}
```

**Step 2**: 更新 checklist.md 完成状态
- 将 `[ ]` 待完成更新为 `[x]` 已完成
- 添加完成日期和 `（auto_discovered: N runs）` 引用
- 若对应 Section 不存在（如 P2-Ratio），自动创建

### 更新示例
```markdown
### 2.1 MG-0 稳定性（非泛化，但必做）

- [x] `Cora / GCN / ratio=0.05 / 5 seeds`（auto_discovered: 120 runs）
  - seeds: `42, 212, 722, 2024, 1337`
  - methods: `GIF, GNNDelete, GraphEraser, GUIDE`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 规模：`4 methods × 6 strategies × 5 seeds = 120 runs`
  - **状态**：✅ 完成 (2026-02-25)
```

### 处理额外实验（清单规划但未实际运行）
交互式询问用户：
```
发现以下实验在 checklist 中规划但未实际运行：
1. P2-Ratio: GIF/cora/GCN/ratio=0.10
   选择操作：[m]标记为待完成 [s]标记为跳过 [i]忽略 [a]全部标记为待完成
```

## 实现步骤

1. 调用 `H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py` 执行实际检查
2. 解析脚本输出并格式化显示给用户
3. `--fill` 模式支持交互式确认

> **注意**：必须使用完整 Python 路径，不得使用 `conda activate gnn && python`。
> Claude Code 运行在非交互式 git bash 中，conda 未初始化，`conda` 命令不可用。

## 执行逻辑

当用户调用 `/exp-status` 时：

```bash
# 基础调用（必须用完整路径）
H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py

# 带参数调用
H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py --phase mg0 --detail
H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py --fill --dry-run
H:/conda_package/envs/gnn/python.exe scripts/evaluation/exp_status_checker.py --fill --yes
```

### 参数映射

| 用户输入 | 脚本参数 |
|----------|----------|
| `--phase mg0` | `--phase mg0` |
| `--phase mg1` | `--phase mg1` |
| `--phase mg2` | `--phase mg2` |
| `--phase mg3` | `--phase mg3` |
| `--method GIF` | `--method GIF` |
| `--dataset cora` | `--dataset cora` |
| `--detail` | `--detail` |
| `--fill` | `--fill` |
| `--fill --yes` | `--fill --yes` |
| `--fill --dry-run` | `--fill --dry-run` |

## 安全机制

1. **备份**：修改 checklist 前自动创建 `.bak` 文件
2. **Dry Run**：`--fill --dry-run` 只显示建议修改，不实际写入
3. **交互确认**：`--fill` 无 `--yes` 时需用户确认
4. **标记来源**：自动添加的记录带有 `[AUTO-FILLED]` 标记

## 脚本位置

- **主脚本**: `scripts/evaluation/exp_status_checker.py`
- **清单文件**: `self/generalization_experiment_checklist.md`
- **结果目录**: `results/experiments/`
- **自动记录**: `results/experiments/auto_discovered.json`

用户输入: $ARGUMENTS
