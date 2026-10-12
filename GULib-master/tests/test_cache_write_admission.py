"""First-admission contracts using small arrays, without model execution."""
import numpy as np
import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, ProducerVersion
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.output_evaluation import OutputEvaluationPayload, OUTPUT_EVALUATION_CONTRACT
from cache_v2.unlearning_output import UnlearningOutputPayload, OUTPUT_CONTRACT
from cache_v2.store import ArtifactStore
from test_cache_v2_formal_artifacts import _selection_recipe, GRAPH_HASH


VERSION = ProducerVersion('write-admission-fixture-v1', 'write-admission-source-v1')


def evaluation_case(root, count):
    """Use existing Selection fixture and directly supplied Output arrays."""
    selection_recipe = ArtifactRecipe({**_selection_recipe().fields, 'node_id_space': 'pyg-global-node-index-v1'})
    store = ArtifactStore(root, producer_version=VERSION)
    store.initialize()
    selection = store.store_selection(selection_recipe, [4, 1], num_nodes=6,
        candidate_nodes=list(range(6)))
    outputs = []
    for number in range(count):
        identity = dict(dataset_input={'fixture': 'six-nodes'},
            pairing={'selected_nodes': [4, 1]}, target={'method': 'Retrain', 'fixture': number},
            graph_fingerprint=GRAPH_HASH, producer_version=VERSION.to_dict(),
            selection={'artifact_id': selection.artifact_id,
                'recipe_hash': selection_recipe.recipe_hash, 'content_hash': selection.content_hash})
        payload = UnlearningOutputPayload(identity,
            {'logits': np.zeros((6, 2), dtype=np.float32), 'selected_nodes': np.array([4, 1])},
            {'weight': np.zeros((2, 2), dtype=np.float32)}, {})
        recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity})
        saved = FormalArtifactStore(root, producer_version=VERSION).store_payload(recipe, payload)
        outputs.append(dict(identity=identity, reference={
            'artifact_id': saved.artifact_id, 'recipe_hash': recipe.recipe_hash,
            'content_hash': saved.content_hash}))
    return outputs


def evaluation_request(outputs, token):
    identity = {'outputs': outputs, 'metric': {'name': 'write-fixture', 'version': token}}
    payload = OutputEvaluationPayload(identity, {'accuracy': 0.5})
    recipe = ArtifactRecipe({'artifact_contract': OUTPUT_EVALUATION_CONTRACT,
        'evaluation_identity': identity, 'producer_version': VERSION.to_dict()})
    return recipe, payload


@pytest.mark.parametrize('count', [1, 2])
def test_first_save_encodes_once_and_publishes_exact_bytes(tmp_path, monkeypatch, count):
    import hashlib
    import cache_v2.formal_store as formal
    from cache_v2.index import CacheIndexBatch
    outputs = evaluation_case(tmp_path, count)
    recipe, payload = evaluation_request(outputs, 'once')
    expected = payload.canonical_bytes
    encoded = []
    original = OutputEvaluationPayload.canonical_bytes.fget
    def encode(value):
        encoded.append(value)
        return original(value)
    hashed = []
    def hash_bytes(value):
        hashed.append(value)
        return hashlib.sha256(value).hexdigest()
    monkeypatch.setattr(OutputEvaluationPayload, 'canonical_bytes', property(encode))
    monkeypatch.setattr(formal, 'sha256_bytes', hash_bytes)
    monkeypatch.setattr(CacheIndexBatch, 'add_dependency',
        lambda *a, **k: pytest.fail('new child traversed existing-node dependency validation'))
    store = FormalArtifactStore(tmp_path, producer_version=VERSION)
    saved = store.store_payload(recipe, payload)
    assert encoded == [payload]
    assert hashed == [expected]
    assert (tmp_path / saved.semantic_path).read_bytes() == expected
    assert saved.content_hash == hashlib.sha256(expected).hexdigest()
    assert store.index.parents(saved.artifact_id) == sorted(o['reference']['artifact_id'] for o in outputs)
    loaded = store.load_payload_read_only(ArtifactType.EVALUATION, recipe)
    assert loaded.payload.values == payload.values


def test_new_artifact_edges_use_foreign_keys_and_roll_back_together(tmp_path):
    from cache_v2 import CacheIndexError
    from test_cache_v2 import _artifact_header
    index = CacheIndex(tmp_path / 'index.sqlite')
    index.initialize()
    parent = _artifact_header('prediction', {'name': 'parent'}, b'parent')
    child = _artifact_header('evaluation', {'name': 'child'}, b'child')
    index.register_artifact(parent)
    with pytest.raises(CacheIndexError, match='FOREIGN KEY'):
        with index.transaction() as writer:
            writer.insert_artifact(child, dependencies=(('input', parent.artifact_id),
                ('input', 'pred_00000000_00000000')))
    assert index.find_artifact('evaluation', child.recipe_hash) is None
    with index.transaction() as writer:
        writer.insert_artifact(child, dependencies=(('input', parent.artifact_id),))
    assert index.parents(child.artifact_id) == [parent.artifact_id]


def test_new_artifact_insert_cannot_bypass_existing_graph_cycle_checks(tmp_path):
    from cache_v2 import CacheIndexError, ContractValidationError
    from cache_v2.errors import DependencyCycleError
    from test_cache_v2 import _artifact_header
    index = CacheIndex(tmp_path / 'index.sqlite')
    index.initialize()
    parent = _artifact_header('prediction', {'name': 'parent'}, b'parent')
    child = _artifact_header('evaluation', {'name': 'child'}, b'child')
    index.register_artifact(parent)
    with index.transaction() as writer:
        writer.insert_artifact(child, dependencies=(('input', parent.artifact_id),))
    with pytest.raises(CacheIndexError, match='UNIQUE'):
        with index.transaction() as writer:
            writer.insert_artifact(parent, dependencies=(('input', child.artifact_id),))
    with pytest.raises(DependencyCycleError):
        with index.transaction() as writer:
            writer.add_dependency(child.artifact_id, parent.artifact_id)
    fresh = _artifact_header('evaluation', {'name': 'self-edge'}, b'self-edge')
    with pytest.raises(ContractValidationError, match='itself'):
        with index.transaction() as writer:
            writer.insert_artifact(fresh, dependencies=(('input', fresh.artifact_id),))
    assert index.parents(parent.artifact_id) == []
    assert index.parents(child.artifact_id) == [parent.artifact_id]


def test_failed_admission_cleans_files_and_rolls_back_index(tmp_path, monkeypatch):
    from cache_v2.index import CacheIndexBatch
    outputs = evaluation_case(tmp_path, 2)
    recipe, payload = evaluation_request(outputs, 'rollback')
    store = FormalArtifactStore(tmp_path, producer_version=VERSION)
    before = set((tmp_path / 'artifacts').rglob('*.*'))
    original = CacheIndexBatch.insert_artifact
    def fail_after_insert(writer, header, **kwargs):
        original(writer, header, **kwargs)
        raise RuntimeError('after new artifact and edges')
    monkeypatch.setattr(CacheIndexBatch, 'insert_artifact', fail_after_insert)
    with pytest.raises(RuntimeError, match='after new artifact'):
        store.store_payload(recipe, payload)
    assert store.index.find_artifact('evaluation', recipe.recipe_hash) is None
    assert set((tmp_path / 'artifacts').rglob('*.*')) == before
