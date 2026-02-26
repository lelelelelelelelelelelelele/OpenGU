"""
exp_status_checker.py - Check experiment progress against checklist with sanity checks.

Upgraded: 2026-02-27
- Added strict seed counting (N=5)
- Added quality filtering (detects silent fallbacks/identical F1)
"""
import os
import re
import sys
import json
import shutil
import argparse
import numpy as np
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
    "mg0": PhaseConfig("MG-0", "mg0_completion", ["GIF", "GNNDelete", "GraphEraser", "GUIDE"], "cora", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg1": PhaseConfig("MG-1", "mg1_citeseer", ["GIF", "GNNDelete", "GraphEraser"], "citeseer", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg2": PhaseConfig("MG-2", "mg2_gat", ["GIF", "GNNDelete", "GraphEraser"], "cora", "GAT", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg3_citeseer": PhaseConfig("MG-3-Citeseer", "mg3_citeseer", ["IDEA", "MEGU"], "citeseer", "GCN", [42, 212, 722, 1337, 2024], ["random", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "mg3_gat": PhaseConfig("MG-3-GAT", "mg3_gat", ["IDEA", "MEGU"], "cora", "GAT", [42, 212, 722, 1337, 2024], ["random", "tracin", "im_v4", "hybrid_v4"], ["im", "hybrid"]),
    "ratio_sensitivity": PhaseConfig("P2-Ratio", "ratio_sensitivity", ["GIF", "GNNDelete"], "cora", "GCN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"]),
    "p2_ext": PhaseConfig("P2-EXT", "p2_ext_gif_GCN", ["GIF"], "cora,citeseer", "GCN,GAT,GIN", [42, 212, 722, 1337, 2024], ["random", "degree", "pagerank", "tracin", "im_v4", "hybrid_v4"], ratios=["0.10", "0.20"])
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

def scan_eval_coverage():
    """
    Upgraded Coverage: Requires all 5 seeds to be present for 'complete'.
    """
    # 1. Scan relative
    rel_coverage = defaultdict(int)
    rel_path = Path("results/relative")
    if rel_path.exists():
        for f in rel_path.rglob("relative_*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in:
                    cfg = json.load(f_in).get('config', {})
                    key = (cfg.get('unlearning_methods'), cfg.get('dataset_name'), cfg.get('base_model'), float(cfg.get('unlearn_ratio', 0.05)))
                    rel_coverage[key] += 1
            except: continue

    # 2. Scan collateral
    col_coverage = defaultdict(int)
    col_path = Path("results/collateral")
    if col_path.exists():
        for f in col_path.rglob("collateral_*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in:
                    cfg = json.load(f_in).get('config', {})
                    key = (cfg.get('unlearning_methods'), cfg.get('dataset_name'), cfg.get('base_model'), float(cfg.get('unlearn_ratio', 0.05)))
                    col_coverage[key] += 1
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
                        r_cnt = rel_coverage.get(lookup_key, 0)
                        c_cnt = col_coverage.get(lookup_key, 0)
                        
                        r_status = f"{r_cnt}/5" if r_cnt < 5 else "✅ 5/5"
                        c_status = f"{c_cnt}/5" if c_cnt < 5 else "✅ 5/5"
                        
                        if r_cnt < 5 or c_cnt < 5:
                            label = f"{m}/{d}/{mod}/r{r}"
                            print(f"{label:<50} | {r_status:<12} | {c_status:<12}")
    print("="*85)

from collections import defaultdict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-dir', default='results/experiments')
    args = parser.parse_args()

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

    scan_eval_coverage()

if __name__ == '__main__':
    main()
