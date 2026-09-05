"""OpenGU result layout policy shared by executors and SyncMate recipes."""
import re


def modular_output_path(experiment_id: str, run_id: str) -> str:
    for value in (experiment_id, run_id):
        if not isinstance(value, str) or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', value) is None:
            raise ValueError('unsafe experiment or run identity for the result layout')
    return f'results/runs/modular/{experiment_id}/{run_id}/summary.json'


def atomic_output_path(plan: dict) -> str:
    return modular_output_path(plan['experiment_id'], plan['run_id'])
