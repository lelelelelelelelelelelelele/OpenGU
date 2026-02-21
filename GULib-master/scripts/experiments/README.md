# 实验脚本说明

本目录包含用于运行 GULib 攻击评估实验的脚本。

## 脚本列表

| 脚本 | 用途 |
|------|------|
| `run_mg0_completion.sh` | MG-0 稳定性实验补全 |
| `run_mg1_citeseer.sh` | MG-1 Citeseer 数据集实验 |
| `run_mg2_gat.sh` | MG-2 GAT 模型实验 |
| `run_mg3_extended.sh` | MG-3 扩展实验 (IDEA, MEGU) |
| `run_all_generalization.sh` | 所有泛化实验汇总 |
| `run_ratio_sensitivity.sh` | Ratio 敏感性实验（攻击强度曲线） |

## 使用方法

### 基本运行

```bash
# 进入项目根目录
cd H:/project/OpenGU/GULib-master

# 运行 MG-0 稳定性实验
bash scripts/experiments/run_mg0_completion.sh

# 运行 MG-1 Citeseer 数据集实验
bash scripts/experiments/run_mg1_citeseer.sh

# 运行 MG-2 GAT 模型实验
bash scripts/experiments/run_mg2_gat.sh

# 运行 MG-3 扩展实验
bash scripts/experiments/run_mg3_extended.sh
```

### 修复模式

跳过已完成的任务，从断点继续：

```bash
bash scripts/experiments/run_mg0_completion.sh --repair
```

### Collateral 评估

攻击实验完成后，自动运行 collateral 评估（retrain gap + collateral damage）：

```bash
# 攻击 + collateral 一起跑
bash scripts/experiments/run_mg0_completion.sh --run_collateral

# 也可以单独运行（需要先有攻击实验结果）
bash scripts/experiments/run_mg1_citeseer.sh --repair --run_collateral
```

**注意**: `--run_collateral` 需要先运行过对应的攻击实验（有 cache 结果）。

### 运行全部泛化实验

```bash
bash scripts/experiments/run_all_generalization.sh
```

## Ratio 敏感性实验

运行不同 unlearn_ratio 下的攻击效果，生成攻击强度曲线。

```bash
# 运行 ratio 敏感性实验
bash scripts/experiments/run_ratio_sensitivity.sh

# 修复模式
bash scripts/experiments/run_ratio_sensitivity.sh --repair
```

### 参数配置

- **RATIOS**: 0.01, 0.05, 0.10, 0.20
- **SEEDS**: 42,212,722,1337,2024
- **STRATEGIES**: random,degree,pagerank,tracin,im,hybrid

### 输出

结果保存至 `results/experiments/ratio_sensitivity/`

## 实验规模

| 实验 | 配置 | Runs (攻击) | Runs (collateral) |
|------|------|-------------|-------------------|
| MG-0 | Cora / GCN / 4 methods / 5 seeds / 6 strategies | 120 | 120 |
| MG-1 | Citeseer / GCN / 3 methods / 5 seeds / 6 strategies | 90 | 90 |
| MG-2 | Cora / GAT / 3 methods / 5 seeds / 6 strategies | 90 | 90 |
| MG-3 | Citeseer+GAT / IDEA,MEGU / 4 strategies / 5 seeds | 80 | 80 |
| Ratio | Cora / GCN / 4 methods / 5 seeds / 6 strategies / 4 ratios (0.20→0.01) | 480 | 80 |

## 验证脚本

```bash
# 检查脚本是否存在
ls -la scripts/experiments/run_*.sh
```
