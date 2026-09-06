"""Ordinary tables retain scientific axes without generated configurations."""
from pathlib import Path
import pytest
from experiments.aagu015.definitions import CONFIG,dry_run
from experiments.modular_config import load_experiment,experiment_batches
from experiments.modular_run import execute


def test_all_ordinary_tables_no_write_or_producer(monkeypatch):
    import experiments.modular_run as entry
    def forbidden(*a,**k):raise AssertionError('dry-run crossed a runtime boundary')
    for name in ('read_dataset','prepare_model','resolve_methods'):
        monkeypatch.setattr(entry,name,forbidden)
    monkeypatch.setattr(Path,'mkdir',forbidden)
    result=dry_run()
    assert result['counts']=={'stage_s':306,'stage_u':612,'independent_retrain':306,
        'conditional_preparation_groups':9,'conditional_score_groups':141,'conditional_selection_groups':282}
    assert result['maintained_yaml']==12 and result['generated_yaml']==0
    assert not list((CONFIG/'generated').rglob('*.yaml'))
    assert {(r['dataset'],r['planned_k']) for r in result['stage_s']}=={
        ('Cora',18),('Cora',94),('CiteSeer',23),('CiteSeer',116),('PubMed',138),('PubMed',690)}


def test_declared_selection_stages_pair_training_seeds():
    for path in CONFIG.glob('stage_u_*.yaml'):
        config=load_experiment(path)
        assert len(config['selectors'])==17
        assert config['selector_refs']
        batches=list(experiment_batches(config))
        assert len(batches)==6
        for batch in batches:
            assert {i['training']['seed'] for i in batch['unlearnings']}=={batch['matrix_values']['training_seed']}
            assert len(batch['selectors'])==17
        assert execute(path,dry_run=True)['logical_cells']==204


def test_032_remains_42_conditions():
    plan=execute(CONFIG.parent/'aagu032/experiment.yaml',dry_run=True)
    assert plan['logical_cells']==42
