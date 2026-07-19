"""Boundary tests for the decoupled Cache V2 Selection canary."""

from __future__ import annotations

import ast

import pytest

from scripts import cache_v2_selection_canary as canary


def _args(tmp_path, mode="cold"):
    return canary._parser().parse_args(
        [
            mode,
            "--store-root",
            str((tmp_path / "store").resolve()),
            "--processed-root",
            str((tmp_path / "processed").resolve()),
            "--legacy-results-root",
            str((tmp_path / "results").resolve()),
            "--strategy",
            "degree",
        ]
    )


def test_canary_has_no_dataset_framework_or_downloader_imports():
    source = canary.__file__
    tree = ast.parse(open(source, encoding="utf-8").read(), filename=source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert not any(
        name.split(".", 1)[0] in {"ogb", "torch_geometric", "dataset"}
        for name in imports
    )


def test_parser_exposes_only_canonical_processed_input(tmp_path):
    args = _args(tmp_path)
    assert args.processed_root == (tmp_path / "processed").resolve()
    from experiments.selection_producer import load_selection_request

    request = load_selection_request(canary._selection_config(args))
    assert request.dataset == "cora"
    assert request.strategies == ("degree",)
    assert request.train_ratio == 0.8
    assert request.is_transductive is True
    with pytest.raises(SystemExit):
        canary._parser().parse_args(
            ["cold", "--store-root", str((tmp_path / "store").resolve()), "--allow-download"]
        )
    with pytest.raises(SystemExit):
        canary._parser().parse_args(
            ["cold", "--store-root", str((tmp_path / "store").resolve()), "--dataset-root", "raw"]
        )


def test_execute_delegates_dataset_and_production_to_experiment_layer(tmp_path, monkeypatch):
    captured = {}

    def fake_materialize(**kwargs):
        captured.update(kwargs)
        return {
            "ok": True,
            "results": [{"hit": False, "producer_called": True}],
            "split_reconstructed": False,
        }

    import experiments.selection_producer as producer

    monkeypatch.setattr(producer, "materialize_selection", fake_materialize)
    sentinel = object()
    document = canary.execute(_args(tmp_path), dataset_inputs=sentinel)

    assert captured["dataset_inputs"] is sentinel
    assert captured["processed_root"] == (tmp_path / "processed").resolve()
    assert captured["fail_if_producer_called"] is False
    assert document["dataset_access_owner"] == "experiments.selection_inputs"
    assert document["download_performed"] is False
    assert document["split_reconstructed"] is False


def test_warm_canary_arms_producer_sentinel(tmp_path, monkeypatch):
    captured = {}

    def fake_materialize(**kwargs):
        captured.update(kwargs)
        return {"ok": True, "results": [{"hit": True, "producer_called": False}]}

    import experiments.selection_producer as producer

    monkeypatch.setattr(producer, "materialize_selection", fake_materialize)
    canary.execute(_args(tmp_path, mode="warm"), dataset_inputs=object())
    assert captured["fail_if_producer_called"] is True


@pytest.mark.parametrize(
    ("mode", "result"),
    [
        ("cold", {"hit": True, "producer_called": False}),
        ("cold", {"hit": False, "producer_called": False}),
        ("warm", {"hit": False, "producer_called": True}),
        ("warm", {"hit": True, "producer_called": True}),
    ],
)
def test_phase_contract_fails_closed(mode, result):
    with pytest.raises(RuntimeError):
        canary._validate_phase(mode, {"results": [result]})
