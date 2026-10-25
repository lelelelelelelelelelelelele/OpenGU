# EXP-014 · Paper appendix: request-generation cost

2026-10-25 · 用户确认纳入论文：正文一句指向附录，估计合入同一成本表并用脚注标明。

## Paper text and measured costs

On ogbn-arxiv (169,343 nodes), we use a random 70/10/20 split with seed 2024, rather than the official temporal split, and select 5,927 nodes from 118,540 training candidates (5%). R-point, D-full, and fixed-budget IM-RR with 4,096 and 16,384 samples produced complete requests with the required size, uniqueness, candidate membership, and input identity verified. IM uses selector seed 11 and propagation probability 0.1; D-full retains the gt_full GCN configuration and training seed 42. IM sampling and greedy coverage execute entirely on the CPU, without model training or GPU acceleration. R-point and D-full use the GPU for model/gradient computation and include CPU processing. These experiments evaluate request generation only; they contain no large-graph GU or retraining outcomes.

| Selector | Computation | Selector entry | Whole job (s) | Outcome |
| --- | --- | ---: | ---: | --- |
| R-point | GPU + CPU | 324.512 s | 364 | Completed |
| D-full | GPU + CPU | 2016.938 s | 2059 | Completed |
| IM-RR4096 | CPU only | 1316.066 s | 1365 | Completed |
| IM-RR16384 | CPU only | 6461.769 s | 6511 | Completed |
| IM-RR65536 | CPU only | 6–8 h (est.)* | 7202 | Timeout (2 h) |

* Estimated selector-entry completion time, extrapolated from measured ogbn-arxiv RR timings and small-graph replay tests (4 times as many samples took 4.33--4.37 times as long at the highest two tested budgets). The approximately 6--8 hours is not a measured completion or runtime bound; the observed run timed out after 2 hours. Exact scenarios and original timing boundaries are retained in the evidence report.

Selector-entry time includes current request access and verification; for R-point and D-full it also includes model preparation. Whole-job time is measured between Core start and finish and excludes queue and return. Successful IM runs invoked the Selection producer on a MISS; R-point and D-full had Checkpoint/Score/Selection MISS. The RR=65,536 run reached its 7,200-second limit without a complete trusted output; its 7,202-second wall includes termination overhead. RR=16,384 completed normally at 6,511 seconds, crossing the pre-agreed 6,480-second expansion-stop threshold. CPU model and thread allocation were not normalized; code/Core versions differ across runs. The table is not a controlled hardware or speedup comparison.

## Small-graph timing evidence

Existing small-graph tests recomputed sampling plus greedy selection for Cora, CiteSeer, and PubMed at four RR budgets and three selector seeds (11, 22, 33). These timings exclude graph loading/construction and cache access, and the replayed node sequences matched the verified selections. The small-graph deletion budget was 10%, versus 5% on ogbn-arxiv. From 16,384 to 65,536 samples, mean computation time increased by 4.33, 4.37, and 4.36 times, respectively. This is empirical support for approximately proportional growth over those tested budgets, not a universal scaling law. For fixed graph and sampling distribution, expected sampling work is additive in the number of samples; greedy/index operations and memory effects need not follow the same proportionality.

| Graph | RR1024 (s) | RR4096 (s) | RR16384 (s) | RR65536 (s) | Last-tier ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cora | 0.032 | 0.093 | 0.348 | 1.510 | 4.33 |
| CiteSeer | 0.024 | 0.106 | 0.290 | 1.265 | 4.37 |
| PubMed | 1.262 | 5.838 | 24.818 | 108.100 | 4.36 |

## Provenance and rebuild

[EXP-014 full report](../../../../self/research/experiments/drafts/EXP-014/REPORT.html) · [Frozen numbers](../../../../self/research/experiments/drafts/EXP-014/SUMMARY.json) · [36-condition raw timings](../../../../.workblock/items/AAGU-053/evidence/rr10-20260913/rr-condition-summary.csv)

原执行SHA、缓存、身份核验与源文件哈希沿EXP-014冻结数字保留。SHA256(SUMMARY.json): `9740692d1a306849a10cb1a32b963bfec00e311a5b2f5a98bcbd773eafd0dd76`.

由本目录 build.py 从冻结数字生成；HTML由同目录 build_report.ps1 生成。LaTeX片段为 sections/selector_cost.tex，估计合入原成本表并加脚注；原始产物、科学接纳和执行范围保持原记录。
