from pathlib import Path

from scripts.evaluation import cli


def test_cli_extract_dispatch(monkeypatch, tmp_path):
    called = {}

    def _fake_run_extraction(logs_dir, out_json, print_table):
        called["logs_dir"] = logs_dir
        called["out_json"] = out_json
        called["print_table"] = print_table
        return {}, {}, out_json

    monkeypatch.setattr(cli.extractor, "run_extraction", _fake_run_extraction)

    output = tmp_path / "metrics.json"
    rc = cli.main(["extract", "--logs-dir", str(tmp_path), "--out-json", str(output), "--no-print-table"])
    assert rc == 0
    assert called["out_json"] == output
    assert called["print_table"] is False


def test_cli_plot_attack_dispatch(monkeypatch, tmp_path):
    called = {}
    class _AttackModule:
        @staticmethod
        def load_attack_matrix(path):
            called["input"] = path
            return {
                "methods": ["GIF"],
                "strategies": ["random"],
                "values": {"GIF": {"random": 0.01}},
                "unit": "ratio",
            }

        @staticmethod
        def generate_attack_charts(payload, out_dir):
            called["payload"] = payload
            called["out_dir"] = out_dir
            return [out_dir / "attack_effectiveness_by_method.png"]

    monkeypatch.setattr(cli, "_load_attack_charts", lambda: _AttackModule)
    monkeypatch.setattr(cli, "_load_step0_plots", lambda: object())

    in_json = tmp_path / "attack.json"
    out_dir = tmp_path / "plots"
    rc = cli.main(["plot", "--type", "attack", "--input-json", str(in_json), "--out-dir", str(out_dir)])
    assert rc == 0
    assert called["input"] == in_json
    assert called["out_dir"] == out_dir


def test_cli_all_dispatch(monkeypatch, tmp_path):
    called = {}

    def _fake_extract(logs_dir, out_json, print_table):
        called["extract"] = (logs_dir, out_json, print_table)
        return {}, {}, out_json

    class _Step0Module:
        @staticmethod
        def load_round2(path):
            called["round2_input"] = path
            return {"GIF": {"0.005": {"status": "OK", "f1_after": 0.8, "unlearn_time": 1.0}}}

        @staticmethod
        def run_step0_plotting(results, plot_dir, compat_json, report_md):
            called["step0"] = (results, plot_dir, compat_json, report_md)
            return compat_json, report_md

    monkeypatch.setattr(cli.extractor, "run_extraction", _fake_extract)
    monkeypatch.setattr(cli, "_load_step0_plots", lambda: _Step0Module)
    monkeypatch.setattr(cli, "_load_attack_charts", lambda: object())

    out_root = tmp_path / "step0"
    rc = cli.main([
        "all",
        "--logs-dir",
        str(tmp_path / "logs"),
        "--step0-input-json",
        str(tmp_path / "round2.json"),
        "--out-root",
        str(out_root),
        "--no-print-table",
    ])
    assert rc == 0
    assert "extract" in called
    assert "step0" in called
