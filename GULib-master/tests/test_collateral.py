"""Tests for train_only pipeline support, _get_trained_model, run_retrain, and eval_collateral."""

import importlib.util
import os
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


# ===========================================================================
# Test: run_retrain mask manipulation
# ===========================================================================

class TestRunRetrainMask:
    """Test that run_retrain correctly manipulates train_mask and restores it."""

    def test_train_mask_restored_after_retrain(self):
        """train_mask should be fully restored after run_retrain."""
        from attack.pipeline_adapter import AttackPipeline

        data = _make_dummy_data()
        original_mask = data.train_mask.clone()
        selected = torch.tensor([0, 1, 2, 3, 4])

        obj = object.__new__(AttackPipeline)
        obj.args = {"train_only": False, "num_runs": 1, "base_model": "GCN"}
        obj.data = data
        obj.original_data = MagicMock()
        obj.dataset = MagicMock()
        obj.logger = MagicMock()

        fake_model = _make_dummy_model()
        mock_mz = MagicMock()
        mock_mz.model = fake_model

        mock_method = MagicMock()
        mock_method.target_model.model = fake_model
        mock_method.run_exp = MagicMock()

        with patch('attack.pipeline_adapter.model_zoo', return_value=mock_mz), \
             patch('attack.pipeline_adapter.UnlearningManager') as mock_um:
            mock_um.return_value.get_method.return_value = mock_method
            obj._evaluate_model = lambda m: 0.75

            _, f1 = obj.run_retrain(selected)

        assert torch.equal(data.train_mask, original_mask)
        assert obj.args["train_only"] is False
        assert f1 == 0.75

    def test_selected_nodes_excluded_during_retrain(self):
        """During retrain, selected nodes should be masked out in train_mask."""
        from attack.pipeline_adapter import AttackPipeline

        data = _make_dummy_data()
        selected = torch.tensor([0, 1, 2])

        obj = object.__new__(AttackPipeline)
        obj.args = {"train_only": False, "num_runs": 1, "base_model": "GCN"}
        obj.data = data
        obj.original_data = MagicMock()
        obj.dataset = MagicMock()
        obj.logger = MagicMock()

        captured_masks = []

        fake_model = _make_dummy_model()
        mock_mz = MagicMock()
        mock_mz.model = fake_model

        def capture_run_exp():
            captured_masks.append(data.train_mask.clone())

        mock_method = MagicMock()
        mock_method.target_model.model = fake_model
        mock_method.run_exp = capture_run_exp

        with patch('attack.pipeline_adapter.model_zoo', return_value=mock_mz), \
             patch('attack.pipeline_adapter.UnlearningManager') as mock_um:
            mock_um.return_value.get_method.return_value = mock_method
            obj._evaluate_model = lambda m: 0.70

            obj.run_retrain(selected)

        assert len(captured_masks) == 1
        mask_during = captured_masks[0]
        for node_id in selected.tolist():
            assert mask_during[node_id].item() is False

    def test_train_only_flag_set_during_retrain(self):
        """train_only should be True when run_exp is called during retrain."""
        from attack.pipeline_adapter import AttackPipeline

        data = _make_dummy_data()
        selected = torch.tensor([5, 6])

        obj = object.__new__(AttackPipeline)
        obj.args = {"train_only": False, "num_runs": 1, "base_model": "GCN"}
        obj.data = data
        obj.original_data = MagicMock()
        obj.dataset = MagicMock()
        obj.logger = MagicMock()

        captured_args = []

        fake_model = _make_dummy_model()
        mock_mz = MagicMock()
        mock_mz.model = fake_model

        def capture_run_exp():
            captured_args.append(obj.args.get("train_only"))

        mock_method = MagicMock()
        mock_method.target_model.model = fake_model
        mock_method.run_exp = capture_run_exp

        with patch('attack.pipeline_adapter.model_zoo', return_value=mock_mz), \
             patch('attack.pipeline_adapter.UnlearningManager') as mock_um:
            mock_um.return_value.get_method.return_value = mock_method
            obj._evaluate_model = lambda m: 0.70

            obj.run_retrain(selected)

        assert captured_args == [True]
        # After retrain, should be reset
        assert obj.args["train_only"] is False


# ===========================================================================
# Test: eval_collateral.py helper
# ===========================================================================

class TestFindCacheEntry:
    """Test the find_cache_entry function."""

    def test_returns_none_for_missing(self):
        from eval_collateral import find_cache_entry
        cache = MagicMock()
        cache.get.return_value = None

        result = find_cache_entry(cache, {"dataset_name": "cora"}, "random")
        assert result is None

    def test_passes_strategy_name_in_config(self):
        from eval_collateral import find_cache_entry
        cache = MagicMock()
        cache.get.return_value = MagicMock()

        args = {"dataset_name": "cora", "base_model": "GCN"}
        find_cache_entry(cache, args, "tracin")

        call_config = cache.get.call_args[0][0]
        assert call_config['strategy_name'] == 'tracin'

    def test_strips_non_hashable_keys(self):
        from eval_collateral import find_cache_entry
        cache = MagicMock()
        cache.get.return_value = None

        args = {"dataset_name": "cora", "complex_obj": [1, 2, 3]}
        find_cache_entry(cache, args, "random")

        call_config = cache.get.call_args[0][0]
        assert 'complex_obj' not in call_config

    def test_does_not_mutate_original_args(self):
        from eval_collateral import find_cache_entry
        cache = MagicMock()
        cache.get.return_value = None

        args = {"dataset_name": "cora", "base_model": "GCN"}
        find_cache_entry(cache, args, "random")

        # Original args should not have strategy_name added
        assert 'strategy_name' not in args

    def test_matches_random_seed_when_scanning_cache_files(self):
        from eval_collateral import find_cache_entry
        from attack.result_cache import ResultCache
        from attack.attack_result import AttackResult

        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ResultCache(cache_dir=tmpdir)
            base_config = {
                "dataset_name": "cora",
                "base_model": "GCN",
                "unlearning_methods": "GNNDelete",
                "unlearn_ratio": 0.05,
                "strategy_name": "random",
                "unlearn_task": "node",
                "downstream_task": "node",
                "is_transductive": True,
                "is_balanced": False,
            }

            config_seed_1 = base_config.copy()
            config_seed_1["random_seed"] = 111
            config_seed_2 = base_config.copy()
            config_seed_2["random_seed"] = 222

            result_seed_1 = AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1, 2, 3]),
                f1_before=0.8,
                f1_after=0.7,
                unlearn_time=1.0,
                total_time=1.5,
            )
            result_seed_2 = AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([4, 5, 6]),
                f1_before=0.8,
                f1_after=0.6,
                unlearn_time=1.0,
                total_time=1.5,
            )

            cache.save(result_seed_1, config_seed_1)
            cache.save(result_seed_2, config_seed_2)

            args = {
                "dataset_name": "cora",
                "base_model": "GCN",
                "unlearning_methods": "GNNDelete",
                "unlearn_ratio": 0.05,
                "random_seed": 222,
            }
            matched = find_cache_entry(cache, args, "random")
            assert matched is not None
            assert matched.selected_nodes.tolist() == [4, 5, 6]
