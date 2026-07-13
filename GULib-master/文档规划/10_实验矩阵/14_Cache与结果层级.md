---
title: Cache 与结果层级
created: 2026-07-09
updated: 2026-07-09
type: experiment-cache-map
tags: [cache, results, experiment, rerun]
---

# Cache 与结果层级

这页只回答一个问题：**跑出来的结果和 cache 分几层，修 bug 时应该动哪一层。**

结论：

- `results/runs/` 是 Phase B 的当前主产物。
- `results/cache/` 是旧 pipeline / ResultCache 的完整 cell 缓存。
- `results/selection_cache/` 是选点列表。
- `results/score_cache/` 是昂贵 score 的中间缓存，其中 TracIn 看 `score_cache/if/`，IM 看 `score_cache/im*`。
- 修 GraphRevoker 不等于清 selector cache；修 TracIn 不等于清 IM cache。

---

## 1. 主结果层：`results/runs/`

Phase B 每个 cell 写在：

```text
results/runs/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{N}/
  attack.json
  collateral.json
  predictions.npz
  _meta.json
```

| 文件 | 层级 | 含义 | 可否离线重算 |
|---|---|---|---|
| `attack.json` | L3 metric | attack 结果、selected nodes、F1 / update-detection AUC 等 | 部分可重算 |
| `collateral.json` | L3 metric | retrain gap、prediction shift、hop-decay 等 | 部分可重算 |
| `predictions.npz` | L2 artifact | before / unlearned / retrained logits、labels、masks | 不能便宜重算 |
| `_meta.json` | audit | config、git sha、时间、机器 | 不重算 |

`produced` 只说明这些文件存在；`usable` 才说明实现、cache、metric 口径都能当证据。

---

## 2. Cache 层

| 层 | 路径 | 存什么 | 共享范围 | 修复时怎么判断 |
|---|---|---|---|---|
| ResultCache | `results/cache/` | 完整 attack run metrics | 同 config | metric / method / selector 输出污染时，清对应配置或整层重跑 |
| SelectionCache | `results/selection_cache/` | `selected_nodes` | 通常跨 method | selector 算法变了才清 |
| ScoreCache IF | `results/score_cache/if/` | TracIn per-candidate scores | per method / seed 保守 key | TracIn 公式、eval/query loss、梯度定义变了必须清或隔离 |
| ScoreCache IM | `results/score_cache/im/` | IM initial marginal gains | 跨 method / seed | GraphRevoker / TracIn 修复不清 |
| ScoreCache IM-CELF | `results/score_cache/im_celf/` | full CELF selected nodes + gains | 跨 method / seed，同 k | GraphRevoker / TracIn 修复不清 |
| Baseline cache | `results/baseline/k5_random/` | k=5 noise floor | per method/model/seed | method dispatcher 或 baseline generator 变了才补 |
| Method state | `data/<Method>/` | checkpoint / partition / method 内状态 | method-local | method 实现、聚合器、架构维度或磁盘状态污染时清对应 method |

---

## 3. 两个典型修复

| 修复 | 应动 | 不应动 |
|---|---|---|
| GraphRevoker method 修复 | `data/GraphRevoker/`、`results/runs/*/GraphRevoker_*/`、GraphRevoker k=5 baseline（如旧 alias 污染） | random/degree/pagerank/IM/TracIn 的 selection cache；其他 method outputs |
| TracIn proper fix | `results/score_cache/if/`、TracIn/Hybrid selection cache、`results/runs/*/*_tracin|*_hybrid/` | IM cache；random/degree/pagerank/IM outputs；GU method state |

详细流程见 [[13_重跑与缓存修复Runbook]]。

如果问题不是单次 rerun，而是 `ResultCache` / `SelectionCache` / `selected_nodes` source of truth 的架构治理，见 [[19_Cache架构重设计与迁移方案]]。

边界不要混用：本页记录现有 Legacy 层级与故障处置；V2 架构落地和迁移默认只读 Legacy，不把“修复某次坏 cache”扩大成批量迁移或清理。

---

## 4. 判定表

| 问题 | produced | usable | rerun |
|---|---|---|---|
| 文件存在但 GraphRevoker method 退化 | yes | no | yes |
| 文件存在但 old TracIn 公式 | yes | no | yes |
| random / degree / pagerank / IM 与 TracIn bug 无关 | yes | yes, 若其它口径无误 | no |
| only 新增 forward metric | yes | yes, 可补 metric | no train rerun |
| `predictions.npz` 缺失 | partial | no | yes |
| `_meta.json` 缺失 | suspicious | no | rerun or audit manually |

---

## 5. 修改后同步

cache / result 口径变化至少同步：

- [[13_重跑与缓存修复Runbook]]
- [[15_实验运行入口与脚本]]
- [config_inventory.html](../../self/dashboard/config_inventory.html)
- [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)
- [[00_动态工作台/02_TODO台账]]

