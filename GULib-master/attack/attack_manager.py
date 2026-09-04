"""
AttackManager - Central dispatcher for attack experiments.

This module provides the main interface for running attack experiments,
managing strategies, and collecting results.
"""
import os
import sys
import time
import json
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
)
from attack.attack_result import AttackResult, ComparisonResult
from attack.pipeline_adapter import AttackPipeline
from attack.result_cache import ResultCache
from attack.selection_cache import SelectionCache
from attack.cache_identity import (store_root, strategy_version, producer_version, model_fingerprint,
                                   split_fingerprint, target_parameters, seeded_execution,
                                   selector_training_parameters, train_selector_model)
from experiments.selection_inputs import make_dataset_selection_inputs
from cache_v2.selection_materializer import build_selection_recipe, SelectionArtifactRequest
from cache_v2.formal_artifacts import ordered_int_hash
from attack.attack_strategies.im_strategy import HAS_NUMBA
from utils.metric_policy import update_detection_auc_result_value


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
    # Note: as of 2026-05-05 the V4 classes (IMV4Strategy, HybridV4Strategy)
    # were merged into IMStrategy / HybridStrategy. Batch-CELF is now the
    # canonical numba path inside IMStrategy, gated by `im_batch_size`
    # (legacy `im_v4_batch_size` still accepted). Backward-compat aliases
    # `IMV4Strategy = IMStrategy` and `HybridV4Strategy = HybridStrategy`
    # are kept in `attack_strategies/__init__.py` so external imports of
    # the old names still resolve.
    BUILTIN_STRATEGIES = {
        "random": RandomStrategy,
        "degree": DegreeStrategy,
        "pagerank": PageRankStrategy,
        "tracin": TracInStrategy,
        "im": IMStrategy,
        "hybrid": HybridStrategy,
    }
    # Built-in strategies with complete generic V2 producer identities.
    REUSABLE_SELECTION_STRATEGIES = {"random", "degree", "pagerank", "im", "tracin", "hybrid"}
    # Shard/SISA methods do not expose the canonical vanilla base model through
    # train_only. TracIn/Hybrid selection for these methods is only safe when it
    # reuses a method-agnostic SelectionCache entry computed by a canonical
    # full-model method earlier in the matrix.
    SHARD_METHODS_REQUIRE_CANONICAL_SELECTOR_CACHE = {"GraphEraser", "GUIDE", "GraphRevoker"}

    def __init__(
        self,
        args: Dict[str, Any],
        pipeline: Optional[AttackPipeline] = None,
        cache_dir: Optional[str] = None,
        use_cache: bool = True,
    ):
        """
        Initialize the AttackManager.

        Args:
            args: Configuration dictionary from parameter_parser()
            pipeline: Optional pre-initialized AttackPipeline
            cache_dir: Directory for result caching
            use_cache: Whether to enable optional Result, Selection and Score caching
        """
        self.args = dict(args)
        args = self.args
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

        # All consumers share one lazy V2 store. Construction performs no IO.
        self.use_cache = use_cache
        self.cache_root = Path(cache_dir).absolute().resolve() if cache_dir else store_root(args)
        self.args["cache_v2_store_root"] = str(self.cache_root)
        self.cache = ResultCache(self.cache_root)
        self.selection_cache = SelectionCache(self.cache_root)
        self.results: Dict[str, AttackResult] = {}
        self._initial_model_hash = model_fingerprint(self.model)
        import copy
        self._selector_initial_model = copy.deepcopy(self.model)
        self._selector_model = None
        source_root = Path(__file__).resolve().parents[1]
        sources = ["attack/attack_manager.py", "attack/pipeline_adapter.py", "attack/cache_identity.py",
                   "attack/result_cache.py", "attack/attack_result.py", "unlearning_manager.py"]
        for directory in ("unlearning", "pipeline", "task", "model", "utils"):
            sources.extend(path.relative_to(source_root).as_posix()
                           for path in (source_root / directory).rglob("*.py"))
        self._result_producer = producer_version("attack-evaluation", sources)

        # Register built-in strategies
        self._register_builtin_strategies()

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

    def _strategy_params_for_cache(self, strategy_name: str) -> Dict[str, Any]:
        # Each strategy's cache key must include EVERY arg that meaningfully
        # changes the selected nodes, otherwise SelectionCache silently
        # cross-contaminates between two configurations sharing the static
        # fields (dataset/seed/k/...) but differing in strategy hyperparam.
        im_batch_size = int(self.args.get("im_batch_size", self.args.get("im_v4_batch_size", 5)))
        if strategy_name == "im":
            # im is the batch-CELF v4 implementation (the v4 suffix was dropped 2026-05-04)
            return {
                "propagation_prob": float(self.args.get("propagation_prob", 0.1)),
                "mc_rounds": int(self.args.get("mc_rounds", 100)),
                "candidate_fraction": float(self.args.get("candidate_fraction", 1.0)),
                "im_batch_size": im_batch_size,
            }
        elif strategy_name == "pagerank":
            return {
                "pagerank_alpha": float(self.args.get("pagerank_alpha", 0.85)),
            }
        elif strategy_name == "tracin":
            # loss_type changes per-node loss → changes gradients → changes
            # selection. base_model is already in the main selection_config.
            return {
                "loss_type": str(self.args.get("loss", "cross_entropy")),
            }
        elif strategy_name == "hybrid":
            # Hybrid fuses TracIn + IM, so its cache key must include EVERY
            # knob from both branches plus the fusion params. Without these
            # two Hybrid runs differing only in alpha / fusion_method /
            # candidate_fraction would collide on the same cache entry.
            hybrid_alpha = self.args.get("hybrid_alpha")
            if hybrid_alpha is None:
                hybrid_alpha = self.args.get("alpha", 0.5)
            return {
                "fusion_method": str(self.args.get("fusion_method", "rank")),
                "hybrid_alpha": float(hybrid_alpha),
                "loss_type": str(self.args.get("loss", "cross_entropy")),
                "propagation_prob": float(self.args.get("propagation_prob", 0.1)),
                "mc_rounds": int(self.args.get("mc_rounds", 100)),
                "candidate_fraction": float(self.args.get("candidate_fraction", 1.0)),
                "im_batch_size": im_batch_size,
                "im_selector_seed": int(self.args.get("im_selector_seed", 2024)),
            }
        return {}

    # Strategies whose selection is a deterministic function of graph topology
    # + their own hyperparams (no dependence on the GNN model or training seed).
    # Their SelectionCache key is anchored to a constant so cross-seed runs
    # share the cache instead of recomputing identical results.
    TOPOLOGY_ONLY_STRATEGIES = frozenset({"degree", "pagerank"})

    def _selection_request(self, strategy_name, k, inputs):
        parameters = self._strategy_params_for_cache(strategy_name)
        if strategy_name in {"im", "hybrid"}:
            parameters["implementation_backend"] = "numba" if HAS_NUMBA else "python"
            parameters["parallel_mc"] = bool(self.args.get("im_parallel_mc", True))
        parameters["split_fingerprint"] = split_fingerprint(self.data)
        seed = self._seed_value()
        if strategy_name in self.TOPOLOGY_ONLY_STRATEGIES:
            seed = 0
        elif strategy_name == "im":
            seed = int(self.args.get("im_selector_seed", 2024))
        if getattr(self.get_strategy(strategy_name), "requires_trained_model", False):
            # Shard consumers reuse the canonical full-model selector; GU
            # method identity belongs to the downstream Evaluation Recipe.
            from experiments.implementation_identity import implementation_fingerprint, model_functions
            from experiments.modular_model import train_supervised
            parameters["training"] = selector_training_parameters(self.args, self.model)
            parameters["initial_model_hash"] = self._initial_model_hash
            parameters["model_implementation"] = implementation_fingerprint(*model_functions(self.model), train_selector_model, train_supervised)
        producer = strategy_version(strategy_name)
        recipe = build_selection_recipe(dataset_fingerprint=inputs.dataset_fingerprint,
            graph_fingerprint=inputs.graph_fingerprint, candidate_set_hash=inputs.candidate_set_hash,
            num_nodes=inputs.num_nodes, candidate_count=inputs.candidate_count,
            node_id_space="opengu-node-id", strategy=strategy_name, seed=seed, k=int(k),
            producer_version=producer, algorithm_version="generic-selection-v1", parameters=parameters)
        return SelectionArtifactRequest(recipe, producer, inputs.num_nodes)

    def _result_request(self, selection, inputs):
        target = {"parameters": target_parameters(self.args),
                  "dataset_fingerprint": inputs.dataset_fingerprint,
                  "split_fingerprint": split_fingerprint(self.data),
                  "initial_model_hash": self._initial_model_hash}
        return self.cache.request(selection, inputs.graph_fingerprint,
            ordered_int_hash(selection.selected_nodes), target, self._result_producer)

    def _needs_canonical_selector_cache(self, strategy_name: str, strategy: BaseStrategy) -> bool:
        method = str(self.args.get("unlearning_methods", ""))
        return (
            method in self.SHARD_METHODS_REQUIRE_CANONICAL_SELECTOR_CACHE
            and getattr(strategy, "requires_trained_model", False)
            and strategy_name in self.REUSABLE_SELECTION_STRATEGIES
        )

    def _raise_canonical_selector_cache_miss(self, strategy_name: str):
        method = str(self.args.get("unlearning_methods", ""))
        raise RuntimeError(
            "SelectionCache miss for trained-model selector "
            f"{method}/{strategy_name}. Shard/SISA train_only is not the "
            "canonical vanilla base model for TracIn/Hybrid selection. "
            "Run a canonical full-model method (e.g. GIF or GNNDelete) for "
            "this dataset/model/seed/strategy first, or prewarm the "
            "SelectionCache from that path."
        )

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
        """Resolve V2 first; only a clean MISS executes selection/unlearning."""
        enabled = self.use_cache if use_cache is None else bool(use_cache)
        previous = self.args.get("use_cache", True)
        self.args["use_cache"] = enabled
        try:
            return self._run_attack(strategy_name, k, enabled)
        finally:
            self.args["use_cache"] = previous

    def _run_attack(self, strategy_name, k, enabled):
        strategy = self.get_strategy(strategy_name)
        if strategy is None:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        print(f"[AttackManager] Running attack with strategy: {strategy_name}")
        inputs = make_dataset_selection_inputs(self.data, dataset_name=self.args["dataset_name"])
        request = self._selection_request(strategy_name, k, inputs)
        started = time.time()
        selection = self.selection_cache.get(request) if enabled else None
        selection_hit = selection is not None
        request_result = self._result_request(selection, inputs) if selection_hit else None
        if request_result is not None:
            cached, provenance = self.cache.get_with_provenance(request_result)
            if cached is not None:
                cached.selection_cache_hit = True
                cached.selection_reuse_time = time.time() - started
                cached.result_cache_hit = True
                cached.result_cache_key = provenance["cache_key"]
                cached.result_cache_source = provenance["source_file"]
                cached.result_cache_lookup_mode = provenance["lookup_policy"]
                cached.result_artifact_id = provenance["cache_key"]
                cached.result_recipe_hash = provenance["recipe_hash"]
                cached.result_content_hash = provenance["content_hash"]
                self.results[strategy_name] = cached
                print(f"[CacheV2] HIT evaluation {cached.result_cache_key}")
                return cached
        selection_reuse_time = time.time() - started if selection_hit else None
        if selection_hit:
            print(f"[CacheV2] HIT selection {selection.artifact_id}")
            selected_nodes = torch.tensor(selection.selected_nodes, dtype=torch.long)
            selection_seconds = selection.selection_time
        else:
            if self._needs_canonical_selector_cache(strategy_name, strategy):
                self._raise_canonical_selector_cache_miss(strategy_name)
            print(f"[CacheV2] {'MISS' if enabled else 'BYPASS'} selection {request.recipe.recipe_hash}")
            selected_nodes, selection_seconds = self.produce_selection(strategy_name, k)
        with seeded_execution(self._seed_value()):
            result_dict = self.pipeline.run_with_selected_nodes(strategy_name=strategy_name,
                selected_nodes=selected_nodes, selection_time=selection_seconds)
        if enabled and not selection_hit and not result_dict.get("failed"):
            selection = self.selection_cache.save(selected_nodes.cpu().tolist(), request, selection_seconds)
            request_result = self._result_request(selection, inputs)
        checkpoint = dict(result_dict.get("target_checkpoint") or {})
        result = AttackResult(strategy_name=strategy_name, selected_nodes=result_dict["selected_nodes"],
            f1_before=result_dict["f1_before"], f1_after=result_dict["f1_after"],
            unlearn_time=result_dict["unlearn_time"], total_time=time.time()-started,
            selection_time=float(result_dict.get("selection_time", 0.0)),
            selection_reuse_time=selection_reuse_time, selection_cache_hit=selection_hit if enabled else None,
            selection_cache_key=selection.artifact_id if selection else None,
            selection_cache_source=selection.source if selection else None,
            selection_cache_lookup_mode="cache_v2_exact_recipe" if enabled else None,
            selection_artifact_id=selection.artifact_id if selection else None,
            selection_recipe_hash=selection.recipe_hash if selection else None,
            selection_content_hash=selection.content_hash if selection else None,
            selection_authoritative=True if selection else None,
            target_checkpoint_path=checkpoint.get("path"),
            target_checkpoint_file_sha256=checkpoint.get("file_sha256"),
            target_checkpoint_state_hash=checkpoint.get("state_hash"),
            result_cache_hit=False if enabled else None, mia_auc=result_dict.get("mia_auc"),
            config=self._build_config(strategy_name, k), failed=bool(result_dict.get("failed", False)),
            failure_reason=result_dict.get("failure_reason"))
        self.results[strategy_name] = result
        if enabled and not result.failed:
            stored = self.cache.save(result, request_result)
            result.result_cache_key = stored.artifact_id
            result.result_artifact_id = stored.artifact_id
            result.result_recipe_hash = request_result.recipe.recipe_hash
            result.result_content_hash = stored.content_hash
            result.result_cache_source = str(self.cache_root / stored.semantic_path)
            result.result_cache_lookup_mode = "cache_v2_exact_recipe"
            print(f"[CacheV2] MISS evaluation {stored.artifact_id}")
        return result

    def produce_selection(self, strategy_name, k):
        """Experiment-owned MISS computation, shared with the prewarm entry."""
        strategy = self.get_strategy(strategy_name)
        if self._needs_canonical_selector_cache(strategy_name, strategy):
            self._raise_canonical_selector_cache_miss(strategy_name)
        with seeded_execution(self._seed_value()):
            selection_model = self.pipeline.model
            if getattr(strategy, "requires_trained_model", False):
                if self._selector_model is None:
                    import copy
                    self._selector_model = train_selector_model(copy.deepcopy(self._selector_initial_model),
                        self.data, selector_training_parameters(self.args, self._selector_initial_model))
                selection_model = self._selector_model
            started = time.time()
            nodes = strategy.select_nodes(self.data, selection_model, k).cpu()
            selection_seconds = time.time() - started
        candidates = self._candidate_nodes().tolist()
        if nodes.numel() != int(k) or nodes.unique().numel() != int(k) or not set(nodes.tolist()).issubset(candidates):
            raise ValueError("selection producer returned invalid candidate nodes")
        print(f"[AttackManager] Selection took {selection_seconds:.6f}s")
        return nodes, selection_seconds

    def run_attack_with_selected_nodes(
        self,
        strategy_name: str,
        selected_nodes: Any,
        *,
        selection_provenance: Dict[str, Any],
        selection_time: float = 0.0,
        selection_reuse_time: Optional[float] = None,
    ) -> AttackResult:
        """Run unlearning from a verified external Selection Artifact.

        This path never queries or writes ResultCache, SelectionCache, or
        ScoreCache.  The caller must provide authoritative Artifact
        provenance; missing fields fail before the unlearning pipeline runs.
        """

        if not isinstance(strategy_name, str) or not strategy_name:
            raise ValueError("Selection Artifact strategy label must be non-empty")
        required = {
            "artifact_id",
            "recipe_hash",
            "content_hash",
            "source_file",
            "hit_source",
            "lookup_policy",
            "authoritative",
        }
        missing = sorted(key for key in required if selection_provenance.get(key) is None)
        if missing:
            raise ValueError(
                "Selection Artifact provenance is missing: {0}".format(",".join(missing))
            )
        if selection_provenance.get("authoritative") is not True:
            raise ValueError("Selection Artifact provenance must be authoritative")
        recipe = selection_provenance.get("recipe")
        if self.get_strategy(strategy_name) is None and (
            not isinstance(recipe, dict)
            or recipe.get("strategy") != strategy_name
        ):
            raise ValueError(
                "Selection Artifact provenance strategy must match the result label"
            )
        nodes = torch.as_tensor(selected_nodes, dtype=torch.long).view(-1).cpu()
        if nodes.numel() <= 0:
            raise ValueError("Selection Artifact must contain at least one node")
        if nodes.unique().numel() != nodes.numel():
            raise ValueError("Selection Artifact contains duplicate nodes")
        candidates = set(int(node) for node in self._candidate_nodes().tolist())
        invalid = [int(node) for node in nodes.tolist() if int(node) not in candidates]
        if invalid:
            raise ValueError(
                "Selection Artifact contains nodes outside the candidate set: {0}".format(
                    invalid
                )
            )

        print(
            "[CacheV2] HIT "
            f"strategy={strategy_name} artifact_id={selection_provenance['artifact_id']} "
            f"lookup={selection_provenance['lookup_policy']}"
        )
        started = time.time()
        result_dict = self.pipeline.run_with_selected_nodes(
            strategy_name=strategy_name,
            selected_nodes=nodes,
            selection_time=float(selection_time),
        )
        total_time = time.time() - started
        config = self._build_config(strategy_name, int(nodes.numel()))
        target_checkpoint = dict(result_dict.get("target_checkpoint") or {})
        result = AttackResult(
            strategy_name=strategy_name,
            selected_nodes=result_dict["selected_nodes"],
            f1_before=result_dict["f1_before"],
            f1_after=result_dict["f1_after"],
            unlearn_time=result_dict["unlearn_time"],
            total_time=total_time,
            selection_time=float(selection_time),
            selection_reuse_time=selection_reuse_time,
            selection_cache_hit=True,
            selection_cache_key=str(selection_provenance["artifact_id"]),
            selection_cache_source=str(selection_provenance["source_file"]),
            selection_cache_lookup_mode=str(selection_provenance["lookup_policy"]),
            selection_cache_source_k=None,
            selection_artifact_id=str(selection_provenance["artifact_id"]),
            selection_recipe_hash=str(selection_provenance["recipe_hash"]),
            selection_content_hash=str(selection_provenance["content_hash"]),
            selection_authoritative=True,
            target_checkpoint_path=target_checkpoint.get("path"),
            target_checkpoint_file_sha256=target_checkpoint.get("file_sha256"),
            target_checkpoint_state_hash=target_checkpoint.get("state_hash"),
            result_cache_hit=None,
            mia_auc=result_dict.get("mia_auc"),
            config=config,
            failed=bool(result_dict.get("failed", False)),
            failure_reason=result_dict.get("failure_reason"),
        )
        self.results[strategy_name] = result
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
