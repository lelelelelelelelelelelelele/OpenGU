"""Read-only historical-cell audit for source-independent Cache V2 lookup.

Run in the active checkout against existing assets. Never computes, repairs,
retires or writes cache/index/run files. JSON output is an inspection artifact.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from cache_v2 import ArtifactRecipe, ArtifactResolver, ArtifactType, CacheIndex, ProducerVersion
from cache_v2.computation_identity import stored_recipe, matching_records
from cache_v2.runtime import _decode_exact_mapping
from experiments.artifact_producer import FormalArtifactRequest, materialize_formal_artifact


def audit(store_root, run_path):
    root, run_path = Path(store_root).resolve(), Path(run_path).resolve()
    run_bytes = run_path.read_bytes()
    run = json.loads(run_bytes)
    index = CacheIndex(root / 'index.sqlite')
    index.check_schema()
    before = hashlib.sha256(index.database_path.read_bytes()).hexdigest()
    resolver = ArtifactResolver(index)
    rows, samples, sampled = [], [], set()
    for cell in run['cells']:
        reference = cell.get('output', {})
        row = {'cell_id': cell['cell_id'], 'conditions': cell['conditions'], 'historical_output': reference}
        try:
            record = index.get_artifact(reference['artifact_id'])
            if any(record[key] != reference[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')):
                raise ValueError('historical output reference differs from index')
            recipe = stored_recipe(record)
            fields = recipe.fields
            producer = ProducerVersion(**{**fields['producer_version'], 'source_fingerprint': 'aagu086-read-only-consumer-probe'})
            fields['producer_version'] = producer.to_dict()
            request = FormalArtifactRequest(ArtifactType.PREDICTION, ArtifactRecipe(fields), producer)
            resolved = resolver.explain_exact(ArtifactType.PREDICTION, request.recipe)
            candidates = matching_records(index, ArtifactType.PREDICTION, request.recipe)
            row.update(status='reusable' if resolved.hit else 'conflict' if any('conflict' in r for r in resolved.miss_reasons) else 'invalid',
                       reasons=list(resolved.miss_reasons), candidates=[
                           {key: r[key] for key in ('artifact_id', 'recipe_hash', 'content_hash', 'created_at', 'status')} for r in candidates])
            method = cell['conditions']['method']
            if resolved.hit and method not in sampled:
                sampled.add(method)
                chosen = resolved.exact_candidate
                payload = root / chosen['semantic_path']
                header = payload.with_name('header.json')
                snapshot = [(p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest()) for p in (payload, header)]
                def forbidden():
                    raise AssertionError('producer must never execute during historical audit')
                result = materialize_formal_artifact(root, request, forbidden)
                after = [(p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest()) for p in (payload, header)]
                samples.append(dict(method=method, historical_id=reference['artifact_id'], consumed_id=result.artifact_id,
                    producer_called=result.producer_called, bytes_and_mtime_unchanged=snapshot == after,
                    generation_producer=result.result.generation_producer, consumption_producer=result.result.consumption_producer))
        except Exception as error:
            row.update(status='missing' if 'not found' in str(error).lower() else 'invalid', reasons=[type(error).__name__ + ': ' + str(error)])
        rows.append(row)
    # Different actual ensemble state remains a separate computation identity.
    revoker = []
    predictions = index.find_artifacts_by_type(ArtifactType.PREDICTION)
    for record in predictions:
        fields = stored_recipe(record).fields
        if fields.get('target', {}).get('method') == 'GraphRevoker':
            revoker.append({'artifact_id': record['artifact_id'], 'ensemble_state_hash': fields['target'].get('ensemble_state_hash'),
                            'created_at': record['created_at']})
    index_after = hashlib.sha256(index.database_path.read_bytes()).hexdigest()
    return {'run_path': str(run_path), 'run_sha256': hashlib.sha256(run_bytes).hexdigest(),
            'historical_commit': run.get('commit'), 'cell_count': len(rows), 'counts': dict(Counter(row['status'] for row in rows)),
            'index_sha256_before': before, 'index_sha256_after': index_after, 'index_unchanged': before == index_after,
            'samples': samples, 'cells': rows, 'graphrevoker_states': revoker,
            'retirement': {'eligible_artifact_ids': [], 'executed': False,
                'reason': 'No project-owned formal Artifact retire/unlink/GC writer exists. Different content and unproven job ownership block deletion; time windows alone are not authority.'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True)
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.store, args.run), ensure_ascii=False, indent=2))
