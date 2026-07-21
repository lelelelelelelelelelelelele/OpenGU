# 小图 Selection Dataset 布局审计与迁移报告

> **Verdict: PASS WITH GRANDFATHERED GT EXCEPTION** — SSH active 主目录的数据路径、代码解析与 provenance 合同已经收口；既有 public `3 datasets × 3 seeds` GPU cold/warm 矩阵经数据内容与 scorer 语义核验后作为一次性权威 GT 接受，无需重跑。OpenGU canonical processed 的 PubMed pair 仍缺失，但不影响 public benchmark 的本次验收。

## 1. 结论

- SSH 登录与正式 active checkout 根目录均为 `/autodl-fs/data/OpenGU/GULib-master`。
- public 17-method benchmark 的唯一默认根已定为 `/autodl-fs/data/OpenGU/GULib-master/data/raw`，数据目录为 lowercase `cora`、`citeseer`、`pubmed`。
- OpenGU integrated Selection 的 canonical 输入仍是 `/autodl-fs/data/OpenGU/GULib-master/data/processed/{transductive,inductive}/*.pkl`。它与 public Planetoid 固定 split 是两条不同数据通道。
- 既有 benchmark 实际使用 `/autodl-fs/data/OpenGU-shared/Planetoid` 和隔离 worktree；其 `9/9` 经一次性 grandfathered GT 例外接受为 **public-split 17-output benchmark 权威结果**。它仍不得改称 active-root 运行或 OpenGU 80/20 实验；对应数据副本已在逐文件等同性验证后删除。
- 三套 public PyG cache 已从共享副本复制到 active 主目录并逐文件 SHA-256 验证；历史 shared/worktree/experiment source copies 已按用户明确授权清理。
- accepted CiteSeer canonical processed pair 已回填 active；Cora pair 原本已在 active 且与历史副本相同；PubMed pair 未在受检历史目录中找到，因此未用 public `data.pt` 冒充。
- 代码提交 `da3688c3e40b6b2d50f26717ad036b8c041bbde0` 将 B/C selection、benchmark、matrix 与 downstream 改成 repo-relative、fail-closed、path-aware + content-aware provenance；`51f19460b51a048e33e840a99e35826f5b7af2b4` 将 C-target 及正式/诊断 TracIn gate 收口到同一合同。
- 根 `AGENTS.md` 与 `CLAUDE.md` 已将 active `data/raw` / `data/processed` 合同、外部副本禁用、正式运行禁下载和 provenance preflight 固化为 SSH agent 强制规则。
- 清理后的目录级复扫显示，SSH shared/worktree/experiment roots 中有内容的 `data/raw`、`data/processed/transductive`、`data/processed/inductive` 数量均为 `0`；source dataset 只保留在 active 主目录。

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

## 5. 重复副本清理

| 精确范围 | 删除文件 | 删除字节 | 删除前证据 | 状态 |
|---|---:|---:|---|---|
| SSH shared Planetoid root | 33 | 116,595,446 | 三套 public cache 的 9 个有效输入逐文件 SHA-256 等于 active | 已删除 |
| SSH TracIn G4 Planetoid root | 11 | 16,297,508 | Cora raw 与 `data.pt` 等于 active；PyG 空元数据不参与数据身份 | 已删除 |
| SSH accepted E1 raw CiteSeer | 11 | 50,501,924 | 11/11 文件与 active 相同 | 已删除 |
| SSH E1 / GraphRevoker / E4 / A5 / A5 nested canonical pickle copies | 10 | 360,257,462 | 十个 pickle 分别与 active Cora/CiteSeer counterpart byte-identical | 已删除 |
| 本地 `data/raw/Planetoid` | 33 | 116,595,446 | CiteSeer/PubMed 六类张量完全相同；Cora 特征、标签、mask 及有向边多重集合相同，仅边列顺序/序列化不同 | 已删除 |

SSH 共删除 `65` 个文件、`543,652,340` bytes；本地另删除 `33` 个文件、`116,595,446` bytes。删除前旧路径 executable reference 为 `0`、运行中进程引用为 `0`，所有目标均为非 symlink 的精确绝对路径。删除后再次扫描，外部 populated source roots 为 `0`；active `data/raw` 保留 `49` 个文件，active `data/processed/transductive` 保留 `6` 个文件。历史实验结果、method-specific artifacts 和 unrelated dirty files 均未删除。

## 6. 代码与验证

| Check | Result |
|---|---|
| Local focused tests | `52 passed in 0.58s` |
| SSH active focused tests | `52 passed in 1.45s` |
| Python compilation / diff hygiene | passed；`git diff --check` clean |
| Local real Cora cold smoke | ScoreBundle miss；17/17 Selection Artifact `miss_saved` |
| Local real Cora warm smoke | exact ScoreBundle hit；17/17 Selection Artifact hit；producer sentinel 未触发 |
| Smoke dataset provenance | canonical root match；Cora source fingerprint `d16c609f...`; public split `140/500/1000`; Git dirty 状态显式记录 |
| SSH active branch | caller cleanup 基线为 `codex/fix-dataset-layout-20260721` at `51f19460b51a048e33e840a99e35826f5b7af2b4`；规则/报告提交可推进 HEAD，正式运行必须重新读取并冻结当时的 exact HEAD |
| Post-delete source scan | external populated source roots `0`；Cora/CiteSeer/PubMed 从 active lowercase raw path 加载并通过 fixed-split validation |
| SSH unrelated dirty files | 原有 `results/_journal/auto_report.{md,html}` 等仍保留；未暂存、未清理、未覆盖 |
| Scorer semantic diff | `9240b9a` 与 accepted main 的 ScoreBundle `produce()` 块逐字一致；B/C core 与 C-target core Git blob 均未变化 |
| Grandfathered GT scope | 接受 v3.0 result payload、17-output ranking、cold/warm 与 GPU telemetry；不接受旧 cache 作为 v3.1 exact hit，不扩展到 OpenGU 80/20 或 GU outcome |

SyncMate 当前已注册 staged small-selection recipes，包括 `opengu-small-selection-full-v1`；它适用于未来 active-root 新运行的调度、收集与验真。历史 `9240b9a` 矩阵不是由该 recipe 执行，本次 GT 接受依据是逐文件 dataset 等同性、scorer 语义未变和已完成的 cold/warm/GPU gate，不倒填 SyncMate 执行声明。

## 7. Grandfathered 3×3 GT 验收

现有 SSH GPU 矩阵在 `9240b9a` 上完成：

- Cora/CiteSeer/PubMed × seeds 42/212/2024 = `9/9` cells；
- `153/153` 方法级 cold Selection miss→warm exact hit；
- 0 failures；cold ScoreBundle mean/max `6.8038/9.1624 s`；warm read `0.3200/0.9635 s`；
- 峰值 allocated/reserved `357/384 MiB`；
- 机器证据保留在 `results/bc_target_v2/selection_benchmark_20260721/`，双格式结论见 `reports/small_graph_selection_BENCHMARK_REPORT.{md,html}`。

### 7.1 为什么不重跑

1. **数据内容不变。** shared 三套 public cache 的 9 个有效输入在删除前逐文件 SHA-256 等于 active；2026-07-22 从 SSH active 只读重算得到同一组已记录 source fingerprint 与 `processed/data.pt` SHA-256。
2. **score/ranking 语义不变。** `9240b9a` 之后没有修改 ScoreBundle `produce()`、B/C core 或 C-target core；v3.1 只把 dataset source/Git provenance 加入 fail-closed 身份，并增加 SyncMate 调度。
3. **目标证据已经齐全。** 原矩阵已同时记录每方法 cold selection、共享 ScoreBundle total、warm exact read、GPU 峰值和失败状态。重新执行只会得到新的 Recipe/Artifact ID，不会补充本验收缺失项。

因此本轮采用明确的一次性例外：以服务器 v3.0 results 作为该 public benchmark 的 GT/analysis authority，并退休本机旧重复/legacy 运行。v3.0 与 v3.1 Artifact 身份继续严格分离；未来任何新增 dataset、seed、算法版本或结果内容都必须从 active canonical root 按新合同运行。

## 8. 待决事项

1. PubMed 若要进入 OpenGU integrated 80/20 Selection，必须通过冻结 seed/config 的 OpenGU preprocessing 生成新的 canonical pair，并另做 split fingerprint 验收。
2. 后续新增或恢复 dataset 必须先写入 active `data/raw` 或经 accepted preprocessing 写入 active `data/processed/{transductive,inductive}`；不得在 shared/worktree/experiment root 新建 authoritative source copy。method-specific evidence 仍按现有 artifact 规则保留。
