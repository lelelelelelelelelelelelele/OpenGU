# Master Repair Script (PowerShell Version)
# Fixing GNNDelete Corruption & Completing GIF P2-EXT

$REPO_ROOT = "H:/project/OpenGU/GULib-master"
$PYTHON_BIN = "H:/conda_package/envs/gnn/python.exe"
$env:PYTHONPATH = "$env:PYTHONPATH;$REPO_ROOT/scripts/evaluation"

Set-Location $REPO_ROOT

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "PHASE 1: Re-running GNNDelete (MG-1 & MG-2) Main Experiments"
Write-Host "==========================================================" -ForegroundColor Cyan

# 1.1 MG-1: Citeseer / GCN
Write-Host ">>> Running GNNDelete MG-1 (Citeseer/GCN)..."
& $PYTHON_BIN demo_attack.py --methods GNNDelete --datasets citeseer --base_model GCN --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --ratios 0.05 --seeds 42,212,722,1337,2024 --no_cache

# 1.2 MG-2: Cora / GAT
Write-Host ">>> Running GNNDelete MG-2 (Cora/GAT)..."
& $PYTHON_BIN demo_attack.py --methods GNNDelete --datasets cora --base_model GAT --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --ratios 0.05 --seeds 42,212,722,1337,2024 --no_cache

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "PHASE 2: Filling Evaluation Gaps (Relative & Collateral)"
Write-Host "==========================================================" -ForegroundColor Cyan

# 2.1 GIF P2-EXT Evaluations
# Since the .sh has CRLF issues, we run the commands directly here
$GIF_DATASETS = "cora", "citeseer"
$GIF_MODELS = "GCN", "GAT", "GIN"
$GIF_RATIOS = "0.10", "0.20"
$GIF_SEEDS = "42", "212", "722", "1337", "2024"

Write-Host ">>> Filling GIF P2-EXT Gaps (Relative & Collateral)..."
foreach ($mod in $GIF_MODELS) {
    foreach ($ds in $GIF_DATASETS) {
        foreach ($r in $GIF_RATIOS) {
            # Relative
            foreach ($s in $GIF_SEEDS) {
                & $PYTHON_BIN experiments/baseline_k5/eval_relative.py --unlearning_methods GIF --dataset_name $ds --base_model $mod --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --unlearn_ratio $r --random_seed $s --repair
            }
            # Collateral
            & $PYTHON_BIN eval_collateral.py --unlearning_methods GIF --dataset_name $ds --base_model $mod --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --unlearn_ratio $r --repair
        }
    }
}

# 2.2 GNNDelete Evaluation Completion
Write-Host ">>> Filling GNNDelete MG-1/2 Gaps (Relative & Collateral)..."
$GNND_TASKS = @{ "citeseer"="GCN"; "cora"="GAT" }
foreach ($ds in $GNND_TASKS.Keys) {
    $mod = $GNND_TASKS[$ds]
    foreach ($s in $GIF_SEEDS) {
        & $PYTHON_BIN experiments/baseline_k5/eval_relative.py --unlearning_methods GNNDelete --dataset_name $ds --base_model $mod --strategies random,degree,pagerank,tracin,im_v4,hybrid_v4 --unlearn_ratio 0.05 --random_seed $s --repair
    }
    & $PYTHON_BIN eval_collateral.py --unlearning_methods GNNDelete --dataset_name $ds --base_model $mod --unlearn_ratio 0.05 --repair
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "PHASE 3: Final Data Aggregation & Reporting"
Write-Host "==========================================================" -ForegroundColor Cyan
& $PYTHON_BIN scripts/evaluation/final_data_aggregator.py
& $PYTHON_BIN scripts/evaluation/gen_md_report_v2.py

Write-Host "`nMaster Repair Complete! Please check report/paper/sections/cross_seed_tables.md" -ForegroundColor Green
