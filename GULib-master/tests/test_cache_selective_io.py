"""Independent trusted metadata and selective on-disk Output consumption."""
import io
from pathlib import Path

import numpy as np
import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, CacheIndexError
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.reading import read_metric_output
from cache_v2.store import ArtifactIntegrityError
from cache_v2.unlearning_output import UnlearningOutputPayload, OUTPUT_CONTRACT
from experiments.unlearning_outputs import load_output_payload
from test_cache_write_admission import evaluation_case, VERSION


def test_admitted_index_reads_only_decode_json(tmp_path, monkeypatch):
    import cache_v2.index as module
    outputs = evaluation_case(tmp_path, 1)
    index = CacheIndex(tmp_path / 'index.sqlite')
    reference = outputs[0]['reference']
    def forbidden(*args, **kwargs):
        pytest.fail('ordinary metadata read revalidated an admitted row')
    monkeypatch.setattr(module, '_parse_canonical_json', forbidden)
    monkeypatch.setattr(module, '_validate_artifact_record', forbidden)
    monkeypatch.setattr(module, 'build_artifact_id', forbidden)
    record = index.get_artifact(reference['artifact_id'])
    assert all(record[key] == value for key, value in reference.items())
    assert index.find_artifact(ArtifactType.PREDICTION, reference['recipe_hash']) == record
    # Upper reference consumers must not rebuild admitted Recipes either.
    monkeypatch.setattr(ArtifactRecipe, '__init__', forbidden)
    assert load_output_payload(reference, tmp_path).identity == outputs[0]['identity']
    from experiments.evaluation_cache import describe_output
    assert describe_output(reference, tmp_path) == outputs[0]['identity']


def test_invalid_index_json_is_still_a_read_error():
    from cache_v2.index import _json_record
    with pytest.raises(CacheIndexError, match='invalid metadata_json'):
        _json_record({'metadata_json': '{'})


def test_metric_reader_seeks_past_unused_tensor_bodies(tmp_path, monkeypatch):
    outputs = evaluation_case(tmp_path, 1)
    identity = {**outputs[0]['identity'], 'target': {'method': 'Retrain', 'fixture': 'large-state'}}
    logits = np.arange(48, dtype=np.float32).reshape(6, 8)
    payload = UnlearningOutputPayload(identity,
        {'logits': logits, 'selected_nodes': np.array([4, 1])},
        {'weight': np.zeros(1024 * 1024, dtype=np.float32)},
        {'unused': np.zeros(1024 * 1024, dtype=np.float32)})
    recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity})
    saved = FormalArtifactStore(tmp_path, producer_version=VERSION).store_payload(recipe, payload)
    path = tmp_path / saved.semantic_path
    reference = {key: getattr(saved, key) for key in ('artifact_id', 'recipe_hash', 'content_hash')}
    read_bytes = []
    streams = []
    original_open = Path.open
    class CountingReader(io.BufferedReader):
        def read(self, size=-1):
            result = super().read(size)
            read_bytes.append(len(result))
            return result
    def open_file(target, *args, **kwargs):
        if target == path:
            stream = CountingReader(io.FileIO(target, 'rb'))
            streams.append(stream)
            return stream
        return original_open(target, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', open_file)
    original_bytes = Path.read_bytes
    def read_whole(target):
        assert target != path, 'metric reader read the whole NPZ'
        return original_bytes(target)
    monkeypatch.setattr(Path, 'read_bytes', read_whole)
    value = load_output_payload(reference, tmp_path, reader=read_metric_output)
    assert value.identity == identity
    np.testing.assert_array_equal(value.arrays['logits'], logits)
    np.testing.assert_array_equal(value.arrays['selected_nodes'], [4, 1])
    assert not value.arrays['logits'].flags.writeable
    assert not hasattr(value, 'state') and not hasattr(value, 'auxiliary')
    assert sum(read_bytes) < 100_000 < path.stat().st_size
    assert streams and all(stream.closed for stream in streams)


@pytest.mark.parametrize('failure', ['missing', 'malformed'])
def test_metric_reader_propagates_real_file_errors(tmp_path, failure):
    outputs = evaluation_case(tmp_path, 1)
    reference = outputs[0]['reference']
    record = CacheIndex(tmp_path / 'index.sqlite').get_artifact(reference['artifact_id'])
    path = tmp_path / record['semantic_path']
    if failure == 'missing':
        path.unlink()
    else:
        path.write_bytes(b'not an NPZ')
    with pytest.raises(ArtifactIntegrityError, match='missing|cannot be read or parsed'):
        load_output_payload(reference, tmp_path, reader=read_metric_output)
