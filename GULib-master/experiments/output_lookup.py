"""Read existing Output artifacts before invoking any model computation.

The request matches the persisted Output v2 contract and its registered source
compatibility. Execution consumers still own production and recheck on MISS.
"""
from pathlib import Path
from cache_v2 import ArtifactRecipe, ArtifactType, canonical_sha256
from cache_v2.unlearning_output import OUTPUT_CONTRACT
from experiments.checkpoint_references import training_identity, ensemble_identity, read_checkpoint_reference


class OutputLookup:
    def __init__(self, checkpoint_root, store_root, reference_directory):
        self.checkpoint_root = checkpoint_root
        self.store_root = Path(store_root)
        self.reference_directory = reference_directory
        self.group = None
        self.references = {}
        self.requests = {}
        self.catalogue_count = None

    def select_group(self, group):
        if group != self.group:
            self.references.clear()
            self.requests.clear()
            self.catalogue_count = None
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

    def prepare(self, instances, data):
        """Register shared method/checkpoint metadata once before cell access."""
        from experiments.modular_gu import gu_producer
        for instance in instances:
            gu_producer(instance['method'], instance['model'])
            if instance['method'] != 'Retrain':
                self.checkpoint(instance, data)
            if instance['method'] in ('GraphEraser','GraphRevoker'):
                self.checkpoint(instance, data, ensemble=True)

    def lookup(self, instance, *, selection, data, dataset_input, dataset_identity, dataset_root,
               inputs, observer=None, audit=None):
        from experiments.modular_gu import gu_producer
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
        pairing = dict(data_identity=dataset_identity, selected_nodes=list(selection.selected_nodes),
                       deletion=instance['deletion'],model=instance['model'],training=instance['training'])
        lookup_fields = {'dataset_input':dataset_input, 'target':target,
            'selection':{k:getattr(selection,k) for k in ('artifact_id','recipe_hash','content_hash')},
            'graph_fingerprint':inputs.graph_fingerprint, 'artifact_contract':OUTPUT_CONTRACT}
        key = canonical_sha256(dict(fields=lookup_fields,pairing=pairing,producer=producer.to_dict()))
        from cache_v2 import CacheIndex, ArtifactResolver
        from cache_v2.runtime import _decode_exact_mapping
        from cache_v2.source_compatibility import recipe_candidates
        from experiments.evaluation_cache import evaluate_single, phase
        index_path = self.store_root / 'index.sqlite'
        if not index_path.is_file():
            return None, None
        with phase(audit, 'output_query'):
            index = CacheIndex(index_path)
            with index.read_session():
                count = index.artifact_count(ArtifactType.PREDICTION)
                if count != self.catalogue_count:
                    self.requests.clear()
                    self.catalogue_count = count
                if key not in self.requests:
                    candidates = []
                    for record in index.find_artifacts_by_type(ArtifactType.PREDICTION, recipe_fields=lookup_fields,
                                                              parent_artifact_id=selection.artifact_id):
                        wrapper = _decode_exact_mapping(record['recipe'],'Output Recipe')
                        recipe = ArtifactRecipe(wrapper['fields'],recipe_version=wrapper['recipe_version'])
                        fields = recipe.fields
                        if any(fields['pairing'].get(k) != v for k,v in pairing.items()):
                            continue
                        current = ArtifactRecipe({**fields,'producer_version':producer.to_dict()})
                        rank = next((i for i,candidate in enumerate(recipe_candidates(ArtifactType.PREDICTION,current)) if candidate==recipe),None)
                        if rank is not None:
                            candidates.append((rank,record,recipe))
                    if not candidates:
                        return None, None
                    first_rank = min(c[0] for c in candidates)
                    preferred = [c for c in candidates if c[0]==first_rank]
                    if len(preferred) != 1:
                        raise ValueError('ambiguous registered Output for the same effective inputs')
                    _, record, recipe = preferred[0]
                    self.requests[key] = ({k:record[k] for k in ('artifact_id','recipe_hash','content_hash')},recipe)
                reference, recipe = self.requests[key]
                explanation = ArtifactResolver(index).explain_cached(ArtifactType.PREDICTION,recipe)
                if not explanation.hit or any(explanation.exact_candidate[k] != v for k,v in reference.items()):
                    raise ValueError('Output lookup failed closed: ' + ','.join(explanation.miss_reasons))
            reference = dict(reference)
            actual_identity = {k:v for k,v in recipe.fields.items() if k != 'artifact_contract'}
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
