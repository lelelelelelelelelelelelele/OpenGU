"""Source extraction acceleration must preserve every scientific digest."""
import importlib.util
import inspect

import pytest

import experiments.implementation_identity as identity


@pytest.mark.parametrize('method', ['GNNDelete', 'Retrain', 'GIF', 'MEGU', 'IDEA', 'GraphEraser', 'GraphRevoker'])
def test_gu_fingerprints_match_unindexed_extraction(method, monkeypatch):
    from experiments.modular_gu import gu_producer
    accelerated = identity.computation_source
    reference = inspect.unwrap(accelerated)
    model = {'architecture': 'OpenGU.GCNNet', 'hidden_channels': 4}
    with monkeypatch.context() as patch:
        patch.setattr(identity, 'computation_source', reference)
        with identity.fingerprint_session():
            expected = gu_producer(method, model)
    with identity.fingerprint_session():
        assert gu_producer(method, model) == expected


def test_metric_fingerprints_and_receipts_match_unindexed_extraction(monkeypatch):
    from experiments.modular_evaluation import CASES, _formula_functions
    from experiments.evaluation_cache import evaluation_request
    accelerated = identity.computation_source
    reference = inspect.unwrap(accelerated)
    for case, spec in CASES.items():
        with monkeypatch.context() as patch:
            patch.setattr(identity, 'computation_source', reference)
            with identity.fingerprint_session():
                before = evaluation_request(case, spec['metrics'], [], _formula_functions(case), spec['producer_version'])
        with identity.fingerprint_session():
            after = evaluation_request(case, spec['metrics'], [], _formula_functions(case), spec['producer_version'])
        assert after.recipe.canonical_json == before.recipe.canonical_json
        assert after.recipe.recipe_hash == before.recipe.recipe_hash


def test_indexed_source_preserves_decorators_comments_and_eof(tmp_path, monkeypatch):
    path = tmp_path / 'extraction_fixture.py'
    path.write_text('''from dataclasses import dataclass
@dataclass(frozen=True)
class Sample:
    value: int
    @staticmethod
    def multiline():
        return (
            1 + 2
        )
    # unrelated outer comment
        # inspect includes this trailing inner comment

    async def nested(self):
        def inner():
            return self.value
        return inner()

    def one_line(self): return self.value

def last():
    return 7''', encoding='utf-8')
    spec = importlib.util.spec_from_file_location('extraction_fixture', path)
    module = importlib.util.module_from_spec(spec)
    import sys
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    values = [module.Sample, module.Sample.multiline, module.Sample.nested, module.Sample.one_line, module.last]
    reference = inspect.unwrap(identity.computation_source)
    expected = [reference(value) for value in values]
    original = identity.ast.parse
    calls = []
    def parse(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)
    monkeypatch.setattr(identity.ast, 'parse', parse)
    with identity.fingerprint_session():
        assert [identity.computation_source(v) for v in values] == expected
        assert [identity.computation_source(v) for v in values] == expected
    assert len(calls) == 1
    with identity.fingerprint_session():
        assert identity.computation_source(module.Sample) == expected[0]
    assert len(calls) == 2
