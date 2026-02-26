import os
import json
from pathlib import Path

def audit_results():
    stats = {'total_scanned': 0, 'identical_f1_detected': [], 'zero_delta_detected': [], 'garbage_baseline_detected': []}
    RANDOM_GUESS = {'citeseer': 0.18, 'cora': 0.30, 'pubmed': 0.40}
    paths_to_audit = [Path("results/experiments"), Path("results/relative")]
    for base_path in paths_to_audit:
        if not base_path.exists(): continue
        for f in base_path.rglob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in: data = json.load(f_in)
                all_res = []
                if 'results' in data:
                    if isinstance(data['results'], dict):
                        for m_key, m_data in data['results'].items():
                            if isinstance(m_data, dict) and 'results' in m_data:
                                for s, s_data in m_data['results'].items():
                                    if s != 'comparison': all_res.append(s_data)
                    elif isinstance(data['results'], list): all_res = data['results']
                if not all_res: continue
                f1_afters = []
                for res in all_res:
                    f1_before = res.get('f1_before') or res.get('perf_before')
                    f1_after = res.get('f1_after') or res.get('perf_unlearn')
                    dataset = data.get('config', {}).get('dataset_name', '').lower()
                    if f1_after is not None:
                        f1_afters.append(round(f1_after, 4))
                        if f1_before is not None and abs(f1_after - f1_before) < 1e-7:
                            stats['zero_delta_detected'].append(f"{f} | strategy: {res.get('strategy')}")
                        for ds, val in RANDOM_GUESS.items():
                            if ds in dataset and abs(f1_after - val) < 0.02:
                                stats['garbage_baseline_detected'].append(f"{f} | F1={f1_after}")
                if len(f1_afters) > 1 and len(set(f1_afters)) == 1: stats['identical_f1_detected'].append(str(f))
                stats['total_scanned'] += 1
            except: continue
    cache_path = Path("results/cache")
    if cache_path.exists():
        for f in cache_path.rglob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as f_in: data = json.load(f_in)
                f1_b = data.get('f1_before'); f1_a = data.get('f1_after')
                if f1_b and f1_a and abs(f1_a - f1_b) < 1e-7: stats['zero_delta_detected'].append(f"Cache: {f}")
                stats['total_scanned'] += 1
            except: continue
    return stats

if __name__ == "__main__":
    results = audit_results()
    print(f"Scanned: {results['total_scanned']}")
    print(f"Identical F1 Groups: {len(results['identical_f1_detected'])}")
    print(f"Zero Delta: {len(results['zero_delta_detected'])}")
    print(f"Garbage Baseline: {len(results['garbage_baseline_detected'])}")
    if results['identical_f1_detected']:
        print("\n--- IDENTICAL F1 ---")
        for p in results['identical_f1_detected'][:10]: print(p)
    if results['garbage_baseline_detected']:
        print("\n--- GARBAGE BASELINE ---")
        for p in results['garbage_baseline_detected'][:10]: print(p)
