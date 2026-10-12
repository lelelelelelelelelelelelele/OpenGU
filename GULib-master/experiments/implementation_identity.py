"""Fingerprint explicitly owned Python computations and their local helpers."""
from __future__ import annotations

import ast
import hashlib
import inspect
from functools import wraps
import json
from pathlib import Path
from contextlib import contextmanager
from contextvars import ContextVar


ROOT = Path(__file__).resolve().parents[1]
_run_fingerprints = ContextVar('run_fingerprints', default=None)
_run_producers = ContextVar('run_producers', default=None)
_source_files = ContextVar('computation_source_files', default=None)
_source_texts = ContextVar('computation_source_texts', default=None)


@contextmanager
def fingerprint_session():
    """Source is fixed during one execution; never reuse fingerprints across runs."""
    token = _run_fingerprints.set({})
    producer_token = _run_producers.set({})
    source_token = _source_files.set({})
    text_token = _source_texts.set({})
    try:
        yield
    finally:
        _run_producers.reset(producer_token)
        _source_files.reset(source_token)
        _source_texts.reset(text_token)
        _run_fingerprints.reset(token)


def computation_source(function):
    """Include class decorators consistently on Python 3.8 and newer."""
    lines, first = inspect.getsourcelines(function)
    if not inspect.isclass(function):
        return ''.join(lines)
    path = inspect.getsourcefile(function)
    source = Path(path).read_text(encoding='utf-8')
    classes = [node for node in ast.walk(ast.parse(source))
               if isinstance(node, ast.ClassDef) and node.name == function.__name__
               and first <= node.lineno < first + len(lines)]
    if not classes:
        raise ValueError('cannot locate computation class in its source')
    node = min(classes, key=lambda value: value.lineno)
    start = min([node.lineno] + [item.lineno for item in node.decorator_list])
    return ''.join(source.splitlines(keepends=True)[start - 1:node.end_lineno])


def implementation_fingerprint(*functions):
    memo = _run_fingerprints.get()
    if memo is not None and functions in memo:
        return memo[functions]
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
        sources[name] = computation_source(function)
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
    value = digest.hexdigest()
    if memo is not None:
        memo[functions] = value
    return value


def model_functions(model):
    """Forward/training implementation excludes GU-only reason_once helpers."""
    functions = [type(model).__init__, type(model).forward]
    if hasattr(model, 'load_config'):
        functions.append(type(model).load_config)
    return functions


def model_factory_fingerprint(model_config):
    """Hash common initialization plus only the selected factory branch."""
    from experiments.modular_model import create_model, runtime_defaults
    tree = ast.parse(computation_source(create_model))
    function = tree.body[0]
    for i, node in enumerate(function.body):
        if not isinstance(node, ast.If):
            continue
        branch = node
        while isinstance(branch, ast.If):
            test = branch.test
            if (not isinstance(test, ast.Compare) or not isinstance(test.left, ast.Subscript)
                    or ast.literal_eval(test.left.slice.value if isinstance(test.left.slice, ast.Index) else test.left.slice) != 'architecture'
                    or len(test.comparators) != 1 or not isinstance(test.ops[0], ast.Eq)):
                raise ValueError('unrecognized model factory branch')
            if ast.literal_eval(test.comparators[0]) == model_config['architecture']:
                function.body[i:i + 1] = branch.body
                break
            branch = branch.orelse[0] if len(branch.orelse) == 1 else None
        else:
            raise ValueError('model architecture has no factory branch')
        break
    else:
        raise ValueError('model factory has no architecture dispatch')
    class NormalizeSlice(ast.NodeTransformer):
        def visit_Index(self, node):
            return self.visit(node.value)
    tree = NormalizeSlice().visit(tree)
    def structural(value):
        if isinstance(value, ast.AST):
            return [type(value).__name__, {name: structural(member)
                for name, member in ast.iter_fields(value)
                if (member is not None and member != []) or name == 'value'}]
        if isinstance(value, list):
            return [structural(member) for member in value]
        return value
    # ast.dump omits optional None fields on newer Python, but prints them on 3.8.
    source = json.dumps(structural(tree), sort_keys=True, separators=(',', ':'))
    return hashlib.sha256((source + implementation_fingerprint(runtime_defaults)).encode()).hexdigest()


def _index_source_blocks(extract):
    """Transparent extraction accelerator; preserve source identity via unwrap.

    The original extractor remains appropriate for isolated functions. Classes
    justify parsing their file once and sharing bounds with overlapping methods.
    No source text or digest survives the explicit fingerprint session.
    """
    def read(function):
        files = _source_files.get()
        function = inspect.unwrap(function)
        path = inspect.getsourcefile(function)
        if files is None or (path not in files and not inspect.isclass(function)):
            return extract(function)
        if path not in files:
            source = Path(path).read_text(encoding='utf-8')
            blocks = {}
            pending = list(ast.parse(source).body)
            while pending:
                node = pending.pop()
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    start = min([node.lineno] + [item.lineno for item in node.decorator_list])
                    blocks[start] = blocks[node.lineno] = node
                # Definitions occur in statement suites, never inside the
                # expression trees that dominate numerical implementations.
                for suite in ('body', 'orelse', 'finalbody', 'handlers', 'cases'):
                    pending.extend(getattr(node, suite, ()))
            files[path] = (source.splitlines(keepends=True), blocks)
        lines, blocks = files[path]
        _, first = inspect.findsource(function)
        if getattr(function, '__name__', None) == '<lambda>':
            return ''.join(inspect.getblock(lines[first:]))
        node = blocks[first + 1]
        start = min([node.lineno] + [item.lineno for item in node.decorator_list])
        end = node.end_lineno
        if not isinstance(node, ast.ClassDef) and node.body[0].lineno > node.lineno:
            # inspect includes indented trailing comments, even when separated
            # by an unindented comment, but excludes trailing blank lines.
            column = node.body[0].col_offset
            for number in range(end, len(lines)):
                line = lines[number]
                if not line.strip():
                    continue
                if line.lstrip().startswith('#'):
                    if len(line)-len(line.lstrip()) >= column:
                        end = number + 1
                else:
                    break
        result = ''.join(lines[start - 1:end])
        if not isinstance(node, ast.ClassDef) and not result.endswith('\n'):
            result += '\n'  # inspect/linecache normalizes a missing final newline.
        return result
    @wraps(extract)
    def indexed(function):
        texts = _source_texts.get()
        if texts is not None and function in texts:
            return texts[function]
        result = read(function)
        if texts is not None:
            texts[function] = result
        return result
    return indexed


# functools.wraps keeps the existing computation-source identity. Both paths
# must return byte-for-byte identical text; no hash compatibility table is used.
computation_source = _index_source_blocks(computation_source)
