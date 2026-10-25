"""Read-only arithmetic audit of existing e79r6 evidence; no training or new tests."""
from pathlib import Path
import csv
import hashlib
import itertools
import json
import statistics

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PROFILE = ROOT / 'self/research/analyses/EXP-011_EXP-079/response_seed_profiles.csv'
PAIRED = ROOT / 'self/research/analyses/EXP-011_EXP-079/paired_vs_random.csv'


def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    with (HERE / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    profiles = [r for r in read(PROFILE) if r['experiment'] == 'EXP-079']
    key = lambda r: (r['dataset'], r['method'], r['source'], r['selector'], int(r['seed']))
    index = {key(r): r for r in profiles}
    assert len(index) == len(profiles)
    paired = [r for r in read(PAIRED) if r['experiment'] == 'EXP-079']
    effects = []
    max_error = 0.0
    for dataset, source in itertools.product(['Cora', 'CiteSeer', 'PubMed'], ['GCN', 'SGC', 'GAT', 'GIN']):
        requests = [r for r in profiles if r['dataset'] == dataset and r['method'] == 'GIF' and r['source'] == source and r['selector'] == 'r_point']
        assert len(requests) == 10
        out = dict(dataset=dataset, method='GIF', source=source, selector='r_point', n=10)
        for metric, label in [('after', 'delta_accuracy'), ('flip', 'delta_disagreement')]:
            values = [float(r[metric]) - float(index[(dataset, 'GIF', 'baseline', 'random', int(r['seed']))][metric]) for r in requests]
            mean = statistics.mean(values)
            old = [r for r in paired if (r['dataset'], r['method'], r['source'], r['selector'], r['metric']) == (dataset, 'GIF', source, 'r_point', metric)]
            assert len(old) == 1
            error = abs(mean - float(old[0]['mean']))
            assert error < 1e-10
            max_error = max(max_error, error)
            out.update({label + '_mean_pp': mean, label + '_sd_pp': statistics.stdev(values), label + '_existing_pointwise95_lo': float(old[0]['lo']), label + '_existing_pointwise95_hi': float(old[0]['hi'])})
        out['status'] = 'Existing exploratory pointwise intervals; no new confirmatory test or equivalence claim'
        effects.append(out)
    write('GIF_SOURCE_EFFECTS.csv', effects)

    interactions = []
    for dataset, source, metric, (left, right) in itertools.product(['Cora', 'CiteSeer', 'PubMed'], ['GCN', 'SGC', 'GAT', 'GIN'], ['U', 'flip'], itertools.combinations(['GIF', 'GraphEraser', 'GraphRevoker'], 2)):
        seeds = sorted(int(r['seed']) for r in profiles if (r['dataset'], r['method'], r['source'], r['selector']) == (dataset, left, source, 'r_point'))
        assert len(seeds) == 10
        values = []
        for seed in seeds:
            def value(method, selector):
                return float(index[(dataset, method, source, selector, seed)][metric])
            values.append((value(left, 'gt_full') - value(left, 'r_point')) - (value(right, 'gt_full') - value(right, 'r_point')))
        interactions.append(dict(dataset=dataset, source=source, metric=metric, method_left=left, method_right=right, contrast='(Dfull-Rpoint)_left - (Dfull-Rpoint)_right', n=10, mean_pp=statistics.mean(values), sd_pp=statistics.stdev(values), seed_values=json.dumps(dict(zip(seeds, values))), status='Outcome-disclosed descriptive clean-coordinate interaction; no p value/CI or preregistration claim'))
    assert len(interactions) == 72
    write('CLEAN_METHOD_SELECTOR_INTERACTIONS.csv', interactions)
    receipt = dict(scope='Existing EXP079 e79r6 scalar evidence; no raw model/selection reacceptance or scientific decision', inputs=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [PROFILE, PAIRED]], source_effect_rows=len(effects), existing_mean_assertions=24, max_mean_error=max_error, descriptive_interaction_rows=len(interactions), script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE / 'ARITHMETIC_AUDIT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    for row in effects:
        print(row['dataset'], row['source'], 'dAcc', round(row['delta_accuracy_mean_pp'], 3), 'dD', round(row['delta_disagreement_mean_pp'], 3))


if __name__ == '__main__':
    main()
