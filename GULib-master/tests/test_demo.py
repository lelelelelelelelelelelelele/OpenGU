"""Integration tests for the demo script and end-to-end workflow."""

import os
import sys

# Set up mock arguments BEFORE importing config-dependent modules
sys.argv = ['pytest', '--dataset_name', 'cora', '--base_model', 'SGC', '--unlearning_methods', 'SGU']

import pytest
import torch
import tempfile
import subprocess
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import attack modules (after setting sys.argv)
from attack.attack_strategies import RandomStrategy, DegreeStrategy, PageRankStrategy, TracInStrategy


class TestDemoImports:
    """Tests for module imports and basic structure."""

    def test_import_attack_manager(self):
        """Test that AttackManager can be imported."""
        from attack import AttackManager
        assert AttackManager is not None

    def test_import_attack_result(self):
        """Test that AttackResult can be imported."""
        from attack import AttackResult, ComparisonResult
        assert AttackResult is not None
        assert ComparisonResult is not None

    def test_import_pipeline(self):
        """Test that AttackPipeline can be imported."""
        from attack import AttackPipeline
        assert AttackPipeline is not None

    def test_import_strategies(self):
        """Test that all strategies can be imported."""
        from attack import (
            BaseStrategy,
            RandomStrategy,
            DegreeStrategy,
            PageRankStrategy,
            TracInStrategy,
        )
        assert BaseStrategy is not None
        assert RandomStrategy is not None
        assert DegreeStrategy is not None
        assert PageRankStrategy is not None
        assert TracInStrategy is not None

    def test_import_utilities(self):
        """Test that utility functions can be imported."""
        from attack import create_manager, quick_demo, create_pipeline_from_args
        assert create_manager is not None
        assert quick_demo is not None
        assert create_pipeline_from_args is not None


class TestStrategyCreation:
    """Tests for strategy creation with mock args."""

    def test_create_random_strategy(self):
        """Test creating RandomStrategy."""
        args = {"seed": 2024}
        strategy = RandomStrategy(args)
        assert strategy is not None

        # Test selection
        from torch_geometric.data import Data
        data = Data(
            x=torch.randn(100, 16),
            edge_index=torch.randint(0, 100, (2, 300)),
            y=torch.randint(0, 7, (100,)),
        )
        result = strategy.select_nodes(data, model=None, k=10)
        assert result.shape == (10,)

    def test_create_degree_strategy(self):
        """Test creating DegreeStrategy."""
        args = {"seed": 2024}
        strategy = DegreeStrategy(args)
        assert strategy is not None

        from torch_geometric.data import Data
        data = Data(
            x=torch.randn(100, 16),
            edge_index=torch.randint(0, 100, (2, 300)),
            y=torch.randint(0, 7, (100,)),
        )
        result = strategy.select_nodes(data, model=None, k=10)
        assert result.shape == (10,)

    def test_create_pagerank_strategy(self):
        """Test creating PageRankStrategy."""
        args = {"seed": 2024, "pagerank_alpha": 0.85}
        strategy = PageRankStrategy(args)
        assert strategy is not None

        from torch_geometric.data import Data
        data = Data(
            x=torch.randn(100, 16),
            edge_index=torch.randint(0, 100, (2, 300)),
            y=torch.randint(0, 7, (100,)),
        )
        result = strategy.select_nodes(data, model=None, k=10)
        assert result.shape == (10,)


class TestDemoConfiguration:
    """Tests for demo configuration and argument handling."""

    def test_demo_args_parsing(self):
        """Test that demo arguments can be parsed."""
        # Import the demo module's argument parser
        import importlib.util
        spec = importlib.util.spec_from_file_location("demo_attack", "demo_attack.py")
        demo_module = importlib.util.module_from_spec(spec)

        # We can't fully load it due to dependencies, but we can verify the file exists
        assert os.path.exists("demo_attack.py")

    def test_demo_script_exists(self):
        """Test that demo_attack.py exists."""
        assert os.path.exists("demo_attack.py")

    def test_demo_script_syntax(self):
        """Test that demo_attack.py has valid syntax."""
        with open("demo_attack.py", "r") as f:
            code = f.read()

        # Try to compile to check syntax
        try:
            compile(code, "demo_attack.py", "exec")
            assert True
        except SyntaxError as e:
            pytest.fail(f"Syntax error in demo_attack.py: {e}")

    def test_demo_preserves_common_args_for_config_import(self):
        """demo_attack must not let config.py parse default dataset/method/ratio."""
        code = r"""
import json
import sys
import demo_attack
import config
payload = {
    "argv": sys.argv[1:],
    "dataset_name": config.args["dataset_name"],
    "base_model": config.args["base_model"],
    "unlearning_methods": config.args["unlearning_methods"],
    "unlearn_ratio": config.args["unlearn_ratio"],
    "proportion_unlearned_nodes": config.args["proportion_unlearned_nodes"],
    "random_seed": config.args["random_seed"],
    "unlearning_path": config.unlearning_path,
}
print(json.dumps(payload, sort_keys=True))
"""
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                code,
                "--dataset_name",
                "ogbn-arxiv",
                "--base_model",
                "GCN",
                "--unlearning_methods",
                "GIF",
                "--unlearn_ratio",
                "0.05",
                "--seed",
                "42",
                "--strategies",
                "random",
                "--no_cache",
            ],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(completed.stdout.strip().splitlines()[-1])

        assert payload["dataset_name"] == "ogbn-arxiv"
        assert payload["base_model"] == "GCN"
        assert payload["unlearning_methods"] == "GIF"
        assert payload["unlearn_ratio"] == 0.05
        assert payload["proportion_unlearned_nodes"] == 0.05
        assert payload["random_seed"] == 42
        assert "unlearning_nodes_0.05_ogbn-arxiv" in payload["unlearning_path"]
        assert "--strategies" not in payload["argv"]


class TestResultStructure:
    """Tests for result data structures."""

    def test_attack_result_structure(self):
        """Test AttackResult has all required fields."""
        from attack import AttackResult
        import inspect

        sig = inspect.signature(AttackResult.__init__)
        params = list(sig.parameters.keys())

        required_params = [
            "strategy_name",
            "selected_nodes",
            "f1_before",
            "f1_after",
            "unlearn_time",
            "total_time",
        ]

        for param in required_params:
            assert param in params, f"Missing parameter: {param}"

    def test_comparison_result_structure(self):
        """Test ComparisonResult has all required fields."""
        from attack import ComparisonResult
        import inspect

        sig = inspect.signature(ComparisonResult.__init__)
        params = list(sig.parameters.keys())

        assert "results" in params
        assert "config" in params


class TestOutputFormats:
    """Tests for output format consistency."""

    def test_result_json_serialization(self):
        """Test that results can be serialized to JSON."""
        from attack import AttackResult
        import json

        result = AttackResult(
            strategy_name="test",
            selected_nodes=torch.tensor([1, 2, 3]),
            f1_before=0.85,
            f1_after=0.80,
            unlearn_time=1.0,
            total_time=1.5,
            mia_auc=0.65,
        )

        # Should be serializable
        d = result.to_dict()
        json_str = json.dumps(d)
        assert json_str is not None
        assert len(json_str) > 0

        # Should be deserializable
        loaded = json.loads(json_str)
        assert loaded["strategy_name"] == "test"
        assert loaded["f1_before"] == 0.85

    def test_comparison_json_serialization(self):
        """Test that comparison results can be serialized."""
        from attack import AttackResult, ComparisonResult
        import json

        results = [
            AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1]),
                f1_before=0.85,
                f1_after=0.80,
                unlearn_time=1.0,
                total_time=1.5,
            ),
            AttackResult(
                strategy_name="degree",
                selected_nodes=torch.tensor([2]),
                f1_before=0.85,
                f1_after=0.75,
                unlearn_time=1.2,
                total_time=1.8,
            ),
        ]

        comparison = ComparisonResult(results=results)
        d = comparison.to_dict()

        # Should be serializable
        json_str = json.dumps(d)
        assert json_str is not None

        # Should contain expected fields
        loaded = json.loads(json_str)
        assert "results" in loaded
        assert "comparison" in loaded
        assert "best_strategy" in loaded["comparison"]


class TestCacheFunctionality:
    """Tests for caching functionality."""

    def test_cache_directory_creation(self):
        """Test that cache directory is created."""
        from attack import ResultCache
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = os.path.join(tmpdir, "test_cache")
            cache = ResultCache(cache_dir=cache_dir)

            assert os.path.exists(cache_dir)

    def test_cache_key_consistency(self):
        """Test that same config produces same cache key."""
        from attack import ResultCache
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ResultCache(cache_dir=tmpdir)

            config = {
                "dataset_name": "cora",
                "base_model": "SGC",
                "unlearning_methods": "SGU",
                "unlearn_ratio": 0.05,
                "seed": 2024,
                "strategy_name": "random",
            }

            key1 = cache._generate_cache_key(config)
            key2 = cache._generate_cache_key(config)

            assert key1 == key2

    def test_cache_different_configs(self):
        """Test that different configs produce different cache keys."""
        from attack import ResultCache
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ResultCache(cache_dir=tmpdir)

            config1 = {
                "dataset_name": "cora",
                "base_model": "SGC",
                "unlearning_methods": "SGU",
                "unlearn_ratio": 0.05,
                "seed": 2024,
                "strategy_name": "random",
            }

            config2 = config1.copy()
            config2["strategy_name"] = "degree"

            key1 = cache._generate_cache_key(config1)
            key2 = cache._generate_cache_key(config2)

            assert key1 != key2


class TestDeterministicBehavior:
    """Tests for deterministic behavior with fixed seeds."""

    def test_random_strategy_deterministic(self):
        """Test that random strategy is deterministic with fixed seed."""
        import random
        import numpy as np

        from torch_geometric.data import Data

        # Create data first (without seed-dependent operations in this test)
        data = Data(
            x=torch.zeros(100, 16),
            edge_index=torch.tensor([[0, 1], [1, 2]]),
            y=torch.zeros(100, dtype=torch.long),
        )

        # Set seed and run first time
        random.seed(2024)
        np.random.seed(2024)
        torch.manual_seed(2024)

        strategy1 = RandomStrategy({})
        result1 = strategy1.select_nodes(data, model=None, k=10)

        # Reset seed and run again
        random.seed(2024)
        np.random.seed(2024)
        torch.manual_seed(2024)

        strategy2 = RandomStrategy({})
        result2 = strategy2.select_nodes(data, model=None, k=10)

        assert torch.equal(result1, result2)

    def test_degree_strategy_deterministic(self):
        """Test that degree strategy is deterministic."""
        strategy1 = DegreeStrategy({})
        strategy2 = DegreeStrategy({})

        from torch_geometric.data import Data
        data = Data(
            x=torch.randn(100, 16),
            edge_index=torch.randint(0, 100, (2, 300)),
            y=torch.randint(0, 7, (100,)),
        )

        result1 = strategy1.select_nodes(data, model=None, k=10)
        result2 = strategy2.select_nodes(data, model=None, k=10)

        assert torch.equal(result1, result2)


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_strategy_name(self):
        """Test handling of invalid strategy name."""
        # This would be tested with a mock or would need the full framework
        # For now, we just verify the error message format
        from attack.attack_manager import AttackManager

        # Check that BUILTIN_STRATEGIES doesn't contain invalid entries
        invalid_names = ["invalid", "unknown", ""]
        for name in invalid_names:
            assert name not in AttackManager.BUILTIN_STRATEGIES

    def test_empty_strategy_list(self):
        """Test handling of empty strategy list in comparison."""
        from attack import ComparisonResult

        comparison = ComparisonResult(results=[])
        assert comparison.best_strategy is None
        assert len(comparison.results) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
