import pandas as pd
import numpy as np
from pathlib import Path

def generate_md_report(csv_path, output_md_path):
    df = pd.read_csv(csv_path)
    
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write("# Cross-Seed Statistical Results Summary\n\n")
        f.write("> **Data Source**: `results/evaluation/stats/all_phases_stats.csv`\n\n")
        f.write("> **Metrics**: F1 Drop (%) ± Std, p-value vs Random (Paired T-test)\n\n")
        f.write("> **Significance**: * p < 0.05, ** p < 0.01\n\n")
        
        for phase in df['Phase'].unique():
            f.write(f"## Phase: {phase.upper()}\n\n")
            phase_df = df[df['Phase'] == phase].copy()
            
            # Format display strings
            def format_row(row):
                sig = ""
                if row['P_Value_vs_Random'] < 0.01: sig = "**"
                elif row['P_Value_vs_Random'] < 0.05: sig = "*"
                
                f1_str = f"{row['F1_Drop_Mean']:.2f} ± {row['F1_Drop_Std']:.2f}{sig}"
                return f1_str

            phase_df['F1_Drop_Display'] = phase_df.apply(format_row, axis=1)
            
            # Pivot for cleaner table: Method vs Strategy
            table = phase_df.pivot(index='Method', columns='Strategy', values='F1_Drop_Display')
            
            # Ensure random is first column if exists
            cols = list(table.columns)
            if 'random' in cols:
                cols.remove('random')
                cols = ['random'] + cols
            table = table[cols]
            
            # Manual Markdown table generation (since tabulate is missing)
            f.write("| Method | " + " | ".join(cols) + " |\n")
            f.write("| :--- | " + " | ".join(["---:"] * len(cols)) + " |\n")
            for method, row in table.iterrows():
                f.write(f"| {method} | " + " | ".join([str(v) if pd.notna(v) else "-" for v in row]) + " |\n")
            f.write("\n\n")

if __name__ == "__main__":
    generate_md_report('results/evaluation/stats/all_phases_stats.csv', 'report/paper/sections/cross_seed_tables.md')
