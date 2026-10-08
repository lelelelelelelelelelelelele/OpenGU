"""Read existing Output artifacts before invoking any model computation.

The request is the persisted Output v2 contract. Execution consumers still own
production and recheck on MISS; no source aliases or alternate artifact keys.
"""
from pathlib import Path
from cache_v2 import ArtifactRecipe, ArtifactType, canonical_sha256
from cache_v2.unlearning_output import OUTPUT_CONTRACT
from experiments.artifact_producer import FormalArtifactRequest
from experiments.checkpoint_references import training_identity, ensemble_identity, read_checkpoint_reference


class OutputLookup:
    def __init__(self, checkpoint_root, store_root, reference_directory):
        self.checkpoint_root = checkpoint_root
        self.store_root = Path(store_root)
        self.reference_directory = reference_directory
        self.group = None
        self.references = {}

    def select_group(self, group):
        if group != self.group:
            self.references.clear()
            self.group = group

    def checkpoint(self, instance, data, *, ensemble=False):
        identity = {key:instance.get(key) for key in ('model','training','checkpoint')}
        if ensemble:
            identity.update(method=instance['method'], parameters=instance['parameters'])
        key = canonical_sha256(identity)
        if key not in self.references:
            if instance.get('checkpoint') is not None and not ensemble:
                # An external PT has no trusted metadata record. Read its exact
                # state without creating a model; never guess its state hash.
                from utils.target_checkpoint import load_weights, data_identity
                from experiments.implementation_identity import implementation_fingerprint
                from experiments.checkpoint_references import model_class
                from experiments.modular_model import numerical_environment
                cls = model_class(instance['model'])
                functions = [cls.__init__, cls.forward]
                if hasattr(cls, 'load_config'):
                    functions.append(cls.load_config)
                value = load_weights(Path(self.reference_directory) / instance['checkpoint'])
                value.pop('state_dict')
                value.update(hit=False, source='external_state_dict',
                    effective_identity={'data_identity':data_identity(data), 'model':instance['model'],
                        'execution_seed':instance['training']['seed'], 'numerics':numerical_environment(data),
                        'implementation':implementation_fingerprint(*functions)})
            elif ensemble:
                metadata = ensemble_identity(instance, data)
                value = read_checkpoint_reference(self.store_root.parent / 'runtime/modular/checkpoints',
                    metadata, instance['method'].lower() + '-')
            else:
                value = read_checkpoint_reference(self.checkpoint_root, training_identity(instance, data))
            if value is None:
                return None  # A cold producer may create it later in this run.
            self.references[key] = value
        return self.references[key]

    def lookup(self, instance, *, selection, data, dataset_input, dataset_root,
               inputs, observer=None, audit=None):
        from experiments.modular_gu import gu_producer
        from experiments.node_deletion import pairing_identity
        checkpoint = preparation = None
        target = {'method':instance['method'], 'parameters':instance['parameters']}
        if instance['method'] != 'Retrain':
            checkpoint = self.checkpoint(instance, data)
            if checkpoint is None:
                return None, None
            target['checkpoint_state_hash'] = checkpoint['state_hash']
        if instance['method'] in ('GraphEraser','GraphRevoker'):
            preparation = self.checkpoint(instance, data, ensemble=True)
            if preparation is None:
                return None, None
            target.update(initialization='independent-shard-training', ensemble_state_hash=preparation['state_hash'])
        producer = gu_producer(instance['method'], instance['model'])
        identity = {'dataset_input':dataset_input, 'target':target,
            'pairing':pairing_identity(instance, data, selection.selected_nodes),
            'selection':{k:getattr(selection,k) for k in ('artifact_id','recipe_hash','content_hash')},
            'graph_fingerprint':inputs.graph_fingerprint, 'producer_version':producer.to_dict()}
        request = FormalArtifactRequest(ArtifactType.PREDICTION,
            ArtifactRecipe({'artifact_contract':OUTPUT_CONTRACT, **identity}), producer)
        from cache_v2 import CacheIndex, ArtifactResolver
        from experiments.evaluation_cache import describe_output, evaluate_single, phase
        index_path = self.store_root / 'index.sqlite'
        if not index_path.is_file():
            return None, None
        with phase(audit, 'output_query'):
            explanation = ArtifactResolver(CacheIndex(index_path)).explain_compatible(ArtifactType.PREDICTION, request.recipe)
            if not explanation.hit:
                if explanation.exact_candidate is None and explanation.miss_reasons == ('no_exact_candidate',):
                    return None, None
                raise ValueError('Output lookup failed closed: ' + ','.join(explanation.miss_reasons))
            reference = {key:explanation.exact_candidate[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
            actual_identity = describe_output(reference, self.store_root, dataset_input=dataset_input)
        values, evaluation_cache = evaluate_single(reference, actual_identity, store_root=self.store_root,
            data=data, dataset_root=dataset_root, audit=audit)
        if observer is not None and hasattr(observer, 'identity'):
            observer.identity['output_identity'] = actual_identity
        result = {**reference, 'output':reference, 'hit':True, 'producer_called':False,
            'generation_producer':actual_identity['producer_version'], 'consumption_producer':producer.to_dict(),
            'compute_seconds':0.0, **values, 'target':target, 'evaluation_cache':evaluation_cache}
        if preparation is not None:
            result['ensemble_preparation'] = preparation
        elif instance['method'] != 'MEGU':
            result['cache_policy'] = 'reuse'
        return result, checkpoint
