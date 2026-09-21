from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from scripts.syncmate import syncmate as sm
import pytest
import opengu_recipes as _project_recipes
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import artifacts as _artifacts, brief as _brief, bundles as _bundles, cli as _cli, collection as _collection, constants as _constants, context as _context, dashboard as _dashboard, devices as _devices, diagnostics as _diagnostics, dispatch as _dispatch, evidence as _evidence, fingerprints as _fingerprints, gates as _gates, handoff as _handoff, history as _history, identity as _identity, index as _index, next_steps as _next_steps, preflight as _preflight, queue as _queue, receipts as _receipts, recipes as _recipes, saved_reports as _saved_reports, snapshot as _snapshot, storage as _storage, worker as _worker, workflow as _workflow

class AdapterFixture(OpenGUProjectExtension):
    """Use real result/acceptance policies without unrelated research expansion."""
    def recipes(self, project_root):
        return _constants.RUNNER_RECIPE_DEFINITIONS


@pytest.fixture(autouse=True)
def scoped_project(tmp_path):
    with _context.use(tmp_path, extension=AdapterFixture(), require_origin_main=True):
        yield


def _run_cli(argv):
    return _cli.main(argv, project_root=_context.current().root, extension=_context.extension(), require_origin_main=True)


def _project_acceptance(profile, definition, *, node_id, expected_git_sha):
    return _context.extension().accept(profile, definition, {
        'artifact_index': _index.load_artifact_index(), 'node_id': node_id,
        'expected_git_sha': expected_git_sha, 'project_root': _context.current().root,
    })


def _write(path: Path, data: bytes = b"{}") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _write_leaf(root: Path, rel_leaf: str, *, meta_sha: str = "abc1234") -> Path:
    leaf = root / rel_leaf
    _write(leaf / "attack.json", b'{"attack": true}')
    _write(leaf / "collateral.json", b'{"collateral": true}')
    _write(leaf / "_meta.json", json.dumps({"git_sha": meta_sha, "hostname": "host-a"}).encode())
    return leaf


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _stage_by_id(stages, stage_id):
    return next(stage for stage in stages if stage["id"] == stage_id)


def test_default_implementation_is_core_backed_exact_entry():
    assert Path(sm.__file__).name == 'syncmate.py'
    assert sm.core_main is _cli.main
    assert sm.__name__ == 'scripts.syncmate.syncmate'


def test_reviewed_project_recipes_satisfy_core_execution_contract():
    # UI enumeration alone does not instantiate Core's bounded Recipe contract.
    with _context.use(sm.PROJECT_ROOT, extension=OpenGUProjectExtension()):
        recipes = _recipes.ExecutionAdapter().recipes()
    assert set(recipes) == set(_project_recipes.recipe_definitions())
    assert all(1 <= recipe.timeout_seconds <= _constants.RUNNER_AGENT_MAX_TIMEOUT_SECONDS
               for recipe in recipes.values())


def test_direct_syncmate_script_bootstraps_repo_import_path(tmp_path):
    script = Path(sm.__file__).resolve()
    repo = script.parents[2]
    probe = (
        "import os,runpy,sys; "
        "repo=os.path.abspath(sys.argv[2]); "
        "sys.path=[p for p in sys.path if os.path.abspath(p or os.getcwd()) != repo]; "
        "scope=runpy.run_path(sys.argv[1],run_name='syncmate_probe'); "
        "import experiments; "
        "assert str(scope['PROJECT_ROOT']) in sys.path"
    )

    completed = subprocess.run(
        [sys.executable, "-c", probe, str(script), str(repo)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr


def test_bundle_and_import_bundle_offline_roundtrip_updates_trusted_results(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    leaf_rel = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.71, "mia_auc": 0.64, "selected_nodes": [1, 2]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.8, "gap": 0.03}]}).encode(),
        "_meta.json": json.dumps({"git_sha": "abcdef123", "hostname": "runner-a", "timestamp": "2026-07-01T10:00:00"}).encode(),
    }

    _context.select(root=runner)
    _context.select(root=(runner_sync).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    _devices.write_device_config(runner_config, _devices.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    for name, data in artifacts.items():
        _write(runner / leaf_rel / name, data)

    assert _run_cli(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    bundle_out = json.loads(capsys.readouterr().out)
    assert bundle_out["mode"] == "bundle"
    assert bundle_out["summary"]["manifest_files"] == 3
    assert bundle_out["summary"]["manifest_leaves"] == 1
    assert bundle_path.is_file()

    _context.select(root=collector)
    _context.select(root=(collector_sync).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    config = _devices.build_device_config("local", "collector", str(collector))
    _devices.add_peer_to_device(
        config,
        "gpu4090",
        _devices.build_peer_config("runner", "ssh-gpu", str(runner)),
    )
    _devices.write_device_config(collector_config, config)

    assert _run_cli(["--config", str(collector_config), "import-bundle", str(bundle_path), "--json"]) == 0
    import_out = json.loads(capsys.readouterr().out)
    local_leaf = collector / "results" / "runs" / "gpu4090" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    index = json.loads((collector_sync / "artifact_index.json").read_text(encoding="utf-8"))

    assert import_out["mode"] == "import-bundle"
    assert import_out["known_peer"] is True
    assert import_out["collect"]["summary"]["fetched"] == 3
    assert import_out["collect"]["summary"]["verified"] == 3
    assert import_out["verify"]["summary"]["status"] == "verified"
    assert import_out["remote_status"]["report_path"] == ".syncmate/remote_status_gpu4090.json"
    assert import_out["results"]["written"] is True
    assert import_out["results"]["reason"] == "written"
    assert import_out["results"]["summary"]["rows"] == 1
    assert import_out["results_table_path"] == ".syncmate/results_table.json"
    assert import_out["results_csv_path"] == ".syncmate/results_table.csv"
    assert (collector_sync / "last_collect_gpu4090.json").is_file()
    assert (collector_sync / "last_verify_gpu4090.json").is_file()
    assert all((local_leaf / name).is_file() for name in artifacts)
    assert index["peers"]["gpu4090"]["summary"]["status"] == "verified"
    assert index["peers"]["gpu4090"]["summary"]["indexed"] == 3
    assert index["peers"]["gpu4090"]["source_report"] == ".syncmate/last_verify_gpu4090.json"
    assert (collector_sync / "results_table.json").is_file()
    assert (collector_sync / "results_table.csv").is_file()

    assert _run_cli(["--config", str(collector_config), "results", "--write", "--check", "--json"]) == 0
    results_out = json.loads(capsys.readouterr().out)
    assert results_out["summary"]["rows"] == 1
    assert results_out["summary"]["parse_errors"] == 0
    assert results_out["rows"][0]["node_id"] == "gpu4090"
    assert results_out["rows"][0]["f1_after"] == 0.71
    assert results_out["rows"][0]["f1_drop"] == 0.09000000000000008
    assert (collector_sync / "results_table.json").is_file()
    assert (collector_sync / "results_table.csv").is_file()


def test_sync_runs_apply_verify_and_writes_receipt_brief_dashboard(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    _context.select(root=repo)
    _context.select(root=(sync_dir).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(_identity, 'now_iso', lambda: "2026-07-01T12:00:00")

    config = _devices.build_device_config("local", "collector", str(repo))
    peer = _devices.build_peer_config("runner", "ssh-gpu", "/repo")
    peer["artifact_policy"] = {"include": ["attack.json", "collateral.json", "_meta.json"]}
    _devices.add_peer_to_device(config, "gpu4090", peer)
    _devices.write_device_config(config_path, config)

    leaf_remote = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    leaf_local = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.71, "mia_auc": 0.64, "selected_nodes": [1, 2]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.8, "gap": 0.03}]}).encode(),
        "_meta.json": json.dumps({"git_sha": "abcdef123", "hostname": "host-a", "timestamp": "2026-07-01T11:00:00"}).encode(),
    }
    calls = {"remote": [], "diff": [], "collect": [], "verify": []}

    def fake_remote(node_id, *_args, **_kwargs):
        calls["remote"].append(node_id)
        return {
            "generated_at": "2026-07-01T11:00:00",
            "node_id": node_id,
            "summary": {"result_leaves": 1, "git_dirty": False, "log_errors": 0},
            "errors": [],
            "report_path": f".syncmate/remote_status_{node_id}.json",
        }

    def fake_diff(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, save=True):
        calls["diff"].append((node_id, landing, artifact_names, save))
        return {
            "generated_at": "2026-07-01T11:05:00",
            "node_id": node_id,
            "mode": "diff",
            "landing": landing,
            "summary": {"remote_files": 3, "remote_leaves": 1, "remote_incomplete": 0, "already_current": 0, "missing": 3, "conflicts": 0},
            "missing": [
                {"path": f"{leaf_remote}/{name}", "sha256": _sha(data)}
                for name, data in artifacts.items()
            ],
            "conflicts": [],
            "errors": [],
            "report_path": f".syncmate/last_diff_{node_id}.json",
        }

    def fake_collect(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, overwrite=False, save=True):
        calls["collect"].append((node_id, landing, artifact_names, overwrite, save))
        for name, data in artifacts.items():
            _write(repo / f"{leaf_local}/{name}", data)
        return {
            "generated_at": "2026-07-01T11:10:00",
            "node_id": node_id,
            "mode": "apply",
            "landing": landing,
            "summary": {"remote_files": 3, "remote_leaves": 1, "remote_incomplete": 0, "already_current": 0, "missing_fetched": 3, "verified": 3, "conflicts": 0},
            "fetched": [
                {"path": f"{leaf_remote}/{name}", "local_path": f"{leaf_local}/{name}"}
                for name in artifacts
            ],
            "verification_failed": [],
            "conflicts": [],
            "errors": [],
            "artifact_index": ".syncmate/artifact_index.json",
            "report_path": f".syncmate/last_collect_{node_id}.json",
        }

    def fake_verify(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, save=True):
        calls["verify"].append((node_id, landing, artifact_names, save))
        _write(
            sync_dir / "artifact_index.json",
            json.dumps({
                "version": 0,
                "updated_at": "2026-07-01T11:20:00",
                "errors": [],
                "peers": {
                    node_id: {
                        "node_id": node_id,
                        "updated_at": "2026-07-01T11:20:00",
                        "landing": landing,
                        "artifact_policy": {"include": ["attack.json"]},
                        "source_report": f".syncmate/last_verify_{node_id}.json",
                        "summary": {
                            "remote_files": 3,
                            "remote_leaves": 1,
                            "remote_incomplete": 0,
                            "indexed": 3,
                            "missing": 0,
                            "conflicts": 0,
                            "status": "verified",
                        },
                        "items": [
                            {
                                "source_node": node_id,
                                "remote_path": f"{leaf_remote}/{name}",
                                "local_path": f"{leaf_local}/{name}",
                                "sha256": _sha(data),
                            }
                            for name, data in artifacts.items()
                        ],
                    },
                },
            }).encode(),
        )
        return {
            "generated_at": "2026-07-01T11:20:00",
            "node_id": node_id,
            "mode": "verify",
            "landing": landing,
            "summary": {"remote_files": 3, "remote_leaves": 1, "remote_incomplete": 0, "verified_current": 3, "missing": 0, "conflicts": 0, "status": "verified"},
            "verified": [
                {"path": f"{leaf_remote}/{name}", "sha256": _sha(data)}
                for name, data in artifacts.items()
            ],
            "missing": [],
            "conflicts": [],
            "errors": [],
            "artifact_index": ".syncmate/artifact_index.json",
            "report_path": f".syncmate/last_verify_{node_id}.json",
        }

    monkeypatch.setattr(_collection, 'apply_remote_status', fake_remote)
    monkeypatch.setattr(_collection, 'diff_collect', fake_diff)
    monkeypatch.setattr(_collection, 'apply_collect', fake_collect)
    monkeypatch.setattr(_collection, 'verify_collect', fake_verify)

    assert _run_cli(["--config", str(config_path), "sync", "gpu4090", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert calls["remote"] == ["gpu4090"]
    assert calls["diff"] == [("gpu4090", "results/runs/gpu4090", ("attack.json", "collateral.json", "_meta.json"), True)]
    assert calls["collect"] == [("gpu4090", "results/runs/gpu4090", ("attack.json", "collateral.json", "_meta.json"), False, True)]
    assert calls["verify"] == [("gpu4090", "results/runs/gpu4090", ("attack.json", "collateral.json", "_meta.json"), True)]
    assert out["mode"] == "sync"
    assert out["apply"] is True
    assert out["verify"] is True
    assert out["results_table_path"] == ".syncmate/results_table.json"
    assert out["results_csv_path"] == ".syncmate/results_table.csv"
    assert out["results"]["summary"]["rows"] == 1
    assert out["results"]["parse_errors"] == 0
    assert out["automation_core"]["status"] == "ok"
    assert out["automation_core"]["totals"]["missing"] == 3
    assert out["automation_core"]["totals"]["fetched_missing"] == 3
    assert out["automation_core"]["totals"]["checksum_verified"] == 3
    assert out["automation_core"]["totals"]["checksum_failed"] == 0
    assert out["automation_core"]["totals"]["indexed"] == 3
    assert out["automation_core"]["results"]["delta"]["previous_rows"] == 0
    assert out["automation_core"]["results"]["delta"]["current_rows"] == 1
    assert out["automation_core"]["results"]["delta"]["added_rows"] == 1
    assert out["receipt"]["preflight"]["status"] == "ready"
    assert out["receipt"]["automation_core"]["results"]["delta"]["added_rows"] == 1
    assert out["receipt"]["trusted_results"]["status"] == "ok"
    assert out["receipt"]["trusted_results"]["summary"]["rows"] == 1
    assert out["receipt"]["trusted_results"]["files"]["csv"] == ".syncmate/results_table.csv"
    assert out["receipt"]["peers"]["gpu4090"]["state"] == "accepted"
    assert out["receipt_path"] == ".syncmate/receipt_gpu4090.md"
    assert out["brief_path"] == ".syncmate/brief.md"
    assert out["runbook_path"] == ".syncmate/runbook.md"
    assert out["checklist_path"] == ".syncmate/checklist.md"
    assert out["dashboard"] == ".syncmate/status.html"
    assert out["workflow"] == ".syncmate/workflow.json"
    assert out["automation_core_path"] == ".syncmate/automation_core.json"
    assert out["automation_core_markdown_path"] == ".syncmate/automation_core.md"
    assert out["acceptance"] == ".syncmate/acceptance.json"
    assert out["action_plan"] == ".syncmate/action_plan.json"
    assert out["action_plan_markdown"] == ".syncmate/action_plan.md"
    assert out["preflight"]["report_path"] == ".syncmate/last_preflight.json"
    assert (sync_dir / "receipt_gpu4090.md").is_file()
    assert (sync_dir / "brief.md").is_file()
    assert (sync_dir / "runbook.md").is_file()
    assert (sync_dir / "checklist.md").is_file()
    assert (sync_dir / "last_preflight.json").is_file()
    assert (sync_dir / "results_table.json").is_file()
    assert (sync_dir / "results_table.csv").is_file()
    assert (sync_dir / "status.html").is_file()
    assert (sync_dir / "workflow.json").is_file()
    assert (sync_dir / "automation_core.json").is_file()
    assert (sync_dir / "automation_core.md").is_file()
    assert (sync_dir / "acceptance.json").is_file()
    assert (sync_dir / "action_plan.json").is_file()
    assert (sync_dir / "action_plan.md").is_file()
    assert (sync_dir / "state.json").is_file()
    assert (sync_dir / "history.jsonl").is_file()
    receipt_text = (sync_dir / "receipt_gpu4090.md").read_text(encoding="utf-8")
    assert "Automation Evidence" in receipt_text
    assert "Automation Core" in receipt_text
    assert "added=1" in receipt_text
    assert "Trusted results: status=ok rows=1" in receipt_text
    brief_text = (sync_dir / "brief.md").read_text(encoding="utf-8")
    assert "## Automation Core" in brief_text
    assert "added=1" in brief_text
    assert "Checksum OK/failed: 3/0" in brief_text
    assert ".syncmate/checklist.md" in brief_text
    assert ".syncmate/runbook.md" in brief_text
    runbook_text = (sync_dir / "runbook.md").read_text(encoding="utf-8")
    assert "# Syncmate Runbook" in runbook_text
    assert "python scripts/syncmate/syncmate.py sync gpu4090" in runbook_text
    checklist_text = (sync_dir / "checklist.md").read_text(encoding="utf-8")
    assert "# Syncmate Checklist" in checklist_text
    assert "Trusted result rows: 1" in checklist_text
    assert ".syncmate/acceptance.json" in checklist_text
    dashboard_html = (sync_dir / "status.html").read_text(encoding="utf-8")
    workflow_json = json.loads((sync_dir / "workflow.json").read_text(encoding="utf-8"))
    automation_json = json.loads((sync_dir / "automation_core.json").read_text(encoding="utf-8"))
    automation_markdown = (sync_dir / "automation_core.md").read_text(encoding="utf-8")
    acceptance_json = json.loads((sync_dir / "acceptance.json").read_text(encoding="utf-8"))
    assert workflow_json["mode"] == "workflow"
    assert workflow_json["workflow_path"] == ".syncmate/workflow.json"
    assert automation_json["mode"] == "automation_core"
    assert automation_json["automation_core_path"] == ".syncmate/automation_core.json"
    assert automation_json["automation_core_markdown_path"] == ".syncmate/automation_core.md"
    assert automation_json["totals"]["indexed"] == 3
    assert "# Syncmate Automation Core" in automation_markdown
    assert "Checksum OK/failed: 3/0" in automation_markdown
    assert acceptance_json["mode"] == "acceptance"
    assert acceptance_json["acceptance_path"] == ".syncmate/acceptance.json"
    assert acceptance_json["automation_core"]["totals"]["checksum_verified"] == 3
    action_plan_json = json.loads((sync_dir / "action_plan.json").read_text(encoding="utf-8"))
    action_plan_markdown = (sync_dir / "action_plan.md").read_text(encoding="utf-8")
    assert action_plan_json["mode"] == "next"
    assert action_plan_json["action_plan_path"] == ".syncmate/action_plan.json"
    assert "# Syncmate Action Plan" in action_plan_markdown
    assert "Acceptance" in dashboard_html
    assert ".syncmate/acceptance.json" in dashboard_html
    assert "Automation Workflow" in dashboard_html
    assert ".syncmate/workflow.json" in dashboard_html
    assert "Next Commands" in dashboard_html
    assert "<th>Evidence</th>" in dashboard_html
    assert "Manual Actions" in dashboard_html
    assert "python scripts/syncmate/syncmate.py collect gpu4090 --apply" in dashboard_html
    assert "writes: results/runs/gpu4090/" in dashboard_html
    assert "Trusted Results Table" in dashboard_html
    assert ".syncmate/results_table.csv" in dashboard_html
    assert "<td class='num'>1</td>" in dashboard_html or ">1</b>" in dashboard_html


def test_sync_local_transport_collects_from_same_machine_repo(tmp_path, monkeypatch, capsys):
    collector = tmp_path / "collector"
    runner = tmp_path / "runner"
    sync_dir = collector / ".syncmate"
    config_path = sync_dir / "device.yaml"
    _context.select(root=collector)
    _context.select(root=(sync_dir).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "local"})

    leaf = runner / "results" / "runs" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.72, "mia_auc": 0.61, "selected_nodes": [1, 3]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.81, "gap": 0.04}]}).encode(),
        "_meta.json": json.dumps({"git_sha": "remote123", "hostname": "runner-local"}).encode(),
    }
    for name, data in artifacts.items():
        _write(leaf / name, data)

    config = _devices.build_device_config("collector", "collector", str(collector))
    _devices.add_peer_to_device(
        config,
        "local-runner",
        _devices.build_peer_config(
            "runner",
            None,
            str(runner),
            transport="local",
        ),
    )
    _devices.write_device_config(config_path, config)

    assert _run_cli(["--config", str(config_path), "sync", "local-runner", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    local_attack = collector / "results" / "runs" / "local-runner" / "cora_GCN_r0.05" / "GIF_im" / "seed42" / "attack.json"
    index = json.loads((sync_dir / "artifact_index.json").read_text(encoding="utf-8"))
    results_table = json.loads((sync_dir / "results_table.json").read_text(encoding="utf-8"))

    assert out["peer_results"]["local-runner"]["remote_status"]["remote"]["transport"] == "local"
    assert out["peer_results"]["local-runner"]["collect"]["remote"]["transport"] == "local"
    assert out["receipt"]["peers"]["local-runner"]["state"] == "accepted"
    assert local_attack.read_bytes() == artifacts["attack.json"]
    assert index["peers"]["local-runner"]["summary"]["status"] == "verified"
    assert index["peers"]["local-runner"]["items"][0]["local_path"].startswith("results/runs/local-runner/")
    assert results_table["summary"]["rows"] == 1
    assert results_table["rows"][0]["node_id"] == "local-runner"
    assert (sync_dir / "receipt_local-runner.md").is_file()
    assert (sync_dir / "status.html").is_file()
    assert (sync_dir / "workflow.json").is_file()


def test_results_cli_extracts_metrics_from_trusted_index(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    _context.select(root=repo)
    _context.select(root=(sync_dir).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    _devices.write_device_config(config_path, _devices.build_device_config("local", "collector", str(repo)))
    leaf_rel = "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42"
    artifacts = {
        "attack.json": json.dumps({
            "results": {
                "random": {
                    "f1_after": 0.72,
                    "mia_auc": 0.61,
                    "unlearn_time": 12.5,
                    "selection_time": 1.25,
                    "selection_cache_hit": True,
                    "selected_nodes": [1, 2, 3],
                }
            }
        }).encode(),
        "collateral.json": json.dumps({
            "results": [{
                "strategy": "random",
                "perf_before": 0.8,
                "perf_unlearn": 0.72,
                "perf_retrain": 0.75,
                "gap": -0.03,
                "hop_decay": {
                    "1_hop_flip_rate": 0.1,
                    "1_hop_count": 10,
                    "gt3_hop_flip_rate": 0.02,
                    "gt3_hop_count": 5,
                },
            }]
        }).encode(),
        "_meta.json": json.dumps({
            "git_sha": "abcdef123456",
            "hostname": "host-a",
            "timestamp": "2026-07-01T00:00:00",
        }).encode(),
    }
    items = []
    for name, data in artifacts.items():
        local_path = f"{leaf_rel}/{name}"
        _write(repo / local_path, data)
        items.append({
            "source_node": "gpu4090",
            "remote_path": f"results/runs/cora_GCN_r0.05/GIF_random/seed42/{name}",
            "local_path": local_path,
            "sha256": _sha(data),
            "verified_at": "2026-07-01T00:00:00",
        })
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T00:00:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "updated_at": "2026-07-01T00:00:00",
                    "landing": "results/runs/gpu4090",
                    "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                    "source_report": ".syncmate/last_verify_gpu4090.json",
                    "summary": {"indexed": 3, "status": "verified"},
                    "items": items,
                },
            },
        }).encode(),
    )

    assert _run_cli(["--config", str(config_path), "results", "gpu4090", "--write", "--check", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    row = out["rows"][0]

    assert out["summary"]["rows"] == 1
    assert out["index_check"]["status"] == "ok"
    assert row["method"] == "GIF"
    assert row["strategy"] == "random"
    assert row["dataset"] == "cora"
    assert row["base_model"] == "GCN"
    assert row["ratio"] == "0.05"
    assert row["selected_n"] == 3
    assert row["f1_after"] == 0.72
    assert round(row["f1_drop"], 6) == 0.08
    assert row["mia_auc"] == 0.61
    assert row["gap"] == -0.03
    assert row["git_sha"] == "abcdef1"
    assert row["attack_sha256"] == _sha(artifacts["attack.json"])
    assert (sync_dir / "results_table.json").is_file()
    csv_text = (sync_dir / "results_table.csv").read_text(encoding="utf-8")
    assert "node_id,complete,cell,dataset,base_model,ratio,method,strategy" in csv_text
    assert "gpu4090,true,cora_GCN_r0.05,cora,GCN,0.05,GIF,random" in csv_text


def test_gate_payload_requires_trusted_results_table(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _context.select(root=repo)
    monkeypatch.setattr(_identity, 'now_iso', lambda: "2026-07-01T12:00:00")

    leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({
            "results": {"im": {"f1_after": 0.71, "mia_auc": 0.64, "selected_nodes": [1, 2]}}
        }).encode(),
        "collateral.json": json.dumps({
            "results": [{"strategy": "im", "perf_before": 0.8, "gap": 0.03}]
        }).encode(),
        "_meta.json": json.dumps({"git_sha": "abcdef123", "hostname": "host-a"}).encode(),
    }
    for name, data in artifacts.items():
        _write(repo / leaf / name, data)

    index = {
        "index_path": ".syncmate/artifact_index.json",
        "peers": {
            "gpu4090": {
                "node_id": "gpu4090",
                "summary": {"indexed": 3, "status": "verified"},
                "items": [
                    {
                        "source_node": "gpu4090",
                        "remote_path": f"results/runs/cora_GCN_r0.05/GIF_im/seed42/{name}",
                        "local_path": f"{leaf}/{name}",
                        "sha256": _sha(data),
                    }
                    for name, data in artifacts.items()
                ],
            },
        },
    }
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "artifact_index": index,
        "results_table": None,
    }

    missing = _gates.gate_payload(snapshot, [], require_results=True)
    missing_codes = {item["code"] for item in missing["failures"]}

    assert missing["passed"] is False
    assert missing["require_results"] is True
    assert "gate-results-missing" in missing_codes

    results_table = _index.results_payload_from_index(index)
    snapshot["results_table"] = results_table
    clean = _gates.gate_payload(snapshot, [], require_results=True)

    assert clean["passed"] is True
    assert clean["results_check"]["status"] == "ok"

    stale = json.loads(json.dumps(results_table))
    stale["summary"]["rows"] = 0
    snapshot["results_table"] = stale
    failed = _gates.gate_payload(snapshot, [], require_results=True)
    failed_codes = {item["code"] for item in failed["failures"]}

    assert failed["passed"] is False
    assert "gate-results-stale" in failed_codes


def test_results_use_remote_leaf_semantics_when_landing_wraps_remote_node(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _context.select(root=repo)
    _context.select(root=(repo / ".syncmate").parent)
    remote_leaf = "results/runs/__syncmate_gate4__/cora_GCN_r0.05/GIF_degree/seed42"
    local_leaf = (
        "results/runs/__syncmate_gate4_autodl__/__syncmate_gate4__/"
        "cora_GCN_r0.05/GIF_degree/seed42"
    )
    payloads = {
        "attack.json": json.dumps({
            "results": {"degree": {"f1_after": 0.45, "mia_auc": 0.54}},
        }).encode(),
        "collateral.json": json.dumps({
            "results": [{"strategy": "degree", "perf_before": 0.47}],
        }).encode(),
        "_meta.json": json.dumps({"git_sha": "e6091f9"}).encode(),
    }
    items = []
    for name, payload in payloads.items():
        local_path = f"{local_leaf}/{name}"
        _write(repo / local_path, payload)
        items.append({
            "source_node": "autodl-gate4",
            "remote_path": f"{remote_leaf}/{name}",
            "local_path": local_path,
            "sha256": _sha(payload),
        })
    index = {
        "version": 0,
        "peers": {
            "autodl-gate4": {
                "node_id": "autodl-gate4",
                "landing": "results/runs/__syncmate_gate4_autodl__",
                "artifact_policy": {"include": list(payloads)},
                "summary": {"indexed": len(items)},
                "items": items,
            },
        },
    }

    result = _index.results_payload_from_index(index)

    assert result["summary"]["rows"] == 1
    row = result["rows"][0]
    assert row["cell"] == "cora_GCN_r0.05"
    assert row["dataset"] == "cora"
    assert row["base_model"] == "GCN"
    assert row["ratio"] == "0.05"
    assert row["method"] == "GIF"
    assert row["strategy"] == "degree"
    assert row["seed"] == "seed42"



def test_lifecycle_cli_reports_accepted_phase_and_trace_check(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    _context.select(root=repo)
    _context.select(root=(sync_dir).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(_identity, 'now_iso', lambda: "2026-07-01T12:00:00")

    config = _devices.build_device_config("local", "collector", str(repo))
    _devices.add_peer_to_device(
        config,
        "gpu4090",
        _devices.build_peer_config("runner", "ssh-gpu", "/repo"),
    )
    _devices.write_device_config(config_path, config)
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    local_leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.72, "mia_auc": 0.61, "selected_nodes": [1]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.80}]}).encode(),
        "_meta.json": json.dumps({"git_sha": "abcdef123", "hostname": "host-a"}).encode(),
    }
    for name, data in artifacts.items():
        _write(repo / local_leaf / name, data)
    _write(
        sync_dir / "last_preflight.json",
        json.dumps({
            "generated_at": "2026-07-01T11:20:00",
            "mode": "preflight",
            "status": "ready",
            "summary": {"peers": 1, "ready": 1, "blocked": 0, "errors": 0, "warnings": 0},
            "report_path": ".syncmate/last_preflight.json",
            "peers": {"gpu4090": {"status": "ready", "ready": True}},
        }).encode(),
    )
    _write(
        sync_dir / "last_verify_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:30:00",
            "node_id": "gpu4090",
            "mode": "verify",
            "landing": "results/runs/gpu4090",
            "summary": {
                "remote_files": 3,
                "remote_leaves": 1,
                "remote_incomplete": 0,
                "verified_current": 3,
                "missing": 0,
                "conflicts": 0,
                "status": "verified",
            },
            "verified": [
                {"path": f"{remote_leaf}/{name}", "sha256": _sha(data)}
                for name, data in artifacts.items()
            ],
            "missing": [],
            "conflicts": [],
            "errors": [],
            "artifact_index": ".syncmate/artifact_index.json",
        }).encode(),
    )
    index = {
        "version": 0,
        "updated_at": "2026-07-01T11:30:00",
        "errors": [],
        "peers": {
            "gpu4090": {
                "node_id": "gpu4090",
                "updated_at": "2026-07-01T11:30:00",
                "landing": "results/runs/gpu4090",
                "source_report": ".syncmate/last_verify_gpu4090.json",
                "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                "summary": {
                    "remote_files": 3,
                    "remote_leaves": 1,
                    "remote_incomplete": 0,
                    "indexed": 3,
                    "missing": 0,
                    "conflicts": 0,
                    "status": "verified",
                },
                "items": [
                    {
                        "source_node": "gpu4090",
                        "remote_path": f"{remote_leaf}/{name}",
                        "local_path": f"{local_leaf}/{name}",
                        "sha256": _sha(data),
                    }
                    for name, data in artifacts.items()
                ],
            },
        },
    }
    _write(sync_dir / "artifact_index.json", json.dumps(index).encode())
    _index.write_results_table_files(_index.results_payload_from_index(index))

    assert _run_cli(["--config", str(config_path), "lifecycle", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["ready"] is True
    assert out["current"]["phase"] == "accepted"
    assert out["next"]["primary"]["command"] == "python scripts/syncmate/syncmate.py trace gpu4090 --check"
    assert out["summary"]["indexed_artifacts"] == 3
    assert out["summary"]["result_rows"] == 1


def test_workflow_payload_marks_missing_results_table_after_verified_index(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    _context.select(root=repo)
    monkeypatch.setattr(_identity, 'now_iso', lambda: "2026-07-01T12:00:00")

    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    local_leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({
            "results": {"im": {"f1_after": 0.72, "mia_auc": 0.61, "selected_nodes": [1]}}
        }).encode(),
        "collateral.json": json.dumps({
            "results": [{"strategy": "im", "perf_before": 0.81, "gap": 0.04}]
        }).encode(),
        "_meta.json": json.dumps({"git_sha": "abcdef123", "hostname": "host-a"}).encode(),
    }
    for name, data in artifacts.items():
        _write(repo / local_leaf / name, data)

    index_items = [
        {
            "source_node": "gpu4090",
            "remote_path": f"{remote_leaf}/{name}",
            "local_path": f"{local_leaf}/{name}",
            "sha256": _sha(data),
        }
        for name, data in artifacts.items()
    ]
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {
            "id": "local",
            "role": "collector",
            "peers": ["gpu4090"],
            "peer_configs": {
                "gpu4090": {"ssh": "ssh-gpu", "repo_path": "/repo", "landing": "results/runs/gpu4090"},
            },
        },
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {"result_leaves": 1, "git_short_sha": "abc1234"},
                "errors": [],
            },
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "summary": {"missing": 0, "conflicts": 0, "remote_incomplete": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:20:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0, "remote_incomplete": 0, "verified_current": 3},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {
            "peers": {
                "gpu4090": {
                    "updated_at": "2026-07-01T11:20:00",
                    "summary": {"indexed": 3, "status": "verified", "missing": 0, "conflicts": 0, "remote_incomplete": 0},
                    "items": index_items,
                },
            },
        },
        "results_table": None,
    }

    result = _workflow.workflow_payload(snapshot, [], require_verify=True, require_results=True)
    peer = result["peers"]["gpu4090"]
    results_stage = _stage_by_id(result["global_stages"], "results")
    commands = [item["command"] for item in result["next"]["commands"]]

    assert peer["status"] == "ok"
    assert _stage_by_id(peer["stages"], "index")["status"] == "ok"
    assert results_stage["status"] == "action-needed"
    assert results_stage["command"] == "python scripts/syncmate/syncmate.py results --write --check"
    assert "python scripts/syncmate/syncmate.py results --write --check" in commands


def test_acceptance_cli_can_write_machine_readable_verdict(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    _context.select(root=repo)
    _context.select(root=(sync_dir).parent)
    monkeypatch.setattr(_identity, 'git_state', lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(_identity, 'now_iso', lambda: "2026-07-01T12:00:00")

    config = _devices.build_device_config("local", "collector", str(repo))
    _devices.add_peer_to_device(
        config,
        "gpu4090",
        _devices.build_peer_config("runner", "ssh-gpu", "/repo"),
    )
    _devices.write_device_config(config_path, config)
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    local_leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({
            "results": {
                "im": {
                    "f1_after": 0.72,
                    "mia_auc": 0.61,
                    "unlearn_time": 1.25,
                    "selection_time": 0.33,
                    "selected_nodes": [1, 3, 5],
                }
            }
        }).encode(),
        "collateral.json": json.dumps({
            "results": [{"strategy": "im", "perf_before": 0.81, "gap": 0.04}]
        }).encode(),
        "_meta.json": json.dumps({
            "git_sha": "smoke1234567890",
            "hostname": "gpu4090",
            "timestamp": "2026-07-01T11:30:00",
        }).encode(),
    }
    items = []
    verified = []
    for name, payload in artifacts.items():
        remote_path = f"{remote_leaf}/{name}"
        local_path = f"{local_leaf}/{name}"
        _write(repo / local_path, payload)
        item = {
            "source_node": "gpu4090",
            "remote_path": remote_path,
            "local_path": local_path,
            "sha256": _sha(payload),
        }
        items.append(item)
        verified.append({"path": remote_path, "sha256": _sha(payload), "local_path": local_path})

    _write(
        sync_dir / "last_preflight.json",
        json.dumps({
            "generated_at": "2026-07-01T11:00:00",
            "mode": "preflight",
            "status": "ready",
            "summary": {"peers": 1, "ready": 1, "blocked": 0, "errors": 0, "warnings": 0},
            "report_path": ".syncmate/last_preflight.json",
            "peers": {"gpu4090": {"status": "ready", "ready": True}},
        }).encode(),
    )
    _write(
        sync_dir / "remote_status_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:05:00",
            "node_id": "gpu4090",
            "summary": {"device_id": "gpu4090", "role": "runner", "result_leaves": 1, "git_short_sha": "s"},
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_diff_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:10:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 3, "remote_leaves": 1, "missing": 0, "conflicts": 0, "to_fetch": 0},
            "missing": [],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_collect_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:20:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 3, "remote_leaves": 1, "missing_fetched": 3, "verified": 3, "conflicts": 0},
            "fetched": verified,
            "verification_failed": [],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_verify_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:30:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {
                "remote_files": 3,
                "remote_leaves": 1,
                "remote_incomplete": 0,
                "verified_current": 3,
                "missing": 0,
                "conflicts": 0,
                "status": "verified",
            },
            "verified": verified,
            "missing": [],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    index = {
        "version": 0,
        "updated_at": "2026-07-01T11:30:00",
        "errors": [],
        "peers": {
            "gpu4090": {
                "node_id": "gpu4090",
                "updated_at": "2026-07-01T11:30:00",
                "landing": "results/runs/gpu4090",
                "source_report": ".syncmate/last_verify_gpu4090.json",
                "summary": {
                    "remote_files": 3,
                    "remote_leaves": 1,
                    "remote_incomplete": 0,
                    "indexed": 3,
                    "missing": 0,
                    "conflicts": 0,
                    "status": "verified",
                },
                "items": items,
            },
        },
    }
    _write(sync_dir / "artifact_index.json", json.dumps(index).encode())
    _index.write_results_table_files(_index.results_payload_from_index(index))

    assert _run_cli(["--config", str(config_path), "acceptance", "gpu4090", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    saved = json.loads((sync_dir / "acceptance.json").read_text(encoding="utf-8"))

    assert out["mode"] == "acceptance"
    assert out["acceptance_path"] == ".syncmate/acceptance.json"
    assert out["ready"] is True
    assert out["status"] == "ready"
    assert out["landing_rule"] == "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/"
    assert out["automation_core"]["totals"]["fetched_missing"] == 3
    assert out["automation_core"]["totals"]["checksum_verified"] == 3
    assert out["automation_core"]["results"]["rows"] == 1
    assert out["gate"]["passed"] is True
    assert saved["acceptance_path"] == ".syncmate/acceptance.json"
    assert saved["ready"] is True

