import itertools
import pytest
from experiments.modular_artifacts import ordered_execution_rows

@pytest.mark.parametrize('method', [None, 'retrain.yaml'])
def test_execution_order_does_not_change_condition_binding(method):
    rows=[];cells=[]
    for dataset,seed,budget in itertools.product(['Cora','PubMed'],[42,212],[.01,.15]):
        m=dict(dataset_name=dataset,training_seed=seed,budget_ratio=budget)
        for selector in ['degree.yaml','random.yaml']:
            c=dict(m,selector_ref=selector,unlearning_ref=method)
            cells.append({'conditions':c})
            rows.append(dict(matrix_values=m,selector_ref=selector,unlearning_ref=method,output=str(c)))
    executed=sorted(rows,key=lambda r:-r['matrix_values']['budget_ratio'])
    assert ordered_execution_rows(cells,executed)==rows
    assert ordered_execution_rows(cells,list(reversed(executed)))==rows
    with pytest.raises(ValueError):ordered_execution_rows(cells,executed[:-1])
    with pytest.raises(ValueError):ordered_execution_rows(cells,executed+[executed[0]])
    with pytest.raises(ValueError):ordered_execution_rows(cells+[cells[0]],executed)
