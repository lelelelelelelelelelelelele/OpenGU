from pathlib import Path
import csv, json, hashlib, statistics, collections
ROOT = Path('.')
OUT = ROOT/'self/research/analyses/evidence/AAGU-032-AAGU-053-3000epoch-20260923'
OUT.mkdir(parents=True, exist_ok=True)

RUNS = {
 '032': ROOT/'results/runs/gpu4090/aagu032-extended-v2-multi-gcn-retrain/aagu032-recovery-full-20260920/run.json',
 '053': ROOT/'results/runs/gpu4090/aagu053-im-group-budget10/aagu053-newtraining-full-20260920/run.json'
}
def load_run(p):
 x=json.loads(p.read_text(encoding='utf-8'))
 assert x['status']=='completed'
 cellmap={}
 for c in x['cells']:
  assert c['status']=='completed'
  folder=p.parent/c['path']
  for name,decl in c['files'].items():
   target=folder/name
   assert target.is_file(), (c['cell_id'],name)
   got=hashlib.sha256(target.read_bytes()).hexdigest()
   assert got==decl['sha256'], (c['cell_id'],name,'hash mismatch')
  m=json.loads((folder/'metrics.json').read_text(encoding='utf-8'))
  s=json.loads((folder/'selection.json').read_text(encoding='utf-8'))
  c['_metrics']=m
  c['_selection']=s
  cellmap[c['cell_id']]=c
 return x,cellmap
def row_values(c):
 out={}
 for row in c['_metrics']['rows']:
  out[row['stage']]=row['values']
 return out
def stats(vals):
 vals=list(vals)
 return {'n':len(vals),'mean':statistics.mean(vals),
         'sd':statistics.stdev(vals) if len(vals)>1 else None,
         'min':min(vals),'max':max(vals)}
def s(v): return None if v is None else round(v,8)
def pctstats(vals):
 z=stats(vals)
 return {k:(round(v*100,6) if v is not None else None) for k,v in z.items()}
def ppstats(vals):
 z=stats(vals)
 return {k:(round(v,6) if v is not None else None) for k,v in z.items()}
def writecsv(path, rows):
 if not rows: return
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]))
  w.writeheader(); w.writerows(rows)

# AAGU-032: same condition-coordinate keys, old accepted summary rows vs recovered 3000-epoch run.
old032_path=ROOT/'.workblock/items/AAGU-033/analysis/20260908/retrain_cells.csv'
with old032_path.open(encoding='utf-8-sig',newline='') as f: old032=list(csv.DictReader(f))
run032,m032=load_run(RUNS['032'])
assert len(old032)==360 and len(m032)==360
assert len({r['cell_id'] for r in old032})==360
assert set(r['cell_id'] for r in old032)==set(m032)
a032=[]
for o in old032:
 c=m032[o['cell_id']]
 co=c['conditions']
 assert o['dataset']==co['dataset_name']
 assert int(o['training_seed'])==co['seed']
 assert float(o['budget_ratio'])==co['budget_ratio']
 assert o['selector_ref']==co['selector_ref']
 assert o['dataset_fingerprint']==co['dataset_fingerprint']
 vals=row_values(c)
 new=vals['utility']['f1_after']
 assert vals['method']['f1']==new, (o['cell_id'],'method/utility F1 mismatch')
 old=float(o['f1_after'])
 a032.append({
  'dataset':o['dataset'],'training_seed':int(o['training_seed']),
  'budget_ratio':float(o['budget_ratio']),'selector_ref':o['selector_ref'],
  'cell_id':o['cell_id'],'selection_id_old':o['selection_id'],
  'selection_id_new':c['selection_id'],'selection_id_same':o['selection_id']==c['selection_id'],
  'output_recipe_hash_old':o['output_recipe_hash'],
  'output_recipe_hash_new':c['output']['recipe_hash'],
  'old_f1_after_pct':old*100,'new_f1_after_pct':new*100,
  'delta_new_minus_old_pp':(new-old)*100
 })
g032=collections.defaultdict(list)
for r in a032: g032[(r['dataset'],r['budget_ratio'],r['selector_ref'])].append(r)
sum032=[]
for key,rs in sorted(g032.items()):
 old=[r['old_f1_after_pct'] for r in rs]; new=[r['new_f1_after_pct'] for r in rs]; d=[r['delta_new_minus_old_pp'] for r in rs]
 sum032.append(dict(dataset=key[0],budget_ratio=key[1],selector_ref=key[2],n=len(rs),
  old_mean_pct=statistics.mean(old),old_sd_pct=statistics.stdev(old),
  new_mean_pct=statistics.mean(new),new_sd_pct=statistics.stdev(new),
  delta_mean_pp=statistics.mean(d),delta_sd_pp=statistics.stdev(d),
  selection_ids_same=sum(r['selection_id_same'] for r in rs),
  output_recipes_same=sum(r['output_recipe_hash_old']==r['output_recipe_hash_new'] for r in rs)))
writecsv(OUT/'AAGU-032-all-conditions.csv',a032)
writecsv(OUT/'AAGU-032-summary-120-groups.csv',sum032)
core=['degree.yaml','gt_full.yaml','gt_full_all_trainable.yaml','gt_full_all_trainable_hops3.yaml']
labels={'degree.yaml':'Degree','gt_full.yaml':'D-full 末层 / 2-hop',
 'gt_full_all_trainable.yaml':'D-full 全参数 / 2-hop',
 'gt_full_all_trainable_hops3.yaml':'D-full 全参数 / 3-hop'}
t032={}
for ds in ['Cora','CiteSeer','PubMed']:
 rows=[]
 for b in [.01,.05,.10,.15]:
  row={'budget':f'{b*100:.0f}%'}
  for sel in core:
   item=next(x for x in sum032 if x['dataset']==ds and x['budget_ratio']==b and x['selector_ref']==sel)
   row[labels[sel]]=item
  rows.append(row)
 t032[ds]=rows
d032_summary={}
for ds in ['Cora','CiteSeer','PubMed']:
 rr=[r for r in a032 if r['dataset']==ds]
 d032_summary[ds]={
  'n':len(rr),'all_condition_old_mean_pct':statistics.mean(x['old_f1_after_pct'] for x in rr),
  'all_condition_new_mean_pct':statistics.mean(x['new_f1_after_pct'] for x in rr),
  'all_condition_delta_mean_pp':statistics.mean(x['delta_new_minus_old_pp'] for x in rr),
  'delta_range_pp':[min(x['delta_new_minus_old_pp'] for x in rr),max(x['delta_new_minus_old_pp'] for x in rr)],
  'selector_id_same':sum(x['selection_id_same'] for x in rr),
  'output_recipe_same':sum(x['output_recipe_hash_old']==x['output_recipe_hash_new'] for x in rr),
  'cache_method_hit':sum(c['cache']['method']=='hit' for c in run032['cells']),
  'producer_called':sum(c['producer_called'].get('method') is True for c in run032['cells'])
 }
# degree vs 3 D-full selectors within each dataset-budget
d032_effect={}
for ds in ['Cora','CiteSeer','PubMed']:
 vals=[]
 for b in [.01,.05,.10,.15]:
  degree=next(x['new_mean_pct'] for x in sum032 if x['dataset']==ds and x['budget_ratio']==b and x['selector_ref']=='degree.yaml')
  for sel in core[1:]:
   v=next(x['new_mean_pct'] for x in sum032 if x['dataset']==ds and x['budget_ratio']==b and x['selector_ref']==sel)
   vals.append(v-degree) # Dfull - Degree; negative means lower F1 / stronger utility damage
 d032_effect[ds]={'comparisons':len(vals),'dfull_lower_f1':sum(v<0 for v in vals),'equal':sum(v==0 for v in vals),'dfull_higher_f1':sum(v>0 for v in vals),
                  'mean_df_minus_degree_pp':statistics.mean(vals),'min_pp':min(vals),'max_pp':max(vals)}

# AAGU-053: old paired detail rows vs current GNNDelete/Retrain outputs.
old053=json.loads((ROOT/'.workblock/items/AAGU-053/evidence/table-detail.json').read_text(encoding='utf-8-sig'))
run053,m053=load_run(RUNS['053'])
assert len(old053)==48 and len(m053)==96
new_gn=[c for c in run053['cells'] if c['conditions']['method']=='GNNDelete']
new_rt=[c for c in run053['cells'] if c['conditions']['method']=='Retrain']
assert len(new_gn)==48 and len(new_rt)==48
a053=[]
for o in old053:
 g=m053[o['cell_id']]
 assert g['conditions']['method']=='GNNDelete'
 assert g['conditions']['dataset_name']==o['dataset']
 assert g['selection_id']==o['selection_id']
 candidates=[c for c in new_rt if c['conditions']['dataset_name']==o['dataset'] and c['selection_id']==o['selection_id']]
 assert len(candidates)==1, (o['dataset'],o['selector'],o['seed'],len(candidates))
 r=candidates[0]
 assert g['conditions']['selector_ref']==r['conditions']['selector_ref']
 vg=row_values(g); vr=row_values(r)
 assert vg['method']['f1']==vg['utility']['f1_after']
 assert vr['method']['f1']==vr['utility']['f1_after']
 p0n=vg['utility']['f1_before']*100
 gun=vg['utility']['f1_after']*100
 rtn=vr['utility']['f1_after']*100
 p0o=float(o['p0']); guo=float(o['gu']); rto=float(o['retrain'])
 a053.append({
  'dataset':o['dataset'],'selector':o['selector'],'selector_seed':o['seed'],
  'cell_id':o['cell_id'],'selection_id_old':o['selection_id'],'selection_id_new':g['selection_id'],
  'selection_same':True,'p0_old_pct':p0o,'p0_new_pct':p0n,'p0_delta_pp':p0n-p0o,
  'gu_old_pct':guo,'gu_new_pct':gun,'gu_delta_pp':gun-guo,
  'retrain_old_pct':rto,'retrain_new_pct':rtn,'retrain_delta_pp':rtn-rto,
  'gap_old_pp':rto-guo,'gap_new_pp':rtn-gun,'gap_delta_pp':(rtn-gun)-(rto-guo),
  'p0_gu_old_pp':p0o-guo,'p0_gu_new_pp':p0n-gun,'p0_gu_delta_pp':(p0n-gun)-(p0o-guo),
  'p0_retrain_old_pp':p0o-rto,'p0_retrain_new_pp':p0n-rtn,'p0_retrain_delta_pp':(p0n-rtn)-(p0o-rto),
  'gnn_cell_cache':g['cache']['method'],'retrain_cell_cache':r['cache']['method'],
  'gnn_producer_called':g['producer_called'].get('method'),'retrain_producer_called':r['producer_called'].get('method')
 })
writecsv(OUT/'AAGU-053-all-pairs.csv',a053)
g053=collections.defaultdict(list)
for r in a053:g053[(r['dataset'],r['selector'])].append(r)
sum053=[]
for key,rs in sorted(g053.items()):
 q={'dataset':key[0],'selector':key[1],'n':len(rs)}
 for measure in ['p0','gu','retrain','gap']:
  old=[r[f'{measure}_old_pct' if measure!='gap' else 'gap_old_pp'] for r in rs]
  new=[r[f'{measure}_new_pct' if measure!='gap' else 'gap_new_pp'] for r in rs]
  delta=[r[f'{measure}_delta_pp'] for r in rs]
  q[f'{measure}_old_mean']=statistics.mean(old);q[f'{measure}_old_sd']=statistics.stdev(old) if len(old)>1 else None
  q[f'{measure}_new_mean']=statistics.mean(new);q[f'{measure}_new_sd']=statistics.stdev(new) if len(new)>1 else None
  q[f'{measure}_delta_mean']=statistics.mean(delta);q[f'{measure}_delta_sd']=statistics.stdev(delta) if len(delta)>1 else None
 for measure in ['p0_gu','p0_retrain']:
  old=[r[f'{measure}_old_pp'] for r in rs]
  new=[r[f'{measure}_new_pp'] for r in rs]
  delta=[r[f'{measure}_delta_pp'] for r in rs]
  q[f'{measure}_old_mean']=statistics.mean(old);q[f'{measure}_old_sd']=statistics.stdev(old) if len(old)>1 else None
  q[f'{measure}_new_mean']=statistics.mean(new);q[f'{measure}_new_sd']=statistics.stdev(new) if len(new)>1 else None
  q[f'{measure}_delta_mean']=statistics.mean(delta);q[f'{measure}_delta_sd']=statistics.stdev(delta) if len(delta)>1 else None
 q['selection_same_n']=sum(r['selection_same'] for r in rs)
 q['method_hits']=sum(r['gnn_cell_cache']=='hit' for r in rs)+sum(r['retrain_cell_cache']=='hit' for r in rs)
 q['method_misses']=sum(r['gnn_cell_cache']=='miss' for r in rs)+sum(r['retrain_cell_cache']=='miss' for r in rs)
 sum053.append(q)
writecsv(OUT/'AAGU-053-summary-18-groups.csv',sum053)

# Dataset-level facts and compact tables.
d053_summary={}
for ds in ['Cora','CiteSeer','PubMed']:
 rr=[r for r in a053 if r['dataset']==ds]
 d053_summary[ds]={
  'n_pairs':len(rr),'same_selection_n':sum(r['selection_same'] for r in rr),
  'old_gu_mean_pct':statistics.mean(r['gu_old_pct'] for r in rr),
  'new_gu_mean_pct':statistics.mean(r['gu_new_pct'] for r in rr),
  'gu_delta_mean_pp':statistics.mean(r['gu_delta_pp'] for r in rr),
  'old_retrain_mean_pct':statistics.mean(r['retrain_old_pct'] for r in rr),
  'new_retrain_mean_pct':statistics.mean(r['retrain_new_pct'] for r in rr),
  'retrain_delta_mean_pp':statistics.mean(r['retrain_delta_pp'] for r in rr),
  'old_gap_mean_pp':statistics.mean(r['gap_old_pp'] for r in rr),
  'new_gap_mean_pp':statistics.mean(r['gap_new_pp'] for r in rr),
  'gap_delta_mean_pp':statistics.mean(r['gap_delta_pp'] for r in rr),
  'old_p0_minus_gu_mean_pp':statistics.mean(r['p0_old_pct']-r['gu_old_pct'] for r in rr),
  'new_p0_minus_gu_mean_pp':statistics.mean(r['p0_new_pct']-r['gu_new_pct'] for r in rr),
  'p0_minus_gu_delta_mean_pp':statistics.mean(r['p0_gu_delta_pp'] for r in rr),
  'old_p0_minus_retrain_mean_pp':statistics.mean(r['p0_old_pct']-r['retrain_old_pct'] for r in rr),
  'new_p0_minus_retrain_mean_pp':statistics.mean(r['p0_new_pct']-r['retrain_new_pct'] for r in rr),
  'p0_minus_retrain_delta_mean_pp':statistics.mean(r['p0_retrain_delta_pp'] for r in rr)
 }
# exact counts per selector and method cache
cache053={}
for method in ['GNNDelete','Retrain']:
 cc=[c for c in run053['cells'] if c['conditions']['method']==method]
 cache053[method]={'n':len(cc),'method_cache':dict(collections.Counter(c['cache']['method'] for c in cc)),
   'producer_called':dict(collections.Counter(str(c['producer_called'].get('method')) for c in cc))}
summary={
 'artifacts':{
  '032':{'run_id':run032['run_id'],'commit':run032['commit'],'cells':len(m032),'checksum_verified_files':sum(len(c['files']) for c in run032['cells']),
         'cache_method':dict(collections.Counter(c['cache']['method'] for c in run032['cells'])),
         'producer_called':dict(collections.Counter(str(c['producer_called'].get('method')) for c in run032['cells']))},
  '053':{'run_id':run053['run_id'],'commit':run053['commit'],'cells':len(m053),'checksum_verified_files':sum(len(c['files']) for c in run053['cells']),
         'cache_method':dict(collections.Counter(c['cache']['method'] for c in run053['cells'])),
         'producer_called':dict(collections.Counter(str(c['producer_called'].get('method')) for c in run053['cells'])),
         'cache_by_method':cache053}
 },
 '032':{'old_new_pairs':len(a032),'selection_ids_same':sum(r['selection_id_same'] for r in a032),
        'output_recipes_same':sum(r['output_recipe_hash_old']==r['output_recipe_hash_new'] for r in a032),
        'datasets':d032_summary,'degree_vs_dfull':d032_effect,'core_tables':t032},
 '053':{'old_new_pairs':len(a053),'selection_ids_same':sum(r['selection_same'] for r in a053),
        'datasets':d053_summary,'groups':sum053}
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({
 'out':str(OUT),
 '032':summary['artifacts']['032'],
 '032_condition_deltas':{ds:{'mean_delta_pp':round(vals['all_condition_delta_mean_pp'],3),'range': [round(x,3) for x in vals['delta_range_pp']],'selection_id_same':vals['selector_id_same']} for ds,vals in d032_summary.items()},
 '032_dfull_vs_degree':d032_effect,
 '053':summary['artifacts']['053'],
 '053_datasets':{ds:{k:round(v,3) for k,v in vals.items() if k.endswith('mean_pct') or k.endswith('mean_pp')} for ds,vals in d053_summary.items()},
},ensure_ascii=False,indent=2))
