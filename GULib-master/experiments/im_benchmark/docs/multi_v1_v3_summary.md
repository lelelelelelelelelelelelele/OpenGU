# All Variants Benchmark Results (Seed=2024)

### Dataset: `citeseer`, K: `50`
**Baseline (V0)**: Time = 36.49s, Spread = 2480.00

| Variant | Time (s) | Speedup | Spread | Spread Loss (%) | Overlap (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1: Fast-Hash** | 36.04s | **1.0x** | 2480.00 | 0.00% | 100.0% |
| **V2: Top-K** | 10.66s | **3.4x** | 2120.00 | 14.52% | 2.0% |
| **V3: Pruning (M=400)** | 87.70s | **0.4x** | 2246.00 | 9.44% | 8.0% |
| **V4: Batch (B=5)** | 22.90s | **1.6x** | 2183.00 | 11.98% | 10.0% |

### Dataset: `citeseer`, K: `135`
**Baseline (V0)**: Time = 78.11s, Spread = 2763.00

| Variant | Time (s) | Speedup | Spread | Spread Loss (%) | Overlap (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1: Fast-Hash** | 89.93s | **0.9x** | 2763.00 | 0.00% | 100.0% |
| **V2: Top-K** | 10.71s | **7.3x** | 2120.00 | 23.27% | 0.7% |
| **V3: Pruning (M=400)** | 172.28s | **0.5x** | 2246.00 | 18.71% | 3.0% |
| **V4: Batch (B=5)** | 19.80s | **3.9x** | 2292.00 | 17.05% | 11.9% |

### Dataset: `cora`, K: `50`
**Baseline (V0)**: Time = 38.35s, Spread = 2652.00

| Variant | Time (s) | Speedup | Spread | Spread Loss (%) | Overlap (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1: Fast-Hash** | 33.16s | **1.2x** | 2652.00 | 0.00% | 100.0% |
| **V2: Top-K** | 10.62s | **3.6x** | 2485.00 | 6.30% | 2.0% |
| **V3: Pruning (M=400)** | 88.85s | **0.4x** | 2528.00 | 4.68% | 4.0% |
| **V4: Batch (B=5)** | 20.57s | **1.9x** | 2549.00 | 3.88% | 16.0% |

### Dataset: `cora`, K: `135`
**Baseline (V0)**: Time = 652.97s, Spread = 2700.00

| Variant | Time (s) | Speedup | Spread | Spread Loss (%) | Overlap (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1: Fast-Hash** | Skipped (Too slow) | - | - | - | - |
| **V2: Top-K** | 10.12s | **64.5x** | 2485.00 | 7.96% | 45.9% |
| **V3: Pruning (M=400)** | 197.71s | **3.3x** | 2528.00 | 6.37% | 16.3% |
| **V4: Batch (B=5)** | 18.90s | **34.6x** | 2666.00 | 1.26% | 45.2% |

