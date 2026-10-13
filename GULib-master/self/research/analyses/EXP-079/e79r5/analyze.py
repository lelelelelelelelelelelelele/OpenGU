"""Rebuild the EXP-079 scientific analysis from the trusted e79r5 return only."""
from pathlib import Path
import base64
from collections import Counter
import hashlib
import itertools
import json
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'results/runs/gpu4090/exp079-surrogate-multiseed/e79r5'
SHA = 'e02b5fa40ebce66fb45e57ea23b8d6c8d7856685'
JOB = 'exp079-20261013-e79r5'
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
METHODS = ['GNNDelete', 'GIF', 'IDEA', 'MEGU', 'GraphEraser', 'GraphRevoker']
SOURCES = ['GCN', 'SGC', 'GAT', 'GIN']
SELECTORS = ['r_point', 'gt_full']
COHORTS = {'new7': list(range(7)), 'old3': [42, 212, 2024], 'all10': [42, 212, 2024, *range(7)]}
KEY = ['dataset', 'method', 'seed']
GROUP = ['dataset', 'method', 'selector', 'source']

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_json(name, data):
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def table(df):
    def fmt(x):
        if isinstance(x, (float, np.floating)):
            return f'{x:.3f}' if np.isfinite(x) else 'NA'
        return str(x)
    return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(map(fmt, row))+' |' for row in df.itertuples(index=False, name=None))

def interval(v):
    v=np.asarray(v, dtype=float)
    mean=float(v.mean()); sd=float(v.std(ddof=1)); half=float(stats.t.ppf(.975, len(v)-1)*sd/np.sqrt(len(v)))
    return mean, sd, mean-half, mean+half

def rho(x,y):
    x=np.round(x,10);y=np.round(y,10)
    if np.ptp(x)<1e-10 or np.ptp(y)<1e-10:return np.nan
    return float(stats.spearmanr(x,y).statistic)

def load():
    delivery=read(ROOT/f'.syncmate/deliveries/{JOB}.json')
    result=delivery['result']; assert result['ok'] and result['gate_passed']
    assert result['project_acceptance']['passed'] and result['project_acceptance']['accepted_cells']==2520
    assert delivery['execution']['git_sha']==SHA
    prefix='results/runs/exp079-surrogate-multiseed/e79r5/'
    manifest=result['completed_job']['result']['manifest']
    expected={x['path']:x['sha256'] for x in manifest['artifacts']}
    index={x['path']:x for x in read(ROOT/'.syncmate/artifact_index.json')['peers']['gpu4090']['items']}
    assert len(expected)==5041 and manifest['status']=='verified'
    for path,sha in expected.items():
        assert path.startswith(prefix)
        local=BASE/path[len(prefix):]
        assert digest(local)==sha and index[path]['sha256']==sha
        assert (ROOT/index[path]['local_path']).resolve()==local.resolve()
    run=read(BASE/'run.json')
    assert run['commit']==SHA and run['status']=='completed' and len(run['cells'])==2520
    records=[];selections={};outputs={};producers=Counter()
    for c in run['cells']:
        assert c['status']=='completed'
        cond=c['conditions'];p=BASE/c['path']
        assert cond['budget_ratio']==.1 and cond['model']=='OpenGU.GCNNet'
        for name,info in c['files'].items():assert expected[prefix+c['path']+'/'+name]==info['sha256']
        met=read(p/'metrics.json');sel=read(p/'selection.json')
        assert met['cell_id']==sel['cell_id']==c['cell_id'] and sel['selection_id']==c['selection_id']
        nodes=frozenset(sel['selected_nodes']);assert len(nodes)==len(sel['selected_nodes'])==sel['requested_k']
        if c['selection_id'] in selections:assert selections[c['selection_id']]==nodes
        selections[c['selection_id']]=nodes
        stages={r['stage']:r for r in met['rows']};u=stages['utility']['values'];m=stages['method']['values']
        stem=Path(cond['selector_ref']).stem
        source=next((s for s in SOURCES[1:] if stem.endswith('_'+s.lower())), 'GCN') if cond['selector'] in SELECTORS else 'baseline'
        row=dict(cell_id=c['cell_id'],dataset=cond['dataset_name'],method=cond['method'],seed=cond['training_seed'],
                 random_seed=cond.get('random_selector_seed'),source=source,selector=cond['selector'],split=cond['dataset_fingerprint'],
                 selection_id=c['selection_id'],output_id=c['output']['artifact_id'],after=100*u['f1_after'],
                 before=None if u['f1_before'] is None else 100*u['f1_before'],
                 U=None if u['f1_before'] is None else 100*(u['f1_before']-u['f1_after']),G=None,flip=None,
                 update_detection_auc=m.get('update_detection_auc'),update_detection_auc_status=m.get('update_detection_auc_status'))
        if cond['method']!='Retrain':
            g=stages['post_unlearning_utility_and_retrain_gap'];f=stages['post_unlearning_flip_hop']
            assert g['baseline_output']==f['baseline_output']
            row.update(G=100*g['values']['gap'],retrain=100*g['values']['perf_retrain'],
                       baseline_id=g['baseline_output']['artifact_id'],flip=100*f['values']['fraction_flipped'])
            assert abs(row['G']-(row['retrain']-row['after']))<1e-8
        outputs[row['output_id']]=row
        records.append(row)
        producers.update(k for k,v in c['producer_called'].items() if v)
    df=pd.DataFrame(records)
    assert len(df.cell_id.unique())==2520 and set(df.seed)==set(COHORTS['all10'])
    assert df.groupby(['dataset','method','seed']).size().eq(12).all()
    assert df.groupby('dataset').split.nunique().eq(1).all()
    assert df.groupby(['dataset','seed','selector','source','random_seed'],dropna=False).selection_id.nunique().eq(1).all()
    random_rows=df[df.selector=='random']
    assert random_rows.groupby(KEY).random_seed.apply(lambda x:set(x)=={11,22,33}).all()
    for row in records:
        if row['method']=='Retrain':continue
        b=outputs[row['baseline_id']]
        assert b['method']=='Retrain' and all(b[k]==row[k] for k in ['dataset','seed','split','selection_id'])
        assert abs(b['after']-row['retrain'])<1e-8
    assert np.isfinite(df[df.method!='Retrain'][['U','G','flip']].to_numpy()).all()
    # Verify the old run's selected files before comparing reused scientific identities.
    oldbase=ROOT/'results/runs/gpu4090/exp013-surrogate-to-gcn/r1'
    oldrun=read(oldbase/'run.json');oldprefix='results/runs/exp013-surrogate-to-gcn/r1/'
    assert digest(oldbase/'run.json')==index[oldprefix+'run.json']['sha256']
    current={(r['dataset'],r['method'],r['seed'],r['selector'],r['source'],r['random_seed']):r for r in records};oldmatch=0
    for c in oldrun['cells']:
        co=c['conditions'];stem=Path(co['selector_ref']).stem
        source=next((s for s in SOURCES[1:] if stem.endswith('_'+s.lower())), 'GCN') if co['selector'] in SELECTORS else 'baseline'
        r=current[co['dataset_name'],co['method'],co['training_seed'],co['selector'],source,co.get('random_selector_seed')]
        assert r['split']==co['dataset_fingerprint']
        assert r['seed'] in COHORTS['old3'] and r['selection_id']==c['selection_id'] and r['output_id']==c['output']['artifact_id']
        for name,info in c['files'].items():assert digest(oldbase/c['path']/name)==info['sha256']==index[oldprefix+c['path']+'/'+name]['sha256']
        oldst={x['stage']:x for x in read(oldbase/c['path']/'metrics.json')['rows']}
        assert abs(r['after']-100*oldst['utility']['values']['f1_after'])<1e-8
        if r['method']!='Retrain':
            assert abs(r['U']-100*oldst['utility']['values']['f1_drop'])<1e-8
            assert abs(r['G']-100*oldst['post_unlearning_utility_and_retrain_gap']['values']['gap'])<1e-8
        oldmatch+=1
    assert oldmatch==756
    matchkeys=['dataset','seed','selector','source','random_seed']
    gi=df[df.method=='GIF'].merge(df[df.method=='IDEA'],on=matchkeys,suffixes=('_gif','_idea'),validate='one_to_one')
    gif_idea_diff=float(np.max(np.abs(gi.U_gif-gi.U_idea)))
    audit=dict(job_id=JOB,run_id='e79r5',execution_sha=SHA,config_path=run['config_path'],
               run_sha256=expected[prefix+'run.json'],verified_files=5041,cells=2520,paired_gu_cells=2160,
               old_run_sha=oldrun['commit'],old_cells_identity_and_metric_match=oldmatch,
               dataset_fingerprints=df.groupby('dataset').split.first().to_dict(),
               gif_idea_max_U_difference=gif_idea_diff,
               cache_counts={k:dict(Counter(c['cache'][k] for c in run['cells'] if k in c['cache'])) for k in run['cells'][0]['cache']},
               producer_called_counts=dict(producers),scientific_acceptance='not_requested',
               job_seconds=(datetime.fromisoformat(result['completed_job']['receipt']['finished_at'])-datetime.fromisoformat(result['completed_job']['receipt']['started_at'])).total_seconds(),selection_unique_ids=len(selections))
    write_json('audit.json',audit);df.to_csv(OUT/'cells.csv',index=False)
    return df,selections,audit

def paired(df):
    gu=df[df.method!='Retrain'].copy()
    random=gu[gu.selector=='random'].groupby(KEY)[['U','G','flip']].mean().add_suffix('_random').reset_index()
    degree=gu[gu.selector=='degree'][KEY+['U','G','flip']].rename(columns={k:k+'_degree' for k in ['U','G','flip']})
    direct=gu[gu.source=='GCN'][KEY+['selector','U','G','flip']].rename(columns={k:k+'_direct' for k in ['U','G','flip']})
    a=gu[gu.source.isin(SOURCES)].merge(random,on=KEY,validate='many_to_one').merge(degree,on=KEY,validate='many_to_one').merge(direct,on=KEY+['selector'],validate='many_to_one')
    for metric in ['U','G','flip']:
        for ref in ['direct','random','degree']:a[metric+'_vs_'+ref]=a[metric]-a[metric+'_'+ref]
    a.to_csv(OUT/'paired_seed_values.csv',index=False)
    rows=[]
    for cohort,seeds in COHORTS.items():
        for key,g in a[a.seed.isin(seeds)].groupby(GROUP):
            r=dict(zip(GROUP,key));r.update(cohort=cohort,n=len(g))
            for metric in ['U','G','flip','U_vs_direct','U_vs_random','U_vs_degree','G_vs_direct','G_vs_random']:
                for label,value in zip(['mean','sd','lo','hi'],interval(g[metric])):r[metric+'_'+label]=value
            r['paired_MAE_direct']=float(np.abs(g.U_vs_direct).mean())
            # Optional scale diagnostic from the earlier proposal; not a confirmatory endpoint.
            x=(g.U_direct-g.U_random).to_numpy();y=g.U_vs_random.to_numpy()
            xm,_,xl,xh=interval(x);ym=float(y.mean());n=len(x)
            r.update(direct_random_mean=xm,direct_random_lo=xl,direct_random_hi=xh,retention=np.nan,retention_lo=np.nan,retention_hi=np.nan,retention_status='reference_not_established')
            if xl>0:
                vxx,vxy,vyy=np.var(x,ddof=1)/n,np.cov(x,y,ddof=1)[0,1]/n,np.var(y,ddof=1)/n
                t2=stats.t.ppf(.975,n-1)**2
                aa=xm*xm-t2*vxx;bb=-2*(xm*ym-t2*vxy);cc=ym*ym-t2*vyy
                disc=bb*bb-4*aa*cc
                assert aa>0 and disc>=-1e-10
                roots=sorted([(-bb-np.sqrt(max(0,disc)))/(2*aa),(-bb+np.sqrt(max(0,disc)))/(2*aa)])
                r.update(retention=ym/xm,retention_lo=roots[0],retention_hi=roots[1],retention_status='exploratory_finite')
            for ref in ['random','degree']:r['wins_vs_'+ref]=int((g['U_vs_'+ref]>1e-10).sum())
            rows.append(r)
    summary=pd.DataFrame(rows);summary.to_csv(OUT/'summary.csv',index=False)
    return a,summary

def correlations(a,dedup):
    rows=[];rng=np.random.default_rng(79014)
    methods=[m for m in METHODS if not (dedup and m=='IDEA')]
    for cohort,seeds in COHORTS.items():
        for (d,sel),g in a[a.seed.isin(seeds)].groupby(['dataset','selector']):
            direct=g[g.source=='GCN'].pivot(index='seed',columns='method',values='U').reindex(index=seeds,columns=methods).to_numpy()
            ran=g[g.source=='GCN'].pivot(index='seed',columns='method',values='U_random').reindex(index=seeds,columns=methods).to_numpy()
            deg=g[g.source=='GCN'].pivot(index='seed',columns='method',values='U_degree').reindex(index=seeds,columns=methods).to_numpy()
            for src in SOURCES[1:]:
                sur=g[g.source==src].pivot(index='seed',columns='method',values='U').reindex(index=seeds,columns=methods).to_numpy()
                boot=[]
                for ids in rng.integers(0,len(seeds),size=(2000,len(seeds))):boot.append(rho(direct[ids].mean(0),sur[ids].mean(0)))
                valid=np.array(boot);valid=valid[np.isfinite(valid)]
                rows.append(dict(cohort=cohort,dataset=d,selector=sel,source=src,n_methods=len(methods),
                                 rho=rho(direct.mean(0),sur.mean(0)),rho_random=rho(direct.mean(0),ran.mean(0)),
                                 rho_degree=rho(direct.mean(0),deg.mean(0)),rho_random_adjusted=rho((direct-ran).mean(0),(sur-ran).mean(0)),
                                 bootstrap_lo=float(np.quantile(valid,.025)),bootstrap_hi=float(np.quantile(valid,.975)),
                                 bootstrap_undefined=2000-len(valid)))
    out=pd.DataFrame(rows);out.to_csv(OUT/'correlations.csv',index=False);return out

def overlap(df,selections):
    rows=[];within=[]
    def jac(x,y):return len(x&y)/len(x|y)
    # Select one GU to avoid counting identical selections seven times.
    q=df[(df.method=='GNNDelete') & df.source.isin(SOURCES)]
    lookup={(r.dataset,r.selector,r.source,r.seed):selections[r.selection_id] for r in q.itertuples()}
    for cohort,seeds in COHORTS.items():
        for d,sel in itertools.product(DATASETS,SELECTORS):
            for src in SOURCES[1:]:
                vals=[jac(lookup[d,sel,'GCN',s],lookup[d,sel,src,s]) for s in seeds]
                rows.append(dict(cohort=cohort,dataset=d,selector=sel,source=src,mean=np.mean(vals),sd=np.std(vals,ddof=1),min=min(vals),max=max(vals)))
            for src in SOURCES:
                vals=[jac(lookup[d,sel,src,s],lookup[d,sel,src,t]) for s,t in itertools.combinations(seeds,2)]
                within.append(dict(cohort=cohort,dataset=d,selector=sel,source=src,mean=np.mean(vals),min=min(vals),max=max(vals),pairs=len(vals)))
    cross=pd.DataFrame(rows);cross.to_csv(OUT/'selection_overlap.csv',index=False)
    pd.DataFrame(within).to_csv(OUT/'within_source_overlap.csv',index=False)
    return cross,pd.DataFrame(within)

def figures(a,summary):
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    colors=['#255b94','#db7226','#329075','#994f9c']
    for selector in SELECTORS:
        fig,axes=plt.subplots(3,6,figsize=(22,10),layout='constrained')
        for i,d in enumerate(DATASETS):
            for j,m in enumerate(METHODS):
                ax=axes[i,j];g=a[(a.dataset==d)&(a.method==m)&(a.selector==selector)]
                for k,src in enumerate(SOURCES):
                    z=g[g.source==src].sort_values('seed');mu,sd,lo,hi=interval(z.U)
                    ax.scatter(k+np.linspace(-.1,.1,10),z.U,s=15,c=[colors[k] if s in range(7) else '#aab1ba' for s in z.seed],alpha=.7)
                    ax.errorbar(k,mu,yerr=[[mu-lo],[hi-mu]],fmt='D',color=colors[k],capsize=3,ms=4)
                ax.axhline(g.U_random.mean(),color='#444',ls='--',label='Random')
                ax.axhline(g.U_degree.mean(),color='#b68b21',ls=':',label='Degree')
                ax.axhline(0,color='#bbb',lw=.7);ax.set_xticks(range(4),SOURCES);ax.set_title(d+' / '+m)
                if j==0:ax.set_ylabel('F1 drop (pp)')
                ax.grid(axis='y',alpha=.15)
        fig.suptitle(selector+' | 10 training seeds, fixed split, deletion ratio 0.1\nDiamond: mean; bar: pointwise 95% t CI; dots: seeds (gray = original 3); dashed: Random; dotted: Degree. Each panel has its own scale.',fontsize=13)
        fig.savefig(OUT/f'{selector}_drop.png',dpi=155);plt.close(fig)
    focus=summary[(summary.cohort=='all10') & (summary.source=='GIN')]
    fig,axes=plt.subplots(1,3,figsize=(15,7),layout='constrained')
    labels=[f'{s}/{m}' for s in SELECTORS for m in METHODS]
    for ax,d in zip(axes,DATASETS):
        for shift,ref,color in [(-.18,'direct','#255b94'),(0,'random','#329075'),(.18,'degree','#db7226')]:
            g=focus[focus.dataset==d].set_index(['selector','method']).reindex(list(itertools.product(SELECTORS,METHODS)))
            mu=g['U_vs_'+ref+'_mean'];lo=g['U_vs_'+ref+'_lo'];hi=g['U_vs_'+ref+'_hi']
            ax.errorbar(mu,np.arange(12)+shift,xerr=[mu-lo,hi-mu],fmt='o',ms=3,capsize=2,label='GIN - '+ref,color=color)
        ax.set_yticks(range(12),labels);ax.invert_yaxis();ax.axvline(0,c='#333',lw=.8);ax.set_title(d);ax.set_xlabel('Paired F1-drop difference (pp)');ax.grid(axis='x',alpha=.15)
    axes[0].legend(loc='upper left',bbox_to_anchor=(0,-.12),ncol=3,fontsize=8)
    fig.suptitle('GIN transfer contrasts | 10 seeds | pointwise 95% paired t intervals\nPositive = larger utility loss; zero-crossing does not establish equivalence.',fontsize=13)
    fig.savefig(OUT/'gin_contrasts.png',dpi=160);plt.close(fig)

def main():
    df,selections,audit=load();a,s=paired(df)
    corr=correlations(a,audit['gif_idea_max_U_difference']<1e-10)
    overlap(df,selections);figures(a,s)
    from report import build_report
    build_report()
    print(json.dumps(audit,ensure_ascii=False,indent=2))
    focus=s[(s.dataset=='Cora')&(s.method=='GNNDelete')&(s.selector=='gt_full')&(s.source=='GIN')]
    print(focus[['cohort','U_mean','U_vs_direct_mean','U_vs_direct_lo','U_vs_direct_hi','U_vs_random_mean','U_vs_random_lo','U_vs_random_hi','U_vs_degree_mean','U_vs_degree_lo','U_vs_degree_hi']].to_string(index=False))

if __name__=='__main__':main()
