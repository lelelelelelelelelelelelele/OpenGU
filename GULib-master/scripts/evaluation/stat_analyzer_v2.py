import os
import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
from exp_status_checker import aggregate_metrics, PHASE_CONFIGS, scan_actual_results, parse_checklist

def compute_detailed_stats(phase_key):
    """
    Extends exp_status_checker logic to include p-values and raw arrays.
    """
    phase_config = PHASE_CONFIGS.get(phase_key)
    if not phase_config:
        return None

    # Use existing scanner logic to find all JSONs
    base_path = Path('results/experiments')
    phase_dir = base_path / phase_config.dir_name / "phase_a"
    if not phase_dir.exists():
        return None

    # Data structure: {method: {strategy: {metric: [values_per_seed]}}}
    raw_data = {}
    
    for seed_dir in phase_dir.iterdir():
        if not seed_dir.is_dir(): continue
        summary_file = seed_dir / "_summary.json"
        if not summary_file.exists(): continue
        
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            results = data.get('results', {})
            for m_key, m_data in results.items():
                method = m_key.split('_')[0]
                if method not in phase_config.methods: continue
                
                if method not in raw_data: raw_data[method] = {}
                
                strat_results = m_data.get('results', {})
                for strategy, s_data in strat_results.items():
                    if strategy == 'comparison' or not strategy: continue
                    if strategy not in raw_data[method]: raw_data[method][strategy] = {'f1_drop': [], 'mia_auc': []}
                    
                    if s_data.get('f1_drop') is not None:
                        raw_data[method][strategy]['f1_drop'].append(s_data['f1_drop'])
                    if s_data.get('mia_auc') is not None:
                        raw_data[method][strategy]['mia_auc'].append(s_data['mia_auc'])
        except: continue

    # Calculate statistics and p-values vs random
    rows = []
    for method, strats in raw_data.items():
        random_vals = strats.get('random', {}).get('f1_drop', [])
        
        for strategy, metrics in strats.items():
            f1_vals = metrics.get('f1_drop', [])
            if not f1_vals: continue
            
            mean_f1 = np.mean(f1_vals) * 100
            std_f1 = np.std(f1_vals) * 100
            
            # T-test vs Random
            p_val = 1.0
            if strategy != 'random' and len(random_vals) == len(f1_vals) and len(f1_vals) > 1:
                _, p_val = stats.ttest_rel(f1_vals, random_vals)
            
            rows.append({
                'Phase': phase_key,
                'Method': method,
                'Strategy': strategy,
                'F1_Drop_Mean': mean_f1,
                'F1_Drop_Std': std_f1,
                'P_Value_vs_Random': p_val,
                'N_Seeds': len(f1_vals),
                'MIA_AUC_Mean': np.mean(metrics.get('mia_auc', [0])) if metrics.get('mia_auc') else 0
            })
            
    return pd.DataFrame(rows)

def main():
    output_dir = Path("results/evaluation/stats")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_dfs = []
    for phase in PHASE_CONFIGS.keys():
        print(f"Processing {phase}...")
        df = compute_detailed_stats(phase)
        if df is not None and not df.empty:
            df.to_csv(output_dir / f"{phase}_stats.csv", index=False)
            all_dfs.append(df)
            
    if all_dfs:
        full_df = pd.concat(all_dfs)
        full_df.to_csv(output_dir / "all_phases_stats.csv", index=False)
        print(f"\nSuccess! Stats saved to {output_dir}")
        
        # Simple report
        print("\nSignificant Findings (p < 0.05 vs Random):")
        sig = full_df[full_df['P_Value_vs_Random'] < 0.05]
        if not sig.empty:
            print(sig[['Phase', 'Method', 'Strategy', 'F1_Drop_Mean', 'P_Value_vs_Random']])
        else:
            print("No statistically significant differences found yet.")

if __name__ == "__main__":
    main()
