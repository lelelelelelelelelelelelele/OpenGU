# Experiment Repair Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `experiments/AGENTS.md` route Selection/selector and GU-method defects through the human-readable `13_重跑与缓存修复Runbook.md` before any machine-side repair operation.

**Architecture:** The experiment guide owns one link to the human repair decision source. That source determines whether the Selection or GU repair chain applies and establishes the affected evidence boundary; machine instructions are reached only through the Runbook after the scope is known.

**Tech Stack:** Markdown, Git, PowerShell, ripgrep.

## Global Constraints

- Modify only `experiments/AGENTS.md` plus this implementation plan.
- Do not modify `13_重跑与缓存修复Runbook.md` or the SyncMate machine Runbook.
- Do not recreate `13A` or `13B`.
- Preserve the existing root/experiment ownership, GPU, dry-run and `data/processed` rules.
- Keep the repair Runbook link at one authoritative location in `experiments/AGENTS.md`.

---

### Task 1: Route Experiment Repairs Through The Human Runbook

**Files:**
- Modify: `experiments/AGENTS.md:15-18`
- Modify: `experiments/AGENTS.md:55`
- Modify: `experiments/AGENTS.md:98`

**Interfaces:**
- Consumes: the user-approved distinction between Selection/selector repair and GU-method repair
- Produces: one semantic repair link and two non-duplicating references to the already confirmed repair chain

- [ ] **Step 1: Replace the generic repair-context bullet**

Use this exact text:

```markdown
- 出现 Selection/selector 或 GU method 缺陷，以及相关 Cache、Artifact、结果或证据的失效与恢复问题时，先读取[重跑与缓存修复 Runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md)中对应的修复链，确认影响范围和证据边界；只有范围明确后，才执行该页链接的机器端操作规范。
```

- [ ] **Step 2: Remove duplicate generic Runbook wording**

In the existing-cell paragraph, replace `按 repair Runbook 判断` with
`按已确认的修复链判断`。

In the evidence-closure paragraph, remove the second Runbook link and state
that invalidation, repair, rerun and recovery follow the confirmed repair
chain.

- [ ] **Step 3: Verify the routing contract**

Run:

```powershell
rg -n '重跑与缓存修复 Runbook|Selection/selector|GU method|已确认的修复链|机器端操作规范' experiments/AGENTS.md
```

Expected:

- one Markdown link to `13_重跑与缓存修复Runbook.md`;
- one Selection/selector versus GU-method routing statement;
- later paragraphs refer to the confirmed repair chain without a second link.

- [ ] **Step 4: Verify scope and formatting**

Run:

```powershell
git diff --check
git diff -- experiments/AGENTS.md
git status --short
```

Expected: no whitespace errors; no changes to either repair Runbook, root
guidance, experiment code, configuration, Cache, results or live state.

- [ ] **Step 5: Commit the focused documentation change**

```powershell
git add -- experiments/AGENTS.md docs/superpowers/plans/2026-07-30-experiment-repair-routing.md
git diff --cached --name-status
git commit -m "docs(experiments): route repairs through human runbook"
```

Expected: the commit contains exactly the experiment guide and this plan.
