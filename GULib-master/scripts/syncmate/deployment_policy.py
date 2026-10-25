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
        'gpu4090-2': {'ssh': 'autodl-opengu-2', 'repo_path': '/autodl-fs/data/OpenGU/GULib-master'},
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
    if not isinstance(peer.get('python_executable'), str) or not peer['python_executable']:
        raise ValueError('registered node requires an explicit interpreter')
    return target


def dependency_pin(root):
    value = json.loads((Path(root) / 'scripts/syncmate/core_dependency.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    return value, digest


def receipt_path(root, node, target, policy):
    deployment_target(policy, node)
    if not isinstance(target, str) or not re.fullmatch('[0-9a-f]{40}', target):
        raise ValueError('full target Git identity required')
    return Path(root) / '.workblock/runtime/install' / node / target / 'receipt.json'


def validate_receipt(result, node, target, policy, *, expected_environment, bundle_sha256=None):
    registered = deployment_target(policy, node)
    if not isinstance(result, dict):
        raise ValueError('installation receipt must be an object')
    if (result.get('node') != node or result.get('ssh') != registered['ssh']
            or result.get('project') != registered['repo_path']
            or result.get('target') != target or result.get('head') != target
            or result.get('status') not in ('installed', 'already_installed')
            or result.get('transport') != policy['transport']
            or result.get('policy_sha256') != policy['sha256']
            or result.get('origin_refs_unchanged') is not True):
        raise ValueError('installation receipt is not successful for this node, target and private policy')
    observed = result.get('environment') or {}
    if (result.get('expected_environment') != expected_environment
            or observed.get('node_id') != node or observed.get('git_sha') != target
            or observed.get('requested_python') != expected_environment['python_executable']
            or observed.get('core_dependency_sha256') != expected_environment['core_dependency_sha256']
            or observed.get('core_payload_verified') is not True or not observed.get('python_executable')):
        raise ValueError('installation receipt does not verify this node environment')
    if result['status'] == 'installed':
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
    _, core_sha = dependency_pin(root)
    expected = {'python_executable': peer['python_executable'], 'core_dependency_sha256': core_sha}
    validate_receipt(result, node, target, policy, expected_environment=expected)
    return {'path': str(path), 'node': node, 'target': target, 'status': result['status']}


def execution_readiness(peer, definition):
    """The existing Core UI hook consumes the same selected-node credential."""
    from syncmate_core import context, identity, devices
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    project = context.current()
    try:
        device, warnings = devices.load_device(project.device_file)
        if warnings:
            raise ValueError('; '.join(warnings))
        matches = [node for node, registered in device.get('peers', {}).items() if registered == peer]
        if len(matches) != 1:
            raise ValueError('selected peer does not identify one registered node')
        node = context.validate_node_id(matches[0])
        policy = deployment_policy(project.root)
        proof = installation_receipt(project.root, node, identity.git_state()['sha'], policy, peer=peer)
        dependency = verify_core_dependency(pin_path=project.root / 'scripts/syncmate/core_dependency.json')
        return {'ready': dependency['ready'], 'errors': dependency['errors'],
                'node': node, 'installation_receipt': proof}
    except (ValueError, OSError, KeyError) as exc:
        return {'ready': False, 'errors': [str(exc)]}
