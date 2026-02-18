"""
AttackManager - Central dispatcher for attack experiments.

This module provides the main interface for running attack experiments,
managing strategies, and collecting results.
"""
import os
import sys
import time
import torch
from typing import Dict, List, Optional, Any, Type
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from attack.attack_strategies import (
    BaseStrategy,
    RandomStrategy,
    DegreeStrategy,
    PageRankStrategy,
    TracInStrategy,
)
from attack.attack_result import AttackResult, ComparisonResult
from attack.pipeline_adapter import AttackPipeline
from attack.result_cache import ResultCache, LogBasedCache


class AttackManager:
    """
    Central manager for attack experiments.

    The AttackManager:
    1. Registers and manages attack strategies
    2. Coordinates "select nodes → run unlearning → collect results"
    3. Supports multi-strategy comparison experiments
    4. Handles result caching

    Example:
        >>> args = parameter_parser()
        >>> data, model = ...  # Load from pipeline
        >>> manager = AttackManager(args, data, model)
        >>> manager.register_strategy("random", RandomStrategy(args))
        >>> manager.register_strategy("tracin", TracInStrategy(args))
        >>> result = manager.run_attack("tracin", k=50)
        >>> comparison = manager.compare_strategies(["random", "tracin"], k=50)
    """

    # Built-in strategy registry
    BUILTIN_STRATEGIES = {
        "random": RandomStrategy,
        "degree": DegreeStrategy,
        "pagerank": PageRankStrategy,
        "tracin": TracInStrategy,
    }

    def __init__(
        self,
        args: Dict[str, Any],
        pipeline: Optional[AttackPipeline] = None,
        cache_dir: str = "./results/cache",
        use_cache: bool = True,
    ):
        """
        Initialize the AttackManager.

        Args:
            args: Configuration dictionary from parameter_parser()
            pipeline: Optional pre-initialized AttackPipeline
            cache_dir: Directory for result caching
            use_cache: Whether to enable result caching
        """
        self.args = args
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Initialize pipeline
        if pipeline is None:
            self.pipeline = AttackPipeline(args)
        else:
            self.pipeline = pipeline

        self.data = self.pipeline.data
        self.model = self.pipeline.model

        # Strategy registry
        self._strategies: Dict[str, BaseStrategy] = {}

        # Cache
        self.use_cache = use_cache
        if use_cache:
            self.cache = ResultCache(cache_dir)
            self.log_cache = LogBasedCache()
        else:
            self.cache = None
            self.log_cache = None

        # Results storage
        self.results: Dict[str, AttackResult] = {}

        # Register built-in strategies
        self._register_builtin_strategies()

    def _register_builtin_strategies(self):
        """Register all built-in strategies."""
        for name, strategy_class in self.BUILTIN_STRATEGIES.items():
            try:
                strategy = strategy_class(self.args)
                self.register_strategy(name, strategy)
            except Exception as e:
                print(f"[AttackManager] Failed to register {name}: {e}")

    def register_strategy(self, name: str, strategy: BaseStrategy):
        """
        Register an attack strategy.

        Args:
            name: Unique name for the strategy
            strategy: Strategy instance
        """
        self._strategies[name] = strategy
        print(f"[AttackManager] Registered strategy: {name}")

    def get_strategy(self, name: str) -> Optional[BaseStrategy]:
        """
        Get a registered strategy by name.

        Args:
            name: Strategy name

        Returns:
            Strategy instance or None if not found
        """
        return self._strategies.get(name)

    def list_strategies(self) -> List[str]:
        """List all registered strategy names."""
        return list(self._strategies.keys())

    def _build_config(self, strategy_name: str, k: int) -> Dict[str, Any]:
        """Build configuration dict for caching."""
        config = self.args.copy()
        config['strategy_name'] = strategy_name
        config['k'] = k
        # Remove non-hashable items
        for key in list(config.keys()):
            if not isinstance(config[key], (str, int, float, bool, type(None))):
                del config[key]
        return config

    def run_attack(self, strategy_name: str, k: int, use_cache: Optional[bool] = None) -> AttackResult:
        """
        Run a single attack experiment.

        Args:
            strategy_name: Name of the strategy to use
            k: Number of nodes to select
            use_cache: Override global cache setting

        Returns:
            AttackResult containing experiment results

        Raises:
            ValueError: If strategy not found
        """
        strategy = self.get_strategy(strategy_name)
        if strategy is None:
            raise ValueError(f"Strategy '{strategy_name}' not found. Registered: {self.list_strategies()}")

        # Check cache
        use_cache = use_cache if use_cache is not None else self.use_cache
        config = self._build_config(strategy_name, k)

        if use_cache and self.cache:
            cached_result = self.cache.get(config)
            if cached_result is not None:
                self.results[strategy_name] = cached_result
                return cached_result

        # Run experiment
        print(f"\n[AttackManager] Running attack with strategy: {strategy_name}")
        print(f"[AttackManager] Selecting {k} nodes for unlearning")

        start_time = time.time()

        # Run through pipeline
        result_dict = self.pipeline.run_with_strategy(strategy, k)

        total_time = time.time() - start_time

        # Build AttackResult
        result = AttackResult(
            strategy_name=strategy_name,
            selected_nodes=result_dict["selected_nodes"],
            f1_before=result_dict["f1_before"],
            f1_after=result_dict["f1_after"],
            unlearn_time=result_dict["unlearn_time"],
            total_time=total_time,
            mia_auc=result_dict.get("mia_auc"),
            config=config,
        )

        # Store and cache result
        self.results[strategy_name] = result

        if use_cache and self.cache:
            self.cache.save(result, config)

        return result

    def compare_strategies(
        self,
        strategy_names: Optional[List[str]] = None,
        k: int = 50,
        save_path: Optional[str] = None,
    ) -> ComparisonResult:
        """
        Compare multiple strategies.

        Args:
            strategy_names: List of strategy names to compare (None = all registered)
            k: Number of nodes to select
            save_path: Optional path to save comparison results

        Returns:
            ComparisonResult containing all results
        """
        if strategy_names is None:
            strategy_names = self.list_strategies()

        print(f"\n[AttackManager] Comparing {len(strategy_names)} strategies: {strategy_names}")
        print(f"[AttackManager] Each strategy will select {k} nodes\n")

        results = []

        for name in strategy_names:
            try:
                result = self.run_attack(name, k)
                results.append(result)
            except Exception as e:
                print(f"[AttackManager] Error running {name}: {e}")
                import traceback
                traceback.print_exc()

        # Build comparison result
        config = self._build_config("comparison", k)
        config['strategies'] = strategy_names

        comparison = ComparisonResult(results=results, config=config)

        # Save if requested
        if save_path:
            comparison.save(save_path)
            print(f"[AttackManager] Saved comparison results to: {save_path}")

        # Print summary
        comparison.print_summary()

        return comparison

    def save_results(self, base_path: str):
        """
        Save all results to a directory.

        Args:
            base_path: Directory path for saving results
        """
        base_dir = Path(base_path)
        base_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save individual results
        for name, result in self.results.items():
            path = base_dir / f"{name}_{timestamp}.json"
            result.save(str(path))

        print(f"[AttackManager] Saved {len(self.results)} results to: {base_dir}")

    def get_all_results(self) -> Dict[str, AttackResult]:
        """Get all stored results."""
        return self.results.copy()

    def clear_results(self):
        """Clear all stored results."""
        self.results.clear()


def create_manager(
    dataset_name: str = "cora",
    base_model: str = "SGC",
    unlearning_method: str = "SGU",
    unlearn_ratio: float = 0.05,
    **kwargs
) -> AttackManager:
    """
    Factory function to create an AttackManager with common configurations.

    Args:
        dataset_name: Dataset name (e.g., 'cora', 'citeseer')
        base_model: GNN model name (e.g., 'SGC', 'GCN')
        unlearning_method: Unlearning method name (e.g., 'SGU', 'GIF')
        unlearn_ratio: Ratio of nodes to unlearn
        **kwargs: Additional arguments

    Returns:
        Configured AttackManager
    """
    from parameter_parser import parameter_parser

    # Build args
    args = parameter_parser()

    # Override with provided values
    args['dataset_name'] = dataset_name
    args['base_model'] = base_model
    args['unlearning_methods'] = unlearning_method
    args['unlearn_ratio'] = unlearn_ratio

    # Apply additional kwargs
    for key, value in kwargs.items():
        args[key] = value

    return AttackManager(args)


def quick_demo(
    strategies: Optional[List[str]] = None,
    k: Optional[int] = None,
    dataset: str = "cora",
    model: str = "SGC",
    method: str = "SGU",
) -> ComparisonResult:
    """
    Quick demo function to compare attack strategies.

    Args:
        strategies: List of strategy names (default: ['random', 'tracin'])
        k: Number of nodes to select (default: 5% of dataset)
        dataset: Dataset name
        model: GNN model name
        method: Unlearning method name

    Returns:
        ComparisonResult
    """
    if strategies is None:
        strategies = ["random", "tracin"]

    # Create manager
    manager = create_manager(
        dataset_name=dataset,
        base_model=model,
        unlearning_method=method,
    )

    # Auto-determine k if not provided
    if k is None:
        num_nodes = manager.data.num_nodes
        k = int(num_nodes * 0.05)
        print(f"[QuickDemo] Auto-selected k={k} (5% of {num_nodes} nodes)")

    # Run comparison
    return manager.compare_strategies(strategies, k=k)
