"""Unit tests for AttackManager and related components."""

import os
import sys

# Set up mock arguments BEFORE importing config-dependent modules
sys.argv = ['pytest', '--dataset_name', 'cora', '--base_model', 'SGC', '--unlearning_methods', 'SGU']

import pytest
import torch
import tempfile
import shutil
from pathlib import Path
from torch_geometric.data import Data

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import attack modules (after setting sys.argv)
from attack.attack_result import AttackResult, ComparisonResult
from attack.result_cache import ResultCache, LogBasedCache
from attack.attack_strategies import RandomStrategy, DegreeStrategy, PageRankStrategy


def _make_dummy_data(num_nodes=100, num_features=16, num_classes=7, num_edges=300):
    """Create a dummy PyG Data object for testing."""
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))
    y = torch.randint(0, num_classes, (num_nodes,))

    # Add train/val/test masks
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    train_mask[:60] = True
    val_mask[60:80] = True
    test_mask[80:] = True

    return Data(
        x=x,
        edge_index=edge_index,
        y=y,
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
    )


class TestAttackResult:
    """Tests for AttackResult data class."""

    def test_basic_creation(self):
        """Test basic AttackResult creation."""
        result = AttackResult(
            strategy_name="random",
            selected_nodes=torch.tensor([1, 2, 3]),
            f1_before=0.85,
            f1_after=0.75,
            unlearn_time=1.5,
            total_time=2.0,
        )

        assert result.strategy_name == "random"
        assert result.f1_before == 0.85
        assert result.f1_after == 0.75
        assert result.f1_drop == pytest.approx(0.10, abs=0.001)
        assert result.f1_drop_ratio == pytest.approx(11.76, abs=0.1)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = AttackResult(
            strategy_name="degree",
            selected_nodes=torch.tensor([1, 2, 3]),
            f1_before=0.90,
            f1_after=0.80,
            unlearn_time=2.0,
            total_time=3.0,
            mia_auc=0.65,
        )

        d = result.to_dict()

        assert d["strategy_name"] == "degree"
        assert d["f1_before"] == 0.90
        assert d["f1_after"] == 0.80
        assert d["f1_drop"] == 0.10
        assert d["mia_auc"] == 0.65
        assert "selected_nodes" in d

    def test_save_and_load(self):
        """Test saving and loading results."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = AttackResult(
                strategy_name="pagerank",
                selected_nodes=torch.tensor([1, 2, 3, 4, 5]),
                f1_before=0.88,
                f1_after=0.82,
                unlearn_time=1.0,
                total_time=1.5,
            )

            path = os.path.join(tmpdir, "result.json")
            result.save(path)

            assert os.path.exists(path)

            loaded = AttackResult.load(path)
            assert loaded.strategy_name == result.strategy_name
            assert loaded.f1_before == result.f1_before
            assert loaded.f1_after == result.f1_after


class TestComparisonResult:
    """Tests for ComparisonResult data class."""

    def test_basic_creation(self):
        """Test basic ComparisonResult creation."""
        results = [
            AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1, 2]),
                f1_before=0.85,
                f1_after=0.80,
                unlearn_time=1.0,
                total_time=1.5,
            ),
            AttackResult(
                strategy_name="degree",
                selected_nodes=torch.tensor([3, 4]),
                f1_before=0.85,
                f1_after=0.75,
                unlearn_time=1.2,
                total_time=1.8,
            ),
        ]

        comparison = ComparisonResult(results=results)

        assert comparison.best_strategy == "degree"
        assert len(comparison.results) == 2

    def test_relative_improvement(self):
        """Test relative improvement calculation."""
        results = [
            AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1, 2]),
                f1_before=0.90,
                f1_after=0.85,
                unlearn_time=1.0,
                total_time=1.5,
            ),
            AttackResult(
                strategy_name="degree",
                selected_nodes=torch.tensor([3, 4]),
                f1_before=0.90,
                f1_after=0.80,
                unlearn_time=1.2,
                total_time=1.8,
            ),
        ]

        comparison = ComparisonResult(results=results)

        # Random drop: 0.05, Degree drop: 0.10
        # Improvement: 0.10 / 0.05 = 2.0
        improvement = comparison.get_relative_improvement("degree", "random")
        assert improvement == pytest.approx(2.0, abs=0.01)


class TestResultCache:
    """Tests for ResultCache."""

    def test_cache_key_generation(self):
        """Test cache key generation."""
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

            # Same config should generate same key
            key1 = cache._generate_cache_key(config)
            key2 = cache._generate_cache_key(config)
            assert key1 == key2

            # Different config should generate different key
            config2 = config.copy()
            config2["strategy_name"] = "degree"
            key3 = cache._generate_cache_key(config2)
            assert key1 != key3

    def test_save_and_get(self):
        """Test saving and retrieving from cache."""
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

            result = AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1, 2, 3]),
                f1_before=0.85,
                f1_after=0.80,
                unlearn_time=1.0,
                total_time=1.5,
            )

            # Save to cache
            cache.save(result, config)

            # Retrieve from cache
            cached = cache.get(config)
            assert cached is not None
            assert cached.strategy_name == result.strategy_name
            assert cached.f1_before == result.f1_before

    def test_cache_miss(self):
        """Test cache miss."""
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

            # No cache entry exists
            cached = cache.get(config)
            assert cached is None

    def test_cache_invalidation(self):
        """Test cache invalidation."""
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

            result = AttackResult(
                strategy_name="random",
                selected_nodes=torch.tensor([1, 2, 3]),
                f1_before=0.85,
                f1_after=0.80,
                unlearn_time=1.0,
                total_time=1.5,
            )

            cache.save(result, config)
            assert cache.get(config) is not None

            # Invalidate
            cache.invalidate(config)
            assert cache.get(config) is None


class TestAttackManagerBasics:
    """Basic tests for AttackManager (without full pipeline)."""

    def test_strategy_registration(self):
        """Test strategy registration."""
        # Create mock args
        args = {
            "dataset_name": "cora",
            "base_model": "SGC",
            "unlearning_methods": "SGU",
            "unlearn_ratio": 0.05,
            "seed": 2024,
        }

        # Create manager (without pipeline)
        # Note: This test is limited since we can't easily mock the full pipeline
        # In practice, these tests would be run with the actual framework

        # Test that strategies can be created
        random_strategy = RandomStrategy(args)
        degree_strategy = DegreeStrategy(args)

        assert random_strategy is not None
        assert degree_strategy is not None

    def test_builtin_strategies_list(self):
        """Test that built-in strategies are available."""
        from attack.attack_manager import AttackManager

        expected_strategies = ["random", "degree", "pagerank", "tracin"]

        for strategy in expected_strategies:
            assert strategy in AttackManager.BUILTIN_STRATEGIES


class TestAttackResultEdgeCases:
    """Edge case tests for AttackResult."""

    def test_zero_f1_before(self):
        """Test handling of zero f1_before."""
        result = AttackResult(
            strategy_name="test",
            selected_nodes=torch.tensor([1]),
            f1_before=0.0,
            f1_after=0.0,
            unlearn_time=1.0,
            total_time=1.0,
        )

        assert result.f1_drop_ratio == 0.0

    def test_negative_f1_drop(self):
        """Test handling of negative F1 drop (improvement)."""
        result = AttackResult(
            strategy_name="test",
            selected_nodes=torch.tensor([1]),
            f1_before=0.80,
            f1_after=0.85,
            unlearn_time=1.0,
            total_time=1.0,
        )

        assert result.f1_drop == pytest.approx(-0.05, abs=0.001)
        assert result.f1_drop_ratio < 0

    def test_empty_selected_nodes(self):
        """Test handling of empty selected nodes."""
        result = AttackResult(
            strategy_name="test",
            selected_nodes=torch.tensor([]),
            f1_before=0.85,
            f1_after=0.85,
            unlearn_time=0.0,
            total_time=0.0,
        )

        assert len(result.selected_nodes) == 0
        d = result.to_dict()
        assert d["selected_nodes"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
