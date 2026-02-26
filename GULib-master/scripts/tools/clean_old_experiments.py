import json
import os
from pathlib import Path

# Find project root (one level up from scripts/tools/)
project_root = Path(__file__).resolve().parent.parent.parent
exp_dir = project_root / 'results' / 'experiments'

# 1. Delete standalone bad JSON files
deleted_files = 0
for f in exp_dir.rglob('*.json'):
    if 'cache' in str(f) or 'auto_discovered' in str(f) or 'attack_matrix' in str(f) or '_summary' in str(f):
        continue
    try:
        with open(f, 'r') as fp:
            data = json.load(fp)
        if isinstance(data, dict) and data.get('config', {}).get('unlearning_methods') == 'GNNDelete' and data.get('config', {}).get('dataset_name') == 'citeseer':
            f.unlink()
            deleted_files += 1
    except Exception as e:
        pass

# 2. Remove from _summary.json
updated_summaries = 0
for f in exp_dir.rglob('_summary.json'):
    try:
        with open(f, 'r') as fp:
            data = json.load(fp)
        
        modified = False
        if 'results' in data:
            keys_to_delete = []
            for k, v in data['results'].items():
                # k looks like "GNNDelete_citeseer_GCN_r0.05"
                if k.startswith('GNNDelete_citeseer'):
                    keys_to_delete.append(k)
            
            for k in keys_to_delete:
                del data['results'][k]
                modified = True
                
        if modified:
            with open(f, 'w') as fp:
                json.dump(data, fp, indent=2)
            updated_summaries += 1
    except Exception as e:
        pass

print(f"Deleted {deleted_files} bad standalone JSON files.")
print(f"Cleaned GNNDelete_citeseer entries from {updated_summaries} _summary.json files.")
