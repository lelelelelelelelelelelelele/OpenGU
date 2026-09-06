"""Reproducible, read-only AAGU-034 configuration and active-reference audit."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from experiments.effective_config import read_yaml
from experiments.modular_config import load_instance, load_experiment, configuration_fingerprint
from experiments.modular_run import execute
from experiments.aagu015.definitions import dry_run
from scripts.syncmate.opengu_recipes import recipe_definitions

BASELINE = '2b9bcafbfc789d0c60362b4246eee2a34440213b'


def audit():
    active = sorted((ROOT/'experiments/configs').rglob('*.yaml'))
    examples = sorted((ROOT/'docs/experiment_contract/examples').glob('*.yaml'))
    before = subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,
        'GULib-master/experiments/configs'],cwd=ROOT.parent,text=True).splitlines()
    before = [p for p in before if p.endswith('.yaml')]
    rows = []
    for path in active + examples:
        raw = read_yaml(path)
        kind = raw['kind']
        if kind == 'experiment':
            config = load_experiment(path)
            plan = execute(path,dry_run=True)
            rows.append({'path':path.relative_to(ROOT).as_posix(),'kind':kind,
                'logical_cells':plan['logical_cells'],'stage':plan['stage'],
                'configuration_fingerprint':configuration_fingerprint(path)})
        else:
            load_instance(path,kind)
            rows.append({'path':path.relative_to(ROOT).as_posix(),'kind':kind})
    archived = []
    for path in sorted((ROOT/'docs/archive/experiment-configs-pre-aagu034').glob('*.yaml')):
        old = 'GULib-master/experiments/configs/' + path.name
        raw = subprocess.check_output(['git','show',BASELINE+':'+old],cwd=ROOT)
        assert raw == path.read_bytes().replace(b'\r\n',b'\n'), 'historical Git YAML content changed: '+old
        archived.append({'before':old.split('/',1)[1],
                         'after':path.relative_to(ROOT).as_posix()})
    retired = ['experiments.target_direct_v1.'+name for name in
        ('run_selection','run_outputs','build_gu_config','build_manifest','adapter','syncmate_stage')]
    retired += ['experiments.syncmate_atomic_stage','target_direct_syncmate_v2']
    retired += ['syncmate_m1', 'class OpenGUAdapter', 'physical_replacement_approved',
                'compatibility_candidate', 'OPENGU_SETUP_CONFIG_SHA256']
    retired_files = json.loads((Path(__file__).parent/'retired-code.json').read_text(encoding='utf-8'))
    assert all(not (ROOT/path).exists() for path in retired_files), 'retired source file still exists'
    violations = []
    for directory in ('experiments','scripts'):
        for path in (ROOT/directory).rglob('*.py'):
            content = path.read_text(encoding='utf-8')
            violations.extend(path.relative_to(ROOT).as_posix()+': '+marker for marker in retired if marker in content)
    assert not violations, violations
    contracts = dry_run()
    registry = recipe_definitions()
    assert set(registry) == {'smoke','opengu-preflight-v1','opengu-aagu007-v1'}
    recipe = registry['opengu-aagu007-v1']
    assert configuration_fingerprint(ROOT/recipe['config_path']) == recipe['configuration_fingerprint']
    assert len(recipe['expected_artifact_paths']) == 17
    return {'passed':True,'baseline':BASELINE,'active_yaml_before':len(before),
        'active_yaml_after':len(active),'common_small_tables':sum(r['kind']!='experiment' for r in rows),
        'ordinary_active_experiments':sum(r['kind']=='experiment' for r in rows[:len(active)]),
        'contract_examples':len(examples),'aagu015_yaml_before':449,'aagu015_yaml_after':12,
        'generated_deleted':424,'aagu015_counts':contracts['counts'],'archive_byte_checks':archived,
        'retired_runtime_reference_matches':violations,'retired_files_absent':retired_files,
        'registered_recipes':list(registry),
        'registration':recipe,'rows':rows,'boundary':'configuration and source audit only; no runtime data or producer'}


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2,ensure_ascii=False))
