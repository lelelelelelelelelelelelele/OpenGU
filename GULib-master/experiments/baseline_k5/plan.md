# 实验计划：排除 Unlearning 方法本身对 F1 的影响

## Context

**问题背景**：Shard-based 方法（GraphEraser）存在"保护效应"——即使随机删除节点，F1 也会提升。这导致无法区分攻击策略的真正效果与方法本身的"自我修复"效应。

**目标**：设计基准实验，排除 unlearning 方法本身对 F1 的影响，获得真实的攻击效果评估。

---

## 方案：K=5 本底基准 + 相对指标计算

### 原理

使用 k=5 作为基准（用户建议）：
- k=0 不可行：GIF 类方法无变化，难以对比
- k=1 太少：随机波动太大
- k=5 合理：占比小（~1-2% on Cora），足以触发 unlearning 方法（如 GraphEraser）的一整套重训练流程，从而剥离出其固有的"环境本底值"（固有波动或保护效应），而不至于对图结构造成实质性破坏。

计算公式：
```
baseline_f1_after = mean(f1_after(k=5, random)) across 5 seeds
attack_f1_after = f1_after(ratio=0.05, attack_strategy)

# 该差值反映了排除了方法固有机制影响后的真实攻击下降幅度
relative_f1_drop = baseline_f1_after - attack_f1_after
```

---

## 三步执行流程

### 步骤 1：一键批量生成 K=5 本底数据（跨 Seed 平均）

使用 `run_all_baselines.py` 一键批量运行所有 (Method × Dataset × Model × Seed) 的 K=5 random 基准实验，并自动计算跨 seed 的平均值：

```bash
python experiments/baseline_k5/run_all_baselines.py
```

该脚本会：
1. 遍历所有配置组合（见下方矩阵表），逐个调用 `generate_baseline.py`
2. 将每个 seed 的结果存入 `results/baseline/k5_random/{Method}/{Dataset}/{Model}/baseline_seed{X}_k5.json`
3. 全部跑完后，**自动计算 5 个 seed 的 F1 均值**，写入 `baseline_averaged_k5.json` → 这才是后续评估使用的权威基准

如果只需单个配置，可直接调用底层脚本：
```bash
python experiments/baseline_k5/generate_baseline.py \
    --dataset_name cora \
    --base_model GCN \
    --unlearning_methods GraphEraser \
    --random_seed 111 \
    --baseline_k 5
```

### 步骤 2：运行相对指标评估

使用 `eval_relative.py` 读取平均后的 K=5 本底缓存，与实际攻击结果 (`results/cache/`) 中的对应实验进行比对：

```bash
python experiments/baseline_k5/eval_relative.py \
    --dataset_name cora \
    --base_model GCN \
    --unlearning_methods GraphEraser \
    --strategies im_v4,tracin,hybrid_v4 \
    --unlearn_ratio 0.05 \
    --random_seed 42  # ← 这里的 seed 是攻击实验的 seed，和 baseline 的 seed 无关
```

支持 `--repair` 模式跳过已完成项，缺失数据会报出精确的缺失配置信息。

### 步骤 3：批量评估（可选脚本化）

在 shell 脚本中嵌套循环调用 `eval_relative.py`，类似 `run_mg3_extended.sh` 调用 `eval_collateral.py` 的方式：

```bash
METHODS="GNNDelete GIF GraphEraser"
DATASETS="cora citeseer"
ATTACK_SEEDS="42 212 722 1337 2024"  # 主实验 seeds

for METHOD in $METHODS; do
    for DATASET in $DATASETS; do
        for SEED in $ATTACK_SEEDS; do
            python experiments/baseline_k5/eval_relative.py \
                --dataset_name "$DATASET" \
                --base_model GCN \
                --unlearning_methods "$METHOD" \
                --strategies im_v4,tracin,hybrid_v4 \
                --unlearn_ratio 0.05 \
                --random_seed "$SEED" \
                --repair
        done
    done
done
```

---

## 实验配置矩阵

### Seeds

| 用途 | Seeds | 说明 |
|------|-------|------|
| **K=5 基准实验** | `111, 333, 555, 777, 999` | 独立种子，避免与攻击实验耦合 |
| **攻击实验** | `42, 212, 722, 1337, 2024` | 主实验种子，eval_relative 逐个读取 |

### K=5 随机基准（步骤 1 覆盖范围）

| Method | Datasets | Model | Seeds | K | 输出目录 |
|--------|----------|-------|-------|---|---------|
| GNNDelete | cora, citeseer | GCN | 5 | 5 | `results/baseline/k5_random/{Method}/{Dataset}/GCN/` |
| GIF | cora, citeseer | GCN | 5 | 5 | 同上 |
| GraphEraser | cora, citeseer | GCN | 5 | 5 | 同上 |
**总计：3 方法 × 2 数据集 × 5 seeds = 30 次生成运行**

### 攻击实验对比（已有结果直接读取）

| Method | Datasets | Ratio | Strategies | 来源 |
|--------|----------|-------|------------|------|
| GNNDelete | cora, citeseer | 0.05 | im_v4, tracin, hybrid_v4 | `results/cache/` |
| GIF | cora, citeseer | 0.05 | im_v4, tracin, hybrid_v4 | `results/cache/` |
| GraphEraser | cora, citeseer | 0.05 | im_v4, tracin, hybrid_v4 | `results/cache/` |

---

## 关键文件

| 脚本 | 用途 | 参数风格 |
|------|------|---------|
| `experiments/baseline_k5/run_all_baselines.py` | **一键批量**跑全量 K=5 + 自动平均 | 无参数，配置写在脚本头部 |
| `experiments/baseline_k5/generate_baseline.py` | **单次**跑特定配置的 K=5 | `--dataset_name --base_model --unlearning_methods --random_seed --baseline_k` |
| `experiments/baseline_k5/eval_relative.py` | 读取本底 + 攻击缓存，计算相对指标 | `--dataset_name --base_model --unlearning_methods --strategies --unlearn_ratio --random_seed --repair` |

### 结果存储结构

```
results/
├── baseline/k5_random/          ← K=5 本底数据
│   ├── GraphEraser/cora/GCN/
│   │   ├── baseline_seed111_k5.json
│   │   ├── baseline_seed333_k5.json
│   │   ├── baseline_seed555_k5.json
│   │   ├── baseline_seed777_k5.json
│   │   ├── baseline_seed999_k5.json
│   │   └── baseline_averaged_k5.json  ← eval_relative.py 读取的权威基准
│   ├── GIF/cora/GCN/...
│   └── ...
├── cache/                        ← 攻击实验缓存（由 demo_attack.py 生成）
└── relative/                     ← 相对指标输出
    ├── GraphEraser/cora/GCN/
    │   ├── relative_seed42_xxxx.json
    │   └── ...
    └── ...
```

---

## 指标解读

| 指标 | 含义 | 解读 |
|-----|------|------|
| `baseline_f1_after` | K=5 random 的跨 seed 平均 F1 | 方法固有保护效应本底 |
| `attack_f1_after` | 真实策略攻击后的 F1 | 攻击后实际表现 |
| `gap` | `attack_f1 - baseline_f1` | < 0 = 攻击有效 |
| `relative_f1_drop` | `baseline_f1 - attack_f1` | > 0 = 攻击在剔除系统因素后仍有破坏力 |
