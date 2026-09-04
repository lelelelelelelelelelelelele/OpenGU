# -*- coding: utf-8 -*-
"""Generate the paired decision surface from one verified observation set."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OBS = json.loads((HERE/'observations.json').read_text(encoding='utf-8'))


def run(test, experiment):
    case = next(c for c in OBS['consumer_evidence'] if c['test'] == test)
    return next(r for r in case['evidence']['consumer_runs'] if r['experiment_id'] == experiment)


def main():
    title = 'AAGU-026 · 科研计划与执行上下文正交'
    delta = '科研 YAML 现在由 Dataset/Split、Selector、Unlearning、Evaluation 四类实例组成，大表只列执行需要的引用和组合；research_question 与 decision_owner 留在 WorkItem／实验说明，不再进入可执行协议。真实 target-direct formal 表引用 17 个 Selector 小表、1 个 GNNDelete 小表和 1 个 Evaluation 小表。Device、Store、Runtime、Output 和执行授权已移交 SyncMate／项目执行策略。'
    observations = '真实 CPU 消费者已分别跑通 Selector-only、已有 Selection→GU，以及 1 Dataset/Split × 1 Selector × 1 GU × 1 Evaluation。多引用大表只是调度这些独立 cell，不形成整包缓存身份。改变 Evaluation 只改变 Evaluation receipt，Selection 与 GU Result 均 HIT；设备与 Torch/CUDA build 只进入执行回执，不再进入 Score/Checkpoint 身份。'
    decision = '建议接受本 Block 的返工候选。123 项 CPU／集成检查、182 项 SyncMate 检查通过；SyncMate 检查绑定已落地主线 main@a4d1c5d，未使用正在验收的 SM-004 候选。主项目 3,990 个历史结果文件及所列缓存目录前后哈希一致。由用户决定接受、继续返工或拒绝；正式 GPU、SSH 部署和科学结果接纳仍未执行。'
    scenarios = [
        ('原子运行与简写小表', '可解析计划展示一个独立的 1×1×1 cell；真实 CPU 测试分别覆盖 Selector-only、已有 Selection→GU 和 Selector→GU→Evaluation。五 Selector × 两 GU 的大表只是同类 cell 的批量调度。B-Hutch 32 沿用默认 probes=32，64 小表只增加 probes=64。', 'PASS', 'experiment_one_selector_one_gu.yaml / test_real_gu_consumes_existing_selection_without_producer / test_evaluation_is_independent_and_unimplemented_case_fails_closed'),
        ('运行上下文正交', '实验 YAML 出现 device、store_root、runtime_root、output、execution_authorized 或 execution_binding 会被拒绝。项目 ExecutionContext 固定一个 results/cache_v2，并按 job ID 生成 checkpoint、scratch 和 output；设备与 Torch/CUDA 版本只在 execution receipt。', 'PASS', 'test_operational_fields_are_rejected_and_context_is_external / test_project_context_owns_fixed_store_runtime_device_and_output / test_device_and_library_build_are_execution_provenance_not_recipe_identity'),
        ('Evaluation 独立与失败关闭', 'post_unlearning_utility 可独立选取指标；只改变其指标集合时既有 Selection 和 GU Result 均 HIT，只有 evaluation receipt 改变。普通 modular lane 没有 exact retrain，因此 post_unlearning_utility_and_retrain_gap 会在任何 Store 写入前拒绝；target-direct SyncMate lane 明确绑定了它的现有三模型消费者。', 'PASS / BOUNDED', 'test_evaluation_is_independent_and_unimplemented_case_fails_closed / test_formal_selector_reference_is_consumed_and_frozen'),
        ('跨实验复用', '同一图、模型和 Selector 换 experiment_id 后重跑，三个 Score 与 Selection 均 HIT，身份完全一致。通用 TracIn 另验证 case_id 变化。', 'PASS', 'test_method_cold_warm_and_hutch_isolation / test_trained_selector_is_independent_of_gu_parameters_and_producer'),
        ('GU 变化不反向污染选点', '真实 GNNDelete 的 unlearn_lr 从 0.01 改为 0.02，自己的 GU Result MISS；既有 Selection 直接复用。GU 换 GIF，或替换 GIF 调用的 GCN reason_once 实现，Selection 仍 HIT，GU Result 正确 MISS。', 'PASS', 'test_real_gu_consumes_existing_selection_without_producer / test_real_gu_method_and_default_equivalence / test_actual_dependency_implementation_changes'),
        ('单方法变更', 'B-Hutch probes 从默认 32 改为 2，只有 B-Hutch 的 Score/Selection MISS；degree、TracIn 都 HIT。替换 degree 实现只重算 degree；改变 LiSSA 声明默认值只重算消费它的 B-Hutch。', 'PASS', 'test_method_cold_warm_and_hutch_isolation / test_actual_dependency_implementation_changes'),
        ('默认值与预算', '省略 B-Hutch 和 GNNDelete 默认参数与显式填写同值的实例命中相同身份。K 从 1 改为 2，预算无关 Score HIT，Selection MISS 且确有两个节点。改文件名和实验编号不影响身份。', 'PASS', 'test_default_expansion_and_budget_reuse / test_real_gu_method_and_default_equivalence'),
        ('两侧模型独立', 'Selector 使用真实 SGC、GU 使用真实 GCN/GNNDelete，运行完成且两侧 checkpoint 不同；相同训练身份则复用同一 checkpoint。提供 metadata 不匹配的 checkpoint 被拒绝。', 'PASS', 'test_different_selector_and_gu_backbones / test_mismatched_persisted_data_and_checkpoint_rejected'),
        ('入口与无 producer 消费', '独立进程运行 experiments/run.py 的计划 dry-run；不带外部 ExecutionContext 的实际执行被拒绝。测试随后用显式验证上下文完成 selector，再把其 Selection 交给 GNNDelete；禁止 selector producer 后，Selection→GU 冷／热仍成功。', 'PASS', 'test_real_command_entry_selector_and_existing_selection / test_real_gu_consumes_existing_selection_without_producer'),
        ('精确输入拒绝', '未知参数、错误类型、NaN、重复 YAML 字段、大表隐式 override、错误 Selection content_hash、被改变的数据文件以及错误 checkpoint metadata 均失败。未重新划分或修复输入。', 'PASS', 'test_invalid_method_configuration_fails_before_store / test_yaml_duplicate_and_implicit_override_rejected / test_missing_and_wrong_identity_fail_before_execution / test_mismatched_persisted_data_and_checkpoint_rejected'),
        ('原科研公式', '以同一真实 GCN 六个 checkpoint，把原 point、graph、Hessian 与轨迹表达式同逐方法消费者对照；17 项绝对差均为 0，随后全部 17 个 Score/Selection 热命中且禁止 producer 调用。', 'PASS', 'test_all_seventeen_methods_match_pre_refactor_formulas'),
        ('正式 SyncMate 链路', 'target-direct formal 科研表已从内联方法名改为 17 个 Selector 引用，并独立引用 GNNDelete 与 retrain-gap Evaluation；引用内容由 stage 校验。GPU 名称、CUDA 序号和所有运行路径来自 SyncMate preflight／项目策略。静态 recipe 的配置 SHA 已同步。', 'PASS / NOT OBSERVED', 'test_target_direct_syncmate_stage.py / test_syncmate.py'),
    ]
    cold = run('test_method_cold_warm_and_hutch_isolation', 'cold')
    warm = run('test_method_cold_warm_and_hutch_isolation', 'different_experiment')
    changed = run('test_method_cold_warm_and_hutch_isolation', 'hutch2')
    identity_rows = []
    for i, name in enumerate(('degree', 'B-Hutch', 'TracIn point cp3')):
        a,b,c = [r['selectors'][i]['score'] for r in (cold,warm,changed)]
        identity_rows.append([name, a['recipe_hash'][:12], 'MISS → HIT', c['recipe_hash'][:12], 'HIT' if c['hit'] else 'MISS'])
    protected = next(r for r in OBS['protected_roots'] if r['file_count'] == 3990)
    boundaries = [
        '证据使用 20 节点、3 特征、2 类的临时 CPU 图，三个已持久化 mask 为 10/5/5。常规训练 3 epoch、数值对照 6 epoch；GU 使用缩小计算量的真实 GNNDelete/GIF。它证明配置传递和缓存行为，不证明大图性能、IF 近似质量或攻击有效性。',
        '当前模块入口支持 GCN 两层、SGC 三层，GNNDelete/GCN 以及 GIF/GCN、SGC 的节点删除。模型和训练可在小表省略默认值，也可由两侧分别显式覆盖；超出实现的字段和组合直接拒绝。',
        'post_unlearning_utility 已在 modular lane 实际执行。post_unlearning_utility_and_retrain_gap 只在现有 target-direct SyncMate lane 声明可用，因为它需要 model_before、model_unlearned 和同一 Selection 的 exact retrain；本轮未在 SSH/GPU 上重新执行该消费者。Selector 排名比较和正式配对重训练属于 AAGU-015 的实验分析与证据链，不在 026 中注册空消费者。',
        '仓库指标目录记录的历史 GIF/IDEA hop-flip 问题没有在本 Block 被掩盖或宣称修复；本次 Evaluation 表不接纳这些已知受影响指标。旧 retrain seed 问题已有既存修复，本轮没有把代码存在等同于所有 lane 都已完成。',
        '跨 device HIT 的验证边界是身份结构：Score 与 checkpoint Recipe 只保留 dtype 等科研数值语义，CPU/CUDA/Torch build 位于 execution receipt。是否物理 HIT 仍要求执行端能看到同一个完整 Store；本轮没有用可工作的 CUDA 环境做跨设备实跑。',
        '旧 ScoreBundle 活动共同键已移除；复用既有存储格式，每种方法单独保存一个载荷。旧 Artifact 无删除、覆写、迁移或放宽接纳。源项目的缓存目录本来不存在；主项目 results/runs 的 3,990 文件在本轮 Verify 前后逐文件 SHA 一致。',
        'AAGU-001 的既有 SSH 安装失败未在此处理；AAGU-015 的目标、协议和科研接纳选择仍由该任务负责。本 Block 未进行 SSH 写入、正式 GPU、push、install、Apply 或清理。',
        'SyncMate 消费回归绑定已落地主线 `main@a4d1c5d4b779ed822ed2b7ca19d255151958a5dc`。隔离快照中的旧入口 182 项通过；正在验收且已删除 legacy 的 SM-004 分支不属于 026 的依赖基线。',
        'CPU 进程屏蔽 CUDA；CuPy 提示未找到 CUDA 路径，另有依赖弃用提示，均未造成失败。正式 CUDA 行为未被 CPU 通过数代替。',
        '配对报告的 Human Result、唯一待决定投影和本地链接已通过结构检查。浏览器安全策略拒绝自动打开 file:// 页面，因此本轮更新后的桌面与窄屏视觉结果为 NOT OBSERVED；这不升级为视觉 PASS。',
    ]
    provenance = ('观察记录绑定已执行检查的 Git checkpoint `' + OBS['candidate'] + '`。报告完成会推进同一 source branch 的 HEAD；决定对象始终是该分支当前 clean HEAD。最终 Verify 将记录精确 HEAD、与该检查点的报告差异和复用理由。')
    md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', delta, '', '### 核心观察', '', observations, '', '### 当前决定', '', '> 当前验收决定：`待决定`', '', decision, '', '## 逐方法冷／热观察', '', '同一临时 Store：第一次全部 MISS；换实验编号后全部 HIT；只改 B-Hutch probes 后两种无关方法继续 HIT。下表展示 Score Recipe hash 前 12 位，Selection 的变化同样满足此矩阵。', '', '| 方法 | 冷／热相同 Recipe | 冷 → 热 | 改 probes 后 Recipe | 结果 |', '|---|---|---|---|---|']
    md += ['| ' + ' | '.join(row) + ' |' for row in identity_rows]
    md += ['', '完整身份、有效配置、参数来源和 producer 观察见 [observations.json](evidence/observations.json)。', '', '## 核心验收逐项判断', '']
    for name, story, status, test in scenarios:
        md += [f'### {name} — {status}', '', story, '', f'证据：`{test}`。', '']
    md += ['## 历史保护与验证范围', '', f"实际历史目录摘要：`{protected['before_sha256']}`；前后相同，3,990 文件。其余所列缓存根及 linked source 的历史根均无变化。完整逐文件清单保存在忽略的 runtime 中，报告保留各根摘要。", '']
    for paragraph in boundaries:
        md += [paragraph, '']
    md += ['## 候选、复核与后续决定', '', provenance, '', '[WorkItem](WORKITEM.md) · [模块使用说明](../../../docs/modular_experiments.md) · [可重跑验证脚本](evidence/verify.py) · [最终 Verify](../../runtime/aagu-026/final-verification.json)', '', '当前 source branch：`refs/heads/codex/aagu-026-modular-cache`。当前状态为 awaiting_acceptance。Agent 建议接受；用户尚未作决定。接受后才进入同一 Block 的 Closeout，返工继续使用同一 locator。', '']
    (HERE.parent/'REPORT.md').write_bytes('\n'.join(md).encode('utf-8'))
    e=html.escape
    rows=''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in row)+'</tr>' for row in identity_rows)
    cards=''.join(f'<article><div class="row"><h3>{e(name)}</h3><span class="pass">{e(status)}</span></div><p>{e(story)}</p><details><summary>查看证据定位</summary><code>{e(test)}</code></details></article>' for name,story,status,test in scenarios)
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+e(title)+'''</title><style>
    :root{color-scheme:light;--ink:#20333a;--muted:#607178;--line:#d9e2e4;--green:#176348}*{box-sizing:border-box}body{margin:0;background:#f4f6f5;color:var(--ink);font:16px/1.75 "Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1140px;margin:auto;padding:38px 36px 80px}header{border-bottom:2px solid var(--ink);padding-bottom:22px}h1{font-size:32px;line-height:1.4;letter-spacing:-.5px;margin:8px 0}h2{font-size:23px;margin:0 0 18px}h3{font-size:18px;margin:0 0 8px}p{margin:0 0 14px}.eyebrow{letter-spacing:2px;color:var(--green);font-size:12px;font-weight:700}.lead{padding:26px;background:white;border:1px solid var(--line);margin:26px 0}.lead h2{font-size:14px;color:var(--muted);letter-spacing:1px}.lead .segment{margin-bottom:18px}.decision{border-top:1px solid var(--line);padding-top:18px}.badge{display:inline-block;background:#fff1c7;color:#63480b;border:1px solid #e4c774;border-radius:4px;padding:2px 12px;margin-bottom:10px;font-weight:700}.stats{display:flex;gap:14px;flex-wrap:wrap;margin:22px 0}.stats div{flex:1;min-width:180px;padding:16px 20px;background:#e7f0eb;border-left:3px solid var(--green)}.stats strong{font-size:28px;margin-right:10px}.section{margin-top:34px}.table-wrap{overflow:auto;background:white;border:1px solid var(--line);margin-bottom:14px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:14px;border-bottom:1px solid var(--line);white-space:nowrap}th{background:#eaf0ee;color:var(--green)}article{background:white;border:1px solid var(--line);padding:22px;margin:12px 0}.row{display:flex;justify-content:space-between;gap:20px;align-items:baseline}.pass{color:var(--green);font-size:12px;font-weight:700;white-space:nowrap}details{color:var(--muted);font-size:13px}summary{cursor:pointer}code{font:12px/1.7 Consolas,monospace;overflow-wrap:anywhere}a{color:#176d65;text-decoration-thickness:1px;text-underline-offset:3px}.note{color:var(--muted);font-size:14px}.boundary{border-left:3px solid #b8c8c4;padding-left:20px}.footer{margin-top:30px;padding-top:20px;border-top:1px solid var(--line)}@media(max-width:600px){main{padding:20px 18px 50px}h1{font-size:26px}.lead{padding:20px}.row{display:block}.stats{gap:8px}.stats div{min-width:145px;padding:12px}.stats strong{font-size:25px}article{padding:18px}}
    </style><main><header><div class="eyebrow">AAGU-026 / HUMAN ACCEPTANCE</div><h1>科研计划与执行上下文正交</h1><p class="note">引用式科研 YAML · SyncMate 运行策略 · Evaluation 能力边界</p></header><section class="lead" data-workblock-human-result="2.1"><h2>Human Result</h2><div class="segment"><h3>实际增量</h3><p>'''+e(delta)+'''</p></div><div class="segment"><h3>核心观察</h3><p>'''+e(observations)+'''</p></div><div class="decision"><h3>当前决定</h3><span class="badge" data-workblock-decision="pending">待决定</span><p>'''+e(decision)+'''</p></div></section><div class="stats"><div><strong>17 / 17</strong>评分数值一致</div><div><strong>305</strong>检查通过</div><div><strong>3,990</strong>历史文件未变</div></div><section class="section"><h2>逐方法冷／热观察</h2><p>同一临时 Store，先全部 MISS，再跨实验全部 HIT；只改 B-Hutch probes 后，两种无关方法继续命中。Selection 同样满足此矩阵。</p><div class="table-wrap"><table><thead><tr><th>方法</th><th>冷／热 Recipe</th><th>冷 → 热</th><th>改 probes 后</th><th>结果</th></tr></thead><tbody>'''+rows+'''</tbody></table></div><p class="note">表中 hash 为前 12 位。<a href="evidence/observations.json">完整身份、有效配置、参数来源与 producer 观察</a></p></section><section class="section"><h2>核心验收逐项判断</h2>'''+cards+'''</section><section class="section boundary"><h2>历史保护与验证范围</h2><p>历史目录前后摘要相同；3,990 文件逐个验证 SHA。摘要：<code>'''+e(protected['before_sha256'])+'''</code></p>'''+''.join('<p>'+e(p)+'</p>' for p in boundaries)+'''</section><section class="footer"><h2>候选与后续决定</h2><p>'''+e(provenance)+'''</p><p>当前分支：<code>refs/heads/codex/aagu-026-modular-cache</code>。当前状态为 awaiting_acceptance。Agent 建议接受，用户尚未决定；接受后进入同一 Block 的 Closeout，返工沿用同一 locator。</p><p><a href="WORKITEM.md">WorkItem</a> · <a href="../../../docs/modular_experiments.md">模块使用说明</a> · <a href="evidence/verify.py">重跑验证</a> · <a href="../../runtime/aagu-026/final-verification.json">最终 Verify</a> · <a href="REPORT.md">Markdown 报告</a></p></section></main></html>'''
    (HERE.parent/'REPORT.html').write_bytes(page.encode('utf-8'))


if __name__ == '__main__':
    main()
