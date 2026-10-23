"""Read-only reanalysis of verified paper inputs; never runs GU or edits records.

Outputs are descriptive, exploratory training-seed contrasts. No hypothesis
family is selected after seeing a p-value; no new p-values are produced.
Pointwise t intervals use df=2 or df=9 and do not establish equivalence.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
FIXED = ROOT / "self/research/analyses/EXP-011_EXP-079"
BUDGET = ROOT / "self/research/analyses/EXP-080/full-20261021"
T_CRIT = {3: 4.302652729749464, 10: 2.2621571628540993}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stats(values):
    values = [float(v) for v in values if pd.notna(v)]
    n = len(values)
    if not n:
        return dict(n=0, mean=None, sd=None, lo=None, hi=None,
                    positive=None, negative=None)
    assert n in T_CRIT, n
    avg = statistics.mean(values)
    sd = statistics.stdev(values)
    half = T_CRIT[n] * sd / math.sqrt(n)
    return dict(n=n, mean=avg, sd=sd, lo=avg-half, hi=avg+half,
                positive=sum(v > 1e-10 for v in values),
                negative=sum(v < -1e-10 for v in values))


def write_csv(name, rows):
    pd.DataFrame(rows).to_csv(OUT / name, index=False, encoding="utf-8")


manifest = json.loads((FIXED / "derived_data_hashes.json").read_text(encoding="utf-8"))
checks = {}
for name in ["seed_values.csv", "cells.csv", "paired_seed_values.csv"]:
    checks[str((FIXED / name).relative_to(ROOT))] = sha(FIXED / name)
    assert checks[str((FIXED / name).relative_to(ROOT))] == manifest[name], name
budget_proof = json.loads((BUDGET / "statistics_validation.json").read_text(encoding="utf-8"))
checks[str((BUDGET / "cells.csv").relative_to(ROOT))] = sha(BUDGET / "cells.csv")
assert sha(BUDGET / "cells.csv") == budget_proof["input_sha256"]

# 079: use all data sets, sources and methods; baseline source is shared.
seed = pd.read_csv(FIXED / "seed_values.csv")
fixed = seed[seed.experiment.eq("EXP-079")].copy()
assert not fixed.duplicated(["dataset", "method", "source", "selector", "seed"]).any()
fixed_raw = pd.read_csv(FIXED / "cells.csv")
fixed_raw = fixed_raw[fixed_raw.experiment.eq("EXP-079")]
assert len(fixed_raw) == 2520
contrast_seeds = []
for (ds, method), sub in fixed.groupby(["dataset", "method"]):
    for src in ["GCN", "SGC", "GAT", "GIN"]:
        conditions = {sel: sub[sub.selector.eq(sel) & sub.source.eq(src)].set_index("seed")
                      for sel in ["gt_full", "r_point"]}
        conditions.update({sel: sub[sub.selector.eq(sel)].set_index("seed")
                           for sel in ["degree", "random"]})
        assert all(len(part) == 10 for part in conditions.values())
        for a, b in [("gt_full", "r_point"), ("gt_full", "degree"),
                     ("r_point", "degree")]:
            joined = conditions[a].join(conditions[b], lsuffix="_a", rsuffix="_b", how="inner")
            assert len(joined) == 10
            for training_seed, row in joined.iterrows():
                contrast_seeds.append(dict(dataset=ds, method=method, source=src,
                    contrast=f"{a}-minus-{b}", seed=int(training_seed),
                    accuracy_delta=row.after_a-row.after_b,
                    disagreement_delta=row.flip_a-row.flip_b))
contrasts = pd.DataFrame(contrast_seeds)
summary = []
for keys, group in contrasts.groupby(["dataset", "method", "source", "contrast"]):
    base = dict(zip(["dataset", "method", "source", "contrast"], keys))
    for metric in ["accuracy_delta", "disagreement_delta"]:
        summary.append(dict(**base, metric=metric, **stats(group[metric])))
write_csv("source_strategy_seed_contrasts.csv", contrast_seeds)
write_csv("source_strategy_contrasts.csv", summary)

# Difference-in-differences: GU selector ordering minus matched Retrain ordering.
ret = contrasts[contrasts.method.eq("Retrain")][["dataset", "source", "contrast", "seed", "accuracy_delta"]]
ret = ret.rename(columns={"accuracy_delta": "retrain_delta"})
inter = contrasts[~contrasts.method.eq("Retrain")].merge(ret,
    on=["dataset", "source", "contrast", "seed"], validate="many_to_one")
inter["interaction"] = inter.accuracy_delta-inter.retrain_delta
inter_summary = []
for keys, group in inter.groupby(["dataset", "method", "source", "contrast"]):
    item = dict(zip(["dataset", "method", "source", "contrast"], keys))
    item.update(stats(group.interaction))
    item["gu_delta_mean"] = group.accuracy_delta.mean()
    item["retrain_delta_mean"] = group.retrain_delta.mean()
    item["opposite_mean_ordering"] = bool(item["gu_delta_mean"]*item["retrain_delta_mean"] < 0)
    item["opposite_seed_ordering_count"] = int((group.accuracy_delta*group.retrain_delta < 0).sum())
    inter_summary.append(item)
inter.to_csv(OUT / "gu_retrain_strategy_interaction_seeds.csv", index=False, encoding="utf-8")
write_csv("gu_retrain_strategy_interactions.csv", inter_summary)

# 080: average IM requests within each training seed before any comparison.
raw = pd.read_csv(BUDGET / "cells.csv")
assert len(raw) == 2016 and raw.cell_id.nunique() == 2016
group_keys = ["dataset", "method", "selector", "ratio", "seed"]
metrics = ["accuracy", "disagreement", "gap", "before"]
b = raw.groupby(group_keys, as_index=False)[metrics].mean()
base = b[b.selector.eq("random")].drop(columns="selector")
paired = b.merge(base, on=["dataset", "method", "ratio", "seed"],
    suffixes=("", "_random"), validate="many_to_one")
paired["extra_loss"] = paired.accuracy_random-paired.accuracy
paired["extra_D"] = paired.disagreement-paired.disagreement_random
paired["extra_gap"] = paired.gap-paired.gap_random
for name in ["extra_loss", "extra_D", "extra_gap"]:
    assert paired.loc[paired.selector.eq("random"), name].dropna().abs().max() < 1e-10
paired.to_csv(OUT / "budget_random_seed_contrasts.csv", index=False, encoding="utf-8")
budget_summary = []
for keys, group in paired.groupby(["dataset", "method", "selector", "ratio"]):
    condition = dict(zip(["dataset", "method", "selector", "ratio"], keys))
    for metric in ["accuracy", "disagreement", "extra_loss", "extra_D", "extra_gap"]:
        budget_summary.append(dict(**condition, metric=metric, **stats(group[metric])))
write_csv("budget_random_contrasts.csv", budget_summary)

# Strategic-budget interaction beyond the Random budget response. This is a
# descriptive, within-seed contrast; not a sequential deletion trajectory.
budget_change_seeds = []
for (ds, method, sel), group in paired.groupby(["dataset", "method", "selector"]):
    low = group[group.ratio.eq(.05)].set_index("seed")
    for hi_ratio in [.33, .5]:
        high = group[group.ratio.eq(hi_ratio)].set_index("seed")
        if len(high) == 0:
            assert ds == "Cora" and hi_ratio == .5 and method in ["GraphEraser", "GraphRevoker"]
            continue
        joined = low.join(high, lsuffix="_low", rsuffix="_high", how="inner")
        assert len(joined) == 3
        for training_seed, row in joined.iterrows():
            item = dict(dataset=ds, method=method, selector=sel,
                        low_ratio=.05, high_ratio=hi_ratio, seed=int(training_seed))
            for metric in ["accuracy", "disagreement", "extra_loss", "extra_D", "extra_gap"]:
                item[metric+"_change"] = row[metric+"_high"]-row[metric+"_low"]
            budget_change_seeds.append(item)
changes = pd.DataFrame(budget_change_seeds)
change_summary = []
for keys, group in changes.groupby(["dataset", "method", "selector", "low_ratio", "high_ratio"]):
    condition = dict(zip(["dataset", "method", "selector", "low_ratio", "high_ratio"], keys))
    for metric in ["accuracy", "disagreement", "extra_loss", "extra_D", "extra_gap"]:
        change_summary.append(dict(**condition, metric=metric+"_change", **stats(group[metric+"_change"])))
write_csv("budget_interaction_seeds.csv", budget_change_seeds)
write_csv("budget_interactions.csv", change_summary)

# Method-level endpoint identities at common 10% conditions: evaluate actual
# Output identity before assigning the 'old protocol' label to every method.
overlap = []
fr = fixed_raw[(fixed_raw.seed.isin([42, 212, 2024])) &
               ((fixed_raw.source.eq("GCN")) | fixed_raw.selector.eq("degree"))]
br = raw[raw.ratio.eq(.1) & raw.selector.isin(["r_point", "gt_full", "degree"])]
key = ["dataset", "method", "selector", "seed", "selection_id"]
matched = br.merge(fr, on=key, suffixes=("_080", "_079"), validate="one_to_one")
for method, part in matched.groupby("method"):
    overlap.append(dict(method=method, matched_cells=len(part),
        same_output_id=int((part.output_id_080==part.output_id_079).sum()),
        max_accuracy_difference=float((part.accuracy-part.after).abs().max()),
        datasets=sorted(part.dataset.unique())))
write_csv("common_condition_output_identity.csv", overlap)

validation = dict(passed=True, input_sha256=checks,
    fixed_run="e79r6", budget_runs=sorted(raw.run_id.unique()),
    source_contrasts=len(summary), source_interactions=len(inter_summary),
    budget_contrasts=len(budget_summary), budget_interactions=len(change_summary),
    common_condition_identity=overlap,
    statistical_scope="Exploratory paired training-seed summaries. Pointwise t intervals, no multiplicity correction or equivalence test. Fixed splits. IM draws averaged within seed. Budget conditions and GU coordinates are not independent samples.",
    source_t_intervals="n=10 df=9", budget_t_intervals="n=3 df=2, very uncertain; retain SD and per-seed values",
    no_new_gpu_runs=True, scientific_acceptance="not_requested")
(OUT / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(validation, ensure_ascii=False, indent=2))
