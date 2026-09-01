from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


from scripts.syncmate import syncmate as sm


def test_default_implementation_is_core_backed_exact_entry():
    assert Path(sm.__file__).name == "syncmate.py"
    assert Path(sm.implementation_file).parent.name == "syncmate_core"
    assert Path(sm.compatibility_entry_file).resolve() == Path(sm.__file__).resolve()


def test_direct_syncmate_script_bootstraps_repo_import_path(tmp_path):
    script = Path(sm.__file__).resolve()
    repo = script.parents[2]
    probe = (
        "import os,runpy,sys; "
        "repo=os.path.abspath(sys.argv[2]); "
        "sys.path=[p for p in sys.path if os.path.abspath(p or os.getcwd()) != repo]; "
        "scope=runpy.run_path(sys.argv[1],run_name='syncmate_probe'); "
        "import experiments; "
        "assert str(scope['REPO_ROOT']) in sys.path"
    )

    completed = subprocess.run(
        [sys.executable, "-c", probe, str(script), str(repo)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr


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


def test_report_age_and_stale_detection(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-02T12:00:00")

    assert sm.report_age_hours("2026-07-02T06:00:00") == 6
    assert sm.format_age("2026-07-02T06:00:00") == "6.0h"
    assert not sm.is_report_stale("2026-07-02T06:00:00")
    assert sm.is_report_stale("2026-07-01T06:00:00")
    assert sm.format_age("not-a-time") == "unknown"


def test_remote_shell_commands_quote_repo_paths_and_roots():
    repo_path = "/tmp/Open GU/repo's copy"
    roots = ["results/runs/cora GCN", "results/runs/weird'cell"]

    status_cmd = sm.remote_status_command(repo_path)
    manifest_cmd = sm.remote_manifest_command(
        repo_path,
        roots,
        ("attack.json", "predictions.npz", "weird'name.json"),
    )
    tar_cmd = sm.remote_tar_command(repo_path)

    assert "cd '/tmp/Open GU/repo'\"'\"'s copy'" in status_cmd
    assert "cd '/tmp/Open GU/repo'\"'\"'s copy'" in manifest_cmd
    assert "'results/runs/cora GCN'" in manifest_cmd
    assert "'results/runs/weird'\"'\"'cell'" in manifest_cmd
    assert "--include attack.json predictions.npz 'weird'\"'\"'name.json'" in manifest_cmd
    assert "cd '/tmp/Open GU/repo'\"'\"'s copy' && tar czf - -T -" == tar_cmd


def test_remote_status_and_manifest_use_quoted_commands(monkeypatch):
    calls = []

    def fake_check_output(cmd, stderr=None):
        calls.append((cmd, stderr))
        if "manifest" in cmd[2]:
            return b'{"items": [], "count": 0}'
        return b'{"device": {"id": "remote"}}'

    monkeypatch.setattr(sm.subprocess, "check_output", fake_check_output)

    status = sm.remote_status_snapshot("ssh-host", "/tmp/Open GU/repo's copy")
    manifest = sm.remote_manifest(
        "ssh-host",
        "/tmp/Open GU/repo's copy",
        ["results/runs/cora GCN"],
        ("attack.json", "predictions.npz"),
    )

    assert status["device"]["id"] == "remote"
    assert manifest["count"] == 0
    assert calls[0][0][0:2] == ["ssh", "ssh-host"]
    assert "cd '/tmp/Open GU/repo'\"'\"'s copy'" in calls[0][0][2]
    assert "'results/runs/cora GCN'" in calls[1][0][2]
    assert "--include attack.json predictions.npz" in calls[1][0][2]
    assert calls[0][1] == subprocess.STDOUT


def test_remote_status_and_manifest_use_configured_python_executable(monkeypatch):
    calls = []

    def fake_check_output(cmd, stderr=None):
        calls.append(cmd)
        if "manifest" in cmd[2]:
            return b'{"items": [], "count": 0}'
        return b'{"device": {"id": "remote"}}'

    monkeypatch.setattr(sm.subprocess, "check_output", fake_check_output)

    python_executable = "/root/miniconda3/bin/python"
    sm.remote_status_snapshot("ssh-host", "/repo", python_executable)
    sm.remote_manifest(
        "ssh-host",
        "/repo",
        ["results/runs"],
        ("attack.json",),
        python_executable,
    )

    assert "/root/miniconda3/bin/python scripts/syncmate/syncmate.py status" in calls[0][2]
    assert "/root/miniconda3/bin/python scripts/syncmate/syncmate.py manifest" in calls[1][2]


def test_remote_status_plan_uses_peer_python_executable(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config(
        "runner",
        "ssh-gpu",
        "/remote/repo",
        "results/runs/gpu4090",
        ["results/runs"],
        python_executable="/root/miniconda3/bin/python",
    )
    sm.add_peer_to_device(config, "gpu4090", peer)
    sm.write_device_config(config_path, config)

    assert sm.main([
        "--config", str(config_path),
        "remote-status", "gpu4090", "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["python_executable"] == "/root/miniconda3/bin/python"
    assert "/root/miniconda3/bin/python scripts/syncmate/syncmate.py status" in out["command"]


def test_scan_results_classifies_node_bare_and_nested_layouts(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    runs = repo / "results" / "runs"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runs)

    _write_leaf(runs, "gpu4090/cora_GCN_r0.05/GIF_random/seed42")
    _write_leaf(runs, "ogbn-arxiv_GCN_r0.01/GIF_random/seed42")
    _write_leaf(runs, "ablating/results/runs/cora_GAT_r0.05/GIF_im/seed212")

    result = sm.scan_results()

    assert result["nodes"]["gpu4090"]["issues"] == []
    assert result["nodes"]["gpu4090"]["cells"] == {"cora_GCN_r0.05": 1}

    assert "bare-results-layout" in result["nodes"]["bare"]["issues"]
    assert result["nodes"]["bare"]["cells"] == {"ogbn-arxiv_GCN_r0.01": 1}

    assert "nested-results-wrapper" in result["nodes"]["ablating"]["issues"]
    assert result["nodes"]["ablating"]["cells"] == {"cora_GAT_r0.05": 1}
    assert result["nodes"]["ablating"]["layouts"] == {"nested-results-wrapper": 1}


def test_scan_progress_reports_recent_logs_and_error_keywords(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    _write(repo / "log" / "GIF" / "cora" / "GCN" / "ok.log", b"epoch 1\nfinished cleanly\n")
    _write(
        repo / "log" / "GIF" / "cora" / "GCN" / "bad.log",
        b"start\nTraceback (most recent call last)\nRuntimeError: CUDA out of memory\n",
    )
    _write(repo / "log" / "GIF" / "cora" / "GCN" / "ignored.bin", b"Traceback")

    result = sm.scan_progress(limit=5, scan_limit=10)
    paths = {item["path"] for item in result["recent_logs"]}
    error = result["error_logs"][0]

    assert result["root"] == "log"
    assert result["summary"]["total_log_files"] == 2
    assert result["summary"]["error_logs"] == 1
    assert "log/GIF/cora/GCN/ok.log" in paths
    assert "log/GIF/cora/GCN/bad.log" in paths
    assert "runtimeerror" in error["keywords"]
    assert "cuda out of memory" in error["keywords"]
    assert "ignored.bin" not in paths


def test_progress_cli_returns_log_summary(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
    _write(repo / "log" / "GIF" / "cora" / "GCN" / "run.log", b"finished\n")

    assert sm.main(["--config", str(config_path), "progress", "--json"]) == 0


def test_write_state_appends_compact_history_with_delta(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    base = {
        "generated_at": "2026-07-01T11:00:00",
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"]},
        "git": {"short_sha": "abc1234", "dirty": False},
        "results": {"total_leaves": 1, "nodes": {"gpu4090": {}}},
        "progress": {"summary": {"total_log_files": 3, "error_logs": 0, "newest_age": "2m"}},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {"gpu4090": {"summary": {"indexed": 1}, "items": []}}},
    }
    later = {
        **base,
        "generated_at": "2026-07-01T11:10:00",
        "results": {"total_leaves": 4, "nodes": {"gpu4090": {}, "h800": {}}},
        "progress": {"summary": {"total_log_files": 5, "error_logs": 2, "newest_age": "1m"}},
        "remote_status": {"gpu4090": {}},
        "artifact_index": {"peers": {"gpu4090": {"summary": {"indexed": 4}, "items": []}}},
    }

    sm.write_state(base, "status")
    sm.write_state(later, "refresh")
    entries = sm.read_history(limit=10)

    assert (sync_dir / "state.json").is_file()
    assert (sync_dir / "history.jsonl").is_file()
    assert [item["event"] for item in entries] == ["status", "refresh"]
    assert entries[0]["delta"] == {}
    assert entries[1]["delta"] == {
        "indexed_artifacts": 3,
        "log_errors": 2,
        "remote_reports": 1,
        "result_leaves": 3,
    }
    assert "remote_status" not in entries[1]

    assert sm.main(["--config", str(sync_dir / "device.yaml"), "history", "--json", "--limit", "1"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["entries"][0]["event"] == "refresh"


def test_results_table_delta_tracks_added_and_changed_rows():
    previous = {
        "rows": [
            {
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "method_strategy": "GIF_im",
                "strategy": "im",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42",
                "f1_after": 0.70,
                "status": "ok",
            },
        ],
    }
    current = {
        "rows": [
            {
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "method_strategy": "GIF_im",
                "strategy": "im",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42",
                "f1_after": 0.71,
                "status": "ok",
            },
            {
                "node_id": "h800",
                "cell": "pubmed_GCN_r0.05",
                "method": "MEGU",
                "method_strategy": "MEGU_degree",
                "strategy": "degree",
                "strategy_full": "degree",
                "seed": "seed7",
                "local_leaf": "results/runs/h800/pubmed_GCN_r0.05/MEGU_degree/seed7",
                "f1_after": 0.62,
                "status": "ok",
            },
        ],
    }

    delta = sm.results_table_delta(previous, current, limit=1)

    assert delta["previous_rows"] == 1
    assert delta["current_rows"] == 2
    assert delta["added_rows"] == 1
    assert delta["changed_rows"] == 1
    assert delta["removed_rows"] == 0
    assert delta["examples"]["added"][0]["node_id"] == "h800"
    assert delta["examples"]["changed"][0]["f1_after"] == 0.71


def test_fingerprint_excludes_volatile_timestamps_by_default():
    base = {
        "generated_at": "2026-07-01T11:00:00",
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "peer_configs": {}},
        "git": {"branch": "b", "short_sha": "abc1234", "dirty": False, "status_short": []},
        "results": {"root": "results/runs", "total_leaves": 1, "nodes": {"gpu4090": {"files": {"attack.json": 1}}}},
        "progress": {"summary": {"total_log_files": 1, "error_logs": 0, "newest_age": "1m"}},
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T10:00:00",
                "summary": {"result_leaves": 1, "latest_log_age": "1m"},
                "errors": [],
            },
        },
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {
            "updated_at": "2026-07-01T10:30:00",
            "peers": {
                "gpu4090": {
                    "updated_at": "2026-07-01T10:30:00",
                    "summary": {"indexed": 1},
                    "items": [{
                        "local_path": "results/runs/gpu4090/cell/method/seed42/attack.json",
                        "remote_path": "results/runs/cell/method/seed42/attack.json",
                        "sha256": "abc",
                        "verified_at": "2026-07-01T10:30:00",
                    }],
                },
            },
        },
    }
    later = json.loads(json.dumps(base))
    later["generated_at"] = "2026-07-01T12:00:00"
    later["progress"]["summary"]["newest_age"] = "2m"
    later["remote_status"]["gpu4090"]["generated_at"] = "2026-07-01T11:00:00"
    later["remote_status"]["gpu4090"]["summary"]["latest_log_age"] = "2m"
    later["artifact_index"]["updated_at"] = "2026-07-01T11:30:00"
    later["artifact_index"]["peers"]["gpu4090"]["items"][0]["verified_at"] = "2026-07-01T11:30:00"

    first = sm.fingerprint_payload(base)
    second = sm.fingerprint_payload(later)
    audited = sm.fingerprint_payload(later, include_timestamps=True)

    assert first["token"] == second["token"]
    assert first["components"]["artifact_index"] == second["components"]["artifact_index"]
    assert audited["token"] != first["token"]


def test_fingerprint_cli_supports_expect_prefix(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main(["--config", str(config_path), "fingerprint", "--json"]) == 0
    token = json.loads(capsys.readouterr().out)["token"]
    assert sm.main(["--config", str(config_path), "fingerprint", "--expect", token[:8], "--json"]) == 0
    matched = json.loads(capsys.readouterr().out)
    assert matched["matched"] is True
    assert sm.main(["--config", str(config_path), "fingerprint", "--expect", "deadbeef", "--json"]) == 1
    mismatched = json.loads(capsys.readouterr().out)
    assert mismatched["matched"] is False


def test_compare_fingerprint_payload_reports_component_differences():
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090", "h800"]},
        "fingerprint": {
            "token": "local-token",
            "components": {
                "device": "local-device",
                "git": "same-git",
                "results": "local-results",
            },
            "counts": {"git": {"short_sha": "abc1234"}},
        },
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "report_path": ".syncmate/remote_status_gpu4090.json",
                "summary": {
                    "fingerprint": "remote-token",
                    "fingerprint_components": {
                        "device": "remote-device",
                        "git": "same-git",
                        "results": "remote-results",
                    },
                },
                "errors": [],
            },
            "h800": {
                "generated_at": "2026-07-01T11:00:00",
                "report_path": ".syncmate/remote_status_h800.json",
                "summary": {
                    "fingerprint": "remote-token-2",
                    "fingerprint_components": {
                        "device": "remote-device",
                        "git": "other-git",
                        "results": "remote-results",
                    },
                },
                "errors": [],
            },
        },
    }

    result = sm.compare_fingerprint_payload(snapshot)
    gpu = result["peers"]["gpu4090"]
    h800 = result["peers"]["h800"]

    assert result["summary"]["peers"] == 2
    assert gpu["status"] == "different"
    assert gpu["components"]["git"]["match"] is True
    assert set(gpu["different_components"]) == {"device", "results"}
    assert gpu["attention_components"] == []
    assert h800["status"] == "attention"
    assert h800["attention_components"] == ["git"]
    assert "git" in h800["action"]


def test_compare_cli_reads_saved_remote_status_fingerprint(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "local"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    _write(
        sync_dir / "remote_status_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:00:00",
            "node_id": "gpu4090",
            "summary": {
                "fingerprint": "remote-token",
                "fingerprint_components": {"git": "remote-git"},
            },
            "snapshot": {},
            "errors": [],
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "compare", "gpu4090", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    peer = out["peers"]["gpu4090"]

    assert out["mode"] == "compare"
    assert peer["remote_token"] == "remote-token"
    assert peer["status"] == "attention"
    assert peer["attention_components"] == ["git"]
    assert peer["remote_report"] == ".syncmate/remote_status_gpu4090.json"


def test_build_snapshot_includes_fingerprint_and_export_manifest(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    _write(sync_dir / "export_manifest.json", json.dumps({"mode": "export", "summary": {"leaves": 1}}).encode())

    snapshot = sm.build_snapshot(sm.build_device_config("local", "collector", str(repo)), [])

    assert snapshot["export_manifest"]["mode"] == "export"
    assert snapshot["fingerprint"]["mode"] == "fingerprint"
    assert len(snapshot["fingerprint"]["token"]) == 16
    assert "export_manifest" in snapshot["fingerprint"]["components"]


def test_publish_cli_writes_compact_status_package(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("gpu4090", "runner", str(repo), collector_hint="local")
    sm.write_device_config(config_path, config)
    _write_leaf(repo / "results" / "runs", "cora_GCN_r0.05/GIF_im/seed42")

    assert sm.main(["--config", str(config_path), "publish", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    publish_path = sync_dir / "publish_gpu4090.json"

    assert out["mode"] == "publish"
    assert out["summary"]["device_id"] == "gpu4090"
    assert out["summary"]["manifest_files"] == 3
    assert out["summary"]["manifest_leaves"] == 1
    assert out["manifest"]["count"] == 3
    assert "items" not in out["manifest"]
    assert len(out["manifest"]["sample_items"]) == 3
    assert "leaves" not in out["manifest"]["inventory"]
    assert len(out["manifest"]["inventory"]["sample_leaves"]) == 1
    assert out["git"]["status_short_count"] == 0
    assert out["publish_path"] == ".syncmate/publish_gpu4090.json"
    assert publish_path.is_file()
    saved = json.loads(publish_path.read_text(encoding="utf-8"))
    assert saved["fingerprint"]["mode"] == "fingerprint"
    assert not (sync_dir / "state.json").exists()


def test_publish_include_items_outputs_full_manifest(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("gpu4090", "runner", str(repo), collector_hint="local")
    sm.write_device_config(config_path, config)
    _write_leaf(repo / "results" / "runs", "cora_GCN_r0.05/GIF_im/seed42")

    assert sm.main(["--config", str(config_path), "publish", "--include-items", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert len(out["manifest"]["items"]) == 3
    assert "sample_items" not in out["manifest"]
    assert all("sha256" in item for item in out["manifest"]["items"])


def test_import_publish_saves_remote_status_and_compare_reads_it(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    package_path = tmp_path / "publish_gpu4090.json"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "local"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/remote/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    package = {
        "generated_at": "2026-07-01T10:00:00",
        "mode": "publish",
        "package_version": 0,
        "device": {"id": "gpu4090", "role": "runner", "repo_path": "/remote/repo"},
        "git": {"short_sha": "remote", "dirty": False, "status_short_count": 0},
        "fingerprint": {"token": "remote-token", "components": {"git": "remote-git", "results": "remote-results"}},
        "progress": {"summary": {"total_log_files": 2, "error_logs": 0, "newest_age": "4m"}},
        "results": {"root": "results/runs", "total_leaves": 1, "nodes": {"bare": {"leaves": 1}}},
        "manifest": {
            "count": 3,
            "roots": ["results/runs"],
            "inventory": {"summary": {"leaves": 1, "incomplete": 0}},
            "items": [{"path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json", "sha256": "abc"}],
        },
        "summary": {
            "device_id": "gpu4090",
            "role": "runner",
            "git_short_sha": "remote",
            "git_dirty": False,
            "fingerprint": "remote-token",
            "result_leaves": 1,
            "manifest_files": 3,
            "manifest_leaves": 1,
            "manifest_incomplete": 0,
            "log_files": 2,
            "log_errors": 0,
            "latest_log_age": "4m",
        },
        "errors": [],
    }
    package_path.write_text(json.dumps(package), encoding="utf-8")

    assert sm.main(["--config", str(config_path), "import-publish", str(package_path), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    report_path = sync_dir / "remote_status_gpu4090.json"
    saved = json.loads(report_path.read_text(encoding="utf-8"))

    assert out["mode"] == "import-publish"
    assert out["known_peer"] is True
    assert out["saved"] is True
    assert out["report_path"] == ".syncmate/remote_status_gpu4090.json"
    assert saved["summary"]["fingerprint"] == "remote-token"
    assert saved["summary"]["fingerprint_components"]["git"] == "remote-git"
    assert saved["summary"]["manifest_files"] == 3
    assert saved["remote"]["transport"] == "ssh"
    assert saved["remote"]["source"] == "publish"
    assert saved["remote"]["repo_path"] == "/remote/repo"
    assert saved["snapshot"]["published_manifest"]["count"] == 3

    assert sm.main(["--config", str(config_path), "compare", "gpu4090", "--json"]) == 0
    compare = json.loads(capsys.readouterr().out)
    peer = compare["peers"]["gpu4090"]
    assert peer["remote_token"] == "remote-token"
    assert peer["remote_report"] == ".syncmate/remote_status_gpu4090.json"
    assert peer["status"] == "attention"


def test_import_publish_no_save_previews_without_writing_report(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    package_path = tmp_path / "publish_gpu4090.json"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
    package_path.write_text(json.dumps({
        "generated_at": "2026-07-01T10:00:00",
        "mode": "publish",
        "package_version": 0,
        "device": {"id": "gpu4090", "role": "runner", "repo_path": "/remote/repo"},
        "git": {"short_sha": "remote", "dirty": False},
        "fingerprint": {"token": "remote-token", "components": {"git": "remote-git"}},
        "progress": {"summary": {}},
        "results": {"total_leaves": 0, "nodes": {}},
        "manifest": {"count": 0, "inventory": {"summary": {}}},
        "summary": {"device_id": "gpu4090", "fingerprint": "remote-token"},
        "errors": [],
    }), encoding="utf-8")

    assert sm.main(["--config", str(config_path), "import-publish", str(package_path), "--no-save", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["saved"] is False
    assert out["known_peer"] is False
    assert "report_path" not in out
    assert not (sync_dir / "remote_status_gpu4090.json").exists()


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

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    for name, data in artifacts.items():
        _write(runner / leaf_rel / name, data)

    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    bundle_out = json.loads(capsys.readouterr().out)
    assert bundle_out["mode"] == "bundle"
    assert bundle_out["summary"]["manifest_files"] == 3
    assert bundle_out["summary"]["manifest_leaves"] == 1
    assert bundle_path.is_file()

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "STATE_FILE", collector_sync / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", collector_sync / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    config = sm.build_device_config("local", "collector", str(collector))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", str(runner), "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(collector_config, config)

    assert sm.main(["--config", str(collector_config), "import-bundle", str(bundle_path), "--json"]) == 0
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

    assert sm.main(["--config", str(collector_config), "results", "--write", "--check", "--json"]) == 0
    results_out = json.loads(capsys.readouterr().out)
    assert results_out["summary"]["rows"] == 1
    assert results_out["summary"]["parse_errors"] == 0
    assert results_out["rows"][0]["node_id"] == "gpu4090"
    assert results_out["rows"][0]["f1_after"] == 0.71
    assert results_out["rows"][0]["f1_drop"] == 0.09000000000000008
    assert (collector_sync / "results_table.json").is_file()
    assert (collector_sync / "results_table.csv").is_file()


def test_handoff_pack_writes_evidence_only_zip_without_raw_artifacts(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
    _write(repo / "results" / "runs" / "cell" / "method" / "seed" / "attack.json", b"raw")

    assert sm.main(["--config", str(config_path), "handoff-pack", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    pack_path = sync_dir / "handoff_pack_local.zip"

    assert out["mode"] == "handoff-pack"
    assert out["handoff_pack_path"] == ".syncmate/handoff_pack_local.zip"
    assert out["policy"]["contains_raw_artifacts"] is False
    assert out["policy"]["contains_device_setup"] is False
    assert pack_path.is_file()

    with zipfile.ZipFile(pack_path) as zf:
        names = set(zf.namelist())
        manifest = json.loads(zf.read(sm.HANDOFF_PACK_MANIFEST_NAME).decode("utf-8"))

    assert sm.HANDOFF_PACK_MANIFEST_NAME in names
    assert ".syncmate/status.html" in names
    assert ".syncmate/runbook.md" in names
    assert ".syncmate/checklist.md" in names
    assert ".syncmate/brief.md" in names
    assert ".syncmate/workflow.json" in names
    assert ".syncmate/automation_core.json" in names
    assert ".syncmate/automation_core.md" in names
    assert ".syncmate/acceptance.json" in names
    assert ".syncmate/device.yaml" not in names
    assert not any(name.startswith("results/runs/") for name in names)
    assert manifest["summary"]["files"] == out["summary"]["files"]
    assert all("sha256" in item for item in manifest["files"])

    assert sm.main(["inspect-handoff-pack", str(pack_path), "--limit", "3", "--json"]) == 0
    inspect_out = json.loads(capsys.readouterr().out)
    assert inspect_out["mode"] == "inspect-handoff-pack"
    assert inspect_out["handoff_pack_path"] == ".syncmate/handoff_pack_local.zip"
    assert inspect_out["audit"]["status"] == "ok"
    assert sm.is_sha256_hex(inspect_out["audit"]["zip_sha256"])
    assert inspect_out["audit"]["manifest_files"] == out["summary"]["files"]
    assert inspect_out["audit"]["verified_files"] == out["summary"]["files"]
    assert inspect_out["audit"]["contains_raw_artifacts"] is False
    assert inspect_out["audit"]["contains_device_setup"] is False
    assert len(inspect_out["files"]["sample"]) == 3
    assert not (sync_dir / "last_handoff_pack_inspect_local.json").exists()

    assert sm.main(["inspect-handoff-pack", str(pack_path), "--write", "--json"]) == 0
    written_inspect = json.loads(capsys.readouterr().out)
    saved_inspect = sync_dir / "last_handoff_pack_inspect_local.json"
    assert saved_inspect.is_file()
    assert written_inspect["node_id"] == "local"
    assert written_inspect["report_path"] == ".syncmate/last_handoff_pack_inspect_local.json"
    assert json.loads(saved_inspect.read_text(encoding="utf-8"))["audit"]["status"] == "ok"

    tampered_pack = tmp_path / "handoff_with_raw_artifact.zip"
    with zipfile.ZipFile(pack_path) as src, zipfile.ZipFile(tampered_pack, "w") as dst:
        for info in src.infolist():
            dst.writestr(info, src.read(info.filename))
        dst.writestr("results/runs/raw/attack.json", b"raw")

    assert sm.main(["inspect-handoff-pack", str(tampered_pack), "--json"]) == 1
    tampered_out = json.loads(capsys.readouterr().out)
    assert tampered_out["audit"]["status"] == "invalid"
    assert tampered_out["audit"]["contains_raw_artifacts"] is True
    assert any("raw results artifact" in error for error in tampered_out["errors"])

    include_setup_pack = tmp_path / "handoff_with_setup.zip"
    assert sm.main([
        "--config", str(config_path),
        "handoff-pack", "--include-setup", "--output", str(include_setup_pack), "--json",
    ]) == 0
    include_setup_out = json.loads(capsys.readouterr().out)
    with zipfile.ZipFile(include_setup_pack) as zf:
        setup_names = set(zf.namelist())

    assert include_setup_out["policy"]["contains_device_setup"] is True
    assert ".syncmate/device.yaml" in setup_names


def test_inspect_bundle_is_read_only_and_reports_audit_summary(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    runner_sync = runner / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    leaf_rel = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / leaf_rel / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / leaf_rel / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / leaf_rel / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    assert sm.main(["inspect-bundle", str(bundle_path), "--limit", "2", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "inspect-bundle"
    assert out["audit"]["status"] == "ok"
    assert out["device"]["id"] == "gpu4090"
    assert out["manifest"]["count"] == 3
    assert out["manifest"]["inventory_summary"]["leaves"] == 1
    assert len(out["manifest"]["sample_items"]) == 2
    assert out["manifest"]["items_truncated"] is True
    assert "import-bundle" in out["commands"]["dry_run"]
    assert not (runner / "results" / "runs" / "gpu4090").exists()
    assert not (runner_sync / "last_collect_gpu4090.json").exists()
    assert not (runner_sync / "last_bundle_inspect_gpu4090.json").exists()
    assert not (runner_sync / "artifact_index.json").exists()

    assert sm.main(["inspect-bundle", str(bundle_path), "--limit", "2", "--write", "--json"]) == 0
    written = json.loads(capsys.readouterr().out)
    saved_report = runner_sync / "last_bundle_inspect_gpu4090.json"
    snapshot = sm.build_snapshot(sm.build_device_config("local", "collector", str(runner)), [])
    reports = sm.peer_reports_payload(snapshot, [], node_ids=["gpu4090"], limit=2)

    assert written["report_path"] == ".syncmate/last_bundle_inspect_gpu4090.json"
    assert saved_report.is_file()
    assert snapshot["bundle_inspect_reports"]["gpu4090"]["audit"]["status"] == "ok"
    assert reports["peers"]["gpu4090"]["bundle_inspect"]["summary"]["audit_status"] == "ok"
    assert reports["peers"]["gpu4090"]["bundle_inspect"]["summary"]["manifest_files"] == 3
    assert not (runner / "results" / "runs" / "gpu4090").exists()
    assert not (runner_sync / "last_collect_gpu4090.json").exists()
    assert not (runner_sync / "artifact_index.json").exists()


def test_import_bundle_leaves_checksum_conflicts_without_overwrite(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    local_leaf = collector / "results" / "runs" / "gpu4090" / "cora_GCN_r0.05" / "GIF_im" / "seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    sm.write_device_config(collector_config, sm.build_device_config("local", "collector", str(collector)))
    _write(local_leaf / "attack.json", b'{"old": true}')

    assert sm.main(["--config", str(collector_config), "import-bundle", str(bundle_path), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["known_peer"] is False
    assert out["collect"]["summary"]["fetched"] == 2
    assert out["collect"]["summary"]["conflicts"] == 1
    assert out["verify"]["summary"]["status"] == "incomplete"
    assert out["verify"]["summary"]["conflicts"] == 1
    assert out["results"]["written"] is False
    assert out["results"]["reason"] == "verification-not-clean"
    assert (local_leaf / "attack.json").read_bytes() == b'{"old": true}'


def test_import_bundle_dry_run_does_not_extract_or_write_reports(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    sm.write_device_config(collector_config, sm.build_device_config("local", "collector", str(collector)))

    assert sm.main(["--config", str(collector_config), "import-bundle", str(bundle_path), "--dry-run", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "import-bundle-dry-run"
    assert out["dry_run"] is True
    assert out["saved"] is False
    assert out["collect"]["summary"]["to_fetch"] == 3
    assert out["collect"]["summary"]["fetched"] == 0
    assert out["collect"]["summary"]["verified"] == 0
    assert out["verify"]["summary"]["status"] == "incomplete"
    assert out["results"]["written"] is False
    assert out["results"]["reason"] == "dry-run"
    assert not (collector / "results").exists()
    assert not (collector_sync / "remote_status_gpu4090.json").exists()
    assert not (collector_sync / "last_collect_gpu4090.json").exists()
    assert not (collector_sync / "last_verify_gpu4090.json").exists()
    assert not (collector_sync / "artifact_index.json").exists()
    assert not (collector_sync / "results_table.json").exists()
    assert not (collector_sync / "results_table.csv").exists()


def test_import_bundle_dry_run_write_plan_saves_offline_diff_only(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    config = sm.build_device_config("local", "collector", str(collector))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "", str(runner), "results/runs/gpu4090", ["results/runs"], transport="local"),
    )
    sm.write_device_config(collector_config, config)

    assert sm.main([
        "--config", str(collector_config),
        "import-bundle", str(bundle_path),
        "--dry-run", "--write-plan", "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    diff_report = json.loads((collector_sync / "last_diff_gpu4090.json").read_text(encoding="utf-8"))
    remote_report = json.loads((collector_sync / "remote_status_gpu4090.json").read_text(encoding="utf-8"))
    device, warnings = sm.load_device(collector_config)
    snapshot = sm.build_snapshot(device, warnings)

    assert out["mode"] == "import-bundle-dry-run"
    assert out["dry_run"] is True
    assert out["saved"] is False
    assert out["plan_saved"] is True
    assert out["plan_report_path"] == ".syncmate/last_diff_gpu4090.json"
    assert out["remote_status_report_path"] == ".syncmate/remote_status_gpu4090.json"
    assert diff_report["mode"] == "import-bundle-dry-run"
    assert diff_report["summary"]["missing"] == 3
    assert diff_report["summary"]["to_fetch"] == 3
    assert remote_report["bundle"]["manifest_count"] == 3
    assert snapshot["diff_reports"]["gpu4090"]["summary"]["missing"] == 3
    assert not (collector / "results").exists()
    assert not (collector_sync / "last_collect_gpu4090.json").exists()
    assert not (collector_sync / "last_verify_gpu4090.json").exists()
    assert not (collector_sync / "artifact_index.json").exists()
    assert not (collector_sync / "results_table.json").exists()
    assert not (collector_sync / "results_table.csv").exists()


def test_import_bundle_rejects_corrupt_member_before_landing(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    corrupt_bundle = tmp_path / "bundle_gpu4090_corrupt.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    with zipfile.ZipFile(bundle_path) as zf:
        manifest = json.loads(zf.read(sm.BUNDLE_MANIFEST_NAME).decode("utf-8"))
    with zipfile.ZipFile(corrupt_bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(sm.BUNDLE_MANIFEST_NAME, json.dumps(manifest))
        for item in manifest["manifest"]["items"]:
            path = item["path"]
            if path.endswith("attack.json"):
                zf.writestr(path, b'{"corrupt": true}')
            else:
                zf.writestr(path, (runner / path).read_bytes())

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    sm.write_device_config(collector_config, sm.build_device_config("local", "collector", str(collector)))

    assert sm.main(["--config", str(collector_config), "import-bundle", str(corrupt_bundle), "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    local_leaf = collector / "results" / "runs" / "gpu4090" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    index = json.loads((collector_sync / "artifact_index.json").read_text(encoding="utf-8"))

    assert any("bundle checksum mismatch" in error for error in out["errors"])
    assert out["collect"]["summary"]["fetched"] == 2
    assert out["collect"]["summary"]["verification_failed"] == 1
    assert out["verify"]["summary"]["status"] == "incomplete"
    assert out["results"]["written"] is False
    assert out["results"]["reason"] == "verification-not-clean"
    assert not (local_leaf / "attack.json").exists()
    assert (local_leaf / "collateral.json").is_file()
    assert (local_leaf / "_meta.json").is_file()
    assert index["peers"]["gpu4090"]["summary"]["indexed"] == 2
    assert index["peers"]["gpu4090"]["summary"]["status"] == "incomplete"


def test_import_bundle_rejects_duplicate_manifest_path_before_extract(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    collector = tmp_path / "collector"
    runner_sync = runner / ".syncmate"
    collector_sync = collector / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    collector_config = collector_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    duplicate_bundle = tmp_path / "bundle_gpu4090_duplicate.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    with zipfile.ZipFile(bundle_path) as zf:
        manifest = json.loads(zf.read(sm.BUNDLE_MANIFEST_NAME).decode("utf-8"))
    manifest["manifest"]["items"].append(dict(manifest["manifest"]["items"][0]))
    manifest["manifest"]["count"] = len(manifest["manifest"]["items"])
    with zipfile.ZipFile(duplicate_bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(sm.BUNDLE_MANIFEST_NAME, json.dumps(manifest))
        for item in manifest["manifest"]["items"]:
            path = item["path"]
            if path not in zf.namelist():
                zf.writestr(path, (runner / path).read_bytes())

    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", collector_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", collector_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "collector"})
    sm.write_device_config(collector_config, sm.build_device_config("local", "collector", str(collector)))

    assert sm.main(["--config", str(collector_config), "import-bundle", str(duplicate_bundle), "--json"]) == 1
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "import-bundle-invalid"
    assert out["bundle_audit"]["status"] == "invalid"
    assert any("duplicate item path" in error for error in out["bundle_audit"]["errors"])
    assert not (collector / "results").exists()
    assert not (collector_sync / "artifact_index.json").exists()
    assert not (collector_sync / "last_collect_gpu4090.json").exists()
    assert not (collector_sync / "last_verify_gpu4090.json").exists()


def test_inspect_bundle_reports_invalid_manifest_without_extracting(tmp_path, monkeypatch, capsys):
    runner = tmp_path / "runner"
    runner_sync = runner / ".syncmate"
    runner_config = runner_sync / "device.yaml"
    bundle_path = tmp_path / "bundle_gpu4090.zip"
    duplicate_bundle = tmp_path / "bundle_gpu4090_duplicate.zip"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"

    monkeypatch.setattr(sm, "REPO_ROOT", runner)
    monkeypatch.setattr(sm, "SYNC_DIR", runner_sync)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runner / "results" / "runs")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", runner_config)
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "runner"})
    sm.write_device_config(runner_config, sm.build_device_config("gpu4090", "runner", str(runner), collector_hint="local"))
    _write(runner / remote_leaf / "attack.json", b'{"results": {"im": {"f1_after": 0.71}}}')
    _write(runner / remote_leaf / "collateral.json", b'{"results": [{"strategy": "im", "perf_before": 0.8}]}')
    _write(runner / remote_leaf / "_meta.json", b'{"git_sha": "abcdef123"}')
    assert sm.main(["--config", str(runner_config), "bundle", "--output", str(bundle_path), "--json"]) == 0
    capsys.readouterr()

    with zipfile.ZipFile(bundle_path) as zf:
        manifest = json.loads(zf.read(sm.BUNDLE_MANIFEST_NAME).decode("utf-8"))
    manifest["manifest"]["items"].append(dict(manifest["manifest"]["items"][0]))
    manifest["manifest"]["count"] = len(manifest["manifest"]["items"])
    with zipfile.ZipFile(duplicate_bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(sm.BUNDLE_MANIFEST_NAME, json.dumps(manifest))
        for item in manifest["manifest"]["items"]:
            path = item["path"]
            if path not in zf.namelist():
                zf.writestr(path, (runner / path).read_bytes())

    assert sm.main(["inspect-bundle", str(duplicate_bundle), "--json"]) == 1
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "inspect-bundle"
    assert out["audit"]["status"] == "invalid"
    assert any("duplicate item path" in error for error in out["errors"])
    assert not (runner / "results" / "runs" / "gpu4090").exists()
    assert not (runner_sync / "artifact_index.json").exists()


def test_manifest_hashes_only_json_meta_artifacts(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "git_state", lambda: {"short_sha": "testsha", "dirty": False})

    leaf = repo / "results" / "runs" / "cora_GCN_r0.05" / "GIF_random" / "seed42"
    _write(leaf / "attack.json", b"attack")
    _write(leaf / "collateral.json", b"collateral")
    _write(leaf / "_meta.json", b"meta")
    _write(leaf / "predictions.npz", b"ignored")

    manifest = sm.manifest_for_roots(["results/runs/cora_GCN_r0.05"])

    assert manifest["count"] == 3
    assert manifest["artifact_policy"]["include"] == ["attack.json", "collateral.json", "_meta.json"]
    assert manifest["inventory"]["summary"]["leaves"] == 1
    assert manifest["inventory"]["summary"]["complete"] == 1
    assert manifest["inventory"]["summary"]["incomplete"] == 0
    by_name = {Path(item["path"]).name: item for item in manifest["items"]}
    assert set(by_name) == {"attack.json", "collateral.json", "_meta.json"}
    assert by_name["attack.json"]["sha256"] == _sha(b"attack")


def test_manifest_inventory_flags_incomplete_remote_leaf(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "git_state", lambda: {"short_sha": "testsha", "dirty": False})

    leaf = repo / "results" / "runs" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    _write(leaf / "attack.json", b"attack")

    manifest = sm.manifest_for_roots(["results/runs/cora_GCN_r0.05"])
    inventory = manifest["inventory"]

    assert inventory["summary"]["leaves"] == 1
    assert inventory["summary"]["complete"] == 0
    assert inventory["summary"]["incomplete"] == 1
    assert inventory["leaves"][0]["cell"] == "cora_GCN_r0.05"
    assert inventory["leaves"][0]["method_strategy"] == "GIF_im"
    assert inventory["leaves"][0]["missing"] == ["collateral.json", "_meta.json"]


def test_manifest_can_include_predictions_when_requested(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "git_state", lambda: {"short_sha": "testsha", "dirty": False})

    leaf = repo / "results" / "runs" / "cora_GCN_r0.05" / "GIF_random" / "seed42"
    _write(leaf / "attack.json", b"attack")
    _write(leaf / "predictions.npz", b"predictions")

    manifest = sm.manifest_for_roots(
        ["results/runs/cora_GCN_r0.05"],
        ("attack.json", "predictions.npz"),
    )

    assert manifest["count"] == 2
    assert manifest["artifact_policy"]["include"] == ["attack.json", "predictions.npz"]
    by_name = {Path(item["path"]).name: item for item in manifest["items"]}
    assert set(by_name) == {"attack.json", "predictions.npz"}
    assert by_name["predictions.npz"]["sha256"] == _sha(b"predictions")


def test_artifact_names_for_peer_merges_global_and_peer_policy():
    device = {
        "artifact_policy": {
            "include": ["attack.json", "collateral.json", "_meta.json", "predictions.npz"],
            "exclude": ["collateral.json"],
        }
    }
    peer = {"artifact_policy": {"exclude": ["attack.json"]}}

    assert sm.artifact_names_for_peer(device, peer) == ("_meta.json", "predictions.npz")
    assert sm.artifact_names_for_peer(device, {"artifact_policy": {"include": ["predictions.npz"]}}) == (
        "predictions.npz",
    )


def test_init_device_writes_config_and_refuses_overwrite(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    config = sm.build_device_config("local", "collector", str(repo))
    sm.write_device_config(config_path, config)
    loaded, warnings = sm.load_device(config_path)

    assert warnings == []
    assert loaded["device_id"] == "local"
    assert loaded["role"] == "collector"
    assert loaded["repo_path"] == str(repo)
    assert loaded["peers"] == {}

    try:
        sm.write_device_config(config_path, sm.build_device_config("other", "runner", str(repo)))
    except SystemExit as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("expected existing device config to be protected")

    sm.write_device_config(config_path, sm.build_device_config("other", "runner", str(repo)), force=True)
    loaded, _warnings = sm.load_device(config_path)
    assert loaded["device_id"] == "other"
    assert loaded["role"] == "runner"


def test_init_device_runner_can_record_collector_hint(tmp_path):
    repo = tmp_path / "repo"
    config = sm.build_device_config("gpu4090", "runner", str(repo), collector_hint="local-laptop")

    assert config == {
        "version": 0,
        "device_id": "gpu4090",
        "role": "runner",
        "repo_path": str(repo),
        "collector_hint": "local-laptop",
    }


def test_init_device_cli_can_write_artifact_policy(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    assert sm.main([
        "--config", str(config_path),
        "init-device",
        "--device-id", "local",
        "--role", "collector",
        "--repo-path", str(repo),
        "--artifact-include", "attack.json", "_meta.json", "predictions.npz",
        "--artifact-exclude", "collateral.json",
    ]) == 0

    loaded, warnings = sm.load_device(config_path)

    assert warnings == []
    assert loaded["artifact_policy"] == {
        "include": ["attack.json", "_meta.json", "predictions.npz"],
        "exclude": ["collateral.json"],
    }
    assert sm.artifact_names_for_peer(loaded, None) == ("attack.json", "_meta.json", "predictions.npz")


def test_add_peer_cli_updates_collector_config_and_refuses_duplicate(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    assert sm.main([
        "--config", str(config_path),
        "init-device",
        "--device-id", "local",
        "--role", "collector",
        "--repo-path", str(repo),
    ]) == 0
    assert sm.main([
        "--config", str(config_path),
        "add-peer", "gpu4090",
        "--ssh", "autodl-4090",
        "--repo-path", "~/autodl-fs/OpenGU/GULib-master",
        "--python-executable", "/root/miniconda3/bin/python",
        "--result-root", "results/runs/cora_GCN_r0.05",
        "--result-root", "results/runs/cora_GAT_r0.05",
    ]) == 0

    loaded, warnings = sm.load_device(config_path)
    peer = loaded["peers"]["gpu4090"]

    assert warnings == []
    assert peer["role"] == "runner"
    assert peer["ssh"] == "autodl-4090"
    assert peer["python_executable"] == "/root/miniconda3/bin/python"
    assert peer["landing"] == "results/runs/gpu4090"
    assert peer["result_roots"] == [
        "results/runs/cora_GCN_r0.05",
        "results/runs/cora_GAT_r0.05",
    ]

    try:
        sm.main([
            "--config", str(config_path),
            "add-peer", "gpu4090",
            "--ssh", "autodl-4090",
            "--repo-path", "~/autodl-fs/OpenGU/GULib-master",
        ])
    except SystemExit as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("expected duplicate peer to be protected")


def test_add_peer_local_transport_does_not_require_ssh(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    runner = tmp_path / "runner"
    runner.mkdir()
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main([
        "--config", str(config_path),
        "add-peer", "local-runner",
        "--local",
        "--repo-path", str(runner),
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    loaded, warnings = sm.load_device(config_path)
    peer = loaded["peers"]["local-runner"]

    assert warnings == []
    assert out["peer"]["transport"] == "local"
    assert peer["transport"] == "local"
    assert peer["ssh"] == "local"
    assert peer["repo_path"] == str(runner)


def test_add_peer_cli_can_write_artifact_policy(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main([
        "--config", str(config_path),
        "add-peer", "h800",
        "--ssh", "autodl-h800",
        "--repo-path", "~/repo",
        "--artifact-include", "attack.json", "_meta.json",
        "--artifact-include", "predictions.npz",
        "--artifact-exclude", "collateral.json",
    ]) == 0

    loaded, warnings = sm.load_device(config_path)
    peer = loaded["peers"]["h800"]

    assert warnings == []
    assert peer["artifact_policy"] == {
        "include": ["attack.json", "_meta.json", "predictions.npz"],
        "exclude": ["collateral.json"],
    }
    assert sm.artifact_names_for_peer(loaded, peer) == ("attack.json", "_meta.json", "predictions.npz")


def test_artifact_policy_cli_rejects_path_entries():
    try:
        sm.artifact_policy_from_cli([["attack.json", "../escape.json"]], None)
    except SystemExit as exc:
        assert "artifact policy entries must be file names" in str(exc)
    else:
        raise AssertionError("expected unsafe artifact policy entry to be rejected")


def test_add_peer_requires_collector_role(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    sm.write_device_config(config_path, sm.build_device_config("gpu4090", "runner", str(repo)))

    try:
        sm.main([
            "--config", str(config_path),
            "add-peer", "h800",
            "--ssh", "autodl-h800",
            "--repo-path", "~/autodl-fs/OpenGU/GULib-master",
        ])
    except SystemExit as exc:
        assert "requires this device role" in str(exc)
    else:
        raise AssertionError("expected runner-side add-peer to be rejected")


def test_setup_plan_guides_missing_collector_and_peer_config(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)

    assert sm.main([
        "--config", str(config_path),
        "setup-plan",
        "--role", "collector",
        "--device-id", "local",
        "--repo-path", str(repo),
        "--peer-id", "gpu4090",
        "--peer-ssh", "autodl-4090",
        "--peer-repo-path", "/remote/repo",
        "--peer-python-executable", "/root/miniconda3/bin/python",
        "--result-root", "results/runs/cora_GCN_r0.05",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    actions = {item["id"]: item for item in out["actions"]}

    assert out["mode"] == "setup-plan"
    assert out["current"]["config_exists"] is False
    assert out["missing_inputs"] == []
    assert actions["init-current"]["status"] == "needed"
    assert actions["add-peer"]["status"] == "needed"
    assert "init-device --device-id local --role collector" in actions["init-current"]["command"]
    assert "add-peer gpu4090 --ssh autodl-4090 --repo-path /remote/repo" in actions["add-peer"]["command"]
    assert "--python-executable /root/miniconda3/bin/python" in actions["add-peer"]["command"]
    assert "/root/miniconda3/bin/python scripts/syncmate/syncmate.py init-device" in actions["init-runner"]["command"]
    assert "sync gpu4090 --dry-run" in actions["sync-dry-run"]["command"]


def test_setup_plan_can_generate_local_peer_commands(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)

    assert sm.main([
        "--config", str(config_path),
        "setup-plan",
        "--role", "collector",
        "--device-id", "local",
        "--repo-path", str(repo),
        "--peer-id", "local-runner",
        "--peer-local",
        "--peer-repo-path", "../GULib-runner-copy",
        "--result-root", "results/runs",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    actions = {item["id"]: item for item in out["actions"]}

    assert out["target"]["peer_transport"] == "local"
    assert out["target"]["peer_ssh"] is None
    assert out["missing_inputs"] == []
    assert "init-runner" not in actions
    assert "add-peer local-runner --local --repo-path ../GULib-runner-copy" in actions["add-peer"]["command"]
    assert "--ssh" not in actions["add-peer"]["command"]
    assert "sync local-runner --dry-run" in actions["sync-dry-run"]["command"]


def test_setup_plan_local_peer_does_not_require_ssh_input(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)

    assert sm.main([
        "--config", str(config_path),
        "setup-plan",
        "--role", "collector",
        "--peer-id", "local-runner",
        "--peer-local",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert "peer_repo_path" in out["missing_inputs"]
    assert "peer_ssh" not in out["missing_inputs"]
    assert out["target"]["peer_repo_path"] == "<local_runner_repo_path>"


def test_setup_plan_write_marks_existing_peer_not_needed(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "autodl-4090", "/remote/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    assert sm.main([
        "--config", str(config_path),
        "setup-plan",
        "--peer-id", "gpu4090",
        "--peer-ssh", "autodl-4090",
        "--peer-repo-path", "/remote/repo",
        "--write",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    actions = {item["id"]: item for item in out["actions"]}
    plan_path = sync_dir / "setup_plan.md"

    assert actions["init-current"]["status"] == "not-needed"
    assert actions["add-peer"]["status"] == "not-needed"
    assert out["setup_plan_path"] == ".syncmate/setup_plan.md"
    assert plan_path.is_file()
    text = plan_path.read_text(encoding="utf-8")
    assert "# Syncmate Setup Plan" in text
    assert "Status: not-needed" in text
    assert "sync gpu4090" in text


def test_layout_cli_shows_peer_paths_and_trusted_outputs(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config(
            "runner",
            "ssh-gpu",
            "/remote/repo",
            "results/runs/gpu4090",
            ["results/runs"],
            artifact_policy={"include": ["attack.json", "_meta.json"]},
        ),
    )
    sm.write_device_config(config_path, config)
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T06:00:00",
            "peers": {
                "gpu4090": {
                    "summary": {"indexed": 2, "status": "verified"},
                    "items": [],
                },
            },
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T06:01:00",
            "summary": {"rows": 1},
            "rows": [{"node_id": "gpu4090", "cell": "cora_GCN_r0.05"}],
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "layout", "gpu4090", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    peer = out["peers"]["gpu4090"]

    assert out["mode"] == "layout"
    assert out["local_paths"]["artifact_index"] == ".syncmate/artifact_index.json"
    assert out["local_paths"]["results_table_csv"] == ".syncmate/results_table.csv"
    assert out["local_paths"]["checklist"] == ".syncmate/checklist.md"
    assert out["local_paths"]["workflow"] == ".syncmate/workflow.json"
    assert out["local_paths"]["automation_core"] == ".syncmate/automation_core.json"
    assert out["local_paths"]["automation_core_markdown"] == ".syncmate/automation_core.md"
    assert out["local_paths"]["acceptance"] == ".syncmate/acceptance.json"
    assert peer["transport"] == "ssh"
    assert peer["remote_result_roots"] == ["results/runs"]
    assert peer["local_landing"] == "results/runs/gpu4090"
    assert peer["artifact_policy"]["include"] == ["attack.json", "_meta.json"]
    assert peer["example_mapping"]["remote"] == "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    assert peer["example_mapping"]["local"] == "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    assert peer["trusted"]["indexed_artifacts"] == 2
    assert peer["trusted"]["index_status"] == "verified"
    assert peer["trusted"]["result_rows"] == 1
    assert peer["commands"]["sync"] == "python scripts/syncmate/syncmate.py sync gpu4090"


def test_layout_text_mentions_landing_and_sync_command(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "local-runner",
        sm.build_peer_config(
            "runner",
            None,
            "../GULib-runner-copy",
            "results/runs/local-runner",
            ["results/runs"],
            transport="local",
        ),
    )
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "layout", "local-runner"]) == 0
    text = capsys.readouterr().out

    assert "syncmate layout: local (collector)" in text
    assert "transport=local landing=results/runs/local-runner" in text
    assert "results/runs/local-runner/cora_GCN_r0.05/GIF_random/seed42/attack.json" in text
    assert ".syncmate/results_table.csv" in text
    assert ".syncmate/acceptance.json" in text
    assert "python scripts/syncmate/syncmate.py sync local-runner" in text


def test_landings_cli_shows_local_landing_inventory_and_rows(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": b'{"results": {"im": {"f1_after": 0.72}}}',
        "collateral.json": b'{"results": [{"strategy": "im", "perf_before": 0.81}]}',
        "_meta.json": b'{"git_sha": "abc1234", "hostname": "gpu4090"}',
    }
    items = []
    verified = []
    for name, payload in artifacts.items():
        local_path = f"{leaf}/{name}"
        remote_path = f"{remote_leaf}/{name}"
        _write(repo / local_path, payload)
        digest = _sha(payload)
        items.append({
            "source_node": "gpu4090",
            "remote_path": remote_path,
            "local_path": local_path,
            "sha256": digest,
        })
        verified.append({"path": remote_path, "local_path": local_path, "sha256": digest})

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
            "verified": verified,
            "missing": [],
            "conflicts": [],
            "errors": [],
            "artifact_index": ".syncmate/artifact_index.json",
            "report_path": ".syncmate/last_verify_gpu4090.json",
        }).encode(),
    )
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
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
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T11:40:00",
            "mode": "results",
            "summary": {"peers": 1, "leaves": 1, "rows": 1, "complete_leaves": 1, "parse_errors": 0},
            "rows": [{
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": leaf,
                "status": "ok",
                "f1_after": 0.72,
            }],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "landings", "gpu4090", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    peer = out["peers"]["gpu4090"]

    assert out["mode"] == "landings"
    assert out["landing_rule"] == "results/runs/<node_id>/<cell>/<method_strategy>/<seed>/"
    assert out["summary"]["totals"]["result_rows"] == 1
    assert peer["state"] == "accepted"
    assert peer["landing"] == "results/runs/gpu4090"
    assert peer["landing_path"]["exists"] is True
    assert peer["counts"]["indexed"] == 3
    assert peer["inventory"]["summary"]["complete"] == 1
    assert peer["results"]["rows"] == 1
    assert peer["results"]["examples"][0]["local_leaf"] == leaf
    assert peer["commands"]["collect"] == "python scripts/syncmate/syncmate.py collect gpu4090 --apply"
    assert out["files"]["acceptance"] == ".syncmate/acceptance.json"

    assert sm.main([
        "--config", str(config_path),
        "checklist", "gpu4090", "--write", "--json",
        "--no-require-preflight", "--no-require-results",
    ]) == 0
    checklist_out = json.loads(capsys.readouterr().out)
    checklist_path = sync_dir / "checklist.md"
    checklist_text = checklist_path.read_text(encoding="utf-8")

    assert checklist_out["mode"] == "checklist"
    assert checklist_out["checklist_path"] == ".syncmate/checklist.md"
    assert checklist_out["ready"] is True
    assert checklist_out["landings"]["peers"]["gpu4090"]["landing"] == "results/runs/gpu4090"
    assert checklist_out["landings"]["peers"]["gpu4090"]["result_rows"] == 1
    assert checklist_out["landings"]["peers"]["gpu4090"]["next_command"] == "python scripts/syncmate/syncmate.py acceptance gpu4090 --write --json"
    assert "# Syncmate Checklist" in checklist_text
    assert "results/runs/gpu4090" in checklist_text
    assert ".syncmate/acceptance.json" in checklist_text


def test_runbook_cli_writes_missing_setup_guide(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    repo.mkdir()
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    assert sm.main(["--config", str(config_path), "runbook", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    runbook_path = sync_dir / "runbook.md"
    text = runbook_path.read_text(encoding="utf-8")
    commands = [item["command"] for item in out["commands"]]

    assert out["mode"] == "runbook"
    assert out["runbook_path"] == ".syncmate/runbook.md"
    assert out["device"]["setup_ready"] is False
    assert out["device"]["setup_warnings"]
    assert out["summary"]["configured_peers"] == 0
    assert "python scripts/syncmate/syncmate.py setup-plan" in commands
    assert any("init-device --role collector" in command for command in commands)
    assert runbook_path.is_file()
    assert "# Syncmate Runbook" in text
    assert "device setup missing" in text
    assert ".syncmate/runbook.md" in text


def test_runbook_cli_writes_collector_peer_flow(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"])
    peer["artifact_policy"] = {"include": ["attack.json", "_meta.json"]}
    sm.add_peer_to_device(config, "gpu4090", peer)
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "runbook", "gpu4090", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    runbook_path = sync_dir / "runbook.md"
    text = runbook_path.read_text(encoding="utf-8")
    commands = [item["command"] for item in out["commands"]]

    assert out["device"]["setup_ready"] is True
    assert out["summary"]["configured_peers"] == 1
    assert out["summary"]["selected_peers"] == 1
    assert out["peers"]["gpu4090"]["landing"] == "results/runs/gpu4090"
    assert out["peers"]["gpu4090"]["artifact_policy"]["include"] == ["attack.json", "_meta.json"]
    assert "python scripts/syncmate/syncmate.py preflight --write" in commands
    assert "python scripts/syncmate/syncmate.py sync gpu4090" in commands
    assert out["peers"]["gpu4090"]["commands"]["checklist"] == "python scripts/syncmate/syncmate.py checklist gpu4090 --write"
    assert "# Syncmate Runbook" in text
    assert "results/runs/gpu4090" in text
    assert "python scripts/syncmate/syncmate.py sync gpu4090" in text
    assert ".syncmate/checklist.md" in text


def test_smoke_cli_runs_local_end_to_end_and_keeps_workspace(tmp_path, monkeypatch, capsys):
    current = tmp_path / "current"
    current_sync = current / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", current)
    monkeypatch.setattr(sm, "SYNC_DIR", current_sync)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", current_sync / "device.yaml")
    monkeypatch.setattr(sm, "STATE_FILE", current_sync / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", current_sync / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", current / "results" / "runs")

    assert sm.main(["smoke", "--workdir", str(tmp_path / "smoke"), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    collector = Path(out["collector_root"])

    assert out["passed"] is True
    assert out["kept"] is True
    assert out["cleaned"] is False
    assert out["checks"]["preflight_ready"] is True
    assert out["checks"]["collect_checksum_ok"] is True
    assert out["checks"]["checklist_written"] is True
    assert out["checks"]["runbook_written"] is True
    assert out["checks"]["action_plan_written"] is True
    assert out["checks"]["automation_core_markdown_written"] is True
    assert out["summary"]["diff_missing"] == 3
    assert out["summary"]["collected"] == 3
    assert out["summary"]["export_leaves"] == 1
    assert out["summary"]["export_artifacts"] == 3
    assert (collector / out["files"]["local_artifact"]).is_file()
    export_manifest = json.loads(
        (collector / out["files"]["export_manifest"]).read_text(encoding="utf-8")
    )
    assert export_manifest["summary"]["leaves"] == 1
    assert export_manifest["leaves"][0]["node_id"] == "local-runner"
    assert (collector / out["files"]["acceptance"]).is_file()
    assert (collector / out["files"]["action_plan"]).is_file()
    assert (collector / out["files"]["action_plan_markdown"]).is_file()
    assert (collector / out["files"]["automation_core_markdown"]).is_file()
    assert (collector / out["files"]["checklist"]).is_file()
    assert (collector / out["files"]["runbook"]).is_file()
    acceptance = json.loads((collector / out["files"]["acceptance"]).read_text(encoding="utf-8"))
    action_plan = json.loads((collector / out["files"]["action_plan"]).read_text(encoding="utf-8"))
    assert acceptance["mode"] == "acceptance"
    assert acceptance["automation_core"]["totals"]["checksum_verified"] == 3
    assert action_plan["mode"] == "next"
    assert not current_sync.exists()
    assert sm.REPO_ROOT == current
    assert sm.SYNC_DIR == current_sync


def test_smoke_cli_cleans_temporary_workspace_by_default(tmp_path, monkeypatch, capsys):
    current = tmp_path / "current"
    current_sync = current / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", current)
    monkeypatch.setattr(sm, "SYNC_DIR", current_sync)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", current_sync / "device.yaml")
    monkeypatch.setattr(sm, "STATE_FILE", current_sync / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", current_sync / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", current / "results" / "runs")

    assert sm.main(["smoke", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["passed"] is True
    assert out["kept"] is False
    assert out["cleaned"] is True
    assert not Path(out["workdir"]).exists()
    assert not current_sync.exists()


def test_refresh_updates_all_peers_without_collecting_by_default(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "gpu4090", sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]))
    sm.add_peer_to_device(config, "h800", sm.build_peer_config("runner", "ssh-h800", "/repo", "results/runs/h800", ["results/runs"]))
    sm.write_device_config(config_path, config)

    calls = {"remote": [], "diff": [], "collect": [], "verify": []}

    def fake_remote(node_id, _ssh, _repo_path, save=True):
        calls["remote"].append((node_id, save))
        return sm.write_sync_report("remote_status", node_id, {
            "generated_at": "2026-07-01T00:00:00",
            "node_id": node_id,
            "mode": "apply",
            "summary": {"device_id": node_id, "role": "runner", "git_dirty": False, "result_leaves": 0},
            "snapshot": {"results": {"nodes": {}}},
            "errors": [],
        })

    def fake_diff(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, save=True):
        calls["diff"].append((node_id, save, artifact_names))
        return sm.write_sync_report("last_diff", node_id, {
            "generated_at": "2026-07-01T00:00:01",
            "node_id": node_id,
            "mode": "diff",
            "landing": landing,
            "summary": {"remote_files": 0, "already_current": 0, "missing": 0, "conflicts": 0, "to_fetch": 0},
            "missing": [],
            "conflicts": [],
            "errors": [],
        })

    def fake_collect(*_args, **_kwargs):
        calls["collect"].append(True)
        raise AssertionError("refresh should not collect without --apply")

    def fake_verify(*_args, **_kwargs):
        calls["verify"].append(True)
        raise AssertionError("refresh should not verify without --verify")

    monkeypatch.setattr(sm, "apply_remote_status", fake_remote)
    monkeypatch.setattr(sm, "diff_collect", fake_diff)
    monkeypatch.setattr(sm, "apply_collect", fake_collect)
    monkeypatch.setattr(sm, "verify_collect", fake_verify)

    assert sm.main(["--config", str(config_path), "refresh", "--json"]) == 0

    assert [item[0] for item in calls["remote"]] == ["gpu4090", "h800"]
    assert [item[0] for item in calls["diff"]] == ["gpu4090", "h800"]
    assert [item[2] for item in calls["diff"]] == [sm.ARTIFACT_NAMES, sm.ARTIFACT_NAMES]
    assert calls["collect"] == []
    assert calls["verify"] == []
    assert (sync_dir / "state.json").is_file()
    assert (sync_dir / "status.html").is_file()
    assert (sync_dir / "workflow.json").is_file()


def test_refresh_apply_collects_selected_peer(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "gpu4090", sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]))
    sm.add_peer_to_device(config, "h800", sm.build_peer_config("runner", "ssh-h800", "/repo", "results/runs/h800", ["results/runs"]))
    sm.write_device_config(config_path, config)

    calls = {"collect": []}

    monkeypatch.setattr(sm, "apply_remote_status", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})
    monkeypatch.setattr(sm, "diff_collect", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})

    def fake_collect(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, overwrite=False, save=True):
        calls["collect"].append((node_id, overwrite, save, landing, artifact_names))
        return {"node_id": node_id, "errors": [], "landing": landing}

    monkeypatch.setattr(sm, "apply_collect", fake_collect)

    assert sm.main(["--config", str(config_path), "refresh", "h800", "--apply", "--overwrite", "--no-dashboard", "--no-write-state", "--json"]) == 0

    assert calls["collect"] == [("h800", True, True, "results/runs/h800", sm.ARTIFACT_NAMES)]
    assert not (sync_dir / "status.html").exists()
    assert not (sync_dir / "workflow.json").exists()
    assert not (sync_dir / "state.json").exists()
    assert not (sync_dir / "history.jsonl").exists()


def test_refresh_apply_verify_runs_acceptance_for_selected_peer(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config("runner", "ssh-h800", "/repo", "results/runs/h800", ["results/runs"])
    peer["artifact_policy"] = {"include": ["attack.json", "predictions.npz"]}
    sm.add_peer_to_device(config, "h800", peer)
    sm.write_device_config(config_path, config)

    calls = {"collect": [], "verify": []}
    monkeypatch.setattr(sm, "apply_remote_status", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})
    monkeypatch.setattr(sm, "diff_collect", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})

    def fake_collect(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, overwrite=False, save=True):
        calls["collect"].append((node_id, landing, artifact_names, overwrite, save))
        return {"node_id": node_id, "errors": [], "landing": landing}

    def fake_verify(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, save=True):
        calls["verify"].append((node_id, landing, artifact_names, save))
        return {
            "node_id": node_id,
            "mode": "verify",
            "landing": landing,
            "summary": {"remote_files": 2, "verified_current": 2, "missing": 0, "conflicts": 0, "status": "verified"},
            "missing": [],
            "conflicts": [],
            "errors": [],
        }

    monkeypatch.setattr(sm, "apply_collect", fake_collect)
    monkeypatch.setattr(sm, "verify_collect", fake_verify)

    assert sm.main([
        "--config", str(config_path),
        "refresh", "h800", "--apply", "--verify", "--overwrite",
        "--no-dashboard", "--no-write-state", "--json",
    ]) == 0

    assert calls["collect"] == [("h800", "results/runs/h800", ("attack.json", "predictions.npz"), True, True)]
    assert calls["verify"] == [("h800", "results/runs/h800", ("attack.json", "predictions.npz"), True)]


def test_sync_runs_apply_verify_and_writes_receipt_brief_dashboard(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"])
    peer["artifact_policy"] = {"include": ["attack.json", "collateral.json", "_meta.json"]}
    sm.add_peer_to_device(config, "gpu4090", peer)
    sm.write_device_config(config_path, config)

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

    monkeypatch.setattr(sm, "apply_remote_status", fake_remote)
    monkeypatch.setattr(sm, "diff_collect", fake_diff)
    monkeypatch.setattr(sm, "apply_collect", fake_collect)
    monkeypatch.setattr(sm, "verify_collect", fake_verify)

    assert sm.main(["--config", str(config_path), "sync", "gpu4090", "--json"]) == 0
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


def test_sync_no_results_skips_result_table_write(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    monkeypatch.setattr(sm, "refresh_peer", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})
    monkeypatch.setattr(
        sm,
        "write_results_table_files",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("--no-results should skip table writes")),
    )

    assert sm.main([
        "--config", str(config_path),
        "sync", "gpu4090", "--no-results",
        "--no-receipt", "--no-brief", "--no-dashboard", "--no-write-state",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["results_table_path"] is None
    assert out["runbook_path"] is None
    assert out["checklist_path"] is None
    assert out["results"]["written"] is False
    assert not (sync_dir / "results_table.json").exists()
    assert not (sync_dir / "results_table.csv").exists()
    assert not (sync_dir / "runbook.md").exists()
    assert not (sync_dir / "checklist.md").exists()
    assert not (sync_dir / "workflow.json").exists()
    assert not (sync_dir / "automation_core.json").exists()
    assert not (sync_dir / "acceptance.json").exists()


def test_sync_local_transport_collects_from_same_machine_repo(tmp_path, monkeypatch, capsys):
    collector = tmp_path / "collector"
    runner = tmp_path / "runner"
    sync_dir = collector / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", collector)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", collector / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "local"})

    leaf = runner / "results" / "runs" / "cora_GCN_r0.05" / "GIF_im" / "seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.72, "mia_auc": 0.61, "selected_nodes": [1, 3]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.81, "gap": 0.04}]}).encode(),
        "_meta.json": json.dumps({"git_sha": "remote123", "hostname": "runner-local"}).encode(),
    }
    for name, data in artifacts.items():
        _write(leaf / name, data)

    config = sm.build_device_config("collector", "collector", str(collector))
    sm.add_peer_to_device(
        config,
        "local-runner",
        sm.build_peer_config(
            "runner",
            None,
            str(runner),
            "results/runs/local-runner",
            ["results/runs"],
            transport="local",
        ),
    )
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "sync", "local-runner", "--json"]) == 0
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


def test_sync_dry_run_skips_collect_verify_and_optional_writes(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    calls = {"remote": [], "diff": []}
    monkeypatch.setattr(sm, "apply_remote_status", lambda node_id, *_args, **_kwargs: calls["remote"].append(node_id) or {"node_id": node_id, "errors": []})
    monkeypatch.setattr(sm, "diff_collect", lambda node_id, *_args, **_kwargs: calls["diff"].append(node_id) or {"node_id": node_id, "landing": "results/runs/gpu4090", "summary": {"missing": 0, "conflicts": 0}, "errors": []})
    monkeypatch.setattr(sm, "apply_collect", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("dry-run should not collect")))
    monkeypatch.setattr(sm, "verify_collect", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("dry-run should not verify")))

    assert sm.main([
        "--config", str(config_path),
        "sync", "gpu4090", "--dry-run",
        "--no-receipt", "--no-brief", "--no-dashboard", "--no-write-state",
        "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert calls == {"remote": ["gpu4090"], "diff": ["gpu4090"]}
    assert out["dry_run"] is True
    assert out["apply"] is False
    assert out["verify"] is False
    assert out["receipt_path"] is None
    assert out["brief_path"] is None
    assert out["runbook_path"] is None
    assert out["checklist_path"] is None
    assert out["dashboard"] is None
    assert out["workflow"] is None
    assert not (sync_dir / "receipt_gpu4090.md").exists()
    assert not (sync_dir / "brief.md").exists()
    assert not (sync_dir / "runbook.md").exists()
    assert not (sync_dir / "checklist.md").exists()
    assert not (sync_dir / "status.html").exists()
    assert not (sync_dir / "workflow.json").exists()
    assert not (sync_dir / "state.json").exists()


def test_refresh_verify_returns_nonzero_when_acceptance_fails(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "gpu4090", sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]))
    sm.write_device_config(config_path, config)

    monkeypatch.setattr(sm, "apply_remote_status", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})
    monkeypatch.setattr(sm, "diff_collect", lambda node_id, *_args, **_kwargs: {"node_id": node_id, "errors": []})

    def fake_verify(node_id, *_args, **_kwargs):
        return {
            "node_id": node_id,
            "mode": "verify",
            "summary": {"missing": 1, "conflicts": 0, "status": "incomplete"},
            "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
            "conflicts": [],
            "errors": [],
        }

    monkeypatch.setattr(sm, "verify_collect", fake_verify)

    assert sm.main([
        "--config", str(config_path),
        "refresh", "gpu4090", "--verify",
        "--no-dashboard", "--no-write-state", "--json",
    ]) == 1


def test_apply_remote_status_saves_snapshot_summary(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    snapshot = {
        "device": {"id": "gpu4090", "role": "runner"},
        "git": {"short_sha": "abc1234", "dirty": False},
        "results": {"total_leaves": 12, "nodes": {"bare": {}, "gpu4090": {}}},
        "progress": {
            "summary": {
                "total_log_files": 9,
                "error_logs": 2,
                "newest_age": "4m",
            },
        },
    }
    monkeypatch.setattr(sm, "remote_status_snapshot", lambda *_args: snapshot)

    result = sm.apply_remote_status("gpu4090", "autodl-4090", "~/repo")

    expected_summary = {
        "device_id": "gpu4090",
        "role": "runner",
        "git_short_sha": "abc1234",
        "git_dirty": False,
        "result_leaves": 12,
        "result_nodes": ["bare", "gpu4090"],
        "log_files": 9,
        "log_errors": 2,
        "latest_log_age": "4m",
        "fingerprint": result["summary"]["fingerprint"],
        "fingerprint_components": result["summary"]["fingerprint_components"],
    }
    assert {key: result["summary"][key] for key in expected_summary} == expected_summary
    assert len(result["summary"]["fingerprint"]) == 16
    assert "results" in result["summary"]["fingerprint_components"]
    report_path = sync_dir / "remote_status_gpu4090.json"
    assert report_path.is_file()
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["snapshot"] == snapshot
    assert saved["snapshot"]["fingerprint"]["token"] == result["summary"]["fingerprint"]


def test_apply_remote_status_reports_remote_errors(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")

    def fail(_ssh, _repo_path):
        raise RuntimeError("ssh unavailable")

    monkeypatch.setattr(sm, "remote_status_snapshot", fail)

    result = sm.apply_remote_status("gpu4090", "autodl-4090", "~/repo")

    assert result["mode"] == "apply"
    assert result["errors"] == ["remote status failed: RuntimeError: ssh unavailable"]


def test_load_remote_status_reports_reads_saved_summary(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "remote": {"ssh": "autodl-4090"},
        "summary": {"device_id": "gpu4090", "result_leaves": 8},
        "errors": [],
    }
    _write(sync_dir / "remote_status_gpu4090.json", json.dumps(report).encode())

    reports = sm.load_remote_status_reports()

    assert reports["gpu4090"]["node_id"] == "gpu4090"
    assert reports["gpu4090"]["generated_at"] == "2026-07-01T00:00:00"
    assert reports["gpu4090"]["summary"]["result_leaves"] == 8
    assert reports["gpu4090"]["report_path"] == ".syncmate/remote_status_gpu4090.json"
    assert reports["gpu4090"]["snapshot"] == {}


def test_load_remote_status_reports_accepts_utf8_bom(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "summary": {"device_id": "gpu4090", "result_leaves": 8},
        "errors": [],
    }
    _write(sync_dir / "remote_status_gpu4090.json", json.dumps(report).encode("utf-8-sig"))

    reports = sm.load_remote_status_reports()

    assert reports["gpu4090"]["errors"] == []
    assert reports["gpu4090"]["summary"]["device_id"] == "gpu4090"


def test_load_collect_reports_reads_saved_summary_and_bom(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "mode": "apply",
        "landing": "results/runs/gpu4090",
        "summary": {"remote_files": 3, "already_current": 1, "verified": 2},
        "remote_inventory": {"summary": {"leaves": 1, "incomplete": 1}, "leaves": [{"missing": ["_meta.json"]}]},
        "conflicts": [{"path": "results/runs/cell/method/seed/collateral.json"}],
        "verification_failed": [],
        "errors": [],
    }
    _write(sync_dir / "last_collect_gpu4090.json", json.dumps(report).encode("utf-8-sig"))

    reports = sm.load_collect_reports()

    assert reports["gpu4090"]["node_id"] == "gpu4090"
    assert reports["gpu4090"]["summary"]["remote_files"] == 3
    assert reports["gpu4090"]["remote_inventory"]["summary"]["incomplete"] == 1
    assert len(reports["gpu4090"]["conflicts"]) == 1
    assert reports["gpu4090"]["report_path"] == ".syncmate/last_collect_gpu4090.json"


def test_load_diff_reports_reads_saved_summary_and_bom(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "mode": "diff",
        "landing": "results/runs/gpu4090",
        "summary": {"remote_files": 3, "already_current": 1, "missing": 1, "conflicts": 1},
        "remote_inventory": {"summary": {"leaves": 1, "incomplete": 1}, "leaves": [{"missing": ["_meta.json"]}]},
        "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
        "conflicts": [{"path": "results/runs/cell/method/seed/attack.json"}],
        "errors": [],
    }
    _write(sync_dir / "last_diff_gpu4090.json", json.dumps(report).encode("utf-8-sig"))

    reports = sm.load_diff_reports()

    assert reports["gpu4090"]["node_id"] == "gpu4090"
    assert reports["gpu4090"]["summary"]["missing"] == 1
    assert reports["gpu4090"]["remote_inventory"]["summary"]["incomplete"] == 1
    assert len(reports["gpu4090"]["conflicts"]) == 1
    assert reports["gpu4090"]["report_path"] == ".syncmate/last_diff_gpu4090.json"


def test_load_verify_reports_reads_saved_summary_and_bom(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "mode": "verify",
        "landing": "results/runs/gpu4090",
        "artifact_policy": {"include": ["attack.json", "_meta.json"]},
        "summary": {"remote_files": 3, "verified_current": 2, "missing": 1, "conflicts": 0},
        "remote_inventory": {"summary": {"leaves": 1, "incomplete": 1}, "leaves": [{"missing": ["_meta.json"]}]},
        "verified": [{"path": "results/runs/cell/method/seed/attack.json"}],
        "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
        "conflicts": [],
        "errors": [],
    }
    _write(sync_dir / "last_verify_gpu4090.json", json.dumps(report).encode("utf-8-sig"))

    reports = sm.load_verify_reports()

    assert reports["gpu4090"]["node_id"] == "gpu4090"
    assert reports["gpu4090"]["summary"]["verified_current"] == 2
    assert reports["gpu4090"]["artifact_policy"]["include"] == ["attack.json", "_meta.json"]
    assert reports["gpu4090"]["remote_inventory"]["summary"]["incomplete"] == 1
    assert len(reports["gpu4090"]["verified"]) == 1
    assert reports["gpu4090"]["report_path"] == ".syncmate/last_verify_gpu4090.json"


def test_load_bundle_inspect_reports_reads_saved_audit_and_bom(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "mode": "inspect-bundle",
        "bundle_path": "bundle_gpu4090.zip",
        "device": {"id": "gpu4090", "role": "runner"},
        "git": {"short_sha": "abc1234", "dirty": False},
        "fingerprint": {"token": "fp123"},
        "manifest": {"count": 3, "inventory_summary": {"leaves": 1, "incomplete": 0}},
        "audit": {"status": "ok", "errors": [], "warnings": []},
        "commands": {"import": "python scripts/syncmate/syncmate.py import-bundle bundle_gpu4090.zip"},
        "errors": [],
    }
    _write(sync_dir / "last_bundle_inspect_gpu4090.json", json.dumps(report).encode("utf-8-sig"))

    reports = sm.load_bundle_inspect_reports()

    assert reports["gpu4090"]["node_id"] == "gpu4090"
    assert reports["gpu4090"]["audit"]["status"] == "ok"
    assert reports["gpu4090"]["manifest"]["inventory_summary"]["leaves"] == 1
    assert reports["gpu4090"]["fingerprint"]["token"] == "fp123"
    assert reports["gpu4090"]["report_path"] == ".syncmate/last_bundle_inspect_gpu4090.json"


def test_compare_manifest_detects_same_missing_and_conflicts(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    landing = "results/runs/gpu4090"
    same_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    conflict_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"

    _write(sm.local_landing_path(landing, same_remote), b"same")
    _write(sm.local_landing_path(landing, conflict_remote), b"local")

    manifest = {
        "items": [
            {"path": same_remote, "sha256": _sha(b"same")},
            {"path": conflict_remote, "sha256": _sha(b"remote")},
            {"path": missing_remote, "sha256": _sha(b"missing")},
        ]
    }

    missing, same, conflicts = sm.compare_manifest(landing, manifest)

    assert [item["path"] for item in same] == [same_remote]
    assert [item["path"] for item in missing] == [missing_remote]
    assert [item["path"] for item in conflicts] == [conflict_remote]
    assert conflicts[0]["local_sha256"] == _sha(b"local")


def test_diff_collect_reports_missing_current_and_conflicts(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    landing = "results/runs/gpu4090"
    same_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    conflict_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"

    _write(sm.local_landing_path(landing, same_remote), b"same")
    _write(sm.local_landing_path(landing, conflict_remote), b"local")

    manifest = {
        "git": {"short_sha": "remote"},
        "count": 3,
        "items": [
            {"path": same_remote, "size": 4, "sha256": _sha(b"same")},
            {"path": conflict_remote, "size": 6, "sha256": _sha(b"remote")},
            {"path": missing_remote, "size": 7, "sha256": _sha(b"missing")},
        ],
    }
    calls = []

    def fake_remote_manifest(_ssh, _repo_path, _roots, artifact_names=None):
        calls.append(artifact_names)
        return manifest

    monkeypatch.setattr(sm, "remote_manifest", fake_remote_manifest)

    result = sm.diff_collect(
        "gpu4090",
        "ssh-host",
        "/repo",
        ["results/runs"],
        landing,
        artifact_names=("attack.json", "predictions.npz"),
        save=False,
    )

    assert result["summary"]["remote_files"] == 3
    assert result["summary"]["already_current"] == 1
    assert result["summary"]["missing"] == 1
    assert result["summary"]["conflicts"] == 1
    assert result["artifact_policy"]["include"] == ["attack.json", "predictions.npz"]
    assert calls == [("attack.json", "predictions.npz")]
    assert result["missing"][0]["path"] == missing_remote
    assert result["conflicts"][0]["path"] == conflict_remote


def test_diff_collect_reports_remote_inventory_incomplete(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    landing = "results/runs/gpu4090"
    attack_remote = "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    manifest = {
        "git": {"short_sha": "remote"},
        "count": 1,
        "items": [
            {"path": attack_remote, "size": 6, "sha256": _sha(b"attack")},
        ],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args: manifest)

    result = sm.diff_collect(
        "gpu4090",
        "ssh-host",
        "/repo",
        ["results/runs"],
        landing,
        artifact_names=("attack.json", "collateral.json", "_meta.json"),
        save=False,
    )

    assert result["summary"]["remote_leaves"] == 1
    assert result["summary"]["remote_incomplete"] == 1
    leaf = result["remote_inventory"]["leaves"][0]
    assert leaf["remote_leaf"] == "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    assert leaf["missing"] == ["collateral.json", "_meta.json"]


def test_diff_collect_saves_last_diff_report(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    landing = "results/runs/gpu4090"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"
    manifest = {
        "git": {"short_sha": "remote"},
        "count": 1,
        "items": [{"path": missing_remote, "size": 7, "sha256": _sha(b"missing")}],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args: manifest)

    result = sm.diff_collect("gpu4090", "ssh-host", "/repo", ["results/runs"], landing)

    assert result["report_path"] == ".syncmate/last_diff_gpu4090.json"
    assert (sync_dir / "last_diff_gpu4090.json").is_file()


def test_apply_collect_counts_only_actually_fetched_missing_artifacts(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    landing = "results/runs/gpu4090"
    fetched_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    failed_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"
    manifest = {
        "git": {"short_sha": "remote"},
        "count": 2,
        "items": [
            {"path": fetched_remote, "size": 5, "sha256": _sha(b"fetch")},
            {"path": failed_remote, "size": 4, "sha256": _sha(b"miss")},
        ],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args, **_kwargs: manifest)

    def fake_fetch(_ssh, _repo_path, items, landing_arg):
        assert [item["path"] for item in items] == [fetched_remote, failed_remote]
        target = sm.local_landing_path(landing_arg, fetched_remote)
        _write(target, b"fetch")
        return [{"path": fetched_remote, "local_path": sm.rel(target)}]

    monkeypatch.setattr(sm, "fetch_items", fake_fetch)

    result = sm.apply_collect(
        "gpu4090",
        "ssh-host",
        "/repo",
        ["results/runs"],
        landing,
        artifact_names=("attack.json", "_meta.json"),
        save=False,
    )

    assert result["summary"]["to_fetch"] == 2
    assert result["summary"]["fetched"] == 1
    assert result["summary"]["missing_fetched"] == 1
    assert result["summary"]["verified"] == 1
    assert result["summary"]["verification_failed"] == 1
    assert result["verification_failed"] == [failed_remote]
    assert result["fetched"] == [{"path": fetched_remote, "local_path": f"results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json"}]
    assert "checksum failed for 1 file(s)" in result["errors"]


def test_verify_collect_saves_acceptance_report(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    landing = "results/runs/gpu4090"
    same_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    conflict_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"

    _write(sm.local_landing_path(landing, same_remote), b"same")
    _write(sm.local_landing_path(landing, conflict_remote), b"local")

    manifest = {
        "git": {"short_sha": "remote"},
        "count": 3,
        "items": [
            {"path": same_remote, "size": 4, "sha256": _sha(b"same")},
            {"path": conflict_remote, "size": 6, "sha256": _sha(b"remote")},
            {"path": missing_remote, "size": 7, "sha256": _sha(b"missing")},
        ],
    }
    calls = []

    def fake_remote_manifest(_ssh, _repo_path, _roots, artifact_names=None):
        calls.append(artifact_names)
        return manifest

    monkeypatch.setattr(sm, "remote_manifest", fake_remote_manifest)

    result = sm.verify_collect(
        "gpu4090",
        "ssh-host",
        "/repo",
        ["results/runs"],
        landing,
        artifact_names=("attack.json", "collateral.json", "_meta.json"),
    )

    assert result["mode"] == "verify"
    assert result["summary"]["remote_files"] == 3
    assert result["summary"]["verified_current"] == 1
    assert result["summary"]["missing"] == 1
    assert result["summary"]["conflicts"] == 1
    assert result["summary"]["status"] == "incomplete"
    assert result["verified"][0]["path"] == same_remote
    assert result["missing"][0]["path"] == missing_remote
    assert result["conflicts"][0]["path"] == conflict_remote
    assert calls == [("attack.json", "collateral.json", "_meta.json")]
    assert result["report_path"] == ".syncmate/last_verify_gpu4090.json"
    assert result["artifact_index"] == ".syncmate/artifact_index.json"
    assert (sync_dir / "last_verify_gpu4090.json").is_file()
    index = json.loads((sync_dir / "artifact_index.json").read_text(encoding="utf-8"))
    entry = index["peers"]["gpu4090"]
    assert entry["summary"]["indexed"] == 1
    assert entry["summary"]["status"] == "incomplete"
    assert entry["source_report"] == ".syncmate/last_verify_gpu4090.json"
    assert entry["items"][0]["remote_path"] == same_remote
    assert entry["items"][0]["local_path"] == "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json"


def test_verify_collect_marks_remote_inventory_incomplete(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    landing = "results/runs/gpu4090"
    attack_remote = "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    _write(sm.local_landing_path(landing, attack_remote), b"attack")
    manifest = {
        "git": {"short_sha": "remote"},
        "count": 1,
        "items": [
            {"path": attack_remote, "size": 6, "sha256": _sha(b"attack")},
        ],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args: manifest)

    result = sm.verify_collect(
        "gpu4090",
        "ssh-host",
        "/repo",
        ["results/runs"],
        landing,
        artifact_names=("attack.json", "collateral.json", "_meta.json"),
        save=False,
    )

    assert result["summary"]["missing"] == 0
    assert result["summary"]["conflicts"] == 0
    assert result["summary"]["remote_incomplete"] == 1
    assert result["summary"]["status"] == "incomplete"
    assert result["verified"][0]["path"] == attack_remote
    assert "remote inventory incomplete: leaves=1" in sm.verify_result_failures(result)


def test_verify_cli_uses_peer_artifact_policy(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"])
    peer["artifact_policy"] = {"include": ["attack.json", "predictions.npz"]}
    sm.add_peer_to_device(config, "gpu4090", peer)
    sm.write_device_config(config_path, config)

    calls = []

    def fake_verify(node_id, _ssh, _repo_path, _roots, landing, *, artifact_names=None, save=True):
        calls.append((node_id, landing, artifact_names, save))
        return {
            "node_id": node_id,
            "mode": "verify",
            "landing": landing,
            "summary": {"missing": 0, "conflicts": 0, "status": "verified"},
            "missing": [],
            "conflicts": [],
            "errors": [],
        }

    monkeypatch.setattr(sm, "verify_collect", fake_verify)

    assert sm.main(["--config", str(config_path), "verify", "gpu4090", "--apply", "--no-save", "--json"]) == 0
    assert calls == [("gpu4090", "results/runs/gpu4090", ("attack.json", "predictions.npz"), False)]


def test_handoff_payload_renders_local_and_remote_ai_commands(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    device = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config(
        "runner",
        "ssh-gpu",
        "/tmp/Open GU/repo's copy",
        "results/runs/gpu4090",
        ["results/runs/cora GCN"],
    )
    peer["artifact_policy"] = {"include": ["attack.json", "predictions.npz"]}

    payload = sm.handoff_payload(device, "gpu4090", peer, config_path)
    markdown = sm.render_handoff_markdown(payload)

    assert payload["artifact_policy"]["include"] == ["attack.json", "predictions.npz"]
    assert payload["reports"]["verify"] == ".syncmate/last_verify_gpu4090.json"
    assert payload["reports"]["workflow"] == ".syncmate/workflow.json"
    assert payload["reports"]["automation_core"] == ".syncmate/automation_core.json"
    assert payload["reports"]["results_table"] == ".syncmate/results_table.json"
    assert payload["reports"]["checklist"] == ".syncmate/checklist.md"
    assert payload["reports"]["runbook"] == ".syncmate/runbook.md"
    assert payload["state"]["available"] is False
    assert "python scripts/syncmate/syncmate.py verify gpu4090 --apply" in payload["commands"]["collector"]["verify"]
    assert payload["commands"]["collector"]["workflow"] == "python scripts/syncmate/syncmate.py workflow gpu4090 --write --json"
    assert payload["commands"]["collector"]["automation_core"] == "python scripts/syncmate/syncmate.py automation-core gpu4090 --write --json"
    assert payload["commands"]["collector"]["checklist"] == "python scripts/syncmate/syncmate.py checklist gpu4090 --write"
    assert payload["commands"]["collector"]["runbook"] == "python scripts/syncmate/syncmate.py runbook gpu4090 --write"
    assert payload["commands"]["collector"]["brief"] == "python scripts/syncmate/syncmate.py brief"
    assert "import-bundle <bundle_gpu4090.zip>" in payload["commands"]["collector"]["import_bundle"]
    assert "init-device --device-id gpu4090 --role runner" in payload["commands"]["remote_agent"]["init_device"]
    assert "--collector-hint local" in payload["commands"]["remote_agent"]["init_device"]
    assert "--artifact-include attack.json predictions.npz" in payload["commands"]["remote_agent"]["init_device"]
    assert "--include attack.json predictions.npz" in payload["commands"]["remote_agent"]["manifest_json"]
    assert "python scripts/syncmate/syncmate.py bundle" in payload["commands"]["remote_agent"]["bundle"]
    assert "cd '/tmp/Open GU/repo'\"'\"'s copy'" in payload["commands"]["remote_agent"]["status_json"]
    assert "# Syncmate Handoff: gpu4090" in markdown
    assert "## Current State" in markdown
    assert "Snapshot: unavailable" in markdown
    assert "## Remote AI Commands" in markdown
    assert "init-device --device-id gpu4090 --role runner" in markdown
    assert "python scripts/syncmate/syncmate.py import-bundle <bundle_gpu4090.zip>" in markdown
    assert "python scripts/syncmate/syncmate.py bundle" in markdown
    assert "python scripts/syncmate/syncmate.py summary" in markdown
    assert "python scripts/syncmate/syncmate.py brief" in markdown
    assert "python scripts/syncmate/syncmate.py workflow gpu4090 --write --json" in markdown
    assert "python scripts/syncmate/syncmate.py automation-core gpu4090 --write --json" in markdown
    assert "python scripts/syncmate/syncmate.py checklist gpu4090 --write" in markdown
    assert "python scripts/syncmate/syncmate.py runbook gpu4090 --write" in markdown
    assert "python scripts/syncmate/syncmate.py next --require-preflight --require-verify" in markdown
    assert "python scripts/syncmate/syncmate.py inventory" in markdown
    assert "python scripts/syncmate/syncmate.py preflight --write" in markdown
    assert "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify" in markdown
    assert "results/runs/gpu4090" in markdown


def test_handoff_cli_writes_markdown_runbook(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"])
    peer["artifact_policy"] = {"include": ["attack.json", "_meta.json"]}
    sm.add_peer_to_device(config, "gpu4090", peer)
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "handoff", "gpu4090", "--write"]) == 0

    handoff_path = sync_dir / "handoff_gpu4090.md"
    assert handoff_path.is_file()
    text = handoff_path.read_text(encoding="utf-8")
    assert "# Syncmate Handoff: gpu4090" in text
    assert "## Current State" in text
    assert "Workflow: status=" in text
    assert "Automation core: status=" in text
    assert "init-device --device-id gpu4090 --role runner" in text
    assert "python scripts/syncmate/syncmate.py summary" in text
    assert "python scripts/syncmate/syncmate.py brief" in text
    assert "python scripts/syncmate/syncmate.py workflow gpu4090 --write --json" in text
    assert "python scripts/syncmate/syncmate.py automation-core gpu4090 --write --json" in text
    assert "python scripts/syncmate/syncmate.py next --require-preflight --require-verify" in text
    assert "python scripts/syncmate/syncmate.py inventory" in text
    assert "python scripts/syncmate/syncmate.py collect gpu4090 --apply" in text
    assert "python scripts/syncmate/syncmate.py verify gpu4090 --apply" in text
    assert "python scripts/syncmate/syncmate.py preflight --write" in text
    assert "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify" in text
    assert ".syncmate/automation_core.json" in text
    assert ".syncmate/checklist.md" in text
    assert ".syncmate/runbook.md" in text
    assert "--include attack.json _meta.json" in text


def test_handoff_cli_can_write_all_configured_peers(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo-gpu", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.add_peer_to_device(
        config,
        "h800",
        sm.build_peer_config("runner", "ssh-h800", "/repo-h800", "results/runs/h800", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "handoff", "--write", "--json"]) == 0

    gpu_handoff = sync_dir / "handoff_gpu4090.md"
    h800_handoff = sync_dir / "handoff_h800.md"
    all_handoff = sync_dir / "handoff_all.md"

    assert gpu_handoff.is_file()
    assert h800_handoff.is_file()
    assert all_handoff.is_file()
    text = all_handoff.read_text(encoding="utf-8")
    assert "# Syncmate Handoffs" in text
    assert "gpu4090: transport=ssh ssh=ssh-gpu" in text
    assert "h800: transport=ssh ssh=ssh-h800" in text
    assert "# Syncmate Handoff: gpu4090" in text
    assert "# Syncmate Handoff: h800" in text
    assert "## Current State" in text
    assert ".syncmate/automation_core.json" in text
    assert ".syncmate/checklist.md" in text


def test_apply_collect_fetches_only_missing_and_verifies(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    landing = "results/runs/gpu4090"
    same_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json"
    conflict_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"
    remote_bytes = {
        same_remote: b"same",
        conflict_remote: b"remote",
        missing_remote: b"missing",
    }

    _write(sm.local_landing_path(landing, same_remote), b"same")
    _write(sm.local_landing_path(landing, conflict_remote), b"local")
    manifest = {
        "git": {"short_sha": "remote"},
        "count": 3,
        "items": [
            {"path": path, "size": len(data), "sha256": _sha(data)}
            for path, data in remote_bytes.items()
        ],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args: manifest)

    fetched_paths = []

    def fake_fetch(_ssh, _repo_path, items, fetch_landing):
        for item in items:
            fetched_paths.append(item["path"])
            _write(sm.local_landing_path(fetch_landing, item["path"]), remote_bytes[item["path"]])
        return [{"path": item["path"], "local_path": str(sm.local_landing_path(fetch_landing, item["path"]))} for item in items]

    monkeypatch.setattr(sm, "fetch_items", fake_fetch)

    result = sm.apply_collect("gpu4090", "ssh-host", "/repo", ["results/runs"], landing)

    assert fetched_paths == [missing_remote]
    assert result["summary"]["already_current"] == 1
    assert result["summary"]["missing_fetched"] == 1
    assert result["summary"]["conflicts"] == 1
    assert result["summary"]["verified"] == 1
    assert result["errors"] == []
    assert sm.local_landing_path(landing, conflict_remote).read_bytes() == b"local"
    assert sm.local_landing_path(landing, missing_remote).read_bytes() == b"missing"
    assert (sync_dir / "last_collect_gpu4090.json").is_file()
    index = json.loads((sync_dir / "artifact_index.json").read_text(encoding="utf-8"))
    entry = index["peers"]["gpu4090"]
    assert entry["summary"]["indexed"] == 2
    assert entry["summary"]["status"] == "partial"
    indexed_paths = {item["remote_path"] for item in entry["items"]}
    assert indexed_paths == {same_remote, missing_remote}
    assert conflict_remote not in indexed_paths


def test_apply_collect_reports_checksum_failure(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    landing = "results/runs/gpu4090"
    missing_remote = "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"
    manifest = {
        "count": 1,
        "items": [{"path": missing_remote, "size": 7, "sha256": _sha(b"missing")}],
    }
    monkeypatch.setattr(sm, "remote_manifest", lambda *_args: manifest)

    def fake_bad_fetch(_ssh, _repo_path, items, fetch_landing):
        for item in items:
            _write(sm.local_landing_path(fetch_landing, item["path"]), b"wrong")
        return [{"path": item["path"], "local_path": str(sm.local_landing_path(fetch_landing, item["path"]))} for item in items]

    monkeypatch.setattr(sm, "fetch_items", fake_bad_fetch)

    result = sm.apply_collect("gpu4090", "ssh-host", "/repo", ["results/runs"], landing)

    assert result["summary"]["verified"] == 0
    assert result["verification_failed"] == [missing_remote]
    assert result["errors"] == ["checksum failed for 1 file(s)"]


def test_index_cli_reads_persistent_artifact_index(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sync_dir.mkdir(parents=True)
    (sync_dir / "artifact_index.json").write_text(
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T00:00:00",
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "updated_at": "2026-07-01T00:00:00",
                    "landing": "results/runs/gpu4090",
                    "source_report": ".syncmate/last_verify_gpu4090.json",
                    "summary": {"indexed": 3, "status": "verified"},
                    "items": [],
                }
            },
        }),
        encoding="utf-8",
    )

    assert sm.main(["--config", str(sync_dir / "device.yaml"), "index", "--json"]) == 0


def test_inventory_groups_indexed_artifacts_by_experiment_leaf(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    index = {
        "index_path": ".syncmate/artifact_index.json",
        "peers": {
            "gpu4090": {
                "landing": "results/runs/gpu4090",
                "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                "summary": {"indexed": 4},
                "items": [
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json",
                        "sha256": _sha(b"attack"),
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/collateral.json",
                        "sha256": _sha(b"collateral"),
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/_meta.json",
                        "sha256": _sha(b"meta"),
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_im/seed212/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed212/attack.json",
                        "sha256": _sha(b"attack2"),
                    },
                ],
            }
        },
    }

    result = sm.inventory_from_index(index)
    incomplete = sm.inventory_from_index(index, only_incomplete=True)

    assert result["summary"]["leaves"] == 2
    assert result["summary"]["complete"] == 1
    assert result["summary"]["incomplete"] == 1
    leaves = result["peers"]["gpu4090"]["leaves"]
    assert leaves[0]["cell"] == "cora_GCN_r0.05"
    assert leaves[0]["method_strategy"] == "GIF_im"
    assert leaves[0]["missing"] == ["collateral.json", "_meta.json"]
    assert leaves[1]["complete"] is True
    assert incomplete["peers"]["gpu4090"]["summary"]["shown"] == 1
    assert incomplete["peers"]["gpu4090"]["leaves"][0]["method_strategy"] == "GIF_im"
    rows = sm.inventory_csv_rows(result)
    assert rows[0]["node_id"] == "gpu4090"
    assert rows[0]["complete"] == "false"
    assert rows[0]["missing"] == "collateral.json;_meta.json"
    assert rows[1]["complete"] == "true"


def test_inventory_cli_reads_index(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sync_dir.mkdir(parents=True)
    (sync_dir / "artifact_index.json").write_text(
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T00:00:00",
            "peers": {
                "gpu4090": {
                    "landing": "results/runs/gpu4090",
                    "summary": {"indexed": 1},
                    "items": [{
                        "remote_path": "results/runs/cell/method/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cell/method/seed42/attack.json",
                        "sha256": _sha(b"attack"),
                    }],
                }
            },
        }),
        encoding="utf-8",
    )

    assert sm.main(["--config", str(sync_dir / "device.yaml"), "inventory", "--json"]) == 0
    assert sm.main(["--config", str(sync_dir / "device.yaml"), "inventory", "--csv"]) == 0
    out = capsys.readouterr().out
    assert "node_id,complete,cell,method_strategy,seed" in out
    assert "gpu4090,false,cell,method,seed42" in out


def test_export_payload_uses_complete_trusted_leaves_by_default():
    index = {
        "version": 0,
        "updated_at": "2026-07-01T00:00:00",
        "index_path": ".syncmate/artifact_index.json",
        "peers": {
            "gpu4090": {
                "landing": "results/runs/gpu4090",
                "updated_at": "2026-07-01T00:00:00",
                "source_report": ".syncmate/last_verify_gpu4090.json",
                "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                "summary": {"indexed": 4},
                "items": [
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json",
                        "sha256": _sha(b"attack"),
                        "verified_at": "2026-07-01T00:00:00",
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/collateral.json",
                        "sha256": _sha(b"collateral"),
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/_meta.json",
                        "sha256": _sha(b"meta"),
                    },
                    {
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_im/seed212/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed212/attack.json",
                        "sha256": _sha(b"attack2"),
                    },
                ],
            },
        },
        "errors": [],
    }

    result = sm.export_payload_from_index(index)
    with_incomplete = sm.export_payload_from_index(index, include_incomplete=True)
    rows = sm.export_csv_rows(result)

    assert result["mode"] == "export"
    assert result["summary"]["leaves"] == 1
    assert result["summary"]["artifacts"] == 3
    assert result["summary"]["skipped_incomplete"] == 1
    assert result["leaves"][0]["complete"] is True
    assert set(result["leaves"][0]["artifacts"]) == {"attack.json", "collateral.json", "_meta.json"}
    assert with_incomplete["summary"]["leaves"] == 2
    assert with_incomplete["summary"]["incomplete_leaves"] == 1
    assert len(rows) == 3
    assert rows[0]["node_id"] == "gpu4090"
    assert rows[0]["source_report"] == ".syncmate/last_verify_gpu4090.json"


def test_export_cli_writes_manifest_csv_and_checks_index(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.write_device_config(config_path, config)
    paths = {
        "attack.json": ("results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json", b"attack"),
        "collateral.json": ("results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/collateral.json", b"collateral"),
        "_meta.json": ("results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/_meta.json", b"meta"),
    }
    items = []
    for name, (local_path, data) in paths.items():
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

    assert sm.main(["--config", str(config_path), "export", "gpu4090", "--write", "--check", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    manifest_path = sync_dir / "export_manifest.json"
    csv_path = sync_dir / "export_manifest.csv"

    assert out["summary"]["leaves"] == 1
    assert out["index_check"]["status"] == "ok"
    assert out["written"] == {
        "manifest": ".syncmate/export_manifest.json",
        "csv": ".syncmate/export_manifest.csv",
    }
    assert manifest_path.is_file()
    assert csv_path.is_file()
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "node_id,complete,cell,method_strategy,seed,artifact,local_path" in csv_text
    assert "gpu4090,true,cora_GCN_r0.05,GIF_random,seed42,attack.json" in csv_text


def test_results_cli_extracts_metrics_from_trusted_index(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
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

    assert sm.main(["--config", str(config_path), "results", "gpu4090", "--write", "--check", "--json"]) == 0
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


def test_export_check_returns_nonzero_on_index_checksum_drift(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
    local_path = "results/runs/gpu4090/cell/method/seed42/attack.json"
    _write(repo / local_path, b"changed")
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T00:00:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "landing": "results/runs/gpu4090",
                    "artifact_policy": {"include": ["attack.json"]},
                    "summary": {"indexed": 1, "status": "verified"},
                    "items": [{
                        "remote_path": "results/runs/cell/method/seed42/attack.json",
                        "local_path": local_path,
                        "sha256": _sha(b"original"),
                    }],
                },
            },
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "export", "gpu4090", "--check", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["index_check"]["status"] == "failed"
    assert out["index_check"]["mismatched"] == 1


def test_trace_cli_shows_landing_result_chain_and_checksum_drift(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))
    local_leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": b'{"results":{"im":{"f1_after":0.72,"mia_auc":0.61}}}',
        "collateral.json": b'{"results":[{"strategy":"im","perf_before":0.80}]}',
        "_meta.json": b'{"git_sha":"abcdef123","hostname":"host-a"}',
    }
    items = []
    for name, data in artifacts.items():
        local_path = f"{local_leaf}/{name}"
        _write(repo / local_path, data)
        items.append({
            "source_node": "gpu4090",
            "remote_path": f"{remote_leaf}/{name}",
            "local_path": local_path,
            "sha256": _sha(data),
            "verified_at": "2026-07-01T11:30:00",
        })
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T11:30:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "updated_at": "2026-07-01T11:30:00",
                    "landing": "results/runs/gpu4090",
                    "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                    "source_report": ".syncmate/last_verify_gpu4090.json",
                    "summary": {"indexed": 3, "status": "verified", "missing": 0, "conflicts": 0},
                    "items": items,
                },
            },
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T11:40:00",
            "mode": "results",
            "summary": {"rows": 1, "leaves": 1, "complete_leaves": 1, "parse_errors": 0},
            "rows": [{
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "method_strategy": "GIF_im",
                "strategy": "im",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": local_leaf,
                "status": "ok",
                "f1_after": 0.72,
                "mia_auc": 0.61,
            }],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "trace", "gpu4090", "--check", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    leaf = out["leaves"][0]
    by_artifact = {item["artifact"]: item for item in leaf["artifacts"]}

    assert out["mode"] == "trace"
    assert out["summary"]["checksum_failed"] == 0
    assert leaf["status"] == "trusted-result"
    assert leaf["trusted_for_results"] is True
    assert leaf["remote_leaf"] == remote_leaf
    assert leaf["local_leaf"] == local_leaf
    assert leaf["results"]["rows"] == 1
    assert by_artifact["attack.json"]["checksum_status"] == "ok"
    assert by_artifact["attack.json"]["exists"] is True
    assert by_artifact["attack.json"]["actual_sha256"] == _sha(artifacts["attack.json"])

    _write(repo / local_leaf / "attack.json", b"changed")
    assert sm.main(["--config", str(config_path), "trace", "gpu4090", "--check", "--json"]) == 1
    drift = json.loads(capsys.readouterr().out)
    drift_leaf = drift["leaves"][0]
    drift_artifacts = {item["artifact"]: item for item in drift_leaf["artifacts"]}

    assert drift["summary"]["checksum_failed"] == 1
    assert drift_leaf["status"] == "checksum-failed"
    assert drift_artifacts["attack.json"]["checksum_status"] == "mismatch"
    assert drift_artifacts["attack.json"]["actual_sha256"] == _sha(b"changed")


def test_index_helpers_respect_explicit_empty_index(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sync_dir.mkdir(parents=True)
    (sync_dir / "artifact_index.json").write_text(
        json.dumps({
            "version": 0,
            "peers": {
                "gpu4090": {
                    "summary": {"indexed": 1},
                    "items": [{
                        "remote_path": "results/runs/cell/method/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cell/method/seed42/attack.json",
                        "sha256": _sha(b"attack"),
                    }],
                },
            },
        }),
        encoding="utf-8",
    )

    inventory = sm.inventory_from_index({})
    index_check = sm.check_artifact_index({})

    assert inventory["summary"]["peers"] == 0
    assert index_check["summary"]["peers"] == 0


def test_index_check_detects_local_drift(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T00:00:00")

    ok_path = repo / "results" / "runs" / "gpu4090" / "cell" / "method" / "seed42" / "attack.json"
    changed_path = repo / "results" / "runs" / "gpu4090" / "cell" / "method" / "seed42" / "_meta.json"
    missing_rel = "results/runs/gpu4090/cell/method/seed42/collateral.json"
    _write(ok_path, b"ok")
    _write(changed_path, b"local")
    sync_dir.mkdir(parents=True)
    (sync_dir / "artifact_index.json").write_text(
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T00:00:00",
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "updated_at": "2026-07-01T00:00:00",
                    "landing": "results/runs/gpu4090",
                    "summary": {"indexed": 4, "status": "verified"},
                    "items": [
                        {
                            "remote_path": "results/runs/cell/method/seed42/attack.json",
                            "local_path": "results/runs/gpu4090/cell/method/seed42/attack.json",
                            "sha256": _sha(b"ok"),
                        },
                        {
                            "remote_path": "results/runs/cell/method/seed42/_meta.json",
                            "local_path": "results/runs/gpu4090/cell/method/seed42/_meta.json",
                            "sha256": _sha(b"remote"),
                        },
                        {
                            "remote_path": "results/runs/cell/method/seed42/collateral.json",
                            "local_path": missing_rel,
                            "sha256": _sha(b"missing"),
                        },
                        {
                            "remote_path": "results/runs/cell/method/seed42/escape.json",
                            "local_path": "../escape.json",
                            "sha256": _sha(b"escape"),
                        },
                    ],
                }
            },
        }),
        encoding="utf-8",
    )

    result = sm.check_artifact_index()

    assert result["summary"]["status"] == "failed"
    assert result["summary"]["checked"] == 2
    assert result["summary"]["ok"] == 1
    assert result["summary"]["missing"] == 1
    assert result["summary"]["mismatched"] == 1
    assert result["summary"]["unsafe"] == 1
    assert result["missing"][0]["local_path"] == missing_rel
    assert result["mismatched"][0]["local_path"] == "results/runs/gpu4090/cell/method/seed42/_meta.json"
    assert result["unsafe"][0]["local_path"] == "../escape.json"
    assert sm.main(["--config", str(sync_dir / "device.yaml"), "index", "--check", "--json"]) == 1


def test_local_landing_path_rejects_path_escape(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    try:
        sm.local_landing_path("results/runs/gpu4090", "../../escape.json")
    except SystemExit as exc:
        assert "Unsafe target path" in str(exc)
    else:
        raise AssertionError("expected unsafe path to be rejected")


def test_local_landing_path_rejects_unsafe_landing(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    for landing in ("../outside", "/tmp/outside", "C:/tmp/outside", "~/outside"):
        try:
            sm.local_landing_path(landing, "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json")
        except SystemExit as exc:
            assert "Unsafe landing path" in str(exc)
        else:
            raise AssertionError(f"expected landing {landing!r} to be rejected")


def test_doctor_reports_actionable_layout_and_setup_diagnostics(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    runs = repo / "results" / "runs"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runs)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    _write_leaf(runs, "ablating/results/runs/cora_GAT_r0.05/GIF_im/seed212", meta_sha="aaa1111")
    snapshot = sm.build_snapshot(
        {"device_id": "dev-a", "role": "unknown", "repo_path": str(repo), "peers": {}},
        ["device setup missing: .syncmate/device.yaml"],
    )

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "setup-warning" in codes
    assert "unknown-role" in codes
    assert "nested-results-wrapper" in codes
    assert sm.status_label(snapshot, diagnostics) == "review"


def test_doctor_warns_when_verified_report_has_no_artifact_index(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "setup_warnings": [], "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": [], "short_sha": "local"},
        "results": {"nodes": {"gpu4090": {"issues": []}}},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {"peers": {}},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "artifact-index-missing" in codes


def test_doctor_warns_when_trusted_inventory_leaf_is_incomplete(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "setup_warnings": [], "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": [], "short_sha": "local"},
        "results": {"nodes": {"gpu4090": {"issues": []}}},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {
            "peers": {
                "gpu4090": {
                    "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                    "summary": {"indexed": 1, "status": "verified"},
                    "items": [{
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json",
                        "sha256": _sha(b"attack"),
                    }],
                },
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}
    inventory_warning = next(item for item in diagnostics if item["code"] == "artifact-inventory-incomplete")

    assert "artifact-inventory-incomplete" in codes
    assert inventory_warning["node"] == "gpu4090"
    assert "collateral.json=1" in inventory_warning["message"]
    assert "_meta.json=1" in inventory_warning["message"]


def test_doctor_reports_verified_remote_inventory_incomplete(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "setup_warnings": [], "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": [], "short_sha": "local"},
        "results": {"nodes": {"gpu4090": {"issues": []}}},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {
                    "status": "incomplete",
                    "missing": 0,
                    "conflicts": 0,
                    "remote_incomplete": 1,
                },
                "missing": [],
                "conflicts": [],
                "errors": [],
                "remote_inventory": {
                    "summary": {"leaves": 1, "complete": 0, "incomplete": 1},
                    "leaves": [{
                        "remote_leaf": "results/runs/cora_GCN_r0.05/GIF_im/seed42",
                        "cell": "cora_GCN_r0.05",
                        "method_strategy": "GIF_im",
                        "seed": "seed42",
                        "artifacts": ["attack.json"],
                        "missing": ["collateral.json", "_meta.json"],
                        "complete": False,
                    }],
                },
            },
        },
        "artifact_index": {"peers": {"gpu4090": {"summary": {"indexed": 0}, "items": []}}},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}
    remote_warning = next(item for item in diagnostics if item["code"] == "verify-remote-inventory-incomplete")

    assert "verify-remote-inventory-incomplete" in codes
    assert remote_warning["severity"] == "error"
    assert "collateral.json=1" in remote_warning["message"]


def test_doctor_reports_orphaned_reports_and_index_entries(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "setup_warnings": [], "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": [], "short_sha": "local"},
        "results": {"nodes": {"gpu4090": {"issues": []}}},
        "remote_status": {
            "oldpeer": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {},
                "errors": [],
                "report_path": ".syncmate/remote_status_oldpeer.json",
            }
        },
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {
            "index_path": ".syncmate/artifact_index.json",
            "peers": {
                "oldpeer": {"summary": {"indexed": 2}, "items": []},
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "orphaned-sync-report" in codes
    assert "orphaned-artifact-index" in codes
    assert sm.orphaned_sync_entries(snapshot) == [
        {"kind": "remote_status", "node_id": "oldpeer", "path": ".syncmate/remote_status_oldpeer.json"},
        {"kind": "artifact_index", "node_id": "oldpeer", "path": ".syncmate/artifact_index.json", "indexed": 2},
    ]


def test_archive_orphans_dry_run_and_apply(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(sync_dir / "device.yaml", config)
    _write(sync_dir / "remote_status_oldpeer.json", json.dumps({"generated_at": "2026-07-01T10:00:00"}).encode())
    _write(sync_dir / "last_diff_oldpeer.json", json.dumps({"generated_at": "2026-07-01T10:01:00"}).encode())
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T10:02:00",
            "peers": {
                "gpu4090": {"summary": {"indexed": 1}, "items": []},
                "oldpeer": {"summary": {"indexed": 2}, "items": []},
            },
        }).encode(),
    )

    device, warnings = sm.load_device(sync_dir / "device.yaml")
    snapshot = sm.build_snapshot(device, warnings)
    plan = sm.archive_orphaned_sync_state(snapshot, apply=False)
    next_steps = sm.next_steps_payload(snapshot, [], limit=10)

    assert plan["applied"] is False
    assert plan["summary"]["report_files"] == 2
    assert plan["summary"]["index_entries"] == 1
    assert "python scripts/syncmate/syncmate.py archive-orphans" in [
        item["command"] for item in next_steps["commands"]
    ]
    assert (sync_dir / "remote_status_oldpeer.json").is_file()
    assert (sync_dir / "last_diff_oldpeer.json").is_file()

    result = sm.archive_orphaned_sync_state(snapshot, apply=True)
    archive_dir = repo / result["archive_dir"]
    index = json.loads((sync_dir / "artifact_index.json").read_text(encoding="utf-8"))

    assert result["applied"] is True
    assert not (sync_dir / "remote_status_oldpeer.json").exists()
    assert not (sync_dir / "last_diff_oldpeer.json").exists()
    assert (archive_dir / "remote_status_oldpeer.json").is_file()
    assert (archive_dir / "last_diff_oldpeer.json").is_file()
    assert (archive_dir / "artifact_index_before_orphan_archive.json").is_file()
    assert sorted(index["peers"]) == ["gpu4090"]


def test_gate_payload_fail_thresholds_and_strict_behavior():
    snapshot = {
        "generated_at": "2026-07-01T00:00:00",
        "device": {"id": "local", "peers": []},
        "git": {"dirty": False, "status_short": []},
    }
    diagnostics = [{
        "severity": "warn",
        "code": "stale",
        "message": "stale report",
        "action": "refresh",
    }]

    default_gate = sm.gate_payload(snapshot, diagnostics)
    relaxed_gate = sm.gate_payload(snapshot, diagnostics, fail_on="error")
    strict_gate = sm.gate_payload(snapshot, diagnostics, fail_on="info")
    info_gate = sm.gate_payload(snapshot, diagnostics, fail_on="info")

    assert default_gate["passed"] is False
    assert relaxed_gate["passed"]
    assert strict_gate["passed"] is False
    assert strict_gate["failures"][0]["code"] == "stale"
    assert info_gate["passed"] is False


def test_gate_payload_requires_clean_verify_reports(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090", "h800"]},
        "git": {"dirty": False, "status_short": []},
        "artifact_index": {
            "peers": {
                "gpu4090": {
                    "summary": {"indexed": 0, "status": "verified"},
                    "items": [],
                },
            },
        },
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
    }

    result = sm.gate_payload(snapshot, [], require_verify=True)
    codes = {item["code"] for item in result["failures"]}

    assert result["passed"] is False
    assert codes == {"gate-verify-missing", "gate-index-missing"}
    assert result["failures"][0]["node"] == "h800"

    snapshot["verify_reports"]["h800"] = {
        "generated_at": "2026-07-01T11:31:00",
        "summary": {"status": "incomplete", "missing": 1, "conflicts": 0},
        "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
        "conflicts": [],
        "errors": [],
    }
    result = sm.gate_payload(snapshot, [], require_verify=True)
    codes = {item["code"] for item in result["failures"]}

    assert "gate-verify-incomplete" in codes
    assert "gate-verify-status" in codes
    assert "gate-index-missing" in codes


def test_gate_payload_requires_saved_preflight_report(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "preflight": None,
    }

    result = sm.gate_payload(snapshot, [], require_preflight=True)
    codes = {item["code"] for item in result["failures"]}

    assert result["passed"] is False
    assert result["require_preflight"] is True
    assert "gate-preflight-missing" in codes

    snapshot["preflight"] = {
        "generated_at": "2026-07-01T11:55:00",
        "status": "blocked",
        "summary": {"peers": 1, "ready": 0, "blocked": 1, "errors": 2, "warnings": 0},
        "peers": {"gpu4090": {"status": "blocked"}},
        "report_path": ".syncmate/last_preflight.json",
    }
    result = sm.gate_payload(snapshot, [], require_preflight=True)
    codes = {item["code"] for item in result["failures"]}

    assert result["passed"] is False
    assert "gate-preflight-blocked" in codes

    snapshot["preflight"] = {
        "generated_at": "2026-07-01T11:55:00",
        "status": "ready",
        "summary": {"peers": 1, "ready": 1, "blocked": 0, "errors": 0, "warnings": 0},
        "peers": {"gpu4090": {"status": "ready"}},
        "report_path": ".syncmate/last_preflight.json",
    }
    result = sm.gate_payload(snapshot, [], require_preflight=True)

    assert result["passed"] is True
    assert result["gate_diagnostics"] == []

    snapshot["device"]["peers"] = ["gpu4090", "h800"]
    result = sm.gate_payload(snapshot, [], require_preflight=True)
    codes = {item["code"] for item in result["failures"]}

    assert result["passed"] is False
    assert "gate-preflight-peer-missing" in codes


def test_gate_payload_requires_artifact_index_integrity(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    local_path = "results/runs/gpu4090/cell/method/seed42/attack.json"
    _write(repo / local_path, b"changed")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {
            "index_path": ".syncmate/artifact_index.json",
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "summary": {"indexed": 1, "status": "verified"},
                    "items": [{
                        "remote_path": "results/runs/cell/method/seed42/attack.json",
                        "local_path": local_path,
                        "sha256": _sha(b"remote"),
                    }],
                },
            },
        },
    }

    result = sm.gate_payload(snapshot, [], require_verify=True)
    codes = {item["code"] for item in result["failures"]}

    assert result["passed"] is False
    assert "gate-index-checksum-mismatch" in codes
    assert result["index_check"]["summary"]["mismatched"] == 1


def test_gate_payload_requires_trusted_results_table(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

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

    missing = sm.gate_payload(snapshot, [], require_results=True)
    missing_codes = {item["code"] for item in missing["failures"]}

    assert missing["passed"] is False
    assert missing["require_results"] is True
    assert "gate-results-missing" in missing_codes

    results_table = sm.results_payload_from_index(index)
    snapshot["results_table"] = results_table
    clean = sm.gate_payload(snapshot, [], require_results=True)

    assert clean["passed"] is True
    assert clean["results_check"]["status"] == "ok"

    stale = json.loads(json.dumps(results_table))
    stale["summary"]["rows"] = 0
    snapshot["results_table"] = stale
    failed = sm.gate_payload(snapshot, [], require_results=True)
    failed_codes = {item["code"] for item in failed["failures"]}

    assert failed["passed"] is False
    assert "gate-results-stale" in failed_codes


def test_gate_payload_rejects_incomplete_trusted_inventory(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    attack_data = b'{"attack": true}'
    local_path = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    _write(repo / local_path, attack_data)
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {
            "index_path": ".syncmate/artifact_index.json",
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "artifact_policy": {"include": ["attack.json", "collateral.json", "_meta.json"]},
                    "summary": {"indexed": 1, "status": "verified"},
                    "items": [{
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json",
                        "local_path": local_path,
                        "sha256": _sha(attack_data),
                    }],
                },
            },
        },
    }

    result = sm.gate_payload(snapshot, [], require_verify=True)
    codes = {item["code"] for item in result["failures"]}
    inventory_failure = next(item for item in result["failures"] if item["code"] == "gate-inventory-incomplete")

    assert result["passed"] is False
    assert "gate-inventory-incomplete" in codes
    assert "gate-index-checksum-mismatch" not in codes
    assert result["index_check"]["summary"]["status"] == "ok"
    assert inventory_failure["node"] == "gpu4090"
    assert "collateral.json=1" in inventory_failure["message"]


def test_gate_payload_rejects_remote_inventory_incomplete(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
                "summary": {
                    "status": "incomplete",
                    "missing": 0,
                    "conflicts": 0,
                    "remote_incomplete": 1,
                },
                "missing": [],
                "conflicts": [],
                "errors": [],
                "remote_inventory": {
                    "summary": {"leaves": 1, "complete": 0, "incomplete": 1},
                    "leaves": [{
                        "remote_leaf": "results/runs/cora_GCN_r0.05/GIF_im/seed42",
                        "cell": "cora_GCN_r0.05",
                        "method_strategy": "GIF_im",
                        "seed": "seed42",
                        "artifacts": ["attack.json"],
                        "missing": ["collateral.json", "_meta.json"],
                        "complete": False,
                    }],
                },
            },
        },
        "artifact_index": {
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "summary": {"indexed": 0, "status": "incomplete"},
                    "items": [],
                },
            },
        },
    }

    result = sm.gate_payload(snapshot, [], require_verify=True)
    codes = {item["code"] for item in result["failures"]}
    remote_failure = next(item for item in result["failures"] if item["code"] == "gate-remote-inventory-incomplete")

    assert result["passed"] is False
    assert "gate-remote-inventory-incomplete" in codes
    assert "gate-index-missing" not in codes
    assert "collateral.json=1" in remote_failure["message"]


def test_summary_payload_compacts_peer_reports_and_actions(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"]},
        "git": {"dirty": False, "status_short": []},
        "results": {"total_leaves": 10},
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {"git_short_sha": "abc1234", "git_dirty": False, "result_leaves": 12},
                "errors": [],
            },
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "summary": {"remote_files": 3, "missing": 1, "conflicts": 0},
                "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {
            "index_path": ".syncmate/artifact_index.json",
            "peers": {
                "oldpeer": {"summary": {"indexed": 1}, "items": []},
            },
        },
    }
    diagnostics = [{
        "severity": "warn",
        "code": "diff-missing",
        "node": "gpu4090",
        "message": "missing files",
        "action": "collect gpu4090 --apply",
    }]

    result = sm.summary_payload(snapshot, diagnostics, fail_on="error")

    assert result["mode"] == "summary"
    assert result["gate"]["passed"]
    assert result["totals"]["peers"] == 1
    assert result["totals"]["orphaned_sync_state"] == 1
    assert result["orphaned_sync_state"][0]["node_id"] == "oldpeer"
    assert result["peers"][0]["node_id"] == "gpu4090"
    assert result["peers"][0]["diff"]["missing"] == 1
    assert result["top_diagnostics"][0]["code"] == "diff-missing"
    assert result["next_actions"] == ["collect gpu4090 --apply"]


def test_brief_payload_and_markdown_combine_status_next_and_history(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    monkeypatch.setattr(sm, "read_history", lambda limit=5: [{
        "generated_at": "2026-07-01T11:50:00",
        "event": "refresh",
        "results": {"leaves": 9},
        "artifact_index": {"indexed": 3},
        "progress": {"log_errors": 1},
        "delta": {"result_leaves": 2},
    }])
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
        "git": {"dirty": False, "status_short": [], "short_sha": "abc1234"},
        "results": {"total_leaves": 10},
        "progress": {"summary": {"total_log_files": 4, "error_logs": 1}},
        "remote_status": {
            "gpu4090": {"generated_at": "2026-07-01T11:55:00", "summary": {}, "errors": []},
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:56:00",
                "summary": {"missing": 1, "conflicts": 0},
                "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
        "preflight": {
            "generated_at": "2026-07-01T11:40:00",
            "status": "ready",
            "summary": {"peers": 1, "ready": 1, "blocked": 0, "errors": 0, "warnings": 0},
            "report_path": ".syncmate/last_preflight.json",
        },
    }
    diagnostics = [{
        "severity": "warn",
        "code": "diff-missing",
        "node": "gpu4090",
        "message": "missing files",
        "action": "collect gpu4090 --apply",
    }]

    result = sm.brief_payload(snapshot, diagnostics, require_verify=False, limit=3)
    markdown = sm.render_brief_markdown(result)

    assert result["mode"] == "brief"
    assert result["preflight"]["status"] == "ready"
    assert result["history"][0]["event"] == "refresh"
    assert result["next_commands"][0]["command"] == "python scripts/syncmate/syncmate.py collect gpu4090 --apply"
    assert result["top_diagnostics"][0]["code"] == "diff-missing"
    assert result["workflow"]["path"] == ".syncmate/workflow.json"
    assert any(item["stage"] == "collect" for item in result["workflow"]["attention"])
    assert result["automation_core"]["status"] == "partial"
    assert result["automation_core"]["totals"]["missing"] == 1
    assert result["automation_core"]["totals"]["fetched_missing"] == 0
    assert result["acceptance"]["status"] == "pending"
    assert result["files"]["acceptance"] == ".syncmate/acceptance.json"
    assert result["files"]["action_plan"] == ".syncmate/action_plan.json"
    assert result["files"]["action_plan_markdown"] == ".syncmate/action_plan.md"
    assert "# Syncmate Brief" in markdown
    assert "## Acceptance" in markdown
    assert ".syncmate/acceptance.json" in markdown
    assert ".syncmate/action_plan.json" in markdown
    assert ".syncmate/action_plan.md" in markdown
    assert "Latest Preflight" in markdown
    assert "## Workflow" in markdown
    assert "## Automation Core" in markdown
    assert "Missing/fetched: 1/0" in markdown
    assert "delta=unavailable" in markdown
    assert "gpu4090/collect" in markdown
    assert ".syncmate/last_preflight.json" in markdown
    assert "python scripts/syncmate/syncmate.py collect gpu4090 --apply" in markdown
    assert "python scripts/syncmate/syncmate.py lifecycle --json" in markdown
    assert "python scripts/syncmate/syncmate.py next --write --require-preflight --require-verify --require-results" in markdown
    assert "delta=result_leaves=+2" in markdown


def test_brief_cli_writes_current_state_markdown(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main(["--config", str(config_path), "brief", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    brief_path = sync_dir / "brief.md"

    assert out["mode"] == "brief"
    assert out["brief_path"] == ".syncmate/brief.md"
    assert out["action_plan_path"] == ".syncmate/action_plan.json"
    assert out["action_plan_markdown_path"] == ".syncmate/action_plan.md"
    assert brief_path.is_file()
    assert (sync_dir / "action_plan.json").is_file()
    assert (sync_dir / "action_plan.md").is_file()
    action_plan = json.loads((sync_dir / "action_plan.json").read_text(encoding="utf-8"))
    text = brief_path.read_text(encoding="utf-8")
    assert action_plan["mode"] == "next"
    assert action_plan["action_plan_path"] == ".syncmate/action_plan.json"
    assert action_plan["action_plan_markdown_path"] == ".syncmate/action_plan.md"
    assert "# Syncmate Brief" in text
    assert "Status:" in text
    assert "## Workflow" in text
    assert "## Automation Core" in text
    assert "## Acceptance" in text
    assert ".syncmate/workflow.json" in text
    assert ".syncmate/automation_core.json" in text
    assert ".syncmate/acceptance.json" in text
    assert ".syncmate/action_plan.json" in text
    assert ".syncmate/action_plan.md" in text
    assert ".syncmate/checklist.md" in text
    assert not (sync_dir / "state.json").exists()
    assert not (sync_dir / "history.jsonl").exists()


def test_peer_reports_payload_compacts_report_details(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"]},
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {"git_short_sha": "abc1234", "git_dirty": False, "result_leaves": 2},
                "errors": [],
                "report_path": ".syncmate/remote_status_gpu4090.json",
            },
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "landing": "results/runs/gpu4090",
                "summary": {
                    "remote_files": 2,
                    "remote_leaves": 1,
                    "remote_incomplete": 1,
                    "missing": 2,
                    "conflicts": 1,
                },
                "remote_inventory": {
                    "summary": {"leaves": 1, "complete": 0, "incomplete": 1},
                    "leaves": [{
                        "remote_leaf": "results/runs/cora_GCN_r0.05/GIF_im/seed42",
                        "missing": ["collateral.json", "_meta.json"],
                        "complete": False,
                    }],
                },
                "missing": [
                    {"path": "results/runs/cell/method/seed/_meta.json", "sha256": "a"},
                    {"path": "results/runs/cell/method/seed/collateral.json", "sha256": "b"},
                ],
                "conflicts": [{"path": "results/runs/cell/method/seed/attack.json", "local_sha256": "local"}],
                "errors": [],
                "report_path": ".syncmate/last_diff_gpu4090.json",
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
    }
    diagnostics = [{
        "severity": "warn",
        "code": "diff-missing",
        "node": "gpu4090",
        "message": "missing files",
        "action": "collect gpu4090 --apply",
    }]

    result = sm.peer_reports_payload(snapshot, diagnostics, node_ids=["gpu4090"], limit=1)
    peer = result["peers"]["gpu4090"]

    assert result["mode"] == "reports"
    assert peer["known"] is True
    assert peer["remote"]["summary"]["git_short_sha"] == "abc1234"
    assert peer["diff"]["summary"]["remote_incomplete"] == 1
    assert len(peer["diff"]["examples"]["missing"]) == 1
    assert peer["diff"]["remote_inventory_incomplete"]["missing_counts"] == {
        "collateral.json": 1,
        "_meta.json": 1,
    }
    assert peer["diagnostics"][0]["code"] == "diff-missing"


def test_reports_cli_returns_compact_peer_json(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    _write(
        sync_dir / "last_diff_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:10:00",
            "node_id": "gpu4090",
            "mode": "diff",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 1, "remote_leaves": 1, "remote_incomplete": 1, "missing": 1, "conflicts": 0},
            "remote_inventory": {
                "summary": {"leaves": 1, "complete": 0, "incomplete": 1},
                "leaves": [{
                    "remote_leaf": "results/runs/cora_GCN_r0.05/GIF_im/seed42",
                    "missing": ["_meta.json"],
                    "complete": False,
                }],
            },
            "missing": [{"path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/_meta.json"}],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "reports", "gpu4090", "--json", "--limit", "1"]) == 0
    out = json.loads(capsys.readouterr().out)
    peer = out["peers"]["gpu4090"]

    assert out["summary"]["peers"] == 1
    assert peer["diff"]["summary"]["remote_incomplete"] == 1
    assert peer["diff"]["remote_inventory_incomplete"]["examples"][0]["remote_leaf"].endswith("seed42")
    assert len(peer["diff"]["examples"]["missing"]) == 1


def test_receipt_payload_summarizes_landing_checksums_and_local_examples(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {
            "id": "local",
            "role": "collector",
            "peers": ["gpu4090"],
            "peer_configs": {
                "gpu4090": {"landing": "results/runs/gpu4090"},
            },
        },
        "remote_status": {},
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "landing": "results/runs/gpu4090",
                "summary": {
                    "remote_files": 3,
                    "remote_leaves": 1,
                    "remote_incomplete": 0,
                    "already_current": 1,
                    "missing": 1,
                    "conflicts": 0,
                },
                "missing": [{"path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/_meta.json"}],
                "conflicts": [],
                "errors": [],
                "report_path": ".syncmate/last_diff_gpu4090.json",
            },
        },
        "collect_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:20:00",
                "landing": "results/runs/gpu4090",
                "summary": {
                    "remote_files": 3,
                    "remote_leaves": 1,
                    "remote_incomplete": 0,
                    "already_current": 1,
                    "missing_fetched": 1,
                    "verified": 2,
                    "conflicts": 0,
                },
                "fetched": [{
                    "path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/_meta.json",
                    "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/_meta.json",
                }],
                "verification_failed": [],
                "conflicts": [],
                "errors": [],
                "report_path": ".syncmate/last_collect_gpu4090.json",
                "artifact_index": ".syncmate/artifact_index.json",
            },
        },
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:30:00",
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
                "missing": [],
                "conflicts": [],
                "errors": [],
                "report_path": ".syncmate/last_verify_gpu4090.json",
                "artifact_index": ".syncmate/artifact_index.json",
            },
        },
        "artifact_index": {
            "peers": {
                "gpu4090": {
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
                    "items": [{
                        "remote_path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json",
                        "local_path": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json",
                        "sha256": "abc",
                    }],
                },
            },
        },
        "results_table": {
            "generated_at": "2026-07-01T11:40:00",
            "summary": {
                "peers": 1,
                "leaves": 1,
                "rows": 1,
                "complete_leaves": 1,
                "incomplete_leaves": 0,
                "parse_error_rows": 0,
                "parse_errors": 0,
            },
            "rows": [{
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "method_strategy": "GIF_im",
                "strategy": "im",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42",
                "status": "ok",
            }],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        },
    }

    result = sm.receipt_payload(snapshot, node_ids=["gpu4090"], limit=2)
    peer = result["peers"]["gpu4090"]
    markdown = sm.render_receipt_markdown(result)

    assert result["mode"] == "receipt"
    assert result["summary"]["accepted"] == 1
    assert peer["state"] == "accepted"
    assert peer["landing"] == "results/runs/gpu4090"
    assert peer["counts"]["fetched_missing"] == 1
    assert peer["counts"]["verified"] == 3
    assert peer["counts"]["indexed"] == 3
    assert result["automation_core"]["status"] == "ok"
    assert result["automation_core"]["totals"]["checksum_verified"] == 3
    assert result["automation_core"]["totals"]["indexed"] == 3
    assert result["automation_core"]["results"]["rows"] == 1
    assert result["automation_core"]["results"]["delta"] is None
    assert peer["examples"]["local_artifacts"][0]["local_path"].endswith("attack.json")
    assert "# Syncmate Receipt" in markdown
    assert "Automation Core" in markdown
    assert "delta=unavailable" in markdown
    assert "state=accepted" in markdown
    assert "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json" in markdown


def test_receipt_cli_writes_markdown_from_saved_reports(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    remote_path = "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    local_path = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    _write(repo / local_path, b"attack")
    _write(
        sync_dir / "last_verify_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:30:00",
            "node_id": "gpu4090",
            "mode": "verify",
            "landing": "results/runs/gpu4090",
            "summary": {
                "remote_files": 1,
                "remote_leaves": 1,
                "remote_incomplete": 0,
                "verified_current": 1,
                "missing": 0,
                "conflicts": 0,
                "status": "verified",
            },
            "verified": [{"path": remote_path, "sha256": _sha(b"attack")}],
            "missing": [],
            "conflicts": [],
            "errors": [],
            "artifact_index": ".syncmate/artifact_index.json",
        }).encode(),
    )
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
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
                        "remote_files": 1,
                        "remote_leaves": 1,
                        "remote_incomplete": 0,
                        "indexed": 1,
                        "missing": 0,
                        "conflicts": 0,
                        "status": "verified",
                    },
                    "items": [{
                        "source_node": "gpu4090",
                        "remote_path": remote_path,
                        "local_path": local_path,
                        "sha256": _sha(b"attack"),
                    }],
                },
            },
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T11:40:00",
            "mode": "results",
            "summary": {
                "peers": 1,
                "leaves": 1,
                "rows": 1,
                "complete_leaves": 1,
                "incomplete_leaves": 0,
                "parse_error_rows": 0,
                "parse_errors": 0,
            },
            "rows": [{
                "node_id": "gpu4090",
                "cell": "cora_GCN_r0.05",
                "method": "GIF",
                "method_strategy": "GIF_im",
                "strategy": "im",
                "strategy_full": "im",
                "seed": "seed42",
                "local_leaf": "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42",
                "status": "ok",
            }],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "receipt", "gpu4090", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    receipt_path = sync_dir / "receipt_gpu4090.md"

    assert out["receipt_path"] == ".syncmate/receipt_gpu4090.md"
    assert out["peers"]["gpu4090"]["state"] == "accepted"
    assert out["automation_core"]["totals"]["checksum_verified"] == 1
    assert out["automation_core"]["totals"]["indexed"] == 1
    assert out["automation_core"]["results"]["rows"] == 1
    assert out["automation_core"]["results"]["delta"] is None
    assert receipt_path.is_file()
    text = receipt_path.read_text(encoding="utf-8")
    assert "# Syncmate Receipt" in text
    assert "Automation Core" in text
    assert "delta=unavailable" in text
    assert "state=accepted" in text
    assert local_path in text


def test_summary_cli_returns_machine_readable_digest(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "summary", "--json"]) == 0


def test_overview_cli_combines_layout_gate_receipt_and_next(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    remote_leaf = "results/runs/cora_GCN_r0.05/GIF_im/seed42"
    local_leaf = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42"
    artifacts = {
        "attack.json": json.dumps({"results": {"im": {"f1_after": 0.72, "mia_auc": 0.61, "selected_nodes": [1]}}}).encode(),
        "collateral.json": json.dumps({"results": [{"strategy": "im", "perf_before": 0.81, "gap": 0.04}]}).encode(),
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
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
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
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T11:35:00",
            "mode": "results",
            "summary": {"rows": 1, "leaves": 1, "complete_leaves": 1, "parse_errors": 0},
            "rows": [{"node_id": "gpu4090", "cell": "cora_GCN_r0.05"}],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        }).encode(),
    )

    assert sm.main([
        "--config", str(config_path),
        "overview", "--require-preflight", "--require-verify", "--fail-on", "error", "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "overview"
    assert out["policy"]["require_preflight"] is True
    assert out["policy"]["require_verify"] is True
    assert out["gate"]["passed"] is True
    assert out["layout"]["peers"]["gpu4090"]["local_landing"] == "results/runs/gpu4090"
    assert out["layout"]["peers"]["gpu4090"]["trusted"]["indexed_artifacts"] == 3
    assert out["receipt"]["trusted_results"]["summary"]["rows"] == 1
    assert out["totals"]["result_rows"] == 1
    assert out["files"]["results_csv"] == ".syncmate/results_table.csv"
    assert out["files"]["workflow"] == ".syncmate/workflow.json"
    assert out["workflow"]["summary"]["peers"] == 1
    assert out["next"]["require_preflight"] is True


def test_overview_text_returns_nonzero_when_gate_fails(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main(["--config", str(config_path), "overview", "--require-preflight", "--limit", "2"]) == 1
    text = capsys.readouterr().out

    assert "syncmate overview: local" in text
    assert "gate=fail" in text
    assert "gate-preflight-missing" in text


def test_lifecycle_cli_reports_missing_setup_phase(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    assert sm.main(["--config", str(config_path), "lifecycle", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["mode"] == "lifecycle"
    assert out["current"]["phase"] == "setup-needed"
    assert out["current"]["stage"] == "setup"
    assert out["next"]["primary"]["command"] == "python scripts/syncmate/syncmate.py setup-plan"


def test_lifecycle_cli_reports_collect_phase_from_saved_diff(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    _write(
        sync_dir / "remote_status_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:00:00",
            "node_id": "gpu4090",
            "summary": {"result_leaves": 1},
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_diff_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:10:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 3, "remote_leaves": 1, "missing": 2, "conflicts": 0},
            "missing": [
                {"path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json"},
                {"path": "results/runs/cora_GCN_r0.05/GIF_im/seed42/_meta.json"},
            ],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )

    assert sm.main([
        "--config", str(config_path),
        "lifecycle", "--no-require-preflight", "--no-require-results", "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["current"]["phase"] == "collect-needed"
    assert out["current"]["node_id"] == "gpu4090"
    assert out["next"]["primary"]["command"] == "python scripts/syncmate/syncmate.py collect gpu4090 --apply"
    assert out["attention"][0]["id"] == "collect"


def test_lifecycle_cli_reports_accepted_phase_and_trace_check(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
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
    sm.write_results_table_files(sm.results_payload_from_index(index))

    assert sm.main(["--config", str(config_path), "lifecycle", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)

    assert out["ready"] is True
    assert out["current"]["phase"] == "accepted"
    assert out["next"]["primary"]["command"] == "python scripts/syncmate/syncmate.py trace gpu4090 --check"
    assert out["summary"]["indexed_artifacts"] == 3
    assert out["summary"]["result_rows"] == 1


def test_next_steps_payload_orders_executable_commands(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {
            "id": "local",
            "role": "collector",
            "peers": ["gpu4090", "h800"],
            "peer_configs": {
                "gpu4090": {"ssh": "ssh-gpu", "repo_path": "/repo", "landing": "results/runs/gpu4090"},
                "h800": {"ssh": "ssh-h800", "repo_path": "/repo", "landing": "results/runs/h800"},
            },
        },
        "remote_status": {
            "gpu4090": {"generated_at": "2026-07-01T11:00:00", "summary": {}, "errors": []},
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "summary": {"missing": 2, "conflicts": 0},
                "missing": [{"path": "a"}, {"path": "b"}],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
    }

    result = sm.next_steps_payload(snapshot, [], require_verify=True)
    commands = [item["command"] for item in result["commands"]]

    assert commands[0] == "python scripts/syncmate/syncmate.py collect gpu4090 --apply"
    assert commands[1] == "python scripts/syncmate/syncmate.py verify gpu4090 --apply"
    assert commands[2] == "python scripts/syncmate/syncmate.py remote-status h800 --apply"
    assert commands[-1] == "python scripts/syncmate/syncmate.py gate --require-verify"
    collect_step = result["commands"][0]
    assert collect_step["evidence"]["reads"] == [".syncmate/last_diff_gpu4090.json"]
    assert "results/runs/gpu4090/" in collect_step["evidence"]["writes"]
    assert ".syncmate/last_collect_gpu4090.json" in collect_step["evidence"]["writes"]
    assert ".syncmate/last_verify_gpu4090.json" in collect_step["evidence"]["writes"]
    assert ".syncmate/artifact_index.json" in collect_step["evidence"]["writes"]
    assert "copies-selected-artifacts" in collect_step["effects"]
    assert "verifies-checksums" in collect_step["effects"]
    assert "updates-trusted-index" in collect_step["effects"]
    verify_step = result["commands"][1]
    assert verify_step["evidence"]["writes"] == [
        ".syncmate/last_verify_gpu4090.json",
        ".syncmate/artifact_index.json",
    ]
    assert "contacts-peer" in verify_step["effects"]
    assert result["manual_actions"] == []


def test_next_steps_uses_import_bundle_for_saved_offline_diff(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
    bundle_path = "C:/tmp/bundle_gpu4090.zip"
    snapshot = {
        "generated_at": "2026-07-01T12:00:00",
        "device": {
            "id": "local",
            "role": "collector",
            "setup_warnings": [],
            "peers": ["gpu4090"],
            "peer_configs": {
                "gpu4090": {"repo_path": "C:/runner", "landing": "results/runs/gpu4090", "transport": "local"},
            },
        },
        "git": {"dirty": False, "status_short": [], "short_sha": "runner"},
        "results": {"nodes": {}, "total_leaves": 0},
        "remote_status": {
            "gpu4090": {"generated_at": "2026-07-01T11:00:00", "summary": {}, "errors": []},
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "mode": "import-bundle-dry-run",
                "remote": {"source": "bundle", "bundle_path": bundle_path, "git": {"short_sha": "runner"}},
                "summary": {"missing": 2, "conflicts": 0},
                "missing": [{"path": "a"}, {"path": "b"}],
                "conflicts": [],
                "errors": [],
                "report_path": ".syncmate/last_diff_gpu4090.json",
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    result = sm.next_steps_payload(snapshot, diagnostics, require_verify=True)
    commands = [item["command"] for item in result["commands"]]
    diff_missing = next(item for item in diagnostics if item["code"] == "diff-missing")

    expected = sm.command_line(["python", "scripts/syncmate/syncmate.py", "import-bundle", bundle_path])
    assert diff_missing["action"] == f"Run {expected} to extract and verify missing selected artifacts from the copied bundle."
    assert commands[0] == expected
    assert result["commands"][0]["evidence"]["inspects"] == ["copied bundle zip"]
    assert ".syncmate/results_table.json" in result["commands"][0]["evidence"]["writes"]
    assert "offline" in result["commands"][0]["effects"]
    assert "extracts-trusted-results" in result["commands"][0]["effects"]
    assert "python scripts/syncmate/syncmate.py verify gpu4090 --apply" not in commands


def test_next_steps_require_results_refreshes_table_before_gate(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
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
            "gpu4090": {"generated_at": "2026-07-01T11:00:00", "summary": {}, "errors": []},
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "summary": {"missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:20:00",
                "summary": {"status": "verified", "missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "artifact_index": {
            "peers": {
                "gpu4090": {
                    "summary": {"indexed": 1, "status": "verified"},
                    "items": [{"local_path": "results/runs/gpu4090/cell/method/seed/attack.json", "sha256": "abc"}],
                },
            },
        },
        "results_table": None,
    }

    result = sm.next_steps_payload(snapshot, [], require_verify=True, require_results=True)
    commands = [item["command"] for item in result["commands"]]

    assert "python scripts/syncmate/syncmate.py results --write --check" in commands
    assert commands[-1] == "python scripts/syncmate/syncmate.py gate --require-verify --require-results"
    results_step = next(item for item in result["commands"] if item["kind"] == "results")
    assert results_step["evidence"]["reads"] == [".syncmate/artifact_index.json"]
    assert results_step["evidence"]["writes"] == [
        ".syncmate/results_table.json",
        ".syncmate/results_table.csv",
    ]
    gate_step = result["commands"][-1]
    assert ".syncmate/results_table.json" in gate_step["evidence"]["reads"]
    assert "read-only-gate" in gate_step["effects"]
    assert result["require_results"] is True


def _stage_by_id(stages, stage_id):
    return next(stage for stage in stages if stage["id"] == stage_id)


def test_workflow_payload_marks_incremental_collect_stage(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
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
                "summary": {"missing": 2, "conflicts": 0, "remote_incomplete": 0},
                "missing": [{"path": "a"}, {"path": "b"}],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
        "results_table": None,
    }

    result = sm.workflow_payload(snapshot, [], require_verify=True, require_results=True)
    peer = result["peers"]["gpu4090"]
    collect_stage = _stage_by_id(peer["stages"], "collect")
    verify_stage = _stage_by_id(peer["stages"], "verify")
    results_stage = _stage_by_id(result["global_stages"], "results")

    assert result["mode"] == "workflow"
    assert peer["status"] == "action-needed"
    assert collect_stage["status"] == "action-needed"
    assert collect_stage["command"] == "python scripts/syncmate/syncmate.py collect gpu4090 --apply"
    assert verify_stage["status"] == "waiting"
    assert results_stage["status"] == "waiting"


def test_workflow_payload_marks_missing_results_table_after_verified_index(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

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

    result = sm.workflow_payload(snapshot, [], require_verify=True, require_results=True)
    peer = result["peers"]["gpu4090"]
    results_stage = _stage_by_id(result["global_stages"], "results")
    commands = [item["command"] for item in result["next"]["commands"]]

    assert peer["status"] == "ok"
    assert _stage_by_id(peer["stages"], "index")["status"] == "ok"
    assert results_stage["status"] == "action-needed"
    assert results_stage["command"] == "python scripts/syncmate/syncmate.py results --write --check"
    assert "python scripts/syncmate/syncmate.py results --write --check" in commands


def test_workflow_cli_can_write_machine_readable_stage_state(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.write_device_config(config_path, config)

    assert sm.main([
        "--config", str(config_path),
        "workflow", "--write", "--json", "--no-require-verify", "--no-require-results",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    saved = json.loads((sync_dir / "workflow.json").read_text(encoding="utf-8"))

    assert out["workflow_path"] == ".syncmate/workflow.json"
    assert saved["mode"] == "workflow"
    assert saved["workflow_path"] == ".syncmate/workflow.json"
    assert saved["global_stages"][0]["id"] == "preflight"


def test_automation_core_cli_can_write_machine_readable_ledger(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    remote_path = "results/runs/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    local_path = "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json"
    _write(repo / local_path, b"attack")
    _write(
        sync_dir / "last_diff_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:00:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 1, "remote_leaves": 1, "missing": 1, "conflicts": 0, "to_fetch": 1},
            "missing": [{"path": remote_path, "sha256": _sha(b"attack")}],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_collect_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:10:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 1, "remote_leaves": 1, "missing_fetched": 1, "verified": 1, "conflicts": 0},
            "fetched": [{"path": remote_path, "local_path": local_path}],
            "verification_failed": [],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "last_verify_gpu4090.json",
        json.dumps({
            "generated_at": "2026-07-01T11:20:00",
            "node_id": "gpu4090",
            "landing": "results/runs/gpu4090",
            "summary": {"remote_files": 1, "remote_leaves": 1, "verified_current": 1, "missing": 0, "conflicts": 0, "status": "verified"},
            "verified": [{"path": remote_path, "sha256": _sha(b"attack")}],
            "missing": [],
            "conflicts": [],
            "errors": [],
        }).encode(),
    )
    _write(
        sync_dir / "artifact_index.json",
        json.dumps({
            "version": 0,
            "updated_at": "2026-07-01T11:20:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "updated_at": "2026-07-01T11:20:00",
                    "landing": "results/runs/gpu4090",
                    "source_report": ".syncmate/last_verify_gpu4090.json",
                    "summary": {"remote_files": 1, "remote_leaves": 1, "indexed": 1, "missing": 0, "conflicts": 0, "status": "verified"},
                    "items": [{"source_node": "gpu4090", "remote_path": remote_path, "local_path": local_path, "sha256": _sha(b"attack")}],
                },
            },
        }).encode(),
    )
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T11:30:00",
            "mode": "results",
            "summary": {"peers": 1, "leaves": 1, "rows": 1, "complete_leaves": 1, "parse_errors": 0},
            "rows": [{"node_id": "gpu4090", "cell": "cora_GCN_r0.05", "method": "GIF", "strategy_full": "im", "seed": "seed42", "status": "ok"}],
            "parse_errors": [],
            "errors": [],
            "files": {"json": ".syncmate/results_table.json", "csv": ".syncmate/results_table.csv"},
        }).encode(),
    )

    assert sm.main(["--config", str(config_path), "automation-core", "gpu4090", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    saved = json.loads((sync_dir / "automation_core.json").read_text(encoding="utf-8"))
    markdown = (sync_dir / "automation_core.md").read_text(encoding="utf-8")

    assert out["mode"] == "automation_core"
    assert out["automation_core_path"] == ".syncmate/automation_core.json"
    assert out["automation_core_markdown_path"] == ".syncmate/automation_core.md"
    assert out["status"] == "ok"
    assert out["totals"]["missing"] == 1
    assert out["totals"]["fetched_missing"] == 1
    assert out["totals"]["checksum_verified"] == 1
    assert out["totals"]["indexed"] == 1
    assert out["results"]["rows"] == 1
    assert saved["automation_core_path"] == ".syncmate/automation_core.json"
    assert saved["peers"]["gpu4090"]["verify_status"] == "verified"
    peer = out["peers"]["gpu4090"]
    assert peer["examples"]["missing"][0]["path"] == remote_path
    assert peer["examples"]["fetched"][0]["local_path"] == local_path
    assert peer["examples"]["verified"][0]["path"] == remote_path
    assert peer["examples"]["indexed"][0]["local_path"] == local_path
    assert peer["trusted_results"]["rows"] == 1
    assert peer["trusted_results"]["examples"][0]["cell"] == "cora_GCN_r0.05"
    assert saved["peers"]["gpu4090"]["examples"]["indexed"][0]["sha256"] == _sha(b"attack")
    assert saved["peers"]["gpu4090"]["trusted_results"]["examples"][0]["status"] == "ok"
    assert "# Syncmate Automation Core" in markdown
    assert "results/runs/gpu4090/cora_GCN_r0.05/GIF_im/seed42/attack.json" in markdown
    assert "Trusted result examples" in markdown


def test_acceptance_cli_can_write_machine_readable_verdict(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
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
    sm.write_results_table_files(sm.results_payload_from_index(index))

    assert sm.main(["--config", str(config_path), "acceptance", "gpu4090", "--write", "--json"]) == 0
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


def test_results_use_remote_leaf_semantics_when_landing_wraps_remote_node(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
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

    result = sm.results_payload_from_index(index)

    assert result["summary"]["rows"] == 1
    row = result["rows"][0]
    assert row["cell"] == "cora_GCN_r0.05"
    assert row["dataset"] == "cora"
    assert row["base_model"] == "GCN"
    assert row["ratio"] == "0.05"
    assert row["method"] == "GIF"
    assert row["strategy"] == "degree"
    assert row["seed"] == "seed42"


def test_next_steps_payload_can_require_saved_preflight(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")
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
            "gpu4090": {"generated_at": "2026-07-01T11:00:00", "summary": {}, "errors": []},
        },
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "summary": {"missing": 0, "conflicts": 0},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {},
        "verify_reports": {},
        "artifact_index": {"peers": {}},
        "preflight": None,
    }

    result = sm.next_steps_payload(
        snapshot,
        [],
        require_verify=True,
        require_preflight=True,
    )
    commands = [item["command"] for item in result["commands"]]

    assert result["require_preflight"] is True
    assert commands[0] == "python scripts/syncmate/syncmate.py preflight --write"
    assert "python scripts/syncmate/syncmate.py verify gpu4090 --apply" in commands
    assert commands[-1] == "python scripts/syncmate/syncmate.py gate --require-preflight --require-verify"
    assert result["manual_actions"] == []


def test_next_cli_returns_command_queue(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    assert sm.main([
        "--config", str(config_path),
        "next", "--require-preflight", "--require-verify", "--require-results", "--write", "--json",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    action_json = sync_dir / "action_plan.json"
    action_md = sync_dir / "action_plan.md"

    assert out["action_plan_path"] == ".syncmate/action_plan.json"
    assert out["action_plan_markdown_path"] == ".syncmate/action_plan.md"
    assert action_json.is_file()
    assert action_md.is_file()
    saved = json.loads(action_json.read_text(encoding="utf-8"))
    markdown = action_md.read_text(encoding="utf-8")
    assert saved["mode"] == "next"
    assert saved["commands"][0]["command"] == "python scripts/syncmate/syncmate.py preflight --write"
    assert saved["commands"][0]["evidence"]["writes"] == [".syncmate/last_preflight.json"]
    assert "# Syncmate Action Plan" in markdown
    assert "python scripts/syncmate/syncmate.py preflight --write" in markdown
    assert "Writes: `.syncmate/last_preflight.json`" in markdown


def test_gate_cli_returns_nonzero_for_blocking_diagnostics(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "bad", {"role": "runner", "ssh": "", "repo_path": "", "landing": "results/runs/bad"})
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "gate", "--json"]) == 1


def test_preflight_payload_reports_ready_peer_commands(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config_path = repo / ".syncmate" / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")

    config = sm.build_device_config("local", "collector", str(repo))
    peer = sm.build_peer_config(
        "runner",
        "ssh-gpu",
        "/remote/repo",
        "results/runs/gpu4090",
        ["results/runs/cora_GCN_r0.05"],
        {"include": ["attack.json", "collateral.json", "_meta.json"]},
    )
    sm.add_peer_to_device(config, "gpu4090", peer)

    result = sm.preflight_payload(config, [], config_path=config_path, node_ids=["gpu4090"])
    peer_result = result["peers"]["gpu4090"]

    assert result["status"] == "ready"
    assert result["summary"]["ready"] == 1
    assert peer_result["ready"] is True
    assert peer_result["landing"] == "results/runs/gpu4090"
    assert peer_result["artifact_policy"]["include"] == ["attack.json", "collateral.json", "_meta.json"]
    assert peer_result["automation"] == [
        "remote-status",
        "manifest-diff",
        "incremental-collect",
        "checksum-verify",
        "trusted-results",
    ]
    assert "sync gpu4090" in peer_result["commands"]["sync"]
    assert result["next_commands"][0]["command"].endswith("sync gpu4090")


def test_preflight_cli_can_write_latest_report(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "preflight", "gpu4090", "--write", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    report = json.loads((sync_dir / "last_preflight.json").read_text(encoding="utf-8"))

    assert out["report_path"] == ".syncmate/last_preflight.json"
    assert report["status"] == "ready"
    assert report["summary"]["ready"] == 1
    assert report["report_path"] == ".syncmate/last_preflight.json"
    assert not (sync_dir / "state.json").exists()


def test_preflight_cli_blocks_missing_setup(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")

    assert sm.main(["--config", str(config_path), "preflight", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    codes = {item["code"] for item in out["device"]["checks"]}

    assert out["status"] == "blocked"
    assert "setup-missing" in codes
    assert "device-role-unknown" in codes
    assert not (sync_dir / "state.json").exists()


def test_preflight_cli_returns_nonzero_for_bad_peer(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "bad", {
        "role": "runner",
        "ssh": "",
        "repo_path": "",
        "landing": "../outside",
        "result_roots": ["../outside"],
        "artifact_policy": {"include": ["../escape.json"]},
    })
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "preflight", "bad", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    checks = out["peers"]["bad"]["checks"]
    codes = {item["code"] for item in checks}

    assert out["status"] == "blocked"
    assert out["summary"]["blocked"] == 1
    assert "peer-ssh-missing" in codes
    assert "peer-repo-path-missing" in codes
    assert "peer-landing-unsafe" in codes
    assert "peer-result-root-unsafe" in codes
    assert "peer-artifact-policy-invalid" in codes


def test_sync_blocks_on_preflight_before_remote_calls(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(config, "bad", {
        "role": "runner",
        "ssh": "",
        "repo_path": "",
        "landing": "results/runs/bad",
        "result_roots": ["results/runs"],
    })
    sm.write_device_config(config_path, config)
    monkeypatch.setattr(
        sm,
        "refresh_peer",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("sync should stop before remote calls")),
    )

    assert sm.main(["--config", str(config_path), "sync", "bad", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    codes = {item["code"] for item in out["preflight"]["peers"]["bad"]["checks"]}

    assert out["mode"] == "sync"
    assert out["status"] == "blocked"
    assert out["peer_results"] == {}
    assert "peer-ssh-missing" in codes
    assert "peer-repo-path-missing" in codes
    assert out["preflight"]["report_path"] == ".syncmate/last_preflight.json"
    assert (sync_dir / "last_preflight.json").is_file()
    assert not (sync_dir / "state.json").exists()


def test_refresh_blocks_unknown_peer_with_preflight_json(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)
    monkeypatch.setattr(
        sm,
        "refresh_peer",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("refresh should stop before remote calls")),
    )

    assert sm.main(["--config", str(config_path), "refresh", "unknown", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    codes = {item["code"] for item in out["preflight"]["peers"]["unknown"]["checks"]}

    assert out["mode"] == "refresh"
    assert out["status"] == "blocked"
    assert out["peer_results"] == {}
    assert "peer-unknown" in codes
    assert out["preflight"]["report_path"] == ".syncmate/last_preflight.json"
    assert (sync_dir / "last_preflight.json").is_file()
    assert not (sync_dir / "state.json").exists()
    assert not (sync_dir / "status.html").exists()


def test_refresh_no_save_does_not_write_blocked_preflight_report(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    config = sm.build_device_config("local", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "gpu4090",
        sm.build_peer_config("runner", "ssh-gpu", "/repo", "results/runs/gpu4090", ["results/runs"]),
    )
    sm.write_device_config(config_path, config)

    assert sm.main(["--config", str(config_path), "refresh", "unknown", "--no-save", "--json"]) == 1
    out = json.loads(capsys.readouterr().out)

    assert out["status"] == "blocked"
    assert "report_path" not in out["preflight"]
    assert not (sync_dir / "last_preflight.json").exists()


def test_build_snapshot_includes_peer_configs(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    peer = sm.build_peer_config("runner", "autodl-4090", "~/repo", "results/runs/gpu4090", ["results/runs"])
    snapshot = sm.build_snapshot(
        {"device_id": "local", "role": "collector", "repo_path": str(repo), "peers": {"gpu4090": peer}},
        [],
    )

    assert snapshot["device"]["peers"] == ["gpu4090"]
    assert snapshot["device"]["peer_configs"]["gpu4090"] == peer


def test_doctor_reports_peer_config_issues():
    snapshot = {
        "device": {
            "id": "local",
            "role": "collector",
            "setup_warnings": [],
            "peers": ["bad", "dup-a", "dup-b", "unsafe-root"],
            "peer_configs": {
                "bad": {
                    "role": "mystery",
                    "ssh": "",
                    "repo_path": "",
                    "landing": "../outside",
                    "result_roots": "results/runs",
                },
                "dup-a": {
                    "role": "runner",
                    "ssh": "ssh-a",
                    "repo_path": "~/repo",
                    "landing": "results/runs/shared",
                    "result_roots": ["results/runs"],
                },
                "dup-b": {
                    "role": "runner",
                    "ssh": "ssh-b",
                    "repo_path": "~/repo",
                    "landing": "results/runs/shared",
                    "result_roots": ["results/runs"],
                },
                "unsafe-root": {
                    "role": "runner",
                    "ssh": "ssh-c",
                    "repo_path": "~/repo",
                    "landing": "results/runs/unsafe-root",
                    "result_roots": ["../outside"],
                },
            },
        },
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "peer-config-missing-field" in codes
    assert "peer-role-invalid" in codes
    assert "peer-landing-unsafe" in codes
    assert "peer-result-roots-invalid" in codes
    assert "peer-result-root-unsafe" in codes
    assert "peer-landing-duplicate" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_doctor_reports_invalid_artifact_policies():
    snapshot = {
        "device": {
            "id": "local",
            "role": "collector",
            "setup_warnings": [],
            "artifact_policy": {"include": ["attack.json", "_meta.json"]},
            "peers": ["bad-policy"],
            "peer_configs": {
                "bad-policy": {
                    "role": "runner",
                    "ssh": "ssh-a",
                    "repo_path": "~/repo",
                    "landing": "results/runs/bad-policy",
                    "result_roots": ["results/runs"],
                    "artifact_policy": {"include": ["../escape.json"]},
                },
            },
        },
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "peer-artifact-policy-invalid" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"

    snapshot["device"]["artifact_policy"] = {"include": "attack.json"}
    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "artifact-policy-invalid" in codes


def test_doctor_reports_missing_remote_status_for_configured_peer(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})

    snapshot = sm.build_snapshot(
        {
            "device_id": "local",
            "role": "collector",
            "repo_path": str(repo),
            "peers": {
                "gpu4090": sm.build_peer_config(
                    "runner",
                    "ssh-gpu",
                    "/remote/repo",
                    "results/runs/gpu4090",
                    ["results/runs"],
                ),
            },
        },
        [],
    )

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    missing = [item for item in diagnostics if item["code"] == "remote-status-missing"]

    assert missing
    assert missing[0]["node"] == "gpu4090"
    assert "remote-status gpu4090 --apply" in missing[0]["action"]


def test_doctor_reports_remote_status_errors_dirty_and_result_issues():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090", "h800"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {
            "gpu4090": {
                "summary": {"device_id": "gpu4090", "git_short_sha": "abc1234", "git_dirty": True},
                "errors": [],
                "snapshot": {
                    "results": {
                        "nodes": {
                            "bare": {
                                "issues": ["multiple-git-shas", "missing-artifacts"],
                                "git_shas": {"aaa1111": 2, "bbb2222": 1},
                                "missing": {"collateral.json": 1},
                            }
                        }
                    }
                },
            },
            "h800": {
                "summary": {},
                "errors": ["remote status failed: timeout"],
                "snapshot": {},
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "remote-dirty-worktree" in codes
    assert "remote-multiple-git-shas" in codes
    assert "remote-missing-artifacts" in codes
    assert "remote-status-error" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_doctor_reports_fingerprint_attention_for_git_component():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"short_sha": "abc1234", "dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "fingerprint": {
            "token": "local-token",
            "components": {"git": "local-git", "device": "local-device"},
            "counts": {},
        },
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {
                    "device_id": "gpu4090",
                    "git_short_sha": "abc1234",
                    "git_dirty": False,
                    "fingerprint": "remote-token",
                    "fingerprint_components": {"git": "remote-git", "device": "remote-device"},
                },
                "errors": [],
                "snapshot": {},
            }
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    attention = next(item for item in diagnostics if item["code"] == "fingerprint-attention")
    gate = sm.gate_payload(snapshot, diagnostics, fail_on="error")

    assert attention["severity"] == "error"
    assert attention["node"] == "gpu4090"
    assert "git" in attention["message"]
    assert gate["passed"] is False
    assert any(item["code"] == "fingerprint-attention" for item in gate["failures"])


def test_doctor_warns_when_remote_status_lacks_fingerprint_metadata():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"short_sha": "abc1234", "dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:00:00",
                "summary": {"device_id": "gpu4090", "git_short_sha": "abc1234", "git_dirty": False},
                "errors": [],
                "snapshot": {},
            }
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    missing = next(item for item in diagnostics if item["code"] == "fingerprint-missing")

    assert missing["severity"] == "warn"
    assert missing["node"] == "gpu4090"
    assert "remote-status gpu4090 --apply" in missing["action"]


def test_doctor_reports_git_mismatch_across_remote_and_manifest_reports():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"short_sha": "local12", "dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {
            "gpu4090": {
                "summary": {"device_id": "gpu4090", "git_short_sha": "remote1", "git_dirty": False},
                "errors": [],
                "snapshot": {},
            }
        },
        "diff_reports": {
            "gpu4090": {
                "remote": {"git": {"short_sha": "remote2"}},
                "summary": {},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
        "collect_reports": {
            "gpu4090": {
                "remote": {"git": {"sha": "remote3456789abcdef"}},
                "summary": {},
                "conflicts": [],
                "verification_failed": [],
                "errors": [],
            },
        },
        "verify_reports": {
            "gpu4090": {
                "remote": {"git": {"short_sha": "remote4"}},
                "summary": {},
                "missing": [],
                "conflicts": [],
                "errors": [],
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "remote-git-mismatch" in codes
    assert "diff-git-mismatch" in codes
    assert "collect-git-mismatch" in codes
    assert "verify-git-mismatch" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_git_id_matching_accepts_short_and_full_prefixes():
    assert sm.git_ids_match("abcdef1234567890", "abcdef1")
    assert sm.git_ids_match("abcdef1", "abcdef1234567890")
    assert sm.git_ids_match("unknown", "abcdef1")
    assert not sm.git_ids_match("abcdef1", "1234567")


def test_doctor_reports_collect_missing_errors_conflicts_and_checksum_failures():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090", "h800"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "collect_reports": {
            "gpu4090": {
                "report_path": ".syncmate/last_collect_gpu4090.json",
                "errors": ["checksum failed for 1 file(s)"],
                "verification_failed": ["results/runs/cell/method/seed/_meta.json"],
                "conflicts": [{"path": "results/runs/cell/method/seed/attack.json"}],
                "summary": {},
            }
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "collect-report-missing" in codes
    assert "collect-error" in codes
    assert "collect-checksum-failed" in codes
    assert "collect-conflicts" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_doctor_reports_diff_errors_missing_and_conflicts():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "diff_reports": {
            "gpu4090": {
                "report_path": ".syncmate/last_diff_gpu4090.json",
                "errors": [],
                "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
                "conflicts": [{"path": "results/runs/cell/method/seed/attack.json"}],
                "summary": {"missing": 1, "conflicts": 1},
            },
            "h800": {
                "report_path": ".syncmate/last_diff_h800.json",
                "errors": ["remote manifest failed: timeout"],
                "summary": {},
            },
        },
        "collect_reports": {},
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "diff-missing" in codes
    assert "diff-conflicts" in codes
    assert "diff-error" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_doctor_newer_clean_verify_supersedes_planning_diff_missing():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "diff_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:10:00",
                "report_path": ".syncmate/last_diff_gpu4090.json",
                "errors": [],
                "missing": [{"path": "results/runs/cell/method/seed/attack.json"}],
                "conflicts": [],
                "summary": {"missing": 1, "conflicts": 0},
            },
        },
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "generated_at": "2026-07-01T11:20:00",
                "errors": [],
                "summary": {
                    "status": "verified",
                    "missing": 0,
                    "conflicts": 0,
                    "verified_current": 1,
                },
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)

    assert "diff-missing" not in {item["code"] for item in diagnostics}


def test_doctor_reports_verify_errors_missing_and_conflicts():
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {},
        "diff_reports": {},
        "collect_reports": {},
        "verify_reports": {
            "gpu4090": {
                "report_path": ".syncmate/last_verify_gpu4090.json",
                "errors": [],
                "missing": [{"path": "results/runs/cell/method/seed/_meta.json"}],
                "conflicts": [{"path": "results/runs/cell/method/seed/attack.json"}],
                "summary": {"missing": 1, "conflicts": 1},
            },
            "h800": {
                "report_path": ".syncmate/last_verify_h800.json",
                "errors": ["remote manifest failed: timeout"],
                "summary": {},
            },
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "verify-missing" in codes
    assert "verify-conflicts" in codes
    assert "verify-error" in codes
    assert sm.status_label(snapshot, diagnostics) == "attention"


def test_doctor_reports_stale_remote_diff_and_collect_reports(monkeypatch):
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-02T12:00:00")
    snapshot = {
        "device": {"id": "local", "role": "collector", "peers": ["gpu4090"], "setup_warnings": []},
        "git": {"dirty": False, "status_short": []},
        "results": {"nodes": {"local": {"issues": []}}, "total_leaves": 1},
        "remote_status": {
            "gpu4090": {"generated_at": "2026-07-01T06:00:00", "summary": {}, "errors": [], "snapshot": {}},
        },
        "diff_reports": {
            "gpu4090": {"generated_at": "2026-07-01T06:00:00", "summary": {}, "missing": [], "conflicts": [], "errors": []},
        },
        "collect_reports": {
            "gpu4090": {"generated_at": "2026-07-01T06:00:00", "summary": {}, "conflicts": [], "verification_failed": [], "errors": []},
        },
        "verify_reports": {
            "gpu4090": {"generated_at": "2026-07-01T06:00:00", "summary": {}, "missing": [], "conflicts": [], "errors": []},
        },
    }

    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    codes = {item["code"] for item in diagnostics}

    assert "remote-status-stale" in codes
    assert "diff-stale" in codes
    assert "collect-stale" in codes
    assert "verify-stale" in codes
    assert sm.status_label(snapshot, diagnostics) == "review"


def test_dashboard_html_contains_device_status_nodes_and_actions(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    runs = repo / "results" / "runs"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "RESULTS_RUNS", runs)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": True, "status_short": ["M x"], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T01:10:00")

    _write_leaf(runs, "gpu4090/cora_GCN_r0.05/GIF_random/seed42")
    remote_report = {
        "generated_at": "2026-07-01T00:00:00",
        "node_id": "gpu4090",
        "summary": {
            "device_id": "gpu4090",
            "role": "runner",
            "git_short_sha": "abc1234",
            "git_dirty": False,
            "result_leaves": 12,
            "result_nodes": ["bare", "gpu4090"],
            "fingerprint": "remote-token",
            "fingerprint_components": {"git": "remote-git", "results": "remote-results"},
        },
        "errors": [],
    }
    _write(sync_dir / "remote_status_gpu4090.json", json.dumps(remote_report).encode())
    diff_report = {
        "generated_at": "2026-07-01T00:05:00",
        "node_id": "gpu4090",
        "landing": "results/runs/gpu4090",
        "summary": {
            "remote_files": 3,
            "already_current": 1,
            "missing": 2,
            "conflicts": 0,
            "to_fetch": 2,
        },
        "missing": [{"path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"}],
        "conflicts": [],
        "errors": [],
    }
    _write(sync_dir / "last_diff_gpu4090.json", json.dumps(diff_report).encode())
    collect_report = {
        "generated_at": "2026-07-01T00:10:00",
        "node_id": "gpu4090",
        "landing": "results/runs/gpu4090",
        "summary": {
            "remote_files": 3,
            "already_current": 1,
            "missing_fetched": 2,
            "verified": 2,
        },
        "conflicts": [],
        "verification_failed": [],
        "errors": [],
    }
    _write(sync_dir / "last_collect_gpu4090.json", json.dumps(collect_report).encode())
    verify_report = {
        "generated_at": "2026-07-01T00:20:00",
        "node_id": "gpu4090",
        "landing": "results/runs/gpu4090",
        "summary": {
            "remote_files": 3,
            "verified_current": 3,
            "missing": 0,
            "conflicts": 0,
            "status": "verified",
        },
        "verified": [{"path": "results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json"}],
        "missing": [],
        "conflicts": [],
        "errors": [],
    }
    _write(sync_dir / "last_verify_gpu4090.json", json.dumps(verify_report).encode())
    artifact_index = {
        "version": 0,
        "updated_at": "2026-07-01T00:20:00",
        "peers": {
            "gpu4090": {
                "node_id": "gpu4090",
                "updated_at": "2026-07-01T00:20:00",
                "landing": "results/runs/gpu4090",
                "source_report": ".syncmate/last_verify_gpu4090.json",
                "summary": {
                    "remote_files": 3,
                    "indexed": 3,
                    "missing": 0,
                    "conflicts": 0,
                    "status": "verified",
                },
                "items": [],
            }
        },
    }
    _write(sync_dir / "artifact_index.json", json.dumps(artifact_index).encode())
    _write(
        sync_dir / "results_table.json",
        json.dumps({
            "generated_at": "2026-07-01T00:30:00",
            "mode": "results",
            "summary": {
                "rows": 4,
                "leaves": 2,
                "complete_leaves": 2,
                "parse_errors": 0,
            },
            "rows": [],
            "parse_errors": [],
            "errors": [],
            "files": {
                "json": ".syncmate/results_table.json",
                "csv": ".syncmate/results_table.csv",
            },
        }).encode(),
    )
    _write(
        sync_dir / "last_preflight.json",
        json.dumps({
            "generated_at": "2026-07-01T00:40:00",
            "mode": "preflight",
            "status": "ready",
            "summary": {
                "peers": 1,
                "ready": 1,
                "blocked": 0,
                "errors": 0,
                "warnings": 0,
            },
            "report_path": ".syncmate/last_preflight.json",
            "peers": {
                "gpu4090": {"status": "ready", "ready": True},
            },
        }).encode(),
    )
    snapshot = sm.build_snapshot(
        {
            "device_id": "local",
            "role": "collector",
            "repo_path": str(repo),
            "peers": {
                "gpu4090": sm.build_peer_config(
                    "runner",
                    "ssh-gpu",
                    "/remote/repo",
                    "results/runs/gpu4090",
                    ["results/runs"],
                ),
            },
        },
        [],
    )
    diagnostics = sm.diagnostics_for_snapshot(snapshot)
    out = sm.write_dashboard(snapshot, diagnostics)
    html = out.read_text(encoding="utf-8")
    workflow = json.loads((sync_dir / "workflow.json").read_text(encoding="utf-8"))
    automation_core = json.loads((sync_dir / "automation_core.json").read_text(encoding="utf-8"))
    automation_markdown = (sync_dir / "automation_core.md").read_text(encoding="utf-8")
    acceptance = json.loads((sync_dir / "acceptance.json").read_text(encoding="utf-8"))
    action_plan = json.loads((sync_dir / "action_plan.json").read_text(encoding="utf-8"))
    dashboard_checklist = (sync_dir / "checklist.md").read_text(encoding="utf-8")
    dashboard_runbook = (sync_dir / "runbook.md").read_text(encoding="utf-8")

    assert "Syncmate Status" in html
    assert "local" in html
    assert "gpu4090" in html
    assert "dirty-worktree" in html
    assert "Remote Peers" in html
    assert "Latest Preflight" in html
    assert ".syncmate/last_preflight.json" in html
    assert "Operation Entry Points" in html
    assert "python scripts/syncmate/syncmate.py runbook --write" in html
    assert ".syncmate/runbook.md" in html
    assert "python scripts/syncmate/syncmate.py next --write --require-preflight --require-verify --require-results" in html
    assert ".syncmate/action_plan.json" in html
    assert "python scripts/syncmate/syncmate.py landings gpu4090" in html
    assert "python scripts/syncmate/syncmate.py trace --check" in html
    assert "python scripts/syncmate/syncmate.py trace gpu4090 --check" in html
    assert "python scripts/syncmate/syncmate.py lifecycle --json" in html
    assert "python scripts/syncmate/syncmate.py automation-core --write" in html
    assert ".syncmate/automation_core.md" in html
    assert "python scripts/syncmate/syncmate.py checklist gpu4090 --write" in html
    assert "python scripts/syncmate/syncmate.py handoff gpu4090 --write" in html
    assert "# Syncmate Checklist" in dashboard_checklist
    assert "# Syncmate Runbook" in dashboard_runbook
    assert "python scripts/syncmate/syncmate.py sync gpu4090" in dashboard_runbook
    assert "Acceptance" in html
    assert ".syncmate/acceptance.json" in html
    assert "Automation Core" in html
    assert "Checksum OK" in html
    assert "unavailable" in html
    assert "Automation Workflow" in html
    assert ".syncmate/workflow.json" in html
    assert "Next Commands" in html
    assert "Manual Actions" in html
    assert "python scripts/syncmate/syncmate.py collect gpu4090 --apply" in html
    assert workflow["mode"] == "workflow"
    assert workflow["workflow_path"] == ".syncmate/workflow.json"
    assert automation_core["mode"] == "automation_core"
    assert automation_core["automation_core_path"] == ".syncmate/automation_core.json"
    assert automation_core["automation_core_markdown_path"] == ".syncmate/automation_core.md"
    assert automation_core["totals"]["checksum_verified"] == 3
    assert automation_core["results"]["rows"] == 4
    assert "Syncmate Automation Core" in automation_markdown
    assert acceptance["mode"] == "acceptance"
    assert acceptance["acceptance_path"] == ".syncmate/acceptance.json"
    assert action_plan["mode"] == "next"
    assert action_plan["action_plan_path"] == ".syncmate/action_plan.json"
    assert "Sync Layout" in html
    assert "/remote/repo" in html
    assert "results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json" in html
    assert "results/runs/gpu4090/cora_GCN_r0.05/GIF_random/seed42/attack.json" in html
    assert "python scripts/syncmate/syncmate.py sync gpu4090" in html
    assert "Fingerprint Compare" in html
    assert "remote-token" in html
    assert "Different Components" in html
    assert "Trusted Results Table" in html
    assert ".syncmate/results_table.csv" in html
    assert ">4</b>" in html or "<td class='num'>4</td>" in html
    assert "Age" in html
    assert "1.2h" in html
    assert "abc1234" in html
    assert ".syncmate/remote_status_gpu4090.json" in html
    assert "Collect Diffs" in html
    assert ".syncmate/last_diff_gpu4090.json" in html
    assert "Last Collections" in html
    assert "results/runs/gpu4090" in html
    assert ".syncmate/last_collect_gpu4090.json" in html
    assert "Latest Verifications" in html
    assert ".syncmate/last_verify_gpu4090.json" in html
    assert "verified" in html
    assert "Artifact Index" in html
    assert "Indexed Artifacts" in html
    assert "Result Nodes" in html


def test_dashboard_cli_writes_workflow_report_path(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    sm.write_device_config(config_path, sm.build_device_config("local", "collector", str(repo)))

    assert sm.main(["--config", str(config_path), "dashboard", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    workflow = json.loads((sync_dir / "workflow.json").read_text(encoding="utf-8"))
    automation_core = json.loads((sync_dir / "automation_core.json").read_text(encoding="utf-8"))
    automation_markdown = (sync_dir / "automation_core.md").read_text(encoding="utf-8")
    acceptance = json.loads((sync_dir / "acceptance.json").read_text(encoding="utf-8"))

    assert out["dashboard"] == ".syncmate/status.html"
    assert out["workflow"] == ".syncmate/workflow.json"
    assert out["automation_core"] == ".syncmate/automation_core.json"
    assert out["automation_core_markdown"] == ".syncmate/automation_core.md"
    assert out["acceptance"] == ".syncmate/acceptance.json"
    assert out["action_plan"] == ".syncmate/action_plan.json"
    assert out["action_plan_markdown"] == ".syncmate/action_plan.md"
    assert out["checklist"] == ".syncmate/checklist.md"
    assert out["runbook"] == ".syncmate/runbook.md"
    assert (sync_dir / "checklist.md").is_file()
    assert (sync_dir / "runbook.md").is_file()
    assert (sync_dir / "automation_core.md").is_file()
    assert (sync_dir / "action_plan.json").is_file()
    assert (sync_dir / "action_plan.md").is_file()
    assert workflow["mode"] == "workflow"
    assert workflow["workflow_path"] == ".syncmate/workflow.json"
    assert automation_core["mode"] == "automation_core"
    assert automation_core["automation_core_path"] == ".syncmate/automation_core.json"
    assert automation_core["automation_core_markdown_path"] == ".syncmate/automation_core.md"
    assert "Syncmate Automation Core" in automation_markdown
    assert acceptance["mode"] == "acceptance"
    assert acceptance["acceptance_path"] == ".syncmate/acceptance.json"
    action_plan = json.loads((sync_dir / "action_plan.json").read_text(encoding="utf-8"))
    assert action_plan["mode"] == "next"
    assert action_plan["action_plan_markdown_path"] == ".syncmate/action_plan.md"


def test_write_dashboard_can_skip_checklist_but_keep_runbook(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "STATE_FILE", sync_dir / "state.json")
    monkeypatch.setattr(sm, "STATUS_HTML", sync_dir / "status.html")
    monkeypatch.setattr(sm, "RESULTS_RUNS", repo / "results" / "runs")
    monkeypatch.setattr(sm, "git_state", lambda: {"dirty": False, "status_short": [], "branch": "b", "short_sha": "s"})
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-01T12:00:00")

    device = sm.build_device_config("local", "collector", str(repo))
    sm.write_device_config(config_path, device)
    snapshot = sm.build_snapshot(device, [])
    diagnostics = sm.diagnostics_for_snapshot(snapshot)

    out = sm.write_dashboard(snapshot, diagnostics, write_checklist_doc=False)

    assert out == sync_dir / "status.html"
    assert (sync_dir / "status.html").is_file()
    assert (sync_dir / "runbook.md").is_file()
    assert (sync_dir / "action_plan.json").is_file()
    assert (sync_dir / "action_plan.md").is_file()
    assert not (sync_dir / "checklist.md").exists()


def test_runner_queue_submit_validates_and_writes_static_dashboard(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    config_path = sync_dir / "device.yaml"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "DEFAULT_DEVICE_FILE", config_path)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-14T12:00:00")

    sm.write_device_config(config_path, sm.build_device_config("runner-a", "runner", str(repo)))

    assert sm.main([
        "--config", str(config_path), "runner-queue", "submit", "--job-id", "smoke-001",
        "--recipe", "smoke", "--requested-by", "operator",
        "--expected-git-sha", "a" * 40, "--json",
    ]) == 0
    submitted = json.loads(capsys.readouterr().out)
    assert submitted["path"] == ".syncmate/runner_queue/inbox/smoke-001.yaml"
    assert submitted["job"]["expected_git_sha"] == "a" * 40
    assert (sync_dir / "runner_queue" / "receipts" / "smoke-001.json").is_file()

    assert sm.main(["--config", str(config_path), "runner-queue", "validate", "--write", "--json"]) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["validation"]["valid"] is True
    assert validated["counts"]["inbox"] == 1
    assert (sync_dir / "runner_queue" / "manifest.json").is_file()

    assert sm.main(["--config", str(config_path), "runner-queue", "dashboard", "--json"]) == 0
    dashboard = json.loads(capsys.readouterr().out)
    html = (sync_dir / "runner_queue" / "status.html").read_text(encoding="utf-8")
    assert dashboard["dashboard"] == ".syncmate/runner_queue/status.html"
    assert "SyncMate <span>Runner Queue</span>" in html
    assert "smoke-001" in html
    assert "Inbox → running → done | failed | blocked" in html
    assert ":root{" in html
    assert ":root{{" not in html


def test_runner_queue_run_once_claims_only_allowlisted_smoke_job(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-14T12:00:00")
    monkeypatch.setattr(sm, "runner_recipe_binding", lambda recipe: {"ready": True, "errors": [], "recipe": {"id": recipe}})
    sm.runner_queue_submit("smoke-001", "smoke")
    calls = []

    class Completed:
        returncode = 0
        stdout = '{"passed": true, "mode": "smoke"}'
        stderr = ""

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return Completed()

    monkeypatch.setattr(sm.subprocess, "run", fake_run)
    result = sm.runner_queue_run_once({"role": "runner", "device_id": "gpu4090"})

    assert result["status"] == "done"
    assert result["job_id"] == "smoke-001"
    assert calls[0][0][1:] == ["scripts/syncmate/syncmate.py", "smoke", "--json"]
    assert "shell" not in calls[0][1]
    assert (sync_dir / "runner_queue" / "done" / "smoke-001.yaml").is_file()
    outcome = json.loads((sync_dir / "runner_queue" / "results" / "smoke-001.json").read_text(encoding="utf-8"))
    assert outcome["recipe_passed"] is True
    assert outcome["command"][1:] == ["scripts/syncmate/syncmate.py", "smoke", "--json"]


def test_runner_queue_blocks_invalid_yaml_and_never_executes_it(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "now_iso", lambda: "2026-07-14T12:00:00")
    bad = sync_dir / "runner_queue" / "inbox" / "unsafe.yaml"
    _write(bad, b"protocol: syncmate-runner-queue/v1\nversion: 1\nid: unsafe\nrecipe: shell\ncreated_at: 2026-07-14T12:00:00\ncommand: rm -rf /\n")
    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)))

    result = sm.runner_queue_run_once({"role": "runner", "device_id": "gpu4090"})

    assert result["status"] == "blocked"
    assert not calls
    assert (sync_dir / "runner_queue" / "blocked" / "unsafe.yaml").is_file()
    outcome = json.loads((sync_dir / "runner_queue" / "results" / "unsafe.json").read_text(encoding="utf-8"))
    assert outcome["status"] == "blocked"
    assert "unsupported job fields: command" in outcome["reason"]


def test_runner_queue_refuses_to_run_on_collector_only_device(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sm.runner_queue_submit("smoke-001", "smoke")

    result = sm.runner_queue_run_once({"role": "collector", "device_id": "laptop"})

    assert result["status"] == "blocked"
    assert (sync_dir / "runner_queue" / "inbox" / "smoke-001.yaml").is_file()


def test_runner_queue_contract_is_read_only_until_explicitly_written(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)

    assert sm.main(["runner-queue", "contract", "--json"]) == 0
    contract = json.loads(capsys.readouterr().out)

    assert not sync_dir.exists()
    assert contract["protocol"] == "syncmate-runner-queue/v1"
    assert contract["job_schema"]["additional_fields"] is False
    assert "expected_git_sha" in contract["job_schema"]["optional"]
    assert contract["job_schema"]["expected_git_sha_pattern"] == "[0-9a-fA-F]{40}"
    expected_recipes = [
        "smoke",
        "opengu-preflight-v1",
        "opengu-cache-v2-gate4-v1",
    ]
    expected_recipes.extend(
        "opengu-target-direct-selection-{0}-v2".format(stage)
        for stage in sm.TARGET_DIRECT_STAGES
    )
    expected_recipes.extend(
        "opengu-target-direct-gu-gate-{0}-v2".format(
            sm._target_direct_ratio_id(ratio)
        )
        for ratio in sm.TARGET_DIRECT_RATIOS
    )
    expected_recipes.extend(
        "opengu-target-direct-gu-{0}-{1}-v2".format(
            stage, sm._target_direct_ratio_id(ratio)
        )
        for stage in sm.TARGET_DIRECT_STAGES
        for ratio in sm.TARGET_DIRECT_RATIOS
    )
    assert contract["execution"]["allowlisted_recipes"] == expected_recipes
    assert contract["execution"]["single_shot_flag"] == "--once"
    assert "runner-agent serve" in contract["state_machine"]["owner"]
    assert "bypassing SyncMate collection, checksum verification, or gate evidence" in contract["integration"]["forbidden"]

    assert sm.main(["runner-queue", "contract", "--write", "--json"]) == 0
    written = json.loads(capsys.readouterr().out)
    saved = json.loads((sync_dir / "runner_queue" / "contract.json").read_text(encoding="utf-8"))

    assert written["contract_path"] == ".syncmate/runner_queue/contract.json"
    assert saved["integration"]["opengu"].startswith("May submit or observe")


def test_runner_agent_lock_is_exclusive_and_released(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")

    owner = sm.runner_agent_acquire_lock("runner-a")
    assert owner["device_id"] == "runner-a"
    try:
        sm.runner_agent_acquire_lock("runner-b")
    except RuntimeError as exc:
        assert "lock already exists" in str(exc)
    else:
        raise AssertionError("second runner agent acquired an existing lock")
    sm.runner_agent_release_lock()
    assert not sm.runner_agent_lock_dir().exists()


def test_runner_agent_processes_exactly_one_job_under_lock(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(sm, "runner_recipe_binding", lambda recipe: {"ready": True, "errors": [], "recipe": {"id": recipe}})
    sm.runner_queue_submit("smoke-001", "smoke")

    class Completed:
        returncode = 0
        stdout = '{"passed": true}'
        stderr = ""

    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append((args, kwargs)) or Completed())
    outcome = sm.runner_agent_serve({"role": "runner", "device_id": "runner-a"}, poll_seconds=1, max_jobs=1)

    assert outcome["status"] == "completed"
    assert outcome["processed"] == 1
    assert len(calls) == 1
    assert not sm.runner_agent_lock_dir().exists()


def test_runner_queue_validates_full_json_before_bounding_diagnostic_tail(
    tmp_path, monkeypatch
):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(
        sm,
        "runner_recipe_binding",
        lambda recipe: {"ready": True, "errors": [], "recipe": {"id": recipe}},
    )
    sm.runner_queue_submit("large-json-001", "smoke")

    class Completed:
        returncode = 0
        stdout = json.dumps({"passed": True, "padding": "x" * 20000})
        stderr = ""

    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: Completed())

    outcome = sm.runner_queue_run_once({"role": "runner", "device_id": "runner-a"})
    result = json.loads(
        (sync_dir / "runner_queue" / "results" / "large-json-001.json").read_text(
            encoding="utf-8"
        )
    )

    assert outcome["status"] == "done"
    assert result["recipe_passed"] is True
    assert result["stdout_truncated"] is True
    assert len(result["stdout"]) == 16000
    assert result["stdout_sha256"] == hashlib.sha256(
        Completed.stdout.encode("utf-8")
    ).hexdigest()


def test_runner_queue_blocks_config_or_git_binding_mismatch_before_execution(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sm.runner_queue_submit("smoke-001", "smoke")
    mismatch = {"ready": False, "errors": ["fixed recipe config SHA-256 differs from recipe metadata"], "expected": {"git_sha": "expected"}, "observed": {"git_sha": "other"}}
    monkeypatch.setattr(sm, "runner_recipe_binding", lambda recipe: mismatch)
    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append(args))

    outcome = sm.runner_queue_run_once({"role": "runner", "device_id": "runner-a"})

    assert outcome["status"] == "blocked"
    assert not calls
    result = json.loads((sync_dir / "runner_queue" / "results" / "smoke-001.json").read_text(encoding="utf-8"))
    assert result["recipe_binding"]["observed"]["git_sha"] == "other"


def test_runner_queue_blocks_exact_job_git_mismatch_before_execution(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sm.runner_queue_submit("smoke-001", "smoke", expected_git_sha="a" * 40)
    binding = {
        "ready": True,
        "errors": [],
        "observed": {"git_sha": "b" * 40},
        "recipe": {"id": "smoke"},
    }
    monkeypatch.setattr(sm, "runner_recipe_binding", lambda recipe: binding)
    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append(args))

    outcome = sm.runner_queue_run_once({"role": "runner", "device_id": "runner-a"})

    assert outcome["status"] == "blocked"
    assert not calls
    result = json.loads(
        (sync_dir / "runner_queue" / "results" / "smoke-001.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["recipe_binding"]["job_expected_git_sha"] == "a" * 40
    assert result["recipe_binding"]["job_exact_git_match"] is False


def test_runner_queue_duplicate_state_and_terminal_result_are_not_overwritten(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    monkeypatch.setattr(sm, "runner_recipe_binding", lambda recipe: {"ready": True, "errors": []})
    sm.runner_queue_submit("smoke-001", "smoke")
    inbox = sync_dir / "runner_queue" / "inbox" / "smoke-001.yaml"
    duplicate = sync_dir / "runner_queue" / "done" / "smoke-001.yaml"
    duplicate.parent.mkdir(parents=True, exist_ok=True)
    duplicate.write_bytes(inbox.read_bytes())
    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append(args))

    outcome = sm.runner_queue_run_once({"role": "runner", "device_id": "runner-a"})

    assert outcome["status"] == "blocked"
    assert not calls
    assert inbox.exists() and duplicate.exists()


def test_runner_agent_refuses_stale_running_without_automatic_retry(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sm.runner_queue_submit("smoke-001", "smoke")
    (sync_dir / "runner_queue" / "inbox" / "smoke-001.yaml").replace(sync_dir / "runner_queue" / "running" / "smoke-001.yaml")
    calls = []
    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: calls.append(args))

    outcome = sm.runner_agent_serve({"role": "runner", "device_id": "runner-a"}, poll_seconds=1, max_idle_polls=0)

    assert outcome["status"] == "blocked"
    assert not calls
    assert (sync_dir / "runner_queue" / "running" / "smoke-001.yaml").exists()


def test_runner_agent_inspect_distinguishes_active_and_orphaned_running(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    sm.runner_queue_submit("smoke-001", "smoke")
    (sync_dir / "runner_queue" / "inbox" / "smoke-001.yaml").replace(
        sync_dir / "runner_queue" / "running" / "smoke-001.yaml"
    )

    orphaned = sm.runner_agent_inspect_payload()
    assert orphaned["active_running"] is False
    assert orphaned["stale_running"] is True

    sm.runner_agent_acquire_lock("runner-a")
    try:
        active = sm.runner_agent_inspect_payload()
        assert active["active_running"] is True
        assert active["stale_running"] is False
    finally:
        sm.runner_agent_release_lock()


def test_runner_agent_dispatch_rejects_nonrunner_peer_without_remote_execution(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config = sm.build_device_config("collector-a", "collector", str(repo))
    sm.add_peer_to_device(config, "bad-peer", sm.build_peer_config(
        "collector", None, str(repo), "results/runs/bad-peer", ["results/runs"], transport="local",
    ))
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    called = []
    monkeypatch.setattr(sm, "runner_agent_peer_invoke", lambda *args, **kwargs: called.append(args))

    outcome = sm.runner_agent_dispatch_payload(config, [], config_path=repo / ".syncmate" / "device.yaml", node_id="bad-peer",
                                               job_id="preflight-001", recipe="opengu-preflight-v1", requested_by=None, note=None)

    assert outcome["status"] == "blocked"
    assert not called


def test_runner_agent_dispatch_binds_clean_remote_exact_git_sha(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    config = sm.build_device_config("collector-a", "collector", str(repo))
    sm.add_peer_to_device(
        config,
        "runner-a",
        sm.build_peer_config(
            "runner",
            None,
            str(repo / "runner"),
            "results/runs/runner-a",
            ["results/runs"],
            transport="local",
        ),
    )
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", repo / ".syncmate")
    monkeypatch.setattr(
        sm,
        "preflight_payload",
        lambda *args, **kwargs: {
            "status": "ready",
            "summary": {"ready": 1, "blocked": 0},
        },
    )
    monkeypatch.setattr(sm, "maybe_write_preflight_report", lambda *args, **kwargs: None)
    calls = []

    def invoke(_peer, arguments, **_kwargs):
        calls.append(arguments)
        if arguments == ["self", "--json"]:
            return {
                "ok": True,
                "payload": {"git": {"sha": "c" * 40, "dirty": False}},
                "errors": [],
            }
        return {"ok": True, "payload": {"submitted": True}, "errors": []}

    monkeypatch.setattr(sm, "runner_agent_peer_invoke", invoke)

    outcome = sm.runner_agent_dispatch_payload(
        config,
        [],
        config_path=repo / ".syncmate" / "device.yaml",
        node_id="runner-a",
        job_id="gate4-001",
        recipe="opengu-cache-v2-gate4-v1",
        requested_by="operator",
        note="exact pin",
    )

    assert outcome["status"] == "submitted"
    assert outcome["expected_git_sha"] == "c" * 40
    assert calls[0] == ["self", "--json"]
    assert "--expected-git-sha" in calls[1]
    assert calls[1][calls[1].index("--expected-git-sha") + 1] == "c" * 40


def test_runner_agent_peer_invoke_uses_configured_python_executable(monkeypatch):
    calls = []

    class Completed:
        returncode = 0
        stdout = '{"submitted": true}'
        stderr = ""

    monkeypatch.setattr(sm.subprocess, "run", lambda command, **kwargs: calls.append(command) or Completed())
    peer = {
        "role": "runner",
        "transport": "ssh",
        "ssh": "autodl-opengu",
        "repo_path": "/autodl-fs/data/OpenGU/GULib-master",
        "python_executable": "/root/miniconda3/bin/python",
    }

    result = sm.runner_agent_peer_invoke(
        peer,
        ["runner-queue", "status", "--json"],
    )

    assert result["ok"] is True
    assert calls[0][:2] == ["ssh", "autodl-opengu"]
    assert "&& PYTHONDONTWRITEBYTECODE=1 " in calls[0][2]
    assert "/root/miniconda3/bin/python scripts/syncmate/syncmate.py runner-queue status --json" in calls[0][2]


def test_runner_agent_collect_failure_never_reports_acceptance(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)

    class Completed:
        returncode = 0
        stdout = '{"gate": {"passed": false}}'
        stderr = "checksum mismatch"

    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: Completed())
    outcome = sm.runner_agent_collect_and_gate(repo / ".syncmate" / "device.yaml", "runner-a")

    assert outcome["ok"] is False
    assert outcome["gate_passed"] is False


def test_gate4_runner_recipe_is_fixed_bounded_and_collectable():
    definition = sm.runner_recipe_definition("opengu-cache-v2-gate4-v1")

    assert definition["argv"] == [
        "{python}",
        "-m",
        "scripts.cache_v2_gate4_canary",
        "--json",
    ]
    assert definition["expected_git_sha"] == sm.GATE4_RECIPE_BASE_SHA
    assert definition["config_sha256"] == (
        "45f587853aee6a91e85efd82ee40350435969a7b51b9539062762ae06b875980"
    )
    assert definition["timeout_seconds"] == 3600
    assert definition["collector_acceptance"] is True
    assert len(definition["expected_artifact_paths"]) == 4
    assert all(
        path.startswith("results/runs/__syncmate_gate4__/")
        for path in definition["expected_artifact_paths"]
    )
    assert "predictions.npz" in definition["expected_artifact_paths"][2]


def test_recipe_config_hash_is_line_ending_stable(tmp_path):
    lf = tmp_path / "lf.yaml"
    crlf = tmp_path / "crlf.yaml"
    lf.write_bytes(b"version: 1\nname: smoke\n")
    crlf.write_bytes(b"version: 1\r\nname: smoke\r\n")

    assert sm.sha256_file(lf) != sm.sha256_file(crlf)
    assert sm.sha256_recipe_config(lf) == sm.sha256_recipe_config(crlf)


def test_gate4_runner_recipe_uses_exact_scoped_git_delta(monkeypatch):
    changed = [
        "GULib-master/attack/pipeline_adapter.py",
        "GULib-master/config.py",
        "GULib-master/dataset/original_dataset.py",
        "GULib-master/experiments/run.py",
        "GULib-master/experiments/configs/cache_v2_gate4_cora_degree_canary.yaml",
        "GULib-master/experiments/processed_provider.py",
        "GULib-master/parameter_parser.py",
        "GULib-master/scripts/cache_v2_gate4_canary.py",
        "GULib-master/scripts/syncmate/syncmate.py",
        "GULib-master/tests/test_auto_report_v3.py",
        "GULib-master/tests/test_cache_v2_gate4_canary.py",
        "GULib-master/tests/test_demo.py",
        "GULib-master/tests/test_experiment_processed_provider.py",
        "GULib-master/tests/test_phase_b_invariants.py",
        "GULib-master/tests/test_syncmate.py",
        "GULib-master/utils/dataset_utils.py",
        "GULib-master/utils/logger.py",
    ]
    monkeypatch.setattr(sm, "run_git", lambda args: "f" * 40)

    class Ancestor:
        returncode = 0

    monkeypatch.setattr(sm.subprocess, "run", lambda *args, **kwargs: Ancestor())
    monkeypatch.setattr(
        sm.subprocess,
        "check_output",
        lambda *args, **kwargs: ("\n".join(changed) + "\n").encode(),
    )

    binding = sm.runner_recipe_git_binding(
        sm.GATE4_RECIPE_BASE_SHA,
        sm.GATE4_RECIPE_ALLOWED_DELTA,
    )

    assert binding["ok"] is True
    assert binding["mode"] == "tooling-delta"
    assert binding["changed_paths"] == changed

    changed.append("GULib-master/cache_v2/store.py")
    rejected = sm.runner_recipe_git_binding(
        sm.GATE4_RECIPE_BASE_SHA,
        sm.GATE4_RECIPE_ALLOWED_DELTA,
    )
    assert rejected["ok"] is False
    assert "non-tooling commits" in rejected["errors"][0]


def test_runner_delta_file_allowlist_does_not_accept_prefix_collisions():
    assert sm._runner_delta_path_allowed(
        "GULib-master/experiments/run.py",
        ("GULib-master/experiments/run.py",),
    )
    assert not sm._runner_delta_path_allowed(
        "GULib-master/experiments/run.py.backup",
        ("GULib-master/experiments/run.py",),
    )
    assert sm._runner_delta_path_allowed(
        "GULib-master/scripts/syncmate/helper.py",
        ("GULib-master/scripts/syncmate/",),
    )


def test_target_direct_recipes_freeze_dynamic_k_scope_and_artifact_sets():
    selection = sm.runner_recipe_definition(
        "opengu-target-direct-selection-citeseer-seed212-v2"
    )
    gate_1 = sm.runner_recipe_definition(
        "opengu-target-direct-gu-gate-r001-v2"
    )
    gate_5 = sm.runner_recipe_definition(
        "opengu-target-direct-gu-gate-r005-v2"
    )
    full = sm.runner_recipe_definition(
        "opengu-target-direct-gu-pubmed-seed2024-r005-v2"
    )

    assert selection["recipe_introduced_git_sha"] == (
        "264b38995cebc84d10402d8113ea949ca2cfa34f"
    )
    assert selection["config_sha256"] == sm.TARGET_DIRECT_CONFIG_SHA256
    assert selection["selection_matrix"]["candidate_count"] == 2328
    assert selection["selection_matrix"]["split_contract"] == {
        "processed_profile": "planetoid_70_10_20_seed2024",
        "train_ratio": 0.7,
        "val_ratio": 0.1,
        "test_ratio": 0.2,
        "split_seed": 2024,
    }
    assert selection["selection_matrix"]["budget_ratios"] == [0.01, 0.05]
    assert selection["selection_matrix"]["expected_k_by_ratio"] == {
        "0.01": 23,
        "0.05": 116,
    }
    assert selection["selection_matrix"]["score_budget_semantics"] == (
        "prefix_stable_budget_independent"
    )
    assert selection["selection_matrix"]["parameter_scope"] == "last_layer"
    assert len(selection["expected_artifact_paths"]) == 5
    assert gate_1["gu_gate"]["ratio"] == 0.01
    assert gate_1["gu_gate"]["k"] == 18
    assert gate_5["gu_gate"]["ratio"] == 0.05
    assert gate_5["gu_gate"]["k"] == 94
    assert gate_1["gu_gate"]["target_checkpoint_required"] is True
    assert len(gate_1["expected_artifact_paths"]) == 4
    assert set(gate_1["expected_artifact_paths"]).isdisjoint(
        set(gate_5["expected_artifact_paths"])
    )
    assert full["gu_stage"]["candidate_count"] == 13801
    assert full["gu_stage"]["split_contract"] == selection[
        "selection_matrix"
    ]["split_contract"]
    assert full["gu_stage"]["k"] == 690
    assert full["gu_stage"]["ratio"] == 0.05
    assert full["gu_stage"]["execution_authorized"] is False
    assert full["gu_stage"]["candidate_matrix_only"] is True
    assert full["gu_stage"]["selectors"] == list(
        sm.TARGET_DIRECT_STRATEGIES
    )
    assert len(full["expected_artifact_paths"]) == 68


def test_target_direct_recipe_hash_matches_normalized_frozen_config_source():
    config_path = Path(sm.REPO_ROOT) / sm.TARGET_DIRECT_CONFIG
    assert sm.TARGET_DIRECT_CONFIG_SHA256 == sm.sha256_recipe_config(config_path)


def test_target_direct_selection_acceptance_binds_timing_scope_and_checkpoint(
    tmp_path, monkeypatch
):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    definition = sm.runner_recipe_definition(
        "opengu-target-direct-selection-cora-seed42-v2"
    )
    landing = "results/runs/gpu4090-target-direct"
    paths = {}
    for remote in definition["expected_artifact_paths"][:4]:
        local = sm.local_landing_path(landing, remote)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text('{"status":"success"}\n', encoding="utf-8")
        paths[remote] = local
    receipt_remote = definition["expected_artifact_paths"][4]
    receipt_path = sm.local_landing_path(landing, receipt_remote)
    receipt = {
        "schema": "target_direct_v1.syncmate_selection_cell",
        "version": 2,
        "dataset": "Cora",
        "seed": 42,
        "status": "success",
        "experiment_git_sha": "a" * 40,
        "parameter_scope": "last_layer",
        "candidate_count": 1895,
        "budget_ratios": [0.01, 0.05],
        "expected_k_by_ratio": {"0.01": 18, "0.05": 94},
        "formal_score_count": 17,
        "score_budget_semantics": "prefix_stable_budget_independent",
        "budget_conditioned_strategies": [],
        "score_bundle_cold_total_seconds": 4.0,
        "score_bundle_warm_read_seconds": {
            "0.01_warm": 0.02,
            "0.05_cold_projection": 0.02,
            "0.05_warm": 0.02,
        },
        "ratio_results": {
            ratio: {
                "ratio": float(ratio),
                "k": expected_k,
                "cold_method_timings": {
                    strategy: {
                        "status": "success",
                        "cache_hit": False,
                        "selection_projection_cache_hit": False,
                        "cold_selection_projection_seconds": 0.01,
                    }
                    for strategy in sm.TARGET_DIRECT_STRATEGIES
                },
                "warm_method_timings": {
                    strategy: {
                        "status": "success",
                        "cache_hit": True,
                        "selection_projection_cache_hit": True,
                    }
                    for strategy in sm.TARGET_DIRECT_STRATEGIES
                },
                "failure_state": {"state": "success", "failure": None},
            }
            for ratio, expected_k in (("0.01", 18), ("0.05", 94))
        },
        "target_checkpoint": {
            "file_sha256": "b" * 64,
            "state_hash": "c" * 64,
        },
        "device_name": "NVIDIA GeForce RTX 4090",
        "peak_gpu_allocated_bytes": 1024,
        "peak_gpu_reserved_bytes": 2048,
    }
    for ratio, cold_index, warm_index in (
        ("0.01", 0, 2),
        ("0.05", 1, 3),
    ):
        receipt["ratio_results"][ratio]["cold_sha256"] = sm.sha256_file(
            paths[definition["expected_artifact_paths"][cold_index]]
        )
        receipt["ratio_results"][ratio]["warm_sha256"] = sm.sha256_file(
            paths[definition["expected_artifact_paths"][warm_index]]
        )
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    paths[receipt_remote] = receipt_path
    sm.write_artifact_index(
        {
            "version": 0,
            "updated_at": "2026-07-24T00:00:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "landing": landing,
                    "remote": {"git": {"sha": "a" * 40}},
                    "summary": {"status": "verified", "indexed": 5},
                    "items": [
                        {
                            "remote_path": remote,
                            "local_path": sm.rel(paths[remote]),
                            "sha256": sm.sha256_file(paths[remote]),
                        }
                        for remote in definition["expected_artifact_paths"]
                    ],
                }
            },
        }
    )

    result = sm.target_direct_selection_acceptance_payload(
        definition,
        node_id="gpu4090",
        expected_git_sha="a" * 40,
    )

    assert result["passed"] is True
    assert result["mode"] == "target-direct-selection-acceptance"
    assert result["accepted_cells"] == 1


def test_target_direct_gu_gate_acceptance_requires_exact_target_checkpoint(
    tmp_path, monkeypatch
):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    definition = sm.runner_recipe_definition(
        "opengu-target-direct-gu-gate-r001-v2"
    )
    landing = "results/runs/gpu4090-target-direct"
    documents = {
        "attack.json": {
            "results": {"degree": {"failed": False, "total_time": 1.0}}
        },
        "collateral.json": {
            "results": [{"strategy": "degree", "gap": 0.1}]
        },
        "_meta.json": {
            "git_sha": "a" * 40,
            "method": "GNNDelete",
            "strategy": "degree",
            "seed": 42,
            "config": {
                "claims": {
                    "parameter_scope": "last_layer",
                    "deletion_ratio": 0.01,
                }
            },
            "selection_artifact": {
                "artifact_id": "selection_degree",
                "recipe_hash": "b" * 64,
                "content_hash": "c" * 64,
                "strategy": "degree",
                "ratio": 0.01,
                "k": 18,
                "authoritative": True,
                "target_checkpoint": {
                    "state_hash": "d" * 64,
                    "file_sha256": "e" * 64,
                },
            },
        },
    }
    items = []
    for remote in definition["expected_artifact_paths"]:
        local = sm.local_landing_path(landing, remote)
        local.parent.mkdir(parents=True, exist_ok=True)
        name = remote.rsplit("/", 1)[-1]
        if name in documents:
            local.write_text(json.dumps(documents[name]), encoding="utf-8")
        else:
            local.write_bytes(b"npz")
        items.append(
            {
                "remote_path": remote,
                "local_path": sm.rel(local),
                "sha256": sm.sha256_file(local),
            }
        )
    sm.write_artifact_index(
        {
            "version": 0,
            "updated_at": "2026-07-24T00:00:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "landing": landing,
                    "remote": {"git": {"sha": "a" * 40}},
                    "summary": {"status": "verified", "indexed": 4},
                    "items": items,
                }
            },
        }
    )

    result = sm.target_direct_gu_acceptance_payload(
        definition,
        node_id="gpu4090",
        expected_git_sha="a" * 40,
    )

    assert result["passed"] is True
    assert result["mode"] == "target-direct-gu-acceptance"
    assert result["target_checkpoint_state_hash"] == "d" * 64


def test_target_direct_gu_stage_acceptance_requires_one_shared_checkpoint(
    tmp_path, monkeypatch
):
    repo = tmp_path / "repo"
    sync_dir = repo / ".syncmate"
    monkeypatch.setattr(sm, "REPO_ROOT", repo)
    monkeypatch.setattr(sm, "SYNC_DIR", sync_dir)
    definition = sm.runner_recipe_definition(
        "opengu-target-direct-gu-cora-seed42-r001-v2"
    )
    definition["expected_artifact_paths"] = definition[
        "expected_artifact_paths"
    ][:8]
    definition["gu_stage"]["selectors"] = ["degree", "a_grad_norm"]
    landing = "results/runs/gpu4090-target-direct"
    items = []
    for selector in definition["gu_stage"]["selectors"]:
        parent = (
            sm.TARGET_DIRECT_GU_OUTPUT_ROOT
            + "/cora_GCN_r0.01/GNNDelete_"
            + selector
            + "/seed42"
        )
        documents = {
            "attack.json": {
                "results": {selector: {"failed": False, "total_time": 1.0}}
            },
            "collateral.json": {
                "results": [{"strategy": selector, "gap": 0.1}]
            },
            "_meta.json": {
                "git_sha": "a" * 40,
                "method": "GNNDelete",
                "strategy": selector,
                "seed": 42,
                "config": {
                    "claims": {
                        "parameter_scope": "last_layer",
                        "deletion_ratio": 0.01,
                    }
                },
                "selection_artifact": {
                    "artifact_id": "selection_" + selector,
                    "recipe_hash": "b" * 64,
                    "content_hash": "c" * 64,
                    "strategy": selector,
                    "ratio": 0.01,
                    "k": 18,
                    "authoritative": True,
                    "target_checkpoint": {
                        "state_hash": "d" * 64,
                        "file_sha256": "e" * 64,
                    },
                },
            },
        }
        for name, document in documents.items():
            remote = parent + "/" + name
            local = sm.local_landing_path(landing, remote)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(json.dumps(document), encoding="utf-8")
            items.append(
                {
                    "remote_path": remote,
                    "local_path": sm.rel(local),
                    "sha256": sm.sha256_file(local),
                }
            )
        remote = parent + "/predictions.npz"
        local = sm.local_landing_path(landing, remote)
        with zipfile.ZipFile(local, "w") as archive:
            archive.writestr(selector + "__selected_nodes.npy", b"test")
        items.append(
            {
                "remote_path": remote,
                "local_path": sm.rel(local),
                "sha256": sm.sha256_file(local),
            }
        )
    sm.write_artifact_index(
        {
            "version": 0,
            "updated_at": "2026-07-24T00:00:00",
            "errors": [],
            "peers": {
                "gpu4090": {
                    "node_id": "gpu4090",
                    "landing": landing,
                    "remote": {"git": {"sha": "a" * 40}},
                    "summary": {"status": "verified", "indexed": 8},
                    "items": items,
                }
            },
        }
    )

    result = sm.target_direct_gu_stage_acceptance_payload(
        definition,
        node_id="gpu4090",
        expected_git_sha="a" * 40,
    )

    assert result["passed"] is True
    assert result["mode"] == "target-direct-gu-stage-acceptance"
    assert result["accepted_cells"] == 2
    assert {
        cell["target_checkpoint_state_hash"] for cell in result["cells"]
    } == {"d" * 64}
