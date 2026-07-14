# OpenGU Git 全面一致性审计与安全对齐报告

> 审计冻结时间：2026-07-14 17:30 CST 左右
> Git root：`E:/project/OpenGU`
> 项目目录：`E:/project/OpenGU/GULib-master`
> 源码基线：`d38df1430a3259b332700571c85350a0ef166568`
> 本文件是源码基线之后的审计文档；发布它不会改变 Cache、GraphRevoker 或 TracIn 源码。

## 1. 结论

**结论：主工作线已经一致；不应为了“表面全同”去移动实验快照或清理用户数据。**

- local current、GitHub feature、SSH active、primary SSH isolated 的源码均为 `d38df143`。
- local `main` 与 GitHub `main` 均为 `3f631fb`，是 feature 的直接祖先；冻结时 feature 比 main 多 23 个提交，main 没有反向独有提交。
- 本地 3 个 worktree 没有遗失的未提交源码。AutoReport V3 worktree 只有 3 个未跟踪 planning 文件，属于正在进行的另一 session。
- 发现 3 个没有出现在任何 origin ref 的历史本地提交，但它们分别是旧 4090 backup、结果清理脚本、重投稿 paper framing；都不应在本轮自动 push/merge。
- SSH active 的 journal、A6 YAML、Cache V2 SQLite、`../_backups` 全部保留。没有执行 stash、checkout、clean、reset、GC、prune 或结果清理。
- 其余 7 个 SSH checkout 中，6 个是按被测 SHA 固定的可复现实验快照，1 个是旧 dirty `nips-prep` checkout；它们都在 `d38df143` 的祖先链上，不是新的未 push 源码。
- 本轮唯一 Git 对齐写操作是本地无 prune 的 `git fetch origin --tags`。`main` 合并仍是显式审批门。

## 2. 五个目标面的冻结状态

| 目标面 | Branch / ref | HEAD | Dirty | 未合并 / 未发布工作 |
|---|---|---|---|---|
| Local current | `codex/citeseer-e1-graphrevoker-20260714` | `d38df143` | tracked + 普通 untracked clean；仅有 ignored 本地状态 | 相对 `origin/main` 多 23 个线性提交 |
| Local main | `main` | `3f631fb` | 未 checkout，dirty 不适用 | 比 feature 少 23 个提交；与 `origin/main` 完全一致 |
| GitHub origin | `main` / feature | `3f631fb` / `d38df143` | 不适用 | feature 尚未进入 main；其他历史 origin branches 仍独立存在 |
| SSH active | `codex/citeseer-e1-graphrevoker-20260714` | `d38df143` | journal modified；A6 与 `_backups` untracked；SQLite ignored | backup branch `39d284d` 本地保留；3 个保护 stash |
| SSH primary isolated | `codex/citeseer-e1-graphrevoker-20260714` | `d38df143` | 普通 dirty clean；只有 ignored test/cache 状态 | 无未 push commit |

Primary isolated 路径：`/autodl-fs/data/opengu-experiments/cache-v2-simple-f1fcd2c`。

## 3. Local / origin 审计

### 3.1 Worktrees

| Worktree | 状态 | 结论 |
|---|---|---|
| `E:/project/OpenGU` | feature `d38df143`，clean | 当前主工作树，与 origin feature 一致 |
| `C:/Users/ADMIN/.codex/worktrees/92ea/OpenGU` | `codex/autoreport-v3-20260714@d38df143`；3 个未跟踪 planning Markdown | 活跃 AutoReport V3 session；不删除、不代提交 |
| `C:/Users/ADMIN/.codex/worktrees/ab43/OpenGU` | detached `d38df143`，clean | 无遗留 dirty；保持 detached，避免干扰未知 session |

### 3.2 Feature stack

`main@3f631fb` 是 feature 的 merge-base；`main...feature = 0 / 23`。现有 23 个提交已经按语义组织，不建议 rewrite/squash：

1. Git history + Cache V2.1 contract / architecture / ignore / dashboard / IF taxonomy；
2. Selection Artifact store Gate 1 与 Citeseer V2 canary；
3. Citeseer E1、GraphRevoker canary 及成对 MD/HTML 验收；
4. Selection materializer、simple producers、tie stabilization 与 SSH acceptance。

相对 main 共 51 个文件，18,939 insertions / 39 deletions。新增内容主要位于 `cache_v2/`、`docs/`、`report/`、配置、测试和文档地图；没有 results/cache/runs payload 进入该栈。

### 3.3 未出现在任何 origin ref 的本地提交

| Commit | Branch | 类型 | 本轮决策 |
|---|---|---|---|
| `39d284d` | `backup/4090-phase-b-fixes-39d284d` | IM / IF pipeline + 运维脚本的旧 4090 恢复点 | 保留，不 push；本轮不做算法改动 |
| `92a28b6` | `bug/perf-unlearn-collateral-collision` | `cleanup_if_family_collateral.py` | 保留，不 push；本轮禁止清理实验结果 |
| `565aaf6` | `paper/alignment-experiment` | paper framing + FIG-5 PDF | 保留，不 push；它是重投稿候选线 |

本地另有 3 个 2026-04/05 stash，分别保存 paper WIP、本地设置与旧报告/文档 WIP；全部保留。

### 3.4 Codex refs 与不可达对象

- 最新 Codex tree snapshot 与 `d38df143` 的 commit tree 完全相同。
- 较早 snapshot-only 文件只有 5 个 Obsidian UI 配置和 2 个未引用 `@2x.png`，当前都被精确 ignore。
- `git fsck --no-reflogs --unreachable` 找到 51 个 commit：31 个 stash 内部对象、15 个旧 standalone/rewrite、5 个 2026-07-14 临时提交/回滚。
- 7 月 14 日两项 canary patch 已进入 feature；临时 `A5_*_clean*.yaml` 已显式 revert 并被 stable 配置替代。
- 未运行 `git gc`、reflog expire 或内部 ref 清理。

## 4. 产物分层与 Git 安全

本地主工作树 ignored 文件共 8,862 个、约 10.02 GB：

| 类别 | 文件数 | 大小 | Git 决策 |
|---|---:|---:|---|
| 实验数据 / cache / logs | 7,973 | 约 9.89 GB | 永不 broad add；保留在工作树 |
| paper / report build | 132 | 约 79.7 MB | 仅提交明确的源文档/最终静态报告，不提交构建垃圾 |
| 依赖 | 353 | 约 7.0 MB | 不提交 |
| session planning | 65 | 约 1.2 MB | 不提交 |
| compiled Python | 284 | 约 4.0 MB | 不提交 |

排除生成区后，没有发现被 ignore 的新算法 Python、shell 或 YAML 源码。`results/cache_v2/index.sqlite` 和 `results/runs/` 均已被精确 ignore。

## 5. SSH active 保护证据

路径：`/autodl-fs/data/OpenGU/GULib-master`。

| 保护对象 | Git 状态 | 大小 | SHA-256 |
|---|---|---:|---|
| `results/_journal/auto_report.md` | tracked modified | 980,451 B | `0273a88a0d56952c232fc1b5165ad5bbab66a1940ba6ceae01def784fa817d3b` |
| `experiments/configs/A6_cora_gin_r0.05_notracin.yaml` | untracked | 433 B | `5f7c4186f1e89c748a47f6064a489ffbdb4d4308a70a528911d7c28eccba7edf` |
| `results/cache_v2/index.sqlite` | ignored | 11,177,984 B | `1260d2f287fdcc73dffa6158b4f3240724783a2622061bc4ce90472e68f3c86e` |
| `../_backups` | repo-wide untracked | 约 249 KB | 目录；未做聚合 hash，逐文件保持原状 |

`../_backups` 当前包含 GraphRevoker degree/seed42 probe 的 cell、manifest、ResultCache 与 SelectionCache 备份。SSH active 另有 3 个 preservation stash，内容均为 A6 YAML + journal 快照。全部未动。

SSH active 的 ignored code-like 筛查只有 `.pytest_cache/README.md` 与本地 `AGENTS.md`，没有隐藏的新算法源码。审计时没有相关 live runner，但这不构成清理授权。

## 6. SSH 全部 checkout

| Checkout | HEAD | 相对 `d38df143` | Dirty / data | 决策 |
|---|---|---:|---|---|
| `/autodl-fs/data/OpenGU` | feature `d38df143` | 0 behind | 保护 dirty；results 约 628 MB | active，保持 dirty |
| `.../citeseer-e1-aad4e99` | feature `aad4e99` | 9 behind | journal modified；results 约 14 MB | E1 可复现快照，保持 pin |
| `.../graphrevoker-cora-aad4e99` | detached `93095d9` | 7 behind | journal modified；results 约 2.9 MB | GraphRevoker 可复现快照，保持 pin |
| `.../cache-v2-im-b10f672-bundle` | feature `b10f672` | 4 behind | 普通 clean | IM materializer 快照，保持 pin |
| `.../cache-v2-simple-f1fcd2c` | feature `d38df143` | 0 behind | 普通 clean | primary isolated，已对齐 |
| `/tmp/opengu-cache-v2-gate1-9b90ad4` | recovery `9b90ad4` | 15 behind | 普通 clean | Gate 1 快照，保持 pin |
| `/tmp/opengu-citeseer-v2-canary-83842e6` | canary `83842e6` | 11 behind | 普通 clean | Citeseer V2 快照，保持 pin |
| `/tmp/autodl-fs/OpenGU` | `nips-prep@073457f` | 133 behind | journal + PID/log dirty；results 约 223 MB | 旧实验 checkout，禁止 clean/pull/prune |

所有这些 HEAD 都是 `d38df143` 的祖先。GraphRevoker clone 的 `origin` 是本地 Citeseer clone，因此它显示“2 commits not on local origin refs”，但这两个提交已在 GitHub feature 中，不是未 push 工作。

SSH active 的 remote-tracking refs 还残留 GitHub 已删除的旧 branches。它们只是 stale refs；`git remote prune origin` 会删除本地恢复线索，本轮不执行。

## 7. 建议的 commit / branch / merge 顺序

1. **保持现有 feature stack 不改写。** 23 个提交已经语义化，且 origin、local current、SSH active、primary isolated 的源码一致。
2. **让 AutoReport V3 在独立 branch 完成。** 建议先提交 schema/writer/runner/tests，再提交设计文档与一致的 MD/HTML 验收报告；根级 planning 文件不进入 Git。
3. **经用户确认后，把 feature fast-forward 到 main。** 当前 main 没有独有提交，技术上可 `--ff-only`；这一步会改变 `main`，本轮故意停在门前。
4. **main 更新后再整合 AutoReport V3。** 它以 `d38df143` 为基线，可在完成测试后作为后续独立 PR/merge。
5. **历史恢复线不合并。** `39d284d`、`92a28b6`、`565aaf6` 和旧 stashes 继续作为显式恢复点；若未来要发布，必须逐条重新审查，而非批量 push。
6. **实验 checkout 保持 pin。** 只有 active/primary isolated 跟随当前工作线；E1、GraphRevoker、Gate1、Citeseer V2、IM materializer 和 legacy nips checkout 继续固定被测 SHA。

## 8. 本轮已执行 / 明确未执行

已执行：

- `git ls-remote` 核验 GitHub heads；
- 本地 `git fetch origin --tags --no-recurse-submodules`，无 prune；
- local/SSH 全部只读 status、refs、stash、commit graph、worktree、hash 与进程审计；
- 生成本 Markdown 与同结论的静态 HTML。

未执行：

- 未合并或移动 `main`；
- 未 push 3 个历史 local-only commits；
- 未 stash/drop/reset/checkout/clean SSH active；
- 未覆盖或删除 journal、A6 YAML、SQLite、`_backups`、results、runs、cache、PID/log；
- 未改 TracIn 或其他算法；
- 未 prune refs、删除 worktree、运行 GC 或清理实验结果。

## 9. 审计边界

- GitHub heads 以 2026-07-14 本轮 `ls-remote` 为准；SSH clone 的 stale remote-tracking refs 不视为 GitHub 当前状态。
- 报告冻结的是审计文档发布前的源码状态 `d38df143`。若本报告随后作为 documentation-only commit 发布，最终 feature HEAD 会前进一格，但 `cache_v2/`、`attack/`、`experiments/` 与算法源码仍保持 `d38df143` 内容。
- 没有 live runner 只代表审计时刻，不授权删除旧结果或 PID/log。
