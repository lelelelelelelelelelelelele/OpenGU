import os
import glob
import statistics

log_files = glob.glob('log/IF/**/*.log', recursive=True) + glob.glob('log/GIF/**/*.log', recursive=True)

times_by_ds = {}

for f in log_files:
    # the dataset is usually the second directory e.g., log/IF/cora/GCN/...
    parts = f.replace('\\', '/').split('/')
    if len(parts) >= 3:
        ds = parts[2]
        try:
            with open(f, 'r', encoding='utf-8') as file:
                for line in file:
                    if "unlearning time" in line.lower() or "unlearn time" in line.lower():
                        # Simple extraction
                        # e.g., "INFO: GIF unlearing time: avg=184.2123 seconds"
                        try:
                            # Try to extract the number
                            words = line.replace('=', ' ').replace(':', ' ').split()
                            for w in words:
                                try:
                                    val = float(w)
                                    # Filter out F1 scores etc, looking for reasonable time values
                                    if 0.1 < val < 10000:
                                        if ds not in times_by_ds:
                                            times_by_ds[ds] = []
                                        times_by_ds[ds].append(val)
                                        break
                                except ValueError:
                                    pass
                        except:
                            pass
        except:
            pass

print("Extracted Authentic IF/GIF (IHVP) Calculation Times:")
for ds, times in times_by_ds.items():
    if times:
        print(f"Dataset {ds}: mean={statistics.mean(times):.4f}s, min={min(times):.4f}s, max={max(times):.4f}s, count={len(times)}")
