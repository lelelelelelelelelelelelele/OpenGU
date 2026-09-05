"""Render the requested OpenGU component Smoke and real Timeout evidence."""
import hashlib
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
ITEM = HERE.parent
read = lambda name: json.loads((HERE/name).read_text(encoding='utf-8-sig'))
pilot = read('verification.json')
scope = read('scope-smoke.json')
timeout = read('timeout-smoke.json')
components = read('component-observations.json')
assert pilot['evidence_integrity_passed'] and scope['passed'] and timeout['passed']
assert components['tests']['tests'] == '15' and components['tests']['failures'] == '0'
for name, digest in pilot['sources_sha256'].items():
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest

failed = next(x for x in timeout['cases'] if x['case'] == 'timeout')
title = 'AAGU-002 · OpenGU Smoke Test 与 Timeout 验收'
change = '已完成设备与字段核查、20 节点小图的真实 CPU 组件 Smoke、传输与证据链 Smoke，以及实际子进程的 Timeout 验证。所有运行均为有界软件测试，没有启动 007 正式实验。'
observation = f"组件与实验入口检查 15/15 通过；传输 Smoke 12/12 通过；38 个 recipe 的超时合同字段一致。1 秒预算的小任务实际触发超时，整次处理耗时 {failed['elapsed_seconds']:.3f} 秒，保存 failed 回执、子进程已退出、没有最终成功产物；随后正常任务完成，最终队列 idle。"
decision = 'Agent 建议接受本轮 Smoke 与 Timeout 准备验证。按用户最后澄清，先提供本报告供审阅，当前不写 accepted、不合并或安装。最小正式科研实验和研究结果由 007 单独运行与验收；本次通过不表示完整组件计时或大图成本预测已实现。'
rows = [
 ('设备与环境', '真实 SSH 观察', '固定 gpu4090 身份、唯一活跃检出、RTX 4090 和两端 60 个 Core 文件核验通过；现有 adapter 对缺 GPU 注入和已有输出明确拒绝。'),
 ('实验字段', '38/38 recipe', 'timeout_seconds、recipe ID、完整 Git SHA 和配置 SHA 在实际 Core 执行合同中吻合，预算沿用配方。ready 是检查输出，不是新增的用户参数。'),
 ('Selector / Score / Selection', '20 节点 CPU 实跑', '实际调用现有消费者；冷运行计算，热运行复用；Hutch 参数改变只使对应身份失效。额外单 Selector → 单 GNNDelete 验证构成最小组件链。'),
 ('GU 与 Metrics', '真实 CPU 消费者', 'GNNDelete 使用已有 Selection；禁止 Selector producer 后仍能冷运行/热复用。离线指标独立读取，缺失 Retrain 证据明确拒绝。'),
 ('实验入口', '共 15 项检查通过', '包括上述三个组件场景，以及原子配方、输出合同、缺 GPU、旧输出和非法 recipe 等入口检查。小图训练 3 epochs，GU 2 epochs。'),
 ('传输和证据链', '12/12 Smoke 检查', '3 个示例 Artifact 完成传输、SHA 校验、可信索引和导出；独立临时目录已清理。'),
 ('已有耗时证据', '5 份 summary 哈希吻合', '可读取 Score 基准、本次访问、Selection 时间和 GU 历史时间。HIT 不改写首次基准；未知访问耗时没有填成 0。'),
]
time_rows=[]
for case in timeout['cases']:
    name={'control':'正常对照','timeout':'实际超时','after-timeout':'超时后的正常任务'}[case['case']]
    time_rows.append((name, str(case['timeout_seconds'])+' 秒', f"{case['elapsed_seconds']:.3f} 秒", case['queue_result']['status'],
                     '预期失败；进程退出、无成功产物' if case['case']=='timeout' else '正常完成并保存产物'))
limits=[
 'Timeout 测试在本地临时干净 Git 仓库中使用已安装 Core 的真实队列和 subprocess.run，受控任务本应等待 4 秒，预算为 1 秒。没有 mock 超时异常，也没有改写任何正式 recipe。',
 '表中的处理耗时包含预检、启动和回执开销，不能把约 1.18 秒解释为精确 CPU 计算时间。只确认直接子进程终止，未测试任意后代进程树。',
 '组件 Smoke 使用 CPU；导入时出现本机 RTX 5070 与现有 PyTorch CUDA build 不兼容警告，不代表这些 CPU 测试使用了本机 GPU。正式 GPU 环境仍是既有 SSH 4090。',
 '作业级 timeout 已接通；完整模型准备、GU 访问计时、逐组件首次测量以及大图外推仍有缺口。这些不能写成“所有计时能力已经完成”，也不阻塞当前有限 Smoke 验收。',
 '工具层仍保留预检拒绝后可入队、空预检对象可能被误判的隔离发现；明确拒绝的测试在执行前被挡住。它们不是实际 OpenGU 已在缺 GPU 时运行的证据，本轮不接手 SM-001。',
 '设备证据有时间和版本边界；007 正式运行前仍须重新核对当时的设备、三方代码身份、数据、配方及已有产物。002 不替代其科研接受。',
]
links=[('正常→超时→继续正常：完整回执','evidence/timeout-smoke.json'),('Timeout 可重跑脚本','evidence/timeout_smoke.py'),
 ('15 项测试及 CPU 运行原始证据','evidence/component-smoke.xml'),('组件运行摘要','evidence/component-observations.json'),
 ('38 个合同、传输 Smoke 与耗时证据','evidence/scope-smoke.json'),('真实 SSH 设备观察','evidence/remote-probe.stdout.json'),('同一 WorkItem','WORKITEM.md')]
md=[f'# {title}','','## Human Result','','### 实际增量','',change,'','### 核心观察','',observation,'','### 当前决定','',decision,'','> 当前验收决定：`待决定`','','## 各部件验证','','| 部件 | 证据 | 结果 |','|---|---|---|']
md+=['| '+' | '.join(row)+' |' for row in rows]
md+=['','## Timeout 实测','','| 场景 | 配置上限 | 整次处理耗时 | 作业状态 | 观察 |','|---|---|---|---|---|']
md+=['| '+' | '.join(row)+' |' for row in time_rows]
md+=['','三组验证均 PASS：中间任务的 failed 正是预期结果。三次处理后没有 running 作业，额外 run_once 返回 idle，没有自动重试失败任务。','', '## 结论边界','']+['- '+x for x in limits]
md+=['','## 证据与复核','']+[f'- [{name}]({url})' for name,url in links]
md+=['','此前范围讨论曾把 007 的正式最小实验重复加入 002，后又提出直接接受；用户最后明确先交付 Smoke、Timeout 和验收报告。当前以这一要求为准，历史原始观测保留，不沿用先前的自动 Closeout 建议。','']
(ITEM/'REPORT.md').write_text('\n'.join(md),encoding='utf-8')
e=html.escape
def table(data):
    return ''.join('<tr>'+''.join(f'<td>{e(cell)}</td>' for cell in row)+'</tr>' for row in data)
body=f'''<header><p class="eyebrow">AAGU-002 · OPENGU PREPARATION VERIFICATION</p><h1>Smoke Test 与 Timeout 已验证</h1><p class="badge">15 项组件检查 · 12 项传输检查 · 3 个真实进程任务</p></header>
<section data-workblock-human-result><h2>Human Result</h2><h3>实际增量</h3><p>{e(change)}</p><h3>核心观察</h3><p>{e(observation)}</p><h3>当前决定</h3><p>{e(decision)}</p><p class="decision">当前验收决定：<span data-workblock-decision="pending">待决定</span></p></section>
<section><h2>各部件验证</h2><div class="table"><table><thead><tr><th>部件</th><th>证据</th><th>结果</th></tr></thead><tbody>{table(rows)}</tbody></table></div></section>
<section><h2>Timeout 实测</h2><div class="table"><table><thead><tr><th>场景</th><th>配置上限</th><th>整次处理耗时</th><th>作业状态</th><th>观察</th></tr></thead><tbody>{table(time_rows)}</tbody></table></div><p>三组验证均 PASS：中间任务的 failed 正是预期结果。进程已退出、无成功产物，后续任务正常完成；最终队列 idle，没有自动重试失败任务。</p></section>
<section><h2>结论边界</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in limits)}</ul></section>
<section><h2>证据与复核</h2><ul>{''.join(f'<li><a href="{url}">{e(name)}</a></li>' for name,url in links)}</ul><p>按用户最后要求先交付报告，不沿用此前直接 Closeout 的建议。007 正式实验未运行。</p></section>'''
css='''*{box-sizing:border-box}body{margin:0 auto;max-width:1160px;padding:28px 32px 60px;background:#f3f5f7;color:#182a38;font:16px/1.65 "Segoe UI","Microsoft YaHei",sans-serif}h1{font-size:32px;line-height:1.3;margin:8px 0 16px}h2{font-size:23px;margin:0 0 12px}h3{font-size:18px;margin:12px 0 4px}p{margin:6px 0 12px}.eyebrow{font-size:12px;letter-spacing:1.5px;color:#627181}.badge{font-weight:700;color:#176856}section{padding:24px 28px;margin:20px 0;background:white;border:1px solid #d8e1e7;border-radius:10px}[data-workblock-human-result]{border-top:5px solid #267e70}.decision{background:#fff1d8;padding:8px 14px}.decision span{font-weight:700}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #dde4e9}td:first-child{min-width:130px}th{background:#f1f5f7}td:nth-child(2){min-width:105px}a{color:#146d7f;overflow-wrap:anywhere}li{margin:10px 0}.table{overflow:auto}section p{overflow-wrap:anywhere}@media(max-width:700px){body{padding:16px 12px}section{padding:18px}h1{font-size:28px}}'''
(ITEM/'REPORT.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{css}</style></head><body>{body}</body></html>\n',encoding='utf-8')
print('Generated Smoke and Timeout acceptance report')
