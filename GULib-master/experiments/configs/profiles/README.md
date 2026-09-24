# GIF/IDEA fixed-PT Parameter Profile

`gif_idea_fixed_pt.yaml` contains the frozen values used by these existing
multi-request validation cases (Random 104246/104247/104248, deletion ratio 0.1,
GIF/IDEA T=100/200/400 and one paired Retrain per request):

| Condition | Existing experiment YAML | Execution commit supplying the values |
| --- | --- | --- |
| Cora H16 | `experiments/configs/aagu066/validation_h16.yaml` | `b6f017987003ed8bef7d1c7284a80739e1c60792` |
| Cora H64 | `experiments/configs/aagu066/validation_h64.yaml` | `b6f017987003ed8bef7d1c7284a80739e1c60792` |
| CiteSeer H64 | `experiments/configs/aagu067/validation_h64.yaml` | `88e46cc66f95ae25e13c3eb40ea3f685f75cc6c4` |
| PubMed H64 | `experiments/configs/aagu068/validation_h64.yaml` | `88e46cc66f95ae25e13c3eb40ea3f685f75cc6c4` |

Each condition passed its 2026-09-24 multi-request numerical stability check.
This is not a claim of general stability or final scientific acceptance.
Keep the full recorded precision: GIF and IDEA damp values can differ slightly.
These values supersede the earlier Cora H16 R2 example. CiteSeer/PubMed H16 have
no mapping. Each condition is valid only with its independently calibrated fixed
checkpoint and Dataset/Split; matching by dataset and width is not scientific
authorization to transfer it to another checkpoint.

An experiment opts in with `parameter_profile_ref` relative to its own YAML.
Its GIF/IDEA method references retain `iteration`, model, training and checkpoint;
remove the fields supplied by the profile from those references. Supplying the
same field in both places is an error. Retrain is unaffected.

AAGU-077 verification uses the four existing tables as test inputs. Disposable
copies change only reference locations and the parameter source; normal
`experiments/run.py <yaml> --dry_run` output is compared against the original
inline configuration for all 84 cells. The canonical Item's
`evidence/four-condition/verify.py` retains this replay and its source snapshots.
Original calibration/validation YAML and historical execution recipes remain
the provenance of the completed experiments; this check submits no GPU work.
