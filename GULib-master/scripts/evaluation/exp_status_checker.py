"""
exp_status_checker.py - Check experiment progress against checklist.

Parses self/generalization_experiment_checklist.md, scans results/experiments/,
and compares expected vs actual experiments to compute completion rates.

Usage:
    python scripts/evaluation/exp_status_checker.py
    python scripts/evaluation/exp_status_checker.py --phase mg0
    python scripts/evaluation/exp_status_checker.py --phase mg1 --detail
    python scripts/evaluation/exp_status_checker.py --fill --dry-run
    python scripts/evaluation/exp_status_checker.py --fill --yes
"""
import os
import re
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from dataclasses import dataclass, asdict


class ExperimentKey(NamedTuple):
    """Unique identifier for an experiment."""
    phase: str
    method: str
    dataset: str
    model: str
    seed: int
    strategy: str
    ratio: float = 0.05  # Default ratio for MG experiments

    def __str__(self):
        return f"{self.phase}:{self.method}/{self.dataset}/{self.model}/seed={self.seed}/{self.strategy}/r{self.ratio}"


@dataclass
class PhaseConfig:
    """Configuration for an experiment phase."""
    name: str
    dir_name: str
    methods: List[str]
    dataset: str
    model: str
    seeds: List[int]
    strategies: List[str]  # 正式策略（报告用）
    legacy_strategies: List[str] = None  # 旧版策略（作为cache保留，不计入checklist）

    @property
    def total_runs(self) -> int:
        """正式实验总数（用于计算完成率）"""
        return len(self.methods) * len(self.seeds) * len(self.strategies)

    @property
    def all_strategies(self) -> List[str]:
        """所有策略（正式 + legacy）"""
        legacy = self.legacy_strategies or []
        return self.strategies + legacy


# Phase configurations based on checklist.md
# Note: legacy_strategies are kept as cache but not counted in checklist completion
PHASE_CONFIGS = {
    "mg0": PhaseConfig(
        name="MG-0",
        dir_name="mg0_completion",
        methods=["GIF", "GNNDelete", "GraphEraser", "GUIDE"],
        dataset="cora",
        model="GCN",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"],
        legacy_strategies=["im", "hybrid"]  # Old versions kept as cache
    ),
    "mg1": PhaseConfig(
        name="MG-1",
        dir_name="mg1_citeseer",
        methods=["GIF", "GNNDelete", "GraphEraser"],
        dataset="citeseer",
        model="GCN",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"],
        legacy_strategies=["im", "hybrid"]
    ),
    "mg2": PhaseConfig(
        name="MG-2",
        dir_name="mg2_gat",
        methods=["GIF", "GNNDelete", "GraphEraser"],
        dataset="cora",
        model="GAT",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"],
        legacy_strategies=["im", "hybrid"]
    ),
    "mg3_citeseer": PhaseConfig(
        name="MG-3-Citeseer",
        dir_name="mg3_citeseer",
        methods=["IDEA", "MEGU"],
        dataset="citeseer",
        model="GCN",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "tracin", "im_v4", "hybrid_v4"],
        legacy_strategies=["im", "hybrid"]
    ),
    "mg3_gat": PhaseConfig(
        name="MG-3-GAT",
        dir_name="mg3_gat",
        methods=["IDEA", "MEGU"],
        dataset="cora",
        model="GAT",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "tracin", "im_v4", "hybrid_v4"],
        legacy_strategies=["im", "hybrid"]
    ),
    "ratio_sensitivity": PhaseConfig(
        name="P2-Ratio",
        dir_name="ratio_sensitivity",
        methods=["GIF", "GNNDelete"],
        dataset="cora",
        model="GCN",
        seeds=[42, 212, 722, 1337, 2024],
        strategies=["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"],
        # Ratios: 0.2, 0.1, 0.05, 0.01 - handled specially in scan
    ),
}


def parse_checklist(path: str) -> Dict[str, List[ExperimentKey]]:
    """
    Parse the checklist markdown file to extract marked experiments.

    Returns a dict mapping phase names to lists of completed experiment keys.
    """
    if not os.path.exists(path):
        return {}

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    completed = {}

    # Look for [x] markers indicating completed experiments
    # Pattern matches lines like: - [x] `MG-0`：`Cora / GCN / GUIDE / seed=42 / random`
    pattern = r'- \[x\]\s*`([^`]+)`\s*：\s*`([^`]+)`'
    matches = re.finditer(pattern, content)

    for match in matches:
        phase_marker = match.group(1).lower()
        details = match.group(2)

        # Try to parse details like "Cora / GCN / GUIDE / seed=42 / random"
        parts = [p.strip() for p in details.split('/')]

        if len(parts) >= 5:
            dataset = parts[0].lower()
            model = parts[1].upper()

            # Check if ratio is included (new format)
            ratio = 0.05  # default
            method_idx = 2

            # Check if parts[2] is a ratio like "r=0.05" or "ratio=0.05"
            ratio_match = re.match(r'r(?:atio)?=?(\d+\.?\d*)', parts[2])
            if ratio_match:
                ratio = float(ratio_match.group(1))
                method_idx = 3

            if len(parts) >= method_idx + 2:
                method = parts[method_idx]
                seed_part = parts[method_idx + 1]
                strategy = parts[method_idx + 2].lower()

                # Extract seed number
                seed_match = re.search(r'seed=(\d+)', seed_part)
                if seed_match:
                    seed = int(seed_match.group(1))

                # Determine phase
                phase = None
                for pkey, pconfig in PHASE_CONFIGS.items():
                    if (pconfig.dataset.lower() == dataset and
                        pconfig.model.upper() == model and
                        method in pconfig.methods and
                        seed in pconfig.seeds and
                        strategy in pconfig.strategies):
                        phase = pkey
                        break

                if phase:
                    key = ExperimentKey(phase, method, dataset, model, seed, strategy, ratio)
                    if phase not in completed:
                        completed[phase] = []
                    completed[phase].append(key)

    return completed


def scan_actual_results(base_dir: str) -> Tuple[Set[ExperimentKey], Set[ExperimentKey]]:
    """
    Scan results/experiments/ directory to find actual completed experiments.

    Returns:
        Tuple of (official_experiments, legacy_experiments)
        - official: experiments with strategies in phase_config.strategies
        - legacy: experiments with strategies in phase_config.legacy_strategies
    """
    official_found = set()
    legacy_found = set()
    base_path = Path(base_dir)

    if not base_path.exists():
        return official_found, legacy_found

    for phase_key, phase_config in PHASE_CONFIGS.items():
        phase_dir = base_path / phase_config.dir_name / "phase_a"
        if not phase_dir.exists():
            continue

        # Build set of official and legacy strategies for quick lookup
        official_strategies = set(s.lower() for s in phase_config.strategies)
        legacy_strategies = set(s.lower() for s in (phase_config.legacy_strategies or []))

        # Look for seed directories like 20260221_184153_seed2024
        for seed_dir in phase_dir.iterdir():
            if not seed_dir.is_dir():
                continue

            # Extract seed from directory name
            seed_match = re.search(r'seed(\d+)', seed_dir.name)
            if not seed_match:
                continue
            seed = int(seed_match.group(1))

            # Look for _summary.json
            summary_file = seed_dir / "_summary.json"
            if not summary_file.exists():
                continue

            # Parse summary file
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Extract ratio from config (default to 0.05 for MG experiments)
                config = data.get('config', {})
                ratios = config.get('ratios', [0.05])

                # Extract results from summary
                results = data.get('results', {})
                for method_dataset_key, method_data in results.items():
                    # key format: "GIF_cora_GCN_0.05" or "GIF_cora_GCN_r0.2" for ratio_sensitivity
                    parts = method_dataset_key.split('_')
                    if len(parts) >= 3:
                        method = parts[0]
                        dataset = parts[1].lower()
                        model = parts[2].upper()

                        # For ratio_sensitivity, extract ratio from the key (e.g., "r0.2")
                        # Otherwise use config ratios
                        ratio_list = []
                        for part in parts[3:]:
                            if part.startswith('r'):
                                try:
                                    ratio_val = float(part[1:])  # Remove 'r' prefix
                                    ratio_list.append(ratio_val)
                                except ValueError:
                                    pass
                        if not ratio_list:
                            ratio_list = ratios if ratios else [0.05]

                        # Get strategy results
                        strategy_results = method_data.get('results', {})
                        for strategy in strategy_results.keys():
                            if strategy and strategy != 'comparison':
                                strategy_lower = strategy.lower()

                                # Create entry for each ratio
                                for ratio in ratio_list:
                                    key = ExperimentKey(
                                        phase=phase_key,
                                        method=method,
                                        dataset=dataset,
                                        model=model,
                                        seed=seed,
                                        strategy=strategy_lower,
                                        ratio=ratio
                                    )
                                # Categorize as official or legacy
                                if strategy_lower in official_strategies:
                                    official_found.add(key)
                                elif strategy_lower in legacy_strategies:
                                    legacy_found.add(key)
                                else:
                                    # Unknown strategy - treat as official for now
                                    official_found.add(key)

            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to parse {summary_file}: {e}", file=sys.stderr)
                continue

    return official_found, legacy_found


@dataclass
class ProgressReport:
    """Report of experiment progress."""
    phase: str
    total: int  # 正式实验总数
    completed: int  # 正式实验完成数
    remaining: int  # 剩余正式实验
    completion_pct: float
    legacy_count: int = 0  # legacy实验数量（作为cache保留）


@dataclass
class GapAnalysis:
    """Analysis of gaps between expected and actual experiments."""
    missing: Set[ExperimentKey]  # Actual has but checklist doesn't record
    extra: Set[ExperimentKey]    # Checklist records but actual doesn't have


def compute_progress(expected: Dict[str, List[ExperimentKey]],
                    official: Set[ExperimentKey],
                    legacy: Set[ExperimentKey]) -> Dict[str, ProgressReport]:
    """
    Compute progress for each phase.

    Args:
        expected: Dict mapping phase -> list of completed experiment keys from checklist
        official: Set of official experiment keys found in results directory
        legacy: Set of legacy experiment keys found in results directory (cache)

    Returns:
        Dict mapping phase name to ProgressReport
    """
    reports = {}

    for phase_key, phase_config in PHASE_CONFIGS.items():
        # Count completed from official results that match this phase
        completed = sum(1 for key in official if key.phase == phase_key)
        legacy_count = sum(1 for key in legacy if key.phase == phase_key)

        # For ratio_sensitivity, calculate total based on config (methods x strategies x ratios x seeds)
        # ratios: 0.2, 0.1, 0.05, 0.01 = 4 ratios
        if phase_key == "ratio_sensitivity":
            num_ratios = 4  # 0.2, 0.1, 0.05, 0.01
            total = len(phase_config.methods) * len(phase_config.strategies) * num_ratios * len(phase_config.seeds)
        else:
            total = phase_config.total_runs

        reports[phase_key] = ProgressReport(
            phase=phase_config.name,
            total=total,
            completed=completed,
            remaining=total - completed,
            completion_pct=(completed / total * 100) if total > 0 else 0,
            legacy_count=legacy_count
        )

    return reports


def analyze_gaps(expected: Dict[str, List[ExperimentKey]],
                official: Set[ExperimentKey],
                legacy: Set[ExperimentKey]) -> GapAnalysis:
    """
    Analyze gaps between checklist and actual results.

    Returns GapAnalysis with:
    - missing: experiments that exist in official but not in checklist
    - extra: experiments that are in checklist but not in official

    Note: legacy experiments are not counted as missing (they are kept as cache)
    """
    # Flatten expected into a set
    expected_set = set()
    for phase_keys in expected.values():
        expected_set.update(phase_keys)

    # Only official experiments count for gap analysis
    missing = official - expected_set  # Official has but checklist doesn't
    extra = expected_set - official    # Checklist has but official doesn't

    return GapAnalysis(missing=missing, extra=extra)


def format_progress_table(reports: Dict[str, ProgressReport]) -> str:
    """Format progress reports as a table."""
    lines = []
    lines.append("=" * 85)
    lines.append(f"{'Phase':<18} {'Total':>8} {'Completed':>10} {'Remaining':>10} {'Progress':>10} {'Legacy':>8}")
    lines.append("-" * 85)

    total_total = 0
    total_completed = 0
    total_legacy = 0

    for phase_key in ["mg0", "mg1", "mg2", "mg3_citeseer", "mg3_gat", "ratio_sensitivity"]:
        if phase_key in reports:
            r = reports[phase_key]
            legacy_str = f"({r.legacy_count})" if r.legacy_count > 0 else "-"
            lines.append(f"{r.phase:<18} {r.total:>8} {r.completed:>10} {r.remaining:>10} {r.completion_pct:>9.0f}% {legacy_str:>8}")
            total_total += r.total
            total_completed += r.completed
            total_legacy += r.legacy_count

    lines.append("-" * 85)
    total_pct = (total_completed / total_total * 100) if total_total > 0 else 0
    legacy_total_str = f"({total_legacy})" if total_legacy > 0 else "-"
    lines.append(f"{'Total':<18} {total_total:>8} {total_completed:>10} {total_total - total_completed:>10} {total_pct:>9.0f}% {legacy_total_str:>8}")
    lines.append("=" * 85)
    lines.append("")
    lines.append("Note: Legacy = old strategy versions kept as cache (im/hybrid -> im_v4/hybrid_v4)")

    return "\n".join(lines)


def format_detail_output(reports: Dict[str, ProgressReport],
                        gaps: GapAnalysis,
                        phase_filter: Optional[str] = None) -> str:
    """Format detailed output showing missing experiments."""
    lines = []

    for phase_key, report in reports.items():
        if phase_filter and phase_key != phase_filter.lower():
            continue

        phase_config = PHASE_CONFIGS.get(phase_key)
        if not phase_config:
            continue

        lines.append(f"\n{report.phase}: {phase_config.dataset.upper()} / {phase_config.model}")
        lines.append(f"  Total: {report.total} runs ({len(phase_config.methods)} methods x {len(phase_config.strategies)} strategies x {len(phase_config.seeds)} seeds)")
        lines.append(f"  Completed: {report.completed}/{report.total}")
        lines.append(f"  Methods: {', '.join(phase_config.methods)}")
        lines.append(f"  Seeds: {', '.join(map(str, phase_config.seeds))}")

        # Show missing experiments
        phase_missing = [k for k in gaps.missing if k.phase == phase_key]
        if phase_missing:
            lines.append(f"\n  [Missing in checklist - auto-discovered]")
            for key in sorted(phase_missing, key=lambda k: (k.method, k.seed, k.strategy))[:10]:
                lines.append(f"    - {key.method}/{key.dataset}/{key.model}/seed={key.seed}/{key.strategy}")
            if len(phase_missing) > 10:
                lines.append(f"    ... and {len(phase_missing) - 10} more")

        phase_extra = [k for k in gaps.extra if k.phase == phase_key]
        if phase_extra:
            lines.append(f"\n  [Extra in checklist - not found in results]")
            for key in sorted(phase_extra, key=lambda k: (k.method, k.seed, k.strategy))[:10]:
                lines.append(f"    - {key.method}/{key.dataset}/{key.model}/seed={key.seed}/{key.strategy}")
            if len(phase_extra) > 10:
                lines.append(f"    ... and {len(phase_extra) - 10} more")

    return "\n".join(lines)


def generate_fill_suggestions(gaps: GapAnalysis) -> List[Dict]:
    """Generate suggestions for filling the checklist."""
    suggestions = []

    # Missing: actual has but checklist doesn't
    for key in sorted(gaps.missing):
        suggestions.append({
            'type': 'missing',
            'phase': key.phase,
            'method': key.method,
            'dataset': key.dataset,
            'model': key.model,
            'seed': key.seed,
            'strategy': key.strategy,
            'action': 'add',
            'description': f"Add completed experiment to checklist"
        })

    # Extra: checklist has but actual doesn't
    for key in sorted(gaps.extra):
        suggestions.append({
            'type': 'extra',
            'phase': key.phase,
            'method': key.method,
            'dataset': key.dataset,
            'model': key.model,
            'seed': key.seed,
            'strategy': key.strategy,
            'action': 'review',
            'description': f"Experiment marked complete but not found in results"
        })

    return suggestions


def load_auto_discovered(path: str) -> Dict[str, List[ExperimentKey]]:
    """
    Load auto-discovered experiments from JSON file.

    Returns a dict mapping phase names to lists of experiment keys.
    """
    if not os.path.exists(path):
        return {}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        completed = {}
        for entry in data.get('entries', []):
            key = ExperimentKey(
                phase=entry['phase'],
                method=entry['method'],
                dataset=entry['dataset'],
                model=entry['model'],
                seed=entry['seed'],
                strategy=entry['strategy'],
                ratio=entry.get('ratio', 0.05)
            )
            if key.phase not in completed:
                completed[key.phase] = []
            completed[key.phase].append(key)

        return completed
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to load auto_discovered.json: {e}", file=sys.stderr)
        return {}


def get_auto_discovered_path() -> str:
    """Get the path to the auto_discovered.json file."""
    return os.path.join('results', 'experiments', 'auto_discovered.json')


def log_auto_discovered(gaps: GapAnalysis, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Log auto-discovered experiments to JSON file instead of modifying checklist.

    Args:
        gaps: GapAnalysis with missing experiments to log
        dry_run: If True, don't actually write changes

    Returns:
        (success, message)
    """
    # Filter to only missing experiments (actual has but checklist doesn't)
    to_add = sorted(gaps.missing)

    if not to_add:
        return True, "No missing experiments to log."

    json_path = get_auto_discovered_path()

    # Load existing data if file exists
    existing_data = {'last_updated': None, 'sources': {}, 'entries': []}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Build set of existing entries to avoid duplicates
    existing_keys = set()
    for entry in existing_data.get('entries', []):
        key = (entry['phase'], entry['method'], entry['dataset'], entry['model'],
               entry['seed'], entry['strategy'], entry.get('ratio', 0.05))
        existing_keys.add(key)

    # Add new entries
    new_entries = []
    sources_count = {}

    for key in to_add:
        key_tuple = (key.phase, key.method, key.dataset, key.model,
                     key.seed, key.strategy, key.ratio)
        if key_tuple in existing_keys:
            continue

        entry = {
            'phase': key.phase,
            'method': key.method,
            'dataset': key.dataset,
            'model': key.model,
            'seed': key.seed,
            'strategy': key.strategy,
            'ratio': key.ratio,
            'discovered_at': datetime.now().isoformat()
        }
        new_entries.append(entry)

        # Count by source (phase)
        phase = key.phase
        sources_count[phase] = sources_count.get(phase, 0) + 1

    if not new_entries:
        return True, "All missing experiments already logged."

    # Update sources count
    existing_sources = existing_data.get('sources', {})
    for phase, count in sources_count.items():
        existing_sources[phase] = existing_sources.get(phase, 0) + count

    # Prepare new data
    new_data = {
        'last_updated': datetime.now().isoformat(),
        'sources': existing_sources,
        'entries': existing_data.get('entries', []) + new_entries
    }

    if dry_run:
        return True, f"[DRY-RUN] Would log {len(new_entries)} entries to {json_path}"
    else:
        # Ensure directory exists
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        return True, f"Logged {len(new_entries)} entries to {json_path}"


def aggregate_metrics(phase: str) -> Dict[str, Dict[str, any]]:
    """
    Aggregate metrics from _summary.json files for a phase.

    Returns a dict mapping metric type to method-level values:
    {
        'f1_drop': {'GIF': '6.8%±0.5', 'GNNDelete': '17.2%±2.1', ...},
        'mia_auc': {'GIF': '0.60', 'GNNDelete': '0.86', ...},
        'collateral': {'GIF': 'yes', 'GNNDelete': 'no', ...},
        'relative': {'GIF': 'yes', 'GNNDelete': '-', ...},
    }
    """
    import numpy as np

    base_path = Path('results/experiments')
    phase_config = PHASE_CONFIGS.get(phase)
    if not phase_config:
        return {}

    phase_dir = base_path / phase_config.dir_name / "phase_a"
    if not phase_dir.exists():
        return {}

    # Collect metrics by method
    method_metrics = {}

    # First, scan collateral directory to find completed collateral evaluations
    # Format: results/collateral/{method}/{dataset}/{model}/
    collateral_base = Path('results/collateral')
    for method in phase_config.methods:
        # Check for collateral results for this method + dataset + model combination
        method_collateral_dir = collateral_base / method / phase_config.dataset / phase_config.model
        if method_collateral_dir.exists():
            collateral_files = list(method_collateral_dir.glob('collateral_*.json'))
            if collateral_files:
                # Found collateral results for this method
                for m in phase_config.methods:
                    if m not in method_metrics:
                        method_metrics[m] = {
                            'f1_drops': [],
                            'mia_aucs': [],
                            'has_collateral': False,
                            'has_relative': False,
                            'relative_f1_drops': [],
                        }
                method_metrics[method]['has_collateral'] = True

    # Scan results/relative/ directory (generated by eval_relative.py)
    relative_base = Path('results/relative')
    for method in phase_config.methods:
        method_relative_dir = relative_base / method / phase_config.dataset / phase_config.model
        if method_relative_dir.exists():
            relative_files = list(method_relative_dir.glob('relative_seed*.json'))
            if relative_files:
                if method not in method_metrics:
                    method_metrics[method] = {
                        'f1_drops': [],
                        'mia_aucs': [],
                        'has_collateral': False,
                        'has_relative': False,
                        'relative_f1_drops': [],
                    }
                method_metrics[method]['has_relative'] = True
                for rf in relative_files:
                    try:
                        with open(rf, 'r', encoding='utf-8') as f:
                            rel_data = json.load(f)
                        for entry in rel_data.get('results', []):
                            val = entry.get('relative_f1_drop')
                            if val is not None:
                                method_metrics[method]['relative_f1_drops'].append(val)
                    except (json.JSONDecodeError, IOError):
                        continue

    for seed_dir in phase_dir.iterdir():
        if not seed_dir.is_dir():
            continue

        summary_file = seed_dir / "_summary.json"
        if not summary_file.exists():
            continue

        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            results = data.get('results', {})
            for method_key, method_data in results.items():
                # Extract method name (e.g., "GIF_cora_GCN_0.05" -> "GIF")
                method_name = method_key.split('_')[0] if method_key else None
                if not method_name or method_name not in phase_config.methods:
                    continue

                if method_name not in method_metrics:
                    method_metrics[method_name] = {
                        'f1_drops': [],
                        'mia_aucs': [],
                        'has_collateral': False,
                        'has_relative': False,
                        'relative_f1_drops': [],
                    }

                # Extract attack results - data is in method_data['results'][strategy]
                strategy_results = method_data.get('results', {})
                for strategy, strategy_data in strategy_results.items():
                    if strategy == 'comparison' or not strategy:
                        continue

                    # F1 Drop - directly in strategy_data
                    f1_drop = strategy_data.get('f1_drop')
                    if f1_drop is not None:
                        method_metrics[method_name]['f1_drops'].append(f1_drop)

                    # MIA AUC - directly in strategy_data
                    mia_auc = strategy_data.get('mia_auc')
                    if mia_auc is not None:
                        method_metrics[method_name]['mia_aucs'].append(mia_auc)

                    # Collateral (retrain gap) - check for collateral_metrics
                    if strategy_data.get('collateral_metrics'):
                        method_metrics[method_name]['has_collateral'] = True

                    # Relative - now detected via results/relative/ directory scan above

        except (json.JSONDecodeError, IOError) as e:
            continue

    # Aggregate into final format
    aggregated = {
        'f1_drop': {},
        'mia_auc': {},
        'collateral': {},
        'relative': {}
    }

    for method, metrics in method_metrics.items():
        # F1 Drop: compute mean +/- std (convert to percentage)
        f1_drops = metrics['f1_drops']
        if f1_drops:
            mean_val = np.mean(f1_drops) * 100  # Convert to percentage
            std_val = np.std(f1_drops) * 100
            aggregated['f1_drop'][method] = f"{mean_val:.1f}%+/-{std_val:.1f}"
        else:
            aggregated['f1_drop'][method] = "-"

        # MIA AUC: compute mean
        mia_aucs = metrics['mia_aucs']
        if mia_aucs:
            mean_auc = np.mean(mia_aucs)
            aggregated['mia_auc'][method] = f"{mean_auc:.2f}"
        else:
            aggregated['mia_auc'][method] = "-"

        # Collateral: check if available
        aggregated['collateral'][method] = "yes" if metrics['has_collateral'] else "no"

        # Relative: compute mean +/- std of relative_f1_drop (percentage)
        rel_drops = metrics['relative_f1_drops']
        if rel_drops:
            mean_val = np.mean(rel_drops) * 100
            std_val = np.std(rel_drops) * 100
            aggregated['relative'][method] = f"{mean_val:.1f}%+/-{std_val:.1f}"
        elif metrics['has_relative']:
            aggregated['relative'][method] = "yes"
        else:
            aggregated['relative'][method] = "-"

    return aggregated


def update_checklist_status(checklist_path: str, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Update checklist.md with completion status based on auto_discovered.json.

    This function:
    1. Reads auto_discovered.json to get completed phases and counts
    2. Updates checklist.md sections (2.1-2.4, 2.6) from [ ] to [x]
    3. Adds completion date and run count reference

    Args:
        checklist_path: Path to checklist file
        dry_run: If True, don't actually write changes

    Returns:
        (success, message)
    """
    auto_discovered_path = get_auto_discovered_path()

    if not os.path.exists(auto_discovered_path):
        return False, "auto_discovered.json not found. Run --fill first to create it."

    # Load auto_discovered to get run counts
    try:
        with open(auto_discovered_path, 'r', encoding='utf-8') as f:
            auto_data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return False, f"Failed to load auto_discovered.json: {e}"

    # Count runs per phase
    phase_counts = {}
    for entry in auto_data.get('entries', []):
        phase = entry['phase']
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    if not phase_counts:
        return True, "No entries in auto_discovered.json to sync."

    # Read checklist
    if not os.path.exists(checklist_path):
        return False, f"Checklist file not found: {checklist_path}"

    with open(checklist_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Backup
    if not dry_run:
        backup_path = checklist_path + ".bak"
        shutil.copy2(checklist_path, backup_path)

    # Phase to Section mapping
    phase_to_section = {
        "mg0": ("### 2.1", "MG-0 稳定性"),
        "mg1": ("### 2.2", "MG-1 最小跨数据集泛化"),
        "mg2": ("### 2.3", "MG-2 最小跨模型泛化"),
        "mg3_citeseer": ("### 2.4", "MG-3"),
        "mg3_gat": ("### 2.4", "MG-3"),
        "ratio_sensitivity": ("### 2.6", "Ratio 敏感性"),
    }

    # Expected run counts for each phase (for validation)
    expected_counts = {
        "mg0": 4 * 6 * 5,  # 4 methods x 6 strategies x 5 seeds = 120
        "mg1": 3 * 6 * 5,  # 3 methods x 6 strategies x 5 seeds = 90
        "mg2": 3 * 6 * 5,  # 3 methods x 6 strategies x 5 seeds = 90
        "mg3_citeseer": 2 * 4 * 5,  # 2 methods x 4 strategies x 5 seeds = 40
        "mg3_gat": 2 * 4 * 5,  # 2 methods x 4 strategies x 5 seeds = 40
        "ratio_sensitivity": 2 * 6 * 4 * 5,  # 2 methods x 6 strategies x 4 ratios x 5 seeds = 240
    }

    updated_sections = []
    updated_metrics = []  # Track sections with metrics updates
    today = datetime.now().strftime("%Y-%m-%d")

    # Process each phase with entries
    for phase, count in phase_counts.items():
        if phase not in phase_to_section:
            continue

        section_header, section_name = phase_to_section[phase]
        phase_config = PHASE_CONFIGS.get(phase)
        expected = expected_counts.get(phase, 0)

        # Calculate completion ratio
        is_complete = count >= expected * 0.9  # Allow 90% threshold

        # Find the section
        section_pattern = rf"{re.escape(section_header)}.*?\n(.*?)(?=\n### |\Z)"
        section_match = re.search(section_pattern, content, re.DOTALL)

        if not section_match:
            continue

        section_content = section_match.group(0)
        bullet_content = section_match.group(1)

        # Look for the main bullet (both - [ ] and - [x])
        # Try format with backticks first, then without
        bullet_pattern = r'(- \[x?\])\s+`([^`]+)`'
        bullet_match = re.search(bullet_pattern, bullet_content)

        if not bullet_match:
            # Try format without backticks (e.g., "- [x] 在 MG-1 + MG-2 基础上增加...")
            bullet_pattern = r'(- \[x?\])\s+(.+)'
            bullet_match = re.search(bullet_pattern, bullet_content)

        if bullet_match:
            # Update with completion info
            old_bullet = bullet_match.group(0)
            checkbox = bullet_match.group(1)  # "- [ ]" or "- [x]"
            details = bullet_match.group(2)   # "Cora / GCN / ratio=0.05 / 5 seeds"

            # Check if already has auto_discovered (prevent duplicates)
            has_auto_discovered = "auto_discovered" in old_bullet

            if checkbox == "- [x]" and has_auto_discovered:
                # Already has everything - check if date needs update
                date_pattern = r'\*\*状态\*\*：✅ 完成 \(\d{4}-\d{2}-\d{2}\)'
                if re.search(date_pattern, old_bullet):
                    # Update date only
                    new_bullet = re.sub(
                        date_pattern,
                        f'**状态**：✅ 完成 ({today})',
                        old_bullet
                    )
                else:
                    new_bullet = old_bullet  # No change needed
            elif checkbox == "- [x]" and not has_auto_discovered:
                # Has [x] but missing auto_discovered count - add it
                # For format with backticks
                if "`" in details:
                    new_bullet = old_bullet.replace(
                        f"- [x] `{details}`",
                        f"- [x] `{details}`（auto_discovered: {count} runs）"
                    )
                else:
                    # For format without backticks
                    new_bullet = old_bullet.replace(
                        f"- [x] {details}",
                        f"- [x] {details}（auto_discovered: {count} runs）"
                    )

                # Add or update status date
                if "**状态**" in section_content:
                    new_bullet = re.sub(
                        r'\*\*状态\*\*：✅ 完成 \(\d{4}-\d{2}-\d{2}\)',
                        f'**状态**：✅ 完成 ({today})',
                        new_bullet
                    )
                else:
                    new_bullet += f"\n  - **状态**：✅ 完成 ({today})"
            elif checkbox == "- [ ]":
                # Mark as complete ([ ] → [x])
                new_bullet = f"- [x] `{details}`（auto_discovered: {count} runs）\n  - **状态**：✅ 完成 ({today})"
            else:
                new_bullet = old_bullet  # No change needed

            # Always add/update evaluation metrics for completed sections
            if checkbox == "- [x]":
                # Get aggregated metrics for this phase
                metrics_data = aggregate_metrics(phase)

                if metrics_data and any(metrics_data.values()):
                    # Get methods from config
                    methods = phase_config.methods if phase_config else []

                    # Build new format metrics summary (by metric type, not by method)
                    metrics_lines = ["  - **评估汇总**："]

                    # F1 Drop row
                    f1_parts = []
                    for m in methods:
                        val = metrics_data.get('f1_drop', {}).get(m, '-')
                        f1_parts.append(f"{m}={val}")
                    if f1_parts:
                        metrics_lines.append(f"    - **F1 Drop**: {', '.join(f1_parts)}")

                    # MIA AUC row
                    mia_parts = []
                    for m in methods:
                        val = metrics_data.get('mia_auc', {}).get(m, '-')
                        mia_parts.append(f"{m}={val}")
                    if mia_parts:
                        metrics_lines.append(f"    - **MIA AUC**: {', '.join(mia_parts)}")

                    # Collateral row
                    col_parts = []
                    for m in methods:
                        val = metrics_data.get('collateral', {}).get(m, 'no')
                        col_parts.append(f"{m}={val}")
                    if col_parts:
                        metrics_lines.append(f"    - **Collateral**: {', '.join(col_parts)}")

                    # Relative row
                    rel_parts = []
                    for m in methods:
                        val = metrics_data.get('relative', {}).get(m, '-')
                        rel_parts.append(f"{m}={val}")
                    if rel_parts:
                        metrics_lines.append(f"    - **Relative**: {', '.join(rel_parts)}")

                    metrics_summary = "\n".join(metrics_lines)

                    # Check if "评估汇总" already exists, update or add
                    if "**评估汇总**" in section_content:
                        # Replace existing evaluation summary
                        old_metrics_pattern = r'  - \*\*评估汇总\*\*：.*?(?=\n  - |\n\n|\Z)'
                        section_content = re.sub(old_metrics_pattern, metrics_summary, section_content, flags=re.DOTALL)
                    else:
                        # Add after the bullet (at the end of section_content)
                        # Find where to insert: after bullet content, before next sub-bullet or section end
                        bullet_end_pattern = r'(- \[x\] `[^\n]+`[^\n]*)'
                        bullet_match = re.search(bullet_end_pattern, section_content)
                        if bullet_match:
                            insert_pos = bullet_match.end()
                            # Find next line that starts with "  - " or empty line
                            rest_content = section_content[insert_pos:]
                            next_bullet = re.search(r'\n  - ', rest_content)
                            if next_bullet:
                                insert_pos = insert_pos + next_bullet.start()
                                section_content = section_content[:insert_pos] + "\n" + metrics_summary + section_content[insert_pos:]
                            else:
                                section_content = section_content + "\n" + metrics_summary

                    # Update content with modified section_content
                    content = content.replace(section_match.group(0), section_content)
                    updated_metrics.append(section_name)

            if old_bullet != new_bullet:
                content = content.replace(old_bullet, new_bullet, 1)
                updated_sections.append(f"{section_name}: {count} runs")

    # Handle P2-Ratio section 2.6 if needed (not in checklist yet)
    if "ratio_sensitivity" in phase_counts and "### 2.6" not in content:
        # Need to add Section 2.6
        ratio_section = """
### 2.6 Ratio 敏感性（攻击强度曲线）

- [x] `Cora / GCN / GIF / ratio=0.01,0.05,0.10,0.20 / 5 seeds`（auto_discovered: {} runs）
  - seeds: `42, 212, 722, 2024, 1337`
  - methods: `GIF, GNNDelete`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - ratios: `0.01, 0.05, 0.10, 0.20`
  - 规模：`2 methods × 6 strategies × 4 ratios × 5 seeds = 240 runs`
  - **状态**：✅ 完成 ({})

""".format(phase_counts.get("ratio_sensitivity", 0), today)

        # Find insertion point (after Section 2.5)
        insert_pattern = r'(### 2.5 最小泛化通过标准.*?)(?=## |\Z)'
        insert_match = re.search(insert_pattern, content, re.DOTALL)
        if insert_match:
            content = content[:insert_match.end()] + ratio_section + content[insert_match.end():]
            updated_sections.append("Ratio 敏感性 (new section added)")

    if not updated_sections and not updated_metrics:
        return True, "No sections needed updating."

    # Combine both types of updates
    all_updates = updated_sections + [f"{m}: metrics" for m in updated_metrics if m not in updated_sections]

    # Write back
    if dry_run:
        return True, f"[DRY-RUN] Would update {len(all_updates)} sections: {', '.join(all_updates)}"
    else:
        with open(checklist_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, f"Updated {len(all_updates)} sections: {', '.join(all_updates)} (backup: {checklist_path}.bak)"


###############################################################################
# Evaluation coverage scanning (collateral / relative)
###############################################################################

# Expected evaluation matrix: (method, dataset, model, ratio) combinations
# that should have collateral and relative evaluations.
EVAL_EXPECTED = {
    # Matches actual experiment runs per phase (see PHASE_CONFIGS)
    "mg0": {
        "methods": ["GIF", "GNNDelete", "GraphEraser", "GUIDE"],
        "dataset": "cora", "model": "GCN", "ratios": [0.05],
    },
    "mg1": {
        "methods": ["GIF", "GNNDelete", "GraphEraser"],
        "dataset": "citeseer", "model": "GCN", "ratios": [0.05],
    },
    "mg2": {
        "methods": ["GIF", "GNNDelete", "GraphEraser"],
        "dataset": "cora", "model": "GAT", "ratios": [0.05],
    },
    "mg3_citeseer": {
        "methods": ["IDEA", "MEGU"],
        "dataset": "citeseer", "model": "GCN", "ratios": [0.05],
    },
    "mg3_gat": {
        "methods": ["IDEA", "MEGU"],
        "dataset": "cora", "model": "GAT", "ratios": [0.05],
    },
    "ratio_sensitivity": {
        "methods": ["GIF", "GNNDelete"],
        "dataset": "cora", "model": "GCN", "ratios": [0.01, 0.05, 0.10, 0.20],
    },
}


def _scan_collateral(base_dir: str = "results/collateral") -> dict:
    """Scan collateral results and return {(method, dataset, model, ratio): set(strategies)}."""
    base = Path(base_dir)
    coverage = {}
    if not base.exists():
        return coverage
    for fpath in base.rglob("collateral_*.json"):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data.get("config", {})
            key = (
                cfg.get("unlearning_methods", ""),
                cfg.get("dataset_name", ""),
                cfg.get("base_model", ""),
                round(float(cfg.get("unlearn_ratio", 0)), 4),
            )
            strats = set()
            for r in data.get("results", []):
                s = r.get("strategy", "")
                if s:
                    strats.add(s)
            if key not in coverage:
                coverage[key] = set()
            coverage[key] |= strats
        except Exception:
            continue
    return coverage


def _scan_relative(base_dir: str = "results/relative") -> dict:
    """Scan relative results and return {(method, dataset, model, ratio): n_seeds}."""
    base = Path(base_dir)
    coverage = {}
    if not base.exists():
        return coverage
    for fpath in base.rglob("relative_*.json"):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = data.get("config", {})
            key = (
                cfg.get("unlearning_methods", ""),
                cfg.get("dataset_name", ""),
                cfg.get("base_model", ""),
                round(float(cfg.get("unlearn_ratio", 0.05)), 4),
            )
            n_results = len(data.get("results", []))
            if n_results > 0:
                coverage[key] = coverage.get(key, 0) + 1
        except Exception:
            continue
    return coverage


def scan_eval_coverage() -> str:
    """Scan collateral and relative results, return formatted report."""
    collateral = _scan_collateral()
    relative = _scan_relative()

    lines = []
    lines.append("")
    lines.append("=" * 85)
    lines.append("Evaluation Coverage (Collateral / Relative)")
    lines.append("=" * 85)

    gaps = []
    ok_count = 0

    for phase_key in ["mg0", "mg1", "mg2", "mg3_citeseer", "mg3_gat", "ratio_sensitivity"]:
        cfg = EVAL_EXPECTED.get(phase_key)
        if not cfg:
            continue
        for method in cfg["methods"]:
            for ratio in cfg["ratios"]:
                key = (method, cfg["dataset"], cfg["model"], ratio)

                coll_strats = collateral.get(key, set())
                # Filter to only v4 strategies for checking
                has_collateral = len(coll_strats) > 0
                rel_count = relative.get(key, 0)
                has_relative = rel_count > 0

                if has_collateral and has_relative:
                    ok_count += 1
                else:
                    status_parts = []
                    if not has_collateral:
                        if coll_strats is not None and len(coll_strats) == 0 and key in collateral:
                            status_parts.append("collateral=empty(0 strategies)")
                        else:
                            status_parts.append("collateral=MISSING")
                    if not has_relative:
                        status_parts.append("relative=MISSING")
                    label = PHASE_CONFIGS.get(phase_key, PhaseConfig(phase_key, "", [], "", "", [], [])).name
                    ratio_str = f"r={ratio}" if ratio != 0.05 else "r=0.05"
                    gaps.append(f"  {label:<16} {method:>12}/{cfg['dataset']:>10}/{cfg['model']:>4}/{ratio_str:<8}  {', '.join(status_parts)}")

    if gaps:
        lines.append(f"\n  Gaps ({len(gaps)}):")
        lines.extend(gaps)
    else:
        lines.append("\n  All evaluations complete!")

    lines.append(f"\n  Summary: {ok_count} complete, {len(gaps)} missing/incomplete")
    lines.append("=" * 85)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Check experiment progress against checklist',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                           # Show all phases progress
    %(prog)s --phase mg0               # Show only MG-0 progress
    %(prog)s --method GIF              # Filter by method
    %(prog)s --detail                  # Show detailed missing experiments
    %(prog)s --fill --dry-run          # Preview auto_discovered.json updates
    %(prog)s --fill --yes              # Log to auto_discovered.json
        """
    )
    parser.add_argument('--phase', type=str, choices=['mg0', 'mg1', 'mg2', 'mg3', 'ratio'],
                       help='Show only specific phase')
    parser.add_argument('--method', type=str,
                       help='Filter by unlearning method')
    parser.add_argument('--dataset', type=str,
                       help='Filter by dataset')
    parser.add_argument('--detail', action='store_true',
                       help='Show detailed missing experiments')
    parser.add_argument('--fill', action='store_true',
                       help='Log discovered experiments to auto_discovered.json (does not modify checklist)')
    parser.add_argument('--yes', action='store_true',
                       help='Auto-confirm fill operation (no interactive prompt)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without writing')
    parser.add_argument('--checklist', type=str,
                       default='self/generalization_experiment_checklist.md',
                       help='Path to checklist file')
    parser.add_argument('--results-dir', type=str,
                       default='results/experiments',
                       help='Base directory for results')

    args = parser.parse_args()

    # Parse checklist and scan actual results
    print(f"Loading checklist: {args.checklist}")
    expected = parse_checklist(args.checklist)

    # Also load auto-discovered experiments from JSON
    auto_discovered_path = get_auto_discovered_path()
    if os.path.exists(auto_discovered_path):
        print(f"Loading auto-discovered: {auto_discovered_path}")
        auto_expected = load_auto_discovered(auto_discovered_path)
        # Merge with expected (auto takes precedence for duplicates)
        for phase, keys in auto_expected.items():
            if phase not in expected:
                expected[phase] = []
            for key in keys:
                if key not in expected[phase]:
                    expected[phase].append(key)

    print(f"Scanning results: {args.results_dir}")
    official, legacy = scan_actual_results(args.results_dir)

    # Compute progress
    reports = compute_progress(expected, official, legacy)

    # Filter by phase if specified
    if args.phase:
        phase_map = {
            'mg0': ['mg0'],
            'mg1': ['mg1'],
            'mg2': ['mg2'],
            'mg3': ['mg3_citeseer', 'mg3_gat'],
            'ratio': ['ratio_sensitivity']
        }
        valid_phases = phase_map.get(args.phase, [args.phase])
        reports = {k: v for k, v in reports.items() if k in valid_phases}

    # Print progress table
    print("\n" + format_progress_table(reports))

    # Print evaluation coverage
    print(scan_eval_coverage())

    # Detailed output
    if args.detail or args.fill:
        gaps = analyze_gaps(expected, official, legacy)

        if args.detail:
            print(format_detail_output(reports, gaps, args.phase))

        # Fill mode
        if args.fill:
            print("\n" + "=" * 70)
            print("CHECKLIST GAP ANALYSIS")
            print("=" * 70)

            if gaps.missing:
                print(f"\n[Missing in checklist - found {len(gaps.missing)} official experiments]")
                for key in sorted(list(gaps.missing))[:5]:
                    print(f"  - {key}")
                if len(gaps.missing) > 5:
                    print(f"  ... and {len(gaps.missing) - 5} more")

            if gaps.extra:
                print(f"\n[Extra in checklist - not found {len(gaps.extra)} experiments]")
                for key in sorted(list(gaps.extra))[:5]:
                    print(f"  - {key}")
                if len(gaps.extra) > 5:
                    print(f"  ... and {len(gaps.extra) - 5} more")

            # Show legacy experiments count
            total_legacy = sum(1 for k in legacy)
            if total_legacy > 0:
                print(f"\n[Legacy experiments (cache only) - {total_legacy} found]")
                print("  (im/hybrid old versions kept as cache, not counted in checklist)")

            # Update auto_discovered.json AND checklist.md
            if not args.dry_run and not args.yes:
                response = input("\nLog to auto_discovered.json and update checklist? [y/N]: ").strip().lower()
                if response != 'y':
                    print("Aborted.")
                    return

            # Step 1: Write to auto_discovered.json
            success, message = log_auto_discovered(gaps, dry_run=args.dry_run)
            print(f"\n[1/2] {message}")

            if not success:
                sys.exit(1)

            # Step 2: Update checklist.md status
            success2, message2 = update_checklist_status(args.checklist, dry_run=args.dry_run)
            print(f"[2/2] {message2}")

            if not success2:
                sys.exit(1)


if __name__ == '__main__':
    main()
