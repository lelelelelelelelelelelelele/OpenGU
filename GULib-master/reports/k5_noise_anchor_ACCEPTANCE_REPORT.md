# K5 noise-anchor 独立代码线验收与收口报告

> Date: 2026-07-22<br>
> Source branch: `codex/wip-k5-noise-anchor-20260721`（已合并并清理）<br>
> Registered parent: `main`<br>
> Audited parent baseline: `main@c26759d51ab0665dff8d78e96a0915aadd0877a2`<br>
> Code-line acceptance merge: `b280422cd794df1246df2218ce56215e4d14cdbf`<br>
> Scope: 代码/配置、legacy 归档、单元/集成验证、合并/推送/SSH 同步、正式运行前置门；本报告不包含可引用的正式 K5 实验结果。

## Verdict

| Gate | Verdict | Evidence |
|---|---|---|
| K5 代码线 | **PASS — 已按 `--no-ff` 合入登记父线 `main`** | 接收 merge `b280422`；本地/GitHub/SSH 完成同步；合并后本地与 SSH 均为 `17 passed` |
| `method_perf_before` 语义 | **PASS** | GraphEraser/GraphRevoker 生成与 V2 resume 都被约束为 `shard_aggregate_f1` |
| legacy 隔离 | **PASS** | 102/102 JSON 以 `R100` 移到 `results/baseline/k5_random_OLD_20260227/`；canonical `k5_random/` 为空 |
| 旧结果防命中 | **PASS** | 路径隔离 + schema v2 + config/source 校验；旧 102 JSON 中 v2-compatible schema=`0` |
| 正式 K5 执行 | **BLOCKED — 未启动，符合治理要求** | SSH active 非 clean；`/dev/nvidia0` 缺失；未满足 clean main + RTX 4090 + fixed full SHA |

> [!IMPORTANT]
> 本次收口结论是“代码线已经接收并同步”，不是“K5 实验已经完成”。正式 gate/MVP 仍被 SSH 用户资产与 GPU 状态阻断；只有 SSH `main` clean、RTX 4090 就绪且最终完整 SHA 固定后才能启动。

## 1. 分支历史与真实父线

本地 Git 配置明确记录：

```text
branch.codex/wip-k5-noise-anchor-20260721.openguParent = main
```

历史审计显示，分支最初从较早的 `4de8c75` 开出；随后先合入当时的 `main@b941303`，本次又合入当前审计基线 `main@c26759d`。因此：

- **登记父线和真实接收目标都是 `main`**；
- 最初 fork 点较旧，但不构成另一条 research/release 父线；
- 接收前 `main...K5` 计数为 `0 / 8`，即审计基线 main 已成为最终 K5 HEAD `47e67ec` 的祖先；
- 接收动作已使用 `git merge --no-ff codex/wip-k5-noise-anchor-20260721` 完成：merge `b280422` 的父提交为 `c26759d` 与 `47e67ec`，完整保留 K5 改进边界。

K5 侧关键提交：

| Commit | 作用 |
|---|---|
| `9093df2` | 建立 method-specific K5 noise-anchor WIP |
| `0f6475e` | 引入 V2 schema、失败拒绝和 canonical root |
| `8f47619` | 物理归档 legacy K5 evidence |
| `f7f42b4` | 把 V2 resume 绑定到 method-native before source |
| `968e40f` | 增加 formal preflight、canonical processed provenance 和 GPU/Git gate |

## 2. `method_perf_before` 是否必然来自 shard/SISA ensemble

结论：**对 GraphEraser 和 GraphRevoker，是。** 该结论同时覆盖“新生成”和“断点复用”。

生成链如下：

1. `generate_baseline.py` 使用独立的 `before_pipeline` 调用 `measure_method_perf_before(...)`；before 测量与实际随机删除运行不共享 pipeline 状态。
2. `measure_method_perf_before(...)` 先调用 `_ensure_base_model_trained()`。
3. shard 方法的 `train_only` 路径执行 `Shard_based_pipeline.run_exp → exp_partition → exp_train → aggregate_shard_model`，跳过 unlearning。
4. GraphEraser 的 `aggregate(...)` 用所有 shard posterior 的 Aggregator 计算并写入 `self.aggregate_f1_score`。
5. GraphRevoker 的 `aggregate(...)` 同样生成所有 shard posterior，再由 mean/optimal/majority/contrastive aggregator 写入 `self.aggregate_f1_score`。
6. K5 合同对两种方法只读取 `pipeline.method.aggregate_f1_score`，不会调用单一 `model_zoo.model` 的普通评估。

V2 复用侧新增了第二道门：

```text
GraphEraser / GraphRevoker
  before_metric        = method_train_only_f1
  before_metric_source = shard_aggregate_f1
```

`load_valid_record(...)` 会把该 source 纳入 expected config。即便文件自称 schema v2，只要把 shard 方法标成 `trained_model_test_f1`，也会被判 stale/incompatible，不能 resume。

## 3. 旧 102 个 JSON 为什么不会被新运行命中

### 3.1 物理路径已经分离

审计计数：

| 项目 | 数量 |
|---|---:|
| `_OLD` 下 tracked JSON | 102 |
| `_OLD` 下物理 JSON | 102 |
| commit `8f47619` 的 `R100` JSON rename | 102 |
| canonical `k5_random/` tracked JSON | 0 |
| canonical `k5_random/` 物理 JSON | 0 |

旧证据位于：

```text
results/baseline/k5_random_OLD_20260227/
```

新运行只在以下 canonical root 查找/写入：

```text
results/baseline/k5_random/
```

这不是通过改一个临时输出根绕开旧文件；102 个 tracked 文件本身已从旧 canonical 路径移动到同一源目录下带日期的明确 `_OLD` 归档。

### 3.2 schema 和 config 双重拒绝

102 个 legacy JSON 的解析审计结果：

| 类型 | 数量 |
|---|---:|
| per-seed | 82 |
| averaged | 16 |
| batch summary | 4 |
| parse error | 0 |
| 缺少 V2 schema | 102 |
| v2-compatible schema | 0 |

即使把旧文件错误复制回 canonical 同名位置，`load_valid_record(...)` 也会因缺少 `schema=opengu.k5_noise_anchor` / `schema_version=2` 拒绝；不会覆盖，也不会当作成功 resume。

### 3.3 legacy archive 显式禁写

`validate_output_root(...)` 现在拒绝 `_OLD` 根及其任何子目录。这样即使显式传入 `--output_root .../k5_random_OLD_20260227`，也不能在旧归档里补出新的 V2 文件，避免混合时代证据。

## 4. Formal-lane 收紧

新增 `experiments/baseline_k5/formal_preflight.py`，并把 `rerun_cora_noise_anchor.py` 变为 fail-closed formal entrypoint：

- `--preflight-only` 只读报告 readiness，不创建结果、不启动 GPU 工作；
- 实际运行必须显式传入 `--expected-git-sha <40-char SHA>`；
- branch 必须是 `main`；
- Git 必须 clean，错误信息携带精确 dirty path；
- GPU 0 必须由 `nvidia-smi` 和 PyTorch 同时识别为 RTX 4090；
- `root_path` 固定为 active checkout；
- `processed_root` 固定为 active `data/processed`；
- canonical processed data/dataset pair 必须在计时前完整存在；
- preflight 记录 requested path、real path、size、SHA-256、split counts、split-index SHA-256、source fingerprint 和 Git/GPU provenance；
- 正式矩阵注册唯一 1-cell gate：`Cora/GCN/GraphRevoker/seed111/k=5`，优先覆盖 shard/SISA aggregate-before 与 GraphRevoker partition 路径；
- `--gate-only` 只运行该 cell；gate manifest 绑定完整 main SHA、canonical dataset fingerprint、cell identity 与 artifact SHA-256；
- 全矩阵入口必须显式 `--resume`，并先验证同 SHA 的 gate manifest 与 V2 artifact；无 gate、被篡改 gate 或直接全跑都会 fail closed；
- 运行结束再次核对 branch/SHA/dirty，防止矩阵跨 SHA 或运行中污染源码状态。

## 5. 验证

K5 功能分支、合并后的本地 main 与同步后的 SSH main 仅运行代码测试和只读/non-formal preflight，没有启动可引用的 GPU 实验。

| Validation | Result |
|---|---|
| `pytest tests/test_baseline_k5_v2.py tests/test_experiment_processed_provider.py -q` | 原 K5 接收为 **17 passed**；补入 gate→同 SHA resume 合同后为 **21 passed** |
| `py_compile`：K5 contract/preflight/generator/runners | **PASS**（本地与 SSH） |
| `git diff --check` | **PASS**（无 whitespace error） |
| `git merge-tree --write-tree main K5`（接收前） | **PASS / no conflict** |
| `--no-ff` 接收 merge | **PASS** — `b280422`，parents=`c26759d 47e67ec` |
| 本地 `--preflight-only` non-formal 诊断 | 正确拒绝 K5 branch、缺 canonical pair、RTX 5070 |
| SSH `--preflight-only` non-formal 诊断 | 正确验证 canonical Cora pair，并拒绝 dirty active 与不可用 GPU |
| Markdown/HTML 关键结论与数字一致性 | **PASS** |
| 浏览器视觉预览 | **NOT RUN** — in-app browser 的 `file://` URL 策略拒绝本地页；未绕过策略，未伪称目视通过 |

## 6. SSH active 精确 blocker（只读检查）

检查目标：`autodl-opengu:/autodl-fs/data/OpenGU/GULib-master`。

代码接收并快进同步后，Git 引用对齐：

```text
local main = GitHub origin/main = SSH main = SSH origin/main
= b280422cd794df1246df2218ce56215e4d14cdbf
```

SSH `--preflight-only` 验证 canonical Cora processed pair 位于 active checkout，未使用下载或运行时预处理：

| Evidence | Value |
|---|---|
| data pickle | `15850381` bytes；SHA-256 `e8919e1850b4a9682a384d93dd2f8cf3733190d565ee9287843af1cd82b5432f` |
| dataset pickle | `15723324` bytes；SHA-256 `1dcbb6be57c174bcad6fe8186ec5eadfeb01196dd7ee33772e697aa5057ad6e4` |
| split | train=`2166`，val=`0`，test=`542`，nodes=`2708`，directed edges=`10556` |
| source fingerprint | `fe93535af1f59cb967ed7ec14b25fd02c87e207ea51c028b72456203be519ba6` |

但 active checkout 仍不是 clean：

```text
 M results/_journal/auto_report.html
 M results/_journal/auto_report.md
?? %ln                                      # 0-byte file
?? experiments/configs/A6_cora_gin_r0.05_notracin.yaml
?? results/_journal/archive/auto_report_2026-05-06_to_2026-07-10_active4090.md
?? results/_journal/auto_report.events.jsonl
```

此外，`../_backups` 的两个用户备份目录共有 13 个 Git 可见未跟踪文件。上述 journal、config、archive/event、`%ln` 与 backup 资产均未被覆盖、删除或移动。

GPU gate 同时失败：

```text
/dev/nvidia0 = missing
nvidia-smi = OSError: [Errno 8] Exec format error
```

因此正式 K5 **没有启动**。这些用户资产必须先由用户决定如何接收/归档，GPU 容器也必须重新挂载 RTX 4090；不能为获得 clean 状态而覆盖或删除它们。

## 7. Worktree 清理边界

K5 临时线已在资产盘点后完成清理：

| Location | Non-ignored | Ignored inventory | Action |
|---|---:|---|---|
| local K5 worktree | 0 | 64 个 `.pytest_cache` / `__pycache__` 文件 | worktree 与空父目录已删除 |
| SSH K5 worktree | 0 | 56 个 `.pytest_cache` / `__pycache__` 文件 | worktree 已删除 |
| local/GitHub/SSH K5 branch refs | — | 已被 `main` 包含 | 精确删除，不做 broad prune |

删除的 120 个文件全部是可再生测试/字节码缓存，没有 K5 实验结果、配置或用户文档资产。

以下 worktree 因不属于 K5 或含 ignored 用户资产而保留：本地 `main-tracin-sup-merge` 现承载 `main` 且含历史 result/cache；本地 `syncmate-small-selection` 含 `.syncmate/device.yaml` 与 `remote_status_gpu4090.json`；SSH A5 detached worktree 不属于本线；主工作区的 `codex/docs-grandfather-selection-20260722` 是无关活动分支。其中的 ignored/用户资产均未被覆盖、移动或删除；无关分支没有被切换或改写。

## 8. 接收后正式运行条件

K5 代码接收和 canonical dataset 两项已经通过；正式执行仍须同时满足以下条件：

1. `b280422` 是最终 `main` 的祖先，且本地、GitHub、SSH active `main` 指向同一个最终完整 40 位 SHA；
2. SSH active `git status --short --branch` clean；
3. canonical Cora processed pair 在实际启动前再次 preflight 通过且位于 active checkout；
4. GPU 0 是 RTX 4090，且 `torch.cuda.is_available()` 为 true；
5. 注册的 `GraphRevoker/GCN/seed111/k=5` gate 先通过，manifest 与 artifact 绑定同一 SHA/dataset fingerprint；
6. canonical `results/baseline/k5_random/` 在 gate 前为空，扩展时仅含 gate 及 source/config 完全匹配的 V2 resume cells。

入口：

```bash
python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --preflight-only \
  --expected-git-sha <accepted-main-full-sha>

python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --gate-only \
  --expected-git-sha <accepted-main-full-sha>

python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --resume \
  --expected-git-sha <the-same-accepted-main-full-sha>
```

任一 gate 失败都必须停止，不得覆盖 journal/config/backup，不得把旧 K5 JSON 当作 resume，也不得在功能分支上补跑正式 cell。该顺序已经由 runner 强制执行，不再依赖操作者或对话记忆。
