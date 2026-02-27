import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create output directory
os.makedirs('results/paper_figures', exist_ok=True)

# Load data
df = pd.read_csv('results/evaluation/stats/final_paper_stats.csv')

# --- FIG-1: Generalization Potency ---
def plot_fig1():
    # Filter for methods GIF, GNNDelete, GraphEraser, ratio=0.05
    methods = ['GIF', 'GNNDelete', 'GraphEraser']
    strategies = ['random', 'pagerank', 'degree', 'tracin', 'im_v4', 'hybrid_v4']
    
    df_f1 = df[(df['Method'].isin(methods)) & (df['Ratio'] == 0.05) & (df['Strategy'].isin(strategies))].copy()
    
    # Create combined setting column
    df_f1['Setting'] = df_f1['Dataset'] + '-' + df_f1['Model']
    
    # Needs to be restricted to (Cora, GCN), (Citeseer, GCN), (Cora, GAT)
    settings = ['cora-GCN', 'citeseer-GCN', 'cora-GAT']
    df_f1 = df_f1[df_f1['Setting'].isin(settings)]
    
    # We want grouped bar chart: x=Setting, hue=Strategy, y=Rel_F1_Drop_Mean, grid by Method
    g = sns.catplot(
        data=df_f1, kind="bar",
        x="Setting", y="Rel_F1_Drop_Mean", hue="Strategy", col="Method",
        errorbar=None, palette="viridis", height=5, aspect=1.2,
        hue_order=['random', 'degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4']
    )
    g.set_axis_labels("Dataset-Model", "Relative F1 Drop (%)")
    g.set_titles("{col_name}")
    g.fig.suptitle("FIG-1: Generalization Potency (Relative F1 Drop vs. Random k=5 Baseline)", y=1.05)
    plt.savefig('results/paper_figures/FIG-1_Generalization.pdf', bbox_inches='tight')
    plt.savefig('results/paper_figures/FIG-1_Generalization.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("FIG-1 generated.")

# --- FIG-2: Attack Scaling Efficiency ---
def plot_fig2():
    methods = ['GIF', 'GNNDelete']
    # Removed 'random' entirely as requested
    strategies = ['degree', 'pagerank', 'tracin', 'im_v4', 'hybrid_v4']
    
    df_f2 = df[(df['Method'].isin(methods)) & (df['Dataset'] == 'cora') & (df['Model'] == 'GCN') & (df['Strategy'].isin(strategies))].copy()
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    palette = sns.color_palette("muted", len(strategies))
    color_dict = dict(zip(strategies, palette))
    color_dict['hybrid_v4'] = 'red' # Keep hybrid prominent
    color_dict['im_v4'] = 'darkorange'
    
    for i, method in enumerate(methods):
        ax = axes[i]
        subset = df_f2[df_f2['Method'] == method].copy()
        
        # Ensure Ratio is numeric and sorted
        subset['Ratio'] = pd.to_numeric(subset['Ratio'])
        subset = subset.sort_values('Ratio')
        
        sns.lineplot(data=subset, x='Ratio', y='Rel_F1_Drop_Mean', hue='Strategy', marker='o', ax=ax,
                     hue_order=strategies, palette=color_dict, linewidth=2)
        
        ax.set_title(f"Method: {method} (Cora-GCN)")
        ax.set_xlabel("Unlearning Ratio")
        ax.set_ylabel("Relative F1 Drop (%)")
        ax.set_ylim(bottom=0)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.suptitle("FIG-2: Attack Scaling Efficiency (Strength-vs-Budget)", y=1.05)
    plt.tight_layout()
    plt.savefig('results/paper_figures/FIG-2_Scaling.pdf', bbox_inches='tight')
    plt.savefig('results/paper_figures/FIG-2_Scaling.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("FIG-2 generated.")

# --- FIG-3: The Unlearning Vulnerability Spectrum ---
def plot_fig3():
    # Show Ratio=0.05. GIF, GNNDelete, GraphEraser use cora-GCN. IDEA, MEGU use cora-GAT.
    methods_gcn = ['GIF', 'GNNDelete', 'GraphEraser']
    methods_gat = ['IDEA', 'MEGU']
    
    df_gcn = df[(df['Dataset'] == 'cora') & (df['Model'] == 'GCN') & (df['Ratio'] == 0.05) & (df['Method'].isin(methods_gcn))].copy()
    df_gat = df[(df['Dataset'] == 'cora') & (df['Model'] == 'GAT') & (df['Ratio'] == 0.05) & (df['Method'].isin(methods_gat))].copy()
    
    df_f3 = pd.concat([df_gcn, df_gat])
    
    if df_f3.empty:
        print("FIG-3 data empty, skipping")
        return
        
    pivot_df = df_f3.pivot_table(index='Method', columns='Strategy', values='Rel_F1_Drop_Mean').reset_index()
    
    # Ensure columns exist
    strats = ['tracin', 'im_v4', 'hybrid_v4']
    for col in strats:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(pivot_df['Method']))
    width = 0.25
    
    # Plot multiple bars 
    bars1 = ax1.bar(x - width, pivot_df['tracin'], width, label='TracIn (5%)', color='dodgerblue', edgecolor='black')
    bars2 = ax1.bar(x, pivot_df['im_v4'], width, label='IM (5%)', color='darkorange', edgecolor='black')
    bars3 = ax1.bar(x + width, pivot_df['hybrid_v4'], width, label='Hybrid Attack (5%)', color='crimson', edgecolor='black')
    
    # Add value labels
    ax1.bar_label(bars1, fmt='%.1f', padding=3, fontsize=9)
    ax1.bar_label(bars2, fmt='%.1f', padding=3, fontsize=9)
    ax1.bar_label(bars3, fmt='%.1f', padding=3, fontsize=9)

    ax1.set_xlabel('Unlearning Method', fontweight='bold')
    ax1.set_ylabel('Relative F1 Drop (%)', color='black', fontweight='bold')
    
    max_val = max(pivot_df['tracin'].max(), pivot_df['im_v4'].max(), pivot_df['hybrid_v4'].max())
    ax1.set_ylim(0, max(max_val * 1.2, 5))
    ax1.set_title('FIG-3: Universal Vulnerability Spectrum (Ratio=0.05)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(pivot_df['Method'])
    ax1.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0))
    
    plt.tight_layout()
    plt.savefig('results/paper_figures/FIG-3_Spectrum.pdf', bbox_inches='tight')
    plt.savefig('results/paper_figures/FIG-3_Spectrum.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("FIG-3 generated.")

# --- FIG-4: Statistical Significance Heatmap ---
def plot_fig4():
    strategies = ['pagerank', 'degree', 'tracin', 'im_v4', 'hybrid_v4']
    
    methods_gcn = ['GIF', 'GNNDelete', 'GraphEraser']
    methods_gat = ['IDEA', 'MEGU']
    
    df_gcn = df[(df['Dataset'] == 'cora') & (df['Model'] == 'GCN') & (df['Ratio'] == 0.05) & (df['Method'].isin(methods_gcn)) & (df['Strategy'].isin(strategies))].copy()
    df_gat = df[(df['Dataset'] == 'cora') & (df['Model'] == 'GAT') & (df['Ratio'] == 0.05) & (df['Method'].isin(methods_gat)) & (df['Strategy'].isin(strategies))].copy()
    
    df_f4 = pd.concat([df_gcn, df_gat])
    
    if 'P_Value' not in df_f4.columns:
        print("P_Value missing. FIG-4 skipped.")
        return
        
    pivot_p = df_f4.pivot(index='Method', columns='Strategy', values='P_Value')
    
    # Calculate -log10(p-value)
    # Filter out 0 to avoid inf
    pivot_logp = -np.log10(pivot_p.replace(0, 1e-10))
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_logp, annot=True, cmap="YlOrRd", fmt=".2f", cbar_kws={'label': '-log10(p-value)'})
    plt.title("FIG-4: Statistical Significance (-log10 P-Value against Baseline)")
    plt.tight_layout()
    plt.savefig('results/paper_figures/FIG-4_Significance.pdf', bbox_inches='tight')
    plt.savefig('results/paper_figures/FIG-4_Significance.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("FIG-4 generated.")

# --- FIG-5: Attack Depth & Mimicry (Collateral Damage) ---
def plot_fig5():
    # Filter for Ratio=0.05, cora-GCN (and cora-GAT for IDEA/MEGU)
    df_f5 = df[(df['Dataset'] == 'cora') & (df['Ratio'] == 0.05)].copy()
    
    plt.figure(figsize=(10, 7))
    
    # Target zone: High Potency, Low Gap
    plt.axvspan(5, 20, 0, 0.2, color='green', alpha=0.1, label='Target Region (Effective & Honest)')
    
    # Create scatterplot
    ax = sns.scatterplot(
        data=df_f5, 
        x="Rel_F1_Drop_Mean", 
        y="Retrain_Gap_Abs_Mean", 
        hue="Method", 
        style="Strategy",
        s=180,
        palette="bright",
        edgecolor='black',
        alpha=0.9
    )
    
    # Annotate specific high-potency points
    for i, row in df_f5.iterrows():
        if row['Rel_F1_Drop_Mean'] > 10 or (row['Rel_F1_Drop_Mean'] > 2 and row['Retrain_Gap_Abs_Mean'] < 1):
            plt.text(row['Rel_F1_Drop_Mean']+0.2, row['Retrain_Gap_Abs_Mean'], 
                     f"{row['Method']}-{row['Strategy']}", fontsize=8, alpha=0.7)
    
    plt.xlabel("Attack Potency (Relative F1 Drop %)", fontweight='bold')
    plt.ylabel("Mimicry Error (Retrain Gap %)", fontweight='bold')
    plt.title("FIG-5: Attack Depth vs. Mimicry (Bottom-Right is Target)", pad=20)
    
    # Better limits
    plt.xlim(0, max(df_f5['Rel_F1_Drop_Mean'].max() * 1.1, 10))
    plt.ylim(0, max(df_f5['Retrain_Gap_Abs_Mean'].max() * 1.1, 5))
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True, linestyle=':', alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('results/paper_figures/FIG-5_Collateral.pdf', bbox_inches='tight')
    plt.savefig('results/paper_figures/FIG-5_Collateral.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("FIG-5 generated.")

if __name__ == '__main__':
    print("Generating all paper figures...")
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()
    plot_fig5()
    print("All done. Figures saved to results/paper_figures/")
