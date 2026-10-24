"""Bounded, local-only adoption inventory. Does not modify source or live state."""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import html
import json
import math
import statistics as stats
import subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
FIX='self/research/analyses/EXP-011_EXP-079/'
BUD='self/research/analyses/EXP-080/full-20261021/'
AUD='paper_writing/review/2026-10-24-self-audit/'
R2='paper_writing/review/2026-10-24-round2/'
manifest={};checks=[]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):
    p=ROOT/path;manifest[path]=dict(sha256=sha(p),bytes=p.stat().st_size)
    return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(path):
    p=ROOT/path;manifest[path]=dict(sha256=sha(p),bytes=p.stat().st_size)
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def verify(path,expected,scope):
    actual=sha(ROOT/path);assert actual==expected,(path,actual,expected)
    checks.append(dict(path=path,check=scope,sha256=actual))
def close(a,b):assert math.isclose(float(a),float(b),abs_tol=1e-8,rel_tol=1e-10),(a,b)
def write(name,rs):
    if not rs:return
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def accept_method(r):return r['method']!='GNNDelete'
def method_semantics(method):
    if method=='GraphRevoker':return 'as-implemented GPA+optimal project variant; full original-paper contrastive aggregation not reproduced; per-Output creating producer not reaudited here'
    if method=='GraphEraser':return 'as-implemented project instance; complete original-paper fidelity not audited; per-Output creating producer not reaudited here'
    return 'method-specific implementation limitations remain; this inventory is not a paper-fidelity certification'
def evidence(r,scope):return {**r,'adoption_scope':scope,'independent_method_evidence':r.get('method')!='IDEA','method_semantics':method_semantics(r.get('method'))}
def summarize(values):
    mean=stats.mean(values);sd=stats.stdev(values);half=2.2621571628540993*sd/math.sqrt(len(values))
    return dict(n=len(values),mean=mean,sd=sd,lo=mean-half,hi=mean+half)


def main():
    outline=ROOT/'paper_writing/outline/OUTLINE.md'
    assert '详细提纲 v6' in outline.read_text(encoding='utf-8')
    manifest['paper_writing/outline/OUTLINE.md']=dict(sha256=sha(outline),bytes=outline.stat().st_size)
    for path in (AUD+'inventory/INVENTORY.md',R2+'ANALYSIS_REVIEW.md',R2+'EXPERIMENT_REVIEW.md','self/research/experiments/drafts/round3-positioning/POSITIONING_MEMO.md'):
        manifest[path]=dict(sha256=sha(ROOT/path),bytes=(ROOT/path).stat().st_size)
    for path in ('.workblock/items/AAGU-101/REPORT.md','.workblock/items/AAGU-105/REPORT.md',FIX+'REPORT.md',AUD+'validity/VALIDITY.md'):
        manifest[path]=dict(sha256=sha(ROOT/path),bytes=(ROOT/path).stat().st_size)
    # Bounded execution-checkout check. It does not retroactively bind every HIT
    # to its original producer and does not certify original-paper fidelity.
    execution_sha='bab1781e182254e0b02cbeb1de138d58f7f1cd50'
    accepted_fix='7491b59dab42635b64aecd5c463d5d7047c70447'
    paths={'GraphEraser':'GULib-master/unlearning/unlearning_methods/GraphEraser/aggregation/optimal_aggregator.py','GraphRevoker':'GULib-master/unlearning/unlearning_methods/GraphRevoker/lib_aggregator/optimal_aggregator.py'}
    semantics=[]
    for method,path in paths.items():
        blobs=subprocess.check_output(['git','rev-parse',execution_sha+':'+path,accepted_fix+':'+path],cwd=ROOT,text=True,encoding='utf-8').splitlines()
        assert len(blobs)==2 and blobs[0]==blobs[1]
        semantics.append(dict(method=method,execution_sha=execution_sha,accepted_fix_candidate=accepted_fix,path=path,execution_blob=blobs[0],accepted_fix_blob=blobs[1],double_softmax_status='corrected at executed checkout; same code as accepted A101 fix',per_output_original_producer_binding='not reaudited in this bounded pass',paper_fidelity='NOT established; '+method_semantics(method),allowed_use='named project instance, conditional descriptive source boundary only',excluded_use='original-paper algorithm defect/fidelity assertion; independent validation of new A; unqualified current original-algorithm comparison'))
    (OUT/'METHOD_SEMANTICS.json').write_text(json.dumps(semantics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    hashes=load(FIX+'derived_data_hashes.json')
    for name in ('cells.csv','seed_values.csv','summary.csv','paired_seed_values.csv','paired_vs_random.csv'):
        verify(FIX+name,hashes[name],'current CSV matches prior audited derived-data hash')
    audit=load(AUD+'analysis/validation.json');assert audit['passed']
    assert load(AUD+'analysis/independent_validation.json')['passed']
    for path,expected in audit['input_sha256'].items():verify(path.replace('\\','/'),expected,'claim_audit input bytes unchanged')
    hop_audit=load(AUD+'inventory/HOP_VALIDATION.json');assert hop_audit['passed']
    # Rehash the five run manifests and saved delivery receipts, not all cell files.
    for source in hop_audit['source_runs']:
        verify(source['run'],source['sha256'],'current source manifest matches previous full audit')
        verify(source['delivery'],source['delivery_sha256'],'saved trusted-delivery bytes unchanged')
        receipt=load(source['delivery']);assert receipt['result']['status']=='accepted' and receipt['result']['project_acceptance']['passed']
    input_audit=load(FIX+'input_audit.json');budget_audit=load(BUD+'verification.json')
    sv=load(BUD+'statistics_validation.json');assert sv['passed']
    verify(BUD+'cells.csv',sv['input_sha256'],'prior 51720-check budget audit input unchanged')

    cells=rows(FIX+'cells.csv');seeds=rows(FIX+'seed_values.csv');summary=rows(FIX+'summary.csv')
    paired=rows(FIX+'paired_seed_values.csv');random_summary=rows(FIX+'paired_vs_random.csv')
    source_direct=rows(AUD+'analysis/source_strategy_contrasts.csv')
    source_direct_seed=rows(AUD+'analysis/source_strategy_seed_contrasts.csv')
    # Recalculate all adopted source direct contrasts from audited seed endpoints.
    ix={(r['dataset'],r['method'],r['source'],r['selector'],r['seed']):r for r in seeds if r['experiment']=='EXP-079'}
    direct_values=defaultdict(list);direct_checked=0
    for r in source_direct_seed:
        if not accept_method(r):continue
        left,right=r['contrast'].split('-minus-');src=r['source'];d=r['dataset'];m=r['method'];seed=r['seed']
        a=ix[d,m,src,left,seed];b=ix[d,m,'baseline' if right=='degree' else src,right,seed]
        for out,key in [('accuracy_delta','after'),('disagreement_delta','flip')]:
            if not a[key] or not b[key]:assert not r[out];continue
            value=float(a[key])-float(b[key]);close(value,r[out]);direct_checked+=1
            direct_values[d,m,src,r['contrast'],out].append(value)
    for r in source_direct:
        if not accept_method(r):continue
        vals=direct_values[r['dataset'],r['method'],r['source'],r['contrast'],r['metric']]
        assert len(vals)==int(r['n'])
        if vals:
            for k,v in summarize(vals).items():close(v,r[k]);direct_checked+=1
    # Full source-family against Random: preserve all sources/methods, no winning-only slice.
    source_random=[r for r in random_summary if r['experiment']=='EXP-079' and accept_method(r)]
    source_endpoints=[evidence(r,'e79r6 current shard300; source comparison only') for r in summary if r['experiment']=='EXP-079' and accept_method(r)]
    source_groups=defaultdict(list)
    for r in source_random:
        if r['selector'] in ('r_point','gt_full') and r['metric']=='after':source_groups[r['dataset'],r['method'],r['selector']].append(r)
    scope=[]
    for (d,m,s),rr in sorted(source_groups.items()):
        assert len(rr)==4
        by={r['source']:r for r in rr}
        scope.append(dict(dataset=d,method=m,selector=s,independent_method_evidence=m!='IDEA',method_semantics=method_semantics(m),
            **{source+'_delta_accuracy_pp':float(by[source]['mean']) for source in ('GCN','SGC','GAT','GIN')},
            below_zero_pointwise_intervals=sum(float(r['hi'])<0 for r in rr),above_zero_pointwise_intervals=sum(float(r['lo'])>0 for r in rr),
            min_mean_pp=min(float(r['mean']) for r in rr),max_mean_pp=max(float(r['mean']) for r in rr)))
    write('source_endpoints.csv',source_endpoints)
    write('source_direct_contrasts.csv',[evidence(r,'exploratory paired joint-seed; pointwise intervals') for r in source_direct if accept_method(r)])
    write('source_random_contrasts.csv',[evidence(r,'shared Random baseline; pointwise intervals') for r in source_random])
    write('source_scope.csv',scope)
    fixed=[evidence(r,'e11r1 current shard300; fixed10pct') for r in summary if r['experiment']=='EXP-011' and accept_method(r)]
    write('fixed10_endpoints.csv',fixed)
    write('fixed10_random_contrasts.csv',[evidence(r,'e11r1; Random10/IM3 averaged within seed') for r in random_summary if r['experiment']=='EXP-011' and accept_method(r)])
    # All common-condition Output identities retained for valid methods only.
    common=rows(AUD+'analysis/common_condition_output_identity.csv')
    write('common_output_identity.csv',[r for r in common if accept_method(r)])

    bcells=rows(BUD+'cells.csv');bseed=rows(BUD+'seed_values.csv');bsum=rows(BUD+'condition_summary.csv')
    # Independently recompute full seven-point nonshard means from audited raw-cell CSV.
    bgroups=defaultdict(list)
    for r in bcells:
        if r['method'] in ('GIF','IDEA','MEGU','Retrain'):bgroups[r['dataset'],r['method'],r['selector'],r['ratio'],r['seed']].append(r)
    bindex={(r['dataset'],r['method'],r['selector'],r['ratio'],r['seed']):r for r in bseed}
    cindex={(r['dataset'],r['method'],r['selector'],r['ratio']):r for r in bsum}
    bchecks=0;by_condition=defaultdict(list)
    for key,rs in bgroups.items():
        row=bindex[key];by_condition[key[:-1]].append(row)
        for metric in ('accuracy','cross_entropy','disagreement','retrain'):
            vals=[float(r[metric]) for r in rs if r[metric]]
            if not vals:assert not row[metric];continue
            close(stats.mean(vals),row[metric]);bchecks+=1
    for key,rs in by_condition.items():
        for metric in ('accuracy','cross_entropy','disagreement','retrain'):
            vals=[float(r[metric]) for r in rs if r[metric]]
            if not vals:continue
            close(stats.mean(vals),cindex[key][metric+'_mean']);close(stats.stdev(vals),cindex[key][metric+'_std']);bchecks+=2
    write('budget_current_nonshard.csv',[evidence(r,'080 GIF/IDEA/MEGU/Ret; 7 budgets, original evaluation graph') for r in bsum if r['method'] in ('GIF','IDEA','MEGU','Retrain')])
    write('budget_historical_shards.csv',[evidence(r,'historical 080 shard implementation; NOT current shard300 result') for r in bsum if r['method'] in ('GraphEraser','GraphRevoker')])
    ratios=(.05,.075,.1,.15,.22,.33,.5);curves=[];curvepoints=[]
    for d in ('Cora','CiteSeer'):
        for m in ('GIF','MEGU'):
            for baseline in ('random','degree'):
                means=[]
                for ratio in ratios:
                    a=cindex[d,m,'r_point',str(ratio)];b=cindex[d,m,baseline,str(ratio)]
                    vals=[float(bindex[d,m,'r_point',str(ratio),seed]['disagreement'])-float(bindex[d,m,baseline,str(ratio),seed]['disagreement']) for seed in ('42','212','2024')]
                    val=stats.mean(vals);close(val,float(a['disagreement_mean'])-float(b['disagreement_mean']));means.append(val)
                    curvepoints.append(dict(dataset=d,method=m,baseline=baseline,ratio=ratio,D_difference_pp=val,SD_pp=stats.stdev(vals),
                        request_GU_accuracy_pct=a['accuracy_mean'],reference_GU_accuracy_pct=b['accuracy_mean'],request_Ret_accuracy_pct=a['retrain_mean'],reference_Ret_accuracy_pct=b['retrain_mean'],request_D_pct=a['disagreement_mean'],reference_D_pct=b['disagreement_mean']))
                curves.append(dict(dataset=d,method=m,baseline=baseline,**{'r'+str(r):v for r,v in zip(ratios,means)},
                    descending_adjacent_steps=sum(b<a-1e-10 for a,b in zip(means,means[1:])),all_points_positive=all(v>1e-10 for v in means)))
    write('budget_seven_point_curves.csv',curvepoints);write('budget_shape_summary.csv',curves)
    geometry=rows(AUD+'inventory/request_geometry_summary.csv');hops=rows(AUD+'inventory/hop_summary.csv')
    write('fixed10_geometry.csv',[r for r in geometry if r['experiment']=='EXP-011'])
    write('fixed10_hops.csv',[evidence(r,'different selector bands have different node memberships; descriptive only') for r in hops if r['experiment']=='EXP-011' and accept_method(r)])

    costs=load(AUD+'inventory/EXP014_collected_selector_audit.json')
    for r in costs:
        verify(r['selection_file'],r['selection_sha256'],'014 Selection bytes physically rehashed now')
        selected=load(r['selection_file'])['selected_nodes']
        assert len(selected)==len(set(selected))==5927 and min(selected)>=0 and max(selected)<169343
    e14=load('self/research/experiments/EXP-014.json');timeout=load('.syncmate/exp014-launch-20261024/rr65536-timeout.json')
    assert timeout['job']['error_code']=='recipe_timeout' and timeout['job']['state']=='failed'
    for job in ('exp014-20261024-e14b1','exp014-20261024-e14r3'):
        delivery=load('.syncmate/deliveries/'+job+'.json');assert delivery['result']['status']=='accepted' and delivery['result']['project_acceptance']['passed']
    rr=load('.workblock/items/AAGU-056/evidence/execution-20260911/closeout-verification.json');assert rr['status']=='PASS'
    rr_collection=load('.workblock/items/AAGU-056/evidence/execution-20260911/collection.json');assert rr_collection['status']=='accepted'
    costrows=[dict(selector=r['selector'],configuration='014 5% k5927',status='accepted_execution',cell_access_seconds=r['access_wall_seconds'],model_prepare_seconds=r['exclusive_phases'].get('model_prepare'),selector_access_seconds=r['exclusive_phases']['selector_access'],selector_compute_seconds=r['selection_seconds'],job_wall_seconds=r['job_wall_seconds'],shared_job_wall=r['job_wall_shared'],sampled_container_peak_GiB=None,evidence_level='receipt reread + Selection hash/count recheck; candidate membership inherited from acceptance') for r in costs]
    costrows.extend([
        dict(selector='IM-RR1024',configuration='056 5% k5927 seed11',status='accepted_execution_historical',cell_access_seconds=None,model_prepare_seconds=None,selector_access_seconds=None,selector_compute_seconds=rr['selection_seconds'],job_wall_seconds=rr['resources']['elapsed_seconds'],shared_job_wall=False,sampled_container_peak_GiB=rr['resources']['sampled_cgroup_peak_bytes']/1024**3,evidence_level='historical accepted audit reread; raw artifacts NOT rehashed in this pass'),
        dict(selector='IM-RR65536',configuration='014 5% k5927 seed11',status='recipe_timeout_at_7200s',cell_access_seconds=None,model_prepare_seconds=None,selector_access_seconds=None,selector_compute_seconds=None,job_wall_seconds=7202.0,shared_job_wall=False,sampled_container_peak_GiB=None,evidence_level='exact terminal job receipt; no trusted completed result; cache completion stage unknown'),
        dict(selector='D-full',configuration='014 planned 5% k5927',status='not_submitted',cell_access_seconds=None,model_prepare_seconds=None,selector_access_seconds=None,selector_compute_seconds=None,job_wall_seconds=None,shared_job_wall=None,sampled_container_peak_GiB=None,evidence_level='current EXP014 state and timeout receipt; no result')])
    attempts={a['run_id']:a for a in e14['attempts']}
    for r in costrows:
        selector=r['selector']
        rid={'random':'e14b1','degree':'e14b1','r_point':'e14r3','IM-RR65536':'e14r4'}.get(selector)
        r['execution_sha']=attempts[rid]['git_sha'] if rid else rr['git_sha'] if selector=='IM-RR1024' else None
        r['job_id']=attempts[rid]['job_id'] if rid else 'aagu056-rr1024-v1' if selector=='IM-RR1024' else None
        r['wall_boundary']='process elapsed, not Core whole-job wall' if selector=='IM-RR1024' else 'Core whole-job excluding queue/return' if rid else None
        r['node']='gpu4090' if selector!='D-full' else None
        r['hardware_validation']='node identity only; hardware utilization/device-specific time not independently reverified'
        r['cache_observation']='score/Selection MISS; producer called' if selector in ('random','degree','r_point') else 'Selector MISS; actual call recorded in historical accepted report' if selector=='IM-RR1024' else 'unknown/no trusted completed result' if selector=='IM-RR65536' else 'not run'
    write('selector_costs.csv',costrows)

    claims=[
        dict(id='S1',target='Q1 / F2 / Appendix C',claim='Fixed10 complete mechanism context and method/data counterexamples',sources=[FIX+'summary.csv',FIX+'paired_vs_random.csv'],outputs=['fixed10_endpoints.csv','fixed10_random_contrasts.csv'],filter='e11r1; exclude GNNDelete; IDEA visible but not independent',admission='adopt descriptive support; not new A replication',figure_action='Regenerate F2 with all 3 datasets x 6 endpoint columns; show full 8 settings in Appendix C; old plots contain excluded method and cannot be pasted unchanged'),
        dict(id='S2',target='Q1 local interpretation / R0 / Appendix C',claim='Coverage and disagreement are distinct, with explicit far-band and composition counterexamples',sources=[AUD+'inventory/request_geometry_summary.csv',AUD+'inventory/hop_summary.csv',AUD+'inventory/HOP_VALIDATION.json'],outputs=['fixed10_geometry.csv','fixed10_hops.csv'],filter='e11r1; no GNNDelete; all bands and denominators retained',admission='historical full metric audit + current source manifest rehash; no fresh metric-cell rehash',figure_action='Pair within-band D with band share; never overlay different node populations as paired intervention'),
        dict(id='S3',target='Q3 / T3 / Appendix E',claim='Source boundary of directly paired request effects, including signs that change',sources=[FIX+'seed_values.csv',FIX+'paired_vs_random.csv',AUD+'analysis/source_strategy_contrasts.csv'],outputs=['source_endpoints.csv','source_direct_contrasts.csv','source_random_contrasts.csv','source_scope.csv'],filter='e79r6; 3 datasets x 4 sources x all eligible methods; remove old GNNDelete and margin family',admission='current derived hashes + all adopted direct differences independently recomputed; 10 joint seeds',figure_action='T3 compact range and examples; Appendix E all direct pair intervals + raw GU/Ret values; shared Degree/Random not duplicated as independent observations'),
        dict(id='S4',target='Q2 / F3 / Appendix D',claim='Seven-budget shape bounds the 5-to-33 exploratory interaction',sources=[BUD+'cells.csv',BUD+'seed_values.csv',BUD+'condition_summary.csv'],outputs=['budget_current_nonshard.csv','budget_seven_point_curves.csv','budget_shape_summary.csv'],filter='GIF/MEGU main; IDEA duplicate coordinate; Ret visible; all 7 points',admission='current audited raw CSV hash + seed/mean/SD recomputation; not new graph control result',figure_action='Main 2 datasets x 2 GU with R-point minus Random/Degree; preserve small dips and zero/negative early points, raw GU/Ret table adjacent'),
        dict(id='S5',target='Appendix D historical implementation boundary',claim='Historical shard curves constrain scope but do not describe current shard300 implementation',sources=[BUD+'condition_summary.csv',AUD+'analysis/common_condition_output_identity.csv'],outputs=['budget_historical_shards.csv','common_output_identity.csv'],filter='080 old GraphEraser/GraphRevoker only; no GNNDelete',admission='historical-only panel; Cora50% absent, never zero-imputed',figure_action='Separate old-protocol panel; never splice e79r6 10% into 080 curve'),
        dict(id='S6',target='Appendix B / Table B3',claim='Actual selector cost includes successful requests and a timed-out intended setting',sources=[AUD+'inventory/EXP014_collected_selector_audit.json','.workblock/items/AAGU-056/evidence/execution-20260911/closeout-verification.json','.syncmate/exp014-launch-20261024/rr65536-timeout.json'],outputs=['selector_costs.csv'],filter='014 Random/Degree/R-point; historical 056 RR1024; failed 014 RR65536; D-full absent',admission='014 Selection physically rechecked; 056 historical audit only; failure receipt current',figure_action='Table separated stage clocks/config/version/cache; replace v6 running with timeout, no acceleration ratio or large-graph GU claim'),
        dict(id='S7',target='Experimental design / Appendix A',claim='Existing calibration, no-update and training diagnostics support implementation validity within their own scope',sources=[AUD+'inventory/INVENTORY.md',AUD+'inventory/EXP082_validation_audit.json',AUD+'validity/calibration_summary.json'],outputs=[],filter='062/065-068 fixed PT Random10%;078 isolated baseline diagnostics;082 corrected shard trajectories',admission='historical inventory only in this pass; no new physical validation; cannot replace strategic B Ret/no-update controls',figure_action='Short validity scope table, not extra RQ or independent scientific replication'),
        dict(id='X1',target='Excluded / unresolved',claim='No adoption of old GNNDelete, all-method source margins, new-target generalization or causal mechanism',sources=[R2+'EXPERIMENT_REVIEW.md','self/research/experiments/drafts/round3-positioning/POSITIONING_MEMO.md'],outputs=[],filter='all old GNNDelete rows excluded; shared outputs and GIF/IDEA never independent',admission='not supported; pending A/B controls governed elsewhere',figure_action='Old figure files cannot be reused unchanged; A/B new evidence is separately adjudicated')]
    for claim in claims:
        if claim['id'] in ('S1','S2','S3','S5'):
            claim['method_semantics_boundary']='GraphEraser/GraphRevoker are named as-implemented instances only, never fidelity-certified original algorithms; see METHOD_SEMANTICS.json. Execution-code A101 fix is verified for 011/079, per-Output creating producer not reaudited; 080 historical protocol stays separate.'
            claim['figure_action']+=' Label both shard methods as project instances in axes/caption. If a table claims faithful original-algorithm comparison, omit these coordinates or move them to an explicitly variant-labelled appendix.'
    payload=dict(status='support_inventory_only',scientific_gate='not_adjudicated',new_gpu_runs=0,new_methods=0,claims=claims,
        method_semantics=semantics,
        verification=dict(source_direct_numeric_checks=direct_checked,budget_raw_seed_summary_checks=bchecks,physical_hash_checks=len(checks),
            not_rechecked='011/079/080 individual returned cells, Dataset/model payloads, 056 original files and validity archives; rely on named historical audits for these'),
        scope_counts=dict(fixed10_rows=len(fixed),source_endpoint_rows=len(source_endpoints),source_direct_rows=sum(accept_method(r) for r in source_direct),source_family_rows=len(scope),budget_nonshard_conditions=280,budget_historical_shard_conditions=130,seven_point_curves=8),source_manifest=manifest,physical_checks=checks)
    (OUT/'CLAIM_SOURCE_FIGURE_MAP.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    render(payload,scope,curves,costrows,summary,geometry,hops)
    print(json.dumps({k:payload[k] for k in ('status','verification','scope_counts')},ensure_ascii=False))


def render(payload,scope,curves,costs,summary,geometry,hops):
    md=[];body=[]
    def heading(t):md.append('## '+t+'\n');body.append('<h2>'+html.escape(t)+'</h2>')
    def para(t):md.append(t+'\n');body.append('<p>'+html.escape(t)+'</p>')
    def table(columns,rr):
        vals=[[f'{r[k]:.3f}' if isinstance(r[k],float) else str(r[k]) for k in columns] for r in rr]
        md.append('| '+' | '.join(columns)+' |\n| '+' | '.join('---' for _ in columns)+' |\n'+'\n'.join('| '+' | '.join(v)+' |' for v in vals)+'\n')
        body.append('<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in columns)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in v)+'</tr>' for v in vals)+'</tbody></table></div>')
    title='第三轮已有证据采用清单：完整范围、反例与成本'
    md.append('# '+title+'\n');body.append('<h1>'+title+'</h1>')
    para('结论：已有011/079/080材料足够支撑完整范围与反例，不必把主文限制成A/B几个有利坐标。但它们只承担科学发现的背景、边界和实际量级；“策略不同”本身不构成新的核心贡献。A的确认、B的端点解释及两图/C&S/Ret质量门槛仍由冻结协议独立判断，本清单不提前放行写作。')
    para('本轮仅本地只读整理。当前v6提纲和第一/二轮审查为采用依据；所有输出在本独有ignored目录。采用CSV完全排除历史GNNDelete，保留IDEA原值但标记不增加独立方法证据；080历史分片另表。没有新增GPU、方法或主张，也没有改动提纲或Work Plan状态。')
    heading('1. 可执行的图表采用表')
    table(['id','target','admission','figure_action'],payload['claims'])
    para('每项精确输入、筛选规则、待生成图及输出文件写入CLAIM_SOURCE_FIGURE_MAP.json。旧011/079图册含已隔离GNNDelete，旧080图册还混有历史分片，不能直接粘贴进最终论文；必须由这里的限定CSV重绘。这里给采用计划与数据，不冒充已经排版完成的论文图。')
    heading('1.1 分片方法语义：修正聚合损失，不等于忠实复现原算法')
    para('已有A101/A105记录明确：两方法交叉熵前多余softmax已修正，并进入独立shard_epochs=300的正式配置；本轮又只读比较e11r1/e79r6执行SHA bab1781与A101修正候选7491b59，两聚合器Git blob分别完全相同（GraphEraser d9cee2f5f8b569658825b1160837ae43b4301396；GraphRevoker 3b06716899f41b09edd9689f790512694b72ed53）。所以不能把079简单归为仍执行旧double-softmax的结果；但这一核验只绑定执行checkout代码，并未逐个追溯所有HIT Output的原始MISS producer。表格字节正确不能代替方法语义审计。')
    para('GraphRevoker已知仍是项目GPA+optimal变体，A101明确没有补齐原论文全部模块，e79r6原报告也明确未转成完整对比聚合实现。GraphEraser已确认共同loss修正，但本清单没有对其全流程与原论文逐模块做忠实性审计。因此079两者仅可命名为as-implemented项目实例，用于条件性source描述和反例；不能将Cora/GIN与SGC反例写成已证实的原论文算法性质、缺陷或新A的跨source确认。')
    para('具体采用边界：在明确列出实现、聚合、分片预算和运行身份的经验表中保留原值，轴标签/图注同时标明项目实例；如主文表宣称比较忠实复现的原论文算法，则两者应移出该表或进入单独变体附录，待具体producer/完整方法审计后再决定更强采用。尚无证据要求把整个079分片矩阵当数值损坏隔离；必须隔离的是不带实现限定的算法级论断。旧080分片仍仅作其原历史协议记录，旧GNNDelete仍全部隔离，不因本段恢复。METHOD_SEMANTICS.json保留已知证据和未审范围。')
    heading('2. 011：让IM/topology进入主图，同时保留相反条件')
    fi={(r['dataset'],r['method'],r['selector']):float(r['mean']) for r in summary if r['experiment']=='EXP-011' and r['metric']=='after'}
    fixedrows=[dict(dataset=d,method=m,**{s:fi[d,m,s] for s in ('random','degree','rr_65536','r_point','gt_full')}) for d in ('Cora','CiteSeer','PubMed') for m in ('GIF','MEGU','GraphEraser','GraphRevoker','Retrain')]
    table(['dataset','method','random','degree','rr_65536','r_point','gt_full'],fixedrows)
    para('表为10%预算accuracy原值（%），三联合运行均值；完整八设置、IDEA、CE、AUC、GU–Ret gap/D及点态区间在fixed10_endpoints.csv和fixed10_random_contrasts.csv。图F2可用相对Random变化压缩，但原始Ret与GU端点不能丢。PubMed GraphEraser在R-point为85.759%、Random为87.017%；CiteSeer对应75.125%与74.635%，方向不同。不能把单一选择器命名为普遍最强，或把高于Random解释为防御成功。GraphRevoker始终按当前已披露变体标注。')
    geo=[r for r in geometry if r['experiment']=='EXP-011' and r['selector'] in ('random','degree','rr_65536','r_point')]
    table(['dataset','selector','hop1_share_pct','within2_share_pct','gt3_share_pct'],geo)
    para('以上为test节点的距离带构成（%）；IM-RR65536两跳覆盖Cora/CiteSeer/PubMed为83.52/59.81/86.49%，R-point为53.32/37.34/57.75%。Cora GIF一跳D的R-point/IM为26.87/3.63%，MEGU为21.59/4.53%，而远处均近零；Cora GraphEraser在>3-hop仍为9.86/14.54%，GraphRevoker为18.63/14.08%。这些反例要求同图给每带分母：覆盖广不自动等于带内D大，带内D顺序不自动等于整体D顺序，也不能把不同selector的节点带当作配对因果处理。')
    heading('3. 079：来源采用应保留整个家族，而不是只留PubMed示例')
    table(['dataset','method','selector','GCN_delta_accuracy_pp','SGC_delta_accuracy_pp','GAT_delta_accuracy_pp','GIN_delta_accuracy_pp'],[r for r in scope if r['selector']=='r_point' and r['method']!='IDEA'])
    para('表为R-point相对同seed内Random均值的accuracy差（pp），source_scope.csv另保留D-full与全部点态区间范围；source_direct_contrasts.csv覆盖D-full−R-point、R-point−Degree、D-full−Degree的accuracy与D，source_endpoints.csv保留GU/Ret原值。两分片行均按上节as-implemented语义解释：PubMed项目GraphEraser实例四source为−0.969/−0.421/−1.306/−0.695pp，各点态区间低于零，但Cora同实例在GIN为+0.498pp、SGC为−1.236pp，CiteSeer在GCN/GIN为正、GAT/SGC均值为负。只有在明确实例限定的T3中才可展示这些反例，不能只突出一致的一行，也不能据此声称原论文算法的source性质。')
    para('n=10是联合选点/训练流程。每dataset/source的R-point、D-full各十个不同Selection，Degree一份、Random三份跨seed复用；四source共享参照，不能当四次独立确认，也不是四目标backbone。完整源表包含五GU实现坐标加Ret，但GIF/IDEA近重合意味着独立方法模式不能按五份计。旧GNNDelete的方向频率、margin或源稳定性统计全部不采用。')
    heading('4. 080：七预算形态和原值决定5%→33%该怎么写')
    table(['dataset','method','baseline','r0.05','r0.075','r0.1','r0.15','r0.22','r0.33','r0.5','descending_adjacent_steps'],curves)
    para('表为D(R-point)−D(指定baseline)（pp），所有七个预算均保留；逐seed配对SD与两边GU/Ret accuracy及原始D在budget_seven_point_curves.csv。这里八条展示曲线中五条存在相邻预算均值回落，不能概括成全程单调：CiteSeer GIF相对Random在10%→15%为2.753→2.703pp，MEGU为3.604→3.353pp；Cora MEGU相对Degree在5%→7.5%为0.677→0。小幅回落也不单独证明总体非单调，只是要求保留观察曲线。')
    para('F3建议主画GIF/MEGU的两数据集、两baseline差值曲线，紧邻GU和Ret原始端点表。完整280个非分片/Ret条件原值在budget_current_nonshard.csv，IM三draw先seed内平均，保留IDEA但不作额外确认。CiteSeer33%时IM相对Random的D约+0.350/+0.234pp，R-point约+14.615/+14.815pp（GIF/MEGU）；这支持具体有限请求比较，不能解释成IM正确遗忘。Random/Degree每预算只有一份请求跨三seed复用；5%→33%为探索性端点，不是预设阈值或随机请求期望。')
    para('130个历史分片条件单列budget_historical_shards.csv。Cora50%两分片没有可用端点，必须留空/断线，不能补零；Cora历史GraphRevoker的R-point−Degree D差从5%到33%反而减少6.458±5.056pp，三个seed均负，仅作为旧协议边界，不移植为当前变体结论。共同10%非分片+Ret的72个可采用引用在079/080复用同一Output（另18个旧GNNDelete隔离），不能累加成独立证据；两分片的36个匹配引用均不同，不得将新079点接进旧080曲线。')
    heading('5. 大图成本必须包含未完成和超时')
    table(['selector','status','cell_access_seconds','model_prepare_seconds','selector_access_seconds','selector_compute_seconds','job_wall_seconds','sampled_container_peak_GiB'],costs)
    para('图规模169,343节点、118,540候选，k=5,927。014 Random/Degree同一完整job的wall均引用54s，不能相加成108s；各自cell访问为2.601/4.642s。R-point cell324.512s=模型准备48.060s+selector访问276.452s（另有极小调度差），完整job364s。selector_compute在不同实现中只覆盖其记录阶段，R-point的大头score访问275.244s不能被1.145s的末端选集提取掩盖。')
    para('014 IM-RR65536已recipe_timeout：7200s硬上限，Core完整wall7202s，无可信完成产物。v6仍写“运行中”已过时；应改成明确失败边界。D-full尚未提交，不填0。056 RR1024的selector366.546s、进程380.390s、5s采样容器峰值7.592GiB为历史已接受执行，原始文件本轮未重新物理核验；该内存不是精确进程峰值。RR1024与65536配置/版本不同，不能推加速比或外推完成耗时；全部成本结果没有大图GU/Ret端点。selector_costs.csv保留每行job、执行SHA、节点、缓存与计时边界；硬件利用率和device-specific时间本轮未复核。')
    heading('6. 验证层级与仍不可采用的内容')
    para(f"本轮物理SHA核对{payload['verification']['physical_hash_checks']}项；五个旧科学run的manifest及delivery字节与既有完整审计一致，当前CSV与既有哈希一致。重新计算{payload['verification']['source_direct_numeric_checks']}项已采用来源差/区间数值与{payload['verification']['budget_raw_seed_summary_checks']}项预算raw-cell→seed→均值/SD；014三份Selection重新核对哈希、5927唯一ID及范围。candidate-mask成员资格仍引用项目验收，本轮没有加载正式Dataset。")
    para('并未再次逐文件核验011/079/080全部returned cell或重算模型预测；历史可信链依赖input_audit、verification、HOP_VALIDATION、claim_audit及独立复核记录。Hop派生表本轮读取并记录哈希，原metric的5985文件核验沿用第一轮审计。056只重读历史accepted核验；062/065–068、078、082只是库存层引用，本轮未重核其payload。机器映射记录每个来源的当前哈希及这一边界，不把本次整理写成新完整科学验收。')
    para('可采用的有效性背景：固定PT、10%三个新Random请求的84格数值/非退化验证；baseline checkpoint诊断；分片300→3000验证变化±0.901pp。它们不能替代B战略大预算的Ret训练质量、同权重两图或matched C&S。既有Random多请求也不是同一固定请求的R–R重训噪声。没有目标backbone、多split、真实请求权限、因果传播、隐私泄漏或认证遗忘证据；这些强主张仍不能采用。')
    para('最终采用顺序：先由新A/B完成冻结门槛并确定具体新增认识；再以S1/S2给机制与空间边界，以S3限制source外推，以S4/S5展示完整预算及版本反例，以S6给可运行成本与失败。上述材料丰富证据范围，不增加核心发现数量，也不能用来掩盖A/B贡献不足。')
    (OUT/'REPORT.md').write_text('\n'.join(md),encoding='utf-8')
    style='body{max-width:1280px;margin:32px auto;padding:0 24px;font:16px/1.75 system-ui,"Microsoft YaHei",sans-serif;color:#243447}h1{font-size:30px}h2{margin-top:32px}.scroll{overflow:auto}table{border-collapse:collapse;font-size:13px}th,td{border:1px solid #cbd5e1;padding:8px;vertical-align:top}th{background:#eaf0f6;white-space:nowrap}tr:nth-child(even){background:#f8fafc}'
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="source-sha256" content="'+sha(OUT/'REPORT.md')+'"><title>'+title+'</title><style>'+style+'</style></head><body>'+''.join(body)+'</body></html>',encoding='utf-8')

if __name__=='__main__':main()
