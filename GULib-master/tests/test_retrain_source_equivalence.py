"""Reviewed ordinary Retrain sources; no training, forward, or experiment run."""
import numpy as np
import pytest

from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion
from cache_v2.formal_store import FormalArtifactStore
from cache_v2.store import ArtifactStore
from cache_v2.source_compatibility import recipe_candidates, source_candidates
from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
from experiments.artifact_producer import (
    FormalArtifactRequest, materialize_formal_artifact, resolve_formal_artifact,
)
from test_cache_v2_formal_artifacts import _selection_recipe, _tree_state, SELECTION_VERSION

OLD='31e847b58a5d6ab4aea6bb542b9a3765191b27ccd7344f65d45312e1dc2f07f0'
NEW='0069c204390f24d2fe6e388a20e56593aee6cf27d3b8ef5ae44d2f6f08c77123'
SEMANTIC='opengu-independent-node-output-v1'
MODEL=dict(architecture='OpenGU.GCNNet',layers=2,hidden_channels=64,dropout=0.5)


def forbidden(*args,**kwargs):
    raise AssertionError('No training or other producer may execute')


def fixture(root,source):
    selection_fields=_selection_recipe().fields
    selection_fields['node_id_space']='pyg-global-node-index-v1'
    selection_recipe=ArtifactRecipe(selection_fields)
    selection_store=ArtifactStore(root,producer_version=SELECTION_VERSION)
    selection_store.initialize()
    selection=selection_store.store_selection(selection_recipe,[4,1],num_nodes=6,
        candidate_nodes=tuple(range(6)),compute_seconds=0.)
    producer=ProducerVersion(SEMANTIC,source)
    identity=dict(dataset_input={'artifact_id':'fixture-dataset'},
        graph_fingerprint='a'*64,target={'method':'Retrain','parameters':{}},
        pairing=dict(model=MODEL,training=dict(seed=42,epochs=300,lr=.01,weight_decay=0.,optimizer='adam'),
            selected_nodes=[4,1],data_identity=dict(split_hash='b'*64),
            deletion=dict(evaluation_graph='original')),
        selection=dict(artifact_id=selection.artifact_id,recipe_hash=selection_recipe.recipe_hash,
            content_hash=selection.content_hash),
        producer_version=producer.to_dict())
    # Deliberately synthetic saved logits/state: this is a storage-contract
    # fixture, never a trained scientific result.
    payload=UnlearningOutputPayload(identity,
        dict(logits=np.zeros((6,2),dtype=np.float32),selected_nodes=np.array([4,1],dtype=np.int64)),
        {'fixture_weight':np.zeros((2,3),dtype=np.float32)}, {})
    recipe=ArtifactRecipe(dict(artifact_contract=OUTPUT_CONTRACT,**identity))
    result=FormalArtifactStore(root,producer_version=producer).store_payload(recipe,payload)
    return recipe,result


@pytest.mark.parametrize('stored,requested',[(OLD,NEW),(NEW,OLD)])
def test_real_registry_hit_preserves_store_and_never_calls_producer(tmp_path,stored,requested):
    recipe,original=fixture(tmp_path,stored)
    before=_tree_state(tmp_path)
    fields=recipe.fields
    producer=ProducerVersion(SEMANTIC,requested)
    fields['producer_version']=producer.to_dict()
    request=FormalArtifactRequest(ArtifactType.PREDICTION,ArtifactRecipe(fields),producer)
    result=materialize_formal_artifact(tmp_path,request,forbidden)
    assert not result.producer_called
    assert result.artifact_id==original.artifact_id
    assert result.result.generation_producer==ProducerVersion(SEMANTIC,stored).to_dict()
    assert result.result.consumption_producer==producer.to_dict()
    assert _tree_state(tmp_path)==before


@pytest.mark.parametrize('change',[
    lambda f:f['pairing']['training'].update(seed=43),
    lambda f:f['pairing']['training'].update(epochs=3000),
    lambda f:f['pairing']['model'].update(hidden_channels=32),
    lambda f:f['pairing']['data_identity'].update(split_hash='c'*64),
    lambda f:f['selection'].update(content_hash='d'*64),
    lambda f:f['pairing']['deletion'].update(evaluation_graph='retained'),
    lambda f:f.update(reference=dict(policy='ret-deterministic-v1',arm='joint')),
])
def test_non_source_inputs_and_diagnostic_reference_cannot_reuse(tmp_path,change):
    recipe,_=fixture(tmp_path,OLD)
    before=_tree_state(tmp_path)
    fields=recipe.fields
    producer=ProducerVersion(SEMANTIC,NEW)
    fields['producer_version']=producer.to_dict()
    change(fields)
    request=FormalArtifactRequest(ArtifactType.PREDICTION,ArtifactRecipe(fields),producer)
    assert resolve_formal_artifact(tmp_path,request) is None
    assert _tree_state(tmp_path)==before


def test_current_producer_is_the_reviewed_source():
    from experiments.modular_gu import gu_producer
    assert gu_producer('Retrain',MODEL).source_fingerprint==NEW
    context=dict(model=MODEL,semantic_version=SEMANTIC)
    candidates=list(source_candidates('prediction','Retrain',context,dict(source_fingerprint=NEW)))
    assert candidates[0]==dict(source_fingerprint=NEW)
    assert dict(source_fingerprint=OLD) in candidates
    assert list(source_candidates('prediction','GIF',context,dict(source_fingerprint=NEW)))==[dict(source_fingerprint=NEW)]


def test_source_substitution_never_drops_reference_fields(tmp_path):
    recipe,_=fixture(tmp_path,OLD)
    fields=recipe.fields
    fields['producer_version']=ProducerVersion(SEMANTIC,NEW).to_dict()
    fields['reference']=dict(policy='ret-deterministic-v1',arm='joint')
    request=ArtifactRecipe(fields)
    for candidate in recipe_candidates(ArtifactType.PREDICTION,request):
        actual=candidate.fields
        actual['producer_version']=fields['producer_version']
        assert actual==fields
