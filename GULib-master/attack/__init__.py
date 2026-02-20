"""
Attack module for adversarial attacks on GNN unlearning methods.

This module provides:
- Attack strategies for node selection (Random, Degree, PageRank, TracIn, IM, Hybrid)
- AttackManager for coordinating experiments
- AttackPipeline for encapsulating main.py logic
- ResultCache for caching experiment results
- AttackResult data structures
- Evaluation functions for attribution framework (F1 drop, MIA AUC, retrain gap, etc.)

Example:
    >>> from attack import AttackManager, AttackResult
    >>> from attack.attack_strategies import TracInStrategy
    >>>
    >>> manager = AttackManager(args)
    >>> result = manager.run_attack("tracin", k=50)
    >>> comparison = manager.compare_strategies(["random", "tracin"], k=50)
"""

# Import main classes
from .attack_manager import AttackManager, create_manager, quick_demo
from .attack_result import AttackResult, ComparisonResult
from .pipeline_adapter import AttackPipeline, create_pipeline_from_args
from .result_cache import ResultCache, LogBasedCache
from .selection_cache import SelectionCache, SelectionResult

# Import strategies
from .attack_strategies import (
    BaseStrategy,
    RandomStrategy,
    DegreeStrategy,
    PageRankStrategy,
    TracInStrategy,
    IMStrategy,
    HybridStrategy,
)

# Import evaluation functions
from .attack_eval import (
    evaluate_f1_drop,
    evaluate_mia_auc,
    evaluate_retrain_gap,
    evaluate_collateral_damage,
    compute_gap_statistics,
)

# Version info
__version__ = "0.1.0"

__all__ = [
    # Main classes
    "AttackManager",
    "AttackResult",
    "ComparisonResult",
    "AttackPipeline",
    "ResultCache",
    "LogBasedCache",
    "SelectionCache",
    "SelectionResult",
    # Strategies
    "BaseStrategy",
    "RandomStrategy",
    "DegreeStrategy",
    "PageRankStrategy",
    "TracInStrategy",
    "IMStrategy",
    "HybridStrategy",
    # Evaluation
    "evaluate_f1_drop",
    "evaluate_mia_auc",
    "evaluate_retrain_gap",
    "evaluate_collateral_damage",
    "compute_gap_statistics",
    # Utilities
    "create_manager",
    "quick_demo",
    "create_pipeline_from_args",
]
