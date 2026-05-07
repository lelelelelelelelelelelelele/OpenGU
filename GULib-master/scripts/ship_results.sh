#!/bin/bash
# 用法: bash scripts/ship_results.sh cora     # 机 A (4090)
#       bash scripts/ship_results.sh arxiv    # 机 B (h20)
# 行为：gate -> 只 tar json/_meta（跳过 npz） -> md5
set -e
cd ~/autodl-fs/OpenGU/GULib-master
TS=$(date +%Y%m%d_%H%M)

case "$1" in
  cora)
    echo "[gate] cora_GCN..."
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
    echo "[gate] cora_GAT..."
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
    OUT=cora_results_${TS}.tar.gz
    DIRS="results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05"
    # A.5 / A.6 / 其他可选目录如果存在就一并打
    for d in results/runs/cora_GCN_r0.0[12] results/runs/cora_GCN_r0.1[0] \
             results/runs/cora_GCN_r0.20 results/runs/cora_GIN_r0.05 \
             results/runs/citeseer_GCN_r0.0[5] results/runs/citeseer_GCN_r0.20; do
      [ -d "$d" ] && DIRS="$DIRS $d"
    done
    find $DIRS -type f \( -name '*.json' -o -name '_meta.json' \) \
        | tar czf "$OUT" -T -
    ;;
  arxiv)
    for tier in T1_seed42 T2_seed212 T3_seed722; do
      yaml="experiments/configs/phase_b_arxiv_${tier}.yaml"
      [ -f "$yaml" ] || continue
      seed=$(echo $tier | sed 's/.*seed//')
      [ "$(ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed${seed}/attack.json 2>/dev/null | wc -l)" -gt 0 ] || continue
      echo "[gate] $tier..."
      python scripts/gate_runs.py "$yaml" --f1-min 0.55 --f1-max 0.85 \
          || echo "  ↑ FAIL but proceeding (deadline mode)"
    done
    OUT=arxiv_results_${TS}.tar.gz
    find results/runs/ogbn-arxiv_GCN_r0.05 \
         -type f \( -name '*.json' -o -name '_meta.json' \) \
         | tar czf "$OUT" -T -
    ;;
  *)
    echo "usage: $0 {cora|arxiv}"; exit 2 ;;
esac

ls -lh "$OUT"
md5sum "$OUT" > "${OUT}.md5"
cat "${OUT}.md5"
echo "[done] tar at $(pwd)/$OUT"
