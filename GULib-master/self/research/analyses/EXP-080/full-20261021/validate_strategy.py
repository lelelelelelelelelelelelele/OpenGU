"""Standard-library verification of strategy contrasts and profile geometry."""
from pathlib import Path
from collections import defaultdict
import csv
import json
import math
import statistics

OUT = Path(__file__).resolve().parent
FIELDS = ['dataset', 'method', 'selector', 'ratio', 'seed']
METHODS = ['GIF', 'MEGU', 'GNNDelete', 'GraphEraser', 'GraphRevoker']


def read(name):
    with (OUT / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def key(row):
    return tuple(row[k] for k in FIELDS)


seeds = {key(r): r for r in read('seed_values.csv')}
checks = 0


def check(actual, expected):
    global checks
    assert math.isclose(float(actual), expected, abs_tol=1e-9, rel_tol=1e-10), (actual, expected)
    checks += 1


def loss(ds, method, selector, ratio, seed):
    return float(seeds[(ds, method, 'random', ratio, seed)]['accuracy']) - float(
        seeds[(ds, method, selector, ratio, seed)]['accuracy'])


groups = defaultdict(lambda: defaultdict(list))
for row in read('strategy_seed_contrasts.csv'):
    ds, method, selector, ratio, seed = key(row)
    h = loss(ds, method, selector, ratio, seed)
    interaction = h - loss(ds, 'Retrain', selector, ratio, seed)
    check(row['H'], h)
    check(row['interaction'], interaction)
    values = {'H': h, 'interaction': interaction}
    if method != 'Retrain':
        delta = float(seeds[key(row)]['disagreement']) - float(
            seeds[(ds, method, 'random', ratio, seed)]['disagreement'])
        check(row['D_extra'], delta)
        values['D_extra'] = delta
    for name, value in values.items():
        groups[key(row)[:-1]][name].append(value)
for row in read('strategy_summary.csv'):
    for metric, values in groups[tuple(row[k] for k in FIELDS[:-1])].items():
        check(row[metric + '_mean'], statistics.mean(values))
        check(row[metric + '_std'], statistics.stdev(values))
for row in read('im_profile_distances.csv'):
    ds, ratio, seed = (row[k] for k in ['dataset', 'ratio', 'seed'])
    used = METHODS if row['scope'] == 'five_GU' else [m for m in METHODS if m != 'GNNDelete']
    a = [loss(ds, m, 'im_rr_greedy', ratio, seed) for m in used]
    b = [loss(ds, m, row['comparator'], ratio, seed) for m in used]
    check(row['raw_rms_pp'], math.sqrt(statistics.mean((x-y)**2 for x, y in zip(a, b))))
    am, bm = statistics.mean(a), statistics.mean(b)
    check(row['centered_rms_pp'], math.sqrt(statistics.mean(((x-am)-(y-bm))**2 for x, y in zip(a, b))))
receipt = {'passed': True, 'checks': checks, 'method': 'csv/statistics independent H, interaction, D_extra, means, SD and profile-distance recomputation.'}
(OUT / 'strategy_statistics_validation.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
print(json.dumps(receipt))
