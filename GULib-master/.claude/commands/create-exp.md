# 创建实验

根据用户描述的实验意图，自动完成实验配置、脚本创建、执行和报告生成的完整流程。

## 用法

```bash
/create-exp [实验意图描述]
```

## 完整流程

### Step 1: 解析实验意图

用户需要描述：
- **目标方法** (methods): 如 `GIF`, `GNNDelete`, `GraphEraser`, `GUIDE`, `IDEA`, `MEGU` 等
- **目标数据集** (datasets): 如 `cora`, `citeseer`, `pubmed` 等
- **模型** (base_model): 如 `GCN`, `GAT`, `GIN`, `SAGE` 等
- **攻击策略** (strategies): 如 `random`, `degree`, `pagerank`, `tracin`, `im`, `hybrid`
- **unlearn_ratio**: 如 `0.01`, `0.05`, `0.10`, `0.20`
- **Seeds**: 如 `42,212,722,1337,2024`
- **实验阶段**: 如 `MG-0`, `MG-1`, `MG-2`, `MG-3`, `ratio` 等

### Step 2: 检查 Checklist

1. 读取 `self/generalization_experiment_checklist.md`
2. 搜索是否有匹配的实验配置
3. 如果存在，询问用户是否使用现有配置还是创建新配置

### Step 3: 创建/更新 Checklist 条目

如果实验不在 checklist 中：

1. 根据实验阶段添加到对应 Section：
   - MG-0 → Section 2.1
   - MG-1 → Section 2.2
   - MG-2 → Section 2.3
   - MG-3 → Section 2.4
   - Ratio → Section 2.6
   - 其他 → Section 3.x

2. 格式：
```markdown
- [ ] `{Dataset} / {Model} / ratio={Ratio} / {Seeds_count} seeds`（auto_discovered: N runs）
  - methods: `{method1,method2,...}`
  - strategies: `{strategy1,strategy2,...}`
  - seeds: `{seed1,seed2,...}`
  - 规模：`{methods_count} methods × {strategies_count} strategies × {seeds_count} seeds = {total} runs`
  - **状态**：待运行
```

### Step 4: 创建 Shell 脚本

在 `scripts/experiments/` 目录下创建 `run_{phase_name}.sh`：

```bash
#!/bin/bash
# 实验配置
METHODS="{methods}"
DATASETS="{datasets}"
BASE_MODEL="{model}"
STRATEGIES="{strategies}"
RATIOS="{ratio}"
SEEDS="{seeds}"

# 调用 run_experiments.py
$PYTHON_BIN run_experiments.py \
    --methods $METHODS \
    --datasets $DATASETS \
    --base_model $BASE_MODEL \
    --strategies $STRATEGIES \
    --ratios $RATIOS \
    --seeds $SEEDS \
    --cuda $CUDA \
    --output results/experiments/{output collateral_dir}

# 运行 评估 (可选)
if [ "$RUN_COLLATERAL" -eq 1 ]; then
    $PYTHON_BIN eval_collateral.py \
        --dataset_name "$DATASETS" \
        --base_model "$BASE_MODEL" \
        --unlearning_methods "$METHODS" \
        --strategies "$STRATEGIES" \
        --unlearn_ratio "$RATIOS"
fi
```

### Step 5: 运行实验

1. 询问用户确认后执行脚本
2. 可以选择在后台运行 (`run_in_background: true`)
3. 监控实验进度

### Step 6: 评估与报告

1. 实验完成后，运行相对评估（如果需要）：
```bash
$PYTHON_BIN experiments/baseline_k5/eval_relative.py \
    --method {method} \
    --dataset {dataset} \
    --model {model}
```

2. 调用 `/exp-status --fill` 回填数据：
```bash
$PYTHON_BIN scripts/evaluation/exp_status_checker.py --fill --yes
```

3. 生成实验报告摘要

## 示例

### 示例 1: 创建 MG-1 跨数据集实验

用户输入：
```
创建一个 MG-1 实验，测试 GNNDelete 和 GraphEraser 在 citeseer 数据集上的表现，使用 GCN 模型，6 个策略，5 个 seeds
```

处理流程：
1. 检查 checklist → MG-1 已有 GNNDelete 和 GraphEraser，但缺少当前配置
2. 更新 checklist → 添加新配置
3. 创建 `run_mg1_new.sh` → 调用 run_experiments.py
4. 运行实验
5. 执行 /exp-status --fill

### 示例 2: 创建 Ratio 敏感性实验

用户输入：
```
测试 GIF 在 ratio=0.01,0.05,0.10,0.20 下的攻击效果
```

## 注意事项

- 默认 seeds: `42,212,722,1337,2024`
- 默认 ratio: `0.05`
- 策略版本: 使用 `im_v4` 和 `hybrid_v4` 作为正式版本
- 运行前确认计算资源充足
- 大规模实验建议使用 `--repair` 模式

## 交互确认

在以下步骤需要用户确认：
1. 创建新的 checklist 条目
2. 创建新的 shell 脚本
3. 开始执行实验
4. 执行 /exp-status --fill

用户输入: $ARGUMENTS