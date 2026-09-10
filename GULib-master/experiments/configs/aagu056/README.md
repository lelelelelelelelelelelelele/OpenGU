# AAGU-056 first Selector gate draft

`rr_1024.yaml` declares one topology-only IM RR condition on canonical ogbn-arxiv:
RR count 1024, propagation probability 0.1, IM seed 11, and 5% of the persisted
train-mask candidate pool. The existing consumer resolves actual K. No model
training, unlearning, retraining, or evaluation methods are declared.

## Pending Dataset/Split binding

The public reference `ogbn_arxiv.yaml` is reserved for
`experiments/configs/datasets/ogbn_arxiv.yaml`, which does not yet exist.
The experiment intentionally fails closed until that instance is bound to a
verified canonical arxiv manifest, its SHA-256, and actual split hash. Do not
invent hashes, substitute a Planetoid dataset, or download/rebuild data to fill
this reference. The formal data root is
`/autodl-fs/data/OpenGU/GULib-master/data/processed`.

Once the binding exists, validate through the ordinary launcher:

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu056/rr_1024.yaml --dry_run
```

This draft is not a runnable or accepted formal gate. Before launch, the same
WorkItem requires a Core recipe and independent run identity, a job timeout no
greater than 21600 seconds, numerical memory limits based on available SSH
resources, and formal code/device/data/cache preflight. Preserve existing caches
and report exact HIT separately from computation. Only after RR-1024 collection
and verification should RR-4096 be considered; RR-16384 follows that decision.

The canonical scope and acceptance contract remain in
`.workblock/items/AAGU-056/WORKITEM.md` in the canonical project.
