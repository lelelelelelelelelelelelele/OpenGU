"""
AttackPipeline - Encapsulates main.py logic for attack experiments.

This module provides a reusable pipeline that:
1. Loads data and initializes models (reuses main.py logic)
2. Supports custom node selection strategies
3. Runs unlearning experiments
4. Collects and returns results
"""
import os
import sys
import time
import torch
import numpy as np
from typing import Optional, Dict, Any, List, Tuple
from torch import Tensor

# Add parent directory to path for imports
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

# NOTE: heavy imports (`model.model_zoo`, `unlearning_manager`, etc.) are
# intentionally deferred to call sites below. attack/__init__.py eagerly
# imports this module via attack_manager, and main.py's first import is
# `model.model_zoo` — pulling those back here at module level closes the
# cycle (model_zoo → unlearning → CEU → attack → attack_manager →
# pipeline_adapter → model_zoo / unlearning_manager) before the upstream
# modules finish initializing. Lightweight stdlib/utility imports stay at
# top level; anything that transits through `unlearning.*` or `model.*`
# stays inside the methods that use it.
from utils.logger import create_logger
from utils.utils import calc_f1
from attack.attack_strategies import BaseStrategy

model_zoo = None
UnlearningManager = None


def _load_model_zoo():
    global model_zoo
    if model_zoo is None:
        from model.model_zoo import model_zoo as _model_zoo
        model_zoo = _model_zoo
    return model_zoo


def _load_unlearning_manager():
    global UnlearningManager
    if UnlearningManager is None:
        from unlearning_manager import UnlearningManager as _UnlearningManager
        UnlearningManager = _UnlearningManager
    return UnlearningManager


class AttackPipeline:
    """
    Pipeline for running attack experiments with custom node selection strategies.

    This class encapsulates the core logic from main.py and adds support for:
    - Custom node selection strategies
    - Result caching
    - Metric collection

    Example:
        >>> args = parameter_parser()
        >>> pipeline = AttackPipeline(args)
        >>> result = pipeline.run_with_strategy(strategy, k=50)
    """

    def __init__(self, args: Dict[str, Any], logger=None):
        """
        Initialize the attack pipeline.

        Args:
            args: Configuration dictionary from parameter_parser()
            logger: Optional logger instance (creates one if not provided)
        """
        self.args = args
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Setup logger
        if logger is None:
            self.logger = create_logger(args)
        else:
            self.logger = logger

        # Initialize components
        self.original_data = None
        self.data = None
        self.dataset = None
        self.model_zoo = None
        self.model = None
        self.manager = None
        self.method = None

        # State_dict snapshots used to keep training reproducible across
        # strategies in compare_strategies(). Without these, every
        # method.run_exp() trains in-place on whatever weights the previous
        # strategy left behind (post-unlearn), so strategy ordering would
        # affect f1_after / collateral.
        #   _random_init_state_dict: snapshotted at _setup, restored before
        #       every method.run_exp() (both in _ensure_base_model_trained
        #       for the train-for-selection step, and in
        #       _run_unlearning_with_selected_nodes for the actual
        #       train+unlearn run). Ensures every training run starts from
        #       the SAME clean random init.
        #   _trained_state_dict: snapshotted on the first
        #       _ensure_base_model_trained call. Subsequent calls restore
        #       this for select_nodes, so the "base model" used by all
        #       requires_trained_model strategies is bit-identical.
        self._random_init_state_dict = None
        self._trained_state_dict = None

        # Metrics storage
        self.f1_before = 0.0
        self.f1_after = 0.0

        # Run setup
        self._setup()

    def _setup(self):
        """Initialize data, model, and unlearning method."""
        # Lazy imports — see top-of-file note on the import cycle
        from dataset.original_dataset import original_dataset
        from utils.dataset_utils import process_data
        model_zoo_cls = _load_model_zoo()
        unlearning_manager_cls = _load_unlearning_manager()

        self.logger.info("Initializing AttackPipeline...")

        # Load data
        self.original_data = original_dataset(self.args, self.logger)
        self.data, self.dataset = self.original_data.load_data()
        self.data = process_data(self.logger, self.data, self.args)

        # Initialize model
        self.model_zoo = model_zoo_cls(self.args, self.data)
        self.model = self.model_zoo.model

        if self.args["base_model"] not in ["GST", "Projector"]:
            self.logger.log_model_info(self.model)

        # Snapshot the random-init weights BEFORE any training happens.
        # _restore_random_init() reloads this before every method.run_exp()
        # so each strategy's training run starts from the same clean state
        # rather than from whatever the previous strategy left behind.
        try:
            self._random_init_state_dict = {
                k: v.detach().clone() for k, v in self.model.state_dict().items()
            }
        except Exception as exc:
            self.logger.warning(
                f"Could not snapshot random-init state_dict ({exc}); "
                "strategy ordering may affect downstream metrics."
            )
            self._random_init_state_dict = None

        # Initialize unlearning manager
        self.manager = unlearning_manager_cls(
            self.args, self.original_data, self.data,
            self.logger, self.model_zoo, self.dataset
        )
        self.method = self.manager.get_method()

        self.logger.info("AttackPipeline initialized successfully.")

    def _restore_random_init(self):
        """Reset self.model to the random-init weights snapshotted at _setup.

        Called before every method.run_exp() so training runs are independent
        of which strategy ran previously. No-op if the snapshot was not taken
        (e.g., model lacks a standard state_dict — GST/Projector edge case).
        """
        if self._random_init_state_dict is None:
            return
        try:
            self.model.load_state_dict(self._random_init_state_dict)
        except Exception as exc:
            self.logger.warning(
                f"_restore_random_init failed ({exc}); training will proceed "
                "from whatever state self.model is currently in."
            )

    def _evaluate_model(self, model=None) -> float:
        """
        Evaluate the model and return F1 score.

        Args:
            model: Optional model to evaluate (uses pipeline model if None)

        Returns:
            F1 score on test set
        """
        if model is None:
            model = self.model

        model.eval()
        device = next(model.parameters()).device
        data = self.data.to(device)

        with torch.no_grad():
            # Get predictions
            out = model(data.x, data.edge_index)

            # Calculate F1 using existing utility
            y_true = data.y.cpu().numpy()
            y_pred = out.cpu().numpy()
            test_mask = data.test_mask

            f1 = calc_f1(y_true, y_pred, test_mask, multilabel=False)

        return f1

    def _inject_unlearn_nodes(self, nodes: Tensor, run_id: int = 0):
        """
        Inject selected nodes into the unlearning configuration.

        This writes the selected nodes to the file that the unlearning method
        will read in unlearning_request().

        Args:
            nodes: Tensor of node indices to unlearn
            run_id: Run identifier for file naming
        """
        # Ensure nodes are numpy array
        if isinstance(nodes, Tensor):
            nodes = nodes.cpu().numpy()

        # Construct path matching config.py format
        # unlearning_path = root_path + "/data/unlearning_task/{transductive|inductive}/{balanced|imbalanced}/unlearning_nodes_{ratio}_{dataset}"
        root_path = "."

        if self.args["is_transductive"]:
            split_type = "transductive"
        else:
            split_type = "inductive"

        if self.args["is_balanced"]:
            balance_type = "balanced"
        else:
            balance_type = "imbalanced"

        path = f"{root_path}/data/unlearning_task/{split_type}/{balance_type}/unlearning_nodes_{self.args['unlearn_ratio']}_{self.args['dataset_name']}_{run_id}.txt"

        # Sanity check: the path we write must match the one downstream
        # unlearning methods read from `config.unlearning_path`. A mismatch
        # means config.py was loaded with the wrong sys.argv (the demo_attack
        # arg-stripping bug from before commit 66a90f8). Fail fast so a
        # regression doesn't silently unlearn nodes from a stale file.
        from config import unlearning_path as _config_unlearning_path
        expected = f"{_config_unlearning_path}_{run_id}.txt"
        if os.path.normpath(path) != os.path.normpath(expected):
            raise AssertionError(
                "AttackPipeline path mismatch:\n"
                f"  inject  = {os.path.normpath(path)}\n"
                f"  config  = {os.path.normpath(expected)}\n"
                "config.unlearning_path was bound to different args than "
                "self.args. Check that demo_attack.py / experiments/run.py "
                "preserve dataset_name/unlearn_ratio/is_transductive/is_balanced "
                "in sys.argv before any module imports config."
            )

        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Write nodes to file
        np.savetxt(path, nodes, fmt='%d')

        self.logger.info(f"Injected {len(nodes)} nodes to unlearn at {path}")

    def _ensure_base_model_trained(self):
        """
        Train the base model on the full train set so that strategies
        which derive scores from gradients/logits (TracIn, Hybrid) see a
        TRAINED model rather than the random-init weights produced by
        model_zoo.__init__.

        First call: restores random-init weights (so this training runs on
        a clean starting point — see _restore_random_init for why), runs
        the unlearning method's train_only path, then snapshots the
        resulting trained state_dict.

        Subsequent calls: load the trained snapshot directly. No
        retraining, no dependence on whatever the previous strategy left
        behind in self.model_zoo.model.

        Notes on Shard_based methods (GraphEraser/GUIDE/GraphRevoker):
        their "trained model" is a shard-aggregated artifact stored to
        disk; self.model_zoo.model isn't directly trained by run_exp.
        We still snapshot whatever _get_trained_model returns; if that
        falls back to the untrained model_zoo.model, the strategy
        effectively sees random-init for shard methods. We log a warning
        in that case but don't crash, since random/im/etc. don't care
        and TracIn/Hybrid + Shard isn't a supported combo for B.1/B.2.
        """
        if self._trained_state_dict is not None:
            try:
                self.model.load_state_dict(self._trained_state_dict)
                return
            except Exception as exc:
                self.logger.warning(
                    f"Failed to restore trained-model snapshot ({exc}); "
                    "re-training from scratch."
                )
                self._trained_state_dict = None

        self.logger.info(
            "Training base model for selection (requires_trained_model strategy)..."
        )
        prev_train_only = self.args.get("train_only", False)
        prev_num_runs = self.args.get("num_runs", 1)

        try:
            # Reset to clean random-init so the training trajectory is
            # independent of any previous strategy's run_exp side effects.
            self._restore_random_init()

            self.args["train_only"] = True
            self.args["num_runs"] = 1
            self.method = self.manager.get_method()
            self.method.run_exp()
        finally:
            self.args["train_only"] = prev_train_only
            self.args["num_runs"] = prev_num_runs

        trained = self._get_trained_model()
        # Point self.model at the trained module so select_nodes uses it
        self.model = trained

        try:
            self._trained_state_dict = {
                k: v.detach().clone() for k, v in trained.state_dict().items()
            }
            f1 = self._evaluate_model(trained)
            self.logger.info(f"Base model trained (F1={f1:.4f}); trained state_dict snapshot taken.")
        except Exception as exc:
            self.logger.warning(
                f"Could not snapshot trained state_dict ({exc}). "
                "Subsequent strategies will retrain instead of restoring."
            )
            self._trained_state_dict = None

    def run_with_strategy(self, strategy: BaseStrategy, k: int, run_id: int = 0) -> Dict[str, Any]:
        """
        Run a complete attack experiment with the given strategy.

        Args:
            strategy: Node selection strategy
            k: Number of nodes to select
            run_id: Run identifier (for multiple runs)

        Returns:
            Dictionary containing experiment results
        """
        strategy_label = strategy.__class__.__name__
        self.logger.info(f"Running attack with strategy: {strategy_label}")
        self.logger.info(f"Selecting {k} nodes for unlearning")

        # Train base model in-place if the strategy needs trained weights.
        # Without this, gradient-based strategies (TracIn/Hybrid) compute
        # scores on random-init weights — see commit message.
        if getattr(strategy, "requires_trained_model", False):
            self._ensure_base_model_trained()

        start_time = time.time()  # Start timing before selection
        selection_start = time.time()
        selected_nodes = strategy.select_nodes(self.data, self.model, k)
        selection_time = time.time() - selection_start

        self.logger.info(f"Strategy selected nodes: {selected_nodes[:10].tolist()}... (showing first 10)")
        self.logger.info(f"Selection took {selection_time:.2f}s")

        return self.run_with_selected_nodes(
            strategy_name=strategy_label,
            selected_nodes=selected_nodes,
            selection_time=selection_time,
            run_id=run_id,
            start_time=start_time,  # Pass start_time so total_time includes selection
        )

    def run_with_selected_nodes(
        self,
        strategy_name: str,
        selected_nodes: Tensor,
        selection_time: float = 0.0,
        run_id: int = 0,
        start_time: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Run unlearning with pre-selected nodes (selection already done or reused).

        Args:
            strategy_name: Strategy label for logging/result metadata
            selected_nodes: Node indices to unlearn
            selection_time: Selection cost to record in result
            run_id: Run identifier (for multiple runs)
            start_time: Optional start time from before selection (for accurate total_time)

        Returns:
            Dictionary containing experiment results
        """
        if start_time is None:
            start_time = time.time()  # Fallback if not provided
        if not isinstance(selected_nodes, Tensor):
            selected_nodes = torch.tensor(selected_nodes, dtype=torch.long)
        else:
            selected_nodes = selected_nodes.cpu().long()

        return self._run_unlearning_with_selected_nodes(
            strategy_name=strategy_name,
            selected_nodes=selected_nodes,
            selection_time=selection_time,
            run_id=run_id,
            start_time=start_time,
        )

    def _run_unlearning_with_selected_nodes(
        self,
        strategy_name: str,
        selected_nodes: Tensor,
        selection_time: float,
        run_id: int,
        start_time: float,
    ) -> Dict[str, Any]:
        # Step 1: Inject selected nodes
        self._inject_unlearn_nodes(selected_nodes, run_id)

        # Step 2: Reset model to random init so this run_exp's
        # train_original_model phase trains from a clean state. Without
        # this, training starts from whatever the previous strategy left
        # behind (post-unlearn weights, or trained-snapshot from
        # _ensure_base_model_trained), and f1_after / mia_auc end up
        # depending on strategy ordering.
        self._restore_random_init()

        # Step 3: Run unlearning experiment (trains model + unlearns)
        # Reset the method to pick up the new unlearning nodes
        self.method = self.manager.get_method()

        unlearn_start = time.time()

        # Run the unlearning experiment
        try:
            # Run a single iteration
            self.args["num_runs"] = 1
            self.method.run_exp()

            # Extract results from the method
            # poison_f1 = pre-unlearning F1 (set during train_original_model for edge tasks)
            # average_f1 = post-unlearning F1
            unlearn_time = getattr(self.method, 'avg_unlearning_time', [0])[0] if hasattr(self.method, 'avg_unlearning_time') else 0
            f1_after = getattr(self.method, 'average_f1', [0])[0] if hasattr(self.method, 'average_f1') else 0
            mia_auc = getattr(self.method, 'average_auc', [None])[0] if hasattr(self.method, 'average_auc') else None

            # Get pre-unlearning F1: use poison_f1 if available, otherwise set to None
            f1_before_arr = getattr(self.method, 'poison_f1', None)
            if f1_before_arr is not None and f1_before_arr[0] > 0:
                f1_before = float(f1_before_arr[0])
            else:
                # Removed fallback (self._evaluate_model()) because evaluating model post-run 
                # yields invalid pre-unlearning baseline metrics.
                f1_before = None

        except Exception as e:
            self.logger.error(f"Error during unlearning: {e}")
            import traceback
            traceback.print_exc()
            f1_before = None
            f1_after = 0.0
            unlearn_time = time.time() - unlearn_start
            mia_auc = None

        unlearn_time = time.time() - unlearn_start if unlearn_time == 0 else unlearn_time
        total_time = time.time() - start_time

        # If f1_after wasn't set properly, evaluate
        if f1_after == 0:
            f1_after = self._evaluate_model()

        if f1_before is not None:
            f1_drop = f1_before - f1_after
            self.logger.info(f"F1 before unlearning: {f1_before:.4f}")
            self.logger.info(f"F1 after unlearning: {f1_after:.4f}")
            self.logger.info(f"F1 drop: {f1_drop:.4f}")
        else:
            f1_drop = None
            self.logger.info("F1 before unlearning: NA")
            self.logger.info(f"F1 after unlearning: {f1_after:.4f}")
            self.logger.info("F1 drop: NA")
            
        self.logger.info(f"Unlearning took {unlearn_time:.2f}s")

        return {
            "strategy_name": strategy_name,
            "selected_nodes": selected_nodes,
            "f1_before": f1_before,
            "f1_after": f1_after,
            "f1_drop": f1_drop,
            "unlearn_time": unlearn_time,
            "selection_time": selection_time,
            "total_time": total_time,
            "mia_auc": mia_auc,
        }

    def _get_trained_model(self):
        """
        Extract the trained model from the unlearning method object.

        Different pipeline types store the model in different locations:
        - Learning_based / IF_based: self.method.target_model.model
        - Shard_based: aggregated model accessed via disk; use self.method.model_zoo.model
        """
        method = self.method
        # IF_based and Learning_based pipelines
        if hasattr(method, 'target_model') and method.target_model is not None:
            if hasattr(method.target_model, 'model'):
                return method.target_model.model
        # Shard_based pipelines
        if hasattr(method, 'model_zoo') and hasattr(method.model_zoo, 'model'):
            return method.model_zoo.model
        # Fallback
        return self.model

    def run_retrain(self, selected_nodes: Tensor) -> Tuple[Any, float]:
        """
        Train model from scratch on data EXCLUDING selected_nodes.

        This reinitializes the model and method, sets train_only=True so that
        run_exp() only trains without performing unlearning, then evaluates.

        Args:
            selected_nodes: Tensor of node indices to exclude from training

        Returns:
            (model_retrained, f1_retrained)
        """
        # 1. Backup original train_mask
        original_train_mask = self.data.train_mask.clone()

        # 2. Exclude selected_nodes from train_mask
        node_idx = selected_nodes.long()
        self.data.train_mask[node_idx] = False

        # 3. Reinitialize model + method with train_only (lazy imports — see top-of-file note)
        model_zoo_cls = _load_model_zoo()
        unlearning_manager_cls = _load_unlearning_manager()
        self.args["train_only"] = True
        self.args["num_runs"] = 1
        self.model_zoo = model_zoo_cls(self.args, self.data)
        self.model = self.model_zoo.model

        self.manager = unlearning_manager_cls(
            self.args, self.original_data, self.data,
            self.logger, self.model_zoo, self.dataset
        )
        self.method = self.manager.get_method()

        # 4. run_exp() trains only (no unlearning due to train_only flag)
        self.method.run_exp()

        # 5. Extract retrained model and evaluate
        model_retrained = self._get_trained_model()
        f1_retrained = self._evaluate_model(model_retrained)

        # 6. Restore original state
        self.data.train_mask = original_train_mask
        self.args["train_only"] = False

        self.logger.info(f"Retrain F1 (excl {len(selected_nodes)} nodes): {f1_retrained:.4f}")
        return model_retrained, f1_retrained

    def compare_strategies(self, strategies: Dict[str, BaseStrategy], k: int) -> List[Dict[str, Any]]:
        """
        Compare multiple strategies.

        Args:
            strategies: Dictionary mapping strategy names to strategy instances
            k: Number of nodes to select

        Returns:
            List of result dictionaries
        """
        results = []

        for name, strategy in strategies.items():
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Evaluating strategy: {name}")
            self.logger.info(f"{'='*60}")

            result = self.run_with_strategy(strategy, k)
            results.append(result)

        return results


def create_pipeline_from_args(args_dict: Optional[Dict[str, Any]] = None) -> AttackPipeline:
    """
    Factory function to create an AttackPipeline from arguments.

    Args:
        args_dict: Optional argument dictionary (uses parameter_parser() if None)

    Returns:
        Initialized AttackPipeline
    """
    if args_dict is None:
        from parameter_parser import parameter_parser
        args_dict = parameter_parser()

    return AttackPipeline(args_dict)
