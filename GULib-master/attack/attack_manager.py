"""
AttackManager - Central dispatcher for attack experiments.

This module provides the main interface for running attack experiments,
managing strategies, and collecting results.
"""
import os
import sys
import time
import json
import hashlib
import numpy as np
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
    IMStrategy,
    HybridStrategy,
    IMV4Strategy,
    HybridV4Strategy,
)
from attack.attack_result import AttackResult, ComparisonResult
from attack.pipeline_adapter import AttackPipeline
from attack.result_cache import ResultCache, LogBasedCache
from attack.selection_cache import SelectionCache, SelectionResult


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
    # Note: "im" and "hybrid" are aliased to the v4 (batch-CELF + decoupled MC seed)
    # implementations as of 2026-05-04. Old CELF / coupled-RNG classes (IMStrategy,
    # HybridStrategy in *_strategy.py) remain in source as base classes only — not
    # registered. Drop the v4 suffix everywhere downstream.
    BUILTIN_STRATEGIES = {
        "random": RandomStrategy,
        "degree": DegreeStrategy,
        "pagerank": PageRankStrategy,
        "tracin": TracInStrategy,
        "im": IMV4Strategy,
        "hybrid": HybridV4Strategy,
    }
    REUSABLE_SELECTION_STRATEGIES = {"random", "pagerank", "im"}
    # Runtime k-subset reuse is safe only for deterministic ranking strategies.
    SUBSET_REUSABLE_SELECTION_STRATEGIES = {"im"}

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
            self.selection_cache = SelectionCache("./results/selection_cache")
        else:
            self.cache = None
            self.log_cache = None
            self.selection_cache = None

        # Results storage
        self.results: Dict[str, AttackResult] = {}
        self._graph_fingerprint: Optional[str] = None

        # Register built-in strategies
        self._register_builtin_strategies()

    @staticmethod
    def _stable_hash(payload: Dict[str, Any]) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]

    def _seed_value(self) -> int:
        seed_value = self.args.get("random_seed", self.args.get("seed", 2024))
        try:
            return int(seed_value)
        except (TypeError, ValueError):
            return 2024

    def _candidate_nodes(self) -> np.ndarray:
        if hasattr(self.data, "train_mask") and self.data.train_mask is not None:
            nodes = self.data.train_mask.nonzero(as_tuple=False).squeeze(-1).cpu().numpy()
            return nodes.astype(np.int64, copy=False)
        return np.arange(self.data.num_nodes, dtype=np.int64)

    def _compute_graph_fingerprint(self) -> str:
        if self._graph_fingerprint is not None:
            return self._graph_fingerprint

        edge_index = self.data.edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
        candidates = self._candidate_nodes()
        digest = hashlib.sha256()
        digest.update(np.int64(self.data.num_nodes).tobytes())
        digest.update(edge_index.tobytes())
        digest.update(candidates.tobytes())
        self._graph_fingerprint = digest.hexdigest()[:32]
        return self._graph_fingerprint

    def _strategy_params_for_cache(self, strategy_name: str) -> Dict[str, Any]:
        if strategy_name == "im":
            # im is the batch-CELF v4 implementation (the v4 suffix was dropped 2026-05-04)
            return {
                "propagation_prob": float(self.args.get("propagation_prob", 0.1)),
                "mc_rounds": int(self.args.get("mc_rounds", 100)),
                "candidate_fraction": float(self.args.get("candidate_fraction", 1.0)),
                "im_batch_size": int(self.args.get("im_v4_batch_size", 5)),
            }
        elif strategy_name == "pagerank":
            return {
                "pagerank_alpha": float(self.args.get("pagerank_alpha", 0.85)),
            }
        return {}

    def _build_selection_config(self, strategy_name: str, k: int) -> Dict[str, Any]:
        strategy_params = self._strategy_params_for_cache(strategy_name)
        strategy_params_fingerprint = self._stable_hash(strategy_params)
        seed_for_key = self._seed_value()
        if strategy_name == "im":
            # IM uses a fixed im_selector_seed (default 2024, A.4-decoupled
            # from training seed). Anchoring the cache key to im_selector_seed
            # — not the training seed — lets cross-seed runs share a single
            # IM computation instead of recomputing identical results 3x.
            seed_for_key = int(self.args.get("im_selector_seed", 2024))
        return {
            "dataset_name": str(self.args.get("dataset_name", "")),
            "base_model": str(self.args.get("base_model", "")),
            "unlearn_ratio": float(self.args.get("unlearn_ratio", 0.0)),
            "seed": seed_for_key,
            "strategy_name": strategy_name,
            "k": int(k),
            "is_transductive": bool(self.args.get("is_transductive", True)),
            "is_balanced": bool(self.args.get("is_balanced", False)),
            "train_ratio": float(self.args.get("train_ratio", 0.8)),
            "val_ratio": float(self.args.get("val_ratio", 0.0)),
            "test_ratio": float(self.args.get("test_ratio", 0.2)),
            "graph_fingerprint": self._compute_graph_fingerprint(),
            "strategy_params_fingerprint": strategy_params_fingerprint,
        }

    def _supports_subset_reuse(self, strategy_name: str) -> bool:
        if strategy_name not in self.SUBSET_REUSABLE_SELECTION_STRATEGIES:
            return False
        if strategy_name == "im":
            # IM with candidate_fraction < 1 may prune candidate set as a function of k.
            try:
                return float(self.args.get("candidate_fraction", 1.0)) >= 1.0
            except (TypeError, ValueError):
                return False
        return True

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

        # Run through pipeline (optionally reusing method-agnostic selection cache)
        result_dict = None
        selection_cache_hit = False
        selection_cache_key = None
        selection_cache_source = None
        selection_cache_source_k = None
        selection_cache_lookup_mode = "exact"
        selection_time_value = None
        selection_reuse_time = None
        if (
            use_cache
            and self.selection_cache is not None
            and strategy_name in self.REUSABLE_SELECTION_STRATEGIES
        ):
            selection_config = self._build_selection_config(strategy_name, k)
            cache_lookup_start = time.time()
            cached_selection, selection_key, source_file = self.selection_cache.get(selection_config)
            selection_cache_key = selection_key
            selection_cache_source = source_file
            if cached_selection is None and self._supports_subset_reuse(strategy_name):
                (
                    superset_selection,
                    superset_key,
                    superset_source,
                    superset_k,
                ) = self.selection_cache.get_smallest_superset(selection_config, required_k=k)
                if superset_selection is not None:
                    cached_selection = superset_selection
                    selection_cache_key = superset_key
                    selection_cache_source = superset_source
                    selection_cache_source_k = superset_k
                    selection_cache_lookup_mode = "superset"
            if cached_selection is not None and len(cached_selection.selected_nodes) < int(k):
                print(
                    "[SelectionCache] MISS-INVALID "
                    f"strategy={strategy_name} selection_key={selection_cache_key} "
                    f"cached_count={len(cached_selection.selected_nodes)} required_k={k}"
                )
                cached_selection = None
            if cached_selection is not None:
                selection_cache_hit = True
                selected_nodes = torch.tensor(cached_selection.selected_nodes[: int(k)], dtype=torch.long)
                selection_reuse_time = time.time() - cache_lookup_start
                selection_time_value = float(cached_selection.selection_time)
                speedup = None
                if selection_reuse_time > 0:
                    speedup = selection_time_value / selection_reuse_time
                speedup_text = f"{speedup:.2f}x" if speedup is not None else "NA"
                mode_text = f"reuse_mode={selection_cache_lookup_mode}"
                if selection_cache_source_k is not None:
                    mode_text = f"{mode_text} source_k={selection_cache_source_k} target_k={k}"
                print(
                    "[SelectionCache] HIT "
                    f"strategy={strategy_name} selection_key={selection_cache_key} "
                    f"{mode_text} "
                    f"original_selection_time={selection_time_value:.4f}s "
                    f"reuse_time={selection_reuse_time:.6f}s "
                    f"speedup={speedup_text} "
                    f"source={selection_cache_source}"
                )
                result_dict = self.pipeline.run_with_selected_nodes(
                    strategy_name=strategy_name,
                    selected_nodes=selected_nodes,
                    selection_time=selection_time_value,
                )
            else:
                print(
                    "[SelectionCache] MISS "
                    f"strategy={strategy_name} selection_key={selection_cache_key}"
                )
                result_dict = self.pipeline.run_with_strategy(strategy, k)
                selection_time_value = float(result_dict.get("selection_time", 0.0))
                print(
                    "[SelectionCache] MISS-RESULT "
                    f"strategy={strategy_name} selection_key={selection_cache_key} "
                    f"original_selection_time={selection_time_value:.4f}s"
                )
                to_cache = SelectionResult(
                    strategy_name=strategy_name,
                    selected_nodes=result_dict["selected_nodes"].cpu().tolist(),
                    selection_time=selection_time_value,
                    selection_key=selection_cache_key or "",
                    metadata={
                        "dataset_name": selection_config.get("dataset_name"),
                        "base_model": selection_config.get("base_model"),
                        "seed": selection_config.get("seed"),
                        "graph_fingerprint": selection_config.get("graph_fingerprint"),
                    },
                )
                cache_path = self.selection_cache.save(to_cache, selection_config)
                print(f"[SelectionCache] Saved strategy={strategy_name} -> {cache_path}")
        else:
            result_dict = self.pipeline.run_with_strategy(strategy, k)
            selection_time_value = float(result_dict.get("selection_time", 0.0))

        if selection_time_value is None:
            selection_time_value = float(result_dict.get("selection_time", 0.0))

        total_time = time.time() - start_time

        # Build AttackResult
        result = AttackResult(
            strategy_name=strategy_name,
            selected_nodes=result_dict["selected_nodes"],
            f1_before=result_dict["f1_before"],
            f1_after=result_dict["f1_after"],
            unlearn_time=result_dict["unlearn_time"],
            total_time=total_time,
            selection_time=selection_time_value,
            selection_reuse_time=selection_reuse_time,
            selection_cache_hit=selection_cache_hit,
            selection_cache_key=selection_cache_key,
            selection_cache_source=selection_cache_source,
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
