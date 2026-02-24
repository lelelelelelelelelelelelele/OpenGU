import json, os

cache_dir = r"results\selection_cache"
res_file = r"experiments\im_benchmark\bench_results.json"
found = False

for f in os.listdir(cache_dir):
    try:
        if not f.endswith(".json"): continue
        p = os.path.join(cache_dir, f)
        with open(p, 'r') as fp:
            data = json.load(fp)
            
        config = data.get('config', {})
        result = data.get('selection_result', {})
        
        dataset = config.get('dataset_name', '')
        strategy = config.get('strategy_name', '')
        nodes = result.get('selected_nodes', [])
        
        # In the context of the user's project, the exact IM parameters are seed=2024 and k=135
        # The benchmark we ran also used seed=2024
        if dataset == 'cora' and strategy == 'im' and len(nodes) == 135 and config.get('seed') == 2024:
            t = result.get('selection_time', 0.0)
            print(f"Match: {f}, Time: {t}s")
            
            with open(res_file, 'r', encoding='utf-8') as rf: 
                bench = json.load(rf)
                
            bench['V0: Baseline'] = {
                'time': t, 
                'selected': nodes, 
                'spread': 0.0  # Will be evaluated by our benchmark script
            }
            
            with open(res_file, 'w', encoding='utf-8') as wf: 
                json.dump(bench, wf, indent=2)
                
            found = True
            break
    except Exception as e:
        pass

print("Injected V0" if found else "Not found V0")
