"""Frozen EXP-079 response-profile analysis. Read raw returns; never run models.

python -B -X utf8 self/research/analyses/EXP-079/e79r5/response_pattern.py
Outputs are prefixed response_; report rendering is in response_pattern_report.py.
"""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import subprocess
import sys
import numpy as np
import pandas as pd
from scipy import stats
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
RUN = ROOT/'results/runs/gpu4090/exp079-surrogate-multiseed/e79r5'
SHA = 'e02b5fa40ebce66fb45e57ea23b8d6c8d7856685'
JOB = 'exp079-20261013-e79r5'
SEEDS = [42, 212, 2024, *range(7)]
DS = ['Cora', 'CiteSeer', 'PubMed']
SRC = ['GCN', 'SGC', 'GAT', 'GIN']
SEL = ['gt_full', 'r_point']
GU = ['GNNDelete', 'GIF', 'IDEA', 'MEGU', 'GraphEraser', 'GraphRevoker']
MAIN = [g for g in GU if g != 'IDEA']
CONDS = [(s,a) for s in SEL for a in SRC]+[('degree','baseline'),('random','baseline')]
LABELS = [f'{s} / {a}' if a != 'baseline' else s.title() for s,a in CONDS]
COLORS = ['#2055a5','#a56b12','#168a7c','#ba4976']

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def save(name, df): df.to_csv(OUT/name,index=False,encoding='utf-8')
def interval(v):
    v=np.asarray(v,float); assert len(v)==10 and np.isfinite(v).all()
    m=v.mean(); h=stats.t.ppf(.975,9)*v.std(ddof=1)/np.sqrt(10)
    p=1. if np.allclose(v,0,atol=1e-12) else (0. if v.std(ddof=1)<1e-12 else stats.ttest_1samp(v,0).pvalue)
    return dict(mean=float(m),lo=float(m-h),hi=float(m+h),p=float(p),n=10)
def holm(p):
    p=np.asarray(p,float); ix=np.argsort(p); ans=np.empty_like(p)
    ans[ix]=np.minimum(1,np.maximum.accumulate(p[ix]*np.arange(len(p),0,-1)))
    return ans
def center(x): return x-x.mean(axis=-1,keepdims=True)

def audit_inputs():
    delivery=read(ROOT/f'.syncmate/deliveries/{JOB}.json')
    result=delivery['result']
    assert result['ok'] and result['gate_passed'] and result['project_acceptance']['passed']
    assert result['project_acceptance']['accepted_cells']==2520
    assert delivery['execution']['git_sha']==SHA
    manifest=result['completed_job']['result']['manifest']
    expected={x['path']:x['sha256'] for x in manifest['artifacts']}
    index={x['path']:x for x in read(ROOT/'.syncmate/artifact_index.json')['peers']['gpu4090']['items']}
    prefix='results/runs/exp079-surrogate-multiseed/e79r5/'
    assert len(expected)==5041 and manifest['status']=='verified'
    for path,sha in expected.items():
        assert path.startswith(prefix)
        p=RUN/path[len(prefix):]
        assert digest(p)==sha==index[path]['sha256'],path
        assert (ROOT/index[path]['local_path']).resolve()==p.resolve()
    run=read(RUN/'run.json'); assert run['commit']==SHA and run['status']=='completed'
    rows=[]; sets={}; requested={}; protocols=set(); masks=set(); raw_ce={}
    for c in run['cells']:
        assert c['status']=='completed'
        cond=c['conditions']; path=RUN/c['path']
        assert cond['model']=='OpenGU.GCNNet' and cond['budget_ratio']==.1
        for name,f in c['files'].items(): assert expected[prefix+c['path']+'/'+name]==f['sha256']
        met=read(path/'metrics.json'); selection=read(path/'selection.json')
        assert c['cell_id']==met['cell_id']==selection['cell_id']
        assert c['selection_id']==selection['selection_id']
        nodes=frozenset(selection['selected_nodes'])
        assert len(nodes)==len(selection['selected_nodes'])==selection['requested_k']
        stem=Path(cond['selector_ref']).stem
        source=next((a for a in SRC[1:] if stem.endswith('_'+a.lower())),'GCN') if cond['selector'] in SEL else 'baseline'
        k=(cond['dataset_name'],cond['selector'],source,cond['training_seed'],cond.get('random_selector_seed'))
        if k in sets: assert sets[k]==nodes
        sets[k]=nodes; requested.setdefault(cond['dataset_name'],set()).add(len(nodes))
        stages={r['stage']:r for r in met['rows']}; u=stages['utility']['values']
        r=dict(cell_id=c['cell_id'],dataset=cond['dataset_name'],method=cond['method'],seed=cond['training_seed'],
               selector=cond['selector'],source=source,random_seed=cond.get('random_selector_seed'),
               split=cond['dataset_fingerprint'],selection_id=c['selection_id'],output_id=c['output']['artifact_id'],
               before=None if u['f1_before'] is None else 100*u['f1_before'],after=100*u['f1_after'],
               U=None if u['f1_before'] is None else 100*(u['f1_before']-u['f1_after']),G=None,flip=None)
        raw_ce[c['cell_id']]=stages['method']['values']['cross_entropy']
        if cond['method']!='Retrain':
            g=stages['post_unlearning_utility_and_retrain_gap']; f=stages['post_unlearning_flip_hop']
            assert g['baseline_output']==f['baseline_output']==f['identity']['retrain_output']
            pr=f['identity']['protocol']; protocols.add(pr['comparison']); masks.add(pr['evaluation_mask'])
            assert pr['dataset_input']['instance']['split']['seed']==2024
            r.update(G=100*g['values']['gap'],retrain=100*g['values']['perf_retrain'],
                     baseline_id=g['baseline_output']['artifact_id'],flip=100*f['values']['fraction_flipped'])
            assert abs(r['G']-(r['retrain']-r['after']))<1e-8
        rows.append(r)
    df=pd.DataFrame(rows); assert len(df)==df.cell_id.nunique()==2520
    assert set(df.seed)==set(SEEDS) and df.groupby(['dataset','seed','method']).size().eq(12).all()
    assert df.groupby('dataset').split.nunique().eq(1).all()
    assert df[df.method!='Retrain'].groupby(['dataset','seed','method']).before.apply(lambda s:np.ptp(s)<1e-8).all()
    outputs=df.set_index('output_id')
    for r in rows:
        if r['method']=='Retrain': continue
        b=outputs.loc[r['baseline_id']]
        assert b.method=='Retrain' and all(b[k]==r[k] for k in ['dataset','seed','split','selection_id'])
        assert abs(b.after-r['retrain'])<1e-8
    assert protocols=={'argmax_gu_vs_same_request_retrain_first_index_ties'}
    existing=pd.read_csv(OUT/'cells.csv').set_index('cell_id').loc[df.cell_id]
    for key in ['dataset','method','seed','selector','source','split','selection_id','output_id']:
        assert np.array_equal(existing[key].to_numpy(),df[key].to_numpy()),key
    assert np.allclose(existing.random_seed,df.random_seed,equal_nan=True)
    for key in ['U','G','flip','before','after']:
        assert np.allclose(existing[key],df[key],atol=1e-9,equal_nan=True),key
    gu=df[df.method!='Retrain'].copy()
    assert gu[gu.selector=='random'].groupby(['dataset','seed','method']).random_seed.apply(lambda s:set(s)=={11,22,33}).all()
    profiles=gu.groupby(['dataset','seed','selector','source','method'],as_index=False)[['U','G','flip']].mean()
    paired=pd.read_csv(OUT/'paired_seed_values.csv')
    assert len(paired)==1440
    for metric in ['U','G','flip']:
        check=paired.merge(profiles[['dataset','seed','selector','source','method',metric]],on=['dataset','seed','selector','source','method'],suffixes=('_saved','_raw'),validate='one_to_one')
        assert np.allclose(check[metric+'_saved'],check[metric+'_raw'],atol=1e-9)
        rr=profiles[profiles.selector=='random'][['dataset','seed','method',metric]].rename(columns={metric:'raw_random'})
        check=paired.merge(rr,on=['dataset','seed','method'],validate='many_to_one')
        assert np.allclose(check[metric+'_random'],check.raw_random,atol=1e-9)
        assert np.allclose(check[metric+'_vs_random'],check[metric]-check.raw_random,atol=1e-9)
    summary=pd.read_csv(OUT/'summary.csv'); summary=summary[summary.cohort=='all10']
    assert summary.n.eq(10).all() and len(summary)==144
    for metric in ['U','G','flip']:
        check=summary.merge(profiles.groupby(['dataset','selector','source','method'],as_index=False)[metric].mean(),on=['dataset','selector','source','method'],validate='one_to_one')
        assert np.allclose(check[metric+'_mean'],check[metric],atol=1e-9)
    repeats=[]
    for ds in DS:
        for s,a in CONDS:
            ss=[v for k,v in sets.items() if k[:3]==(ds,s,a)]
            j=[len(x&y)/len(x|y) for x,y in combinations(ss,2)]
            repeats.append(dict(dataset=ds,selector=s,source=a,requests=len(ss),unique_node_sets=len(set(ss)),jaccard_mean=float(np.mean(j)),jaccard_min=float(min(j))))
    save('response_selection_repetition.csv',pd.DataFrame(repeats))
    pivot=gu.pivot(index=['dataset','seed','selector','source','random_seed'],columns='method',values='U')
    maxdiff=float((pivot.GIF-pivot.IDEA).abs().max()); assert maxdiff==0
    for metric in ['G','flip']:
        pp=gu.pivot(index=['dataset','seed','selector','source','random_seed'],columns='method',values=metric)
        assert (pp.GIF-pp.IDEA).abs().max()==0,metric
    ce=gu.assign(CE=gu.cell_id.map(raw_ce)).pivot(index=['dataset','seed','selector','source','random_seed'],columns='method',values='CE')
    code=[]
    for path in ['experiments/flip_hop_metrics.py','experiments/node_deletion.py','experiments/target_direct_v1/methods.py','experiments/configs/exp079/surrogate_multiseed.yaml']:
        frozen=subprocess.check_output(['git','show',f'{SHA}:GULib-master/{path}'],cwd=ROOT)
        assert frozen.replace(b'\r\n',b'\n')==(ROOT/path).read_bytes().replace(b'\r\n',b'\n')
        code.append(dict(path=path,matches_execution_sha=True))
    audit=dict(job_id=JOB,run_id='e79r5',execution_sha=SHA,run_sha256=digest(RUN/'run.json'),
               verified_files=5041,raw_cells=2520,raw_gu_cells=2160,paired_selector_gu_rows=1440,
               seed_profile_gu_rows=len(profiles),seed_clusters=10,gu_coordinates_main=5,gu_coordinates_full=6,
               random_selections_per_training_seed=3,random_seed_ids=[11,22,33],split_seed=2024,budget_ratio=.1,
               requested_k={k:sorted(v) for k,v in requested.items()},flip_protocol=sorted(protocols),flip_masks=sorted(masks),
               gif_idea_U_max_difference=maxdiff,gif_idea_CE_max_difference=float((ce.GIF-ce.IDEA).abs().max()),
               csv_matches_raw=True,summary_used_cohort='all10',source_checks=code,
               input_hashes={n:digest(OUT/n) for n in ['cells.csv','paired_seed_values.csv','summary.csv']},
               versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__,matplotlib=matplotlib.__version__),
               new_gpu_runs=0,scientific_acceptance='not_requested')
    dump('response_input_audit.json',audit)
    save('response_seed_profiles.csv',profiles)
    # Retrain contextual outcome is F1, not a seventh GU response coordinate.
    retrain=df[df.method=='Retrain'].groupby(['dataset','seed','selector','source'],as_index=False).after.mean()
    save('response_retrain_f1.csv',retrain)
    return profiles,retrain,audit

def tensor(profiles,ds,metric,methods=MAIN):
    p=profiles[profiles.dataset==ds].set_index(['seed','selector','source','method'])[metric]
    x=np.array([[[p.loc[(seed,s,a,g)] for g in methods] for s,a in CONDS] for seed in SEEDS])
    assert x.shape==(10,10,len(methods)) and np.isfinite(x).all()
    return x

def cv_sq(z):
    # Distinct-seed cross-products eliminate within-seed noise bias, no whitening.
    n,m=z.shape
    return float((np.sum(z.sum(axis=0)**2)-np.sum(z*z))/(n*(n-1)*m))
def cv_margin(x):
    w=[]; b=[]
    for a,bidx in combinations(range(4),2):
        w.extend([cv_sq(x[:,a]-x[:,bidx]),cv_sq(x[:,4+a]-x[:,4+bidx])])
        b.extend([cv_sq(x[:,a]-x[:,4+bidx]),cv_sq(x[:,4+a]-x[:,bidx])])
    return float(np.mean(w)),float(np.mean(b))
def jack_margin(x):
    w,b=cv_margin(x); est=b-w; n=len(x)
    loo=np.array([np.subtract(*cv_margin(np.delete(x,i,axis=0))[::-1]) for i in range(n)])
    se=np.sqrt((n-1)/n*np.sum((loo-loo.mean())**2)); half=stats.t.ppf(.975,n-1)*se
    return dict(within_cv2=w,between_cv2=b,margin_cv2=est,lo=float(est-half),hi=float(est+half),jackknife_se=float(se))

def analyze(profiles):
    summary=[]; contrasts=[]; pairs=[]; preservation=[]; distances=[]; margins=[]; repeat=[]; angular=[]; strategy=[]
    sets=[('dedup5',MAIN),('full6',GU)]+[('drop_'+g,[h for h in MAIN if h!=g]) for g in MAIN]
    for ds in DS:
        for metric in ['U','G','flip']:
            x=tensor(profiles,ds,metric)
            delta=x-x[:,[-1],:]
            for ai,a in enumerate(SRC):
                for j,g in enumerate(MAIN):
                    strategy.append(dict(dataset=ds,metric=metric,source=a,method=g,contrast='gt_full-r_point',**interval(x[:,ai,j]-x[:,4+ai,j])))
            for i,(s,a) in enumerate(CONDS):
                for j,g in enumerate(MAIN):
                    z=(delta[:,i,j]-(delta[:,i,:].sum(axis=1)-delta[:,i,j])/(len(MAIN)-1))
                    contrasts.append(dict(dataset=ds,metric=metric,selector=s,source=a,method=g,**interval(z)))
                for j,k in combinations(range(len(MAIN)),2):
                    z=delta[:,i,j]-delta[:,i,k]
                    pairs.append(dict(dataset=ds,metric=metric,selector=s,source=a,GU_A=MAIN[j],GU_B=MAIN[k],**interval(z)))
                for j,g in enumerate(GU):
                    values=profiles[(profiles.dataset==ds)&(profiles.selector==s)&(profiles.source==a)&(profiles.method==g)].set_index('seed').loc[SEEDS,metric]
                    summary.append(dict(dataset=ds,metric=metric,selector=s,source=a,method=g,**interval(values)))
                cx=center(x[:,i])
                noise=float(np.var(cx,axis=0,ddof=1).mean())
                signal=cv_sq(cx)
                cdelta=center(delta[:,i]); dn=float(np.var(cdelta,axis=0,ddof=1).mean())
                repeat.append(dict(dataset=ds,metric=metric,selector=s,source=a,centered_mean_signal_cv2=signal,seed_noise_energy=noise,mean_profile_uncertainty_energy=noise/10,
                    excess_random_signal_cv2=cv_sq(cdelta),excess_random_seed_noise_energy=dn))
            for sidx,s in enumerate(SEL):
                for aidx,a in enumerate(SRC[1:],1):
                    direct=delta[:,sidx*4]; target=delta[:,sidx*4+aidx]
                    for j,k in combinations(range(5),2):
                        d=direct[:,j]-direct[:,k]; z=target[:,j]-target[:,k]
                        dr=interval(d); sr=interval(z); shift=interval(z-d)
                        preservation.append(dict(dataset=ds,metric=metric,selector=s,source=a,GU_A=MAIN[j],GU_B=MAIN[k],
                            GCN_mean=dr['mean'],GCN_lo=dr['lo'],GCN_hi=dr['hi'],source_mean=sr['mean'],source_lo=sr['lo'],source_hi=sr['hi'],
                            same_mean_sign=bool(dr['mean']*sr['mean']>0),both_pointwise_same_sign=bool((dr['lo']>0 and sr['lo']>0) or (dr['hi']<0 and sr['hi']<0)),
                            shift_mean=shift['mean'],shift_lo=shift['lo'],shift_hi=shift['hi']))
            for mode in ['level','centered']:
                xx=x if mode=='level' else center(x)
                means=xx.mean(axis=0)
                for i,j in combinations(range(10),2):
                    distances.append(dict(dataset=ds,metric=metric,mode=mode,condition_A=LABELS[i],condition_B=LABELS[j],
                        RMSE_mean=float(np.sqrt(np.mean((means[i]-means[j])**2))),distance_cv2=cv_sq(xx[:,i]-xx[:,j])))
            for name,methods in sets:
                xx=tensor(profiles,ds,metric,methods)
                for mode in ['level','centered']:
                    zz=xx if mode=='level' else center(xx)
                    r=jack_margin(zz)
                    means=zz.mean(axis=0); w=[];b=[]
                    for a,bidx in combinations(range(4),2):
                        w.extend([np.sqrt(np.mean((means[a]-means[bidx])**2)),np.sqrt(np.mean((means[4+a]-means[4+bidx])**2))])
                        b.extend([np.sqrt(np.mean((means[a]-means[4+bidx])**2)),np.sqrt(np.mean((means[4+a]-means[bidx])**2))])
                    margins.append(dict(dataset=ds,metric=metric,mode=mode,coordinates=name,m=len(methods),n_seed_clusters=10,architecture_pairs=6,
                        within_RMSE=float(np.mean(w)),between_RMSE=float(np.mean(b)),margin_RMSE=float(np.mean(b)-np.mean(w)),**r))
    # Angular similarity is supplementary: five coordinates, no independent tests.
    for ds in DS:
        for coord,methods in [('dedup5',MAIN),('drop_GNNDelete',[g for g in MAIN if g!='GNNDelete'])]:
            x=tensor(profiles,ds,'U',methods)
            for ref in ['raw','excess_random']:
                z=center(x if ref=='raw' else x-x[:,[-1],:]).mean(axis=0)
                for si,s in enumerate(SEL):
                    i=si*4
                    for ai,a in enumerate(SRC[1:],1):
                        j=i+ai; other=(1-si)*4+ai
                        def cosine(p,q):
                            den=np.linalg.norm(p)*np.linalg.norm(q)
                            return float(np.dot(p,q)/den) if den>1e-10 else np.nan
                        angular.append(dict(dataset=ds,coordinates=coord,reference=ref,selector=s,source=a,
                            same_selector_cosine=cosine(z[i],z[j]),other_selector_cosine=cosine(z[i],z[other]),
                            GCN_norm_pp=float(np.linalg.norm(z[i])/np.sqrt(len(methods))),source_norm_pp=float(np.linalg.norm(z[j])/np.sqrt(len(methods)))))
    save('response_shape_cosine.csv',pd.DataFrame(angular))
    st=pd.DataFrame(strategy)
    for metric in ['U','G','flip']:
        ix=st.metric==metric; st.loc[ix,'p_holm']=holm(st.loc[ix,'p'])
    save('response_gt_vs_r_point.csv',st)
    c=pd.DataFrame(contrasts); pair=pd.DataFrame(pairs)
    # Control family over all dataset x strategy/source x GU endpoints per metric.
    for metric in ['U','G','flip']:
        ix=(c.metric==metric)&(c.selector!='random'); c.loc[ix,'p_holm']=holm(c.loc[ix,'p'])
        ix=(pair.metric==metric)&(pair.selector!='random'); pair.loc[ix,'p_holm']=holm(pair.loc[ix,'p'])
    save('response_profile_summary.csv',pd.DataFrame(summary))
    save('response_selectivity.csv',c)
    save('response_GU_pair_interactions.csv',pair)
    save('response_interaction_preservation.csv',pd.DataFrame(preservation))
    save('response_distances.csv',pd.DataFrame(distances))
    save('response_consistency_margin.csv',pd.DataFrame(margins))
    save('response_repeatability.csv',pd.DataFrame(repeat))
    # Both contrast-of-contrasts cancels common additive GU sensitivity, but Random
    # is one shared block, not 8 independent observations.
    for ds in DS:
        xx=tensor(profiles,ds,'U'); ref=xx[:,[-1]]
        assert np.allclose(center(xx[:,0]-xx[:,1]),center((xx-ref)[:,0]-(xx-ref)[:,1]))
        gg=tensor(profiles,ds,'G')
        assert np.allclose(center(xx-xx[:,[-1]]),center(gg-gg[:,[-1]]),atol=1e-8)
    return pd.DataFrame(summary),c,pd.DataFrame(margins),pd.DataFrame(distances)

def export(fig,name):
    for ext in ['png','svg','pdf']:
        path=OUT/f'{name}.{ext}'
        fig.savefig(path,dpi=170,bbox_inches='tight',facecolor='white',metadata={'Creator':'EXP-079 response_pattern.py'} if ext=='pdf' else None)
        if ext=='svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)

def figures(profiles,summary,contrasts,margins,distances):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    short=['GNNDelete','GIF','IDEA','MEGU','GraphEraser','GraphRevoker']
    fig,axs=plt.subplots(3,2,figsize=(16,17),layout='constrained')
    for row,ds in enumerate(DS):
        for col,metric in enumerate(['U','G']):
            ax=axs[row,col]; z=tensor(profiles,ds,metric,GU).mean(axis=0)
            vmax=max(1.,float(abs(z).max())); norm=TwoSlopeNorm(vcenter=0,vmin=-vmax,vmax=vmax)
            im=ax.imshow(z,cmap='RdBu_r',norm=norm,aspect='auto')
            ax.set(xticks=range(6),xticklabels=short,yticks=range(10),yticklabels=LABELS,
                title=f'{ds} | {metric} (pp) | 10 training seeds')
            ax.tick_params(axis='x',labelrotation=25)
            for i in range(10):
                for j in range(6):ax.text(j,i,f'{z[i,j]:.2f}',ha='center',va='center',color='white' if abs(z[i,j])>vmax*.6 else '#172230')
            fig.colorbar(im,ax=ax,shrink=.7,label='pp; positive = lower utility / below Retrain')
    fig.suptitle('Response atlas | fixed target GCN, split 2024, budget 10%\nGCN = direct selection reference; Degree is deterministic; Random = mean of 11/22/33 within each seed',fontsize=15)
    export(fig,'response_atlas_U_G_10seeds')
    fig,axs=plt.subplots(3,3,figsize=(17,12),layout='constrained',sharey='row')
    for row,ds in enumerate(DS):
        for col,s in enumerate(['gt_full','r_point','controls']):
            ax=axs[row,col]; conds=[(s,a) for a in SRC] if col<2 else CONDS[-2:]
            for idx,(sel,src) in enumerate(conds):
                ss=summary[(summary.dataset==ds)&(summary.metric=='U')&(summary.selector==sel)&(summary.source==src)].set_index('method').loc[GU]
                color=COLORS[idx] if col<2 else ['#535767','#999999'][idx]
                ax.errorbar(np.arange(6)+(idx-1.5)*.05,ss['mean'],yerr=[ss['mean']-ss.lo,ss.hi-ss['mean']],fmt='o-',color=color,linewidth=1.3,capsize=2,label=src if col<2 else sel.title())
            ax.axhline(0,color='#555',linewidth=.6)
            ax.set(xticks=range(6),xticklabels=short,title=f'{ds} | {s}',ylabel='U: F1 before - F1 after (pp)')
            ax.tick_params(axis='x',labelrotation=40); ax.grid(axis='y',alpha=.2)
            ax.legend(fontsize=8,ncol=2)
    fig.suptitle('Absolute utility response | pointwise 95% t intervals over 10 paired training seeds\nGIF and IDEA shown separately; inferential geometry counts them once',fontsize=15)
    export(fig,'response_profiles_U_10seeds')
    fig,axs=plt.subplots(3,2,figsize=(16,12),layout='constrained',sharey='row')
    for row,ds in enumerate(DS):
        for col,s in enumerate(SEL):
            ax=axs[row,col]
            for idx,a in enumerate(SRC):
                ss=contrasts[(contrasts.dataset==ds)&(contrasts.metric=='U')&(contrasts.selector==s)&(contrasts.source==a)].set_index('method').loc[MAIN]
                ax.errorbar(np.arange(5)+(idx-1.5)*.12,ss['mean'],yerr=[ss['mean']-ss.lo,ss.hi-ss['mean']],fmt='o',capsize=3,color=COLORS[idx],label=a)
            ax.axhline(0,color='#555',linewidth=.8)
            ax.set(xticks=range(5),xticklabels=MAIN,title=f'{ds} | {s}',ylabel='S: excess over Random, GU vs rest (pp)')
            ax.tick_params(axis='x',labelrotation=25); ax.grid(axis='y',alpha=.2); ax.legend(ncol=4,fontsize=8)
    fig.suptitle('Relative selectivity | S(g) = (U - Random)(g) - mean of the other 4 GU\nPositive = extra harm is more concentrated on this GU; pointwise intervals, full Holm results in CSV',fontsize=15)
    export(fig,'response_selectivity_U_10seeds')
    fig,axs=plt.subplots(1,3,figsize=(19,7),layout='constrained')
    for ax,ds in zip(axs,DS):
        z=np.zeros((10,10)); part=distances[(distances.dataset==ds)&(distances.metric=='U')&(distances['mode']=='centered')]
        for r in part.itertuples():
            i,j=LABELS.index(r.condition_A),LABELS.index(r.condition_B);z[i,j]=z[j,i]=r.RMSE_mean
        im=ax.imshow(z,cmap='YlGnBu',vmin=0)
        ax.set(xticks=range(10),yticks=range(10),xticklabels=LABELS,yticklabels=LABELS,title=ds)
        ax.tick_params(axis='x',labelrotation=90)
        for i in range(10):
            for j in range(10):ax.text(j,i,f'{z[i,j]:.1f}',ha='center',va='center',fontsize=7,color='white' if z[i,j]>z.max()*.6 else '#172230')
        ax.axhline(3.5,color='#d97442');ax.axvline(3.5,color='#d97442')
        fig.colorbar(im,ax=ax,shrink=.65,label='RMSE of mean centered profiles (pp)')
    fig.suptitle('Profile geometry | all 10 conditions, 5 distinct GU coordinates\nSubtract each profile mean; retain pp scale; distances are descriptive, not independent samples',fontsize=15)
    export(fig,'response_distance_matrix_U_10seeds')
    fig,axs=plt.subplots(2,3,figsize=(16,9),layout='constrained')
    names=['dedup5','full6']+['drop_'+g for g in MAIN]
    for row,metric in enumerate(['U','flip']):
        for col,ds in enumerate(DS):
            ax=axs[row,col]; q=margins[(margins.dataset==ds)&(margins.metric==metric)&(margins['mode']=='centered')].set_index('coordinates').loc[names]
            ax.errorbar(q.margin_cv2,np.arange(len(q)),xerr=[q.margin_cv2-q.lo,q.hi-q.margin_cv2],fmt='o',capsize=3,color='#2055a5')
            ax.axvline(0,color='#555',linewidth=.8)
            ax.set(yticks=range(7),yticklabels=names,title=f'{ds} | {metric}',xlabel='Cross-seed distance margin (pp squared)')
            ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
    fig.suptitle('Same selector across surrogate vs different selector across surrogate\nPositive margin = between-selector distance exceeds within-selector distance; approximate 95% seed jackknife intervals',fontsize=14)
    export(fig,'response_margin_sensitivity_10seeds')
    fig,axs=plt.subplots(1,3,figsize=(18,7),layout='constrained')
    for ax,ds in zip(axs,DS):
        z=tensor(profiles,ds,'flip',GU).mean(axis=0)
        im=ax.imshow(z,cmap='YlOrRd',aspect='auto',vmin=0)
        ax.set(xticks=range(6),yticks=range(10),xticklabels=short,yticklabels=LABELS,title=ds)
        ax.tick_params(axis='x',labelrotation=35)
        for i in range(10):
            for j in range(6):ax.text(j,i,f'{z[i,j]:.1f}',ha='center',va='center',color='white' if z[i,j]>z.max()*.6 else '#172230')
        fig.colorbar(im,ax=ax,shrink=.7,label='GU vs matched Retrain disagreement (%)')
    fig.suptitle('Prediction disagreement | 10 training seeds | same-request GU vs Retrain\nThis is not a before/after flip rate and not proof of successful forgetting',fontsize=15)
    export(fig,'response_disagreement_10seeds')

def main():
    profiles,retrain,audit=audit_inputs()
    summary,c,m,d=analyze(profiles)
    figures(profiles,summary,c,m,d)
    print(m[(m.metric=='U')&(m.coordinates=='dedup5')][['dataset','mode','within_RMSE','between_RMSE','margin_cv2','lo','hi']].to_string(index=False))
    print('Verified 5041 raw files; all ten seeds; generated six PNG/SVG/PDF figures and analysis CSVs.')

if __name__=='__main__': main()
