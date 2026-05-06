# §1 Introduction

> Status: outline
> Parent: §1
> Depends on: §3/§5 framing locked first
> Updated: 2026-05-05

## Content / Claim arc

- **Hook**: machine unlearning is now load-bearing for privacy compliance; approximate methods trade exactness for efficiency, and that approximation gap is exploitable.
- **Gap**: prior unlearning literature evaluates correctness *under benign deletion*. No systematic adversarial audit of approximate graph unlearning exists.
- **Contributions** (lock at end of writing):
  1. First systematic adversarial audit of 5 approximate GU methods × 3 mechanism families
  2. Selection toolkit (TracIn / IM / Hybrid) under explicit black-/grey-box access spectrum
  3. **Collateral Diagnostics** — retrain gap, prediction shift, novel hop-distance decay
  4. **Vulnerability Fingerprint** — 2D mechanism decomposition revealing per-family geometric structure (incl. counter-intuitive Shard Protection)
- **Roadmap** paragraph mirroring §2–§6.

## Evidence binding

- For "load-bearing": cite GDPR / right-to-be-forgotten + recent unlearning surveys
- For "exploitable" hook: forward-cite §5.1 Vulnerability Fingerprint figure

## Open questions

- **Q-1.1**: contribution ordering — methodology-first (current) vs finding-first (lead with Fingerprint)?
- Vision-graph framing retained from abstract or downplayed for NeurIPS?

## Cross-refs

- → §2 (related work gap)
- → §5.1 (headline finding)
