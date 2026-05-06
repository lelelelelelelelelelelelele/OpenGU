"""Diagnose whether r=0.05 MIA AUC is exactly identical (bug) or coincidentally rounded the same."""
import json
import glob
import os

for ratio_dir in ["cora_GCN_r0.05", "cora_GCN_r0.1"]:
    print(f"\n=== {ratio_dir} ===")
    for d in sorted(glob.glob(f"H:/project/OpenGU/GULib-master/results/runs/{ratio_dir}/GraphRevoker_*/seed42")):
        d = d.replace("\\", "/")
        strat = os.path.basename(os.path.dirname(d)).split("GraphRevoker_", 1)[1]
        a = json.load(open(d + "/attack.json"))
        r = a["results"][strat]
        mia = r.get("mia_auc")
        sel = r.get("selected_nodes", [])
        # Print to full float precision + first selected nodes (selection should differ across strategies)
        print(f"  {strat:10s}  mia_auc = {mia!r}    "
              f"|selected|={len(sel):3d}  first3={sel[:3]}  cache_hit={r.get('selection_cache_hit')}")
