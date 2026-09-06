"""Validate or execute one ordinary experiment YAML, directly or through Core."""
from __future__ import annotations
import argparse
import contextlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main(argv=None):
    # The command's JSON and diagnostic streams use the same encoding on Windows and SSH.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--verification-root', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--device-config', type=Path, default=ROOT / '.syncmate/device.yaml')
    args = parser.parse_args(argv)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            from experiments.modular_run import execute
            if args.dry_run:
                if args.verification_root or args.run_id:
                    raise ValueError('dry-run has no execution context')
                result = execute(args.config, dry_run=True)
            else:
                if args.run_id is None:
                    raise ValueError('execution requires --run-id')
                from experiments.modular_config import load_experiment
                from experiments.modular_execution import device_context
                config = load_experiment(args.config)
                context = device_context(config['experiment_id'], run_id=args.run_id,
                    device_file=args.device_config, verification_root=args.verification_root)
                if args.verification_root:
                    import torch
                    torch.set_num_threads(1)
                result = execute(args.config, context=context)
                from experiments.modular_artifacts import generated_paths
                result.update(passed=True, generated_artifacts=generated_paths(result, context))
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 1 if result.get('passed') is False else 0
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
