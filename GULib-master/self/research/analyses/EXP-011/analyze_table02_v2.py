"""Reproduce descriptive Table02 v2 statistics from verified local artifacts."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'results/runs/gpu4090/exp011-t2/0925-v1'
run = json.loads((BASE / 'run.json').read_text())
assert run['commit'] == '1f5cfec08494ef1a78eda16bd3f69428ac47b0bd'
assert len(run['cells']) == 1449
rows = []
for cell in run['cells']:
    assert cell['status'] == 'completed'
    for name, info in cell['files'].items():
        assert hashlib.sha256((BASE / cell['path'] / name).read_bytes()).hexdigest() == info['sha256']
    c = cell['conditions']
    stages = {x['stage']: x for x in json.loads((BASE / cell['path'] / 'metrics.json').read_text())['rows']}
    u = stages['utility']['values']
    selector = Path(c['selector_ref']).stem
    row = dict(cell_id=cell['cell_id'], dataset=c['dataset_name'], method=c['method'],
               selector=selector, seed=c['training_seed'], selection_id=cell['selection_id'],
               after=100*u['f1_after'], before=100*u['f1_before'] if u['f1_before'] is not None else None, drop=100*u['f1_drop'] if u['f1_drop'] is not None else None,
               output=cell['output'])
    if c['method'] != 'Retrain':
        g = stages['post_unlearning_utility_and_retrain_gap']
        f = stages['post_unlearning_flip_hop']
        assert g['baseline_output'] == f['baseline_output']
        row.update(gap=-100*g['values']['gap'], flip=100*f['values']['fraction_flipped'], baseline=g['baseline_output'])
    rows.append(row)
retrains = {r['output']['artifact_id']: r for r in rows if r['method']=='Retrain'}
for r in rows:
    if 'baseline' in r:
        b = retrains[r['baseline']['artifact_id']]
        assert b['output'] == r['baseline'] and b['selection_id']==r['selection_id']
        assert (b['dataset'], b['seed']) == (r['dataset'], r['seed'])
        assert abs(r['gap']-(r['after']-b['after'])) < 1e-8
random = defaultdict(list)
for r in rows:
    if r['selector']=='random': random[r['dataset'],r['method'],r['seed']].append(r['after'])
assert all(len(v)==10 for v in random.values())
groups = defaultdict(list)
for r in rows:
    r['relative_random'] = r['after'] - mean(random[r['dataset'],r['method'],r['seed']])
    groups[r['dataset'],r['method'],r['selector']].append(r)
summary=[]
for (d,m,s), rr in sorted(groups.items()):
    seeds = defaultdict(list)
    for r in rr: seeds[r['seed']].append(r['after'])
    assert len(seeds)==3
    v=dict(dataset=d,method=m,selector=s,n=len(rr),train_sd=stdev([mean(a) for a in seeds.values()]))
    for k in ['after','before','drop','gap','flip','relative_random']:
        v[k]=mean(r[k] for r in rr) if rr[0].get(k) is not None else None
    summary.append(v)
with (OUT/'table02-v2-summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
new={ (r['dataset'],r['seed'],r['selector'],r['selection_id']):r for r in rows if r['method']=='IDEA'}
pairs=[(r,new[r['dataset'],r['seed'],r['selector'],r['selection_id']]) for r in rows if r['method']=='GIF']
stats=dict(cells=len(rows),gu_pairs=sum('baseline' in r for r in rows),selections=len(set(r['selection_id'] for r in rows)),
           gif_idea_equal_f1=sum(a['after']==b['after'] for a,b in pairs),
           gif_idea_equal_content_hash=sum(a['output']['content_hash']==b['output']['content_hash'] for a,b in pairs),
           gif_idea_max_f1_difference_pp=max(abs(a['after']-b['after']) for a,b in pairs),
           manifest_sha256=hashlib.sha256((BASE/'run.json').read_bytes()).hexdigest())
(OUT/'table02-v2-audit.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
lines = ['# Table02 v2 完整统计', '', '由 analyze_table02_v2.py 生成。F1 为百分数，其余差值及训练 SD 为百分点；Flip 为 GU 与同请求 Retrain 的预测分歧百分比。', '']
for d in ['Cora','CiteSeer','PubMed']:
    lines += ['## '+d, '', '| 方法 | Selector | n | after F1 | 训练SD | before−after | GU−Retrain | 相对Random | Flip % |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for v in summary:
        if v['dataset'] != d: continue
        values = [v['method'],v['selector'],str(v['n'])]+['—' if v[k] is None else f'{v[k]:.3f}' for k in ['after','train_sd','drop','gap','relative_random','flip']]
        lines.append('| '+' | '.join(values)+' |')
    lines.append('')
(OUT/'table02-v2-tables.md').write_text('\n'.join(lines),encoding='utf-8')

