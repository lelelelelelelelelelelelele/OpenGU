"""Effective computation identity; immutable historical Recipe hashes stay intact.

Only the explicitly owned source-code fields below are non-computational.
Data fingerprints, dependency references and actual state hashes are untouched.
"""
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from .contracts import ArtifactRecipe
from .errors import CacheResolutionError


def effective_fields(fields):
    result = deepcopy(dict(fields))
    for name in ("producer", "producer_version"):
        producer = result.get(name)
        if isinstance(producer, dict) and "source_fingerprint" in producer:
            producer["source_fingerprint"] = None
    return result


def computation_recipe(recipe):
    return ArtifactRecipe(effective_fields(recipe.fields), recipe_version=recipe.recipe_version)


def checkpoint_inputs(metadata):
    # These are the exact top-level fields emitted by the ordinary model,
    # trajectory and ensemble checkpoint producers. Never recursively strip keys.
    return {k: deepcopy(v) for k, v in metadata.items()
            if k not in ("implementation", "trajectory_implementation")}


def stored_recipe(record, requested=None):
    from .runtime import _decode_exact_mapping
    wrapper = _decode_exact_mapping(record["recipe"], "indexed Recipe")
    recipe = ArtifactRecipe(wrapper["fields"], recipe_version=wrapper["recipe_version"])
    if recipe.recipe_hash != record["recipe_hash"]:
        raise CacheResolutionError("indexed Recipe hash mismatch")
    if requested is not None and computation_recipe(recipe) != computation_recipe(requested):
        raise CacheResolutionError("effective computation inputs differ")
    return recipe


@lru_cache(maxsize=4)
def _effective_index(database, signature):
    # Rebuildable, process-local projection only. No on-disk migration or aliases.
    from .index import CacheIndex
    from .contracts import ArtifactType
    index = CacheIndex(database)
    groups = {}
    for kind in ArtifactType:
        for row in index.find_artifacts_by_type(kind):
            key = (kind.value, computation_recipe(stored_recipe(row)).recipe_hash)
            groups.setdefault(key, []).append(row)
    for rows in groups.values():
        rows.sort(key=lambda row: (row["created_at"], row["artifact_id"]))
    return groups


def matching_records(index, artifact_type, recipe):
    from .contracts import ArtifactType
    database = str(index.database_path.resolve())
    paths = [Path(database + suffix) for suffix in ("", "-wal")]
    signature = tuple((p.stat().st_mtime_ns, p.stat().st_size) if p.exists() else None for p in paths)
    key = (ArtifactType(artifact_type).value, computation_recipe(recipe).recipe_hash)
    return deepcopy(_effective_index(database, signature).get(key, []))
