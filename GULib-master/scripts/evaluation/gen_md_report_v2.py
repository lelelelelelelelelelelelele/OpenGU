import pandas as pd
import numpy as np
from pathlib import Path

def generate_md_report(csv_path, output_md_path):
    df = pd.read_csv(csv_path)
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write("# Final Cross-Seed Statistical Results (Purified Metrics)\n\n")
        f.write("> **Data Source**: `results/evaluation/stats/final_paper_stats.csv`\n\n")
        f.write("> **Metric Format**: **Rel_F1_Drop** (Retrain_Gap)\n\n")
        f.write("> **Relative F1 Drop (%)** = [k=5 Baseline F1] - [Attack F1]\n\n")
        f.write("> **Retrain Gap (%)** = |Unlearn F1 - Retrain F1| (Mimicry Quality)\n\n")
        f.write("> **Significance**: * p < 0.05, ** p < 0.01 (One-sample T-test vs 0)\n\n")
        
        # Group by Dataset, Model, and Ratio to avoid duplicates
        settings = df.groupby(['Dataset', 'Model', 'Ratio'])
        for (dataset, model, ratio), group in settings:
            f.write(f"## Setting: {dataset.upper()} / {model} (Ratio: {ratio})\n\n")
            def format_cell(row):
                sig = ""
                if row['P_Value'] < 0.01: sig = "**"
                elif row['P_Value'] < 0.05: sig = "*"
                drop = f"{row['Rel_F1_Drop_Mean']:.2f}{sig}"
                gap = f"{row['Retrain_Gap_Abs_Mean']:.2f}" if row['Retrain_Gap_Abs_Mean'] > 0 else "-"
                return f"{drop} ({gap})"
            group_copy = group.copy()
            group_copy['Display'] = group_copy.apply(format_cell, axis=1)
            table = group_copy.pivot(index='Method', columns='Strategy', values='Display')
            cols = list(table.columns)
            primary = ['random', 'tracin', 'im_v4', 'hybrid_v4']
            ordered_cols = [c for c in primary if c in cols] + [c for c in cols if c not in primary]
            table = table[ordered_cols]
            f.write("| Method | " + " | ".join(ordered_cols) + " |\n")
            f.write("| :--- | " + " | ".join(["---:"] * len(ordered_cols)) + " |\n")
            for method, row in table.iterrows():
                f.write(f"| {method} | " + " | ".join([str(v) if pd.notna(v) else "-" for v in row]) + " |\n")
            f.write("\n\n")

if __name__ == "__main__":
    generate_md_report('results/evaluation/stats/final_paper_stats.csv', 'report/paper/sections/cross_seed_tables.md')
