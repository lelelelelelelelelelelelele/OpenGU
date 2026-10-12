"""Decode already admitted immutable cache content without rebuilding it."""
from dataclasses import MISSING, fields
from io import BytesIO
import json
from types import SimpleNamespace
import zipfile


def cached_fields(cls, values):
    """Construct a stored value; producer constructors own admission checks."""
    result = object.__new__(cls)
    definitions = fields(cls)
    if set(values) - {field.name for field in definitions}:
        raise ValueError('unknown cached payload fields')
    for field in definitions:
        if field.name in values:
            value = values[field.name]
        elif field.default is not MISSING:
            value = field.default
        else:
            raise ValueError('missing cached payload field: ' + field.name)
        object.__setattr__(result, field.name, value)
    return result


def cached_npz(cls, payload):
    from .formal_artifacts import _read_npy
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        metadata = json.loads(archive.read('metadata.json'))
        names = set(archive.namelist())
        values = {}
        for field in fields(cls):
            member = field.name + '.npy'
            if member in names:
                value = _read_npy(archive.read(member), field.name)
                value.setflags(write=False)
                values[field.name] = value
            elif field.name in metadata:
                values[field.name] = metadata[field.name]
            elif field.name == 'scores':
                values[field.name] = None
    return cached_fields(cls, values)


def _output_groups(archive, metadata, groups):
    from .formal_artifacts import _read_npy
    values = {}
    for group in groups:
        values[group] = {}
        for key in metadata['tensors'][group]:
            value = _read_npy(archive.read(group + '__' + key + '.npy'), key)
            value.setflags(write=False)
            values[group][key] = value
    return values


def read_cached_payload(cls, payload):
    """Decode an admitted value without invoking its producer constructor.

    IO stays outside scientific Payload classes: their original source is part
    of the computation fingerprint and must not change with reader optimizations.
    """
    if getattr(cls, 'payload_schema', None) == 'cache_v2.node_unlearning_output':
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            metadata = json.loads(archive.read('metadata.json'))
            groups = _output_groups(archive, metadata, ('arrays', 'state', 'auxiliary'))
        return cached_fields(cls, dict(identity=metadata['identity'],
            payload_version=metadata['payload_version'], **groups))
    if getattr(cls, 'file_extension', None) == 'npz':
        return cached_npz(cls, payload)
    values = json.loads(payload)
    for name in ('selected_nodes_ordered', 'candidate_nodes_ordered'):
        if name in values:
            values[name] = tuple(values[name])
    if 'candidate_nodes_ordered' in values:
        for name in ('scores', 'rankings'):
            values[name] = {key: tuple(value) for key, value in values[name].items()}
    return cached_fields(cls, values)


def read_metric_output(path):
    """Seek to evaluation members; do not read model/auxiliary tensor bodies."""
    with path.open('rb') as stream, zipfile.ZipFile(stream) as archive:
        metadata = json.loads(archive.read('metadata.json'))
        groups = _output_groups(archive, metadata, ('arrays',))
    return SimpleNamespace(identity=metadata['identity'], arrays=groups['arrays'])
