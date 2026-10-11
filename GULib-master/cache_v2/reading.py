"""Decode already admitted immutable cache content without rebuilding it."""
from dataclasses import MISSING, fields


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
    import json
    import zipfile
    from io import BytesIO
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
