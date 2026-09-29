import importlib.util
from pathlib import Path
from types import SimpleNamespace
import pytest

spec = importlib.util.spec_from_file_location('cache_gate', Path(__file__).parents[1] / 'scripts/verify_exp011_cache.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def test_miss_fails_before_caller_can_compute():
    request = SimpleNamespace(recipe=SimpleNamespace(recipe_hash='missing-recipe'))
    calls = []
    def consumer():
        gate.require_hit(lambda root, req: None)(None, request)
        calls.append('producer')
    with pytest.raises(AssertionError, match='cache MISS: missing-recipe'):
        consumer()
    assert calls == []


def test_hit_preserves_verified_result_and_fingerprint_source():
    result = object()
    def resolver(root, request):
        return result
    wrapped = gate.require_hit(resolver)
    assert wrapped(None, None) is result
    assert wrapped.__wrapped__ is resolver
    blocked = gate.forbid(resolver)
    assert blocked.__wrapped__ is resolver
    with pytest.raises(AssertionError, match='forbids producer'):
        blocked(None, None)
