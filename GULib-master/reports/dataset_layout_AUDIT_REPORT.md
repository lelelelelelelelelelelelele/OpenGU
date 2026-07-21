# 小图 Selection Dataset 布局审计与迁移报告

> **Verdict: CONDITIONAL PASS** — SSH active 主目录的数据路径、代码解析与 provenance 合同已经收口；public Cora/CiteSeer/PubMed 可从主目录无下载读取。OpenGU canonical processed 的 PubMed pair 仍缺失，正式 `3 datasets × 3 seeds` GPU cold/warm 矩阵因当前容器未挂 GPU 而尚未启动。

## 1. 结论

- SSH 登录与正式 active checkout 根目录均为 `/autodl-fs/data/OpenGU/GULib-master`。
- public 17-method benchmark 的唯一默认根已定为 `/autodl-fs/data/OpenGU/GULib-master/data/raw`，数据目录为 lowercase `cora`、`citeseer`、`pubmed`。
- OpenGU integrated Selection 的 canonical 输入仍是 `/autodl-fs/data/OpenGU/GULib-master/data/processed/{transductive,inductive}/*.pkl`。它与 public Planetoid 固定 split 是两条不同数据通道。
- 旧 benchmark 实际使用 `/autodl-fs/data/OpenGU-shared/Planetoid` 和隔离 worktree；其 `9/9` 只保留为 public-split 诊断证据，不能改称 active-root 或 OpenGU 80/20 实验。
- 三套 public PyG cache 已从共享副本复制到 active 主目录，源副本保留，目标逐文件 SHA-256 验证通过。
- accepted CiteSeer canonical processed pair 已回填 active；Cora pair 原本已在 active 且与历史副本相同；PubMed pair 未在受检历史目录中找到，因此未用 public `data.pt` 冒充。
- 代码提交 `da3688c3e40b6b2d50f26717ad036b8c041bbde0` 将 B/C selection、benchmark、matrix 与 downstream 改成 repo-relative、fail-closed、path-aware + content-aware provenance。

## 2. 冻结的数据合同

| 通道 | Canonical root | 数据含义 | Runner 行为 |
|---|---|---|---|
| Public Planetoid benchmark | `<checkout>/data/raw/{cora,citeseer,pubmed}` | PyG `split=public`；用于本轮 17-output B/C benchmark | 必须已有 8 个 `ind.<dataset>.*` raw 文件和 `processed/data.pt`；禁止自动下载与运行时加工 |
| OpenGU integrated Selection | `<checkout>/data/processed/{transductive,inductive}` | OpenGU 持久化图、split 与候选集 | 只读 canonical pickle；禁止下载或重建 split |
| Runtime cache / outputs | `<checkout>/results/cache_v2/...` 与版本化 output root | ScoreBundle、Selection Artifact 和报告证据 | 换算法或数据合同必须使用新 recipe/output identity；旧证据不覆盖 |

每个新 selection summary 都记录：requested root、absolute/resolved/canonical root、resolved dataset/raw/processed 路径、8 个 raw SHA-256、`data.pt` SHA-256、聚合 source fingerprint、split count、Git HEAD/branch/dirty 状态和代码 source fingerprint。cold、warm 与 downstream 必须消费同一 source fingerprint 和 resolved path。

## 3. SSH active public 数据

| Dataset | Active dataset directory | Source fingerprint | `processed/data.pt` SHA-256 | Public train/val/test |
|---|---|---|---|---:|
| Cora | `/autodl-fs/data/OpenGU/GULib-master/data/raw/cora` | `8201869db05fe584d6ee429b1c965be6b4cb4214b312c70963ac3be7b45e888f` | `1ac38ca581468b1c24a6a14ca30f735f384ff8c643b781c657c3d476e382413f` | `140/500/1000` |
| CiteSeer | `/autodl-fs/data/OpenGU/GULib-master/data/raw/citeseer` | `fba32999724ad1cf79676f3a0f09583c63ec9e439dfefaa6430dd7ba85e533da` | `d40ff756d7134c211899c75d52b1ad3c2429bb1880d84eb0a129317df448534d` | `120/500/1000` |
| PubMed | `/autodl-fs/data/OpenGU/GULib-master/data/raw/pubmed` | `3ccd73931a2a9149a20d782036f8ecb5f5eb50e797396d176244e1ff74001f6c` | `2b28d1f66a49c05ab1422bc5653fb7f7e1b3243c644b3b8fb12fadc562b3d09b` | `60/500/1000` |

PyG 从三个 lowercase active 路径直接读取后得到的图规模分别为 Cora `2708 nodes / 10556 directed edges`、CiteSeer `3327 / 9104`、PubMed `19717 / 88648`。这些计数和 fixed masks 均由 runner 在加载后再次验证。

## 4. SSH active OpenGU canonical processed 数据

| Dataset | Split data pickle | Dataset pickle | 状态 |
|---|---|---|---|
| Cora | `e8919e1850b4a9682a384d93dd2f8cf3733190d565ee9287843af1cd82b5432f` | `1dcbb6be57c174bcad6fe8186ec5eadfeb01196dd7ee33772e697aa5057ad6e4` | 原已存在；OpenGU split `2166/0/542` |
| CiteSeer | `20773eda474ea46a0a063eb6ef6615572c2cede317419f500f2a9f0018b3941b` | `fbb744100deca78b049d9a43762b3feb78232e8d4f1e8341fe471c2e9f7d6e84` | 从 accepted E1 副本 exclusive-create 回填；OpenGU split `2661/0/666` |
| PubMed | — | — | **MISSING**；未找到可信历史 80/20 pair，不允许以 public PyG `data.pt` 替代 |

public 与 OpenGU canonical 的 Cora/CiteSeer node/edge 数一致，但 candidate/target masks 不同。路径正确不代表 split 正确，因此 runner 同时绑定文件内容与 split identity。

## 5. 重复副本审计

| 位置 | 内容 | 与 active 的关系 | 当前处理 |
|---|---|---|---|
| `/autodl-fs/data/OpenGU-shared/Planetoid` | Cora/CiteSeer/PubMed public raw + PyG processed | active 三套 public cache 的复制源；迁移后逐文件相同 | 保留；待用户明确批准后才删除 |
| `/autodl-fs/data/OpenGU-worktrees/tracin-v2-g4/data/Planetoid/Cora` | Cora public cache | raw 与 `data.pt` 相同；仅 PyG `pre_filter.pt` / `pre_transform.pt` 元数据不同 | 保留；语义重复候选 |
| accepted CiteSeer E1 checkout `data/raw/citeseer` | CiteSeer public cache | 11/11 文件与 shared/active 相同 | 保留；实验归档确认后可清理 |
| GraphRevoker experiment checkouts | Cora canonical processed pair | 与 active 两个 pickle byte-identical | 保留；不能把 method-specific evidence 一并误删 |
| accepted E1、A5 及 A5 nested checkout | CiteSeer canonical processed pair | 三组 pickle byte-identical；A5 存在 nested `GULib-master/GULib-master` 重复 | 保留；nested leaf 是最高优先清理候选 |
| 本地 `E:/project/OpenGU/GULib-master/data/raw/Planetoid` | 三套 public cache | CiteSeer/PubMed 内容相同；Cora test-index 仅行尾不同且 `data.pt` 序列化不同，语义需按 tensor 验证 | 保留；不做无确认删除 |

本轮没有删除、移动或覆盖任何旧数据。迁移只写入事前确认不存在的 active 目标；源文件复制前后保留，目标完成后做 SHA-256 复核。

## 6. 代码与验证

| Check | Result |
|---|---|
| Local focused tests | `38 passed in 1.24s` |
| SSH active focused tests | `38 passed in 4.58s` |
| Python compilation / diff hygiene | passed；`git diff --check` clean |
| Local real Cora cold smoke | ScoreBundle miss；17/17 Selection Artifact `miss_saved` |
| Local real Cora warm smoke | exact ScoreBundle hit；17/17 Selection Artifact hit；producer sentinel 未触发 |
| Smoke dataset provenance | canonical root match；Cora source fingerprint `d16c609f...`; public split `140/500/1000`; Git dirty 状态显式记录 |
| SSH active branch | `codex/fix-dataset-layout-20260721` at `da3688c3e40b6b2d50f26717ad036b8c041bbde0` |
| SSH unrelated dirty files | 原有 `results/_journal/auto_report.{md,html}` 等仍保留；未暂存、未清理、未覆盖 |

SyncMate runner queue 当前只允许 `smoke`、`opengu-preflight-v1`、`opengu-cache-v2-gate4-v1` 静态 recipe，不能安全调度任意 17-method 命令。本轮不绕过其 allowlist；正式 benchmark 由 exact Git SHA、source fingerprint、dataset fingerprint 和 cold/warm producer sentinel 绑定。SyncMate 可在后续为已注册 recipe 做结果收集，但本次不将其错误地宣称为执行证据。

## 7. 正式 3×3 GPU 矩阵状态

当前 SSH 容器：

- hostname: `autodl-container-cce24cb250-11e2a1b2`；
- `/dev/nvidia*`: 空；
- `torch.cuda.is_available()`: `False`；
- `torch.cuda.device_count()`: `0`；
- 磁盘：`195G` 可用；新 cache/output identity 均不存在。

因此未启动默认 `auto` 模式，避免它静默落到 CPU 并产生没有峰值显存的“伪正式”报告。GPU 重新挂载后，从 SSH active 主目录运行：

```bash
/root/miniconda3/bin/python -m experiments.bc_target_v2.benchmark_selection \
  --device cuda \
  --experiment-git-sha da3688c3e40b6b2d50f26717ad036b8c041bbde0
```

新默认 identity：

- cache: `results/cache_v2/bc_target_v3_1_canonical_public_20260721`；
- cells/manifest: `results/bc_target_v2/selection_benchmark_canonical_20260721`；
- reports: `reports/small_graph_selection_CANONICAL_BENCHMARK_REPORT.{md,html}`。

验收条件仍是 9/9 cells、每格 17 cold selection 时间、一次共享 ScoreBundle cold total、warm exact read、峰值 allocated/reserved VRAM 和明确 failure 状态；cold/warm dataset source 与 Git HEAD 必须逐格一致。

## 8. 待决事项

1. 在 AutoDL 控制台恢复带 GPU 的 `gnn_20` 实例或重新挂载 GPU 后，执行上面的 3×3 矩阵。
2. PubMed 若要进入 OpenGU integrated 80/20 Selection，必须通过冻结 seed/config 的 OpenGU preprocessing 生成新的 canonical pair，并另做 split fingerprint 验收。
3. 任何重复副本清理都需单独批准精确目标。优先候选是 A5 nested canonical processed leaf，其次是迁移完成后的 shared Planetoid；旧实验 checkout 的 method-specific evidence 不应按整个 `data/` 目录粗删。
