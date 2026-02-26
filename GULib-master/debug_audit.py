import json
from pathlib import Path

def check_file(filename):
    fpath = Path('results/cache') / filename
    if not fpath.exists():
        print(f"File {filename} not found.")
        return

    with open(fpath, 'r') as f:
        data = json.load(f)

    res = data.get('result', {})
    b = res.get('f1_before')
    a = res.get('f1_after')
    
    # 核心判定逻辑：如果差值极小，判定为失效
    is_corrupted = (b is not None and a is not None and abs(a - b) < 1e-7)
    
    print(f"--- Audit Result for {filename} ---")
    print(f"F1 Before: {b}")
    print(f"F1 After:  {a}")
    print(f"Status:    {'FAILED (Zero Delta/Corrupted)' if is_corrupted else 'PASSED'}")

if __name__ == "__main__":
    check_file('3b33178e020a5889.json')
