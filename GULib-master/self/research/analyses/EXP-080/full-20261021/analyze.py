"""Completed EXP080 three-table analysis. Writes only beside this script; no experiment mutation."""
from pathlib import Path
import json,hashlib,sys,subprocess
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'experiments/modular_run.py').exists())
SOURCES=[('exp080-20261019-e80r306','exp080-cc-citeseer-high','e80r306',147,'8fb8169475b015ac4cc6dd1a61c6d26ee5ff7670'),('exp080-20261018-e80r305','exp080-cc-base','e80r305',1764,'a217daf5c67b485afed63c393b5e8bb23820b237'),('exp080-20261018-e80r302','exp080-cc-cora-high','e80r302',105,'9d24b46ff14156685c62d8cdb59df1840d9e2c22')]
METHODS=['Retrain','GIF','IDEA','MEGU','GNNDelete','GraphEraser','GraphRevoker']
SELECTORS=['random','degree','r_point','gt_full','im_rr_greedy']
METRICS=['accuracy','classification_auc','cross_entropy','before','drop','gap','disagreement','retrain','update_detection_auc']
KEYS=['dataset','method','selector','ratio']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def csv(name,df):df.to_csv(OUT/name,index=False,encoding='utf-8')
def request(c):return (c['dataset_name'],c['training_seed'],c['budget_ratio'],c['selector'],c.get('im_selector_seed',-1))
index=read(ROOT/'.syncmate/artifact_index.json');idx={x['path']:x for x in index['peers']['gpu4090']['items']}
rows=[];audit=[];selections={};retrains={};gu_pairs=[];masks={};hops=[]
for job,experiment,rid,count,commit in SOURCES:
    dp=ROOT/'.syncmate/deliveries'/f'{job}.json';d=read(dp);h=read(ROOT/'.syncmate/runs'/f'{job}.json');r=d['result']
    assert d['execution']==h['execution'] and d['execution']['git_sha']==commit
    assert r['ok'] and r['gate_passed'] and r['project_acceptance']['passed'] and r['project_acceptance']['accepted_cells']==count
    manifest=r['completed_job']['result']['manifest'];assert manifest['status']=='verified'
    expected={x['path']:x['sha256'] for x in manifest['artifacts']}
    assert set(expected)==set(h['execution']['artifact_paths'])==set(h['execution']['collect_paths'])
    prefix=f'results/runs/{experiment}/{rid}/';raw=ROOT/'results/runs/gpu4090'/experiment/rid
    for path,digest in expected.items():
        assert path.startswith(prefix)
        local=raw/path[len(prefix):]
        assert sha(local)==digest==idx[path]['sha256'],path
        assert (ROOT/idx[path]['local_path']).resolve()==local.resolve()
    run=read(raw/'run.json');assert run['status']=='completed' and run['commit']==commit and len(run['cells'])==count
    for c in run['cells']:
        cond=c['conditions'];k=request(cond);folder=raw/c['path'];m=read(folder/'metrics.json');sel=read(folder/'selection.json')
        assert c['status']=='completed' and c['cell_id']==m['cell_id']==sel['cell_id']
        for name,info in c['files'].items():assert expected[prefix+c['path']+'/'+name]==info['sha256']
        nodes=tuple(sel['selected_nodes']);assert len(nodes)==len(set(nodes))==sel['requested_k']
        if k in selections:assert selections[k]==nodes,'Selection mismatch across methods'
        selections[k]=nodes
        stages={s['stage']:s for s in m['rows']};u=stages['utility']['values'];base=stages['method']['values']
        assert abs(base['accuracy']-u['f1_after'])<1e-12
        row=dict(dataset=cond['dataset_name'],method=cond['method'],selector=cond['selector'],ratio=cond['budget_ratio'],seed=cond['training_seed'],im_seed=cond.get('im_selector_seed',-1),requested_k=len(nodes),job_id=job,run_id=rid,execution_sha=commit,cell_id=c['cell_id'],cell_path=str(folder.relative_to(ROOT)).replace('\\','/'),split=cond['dataset_fingerprint'],selection_id=c['selection_id'],selected_nodes_sha256=hashlib.sha256(json.dumps(nodes,separators=(',',':')).encode()).hexdigest(),output_id=c['output']['artifact_id'],accuracy=100*base['accuracy'],classification_auc=base['classification_auc'],cross_entropy=base['cross_entropy'],before=None if u['f1_before'] is None else 100*u['f1_before'],drop=None if u['f1_drop'] is None else 100*u['f1_drop'],gap=None,disagreement=None,retrain=None,update_detection_auc=base['update_detection_auc'],update_detection_status=base['update_detection_auc_status'],method_cache=c['cache']['method'])
        if cond['method']=='Retrain':retrains[k]=(c['output'],nodes,row['accuracy'])
        else:
            g=stages['post_unlearning_utility_and_retrain_gap'];f=stages['post_unlearning_flip_hop'];pr=f['identity']['protocol']
            assert g['baseline_output']==f['baseline_output']==f['identity']['retrain_output']
            assert pr['comparison']=='argmax_gu_vs_same_request_retrain_first_index_ties' and pr['evaluation_mask']=='test_mask_excluding_selected_nodes'
            masks.setdefault(cond['dataset_name'],set()).add(pr['evaluation_mask_sha256'])
            row.update(gap=100*g['values']['gap'],retrain=100*g['values']['perf_retrain'],disagreement=100*f['values']['fraction_flipped'])
            assert abs(row['gap']-(row['retrain']-row['accuracy']))<1e-8
            assert abs(row['drop']-(row['before']-row['accuracy']))<1e-8
            gu_pairs.append((k,g['baseline_output'],nodes,row['retrain']))
            for band in ['1','2','3','gt3']:
                v=f['values'];hops.append(dict(dataset=row['dataset'],method=row['method'],selector=row['selector'],ratio=row['ratio'],seed=row['seed'],im_seed=row['im_seed'],band=band,nodes=v[band+'_hop_count'],flipped=v[band+'_hop_flipped_count']))
        rows.append(row)
    audit.append(dict(job_id=job,run_id=rid,execution_sha=commit,cells=count,verified_files=len(expected),run_sha256=sha(raw/'run.json'),delivery_sha256=sha(dp),source=str(raw.relative_to(ROOT)).replace('\\','/')))
for k,baseline,nodes,perf in gu_pairs:
    output,refnodes,acc=retrains[k];assert baseline==output and nodes==refnodes and abs(perf-acc)<1e-8
df=pd.DataFrame(rows);assert len(df)==2016 and not df.duplicated(['dataset','method','selector','ratio','seed','im_seed']).any()
assert set(df.seed)=={42,212,2024} and df.groupby('dataset').split.nunique().eq(1).all()
assert all(len(v)==1 for v in masks.values())
assert df.groupby(KEYS+['seed']).size().reset_index(name='n').apply(lambda r:r['n']==(3 if r.selector=='im_rr_greedy' else 1),axis=1).all()
prefix_checks=[]
for ds,seed,_,selector,im in sorted(selections):
    key=(ds,seed,selector,im)
    if any(x['key']==list(key) for x in prefix_checks):continue
    points=sorted((k[2],v) for k,v in selections.items() if (k[0],k[1],k[3],k[4])==key)
    for (r1,n1),(r2,n2) in zip(points,points[1:]):
        prefix_checks.append(dict(key=list(key),low=r1,high=r2,strict_prefix=n1==n2[:len(n1)]))
assert all(x['strict_prefix'] for x in prefix_checks)
csv('cells.csv',df)
seed=df.groupby(KEYS+['seed'],as_index=False)[METRICS].mean();csv('seed_values.csv',seed)
summary=seed.groupby(KEYS)[METRICS].agg(['mean','std','count']);summary.columns=['_'.join(c) for c in summary.columns];summary=summary.reset_index();csv('condition_summary.csv',summary)
assert summary['accuracy_count'].eq(3).all()
end=[]
for (ds,m,s),g in seed.groupby(['dataset','method','selector']):
    lo=g[g.ratio==.05].set_index('seed')
    for high in [.33,.5]:
        hi=g[g.ratio==high].set_index('seed')
        if hi.empty:continue
        assert set(lo.index)==set(hi.index)
        for metric in METRICS:
            delta=hi[metric]-lo[metric]
            if delta.notna().any():end.append(dict(dataset=ds,method=m,selector=s,low=.05,high=high,metric=metric,mean=delta.mean(),sd=delta.std(ddof=1),negative=int((delta<0).sum()),positive=int((delta>0).sum()),n=3))
end=pd.DataFrame(end);csv('endpoint_changes.csv',end)
random=seed[seed.selector=='random'].drop(columns='selector');contrast=seed.merge(random,on=['dataset','method','ratio','seed'],suffixes=('','_random'),validate='many_to_one')
for m in METRICS:contrast[m+'_vs_random']=contrast[m]-contrast[m+'_random']
csv('paired_vs_random.csv',contrast)
cols=[m+'_vs_random' for m in METRICS];cs=contrast.groupby(KEYS)[cols].agg(['mean','std']);cs.columns=['_'.join(c) for c in cs.columns];cs=cs.reset_index();csv('paired_vs_random_summary.csv',cs)
pivot=df.pivot(index=['dataset','ratio','selector','seed','im_seed'],columns='method',values=['accuracy','classification_auc','cross_entropy','drop','gap','disagreement'])
duplicates={m:float((pivot[m]['GIF']-pivot[m]['IDEA']).abs().max()) for m in pivot.columns.levels[0]}
hop=pd.DataFrame(hops);csv('hop_counts.csv',hop)
hop['rate']=np.where(hop.nodes>0,100*hop.flipped/hop.nodes,np.nan)
hs=hop.groupby(KEYS+['seed','band'],as_index=False)[['rate','nodes']].mean().groupby(KEYS+['band'])[['rate','nodes']].agg(['mean','std','count']);hs.columns=['_'.join(c) for c in hs.columns];csv('hop_summary.csv',hs.reset_index())
colors=dict(zip(METHODS,['#20252e','#196f91','#9c53a5','#bd7a18','#c54236','#2b8b65','#6e6c9b']))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':160})
for metric,label in [('accuracy','Test accuracy (%)'),('disagreement','GU vs Retrain disagreement (%)'),('classification_auc','Test classification AUROC'),('cross_entropy','Test cross entropy'),('drop','Before - after accuracy (pp)')]:
    fig,axes=plt.subplots(2,5,figsize=(17,7),sharex=True)
    for i,ds in enumerate(['Cora','CiteSeer']):
        for j,s in enumerate(SELECTORS):
            ax=axes[i,j]
            for method in METHODS:
                v=summary[(summary.dataset==ds)&(summary.selector==s)&(summary.method==method)].sort_values('ratio')
                if not v[metric+'_count'].any():continue
                x=v.ratio.to_numpy()*100;y=v[metric+'_mean'].to_numpy();sd=v[metric+'_std'].to_numpy()
                ax.plot(x,y,label=method+('*' if method=='GraphRevoker' else ''),color=colors[method],marker='o',ms=3,lw=1.7,ls='--' if method=='IDEA' else '-')
                ax.fill_between(x,y-sd,y+sd,color=colors[method],alpha=.07)
            if metric=='disagreement':
                last=100*summary[(summary.dataset==ds)&(summary.selector==s)&(summary.method=='Retrain')].ratio.max()
                ax.plot([5,last],[0,0],color=colors['Retrain'],ls=':',lw=1.5,label='Retrain vs itself = 0')
                ax.set_ylim(bottom=-2)
            ax.set_title(ds+' | '+('IM (3 draws/seed)' if s=='im_rr_greedy' else s));ax.grid(alpha=.18);ax.set_xticks([5,15,33,50])
            if i==1:ax.set_xlabel('Deleted training candidates (%)')
            if j==0:ax.set_ylabel(label)
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.025),ncol=7,fontsize=8)
    fig.text(.5,.007,'* GraphRevoker: GPA + optimal. A dotted zero line, where shown, is a self-comparison identity reference.',ha='center',fontsize=8)
    fig.suptitle(label+' | All 5 selectors, all available methods\n3 training seeds | mean +/- sample SD | missing endpoints left absent',fontsize=12)
    fig.tight_layout(rect=[0,.085,1,.92])
    for ext in ['png','svg','pdf']:
        target=OUT/(metric+'.'+ext)
        fig.savefig(target,bbox_inches='tight')
        if ext=='svg':
            target.write_text('\n'.join(line.rstrip() for line in target.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)
dump('verification.json',dict(scope='Completed base1764+Cora high105+CiteSeer high147; gates and EXP081 excluded',sources=audit,verified_files=sum(x['verified_files'] for x in audit),cells=len(df),request_count=len(selections),gu_retrain_pairs=len(gu_pairs),prefix_checks=len(prefix_checks),all_prefix_checks_pass=True,selection_same_across_methods=True,evaluation_masks={k:list(v) for k,v in masks.items()},gif_idea_max_abs_difference=duplicates,rows_by_dataset_method=df.groupby(['dataset','method']).size().unstack().to_dict(),missing_before=int(df.before.isna().sum()),index_sha256=sha(ROOT/'.syncmate/artifact_index.json'),new_gpu_jobs=0,scientific_acceptance='not_evaluated',inference='3 training-seed descriptive mean/sample SD; IM repeats first averaged within seed; no hypothesis tests'))
print(json.dumps({'cells':len(df),'files':sum(x['verified_files'] for x in audit),'paired':len(gu_pairs),'prefix_checks':len(prefix_checks),'gif_idea':duplicates}))
print('RETRAIN 5->33');print(end[(end.method=='Retrain')&(end.metric=='accuracy')&(end.high==.33)].to_string(index=False))
print('R_POINT 5->33');print(end[(end.selector=='r_point')&(end.metric.isin(['accuracy','disagreement']))&(end.high==.33)].to_string(index=False))
print('CORA50 RPOINT');print(summary[(summary.dataset=='Cora')&(summary.selector=='r_point')&(summary.ratio==.5)][['method','accuracy_mean','drop_mean','gap_mean','disagreement_mean']].to_string(index=False))
