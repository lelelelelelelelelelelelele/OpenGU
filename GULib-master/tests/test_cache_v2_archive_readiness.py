import json

from cache_v2.archive_readiness import (
    build_archive_readiness_manifest,
    publish_archive_readiness_manifest,
)
from cache_v2.index import CacheIndex
from cache_v2.legacy_freeze import plan_or_freeze_legacy_caches
from scripts import cachectl


def _fixture(tmp_path):
    source = (tmp_path / "repo").resolve()
    results = source / "results"
    for name in ("cache", "selection_cache", "score_cache"):
        root = results / name
        root.mkdir(parents=True)
        (root / (name + ".bin")).write_bytes(name.encode("utf-8"))
    (source / "consumer.py").write_text(
        'cache = ResultCache("./results/cache")\n', encoding="utf-8"
    )
    index = CacheIndex((results / "cache_v2" / "index.sqlite").resolve())
    index.initialize()
    plan_or_freeze_legacy_caches(
        results, actor="maintainer", reason="fixture archive prep", apply=True
    )
    return source, results


def test_archive_manifest_separates_preparation_from_delete(tmp_path):
    source, results = _fixture(tmp_path)
    manifest = build_archive_readiness_manifest(results, source)
    assert manifest["legacy"]["total_files"] == 3
    assert manifest["freeze"]["state"] == "frozen"
    assert manifest["cache_v2"]["schema_ok"] is True
    assert manifest["consumer_refs"]["count"] == 1
    assert manifest["verdict"]["archive_preparation_complete"] is True
    assert manifest["verdict"]["physical_archive_authorized"] is False
    assert manifest["verdict"]["legacy_delete_ready"] is False
    assert manifest["rollback"]["legacy_payloads_moved"] is False


def test_archive_plan_dry_run_zero_write_and_apply_writes_manifest_only(tmp_path, capsys):
    source, results = _fixture(tmp_path)
    output = source / "evidence" / "archive-manifest.json"
    planned = publish_archive_readiness_manifest(results, source, output, apply=False)
    assert planned["writes"] == []
    assert not output.exists()

    args = [
        "legacy",
        "archive-plan",
        "--root",
        str(results),
        "--source-root",
        str(source),
        "--output",
        str(output),
        "--apply",
    ]
    assert cachectl.main(args) == 0
    response = json.loads(capsys.readouterr().out)
    assert response["writes"] == [str(output)]
    assert output.is_file()
    assert all((results / name).is_dir() for name in ("cache", "selection_cache", "score_cache"))
