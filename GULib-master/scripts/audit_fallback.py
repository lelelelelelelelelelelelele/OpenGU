import os
import re
from collections import Counter

LOG_DIRS = ["results/experiments", "results/_archive", "results/_deprecated_tracin_bug", "results/step0_validation"]

def parse_logs():
    fallback_cases = []
    total_logs = 0
    total_runs_checked = 0
    
    for base_dir in LOG_DIRS:
        if not os.path.exists(base_dir): continue
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".log") or file.endswith("results.json"):
                    # Only focus on log files, ignoring huge json unless needed
                    if not file.endswith(".log"): continue
                    path = os.path.join(root, file)
                    total_logs += 1
                    
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        
                        poison_f1 = None
                        f1_before = None
                        strategy = "Unknown"
                        
                        for line in lines:
                            if "Evaluating strategy:" in line:
                                strategy = line.split("Evaluating strategy:")[1].strip()
                            if "Poison F1 Score:" in line:
                                match = re.search(r'Poison F1 Score:\s*([\d\.]+)', line)
                                if match:
                                    poison_f1 = float(match.group(1))
                            if "F1 before unlearning:" in line:
                                match = re.search(r'F1 before unlearning:\s*([\d\.]+)', line)
                                if match:
                                    f1_before = float(match.group(1))
                                    total_runs_checked += 1
                                    
                                    # Fallback detected
                                    if poison_f1 == 0.0 and f1_before > 0.0:
                                        fallback_cases.append((path, strategy, poison_f1, f1_before))
                                    elif poison_f1 is None and f1_before > 0.0:
                                        # Often means poison_f1 was never recorded but f1_before generated a positive value
                                        fallback_cases.append((path, strategy, "Missing/None", f1_before))
                                    
                                    # Reset for next iteration in same log
                                    poison_f1 = None
                                    f1_before = None
                                
    print(f"Total log files checked: {total_logs}")
    print(f"Total F1 evaluations checked: {total_runs_checked}")
    print(f"Found {len(fallback_cases)} fallback occurrences.")
    
    summary = Counter()
    method_counter = Counter()
    for case in fallback_cases:
        path = case[0]
        # Try to infer method from the path or filename
        # File often named like method_dataset_model.log or it's inside a folder
        filename = os.path.basename(path)
        method = filename.split('_')[0] if '_' in filename else "Unknown"
        method_counter[method] += 1
        summary[path] += 1
        
    print(f"\nNumber of log files containing fallback hit: {len(summary)}")
    print(f"\nFallback hits per Unlearning Method:")
    for method, count in method_counter.most_common():
        print(f" - {method}: {count} times")
        
    print("\n--- Example Hits ---")
    for i, case in enumerate(fallback_cases[:20]):
        filename = os.path.basename(case[0])
        print(f"[{filename}] Strategy: {case[1]}, poison_f1: {case[2]}, f1_before(fallback): {case[3]}")

if __name__ == "__main__":
    parse_logs()
