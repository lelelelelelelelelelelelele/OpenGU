#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Shard 保护效应分析图
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 基于脚本路径定位数据与输出目录，避免依赖当前工作目录
SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = SCRIPT_DIR.parent
DATA_DIR = ANALYSIS_DIR / "assets" / "data"
FIGURE_DIR = ANALYSIS_DIR / "assets" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 加载数据
with open(DATA_DIR / 'shard_effect_data.json', encoding='utf-8') as f:
    step0_data = json.load(f)

with open(DATA_DIR / 'mg0_shard_effect_data.json', encoding='utf-8') as f:
    mg0_data = json.load(f)

# 图1: Step0 baseline - 所有方法的 f1 变化
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图: Step0 baseline
methods = [d['method'] for d in step0_data]
pct_changes = [d['pct_change'] for d in step0_data]
colors = ['red' if p > 0 else 'blue' for p in pct_changes]

ax1 = axes[0]
bars = ax1.barh(methods, pct_changes, color=colors, alpha=0.7)
ax1.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
ax1.set_xlabel('F1 Change (%)')
ax1.set_title('Step0: Random Selection Baseline (ratio=0.05)')
ax1.set_xlim(-20, 25)

# 添加数值标签
for bar, pct in zip(bars, pct_changes):
    width = bar.get_width()
    ax1.text(width + 1, bar.get_y() + bar.get_height()/2,
             f'{pct:+.2f}%', va='center', fontsize=9)

# 右图: MG-0 按方法类型分组
method_types = {
    'Learning-based': ['GNNDelete'],
    'IF-based': ['GIF'],
    'Shard-based': ['GraphEraser']
}

# 计算每个类型的平均变化
type_avg = {}
for mtype, methods in method_types.items():
    vals = [d['pct_change'] for d in mg0_data if d['method'] in methods]
    type_avg[mtype] = np.mean(vals)

ax2 = axes[1]
colors2 = ['green' if v < 0 else 'orange' for v in type_avg.values()]
bars2 = ax2.barh(list(type_avg.keys()), list(type_avg.values()), color=colors2, alpha=0.7)
ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
ax2.set_xlabel('Average F1 Change (%)')
ax2.set_title('MG-0: F1 Change by Method Type (avg over strategies)')
ax2.set_xlim(-15, 5)

for bar, pct in zip(bars2, type_avg.values()):
    width = bar.get_width()
    ax2.text(width - 3, bar.get_y() + bar.get_height()/2,
             f'{pct:+.2f}%', va='center', fontsize=10, color='white', fontweight='bold')

plt.tight_layout()
overview_path = FIGURE_DIR / 'shard_effect_overview.png'
plt.savefig(overview_path, dpi=150, bbox_inches='tight')
print(f'Saved: {overview_path}')

# 图2: 详细对比 - GraphEraser 的所有策略
fig2, ax = plt.subplots(figsize=(10, 6))

shard_data = [d for d in mg0_data if d['method'] == 'GraphEraser']
x = np.arange(len(shard_data))
pct_vals = [d['pct_change'] for d in shard_data]
labels = [f"{d['method']}_{d['strategy']}" for d in shard_data]

colors3 = ['orange' if p > 0 else 'green' for p in pct_vals]
bars3 = ax.bar(x, pct_vals, color=colors3, alpha=0.7)

ax.set_ylabel('F1 Change (%)')
ax.set_title('GraphEraser: F1 Change Across Strategies')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 标注数值
for bar, pct in zip(bars3, pct_vals):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{pct:+.1f}%', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
detail_path = FIGURE_DIR / 'shard_effect_detail.png'
plt.savefig(detail_path, dpi=150, bbox_inches='tight')
print(f'Saved: {detail_path}')

# 图3: 对比 Learning-based vs Shard-based
fig3, ax = plt.subplots(figsize=(8, 5))

# Learning-based: GNNDelete
ln_data = [d for d in mg0_data if d['method'] == 'GNNDelete']
ln_pct = [d['pct_change'] for d in ln_data]

# Shard-based: GraphEraser
shard_pcts = [d['pct_change'] for d in shard_data]

positions = [1, 2]
bp1 = ax.boxplot([ln_pct, shard_pcts], positions=positions, widths=0.6,
                  patch_artist=True)
bp1['boxes'][0].set_facecolor('lightblue')
bp1['boxes'][1].set_facecolor('lightsalmon')

ax.set_xticklabels(['Learning-based\n(GNNDelete)', 'Shard-based\n(GraphEraser)'])
ax.set_ylabel('F1 Change (%)')
ax.set_title('Attack Effect: Learning-based vs Shard-based')
ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

# 添加均值点
ax.scatter([1], [np.mean(ln_pct)], color='blue', s=100, zorder=5, marker='D', label='Mean')
ax.scatter([2], [np.mean(shard_pcts)], color='red', s=100, zorder=5, marker='D')

ax.legend()
plt.tight_layout()
boxplot_path = FIGURE_DIR / 'learning_vs_shard_boxplot.png'
plt.savefig(boxplot_path, dpi=150, bbox_inches='tight')
print(f'Saved: {boxplot_path}')

print('\n所有图表已生成!')
