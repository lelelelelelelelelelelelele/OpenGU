"""Validate or execute one ordinary experiment YAML, directly or through Core."""
from __future__ import annotations
import argparse
import contextlib
import json
from pathlib import Path
import sys
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main(argv=None, *, notify=None):
    # The command's JSON and diagnostic streams use the same encoding on Windows and SSH.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--verification-root', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--device', help='explicit native device: cpu, cuda, or cuda:N')
    parser.add_argument('--syncmate', action='store_true', help='enable the optional SyncMate adapter')
    parser.add_argument('--device-config', type=Path, help='SyncMate device file; requires --syncmate')
    args = parser.parse_args(argv)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            from experiments.modular_run import execute
            if args.dry_run:
                if any((args.verification_root, args.run_id, args.device,
                        args.syncmate, args.device_config, notify is not None)):
                    raise ValueError('dry-run has no execution context')
                result = execute(args.config, dry_run=True)
            else:
                if args.run_id is None:
                    raise ValueError('execution requires --run-id')
                from experiments.modular_config import load_experiment, configuration_fingerprint
                config = load_experiment(args.config)
                if args.syncmate:
                    if args.device is not None or notify is not None:
                        raise ValueError('--syncmate owns its device and notification callback')
                    from scripts.syncmate.opengu_execution import device_context, make_notify
                    context = device_context(config['experiment_id'], run_id=args.run_id,
                        device_file=args.device_config or ROOT / '.syncmate/device.yaml',
                        verification_root=args.verification_root)
                    notify = make_notify(config, context, config_path=args.config)
                else:
                    if args.device_config is not None:
                        raise ValueError('--device-config requires --syncmate')
                    from experiments.modular_execution import native_context
                    context = native_context(config['experiment_id'], run_id=args.run_id,
                        request_device=args.device, verification_root=args.verification_root)
                if args.verification_root:
                    import torch
                    torch.set_num_threads(1)
                from scripts.evaluation.reporting.events import (
                    artifact_ref, make_cell_id, new_run_id, prior_attempt_context, record_event,
                )
                from utils.target_checkpoint import sha256_file
                # A YAML invocation owns a run lifecycle; its matrix cells remain
                # in the existing summary, not fabricated model/method coordinates.
                identity = {'scope': 'experiment', 'experiment_id': config['experiment_id'],
                    'dataset': ','.join(d['dataset']['name'] for d in config['datasets']), 'execution_stage': config['stage']}
                journal = context.runtime_root.parent / '_journal'
                event_path = journal / 'auto_report.events.jsonl'
                cell_id = make_cell_id(identity)
                fingerprint = configuration_fingerprint(args.config)
                attempt, _ = prior_attempt_context(cell_id, fingerprint, event_path)
                event = dict(identity=identity, stage='run', producer='experiments.run',
                    config_fingerprint=fingerprint, git_sha=context.source_git_sha,
                    cell_id=cell_id, run_id=new_run_id(cell_id), attempt=attempt,
                    metadata={'execution_run_id': context.run_id, 'level': context.level,
                              'config_path': str(args.config.resolve())},
                    event_path=event_path, status_md_path=journal / 'auto_report.md',
                    status_html_path=journal / 'auto_report.html')
                started = perf_counter()
                record_event(state='started', **event)
                from experiments.modular_artifacts import generated_paths
                try:
                    result = execute(args.config, context=context, notify=notify)
                    result.update(passed=True, generated_artifacts=generated_paths(result, context))
                except BaseException as exc:
                    event['metadata'].update(wall_seconds=perf_counter()-started,
                        **getattr(exc, 'execution_timing', {}))
                    try:
                        record_event(state='failed', error={'type': type(exc).__name__,
                                                           'message': str(exc) or type(exc).__name__}, **event)
                    except Exception as report_error:
                        print('AutoReport failed to record failure: {}'.format(report_error), file=sys.stderr)
                    raise
                event['metadata'].update(wall_seconds=perf_counter()-started, **result.get('execution_timing', {}))
                record_event(state='completed', artifacts=[artifact_ref(path=context.output,
                    artifact_type='opengu.modular_run', content_hash=sha256_file(context.output))], **event)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 1 if result.get('passed') is False else 0
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
