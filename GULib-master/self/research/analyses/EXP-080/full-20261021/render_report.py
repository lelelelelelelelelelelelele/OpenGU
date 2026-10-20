from pathlib import Path
import importlib.util
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'experiments/modular_run.py').exists())
spec=importlib.util.spec_from_file_location('existing_report_renderer',ROOT/'reports/forgetting_response_audit/render_report.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.OUT=OUT
module.build('STRATEGY_REPORT','五种策略一起看<br>IM有没有稳定模式？','EXP-080 · 全预算 · 三训练seed','strategy_report_validation.json','2026-10-21')
module.build('REPORT','CiteSeer 50%已补齐<br>GU是否跟随重训练','EXP-080 · 2,016个可信条件','report_validation.json','2026-10-21')
