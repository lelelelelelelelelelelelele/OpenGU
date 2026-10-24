"""Strict lightweight trace validation and read-only endpoint loading; no forward."""
import json
import math

from cache_v2 import canonical_sha256
from experiments.ret_reference_policy import ARMS, DETERMINISTIC, OBSERVED
from experiments.observers.ret_reference import AUDIT_EPOCHS


def validate_trace(document, trace, reference, cell):
    if (document.get('identity') != reference['identity'] or document.get('status') != 'completed'
            or document.get('name') != 'ret_reference_trace'
            or document.get('semantic_version') != reference['semantic_version']):
        raise ValueError('Ret reference document identity/status mismatch')
    diagnostics = document['diagnostics']
    if any(diagnostics.get(k) != v for k,v in dict(validation_graph='retained(S)',
        validation_mask='original_val_mask',selection_rule='maximum_validation_accuracy_earliest_tie',
        primary_endpoint='final3000',auxiliary_endpoint='validation_best',
        primary_probe='original',secondary_probe='retained(S)',repetitions_are_independent_samples=False).items()):
        raise ValueError('Ret reference endpoint/selection semantics mismatch')
    mode = cell['conditions'].get('reference_mode','reference')
    if mode not in ('reference','probe'):
        raise ValueError('Ret reference unknown execution mode')
    repeats = ['off1','off2','on1','on2'] if mode=='probe' else ['reference']
    replays = diagnostics['replays']
    if [r['repeat'] for r in replays] != repeats or document['identity'].get('reference_execution') != [r['identity'] for r in replays]:
        raise ValueError('Ret reference repetition/identity mismatch')
    rows = [json.loads(line) for line in trace.splitlines()]
    if len(rows) != 3000*len(repeats):
        raise ValueError('Ret reference trace incomplete')
    base = document['identity']['output_identity'].get('reference')
    spec = document['identity'].get('reference_configuration',base)
    if 'source' in cell and (cell['conditions'].get('reference_arm') != spec['arm']
                            or cell['conditions'].get('reference_policy') != spec['policy']):
        raise ValueError('Ret reference configured arm/policy differs from cell')
    for index,replay in enumerate(replays):
        execution = replay['identity']
        if (execution['arm'] not in ARMS or execution['policy'] not in (DETERMINISTIC,OBSERVED)
                or execution['arm'] != spec['arm'] or execution['policy'] != spec['policy']
                or execution['training']['epochs'] != 3000
                or execution['training']['seed'] != cell['conditions']['seed']
                or canonical_sha256(execution['environment']) != execution['numerical_environment_hash']
                or execution['initial_state_hash'] != replay['initial_state_hash']
                or execution['training_start_rng'] != replay['initial_rng']
                or base is not None and any(execution[k] != v for k,v in base.items())):
            raise ValueError('Ret reference execution binding mismatch')
        if execution['policy']==OBSERVED and mode!='probe':
            raise ValueError('observed policy cannot define a new reference')
        if execution['policy']==DETERMINISTIC:
            expected=dict(deterministic_algorithms=True,deterministic_warn_only=False,cudnn_deterministic=True,
                cudnn_benchmark=False,matmul_tf32=False,cudnn_tf32=False,cublas_workspace_config=':4096:8')
            if execution['environment']['backend'] != expected or not execution['environment']['configured_before_cuda']:
                raise ValueError('Ret deterministic backend receipt mismatch')
        observed = not replay['repeat'].startswith('off')
        current = rows[index*3000:(index+1)*3000]
        if replay['observe'] is not observed or [r['epoch'] for r in current] != list(range(1,3001)):
            raise ValueError('Ret reference observer/epoch mismatch')
        fields = {'repeat','epoch','train_loss','update_lr'} | ({'validation_accuracy','validation_cross_entropy'} if observed else set())
        if any(set(r)!=fields or r['repeat']!=replay['repeat'] or any(
                not math.isfinite(v) for k,v in r.items() if k!='repeat') for r in current):
            raise ValueError('Ret reference trace fields/nonfinite values')
        if observed:
            best = max(current,key=lambda r:r['validation_accuracy'])
            if replay['validation_best'] != dict(epoch=best['epoch'],accuracy=best['validation_accuracy'],cross_entropy=best['validation_cross_entropy']):
                raise ValueError('Ret reference best is not earliest validation maximum')
            from experiments.observers.retrain_validation import window_summary
            if replay['windows'] != window_summary(current,replay['validation_best']):
                raise ValueError('Ret reference window statistics mismatch')
        elif replay['validation_best'] is not None or replay['windows'] is not None:
            raise ValueError('Ret off repetition contains validation selection')
        endpoints = replay['endpoints']
        if set(endpoints) != ({'final','best'} if observed else {'final'}):
            raise ValueError('Ret reference fixed endpoint set mismatch')
        if [r['epoch'] for r in replay['snapshots']] != list(AUDIT_EPOCHS):
            raise ValueError('Ret reference training audit steps mismatch')
        if replay['snapshots'][-1]['state_hash'] != endpoints['final']['state_hash'] or replay['snapshots'][-1]['rng'] != replay['final_rng']:
            raise ValueError('Ret reference final state/RNG differs from training endpoint')
        for role,endpoint in endpoints.items():
            epoch = 3000 if role=='final' else replay['validation_best']['epoch']
            if endpoint['epoch'] != epoch or endpoint['checkpoint_role'] != role or set(endpoint['probes']) != {'original','retained'}:
                raise ValueError('Ret reference endpoint identity mismatch')
    return diagnostics


def load_endpoints(run_path, run_sha256, cell_id, *, dataset_root, store_root):
    """Consume exact run/Output plus hashed weights and logits; never train or forward."""
    import numpy as np
    import torch
    from pathlib import Path
    from experiments.modular_artifacts import read_run, safe_path
    from experiments.unlearning_outputs import load_output_payload, resolve_output
    from utils.target_checkpoint import load_weights, state_hash, sha256_file
    run, documents = read_run(run_path,run_sha256)
    matches = [(cell,doc) for cell,doc in zip(run['cells'],documents) if cell['cell_id']==cell_id]
    if len(matches)!=1:
        raise ValueError('Ret endpoint requires one exact cell')
    cell,document = matches[0]
    saved = json.loads(document['observers/ret_reference_trace/result.json'])
    reference = next(r for r in cell['observers'] if r['name']=='ret_reference_trace')
    diagnostics = validate_trace(saved,document['observers/ret_reference_trace/trace.jsonl'],reference,cell)
    source = cell.get('output',cell.get('source',{}).get('output'))
    payload = load_output_payload(source,store_root,dataset_root=dataset_root)
    resolved = resolve_output(payload,dataset_root)
    root = Path(dataset_root)
    endpoints = {}
    for replay in diagnostics['replays']:
        endpoints[replay['repeat']] = {}
        for role,entry in replay['endpoints'].items():
            path = safe_path(root,entry['weights']['path'])
            loaded = load_weights(path)
            if loaded['file_sha256'] != entry['weights']['sha256'] or loaded['state_hash'] != entry['state_hash']:
                raise ValueError('Ret endpoint weights bytes/state mismatch')
            predictions = {}
            for graph,probe in entry['probes'].items():
                path = safe_path(root,probe['path'])
                if sha256_file(path)!=probe['sha256']:
                    raise ValueError('Ret endpoint logits file checksum mismatch')
                with np.load(path,allow_pickle=False) as values:
                    if set(values.files)!={'logits'}:
                        raise ValueError('Ret endpoint logits fields mismatch')
                    logits = values['logits'].copy()
                if logits.shape != resolved.arrays['logits'].shape or not np.isfinite(logits).all():
                    raise ValueError('Ret endpoint logits shape/nonfinite mismatch')
                from experiments.observers.retrain_validation import classification
                measured = classification(torch.tensor(logits),torch.tensor(resolved.arrays['y']),torch.tensor(resolved.arrays['test_mask']))
                if measured['accuracy'] != probe['test']['accuracy'] or not math.isclose(
                        measured['cross_entropy'],probe['test']['cross_entropy'],rel_tol=1e-6,abs_tol=1e-5):
                    raise ValueError('Ret endpoint saved metrics disagree with bound labels/logits')
                predictions[graph] = logits
            if 'output' in cell and role=='final':
                if loaded['state_hash'] != state_hash({k:torch.tensor(v) for k,v in payload.state.items()}) or not np.array_equal(predictions['original'],payload.arrays['logits']):
                    raise ValueError('Ret final endpoint differs from cell Output')
            endpoints[replay['repeat']][role] = dict(state=loaded['state_dict'],logits=predictions,manifest=entry)
    return dict(run=run,cell=cell,diagnostics=diagnostics,endpoints=endpoints,output=resolved,
                mode='read_only_no_forward')
