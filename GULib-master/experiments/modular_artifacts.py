"""Portable method outputs for the normal SyncMate checksum/collection chain."""
from pathlib import Path
import hashlib
import json

ARTIFACT_NAMES = ('attack.json', 'output-references.json', 'predictions.npz', '_meta.json')


def generated_paths(summary, context):
    """Files actually exported by this stage, relative to its execution workspace."""
    root = context.store_root.parent.parent
    return [context.output.relative_to(root).as_posix()] + [
        (context.output.parent / item['path']).relative_to(root).as_posix()
        for row in summary['unlearning'] for item in row['collected_artifacts'].values()]


def output_paths(summary_path, count):
    parent = Path(summary_path).parent / (Path(summary_path).stem + '.outputs')
    return tuple((parent / str(i) / name).as_posix()
                 for i in range(count) for name in ARTIFACT_NAMES)


def save_method_result(row, *, store_root, output_dir, strategy, meta):
    """Export the same verified payload that the independent method cached."""
    from experiments.unlearning_outputs import load_output
    payload = load_output(row['output'], store_root)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {**row['result'], 'failed': False,
              'selected_nodes': payload.arrays['selected_nodes'].tolist(),
              'output': row['output'], 'evaluation': row['evaluation'],
              'producer_called': row['producer_called'], 'cache_hit': row['hit'],
              'compute_seconds': row['compute_seconds']}
    documents = {'attack.json': {'results': {strategy: result}},
                 'output-references.json': {'strategy': strategy, 'output': row['output']},
                 '_meta.json': {**meta, 'output_reference': row['output'],
                               'evaluation_receipt_id': row['evaluation']['evaluation_receipt_id']}}
    for name, value in documents.items():
        with (output_dir / name).open('x', encoding='utf-8') as handle:
            json.dump(value, handle, indent=2, allow_nan=False)
    with (output_dir / 'predictions.npz').open('xb') as handle:
        handle.write(payload.canonical_bytes)


def export_outputs(summary, *, output, store_root):
    for index, row in enumerate(summary['unlearning']):
        from experiments.unlearning_outputs import load_output
        payload = load_output(row['output'], store_root)
        folder = output.parent / (output.stem + '.outputs') / str(index)
        strategy = row.get('selector_ref') or 'bound-selection'
        save_method_result(row, store_root=store_root, output_dir=folder,
            strategy=strategy, meta={'method': payload.identity['target']['method'],
                'strategy': strategy, 'seed': payload.identity['pairing']['training']['seed'],
                'selection_artifact': payload.identity['selection'],
                'matrix_values': row['matrix_values'],
                'dataset': summary['datasets'][row['matrix_values']['dataset_index']],
                'config_fingerprint': summary['configuration_fingerprint'],
                'git_sha': summary['execution_receipt']['source_git_sha'],
                'execution_receipt': summary['execution_receipt']})
        row['collected_artifacts'] = {name: {
            'path': (folder / name).relative_to(output.parent).as_posix(),
            'sha256': hashlib.sha256((folder / name).read_bytes()).hexdigest()}
            for name in ARTIFACT_NAMES}


def read_summary_outputs(path, expected_sha256):
    """Verify a collected summary and its portable outputs without a remote Store."""
    from scripts.syncmate.opengu_method_output import read_method_output
    path = Path(path).resolve()
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError('summary checksum mismatch')
    summary = json.loads(path.read_text(encoding='utf-8'))
    if summary.get('schema') != 'opengu.modular_run' or summary.get('version') != 3:
        raise ValueError('expected modular summary version 3')
    outputs = []
    seen = set()
    for index, row in enumerate(summary['unlearning']):
        expected = {(Path(path.stem + '.outputs') / str(index) / name).as_posix() for name in ARTIFACT_NAMES}
        paths = {item['path'] for item in row['collected_artifacts'].values()}
        if (set(row['collected_artifacts']) != set(ARTIFACT_NAMES)
                or len(paths) != len(ARTIFACT_NAMES) or seen & paths or paths != expected):
            raise ValueError('duplicate or invalid summary output paths')
        seen.update(paths)
        artifacts = {name: {'local_path': item['path'], 'sha256': item['sha256']}
                     for name, item in row['collected_artifacts'].items()}
        result = read_method_output(artifacts, path.parent)
        if result['output'] != row['output']:
            raise ValueError('summary output differs from collected payload')
        if result['meta']['config_fingerprint'] != summary['configuration_fingerprint']:
            raise ValueError('collected configuration fingerprint mismatch')
        if result['meta']['execution_receipt'] != summary['execution_receipt']:
            raise ValueError('collected execution receipt mismatch')
        from cache_v2 import canonical_sha256
        binding = row['matrix_values']
        if type(binding['dataset_index']) is not int or not 0 <= binding['dataset_index'] < len(summary['datasets']):
            raise ValueError('invalid collected dataset index')
        dataset = summary['datasets'][binding['dataset_index']]
        if (binding['dataset_name'] != dataset['dataset']['dataset']['name']
                or binding['dataset_fingerprint'] != canonical_sha256(dataset['dataset'])
                or result['meta']['matrix_values'] != binding
                or result['payload'].identity['pairing']['data_identity'] != dataset['data_identity']):
            raise ValueError('collected output Dataset/Split ownership mismatch')
        outputs.append(result)
    return summary, outputs
