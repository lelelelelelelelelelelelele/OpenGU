import json
import glob
import statistics

files = glob.glob('results/cache/*.json')
records = []
for f in files:
    try:
        data = json.load(open(f, 'r', encoding='utf-8'))
        records.append(data)
    except:
        pass

ds_selection_times = {}
for r in records:
    c = r.get('config', {})
    res = r.get('result', {})
    
    # We want exact TracIn selection times
    if res.get('strategy_name') == 'tracin':
        ds = c.get('dataset_name', 'unknown')
        sel_time = res.get('selection_time')
        
        if sel_time is not None and sel_time > 0.05:  # filter zeros/cache hits
            if ds not in ds_selection_times:
                ds_selection_times[ds] = []
            ds_selection_times[ds].append(sel_time)

print("Authentic TracIn Selection Times in Cache:")
for ds, times in ds_selection_times.items():
    if times:
        print(f"Dataset {ds}: mean={statistics.mean(times):.4f}s, min={min(times):.4f}s, max={max(times):.4f}s, count={len(times)}")
