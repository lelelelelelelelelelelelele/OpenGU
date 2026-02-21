"""
Add seed 2024 GNNDelete/GIF tracin-only results to phase_a_v2_tracin_fix.
Also check if mg0_completion deprecated files had non-tracin data we need.
"""
import json, glob, os
import numpy as np

v2_base = 'results/experiments/_archive/phase_a_v2_tracin_fix'
new_base = 'results/experiments/_archive/tracin_fix_phase_a/phase_a'
deprecated_base = 'results/_deprecated_tracin_bug/mg0_completion/phase_a'

# Check what mg0_completion had for seed 2024
print("=== Deprecated mg0_completion seed 2024 data ===")
for f in glob.glob(f'{deprecated_base}/*/*.json'):
    if '_summary' in f:
        continue
    d = json.load(open(f))
    fname = os.path.basename(f)
    strats = list(d.get('results', {}).keys())
    print(f"  {fname}: strategies = {strats}")

# The mg0_completion files had all 6 strategies including buggy tracin
# We need to recover non-tracin strategies from them and replace tracin with fixed version

# Find the v2 seed 2024 directory (should have GraphEraser/GUIDE already)
seed2024_dirs = [d for d in os.listdir(v2_base) if 'seed2024' in d]
print(f"\nExisting v2 seed 2024 dirs: {seed2024_dirs}")

# For GNNDelete/GIF seed 2024: copy from deprecated (non-tracin strategies) + new tracin
for f in glob.glob(f'{deprecated_base}/*/*.json'):
    if '_summary' in f:
        continue
    d = json.load(open(f))
    fname = os.path.basename(f)
    method = fname.split('_cora')[0]

    # Get new tracin data
    new_files = glob.glob(f'{new_base}/*/{method}_cora_GCN_r0.05_s2024.json')
    if new_files:
        new_d = json.load(open(new_files[0]))
        d['results']['tracin'] = new_d['results']['tracin']
        print(f"  Replaced tracin in {fname} with fixed version")

    # Find or create the seed 2024 directory in v2
    if seed2024_dirs:
        out_dir = os.path.join(v2_base, seed2024_dirs[0])
    else:
        out_dir = os.path.join(v2_base, '20260221_seed2024')
        os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, fname)
    with open(out_path, 'w') as fout:
        json.dump(d, fout, indent=2)
    print(f"  Wrote: {out_path}")

# Now regenerate the comparison table
print("\n" + "=" * 90)
print("Phase A v2 (TracIn Fixed) — CORRECTED Multi-Strategy Comparison Table")
print("=" * 90)

strategies = ['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid']
methods = ['GNNDelete', 'GIF', 'GraphEraser', 'GUIDE']

all_data = {}
for seed_d in os.listdir(v2_base):
    seed_path = os.path.join(v2_base, seed_d)
    if not os.path.isdir(seed_path):
        continue
    for mf in glob.glob(os.path.join(seed_path, '*.json')):
        if '_summary' in mf or '_comparison' in mf:
            continue
        d = json.load(open(mf))
        method = os.path.basename(mf).split('_cora')[0]
        for strat, r in d.get('results', {}).items():
            key = (method, strat)
            if key not in all_data:
                all_data[key] = []
            all_data[key].append(r['f1_drop'])

header = f"{'Method':<15}"
for s in strategies:
    header += f"  {s:>13}"
print(header)
print('-' * (15 + 15 * len(strategies)))

table_lines = []
table_lines.append("Phase A v2 (TracIn Fixed) — Multi-Strategy Comparison Table")
table_lines.append(f"Dataset: cora | Model: GCN | Ratio: 0.05")
table_lines.append(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
table_lines.append("=" * 105)
table_lines.append(header)
table_lines.append('-' * (15 + 15 * len(strategies)))

for method in methods:
    row = f"{method:<15}"
    for s in strategies:
        key = (method, s)
        if key in all_data:
            vals = all_data[key]
            m = np.mean(vals)
            sd = np.std(vals)
            n = len(vals)
            cell = f"{m*100:>5.2f}+/-{sd*100:4.2f}%({n})"
            row += f"  {cell:>13}"
        else:
            row += f"  {'N/A':>13}"
    print(row)
    table_lines.append(row)

print("=" * 105)
table_lines.append("=" * 105)
table_lines.append("Note: tracin uses FIXED data (commit 55c8971), other strategies unchanged")
table_lines.append("(n) = number of seeds contributing to that cell")

# Save
table_path = os.path.join(v2_base, '_comparison_table.txt')
with open(table_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(table_lines))
print(f"\nSaved to: {table_path}")

# Verify tracin seed counts
print("\n=== TracIn seed count verification ===")
for method in methods:
    key = (method, 'tracin')
    n = len(all_data.get(key, []))
    print(f"  {method}: {n} seeds")
