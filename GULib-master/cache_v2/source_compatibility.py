"""Ordered, explicit source substitutions; storage and integrity remain producer-owned."""
from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path
from .contracts import ArtifactRecipe, ArtifactType
from .errors import CacheResolutionError, ContractValidationError


@lru_cache(maxsize=1)
def registry():
    data = json.loads(Path(__file__).with_name("source_compatibility.json").read_text(encoding="utf-8"))
    if set(data) != {"groups"} or not isinstance(data["groups"], list):
        raise ContractValidationError("source compatibility registry requires groups")
    allowed = {"source_fingerprint", "implementation", "trajectory_implementation"}
    for group in data["groups"]:
        if set(group) != {"cache_scope", "producer", "applies_to", "fingerprints", "reason", "evidence"}:
            raise ContractValidationError("invalid source compatibility group fields")
        if any(not isinstance(group[k], str) or not group[k] for k in ("cache_scope", "producer", "reason")):
            raise ContractValidationError("source compatibility scope, producer and reason are required")
        if not isinstance(group["applies_to"], dict) or not isinstance(group["evidence"], list) or not group["evidence"]:
            raise ContractValidationError("source compatibility conditions and evidence are required")
        members = group["fingerprints"]
        if not isinstance(members, list) or not members:
            raise ContractValidationError("source compatibility requires fingerprint members")
        for member in members:
            if not isinstance(member, dict) or not member or not set(member) <= allowed:
                raise ContractValidationError("invalid source fingerprint fields")
            if set(member) != set(members[0]) or any(not isinstance(v, str) or not v for v in member.values()):
                raise ContractValidationError("fingerprints must contain matching, nonempty source fields")
    return data["groups"]


def source_candidates(cache_scope, producer, context, current):
    """Current first; directly applicable groups in file order, without transitive expansion."""
    yield dict(current)
    seen = {tuple(sorted(current.items()))}
    for group in registry():
        if group["cache_scope"] != cache_scope or group["producer"] != producer:
            continue
        if any(context.get(k) != v for k, v in group["applies_to"].items()):
            continue
        if current not in group["fingerprints"]:
            continue
        for member in group["fingerprints"]:
            key = tuple(sorted(member.items()))
            if key not in seen:
                seen.add(key)
                yield dict(member)


def recipe_candidates(artifact_type, recipe):
    fields = recipe.fields
    slot = "producer_version" if "producer_version" in fields else "producer"
    source = fields.get(slot, {})
    scope = ArtifactType(artifact_type).value
    producer = fields.get("target", {}).get("method") or fields.get("selector")
    if producer is None:
        producer = ",".join(fields.get("score_names", [])) or source.get("semantic_version", "")
    model = fields.get("pairing", {}).get("model", fields.get("selector_model", {}))
    context = {"semantic_version": source.get("semantic_version"), "model": model}
    for member in source_candidates(scope, producer, context, {"source_fingerprint": source.get("source_fingerprint")}):
        updated = deepcopy(fields)
        if slot in updated:
            updated[slot].update(member)
        yield ArtifactRecipe(updated, recipe_version=recipe.recipe_version)


def stored_recipe(record, requested=None, artifact_type=None):
    from .runtime import _decode_exact_mapping
    wrapper = _decode_exact_mapping(record["recipe"], "indexed Recipe")
    recipe = ArtifactRecipe(wrapper["fields"], recipe_version=wrapper["recipe_version"])
    if recipe.recipe_hash != record["recipe_hash"]:
        raise CacheResolutionError("indexed Recipe hash mismatch")
    if requested is not None and not any(recipe == candidate for candidate in recipe_candidates(artifact_type, requested)):
        raise CacheResolutionError("indexed Recipe is not an allowed source candidate")
    return recipe


def checkpoint_candidates(metadata, scope="training_checkpoint"):
    current = {key: metadata[key] for key in ("implementation", "trajectory_implementation") if key in metadata}
    context = {"model": metadata.get("model"), "format": metadata.get("format")}
    producer = metadata.get("method", "supervised_training")
    for member in source_candidates(scope, producer, context, current):
        yield {**deepcopy(metadata), **member}
