"""Read-only EXP-084 checkpoint-selection audit; emit one JSON document to stdout.

Run after the runner is idle, with explicit run/checksum and producer identities.
For a main-run HIT, --generation-run must identify a native MISS run with the
exact same Output and conditions. No checkpoint is inferred from a HIT alone.
Model payloads remain remote; stdout contains identities and scalar metadata.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import numbers
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def contained(root, path):
    path = (root / path).resolve() if not path.is_absolute() else path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError('input path is outside the explicit repository') from exc
    return path


def audit(args):
    root = args.repo_root.resolve()
    sys.path.insert(0, str(root))
    require(re.fullmatch('[0-9a-f]{40}', args.expected_commit), 'expected commit must be a full lowercase SHA')
    require(re.fullmatch('[0-9a-f]{64}', args.expected_source), 'expected producer source must be SHA-256')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    require(head == args.expected_commit, 'audit checkout differs from the frozen run commit')

    import numpy as np
    import torch
    from cache_v2 import ArtifactRecipe
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_output_payload
    from experiments.modular_model import runtime_defaults
    runtime_defaults()  # Isolate OpenGU's import-time argument parser.
    from experiments.modular_gu import gu_producer
    from experiments.implementation_identity import fingerprint_session
    from utils.target_checkpoint import state_hash

    store = root / 'results/cache_v2'
    index_path = store / 'index.sqlite'
    index_before = digest(index_path.read_bytes())

    def read_bound_run(path, expected_hash):
        require(re.fullmatch('[0-9a-f]{64}', expected_hash), 'run checksum must be SHA-256')
        path = contained(root, Path(path))
        run, documents = read_run(path, expected_hash)
        require(run['commit'] == args.expected_commit, 'run commit differs from the frozen commit')
        require(run['experiment_id'] == args.experiment_id, 'unexpected experiment identity')
        require(run['stage'] == 'unlearning', 'checkpoint audit requires an unlearning run')
        expected_path = root / 'results/runs' / run['experiment_id'] / run['run_id'] / 'run.json'
        require(path == expected_path, 'run path differs from the ordinary executor layout')
        return dict(path=path.relative_to(root).as_posix(), sha256=expected_hash,
                    run=run, documents=documents)

    target = read_bound_run(args.run, args.run_sha256)
    sources = [read_bound_run(path, sha) for path, sha in args.generation_run]
    require(len({s['path'] for s in sources}) == len(sources), 'duplicate generation run')
    require(target['path'] not in {s['path'] for s in sources}, 'target run cannot be its own generation-run input')

    rows = []
    checkpoint_hashes = {}
    with fingerprint_session():
        for cell, document in zip(target['run']['cells'], target['documents']):
            if cell['conditions']['method'] != 'GNNDelete':
                continue
            reference = cell['output']
            require(set(reference) == {'artifact_id', 'recipe_hash', 'content_hash'},
                    'audit requires an exact Cache V2 Output reference')
            cache_state = cell['cache']['method']
            if cache_state == 'miss':
                require(cell['producer_called']['method'] is True, 'MISS lacks native producer execution')
                native, native_cell, native_document = target, cell, document
            else:
                require(cache_state == 'hit' and cell['producer_called']['method'] is False,
                        'unsupported or inconsistent method cache state')
                require(not args.require_all_miss, 'technical gate unexpectedly contains a GNNDelete HIT')
                matches = [(source, c, d) for source in sources
                           for c, d in zip(source['run']['cells'], source['documents'])
                           if c.get('output') == reference and c['conditions'] == cell['conditions']
                           and c.get('cache', {}).get('method') == 'miss'
                           and c.get('producer_called', {}).get('method') is True]
                require(len(matches) == 1, 'HIT has no unique explicitly bound native MISS run')
                native, native_cell, native_document = matches[0]
            require(native_document['selection.json'] == document['selection.json'],
                    'generation and consumption Selection documents differ')

            payload = load_output_payload(reference, store, dataset_root=root)
            identity = payload.identity
            producer = identity['producer_version']
            require(identity['target']['method'] == 'GNNDelete', 'Output is not GNNDelete')
            require(producer['source_fingerprint'] == args.expected_source, 'Output producer is not the reviewed repair')
            require(gu_producer('GNNDelete', identity['pairing']['model']).to_dict() == producer,
                    'installed producer differs from Output producer')
            require(ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity}).recipe_hash == reference['recipe_hash'],
                    'Output identity differs from the cell recipe')
            require(identity['selection']['artifact_id'] == cell['selection_id'] == document['selection.json']['selection_id'],
                    'Output Selection identity differs from cell')
            require(identity['pairing']['selected_nodes'] == document['selection.json']['selected_nodes'],
                    'Output ordered request differs from cell')
            require(identity['pairing']['training']['seed'] == cell['conditions']['seed'],
                    'Output seed differs from cell')
            require(identity['pairing']['model']['architecture'] == cell['conditions']['model'],
                    'Output model differs from cell')
            for checked_cell in (cell, native_cell):
                provenance = checked_cell['cache_provenance']
                require(provenance.get('generation_producer') == producer,
                        'run generation producer differs from exact Output')
                require(provenance.get('consumption_producer') == producer,
                        'run consumption producer differs from exact Output')

            checkpoint_path = contained(root, Path('results/runtime/modular') / native['run']['run_id'] /
                                        'unlearning' / reference['recipe_hash'] / 'model_best.pt')
            checkpoint_bytes = checkpoint_path.read_bytes()  # Missing runtime is a hard failure.
            checkpoint_sha = digest(checkpoint_bytes)
            checkpoint_hashes[checkpoint_path] = checkpoint_sha
            # This is the exact owned runtime of the checksum-bound native MISS,
            # not an arbitrary uploaded checkpoint. sklearn's selection score
            # is a NumPy scalar, unsupported by torch 2.2's weights-only reader.
            checkpoint = torch.load(io.BytesIO(checkpoint_bytes), map_location='cpu', weights_only=False)
            require(set(checkpoint) == {'model_state', 'epoch', 'selection_stage', 'selection_metric', 'selection_score'},
                    'checkpoint selection metadata is missing or unexpected')
            epoch, score = checkpoint['epoch'], checkpoint['selection_score']
            epochs = identity['target']['parameters']['unlearning_epochs']
            require(type(epoch) is int and 0 <= epoch < epochs, 'selected epoch is outside declared training range')
            require(checkpoint['selection_stage'] == 'val', 'checkpoint was not selected on validation')
            require(checkpoint['selection_metric'] == 'accuracy+micro_f1', 'checkpoint selection metric drifted')
            require(isinstance(score, numbers.Real) and not isinstance(score, bool)
                    and math.isfinite(score) and 0 <= score <= 2,
                    'invalid checkpoint validation selection score')
            score = float(score)
            state = checkpoint['model_state']
            require(set(state) == set(payload.state), 'checkpoint and Output state keys differ')
            for name, tensor in state.items():
                require(isinstance(tensor, torch.Tensor), 'checkpoint state contains a non-tensor')
                array = tensor.detach().cpu().numpy()
                stored = payload.state[name]
                require(array.dtype == stored.dtype and array.shape == stored.shape,
                        'checkpoint and Output tensor type/shape differ: ' + name)
                require(np.isfinite(array).all() and np.array_equal(array, stored),
                        'checkpoint and Output weights differ or are nonfinite: ' + name)

            rows.append(dict(cell_id=cell['cell_id'], conditions=cell['conditions'], output=reference,
                selection_id=cell['selection_id'], initial_checkpoint_state_hash=identity['target']['checkpoint_state_hash'],
                producer=producer, consumption_cache_state=cache_state,
                generation_run=dict(path=native['path'], sha256=native['sha256'],
                                    run_id=native['run']['run_id'], cell_id=native_cell['cell_id']),
                checkpoint=dict(path=checkpoint_path.relative_to(root).as_posix(), sha256=checkpoint_sha,
                                epoch_zero_based=epoch, selection_stage=checkpoint['selection_stage'],
                                selection_metric=checkpoint['selection_metric'], selection_score=score,
                                model_state_hash=state_hash(state), tensor_count=len(state),
                                exported_output_weights_exact=True)))

    require(len(rows) == args.expected_gnndelete_cells > 0, 'GNNDelete audit count differs from frozen expectation')
    require(digest(index_path.read_bytes()) == index_before, 'cache index changed during the read-only audit; require idle runner')
    for path, expected in checkpoint_hashes.items():
        require(digest(path.read_bytes()) == expected, 'runtime checkpoint changed during audit')
    return dict(status='passed', scope='checkpoint-selection provenance and exact exported weights only; no scientific acceptance',
        read_only=True, producer_calls=0, audit_script_sha256=digest(Path(__file__).read_bytes()),
        audit_checkout_commit=head, expected_source=args.expected_source,
        target_run=dict(path=target['path'], sha256=target['sha256'], run_id=target['run']['run_id']),
        generation_runs=[dict(path=s['path'], sha256=s['sha256'], run_id=s['run']['run_id']) for s in sources],
        index_sha256=index_before, index_unchanged=True, audited_cells=len(rows), rows=rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--run-sha256', required=True)
    parser.add_argument('--expected-commit', required=True)
    parser.add_argument('--expected-source', required=True)
    parser.add_argument('--expected-gnndelete-cells', type=int, required=True)
    parser.add_argument('--experiment-id', default='exp084-gnndelete-checkpoint-audit')
    parser.add_argument('--require-all-miss', action='store_true')
    parser.add_argument('--generation-run', nargs=2, action='append', default=[], metavar=('PATH', 'SHA256'))
    args = parser.parse_args(argv)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            result = audit(args)
    except Exception as exc:
        print(json.dumps(dict(status='failed', error_type=type(exc).__name__, error=str(exc),
                              read_only=True, scientific_acceptance='not_evaluated'), ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
