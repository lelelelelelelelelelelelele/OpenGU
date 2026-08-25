import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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


def _write_item(root, code, status, item_type="Block", title=None):
    path = root / ".workblock" / "items" / code / "WORKITEM.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    id_label = "Todo ID" if item_type == "Todo" else "Block ID"
    path.write_text(
        f"""# {code} · {title or code}

{id_label}: `{code}`

当前状态: `{status}`

Item Type: {item_type}
""",
        encoding="utf-8",
    )
    return path


def _node_table(rows):
    rendered = [
        "| ID | 类型 | 节点 | 优先级 | 前置 | Owner |",
        "|---|---|---|---|---|---|",
    ]
    rendered.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(rendered)


class DashboardRefreshTests(unittest.TestCase):
    def test_workitem_statuses_are_projected_from_records(self):
        refresh = _load_refresh_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_item(root, "AAGU-001", "accepted")
            _write_item(root, "AAGU-002", "registered / not claimed")
            _write_item(root, "AAGU-003", "registered / not claimed")
            _write_item(root, "AAGU-004", "todo candidate", "Todo")
            _write_item(root, "AAGU-005", "awaiting acceptance")
            _write_item(root, "AAGU-006", "working / claimed")
            md = """# Workplan

## 5. 实验 timeline

""" + _node_table(
                [
                    ("AAGU-001", "EXP", "closed", "P0", "—", "owner"),
                    ("AAGU-002", "EXP", "ready", "P0", "AAGU-001", "owner"),
                    ("AAGU-003", "EXP", "blocked", "P1", "AAGU-005", "owner"),
                    ("AAGU-004", "EXP", "candidate", "P1", "AAGU-001", "owner"),
                    ("AAGU-005", "EXP", "review", "P1", "—", "owner"),
                    ("AAGU-006", "EXP", "working", "P1", "—", "owner"),
                ]
            )

            items = refresh.load_workitems(root / ".workblock" / "items")
            nodes = refresh.parse_plan_nodes(md)
            projected = {
                node["id"]: node
                for node in refresh.project_nodes(nodes, items, "AAGU-006")
            }

            self.assertEqual(projected["AAGU-001"]["projection"], "accepted / closed")
            self.assertEqual(projected["AAGU-002"]["projection"], "registered / not claimed")
            self.assertEqual(projected["AAGU-003"]["projection"], "blocked by AAGU-005")
            self.assertEqual(projected["AAGU-004"]["projection"], "todo candidate / ready to promote")
            self.assertEqual(projected["AAGU-005"]["projection"], "awaiting acceptance")
            self.assertEqual(projected["AAGU-006"]["projection"], "in progress / current")

    def test_drift_checks_detect_duplicate_closed_current_and_stale_todo_block(self):
        refresh = _load_refresh_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_item(root, "AAGU-001", "accepted")
            _write_item(root, "AAGU-002", "blocked", "Todo")
            plan = root / "WORKPLAN.md"
            plan.write_text(
                """# Workplan

Current node: AAGU-001

## 5. 实验 timeline

"""
                + _node_table(
                    [
                        ("AAGU-001", "EXP", "closed", "P0", "—", "[missing](missing.md)"),
                        ("AAGU-002", "EXP", "candidate", "P0", "AAGU-001", "owner"),
                        ("AAGU-002", "EXP", "duplicate", "P0", "AAGU-001", "owner"),
                    ]
                ),
                encoding="utf-8",
            )
            md = plan.read_text(encoding="utf-8")
            items = refresh.load_workitems(root / ".workblock" / "items")
            nodes = refresh.parse_plan_nodes(md)
            errors = refresh.validate_drift(md, plan, nodes, items, "AAGU-001")
            joined = "\n".join(errors)

            self.assertIn("duplicate node mapping: AAGU-002", joined)
            self.assertIn("current node is already accepted/closed: AAGU-001", joined)
            self.assertIn("Todo AAGU-002 remains blocked after all dependencies closed", joined)
            self.assertIn("broken link: missing.md", joined)

    def test_refresh_updates_projection_and_generated_cards_wrap(self):
        refresh = _load_refresh_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "WORKPLAN.md"
            output = root / "progress.html"
            (root / "owner.md").write_text("owner", encoding="utf-8")
            _write_item(root, "AAGU-001", "registered / not claimed")
            source.write_text(
                """# Workplan

> Last updated: 2026-08-26

Current node: AAGU-001

## 0. 一句话现状

Ready.

[dashboard](progress.html)

## 1. WorkItem 状态投影

<!-- WORKITEM_STATUS:BEGIN -->
stale
<!-- WORKITEM_STATUS:END -->

## 5. 实验 timeline

"""
                + _node_table(
                    [
                        (
                            "AAGU-001",
                            "EXP",
                            "Long task with `very_long_unbroken_identifier_for_dashboard`",
                            "P0",
                            "—",
                            "[owner](owner.md)",
                        )
                    ]
                ),
                encoding="utf-8",
            )

            with mock.patch.object(refresh, "ROOT", root), mock.patch.object(
                refresh, "SRC", source
            ), mock.patch.object(refresh, "OUT", output), mock.patch.object(
                refresh, "WORKITEM_ROOT", root / ".workblock" / "items"
            ):
                self.assertEqual(refresh.main([]), 0)

            rendered = output.read_text(encoding="utf-8")
            projected = source.read_text(encoding="utf-8")
            self.assertIn("registered / not claimed / current", projected)
            self.assertIn('"id": "AAGU-001"', rendered)
            self.assertIn("very_long_unbroken_identifier_for_dashboard", rendered)
            self.assertIn(".item .txt{flex:1;min-width:0}", rendered)
            self.assertIn("overflow-wrap:anywhere", rendered)


if __name__ == "__main__":
    unittest.main()
