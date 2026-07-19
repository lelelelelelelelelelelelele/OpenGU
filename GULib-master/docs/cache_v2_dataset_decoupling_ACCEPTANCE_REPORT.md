---
title: Cache V2 Dataset 职责解耦验收报告
date: 2026-07-15
updated: 2026-07-16
status: accepted-server-smoke-follow-up
---

# Cache V2 Dataset 职责解耦验收报告

## 1. 验收结论

**ACCEPTED。** Cache V2 的 dataset 职责越界已关闭：Cache 代码不再导入 dataset/experiment、Torch/PyG/OGB 或 YAML，不再提供 producer callback；canonical processed dataset、persisted candidates 和 selector 调用全部位于 OpenGU experiment 层。Cache exact hit 只做 Recipe/Artifact 解析与完整性校验，miss 由上游 producer 计算后显式写入。现有 canonical Cora 与 CPU 回归证据足以支持本次 Cache V2 有效性判断；服务器 smoke 仅作为环境差异检查，不是验收门槛。

| 验收项 | 结论 | 证据 |
|---|---|---|
| Dataset ownership | 通过 | `experiments/selection_inputs.py` 只读 canonical processed pickle，不下载、不重建 split |
| Cache dependency boundary | 通过 | AST 静态测试确认 `cache_v2` 无 dataset/experiment/torch/PyG/OGB/YAML import |
| Cache HIT isolation | 通过 | HIT API 无 provider/producer 参数；测试注入 forbidden provider/producer，调用数为 0 |
| Cache MISS ownership | 通过 | `experiments.selection_producer` 调用注入 producer、校验节点，再调用纯 store API |
| Recipe identity | 通过 | 绑定 dataset fingerprint、candidate hash、selector seed/k 与 producer version |
| Store/conflict/integrity | 通过 | Artifact ID、原子写入、identical、conflict marker、quarantine、corruption fail-closed 回归通过 |
| Runner / AutoReport | 通过 | selection-only、attack-only、complete、failed:collateral 与 authoritative Cache provenance 回归通过 |
| Canonical Cora | 通过 | 2708 nodes、10556 edges、2166 persisted candidates；CPU cold/warm 同一 Artifact |
| Server smoke | 非阻塞 TODO | 本地已有 canonical processed Cora 与充分 CPU 证据；后续只排查服务器环境/路径差异，不重判架构有效性 |

## 2. 实现落点

- 新增 `experiments/selection_inputs.py`：从 `data/processed/{transductive|inductive}` 读取 OpenGU 既有 pickle，以持久化 `train_mask/train_indices` 形成 candidate set，并生成 dataset/graph/candidate fingerprints。
- 新增 `experiments/selection_producer.py`：保留 IM/Random/Degree/PageRank 现有机制与版本语义，负责 request 展开、strategy import、producer 调用、结果校验与 Legacy 只读比较。
- 收缩 `cache_v2/selection_materializer.py`：仅保留 Selection Recipe v2、exact resolver 和显式 selected-node Artifact materialization。
- 收缩 `cache_v2/store.py`：删除 `get_or_compute`、`observe_recomputation`、producer counter 与 callback 执行；保留纯 `store_selection`、read-only load、完整性与冲突处理。
- 更新 `experiments/run.py` 与 `scripts/cachectl.py`：使用 `processed_root` 上游路径；Cache 配置中的 `dataset_root` / `allow_download` 明确 fail closed。
- 更新独立 canary：只接受 canonical `--processed-root`，不再支持临时 raw dataset 或下载。

详细边界见 `docs/cache_v2_dataset_decoupling_DESIGN.md`。

## 3. 关键路径验证

### 3.1 HIT

```text
Selection Recipe identity -> exact resolver -> payload/header verification -> Artifact
```

Cache HIT 测试同时安装会抛错的 dataset provider 与 producer。`resolve_selection_artifact` 命中后二者调用数均为 0；payload 内容与 Artifact ID 验证通过，store 文件不变。

### 3.2 MISS

```text
canonical processed provider -> SelectionInputs -> exact miss
-> experiment producer -> candidate validation -> Cache store
```

冷启动只由注入的 experiment producer 计算一次；随后相同 Recipe 的 warm 调用启用 fail-if-called sentinel，返回 exact hit 且 `producer_called=false`。

### 3.3 兼容边界

- Artifact ID 构造与 `sel_<recipe8>_<content8>` 形式未改变。
- 旧 Artifact 可继续按显式 Artifact ID 读取。
- 新 producer resolution 必须携带 `opengu-selection-recipe-v2` 完整 identity；旧 Recipe 不隐式升级，明确 fail closed。
- Legacy cache 只读快照在 canonical cold/warm 前后相同；未执行 promotion、repair、delete 或 archive mutation。

## 4. Canonical processed Cora 证据

只读输入为：

```text
E:\project\OpenGU\GULib-master\data\processed\transductive\cora0.8_0_0.2.pkl
```

| 字段 | 结果 |
|---|---|
| nodes / edges | 2708 / 10556 |
| persisted candidates | 2166 |
| device | CPU |
| dataset fingerprint | `a77b911b3feddfd6d9aa269e2b4048304a9f5e4f21fe36539d99d7fce874354b` |
| candidate set hash | `7d55f2d596ea4386a1d1d926a7a662e19e0c53202e6da8782292a3a2a5304765` |
| Degree ratio / k | 0.05 / 108 |
| Recipe hash | `04fe0b95d7d8388e366638caf23f92ede2a607e162a8ebd24ea7c65917ddc5ea` |
| Artifact ID | `sel_04fe0b95_82b98325` |
| cold | `hit=false`, `producer_called=true` |
| warm | `hit=true`, `producer_called=false` |
| Legacy snapshot | cold/warm 均 `legacy_cache_unchanged=true` |

最终隔离 store 位于 ignored `.planning/cache-v2-decouple-dataset-20260715/canonical-cora-store-final`，没有写入、删除或移动 `results/cache`、`results/cache_v2`、`results/runs` 或服务器 archive。

## 5. 测试结果

### 5.1 范围内回归

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q `
  <all tests/test_cache_v2*.py> tests/test_auto_report_v3.py
# 118 passed in 3.86s
```

覆盖：Recipe/Artifact/store/resolver、HIT/MISS 注入边界、canonical Cora shape、runner integration、selection-only / attack-only / complete / failed:collateral、AutoReport authority/source/Recipe、Legacy freeze 与 conflict resolution。

### 5.2 宽 CPU 回归

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
E:/conda_package/envs/gnn/python.exe -m pytest -q tests `
  --ignore=tests/test_report_figure_refresh.py `
  --deselect=tests/test_collateral.py::TestGetTrainedModel::test_extracts_from_target_model `
  --deselect=tests/test_collateral.py::TestGetTrainedModel::test_extracts_from_model_zoo `
  --deselect=tests/test_collateral.py::TestGetTrainedModel::test_fallback_to_pipeline_model
# 500 passed, 3 deselected in 17.01s
```

3 个 deselected 测试依赖手工构造但没有 `args` 的既有 `AttackPipeline` stub，失败点位于未修改的 `attack/pipeline_adapter.py`，与本改动无关。本任务未顺手修改它。首次宽扫描未屏蔽本机 CUDA 时，TracIn/Hybrid 测试在不兼容的 5070 kernel launch 处失败；显式禁用 CUDA 后 9 项全部通过，未修改其机制。

## 6. AutoReport 与 staged runner

回归确认：

- status projection 保持 `selection-only`、`attack-only`、`complete`、`failed:collateral`；
- runner 仍将同一 Selection Artifact 映射给对应 strategy/seed consumer；
- selection event 保持 `authoritative=true`、`cache_v2:<artifact_id>` hit source、`cache_v2_exact_artifact_id` lookup policy 与 Recipe hash；
- `demo_attack.py` / `eval_collateral.py` 继续接收显式 Artifact ID，attack/collateral 分阶段能力不变。

## 7. 完成清单

- [x] 从 `fa67c13` 在独立 worktree 创建 `codex/cache-v2-decouple-dataset-20260715`。
- [x] dataset provider、candidate identity 与 Selection producer 移至 experiment 层。
- [x] Cache 删除 dataset/download/split/selector import 与 producer callback。
- [x] Recipe 绑定 dataset fingerprint、candidate hash 与 producer version。
- [x] 旧 Recipe 提供明确 fail-closed 版本边界，旧 Artifact 显式 ID 读取保留。
- [x] runner、Cache/AutoReport、stage、conflict/integrity CPU 回归通过。
- [x] canonical processed Cora 本地只读与 cold/warm CPU 验证通过。
- [x] Markdown 设计说明与 Markdown/HTML 成对验收报告完成。

### 非阻塞后续 TODO

- [ ] 在标准根 `/autodl-fs/data/OpenGU/GULib-master` 做最小 CPU server smoke；仓库与历史结果目录保持只读，不下载数据、不运行 GPU。该项只排查环境/路径差异，不影响本报告的 `ACCEPTED` 结论。

### 明确非目标

- TracIn/Hybrid producer 接入或算法机制修改。
- 3 个既有 `AttackPipeline` stub 测试修复。

## 8. 已知边界

本轮不迁移历史 Selection Recipe，不改变 TracIn/Hybrid 算法，不下载数据，不运行正式 GPU 实验，不修改服务器 AutoReport archive。服务器 smoke 不是本地验收通过的前置条件；后续只在标准根 `/autodl-fs/data/OpenGU/GULib-master` 做最小 CPU 环境确认，并保持仓库、现有 cache/results 与历史 archive 不变。
