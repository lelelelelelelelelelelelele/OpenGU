@echo off
REM ============================================================
REM  run_all_eval_relative.bat
REM  Batch eval_relative.py for MG-0 ~ MG-3 + Ratio Sensitivity
REM  Run from: h:\project\OpenGU\GULib-master
REM ============================================================

set PYTHON=h:\conda_package\envs\gnn\python.exe
set SCRIPT=experiments/baseline_k5/eval_relative.py
set STRATEGIES=im_v4,tracin,hybrid_v4
set SEEDS=42 212 722 1337 2024

echo ======================================================================
echo  Batch eval_relative.py  (MG-0 ~ MG-3 + Ratio)
echo ======================================================================

REM ------------------------------------------------------------------
REM  MG-0: Cora / GCN / GIF, GNNDelete, GraphEraser, GUIDE
REM ------------------------------------------------------------------
echo.
echo [MG-0] Cora / GCN  (3 methods x 5 seeds, GUIDE blocked)
REM TODO: GUIDE needs re-run first, uncomment after GUIDE experiments are re-done
REM for %%M in (GIF GNNDelete GraphEraser GUIDE) do (
for %%M in (GIF GNNDelete GraphEraser) do (
    for %%S in (%SEEDS%) do (
        echo   -- %%M / cora / GCN / seed=%%S
        %PYTHON% %SCRIPT% --dataset_name cora --base_model GCN --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio 0.05 --random_seed %%S --baseline_k 5
    )
)

REM ------------------------------------------------------------------
REM  MG-1: Citeseer / GCN / GIF, GNNDelete, GraphEraser
REM ------------------------------------------------------------------
echo.
echo [MG-1] Citeseer / GCN  (3 methods x 5 seeds)
for %%M in (GIF GNNDelete GraphEraser) do (
    for %%S in (%SEEDS%) do (
        echo   -- %%M / citeseer / GCN / seed=%%S
        %PYTHON% %SCRIPT% --dataset_name citeseer --base_model GCN --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio 0.05 --random_seed %%S --baseline_k 5
    )
)

REM ------------------------------------------------------------------
REM  MG-2: Cora / GAT / GIF, GNNDelete, GraphEraser
REM ------------------------------------------------------------------
echo.
echo [MG-2] Cora / GAT  (3 methods x 5 seeds)
for %%M in (GIF GNNDelete GraphEraser) do (
    for %%S in (%SEEDS%) do (
        echo   -- %%M / cora / GAT / seed=%%S
        %PYTHON% %SCRIPT% --dataset_name cora --base_model GAT --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio 0.05 --random_seed %%S --baseline_k 5
    )
)

REM ------------------------------------------------------------------
REM  MG-3: Extended Methods (IDEA, MEGU)
REM    - Citeseer / GCN
REM    - Cora / GAT
REM ------------------------------------------------------------------
echo.
echo [MG-3] Extended Methods (IDEA, MEGU)
for %%M in (IDEA MEGU) do (
    for %%S in (%SEEDS%) do (
        echo   -- %%M / citeseer / GCN / seed=%%S
        %PYTHON% %SCRIPT% --dataset_name citeseer --base_model GCN --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio 0.05 --random_seed %%S --baseline_k 5
    )
    for %%S in (%SEEDS%) do (
        echo   -- %%M / cora / GAT / seed=%%S
        %PYTHON% %SCRIPT% --dataset_name cora --base_model GAT --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio 0.05 --random_seed %%S --baseline_k 5
    )
)

REM ------------------------------------------------------------------
REM  Ratio Sensitivity: Cora / GCN / GIF, GNNDelete
REM    - ratio = 0.01, 0.05, 0.10, 0.20
REM    (0.05 already covered by MG-0, but re-running is harmless)
REM ------------------------------------------------------------------
echo.
echo [Ratio] Cora / GCN / GIF + GNNDelete  (2 methods x 4 ratios x 5 seeds)
for %%M in (GIF GNNDelete) do (
    for %%R in (0.01 0.05 0.10 0.20) do (
        for %%S in (%SEEDS%) do (
            echo   -- %%M / cora / GCN / ratio=%%R / seed=%%S
            %PYTHON% %SCRIPT% --dataset_name cora --base_model GCN --unlearning_methods %%M --strategies %STRATEGIES% --unlearn_ratio %%R --random_seed %%S --baseline_k 5
        )
    )
)

echo.
echo ======================================================================
echo  ALL DONE!
echo ======================================================================
pause
