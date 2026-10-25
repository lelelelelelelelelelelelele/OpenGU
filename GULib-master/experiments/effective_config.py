"""Strict, semantic configuration values; source locations are provenance only."""
from __future__ import annotations

import copy
import math
from pathlib import Path
import yaml
from contextlib import contextmanager
from contextvars import ContextVar

_source = ContextVar('opengu_committed_config', default=None)


@contextmanager
def committed_files(source, *, root=None):
    """Explicit committed input view; a missing file never falls back to disk."""
    view = (source, Path(root or source.root).resolve(), set(source.files()), {})
    token = _source.set(view)
    try:
        yield view[3]
    finally:
        _source.reset(token)


def configuration_root(default):
    view = _source.get()
    return view[1] if view else Path(default)


def source_bytes(path):
    view = _source.get()
    if view is None:
        return Path(path).read_bytes()
    relative = Path(path).resolve().relative_to(view[1]).as_posix()
    if relative not in view[3]:
        view[3][relative] = view[0].read_bytes(relative)
    return view[3][relative]


def source_file(path):
    view = _source.get()
    if view is None:
        return Path(path).is_file()
    relative = Path(path).resolve().relative_to(view[1]).as_posix()
    return relative in view[2]


class ConfigurationError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            if key_node.tag == 'tag:yaml.org,2002:merge':
                raise ConfigurationError('YAML merge/implicit inheritance is not supported')
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise ConfigurationError(f'duplicate field: {key}')
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def read_yaml(path):
    value = yaml.load(source_bytes(path).decode('utf-8'), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ConfigurationError('configuration must be a mapping')
    return value


def fields(value, allowed, required=(), label='configuration'):
    if not isinstance(value, dict):
        raise ConfigurationError(f'{label} must be a mapping')
    unknown, missing = set(value) - set(allowed), set(required) - set(value)
    if unknown or missing:
        raise ConfigurationError(f'{label}: unknown={sorted(unknown)}, missing={sorted(missing)}')


def effective(overrides, defaults, label='parameters'):
    """Expand declared defaults with exact types and reject silent overrides."""
    fields(overrides, defaults, label=label)
    result = copy.deepcopy(defaults)
    for key, default in defaults.items():
        value = overrides.get(key, default)
        name = f'{label}.{key}'
        if isinstance(default, dict):
            result[key] = effective(value, default, name)
        elif isinstance(default, float):
            if isinstance(value, bool):
                raise ConfigurationError(f'{name} must be finite numeric')
            try:
                value = float(value)
            except (ValueError, TypeError):
                raise ConfigurationError(f'{name} must be finite numeric') from None
            if not math.isfinite(value):
                raise ConfigurationError(f'{name} must be finite numeric')
            result[key] = value
        elif not isinstance(value, type(default)) or (isinstance(value, bool) and not isinstance(default, bool)):
            raise ConfigurationError(f'{name} must be {type(default).__name__}')
        else:
            result[key] = copy.deepcopy(value)
    return result


def choice(value, values, label):
    if value not in values:
        raise ConfigurationError(f'{label} must be one of {tuple(values)}')
    return value
