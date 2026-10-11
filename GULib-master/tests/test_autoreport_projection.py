from scripts.evaluation.reporting import summary
from scripts.evaluation.reporting import events as journal


def test_bounded_projection_preserves_history_order_and_total(monkeypatch):
    def event(cell, state, timestamp):
        return dict(cell_id=cell, run_id='run_' + cell, state=state,
                    timestamp=timestamp, stage='attack',
                    identity=dict(dataset=cell), metrics={})

    events = [event('old', 'started', '01'), event('old', 'failed', '03'),
              event('new', 'started', '02'), event('new', 'completed', '03'),
              event('hidden', 'completed', '00')]
    original = summary._cache_summary
    formatted = []

    def cache(group):
        formatted.append(group[-1]['cell_id'])
        return original(group)

    monkeypatch.setattr(summary, '_cache_summary', cache)
    rows, total = summary.build_status_rows(events, max_cells=2)
    assert total == 3
    assert [(row['cell_id'], row['state']) for row in rows] == [
        ('old', 'failed:attack'), ('new', 'attack-only')]
    assert formatted == ['old', 'new']


def test_projection_reuses_validated_append_but_observes_external_changes(tmp_path, monkeypatch):
    path = tmp_path / 'events.jsonl'
    journal.record_event(identity=dict(dataset='graph', model='GCN', method='MEGU', ratio=.1),
                         stage='attack', state='completed', producer='test',
                         config_fingerprint='config', git_sha='sha',
                         metrics={'F1': .75}, event_path=path, refresh=False)
    original = journal.read_event_stream
    reads = []

    def read(source):
        reads.append(source)
        return original(source)

    monkeypatch.setattr(journal, 'read_event_stream', read)
    options = dict(event_path=path, markdown_path=tmp_path/'view.md', html_path=tmp_path/'view.html')
    summary.write_status_views(**options)
    assert reads == []
    assert '0.75' in options['markdown_path'].read_text(encoding='utf-8')
    with path.open('a', encoding='utf-8') as handle:
        handle.write('broken external line\n')
    summary.write_status_views(**options)
    assert reads == [path.resolve()]
    assert 'Parse warnings: 1' in options['markdown_path'].read_text(encoding='utf-8')


def test_projection_uses_written_fact_after_caller_mutates_nested_data(tmp_path):
    path = tmp_path/'events.jsonl'
    event = journal.build_event(identity=dict(dataset='graph', model='GCN', method='MEGU', ratio=.1),
                                stage='attack', state='completed', producer='test',
                                config_fingerprint='config', git_sha='sha', metrics={'F1': .75},
                                metadata={'pair': ('tuple', {'value': 'original'})})
    journal.append_event(event, event_path=path, refresh=False)
    written, warnings = journal.read_event_stream(path)
    event['metrics']['F1'] = .99
    event['metadata']['pair'][1]['value'] = 'changed'
    projected, _ = journal._projection_events(path)
    assert not warnings and projected == written
    assert projected[0]['metrics'] == {'F1': .75}
    assert projected[0]['metadata']['pair'] == ['tuple', {'value': 'original'}]
