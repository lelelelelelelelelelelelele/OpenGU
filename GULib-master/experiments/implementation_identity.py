"""Fingerprint explicitly owned Python computations and their local helpers."""
from __future__ import annotations

import hashlib
import inspect
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def implementation_fingerprint(*functions):
    pending, seen, sources = list(functions), set(), {}
    while pending:
        function = inspect.unwrap(pending.pop())
        if function in seen:
            continue
        seen.add(function)
        try:
            path = inspect.getsourcefile(function)
        except TypeError:  # Built-in classes have no project source.
            continue
        if not path or path.startswith('<') or ROOT not in Path(path).resolve().parents:
            continue
        name = function.__module__ + '.' + function.__qualname__
        sources[name] = inspect.getsource(function)
        if inspect.isclass(function):
            pending.extend(base for base in function.__bases__ if base is not object)
            pending.extend(value for value in vars(function).values() if inspect.isfunction(value))
        code = getattr(function, '__code__', None)
        namespace = getattr(function, '__globals__', {})
        if code:
            for symbol in code.co_names:
                dependency = namespace.get(symbol)
                if inspect.isclass(dependency) and symbol == function.__qualname__.split('.')[0]:
                    continue
                if inspect.isfunction(dependency) or inspect.isclass(dependency):
                    pending.append(dependency)
    digest = hashlib.sha256()
    for name, source in sorted(sources.items()):
        digest.update(name.encode() + b'\0' + source.encode() + b'\0')
    return digest.hexdigest()


def model_functions(model):
    """Forward/training implementation excludes GU-only reason_once helpers."""
    functions = [type(model).__init__, type(model).forward]
    if hasattr(model, 'load_config'):
        functions.append(type(model).load_config)
    return functions
