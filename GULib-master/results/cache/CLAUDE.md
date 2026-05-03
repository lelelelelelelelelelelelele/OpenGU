# results/cache/ — ResultCache（哈希命名）

> Created: 2026-05-03
> Maintained by: `attack/result_cache.py`
> 上层规则：`self/dashboard/CLAUDE.md`

## 目的

缓存一次完整 attack run 的所有 metrics，避免重复跑 GU 训练。

每个文件 = 一个 `(method, dataset, model, ratio, seed, strategy, ...)` 配置的结果。

## 命名约定

文件名 = MD5/SHA hash of config dict（来自 `result_cache.py`），形如 `0246aba9a1d44233f82eada786244b6b.json`。

**绝对不要手动改名**——cache 查找逻辑用 hash 反查，重命名会让所有现有数据"消失"。

## 文件内容结构

```json
{
  "cache_key": "0246aba9...",
  "cached_at": "2026-02-21T18:31:22",
  "config": { ... 完整 attack 配置 ... },
  "result": { ... metrics dict ... }
}
```

`config` 字段是反查的唯一钥匙。看不懂某个 hash 文件时，直接读 `config`。

## 当前状态（2026-05-03 快照）

- 文件数：1148 个 JSON
- 总大小：~12 MB
- 解析状态：全部可读，未发现坏文件（per `results/README.md`）

## 为什么不重命名

历史决策：hash 命名保证**任意配置组合都能稳定 hit**（不会因为人手错命名而 miss）。代价是不直观——这个代价用 `_index.json` 解决，不用重命名解决。

## 反查工具（待建）

`scripts/dashboard/cache_lookup.py`（计划 Phase A 后期建）：

```powershell
# 正向：知道 config 找 hash
python scripts/dashboard/cache_lookup.py --method GIF --dataset cora --strategy im_v4 --seed 722
# → results/cache/0246aba9....json

# 反向：知道 hash 找 config
python scripts/dashboard/cache_lookup.py --hash 0246aba9
# → {method: GIF, dataset: cora, ...}
```

工具读取 `_index.json`（自动从所有 cache 文件抽 `config` 字段建立）。

## 安全规则（不要做的事）

| 操作 | 后果 |
|------|------|
| `rm *.json` 批量删除 | 全部缓存丢失，需重跑 |
| 手动改名（如改成 `GIF_xxx.json`）| `result_cache.py` 反查失败，等同丢失 |
| 编辑 cache 文件内容 | 下次 hash 命中时数据污染 |
| 跨机器复制时改路径分隔符 | 可能读不出 config 路径字段 |

## 可以做的事

| 操作 | 说明 |
|------|------|
| 整目录删除（`rm -rf cache/`）| 安全，下次跑会自动重建。仅丢失"是否需要重跑"的判断成本 |
| 备份 | `tar` 整个目录即可 |
| 查看某个文件 | `cat <hash>.json` 读 `config` 字段判断是什么 |
| 用 `cache_lookup.py` 查询 | 推荐方式 |

## 与 selection_cache 的差别

- `cache/`（本目录）：完整 attack run 的最终 metrics——high-level，跑一次产出一个 cell
- `selection_cache/`：selector 选出的节点 ID 列表——low-level，跨 GU method 复用（同一个 IM 选点可被多个 method 用）

修了 metric bug（如 MIA bug）后必须**清掉 cache/ 再重跑**，但 `selection_cache/` 通常无需清（除非 selector 行为变了）。

## bug 修复期注意

Phase A 修 MIA bug 后，所有受影响 family（MEGU/IDEA/GraphEraser/GUIDE）的 cache 文件含错的 `mia_auc=0.0`。两个选项：

1. **清相关 cache 重跑**（推荐）：保证 paper 的 MIA 数字一致
2. **保留 + 标污**：在 `_index.json` 加 `mia_bug=true` 字段；后续读取时跳过 mia_auc 字段

当前推荐 1，因为 Phase B 反正要 arxiv 重跑，piggyback 修复成本低。
