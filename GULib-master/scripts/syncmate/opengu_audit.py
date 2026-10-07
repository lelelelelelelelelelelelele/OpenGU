"""Reconcile interrupted audit entries with a trusted local Core terminal job."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.evaluation.reporting.events import read_event_stream, record_event, refresh_status_views


def reconcile(job, definition, execution, terminal, event_path):
    """Consume Core facts; never schedule, retry, or rewrite original events."""
    from syncmate_core.job_status import validate_status
    validate_status(terminal, job_id=job['id'], execution=execution)
    if terminal.get('state') not in ('failed', 'blocked', 'stale') or not terminal.get('finished_at'):
        raise ValueError('a finished unsuccessful Core job is required')
    if execution['git_sha'] != job['expected_git_sha'] or execution['config_sha256'] != definition['config_sha256']:
        raise ValueError('terminal execution binding mismatch')
    if execution['run_identity'] != definition['run_identity'] or execution['recipe'] != job['recipe']:
        raise ValueError('terminal run identity mismatch')
    identity = definition['run_identity']
    events, warnings = read_event_stream(event_path)
    if warnings:
        raise ValueError('untrusted audit stream')
    selected = [e for e in events if e['git_sha'] == job['expected_git_sha']
        and e['config_fingerprint'] == definition['configuration_fingerprint']
        and e['identity'].get('experiment_id') == identity['experiment_id']
        and e['metadata'].get('execution_run_id') == identity['run_id']]
    if not selected:
        raise ValueError('no audit attempt matches the exact Core execution')
    runs = {}
    for e in selected:
        runs[(e['cell_id'], e['run_id'], e['stage'])] = e
    appended = 0
    for e in runs.values():
        if e['state'] != 'started':
            continue
        record_event(identity=e['identity'], stage=e['stage'], state='failed', producer='scripts.syncmate.opengu_audit',
            config_fingerprint=e['config_fingerprint'], git_sha=e['git_sha'], cell_id=e['cell_id'],
            run_id=e['run_id'], attempt=e['attempt'], metadata={**e['metadata'], 'terminal_source': terminal,
                'timing_semantics': 'interrupted; wall/unfinished phase duration unknown'},
            error={'type': terminal.get('error_code') or 'CORE_TERMINAL',
                   'message': 'Core reports {} for {}'.format(terminal['state'], job['id'])},
            event_path=event_path, refresh=False)
        appended += 1
    refresh_status_views(event_path=event_path)
    return appended


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job-id', required=True)
    args = parser.parse_args()
    from syncmate_core.context import use
    from syncmate_core.queue import runner_queue_job_details, runner_queue_job_status
    from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
    root = Path(__file__).resolve().parents[2]
    with use(root, extension=OpenGUProjectExtension()):
        details = runner_queue_job_details(args.job_id)
        job = details
        definition = OpenGUProjectExtension().resolve_recipe(root, job['recipe'])
        terminal = runner_queue_job_status(args.job_id)
        print(reconcile(job, definition, details['receipt']['output_contract'], terminal,
            root / 'results/runtime/modular/_journal/auto_report.events.jsonl'))


if __name__ == '__main__':
    main()
