"""Collect YAML-bound shared inputs through Core's checksum/index chain."""
import json
from pathlib import Path

from experiments.dataset_inputs import input_path, bind_input, resolve_input
from experiments.modular_config import load_experiment
from utils.target_checkpoint import sha256_file


def collect_inputs(config_path, *, node_id, ssh, repo_path, project_root,
                   python_executable='python', expected_git_sha=None):
    from syncmate_core import collection
    root = Path(project_root).resolve()
    config = load_experiment(config_path)
    phases = []

    def collect_exact(expected):
        names = tuple(sorted({Path(p).name for p in expected}))
        roots = sorted({str(Path(p).parent).replace('\\', '/') for p in expected})
        args = (node_id, ssh, repo_path, roots, '.')
        options = dict(artifact_names=names, python_executable=python_executable,
                       expected_paths=sorted(expected), expected_git_sha=expected_git_sha)
        diff, missing, same, conflicts = collection.collect_diff_payload(*args, **options)
        if conflicts:
            raise ValueError('shared input conflicts with existing formal dependency')
        for item in missing + same:
            if item['sha256'] != expected[item['path']]:
                raise ValueError('runner shared input checksum differs from YAML/manifest')
        result = collection.apply_collect(*args, **options)
        if result.get('errors'):
            raise ValueError('shared input collection failed: ' + str(result['errors']))
        verified = collection.verify_collect(*args, **options)
        if verified['summary']['status'] != 'verified':
            raise ValueError('shared input collection is unverified')
        for relative, digest in expected.items():
            if sha256_file(input_path(root, relative)) != digest:
                raise ValueError('shared input changed during collection')
        phases.append({'fetched': result['summary']['fetched'],
                       'new_bytes': sum(item['size'] for item in missing),
                       'files': expected})

    manifests = {}
    for instance, directory in zip(config['datasets'], config['dataset_directories']):
        path = (Path(directory) / instance['artifacts']['manifest']).resolve()
        relative = path.relative_to(root).as_posix()
        if not relative.startswith('data/processed/'):
            raise ValueError('shared input collection requires formal data/processed paths')
        digest = instance['artifacts']['manifest_sha256']
        if relative in manifests and manifests[relative] != digest:
            raise ValueError('conflicting Dataset manifest bindings')
        manifests[relative] = digest
    collect_exact(manifests)
    graphs = {}
    for relative in manifests:
        path = input_path(root, relative)
        manifest = json.loads(path.read_text(encoding='utf-8'))
        graph = (path.parent / manifest['data_path']).resolve().relative_to(root).as_posix()
        if not graph.startswith('data/processed/'):
            raise ValueError('shared graph must remain in formal data/processed')
        if graph in graphs and graphs[graph] != manifest['data_sha256']:
            raise ValueError('conflicting shared graph bindings')
        graphs[graph] = manifest['data_sha256']
    collect_exact(graphs)
    for instance, directory in zip(config['datasets'], config['dataset_directories']):
        resolve_input(bind_input(instance, directory, root), root)
    return {'verified': True, 'phases': phases}


def main(argv, project_root):
    import argparse
    from syncmate_core import context, devices
    from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('node_id')
    parser.add_argument('--config', required=True)
    args = parser.parse_args(argv)
    with context.use(project_root, extension=OpenGUProjectExtension()):
        device, warnings = devices.load_device(Path(project_root) / '.syncmate/device.yaml')
        if warnings:
            raise ValueError('; '.join(warnings))
        peer = device['peers'][args.node_id]
        result = collect_inputs(Path(project_root) / args.config, node_id=args.node_id,
            ssh=devices.transport_ssh_value(peer), repo_path=peer['repo_path'],
            project_root=project_root, python_executable=peer.get('python_executable', 'python'))
    print(json.dumps(result))
    return 0
