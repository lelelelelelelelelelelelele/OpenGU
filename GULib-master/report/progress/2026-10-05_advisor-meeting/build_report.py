"""Build the advisor report from REPORT.md and verified, read-only run evidence."""
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import html
import json
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.mathtext import math_to_image
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSETS = HERE / 'assets'
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'Microsoft YaHei', 'axes.unicode_minus': False,
                     'font.size': 11, 'svg.fonttype': 'path', 'axes.spines.top': False,
                     'axes.spines.right': False})
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
METHODS = ['GNNDelete', 'GIF', 'MEGU', 'GraphEraser', 'GraphRevoker']
SELECTORS = ['degree', 'pagerank', 'r_point', 'gt_full', 'rr_4096', 'rr_16384', 'rr_65536']
LABELS = ['Degree', 'PageRank', 'R-point', 'D-full', 'RR-4096', 'RR-16384', 'RR-65536']


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_run(rel, expected_sha, count, random_count):
    base = ROOT / rel
    run = read(base / 'run.json')
    assert sha(base / 'run.json') == expected_sha
    assert len(run['cells']) == count and run['status'] == 'completed'
    rows, checked = [], 0
    for cell in run['cells']:
        assert cell['status'] == 'completed'
        for name, meta in cell['files'].items():
            assert sha(base / cell['path'] / name) == meta['sha256']
            checked += 1
        c = cell['conditions']
        stages = {s['stage']: s for s in read(base / cell['path'] / 'metrics.json')['rows']}
        sel = read(base / cell['path'] / 'selection.json')
        assert cell['selection_id'] == sel['selection_id']
        assert len(set(sel['selected_nodes'])) == len(sel['selected_nodes']) == sel['requested_k']
        assert c['budget_ratio'] == .1
        v = stages['utility']['values']
        stem = Path(c['selector_ref']).stem
        source = next((s for s in ['SGC', 'GAT', 'GIN'] if stem.endswith('_' + s.lower())), 'GCN')
        selector = c['selector'] if count == 756 else stem
        before = None if v['f1_before'] is None else 100 * v['f1_before']
        r = dict(dataset=c['dataset_name'], method=c['method'], seed=c['training_seed'],
                 selector=selector, source=source, before=before, after=100*v['f1_after'],
                 cell_id=cell['cell_id'], split=c['dataset_fingerprint'],
                 selection_id=cell['selection_id'], output=cell['output'])
        if c['method'] != 'Retrain':
            gap = stages['post_unlearning_utility_and_retrain_gap']
            flip = stages['post_unlearning_flip_hop']
            assert gap['baseline_output'] == flip['baseline_output']
            r.update(G=100*gap['values']['gap'], flip=100*flip['values']['fraction_flipped'],
                     baseline=gap['baseline_output'], U=before-r['after'])
        rows.append(r)
    by_output = {r['output']['artifact_id']: r for r in rows if r['method'] == 'Retrain'}
    for r in rows:
        if r['method'] == 'Retrain':
            continue
        b = by_output[r['baseline']['artifact_id']]
        assert b['output'] == r['baseline']
        assert all(r[k] == b[k] for k in ['dataset', 'split', 'seed', 'selection_id'])
        assert abs(r['G'] - (b['after']-r['after'])) < 1e-8
        r['R'] = b['after']
        r['D'] = r['before'] - b['after']
        assert abs(r['U'] - r['D'] - r['G']) < 1e-8
    df = pd.DataFrame(rows)
    rand = df[df.selector == 'random']
    keys = ['dataset', 'method', 'seed']
    assert rand.groupby(keys).size().eq(random_count).all()
    refs = rand.groupby(keys)[['after', 'G']].mean().rename(columns={'after':'random_after', 'G':'random_G'})
    df = df.merge(refs, on=keys, validate='many_to_one')
    df['A'] = df.random_after - df.after
    df['E'] = df.G - df.random_G
    df['A_R'] = df.A - df.E
    return df, {'commit':run['commit'], 'cells':count, 'verified_cell_files':checked,
                'manifest_sha256':expected_sha, 'random_draws_per_training_seed':random_count}


t11, audit11 = load_run('results/runs/gpu4090/exp011-t2/0925-v1',
    'ae24efa4a348cdcee1e87efd6aa15714c679c7a0a8591787c41cf1c6e95e7720', 1449, 10)
t13, audit13 = load_run('results/runs/gpu4090/exp013-surrogate-to-gcn/r1',
    '70588d5793760e44ae268dfe55b3648e0638b71fde3a4db0eee998dc51760a49', 756, 3)
assert audit11['commit'] == '1f5cfec08494ef1a78eda16bd3f69428ac47b0bd'
assert audit13['commit'] == '62926d95b843af137076eb9dd0a15e1c54c75663'
original13 = pd.read_csv(ROOT / 'self/research/analyses/EXP-013/cells.csv').set_index('cell_id')
for _, r in t13[t13.method != 'Retrain'].iterrows():
    for k in ['after', 'before', 'U', 'G', 'flip']:
        assert np.isclose(r[k], original13.loc[r.cell_id, k]), (r.cell_id, k)

# First average selection repeats within each training seed; then weight seeds equally.
keys11 = ['dataset', 'method', 'selector', 'seed']
values = ['before', 'after', 'U', 'D', 'G', 'A', 'A_R', 'E', 'flip']
seed11 = t11.groupby(keys11, as_index=False)[values].mean()
avg11 = seed11.groupby(keys11[:-1])[values].mean()
original11 = pd.read_csv(ROOT / 'self/research/analyses/EXP-011/table02-v2-summary.csv').set_index(keys11[:-1])
for key, r in original11.iterrows():
    x = avg11.loc[key]
    assert np.isclose(x.after, r.after)
    assert np.isclose(x.A, -r.relative_random)
    if key[1] != 'Retrain':
        assert np.isclose(x.G, -r.gap) and np.isclose(x.flip, r.flip)
        assert np.isclose(x.U, r['drop'])
avg11.reset_index().to_csv(ASSETS / 'table02-unified-signs.csv', index=False, encoding='utf-8')
for d in DATASETS:
    for s in ['random'] + SELECTORS:
        assert np.isclose(avg11.loc[(d, 'GIF', s)].after, avg11.loc[(d, 'IDEA', s)].after)


def save(fig, stem):
    fig.savefig(ASSETS / (stem+'.svg'), bbox_inches='tight', facecolor='white')
    fig.savefig(ASSETS / (stem+'.png'), dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# Retrain is the first empirical link in the manuscript's argument.
retrain_rows = []
fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.0), layout='constrained')
for ax, d in zip(axes, DATASETS):
    for x, sel in enumerate(['r_point', 'gt_full']):
        group = seed11[(seed11.dataset == d) & (seed11.method == 'Retrain') &
                       (seed11.selector == sel)].sort_values('seed')
        assert len(group) == 3
        vals = group.A.to_numpy()
        ax.bar(x, vals.mean(), width=.5, color=['#294d63', '#298e8a'][x])
        ax.scatter(x + np.array([-.11, 0, .11]), vals, s=28,
                   c=['#913f55', '#e1a032', '#244d90'], edgecolors='white', zorder=3)
        ax.text(x, max(vals.max(), vals.mean()) + .14,
                f'{vals.mean():+.2f}', ha='center', fontsize=11)
        retrain_rows.append(dict(dataset=d, selector=sel,
            random_after=avg11.loc[(d, 'Retrain', 'random'), 'after'],
            after_mean=group.after.mean(), after_sd=group.after.std(ddof=1),
            A_R_mean=vals.mean(), A_R_sd=vals.std(ddof=1)))
    ax.axhline(0, color='#6b7785', lw=.8)
    ax.set_ylim(-1.4, 3.9)
    ax.set_xticks([0, 1], ['R-point', 'D-full'])
    ax.set_title(d, loc='left', weight='bold')
    ax.set_ylabel('Retrain 相对 Random 的额外损伤（pp）')
save(fig, '05-retrain-reference')
pd.DataFrame(retrain_rows).to_csv(ASSETS / 'retrain-reference.csv', index=False, encoding='utf-8')


# Fixed complete selector matrix, without selecting the strongest strategy per method.
fig, axes = plt.subplots(3, 1, figsize=(11.8, 10.8), layout='constrained')
for ax, d in zip(axes, DATASETS):
    arr = np.array([[avg11.loc[(d,m,s)].A for s in SELECTORS] for m in METHODS])
    im = ax.imshow(arr, cmap='RdBu_r', norm=TwoSlopeNorm(vmin=-7, vcenter=0, vmax=7), aspect='auto')
    ax.set_xticks(range(7), LABELS, fontsize=10)
    ax.set_yticks(range(5), ['GNNDelete','GIF / IDEA','MEGU','GraphEraser','GraphRevoker'])
    ax.set_title(d, loc='left', weight='bold', fontsize=14)
    for (i,j), val in np.ndenumerate(arr):
        ax.text(j,i,f'{val:+.2f}',ha='center',va='center',color='white' if abs(val)>4.4 else '#17293b',fontsize=10)
fig.colorbar(im, ax=axes, shrink=.6, label='相对 Random 的额外效用损失 A（pp）；正值表示损失增加')
save(fig, '01-selector-response')

# Explicit observed endpoint decomposition, plus random-adjusted decomposition.
chosen = [('Cora','GNNDelete','gt_full'), ('PubMed','GIF','gt_full')]
avg11.loc[chosen].reset_index().to_csv(ASSETS/'decomposition-cases.csv', index=False, encoding='utf-8')
fig, axes = plt.subplots(1,2,figsize=(11.8,4.6),layout='constrained')
for ax,key in zip(axes,chosen):
    r=avg11.loc[key]
    xx=np.arange(6)
    vv=[r.U,r.D,r.G,r.A,r.A_R,r.E]
    ax.bar(xx,vv,color=['#294d63','#e2ad54','#298e8a']*2,width=.62)
    ax.axhline(0,color='#6b7785',lw=.8)
    for x,v in zip(xx,vv):
        ax.text(x,v+(0.4 if v>=0 else -.35),f'{v:+.2f}',ha='center',va='bottom' if v>=0 else 'top',fontsize=10)
    ax.set_xticks(xx,['总损失\nU','重训变化\nD','效用差距\nG','额外损失\nA','重训增量\nA_R','差距增量\nE'])
    ax.axvline(2.5,color='#c4cdd4',ls='--')
    ax.set_title(f'{key[0]} / {key[1]} / D-full',loc='left',fontsize=12)
    ax.set_ylabel('百分点（pp）')
    ax.set_ylim(min(vv)-1.2,max(vv)+2.5)
save(fig,'02-decomposition')

fig,axes=plt.subplots(1,3,figsize=(11.8,3.9),layout='constrained')
for ax,d in zip(axes,DATASETS):
    rr=avg11.loc[(d,'GIF','random')]
    pp=avg11.loc[(d,'GIF','r_point')]
    vals=[rr.flip,pp.flip]
    ax.bar([0,1],vals,color=['#9caeb9','#298e8a'],width=.55)
    for x,v in enumerate(vals): ax.text(x,v+.12,f'{v:.2f}%',ha='center')
    ax.set_xticks([0,1],['Random','R-point'])
    ax.set_ylim(0,9)
    ax.set_title(f'{d}\nR-point 的额外效用损失 A = {pp.A:+.2f} pp',fontsize=11)
    ax.set_ylabel('与同请求 Retrain 的预测分歧（%）')
save(fig,'03-utility-and-disagreement')

# All source models and both simple baselines, with training repeats visible.
keys13=['dataset','method','source','selector','seed']
seed13=t13.groupby(keys13,as_index=False)[values].mean()

# Compare strategies and selector models; training seeds remain repeat units.
behavior11 = seed11[seed11.method != 'Retrain'].copy()
random11 = behavior11[behavior11.selector == 'random'].set_index(
    ['dataset', 'method', 'seed']).flip.rename('random_flip')
behavior11 = behavior11.join(random11, on=['dataset', 'method', 'seed'])
behavior11['delta_flip'] = behavior11.flip - behavior11.random_flip
behavior13 = seed13[seed13.method != 'Retrain'].copy()
random13 = behavior13[behavior13.selector == 'random'].set_index(
    ['dataset', 'method', 'seed']).flip.rename('random_flip')
behavior13 = behavior13.join(random13, on=['dataset', 'method', 'seed'])
behavior13['delta_flip'] = behavior13.flip - behavior13.random_flip

def behavior_summary(frame, keys):
    summary = frame.groupby(keys)[['flip', 'delta_flip', 'A']].agg(['mean', 'std', 'min', 'max'])
    summary.columns = ['_'.join(c) for c in summary.columns]
    return summary

b11 = behavior_summary(behavior11, ['dataset', 'method', 'selector'])
b13 = behavior_summary(behavior13, ['dataset', 'method', 'selector', 'source'])
b11.reset_index().to_csv(ASSETS/'behavior-selector-summary.csv', index=False, encoding='utf-8')
b13.reset_index().to_csv(ASSETS/'behavior-transfer-summary.csv', index=False, encoding='utf-8')
behavior13.to_csv(ASSETS/'behavior-transfer-seeds.csv', index=False, encoding='utf-8')

# GIF R-point example: behavior and task utility, with source model as the axis.
fig, axes = plt.subplots(2, 3, figsize=(11.8, 7.0), layout='constrained', sharey='row')
for j, d in enumerate(DATASETS):
    for i, (metric, title, bounds) in enumerate([
        ('delta_flip', '相对 Random 的预测分歧增量（pp）', (-1.6, 6.3)),
        ('A', '相对 Random 的额外效用损伤（pp）', (-1.6, 1.6)),
    ]):
        ax = axes[i, j]
        for x, (src, sel) in enumerate([('GCN', 'r_point'), ('SGC', 'r_point'),
                                       ('GAT', 'r_point'), ('GIN', 'r_point'), ('GCN', 'degree')]):
            row = b13.loc[(d, 'GIF', sel, src)]
            mean, sd = row[metric+'_mean'], row[metric+'_std']
            assert bounds[0] < mean-sd and mean+sd < bounds[1]
            ax.bar(x, mean, yerr=sd, capsize=3, width=.58,
                   color='#294d63' if x == 0 else '#a3afb8' if x == 4 else '#298e8a',
                   error_kw={'elinewidth': 1, 'ecolor': '#4e606b'})
            ax.text(x, max(mean+sd, 0)+.14, f'{mean:+.2f}', ha='center', fontsize=9)
        ax.axhline(0, color='#6b7785', lw=.8)
        ax.set_ylim(*bounds)
        ax.set_xticks(range(5), ['GCN\ndirect', 'SGC', 'GAT', 'GIN', 'Degree'], fontsize=9)
        ax.set_ylabel(title, fontsize=10)
        if i == 0:
            ax.set_title(d, loc='left', fontsize=13, weight='bold')
fig.suptitle('GIF / R-point：更换选点模型后的两种响应\n均值 ± 训练重复 SD（n = 3）；Degree 为结构基线', fontsize=13)
save(fig, '06-surrogate-behavior')

fig,axes=plt.subplots(1,3,figsize=(11.8,4.6),layout='constrained')
transfer=[]
for ax,d in zip(axes,DATASETS):
    groups=[('GCN','gt_full'),('SGC','gt_full'),('GAT','gt_full'),('GIN','gt_full'),('GCN','random'),('GCN','degree')]
    for x,(src,sel) in enumerate(groups):
        a=seed13[(seed13.dataset==d)&(seed13.method=='GNNDelete')&(seed13.source==src)&(seed13.selector==sel)].sort_values('seed')
        assert len(a)==3
        v=a.U.to_numpy()
        ax.bar(x,v.mean(),color='#294d63' if src=='GCN' and sel=='gt_full' else '#298e8a' if sel=='gt_full' else '#a3afb8',width=.58,alpha=.84)
        ax.scatter(x+np.array([-.13,0,.13]),v,s=24,c=['#913f55','#e1a032','#244d90'],zorder=3,edgecolors='white',linewidths=.4)
        ax.text(x,max(v)+.55,f'{v.mean():.2f}',ha='center',fontsize=9)
        transfer.append(dict(dataset=d,source=src,selector=sel,U_mean=v.mean(),U_sd=v.std(ddof=1)))
    ax.set_xticks(range(6),['GCN\ndirect','SGC','GAT','GIN','Random','Degree'],fontsize=9)
    ax.set_ylim(-2.2,25.8)
    ax.axhline(0,color='#6b7785',lw=.8)
    ax.set_title(d,loc='left',fontsize=13,weight='bold')
    ax.set_ylabel('总效用下降 U（pp）')
save(fig,'04-transfer')
pd.DataFrame(transfer).to_csv(ASSETS/'transfer-example.csv',index=False,encoding='utf-8')

source=(HERE/'REPORT.md').read_text(encoding='utf-8-sig')
assert '\ufffd' not in source

# Bind the dated acceptance table to both authoritative Work Plan layers.
expected_states = {
    'EXP-011': ('completed', 'complete', 'accepted'),
    'EXP-013': ('completed', 'complete', 'not_requested'),
    'EXP-032': ('completed', 'review', 'pending'),
    'EXP-053': ('completed', 'complete', 'accepted'),
    'EXP-062': ('not_required', 'complete', 'accepted'),
    'EXP-079': ('pending', None, None),
}
snapshot = {'as_of': '2026-10-06', 'experiments': []}
for exp, states in expected_states.items():
    live_path = ROOT / f'self/research/experiments/{exp}.json'
    analysis_path = ROOT / f'self/research/analyses/{exp}.json'
    live = read(live_path)
    analysis = read(analysis_path) if analysis_path.exists() else {}
    observed = (live.get('execution', {}).get('state'),
                analysis.get('analysis', {}).get('state'),
                analysis.get('decision', {}).get('state'))
    assert observed == states, (exp, 'Refresh the dated report status table', observed)
    snapshot['experiments'].append(dict(id=exp, execution=live.get('execution'),
        analysis=analysis.get('analysis'), decision=analysis.get('decision'),
        live_source=str(live_path.relative_to(ROOT)), live_sha256=sha(live_path),
        analysis_source=str(analysis_path.relative_to(ROOT)) if analysis else None,
        analysis_sha256=sha(analysis_path) if analysis else None))
(ASSETS/'workplan-status-snapshot.json').write_text(
    json.dumps(snapshot, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# Check printed tables against independently reproduced data.
def signed(value, digits=2):
    return f'{value:+.{digits}f}'.replace('-', '−')

printed_rows = []
for d in DATASETS:
    r, p, g = [avg11.loc[(d, 'Retrain', sel)] for sel in ['random', 'r_point', 'gt_full']]
    printed_rows.append(f'| {d} | {r.after:.2f}% | {p.after:.2f}% | {g.after:.2f}% | {signed(p.A)} pp | {signed(g.A)} pp |')
    r, p = [avg11.loc[(d, 'GIF', sel)] for sel in ['random', 'r_point']]
    printed_rows.append(f'| {d} | {signed(p.A)} pp | {r.flip:.2f}% | {p.flip:.2f}% |')
for d, m, sel in chosen:
    r = avg11.loc[(d, m, sel)]
    printed_rows.append(f'| {d} / {m} / D-full | ' + ' | '.join(
        signed(r[k]) for k in ['U', 'D', 'G', 'A', 'A_R', 'E']) + ' |')
for d in ['Cora', 'PubMed']:
    vals = []
    for src, sel in [('GCN','gt_full'), ('GIN','gt_full'), ('SGC','gt_full'), ('GCN','random'), ('GCN','degree')]:
        vals.append(seed13[(seed13.dataset == d) & (seed13.method == 'GNNDelete') &
                          (seed13.source == src) & (seed13.selector == sel)].U.mean())
    printed_rows.append(f'| {d} / GNNDelete / D-full | ' + ' | '.join(f'{v:.2f}' for v in vals) + ' |')
for row in printed_rows:
    assert row in source, ('Printed report row does not match evidence', row)

for sel, label in [('random', 'Random'), ('degree', 'Degree'), ('pagerank', 'PageRank'),
                   ('rr_4096', 'IM / RR-4096'), ('rr_16384', 'IM / RR-16384'),
                   ('rr_65536', 'IM / RR-65536'), ('r_point', 'R-point'), ('gt_full', 'D-full')]:
    cells = [f'{b11.loc[(d,"GIF",sel)].flip_mean:.2f} ± {b11.loc[(d,"GIF",sel)].flip_std:.2f}' for d in DATASETS]
    row = '| '+label+' | '+' | '.join(cells)+' |'
    assert row in source, row
    printed_rows.append(row)
for src in ['GCN', 'SGC', 'GAT', 'GIN']:
    label = 'GCN direct' if src == 'GCN' else src
    cells = [f'{signed(b13.loc[(d,"GIF","r_point",src)].delta_flip_mean)} ± {b13.loc[(d,"GIF","r_point",src)].delta_flip_std:.2f}' for d in DATASETS]
    row = '| '+label+' | '+' | '.join(cells)+' |'
    assert row in source, row
    printed_rows.append(row)
for d in DATASETS:
    r = b13.loc[(d, 'MEGU', 'r_point', 'GAT')]
    row = f'| {d} | {signed(r.A_mean)} pp | {signed(r.delta_flip_mean)} pp |'
    assert row in source, row
    printed_rows.append(row)

contrast32 = pd.read_csv(ROOT / 'self/research/analyses/evidence/AAGU-032-AAGU-053-3000epoch-20260923/AAGU-032-paired-baseline-contrasts.csv')
selected32 = contrast32[contrast32.selector.isin(['gt_full', 'gt_full_all_trainable', 'gt_full_all_trainable_hops3'])]
assert len(selected32) == 72
for d in DATASETS:
    degree = selected32[(selected32.dataset == d) & (selected32.reference == 'degree')].test_accuracy_difference_pp
    random = selected32[(selected32.dataset == d) & (selected32.reference == 'random')].test_accuracy_difference_pp
    assert len(degree) == len(random) == 12
    counts = f'{(degree < -1e-10).sum()} / {(degree.abs() <= 1e-10).sum()} / {(degree > 1e-10).sum()}'
    row = f'| {d} | {signed(degree.mean(), 3)} pp | {counts} | {signed(random.mean(), 3)} pp |'
    assert row in source, row
    printed_rows.append(row)

formulas=[]
def formula(m):
    expression=m.group(1).strip()
    buffer=BytesIO()
    math_to_image('$'+expression+'$',buffer,format='svg',dpi=160,color='#193b48')
    s=buffer.getvalue().decode('utf-8')
    s=s[s.index('<svg'):]
    token=f'FORMULA{len(formulas):03d}TOKEN'
    formulas.append((token,'<div class="equation" role="img" aria-label="'+html.escape(expression,quote=True)+'">'+s+'</div>'))
    return token

body=MarkdownIt('commonmark',{'html':False}).enable('table').render(re.sub(r'\$\$(.*?)\$\$',formula,source,flags=re.S))
for token,replacement in formulas:
    body=body.replace('<p>'+token+'</p>',replacement)

# Embed all report figures: the HTML reads offline without external fonts/scripts.
def embed(m):
    path=HERE/m.group(1)
    assert path.is_file(),path
    data=base64.b64encode(path.read_bytes()).decode('ascii')
    return 'src="data:image/png;base64,'+data+'"'
body=re.sub(r'src="(assets/[^\"]+\.png)"',embed,body)
toc=[]
counter=[0]
def heading(m):
    counter[0]+=1
    name='section-'+str(counter[0])
    toc.append('<a href="#'+name+'">'+m.group(1)+'</a>')
    return '<h2 id="'+name+'">'+m.group(1)+'</h2>'
body=re.sub(r'<h2>(.*?)</h2>',heading,body)
style='''
:root{color-scheme:light;--ink:#203440;--muted:#647681;--teal:#167a76}
*{box-sizing:border-box}body{margin:0;background:#f2f5f4;color:var(--ink);font:16px/1.9 "Microsoft YaHei","Segoe UI",sans-serif}
header{background:#193b48;color:#e6f0ef;padding:28px max(24px,calc((100vw - 1060px)/2));font-size:14px;letter-spacing:.06em}
main{max-width:1120px;margin:0 auto;background:#fff;padding:44px 54px 72px}
h1{font-size:32px;line-height:1.4;letter-spacing:-.02em;margin:0 0 16px}h2{font-size:24px;line-height:1.5;margin:56px 0 18px;padding-top:18px;border-top:2px solid #d5e5e1;color:#154f55;scroll-margin-top:20px}h3{font-size:19px;margin:30px 0 12px}
p{margin:14px 0}a{color:#126e75;text-underline-offset:3px}strong{font-weight:650}blockquote{border-left:4px solid #2e9188;margin:24px 0;padding:10px 24px;background:#f0f7f5;font-size:18px}blockquote p{margin:8px 0}
table{width:100%;border-collapse:collapse;margin:22px 0;font-size:13.5px;line-height:1.65}thead{background:#eaf3f1}th,td{padding:10px 12px;text-align:left;border-bottom:1px solid #dbe5e2}th{font-weight:650}tr:nth-child(even){background:#f8faf9}
img{max-width:100%;height:auto;display:block;margin:22px auto}code{font: .88em Consolas,monospace;background:#edf2f2;padding:2px 4px;overflow-wrap:anywhere}.equation{overflow-x:auto;background:#f6f9f8;padding:20px;margin:22px 0;text-align:center}.equation svg{max-width:100%;height:auto;min-height:24px}
nav{display:flex;gap:8px 20px;flex-wrap:wrap;padding:20px 0;margin-top:14px;border-top:1px solid #dbe5e2;font-size:13px}nav a{text-decoration:none}details{margin:24px 0;padding:12px 18px;border:1px solid #d5e5e1;border-radius:6px}summary{cursor:pointer;color:var(--teal);font-size:14px}li{margin:7px 0}footer{padding:24px;color:var(--muted);text-align:center;font-size:12px}
@media(max-width:720px){main{padding:28px 20px}h1{font-size:26px}h2{font-size:22px}table{display:block;overflow-x:auto}blockquote{padding:8px 16px}}
@media print{body{background:white;font-size:11pt}header,details,nav,footer{display:none}main{padding:0;max-width:none}h1{font-size:23pt}h2{font-size:17pt;break-after:avoid;margin-top:28px}h3{break-after:avoid}table,img,.equation{break-inside:avoid}a{color:inherit;text-decoration:none}blockquote{font-size:12pt}img{max-height:22cm}thead{display:table-header-group}}
'''
contents='<details><summary>目录：讲稿、实验验收、数据与理论备稿</summary><nav aria-label="章节导航">'+''.join(toc)+'</nav></details>'
body=body.replace('<h2 ',contents+'<h2 ',1)
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>从节点影响到图遗忘响应 · 2026-10-05 研究讨论</title><style>'+style+'</style></head><body><header>OPENGU RESEARCH / 研究讨论 / 2026.10.05</header><main>'+body+'</main><footer>Markdown 原稿：REPORT.md · 图表由已核验实验输出生成</footer></body></html>'
(HERE/'REPORT.html').write_text(page,encoding='utf-8')

links=[]
for target in re.findall(r'\]\(([^)]+)\)',source):
    if target.startswith(('https://','http://','#')): continue
    path=(HERE/target.split('#')[0]).resolve()
    assert path.exists(),path
    links.append(str(path))
assert not re.search(r'<(?:script|link)\b',page)
assert 'src="assets/' not in page
assert 'FORMULA000TOKEN' not in page
audit={'date':'2026-10-06','EXP-011':audit11,'EXP-013':audit13,
       'gap_convention':'G = Retrain - GU; A = Random - selected; E = G_selected - G_random',
       'matching':'full output reference, selection_id, split and training seed checked',
       'summary_csv_reproduced':True,'all_report_local_links_exist':len(links),
       'printed_data_rows_checked':len(printed_rows),
       'workplan_status_records_checked':len(snapshot['experiments']),
       'offline_html':True,'formula_count':len(formulas),
       'source_sha256':sha(HERE/'REPORT.md'),
       'figure_sha256':{p.name:sha(p) for p in sorted(ASSETS.glob('[0-9][0-9]-*.png'))}}
(HERE/'validation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
