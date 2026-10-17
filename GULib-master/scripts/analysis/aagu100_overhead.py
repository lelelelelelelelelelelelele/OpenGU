"""AAGU-100: read collected evidence or profile disposable local persistence.

No experiment launcher, SSH, dataset, or production-cache access. Profiles are
synthetic CPU diagnostics, never formal performance or scientific results.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import cProfile
import hashlib
import json
import os
from pathlib import Path
import platform
import pstats
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze(source, destination):
    snapshot = read(source / "timing-audit-snapshot.json")
    prior = {r['run_id']: r for r in read(source / 'timing-breakdown.json')}
    result = {}
    for name, run_id in [('gif', 'e80r201'), ('idea', 'e80r202')]:
        path = source / f'{run_id}.run.json'
        run = read(path)
        assert run['status'] == 'completed' and run['run_id'] == run_id
        cells = run['cells']
        assert len(cells) == len({c['cell_id'] for c in cells}) == 882
        checked = 0
        duplicate_metrics = 0
        selected_counts = []
        with zipfile.ZipFile(source / f'{run_id}.cells.zip') as archive:
            for cell in cells:
                for filename, expected in cell['files'].items():
                    content = archive.read(cell['path'] + '/' + filename)
                    assert hashlib.sha256(content).hexdigest() == expected['sha256']
                    checked += 1
                    if filename == 'metrics.json':
                        metrics = {r['stage']: r['values'] for r in json.loads(content)['rows']}
                        duplicate_metrics += metrics['method'] == metrics['post_method_metrics']
                    elif filename == 'selection.json':
                        selection = json.loads(content)
                        selected_counts.append(len(selection.get('selected_nodes', [])))
                        assert selection['requested_k'] == len(selection['selected_nodes'])
        terminal = snapshot['totals'][run_id]['terminal']
        assert run['commit'] == terminal['git_sha']
        meta = terminal['metadata']
        phases = meta['phase_seconds_exclusive']
        grouped = defaultdict(list)
        for cell in cells:
            assert cell['status'] == 'completed'
            grouped[cell['conditions']['method']].append(cell)
        methods = {}
        for method, rows in grouped.items():
            cache = {k: dict(Counter(r['cache'].get(k, 'absent') for r in rows))
                     for k in sorted(set().union(*(r['cache'] for r in rows)))}
            producer = sum(r['timing'].get('method_compute_seconds', 0)
                           for r in rows if r['producer_called']['method'])
            methods[method] = dict(rows=len(rows), cache=cache,
                current_miss_producer_seconds=producer,
                unique_outputs=len({r['output']['artifact_id'] for r in rows}),
                unique_evaluations={key: len({r['cache_provenance']['evaluations'][key]['artifact_id']
                    for r in rows if key in r['cache_provenance'].get('evaluations', {})})
                    for key in ('post_method_metrics', 'post_unlearning_utility_and_retrain_gap', 'post_unlearning_flip_hop')})
            expected = prior[run_id]['current_miss_producer_seconds'].get(method, 0)
            assert abs(producer - expected) < 1e-6, (method, producer, expected)
        requests = {}
        for cell in cells:
            key = json.dumps({k: v for k, v in cell['conditions'].items()
                              if k not in ('method', 'unlearning_ref')}, sort_keys=True)
            if key in requests:
                assert requests[key]['selection_id'] == cell['selection_id']
            requests[key] = cell
        assert len(requests) == 441
        counter = snapshot['totals'][run_id]['counts']
        assert counter == {'run:started': 1, 'run:completed': 1,
            'selection:started': 441, 'selection:completed': 441,
            'attack:started': 882, 'attack:completed': 882,
            'evaluation:started': 5292, 'evaluation:completed': 5292}
        result[run_id] = dict(method=name.upper(), commit=run['commit'],
            rows=len(cells), requests=len(requests), methods=methods,
            axes={k: sorted({str(c['conditions'].get(k)) for c in cells}) for k in
                ('dataset_name', 'model', 'training_seed', 'budget_ratio', 'selector', 'im_selector_seed')},
            verified_cell_files=checked, exact_method_post_metric_matches=duplicate_metrics,
            selected_node_count_range=[min(selected_counts), max(selected_counts)],
            selection_cache=dict(Counter(c['cache']['selection'] for c in requests.values())),
            score_cache=dict(Counter(c['cache']['score'] for c in requests.values())),
            unique_selections=len({c['selection_id'] for c in requests.values()}),
            events=counter, execution_audit_calls=sum(counter.values())-2,
            native_wall_seconds=meta['wall_seconds'], core_job_seconds=prior[run_id]['job_seconds'],
            audit_seconds=meta['audit_seconds'], exclusive_phases=phases,
            exclusive_sum_seconds=sum(phases.values()),
            native_unattributed_seconds=meta['wall_seconds']-meta['audit_seconds']-sum(phases.values()),
            outside_native_wall_seconds=prior[run_id]['job_seconds']-meta['wall_seconds'],
            run_file_sha256=digest(path))
        assert result[run_id]['native_unattributed_seconds'] >= 0
    save(destination, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


@contextmanager
def measure_fsync():
    """Time the real fsync; retain its semantics, record calling site."""
    original = os.fsync
    calls = defaultdict(lambda: dict(calls=0, seconds=0.0))
    def measured(fd):
        frame = sys._getframe(1)
        key = f'{Path(frame.f_code.co_filename).name}:{frame.f_code.co_name}'
        started = time.perf_counter()
        try:
            return original(fd)
        finally:
            calls[key]['calls'] += 1
            calls[key]['seconds'] += time.perf_counter() - started
    os.fsync = measured
    try:
        yield calls
    finally:
        os.fsync = original


def measured(label, fn, *, profiling=True):
    profile = cProfile.Profile()
    with measure_fsync() as fsync:
        started = time.perf_counter()
        if profiling:
            profile.enable()
        value = fn()
        if profiling:
            profile.disable()
        elapsed = time.perf_counter() - started
    functions = []
    stats = pstats.Stats(profile).stats if profiling else {}
    for (filename, line, name), (primitive, calls, own, cumulative, _) in stats.items():
        try:
            filename = str(Path(filename).relative_to(ROOT))
        except ValueError:
            filename = Path(filename).name
        functions.append(dict(file=filename, line=line, function=name,
            calls=calls, primitive_calls=primitive, self_seconds=own, cumulative_seconds=cumulative))
    return dict(label=label, profiling=profiling, wall_seconds=elapsed, fsync=dict(fsync),
                functions=sorted(functions, key=lambda f: -f['cumulative_seconds']), result=value)


def audit_profiles(root):
    from scripts.evaluation.reporting import events
    results = []
    for size in (0, 13230, 26460):
        path = root / f'audit-{size}.jsonl'
        with path.open('x', encoding='utf-8', newline='\n') as handle:
            for i in range(size):
                event = events.build_event(identity=dict(dataset='synthetic', model='GCN', method='IDEA', ratio=.1, seed=i),
                    stage='evaluation', state='started', producer='AAGU-100 synthetic',
                    config_fingerprint='synthetic', git_sha='synthetic')
                handle.write(events._canonical_json(event) + '\n')
        serial = 0
        def append(count):
            nonlocal serial
            for _ in range(count):
                serial += 1
                common = dict(identity=dict(dataset='synthetic', model='GCN', method='IDEA', ratio=.1, seed=serial),
                    stage='evaluation', producer='AAGU-100 synthetic', config_fingerprint='synthetic',
                    git_sha='synthetic', event_path=path, refresh=False)
                run_id = events.new_run_id(events.make_cell_id(common['identity']))
                events.record_event(state='started', run_id=run_id, **common)
                events.record_event(state='completed', run_id=run_id, metrics={'accuracy': .8}, **common)
            return dict(events=2*count, file_bytes=path.stat().st_size)
        results.append(measured(f'audit history={size} cold first pair', lambda: append(1)))
        results.append(measured(f'audit history={size} warm 40 pairs', lambda: append(40)))
        # Simulate a legitimate external append by invalidating only this local cache.
        events._validated_streams.pop(path.resolve(), None)
        results.append(measured(f'audit history={size} cache-invalidated pair', lambda: append(1)))
    return results


def evaluation_profiles(root):
    from cache_v2 import ArtifactRecipe, ArtifactType, ArtifactStatus, CacheIndex, ProducerVersion
    from cache_v2.contracts import ArtifactHeader, VerificationStatus
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from cache_v2.output_evaluation import OUTPUT_EVALUATION_CONTRACT, OutputEvaluationPayload
    from experiments.artifact_producer import FormalArtifactRequest
    from experiments.evaluation_cache import cached_measurements
    producer = ProducerVersion('aagu100-synthetic-local')
    results = []
    for size in (100, 1000, 10000):
        store = root / f'evaluation-{size}'
        index = CacheIndex(store / 'index.sqlite')
        index.initialize()
        outputs = []
        for method in ('IDEA', 'Retrain'):
            identity = dict(graph_fingerprint='a'*64, target={'method':method},
                pairing={'selected_nodes':list(range(size))}, producer_version=producer.to_dict())
            recipe = ArtifactRecipe(dict(artifact_contract=OUTPUT_CONTRACT, **identity))
            header = ArtifactHeader(artifact_type=ArtifactType.PREDICTION, recipe=recipe,
                content_hash=hashlib.sha256(method.encode()).hexdigest(), producer_version=producer, status=ArtifactStatus.VALID,
                verification_status=VerificationStatus.VERIFIED, semantic_path=f'synthetic/{method}.npz')
            # Synthetic metadata fixture. No prediction bytes: the Evaluation admission
            # contract checks exact registered metadata without consuming parent NPZ.
            index.register_artifact(header)
            outputs.append(dict(reference=dict(artifact_id=header.artifact_id,
                recipe_hash=header.recipe_hash, content_hash=header.content_hash), identity=identity))
        with index.read_session(), index.write_session():
            for parents in (1, 2):
                for repeat in range(6):
                    identity = dict(case=f'synthetic-{parents}-{repeat}', outputs=outputs[:parents])
                    request = FormalArtifactRequest(ArtifactType.EVALUATION, ArtifactRecipe(dict(
                        artifact_contract=OUTPUT_EVALUATION_CONTRACT, evaluation_identity=identity,
                        producer_version=producer.to_dict())), producer)
                    def access():
                        values, cache = cached_measurements(request, store, lambda: {'synthetic_metric':.8})
                        return dict(hit=cache['hit'], artifact_id=cache['artifact_id'], values=values)
                    results.append(measured(f'evaluation nodes={size} parents={parents} repeat={repeat} MISS', access, profiling=repeat<3))
                    def hit():
                        def forbidden():
                            raise AssertionError('HIT called producer')
                        values, cache = cached_measurements(request, store, forbidden)
                        return dict(hit=cache['hit'], artifact_id=cache['artifact_id'], values=values)
                    results.append(measured(f'evaluation nodes={size} parents={parents} repeat={repeat} HIT', hit, profiling=repeat<3))
                    assert results[-1]['result']['hit'] and not results[-2]['result']['hit']
                    assert results[-1]['result']['artifact_id'] == results[-2]['result']['artifact_id']
    return results


def profile(root, destination):
    root.mkdir(parents=True, exist_ok=False)
    result = dict(environment=dict(python=sys.version, platform=platform.platform(),
        executable=sys.executable, source=str(ROOT), temporary_root=str(root)),
        limitations='Synthetic local CPU fixtures; cProfile overhead included; timings cannot be attributed to formal GPU runs. Python fsync wrapper excludes SQLite internal synchronization. Parent fixtures are metadata-only, no scientific outputs.',
        audit=audit_profiles(root))
    save(destination, result)
    try:
        result['evaluation'] = evaluation_profiles(root)
    except Exception as exc:
        result['error'] = repr(exc)
        save(destination, result)
        raise
    save(destination, result)
    for group in ('audit', 'evaluation'):
        for row in result[group]:
            print(row['label'], round(row['wall_seconds'], 6), 'fsync', row['fsync'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    analyze_parser = sub.add_parser('analyze')
    analyze_parser.add_argument('--source', type=Path, required=True)
    analyze_parser.add_argument('--output', type=Path, required=True)
    profile_parser = sub.add_parser('profile')
    profile_parser.add_argument('--temporary-root', type=Path, required=True)
    profile_parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.mode == 'analyze':
        analyze(args.source.resolve(), args.output.resolve())
    else:
        profile(args.temporary_root.resolve(), args.output.resolve())
