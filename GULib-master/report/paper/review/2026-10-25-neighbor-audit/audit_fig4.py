"""Recompute all clean Fig.4 scalar means/SD and paired Random differences."""
from pathlib import Path
import csv
import hashlib
import itertools
import json
import statistics

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[3] / 'self/research/analyses/EXP-080/full-20261021/seed_values.csv'
with SOURCE.open(encoding='utf-8-sig', newline='') as handle:
    rows = [r for r in csv.DictReader(handle) if r['dataset'] == 'CiteSeer' and r['method'] in ('GIF', 'GraphEraser', 'GraphRevoker', 'Retrain')]
index = {(r['method'], r['selector'], float(r['ratio']), int(r['seed'])): r for r in rows}
assert len(rows) == len(index) == 420
out = []
for method, selector, ratio in itertools.product(('GIF', 'GraphEraser', 'GraphRevoker', 'Retrain'), ('random', 'degree', 'r_point', 'gt_full', 'im_rr_greedy'), sorted({float(r['ratio']) for r in rows})):
    seeds = sorted(int(r['seed']) for r in rows if r['method'] == method and r['selector'] == selector and float(r['ratio']) == ratio)
    assert len(seeds) == 3
    item = dict(dataset='CiteSeer', method=method, selector=selector, ratio=ratio, n=3)
    for metric in ('accuracy', 'disagreement', 'retrain'):
        raw = [index[(method, selector, ratio, seed)][metric] for seed in seeds]
        if all(value == '' for value in raw):
            item.update({metric + '_mean': '', metric + '_sd': '', metric + '_minus_random_mean_pp': '', metric + '_minus_random_sd_pp': ''})
            continue
        assert all(value != '' for value in raw), (method, selector, ratio, metric)
        values = [float(index[(method, selector, ratio, seed)][metric]) for seed in seeds]
        delta = [v - float(index[(method, 'random', ratio, seed)][metric]) for v, seed in zip(values, seeds)]
        item.update({metric + '_mean': statistics.mean(values), metric + '_sd': statistics.stdev(values), metric + '_minus_random_mean_pp': statistics.mean(delta), metric + '_minus_random_sd_pp': statistics.stdev(delta)})
    out.append(item)
with (HERE / 'FIG4_CLEAN_DESCRIPTIVE.csv').open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(out[0]))
    writer.writeheader()
    writer.writerows(out)
highlights = [r for r in out if r['method'] == 'GIF' and r['selector'] == 'r_point' and r['ratio'] in (.1, .5)]
receipt = dict(input=str(SOURCE), input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(), source_rows=420, summary_rows=len(out), highlights=highlights, status='Historical scalar arithmetic only; no new inference or scientific acceptance')
(HERE / 'FIG4_ARITHMETIC.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(highlights, ensure_ascii=False))
