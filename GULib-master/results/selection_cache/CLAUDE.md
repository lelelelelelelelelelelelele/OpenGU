# results/selection_cache/ — SelectionCache（哈希命名，跨方法共享）

> Created: 2026-05-03
> Maintained by: `attack/selection_cache.py`
> 上层规则：`self/dashboard/CLAUDE.md`

## 目的

缓存 attack strategy 选出来的**节点 ID 列表**（不含 metrics）。**跨 GU method 共享**——同一个 IM 选点可被 GIF / GNNDelete / GraphEraser 重复使用，省去 selector 的重复计算（IM 在大图上几小时不止）。

## 命名约定

文件名 = hash(strategy_config)，与 `cache/` 同样是 hash 命名。`strategy_config` 一般包含：

- `dataset`, `model`（pre-unlearn 模型）
- `strategy_name`, `k`（或 `ratio`）
- 该 strategy 的内部参数（mc_rounds、propagation_prob 等）
- `seed`（GU 训练 seed——见下方"selector seed vs GU seed"）

**关键设计**：key 不含 GU `method` 字段——因为同一组选点对所有 method 通用。

## selector seed vs GU seed（重要）

**当前设计**：selection_cache 的 hash 含 GU 训练 seed，导致：

- 同一 strategy 在不同 GU seed 下选出**不同节点集**
- IM_v4 在 5 个 GU seed 下 Jaccard 仅 0.13（详见 `self/dashboard/VALIDATION_LOG.md` V-2026-05-03-03）

**Phase A.4 计划解耦**：让 IM_v4 用 fixed `mc_seed`（与 GU seed 无关）。改完后：

- 旧 selection_cache 条目仍可用（其他 strategy 不受影响）
- 新 IM_v4 条目跨 GU seed 共享同一组选点 → cache 体积下降
- 解耦后产生的新 cache key 模式与旧的不冲突（hash 不同）

## 当前状态（2026-05-03 快照）

- 文件数：297 个 JSON
- 总大小：~2.2 MB
- 解析状态：全部可读

## 文件内容结构

```json
{
  "cache_key": "...",
  "config": { strategy 子配置 },
  "selected_nodes": [...],
  "selection_time": ...,
  "cached_at": "..."
}
```

## 安全规则

与 `results/cache/CLAUDE.md` 同——**不要改名、不要手动编辑、整目录可删**。

## 不要清空 selection_cache 的场景

- 改了 GU 方法实现 → 选点不变，不要清
- 改了 metric 计算 → 选点不变，不要清
- 改了 IM_v4 的 mc_seed 处理（Phase A.4）→ 旧 entries 保留，新 entries 用新 hash 自动生成

## 必须清空 selection_cache 的场景

- 改了 strategy 的核心算法（IM 公式变了、TracIn 改用不同梯度）→ 旧选点无效
- 改了 dataset 处理逻辑（split 方式变了）→ 节点 index 含义变了

## 重建命令（应急）

如果 selection_cache 丢失或损坏：

```powershell
python scripts/tools/extract_selection_cache.py
```

从 `results/experiments/` 的历史 JSON 中重建（per `results/README.md` §5）。

## 与 cache/ 的协同

跑一次 attack run：

1. selector 先查 `selection_cache/` → 命中则秒级 return；miss 则跑 selector + 写 cache
2. 用选出的节点跑 GU unlearn + retrain → 写 `cache/`
3. 两层 cache 命中模式不同：selection_cache 跨 method 命中率高，cache 仅同配置命中
