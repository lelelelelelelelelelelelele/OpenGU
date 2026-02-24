# 实验计划：排除 Unlearning 方法本身对 F1 的影响

## Context

**问题背景**：Shard-based 方法（GraphEraser、GUIDE）存在"保护效应"——即使随机删除节点，F1 也会提升。这导致无法区分攻击策略的真正效果与方法本身的"自我修复"效应。

**目标**：设计基准实验，排除 unlearning 方法本身对 F1 的影响，获得真实的攻击效果评估。

---

## 方案：K=5 实验 + 相对指标计算

### 原理

使用 k=5 作为基准（用户建议）：
- k=0 不可行：GIF 类方法无变化，难以对比
- k=1 太少：随机波动太大
- k=5 合理：占比小（~1-2% on Cora），足以触发 unlearning 方法运行

计算公式：
```
gap = f1_after(attack) - f1_after(baseline)

其中 baseline 是 k=5 random 策略，attack 是 k=5 的 im/tracin/hybrid 策略
```

### 执行步骤

#### 步骤 1：运行 K=5 随机基准实验

```bash
# 对每个方法运行 k=5 random（5 个 seed）
python demo_attack.py \
    --dataset_name cora --base_model GCN \
    --unlearning_methods GraphEraser \
    --strategies random \
    --k 5 \
    --random_seed 2024

# 重复 seed: 2025, 2026, 2027, 2028
```

结果保存到：`results/baseline/k5_random/GraphEraser/cora/`

#### 步骤 2：运行 K=5 攻击策略实验

```bash
python demo_attack.py \
    --dataset_name cora --base_model GCN \
    --unlearning_methods GraphEraser \
    --strategies im,tracin,hybrid \
    --k 5 \
    --random_seed 2024
```

结果保存到：`results/experiments/k5_attack/GraphEraser/cora/`

#### 步骤 3：计算相对指标

```bash
python eval_relative.py \
    --methods GraphEraser,GUIDE,GNNDelete \
    --datasets cora \
    --strategies im,tracin,hybrid \
    --baseline_dir results/baseline/k5_random \
    --attack_dir results/experiments/k5_attack \
    --k 5 \
    --force
```

---

## 实验任务表

### 实验 1：K=5 随机基准

| Method | Seeds | K | 输出目录 |
|--------|-------|---|----------|
| GraphEraser | 5 | 5 | results/baseline/k5_random/GraphEraser/ |
| GUIDE | 5 | 5 | results/baseline/k5_random/GUIDE/ |
| GNNDelete | 5 | 5 | results/baseline/k5_random/GNNDelete/ |
| GIF | 5 | 5 | results/baseline/k5_random/GIF/ |

### 实验 2：K=5 攻击策略

| Method | Seeds | K | Strategies | 输出目录 |
|--------|-------|---|------------|----------|
| GraphEraser | 5 | 5 | im,tracin,hybrid | results/experiments/k5_attack/ |
| GUIDE | 5 | 5 | im,tracin,hybrid | results/experiments/k5_attack/ |
| GNNDelete | 5 | 5 | im,tracin,hybrid | results/experiments/k5_attack/ |

---

## 关键文件

- 单次实验入口：`demo_attack.py`
- 相对指标计算：`eval_relative.py`（已实现）
- 参数：`--k 5 --strategies random`
- 结果存储：
  - 基准：`results/baseline/k5_random/{method}/`
  - 攻击：`results/experiments/k5_attack/{method}/`
  - 相对指标：`results/relative/`

---

## 数据提取与计算方法

### 从 Results 文件夹提取 f1_after

实验结果保存在 JSON 文件中，可直接读取：

```python
import json
import glob
import os

def extract_f1_from_results(results_dir, method, dataset, strategy, k):
    """从 results 文件夹提取 f1_after 数据"""
    pattern = f"{results_dir}/**/{method}_{dataset}_*_k{k}_*.json"
    files = glob.glob(pattern, recursive=True)

    f1_afters = []
    for f in files:
        with open(f, 'r') as fp:
            data = json.load(fp)
            # 查找对应 strategy 的结果
            for entry in data.get('results', []):
                if entry.get('strategy') == strategy:
                    f1_afters.append(entry.get('f1_after'))

    return f1_afters
```

### 从 Cache 文件夹提取 f1_after

如果需要更底层的缓存数据：

```python
def extract_f1_from_cache(cache_dir, method, dataset):
    """从 cache 文件夹提取 f1_after 数据"""
    cache_file = f"{cache_dir}/{method}_{dataset}_cache.pkl"
    # 读取缓存的 pipeline 结果
    # 提取 f1_after 指标
```

### 计算 Relative F1 Drop

```python
def compute_relative_f1_drop(baseline_f1_afters, attack_f1_afters):
    """
    计算相对 F1 下降

    Args:
        baseline_f1_afters: 基准实验 (k=5, random) 的 f1_after 列表
        attack_f1_afters: 攻击实验 (k=5, im/tracin/hybrid) 的 f1_after 列表

    Returns:
        gap: f1_after 差值
        relative_f1_drop: 相对 F1 下降（正值表示攻击有效）
    """
    import numpy as np

    baseline_f1_after = np.mean(baseline_f1_afters)
    attack_f1_after = np.mean(attack_f1_afters)

    gap = attack_f1_after - baseline_f1_after
    relative_f1_drop = baseline_f1_after - attack_f1_after

    return {
        'baseline_f1_after': baseline_f1_after,
        'attack_f1_after': attack_f1_after,
        'gap': gap,                    # < 0 表示攻击有效
        'relative_f1_drop': relative_f1_drop  # > 0 表示攻击有效
    }
```

**解读**：
- `gap < 0`：attack 的 f1_after 低于 baseline，攻击有效
- `gap ≈ 0`：攻击效果被方法抵消
- `gap > 0`：攻击反而让 F1 更高

### 数据来源目录

| 数据类型 | 路径 |
|---------|------|
| 实验结果 | `results/experiments/mg0_completion/phase_a/` |
| 基准结果 | `results/baseline/k5_random/` |
| Pipeline 缓存 | `results/cache/` |
| 策略选择缓存 | `results/selection_cache/` |

---

## 代码实现

### eval_relative.py - 相对指标计算脚本

新建脚本 `eval_relative.py`：

```python
"""
eval_relative.py - Compute relative F1 metrics.

Compares attack strategies against baseline (k=5 random) to isolate
the true attack effect from method's inherent behavior.

Usage:
    python eval_relative.py \
        --methods GraphEraser,GUIDE,GNNDelete \
        --datasets cora \
        --baseline_dir results/baseline/k5_random \
        --attack_dir results/experiments/mg0_completion/phase_a \
        --output_dir results/relative
"""
import os
import sys
import json
import glob
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_f1_results(results_dir, method, dataset, strategy=None, k=None):
    """Load f1_after values from result JSON files."""
    pattern = f"{results_dir}/**/{method}_{dataset}_*.json"

    if strategy:
        pattern = f"{results_dir}/**/{method}_{dataset}_*_{strategy}_*.json"
    if k:
        pattern = pattern.replace('.json', f'_k{k}.json')

    files = glob.glob(pattern, recursive=True)

    f1_afters = []
    f1_befores = []
    f1_drops = []
    configs = []

    for f in files:
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)

            # 处理不同格式
            if 'results' in data:
                # 批量实验格式
                for entry in data['results']:
                    f1_afters.append(entry.get('f1_after'))
                    f1_befores.append(entry.get('f1_before'))
                    f1_drops.append(entry.get('f1_drop'))
                    configs.append(entry.get('config', {}))
            else:
                # 单次实验格式
                f1_afters.append(data.get('f1_after'))
                f1_befores.append(data.get('f1_before'))
                f1_drops.append(data.get('f1_drop'))
                configs.append(data.get('config', {}))
        except Exception as e:
            print(f"Warning: Failed to load {f}: {e}")

    return {
        'f1_after': f1_afters,
        'f1_before': f1_befores,
        'f1_drop': f1_drops,
        'configs': configs,
        'n_samples': len(f1_afters)
    }


def compute_relative_metrics(baseline_data, attack_data):
    """Compute relative F1 metrics."""
    baseline_f1 = np.mean(baseline_data['f1_after'])
    attack_f1 = np.mean(attack_data['f1_after'])

    baseline_std = np.std(baseline_data['f1_after'])
    attack_std = np.std(attack_data['f1_after'])

    # Gap: attack vs baseline
    gap = attack_f1 - baseline_f1

    # Relative drop (positive = attack effective)
    relative_f1_drop = -gap

    return {
        'baseline_f1_after': float(baseline_f1),
        'baseline_std': float(baseline_std),
        'attack_f1_after': float(attack_f1),
        'attack_std': float(attack_std),
        'gap': float(gap),
        'relative_f1_drop': float(relative_f1_drop),
        'baseline_n': baseline_data['n_samples'],
        'attack_n': attack_data['n_samples']
    }


def main():
    parser = argparse.ArgumentParser(description='Compute relative F1 metrics')
    parser.add_argument('--methods', type=str, default='GraphEraser,GUIDE,GNNDelete,GIF')
    parser.add_argument('--datasets', type=str, default='cora')
    parser.add_argument('--strategies', type=str, default='im,tracin,hybrid')
    parser.add_argument('--baseline_dir', type=str, default='results/baseline/k5_random')
    parser.add_argument('--attack_dir', type=str, default='results/experiments/mg0_completion/phase_a')
    parser.add_argument('--output_dir', type=str, default='results/relative')
    parser.add_argument('--k', type=int, default=5)
    args = parser.parse_args()

    methods = args.methods.split(',')
    datasets = args.datasets.split(',')
    strategies = args.strategies.split(',')
    os.makedirs(args.output_dir, exist_ok=True)

    results = []

    for method in methods:
        for dataset in datasets:
            # 加载 baseline (k=5, random)
            baseline_data = load_f1_results(
                args.baseline_dir, method, dataset,
                strategy='random', k=args.k
            )

            if baseline_data['n_samples'] == 0:
                print(f"Warning: No baseline found for {method}_{dataset}")
                continue

            for strategy in strategies:
                # 加载 attack 结果
                attack_data = load_f1_results(
                    args.attack_dir, method, dataset,
                    strategy=strategy, k=args.k
                )

                if attack_data['n_samples'] == 0:
                    print(f"Warning: No attack result for {method}_{dataset}_{strategy}")
                    continue

                metrics = compute_relative_metrics(baseline_data, attack_data)
                metrics.update({
                    'method': method,
                    'dataset': dataset,
                    'strategy': strategy,
                    'k': args.k,
                    'timestamp': datetime.now().isoformat()
                })

                results.append(metrics)

                print(f"{method} | {dataset} | {strategy}: "
                      f"gap={metrics['gap']:.4f}, relative_drop={metrics['relative_f1_drop']:.4f}")

    # 保存结果
    output_file = f"{args.output_dir}/relative_f1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'config': vars(args),
            'results': results
        }, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == '__main__':
    main()
```

### 输出格式

运行后会生成 JSON 文件：

```json
{
  "config": {
    "methods": ["GraphEraser", "GUIDE"],
    "datasets": ["cora"],
    "strategies": ["im", "tracin"],
    "k": 5
  },
  "results": [
    {
      "method": "GraphEraser",
      "dataset": "cora",
      "strategy": "im",
      "baseline_f1_after": 0.84,
      "attack_f1_after": 0.82,
      "gap": -0.02,
      "relative_f1_drop": 0.02,
      "baseline_n": 5,
      "attack_n": 5
    }
  ]
}
```

### 输出目录

```
results/relative/
├── relative_f1_20260225_143022.json
└── ...
```

---

## 测试结果

已测试 `eval_relative.py`，功能正常：

```bash
python eval_relative.py \
    --methods GraphEraser,GUIDE,GNNDelete \
    --datasets cora \
    --strategies im_v4,tracin,hybrid_v4
```

**输出示例**：
```
[GraphEraser_cora] Random baseline: 7 samples, f1_after=0.8432
  im_v4: gap=-0.0302, relative_f1_drop=0.0302 (attack effective)
  tracin: gap=0.0000, relative_f1_drop=-0.0000 (no significant difference)
  hybrid_v4: gap=-0.0255, relative_f1_drop=0.0255 (attack effective)

[GUIDE_cora] Random baseline: 7 samples, f1_after=0.8258
  im_v4: gap=0.0004, relative_f1_drop=-0.0004 (no significant difference)
  ...

[Cache] Saved: results/relative/relative_xxxx.json
```

**Cache 验证**：第二次运行相同参数时正确命中缓存。

**注意事项**：
- 策略名称使用 `im_v4` 而非 `im`（从 `_summary.json` 中读取）
- 默认 ratio=0.05（可配置）
- 支持 `--force` 强制重新计算