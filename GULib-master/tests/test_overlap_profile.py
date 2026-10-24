"""AAGU-117: real prepared parents, independent membership permutation and GU."""
import copy
import functools
import hashlib
import json
import pickle
from types import SimpleNamespace

import pytest
import torch
import yaml

from test_modular_consumers import tables, run, write_yaml, identities
from test_class_matched_r_point import matched_tables
from test_ret_reference import reference_config, policy_isolation
from experiments.target_direct_v1.overlap_profile import (
    METHOD, overlap_profile_order, score_overlap, draw_seed)
from experiments.target_direct_v1.methods import resolve_parameters


def profile_tables(tables, k=7, seed=144):
    refs = matched_tables(tables, k=k)
    value = yaml.safe_load((tables[0] / refs[1]).read_text(encoding='utf-8'))
    value['method'] = METHOD
    value['parameters'].update(overlap_seed=seed, profile_counts=[2, 7])
    write_yaml(tables[0] / 'profile.yaml', value)
    return refs[:2]


def assert_profile(candidates, source, matched, profile, counts):
    assert sorted(profile) == list(candidates)
    assert len(set(profile)) == len(candidates)
    for k in range(len(candidates) + 1):
        for boundary in counts:
            assert len(set(profile[:k]) & set(source[:boundary])) == len(set(matched[:k]) & set(source[:boundary]))
    assert set(profile[:counts[0]]) < set(profile[:counts[1]])


def forbid_scores(monkeypatch, names=('r_point', 'class_matched_r_point', METHOD)):
    from experiments.target_direct_v1 import methods
    for name in names:
        def forbidden(*a, **kw):
            raise AssertionError('prepared dependency or warm profile recomputed a Score')
        monkeypatch.setitem(methods.METHODS, name, functools.wraps(methods.METHODS[name])(forbidden))


def test_membership_all_prefixes_independent_rng_no_class_access():
    candidates = list(range(36))
    source, matched = candidates[::-1], candidates[::2] + candidates[1::2]
    params = {'profile_counts': [4, 13], 'overlap_seed': 144}
    identities = ({'source': 'S'}, {'source': 'M'})
    before = torch.get_rng_state().clone()
    first = overlap_profile_order(candidates, source, matched, params, *identities)
    assert first == overlap_profile_order(candidates, source, matched, params, *identities)
    assert torch.equal(before, torch.get_rng_state())
    assert_profile(candidates, source, matched, first, params['profile_counts'])
    assert draw_seed(params, *identities) != draw_seed({**params, 'overlap_seed': 145}, *identities)
    assert first != overlap_profile_order(candidates, source, matched, {**params, 'overlap_seed': 145}, *identities)
    class NoLabels:
        @property
        def y(self):
            raise AssertionError('profile permutation read class labels')
    c = SimpleNamespace(candidates=torch.tensor(candidates), data=NoLabels())
    scores = score_overlap(c, params, source_ranking=source, matched_ranking=matched,
                           source_identity=identities[0], matched_identity=identities[1])
    from experiments.c_target_v1.core import stable_ranking
    assert tuple(stable_ranking(candidates, scores)) == first


@pytest.mark.parametrize('field,value', [
    ('candidate_ids', [0, 0, 2, 3, 4, 5]), ('candidate_ids', [1, 0, 2, 3, 4, 5]),
    ('source_ranking', [0, 1]), ('source_ranking', [0, 0, 2, 3, 4, 5]),
    ('source_ranking', [False, 1, 2, 3, 4, 5]), ('matched_ranking', [0, 1, 2, 3, 4, 6]),
    ('profile_counts', [0, 3]), ('profile_counts', [3, 3]), ('profile_counts', [2, 6]),
    ('profile_counts', [2]), ('profile_counts', [True, 3]), ('overlap_seed', -1),
    ('overlap_seed', True), ('overlap_seed', 2**63),
])
def test_invalid_profile_inputs(field, value):
    args = dict(candidate_ids=list(range(6)), source_ranking=list(range(6)),
                matched_ranking=list(range(5, -1, -1)),
                parameters={'profile_counts': [2, 4], 'overlap_seed': 144},
                source_identity={'S': 1}, matched_identity={'M': 1})
    if field in ('profile_counts', 'overlap_seed'):
        args['parameters'][field] = value
    else:
        args[field] = value
    with pytest.raises(ValueError):
        overlap_profile_order(**args)


@pytest.mark.parametrize('parameters', [{}, {'matching_seed':44},
    {'matching_seed':44,'overlap_seed':144},
    {'matching_seed':44,'overlap_seed':True,'profile_counts':[2,7]},
    {'matching_seed':44,'overlap_seed':144,'profile_counts':[7,2]},
    {'matching_seed':44,'overlap_seed':144,'profile_counts':[2,7],'seed':7}])
def test_explicit_profile_configuration(parameters):
    with pytest.raises(ValueError):
        resolve_parameters(METHOD, parameters)


def test_native_cold_only_profile_warm_prefix_and_exact_parents(tables, monkeypatch, record_property):
    refs = profile_tables(tables)
    parents = run(tables, 'parents', selector_refs=refs, return_scores=True)['selectors']
    forbid_scores(monkeypatch, ('r_point', 'class_matched_r_point'))
    cold = run(tables, 'profile-cold', selector_refs=['profile.yaml'], return_scores=True)
    row = cold['selectors'][0]
    assert row['checkpoint']['hit'] and row['score']['producer_called'] and row['selection']['cache']['producer_called']
    for name, parent in zip(('source_r_point', 'source_class_matched'), parents):
        assert row[name]['score_hit'] and not row[name]['producer_called']
        assert row['score']['recipe']['fields'][name] == {k:parent['score'][k] for k in ('artifact_id','recipe_hash','content_hash')}
    assert_profile(list(range(10)), parents[0]['ranking'], parents[1]['ranking'], row['ranking'], [2,7])
    from scripts.syncmate.opengu_recipes import generate, assemble
    spec=generate('profile-cold.yaml',recipe_id='profile-contract',run_id='profile-cold',project_root=tables[0])
    declaration=assemble(spec,tables[0])
    assert spec['expected_datasets']==[{'num_nodes':20,'candidate_count':10}]
    assert len(declaration['expected_artifact_paths'])==3
    assert all((tables[0]/path).is_file() for path in declaration['expected_artifact_paths'])
    record_property('native_recipe',json.dumps(dict(spec=spec,definition=declaration)))
    forbid_scores(monkeypatch, (METHOD,))
    profile_tables(tables, k=2)
    warm = run(tables, 'profile-warm', selector_refs=['profile.yaml'], return_scores=True)
    again = warm['selectors'][0]
    assert identities(cold) == identities(warm)
    assert again['checkpoint']['hit'] and again['score']['hit'] and again['selection']['cache']['hit']
    assert not again['score']['producer_called'] and not again['selection']['cache']['producer_called']
    from experiments.modular_artifacts import read_run
    path = tables[0]/'results/runs/profile-warm/profile-warm/run.json'
    manifest, docs = read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
    assert docs[0]['scores.npz']['ranking'].tolist() == row['ranking']
    assert docs[0]['selection.json']['selected_nodes'] == row['ranking'][:2]
    record_property('profile_cold_warm', json.dumps(dict(cold=row,warm=again)))


@pytest.mark.parametrize('missing', ['proxy','S','M','parent_selection','profile_score','profile_selection'])
def test_missing_preparation_fails_without_producing_any_template(tables, monkeypatch, missing):
    root = tables[0]
    refs = profile_tables(tables, k=2 if missing in ('parent_selection','profile_selection') else 7)
    if missing != 'proxy':
        prepared = run(tables, 'prepared', selector_refs=refs[:1] if missing == 'M' else refs)
    if missing == 'S':
        from cache_v2.index import CacheIndex
        source=prepared['selectors'][0]['score']
        index=CacheIndex(root/'results/cache_v2/index.sqlite')
        record=index.get_artifact(source['artifact_id'])
        (root/'results/cache_v2'/record['semantic_path']).unlink()  # Owned test store fault only.
    if missing == 'profile_selection':
        run(tables, 'small-profile', selector_refs=['profile.yaml'])
        # Parents have full-budget Selection, while P only has its short prefix.
        refs = profile_tables(tables, k=7)
        run(tables, 'large-parents', selector_refs=refs)
    if missing == 'parent_selection':
        profile_tables(tables, k=7)
    forbid_scores(monkeypatch)
    strict = missing in ('profile_score','profile_selection')
    changes = reference_config(tables) if strict else {}
    changes['selector_refs']=['profile.yaml']
    with pytest.raises(Exception, match='(?i)checkpoint MISS|missing|ScoreBundle producer|Selection producer'):
        run(tables, 'rejected', **changes)
    failed=json.loads((root/'results/runs/rejected/rejected/run.json').read_text(encoding='utf-8'))
    assert failed['status']=='failed'
    assert not list((root/'runtime/rejected').rglob('*.pt'))


def test_wrong_parent_identity_and_registered_conflict(tables, monkeypatch):
    from cache_v2 import ArtifactType
    from cache_v2.contracts import ArtifactConflictRecord
    from cache_v2.index import CacheIndex
    from experiments.modular_config import load_instance
    from experiments.modular_model import prepare_model
    from experiments.target_direct_v1.methods import Computations
    from experiments.target_direct_v1.recipe import build_recipe
    root=tables[0]; refs=profile_tables(tables)
    parents=run(tables,'prepared',selector_refs=refs,return_scores=True)['selectors']
    instance=load_instance(root/'profile.yaml','selector')
    data=pickle.loads((root/'graph.pkl').read_bytes())
    model, checkpoints, _=prepare_model(instance,data=data,dataset_name='cpu_fixture',
        checkpoint_root=root/'checkpoints',device='cpu',reference_directory=root,fail_if_training=True)
    options=dict(name=METHOD,computations=Computations(model,data,checkpoints),parameters=instance['parameters'],
        model_config=instance['model'],training=instance['training'],
        source_score=parents[0]['score'],matched_score=parents[1]['score'])
    build_recipe(**options)
    for parent in ('source_score','matched_score'):
        for field in ('recipe_hash','artifact_id','content_hash','recipe'):
            damaged=copy.deepcopy(options[parent]); damaged[field]='wrong'
            with pytest.raises(ValueError):
                build_recipe(**{**options,parent:damaged})
    for field in ('matching_seed','lissa'):
        changed=copy.deepcopy(instance['parameters'])
        if field=='matching_seed':changed[field]=55
        else:changed[field]['iterations']+=1
        with pytest.raises(ValueError):build_recipe(**{**options,'parameters':changed})
    changed=copy.deepcopy(instance['training']);changed['seed']+=1
    with pytest.raises(ValueError):build_recipe(**{**options,'training':changed})
    source=parents[1]['score']
    index=CacheIndex(root/'results/cache_v2/index.sqlite')
    # An explicit contradictory observation in this disposable Store, no repair.
    index.record_conflict(ArtifactConflictRecord(artifact_type=ArtifactType.SCORE,
        recipe_hash=source['recipe_hash'], observed_content_hash='0'*64,
        existing_artifact_id=source['artifact_id'],existing_content_hash=source['content_hash']))
    forbid_scores(monkeypatch)
    with pytest.raises(Exception,match='(?i)conflict'):
        run(tables,'conflicting',selector_refs=['profile.yaml'])


def test_prepared_profile_strict_references_none_final_to_gif(tables, monkeypatch, record_property):
    root,_,gu=tables; refs=profile_tables(tables)
    run(tables,'parents',selector_refs=refs)
    prepared=run(tables,'prepared-profile',selector_refs=['profile.yaml'])['selectors'][0]
    forbid_scores(monkeypatch)
    import experiments.modular_model as modeling
    original=modeling.train_supervised
    def only_ret(*args,**kwargs):
        if kwargs.get('epoch_end') is None:raise AssertionError('strict profile consumption retrained proxy')
        return original(*args,**kwargs)
    monkeypatch.setattr(modeling,'train_supervised',functools.wraps(original)(only_ret))
    config=reference_config(tables,('joint','none'));config['selector_refs']=['profile.yaml']
    result=run(tables,'strict-reference',**config)
    selected=result['selectors'][0]
    assert selected['checkpoint']['hit'] and selected['score']['hit'] and selected['selection']['cache']['hit']
    assert selected['selection']['artifact']==prepared['selection']['artifact']
    from experiments.modular_artifacts import read_run
    path=root/'results/runs/strict-reference/strict-reference/run.json'
    manifest,docs=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    none=json.loads(docs[1]['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0]
    weights=root/none['endpoints']['final']['weights']['path']
    write_yaml(root/'gif.yaml',{**gu,'method':'GIF','parameters':{},'training':{'seed':42},'checkpoint':str(weights)})
    result=run(tables,'profile-gif',stage='unlearning',selector_refs=['profile.yaml'],unlearning_refs=['gif.yaml'])
    gu_path=root/'results/runs/profile-gif/profile-gif/run.json'
    saved,_=read_run(gu_path,hashlib.sha256(gu_path.read_bytes()).hexdigest())
    assert saved['cells'][0]['cache_provenance']['original_checkpoint']['state_hash']==none['endpoints']['final']['state_hash']
    assert result['selectors'][0]['selection']['artifact']==prepared['selection']['artifact']
    record_property('strict_profile_consumer',json.dumps(dict(prepared_selection=prepared['selection']['artifact'],
        reference_run_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reference_cells=len(manifest['cells']),
        none_final=none['endpoints']['final']['state_hash'],gif_run_sha256=hashlib.sha256(gu_path.read_bytes()).hexdigest())))
