"""Offline, identity-checked figure refresh for EXP-011/e11r1 and EXP-079/e79r6.

Run with the project Python from any directory. No training or cache mutation.
The raw-endpoint layout follows the historical q2-metrics/build_primary.py.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import t

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SHA = 'bab1781e182254e0b02cbeb1de138d58f7f1cd50'
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
METHODS = ['Retrain', 'GNNDelete', 'GIF', 'IDEA', 'MEGU', 'GraphEraser', 'GraphRevoker']
PANELS = ['Retrain', 'GNNDelete', 'GIF', 'MEGU', 'GraphEraser', 'GraphRevoker']
SOURCES = ['GCN', 'SGC', 'GAT', 'GIN']
REQUESTS = ['random', 'degree', 'r_point', 'gt_full']
REQUESTS11 = REQUESTS + ['pagerank', 'rr_4096', 'rr_16384', 'rr_65536']
LABELS = dict(zip(REQUESTS11, ['Random', 'Degree', 'R-point', 'D-full', 'PageRank', 'IM 4k', 'IM 16k', 'IM 65k']))
COLORS = dict(zip(REQUESTS11, ['#80909c', '#ca942e', '#288b87', '#ae5b85', '#6683ae', '#7766a0', '#8b724f', '#5e9369']))
SPECS = {'EXP-011': ('exp011-t2', 'e11r1', 'exp011-20261023-e11r1', 1449, 3, '0925-v1'),
         'EXP-079': ('exp079-surrogate-multiseed', 'e79r6', 'exp079-20261023-e79r6', 2520, 10, 'e79r5')}
METRICS = ['after', 'before', 'CE', 'AUC', 'U', 'G', 'flip']
GROUP = ['experiment', 'dataset', 'method', 'source', 'selector']
KEY = ['dataset', 'method', 'seed']


def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
def save(name, df): df.to_csv(OUT/name, index=False, encoding='utf-8')


def ci(values):
    a = np.asarray(values, float)
    assert len(a) > 1 and np.isfinite(a).all()
    m, sd = float(a.mean()), float(a.std(ddof=1))
    h = float(t.ppf(.975, len(a)-1)*sd/np.sqrt(len(a)))
    return dict(mean=m, sd=sd, lo=m-h, hi=m+h, n=len(a))


def load_run(exp, rid, trusted=True):
    experiment, current, job, count, nseed, _ = SPECS[exp]
    base = ROOT/'results/runs/gpu4090'/experiment/rid
    prefix = f'results/runs/{experiment}/{rid}/'
    idx = {i['path']: i for i in read(ROOT/'.syncmate/artifact_index.json')['peers']['gpu4090']['items']}
    runpath = base/'run.json'
    assert sha(runpath) == idx[prefix+'run.json']['sha256']
    run = read(runpath)
    assert run['status'] == 'completed' and len(run['cells']) == count
    assert run['run_id'] == rid
    if trusted:
        delivery = read(ROOT/f'.syncmate/deliveries/{job}.json')
        result = delivery['result']
        assert result['ok'] and result['gate_passed'] and result['project_acceptance']['passed']
        assert result['project_acceptance']['accepted_cells'] == count
        assert delivery['execution']['git_sha'] == run['commit'] == SHA
        manifest = result['completed_job']['result']['manifest']
        assert manifest['status'] == 'verified'
        expected = {a['path']: a['sha256'] for a in manifest['artifacts']}
        assert len(expected) == 2*count+1
        assert expected[prefix+'run.json'] == sha(runpath)
    else:
        expected = {prefix+'run.json': sha(runpath)}
        for c in run['cells']:
            expected.update({prefix+c['path']+'/'+n: v['sha256'] for n, v in c['files'].items()})
    rows = []
    selected = {}
    for c in run['cells']:
        assert c['status'] == 'completed'
        for name, info in c['files'].items():
            path = prefix+c['path']+'/'+name
            p = base/c['path']/name
            assert sha(p) == info['sha256'] == expected[path] == idx[path]['sha256']
            assert (ROOT/idx[path]['local_path']).resolve() == p.resolve()
        co = c['conditions']
        assert co['budget_ratio'] == .1 and co['model'] == 'OpenGU.GCNNet'
        met = read(base/c['path']/'metrics.json')
        sel = read(base/c['path']/'selection.json')
        assert met['cell_id'] == sel['cell_id'] == c['cell_id']
        assert sel['selection_id'] == c['selection_id']
        nodes = tuple(sorted(sel['selected_nodes']))
        assert len(set(nodes)) == len(nodes) == sel['requested_k']
        assert selected.setdefault(c['selection_id'], nodes) == nodes
        stages = {s['stage']: s for s in met['rows']}
        u, m = stages['utility']['values'], stages['method']['values']
        assert abs(m['accuracy']-m['f1']) < 1e-12 and abs(m['accuracy']-u['f1_after']) < 1e-12
        stem = Path(co['selector_ref']).stem
        source = next((s for s in SOURCES[1:] if stem.endswith('_'+s.lower())), 'GCN') if co['selector'] in ['r_point', 'gt_full'] else 'baseline'
        selector = stem if exp == 'EXP-011' else co['selector']
        r = dict(experiment=exp, run_id=rid, cell_id=c['cell_id'], dataset=co['dataset_name'],
                 method=co['method'], seed=co['training_seed'], source=source, selector=selector,
                 random_seed=co.get('random_selector_seed'), im_seed=co.get('im_selector_seed'),
                 selection_id=c['selection_id'], split=co['dataset_fingerprint'],
                 output_id=c['output']['artifact_id'], output_hash=c['output']['content_hash'],
                 after=100*m['accuracy'], CE=m['cross_entropy'], AUC=100*m['classification_auc'],
                 before=None if u['f1_before'] is None else 100*u['f1_before'],
                 U=None if u['f1_before'] is None else 100*u['f1_drop'], G=None, flip=None,
                 baseline_id=None, output_cache=c['cache']['method'])
        assert m['classification_auc_status'] == 'computed'
        if co['method'] != 'Retrain':
            g, f = stages['post_unlearning_utility_and_retrain_gap'], stages['post_unlearning_flip_hop']
            assert g['baseline_output'] == f['baseline_output']
            assert f['identity']['protocol']['evaluation_mask'] == 'test_mask_excluding_selected_nodes'
            assert f['identity']['protocol']['comparison'] == 'argmax_gu_vs_same_request_retrain_first_index_ties'
            r.update(G=100*g['values']['gap'], flip=100*f['values']['fraction_flipped'], baseline_id=g['baseline_output']['artifact_id'])
            assert abs(r['G']-(100*g['values']['perf_retrain']-r['after'])) < 1e-8
        rows.append(r)
    df = pd.DataFrame(rows)
    assert df.cell_id.is_unique and set(df.method) == set(METHODS)
    assert df.groupby('dataset').split.nunique().eq(1).all()
    seeds = {42, 212, 2024} if nseed == 3 else {42, 212, 2024, *range(7)}
    assert set(df.seed) == seeds
    assert df.groupby(KEY).size().eq(23 if nseed == 3 else 12).all()
    outputs = {r['output_id']: r for r in rows}
    for r in rows:
        if r['method'] == 'Retrain': continue
        b = outputs[r['baseline_id']]
        assert b['method'] == 'Retrain'
        assert all(b[k] == r[k] for k in ['dataset', 'seed', 'split', 'selection_id'])
        assert abs(r['G'] - (b['after']-r['after'])) < 1e-8
    for method in METHODS:
        sub = df[df.method.eq(method) & df.selector.eq('random')]
        assert sub.groupby(['dataset','seed']).size().eq(10 if nseed == 3 else 3).all()
    if nseed == 3:
        assert df[df.selector.str.startswith('rr_')].groupby(['dataset','method','seed','selector']).size().eq(3).all()
    assert np.isfinite(df[['after','CE','AUC']].to_numpy()).all()
    assert df[df.method != 'Retrain'].groupby(KEY).before.apply(lambda x: np.ptp(x) < 1e-8).all()
    proof = dict(experiment=exp, run_id=rid, execution_sha=run['commit'], cells=len(df),
                 paired_gu_cells=int((df.method != 'Retrain').sum()), verified_files=len(expected),
                 manifest=str(runpath.relative_to(ROOT)).replace('\\','/'), manifest_sha256=sha(runpath),
                 unique_selection_ids=len(selected), training_seeds=sorted(seeds),
                 cache={k:dict(Counter(c['cache'].get(k,'not_recorded') for c in run['cells'])) for k in run['cells'][0]['cache']},
                 checks='SHA256 + trusted index + '+('delivery/current run + ' if trusted else 'historical manifest + ')+'dataset/seed/selection matched Retrain',
                 scientific_acceptance='not_requested')
    return df, proof


def aggregate(df):
    # One observational unit per training seed: average selection repetitions inside it.
    s = df.groupby(GROUP+['seed'], dropna=False)[METRICS].mean().reset_index()
    sizes = df.groupby(GROUP+['seed'], dropna=False).size().rename('selection_repeats').reset_index()
    s = s.merge(sizes, on=GROUP+['seed'], validate='one_to_one')
    sums = []
    for key, g in s.groupby(GROUP):
        for metric in METRICS:
            if g[metric].isna().all(): continue
            sums.append(dict(zip(GROUP,key), metric=metric, **ci(g[metric])))
    random = s[s.selector.eq('random')][['experiment']+KEY+METRICS].rename(columns={m:m+'_random' for m in METRICS})
    paired = s.merge(random, on=['experiment']+KEY, validate='many_to_one')
    for metric in METRICS:
        paired[metric+'_minus_random'] = paired[metric]-paired[metric+'_random']
    effects = []
    for key, g in paired.groupby(GROUP):
        for metric in METRICS:
            col = metric+'_minus_random'
            if g[col].isna().all(): continue
            effects.append(dict(zip(GROUP,key), metric=metric, **ci(g[col])))
    return s, pd.DataFrame(sums), paired, pd.DataFrame(effects)


def compare(old, new):
    keys = ['dataset','method','seed','source','selector','random_seed','im_seed']
    merged = old.merge(new, on=keys, suffixes=('_old','_new'), validate='one_to_one')
    assert len(merged) == len(new)
    assert (merged.selection_id_old == merged.selection_id_new).all()
    assert (merged.split_old == merged.split_new).all()
    nons = ~merged.method.isin(['GraphEraser','GraphRevoker'])
    assert (merged.loc[nons,'output_id_old'] == merged.loc[nons,'output_id_new']).all()
    for metric in ['after','before','CE','AUC','U','G','flip']:
        assert np.allclose(merged.loc[nons,metric+'_old'], merged.loc[nons,metric+'_new'], equal_nan=True, atol=1e-8, rtol=0)
        merged[metric+'_new_minus_old'] = merged[metric+'_new']-merged[metric+'_old']
    return merged


def main_data():
    all_rows, old_rows, proofs, comparisons = [], [], {}, []
    for exp, spec in SPECS.items():
        new, proof = load_run(exp, spec[1]); old, oldproof = load_run(exp, spec[-1], trusted=False)
        all_rows.append(new); old_rows.append(old); proofs[exp] = dict(current=proof,historical=oldproof)
        comparisons.append(compare(old,new))
    df, old = pd.concat(all_rows,ignore_index=True), pd.concat(old_rows,ignore_index=True)
    seed, summary, paired, effects = aggregate(df)
    oldseed, oldsummary, _, _ = aggregate(old)
    gif = seed[seed.method.eq('GIF')].merge(seed[seed.method.eq('IDEA')],on=['experiment','dataset','seed','source','selector'],suffixes=('_gif','_idea'),validate='one_to_one')
    diffs = {m:float((gif[m+'_gif']-gif[m+'_idea']).abs().max()) for m in ['after','CE','AUC']}
    assert diffs['after'] == 0 and diffs['CE'] < 2e-8 and diffs['AUC'] < .001
    proofs['gif_idea_max_differences'] = diffs
    proofs['non_shard_outputs_and_metrics_unchanged'] = True
    proofs['statistical_unit'] = 'training seed after averaging selection repetitions within seed; pointwise two-sided 95% t CI; no multiplicity correction'
    save('cells.csv',df); save('seed_values.csv',seed); save('summary.csv',summary)
    save('paired_seed_values.csv',paired); save('paired_vs_random.csv',effects)
    save('historical_seed_values.csv',oldseed); save('historical_summary.csv',oldsummary)
    save('old_new_matched_cells.csv',pd.concat(comparisons,ignore_index=True))
    dump('input_audit.json', proofs)
    print(json.dumps(proofs,ensure_ascii=False))
    return seed, summary, paired, effects, oldseed, oldsummary


def export(fig, name):
    for ext in ['png', 'pdf', 'svg']:
        path = OUT/f'{name}.{ext}'
        fig.savefig(path, dpi=180, facecolor='white')
        if ext == 'svg':
            normalize_svg(path)
    plt.close(fig)


def normalize_svg(path):
    path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')


def style():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10, 'text.color':'#253c49',
        'axes.labelcolor':'#253c49','xtick.color':'#526773','ytick.color':'#526773',
        'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})


def decorate(ax):
    ax.grid(axis='y',color='#e5edf0',lw=.7)
    ax.set_axisbelow(True)


def point(ax, x, r, color, marker='o', hollow=False):
    ax.errorbar(x, r['mean'], yerr=[[max(0,r['mean']-r['lo'])],[max(0,r['hi']-r['mean'])]],
                fmt=marker, color=color, mfc='white' if hollow else color, ms=6,
                capsize=3, lw=1.2,zorder=4)


def raw_figures(seed, summary):
    specs = {'after':('Test accuracy (%)','higher is better','accuracy'),
             'CE':('Test cross-entropy','lower is better','ce'),
             'AUC':('Classification macro OvR AUC (%)','higher is better','auc')}
    for exp, spec in SPECS.items():
        rid, n = spec[1], spec[4]
        selectors = REQUESTS if n == 10 else REQUESTS11
        v = seed[seed.experiment.eq(exp) & seed.source.isin(['GCN','baseline'])]
        ss = summary[summary.experiment.eq(exp) & summary.source.isin(['GCN','baseline'])]
        indexed = ss.set_index(['dataset','method','selector','metric'])
        for ds in DATASETS:
            for metric, (ylabel,direction,suffix) in specs.items():
                fig, axes = plt.subplots(2,3,figsize=(15.5,9.6))
                main = v[v.dataset.eq(ds) & ~v.method.isin(['GraphRevoker','IDEA'])]
                summ = ss[ss.dataset.eq(ds) & ss.metric.eq(metric) & ~ss.method.isin(['GraphRevoker','IDEA'])]
                low, high = min(main[metric].min(),summ.lo.min()),max(main[metric].max(),summ.hi.max())
                if metric == 'after': low,high = min(low,main.before.min()),max(high,main.before.max())
                pad = max((high-low)*.13,.002 if metric=='CE' else .05)
                for ax, method in zip(axes.flat,PANELS):
                    sub = v[v.dataset.eq(ds) & v.method.eq(method)]
                    ax.set_title('GIF / IDEA' if method=='GIF' else method,loc='left',fontweight='bold',fontsize=12)
                    decorate(ax)
                    if method != 'GraphRevoker': ax.set_ylim(low-pad,high+pad)
                    else: ax.set_facecolor('#f5f5f5');ax.margins(y=.22)
                    for j, selector in enumerate(selectors):
                        g=sub[sub.selector.eq(selector)].sort_values('seed')
                        assert len(g)==n
                        x=j if method=='Retrain' else j-.10
                        ax.scatter(x+np.linspace(-.065,.065,n),g[metric],s=16,color=COLORS[selector],alpha=.32,edgecolors='none')
                        r=indexed.loc[ds,method,selector,metric]
                        point(ax,x,r,COLORS[selector],marker='D' if method=='Retrain' else 'o',hollow=method=='Retrain')
                        if method!='Retrain':
                            b=indexed.loc[ds,'Retrain',selector,metric]
                            ax.plot([x,j+.10],[r['mean'],b['mean']],color=COLORS[selector],lw=1,alpha=.5)
                            point(ax,j+.10,b,COLORS[selector],marker='D',hollow=True)
                    if metric=='after':
                        text='Before: not recorded'
                        if method!='Retrain':
                            before=sub[sub.selector.eq('random')].before.mean()
                            ax.axhline(before,color='#7a8790',ls='--',lw=1)
                            text=f'Before mean: {before:.2f}%'
                        ax.text(.98,.97,text,transform=ax.transAxes,ha='right',va='top',fontsize=9,color='#66737a')
                    ax.set_xticks(range(len(selectors)))
                    ax.set_xticklabels([LABELS[s] for s in selectors],rotation=25 if n==3 else 0,ha='right' if n==3 else 'center')
                    ax.set_xlim(-.45,len(selectors)-.55)
                    ax.set_ylabel(ylabel)
                fig.suptitle(f'{ds} | {ylabel} under {"four" if n==10 else "eight"} deletion requests',x=.065,ha='left',fontsize=18,fontweight='bold')
                fig.text(.065,.925,f'{exp} / {rid}  |  Raw endpoints: {direction}. No subtraction of Random or Retrain.',fontsize=11)
                fig.legend(handles=[plt.Line2D([],[],marker='o',ls='',color='#526773',label='GU'),
                    plt.Line2D([],[],marker='D',ls='',color='#526773',mfc='white',label='Same-request Retrain'),
                    plt.Line2D([],[],color='#7a8790',ls='--',label='GU Before mean (accuracy only)')],loc='upper center',bbox_to_anchor=(.52,.90),ncol=3,frameon=False)
                fig.text(.065,.025,f'Faint dots: {n} training-seed means. Large dots: means; bars: pointwise 95% t intervals. Selection repeats averaged within each seed.\n'
                    'Same-request Retrain is repeated for comparison. First five panels share a y scale; GraphRevoker has its own scale.\n'
                    'GIF represents the verified overlapping GIF / IDEA task-metric coordinates. Full values and SD are in the accompanying CSV.',fontsize=9,color='#526773')
                fig.subplots_adjust(left=.065,right=.985,top=.82,bottom=.16 if n==3 else .14,wspace=.29,hspace=.44 if n==3 else .36)
                export(fig,f'{rid}_{ds.lower()}_{suffix}')


def contrast_figures(effects, summary):
    # Raw within-request GU/Retrain gap and disagreement complement paired Random contrasts.
    for exp,spec in SPECS.items():
        sels=REQUESTS if spec[4]==10 else REQUESTS11
        es=effects[effects.experiment.eq(exp)&effects.source.isin(['GCN','baseline'])]
        ss=summary[summary.experiment.eq(exp)&summary.source.isin(['GCN','baseline'])]
        for ds in DATASETS:
            fig,axs=plt.subplots(1,3,figsize=(18,7))
            for ax,metric,title in zip(axs,['after','G','flip'],['Accuracy: Selected - Random (pp)','Retrain - GU accuracy (pp)','GU / Retrain disagreement (%)']):
                table=es if metric=='after' else ss
                methods=PANELS[1:]
                sub=table[table.dataset.eq(ds)&table.metric.eq(metric)]
                mat=np.array([[sub[sub.method.eq(m)&sub.selector.eq(s)]['mean'].iloc[0] for m in methods] for s in sels])
                lim=max(.1,float(abs(mat).max()))
                im=ax.imshow(mat,aspect='auto',cmap='YlOrRd' if metric=='flip' else 'RdBu_r',vmin=0 if metric=='flip' else -lim,vmax=lim)
                ax.set_title(title,fontsize=11,fontweight='bold')
                ax.set_xticks(range(5));ax.set_xticklabels(['GNNDelete','GIF / IDEA','MEGU','GraphEraser','GraphRevoker'],rotation=35,ha='right')
                ax.set_yticks(range(len(sels)));ax.set_yticklabels([LABELS[s] for s in sels])
                for i,s in enumerate(sels):
                    for j,m in enumerate(methods):
                        r=sub[sub.method.eq(m)&sub.selector.eq(s)].iloc[0]
                        mark='*' if metric=='after' and (r.lo>0 or r.hi<0) else ''
                        ax.text(j,i,f'{mat[i,j]:.2f}{mark}',ha='center',va='center',fontsize=9,color='white' if abs(mat[i,j])>lim*.65 else '#243642')
                fig.colorbar(im,ax=ax,fraction=.045,pad=.03)
            fig.suptitle(f'{exp} / {spec[1]} | {ds} | Request contrasts and matched-Retrain diagnostics',fontsize=15,fontweight='bold')
            fig.text(.06,.025,'* Selected - Random pointwise 95% paired t interval excludes zero; exploratory, no multiple-comparison correction.\n'
                     'Positive accuracy contrast = higher accuracy; positive Retrain - GU = GU below Retrain. Disagreement is not forgetting correctness.',fontsize=10)
            fig.subplots_adjust(left=.065,right=.97,top=.85,bottom=.23,wspace=.38)
            export(fig,f'{spec[1]}_{ds.lower()}_contrasts')


def protocol_comparison(seed, oldseed):
    rows=[]
    for exp,spec in SPECS.items():
        v=seed[seed.experiment.eq(exp)&seed.source.isin(['GCN','baseline'])]
        old=oldseed[oldseed.experiment.eq(exp)&oldseed.source.isin(['GCN','baseline'])]
        sels=REQUESTS if spec[4]==10 else REQUESTS11
        z=old.merge(v,on=GROUP+['seed'],suffixes=('_old','_new'),validate='one_to_one')
        for key,g in z.groupby(GROUP):
            for metric in ['after','before','G','flip']:
                if g[metric+'_old'].isna().all():continue
                rows.append(dict(zip(GROUP,key),metric=metric,**ci(g[metric+'_new']-g[metric+'_old'])))
        fig,axs=plt.subplots(3,2,figsize=(14,12))
        for i,ds in enumerate(DATASETS):
            for j,m in enumerate(['GraphEraser','GraphRevoker']):
                ax=axs[i,j];decorate(ax)
                for frame,label,color,dx in [(old,'Previous protocol','#929ba2',-.08),(v,'New loss / shard 300','#157f81',.08)]:
                    means=[]
                    for k,s in enumerate(sels):
                        r=ci(frame[frame.dataset.eq(ds)&frame.method.eq(m)&frame.selector.eq(s)].after)
                        point(ax,k+dx,r,color);means.append(r['mean'])
                    ax.plot(np.arange(len(sels))+dx,means,color=color,lw=.7,alpha=.6,label=label)
                ax.set_title(f'{ds} | {m}',loc='left',fontweight='bold')
                ax.set_xticks(range(len(sels)));ax.set_xticklabels([LABELS[s] for s in sels],rotation=25 if spec[4]==3 else 0)
                ax.set_ylabel('Test accuracy (%)');ax.legend(fontsize=8)
        fig.suptitle(f'{exp} | Matched requests, previous vs current protocol',fontsize=17,fontweight='bold')
        fig.text(.065,.025,'Both loss implementation and shard epochs changed. This comparison is not an isolated epoch ablation.\n'
                 'Pointwise 95% t intervals over training-seed means; original runs remain unchanged.',fontsize=10)
        fig.subplots_adjust(top=.93,bottom=.12,hspace=.4,wspace=.23)
        export(fig,spec[1]+'_protocol_comparison')
    save('protocol_change_paired.csv',pd.DataFrame(rows))


def response_refresh(seed):
    # Reuse the reviewed descriptive/statistical functions; do not run its old-data loader or old narrative.
    import importlib.util
    path=ROOT/'self/research/analyses/EXP-079/e79r5/response_pattern.py'
    spec=importlib.util.spec_from_file_location('frozen_response_analysis',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.OUT=OUT
    profiles=seed[seed.experiment.eq('EXP-079')&seed.method.ne('Retrain')].copy()
    save('response_seed_profiles.csv',profiles)
    summary,contrasts,margins,distances=module.analyze(profiles)
    module.figures(profiles,summary,contrasts,margins,distances)
    dump('response_generator_binding.json',dict(generator=str(path.relative_to(ROOT)).replace('\\','/'),sha256=sha(path),
        input='response_seed_profiles.csv',input_sha256=sha(OUT/'response_seed_profiles.csv'),run_id='e79r6',
        execution_sha=SHA, old_loader_called=False, old_narrative_reused=False))


if __name__ == '__main__':
    if '--figures-only' in sys.argv:
        seed,summary,paired,effects,oldseed,oldsummary=[pd.read_csv(OUT/name) for name in
            ['seed_values.csv','summary.csv','paired_seed_values.csv','paired_vs_random.csv','historical_seed_values.csv','historical_summary.csv']]
        # Cached analysis inputs must still match the preceding verified build.
        binding=read(OUT/'derived_data_hashes.json')
        assert all(sha(OUT/name)==digest for name,digest in binding.items())
    else:
        seed,summary,paired,effects,oldseed,oldsummary=main_data()
        dump('derived_data_hashes.json',{p.name:sha(p) for p in OUT.glob('*.csv')})
    style()
    raw_figures(seed,summary)
    contrast_figures(effects,summary)
    protocol_comparison(seed,oldseed)
    response_refresh(seed)
    print('Figures refreshed from the two verified current runs.')
