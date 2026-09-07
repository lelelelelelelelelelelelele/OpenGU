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
    errors, cells = [], []
    if profile not in REVIEWED_PROFILES:
        errors.append('OpenGU acceptance profile is not reviewed')
    else:
        _, errors, expected_paths, by_remote, _ = _peer_evidence(definition, context, 'result')
        root = Path(context['project_root']).resolve()
        try:
            from experiments.modular_artifacts import read_run, planned_cells
            from experiments.modular_config import load_experiment, configuration_fingerprint, resolve_budget
            for remote, entry in by_remote.items():
                path = _safe_project_path(root, entry.get('local_path'))
                if path is None or _sha256(path) != entry['sha256']:
                    raise ValueError('collected checksum mismatch: ' + remote)
            run_remote = next(p for p in expected_paths if p.endswith('/run.json'))
            entry = by_remote[run_remote]
            run_path = root / entry['local_path']
            run, documents = read_run(run_path, entry['sha256'])
            if (run['commit'] != context['expected_git_sha'] or run['run_id'] != definition['run_identity']['run_id']
                    or run['experiment_id'] != definition['run_identity']['experiment_id']
                    or run['config_path'] != definition['config_path'] or run['stage'] != definition['stage']):
                raise ValueError('collected execution identity mismatch')
            config_path = root / definition['config_path']
            if configuration_fingerprint(config_path) != definition['configuration_fingerprint']:
                raise ValueError('collector reviewed configuration changed')
            config = load_experiment(config_path)
            expected_cells = (definition['expected_cells'] if config['stage'] == 'metrics' else planned_cells(config))
            if len(run['cells']) != len(expected_cells):
                raise ValueError('collected cell count differs from registration')
            actual_paths = [run_remote]
            for expected, cell, document in zip(expected_cells, run['cells'], documents):
                if any(cell[key] != expected[key] for key in ('cell_id', 'path', 'conditions')):
                    raise ValueError('result cell conditions differ from configured matrix')
                conditions = cell['conditions']
                counts = definition['expected_datasets'][conditions['dataset_index']]
                selection = document['selection.json']
                if (selection['requested_k'] != resolve_budget(conditions['budget'], counts['candidate_count'])['k']
                        or any(n >= counts['num_nodes'] for n in selection['selected_nodes'])):
                    raise ValueError('result selection differs from requested budget or dataset')
                expected_names = {'selection.json'}
                if config['stage'] != 'selector':
                    expected_names.add('metrics.json')
                if config.get('return_scores'):
                    expected_names.add('scores.npz')
                if set(cell['files']) != expected_names:
                    raise ValueError('missing or unexpected declared cell result')
                if 'metrics.json' in document:
                    from experiments.modular_evaluation import CASES
                    expected_metrics = []
                    if config['stage'] == 'unlearning':
                        expected_metrics = [('method', set(CASES['post_method_metrics']['metrics'])),
                            ('utility', {'f1_before', 'f1_after', 'f1_drop', 'f1_drop_ratio'})]
                    expected_metrics += [(e['case'], set(e['metrics'])) for e in config['evaluations']
                        if conditions['method'] != 'Retrain' or e['case'] != 'post_unlearning_utility_and_retrain_gap']
                    measured = document['metrics.json']['rows']
                    if (len(measured) != len(expected_metrics) or any(
                            r['stage'] != stage or set(r['values']) != names
                            for r, (stage, names) in zip(measured, expected_metrics))):
                        raise ValueError('metrics differ from configured measurement stages')
                if 'scores.npz' in document and conditions['selector'] != 'im':
                    if len(document['scores.npz']['candidate_ids']) != counts['candidate_count']:
                        raise ValueError('score coverage differs from registered candidates')
                for name, artifact in cell['files'].items():
                    remote = str(PurePosixPath(run_remote).parent / cell['path'] / name)
                    actual_paths.append(remote)
                    indexed = by_remote[remote]
                    if ((run_path.parent / cell['path'] / name).resolve() != (root / indexed['local_path']).resolve()
                            or artifact['sha256'] != indexed['sha256']):
                        raise ValueError('result is outside verified collected set')
                cells.append({'cell_id': cell['cell_id'], 'conditions': conditions,
                              'selection_id': cell['selection_id']})
            if set(actual_paths) != set(expected_paths) or len(actual_paths) != len(expected_paths):
                raise ValueError('result files differ from exact recipe declaration')
        except (ValueError, KeyError, IndexError, TypeError, OSError, StopIteration) as exc:
            errors.append(str(exc))
    passed = not errors
    return {'owner': 'opengu', 'profile': profile, 'passed': passed,
            'status': 'accepted' if passed else 'rejected', 'errors': errors,
            'accepted_cells': len(cells), 'cells': cells,
            'scientific_acceptance': 'not_evaluated', 'generated_at': _now_iso()}
