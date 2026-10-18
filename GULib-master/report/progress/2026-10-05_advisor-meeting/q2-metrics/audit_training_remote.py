"""Read-only final-checkpoint training fit; AUDIT supplied on stdin. No fitting."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import hashlib,json,sqlite3,sys,zipfile,subprocess
from pathlib import Path
ROOT=Path('/autodl-fs/data/OpenGU/GULib-master')
os.chdir(ROOT);sys.path.insert(0,str(ROOT))
import torch
from torch.nn import functional as F
torch.set_num_threads(2)
from experiments.dataset_inputs import resolve_input
from experiments.modular_model import create_model
from utils.target_checkpoint import load_weights,data_identity
con=sqlite3.connect((ROOT/'results/cache_v2/index.sqlite').as_uri()+'?mode=ro',uri=True)
con.row_factory=sqlite3.Row
rows=[]
def metrics(z,y):return dict(accuracy=float((z.argmax(-1)==y).double().mean())*100,ce=float(F.cross_entropy(z,y)))
for old in AUDIT['records']:
    if old['dataset']!='Cora' or old['method']!='GraphRevoker':continue
    ref=old['output'];db=dict(con.execute('select * from artifacts where artifact_id=?',(ref['artifact_id'],)).fetchone())
    assert all(db[k]==v for k,v in ref.items())
    p=ROOT/'results/cache_v2'/db['semantic_path']
    assert p.resolve().is_relative_to((ROOT/'results/cache_v2').resolve())
    assert hashlib.sha256(p.read_bytes()).hexdigest()==ref['content_hash']
    with zipfile.ZipFile(p) as z:identity=json.loads(z.read('metadata.json'))['identity']
    data=resolve_input(identity['dataset_input'],ROOT).cpu()
    assert data_identity(data)==identity['pairing']['data_identity']
    cp=Path(old['checkpoint'])
    assert cp.resolve().is_relative_to((ROOT/'results/runtime/modular/checkpoints').resolve())
    loaded=load_weights(cp)
    assert loaded['file_sha256']==old['checkpoint_file_sha256']
    assert loaded['state_hash']==old['initial_ensemble_state_hash']
    state=loaded['state_dict'];assignment=state['assignment'];model_cfg=old['checkpoint_metadata']['model']
    shards=[]
    with torch.inference_mode():
        for i in range(10):
            model=create_model(model_cfg,'shard',data,torch.device('cpu'))
            prefix=f'shard_models.{i}.'
            model.load_state_dict({k[len(prefix):]:v for k,v in state.items() if k.startswith(prefix)},strict=True);model.eval()
            allowed=(assignment==i)|(assignment<0);keep=allowed[data.edge_index[0]]&allowed[data.edge_index[1]]
            z=model(data.x,data.edge_index[:,keep]);mask=data.train_mask&(assignment==i)
            shards.append(dict(shard=i,train_nodes=int(mask.sum()),train=metrics(z[mask],data.y[mask]),
                test=metrics(z[data.test_mask],data.y[data.test_mask])))
        encoder=create_model(model_cfg,'graphrevoker',data,torch.device('cpu'));prefix='partition_encoder.'
        encoder.load_state_dict({k[len(prefix):]:v for k,v in state.items() if k.startswith(prefix)},strict=True);encoder.eval()
        z=encoder(data.x,data.edge_index)
        full=dict(train=metrics(z[data.train_mask],data.y[data.train_mask]),test=metrics(z[data.test_mask],data.y[data.test_mask]))
    rows.append(dict(seed=old['seed'],checkpoint_state_hash=loaded['state_hash'],checkpoint_file_sha256=loaded['file_sha256'],
        training=old['checkpoint_metadata']['training'],shards=shards,partition_encoder=full))
    print('checked training fit',old['seed'],file=sys.stderr,flush=True)
assert len(rows)==10
print(json.dumps(dict(kind='read-only final training fit',new_training_runs=0,
    remote_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
    original_execution_sha=AUDIT['execution_sha'],records=rows),indent=2))
