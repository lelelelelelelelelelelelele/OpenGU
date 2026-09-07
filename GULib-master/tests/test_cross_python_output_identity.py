"""Cross-runtime provenance must stay strict without depending on inspect quirks."""
import copy
import inspect
from dataclasses import dataclass

import pytest
from cache_v2 import canonical_sha256
from experiments.implementation_identity import computation_source, implementation_fingerprint


@dataclass(frozen=True)
class DecoratedPayload:
    value: int


def test_class_fingerprint_is_independent_of_inspect_decorator_start(monkeypatch):
    original = inspect.getsourcelines
    expected = implementation_fingerprint(DecoratedPayload)
    assert computation_source(DecoratedPayload).startswith('@dataclass(frozen=True)\n')
    def class_start(value):
        lines, start = original(value)
        if value is DecoratedPayload:
            while lines[0].startswith('@'):
                lines, start = lines[1:], start + 1
        return lines, start
    monkeypatch.setattr(inspect, 'getsourcelines', class_start)
    assert implementation_fingerprint(DecoratedPayload) == expected
