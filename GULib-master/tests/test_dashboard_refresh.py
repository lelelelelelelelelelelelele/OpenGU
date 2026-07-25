import importlib.util
from pathlib import Path


def _load_refresh_module():
    path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "dashboard"
        / "refresh.py"
    )
    spec = importlib.util.spec_from_file_location("dashboard_refresh", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_todo_cards_wrap_long_task_and_status_text(
    tmp_path, monkeypatch
):
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

    assert (
        """'<span class="txt"><span class="task"><span class="tid">'+"""
        """esc(it.id)+'</span> '"""
    ) in rendered
    assert (
        """(it.label?'<span class="sub">'+it.label+'</span>':'')"""
        in rendered
    )
    assert '"id": "E8"' in rendered
    assert "reports/very_long_acceptance_report_name.md" in rendered
    assert ".item .txt{flex:1;min-width:0}" in rendered
    assert ".sub{display:block;" in rendered
    assert "white-space:normal" in rendered
    assert ".item .task,.item .sub,.item code,.item .ref{" in rendered
    assert "overflow-wrap:anywhere" in rendered
