"""
Data structures for attack experiment results.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from torch import Tensor
import torch
import json
from datetime import datetime


@dataclass
class AttackResult:
    """
    Result of a single attack experiment.

    Attributes:
        strategy_name: Name of the attack strategy used
        selected_nodes: Tensor of selected node indices for unlearning
        f1_before: F1 score before unlearning
        f1_after: F1 score after unlearning
        f1_drop: Absolute F1 drop (f1_before - f1_after)
        f1_drop_ratio: Relative F1 drop ratio (f1_drop / f1_before * 100)
        unlearn_time: Time taken for unlearning (seconds)
        total_time: Total experiment time (seconds)
        mia_auc: MIA AUC score (optional)
        run_timestamp: ISO format timestamp of the run
        config: Experiment configuration dict
    """
    strategy_name: str
    selected_nodes: Tensor
    f1_before: Optional[float]
    f1_after: float
    f1_drop: Optional[float] = field(init=False)
    f1_drop_ratio: Optional[float] = field(init=False)
    unlearn_time: float
    total_time: float
    selection_time: Optional[float] = None
    selection_reuse_time: Optional[float] = None
    selection_cache_hit: Optional[bool] = None
    selection_cache_key: Optional[str] = None
    selection_cache_source: Optional[str] = None
    mia_auc: Optional[float] = None
    run_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    config: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Calculate derived metrics."""
        if self.f1_before is not None:
            self.f1_drop = self.f1_before - self.f1_after
            if self.f1_before > 0:
                self.f1_drop_ratio = (self.f1_drop / self.f1_before) * 100
            else:
                self.f1_drop_ratio = 0.0
        else:
            self.f1_drop = None
            self.f1_drop_ratio = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "strategy_name": self.strategy_name,
            "selected_nodes": self.selected_nodes.cpu().tolist() if isinstance(self.selected_nodes, Tensor) else list(self.selected_nodes),
            "f1_before": round(self.f1_before, 4) if self.f1_before is not None else None,
            "f1_after": round(self.f1_after, 4),
            "f1_drop": round(self.f1_drop, 4) if self.f1_drop is not None else None,
            "f1_drop_ratio": round(self.f1_drop_ratio, 2) if self.f1_drop_ratio is not None else None,
            "unlearn_time": round(self.unlearn_time, 4),
            "total_time": round(self.total_time, 4),
            "selection_time": round(self.selection_time, 4) if self.selection_time is not None else None,
            "selection_reuse_time": round(self.selection_reuse_time, 6) if self.selection_reuse_time is not None else None,
            "selection_cache_hit": self.selection_cache_hit,
            "selection_cache_key": self.selection_cache_key,
            "selection_cache_source": self.selection_cache_source,
            "mia_auc": round(self.mia_auc, 4) if self.mia_auc is not None else None,
            "run_timestamp": self.run_timestamp,
            "config": self.config or {},
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str):
        """Save result to JSON file."""
        with open(path, 'w') as f:
            f.write(self.to_json())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AttackResult":
        """Create AttackResult from dictionary."""
        # Convert selected_nodes back to tensor
        if "selected_nodes" in data:
            data = data.copy()
            data["selected_nodes"] = torch.tensor(data["selected_nodes"])
        return cls(**{k: v for k, v in data.items() if k not in ["f1_drop", "f1_drop_ratio"]})

    @classmethod
    def load(cls, path: str) -> "AttackResult":
        """Load result from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class ComparisonResult:
    """
    Result of comparing multiple attack strategies.

    Attributes:
        results: List of AttackResult objects
        best_strategy: Name of the best performing strategy
        relative_improvements: Dict mapping strategy pairs to improvement ratios
    """
    results: List[AttackResult]
    config: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate and sort results."""
        if self.results:
            # Sort by f1_drop (descending)
            self.results = sorted(self.results, key=lambda r: r.f1_drop, reverse=True)

    @property
    def best_strategy(self) -> Optional[str]:
        """Get the name of the best strategy."""
        if not self.results:
            return None
        return self.results[0].strategy_name

    @property
    def baseline_result(self) -> Optional[AttackResult]:
        """Get the random baseline result for comparison."""
        for r in self.results:
            if r.strategy_name.lower() in ["random", "randomstrategy"]:
                return r
        return None

    def get_relative_improvement(self, strategy_name: str, baseline_name: str = "random") -> Optional[float]:
        """Get relative improvement of a strategy over baseline."""
        baseline = None
        target = None

        for r in self.results:
            if r.strategy_name.lower() == baseline_name.lower() or \
               r.strategy_name.lower() == baseline_name.lower() + "strategy":
                baseline = r
            if r.strategy_name.lower() == strategy_name.lower() or \
               r.strategy_name.lower() == strategy_name.lower() + "strategy":
                target = r

        if baseline is None or target is None:
            return None

        if baseline.f1_drop > 0:
            return target.f1_drop / baseline.f1_drop
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "config": self.config or {},
            "results": {r.strategy_name: r.to_dict() for r in self.results},
            "comparison": {
                "best_strategy": self.best_strategy,
                "ranking": [
                    {
                        "strategy": r.strategy_name,
                        "f1_drop": round(r.f1_drop, 4),
                        "f1_drop_ratio": round(r.f1_drop_ratio, 2),
                        "unlearn_time": round(r.unlearn_time, 4),
                    }
                    for r in self.results
                ],
                "relative_improvements": {
                    r.strategy_name: round(self.get_relative_improvement(r.strategy_name) or 1.0, 2)
                    for r in self.results
                }
            },
            "timestamp": datetime.now().isoformat(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str):
        """Save comparison result to JSON file."""
        with open(path, 'w') as f:
            f.write(self.to_json())

    def print_summary(self):
        """Print a formatted summary of the comparison."""
        print("\n" + "=" * 60)
        print("Attack Strategy Comparison Results")
        print("=" * 60)

        if not self.results:
            print("No results available.")
            return

        # Print header
        print(f"{'Rank':<6}{'Strategy':<15}{'F1 Drop':<12}{'Ratio(%)':<12}{'Time(s)':<12}{'vs Random':<12}")
        print("-" * 60)

        baseline = self.baseline_result

        for i, r in enumerate(self.results, 1):
            vs_baseline = ""
            if baseline and r.strategy_name != baseline.strategy_name:
                improvement = self.get_relative_improvement(r.strategy_name, baseline.strategy_name)
                if improvement:
                    vs_baseline = f"{improvement:.2f}x"

            print(f"{i:<6}{r.strategy_name:<15}{r.f1_drop:<12.4f}{r.f1_drop_ratio:<12.2f}{r.unlearn_time:<12.2f}{vs_baseline:<12}")

        print("=" * 60)
        print(f"Best Strategy: {self.best_strategy}")
        if baseline:
            best_improvement = self.get_relative_improvement(self.best_strategy, baseline.strategy_name)
            if best_improvement:
                print(f"Improvement over Random: {best_improvement:.2f}x")
        print("=" * 60 + "\n")
