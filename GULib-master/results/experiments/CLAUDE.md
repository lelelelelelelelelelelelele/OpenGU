# results/experiments/ — 实验主结果（按批次组织）

> Created: 2026-05-03
> 上层规则：`self/dashboard/CLAUDE.md`

## 子目录的真正含义（最重要）

历史命名很短，肉眼看不出来对应什么实验。下面是**唯一权威的对应表**：

| 子目录 | 实验内容 | 数据集 | 模型 | 备注 |
|--------|---------|-------|------|------|
| `mg0_completion/` | **稳定性实验**（同 dataset/model 多 seed） | cora | GCN | N=5 seeds, ratio=0.05, 5 family，FIG-4b 数据源（前 3 行）|
| `mg1_citeseer/` | **跨数据集** | citeseer | GCN | 仅 GIF/GNNDelete/GraphEraser |
| `mg2_gat/` | **跨 backbone**（GCN → GAT）| cora | GAT | 仅 GIF（部分）|
| `mg3_citeseer/` | **跨 dataset 扩展**（含 IDEA/MEGU）| citeseer | GCN | IDEA/MEGU/GIF/GNNDelete/GraphEraser |
| `mg3_gat/` | **跨 backbone 扩展**（含 IDEA/MEGU）| cora | GAT | FIG-4b 数据源（后 2 行）|
| `p2_ext_gif_GCN/` | GIF 在 GCN 上的 ratio 敏感性 / 扩展 | citeseer | GCN | 仅 GIF |
| `p2_ext_gif_GAT/` | 同上 GAT | citeseer | GAT | 仅 GIF |
| `p2_ext_gif_GIN/` | 同上 GIN | citeseer | GIN | 仅 GIF |
| `im_v4_compare/` | IM_v4 vs 旧 IM 性能对比 | — | — | 方法学 ablation |
| `im_v4_probe/` | IM_v4 算法内部 probe | — | — | debug 用 |
| `ratio_sensitivity/` | ratio sweep | citeseer | GCN/GAT/GIN | 仅 GIF，ratio={0.05, 0.1, 0.2} |
| `_archive/` | 归档（旧批次）| — | — | 只读，不要再写入 |
| `_tmp_timeout_test/` | 临时调试输出 | — | — | 可删 |

## 路径模板

```
results/experiments/<group>/phase_a/<YYYYMMDD_HHMMSS>_seed<seed>/<Method>_<dataset>_<model>_r<ratio>_s<seed>.json
```

例：
```
results/experiments/mg0_completion/phase_a/20260221_183122_seed722/GNNDelete_cora_GCN_r0.05_s722.json
```

## 单文件 JSON 结构

```json
{
  "config": { CLI 参数完整快照 },
  "results": {
    "random":   { "f1_drop": ..., "mia_auc": ..., "selected_nodes": [...] },
    "tracin":   { ... },
    "im_v4":    { ... },
    "hybrid_v4":{ ... },
    "pagerank": { ... },
    "degree":   { ... }
  },
  "summary": { 跨 strategy 聚合 }
}
```

每个 strategy 块的字段定义见 `self/dashboard/METRICS_CATALOG.md`。

## 写入规则

- 由 `main.py` 通过 `attack/result_cache.py` 写入
- 每次重跑写新 timestamp 目录，不覆盖
- 同 (group, seed) 的多次重跑：保留 `completed==total_experiments` 的最新一个，旧的归档到 `_archive/`

## 安全规则

| 操作 | 安全？ |
|------|-------|
| 删除 `_archive/` 内容 | ⚠ 失去历史对照，建议保留 |
| 删除 `_tmp_*` | ✓ 安全 |
| 删除某个 group（如 `im_v4_compare/`）| ⚠ 视情况：若是 ablation 数据，保留；若仅 debug，可删 |
| 手动编辑 JSON | ❌ 不要——会被下次 aggregator 误读 |

## 数据流水线

JSON → `eval_relative.py` → `results/relative/` → `final_data_aggregator.py` → `results/evaluation/stats/final_paper_stats.csv`

详见 `results/README.md` §9。

## 已知 bug 影响（截至 2026-05-03）

⚠ 所有 mg0/mg1/mg3 的 IDEA/MEGU/GraphEraser 文件中的 `mia_auc` 字段为 0.000——**是代码 bug，不是真实测量**。详见 `self/dashboard/EXPERIMENT_DASHBOARD.md §3.1`。

Phase B 重跑修复后，新文件的 mia_auc 会是真实值。**短期内的解析逻辑必须能区分**：

- 0.000 + 任何旧 timestamp → MIA bug 污染，跳过
- 0.000 + 新 timestamp（>= 2026-05-04）→ 真实测量值，保留

## 何时新增子目录

- 新批次实验（如 `mg4_ogbn_arxiv/`）→ 直接建新目录
- 命名规范：保留 `<short_id>_<key_descriptor>` 模式
- **必须更新本文件的对应表**——否则 4 天后又忘了

## 当前 Phase B 计划新增

| 计划目录 | 内容 |
|----------|------|
| `mg5_arxiv_main/` | ogbn-arxiv 主矩阵（5 family × 4 strategy × 3 seed）|
| `mg5_arxiv_feasibility/` | arxiv 可行性闸（每 family × random × 1 seed）|
| `b2_anchor/` | B2 sanity 单点实验 |
