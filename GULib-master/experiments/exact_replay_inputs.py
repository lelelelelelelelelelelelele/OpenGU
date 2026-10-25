"""Exact existing-input seam for observed GIF replay; no selectors or training."""
from pathlib import Path
import hashlib
import json
import re

from experiments.effective_config import ConfigurationError, fields

SCHEMA='opengu.exact-gu-inputs-v1'

def digest(value):
    if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{64}',value):
        raise ConfigurationError('exact input requires a SHA256 digest')

def read_document(reference,directory):
    fields(reference,{'path','sha256'},{'path','sha256'},'exact_inputs')
    digest(reference['sha256'])
    relative=reference['path']
    if (not isinstance(relative,str) or not relative or '\\' in relative or
            Path(relative).is_absolute() or ':' in relative or '..' in Path(relative).parts):
        raise ConfigurationError('exact_inputs.path must be a contained relative JSON path')
    path=(Path(directory)/relative).resolve()
    if not path.is_file() or Path(directory).resolve() not in path.parents:
        raise ConfigurationError('exact input JSON is missing or outside its config directory')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=reference['sha256']:
        raise ConfigurationError('exact input JSON SHA mismatch')
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ConfigurationError('duplicate exact-input field: '+key)
            result[key]=value
        return result
    value=json.loads(raw.decode('utf-8'),object_pairs_hook=unique,
        parse_constant=lambda v:(_ for _ in ()).throw(ConfigurationError('nonfinite exact input')))
    fields(value,{'schema','requests'},{'schema','requests'},'exact input document')
    if value['schema']!=SCHEMA or not isinstance(value['requests'],list) or not value['requests']:
        raise ConfigurationError('nonempty exact GIF request document required')
    seen=set()
    for row in value['requests']:
        fields(row,{'cell_id','selection','selected_nodes','original','retrain','parameters','deletion'},
            {'cell_id','selection','selected_nodes','original','retrain','parameters','deletion'},'exact request')
        if not isinstance(row['cell_id'],str) or not re.fullmatch('[0-9a-f]{20}',row['cell_id']) or row['cell_id'] in seen:
            raise ConfigurationError('exact input coordinates must be unique native cell IDs')
        seen.add(row['cell_id'])
        for name in ('selection','retrain'):
            fields(row[name],{'artifact_id','recipe_hash','content_hash'},
                {'artifact_id','recipe_hash','content_hash'},'exact '+name)
            if not isinstance(row[name]['artifact_id'],str) or not row[name]['artifact_id']:
                raise ConfigurationError('existing Artifact ID required')
            for key in ('recipe_hash','content_hash'):digest(row[name][key])
        nodes=row['selected_nodes']
        if not isinstance(nodes,list) or not nodes or any(type(n) is not int or n<0 for n in nodes) or len(nodes)!=len(set(nodes)):
            raise ConfigurationError('exact ordered selected_nodes must be nonempty unique integers')
        original=row['original']
        fields(original,{'path','file_sha256','state_hash','data_identity','model','execution_seed'},
            {'path','file_sha256','state_hash','data_identity','model','execution_seed'},'exact Original')
        for key in ('file_sha256','state_hash'):digest(original[key])
        if not isinstance(original['path'],str) or not original['path'] or type(original['execution_seed']) is not int:
            raise ConfigurationError('exact Original path and integer seed required')
        if any(not isinstance(row[key],dict) for key in ('parameters','deletion')) or not isinstance(original['model'],dict) or not isinstance(original['data_identity'],dict):
            raise ConfigurationError('exact method/data identities must be mappings')
    return value

def validate_config(config):
    from experiments.modular_artifacts import planned_cells
    from experiments.modular_config import experiment_batches
    if (config['stage']!='unlearning' or {i['method'] for i in config['unlearnings']}!={'GIF'} or
            config['execution']['gu_cache'].get('GIF')!='disabled' or config.get('return_scores')):
        raise ConfigurationError('exact_inputs requires uncached GIF-only unlearning without score export')
    items=[i for batch in experiment_batches(config) for i in batch['unlearnings']]
    iterations={i['parameters']['iteration'] for i in items}
    if len(iterations)!=1 or not iterations<={100,400} or any(not i.get('checkpoint') for i in items):
        raise ConfigurationError('exact replay needs explicit PT and one T100 or T400 endpoint per config')
    required={'linear_solver_trace','same_graph_change'} | ({'hessian_calibration'} if iterations=={100} else set())
    names={r['instance']['name'] for r in config['observers']}
    if names!=required:raise ConfigurationError('exact replay endpoint Observer coverage differs')
    document=read_document(config['exact_inputs'],config['source_directory'])
    expected={r['cell_id'] for r in planned_cells(config)}
    if {r['cell_id'] for r in document['requests']}!=expected:
        raise ConfigurationError('exact input JSON must bind every native cell one-to-one')
    return document

class ExactInputs:
    def __init__(self,config):
        self.config=config
        self.document=validate_config(config)
        self.rows={r['cell_id']:r for r in self.document['requests']}

    def selection(self,cells,selector,*,store_root,data,inputs):
        from experiments.modular_run import verified_selection,selection_prefix
        rows=[self.rows[c['cell_id']] for c in cells]
        first=rows[0]
        if any((r['selection'],r['selected_nodes'])!=(first['selection'],first['selected_nodes']) for r in rows):
            raise ConfigurationError('one declared request must use one exact Selection prefix')
        loaded=verified_selection(first['selection'],store_root=store_root,data=data,inputs=inputs,
            expected_selector=selector['method'])
        prefix=selection_prefix(loaded,selector['budget']['k'])
        if list(prefix.selected_nodes)!=first['selected_nodes']:
            raise ConfigurationError('exact ordered Selection prefix differs')
        # No Score payload was requested or accessed. Selection was read by ID.
        resolved=dict(score=dict(hit=None,producer_called=False,access_seconds=0.),
            selection=dict(strategy=loaded.selector,artifact=dict(first['selection']),artifact_k=loaded.k,
                cache=dict(hit=True,producer_called=False),views={str(prefix.requested_k):dict(selected_nodes=list(prefix.selected_nodes))}),
            selection_seconds=None)
        return resolved,loaded

    def prepare(self,cell,instance,*,data,inputs,dataset_input,store_root,dataset_root,device,checkpoint_root):
        from experiments.modular_model import prepare_model
        from experiments.unlearning_outputs import load_output
        from experiments.node_deletion import pairing_identity,retrain_pairing_matches
        from utils.target_checkpoint import data_identity,sha256_file
        row=self.rows[cell['cell_id']];original=row['original'];directory=Path(self.config['source_directory'])
        checkpoint=(directory/original['path']).resolve()
        if (instance['parameters']!=row['parameters'] or instance['deletion']!=row['deletion'] or
                instance['model']!=original['model'] or instance['training']['seed']!=original['execution_seed'] or
                data_identity(data)!=original['data_identity'] or Path(instance['checkpoint']).resolve()!=checkpoint):
            raise ConfigurationError('exact method/parameters/Original/data/deletion binding differs')
        if not checkpoint.is_file() or sha256_file(checkpoint)!=original['file_sha256']:
            raise ConfigurationError('exact Original file missing or SHA mismatch')
        baseline=load_output(row['retrain'],store_root,data=data,dataset_root=dataset_root)
        expected=dict(target=dict(checkpoint_state_hash=original['state_hash']),selection=row['selection'],
            dataset_input=dataset_input,graph_fingerprint=inputs.graph_fingerprint,
            pairing=pairing_identity(instance,data,row['selected_nodes']))
        if not retrain_pairing_matches(expected,baseline.identity):
            raise ConfigurationError('exact existing Ret does not match request/data/model/deletion')
        model,_,observation=prepare_model(instance,data=data,dataset_name=inputs.dataset_name,checkpoint_root=checkpoint_root,
            device=device,reference_directory=directory,fail_if_training=True)
        if observation['file_sha256']!=original['file_sha256'] or observation['state_hash']!=original['state_hash']:
            raise ConfigurationError('loaded Original file/state differs from frozen historical input')
        return model,observation

    def provenance(self,cell):
        row=self.rows[cell['cell_id']]
        return dict(**self.config['exact_inputs'],cell_id=cell['cell_id'],selection=row['selection'],
            retrain=row['retrain'],original_state_hash=row['original']['state_hash'])
