@echo off
echo Starting Benchmark... > experiments\im_benchmark\bench_log.txt
call h:\conda_package\Scripts\activate.bat gnn
python -u experiments\im_benchmark\run_benchmark.py >> experiments\im_benchmark\bench_log.txt 2>&1
echo FINISHED >> experiments\im_benchmark\bench_log.txt
