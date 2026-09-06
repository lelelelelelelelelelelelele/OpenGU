"""Verify collected portable outputs; human research acceptance stays separate."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

REVIEWED_PROFILES = {'modular-output-v1'}

def _now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_project_path(project_root: Path, value: Any) -> Path | None:
    text = str(value or "").replace("\\", "/")
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        return None
    root = project_root.resolve()
    candidate = (root / Path(*path.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _peer_evidence(
    definition: Mapping[str, Any],
    context: Mapping[str, Any],
    label: str,
) -> tuple[dict[str, Any], list[str], list[str], dict[str, Mapping[str, Any]], str | None]:
    node_id = str(context.get("node_id") or "")
    index = context.get("artifact_index") or {}
    peer = ((index.get("peers") or {}).get(node_id) or {}) if isinstance(index, Mapping) else {}
    errors: list[str] = []
    expected_paths = list(definition.get("expected_artifact_paths") or [])
    expected = set(expected_paths)
    # Core binds this recipe's paths to the submission handoff. The peer index
    # also retains other runs; only this delivery participates in acceptance.
    items = [
        item for item in (peer.get("items") or [])
        if isinstance(item, Mapping)
        and str(item.get("remote_path") or item.get("path") or "") in expected
    ]
    by_remote = {
        str(item.get("remote_path") or item.get("path")): item
        for item in items
    }
    if len(by_remote) != len(items):
        errors.append(f"{label} delivery artifact index contains duplicate paths")
    if (peer.get("summary") or {}).get("status") != "verified":
        errors.append(f"{label} artifact index is not verified")
    if set(by_remote) != expected:
        errors.append(f"verified {label} artifact set differs from the reviewed recipe")
    observed_sha = ((peer.get("remote") or {}).get("git") or {}).get("sha")
    expected_sha = context.get("expected_git_sha")
    if expected_sha and observed_sha != expected_sha:
        errors.append(f"verified {label} artifact Git SHA differs from the dispatched SHA")
    return peer, errors, expected_paths, by_remote, observed_sha


def acceptance_payload(profile, definition, context):
    errors = []
    cells = []
    if profile not in REVIEWED_PROFILES:
        errors.append('OpenGU acceptance profile is not reviewed')
    else:
        _, errors, expected_paths, by_remote, observed_sha = _peer_evidence(definition, context, 'modular')
        root = Path(context['project_root']).resolve()
        try:
            for remote, entry in by_remote.items():
                path = _safe_project_path(root, entry.get('local_path'))
                if path is None or _sha256(path) != entry['sha256']:
                    raise ValueError('collected checksum mismatch: ' + remote)
            summary_remote = next(p for p in expected_paths if p.endswith('/summary.json'))
            entry = by_remote[summary_remote]
            from experiments.modular_artifacts import read_summary_outputs
            summary, outputs = read_summary_outputs(root / entry['local_path'], entry['sha256'])
            if summary['configuration_fingerprint'] != definition['configuration_fingerprint']:
                raise ValueError('summary differs from registered effective configuration')
            if summary['logical_cells'] != definition['logical_cells']:
                raise ValueError('collected logical count differs from registration')
            execution = summary['execution_receipt']
            if (execution.get('source_git_sha') != context['expected_git_sha']
                    or execution['run_id'] != definition['run_identity']['run_id']
                    or summary['experiment_id'] != definition['run_identity']['experiment_id']):
                raise ValueError('collected execution identity mismatch')
            from experiments.modular_config import load_experiment, experiment_batches, resolve_budget, selector_entries, unlearning_entries
            config = load_experiment(root / definition['config_path'])
            from experiments.modular_config import configuration_fingerprint
            if configuration_fingerprint(root / definition['config_path']) != definition['configuration_fingerprint']:
                raise ValueError('collector reviewed configuration changed')
            if summary['dataset'] != config['dataset']:
                raise ValueError('summary Dataset/Split differs from configuration')
            stage = config['stage']
            if stage not in ('selector', 'unlearning', 'metrics') or summary['stage'] != stage or definition['stage'] != stage:
                raise ValueError('collected stage differs from registration or configuration')
            if summary['data_identity']['split_hash'] != config['dataset']['artifacts']['split_hash']:
                raise ValueError('summary Split identity differs from configuration')
            batches = list(experiment_batches(config))
            expected = [(batch, gu, selector, selector_ref, gu_ref)
                        for batch in batches
                        for gu, gu_ref, selector, selector_ref in unlearning_entries(batch)]
            if len(expected) != len(outputs):
                raise ValueError('collected rows differ from ordinary matrix expansion')
            selector_rows = summary['selectors']
            expected_selectors = [(batch, selector, ref) for batch in batches
                                  for selector, ref in selector_entries(batch)]
            logical_cells = (sum(len(batch['output_inputs']) for batch in batches) if stage == 'metrics'
                             else len(expected) if stage == 'unlearning' else len(expected_selectors))
            if logical_cells != definition['logical_cells']:
                raise ValueError('registered logical count differs from ordinary matrix expansion')
            if stage != 'unlearning' and (outputs or summary['unlearning']):
                raise ValueError('non-Unlearning stage contains method outputs')
            if stage == 'selector' and summary['evaluations']:
                raise ValueError('Selector stage contains evaluations')
            if len(selector_rows) != len(expected_selectors):
                raise ValueError('collected Selector row count mismatch')
            for (batch, selector, ref), row in zip(expected_selectors, selector_rows):
                score = row['score']['recipe']['fields']
                if (row['matrix_values'] != batch['matrix_values'] or row['selector_ref'] != ref
                        or row['selection']['strategy'] != selector['method']
                        or score['score_names'] != [selector['method']]
                        or score['parameters'] != selector['parameters']
                        or score['data_identity'] != summary['data_identity']
                        or score.get('training') != selector.get('training')
                        or score.get('selector_model') != selector.get('model')):
                    raise ValueError('Selector differs from the effective configuration')
                if stage == 'selector':
                    k = resolve_budget(selector['budget'], definition['expected_dataset']['candidate_count'])['k']
                    nodes = row['selection']['views'][str(k)]['selected_nodes']
                    if len(nodes) != k or len(set(nodes)) != k:
                        raise ValueError('Selector view differs from the effective budget')
                    cells.append({'selector_ref': ref, 'matrix_values': batch['matrix_values'],
                                  'selection': row['selection']['artifact']})
            if stage == 'metrics':
                from cache_v2 import canonical_sha256
                evaluations = summary['evaluations']
                if len(evaluations) != len(config['evaluations']):
                    raise ValueError('collected Evaluation count differs from configuration')
                for instance, evaluation in zip(config['evaluations'], evaluations):
                    if evaluation['effective_config'] != instance or not evaluation['rows']:
                        raise ValueError('Metrics differs from the effective evaluation configuration')
                    # One input summary can supply multiple evaluated outputs.
                    for row in evaluation['rows']:
                        identity = row['identity']
                        if (identity['case'] != instance['case']
                                or identity['metrics'] != sorted(instance['metrics'])
                                or identity['producer_version'] != instance['producer_version']
                                or set(row['metrics']) != set(instance['metrics'])
                                or row['evaluation_receipt_id'] != 'evalr_' + canonical_sha256(identity)[:32]):
                            raise ValueError('Metrics receipt differs from the effective evaluation')
                        cells.append({'evaluation': row})
            for index, ((batch, gu, selector, selector_ref, gu_ref), output) in enumerate(zip(expected, outputs)):
                identity = output['payload'].identity
                row = summary['unlearning'][index]
                selected = next(item for item in selector_rows
                                if item['matrix_values'] == batch['matrix_values'] and item['selector_ref'] == selector_ref)
                k = resolve_budget(selector['budget'], definition['expected_dataset']['candidate_count'])['k']
                if (row['matrix_values'] != batch['matrix_values'] or row['selector_ref'] != selector_ref
                        or row['unlearning_ref'] != gu_ref
                        or identity['pairing']['data_identity'] != summary['data_identity']
                        or summary['data_identity']['split_hash'] != config['dataset']['artifacts']['split_hash']
                        or len(output['payload'].arrays['y']) != definition['expected_dataset']['num_nodes']
                        or int(output['payload'].arrays['train_mask'].sum()) != definition['expected_dataset']['candidate_count']
                        or len(output['payload'].arrays['selected_nodes']) != k
                        or identity['selection'] != {key: selected['selection']['artifact'][key]
                            for key in ('artifact_id','recipe_hash','content_hash')}
                        or output['payload'].arrays['selected_nodes'].tolist() != selected['selection']['views'][str(k)]['selected_nodes']):
                    raise ValueError('output Dataset/Split, Selector or budget binding mismatch')
                for name, artifact in row['collected_artifacts'].items():
                    remote = str(PurePosixPath(summary_remote).parent / (PurePosixPath(summary_remote).stem + '.outputs') / str(index) / name)
                    collected = by_remote[remote]
                    actual = (root / entry['local_path']).parent / artifact['path']
                    if (actual.resolve() != (root / collected['local_path']).resolve()
                            or artifact['sha256'] != collected['sha256']):
                        raise ValueError('summary output is outside the verified collected set')
                if (identity['target']['method'] != gu['method']
                        or identity['target']['parameters'] != gu['parameters']
                        or identity['pairing']['model'] != gu['model']
                        or identity['pairing']['training'] != gu['training']
                        or identity['pairing']['deletion'] != gu['deletion']):
                    raise ValueError('output differs from the effective method configuration')
                cells.append({'method': gu['method'], 'seed': gu['training']['seed'],
                    'output': output['output'], 'evaluation': output['evaluation'],
                    'selection': identity['selection']})
        except (ValueError, KeyError, TypeError, OSError, StopIteration) as exc:
            errors.append(str(exc))
    passed = not errors
    return {'owner': 'opengu', 'profile': profile, 'passed': passed,
            'status': 'accepted' if passed else 'rejected', 'errors': errors,
            'accepted_cells': len(cells), 'cells': cells,
            'scientific_acceptance': 'not_evaluated', 'generated_at': _now_iso()}
