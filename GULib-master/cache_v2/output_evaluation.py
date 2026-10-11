"""Complete measurements of exact Output v2 dependencies in the existing Store."""
from dataclasses import dataclass
from typing import Mapping

from .contracts import ArtifactType, validate_artifact_id, validate_sha256
from .errors import ContractValidationError
from .canonical import sha256_bytes
from .store import _plain_json_bytes, _parse_canonical_plain_json, ArtifactIntegrityError

OUTPUT_EVALUATION_CONTRACT = 'opengu-output-evaluation-v1'


@dataclass(frozen=True)
class OutputEvaluationPayload:
    identity: Mapping
    values: Mapping
    payload_version: int = 1

    artifact_type = ArtifactType.EVALUATION
    payload_schema = 'cache_v2.output_evaluation'
    contract_version = 1
    file_extension = 'json'

    def __post_init__(self):
        if self.payload_version != 1 or not self.values:
            raise ContractValidationError('invalid Output Evaluation payload')
        identity = _parse_canonical_plain_json(_plain_json_bytes(dict(self.identity)), 'evaluation identity')
        outputs = identity.get('outputs', [])
        if not outputs or len(outputs) > 2:
            raise ContractValidationError('Evaluation requires one or two exact Outputs')
        for output in outputs:
            ref = output['reference']
            if set(ref) != {'artifact_id', 'recipe_hash', 'content_hash'} or not validate_artifact_id(ref['artifact_id']).startswith('pred_'):
                raise ContractValidationError('Evaluation requires Cache V2 Output references')
            for key in ('recipe_hash', 'content_hash'):
                validate_sha256(ref[key], key)
            validate_sha256(output['identity']['graph_fingerprint'], 'graph_fingerprint')
        if len({o['reference']['artifact_id'] for o in outputs}) != len(outputs):
            raise ContractValidationError('duplicate Evaluation Output dependency')
        object.__setattr__(self, 'identity', identity)
        object.__setattr__(self, 'values', _parse_canonical_plain_json(_plain_json_bytes(dict(self.values)), 'evaluation values'))

    def to_dict(self):
        return dict(identity=dict(self.identity), values=dict(self.values), payload_version=self.payload_version)

    @property
    def canonical_bytes(self):
        return _plain_json_bytes(self.to_dict())

    @property
    def content_hash(self):
        return sha256_bytes(self.canonical_bytes)

    @property
    def dependencies(self):
        return tuple(('output_evaluation_input', o['reference']['artifact_id']) for o in self.identity['outputs'])

    @classmethod
    def from_bytes(cls, value):
        fields = _parse_canonical_plain_json(value, 'Output Evaluation')
        try:
            result = cls(**fields)
        except (TypeError, ValueError, KeyError) as exc:
            raise ArtifactIntegrityError('invalid Output Evaluation') from exc
        if result.canonical_bytes != value:
            raise ArtifactIntegrityError('noncanonical Output Evaluation')
        return result

    def validate_against(self, recipe):
        if (recipe.fields.get('artifact_contract') != OUTPUT_EVALUATION_CONTRACT
                or recipe.fields.get('evaluation_identity') != self.identity):
            raise ArtifactIntegrityError('Output Evaluation identity differs from Recipe')
