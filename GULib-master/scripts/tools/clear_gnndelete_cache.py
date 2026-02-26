import json
import os
from pathlib import Path

# Find project root (one level up from scripts/tools/)
project_root = Path(__file__).resolve().parent.parent.parent
cache_dir = project_root / 'results' / 'cache'
deleted_count = 0
if cache_dir.exists():
    for f in cache_dir.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                if data.get('config', {}).get('unlearning_methods') == 'GNNDelete':
                    fp.close() # Make sure file is closed before deleting
                    f.unlink()
                    deleted_count += 1
        except Exception as e:
            print(f"Error processing {f}: {e}")

print(f'Deleted {deleted_count} cached results for GNNDelete.')
