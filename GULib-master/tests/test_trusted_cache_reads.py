"""Trusted cache consumption is distinct from producer admission and auditing."""
import pickle

import pytest

from test_modular_consumers import tables, run
from test_evaluation_cache import setup


def test_real_hot_entry_does_not_rehash_rebuild_or_audit_ancestors(tables, monkeypatch):
    from cache_v2 import CacheIndex
    from cache_v2.resolver import ArtifactResolver
    from cache_v2.unlearning_output import UnlearningOutputPayload
    from cache_v2.output_evaluation import OutputEvaluationPayload
    import cache_v2.formal_store as formal
    import cache_v2.store as selections
    root, options = setup(tables)
    cold = run(tables, 'trusted-source', **options)
    def forbidden(*a, **k):
        pytest.fail('normal HIT replayed a file integrity or ancestor audit')
    monkeypatch.setattr(ArtifactResolver, '_dependency_issues', forbidden)
    monkeypatch.setattr(CacheIndex, 'parents', forbidden)
    monkeypatch.setattr(formal, 'sha256_bytes', forbidden)
    input_hash = selections.sha256_bytes
    def requested_identity_only(value):
        assert value.startswith(b'['), 'HIT checksummed a Selection file'
        return input_hash(value)
    monkeypatch.setattr(selections, 'sha256_bytes', requested_identity_only)
    monkeypatch.setattr(UnlearningOutputPayload, 'canonical_bytes', property(forbidden))
    monkeypatch.setattr(OutputEvaluationPayload, 'canonical_bytes', property(forbidden))
    warm = run(tables, 'trusted-warm', **options)
    for before, after in zip(cold['unlearning'], warm['unlearning']):
        assert before['output'] == after['output']
        assert before['evaluation'] == after['evaluation']
        assert after['evaluation_cache']['hit']


def test_metric_miss_reads_no_model_state_and_does_not_rebuild_npz(tables, monkeypatch):
    import zipfile
    from experiments.unlearning_outputs import load_metric_output
    from experiments.evaluation_cache import single_values
    from cache_v2.unlearning_output import UnlearningOutputPayload
    root, options = setup(tables)
    cold = run(tables, 'slim-source', **options)
    data = pickle.loads((root/'graph.pkl').read_bytes())
    reference = cold['unlearning'][0]['output']
    original = zipfile.ZipFile.read
    def read(archive, member, *args, **kwargs):
        assert not str(member).startswith(('state__', 'auxiliary__'))
        return original(archive, member, *args, **kwargs)
    monkeypatch.setattr(zipfile.ZipFile, 'read', read)
    monkeypatch.setattr(UnlearningOutputPayload, 'canonical_bytes',
                        property(lambda *a: pytest.fail('metric input rebuilt NPZ')))
    output = load_metric_output(reference, root/'results/cache_v2', data=data, dataset_root=root)
    values = single_values(reference, output)
    assert values['result'] == cold['unlearning'][0]['result']
    assert values['evaluation'] == cold['unlearning'][0]['evaluation']
    assert not hasattr(output, 'state')


def test_exact_reference_read_does_not_rescan_computation_source(tables, monkeypatch):
    from experiments.unlearning_outputs import load_output_payload, load_metric_output
    from experiments.evaluation_cache import describe_output
    from cache_v2 import CacheIndex
    import experiments.modular_gu as gu
    root, options = setup(tables)
    cold = run(tables, 'reference-source', **options)
    reference = cold['unlearning'][0]['output']
    def forbidden(*a, **k):
        pytest.fail('exact admitted reference regenerated a computation fingerprint')
    monkeypatch.setattr(gu, 'gu_producer', forbidden)
    # The exact row just read by Artifact ID is passed to the lower Store.
    monkeypatch.setattr(CacheIndex, 'find_artifact', forbidden)
    payload = load_output_payload(reference, root/'results/cache_v2')
    assert describe_output(reference, root/'results/cache_v2') == payload.identity
    output = load_metric_output(reference, root/'results/cache_v2', dataset_root=root)
    assert output.identity == payload.identity


def test_write_connection_reuse_keeps_independent_commits_and_rollback(tmp_path):
    from cache_v2 import CacheIndex
    from test_cache_v2_formal_artifacts import _score_recipe, _score_payload, SCORE_VERSION
    from cache_v2.formal_store import FormalArtifactStore
    index = CacheIndex(tmp_path/'index.sqlite')
    index.initialize()
    store = FormalArtifactStore(tmp_path, producer_version=SCORE_VERSION, index=index)
    with index.write_session(), index.read_session():
        stored = store.store_payload(_score_recipe(), _score_payload())
        independent = CacheIndex(index.path)
        assert independent.get_artifact(stored.artifact_id)['status'] == 'valid'
        with pytest.raises(RuntimeError, match='after commit'):
            with index.transaction() as writer:
                writer.connection.execute('DELETE FROM artifacts WHERE artifact_id=?', (stored.artifact_id,))
                raise RuntimeError('after commit')
        assert independent.get_artifact(stored.artifact_id)['status'] == 'valid'


def test_lazy_writer_does_not_claim_an_unopened_index_is_valid(tmp_path):
    from cache_v2 import CacheIndex
    from cache_v2.errors import IndexNotFoundError
    index = CacheIndex(tmp_path/'absent.sqlite')
    with index.write_session(), pytest.raises(IndexNotFoundError):
        index.check_schema()
