"""Quick scan of all baseline files to check f1_after values."""
import json, os

base = "results/baseline/k5_random"
print("=" * 80)
print("BASELINE HEALTH CHECK")
print("=" * 80)

for method in sorted(os.listdir(base)):
    mpath = os.path.join(base, method)
    if not os.path.isdir(mpath):
        continue
    for dataset in sorted(os.listdir(mpath)):
        dpath = os.path.join(mpath, dataset)
        if not os.path.isdir(dpath):
            continue
        for model in sorted(os.listdir(dpath)):
            mopath = os.path.join(dpath, model)
            if not os.path.isdir(mopath):
                continue
            for fname in sorted(os.listdir(mopath)):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(mopath, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        data = json.load(f)
                    f1 = data.get("f1_after")
                    flag = "BAD" if f1 is not None and f1 < 0.3 else "OK "
                    print(f"  [{flag}] {method}/{dataset}/{model}/{fname}: f1_after={f1}")
                except Exception as e:
                    print(f"  [ERR] {fpath}: {e}")

print("=" * 80)
