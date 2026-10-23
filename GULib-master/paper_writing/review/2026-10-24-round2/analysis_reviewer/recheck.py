"""Read-only descriptive checks for the simulated round-2 analysis review.

Inputs are existing local derived tables. This script does not run training,
change experiment state, or validate scientific correctness of cached outputs.
"""
from pathlib import Path
import hashlib
import json

import pandas as pd

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
AUDIT = ROOT / "paper_writing/review/2026-10-24-self-audit"
FIXED = ROOT / "self/research/analyses/EXP-011_EXP-079/cells.csv"
FILES = {
    "interactions": AUDIT / "analysis/gu_retrain_strategy_interactions.csv",
    "contrasts": AUDIT / "analysis/source_strategy_contrasts.csv",
    "budget_seed": AUDIT / "analysis/budget_random_seed_contrasts.csv",
    "hop_cells": AUDIT / "inventory/hop_cells.csv",
    "hop_seed": AUDIT / "inventory/hop_seed_values.csv",
    "fixed_cells": FIXED,
}

inter = pd.read_csv(FILES["interactions"])
primary = inter[inter.contrast.eq("gt_full-minus-r_point")].copy()
contrasts = pd.read_csv(FILES["contrasts"])
contrasts = contrasts[
    contrasts.contrast.eq("gt_full-minus-r_point")
    & contrasts.metric.eq("accuracy_delta")
]
ret = contrasts[contrasts.method.eq("Retrain")][["dataset", "source", "lo", "hi"]]
ret = ret.rename(columns={"lo": "ret_lo", "hi": "ret_hi"})
joint = contrasts[contrasts.method.ne("Retrain")].merge(ret, on=["dataset", "source"])
joint["opposite_pointwise_intervals"] = (
    (joint.hi.lt(0) & joint.ret_lo.gt(0))
    | (joint.lo.gt(0) & joint.ret_hi.lt(0))
)
joint.to_csv(OUT / "family_endpoint_intervals.csv", index=False, encoding="utf-8")

family = []
for name, part in [("all_six_GU", primary), ("exclude_IDEA", primary[primary.method.ne("IDEA")])]:
    family.append({
        "display_scope": name,
        "conditions": len(part),
        "opposite_mean_ordering": int(part.opposite_mean_ordering.sum()),
        "all_ten_seed_opposite": int(part.opposite_seed_ordering_count.eq(10).sum()),
        "at_least_eight_seed_opposite": int(part.opposite_seed_ordering_count.ge(8).sum()),
        "negative_pointwise_interaction_interval": int(part.hi.lt(0).sum()),
    })

cells = pd.read_csv(FILES["fixed_cells"])
cells = cells[cells.experiment.eq("EXP-079") & cells.method.eq("Retrain")]
identities = cells.groupby(["dataset", "source", "selector"], as_index=False).agg(
    rows=("selection_id", "size"),
    unique_selection_ids=("selection_id", "nunique"),
    seeds=("seed", "nunique"),
)
identities.to_csv(OUT / "selection_identity_counts.csv", index=False, encoding="utf-8")

budget = pd.read_csv(FILES["budget_seed"])
budget = budget[
    budget.method.ne("Retrain") & budget.selector.isin(["r_point", "degree"])
    & budget.ratio.isin([0.05, 0.33])
]
direct = budget.pivot(index=["dataset", "method", "seed", "ratio"], columns="selector", values="disagreement").reset_index()
direct["rpoint_minus_degree_D_pp"] = direct.r_point - direct.degree
change = direct.pivot(index=["dataset", "method", "seed"], columns="ratio", values="rpoint_minus_degree_D_pp").reset_index()
change = change.rename(columns={0.05: "difference_5pct_pp", 0.33: "difference_33pct_pp"})
change["change_pp"] = change.difference_33pct_pp - change.difference_5pct_pp
change["scope_note"] = change.method.map({
    "GIF": "nonshard; IDEA outputs are near duplicates in this profile",
    "IDEA": "nonshard; near-duplicate GIF coordinate, not independent confirmation",
    "MEGU": "nonshard; evaluated pipeline includes C&S",
    "GNNDelete": "quarantined from current claims; main-case test-mask selection traced separately; remaining scope under audit",
    "GraphEraser": "historical EXP080 shard protocol",
    "GraphRevoker": "historical EXP080 shard variant",
})
change.to_csv(OUT / "rpoint_degree_budget_seed.csv", index=False, encoding="utf-8")
budget_summary = change.groupby(["dataset", "method", "scope_note"], as_index=False).agg(
    mean_difference_5pct_pp=("difference_5pct_pp", "mean"),
    mean_difference_33pct_pp=("difference_33pct_pp", "mean"),
    mean_change_pp=("change_pp", "mean"), sd_change_pp=("change_pp", "std"),
    positive_seeds=("change_pp", lambda v: int(v.gt(0).sum())),
    negative_seeds=("change_pp", lambda v: int(v.lt(0).sum())),
    seeds=("seed", "size"),
)
budget_summary.to_csv(OUT / "rpoint_degree_budget_summary.csv", index=False, encoding="utf-8")

hop = pd.read_csv(FILES["hop_cells"])
hop = hop[
    hop.experiment.eq("EXP-011") & hop.dataset.eq("Cora")
    & hop.selector.isin(["r_point", "rr_65536"])
]
cell_totals = hop.drop_duplicates("cell_id").copy()
cell_totals["overall_D_pct"] = 100 * cell_totals.test_disagreements / cell_totals.test_nodes
# Average request draws within training seed, then give each seed equal weight.
totals = cell_totals.groupby(["method", "selector", "seed"], as_index=False).overall_D_pct.mean()
totals = totals.groupby(["method", "selector"], as_index=False).overall_D_pct.mean()
hop_seed = pd.read_csv(FILES["hop_seed"])
hop_seed = hop_seed[
    hop_seed.experiment.eq("EXP-011") & hop_seed.dataset.eq("Cora")
    & hop_seed.selector.isin(["r_point", "rr_65536"])
]
hop_summary = hop_seed.groupby(["method", "selector", "band"], as_index=False)[["rate_pct", "mean_node_share_pct"]].mean()
hop_summary = hop_summary.merge(totals, on=["method", "selector"])
hop_summary["GNNDelete_excluded_from_current_claims"] = hop_summary.method.eq("GNNDelete")
hop_summary.to_csv(OUT / "hop_composition_example.csv", index=False, encoding="utf-8")

facts = {
    "scope": "Simulated review; descriptive checks of existing derived outputs only.",
    "not_independent_replications": "Source/method conditions and intervals share endpoints; frequency is a finite-suite description, not an estimated population probability.",
    "all_interaction_rows": len(inter),
    "family": family,
    "opposite_marginal_pointwise_intervals_count": int(joint.opposite_pointwise_intervals.sum()),
    "all_ten_seed_opposite_conditions": primary[primary.opposite_seed_ordering_count.eq(10)][["dataset", "method", "source"]].to_dict(orient="records"),
    "random_free_degree_comparison": budget_summary.to_dict(orient="records"),
    "hop_example": hop_summary.to_dict(orient="records"),
    "input_sha256": {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in FILES.items()},
}
(OUT / "checks.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"family": family, "budget": facts["random_free_degree_comparison"], "output": str(OUT)}, ensure_ascii=False, indent=2))
