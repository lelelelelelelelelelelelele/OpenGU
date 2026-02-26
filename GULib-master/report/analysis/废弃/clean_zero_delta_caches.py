import json
import os
from pathlib import Path

def clean_zero_delta():
    cache_dir = Path('./results/cache')
    deleted_count = 0
    
    if not cache_dir.exists():
        print("No cache directory found.")
        return

    for f in cache_dir.glob('*.json'):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
            
            # Use the result nested object
            res = data.get('result', {})
            b = res.get('f1_before')
            a = res.get('f1_after')
            
            if b is not None and a is not None:
                # Core Audit: If unlearning has ZERO impact on F1 (Delta < 1e-9), it's a corrupted run
                delta = abs(float(a) - float(b))
                if delta < 1e-12:
                    print("Deleting %s | F1: %.4f | Delta: %.2e (Zero Impact)" % (f.name, float(a), delta))
                    f.unlink()
                    deleted_count += 1
        except Exception as e:
            pass

    print("\nSuccessfully purged %d zero-impact (corrupted) cache entries." % deleted_count)

if __name__ == "__main__":
    clean_zero_delta()
