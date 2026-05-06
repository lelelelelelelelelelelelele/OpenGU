"""
exp_status_checker.py - Check experiment progress against checklist with sanity checks.

Upgraded: 2026-02-27
- Added strict seed counting (N=5)
- Added quality filtering (detects silent fallbacks/identical F1)

⚠ 2026-05-06: STALE for Phase B. Walks `results/relative/`,
`results/collateral/`, `results/experiments/` — all three are gitignored
post-2026-05-05 as bug-polluted, so this checker will report 0 progress
on a fresh checkout. For Phase B progress use `scripts/gate_runs.py
results/runs/<cell>` instead, which is the canonical pass/fail gate
(4 files + mia_auc + f1 range).
"""
import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from dataclasses import dataclass, asdict

# Constants for detection
RANDOM_GUESS = {'citeseer': 0.18, 'cora': 0.30, 'pubmed': 0.40}

class ExperimentKey(NamedTuple):
    phase: str
    method: str
    dataset: str
    model: str
    seed: int
    strategy: str
    ratio: float = 0.05

    def __str__(self):
        return f"{self.phase}:{self.method}/{self.dataset}/{self.model}/seed={self.seed}/{self.strategy}/r{self.ratio}"

@dataclass
class PhaseConfig:
    name: str
    dir_name: str
    methods: List[str]
    dataset: str
    model: str
    seeds: List[int]
    strategies: List[str]
    legacy_strategies: List[str] = None
    ratios: List[str] = None

    @property
    def total_runs(self) -> int:
        num_ratios = len(self.ratios) if self.ratios else 1
        ds_list = self.dataset.split(',')
        md_list = self.model.split(',')
        return len(self.methods) * len(ds_list) * len(md_list) * len(self.seeds) * len(self.strategies) * num_ratios

PHASE_CONFIGS = {
    "mg0": PhaseConfig("MG-0", "mg0_completion", ["GIF", "GNNDelete", "GraphEraser"], "cora", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg1": PhaseConfig("MG-1", "mg1_citeseer", ["GIF", "GNNDelete", "GraphEraser"], "citeseer", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg2": PhaseConfig("MG-2", "mg2_gat", ["GIF", "GNNDelete", "GraphEraser"], "cora", "GAT", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg3_citeseer": PhaseConfig("MG-3-Citeseer", "mg3_citeseer", ["IDEA", "MEGU"], "citeseer", "GCN", [42, 212, 722, 1337, 2024], ["random", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg3_gat": PhaseConfig("MG-3-GAT", "mg3_gat", ["IDEA", "MEGU"], "cora", "GAT", [42, 212, 722, 1337, 2024], ["random", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "ratio_sensitivity": PhaseConfig("P2-Ratio", "ratio_sensitivity", ["GIF", "GNNDelete"], "cora", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ratios=["0.01", "0.05", "0.10", "0.20"]),
    "p2_ext": PhaseConfig("P2-EXT", "p2_ext_gif", ["GIF"], "cora,citeseer", "GCN,GAT,GIN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ratios=["0.10", "0.20"])
}

def check_f1_quality(results_dict, dataset_name):
    """
    Quality filter: Returns False if result shows signs of silent fallback.
    """
    f1_afters = []
    for s, s_data in results_dict.items():
        if s == 'comparison' or not s: continue
        f1 = s_data.get('f1_after')
        if f1 is not None: f1_afters.append(round(f1, 4))
    
    if not f1_afters: return True
    
    # Sign 1: Strategy Invariance (Fallback)
    if len(f1_afters) > 1 and len(set(f1_afters)) == 1:
        # Special case: if F1 is extremely high, it might be legit (but unlikely for attack)
        if f1_afters[0] < 0.80: return False
        
    # Sign 2: Zero Delta
    for s, s_data in results_dict.items():
        if s == 'comparison': continue
        b = s_data.get('f1_before'); a = s_data.get('f1_after')
        if b and a and abs(a - b) < 1e-7: return False
        
    return True

def scan_actual_results(base_dir: str) -> Tuple[Set[ExperimentKey], Set[ExperimentKey]]:
    official_found = set()
    legacy_found = set()
    base_path = Path(base_dir)
    if not base_path.exists(): return official_found, legacy_found

    for exp_dir in base_path.iterdir():
        if not exp_dir.is_dir(): continue
        phase_dir = exp_dir / "phase_a"
        if not phase_dir.exists(): continue

        for seed_dir in phase_dir.iterdir():
            if not seed_dir.is_dir(): continue
            seed_match = re.search(r'seed(\d+)', seed_dir.name)
            if not seed_match: continue
            seed = int(seed_match.group(1))
            
            summary_file = seed_dir / "_summary.json"
            if not summary_file.exists(): continue

            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                results = data.get('results', {})
                dataset_name = data.get('config', {}).get('dataset_name', '').lower()
                
                for m_key, m_data in results.items():
                    # Quality Check
                    if not check_f1_quality(m_data.get('results', {}), dataset_name):
                        continue

                    parts = m_key.split('_')
                    if len(parts) >= 3:
                        method, ds, model = parts[0], parts[1].lower(), parts[2].upper()
                        ratio_list = [float(p[1:]) for p in parts[3:] if p.startswith('r')] or [0.05]
                        
                        for strategy in m_data.get('results', {}).keys():
                            if not strategy or strategy == 'comparison': continue
                            for ratio in ratio_list:
                                key = ExperimentKey(exp_dir.name, method, ds, model, seed, strategy.lower(), ratio)
                                official_found.add(key)
            except: continue
    return official_found, legacy_found

def scan_eval_coverage(args=None):
    """
    Upgraded Coverage: Requires all 5 seeds to be present for 'complete'.
    """
    show_all = args.show_all if args and hasattr(args, 'show_all') else False

    # 1. Scan relative
    rel_coverage = defaultdict(set)
    rel_path = Path("results/relative")
    if rel_path.exists():
        for f in rel_path.rglob("relative_*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in:
                    data = json.load(f_in)
                    # Skip files with empty results
                    if not data.get('results'):
                        continue
                    cfg = data.get('config', {})
                    key = (cfg.get('unlearning_methods'), cfg.get('dataset_name'), cfg.get('base_model'), float(cfg.get('unlearn_ratio', 0.05)))

                    # Store unique seeds
                    seed = cfg.get('random_seed', cfg.get('seed'))
                    if seed is not None:
                        rel_coverage[key].add(int(seed))
            except: continue

    # 2. Scan collateral
    col_coverage = defaultdict(set)
    col_path = Path("results/collateral")
    if col_path.exists():
        for f in col_path.rglob("collateral_*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in:
                    data = json.load(f_in)
                    results = data.get('results', [])
                    # Skip files with empty results
                    if not results:
                        continue
                    cfg = data.get('config', {})
                    key = (cfg.get('unlearning_methods'), cfg.get('dataset_name'), cfg.get('base_model'), float(cfg.get('unlearn_ratio', 0.05)))

                    # Priority 1: Config seed
                    root_seed = cfg.get('random_seed', cfg.get('seed'))
                    if root_seed is not None:
                        col_coverage[key].add(int(root_seed))

                    # Priority 2: Per-result seeds (merged storage mode)
                    for res in results:
                        if 'seed' in res:
                            col_coverage[key].add(int(res['seed']))
            except: continue

    print("\n" + "="*85)
    print(f"{'Configuration':<50} | {'Rel (Seeds)':<12} | {'Col (Seeds)':<12}")
    print("-"*85)
    
    for phase_key, cfg in PHASE_CONFIGS.items():
        for m in cfg.methods:
            ds_list = cfg.dataset.split(',')
            md_list = cfg.model.split(',')
            ratios = [float(r) for r in cfg.ratios] if cfg.ratios else [0.05]
            for d in ds_list:
                for mod in md_list:
                    for r in ratios:
                        lookup_key = (m, d, mod, r)
                        r_cnt = len(rel_coverage.get(lookup_key, set()))
                        c_cnt = len(col_coverage.get(lookup_key, set()))
                        
                        r_status = f"{r_cnt}/5" if r_cnt < 5 else "5/5 OK"
                        c_status = f"{c_cnt}/5" if c_cnt < 5 else "5/5 OK"

                        if r_cnt < 5 or c_cnt < 5 or show_all:
                            label = f"{m}/{d}/{mod}/r{r}"
                            print(f"{label:<50} | {r_status:<12} | {c_status:<12}")
    print("="*85)

from collections import defaultdict
import glob

# Phase to checklist section mapping
PHASE_TO_SECTION = {
    "mg0": ("2.1", "MG-0 稳定性"),
    "mg1": ("2.2", "MG-1 最小跨数据集泛化"),
    "mg2": ("2.3", "MG-2 最小跨模型泛化"),
    "mg3_citeseer": ("2.4", "MG-3（可选）扩展到 5 方法"),
    "mg3_gat": ("2.4", "MG-3（可选）扩展到 5 方法"),
    "ratio_sensitivity": ("2.6", "Ratio 敏感性（攻击强度曲线）"),
    "p2_ext": ("P2-EXT", "P2-EXT 扩展实验"),
}


def load_checklist() -> dict:
    """Parse checklist and extract completion status for each phase."""
    checklist_path = Path("self/generalization_experiment_checklist.md")
    if not checklist_path.exists():
        return {}

    content = checklist_path.read_text(encoding='utf-8')
    status = {}

    # Extract phase completion status from markdown (using Chinese brackets)
    phase_patterns = [
        (r'- \[x\] `Cora / GCN / ratio=0\.05 / 5 seeds`.*?（auto_discovered: (\d+) runs）', 'mg0'),
        (r'- \[x\] `Citeseer / GCN / ratio=0\.05 / 5 seeds`.*?（auto_discovered: (\d+) runs）', 'mg1'),
        (r'- \[x\] `Cora / GAT / ratio=0\.05 / 5 seeds`.*?（auto_discovered: (\d+) runs）', 'mg2'),
    ]

    for pattern, phase_key in phase_patterns:
        match = re.search(pattern, content)
        if match:
            status[phase_key] = {
                'marked': True,
                'runs': int(match.group(1)) if match.group(1) else 0
            }
        else:
            status[phase_key] = {'marked': False, 'runs': 0}

    # Check for ratio sensitivity (using Chinese brackets)
    if re.search(r'- \[x\] `Cora / GCN / GIF / ratio=0\.01,0\.05,0\.10,0\.20 / 5 seeds`', content):
        match = re.search(r'- \[x\] `Cora / GCN / GIF / ratio=0\.01,0\.05,0\.10,0\.20 / 5 seeds`.*?（auto_discovered: (\d+) runs）', content)
        if match:
            status['ratio_sensitivity'] = {'marked': True, 'runs': int(match.group(1))}
    else:
        status['ratio_sensitivity'] = {'marked': False, 'runs': 0}

    return status


def get_discovered_runs() -> Tuple[Set[ExperimentKey], dict]:
    """Load all discovered experiments from results/experiments/."""
    official_found = set()
    source_counts = {}

    base_path = Path("results/experiments")
    if not base_path.exists():
        return official_found, source_counts

    # Skip non-experiment directories
    skip_dirs = {'_archive', '_tmp', '_tmp_timeout_test', 'auto_discovered.json'}

    for exp_dir in base_path.iterdir():
        if not exp_dir.is_dir():
            continue
        if exp_dir.name.startswith('_'):
            continue
        if exp_dir.name in skip_dirs:
            continue

        # Determine phase key from directory name
        dir_name = exp_dir.name
        phase_key = dir_name.replace("mg0_completion", "mg0")
        phase_key = phase_key.replace("mg1_citeseer", "mg1")
        phase_key = phase_key.replace("mg2_gat", "mg2")
        phase_key = phase_key.replace("mg3_citeseer", "mg3_citeseer")
        phase_key = phase_key.replace("mg3_gat", "mg3_gat")
        phase_key = phase_key.replace("ratio_sensitivity", "ratio_sensitivity")
        phase_key = phase_key.replace("p2_ext_gif", "p2_ext")

        phase_dir = exp_dir / "phase_a"
        if not phase_dir.exists():
            continue

        count = 0
        for seed_dir in phase_dir.iterdir():
            if not seed_dir.is_dir():
                continue
            seed_match = re.search(r'seed(\d+)', seed_dir.name)
            if not seed_match:
                continue
            seed = int(seed_match.group(1))

            summary_file = seed_dir / "_summary.json"
            if not summary_file.exists():
                continue

            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                results = data.get('results', {})
                dataset_name = data.get('config', {}).get('dataset_name', '').lower()

                for m_key, m_data in results.items():
                    if not check_f1_quality(m_data.get('results', {}), dataset_name):
                        continue

                    parts = m_key.split('_')
                    if len(parts) >= 3:
                        method, ds, model = parts[0], parts[1].lower(), parts[2].upper()
                        ratio_list = [float(p[1:]) for p in parts[3:] if p.startswith('r')] or [0.05]

                        for strategy in m_data.get('results', {}).keys():
                            if not strategy or strategy == 'comparison':
                                continue
                            # Filter: only count v4 strategies (official)
                            if strategy in ['im', 'hybrid']:  # Legacy strategies
                                continue
                            for ratio in ratio_list:
                                key = ExperimentKey(phase_key, method, ds, model, seed, strategy.lower(), ratio)
                                official_found.add(key)
                                count += 1
            except:
                continue

        source_counts[phase_key] = count

    return official_found, source_counts


def analyze_gaps(official_found: Set[ExperimentKey]) -> dict:
    """Analyze gaps between discovered experiments and checklist."""
    gaps = {}

    for pk, pcfg in PHASE_CONFIGS.items():
        phase_keys = [k for k in official_found if k.phase.startswith(pk) or (pk.startswith(k.phase) and pk != 'p2_ext')]
        discovered_seeds = set(k.seed for k in phase_keys)

        gaps[pk] = {
            'total_expected': pcfg.total_runs,
            'discovered': len(phase_keys),
            'seeds_found': len(discovered_seeds),
            'expected_seeds': len(pcfg.seeds),
        }

    return gaps


def handle_fill_mode(args):
    """Handle --fill mode: scan, report gaps, write auto_discovered.json (no checklist modification)."""
    print("=" * 70)
    print("CHECKLIST GAP ANALYSIS")
    print("=" * 70)

    # Step 1: Get discovered experiments
    official_found, source_counts = get_discovered_runs()
    total_discovered = sum(source_counts.values())

    print(f"\n[Discovered experiments - {total_discovered} runs]")
    for phase, count in sorted(source_counts.items()):
        print(f"  - {phase}: {count} runs")

    # Step 2: Load checklist status
    checklist_status = load_checklist()

    print(f"\n[Current checklist status]")
    for phase in ['mg0', 'mg1', 'mg2', 'ratio_sensitivity']:
        info = checklist_status.get(phase, {'marked': False, 'runs': 0})
        status = "[x]" if info['marked'] else "[ ]"
        print(f"  - {phase}: {status} ({info['runs']} runs recorded)")

    # Step 3: Analyze gaps
    gaps = analyze_gaps(official_found)

    print(f"\n[Gap Analysis]")
    updates_needed = []
    for pk in ['mg0', 'mg1', 'mg2', 'ratio_sensitivity', 'p2_ext']:
        discovered = source_counts.get(pk, 0)
        recorded = checklist_status.get(pk, {}).get('runs', 0)
        is_marked = checklist_status.get(pk, {}).get('marked', False)

        if discovered > 0 and not is_marked:
            print(f"  - {pk}: discovered {discovered}, NOT marked in checklist")
            updates_needed.append(pk)
        elif discovered > 0 and is_marked:
            if recorded != discovered:
                print(f"  - {pk}: discovered {discovered}, recorded {recorded} (MISMATCH!)")
                updates_needed.append(pk)
            else:
                print(f"  - {pk}: discovered {discovered}, matches recorded")

    print(f"\n[Proposed checklist updates]")
    final_updates = []
    for pk in updates_needed:
        section_id, section_name = PHASE_TO_SECTION.get(pk, (pk, pk))
        discovered = source_counts.get(pk, 0)
        recorded = checklist_status.get(pk, {}).get('runs', 0)

        # Only update if discovered >= recorded, or if currently unmarked
        if discovered >= recorded:
            print(f"  - {section_name}: would update to {discovered} runs")
            final_updates.append((pk, discovered))
        else:
            print(f"  - {section_name}: WARNING - discovered {discovered} < recorded {recorded}, SKIPPING")

    updates_needed = [pk for pk, _ in final_updates]

    # Enhanced MISMATCH details: show per-method breakdown
    if updates_needed:
        print(f"\n[MISMATCH Details]")
        for pk, discovered_count in final_updates:
            recorded = checklist_status.get(pk, {}).get('runs', 0)
            section_id, section_name = PHASE_TO_SECTION.get(pk, (pk, pk))

            # Per-method breakdown from discovered keys
            phase_keys = [k for k in official_found if k.phase == pk]
            method_counts = defaultdict(int)
            for k in phase_keys:
                method_counts[k.method] += 1

            pcfg = PHASE_CONFIGS.get(pk)
            if pcfg:
                expected_per_method = pcfg.total_runs // len(pcfg.methods) if pcfg.methods else 0
                missing_methods = []
                for m in pcfg.methods:
                    actual = method_counts.get(m, 0)
                    if actual < expected_per_method:
                        missing_methods.append(f"{m} ({actual}/{expected_per_method} runs)")
                if missing_methods:
                    print(f"  [MISMATCH] {pk}: discovered {discovered_count}, recorded {recorded}")
                    print(f"    -> 缺失 methods: {', '.join(missing_methods)}")
                    print(f"    -> 建议更新 checklist §{section_id}")
                else:
                    print(f"  [MISMATCH] {pk}: discovered {discovered_count}, recorded {recorded}")
                    print(f"    -> 建议更新 checklist §{section_id}")

    # If no updates needed, exit
    if not updates_needed:
        print("\n[INFO] Checklist is up to date!")

    # Write auto_discovered.json
    mismatches = []
    for pk, discovered_count in final_updates:
        recorded = checklist_status.get(pk, {}).get('runs', 0)
        mismatches.append({
            "phase": pk,
            "discovered": discovered_count,
            "recorded": recorded,
            "delta": discovered_count - recorded,
        })

    output = {
        "last_updated": datetime.now().isoformat(),
        "sources": source_counts,
        "total": total_discovered,
        "checklist_status": {k: v for k, v in checklist_status.items()},
        "mismatches": mismatches,
    }
    output_path = Path("results/experiments/auto_discovered.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n[SAVED] {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-dir', default='results/experiments')
    parser.add_argument('--phase', help='Filter by phase (mg0, mg1, mg2, mg3, ratio, p2_ext)')
    parser.add_argument('--method', help='Filter by method')
    parser.add_argument('--dataset', help='Filter by dataset')
    parser.add_argument('--detail', action='store_true', help='Show missing experiment details')
    parser.add_argument('--fill', action='store_true', help='Scan and report gaps, write auto_discovered.json (does NOT modify checklist)')
    parser.add_argument('--show_all', action='store_true', help='Show all configs in coverage table (not just missing ones)')
    args = parser.parse_args()

    if args.fill:
        return handle_fill_mode(args)

    print(f"Scanning results with Sanity Checks...")
    official, _ = scan_actual_results(args.results_dir)
    
    # Progress Summary
    print("\nExperiment Progress (Quality Verified):")
    for pk, pcfg in PHASE_CONFIGS.items():
        # Match phase by dir_name
        done = sum(1 for k in official if k.phase.startswith(pcfg.dir_name) or pcfg.dir_name.startswith(k.phase))
        total = pcfg.total_runs
        pct = (done/total*100) if total>0 else 0
        print(f"- {pcfg.name:<15}: {done}/{total} runs ({pct:.1f}%)")

    scan_eval_coverage(args)

if __name__ == '__main__':
    main()
