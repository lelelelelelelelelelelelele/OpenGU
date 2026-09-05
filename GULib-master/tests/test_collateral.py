"""Tests for train_only pipeline support, _get_trained_model."""

import importlib.util
import os
import random
import sys
import tempfile
import torch
import torch.nn as nn
import numpy as np
from unittest.mock import MagicMock, patch
from torch_geometric.data import Data


# ---------------------------------------------------------------------------
# Direct module loader to avoid pipeline/__init__.py circular imports
# ---------------------------------------------------------------------------

_MODULE_CACHE = {}

def _load_module_direct(filename, subdir='pipeline'):
    """Load a module file directly, bypassing __init__.py."""
    key = f"{subdir}/{filename}"
    if key in _MODULE_CACHE:
        return _MODULE_CACHE[key]
    module_name = f"_direct_{subdir}_{filename.replace('.py', '')}"
    filepath = os.path.join(os.path.dirname(__file__), '..', subdir, filename)
    filepath = os.path.abspath(filepath)
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    _MODULE_CACHE[key] = mod
    return mod


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_dummy_data(num_nodes=100, num_features=16, num_classes=7):
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, 300))
    y = torch.randint(0, num_classes, (num_nodes,))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:60] = True
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask[80:] = True
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, test_mask=test_mask)


def _make_dummy_model(num_features=16, num_classes=7):
    class DummyGNN(nn.Module):
        def __init__(self, in_ch, out_ch):
            super().__init__()
            self.lin = nn.Linear(in_ch, out_ch)

        def forward(self, x, edge_index=None):
            return self.lin(x)

    return DummyGNN(num_features, num_classes)


# ===========================================================================
# Test: train_only flag in pipeline base classes
# ===========================================================================

class TestTrainOnlyLearningBased:
    """Test train_only early return in Learning_based_pipeline.run_exp()."""

    def _get_cls(self):
        mod = _load_module_direct('Learning_based_pipeline.py')
        return mod.Learning_based_pipeline

    def test_train_only_skips_unlearn(self):
        """When train_only=True, unlearning_request and unlearn should NOT be called."""
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "downstream_task": "node",
                "unlearn_task": "node", "train_only": True}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.determine_target_model = lambda: calls.append("determine")
        pipeline.train_original_model = lambda: calls.append("train")
        pipeline.unlearning_request = lambda: calls.append("unlearn_request")
        pipeline.unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp()

        assert "train" in calls
        assert "unlearn_request" not in calls
        assert "unlearn" not in calls

    def test_default_runs_unlearn(self):
        """Without train_only, unlearning should proceed normally."""
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "downstream_task": "node",
                "unlearn_task": "node"}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.determine_target_model = lambda: calls.append("determine")
        pipeline.train_original_model = lambda: calls.append("train")
        pipeline.unlearning_request = lambda: calls.append("unlearn_request")
        pipeline.unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp()

        assert "train" in calls
        assert "unlearn_request" in calls
        assert "unlearn" in calls

    def test_run_exp_mem_unaffected_by_train_only(self):
        """run_exp_mem should NOT check train_only (backward compatibility)."""
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "train_only": True}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.determine_target_model = lambda: calls.append("determine")
        pipeline.train_original_model = lambda: calls.append("train")
        pipeline.unlearning_request = lambda: calls.append("unlearn_request")
        pipeline.unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp_mem()
        assert "unlearn" in calls

    def test_missing_train_only_key(self):
        """Pipeline works when train_only key is completely absent from args."""
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "downstream_task": "node",
                "unlearn_task": "node"}

        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.determine_target_model = lambda: calls.append("determine")
        pipeline.train_original_model = lambda: calls.append("train")
        pipeline.unlearning_request = lambda: calls.append("unlearn_request")
        pipeline.unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp()
        assert "unlearn" in calls
        assert "train_only" not in args  # Key should NOT have been added


class TestTrainOnlyShardBased:
    """Test train_only early return in Shard_based_pipeline.run_exp()."""

    def _get_cls(self):
        mod = _load_module_direct('Shard_based_pipeline.py')
        return mod.Shard_based_pipeline

    def test_train_only_skips_unlearn(self):
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "train_only": True}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.exp_partition = lambda: calls.append("partition")
        pipeline.exp_train = lambda: calls.append("train")
        pipeline.exp_unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp()

        assert "partition" in calls
        assert "train" in calls
        assert "unlearn" not in calls

    def test_default_runs_unlearn(self):
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.exp_partition = lambda: calls.append("partition")
        pipeline.exp_train = lambda: calls.append("train")
        pipeline.exp_unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp()

        assert "partition" in calls
        assert "train" in calls
        assert "unlearn" in calls

    def test_run_exp_mem_unaffected(self):
        cls = self._get_cls()
        args = {"num_runs": 1, "num_shards": 1, "train_only": True}
        model_zoo_mock = MagicMock()
        model_zoo_mock.data = _make_dummy_data()

        pipeline = cls(args, MagicMock(), model_zoo_mock)
        calls = []
        pipeline.exp_partition = lambda: calls.append("partition")
        pipeline.exp_train = lambda: calls.append("train")
        pipeline.exp_unlearn = lambda: calls.append("unlearn")

        pipeline.run_exp_mem()
        assert "unlearn" in calls


# NOTE: IF_based_pipeline tests are skipped because IF_based_pipeline.py
# imports `from task import get_trainer` at module level, which triggers
# circular imports in isolation. The train_only logic is identical across
# all 3 pipelines (same 2-line pattern), so Learning + Shard coverage
# suffices. IF_based is verified in integration tests (actual experiment runs).


# ===========================================================================
# Test: _get_trained_model
# ===========================================================================

class TestGetTrainedModel:
    """Test _get_trained_model extracts model from different pipeline types."""

    def _make_attack_pipeline_stub(self):
        from attack.pipeline_adapter import AttackPipeline
        obj = object.__new__(AttackPipeline)
        obj.model = _make_dummy_model()
        obj.method = MagicMock()
        return obj

    def test_extracts_from_target_model(self):
        """IF/Learning based: method.target_model.model"""
        pipeline = self._make_attack_pipeline_stub()
        expected_model = _make_dummy_model()
        pipeline.method.target_model = MagicMock()
        pipeline.method.target_model.model = expected_model

        result = pipeline._get_trained_model()
        assert result is expected_model

    def test_extracts_from_model_zoo(self):
        """Shard based: method.model_zoo.model"""
        pipeline = self._make_attack_pipeline_stub()
        pipeline.method.target_model = None
        expected_model = _make_dummy_model()
        pipeline.method.model_zoo = MagicMock()
        pipeline.method.model_zoo.model = expected_model

        result = pipeline._get_trained_model()
        assert result is expected_model

    def test_fallback_to_pipeline_model(self):
        """If neither target_model nor model_zoo available, return self.model."""
        pipeline = self._make_attack_pipeline_stub()
        pipeline.method = MagicMock(spec=[])  # no attributes at all

        result = pipeline._get_trained_model()
        assert result is pipeline.model
