"""
ResultCache - Caching mechanism for attack experiment results.

This module provides caching functionality to avoid re-running identical
experiments. Cache keys are derived from experiment configurations.
"""
import os
import json
import hashlib
import torch
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path

from attack.attack_result import AttackResult, ComparisonResult


class ResultCache:
    """
    Cache for attack experiment results based on configuration.

    Cache keys are generated from specific configuration fields to ensure
    that only truly identical experiments are served from cache.

    Example:
        >>> cache = ResultCache(cache_dir="./results/cache")
        >>> result = cache.get(config)
        >>> if result is None:
        ...     result = run_experiment(config)
        ...     cache.save(result, config)
    """

    # Configuration fields that determine cache identity. Any arg that
    # meaningfully changes f1_after / mia_auc must be here, otherwise two
    # configurations differing only in that arg silently collide.
    CACHE_KEY_FIELDS = [
        'dataset_name',
        'base_model',
        'unlearning_methods',
        'unlearn_ratio',
        'k',  # Explicitly include k for cache key uniqueness
        'random_seed',
        'seed',
        'strategy_name',
        'unlearn_task',
        'downstream_task',
        'is_transductive',
        'is_balanced',
        # GCN over-parameterization (cora=2/64, arxiv=3/256). Without
        # these, an arxiv 3/256 cache entry would collide with a future
        # 4/256 ablation under the same (dataset, model) tuple.
        'gcn_num_layers',
        'gcn_hidden',
        # Per-method loss / fusion coefficients
        'alpha',          # GNNDelete / CGU loss coeff
        'hybrid_alpha',   # Hybrid fusion weight (decoupled from alpha 2026-05-06)
        # Hybrid / IM hyperparameters (added 2026-05-06 for A3 alpha-sweep
        # readiness — without these, sweeping fusion_method or any IM knob
        # would collide on the same ResultCache entry).
        'fusion_method',          # Hybrid: "rank" / "linear" fusion
        'candidate_fraction',     # IM/Hybrid: top-fraction CELF pruning
        'mc_rounds',              # IM/Hybrid: MC rounds for IC simulation
        'im_batch_size',          # IM/Hybrid: batch-CELF batch size
        'im_selector_seed',       # IM/Hybrid: decoupled selector RNG seed
    ]
    LEGACY_CACHE_KEY_FIELDS = [
        'dataset_name',
        'base_model',
        'unlearning_methods',
        'unlearn_ratio',
        'seed',
        'strategy_name',
        'unlearn_task',
        'downstream_task',
        'is_transductive',
        'is_balanced',
    ]

    def __init__(self, cache_dir: str = "./results/cache", max_age_days: int = 30):
        """
        Initialize the result cache.

        Args:
            cache_dir: Directory to store cache files
            max_age_days: Maximum age of cache entries in days (0 = no limit)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_days = max_age_days

    @staticmethod
    def _field_value(config: Dict[str, Any], field: str) -> Any:
        if field == 'random_seed':
            return config.get('random_seed', config.get('seed', "default"))
        if field == 'seed':
            return config.get('seed', config.get('random_seed', "default"))
        return config.get(field, "default")

    def _hash_fields(self, config: Dict[str, Any], fields: List[str]) -> str:
        key_parts = []
        for field in fields:
            value = self._field_value(config, field)
            key_parts.append(f"{field}={value}")
        return "_".join(key_parts)

    def _generate_cache_key(self, config: Dict[str, Any]) -> str:
        """
        Generate a cache key from configuration.

        Args:
            config: Experiment configuration dictionary

        Returns:
            Cache key string
        """
        key_string = self._hash_fields(config, self.CACHE_KEY_FIELDS)

        # Hash to create safe filename
        hash_obj = hashlib.md5(key_string.encode())
        cache_key = hash_obj.hexdigest()[:16]

        return cache_key

    def _generate_legacy_cache_key(self, config: Dict[str, Any]) -> str:
        key_string = self._hash_fields(config, self.LEGACY_CACHE_KEY_FIELDS)
        hash_obj = hashlib.md5(key_string.encode())
        return hash_obj.hexdigest()[:16]

    @staticmethod
    def _should_try_legacy(config: Dict[str, Any]) -> bool:
        """Only allow legacy fallback when k is not explicitly provided."""
        return ('k' not in config) or (config.get('k') is None)

    def _resolve_cache_keys(self, config: Dict[str, Any]) -> List[str]:
        """Build cache lookup keys in priority order."""
        cache_keys = [self._generate_cache_key(config)]
        if self._should_try_legacy(config):
            legacy_key = self._generate_legacy_cache_key(config)
            if legacy_key not in cache_keys:
                cache_keys.append(legacy_key)
        return cache_keys

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """
        Check if a cache entry is still valid (not expired).

        Args:
            cache_path: Path to cache file

        Returns:
            True if cache is valid, False otherwise
        """
        if not cache_path.exists():
            return False

        if self.max_age_days <= 0:
            return True

        # Check file age
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age = datetime.now() - mtime

        return age < timedelta(days=self.max_age_days)

    def get(self, config: Dict[str, Any]) -> Optional[AttackResult]:
        """
        Retrieve a cached result if available.

        Args:
            config: Experiment configuration dictionary

        Returns:
            AttackResult if cache hit, None otherwise
        """
        cache_keys = self._resolve_cache_keys(config)

        for cache_key in cache_keys:
            cache_path = self._get_cache_path(cache_key)
            if not self._is_cache_valid(cache_path):
                continue
            try:
                with open(cache_path, 'r') as f:
                    cache_data = json.load(f)

                if 'result' not in cache_data:
                    continue

                result = AttackResult.from_dict(cache_data['result'])
                print(f"[Cache] Hit for key: {cache_key}")
                print(f"[Cache] Cached at: {cache_data.get('cached_at', 'unknown')}")
                return result
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"[Cache] Error reading cache: {e}")
                continue

        return None

    def save(self, result: AttackResult, config: Dict[str, Any]):
        """
        Save a result to the cache.

        Args:
            result: AttackResult to cache
            config: Experiment configuration dictionary
        """
        cache_key = self._generate_cache_key(config)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            'cache_key': cache_key,
            'cached_at': datetime.now().isoformat(),
            'config': {k: self._field_value(config, k) for k in self.CACHE_KEY_FIELDS},
            'result': result.to_dict(),
        }

        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)

        print(f"[Cache] Saved result to: {cache_path}")

    def invalidate(self, config: Dict[str, Any]) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            config: Experiment configuration dictionary

        Returns:
            True if entry was found and removed, False otherwise
        """
        cache_keys = self._resolve_cache_keys(config)

        removed = False
        for cache_key in cache_keys:
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                cache_path.unlink()
                print(f"[Cache] Invalidated: {cache_key}")
                removed = True

        return removed

    def clear_all(self):
        """Clear all cache entries."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print(f"[Cache] Cleared all entries from {self.cache_dir}")

    def list_entries(self) -> List[Dict[str, Any]]:
        """
        List all cache entries.

        Returns:
            List of cache entry metadata
        """
        entries = []

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)

                entries.append({
                    'cache_key': cache_data.get('cache_key'),
                    'cached_at': cache_data.get('cached_at'),
                    'config': cache_data.get('config'),
                    'strategy': cache_data.get('result', {}).get('strategy_name'),
                    'f1_drop': cache_data.get('result', {}).get('f1_drop'),
                })
            except (json.JSONDecodeError, KeyError):
                continue

        return sorted(entries, key=lambda x: x.get('cached_at', ''), reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        entries = self.list_entries()
        total_size = sum(
            f.stat().st_size
            for f in self.cache_dir.glob("*.json")
        )

        return {
            'num_entries': len(entries),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir),
            'max_age_days': self.max_age_days,
            'entries': entries[:10],  # Last 10 entries
        }


class LogBasedCache:
    """
    Alternative cache implementation that reads from existing log files.

    This is useful for recovering results from previous experiment runs
    without having to use the explicit cache mechanism.
    """

    def __init__(self, log_dir: str = "./log"):
        """
        Initialize the log-based cache.

        Args:
            log_dir: Base directory for logs
        """
        self.log_dir = Path(log_dir)

    def _find_log_file(self, config: Dict[str, Any]) -> Optional[Path]:
        """
        Find a log file matching the configuration.

        Args:
            config: Experiment configuration

        Returns:
            Path to log file if found, None otherwise
        """
        method = config.get('unlearning_methods', '')
        dataset = config.get('dataset_name', '')
        model = config.get('base_model', '')

        # Construct expected log path
        method_dir = self.log_dir / method / dataset / model

        if not method_dir.exists():
            return None

        # Look for timestamped directories
        log_dirs = sorted(method_dir.glob("*"), reverse=True)

        for log_dir in log_dirs:
            if log_dir.is_dir():
                # Look for log files inside
                log_files = list(log_dir.glob("*.log"))
                if log_files:
                    return log_files[0]

        return None

    def _parse_log_for_metrics(self, log_path: Path) -> Optional[Dict[str, float]]:
        """
        Parse a log file for metrics.

        Args:
            log_path: Path to log file

        Returns:
            Dictionary of metrics if found, None otherwise
        """
        metrics = {}

        try:
            with open(log_path, 'r') as f:
                content = f.read()

            # Look for common patterns in logs
            # This is a simple heuristic parser
            lines = content.split('\n')

            for line in lines:
                # Look for F1 scores
                if 'F1 Score' in line and 'Unlearn' in line:
                    try:
                        # Extract number after colon
                        parts = line.split(':')
                        if len(parts) >= 2:
                            value = float(parts[-1].strip().split()[0])
                            metrics['f1_after'] = value
                    except (ValueError, IndexError):
                        pass

                if 'Poison F1 Score' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            value = float(parts[-1].strip().split()[0])
                            metrics['f1_before'] = value
                    except (ValueError, IndexError):
                        pass

                if 'AUC Score' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            value = float(parts[-1].strip().split()[0])
                            metrics['mia_auc'] = value
                    except (ValueError, IndexError):
                        pass

                if 'Unlearning Time' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            value = float(parts[-1].strip().split()[0])
                            metrics['unlearn_time'] = value
                    except (ValueError, IndexError):
                        pass

        except Exception as e:
            print(f"[LogCache] Error parsing log: {e}")
            return None

        return metrics if metrics else None

    def get(self, config: Dict[str, Any]) -> Optional[AttackResult]:
        """
        Try to recover a result from existing logs.

        Args:
            config: Experiment configuration

        Returns:
            AttackResult if found in logs, None otherwise
        """
        log_path = self._find_log_file(config)

        if log_path is None:
            return None

        metrics = self._parse_log_for_metrics(log_path)

        if metrics is None:
            return None

        print(f"[LogCache] Recovered result from: {log_path}")

        # Construct a partial result
        return AttackResult(
            strategy_name=config.get('strategy_name', 'unknown'),
            selected_nodes=torch.tensor([]),  # Not recoverable from logs
            f1_before=metrics.get('f1_before', 0.0),
            f1_after=metrics.get('f1_after', 0.0),
            unlearn_time=metrics.get('unlearn_time', 0.0),
            total_time=metrics.get('unlearn_time', 0.0),
            mia_auc=metrics.get('mia_auc'),
            config=config,
        )
