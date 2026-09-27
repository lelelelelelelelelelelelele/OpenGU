"""One immutable method output, including model state and evaluation inputs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
import numpy as np
from .contracts import ArtifactType
from .canonical import sha256_bytes
from .errors import ContractValidationError
from .store import ArtifactIntegrityError, _plain_json_bytes, _parse_canonical_plain_json
from .formal_artifacts import (
    _archive_bytes, _npy_bytes, _read_archive, _read_npy, ordered_int_hash,
)

OUTPUT_CONTRACT = 'opengu-node-unlearning-output-v2'
BASE_ARRAYS = frozenset(('logits', 'selected_nodes'))


@dataclass(frozen=True)
class UnlearningOutputPayload:
    identity: Mapping
    arrays: Mapping
    state: Mapping
    auxiliary: Mapping
    payload_version: int = 2

    artifact_type = ArtifactType.PREDICTION
    payload_schema = 'cache_v2.node_unlearning_output'
    contract_version = 2
    file_extension = 'npz'

    def __post_init__(self):
        if self.payload_version != 2:
            raise ContractValidationError('unknown unlearning output version')
        identity = _parse_canonical_plain_json(_plain_json_bytes(dict(self.identity)), 'output identity')
        if not BASE_ARRAYS <= set(self.arrays) or set(self.arrays) - BASE_ARRAYS - {'logits_before'}:
            raise ContractValidationError('unlearning output arrays are incomplete')
        if not self.state:
            raise ContractValidationError('unlearning output needs model state')
        for name in ('arrays', 'state', 'auxiliary'):
            values = {}
            for key, value in getattr(self, name).items():
                if not isinstance(key, str) or not key or '/' in key or '\\' in key:
                    raise ContractValidationError('invalid output tensor name')
                array = np.array(value, copy=True)
                if array.dtype.kind not in 'bifu' or not np.isfinite(array).all():
                    raise ContractValidationError('output tensors must be finite numeric arrays')
                array.setflags(write=False)
                values[key] = array
            object.__setattr__(self, name, values)
        a = self.arrays
        if 'dataset_input' not in identity:
            raise ContractValidationError('output requires an exact Dataset/Split reference')
        if a['logits'].ndim != 2:
            raise ContractValidationError('logits must be a matrix')
        n = a['logits'].shape[0]
        if 'logits_before' in a and a['logits_before'].shape != a['logits'].shape:
            raise ContractValidationError('before/after logits differ in shape')
        nodes = a['selected_nodes']
        if (nodes.dtype.kind not in 'iu' or nodes.ndim != 1 or len(nodes) == 0
                or len(np.unique(nodes)) != len(nodes) or (nodes < 0).any() or (nodes >= n).any()):
            raise ContractValidationError('invalid selected nodes')
        if nodes.tolist() != identity['pairing']['selected_nodes']:
            raise ContractValidationError('output request differs from pairing identity')
        if identity['target']['method'] != 'Retrain' and 'logits_before' not in a:
            raise ContractValidationError('GU output requires baseline logits')
        object.__setattr__(self, 'identity', identity)

    @property
    def graph_fingerprint(self):
        return self.identity['graph_fingerprint']

    @property
    def node_id_space(self):
        return 'pyg-global-node-index-v1'

    @property
    def metadata(self):
        return {'selected_nodes_hash': ordered_int_hash(self.arrays['selected_nodes'])}

    @property
    def dependencies(self):
        return (('selection_input', self.identity['selection']['artifact_id']),)

    @property
    def canonical_bytes(self):
        names = {group: sorted(getattr(self, group)) for group in ('arrays', 'state', 'auxiliary')}
        metadata = {'payload_version': 2, 'identity': self.identity, 'tensors': names}
        entries = [('metadata.json', _plain_json_bytes(metadata))]
        for group in ('arrays', 'state', 'auxiliary'):
            keys = names[group]
            entries.extend((group + '__' + key + '.npy', _npy_bytes(getattr(self, group)[key])) for key in keys)
        return _archive_bytes(entries)

    @property
    def content_hash(self):
        return sha256_bytes(self.canonical_bytes)

    @classmethod
    def from_bytes(cls, payload):
        import io
        import zipfile
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            metadata = _parse_canonical_plain_json(archive.read('metadata.json'), 'output metadata')
        names = metadata['tensors']
        expected = ['metadata.json'] + [group + '__' + key + '.npy' for group in ('arrays', 'state', 'auxiliary') for keys in [names[group]] for key in keys]
        members = _read_archive(payload, expected, 'unlearning output')
        groups = {group: {key: _read_npy(members[group + '__' + key + '.npy'], key) for key in keys}
                  for group in ('arrays', 'state', 'auxiliary') for keys in [names[group]]}
        result = cls(identity=metadata['identity'], payload_version=metadata['payload_version'], **groups)
        if result.canonical_bytes != payload:
            raise ArtifactIntegrityError('noncanonical unlearning output')
        return result

    def validate_against(self, recipe):
        if recipe.fields != {'artifact_contract': OUTPUT_CONTRACT, **self.identity}:
            raise ArtifactIntegrityError('unlearning output identity differs from Recipe')
