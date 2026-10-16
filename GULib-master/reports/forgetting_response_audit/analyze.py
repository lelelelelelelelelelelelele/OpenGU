"""Read-only reanalysis of accepted EXP-079/e79r5; write only beside this script.

E:/conda_package/envs/gnn/python.exe -B -X utf8 reports/forgetting_response_audit/analyze.py
No model execution, new experimental evidence, or result/state mutation occurs.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
RAW = ROOT / "results/runs/gpu4090/exp079-surrogate-multiseed/e79r5"
OLD = ROOT / "self/research/analyses/EXP-079/e79r5"
JOB = "exp079-20261013-e79r5"
SHA = "e02b5fa40ebce66fb45e57ea23b8d6c8d7856685"
DATASETS = ["Cora", "CiteSeer", "PubMed"]
METHODS = ["GNNDelete", "GIF", "IDEA", "MEGU", "GraphEraser", "GraphRevoker"]
SEEDS = [42, 212, 2024, 0, 1, 2, 3, 4, 5, 6]
SOURCES = ["GCN", "SGC", "GAT", "GIN"]
CONDITIONS = [("random", "baseline"), ("degree", "baseline")] + [
    (s, a) for s in ["gt_full", "r_point"] for a in SOURCES
]
METRICS = ["U", "G", "Rloss", "D"]
KEYS = ["dataset", "method", "selector", "source"]
COLORS = dict(zip(METHODS, ["#c04635", "#7250a1", "#a94d95", "#c18a21", "#188078", "#2864a3"]))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def save(name, frame):
    frame.to_csv(OUT / name, index=False, encoding="utf-8")


def interval(values):
    values = np.asarray(values, dtype=float)
    assert len(values) == 10 and np.isfinite(values).all()
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    half = float(stats.t.ppf(0.975, 9) * sd / np.sqrt(10))
    return dict(mean=mean, lo=mean-half, hi=mean+half, sd=sd, n=10)


def condition(selector, source):
    return selector.title() if source == "baseline" else selector + " / " + source


def audit_and_extract():
    delivery_path = ROOT / f".syncmate/deliveries/{JOB}.json"
    index_path = ROOT / ".syncmate/artifact_index.json"
    delivery, index_data = read(delivery_path), read(index_path)
    result = delivery["result"]
    assert result["ok"] and result["gate_passed"] and result["project_acceptance"]["passed"]
    assert result["project_acceptance"]["accepted_cells"] == 2520
    assert delivery["execution"]["git_sha"] == SHA
    manifest = result["completed_job"]["result"]["manifest"]
    assert manifest["status"] == "verified"
    expected = {x["path"]: x["sha256"] for x in manifest["artifacts"]}
    index = {x["path"]: x for x in index_data["peers"]["gpu4090"]["items"]}
    prefix = "results/runs/exp079-surrogate-multiseed/e79r5/"
    assert len(expected) == 5041
    for path, digest in expected.items():
        assert path.startswith(prefix)
        local = RAW / path[len(prefix):]
        assert sha256(local) == digest == index[path]["sha256"], path
        assert (ROOT / index[path]["local_path"]).resolve() == local.resolve()

    run = read(RAW / "run.json")
    assert run["commit"] == SHA and run["status"] == "completed"
    rows, protocols, masks, requested, selected = [], set(), set(), {}, {}
    for cell in run["cells"]:
        assert cell["status"] == "completed"
        cond = cell["conditions"]
        assert cond["model"] == "OpenGU.GCNNet" and cond["budget_ratio"] == .1
        for name, info in cell["files"].items():
            assert expected[prefix + cell["path"] + "/" + name] == info["sha256"]
        folder = RAW / cell["path"]
        met, selection = read(folder / "metrics.json"), read(folder / "selection.json")
        assert cell["cell_id"] == met["cell_id"] == selection["cell_id"]
        assert cell["selection_id"] == selection["selection_id"]
        nodes = frozenset(selection["selected_nodes"])
        assert len(nodes) == len(selection["selected_nodes"]) == selection["requested_k"]
        requested.setdefault(cond["dataset_name"], set()).add(len(nodes))
        stem = Path(cond["selector_ref"]).stem
        source = next((s for s in SOURCES[1:] if stem.endswith("_" + s.lower())), "GCN") if cond["selector"] in ["gt_full", "r_point"] else "baseline"
        request_key = (cond["dataset_name"], cond["training_seed"], cond["selector"], source, cond.get("random_selector_seed"))
        if request_key in selected:
            assert selected[request_key] == nodes
        selected[request_key] = nodes
        stages = {x["stage"]: x for x in met["rows"]}
        utility = stages["utility"]["values"]
        row = dict(cell_id=cell["cell_id"], dataset=cond["dataset_name"], method=cond["method"],
                   seed=cond["training_seed"], selector=cond["selector"], source=source,
                   random_seed=cond.get("random_selector_seed"), split=cond["dataset_fingerprint"],
                   selection_id=cell["selection_id"], output_id=cell["output"]["artifact_id"],
                   before=None if utility["f1_before"] is None else 100*utility["f1_before"],
                   after=100*utility["f1_after"], U=None, G=None, Rloss=None, D=None,
                   update_detection_auc=stages["method"]["values"]["update_detection_auc"],
                   update_detection_auc_status=stages["method"]["values"]["update_detection_auc_status"])
        if cond["method"] != "Retrain":
            gap, flip = stages["post_unlearning_utility_and_retrain_gap"], stages["post_unlearning_flip_hop"]
            assert gap["baseline_output"] == flip["baseline_output"] == flip["identity"]["retrain_output"]
            protocol = flip["identity"]["protocol"]
            protocols.add(protocol["comparison"])
            masks.add(protocol["evaluation_mask"])
            assert protocol["dataset_input"]["instance"]["split"]["seed"] == 2024
            row.update(U=100*(utility["f1_before"]-utility["f1_after"]), G=100*gap["values"]["gap"],
                       D=100*flip["values"]["fraction_flipped"], retrain=100*gap["values"]["perf_retrain"],
                       baseline_id=gap["baseline_output"]["artifact_id"])
            row["Rloss"] = row["U"] - row["G"]
            assert abs(row["G"] - (row["retrain"]-row["after"])) < 1e-8
            assert abs(row["Rloss"] - (row["before"]-row["retrain"])) < 1e-8
        rows.append(row)
    frame = pd.DataFrame(rows)
    assert len(frame) == frame.cell_id.nunique() == 2520
    assert set(frame.seed) == set(SEEDS)
    assert set(frame.method) == set(METHODS + ["Retrain"])
    assert frame.groupby(["dataset", "method", "seed"]).size().eq(12).all()
    assert frame.groupby("dataset").split.nunique().eq(1).all()
    assert protocols == {"argmax_gu_vs_same_request_retrain_first_index_ties"}
    outputs = frame.set_index("output_id")
    for row in rows:
        if row["method"] == "Retrain":
            continue
        baseline = outputs.loc[row["baseline_id"]]
        assert baseline.method == "Retrain"
        assert all(baseline[k] == row[k] for k in ["dataset", "seed", "split", "selection_id"])
        assert abs(baseline.after-row["retrain"]) < 1e-8
    existing = pd.read_csv(OLD / "cells.csv").set_index("cell_id").loc[frame.cell_id]
    for key in ["dataset", "method", "seed", "selector", "source", "split", "selection_id", "output_id"]:
        assert np.array_equal(existing[key].to_numpy(), frame[key].to_numpy()), key
    for saved, fresh in [("before", "before"), ("after", "after"), ("U", "U"), ("G", "G"), ("flip", "D"), ("random_seed", "random_seed"), ("retrain", "retrain"), ("update_detection_auc","update_detection_auc")]:
        assert np.allclose(existing[saved], frame[fresh], atol=1e-9, rtol=1e-10, equal_nan=True), saved
    assert np.array_equal(existing.update_detection_auc_status.to_numpy(),frame.update_detection_auc_status.to_numpy())
    gu = frame[frame.method != "Retrain"].copy()
    assert len(gu) == 2160
    assert gu[gu.selector == "random"].groupby(["dataset", "method", "seed"]).random_seed.apply(lambda x: set(x) == {11, 22, 33}).all()
    profiles = gu.groupby(KEYS + ["seed"], as_index=False)[METRICS + ["before", "after", "retrain", "update_detection_auc"]].mean()
    assert len(profiles) == 1800 and profiles.groupby(KEYS).size().eq(10).all()
    duplicates = {}
    for metric in METRICS:
        pivot = gu.pivot(index=["dataset", "seed", "selector", "source", "random_seed"], columns="method", values=metric)
        maximum = float((pivot.GIF-pivot.IDEA).abs().max())
        assert maximum == 0
        duplicates[metric] = maximum
    audit = dict(job_id=JOB, run_id="e79r5", execution_sha=SHA,
                 config_path="experiments/configs/exp079/surrogate_multiseed.yaml",
                 verified_files=5041, raw_cells=2520, raw_gu_cells=2160, collapsed_seed_rows=1800,
                 datasets=DATASETS, methods=METHODS, conditions_per_dataset_method=10,
                 training_seeds=SEEDS, n_independent_seed_clusters=10,
                 random_selector_seeds=[11,22,33], random_aggregation="average three requests within each training seed before inference",
                 target_model="OpenGU.GCNNet", split_seed=2024, deletion_budget_ratio=.1,
                 requested_nodes={k:sorted(v) for k,v in requested.items()},
                 dataset_fingerprints=frame.groupby("dataset").split.first().to_dict(),
                 D_comparison=sorted(protocols), D_evaluation_mask=sorted(masks),
                 gif_idea_raw_metric_max_abs_difference=duplicates,
                 gif_idea_independent_method_evidence=False,
                 csv_matches_raw=True, matched_retrain_identity_passed=True,
                 interval="pointwise two-sided Student t 95% CI over 10 training-seed clusters; df=9; no multiplicity adjustment; not equivalence tests",
                 metrics={"U":"100*(utility_before-utility_GU), percentage points; stored f1 is accuracy in this single-label implementation, equivalent to micro-F1, not macro-F1", "G":"100*(utility_shared_Retrain-utility_GU), percentage points", "Rloss":"U-G=100*(utility_method_before-utility_shared_Retrain), percentage points; algebraic baseline-to-shared-Retrain difference, not uniformly pure data-removal damage", "D":"100*mean(argmax_GU != argmax_same_request_shared_Retrain), percent of test nodes", "update_detection_auc":"AUROC distinguishing selected nodes from test nodes using per-node L2 softmax(before)-softmax(after); no update magnitude or privacy guarantee"},
                 input_hashes={str(p.relative_to(ROOT)).replace("\\", "/"):sha256(p) for p in [OLD/"cells.csv", RAW/"run.json", delivery_path, index_path]},
                 checks={"delivery_gate_project_acceptance":True,"all_5041_raw_file_sha256_matches_manifest_and_index":True,"csv_full_identity_and_metric_agreement":True,"same_request_retrain_pairing":True,"seed_condition_coverage":True,"random_clusters":True,"metric_algebra":True},
                 limitations=["One fixed split and one 10% deletion budget; no budget response curve.","Training-seed intervals do not establish cross-split or cross-request-population generalization.","D measures GU versus same-request shared retraining, not GU versus pre-unlearning model.","The shared Retrain reference is a single GCN, not retraining within each sharded model family; G and D may include pre-existing family differences. Rloss is an algebraic baseline-to-shared-Retrain difference, not universally identifiable deletion damage.","No matched no-update control or independent retrain-versus-retrain stochastic calibration.","No saved parameters/logits are consumed; metric-only reanalysis cannot estimate update magnitude. Computed update-detection AUC differing from 0.5 is indirect evidence against fully identical softmax outputs under the implemented comparison, not against arbitrarily small changes or score-representation changes.","Before/after score representations can differ for some method adapters; raw logit distances require semantic alignment before interpretation.","Small means and confidence intervals crossing zero are not equivalence evidence.","Cross-condition ranges are descriptive; conditions are neither independent replicates nor random samples.","All six GU methods are displayed, but GIF and IDEA are identical on these four raw metrics and are not independent corroboration."],
                 versions=dict(python=sys.version,numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__),
                 new_gpu_runs=0, previous_outputs_modified=False, scientific_acceptance="not_requested")
    save("seed_values.csv", profiles)
    save("raw_gu_metrics.csv", gu)
    auc_rows=[]
    for (dataset,method),subset in gu.groupby(["dataset","method"]):
        zero=subset.U == 0
        auc_rows.append(dict(dataset=dataset,method=method,raw_cells=len(subset),
                             computed_cells=int((subset.update_detection_auc_status=="computed").sum()),
                             auc_raw_min=float(subset.update_detection_auc.min()),auc_raw_max=float(subset.update_detection_auc.max()),
                             auc_equals_half_cells=int((subset.update_detection_auc==.5).sum()),
                             U_exact_zero_cells=int(zero.sum()),
                             U_exact_zero_auc_not_half_cells=int((zero & (subset.update_detection_auc!=.5)).sum())))
    save("update_detection_coverage.csv",pd.DataFrame(auc_rows))
    audit["update_detection_checks"]=dict(raw_gu_cells=len(gu),computed_cells=int((gu.update_detection_auc_status=="computed").sum()),
        auc_min=float(gu.update_detection_auc.min()),auc_max=float(gu.update_detection_auc.max()),
        auc_equals_half_cells=int((gu.update_detection_auc==.5).sum()),
        U_exact_zero_cells=int((gu.U==0).sum()),
        U_exact_zero_auc_not_half_cells=int(((gu.U==0)&(gu.update_detection_auc!=.5)).sum()))
    return profiles, audit


def summarize(profiles):
    rows, long = [], []
    for key, subset in profiles.groupby(KEYS, sort=False):
        row = dict(zip(KEYS, key))
        row["condition"] = condition(row["selector"], row["source"])
        row["n"] = 10
        for metric in METRICS:
            info = interval(subset.set_index("seed").loc[SEEDS, metric])
            row.update({metric+"_"+k:v for k,v in info.items() if k != "n"})
            long.append({**dict(zip(KEYS,key)), "condition":row["condition"], "metric":metric, "unit":"percent" if metric == "D" else "percentage_points", **info})
        row.update({"update_detection_auc_"+k:v for k,v in interval(subset.set_index("seed").loc[SEEDS,"update_detection_auc"]).items() if k!="n"})
        rows.append(row)
    summary = pd.DataFrame(rows)
    assert len(summary) == 180 and len(long) == 720
    save("all_condition_summary.csv", summary)
    save("all_condition_summary_long.csv", pd.DataFrame(long))
    coverage = []
    for (dataset, method), subset in summary.groupby(["dataset", "method"], sort=False):
        row = dict(dataset=dataset, method=method, conditions=10, seeds_per_condition=10)
        for metric in METRICS:
            column = metric+"_mean"
            low, high = subset.loc[subset[column].idxmin()], subset.loc[subset[column].idxmax()]
            row.update({metric+"_mean_min":float(low[column]), metric+"_min_condition":low["condition"], metric+"_mean_max":float(high[column]), metric+"_max_condition":high["condition"]})
        coverage.append(row)
    assert len(coverage) == 18
    save("coverage_ranges.csv", pd.DataFrame(coverage))
    contrasts, contrasts_long = [], []
    for baseline_name in ["random", "degree"]:
        baseline = profiles[profiles.selector == baseline_name].set_index(["dataset", "method", "seed"])
        for key, subset in profiles.groupby(KEYS, sort=False):
            if key[2] == baseline_name:
                continue
            row = dict(zip(KEYS, key))
            row.update(condition=condition(row["selector"], row["source"]), baseline=baseline_name, n=10)
            ordered = subset.set_index("seed").loc[SEEDS]
            reference = baseline.loc[(key[0],key[1])].loc[SEEDS]
            for metric in ["U", "D", "G"]:
                info = interval(ordered[metric].to_numpy()-reference[metric].to_numpy())
                row.update({metric+"_"+k:v for k,v in info.items() if k != "n"})
                contrasts_long.append({**dict(zip(KEYS,key)), "condition":row["condition"], "baseline":baseline_name, "metric":metric, "unit":"percentage_points", **info})
            contrasts.append(row)
    assert len(contrasts) == 324 and len(contrasts_long) == 972
    save("paired_contrasts.csv", pd.DataFrame(contrasts))
    save("paired_contrasts_long.csv", pd.DataFrame(contrasts_long))
    return summary, pd.DataFrame(coverage), pd.DataFrame(contrasts)


def export_figure(fig, stem):
    for extension in ["png", "svg", "pdf"]:
        fig.savefig(OUT / (stem+"."+extension), dpi=190, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def figures(summary):
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10, "axes.spines.top":False, "axes.spines.right":False, "svg.fonttype":"none"})
    fig, axes = plt.subplots(1,3,figsize=(15.0,5.4))
    for ax,dataset in zip(axes,DATASETS):
        for method in METHODS:
            subset = summary[(summary.dataset == dataset)&(summary.method == method)]
            assert len(subset) == 10
            if method == "IDEA":
                ax.scatter(subset.U_mean,subset.D_mean,s=73,facecolors="none",edgecolors=COLORS[method],marker="D",linewidths=1.2,zorder=5)
            else:
                ax.scatter(subset.U_mean,subset.D_mean,s=43,c=COLORS[method],alpha=.84,edgecolors="white",linewidths=.4,zorder=4)
        ax.axvline(0,c="#a8b2ba",ls="--",lw=.8,zorder=0)
        ax.set_title(dataset,fontweight="bold",fontsize=13)
        ax.set_xlabel("Accuracy drop U (percentage points)")
        ax.set_ylabel("GU / shared Retrain disagreement D (%)")
        ax.grid(alpha=.14)
        ax.set_ylim(bottom=0)
    handles=[Line2D([],[],ls="",marker="D" if m=="IDEA" else "o",ms=7,markerfacecolor="none" if m=="IDEA" else COLORS[m],markeredgecolor=COLORS[m],label=m) for m in METHODS]
    fig.legend(handles=handles,loc="upper center",bbox_to_anchor=(.5,.96),ncol=6,frameon=False)
    fig.suptitle("Small accuracy drops can coexist with disagreement from retraining",fontsize=16,y=1.03,fontweight="bold")
    fig.text(.5,.014,"60 means per panel: 6 GU methods x 10 request conditions; n = 10 training seeds. Stored f1 = accuracy (micro-F1).\nGIF / IDEA coincide (hollow diamonds overlay GIF); no jitter. Reference: one shared GCN Retrain, not within-family retraining.",ha="center",fontsize=9,color="#455464")
    fig.subplots_adjust(top=.81,bottom=.19,wspace=.31)
    export_figure(fig,"utility_vs_retrain_disagreement")

    shown=[("random","baseline"),("degree","baseline"),("gt_full","GCN"),("r_point","GCN")]
    palette=["#536675","#ce8623","#1d8e83","#8463b0"]
    offsets=np.linspace(-.27,.27,4)
    fig,axes=plt.subplots(1,2,figsize=(13.0,6.9),sharey=True)
    for ax,metric,title in zip(axes,["U","D"],["Accuracy drop U (percentage points)","GU / shared Retrain disagreement D (%)"]):
        for i,(selector,source) in enumerate(shown):
            subset=summary[(summary.dataset=="CiteSeer")&(summary.selector==selector)&(summary.source==source)].set_index("method").loc[METHODS]
            mean=subset[metric+"_mean"].to_numpy()
            error=np.array([mean-subset[metric+"_lo"].to_numpy(),subset[metric+"_hi"].to_numpy()-mean])
            ax.errorbar(mean,np.arange(6)+offsets[i],xerr=error,fmt="o",ms=5,color=palette[i],capsize=2.5,lw=1.25,label=condition(selector,source))
        ax.axvline(0,c="#a8b2ba",ls="--",lw=.8)
        ax.set_xlabel(title)
        ax.set_yticks(np.arange(6),METHODS)
        ax.grid(axis="x",alpha=.18)
        ax.set_ylim(5.65,-.65)
    axes[1].tick_params(labelleft=True)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="upper center",bbox_to_anchor=(.5,.925),ncol=4,frameon=False)
    fig.suptitle("CiteSeer: matched utility and retraining-disagreement readouts",fontsize=15,y=.995,fontweight="bold")
    fig.text(.5,.021,"Pointwise 95% t CIs; n = 10 training seeds; Random averages 3 requests within each seed. Stored f1 = accuracy (micro-F1).\nShared GCN Retrain can include method-family differences. GIF / IDEA match; small means or overlapping CIs do not establish equivalence.",ha="center",fontsize=9,color="#455464")
    fig.subplots_adjust(top=.83,bottom=.15,wspace=.30,left=.11,right=.98)
    export_figure(fig,"citeseer_four_condition_intervals")


def main():
    profiles,audit=audit_and_extract()
    summary,coverage,contrasts=summarize(profiles)
    figures(summary)
    outputs=["seed_values.csv","raw_gu_metrics.csv","all_condition_summary.csv","all_condition_summary_long.csv","coverage_ranges.csv","paired_contrasts.csv","paired_contrasts_long.csv","update_detection_coverage.csv"]
    outputs += [stem+"."+ext for stem in ["utility_vs_retrain_disagreement","citeseer_four_condition_intervals"] for ext in ["png","svg","pdf"]]
    audit["checks"].update(all_condition_summary_rows_180=len(summary)==180, coverage_rows_18=len(coverage)==18, paired_contrast_rows_324=len(contrasts)==324, all_csv_numeric_metrics_finite=bool(np.isfinite(profiles[METRICS].to_numpy()).all()))
    for name,digest in audit["input_hashes"].items():
        assert sha256(ROOT/name)==digest, "Input changed during analysis: "+name
    audit["checks"]["input_files_unchanged_during_analysis"]=True
    audit["analysis_script_sha256"]=sha256(Path(__file__))
    audit["output_sha256"]={name:sha256(OUT/name) for name in outputs}
    dump("verification.json",audit)
    print(json.dumps({"status":"passed","output_directory":str(OUT),"verified_raw_files":5041,"summary_rows":180,"coverage_rows":18,"paired_contrast_rows":324,"figures":2,"new_gpu_runs":0},indent=2))
    example=summary[(summary.dataset=="CiteSeer")&(summary.method.isin(["GraphEraser","GraphRevoker"]))&(summary.source.isin(["baseline","GCN"]))]
    print(example[["method","condition","U_mean","U_lo","U_hi","G_mean","G_lo","G_hi","D_mean","D_lo","D_hi"]].to_string(index=False))
    example=contrasts[(contrasts.dataset=="CiteSeer")&(contrasts.method.isin(["GraphEraser","GraphRevoker"]))&(contrasts.source=="GCN")&(contrasts.baseline=="random")]
    print(example[["method","condition","baseline","U_mean","U_lo","U_hi","G_mean","G_lo","G_hi","D_mean","D_lo","D_hi"]].to_string(index=False))


if __name__ == "__main__":
    main()
