# -*- coding: utf-8 -*-
"""Render the AAGU-005 handoff review from its recorded observations."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
observed = json.loads((HERE / 'repair-observations.json').read_text(encoding='utf-8'))
remote = json.loads((HERE / 'remote-readback.json').read_text(encoding='utf-8'))
suite = ET.parse(HERE / 'repair-tests.xml').getroot().find('testsuite')
assert suite is not None and suite.attrib['failures'] == suite.attrib['errors'] == '0'
assert observed['dependency_local']['ready'] and remote['dependency']['ready']
assert len(observed['atomic_recipes']) == 6 and all(r['status'] == 'PASS' for r in observed['atomic_recipes'])
failures = [r for r in observed['formal_gu_recipe_audit'] if r['status'] == 'FAIL']
assert len(observed['formal_gu_recipe_audit']) == 20 and not failures
assert observed['formal_gu_preflight']['status'] == 'PASS' and observed['formal_config_hash_matches']
checks = json.loads((HERE / 'repair-verification.json').read_text(encoding='utf-8'))
assert len(checks['collection_scenarios']) == 2 and all(x['accepted']['passed'] for x in checks['collection_scenarios'])
accepted = bool(re.search(r'^当前状态:\s*`accepted(?: /[^`]*)?`', (ITEM / 'WORKITEM.md').read_text(encoding='utf-8'), re.M))
decision = '接受' if accepted else '待决定'

title = 'AAGU-005 · OpenGU 与 SyncMate 接入修复'
change = '已修复 OpenGU 消费端的预检参数、静态配置摘要、GNNDelete / Retrain 产物声明、收集后校验与结果表读取。20 个 GU 配方直接复用执行器的文件清单；无需在每个方法结果中生成 collateral.json。'
finding = f"{suite.attrib['tests']} 项相关检查通过。20/20 正式 GU 配方与执行器一致，6/6 原子配方保持一致。临时 CPU 图上真实运行两种方法，再经 SyncMate 收集、SHA 校验、OpenGU 接受检查及结果表读取；重复收集新增 0 个文件。12 类错误均被拒绝。"
recommendation = '建议接受 AAGU-005 本轮约定的代码正确性与 CPU 接入验证范围。旧版 GPU 实测仅作为历史证据；本次修复尚未在远端 GPU 上重跑，也尚未合入或部署。当前由用户作验收决定。'

delivery = [
    ('原子实验入口与配方', 'Degree、B-Hutch first/warm、D-full Selector-only、自动回传及新版 handoff 共 6 个固定配方，绑定配置摘要、运行身份与输出。', 'experiments/syncmate_atomic_stage.py；scripts/syncmate/opengu_recipes.py'),
    ('启动参数隔离', '隔离 --recipe，避免被 OpenGU import-time 参数解析误读。失败与拒绝不会进入训练。', 'experiments/syncmate_atomic_stage.py'),
    ('输出交接', '配方与执行器共用 modular_output_path；执行前核对 queue receipt 的 output_contract。', 'scripts/syncmate/opengu_layout.py；experiments/modular_execution.py'),
    ('Core 安装身份', '消费端核对 0.4.0 的完整文件集合与内容哈希；设备配置保留接入事实，项目代码拥有结果规则。', 'scripts/syncmate/core_dependency.json；verify_core_dependency.py；opengu_adapter.py'),
]
history = [
    ('Degree → GNNDelete → utility', '真实 RTX 4090 运行、返回 summary 并校验；重复收集为 0。', 'OpenGU 93e6e56b / Core 0.3.1', '证明该版本真实执行与回传链。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/verify-final.json'),
    ('B-Hutch 32 probes first / warm', 'Score、Selection、GU 首遍 MISS，热读 HIT 且 producer=false；传输校验通过。原记录保留 F1 差值读回失败。', 'OpenGU 6dc1aa92 / Core 0.3.1', '复用缓存与传输证据；不把旧指标失败改成 PASS。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/b-hutch32/cache-comparison.json'),
    ('D-full Selector-only', '1895 个有限分数、完整降序排名、18 个节点；1 Selector / 0 GU / 0 Evaluation。', 'OpenGU 53e1da5b / Core 0.3.1', '证明该版本 Selector 输出和回传。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/d-full/verification.json'),
    ('D-full warm 自动回传', 'checkpoint / Score / Selection 全 HIT，producer=false；同一后台流程完成回传和 SHA 校验。', 'OpenGU e27425e6 / Core 0.3.2', '证明旧版无需 Agent 补 collect；不覆盖 0.4.0 的新 GPU 运行。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/auto-return/verification.json'),
    ('0.4.0 执行交接', 'Core 91 项、OpenGU 221 项检查；两个真实本地 Git 检出、独立 worker、自动回传及改设备后的手动补收通过。', 'OpenGU e8f23a94 / Core 5dd378cb', '保留当时的 Core 交接证据；本轮变更部分另以 311 项检查核验，未新增 GPU 实测。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/output-handoff/verification.json'),
]
gaps = [
    ('预检与配置摘要', '此前配置路径误传为 ratio，gate_only 丢失；配置摘要也停留在 028 增加 Retrain 之前。现按登记配方准确传递参数并固定当前配置摘要，20 项真实预检签名检查通过。', '正式设备、Selection 前置与矩阵授权继续由原 preflight 检查；测试没有绕过正式运行门槛。', '../../../scripts/syncmate/opengu_adapter.py'),
    ('独立方法产物声明', '此前只声明 GNNDelete 与旧 collateral 文件。现在直接复用执行器 gu_artifacts：gate 8 文件、17-selector stage 136 文件，完整包含 GNNDelete 与 Retrain。20 个配方全部一致。', '方法参数同时与实际矩阵消费者对照，避免配方和运行入口各自维护不同条件。', '../../../scripts/syncmate/opengu_recipes.py'),
    ('收集后的内容与身份核验', '现从已收集的 predictions.npz 解析完整模型/预测，核对 SHA、Recipe/Artifact/内容身份、三处 Output 引用、Selection、checkpoint、方法条件和共享输入，再重算单方法指标。', '真实 CPU 结果通过；缺少 Retrain、重复/未验证索引、Git 不符、字节损坏、引用/指标/checkpoint/Selection 不符、预测缺失/无效、方法参数不符均拒绝。', '../../../scripts/syncmate/opengu_method_output.py'),
    ('结果表与相邻入口', 'results 按独立输出格式读取两种方法，保留完整策略名称，跨方法比较仍是后处理。基础 smoke Adapter 按需加载实验模块，相邻 M1 独立入口也通过回归。', '没有新建兼容分支或复制 Core；旧测试中的假 collateral、无效 npz 通过案例已被真实生产与收集测试替代。', '../../../scripts/syncmate/opengu_results.py'),
]
notes = [
    '代码检查使用本地项目 Python 与 Core 0.4.0。完整测试包括 SyncMate、完整与基础 Adapter、Core 依赖、原子入口、target-direct stage、独立 Retrain/输出及新增 GU 收集测试；311 passed、0 failure/error/skip。',
    '两个正向收集场景分别覆盖 gate 与 stage 接受路径。执行和收集使用临时目录与真实本地 Git runner；测试图只有 20 个节点、10 个候选、k=1，正式配方与数据未被改写。正式 20 个配方另做完整静态合同与预检参数检查。',
    '收集与接受期间禁止模型 forward 和训练更新；远端 Cache V2 没有复制到 collector，源 Store 的前后文件哈希不变。这里证明的是代码消费闭环，不把 CPU 场景写成新的 GPU 实验。',
    '最终产品检查点为 ' + checks['product_checkpoint'] + '。后续提交只更新本 item 的证据/报告/状态和看板；实现、依赖、配置与测试无差异时复用该检查结果。CLI 编译与独立 smoke 亦通过。',
    '最初失败证据 observations.json、13 项旧检查及历史实测保留；新核验写入 repair-observations.json 和 repair-tests.xml，未把过去失败改写成过去通过。',
    'F1 冷热差异来自保存基础指标时舍入后又重算差值；028 已改为保存完整浮点精度，相关回归继续通过。',
    '此前已读回本地与 SSH Core 0.4.0 的 60 文件依赖一致；SSH OpenGU 仍是已落地主线 c9e094c5。本次修复是独立分支上的待验收代码，不能说远端已安装此修复。',
]
links = [
    ('当前 WorkItem', 'WORKITEM.md'),
    ('修复后的合同与预检观察', 'evidence/repair-observations.json'),
    ('311 项原始测试结果', 'evidence/repair-tests.xml'),
    ('真实收集、接受与结果表证据', 'evidence/repair-verification.json'),
    ('修复核验说明', 'evidence/repair-verification.md'),
    ('最初缺口观察（历史）', 'evidence/observations.json'),
    ('只读跨接口核对脚本', 'evidence/audit.py'),
    ('028 已接受的独立方法与 Metrics 说明', '../AAGU-028/REPORT.md'),
    ('SM-005 原始报告', 'E:/project/SyncMate/.workblock/items/SM-005/REPORT.md'),
]

md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', change, '',
      '### 核心观察', '', finding, '', '### 当前决定', '', recommendation, '',
      f'> 当前验收决定：`{decision}`', '', '## 此前已经交付的 OpenGU 改动', '',
      '| 内容 | 已实现行为 | 主要位置 |', '|---|---|---|']
md += ['| ' + ' | '.join(row) + ' |' for row in delivery]
md += ['', '最后一轮输出交接覆盖 13 个文件；本轮承接这些既有 Git 交付，并修复当前正式 GU 消费端。', '', '## 真实运行证据与适用范围', '']
for name, fact, version, reuse, link in history:
    md += [f'### {name}', '', fact, '', f'版本：`{version}`。{reuse} [原始证据]({link})', '']
md += ['## 本轮修复与验证', '']
for name, fact, followup, link in gaps:
    md += [f'### {name}', '', fact, '', f'**核验边界**：{followup} [源码位置]({link})', '']
md += ['## 本轮核验与解释', ''] + ['- ' + note for note in notes]
md += ['', '## 下一步', '', '由用户验收当前代码与 CPU 接入验证结果；接受后沿用同一 AAGU-005 完成合入和已登记的同步动作。新的正式 GPU 运行仍按项目门槛及其独立授权执行。', '', '## 证据入口', '']
md += [f'- [{label}]({url})' for label, url in links]
(ITEM / 'REPORT.md').write_text('\n'.join(md) + '\n', encoding='utf-8')

e = html.escape
def href(url):
    return e(Path(url).as_uri() if re.match(r'^[A-Za-z]:/', url) else url)

table = ''.join('<tr>' + ''.join('<td>' + e(c) + '</td>' for c in row) + '</tr>' for row in delivery)
history_html = ''.join(f'<article><h3>{e(n)}</h3><p>{e(f)}</p><p class="meta">{e(v)}</p><p>{e(r)} <a href="{href(url)}">原始证据</a></p></article>' for n,f,v,r,url in history)
gap_html = ''.join(f'<article class="gap"><h3>{e(n)}</h3><p>{e(f)}</p><p><b>核验边界：</b>{e(followup)} <a href="{href(url)}">源码位置</a></p></article>' for n,f,followup,url in gaps)
body = f'''<header><p class="eyebrow">OpenGU / AAGU-005 / 接入交接</p><h1>OpenGU 接入已修复<br>311 项检查通过</h1></header>
<section data-workblock-human-result class="human"><h2>Human Result</h2>
<h3>实际增量</h3><p>{e(change)}</p><h3>核心观察</h3><p>{e(finding)}</p>
<h3>当前决定</h3><p>{e(recommendation)}</p><p class="decision">当前验收决定：<span data-workblock-decision="{'accepted' if accepted else 'pending'}">{decision}</span></p></section>
<section><h2>此前已经交付的 OpenGU 改动</h2><div class="table"><table><thead><tr><th>内容</th><th>已实现行为</th><th>主要位置</th></tr></thead><tbody>{table}</tbody></table></div><p>最后一轮输出交接覆盖 13 个文件；本轮承接这些既有 Git 交付，并修复当前正式 GU 消费端。</p></section>
<section><h2>真实运行证据与适用范围</h2><div class="cards">{history_html}</div></section>
<section><h2>本轮修复与验证</h2>{gap_html}</section>
<section><h2>本轮核验与解释</h2><ul>{''.join('<li>'+e(n)+'</li>' for n in notes)}</ul></section>
<section><h2>下一步</h2><p>由用户验收当前代码与 CPU 接入验证结果；接受后沿用同一 AAGU-005 完成合入和已登记的同步动作。新的正式 GPU 运行仍按项目门槛及其独立授权执行。</p></section>
<section><h2>证据入口</h2><ul>{''.join(f'<li><a href="{href(url)}">{e(label)}</a></li>' for label,url in links)}</ul></section>'''
css = '''*{box-sizing:border-box}html{background:#f3f5f6;color:#213340;font-family:"Segoe UI","Microsoft YaHei",sans-serif}body{max-width:1140px;margin:auto;padding:28px 34px 52px;line-height:1.72}header{padding:0 4px 18px}.eyebrow{color:#546a76;font-size:13px;letter-spacing:1.2px;margin:0}h1{font-size:32px;line-height:1.32;margin:8px 0 0}h2{font-size:23px;margin:0 0 16px}h3{font-size:17px;margin:12px 0 5px}p{margin:7px 0 12px}p,li{overflow-wrap:anywhere}section{background:#fff;border:1px solid #d9e1e5;border-radius:10px;margin-bottom:20px;padding:24px 28px}.human{border-top:5px solid #b97c25}.human h2{font-size:17px;color:#92601c;margin-bottom:8px}.decision{padding:9px 14px;background:#fff2dc;border-radius:5px}.decision span{font-weight:700;color:#8e5917}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #dce4e7;overflow-wrap:anywhere}th{background:#edf3f4}td:first-child{width:20%;font-weight:600}td:last-child{width:29%;font-size:12px}.cards{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{padding:0 6px;border-top:2px solid #b7d4cf}.meta{font-size:12px;color:#55737b}.gap{border-top:2px solid #d8b58d;padding:9px 3px;margin:12px 0}a{color:#17677b;text-underline-offset:3px;overflow-wrap:anywhere}li{margin-bottom:12px}ul{padding-left:22px}.table{overflow:auto}code{overflow-wrap:anywhere}@media(max-width:720px){body{padding:18px 12px}section{padding:18px 16px}.cards{grid-template-columns:1fr}h1{font-size:27px}h2{font-size:21px}td,th{padding:8px;font-size:12px}}@media print{html{background:white}body{max-width:none;padding:0}section,article{break-inside:avoid}.cards{display:block}}'''
(ITEM / 'REPORT.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{css}</style></head><body><main>{body}</main></body></html>\n', encoding='utf-8')
print('Rendered AAGU-005 repair report with verified CPU scope and pending decision.')
