"""Render the paired configuration-checkpoint report from verified definitions."""
from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
ROOT = HERE.parents[3]


def main():
    summary = json.loads((HERE / 'definition-summary.json').read_text(encoding='utf-8'))
    counts = summary['counts']
    title = 'AAGU-015 · Selector 两阶段实验与证据'
    increment = (f"按用户澄清，015 交付实验方案与可执行链路，并用必要的最小验证确认接通。已有 {counts['stage_s']} 个阶段 S cell "
                 f"和 {counts['stage_u']} 个阶段 U 候选 cell 表示方案覆盖范围；424 份生成 YAML 与既有展开证据保留。全量实验和完整科研结论不属于本次验收要求。当前链路尚未完成。")
    observations = [
        ('NOT CONFIRMED（方案完整性）', '两阶段范围、Q1–Q4、候选参数与解释边界已有定义；用户已明确 015 负责方案和链路。逐项比较设计及指标输入仍需在实现中完整对齐。'),
        ('PASS（配置与展开）', '三个 Dataset/Split、17 个 Selector、两种 GU 和评价引用可解析。324 张计划表展开为 306/612 cell；两个真实 CLI dry-run 成功，未知字段、错误引用和漂移被拒绝，未创建研究结果。'),
        ('NOT OBSERVED（数据接缝）', '读取、验证和绑定数据，以及候选/checkpoint 准备的链路还未在 015 接通。现有测试只证明空 Dataset/Split 引用会在模型、Store 和结果写入前停止。'),
        ('NOT OBSERVED（S 链路验证）', '还需把 Score、排名、Selection、相关性/选集比较和分段计时接入最小链路验证。此处缺的是可运行接口的证据，不是三数据集全量对照和成本结果。'),
        ('NOT CONFIRMED（U 链路）', 'U 计划只声明固定 selection_input，没有 selector_refs；普通 modular GU 仍缺完整重训练消费者。需要最小端到端验证证明同一 Selection→GU→Retrain/Evaluation 接通。'),
        ('NOT OBSERVED（端到端验证）', '已完成的 8 项检查证明配置及失败关闭边界；015 的最小实际消费者链尚未完整验证。306/612 全量运行和正式科研结论不列作缺口。'),
        ('PASS（报告范围已纠正）', '配对报告现在审阅实验方案、实现和验证证据。Claim 保持 ongoing，等待补齐链路后再交用户验收；撤回先前要求特殊先行落地配置的确认。'),
    ]
    decision = ('Agent 判断：链路验证证据不足，继续完成同一 015 的设计与实现。用户已经明确本次范围，无需再次确认这一范围或特殊先行合入配置。'
                '015 的验收对象是实验方案、可执行链路和必要最小验证；后续真实数据 canary、SSH/GPU 与全量实验按项目规则另行明确执行范围。')
    defaults = [
        ('Dataset/Split', 'Cora / CiteSeer / PubMed；70/10/20；split seed 2024'),
        ('模型与训练', 'GCN，两层，hidden 64，dropout 0.5；100 epochs；Adam；lr 0.005；weight decay 0.000001；无 scheduler'),
        ('训练 seeds / 预算', '42、212、2024；训练候选数的 1% / 5%；floor_with_minimum_one'),
        ('Selector 默认', 'last_layer；validation-conditioned 方法使用 val_mask；LiSSA 20 / scale 25 / damp 0.01；B Hutchinson 32 probes / seed 1729'),
        ('对照与 checkpoint', 'random seed 104245；CP3=[1,50,100]；CP6=[1,10,25,50,75,100]'),
        ('GNNDelete', 'unlearn_lr 0.01；50 epochs；alpha 0.5；mse_mean / both_layerwise；Adam'),
        ('GIF', 'iteration 100；scale 1000000000；damp 0；GIF_method=GIF'),
        ('评价', 'post_unlearning_utility_and_retrain_gap；当前 modular 消费者拒绝，不降为 utility-only'),
    ]
    sharing = [
        ('训练准备', str(counts['conditional_preparation_groups']), '3 数据集 × 3 训练 seeds；checkpoint 仍需精确内容验证'),
        ('Score', str(counts['conditional_score_groups']), '15 个模型型方法 × 9，加 degree/random 各 3；Score 与预算无关'),
        ('Selection', str(counts['conditional_selection_groups']), '141 个条件 Score 组 × 2 预算；具体集合重合尚未观测'),
    ]
    gates = [
        ('已接受前置', 'PASS', '001、006、026、009 的 accepted Record 与代码均在 main@19b3b865；026 merge 为 426aebd8。'),
        ('数据与 checkpoint', '实现待办', '接通文件验证、绑定、候选构造和 checkpoint 准备；缺失身份不能用空引用或临时重切划分代替。'),
        ('S / U 消费者', '实现待办', '比较、计时及完整重训练评价接缝待完成。配置能展开不等于这些消费者已接通。'),
        ('最小链路验证', '验证待办', '在隔离最小输入上验证真实消费者和产物身份，明确软件 fixture 与正式数据的证据差别。'),
        ('正式部署与调度', '后续执行条件', 'SSH/GPU、三端同一 main、正式输入、canary 和成本审批适用于后续正式运行；不要求 015 跑完矩阵，也不阻塞本地链路实现。'),
    ]
    evidence = [
        ('配置说明与生成命令', '../../../experiments/configs/aagu015/README.md'),
        ('阶段 S 源表', '../../../experiments/configs/aagu015/stage_s.yaml'),
        ('阶段 U 源表', '../../../experiments/configs/aagu015/stage_u.yaml'),
        ('有效参数、449 份 YAML 哈希与检查摘要', 'evidence/definition-summary.json'),
        ('306 个 S cell 与条件共享依赖', 'evidence/stage-s-cells.csv'),
        ('612 个 U cell 与固定 Selection 来源', 'evidence/stage-u-cells.csv'),
        ('可重跑验证器', 'evidence/verify.py'),
        ('完整展开及逐字段来源（本地运行证据）', '../../runtime/aagu015/definition-expansion.json'),
        ('干净配置检查点的验证回执', '../../runtime/aagu015/verification.json'),
        ('更正后桌面首屏渲染', '../../runtime/aagu015/report-scope-desktop.png'),
        ('更正后窄屏渲染', '../../runtime/aagu015/report-scope-narrow.png'),
        ('更正后完整报告渲染', '../../runtime/aagu015/report-scope-full.png'),
        ('当前 WorkItem', 'WORKITEM.md'),
    ]
    verification = ('配置检查点 59baa2ae909e7fba92278d9201c635b80be65cdc 上，8 项针对性回归、324 个 parser 计划、'
                    '2 个真实 CLI dry-run 与 dashboard 校验通过。源 worktree 列入保护范围的 7 个数据/缓存/结果文件前后 SHA-256 相同；'
                    '其余缺失的保护目录仍缺失。测试只核对软件边界，不构成正式实验、计时或研究证据。'
                    '本次更正 WorkItem、配置说明、看板和报告的范围文字；配置 YAML、生成器和消费者未变，复用该检查点的定义验证，单独校验更正内容。'
                    '定义摘要中旧 blocking_inputs 是正式运行准备项，不作为更正后的 Block 完成条件。')
    render_note = ('更正后的 HTML 视觉检查：PASS（已观察范围）。已重新渲染并查看 1440×1100 桌面首屏、'
                   '600×1800 窄屏和 1440×3300 完整页面；范围说明、待办与决定区可读，没有可见重叠或横向截断。'
                   '验证仅支持当前报告的可读性，不代表链路实现完成。')
    md = [f'# {title}', '', '## Human Result', '', '### 实际增量', '', increment, '',
          '主要证据：[定义摘要](evidence/definition-summary.json) · [阶段 S cell 表](evidence/stage-s-cells.csv) · [阶段 U cell 表](evidence/stage-u-cells.csv)。',
          '', '### 核心观察', '']
    md += [f'{i}. **{status}** — {text}' for i, (status, text) in enumerate(observations, 1)]
    md += ['', '### 当前决定', '', '> 当前验收决定：`待决定`', '', decision, '']
    def md_table(heading, headers, rows):
        md.extend(['## ' + heading, '', '| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |'])
        md.extend('| ' + ' | '.join(row) + ' |' for row in rows)
        md.append('')
    md_table('默认展开与当前科研配置', ('配置项', '实际展开值'), defaults)
    md_table('条件共享依赖', ('对象', '配置组数', '解释'), sharing)
    caveat = '组标识是有效配置的比较指纹，不是 Recipe/Artifact 哈希、实际训练次数或 HIT。真实数据、候选、checkpoint 与 producer 身份一致后才允许共享。'
    md += [caveat, '']
    md_table('实现待办与后续运行边界', ('事项', '归属', '当前事实'), gates)
    md += ['## 验证与证据', '', verification, '', render_note, '']
    md += [f'- [{label}]({url})' for label, url in evidence]
    md += ['', '## 生成 YAML 示例', '']
    examples = [('阶段 S：Cora / seed42 / 1%', 'stage_s/cora-seed42-r0.01.yaml'),
                ('阶段 U：同一 degree Selection → GNNDelete / GIF', 'stage_u/cora-seed42-r0.01-degree.yaml')]
    snippets = []
    for label, relative in examples:
        content = (ROOT / 'experiments/configs/aagu015/generated' / relative).read_text(encoding='utf-8')
        snippets.append((label, content))
        md += ['### ' + label, '', '```yaml', content.rstrip(), '```', '']
    (ITEM / 'REPORT.md').write_text('\n'.join(md), encoding='utf-8')

    esc = html.escape
    def table(headers, rows):
        return '<div class="table"><table><thead><tr>' + ''.join('<th>' + esc(h) + '</th>' for h in headers) + '</tr></thead><tbody>' + ''.join(
            '<tr>' + ''.join('<td>' + esc(v) + '</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table></div>'
    body = f'<header><p class="eyebrow">AAGU-015 · 配置检查点 · ongoing</p><h1>{esc(title)}</h1></header>'
    body += '<section data-workblock-human-result="2.1"><h2>Human Result</h2><h3>实际增量</h3><p>' + esc(increment) + '</p><p>主要证据：<a href="evidence/definition-summary.json">定义摘要</a> · <a href="evidence/stage-s-cells.csv">阶段 S cell 表</a> · <a href="evidence/stage-u-cells.csv">阶段 U cell 表</a>。</p><h3>核心观察</h3><ol class="observations">'
    body += ''.join('<li><strong>' + esc(status) + '</strong><span>' + esc(text) + '</span></li>' for status, text in observations)
    body += '</ol><h3>当前决定</h3><div class="decision"><span data-workblock-decision="pending">待决定</span><p>' + esc(decision) + '</p></div></section>'
    body += '<section><h2>默认展开与当前科研配置</h2>' + table(('配置项', '实际展开值'), defaults) + '</section>'
    body += '<section><h2>条件共享依赖</h2>' + table(('对象', '配置组数', '解释'), sharing) + '<p>' + esc(caveat) + '</p></section>'
    body += '<section><h2>实现待办与后续运行边界</h2>' + table(('事项', '归属', '当前事实'), gates) + '</section>'
    body += '<section><h2>验证与证据</h2><p>' + esc(verification) + '</p><p>' + esc(render_note) + '</p><ul class="links">'
    body += ''.join('<li><a href="' + esc(url, quote=True) + '">' + esc(label) + '</a></li>' for label, url in evidence) + '</ul></section>'
    body += '<section><h2>生成 YAML 示例</h2>' + ''.join('<details><summary>' + esc(label) + '</summary><pre>' + esc(content) + '</pre></details>' for label, content in snippets) + '</section>'
    style = '''*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#202b38;font:15px/1.65 "Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1160px;margin:auto;padding:30px 32px 70px}header{margin-bottom:24px}h1{font-size:30px;line-height:1.3;margin:8px 0}h2{font-size:21px;margin:0 0 18px}h3{font-size:16px;margin:16px 0 7px}p{margin:7px 0 14px}.eyebrow{color:#45647c;font-size:13px;letter-spacing:.08em}section{background:white;padding:26px 30px;border:1px solid #dfe5e9;border-radius:12px;margin-bottom:22px}.observations{padding-left:23px;margin:5px 0}.observations li{padding:5px 0}.observations strong{font-size:12px;color:#53697a;margin-right:10px}.decision{background:#fff7e5;border-left:4px solid #bc8424;padding:14px 18px}.decision span{font-weight:700;color:#7e5617}.decision p{margin:5px 0 0}.table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:11px 12px;border-bottom:1px solid #e4e9ed;vertical-align:top}th{background:#f1f5f8}td:first-child{font-weight:600;min-width:115px}a{color:#14698f;text-underline-offset:3px;overflow-wrap:anywhere}.links{padding-left:23px}.links li{margin:6px 0}details{border:1px solid #dce4ea;border-radius:8px;margin:12px 0}summary{padding:13px;cursor:pointer;font-weight:600}pre{font:12px/1.6 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;padding:18px;background:#f5f8fa;margin:0}@media(max-width:640px){main{padding:18px 12px}h1{font-size:24px}section{padding:20px 17px}body{font-size:14px}.observations strong{display:block}th,td{padding:9px}td:first-child{min-width:75px}}'''
    (ITEM / 'REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + esc(title) + '</title><style>' + style + '</style><main>' + body + '</main></html>', encoding='utf-8')


if __name__ == '__main__':
    main()
