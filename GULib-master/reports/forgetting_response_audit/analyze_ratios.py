"""EXP-032 current recovery-run budget analysis; read frozen evidence only.

E:/conda_package/envs/gnn/python.exe -B -X utf8 reports/forgetting_response_audit/analyze_ratios.py
Writes only ratio_* derived artifacts beside this script. No training or state edits.
"""
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import json
import subprocess
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
JOB="aagu032-recovery-full-20260920"
EXPERIMENT="aagu032-extended-v2-multi-gcn-retrain"
RAW=ROOT/"results/runs/gpu4090"/EXPERIMENT/JOB
REGISTER=ROOT/"self/research/analyses/EXP-032.json"
SHA="ee4ea59509523a650fe67bacf9bc961dfe9db78b"
RUN_SHA="8391e397c1c12075e66249844fe93ca70423a0fede0785faae23185e0541e1ed"
DS=["Cora","CiteSeer","PubMed"]
SEEDS=[42,212,2024]
RATIOS=[.01,.05,.10,.15]
SELECTORS=["gt_full","gt_full_all_trainable","degree","random","gt_simple","r_point","p_graph","p_point","gt_full_all_trainable_hops3","gt_full_sgc_all_trainable_hops3"]
DISPLAY=["random","degree","r_point","gt_full"]


def read(p): return json.loads(p.read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
def save(name,df): df.to_csv(OUT/name,index=False,encoding="utf-8")
def frozen(path): return subprocess.check_output(["git","show",f"{SHA}:GULib-master/{path}"],cwd=ROOT).decode("utf-8")
def mean_sd(values):
    values=np.asarray(values,float)
    assert len(values)==3 and np.isfinite(values).all()
    return dict(mean=float(values.mean()),sd=float(values.std(ddof=1)),minimum=float(values.min()),maximum=float(values.max()),n=3)


def audit_inputs():
    registered=read(REGISTER)
    attempt=next(a for a in registered["attempts"] if a["run_id"]==JOB)
    assert attempt["manifest"]["sha256"]==RUN_SHA==digest(RAW/"run.json")
    assert attempt["manifest"]["commit"]==SHA and attempt["manifest"]["completed"]==360
    run=read(RAW/"run.json")
    assert run["commit"]==SHA and run["status"]=="completed"
    assert run["run_id"]==JOB and run["experiment_id"]==EXPERIMENT
    index_path=ROOT/".syncmate/artifact_index.json"
    index={i["path"]:i for i in read(index_path)["peers"]["gpu4090"]["items"]}
    delivery_path=ROOT/f".syncmate/deliveries/{JOB}.json"
    delivery=read(delivery_path)
    assert delivery["execution"]["git_sha"]==SHA
    manifest=delivery["result"]["completed_job"]["result"]["manifest"]
    assert manifest["status"]=="verified"
    expected={a["path"]:a["sha256"] for a in manifest["artifacts"]}
    prefix=f"results/runs/{EXPERIMENT}/{JOB}/"
    assert len(expected)==721
    indexed_dates=set()
    for path,h in expected.items():
        assert path.startswith(prefix)
        local=RAW/path[len(prefix):]
        assert digest(local)==h==index[path]["sha256"],path
        assert (ROOT/index[path]["local_path"]).resolve()==local.resolve()
        assert index[path]["remote_git"]["sha"]==SHA
        indexed_dates.add(index[path]["verified_at"])
    assert expected[prefix+"run.json"]==RUN_SHA
    rows=[]
    node_lists={}
    identity_sets=defaultdict(set)
    cache=Counter()
    called=Counter()
    for cell in run["cells"]:
        assert cell["status"]=="completed"
        cond=cell["conditions"]
        assert cond["method"]=="Retrain" and cond["model"]=="OpenGU.GCNNet"
        selector=Path(cond["selector_ref"]).stem
        assert selector in SELECTORS
        assert cond["dataset_name"] in DS and cond["training_seed"] in SEEDS and cond["budget_ratio"] in RATIOS
        assert cond["budget"]==dict(mode="ratio",value=cond["budget_ratio"])
        assert cond["seed"]==cond["training_seed"]
        folder=RAW/cell["path"]
        assert set(cell["files"])=={"metrics.json","selection.json"}
        for name,info in cell["files"].items():
            assert expected[prefix+cell["path"]+"/"+name]==info["sha256"]
        met,selection=read(folder/"metrics.json"),read(folder/"selection.json")
        assert met["cell_id"]==selection["cell_id"]==cell["cell_id"]
        assert selection["selection_id"]==cell["selection_id"]
        selected=selection["selected_nodes"]
        assert len(set(selected))==len(selected)==selection["requested_k"]
        coordinate=(cond["dataset_name"],selector,cond["training_seed"],cond["budget_ratio"])
        assert coordinate not in node_lists
        node_lists[coordinate]=selected
        nodes_hash=hashlib.sha256(json.dumps(selected,separators=(",",":")).encode("utf-8")).hexdigest()
        identity_sets[selection["selection_id"]].add(nodes_hash)
        stages={r["stage"]:r["values"] for r in met["rows"]}
        utility=stages["utility"]
        assert set(stages)=={"method","utility","post_method_metrics"}
        assert stages["method"]==stages["post_method_metrics"]
        assert abs(stages["method"]["accuracy"]-utility["f1_after"])<1e-12
        assert abs(stages["method"]["f1"]-utility["f1_after"])<1e-12
        assert all(utility[k] is None for k in ["f1_before","f1_drop","f1_drop_ratio"])
        assert stages["method"]["update_detection_auc"] is None
        assert stages["method"]["update_detection_auc_status"]=="missing_original_predictions"
        cache.update([cell["cache"]["method"]])
        called.update([str(cell["producer_called"]["method"])])
        rows.append(dict(dataset=cond["dataset_name"],selector=selector,selector_method=cond["selector"],selector_ref=cond["selector_ref"],seed=cond["training_seed"],ratio=cond["budget_ratio"],ratio_percent=100*cond["budget_ratio"],accuracy=100*utility["f1_after"],cross_entropy=stages["method"]["cross_entropy"],classification_auc=stages["method"]["classification_auc"],requested_k=selection["requested_k"],cell_id=cell["cell_id"],cell_path=cell["path"],split=cond["dataset_fingerprint"],selection_id=selection["selection_id"],selected_nodes_sha256=nodes_hash,selection_file_sha256=digest(folder/"selection.json"),metrics_file_sha256=digest(folder/"metrics.json"),output_id=cell["output"]["artifact_id"],output_content_hash=cell["output"]["content_hash"]))
    df=pd.DataFrame(rows)
    assert len(df)==df.cell_id.nunique()==360
    assert df.groupby(["dataset","selector","ratio"]).size().eq(3).all()
    assert df.groupby(["dataset","seed","ratio"]).size().eq(10).all()
    assert df.groupby("dataset").split.nunique().eq(1).all()
    assert df.groupby(["dataset","ratio"]).requested_k.nunique().eq(1).all()
    nested=[]
    for ds in DS:
        for selector in SELECTORS:
            for seed in SEEDS:
                for low,high in zip(RATIOS[:-1],RATIOS[1:]):
                    a,b=node_lists[(ds,selector,seed,low)],node_lists[(ds,selector,seed,high)]
                    assert b[:len(a)]==a
                    nested.append(dict(dataset=ds,selector=selector,seed=seed,low_ratio=low,high_ratio=high,low_k=len(a),high_k=len(b),ordered_prefix=True))
    assert len(nested)==270
    config_path=run["config_path"]
    config=frozen(config_path)
    parser=frozen("experiments/modular_config.py")
    retrain_config=frozen("experiments/configs/unlearning/retrain.yaml")
    assert hashlib.sha256(config.encode("utf-8")).hexdigest()==delivery["execution"]["config_sha256"]
    assert "'epochs': 3000" in parser and "training:" not in config and "training:" not in retrain_config
    # Some archived selection IDs are prefix/scoring identities reused at several budgets.
    # Never join observations on selection_id: the full coordinate + returned file SHA is used.
    duplicate_ids={k:len(v) for k,v in identity_sets.items() if len(v)>1}
    audit=dict(experiment_id="EXP-032",runtime_experiment_id=EXPERIMENT,run_id=JOB,execution_sha=SHA,
               registered_run_sha256=RUN_SHA,verified_files=721,verified_cell_files=720,
               trusted_index_entries=721,trusted_index_verified_at=sorted(indexed_dates),
               delivery_top_level_status=delivery["result"]["status"],delivery_top_level_ok=delivery["result"]["ok"],
               delivery_top_level_gate_passed=delivery["result"]["gate_passed"],
               delivery_top_level_project_acceptance=delivery["result"]["project_acceptance"],
               delivery_top_level_errors=delivery["result"].get("errors",[]),
               completed_job_manifest_status=manifest["status"],
               trust_scope="Registered run hash, current trusted-index identities, completed-job manifest, and all local file hashes agree. The latest delivery wrapper records a later collection failure and is not claimed to pass.",
               raw_cells=360,datasets=DS,selectors=SELECTORS,training_seeds=SEEDS,ratios=RATIOS,
               target_model="OpenGU.GCNNet",methods=["Retrain"],original_baseline_cells=0,GU_cells=0,
               original_prediction_status_counts={"missing_original_predictions":360},
               training_epochs_default_at_execution_sha=3000,
               method_cache_counts=dict(cache),method_producer_called_counts=dict(called),
               dataset_fingerprints=df.groupby("dataset").split.first().to_dict(),
               requested_k_by_dataset_ratio=[dict(dataset=d,ratio=float(r),requested_k=int(g.requested_k.iloc[0])) for (d,r),g in df.groupby(["dataset","ratio"])],
               selection_identity=dict(unique_selection_ids=len(identity_sets),ids_reused_for_multiple_node_lists=len(duplicate_ids),max_node_lists_per_selection_id=max(map(len,identity_sets.values())),binding="dataset + full selector_ref + training_seed + ratio + cell_id + selection file SHA; never selection_id alone",nested_adjacent_budget_prefix_checks=270,all_prefix_checks_passed=True),
               metrics=dict(accuracy="100 * utility.f1_after; stored f1/accuracy/post_method_metrics agree; test accuracy, equivalent to micro-F1 in this single-label task",budget_change="higher-budget accuracy minus lower-budget accuracy, percentage points",baseline_contrast="selector accuracy minus matched Random or Degree accuracy, percentage points"),
               inference="Descriptive mean and sample SD over 3 paired training seeds. No significance tests, confidence intervals, equivalence tests, or cross-selector pseudo-replication.",
               selected_display_strategies=DISPLAY,
               limitations=["Only Retrain outcomes; no GU curve or Original/zero-deletion endpoint is recorded.","1%-to-15% changes are not Original-to-Retrain losses.","Three training seeds and a fixed dataset split; intervals in the plot are sample SD, not confidence intervals.","Budget chains use nested selected-node prefixes; this does not guarantee monotonic model accuracy.","One Random request per seed/ratio in this run; no three-request averaging used in EXP-079 is imported.","Selection IDs are reused across budget prefixes; full coordinates and file hashes, not the ID alone, bind evidence.","Later delivery collection failed with WinError206; no overall delivery-gate PASS is asserted despite matching current trusted index and local artifacts.","No result from obsolete positional mappings, old training-parameter runs, or another GU run is joined into this budget analysis."],
               input_hashes={str(p.relative_to(ROOT)).replace("\\","/"):digest(p) for p in [REGISTER,RAW/"run.json",index_path,delivery_path]},
               frozen_source_sha256={config_path:hashlib.sha256(config.encode("utf-8")).hexdigest(),"experiments/modular_config.py":hashlib.sha256(parser.encode("utf-8")).hexdigest(),"experiments/configs/unlearning/retrain.yaml":hashlib.sha256(retrain_config.encode("utf-8")).hexdigest()},
               checks=dict(registered_run_hash=True,all_manifest_index_local_hashes_match=True,full_condition_coverage=True,cell_metric_selection_binding=True,accuracy_fields_agree=True,original_baseline_absent=True,nested_budget_prefixes=True,execution_training_default_verified=True),
               new_GPU_runs=0,new_models_trained=0,scientific_acceptance="not_requested",
               versions=dict(python=sys.version,numpy=np.__version__,pandas=pd.__version__,matplotlib=matplotlib.__version__))
    save("ratio_cells.csv",df)
    save("ratio_prefix_checks.csv",pd.DataFrame(nested))
    return df,audit


def analyze(df):
    summary=[]
    for (ds,selector,ratio),group in df.groupby(["dataset","selector","ratio"]):
        summary.append(dict(dataset=ds,selector=selector,ratio=ratio,ratio_percent=100*ratio,requested_k=int(group.requested_k.iloc[0]),**mean_sd(group.set_index("seed").loc[SEEDS,"accuracy"])))
    summary=pd.DataFrame(summary)
    assert len(summary)==120
    save("ratio_condition_summary.csv",summary)
    changes,change_seeds=[],[]
    spans=[(.01,.05),(.05,.10),(.10,.15),(.01,.15)]
    for (ds,selector),group in df.groupby(["dataset","selector"]):
        grid=group.pivot(index="seed",columns="ratio",values="accuracy").loc[SEEDS]
        for low,high in spans:
            values=grid[high]-grid[low]
            for seed,value in values.items():
                change_seeds.append(dict(dataset=ds,selector=selector,seed=seed,low_ratio=low,high_ratio=high,change_pp=float(value)))
            changes.append(dict(dataset=ds,selector=selector,low_ratio=low,high_ratio=high,direction="higher_budget_minus_lower_budget",seeds_decreased=int((values<0).sum()),seeds_increased=int((values>0).sum()),**mean_sd(values)))
    changes=pd.DataFrame(changes)
    assert len(changes)==120 and len(change_seeds)==360
    save("ratio_budget_changes.csv",changes)
    save("ratio_budget_change_seed_values.csv",pd.DataFrame(change_seeds))
    contrasts,contrast_seeds=[],[]
    for base in ["random","degree"]:
        baseline=df[df.selector==base].set_index(["dataset","seed","ratio"])
        for (ds,selector,ratio),group in df.groupby(["dataset","selector","ratio"]):
            if selector==base: continue
            current=group.set_index("seed").loc[SEEDS,"accuracy"]
            ref=pd.Series([baseline.loc[(ds,s,ratio),"accuracy"] for s in SEEDS],index=SEEDS)
            values=current-ref
            for seed,value in values.items():
                contrast_seeds.append(dict(dataset=ds,selector=selector,baseline=base,seed=seed,ratio=ratio,contrast_pp=float(value)))
            contrasts.append(dict(dataset=ds,selector=selector,baseline=base,ratio=ratio,direction="selector_minus_baseline",**mean_sd(values)))
    contrasts=pd.DataFrame(contrasts)
    assert len(contrasts)==216 and len(contrast_seeds)==648
    save("ratio_baseline_contrasts.csv",contrasts)
    save("ratio_baseline_contrast_seed_values.csv",pd.DataFrame(contrast_seeds))
    # Candidate settings are reported without threshold-based selection or new success claims.
    display_change=changes[(changes.low_ratio==.01)&(changes.high_ratio==.15)&changes.selector.isin(DISPLAY)].copy()
    save("ratio_display_endpoint_changes.csv",display_change)
    return summary,changes,contrasts


def draw(df,summary):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False,"svg.fonttype":"none"})
    colors={"random":"#60717d","degree":"#ce8a24","r_point":"#2d85a8","gt_full":"#b55075"}
    labels={"random":"Random","degree":"Degree","r_point":"r_point","gt_full":"gt_full"}
    fig,axes=plt.subplots(1,3,figsize=(14.4,5.7))
    for ax,ds in zip(axes,DS):
        for selector in DISPLAY:
            group=summary[(summary.dataset==ds)&(summary.selector==selector)].sort_values("ratio")
            raw=df[(df.dataset==ds)&(df.selector==selector)]
            ax.scatter(raw.ratio_percent,raw.accuracy,c=colors[selector],s=19,alpha=.38,edgecolors="none",zorder=2)
            ax.errorbar(group.ratio_percent,group["mean"],yerr=group.sd,color=colors[selector],marker="o",markersize=5,lw=1.8,capsize=3,label=labels[selector],zorder=3)
        ax.set_title(ds,fontweight="bold",fontsize=13)
        ax.set_xticks([1,5,10,15])
        ax.set_xlabel("Deletion budget (% of training candidates)")
        ax.set_ylabel("Retrain test accuracy (%)")
        ax.grid(alpha=.16)
        ax.set_xlim(.5,15.5)
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="upper center",bbox_to_anchor=(.5,.895),ncol=4,frameon=False)
    fig.suptitle("EXP-032: retraining response across deletion budgets",fontsize=16,fontweight="bold",y=1.005)
    fig.text(.5,.94,"Current recovery run only | Retrain only | No GU or Original / 0% endpoint",ha="center",fontsize=11,color="#495b68")
    fig.text(.5,.025,"Means +/- sample SD across 3 training seeds (42, 212, 2024); faint dots show individual seeds. SD is not a confidence interval.\nFour fixed display selectors; all 10 are in the CSV. Lines join measured budgets; panel y-scales differ. Stored f1 = accuracy / micro-F1.",ha="center",fontsize=9,color="#495b68")
    fig.subplots_adjust(top=.77,bottom=.19,wspace=.27,left=.06,right=.99)
    for ext in ["png","svg","pdf"]:
        fig.savefig(OUT/("ratio_retrain_accuracy."+ext),dpi=190,facecolor="white",bbox_inches="tight")
    plt.close(fig)


def main():
    df,audit=audit_inputs()
    summary,changes,contrasts=analyze(df)
    draw(df,summary)
    files=["ratio_cells.csv","ratio_prefix_checks.csv","ratio_condition_summary.csv","ratio_budget_changes.csv","ratio_budget_change_seed_values.csv","ratio_baseline_contrasts.csv","ratio_baseline_contrast_seed_values.csv","ratio_display_endpoint_changes.csv"]
    files += ["ratio_retrain_accuracy."+ext for ext in ["png","svg","pdf"]]
    audit["output_rows"]={"raw_cells":360,"condition_summary":120,"budget_change_summary":120,"baseline_contrast_summary":216,"prefix_checks":270}
    audit["output_sha256"]={name:digest(OUT/name) for name in files}
    for path,h in audit["input_hashes"].items():
        assert digest(ROOT/path)==h,path
    audit["checks"]["inputs_unchanged_during_analysis"]=True
    audit["analysis_script_sha256"]=digest(Path(__file__))
    write_json("ratio_verification.json",audit)
    print(json.dumps(dict(output=str(OUT),checks=audit["checks"],rows=audit["output_rows"],delivery_top_level_status=audit["delivery_top_level_status"]),ensure_ascii=False,indent=2))
    print(changes[(changes.low_ratio==.01)&(changes.high_ratio==.15)&changes.selector.isin(DISPLAY)][["dataset","selector","mean","sd","seeds_decreased","seeds_increased"]].to_string(index=False))
    print(contrasts[(contrasts.ratio==.15)&contrasts.selector.isin(["gt_full","r_point"])][["dataset","selector","baseline","mean","sd"]].to_string(index=False))


if __name__=="__main__": main()
