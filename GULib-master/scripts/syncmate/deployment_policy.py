"""Reviewed private deployment targets shared by install, preview and CLI."""
import hashlib
import json
import re
from pathlib import Path

POLICY_PATH = Path('scripts/syncmate/deployment.json')
PRIVATE_POLICY = {
    'schema_version': 2, 'transport': 'private-bundle', 'require_origin_main': False,
    'targets': {
        'gpu4090': {'ssh': 'autodl-opengu', 'repo_path': '/autodl-fs/data/OpenGU/GULib-master'},
        'gpu4090-2': {'ssh': 'autodl-opengu-2', 'repo_path': '/autodl-fs/data/OpenGU-2/GULib-master'},
    },
}


def deployment_policy(root):
    path = Path(root) / POLICY_PATH
    if path.is_symlink() or not path.is_file():
        raise ValueError('reviewed deployment policy is missing or linked')
    value = json.loads(path.read_text(encoding='utf-8'))
    if (value != PRIVATE_POLICY or type(value.get('schema_version')) is not int
            or type(value.get('require_origin_main')) is not bool):
        raise ValueError('unsupported deployment policy')
    canonical = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return {**value, 'sha256': hashlib.sha256(canonical).hexdigest()}


def deployment_target(policy, node):
    target = policy.get('targets', {}).get(node)
    if not isinstance(target, dict):
        raise ValueError('select a registered deployment node')
    return target


def validate_peer(peer, node, policy):
    target = deployment_target(policy, node)
    if (not isinstance(peer, dict) or peer.get('transport', 'ssh') != 'ssh'
            or peer.get('role', 'runner') not in ('runner', 'runner+collector')
            or peer.get('ssh') != target['ssh'] or peer.get('repo_path') != target['repo_path']):
        raise ValueError('device peer does not match the registered node alias and project')
    return target


def receipt_path(root, node, target, policy):
    deployment_target(policy, node)
    if not isinstance(target, str) or not re.fullmatch('[0-9a-f]{40}', target):
        raise ValueError('full target Git identity required')
    return Path(root) / '.workblock/runtime/install' / node / target / 'receipt.json'


def validate_receipt(result, node, target, policy, *, bundle_sha256=None):
    registered = deployment_target(policy, node)
    if not isinstance(result, dict):
        raise ValueError('installation receipt must be an object')
    if (result.get('node') != node or result.get('ssh') != registered['ssh']
            or result.get('project') != registered['repo_path']
            or result.get('target') != target or result.get('head') != target
            or result.get('status') not in ('initialized', 'installed', 'already_installed')
            or result.get('transport') != policy['transport']
            or result.get('policy_sha256') != policy['sha256']
            or result.get('origin_refs_unchanged') is not True):
        raise ValueError('installation receipt is not successful for this node, target and private policy')
    if result['status'] in ('initialized', 'installed'):
        actual = result.get('bundle_sha256') or ''
        if (not isinstance(actual, str) or not re.fullmatch('[0-9a-f]{64}', actual)
                or (bundle_sha256 is not None and actual != bundle_sha256)):
            raise ValueError('installation receipt lacks matching bundle identity')


def installation_receipt(root, node, target, policy, *, peer):
    validate_peer(peer, node, policy)
    path = receipt_path(root, node, target, policy)
    if path.is_symlink() or not path.is_file():
        raise ValueError('exact node private installation receipt is missing')
    result = json.loads(path.read_text(encoding='utf-8'))
    validate_receipt(result, node, target, policy)
    return {'path': str(path), 'node': node, 'target': target, 'status': result['status']}
