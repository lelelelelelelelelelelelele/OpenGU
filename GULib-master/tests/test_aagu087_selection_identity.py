"""Real selector-to-GU regression, using the shipped compatibility registry."""
from functools import wraps
import pytest
import yaml

from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion
from cache_v2.source_compatibility import recipe_candidates, stored_recipe
from experiments.target_direct_v1 import method_cache
from experiments.implementation_identity import implementation_fingerprint
from test_modular_consumers import tables, run, write_yaml
from test_cache_v2_formal_artifacts import _tree_state


OLD = '478e61a1077d338e99cc3bdb4cba75f036c34f74b36eb27e36ea366d37705c4b'
ORCHESTRATION = 'b593fa9155d203f523c4c5754eab5b819bff0cb9ac764c6d970c5ae4329c2114'
METHODS = ['r_point', 'gt_full', 'degree', 'random', 'pagerank']


@pytest.mark.parametrize('method', METHODS)
def test_real_historical_selection_to_gu_with_newer_duplicate(tables, monkeypatch, method):
    root = tables[0]
    source = 'r_point.yaml' if method in ('r_point', 'gt_full') else 'degree.yaml'
    selector = yaml.safe_load((root / source).read_text())
    selector['method'] = method
    if method in ('r_point', 'gt_full'):
        selector['parameters'] = {'lissa': {'iterations': 2, 'scale': 25., 'damp': .01}}
    write_yaml(root / 'selected.yaml', selector)
    options = dict(stage='unlearning', selector_refs=['selected.yaml'],
                   unlearning_refs=['gu.yaml'], evaluation_refs=['utility.yaml'])
    with monkeypatch.context() as patch:
        patch.setattr(method_cache, 'implementation_fingerprint', lambda *args: OLD)
        historical = run(tables, 'historical', **options)

    # Reproduce the failed deployment: same selection bytes, unregistered source.
    import cache_v2.source_compatibility as compatibility
    with monkeypatch.context() as patch:
        patch.setattr(method_cache, 'implementation_fingerprint', lambda *args: ORCHESTRATION)
        patch.setattr(compatibility, 'registry', lambda: [])
        duplicate = run(tables, 'duplicate', **options)
    old = historical['selectors'][0]['selection']['artifact']
    new = duplicate['selectors'][0]['selection']['artifact']
    assert old['artifact_id'] != new['artifact_id']
    assert old['content_hash'] == new['content_hash']
    assert duplicate['unlearning'][0]['producer_called']

    # Guard the real computation seams, keeping their inspected source identity.
    import experiments.modular_gu as gu
    for mapping, key in [(gu.GU_METHODS, 'GNNDelete')]:
        original = mapping[key]
        @wraps(original)
        def forbidden(*args, **kwargs):
            raise AssertionError('cached computation producer was called')
        monkeypatch.setitem(mapping, key, forbidden)
    get_score = method_cache.ScoreBundleStore.get_or_compute
    def guarded_score(self, recipe, producer, **kwargs):
        kwargs['fail_if_called'] = True
        return get_score(self, recipe, producer, **kwargs)
    monkeypatch.setattr(method_cache.ScoreBundleStore, 'get_or_compute', guarded_score)
    materialize = method_cache.materialize_budget_selection
    def guarded(**kwargs):
        kwargs['fail_if_producer_called'] = True
        return materialize(**kwargs)
    monkeypatch.setattr(method_cache, 'materialize_budget_selection', guarded)
    cache_root = root / 'results/cache_v2'
    before = _tree_state(cache_root)
    warm = run(tables, 'fixed', **options)
    actual = warm['selectors'][0]
    assert actual['selection']['artifact'] == old
    assert actual['score']['artifact_id'] == historical['selectors'][0]['score']['artifact_id']
    assert actual['score']['producer_called'] is False
    assert actual['selection']['cache']['producer_called'] is False
    assert warm['unlearning'][0]['artifact_id'] == historical['unlearning'][0]['artifact_id']
    assert warm['unlearning'][0]['producer_called'] is False
    assert _tree_state(cache_root) == before

    # An exact current object must still win over registered historical objects.
    from cache_v2.index import CacheIndex
    from cache_v2.selection_materializer import SelectionArtifactRequest, store_selection_artifact, resolve_selection_artifact
    index = CacheIndex(cache_root / 'index.sqlite')
    previous = stored_recipe(index.get_artifact(old['artifact_id']))
    producer = ProducerVersion('target-direct-method-prefix-v1',
                              implementation_fingerprint(method_cache.project_ranking))
    fields = previous.fields
    fields['producer_version'] = producer.to_dict()
    request = SelectionArtifactRequest.from_recipe(ArtifactRecipe(fields), producer)
    nodes = actual['selection']['views']['1']['selected_nodes']
    current = store_selection_artifact(cache_root, request, selected_nodes=nodes, compute_seconds=0.)
    assert resolve_selection_artifact(cache_root, request).result.artifact_id == current.artifact_id


@pytest.mark.parametrize('method', METHODS)
def test_registry_current_source_and_unknown_source_boundaries(method):
    current = implementation_fingerprint(method_cache.project_ranking)
    fields = {'selector': method, 'producer_version': {
        'semantic_version': 'target-direct-method-prefix-v1', 'source_fingerprint': current}}
    candidates = list(recipe_candidates(ArtifactType.SELECTION, ArtifactRecipe(fields)))
    assert [x.fields['producer_version']['source_fingerprint'] for x in candidates] == [current, OLD, ORCHESTRATION]
    fields['producer_version']['source_fingerprint'] = 'unreviewed-algorithm-change'
    assert len(list(recipe_candidates(ArtifactType.SELECTION, ArtifactRecipe(fields)))) == 1
    fields['producer_version']['source_fingerprint'] = current
    fields['producer_version']['semantic_version'] = 'different-algorithm'
    assert len(list(recipe_candidates(ArtifactType.SELECTION, ArtifactRecipe(fields)))) == 1
