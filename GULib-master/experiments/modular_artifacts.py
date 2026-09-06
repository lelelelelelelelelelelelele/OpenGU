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
    outputs = []
    for row in summary['unlearning']:
        artifacts = {name: {'local_path': item['path'], 'sha256': item['sha256']}
                     for name, item in row['collected_artifacts'].items()}
        result = read_method_output(artifacts, path.parent)
        if result['output'] != row['output']:
            raise ValueError('summary output differs from collected payload')
        if result['meta']['config_fingerprint'] != summary['configuration_fingerprint']:
            raise ValueError('collected configuration fingerprint mismatch')
        if result['meta']['execution_receipt'] != summary['execution_receipt']:
            raise ValueError('collected execution receipt mismatch')
        outputs.append(result)
    return summary, outputs
