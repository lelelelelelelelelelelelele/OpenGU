# §3.1 Threat Model

> Status: outline (current draft `overleaf/sec/3_method.tex` L4–34)
> Parent: §3 Attack Framework
> Depends on: nothing (writeable now)
> Updated: 2026-05-05

## Content

- **Formalism** (keep current): graph $G=(V,E,X)$, classifier $f_\theta$, unlearning operator $\mathcal{U}(f_\theta,\mathcal{D}_{\mathrm{tr}},S)\to f_{\theta'}$
- **Attacker objective** Eq. (1) — argmax F1 drop subject to budget $|S|\le k = \lceil r|\mathcal{D}_{\mathrm{tr}}|\rceil$
- **NEW: Access Spectrum** — explicit table mapping each strategy to access requirements:

| Access | Information | Strategies in this paper |
|---|---|---|
| **Black-box** | only deletion API | random, degree, pagerank |
| **Grey-box** | + trained $f_\theta$, gradients, feature/structure access | tracin, im, hybrid |
| **White-box** | + modify training data / unlearning algorithm | **out of scope** (not realistic deletion-API threat) |

- **Reframe baselines**: random/degree/pagerank are no longer "weak baselines" — they are **black-box lower-bound attackers**. This raises their interpretive weight in §5.

## Evidence binding

- Existing draft: `overleaf/sec/3_method.tex` L7–34
- Coalition-of-users justification → forward link to §6.4 broader impact

## Open questions

- **Q-3.1.1**: access-spectrum format — table (clean, recommended) vs running prose (more compact)?
- **Q-3.1.2**: should we explicitly comment on "deletion-as-poisoning" framing from prior work and how grey-box differs?

## Cross-refs

- → §3.2 (each selector's access tier)
- → §5 (random as black-box reference line)
- → §6.3 (limitation: white-box not evaluated)
