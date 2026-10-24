"""Fixed-weight graph and matched MEGU postprocessing diagnostics.

Only exact saved Output/checkpoint consumers are permitted here. This module
never trains, recomputes a Selection, or repairs missing input artifacts.
"""
from __future__ import annotations

import itertools
from types import SimpleNamespace
import numpy as np
import torch

from experiments.effective_config import ConfigurationError
from experiments.response_diagnostics import prediction_triangle, prediction_by_label, response_diagnostics
from experiments.unlearning_outputs import restore_model
from experiments.modular_model import create_model
from experiments.modular_megu import megu_logits
from experiments.checkpoint_references import training_identity, read_checkpoint_reference
from utils.target_checkpoint import load_cached_weights, state_hash, data_identity


CASE = 'post_unlearning_response_graph_sensitivity'
TRIANGLE_KEYS = tuple(prediction_triangle(np.zeros((0,2)), np.zeros((0,2)),
                                        np.zeros((0,2)), np.array([],dtype=np.int64)))
ENDPOINTS = ('no_update_raw','no_update_cs','updated_raw','updated_cs')
GRAPHS = ('original','retained')
METRICS = tuple(g+'_graph_'+kind+'_'+key for g in GRAPHS
                for kind in ('raw','published','matched_cs') for key in TRIANGLE_KEYS) + tuple(
    g+'_graph_'+a+'_vs_'+b+'_disagreement_count' for g in GRAPHS
    for a,b in itertools.combinations(ENDPOINTS,2)) + tuple(
    g+'_graph_'+e+'_'+metric for g in GRAPHS for e in ENDPOINTS
    for metric in ('accuracy','cross_entropy')) + tuple(
    e+'_graph_disagreement_count' for e in (*ENDPOINTS,'retrain_raw'))


def reproduction_policy():
    # Literal policy is part of the computation fingerprint. Never tune on failures.
    return dict(raw_atol=1e-5, raw_rtol=1e-4, probability_atol=1e-5,
                cross_entropy_atol=1e-4, require_all_node_argmax_equal=True)


def _array(value):
    return value.detach().cpu().numpy().copy()


def _probabilities(logits):
    values=np.asarray(logits,dtype=np.float64)
    shifted=values-values.max(axis=1,keepdims=True)
    probabilities=np.exp(shifted)
    return probabilities/probabilities.sum(axis=1,keepdims=True)


def reproduce(saved, actual, name, *, probabilities=False):
    policy=reproduction_policy()
    saved,actual=np.asarray(saved),np.asarray(actual)
    if (saved.ndim!=2 or saved.shape!=actual.shape or not np.isfinite(saved).all()
            or not np.isfinite(actual).all()):
        raise ConfigurationError(name+': reproduction failed: invalid logits')
    changed=int(np.count_nonzero(saved.argmax(1)!=actual.argmax(1)))
    left,right=(_probabilities(saved),_probabilities(actual)) if probabilities else (saved,actual)
    error=float(np.max(np.abs(left-right)))
    close=(error<=policy['probability_atol'] if probabilities else
           bool(np.allclose(left,right,atol=policy['raw_atol'],rtol=policy['raw_rtol'])))
    if changed or not close:
        raise ConfigurationError(f'{name}: reproduction failed: changed_labels={changed}, max_abs_error={error}, probabilities={probabilities}')
    return dict(changed_labels=changed,max_abs_error=error,probabilities=probabilities)


def restore_original(output, data, checkpoint_root, device, original_checkpoint=None):
    """Resolve one deterministic checkpoint and verify actual bytes and state."""
    binding=output.identity['pairing']
    expected=output.identity['target'].get('checkpoint_state_hash')
    external = all(binding['training'].get(k) is None for k in ('epochs','optimizer','lr','weight_decay','scheduler'))
    if external:
        from pathlib import Path
        from experiments.modular_model import numerical_environment
        from experiments.implementation_identity import implementation_fingerprint, model_functions
        from utils.target_checkpoint import load_weights
        receipt = original_checkpoint
        if (not expected or not isinstance(receipt,dict)
                or set(receipt) != {'path','file_sha256','state_hash','hit','source','effective_identity'}
                or receipt['source'] != 'external_state_dict' or type(receipt['hit']) is not bool
                or receipt['state_hash'] != expected or not Path(receipt['path']).is_absolute()):
            raise ConfigurationError('external Original requires its exact declared checkpoint receipt')
        model=create_model(binding['model'],output.identity['dataset_input']['instance']['dataset']['name'],data,device)
        effective = dict(data_identity=data_identity(data),model=binding['model'],
            execution_seed=binding['training']['seed'],numerics=numerical_environment(data),
            implementation=implementation_fingerprint(*model_functions(model)))
        if receipt['effective_identity'] != effective:
            raise ConfigurationError('external Original Dataset/model/seed identity mismatch')
        loaded=load_weights(receipt['path'],model)
        if (loaded['file_sha256'] != receipt['file_sha256'] or loaded['state_hash'] != expected
                or state_hash(model.state_dict()) != expected):
            raise ConfigurationError('external Original bytes/state differ from exact receipt')
        return model.eval(),dict(source='external_state_dict',**{k:receipt[k] for k in
            ('path','file_sha256','state_hash','effective_identity')})
    if original_checkpoint is not None:
        raise ConfigurationError('external Original receipt supplied for internal training identity')
    if (not expected or any(binding['training'].get(k) is None
            for k in ('epochs','optimizer','lr','weight_decay','scheduler'))):
        raise ConfigurationError('Original requires an exact internal training checkpoint; external/missing references are unsupported')
    instance=dict(model=binding['model'],training=binding['training'])
    metadata=training_identity(instance,data)
    reference=read_checkpoint_reference(checkpoint_root,metadata)
    if reference is None:
        raise ConfigurationError('Original checkpoint MISS; graph diagnostics cannot train')
    if reference['state_hash']!=expected:
        raise ConfigurationError('Original checkpoint metadata state hash differs from Output target')
    model=create_model(binding['model'],output.identity['dataset_input']['instance']['dataset']['name'],data,device)
    loaded=load_cached_weights(reference['path'],metadata,model)
    if (loaded['file_sha256']!=reference['file_sha256'] or loaded['state_hash']!=expected
            or state_hash(model.state_dict())!=expected):
        raise ConfigurationError('Original checkpoint bytes/state differ from exact reference')
    from pathlib import Path
    path=Path(reference['path']).resolve().relative_to(Path(checkpoint_root).resolve()).as_posix()
    return model.eval(),dict(checkpoint_root='execution_context.checkpoint_root',path=path,
        file_sha256=loaded['file_sha256'],state_hash=expected,
        generation_metadata=loaded['generation_metadata'],consumption_metadata=metadata)


def _graph(arrays, edges, train_mask, device):
    return SimpleNamespace(x=torch.tensor(arrays['x'],device=device),y=torch.tensor(arrays['y'],device=device),
        edge_index=torch.tensor(edges,device=device),train_mask=torch.tensor(train_mask,device=device),
        val_mask=torch.tensor(arrays['val_mask'],device=device),test_mask=torch.tensor(arrays['test_mask'],device=device),
        num_nodes=len(arrays['y']))


def _state(model):
    return state_hash(model.state_dict())


def _saved_deletion_masks(output):
    masks={}
    for name in ('deletion1','deletion2'):
        value=np.asarray(output.auxiliary.get(name+'_mask'))
        if value.dtype!=np.bool_ or value.shape!=output.arrays['y'].shape:
            raise ConfigurationError('GNNDelete requires saved boolean node mask: '+name)
        masks[name]=value.copy()
    return masks


def _raw_logits(model,graph,deletion_masks=None):
    def check_masks():
        for name,expected in (deletion_masks or {}).items():
            actual=getattr(model,name).mask
            if (actual.device!=graph.x.device or actual.dtype!=torch.bool
                    or not np.array_equal(_array(actual),expected)):
                raise ConfigurationError('GNNDelete changed saved deletion mask/device: '+name)
    check_masks()
    result=_array(model.eval()(graph.x,graph.edge_index))
    check_masks()
    return result


def graph_sensitivity(output,retrain,*,checkpoint_root,device,original_checkpoint=None):
    """Original reproduction is a hard gate before changing evaluation edges."""
    if checkpoint_root is None or device is None:
        raise ConfigurationError('graph diagnostics requires explicit checkpoint root and execution device')
    method=output.identity['target']['method']
    binding=output.identity['pairing']
    if (method not in ('GIF','MEGU','GNNDelete') or binding['model']['architecture']!='OpenGU.GCNNet'
            or binding['deletion']['evaluation_graph']!='original'):
        raise ConfigurationError('graph diagnostics supports original-evaluated GCN GIF/MEGU/GNNDelete with matched Retrain only')
    original_metrics,first_protocol=response_diagnostics(output,retrain)
    a=output.arrays
    mask=a['test_mask'].copy()
    mask[a['selected_nodes']]=False
    graphs={g:_graph(a,a['edge_index'] if g=='original' else a['training_edge_index'],
                    a['train_mask'] if g=='original' else a['retain_mask'],device) for g in GRAPHS}
    graph_hashes={g:data_identity(data) for g,data in graphs.items()}
    if (graph_hashes['original']!=binding['data_identity']
            or graph_hashes['retained']!=binding['training_graph_identity']):
        raise ConfigurationError('diagnostic graph identities differ from bound Output')
    if method=='MEGU' and 'megu_pseudo_labels' not in output.auxiliary:
        raise ConfigurationError('MEGU requires saved pseudo-labels; cannot regenerate')
    deletion_masks=_saved_deletion_masks(output) if method=='GNNDelete' else None
    original,checkpoint=restore_original(output,graphs['original'],checkpoint_root,device,original_checkpoint)
    models=dict(no_update_raw=original,updated_raw=restore_model(output).to(device),retrain_raw=restore_model(retrain).to(device))
    if deletion_masks is not None:
        # DeletionLayer.mask is an ordinary attribute, so Module.to does not move it.
        for name,saved in deletion_masks.items():
            getattr(models['updated_raw'],name).mask=torch.tensor(saved,device=device)
    states={k:_state(model) for k,model in models.items()}
    for endpoint,payload in (('updated_raw',output),('retrain_raw',retrain)):
        expected_state=state_hash({k:torch.tensor(v) for k,v in payload.state.items()})
        if states[endpoint]!=expected_state:
            raise ConfigurationError('restored Output weights differ from saved state: '+endpoint)
    pseudo=None
    if method=='MEGU':
        if 'megu_pseudo_labels' not in output.auxiliary:
            raise ConfigurationError('MEGU requires saved pseudo-labels; cannot regenerate')
        pseudo=np.asarray(output.auxiliary['megu_pseudo_labels'])
        if (pseudo.shape!=a['y'].shape or not np.issubdtype(pseudo.dtype,np.integer)
                or not np.array_equal(pseudo,a['logits_before'].argmax(1))):
            raise ConfigurationError('MEGU saved pseudo-labels differ from persisted Original original-graph argmax')
        for model in (original,models['updated_raw']):
            model.megu_pseudo_labels=torch.tensor(pseudo,device=device)
    values={key:None for key in METRICS}
    outputs={}
    checks={}
    by_label={}
    for graph_name,graph in graphs.items():
        with torch.no_grad():
            current={k:_raw_logits(model,graph,deletion_masks if k=='updated_raw' else None) for k,model in models.items()}
            if method=='MEGU':
                for endpoint,model in (('no_update_cs',original),('updated_cs',models['updated_raw'])):
                    current[endpoint]=_array(megu_logits(model,graph,graphs['retained'].train_mask,output.identity['target']['parameters']))
        if any(not np.isfinite(logits).all() for logits in current.values()):
            raise ConfigurationError(graph_name+': nonfinite diagnostic endpoint')
        published=current['updated_cs'] if method=='MEGU' else current['updated_raw']
        if graph_name=='original':
            checks['Original']=reproduce(a['logits_before'],current['no_update_raw'],'Original')
            checks['Retrain']=reproduce(retrain.arrays['logits'],current['retrain_raw'],'Retrain')
            checks[method]=reproduce(a['logits'],published,method,probabilities=method=='MEGU')
            if pseudo is not None and not np.array_equal(pseudo,current['no_update_raw'].argmax(1)):
                raise ConfigurationError('MEGU saved pseudo-labels differ from restored Original')
            reproduced=prediction_triangle(current['no_update_raw'][mask],published[mask],current['retrain_raw'][mask],a['y'][mask])
            for key,result in reproduced.items():
                expected=original_metrics[key]
                if key.endswith('cross_entropy'):
                    equal=(result==expected if result is None or expected is None else abs(result-expected)<=reproduction_policy()['cross_entropy_atol'])
                else:
                    equal=result==expected
                if not equal:
                    raise ConfigurationError(f'original graph metric reproduction failed: {key}: saved={expected}, actual={result}')
        triangles=dict(raw=(current['no_update_raw'],current['updated_raw']),published=(current['no_update_raw'],published))
        if method=='MEGU':
            triangles['matched_cs']=(current['no_update_cs'],current['updated_cs'])
        for name,(o,g) in triangles.items():
            measured=prediction_triangle(o[mask],g[mask],current['retrain_raw'][mask],a['y'][mask])
            values.update({graph_name+'_graph_'+name+'_'+k:v for k,v in measured.items()})
            by_label.setdefault(graph_name,{})[name]=prediction_by_label(o[mask],g[mask],current['retrain_raw'][mask],a['y'][mask])
        from experiments.response_diagnostics import cross_entropy
        for endpoint in ENDPOINTS:
            if endpoint not in current:
                continue
            labels=current[endpoint][mask].argmax(1)
            values[graph_name+'_graph_'+endpoint+'_accuracy']=float((labels==a['y'][mask]).mean()) if mask.any() else None
            values[graph_name+'_graph_'+endpoint+'_cross_entropy']=cross_entropy(current[endpoint][mask],a['y'][mask])
        for left,right in itertools.combinations(ENDPOINTS,2):
            if left in current and right in current:
                values[graph_name+'_graph_'+left+'_vs_'+right+'_disagreement_count']=int(np.count_nonzero(current[left][mask].argmax(1)!=current[right][mask].argmax(1)))
        outputs[graph_name]=current
    # A second original forward exposes graph-state caches or input mutation.
    with torch.no_grad():
        for endpoint,model in models.items():
            checks['roundtrip_'+endpoint]=reproduce(outputs['original'][endpoint],_raw_logits(model,graphs['original'],deletion_masks if endpoint=='updated_raw' else None),endpoint+' graph roundtrip')
        if method=='MEGU':
            for endpoint,model in (('no_update_cs',original),('updated_cs',models['updated_raw'])):
                checks['roundtrip_'+endpoint]=reproduce(outputs['original'][endpoint],_array(megu_logits(model,graphs['original'],graphs['retained'].train_mask,output.identity['target']['parameters'])),endpoint+' graph roundtrip',probabilities=True)
                if not np.array_equal(_array(model.megu_pseudo_labels),pseudo):
                    raise ConfigurationError('graph diagnostics mutated saved pseudo-labels')
    if any(_state(model)!=states[endpoint] for endpoint,model in models.items()):
        raise ConfigurationError('graph diagnostics mutated model state')
    if any(data_identity(graphs[g])!=graph_hashes[g] for g in GRAPHS):
        raise ConfigurationError('graph diagnostics mutated bound inputs')
    for endpoint in (*ENDPOINTS,'retrain_raw'):
        if endpoint in outputs['original']:
            values[endpoint+'_graph_disagreement_count']=int(np.count_nonzero(outputs['original'][endpoint][mask].argmax(1)!=outputs['retained'][endpoint][mask].argmax(1)))
    from utils.target_checkpoint import tensor_hash
    protocol=dict(version='fixed-weight-two-graphs-matched-cs-v2',first_layer=first_protocol,
        class_order='zero_based_label_id',by_label=by_label,
        checkpoint=checkpoint,state_hashes=states,graphs=graph_hashes,
        reproduction_policy=reproduction_policy(),reproduction_observations=checks,
        evaluation_mask='unchanged_test_mask_excluding_selected',
        observed_execution=dict(device_type=torch.device(device).type,cuda_version=torch.version.cuda),
        deletion_masks=(dict(status='applicable',source='saved_output_auxiliary',
            graph_policy='fixed_across_original_retained_and_roundtrip',model='GCNDelete',
            masks={name:dict(sha256=tensor_hash(torch.tensor(value)),count=int(value.sum()))
                   for name,value in deletion_masks.items()}) if deletion_masks is not None
                   else dict(status='not_applicable')),
        cs=(dict(status='applicable',pseudo_label_source='saved_original_original_graph_argmax',
            pseudo_labels_sha256=tensor_hash(torch.tensor(pseudo)),anchors='saved_pseudo_labels_on_retained_train_mask',
            parameters=output.identity['target']['parameters'],correction_layers=80,smoothing_layers=80,
            autoscale=False,scale=1.,prediction='log_clamped_probabilities') if method=='MEGU' else dict(status='not_applicable')))
    return values,protocol
