import json

res_file = r'experiments\im_benchmark\bench_results.json'
src_file = r'results\selection_cache\7c463b03c4a8fa904f594feb744d686c.json'

with open(src_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(res_file, 'r', encoding='utf-8') as f:
    bench = json.load(f)

bench['V0: Baseline'] = {
    'time': data['selection_result']['selection_time'],
    'selected': data['selection_result']['selected_nodes'],
    'spread': 0.0
}

with open(res_file, 'w', encoding='utf-8') as f:
    json.dump(bench, f, indent=2)

print("Injected V0 successfully.")
