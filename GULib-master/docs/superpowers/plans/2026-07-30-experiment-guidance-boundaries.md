# Experiment Guidance Boundaries Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove duplicated experiment-entry facts from the root guide and make `experiments/AGENTS.md` the sole owner of local dry-run, registered launcher, and formal GPU fallback rules.

**Architecture:** The root guide keeps repository-wide execution roles and routes experiment-specific behavior downward. The experiment guide owns the concrete generic runner, local interpreter, context-loading boundary, and GPU hard stop. Repair documentation and its links remain byte-for-byte outside this phase.

**Tech Stack:** Markdown, Git, PowerShell, ripgrep.

## Global Constraints

- Modify only `AGENTS.md` and `experiments/AGENTS.md` during implementation.
- Preserve the current `data/processed` formal-data policy.
- Do not modify, move, delete, or relink `13_重跑与缓存修复Runbook.md`, `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`, or any `13A/13B` path.
- Do not stage unrelated working-tree changes.
- Keep current experiment status out of both agent guides.

---

### Task 1: Align Root And Experiment Guidance Ownership

**Files:**
- Modify: `AGENTS.md:23-45`
- Modify: `experiments/AGENTS.md:11-18`
- Modify: `experiments/AGENTS.md:43-46`
- Modify: `experiments/AGENTS.md:79-91`
- Verify unchanged: `文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md`
- Verify unchanged: `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md`

**Interfaces:**
- Consumes: the approved design in `docs/superpowers/specs/2026-07-30-experiment-guidance-and-repair-ownership-design.md`
- Produces: one root-to-directory ownership route, one local generic-matrix dry-run command, and one formal GPU hard stop

- [ ] **Step 1: Remove concrete experiment entry points from the root execution pipeline**

Replace the sentence that names `experiments/run.py` and `main.py` with:

```markdown
Registered experiment definitions enter the execution chain through the launcher owned by their plan and directory-level guidance:
```

Keep the existing high-level flow from `CLI / YAML` through reviewable
artifacts, because it describes repository architecture rather than a concrete
launcher.

- [ ] **Step 2: Remove the interpreter and formal-entry facts from root runtime guidance**

Replace root section 5 with wording that retains the `config.py` import hazard,
local-versus-SSH responsibility, and proportional validation while routing
experiment-specific commands downward:

```markdown
Use the local machine for code changes, CPU analysis, targeted tests, and reviewing verified evidence. `config.py` parses CLI arguments at import time; do not import it from lightweight tests or notebooks unless the CLI context is intentionally supplied. Run formal GPU experiments from the active SSH checkout; `experiments/AGENTS.md` owns experiment entry-point selection, local experiment commands, and the detailed remote environment, dataset, pinned-SHA, and formal-gate rules. Validate changes in proportion to their risk: run the smallest relevant tests for code, the registered dry-run for experiment configurations, and link plus generated-artifact checks for documentation.
```

- [ ] **Step 3: Make dry-run context loading explicit in the experiment guide**

Replace the current line that groups source reading, local tests, dry-run, and
smoke together with:

```markdown
- 仅做源码阅读或局部测试时，不加载正式运行和修复材料；dry-run 或 disposable smoke 只加载当前配置与 launcher 所需的相邻验证材料，不加载失败恢复材料。
```

Keep the preceding WORKPLAN, formal-launch, and failure/recovery routing lines
unchanged.

- [ ] **Step 4: Put the local interpreter only in the experiment guide**

Replace the generic dry-run command with:

```markdown
通用矩阵在本地先用 `E:/conda_package/envs/gnn/python.exe experiments/run.py <registered-config.yaml> --dry_run` 验证定义；正式执行只使用注册计划指定的 launcher。
```

Keep the following SyncMate rule unchanged.

- [ ] **Step 5: Add the formal GPU hard stop**

Insert immediately after the shared-stage-check and experiment-preflight list:

```markdown
正式 GPU gate 或 matrix 必须枚举到至少一张 GPU；GPU 不可用时立即停止，禁止自动降级到 CPU。
```

Do not change the existing local CPU analysis, formal SSH, clean-tree, SHA,
Cache, or `data/processed` rules.

- [ ] **Step 6: Verify root facts are removed and directory ownership is complete**

Run:

```powershell
rg -n 'experiments/run.py|E:/conda_package/envs/gnn/python.exe|formal entry point' AGENTS.md
```

Expected: no matches and ripgrep exit code `1`.

Run:

```powershell
rg -n 'E:/conda_package/envs/gnn/python.exe experiments/run.py .*--dry_run|正式 GPU gate 或 matrix 必须枚举到至少一张 GPU|禁止自动降级到 CPU' experiments/AGENTS.md
```

Expected: one dry-run command and one GPU hard-stop line.

- [ ] **Step 7: Verify deferred repair documentation is untouched**

Run:

```powershell
git diff --exit-code HEAD -- 'GULib-master/文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md' 'GULib-master/scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md'
```

Expected: exit code `0` and no output.

- [ ] **Step 8: Review the complete documentation diff**

Run:

```powershell
git diff --check
git diff -- 'GULib-master/AGENTS.md' 'GULib-master/experiments/AGENTS.md'
git status --short
```

Expected: no whitespace errors; only the approved root and experiment-guide
changes are selected for the implementation commit; unrelated dirty files
remain unstaged.

- [ ] **Step 9: Commit only the two agent guides**

```powershell
git add -- 'GULib-master/AGENTS.md' 'GULib-master/experiments/AGENTS.md'
git diff --cached --name-status
git commit -m "docs(experiments): align guidance ownership"
```

Expected: the staged file list contains exactly the two agent guides.
