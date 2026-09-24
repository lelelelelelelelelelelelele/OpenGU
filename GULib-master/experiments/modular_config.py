"""One experiment table references independent, fully resolved module instances."""
from __future__ import annotations

from experiments.im_methods import IM_METHODS

import copy
import math
from pathlib import Path
from experiments.effective_config import read_yaml, fields, effective, choice, ConfigurationError
from experiments.target_direct_v1.methods import resolve_parameters, uses_model, SCORE_NAMES

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIRECTORIES = {
    'dataset_refs': 'datasets',
    'selector_refs': 'selectors',
    'unlearning_refs': 'unlearning',
    'evaluation_refs': 'evaluations',
}
PARAMETER_PROFILE_METHODS = {
    'GIF': {'scale', 'damp', 'GIF_method'},
    'IDEA': {'scale', 'damp', 'gaussian_mean', 'gaussian_std'},
}


def resolve_reference(field, reference, source_directory):
    """Resolve public names independently of the experiment table's location.

    Bare names select public instances. Explicit relative paths are anchored to
    the containing YAML; absolute files are used directly.
    """
    if not isinstance(reference, str) or not reference:
        raise ConfigurationError(f'{field} requires a YAML filename or file path')
    path = Path(reference)
    if not path.is_absolute():
        if ':' in reference:
            raise ConfigurationError(f'{field}: drive-relative paths are not allowed')
        if '/' in reference or '\\' in reference:
            path = Path(source_directory) / reference.replace('\\', '/')
        else:
            directory = (ROOT / 'experiments/configs' / REFERENCE_DIRECTORIES[field]).resolve()
            path = (directory / reference).resolve()
            if path.parent != directory:
                raise ConfigurationError(f'{field} resolves outside its public directory')
    if path.suffix not in ('.yaml', '.yml') or not path.is_file():
        raise ConfigurationError(f'{field}: YAML file does not exist: {path}')
    return path.resolve()


def resolve_parameter_profile_ref(reference, source_directory):
    if not isinstance(reference, str) or not reference.strip():
        raise ConfigurationError('parameter_profile_ref requires a YAML file path')
    path = Path(reference)
    if not path.is_absolute():
        if ':' in reference:
            raise ConfigurationError('parameter_profile_ref: drive-relative paths are not allowed')
        path = Path(source_directory) / reference.replace('\\', '/')
    if path.suffix not in ('.yaml', '.yml') or not path.is_file():
        raise ConfigurationError(f'parameter_profile_ref: YAML file does not exist: {path}')
    return path.resolve()


def load_parameter_profile(path):
    value = read_yaml(path)
    fields(value, {'kind', 'schema_version', 'profiles'},
           {'kind', 'schema_version', 'profiles'}, 'parameter profile')
    if value['kind'] != 'parameter_profile' or type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ConfigurationError(f'{path}: expected parameter_profile schema_version 1')
    if not isinstance(value['profiles'], list) or not value['profiles']:
        raise ConfigurationError('parameter profile requires a nonempty profiles list')
    names = set()
    keys = set()
    for profile in value['profiles']:
        fields(profile, {'name', 'dataset', 'model', 'methods'},
               {'name', 'dataset', 'model', 'methods'}, 'parameter profile entry')
        name = profile['name']
        dataset = profile['dataset']
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ConfigurationError('parameter profile names must be distinct nonempty strings')
        if not isinstance(dataset, str) or not dataset.strip():
            raise ConfigurationError('parameter profile dataset must be a nonempty string')
        names.add(name)
        model = profile['model']
        fields(model, {'architecture', 'hidden_channels'},
               {'architecture', 'hidden_channels'}, 'parameter profile model')
        if (model['architecture'] != 'OpenGU.GCNNet'
                or type(model['hidden_channels']) is not int or model['hidden_channels'] <= 0):
            raise ConfigurationError('GIF/IDEA profiles require a GCN architecture and positive hidden_channels')
        key = (dataset, model['architecture'], model['hidden_channels'])
        if key in keys:
            raise ConfigurationError(
                'ambiguous parameter profile entries for dataset={0}, GCN hidden_channels={1}'.format(
                    dataset, model['hidden_channels']))
        keys.add(key)
        methods = profile['methods']
        if not isinstance(methods, dict) or not methods or set(methods) - set(PARAMETER_PROFILE_METHODS):
            raise ConfigurationError('parameter profile methods must contain GIF and/or IDEA')
        for method, parameters in methods.items():
            expected = PARAMETER_PROFILE_METHODS[method]
            fields(parameters, expected, expected, 'parameter profile {0} parameters'.format(method))
            scale = parameters['scale']
            damp = parameters['damp']
            if (not isinstance(scale, (int, float)) or isinstance(scale, bool)
                    or not math.isfinite(scale) or scale <= 0
                    or not isinstance(damp, (int, float)) or isinstance(damp, bool)
                    or not math.isfinite(damp) or not 0 <= damp < 1):
                raise ConfigurationError('invalid {0} parameter profile scale/damp'.format(method))
            if method == 'GIF':
                choice(parameters['GIF_method'], ('GIF', 'IF'), 'GIF_method')
            else:
                mean = parameters['gaussian_mean']
                std = parameters['gaussian_std']
                if (not isinstance(mean, (int, float)) or isinstance(mean, bool)
                        or not math.isfinite(mean) or not isinstance(std, (int, float))
                        or isinstance(std, bool) or not math.isfinite(std) or std < 0):
                    raise ConfigurationError('invalid IDEA parameter profile gaussian settings')
    return value['profiles']


def parameter_profile_match(profiles, dataset, unlearning_path):
    method_value = read_yaml(unlearning_path)
    method = method_value.get('method')
    if method not in PARAMETER_PROFILE_METHODS:
        return None
    model = method_value.get('model', {})
    if not isinstance(model, dict):
        raise ConfigurationError('unlearning model must be a mapping')
    architecture = model.get('architecture', 'OpenGU.GCNNet')
    hidden_channels = model.get('hidden_channels', 64)
    if architecture != 'OpenGU.GCNNet':
        raise ConfigurationError('GIF/IDEA parameter profiles require OpenGU.GCNNet')
    if type(hidden_channels) is not int or hidden_channels <= 0:
        raise ConfigurationError('GIF/IDEA parameter profile matching requires positive model.hidden_channels')
    dataset_name = dataset['dataset']['name']
    matches = [profile for profile in profiles
               if profile['dataset'] == dataset_name
               and profile['model']['architecture'] == architecture
               and profile['model']['hidden_channels'] == hidden_channels]
    if len(matches) != 1:
        raise ConfigurationError(
            '{0} GIF/IDEA parameter profile matches for dataset={1}, GCN hidden_channels={2}'.format(
                'missing' if not matches else 'ambiguous', dataset_name, hidden_channels))
    profile = matches[0]
    if method not in profile['methods']:
        raise ConfigurationError(
            'parameter profile {0} has no {1} parameters for dataset={2}, GCN hidden_channels={3}'.format(
                profile['name'], method, dataset_name, hidden_channels))
    parameters = profile['methods'][method]
    supplied = method_value.get('parameters', {})
    if not isinstance(supplied, dict):
        raise ConfigurationError('unlearning parameters must be a mapping')
    overlap = set(supplied) & set(parameters)
    if overlap:
        raise ConfigurationError(
            'parameters supplied by both unlearning reference and parameter profile: {0}'.format(
                ', '.join(sorted(overlap))))
    return {'profile': profile, 'method': method, 'parameters': parameters}


def model_training(value, *, pretrained=False):
    """Resolve the OpenGU model defaults without copying them into every method file."""
    fields(value, {'model', 'training'}, (), 'model/training')
    model = value.get('model', {})
    fields(model, {'architecture', 'layers', 'hidden_channels', 'dropout'}, (), 'model')
    architecture = choice(model.get('architecture', 'OpenGU.GCNNet'),
                          ('OpenGU.GCNNet', 'OpenGU.SGCNet'), 'architecture')
    default = {'architecture': architecture, 'layers': 2, 'hidden_channels': 64, 'dropout': 0.5}
    if architecture == 'OpenGU.SGCNet':
        default.update(layers=3, dropout=0.0)
    model = effective(model, default, 'model')
    valid_layers = model['layers'] == default['layers']
    if architecture == 'OpenGU.SGCNet':
        valid_layers = type(model['layers']) is int and model['layers'] > 0
    if not valid_layers or model['hidden_channels'] <= 0 or model['dropout'] != default['dropout']:
        raise ConfigurationError('model shape/dropout is outside the supported OpenGU implementation')
    if architecture == 'OpenGU.SGCNet' and model['hidden_channels'] != 64:
        raise ConfigurationError('OpenGU SGC has no hidden_channels override')
    if pretrained:
        supplied = value.get('training', {})
        unused = ('epochs', 'optimizer', 'lr', 'weight_decay', 'scheduler')
        fields(supplied, {'seed', *unused}, (), 'training')
        seed = effective({k: v for k, v in supplied.items() if k == 'seed'}, {'seed': 42}, 'training')['seed']
        if seed < 0:
            raise ConfigurationError('invalid training seed')
        # These settings describe no executed training in the external-weight lane.
        return model, {**dict.fromkeys(unused), 'seed': seed}
    props = read_yaml(ROOT / 'model/properties' / ('GCN.yaml' if architecture.endswith('GCNNet') else 'SGC.yaml'))
    training = effective(value.get('training', {}), {'epochs': 3000, 'optimizer': 'Adam', 'lr': float(props['lr']),
        'weight_decay': float(props['decay']), 'scheduler': 'none', 'seed': 42}, 'training')
    choice(training['optimizer'], ('Adam', 'SGD'), 'optimizer')
    choice(training['scheduler'], ('none',), 'scheduler')
    if training['epochs'] <= 0 or training['lr'] <= 0 or training['weight_decay'] < 0 or training['seed'] < 0:
        raise ConfigurationError('invalid training settings')
    return model, training


def selector(value):
    fields(value, {'kind', 'schema_version', 'method', 'candidate', 'budget', 'selection_rule',
                   'model', 'training', 'parameters', 'numerics', 'checkpoint'},
                  {'kind', 'schema_version', 'method', 'candidate', 'budget'}, 'selector')
    choice(value['method'], (*SCORE_NAMES, *IM_METHODS), 'selector method')
    if value['candidate'] != {'pool': 'train_mask'}:
        raise ConfigurationError('candidate pool must explicitly reference persisted train_mask')
    result = {key: value[key] for key in ('kind', 'schema_version', 'method', 'candidate', 'budget')}
    if value['method'] in IM_METHODS:
        from experiments.modular_im import resolve_im_parameters
        from experiments.modular_rr import resolve_rr_parameters
        resolver = resolve_im_parameters if value['method'] == 'im' else resolve_rr_parameters
        result['parameters'] = resolver(value.get('parameters', {}))
        if set(value) & {'model', 'training', 'checkpoint', 'selection_rule', 'numerics'}:
            raise ConfigurationError('IM is a topology-only K-set selector without a ranking rule')
        return result
    result['parameters'] = resolve_parameters(value['method'], value.get('parameters'))
    result['selection_rule'] = effective(value.get('selection_rule', {}),
        {'direction': 'descending', 'tie_break': 'node_id_ascending'}, 'selection_rule')
    if result['selection_rule'] != {'direction': 'descending', 'tie_break': 'node_id_ascending'}:
        raise ConfigurationError('only score_desc_node_id_asc is implemented')
    result['numerics'] = effective(value.get('numerics', {}), {'dtype': 'float32'}, 'numerics')
    choice(result['numerics']['dtype'], ('float32',), 'dtype')
    if uses_model(value['method']):
        if value.get('checkpoint') and value['method'].startswith('tracin_cp_'):
            raise ConfigurationError('trajectory selectors train their own checkpoints; a final PT is insufficient')
        result['model'], result['training'] = model_training({k: value[k] for k in ('model', 'training') if k in value}, pretrained=value.get('checkpoint') is not None)
        if 'checkpoint' in value:
            result['checkpoint'] = value['checkpoint']
    elif set(value) & {'model', 'training', 'checkpoint'}:
        raise ConfigurationError('topology/random selector must not declare an unused model')
    return result


def gu_defaults(method):
    if method == 'Retrain':
        return {}
    # Defaults are read from the real CLI owner, without importing config.py.
    import sys
    from parameter_parser import parameter_parser
    previous = sys.argv
    try:
        sys.argv = ['modular-defaults']
        defaults = parameter_parser()
    finally:
        sys.argv = previous
    if method == 'GraphEraser':
        from experiments.modular_shards import grapheraser_defaults
        return grapheraser_defaults(defaults)
    if method == 'GraphRevoker':
        from experiments.modular_graphrevoker import graphrevoker_defaults
        return graphrevoker_defaults(defaults)
    if method == 'GNNDelete':
        result = {k: defaults[k] for k in ('unlearn_lr', 'unlearning_epochs', 'alpha', 'loss_fct', 'loss_type')}
        result.update(deletion_optimizer='Adam', deletion_weight_decay=0.0)
        return result
    if method == 'GIF':
        return {k: defaults[k] for k in ('iteration', 'scale', 'damp', 'GIF_method')}
    if method == 'MEGU':
        props = read_yaml(ROOT / 'model/properties/GCN.yaml')
        return {**{k: defaults[k] for k in ('unlearning_epochs', 'kappa', 'alpha1', 'alpha2', 'GNN_layer')},
                'unlearn_lr': float(props['lr']), 'unlearn_weight_decay': float(props['decay'])}

    if method == 'IDEA':
        return {k: defaults[k] for k in ('iteration', 'scale', 'damp', 'gaussian_mean', 'gaussian_std')}
    raise ConfigurationError('supported GU methods: GNNDelete, GIF, MEGU, IDEA, GraphEraser, GraphRevoker, Retrain')


def unlearning(value, *, parameter_profile_parameters=None):
    fields(value, {'kind', 'schema_version', 'method', 'model', 'training', 'parameters', 'checkpoint', 'deletion'},
                  {'kind', 'schema_version', 'method'}, 'unlearning')
    supplied_parameters = value.get('parameters', {})
    if parameter_profile_parameters is not None:
        if not isinstance(supplied_parameters, dict):
            raise ConfigurationError('unlearning parameters must be a mapping')
        overlap = set(supplied_parameters) & set(parameter_profile_parameters)
        if overlap:
            raise ConfigurationError(
                'parameters supplied by both unlearning reference and parameter profile: {0}'.format(
                    ', '.join(sorted(overlap))))
        supplied_parameters = {**supplied_parameters, **parameter_profile_parameters}
    params = effective(supplied_parameters, gu_defaults(value['method']))
    if value['method'] == 'GraphEraser':
        from experiments.modular_shards import validate_grapheraser
        validate_grapheraser(params)
    if value['method'] == 'GraphRevoker':
        from experiments.modular_graphrevoker import validate_graphrevoker
        validate_graphrevoker(params)
    if value['method'] == 'GNNDelete':
        if (params['unlearn_lr'] <= 0 or params['unlearning_epochs'] <= 0 or not 0 <= params['alpha'] <= 1
                or params['deletion_optimizer'] != 'Adam' or params['deletion_weight_decay'] != 0
                or params['loss_type'] != 'both_layerwise' or params['loss_fct'] != 'mse_mean'):
            raise ConfigurationError('invalid or unsupported GNNDelete node configuration')
    elif value['method'] == 'GIF':
        if params['iteration'] <= 0 or params['scale'] <= 0 or not 0 <= params['damp'] < 1:
            raise ConfigurationError('invalid GIF parameters')
        choice(params['GIF_method'], ('GIF', 'IF'), 'GIF_method')
    if value['method'] == 'MEGU':
        if (params['unlearning_epochs'] <= 0 or params['GNN_layer'] <= 0 or params['kappa'] < 0
                or not 0 <= params['alpha1'] <= 1 or not 0 <= params['alpha2'] <= 1):
            raise ConfigurationError('invalid MEGU parameters')
    elif value['method'] == 'IDEA':
        if (type(params['iteration']) is not int or params['iteration'] <= 0
                or not math.isfinite(params['scale']) or params['scale'] <= 0
                or not 0 <= params['damp'] < 1
                or not math.isfinite(params['gaussian_mean'])
                or not math.isfinite(params['gaussian_std']) or params['gaussian_std'] < 0):
            raise ConfigurationError('invalid IDEA parameters')
    if value['method'] == 'MEGU' and (not math.isfinite(params['unlearn_lr']) or params['unlearn_lr'] <= 0
            or not math.isfinite(params['unlearn_weight_decay']) or params['unlearn_weight_decay'] < 0):
        raise ConfigurationError('invalid MEGU unlearning optimizer settings')
    checkpoint = value.get('checkpoint')
    if checkpoint is not None:
        if value['method'] not in ('GIF', 'IDEA', 'MEGU', 'GNNDelete'):
            raise ConfigurationError('external checkpoint requires a supported single-model GU method')
        if not isinstance(checkpoint, str) or not checkpoint.strip():
            raise ConfigurationError('checkpoint must be a nonempty pure state_dict file path')
    model, training = model_training({k: value[k] for k in ('model', 'training') if k in value},
                                     pretrained=checkpoint is not None)
    if value['method'] == 'GraphEraser' and model['architecture'] != 'OpenGU.GCNNet':
        raise ConfigurationError('GraphEraser modular node consumer currently supports GCN')
    if value['method'] == 'GNNDelete' and model['architecture'] != 'OpenGU.GCNNet':
        raise ConfigurationError('GNNDelete modular node consumer currently supports GCN')
    if value['method'] == 'IDEA' and model['architecture'] != 'OpenGU.GCNNet':
        raise ConfigurationError('IDEA modular node consumer currently supports GCN')
    if value['method'] == 'Retrain' and 'checkpoint' in value:
        raise ConfigurationError('Retrain starts from scratch and cannot consume a checkpoint')
    from experiments.node_deletion import resolve_deletion
    return {**value, 'model': model, 'training': training, 'parameters': params,
            'deletion': resolve_deletion(value.get('deletion'))}


def load_instance(path, expected_kind, *, parameter_profile_parameters=None):
    value = read_yaml(path)
    if value.get('kind') != expected_kind or type(value.get('schema_version')) is not int or value.get('schema_version') != 1:
        raise ConfigurationError(f'{path}: expected {expected_kind} schema_version 1')
    if expected_kind in ('unlearning', 'selector') and 'checkpoint' in value:
        checkpoint = value['checkpoint']
        if checkpoint is None:
            del value['checkpoint']
        elif not isinstance(checkpoint, str) or not checkpoint.strip():
            raise ConfigurationError('checkpoint must be a nonempty pure state_dict file path')
        else:
            value['checkpoint'] = str((Path(path).resolve().parent / checkpoint).resolve())
    if expected_kind == 'selector':
        return selector(value)
    if expected_kind == 'unlearning':
        return unlearning(value, parameter_profile_parameters=parameter_profile_parameters)
    if expected_kind == 'evaluation':
        from experiments.modular_evaluation import resolve_evaluation
        return resolve_evaluation(value)
    fields(value, {'kind', 'schema_version', 'dataset', 'preprocessing', 'split', 'artifacts'},
                  {'kind', 'schema_version', 'dataset', 'preprocessing', 'split', 'artifacts'}, 'dataset_split')
    fields(value['preprocessing'], {'adapter'}, {'adapter'}, 'preprocessing')
    choice(value['preprocessing']['adapter'], ('OpenGU_persisted_processed_pair',), 'preprocessing.adapter')
    split = value['split']
    fields(split, {'profile', 'train_ratio', 'val_ratio', 'test_ratio', 'seed'},
           {'profile', 'train_ratio', 'val_ratio', 'test_ratio', 'seed'}, 'split')
    split = effective(split, {'profile':'', 'train_ratio':.7, 'val_ratio':.1, 'test_ratio':.2, 'seed':2024}, 'split')
    if not split['profile'] or split['seed'] < 0 or any(not 0 < split[k] < 1 for k in ('train_ratio','val_ratio','test_ratio')):
        raise ConfigurationError('invalid persisted split metadata')
    if abs(sum(split[k] for k in ('train_ratio','val_ratio','test_ratio')) - 1) > 1e-12:
        raise ConfigurationError('split ratios must sum to one')
    value['split'] = split
    return value


def configuration_sources(path, resolved, *, parameter_profile_parameters=None, parameter_profile_source=None):
    """Per-field provenance is recorded outside all computational identities."""
    original = read_yaml(path)
    sources = {}
    def visit(value, supplied, prefix=''):
        for key, item in value.items():
            name = prefix + key
            if isinstance(item, dict):
                visit(item, supplied.get(key, {}), name + '.')
            elif (name.startswith('parameters.') and parameter_profile_parameters is not None
                  and name[len('parameters.'):] in parameter_profile_parameters):
                sources[name] = 'parameter_profile:' + str(Path(parameter_profile_source).resolve())
            elif name in ('training.lr', 'training.weight_decay', 'training.epochs',
                          'training.optimizer', 'training.scheduler') and item is None and resolved.get('checkpoint'):
                sources[name] = 'not_applicable:external_checkpoint'
            elif key in supplied:
                sources[name] = 'instance:' + str(Path(path).resolve())
            elif name.startswith('parameters.') and resolved.get('method') in IM_METHODS:
                sources[name] = ('experiments/selection_producer.py:ImParameters' if resolved['method'] == 'im'
                                else 'experiments/modular_rr.py:resolve_rr_parameters')
            elif name.startswith('parameters.'):
                sources[name] = ('experiments/target_direct_v1/methods.py:parameter_defaults' if resolved['kind'] == 'selector'
                                 else 'parameter_parser.py + experiments/modular_config.py:gu_defaults')
            elif name in ('training.lr', 'training.weight_decay'):
                sources[name] = 'model/properties/' + ('GCN.yaml' if resolved['model']['architecture'].endswith('GCNNet') else 'SGC.yaml')
            else:
                sources[name] = 'experiments/modular_config.py:declared_defaults'
    visit(resolved, original)
    return sources


def resolve_budget(value, candidate_count):
    fields(value, {'mode', 'value', 'denominator', 'rounding'}, {'mode', 'value'}, 'budget')
    mode = choice(value['mode'], ('ratio', 'k'), 'budget.mode')
    if mode == 'ratio':
        normalized = effective(value, {'mode': 'ratio', 'value': 0.01,
            'denominator': 'train_candidate_count', 'rounding': 'floor_with_minimum_one'}, 'budget')
        if not 0 < normalized['value'] <= 1 or normalized['denominator'] != 'train_candidate_count' or normalized['rounding'] != 'floor_with_minimum_one':
            raise ConfigurationError('invalid ratio budget')
        k = max(1, int(candidate_count * normalized['value']))
    else:
        fields(value, {'mode', 'value'}, {'mode', 'value'}, 'absolute budget')
        normalized = effective(value, {'mode': 'k', 'value': 1}, 'budget')
        k = normalized['value']
    if not 0 < k <= candidate_count:
        raise ConfigurationError('K is outside the candidate set')
    return {**normalized, 'k': k}


def load_experiment(path):
    path = Path(path).resolve()
    value = read_yaml(path)
    required = {'kind', 'schema_version', 'experiment_id', 'stage', 'dataset_refs', 'matrix'}
    fields(value, required | {'round',
        'selector_refs', 'unlearning_refs', 'evaluation_refs', 'case_id', 'output_inputs',
        'seeds', 'random_selector_seeds', 'budget_ratios', 'im_selector_seeds', 'return_scores',
        'execution', 'observers', 'parameter_profile_ref'},
        required, 'experiment')
    if value['kind'] != 'experiment' or type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ConfigurationError('expected experiment schema_version 1')
    choice(value['stage'], ('selector', 'unlearning', 'metrics'), 'stage')
    choice(value['matrix'], ('cartesian_product',), 'matrix')
    if value['stage'] != 'metrics' and not value.get('selector_refs'):
        raise ConfigurationError('selector_refs is required for selector and unlearning stages')
    if value['stage'] == 'selector' and value.get('unlearning_refs'):
        raise ConfigurationError('selector stage needs selector_refs and no GU inputs')
    if value['stage'] == 'unlearning' and not value.get('unlearning_refs'):
        raise ConfigurationError('unlearning stage requires unlearning_refs')
    if value['stage'] == 'metrics':
        if not value.get('output_inputs') or not value.get('evaluation_refs'):
            raise ConfigurationError('metrics stage requires output_inputs and evaluation_refs')
        if any(value.get(key) for key in ('selector_refs', 'unlearning_refs')):
            raise ConfigurationError('metrics stage consumes only explicit output references')
    elif 'output_inputs' in value:
        raise ConfigurationError('output_inputs belongs to the metrics stage')
    if type(value.get('return_scores', False)) is not bool:
        raise ConfigurationError('return_scores must be boolean')
    if value['stage'] == 'metrics':
        if value.get('return_scores'):
            raise ConfigurationError('metrics does not generate scores')
        for source in value['output_inputs']:
            fields(source, {'run', 'sha256'}, {'run', 'sha256'}, 'metrics input')
    result = dict(value)
    refs = value['dataset_refs']
    if not isinstance(refs, list) or not refs:
        raise ConfigurationError('dataset_refs must be a nonempty list')
    paths = [resolve_reference('dataset_refs', ref, path.parent) for ref in refs]
    result['datasets'] = [load_instance(p, 'dataset_split') for p in paths]
    from cache_v2 import canonical_sha256
    fingerprints = [canonical_sha256(item) for item in result['datasets']]
    if len(set(paths)) != len(paths) or len(set(fingerprints)) != len(fingerprints):
        raise ConfigurationError('dataset_refs must not contain duplicate Dataset/Split instances')
    result['dataset_directories'] = [str(p.parent) for p in paths]
    result['configuration_sources'] = {
        'datasets': [str(p) for p in paths], 'selectors': [], 'unlearnings': [], 'evaluations': []}
    profile_path = None
    profile_entries = None
    if 'parameter_profile_ref' in value:
        if value['stage'] != 'unlearning':
            raise ConfigurationError('parameter_profile_ref belongs to the unlearning stage')
        profile_path = resolve_parameter_profile_ref(value['parameter_profile_ref'], path.parent)
        profile_entries = load_parameter_profile(profile_path)
        result['configuration_sources']['parameter_profile'] = str(profile_path)
    for field, kind in (('selector_refs', 'selector'), ('unlearning_refs', 'unlearning'),
                        ('evaluation_refs', 'evaluation')):
        refs = value.get(field, [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ConfigurationError(f'{field} must be a list of file references')
        paths = [resolve_reference(field, ref, path.parent) for ref in refs]
        if field == 'unlearning_refs' and profile_entries is not None:
            unlearnings_by_dataset = []
            sources_by_dataset = []
            profiles_by_dataset = []
            for dataset in result['datasets']:
                unlearnings = []
                sources = []
                selections = {}
                for ref_path in paths:
                    match = parameter_profile_match(profile_entries, dataset, ref_path)
                    if match is None:
                        instance = load_instance(ref_path, kind)
                        source = configuration_sources(ref_path, instance)
                    else:
                        profile = match['profile']
                        parameters = match['parameters']
                        instance = load_instance(ref_path, kind, parameter_profile_parameters=parameters)
                        source = configuration_sources(ref_path, instance,
                            parameter_profile_parameters=parameters, parameter_profile_source=profile_path)
                        selected = selections.setdefault(profile['name'], {
                            'name': profile['name'], 'dataset': profile['dataset'],
                            'model': copy.deepcopy(profile['model']), 'methods': {}})
                        selected['methods'][match['method']] = copy.deepcopy(parameters)
                    unlearnings.append(instance)
                    sources.append(source)
                if not selections:
                    raise ConfigurationError('parameter_profile_ref requires at least one GIF or IDEA unlearning reference')
                unlearnings_by_dataset.append(unlearnings)
                sources_by_dataset.append(sources)
                profiles_by_dataset.append({'reference': str(profile_path),
                    'selections': list(selections.values())})
            result['unlearnings_by_dataset'] = unlearnings_by_dataset
            result['configuration_sources']['unlearnings_by_dataset'] = sources_by_dataset
            result['effective_parameter_profiles'] = profiles_by_dataset
            result['unlearnings'] = unlearnings_by_dataset[0]
            result['configuration_sources']['unlearnings'] = sources_by_dataset[0]
            result['effective_parameter_profile'] = {
                'reference': str(profile_path), 'by_dataset': profiles_by_dataset}
            continue
        result[kind + 's'] = [load_instance(ref_path, kind) for ref_path in paths]
        result['configuration_sources'][kind + 's'] = [configuration_sources(ref_path, item)
            for ref_path, item in zip(paths, result[kind + 's'])]
    from experiments.observers import observer_specs, validate_capabilities
    execution = value.get('execution', {})
    fields(execution, {'gu_cache'}, (), 'execution')
    policies = execution.get('gu_cache', {})
    methods = {item['method'] for item in result['unlearnings']}
    fields(policies, methods, (), 'execution.gu_cache')
    result['execution'] = {'gu_cache': policies}
    result['observers'] = []
    if not isinstance(value.get('observers', []), list):
        raise ConfigurationError('observers must be a list')
    for entry in value.get('observers', []):
        fields(entry, {'name', 'parameters', 'methods'}, {'name', 'methods'}, 'observer attachment')
        if (not isinstance(entry['methods'], list) or not entry['methods']
                or len(set(entry['methods'])) != len(entry['methods']) or set(entry['methods']) - methods):
            raise ConfigurationError('observer methods must select distinct configured methods')
        from experiments.observers import resolve_observer
        spec = resolve_observer({k: v for k, v in entry.items() if k != 'methods'})
        result['observers'].append({'methods': entry['methods'], 'instance': spec})
    if value['stage'] != 'unlearning' and (execution or result['observers']):
        raise ConfigurationError('execution and observers belong to unlearning')
    for method in methods:
        specs = observer_specs(result, method)
        if len({spec['name'] for spec in specs}) != len(specs):
            raise ConfigurationError('duplicate observer for method')
        validate_capabilities(method, specs, policies.get(method, 'reuse'))
    result['source_directory'] = str(path.parent)
    # Validate matrix axes while parsing, including during the ordinary dry-run.
    validate_repeats(result)
    return result


def validate_repeats(config):
    """Explicit experimental axes, not arbitrary module-parameter overrides."""
    for field in ('seeds', 'random_selector_seeds', 'budget_ratios', 'im_selector_seeds'):
        if field not in config:
            continue
        values = config[field]
        if config['stage'] == 'metrics':
            raise ConfigurationError('metrics consumes fixed outputs and cannot declare repeat axes')
        if not isinstance(values, list) or not values:
            raise ConfigurationError(field + ' must be a nonempty list')
        for value in values:
            valid = (type(value) is int and value >= 0) if field in ('seeds', 'random_selector_seeds', 'im_selector_seeds') else (
                type(value) in (int, float) and math.isfinite(value) and 0 < value <= 1)
            if not valid:
                raise ConfigurationError('invalid ' + field + ' value')
        if len(set(values)) != len(values):
            raise ConfigurationError(field + ' must not contain duplicates')
    if 'random_selector_seeds' in config and not any(s['method'] == 'random' for s in config['selectors']):
        raise ConfigurationError('random_selector_seeds requires a Random selector')
    im = [s for s in config['selectors'] if s['method'] in IM_METHODS]
    if 'im_selector_seeds' in config and not im:
        raise ConfigurationError('im_selector_seeds requires an IM selector')
    if im and config.get('return_scores'):
        raise ConfigurationError('IM Selection stores selected nodes only; return_scores is unavailable')
    if 'budget_ratios' in config:
        if not config['selectors'] or any(s['budget']['mode'] != 'ratio' for s in config['selectors']):
            raise ConfigurationError('budget_ratios requires ratio-based selector refs')
    if 'seeds' in config:
        models = [s for s in config['selectors'] if s['method'] not in IM_METHODS and uses_model(s['method'])] + config['unlearnings']
        if not models:
            raise ConfigurationError('seeds requires a model training consumer')
        if any('checkpoint' in instance for instance in models):
            raise ConfigurationError('seeds cannot relabel an explicit checkpoint; use separate instances')


def experiment_batches(config):
    """Resolve paired training repetitions in memory; never write leaf YAML.

    Within a batch, Selector x Unlearning remains the existing Cartesian product.
    Training seeds are paired across the two model consumers, not crossed.
    """
    for index, dataset in enumerate(config['datasets']):
        for seed in config.get('seeds', [None]):
            for ratio in config.get('budget_ratios', [None]):
                batch = copy.deepcopy(config)
                batch['dataset'] = dataset
                batch['dataset_directory'] = config['dataset_directories'][index]
                batch['matrix_values'] = {**dataset_binding(config, index), 'training_seed': seed, 'budget_ratio': ratio}
                if 'unlearnings_by_dataset' in config:
                    batch['unlearnings'] = copy.deepcopy(config['unlearnings_by_dataset'][index])
                    batch['configuration_sources']['unlearnings'] = copy.deepcopy(
                        config['configuration_sources']['unlearnings_by_dataset'][index])
                    batch['effective_parameter_profile'] = copy.deepcopy(
                        config['effective_parameter_profiles'][index])
                for kind in ('selector', 'unlearning'):
                    for instance_index, instance in enumerate(batch[kind + 's']):
                        sources = batch['configuration_sources'][kind + 's'][instance_index]
                        if seed is not None and 'training' in instance:
                            instance['training']['seed'] = seed
                            sources['training.seed'] = 'experiment:seeds'
                        if kind == 'selector' and ratio is not None:
                            instance['budget']['value'] = float(ratio)
                            sources['budget.value'] = 'experiment:budget_ratios'
                im = [i for i, item in enumerate(batch['selectors']) if item['method'] in IM_METHODS]
                random = [i for i, item in enumerate(batch['selectors'])
                          if item['method'] == 'random' and 'random_selector_seeds' in config]
                ordinary = [i for i in range(len(batch['selectors'])) if i not in im and i not in random]
                if not im and not random:
                    yield batch
                    continue
                def subset(indices):
                    part = copy.deepcopy(batch)
                    part['selectors'] = [part['selectors'][i] for i in indices]
                    part['selector_refs'] = [part['selector_refs'][i] for i in indices]
                    part['configuration_sources']['selectors'] = [part['configuration_sources']['selectors'][i] for i in indices]
                    return part
                if ordinary:
                    yield subset(ordinary)
                for i in random:
                    for random_seed in config['random_selector_seeds']:
                        part = subset([i])
                        part['selectors'][0]['parameters']['seed'] = random_seed
                        part['matrix_values']['random_selector_seed'] = random_seed
                        part['configuration_sources']['selectors'][0]['parameters.seed'] = 'experiment:random_selector_seeds'
                        yield part
                for i in im:
                    for im_seed in config.get('im_selector_seeds', [batch['selectors'][i]['parameters']['im_selector_seed']]):
                        part = subset([i])
                        part['selectors'][0]['parameters']['im_selector_seed'] = im_seed
                        part['matrix_values']['im_selector_seed'] = im_seed
                        if 'im_selector_seeds' in config:
                            part['configuration_sources']['selectors'][0]['parameters.im_selector_seed'] = 'experiment:im_selector_seeds'
                        yield part


def selector_entries(batch):
    """Declared order, shared by execution and collected-result verification."""
    return list(zip(batch['selectors'], batch.get('selector_refs', [])))


def unlearning_entries(batch):
    """GU-major Cartesian rows with the same effective Selector declarations."""
    return [(gu, gu_ref, selector, selector_ref)
            for gu, gu_ref in zip(batch['unlearnings'], batch.get('unlearning_refs', []))
            for selector, selector_ref in selector_entries(batch)]


def configuration_fingerprint(path):
    """Bind all reviewed YAML text, separately from computational cache keys."""
    import hashlib
    import json
    path = Path(path).resolve()
    visited = set()
    def document(current):
        current = current.resolve()
        if current in visited:
            raise ConfigurationError('cyclic configuration references')
        visited.add(current)
        value = read_yaml(current)
        refs = []
        for field in ('dataset_refs', 'selector_refs', 'unlearning_refs', 'evaluation_refs'):
            refs.extend(resolve_reference(field, ref, current.parent) for ref in value.get(field, []))
        if 'parameter_profile_ref' in value:
            refs.append(resolve_parameter_profile_ref(value['parameter_profile_ref'], current.parent))
        children = [document(ref) for ref in refs]
        visited.remove(current)
        return {'document': value, 'references': children}
    return hashlib.sha256(json.dumps(document(path), sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def dataset_binding(config, index):
    """Presentation coordinates never enter computational cache identities."""
    from cache_v2 import canonical_sha256
    dataset = config['datasets'][index]
    return {'dataset_index': index, 'dataset_name': dataset['dataset']['name'],
            'dataset_fingerprint': canonical_sha256(dataset)}

