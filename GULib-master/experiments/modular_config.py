"""One experiment table references independent, fully resolved module instances."""
from __future__ import annotations

import copy
import math
from pathlib import Path
from experiments.effective_config import read_yaml, fields, effective, choice, ConfigurationError
from experiments.target_direct_v1.methods import resolve_parameters, uses_model, SCORE_NAMES

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIRECTORIES = {
    'dataset_ref': 'datasets',
    'selector_refs': 'selectors',
    'unlearning_refs': 'unlearning',
    'evaluation_refs': 'evaluations',
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


def model_training(value):
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
    if model['layers'] != default['layers'] or model['hidden_channels'] <= 0 or model['dropout'] != default['dropout']:
        raise ConfigurationError('model shape/dropout is outside the supported OpenGU implementation')
    if architecture == 'OpenGU.SGCNet' and model['hidden_channels'] != 64:
        raise ConfigurationError('OpenGU SGC has no hidden_channels override')
    props = read_yaml(ROOT / 'model/properties' / ('GCN.yaml' if architecture.endswith('GCNNet') else 'SGC.yaml'))
    training = effective(value.get('training', {}), {'epochs': 100, 'optimizer': 'Adam', 'lr': float(props['lr']),
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
    choice(value['method'], SCORE_NAMES, 'selector method')
    if value['candidate'] != {'pool': 'train_mask'}:
        raise ConfigurationError('candidate pool must explicitly reference persisted train_mask')
    result = {key: value[key] for key in ('kind', 'schema_version', 'method', 'candidate', 'budget')}
    result['parameters'] = resolve_parameters(value['method'], value.get('parameters'))
    result['selection_rule'] = effective(value.get('selection_rule', {}),
        {'direction': 'descending', 'tie_break': 'node_id_ascending'}, 'selection_rule')
    if result['selection_rule'] != {'direction': 'descending', 'tie_break': 'node_id_ascending'}:
        raise ConfigurationError('only score_desc_node_id_asc is implemented')
    result['numerics'] = effective(value.get('numerics', {}), {'dtype': 'float32'}, 'numerics')
    choice(result['numerics']['dtype'], ('float32',), 'dtype')
    if uses_model(value['method']):
        result['model'], result['training'] = model_training({k: value[k] for k in ('model', 'training') if k in value})
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
    if method == 'GNNDelete':
        result = {k: defaults[k] for k in ('unlearn_lr', 'unlearning_epochs', 'alpha', 'loss_fct', 'loss_type')}
        result.update(deletion_optimizer='Adam', deletion_weight_decay=0.0)
        return result
    if method == 'GIF':
        return {k: defaults[k] for k in ('iteration', 'scale', 'damp', 'GIF_method')}
    raise ConfigurationError('supported GU methods: GNNDelete, GIF, Retrain')


def unlearning(value):
    fields(value, {'kind', 'schema_version', 'method', 'model', 'training', 'parameters', 'checkpoint', 'deletion'},
                  {'kind', 'schema_version', 'method'}, 'unlearning')
    params = effective(value.get('parameters', {}), gu_defaults(value['method']))
    if value['method'] == 'GNNDelete':
        if (params['unlearn_lr'] <= 0 or params['unlearning_epochs'] <= 0 or not 0 <= params['alpha'] <= 1
                or params['deletion_optimizer'] != 'Adam' or params['deletion_weight_decay'] != 0
                or params['loss_type'] != 'both_layerwise' or params['loss_fct'] != 'mse_mean'):
            raise ConfigurationError('invalid or unsupported GNNDelete node configuration')
    elif value['method'] == 'GIF':
        if params['iteration'] <= 0 or params['scale'] <= 0 or not 0 <= params['damp'] < 1:
            raise ConfigurationError('invalid GIF parameters')
        choice(params['GIF_method'], ('GIF', 'IF'), 'GIF_method')
    model, training = model_training({k: value[k] for k in ('model', 'training') if k in value})
    if value['method'] == 'GNNDelete' and model['architecture'] != 'OpenGU.GCNNet':
        raise ConfigurationError('GNNDelete modular node consumer currently supports GCN')
    if value['method'] == 'Retrain' and 'checkpoint' in value:
        raise ConfigurationError('Retrain starts from scratch and cannot consume a checkpoint')
    from experiments.node_deletion import resolve_deletion
    return {**value, 'model': model, 'training': training, 'parameters': params,
            'deletion': resolve_deletion(value.get('deletion'))}


def load_instance(path, expected_kind):
    value = read_yaml(path)
    if value.get('kind') != expected_kind or type(value.get('schema_version')) is not int or value.get('schema_version') != 1:
        raise ConfigurationError(f'{path}: expected {expected_kind} schema_version 1')
    if value.get('checkpoint'):
        fields(value['checkpoint'], {'path', 'file_sha256', 'state_hash'},
               {'path', 'file_sha256', 'state_hash'}, 'checkpoint')
        if any(not isinstance(v, str) or not v for v in value['checkpoint'].values()):
            raise ConfigurationError('checkpoint needs nonempty path and exact hashes')
        value['checkpoint'] = dict(value['checkpoint'])
        if 'path' in value['checkpoint']:
            value['checkpoint']['path'] = str((Path(path).resolve().parent / value['checkpoint']['path']).resolve())
    if expected_kind == 'selector':
        return selector(value)
    if expected_kind == 'unlearning':
        return unlearning(value)
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


def configuration_sources(path, resolved):
    """Per-field provenance is recorded outside all computational identities."""
    original = read_yaml(path)
    sources = {}
    def visit(value, supplied, prefix=''):
        for key, item in value.items():
            name = prefix + key
            if isinstance(item, dict):
                visit(item, supplied.get(key, {}), name + '.')
            elif key in supplied:
                sources[name] = 'instance:' + str(Path(path).resolve())
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
    required = {'kind', 'schema_version', 'experiment_id', 'stage', 'dataset_ref', 'matrix'}
    fields(value, required | {'round',
        'selector_refs', 'unlearning_refs', 'evaluation_refs', 'case_id', 'output_inputs',
        'seeds', 'budget_ratios'},
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
    result = dict(value)
    dataset_path = resolve_reference('dataset_ref', value['dataset_ref'], path.parent)
    result['dataset'] = load_instance(dataset_path, 'dataset_split')
    result['dataset_directory'] = str(dataset_path.parent)
    result['configuration_sources'] = {
        'dataset': str(dataset_path), 'selectors': [], 'unlearnings': [], 'evaluations': []}
    for field, kind in (('selector_refs', 'selector'), ('unlearning_refs', 'unlearning'),
                        ('evaluation_refs', 'evaluation')):
        refs = value.get(field, [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ConfigurationError(f'{field} must be a list of file references')
        paths = [resolve_reference(field, ref, path.parent) for ref in refs]
        result[kind + 's'] = [load_instance(ref_path, kind) for ref_path in paths]
        result['configuration_sources'][kind + 's'] = [configuration_sources(ref_path, item)
            for ref_path, item in zip(paths, result[kind + 's'])]
    result['source_directory'] = str(path.parent)
    # Validate matrix axes while parsing, including during the ordinary dry-run.
    validate_repeats(result)
    return result


def validate_repeats(config):
    """Two explicit experimental axes, not arbitrary module-parameter overrides."""
    for field in ('seeds', 'budget_ratios'):
        if field not in config:
            continue
        values = config[field]
        if config['stage'] == 'metrics':
            raise ConfigurationError('metrics consumes fixed outputs and cannot declare repeat axes')
        if not isinstance(values, list) or not values:
            raise ConfigurationError(field + ' must be a nonempty list')
        for value in values:
            valid = (type(value) is int and value >= 0) if field == 'seeds' else (
                type(value) in (int, float) and math.isfinite(value) and 0 < value <= 1)
            if not valid:
                raise ConfigurationError('invalid ' + field + ' value')
        if len(set(values)) != len(values):
            raise ConfigurationError(field + ' must not contain duplicates')
    if 'budget_ratios' in config:
        if not config['selectors'] or any(s['budget']['mode'] != 'ratio' for s in config['selectors']):
            raise ConfigurationError('budget_ratios requires ratio-based selector refs')
    if 'seeds' in config:
        models = [s for s in config['selectors'] if uses_model(s['method'])] + config['unlearnings']
        if not models:
            raise ConfigurationError('seeds requires a model training consumer')
        if any('checkpoint' in instance for instance in models):
            raise ConfigurationError('seeds cannot relabel an explicit checkpoint; use separate instances')


def experiment_batches(config):
    """Resolve paired training repetitions in memory; never write leaf YAML.

    Within a batch, Selector x Unlearning remains the existing Cartesian product.
    Training seeds are paired across the two model consumers, not crossed.
    """
    for seed in config.get('seeds', [None]):
        for ratio in config.get('budget_ratios', [None]):
            batch = copy.deepcopy(config)
            batch['matrix_values'] = {'training_seed': seed, 'budget_ratio': ratio}
            for kind in ('selector', 'unlearning'):
                for index, instance in enumerate(batch[kind + 's']):
                    sources = batch['configuration_sources'][kind + 's'][index]
                    if seed is not None and 'training' in instance:
                        instance['training']['seed'] = seed
                        sources['training.seed'] = 'experiment:seeds'
                    if kind == 'selector' and ratio is not None:
                        instance['budget']['value'] = float(ratio)
                        sources['budget.value'] = 'experiment:budget_ratios'
            yield batch


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
        refs = ([resolve_reference('dataset_ref', value['dataset_ref'], current.parent)] if 'dataset_ref' in value else [])
        for field in ('selector_refs', 'unlearning_refs', 'evaluation_refs'):
            refs.extend(resolve_reference(field, ref, current.parent) for ref in value.get(field, []))
        children = [document(ref) for ref in refs]
        visited.remove(current)
        return {'document': value, 'references': children}
    return hashlib.sha256(json.dumps(document(path), sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()
