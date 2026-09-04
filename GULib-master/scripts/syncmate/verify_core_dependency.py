"""Verify the installed payload against the independently published Core wheel."""
from __future__ import annotations
import argparse
import hashlib
import json
from importlib import metadata
from pathlib import Path

PIN_PATH = Path(__file__).with_name('core_dependency.json')


def verify_core_dependency(*, distribution_lookup=metadata.distribution, core_module=None,
                           pin_path=PIN_PATH):
    pin = json.loads(Path(pin_path).read_text(encoding='utf-8'))
    result = {'ready': False, 'expected': {k: v for k, v in pin.items() if k != 'files'},
              'observed': {}, 'errors': []}
    errors = result['errors']
    try:
        dist = distribution_lookup(pin['distribution'])
    except metadata.PackageNotFoundError:
        errors.append('SyncMate Core distribution is not installed')
        return result
    if core_module is None:
        try:
            import syncmate_core as core_module
        except ImportError as exc:
            errors.append('SyncMate Core module import failed: ' + str(exc))
    module_file = getattr(core_module, '__file__', None)
    observed = result['observed']
    observed.update(distribution_version=dist.version,
                    version=getattr(core_module, '__version__', None),
                    module_file=str(Path(module_file).resolve()) if module_file else None)
    if dist.version != pin['version'] or observed['version'] != pin['version']:
        errors.append('SyncMate Core version mismatch')
    expected_module = Path(dist.locate_file('syncmate_core/__init__.py')).resolve()
    if not module_file or Path(module_file).resolve() != expected_module:
        errors.append('SyncMate Core imported module does not belong to the installed distribution')
    checked = 0
    for relative, digest in pin['files'].items():
        path = Path(dist.locate_file(relative))
        if not path.is_file() or path.is_symlink():
            errors.append('SyncMate Core payload missing or linked: ' + relative)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append('SyncMate Core payload SHA-256 mismatch: ' + relative)
        else:
            checked += 1
    package = expected_module.parent
    actual = {p.relative_to(package.parent).as_posix() for p in package.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    expected = {p for p in pin['files'] if p.startswith('syncmate_core/')}
    if actual != expected:
        errors.append('SyncMate Core package file set mismatch')
    observed['verified_payload_files'] = checked
    result['ready'] = not errors
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    result = verify_core_dependency()
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else
          'SyncMate Core dependency: ' + ('ready' if result['ready'] else 'blocked') +
          '\n' + '\n'.join(result['errors']))
    return 0 if result['ready'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
