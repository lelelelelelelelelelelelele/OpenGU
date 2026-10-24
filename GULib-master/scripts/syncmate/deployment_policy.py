"""One reviewed private deployment policy shared by install, preview and CLI."""
import hashlib
import json
from pathlib import Path

POLICY_PATH = Path('scripts/syncmate/deployment.json')
PRIVATE_POLICY = {'schema_version': 1, 'transport': 'private-bundle', 'require_origin_main': False}


def deployment_policy(root):
    path = Path(root) / POLICY_PATH
    if path.is_symlink() or not path.is_file():
        raise ValueError('reviewed deployment policy is missing or linked')
    raw = path.read_bytes()
    value = json.loads(raw.decode('utf-8'))
    if value != PRIVATE_POLICY or type(value.get('schema_version')) is not int or type(value.get('require_origin_main')) is not bool:
        raise ValueError('unsupported deployment policy')
    # Hash the reviewed policy object; Git checkout CRLF must not change its identity.
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return {**value, 'sha256': hashlib.sha256(canonical).hexdigest()}


def validate_receipt(result, target, policy, *, bundle_sha256=None):
    import re
    if not isinstance(result, dict):
        raise ValueError('installation receipt must be an object')
    if (result.get('target') != target or result.get('head') != target
            or result.get('status') not in ('installed', 'already_installed')
            or result.get('project') != '/autodl-fs/data/OpenGU/GULib-master'
            or result.get('transport') != policy['transport']
            or result.get('policy_sha256') != policy['sha256']
            or result.get('origin_refs_unchanged') is not True):
        raise ValueError('installation receipt is not successful for this target and private policy')
    if result['status'] == 'installed':
        actual = result.get('bundle_sha256') or ''
        if not re.fullmatch('[0-9a-f]{64}', actual) or (bundle_sha256 is not None and actual != bundle_sha256):
            raise ValueError('installation receipt lacks matching bundle identity')


def installation_receipt(root, target, policy):
    path = Path(root) / '.workblock/runtime/install' / target / 'receipt.json'
    if path.is_symlink() or not path.is_file():
        raise ValueError('exact private installation receipt is missing')
    result = json.loads(path.read_text(encoding='utf-8'))
    validate_receipt(result, target, policy)
    return {'path': str(path), 'target': target, 'status': result['status']}
