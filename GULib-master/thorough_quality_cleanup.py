import json
import os
from pathlib import Path

def thorough_cleanup():
    results_dir = Path('./results')
    deleted_count = 0
    
    for root, _, files in os.walk(results_dir):
        if 'selection_cache' in root: continue
        for file in files:
            if not file.endswith('.json'): continue
            fpath = Path(root) / file
            
            try:
                with open(fpath, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                
                is_corrupted = False
                
                # Check single results
                if 'f1_after' in data and 'f1_before' in data:
                    if abs(float(data['f1_after']) - float(data['f1_before'])) < 1e-12:
                        is_corrupted = True
                elif 'result' in data and 'f1_after' in data['result']:
                    res = data['result']
                    if abs(float(res.get('f1_after', 0)) - float(res.get('f1_before', 0))) < 1e-12:
                        is_corrupted = True
                
                # Check batch/summary results
                results_field = data.get('results', [])
                if isinstance(results_field, list) and len(results_field) > 0:
                    deltas = []
                    for r in results_field:
                        b = r.get('f1_before', r.get('perf_before'))
                        a = r.get('f1_after', r.get('perf_unlearn', r.get('attack_f1_after')))
                        if b is not None and a is not None:
                            deltas.append(abs(float(a) - float(b)))
                    if deltas and all(d < 1e-12 for d in deltas):
                        is_corrupted = True
                elif isinstance(results_field, dict) and len(results_field) > 0:
                    bad_entries = 0
                    total_entries = 0
                    for m_key, m_data in results_field.items():
                        inner_res = m_data.get('results', {})
                        for s, s_data in inner_res.items():
                            if s == 'comparison': continue
                            b = s_data.get('f1_before')
                            a = s_data.get('f1_after')
                            if b is not None and a is not None:
                                total_entries += 1
                                if abs(float(a) - float(b)) < 1e-12:
                                    bad_entries += 1
                    if total_entries > 0 and bad_entries == total_entries:
                        is_corrupted = True

                if is_corrupted:
                    fp.close()
                    print("Deleting: %s" % fpath)
                    fpath.unlink()
                    deleted_count += 1
            except Exception: pass

    print("\nCleanup Complete. Total files removed: %d" % deleted_count)

if __name__ == "__main__":
    thorough_cleanup()
