"""Calibrate explicit IF damping from a fixed checkpoint, without deletion/F1 access."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import torch
from torch_geometric.datasets import Planetoid
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from aagu052_local_if_debug import split_real_cora


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    opts=parser.parse_args()
    assert not opts.output.exists()
    assert (opts.data/'Cora/processed/data.pt').is_file()
    sys.argv=['calibrate_if_damping']
    torch.set_num_threads(2)
    from experiments.modular_model import create_model
    data=split_real_cora(Planetoid(str(opts.data),'Cora')[0],2024)
    data.num_classes=int(data.y.max())+1
    model=create_model(dict(architecture='OpenGU.GCNNet',layers=2,hidden_channels=8),'Cora',data,'cpu')
    model.load_state_dict(torch.load(opts.checkpoint,map_location='cpu',weights_only=True))
    model=model.double().eval();data.x=data.x.double()
    params=list(model.parameters());sizes=[p.numel() for p in params]
    out=model(data.x,data.edge_index)
    loss=torch.nn.functional.cross_entropy(out[data.train_mask],data.y[data.train_mask],reduction='sum')
    gradient=torch.autograd.grad(loss,params,create_graph=True)
    def mv(v):
        pieces=tuple(x.reshape_as(p) for x,p in zip(v.split(sizes),params))
        return torch.cat([g.flatten() for g in torch.autograd.grad(gradient,params,grad_outputs=pieces,retain_graph=True)]).detach()
    results=[]
    for seed in [173,941]:
        rng=torch.Generator().manual_seed(seed)
        q=torch.randn(sum(sizes),generator=rng,dtype=torch.double);q/=q.norm()
        basis=[];diagonal=[];off=[];prev=torch.zeros_like(q);beta=0.
        for step in range(80):
            basis.append(q);z=mv(q)-beta*prev;alpha=q@z;z-=alpha*q
            # Two-pass reorthogonalization prevents duplicate Ritz directions.
            for _ in range(2):
                for b in basis:z-=torch.dot(b,z)*b
            diagonal.append(float(alpha));new_beta=float(z.norm())
            if step==79 or new_beta<1e-12:break
            off.append(new_beta);prev,q=q,z/new_beta;beta=new_beta
        t=torch.diag(torch.tensor(diagonal,dtype=torch.double))
        if off:
            d=torch.tensor(off,dtype=torch.double);t+=torch.diag(d,1)+torch.diag(d,-1)
        eig,vectors=torch.linalg.eigh(t)
        residuals=[]
        for index in [0,-1]:
            vector=sum(b*c for b,c in zip(basis,vectors[:,index]));residuals.append(float((mv(vector)-eig[index]*vector).norm()))
        results.append(dict(seed=seed,steps=len(basis),minimum=float(eig[0]),maximum=float(eig[-1]),extreme_residuals=residuals))
    low=min(r['minimum'] for r in results);high=max(r['maximum'] for r in results)
    pow2=lambda x:2.**math.ceil(math.log2(x))
    mu=pow2(max(2*abs(min(low,0)),.01*high,1e-6))
    scale=pow2(high+mu)
    rho=max(abs(1-(low+mu)/scale),abs(1-(high+mu)/scale))
    steps=int(pow2(max(100,math.ceil(math.log(1e-5)/math.log(rho)))))
    assert steps<=16384
    n=int(data.train_mask.sum())
    result=dict(checkpoint=str(opts.checkpoint.resolve()),checkpoint_sha256=hashlib.sha256(opts.checkpoint.read_bytes()).hexdigest(),
        hessian='sum training cross-entropy, matching original IF data-loss convention',training_loss='mean CE + Adam coupled weight_decay=1e-6',
        training_count=n,regularizer_curvature_in_sum_units=n*1e-6,
        sum_loss=float(loss.detach()),mean_gradient_l2=float(torch.cat([g.detach().flatten() for g in gradient]).norm()/n),
        dtype='float64',lanczos=results,parameters=dict(iteration=steps,scale=scale,damp=mu/scale),mu=mu,
        estimated_shifted_min=low+mu,estimated_contraction=rho,
        limitation='Finite Lanczos estimates do not certify global positive definiteness; no deletion requests, F1 or result tuning used.')
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    opts.output.write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
