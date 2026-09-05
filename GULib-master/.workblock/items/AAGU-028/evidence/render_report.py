"""Generate the paired acceptance projection from verified CPU observations."""
from pathlib import Path
import html
import json

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
v = json.loads((HERE / 'observations.json').read_text(encoding='utf-8'))
assert v['protected_unchanged'] and all(c['exit_code'] == 0 for c in v['checks'])
assert all(t['passed'] for t in v['test_results'])
count = len(v['test_results'])
protected = sum(r['file_count'] for r in v['protected_roots'])
example = v['example']
assert example['metrics_repeat_equal'] and example['training_steps_forbidden_during_reads']
assert not example['hot_retrain_producer_called']

title = 'AAGU-028 · Retrain 独立方法与 Metrics 输出复用'
change = 'Retrain 现在可以从独立 Unlearning 小表执行并保存完整输出；GNNDelete 与 GIF 显式引用同一个 Retrain。Metrics 只读取已完成的模型预测和评价输入，旧 eval_collateral 内部训练入口已删除。'
observation = f'在隔离 CPU 小图中，Retrain 冷运行完成训练，热读取复用同一产物；禁止 Selector、原模型准备与优化器训练后，Metrics 连续两次重算的身份和数值完全一致。{count} 项测试及 24 节点示例通过，核对范围内 {protected:,} 个历史结果文件哈希未变。'
decision = 'Agent 建议接受本次软件修复：独立执行、真实输出复用和错误身份拒绝已有约定证据。当前由用户决定接受、返工或拒绝；正式 GPU 运行与完整研究矩阵尚未执行，仍需后续实验各自的运行门槛。'

scenarios = [
 ('独立方法与冷／热运行', '已有 Selection 进入独立 Retrain YAML，冷运行没有创建原模型 checkpoint，也没有调用 Selector producer；再次读取时 producer_called=false，引用和数值一致。', 'test_independent_retrain_cold_hot_cross_gu_and_metrics_only'),
 ('跨 GU 复用和只读评价', '同一请求的 GNNDelete、GIF 共用一个 Retrain 引用。阻断 Selector、prepare_model、Adam/SGD step 后，热读和两次 Metrics 仍成功；Store 全文件快照相同。改变 GU 参数或指标集合后，Retrain 继续命中。', 'test_independent_retrain_cold_hot_cross_gu_and_metrics_only；test_gu_parameters_and_metrics_do_not_change_retrain'),
 ('删除语义与模型可复核', '删除节点不再参与监督，全部关联边被移除；节点编号和特征行保留。保存的模型 state 重建后，前向 logits 与保存数组逐元素相等。Retrain state 与既有监督训练器在相同保留图上的 state 哈希相同。', 'test_retrain_removes_supervision_and_incident_edges；test_independent_retrain_cold_hot_cross_gu_and_metrics_only'),
 ('不同身份明确拒绝', '模型、训练、评价图语义或请求改变时产生新身份，旧配对被拒绝。分别修改真实特征、标签、边、split 后，旧输出不能被消费；输出损坏、完整哈希不符、producer 改变、Selection 依赖缺失均拒绝，没有隐式重训。', 'test_retrain_identity_changes_and_pairing_rejects；test_actual_dataset_changes_cannot_consume_old_output；test_missing_and_corrupted_outputs_rejected_without_training；test_changed_producer_and_missing_selection_dependency_rejected'),
 ('CLI 与活动调用链', '独立 eval_collateral CLI 读取已完成输出，返回 training_producer_called=false，Store 未变；target-direct 的共享执行消费者在 CPU 上完成明确 GU/Retrain 配对。正式 stage 的 GPU 调用未执行。', 'test_metrics_cli_and_target_direct_shared_consumer；既有 target-direct 配置／stage 回归'),
 ('精度与历史数据', f'AttackResult 的 JSON 往返保留原始浮点值，Metrics 从原始 logits 计算。source 与 canonical 的 10 个 cache/result 根逐文件核对，{protected:,} 个现有文件未变；原本不存在的根没有被创建。', 'test_aggregate_serialization_is_lossless；TestAttackResult.test_to_dict；protected-before/after.json'),
]
boundaries = [
 '软件证据范围是本地 CPU、节点删除和已支持的 GCN/SGC 消费者，主要集成覆盖 GNNDelete、GIF、Retrain。不是任意 GU、模型或 edge/feature 删除的承诺。',
 '默认删除语义：排除选中节点的监督、删除全部关联边、保留孤立特征行；默认在原图统一评价，也可明确选择保留图。GU 自有训练算法沿用现有实现。',
 '跨 GU 计算复用使用同一已验证 Selection 引用；Metrics 再核对实际节点请求及共同模型、训练和评价语义。不能把不同来源或相近身份的输出猜配成同一结果。',
 '新 target checkpoint 明确记录训练条件；旧 checkpoint 缺少这些字段时拒绝接纳，保留历史文件。其他旧矩阵若仍依赖隐式 collateral 路径，会明确失败，须在其所属任务接入输出消费者。',
 'NOT OBSERVED：SSH/GPU 正式 stage、真实正式数据上的成本与完整矩阵。样例的 utility 相等且 gap=0 只用于核对数据流，不证明任何方法效果或科研结论。',
]
links = [
 ('权威 WorkItem 与当前 source branch', 'WORKITEM.md'),
 ('数据流、删除语义与可重跑命令', '../../../docs/retrain_outputs.md'),
 ('160 项结果、原始证据哈希及输出引用', 'evidence/observations.json'),
 ('隔离 CPU Verify 脚本', 'evidence/verify.py'),
 ('最小可运行示例', '../../../experiments/examples/retrain_cpu.py'),
]
rows = example['metrics'][0]['rows']
example_lines = []
for method, row in zip(('GNNDelete', 'GIF'), rows):
    m = row['metrics']
    example_lines.append((method, repr(m['perf_unlearn']), repr(m['perf_retrain']), repr(m['gap'])))

md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', change, '',
      '### 核心观察', '', observation, '', '主要证据：[真实 CPU 观察](evidence/observations.json) 与下方场景。', '',
      '### 当前决定', '', decision, '', '> 当前验收决定：`待决定`', '', '## 验收场景与实际观察', '']
for name, text, test in scenarios:
    md.extend([f'### {name}', '', text, '', f'**PASS** · `{test}`', ''])
md.extend(['## 24 节点可重跑示例', '', '表中保留实际存储精度。两种 GU 引用同一 Retrain，独立 Metrics 两次结果完全相同。', '',
           '| 方法 | perf_unlearn | perf_retrain | gap |', '|---|---:|---:|---:|'])
md.extend('| ' + ' | '.join(r) + ' |' for r in example_lines)
md.extend(['', 'Retrain 引用：`' + example['retrain_output']['artifact_id'] + '`。完整 recipe/content 哈希见 observations.json。', '', '## 边界与尚未观察', ''])
md.extend('- ' + b for b in boundaries)
md.extend(['', '## 证据与复核', ''])
md.extend(f'- [{label}]({url})' for label, url in links)
md.extend(['', '原始日志目录：`' + v['raw_evidence_directory'] + '`。该目录为本机 ignored 运行证据；持久摘要与原始文件哈希保存在 observations.json。', '',
           '统一 Verify 在干净软件检查点运行。报告、Record 与证据投影加入后的当前候选由 source branch 的 clean HEAD 唯一确定，最终 diff 复核与新增报告检查记入 WorkItem。测试日志不替代人的决定。', '',
           '若返工改变待接受代码，在同一 WorkItem 更新候选和当前报告，决定保持待决定；若接受，由同一次 Closeout 同步当前决定并按项目流程执行。', ''])
(ITEM / 'REPORT.md').write_text('\n'.join(md), encoding='utf-8')

e = html.escape
cards = ''.join(f'<article><h3>{e(name)}</h3><p>{e(text)}</p><p class="evidence"><b>PASS</b> · {e(test)}</p></article>' for name, text, test in scenarios)
table = ''.join('<tr>' + ''.join(f'<td>{e(cell)}</td>' for cell in row) + '</tr>' for row in example_lines)
body = f'''<header><div class="eyebrow">软件验收 · AAGU-028 · FIX</div><h1>Retrain 独立执行<br>Metrics 复用已完成输出</h1><p>同一 WorkItem · formal 验收路线 · 等待人的决定</p></header>
<section data-workblock-human-result class="human"><h2>Human Result</h2>
<h3>实际增量</h3><p>{e(change)}</p><h3>核心观察</h3><p>{e(observation)}</p>
<p>主要证据：<a href="evidence/observations.json">真实 CPU 观察</a>与下方场景。</p>
<h3>当前决定</h3><p>{e(decision)}</p><div class="decision">当前验收决定：<span data-workblock-decision="pending">待决定</span></div></section>
<section><h2>验收场景与实际观察</h2><div class="cards">{cards}</div></section>
<section><h2>24 节点可重跑示例</h2><p>表中保留实际存储精度。两种 GU 引用同一 Retrain，独立 Metrics 两次结果完全相同。</p>
<div class="table-wrap"><table><thead><tr><th>方法</th><th>perf_unlearn</th><th>perf_retrain</th><th>gap</th></tr></thead><tbody>{table}</tbody></table></div>
<p>Retrain 引用：<code>{e(example['retrain_output']['artifact_id'])}</code>。完整 recipe/content 哈希见 observations.json。</p></section>
<section><h2>边界与尚未观察</h2><ul>{''.join('<li>'+e(b)+'</li>' for b in boundaries)}</ul></section>
<section><h2>证据与复核</h2><ul>{''.join(f'<li><a href="{url}">{e(label)}</a></li>' for label,url in links)}</ul>
<p>原始日志目录：<code>{e(v['raw_evidence_directory'])}</code>。该目录为本机 ignored 运行证据；持久摘要与原始文件哈希保存在 observations.json。</p>
<p>统一 Verify 在干净软件检查点运行。报告、Record 与证据投影加入后的当前候选由 source branch 的 clean HEAD 唯一确定，最终 diff 复核与新增报告检查记入 WorkItem。测试日志不替代人的决定。</p>
<p>若返工改变待接受代码，在同一 WorkItem 更新候选和当前报告，决定保持待决定；若接受，由同一次 Closeout 同步当前决定并按项目流程执行。</p></section>'''
css = '''*{box-sizing:border-box}html{background:#f2f5f8;color:#152535;font-family:"Segoe UI","Microsoft YaHei",sans-serif}body{max-width:1120px;margin:0 auto;padding:32px 34px 60px;line-height:1.7}header{padding:0 4px 24px}h1{font-size:34px;line-height:1.3;letter-spacing:-.6px;margin:8px 0}h2{font-size:24px;margin:0 0 16px}h3{font-size:18px;margin:16px 0 5px}p{margin:8px 0 13px}header p,.eyebrow{color:#546579}.eyebrow{font-size:13px;letter-spacing:2px}section{background:white;padding:26px 30px;border:1px solid #dae2eb;border-radius:10px;margin:0 0 22px}.human{border-top:5px solid #267a73}.human h2{font-size:18px;color:#267a73}.human h3{margin-top:12px}.decision{background:#fff5da;padding:10px 16px;border-radius:5px}.decision span{font-weight:700;color:#785516}.cards{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{border-top:2px solid #c8dedb;padding:0 6px}.evidence{font-size:12px;color:#596a77;overflow-wrap:anywhere}.evidence b{color:#17685b}a{color:#156d7e;text-decoration-thickness:1px;text-underline-offset:3px}code{font-size:13px;overflow-wrap:anywhere}li{margin-bottom:12px}table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:12px;border-bottom:1px solid #dae2eb}th{background:#f0f5f6}.table-wrap{overflow:auto}ul{padding-left:22px}@media(max-width:720px){body{padding:18px 12px}section{padding:20px 18px}.cards{grid-template-columns:1fr}h1{font-size:28px}td,th{padding:8px;font-size:13px}}@media print{html{background:white}body{max-width:none;padding:0}section{break-inside:avoid}.cards{display:block}article{break-inside:avoid}}'''
(ITEM / 'REPORT.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><style>{css}</style><main>{body}</main></html>\n', encoding='utf-8')
print('Generated REPORT.md and REPORT.html from verified observations')
