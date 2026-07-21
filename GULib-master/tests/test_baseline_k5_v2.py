import json
import pickle
from pathlib import Path
from types import SimpleNamespace

import pytest

from experiments.baseline_k5.baseline_contract import (
    LEGACY_ARCHIVE_ROOT_NAME,
    RESULT_ROOT_NAME,
    SCHEMA,
    SCHEMA_VERSION,
    default_result_root,
    expected_config,
    legacy_archive_root,
    measure_method_perf_before,
    validate_record,
    validate_output_root,
    validate_run_result,
)
from experiments.baseline_k5 import formal_preflight


class _Method:
    aggregate_f1_score = 0.713


class _ShardPipeline:
    method = _Method()

    def __init__(self):
        self.trained = False

    def _ensure_base_model_trained(self):
        self.trained = True

    def _get_trained_model(self):
        raise AssertionError("shard metric must not use a single model")


class _ModelPipeline:
    method = object()

    def __init__(self):
        self.trained = False
        self.model = object()

    def _ensure_base_model_trained(self):
        self.trained = True

    def _get_trained_model(self):
        return self.model

    def _evaluate_model(self, model):
        assert model is self.model
        return 0.882


def _record():
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "f1_after": 0.70,
        "method_perf_before": 0.72,
        "method_noise_drop": 0.02,
        "config": dict(
            expected_config(
                dataset="cora", model="GCN", method="GIF", seed=111, k=5
            )
        ),
    }


def test_v2_result_uses_canonical_path_and_legacy_has_separate_archive(tmp_path: Path):
    root = default_result_root(tmp_path)
    assert root.name == RESULT_ROOT_NAME
    assert root == tmp_path / "results" / "baseline" / "k5_random"
    archive = legacy_archive_root(tmp_path)
    assert archive.name == LEGACY_ARCHIVE_ROOT_NAME
    assert archive != root
    with pytest.raises(ValueError, match="legacy k5 archive is immutable"):
        validate_output_root(archive / "GraphRevoker", tmp_path)


@pytest.mark.parametrize("method", ["GraphEraser", "GraphRevoker"])
def test_shard_before_uses_aggregate_metric(method):
    pipeline = _ShardPipeline()
    value, source = measure_method_perf_before(pipeline, method)
    assert pipeline.trained is True
    assert value == pytest.approx(0.713)
    assert source == "shard_aggregate_f1"


def test_non_shard_before_uses_trained_model_evaluation():
    pipeline = _ModelPipeline()
    value, source = measure_method_perf_before(pipeline, "GIF")
    assert pipeline.trained is True
    assert value == pytest.approx(0.882)
    assert source == "trained_model_test_f1"


def test_failed_unlearning_is_rejected_even_with_plausible_f1():
    with pytest.raises(RuntimeError, match="boom"):
        validate_run_result(
            {
                "failed": True,
                "failure_reason": "boom",
                "f1_after": 0.8,
                "selected_nodes": list(range(5)),
            },
            5,
        )


def test_legacy_record_cannot_be_reused_as_v2():
    record = _record()
    record.pop("schema")
    with pytest.raises(ValueError, match="not a k5 noise-anchor v2"):
        validate_record(record, _record()["config"])


@pytest.mark.parametrize("method", ["GraphEraser", "GraphRevoker"])
def test_shard_v2_record_cannot_claim_single_model_before(method):
    expected = expected_config(
        dataset="cora", model="GCN", method=method, seed=111, k=5
    )
    record = _record()
    record["config"] = dict(expected)
    record["config"]["before_metric_source"] = "trained_model_test_f1"
    with pytest.raises(ValueError, match="before_metric_source"):
        validate_record(record, expected)


def test_v2_record_requires_consistent_noise_drop():
    record = _record()
    validate_record(record, record["config"])
    record["method_noise_drop"] = 0.01
    with pytest.raises(ValueError, match="inconsistent"):
        validate_record(record, record["config"])


def test_processed_source_records_real_paths_hashes_and_split(tmp_path: Path):
    lane = tmp_path / "data" / "processed" / "transductive"
    lane.mkdir(parents=True)
    data_path = lane / "cora0.8_0_0.2.pkl"
    dataset_path = lane / "cora0.8_0_0.2dataset.pkl"
    data = SimpleNamespace(
        num_nodes=4,
        edge_index=SimpleNamespace(shape=(2, 6)),
        train_mask=[True, True, True, False],
        val_mask=[False, False, False, False],
        test_mask=[False, False, False, True],
    )
    data_path.write_bytes(pickle.dumps(data))
    dataset_path.write_bytes(pickle.dumps({"name": "cora"}))

    source = formal_preflight.resolve_processed_source(tmp_path, dataset="cora")
    assert source["resolved_root"] == str((tmp_path / "data" / "processed").resolve())
    assert source["split_identity"]["counts"] == {
        "train": 3,
        "val": 0,
        "test": 1,
    }
    assert len(source["source_fingerprint"]) == 64
    assert all(len(item["sha256"]) == 64 for item in source["files"])


def test_formal_preflight_reports_exact_git_and_gpu_blockers(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        formal_preflight,
        "collect_git_provenance",
        lambda root: {
            "branch": "codex/wip",
            "git_sha": "a" * 40,
            "dirty": True,
            "status_entries": [" M results/_journal/auto_report.md"],
        },
    )
    monkeypatch.setattr(
        formal_preflight,
        "resolve_processed_source",
        lambda root, dataset: {"dataset": dataset, "source_fingerprint": "b" * 64},
    )
    monkeypatch.setattr(
        formal_preflight,
        "collect_gpu_provenance",
        lambda: {
            "devices": [{"index": 0, "name": "NVIDIA A100"}],
            "torch_cuda_available": False,
            "torch_device_name": None,
        },
    )
    result = formal_preflight.build_formal_preflight(
        tmp_path, expected_git_sha="c" * 40
    )
    assert result["ready"] is False
    text = "\n".join(result["errors"])
    assert "git-branch" in text
    assert "git-sha" in text
    assert "git-dirty" in text
    assert "RTX 4090 required" in text
    assert "torch.cuda.is_available() is false" in text
