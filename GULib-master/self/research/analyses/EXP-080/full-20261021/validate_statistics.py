"""Independently recompute descriptive statistics using the standard library."""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import math
import statistics

OUT = Path(__file__).resolve().parent
KEYS = ['dataset', 'method', 'selector', 'ratio']
METRICS = ['accuracy', 'classification_auc', 'cross_entropy', 'before',
           'drop', 'gap', 'disagreement', 'retrain', 'update_detection_auc']


def read(name):
    with (OUT / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def key(row, fields):
    return tuple(row[field] for field in fields)


def number(value):
    return None if value == '' else float(value)


checks = 0


def check(actual, expected):
    global checks
    actual = number(actual)
    assert (actual is None) == (expected is None), (actual, expected)
    if actual is not None:
        assert math.isclose(actual, expected, abs_tol=1e-9, rel_tol=1e-10), (actual, expected)
    checks += 1


raw = read('cells.csv')
assert len(raw) == 2016
groups = defaultdict(list)
for row in raw:
    groups[key(row, KEYS + ['seed'])].append(row)
seeds = {}
for group, rows in groups.items():
    assert len(rows) == (3 if group[2] == 'im_rr_greedy' else 1)
    seeds[group] = {}
    for metric in METRICS:
        values = [number(r[metric]) for r in rows if r[metric] != '']
        seeds[group][metric] = statistics.mean(values) if values else None
for row in read('seed_values.csv'):
    for metric in METRICS:
        check(row[metric], seeds[key(row, KEYS + ['seed'])][metric])
for row in read('condition_summary.csv'):
    for metric in METRICS:
        values = [seeds[key(row, KEYS) + (seed,)][metric] for seed in ['42', '212', '2024']]
        values = [v for v in values if v is not None]
        check(row[metric + '_mean'], statistics.mean(values) if values else None)
        check(row[metric + '_std'], statistics.stdev(values) if len(values) > 1 else None)
        check(row[metric + '_count'], len(values))
for row in read('endpoint_changes.csv'):
    values = []
    for seed in ['42', '212', '2024']:
        prefix = key(row, ['dataset', 'method', 'selector'])
        lo = seeds[prefix + (row['low'], seed)][row['metric']]
        hi = seeds[prefix + (row['high'], seed)][row['metric']]
        values.append(hi - lo)
    check(row['mean'], statistics.mean(values))
    check(row['sd'], statistics.stdev(values))
    check(row['negative'], sum(v < 0 for v in values))
    check(row['positive'], sum(v > 0 for v in values))
contrasts = {}
for group, values in seeds.items():
    ds, method, selector, ratio, seed = group
    baseline = seeds[(ds, method, 'random', ratio, seed)]
    contrasts[group] = {m: None if values[m] is None else values[m] - baseline[m] for m in METRICS}
for row in read('paired_vs_random.csv'):
    for metric in METRICS:
        check(row[metric + '_vs_random'], contrasts[key(row, KEYS + ['seed'])][metric])
for row in read('paired_vs_random_summary.csv'):
    for metric in METRICS:
        values = [contrasts[key(row, KEYS) + (seed,)][metric] for seed in ['42', '212', '2024']]
        values = [v for v in values if v is not None]
        check(row[metric + '_vs_random_mean'], statistics.mean(values) if values else None)
        check(row[metric + '_vs_random_std'], statistics.stdev(values) if len(values) > 1 else None)
receipt = {
    'passed': True, 'checks': checks, 'cells': len(raw), 'seed_groups': len(seeds),
    'method': 'Independent csv/statistics recomputation; no pandas aggregation used.',
    'input_sha256': hashlib.sha256((OUT / 'cells.csv').read_bytes()).hexdigest(),
    'scope': 'All seed means, condition means/SD/counts, endpoint differences and same-seed Random contrasts.',
}
(OUT / 'statistics_validation.json').write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
