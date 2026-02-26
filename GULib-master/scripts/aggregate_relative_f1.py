import os
import json
from collections import defaultdict
import numpy as np

def aggregate_relative_results(base_dir='h:/project/OpenGU/GULib-master/results/relative'):
    aggregated = defaultdict(lambda: defaultdict(list))
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.startswith('relative_seed') and file.endswith('.json'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    data = json.load(f)
                
                config = data.get('config', {})
                method = config.get('unlearning_methods', 'Unknown')
                dataset = config.get('dataset_name', 'Unknown')
                model = config.get('base_model', 'Unknown')
                ratio = config.get('unlearn_ratio', 0.05)
                
                for res in data.get('results', []):
                    strategy = res.get('strategy', 'Unknown')
                    f1_drop = res.get('relative_f1_drop', 0)
                    
                    key = (method, dataset, model, ratio, strategy)
                    aggregated[key]['f1_drop'].append(f1_drop)
                    
    print('\nRelative F1 Drop Aggregation (across 5 seeds):')
    print('-' * 90)
    print(f'{"Method":15s} | {"Dataset":10s} | {"Model":5s} | {"Ratio":5s} | {"Strategy":12s} | {"Mean F1 Drop":12s} | {"Std F1 Drop":12s} | {"N"}')
    print('-' * 90)
    for key, vals in sorted(aggregated.items()):
        method, dataset, model, ratio, strategy = key
        drops = vals['f1_drop']
        mean = np.mean(drops)
        std = np.std(drops)
        print(f'{method:15s} | {dataset:10s} | {model:5s} | {ratio:<5.2f} | {strategy:12s} | {mean*100:9.2f}%   | ± {std*100:8.2f}% | {len(drops)}')

if __name__ == '__main__':
    aggregate_relative_results()
