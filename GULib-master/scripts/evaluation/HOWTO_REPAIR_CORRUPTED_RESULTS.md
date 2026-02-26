# 指南：如何修复因代码 Bug 导致的受污染实验数据

当我们在底层代码（例如某个 Unlearning 算法的 `gnndelete.py` 等）中发现并修复了一个会导致“退化为随机猜测”、“F1 不变”等严重 Bug 时，直接运行实验脚本往往**无法生效**。这是因为框架的双层缓存机制和历史记录机制会直接读取之前跑出的错误数据。

为了确保代码修复后能够真正触发**重新训练 (Retrain)** 并生成正确数据，且**不丢失昂贵的图节点选点耗时 (Selection Cache)**，请严格按照以下标准化流程操作。

---

## 第一步：定位并清理被污染的结果缓存 (Result Cache)

框架的实验结果缓存在 `results/cache/` 目录下。当参数完全一致时，程序会直接读取缓存而非重新训练。

**目标**：仅删除受污染配置的 `Result Cache`，**绝对不要**删除 `results/selection_cache/`。

**操作**：编写并运行一个简易 Python 脚本来靶向删除。
例如，我们要清理 `GNNDelete` 的所有受污染缓存：

```python
# clean_target_cache.py
import json
from pathlib import Path

cache_dir = Path('./results/cache')
deleted_count = 0

if cache_dir.exists():
    for f in cache_dir.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                # 修改此处的判定条件为你的受污染目标
                if data.get('config', {}).get('unlearning_methods') == 'GNNDelete':
                    fp.close()
                    f.unlink()
                    deleted_count += 1
        except Exception as e:
            pass

print(f'Deleted {deleted_count} cached results.')
```
```bash
python clean_target_cache.py
```

---

## 第二步：清理被污染的历史实验记录 (Experiment Logs)

除了底层 Cache，由于修复模式 (`--repair`) 依赖于检测 `results/experiments/` 中的 `_summary.json` 文件。如果错误的数据已经记录在案，修复脚本会认为“这个实验已经跑过了”而跳过。

**目标**：删除受污染的独立 JSON 文件，并从 `_summary.json` 中剔除相应的字典记录。

**操作**：运行针对性的清理脚本。
例如，清理 `GNNDelete` 在 `citeseer` 数据集上的历史记录：

```python
# clean_target_history.py
import json
from pathlib import Path

exp_dir = Path('results/experiments')

# 1. 删除独立的错误 JSON 文件
deleted_files = 0
for f in exp_dir.rglob('*.json'):
    if 'cache' in str(f) or 'auto_discovered' in str(f) or 'attack_matrix' in str(f) or '_summary' in str(f):
        continue
    try:
        with open(f, 'r') as fp:
            data = json.load(fp)
        # 修改此处的判定条件
        if isinstance(data, dict) and data.get('config', {}).get('unlearning_methods') == 'GNNDelete' and data.get('config', {}).get('dataset_name') == 'citeseer':
            f.unlink()
            deleted_files += 1
    except Exception: pass

# 2. 从 _summary.json 中剔除错误记录
updated_summaries = 0
for f in exp_dir.rglob('_summary.json'):
    try:
        with open(f, 'r') as fp:
            data = json.load(fp)
        
        modified = False
        if 'results' in data:
            keys_to_delete = [k for k in data['results'].keys() if k.startswith('GNNDelete_citeseer')]
            for k in keys_to_delete:
                del data['results'][k]
                modified = True
                
        if modified:
            with open(f, 'w') as fp:
                json.dump(data, fp, indent=2)
            updated_summaries += 1
    except Exception: pass

print(f"Deleted {deleted_files} bad standalone JSON files.")
print(f"Cleaned entries from {updated_summaries} _summary.json files.")
```
```bash
python clean_target_history.py
```

---

## 第三步：执行主实验修复 (Repair Main Experiments)

缓存和历史记录清理干净后，即可使用自带的补全机制。

**注意**：**千万不要加上 `--no_cache`**，因为我们必须依赖 `selection_cache` 来跳过几百秒的 IM 等策略选点耗时，让重修能够实现“秒刷”。

执行对应实验的 Repair 命令，例如：
```bash
# 针对 MG-1 实验使用 --repair 模式
./scripts/experiments/run_mg1_citeseer.sh --repair
```
或者直接使用 `demo_attack.py` 覆盖运行：
```bash
python demo_attack.py --methods GNNDelete --datasets citeseer --base_model GCN --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --ratios 0.05 --seeds 42,212,722,1337,2024
```

---

## 第四步：修复下游衍生评估 (Relative & Collateral)

主实验缓存生成后，衍生计算（例如 Relative Drop 和 Collateral Damage）往往也包含旧的错误缓存。为了防止脚本因检测到已有结果而跳过，**必须先手动删除对应的衍生结果缓存**。

**1. 清理衍生评估缓存：**
```bash
# 删除 Relative 和 Collateral 的旧结果文件 (以 GNNDelete_citeseer 为例)
rm -f results/relative_eval/GNNDelete_citeseer*
rm -f results/collateral_eval/GNNDelete_citeseer*
```

**2. 执行针对性修复指令：**
```bash
# 修复 Relative (随机基线评估)
python experiments/baseline_k5/eval_relative.py --unlearning_methods GNNDelete --dataset_name citeseer --base_model GCN --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --unlearn_ratio 0.05 --random_seed 42,212,722,1337,2024 --repair

# 修复 Collateral Damage (连带损伤评估)
python eval_collateral.py --unlearning_methods GNNDelete --dataset_name citeseer --base_model GCN --unlearn_ratio 0.05 --repair
```

---

## 第五步：重新生成最终统计表

所有数据更新完毕后，运行最后的数据聚合脚本，确保输出到论文或报告里的 CSV 表格是最新计算的准确数据：

```bash
python scripts/evaluation/final_data_aggregator.py
```

## 总结

**Bug 修复后的数据刷新黄金法则：**
1. 删 Result Cache
2. 删 / 修 Experiments JSON 历史文件
3. 带 `--repair` 重跑主实验 (秒读选点，真实重练)
4. 带 `--repair` 重跑 Relative 和 Collateral 评估
5. 重新聚合数据
