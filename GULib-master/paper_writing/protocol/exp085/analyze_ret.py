"""Frozen, read-only Ret analysis over exact trusted returns; no training/SSH."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import math
import re
import statistics
import sys

sys.dont_write_bytecode = True

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OBS='retrain_validation_trace'
FILES={'selection.json','metrics.json','observers/'+OBS+'/result.json','observers/'+OBS+'/trace.jsonl'}


def require(ok, message):
    if not ok: raise ValueError(message)


def no_duplicates(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key: '+key)
        result[key]=value
    return result


def read(path):
    path=Path(path)
    def parse(text):
        return json.loads(text,object_pairs_hook=no_duplicates,
            parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON: '+x)))
    text=path.read_text(encoding='utf-8-sig')
    if path.suffix=='.jsonl':
        require(all(line.strip() for line in text.splitlines()),'blank JSONL observation')
        return [parse(line) for line in text.splitlines()]
    return parse(text)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def number(value, label, minimum=None, maximum=None):
    require(type(value) in (int,float) and math.isfinite(value),'invalid number: '+label)
    require(minimum is None or value>=minimum,'below bound: '+label)
    require(maximum is None or value<=maximum,'above bound: '+label)
    return value


def close(actual, expected, label, atol=1e-12, rtol=0.):
    number(actual,label);number(expected,label)
    require(abs(actual-expected)<=atol+rtol*abs(expected),'numeric mismatch: '+label)


def quantify(trace, diagnostic):
    require(len(trace)==3000,'trace must contain exactly 3000 observations')
    for epoch,row in enumerate(trace,1):
        require(type(row['epoch']) is int and row['epoch']==epoch,'unordered/duplicate/missing epoch')
        require(set(row)=={'epoch','train_loss','update_lr','validation_accuracy','validation_cross_entropy'},'unexpected trace columns')
        number(row['train_loss'],'train loss',0)
        number(row['validation_cross_entropy'],'validation CE',0)
        number(row['validation_accuracy'],'validation accuracy',0,1)
        number(row['update_lr'],'learning rate',0)
        require(row['update_lr']>0,'nonpositive learning rate')
    best_index=max(range(3000),key=lambda i:trace[i]['validation_accuracy'])
    best=trace[best_index]; final=trace[-1]
    require(diagnostic['epochs']==3000 and diagnostic['best']['epoch']==best_index+1
            and diagnostic['final']['epoch']==3000,'checkpoint selection is not earliest validation maximum/fixed final')
    for role,row in (('best',best),('final',final)):
        require(diagnostic[role]['checkpoint_role']==role,'endpoint role differs')
        for key in ('accuracy','cross_entropy'):
            close(diagnostic[role]['validation'][key],row['validation_'+key],role+' validation '+key)
            number(diagnostic[role]['test'][key],role+' test '+key,0,1 if key=='accuracy' else None)
    before=sum(r['validation_cross_entropy'] for r in trace[2000:2500])/500
    after=sum(r['validation_cross_entropy'] for r in trace[2500:3000])/500
    gap=best['validation_accuracy']-final['validation_accuracy']
    expected=dict(validation_accuracy_gap=gap,ce_2001_2500=before,ce_2501_3000=after,
        ce_relative_increase=(after-before)/before if before else None,
        ce_relative_increase_status='finite' if before else 'zero_to_positive' if after else 'both_zero',
        accuracy_trigger=gap>=.01,ce_trigger=(after>=1.1*before if before else after>0))
    expected['optimization_sensitive']=expected['accuracy_trigger'] or expected['ce_trigger']
    require(set(diagnostic['windows'])==set(expected),'unexpected window fields')
    for key,value in expected.items():
        actual=diagnostic['windows'][key]
        if type(value) in (int,float): close(actual,value,key)
        else: require(actual==value,'window decision differs: '+key)
    require(diagnostic['validation_graph']=='retained' and diagnostic['validation_mask']=='original_split_val_mask'
        and diagnostic['selection_rule']=='maximum_validation_accuracy_earliest_tie'
        and diagnostic['test_graph']=='original' and diagnostic['test_policy']=='fixed_best_and_final_only'
        and diagnostic['train_loss_semantics']=='pre_update_train_mode_cross_entropy'
        and diagnostic['validation_semantics']=='post_update_eval_mode_cross_entropy_and_accuracy','diagnostic protocol differs')
    return dict(best_epoch=best_index+1,best_validation_accuracy=best['validation_accuracy'],
        final_validation_accuracy=final['validation_accuracy'],validation_accuracy_gap_pp=100*gap,
        val_ce_2001_2500=before,val_ce_2501_3000=after,
        ce_relative_increase=expected['ce_relative_increase'],ce_relative_increase_status=expected['ce_relative_increase_status'],
        accuracy_trigger=expected['accuracy_trigger'],ce_trigger=expected['ce_trigger'],
        optimization_sensitive=expected['optimization_sensitive'],
        final_preupdate_train_ce=final['train_loss'],min_validation_ce=min(r['validation_cross_entropy'] for r in trace))


def exact_final(diagnostic):
    comparison=diagnostic['old_final_comparison']
    require(type(comparison['state_hash_equal']) is bool,'invalid state equality')
    for name in ('all_node_prediction_changes','test_prediction_changes'):
        require(type(comparison[name]) is int and comparison[name]>=0,'invalid prediction change count')
    number(comparison['maximum_absolute_logit_error'],'old-final logit error',0)
    return (comparison['state_hash_equal'] and comparison['all_node_prediction_changes']==0
        and comparison['test_prediction_changes']==0 and comparison['maximum_absolute_logit_error']==0)


def reconstruct_pair(metrics, expected_count):
    n=metrics['node_count'];require(type(n) is int and n==expected_count,'paired test denominator differs')
    require(metrics['correctness_order']==['GU','Ret'] and set(metrics['cells'])=={'00','01','10','11'},'paired correctness cells differ')
    for bits,cell in metrics['cells'].items():
        count,different=cell['count'],cell['disagreement_count']
        require(type(count) is int and type(different) is int and 0<=different<=count,'invalid paired counts')
        require((bits!='11' or different==0) and (bits not in ('01','10') or different==count),'impossible correctness/disagreement counts')
    require(sum(v['count'] for v in metrics['cells'].values())==n,'paired cells do not reconstruct N')
    different=sum(v['disagreement_count'] for v in metrics['cells'].values())
    require(type(metrics['disagreement_count']) is int and different==metrics['disagreement_count'],'paired cells do not reconstruct disagreement')
    expected={'disagreement':different/n if n else None,
        'gu_accuracy':sum(v['count'] for k,v in metrics['cells'].items() if k[0]=='1')/n if n else None,
        'retrain_accuracy':sum(v['count'] for k,v in metrics['cells'].items() if k[1]=='1')/n if n else None}
    for key,value in expected.items():
        if n: close(metrics[key],value,'paired '+key)
        else: require(metrics[key] is None,'empty class rate must be null')
    for key in ('gu_cross_entropy','retrain_cross_entropy'):
        if n: number(metrics[key],key,0)
        else: require(metrics[key] is None,'empty class CE must be null')
    return metrics


def validate_pair_classes(comparison, expected_count=666):
    metrics=reconstruct_pair(comparison['metrics'],expected_count)
    groups=comparison['by_class']
    require([v['class_id'] for v in groups]==list(range(6)),'all six CiteSeer classes required in label order')
    for group in groups:
        reconstruct_pair(group['metrics'],group['metrics']['node_count'])
    require(sum(g['metrics']['node_count'] for g in groups)==expected_count,'class counts do not reconstruct N')
    for bits in ('00','01','10','11'):
        for key in ('count','disagreement_count'):
            require(sum(g['metrics']['cells'][bits][key] for g in groups)==metrics['cells'][bits][key],'class aggregation differs: '+bits+'/'+key)
    for key in ('gu_cross_entropy','retrain_cross_entropy'):
        close(sum(g['metrics'][key]*g['metrics']['node_count'] for g in groups if g['metrics']['node_count'])/expected_count,metrics[key],'class weighted '+key)
    return metrics


def helper_for(frozen):
    path=ROOT/frozen['trusted_helper_path']
    require(sha(path)==frozen['trusted_helper_sha256'],'TrustedRun helper changed')
    spec=importlib.util.spec_from_file_location('ret_private_trusted_helper',path)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    # Its unchanged TrustedRun validates every receipt/hash/index relationship;
    # only this private module's decoder gains strict JSONL parsing.
    helper.read=read
    return helper


def check_frozen(path, expected_sha, formal=True):
    require(sha(path)==expected_sha,'frozen manifest checksum differs')
    frozen=read(path)
    require(frozen['status']==('frozen_before_ret_dispatch' if formal else 'prepared_not_formal_freeze'),'not an appropriate freeze state')
    require(frozen['seeds']==[42,212,2024] and frozen['selectors']==['r_point','random','degree'],'frozen matrix changed')
    require(frozen['source_dataset_index']==1 and frozen['dataset_fingerprint']=='5aff7d08d539f2f9a7d85c02b20f85aa94f0ca8ee15ecdf429d8c35fbf12f9ac','frozen Dataset differs')
    for ref in frozen['protocols']:
        require(sha(ROOT/ref['path'])==ref['sha256'],'frozen protocol changed')
    for key in ('analysis_script','analysis_plan','endpoint_audit_script'):
        require(sha(path.parent/frozen[key])==frozen[key+'_sha256'],key+' changed')
    source_path=path.parent/frozen['source_manifest']
    require(sha(source_path)==frozen['source_manifest_sha256'],'frozen source changed')
    for batch in frozen['batches']:
        require(sha(ROOT/batch['config_path'])==batch['config_sha256'],'configuration changed')
        require(sha(ROOT/batch['recipe_path'])==batch['recipe_sha256'],'Recipe changed')
    return frozen,read(source_path)


def validate_cell(cell, documents, ref, frozen, source, batch, commit):
    from cache_v2 import ArtifactRecipe
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    require(cell['conditions']==ref['conditions'] and cell['conditions']['dataset_index']==1,'source conditions changed')
    require(set(cell['files'])==FILES and 'output' not in cell,'new run must expose diagnostics, not masquerade as old Output')
    expected_source={key:source[key] for key in ('experiment_id','run_id','commit','run_sha256')}
    expected_source.update(cell_id=cell['cell_id'],output=ref['output'])
    require(cell['source']==expected_source,'exact old source binding changed')
    require(cell['selection_id']==ref['selection_id'],'Selection identity changed')
    selection=documents['selection.json']
    require(selection['selected_nodes']==ref['selected_nodes'] and selection['requested_k']==768,'ordered deletion request changed')
    require(cell['cache']=={'method':'disabled'} and cell['producer_called']=={'selection':False,'original':False,'method':True},'unexpected producer/cache lane')
    observers=cell['observers'];require(len(observers)==1,'unexpected Observers')
    observer=observers[0]; result=documents['observers/'+OBS+'/result.json']
    trace=documents['observers/'+OBS+'/trace.jsonl']
    for key in ('name','semantic_version','status','identity','parameters','implementation'):
        require(observer[key]==result[key],'Observer reference differs from result: '+key)
    require(result['name']==OBS and result['status']=='completed' and result['parameters']=={} and result['error'] is None,'Observer incomplete')
    require(result['implementation']==frozen['observer_implementation'],'Observer implementation changed')
    expected_events=[{'phase':'epoch_end','step':i} for i in range(1,3001)]+[{'phase':'training_complete','step':3000}]
    require(result['events']==expected_events,'Observer callback coverage differs')
    identity=result['identity']
    require(identity['commit']==commit and identity['conditions']==ref['conditions']
        and identity['source']==expected_source and identity['configuration_fingerprint']==batch['configuration_fingerprint']
        and identity['run_id']==batch['run_id'] and identity['experiment_id']==batch['experiment_id']
        and identity['cell_id']==cell['cell_id'],'Observer execution identity differs')
    old_identity=identity['output_identity'];pair=old_identity['pairing']
    require(ArtifactRecipe({'artifact_contract':OUTPUT_CONTRACT,**old_identity}).recipe_hash==ref['output']['recipe_hash'],'Output recipe identity differs')
    require(old_identity['target']['method']=='Retrain' and old_identity['selection']['artifact_id']==ref['selection_id']
        and pair['selected_nodes']==ref['selected_nodes'] and pair['model']['architecture']=='OpenGU.GCNNet','source Output fields differ')
    require(identity['training']==pair['training'] and identity['training']['epochs']==3000
        and identity['training']['seed']==ref['conditions']['seed']
        and identity['training']['optimizer']=='Adam' and identity['training']['scheduler']=='none','Ret training settings differ')
    require(identity['validation_graph_identity']==pair['training_graph_identity']
        and pair['deletion']['evaluation_graph']=='original','validation/test graph differs')
    require(identity['producer']=={'semantic_version':'ret-source-validation-diagnostics-v1',
        'implementation':frozen['producer_implementation']},'Ret replay producer changed')
    diagnostic=result['diagnostics']; stats=quantify(trace,diagnostic)
    for row in trace: close(row['update_lr'],identity['training']['lr'],'fixed learning rate')
    comparison=diagnostic['old_final_comparison']
    require(comparison['all_node_prediction_changes']<=3327 and comparison['test_prediction_changes']<=666
        and comparison['test_prediction_changes']<=comparison['all_node_prediction_changes'],'invalid prediction denominator')
    for key in ('accuracy','cross_entropy'):
        close(comparison['old_test'][key],ref['old_test'][key],'source old test '+key,
              atol=2e-6 if key=='cross_entropy' else 1e-12,rtol=2e-6 if key=='cross_entropy' else 0)
    for role in ('best','final'):
        endpoint=diagnostic[role]
        require(re.fullmatch('[0-9a-f]{64}',endpoint['state_hash']) is not None,'invalid endpoint state identity')
        for key,suffix in (('weights','.pt'),('predictions','.npz')):
            value=endpoint[key];path=PurePosixPath(value['path'])
            wanted=f'results/runtime/modular/{batch["run_id"]}/retrain_diagnostics/{cell["cell_id"]}/{role}{suffix}'
            require(str(path)==wanted and re.fullmatch('[0-9a-f]{64}',value['sha256']) is not None,'endpoint asset path/hash differs')
    expected_metrics={role+'_'+key:diagnostic[role]['test'][key] for role in ('best','final') for key in ('accuracy','cross_entropy')}
    expected_metrics.update(best_epoch=stats['best_epoch'],final_epoch=3000,
        best_validation_accuracy=stats['best_validation_accuracy'],final_validation_accuracy=stats['final_validation_accuracy'],
        optimization_sensitive=int(stats['optimization_sensitive']))
    rows=documents['metrics.json']['rows']
    require(len(rows)==1 and rows[0]['stage']==OBS and rows[0]['values']==expected_metrics,'summary metrics differ from validated trajectory/endpoints')
    base=dict(seed=ref['conditions']['seed'],selector=ref['conditions']['selector'],cell_id=cell['cell_id'],run_id=batch['run_id'])
    endpoints=[]
    for role,metrics in [('old_final',comparison['old_test'])]+[(role,diagnostic[role]['test']) for role in ('best','final')]:
        endpoints.append(dict(base,checkpoint_role=role,epoch=3000 if role=='old_final' else diagnostic[role]['epoch'],
            accuracy=metrics['accuracy'],cross_entropy=metrics['cross_entropy']))
    stats.update(base,old_final_exact=exact_final(diagnostic),
        new_final_minus_old_final_accuracy_pp=100*(diagnostic['final']['test']['accuracy']-comparison['old_test']['accuracy']),
        best_minus_final_test_accuracy_pp=100*(diagnostic['best']['test']['accuracy']-diagnostic['final']['test']['accuracy']),
        best_minus_final_test_ce=diagnostic['best']['test']['cross_entropy']-diagnostic['final']['test']['cross_entropy'],
        all_node_prediction_changes=comparison['all_node_prediction_changes'],test_prediction_changes=comparison['test_prediction_changes'],
        maximum_absolute_logit_error=comparison['maximum_absolute_logit_error'],state_hash_equal=comparison['state_hash_equal'])
    for key,value in cell['timing'].items(): number(value,key,0);stats[key]=value
    return stats,endpoints,[dict(base,**row) for row in trace]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frozen-manifest',type=Path,required=True);p.add_argument('--frozen-sha256',required=True)
    p.add_argument('--expected-commit');p.add_argument('--scope',choices=('pilot','complete'),default='pilot')
    p.add_argument('--check-preparation',action='store_true')
    p.add_argument('--endpoint-audit',nargs=2,action='append',default=[],metavar=('JSON','SHA256'))
    args=p.parse_args()
    frozen,source=check_frozen(args.frozen_manifest,args.frozen_sha256,formal=not args.check_preparation)
    helper=helper_for(frozen)
    if args.check_preparation:
        print(json.dumps({'prepared':True,'formal_dispatch_ready':False,'source_cells':len(source['cells'])}));return
    require(args.expected_commit and re.fullmatch('[0-9a-f]{40}',args.expected_commit),'exact execution SHA required')
    sys.path.insert(0,str(ROOT))
    audits={}
    for path,checksum in args.endpoint_audit:
        require(sha(path)==checksum,'endpoint audit checksum differs')
        audit=read(path)
        require(audit['status']=='passed' and audit['read_only'] is True and audit['producer_calls']==0
            and audit['index_unchanged'] is True and audit['execution_sha']==args.expected_commit
            and audit['forward_calls']==0 and audit['cache_mutations']==0 and audit['saved_predictions_only'] is True
            and audit['source_run_sha256']==source['run_sha256'] and audit['source_manifest_sha256']==frozen['source_manifest_sha256']
            and audit['frozen_manifest_sha256']==args.frozen_sha256
            and audit['audit_script_sha256']==frozen['endpoint_audit_script_sha256'],'endpoint audit failed or identity differs')
        run_id=audit['run_id'];require(run_id not in audits,'duplicate endpoint audit')
        audits[run_id]=audit
    selected_batches=frozen['batches'][:1 if args.scope=='pilot' else 2]
    require(set(audits)=={b['run_id'] for b in selected_batches},'exact endpoint audit coverage required')
    items=read(ROOT/'.syncmate/artifact_index.json')['peers']['gpu4090']['items']
    index={x['path']:x for x in items};require(len(index)==len(items),'duplicate trusted index paths')
    old=helper.TrustedRun(source['job_id'],source['experiment_id'],source['run_id'],index)
    require(sha(old.local_root/'run.json')==source['run_sha256'] and old.run['commit']==source['commit'],'trusted old run changed')
    refs={v['cell_id']:v for v in source['cells']}
    require(len(refs)==9,'frozen source matrix incomplete')
    expected={(seed,selector) for seed in frozen['seeds'] for selector in frozen['selectors']}
    require({(v['conditions']['seed'],v['conditions']['selector']) for v in refs.values()}==expected,'frozen nine coordinates differ')
    gu_refs={g['cell_id']:g for g in source['gu_cells']}
    require(len(gu_refs)==18 and {(g['conditions']['seed'],g['conditions']['selector'],g['conditions']['method']) for g in gu_refs.values()}=={
        (seed,selector,method) for seed,selector in expected for method in ('GIF','MEGU')},'fixed GU matrix incomplete')
    for gu_id,gu_ref in gu_refs.items():
        gu_cell=old.cells[gu_id];gu_docs=old.cell_documents(gu_cell)
        require(gu_cell['output']==gu_ref['output'] and gu_cell['conditions']==gu_ref['conditions']
            and gu_cell['selection_id']==gu_ref['selection_id']
            and gu_cell['files']['selection.json']['sha256']==gu_ref['selection_sha256']
            and gu_docs['selection.json']['selected_nodes']==gu_ref['selected_nodes'],'frozen GU source differs')
    stats,endpoints,traces,admitted,pairs,class_rows,correctness_rows=[],[],[],[],[],[],[]
    for batch in selected_batches:
        new=helper.TrustedRun(batch['job_id'],batch['experiment_id'],batch['run_id'],index)
        require(new.run['commit']==args.expected_commit and new.run['stage']=='retrain_diagnostics','execution SHA/stage differs')
        require(new.run['config_path']==new.execution['config_path']==batch['config_path']
            and new.execution['config_sha256']==batch['config_sha256'] and new.execution['recipe']==batch['recipe'],'frozen execution differs')
        require(set(new.execution['artifact_paths'])==set(batch['expected_artifact_paths']),'frozen file scope differs')
        require(set(new.cells)==set(batch['cell_ids']),'incomplete or expanded batch')
        asset_audit=audits[batch['run_id']]
        require(asset_audit['run_sha256']==sha(new.local_root/'run.json'),'endpoint audit run differs')
        audited={r['cell_id']:r for r in asset_audit['rows']}
        require(len(audited)==len(asset_audit['rows']) and set(audited)==set(new.cells),'endpoint audit cells differ')
        for cell_id,cell in new.cells.items():
            ref=refs[cell_id];old_cell=old.cells[cell_id];old_docs=old.cell_documents(old_cell)
            require(old_cell['output']==ref['output'] and old_cell['conditions']==ref['conditions']
                and old_cell['selection_id']==ref['selection_id']
                and old_cell['files']['selection.json']['sha256']==ref['selection_sha256']
                and old_docs['selection.json']['selected_nodes']==ref['selected_nodes'],'frozen old reference differs')
            documents=new.cell_documents(cell)
            result=documents['observers/'+OBS+'/result.json'];asset_row=audited[cell_id]
            require(asset_row['source_output']==ref['output'] and asset_row['conditions']==ref['conditions']
                and asset_row['observer_result_sha256']==cell['files']['observers/'+OBS+'/result.json']['sha256']
                and asset_row['recorded_comparison']==result['diagnostics']['old_final_comparison'],'asset audit source/result differs')
            for role in ('best','final'):
                require(asset_row['endpoints'][role]['state_hash']==result['diagnostics'][role]['state_hash']
                    and asset_row['endpoints'][role]['weights']==result['diagnostics'][role]['weights']
                    and asset_row['endpoints'][role]['predictions']==result['diagnostics'][role]['predictions'],'asset audit endpoint differs')
            comparisons=asset_row['gu_comparisons']
            require(len(comparisons)==6 and {(p['method'],p['checkpoint_role']) for p in comparisons}=={
                (m,role) for m in ('GIF','MEGU') for role in ('old_final','final','best')},'fixed paired role/method scope differs')
            for comparison in comparisons:
                gu_ref=gu_refs[comparison['gu_cell_id']]
                require(gu_ref['retrain_cell_id']==cell_id and gu_ref['output']==comparison['gu_output']
                    and gu_ref['conditions']['method']==comparison['method'],'paired GU identity differs')
                metrics=validate_pair_classes(comparison)
                role=comparison['checkpoint_role']
                ret_test=result['diagnostics']['old_final_comparison']['old_test'] if role=='old_final' else result['diagnostics'][role]['test']
                for key in ('accuracy','cross_entropy'):
                    close(metrics['retrain_'+key],ret_test[key],'paired Ret '+key,atol=2e-6 if key=='cross_entropy' else 1e-12,rtol=2e-6 if key=='cross_entropy' else 0)
                    close(metrics['gu_'+key],gu_ref['old_test'][key],'paired GU '+key,atol=2e-6 if key=='cross_entropy' else 1e-12,rtol=2e-6 if key=='cross_entropy' else 0)
                base=dict(seed=ref['conditions']['seed'],selector=ref['conditions']['selector'],method=comparison['method'],
                    checkpoint_role=role,retrain_cell_id=cell_id,gu_cell_id=comparison['gu_cell_id'])
                pairs.append(dict(base,**{k:v for k,v in metrics.items() if k not in ('correctness_order','cells')}))
                for group in [{'class_id':'all','metrics':metrics}]+comparison['by_class']:
                    for bits,counts in group['metrics']['cells'].items(): correctness_rows.append(dict(base,class_id=group['class_id'],correctness_bits=bits,**counts))
                    if group['class_id']!='all': class_rows.append(dict(base,class_id=group['class_id'],**{k:v for k,v in group['metrics'].items() if k not in ('correctness_order','cells')}))
            row,ep,trace=validate_cell(cell,documents,ref,frozen,source,batch,args.expected_commit)
            stats.append(row);endpoints.extend(ep);traces.extend(trace)
        require(new.checked_files==set(new.verified),'unvalidated returned file')
        admitted.append({'job_id':new.job_id,'run_sha256':sha(new.local_root/'run.json'),
            'delivery_sha256':sha(new.delivery_path),'handoff_sha256':sha(new.handoff_path),'checked_files':len(new.checked_files)})
    wanted=expected if args.scope=='complete' else {(42,s) for s in frozen['selectors']}
    require(len(stats)==len(wanted) and {(v['seed'],v['selector']) for v in stats}==wanted,'scope lacks fixed coordinates')
    mismatch=[r['cell_id'] for r in stats if not r['old_final_exact']]
    sensitive=[r['cell_id'] for r in stats if r['optimization_sensitive']]
    contrasts=[]
    by={(r['seed'],r['selector'],r['checkpoint_role']):r for r in endpoints}
    for seed in sorted({r['seed'] for r in stats}):
        for baseline in ('random','degree'):
            for role in ('old_final','final','best'):
                point,control=by[seed,'r_point',role],by[seed,baseline,role]
                contrasts.append(dict(seed=seed,baseline=baseline,checkpoint_role=role,
                    rpoint_minus_baseline_accuracy_pp=100*(point['accuracy']-control['accuracy']),
                    rpoint_minus_baseline_ce=point['cross_entropy']-control['cross_entropy']))
    summaries=[]
    for selector in frozen['selectors']:
        rows=[r for r in stats if r['selector']==selector]
        summaries.append(dict(selector=selector,n=len(rows),triggered=sum(r['optimization_sensitive'] for r in rows),
            mean_validation_gap_pp=statistics.mean(r['validation_accuracy_gap_pp'] for r in rows),
            mean_best_minus_final_test_pp=statistics.mean(r['best_minus_final_test_accuracy_pp'] for r in rows),
            sd_best_minus_final_test_pp=statistics.stdev(r['best_minus_final_test_accuracy_pp'] for r in rows) if len(rows)>1 else None))
    pair_by={(r['seed'],r['selector'],r['method'],r['checkpoint_role']):r for r in pairs}
    require(len(pair_by)==len(stats)*6==len(pairs),'paired endpoint matrix differs')
    sensitivity=[];gu_contrasts=[]
    for row in pairs:
        old_pair=pair_by[row['seed'],row['selector'],row['method'],'old_final']
        sensitivity.append(dict(row,disagreement_change_vs_oldfinal_pp=100*(row['disagreement']-old_pair['disagreement'])))
    for seed in sorted({r['seed'] for r in stats}):
        for method in ('GIF','MEGU'):
            for baseline in ('random','degree'):
                for role in ('old_final','final','best'):
                    point,control=pair_by[seed,'r_point',method,role],pair_by[seed,baseline,method,role]
                    old_diff=pair_by[seed,'r_point',method,'old_final']['disagreement']-pair_by[seed,baseline,method,'old_final']['disagreement']
                    difference=point['disagreement']-control['disagreement']
                    gu_contrasts.append(dict(seed=seed,method=method,baseline=baseline,checkpoint_role=role,
                        rpoint_minus_baseline_disagreement_pp=100*difference,
                        change_in_request_contrast_vs_oldfinal_pp=100*(difference-old_diff)))
    out=HERE/'analysis'/args.scope;out.mkdir(parents=True,exist_ok=False)
    for name,rows in [('trajectories',stats),('endpoints',endpoints),('full_trace',traces),('paired_request_contrasts',contrasts),('condition_summary',summaries),
                      ('gu_reference_pairs',sensitivity),('gu_reference_classes',class_rows),('gu_reference_correctness',correctness_rows),('gu_request_contrasts',gu_contrasts)]:
        helper.csv_write(out/(name+'.csv'),rows)
    decision={'status':'validated_returned_diagnostics','scope':args.scope,'cell_count':len(stats),'trace_rows':len(traces),
        'scientific_gate':'stop_unexplained_final_difference' if mismatch else 'pilot_pass_complete_remaining_six' if args.scope=='pilot' else 'complete_requires_B_reassessment' if sensitive else 'complete_no_protocol_trigger',
        'mismatched_final_cells':mismatch,'optimization_sensitive_cells':sensitive,'writing_gate':'not_met',
        'formal_scope_complete':args.scope=='complete','execution_sha':args.expected_commit,'admitted_runs':admitted,
        'gu_pairs':len(stats)*2,'gu_pair_endpoint_rows':len(pairs),'class_analysis':'post_hoc_descriptive_all_six_classes',
        'frozen_manifest_sha256':sha(args.frozen_manifest),'analysis_script_sha256':sha(Path(__file__)),
        'remote_endpoint_assets':'independently rehashed and state/logit/metric comparisons checked by explicit read-only audit',
        'endpoint_audit_sha256':{Path(path).name:checksum for path,checksum in args.endpoint_audit},
        'ret_best_does_not_replace_old_final':True}
    (out/'DECISION.json').write_text(json.dumps(decision,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    helper.document(out,'Ret 验证轨迹：'+args.scope,[
        f'可信回传诊断{len(stats)}条、完整逐轮记录{len(traces)}行。科学状态：{decision["scientific_gate"]}。',
        'best、final、old-final同时报告；best只由retained图原validation mask的accuracy决定，并列选最早。测试端点不参与选择。',
        f'新旧final存在差异的条件{len(mismatch)}条；触发预定优化敏感阈值{len(sensitive)}条。任何新旧final差异均暂停扩展和科学解释，需要有证据的原因审查，不自动归因CUDA随机性。',
        'pilot无触发不能排除其他seed；B若仍承担核心，必须完整九条。未触发不证明收敛或训练充分。',
        '三个seed是固定split上的请求与训练程序重复，按seed配对，不把epoch或测试节点当独立样本；这里只给描述性均值/SD，不作功效或收敛保证。',
        '完整数值见full_trace.csv、trajectories.csv、endpoints.csv、paired_request_contrasts.csv和condition_summary.csv。此范围只有33% Ret，不能单独证明B的5%→33%分歧关系，也不能挑测试更好的checkpoint替代原参照。',
        f'直接配对固定{len(stats)*2}个GIF/MEGU旧Output与三类Ret端点，共{len(pairs)}条记录；分歧和accuracy均由四格正确性及格内分歧整数独立重建。GU_reference/REPORT.html展示每个seed的R-point−Random/Degree的D差与相对旧参照的变化，不从Ret utility推断。',
        '全部六类别的配对整数还原全局N=666；该解释是在查看B后新增的post-hoc descriptive分析，不能当预注册机制或因果证据。',
        '端点通过另行只读资产审计，绑定本run哈希、旧Output、权重及预测文件哈希；不重新训练或选择模型。writing_gate保持not_met。'],
        ['seed','selector','best_epoch','validation_accuracy_gap_pp','val_ce_2001_2500','val_ce_2501_3000','optimization_sensitive','old_final_exact','best_minus_final_test_accuracy_pp'],stats)
    paired_out=out/'GU_reference';paired_out.mkdir()
    helper.document(paired_out,'GU–Ret参考敏感性：'+args.scope,[
        '全部预定GIF/MEGU条件与old-final/new-final/best比较；表中正值表示R-point分歧高于相应基线，单位为百分点。',
        'change_in_request_contrast_vs_oldfinal_pp是相同seed/method的请求差相对旧参考的改变量。每一对D、CE及双方accuracy在上级gu_reference_pairs.csv中，全部类别和四格整数分别在gu_reference_classes.csv及gu_reference_correctness.csv。',
        '科学状态：'+decision['scientific_gate']+'。如新旧final不可解释，所有数值仅用于定位差异，不得据此开始机制推断。',
        '只读保存预测，没有训练或forward；MEGU为保存的updated+C&S。类别解释为post-hoc descriptive。33%参考敏感性不等于5%→33%在新参考下的完整预算交互。'],
        ['seed','method','baseline','checkpoint_role','rpoint_minus_baseline_disagreement_pp','change_in_request_contrast_vs_oldfinal_pp'],gu_contrasts)
    print(json.dumps(decision,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try: main()
    except (KeyError,ValueError,OSError,AssertionError) as exc:
        raise SystemExit('RET ANALYSIS NOT ACCEPTED: '+str(exc))
