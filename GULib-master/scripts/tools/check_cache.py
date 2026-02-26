import json
import os
from pathlib import Path

# Find project root (one level up from scripts/tools/)
project_root = Path(__file__).resolve().parent.parent.parent
cache_dir = project_root / 'results' / 'cache'
gnndelete_caches = []
if not cache_dir.exists():
    print("No cache directory.")
else:
    for f in cache_dir.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                if data.get('config', {}).get('unlearning_methods') == 'GNNDelete' and data.get('config', {}).get('dataset_name') == 'citeseer':
                    gnndelete_caches.append((f, data))
        except Exception as e:
            pass

    print(f'Found {len(gnndelete_caches)} cached results for GNNDelete on Citeseer.')
    for f, d in gnndelete_caches[:5]:
        print(f"File: {f.name}, Seed: {d['config'].get('random_seed')}, Strategy: {d['config'].get('strategy_name')}, F1 After: {d['result'].get('f1_after')}, Cached at: {d.get('cached_at')}")
