# CiteSeer / PubMed H64 Observer candidate tables

Status: generated and dry-run validated; Observer not executed; parameters not frozen.

Each dataset: GIF/IDEA x rho 0.8/0.5 x T=100/200/400 = 12 cells (24 total). Random seed=104245; budget=10% of train_mask; fixed H64 seed42 checkpoint. GU output cache disabled. Observers: linear_solver_trace, same_graph_change, hessian_calibration.

| Dataset | Method | rho | scale | damp (full precision) | mu | T |
|---|---|---:|---:|---:|---:|---|
| CiteSeer H64 | GIF | 0.8 | 23004 | 0.20094722036615764 | 4622.58985730309 | 100, 200, 400 |
| CiteSeer H64 | GIF | 0.5 | 36806 | 0.5005865852660731 | 18424.589857303086 | 100, 200, 400 |
| CiteSeer H64 | IDEA | 0.8 | 23004 | 0.20094722036615764 | 4622.58985730309 | 100, 200, 400 |
| CiteSeer H64 | IDEA | 0.5 | 36806 | 0.5005865852660731 | 18424.589857303086 | 100, 200, 400 |
| PubMed H64 | GIF | 0.8 | 173215 | 0.20037196190824003 | 34707.4293819358 | 100, 200, 400 |
| PubMed H64 | GIF | 0.5 | 277144 | 0.50023247619265 | 138636.4293819358 | 100, 200, 400 |
| PubMed H64 | IDEA | 0.8 | 173215 | 0.20037196190823992 | 34707.42938193578 | 100, 200, 400 |
| PubMed H64 | IDEA | 0.5 | 277144 | 0.50023247619265 | 138636.4293819358 | 100, 200, 400 |

## Evidence and identity

Original calculation source SHA: `501716bc30d59e39fa21d75c1f7af43a4ff47572`. CUDA, float64, Lanczos seeds 173/941, 80 steps each. Tool SHA-256: `7cedd9555642b5dea13215478e6b8dfc4c4bc4863f1f259e84d1ab882cb228b8`. Raw JSON includes data/split identity, checkpoint SHA/state hash, residuals and effective YAML. Receipts retain original collection paths; archived raw files are byte-for-byte copies.

H64 theory YAML now equals the actual effective input and directly references the audited cache. No paired-PT run was fabricated. H16 unchanged.

- [CiteSeer table](../../../experiments/configs/aagu067/observer_candidates_h64.yaml), [raw result](citeseer.json), [receipt](citeseer.receipt.json)
- [PubMed table](../../../experiments/configs/aagu068/observer_candidates_h64.yaml), [raw result](pubmed.json), [receipt](pubmed.receipt.json)
- [Generation manifest](generation.json), [verification](verification.json)

Finite Ritz estimates are not certified full-spectrum bounds. No training, Observer, retrain comparison, parameter freeze or scientific acceptance occurred. Dry-run validates configuration expansion, not remote launch readiness. Before execution, verify the recorded checkpoint SHA/state hash and dataset identity, then prepare/review a separate SyncMate Recipe and normal execution preflight.
