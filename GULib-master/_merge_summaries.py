"""
Merge old phase_a summaries with new tracin fix data.
For each seed: replace tracin strategy in each method's results, regenerate _summary.json.
Output to archived phase_a_v2_tracin_fix directory structure.
"""
import json, glob, os, shutil
from datetime import datetime
from copy import deepcopy

old_base = 'results/experiments/_archive/phase_a'
new_base = 'results/experiments/_archive/tracin_fix_phase_a/phase_a'
out_base = 'results/experiments/_archive/phase_a_v2_tracin_fix'

os.makedirs(out_base, exist_ok=True)

# Map seed -> new tracin results by method
new_tracin = {}  # (seed, method) -> tracin result dict
for f in sorted(glob.glob(f'{new_base}/*/*.json')):
    if '_summary' in f:
        continue
    d = json.load(open(f))
    fname = os.path.basename(f)
    method = fname.split('_cora')[0]
    seed = fname.split('_s')[-1].replace('.json', '')
    new_tracin[(seed, method)] = d['results']['tracin']

print(f"Loaded {len(new_tracin)} new tracin results")

# Process each old seed directory
seed_dirs = sorted(glob.glob(f'{old_base}/*/'))
for seed_dir in seed_dirs:
    dirname = os.path.basename(seed_dir.rstrip('/\\'))
    # Extract seed from dirname like "20260220_195416_seed42"
    seed = dirname.split('_seed')[-1]

    out_dir = os.path.join(out_base, dirname)
    os.makedirs(out_dir, exist_ok=True)

    # Process _summary.json
    summary_path = os.path.join(seed_dir, '_summary.json')
    if os.path.exists(summary_path):
        summary = json.load(open(summary_path))
        # Update tracin in each method's results
        for method_key, method_data in summary.get('results', {}).items():
            # method_key like "GIF_cora_GCN_r0.05"
            method_name = method_key.split('_cora')[0]
            if (seed, method_name) in new_tracin:
                method_data['results']['tracin'] = new_tracin[(seed, method_name)]
                print(f"  Updated tracin in summary: {method_key} seed={seed}")

        with open(os.path.join(out_dir, '_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2)

    # Process individual method JSONs
    for method_file in glob.glob(os.path.join(seed_dir, '*.json')):
        fname = os.path.basename(method_file)
        if fname == '_summary.json':
            continue

        d = json.load(open(method_file))
        method_name = fname.split('_cora')[0]

        if (seed, method_name) in new_tracin:
            d['results']['tracin'] = new_tracin[(seed, method_name)]
            print(f"  Updated tracin in: {fname} seed={seed}")

        with open(os.path.join(out_dir, fname), 'w') as f:
            json.dump(d, f, indent=2)

print(f"\nMerged results written to: {out_base}/")

# Now generate the cross-seed aggregated summary table
import numpy as np

strategies = ['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid']
methods = ['GNNDelete', 'GIF', 'GraphEraser', 'GUIDE']
seeds_found = sorted(set(d.split('_seed')[-1] for d in os.listdir(out_base)), key=int)

print(f"\n{'='*90}")
print(f"Phase A v2 (TracIn Fixed) — Multi-Strategy Comparison Table")
print(f"Dataset: cora | Model: GCN | Ratio: 0.05 | Seeds: {', '.join(seeds_found)}")
print(f"{'='*90}")

# Collect data
all_data = {}  # (method, strategy) -> [f1_drop values]
for seed_d in os.listdir(out_base):
    seed_path = os.path.join(out_base, seed_d)
    if not os.path.isdir(seed_path):
        continue
    for mf in glob.glob(os.path.join(seed_path, '*.json')):
        if '_summary' in mf:
            continue
        d = json.load(open(mf))
        method = os.path.basename(mf).split('_cora')[0]
        for strat, r in d.get('results', {}).items():
            key = (method, strat)
            if key not in all_data:
                all_data[key] = []
            all_data[key].append(r['f1_drop'])

# Print table
header = f"{'Method':<15}"
for s in strategies:
    header += f" {s:>12}"
print(header)
print('-' * (15 + 13 * len(strategies)))

for method in methods:
    # Per-seed rows
    row_mean = f"{'':>15}"
    row = f"{method:<15}"
    means = []
    for s in strategies:
        key = (method, s)
        if key in all_data:
            vals = all_data[key]
            m = np.mean(vals)
            sd = np.std(vals)
            row += f" {m*100:>5.2f}±{sd*100:4.2f}%"
            means.append((s, m))
        else:
            row += f" {'N/A':>12}"
            means.append((s, None))
    # Find best strategy
    valid = [(s, m) for s, m in means if m is not None]
    if valid:
        best_s, best_m = max(valid, key=lambda x: x[1])
        row += f"  best={best_s}"
    print(row)

print(f"{'='*90}")
print(f"(tracin column uses FIXED data from commit 55c8971)")

# Save table as text file too
table_path = os.path.join(out_base, '_comparison_table.txt')
with open(table_path, 'w', encoding='utf-8') as f:
    f.write(f"Phase A v2 (TracIn Fixed) — Multi-Strategy Comparison Table\n")
    f.write(f"Dataset: cora | Model: GCN | Ratio: 0.05 | Seeds: {', '.join(seeds_found)}\n")
    f.write(f"Generated: {datetime.now().isoformat()}\n")
    f.write(f"{'='*90}\n")
    f.write(header + "\n")
    f.write('-' * (15 + 13 * len(strategies)) + "\n")
    for method in methods:
        row = f"{method:<15}"
        for s in strategies:
            key = (method, s)
            if key in all_data:
                vals = all_data[key]
                m = np.mean(vals)
                sd = np.std(vals)
                n = len(vals)
                row += f" {m*100:>5.2f}±{sd*100:4.2f}%"
            else:
                row += f" {'N/A':>12}"
        print_row = row  # for console
        f.write(row + "\n")
    f.write(f"{'='*90}\n")
    f.write(f"Note: tracin column uses FIXED data (commit 55c8971)\n")
    f.write(f"Note: non-tracin strategies have 4 seeds for GNNDelete/GIF, 5 seeds for GraphEraser/GUIDE\n")
    f.write(f"      tracin has 5 seeds for all methods\n")

print(f"\nTable saved to: {table_path}")
