"""Pre-Phase-B paper-stats aggregator. NEEDS REWRITE before Phase B use.

Reads from `results/relative/`, `results/collateral/`, `results/experiments/`
— all three were declared bug-polluted on 2026-05-05 and are now gitignored.
On a fresh checkout these dirs are empty, and on legacy machines they hold
data from runs that have since been audited as wrong (see
self/dashboard/EXPERIMENT_DASHBOARD.md §3.6 for the 8 attack-pipeline bugs
fixed 2026-05-06 that invalidate everything written before that date).

Phase B output lives at:
    results/runs/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{N}/
        {attack.json, collateral.json, predictions.npz, _meta.json}

A Phase B port should walk that tree, not the three legacy ones below.
Until rewritten, running this script will silently produce empty/stale CSVs.
Guard added 2026-05-06.
"""
import os
import sys
import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import re

if __name__ == "__main__" and not os.environ.get("ALLOW_LEGACY_AGGREGATOR"):
    sys.stderr.write(
        "[final_data_aggregator] refusing to run: reads pre-Phase-B dirs that\n"
        "are now gitignored as bug-polluted. Set ALLOW_LEGACY_AGGREGATOR=1 to\n"
        "force-run on a machine that still has the legacy data, or rewrite\n"
        "this aggregator to walk results/runs/{cell}/{method_strategy}/seed*/.\n"
    )
    sys.exit(2)

def extract_seed_from_filename(filename):
    match = re.search(r'seed(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def aggregate_all_metrics():
    # 1. Load Relative F1 Drop
    rel_data = []
    rel_path = Path("results/relative")
    if rel_path.exists():
        for root, dirs, files in os.walk(rel_path):
            for file in files:
                if file.endswith(".json") and "relative" in file:
                    f_path = Path(root) / file
                    try:
                        with open(f_path, 'r', encoding='utf-8') as f_in:
                            data = json.load(f_in)
                        cfg = data.get('config', {})
                        # In relative JSONs, seed might be in config or results entry
                        cfg_seed = cfg.get('random_seed')
                        for entry in data.get('results', []):
                            s = entry.get('seed') or cfg_seed or extract_seed_from_filename(file)
                            if s is None: continue
                            rel_data.append({
                                'Method': str(cfg.get('unlearning_methods')),
                                'Dataset': str(cfg.get('dataset_name')).lower(),
                                'Model': str(cfg.get('base_model')).upper(),
                                'Ratio': str(cfg.get('unlearn_ratio')),
                                'Seed': int(s),
                                'Strategy': str(entry.get('strategy')).lower(),
                                'Rel_F1_Drop': entry.get('relative_f1_drop'),
                                'Baseline_K5_F1': entry.get('baseline_f1_after')
                            })
                    except: continue
    print(f"Found {len(rel_data)} relative entries.")

    # 2. Load Collateral Damage (Retrain Gap)
    col_data = []
    col_path = Path("results/collateral")
    if col_path.exists():
        for root, dirs, files in os.walk(col_path):
            for file in files:
                if file.endswith(".json") and "collateral" in file:
                    f_path = Path(root) / file
                    try:
                        with open(f_path, 'r', encoding='utf-8') as f_in:
                            data = json.load(f_in)
                        cfg = data.get('config', {})
                        # Seed is in config.random_seed for collateral files
                        cfg_seed = cfg.get('random_seed') or extract_seed_from_filename(file)
                        for entry in data.get('results', []):
                            s = entry.get('seed') or cfg_seed
                            if s is None: continue
                            
                            # Note: collateral files might use 'im' instead of 'im_v4'
                            # We normalize to im_v4/hybrid_v4 if they match
                            strat = str(entry.get('strategy')).lower()
                            if strat == 'im': strat = 'im_v4'
                            if strat == 'hybrid': strat = 'hybrid_v4'

                            col_data.append({
                                'Method': str(cfg.get('unlearning_methods')),
                                'Dataset': str(cfg.get('dataset_name')).lower(),
                                'Model': str(cfg.get('base_model')).upper(),
                                'Ratio': str(cfg.get('unlearn_ratio')),
                                'Seed': int(s),
                                'Strategy': strat,
                                'Retrain_Gap': entry.get('gap'), # Note: in collateral JSON, gap is the field name
                                'Utility_Drop': entry.get('collateral_damage', {}).get('utility_drop')
                            })
                    except: continue
    print(f"Found {len(col_data)} collateral entries.")

    # 3. Load Raw Experiments (MIA/Time)
    raw_data = []
    exp_path = Path("results/experiments")
    if exp_path.exists():
        for root, dirs, files in os.walk(exp_path):
            if "_summary.json" in files:
                f_path = Path(root) / "_summary.json"
                file_seed = extract_seed_from_filename(f_path.parent.name)
                try:
                    with open(f_path, 'r', encoding='utf-8') as f_in:
                        data = json.load(f_in)
                    cfg = data.get('config', {})
                    results = data.get('results', {})
                    for m_key, m_data in results.items():
                        method = m_key.split('_')[0]
                        strat_results = m_data.get('results', {})
                        for strategy, s_data in strat_results.items():
                            if strategy == 'comparison' or not strategy: continue
                            
                            ratio = cfg.get('unlearn_ratio', 0.05)
                            if isinstance(ratio, list): ratio = ratio[0]
                            
                            raw_data.append({
                                'Method': str(method),
                                'Dataset': str(cfg.get('dataset_name')).lower(),
                                'Model': str(cfg.get('base_model')).upper(),
                                'Ratio': str(ratio),
                                'Seed': int(file_seed) if file_seed else 2024,
                                'Strategy': str(strategy).lower(),
                                'MIA_AUC': s_data.get('mia_auc'),
                                'Time': s_data.get('selection_time')
                            })
                except: continue
    print(f"Found {len(raw_data)} raw experimental entries.")

    df_rel = pd.DataFrame(rel_data)
    df_col = pd.DataFrame(col_data)
    df_exp = pd.DataFrame(raw_data)

    if df_rel.empty:
        print("Error: No relative data found.")
        return None

    # Merge
    final_df = df_rel
    if not df_col.empty:
        # Note: we might have multiple collateral files for same config due to repairs
        # Keep the latest or most complete? For now, drop duplicates.
        df_col = df_col.drop_duplicates(subset=['Method', 'Dataset', 'Model', 'Ratio', 'Seed', 'Strategy'])
        final_df = pd.merge(final_df, df_col, on=['Method', 'Dataset', 'Model', 'Ratio', 'Seed', 'Strategy'], how='left')
    if not df_exp.empty:
        df_exp = df_exp.drop_duplicates(subset=['Method', 'Dataset', 'Model', 'Ratio', 'Seed', 'Strategy'])
        final_df = pd.merge(final_df, df_exp, on=['Method', 'Dataset', 'Model', 'Ratio', 'Seed', 'Strategy'], how='left')

    # Aggregation
    group_cols = ['Method', 'Dataset', 'Model', 'Ratio', 'Strategy']
    stats_rows = []
    for name, group in final_df.groupby(group_cols):
        vals = group['Rel_F1_Drop'].dropna().values
        p_val = 1.0
        if len(vals) > 1:
            _, p_val = stats.ttest_1samp(vals, 0)
        
        # Calculate Gap metrics (convert to absolute for mimicry quality check)
        gap_mean = group['Retrain_Gap'].abs().mean() * 100 if 'Retrain_Gap' in group.columns else 0
        
        stats_rows.append({
            'Method': name[0], 'Dataset': name[1], 'Model': name[2], 'Ratio': name[3], 'Strategy': name[4],
            'Rel_F1_Drop_Mean': np.mean(vals) * 100 if len(vals)>0 else 0,
            'Rel_F1_Drop_Std': np.std(vals) * 100 if len(vals)>0 else 0,
            'Retrain_Gap_Abs_Mean': gap_mean,
            'MIA_AUC_Mean': group['MIA_AUC'].mean() if 'MIA_AUC' in group.columns else 0,
            'P_Value': p_val, 'N_Seeds': len(vals)
        })

    return pd.DataFrame(stats_rows)

if __name__ == "__main__":
    out_dir = Path("results/evaluation/stats")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = aggregate_all_metrics()
    if df is not None:
        df.to_csv(out_dir / "final_paper_stats.csv", index=False)
        print(f"Final paper stats saved to {out_dir / 'final_paper_stats.csv'}")
        
        # Check high-potency points for FIG-5
        print("\n--- High Mimicry Potential (Low Gap, High Drop) ---")
        best = df[df['Rel_F1_Drop_Mean'] > 2.0].sort_values('Retrain_Gap_Abs_Mean')
        if not best.empty:
            print(best[['Method', 'Dataset', 'Strategy', 'Rel_F1_Drop_Mean', 'Retrain_Gap_Abs_Mean']].head(10))
