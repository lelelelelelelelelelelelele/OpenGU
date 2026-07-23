# SSH 部署根目录摸排与收口报告

> **Verdict: PASS** — 2026-07-24 已将 `/autodl-fs/data` 从九个 OpenGU 同级目录收口为单一 `OpenGU` 部署根；平台目录 `.sys` 与平台文件 `.gitignore` 保留。6952 个证据文件逐文件 SHA-256 校验通过，历史内容未丢失，未来运行路径已增加 active-checkout fail-closed 边界。

## 1. 最终状态

收口后的 `/autodl-fs/data` 顶层只有：

```text
.gitignore
.sys/
OpenGU/
```

证据统一迁入：

```text
/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/
```

该目录匹配仓库现有 `results/_archive_*/` 忽略规则，不改变 SSH active checkout 的 Git 状态，也不属于 canonical dataset 或正式运行输入。

| 验收项 | 结果 |
|---|---:|
| 收口前 OpenGU 同级业务目录 | 9 |
| 删除的空目录 | 2 |
| 迁入 active checkout 的证据树 | 7 |
| 迁移文件 | 6952 |
| 迁移目录 | 1961 |
| 迁移源内容字节 | 1,078,876,926 |
| 归档总字节（含清单和验证日志） | 1,080,852,444 |
| 文件 SHA-256 验证 | 6952/6952 PASS |
| symlink | 0 |
| live process / cwd / fd 引用 | 0 |
| 独立 mount | 0 |
| SSH active Git dirty entries | 0 |

全量清单锚点：

```text
32961210ff7a874b7f13f75987be19f5d825002e9f453bb5ac015976e048882e
```

该值是归档内 `SHA256SUMS` 文件本身的 SHA-256。逐文件复核记录位于归档内 `VERIFY_SHA256.log`。

## 2. 为什么会出现这些目录

结论不是“系统自动生成垃圾”，而是 2026-07-14 至 2026-07-22 的多轮验收把实验隔离错误地实现成了部署根同级扩散，并且缺少统一的退出/归档步骤。

| 根目录 | 直接来源 | 根因分类 |
|---|---|---|
| `opengu-experiments` | Cache V2、Citeseer E1、GraphRevoker 的 fresh clone；E4 queue 日志明确把 `WORKTREE` 指向该根 | 把短期代码隔离实现成永久 sibling clone |
| `opengu-experiment-evidence` | 多份 2026-07-14 验收报告明确指定独立 evidence root | 把证据归档放在部署边界外 |
| `opengu-experiment-ops` | E4/A5 queue shell、PID、日志和临时 YAML | ad-hoc 运维文件没有回收入口 |
| `cache-v2-canary` | Citeseer Cache V2 gate/recheck 的 run、dataset、store、evidence | canary 输出根写在 active checkout 外 |
| `cache-v2-materializer` | IM/simple producer 的独立 ArtifactStore 与失败对照 | materializer store 写在 active checkout 外 |
| `OpenGU-cache-v2-rollout` | `4634504` 引入 Gate4；YAML 和 `scripts/cache_v2_gate4_canary.py` 直接写死该路径 | tracked 配置硬编码 sibling root |
| `OpenGU-small-selection-gu` | `218f642` 起的 GU gate/full v1–v5；v5 Python 与 YAML 直接写死该路径 | tracked 配置硬编码 sibling root |
| `OpenGU-shared` | dataset 副本清理后留下 | 空壳未回收 |
| `OpenGU-worktrees` | rollout/worktree 清理后留下 | 空壳未回收 |

三个系统性原因：

1. **把“隔离”与“部署目录”混为一谈。** fresh clone、canary store、queue ops 和 evidence 都直接落到 `/autodl-fs/data`。
2. **缺少 active-checkout 输出边界。** runner 能解析任意绝对 `runtime_root`、`store_root`、`manifest_path`，因此 tracked YAML 可以持续重建 sibling。
3. **此前 Git 收口范围不完整。** branch/worktree 已收口，但没有把 filesystem deployment root 纳入最终验收。

## 3. 证据保全与迁移

迁移前逐个确认：

- 九个源路径均为 `/autodl-fs/data` 的直接子目录、非 symlink，`readlink -f` 与预期绝对路径相同。
- `OpenGU-shared` 与 `OpenGU-worktrees` 完全为空。
- 其余七个目录无进程参数、cwd、打开 fd 或独立 mount 引用。
- `opengu-experiments` 中四个完整 clone 的代码提交均已进入当前 `main`，但实验 data/results/logs 与两个 dirty `auto_report.md` 并非 active checkout 的逐文件冗余副本。
- evidence、canary、materializer 与 small-selection 树被历史验收报告引用，不能按“旧目录”直接删除。

因此采用同文件系统原子迁移，而不是删除或留下兼容 symlink：

```text
<old sibling>/
  -> OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/<old sibling>/
```

归档内保留：

| 文件 | 用途 |
|---|---|
| `INVENTORY.tsv` | 迁移前每个根的文件数、目录数、字节数与基线 Git SHA |
| `POST_MOVE_INVENTORY.tsv` | 迁移后同口径对账 |
| `SHA256SUMS` | 6952 个文件的相对路径与 SHA-256 |
| `SHA256SUMS.sha256` | 全量清单锚点 |
| `SYMLINKS.tsv` | symlink 清单；本次为空 |
| `VERIFY_SHA256.log` | 迁移后逐文件校验结果 |

历史报告中的旧绝对路径不回写，因为它们记录的是当时的执行事实。本报告是统一 relocation authority。

## 4. 防复发改动

### 4.1 Runner fail closed

新增 `experiments/path_policy.py`。当代码实际运行于：

```text
/autodl-fs/data/OpenGU/GULib-master
```

`processed_root`、`runtime_root`、`run_root`、Cache V2 `store_root`、`legacy_results_root` 和 `manifest_path` 必须全部解析到 active checkout 内；任何 sibling 或 `/tmp` 输出会在创建目录之前失败。

这使仍保留为历史身份的 v1–v4 绝对路径配置无法在 active SSH checkout 上重新扩散目录。

### 4.2 仍可能使用的配置改为 repo-relative

- Cache V2 Gate4：runtime/evidence 写入 `results/runs/`，store 写入 `results/cache_v2/`。
- small-selection GU gate v5：runtime/evidence/manifest 写入 `results/runs/`，store 写入 `results/cache_v2/`。
- small-selection GU full v5：evidence 写入 `results/runs/`。
- canonical processed root 统一写成 `data/processed`，由 checkout 解析。

这些改动形成新的配置 fingerprint；不会冒充 2026-07-17/22 的历史执行身份。

### 4.3 顶层布局验收

新增只读检查：

```bash
python scripts/validate_ssh_deployment_layout.py --base /autodl-fs/data
```

默认只允许 `.gitignore`、`.sys` 和 `OpenGU`；发现任何其他顶层条目即返回非零。

## 5. 验证

| Check | Result |
|---|---|
| 迁移前精确路径与类型检查 | PASS |
| 迁移前 process/cwd/fd/mount 检查 | PASS，0 引用 |
| 迁移前后 root 级 files/dirs/bytes diff | PASS，无差异 |
| 迁移后逐文件 SHA-256 | PASS，6952/6952 |
| 顶层精确扫描 | PASS，仅 `.gitignore`、`.sys`、`OpenGU` |
| SSH active Git status | PASS，clean `main` |
| path policy / layout validator / Gate4 contract tests | PASS，11 passed |
| GU v5 / Cache V2 / runner 相邻回归 | PASS，22 passed（另 217 deselected） |
| Python compilation | PASS |

YAML 变更还执行了 canonical `--dry_run`。本机不是 formal data lane，因此分类如下；这些是预检结果，不是正式实验结果：

| Config | Dry-run classification |
|---|---|
| `cache_v2_gate4_cora_degree_canary.yaml` | 在创建任何输出前 fail closed：本机 worktree 缺少 canonical processed Cora pickle |
| `syncmate_small_selection_gu_gate_v5.yaml` | 在创建任何输出前 fail closed：新的 repo-local external Selection manifest 尚未由 accepted staging step 生成 |
| `syncmate_small_selection_gu_full_v5.yaml` | 该文件是 `syncmate_stage.py` 的阶段编排配置，不是 `experiments/run.py` 单矩阵 schema；专属 `_config()`/17-cell contract tests 已通过 |

迁移动作执行时的 SSH active 基线为：

```text
ea4f34a29f5211079e1f7a7caf5a4c296f14ff08
```

## 6. 已知边界

- 本次没有删除历史实验内容；约 1.08 GB 被保留在 active checkout 的 ignored archive 中。
- 归档不是 formal dataset、cache authority 或可恢复运行根。需要引用旧证据时，应先查本报告和归档清单。
- SSH 当前仍无 GPU device、默认 Python/conda 与预期 `gnn_20`；本次是文件/Git 治理，不构成 formal GPU 实验验收。
- 并行的本机 NeurIPS review 与 target-scope 工作树未被切换、暂存、合并或清理。
