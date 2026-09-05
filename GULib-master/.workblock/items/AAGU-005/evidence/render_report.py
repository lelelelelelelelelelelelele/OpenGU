# -*- coding: utf-8 -*-
"""Render the AAGU-005 handoff review from its recorded observations."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
observed = json.loads((HERE / 'observations.json').read_text(encoding='utf-8'))
remote = json.loads((HERE / 'remote-readback.json').read_text(encoding='utf-8'))
suite = ET.parse(HERE / 'targeted-checks.xml').getroot().find('testsuite')
assert suite is not None and suite.attrib['failures'] == suite.attrib['errors'] == '0'
assert observed['dependency_local']['ready'] and remote['dependency']['ready']
assert len(observed['atomic_recipes']) == 6 and all(r['status'] == 'PASS' for r in observed['atomic_recipes'])
failures = [r for r in observed['formal_gu_recipe_audit'] if r['status'] == 'FAIL']
assert len(failures) == 20 and observed['formal_gu_preflight']['status'] == 'FAIL'
accepted = bool(re.search(r'^当前状态:\s*`accepted(?: /[^`]*)?`', (ITEM / 'WORKITEM.md').read_text(encoding='utf-8'), re.M))
decision = '接受' if accepted else '待决定'

title = 'AAGU-005 · OpenGU 接入交接与当前缺口'
change = '把 SM-005 此前直接提交到 OpenGU 的消费端改动、真实运行与代码检查证据归入同一 AAGU-005。已核对主线承接、SSH 同步和双端 Core 依赖。本轮新增交接报告与只读核对脚本，没有修改实验或接入实现。'
finding = '6 个 SM-005 原子配方的配置与输出合同一致，13 项针对性检查通过；本地与 SSH 均通过 Core 0.4.0 的 60 文件检查。同时发现 20 个 target-direct 正式 GU 配方与当前执行器的产物声明不一致，预检调用还把配置路径误传给删除比例。已有原子链路可用，但全部正式 GU 接入尚未对齐。'
recommendation = '建议先补齐下方正式 GU 接口缺口，再接受 AAGU-005 的完整接入范围。SM-005 已接受的 Core 与原子实验成果继续有效。本报告由用户决定；当前保留待决定，不把已落地代码或局部测试通过写成 AAGU-005 整体接受。'

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
    ('0.4.0 执行交接', 'Core 91 项、OpenGU 221 项检查；两个真实本地 Git 检出、独立 worker、自动回传及改设备后的手动补收通过。', 'OpenGU e8f23a94 / Core 5dd378cb', '本轮复用相同产品文件的证据；新协议未新增 GPU 实测。', 'E:/project/SyncMate/.workblock/items/SM-005/evidence/output-handoff/verification.json'),
]
gaps = [
    ('预检参数传错', 'OpenGU Adapter 调用 preflight_gu(stage, config_path)，但消费者签名为 preflight_gu(stage, ratio, config_path, gate_only=...)。只读复现得到 TypeError：float() 不能接收 WindowsPath，且尚未进入设备或数据预检。', '正确传递登记的 ratio、配置路径和 gate_only；用真实消费者签名核验。', '../../../scripts/syncmate/opengu_adapter.py'),
    ('配方与执行器产物不一致', '队列配方仍要求 GNNDelete 的 attack.json、collateral.json、predictions.npz、_meta.json；028 后执行器输出 output-references.json，并同时枚举独立 GNNDelete / Retrain。2 个 gate 配方各声明 4 个文件、执行器枚举 8 个；18 个整组配方各声明 68 个、执行器枚举 136 个。20/20 集合不相等。', '让配方、执行器与收集声明消费同一已确认单方法产物合同；不能只改文件名而遗漏 Retrain。', '../../../scripts/syncmate/opengu_recipes.py'),
    ('消费端接受检查仍依赖旧 collateral', 'OpenGU 的 GU gate / stage 接受检查仍读取 collateral.json 和旧比较结果；这与独立方法输出、收集后计算差值的当前合同不一致。该项依据源码定位，尚未运行端到端正式 GU 作业。', '按独立方法输出及其内容/依赖身份完成消费检查；跨方法比较保持后处理。', '../../../scripts/syncmate/opengu_acceptance.py'),
]
notes = [
    '本轮检查调用真实配方与真实执行器的产物枚举函数，比较各自输出集合；它不提交任务、不读取正式数据、不运行 GPU 或训练。13 项既有针对性检查覆盖原子入口、拒绝路径和指标无损读回。',
    '这些缺口属于 OpenGU 消费端。现有测试各自使用自己的配方/执行器夹具，局部通过不能证明两侧合同一致；本次跨接口比较补出了这层证据。',
    'F1 读回差异的根因是保存时先舍入基础指标、读回后重新计算差值。028 已改为保存原始浮点精度，本轮无损往返检查通过；历史四舍五入后的结果文件没有被改写或自动修复。',
    'OpenGU 当前产品基线与 SSH 均为 c9e094c55b42b2833fb24fcef5fe08f057605f68，包含 e8f23a94 的消费端交付。上述接入文件相对交接提交未改，后续底层独立方法变更的复用边界由 028 检查与本次跨接口核对共同说明。',
    'SM-005 已在 6a938e2a 接受、合并、推送；双端 0.4.0 安装已验证。其安装回执保留 partial，仅因本地临时 payload 删除被自动审批拒绝。AAGU-005 不处理该清理、不重放安装。',
    '重建 wheel 的容器 SHA-256 为 ab22f394…，原消费端清单记录 a6ecf6de…；两端实际 60 个载荷文件均与原精确清单匹配。当前依赖验证按内容身份通过，不把两个 wheel 容器哈希说成相同。',
]
links = [
    ('当前 WorkItem', 'WORKITEM.md'),
    ('本轮完整观察与原证据哈希', 'evidence/observations.json'),
    ('只读跨接口复现脚本', 'evidence/audit.py'),
    ('13 项检查的原始结果', 'evidence/targeted-checks.xml'),
    ('SSH 代码与 Core 依赖读回', 'evidence/remote-readback.json'),
    ('028 已接受的独立方法与 Metrics 说明', '../AAGU-028/REPORT.md'),
    ('SM-005 原始报告', 'E:/project/SyncMate/.workblock/items/SM-005/REPORT.md'),
]

md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', change, '',
      '### 核心观察', '', finding, '', '### 当前决定', '', recommendation, '',
      f'> 当前验收决定：`{decision}`', '', '## 此前已经交付的 OpenGU 改动', '',
      '| 内容 | 已实现行为 | 主要位置 |', '|---|---|---|']
md += ['| ' + ' | '.join(row) + ' |' for row in delivery]
md += ['', '最后一轮输出交接覆盖 13 个文件；这里承接既有 Git 交付，不创建重复实现。', '', '## 真实运行证据与适用范围', '']
for name, fact, version, reuse, link in history:
    md += [f'### {name}', '', fact, '', f'版本：`{version}`。{reuse} [原始证据]({link})', '']
md += ['## 当前发现的正式 GU 接口缺口', '']
for name, fact, followup, link in gaps:
    md += [f'### {name}', '', fact, '', f'**需修复**：{followup} [源码位置]({link})', '']
md += ['## 本轮核验与解释', ''] + ['- ' + note for note in notes]
md += ['', '## 下一步', '', '沿用 AAGU-005，先修复正式 GU 的预检、产物声明和接受检查，增加配方→执行器→收集的真实消费验证；不重新实现已交付原子链路。核验通过后更新本报告，再交用户决定完整接入范围是否接受。', '', '## 证据入口', '']
md += [f'- [{label}]({url})' for label, url in links]
(ITEM / 'REPORT.md').write_text('\n'.join(md) + '\n', encoding='utf-8')

e = html.escape
def href(url):
    return e(Path(url).as_uri() if re.match(r'^[A-Za-z]:/', url) else url)

table = ''.join('<tr>' + ''.join('<td>' + e(c) + '</td>' for c in row) + '</tr>' for row in delivery)
history_html = ''.join(f'<article><h3>{e(n)}</h3><p>{e(f)}</p><p class="meta">{e(v)}</p><p>{e(r)} <a href="{href(url)}">原始证据</a></p></article>' for n,f,v,r,url in history)
gap_html = ''.join(f'<article class="gap"><h3>{e(n)}</h3><p>{e(f)}</p><p><b>需修复：</b>{e(followup)} <a href="{href(url)}">源码位置</a></p></article>' for n,f,followup,url in gaps)
body = f'''<header><p class="eyebrow">OpenGU / AAGU-005 / 接入交接</p><h1>已有链路可复用<br>正式 GU 接口仍需对齐</h1></header>
<section data-workblock-human-result class="human"><h2>Human Result</h2>
<h3>实际增量</h3><p>{e(change)}</p><h3>核心观察</h3><p>{e(finding)}</p>
<h3>当前决定</h3><p>{e(recommendation)}</p><p class="decision">当前验收决定：<span data-workblock-decision="{'accepted' if accepted else 'pending'}">{decision}</span></p></section>
<section><h2>此前已经交付的 OpenGU 改动</h2><div class="table"><table><thead><tr><th>内容</th><th>已实现行为</th><th>主要位置</th></tr></thead><tbody>{table}</tbody></table></div><p>最后一轮输出交接覆盖 13 个文件；这里承接既有 Git 交付，不创建重复实现。</p></section>
<section><h2>真实运行证据与适用范围</h2><div class="cards">{history_html}</div></section>
<section><h2>当前发现的正式 GU 接口缺口</h2>{gap_html}</section>
<section><h2>本轮核验与解释</h2><ul>{''.join('<li>'+e(n)+'</li>' for n in notes)}</ul></section>
<section><h2>下一步</h2><p>沿用 AAGU-005，先修复正式 GU 的预检、产物声明和接受检查，增加配方→执行器→收集的真实消费验证；不重新实现已交付原子链路。核验通过后更新本报告，再交用户决定完整接入范围是否接受。</p></section>
<section><h2>证据入口</h2><ul>{''.join(f'<li><a href="{href(url)}">{e(label)}</a></li>' for label,url in links)}</ul></section>'''
css = '''*{box-sizing:border-box}html{background:#f3f5f6;color:#213340;font-family:"Segoe UI","Microsoft YaHei",sans-serif}body{max-width:1140px;margin:auto;padding:28px 34px 52px;line-height:1.72}header{padding:0 4px 18px}.eyebrow{color:#546a76;font-size:13px;letter-spacing:1.2px;margin:0}h1{font-size:32px;line-height:1.32;margin:8px 0 0}h2{font-size:23px;margin:0 0 16px}h3{font-size:17px;margin:12px 0 5px}p{margin:7px 0 12px}section{background:#fff;border:1px solid #d9e1e5;border-radius:10px;margin-bottom:20px;padding:24px 28px}.human{border-top:5px solid #b97c25}.human h2{font-size:17px;color:#92601c;margin-bottom:8px}.decision{padding:9px 14px;background:#fff2dc;border-radius:5px}.decision span{font-weight:700;color:#8e5917}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #dce4e7;overflow-wrap:anywhere}th{background:#edf3f4}td:first-child{width:20%;font-weight:600}td:last-child{width:29%;font-size:12px}.cards{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{padding:0 6px;border-top:2px solid #b7d4cf}.meta{font-size:12px;color:#55737b}.gap{border-top:2px solid #d8b58d;padding:9px 3px;margin:12px 0}a{color:#17677b;text-underline-offset:3px;overflow-wrap:anywhere}li{margin-bottom:12px}ul{padding-left:22px}.table{overflow:auto}code{overflow-wrap:anywhere}@media(max-width:720px){body{padding:18px 12px}section{padding:18px 16px}.cards{grid-template-columns:1fr}h1{font-size:27px}h2{font-size:21px}td,th{padding:8px;font-size:12px}}@media print{html{background:white}body{max-width:none;padding:0}section,article{break-inside:avoid}.cards{display:block}}'''
(ITEM / 'REPORT.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{css}</style></head><body><main>{body}</main></body></html>\n', encoding='utf-8')
print('Rendered AAGU-005 report with explicit verified scope and open integration findings.')
