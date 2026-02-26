# Final Cross-Seed Statistical Results (Purified Metrics)

> **Data Source**: `results/evaluation/stats/final_paper_stats.csv`

> **Metric Format**: **Rel_F1_Drop** (Retrain_Gap)

> **Relative F1 Drop (%)** = [k=5 Baseline F1] - [Attack F1]

> **Retrain Gap (%)** = |Unlearn F1 - Retrain F1| (Mimicry Quality)

> **Significance**: * p < 0.05, ** p < 0.01 (One-sample T-test vs 0)

## Setting: CITESEER / GAT (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | -0.78 (1.50) | -0.72 (1.80) | 0.00 (-) | -0.60 (3.75) | -0.54 (1.05) | -1.32 (0.45) |


## Setting: CITESEER / GAT (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | -0.66** (0.90) | -0.48 (5.86) | -0.03 (1.05) | -0.90 (4.50) | -0.72 (1.35) | -1.56* (0.15) |


## Setting: CITESEER / GCN (Ratio: 0.05)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | - | 0.36* (0.75) | 0.09 (0.69) | 0.09 (1.26) | - | - |
| GNNDelete | 53.69** (1.86) | 53.69** (1.50) | 53.69** (0.63) | 53.69** (3.15) | 53.69** (7.06) | 53.69** (4.26) |
| GraphEraser | - | 0.30 (3.78) | 0.36 (1.20) | -0.03 (2.07) | - | - |
| IDEA | - | 0.84** (0.69) | 0.51 (0.78) | 0.27 (1.47) | - | - |
| MEGU | - | 0.99** (0.66) | 0.06 (1.14) | -0.39 (1.14) | - | - |


## Setting: CITESEER / GCN (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 0.03 (1.05) | -0.03 (2.25) | 0.18* (0.15) | -0.18 (1.95) | 0.00 (0.45) | -0.06 (0.15) |


## Setting: CITESEER / GCN (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 0.03 (1.50) | -0.03 (7.66) | 0.18* (1.35) | -0.18 (3.75) | 0.00 (0.90) | -0.06 (0.45) |


## Setting: CITESEER / GIN (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | -0.56 (1.05) | -0.36 (3.60) | -1.21 (1.20) | -1.26 (1.95) | -1.46 (0.75) | -1.61 (0.30) |


## Setting: CITESEER / GIN (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | -0.67 (1.65) | 0.45 (9.01) | -0.97 (2.55) | -0.82 (4.50) | -1.20 (0.45) | -1.27 (0.90) |


## Setting: CORA / GAT (Ratio: 0.05)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | - | 1.77** (0.44) | 3.54** (1.77) | 2.51** (0.85) | - | - |
| GNNDelete | 9.04** (14.61) | 12.91* (9.08) | 16.94** (11.33) | 18.85** (12.18) | 12.44** (14.94) | 12.55** (13.95) |
| GraphEraser | - | 0.26 (3.58) | 6.20** (3.21) | 5.16** (2.69) | - | - |
| IDEA | - | 1.03 (1.07) | 2.55** (0.89) | 1.66** (0.26) | - | - |
| MEGU | - | 0.41 (1.00) | 0.85 (0.92) | 1.44* (0.96) | - | - |


## Setting: CORA / GAT (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 1.85* (-) | 2.66** (2.21) | 3.32** (0.18) | 1.96* (0.92) | 6.24** (0.37) | 6.75** (1.11) |


## Setting: CORA / GAT (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 1.88* (1.29) | 2.55** (8.49) | 1.26 (0.55) | 1.88* (2.58) | 1.59* (0.55) | 1.59** (0.74) |


## Setting: CORA / GCN (Ratio: 0.01)

| Method | tracin | im_v4 | hybrid_v4 |
| :--- | ---: | ---: | ---: |
| GIF | 1.77** (0.70) | 2.14** (0.52) | 1.88** (0.74) |
| GNNDelete | 13.51** (7.71) | 13.62** (16.86) | 15.06** (10.11) |


## Setting: CORA / GCN (Ratio: 0.05)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | - | 0.70** (2.00) | 1.52** (1.24) | 1.41** (0.67) | - | - |
| GNNDelete | - | 8.05** (10.96) | 12.47* (10.85) | 11.44* (10.92) | - | - |
| GraphEraser | - | 1.70* (2.95) | 4.87* (2.47) | 4.39* (1.62) | - | - |


## Setting: CORA / GCN (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 0.85** (0.48) | 1.00** (2.55) | 2.36** (0.55) | 1.88** (0.66) | 3.43** (1.03) | 4.17** (1.00) |
| GNNDelete | - | 13.25** (7.70) | 17.17** (16.28) | 16.11** (12.82) | - | - |


## Setting: CORA / GCN (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 1.37** (0.70) | 0.85** (6.16) | 1.77** (0.63) | 1.66** (1.81) | 0.77* (0.63) | 1.14** (0.74) |
| GNNDelete | - | 15.79* (3.14) | 14.40** (11.49) | 15.87** (18.63) | - | - |


## Setting: CORA / GIN (Ratio: 0.1)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | -0.30 (0.18) | -1.73* (1.11) | 1.25 (0.37) | 0.04 (0.92) | 2.47* (0.18) | 4.47* (0.37) |


## Setting: CORA / GIN (Ratio: 0.2)

| Method | random | tracin | im_v4 | hybrid_v4 | degree | pagerank |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| GIF | 0.85* (1.66) | -0.11 (2.40) | 0.11 (0.37) | 0.04 (7.38) | -1.37 (2.03) | 0.63 (0.55) |


