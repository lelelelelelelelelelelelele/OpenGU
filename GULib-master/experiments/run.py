"""One ordinary experiment YAML: validate, run on disposable CPU, or use SyncMate."""
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path, nargs='?')
    parser.add_argument('--dry_run', action='store_true')
    parser.add_argument('--verification-root', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--recipe')
    args = parser.parse_args(argv)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            if args.recipe:
                if args.config or args.dry_run or args.verification_root or args.run_id:
                    raise ValueError('a registered recipe owns config, run identity and execution context')
                from experiments.syncmate_stage import run
                result = run(args.recipe)
            else:
                if args.config is None:
                    raise ValueError('an ordinary experiment YAML is required')
                from experiments.modular_run import execute
                if args.dry_run:
                    if args.verification_root or args.run_id:
                        raise ValueError('dry-run has no execution context')
                    result = execute(args.config, dry_run=True)
                else:
                    if args.verification_root is None or args.run_id is None:
                        raise ValueError('execution is owned by the registered SyncMate/project stage; '
                                         'local CPU verification requires --verification-root and --run-id')
                    from experiments.modular_config import load_experiment
                    from experiments.modular_execution import verification_context
                    config = load_experiment(args.config)
                    context = verification_context(config['experiment_id'], run_id=args.run_id,
                                                   root=args.verification_root)
                    import torch
                    torch.set_num_threads(1)
                    result = execute(args.config, context=context)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 1 if result.get('passed') is False else 0
    except (ValueError, RuntimeError, FileNotFoundError, FileExistsError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
