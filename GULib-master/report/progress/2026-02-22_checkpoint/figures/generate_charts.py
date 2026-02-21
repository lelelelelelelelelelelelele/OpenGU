#!/usr/bin/env python3
"""生成攻击效果可视化图表"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 数据 (Cora/GCN, seed=2024)
data = {
    'GIF': {'random': 0.009, 'degree': 0.019, 'pagerank': 0.013, 'tracin': 0.020, 'im': 0.017, 'hybrid': 0.028},
    'GNNDelete': {'random': 0.068, 'degree': 0.054, 'pagerank': 0.054, 'tracin': 0.090, 'im': 0.138, 'hybrid': 0.089},
    'GraphEraser': {'random': -0.070, 'degree': -0.044, 'pagerank': -0.030, 'tracin': -0.048, 'im': -0.052, 'hybrid': -0.063},
    'GUIDE': {'random': -0.046, 'degree': -0.083, 'pagerank': -0.052, 'tracin': -0.052, 'im': -0.087, 'hybrid': -0.123},
}

methods = ['GIF', 'GNNDelete', 'GraphEraser', 'GUIDE']
strategies = ['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid']
colors = {'GIF': '#2ecc71', 'GNNDelete': '#e74c3c', 'GraphEraser': '#3498db', 'GUIDE': '#9b59b6'}

output_dir = Path('report/progress/2026-02-22_checkpoint/figures')
output_dir.mkdir(parents=True, exist_ok=True)

# 图1: 柱状图 - 按方法分组
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(strategies))
width = 0.2
multiplier = 0

for method in methods:
    values = [data[method][s] * 100 for s in strategies]  # 转换为百分比
    offset = width * multiplier
    bars = ax.bar(x + offset, values, width, label=method, color=colors[method])
    multiplier += 1

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Attack Strategy', fontsize=12)
ax.set_ylabel('F1 Drop (%)', fontsize=12)
ax.set_title('Attack Effectiveness by Method and Strategy (Cora/GCN)', fontsize=14)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(strategies)
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'attack_effectiveness_by_method.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir / 'attack_effectiveness_by_method.png'}")

# 图2: 热力图 - 方法 × 策略
fig, ax = plt.subplots(figsize=(10, 6))
matrix = np.array([[data[m][s] * 100 for s in strategies] for m in methods])

im = ax.imshow(matrix, cmap='RdYlGn_r', aspect='auto', vmin=-15, vmax=15)

# 添加数值标签
for i in range(len(methods)):
    for j in range(len(strategies)):
        val = matrix[i, j]
        color = 'white' if abs(val) > 7 else 'black'
        ax.text(j, i, f'{val:.1f}%', ha='center', va='center', color=color, fontsize=10)

ax.set_xticks(np.arange(len(strategies)))
ax.set_yticks(np.arange(len(methods)))
ax.set_xticklabels(strategies)
ax.set_yticklabels(methods)
ax.set_xlabel('Attack Strategy', fontsize=12)
ax.set_ylabel('GU Method', fontsize=12)
ax.set_title('Attack Effectiveness Heatmap (F1 Drop %)', fontsize=14)

plt.colorbar(im, ax=ax, label='F1 Drop (%)')
plt.tight_layout()
plt.savefig(output_dir / 'attack_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir / 'attack_heatmap.png'}")

# 图3: 按方法类型分组
fig, ax = plt.subplots(figsize=(10, 6))

categories = ['IF-based\n(GIF)', 'Learning-based\n(GNNDelete)', 'Shard-based\n(GraphEraser, GUIDE)']
# 取各类型的平均值和最有效策略
if_based = [data['GIF'][s] * 100 for s in strategies]
learning_based = [data['GNNDelete'][s] * 100 for s in strategies]
shard_based = [np.mean([data['GraphEraser'][s], data['GUIDE'][s]]) * 100 for s in strategies]

x = np.arange(len(strategies))
width = 0.25

ax.bar(x - width, if_based, width, label='IF-based (GIF)', color='#2ecc71')
ax.bar(x, learning_based, width, label='Learning-based (GNNDelete)', color='#e74c3c')
ax.bar(x + width, shard_based, width, label='Shard-based (avg)', color='#3498db')

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Attack Strategy', fontsize=12)
ax.set_ylabel('F1 Drop (%)', fontsize=12)
ax.set_title('Attack Effectiveness by Method Type', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(strategies)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / 'attack_by_type.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_dir / 'attack_by_type.png'}")

print("\nAll charts generated successfully!")
