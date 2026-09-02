"""Typed Evaluation of a Selection-driven attack, without invented predictions.

Generic GU methods return aggregate metrics, not a PredictionPayload. This
contract records that actual dependency in the existing immutable V2 store.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .contracts import ArtifactRecipe, ArtifactType, validate_artifact_id, validate_sha256
from .errors import CacheV2Error, ContractValidationError
from .store import ArtifactIntegrityError, _plain_json_bytes, _parse_canonical_plain_json
from .canonical import sha256_bytes


ATTACK_EVALUATION_CONTRACT = "opengu-attack-evaluation-v1"


@dataclass(frozen=True)
class AttackEvaluationPayload:
    selection_artifact_id: str
    graph_fingerprint: str
    selected_nodes_hash: str
    metrics: Mapping[str, Any]
    payload_version: int = 1

    artifact_type = ArtifactType.EVALUATION
    payload_schema = "cache_v2.attack_evaluation"
    contract_version = 1
    file_extension = "json"

    def __post_init__(self):
        if self.payload_version != 1:
            raise ContractValidationError("unsupported attack Evaluation payload version")
        selection = validate_artifact_id(self.selection_artifact_id)
        if not selection.startswith("sel_"):
            raise ContractValidationError("attack Evaluation requires a Selection Artifact")
        validate_sha256(self.graph_fingerprint, "graph_fingerprint")
        validate_sha256(self.selected_nodes_hash, "selected_nodes_hash")
        if not isinstance(self.metrics, Mapping) or not self.metrics:
            raise ContractValidationError("attack Evaluation metrics must be non-empty")
        metrics = _parse_canonical_plain_json(_plain_json_bytes(dict(self.metrics)), "metrics")
        nodes = metrics.get("selected_nodes")
        if not isinstance(nodes, list) or sha256_bytes(_plain_json_bytes(nodes)) != self.selected_nodes_hash:
            raise ContractValidationError("attack Evaluation selected nodes do not match identity")
        if metrics.get("failed") is not False:
            raise ContractValidationError("failed attack results are not reusable evidence")
        object.__setattr__(self, "metrics", metrics)

    def to_dict(self):
        return {"payload_version": self.payload_version,
                "selection_artifact_id": self.selection_artifact_id,
                "graph_fingerprint": self.graph_fingerprint,
                "selected_nodes_hash": self.selected_nodes_hash,
                "metrics": dict(self.metrics)}

    @property
    def canonical_bytes(self):
        return _plain_json_bytes(self.to_dict())

    @property
    def content_hash(self):
        return sha256_bytes(self.canonical_bytes)

    @property
    def dependencies(self):
        return (("attack_selection_input", self.selection_artifact_id),)

    @classmethod
    def from_bytes(cls, payload):
        value = _parse_canonical_plain_json(payload, "attack Evaluation")
        try:
            result = cls(**value)
        except (CacheV2Error, TypeError, ValueError) as exc:
            raise ArtifactIntegrityError("invalid attack Evaluation payload") from exc
        if result.canonical_bytes != payload:
            raise ArtifactIntegrityError("attack Evaluation payload is not canonical")
        return result

    def validate_against(self, recipe: ArtifactRecipe):
        fields = recipe.fields
        if fields.get("artifact_contract") != ATTACK_EVALUATION_CONTRACT:
            raise ArtifactIntegrityError("attack Evaluation Recipe contract mismatch")
        for name in ("selection_artifact_id", "graph_fingerprint", "selected_nodes_hash"):
            if fields.get(name) != getattr(self, name):
                raise ArtifactIntegrityError("attack Evaluation identity mismatch: " + name)
