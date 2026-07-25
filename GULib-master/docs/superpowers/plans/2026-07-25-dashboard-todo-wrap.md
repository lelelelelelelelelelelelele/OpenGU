# Dashboard Todo Wrapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make long Todo tasks, status details, paths, and inline code wrap cleanly inside the generated four-column dashboard.

**Architecture:** Keep `WORKPLAN.md` as the source and change only the dashboard generator template. A focused integration-style pytest runs the real generator against a temporary Markdown fixture and asserts the generated DOM and CSS expose the wrapping contract.

**Tech Stack:** Python 3.8+ standard library, pytest, self-contained HTML/CSS/JavaScript.

## Global Constraints

- Do not rewrite `WORKPLAN.md` task content.
- Do not hand-edit `self/dashboard/progress.html`; regenerate it from the script.
- Preserve task parsing, filters, progress counts, colors, and GPU classification.
- Preserve the user's pre-existing uncommitted `WORKPLAN.md` and generated HTML state.

---

### Task 1: Protect the Todo wrapping contract

**Files:**
- Create: `tests/test_dashboard_refresh.py`
- Modify: `scripts/dashboard/refresh.py:281-296`
- Modify: `scripts/dashboard/refresh.py:386-390`
- Regenerate: `self/dashboard/progress.html`

**Interfaces:**
- Consumes: `refresh.main([])` with monkeypatched `SRC` and `OUT` paths.
- Produces: generated Todo markup containing `.task` and block-level `.sub` regions, plus CSS that permits flex shrinking and emergency token wrapping.

- [x] **Step 1: Write the failing test**

```python
import importlib.util
from pathlib import Path


def _load_refresh_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "dashboard" / "refresh.py"
    spec = importlib.util.spec_from_file_location("dashboard_refresh", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_todo_cards_wrap_long_task_and_status_text(tmp_path, monkeypatch):
    refresh = _load_refresh_module()
    source = tmp_path / "WORKPLAN.md"
    output = tmp_path / "progress.html"
    source.write_text(
        """# Workplan

> Last updated: 2026-07-25

## 0. 一句话现状

Ready.

## 1. 状态快照

| 维度 | 状态 | 原因 / 细节 | 权威出处 |
|---|---|---|---|
| code | 🟡 partial | waiting | report |

## 5. 实验

| ID | 任务 | config | 状态 |
|---|---|---|---|
| **E8** ★ | **Long task** with `very_long_unbroken_identifier_for_dashboard` | cfg | ☐ long status with `reports/very_long_acceptance_report_name.md` |
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(refresh, "SRC", source)
    monkeypatch.setattr(refresh, "OUT", output)

    assert refresh.main([]) == 0
    rendered = output.read_text(encoding="utf-8")

    assert '<span class="task"><span class="tid">E8</span>' in rendered
    assert '<span class="sub">long status with ' in rendered
    assert ".item .txt{flex:1;min-width:0}" in rendered
    assert ".sub{display:block;" in rendered
    assert "white-space:normal" in rendered
    assert ".item .task,.item .sub,.item code,.item .ref{" in rendered
    assert "overflow-wrap:anywhere" in rendered
```

- [x] **Step 2: Run the focused test and verify RED**

Run:

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_dashboard_refresh.py
```

Expected: FAIL because the current output has no `.task` wrapper, keeps `.sub` inline with `white-space:nowrap`, and omits `min-width:0` and emergency wrapping.

- [x] **Step 3: Implement the minimal DOM and CSS change**

Change the generated Todo markup to:

```javascript
'<span class="txt"><span class="task"><span class="tid">'+esc(it.id)+'</span> '+it.task+'</span>'+
(it.label?'<span class="sub">'+it.label+'</span>':'')+'</span>'+
```

Change the relevant CSS contract to:

```css
.item .txt{flex:1;min-width:0}
.item .task,.item .sub,.item code,.item .ref{
  overflow-wrap:anywhere;word-break:break-word}
.sub{display:block;color:var(--muted);font-size:11.5px;
  white-space:normal;margin-top:4px;line-height:1.4}
```

- [x] **Step 4: Run the focused test and verify GREEN**

Run:

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_dashboard_refresh.py
```

Expected: `1 passed`.

- [x] **Step 5: Regenerate and validate the real dashboard**

Run:

```powershell
E:/conda_package/envs/gnn/python.exe scripts/dashboard/refresh.py
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_dashboard_refresh.py
git diff --check
```

Expected: the generator reports four stages, the test passes, and `git diff --check` reports no whitespace errors.

- [x] **Step 6: Review the exact diff**

Confirm that:

- `WORKPLAN.md` retains the user's existing content.
- `progress.html` changes only because it was regenerated from that content and the updated template.
- No cache, result, report, or unrelated source file changed.

- [x] **Step 7: Commit the implementation**

```powershell
git add -- scripts/dashboard/refresh.py tests/test_dashboard_refresh.py self/dashboard/progress.html docs/superpowers/plans/2026-07-25-dashboard-todo-wrap.md
git commit -m "fix(dashboard): wrap long todo card details"
```
