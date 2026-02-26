import json
import os
from pathlib import Path

def final_boss_v3_mark_mode():
    results_dir = Path('./results')
    deleted_count = 0
    marked_count = 0
    
    print("Starting ULTIMATE Audit V3 (Selective Delete + Mark Mode)...")

    def process_node(obj):
        """Recursively scan and mark Zero Delta. Returns (is_modified, has_bad_data)."""
        modified = False
        bad_found = False
        
        if isinstance(obj, dict):
            # Check for data point
            b = obj.get('f1_before', obj.get('perf_before', obj.get('baseline_f1_after')))
            a = obj.get('f1_after', obj.get('perf_unlearn', obj.get('attack_f1_after')))
            if b is not None and a is not None:
                try:
                    if abs(float(a) - float(b)) < 1e-12:
                        bad_found = True
                        if 'is_corrupted' not in obj:
                            obj['is_corrupted'] = True
                            obj['corruption_note'] = "Zero Delta detected (2026-02-27 Audit)"
                            modified = True
                except: pass
            
            # Recurse through children
            for k, v in list(obj.items()):
                m, b = process_node(v)
                if m: modified = True
                if b: bad_found = True
        elif isinstance(obj, list):
            for item in obj:
                m, b = process_node(item)
                if m: modified = True
                if b: bad_found = True
        return modified, bad_found

    for root, _, files in os.walk(results_dir):
        if 'selection_cache' in root: continue
        for file in files:
            if not file.endswith('.json'): continue
            fpath = Path(root) / file
            
            try:
                with open(fpath, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                
                # Logic: Delete if it's a leaf result (cache/baseline/single experiment)
                # Mark if it's a validation summary or aggregate table
                is_summary_file = 'step0' in str(fpath) or 'evaluation' in str(fpath)
                
                modified, has_bad = process_node(data)
                
                if has_bad:
                    if is_summary_file:
                        if modified:
                            with open(fpath, 'w', encoding='utf-8') as out:
                                json.dump(data, out, indent=2)
                            print("MARKED: %s" % fpath)
                            marked_count += 1
                    else:
                        # Non-summary files are safe to delete to trigger repair
                        print("PURGING: %s" % fpath)
                        fp.close()
                        fpath.unlink()
                        deleted_count += 1
            except Exception: pass

    print("\nAUDIT V3 COMPLETE.")
    print("Files Purged (to trigger repair): %d" % deleted_count)
    print("Summary Files Marked: %d" % marked_count)

if __name__ == "__main__":
    final_boss_v3_mark_mode()
