import json
from pathlib import Path

def unmark_summary_files():
    summary_files = [
        Path("results/evaluation/step0/all_metrics_detailed.json"),
        Path("results/step0_validation/all_metrics_detailed.json"),
        Path("results/step0_validation/cross_dataset_results.json"),
        Path("results/step0_validation/round2_results.json")
    ]
    
    for fpath in summary_files:
        if not fpath.exists(): continue
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def clean_node(obj, path=""):
                if isinstance(obj, dict):
                    # 如果不是 GUIDE 相关的，或者是 SGU/D2DGN，就移除标记
                    if 'is_corrupted' in obj:
                        # 检查路径中是否包含 GUIDE
                        if "GUIDE" not in str(path) and "GUIDE" not in str(obj):
                            del obj['is_corrupted']
                            if 'corruption_note' in obj: del obj['corruption_note']
                    
                    for k, v in list(obj.items()):
                        clean_node(v, path + "/" + str(k))
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        clean_node(item, path + "[%d]" % i)

            clean_node(data)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print("Unmarked erroneous flags in: %s" % fpath)
        except Exception as e:
            print("Error processing %s: %s" % (fpath, e))

if __name__ == "__main__":
    unmark_summary_files()
