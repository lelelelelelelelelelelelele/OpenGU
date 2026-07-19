"""CPU-only tests for experiment-owned canonical processed artifacts."""

from __future__ import annotations

import pickle
import json
import importlib
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from experiments.processed_provider import (
    ProcessedArtifactError,
    processed_artifact_paths,
)


def _args(processed_root: Path):
    return {
        "dataset_name": "cora",
        "base_model": "GCN",
        "is_transductive": True,
        "is_balanced": False,
        "train_ratio": 0.8,
        "val_ratio": 0,
        "test_ratio": 0.2,
        "proportion_unlearned_nodes": 0.05,
        "processed_root": str(processed_root.resolve()),
    }


def _write_pair(processed_root: Path):
    args = _args(processed_root)
    paths = processed_artifact_paths(args)
    paths.data_path.parent.mkdir(parents=True)
    data = SimpleNamespace(
        num_nodes=2708,
        num_edges=10556,
        train_indices=[0, 1, 2],
    )
    dataset = SimpleNamespace(num_classes=7)
    with paths.data_path.open("wb") as handle:
        pickle.dump(data, handle)
    with paths.dataset_path.open("wb") as handle:
        pickle.dump(dataset, handle)
    return args, paths, data, dataset


def test_processed_provider_uses_canonical_cora_names(tmp_path):
    args = _args(tmp_path / "processed")
    paths = processed_artifact_paths(args)

    assert paths.data_path.name == "cora0.8_0_0.2.pkl"
    assert paths.dataset_path.name == "cora0.8_0_0.2dataset.pkl"
    assert paths.lane == "transductive"
    assert paths.explicit is True


def test_original_dataset_explicit_provider_never_calls_planetoid(tmp_path, monkeypatch):
    args, paths, expected_data, expected_dataset = _write_pair(tmp_path / "processed")
    original_module = importlib.import_module("dataset.original_dataset")

    monkeypatch.setattr(
        original_module,
        "Planetoid",
        lambda *_args, **_kwargs: pytest.fail("Planetoid must not be called"),
    )
    logger = SimpleNamespace(info=lambda *_args, **_kwargs: None)
    loader = original_module.original_dataset(args, logger)

    data, dataset = loader.load_data()

    assert data.num_nodes == expected_data.num_nodes
    assert dataset.num_classes == expected_dataset.num_classes
    assert args["num_unlearned_nodes"] == 135
    assert paths.available


def test_original_dataset_explicit_provider_fails_closed_when_pair_missing(
    tmp_path, monkeypatch
):
    args = _args(tmp_path / "processed")
    paths = processed_artifact_paths(args)
    paths.data_path.parent.mkdir(parents=True)
    with paths.data_path.open("wb") as handle:
        pickle.dump(SimpleNamespace(num_nodes=2708), handle)

    original_module = importlib.import_module("dataset.original_dataset")

    monkeypatch.setattr(
        original_module,
        "Planetoid",
        lambda *_args, **_kwargs: pytest.fail("download fallback must not run"),
    )
    logger = SimpleNamespace(info=lambda *_args, **_kwargs: None)

    with pytest.raises(ProcessedArtifactError, match="forbids raw loading"):
        original_module.original_dataset(args, logger).load_data()


def test_process_data_explicit_provider_does_not_reconstruct_split(tmp_path, monkeypatch):
    args, _paths, expected_data, _dataset = _write_pair(tmp_path / "processed")
    args.update(
        {
            "downstream_task": "node",
            "unlearning_methods": "GIF",
            "unlearn_task": "feature",
        }
    )
    import utils.dataset_utils as dataset_utils

    for name in (
        "transductive_split_node",
        "transductive_split_node_balanced",
        "inductive_split_node",
        "inductive_split_node_balanced",
        "save_data",
    ):
        monkeypatch.setattr(
            dataset_utils,
            name,
            lambda *_args, _name=name, **_kwargs: pytest.fail(
                "{0} must not be called".format(_name)
            ),
        )
    logger = SimpleNamespace(info=lambda *_args, **_kwargs: None)

    observed = dataset_utils.process_data(
        logger,
        SimpleNamespace(num_nodes=1),
        args,
    )

    assert observed.num_nodes == expected_data.num_nodes
    assert observed.num_edges == expected_data.num_edges


def test_parameter_parser_accepts_experiment_owned_roots(tmp_path, monkeypatch):
    from parameter_parser import parameter_parser

    processed_root = (tmp_path / "processed").resolve()
    runtime_root = (tmp_path / "runtime").resolve()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test",
            "--processed_root",
            str(processed_root),
            "--runtime_root",
            str(runtime_root),
        ],
    )

    args = parameter_parser()

    assert args["processed_root"] == str(processed_root)
    assert args["runtime_root"] == str(runtime_root)


def test_config_separates_code_root_from_mutable_runtime_root(tmp_path):
    repository_root = Path(__file__).resolve().parents[1]
    runtime_root = (tmp_path / "runtime").resolve()
    code = """
import json
import config
print(json.dumps({
    "root_path": config.root_path,
    "runtime_root": config.runtime_root,
    "model_path": config.MODEL_PATH,
    "unlearning_path": config.unlearning_path,
}, sort_keys=True))
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            code,
            "--root_path",
            str(repository_root),
            "--runtime_root",
            str(runtime_root),
            "--unlearning_methods",
            "GIF",
        ],
        cwd=repository_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout.strip().splitlines()[-1])

    assert Path(payload["root_path"]) == repository_root
    assert Path(payload["runtime_root"]) == runtime_root
    assert runtime_root in Path(payload["model_path"]).parents
    assert runtime_root in Path(payload["unlearning_path"]).parents
