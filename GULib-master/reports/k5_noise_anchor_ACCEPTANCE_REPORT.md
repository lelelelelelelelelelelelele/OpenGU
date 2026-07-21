# K5 noise-anchor 独立代码线验收报告

> Date: 2026-07-22  
> Source branch: `codex/wip-k5-noise-anchor-20260721`  
> Registered parent: `main`  
> Audited parent baseline: `main@c26759d51ab0665dff8d78e96a0915aadd0877a2`  
> Scope: 代码/配置、legacy 归档、单元/集成验证、正式运行前置门；本报告不包含可引用的正式 K5 实验结果。

## Verdict

| Gate | Verdict | Evidence |
|---|---|---|
| K5 代码线 | **PASS — 可按 `--no-ff` 合入登记父线 `main`** | K5 逻辑已同步当前 main；定向测试 `17 passed`；Python compile 通过；工作树 clean |
| `method_perf_before` 语义 | **PASS** | GraphEraser/GraphRevoker 生成与 V2 resume 都被约束为 `shard_aggregate_f1` |
| legacy 隔离 | **PASS** | 102/102 JSON 以 `R100` 移到 `results/baseline/k5_random_OLD_20260227/`；canonical `k5_random/` 为空 |
| 旧结果防命中 | **PASS** | 路径隔离 + schema v2 + config/source 校验；旧 102 JSON 中 v2-compatible schema=`0` |
| 正式 K5 执行 | **BLOCKED — 未启动，符合治理要求** | SSH active 非 clean；`/dev/nvidia0` 缺失；未满足 clean main + RTX 4090 + fixed full SHA |

> [!IMPORTANT]
> 本次验收结论是“代码线可以接收”，不是“K5 实验已经完成”。任何正式 gate/MVP 都必须在本线合入后的 SSH clean `main` 上，以一个固定 40 位 SHA 启动。

## 1. 分支历史与真实父线

本地 Git 配置明确记录：

```text
branch.codex/wip-k5-noise-anchor-20260721.openguParent = main
```

历史审计显示，分支最初从较早的 `4de8c75` 开出；随后先合入当时的 `main@b941303`，本次又合入当前审计基线 `main@c26759d`。因此：

- **登记父线和真实接收目标都是 `main`**；
- 最初 fork 点较旧，但不构成另一条 research/release 父线；
- 代码审计时 `main...K5` 计数为 `0 / 7`（本报告提交会再增加 1 个 docs commit），即当前 main 已成为 K5 HEAD 的祖先；
- 接收动作仍必须使用 `git merge --no-ff codex/wip-k5-noise-anchor-20260721`，保留完整 K5 改进边界。

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
- 运行结束再次核对 branch/SHA/dirty，防止矩阵跨 SHA 或运行中污染源码状态。

## 5. 验证

本分支仅运行代码测试和只读/non-formal preflight，没有启动可引用的 GPU 实验。

| Validation | Result |
|---|---|
| `pytest tests/test_baseline_k5_v2.py tests/test_experiment_processed_provider.py -q` | **17 passed** |
| `py_compile`：K5 contract/preflight/generator/runners | **PASS** |
| `git diff --check` | **PASS**（仅 Windows LF→CRLF 提示，无 whitespace error） |
| `git merge-tree --write-tree main K5`（合入当前 main 前） | **PASS / no conflict** |
| 本地 `--preflight-only` non-formal 诊断 | 正确拒绝 K5 branch、缺 canonical pair、RTX 5070 |
| Markdown/HTML 关键结论与数字一致性 | **PASS** |
| 浏览器视觉预览 | **NOT RUN** — in-app browser 的 `file://` URL 策略拒绝本地页；未绕过策略，未伪称目视通过 |

## 6. SSH active 精确 blocker（只读检查）

检查目标：`autodl-opengu:/autodl-fs/data/OpenGU/GULib-master`。

Git 引用在检查时对齐：

```text
main = origin/main = c26759d51ab0665dff8d78e96a0915aadd0877a2
```

但 active checkout 不是 clean：

```text
 M results/_journal/auto_report.html
 M results/_journal/auto_report.md
?? experiments/configs/A6_cora_gin_r0.05_notracin.yaml
?? results/_journal/archive/auto_report_2026-05-06_to_2026-07-10_active4090.md
?? results/_journal/auto_report.events.jsonl
```

此外，`../_backups` 有两个用户备份目录，共 13 个 Git 可见未跟踪文件。这些资产未被覆盖、删除或移动。

GPU gate：

```text
/dev/nvidia0 = missing
```

因此正式 K5 **没有启动**。tracked journal、A6 config、archive/event JSONL 和 backup 资产必须先由用户决定如何接收/归档；GPU 容器也必须重新挂载 RTX 4090。不能为获得 clean 状态而覆盖或删除它们。

## 7. Worktree 清理边界

远端 K5 worktree 在检查时：

- non-ignored untracked=`0`；
- ignored=`56`，全部位于 `.pytest_cache/` 或 `__pycache__/`，分布于 12 个缓存目录；
- 没有 K5 实验结果、配置或用户文档资产。

因此，在 K5 线合入、推送、SSH main 快进同步后，可以删除该 K5 worktree 与临时分支；删除的仅是可再生测试/字节码缓存。A5 detached worktree 与 active 用户资产不属于 K5 清理范围。

## 8. 接收后正式运行条件

只有同时满足以下条件才能执行：

1. K5 线已以 `--no-ff` 进入 `main`；
2. 本地、GitHub、SSH active `main` 指向同一个完整 40 位 SHA；
3. SSH active `git status --short --branch` clean；
4. canonical Cora processed pair preflight 通过且位于 active checkout；
5. GPU 0 是 RTX 4090，且 `torch.cuda.is_available()` 为 true；
6. canonical `results/baseline/k5_random/` 为空，或仅含 source/config 完全匹配的 V2 resume cells。

入口：

```bash
python experiments/baseline_k5/rerun_cora_noise_anchor.py --preflight-only
python experiments/baseline_k5/rerun_cora_noise_anchor.py \
  --expected-git-sha <accepted-main-full-sha>
```

任一 gate 失败都必须停止，不得覆盖 journal/config/backup，不得把旧 K5 JSON 当作 resume，也不得在功能分支上补跑正式 cell。
